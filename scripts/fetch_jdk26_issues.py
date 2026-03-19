#!/usr/bin/env python3
"""
通过 OpenJDK Bug 系统 (JBS) API 获取 fixVersion 为 jdk26 的 issues

OpenJDK Bug 系统 API:
https://bugs.openjdk.org/rest/api/2/

用法:
    python3 scripts/fetch_jdk26_issues.py
"""

import json
import requests
import time
import sys
from collections import defaultdict

# OpenJDK Bug 系统 API
JBS_BASE_URL = "https://bugs.openjdk.org/rest/api/2"

def search_issues(jql, start_at=0, max_results=100):
    """搜索 JBS issues"""
    url = f"{JBS_BASE_URL}/search"
    params = {
        'jql': jql,
        'startAt': start_at,
        'maxResults': max_results,
        'fields': 'key,summary,status,priority,components,labels,fixVersions,issuetype,resolution,customfield_10000'
    }
    
    try:
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error searching issues: {e}")
        return None

def get_all_jdk26_issues():
    """获取所有 fixVersion 为 jdk26 的 issues"""
    all_issues = []
    start_at = 0
    max_results = 100
    
    # JQL 查询: fixVersion = jdk26
    jql = 'project = JDK AND fixVersion = "jdk26" ORDER BY key'
    
    print("Fetching JDK 26 issues from OpenJDK Bug System...")
    
    while True:
        result = search_issues(jql, start_at, max_results)
        
        if not result or 'issues' not in result:
            break
        
        issues = result['issues']
        all_issues.extend(issues)
        
        total = result.get('total', 0)
        print(f"  Fetched {len(all_issues)}/{total} issues...")
        
        if len(all_issues) >= total:
            break
        
        start_at += max_results
        time.sleep(0.5)  # 避免请求过快
    
    return all_issues

def parse_issue(issue):
    """解析 issue 数据"""
    fields = issue.get('fields', {})
    
    # 提取组件
    components = [c.get('name', '') for c in fields.get('components', [])]
    
    # 提取 fixVersions
    fix_versions = [v.get('name', '') for v in fields.get('fixVersions', [])]
    
    # 提取优先级
    priority = fields.get('priority', {}).get('name', '')
    
    # 提取状态
    status = fields.get('status', {}).get('name', '')
    
    # 提取类型
    issue_type = fields.get('issuetype', {}).get('name', '')
    
    # 提取标签
    labels = fields.get('labels', [])
    
    return {
        'key': issue.get('key', ''),
        'summary': fields.get('summary', ''),
        'status': status,
        'priority': priority,
        'components': components,
        'fixVersions': fix_versions,
        'issueType': issue_type,
        'labels': labels,
    }

def categorize_issues(issues):
    """分类 issues"""
    by_component = defaultdict(list)
    by_priority = defaultdict(list)
    by_type = defaultdict(list)
    by_status = defaultdict(list)
    
    for issue in issues:
        data = parse_issue(issue)
        
        # 按组件分类
        for comp in data['components']:
            by_component[comp].append(data)
        if not data['components']:
            by_component['unknown'].append(data)
        
        # 按优先级分类
        by_priority[data['priority']].append(data)
        
        # 按类型分类
        by_type[data['issueType']].append(data)
        
        # 按状态分类
        by_status[data['status']].append(data)
    
    return {
        'by_component': by_component,
        'by_priority': by_priority,
        'by_type': by_type,
        'by_status': by_status,
    }

