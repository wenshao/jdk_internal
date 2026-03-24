#!/usr/bin/env python3
"""
Fetch CFV (Call for Votes) data from jdk-dev mailing list archives.
Extracts nominations AND vote replies for comprehensive promotion tracking.

Strategy: Use subject.html to find all CFV-related emails, group by candidate.
The FIRST email in each group is the nomination, subsequent emails are vote replies.
Pipermail strips "Re:" from the subject index, so all emails in a thread look identical.
"""

import csv
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from collections import defaultdict, OrderedDict

BASE_URL = "https://mail.openjdk.org/pipermail/jdk-dev"
OUTPUT_CSV = "/root/git/jdk_internal/scripts/.cfv-votes.csv"
CACHE_FILE = "/root/git/jdk_internal/scripts/.cfv-cache.json"
REPORT_FILE = "/root/git/jdk_internal/contributors/stats/role-promotions.md"

REQUEST_DELAY = 0.25

MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


def fetch_url(url, retries=3):
    """Fetch URL content with retries and rate limiting."""
    for attempt in range(retries):
        try:
            time.sleep(REQUEST_DELAY)
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; JDK-Internal-Research/1.0)'
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode('utf-8', errors='replace')
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            print(f"  WARN: Failed to fetch {url}: {e}", file=sys.stderr)
            return None
    return None


def extract_email_info(html):
    """Extract sender, date, subject, and body from a pipermail email page."""
    if not html:
        return None
    info = {}

    m = re.search(r'<H1>(.*?)</H1>', html, re.DOTALL | re.IGNORECASE)
    info['subject'] = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else ""

    author_match = re.search(r'<B>(.*?)</B>', html)
    if author_match:
        info['sender'] = re.sub(r'<[^>]+>', '', author_match.group(1)).strip()
    else:
        info['sender'] = ""

    date_match = re.search(r'<I>(.*?)</I>', html)
    info['date'] = date_match.group(1).strip() if date_match else ""

    pre_match = re.search(r'<PRE>(.*?)</PRE>', html, re.DOTALL | re.IGNORECASE)
    if pre_match:
        body = pre_match.group(1)
        body = re.sub(r'<[^>]+>', '', body)
        body = body.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
        body = body.replace('&#39;', "'").replace('&quot;', '"')
        info['body'] = body
    else:
        info['body'] = ""

    return info


def parse_date(date_str):
    """Parse pipermail date string to YYYY-MM-DD."""
    if not date_str:
        return ""
    for fmt in [
        '%a %b %d %H:%M:%S %Z %Y',
        '%a, %d %b %Y %H:%M:%S %z',
        '%a %b %d %H:%M:%S %Y',
    ]:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            continue
    return ""


def clean_name(name):
    """Clean a sender name."""
    if not name:
        return ""
    name = re.sub(r'\s*<[^>]+>\s*', '', name)
    name = re.sub(r'\s+at\s+\S+', '', name)
    name = re.sub(r'\([^)]*\)', '', name)
    name = re.sub(r'\s*\S+@\S+', '', name)
    name = name.strip().strip('"').strip("'").strip()
    name = re.sub(r'^\[External\]\s*:?\s*', '', name)
    # Decode HTML entities
    name = name.replace('&#39;', "'").replace('&amp;', '&')
    name = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), name)
    return name


def parse_cfv_subject(subject):
    """Parse a CFV subject line. Returns (candidate, role, project) or None."""
    clean_subj = re.sub(r'^(?:(?:Re|Fwd|FW)\s*:\s*)+', '', subject, flags=re.IGNORECASE)
    clean_subj = re.sub(r'^\[External\]\s*:?\s*', '', clean_subj)
    clean_subj = re.sub(r'^(?:(?:Re|Fwd|FW)\s*:\s*)+', '', clean_subj, flags=re.IGNORECASE)
    clean_subj = clean_subj.strip()

    m = re.match(
        r'CFV\s*:\s*New\s+(.+?)\s+(Committer|Reviewer|Author|Member)\s*:\s*(.+)',
        clean_subj, re.IGNORECASE
    )
    if m:
        project = m.group(1).strip()
        role = m.group(2).strip().title()
        candidate = m.group(3).strip()
        candidate = re.sub(r'\s*\(.*?\)\s*$', '', candidate)
        candidate = candidate.rstrip('.')
        return candidate, role, project
    return None


