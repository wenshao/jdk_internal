#!/usr/bin/env python3
"""
Cross-file consistency checker for JDK documentation.

Checks:
1. JDK version type consistency (JDK 25 = LTS, JDK 26 = non-LTS)
2. Placeholder detection (TODO, TBD, FIXME, WIP, etc.)
3. Contributor organization conflicts across files
4. JEP-to-JDK-version attribution consistency
5. PR count discrepancies for contributors mentioned in multiple files

Usage: python3 scripts/check_consistency.py
"""

import re
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set


REPO_ROOT = Path(__file__).resolve().parent.parent

# Patterns for placeholder detection
PLACEHOLDER_PATTERNS = [
    r'\bTODO\b',
    r'待补充',
    r'\bTBD\b',
    r'\bFIXME\b',
    r'\bWIP\b',
    r'需要补充',
]
PLACEHOLDER_RE = re.compile('|'.join(PLACEHOLDER_PATTERNS))

# JDK 25 should always be LTS
JDK25_BAD_RE = re.compile(
    r'JDK\s*25\s*[^()]*?\b(non-LTS|非\s*LTS|Feature\s*版本|Feature\s*Release)\b',
    re.IGNORECASE
)
# But skip lines that say "JDK 25 is LTS" or are instructions about what NOT to say
JDK25_NEGATION_RE = re.compile(
    r'(WRONG|❌|不要|is LTS|是\s*LTS|IS LTS)', re.IGNORECASE
)

# JDK 26 should NOT be LTS -- patterns that directly associate JDK 26 with LTS
JDK26_DIRECT_LTS_PATTERNS = [
    # "JDK 26 (LTS)" or "JDK 26（LTS）"
    re.compile(r'JDK\s*26\s*[（(]\s*LTS\s*[)）]', re.IGNORECASE),
    # "JDK 26 LTS" (adjacent)
    re.compile(r'JDK\s*26\s+LTS\b', re.IGNORECASE),
    # Lists like "JDK 17, JDK 21, JDK 26" in an LTS context
    re.compile(r'LTS[^.|\n]{0,40}JDK\s*26\b', re.IGNORECASE),
    # "JDK 26 是 LTS" (Chinese: JDK 26 is LTS)
    re.compile(r'JDK\s*26\s*是\s*LTS', re.IGNORECASE),
    # "JDK 26 | ... | LTS |" table pattern
    re.compile(r'JDK\s*26\s*\|[^|]*\|\s*LTS\s*\|', re.IGNORECASE),
]
JDK26_OK_RE = re.compile(
    r'(non-LTS|非\s*LTS|WRONG|❌|不是|Feature|不要|is non-LTS|是 LTS 版本吗)',
    re.IGNORECASE
)

# Contributor + org from markdown tables: "| Name | Org |" or "| Name | ... | Org |"
CONTRIBUTOR_ORG_RE = re.compile(
    r'\|\s*\[?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\]?'  # Name (2+ words, capitalized)
    r'[^|]*\|'                                         # optional link etc + pipe
    r'[^|]*?'                                          # stuff between
    r'\b(Oracle|Red Hat|Google|Amazon|SAP|Alibaba|Tencent|Huawei|'
    r'Microsoft|IBM|Azul|BellSoft|Intel|Independent|Loongson|'
    r'Oracle Labs|ISCAS|Rivos)\b',
    re.IGNORECASE
)

# JEP number to JDK version mapping from text
JEP_VERSION_RE = re.compile(
    r'JEP\s*(\d{3,4})\b[^|\n]{0,80}?\bJDK\s*(\d{2})\b'
    r'|'
    r'\bJDK\s*(\d{2})\b[^|\n]{0,80}?\bJEP\s*(\d{3,4})\b'
)

# Contributor PR count: "Name ... N PRs" or table rows with name and number
CONTRIBUTOR_COUNT_RE = re.compile(
    r'\|\s*\*{0,2}\[?([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})\]?'
    r'[^|]*\|[^|]*?\b(\d{2,5})\b'
)

