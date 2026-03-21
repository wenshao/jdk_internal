# Patricio Chilano Mateo

> HotSpot Runtime 同步/锁定专家，JEP 374 作者，JEP 491 核心实现者，Oracle HotSpot 团队

---
## 目录

1. [基本信息](#1-基本信息)
2. [技术专长](#2-技术专长)
3. [主要 JEP 贡献](#3-主要-jep-贡献)
4. [贡献概览](#4-贡献概览)
5. [关键贡献详解](#5-关键贡献详解)
6. [开发风格](#6-开发风格)
7. [相关链接](#7-相关链接)

---

## 1. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Patricio Chilano Mateo |
| **当前组织** | [Oracle](../../contributors/orgs/oracle.md) - HotSpot Runtime 团队 |
| **GitHub** | [@pchilanomate](https://github.com/pchilanomate) |
| **OpenJDK** | [@pchilanomate](https://openjdk.org/census#pchilanomate) |
| **Inside.java** | [PatricioChilano](https://inside.java/u/PatricioChilano/) |
| **角色** | OpenJDK Reviewer |
| **主要领域** | HotSpot Runtime, 同步/锁定, Monitor, 线程挂起, 偏向锁, 虚拟线程 |
| **代表性 JEP** | JEP 374 (偏向锁废弃), JEP 491 (虚拟线程无 Pinning 同步) |

> **数据来源**: [OpenJDK Census](https://openjdk.org/census#pchilanomate), [JEP 374](https://openjdk.org/jeps/374), [JEP 491](https://openjdk.org/jeps/491), [Inside.java](https://inside.java/u/PatricioChilano/)

---

## 2. 技术专长

`HotSpot Runtime` `Object Monitor` `Synchronization` `Biased Locking` `Thread Suspend` `Virtual Threads` `Loom` `Native Monitors`

Patricio Chilano Mateo 是 Oracle HotSpot Runtime 团队中专注于 JVM 同步和锁定机制的专家。他的工作涵盖了从偏向锁的废弃到虚拟线程 Pinning 问题的解决，是 HotSpot 同步子系统演进的核心推动者。

---

## 3. 主要 JEP 贡献

### JEP 374: Deprecate and Disable Biased Locking (JDK 15)

| 属性 | 值 |
|------|-----|
| **角色** | Author (作者) |
| **状态** | Final |
| **发布版本** | JDK 15 (废弃), JDK 18 (移除) |

**影响**: 偏向锁 (Biased Locking) 是 HotSpot 中一项历史悠久的同步优化技术，但随着现代硬件和 JVM 技术的发展，其维护成本远超收益：
- 默认禁用 `-XX:+UseBiasedLocking`
- 废弃所有相关命令行选项
- 简化了 HotSpot 同步子系统的代码复杂度
- 为后续锁定优化 (如轻量级锁) 扫清障碍

### JEP 491: Synchronize Virtual Threads without Pinning (JDK 24)

| 属性 | 值 |
|------|-----|
| **角色** | 核心实现者 / Reviewer |
| **Lead** | Alan Bateman |
| **状态** | Final |
| **发布版本** | JDK 24 |

**影响**: 解决了虚拟线程最大的痛点 -- synchronized 导致的 Pinning 问题：
- 虚拟线程在 synchronized 块中阻塞时不再钉住 (pin) 平台线程
- 通过 "owner swapping" 技术交换锁的所有者标识
- 大幅提升虚拟线程在使用 synchronized 的代码中的可伸缩性
- 消除了从 synchronized 迁移到 ReentrantLock 的必要性

---

## 4. 贡献概览

### 按类别统计

| 类别 | 描述 |
|------|------|
| 偏向锁废弃与移除 | JEP 374 实现，JDK 18 中完全移除偏向锁代码 |
| 虚拟线程同步 | JEP 491 核心实现，解决 synchronized pinning 问题 |
| Native Monitor 设计 | "Sneaky Locking" 技术，防止 safepoint 期间的死锁 |
| 线程挂起修复 | 修复 block transition 期间的挂起导致的死锁 |
| ObjectMonitor 优化 | Monitor 相关的性能优化和代码清理 |

### 关键成就

- **JEP 374 作者**: 主导偏向锁的废弃和禁用决策
- **JEP 491 核心实现**: 解决虚拟线程 synchronized pinning 问题
- **Native Monitor 设计**: 设计了防止 safepoint 死锁的 "Sneaky Locking" 方案
- **HotSpot 同步子系统现代化**: 推动同步机制从偏向锁时代向轻量级锁时代转型

---

## 5. 关键贡献详解

### 1. 偏向锁废弃 (JEP 374)

**背景**: 偏向锁在 JDK 1.6 中引入，通过消除无竞争情况下的原子操作来降低同步开销。但随着原子指令在现代处理器上的成本降低，偏向锁的收益变得微乎其微，而其实现复杂度却给 HotSpot 代码库带来了沉重的维护负担。

**决策**: Patricio 通过详细的性能分析证明偏向锁在现代工作负载中的收益有限，成功推动了废弃决策。

### 2. 虚拟线程 Pinning 解决方案 (JEP 491)

**问题**: 虚拟线程进入 synchronized 块时被钉住 (pin) 在平台线程上，无法释放载体线程供其他虚拟线程使用，严重限制了可伸缩性。

**解决方案**: Patricio 引入了 "owner swapping" 技术：
- 虚拟线程在 monitor 上阻塞时，将锁的所有者标识从虚拟线程交换为平台线程
- 平台线程得以释放并运行其他虚拟线程
- 当锁变得可用时，重新调度原始虚拟线程

### 3. Native Monitor "Sneaky Locking" 设计

**问题**: JVM 内部的 native monitor 在 safepoint 期间可能导致死锁。

**解决方案**: Patricio 设计了 "Sneaky Locking" 技术，允许线程在 safepoint 期间以安全的方式获取某些锁，从而避免死锁。

---

## 6. 开发风格

Patricio Chilano Mateo 的贡献特点:

1. **深度同步专家**: 专注于 JVM 同步和锁定机制的底层实现
2. **架构级思考**: 推动偏向锁废弃等影响整个 JVM 的架构决策
3. **问题驱动**: 从实际性能问题出发设计解决方案
4. **跨项目影响**: 贡献横跨 HotSpot Runtime、Loom、Lilliput 等多个项目

---

## 7. 相关链接

| 类型 | 链接 |
|------|------|
| **GitHub** | [@pchilanomate](https://github.com/pchilanomate) |
| **OpenJDK Census** | [pchilanomate](https://openjdk.org/census#pchilanomate) |
| **Inside.java** | [PatricioChilano](https://inside.java/u/PatricioChilano/) |
| **JEP 374** | [Deprecate and Disable Biased Locking](https://openjdk.org/jeps/374) |
| **JEP 491** | [Synchronize Virtual Threads without Pinning](https://openjdk.org/jeps/491) |
| **Native Monitor 设计** | [OpenJDK Wiki](https://wiki.openjdk.org/display/hotspot/native+monitors+design) |
| **JBS Issues** | [pchilanomate assignee](https://bugs.openjdk.org/issues/?jql=assignee%20%3D%20pchilanomate) |

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-22
> **状态**: 初稿
