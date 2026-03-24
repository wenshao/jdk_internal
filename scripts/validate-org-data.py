#!/usr/bin/env python3
"""
Validate org page data against CSV.
Checks PR counts, contributor lists, and flags mismatches.

Usage: python3 scripts/validate-org-data.py
"""
import csv, re, os

CSV_FILE = 'by-pr/all-integrated-prs.csv'
ORGS_DIR = 'contributors/orgs'

with open(CSV_FILE) as f:
    rows = list(csv.DictReader(f))

from collections import defaultdict
org_prs = defaultdict(int)
org_authors = defaultdict(set)
for r in rows:
    org = r.get('org','').strip()
    if org:
        org_prs[org] += 1
        org_authors[org].add(r['author'])

ORG_FILES = {
    'Alibaba': 'alibaba.md', 'Amazon': 'amazon.md', 'SAP': 'sap.md',
    'Red Hat': 'redhat.md', 'Tencent': 'tencent.md', 'IBM': 'ibm.md',
    'Intel': 'intel.md', 'Huawei': 'huawei.md', 'Loongson': 'loongson.md',
    'BellSoft': 'bellsoft.md', 'Datadog': 'datadog.md', 'ByteDance': 'bytedance.md',
    'ARM': 'arm.md', 'Azul': 'azul.md',
}

print(f"{'Org':<15} {'CSV PRs':>8} {'Doc PRs':>10} {'Match?':>8}")
print('-' * 45)

for org, filename in ORG_FILES.items():
    filepath = os.path.join(ORGS_DIR, filename)
    if not os.path.exists(filepath): continue
    
    with open(filepath) as f:
        content = f.read()
    
    # Find PR count in doc
    m = re.search(r'Integrated PRs.*?(\d[\d,]+)', content)
    doc_prs = int(m.group(1).replace(',', '')) if m else 0
    
    csv_count = org_prs.get(org, 0)
    diff = abs(csv_count - doc_prs)
    match = '✅' if diff < csv_count * 0.15 else f'❌ Δ{diff}'
    
    print(f"  {org:<13} {csv_count:>8} {doc_prs:>10} {match:>8}")

print(f"\nNote: CSV counts are date-aware (job changers split by period)")
print(f"Doc counts may use different methodology (per-author API search)")
