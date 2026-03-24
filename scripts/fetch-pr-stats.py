#!/usr/bin/env python3
"""
Fetch PR stats (changed_files, additions, deletions) for a repository.
Uses GitHub API: GET /repos/{owner}/{repo}/pulls/{pr_number}

Usage:
  python3 fetch-pr-stats.py <repo> [--limit N]

Examples:
  python3 fetch-pr-stats.py openjdk/valhalla
  python3 fetch-pr-stats.py openjdk/jdk --limit 1000
"""

import csv, json, os, sys, time, urllib.request, urllib.error

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEADERS = {"Accept": "application/vnd.github.v3+json", "User-Agent": "jdk-internal/1.0"}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def api_get(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                remaining = int(resp.headers.get("X-RateLimit-Remaining", 100))
                reset = int(resp.headers.get("X-RateLimit-Reset", 0))
                if remaining < 5:
                    wait = max(reset - int(time.time()), 1) + 2
                    print(f"  Rate limit low ({remaining}), waiting {wait}s...")
                    time.sleep(wait)
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 403:
                reset = int(e.headers.get("X-RateLimit-Reset", 0))
                wait = max(reset - int(time.time()), 1) + 5
                print(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
            elif e.code == 404:
                return None
            else:
                if attempt < retries - 1:
                    time.sleep(2 ** (attempt + 1))
                else:
                    return None
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** (attempt + 1))
            else:
                return None
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fetch-pr-stats.py <repo> [--limit N]")
        sys.exit(1)

    repo = sys.argv[1]
    limit = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[2] == "--limit" else 0
    repo_short = repo.split("/")[1]
    csv_path = os.path.join(BASE_DIR, repo_short, "all-integrated-prs.csv")
    cache_path = os.path.join(BASE_DIR, repo_short, ".pr-stats-cache.json")

    if not os.path.exists(csv_path):
        print(f"CSV not found: {csv_path}")
        sys.exit(1)

    # Load cache
    cache = {}
    if os.path.exists(cache_path):
        with open(cache_path) as f:
            cache = json.load(f)
        print(f"Loaded cache: {len(cache)} PRs")

    # Read CSV to get PR numbers
    rows = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames)
        for row in reader:
            rows.append(row)

    pr_numbers = [r["pr_number"] for r in rows if r.get("pr_number")]
    need_fetch = [p for p in pr_numbers if p not in cache]

    if limit:
        need_fetch = need_fetch[:limit]

    print(f"Total PRs: {len(pr_numbers)}, cached: {len(cache)}, to fetch: {len(need_fetch)}")

    # Fetch PR stats
    fetched = 0
    for i, pr_num in enumerate(need_fetch):
        url = f"https://api.github.com/repos/{repo}/pulls/{pr_num}"
        data = api_get(url)
        if data:
            cache[pr_num] = {
                "changed_files": data.get("changed_files", 0),
                "additions": data.get("additions", 0),
                "deletions": data.get("deletions", 0),
            }
            fetched += 1
        else:
            cache[pr_num] = {"changed_files": 0, "additions": 0, "deletions": 0}

        if (i + 1) % 50 == 0:
            print(f"  Fetched {i+1}/{len(need_fetch)} ({fetched} successful)")
            # Save cache periodically
            with open(cache_path, "w") as f:
                json.dump(cache, f)

        time.sleep(0.3)

    # Save final cache
    with open(cache_path, "w") as f:
        json.dump(cache, f)
    print(f"Cache saved: {len(cache)} PRs")

    # Update CSV
    for field in ["changed_files", "additions", "deletions"]:
        if field not in fields:
            fields.append(field)

    for row in rows:
        pr_num = row.get("pr_number", "")
        if pr_num in cache:
            stats = cache[pr_num]
            row["changed_files"] = str(stats.get("changed_files", ""))
            row["additions"] = str(stats.get("additions", ""))
            row["deletions"] = str(stats.get("deletions", ""))

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV updated: {csv_path}")

    # Print summary
    files_list = [int(cache[p]["changed_files"]) for p in pr_numbers if p in cache and cache[p].get("changed_files")]
    if files_list:
        print(f"\nStats: avg={sum(files_list)/len(files_list):.1f} files, "
              f"median={sorted(files_list)[len(files_list)//2]}, "
              f"max={max(files_list)}")


if __name__ == "__main__":
    main()
