# Stefan Karlsson

> **Organization**: Oracle (HotSpot Garbage Collection Team)
> **Role**: HotSpot GC Engineer, ZGC Lead

---

## 概述

Stefan Karlsson 是 Oracle **HotSpot Garbage Collection Team** 的核心工程师，**ZGC (Z Garbage Collector)** 的主要开发者之一。他与 Per Liden 共同领导了 ZGC 的开发和演进，包括最新的分代 ZGC (Generational ZGC) 特性。

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Stefan Karlsson |
| **当前组织** | Oracle (HotSpot Garbage Collection Team) |
| **专长** | ZGC, Garbage Collection, Memory Management, HotSpot Runtime |

---

## 主要 JEP 贡献

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

## 核心技术贡献

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

## ZGC 技术细节

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

## 合作关系

与以下 HotSpot GC 团队核心开发者密切合作：
- **Per Liden**: ZGC 联合开发者
- **Erik Österlund**: 内存管理架构
- **Coleen Phillimore**: Runtime 系统
- **Kim Barrett**: GC 架构
- **Roman Kennke**: Shenandoah GC (相关工作)

---

## 相关链接

### JEP 文档
- [JEP 439: Generational ZGC](https://openjdk.org/jeps/439)
- [JEP 333: ZGC (Scalable Low-Latency GC)](https://openjdk.org/jeps/333)
- [JEP 519: Compact Object Headers](https://openjdk.org/jeps/519)

### 技术资源
- [ZGC - Low Latency GC for OpenJDK (Presentation)](https://www.jfokus.se/jfokus18/preso/ZGC--Low-Latency-GC-for-OpenJDK.pdf)

---

**Sources**:
- [JEP 439: Generational ZGC](https://openjdk.org/jeps/439)
- [JEP 333: ZGC](https://openjdk.org/jeps/333)
- [JEP 519: Compact Object Headers](https://openjdk.org/jeps/519)
- [Jfokus 2018 - ZGC Presentation](https://www.jfokus.se/jfokus18/preso/ZGC--Low-Latency-GC-for-OpenJDK.pdf)
