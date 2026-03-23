# PR Archive Fetch Status

> Last updated: 2026-03-23 10:52 UTC

## Current Progress

| Data Source | Cached | Total | Coverage | Status |
|------------|--------|-------|----------|--------|
| **JBS** | 5,638 | ~22,800 | **24%** | Incremental |
| **Reviewers** | 11,733 | ~24,800 | **47%** | Incremental |

## How to Resume

```bash
python3 scripts/fetch-jbs-data.py --limit 5000 --delay 1.0 --apply
python3 scripts/fetch-reviewers.py --limit 4500 --apply
```

## Fetch History

| Date | JBS | Reviewers | Note |
|------|-----|-----------|------|
| 2026-03-23 | 300 | 4,500 | Initial |
| 2026-03-23 | 3,538 | 7,933 | Batch 2 |
| 2026-03-23 | 5,638 | 11,733 | Batch 3 |
