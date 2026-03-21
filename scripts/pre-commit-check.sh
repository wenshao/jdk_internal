#!/bin/bash
# pre-commit-check.sh — Fast pre-commit checks for jdk_internal .md files
#
# Designed to run in < 5 seconds on staged files only.
# Catches common errors: broken internal links, placeholder text,
# fabricated JVM flags, factual errors, and fake commit hashes.
#
# Usage:
#   ./scripts/pre-commit-check.sh          # check staged files only
#   ./scripts/pre-commit-check.sh --all    # check ALL .md files in repo
#
# Exit codes:
#   0  all checks passed
#   1  one or more checks failed

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

# ---------------------------------------------------------------------------
# Determine which files to check
# ---------------------------------------------------------------------------
CHECK_ALL=false
if [[ "${1:-}" == "--all" ]]; then
    CHECK_ALL=true
fi

FILELIST=$(mktemp)
ERRFILE=$(mktemp)
trap 'rm -f "$FILELIST" "$ERRFILE"' EXIT

if $CHECK_ALL; then
    find . -name '*.md' -type f | sed 's|^\./||' | grep -v '^reports/' | grep -v '^AGENTS.md' > "$FILELIST"
else
    git diff --cached --name-only --diff-filter=ACM 2>/dev/null \
        | grep '\.md$' | grep -v '^reports/' | grep -v '^AGENTS.md' > "$FILELIST" || true
fi

if [[ ! -s "$FILELIST" ]]; then
    # Nothing to check — pass silently
    exit 0
fi

# Error file starts empty; each check appends errors
> "$ERRFILE"

# ---------------------------------------------------------------------------
# Helper: run grep across all target files using xargs (handles large lists)
# Outputs file:lineno:content lines.
# ---------------------------------------------------------------------------
bulk_grep() {
    local pattern="$1"
    shift
    # Default flags: -nP (line numbers, PCRE)
    local flags="${*:--nP}"
    cat "$FILELIST" | xargs -d'\n' grep $flags -- "$pattern" 2>/dev/null || true
}

