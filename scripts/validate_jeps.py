#!/usr/bin/env python3
"""Validate JEP references in markdown files against a known-good database.

Usage:
    python3 scripts/validate_jeps.py [--fix] [--verbose] [path...]
"""

import argparse
import os
import re
import sys
from collections import defaultdict

# ── Known-good JEP database ──────────────────────────────────────────────
# Format: jep_number -> (jdk_version, short_title, status)
# status: "final", "preview", "incubator", "experimental", "withdrawn",
#         "deprecated", "removed"

JEP_DB = {
    # JDK 8
    104: (8, "Annotations on Types", "final"),
    107: (8, "Bulk Data Ops", "final"),
    109: (8, "Enhance Core Libraries", "final"),
    120: (8, "Repeating Annotations", "final"),
    126: (8, "Lambda", "final"),
    150: (8, "Date & Time API", "final"),
    174: (8, "Nashorn", "final"),
    176: (8, "Mechanical Checking", "final"),
    # JDK 9
    200: (9, "Modular JDK", "final"),
    201: (9, "Modular Source", "final"),
    222: (9, "jshell", "final"),
    238: (9, "Multi-Release JARs", "final"),
    260: (9, "Encapsulate Internal APIs", "final"),
    261: (9, "Module System", "final"),
    269: (9, "Convenience Factory Methods", "final"),
    # JDK 10
    286: (10, "Local-Variable Type Inference", "final"),
    307: (10, "Parallel Full GC for G1", "final"),
    310: (10, "Application CDS", "final"),
    # JDK 11
    309: (11, "Dynamic Class-File Constants", "final"),
    318: (11, "Epsilon GC", "final"),
    320: (11, "Remove Java EE", "removed"),
    321: (11, "HTTP Client", "final"),
    323: (11, "Lambda Parameters", "final"),
    328: (11, "Flight Recorder", "final"),
    330: (11, "Launch Single-File", "final"),
    333: (11, "ZGC Experimental", "experimental"),
    # JDK 12
    189: (12, "Shenandoah Experimental", "experimental"),
    325: (12, "Switch Expressions Preview", "preview"),
    334: (12, "JVM Constants API", "final"),
    340: (12, "One AArch64 Port", "final"),
    341: (12, "Default CDS Archives", "final"),
    344: (12, "Abortable Mixed Collections G1", "final"),
    346: (12, "Promptly Return Unused Memory G1", "final"),
    # JDK 13
    350: (13, "Dynamic CDS Archives", "final"),
    351: (13, "ZGC Uncommit Memory", "final"),
    353: (13, "Reimplement Socket API", "final"),
    354: (13, "Switch Expressions 2nd Preview", "preview"),
    355: (13, "Text Blocks Preview", "preview"),
    # JDK 14
    305: (14, "Pattern Matching instanceof Preview", "preview"),
    343: (14, "Packaging Tool Incubator", "incubator"),
    345: (14, "NUMA-Aware Memory for G1", "final"),
    358: (14, "Helpful NullPointerExceptions", "final"),
    359: (14, "Records Preview", "preview"),
    361: (14, "Switch Expressions", "final"),
    362: (14, "Deprecate Solaris", "deprecated"),
    363: (14, "Remove CMS GC", "removed"),
    364: (14, "ZGC macOS", "final"),
    365: (14, "ZGC Windows", "final"),
    368: (14, "Text Blocks 2nd Preview", "preview"),
    370: (14, "Foreign-Memory Access Incubator", "incubator"),
    # JDK 15
    371: (15, "Hidden Classes", "final"),
    372: (15, "Remove Nashorn", "removed"),
    373: (15, "Reimplement DatagramSocket", "final"),
    374: (15, "Disable Biased Locking", "final"),
    375: (15, "Pattern Matching instanceof 2nd Preview", "preview"),
    377: (15, "ZGC Production", "final"),
    378: (15, "Text Blocks", "final"),
    379: (15, "Shenandoah Production", "final"),
    381: (15, "Remove Solaris/SPARC", "removed"),
    383: (15, "Foreign-Memory Access 2nd Incubator", "incubator"),
    384: (15, "Records 2nd Preview", "preview"),
    385: (15, "Deprecate RMI Activation", "deprecated"),
    # JDK 16
    338: (16, "Vector API Incubator", "incubator"),
    386: (16, "Alpine Linux Port", "final"),
    387: (16, "Elastic Metaspace", "final"),
    388: (16, "Windows/AArch64 Port", "final"),
    389: (16, "Foreign Linker Incubator", "incubator"),
    390: (16, "Warnings for Value-Based Classes", "final"),
    392: (16, "Packaging Tool", "final"),
    393: (16, "Foreign-Memory Access 3rd Incubator", "incubator"),
    394: (16, "Pattern Matching instanceof", "final"),
    395: (16, "Records", "final"),
    396: (16, "Strongly Encapsulate JDK Internals", "final"),
    397: (16, "Sealed Classes 2nd Preview", "preview"),
    # JDK 17
    306: (17, "Restore Always-Strict FP", "final"),
    356: (17, "Enhanced Pseudo-Random Number Generators", "final"),
    382: (17, "New macOS Rendering Pipeline", "final"),
    391: (17, "macOS/AArch64 Port", "final"),
    398: (17, "Deprecate Applet API", "deprecated"),
    403: (17, "Strongly Encapsulate JDK Internals", "final"),
    406: (17, "Pattern Matching for switch Preview", "preview"),
    407: (17, "Remove RMI Activation", "removed"),
    409: (17, "Sealed Classes", "final"),
    410: (17, "Remove Experimental AOT/JIT", "removed"),
    411: (17, "Deprecate Security Manager", "deprecated"),
    412: (17, "Foreign Function & Memory Incubator", "incubator"),
    414: (17, "Vector API 2nd Incubator", "incubator"),
    415: (17, "Context-Specific Deserialization Filters", "final"),
    # JDK 21
    430: (21, "String Templates Preview", "withdrawn"),
    431: (21, "Sequenced Collections", "final"),
    439: (21, "Generational ZGC", "final"),
    440: (21, "Record Patterns", "final"),
    441: (21, "Pattern Matching for switch", "final"),
    442: (21, "Foreign Function & Memory 3rd Preview", "preview"),
    443: (21, "Unnamed Patterns Preview", "preview"),
    444: (21, "Virtual Threads", "final"),
    445: (21, "Unnamed Classes Preview", "preview"),
    446: (21, "Scoped Values Preview", "preview"),
    448: (21, "Vector API 6th Incubator", "incubator"),
    449: (21, "Deprecate Windows 32-bit", "deprecated"),
    451: (21, "Prepare to Disallow Dynamic Agents", "final"),
    452: (21, "Key Encapsulation Mechanism API", "final"),
    453: (21, "Structured Concurrency Preview", "preview"),
    # JDK 22
    423: (22, "Region Pinning for G1", "final"),
    454: (22, "Foreign Function & Memory API", "final"),
    456: (22, "Unnamed Variables & Patterns", "final"),
    457: (22, "Class-File API Preview", "preview"),
    458: (22, "Launch Multi-File Source-Code", "final"),
    459: (22, "String Templates 2nd Preview", "withdrawn"),
    460: (22, "Vector API 7th Incubator", "incubator"),
    461: (22, "Stream Gatherers Preview", "preview"),
    462: (22, "Structured Concurrency 2nd Preview", "preview"),
    463: (22, "Implicitly Declared Classes 2nd Preview", "preview"),
    464: (22, "Scoped Values 2nd Preview", "preview"),
    # JDK 23
    455: (23, "Primitive Types in Patterns Preview", "preview"),
    466: (23, "Class-File API 2nd Preview", "preview"),
    467: (23, "Markdown Documentation Comments", "final"),
    469: (23, "Vector API 8th Incubator", "incubator"),
    471: (23, "Deprecate Memory-Access Methods in sun.misc.Unsafe", "deprecated"),
    473: (23, "Stream Gatherers 2nd Preview", "preview"),
    474: (23, "ZGC Generational Mode by Default", "final"),
    476: (23, "Module Import Declarations Preview", "preview"),
    477: (23, "Implicitly Declared Classes 3rd Preview", "preview"),
    480: (23, "Structured Concurrency 3rd Preview", "preview"),
    481: (23, "Scoped Values 3rd Preview", "preview"),
    482: (23, "Flexible Constructor Bodies 2nd Preview", "preview"),
    # JDK 24
    472: (24, "Prepare to Restrict JNI", "final"),
    475: (24, "Late Barrier Expansion for G1", "final"),
    478: (24, "Key Derivation Function API Preview", "preview"),
    483: (24, "Ahead-of-Time Class Loading", "final"),
    484: (24, "Class-File API", "final"),
    485: (24, "Stream Gatherers", "final"),
    486: (24, "Permanently Disable Security Manager", "final"),
    487: (24, "Scoped Values 4th Preview", "preview"),
    488: (24, "Primitive Types in Patterns 2nd Preview", "preview"),
    489: (24, "Vector API 9th Incubator", "incubator"),
    490: (24, "ZGC Remove Non-Generational Mode", "final"),
    491: (24, "Synchronize Virtual Threads without Pinning", "final"),
    492: (24, "Flexible Constructor Bodies 3rd Preview", "preview"),
    493: (24, "Linking Run-Time Images without JMODs", "final"),
    494: (24, "Module Import Declarations 2nd Preview", "preview"),
    495: (24, "Simple Source Files 2nd Preview", "preview"),
    496: (24, "Quantum-Resistant Module-Lattice-Based KEM", "final"),
    497: (24, "Quantum-Resistant Module-Lattice-Based Digital Signatures", "final"),
    498: (24, "Warn upon Use of Memory-Access Methods in sun.misc.Unsafe", "final"),
    499: (24, "Structured Concurrency 4th Preview", "preview"),
    501: (24, "Deprecate 32-bit x86 Port", "deprecated"),
    # JDK 25
    502: (25, "Stable Values Preview", "preview"),
    503: (25, "Remove 32-bit x86 Port", "removed"),
    506: (25, "Scoped Values", "final"),
    507: (25, "Primitive Types in Patterns 3rd Preview", "preview"),
    509: (25, "Compact Object Headers Experimental", "experimental"),
    510: (25, "Key Derivation Function API 2nd Preview", "preview"),
    511: (25, "Module Import Declarations", "final"),
    512: (25, "Compact Source Files", "final"),
    513: (25, "Flexible Constructor Bodies", "final"),
    514: (25, "AOT Command-Line Ergonomics", "final"),
    515: (25, "AOT Method Profiling", "final"),
    517: (25, "Structured Concurrency 5th Preview", "preview"),
    519: (25, "Compact Object Headers", "final"),
    # JDK 26
    401: (26, "Value Classes Preview", "preview"),
    404: (26, "Generational Shenandoah Experimental", "experimental"),
    416: (26, "Reimplement Core Reflection", "final"),
    516: (26, "AOT Cache", "final"),
    521: (26, "Generational Shenandoah", "final"),
    522: (26, "G1 Barrier Optimization", "final"),
    526: (26, "Lazy Static Final Fields Preview", "preview"),
    528: (26, "Stable Values 2nd Preview", "preview"),
    529: (26, "Vector API 11th Incubator", "incubator"),
    530: (26, "Primitive Types in Patterns 4th Preview", "preview"),
}

