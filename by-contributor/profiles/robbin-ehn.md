# Robbin Ehn

> **GitHub**: [@robehn](https://github.com/robehn)
> **Organization**: Oracle (HotSpot Runtime Team)
> **Role**: HotSpot Runtime Engineer, 并发与线程管理专家
> **Inside.java**: [RobbinEhn](https://inside.java/u/RobbinEhn/)

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [主要 JEP 贡献](#3-主要-jep-贡献)
4. [核心技术贡献](#4-核心技术贡献)
5. [职业经历](#5-职业经历)
6. [演讲](#6-演讲)
7. [技术专长](#7-技术专长)
8. [外部资源](#8-外部资源)

---


## 1. 概述

Robbin Ehn 是 Oracle HotSpot Runtime 团队的工程师，专注于 **并发 (Concurrency)**、**锁机制 (Locking)** 和 **安全点 (Safepointing)** 领域。他是 **JEP 312 (Thread-Local Handshakes)** 的核心实现者，该特性从根本上改变了 JVM 线程同步的方式，允许对单个线程执行回调而无需触发全局 VM 安全点。此外，他还是 OpenJDK **RISC-V 移植项目** 的重要贡献者。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Robbin Ehn |
| **当前组织** | Oracle (HotSpot Runtime Team) |
| **GitHub** | [@robehn](https://github.com/robehn) |
| **OpenJDK** | [@rehn](https://openjdk.org/census#rehn) |
| **Inside.java** | [RobbinEhn](https://inside.java/u/RobbinEhn/) |
| **角色** | JDK Committer, JDK Reviewer |
| **主要领域** | Concurrency, Locking, Safepointing, RISC-V |
| **活跃时间** | 多年持续贡献 |

> **数据来源**: [OpenJDK Census](https://openjdk.org/census#rehn), [GitHub](https://github.com/robehn), [Inside.java](https://inside.java/u/RobbinEhn/)

---

## 3. 主要 JEP 贡献

### JEP 312: Thread-Local Handshakes (JDK 10)

| 属性 | 值 |
|------|-----|
| **角色** | 核心实现者 |
| **Bug ID** | JDK-8185640 |
| **状态** | Delivered |
| **发布版本** | JDK 10 |

**影响**: 引入线程局部握手机制，允许对单个 Java 线程执行回调而无需全局 VM 安全点：
- **单线程停顿**: 可以停止单个线程而非所有线程
- **per-thread 指针**: 通过每线程轮询页面指针实现
- **自愈合**: 线程完成自己的操作后立即继续执行
- **性能影响**: 基准测试显示无显著性能退化 (Linux x64: -0.7%, Solaris SPARC: +1.5%)

---

## 4. 核心技术贡献

### 1. Thread-Local Handshakes 实现

Robbin 设计并实现了线程局部握手机制的核心架构：

```
全局安全点 (传统方式):
┌────────┐ ┌────────┐ ┌────────┐
│Thread 1│ │Thread 2│ │Thread 3│
│  STOP  │ │  STOP  │ │  STOP  │  <- 所有线程必须停止
│  wait  │ │  wait  │ │  wait  │
│  GO    │ │  GO    │ │  GO    │
└────────┘ └────────┘ └────────┘

Thread-Local Handshake (JEP 312):
┌────────┐ ┌────────┐ ┌────────┐
│Thread 1│ │Thread 2│ │Thread 3│
│  STOP  │ │ running│ │ running│  <- 只需停止目标线程
│callback│ │ running│ │ running│
│  GO    │ │ running│ │ running│
└────────┘ └────────┘ └────────┘
```

**实现关键**: 修改安全点轮询机制，使用 per-thread 指针进行间接寻址。VM 维护两个轮询页面 -- 一个始终受保护 (guarded)，一个始终不受保护 (unguarded)。更新目标线程的指针指向受保护页面即可触发该线程的握手。

### 2. 安全点和并发优化

- **Mutex 断言修复**: 修复 `mutexLocker assert_locked_or_safepoint` 在非 VM 线程中的状态访问问题
- **安全点超时诊断**: 改进安全点超时时的错误转储
- **锁机制改进**: 优化 HotSpot 内部锁和同步原语

### 3. RISC-V 移植

Robbin 是 OpenJDK RISC-V 移植项目的重要贡献者：
- **RISC-V 解释器**: 解释器 volatile 引用存储与 G1 GC 的集成
- **寄存器信息**: 向 hs_err 错误文件添加可用寄存器信息
- **FOSDEM 2024 演讲**: "Unleashing RISC-V in Managed Runtimes"

---

## 5. 职业经历

| 时间 | 事件 | 详情 |
|------|------|------|
| **2017 年** | JEP 312 实现 | Thread-Local Handshakes 核心实现 |
| **JDK 10** | JEP 312 交付 | 在 JDK 10 中正式发布 |
| **持续** | HotSpot Runtime 开发 | 并发、锁和安全点改进 |
| **近年** | RISC-V 移植 | OpenJDK RISC-V 平台支持 |
| **2024 年** | FOSDEM 演讲 | RISC-V 在托管运行时中的应用 |

---

## 6. 演讲

| 会议 | 年份 | 主题 |
|------|------|------|
| **FOSDEM** | 2024 | Unleashing RISC-V in Managed Runtimes: Navigating Extensions, Memory Models, and Performance Challenges in OpenJDK |

---

## 7. 技术专长

### 线程与并发
- **安全点**: JVM 安全点机制设计和优化
- **Thread-Local Handshakes**: 线程局部回调机制
- **锁机制**: HotSpot 内部锁和同步

### 平台移植
- **RISC-V**: OpenJDK RISC-V 架构移植
- **解释器**: 字节码解释器平台适配
- **内存模型**: 硬件内存模型与 JMM 映射

---

## 8. 外部资源

| 类型 | 链接 |
|------|------|
| **GitHub** | [robehn](https://github.com/robehn) |
| **Inside.java** | [RobbinEhn](https://inside.java/u/RobbinEhn/) |
| **OpenJDK Census** | [rehn](https://openjdk.org/census#rehn) |
| **JEP 312** | [Thread-Local Handshakes](https://openjdk.org/jeps/312) |
| **FOSDEM 2024** | [Unleashing RISC-V in Managed Runtimes](https://archive.fosdem.org/2024/events/attachments/fosdem-2024-2327-unleashing-risc-v-in-managed-runtimes-navigating-extensions-memory-models-and-performance-challenges-in-openjdk/slides/22609/UnleashingRV_Final_bMFKUDX.pdf) |

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-22
> **状态**: 初稿


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 284 |
| **活跃仓库数** | 4 |
