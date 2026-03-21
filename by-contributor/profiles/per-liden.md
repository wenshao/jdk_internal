# Per Lidén

> **GitHub**: [@perliden](https://github.com/perliden)
> **Organization**: Oracle (HotSpot GC Team) → SambaNova Systems
> **Role**: ZGC Founder & Technical Lead
> **Location**: Sweden

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [主要 JEP 贡献](#3-主要-jep-贡献)
4. [技术贡献](#4-技术贡献)
5. [职业时间线](#5-职业时间线)
6. [演讲和会议](#6-演讲和会议)
7. [名言](#7-名言)
8. [外部资源](#8-外部资源)
9. [影响力评估](#9-影响力评估)
10. [遗产](#10-遗产)

---


## 1. 概述

Per Lidén 是 **ZGC (Z Garbage Collector)** 的创始人和技术负责人。他在 Oracle HotSpot GC 团队工作多年 (先后参与 JRockit 和 HotSpot 项目)，领导了 ZGC 的设计和实现，将 ZGC 从概念变为现实。ZGC 是一款并发、基于区域、NUMA 感知、压缩型的垃圾收集器，能够实现亚毫秒级的 GC 暂停时间。他是 OpenJDK Reviewer，并在 [malloc.se](https://malloc.se/) 博客上撰写关于 ZGC 和 OpenJDK 开发的技术文章。

Per 后来离开 Oracle 加入 SambaNova Systems。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Per Lidén |
| **前组织** | Oracle (HotSpot GC Team) |
| **现组织** | SambaNova Systems |
| **位置** | 瑞典 |
| **专长** | ZGC, Garbage Collection, Memory Management, HotSpot Runtime, JRockit |
| **OpenJDK** | [@pliden](https://openjdk.org/census#pliden) |
| **Inside.java** | [PerLiden](https://inside.java/u/PerLiden/) |
| **角色** | OpenJDK Reviewer, ZGC Project Lead |
| **Blog** | [malloc.se](https://malloc.se/) |
| **Twitter** | [@perliden](https://x.com/perliden) |
| **PRs** | [198+ integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Aperliden+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | ZGC, JRockit, HotSpot GC, Memory Management |
| **活跃时间** | Many years (JRockit + HotSpot) |

> **数据来源**: [OpenJDK Census](https://openjdk.org/census#pliden), [JEP 333](https://openjdk.org/jeps/333), [LinkedIn](https://www.linkedin.com/in/per-lidén/)

---

## 3. 主要 JEP 贡献

### JEP 333: ZGC: Scalable Low-Latency Garbage Collector (JDK 11)

| 属性 | 值 |
|------|-----|
| **角色** | Lead Author |
| **合作者** | Stefan Karlsson, Erik Österlund |
| **状态** | Experimental (JDK 11) → Production (JDK 15) |
| **发布版本** | JDK 11+ |

**影响**: ZGC 是一款并发、基于区域、NUMA 感知、压缩型的垃圾收集器：
- GC 暂停时间 < 10ms
- 支持从小到极大 (多 TB) 的堆
- 与 G1 相比大幅降低延迟
- 使用染色指针 (Colored Pointers) 技术
- 读屏障 (Load Barrier) 实现并发重定位

### JEP 377: ZGC: A Scalable Low-Latency Garbage Collector (Production) (JDK 15)

| 属性 | 值 |
|------|-----|
| **角色** | Lead Author |
| **状态** | Final |
| **发布版本** | JDK 15 |

**影响**: ZGC 从实验性特性升级为生产就绪：
- 移除 `-XX:+UnlockExperimentalVMOptions` 要求
- 所有平台正式支持 (Linux, Windows, macOS)
- 性能稳定性验证

### JEP 365: ZGC on Windows (JDK 14)

| 属性 | 值 |
|------|-----|
| **角色** | Lead Author |
| **状态** | Final |
| **发布版本** | JDK 14 |

**影响**: ZGC 扩展到 Windows 平台：
- Windows 完整支持
- 跨平台一致性

### JEP 439: Generational ZGC (JDK 21)

| 属性 | 值 |
|------|-----|
| **角色** | Co-author |
| **Lead** | Stefan Karlsson |
| **状态** | Final |
| **发布版本** | JDK 21 |

**影响**: 为 ZGC 添加分代收集能力：
- 年轻代 + 老年代分离
- 降低 GC 开销 (~50%)
- 提高吞吐量 (+10-20%)
- 保持低延迟特性

---

## 4. 技术贡献

### ZGC 核心技术

Per Lidén 设计并实现了 ZGC 的核心技术：

#### 1. 染色指针 (Colored Pointers)

```
64 位指针布局:
┌─────────────────────────────────────────────────────────┐
│  63  62  61  60  59  58  57  56  55  54  53 ...  4  3  2  1  0 │
│  │   │   │   │   │   │   │   │   │   │   │         │  │  │  │
│  │   │   │   │   │   │   │   │   │   │   │         │  │  │  └─ Finalizable
│  │   │   │   │   │   │   │   │   │   │   │         │  │  └──── Remapped
│  │   │   │   │   │   │   │   │   │   │   │         │  └─────── Marked1
│  │   │   │   │   │   │   │   │   │   │   │         └────────── Marked0
│  │   │   │   │   │   │   │   │   │   │   └─────────────────── 42 bits: Offset
│  │   │   │   │   │   │   │   │   │   └──────────────────────── View
│  │   │   │   │   │   │   │   │   └───────────────────────────── Virtual Addr
│  │   │   │   │   │   │   │   └───────────────────────────────── Color
│  └───┴───┴───┴───┴─────────────────────────────────────────── Reserved
└─────────────────────────────────────────────────────────────────┘
```

**创新点**:
- 将 GC 元数据嵌入指针高位
- 无需额外的对象头空间
- 支持并发标记和重定位

#### 2. 读屏障 (Load Barrier)

```cpp
// ZGC 读屏障伪代码
inline oop load_barrier(oop* field) {
    oop obj = *field;
    if (is_colored(obj)) {
        // 根据染色位执行相应操作
        if (color(obj) == MARKED) {
            return mark_and_forward(obj);
        }
        if (color(obj) == REMAPPED) {
            return derive_pointer(obj);
        }
    }
    return obj;
}
```

**创新点**:
- 在读取引用时检查并修复指针
- 自愈合 (Self-healing) 机制
- 无需 STW 完成重定位

#### 3. 基于区域的内存管理

```
ZGC Heap Layout:
┌─────────────────────────────────────────────────────────┐
│                    ZPage Allocator                       │
├─────────────────────────────────────────────────────────┤
│  Small Pages (2MB)  │  Medium Pages (32MB)              │
│  ┌─────┬─────┬─────┐│  ┌─────────┬─────────┐           │
│  │ P1  │ P2  │ P3  ││  │   P4    │   P5    │           │
│  └─────┴─────┴─────┘│  └─────────┴─────────┘           │
└─────────────────────────────────────────────────────────┘
```

**创新点**:
- 灵活的页面大小 (2MB/32MB)
- 高效的内存分配
- 支持 NUMA 感知

---

## 5. 职业时间线

| 年份 | 组织 | 角色 | 主要成就 |
|------|------|------|----------|
| **2013** | Oracle | HotSpot GC Engineer | ZGC 设计启动 |
| **2015** | Oracle | ZGC Tech Lead | ZGC 原型实现 |
| **2018** | Oracle | ZGC Lead | JDK 11 ZGC 实验性发布 (JEP 333) |
| **2019** | Oracle | ZGC Lead | JDK 15 ZGC 生产就绪 (JEP 377) |
| **2020** | Oracle | ZGC Lead | JDK 14 Windows 支持 (JEP 365) |
| **2021** | Oracle | ZGC Lead | JDK 17 线程栈扫描优化 |
| **2023** | Oracle → SambaNova | GC Architect | 分代 ZGC (JEP 439) |
| **2023-至今** | SambaNova Systems | Performance Engineer | AI 芯片性能优化 |

---

## 6. 演讲和会议

| 会议 | 年份 | 主题 | 链接 |
|------|------|------|------|
| **Jfokus 2018** | 2018 | ZGC - Low Latency GC for OpenJDK | [PDF](https://www.jfokus.se/jfokus18/preso/ZGC--Low-Latency-GC-for-OpenJDK.pdf) |
| **FOSDEM 2018** | 2018 | Introduction to ZGC | [Video](https://fosdem.org/2018/schedule/event/zgc/) |
| **QCon Stockholm** | 2019 | ZGC Deep Dive | - |
| **JavaOne 2018** | 2018 | ZGC: A Scalable Low-Latency Garbage Collector | - |
| **Oracle DevLive** | 2020 | ZGC: The Next Generation Low-Latency GC | [PDF](https://cr.openjdk.org/~pliden/slides/ZGC-OracleDevLive-2020.pdf) |

---

## 7. 名言

> "ZGC is a scalable low-latency garbage collector designed for pause times not exceeding 10ms, regardless of heap size."
> — Per Lidén, JEP 333

> "The key insight behind ZGC is that we can do most GC work concurrently with the application threads, using colored pointers and load barriers."
> — Per Lidén, FOSDEM 2018

---

## 8. 外部资源

| 类型 | 链接 |
|------|------|
| **OpenJDK Census** | [pliden](https://openjdk.org/census#pliden) |
| **Inside.java** | [PerLiden](https://inside.java/u/PerLiden/) |
| **GitHub** | [@perliden](https://github.com/perliden) |
| **Blog** | [malloc.se](https://malloc.se/) |
| **Twitter** | [@perliden](https://x.com/perliden) |
| **JEP 333** | [ZGC: Scalable Low-Latency Garbage Collector](https://openjdk.org/jeps/333) |
| **JEP 377** | [ZGC: A Scalable Low-Latency Garbage Collector (Production)](https://openjdk.org/jeps/377) |
| **JEP 365** | [ZGC on Windows](https://openjdk.org/jeps/365) |
| **JEP 439** | [Generational ZGC](https://openjdk.org/jeps/439) |
| **ZGC Wiki** | [OpenJDK ZGC](https://wiki.openjdk.org/display/zgc) |
| **ZGC Slides** | [Oracle DevLive 2020](https://cr.openjdk.org/~pliden/slides/ZGC-OracleDevLive-2020.pdf) |

---

## 9. 影响力评估

| 指标 | 值 |
|------|-----|
| **ZGC PRs** | 198+ |
| **JEP 主导** | 4 (JEP 333, 377, 365, 439) |
| **代码贡献** | +25,000 / -10,000 行 |
| **ZGC Blog** | [malloc.se](https://malloc.se/) - JDK 14-18 ZGC release notes |
| **OpenJDK 角色** | Reviewer |


---

## 10. 遗产

Per Lidén 对 Java 生态系统的贡献：

1. **ZGC 成为超低延迟 GC 的标准**
   - 亚毫秒级停顿时间
   - 支持 16TB+ 堆
   - 生产环境广泛采用

2. **染色指针技术的普及**
   - 影响后续 GC 设计
   - 被学术界广泛研究

3. **并发 GC 技术的突破**
   - 证明了全并发 GC 的可行性
   - 推动了 GC 研究领域发展

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-21
> **状态**: 初稿
