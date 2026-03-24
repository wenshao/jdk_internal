# SAP

> PPC 移植、AIX 平台和 **OpenJDK LTS 维护最大贡献组织**

[← 返回组织索引](README.md)

---

## 代表性 PR

> 以下为各贡献者的代表性工作（最新 5 个）。完整列表见 GitHub 链接。

### Matthias Baesken (@MBaesken) — 492 PRs

| Bug ID | 标题 | 分析 |
|--------|------|------|
| [8379802](../../by-pr/8379/8379802.md) | 8379802: [AIX] unify DL_info struct and put it into a single header | [详情](../../by-pr/8379/8379802.md) |
| [8379416](../../by-pr/8379/8379416.md) | 8379416: AIX build fails if system (not GNU) date tool is in PATH | [详情](../../by-pr/8379/8379416.md) |
| [8379499](../../by-pr/8379/8379499.md) | 8379499: [AIX] headless-only build of libjawt.so fails | [详情](../../by-pr/8379/8379499.md) |
| [8379202](../../by-pr/8379/8379202.md) | 8379202: Support linktime-gc on Linux with clang | [详情](../../by-pr/8379/8379202.md) |
| [8378347](../../by-pr/8378/8378347.md) | 8378347: AIX version checks for 7.1 and 5.X are obsolete | [详情](../../by-pr/8378/8378347.md) |

→ [完整 PR 列表](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3AMBaesken+is%3Aclosed+label%3Aintegrated)

### Martin Doerr (@TheRealMDoerr) — 141 PRs

| Bug ID | 标题 | 分析 |
|--------|------|------|
| [8379448](../../by-pr/8379/8379448.md) | 8379448: [PPC64] Build without C2 broken after 8373595 | [详情](../../by-pr/8379/8379448.md) |
| [8378353](../../by-pr/8378/8378353.md) | 8378353: [PPC64] StringCoding.countPositives causes errors when the le | [详情](../../by-pr/8378/8378353.md) |
| [8378233](../../by-pr/8378/8378233.md) | 8378233: depends_only_on_test_impl() assertion hit after JDK-8347365 | [详情](../../by-pr/8378/8378233.md) |
| [8371820](../../by-pr/8371/8371820.md) | 8371820: Further AES performance improvements for key schedule generat | [详情](../../by-pr/8371/8371820.md) |
| [8368205](../../by-pr/8368/8368205.md) | 8368205: [TESTBUG] VectorMaskCompareNotTest.java crashes when MaxVecto | [详情](../../by-pr/8368/8368205.md) |

→ [完整 PR 列表](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3ATheRealMDoerr+is%3Aclosed+label%3Aintegrated)

---

## 目录

