# Datadog

> Compact Object Headers (JEP 519) 主导者, JFR/BTrace 贡献

[← 返回组织索引](README.md)

---

## 代表性 PR

> 以下为各贡献者的代表性工作（最新 5 个）。完整列表见 GitHub 链接。

### Roman Kennke (@rkennke) — 106 PRs

| Bug ID | 标题 | 分析 |
|--------|------|------|
| [8355319](../../by-pr/8355/8355319.md) | 8355319: Update Manpage for Compact Object Headers (Production) | [详情](../../by-pr/8355/8355319.md) |
| [8355319](../../by-pr/8355/8355319.md) | 8355319: Update Manpage for Compact Object Headers (Production) | [详情](../../by-pr/8355/8355319.md) |
| [8357370](../../by-pr/8357/8357370.md) | 8357370: Export supported GCs in JVMCI | [详情](../../by-pr/8357/8357370.md) |
| [8356329](../../by-pr/8356/8356329.md) | 8356329: Report compact object headers in hs_err | [详情](../../by-pr/8356/8356329.md) |
| [8356266](../../by-pr/8356/8356266.md) | 8356266: Fix non-Shenandoah build after JDK-8356075 | [详情](../../by-pr/8356/8356266.md) |

→ [完整 PR 列表](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Arkennke+is%3Aclosed+label%3Aintegrated)

---

## 目录

1. [概览](#1-概览)
2. [贡献者](#2-贡献者)
3. [JEP 贡献](#3-jep-贡献)
4. [数据来源](#4-数据来源)
5. [相关链接](#5-相关链接)

---

## 1. 概览

Datadog 通过关键贡献者参与 OpenJDK 开发，最突出的是 **Roman Kennke 主导的 JEP 519 (Compact Object Headers)**，该特性将 Java 对象头从 128 位压缩到 64 位，在 JDK 25 中成为正式功能。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 113+ |
| **贡献者数** | 2 |
| **活跃时间** | 2020 - 至今 |
| **主要领域** | Compact Object Headers, Shenandoah GC, JFR, BTrace |
| **源码版权** | 19 个文件含 Datadog 版权 |
| **里程碑** | [JEP 519: Compact Object Headers](https://openjdk.org/jeps/519) (JDK 25) |

---

## 2. 贡献者

| 排名 | 贡献者 | GitHub | PRs | 角色 | 主要领域 | 档案 |
|------|--------|--------|-----|------|----------|------|
| 1 | [Roman Kennke](../../by-contributor/profiles/roman-kennke.md) | [@rkennke](https://github.com/rkennke) | 107 | Reviewer | Compact Object Headers, Shenandoah GC | [详情](../../by-contributor/profiles/roman-kennke.md) |
| 2 | Jaroslav Bachorik | [@jbachorik](https://github.com/jbachorik) | 6 | Committer | JFR, BTrace | [详情](../../by-contributor/profiles/jaroslav-bachorik.md) |

**总计**: 113+ PRs (1 Reviewer + 1 Committer)

### Roman Kennke — JEP 519 Lead, Project Lilliput

Roman Kennke 是 OpenJDK **Project Lilliput** 的项目负责人，主导了 Compact Object Headers 从实验 (JEP 450, JDK 24) 到正式功能 (JEP 519, JDK 25) 的全过程。他之前在 Red Hat 主导 Shenandoah GC 开发，后转至 Datadog。

- **位置**: 瑞士苏黎世
- **职业轨迹**: Red Hat (Shenandoah GC) → Amazon → **Datadog** (现)
- **年度贡献**: 2020 (22) → 2021 (36) → 2022 (14) → 2023 (11) → 2024 (13) → 2025 (11)
- **JEP 519 性能**: SPECjbb2015 堆空间减少 22%, CPU 时间减少 8%, GC 次数减少 15%

### Jaroslav Bachorik — JFR/BTrace

Jaroslav Bachorik 是 [BTrace](https://github.com/btraceio/btrace) 项目创始人，专注于 JFR 和 JVM 诊断工具。位于捷克布拉格。

---

## 3. JEP 贡献

| JEP | 标题 | Lead | 版本 |
|-----|------|------|------|
| [JEP 450](https://openjdk.org/jeps/450) | Compact Object Headers (Experimental) | Roman Kennke | JDK 24 |
| [JEP 519](https://openjdk.org/jeps/519) | Compact Object Headers | Roman Kennke | JDK 25 |

---

## 4. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-23

---

## 5. 相关链接

- [Datadog 官网](https://www.datadoghq.com/)
- [JEP 519: Compact Object Headers](https://openjdk.org/jeps/519)
- [Project Lilliput](https://openjdk.org/projects/lilliput/)
- [BTrace Project](https://github.com/btraceio/btrace)

[← 返回组织索引](README.md)

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-23