# ── Regex patterns ────────────────────────────────────────────────────────
# Match "JEP 123", "JEP-123", "[JEP 123]", links like "jep-123.md"
RE_JEP_REF = re.compile(
    r'(?:JEP[- ](\d{2,4}))'       # "JEP 123" or "JEP-123"
    r'|(?:jep-(\d{2,4})\.md)',     # "jep-123.md" file references
    re.IGNORECASE
)

# Match version context: "JDK 21", "(JDK 24)", "JDK21"
RE_JDK_VERSION = re.compile(r'JDK[- ]?(\d{1,2})', re.IGNORECASE)

# Match status indicators near a JEP reference
RE_STATUS = re.compile(
    r'(?:preview|预览|incubat|孵化|experiment|实验|final|正式|standard|标准'
    r'|withdrawn|撤回|deprecated|废弃|removed|移除)',
    re.IGNORECASE
)


def find_md_files(paths):
    """Find all .md files under given paths (or repo root)."""
    result = []
    for p in paths:
        if os.path.isfile(p) and p.endswith('.md'):
            result.append(p)
        elif os.path.isdir(p):
            for root, _dirs, files in os.walk(p):
                for f in files:
                    if f.endswith('.md'):
                        result.append(os.path.join(root, f))
    result.sort()
    return result


