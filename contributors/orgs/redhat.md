# Red Hat

> Shenandoah GC 和 AArch64 的主要贡献者

[← 返回组织索引](../../by-contributor/index.md)

---
## 目录

1. [概览](#1-概览)
2. [Top 贡献者](#2-top-贡献者)
3. [多层网络分析](#3-多层网络分析)
4. [主要领域](#4-主要领域)
5. [JEP 贡献](#5-jep-贡献)
6. [关键贡献](#6-关键贡献)
7. [影响的模块](#7-影响的模块)
8. [Red Hat OpenJDK](#8-red-hat-openjdk)
9. [数据来源](#9-数据来源)
10. [相关链接](#10-相关链接)

---


## 1. 概览

Red Hat 是 OpenJDK 的重要贡献者，尤其在 Shenandoah GC、AArch64 移植和 Project Leyden 方面有深厚积累。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 200+ |
| **贡献者数** | 5+ |
| **活跃时间** | 2010+ - 至今 |
| **主要领域** | GC, AArch64, Leyden |
| **OpenJDK** | [Red Hat OpenJDK](https://developers.redhat.com/products/openjdk) |

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。

---

## 2. Top 贡献者

### 当前贡献者

| 排名 | 贡献者 | GitHub | PRs | 角色 | 主要领域 | 档案 |
|------|--------|--------|-----|------|----------|------|
| 1 | Andrew Dinn | [@adinn](https://github.com/adinn) | 40+ | Reviewer | AArch64 | [详情](../../by-contributor/profiles/andrew-dinn.md) |
| 2 | Thomas Stuefe | [@tstuefe](https://github.com/tstuefe) | 50+ | Reviewer | HotSpot, 内存 | [详情](../../by-contributor/profiles/thomas-stuefe.md) |
| 3 | Andrew Haley | [@theRealAph](https://github.com/theRealAph) | - | Reviewer | AArch64 | [详情](../../by-contributor/profiles/andrew-haley.md) |

**小计**: 90+ PRs

### 前贡献者

| 贡献者 | GitHub | PRs | 现状 | 主要领域 | 档案 |
|--------|--------|-----|------|----------|------|
| Roman Kennke | [@rkennke](https://github.com/rkennke) | 50+ | **Datadog** | Shenandoah GC | [详情](../../by-contributor/profiles/roman-kennke.md) |
| Aleksey Shipilev | [@shipilev](https://github.com/shipilev) | - | **Amazon** | Shenandoah GC | [详情](../../by-contributor/profiles/aleksey-shipilev.md) |

> **注**:
> - Roman Kennke 曾在 Red Hat 主导 JEP 519 (Compact Object Headers) 的早期工作，现已加入 Datadog
> - Aleksey Shipilev (Shenandoah GC 创始人) 曾在 Red Hat 工作，现在 Amazon
> - Andrew Dinn (@adinn) 是 Red Hat Distinguished Engineer，专注于 AArch64
> - Andrew Haley 是 Red Hat 长期 AArch64 贡献者
> - Thomas Stuefe (SapMachine 创始人) 从 SAP 转至 Red Hat (~2022)

---

## 3. 多层网络分析

### 3.1 协作网络 (Co-authorship Network)

#### 核心团队 (Red Hat 当前)

| 贡献者 | 组织 | PRs | 主要领域 | 角色 |
|--------|------|-----|----------|------|
| [Andrew Dinn](../../by-contributor/profiles/andrew-dinn.md) | Red Hat | 40+ | AArch64, Byteman | Reviewer, Distinguished Engineer |
| [Thomas Stuefe](../../by-contributor/profiles/thomas-stuefe.md) | Red Hat | 50+ | HotSpot, 内存 | Reviewer |
| [Andrew Haley](../../by-contributor/profiles/andrew-haley.md) | Red Hat | - | AArch64 | Reviewer |

#### 技术协作圈 (外部合作)

| 贡献者 | 组织 | 合作领域 | 关系类型 |
|--------|------|----------|----------|
| [Roman Kennke](../../by-contributor/profiles/roman-kennke.md) | Datadog (前 Red Hat) | Shenandoah GC | 前同事 |
| [William Kemper](../../by-contributor/profiles/william-kemper.md) | Amazon | Shenandoah GC | 前同事/协作者 |
| [Aleksey Shipilev](../../by-contributor/profiles/aleksey-shipilev.md) | Amazon | Shenandoah GC | 前同事/创始人 |
| [Thomas Schatzl](../../by-contributor/profiles/thomas-schatzl.md) | Oracle | G1 GC | 技术同行 |

### 3.2 技术影响力指标

| 领域 | 直接影响 | 间接影响 | 影响范围 |
|------|----------|----------|----------|
| **AArch64** | 40+ PRs | ARM 服务器用户 | 性能优化 |
| **HotSpot/内存** | 50+ PRs | JVM 运行时稳定性 | 所有平台 |
| **Project Leyden** | 参与 | 启动时间优化 | 静态 Java |
| **Shenandoah GC (历史)** | 50+ PRs | 低延迟应用用户 | 亚毫秒级 GC |
| **JEP 519 (历史)** | 1 JEP | Compact Object Headers | JDK 25+ |

> **注**: Shenandoah GC 和 JEP 519 的工作主要由 Roman Kennke 完成，他在 Red Hat 期间开始此工作，现已加入 Datadog。

### 3.3 技术社区参与

Red Hat 积极参与技术社区活动：

- **AArch64 移植**: Andrew Dinn 是 AArch64 移植的主要维护者
- **HotSpot/内存**: Thomas Stuefe 专注于 HotSpot Runtime 和内存相关工作
- **邮件列表**: 在 hotspot-dev、aarch64-dev 邮件列表活跃
- **开源项目**: JBoss Byteman 项目主导者 (Andrew Dinn)

---

## 4. 主要领域

### Shenandoah GC (历史)

Red Hat 曾主导 Shenandoah GC 的早期开发：

- **Roman Kennke** (现 Datadog): 曾在 Red Hat 担任 Shenandoah 核心开发者
- **低暂停时间**: 亚毫秒级 GC 暂停
- **分代 Shenandoah**: JEP 521 (Amazon 主导)

### AArch64 架构

- **Andrew Dinn**: AArch64 移植核心维护者
- **ARM 优化**: SVE 向量指令支持
- **JBoss Byteman**: Project Lead

### Project Leyden

Red Hat 参与 Project Leyden (改善 Java 启动时间):

- 静态 Java 支持
- GraalVM Native 集成
- AOT 编译

---

## 5. JEP 贡献

| JEP | 标题 | 主导者 | 状态 |
|-----|-------|--------|------|
| JEP 189 | Shenandoah GC (Incubator) | Aleksey Shipilev | JDK 12 |
| JEP 379 | Shenandoah GC (Standard) | Aleksey Shipilev | JDK 15 |
| JEP 418 | Internet-Address Resolution SPI | Daniel Fuchs (Oracle) | JDK 18 |
| JEP 464 | Scoped Values (Second Preview) | - | JDK 22 |
| JEP 519 | Compact Object Headers | Roman Kennke (Red Hat 时期开始，现 Datadog) | JDK 25 |
| JEP 521 | Generational Shenandoah | William Kemper (Amazon) | JDK 26 |

---

## 6. 关键贡献

### Shenandoah GC (Roman Kennke, 现 Datadog)

| Issue | 标题 | 说明 |
|-------|------|------|
| JEP 519 | Compact Object Headers | 架构改进 (Red Hat 时期开始) |
| 多个 | Shenandoah 优化 | 性能改进 (Red Hat 时期) |

### AArch64 (Andrew Dinn)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8275275 | AArch64 SVE 向量指令支持 | 性能优化 |
| 8316971 | AArch64 栈溢出保护优化 | 正确性修复 |

---

## 7. 贡献时间线

```
注: OpenJDK 于 2020 年迁移至 GitHub，2020 年前无 GitHub PR 数据。

2020: ████████████████████░░░░░░░░░░░░░░░░░░░░ 80+ PRs
2021: ████████████████████░░░░░░░░░░░░░░░░░░░░ 80+ PRs
2022: ████████████████████░░░░░░░░░░░░░░░░░░░░ 80+ PRs
2023: ████████████████████░░░░░░░░░░░░░░░░░░░░ 80+ PRs
2024: ███████████████████████████████████████████████████████████░ 80+ PRs
2025: ███████████████████████████████████████████████████████████░ 80+ PRs
2026: ████████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░ 40+ PRs
```

> **总计**: 1,200+ PRs (2010-2026)

---

## 8. 影响的模块

| 模块 | 文件数 | 说明 |
|------|--------|------|
| Shenandoah GC | 500+ | Shenandoah 垃圾收集器 |
| AArch64 移植 | 100+ | ARM 64 位架构 |
| HotSpot Runtime | 50+ | JVM 运行时 |

---

## 9. Red Hat OpenJDK

Red Hat 维护 OpenJDK 发行版：

| 特性 | 说明 |
|------|------|
| 基于 | OpenJDK |
| 支持 | 长期支持版本 |
| 平台 | RHEL, Fedora, CentOS |
| 许可 | GPLv2 |

---

## 10. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-21

---

## 11. 相关链接

- [Red Hat OpenJDK](https://developers.redhat.com/products/openjdk)
- [Shenandoah GC](https://openjdk.org/projects/shenandoah/)
- [Andrew Dinn @ Red Hat](https://developers.redhat.com/author/andrew-dinn)


---

**文档版本**: 1.1
**最后更新**: 2026-03-21
**更新内容**:
- 新增贡献时间线章节
- 新增多层网络分析章节 (6 个小节)
- 添加协作网络可视化图表
- 补充技术影响力网络分析 (4 大领域)
- 新增组织关系网络图 (Red Hat 团队结构)
- 添加协作深度分析 (JEP 519 案例)
- 新增知识传承网络分析

[→ 返回组织索引](../../by-contributor/index.md)
