# G1 vs ZGC vs Shenandoah: 垃圾收集器全面对比指南

> **一句话总结 (One-Line Summary)**
>
> - **G1**: 平衡型选手 — 吞吐量与延迟兼顾, 适合大多数通用场景 (balanced throughput & latency)
> - **ZGC**: 超低延迟 — 亚毫秒暂停, 适合大堆与延迟敏感型应用 (sub-ms pauses, any heap size)
> - **Shenandoah**: 低延迟先驱 — 与 ZGC 目标相似, Red Hat 主导, 更早可用 (low-latency, concurrent compaction)

---

## 目录

1. [核心设计理念](#核心设计理念)
2. [多维度对比表](#多维度对比表)
3. [决策流程图](#决策流程图)
4. [场景推荐](#场景推荐)
5. [关键参数映射表](#关键参数映射表)
6. [JDK 版本推荐](#jdk-版本推荐)
7. [GC 日志对比](#gc-日志对比)
8. [常见误区](#常见误区)
9. [总结](#总结)

---

## 核心设计理念

### G1 (Garbage-First)

G1 将堆划分为等大的 Region, 优先回收垃圾最多的 Region (hence "Garbage-First").
它在 Young GC 和 Mixed GC 之间交替, 通过 `-XX:MaxGCPauseMillis` 控制暂停目标.

```
Heap Layout (Region-based):
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│ E   │ E   │ S   │  O  │  O  │ H   │  O  │ E   │
│(Eden)│(Eden)│(Surv)│(Old)│(Old)│(Hum)│(Old)│(Eden)│
└─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘
E = Eden, S = Survivor, O = Old, H = Humongous
```

- **Stop-the-World**: Young GC + Mixed GC 都有 STW 暂停
- **并发阶段**: Concurrent Marking 是并发的, 但 Compaction 不是
- **目标暂停时间**: 默认 200ms, 可调至 50-100ms

### ZGC (Z Garbage Collector)

ZGC 使用 colored pointers (染色指针) 和 load barriers (读屏障) 实现几乎完全并发的收集.

```
Colored Pointer (64-bit):
┌──────────┬───┬───┬───┬───┬──────────────────────┐
│ unused   │ F │ R │ M1│ M0│   Object Address     │
│ (16 bits)│   │   │   │   │   (44 bits = 16 TB)  │
└──────────┴───┴───┴───┴───┴──────────────────────┘
F = Finalizable, R = Remapped, M0/M1 = Marked
```

- **STW 极短**: 仅 root scanning 阶段 (通常 < 1ms)
- **并发阶段**: Marking, Relocation, Remapping 全部并发
- **无分代 → 分代**: JDK 21 引入 Generational ZGC (`-XX:+ZGenerational`), JDK 23 默认分代

### Shenandoah

Shenandoah 使用 Brooks forwarding pointers 实现并发 compaction.

```
Object with Brooks Pointer:
┌────────────────┬──────────────────┐
│ Brooks Pointer │   Object Data    │
│ (fwd ref)      │                  │
└────────────────┴──────────────────┘
  ↓ (points to new copy during relocation)
┌────────────────┬──────────────────┐
│ Brooks Pointer │   Object Data    │
│ (self-ref)     │   (new copy)     │
└────────────────┴──────────────────┘
```

- **STW**: Init Mark, Final Mark, Init Update Refs — 各约 1-5ms
- **并发阶段**: Concurrent Mark, Concurrent Evacuation, Concurrent Update Refs
- **注意**: Oracle JDK 不包含 Shenandoah, 需使用 OpenJDK 或其他发行版

---

## 多维度对比表

| 维度 (Dimension)            | G1                          | ZGC                         | Shenandoah                  |
|----------------------------|-----------------------------|-----------------------------|------------------------------|
| **最大暂停时间 (Max Pause)** | 50-200ms (typical)         | < 1ms (sub-millisecond)     | 1-10ms (typical)             |
| **吞吐量 (Throughput)**     | ★★★★★ 最高               | ★★★★ 略低 (~3-5%)          | ★★★★ 略低 (~3-5%)          |
| **最小堆大小 (Min Heap)**   | 几十 MB 即可               | 8MB (JDK 21+), 推荐 256MB+ | 推荐 256MB+                  |
| **最大堆大小 (Max Heap)**   | 数十 GB (实践上限)         | 16 TB                       | 数 TB                        |
| **内存开销 (Memory OH)**    | ~5-10% (remembered sets)   | ~3-5% (colored pointers)    | ~5-10% (forwarding ptrs)    |
| **CPU 开销 (CPU OH)**       | 中等                       | 较高 (load barriers)        | 较高 (read/write barriers)   |
| **GC 线程数**               | `-XX:ParallelGCThreads`    | `-XX:ConcGCThreads`         | `-XX:ConcGCThreads`          |
| **延迟抖动 (Jitter)**       | 中等, Mixed GC 可能突增    | 极低, 非常平稳              | 低, 偶有小抖动               |
| **启动时间 (Startup)**      | 快                         | 稍慢 (mmap 开销)            | 与 G1 相当                   |
| **预热时间 (Warmup)**       | 需要几轮 GC 自适应         | 较快稳定                    | 较快稳定                     |
| **容器适配 (Container)**    | 优秀, 默认识别 cgroup      | 优秀, JDK 17+               | 良好                         |
| **压缩类指针 (CompOops)**   | 支持 (堆 < 32GB)           | 支持 (JDK 21+, 堆 < 32GB)  | 支持 (堆 < 32GB)             |
| **NUMA 感知**               | 支持                       | 支持                        | 支持                         |
| **String Dedup**            | 支持                       | 支持 (JDK 18+)              | 支持                         |
| **成熟度 (Maturity)**       | 非常成熟 (JDK 9 默认)      | 生产就绪 (JDK 17+)          | 生产就绪 (JDK 17+)           |
| **Oracle JDK 可用**         | 是                         | 是                          | 否 (仅 OpenJDK 发行版)       |
| **默认 GC**                 | JDK 9+ 默认                | 否                          | 否                           |

### 暂停时间实测参考 (Pause Time Benchmarks)

以 16GB 堆, 中等分配压力为例:

```
暂停时间分布 (Pause Time Distribution):

G1:        [============================] p50=8ms  p99=85ms  max=200ms
ZGC:       [=]                            p50=0.1ms p99=0.5ms max=1ms
Shenandoah:[===]                          p50=1ms  p99=5ms   max=10ms

吞吐量 (归一化, G1 = 100%):

G1:        [██████████████████████████████] 100%
ZGC:       [████████████████████████████ ] 95-97%
Shenandoah:[████████████████████████████ ] 95-97%
```

> **注意**: 实际数据高度依赖工作负载 (workload-dependent). 以上仅为典型范围参考.

---

## 决策流程图

```
                    ┌─────────────────────┐
                    │ 选择 GC Collector   │
                    └────────┬────────────┘
                             │
                   ┌─────────▼──────────┐
                   │ 延迟要求 < 10ms?   │
                   └──┬─────────────┬───┘
                      │ Yes         │ No
                      ▼             ▼
            ┌─────────────────┐  ┌──────────────────┐
            │ 堆 > 32GB?      │  │ 吞吐量优先?      │
            └──┬──────────┬───┘  └──┬───────────┬───┘
               │ Yes      │ No      │ Yes       │ No
               ▼          ▼         ▼           ▼
        ┌──────────┐ ┌────────┐ ┌────────┐ ┌────────────┐
        │ 要求亚ms │ │暂停<1ms│ │  G1    │ │ G1 (默认)  │
        │ 暂停?    │ │ 要求?  │ │ 足够好 │ │ 先试再说   │
        └──┬───┬───┘ └──┬──┬──┘ └────────┘ └────────────┘
           │Y  │N       │Y │N
           ▼   ▼        ▼  ▼
       ┌─────┐┌────┐┌─────┐┌──────────┐
       │ ZGC ││Shen││ ZGC ││ ZGC 或   │
       │     ││    ││     ││ Shenandoah│
       └─────┘└────┘└─────┘└──────────┘

  补充决策:
  ┌──────────────────────────────────────────────┐
  │ 使用 Oracle JDK?  ──Yes──►  G1 或 ZGC       │
  │ 需要最大吞吐量?   ──Yes──►  G1               │
  │ 容器 < 512MB 内存? ──Yes──► G1 (Serial 备选) │
  │ JDK 8 / JDK 11?   ──Yes──► G1 (ZGC 实验性)  │
  └──────────────────────────────────────────────┘
```

---

## 场景推荐

### 1. Web 服务 / API Gateway

| 特征                | 推荐 GC    | 原因                                    |
|---------------------|-----------|----------------------------------------|
| 一般 Web 应用 (< 8GB) | **G1**    | 默认即可, 暂停时间足够, 吞吐量最优       |
| 高并发低延迟 API      | **ZGC**   | p99 延迟要求严格时, ZGC 的亚毫秒暂停无敌  |
| 大型网关 (> 16GB)    | **ZGC**   | 大堆下 G1 暂停可能突破 200ms             |

```bash
# 一般 Web 应用 — G1 (默认, 无需额外配置)
java -Xmx4g -XX:MaxGCPauseMillis=100 -jar web-app.jar

# 高并发低延迟 API — ZGC
java -Xmx8g -XX:+UseZGC -jar api-gateway.jar

# JDK 23+ 分代 ZGC 默认启用, 吞吐量更好
java -Xmx8g -XX:+UseZGC -jar api-gateway.jar
```

### 2. 批处理 / 大数据 (Batch Processing / Big Data)

| 特征                    | 推荐 GC | 原因                              |
|------------------------|---------|----------------------------------|
| Spark/Flink Executor   | **G1**  | 吞吐量优先, 暂停可接受             |
| 大堆内存计算 (> 64GB)   | **ZGC** | 避免 G1 Full GC 长暂停            |

```bash
# Spark Executor — G1
spark.executor.extraJavaOptions=-XX:+UseG1GC -XX:MaxGCPauseMillis=200

# 大堆内存计算 — ZGC
java -Xmx128g -XX:+UseZGC -jar in-memory-compute.jar
```

### 3. 微服务 / 容器 (Microservices / Containers)

| 特征                   | 推荐 GC | 原因                              |
|-----------------------|---------|----------------------------------|
| 小容器 (256MB-1GB)    | **G1**  | 内存效率好, 启动快                 |
| 中等容器 (2-8GB)      | **G1**  | 默认最佳选择                       |
| 延迟敏感容器           | **ZGC** | 即使小堆也能保证低延迟              |

```bash
# 容器推荐配置 — G1
java -XX:+UseG1GC \
     -XX:MaxRAMPercentage=75.0 \
     -XX:InitialRAMPercentage=50.0 \
     -jar microservice.jar

# 容器推荐配置 — ZGC
java -XX:+UseZGC \
     -XX:MaxRAMPercentage=75.0 \
     -XX:SoftMaxHeapSize=1500m \
     -jar microservice.jar
```

### 4. 交易系统 / 金融 (Trading / Finance)

| 特征                  | 推荐 GC    | 原因                                 |
|----------------------|-----------|--------------------------------------|
| 高频交易 (HFT)       | **ZGC**   | 亚毫秒暂停, 避免 GC 导致的延迟毛刺     |
| 风控系统 (大内存)     | **ZGC**   | 大堆 + 低延迟                         |
| 一般交易后台          | **G1**    | 对延迟要求不如 HFT 严格               |

```bash
# 高频交易 — ZGC, 最小化暂停
java -Xmx32g -Xms32g \
     -XX:+UseZGC \
     -XX:+AlwaysPreTouch \
     -XX:-TieredCompilation \
     -jar trading-engine.jar
```

### 5. 桌面应用 / IDE

| 特征                | 推荐 GC      | 原因                             |
|--------------------|-------------|----------------------------------|
| IDE (IntelliJ等)   | **G1/ZGC**  | IntelliJ 2024+ 默认使用 G1       |
| GUI 应用           | **ZGC**     | 避免 GC 导致的 UI 卡顿            |

---

## 关键参数映射表

从一个 GC 迁移到另一个时, 参数如何映射:

### G1 → ZGC 迁移

| G1 参数                         | ZGC 等效 / 替代                  | 说明                          |
|--------------------------------|----------------------------------|------------------------------|
| `-XX:+UseG1GC`                 | `-XX:+UseZGC`                    | 切换收集器                    |
| `-XX:MaxGCPauseMillis=200`     | 不需要 (inherently low-pause)    | ZGC 暂停天然 < 1ms            |
| `-XX:G1HeapRegionSize=16m`     | N/A                              | ZGC 自动管理 region           |
| `-XX:InitiatingHeapOccupancyPercent` | `-XX:SoftMaxHeapSize`       | 控制 GC 触发时机              |
| `-XX:G1MixedGCCountTarget`     | N/A                              | ZGC 无 mixed GC 概念          |
| `-XX:G1ReservePercent`         | N/A                              | ZGC 自动管理                  |
| `-XX:ParallelGCThreads=8`      | `-XX:ConcGCThreads=4`           | ZGC 并发线程 (通常设更少)      |
| `-XX:+UseStringDeduplication`  | `-XX:+UseStringDeduplication`    | 两者都支持                    |

### G1 → Shenandoah 迁移

| G1 参数                         | Shenandoah 等效                  | 说明                          |
|--------------------------------|----------------------------------|------------------------------|
| `-XX:+UseG1GC`                 | `-XX:+UseShenandoahGC`           | 切换收集器                    |
| `-XX:MaxGCPauseMillis=200`     | `-XX:ShenandoahGuaranteedGCInterval` | 间接控制暂停               |
| `-XX:ParallelGCThreads=8`      | `-XX:ConcGCThreads=4`           | 并发线程数                    |
| N/A                            | `-XX:ShenandoahGCHeuristics=adaptive` | 启发式策略              |

### 通用参数 (所有 GC 均适用)

```bash
# 堆大小 — 所有 GC 相同
-Xmx8g -Xms8g

# GC 日志 — 统一格式 (JDK 9+)
-Xlog:gc*:file=gc.log:time,uptime,level,tags:filecount=5,filesize=50m

# 内存预触 — 减少首次访问延迟
-XX:+AlwaysPreTouch

# 容器感知 — JDK 10+ 默认开启
-XX:+UseContainerSupport
-XX:MaxRAMPercentage=75.0
```

---

## JDK 版本推荐

各 GC 在不同 JDK 版本的成熟度:

```
            JDK 11    JDK 17    JDK 21    JDK 23    JDK 25
G1:         ████████  █████████ ██████████ ██████████ ██████████
            成熟      很成熟    非常成熟    非常成熟    非常成熟

ZGC:        ████      ███████   █████████  ██████████ ██████████
            实验性    生产就绪   分代ZGC可用  分代默认   非常成熟

Shenandoah: █████     ███████   ████████   █████████  █████████
            可用      生产就绪   成熟        成熟       很成熟
```

### 具体版本建议

| GC         | 推荐最低版本  | 最佳版本          | 说明                                      |
|------------|-------------|-------------------|------------------------------------------|
| **G1**     | JDK 11      | JDK 21+           | JDK 21 有大量 G1 优化                      |
| **ZGC**    | JDK 17      | **JDK 23+**       | JDK 23 分代 ZGC 默认, 吞吐量显著提升        |
| **Shenandoah** | JDK 17  | JDK 21+           | JDK 17 开始稳定, 21 有更多优化              |

> **关键里程碑 (Key Milestones)**:
> - JDK 15: ZGC 和 Shenandoah 正式脱离实验标志 (production-ready)
> - JDK 21: Generational ZGC (JEP 439) 可选开启
> - JDK 23: Generational ZGC 成为默认模式 (JEP 474)
> - JDK 24: Non-generational ZGC 废弃

---

## GC 日志对比

### G1 典型日志

```
[2024-01-15T10:30:00.123+0800] GC(42) Pause Young (Normal) (G1 Evacuation Pause)
[2024-01-15T10:30:00.123+0800] GC(42)   ParNew: 204800K->12800K(204800K)
[2024-01-15T10:30:00.123+0800] GC(42) Pause Young (Normal) 3200M->2800M(4096M) 12.345ms
                                                                          ^^^^^^^^
                                                                     暂停时间 ~12ms
```

### ZGC 典型日志

```
[2024-01-15T10:30:00.456+0800] GC(108) Garbage Collection (Proactive)
[2024-01-15T10:30:00.456+0800] GC(108) Pause Mark Start 0.015ms
[2024-01-15T10:30:00.470+0800] GC(108) Concurrent Mark 14.000ms
[2024-01-15T10:30:00.470+0800] GC(108) Pause Mark End 0.010ms
[2024-01-15T10:30:00.490+0800] GC(108) Concurrent Relocate 20.000ms
[2024-01-15T10:30:00.490+0800] GC(108) Pause Relocate Start 0.008ms
                                                              ^^^^^
                                                  所有暂停 < 0.1ms
```

### Shenandoah 典型日志

```
[2024-01-15T10:30:00.789+0800] GC(55) Pause Init Mark 0.234ms
[2024-01-15T10:30:00.800+0800] GC(55) Concurrent marking 11.000ms
[2024-01-15T10:30:00.800+0800] GC(55) Pause Final Mark 1.234ms
[2024-01-15T10:30:00.820+0800] GC(55) Concurrent evacuation 20.000ms
[2024-01-15T10:30:00.820+0800] GC(55) Pause Init Update Refs 0.050ms
[2024-01-15T10:30:00.840+0800] GC(55) Concurrent update refs 20.000ms
                                                    暂停合计 ~1.5ms
```

---

## 常见误区

### 误区 1: "ZGC 没有 STW 暂停"

**事实**: ZGC 仍有 STW 暂停, 只是极短 (通常 < 1ms). Root scanning 阶段仍然是 stop-the-world 的. 但与 G1 的几十毫秒到数百毫秒暂停相比, 几乎可以忽略.

### 误区 2: "ZGC 吞吐量远低于 G1"

**事实**: 非分代 ZGC 吞吐量确实略低 (~3-5%), 但分代 ZGC (JDK 23+ 默认) 大幅缩小了差距. 在某些场景下分代 ZGC 吞吐量已经与 G1 持平.

### 误区 3: "小堆不适合用 ZGC"

**事实**: JDK 21+ 的 ZGC 支持最小 8MB 堆. 分代 ZGC 在小堆上表现良好. 但如果堆 < 256MB, G1 通常更合适 (内存开销更低).

### 误区 4: "Shenandoah 比 ZGC 差, 没有使用价值"

**事实**: Shenandoah 在某些场景下有优势:
- 更早可用 (JDK 12), 在 JDK 11 backport 中也可用
- 在某些中等堆大小场景下内存效率更好
- 社区活跃, Red Hat 持续投入

### 误区 5: "切换 GC 只需要换一个参数"

**事实**: 切换 GC 后需要:
1. 移除旧 GC 特有参数 (否则启动报错)
2. 重新调优堆大小 (不同 GC 内存开销不同)
3. 重新压测 (不同 GC 吞吐量特征不同)
4. 更新监控告警阈值

### 误区 6: "G1 已经过时, 应该无脑切 ZGC"

**事实**: G1 仍然是 JDK 默认 GC, 且在以下场景更优:
- 吞吐量优先的批处理任务
- 小堆 (< 1GB) 应用
- 需要最小 CPU 开销的场景
- JDK 11 环境 (ZGC 尚不成熟)

### 误区 7: "GC 调优能解决所有性能问题"

**事实**: GC 调优的收益有上限. 如果应用频繁分配大量短生命周期对象, 更好的做法是:
- 减少对象分配 (object pooling, primitive types)
- 使用 off-heap 内存 (ByteBuffer, Panama API)
- 优化数据结构

---

## 快速切换命令对照

```bash
# 当前使用 G1 (默认)
java -Xmx8g -jar app.jar

# 切换到 ZGC
java -Xmx8g -XX:+UseZGC -jar app.jar

# 切换到 Shenandoah (OpenJDK only)
java -Xmx8g -XX:+UseShenandoahGC -jar app.jar

# 查看当前使用的 GC
java -XX:+PrintFlagsFinal -version 2>&1 | grep "Use.*GC "

# 启用 GC 日志 (通用)
java -Xlog:gc*:file=gc.log:time,uptime,level,tags -jar app.jar
```

---

## 总结

| 如果你...                          | 选择        |
|-----------------------------------|------------|
| 不确定选什么                        | **G1**     |
| 需要最低延迟, 不惜一切代价           | **ZGC**    |
| 堆 > 32GB 且关注延迟               | **ZGC**    |
| 使用 OpenJDK 且需要低延迟           | **ZGC** 或 **Shenandoah** |
| 吞吐量是唯一指标                    | **G1**     |
| JDK 11 且需要低延迟                 | **Shenandoah** (backport 可用) |
| 容器环境, 内存 < 1GB               | **G1**     |

> **最终建议**: 从 G1 开始 (它是默认的). 如果 GC 暂停成为瓶颈, 先测量再切换.
> 升级到 JDK 23+ 后, 分代 ZGC 是低延迟场景的最佳选择.
