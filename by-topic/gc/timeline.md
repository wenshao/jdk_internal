# GC 演进时间线

跨版本追踪垃圾收集器的发展历程。

---

## 时间线概览

```
JDK 8 ───── JDK 11 ───── JDK 15 ───── JDK 17 ───── JDK 21 ───── JDK 26
 │              │              │              │              │              │
 │              │              │              │              │              │
G1 默认        ZGC 引入       ZGC 生产      并发扫描      分代 ZGC      G1 +10-20%
Parallel 默认   (实验)                       Shenandoah    分代 Shen     ZGC NUMA
CMS 废弃        Shenandoah     Windows       JEP 379       JEP 439       JEP 522
               (实验)                                    JEP 429
```

---

## G1 GC

| 版本 | 变更 | JEP | 说明 |
|------|------|-----|------|
| JDK 6 | G1 引入 | - | 替代 CMS 的低延迟 GC |
| JDK 7 | G1 完善 | - | 成为可选 GC |
| JDK 8 | G1 主流 | - | 大堆内存首选 |
| JDK 9 | **G1 默认** | JEP 248 | 替代 ParallelGC |
| JDK 11 | 并发标记改进 | JEP 307 | 降低 pause 时间 |
| JDK 17 | G1 Full GC 改进 | JEP 344 | 降低 worst-case pause |
| JDK 21 | Region 固定 | JEP 431 | 降低延迟 |
| JDK 26 | **吞吐量提升** | JEP 522 | +10-20% 吞吐量 |

### G1 适用场景

- **通用场景**：大多数应用默认选择
- **大堆内存**：4GB - 32GB
- **平衡延迟/吞吐**：Pause 目标 < 500ms

### G1 配置建议

```bash
# 推荐配置
-XX:+UseG1GC                    # 启用 G1
-XX:MaxGCPauseMillis=200        # Pause 目标
-XX:G1HeapRegionSize=16m        # Region 大小
-XX:G1ReservePercent=10         # 保留堆比例

# JDK 26 新增
-XX:+G1UseClaimTable            # 启用 Claim Table (默认)
```