def extract_jep_refs(filepath):
    """Extract all JEP references from a file with line numbers and context."""
    refs = []
    with open(filepath, 'r', encoding='utf-8', errors='replace') as fh:
        for lineno, line in enumerate(fh, 1):
            for m in RE_JEP_REF.finditer(line):
                jep_num = int(m.group(1) or m.group(2))
                # Try to find JDK version on same line
                ver_match = RE_JDK_VERSION.search(line)
                jdk_ver = int(ver_match.group(1)) if ver_match else None
                # Try to detect status on same line
                status_match = RE_STATUS.search(line)
                status_text = status_match.group(0).lower() if status_match else None
                refs.append({
                    'file': filepath,
                    'line': lineno,
                    'jep': jep_num,
                    'jdk_version': jdk_ver,
                    'status_text': status_text,
                    'raw_line': line.rstrip(),
                })
    return refs


def normalize_status(text):
    """Map status text variants to canonical status."""
    if not text:
        return None
    t = text.lower()
    if t in ('preview', '预览'):
        return 'preview'
    if 'incubat' in t or '孵化' in t:
        return 'incubator'
    if 'experiment' in t or '实验' in t:
        return 'experimental'
    if t in ('final', '正式', 'standard', '标准'):
        return 'final'
    if t in ('withdrawn', '撤回'):
        return 'withdrawn'
    if t in ('deprecated', '废弃'):
        return 'deprecated'
    if t in ('removed', '移除'):
        return 'removed'
    return None


