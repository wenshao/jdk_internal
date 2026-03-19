#!/usr/bin/env python3
"""
从本地 JDK git 仓库获取 JDK 26 的 commit 信息
"""

import subprocess
import re
import json
from collections import defaultdict
from datetime import datetime

def get_commits_from_git(repo_path, since="2025-06-01", until="2026-04-01"):
    """从 git 仓库获取 commits"""
    cmd = [
        'git', 'log',
        f'--since={since}',
        f'--until={until}',
        '--pretty=format:%H%n%s%n%an%n%ae%n%ai%n%n',
        '--numstat',
    ]
    
    print(f"Running: git log --since={since} --until={until}")
    result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return []
    
    return parse_git_log(result.stdout)

def parse_git_log(output):
    """解析 git log 输出"""
    commits = []
    current_commit = None
    
    lines = output.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            i += 1
            continue
        
        # 新 commit 开始 (40 字符的 hash)
        if len(line) == 40 and re.match(r'^[a-f0-9]+$', line):
            if current_commit:
                commits.append(current_commit)
            
            current_commit = {
                'hash': line,
                'subject': '',
                'author': '',
                'email': '',
                'date': '',
                'files': [],
                'additions': 0,
                'deletions': 0,
                'issue': None,
            }
            i += 1
            
            # 读取 subject
            if i < len(lines):
                current_commit['subject'] = lines[i].strip()
                # 提取 issue 号
                match = re.search(r'(\d{6,}):', current_commit['subject'])
                if match:
                    current_commit['issue'] = int(match.group(1))
                i += 1
            
            # 读取 author
            if i < len(lines):
                current_commit['author'] = lines[i].strip()
                i += 1
            
            # 读取 email
            if i < len(lines):
                current_commit['email'] = lines[i].strip()
                i += 1
            
            # 读取 date
            if i < len(lines):
                current_commit['date'] = lines[i].strip()[:10]
                i += 1
            
            # 跳过空行
            while i < len(lines) and not lines[i].strip():
                i += 1
            
            # 读取文件变更
            while i < len(lines) and lines[i].strip():
                parts = lines[i].split('\t')
                if len(parts) >= 3:
                    adds = int(parts[0]) if parts[0] != '-' else 0
                    dels = int(parts[1]) if parts[1] != '-' else 0
                    file = parts[2]
                    current_commit['files'].append(file)
                    current_commit['additions'] += adds
                    current_commit['deletions'] += dels
                i += 1
        else:
            i += 1
    
    if current_commit:
        commits.append(current_commit)
    
    return commits

def categorize_commits(commits):
    """分类 commits"""
    component_keywords = {
        'gc': ['g1', 'zgc', 'shenandoah', 'gc/', 'garbage', 'parallelgc', 'heap'],
        'compiler': ['compiler', 'opto/', 'c2', 'c1', 'jit', 'intrinsic', 'graal', 'aot'],
        'network': ['http', 'net/', 'socket', 'websocket', 'quic'],
        'security': ['crypto', 'security', 'tls', 'ssl', 'key', 'cipher', 'signature'],
        'core': ['java.base', 'lang', 'util', 'reflect', 'string'],
        'concurrency': ['thread', 'concurrent', 'lock', 'atomic', 'virtual'],
        'jfr': ['jfr', 'flight'],
        'build': ['make/', 'configure', 'build'],
        'test': ['test/', 'jtreg'],
    }
    
    by_component = defaultdict(list)
    by_author = defaultdict(list)
    by_month = defaultdict(list)
    
    for commit in commits:
        # 根据文件路径和 subject 分类
        text = f"{commit['subject']} {' '.join(commit['files'])}".lower()
        
        matched = False
        for comp, keywords in component_keywords.items():
            for kw in keywords:
                if kw.lower() in text:
                    by_component[comp].append(commit)
                    matched = True
                    break
            if matched:
                break
        
        if not matched:
            by_component['other'].append(commit)
        
        by_author[commit['author']].append(commit)
        
        if commit['date']:
            month = commit['date'][:7]
            by_month[month].append(commit)
    
    return {
        'by_component': by_component,
        'by_author': by_author,
        'by_month': by_month,
    }

