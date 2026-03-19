#!/usr/bin/env python3
"""
使用 GitHub 搜索 API 获取 JDK 26 的 PR 列表
"""

import requests
import json
import time
from collections import defaultdict
from datetime import datetime

GITHUB_API = "https://api.github.com"

def search_prs(query, page=1, per_page=100):
    """使用搜索 API 获取 PRs"""
    url = f"{GITHUB_API}/search/issues"
    params = {
        'q': query,
        'page': page,
        'per_page': per_page,
    }
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data.get('items', [])
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_pr_details(owner, repo, number):
    """获取单个 PR 的详细信息"""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{number}"
    headers = {
        'Accept': 'application/vnd.github.v3+json',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching PR #{number}: {e}")
        return None

def main():
    print("Fetching JDK 26 PRs using GitHub Search API...")
    
    # 搜索查询: repo:openjdk/jdk is:pr is:merged merged:>=2024-10-01
    query = "repo:openjdk/jdk is:pr is:merged merged:>=2024-10-01"
    
    all_prs = []
    page = 1
    
    while True:
        print(f"Fetching page {page}...")
        items = search_prs(query, page=page)
        
        if not items:
            break
        
        for item in items:
            number = item.get('number')
            print(f"  Processing PR #{number}...")
            
            # 获取详细信息
            details = get_pr_details('openjdk', 'jdk', number)
            
            if details:
                all_prs.append({
                    'number': number,
                    'title': item.get('title', ''),
                    'author': item.get('user', {}).get('login', 'unknown'),
                    'merged_at': details.get('merged_at', ''),
                    'additions': details.get('additions', 0),
                    'deletions': details.get('deletions', 0),
                    'labels': [l['name'] for l in item.get('labels', [])],
                    'html_url': item.get('html_url', ''),
                    'body': item.get('body', '')[:500] if item.get('body') else '',
                })
        
        page += 1
        time.sleep(2)  # 搜索 API 限制更严格
        
        if page > 10:  # GitHub 搜索 API 最多返回 1000 条
            print("Reached search API limit (1000 items)")
            break
    
    print(f"\nFetched {len(all_prs)} PRs")
    
    if all_prs:
        # 保存数据
        with open('prs/jdk26-prs.json', 'w') as f:
            json.dump(all_prs, f, indent=2)
        print("Data saved to prs/jdk26-prs.json")

if __name__ == '__main__':
    main()
