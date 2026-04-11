# PR Archive Fetch Status

> Last updated: 2026-04-12

## Current Progress

| Data Source | Cached | Total | Coverage |
|------------|--------|-------|----------|
| **Main repo PRs** | 26,407 | 26,407 | **100%** |
| **JBS metadata** | ~23,100 | ~26,407 | **~87%** |
| **Reviewers** | ~25,468 | ~26,407 | **~96%** |

## Completed Fetches (2026-04-12)

| Repository | Before | After | New PRs |
|-----------|--------|-------|---------|
| `openjdk/jdk` (main) | 24,868 | 26,407 | **+1,539** |
| `openjdk/jdk25u-dev` | 341 | 389 | +48 |
| `openjdk/jdk24u` | 181 | 181 | 0 (EOL) |
| `openjdk/jdk21u-dev` | 2,486 | 2,575 | +89 |
| `openjdk/jdk17u-dev` | 4,000 | 4,043 | +43 |
| `openjdk/jdk11u-dev` | 2,771 | 2,783 | +12 |
| `openjdk/jdk8u-dev` | 601 | 608 | +7 |

## How to Resume

```bash
# Fetch new PRs for main repo
GITHUB_TOKEN=$(gh auth token) python3 scripts/fetch-repo-prs.py openjdk/jdk

# Merge new PRs into enriched CSV
python3 scripts/merge-new-prs.py

# Enrich with JBS and reviewer data
python3 scripts/fetch-jbs-data.py --limit 5000 --delay 0.3 --apply
python3 scripts/fetch-reviewers.py --limit 5000 --apply
```

## Fetch History

| Date | Event | Notes |
|------|-------|-------|
| 2026-03-23 | Initial JBS/Reviewer fetch | 4 batches |
| 2026-03-24 ~ 2026-04-02 | JBS/Reviewer completion | Coverage reached 100% for 24,868 PRs |
| 2026-04-12 | Full data refresh | +1,539 main PRs, 7 sub-repos updated |
| 2026-04-12 | JBS/Reviewer enrichment | In progress for new PRs |
