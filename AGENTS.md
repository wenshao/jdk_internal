# AGENTS.md - AI Assistant Guide

> **Purpose**: Help AI assistants understand this project and contribute effectively
> **Last Updated**: 2026-03-22

---

## Quick Start

### 📚 What is this project?
- **`../jdk`**: JDK source code repository
- **This project (`jdk_internal`)**: Documentation analyzing JDK issues, PRs, and source code
- **Goal**: Create documentation easy for both humans and AI to read

### 🎯 Your Tasks
1. **Read** existing documentation structure
2. **Verify** links before committing (use `ls` or `glob`)
3. **Use GitHub PRs** for contribution statistics (NOT git commits)
4. **Write in English** for explanations, keep technical terms unchanged

---

## Table of Contents

1. [Project Structure](#1-project-structure)
2. [Documentation Standards](#2-documentation-standards)
3. [Research Methodology](#3-research-methodology)
4. [Contribution Statistics](#4-contribution-statistics)
5. [Quality Checklist](#5-quality-checklist)
6. [Common Mistakes](#6-common-mistakes)

---

## 1. Project Structure

```
jdk_internal/
├── AGENTS.md              # This file - AI assistant guide
├── README.md              # Project overview
│
├── by-version/            # ⭐ Browse by JDK version
│   ├── README.md
│   ├── jdk8/              # JDK 8 (LTS 2014)
│   ├── jdk11/             # JDK 11 (LTS 2018)
│   ├── jdk17/             # JDK 17 (LTS 2021)
│   ├── jdk21/             # JDK 21 (LTS 2023)
│   └── jdk26/             # JDK 26 (GA 2026-03-17)
│
├── by-topic/              # ⭐ Browse by topic (architecture view)
│   ├── README.md
│   ├── gc/timeline.md     # G1/ZGC/Shenandoah timeline
│   ├── concurrency/
│   ├── string/
│   └── http/
│
├── by-contributor/        # Browse by contributor
│   ├── README.md
│   ├── profiles/          # 137 contributor profiles
│   └── by-org/
│
├── by-pr/                 # PR/Issue deep analysis
│   ├── README.md
│   └── {issue}/           # Grouped by issue number
│
├── contributors/          # Organization stats
│   ├── orgs/              # Organization pages
│   └── stats/             # Statistics (PRs-based)
│
├── jeps/                  # JEP analysis (21 files)
├── guides/                # General guides
└── modules/               # Module analysis
```

### Version Coverage Priority

| Version | Priority | Content Focus |
|---------|----------|---------------|
| JDK 26 | ⭐⭐⭐⭐⭐ | GA 2026-03-17, detailed tracking |
| JDK 21 | ⭐⭐⭐⭐ | Current LTS, key content |
| JDK 17 | ⭐⭐⭐⭐ | LTS, complete docs |
| JDK 11 | ⭐⭐⭐⭐ | LTS, complete docs |
| JDK 8 | ⭐⭐ | Migration guide, key features |

---

## 2. Documentation Standards

### Section Numbering Format

**All long documents (>200 lines) MUST have:**
1. Section numbers: `1`, `1.1`, `1.1.1`
2. Table of Contents after title
3. Consistent heading levels (max 4 levels)

**Example:**
```markdown
# Title

## Table of Contents
1. [Overview](#1-overview)
2. [Details](#2-details)
   1. [Subsection](#21-subsection)

---

## 1. Overview
Content here...

## 2. Details
### 2.1 Subsection
Content here...
```

### PR Document Template

```markdown
# JDK-XXXXXXX: Short Title

> **Issue**: [link] | **Author**: [Name](profile.md) | **Impact**: ⭐⭐⭐⭐

## Overview
One-sentence description

## Background
Problem context

## Analysis
Technical details

## Solution
Changes made

## Performance
Benchmarks if applicable

## Related PRs
Links to related work
```

### Link Format

| Type | Format | Example |
|------|--------|---------|
| **Profile** | Local link | `[Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)` |
| **Organization** | Local link | `[Oracle](/contributors/orgs/oracle.md)` |
| **PR Analysis** | Local link | `[JDK-8336856](/by-pr/8336/8336856.md)` |
| **JEP** | Local link | `[JEP 506](/jeps/concurrency/jep-506.md)` |
| **External** | Full URL | `[GitHub](https://github.com/openjdk/jdk)` |

---

## 3. Research Methodology

### Data Source Priority

| Priority | Source | Use Case |
|----------|--------|----------|
| **P0** | JBS Issue | Problem definition, status |
| **P0** | GitHub PR | Changes, discussion |
| **P1** | Mailing Lists | Design decisions |
| **P1** | JEP/JSR Docs | Specifications |
| **P2** | Source Code | Implementation details |
| **P3** | Blogs/Talks | Context (auxiliary only) |

**Key Principle**: All conclusions must be supported by P0-P2 sources

### Research Quality Levels

| Level | PR Documents | Topic Documents | Use Case |
|-------|-------------|-----------------|----------|
| **L1** | Title + link + 1 sentence | Timeline overview | Bulk P4 processing |
| **L2** | Overview + key changes | Version comparison | P3 PRs, minor features |
| **L3** | Full template structure | Technical details + examples | P2 PRs, important features |
| **L4** | Principle analysis + benchmarks | Multi-version evolution | P1 PRs, JEPs, core features |

---

## 4. Contribution Statistics

### ⚠️ CRITICAL: Use GitHub Integrated PRs ONLY

**Why NOT git commits?**
```
❌ OpenJDK Committers use @openjdk.org email for commits
❌ Git commits by company email is inaccurate
❌ Many contributions are missed when filtering by company email
✅ GitHub PRs accurately reflect actual contributions
```

### How to Query PRs

**Method 1: Web Interface (Recommended)**
```
https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3A{username}+label%3Aintegrated+is%3Aclosed
```

**Method 2: GitHub CLI**
```bash
# Get all integrated PRs
gh pr list --repo openjdk/jdk --limit 300 \
  --search "author:{username} state:closed label:integrated" \
  --json number,title,closedAt

# Count total
gh pr list --repo openjdk/jdk --limit 1000 \
  --search "author:{username} state:closed label:integrated" \
  --json number --jq 'length'
```

### Statistics Format

```markdown
### Key Metrics

| Metric | Value |
|--------|-------|
| **Integrated PRs** | {count} |
| **Code Changes** | +xxx / -xxx |
| **Main Focus** | xxx |
| **Avg Merge Time** | x.x days |

> **Source**: [GitHub Integrated PRs](link)
```

### Contributor Discovery & Organization Verification (2026-03-23 沉淀)

> 本节总结了通过源码版权 + 邮件列表 + GitHub API + OpenJDK Census 四重验证发现遗漏贡献者的方法论。
> 通过此方法发现了大量被遗漏的贡献者，如 Tencent 从 10+ PRs 修正为 228+ PRs，Red Hat 新发现 Roland Westrelin (225 PRs) 等。

#### 方法 1: 源码版权反查法

**原理**: openjdk/jdk 源码文件头部包含 `Copyright (c) [year], [Organization]` 版权声明。通过搜索非 Oracle 版权 → 定位文件 → 查看 git commit 历史 → 反查 PR 作者 → 确认组织归属。

```bash
# Step 1: 搜索特定组织的版权文件
gh api "search/code?q=%22Tencent%22+repo:openjdk/jdk&per_page=100" \
  --jq '.items[].path'

# Step 2: 查看文件的 commit 作者
gh api "repos/openjdk/jdk/commits?path={file_path}&per_page=5" \
  --jq '.[].author.login'

# Step 3: 验证作者的 GitHub 公司信息
gh api users/{username} --jq '{name, company, location}'

# Step 4: 统计作者的 Integrated PRs
gh api "search/issues?q=repo:openjdk/jdk+author:{username}+label:integrated+is:pr" \
  --jq '.total_count'
```

**注意**: 部分组织曾使用子公司名称 (如 Tencent 曾用 "THL A29 Limited")，需搜索历史名称。

**实战成果**:
| 组织 | 搜索关键词 | 版权文件数 | 发现的遗漏贡献者 |
|------|-----------|-----------|-----------------|
| Tencent | "Tencent" | 58 | Jie Fu (187 PRs), John Jiang (30 PRs) |
| Alibaba | "Alibaba" | 90 | Denghui Dong (36 PRs), Long Yang (3 PRs) |
| Amazon | "Amazon.com" | 526 | Cesar Soares (46 PRs), Chad Rakoczy (18 PRs), Oliver Gillespie (18 PRs) |
| Red Hat | "Red Hat" | 872 | Roland Westrelin (225 PRs) |

#### 方法 2: OpenJDK 邮件列表 CFV 提名法

**原理**: 当贡献者被提名为 Committer/Reviewer 时，提名邮件通常包含其组织归属信息。

```bash
# 浏览 jdk-dev 邮件列表按月归档的主题索引
# URL 格式: https://mail.openjdk.org/pipermail/jdk-dev/{YYYY}-{Month}/subject.html

# 用 WebFetch 获取每月 subject.html，搜索 "CFV" 主题
# 找到 CFV 后，获取提名邮件详情确认组织

# 也可以搜索月度文本归档中的邮箱域名
curl -s "https://mail.openjdk.org/pipermail/jdk-dev/{YYYY}-{Month}.txt" | \
  grep -i "@tencent.com\|@alibaba"
```

**实战成果**:
| 来源 | 发现 |
|------|------|
| jiefu@tencent.com 投票邮件 | 确认 Jie Fu 是 Tencent |
| CFV: Denghui Dong (2021-08) | 确认 "Alibaba JVM Team" |
| CFV: Shaojin Wen (2024-08) | 确认 Alibaba, 由 Claes Redestad 提名 |
| JDK-8364597 "Replace THL A29 Limited with Tencent" | 发现 John Jiang (@johnshajiang) |

#### 方法 3: OpenJDK Census 角色验证法

**原理**: [OpenJDK Census](https://openjdk.org/census) 记录了所有 Author/Committer/Reviewer 的角色。用于验证和修正文档中的角色信息。

```
# 访问 https://openjdk.org/census
# 在 JDK Project 下查找贡献者的 OpenJDK 用户名和角色
# 常见用户名映射: swen=Shaojin Wen, ddong=Denghui Dong, jiefu=Jie Fu
```

#### 方法 4: Dragonwell/Corretto/SapMachine 等下游项目验证法

**原理**: 当 GitHub 公司信息缺失时，可通过检查贡献者在下游发行版项目的贡献来确认归属。

```bash
# 检查是否在 Alibaba Dragonwell 项目有贡献
gh api "search/issues?q=repo:dragonwell-project/dragonwell11+author:{username}" \
  --jq '.total_count'

# 检查是否在 Amazon Corretto 项目有贡献
gh api "search/issues?q=repo:corretto/corretto-17+author:{username}" \
  --jq '.total_count'
```

#### 方法 5: PR 审查关系网络法

**原理**: 同组织贡献者之间经常互相审查 PR。通过分析审查者来推断未知贡献者的归属。

```bash
# 获取某 PR 的审查者列表
gh api "repos/openjdk/jdk/pulls/{pr_number}/reviews" --jq '.[].user.login'
```

**实战成果**: 通过 Swati Sharma (@sviswa7) 的 PR 由 Jatin Bhateja (@jatin-bhateja, Intel) 审查，推断 sviswa7 为 Intel 贡献者。

#### 验证标准

| 证据强度 | 标准 | 是否足以确认归属 |
|----------|------|-----------------|
| ✅ 强 | GitHub 公司标注 | 是 |
| ✅ 强 | CFV 提名邮件明确标注组织 | 是 |
| ✅ 强 | 邮件列表中使用公司邮箱 (如 @tencent.com) | 是 |
| ⚠️ 中 | 下游发行版项目有贡献 (如 Dragonwell) | 是 (需多个信号) |
| ⚠️ 中 | PR 审查关系指向特定组织 | 是 (需多个信号) |
| ❌ 弱 | 仅修改过某组织版权文件 | 否 (Oracle 人也改 Alibaba 文件) |
| ❌ 弱 | 名字听起来像某国家的 | 否 |

### Top Contributors (by PRs)

| Rank | Contributor | PRs | Organization | Focus |
|------|-------------|-----|--------------|-------|
| 1 | [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | 803+ | Amazon | GC, JMH |
| 2 | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | 200+ | Oracle | C2 Compiler |
| 3 | [Phil Race](/by-contributor/profiles/phil-race.md) | 200+ | Oracle | Graphics |
| 4 | [Claes Redestad](/by-contributor/profiles/claes-redestad.md) | 150+ | Oracle | Core Libs |
| 5 | [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | 97 | Alibaba | Core Libs |

---

## 5. Quality Checklist

### Before Committing

**Link Verification** ✅
```bash
# Extract and verify all local links
grep -oE '\]\([^)]+\.md\)' file.md | while read link; do
  path=$(echo "$link" | sed "s/](//;s/)//")
  if [[ "$path" == ../* ]]; then
    target="$(dirname file.md)/$path"
    [ ! -f "$target" ] && echo "BROKEN: $path"
  fi
done
```

**Common Link Errors** ❌
| Error | Wrong | Correct |
|-------|-------|---------|
| Wrong directory | `contributors/organizations/` | `contributors/orgs/` |
| Case sensitivity | `Thomas-Schatzl.md` | `thomas-schatzl.md` |
| Missing subdir | `by-pr/8336856.md` | `by-pr/8336/8336856.md` |

**Content Verification** ✅
- [ ] All local links verified with `ls` or `glob`
- [ ] Profile links use correct filenames (lowercase, hyphens)
- [ ] Organization links use `orgs/` NOT `organizations/`
- [ ] Statistics use GitHub PRs (NOT git commits)
- [ ] JEP/Issue links are correct
- [ ] Technical details verified against source

**Structure Verification** ✅
- [ ] Follows template structure
- [ ] Section numbers consistent (1, 1.1, 1.1.1)
- [ ] Tables have headers
- [ ] Code blocks have language tags
- [ ] No TODO/待补充 placeholders

---

## 6. Common Mistakes

### ❌ WRONG vs ✅ CORRECT

**1. Contribution Statistics**
```markdown
❌ Based on git commits: 1,487 commits
✅ Based on Integrated PRs: 200+ PRs
```

**2. Organization Attribution**
```markdown
❌ Aleksey Shipilev - AWS (outdated)
✅ Aleksey Shipilev - Amazon (current)
```

**3. Link Format**
```markdown
❌ [Shaojin Wen](https://github.com/wenshao)  # External when local exists
✅ [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)  # Local
```

**4. JDK Version**
```markdown
❌ WRONG: "JDK 25 is non-LTS"
✅ JDK 25 IS LTS (September 2025, next LTS after JDK 21)
❌ WRONG: "JDK 26 is LTS"
✅ JDK 26 is non-LTS (March 2026)
```

**5. JEP Attribution**
```markdown
❌ JEP 514/515/519 belong to JDK 25
✅ JEP 514/515/519 belong to JDK 25
```

**6. Contributor Job Changes (verified 2026-03-23)**
```markdown
✅ Aleksey Shipilev - Amazon (since 2023, previously Red Hat 2016-2023, Oracle 2012-2016)
✅ Roman Kennke - Datadog (previously Amazon, Red Hat)
✅ Thomas Stuefe - Red Hat (previously SAP)
✅ William Kemper - Amazon (previously Red Hat)
✅ Andrew Dinn - IBM (previously Red Hat) -- GitHub bio confirms
✅ Severin Gehwolf - IBM (previously Red Hat)
✅ Fei Yang - Huawei (NOT ISCAS PLCT Lab)
✅ Nick Gasson - Arm (NOT Amazon)
✅ Axel Boldt-Christmas - Oracle (NOT SAP)
✅ Jatin Bhateja - Intel (NOT Oracle)
✅ Roland Westrelin - Red Hat (NOT Oracle)
✅ Zhengyu Gu - Datadog (previously Red Hat, Oracle)
✅ Xuelei Fan - Salesforce (previously Oracle)
✅ Hamlin Li - Rivos (previously Oracle)
✅ Quan Anh Mai - Shopee (NOT Independent)
✅ Chris Thalinger - Twitter/X (previously Oracle)
✅ Volker Simonis - AWS (previously SAP)
✅ Thomas Wuerthinger - Oracle Labs VP (NOT "Independent")
✅ Eric Fang - NVIDIA (NOT Oracle)
✅ Martin Haessig (mhaessig) - Oracle (NOT SAP, real name Manuel Hässig)
✅ Jie Fu (DamonFool) - Tencent (jiefu@tencent.com, OpenJDK Reviewer)
✅ John Jiang (johnshajiang) - Tencent (confirmed via JDK-8364597)
```

---

## 7. 系统性审查方法论 (2026-03-22 沉淀)

> 本节总结了对仓库进行 20+ 轮审查、修复 750+ 处错误的经验方法。

### 7.1 多轮审查策略

**核心原则**: 每轮聚焦不同角度，逐步收敛错误数量。

| 轮次 | 聚焦方向 | 预期发现 |
|------|---------|---------|
| 第 1-3 轮 | 事实性错误（JEP 号、版本、API 名称） | 100+ 处/轮 |
| 第 4-6 轮 | 跨文件一致性（同一事实在不同文件中的表述） | 30-50 处/轮 |
| 第 7-10 轮 | 贡献者组织归属（通过网络搜索验证） | 10-20 处/轮 |
| 第 11-15 轮 | 表述严谨性（"替代"→"替代方案"、性能声明加限定词） | 5-15 处/轮 |
| 第 16-20 轮 | 残留清扫（每轮 < 10 处时趋于收敛） | 3-6 处/轮 |

**停止条件**: 连续 2 轮发现 < 5 处新错误。

### 7.2 高频错误模式 (Top 10)

| 排名 | 错误模式 | 发现数 | 检测方法 |
|------|---------|--------|---------|
| 1 | **JEP 号张冠李戴** | ~150 | 逐个核对 openjdk.org/jeps/{number} |
| 2 | **贡献者组织归属错** | ~80 | 网络搜索 GitHub profile + LinkedIn |
| 3 | **Preview/Final 状态混淆** | ~50 | 对照 JEP 标题中的 (Preview)/(Final) |
| 4 | **虚构的 API/JVM flag** | ~40 | 搜索 JDK 源码验证方法名/flag 存在性 |
| 5 | **版本归属错误** | ~30 | 对照 openjdk.org/projects/jdk/{version} |
| 6 | **不严谨表述** | ~30 | "替代 X" 改为 "X 的替代方案"（X 未被废弃时） |
| 7 | **性能数据夸大/无来源** | ~25 | 要求标注 benchmark 来源或加"特定工作负载下" |
| 8 | **代码示例编译错误** | ~20 | 审查变量名、方法签名、返回类型 |
| 9 | **年份/日期错误** | ~15 | 对照 JDK 发布日期表 |
| 10 | **虚构 pre-GitHub PR 数据** | ~10 | OpenJDK 2020 年迁移 GitHub，之前无 PR |

### 7.3 贡献者组织验证工作流

```
Step 1: 检查 GitHub profile (company 字段)
  └─ github.com/{username}

Step 2: 搜索 OpenJDK CFV (Call for Votes) 邮件
  └─ mail.openjdk.org 搜索 "CFV {name}"

Step 3: 检查 OpenJDK Census
  └─ openjdk.org/census

Step 4: 搜索 LinkedIn / Inside.java
  └─ 交叉验证当前职位

Step 5: 检查近期 PR 的邮箱域名
  └─ @oracle.com / @redhat.com / @amazon.com 等
```

**关键发现**: GitHub company 字段最可靠，但可能滞后 6-12 个月。CFV 邮件提供最准确的历史组织信息。

### 7.4 Topic 文档质量评估标准

| 评级 | 标准 | 操作 |
|------|------|------|
| **OK** | JEP 号正确、版本正确、无虚构内容、结构清晰 | 无需修改 |
| **Enhance** | 基本正确但内容薄/缺少最新版本/有个别错误 | 补充 JDK 25-26 内容、修复错误 |
| **Rewrite** | 包含虚构内容（虚构 JEP/API/flag）或大量事实错误 | 重写，基于网络搜索验证 |

**常见需要重写的信号**:
- 出现不存在的 JEP 号（如 JEP 826、JEP 370 用于 KMAC）
- 出现不存在的 JVM flag（如 `-XX:+G1UseClaimTable`）
- 出现不存在的 API 方法（如 `readln()`、`lookupLibrary()`）
- pre-GitHub (2020 前) 的 "PR 数量" 数据
- 代码示例使用 Java 保留字作为变量名（如 `default`）

### 7.5 JDK 版本关键事实速查 (2026-03-22)

| JDK | 类型 | GA 日期 | 关键特性 |
|-----|------|---------|---------|
| 8 | LTS | 2014-03 | Lambda, Stream, java.time |
| 11 | LTS | 2018-09 | HTTP Client, var in lambda, ZGC (实验) |
| 17 | LTS | 2021-09 | Sealed Classes, Records (已 final), ZGC/Shenandoah (生产) |
| 21 | LTS | 2023-09 | Virtual Threads (final), Pattern Switch (final), Gen ZGC (非默认) |
| 25 | **LTS** | 2025-09 | Scoped Values (final), JEP 519 COH (实验), JEP 521 Gen Shenandoah (实验) |
| 26 | Feature | 2026-03 | HTTP/3 (final), G1 JEP 522, AOT JEP 516, Value Classes JEP 401 (preview) |

### 7.6 并行审查策略

使用多个 Agent 并行工作可以大幅加速审查：

```
推荐并行方案:
├── Agent 1: by-version 文件审查
├── Agent 2: by-topic 文件审查
├── Agent 3: 贡献者 profile 审查
└── Agent 4: 跨文件一致性检查

每个 Agent 完成后立即提交，不等待其他 Agent。
```

**注意事项**:
- 不同 Agent 不能修改同一个文件
- 审查 Agent 和修复 Agent 分开运行
- 每轮修复后再启动新一轮审查

---

## 3. Contributor Data Maintenance

### Job Changes and Organization Updates

**Important**: OpenJDK contributors frequently change jobs. Organization attribution must be regularly verified.

**Why this matters**:
- Contributors may move between companies (Oracle → Amazon, Red Hat → Amazon, etc.)
- GitHub company info may be outdated
- OpenJDK Census may lag behind real changes
- PR history spans multiple organizations

**Verification workflow**:

| Step | Action | Source |
|------|--------|--------|
| 1 | Check GitHub profile | `github.com/{username}` |
| 2 | Check LinkedIn | `linkedin.com/in/{username}` |
| 3 | Check recent PRs | GitHub PR search |
| 4 | Check mailing list | mail.openjdk.org |
| 5 | Check OpenJDK Census | openjdk.org/census |

**Example: Aleksey Shipilev**:
```
2011-2015: Red Hat (Shenandoah GC development)
2015-2020: Red Hat (continued)
2020-present: Amazon (Corretto team)
```

**Documentation practice**:
```markdown
### Organization History

| Period | Organization | Role |
|--------|--------------|------|
| 2020-present | Amazon | Senior Engineer |
| 2011-2020 | Red Hat | Senior Engineer |
```

**Update frequency**:
- **Active contributors**: Check every 6 months
- **Inactive contributors**: Check annually
- **After major PRs**: Verify current organization

### Common Job Change Patterns

| From | To | Frequency |
|------|-----|-----------|
| Oracle | Amazon | Common |
| Oracle | Google | Common |
| Red Hat | Amazon | Common |
| Oracle | Independent | Common (retirement/consulting) |
| Company | Startup | Common |

### Red Flags for Outdated Info

| Indicator | Action |
|-----------|--------|
| GitHub company unchanged for 5+ years | Verify |
| No recent PRs (2+ years) | Mark as "formerly" |
| Mailing list signature changed | Update |
| LinkedIn shows new company | Update immediately |

### Documentation Template

```markdown
## 基本信息

| 属性 | 值 |
|------|-----|
| **GitHub** | @username |
| **当前组织** | Company (verified 2026-03) |
| **曾任组织** | Previous Company (2020-2024) |
| **主要领域** | Technical focus |
```

**Note**: Always add verification date to organization info.

### Former Employee Contributions

**Important**: When a contributor leaves an organization, their historical contributions remain attributed to the original organization.

**Example: Sendaoyan Yan**
```
GitHub: @sendaoYan
Total PRs: 202
- 2022: 1 PR (early contribution)
- 2024: 82 PRs (Alibaba period)
- 2025: 95 PRs (Alibaba period)
- 2026: 24 PRs (current, independent/other)

Attribution:
- Historical PRs (2022-2025): Attributed to Alibaba
- Current PRs (2026+): Attributed to current organization or independent
```

**Documentation practice**:
```markdown
### Former Employees

| Contributor | Period | PRs | Current Status |
|-------------|--------|-----|----------------|
| Sendaoyan Yan | 2022-2025 | 201 | Independent/Other |
```

**Why this matters**:
- PRs are timestamped and cannot be re-attributed
- Historical work was done while employed at the organization
- Organization provided resources and support for the contribution
- Accurate historical record of organizational contributions

---

## 4. Quick Reference

### Essential Commands

```bash
# Verify file exists
ls /path/to/file.md

# Find contributor profile
ls by-contributor/profiles/{name}.md

# Check PR directory
ls by-pr/{issue-number}/

# Verify JEP exists
ls jeps/{category}/jep-{number}.md

# Count PRs for contributor
gh pr list --repo openjdk/jdk --search "author:{username} label:integrated" --json number --jq 'length'
```

### Important URLs

| Resource | URL |
|----------|-----|
| **JDK Repo** | https://github.com/openjdk/jdk |
| **JBS Issues** | https://bugs.openjdk.org |
| **OpenJDK Census** | https://openjdk.org/census |
| **JEP Index** | https://openjdk.org/jeps |
| **PR Search** | https://github.com/openjdk/jdk/pulls |

### File Patterns

| Pattern | Example |
|---------|---------|
| **Profile** | `by-contributor/profiles/shaojin-wen.md` |
| **Organization** | `contributors/orgs/oracle.md` |
| **PR Analysis** | `by-pr/8336/8336856.md` |
| **JEP** | `jeps/concurrency/jep-506.md` |
| **Topic** | `by-topic/core/gc/timeline.md` |

---

## 5. Recent Updates

### 2026-03-22 (Major Overhaul)

**系统性审查 (20+ 轮, 750+ 处修复)**:
- ✅ 修复 ~150 处 JEP 号张冠李戴
- ✅ 修复 ~80 处贡献者组织归属错误（通过网络搜索验证 15+ 个重大错误）
- ✅ 修复 ~50 处 Preview/Final 状态混淆
- ✅ 移除 ~40 处虚构的 API/JVM flag/JEP
- ✅ 修正 JDK 25 版本类型为 LTS

**贡献者档案增强**:
- ✅ 新建 27 个 profile（Mark Reinhold, Ron Pressler, Mandy Chung, Glavo 等）
- ✅ 通过网络搜索增强 ~120 个 profile
- ✅ 发现并修正 15+ 个组织归属重大错误
- ✅ 总 profile 数: 170

**Topic 重写/增强**:
- ✅ 重写 8 个 topic（security, concurrency, arch, platform, language, net 等）
- ✅ 增强 25+ 个 topic
- ✅ 新建 3 个 JEP 分析（JEP 506/516/522）

**Distributions 修复**:
- ✅ GraalVM CE/EE 合并反映
- ✅ Oracle 定价模型更新到 2023+ Universal Subscription
- ✅ 修正 non-LTS 支持期

### 2026-03-21

**Kuai Wei Deep Investigation**:
- ✅ Multi-layer association analysis (11 colleagues identified)
- ✅ Added colleague profiles: sendaoyan, yanglong1010, tanghaoth90, xhao, joshua-zhu, luchsh, sanhong, alijvm, aitozi, xiangzhai, headius
- ✅ Documented Shanghai/Hangzhou JVM community network
- ✅ Jeandle JDK project contributions tracked
- ✅ OpenJDK contribution timeline (2018-2025)
- ✅ Reviewer network documented (shade, kvn, vlivanov, etc.)

**Other Updates**:
- ✅ Added Jaroslav Bachorik (DataDog, JFR tools, 6 PRs)
- ✅ Fixed all stats to use GitHub Integrated PRs
- ✅ Corrected JDK 25 as LTS version
- ✅ Updated contributor rankings by PRs
- ✅ Added job change tracking guidelines

### Key Changes
| Document | Change |
|----------|--------|
| `by-version/README.md` | Fixed JDK 25 LTS error |
| `contributors/stats/*` | Changed from commits to PRs |
| `by-contributor/README.md` | Added Jaroslav Bachorik |
| `by-topic/core/performance/` | Added JEP table, fixed links |

---

**Remember**:
1. ✅ Always verify links before committing
2. ✅ Use GitHub PRs for statistics (NOT git commits)
3. ✅ Follow template structures
4. ✅ Keep technical terms in English, descriptions in Chinese
5. ✅ Verify contributor organization info via web search (job changes are common)
6. ✅ JDK 25 is LTS (2025-09), JDK 26 is non-LTS (2026-03) — 不要搞混
7. ✅ 性能声明必须加限定词（"特定工作负载下"）或标注来源
8. ✅ OpenJDK 2020 年才迁移到 GitHub，之前的 "PR 数量" 都是虚构的
9. ✅ "替代 X" vs "X 的替代方案" — 如果 X 未被废弃，用后者
10. ✅ 每轮修复后立即 git commit + push，不要积攒
6. ✅ Document organization history with verification dates
