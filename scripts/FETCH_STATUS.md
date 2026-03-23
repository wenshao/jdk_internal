# PR Archive Fetch Status

> Last updated: 2026-03-23 09:53 UTC

## Current Progress

| Data Source | Cached | Total Needed | Coverage | Status |
|------------|--------|-------------|----------|--------|
| **JBS (priority/component)** | 3,938 | ~22,800 | 17% | Running |
| **GitHub Reviewers** | 8,533 | ~24,800 | 34% | Running |
| **GitHub PR Details** | 0 | ~24,800 | 0% | Not started |

## How to Resume

```bash
# Continue JBS fetch (incremental, picks up from cache)
python3 scripts/fetch-jbs-data.py --limit 5000 --delay 1.0 --apply

# Continue reviewer fetch (uses GitHub Core API, 5000/hr)
python3 scripts/fetch-reviewers.py --limit 4500 --apply

# Apply cached data to CSV without new fetching
python3 scripts/fetch-jbs-data.py --limit 0 --apply
python3 scripts/fetch-reviewers.py --limit 0 --apply
```

## Rate Limits

| API | Limit | Best Practice |
|-----|-------|---------------|
| JBS (bugs.openjdk.org) | ~30 req/min effective | `--delay 1.0` to avoid timeout |
| GitHub Core API | 5,000/hr | reviewer + PR details share this |

## Estimated Remaining Time

| Data | Remaining | Rate | Est. Time |
|------|-----------|------|-----------|
| JBS | ~18,862 | ~30/min | ~628 min (10.0 hr) |
| Reviewers | ~16,267 | ~50/min | ~325 min (5.0 hr) |

## Fetch History

| Date | Action | JBS | Reviewers |
|------|--------|-----|-----------|
| 2026-03-23 | Initial fetch | 300 | 4,500 |
| 2026-03-23 | Batch 2 | 3,538 | 7,933 |
| 2026-03-23 | Batch 3 (running) | 3,938 | 8,533 |
