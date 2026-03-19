#!/usr/bin/env python3
"""
GitHub PR Counter for OpenJDK Contributors

Uses GitHub search API to count integrated PRs for each contributor.
"""

import subprocess
import json
import urllib.request
import urllib.error
import time
import sys

# GitHub usernames for contributors (manually curated)
GITHUB_USERS = {
    # Alibaba
    'wenshao': 'Shaojin Wen',
    'kuaiwei': 'Kuai Wei',
    'YudeLin': 'Yude Lin',
    
    # Tencent
    'bobpengxie': 'Bob Peng Xie',
    'casparcwang': 'Caspar Wang',
    'tobytbzhang': 'Tongbao Zhang',
    'emoryzheng': 'Miao Zheng',
    
    # Loongson
    'sunguoyun': 'Guoyun Sun',
    'aoqi': 'Qi Ao',
    
    # ByteDance
    'Anjian-Wen': 'Anjian Wen',
    
    # Oracle China
    'weijunwang': 'Weijun Wang',
    'ayang': 'Albert Mingkun Yang',
    'mlch': 'Hamlin Li',
    'liach': 'Chen Liang',
    'sya': 'SendaoYan',
}

def get_pr_count(username):
    """Get integrated PR count for a GitHub user"""
    url = f"https://api.github.com/search/issues?q=repo:openjdk/jdk+type:pr+author:{username}+is:merged"
    
    try:
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/vnd.github.v3+json')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            return data.get('total_count', 0)
    except urllib.error.HTTPError as e:
        print(f"  Error for {username}: {e.code}", file=sys.stderr)
        return 0
    except Exception as e:
        print(f"  Error for {username}: {e}", file=sys.stderr)
        return 0

def main():
    print("GitHub PR Counts for OpenJDK Contributors")
    print("=" * 50)
    
    results = []
    
    for username, real_name in GITHUB_USERS.items():
        print(f"Fetching {username} ({real_name})...", end=" ", flush=True)
        count = get_pr_count(username)
        print(f"{count} PRs")
        results.append((username, real_name, count))
        time.sleep(1)  # Rate limiting
    
    print("\n" + "=" * 50)
    print("Summary:")
    print("-" * 50)
    
    # Sort by PR count
    results.sort(key=lambda x: -x[2])
    
    for username, real_name, count in results:
        print(f"{count:4} | {real_name:20} (@{username})")

if __name__ == '__main__':
    main()