def is_yes_vote(body):
    """Check if email body contains a yes vote."""
    if not body:
        return False
    # Check first ~15 lines (votes are usually at top, before quoted text)
    lines = body.split('\n')
    # Find where quoted text starts
    check_lines = []
    for line in lines[:20]:
        if line.strip().startswith('>'):
            break
        check_lines.append(line)

    text = '\n'.join(check_lines)

    patterns = [
        r'(?i)\bvote\s*:\s*yes\b',
        r'(?i)\bvote\s*:\s*\+\s*1\b',
        r'(?i)^\s*yes\s*[.!]?\s*$',
        r'(?i)^\s*\+1\s*[.!]?\s*$',
        r'(?i)\bvote\s+yes\b',
        r'(?i)^\s*vote:\s*yes',
    ]
    for pat in patterns:
        if re.search(pat, text, re.MULTILINE):
            return True
    return False


def is_nomination_email(body):
    """Check if this is the initial nomination email (not a vote reply)."""
    if not body:
        return False
    # Nomination emails are typically longer and contain specific phrases
    indicators = [
        r'(?i)I\s+(?:hereby\s+)?nominate',
        r'(?i)I\s+would\s+like\s+to\s+nominate',
        r'(?i)hereby\s+nominated',
        r'(?i)call\s+for\s+vote',
        r'(?i)voting\s+(?:period|deadline)',
        r'(?i)OpenJDK\s+Census',
        r'(?i)contributions?\s+(?:include|are)',
        r'(?i)commit[s]?\s+to\s+(?:the\s+)?(?:JDK|jdk)',
    ]
    score = 0
    for pat in indicators:
        if re.search(pat, body):
            score += 1
    return score >= 2 or len(body) > 500


def parse_cfv_body(body):
    """Extract stats and areas from a CFV nomination email body."""
    if not body:
        return "", ""

    found_stats = []
    stat_patterns = [
        (r'(\d+)\s+(?:direct\s+)?commits?\b', 'commits'),
        (r'(\d+)\s+(?:JBS\s+)?issues?\b', 'issues'),
        (r'(\d+)\s+contributions?\b', 'contributions'),
        (r'(\d+)\s+changes?\b', 'changes'),
        (r'(\d+)\s+(?:PRs?|pull\s+requests?)\b', 'PRs'),
        (r'(\d+)\s+reviews?\b', 'reviews'),
    ]
    for pat, label in stat_patterns:
        m = re.search(pat, body, re.IGNORECASE)
        if m:
            found_stats.append(f"{m.group(1)} {label}")
    stats = "; ".join(found_stats[:4])

    areas = ""
    area_match = re.search(r'(?:area|work|focus|contribution)[s]?\s*(?:include|:)\s*([^\n]+)', body, re.IGNORECASE)
    if area_match:
        areas = area_match.group(1).strip()[:200]
    else:
        bullets = re.findall(r'[-*]\s+(\S[^\n]{5,80})', body)
        if bullets:
            areas = "; ".join(b.strip() for b in bullets[:4])

    return stats, areas


def find_cfv_groups_in_subject_page(html, month_url):
    """Parse subject.html to find all CFV email links grouped by candidate.

    Pipermail's subject index strips "Re:" and lists all emails in a thread
    with identical subjects. We group by parsed candidate name and treat
    the first URL as the nomination, rest as potential vote replies.
    """
    if not html:
        return {}

    # Find all links on the page with their numeric href
    # Pattern handles multiline: <A HREF="NNNN.html">subject text\n</A>
    all_links = []
    for m in re.finditer(r'<LI><A\s+HREF="(\d+\.html)"[^>]*>(.*?)</A>', html, re.IGNORECASE | re.DOTALL):
        href = m.group(1)
        text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        text = re.sub(r'\s+', ' ', text)  # normalize whitespace
        all_links.append((href, text))

    # Filter for CFV emails and group by candidate
    groups = OrderedDict()  # candidate_key -> {urls: [...], subject: str, ...}

    for href, text in all_links:
        # Check for CFV in subject
        if 'CFV' not in text.upper():
            continue
        # Skip Result emails
        if re.search(r'\bResult\b', text, re.IGNORECASE):
            continue
        # Skip CORRECTION emails
        if re.search(r'\bCORRECTION\b', text, re.IGNORECASE):
            continue

        parsed = parse_cfv_subject(text)
        if not parsed:
            continue

        candidate, role, project = parsed
        # Normalize key: use decoded candidate name
        candidate_decoded = candidate.replace('&#241;', 'n').replace('&#246;', 'o').replace('&#233;', 'e')
        key = f"{candidate_decoded}|{role}|{project}"

        url = f"{month_url}/{href}"
        if key not in groups:
            groups[key] = {
                'urls': [],
                'subject': text,
                'candidate': candidate,
                'role': role,
                'project': project,
            }
        groups[key]['urls'].append(url)

    return groups


