# Frederic Parain

> **GitHub**: [@fparain](https://github.com/fparain)
> **Organization**: Oracle (HotSpot Runtime Team)
> **Role**: JVM Runtime Engineer, Valhalla Contributor
> **OpenJDK Wiki**: [fparain](https://wiki.openjdk.org/display/~fparain)

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [主要 JEP 贡献](#3-主要-jep-贡献)
4. [核心技术贡献](#4-核心技术贡献)
5. [职业经历](#5-职业经历)
6. [演讲和会议](#6-演讲和会议)
7. [技术专长](#7-技术专长)
8. [协作网络](#8-协作网络)
9. [外部资源](#9-外部资源)

---


## 1. 概述

Frederic Parain 是 Oracle 的 **JVM Runtime 工程师**，在 HotSpot 虚拟机开发领域有超过 20 年的经验。他从 2003 年开始参与 HotSpot 开发，先后涉及实时系统 (Real-Time Java)、JVM 工具与诊断 (Serviceability)、以及 **Project Valhalla (值类型/值类)** 的核心工作。他是 **JEP 401 (Value Classes and Objects)** 中堆扁平化 (Heap Flattening) 优化的核心实现者。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Frederic Parain |
| **当前组织** | Oracle (Java Platform Group) |
| **职位** | JVM Runtime Engineer |
| **GitHub** | [@fparain](https://github.com/fparain) |
| **OpenJDK** | [@fparain](https://openjdk.org/census#fparain) |
| **OpenJDK Wiki** | [fparain](https://wiki.openjdk.org/display/~fparain) |
| **角色** | HotSpot Group Member, JDK Reviewer |
| **主要领域** | HotSpot Runtime, Valhalla, Value Classes, Serviceability |
| **项目** | JDK, Valhalla |
| **活跃时间** | 2003 年至今 |

> **数据来源**: [OpenJDK Census](https://openjdk.org/census#fparain), [GitHub](https://github.com/fparain), [OpenJDK Wiki](https://wiki.openjdk.org/display/~fparain)

---

## 3. 主要 JEP 贡献

### JEP 401: Value Classes and Objects (Preview)

| 属性 | 值 |
|------|-----|
| **角色** | 堆扁平化实现者 |
| **项目** | Project Valhalla |
| **状态** | Preview |

**影响**: 引入无身份 (identity-free) 的值类，JVM 可对其进行扁平化存储优化：
- **堆扁平化 (Heap Flattening)**: 将值对象的字段内联存储到包含它的对象或数组中
- **标量化 (Scalarization)**: 在 JIT 编译代码中避免值对象的内存分配
- 显著减少内存占用和间接访问开销

### HotSpot Real-Time 相关工作 (早期)

| 属性 | 值 |
|------|-----|
| **角色** | Real-Time System 工程师 |
| **时间** | 2003 年起 |

**影响**: 为 HotSpot 添加实时线程支持和异步执行能力。

---

## 4. 核心技术贡献

### 1. Project Valhalla - 值类堆扁平化

Frederic 在 JVM Language Summit 2025 上详细介绍了值类的堆扁平化实现：

```
堆扁平化前:
┌──────────────┐     ┌──────────────┐
│   Container  │     │  ValueClass  │
│ ┌──────────┐ │     │ ┌──────────┐ │
│ │ ref ─────┼─┼────>│ │  field1  │ │
│ └──────────┘ │     │ │  field2  │ │
└──────────────┘     │ └──────────┘ │
                     └──────────────┘

堆扁平化后:
┌──────────────────┐
│    Container     │
│ ┌──────────────┐ │
│ │   field1     │ │  (值类字段内联存储)
│ │   field2     │ │
│ └──────────────┘ │
└──────────────────┘
```

**优化效果**:
- 消除额外的对象头 (Object Header) 开销
- 减少堆内存分配
- 改善缓存局部性 (Cache Locality)
- 降低 GC 压力

### 2. JVM Serviceability 和诊断框架

Frederic 在 Serviceability 团队中的贡献：
- **诊断命令框架 (Diagnostic Command Framework)**: 实现 JVM 诊断命令基础设施
- **JVM 管理 API 改进**: 改进 HotSpot 管理接口
- **JVM 融合 (Convergence)**: 参与 JRockit 和 HotSpot 的融合工作

### 3. Real-Time Java

早期在 Real-Time System 项目中的贡献：
- **实时线程支持**: 为 HotSpot 添加实时线程调度能力
- **异步执行**: 实现异步执行支持
- **Real-Time VM 工具改进**: 修复和改进 Real-Time VM 的诊断和工具功能

### 4. Inline Types / Value Types (Valhalla 演进)

Frederic 参与了 Valhalla 项目从 inline types 到 value classes 的演进：
- **JVMTI 兼容性**: 修复 JVMTI `GetObjectMonitorUsage()` 与 inline types 的兼容问题
- **JDB 修复**: 修复 jdb 调试器在 inline class 上调用 "lock" 命令时的崩溃问题
- **值类型原型**: 参与早期 "Minimal Values" 原型实现

---

## 5. 职业经历

| 时间 | 事件 | 详情 |
|------|------|------|
| **2003 年** | 加入 HotSpot Real-Time System 项目 | 实时线程和异步执行 |
| **早期** | Real-Time VM 工具改进 | 诊断和工具功能 |
| **后续** | Serviceability 团队 | JVM 诊断命令框架和管理 API |
| **2012 年** | HotSpot Group Member | 正式成为 HotSpot 小组成员 |
| **2017 年** | Minimal Values 演讲 | "Minimal Values Under the Hood" |
| **2025 年** | JVM Language Summit 演讲 | "Value Classes & Heap Flattening" |
| **至今** | Valhalla 核心贡献者 | 值类堆扁平化实现 |

---

## 6. 演讲和会议

| 会议 | 年份 | 主题 |
|------|------|------|
| **JVM Language Summit** | 2025 | Value Classes & Heap Flattening - What to expect from JEP 401 |
| **技术会议** | 2017 | Minimal Values Under the Hood |

---

## 7. 技术专长

### HotSpot Runtime
- **对象模型**: 对象布局和内存管理
- **值类型**: Value Classes 堆扁平化和标量化
- **诊断框架**: JVM 诊断命令和管理接口

### Project Valhalla
- **堆扁平化**: 值对象的内联存储优化
- **标量化**: JIT 编译中的值对象消除
- **JVMTI 兼容性**: 工具接口与值类型的适配

### Serviceability
- **诊断命令**: JVM 诊断命令框架
- **管理 API**: HotSpot 管理接口
- **调试工具**: JDB 和 JVMTI 支持

---

## 8. 协作网络

| 协作者 | 合作领域 |
|--------|----------|
| [Brian Goetz](/by-contributor/profiles/brian-goetz.md) | Valhalla 项目语言设计 |
| [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | HotSpot Runtime |
| [David Holmes](/by-contributor/profiles/david-holmes.md) | HotSpot Runtime |

---

## 9. 外部资源

| 类型 | 链接 |
|------|------|
| **GitHub** | [fparain](https://github.com/fparain) |
| **OpenJDK Census** | [fparain](https://openjdk.org/census#fparain) |
| **OpenJDK Wiki** | [fparain](https://wiki.openjdk.org/display/~fparain) |
| **JEP 401** | [Value Classes and Objects (Preview)](https://openjdk.org/jeps/401) |
| **Project Valhalla** | [openjdk.org/projects/valhalla](https://openjdk.org/projects/valhalla/) |
| **Valhalla GitHub** | [openjdk/valhalla](https://github.com/openjdk/valhalla) |

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-22
> **状态**: 初稿
