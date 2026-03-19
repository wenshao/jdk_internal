#!/usr/bin/env python3
"""
Organization Contribution Analyzer

Analyzes OpenJDK contributions by organization based on:
- Git commit authors
- Modified files/directories
- Commit message keywords
"""

import subprocess
import sys
import re
from collections import defaultdict
from pathlib import Path

JDK_REPO = "/root/git/jdk"
BRANCH = "upstream_master"

# Organization email patterns
ORG_PATTERNS = {
    'oracle': ['@openjdk.org', '@oracle.com'],
    'redhat': ['@redhat.com', 'redhat'],
    'sap': ['@sap.com'],
    'amazon': ['@amazon.com', '@amazon.de'],
    'google': ['@google.com'],
    'ibm': ['@ibm.com', '@ca.ibm.com'],
    'alibaba': ['@alibaba-inc.com', 'alibaba'],
    'tencent': ['@tencent.com'],
    'loongson': ['@loongson.cn'],
    'bytedance': ['@bytedance.com'],
    'hygon': ['@hygon.cn'],
    'iscas': ['@iscas.ac.cn'],
    'huawei': ['@huawei.com'],
}

# Directory to module mapping
DIR_MODULE_MAP = {
    'src/hotspot/share/gc': 'GC',
    'src/hotspot/share/opto': 'C2 Compiler',
    'src/hotspot/share/runtime': 'HotSpot Runtime',
    'src/hotspot/share/classfile': 'Class File',
    'src/hotspot/share/prims': 'JVM Primitives',
    'src/hotspot/share/oops': 'OOPs',
    'src/hotspot/cpu': 'CPU Port',
    'src/hotspot/share/compiler': 'Compiler',
    'src/java.base/share/classes': 'Core Libraries',
    'src/java.base/share/classes/java/lang': 'java.lang',
    'src/java.base/share/classes/java/util': 'java.util',
    'test/': 'Tests',
    'make/': 'Build System',
    'nashorn/': 'Nashorn',
}

def run_git(cmd):
    """Run git command and return output"""
    full_cmd = f"cd {JDK_REPO} && {cmd}"
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def get_org_commits(org_name):
    """Get commits for an organization"""
    patterns = ORG_PATTERNS.get(org_name, [])
    if not patterns:
        return []
    
    # Build author filter
    author_filter = '|'.join(patterns)
    
    cmd = f'git log {BRANCH} --author="{author_filter}" --format="%H|%ae|%s"'
    output = run_git(cmd)
    
    commits = []
    for line in output.strip().split('\n'):
        if '|' in line:
            parts = line.split('|', 2)
            if len(parts) == 3:
                commits.append({
                    'hash': parts[0],
                    'author': parts[1],
                    'subject': parts[2]
                })
    return commits

def get_org_directories(org_name):
    """Get affected directories for an organization"""
    patterns = ORG_PATTERNS.get(org_name, [])
    if not patterns:
        return {}
    
    author_filter = '|'.join(patterns)
    cmd = f'git log {BRANCH} --author="{author_filter}" --format="" --name-only'
    output = run_git(cmd)
    
    dirs = defaultdict(int)
    for line in output.strip().split('\n'):
        if line.strip():
            # Get directory
            dir_path = str(Path(line).parent)
            dirs[dir_path] += 1
    
    return dict(sorted(dirs.items(), key=lambda x: -x[1]))

def get_org_keywords(org_name):
    """Get commit message keywords for an organization"""
    patterns = ORG_PATTERNS.get(org_name, [])
    if not patterns:
        return {}
    
    author_filter = '|'.join(patterns)
    cmd = f'git log {BRANCH} --author="{author_filter}" --format="%s"'
    output = run_git(cmd)
    
    keywords = defaultdict(int)
    keyword_patterns = [
        r'(?i)\bfix\b',
        r'(?i)\badd\b',
        r'(?i)\bremove\b',
        r'(?i)\bupdate\b',
        r'(?i)\bimplement\b',
        r'(?i)\brefactor\b',
        r'(?i)\boptimize\b',
        r'(?i)\bclean\b',
        r'(?i)\bmerge\b',
        r'JDK-\d+',
        r'(?i)\bshenandoah\b',
        r'(?i)\bg1\b',
        r'(?i)\bzgc\b',
        r'(?i)\baarch64\b',
        r'(?i)\bppc\b',
        r'(?i)\briscv\b',
        r'(?i)\bloongarch\b',
        r'(?i)\baix\b',
    ]
    
    for line in output.strip().split('\n'):
        for pattern in keyword_patterns:
            matches = re.findall(pattern, line)
            for match in matches:
                keywords[match] += 1
    
    return dict(sorted(keywords.items(), key=lambda x: -x[1]))

def analyze_module_distribution(dirs):
    """Analyze module distribution from directories"""
    modules = defaultdict(int)
    
    for dir_path, count in dirs.items():
        matched = False
        for pattern, module in DIR_MODULE_MAP.items():
            if pattern in dir_path:
                modules[module] += count
                matched = True
                break
        if not matched:
            modules['Other'] += count
    
    return dict(sorted(modules.items(), key=lambda x: -x[1]))

def analyze_org(org_name):
    """Analyze an organization's contributions"""
    print(f"\n{'='*60}")
    print(f"Organization: {org_name.upper()}")
    print(f"{'='*60}")
    
    commits = get_org_commits(org_name)
    print(f"\nTotal Commits: {len(commits)}")
    
    # Top authors
    authors = defaultdict(int)
    for c in commits:
        authors[c['author']] += 1
    
    print(f"\nTop Authors:")
    for author, count in sorted(authors.items(), key=lambda x: -x[1])[:10]:
        print(f"  {count:5} {author}")
    
    # Affected directories
    dirs = get_org_directories(org_name)
    print(f"\nTop Directories:")
    for dir_path, count in list(dirs.items())[:15]:
        print(f"  {count:5} {dir_path}")
    
    # Module distribution
    modules = analyze_module_distribution(dirs)
    print(f"\nModule Distribution:")
    for module, count in list(modules.items())[:10]:
        print(f"  {count:5} {module}")
    
    # Keywords
    keywords = get_org_keywords(org_name)
    print(f"\nCommit Keywords:")
    for keyword, count in list(keywords.items())[:15]:
        print(f"  {count:5} {keyword}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Analyze OpenJDK contributions by organization')
    parser.add_argument('org', nargs='?', help='Organization to analyze')
    parser.add_argument('--all', action='store_true', help='Analyze all organizations')
    
    args = parser.parse_args()
    
    if args.all:
        for org in ORG_PATTERNS.keys():
            analyze_org(org)
    elif args.org:
        analyze_org(args.org.lower())
    else:
        print("Usage: python3 org_analyzer.py <org_name>")
        print("       python3 org_analyzer.py --all")
        print(f"\nAvailable organizations: {', '.join(ORG_PATTERNS.keys())}")

if __name__ == '__main__':
    main()