# ---------------------------------------------------------------------------
# 1. Broken internal links (quick: only checks that target .md files exist)
#    Matches patterns like [text](/path/to/file.md) and [text](../relative.md)
#    Skips external URLs and anchors-only links.
# ---------------------------------------------------------------------------
echo "Checking internal links..."
# First, extract all file:lineno:target triples in one pass using Perl.
# This avoids spawning grep subprocesses per line.
cat "$FILELIST" | xargs -d'\n' perl -ne '
    # Track filename from ARGV
    if ($ARGV ne $prev_file) { $prev_file = $ARGV; }
    while (/\]\(([^)]+\.md(?:#[^)]*)?)\)/g) {
        my $target = $1;
        next if $target =~ m{^https?://};
        next if $target =~ m{^mailto:};
        # Strip anchor for file check
        (my $path = $target) =~ s/#.*//;
        next if $path eq "";
        # Resolve path
        my $dir = $ARGV;
        $dir =~ s{/[^/]+$}{};
        $dir = "." if $dir eq $ARGV;  # file in repo root
        my $resolved;
        if ($path =~ m{^/}) {
            $resolved = ".$path";
        } else {
            $resolved = "$dir/$path";
        }
        unless (-f $resolved) {
            printf "%s:%d: Broken link: %s (file not found)\n", $ARGV, $., $target;
        }
    }
' 2>/dev/null >> "$ERRFILE"

# ---------------------------------------------------------------------------
# 2. Placeholder text (TODO, TBD, FIXME, Chinese placeholders)
# ---------------------------------------------------------------------------
echo "Checking for placeholder text..."
PLACEHOLDER_PATTERN='(TODO|TBD|FIXME|待补充|需要补充\s*PR\s*链接)'
bulk_grep "$PLACEHOLDER_PATTERN" -niP | while IFS= read -r line; do
    # Extract file:lineno and the matched placeholder
    file_line="${line%%:*}"
    rest="${line#*:}"
    lineno="${rest%%:*}"
    content="${rest#*:}"
    matched=$(echo "$content" | grep -oiP "$PLACEHOLDER_PATTERN" | head -1)
    echo "  ${file_line}:${lineno}: Placeholder text found: ${matched}"
done >> "$ERRFILE"

# ---------------------------------------------------------------------------
# 3. Fabricated JVM flags (known non-existent flags that AI tends to invent)
#
#    NOTE: The following are REAL flags and are NOT listed here:
#      - ZGenerational (-XX:+ZGenerational, JDK 21+)
#      - UseCompactObjectHeaders (-XX:+UseCompactObjectHeaders, JEP 450 / Lilliput)
#      - G1ConcMarkThreads (-XX:G1ConcMarkThreads, real G1 tuning flag)
#    Only truly fabricated flags are listed here.
# ---------------------------------------------------------------------------
echo "Checking for fabricated JVM flags..."
FAKE_FLAGS_PATTERN='(G1UseClaimTable|ShenandoahYoungGenerationSize|ShenandoahOldGenerationSize|ZGenerationalMode|UseCompactHeaders|G1UseAdaptiveConcRefinement|ShenandoahOptimizeBarriers|UseZGCGeneration|ShenandoahRegionSizeBytes)'

bulk_grep "$FAKE_FLAGS_PATTERN" -nP | while IFS= read -r line; do
    file_line="${line%%:*}"
    rest="${line#*:}"
    lineno="${rest%%:*}"
    content="${rest#*:}"
    matched=$(echo "$content" | grep -oP "$FAKE_FLAGS_PATTERN" | head -1)
    echo "  ${file_line}:${lineno}: Likely fabricated JVM flag: ${matched}"
done >> "$ERRFILE"

# ---------------------------------------------------------------------------
# 4. JDK 25 non-LTS errors
#    JDK 25 IS an LTS release. Flag text that says otherwise.
# ---------------------------------------------------------------------------
echo "Checking for JDK 25 non-LTS errors..."
JDK25_PATTERN='JDK\s*25.{0,30}(non[- ]?LTS|非\s*LTS|Feature Release(?!\s*\(LTS\)))'
bulk_grep "$JDK25_PATTERN" -niP | while IFS= read -r line; do
    file_line="${line%%:*}"
    rest="${line#*:}"
    lineno="${rest%%:*}"
    echo "  ${file_line}:${lineno}: JDK 25 is LTS — text incorrectly says non-LTS or Feature Release"
done >> "$ERRFILE"

# ---------------------------------------------------------------------------
# 5. TLS 1.4 references (TLS 1.4 does not exist as of 2026)
# ---------------------------------------------------------------------------
echo "Checking for TLS 1.4 references..."
bulk_grep 'TLS\s*1\.4' -nP | while IFS= read -r line; do
    file_line="${line%%:*}"
    rest="${line#*:}"
    lineno="${rest%%:*}"
    echo "  ${file_line}:${lineno}: TLS 1.4 does not exist — verify the TLS version"
done >> "$ERRFILE"

# ---------------------------------------------------------------------------
# 6. Fake commit hashes (a1b2c3d4e5f repeating hex nibble pattern)
#    Real hashes are random; this pattern is suspiciously regular.
#    Matches 8+ char hex strings with alternating letter-digit pattern.
# ---------------------------------------------------------------------------
echo "Checking for fake commit hashes..."
FAKE_HASH_PATTERN='\b[a-f][0-9][a-f][0-9][a-f][0-9][a-f][0-9]([a-f][0-9])*\b'
bulk_grep "$FAKE_HASH_PATTERN" -nP | while IFS= read -r line; do
    file_line="${line%%:*}"
    rest="${line#*:}"
    lineno="${rest%%:*}"
    content="${rest#*:}"
    matched=$(echo "$content" | grep -oP "$FAKE_HASH_PATTERN" | head -1)
    if [[ ${#matched} -ge 7 ]]; then
        echo "  ${file_line}:${lineno}: Likely fake commit hash: ${matched}"
    fi
done >> "$ERRFILE"

# ---------------------------------------------------------------------------
# Report results
# ---------------------------------------------------------------------------
echo ""
ERRORS=$(wc -l < "$ERRFILE")
if [[ $ERRORS -gt 0 ]]; then
    echo "FAILED: ${ERRORS} error(s) found:"
    echo ""
    cat "$ERRFILE"
    echo ""
    echo "Commit blocked. Fix the errors above or use 'git commit --no-verify' to bypass."
    exit 1
else
    echo "All pre-commit checks passed."
    exit 0
fi
