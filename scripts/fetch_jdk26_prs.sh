#!/bin/bash
# 获取 JDK 26 PR 数据

OUTPUT_FILE="prs/jdk26-prs.json"

echo "Fetching JDK 26 PRs..."

# 获取 2024年9月以来的合并 PR
gh pr list --repo openjdk/jdk \
    --state merged \
    --limit 3000 \
    --json number,title,author,labels,additions,deletions,changedFiles,mergedAt,comments \
    --search "merged:>=2024-09-01 base:master" \
    > "$OUTPUT_FILE"

echo "Saved to $OUTPUT_FILE"
echo "Total PRs: $(jq 'length' $OUTPUT_FILE)"