# Words that appear in JDK feature/concept names, not person names
NOT_PERSON_WORDS = {
    'pattern', 'matching', 'record', 'sealed', 'switch', 'virtual',
    'thread', 'string', 'vector', 'foreign', 'function', 'memory',
    'class', 'module', 'stream', 'lambda', 'value', 'primitive',
    'structured', 'concurrency', 'scoped', 'preview', 'incubator',
    'unnamed', 'lazy', 'constant', 'compact', 'text', 'block',
    'local', 'variable', 'type', 'inference', 'access', 'control',
    'optimize', 'remove', 'deprecate', 'enhanced', 'flexible',
    'red', 'hat', 'oracle', 'labs', 'shenandoah', 'gc', 'api',
    'jit', 'jvm', 'jdk', 'java', 'project', 'openjdk', 'graal',
    'total', 'changes', 'commits', 'unified', 'generics', 'generic',
    'stable', 'security', 'performance', 'platform', 'build',
    'compiler', 'runtime', 'network', 'library', 'test', 'testing',
    'native', 'image', 'spring', 'boot', 'new', 'old', 'hot', 'spot',
    'garbage', 'collector', 'collection', 'startup', 'time', 'code',
    'heap', 'stack', 'object', 'caching', 'method', 'profiling',
}


def _is_likely_person_name(name: str) -> bool:
    """Heuristic: filter out JDK feature/concept names mistaken as people."""
    words = name.lower().split()
    if len(words) < 2 or len(words) > 3:
        return False
    if any(w in NOT_PERSON_WORDS for w in words):
        return False
    return True


def collect_md_files(root: Path) -> List[Path]:
    """Collect all .md files, skipping hidden dirs and templates."""
    files = []
    for p in sorted(root.rglob('*.md')):
        rel = str(p.relative_to(root))
        if any(part.startswith('.') for part in p.parts):
            continue
        if 'TEMPLATE' in p.name or '_template' in p.name:
            continue
        files.append(p)
    return files


def rel_path(path: Path) -> str:
    """Return path relative to repo root."""
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def check_version_types(files: List[Path]) -> List[dict]:
    """Check JDK 25 = LTS and JDK 26 = non-LTS consistency."""
    issues = []

    for fpath in files:
        try:
            lines = fpath.read_text(encoding='utf-8').splitlines()
        except (UnicodeDecodeError, OSError):
            continue

        for i, line in enumerate(lines, 1):
            # JDK 25 incorrectly marked as non-LTS / Feature
            if JDK25_BAD_RE.search(line) and not JDK25_NEGATION_RE.search(line):
                issues.append({
                    'type': 'jdk25_not_lts',
                    'file': rel_path(fpath),
                    'line': i,
                    'text': line.strip()[:120],
                })

            # JDK 26 incorrectly marked as LTS
            if any(p.search(line) for p in JDK26_DIRECT_LTS_PATTERNS):
                if not JDK26_OK_RE.search(line):
                    issues.append({
                        'type': 'jdk26_lts',
                        'file': rel_path(fpath),
                        'line': i,
                        'text': line.strip()[:120],
                    })

    return issues


def check_placeholders(files: List[Path]) -> List[dict]:
    """Find placeholder strings across all files."""
    hits = []
    # Skip files that document rules or are generated reports
    skip_names = {'AGENTS.md', 'link_verification_report.md'}
    for fpath in files:
        if fpath.name in skip_names:
            continue
        try:
            lines = fpath.read_text(encoding='utf-8').splitlines()
        except (UnicodeDecodeError, OSError):
            continue

        for i, line in enumerate(lines, 1):
            m = PLACEHOLDER_RE.search(line)
            if m:
                hits.append({
                    'file': rel_path(fpath),
                    'line': i,
                    'match': m.group(),
                    'text': line.strip()[:120],
                })
    return hits


def check_contributor_orgs(files: List[Path]) -> List[dict]:
    """Find contributors attributed to different orgs in different files."""
    # name -> { org -> [(file, line)] }
    contributor_orgs: Dict[str, Dict[str, List[Tuple[str, int]]]] = defaultdict(
        lambda: defaultdict(list)
    )

    for fpath in files:
        try:
            lines = fpath.read_text(encoding='utf-8').splitlines()
        except (UnicodeDecodeError, OSError):
            continue

        for i, line in enumerate(lines, 1):
            for m in CONTRIBUTOR_ORG_RE.finditer(line):
                name = re.sub(r'\s+', ' ', m.group(1)).strip()
                if not _is_likely_person_name(name):
                    continue
                org = m.group(2).strip()
                contributor_orgs[name][org].append((rel_path(fpath), i))

    # Find conflicts (multiple orgs for same person)
    conflicts = []
    for name, orgs in sorted(contributor_orgs.items()):
        if len(orgs) > 1:
            conflicts.append({
                'name': name,
                'orgs': {org: locs for org, locs in orgs.items()},
            })
    return conflicts


