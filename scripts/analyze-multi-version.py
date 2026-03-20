#!/usr/bin/env python3
"""
多版本 JDK commit 分析脚本
支持 JDK 21, 17, 11, 8 等版本的 git commit 分析
"""

import subprocess
import re
import json
import sys
import os
from collections import defaultdict
from datetime import datetime

# 版本配置
VERSION_CONFIGS = {
    'jdk8': {
        'since': '2014-01-01',
        'until': '2019-01-01',
        'description': 'JDK 8 (LTS 2014)',
        'git_branch': 'jdk8u-dev',
    },
    'jdk11': {
        'since': '2018-01-01',
        'until': '2023-01-01',
        'description': 'JDK 11 (LTS 2018)',
        'git_branch': 'jdk11u-dev',
    },
    'jdk17': {
        'since': '2021-01-01',
        'until': '2024-01-01',
        'description': 'JDK 17 (LTS 2021)',
        'git_branch': 'jdk17u-dev',
    },
    'jdk21': {
        'since': '2023-01-01',
        'until': '2026-01-01',
        'description': 'JDK 21 (LTS 2023)',
        'git_branch': 'jdk21u-dev',
    },
    'jdk25': {
        'since': '2025-01-01',
        'until': '2026-04-01',
        'description': 'JDK 25 (GA 2025-03)',
        'git_branch': 'jdk25',
    },
    'jdk26': {
        'since': '2025-06-01',
        'until': '2026-04-01',
        'description': 'JDK 26 (GA 2025-09)',
        'git_branch': 'jdk26',
    },
}

def get_commits_from_git(repo_path, version_config):
    """从 git 仓库获取指定版本的 commits"""
    since = version_config['since']
    until = version_config['until']
    branch = version_config.get('git_branch', 'master')
    
    cmd = [
        'git', 'log',
        f'--since={since}',
        f'--until={until}',
        '--pretty=format:%H%n%s%n%an%n%ae%n%ai%n%n',
        '--numstat',
        branch
    ]

    print(f"Running: git log --since={since} --until={until} {branch}")
    result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        # 尝试不带分支名
        cmd = cmd[:-1]
        result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error without branch: {result.stderr}")
            return []

    return parse_git_log(result.stdout)

def parse_git_log(output):
    """解析 git log 输出 (与单版本脚本相同)"""
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
    """分类 commits (与单版本脚本相同)"""
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

def generate_version_report(version, commits, categories, config):
    """生成单个版本的报告"""
    total = len(commits)
    description = config['description']

    report = f"""# {description} Commit 分析报告

> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
> 数据来源: git log ({config['since']} 至 {config['until']})
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

def generate_comparison_report(all_results):
    """生成版本对比报告"""
    report = """# JDK 多版本对比分析报告

> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
> 数据来源: git log

---

## 版本概览

| 版本 | 描述 | 时间范围 | Commit 数 | 主要组件 | Top 贡献者 |
|------|------|----------|-----------|----------|------------|
""".format(datetime=datetime)

    for version, data in all_results.items():
        config = VERSION_CONFIGS[version]
        commits = data['commits']
        categories = data['categories']
        
        total = len(commits)
        
        # 获取主要组件
        top_components = sorted(categories['by_component'].items(),
                                key=lambda x: -len(x[1]))[:3]
        components_str = ', '.join([f"{c}({len(v)})" for c, v in top_components])
        
        # 获取 top 贡献者
        top_authors = sorted(categories['by_author'].items(),
                             key=lambda x: -len(x[1]))[:3]
        authors_str = ', '.join([f"{a}({len(v)})" for a, v in top_authors])
        
        report += f"| {version} | {config['description']} | {config['since']}~{config['until']} | {total} | {components_str} | {authors_str} |\n"

    report += """
---

## 组件趋势对比

| 组件 | JDK 8 | JDK 11 | JDK 17 | JDK 21 | JDK 25 | JDK 26 |
|------|-------|--------|--------|--------|--------|--------|
"""

    # 所有可能的组件
    all_components = set()
    for data in all_results.values():
        all_components.update(data['categories']['by_component'].keys())
    
    component_order = ['gc', 'compiler', 'network', 'security', 'core',
                       'concurrency', 'jfr', 'build', 'test', 'other']
    
    for comp in component_order:
        if comp not in all_components:
            continue
            
        row = f"| {comp} "
        for version in ['jdk8', 'jdk11', 'jdk17', 'jdk21', 'jdk25', 'jdk26']:
            if version in all_results:
                count = len(all_results[version]['categories']['by_component'].get(comp, []))
                total = len(all_results[version]['commits'])
                pct = count / total * 100 if total > 0 else 0
                row += f"| {count} ({pct:.1f}%) "
            else:
                row += "| - "
        row += "|\n"
        report += row

    report += """
---

## 贡献者活跃度趋势

