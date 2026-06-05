#!/usr/bin/env python3
"""
Enrich sub-repo CSVs (jdk*u-dev, jdk22u..jdk25u-dev, riscv-port-*, shenandoah-*)
with org/country (from .author-org-mapping.json) and review_days (computed).

Why this exists: fetch-repo-prs.py preserves enrichment columns for *existing*
PRs but leaves them empty for *new* PRs. This script fills those empty fields
so the LTS-maintenance / distribution / cross-repo reports stay accurate after a
refresh. It is idempotent and only touches empty cells (never overwrites).

Usage:
    python3 scripts/enrich-subrepo-csvs.py            # all sub-repos
    python3 scripts/enrich-subrepo-csvs.py jdk21u-dev # specific repos
    python3 scripts/enrich-subrepo-csvs.py --dry-run
"""

import csv, json, os, sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
ORG_MAP_FILE = os.path.join(SCRIPT_DIR, '.author-org-mapping.json')

# Sub-repos that carry the enrichment schema (org/country/review_days/reviewers).
SUBREPOS = [
    'jdk8u-dev', 'jdk11u-dev', 'jdk17u-dev', 'jdk21u-dev', 'jdk22u', 'jdk23u',
    'jdk24u', 'jdk25u-dev', 'riscv-port-jdk11u', 'riscv-port-jdk17u',
    'shenandoah-jdk21u',
]

ENRICH_COLS = ('org', 'country', 'review_days')


def calc_review_days(created, closed):
    try:
        d1 = datetime.strptime(created, '%Y-%m-%d')
        d2 = datetime.strptime(closed, '%Y-%m-%d')
        return str((d2 - d1).days)
    except Exception:
        return ''


def enrich_repo(repo, org_map, dry_run=False):
    csv_path = os.path.join(ROOT_DIR, repo, 'all-integrated-prs.csv')
    if not os.path.exists(csv_path):
        return None

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        rows = list(reader)

    # Only operate when the enrichment columns are present in this CSV's schema.
    if not all(c in fields for c in ENRICH_COLS):
        return (repo, 0, 0, len(rows), 'no enrichment schema')

    org_filled = 0
    days_filled = 0
    for r in rows:
        author = r.get('author', '')
        if not r.get('org') and author in org_map:
            info = org_map[author]
            r['org'] = info.get('org', '')
            if not r.get('country'):
                r['country'] = info.get('country', '')
            if r['org']:
                org_filled += 1
        if not r.get('review_days'):
            rd = calc_review_days(r.get('created', ''), r.get('closed', ''))
            if rd != '':
                r['review_days'] = rd
                days_filled += 1

    if not dry_run and (org_filled or days_filled):
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    return (repo, org_filled, days_filled, len(rows), 'ok')


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry_run = '--dry-run' in sys.argv
    targets = args if args else SUBREPOS

    org_map = json.load(open(ORG_MAP_FILE))
    print(f"Loaded org map: {len(org_map)} authors")
    print(f"{'[DRY RUN] ' if dry_run else ''}Enriching {len(targets)} sub-repos\n")

    tot_org = tot_days = 0
    for repo in targets:
        res = enrich_repo(repo, org_map, dry_run)
        if res is None:
            print(f"  {repo}: CSV not found, skipping")
            continue
        repo, org_filled, days_filled, n, status = res
        tot_org += org_filled
        tot_days += days_filled
        print(f"  {repo}: org+{org_filled} review_days+{days_filled} ({n} rows) [{status}]")

    print(f"\nTotal: org+{tot_org}, review_days+{tot_days}"
          f"{' (dry run, not written)' if dry_run else ''}")


if __name__ == '__main__':
    main()
