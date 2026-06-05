# PR Archive Fetch Status

> Last updated: 2026-06-06

## Current Progress

| Data Source | Cached | Total | Coverage |
|------------|--------|-------|----------|
| **Main repo PRs** | 27,054 | 27,054 | **100%** |
| **JBS metadata** | 26,535 | 27,054 | **~98%** |
| **Reviewers** | 27,054 | 27,054 | **100%** |

## Completed Fetches (2026-06-06)

| Repository | Before | After | New PRs |
|-----------|--------|-------|---------|
| `openjdk/jdk` (main) | 26,407 | 27,054 | **+647** |
| `openjdk/jdk25u-dev` | 389 | 498 | +109 |
| `openjdk/jdk17u-dev` | 4,043 | 4,164 | +121 |
| `openjdk/jdk21u-dev` | 2,575 | 2,671 | +96 |
| `openjdk/jdk11u-dev` | 2,783 | 2,812 | +28 |
| `openjdk/jdk8u-dev` | 608 | 609 | +1 |

> New main PRs by JDK version: 583× JDK 27, 58× JDK 26, 5× JDK 25, 1× JDK 24.
> JBS + reviewer enrichment: 642 JBS / 647 reviewers fetched, 0 failures.
> All-repo grand total: **46,162** integrated PRs.

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
export GITHUB_TOKEN=$(gh auth token)

# 1. Fetch new PRs (main + sub-repos; cache makes it incremental)
python3 scripts/fetch-repo-prs.py openjdk/jdk
for r in jdk25u-dev jdk21u-dev jdk17u-dev jdk11u-dev jdk8u-dev; do
  python3 scripts/fetch-repo-prs.py "openjdk/$r"
done

# 2. Enrich sub-repo CSVs (org/country/review_days for new PRs)
python3 scripts/enrich-subrepo-csvs.py

# 3. Merge new main-repo PRs into the enriched CSV
python3 scripts/merge-new-prs.py

# 4. Enrich with JBS + reviewer data
python3 scripts/fetch-jbs-data.py --limit 5000 --delay 0.25 --apply
python3 scripts/fetch-reviewers.py --limit 5000 --apply

# 5. Regenerate reports
python3 scripts/generate-stats-reports.py
python3 scripts/generate-version-contributions.py
python3 scripts/verify-links.py
```

## Fetch History

| Date | Event | Notes |
|------|-------|-------|
| 2026-03-23 | Initial JBS/Reviewer fetch | 4 batches |
| 2026-03-24 ~ 2026-04-02 | JBS/Reviewer completion | Coverage reached 100% for 24,868 PRs |
| 2026-04-12 | Full data refresh | +1,539 main PRs, 7 sub-repos updated |
| 2026-06-06 | Full data refresh | +647 main PRs (583× JDK 27), 5 sub-repos updated |
| 2026-06-06 | JBS/Reviewer enrichment | 642 JBS + 647 reviewers, 0 failures; new enrich-subrepo-csvs.py |