def validate_refs(refs, verbose=False):
    """Validate JEP references. Returns (errors, warnings, valid_count)."""
    errors = []
    warnings = []
    valid = 0

    for ref in refs:
        jep = ref['jep']
        fpath = ref['file']
        line = ref['line']
        short = os.path.relpath(fpath)

        if jep not in JEP_DB:
            errors.append(
                f"  {short}:{line}  JEP {jep} does not exist in known database"
            )
            continue

        db_ver, db_title, db_status = JEP_DB[jep]
        is_valid = True

        # Check version attribution
        if ref['jdk_version'] and ref['jdk_version'] != db_ver:
            errors.append(
                f"  {short}:{line}  JEP {jep} attributed to JDK {ref['jdk_version']}"
                f" (correct: JDK {db_ver} - {db_title})"
            )
            is_valid = False

        # Check status
        detected = normalize_status(ref['status_text'])
        if detected:
            if db_status == 'withdrawn' and detected == 'final':
                warnings.append(
                    f"  {short}:{line}  JEP {jep} marked as \"final\" but it was"
                    f" withdrawn ({db_title})"
                )
                is_valid = False
            elif db_status == 'withdrawn' and detected == 'preview':
                warnings.append(
                    f"  {short}:{line}  JEP {jep} marked as preview but it was"
                    f" withdrawn ({db_title})"
                )
                is_valid = False
            elif detected == 'final' and db_status in ('preview', 'incubator', 'experimental'):
                warnings.append(
                    f"  {short}:{line}  JEP {jep} marked as final but is"
                    f" {db_status} ({db_title})"
                )
                is_valid = False
            elif detected == 'preview' and db_status == 'final':
                warnings.append(
                    f"  {short}:{line}  JEP {jep} marked as preview but is"
                    f" final ({db_title})"
                )
                is_valid = False

        if is_valid:
            valid += 1

        if verbose and is_valid:
            print(f"  OK  {short}:{line}  JEP {jep} (JDK {db_ver}, {db_title})")

    return errors, warnings, valid


