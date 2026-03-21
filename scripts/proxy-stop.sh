#!/bin/bash
# Stop transparent proxy

echo "=== Stopping Transparent Proxy ==="

# Remove iptables rules
iptables -t nat -D OUTPUT -p tcp -m owner ! --uid-owner root -j REDSOCKS 2>/dev/null || true
iptables -t nat -F REDSOCKS 2>/dev/null || true
iptables -t nat -X REDSOCKS 2>/dev/null || true
echo "iptables rules removed"

# Stop redsocks
systemctl stop redsocks 2>/dev/null || true
echo "redsocks stopped"

# Kill SSH tunnel
pkill -f "ssh.*-D.*1080" 2>/dev/null || true
echo "SSH tunnel stopped"

echo ""
echo "=== Transparent Proxy Stopped ==="