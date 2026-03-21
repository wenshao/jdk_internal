## Agent Context

- `../jdk` is the JDK source code repository
- This project analyzes JDK issues, pull requests, and source code to create documentation that is easy for both humans and AI to read

## Project Structure

```
jdk_internal/
├── AGENTS.md              # Agent context (this file)
├── README.md              # Project overview with version selection
│
├── by-version/            # 按版本浏览 ⭐ 主要入口
│   ├── index.md           # 版本概览和对比
│   ├── jdk8/              # JDK 8 (LTS 2014)
│   ├── jdk11/             # JDK 11 (LTS 2018)
│   ├── jdk17/             # JDK 17 (LTS 2021)
│   ├── jdk21/             # JDK 21 (LTS 2023)
│   └── jdk26/             # JDK 26 (GA 2026-03-17)
│       ├── index.md       # 版本概览
│       ├── jeps.md        # JEP 汇总
│       └── migration/     # 迁移指南
│
├── by-topic/              # 按主题跨版本浏览 ⭐ 架构视角
│   ├── index.md           # 主题索引
│   ├── gc/                # GC 演进
│   │   └── timeline.md    # G1/ZGC/Shenandoah 时间线
│   ├── concurrency/       # 并发编程
│   ├── string/            # 字符串处理
│   ├── http/              # HTTP 客户端
│   └── security/          # 安全特性
│
├── by-contributor/        # 按贡献者
│   ├── index.md           # 贡献者索引
│   ├── profiles/          # 个人详细页面 (50+ files)
│   │   ├── shaojin-wen.md
│   │   └── ...
│   └── by-org/            # 按组织
│
├── by-pr/                 # 按 PR/Issue 深度分析
│   ├── index.md           # PR 索引
│   ├── {issue}/           # 按 issue 号分组
│   │   └── {number}.md
│   └── components/        # 按组件分组
│
├── jeps/                  # JEP 详细分析 (21 files)
│   └── jep-5xx.md
│
├── guides/                # 通用指南
│   ├── learning-path.md   # 学习路径
│   └── ...
│
└── modules/               # 模块/组件分析
    └── ...
```

## 文档组织原则

### 多版本视角

文档应支持从不同 JDK 版本的用户视角浏览：

1. **按版本** (by-version/)
   - 用户从当前使用的版本切入
   - 看到该版本的特性、问题、迁移指南
   - 支持版本间对比

2. **按主题** (by-topic/)
   - 架构师和技术负责人视角
   - 跨版本追踪某个技术演进
   - 时间线形式展示变化

3. **按贡献者** (by-contributor/)
   - 了解特定贡献者的工作
   - 按组织、地区浏览
   - 追踪专业领域

### 版本覆盖策略

| 版本 | 优先级 | 内容 |
|------|--------|------|
| JDK 8 | 中 | 迁移指南、关键特性 |
| JDK 11 | 高 | LTS 主流版本，完整文档 |
| JDK 17 | 高 | LTS 主流版本，完整文档 |
| JDK 21 | 高 | 当前 LTS，重点内容 |
| JDK 26 | 最高 | 已发布 (GA 2026-03-17)，详细追踪 |

## Documentation Standards

### Version Documents (by-version/{jdkxx}/)

每个版本目录应包含：

```markdown
{version}/
├── index.md           # 版本概览
├── new-since-{prev}.md # 相比上一版本的新特性
├── breaking-changes.md # 破坏性变更
├── known-issues.md     # 已知问题
├── performance.md      # 性能改进
└── migration/          # 迁移指南
    ├── from-{prev}.md  # 从上一版本升级
    └── to-{next}.md    # 升级到下一版本
```

### Topic Documents (by-topic/{topic}/)

每个主题目录应包含：

```markdown
{topic}/
├── index.md           # 主题概述
├── timeline.md        # 时间线 (必需)
└── {version}.md       # 各版本详细说明
```

时间线格式：
```markdown
## {Topic} 演进时间线

| 版本 | 主要变化 | 影响 |
|------|----------|------|
| JDK 8 | ... | ... |
| JDK 11 | ... | ... |
```

### Contributor Documents

