#!/bin/bash
# Transparent proxy setup script
# Routes non-China traffic through SSH SOCKS proxy

PROXY_IP="43.106.142.110"
LOCAL_NET="192.168.0.0/16"
REDSOCKS_PORT=12345

# Create new chain for redsocks
iptables -t nat -N REDSOCKS 2>/dev/null || iptables -t nat -F REDSOCKS

# Exclude local network
iptables -t nat -A REDSOCKS -d 0.0.0.0/8 -j RETURN
iptables -t nat -A REDSOCKS -d 10.0.0.0/8 -j RETURN
iptables -t nat -A REDSOCKS -d 127.0.0.0/8 -j RETURN
iptables -t nat -A REDSOCKS -d 169.254.0.0/16 -j RETURN
iptables -t nat -A REDSOCKS -d 172.16.0.0/12 -j RETURN
iptables -t nat -A REDSOCKS -d 192.168.0.0/16 -j RETURN
iptables -t nat -A REDSOCKS -d 224.0.0.0/4 -j RETURN
iptables -t nat -A REDSOCKS -d 240.0.0.0/4 -j RETURN

# Exclude proxy server (prevent loop)
iptables -t nat -A REDSOCKS -d $PROXY_IP -j RETURN

# Exclude China IPs
iptables -t nat -A REDSOCKS -m set --match-set china dst -j RETURN

# Redirect remaining traffic to redsocks
iptables -t nat -A REDSOCKS -p tcp -j REDIRECT --to-ports $REDSOCKS_PORT

# Apply to all outgoing TCP traffic (except local user)
iptables -t nat -A OUTPUT -p tcp -m owner ! --uid-owner root -j REDSOCKS

echo "Transparent proxy configured!"
echo "Test with: curl -4 ifconfig.me"
