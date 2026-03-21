# Stefan Karlsson

> **GitHub**: [@stefank](https://github.com/stefank)
> **Organization**: [Oracle](../../contributors/orgs/oracle.md) (HotSpot GC Team)
> **Role**: ZGC Lead Developer, JEP 439 Author
> **OpenJDK**: [stefank](https://openjdk.org/census#stefank)

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

Stefan Karlsson 是 Oracle **HotSpot Garbage Collection Team** 的核心工程师，**ZGC (Z Garbage Collector)** 的主要开发者之一。他与 Per Liden 共同领导了 ZGC 的开发和演进，包括分代 ZGC (Generational ZGC, JEP 439) 特性。他于 2013 年加入 HotSpot GC 团队，在此之前自 2006 年起在 Oracle/BEA 从事其他 JVM 相关项目（包括 JRockit 相关工作）。他也是 **PermGen 移除** 和 **Metaspace 实现** 的重要贡献者。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Stefan Karlsson |
| **当前组织** | Oracle (HotSpot Garbage Collection Team) |
| **位置** | Stockholm Metropolitan Area, Sweden |
| **GitHub** | [@stefank](https://github.com/stefank) |
| **专长** | ZGC, Garbage Collection, Memory Management, Metaspace, HotSpot Runtime |
| **Email** | stefan.karlsson@oracle.com |
| **早期经历** | Oracle/BEA JVM 相关项目 (2006-2013), 包括 JRockit Virtual Edition |
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
- **JDK 15**: 生产就绪 (JEP 377)
- **JDK 21**: 分代 ZGC (JEP 439)
- **JDK 23**: 分代模式成为默认 (JEP 474)
- **JDK 24**: 移除非分代模式 (JEP 490)
- **JDK 25+**: 持续优化

---

## 7. 合作关系

与以下 HotSpot GC 团队核心开发者密切合作：
- **Per Liden** (@pliden): ZGC 联合开发者，JEP 333 共同作者
- **Erik Österlund** (@fisk): 内存管理架构, Generational ZGC 共同实现者
- **Axel Boldt-Christmas**: ZGC 贡献者 (2020 年由 Stefan 提名为 Committer), Generational ZGC 共同实现者
- **Albert Mingkun Yang**: Generational ZGC 共同实现者
- **Coleen Phillimore**: Runtime 系统, JEP 519 合作者
- **Kim Barrett**: GC 架构

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
- **PermGen Removal / Metaspace**: 参与移除 Permanent Generation，共同实现 Metaspace (JDK-6964458)，将类元数据存储迁移到本地内存
- **G1 Class Unloading**: G1 垃圾回收器的类卸载功能
- **Mentoring**: 2020 年提名 Axel Boldt-Christmas 为 ZGC Committer

### ZGC 完整 JEP 演进
| JEP | 标题 | 版本 | 角色 |
|-----|------|------|------|
| [JEP 333](https://openjdk.org/jeps/333) | ZGC: Scalable Low-Latency GC | JDK 11 | Co-author |
| [JEP 377](https://openjdk.org/jeps/377) | ZGC: Production Ready | JDK 15 | Contributor |
| [JEP 439](https://openjdk.org/jeps/439) | Generational ZGC | JDK 21 | Author |
| [JEP 474](https://openjdk.org/jeps/474) | ZGC: Generational Mode by Default | JDK 23 | Contributor |
| [JEP 490](https://openjdk.org/jeps/490) | ZGC: Remove Non-Generational Mode | JDK 24 | Contributor |

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