def process_month(year, month_name):
    """Process a single month's archive for CFV threads."""
    month_url = f"{BASE_URL}/{year}-{month_name}"
    subject_url = f"{month_url}/subject.html"

    print(f"Fetching {year}-{month_name}...", flush=True)
    subject_html = fetch_url(subject_url)
    if not subject_html:
        return []

    groups = find_cfv_groups_in_subject_page(subject_html, month_url)
    if not groups:
        print(f"  No CFV threads", flush=True)
        return []

    print(f"  Found {len(groups)} CFV nomination(s)", flush=True)
    results = []

    for key, group in groups.items():
        candidate = group['candidate']
        role = group['role']
        project = group['project']
        urls = group['urls']

        print(f"  {candidate} ({role}): {len(urls)} emails...", end='', flush=True)

        # Fetch first email (likely the nomination)
        first_url = urls[0]
        first_html = fetch_url(first_url)
        first_info = extract_email_info(first_html)

        nominator = ""
        date_str = ""
        stats = ""
        areas = ""
        initial_url = first_url

        if first_info:
            # Check if this is actually the nomination
            if is_nomination_email(first_info.get('body', '')) or len(urls) == 1:
                nominator = clean_name(first_info.get('sender', ''))
                date_str = parse_date(first_info.get('date', ''))
                stats, areas = parse_cfv_body(first_info.get('body', ''))
            else:
                # First email might be a vote - find the nomination
                nominator = clean_name(first_info.get('sender', ''))
                date_str = parse_date(first_info.get('date', ''))

        # Collect voters from remaining emails
        voters = []
        nominator_clean = nominator  # Don't count nominator as a voter

        # If there's only 1 URL, it's just the nomination with no replies
        if len(urls) > 1:
            for reply_url in urls[1:]:
                reply_html = fetch_url(reply_url)
                reply_info = extract_email_info(reply_html)
                if not reply_info:
                    continue

                body = reply_info.get('body', '')
                sender = clean_name(reply_info.get('sender', ''))

                # Check if this is actually the nomination (sometimes sort order differs)
                if not nominator and is_nomination_email(body):
                    nominator = sender
                    date_str = parse_date(reply_info.get('date', ''))
                    stats, areas = parse_cfv_body(body)
                    initial_url = reply_url
                    continue

                # Check for yes vote
                if is_yes_vote(body):
                    if sender and sender not in voters and sender != nominator_clean:
                        voters.append(sender)

        # If first email wasn't identified as nomination but we found one later,
        # re-check the first email as a potential vote
        if nominator != clean_name(first_info.get('sender', '') if first_info else ''):
            if first_info and is_yes_vote(first_info.get('body', '')):
                voter = clean_name(first_info.get('sender', ''))
                if voter and voter not in voters and voter != nominator:
                    voters.insert(0, voter)

        print(f" {len(voters)} votes", flush=True)

        # Decode HTML entities in candidate name
        candidate_clean = candidate.replace('&#241;', '\u00f1').replace('&#246;', '\u00f6').replace('&#233;', '\u00e9')
        candidate_clean = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), candidate_clean)

        results.append({
            'date': date_str,
            'candidate': candidate_clean,
            'role': role,
            'project': project,
            'nominator': nominator,
            'stats': stats,
            'areas': areas,
            'voters': "; ".join(voters),
            'vote_count': len(voters),
            'url': initial_url,
        })

    return results


def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {'months_done': [], 'entries': []}


def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)


def write_csv(entries):
    entries.sort(key=lambda x: x.get('date', ''), reverse=True)
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'date', 'candidate_name', 'role', 'project', 'nominator',
            'stats', 'areas', 'voters', 'vote_count', 'url'
        ])
        writer.writeheader()
        for entry in entries:
            writer.writerow({
                'date': entry.get('date', ''),
                'candidate_name': entry.get('candidate', ''),
                'role': entry.get('role', ''),
                'project': entry.get('project', ''),
                'nominator': entry.get('nominator', ''),
                'stats': entry.get('stats', ''),
                'areas': entry.get('areas', ''),
                'voters': entry.get('voters', ''),
                'vote_count': entry.get('vote_count', 0),
                'url': entry.get('url', ''),
            })
    print(f"\nWrote {len(entries)} entries to {OUTPUT_CSV}", flush=True)