1. [概览](#1-概览)
2. [Top 贡献者](#2-top-贡献者)
3. [影响的模块](#3-影响的模块)
4. [主要领域](#4-主要领域)
5. [关键贡献](#5-关键贡献)
6. [SAP JVM (SapMachine)](#6-sap-jvm-sapmachine)
7. [贡献时间线](#7-贡献时间线)
8. [数据来源](#8-数据来源)
9. [相关链接](#9-相关链接)

---


## 1. 概览

SAP 是 OpenJDK 的长期贡献者，在**主线贡献**和 **LTS 维护**两个维度都有重要影响。SAP 团队在 LTS 维护分支 (jdk17u/21u/11u/25u/8u) 的贡献量位居所有组织之首。

| 指标 | 值 |
|------|-----|
| **主线 Integrated PRs** | 999+ |
| **LTS 维护 PRs** | **5,264** |
| **JMC 项目 PRs** | 34 (RealCLanger) |
| **总计 PRs** | **6,297+** |
| **贡献者数** | 9 |
| **活跃时间** | 2010+ - 至今 |
| **主要领域** | **LTS 维护最大贡献组织**, PPC 移植, AIX, HotSpot |
| **SapMachine** | [SAP SapMachine](https://sap.github.io/SapMachine/) |
| **JMC 贡献** | RealCLanger (31 PRs) |

> **统计说明**: 主线数据来自 `openjdk/jdk`，LTS 维护数据来自 `jdk17u-dev/jdk21u-dev/jdk11u-dev/jdk25u-dev/jdk8u-dev` 五个仓库。统计时间: 2026-03-24。

---

## 2. Top 贡献者

### 主线 + LTS 维护综合统计

| 排名 | 贡献者 | GitHub | 主线 PRs | LTS 维护 PRs | 总计 | 角色 | 档案 |
|------|--------|--------|----------|-------------|------|------|------|
| 1 | Goetz Lindenmaier | [@GoeLin](https://github.com/GoeLin) | 6 | **3,915** | **3,921** | Reviewer | [详情](../../by-contributor/profiles/goetz-lindenmaier.md) |
| 2 | Matthias Baesken | [@MBaesken](https://github.com/MBaesken) | 492 | 499 | 991 | Reviewer | [详情](../../by-contributor/profiles/matthias-baesken.md) |
| 3 | Martin Doerr | [@TheRealMDoerr](https://github.com/TheRealMDoerr) | 141 | 429 | 570 | Committer | [详情](../../by-contributor/profiles/martin-doerr.md) |
| 4 | Christoph Langer | [@RealCLanger](https://github.com/RealCLanger) | 78 | 277 | 355 | Committer | [详情](../../by-contributor/profiles/christoph-langer.md) |
| 5 | Richard Reingruber | [@reinrich](https://github.com/reinrich) | 72 | 30 | 102 | Reviewer | [详情](../../by-contributor/profiles/richard-reingruber.md) |
| 6 | Thomas Stuefe | [@tstuefe](https://github.com/tstuefe) | 140 | 71 | 211 | Contributor | [详情](../../by-contributor/profiles/thomas-stuefe.md) |
| 7 | Johannes Bechberger | [@parttimenerd](https://github.com/parttimenerd) | 28 | 27 | 55 | Contributor | — |
| 8 | David Briemann | [@dbriemann](https://github.com/dbriemann) | 26 | 10 | 36 | Committer | [详情](../../by-contributor/profiles/david-briemann.md) |
| 9 | Volker Simonis | [@simonis](https://github.com/simonis) | 16 | 6 | 22 | Contributor | — |

**总计**: 主线 999+ PRs + LTS 维护 5,264 PRs = **6,263 PRs**

### LTS 维护分支分布

| 贡献者 | jdk17u | jdk21u | jdk11u | jdk25u | jdk8u |
|--------|--------|--------|--------|--------|-------|
| [GoeLin](../../by-contributor/profiles/goetz-lindenmaier.md) | 1,951 | 1,114 | 785 | 65 | 0 |
| [MBaesken](../../by-contributor/profiles/matthias-baesken.md) | 212 | 165 | 95 | 27 | 0 |
| [TheRealMDoerr](../../by-contributor/profiles/martin-doerr.md) | 187 | 89 | 149 | 4 | 0 |
| [RealCLanger](../../by-contributor/profiles/christoph-langer.md) | 65 | 21 | 190 | 1 | 0 |
| 其他 | 78 | 23 | 29 | 8 | 6 |
| **合计** | **2,493** | **1,412** | **1,248** | **105** | **6** |

> **Goetz Lindenmaier** 一人承担了 SAP 维护贡献的 74%，是 OpenJDK 生态中最重要的 LTS 维护者。

---

## 3. 影响的模块

| 模块 | 文件数 | 说明 |
|------|--------|------|
| PPC 移植 (旧) | 42 | PowerPC 架构支持 (旧路径) |
| PPC 移植 (新) | 30 | PowerPC 架构支持 (新路径) |
| C2 编译器 | 22 | 服务端编译器 |
| HotSpot Runtime | 15 | JVM 运行时 |
| AIX 平台 | 14 | AIX 操作系统支持 |
| ADLC | 12 | 架构描述语言编译器 |
| 构建系统 | 10 | Autoconf 构建配置 |

---

## 4. 主要领域

### PowerPC (PPC) 移植

SAP 主导 PowerPC 架构的 OpenJDK 移植：

- **PPC64**: 64 位 PowerPC 支持
- **PPC64LE**: 小端模式支持
- **JIT 支持**: C2 编译器 PPC 后端

### AIX 平台

- AIX 操作系统支持
- AIX 特定的构建配置
- AIX 线程和内存管理

### HotSpot Runtime

- HotSpot 运行时改进
- GC 和内存管理
- 诊断和监控工具

### 构建系统

- 跨平台构建
- Windows 构建
- AIX 构建

---

## 5. 关键贡献

### 构建系统 (Matthias Baesken, 492 主线 PRs)

代表性贡献: AIX 平台支持, 跨平台构建修复, clang 支持, Windows 构建改进。详见 [MBaesken 代表性 PR](#代表性-pr)。

### HotSpot Runtime (Goetz Lindenmaier)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8237354 | HotSpot Runtime 服务层重构 | 架构改进 |
| 8278945 | TLAB 优化 | 性能优化 |

---

## 6. SAP JVM (SapMachine)

SAP 维护自己的 JVM 发行版 SapMachine：

| 特性 | 说明 |
|------|------|
| 基于 | OpenJDK |
| 支持 | 长期支持版本 |
| 特点 | 企业级服务性增强 |
| 许可 | GPLv2 |

**额外特性**:
- 增强的诊断能力
- 更好的错误报告
- 企业级监控
- SapMachine Vitals (OS 和 JVM 统计)

**创始人**: Thomas Stuefe (现为 Red Hat 员工)

---

## 7. 贡献规模对比

SAP 在 OpenJDK 生态中的角色独特——**主线创新 + LTS 维护**双轮驱动：

| 维度 | PRs | 说明 |
|------|-----|------|
| **主线 (openjdk/jdk)** | 999+ | PPC 移植, AIX, 构建系统, HotSpot |
| **jdk17u-dev** | 2,493 | 最大 LTS 维护目标 |
| **jdk21u-dev** | 1,412 | 当前 LTS |
| **jdk11u-dev** | 1,248 | 历史 LTS |
| **jdk25u-dev** | 105 | 新兴维护 |
| **jdk8u-dev** | 6 | 少量 |

> SAP 的 LTS 维护贡献 (5,264 PRs) 超过了 Red Hat (770) 和 Alibaba (559) 的总和。

---



## 审查者网络

> SAP 的 PR 被以下审查者审查最多 (共 3,851 次审查)

| 审查者 | 组织 | 审查次数 |
|--------|------|----------|
| TheRealMDoerr | SAP | 581 |
| MBaesken | SAP | 476 |
| RealLucy | — | 287 |
| RealCLanger | SAP | 205 |
| tstuefe | Red Hat | 197 |
| dholmes-ora | Oracle | 176 |
| reinrich | SAP | 160 |
| phohensee | Oracle | 154 |

### 审查组织分布

| 审查者组织 | 次数 | 占比 |
|-----------|------|------|
| SAP | 1526 | 40% |
| Oracle | 1261 | 33% |
| Red Hat | 333 | 9% |
| Amazon | 156 | 4% |
| Datadog | 30 | 1% |

---

## 8. 数据来源

- **主线**: GitHub PR search `repo:openjdk/jdk author:xxx label:integrated`
- **LTS 维护**: CSV 数据 `jdk17u-dev/jdk21u-dev/jdk11u-dev/jdk25u-dev/jdk8u-dev`
- **统计时间**: 2026-03-24

---

## 9. 相关链接

- [SAP SapMachine](https://sap.github.io/SapMachine/)
- [SAP GitHub](https://github.com/SAP/SapMachine)
- [SapMachine Wiki](https://github.com/SAP/SapMachine/wiki)
- [SAP OpenJDK](https://openjdk.org/groups/hotspot/)

[→ 返回组织索引](README.md)
