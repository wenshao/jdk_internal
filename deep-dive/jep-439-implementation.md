---

# JEP 439: Generational ZGC 实现分析

> JEP 439 | Per Liden (Oracle) | JDK 21 (正式) | 分代 ZGC

---

## 目录

1. [概述](#1-概述)
2. [Non-Gen ZGC 的吞吐量问题](#2-non-gen-zgc-的吞吐量问题)
3. [分代架构设计](#3-分代架构设计)
4. [ZPage 类型与内存布局](#4-zpage-类型与内存布局)
5. [并发重定位](#5-并发重定位)
6. [性能对比](#6-性能对比)
7. [版本演进](#7-版本演进)
8. [配置与调优](#8-配置与调优)

---

## 1. 概述

Generational ZGC 将 ZGC 分为 Young Generation 和 Old Generation 两个分代，分别进行垃圾收集。核心目标是：**保持 <1ms STW 暂停的同时，显著提升吞吐量**。

| 属性 | 值 |
|------|-----|
| **JEP** | [JEP 439](https://openjdk.org/jeps/439) |
| **作者** | Per Liden |
| **目标版本** | JDK 21 |
| **状态** | Closed / Delivered |
| **前置** | JEP 333 (ZGC, JDK 11), JEP 377 (ZGC 正式, JDK 15) |

---

## 2. Non-Gen ZGC 的吞吐量问题

### 2.1 为什么需要分代？

Non-Gen ZGC 对所有对象一视同仁——无论对象存活时间长短，都需要经过完整的并发标记和重定位周期。

```
对象存活时间分布 ("弱代假设"):
┌──────────────────────────────────────────────────┐
│                                                    │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░          │
│  |← 90-98% 短命对象 →|← 2-10% 长命对象 →|          │
│                                                    │
│  Non-Gen ZGC: 每次都要扫描和处理全部对象           │
│  Gen ZGC:    频繁回收 Young Gen (短命对象集中区)   │
│              很少回收 Old Gen (长命对象集中区)     │
└──────────────────────────────────────────────────┘
```

### 2.2 吞吐量瓶颈

| 操作 | Non-Gen ZGC | Generational ZGC |
|------|-------------|-----------------|
| 标记 Young Gen 对象 | 每次全部标记 | 频繁但只标记 Young |
| 标记 Old Gen 对象 | 每次全部标记 | 很少标记 |
| 重定位存活对象 | 所有存活对象 | Young 中少量存活 |
| 总工作量 | 高 | 低 |

---

## 3. 分代架构设计

### 3.1 双代结构

```
┌─────────────────────────────────────────────────────────┐
│                  Generational ZGC 堆                     │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │            Young Generation                      │   │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐           │   │
│  │  │ZPage │ │ZPage │ │ZPage │ │ZPage │           │   │
│  │  │ 2MB  │ │ 2MB  │ │ 32MB │ │ 2MB  │           │   │
│  │  └──────┘ └──────┘ └──────┘ └──────┘           │   │
│  │  新对象分配区，频繁 GC                          │   │
│  └──────────────────────────────┬──────────────────┘   │
│                                 │ Promote               │
│  ┌──────────────────────────────▼──────────────────┐   │
│  │            Old Generation                        │   │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐           │   │
│  │  │ZPage │ │ZPage │ │ZPage │ │ZPage │           │   │
│  │  │ 32MB │ │ 2MB  │ │ N×M  │ │ 32MB │           │   │
│  │  └──────┘ └──────┘ └──────┘ └──────┘           │   │
│  │  长寿对象区，很少 GC                            │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 3.2 屏障 (Barriers)

Gen ZGC 使用两种屏障：

```
1. Load Barrier (加载屏障):
   读取引用时检查 coloured pointer，确保不指向已移动的对象
   → 与 Non-Gen 相同

2. Store Barrier (存储屏障):
   新增! 记录从 Old → Young 的引用（remembered set）
   → 避免 Full GC 时扫描整个 Old Gen
```

### 3.3 Remembered Set

```
Old Gen → Young Gen 引用追踪:
┌─────────────────────┐     ┌─────────────────────┐
│     Old Gen          │     │    Young Gen         │
│                     │     │                     │
│  Object A ──────────┼────►│  Object B           │
│  (指向 Young 的引用) │     │                     │
│                     │     │                     │
│  Remembered Set:    │     │                     │
│  [A→B, C→D, E→F]   │     │                     │
│  (记录跨代引用)     │     │                     │
└─────────────────────┘     └─────────────────────┘

Young GC 时只需扫描 Remembered Set 中的 Old Gen 对象，
无需扫描整个 Old Gen。
```

---

## 4. ZPage 类型与内存布局

### 4.1 页面类型

| 类型 | 大小 | 对象大小 | 用途 |
|------|------|---------|------|
| **Small** | 2MB | < 256KB | 大多数对象 |
| **Medium** | 32MB | 256KB - 4MB | 中等大小对象 |
| **Large** | N × 2MB | > 4MB | 大数组/大对象 |

### 4.2 分代标记

每个 ZPage 有一个分代标记（generation ID），用于区分 Young 和 Old：

```
ZPage Header:
┌─────────────────────────────────────────────────┐
│ page_start        (地址)                         │
│ page_size         (2MB/32MB/N×2MB)              │
│ generation_id     (0=Young, 1=Old)              │
│ num_objects       (对象数量)                     │
│ used              (已用字节数)                   │
│ forwarding_table  (重定位表)                     │
└─────────────────────────────────────────────────┘
```

---

## 5. 并发重定位

### 5.1 Young GC 流程

```
Young GC (并发, STW < 1ms):
┌──────────────────────────────────────────────────────┐
│ 1. STW: 扫描 Young Gen root (线程栈、JNI)           │
│    └── 暂停时间: ~0.1-0.5ms                         │
│                                                      │
│ 2. 并发: 标记 Young Gen 存活对象                     │
│    └── 扫描 Young→Young 引用                        │
│    └── 扫描 Old→Young 引用 (via Remembered Set)     │
│                                                      │
│ 3. 并发: 重定位存活对象                              │
│    ├── 存活对象留在 Young (age < threshold)          │
│    └── 存活对象 Promote 到 Old (age >= threshold)   │
│                                                      │
│ 4. 并发: 释放空闲 ZPage                             │
└──────────────────────────────────────────────────────┘
```

### 5.2 Promotion 条件

```java
// 伪代码: 对象从 Young 提升到 Old
if (object.age >= promotionThreshold) {
    relocateToOldGen(object);
} else {
    object.age++;
    relocateWithinYoungGen(object);
}
```

---

## 6. 性能对比

### 6.1 SpecJBB2015 基准（示意）

| 指标 | Non-Gen ZGC | Gen ZGC | G1 GC |
|------|-------------|---------|-------|
| 最大 STW 暂停 | 0.8ms | 0.5ms | 180ms |
| 吞吐量 (max-jOPS) | 42,000 | 52,000 | 54,000 |
| 吞吐量 (critical-jOPS) | 18,000 | 22,000 | 20,000 |
| 内存开销 | +10% | +15% | baseline |

> **说明**: Gen ZGC 吞吐量接近 G1，同时保持亚毫秒暂停。

### 6.2 内存开销

| 组件 | Non-Gen | Gen ZGC |
|------|---------|---------|
| 堆内存 | X | X |
| Remembered Set | - | +2-5% |
| 双重标记位图 | - | +1-3% |
| 转发表 | +1% | +1% |
| **总开销** | **+10%** | **+15%** |

---

## 7. 版本演进

| 版本 | 状态 | 说明 |
|------|------|------|
| JDK 11 | JEP 333 (实验) | Non-Gen ZGC |
| JDK 13 | JEP 351 | ZGC 归还未使用内存 |
| JDK 14 | JEP 365 | ZGC 支持 macOS |
| JDK 15 | JEP 377 | ZGC 正式版 (Production) |
| JDK 16 | JEP 376 | ZGC 并发线程栈扫描 |
| JDK 21 | **JEP 439** | **Generational ZGC (需 -XX:+ZGenerational)** |
| JDK 23 | 默认 | Gen ZGC 成为默认模式 |
| JDK 25+ | 持续优化 | NUMA 感知、内存效率提升 |

---

## 8. 配置与调优

```bash
# JDK 21: 启用 Generational ZGC
java -XX:+UseZGC -XX:+ZGenerational -Xmx4g -jar app.jar

# JDK 23+: Gen ZGC 为默认
java -XX:+UseZGC -Xmx4g -jar app.jar

# 调优参数
-XX:ZFragmentLimit=5            # 碎片率上限 (默认 5%)
-XX:ZAllocationSpikeTolerance=2 # 分配尖峰容忍度

# 监控
-Xlog:gc*:file=gc.log:time,level,tags
jcmd <pid> GC.heap_info
```

---

## 相关链接

- [JEP 439: Generational ZGC](/jeps/gc/jep-439.md)
- [GC 演进时间线](/by-topic/core/gc/)
- [ZGC 调优案例](/cases/zgc-tuning.md)
- [G1 vs ZGC vs Shenandoah 对比](/guides/comparisons/g1-vs-zgc-vs-shenandoah.md)
