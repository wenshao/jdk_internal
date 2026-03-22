# GC 垃圾收集器 (Garbage Collection)

> 导航中心 — 从选型到调优的速查入口

[← 返回核心平台](../)

---

## 1. GC 概览 (Overview)

Java 垃圾收集器 (Garbage Collector) 自动管理堆内存 (heap memory)，回收不可达对象 (unreachable objects)，是 JVM 性能的核心支柱。GC 的选型和调优直接决定了应用的延迟特性、吞吐量上限和资源利用率。

**HotSpot 当前提供 6 种 GC 实现**:

```
生产级 GC                          特殊用途
──────────                         ─────────
Serial     — 单线程, 最小开销       Epsilon  — No-Op, 零回收 (测试/短命进程)
Parallel   — 多线程, 吞吐优先
G1         — Region-based, 默认 GC (JDK 9+)
ZGC        — 亚毫秒暂停, 染色指针
Shenandoah — 亚毫秒暂停, 并发转发
```

**为什么 GC 选型重要**:

- **延迟 (Latency)**: GC 暂停 (STW pause) 直接影响响应时间; ZGC/Shenandoah 可将暂停控制在 <10ms
- **吞吐量 (Throughput)**: GC 占用的 CPU 时间越多，应用可用时间越少; Parallel GC 吞吐量最高
- **内存效率 (Memory Footprint)**: GC 自身的元数据开销影响可用堆空间; Serial 开销最小
- **扩展性 (Scalability)**: 堆从 MB 到 TB，不同 GC 的表现差异巨大; ZGC 支持最大 16TB 堆

**核心概念速览**:

| 概念 | 英文 | 说明 |
|------|------|------|
| 分代假说 | Generational Hypothesis | 大多数对象朝生夕灭，老对象更难消亡 |
| Stop-the-World | STW | GC 暂停所有应用线程 |
| 并发回收 | Concurrent Collection | GC 与应用线程同时运行 |
| 写屏障 | Write Barrier | 拦截引用写入，维护 GC 不变式 |
| 读屏障 | Load Barrier | 拦截引用读取 (ZGC 特有) |
| 卡表 | Card Table | 记录跨代引用的数据结构 |
| Region | Region | 将堆划分为等大小区域 (G1/ZGC/Shenandoah) |

**GC 算法分类维度**:

| 维度 | 分类 | 示例 |
|------|------|------|
| 按线程数 | 单线程 / 多线程 | Serial vs Parallel |
| 按工作方式 | STW / 并发 / 增量 | Parallel (STW) vs ZGC (并发) |
| 按内存布局 | 连续分代 / Region | Parallel (连续) vs G1 (Region) |
| 按屏障类型 | 无 / 写屏障 / 读屏障 | Serial (无) / G1 (SATB写) / ZGC (Load) |

> 深入了解 GC 基础理论，参见各 GC 详解文档中的 "工作原理" 章节。

---

## 2. GC 选择指南 (Selection Guide)

### 快速决策树

```
开始
  │
  ├─ 内存 < 100MB / 单核 CPU ────────────→ Serial GC
  │
  ├─ 吞吐量优先 (批处理/后台任务) ────────→ Parallel GC
  │
  ├─ 暂停时间 < 10ms (低延迟)
  │    ├─ 需要最低暂停 (<1ms) ──────────→ ZGC
  │    └─ Red Hat/Corretto 生态 ────────→ Shenandoah
  │
  ├─ 通用服务器 / 默认选择 ──────────────→ G1 GC
  │
  └─ 性能测试 / 无 GC 基准 ──────────────→ Epsilon (No-Op GC)
```

### 按场景推荐

| 场景 | 推荐 GC | JVM 参数 | 理由 |
|------|---------|----------|------|
| 桌面/客户端应用 | G1 | `-XX:+UseG1GC` | 平衡暂停与吞吐 |
| 微服务/容器 | G1 | `-XX:+UseG1GC -XX:MaxGCPauseMillis=200` | 容器内存友好 |
| 大数据批处理 | Parallel | `-XX:+UseParallelGC` | 最大吞吐量 |
| 低延迟交易系统 | ZGC | `-XX:+UseZGC` | 暂停 <1ms |
| 大内存 (8GB+) | ZGC / Shenandoah | `-XX:+UseZGC` | 暂停与堆大小无关 |
| 内存受限 (<256MB) | Serial | `-XX:+UseSerialGC` | 最小内存开销 |
| 性能基准测试 | Epsilon | `-XX:+UseEpsilonGC` | 零 GC 干扰 |

