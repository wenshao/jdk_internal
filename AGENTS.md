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
│   └── jdk26/             # JDK 26 (GA 2025-09-16)
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
| JDK 26 | 最高 | 已发布 (GA 2025-09-16)，详细追踪 |

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

## Contribution Statistics Principles

**IMPORTANT: Use GitHub Integrated PRs as the ONLY metric for contribution statistics.**

**Why NOT use git commits?**
- OpenJDK Committers use `@openjdk.org` email for commits
- Git commits by company email domain is inaccurate
- Many contributions are missed when filtering by company email
- GitHub PRs accurately reflect actual contributions

**Query Method:**
```
https://api.github.com/search/issues?q=repo:openjdk/jdk+author:{username}+type:pr+label:integrated
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