def generate_report(commits, categories):
    """生成报告"""
    total = len(commits)
    
    report = f"""# JDK 26 Commit 分析报告

> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
> 数据来源: git log
> 总 Commit 数: {total}

---

## 统计概览

### 按组件分布

| 组件 | Commit 数 | 占比 |
|------|-----------|------|
"""
    
    for comp, items in sorted(categories['by_component'].items(), 
                              key=lambda x: -len(x[1])):
        pct = len(items) / total * 100 if total > 0 else 0
        report += f"| {comp} | {len(items)} | {pct:.1f}% |\n"
    
    report += """
### 按月份分布

| 月份 | Commit 数 |
|------|-----------|
"""
    
    for month, items in sorted(categories['by_month'].items()):
        report += f"| {month} | {len(items)} |\n"
    
    report += """
### Top 30 贡献者

| 排名 | 作者 | Commit 数 |
|------|------|-----------|
"""
    
    for i, (author, items) in enumerate(
            sorted(categories['by_author'].items(), key=lambda x: -len(x[1]))[:30], 1):
        report += f"| {i} | {author} | {len(items)} |\n"
    
    # 各组件详情
    report += "\n---\n\n## 各组件重要 Commit 列表\n"
    
    component_order = ['gc', 'compiler', 'network', 'security', 'core', 
                       'concurrency', 'jfr', 'build']
    
    for comp in component_order:
        if comp in categories['by_component']:
            items = categories['by_component'][comp]
            report += f"\n### {comp.upper()} ({len(items)} Commits)\n\n"
            
            # 按变更大小排序
            sorted_items = sorted(items, 
                                 key=lambda x: x.get('additions', 0) + x.get('deletions', 0),
                                 reverse=True)
            
            for commit in sorted_items[:50]:
                hash_short = commit['hash'][:12]
                subject = commit['subject'][:70]
                author = commit['author']
                adds = commit.get('additions', 0)
                dels = commit.get('deletions', 0)
                issue = commit.get('issue')
                
                if issue:
                    prefix = str(issue)[:4]
                    report += f"- [JDK-{issue}](./{prefix}/{issue}.md) {subject} (+{adds}/-{dels}) {author}\n"
                else:
                    report += f"- `{hash_short}` {subject} (+{adds}/-{dels}) {author}\n"
            
            if len(items) > 50:
                report += f"\n*... 还有 {len(items) - 50} 个 Commits*\n"
    
    return report

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_jdk26_from_git.py <jdk_repo_path>")
        print("Example: python3 fetch_jdk26_from_git.py /root/git/jdk26-temp")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    print(f"Analyzing JDK repo: {repo_path}")
    
    # 获取 commits
    commits = get_commits_from_git(repo_path)
    
    print(f"Found {len(commits)} commits")
    
    if not commits:
        print("No commits found")
        return
    
    # 分类
    categories = categorize_commits(commits)
    
    # 保存原始数据
    with open('prs/jdk26-commits.json', 'w') as f:
        # 简化数据以便保存
        simplified = []
        for c in commits:
            simplified.append({
                'hash': c['hash'][:12],
                'subject': c['subject'],
                'author': c['author'],
                'date': c['date'],
                'issue': c.get('issue'),
                'additions': c.get('additions', 0),
                'deletions': c.get('deletions', 0),
                'files_count': len(c.get('files', [])),
            })
        json.dump(simplified, f, indent=2)
    print("Data saved to prs/jdk26-commits.json")
    
    # 生成报告
    report = generate_report(commits, categories)
    with open('prs/jdk26-commits.md', 'w') as f:
        f.write(report)
    print("Report saved to prs/jdk26-commits.md")
    
    # 打印统计
    print("\n" + "="*50)
    print("统计:")
    print("="*50)
    for comp, items in sorted(categories['by_component'].items(), 
                              key=lambda x: -len(x[1]))[:10]:
        print(f"  {comp}: {len(items)}")

if __name__ == '__main__':
    main()