### 版本建议

| JDK 版本 | 默认 GC | 推荐 | 备注 |
|----------|---------|------|------|
| JDK 8 | Parallel | G1 / Parallel | G1 需显式 `-XX:+UseG1GC` |
| JDK 9-22 | G1 | G1 / ZGC | ZGC 在 JDK 15 生产就绪 |
| JDK 23 | G1 | G1 / ZGC | 分代 ZGC 成为 ZGC 默认模式 (JEP 474) |
| JDK 24 | G1 | G1 / ZGC | 非分代 ZGC 已移除 (JEP 490) |
| JDK 25+ | G1 | G1 / ZGC / Shenandoah | 分代 Shenandoah 生产就绪 (JEP 521) |
| JDK 26 | G1 | G1 / ZGC / Shenandoah | G1 吞吐量改进 (JEP 522) |

### GC 快速切换命令

```bash
# Serial GC
java -XX:+UseSerialGC -jar app.jar

# Parallel GC
java -XX:+UseParallelGC -jar app.jar

# G1 GC (JDK 9+ 默认, 可省略)
java -XX:+UseG1GC -jar app.jar

# ZGC (JDK 15+, JDK 24+ 自动分代模式)
java -XX:+UseZGC -jar app.jar

# Shenandoah (JDK 15+)
java -XX:+UseShenandoahGC -jar app.jar

# Shenandoah 分代模式 (JDK 25+)
java -XX:+UseShenandoahGC -XX:ShenandoahGCMode=generational -jar app.jar

# Epsilon (JDK 11+, 需解锁实验性选项)
java -XX:+UnlockExperimentalVMOptions -XX:+UseEpsilonGC -jar app.jar
```

> 详细调优策略参见 [调优指南](tuning.md) 和 [VM 参数参考](vm-parameters.md)。

---

## 3. GC 综合对比 (Comparison)

| 维度 | Serial | Parallel | G1 | ZGC | Shenandoah |
|------|--------|----------|----|----|------------|
| **设计目标** | 简单 | 吞吐量 | 可预测暂停 | 超低延迟 | 超低延迟 |
| **暂停时间** | 长 (秒级) | 中 (百ms) | 可控 (200ms) | <1ms | <10ms |
| **吞吐量** | 低 | 最高 | 中高 | 中高 | 中 |
| **内存开销** | 最小 | 小 | 中 | 中 | 中 |
| **适用堆大小** | <100MB | 任意 | 任意 | 8MB-16TB | 任意 |
| **并发回收** | 否 | 否 | 部分 | 完全 | 完全 |
| **分代支持** | 是 | 是 | 是 | 是 (JDK 21+) | 是 (JDK 25+) |
| **首发版本** | JDK 1.0 | JDK 1.4 | JDK 7u4 | JDK 11 | JDK 12 |
| **默认 GC** | JDK 1.0-1.3 | JDK 5-8 | JDK 9+ | - | - |
| **屏障类型** | - | - | Write (SATB) | Load (染色指针) | Read+Write (Brooks) |
| **主导组织** | Oracle | Oracle | Oracle | Oracle | Red Hat/Amazon |

> 各 GC 的深度技术分析 (架构、源码、性能基准) 请参见下方详解链接。

---

## 4. 各 GC 详解 (Deep Dives)

### 核心 GC 文档

#### [G1 GC 详解](g1-gc.md) — 默认 GC, Region-based

- 将堆划分为等大小 Region (Eden/Survivor/Old/Humongous)
- 可预测暂停时间 (MaxGCPauseMillis), Young GC + Mixed GC + Full GC
- JDK 26 (JEP 522): 双卡表 (Dual Card Table) 消除写屏障同步, 吞吐量提升 5-15%
- 主导: Thomas Schatzl, Albert Mingkun Yang (Oracle)

#### [ZGC 详解](zgc.md) — 亚毫秒暂停, 染色指针

- 染色指针 (Colored Pointers): 64 位指针高位存储 GC 元数据
- 读屏障 (Load Barrier): 读取引用时自动转发到新地址
- JDK 21+ 分代模式 (JEP 439), JDK 24 移除非分代模式 (JEP 490)
- 暂停时间 <1ms, 与堆大小无关 (支持 8MB-16TB)
- 主导: Per Liden, Stefan Karlsson, Erik Osterlund (Oracle)

