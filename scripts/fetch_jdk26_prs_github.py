#!/usr/bin/env python3
"""
使用 GitHub API 获取 JDK 26 的 PR 列表
"""

import subprocess
import json
import sys
from collections import defaultdict
from datetime import datetime

def fetch_prs_via_gh():
    """使用 gh CLI 获取 PR 列表"""
    print("Fetching JDK 26 PRs from GitHub...")
    
    # 使用 gh CLI 获取 PRs
    # 注意: 需要先 gh auth login
    cmd = [
        'gh', 'pr', 'list',
        '--repo', 'openjdk/jdk',
        '--state', 'merged',
        '--limit', '3000',
        '--json', 'number,title,author,labels,additions,deletions,mergedAt,baseRefName',
        '--search', 'is:merged base:master merged:>=2024-10-01'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return None
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        print("Timeout fetching PRs")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def categorize_prs(prs):
    """分类 PRs"""
    
    # 组件关键词
    component_keywords = {
        'gc': ['G1', 'ZGC', 'Shenandoah', 'gc', 'garbage', 'ParallelGC'],
        'compiler': ['compiler', 'C2', 'C1', 'JIT', 'intrinsic', 'Graal', 'aot'],
        'network': ['http', 'net', 'socket', 'WebSocket', 'QUIC'],
        'security': ['crypto', 'security', 'TLS', 'SSL', 'key', 'cipher'],
        'core': ['lang', 'util', 'reflect', 'String', 'Object', 'collection'],
        'concurrency': ['thread', 'concurrent', 'lock', 'atomic', 'virtual'],
        'jfr': ['jfr', 'flight recorder', 'event'],
        'build': ['build', 'make', 'configure', 'cmake'],
        'test': ['test', 'jtreg'],
    }
    
    by_component = defaultdict(list)
    by_author = defaultdict(list)
    by_month = defaultdict(list)
    
    for pr in prs:
        title = pr.get('title', '').lower()
        
        # 分类到组件
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
        
        # 按作者分类
        author = pr.get('author', {}).get('login', 'unknown')
        by_author[author].append(pr)
        
        # 按月份分类
        merged_at = pr.get('mergedAt', '')
        if merged_at:
            month = merged_at[:7]  # YYYY-MM
            by_month[month].append(pr)
    
    return {
        'by_component': by_component,
        'by_author': by_author,
        'by_month': by_month,
    }

def generate_report(prs, categories):
    """生成报告"""
    
    report = f"""# JDK 26 PR 分析报告

> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
> 总 PR 数: {len(prs)}

---

## 统计概览

### 按组件分布

| 组件 | PR 数 | 占比 |
|------|-------|------|
"""
    
    total = len(prs)
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
### Top 20 贡献者

| 排名 | 作者 | PR 数 |
|------|------|-------|
"""
    
    for i, (author, items) in enumerate(
            sorted(categories['by_author'].items(), key=lambda x: -len(x[1]))[:20], 1):
        report += f"| {i} | @{author} | {len(items)} |\n"
    
    # 各组件详情
    report += "\n---\n\n## 各组件详情\n"
    
    for comp in ['gc', 'compiler', 'network', 'security', 'core', 'concurrency']:
        if comp in categories['by_component']:
            items = categories['by_component'][comp]
            report += f"\n### {comp.upper()} ({len(items)} PRs)\n\n"
            
            # 按变更大小排序
            sorted_items = sorted(items, 
                                 key=lambda x: x.get('additions', 0) + x.get('deletions', 0),
                                 reverse=True)
            
            for pr in sorted_items[:20]:
                num = pr.get('number', 0)
                title = pr.get('title', '')[:60]
                author = pr.get('author', {}).get('login', 'unknown')
                adds = pr.get('additions', 0)
                dels = pr.get('deletions', 0)
                report += f"- [#{num}](https://github.com/openjdk/jdk/pull/{num}) {title} (+{adds}/-{dels}) @{author}\n"
            
            if len(items) > 20:
                report += f"\n*... 还有 {len(items) - 20} 个 PRs*\n"
    
    return report

def main():
    # 获取 PRs
    prs = fetch_prs_via_gh()
    
    if not prs:
        print("Failed to fetch PRs. Trying alternative method...")
        # 可以在这里添加备用方法
        return
    
    print(f"Fetched {len(prs)} PRs")
    
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
