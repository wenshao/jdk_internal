---

# GC 停顿分析：Full GC 抖动导致延迟毛刺

> **声明**：本文中所有 GC 日志、监控数据、性能指标均为 **示意数据（illustrative data）**，实际结果取决于工作负载、硬件环境和 JVM 版本。

---

## 目录

1. [背景与问题描述](#1-背景与问题描述)
2. [环境信息](#2-环境信息)
3. [第一阶段：监控数据分析](#3-第一阶段监控数据分析)
4. [第二阶段：GC 日志诊断](#4-第二阶段gc-日志诊断)
5. [第三阶段：根因定位](#5-第三阶段根因定位)
6. [第四阶段：调优方案](#6-第四阶段调优方案)
7. [最终效果对比](#7-最终效果对比)
8. [经验总结与 Checklist](#8-经验总结与-checklist)

---

## 1. 背景与问题描述

### 1.1 业务场景

**支付结算服务**，核心要求是稳定的低延迟：

| 指标 | SLA 要求 |
|------|----------|
| P50 latency | < 5ms |
| P99 latency | < 50ms |
| P999 latency | < 200ms |
| 可用性 | 99.99% |

### 1.2 问题现象

- **周期性延迟毛刺**：每隔 2-4 小时出现 P99 延迟飙升到 500ms-2s
- **Full GC 触发**：毛刺与 Full GC（即 JDK 17+ G1 的并发标记失败后的 STW 暂停）时间高度吻合
- **大促期间恶化**：流量翻倍时 Full GC 频率从每天 6 次增加到每小时 2-3 次

---

## 2. 环境信息

```
容器规格:    4C8G (Kubernetes Pod)
JDK 版本:    JDK 17.0.12 (Eclipse Temurin)
GC:          G1 GC (默认)
框架:        Spring Boot 3.1 + MyBatis
堆大小:      6GB (-Xms6g -Xmx6g)
```

初始 JVM 参数（问题发生时）：
```bash
java -Xms6g -Xmx6g -XX:+UseG1GC -jar payment-service.jar
```

---

## 3. 第一阶段：监控数据分析

### 3.1 GC 概览（JFR）

通过 JFR（JDK Flight Recorder）持续记录 24 小时：

```
GC 事件统计 (示意):
┌──────────────────────────────┬──────────┐
│ 事件类型                     │ 次数     │
├──────────────────────────────┼──────────┤
│ Young GC (Evacuation Pause)  │ ~2,400   │
│ Mixed GC                     │ ~180     │
│ Concurrent Mark              │ ~24      │
│ Full GC (to-space exhausted) │ 6        │ ← 问题根源
└──────────────────────────────┴──────────┘
```

### 3.2 关键发现

```
Young GC 平均暂停:  18ms
Young GC 最大暂停:  45ms
Mixed GC 平均暂停:  35ms
Full GC 暂停:       800ms - 3,200ms  ← 远超 SLA
```

---

## 4. 第二阶段：GC 日志诊断

### 4.1 GC 日志分析

```bash
# 启用详细 GC 日志
-XX:+PrintGCDetails -Xlog:gc*:file=/logs/gc.log:time,level,tags
```

**Full GC 日志示意**：
```
[2026-01-15T03:42:17.823+0800] Full GC (Allocation Failure)
  [Eden: 512.0M(512.0M)->0.0B(512.0M)
   Survivors: 64.0M->0.0B
   Heap: 5.8G(6.0G)->4.2G(6.0G)]
  [Metaspace: 89123K->89123K(1114112K)]
  [Pause: 1842ms]  ← STW 1.8 秒
```

### 4.2 分析结论

| 根因 | 证据 |
|------|------|
| **Old Gen 占用持续增长** | Full GC 后 Old Gen 仍有 4.2G，说明存在大量长期存活对象 |
| **to-space exhausted** | G1 在混合回收时无法找到足够的空闲 region |
| **Humongous 对象** | 日志中频繁出现大对象分配（>32KB） |

---

## 5. 第三阶段：根因定位

### 5.1 大对象（Humongous Objects）

```bash
# 使用 jcmd 分析堆
jcmd <pid> GC.heap_info
```

发现：大量 `byte[]` 和 `String` 对象超过 G1 region 大小的 50%（32KB/2 = 16KB），被当作 humongous 对象处理，绕过 young gen 直接进入 old gen。

### 5.2 内存泄漏嫌疑

```bash
# JFR 事件: OldObjectSample
jcmd <pid> JFR.start settings=profile +OldObjectSample#cutoff=10m
```

发现：`ConcurrentHashMap$Node[]` 持续增长，来自一个本地缓存实现——缓存条目没有设置过期策略。

### 5.3 Metaspace 膨胀

```
Metaspace: 89MB (使用) / 1114MB (提交)
```

Metaspace 使用不高，排除了类加载器泄漏的可能。

---

## 6. 第四阶段：调优方案

### 方案一：优化应用层缓存

```java
// 之前: 无过期策略的缓存
private final Map<String, Order> orderCache = new ConcurrentHashMap<>();

// 之后: 使用 Caffeine 带过期策略
private final Cache<String, Order> orderCache = Caffeine.newBuilder()
    .maximumSize(10_000)
    .expireAfterWrite(Duration.ofMinutes(30))
    .build();
```

### 方案二：G1 GC 参数调优

```bash
# 优化后的 JVM 参数
java \
  -Xms6g -Xmx6g \
  -XX:+UseG1GC \
  -XX:MaxGCPauseMillis=100 \
  -XX:G1HeapRegionSize=8m \
  -XX:InitiatingHeapOccupancyPercent=40 \
  -XX:G1MixedGCCountTarget=16 \
  -XX:G1ReservePercent=15 \
  -XX:+UseStringDeduplication \
  -XX:+ParallelRefProcEnabled \
  -Xlog:gc*:file=/logs/gc.log:time,level,tags:filecount=10,filesize=50m
```

### 方案三：升级到 JDK 21 + Generational ZGC

```bash
# 最终方案: JDK 21+ Generational ZGC
java \
  -Xms6g -Xmx6g \
  -XX:+UseZGC \
  -XX:+ZGenerational \
  -jar payment-service.jar
```

---

## 7. 最终效果对比

| 指标 | 优化前 (G1 默认) | 方案二 (G1 调优) | 方案三 (Gen ZGC) |
|------|-----------------|-----------------|-----------------|
| Full GC 频率 | 6次/天 | 0次 | 0次 |
| P99 延迟 | 500ms-2s (毛刺) | 80-120ms | 5-15ms |
| P999 延迟 | 1-3s | 200-400ms | 20-40ms |
| Young GC 暂停 | 18ms avg | 12ms avg | <1ms |
| 吞吐量 | baseline | +5% | +3% |

> **说明**: 上述数据为示意数据，实际效果因工作负载而异。Generational ZGC 的优势在于延迟稳定性，而非绝对吞吐量。

---

## 8. 经验总结与 Checklist

### Full GC 抖动排查 Checklist

- [ ] 确认 Full GC 触发原因（Allocation Failure / System.gc() / Metaspace）
- [ ] 检查 Old Gen 使用趋势（是否持续增长）
- [ ] 检查 Humongous 对象数量和大小
- [ ] 使用 JFR OldObjectSample 定位长期存活对象
- [ ] 检查本地缓存是否有大小限制和过期策略
- [ ] 检查是否误调用 `System.gc()`
- [ ] 考虑增大 `-XX:G1HeapRegionSize` 减少 humongous 对象

### 关键经验

1. **G1 Full GC 几乎总是应用问题**——通常是内存泄漏或缓存无限制增长
2. **先用 JFR 排查，再调 JVM 参数**——80% 的 GC 问题是应用代码问题
3. **Generational ZGC 是延迟敏感服务的终极方案**——但需要 JDK 21+
4. **`-XX:+ParallelRefProcEnabled` 对引用处理密集的应用效果显著**

### 相关资源

- [GC 调优实战：G1→ZGC 迁移](gc-tuning-case.md)
- [G1 vs ZGC vs Shenandoah 对比](/guides/comparisons/g1-vs-zgc-vs-shenandoah.md)
- [GC 演进时间线](/by-topic/core/gc/)
- [JFR 指南](/guides/jfr.md)