见 [Contribution Statistics Principles](#contribution-statistics-principles)

### PR Documents (by-pr/{issue}/{number}.md)

使用统一模板：
```markdown
# JDK-XXXXXXX: 简短标题

> **Issue**: [链接] | **Author**: 名字 | **Impact**: ⭐⭐⭐⭐

## 一眼看懂
## 背景
## 问题分析
## 解决方案
## 性能对比
## 风险评估
## 相关 PR
```

## Research Methodology

### Research Quality Levels

Define completion levels to ensure consistent research depth across all documentation.

| Level | Name | PR Document Requirements | Topic Document Requirements | Use Case |
|-------|------|--------------------------|------------------------------|----------|
| **L1** | Summary | Title + link + one-sentence description | Timeline overview | Bulk P4 PR processing |
| **L2** | Brief | Overview + key changes | Version comparison table | P3 PRs, minor features |
| **L3** | Standard | Full template structure | Technical details + examples | P2 PRs, important features |
| **L4** | Deep | Principle analysis + benchmarks + design decisions | Multi-version evolution + source analysis | P1 PRs, JEPs, core features |

### Standard Research Process

```
┌─────────────────────────────────────────────────────────────────┐
│                     JDK Feature/PR Research Process              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Information Gathering                                        │
│     ├─ JBS Issue reading                                        │
│     ├─ GitHub PR description and discussion                     │
│     ├─ Mailing list discussion (if applicable)                  │
│     └─ Related JEP/JSR documents                                │
│         ↓                                                       │
│  2. Code Analysis                                               │
│     ├─ Locate changed files                                     │
│     ├─ Understand technical details                             │
│     └─ Identify impact scope                                    │
│         ↓                                                       │
│  3. Context Building                                            │
│     ├─ Related Issue/PR links                                   │
│     ├─ Historical evolution                                     │
│     └─ Contributor background                                   │
│         ↓                                                       │
│  4. Documentation                                               │
│     ├─ Write following template structure                       │
│     ├─ Code examples                                            │
│     └─ Visualizations (charts/timelines)                        │
│         ↓                                                       │
│  5. Quality Check                                               │
│     └─ Verify against review checklist                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Data Source Priority

| Priority | Data Source | Reliability | Purpose |
|----------|-------------|-------------|---------|
| **P0** | JBS Issue | Official | Problem definition, review status |
| **P0** | GitHub PR | Official | Change content, discussion |
| **P1** | Mailing Lists | Authoritative | Design decision background |
| **P1** | JEP/JSR Docs | Official | Specification definition |
| **P1** | OpenJDK Census | Official | Contributor group membership, organization verification |
| **P2** | Source Code | Factual | Implementation details |
| **P3** | Blogs/Talks | Reference | Explanation and context |

**Key Principles**:
- All conclusions must be supported by P0-P2 sources
- P3 sources are for auxiliary explanation only, never as primary evidence
- Always preserve original links when citing
- **Census Usage**: Use OpenJDK Census for verifying group membership and organization affiliation, NOT for contribution statistics (use GitHub Integrated PRs instead)

### AI-Assisted Research Prompt Templates

#### Template 1: PR Initial Analysis

```
You are a JDK internal implementation expert. Please analyze the following PR:

**PR Information:**
- Title: {title}
- Description: {body}
- Author: {author}
- Changed files: {files}

Please provide:
1. **One-line overview** (under 30 characters)
2. **Technical category**: [GC/Compiler/Runtime/CoreLibs/Network/Security/Other]
3. **Impact assessment**: [Performance/Compatibility/Feature/Refactor]
4. **Key change points** (3-5 items)
5. **Related Issues/JEPs** (if any)
```

#### Template 2: Deep Technical Analysis

```
Perform deep technical analysis based on the following information:

**Source code changes:**
```diff
{diff}
```

**PR discussion:**
{discussion}

Please analyze:
1. **Technical principle**: What underlying problem does this change solve?
2. **Design trade-offs**: Why was this approach chosen? What are the alternatives?
3. **Potential risks**: What problems could this introduce? How are they mitigated?
4. **Use cases**: What scenarios benefit from this change?
```

#### Template 3: Topic Evolution Analysis

```
Analyze the evolution of {topic} in JDK:

**Known version information:**
{version_info}

Please generate:
1. **Evolution timeline**: List key changes by version
2. **Technical turning points**: Important design decisions
3. **Version migration advice**: Considerations when upgrading from older versions
4. **Future direction**: Related unfinished/discussed JEPs
```

### Documentation Review Checklist

Verify the following before marking documentation as complete:

#### Content Completeness
- [ ] Clear overview (一眼看懂/概述 section)
- [ ] All key data has source links
- [ ] Code examples are runnable or explained
- [ ] Technical terms have explanations or links

#### Structure Consistency
- [ ] Follows corresponding template structure
- [ ] Heading levels are reasonable (max 4 levels)
- [ ] Tables have header descriptions
- [ ] Code blocks have language tags

#### Quality Standards
- [ ] No "TODO"/"待补充" placeholders
- [ ] External links are accessible
- [ ] Internal relative paths are correct
- [ ] Proper Chinese-English mixing (technical terms kept in English)

#### Type-Specific Checks

**PR Document Additional Checks:**
- [ ] Issue link is correct
- [ ] PR link is correct
- [ ] Author information is accurate
- [ ] Impact assessment has supporting evidence

**Topic Document Additional Checks:**
- [ ] Has timeline.md
- [ ] Version coverage is continuous
- [ ] Key JEPs are linked

**Contributor Document Additional Checks:**
- [ ] PR statistics use GitHub Integrated PRs
- [ ] Statistics data has source links
- [ ] Representative works have JBS links

### Error Pattern Recognition

Common issues and detection methods:

| Issue Type | Manifestation | Detection Method |
|------------|---------------|------------------|
| Data source error | Using git commit for contribution stats | Check for `git log` results |
| Broken links | JBS links return 404 | Periodic external link check |
| Version misattribution | Feature attributed to wrong version | Cross-verify JEP and version |
| Over-interpretation | Conclusions without data support | Check key statements for citations |
| Template inconsistency | Structure deviates from standard | Compare against template |
| **Wrong local path** | `contributors/organizations/` should be `contributors/orgs/` | Verify actual directory structure with `ls` |

### Local Link Verification Rules

**CRITICAL: Always verify local link paths against actual directory structure.**

When adding or checking local links:

1. **Verify directory structure**:
   ```bash
   # Check actual directory names
   ls -la contributors/
   # Output shows: orgs/ (NOT organizations/)
   ```

2. **Common path patterns in this project**:
   - Contributor profiles: `by-contributor/profiles/{username}.md`
   - Organizations: `contributors/orgs/{orgname}.md` (⚠️ NOT `organizations/`)
   - Topic pages: `by-topic/{category}/{topic}.md`
   - PR analysis: `by-pr/{issue-id}/{pr-number}.md`

3. **Before committing link changes**:
   - Use `Glob` or `ls` to verify target file exists
   - For bulk link updates, verify the path pattern first
   - Check all similar links in the same file

**Example of missed detection (2026-03)**:
- `talks/index.md` had 100+ links using `contributors/organizations/`
- Actual directory is `contributors/orgs/`
- Only detected after user reported broken link
- **Lesson**: When checking one type of link, check all similar patterns in the file

### Organization Link Priority

**CRITICAL: Always prefer local organization links over external URLs.**

When linking to organizations (Oracle, Alibaba, SAP, Red Hat, Amazon, Google, etc.):

1. **Priority order for organization links**:
   - **First**: Local organization page `/contributors/orgs/{orgname}.md`
   - **Second**: External website URL (only if no local page exists)

2. **Available local organization pages**:
   | Organization | Local Link |
   |--------------|------------|
   | Oracle | `/contributors/orgs/oracle.md` |
   | Alibaba | `/contributors/orgs/alibaba.md` |
   | SAP | `/contributors/orgs/sap.md` |
   | Red Hat | `/contributors/orgs/redhat.md` |
   | Amazon | `/contributors/orgs/amazon.md` |
   | Google | `/contributors/orgs/google.md` |
   | IBM | `/contributors/orgs/ibm.md` |
   | Tencent | `/contributors/orgs/tencent.md` |
   | ByteDance | `/contributors/orgs/bytedance.md` |
   | ISCAS PLCT | `/contributors/orgs/iscas-plct.md` |
   | Loongson | `/contributors/orgs/loongson.md` |

3. **When to use external links**:
   - Organization has no local page (e.g., Arm, NTT DATA, University of Washington)
   - Linking to specific resources (downloads, documentation, blogs)
   - Linking to JDK distribution pages

4. **Examples**:
   ```markdown
   # ✅ Correct - local link
   [Oracle](/contributors/orgs/oracle.md)

   # ❌ Wrong - external link when local page exists
   [Oracle](https://www.oracle.com/java/)

   # ✅ Correct - external link for specific resource
   [Oracle JDK Downloads](https://www.oracle.com/java/technologies/downloads/)

   # ✅ Correct - external link when no local page exists
   [Arm](https://www.arm.com/)
   ```

5. **Before adding organization links**:
   - Check if local page exists: `ls contributors/orgs/`
   - Use local link if available
   - Only use external URL for specific resources or when no local page exists

### Research Collaboration Guidelines

When multiple Agents collaborate:

1. **Task Assignment Principles**
   - Assign by component/topic to avoid duplication
   - Priority: P1 > P2 > P3 > P4
   - Related PRs should be handled by the same Agent

2. **Progress Synchronization**
   - Update index.md upon completion
   - Add cross-references in related documents
   - Research log (optional)

3. **Quality Assurance**
   - P1/P2 documents require cross-validation
   - Major updates require notifying related document maintainers

## Contribution Statistics Principles

**IMPORTANT: Use GitHub Integrated PRs as the ONLY metric for contribution statistics.**

**Why NOT use git commits?**
- OpenJDK Committers use `@openjdk.org` email for commits
- Git commits by company email domain is inaccurate
- Many contributions are missed when filtering by company email
- GitHub PRs accurately reflect actual contributions

### PRs 统计方法

**1. Web 界面查询 (推荐)**

访问 GitHub PR 搜索页面：
```
https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3A{username}+label%3Aintegrated+is%3Aclosed
```

示例：
- wenshao 的 Integrated PRs: https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Awenshao+label%3Aintegrated+is%3Aclosed
- shipilev 的 Integrated PRs: https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Ashipilev+label%3Aintegrated+is%3Aclosed

**2. GitHub CLI 查询**

```bash
# 获取所有 Integrated PRs 列表
gh pr list --repo openjdk/jdk --limit 300 \
  --search "author:{username} state:closed label:integrated" \
  --json number,title,closedAt,labels \
  --jq '.[] | "\(.number)|\(.title)|\(.closedAt)"'

# 统计总数
gh pr list --repo openjdk/jdk --limit 1000 \
  --search "author:{username} state:closed label:integrated" \
  --json number --jq 'length'
```

**3. GitHub API 查询**

```bash
# REST API
curl "https://api.github.com/search/issues?q=repo:openjdk/jdk+author:{username}+type:pr+label:integrated&per_page=100"

# 返回字段说明
# - number: PR 编号
# - title: PR 标题
# - closed_at: 合入时间 (用于时间线统计)
# - labels: 包含 "integrated" 标签
```

**4. 统计维度**

| 维度 | 说明 | 示例 |
|------|------|------|
| 总数 | Integrated PRs 总数 | 97 |
| 年度趋势 | 按年份/季度分组 | 2023: 20, 2024: 63 |
| 组件分布 | 按 label 分类 | core-libs, security |
| 影响类型 | 性能优化/重构/Bug修复 | 从标题推断 |

**5. 贡献者页面应包含**

```markdown
### 关键指标

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | {count} |
| **代码变更** | +xxx / -xxx |
| **主要领域** | xxx |
| **平均合入时间** | x.x 天 |

> **统计来源**: [GitHub Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+is%3Aclosed+label%3Aintegrated)

### Integrated PRs 统计

**年度趋势**
**按组件分布**
**最近 10 个 Integrated PRs**
```

**Timeline Statistics:**
- Use PR merge date (`closed_at` field), NOT commit date
- Group by year for timeline visualization

**Do NOT include:**
- Git commit counts
- Contributors without GitHub PRs
- Commit-based timelines

### Contributor PR Verification

**To verify all PRs are documented for a contributor:**

1. **Get all integrated PRs from GitHub:**
   ```bash
   gh pr list --repo openjdk/jdk --limit 300 \
     --search "author:{username} state:closed label:integrated" \
     --json number,title --jq '.[] | "\(.number) \(.title)"'
   ```

   Or use the web interface:
   ```
   https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3A{username}+is%3Aclosed+label%3Aintegrated+
   ```

2. **Compare with documented PRs:**
   - Extract Issue numbers from contributor page
   - Identify missing PRs
   - Categorize and add to appropriate section

3. **Update statistics:**
   - Recalculate category distribution
   - Update total PR count
   - Adjust percentages accordingly

## Output Language

Prefer responding in **English** for normal assistant messages and explanations.

Keep technical artifacts unchanged:
- Code blocks, CLI commands, file paths
- Stack traces, logs, JSON keys
- Identifiers and exact quoted text

## Link Verification Rule

**CRITICAL: All local links must be verified BEFORE committing changes.**

### Pre-Commit Link Verification Process

**When adding or modifying local links in markdown files:**

1. **Extract all local links from the file**:
   ```bash
   # Extract markdown links
   grep -oE '\]\([^)]+\.md\)' path/to/file.md | sort -u
   ```

2. **Verify each target file exists**:
   ```bash
   # Check if linked files exist
   for link in $(grep -oE '\]\(../../[^)]+\.md\)' file.md | sed 's/\](//;s/)//'); do
     target=$(realpath -m "$(dirname file.md)/$link")
     if [ ! -f "$target" ]; then
       echo "BROKEN: $link -> $target"
     fi
   done
   ```

3. **Common link patterns in this project**:
   | From | To | Pattern |
   |------|-----|---------|
   | `contributors/orgs/*.md` | `by-contributor/profiles/*.md` | `../../by-contributor/profiles/{name}.md` |
   | `by-contributor/profiles/*.md` | `contributors/orgs/*.md` | `/contributors/orgs/{org}.md` |
   | `by-version/jdk26/*.md` | `by-pr/*.md` | `../../by-pr/{issue}/{pr}.md` |
   | `anywhere` | `jeps/*.md` | `/jeps/{category}/jep-{num}.md` |

4. **Required verification steps**:
   - [ ] All `../../` relative paths resolved correctly
   - [ ] All `/absolute` paths point to existing files
   - [ ] Profile links use correct filenames (lowercase, hyphens)
   - [ ] Organization links use `orgs/` NOT `organizations/`

### Post-Push Verification

After pushing changes with links, verify via GitHub raw URL:
1. `https://raw.githubusercontent.com/wenshao/jdk_internal/main/{path/to/file}.md`
2. Only after successful verification can the task be marked as complete

### Common Link Errors

| Error | Wrong | Correct |
|-------|-------|---------|
| Wrong directory | `contributors/organizations/` | `contributors/orgs/` |
| Case sensitivity | `Thomas-Schatzl.md` | `thomas-schatzl.md` |
| Missing subdirectory | `by-pr/8336856.md` | `by-pr/8336/8336856.md` |
| Wrong relative depth | `../profiles/` | `../../by-contributor/profiles/` |

---

## Pre-Commit Content Verification

**CRITICAL: All content must be verified BEFORE committing changes.**

### Verification Checklist

#### 1. Local Links Verification ✅

```bash
# Extract and verify all local links
grep -oE '\]\([^)]+\.md\)' path/to/file.md | while read link; do
  # Extract path from markdown link
  path=$(echo "$link" | sed "s/](//;s/)//")
  # Resolve relative path
  if [[ "$path" == ../* ]]; then
    target="$(dirname path/to/file.md)/$path"
    if [ ! -f "$target" ]; then
      echo "BROKEN: $path"
    fi
  fi
done
```

**Required checks:**
- [ ] All `../../` relative paths resolved correctly
- [ ] All `/absolute` paths point to existing files
- [ ] Profile links use correct filenames (lowercase, hyphens)
- [ ] Organization links use `orgs/` NOT `organizations/`

#### 2. Contributor Attribution Verification ✅

**Before documenting contributors:**

| Check | Method | Source |
|-------|--------|--------|
| Organization | Check LinkedIn, GitHub bio, OpenJDK census | [OpenJDK Census](https://openjdk.org/census) |
| PR Count | GitHub PR search with `label:integrated` | GitHub PR Search |
| Role (Committer/Reviewer) | OpenJDK CFV mailing list | [OpenJDK Mailing Lists](https://mail.openjdk.org/) |
| Career History | LinkedIn profile | LinkedIn |

**Common attribution errors:**
- [ ] Contributor listed under wrong organization
- [ ] Using git commits instead of GitHub PRs for statistics
- [ ] Outdated organization (contributor changed jobs)

**Example verification:**
```bash
# Verify contributor's current organization
# 1. Check GitHub profile
gh api users/{username} --jq '.company, .bio'

# 2. Check OpenJDK census for email domain
# https://openjdk.org/census#{username}

# 3. Verify PR count
gh pr list --repo openjdk/jdk --limit 1000 \
  --search "author:{username} state:closed label:integrated" \
  --json number --jq 'length'
```

#### 3. JEP/Issue Reference Verification ✅

**For each JEP or Issue mentioned:**

| Check | Method |
|-------|--------|
| JEP exists | Access `https://openjdk.org/jeps/{number}` |
| Issue exists | Access `https://bugs.openjdk.org/browse/JDK-{number}` |
| Version correct | Cross-reference JEP target release |
| Lead/Owner correct | Check JEP "Owner" field |

**Common errors:**
- [ ] JEP number typo
- [ ] Wrong JDK version attribution
- [ ] JEP Lead attributed to wrong organization

#### 4. Technical Details Verification ✅

**For code examples and technical claims:**

| Check | Method |
|-------|--------|
| Code compiles | Test in appropriate JDK version |
| API exists | Check JDK API documentation |
| Performance claims | Verify with JMH results or PR discussion |
| File paths correct | Check against `../jdk` repository |

**Code example verification:**
```bash
# Verify file exists in JDK source
ls ../jdk/src/java.base/share/classes/java/lang/{ClassName}.java

# Verify method signature
grep -n "public static.*methodName" ../jdk/src/java.base/share/classes/java/lang/{ClassName}.java
```

#### 5. Date and Version Verification ✅

| Check | Method |
|-------|--------|
| JDK GA dates | [OpenJDK Releases](https://openjdk.org/projects/jdk/) |
| JEP delivery versions | JEP status page |
| PR merge dates | GitHub PR `closed_at` field |

**Version mapping:**
| JDK Version | GA Date | LTS |
|-------------|---------|-----|
| JDK 8 | 2014-03 | ✅ |
| JDK 11 | 2018-09 | ✅ |
| JDK 17 | 2021-09 | ✅ |
| JDK 21 | 2023-09 | ✅ |
| JDK 26 | 2026-03 | ❌ |

#### 6. External Links Verification ✅

**For each external URL:**

```bash
# Check if URL is accessible
curl -s -o /dev/null -w "%{http_code}" "{url}"
# Should return 200, not 404 or 403
```

**Common external link issues:**
- [ ] JBS issue links returning 404
- [ ] GitHub PR links outdated
- [ ] Blog post links broken

#### 7. Statistics Verification ✅

**For all numerical claims:**

| Statistic | Verification Method |
|-----------|---------------------|
| PR counts | GitHub PR search `label:integrated` |
| Code lines | `git diff --stat` |
| Performance % | JMH benchmark results in PR |
| Ranking | Cross-check with OpenJDK Census |

**Example:**
```bash
# Verify PR count
gh pr list --repo openjdk/jdk --limit 1000 \
  --search "author:{username} state:closed label:integrated" \
  --json number --jq 'length'

# Should match documented count
```

### Verification Commands Summary

```bash
# 1. Check local links
find . -name "*.md" -exec grep -l "\.\./" {} \; | head -5

# 2. Verify contributor organization
gh api users/{username} --jq '.company'

# 3. Verify PR count
gh pr list --repo openjdk/jdk --limit 1000 \
  --search "author:{username} state:closed label:integrated" \
  --json number --jq 'length'

# 4. Check external links
curl -s -o /dev/null -w "%{http_code}" "https://openjdk.org/jeps/{number}"

# 5. Verify file exists in JDK
ls ../jdk/src/java.base/share/classes/java/lang/String.java
```

### Post-Commit Verification

After pushing, verify via GitHub raw URL:
```
https://raw.githubusercontent.com/wenshao/jdk_internal/main/{path/to/file}.md
```

Only after **all** verifications pass can the task be marked as complete.