def generate_report(entries):
    """Generate the role-promotions.md report."""
    if not entries:
        return

    entries.sort(key=lambda x: x.get('date', ''), reverse=True)

    voter_counts = defaultdict(int)
    voter_for = defaultdict(list)
    candidate_voters = defaultdict(list)

    for entry in entries:
        voters_str = entry.get('voters', '')
        candidate = entry.get('candidate', '')
        if voters_str:
            for voter in voters_str.split('; '):
                voter = voter.strip()
                if voter:
                    voter_counts[voter] += 1
                    voter_for[voter].append(candidate)
                    candidate_voters[candidate].append(voter)

    role_counts = defaultdict(int)
    by_year = defaultdict(lambda: defaultdict(int))
    by_project = defaultdict(int)
    nominators_count = defaultdict(int)

    for entry in entries:
        role = entry.get('role', 'Unknown')
        role_counts[role] += 1
        year = entry.get('date', '')[:4]
        if year:
            by_year[year][role] += 1
        project = entry.get('project', 'Unknown')
        by_project[project] += 1
        nominator = entry.get('nominator', '')
        if nominator:
            nominators_count[nominator] += 1

    lines = []
    lines.append("# OpenJDK Role Promotions (CFV Analysis)")
    lines.append("")
    lines.append(f"> **Data source:** [jdk-dev mailing list](https://mail.openjdk.org/pipermail/jdk-dev/) CFV threads")
    lines.append(f"> **Period:** 2020-01 to 2026-03 | **Last updated:** {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"> **Total promotions tracked:** {len(entries)} | **Unique voters identified:** {len(voter_counts)}")
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append("| Role | Count |")
    lines.append("|------|-------|")
    for role in ['Reviewer', 'Committer', 'Author', 'Member']:
        if role_counts.get(role, 0) > 0:
            lines.append(f"| {role} | {role_counts[role]} |")
    lines.append(f"| **Total** | **{len(entries)}** |")
    lines.append("")

    # Year-over-year
    lines.append("## Promotions by Year")
    lines.append("")
    years_sorted = sorted(by_year.keys(), reverse=True)
    roles_present = [r for r in ['Reviewer', 'Committer', 'Author', 'Member'] if role_counts.get(r, 0) > 0]
    header = "| Year | " + " | ".join(roles_present) + " | Total |"
    sep = "|------|" + "|".join(["-------"] * len(roles_present)) + "|-------|"
    lines.append(header)
    lines.append(sep)
    for year in years_sorted:
        counts = [str(by_year[year].get(r, 0)) for r in roles_present]
        total = sum(by_year[year].values())
        lines.append(f"| {year} | " + " | ".join(counts) + f" | {total} |")
    lines.append("")

    # All promotions table
    lines.append("## All Promotions")
    lines.append("")
    lines.append("| Date | Candidate | Role | Project | Nominator | Votes | Voters |")
    lines.append("|------|-----------|------|---------|-----------|-------|--------|")
    for entry in entries:
        date = entry.get('date', '')
        candidate = entry.get('candidate', '')
        role = entry.get('role', '')
        project = entry.get('project', '')
        nominator = entry.get('nominator', '')
        vote_count = entry.get('vote_count', 0)
        voters = entry.get('voters', '')
        url = entry.get('url', '')

        if len(voters) > 80:
            vlist = voters.split('; ')
            voters_display = "; ".join(vlist[:5])
            if len(vlist) > 5:
                voters_display += f" +{len(vlist)-5} more"
        else:
            voters_display = voters

        cand_display = f"[{candidate}]({url})" if url else candidate
        lines.append(f"| {date} | {cand_display} | {role} | {project} | {nominator} | {vote_count} | {voters_display} |")
    lines.append("")

    # Top voters
    lines.append("## Top Voters (Most Active Community Members)")
    lines.append("")
    lines.append("These individuals participate most frequently in CFV votes, indicating deep community engagement.")
    lines.append("")
    lines.append("| Rank | Voter | Votes Cast | Candidates Supported |")
    lines.append("|------|-------|------------|---------------------|")
    top_voters = sorted(voter_counts.items(), key=lambda x: x[1], reverse=True)[:40]
    for rank, (voter, count) in enumerate(top_voters, 1):
        candidates = voter_for[voter]
        if len(candidates) > 5:
            cand_display = ", ".join(candidates[:5]) + f" +{len(candidates)-5} more"
        else:
            cand_display = ", ".join(candidates)
        lines.append(f"| {rank} | {voter} | {count} | {cand_display} |")
    lines.append("")

    # Top nominators
    lines.append("## Top Nominators")
    lines.append("")
    lines.append("| Rank | Nominator | Nominations |")
    lines.append("|------|-----------|-------------|")
    top_noms = sorted(nominators_count.items(), key=lambda x: x[1], reverse=True)[:20]
    for rank, (nom, count) in enumerate(top_noms, 1):
        lines.append(f"| {rank} | {nom} | {count} |")
    lines.append("")

    # Voter network
    lines.append("## Voter Network Analysis")
    lines.append("")
    lines.append("Relationships between voters and candidates reveal trust networks in the OpenJDK community.")
    lines.append("")

    # Mutual voting
    mutual_votes = []
    seen_pairs = set()
    for candidate in candidate_voters:
        for voter in candidate_voters[candidate]:
            if voter in candidate_voters and candidate in candidate_voters[voter]:
                pair = tuple(sorted([candidate, voter]))
                if pair not in seen_pairs:
                    seen_pairs.add(pair)
                    mutual_votes.append(pair)

    if mutual_votes:
        lines.append("### Mutual Voting Pairs")
        lines.append("")
        lines.append("These pairs have both been promoted AND voted for each other, indicating strong mutual trust.")
        lines.append("")
        lines.append("| Person A | Person B |")
        lines.append("|----------|----------|")
        for a, b in sorted(mutual_votes)[:30]:
            lines.append(f"| {a} | {b} |")
        lines.append("")

    # Co-voting clusters
    lines.append("### Voting Clusters")
    lines.append("")
    lines.append("Pairs of voters who frequently vote on the same candidates.")
    lines.append("")

    co_vote = defaultdict(int)
    for candidate in candidate_voters:
        vlist = candidate_voters[candidate]
        for i in range(len(vlist)):
            for j in range(i + 1, len(vlist)):
                pair = tuple(sorted([vlist[i], vlist[j]]))
                co_vote[pair] += 1

    top_pairs = sorted(co_vote.items(), key=lambda x: x[1], reverse=True)[:25]
    if top_pairs and top_pairs[0][1] >= 2:
        lines.append("| Voter A | Voter B | Co-votes |")
        lines.append("|---------|---------|----------|")
        for (a, b), count in top_pairs:
            if count >= 2:
                lines.append(f"| {a} | {b} | {count} |")
        lines.append("")

    # Stats
    total_votes = sum(entry.get('vote_count', 0) for entry in entries)
    entries_with_votes = sum(1 for e in entries if e.get('vote_count', 0) > 0)
    if entries_with_votes > 0:
        avg_votes = total_votes / entries_with_votes
        max_entry = max(entries, key=lambda x: x.get('vote_count', 0))
        lines.append("## Statistics")
        lines.append("")
        lines.append(f"- **Average votes per promotion:** {avg_votes:.1f}")
        lines.append(f"- **Promotions with recorded votes:** {entries_with_votes}/{len(entries)}")
        lines.append(f"- **Most votes on a single promotion:** {max_entry.get('vote_count', 0)}")
        lines.append(f"- **Most-voted promotion:** {max_entry.get('candidate', '')} ({max_entry.get('role', '')}) with {max_entry.get('vote_count', 0)} votes")
        lines.append("")

    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, 'w') as f:
        f.write('\n'.join(lines))
    print(f"Wrote report to {REPORT_FILE}", flush=True)


