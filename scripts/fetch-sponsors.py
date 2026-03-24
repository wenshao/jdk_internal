#!/usr/bin/env python3
"""
Incremental GitHub sponsor fetcher for OpenJDK PR archive.
Finds /sponsor commands in PR comments.

Usage:
    python3 scripts/fetch-sponsors.py [--limit 4000] [--apply]
"""
import csv, json, subprocess, re, time, sys, os, argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CSV_FILE = os.path.join(ROOT_DIR, 'by-pr/all-integrated-prs.csv')
CACHE_FILE = os.path.join(ROOT_DIR, 'scripts/.sponsor-cache.json')

def load_cache():
    try:
        with open(CACHE_FILE) as f: return json.load(f)
    except: return {}

def save_cache(cache):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, 'w') as f: json.dump(cache, f)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--limit', type=int, default=4000)
    p.add_argument('--apply', action='store_true')
    args = p.parse_args()
    
    cache = load_cache()
    with open(CSV_FILE) as f: rows = list(csv.DictReader(f))
    
    needed = [r['pr_number'] for r in rows if r.get('pr_number') and r['pr_number'] not in cache]
    to_fetch = needed[:args.limit]
    
    print(f"Cache: {len(cache)}, Remaining: {len(needed)}, This run: {len(to_fetch)}")
    
    count = 0
    for i, pr_num in enumerate(to_fetch):
        try:
            result = subprocess.run(
                ['gh', 'api', f'repos/openjdk/jdk/issues/{pr_num}/comments',
                 '--jq', '[.[] | select(.body | test("/sponsor")) | .user.login] | first // ""'],
                capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                cache[pr_num] = result.stdout.strip()
                count += 1
            elif '403' in result.stderr:
                print(f"Rate limited at {count}")
                break
        except: pass
        
        if (i+1) % 200 == 0:
            print(f"  [{i+1}/{len(to_fetch)}] fetched={count}")
            save_cache(cache)
    
    save_cache(cache)
    sponsored = sum(1 for v in cache.values() if v)
    print(f"Done: {count} new, {len(cache)} total, {sponsored} with sponsors")
    
    if args.apply:
        for row in rows:
            pr_num = row.get('pr_number', '')
            if pr_num in cache and cache[pr_num]:
                row['sponsor'] = cache[pr_num]
            else:
                row['sponsor'] = ''
        # Add sponsor field if not exists
        fieldnames = list(rows[0].keys())
        if 'sponsor' not in fieldnames:
            fieldnames.append('sponsor')
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(rows)
        print("Applied to CSV")

if __name__ == '__main__':
    main()
