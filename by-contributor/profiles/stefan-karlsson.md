# Stefan Karlsson

> Oracle HotSpot GC Engineer | ZGC Lead | JEP 439 Author

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [主要 JEP 贡献](#3-主要-jep-贡献)
4. [演讲和会议](#4-演讲和会议)
5. [核心技术贡献](#5-核心技术贡献)
6. [ZGC 技术细节](#6-zgc-技术细节)
7. [合作关系](#7-合作关系)
8. [相关链接](#8-相关链接)

---


## 1. 概述

Stefan Karlsson 是 Oracle **HotSpot Garbage Collection Team** 的核心工程师，**ZGC (Z Garbage Collector)** 的主要开发者之一。他与 Per Liden 共同领导了 ZGC 的开发和演进，包括最新的分代 ZGC (Generational ZGC) 特性。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Stefan Karlsson |
| **当前组织** | Oracle (HotSpot Garbage Collection Team) |
| **位置** | Stockholm Metropolitan Area, Sweden |
| **专长** | ZGC, Garbage Collection, Memory Management, HotSpot Runtime |
| **Email** | stefan.karlsson@oracle.com |
| **Twitter/X** | [@stekarmatrik](https://x.com/stekarmatrik) |
| **OpenJDK** | [@stefank](https://openjdk.org/census#stefank) |
| **角色** | JDK Committer, JDK Reviewer, ZGC Lead |

> **数据来源**: [LinkedIn](https://se.linkedin.com/in/stefan-karlsson-56b3953), [Jfokus 2018](https://www.jfokus.se/jfokus18/preso/ZGC--Low-Latency-GC-for-OpenJDK.pdf)

---

## 3. 主要 JEP 贡献

### JEP 439: Generational ZGC (JDK 21)

| 属性 | 值 |
|------|-----|
| **角色** | Author |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 21 |

**影响**: 为 ZGC 添加分代收集能力，进一步提升 ZGC 的性能：
- 降低 GC 开销
- 提高吞吐量
- 保持低延迟特性

### JEP 333: ZGC: Scalable Low-Latency Garbage Collector (JDK 11)

| 属性 | 值 |
|------|-----|
| **角色** | Co-author |
| **合作者** | Per Liden |
| **状态** | Experimental (JDK 11) → Production (JDK 15) |
| **发布版本** | JDK 11+ |

**影响**: ZGC 是一款并发、基于区域、NUMA 感知、压缩型的垃圾收集器：
- GC 暂停时间 < 10ms
- 支持从小到极大 (多 TB) 的堆
- 与 G1 相比大幅降低延迟

### JEP 519: Compact Object Headers

| 属性 | 值 |
|------|-----|
| **角色** | Contributor |
| **合作者** | Coleen Phillimore, Erik Österlund, Vladimir Kozlov |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 26 |

**影响**: 压缩对象头设计，减少 16% 的 heap 开销。

---

## 4. 演讲和会议

| 会议 | 年份 | 主题 | 合作 |
|------|------|------|------|
| **Jfokus VM Tech Summit** | 2018 | ZGC - Low Latency GC for OpenJDK | Per Lidén |
| **FOSDEM** | 2018 | Introduction to ZGC | - |
| **Jfokus** | 2018 | ZGC Deep Dive | - |

---

## 5. 核心技术贡献

### 1. ZGC 开发

Stefan Karlsson 是 ZGC 从实验性特性到生产就绪的关键贡献者：
- **并发收集**: 大部分工作与应用线程并发执行
- **基于区域**: 分代收集的基础
- **NUMA 感知**: 优化多插槽服务器性能
- **压缩型**: 消除堆碎片

### 2. HotSpot Runtime

- **Handles**: `src/hotspot/share/runtime/handles.hpp` 等核心代码贡献
- 与 Erik Österlund、Coleen Phillimore、Kim Barrett 等核心开发者密切合作

### 3. 演讲和分享

- **Jfokus VM Tech Summit 2018**: "ZGC - Low Latency GC for OpenJDK"
  - 与 Per Liden 共同演讲
- YouTube 上有相关的 ZGC 技术分享视频

---

## 6. ZGC 技术细节

### 设计特点

| 特性 | 描述 |
|------|------|
| **并发性** | 大部分工作与应用线程并发执行 |
| **基于区域** | 分代收集的基础 |
| **NUMA 感知** | 优化多插槽服务器 |
| **压缩型** | 消除堆碎片 |
| **低延迟** | GC 暂停 < 10ms |
| **可扩展** | 支持从小到极大 (多 TB) 的堆 |

### 演进历程

- **JDK 11**: 实验性引入 (JEP 333)
- **JDK 15**: 生产就绪
- **JDK 21**: 分代 ZGC (JEP 439)
- **JDK 23+**: 持续优化

---

## 7. 合作关系

与以下 HotSpot GC 团队核心开发者密切合作：
- **Per Liden**: ZGC 联合开发者
- **Erik Österlund**: 内存管理架构
- **Coleen Phillimore**: Runtime 系统
- **Kim Barrett**: GC 架构
- **Roman Kennke**: Shenandoah GC (相关工作)

---

## 8. 相关链接

### JEP 文档
| JEP | 标题 | 角色 |
|-----|------|------|
| [JEP 439](https://openjdk.org/jeps/439) | Generational ZGC | Author |
| [JEP 333](https://openjdk.org/jeps/333) | ZGC: Scalable Low-Latency GC | Co-author |
| [JEP 519](https://openjdk.org/jeps/519) | Compact Object Headers | Contributor |

### 技术资源
| 类型 | 链接 |
|------|------|
| **Jfokus 2018 PDF** | [ZGC Presentation](https://www.jfokus.se/jfokus18/preso/ZGC--Low-Latency-GC-for-OpenJDK.pdf) |
| **OpenJDK Census** | [stefank](https://openjdk.org/census#stefank) |
| **Twitter/X** | [@stekarmatrik](https://x.com/stekarmatrik) |
| **LinkedIn** | [stefan-karlsson-56b3953](https://se.linkedin.com/in/stefan-karlsson-56b3953) |

### 其他贡献
- **PermGen Removal**: 参与移除 Permanent Generation
- **G1 Class Unloading**: G1 垃圾回收器的类卸载功能
- **Mentoring**: 2020 年提名 Axel Boldt-Christmas 为 ZGC Committer

---

> **文档版本**: 2.0
> **最后更新**: 2026-03-20
> **更新内容**:
> - 添加位置: Stockholm Metropolitan Area, Sweden
> - 添加邮箱: stefan.karlsson@oracle.com
> - 添加 Twitter/X: @stekarmatrik
> - 添加 Jfokus 2018 和 FOSDEM 2018 演讲
> - 添加 PermGen Removal 和 G1 Class Unloading 贡献
> - 添加提名 Axel Boldt-Christmas (2020)