def main():
    print("=" * 60)
    print("OpenJDK CFV Vote Scraper")
    print("=" * 60)

    cache = load_cache()
    all_entries = cache.get('entries', [])
    months_done = set(cache.get('months_done', []))

    months = []
    y, m = 2026, 3
    while (y, m) >= (2020, 1):
        months.append((y, MONTH_NAMES[m - 1]))
        m -= 1
        if m < 1:
            m = 12
            y -= 1

    for year, month_name in months:
        key = f"{year}-{month_name}"
        if key in months_done:
            print(f"Skipping {key} (cached)", flush=True)
            continue

        try:
            results = process_month(year, month_name)
            all_entries.extend(results)
            months_done.add(key)

            cache['months_done'] = list(months_done)
            cache['entries'] = all_entries
            save_cache(cache)
        except KeyboardInterrupt:
            print("\nInterrupted! Saving progress...", flush=True)
            cache['months_done'] = list(months_done)
            cache['entries'] = all_entries
            save_cache(cache)
            break
        except Exception as e:
            print(f"  ERROR processing {key}: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            continue

    # Deduplicate by (candidate, role) - keep the one with more votes
    dedup = {}
    for entry in all_entries:
        key = (entry.get('candidate', ''), entry.get('role', ''))
        if key not in dedup or entry.get('vote_count', 0) > dedup[key].get('vote_count', 0):
            dedup[key] = entry
    unique_entries = list(dedup.values())

    print(f"\nTotal unique CFV entries: {len(unique_entries)}")
    write_csv(unique_entries)
    generate_report(unique_entries)
    print("\nDone!")


if __name__ == '__main__':
    main()
