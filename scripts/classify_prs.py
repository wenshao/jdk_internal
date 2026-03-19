#!/usr/bin/env python3
"""
JDK PR 分类和分析工具

用法:
    python3 scripts/classify_prs.py prs/jdk26-prs.json
"""

import json
import sys
import re
from collections import defaultdict
from datetime import datetime

# 组件关键词映射
COMPONENT_KEYWORDS = {
    'gc': [
        'G1', 'ZGC', 'Shenandoah', 'ParallelGC', 'SerialGC', 
        'garbage', 'GC', 'heap', 'memory', 'collector',
        'marking', 'evacuation', 'relocation', 'region'
    ],
    'compiler': [
        'C2', 'C1', 'JIT', 'compiler', 'intrinsic', 'optimize',
        'SuperWord', 'vectorization', 'loop', 'CodeCache',
        'deoptimization', 'inline', 'Graal', 'aot'
    ],
    'network': [
        'HttpClient', 'HTTP/2', 'HTTP/3', 'QUIC', 'WebSocket',
        'Socket', 'TCP', 'UDP', 'TLS', 'SSL', 'net', 'network',
        'connection', 'request', 'response'
    ],
    'security': [
        'crypto', 'cipher', 'signature', 'key', 'certificate',
        'ML-DSA', 'ML-KEM', 'RSA', 'AES', 'SHA', 'digest',
        'security', 'encrypt', 'decrypt', 'JAR signing'
    ],
    'core': [
        'java.lang', 'java.util', 'reflect', 'String', 'Object',
        'Class', 'Thread', 'ClassLoader', 'method', 'field',
        'annotation', 'generic', 'lambda', 'Optional', 'Stream'
    ],
    'concurrency': [
        'Thread', 'VirtualThread', 'lock', 'concurrent', 'atomic',
        'synchron', 'volatile', 'mutex', 'semaphore', 'Future',
        'CompletableFuture', 'Executor', 'ForkJoin'
    ],
    'jfr': [
        'JFR', 'Flight Recorder', 'event', 'monitoring',
        'profiling', 'tracing', 'recording', 'streaming'
    ],
    'startup': [
        'CDS', 'AOT', 'class loading', 'bootstrap', 'startup',
        'Class Data Sharing', 'AppCDS', 'dynamic archive'
    ],
    'build': [
        'build', 'make', 'configure', 'autoconf', 'cmake',
        'toolchain', 'cross-compile', 'install', 'package'
    ],
    'test': [
        'test', 'jtreg', 'gtest', 'regression', 'unit test',
        'integration test', 'testng'
    ],
}

# 重要性关键词
IMPORTANCE_KEYWORDS = {
    'critical': [
        'crash', 'security', 'vulnerability', 'CVE', 'exploit',
        'data loss', 'corruption', 'hang', 'deadlock'
    ],
    'high': [
        'performance', 'optimize', 'regression', 'slow', 'leak',
        'memory leak', 'OOM', 'timeout', 'scalability'
    ],
    'medium': [
        'bug', 'fix', 'incorrect', 'wrong', 'error', 'fail',
        'improve', 'enhance', 'feature'
    ],
}

def classify_component(title, labels=None):
    """根据标题和标签分类组件"""
    text = title.lower()
    if labels:
        text += ' ' + ' '.join(l.get('name', '') for l in labels).lower()
    
    scores = {}
    for component, keywords in COMPONENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in text)
        if score > 0:
            scores[component] = score
    
    if scores:
        return max(scores, key=scores.get)
    return 'other'

def classify_importance(title, comments=0, additions=0):
    """评估 PR 重要性"""
    text = title.lower()
    
    for level, keywords in IMPORTANCE_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return level
    
    # 基于其他因素判断
    if comments > 10 or additions > 1000:
        return 'high'
    elif comments > 5 or additions > 500:
        return 'medium'
    
    return 'low'

def extract_issue_number(title):
    """从标题提取 JDK Issue 号"""
    match = re.search(r'JDK-(\d+)', title)
    if match:
        return int(match.group(1))
    
    match = re.search(r'(\d{7,})', title)
    if match:
        return int(match.group(1))
    
    return None

