#!/bin/bash
# JDK Internal Docs 质量检查脚本
# 用法: bash scripts/quality_check.sh

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "=========================================="
echo "JDK Internal Docs 质量检查报告"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""

# 1. 基本统计
echo "=== 1. 基本统计 ==="
total_files=$(find . -name '*.md' -type f | wc -l)
total_lines=$(find . -name '*.md' -type f -exec cat {} + | wc -l)
profile_count=$(ls by-contributor/profiles/*.md 2>/dev/null | grep -cv 'jdk2[0-9]-top\|chinese-\|top-\|README\|TEMPLATE\|_template\|analysis' || echo 0)
echo "总文件数: $total_files"
echo "总行数: $total_lines"
echo "贡献者 Profile 数: $profile_count"
echo ""

# 2. 断链检查 (内部 .md 链接)
echo "=== 2. 断链检查 (抽样前 50 个) ==="
broken=0
checked=0
find . -name '*.md' -type f | head -100 | while read f; do
  grep -oP '\]\((/[^)]+\.md)\)' "$f" 2>/dev/null | sed 's/](\(.*\))/\1/' | while read link; do
    target=".$link"
    if [ ! -f "$target" ]; then
      echo "  断链: $f -> $link"
      broken=$((broken+1))
    fi
    checked=$((checked+1))
  done
done 2>/dev/null | head -20
echo ""

# 3. JDK 25 LTS 一致性检查
echo "=== 3. JDK 25 LTS 一致性 ==="
feature_count=$(grep -r "JDK 25.*Feature\|JDK 25.*feature\|JDK 25.*非 LTS" --include="*.md" -l 2>/dev/null | wc -l)
if [ "$feature_count" -gt 0 ]; then
  echo "  ⚠️ 发现 $feature_count 个文件仍将 JDK 25 标为 Feature:"
  grep -r "JDK 25.*Feature\|JDK 25.*feature\|JDK 25.*非 LTS" --include="*.md" -l 2>/dev/null | head -5
else
  echo "  ✅ JDK 25 LTS 状态一致"
fi
echo ""

# 4. 贡献者组织一致性检查
echo "=== 4. 贡献者组织一致性 ==="
# Shipilev should be Amazon everywhere
shipilev_wrong=$(grep -r "Shipilev.*Oracle\|Shipilev.*Red Hat" --include="*.md" 2>/dev/null | grep -v "formerly\|previously\|ex-\|历史\|曾\|当时\|时期\|at the time\|Oracle →\|Oracle->\|Oracle ->\|Career path\|reports/\|→.*Amazon\|->.*Amazon" | wc -l)
echo "  Aleksey Shipilev (应为 Amazon): 错误引用 $shipilev_wrong 处"

# Kennke should be Datadog
kennke_wrong=$(grep -r "Kennke.*Red Hat\|Kennke.*Oracle" --include="*.md" 2>/dev/null | grep -v "formerly\|previously\|ex-\|历史\|曾\|started\|创始\|当时\|时期\|at the time\|Red Hat →\|前 Red Hat\|前Red Hat\|Career path\|Red Hat 期间\|现已加入\|reports/\|→.*Datadog\|->.*Datadog\|Datadog.*Shenandoah\|人才流动" | wc -l)
echo "  Roman Kennke (应为 Datadog): 错误引用 $kennke_wrong 处"

# Stuefe should be Red Hat
stuefe_wrong=$(grep -r "Stuefe.*SAP\|Stuefe.*IBM\|Stuefe.*Oracle" --include="*.md" 2>/dev/null | grep -v "formerly\|previously\|ex-\|历史\|曾\|founder\|当时\|时期\|SAP →\|SAP->\|转至\|reports/\|→.*Red Hat\|->.*Red Hat\|属于.*Red Hat" | wc -l)
echo "  Thomas Stuefe (应为 Red Hat): 错误引用 $stuefe_wrong 处"
echo ""

# 5. 虚构内容检查
echo "=== 5. 虚构内容检查 ==="
# Fabricated JVM flags
for flag in "G1UseClaimTable" "ShenandoahYoungGenerationSize" "ProfileAtExit" "ProfileData" "UseMetaspace"; do
  count=$(grep -r "$flag" --include="*.md" 2>/dev/null | grep -v "不存在\|does not exist\|removed\|fabricated" | wc -l)
  if [ "$count" -gt 0 ]; then
    echo "  ⚠️ 虚构 JVM flag '$flag' 仍出现 $count 处"
  fi
done

# io_uring false claims
iouring=$(grep -r "io_uring.*JDK 21\|useIOUring" --include="*.md" 2>/dev/null | grep -v "不支持\|not supported\|experimental\|未" | wc -l)
if [ "$iouring" -gt 0 ]; then
  echo "  ⚠️ io_uring 虚假支持声明 $iouring 处"
else
  echo "  ✅ 无虚构 io_uring 声明"
fi

# TLS 1.4
tls14=$(grep -r "TLS 1.4" --include="*.md" 2>/dev/null | wc -l)
if [ "$tls14" -gt 0 ]; then
  echo "  ⚠️ TLS 1.4 (不存在) 仍出现 $tls14 处"
else
  echo "  ✅ 无虚构 TLS 1.4"
fi
echo ""

# 6. 虚构 commit hash 检查
echo "=== 6. 虚构 commit hash 检查 ==="
fake_hash=$(grep -r "a1b2c3d4e5f\|b2c3d4e5f6a\|c3d4e5f6a7b" --include="*.md" 2>/dev/null | grep -v "omitted\|省略" | wc -l)
if [ "$fake_hash" -gt 0 ]; then
  echo "  ⚠️ 虚构 commit hash 仍出现 $fake_hash 处"
else
  echo "  ✅ 无虚构 commit hash"
fi
echo ""

# 7. pre-GitHub PR 数据检查
echo "=== 7. pre-GitHub PR 数据检查 ==="
pre_github=$(grep -r "201[0-8].*PR\|201[0-8].*个 PR\|201[0-9].*PRs" --include="*.md" contributors/ 2>/dev/null | grep -v "pending\|待\|不存在\|pre-2020" | wc -l)
echo "  contributors/ 中 pre-2020 PR 声明: $pre_github 处 (OpenJDK 2020 迁移 GitHub)"
echo ""

echo "=========================================="
echo "检查完成"
echo "=========================================="