#### [Shenandoah 详解](shenandoah.md) — 并发回收, Brooks Pointers

- Brooks Pointers: 每个对象包含转发指针域, 支持并发转发
- 读+写屏障: 读写引用时均检查转发指针
- JDK 25 分代模式生产就绪 (JEP 521), 吞吐量接近 G1
- 主导: Aleksey Shipilev (Amazon), William Kemper (Amazon), Roman Kennke (Datadog)

#### [CMS 历史](cms.md) — 已移除, 历史参考

- HotSpot 第一个并发 GC, 标记-清除 (Mark-Sweep) 算法
- JDK 9 废弃 (JEP 291), JDK 14 移除 (JEP 363)
- 碎片化 (fragmentation) 和并发模式失败 (Concurrent Mode Failure) 是其核心问题

### 辅助文档

| 文档 | 说明 |
|------|------|
| [GC 演进时间线](timeline.md) | 从 JDK 1.0 到 JDK 26 的完整时间线 |
| [调优指南](tuning.md) | GC 选择策略与性能优化 |
| [VM 参数参考](vm-parameters.md) | GC 相关 JVM 参数完整列表 |
| [近期改进](recent-changes.md) | JDK 21-26 GC 改进汇总 |

---

## 5. JEP 演进时间线 (JEP Timeline)

