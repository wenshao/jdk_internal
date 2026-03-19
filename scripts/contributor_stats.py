#!/usr/bin/env python3
"""
OpenJDK Contributor Statistics Generator

Usage:
    python3 contributor_stats.py --top 50
    python3 contributor_stats.py --chinese
    python3 contributor_stats.py --by-year
    python3 contributor_stats.py --by-domain
"""

import subprocess
import sys
import json
import re
from collections import defaultdict
from datetime import datetime

# JDK git 仓库路径
JDK_REPO = "/root/git/jdk"
BRANCH = "upstream_master"

# 同一人邮箱映射 (邮箱关键词 -> 标准名)
NAME_MAPPING = {
    # Bot accounts (排除)
    'duke@openjdk': ('J. Duke', True),  # (name, is_bot)
    'lana@openjdk': ('Lana Steuck', True),
    
    # Oracle
    'katleman@openjdk': ('David Katleman', False),
    'jjg@openjdk': ('Jonathan Gibbons', False),
    'prr@openjdk': ('Phil Race', False),
    'race@oracle': ('Phil Race', False),
    'coleenp@openjdk': ('Coleen Phillimore', False),
    'phillimore@oracle': ('Coleen Phillimore', False),
    'darcy@openjdk': ('Joe Darcy', False),
    'tschatzl@openjdk': ('Thomas Schatzl', False),
    'schatzl@oracle': ('Thomas Schatzl', False),
    'amurillo@openjdk': ('Alejandro Murillo', False),
    'serb@openjdk': ('Sergey Bylokhov', False),
    'weijun.wang@oracle': ('Weijun Wang', False),
    'weijun@openjdk': ('Weijun Wang', False),
    'kvn@openjdk': ('Vladimir Kozlov', False),
    'erikj@openjdk': ('Erik Joelsson', False),
    'ihse@openjdk': ('Magnus Ihse Bursie', False),
    'jwilhelm@openjdk': ('Jesper Wilhelmsson', False),
    'dcubed@openjdk': ('Daniel D. Daugherty', False),
    'alanb@openjdk': ('Alan Bateman', False),
    'bateman@oracle': ('Alan Bateman', False),
    'chegar@openjdk': ('Chris Hegarty', False),
    'jlahoda@openjdk': ('Jan Lahoda', False),
    'lahoda@oracle': ('Jan Lahoda', False),
    'psadhukhan@openjdk': ('Prasanta Sadhukhan', False),
    'prasanta@oracle': ('Prasanta Sadhukhan', False),
    'bpb@openjdk': ('Brian Burkhalter', False),
    'burkhalter@oracle': ('Brian Burkhalter', False),
    'ayang@openjdk': ('Albert Mingkun Yang', False),
    'mbaesken@openjdk': ('Matthias Baesken', False),
    'baesken@sap': ('Matthias Baesken', False),
    'dholmes@openjdk': ('David Holmes', False),
    'holmes@oracle': ('David Holmes', False),
    'stefank@openjdk': ('Stefan Karlsson', False),
    'sundar@openjdk': ('Sundararajan Athijegannathan', False),
    'redestad@openjdk': ('Claes Redestad', False),
    'mchung@openjdk': ('Mandy Chung', False),
    'roland@openjdk': ('Roland Westrelin', False),
    'rwestrel@redhat': ('Roland Westrelin', False),
    'kbarrett@openjdk': ('Kim Barrett', False),
    'barrett@oracle': ('Kim Barrett', False),
    'iignatyev@openjdk': ('Igor Ignatyev', False),
    'mcimadamore@openjdk': ('Maurizio Cimadamore', False),
    'iklam@openjdk': ('Ioi Lam', False),
    'zgu@openjdk': ('Zhengyu Gu', False),
    'naoto@openjdk': ('Naoto Sato', False),
    'hannesw@openjdk': ('Hannes Wallnöfer', False),
    'thartmann@openjdk': ('Tobias Hartmann', False),
    'stuefe@openjdk': ('Thomas Stuefe', False),
    'ohair@openjdk': ("Kelly O'Hair", False),
    'dfuchs@openjdk': ('Daniel Fuchs', False),
    'egahlin@openjdk': ('Erik Gahlin', False),
    'gahlin@oracle': ('Erik Gahlin', False),
    'vromero@openjdk': ('Vicente Romero', False),
    'never@openjdk': ('Tom Rodriguez', False),
    'rriggs@openjdk': ('Roger Riggs', False),
    'cjplummer@openjdk': ('Chris Plummer', False),
    'vlivanov@openjdk': ('Vladimir Ivanov', False),
    'hseigel@openjdk': ('Harold Seigel', False),
    'epeter@openjdk': ('Emanuel Peter', False),
    'peter@oracle': ('Emanuel Peter', False),
    'liach@openjdk': ('Chen Liang', False),
    'chen.liang@oracle': ('Chen Liang', False),
    'syan@openjdk': ('SendaoYan', False),
    'yansendao': ('SendaoYan', False),
    
    # Red Hat
    'shade@openjdk': ('Aleksey Shipilev', False),
    'shipilev': ('Aleksey Shipilev', False),
    'aph@openjdk': ('Andrew Haley', False),
    'adinn@redhat': ('Andrew Dinn', False),
    
    # Amazon
    'kemper@openjdk': ('William Kemper', False),
    'kemperw@amazon': ('William Kemper', False),
    'xlpeng@amazon': ('Xiaolong Peng', False),
    'kdnilsen@amazon': ('Kelvin Nilsen', False),
    
    # 中国企业
    'alibaba-inc': None,  # 需要进一步处理
    'tencent': None,
    'loongson': None,
    'bytedance': None,
    'hygon': None,
    'iscas': None,
    'rivos': None,
}