def apply_fixes(refs):
    """Auto-correct version attributions in files."""
    # Group fixes by file
    fixes_by_file = defaultdict(list)
    for ref in refs:
        jep = ref['jep']
        if jep not in JEP_DB:
            continue
        db_ver = JEP_DB[jep][0]
        if ref['jdk_version'] and ref['jdk_version'] != db_ver:
            fixes_by_file[ref['file']].append(ref)

    fixed_count = 0
    for filepath, file_refs in fixes_by_file.items():
        with open(filepath, 'r', encoding='utf-8', errors='replace') as fh:
            lines = fh.readlines()

        for ref in file_refs:
            idx = ref['line'] - 1
            old_line = lines[idx]
            wrong_ver = ref['jdk_version']
            correct_ver = JEP_DB[ref['jep']][0]
            # Replace the version near the JEP reference on this line
            # We target patterns like "JDK 22" -> "JDK 21"
            new_line = re.sub(
                rf'(JEP[- ]{ref["jep"]}\b.*?)JDK[- ]?{wrong_ver}\b',
                rf'\g<1>JDK {correct_ver}',
                old_line
            )
            if new_line == old_line:
                # Try reverse order: version before JEP
                new_line = re.sub(
                    rf'JDK[- ]?{wrong_ver}(\b.*?JEP[- ]{ref["jep"]})',
                    rf'JDK {correct_ver}\1',
                    old_line
                )
            if new_line != old_line:
                lines[idx] = new_line
                fixed_count += 1
                print(f"  FIXED {os.path.relpath(filepath)}:{ref['line']}"
                      f"  JDK {wrong_ver} -> JDK {correct_ver}"
                      f"  (JEP {ref['jep']})")

        with open(filepath, 'w', encoding='utf-8') as fh:
            fh.writelines(lines)

    return fixed_count


def main():
    parser = argparse.ArgumentParser(
        description='Validate JEP references in markdown files')
    parser.add_argument('paths', nargs='*', default=['.'],
                        help='Files or directories to scan (default: .)')
    parser.add_argument('--fix', action='store_true',
                        help='Auto-correct version attributions')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show valid references too')
    args = parser.parse_args()

    md_files = find_md_files(args.paths)
    if not md_files:
        print("No markdown files found.")
        return 0

    all_refs = []
    for f in md_files:
        all_refs.extend(extract_jep_refs(f))

    if not all_refs:
        print("No JEP references found in scanned files.")
        return 0

    # Deduplicate: same file+line+jep only counted once
    seen = set()
    unique_refs = []
    for ref in all_refs:
        key = (ref['file'], ref['line'], ref['jep'])
        if key not in seen:
            seen.add(key)
            unique_refs.append(ref)

    errors, warnings, valid = validate_refs(unique_refs, verbose=args.verbose)

    # Apply fixes if requested (before printing report)
    fixed = 0
    if args.fix and errors:
        print("\n--- Applying fixes ---")
        fixed = apply_fixes(unique_refs)
        print(f"--- {fixed} fix(es) applied ---\n")

    # Report
    total = len(unique_refs)
    issue_count = len(errors) + len(warnings)
    print("=== JEP Validation Report ===")
    print(f"Files scanned: {len(md_files)}")
    print(f"Total JEP references found: {total}")
    print(f"Known JEPs in database: {len(JEP_DB)}")
    print(f"Valid references: {valid}")
    print(f"Issues found: {issue_count}")

    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for e in errors:
            print(e)

    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for w in warnings:
            print(w)

    if not errors and not warnings:
        print("\nAll JEP references are valid.")

    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
