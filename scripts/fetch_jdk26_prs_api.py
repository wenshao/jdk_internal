#!/usr/bin/env python3
"""
使用 GitHub REST API 获取 JDK 26 的 PR 列表
无需认证，使用公开 API
"""

import requests
import json
import time
from collections import defaultdict
from datetime import datetime

GITHUB_API = "https://api.github.com"

def fetch_prs_page(page=1, per_page=100):
    """获取一页 PRs"""
    url = f"{GITHUB_API}/repos/openjdk/jdk/pulls"
    params = {
        'state': 'closed',
        'base': 'master',
        'sort': 'updated',
        'direction': 'desc',
        'page': page,
        'per_page': per_page,
    }
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching page {page}: {e}")
        return None

def fetch_prs_since(start_date="2024-10-01", max_pages=30):
    """获取指定日期之后的 PRs"""
    all_prs = []
    
    for page in range(1, max_pages + 1):
        print(f"Fetching page {page}...")
        prs = fetch_prs_page(page)
        
        if not prs:
            break
        
        # 过滤已合并的 PRs
        merged_prs = [pr for pr in prs if pr.get('merged_at')]
        
        # 检查日期
        stop = False
        for pr in merged_prs:
            merged_at = pr.get('merged_at', '')
            if merged_at and merged_at[:10] >= start_date:
                all_prs.append({
                    'number': pr['number'],
                    'title': pr['title'],
                    'author': pr['user']['login'],
                    'merged_at': merged_at,
                    'additions': pr.get('additions', 0),
                    'deletions': pr.get('deletions', 0),
                    'labels': [l['name'] for l in pr.get('labels', [])],
                    'html_url': pr['html_url'],
                })
            else:
                stop = True
                break
        
        if stop:
            break
        
        time.sleep(0.5)  # 避免请求过快
    
    return all_prs

def categorize_prs(prs):
    """分类 PRs"""
    component_keywords = {
        'gc': ['G1', 'ZGC', 'Shenandoah', 'gc', 'garbage', 'ParallelGC', 'SerialGC'],
        'compiler': ['compiler', 'C2', 'C1', 'JIT', 'intrinsic', 'Graal', 'aot', 'superword'],
        'network': ['http', 'net', 'socket', 'WebSocket', 'QUIC', 'HttpClient', 'HTTP/'],
        'security': ['crypto', 'security', 'TLS', 'SSL', 'key', 'cipher', 'signature', 'ML-DSA', 'ML-KEM'],
        'core': ['lang', 'util', 'reflect', 'String', 'Object', 'collection', 'ArrayList'],
        'concurrency': ['thread', 'concurrent', 'lock', 'atomic', 'virtual', 'Thread'],
        'jfr': ['jfr', 'flight recorder', 'event'],
        'build': ['build', 'make', 'configure', 'cmake', 'icf'],
        'test': ['test', 'jtreg'],
    }
    
    by_component = defaultdict(list)
    by_author = defaultdict(list)
    by_month = defaultdict(list)
    
    for pr in prs:
        title = pr.get('title', '').lower()
        
        matched = False
        for comp, keywords in component_keywords.items():
            for kw in keywords:
                if kw.lower() in title:
                    by_component[comp].append(pr)
                    matched = True
                    break
            if matched:
                break
        
        if not matched:
            by_component['other'].append(pr)
        
        author = pr.get('author', 'unknown')
        by_author[author].append(pr)
        
        merged_at = pr.get('merged_at', '')
        if merged_at:
            month = merged_at[:7]
            by_month[month].append(pr)
    
    return {
        'by_component': by_component,
        'by_author': by_author,
        'by_month': by_month,
    }

def generate_report(prs, categories):
    """生成报告"""
    total = len(prs)
    
    report = f"""# JDK 26 PR 分析报告

> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
> 总 PR 数: {total}

---

## 统计概览

### 按组件分布

| 组件 | PR 数 | 占比 |
|------|-------|------|
"""
    
    for comp, items in sorted(categories['by_component'].items(), 
                              key=lambda x: -len(x[1])):
        pct = len(items) / total * 100
        report += f"| {comp} | {len(items)} | {pct:.1f}% |\n"
    
    report += """
### 按月份分布

| 月份 | PR 数 |
|------|-------|
"""
    
    for month, items in sorted(categories['by_month'].items()):
        report += f"| {month} | {len(items)} |\n"
    
    report += """
### Top 30 贡献者

| 排名 | 作者 | PR 数 |
|------|------|-------|
"""
    
    for i, (author, items) in enumerate(
            sorted(categories['by_author'].items(), key=lambda x: -len(x[1]))[:30], 1):
        report += f"| {i} | @{author} | {len(items)} |\n"
    
    # 各组件详情
    report += "\n---\n\n## 各组件 PR 列表\n"
    
    component_order = ['gc', 'compiler', 'network', 'security', 'core', 
                       'concurrency', 'jfr', 'build']
    
    for comp in component_order:
        if comp in categories['by_component']:
            items = categories['by_component'][comp]
            report += f"\n### {comp.upper()} ({len(items)} PRs)\n\n"
            
            sorted_items = sorted(items, 
                                 key=lambda x: x.get('additions', 0) + x.get('deletions', 0),
                                 reverse=True)
            
            for pr in sorted_items[:50]:
                num = pr.get('number', 0)
                title = pr.get('title', '')[:70]
                author = pr.get('author', 'unknown')
                adds = pr.get('additions', 0)
                dels = pr.get('deletions', 0)
                report += f"- [#{num}](./8{str(num)[:3]}/{num}.md) {title} (+{adds}/-{dels}) @{author}\n"
            
            if len(items) > 50:
                report += f"\n*... 还有 {len(items) - 50} 个 PRs*\n"
    
    return report

def main():
    print("Fetching JDK 26 PRs from GitHub API...")
    
    # 获取 PRs (从 2024-10-01 开始)
    prs = fetch_prs_since("2024-10-01", max_pages=50)
    
    print(f"\nFetched {len(prs)} PRs")
    
    if not prs:
        print("No PRs fetched")
        return
    
    # 分类
    categories = categorize_prs(prs)
    
    # 保存原始数据
    with open('prs/jdk26-prs.json', 'w') as f:
        json.dump(prs, f, indent=2)
    print("Data saved to prs/jdk26-prs.json")
    
    # 生成报告
    report = generate_report(prs, categories)
    with open('prs/jdk26-prs.md', 'w') as f:
        f.write(report)
    print("Report saved to prs/jdk26-prs.md")
    
    # 打印统计
    print("\n" + "="*50)
    print("统计:")
    print("="*50)
    for comp, items in sorted(categories['by_component'].items(), 
                              key=lambda x: -len(x[1]))[:10]:
        print(f"  {comp}: {len(items)}")

if __name__ == '__main__':
    main()
