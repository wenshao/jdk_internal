#!/usr/bin/env python3
"""
Regenerate deep statistics reports in contributors/stats/ from current PR data.

Generates:
- trends.md (annual org trends)
- by-year.md (annual by repo category)
- by-org.md (organization breakdown)
- top50.md (top 50 cross-repo contributors)
- overview.md (data asset overview)

Usage:
    python3 scripts/generate-stats-reports.py
"""

import csv, glob, json, os
from collections import Counter, defaultdict
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
ORG_MAP_FILE = os.path.join(SCRIPT_DIR, '.author-org-mapping.json')
TODAY = date.today().isoformat()

REPO_CLASSIFY = {
    'mainline': ['by-pr'],
    'lts': ['jdk8u-dev', 'jdk11u-dev', 'jdk17u-dev', 'jdk21u-dev', 'jdk22u', 'jdk23u', 'jdk24u', 'jdk25u-dev',
            'riscv-port-jdk11u', 'riscv-port-jdk17u', 'shenandoah-jdk21u'],
    'experimental': ['valhalla', 'panama-foreign', 'loom', 'leyden', 'lilliput', 'babylon', 'amber',
                     'crac', 'mobile', 'riscv-port', 'shenandoah'],
    'tools': ['jfx', 'jmc'],
}


def load_data():
    org_map = json.load(open(ORG_MAP_FILE))
    all_data = {}
    for category, repos in REPO_CLASSIFY.items():
        for repo in repos:
            csv_path = os.path.join(ROOT_DIR, repo, 'all-integrated-prs.csv')
            if not os.path.exists(csv_path):
                continue
            with open(csv_path) as f:
                rows = list(csv.DictReader(f))
            all_data[repo] = (category, rows)
    return all_data, org_map


def get_org(author, csv_org, org_map):
    """Get org for an author, preferring map > CSV > 未映射."""
    if author in org_map:
        return org_map[author].get('org', '') or '未映射'
    if csv_org:
        return csv_org
    return '未映射'