| JEP | 标题 | JDK | Lead | 组织 | 状态 |
|-----|------|-----|------|------|------|
| [JEP 189](https://openjdk.org/jeps/189) | Shenandoah GC (Experimental) | 12 | Roman Kennke | Red Hat | 实验性 |
| [JEP 318](https://openjdk.org/jeps/318) | Epsilon: No-Op GC | 11 | Aleksey Shipilev | Red Hat | 正式 |
| [JEP 333](https://openjdk.org/jeps/333) | ZGC (Experimental) | 11 | Per Liden | Oracle | 实验性 |
| [JEP 363](https://openjdk.org/jeps/363) | Remove CMS GC | 14 | - | Oracle | 已移除 |
| [JEP 377](https://openjdk.org/jeps/377) | ZGC (Production) | 15 | Per Liden | Oracle | 正式 |
| [JEP 379](https://openjdk.org/jeps/379) | Shenandoah GC (Production) | 15 | Roman Kennke | Red Hat | 正式 |
| [JEP 439](https://openjdk.org/jeps/439) | Generational ZGC | 21 | Stefan Karlsson | Oracle | 正式 |
| [JEP 450](https://openjdk.org/jeps/450) | Compact Object Headers (Experimental) | 24 | Roman Kennke | Datadog | 实验性 |
| [JEP 474](https://openjdk.org/jeps/474) | ZGC: Generational Mode by Default | 23 | Stefan Karlsson | Oracle | 正式 |
| [JEP 490](https://openjdk.org/jeps/490) | ZGC: Remove Non-Generational Mode | 24 | Per Liden | Oracle | 已移除 |
| [JEP 404](https://openjdk.org/jeps/404) | Generational Shenandoah (Experimental) | 24 | William Kemper | Amazon | 实验性 |
| [JEP 519](https://openjdk.org/jeps/519) | Compact Object Headers (Product) | 25 | Roman Kennke | Datadog | 正式 |
| [JEP 521](https://openjdk.org/jeps/521) | Generational Shenandoah (Product) | 25 | William Kemper | Amazon | 正式 |
| [JEP 522](https://openjdk.org/jeps/522) | G1: Reduce Synchronization | 26 | Ivan Walulya | Oracle | 正式 |

### 版本演进概览

```
JDK 1.0   JDK 5    JDK 7    JDK 9    JDK 11   JDK 14   JDK 15   JDK 21   JDK 23   JDK 24   JDK 25   JDK 26
  │         │        │        │        │        │        │        │        │        │        │        │
Serial   Parallel  G1正式   G1默认   ZGC     移除CMS  ZGC     分代ZGC  分代ZGC  移除非   分代Shen  G1吞吐
  GC       GC      (7u4)   (JEP248) (实验)  (JEP363) (正式)  (JEP439) 默认    分代ZGC  (JEP521)  改进
                                    Shen             Shen            (JEP474) (JEP490)          (JEP522)
                                    (实验)           (正式)
```

> 完整时间线 (含非 JEP 改进) 参见 [GC 演进时间线](timeline.md) 和 [近期改进](recent-changes.md)。

---

## 6. 关键调优参数速查 (Top 10 Parameters)

| 参数 | 默认值 | 说明 | 适用 GC |
|------|--------|------|---------|
| `-Xms` / `-Xmx` | 平台相关 | 初始/最大堆大小 | 全部 |
| `-XX:MaxGCPauseMillis=N` | 200 | 目标最大暂停时间 (ms) | G1 / Parallel |
| `-XX:G1HeapRegionSize=N` | 自动 | G1 Region 大小 (1-32MB, 2的幂) | G1 |
| `-XX:ParallelGCThreads=N` | CPU核数 | 并行 GC 线程数 | 全部 |
| `-XX:ConcGCThreads=N` | 自动 | 并发 GC 线程数 | G1 / ZGC / Shenandoah |
| `-XX:GCTimeRatio=N` | 99 | GC 时间占比 = 1/(1+N) | Parallel |
| `-XX:G1ReservePercent=N` | 10 | G1 保留堆空间百分比 | G1 |
| `-XX:ZCollectionInterval=N` | 0 | ZGC 定时触发间隔 (秒, 0=禁用) | ZGC |
| `-XX:ShenandoahGCMode=mode` | satb | Shenandoah 模式 (satb/generational) | Shenandoah |
| `-XX:+UseCompactObjectHeaders` | false | 紧凑对象头, 每对象省 4-8 字节 (JDK 25+) | 全部 |

### 各 GC 启用参数速查

| GC | 启用参数 | 关键调优参数 |
|----|----------|-------------|
| Serial | `-XX:+UseSerialGC` | (无需调优) |
| Parallel | `-XX:+UseParallelGC` | `-XX:ParallelGCThreads=N` `-XX:GCTimeRatio=99` |
| G1 | `-XX:+UseG1GC` | `-XX:MaxGCPauseMillis=200` `-XX:G1HeapRegionSize=Nm` |
| ZGC | `-XX:+UseZGC` | `-XX:ZCollectionInterval=N` `-XX:ConcGCThreads=N` |
| Shenandoah | `-XX:+UseShenandoahGC` | `-XX:ShenandoahGCMode=generational` |
| Epsilon | `-XX:+UseEpsilonGC` | (无回收, 无参数) |

> 完整参数列表参见 [VM 参数参考](vm-parameters.md), 调优策略参见 [调优指南](tuning.md)。

---

## 7. 诊断速查 (Diagnostics)

### GC 日志 (-Xlog)

```bash
# 统一日志 (JDK 9+): 输出到文件, 含时间戳
-Xlog:gc*:file=gc.log:time,uptime,level,tags

# 只看暂停时间
-Xlog:gc:stdout:time

# 详细分代信息
-Xlog:gc+heap=debug:file=gc-detail.log
```

### JFR 事件 (Java Flight Recorder)

```bash
# 启动时录制
-XX:StartFlightRecording=filename=gc.jfr,duration=60s

# 运行时录制
jcmd <pid> JFR.start filename=gc.jfr duration=60s
```

**关键 JFR GC 事件**:

| 事件 | 说明 |
|------|------|
| `jdk.GarbageCollection` | 所有 GC 事件 (暂停时间、原因) |
| `jdk.GCPhasePause` | GC 各阶段暂停详情 |
| `jdk.G1GarbageCollection` | G1 专属 (Young/Mixed/Full) |
| `jdk.ZGarbageCollection` | ZGC 专属 (暂停、并发阶段) |
| `jdk.GCHeapSummary` | 每次 GC 前后堆使用量 |
| `jdk.ObjectAllocationOutsideTLAB` | TLAB 外分配 (大对象警告) |

### 常用诊断命令

```bash
# 堆信息
jcmd <pid> GC.heap_info

# 实时 GC 统计 (每秒刷新, 共 10 次)
jstat -gc <pid> 1000 10

# 手动触发 GC (仅调试)
jcmd <pid> GC.run

# 堆转储
jmap -dump:format=b,file=heap.hprof <pid>

# GC 后内存汇总 (无需暂停应用)
jcmd <pid> GC.heap_dump_all /tmp/heap.hprof
```

### 常见 GC 问题快速排查

| 症状 | 可能原因 | 排查命令 |
|------|----------|----------|
| Full GC 频繁 | 老年代过小 / 内存泄漏 | `-Xlog:gc*` + `jmap -histo <pid>` |
| 暂停时间超标 | GC 选型不当 / 堆过大 | `-Xlog:gc+phases=debug` |
| OOM: Java heap | 堆内存不足 | `jcmd <pid> GC.heap_info` |
| OOM: Metaspace | 类加载过多 | `-XX:MaxMetaspaceSize=N` + `jcmd <pid> VM.metaspace` |
| 分配速率过高 | 大量短命对象 | JFR `ObjectAllocationOutsideTLAB` |

> 更多监控与调优实践参见 [调优指南](tuning.md)。

---

## 8. 核心贡献者 (Key Contributors)

> 统计来源: JDK 源码 master 分支 git 历史 | 更新: 2026-03-20

| 贡献者 | 组织 | 主要领域 | 提交数 | 代表 JEP |
|--------|------|----------|--------|----------|
| [Thomas Schatzl](/by-contributor/profiles/thomas-schatzl.md) | Oracle | G1 GC 维护者 | 674 | JEP 522 |
| Albert Mingkun Yang | Oracle | G1 GC | 681 | - |
| [Per Liden](/by-contributor/profiles/per-liden.md) | Oracle | ZGC 创始人 | 198 | JEP 333, 377, 490 |
| [Stefan Karlsson](/by-contributor/profiles/stefan-karlsson.md) | Oracle | 分代 ZGC | 229 | JEP 439, 474 |
| [Erik Osterlund](/by-contributor/profiles/erik-osterlund.md) | Oracle | ZGC 核心 | 96 | - |
| [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | Amazon | Shenandoah 维护者 | 324 | JEP 318 |
| [Zhengyu Gu](/by-contributor/profiles/zhengyu-gu.md) | Datadog | Shenandoah 核心 | 252 | - |
| [William Kemper](/by-contributor/profiles/william-kemper.md) | Amazon | 分代 Shenandoah | 112 | JEP 521 |
| [Roman Kennke](/by-contributor/profiles/roman-kennke.md) | Datadog | Shenandoah / 紧凑对象头 | 163 | JEP 519 |
| [Kim Barrett](/by-contributor/profiles/kim-barrett.md) | Oracle | GC 基础设施 | 235 | - |

### 组织贡献格局

| 组织 | 主导领域 | 贡献占比 | 关键人物 |
|------|----------|----------|----------|
| **Oracle** | G1 GC + ZGC | ~70% | Thomas Schatzl, Per Liden, Stefan Karlsson |
| **Amazon** | Shenandoah 维护 | ~15% | Aleksey Shipilev, William Kemper |
| **Datadog** | Shenandoah + 紧凑对象头 | ~10% | Roman Kennke, Zhengyu Gu |
| **其他** | 平台优化 (AArch64, PPC) | ~5% | SAP, IBM, Intel |

**人才流动**: Shenandoah 核心团队从 Red Hat 转移 -- Aleksey Shipilev, William Kemper 加入 Amazon; Roman Kennke 经 Amazon 转至 Datadog。技术传承未断, 跨公司协作已成常态。

---

## 相关链接

### 内部文档

- [内存管理](../memory/) — 堆、栈、Metaspace
- [性能优化](../performance/) — JVM 调优

### 外部资源

- [OpenJDK GC 项目页](https://openjdk.org/groups/hotspot/docs/GarbageCollection.html)
- [ZGC Wiki](https://wiki.openjdk.org/display/zgc/Main)
- [Shenandoah Wiki](https://wiki.openjdk.org/display/shenandoah/Main)

### 源码目录

```
src/hotspot/share/gc/
├── g1/           — G1 GC 实现 (Oracle)
├── z/            — ZGC 实现 (Oracle)
├── shenandoah/   — Shenandoah 实现 (Red Hat/Amazon/Oracle)
├── parallel/     — Parallel GC 实现
├── serial/       — Serial GC 实现
├── epsilon/      — Epsilon GC 实现
└── shared/       — GC 公共基础设施 (屏障、线程、内存分配)
```

---

**最后更新**: 2026-03-22
