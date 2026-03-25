# PR 分析索引

> **22,560** 个 PR 分析文档，覆盖 P1-P4 优先级，93% 含 GitHub 描述

---

## 概览

| 指标 | 值 |
|------|-----|
| **PR 分析文档** | 22,560 |
| **有深度内容 (>1.5KB)** | 21,195 (93%) |
| **JEP 实现 PR** | 130+ (含 JEP 详情) |
| **P1 PR** | 159 (含 body + files + comments) |
| **P2 PR** | 1,049 (含 body + files + comments) |
| **P3 PR** | 4,312 (含 body + stats) |
| **P4 PR** | 16,286 (含 body + stats) |
| **标注 backport 信息** | 4,545 |
| **标注 regression** | 863 |
| **数据来源** | openjdk/jdk 24,868 Integrated PRs |

## 数据字段

每个 PR 文档包含：

- **基本信息**: Issue 链接, PR 链接, Author, 组织, 创建/合入日期
- **审查**: 审查天数, 审查者列表
- **JBS 数据**: 优先级, 组件, 模块, Fix Version
- **代码变更**: additions/deletions/changed files (P1/P2)
- **PR 描述**: GitHub PR body 全文 (93%)
- **变更文件列表**: 前 15 个文件详情 (P1/P2)
- **审查讨论**: 前 3 条 review comments (P1/P2)
- **Backport 追踪**: 被 backport 到哪些 LTS 版本
- **JEP 详情**: JEP 编号/负责人/状态/目标版本 (JEP PRs)

## 浏览方式

- **按 Bug ID**: `by-pr/{前4位}/{bug_id}.md`，如 [JDK-8336856](8336/8336856.md)
- **按优先级**: [回归 Bug 分析](../contributors/stats/regression-analysis.md) | [Release Notes](../contributors/stats/release-notes.md)
- **按 Backport**: [Backport 追踪](../contributors/stats/backport-tracking.md)
- **按 JEP**: [JEP 索引](../jeps/)
- **完整 CSV**: [all-integrated-prs.csv](all-integrated-prs.csv) (22 字段)

---

> **最后更新**: 2026-03-25
