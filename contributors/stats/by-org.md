# 按组织分类

> OpenJDK 贡献者按所属组织统计 (基于 GitHub Integrated PRs)

---
## 目录

1. [数据来源说明](#1-数据来源说明)
2. [组织贡献总览](#2-组织贡献总览)
3. [Oracle](#3-oracle)
4. [Red Hat](#4-red-hat)
5. [SAP](#5-sap)
6. [IBM](#6-ibm)
7. [Amazon](#7-amazon)
8. [Google](#8-google)
9. [DataDog](#9-datadog)
10. [中国企业](#10-中国企业)
11. [学术机构](#11-学术机构)
12. [组织演进历史](#12-组织演进历史)
13. [数据说明](#13-数据说明)
14. [相关页面](#14-相关页面)

---


## 1. 数据来源说明

| 来源 | 用途 | 说明 |
|------|------|------|
| **GitHub Integrated PRs** | 唯一统计指标 | ⭐ 推荐使用 |
| [OpenJDK Census](https://openjdk.org/census) | 验证组织归属 | 参考来源 |

> ⚠️ **注意**: 不使用 Git commits 统计，因为 OpenJDK Committer 使用 `@openjdk.org` 邮箱提交，无法准确反映实际组织归属。详见 [AGENTS.md - Contribution Statistics Principles](/AGENTS.md#contribution-statistics-principles)

**查询方式**:
```
https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3A{username}+label%3Aintegrated+is%3Aclosed
```

---

## 2. 组织贡献总览

> **统计来源**: [GitHub Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+label%3Aintegrated+is%3Aclosed)
> **数据更新**: 2026-03-21

| 排名 | 组织 | Integrated PRs | 占比 | 贡献者数 | 主要领域 |
|------|------|----------------|------|----------|----------|
| 1 | **Oracle** | 15,000+ | 70%+ | 800+ | 全领域 |
| 2 | **Red Hat** | 1,000+ | 5% | 50+ | GC, 编译器 |
| 3 | **SAP** | 500+ | 2% | 30+ | HotSpot, 构建系统 |
| 4 | **IBM** | 400+ | 2% | 25+ | JVM, AOT |
| 5 | **Amazon** | 300+ | 1.5% | 20+ | GC, 性能 |
| 6 | **Google** | 200+ | 1% | 15+ | 核心库 |
| 7 | **DataDog** | 6 | <1% | 1+ | JFR 工具 |
| 8 | **Alibaba** | 100+ | <1% | 10+ | 核心库，性能 |
| 9 | **腾讯** | 20+ | <1% | 5+ | GC |
| 10 | **华为** | 15+ | <1% | 8+ | JIT, AOT |
| 11 | **字节跳动** | 10+ | <1% | 5+ | RISC-V |

---

## 3. Oracle

**最大贡献者，主导 OpenJDK 开发**

| 贡献者 | Integrated PRs | 领域 |
|--------|----------------|------|
| [Phil Race](/by-contributor/profiles/phil-race.md) | 200+ | 图形/打印 |
| [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | 90+ | HotSpot VM |
| [Thomas Schatzl](/by-contributor/profiles/thomas-schatzl.md) | 150+ | G1 GC |
| [Magnus Ihse Bursie](/by-contributor/profiles/magnus-ihse-bursie.md) | 100+ | 构建系统 |
| [David Holmes](/by-contributor/profiles/david-holmes.md) | 80+ | 线程/并发 |
| [Claes Redestad](/by-contributor/profiles/claes-redestad.md) | 150+ | 核心库/性能 |
| [Brian Burkhalter](/by-contributor/profiles/brian-burkhalter.md) | 100+ | NIO/网络 |
| [Daniel Fuchs](/by-contributor/profiles/daniel-fuchs.md) | 50+ | HTTP/JMX |
| [Erik Gahlin](/by-contributor/profiles/erik-gahlin.md) | 50+ | JFR |
| [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | 200+ | C2 编译器 |
| [Tobias Hartmann](/by-contributor/profiles/tobias-hartmann.md) | 150+ | JIT 编译器 |
| [Vladimir Kozlov](/by-contributor/profiles/vladimir-kozlov.md) | 100+ | C2 架构 |
| [David Beaumont](/by-contributor/profiles/david-beaumont.md) | 20+ | 编译器 |

**主要贡献领域**：
- GC: G1, ZGC, Serial, Parallel
- 编译器：C1, C2, Graal
- 核心库：java.lang, java.util, java.io
- 桌面：AWT, Swing, JavaFX
- 工具：javac, jlink, jpackage
- 安全：TLS, 加密，认证

---

## 4. Red Hat

**GC 和编译器专家**

| 贡献者 | Integrated PRs | 领域 |
|--------|----------------|------|
| [Andrew Dinn](/by-contributor/profiles/andrew-dinn.md) | 50+ | AArch64 |
| [Thomas Stuefe](/by-contributor/profiles/thomas-stuefe.md) | 50+ | HotSpot, CDS |

**主要贡献领域**：
- Shenandoah GC (主要开发者)
- C2 编译器优化
- JFR 改进
- 安全补丁

---

## 5. SAP

**企业级 JVM 优化**

| 贡献者 | Integrated PRs | 领域 |
|--------|----------------|------|
| [Matthias Baesken](/by-contributor/profiles/matthias-baesken.md) | 100+ | 构建系统 |
| Goetz Lindenmaier | 30+ | HotSpot |

**主要贡献领域**：
- HotSpot VM 移植
- 构建系统 (AIX, Windows)
- 企业级特性

---

## 6. IBM

**J9/OpenJ9 贡献**

| 贡献者 | Integrated PRs | 领域 |
|--------|----------------|------|
| [Amit Kumar](/by-contributor/profiles/amit-kumar.md) | 50+ | s390x, Compiler |
| Mark Stoodley | 30+ | AOT |
| Babneet Singh | 20+ | 测试 |

**主要贡献领域**：
- AOT 编译
- GC 优化
- s390x 架构移植

---

## 7. Amazon

**性能和 GC 优化**

| 贡献者 | Integrated PRs | 领域 |
|--------|----------------|------|
| [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | 803+ | Shenandoah GC, JMH |
| ~~[Nick Gasson](/by-contributor/profiles/nick-gasson.md)~~ | ~~30+~~ | **已修正: 属于 Arm，非 Amazon** |
| [William Kemper](/by-contributor/profiles/william-kemper.md) | 50+ | Shenandoah |

**主要贡献领域**：
- Shenandoah GC (Corretto)
- 启动性能优化
- 云原生优化
- AArch64 支持

---

## 8. Google

**核心库贡献**

| 贡献者 | Integrated PRs | 领域 |
|--------|----------------|------|
| Michael Miller-Cushon | 50+ | 核心库 |
| Paul Sandoz | 30+ | 核心库 |

**主要贡献领域**：
- java.util.concurrent
- 性能优化
- API 改进

---

## 9. DataDog

**JVM 诊断和性能分析**

| 贡献者 | Integrated PRs | 领域 |
|--------|----------------|------|
| [Jaroslav Bachorik](/by-contributor/profiles/jaroslav-bachorik.md) | 6 | JFR 工具，BTrace |

**主要贡献**：
- JFR 稳定性改进
- AsyncGetCallTrace 修复
- BTrace 项目创始人

> **注**: Jaroslav Bachorik 主要贡献到 JFR 和 JVM 诊断工具，是 BTrace 项目的创始人。

---

## 10. 中国企业

### 阿里巴巴

| 贡献者 | Integrated PRs | 领域 |
|--------|----------------|------|
| [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | 97 | 核心库/性能 |

**主要贡献**：
- 字符串拼接优化 (JDK-8336856)
- StringBuilder 优化 (JDK-8355177)
- 启动性能改进 (JDK-8349400)
- ClassFile API 改进 (JDK-8341906)

### 腾讯

| 贡献者 | Integrated PRs | 领域 |
|--------|----------------|------|
| Jie Fu | 10+ | GC |

### 华为

| 贡献者 | Integrated PRs | 领域 |
|--------|----------------|------|
| [Fei Yang](/by-contributor/profiles/fei-yang.md) | 20+ | RISC-V |
| Feilong Jiang | 10+ | JIT/AOT |

### 字节跳动

| 贡献者 | Integrated PRs | 领域 |
|--------|----------------|------|
| Anjian-Wen | 10+ | RISC-V |

---

## 11. 学术机构

### ISCAS (中科院软件所)

| 贡献者 | Integrated PRs | 领域 |
|--------|----------------|------|
| Dingli Zhang | 10+ | RISC-V |

### 龙芯

| 贡献者 | Integrated PRs | 领域 |
|--------|----------------|------|
| Zhang Xiaofeng | 10+ | LoongArch |

---

## 12. 组织演进历史

| 时期 | 主要组织 | 事件 |
|------|----------|------|
| 2007-2010 | Sun, Oracle | OpenJDK 开源 |
| 2011-2014 | Oracle, Red Hat | JDK 7/8 发布 |
| 2015-2018 | Oracle, Red Hat, SAP | JDK 9-11 |
| 2019-2021 | +IBM, Amazon | JDK 12-17 |
| 2022-2024 | +中国企业 | JDK 18-23 |
| 2025-2026 | 全球化加速 | JDK 24-26 |

---

## 13. 数据说明

### 统计方法

| 指标 | 说明 | 推荐度 |
|------|------|--------|
| **GitHub Integrated PRs** | 已合入的 PR 数量 | ⭐⭐⭐ 推荐 |
| Git Commits | 历史数据，仅供参考 | ⚠️ 不推荐 |

**为什么推荐 PRs**：
- OpenJDK Committer 使用 `@openjdk.org` 邮箱提交，无法通过邮箱判断公司
- GitHub PR 直接关联贡献者账号，组织归属更准确
- 详见 [AGENTS.md - Contribution Statistics Principles](/AGENTS.md#contribution-statistics-principles)

### 参考来源

| 来源 | URL | 用途 |
|------|-----|------|
| OpenJDK Census | https://openjdk.org/census | 官方统计，验证组织归属 |
| GitHub PR Search | https://github.com/openjdk/jdk/pulls | PR 统计查询 |

### 数据更新

- **更新频率**: 每个 JDK 版本发布后更新
- **上次更新**: 2026-03-21
- **数据验证**: `scripts/contributor_stats.py`

---

## 14. 相关页面

- [Top 50 贡献者](top50.md)
- [中国贡献者](/by-contributor/profiles/chinese-contributors.md)
- [按领域分类](by-domain.md)
- [年度趋势](by-year.md)
- [地区分布](by-region.md)
- [新星贡献者](rising-stars.md)