def analyze_prs(json_file):
    """分析 PR 数据"""
    with open(json_file, 'r') as f:
        prs = json.load(f)
    
    print(f"分析 {len(prs)} 个 PR...\n")
    
    # 统计
    by_component = defaultdict(list)
    by_importance = defaultdict(list)
    by_author = defaultdict(list)
    issues = []
    
    for pr in prs:
        # 提取信息
        title = pr.get('title', '')
        author = pr.get('author', {}).get('login', 'unknown')
        labels = pr.get('labels', [])
        comments = pr.get('comments', 0)
        additions = pr.get('additions', 0)
        deletions = pr.get('deletions', 0)
        
        # 分类
        component = classify_component(title, labels)
        importance = classify_importance(title, comments, additions)
        issue = extract_issue_number(title)
        
        # 记录
        by_component[component].append(pr)
        by_importance[importance].append(pr)
        by_author[author].append(pr)
        
        if issue:
            issues.append({
                'issue': issue,
                'title': title,
                'author': author,
                'component': component,
                'importance': importance,
            })
    
    # 打印报告
    print("=" * 60)
    print("JDK 26 PR 分析报告")
    print("=" * 60)
    
    print(f"\n总 PR 数: {len(prs)}")
    
    print("\n" + "-" * 40)
    print("按组件分布:")
    print("-" * 40)
    for component, pr_list in sorted(by_component.items(), key=lambda x: -len(x[1])):
        pct = len(pr_list) / len(prs) * 100
        print(f"  {component:15} {len(pr_list):5} ({pct:5.1f}%)")
    
    print("\n" + "-" * 40)
    print("按重要性分布:")
    print("-" * 40)
    for importance, pr_list in sorted(by_importance.items(), key=lambda x: -len(x[1])):
        pct = len(pr_list) / len(prs) * 100
        print(f"  {importance:15} {len(pr_list):5} ({pct:5.1f}%)")
    
    print("\n" + "-" * 40)
    print("Top 20 贡献者:")
    print("-" * 40)
    sorted_authors = sorted(by_author.items(), key=lambda x: -len(x[1]))[:20]
    for i, (author, pr_list) in enumerate(sorted_authors, 1):
        print(f"  {i:2}. {author:25} {len(pr_list):4} PRs")
    
    # 输出重要 PR 列表
    print("\n" + "-" * 40)
    print("重要 PR (critical + high):")
    print("-" * 40)
    important_prs = by_importance['critical'] + by_importance['high']
    for pr in sorted(important_prs, key=lambda x: x.get('comments', 0), reverse=True)[:30]:
        print(f"  #{pr['number']:6} {pr['title'][:60]}")
    
    return {
        'total': len(prs),
        'by_component': {k: len(v) for k, v in by_component.items()},
        'by_importance': {k: len(v) for k, v in by_importance.items()},
        'by_author': {k: len(v) for k, v in by_author.items()},
        'issues': issues,
    }

def generate_todo_list(analysis_result, output_file='prs/jdk26-analysis.md'):
    """生成待分析 PR 列表"""
    
    issues = analysis_result['issues']
    
    # 按重要性和组件排序
    important_issues = [
        i for i in issues 
        if i['importance'] in ['critical', 'high']
    ]
    
    # 按组件分组
    by_component = defaultdict(list)
    for issue in important_issues:
        by_component[issue['component']].append(issue)
    
    with open(output_file, 'w') as f:
        f.write("# JDK 26 PR 分析报告\n\n")
        f.write(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"> 总 PR 数: {analysis_result['total']}\n\n")
        
        f.write("## 统计概览\n\n")
        f.write("### 按组件分布\n\n")
        f.write("| 组件 | PR 数 | 占比 |\n")
        f.write("|------|-------|------|\n")
        for comp, count in sorted(analysis_result['by_component'].items(), 
                                  key=lambda x: -x[1]):
            pct = count / analysis_result['total'] * 100
            f.write(f"| {comp} | {count} | {pct:.1f}% |\n")
        
        f.write("\n### 按重要性分布\n\n")
        f.write("| 重要性 | PR 数 | 占比 |\n")
        f.write("|--------|-------|------|\n")
        for imp, count in sorted(analysis_result['by_importance'].items(),
                                 key=lambda x: -x[1]):
            pct = count / analysis_result['total'] * 100
            f.write(f"| {imp} | {count} | {pct:.1f}% |\n")
        
        f.write("\n## 重要 PR 列表\n\n")
        
        for component in ['gc', 'compiler', 'network', 'security', 'concurrency', 'core']:
            if component in by_component:
                f.write(f"\n### {component.upper()}\n\n")
                for issue in by_component[component][:20]:
                    issue_dir = str(issue['issue'])[:4]
                    f.write(f"- [ ] [{issue['issue']}](./{issue_dir}/{issue['issue']}.md) - {issue['title'][:50]} (@{issue['author']})\n")
        
        f.write("\n## Top 贡献者\n\n")
        sorted_authors = sorted(analysis_result['by_author'].items(), 
                                key=lambda x: -x[1])[:20]
        f.write("| 排名 | 贡献者 | PR 数 |\n")
        f.write("|------|--------|-------|\n")
        for i, (author, count) in enumerate(sorted_authors, 1):
            f.write(f"| {i} | @{author} | {count} |\n")
    
    print(f"\n报告已生成: {output_file}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 scripts/classify_prs.py <json_file>")
        sys.exit(1)
    
    result = analyze_prs(sys.argv[1])
    
    if len(sys.argv) > 2:
        generate_todo_list(result, sys.argv[2])
    else:
        generate_todo_list(result)
