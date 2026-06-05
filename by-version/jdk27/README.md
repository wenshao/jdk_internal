# JDK 27

> **状态**: Rampdown Phase One（特性集已冻结） | **预计 GA**: 2026-09-15 | **类型**: Feature Release（非 LTS）

[![OpenJDK](https://img.shields.io/badge/OpenJDK-27-orange)](https://openjdk.org/projects/jdk/27/)
[![License](https://img.shields.io/badge/License-GPLv2--with--Classpath--Exception-blue)](https://openjdk.org/projects/jdk/27/)

---
## 目录

1. [快速导航](#1-快速导航)
2. [版本概览](#2-版本概览)
3. [发布时间线](#3-发布时间线)
4. [JEP 汇总](#4-jep-汇总)
5. [核心贡献者](#5-核心贡献者)
6. [贡献者统计](#6-贡献者统计)
7. [相关链接](#7-相关链接)

---

## 1. 快速导航

| 我想了解 | 链接 |
|---------|------|
| 所有 JEP 详细列表 | [JEP 汇总](./jeps.md) |
| 贡献者排名 | [贡献分析](./contributions.md) |
| 如何试用 | [早期访问版本](https://jdk.java.net/27/) |
| JDK 26 文档 | [JDK 26](../jdk26/) |
| 下一个 LTS (JDK 29) | OpenJDK 计划 2027-09 |

---

## 2. 版本概览

JDK 27 是继 JDK 26 (2026-03-17 GA) 之后的下一个 Feature Release（非 LTS；下一个 LTS 为 2027-09 的 JDK 29）。**已于 2026-06-04 进入 Rampdown Phase One**，从主线 fork 出 `jdk27` 稳定化分支，特性集已冻结，此后仅接受缺陷修复与文档完善。

### 关键特性（9 个 JEP，已 Target）

| JEP | 特性 | 类别 | 性质 |
|-----|------|------|------|
| [523](https://openjdk.org/jeps/523) | Make G1 the Default Garbage Collector in All Environments | GC | 行为变更 |
| [527](../../jeps/security/jep-527.md) | Post-Quantum Hybrid Key Exchange for TLS 1.3 | 安全 | 正式特性 |
| [531](https://openjdk.org/jeps/531) | Lazy Constants (Third Preview) | 核心库 | 预览 |
| [532](https://openjdk.org/jeps/532) | Primitive Types in Patterns, instanceof, and switch (Fifth Preview) | 语言 | 预览 |
| [533](https://openjdk.org/jeps/533) | Structured Concurrency (Seventh Preview) | 并发 | 预览 |
| [534](https://openjdk.org/jeps/534) | Compact Object Headers by Default | 运行时 | 行为变更 |
| [536](https://openjdk.org/jeps/536) | JFR In-Process Data Redaction | 可观测性 | 正式特性 |
| [537](https://openjdk.org/jeps/537) | Vector API (Twelfth Incubator) | 性能/SIMD | 孵化 |
| [538](https://openjdk.org/jeps/538) | PEM Encodings of Cryptographic Objects (Third Preview) | 安全 | 预览 |

**两大默认行为变更值得关注**:
- **JEP 523**: G1 成为**所有环境**的默认 GC（此前在非 server 类、资源受限环境下默认使用 Serial GC）。
- **JEP 534**: 紧凑对象头（Compact Object Headers）成为 HotSpot **默认**对象头布局（64 位架构上对象头 96→64 位），延续 [JEP 519](../../jeps/gc/jep-519.md)（JDK 25 转正）。

---

## 3. 发布时间线

```
2026-03-17  JDK 26 GA（JDK 27 开发开始）
    │
    ▼
2026-06-04  Rampdown Phase One（从主线分支，特性集冻结）  ◀── 当前阶段
    │
    ▼
2026-07-16  Rampdown Phase Two
    │
    ▼
2026-08-06  Initial Release Candidate
    │
    ▼
2026-08-20  Final Release Candidate
    │
    ▼
2026-09-15  General Availability
```

> 数据来源：[OpenJDK JDK 27 项目页](https://openjdk.org/projects/jdk/27/)（页面更新于 2026-06-04）。

---

## 4. JEP 汇总

完整分析详见 [jeps.md](./jeps.md)。下表为已 Target 到 JDK 27 的 9 个 JEP 及其在本仓库的相关分析：

| JEP | 标题 | 类别 | 相关分析 |
|-----|------|------|---------|
| [523](https://openjdk.org/jeps/523) | Make G1 the Default Garbage Collector in All Environments | GC | [G1 时间线](../../by-topic/core/gc/) |
| [527](../../jeps/security/jep-527.md) | Post-Quantum Hybrid Key Exchange for TLS 1.3 | 安全 | [JEP 527 分析](../../jeps/security/jep-527.md) |
| [531](https://openjdk.org/jeps/531) | Lazy Constants (Third Preview) | 核心库 | 前身 [JEP 502 Stable Values](../../jeps/performance/jep-502.md) |
| [532](https://openjdk.org/jeps/532) | Primitive Types in Patterns, instanceof, and switch (Fifth Preview) | 语言 | 前身 [JEP 455](../../jeps/tools/jep-455.md) |
| [533](https://openjdk.org/jeps/533) | Structured Concurrency (Seventh Preview) | 并发 | 前身 [JEP 499](../../jeps/concurrency/jep-499.md) |
| [534](https://openjdk.org/jeps/534) | Compact Object Headers by Default | 运行时 | 前身 [JEP 519](../../jeps/gc/jep-519.md) |
| [536](https://openjdk.org/jeps/536) | JFR In-Process Data Redaction | 可观测性 | [JFR 主题](../../by-topic/core/performance/) |
| [537](https://openjdk.org/jeps/537) | Vector API (Twelfth Incubator) | 性能/SIMD | 前身 [JEP 508](../../jeps/concurrency/jep-508.md) |
| [538](https://openjdk.org/jeps/538) | PEM Encodings of Cryptographic Objects (Third Preview) | 安全 | [安全主题](../../by-topic/security/security/) |

### 候选 JEP (Proposed to Target)

特性集已随 Rampdown Phase One（2026-06-04）冻结，预计不再新增 JEP。

---

## 5. 核心贡献者

> 基于 PR 数据统计，完整排名详见 [contributions.md](./contributions.md)。

JDK 27 开发期（2026-03-21 起）由 Oracle 主导，G1/GC、C2 编译器、client（AWT/Swing）、core-libs 与测试是改动最密集的模块。

---

## 6. 贡献者统计

详见 [contributions.md](./contributions.md)（组织贡献、Top 50 贡献者、模块分布、PR 类型）。

---

## 7. 相关链接

- [OpenJDK JDK 27 项目页](https://openjdk.org/projects/jdk/27/)
- [早期访问版本下载](https://jdk.java.net/27/)
- [JDK 26 文档](../jdk26/)
- [JDK 25 文档](../jdk25/)（上一个 LTS）
- [JEP 分析索引](../../jeps/)