def check_jep_versions(files: List[Path]) -> List[dict]:
    """Check that each JEP is attributed to the same JDK version everywhere."""
    # jep_number -> { jdk_version -> [(file, line)] }
    jep_map: Dict[str, Dict[str, List[Tuple[str, int]]]] = defaultdict(
        lambda: defaultdict(list)
    )

    for fpath in files:
        if fpath.name == 'AGENTS.md':
            continue
        try:
            lines = fpath.read_text(encoding='utf-8').splitlines()
        except (UnicodeDecodeError, OSError):
            continue

        for i, line in enumerate(lines, 1):
            for m in JEP_VERSION_RE.finditer(line):
                jep = m.group(1) or m.group(4)
                ver = m.group(2) or m.group(3)
                if jep and ver:
                    jep_map[jep][ver].append((rel_path(fpath), i))

    conflicts = []
    for jep, versions in sorted(jep_map.items(), key=lambda x: int(x[0])):
        if len(versions) > 1:
            conflicts.append({
                'jep': jep,
                'versions': {v: locs for v, locs in versions.items()},
            })
    return conflicts


def check_pr_counts(files: List[Path]) -> List[dict]:
    """Flag contributors whose PR counts differ by >10% across files."""
    # name -> [(count, file, line)]
    counts: Dict[str, List[Tuple[int, str, int]]] = defaultdict(list)

    for fpath in files:
        try:
            lines = fpath.read_text(encoding='utf-8').splitlines()
        except (UnicodeDecodeError, OSError):
            continue

        for i, line in enumerate(lines, 1):
            for m in CONTRIBUTOR_COUNT_RE.finditer(line):
                name = re.sub(r'\s+', ' ', m.group(1)).strip()
                if not _is_likely_person_name(name):
                    continue
                try:
                    count = int(m.group(2))
                except ValueError:
                    continue
                # Filter out obviously non-PR numbers (years, percentages, etc.)
                if 1900 < count < 2100:
                    continue
                if count < 10 or count > 5000:
                    continue
                counts[name].append((count, rel_path(fpath), i))

    discrepancies = []
    for name, entries in sorted(counts.items()):
        if len(entries) < 2:
            continue
        # Check from different files only
        by_file = defaultdict(list)
        for cnt, f, ln in entries:
            by_file[f].append((cnt, ln))

        if len(by_file) < 2:
            continue

        all_counts = [cnt for cnt, _, _ in entries]
        min_c, max_c = min(all_counts), max(all_counts)
        if min_c == 0:
            continue
        if (max_c - min_c) / min_c > 0.10:
            discrepancies.append({
                'name': name,
                'entries': [(cnt, f, ln) for cnt, f, ln in entries],
                'min': min_c,
                'max': max_c,
            })

    return discrepancies