def generate_report(issues, categories, output_file='prs/jdk26-issues.md'):
    """生成报告"""
    
    with open(output_file, 'w') as f:
        f.write("# JDK 26 Issues 分析报告\n\n")
        f.write(f"> 数据来源: OpenJDK Bug System (fixVersion = jdk26)\n")
        f.write(f"> 总 Issue 数: {len(issues)}\n\n")
        
        # 统计概览
        f.write("## 统计概览\n\n")
        
        # 按状态分布
        f.write("### 按状态分布\n\n")
        f.write("| 状态 | 数量 |\n")
        f.write("|------|------|\n")
        for status, items in sorted(categories['by_status'].items(), 
                                     key=lambda x: -len(x[1])):
            f.write(f"| {status} | {len(items)} |\n")
        
        # 按优先级分布
        f.write("\n### 按优先级分布\n\n")
        f.write("| 优先级 | 数量 |\n")
        f.write("|--------|------|\n")
        priority_order = ['P1', 'P2', 'P3', 'P4', 'P5']
        for priority in priority_order:
            if priority in categories['by_priority']:
                f.write(f"| {priority} | {len(categories['by_priority'][priority])} |\n")
        
        # 按类型分布
        f.write("\n### 按类型分布\n\n")
        f.write("| 类型 | 数量 |\n")
        f.write("|------|------|\n")
        for issue_type, items in sorted(categories['by_type'].items(),
                                        key=lambda x: -len(x[1])):
            f.write(f"| {issue_type} | {len(items)} |\n")
        
        # 按组件分布
        f.write("\n### 按组件分布\n\n")
        f.write("| 组件 | 数量 |\n")
        f.write("|------|------|\n")
        for comp, items in sorted(categories['by_component'].items(),
                                  key=lambda x: -len(x[1])):
            f.write(f"| {comp} | {len(items)} |\n")
        
        # 重要 Issues (P1, P2)
        f.write("\n## 重要 Issues\n\n")
        
        important_issues = []
        for priority in ['P1', 'P2']:
            important_issues.extend(categories['by_priority'].get(priority, []))
        
        f.write(f"### P1/P2 优先级 ({len(important_issues)} 个)\n\n")
        for issue in sorted(important_issues, key=lambda x: x['key']):
            key = issue['key']
            issue_num = key.replace('JDK-', '')
            prefix = issue_num[:4]
            f.write(f"- [{key}](./{prefix}/{issue_num}.md) - {issue['summary'][:60]}\n")
        
        # 按组件分类的 Issues
        f.write("\n## 按组件分类\n\n")
        
        key_components = ['hotspot-gc', 'hotspot-compiler', 'core-libs', 
                         'net', 'security-libs', 'tools']
        
        for comp in key_components:
            if comp in categories['by_component']:
                items = categories['by_component'][comp]
                f.write(f"\n### {comp} ({len(items)} 个)\n\n")
                for issue in sorted(items, key=lambda x: x['key'])[:30]:
                    key = issue['key']
                    issue_num = key.replace('JDK-', '')
                    prefix = issue_num[:4]
                    f.write(f"- [{key}](./{prefix}/{issue_num}.md) - {issue['summary'][:50]}\n")
                if len(items) > 30:
                    f.write(f"\n  ... 还有 {len(items) - 30} 个\n")
        
        # JEP 相关
        f.write("\n## JEP 相关\n\n")
        jep_issues = [i for i in issues if 'jep' in str(i).lower()]
        # 通过 labels 或 summary 识别 JEP
        for issue in issues:
            data = parse_issue(issue)
            if 'jep' in str(data['labels']).lower() or 'jep' in data['summary'].lower():
                key = data['key']
                f.write(f"- [{key}](https://bugs.openjdk.org/browse/{key}) - {data['summary'][:60]}\n")
    
    print(f"报告已生成: {output_file}")

def main():
    # 获取所有 JDK 26 issues
    issues = get_all_jdk26_issues()
    
    if not issues:
        print("未获取到任何 issues")
        return
    
    print(f"\n总共获取 {len(issues)} 个 JDK 26 issues")
    
    # 分类
    categories = categorize_issues(issues)
    
    # 保存原始数据
    with open('prs/jdk26-issues.json', 'w') as f:
        json.dump([parse_issue(i) for i in issues], f, indent=2)
    print("原始数据已保存到: prs/jdk26-issues.json")
    
    # 生成报告
    generate_report(issues, categories)
    
    # 打印简要统计
    print("\n" + "="*50)
    print("简要统计:")
    print("="*50)
    print(f"总 Issue 数: {len(issues)}")
    print(f"\n按优先级:")
    for p in ['P1', 'P2', 'P3', 'P4']:
        count = len(categories['by_priority'].get(p, []))
        if count > 0:
            print(f"  {p}: {count}")
    print(f"\n按类型:")
    for t, items in sorted(categories['by_type'].items(), key=lambda x: -len(x[1]))[:5]:
        print(f"  {t}: {len(items)}")

if __name__ == '__main__':
    main()