→ [JEP 522: G1 GC Throughput](https://openjdk.org/jeps/522)

---

## ZGC (低延迟 GC)

| 版本 | 变更 | JEP | 说明 |
|------|------|-----|------|
| JDK 11 | ZGC 引入 | JEP 333 | 实验性，支持 Linux/macOS |
| JDK 14 | ZGC 生产可用 | JEP 368 | 脱离实验标签 |
| JDK 15 | Windows 支持 | JEP 377 | 跨平台完整支持 |
| JDK 17 | 并发线程栈扫描 | JEP 379 | 降低 pause 时间 |
| JDK 21 | **分代 ZGC** | JEP 439 | 显著降低 GC 频率 |
| JDK 23 | 分代改进 | JEP 474 | 进一步优化 |
| JDK 26 | NUMA-aware Relocation | - | 多插槽服务器优化 |

### ZGC 适用场景

- **大堆内存**：> 10GB
- **低延迟要求**：< 10ms pause
- **多线程应用**：并发标记优势明显

### ZGC 配置建议

```bash
# 启用 ZGC
-XX:+UseZGC                     # 启用 ZGC

# 分代 ZGC (JDK 21+)
-XX:+ZGCGenerational            # 启用分代 (默认)

# 调优参数
-XX:ZAllocationSpikeTolerance=5  # 分配突发容忍度
-XX:ZCollectionInterval=5        # GC 间隔 (秒)
```

### ZGC 性能数据

| 场景 | 非分代 | 分代 ZGC |
|------|--------|----------|
| 吞吐量下降 | 5-10% | < 5% |
| GC 频率 | 基准 | **-50%** |
| Pause 时间 | < 1ms | < 1ms |

→ [JEP 439: Generational ZGC](https://openjdk.org/jeps/439)

---

## Shenandoah

| 版本 | 变更 | JEP | 说明 |
|------|------|-----|------|
| JDK 12 | Shenandoah 引入 | JEP 189 | 实验性 |
| JDK 15 | Shenandoah 生产可用 | JEP 379 | 脱离实验标签 |
| JDK 17 | 并发线程栈扫描 | JEP 379 | 降低 pause 时间 |
| JDK 21 | **分代 Shenandoah** | JEP 429 | 降低 GC 频率 |
| JDK 26 | 进一步优化 | - | 持续改进 |

### Shenandoah vs ZGC

| 特性 | Shenandoah | ZGC |
|------|------------|-----|
| 设计理念 | 全并发 | 尽量并发 |
| Pause 目标 | < 10ms | < 10ms |
| 平台支持 | Linux/Windows/macOS | Linux/Windows/macOS |
| JDK 21 | 分代 | 分代 |
| JDK 26 | 分代 | 分代 + NUMA |
| 维护者 | Red Hat | Oracle |

### Shenandoah 配置建议

```bash
# 启用 Shenandoah
-XX:+UseShenandoahGC            # 启用 Shenandoah

# 分代模式 (JDK 21+)
-XX:ShenandoahGCMode=generational # 分代模式

# 模式选择
-XX:ShenandoahGCHeuristics=adaptive # 自适应启发式
```

→ [JEP 429: Generational Shenandoah](https://openjdk.org/jeps/429)

---

## ParallelGC

| 版本 | 状态 | 说明 |
|------|------|------|
| JDK 8 | **默认 GC** | 吞吐量优先 |
| JDK 9 | 默认改为 G1 | 仍可通过参数使用 |
| JDK 11+ | 可选 | 吞吐量场景仍适用 |

### ParallelGC 适用场景

- **吞吐量优先**：批处理、数据分析
- **CPU 密集**：GC 开销敏感
- **小堆内存**：< 4GB

```bash
# 启用 ParallelGC
-XX:+UseParallelGC              # 启用 ParallelGC
-XX:ParallelGCThreads=8         # GC 线程数
```

---

## 历史版本

### CMS (Concurrent Mark Sweep)

- **JDK 5**: 引入 (JEP 159)
- **JDK 9**: 标记废弃 (JEP 263)
- **JDK 14**: **移除** (JEP 363)

### Serial GC

- 保留用于单线程、小内存场景

---

## GC 选择决策树

```
┌─────────────────────────────────────┐
│         堆内存大小?                  │
└─────────────────────────────────────┘
           │
    ┌──────┴──────┐
    │             │
  < 4GB         > 4GB
    │             │
    ▼             ▼
┌─────────┐  ┌──────────────────┐
│ Serial  │  │   延迟要求?       │
│ Parallel│  └──────────────────┘
└─────────┘           │
              ┌───────┴────────┐
              │                │
           < 10ms           > 10ms
              │                │
              ▼                ▼
         ┌─────────┐      ┌─────────┐
         │   ZGC   │      │   G1    │
         │Shenandoah│     │(默认)   │
         └─────────┘      └─────────┘
```

---

## GC 选择建议

| 场景 | 推荐版本 | 推荐 GC | 理由 |
|------|----------|---------|------|
| 小内存 (< 2GB) | 任何 | SerialGC | 低开销 |
| 通用场景 | 任何 | G1 | 默认选择 |
| 大堆内存 (10GB+) | JDK 17+ | ZGC | 低延迟 |
| 超低延迟 (< 10ms) | JDK 21+ | 分代 ZGC | 最优延迟 |
| 多插槽服务器 | JDK 26 | ZGC (NUMA-aware) | NUMA 优化 |
| 吞吐量优先 | 任何 | ParallelGC | 最大吞吐 |
| RedHat 生态 | JDK 21+ | Shenandoah | RedHat 支持 |

---

## GC 性能对比

| GC | Pause 时间 | 吞吐量 | 堆大小限制 |
|----|-----------|--------|-----------|
| SerialGC | 100ms+ | 高 | ~2GB |
| ParallelGC | 100-500ms | 最高 | ~4GB |
| G1 | < 500ms | 高 | ~32GB |
| ZGC | < 10ms | 中高 | 16TB+ |
| Shenandoah | < 10ms | 中高 | 16TB+ |

---

## 相关链接

- [JEP 522: G1 GC Throughput](https://openjdk.org/jeps/522)
- [JEP 439: Generational ZGC](https://openjdk.org/jeps/439)
- [JEP 429: Generational Shenandoah](https://openjdk.org/jeps/429)
- [JEP 379: Shenandoah](https://openjdk.org/jeps/379)
- [JEP 333: ZGC](https://openjdk.org/jeps/333)
