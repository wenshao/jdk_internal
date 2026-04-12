#!/usr/bin/env python3
"""
Fetch all integrated PRs from any openjdk/* repository.
Uses GitHub Issues Search API with date-range splitting to handle >1000 results.

Usage:
  python3 fetch-repo-prs.py <repo>

Examples:
  python3 fetch-repo-prs.py openjdk/valhalla
  python3 fetch-repo-prs.py openjdk/jdk21u-dev
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
import csv
from datetime import datetime, timedelta

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "jdk-internal-collector/1.0"
}
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
                if remaining < 3:
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
            elif e.code == 422:
                print(f"  422 Unprocessable: {url}")
                return None
            else:
                print(f"  HTTP {e.code}")
                if attempt < retries - 1:
                    time.sleep(2 ** (attempt + 1))
                else:
                    return None
        except Exception as e:
            print(f"  Error: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** (attempt + 1))
            else:
                return None
    return None


def search_prs(repo, date_from, date_to):
    """Search integrated PRs in date range. Returns (items, count) or (None, count) if >1000."""
    query = f"repo:{repo}+is:pr+is:closed+label:integrated+created:{date_from}..{date_to}"
    url = f"https://api.github.com/search/issues?q={query}&per_page=100&sort=created&order=asc"

    all_items = []
    page = 1

    while True:
        data = api_get(f"{url}&page={page}")
        if not data or "items" not in data:
            break

        total = data.get("total_count", 0)
        items = data["items"]
        all_items.extend(items)

        if page == 1 and total > 1000:
            return None, total

        if len(items) < 100:
            break

        page += 1
        if page > 10:
            break
        time.sleep(0.5)

    return all_items, len(all_items)


def split_range(date_from_str, date_to_str, parts=2):
    """Split a date range into equal parts."""
    d_from = datetime.strptime(date_from_str, "%Y-%m-%d")
    d_to = datetime.strptime(date_to_str, "%Y-%m-%d")
    total_days = (d_to - d_from).days
    chunk = max(total_days // parts, 1)

    ranges = []
    current = d_from
    while current <= d_to:
        end = min(current + timedelta(days=chunk), d_to)
        ranges.append((current.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")))
        current = end + timedelta(days=1)
    return ranges


def fetch_range(repo, date_from, date_to, all_prs, depth=0):
    """Recursively fetch PRs, splitting ranges if >1000 results."""
    prefix = "  " * depth
    print(f"{prefix}Fetching {date_from} to {date_to}...")

    items, count = search_prs(repo, date_from, date_to)

    if items is None:
        # Too many results, split
        print(f"{prefix}  Too many ({count}), splitting...")
        sub_ranges = split_range(date_from, date_to, parts=3)
        for sf, st in sub_ranges:
            fetch_range(repo, sf, st, all_prs, depth + 1)
            time.sleep(0.5)
    elif items:
        new = 0
        for item in items:
            pr_num = str(item["number"])
            if pr_num not in all_prs:
                all_prs[pr_num] = item
                new += 1
        print(f"{prefix}  Found {count} ({new} new), total: {len(all_prs)}")
    else:
        print(f"{prefix}  No PRs")


def generate_date_ranges(start_year=2019, end_year=2026):
    """Generate quarterly date ranges."""
    ranges = []
    for year in range(start_year, end_year + 1):
        for q_start, q_end in [("01-01", "03-31"), ("04-01", "06-30"), ("07-01", "09-30"), ("10-01", "12-31")]:
            d_from = f"{year}-{q_start}"
            d_to = f"{year}-{q_end}"
            if datetime.strptime(d_to, "%Y-%m-%d") <= datetime.now():
                ranges.append((d_from, d_to))
            else:
                # Current or future quarter - use today as end
                ranges.append((d_from, datetime.now().strftime("%Y-%m-%d")))
                return ranges
    return ranges


def extract_bug_id(title):
    m = re.match(r'^(\d{7,8})\s*[:\-\s]', title)
    if m:
        return m.group(1)
    m = re.match(r'^JDK-(\d{7,8})', title)
    if m:
        return m.group(1)
    return ""


def write_csv(repo, all_prs):
    """Write CSV output."""
    repo_short = repo.split("/")[1]  # e.g., "valhalla", "jdk21u-dev"
    output_dir = os.path.join(BASE_DIR, repo_short)
    os.makedirs(output_dir, exist_ok=True)

    csv_path = os.path.join(output_dir, "all-integrated-prs.csv")
    cache_path = os.path.join(output_dir, ".pr-cache.json")

    # Save cache
    with open(cache_path, "w") as f:
        json.dump(all_prs, f)

    # Build rows
    rows = []
    for pr_num, item in all_prs.items():
        title = item.get("title", "")
        bug_id = extract_bug_id(title)
        user = item.get("user", {})
        author = user.get("login", "") if isinstance(user, dict) else ""
        created = item.get("created_at", "")[:10]
        closed = item.get("closed_at", "")[:10] if item.get("closed_at") else ""

        labels = []
        if isinstance(item.get("labels"), list):
            labels = [l.get("name", "") for l in item["labels"] if isinstance(l, dict)]

        rows.append({
            "bug_id": bug_id,
            "pr_number": pr_num,
            "title": title,
            "author": author,
            "created": created,
            "closed": closed,
            "labels": "|".join(labels),
        })

    rows.sort(key=lambda x: int(x["pr_number"]))

    fieldnames = ["bug_id", "pr_number", "title", "author", "created", "closed", "labels"]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n{'='*60}")
    print(f"CSV: {csv_path}")
    print(f"Total: {len(rows)} PRs")

    # Stats
    authors = {}
    for r in rows:
        a = r["author"]
        authors[a] = authors.get(a, 0) + 1

    print(f"\nTop 15 contributors:")
    for author, count in sorted(authors.items(), key=lambda x: -x[1])[:15]:
        print(f"  {author}: {count}")

    years = {}
    for r in rows:
        y = r["created"][:4] if r["created"] else "?"
        years[y] = years.get(y, 0) + 1

    print(f"\nYear distribution:")
    for y in sorted(years.keys()):
        print(f"  {y}: {years[y]}")

    return csv_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fetch-repo-prs.py <repo>")
        print("Example: python3 fetch-repo-prs.py openjdk/valhalla")
        sys.exit(1)

    repo = sys.argv[1]

    # Determine start year based on repo
    start_year = 2019
    if "8u" in repo:
        start_year = 2019
    elif "11u" in repo:
        start_year = 2019
    elif "17u" in repo:
        start_year = 2021
    elif "21u" in repo:
        start_year = 2023
    elif "25u" in repo:
        start_year = 2025
    elif "valhalla" in repo:
        start_year = 2019

    print(f"=== Fetching integrated PRs from {repo} ===")
    print(f"Start year: {start_year}")
    print()

    # Load existing cache
    repo_short = repo.split("/")[1]
    cache_path = os.path.join(BASE_DIR, repo_short, ".pr-cache.json")
    all_prs = {}
    if os.path.exists(cache_path):
        with open(cache_path, "r") as f:
            all_prs = json.load(f)
        print(f"Loaded cache: {len(all_prs)} PRs")

    # Fetch
    date_ranges = generate_date_ranges(start_year)
    for d_from, d_to in date_ranges:
        fetch_range(repo, d_from, d_to, all_prs)
        time.sleep(0.5)

    # Write
    csv_path = write_csv(repo, all_prs)
    print(f"\nDone! {len(all_prs)} PRs saved.")


if __name__ == "__main__":
    main()
