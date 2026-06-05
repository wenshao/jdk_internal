#!/usr/bin/env python3
"""
Generate by-version/jdkXX/contributions.md from current PR data.

Scope: PRs where jbs_fix_version == NN (e.g., "26" for JDK 26).

Usage:
    python3 scripts/generate-version-contributions.py             # all versions
    python3 scripts/generate-version-contributions.py 26 27       # specific versions
"""

import csv, json, os, re, sys, glob
from collections import Counter
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CSV_FILE = os.path.join(ROOT_DIR, 'by-pr/all-integrated-prs.csv')
ORG_MAP_FILE = os.path.join(SCRIPT_DIR, '.author-org-mapping.json')
TODAY = date.today().isoformat()


def build_profile_map():
    """Extract username → profile-name mapping from existing contribution files."""
    profile_map = {}
    for f in glob.glob(os.path.join(ROOT_DIR, 'by-version/jdk*/contributions.md')):
        with open(f) as fh:
            content = fh.read()
        for username, profile in re.findall(
            r'\[([\w-]+)\]\(\.\./\.\./by-contributor/profiles/([\w-]+)\.md\)',
            content
        ):
            profile_map[username] = profile
    return profile_map


def org_to_profile_dir(org):
    """Map org name to its profile directory slug."""
    mapping = {
        'Oracle': 'oracle', 'Amazon': 'amazon', 'SAP': 'sap',
        'Red Hat': 'redhat', 'IBM': 'ibm', 'Intel': 'intel',
        'Alibaba': 'alibaba', 'Google': 'google', 'ARM': 'arm',
        'ByteDance': 'bytedance', 'Tencent': 'tencent', 'Huawei': 'huawei',
        'BellSoft': 'bellsoft', 'Loongson': 'loongson', 'Datadog': 'datadog',
        'JetBrains': 'independent', 'NTT Data': 'independent',
        'Independent': 'independent', 'Devexperts': 'independent',
        'Rivos': 'independent', 'Nvidia': 'independent', 'Azul': 'independent',
        'ISCAS': 'iscas-plct', 'Microsoft': 'microsoft', 'Apple': 'apple',
    }
    return mapping.get(org, 'independent')


def render_org_table(org_counts, total):
    lines = ["| 排名 | 组织 | PRs | 占比 |", "|------|------|-----|------|"]
    for i, (org, count) in enumerate(org_counts.most_common(25), 1):
        slug = org_to_profile_dir(org)
        pct = count * 100 // total if total else 0
        cnt_str = f"{count:,}" if count >= 1000 else str(count)
        lines.append(f"| {i} | [{org}](../../contributors/orgs/{slug}.md) | {cnt_str} | {pct}% |")
    return '\n'.join(lines)


def render_author_table(jdk_prs, profile_map, org_map):
    author_counts = Counter(r['author'] for r in jdk_prs)
    lines = ["| 排名 | 贡献者 | PRs | 组织 |", "|------|--------|-----|------|"]
    for i, (author, count) in enumerate(author_counts.most_common(50), 1):
        # Org priority: 1) org_map.json (curated), 2) majority of CSV org column for this author
        org = org_map.get(author, {}).get('org', '')
        if not org:
            author_rows = [r for r in jdk_prs if r['author'] == author]
            org_dist = Counter(r['org'] for r in author_rows if r.get('org'))
            if org_dist:
                org = org_dist.most_common(1)[0][0]

        # Build author cell
        if author in profile_map:
            author_cell = f"[{author}](../../by-contributor/profiles/{profile_map[author]}.md)"
        else:
            author_cell = author

        # Build org cell
        if org:
            slug = org_to_profile_dir(org)
            org_cell = f"[{org}](../../contributors/orgs/{slug}.md)"
        else:
            org_cell = ""

        cnt_str = f"{count:,}" if count >= 1000 else str(count)
        lines.append(f"| {i} | {author_cell} | {cnt_str} | {org_cell} |")
    return '\n'.join(lines)


def render_module_table(jdk_prs):
    counts = Counter(r['module'] for r in jdk_prs if r['module'])
    lines = ["| 模块 | PRs |", "|------|-----|"]
    for mod, cnt in counts.most_common(20):
        lines.append(f"| {mod} | {cnt} |")
    return '\n'.join(lines)


def render_type_table(jdk_prs):
    counts = Counter(r['pr_type'] for r in jdk_prs if r['pr_type'])
    lines = ["| 类型 | PRs |", "|------|-----|"]
    for t, cnt in counts.most_common():
        lines.append(f"| {t} | {cnt} |")
    return '\n'.join(lines)


def generate_version(ver_num, rows, profile_map, org_map, override_total=None):
    """Generate contributions.md content for a specific JDK version."""
    fix_ver = str(ver_num)
    # Scope: prefer jbs_fix_version, but fall back to jdk_version for in-development versions
    jdk_prs = [r for r in rows if r.get('jbs_fix_version') == fix_ver]

    # For latest in-development version, also include PRs targeting it without fix_version yet
    # (rare, but covers edge cases)
    if not jdk_prs:
        return None

    total = len(jdk_prs)

    # Compute org stats - priority: org_map.json, then CSV org, then Independent
    org_counts = Counter()
    for r in jdk_prs:
        org = org_map.get(r['author'], {}).get('org', '') or r.get('org') or 'Independent'
        org_counts[org] += 1

    total_str = f"{total:,}"

    content = f"""# JDK {ver_num} 贡献分析

> 基于 {total_str} 个 Integrated PRs 的数据分析（更新至 {TODAY}）

---

## 组织贡献

{render_org_table(org_counts, total)}

## Top 50 贡献者

{render_author_table(jdk_prs, profile_map, org_map)}

## 模块分布

{render_module_table(jdk_prs)}

## PR 类型

{render_type_table(jdk_prs)}

---
> **数据来源**: by-pr/all-integrated-prs.csv
"""
    return content


def main():
    # Determine target versions
    args = sys.argv[1:]
    if args:
        versions = [int(v) for v in args]
    else:
        versions = list(range(11, 28))

    # Load data
    with open(CSV_FILE) as f:
        rows = list(csv.DictReader(f))

    org_map = json.load(open(ORG_MAP_FILE))
    profile_map = build_profile_map()

    print(f"Loaded {len(rows)} PRs, {len(profile_map)} profile mappings")

    for ver in versions:
        out_path = os.path.join(ROOT_DIR, f'by-version/jdk{ver}/contributions.md')
        if not os.path.exists(os.path.dirname(out_path)):
            print(f"  JDK {ver}: directory does not exist, skipping")
            continue

        content = generate_version(ver, rows, profile_map, org_map)
        if content is None:
            print(f"  JDK {ver}: no PRs with fix_version={ver}, skipping")
            continue

        with open(out_path, 'w') as f:
            f.write(content)

        # Count PRs for status report
        fix_ver = str(ver)
        cnt = sum(1 for r in rows if r.get('jbs_fix_version') == fix_ver)
        print(f"  JDK {ver}: {cnt} PRs → {out_path}")


if __name__ == '__main__':
    main()
