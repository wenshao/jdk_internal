#!/usr/bin/env python3
"""
Merge new PRs from jdk/all-integrated-prs.csv into by-pr/all-integrated-prs.csv.
Enriches with org/country, module, jdk_version, pr_type classification.

Usage: python3 scripts/merge-new-prs.py [--dry-run]
"""

import csv, json, os, re, sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
RAW_CSV = os.path.join(ROOT_DIR, 'jdk', 'all-integrated-prs.csv')
ENRICHED_CSV = os.path.join(ROOT_DIR, 'by-pr', 'all-integrated-prs.csv')
ORG_MAP_FILE = os.path.join(SCRIPT_DIR, '.author-org-mapping.json')

# JDK version date boundaries (created date cutoffs)
JDK_VERSION_RANGES = [
    ('2026-03-21', 'JDK 27'),
    ('2025-09-01', 'JDK 26'),
    ('2025-01-01', 'JDK 25'),
    ('2024-03-20', 'JDK 24'),
    ('2023-09-20', 'JDK 23'),
    ('2023-03-22', 'JDK 22'),
    ('2022-09-21', 'JDK 21'),
    ('2022-03-23', 'JDK 20'),
    ('2021-09-15', 'JDK 19'),
    ('2021-03-17', 'JDK 18'),
    ('2020-09-16', 'JDK 17'),
    ('2020-03-18', 'JDK 16'),
    ('2000-01-01', 'JDK 15'),
]

# Module classification rules (order matters - first match wins)
MODULE_RULES = [
    (r'\b(G1|g1)\b', 'gc/g1'),
    (r'\b(ZGC|zgc)\b', 'gc/zgc'),
    (r'\b(Shenandoah|shenandoah|GenShen|genshen)\b', 'gc'),
    (r'\b(Serial GC|ParallelGC|GC)\b', 'gc'),
    (r'\bC2\b', 'compiler/c2'),
    (r'\bC1\b', 'compiler/c1'),
    (r'\b(Graal|graal)\b', 'compiler'),
    (r'\b(compiler|JIT|jit)\b', 'compiler'),
    (r'\b(AArch64|aarch64)\b', 'arch/aarch64'),
    (r'\b(RISC-V|riscv|RISCV)\b', 'arch/riscv'),
    (r'\b(x86|X86|x86_64)\b', 'arch/x86'),
    (r'\b(s390|s390x|S390)\b', 'arch/s390'),
    (r'\b(PPC64|ppc64|PowerPC)\b', 'arch/ppc'),
    (r'\b(ARM32|arm32)\b', 'arch/arm'),
    (r'\b(JFR|jfr|FlightRecorder)\b', 'runtime/jfr'),
    (r'\b(CDS|cds|AppCDS|AOT cache)\b', 'runtime/cds'),
    (r'\b(Loom|loom|VirtualThread|virtual thread|Fiber)\b', 'runtime/loom'),
    (r'\b(JVMTI|jvmti|serviceability|SA |jcmd|jstack|jmap)\b', 'runtime/serviceability'),
    (r'\b(thread|Thread|monitor|Monitor|synchroniz)\b', 'runtime/threading'),
    (r'\b(class\s*load|ClassLoad|Metaspace|metaspace)\b', 'runtime/classloading'),
    (r'\b(java\.lang|java\.util|java\.time|java\.math|java\.text)\b', 'core-libs'),
    (r'\b(java\.net|http|HTTP|socket|Socket|URL|URI|HttpClient)\b', 'core-libs/java.net'),
    (r'\b(java\.io|java\.nio|File|Path|Channel|Stream|InputStream|OutputStream)\b', 'core-libs/java.io'),
    (r'\b(java\.security|Security|security|crypto|Cipher|TLS|SSL|PKCS|X509)\b', 'security'),
    (r'\b(javac|javap|javadoc|jshell|jlink|jpackage|jmod)\b', 'tools'),
    (r'\b(Swing|swing|AWT|awt|JavaFX|javafx|Font|font|2D|Graphics)\b', 'client'),
    (r'\b(build|Build|make|Make|configure|autoconf|Makefile)\b', 'build'),
    (r'\b(test|Test|jtreg|TestNG|ProblemList)\b', 'test'),
    (r'\b(doc|Doc|javadoc|Javadoc|comment|Comment|typo|Typo|spec)\b', 'doc'),
]

# PR type classification rules
TYPE_RULES = [
    (r'\b(ProblemList|problemlist)\b', 'test'),
    (r'\b(Revert|revert)\b', 'revert'),
    (r'\b(test|Test|jtreg|TestNG)\b.*\b(add|new|create|enable|improve)\b', 'test'),
    (r'\b(add|Add|new|New|create|Create|implement|Implement)\b.*\b(test|Test)\b', 'test'),
    (r'\b(fix|Fix|crash|Crash|NPE|SEGV|assert|Assert|incorrect|wrong|broken|regression|Regression|bug)\b', 'bugfix'),
    (r'\b(cleanup|Cleanup|clean up|Clean up|remove unused|Remove unused|simplify|Simplify)\b', 'cleanup'),
    (r'\b(refactor|Refactor|restructure|reorganize|rename|Rename)\b', 'refactor'),
    (r'\b(optimiz|Optimiz|improve perf|speed up|faster)\b', 'optimization'),
    (r'\b(update|Update|upgrade|Upgrade|bump)\b', 'update'),
    (r'\b(doc|Doc|javadoc|comment|typo|Typo|spelling)\b', 'doc'),
    (r'\b(build|Build|make|Make|configure|autoconf|Makefile|cmake)\b', 'build'),
    (r'\b(add|Add|new|New|support|Support|implement|Implement|introduce|Introduce|enable|Enable)\b', 'enhancement'),
]