def print_report(version_issues, placeholders, org_conflicts,
                 jep_conflicts, pr_discrepancies):
    """Print a grouped report and return total issue count."""
    total_issues = 0
    affected_files: Set[str] = set()

    print("=== Cross-File Consistency Report ===\n")

    # --- 1. Version Type Consistency ---
    print("### 1. Version Type Consistency")
    jdk25_issues = [x for x in version_issues if x['type'] == 'jdk25_not_lts']
    jdk26_issues = [x for x in version_issues if x['type'] == 'jdk26_lts']

    if not jdk25_issues:
        print("  ✅ JDK 25 LTS: consistent across all files")
    else:
        print(f"  ⚠️ JDK 25: {len(jdk25_issues)} file(s) incorrectly mark as non-LTS/Feature")
        for item in jdk25_issues:
            print(f"    - {item['file']}:{item['line']} \"{item['text']}\"")
            affected_files.add(item['file'])
        total_issues += len(jdk25_issues)

    if not jdk26_issues:
        print("  ✅ JDK 26 non-LTS: consistent across all files")
    else:
        print(f"  ⚠️ JDK 26: {len(jdk26_issues)} file(s) incorrectly mark as LTS")
        for item in jdk26_issues:
            print(f"    - {item['file']}:{item['line']} \"{item['text']}\"")
            affected_files.add(item['file'])
        total_issues += len(jdk26_issues)
    print()

    # --- 2. Placeholders ---
    print("### 2. Placeholders Found")
    if not placeholders:
        print("  ✅ No placeholders found")
    else:
        ph_files = set(p['file'] for p in placeholders)
        print(f"  ⚠️ {len(placeholders)} placeholder(s) in {len(ph_files)} file(s):")
        # Group by file for compact output
        by_file = defaultdict(list)
        for item in placeholders:
            by_file[item['file']].append(item)
            affected_files.add(item['file'])
        for f, items in sorted(by_file.items()):
            print(f"    {f}: {len(items)} placeholder(s)")
            for item in items[:3]:
                print(f"      :{item['line']} \"{item['match']}\" ... {item['text'][:70]}")
            if len(items) > 3:
                print(f"      ... and {len(items) - 3} more")
        total_issues += len(placeholders)
    print()

    # --- 3. Contributor Org Conflicts ---
    print("### 3. Contributor Org Conflicts")
    if not org_conflicts:
        print("  ✅ No organization conflicts found")
    else:
        print(f"  ⚠️ {len(org_conflicts)} contributor(s) with conflicting organizations:")
        for conflict in org_conflicts:
            orgs_str = ', '.join(conflict['orgs'].keys())
            print(f"  - {conflict['name']}: attributed to [{orgs_str}]")
            for org, locs in conflict['orgs'].items():
                for f, ln in locs[:3]:  # limit output per org
                    print(f"      {org}: {f}:{ln}")
                    affected_files.add(f)
                if len(locs) > 3:
                    print(f"      ... and {len(locs) - 3} more")
        total_issues += len(org_conflicts)
    print()

    # --- 4. JEP Version Conflicts ---
    print("### 4. JEP-to-JDK Version Consistency")
    if not jep_conflicts:
        print("  ✅ All JEPs consistently attributed to same JDK version")
    else:
        print(f"  ⚠️ {len(jep_conflicts)} JEP(s) attributed to multiple JDK versions:")
        for conflict in jep_conflicts:
            versions_str = ', '.join(f"JDK {v}" for v in conflict['versions'].keys())
            print(f"  - JEP {conflict['jep']}: seen in [{versions_str}]")
            for ver, locs in conflict['versions'].items():
                for f, ln in locs[:2]:
                    print(f"      JDK {ver}: {f}:{ln}")
                    affected_files.add(f)
                if len(locs) > 2:
                    print(f"      ... and {len(locs) - 2} more")
        total_issues += len(jep_conflicts)
    print()

    # --- 5. PR Count Discrepancies ---
    print("### 5. PR Count Discrepancies (>10%)")
    if not pr_discrepancies:
        print("  ✅ No significant PR count discrepancies found")
    else:
        print(f"  ⚠️ {len(pr_discrepancies)} contributor(s) with count discrepancies:")
        for d in pr_discrepancies:
            print(f"  - {d['name']}: range {d['min']}-{d['max']}")
            for cnt, f, ln in d['entries'][:5]:
                print(f"      {cnt}: {f}:{ln}")
                affected_files.add(f)
            if len(d['entries']) > 5:
                print(f"      ... and {len(d['entries']) - 5} more")
        total_issues += len(pr_discrepancies)
    print()

    # --- Summary ---
    print("---")
    print(f"Summary: {total_issues} issue(s) found across {len(affected_files)} file(s)")
    return total_issues


def main():
    md_files = collect_md_files(REPO_ROOT)
    print(f"Scanning {len(md_files)} markdown files...\n")

    version_issues = check_version_types(md_files)
    placeholders = check_placeholders(md_files)
    org_conflicts = check_contributor_orgs(md_files)
    jep_conflicts = check_jep_versions(md_files)
    pr_discrepancies = check_pr_counts(md_files)

    total = print_report(
        version_issues, placeholders, org_conflicts,
        jep_conflicts, pr_discrepancies,
    )

    sys.exit(1 if total > 0 else 0)


if __name__ == '__main__':
    main()
