#!/usr/bin/env python3
"""
Incremental JBS data fetcher for OpenJDK PR archive.
Fetches priority, component, fix_version, labels from bugs.openjdk.org.

Usage:
    python3 scripts/fetch-jbs-data.py [--limit 1000] [--delay 0.5]

Cache: /tmp/jbs_cache.json (incremental, survives across runs)
Output: Updates by-pr/all-integrated-prs.csv
"""

import csv, json, urllib.request, time, sys, os, argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CSV_FILE = os.path.join(ROOT_DIR, 'by-pr/all-integrated-prs.csv')
CACHE_FILE = os.path.join(ROOT_DIR, 'scripts/.jbs-cache.json')

def parse_args():
    p = argparse.ArgumentParser(description='Fetch JBS data for PR archive')
    p.add_argument('--limit', type=int, default=1000, help='Max entries to fetch this run')
    p.add_argument('--delay', type=float, default=0.5, help='Delay between requests (seconds)')
    p.add_argument('--timeout', type=int, default=15, help='HTTP timeout (seconds)')
    p.add_argument('--apply', action='store_true', help='Apply cache to CSV after fetching')
    return p.parse_args()

def load_cache():
    try:
        with open(CACHE_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_cache(cache):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

def fetch_jbs(bugid, timeout=15):
    url = f"https://bugs.openjdk.org/rest/api/2/issue/JDK-{bugid}?fields=priority,components,fixVersions,labels"
    req = urllib.request.Request(url, headers={
        'Accept': 'application/json',
        'User-Agent': 'OpenJDK-PR-Archive/1.0'
    })
    resp = urllib.request.urlopen(req, timeout=timeout)
    data = json.loads(resp.read())
    fields = data.get('fields', {})
    return {
        'priority': fields.get('priority', {}).get('name', '') if fields.get('priority') else '',
        'component': '/'.join(c['name'] for c in fields.get('components', [])),
        'fix_version': ', '.join(v['name'] for v in fields.get('fixVersions', [])),
        'labels': ','.join(fields.get('labels', [])),
    }

def apply_to_csv(cache):
    with open(CSV_FILE) as f:
        rows = list(csv.DictReader(f))
    
    applied = 0
    for row in rows:
        bugid = row.get('bug_id', '')
        if bugid in cache and cache[bugid].get('priority'):
            j = cache[bugid]
            row['jbs_priority'] = j.get('priority', '')
            row['jbs_component'] = j.get('component', '')
            row['jbs_fix_version'] = j.get('fix_version', '')
            row['jbs_labels'] = j.get('labels', '')
            applied += 1
    
    fieldnames = list(rows[0].keys()) if rows else []
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Applied {applied} JBS entries to CSV")

def main():
    args = parse_args()
    cache = load_cache()
    
    with open(CSV_FILE) as f:
        rows = list(csv.DictReader(f))
    
    # Find unfetched bug IDs
    needed = [r['bug_id'] for r in rows 
              if r.get('bug_id') and len(r['bug_id']) == 7 
              and r['bug_id'] not in cache]
    
    total_needed = len(needed)
    to_fetch = needed[:args.limit]
    
    print(f"Cache: {len(cache)} entries")
    print(f"Remaining: {total_needed} entries")
    print(f"This run: {len(to_fetch)} entries (limit={args.limit})")
    print(f"Delay: {args.delay}s, Timeout: {args.timeout}s")
    print()
    
    success = 0
    fail = 0
    start = time.time()
    
    for i, bugid in enumerate(to_fetch):
        try:
            cache[bugid] = fetch_jbs(bugid, timeout=args.timeout)
            success += 1
        except Exception as e:
            cache[bugid] = {'priority': '', 'component': '', 'fix_version': '', 'labels': ''}
            fail += 1
            time.sleep(args.delay * 2)  # Extra delay on failure
        
        if (i + 1) % 100 == 0:
            elapsed = time.time() - start
            rate = (i + 1) / elapsed * 60
            remaining_time = (len(to_fetch) - i - 1) / rate if rate > 0 else 0
            print(f"  [{i+1}/{len(to_fetch)}] success={success} fail={fail} rate={rate:.1f}/min ETA={remaining_time:.0f}min")
            save_cache(cache)
        
        time.sleep(args.delay)
    
    save_cache(cache)
    elapsed = time.time() - start
    
    print(f"\nDone: {success} success, {fail} fail in {elapsed:.0f}s ({(success+fail)/elapsed*60:.1f} req/min)")
    print(f"Cache now: {len(cache)} entries, remaining: {total_needed - len(to_fetch)}")
    
    if args.apply:
        apply_to_csv(cache)

if __name__ == '__main__':
    main()
