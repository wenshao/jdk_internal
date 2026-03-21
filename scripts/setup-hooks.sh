#!/bin/bash
# setup-hooks.sh — Install git pre-commit hook for jdk_internal
#
# Creates a symlink from .git/hooks/pre-commit to scripts/pre-commit-check.sh
# so the checks run automatically before each commit.
#
# Usage:
#   bash scripts/setup-hooks.sh
#
# Safe to run multiple times — will update an existing symlink.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOK_TARGET="$REPO_ROOT/.git/hooks/pre-commit"
HOOK_SOURCE="$REPO_ROOT/scripts/pre-commit-check.sh"

# ---------------------------------------------------------------------------
# Ensure the pre-commit script exists
# ---------------------------------------------------------------------------
if [[ ! -f "$HOOK_SOURCE" ]]; then
    echo "ERROR: $HOOK_SOURCE not found."
    exit 1
fi

# ---------------------------------------------------------------------------
# Make the pre-commit script executable
# ---------------------------------------------------------------------------
chmod +x "$HOOK_SOURCE"

# ---------------------------------------------------------------------------
# Create (or replace) the symlink
# ---------------------------------------------------------------------------
if [[ -L "$HOOK_TARGET" ]]; then
    echo "Updating existing symlink at $HOOK_TARGET"
    rm "$HOOK_TARGET"
elif [[ -f "$HOOK_TARGET" ]]; then
    echo "WARNING: $HOOK_TARGET already exists and is a regular file."
    echo "Backing up to ${HOOK_TARGET}.bak"
    mv "$HOOK_TARGET" "${HOOK_TARGET}.bak"
fi

ln -s "$HOOK_SOURCE" "$HOOK_TARGET"

# ---------------------------------------------------------------------------
# Confirm
# ---------------------------------------------------------------------------
echo ""
echo "Pre-commit hook installed successfully."
echo "  Hook:   $HOOK_TARGET -> $HOOK_SOURCE"
echo ""
echo "The hook will check staged .md files for:"
echo "  - Broken internal links"
echo "  - Placeholder text (TODO, TBD, FIXME, etc.)"
echo "  - Fabricated JVM flags"
echo "  - JDK 25 non-LTS errors"
echo "  - TLS 1.4 references"
echo "  - Fake commit hashes"
echo ""
echo "To bypass the hook for a single commit:  git commit --no-verify"
echo "To check all files manually:             ./scripts/pre-commit-check.sh --all"
