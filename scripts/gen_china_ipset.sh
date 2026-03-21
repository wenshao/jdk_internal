#!/bin/bash
# Generate China IP list for ipset

INPUT="/tmp/apnic.txt"
OUTPUT="/tmp/china_ip_list.txt"

# Parse APNIC data and convert to CIDR
awk -F'|' '
/^apnic\|CN\|ipv4\|/ {
    ip = $4
    count = $5
    # Calculate CIDR prefix length
    cidr = 32 - int(log(count)/log(2))
    print ip "/" cidr
}
' "$INPUT" > "$OUTPUT"

echo "Generated $(wc -l < $OUTPUT) China IP ranges"