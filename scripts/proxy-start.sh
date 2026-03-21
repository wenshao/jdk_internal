#!/bin/bash
# Start transparent proxy for international traffic
# All non-China TCP traffic will go through SSH SOCKS proxy

set -e

PROXY_SERVER="43.106.142.110"
SOCKS_PORT=1080
REDSOCKS_PORT=12345

echo "=== Starting Transparent Proxy ==="

# 1. Start SSH tunnel (SOCKS proxy)
if pgrep -f "ssh.*-D.*${SOCKS_PORT}" > /dev/null; then
    echo "SSH tunnel already running"
else
    echo "Starting SSH tunnel to $PROXY_SERVER..."
    ssh -f -N -D 127.0.0.1:${SOCKS_PORT} \
        -o ServerAliveInterval=60 \
        -o ServerAliveCountMax=3 \
        -o StrictHostKeyChecking=no \
        root@${PROXY_SERVER}
    sleep 2
    echo "SSH tunnel started on port $SOCKS_PORT"
fi

# 2. Load ipset (China IPs)
if ipset list china > /dev/null 2>&1; then
    echo "ipset 'china' already loaded"
else
    echo "Loading China IP list..."
    ipset restore < /etc/ipset.conf
    echo "Loaded $(ipset list china | grep 'Number of entries' | awk '{print $4}') China IP ranges"
fi

# 3. Start redsocks
systemctl is-active redsocks > /dev/null 2>&1 || systemctl start redsocks
echo "redsocks started on port $REDSOCKS_PORT"

# 4. Configure iptables
echo "Configuring iptables..."

# Create REDSOCKS chain if not exists
iptables -t nat -N REDSOCKS 2>/dev/null || iptables -t nat -F REDSOCKS

# Exclude local/private networks
iptables -t nat -A REDSOCKS -d 0.0.0.0/8 -j RETURN
iptables -t nat -A REDSOCKS -d 10.0.0.0/8 -j RETURN
iptables -t nat -A REDSOCKS -d 127.0.0.0/8 -j RETURN
iptables -t nat -A REDSOCKS -d 169.254.0.0/16 -j RETURN
iptables -t nat -A REDSOCKS -d 172.16.0.0/12 -j RETURN
iptables -t nat -A REDSOCKS -d 192.168.0.0/16 -j RETURN
iptables -t nat -A REDSOCKS -d 224.0.0.0/4 -j RETURN
iptables -t nat -A REDSOCKS -d 240.0.0.0/4 -j RETURN

# Exclude proxy server (prevent loop)
iptables -t nat -A REDSOCKS -d ${PROXY_SERVER} -j RETURN

# Exclude China IPs (direct connection)
iptables -t nat -A REDSOCKS -m set --match-set china dst -j RETURN

# Redirect remaining TCP traffic to redsocks
iptables -t nat -A REDSOCKS -p tcp -j REDIRECT --to-ports ${REDSOCKS_PORT}

# Apply to OUTPUT chain (exclude root user to maintain SSH connection)
iptables -t nat -C OUTPUT -p tcp -m owner ! --uid-owner root -j REDSOCKS 2>/dev/null || \
    iptables -t nat -A OUTPUT -p tcp -m owner ! --uid-owner root -j REDSOCKS

echo ""
echo "=== Transparent Proxy Started ==="
echo "Test commands:"
echo "  su - testuser -c 'curl -4 ifconfig.me'     # Should show: $PROXY_SERVER"
echo "  su - testuser -c 'curl -4 www.baidu.com'   # Should work (direct)"