| 贡献者 | JDK 8 | JDK 11 | JDK 17 | JDK 21 | JDK 25 | JDK 26 | 总计 |
|--------|-------|--------|--------|--------|--------|--------|------|
"""

    # 收集所有贡献者
    all_authors = defaultdict(lambda: defaultdict(int))
    for version, data in all_results.items():
        for author, commits in data['categories']['by_author'].items():
            all_authors[author][version] = len(commits)
    
    # 按总 commits 排序
    sorted_authors = sorted(all_authors.items(),
                           key=lambda x: sum(x[1].values()),
                           reverse=True)[:50]
    
    for author, versions in sorted_authors:
        total = sum(versions.values())
        if total < 5:  # 只显示有显著贡献的
            continue
            
        row = f"| {author} "
        for version in ['jdk8', 'jdk11', 'jdk17', 'jdk21', 'jdk25', 'jdk26']:
            count = versions.get(version, 0)
            row += f"| {count} " if count > 0 else "| - "
        row += f"| {total} |\n"
        report += row

    return report

def save_version_data(version, commits, categories):
    """保存版本数据到文件"""
    # 确保目录存在
    os.makedirs('prs', exist_ok=True)
    
    # 保存原始数据 (简化)
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
    
    with open(f'prs/{version}-commits.json', 'w') as f:
        json.dump(simplified, f, indent=2)
    
    print(f"Data saved to prs/{version}-commits.json")
    
    # 保存分类数据
    with open(f'prs/{version}-categories.json', 'w') as f:
        # 简化分类数据以便保存
        simplified_cats = {
            'by_component': {
                comp: [c['hash'][:12] for c in commits]
                for comp, commits in categories['by_component'].items()
            },
            'by_author': {
                author: [c['hash'][:12] for c in commits]
                for author, commits in categories['by_author'].items()
            },
            'by_month': {
                month: [c['hash'][:12] for c in commits]
                for month, commits in categories['by_month'].items()
            }
        }
        json.dump(simplified_cats, f, indent=2)
    
    print(f"Categories saved to prs/{version}-categories.json")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze-multi-version.py <jdk_repo_path> [versions]")
        print("Example: python3 analyze-multi-version.py /root/git/jdk26-temp jdk21 jdk17 jdk11")
        print("Available versions:", ', '.join(VERSION_CONFIGS.keys()))
        sys.exit(1)

    repo_path = sys.argv[1]
    
    # 确定要分析的版本
    if len(sys.argv) > 2:
        versions = sys.argv[2:]
        # 验证版本
        invalid = [v for v in versions if v not in VERSION_CONFIGS]
        if invalid:
            print(f"Error: Invalid versions: {', '.join(invalid)}")
            print(f"Available: {', '.join(VERSION_CONFIGS.keys())}")
            sys.exit(1)
    else:
        # 默认分析所有版本
        versions = list(VERSION_CONFIGS.keys())
    
    print(f"Analyzing JDK repo: {repo_path}")
    print(f"Versions to analyze: {', '.join(versions)}")
    
    all_results = {}
    
    for version in versions:
        config = VERSION_CONFIGS[version]
        print(f"\n{'='*60}")
        print(f"Analyzing {version} ({config['description']})...")
        print(f"Time range: {config['since']} to {config['until']}")
        
        # 获取 commits
        commits = get_commits_from_git(repo_path, config)
        print(f"Found {len(commits)} commits")
        
        if not commits:
            print(f"No commits found for {version}, skipping...")
            continue
        
        # 分类
        categories = categorize_commits(commits)
        
        # 保存数据
        save_version_data(version, commits, categories)
        
        # 生成版本报告
        report = generate_version_report(version, commits, categories, config)
        with open(f'prs/{version}-commits.md', 'w') as f:
            f.write(report)
        print(f"Report saved to prs/{version}-commits.md")
        
        # 存储结果用于对比
        all_results[version] = {
            'commits': commits,
            'categories': categories,
            'config': config
        }
        
        # 打印简要统计
        print(f"\n{version} Statistics:")
        print("-" * 40)
        for comp, items in sorted(categories['by_component'].items(),
                                  key=lambda x: -len(x[1]))[:5]:
            print(f"  {comp}: {len(items)} commits")
    
    # 生成对比报告
    if len(all_results) > 1:
        print(f"\n{'='*60}")
        print("Generating comparison report...")
        
        comparison_report = generate_comparison_report(all_results)
        with open('prs/jdk-versions-comparison.md', 'w') as f:
            f.write(comparison_report)
        print("Comparison report saved to prs/jdk-versions-comparison.md")
    
    print(f"\n{'='*60}")
    print("Multi-version analysis completed!")
    print(f"Analyzed {len(all_results)} versions:")
    for version in all_results.keys():
        print(f"  - {version}: {len(all_results[version]['commits'])} commits")

if __name__ == '__main__':
    main()