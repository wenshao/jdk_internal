#!/usr/bin/env python3
"""
Auto-refresh all analysis reports from all-integrated-prs.csv.
Run this after updating the CSV to regenerate all stats.

Usage: python3 scripts/refresh-all-reports.py
"""
import subprocess, sys, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
os.chdir(ROOT_DIR)

# The report generation logic is embedded in this commit's generation script
# For now, just re-run the inline generation
print("To refresh all reports, re-run the generation commands from the commit.")
print("This script will be expanded to be fully self-contained.")
print()
print("Quick manual refresh:")
print("  1. Update CSV: python3 scripts/fetch-jbs-data.py --limit 0 --apply")
print("  2. Update CSV: python3 scripts/fetch-reviewers.py --limit 0 --apply")
print("  3. Regenerate reports: (run the generation code)")
print()
print("Reports that will be regenerated:")
reports = [
    'contributors/stats/cross-org-collaboration.md',
    'contributors/stats/module-ownership.md',
    'contributors/stats/review-efficiency.md',
    'contributors/stats/trends.md',
    'contributors/stats/china-contributions.md',
    'contributors/stats/rising-stars.md',
    'contributors/stats/pr-type-distribution.md',
    'contributors/stats/reviewer-workload.md',
    'contributors/stats/contributor-retention.md',
    'contributors/stats/jep-tracking.md',
    'contributors/stats/module-evolution.md',
]
for r in reports:
    exists = '✅' if os.path.exists(r) else '❌'
    print(f"  {exists} {r}")

# Per-version
for v in range(16, 27):
    path = f'by-version/jdk{v}/contributions.md'
    exists = '✅' if os.path.exists(path) else '❌'
    print(f"  {exists} {path}")
