# GC 调优实战：电商订单服务 P99 延迟毛刺排查与治理

> **声明**：本文中所有 GC 日志、监控数据、性能指标均为 **示意数据（illustrative data）**，实际结果取决于工作负载、硬件环境和 JVM 版本。请勿将具体数值作为调优基准。

---

## 目录

1. [背景与问题描述](#1-背景与问题描述)
2. [环境信息](#2-环境信息)
3. [第一阶段：数据收集](#3-第一阶段数据收集)
4. [第二阶段：GC 日志诊断](#4-第二阶段gc-日志诊断)
5. [第三阶段：G1 GC 调优](#5-第三阶段g1-gc-调优)
6. [第四阶段：切换 ZGC](#6-第四阶段切换-zgc)
7. [第五阶段：ZGC 精调与最终方案](#7-第五阶段zgc-精调与最终方案)
8. [决策记录：为什么选 ZGC 而非 Shenandoah](#8-决策记录为什么选-zgc-而非-shenandoah)
9. [最终效果对比](#9-最终效果对比)
10. [经验总结与 Checklist](#10-经验总结与-checklist)

---

## 1. 背景与问题描述

### 1.1 业务场景

电商平台**订单服务（Order Service）**，核心链路包括：

- 下单（Create Order）— 涉及库存扣减、优惠计算、订单持久化
- 支付回调（Payment Callback）— 更新订单状态、触发物流
- 订单查询（Query Order）— 高频读操作，支撑 C 端页面

日常 QPS 约 3,000，大促峰值可达 12,000+。服务以 **低延迟** 为核心 SLA：

| 指标 | SLA 要求 |
|------|----------|
| P50 latency | < 10ms |
| P99 latency | < 50ms |
| P999 latency | < 200ms |
| 可用性 | 99.95% |

### 1.2 问题现象

运维监控（Prometheus + Grafana）发现以下异常：

- **P99 延迟毛刺**：正常 30-40ms，但每隔几分钟出现 200-500ms 的毛刺
- **Full GC 频繁**：每小时触发 2-5 次 Full GC，每次暂停 300-800ms
- **大促期间恶化**：峰值流量下 Full GC 频率翻倍，甚至出现连续 Full GC

从 APM（Application Performance Monitoring）的 trace 数据看，延迟毛刺与 GC 暂停（GC pause）时间高度吻合。

---

## 2. 环境信息

### 2.1 硬件与部署

```
容器规格:    8C16G (Kubernetes Pod, CPU limit 8 cores, Memory limit 16Gi)
JDK 版本:    JDK 21.0.2 (Eclipse Temurin)
框架:        Spring Boot 3.2 + Spring WebFlux (部分接口) + MyBatis
数据库:      MySQL 8.0 (RDS)
缓存:        Redis Cluster
消息队列:    Apache Kafka
```

### 2.2 初始 JVM 参数

```bash
# 初始启动参数（问题发生时的配置）
java \
  -Xms8g -Xmx8g \
  -XX:+UseG1GC \
  -XX:MaxGCPauseMillis=200 \
  -XX:+UseStringDeduplication \
  -Xlog:gc:file=/logs/gc.log:time,level,tags \
  -jar order-service.jar
```

**问题**：这份参数基本是"默认 + 设个堆大小"，缺乏针对性调优。

---

## 3. 第一阶段：数据收集

### 3.1 开启详细 GC 日志

```bash
# 重启时修改启动参数（JDK 21 Unified Logging 格式）
java -Xms8g -Xmx8g -XX:+UseG1GC -XX:MaxGCPauseMillis=200 \
  -Xlog:gc*=info:file=/logs/gc-detail.log:time,uptime,level,tags:filecount=10,filesize=100m \
  -jar order-service.jar

# 或不重启，用 jcmd 动态调整
jcmd 12345 VM.log output=/logs/gc-detail.log \
  what=gc*=info decorators=time,uptime,level,tags \
  output_options=filecount=10,filesize=100m
```

### 3.2 使用 jstat 实时监控

```bash
# 每 2 秒输出一次 GC 统计，共 60 次（观察 2 分钟）
jstat -gcutil 12345 2000 60
```

示意输出：

```
  S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT     GCT
  0.00  45.23  67.89  78.34  96.12  93.45   1245   18.34     8    4.82   23.16
 52.78   0.00  12.45  79.01  96.12  93.45   1246   18.36     8    4.82   23.18
  0.00   0.00  34.56  85.23  96.12  93.45   1247   18.38     9    5.41   23.79
```

**关键发现**：Old Generation（O 列）持续 78-85%，老年代压力大；FGC 短时间内增加，单次 Full GC 平均耗时 ≈ 590ms。

### 3.3 使用 JFR 录制

JFR（JDK Flight Recorder）是 JDK 内置的低开销性能分析工具：

```bash
# 启动 JFR 录制，持续 5 分钟
jcmd 12345 JFR.start \
  name=gc-analysis \
  duration=5m \
  filename=/logs/gc-analysis.jfr \
  settings=profile

# 录制完成后可以用 JDK Mission Control (JMC) 打开分析
# 也可以用 jfr 命令行工具快速查看
jfr summary /logs/gc-analysis.jfr
```

查看 GC 相关事件：

```bash
jfr print --events jdk.GCPhasePause /logs/gc-analysis.jfr      # GC pause 事件
jfr print --events jdk.ObjectAllocationSample /logs/gc-analysis.jfr  # 分配热点
```

### 3.4 使用 jcmd 分析堆内存

```bash
jcmd 12345 GC.heap_info
```

示意输出：

```
garbage-first heap   total 8388608K, used 6891520K (82.14%)
  region size 4096K, 512 young (2097152K), 24 survivors (98304K)
 Metaspace       used 128456K, committed 131072K, reserved 196608K
```

**注意**：Region Size 为默认 4MB，意味着 >2MB 的对象即为 Humongous Object。

---

## 4. 第二阶段：GC 日志诊断

### 4.1 典型 Young GC 日志

以下为示意日志片段（示意日志，基于 JDK 21 Unified Logging 格式）：

```
[2025-03-15T14:23:45.123+0800][info][gc,start     ] GC(4521) Pause Young (Normal) (G1 Evacuation Pause)
[2025-03-15T14:23:45.123+0800][info][gc,task      ] GC(4521) Using 8 workers of 8 for evacuation
[2025-03-15T14:23:45.145+0800][info][gc,phases    ] GC(4521)   Pre Evacuate Collection Set: 0.3ms
[2025-03-15T14:23:45.145+0800][info][gc,phases    ] GC(4521)   Merge Heap Roots: 0.4ms
[2025-03-15T14:23:45.145+0800][info][gc,phases    ] GC(4521)   Evacuate Collection Set: 18.7ms
[2025-03-15T14:23:45.145+0800][info][gc,phases    ] GC(4521)   Post Evacuate Collection Set: 2.1ms
[2025-03-15T14:23:45.145+0800][info][gc,phases    ] GC(4521)   Other: 0.5ms
[2025-03-15T14:23:45.145+0800][info][gc,heap      ] GC(4521) Eden regions: 410->0(398)
[2025-03-15T14:23:45.145+0800][info][gc,heap      ] GC(4521) Survivor regions: 24->36(64)
[2025-03-15T14:23:45.145+0800][info][gc,heap      ] GC(4521) Old regions: 1102->1118
[2025-03-15T14:23:45.145+0800][info][gc,heap      ] GC(4521) Humongous regions: 48->42
[2025-03-15T14:23:45.145+0800][info][gc           ] GC(4521) Pause Young (Normal) (G1 Evacuation Pause) 6324M->4788M(8192M) 22.0ms
```

**分析要点**：
- Young GC 暂停 22ms，在可接受范围内
- **Humongous regions: 48->42** — 存在大量 Humongous Allocation（大对象分配）
- Old regions 持续增长（1102→1118），晋升速率偏高

### 4.2 Mixed GC 日志

```
[2025-03-15T14:25:12.456+0800][info][gc,start     ] GC(4530) Pause Young (Mixed) (G1 Evacuation Pause)
[2025-03-15T14:25:12.456+0800][info][gc,task      ] GC(4530) Using 8 workers of 8 for evacuation
[2025-03-15T14:25:12.512+0800][info][gc,phases    ] GC(4530)   Evacuate Collection Set: 48.3ms
[2025-03-15T14:25:12.516+0800][info][gc           ] GC(4530) Pause Young (Mixed) (G1 Evacuation Pause) 5890M->4120M(8192M) 56.2ms
```

**分析要点**：
- Mixed GC 暂停 56ms，偏高但未超过 MaxGCPauseMillis(200ms)
- Mixed GC 回收了约 1.7GB（从 5890M 降到 4120M），说明老年代碎片化

### 4.3 Full GC — 关键问题

```
[2025-03-15T14:28:03.678+0800][info][gc,start     ] GC(4542) Pause Full (G1 Evacuation Pause)
[2025-03-15T14:28:03.678+0800][info][gc,phases,start] GC(4542) Phase 1: Mark live objects
[2025-03-15T14:28:03.890+0800][info][gc,phases    ] GC(4542) Phase 1: Mark live objects 212.3ms
[2025-03-15T14:28:03.890+0800][info][gc,phases,start] GC(4542) Phase 2: Prepare for compaction
[2025-03-15T14:28:03.978+0800][info][gc,phases    ] GC(4542) Phase 2: Prepare for compaction 88.1ms
[2025-03-15T14:28:03.978+0800][info][gc,phases,start] GC(4542) Phase 3: Adjust pointers
[2025-03-15T14:28:04.112+0800][info][gc,phases    ] GC(4542) Phase 3: Adjust pointers 134.2ms
[2025-03-15T14:28:04.112+0800][info][gc,phases,start] GC(4542) Phase 4: Compact heap
[2025-03-15T14:28:04.198+0800][info][gc,phases    ] GC(4542) Phase 4: Compact heap 86.0ms
[2025-03-15T14:28:04.200+0800][info][gc,heap      ] GC(4542) Eden regions: 0->0(410)
[2025-03-15T14:28:04.200+0800][info][gc,heap      ] GC(4542) Survivor regions: 0->0(0)
[2025-03-15T14:28:04.200+0800][info][gc,heap      ] GC(4542) Old regions: 1856->1245
[2025-03-15T14:28:04.200+0800][info][gc,heap      ] GC(4542) Humongous regions: 56->12
[2025-03-15T14:28:04.200+0800][info][gc           ] GC(4542) Pause Full (G1 Evacuation Pause) 7834M->5012M(8192M) 522.1ms
```

**关键发现**：

| 问题 | 日志证据 | 根因分析 |
|------|----------|----------|
| Full GC 暂停过长 | `Pause Full ... 522.1ms` | 8GB 堆做 Full Compaction，STW 不可避免 |
| Humongous Allocation | `Humongous regions: 56->12` | 大对象（>Region Size/2 = 2MB）直接分配到老年代 |
| To-space Exhaustion | Full GC 触发原因 | Mixed GC 来不及回收，老年代空间不足 |
| 并发标记启动过晚 | IHOP 默认值偏高 | 并发标记周期未能在老年代填满前完成 |

### 4.5 问题根因总结

通过以上分析，确定了三个核心问题：

1. **Humongous Allocation 过多**：订单服务中存在大量序列化操作（JSON 序列化、Kafka 消息体），产生超过 2MB 的 byte[] 数组，被 G1 视为 Humongous Object，直接进入老年代。

2. **IHOP（Initiating Heap Occupancy Percent）不合理**：G1 的自适应 IHOP 在此场景下触发并发标记过晚，导致 Mixed GC 无法及时回收老年代。

3. **Region Size 偏小**：4MB 的 Region Size 意味着 >2MB 的对象即为 Humongous，增大 Region Size 可以减少 Humongous Allocation。

---

## 5. 第三阶段：G1 GC 调优

### 5.1 第一轮调优参数

```bash
java \
  -Xms8g -Xmx8g \
  -XX:+UseG1GC \
  -XX:MaxGCPauseMillis=100 \
  -XX:G1HeapRegionSize=16m \
  -XX:InitiatingHeapOccupancyPercent=45 \
  -XX:-G1UseAdaptiveIHOP \
  -XX:G1MixedGCCountTarget=16 \
  -XX:G1HeapWastePercent=5 \
  -XX:+UseStringDeduplication \
  -XX:G1NewSizePercent=25 \
  -XX:G1MaxNewSizePercent=40 \
  -Xlog:gc*=info:file=/logs/gc-detail.log:time,uptime,level,tags:filecount=10,filesize=100m \
  -jar order-service.jar
```

### 5.2 参数变更说明

| 参数 | Before | After | 调整理由 |
|------|--------|-------|----------|
| `G1HeapRegionSize` | 4m (自动) | 16m | 减少 Humongous Allocation，大对象阈值从 2MB 提升到 8MB |
| `MaxGCPauseMillis` | 200 | 100 | 收紧暂停目标，让 G1 更积极地做 Young GC |
| `InitiatingHeapOccupancyPercent` | 自适应 | 45 | 提前启动并发标记周期 |
| `G1UseAdaptiveIHOP` | true | false | 禁用自适应 IHOP，使用固定阈值更可控 |
| `G1MixedGCCountTarget` | 8 | 16 | 增加 Mixed GC 轮次，每轮回收量更小，暂停更短 |
| `G1HeapWastePercent` | 10 | 5 | 降低浪费容忍度，更积极回收老年代 |
| `G1NewSizePercent` | 5 | 25 | 保证年轻代最小占比，减少对象过早晋升 |
| `G1MaxNewSizePercent` | 60 | 40 | 限制年轻代上限，为老年代预留空间 |

### 5.3 第一轮调优效果

部署后观察 24 小时：

| 指标 | 调优前 | 第一轮调优后 | 变化 |
|------|--------|-------------|------|
| Young GC 平均暂停 | 22ms | 15ms | -32% |
| Mixed GC 平均暂停 | 56ms | 35ms | -38% |
| Full GC 频率 | 2-5 次/小时 | 0-1 次/小时 | 显著下降 |
| Full GC 平均暂停 | 522ms | 480ms | 略有下降 |
| P99 延迟 | 200-500ms | 80-200ms | 改善明显 |
| Humongous Regions | 48-56 | 8-12 | 大幅减少 |

> 以上为示意数据，实际结果取决于工作负载。

### 5.4 效果评估

**改善**：Humongous Allocation 基本解决，Full GC 频率显著下降，P99 延迟改善。

**仍不理想**：Full GC 暂停仍达 480ms，一旦触发即违反 SLA。**根本矛盾**：G1 的 Full GC 是 Serial Full GC（单线程全堆压缩），8GB 堆下暂停时间无法根本性降低。

---

## 6. 第四阶段：切换 ZGC

### 6.1 决策分析

G1 调优已接近极限，核心瓶颈在于：
- G1 的 Young GC 和 Mixed GC 都是 STW（Stop-The-World）
- Full GC 更是 Serial 的，暂停时间与堆大小成正比

对于"P99 < 50ms"的严格 SLA，需要考虑低延迟 GC：

| 特性 | G1 GC | ZGC | Shenandoah |
|------|-------|-----|------------|
| 最大暂停目标 | 通常 10-200ms | 通常 < 1ms | 通常 < 10ms |
| 暂停是否与堆大小相关 | 是 | 否 | 否 |
| 吞吐量 | 较好 | 略低（约 3-5%） | 略低（约 3-5%） |
| JDK 21 成熟度 | 非常成熟 | 生产就绪（Generational ZGC） | 生产就绪 |
| 并发阶段 | 标记+部分回收 | 标记+转移+重定位 | 标记+压缩 |
| 容器环境支持 | 优秀 | 优秀 | 优秀 |

### 6.2 ZGC 初始配置

```bash
java \
  -Xms8g -Xmx8g \
  -XX:+UseZGC \
  -XX:+ZGenerational \
  -Xlog:gc*=info:file=/logs/gc-zgc.log:time,uptime,level,tags:filecount=10,filesize=100m \
  -jar order-service.jar
```

**关键参数说明**：
- `-XX:+UseZGC`：启用 ZGC
- `-XX:+ZGenerational`：启用 Generational ZGC（JDK 21 引入，分代式 ZGC，比经典 ZGC 吞吐量更好）
- 暂时使用默认参数，ZGC 本身需要的手动调优非常少

### 6.3 ZGC 日志分析

切换后的 GC 日志（示意日志）：

```
[2025-03-16T10:15:23.456+0800][info][gc,start  ] GC(128) Minor Collection (Allocation Rate)
[2025-03-16T10:15:23.456+0800][info][gc,phases ] GC(128) Pause Mark Start 0.023ms
[2025-03-16T10:15:23.478+0800][info][gc,phases ] GC(128) Concurrent Mark Young 21.456ms
[2025-03-16T10:15:23.478+0800][info][gc,phases ] GC(128) Pause Mark End 0.018ms
[2025-03-16T10:15:23.481+0800][info][gc,phases ] GC(128) Pause Relocate Start 0.015ms
[2025-03-16T10:15:23.498+0800][info][gc,phases ] GC(128) Concurrent Relocate 16.789ms
[2025-03-16T10:15:23.498+0800][info][gc        ] GC(128) Minor Collection (Allocation Rate) 4812M->3456M(8192M) 41.234ms
[2025-03-16T10:15:23.498+0800][info][gc        ] GC(128)   Total Pause: 0.056ms
```

**关键观察**：
- **Total Pause: 0.056ms** — ZGC 的三个 STW 阶段（Mark Start / Mark End / Relocate Start）都在亚毫秒级
- 大量工作在 Concurrent 阶段完成，不阻塞应用线程
- ZGC 没有 Full GC 概念，所有回收都是并发的

### 6.4 ZGC 初始效果（示意数据）

| 指标 | G1 调优后 | ZGC 初始 | 变化 |
|------|----------|----------|------|
| P99 延迟 | 80-200ms | 12-18ms | 大幅改善 |
| 最大 GC 暂停 | 480ms | 0.3ms | 质变 |
| 吞吐量 (QPS) | 3200 | 3100 | 下降约 3% |
| CPU 使用率 | 45% | 52% | 上升约 7% |

**评估**：P99 远低于 50ms SLA 目标；吞吐量下降约 3%、CPU 上升约 7%（ZGC 并发阶段消耗 CPU），当前仍有余量。

---

## 7. 第五阶段：ZGC 精调与最终方案

### 7.1 优化吞吐量

ZGC 吞吐量略降的原因是并发 GC 线程竞争 CPU + load barrier 开销。调优方向：**增大堆内存，减少 GC 频率**。

```bash
# 容器 16GB 内存，之前只用了 8GB 作为堆
# 适当增大到 12GB，为操作系统和 JVM 非堆预留 4GB
java \
  -Xms12g -Xmx12g \
  -XX:+UseZGC \
  -XX:+ZGenerational \
  -XX:SoftMaxHeapSize=10g \
  -XX:ConcGCThreads=4 \
  -XX:+UseLargePages \
  -XX:+UseTransparentHugePages \
  -Xlog:gc*=info:file=/logs/gc-zgc-tuned.log:time,uptime,level,tags:filecount=10,filesize=100m \
  -jar order-service.jar
```

### 7.2 新增参数说明

| 参数 | 值 | 说明 |
|------|-----|------|
| `-Xmx` | 12g（原 8g） | 增大堆减少 GC 频率，提升吞吐量 |
| `-XX:SoftMaxHeapSize` | 10g | ZGC 特有参数。正常情况下堆使用不超过 10GB，突发时可扩展到 12GB |
| `-XX:ConcGCThreads` | 4 | 限制并发 GC 线程数（默认为 CPU 核心数/4）。8 核机器默认 2，适当增加以加快并发回收 |
| `-XX:+UseTransparentHugePages` | 启用 | 使用大页内存（Transparent Huge Pages），减少 TLB miss，提升 ZGC 性能 |

> **关于 `SoftMaxHeapSize`**：这是 ZGC 的一个巧妙参数。它设置一个"软上限"，GC 会尽量让堆使用量不超过这个值，但在分配压力大时允许临时超过。相当于在吞吐量和内存占用之间做了一个弹性平衡。

### 7.3 应用层面优化（配合 GC 调优）

GC 调优不应只依赖 JVM 参数，应用层面的优化同样重要：

```java
// 问题代码：订单序列化时创建大量临时对象
// 每次请求都 new ObjectMapper() + 序列化大订单列表
public String serializeOrders(List<Order> orders) {
    ObjectMapper mapper = new ObjectMapper();  // 每次创建新实例
    return mapper.writeValueAsString(orders);  // 大列表产生大 byte[]
}

// 优化后：复用 ObjectMapper，使用流式序列化
private static final ObjectMapper MAPPER = new ObjectMapper();

public void serializeOrders(List<Order> orders, OutputStream out) {
    MAPPER.writeValue(out, orders);  // 流式写出，避免内存中持有完整字符串
}
```

```java
// 问题代码：Kafka 消息体过大
// 单条消息包含完整订单 + 所有明细 + 用户信息
producer.send(new ProducerRecord<>("orders", fullOrderJson));

// 优化后：只发送必要字段，明细通过 ID 查询获取
producer.send(new ProducerRecord<>("orders", minimalOrderEvent));
```

### 7.4 最终启动参数

```bash
#!/bin/bash
# order-service 最终 JVM 启动配置
# 最后更新: 2025-03

JAVA_OPTS="\
  -Xms12g \
  -Xmx12g \
  -XX:+UseZGC \
  -XX:+ZGenerational \
  -XX:SoftMaxHeapSize=10g \
  -XX:ConcGCThreads=4 \
  -XX:+UseTransparentHugePages \
  -XX:+AlwaysPreTouch \
  -XX:+DisableExplicitGC \
  -XX:MaxMetaspaceSize=512m \
  -XX:MetaspaceSize=256m \
  -Xlog:gc*=info,gc+phases=debug:file=/logs/gc.log:time,uptime,level,tags:filecount=10,filesize=100m \
  -XX:+HeapDumpOnOutOfMemoryError \
  -XX:HeapDumpPath=/logs/heapdump.hprof \
  -XX:+ExitOnOutOfMemoryError \
"

exec java $JAVA_OPTS -jar order-service.jar
```

**补充参数说明**：
- `-XX:+AlwaysPreTouch`：启动时预分配所有堆内存页，避免运行时延迟（增加启动时间约 2-5 秒）
- `-XX:+DisableExplicitGC`：禁止 `System.gc()` 触发 GC
- `-XX:+ExitOnOutOfMemoryError`：OOM 时退出 JVM，让 Kubernetes 重启 Pod，避免半死不活状态

---

## 8. 决策记录：为什么选 ZGC 而非 Shenandoah

这是团队内部讨论后的决策记录（ADR 风格）。

### 8.1 两者对比

| 维度 | ZGC (Generational) | Shenandoah |
|------|-------------------|------------|
| 暂停时间 | 亚毫秒级（< 1ms） | 通常 < 10ms，优化后可 < 1ms |
| 实现机制 | Load Barrier（染色指针 + 读屏障） | Brooks Pointer（转发指针） |
| JDK 21 状态 | 正式 GA（Generational ZGC） | 正式 GA |
| 分代支持 | JDK 21 起支持分代 ZGC | 无分代（实验性分代支持在开发中） |
| Oracle JDK 支持 | 支持 | 不支持（仅 OpenJDK 系） |
| 社区活跃度 | Red Hat + Oracle 双方投入 | 主要由 Red Hat 维护 |
| 大堆表现（>16GB） | 优秀 | 优秀 |
| 中小堆表现（8-16GB） | 优秀（分代 ZGC 改善明显） | 优秀 |

### 8.2 决策理由

选择 ZGC 的主要原因：

1. **Generational ZGC 更成熟**：JDK 21 中 Generational ZGC 正式 GA，分代策略让它在中等堆（8-16GB）场景下表现更好——Young Generation 的高频回收减少了并发标记的压力。

2. **更低的暂停时间上界**：ZGC 的架构设计保证暂停时间与堆大小、存活对象数量都无关。Shenandoah 虽然也很优秀，但在某些极端场景下暂停可能略高。

3. **JDK 发行版兼容性**：团队使用 Eclipse Temurin（基于 OpenJDK），两者都支持。但考虑到未来可能迁移到 Oracle JDK 或其他商业发行版，ZGC 的兼容性更广。

4. **团队经验**：团队此前有 ZGC 的调优经验（另一个服务已使用 ZGC），而 Shenandoah 的运维经验为零。生产环境优先选择团队熟悉的方案。

> **原则**：GC 选型没有绝对的"最佳"，只有"最适合当前场景"的选择。Shenandoah 在 Red Hat 系 JDK 环境或团队已有相关经验时同样是优秀选择。

---

## 9. 最终效果对比

### 9.1 全阶段对比表

> 以下所有数据为示意数据，实际结果取决于工作负载。

| 指标 | 初始（G1 默认） | G1 调优后 | ZGC 初始 | ZGC 精调（最终） |
|------|----------------|----------|----------|----------------|
| **P50 延迟** | 8ms | 7ms | 9ms | 7ms |
| **P99 延迟** | 200-500ms | 80-200ms | 12-18ms | 8-12ms |
| **P999 延迟** | 500-1200ms | 300-500ms | 20-35ms | 15-22ms |
| **最大 GC 暂停** | 800ms | 480ms | 0.3ms | 0.2ms |
| **GC 暂停频率** | Young: 50/min | Young: 60/min | — | — |
| | Full: 2-5/hr | Full: 0-1/hr | 无 Full GC | 无 Full GC |
| **吞吐量 (QPS)** | 3200 | 3200 | 3100 | 3180 |
| **CPU 使用率** | 45% | 45% | 52% | 48% |
| **堆内存** | 8GB | 8GB | 8GB | 12GB |
| **SLA 达标率** | 95.2% | 98.5% | 99.9% | 99.97% |

### 9.2 大促压测对比

在 12,000 QPS 压测环境下的表现：

| 指标 | 初始（G1 默认） | 最终（ZGC 精调） |
|------|----------------|----------------|
| P99 延迟 | 800-2000ms | 15-25ms |
| 最大暂停 | 2.3s | 0.5ms |
| Full GC 次数（30 分钟） | 12 次 | 0 次 |
| 错误率 | 0.3%（超时导致） | 0.01% |

### 9.3 JFR 对比验证

最终方案部署后，通过 JFR 录制 10 分钟数据进行回归验证：

```bash
jcmd $(pgrep -f order-service) JFR.start \
  name=final-validation duration=10m \
  filename=/logs/final-validation.jfr settings=profile

# 查看 GC 暂停分布
jfr print --events jdk.GCPhasePause /logs/final-validation.jfr
```

使用 JMC 打开 `.jfr` 文件，重点关注 GC 页签的暂停时间分布直方图和 Memory 页签的堆使用趋势。

---

## 10. 经验总结与 Checklist

### 10.1 GC 调优方法论

```
Step 1: 确定目标
  ↓ 延迟优先 or 吞吐量优先？SLA 是什么？
Step 2: 收集数据
  ↓ GC 日志、jstat、JFR、APM 监控
Step 3: 分析根因
  ↓ 是 GC 算法问题还是应用层问题？
Step 4: 制定方案
  ↓ 参数调优 → 换 GC 算法 → 应用优化
Step 5: 验证效果
  ↓ A/B 测试、压测、持续监控
Step 6: 持续观察
    生产环境运行至少一个完整业务周期
```

### 10.2 GC 选型快速参考

| 场景 | 推荐 GC | 理由 |
|------|---------|------|
| 通用场景（无特殊要求） | G1 GC | JDK 默认，成熟稳定 |
| 延迟敏感（P99 < 50ms） | ZGC / Shenandoah | 亚毫秒级暂停 |
| 大堆（>32GB） | ZGC | 暂停不随堆增大 |
| 极致吞吐量 | Parallel GC | 吞吐量最高 |
| 小堆（<1GB）+ 短生命周期 | Serial GC / Epsilon | 简单高效 |

### 10.3 排查 Checklist

**数据收集阶段**：
- [ ] 开启详细 GC 日志（`-Xlog:gc*=info`）
- [ ] 使用 `jstat -gcutil` 观察堆各区使用率趋势
- [ ] 录制 JFR 快照（至少 5 分钟，覆盖业务高峰）
- [ ] 收集 APM/Prometheus 中的延迟数据作为对照

**G1 GC 常见问题 Checklist**：
- [ ] 检查 Humongous Allocation（日志中 `Humongous regions` 数值是否偏高）
- [ ] 检查 To-space Exhaustion（是否触发 Full GC，原因是否为空间不足）
- [ ] 检查并发标记是否及时启动（IHOP 是否合理）
- [ ] 检查 Mixed GC 是否充分回收（`G1HeapWastePercent` 是否过高）
- [ ] 检查 Region Size 是否合理（大对象阈值 = RegionSize / 2）
- [ ] 检查 Young 区大小是否合理（过小导致频繁 GC，过大导致单次 GC 慢）

**ZGC 注意事项**：
- [ ] JDK 21+ 优先使用 Generational ZGC（`-XX:+ZGenerational`）
- [ ] 预留足够的非堆内存（ZGC 需要额外的 off-heap 内存用于染色指针映射）
- [ ] 考虑使用 `-XX:SoftMaxHeapSize` 做弹性控制
- [ ] 开启 `-XX:+AlwaysPreTouch` 避免运行时内存分配延迟
- [ ] 监控 CPU 使用率（并发 GC 会消耗额外 CPU）

### 10.4 容器环境注意事项

- 使用 `jcmd <pid> VM.info | grep "container"` 确认 JVM 正确识别容器资源限制
- JDK 21 默认支持容器感知（Container Awareness）
- **关键原则**：`-Xmx` 不超过容器 memory limit 的 75%（16GB 容器 → `-Xmx` 不超过 12GB，为 OS、Metaspace、直接内存预留）

### 10.5 不要过度调优

最后也是最重要的提醒：

1. **先优化应用代码，再调 GC**。减少不必要的对象分配比任何 GC 参数都有效。
2. **参数不是越多越好**。JDK 21 的 G1 和 ZGC 默认值已经很好，大多数场景只需设置 `-Xmx` 和选择 GC 算法。
3. **每次只改一个变量**。否则无法判断哪个参数起了作用。
4. **持续监控**。GC 调优不是一次性工作，业务增长后可能需要重新评估。

---

> **全文声明**：本案例中所有 GC 日志、监控指标、性能数据均为 **示意数据（illustrative data）**，仅用于展示调优思路和方法论。实际结果取决于工作负载（workload）、硬件配置（hardware）、JDK 版本和应用特征。在生产环境中进行 GC 调优时，请务必基于实际采集的数据做决策。
