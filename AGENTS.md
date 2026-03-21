# AGENTS.md - AI Assistant Guide

> **Purpose**: Help AI assistants understand this project and contribute effectively
> **Last Updated**: 2026-03-21

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
│   ├── index.md
│   ├── jdk8/              # JDK 8 (LTS 2014)
│   ├── jdk11/             # JDK 11 (LTS 2018)
│   ├── jdk17/             # JDK 17 (LTS 2021)
│   ├── jdk21/             # JDK 21 (LTS 2023)
│   └── jdk26/             # JDK 26 (GA 2026-03-17)
│
├── by-topic/              # ⭐ Browse by topic (architecture view)
│   ├── index.md
│   ├── gc/timeline.md     # G1/ZGC/Shenandoah timeline
│   ├── concurrency/
│   ├── string/
│   └── http/
│
├── by-contributor/        # Browse by contributor
│   ├── index.md
│   ├── profiles/          # 137 contributor profiles
│   └── by-org/
│
├── by-pr/                 # PR/Issue deep analysis
│   ├── index.md
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
❌ JDK 25 is LTS
✅ JDK 25 is Feature version (JDK 21/26 are LTS)
```

**5. JEP Attribution**
```markdown
❌ JEP 514/515/519 belong to JDK 26
✅ JEP 514/515/519 belong to JDK 25
```

**6. Contributor Job Changes**
```markdown
❌ Aleksey Shipilev - Red Hat (outdated, left in 2020)
✅ Aleksey Shipilev - Amazon (current, since 2020)

❌ Thomas Wuerthinger - Oracle (outdated, left in 2019)
✅ Thomas Wuerthinger - Independent/GraalVM Labs (current)
```

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
- ✅ Corrected JDK 25 as Feature version (not LTS)
- ✅ Updated contributor rankings by PRs
- ✅ Added job change tracking guidelines

### Key Changes
| Document | Change |
|----------|--------|
| `by-version/index.md` | Fixed JDK 25 LTS error |
| `contributors/stats/*` | Changed from commits to PRs |
| `by-contributor/index.md` | Added Jaroslav Bachorik |
| `by-topic/core/performance/` | Added JEP table, fixed links |

---

**Remember**:
1. ✅ Always verify links before committing
2. ✅ Use GitHub PRs for statistics
3. ✅ Follow template structures
4. ✅ Keep technical terms in English
5. ✅ Verify contributor organization info regularly (job changes are common)
6. ✅ Document organization history with verification dates