# 中国企业邮箱域名
CHINESE_DOMAINS = ['alibaba-inc', 'tencent', 'loongson', 'bytedance', 
                   'hygon', 'iscas', 'rivosinc', 'huawei', 'linux.alibaba']

def run_git_command(cmd):
    """运行 git 命令并返回输出"""
    full_cmd = f"cd {JDK_REPO} && {cmd}"
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def get_shortlog(since=None, until=None):
    """获取贡献者统计"""
    cmd = f"git shortlog -sne {BRANCH}"
    if since:
        cmd += f" --since='{since}'"
    if until:
        cmd += f" --until='{until}'"
    return run_git_command(cmd)

def parse_shortlog(output):
    """解析 shortlog 输出"""
    contributors = defaultdict(lambda: {'commits': 0, 'emails': [], 'is_bot': False})
    
    for line in output.strip().split('\n'):
        if not line.strip():
            continue
        
        parts = line.strip().split(None, 1)
        if len(parts) != 2:
            continue
            
        commits = int(parts[0])
        email_part = parts[1]
        
        # 提取邮箱
        if '<' in email_part:
            email = email_part.split('<')[1].split('>')[0].lower()
            name = email_part.split('<')[0].strip()
        else:
            email = email_part.lower()
            name = email_part
        
        # 查找标准名
        standard_name = None
        is_bot = False
        
        for key, value in NAME_MAPPING.items():
            if key in email:
                if value is None:
                    break
                standard_name, is_bot = value
                break
        
        if standard_name:
            contributors[standard_name]['commits'] += commits
            contributors[standard_name]['emails'].append(email)
            contributors[standard_name]['is_bot'] = is_bot
        else:
            contributors[name]['commits'] += commits
            contributors[name]['emails'].append(email)
            contributors[name]['is_bot'] = False
    
    return contributors

def get_yearly_stats():
    """获取年度统计"""
    cmd = f"git log {BRANCH} --format='%ad' --date=format:'%Y'"
    output = run_git_command(cmd)
    
    years = defaultdict(int)
    for line in output.strip().split('\n'):
        if line.strip():
            years[line.strip()] += 1
    
    return dict(sorted(years.items()))

def get_chinese_contributors(output):
    """获取中国贡献者"""
    chinese = []
    
    for line in output.strip().split('\n'):
        if not line.strip():
            continue
        
        parts = line.strip().split(None, 1)
        if len(parts) != 2:
            continue
            
        commits = int(parts[0])
        email_part = parts[1]
        
        # 检查是否是中国企业邮箱
        for domain in CHINESE_DOMAINS:
            if domain in email_part.lower():
                chinese.append({
                    'commits': commits,
                    'raw': email_part
                })
                break
    
    return sorted(chinese, key=lambda x: -x['commits'])

def get_domain_stats(output):
    """获取按邮箱域名的统计"""
    domains = defaultdict(lambda: {'commits': 0, 'contributors': 0})
    
    for line in output.strip().split('\n'):
        if not line.strip():
            continue
        
        parts = line.strip().split(None, 1)
        if len(parts) != 2:
            continue
            
        commits = int(parts[0])
        email_part = parts[1]
        
        if '<' in email_part:
            email = email_part.split('<')[1].split('>')[0].lower()
            domain = email.split('@')[-1] if '@' in email else 'unknown'
            
            domains[domain]['commits'] += commits
            domains[domain]['contributors'] += 1
    
    return dict(sorted(domains.items(), key=lambda x: -x[1]['commits']))

def main():
    import argparse
    parser = argparse.ArgumentParser(description='OpenJDK Contributor Statistics')
    parser.add_argument('--top', type=int, default=50, help='Top N contributors')
    parser.add_argument('--chinese', action='store_true', help='Show Chinese contributors')
    parser.add_argument('--by-year', action='store_true', help='Show yearly statistics')
    parser.add_argument('--by-domain', action='store_true', help='Show domain statistics')
    parser.add_argument('--since', type=str, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--until', type=str, help='End date (YYYY-MM-DD)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    output = get_shortlog(args.since, args.until)
    
    if args.by_year:
        years = get_yearly_stats()
        if args.json:
            print(json.dumps(years, indent=2))
        else:
            print("=== Commits by Year ===")
            for year, count in years.items():
                print(f"{year}: {count}")
    
    elif args.chinese:
        chinese = get_chinese_contributors(output)
        if args.json:
            print(json.dumps(chinese, indent=2))
        else:
            print("=== Chinese Contributors ===")
            for c in chinese[:30]:
                print(f"{c['commits']:5} {c['raw']}")
    
    elif args.by_domain:
        domains = get_domain_stats(output)
        if args.json:
            print(json.dumps(domains, indent=2))
        else:
            print("=== Commits by Domain ===")
            for domain, stats in list(domains.items())[:30]:
                print(f"{domain:30} {stats['commits']:5} commits, {stats['contributors']:3} contributors")
    
    else:
        contributors = parse_shortlog(output)
        
        # 排除 bot，排序
        human_contributors = {k: v for k, v in contributors.items() if not v['is_bot']}
        sorted_contributors = sorted(human_contributors.items(), key=lambda x: -x[1]['commits'])
        
        if args.json:
            result = []
            for name, data in sorted_contributors[:args.top]:
                result.append({
                    'name': name,
                    'commits': data['commits'],
                    'emails': data['emails']
                })
            print(json.dumps(result, indent=2))
        else:
            print(f"=== Top {args.top} Contributors ===")
            for i, (name, data) in enumerate(sorted_contributors[:args.top], 1):
                print(f"{i:3}. {data['commits']:5} {name}")

if __name__ == '__main__':
    main()