def load_org_mapping():
    try:
        with open(ORG_MAP_FILE) as f:
            return json.load(f)
    except:
        return {}


def classify_jdk_version(created_date):
    for cutoff, version in JDK_VERSION_RANGES:
        if created_date >= cutoff:
            return version
    return ''


def classify_module(title):
    for pattern, module in MODULE_RULES:
        if re.search(pattern, title):
            return module
    return ''


def classify_pr_type(title):
    for pattern, pr_type in TYPE_RULES:
        if re.search(pattern, title):
            return pr_type
    return ''


def extract_sub_component(title):
    # Extract first meaningful word after bug_id prefix
    m = re.match(r'^(?:\d{7,8}:\s*)?(?:\[.*?\]\s*)?(\S+)', title)
    if m:
        word = m.group(1).rstrip(':,')
        if len(word) > 1:
            return word
    return ''


def calc_review_days(created, closed):
    try:
        d1 = datetime.strptime(created, '%Y-%m-%d')
        d2 = datetime.strptime(closed, '%Y-%m-%d')
        return str((d2 - d1).days)
    except:
        return ''


def is_jep_pr(title):
    return '1' if re.search(r'\bJEP\b', title, re.IGNORECASE) else '0'


def is_backport_pr(title):
    return '1' if re.search(r'\b(backport|Backport)\b', title) else '0'


def main():
    dry_run = '--dry-run' in sys.argv

    if not os.path.exists(RAW_CSV):
        print(f"Error: {RAW_CSV} not found. Run fetch-repo-prs.py openjdk/jdk first.")
        sys.exit(1)

    org_map = load_org_mapping()

    # Load existing enriched PRs
    with open(ENRICHED_CSV) as f:
        reader = csv.DictReader(f)
        enriched_fields = reader.fieldnames
        enriched_rows = list(reader)

    existing_prs = {r['pr_number'] for r in enriched_rows}
    print(f"Existing enriched PRs: {len(existing_prs)}")

    # Load raw PRs
    with open(RAW_CSV) as f:
        raw_rows = list(csv.DictReader(f))
    print(f"Raw fetched PRs: {len(raw_rows)}")

    # Find new PRs
    new_rows = [r for r in raw_rows if r['pr_number'] not in existing_prs]
    print(f"New PRs to merge: {len(new_rows)}")

    if not new_rows:
        print("No new PRs to merge.")
        return

    # Enrich new PRs
    enriched_new = []
    for r in new_rows:
        author = r.get('author', '')
        org_info = org_map.get(author, {})
        title = r.get('title', '')
        created = r.get('created', '')
        closed = r.get('closed', '')
        bug_id = r.get('bug_id', '')

        enriched = {
            'bug_id': bug_id,
            'pr_number': r['pr_number'],
            'title': title,
            'author': author,
            'org': org_info.get('org', ''),
            'country': org_info.get('country', ''),
            'created': created,
            'closed': closed,
            'review_days': calc_review_days(created, closed),
            'module': classify_module(title),
            'jdk_version': classify_jdk_version(created),
            'pr_type': classify_pr_type(title),
            'is_backport': is_backport_pr(title),
            'is_jep': is_jep_pr(title),
            'sub_component': extract_sub_component(title.split(': ', 1)[1] if ': ' in title else title),
            'has_analysis': '0',
            'jbs_priority': '',
            'jbs_component': '',
            'jbs_fix_version': '',
            'jbs_labels': '',
            'reviewers': '',
            'sponsor': '',
            'changed_files': '',
            'additions': '',
            'deletions': '',
        }
        enriched_new.append(enriched)

    # Show sample
    print(f"\nSample new PRs:")
    for r in enriched_new[:5]:
        print(f"  #{r['pr_number']}: {r['title'][:60]}... [{r['jdk_version']}] [{r['module']}] [{r['pr_type']}]")

    if dry_run:
        print(f"\n[DRY RUN] Would merge {len(enriched_new)} new PRs.")
        # Show version distribution
        from collections import Counter
        ver_dist = Counter(r['jdk_version'] for r in enriched_new)
        print(f"Version distribution: {dict(ver_dist)}")
        return

    # Merge and write
    all_rows = enriched_rows + enriched_new
    all_rows.sort(key=lambda x: int(x['pr_number']))

    with open(ENRICHED_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=enriched_fields)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\nMerged! Total PRs: {len(all_rows)} (+{len(enriched_new)})")

    # Show version distribution of new PRs
    from collections import Counter
    ver_dist = Counter(r['jdk_version'] for r in enriched_new)
    print(f"New PR version distribution: {dict(ver_dist)}")


if __name__ == '__main__':
    main()
