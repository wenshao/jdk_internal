#!/bin/bash

# Check all markdown links in the repository
# Convert relative paths to absolute and verify files exist

ROOT_DIR="/root/git/jdk_internal-x1"
ERROR_COUNT=0
CHECKED_COUNT=0

echo "Checking markdown links in $ROOT_DIR"
echo "========================================"

# Find all markdown files
find "$ROOT_DIR" -name "*.md" -type f | while read -r file; do
    # Extract all markdown links using grep
    # Match patterns like [text](path) or [text](path#anchor)
    links=$(grep -oE '\[([^\]]+)\]\(([^)]+)\)' "$file" 2>/dev/null | grep -oE '\(([^)]+)\)' | tr -d '()')
    
    if [ -n "$links" ]; then
        while IFS= read -r link; do
            # Skip external links (http, https, mailto)
            if [[ "$link" =~ ^https?:// ]] || [[ "$link" =~ ^mailto: ]]; then
                continue
            fi
            
            # Skip anchor-only links
            if [[ "$link" =~ ^# ]]; then
                continue
            fi
            
            # Remove anchor from link
            link_path="${link%%#*}"
            
            # Skip empty paths
            if [ -z "$link_path" ]; then
                continue
            fi
            
            # Resolve the path
            if [[ "$link_path" =~ ^/ ]]; then
                # Absolute path from repo root
                resolved_path="$ROOT_DIR$link_path"
            else
                # Relative path from current file's directory
                file_dir=$(dirname "$file")
                resolved_path=$(cd "$file_dir" && pwd)/$link_path
            fi
            
            # Normalize path (resolve .. and .)
            resolved_path=$(cd "$(dirname "$resolved_path")" 2>/dev/null && pwd)/$(basename "$resolved_path") 2>/dev/null
            
            # Check if file exists
            if [ ! -f "$resolved_path" ]; then
                echo "❌ $file -> $link_path"
                ((ERROR_COUNT++))
            fi
            
            ((CHECKED_COUNT++))
        done <<< "$links"
    fi
done

echo "========================================"
echo "Check completed."
