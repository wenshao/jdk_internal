# Paul Sandoz

> **Organization**: [Oracle](/contributors/orgs/oracle.md) (Java Platform Group)
> **Role**: Architect, Java Platform Group
> **Inside.java**: [PaulSandoz](https://inside.java/u/PaulSandoz/)
> **GitHub**: [@PaulSandoz](https://github.com/PaulSandoz)
> **LinkedIn**: [paul-sandoz](https://www.linkedin.com/in/paul-sandoz-4704562/)

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [职业时间线](#3-职业时间线)
4. [主要 JEP 贡献](#4-主要-jep-贡献)
5. [核心技术贡献](#5-核心技术贡献)
6. [社区活动与协作](#6-社区活动与协作)
7. [相关链接](#7-相关链接)

---


## 1. 概述

Paul Sandoz 是 Oracle Java Platform Group 的 **架构师 (Architect)**，是 Java 平台多项核心基础设施的设计者和实现者。他的贡献横跨 Java 平台的多个层次：从 JDK 16 的 **Stream API** 原始设计与实现，到 JDK 9 的 **VarHandle** (JEP 193)，再到从 JDK 16 开始持续孵化至今的 **Vector API** (JEP 338+)。

在加入 Oracle 之前，Paul Sandoz 曾在 **Sun Microsystems** 共同领导 **JAX-RS** 规范并主导 **Jersey** (JAX-RS 参考实现) 的开发。之后他还曾在 **CloudBees** 工作，随后回到 Oracle 深耕 Java 平台底层。他的职业轨迹从云端 (Netflix/CloudBees)、中间层 (JAX-RS/Jersey)，一路深入到 Java 平台最底层的运行时和向量计算 API。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Paul Sandoz |
| **当前组织** | [Oracle](/contributors/orgs/oracle.md) (Java Platform Group) |
| **职位** | Architect, Java Platform Group |
| **前雇主** | Sun Microsystems, CloudBees |
| **专长领域** | Stream API, Vector API, VarHandle, Code Reflection, JAX-RS/Jersey |

---

## 3. 职业时间线

| 年份 | 事件 | 详情 |
|------|------|------|
| **~2005-2010** | Sun Microsystems | 共同领导 JAX-RS 规范 (JSR 311)，主导 Jersey 参考实现 |
| **~2010-2012** | CloudBees | 云平台开发 |
| **~2012-至今** | Oracle | 回到 Java 平台底层开发 |
| **2014** | JDK 8 发布 | Stream API 核心设计与实现 |
| **2017** | JDK 9 发布 | VarHandle (JEP 193)、More Concurrency Updates (JEP 266) |
| **2021** | JDK 16 发布 | Vector API 首次孵化 (JEP 338) |
| **2023** | JVMLS | Code Reflection 演讲 |
| **2025** | Devoxx Belgium | "Java for AI" 演讲 |
| **2026** | JDK 26 | Vector API 第 11 轮孵化 (JEP 529) |

---

## 4. 主要 JEP 贡献

### Vector API 系列 (JEP 338 → JEP 529)

Paul Sandoz 是 Vector API 的核心作者和推动者，该 API 从 JDK 16 开始孵化，至 JDK 26 已历经 **11 轮孵化**，是 OpenJDK 历史上孵化周期最长的 API 之一。

| JEP | 名称 | JDK 版本 | 角色 |
|-----|------|----------|------|
| **JEP 338** | Vector API (Incubator) | JDK 16 | Owner/Author |
| **JEP 414** | Vector API (Second Incubator) | JDK 17 | Owner |
| **JEP 417** | Vector API (Third Incubator) | JDK 18 | Owner |
| **JEP 426** | Vector API (Fourth Incubator) | JDK 19 | Owner |
| **JEP 438** | Vector API (Fifth Incubator) | JDK 20 | Owner |
| **JEP 448** | Vector API (Sixth Incubator) | JDK 21 | Owner |
| **JEP 460** | Vector API (Seventh Incubator) | JDK 22 | Owner |
| **JEP 469** | Vector API (Eighth Incubator) | JDK 23 | Owner |
| **JEP 489** | Vector API (Ninth Incubator) | JDK 24 | Owner |
| **JEP 508** | Vector API (Tenth Incubator) | JDK 25 | Owner |
| **JEP 529** | Vector API (Eleventh Incubator) | JDK 26 | Owner |

> Vector API 长期处于孵化状态的原因是它依赖 Project Valhalla 的 **Value Types** 支持，以实现最优的内存布局和性能。

### JEP 193: Variable Handles (JDK 9)

| 属性 | 值 |
|------|-----|
| **角色** | Assignee / Reviewer |
| **Owner** | Doug Lea |
| **发布版本** | JDK 9 |

**影响**: VarHandle 提供了替代 `sun.misc.Unsafe` 的标准化内存访问 API，支持多种内存顺序模式（plain、opaque、release/acquire、volatile），是 Java 并发编程的重要基础设施。

### JEP 266: More Concurrency Updates (JDK 9)

| 属性 | 值 |
|------|-----|
| **角色** | Contributor |
| **发布版本** | JDK 9 |

**影响**: 引入 `java.util.concurrent.Flow` (Reactive Streams)、`CompletableFuture` 增强等并发 API 改进。

---

## 5. 核心技术贡献

### 1. Stream API (JDK 8)

Paul Sandoz 是 Stream API 的核心实现者之一，与 Brian Goetz 共同将函数式编程范式引入 Java，支持声明式数据处理和并行流计算。

### 2. Vector API (JDK 16-26)

Vector API 为 Java 提供了显式的 SIMD 向量计算能力，与 Intel 的 Sandhya Viswanathan 合作开发：
- 提供可移植的跨架构向量计算 API，编译为高效的 SIMD 指令 (SSE, AVX, NEON)
- 适用于机器学习、线性代数、密码学、金融计算等领域
- 长期孵化原因：依赖 Project Valhalla 的 Value Types 以实现最优内存布局

### 3. VarHandle (JEP 193, JDK 9)

VarHandle 提供了替代 `sun.misc.Unsafe` 的标准化内存访问 API，支持多种内存顺序模式（plain、opaque、release/acquire、volatile）。

### 4. Code Reflection

近年来参与 **Code Reflection** 的开发，为 Java 提供代码模型的反射能力，支持 AI/ML 计算图和 GPU 编程。

### 5. JAX-RS / Jersey (Sun Microsystems 时期)

在 Sun Microsystems 时期共同领导 **JSR 311 (JAX-RS)** 规范，主导 **Jersey** (JAX-RS 参考实现) 的开发。

---

## 6. 社区活动与协作

### 演讲

| 演讲 | 场合 | 主题 |
|------|------|------|
| "Java for AI" | Devoxx Belgium 2025 | Java 平台的 AI 支持能力 |
| "Code Reflection" | JVMLS 2023 | Code Reflection 技术介绍 |
| "The Vector API in JDK 17" | Inside.java Dev.Live | Vector API 技术详解 |

- **Inside Java Podcast Episode 7** (2020-11-17): "The Vector API" — 与 John Rose 讨论 Vector API 设计

### 核心协作者

| 协作者 | 组织 | 合作领域 |
|--------|------|----------|
| [John Rose](../../by-contributor/profiles/john-rose.md) | Oracle | Vector API, Method Handles |
| [Brian Goetz](../../by-contributor/profiles/brian-goetz.md) | Oracle | Stream API, Lambda |
| Sandhya Viswanathan | Intel | Vector API (Intel 侧主导) |
| [Vladimir Kozlov](../../by-contributor/profiles/vladimir-kozlov.md) | Oracle | Vector API, JIT 编译器 |
| [Doug Lea](../../by-contributor/profiles/doug-lea.md) | SUNY Oswego | VarHandle, 并发 API |

---

## 7. 相关链接

### 官方资料
- [Inside.java - PaulSandoz](https://inside.java/u/PaulSandoz/) | [GitHub](https://github.com/PaulSandoz) | [LinkedIn](https://www.linkedin.com/in/paul-sandoz-4704562/) | [gotopia.tech](https://gotopia.tech/experts/839/paul-sandoz)

### JEP 文档
- [JEP 338: Vector API](https://openjdk.org/jeps/338) | [JEP 529: Vector API (11th)](https://openjdk.org/jeps/529) | [JEP 193: Variable Handles](https://openjdk.org/jeps/193) | [JEP 266: Concurrency Updates](https://openjdk.org/jeps/266)

### 演讲与媒体
- [Inside Java Podcast Ep. 7: The Vector API](https://inside.java/2020/11/17/podcast-007/) | [Vector API in JDK 17](https://inside.java/2021/09/23/devlive-vector-api/) | [Java for AI - Devoxx 2025](https://cr.openjdk.org/~psandoz/conferences/2025-Devoxx-Belgium/Devoxx-Belgium-25-Java-For-AI.pdf) | [JVMLS 2023 - Code Reflection](https://inside.java/2023/08/28/code-reflection/)

> **数据调查时间**: 2026-03-22
> **文档版本**: 1.0
