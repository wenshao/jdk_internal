# Joe Darcy

> **GitHub**: [@jddarcy](https://github.com/jddarcy)
> **OpenJDK**: [@darcy](https://openjdk.org/census#darcy)
> **Organization**: Oracle (Member of Technical Staff, Java Platform Group)
> **LinkedIn**: [jddarcy](https://www.linkedin.com/in/jddarcy)
> **Inside.java**: [JoeDarcy](https://inside.java/u/JoeDarcy/)
> **Education**: Stanford University (HCP Master's)

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [主要贡献](#3-主要贡献)
4. [分析的 PR](#4-分析的-pr)
5. [外部资源](#5-外部资源)

---


## 1. 概述

Joe Darcy 是 Oracle 的长期 JDK 开发者，在 Java 平台上工作超过 20 年 (Sun Microsystems -> Oracle)。他被称为 "Java Floating-Point Czar"，负责 Java 数值计算，同时领导 Compatibility and Specification Review (CSR) 工作组，负责审查 JDK 所有接口变更、新 API、命令行选项等，每年审查数百项变更。他的贡献涵盖核心库、数值计算、Project Coin、基础设施迁移等多个领域。

> **数据来源**: [Inside.java](https://inside.java/u/JoeDarcy/), [GitHub](https://github.com/jddarcy), [Oracle Blog](https://blogs.oracle.com/authors/joe-darcy)

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Joseph D. Darcy (Joe Darcy) |
| **当前组织** | Oracle (Java Platform Group) |
| **GitHub** | [@jddarcy](https://github.com/jddarcy) |
| **OpenJDK** | [@darcy](https://openjdk.org/census#darcy) |
| **角色** | JDK Reviewer, CSR Lead |
| **教育** | Stanford University (HCP Master's program) |
| **专长** | Math Libraries, FDLIBM, Numerics, Project Coin, CSR, 基础设施 |
| **称号** | "Java Floating-Point Czar" |
| **Commits (openjdk/jdk)** | 1,194+ |
| **PRs (integrated)** | 351 |
| **工作经验** | Sun Microsystems → Oracle (20+ years) |
| **Inside.java** | [JoeDarcy](https://inside.java/u/JoeDarcy/) |
| **Oracle Blog** | [Joe Darcy](https://blogs.oracle.com/authors/joe-darcy) |

---

## 3. 主要贡献

### JEP 贡献 (Owner/Author)

| JEP | 标题 | JDK 版本 |
|-----|------|----------|
| JEP 213 | Milling Project Coin | JDK 9 |
| JEP 212 | Resolve Lint and Doclint Warnings | JDK 9 |
| JEP 211 | Elide Deprecation Warnings on Import Statements | JDK 9 |
| JEP 296 | Consolidate the JDK Forest into a Single Repository | JDK 10 |
| JEP 306 | Restore Always-Strict Floating-Point Semantics | JDK 17 |
| JEP 357 | Migrate from Mercurial to Git | JDK 16 |
| JEP 369 | Migrate to GitHub | JDK 16 |

### Project Coin (JSR 334)

Joe Darcy 领导的 Project Coin 为 JDK 7 引入了多项小型语言改进:
- Strings in switch
- 二进制字面量和下划线分隔
- Multi-catch 和更精确的 rethrow
- Diamond 语法 (`<>`)
- try-with-resources
- @SafeVarargs

### JDK 26 (2025-2026)

| PR/Issue | 标题 | 角色 |
|----------|------|------|
| [JDK-8362376](../../by-pr/8362/8362376.md) | 在 Java FDLIBM 实现中使用 @Stable 注解 | Author |

### 核心优化领域

| 领域 | 说明 |
|------|------|
| **数值计算** | FDLIBM、Math 库优化、strictfp 语义 |
| **CSR Lead** | Compatibility and Specification Review 工作组负责人 |
| **基础设施** | JDK 仓库合并、Git/GitHub 迁移 |
| **语言改进** | Project Coin (JDK 7), Milling Project Coin (JDK 9) |

---

## 4. 分析的 PR

### JDK-8362376: 在 Java FDLIBM 实现中使用 @Stable 注解

在 FDLIBM (Freely Distributable LIBM) 实现中应用 @Stable 注解，启用 JIT 优化，实现 5-15% 的性能提升。

**关键改进**:
- 在查找表数组上添加 `@Stable` 注解
- 启用边界检查消除
- 启用常量折叠
- 改善循环向量化

**技术细节**:
- `__libm_sincos_table` 数组添加 @Stable
- `__libm_exp_table` 数组添加 @Stable
- JIT 可以将数组元素视为常量

**性能影响**:
- 三角函数: +5-10%
- 指数/对数: +3-8%
- 密集计算: +10-15%

**文档**: [详细分析](../../by-pr/8362/8362376.md)

---

## 5. 外部资源

### 链接

- **GitHub**: [@jddarcy](https://github.com/jddarcy)
- **OpenJDK Census**: [darcy](https://openjdk.org/census#darcy)
- **Inside.java**: [JoeDarcy](https://inside.java/u/JoeDarcy/)
- **Oracle Blog**: [Joe Darcy](https://blogs.oracle.com/authors/joe-darcy)
- **LinkedIn**: [jddarcy](https://www.linkedin.com/in/jddarcy)
- **ResearchGate**: [Joseph Darcy](https://www.researchgate.net/profile/Joseph-Darcy)
- **Blog Archive**: [BlogsSunComArchive](https://github.com/jddarcy/BlogsSunComArchive)
- **JDK-8362376 Thread**: [Mail Archive](https://mail.openjdk.org/archives/list/jdk-changes@openjdk.org/thread/6W4JAMJLVD4AVRUTCOWAYDLBI5I5PTFH/)

---

> **文档版本**: 2.0
> **最后更新**: 2026-03-22
> **更新内容**:
> - 修正描述: "Java Floating-Point Czar", 非"杰出工程师"
> - 添加 CSR Lead 角色 (Compatibility and Specification Review)
> - 添加完整 JEP 贡献列表 (7 个 JEP)
> - 添加 Project Coin (JSR 334) 详细功能列表
> - 添加 GitHub 统计: 1,194+ commits, 351 integrated PRs
> - 添加 Inside.java, Oracle Blog, ResearchGate 链接
> - 添加 GitHub handle @jddarcy


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 481 |
| **活跃仓库数** | 2 |
