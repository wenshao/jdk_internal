# Ron Pressler

> Oracle Consulting Member of Technical Staff | Project Loom Lead
>
> Virtual Threads、Structured Concurrency、Scoped Values 的创造者

---
## 目录

1. [概要](#1-概要)
2. [职业时间线](#2-职业时间线)
3. [Project Loom 演进与 JEP 列表](#3-project-loom-演进与-jep-列表)
4. [技术影响力](#4-技术影响力)
5. [Quasar 与 Parallel Universe](#5-quasar-与-parallel-universe)
6. [演讲与社区](#6-演讲与社区)
7. [外部资源](#7-外部资源)

---

## 1. 概要

Ron Pressler 是 Oracle Java Platform Group 的 Consulting Member of Technical Staff，也是 **Project Loom** 的技术负责人。Project Loom 将虚拟线程 (Virtual Threads)、结构化并发 (Structured Concurrency) 和作用域值 (Scoped Values) 引入 JDK，彻底改变了 Java 的并发编程范式。

在加入 Oracle 之前，Ron 创立了 Parallel Universe 公司（Y Combinator 孵化），开发了 **Quasar**（JVM 用户态轻量级线程库）和 **Comsat**（基于 Fiber 的标准 API 实现），是将轻量级线程引入 JVM 生态的先驱。

### 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Ron Pressler |
| **组织** | Oracle (Java Platform Group) |
| **职位** | Consulting Member of Technical Staff |
| **主导项目** | Project Loom |
| **专长** | 并发编程、轻量级线程、延续 (Continuations)、分布式系统 |
| **GitHub** | [@pron](https://github.com/pron) |
| **OpenJDK** | [rpressler](https://openjdk.org/census#rpressler) |
| **个人网站** | [pron.github.io](https://pron.github.io/) |
| **Inside.java** | [RonPressler](https://inside.java/u/RonPressler/) |

---

## 2. 职业时间线

| 年份 | 事件 | 详情 |
|------|------|------|
| **早期** | 以色列空军 | 软件开发者与架构师，开发空中交通管制与导弹防御系统，以及大规模集群物理模拟 |
| **~2013** | 创立 Parallel Universe | Y Combinator 孵化的高性能 JVM 服务端技术公司 |
| **2013-2016** | 开发 Quasar & Comsat | 通过字节码增强为 JVM 带来用户态轻量级线程（Fibers） |
| **2014** | JVMLS 演讲 | 在 JVM Language Summit 展示 Quasar 轻量级线程技术 |
| **~2017** | 加入 Oracle | 受 Brian Goetz 邀请加入 Java Platform Group |
| **2018** | Project Loom 启动 | 作为技术负责人主导 Loom 项目开发 |
| **2022 (JDK 19)** | Virtual Threads 首次预览 | JEP 425: Virtual Threads (Preview) |
| **2023 (JDK 21)** | Virtual Threads 正式发布 | JEP 444: Virtual Threads 成为正式特性 |
| **2024-至今** | 持续完善 Loom 生态 | 推进 Structured Concurrency 和 Scoped Values 走向正式化 |

---

## 3. Project Loom 演进与 JEP 列表

Project Loom 是 Java 平台自 Lambda 以来最重要的并发模型变革。Ron Pressler 作为 Lead 主导了三大核心特性从孵化到正式化的完整生命周期，共计 **17 个 JEP**：

### 3.1 Virtual Threads（虚拟线程）

虚拟线程是由 JVM 管理的轻量级线程，不直接绑定操作系统线程，使"每个请求一个线程"的编程模型可扩展到百万级并发。阻塞时自动释放载体线程，底层基于 Continuation 机制实现高效上下文切换。

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| JEP 425 | Virtual Threads (Preview) | 19 | 首次预览 |
| JEP 436 | Virtual Threads (Second Preview) | 20 | 第二次预览 |
| **JEP 444** | **Virtual Threads** | **21** | **正式发布** |

### 3.2 Structured Concurrency（结构化并发）

将不同线程中运行的相关任务视为单一工作单元，统一错误处理、取消传播和可观测性。

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| JEP 428 | Structured Concurrency (Incubator) | 19 | 首次孵化 |
| JEP 437 | Structured Concurrency (Second Incubator) | 20 | 第二次孵化 |
| JEP 453 | Structured Concurrency (Preview) | 21 | 首次预览 |
| JEP 462 | Structured Concurrency (Second Preview) | 22 | 第二次预览 |
| JEP 480 | Structured Concurrency (Third Preview) | 23 | 第三次预览 |
| JEP 499 | Structured Concurrency (Fourth Preview) | 24 | 第四次预览 |
| JEP 505 | Structured Concurrency (Fifth Preview) | 25 | 第五次预览 |
| JEP 525 | Structured Concurrency (Sixth Preview) | 26 | 第六次预览 |

### 3.3 Scoped Values（作用域值）

提供在线程内和线程间共享不可变数据的机制，是 ThreadLocal 的现代替代方案，子线程自动继承父线程的 Scoped Value 绑定且无需拷贝。

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| JEP 429 | Scoped Values (Incubator) | 20 | 首次孵化 |
| JEP 446 | Scoped Values (Preview) | 21 | 首次预览 |
| JEP 464 | Scoped Values (Second Preview) | 22 | 第二次预览 |
| JEP 481 | Scoped Values (Third Preview) | 23 | 第三次预览 |
| JEP 487 | Scoped Values (Fourth Preview) | 24 | 第四次预览 |
| **JEP 506** | **Scoped Values** | **25** | **正式发布** |

---

## 4. 技术影响力

### 从 Quasar 到 Loom 的思想传承

| 理念 | Quasar (库层面) | Project Loom (平台层面) |
|------|----------------|----------------------|
| 轻量级线程 | Fibers（字节码增强） | Virtual Threads（JVM 原生支持） |
| 阻塞透明化 | 需要 @Suspendable 注解 | 自动识别阻塞点 |
| 调度器 | ForkJoinPool 调度 | JVM 内置调度器 |
| 标准 API 集成 | Comsat 适配层 | 核心库原生支持 |

### 对 Java 生态的影响

- **消除反应式编程的必要性**: 虚拟线程让简单的同步代码即可达到异步代码的性能
- **百万级并发**: 单个 JVM 可运行数百万虚拟线程
- **向后兼容**: 现有基于 Thread 的代码可无缝迁移到虚拟线程

---

## 5. Quasar 与 Parallel Universe

**Quasar** 是 Ron 在 Parallel Universe (Y Combinator 孵化) 期间开发的开源 JVM 轻量级线程库，通过 Java Agent 字节码增强将 `@Suspendable` 方法转换为 Continuation，在 ForkJoinPool 上运行数百万用户态 Fibers。**Comsat** 则为 Servlet、JAX-RS、JDBC 等标准 API 提供 Fiber 感知实现，并额外提供 Web Actors API 支持 WebSocket 和服务器推送。

- Quasar: [puniverse/quasar](https://github.com/puniverse/quasar)
- Comsat: [puniverse/comsat](https://github.com/puniverse/comsat)

---

## 6. 演讲与社区

### 重要演讲

| 演讲 | 场合 | 主题 |
|------|------|------|
| "Why Continuations are Coming to Java" | QCon London 2019 | 延续机制与 Loom 设计 |
| Project Loom Overview | Devoxx BE 2019 | Continuations 实现进展 |
| Quasar: Lightweight Threads on the JVM | JVMLS 2014 | Quasar 轻量级线程技术 |
| Project Loom | Curry On 2019 | Loom 并发模型 |
| Virtual Threads | Joker 2020 | 虚拟线程设计与实现 |
| Project Loom | Code Mesh 2020 | Loom 技术深度解析 |

Ron 还在 [Inside.java](https://inside.java/u/RonPressler/) 持续发表 Loom 相关技术文章，并撰写了 [State of Loom](https://cr.openjdk.org/~rpressler/loom/loom/sol1_part2.html) 系列文档阐述设计理念与实现进展。

---

## 7. 外部资源

| 类型 | 链接 |
|------|------|
| **GitHub** | [@pron](https://github.com/pron) |
| **个人博客** | [pron.github.io](https://pron.github.io/) |
| **Inside.java** | [RonPressler](https://inside.java/u/RonPressler/) |
| **OpenJDK Loom Wiki** | [Project Loom](https://wiki.openjdk.org/display/loom) |
| **Quasar** | [puniverse/quasar](https://github.com/puniverse/quasar) |
| **Comsat** | [puniverse/comsat](https://github.com/puniverse/comsat) |
| **Crunchbase** | [Ron Pressler](https://www.crunchbase.com/person/ron-pressler) |
| **QCon Profile** | [Speaker Page](https://archive.qconlondon.com/speakers/ron-pressler) |
| **InfoQ Podcast** | [Java's Project Loom](https://www.infoq.com/podcasts/java-project-loom/) |
| **ECOOP 2015** | [Speaker Profile](https://2015.ecoop.org/profile/ronpressler) |

---

> **数据调查时间**: 2026-03-22
> **文档版本**: 1.0
