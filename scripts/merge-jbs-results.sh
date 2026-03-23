#!/bin/bash
# Merge JBS results from 3 machines into the main cache
# Run after all 3 fetch processes complete

echo "=== Fetching results from remote machines ==="
scp root@172.16.172.143:/tmp/jbs_result2.json /tmp/ 2>/dev/null && echo "  Got result2 from 172.16.172.143" || echo "  FAILED: 172.16.172.143"
scp root@8.136.39.6:/tmp/jbs_result3.json /tmp/ 2>/dev/null && echo "  Got result3 from 8.136.39.6" || echo "  FAILED: 8.136.39.6"

echo ""
echo "=== Merging ==="
python3 << 'PYEOF'
import json, os

CACHE = 'scripts/.jbs-cache.json'
PARTS = ['/tmp/jbs_result1.json', '/tmp/jbs_result2.json', '/tmp/jbs_result3.json']

# Load existing cache
try:
    with open(CACHE) as f: cache = json.load(f)
except: cache = {}

before = len(cache)

# Merge each part
for part in PARTS:
    if os.path.exists(part):
        with open(part) as f: data = json.load(f)
        for k, v in data.items():
            if v.get('priority'):  # Only merge entries with actual data
                cache[k] = v
        print(f"  {part}: {len(data)} entries")
    else:
        print(f"  {part}: NOT FOUND")

after = len(cache)
with open(CACHE, 'w') as f: json.dump(cache, f)
print(f"\nMerged: {before} → {after} (+{after-before} new)")

# Apply to CSV
print("\nApplying to CSV...")
os.system('python3 scripts/fetch-jbs-data.py --limit 0 --apply')
PYEOF
