# Amazon

> Corretto 团队，Shenandoah GC 和 AArch64 优化

[← 返回组织索引](../../by-contributor/index.md)

---
## 目录

1. [概览](#1-概览)
2. [贡献者](#2-贡献者)
3. [主要领域](#3-主要领域)
4. [影响的模块](#4-影响的模块)
5. [贡献时间线](#5-贡献时间线)
6. [JEP 贡献](#6-jep-贡献)
7. [Amazon Corretto](#7-amazon-corretto)
8. [相关 PR 分析文档](#8-相关-pr-分析文档)
9. [数据来源](#9-数据来源)
10. [相关链接](#10-相关链接)

---


## 1. 概览

Amazon 通过 Corretto 团队参与 OpenJDK 开发，专注于 Shenandoah GC、AArch64 架构优化和编译器改进。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 160+ |
| **贡献者数** | 3 |
| **活跃时间** | 2020 - 至今 |
| **主要领域** | Shenandoah GC, AArch64, C2 编译器 |
| **Corretto** | [Amazon Corretto](https://aws.amazon.com/corretto/) |

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。OpenJDK Committer 使用 `@openjdk.org` 邮箱提交代码，因此 git commits 按邮箱统计不准确。

---

## 2. 贡献者

| 排名 | 贡献者 | GitHub | PRs | 角色 | 主要领域 | 档案 |
|------|--------|--------|-----|------|----------|------|
| 1 | William Kemper | [@earthling-amzn](https://github.com/earthling-amzn) | 123 | Reviewer | Shenandoah GC | [详情](../../by-contributor/profiles/william-kemper.md) |
| 2 | Nick Gasson | [@benty-amzn](https://github.com/benty-amzn) | 15 | Reviewer | AArch64 | [详情](../../by-contributor/profiles/nick-gasson.md) |

**小计**: 138 PRs

> **注**: 
> - Andrew Dinn (@adinn) 是 **Red Hat** 员工，不属于 Amazon
> - David Beaumont (@dbeaumont) 是 **Oracle** 员工，不属于 Amazon

---

## 3. 主要领域

### Shenandoah GC (William Kemper)

William Kemper 是 **JEP 521: Generational Shenandoah** 的主要实现者：

| Issue | 标题 | 说明 |
|-------|------|------|
| 8354078 | Implement JEP 521: Generational Shenandoah | **核心贡献** |
| 8370039 | GenShen: array copy SATB barrier improvements | 性能优化 |
| 8368152 | Shenandoah: Incorrect behavior at end of degenerated cycle | 正确性修复 |
| 8264851 | Shenandoah: Rework control loop mechanics | 架构改进 |
| 8350898 | Shenandoah: Eliminate final roots safepoint | 性能优化 |

### AArch64 优化 (Nick Gasson)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8293100 | AArch64 C2 编译器后端优化 | 性能优化 |
| 8319254 | 向量指令自动向量化改进 | 性能优化 |
| 8330456 | 特定微架构优化 | 性能优化 |

---

## 4. 影响的模块

| 模块 | 文件数 | 说明 |
|------|--------|------|
| Shenandoah GC | 80+ | Shenandoah 垃圾收集器 |
| AArch64 移植 | 30+ | ARM 64 位架构 |
| C2 编译器 | 20+ | 服务端编译器 |
| HotSpot Runtime | 15+ | JVM 运行时 |

---

## 5. 贡献时间线

```
2020: ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 3 PRs
2021: ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 5 PRs
2022: ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 8 PRs
2023: ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 12 PRs
2024: ███████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░ 55 PRs
2025: ███████████████████████████████████████████████████████████████░ 55 PRs
```

> **总计**: 138 PRs (2020-2025)

---

## 6. JEP 贡献

| JEP | 标题 | 主导者 | 状态 |
|-----|-------|--------|------|
| JEP 521 | Generational Shenandoah | William Kemper | JDK 26 |

---

## 7. Amazon Corretto

Amazon 维护自己的 JDK 发行版 Corretto：

| 特性 | 说明 |
|------|------|
| 基于 | OpenJDK |
| 支持 | 长期支持 (LTS) |
| 许可 | GPLv2 |
| 平台 | Linux, Windows, macOS |

**特点**:
- 免费生产就绪
- 长期支持
- AWS 优化
- 安全补丁

---

## 8. 相关 PR 分析文档

### Shenandoah GC (William Kemper)

| PR | 标题 | 分析文档 |
|----|------|----------|
| JDK-8354078 | Implement JEP 521: Generational Shenandoah | [详情](../../by-pr/8354/8354078.md) |
| JDK-8370039 | GenShen: SATB barrier improvements | [详情](../../by-pr/8370/8370039.md) |

### AArch64 (Nick Gasson)

| PR | 标题 | 分析文档 |
|----|------|----------|
| JDK-8293100 | AArch64 C2 backend optimization | - |

---

## 9. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-21

---

## 10. 相关链接

- [Amazon Corretto](https://aws.amazon.com/corretto/)
- [Corretto GitHub](https://github.com/corretto)
- [Corretto 文档](https://docs.aws.amazon.com/corretto/)

[→ 返回组织索引](../../by-contributor/index.md)