def gen_trends(all_data, org_map):
    """Annual organization trends - based on main repo only (by-pr)."""
    yearly = defaultdict(lambda: Counter())
    if 'by-pr' not in all_data:
        return None
    _, rows = all_data['by-pr']

    for r in rows:
        year = r.get('created', '')[:4]
        if not year:
            continue
        author = r.get('author', '')
        org = org_map.get(author, {}).get('org', '') or r.get('org', '') or '未映射'
        # Group small orgs as "Other"
        yearly[year][org] += 1

    years = sorted(yearly.keys())
    # Top orgs across all years
    org_totals = Counter()
    for y in years:
        for org, cnt in yearly[y].items():
            org_totals[org] += cnt

    main_orgs = ['Oracle', 'SAP', 'Amazon', 'Red Hat', 'Alibaba']

    lines = ["# 贡献趋势分析", ""]
    lines.append(f"> 基于 {len(rows):,} PRs 主仓库 (openjdk/jdk) 数据")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 年度组织趋势")
    lines.append("")
    header = "| 年份 | " + " | ".join(main_orgs) + " | 其他 | 总计 |"
    sep = "|------|" + "|".join(["--------"] * (len(main_orgs) + 2)) + "|"
    lines.append(header)
    lines.append(sep)
    for y in years:
        row_data = []
        total = sum(yearly[y].values())
        other = total
        for o in main_orgs:
            cnt = yearly[y].get(o, 0)
            row_data.append(str(cnt))
            other -= cnt
        row_data.append(str(other))
        row_data.append(f"**{total}**")
        lines.append(f"| {y} | " + " | ".join(row_data) + " |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"> **统计时间**: {TODAY}")
    return "\n".join(lines) + "\n"


def gen_by_year(all_data):
    """Annual by repo category - all repos."""
    yearly = defaultdict(lambda: Counter())
    total = 0
    for repo, (cat, rows) in all_data.items():
        total += len(rows)
        for r in rows:
            year = r.get('created', '')[:4]
            if year:
                yearly[year][cat] += 1

    years = sorted(yearly.keys())
    lines = ["# 年度贡献趋势 (全仓库)", ""]
    lines.append(f"> 基于 25 个仓库, {total:,} 个 Integrated PRs")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 年度 PR 分布")
    lines.append("")
    lines.append("| 年份 | 主线 | LTS维护 | 实验性 | 工具 | 总计 |")
    lines.append("|------|------|---------|--------|------|------|")
    for y in years:
        yc = yearly[y]
        yt = sum(yc.values())
        lines.append(f"| {y} | {yc.get('mainline', 0)} | {yc.get('lts', 0)} | {yc.get('experimental', 0)} | {yc.get('tools', 0)} | **{yt}** |")

    # Trend chart
    lines.append("")
    lines.append("## 趋势图")
    lines.append("")
    lines.append("```")
    max_total = max(sum(yearly[y].values()) for y in years)
    for y in years:
        yt = sum(yearly[y].values())
        bar = '█' * (yt * 50 // max_total)
        lines.append(f"{y}: {bar} {yt}")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"> **统计时间**: {TODAY}")
    return "\n".join(lines) + "\n"


def gen_by_org(all_data, org_map):
    """Organization breakdown."""
    org_data = defaultdict(lambda: defaultdict(int))
    org_authors = defaultdict(set)
    total = 0
    for repo, (cat, rows) in all_data.items():
        total += len(rows)
        for r in rows:
            author = r.get('author', '')
            if not author:
                continue
            org = org_map.get(author, {}).get('org', '') or r.get('org', '') or '未映射'
            org_data[org][cat] += 1
            org_authors[org].add(author)

    # Sort orgs by total
    org_totals = {org: sum(d.values()) for org, d in org_data.items()}
    sorted_orgs = sorted(org_totals.keys(), key=lambda o: -org_totals[o])

    lines = ["# 按组织统计 (全仓库)", ""]
    lines.append(f"> 基于 25 个仓库, {total:,} 个 Integrated PRs")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 组织贡献全景")
    lines.append("")
    lines.append("| 排名 | 组织 | 主线 | LTS维护 | 实验性 | 工具 | 总计 | 贡献者数 | 占比 |")
    lines.append("|------|------|------|---------|--------|------|------|---------|------|")
    grand_total = sum(org_totals.values())
    for i, org in enumerate(sorted_orgs[:25], 1):
        d = org_data[org]
        t = org_totals[org]
        pct = t * 100 / grand_total
        lines.append(f"| {i} | {org} | {d.get('mainline',0)} | {d.get('lts',0)} | {d.get('experimental',0)} | {d.get('tools',0)} | **{t}** | {len(org_authors[org])} | {pct:.1f}% |")

    total_authors = sum(len(s) for s in org_authors.values())
    lines.append("")
    lines.append(f"**总计**: {grand_total:,} PRs, {total_authors} 贡献者")

    # Specialization analysis
    lines.append("")
    lines.append("## 关键洞察")
    lines.append("")
    lines.append("### 组织专业化指数")
    lines.append("")
    lines.append("| 组织 | 主线占比 | LTS占比 | 实验占比 | 特征 |")
    lines.append("|------|---------|---------|---------|------|")
    for org in sorted_orgs[:15]:
        if org == '未映射':
            continue
        d = org_data[org]
        t = org_totals[org]
        if t < 50:
            continue
        m_pct = d.get('mainline', 0) * 100 // t
        l_pct = d.get('lts', 0) * 100 // t
        e_pct = d.get('experimental', 0) * 100 // t
        if l_pct > 70:
            char = "LTS 维护型"
        elif m_pct > 80:
            char = "主线创新型"
        elif e_pct > 30:
            char = "实验探索型"
        else:
            char = "均衡型"
        lines.append(f"| {org} | {m_pct}% | {l_pct}% | {e_pct}% | {char} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"> **统计时间**: {TODAY}")
    return "\n".join(lines) + "\n"


def gen_top50(all_data, org_map):
    """Top 50 cross-repo contributors."""
    author_data = defaultdict(lambda: defaultdict(int))
    author_repos = defaultdict(set)
    total = 0
    for repo, (cat, rows) in all_data.items():
        total += len(rows)
        for r in rows:
            author = r.get('author', '')
            if not author:
                continue
            author_data[author][cat] += 1
            author_repos[author].add(repo)

    author_totals = {a: sum(d.values()) for a, d in author_data.items()}
    sorted_authors = sorted(author_totals.keys(), key=lambda a: -author_totals[a])

    lines = ["# Top 50 贡献者 (全仓库)", ""]
    lines.append(f"> 基于 25 个仓库, {total:,} 个 Integrated PRs 的完整数据")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("| 排名 | 贡献者 | 组织 | 主线 | LTS维护 | 实验性 | 工具 | 总计 | 仓库数 |")
    lines.append("|------|--------|------|------|---------|--------|------|------|--------|")
    for i, author in enumerate(sorted_authors[:50], 1):
        d = author_data[author]
        t = author_totals[author]
        org = org_map.get(author, {}).get('org', '') or '未映射'
        lines.append(f"| {i} | {author} | {org} | {d.get('mainline',0)} | {d.get('lts',0)} | {d.get('experimental',0)} | {d.get('tools',0)} | **{t}** | {len(author_repos[author])} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"> **统计时间**: {TODAY}")
    return "\n".join(lines) + "\n"


def gen_overview(all_data, org_map):
    """Data asset overview."""
    total = sum(len(rows) for _, rows in all_data.values())
    all_authors = set()
    for repo, (cat, rows) in all_data.items():
        for r in rows:
            if r.get('author'):
                all_authors.add(r['author'])

    # Profile count
    import glob as g
    profiles = len(g.glob(os.path.join(ROOT_DIR, 'by-contributor/profiles/*.md')))
    org_pages = len(g.glob(os.path.join(ROOT_DIR, 'contributors/orgs/*.md')))

    # Repo stats
    repo_stats = []
    for repo, (cat, rows) in all_data.items():
        author_count = len(set(r['author'] for r in rows if r.get('author')))
        repo_stats.append((repo, len(rows), author_count, cat))
    repo_stats.sort(key=lambda x: -x[1])

    lines = ["# 数据资产概览", ""]
    lines.append("> OpenJDK 贡献分析数据库完整统计")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 核心指标")
    lines.append("")
    lines.append("| 指标 | 值 |")
    lines.append("|------|-----|")
    lines.append(f"| **总 Integrated PRs** | **{total:,}** |")
    lines.append(f"| **覆盖仓库** | **{len(all_data)}** |")
    lines.append(f"| **唯一贡献者** | **{len(all_authors)}** |")
    lines.append(f"| **Census 成员** | **672** |")
    lines.append(f"| **贡献者 Profiles** | **{profiles}** |")
    lines.append(f"| **组织页面** | **{org_pages}** |")
    lines.append(f"| **统计时间** | {TODAY} |")

    lines.append("")
    lines.append("## 仓库分布")
    lines.append("")
    lines.append("| 仓库 | PRs | 贡献者 | 类别 |")
    lines.append("|------|-----|--------|------|")
    cat_zh = {'mainline': '主线', 'lts': 'LTS维护', 'experimental': '实验性', 'tools': '工具'}
    for repo, prs, authors, cat in repo_stats:
        lines.append(f"| {repo} | {prs:,} | {authors} | {cat_zh.get(cat, cat)} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"> **生成时间**: {TODAY}")
    return "\n".join(lines) + "\n"


def main():
    all_data, org_map = load_data()
    total = sum(len(rows) for _, rows in all_data.values())
    print(f"Loaded {len(all_data)} repos, {total:,} PRs")
    print()

    generators = [
        ('trends.md', gen_trends),
        ('by-year.md', gen_by_year),
        ('by-org.md', gen_by_org),
        ('top50.md', gen_top50),
        ('overview.md', gen_overview),
    ]

    for filename, gen_fn in generators:
        out_path = os.path.join(ROOT_DIR, 'contributors/stats', filename)
        if gen_fn == gen_trends:
            content = gen_fn(all_data, org_map)
        elif gen_fn == gen_by_year:
            content = gen_fn(all_data)
        elif gen_fn in (gen_by_org, gen_top50, gen_overview):
            content = gen_fn(all_data, org_map)
        if content is None:
            print(f"  {filename}: SKIPPED")
            continue
        with open(out_path, 'w') as f:
            f.write(content)
        print(f"  ✓ {filename}")


if __name__ == '__main__':
    main()
