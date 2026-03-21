#!/usr/bin/env python3
"""
Count integrated PRs for OpenJDK contributors.

Usage: python3 count_prs.py
"""

import urllib.request
import json
import time

# GitHub usernames mapped to real names and organizations
CONTRIBUTORS = {
    # Oracle
    'shipilev': ('Aleksey Shipilev', 'Amazon'),
    'albertnetymk': ('Albert Mingkun Yang', 'Oracle'),
    'naotoj': ('Naoto Sato', 'Oracle'),
    'liach': ('Chen Liang', 'Oracle'),
    'merykitty': ('Hamlin Li', 'Oracle'),
    'YaSuenag': ('Yasumasa Suenaga', 'Oracle'),
    'sendaoYan': ('Sendao Yan', 'Oracle'),
    
    # Alibaba
    'wenshao': ('Shaojin Wen', 'Alibaba'),
    'kuaiwei': ('Kuai Wei', 'Alibaba'),
    
    # ByteDance
    'Anjian-Wen': ('Anjian Wen', 'ByteDance'),
    
    # ISCAS
    'DingliZhang': ('Dingli Zhang', 'ISCAS'),

    # Huawei
    'RealFYang': ('Fei Yang', 'Huawei'),
    
    # Red Hat
    'rgiulietti': ('Raffaello Giulietti', 'Red Hat'),
}

def get_integrated_pr_count(username):
    """Get integrated PR count for a GitHub user."""
    url = f"https://api.github.com/search/issues?q=repo:openjdk/jdk+author:{username}+type:pr+label:integrated"
    
    try:
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/vnd.github.v3+json')
        req.add_header('User-Agent', 'OpenJDK-Stats-Script')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            return data.get('total_count', 0)
    except Exception as e:
        print(f"  Error for {username}: {e}")
        return 0

def main():
    print("OpenJDK Integrated PR Counts")
    print("=" * 60)
    
    results = []
    
    for username, (real_name, org) in CONTRIBUTORS.items():
        print(f"Fetching {username} ({real_name}, {org})...", end=" ", flush=True)
        count = get_integrated_pr_count(username)
        print(f"{count} PRs")
        results.append((username, real_name, org, count))
        time.sleep(0.5)  # Rate limiting
    
    print("\n" + "=" * 60)
    print("By Organization:")
    print("-" * 60)
    
    # Group by org
    org_totals = {}
    for username, real_name, org, count in results:
        if org not in org_totals:
            org_totals[org] = []
        org_totals[org].append((username, real_name, count))
    
    for org in sorted(org_totals.keys()):
        total = sum(c for _, _, c in org_totals[org])
        print(f"\n{org} ({total} PRs):")
        for username, real_name, count in sorted(org_totals[org], key=lambda x: -x[2]):
            print(f"  {count:4} | {real_name:25} (@{username})")
    
    print("\n" + "=" * 60)
    print("All Contributors (sorted by PRs):")
    print("-" * 60)
    for username, real_name, org, count in sorted(results, key=lambda x: -x[3]):
        print(f"{count:4} | {real_name:25} (@{username}) | {org}")

if __name__ == '__main__':
    main()