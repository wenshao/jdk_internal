# GC 演进时间线

跨版本追踪垃圾收集器的发展历程。

---
## 目录

1. [时间线概览](#1-时间线概览)
2. [GC 基础概念](#2-gc-基础概念)
3. [G1 GC](#3-g1-gc)
4. [ZGC (低延迟 GC)](#4-zgc-低延迟-gc)
5. [Shenandoah](#5-shenandoah)
6. [ParallelGC](#6-parallelgc)
7. [GC 选择决策树](#7-gc-选择决策树)
8. [GC 选择建议](#8-gc-选择建议)
9. [GC 性能对比](#9-gc-性能对比)
10. [GC 问题排查](#10-gc-问题排查)
11. [贡献者](#11-贡献者)
12. [相关链接](#12-相关链接)

---


## 1. 时间线概览

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

## 2. GC 基础概念

### 垃圾收集算法分类

```
┌─────────────────────────────────────────────────────────┐
│                    GC 算法分类                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  按线程数                                               │
│  ├── Serial GC      (单线程)                            │
│  └── Parallel GC    (多线程并行)                        │
│                                                         │
│  按工作方式                                             │
│  ├── Stop-the-world (STW)                              │
│  ├── Concurrent    (部分并发)                           │
│  └── Fully concurrent (全并发)                          │
│                                                         │
│  按内存布局                                             │
│  ├── Generational  (分代: Young/Old)                   │
│  └── Region-based  (基于区域: G1/ZGC/Shenandoah)       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### GC 性能指标

| 指标 | 说明 | 目标值 |
|------|------|--------|
| **Throughput** | 吞吐量 (应用运行时间占比) | > 99% |
| **Pause Time** | GC 暂停时间 | < 200ms (G1) |
| **Footprint** | 内存占用 | 尽量小 |

---

## 3. G1 GC

### 架构原理

```
┌─────────────────────────────────────────────────────────┐
│                    G1 Heap Layout                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐  │
│  │ R1 │ R2 │ R3 │ R4 │ R5 │ R6 │ R7 │ R8 │... │ RN │  │
│  └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘  │
│                                                         │
│  Region = 1MB~32MB (必须是 2 的幂)                      │
│                                                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────────────────┐    │
│  │  Eden   │  │ Survivor│  │        Old          │    │
│  │ Regions │  │ Regions │  │      Regions        │    │
│  └─────────┘  └─────────┘  └─────────────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### G1 GC 工作流程

```
1. Young GC (Minor GC)
   ├── 标 Eden Region
   ├── 复制存活对象到 Survivor Region
   └── 维护年龄阈值

2. Concurrent Mark
   ├── Initial Mark (STW, 与 Young GC 并行)
   ├── Root Region Scan
   ├── Concurrent Mark
   ├── Remark (STW)
   └── Cleanup (STW)

3. Mixed GC
   ├── Young Region + Old Region
   └── 复制存活对象到空 Region

4. Full GC (退化时)
   └── 单线程 Mark-Sweep-Compact
```

### G1 版本演进

| 版本 | 变更 | JEP | 说明 |
|------|------|-----|------|
| JDK 6 | G1 引入 | - | 替代 CMS 的低延迟 GC |
| JDK 7 | G1 完善 | - | 成为可选 GC |
| JDK 8 | G1 主流 | - | 大堆内存首选 |
| JDK 9 | **G1 默认** | JEP 248 | 替代 ParallelGC, Thomas Schatzl |
| JDK 11 | 并发标记改进 | JEP 307 | 降低 pause 时间 |
| JDK 12 | 可中断 Mixed GC | JEP 346 | 满足 pause 目标优先 |
| JDK 17 | G1 Full GC 改进 | JEP 344 | 降低 worst-case pause |
| JDK 21 | Region 固定 | JEP 431 | 降低延迟 |
| JDK 26 | **吞吐量提升** | JEP 522 | +10-20% 吞吐量 |

### G1 适用场景

- **通用场景**：大多数应用默认选择
- **大堆内存**：4GB - 32GB
- **平衡延迟/吞吐**：Pause 目标 < 500ms
- **多核 CPU**：并行收集优势明显

### G1 配置详解

```bash
# ===== 基础配置 =====
-XX:+UseG1GC                    # 启用 G1
-XX:MaxGCPauseMillis=200        # Pause 目标 (默认 200ms)
-XX:G1HeapRegionSize=16m        # Region 大小 (自动计算)
-XX:G1ReservePercent=10         # 保留堆比例 (默认 10%)

# ===== Region 大小计算 =====
# RegionSize = HeapSize / 2048
# 范围: 1MB ~ 32MB (必须是 2 的幂)

# ===== 并发配置 =====
-XX:ConcGCThreads=4             # 并发标记线程数 (≈ ParallelGCThreads / 4)
-XX:ParallelGCThreads=8         # STW 期间并行线程数

# ===== 分代配置 =====
-XX:G1NewSizePercent=5          # Young Gen 最小比例
-XX:G1MaxNewSizePercent=60      # Young Gen 最大比例
-XX:TargetSurvivorRatio=50      # Survivor 目标使用率

# ===== Mixed GC 配置 =====
-XX:G1MixedGCCountTarget=8      # Mixed GC 目标次数
-XX:G1OldCSetRegionThreshold=10 # Old Region 回收阈值

# ===== JDK 26 新增 =====
-XX:+G1UseClaimTable            # 启用 Claim Table (默认)
-XX:G1ClaimTableSize=131072     # Claim Table 大小
```

### G1 性能调优指南

#### 1. 确定 Region 大小

```bash
# 计算公式
RegionSize = max(1MB, min(32MB, HeapSize / 2048))

# 示例
HeapSize = 8GB  → RegionSize = 8GB / 2048 = 4MB
HeapSize = 32GB → RegionSize = 32GB / 2048 = 16MB

# 手动设置 (谨慎!)
-XX:G1HeapRegionSize=16m
```

#### 2. 调整 Pause 目标

```bash
# 低延迟优先
-XX:MaxGCPauseMillis=50         # 更激进的目标

# 吞吐量优先
-XX:MaxGCPauseMillis=500        # 更宽松的目标
```

#### 3. 优化 Young Gen 大小

```bash
# 大对象分配多 → 增大 Young Gen
-XX:G1NewSizePercent=20
-XX:G1MaxNewSizePercent=80

# 对象生命周期短 → 减小 Young Gen
-XX:G1NewSizePercent=5
-XX:G1MaxNewSizePercent=40
```

### G1 GC 日志分析

```bash
# 开启 GC 日志
-Xlog:gc*:file=gc.log:time,uptime,level,tags

# 关键日志解析
[GC pause (G1 Evacuation Pause) (young), 0.1234567 secs]
   [Parallel Time: 120.5 ms]
       [GC Worker Start: 0.2 ms]
       [GC Worker End: 0.1 ms]
   [Code Root Fixup: 0.5 ms]
   [Code Root Purge: 0.3 ms]
[Eden: 512.0M(512.0M)->0.0B(640.0M) Survivors: 64.0M->64.0M Heap: 2.5G(4.0G)->2.1G(4.0G)]
```

**关键指标**：
- `GC pause` - GC 暂停时间
- `Eden: X(X)->Y(Y)` - Eden 使用变化
- `Heap: X(X)->Y(Y)` - 整堆使用变化

→ [JEP 522: G1 GC Throughput](https://openjdk.org/jeps/522)

---

## 4. ZGC (低延迟 GC)

### 架构原理

#### Colored Pointers (染色指针)

```
┌─────────────────────────────────────────────────────────┐
│              ZGC Colored Pointer (64-bit)                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  63  62  61  60  59  58  57  56  55  54  53 ...  4  3  2  1  0 │
│  │   │   │   │   │   │   │   │   │   │   │         │  │  │  │
│  │   │   │   │   │   │   │   │   │   │   │         │  │  │  └─ Finalizable (0/1)
│  │   │   │   │   │   │   │   │   │   │   │         │  │  └──── Remapped (0/1)
│  │   │   │   │   │   │   │   │   │   │   │         │  └─────── Marked1 (0/1)
│  │   │   │   │   │   │   │   │   │   │   │         └────────── Marked0 (0/1)
│  │   │   │   │   │   │   │   │   │   │   └─────────────────── 42 bits: Object Offset
│  │   │   │   │   │   │   │   │   │   └────────────────────────  4 bits: View (unused)
│  │   │   │   │   │   │   │   │   └───────────────────────────── 16 bits: Virtual Address (unused)
│  │   │   │   │   │   │   │   └─────────────────────────────────  2 bits: Color
│  │   │   │   │   │   │   └─────────────────────────────────────  Multiple Offset (unused)
│  │   │   │   │   │   └─────────────────────────────────────────  N/A
│  └───┴───┴───┴───┴───────────────────────────────────────────  0 bits (unused, reserved)
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### 读屏障 (Load Barrier)

```java
// ZGC 在每次读取引用时执行读屏障
Object obj = field;  // 触发读屏障

// 读屏障伪代码
Object load_barrier(Object obj) {
    if (is_colored(obj)) {
        // 根据颜色执行相应操作
        if (color == REMAPPED) {
            return derive_pointer(obj);
        }
        if (color == MARKED0 || color == MARKED1) {
            return mark_and_forward(obj);
        }
    }
    return obj;
}
```

### ZGC GC 周期

```
1. Pause Mark Start (STW, ~1ms)
   └── 标记根集合

2. Concurrent Mark
   ├── 遍历对象图
   └── 标记存活对象

3. Pause Mark End (STW, ~1ms)
   └── 处理弱引用等

4. Concurrent Process Recovered Regions
   └── 处理回收区域

5. Pause Relocate Start (STW, ~1ms)
   └── 选择待重定位 Region

6. Concurrent Relocate
   └── 重定位存活对象

7. Concurrent Remap
   └── 更新引用
```

### ZGC 版本演进

| 版本 | 变更 | JEP | 说明 |
|------|------|-----|------|
| JDK 11 | ZGC 引入 | JEP 333 | 实验性, Per Liden, Erik Österlund |
| JDK 14 | ZGC 生产可用 | JEP 368 | 脱离实验标签 |
| JDK 15 | Windows 支持 | JEP 377 | 跨平台完整支持 |
| JDK 17 | 并发线程栈扫描 | JEP 379 | 降低 pause 时间 |
| JDK 21 | **分代 ZGC** | JEP 439 | Stefan Karlsson (Owner), 显著降低 GC 频率 |
| JDK 23 | 分代改进 | JEP 474 | 进一步优化, 默认启用 |
| JDK 26 | NUMA-aware Relocation | - | 多插槽服务器优化 |

### 分代 ZGC 架构

```
┌─────────────────────────────────────────────────────────┐
│              Generational ZGC Layout                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────┐      ┌─────────────────┐          │
│  │   Young Gen     │      │    Old Gen      │          │
│  │   (ZST)         │      │    (ZLT)        │          │
│  │                 │      │                 │          │
│  │  ┌─────┐        │      │  ┌─────────┐    │          │
│  │  │ Eden │        │      │  │  Old    │    │          │
│  │  └─────┘        │      │  │ Objects │    │          │
│  │  ┌─────┐        │      │  └─────────┘    │          │
│  │  │Surv │        │      │                 │          │
│  │  └─────┘        │      │                 │          │
│  └─────────────────┘      └─────────────────┘          │
│                                                         │
│  ZST = Short-lived (Young)                              │
│  ZLT = Long-lived (Old)                                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### ZGC 适用场景

- **大堆内存**：> 10GB
- **低延迟要求**：< 10ms pause
- **多线程应用**：并发标记优势明显
- **延迟敏感服务**：金融交易、实时系统

### ZGC 配置详解

```bash
# ===== 基础配置 =====
-XX:+UseZGC                     # 启用 ZGC

# 分代 ZGC (JDK 21+)
-XX:+ZGCGenerational            # 启用分代 (JDK 23+ 默认)

# ===== 内存配置 =====
-XX:NewSize=512m                # Young Gen 初始大小
-XX:MaxNewSize=2g               # Young Gen 最大大小

# ===== 调优参数 =====
-XX:ZAllocationSpikeTolerance=5  # 分配突发容忍度 (默认 2)
-XX:ZCollectionInterval=5        # GC 间隔 (秒, 默认自动)
-XX:ZFragmentationLimit=25       # 碎片化阈值 (%)

# ===== 并发配置 =====
-XX:ConcGCThreads=4             # 并发 GC 线程数
-XX:ParallelGCThreads=8         # 并行 GC 线程数

# ===== NUMA 优化 (JDK 26) =====
-XX:+UseNUMA                    # 启用 NUMA 感知
-XX:NUMAInterleaving=true       # NUMA 交错分配
```

### ZGC 性能数据

#### 分代 vs 非分代

| 场景 | 非分代 | 分代 ZGC | 改善 |
|------|--------|----------|------|
| 吞吐量下降 | 5-10% | < 5% | **+50%** |
| GC 频率 | 基准 | -50% | **-50%** |
| Pause 时间 | < 1ms | < 1ms | 持平 |
| 堆内存占用 | 基准 | +5% | 略增 |

#### 不同堆大小下的性能

| 堆大小 | GC 频率 | Pause 时间 | 吞吐量 |
|--------|---------|-----------|--------|
| 8GB | 每 10s | < 1ms | 99% |
| 32GB | 每 30s | < 1ms | 98% |
| 128GB | 每 2min | < 1ms | 97% |
| 512GB | 每 5min | < 1ms | 96% |

→ [JEP 439: Generational ZGC](https://openjdk.org/jeps/439)

---

## 5. Shenandoah

### 架构原理

#### Brooks Forwarding Pointers

```
┌─────────────────────────────────────────────────────────┐
│          Shenandoah Brooks Pointer                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Original Object                 Forwarded Object       │
│  ┌─────────────────┐            ┌─────────────────┐    │
│  │ Data            │            │ Data            │    │
│  │                 │            │                 │    │
│  │ [Forward Ptr] ──────────────>│                 │    │
│  │                 │            │                 │    │
│  └─────────────────┘            └─────────────────┘    │
│                                                         │
│  每个对象包含一个转发指针域                             │
│  读/写屏障检查转发指针                                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Shenandoah vs ZGC

| 特性 | Shenandoah | ZGC |
|------|------------|-----|
| 设计理念 | 全并发 | 尽量并发 |
| 转发指针 | Brooks Pointers | Colored Pointers |
| 屏障开销 | 读屏障 + 写屏障 | 仅读屏障 |
| Pause 目标 | < 10ms | < 10ms |
| 平台支持 | Linux/Windows/macOS | Linux/Windows/macOS |
| JDK 21 | 分代 | 分代 |
| JDK 26 | 分代 | 分代 + NUMA |
| 维护者 | Red Hat | Oracle |
| 开源协议 | GPL | GPL |

### Shenandoah 版本演进

| 版本 | 变更 | JEP | 说明 |
|------|------|-----|------|
| JDK 12 | Shenandoah 引入 | JEP 189 | 实验性, Red Hat |
| JDK 15 | Shenandoah 生产可用 | JEP 379 | 脱离实验标签 |
| JDK 17 | 并发线程栈扫描 | JEP 379 | 降低 pause 时间 |
| JDK 21 | **分代 Shenandoah** | JEP 429 | William Kemper (Owner), Red Hat 团队 |
| JDK 26 | 进一步优化 | - | 持续改进 |

### Shenandoah 配置详解

```bash
# ===== 基础配置 =====
-XX:+UseShenandoahGC            # 启用 Shenandoah

# ===== GC 模式 =====
# 1. generational (分代, JDK 21+)
-XX:ShenandoahGCMode=generational

# 2. normal (非分代)
-XX:ShenandoahGCMode=normal

# 3. passive (被动, 仅用于调试)
-XX:ShenandoahGCMode=passive

# ===== 启发式策略 =====
-XX:ShenandoahGCHeuristics=adaptive # 自适应 (推荐)
-XX:ShenandoahGCHeuristics=compact  # 紧凑模式
-XX:ShenandoahGCHeuristics=aggressive # 激进模式
-XX:ShenandoahGCHeuristics=static    # 静态模式

# ===== 并发配置 =====
-XX:ConcGCThreads=4             # 并发 GC 线程数
-XX:ParallelGCThreads=8         # 并行 GC 线程数

# ===== 区域配置 =====
-XX:ShenandoahRegionSize=32m    # Region 大小 (256k-32m)
```

→ [JEP 429: Generational Shenandoah](https://openjdk.org/jeps/429)

---

## 6. ParallelGC

### 架构原理

```
┌─────────────────────────────────────────────────────────┐
│              ParallelGC Heap Layout                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │                  Young Gen                       │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────────────┐  │    │
│  │  │  Eden   │  │ Survivor│  │   Survivor      │  │    │
│  │  │  8/10   │  │   S0    │  │      S1         │  │    │
│  │  └─────────┘  └─────────┘  └─────────────────┘  │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │                   Old Gen                        │    │
│  │                                                   │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### ParallelGC 配置详解

```bash
# ===== 基础配置 =====
-XX:+UseParallelGC              # 启用 ParallelGC

# ===== 线程配置 =====
-XX:ParallelGCThreads=8         # GC 线程数 (默认 = CPU 核数)

# ===== 分代配置 =====
-XX:NewRatio=2                  # Young:Old = 1:2
-XX:SurvivorRatio=8             # Eden:S0:S1 = 8:1:1
-XX:MaxTenuringThreshold=15     # 晋升 Old Gen 阈值

# ===== 吞吐量目标 =====
-XX:GCTimeRatio=99              # GC 时间 <= 1% (默认 99)
-XX:MaxGCPauseMillis=200        # 最大 GC 暂停时间

# ===== 自动调整 =====
-XX:+UseAdaptiveSizePolicy     # 自动调整代大小 (默认)
-XX:-UseAdaptiveSizePolicy     # 禁用自动调整
```

---

## 7. GC 选择决策树

```
┌─────────────────────────────────────────────────────────┐
│                     1. 堆内存大小?                       │
└─────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
           < 4GB                          >= 4GB
              │                               │
              ▼                               ▼
┌─────────────────────┐           ┌───────────────────────┐
│ 2. CPU 核数?        │           │ 3. 延迟要求?          │
├─────────────────────┤           ├───────────────────────┤
│ 单核或双核          │           │ < 10ms                │
│  → SerialGC         │           │  → ZGC / Shenandoah   │
│ 多核                │           │ >= 10ms               │
│  → ParallelGC       │           │  → 继续               │
└─────────────────────┘           └───────────────────────┘
                                            │
                                            ▼
                              ┌───────────────────────┐
                              │ 4. JDK 版本?          │
                              ├───────────────────────┤
                              │ JDK 21+               │
                              │  → 分代 ZGC           │
                              │ JDK 17+               │
                              │  → ZGC                │
                              │ JDK < 17              │
                              │  → G1                 │
                              └───────────────────────┘
```

---

## 8. GC 选择建议

| 场景 | 推荐版本 | 推荐 GC | 理由 |
|------|----------|---------|------|
| 小内存 (< 2GB) | 任何 | SerialGC | 低开销，单线程高效 |
| 单核 CPU | 任何 | SerialGC | 无并行开销 |
| 吞吐量优先 | 任何 | ParallelGC | 最大吞吐，STW 并行 |
| 通用场景 | 任何 | G1 | 默认选择，平衡延迟/吞吐 |
| 大堆内存 (10GB+) | JDK 17+ | ZGC | 低延迟，可扩展到 TB |
| 超低延迟 (< 10ms) | JDK 21+ | 分代 ZGC | 最优延迟，< 1ms pause |
| 多插槽服务器 | JDK 26 | ZGC (NUMA) | NUMA 优化 |
| RedHat 生态 | JDK 21+ | Shenandoah | RedHat 支持 |
| 容器环境 | 任何 | G1 | 内存感知较好 |

---

## 9. GC 性能对比

| GC | Pause 时间 | 吞吐量 | 堆大小限制 | 并发比例 | 适用场景 |
|----|-----------|--------|-----------|----------|----------|
| SerialGC | 100ms+ | 高 | ~2GB | 0% | 单核、小内存 |
| ParallelGC | 100-500ms | 最高 | ~4GB | 0% | 吞吐量优先 |
| G1 | < 500ms | 高 | ~32GB | ~10% | 通用场景 |
| ZGC | < 10ms | 中高 | 16TB+ | ~95% | 低延迟、大堆 |
| Shenandoah | < 10ms | 中高 | 16TB+ | ~95% | 低延迟、大堆 |

---

## 10. GC 问题排查

### 常见 GC 问题

| 问题 | 症状 | 可能原因 | 解决方案 |
|------|------|----------|----------|
| **GC Overhead** | CPU 高，吞吐量低 | 堆太小，GC 频繁 | 增大堆内存 |
| **Long Pause** | 停顿时间长 | Old Gen 满，Full GC | 增大 Old Gen 或切换 GC |
| **OOM** | OutOfMemoryError | 内存泄漏或堆太小 | 分析 heapdump 或增大堆 |
| **Fragmentation** | 碎片化严重 | 对象大小差异大 | 使用压缩 GC |

### GC 日志配置

```bash
# JDK 9+ 统一日志
-Xlog:gc*:file=gc.log:time,uptime,level,tags:filecount=5,filesize=10m

# 详细 GC 信息
-Xlog:gc+heap=debug:file=gc.log:time,uptime

# GC 停顿分析
-Xlog:safepoint:file=safepoint.log:time,uptime
```

### 常用工具

```bash
# jstat - GC 统计
jstat -gcutil <pid> 1000 10

# jmap - 堆转储
jmap -dump:live,format=b,file=heap.hprof <pid>

# jcmd - JVM 诊断
jcmd <pid> GC.heap_info
jcmd <pid> GC.run_finalization

# VisualVM / JConsole
# 图形化监控工具
```

---

## 11. 贡献者

### GC 团队核心成员

| GC | JEP | 主要贡献者 | 公司 |
|----|-----|-----------|------|
| ZGC | JEP 333/377/439 | **Per Liden**, Erik Österlund, Stefan Karlsson | Oracle |
| G1 | JEP 248/307/346/522 | Thomas Schatzl, Per Liden | Oracle |
| Shenandoah | JEP 379/429 | **William Kemper**, Bernd Mathiske, Kelvin Nilsen, Ramki Ramakrishna | Red Hat |

### Per Liden

- **职位**: ZGC Lead, Oracle HotSpot GC Team
- **背景**: 前 JRockit 团队 (被 Oracle 收购)
- **主要贡献**:
  - ZGC 创始人兼技术负责人
  - JRockit GC 代码移植到 HotSpot
  - G1 GC 性能优化 (JEP 522)
- **现职**: SambaNova Systems (AI 性能工程师)

> "ZGC is a scalable low-latency garbage collector designed for pause times not exceeding 10ms."
> — Per Liden, JEP 333

### Erik Österlund

- **职位**: HotSpot GC Team Member, Oracle
- **主要贡献**:
  - ZGC 核心开发者
  - 《The Z Garbage Collector in JDK 25》作者
  - JEP 377/439 Reviewer
- **专长**: 低延迟 GC、染色指针技术

### Stefan Karlsson

- **职位**: HotSpot Developer, Oracle
- **主要贡献**:
  - JEP 439 Owner (分代 ZGC)
  - JEP 474 (ZGC 分代模式默认)
  - G1 GC 并发标记改进

### William Kemper

- **职位**: Principal Software Engineer, Red Hat
- **主要贡献**:
  - JEP 404/429 Owner (分代 Shenandoah)
  - Shenandoah GC 核心开发者
  - Brooks Pointers 技术实现

### Red Hat Shenandoah 团队

| 成员 | 角色 |
|------|------|
| **Bernd Mathiske** | JEP 404 作者 |
| **Kelvin Nilsen** | JEP 404 作者 |
| **Ramki Ramakrishna** | JEP 404 作者 |

---

## 12. 相关链接

- [JEP 522: G1 GC Throughput](https://openjdk.org/jeps/522)
- [JEP 439: Generational ZGC](https://openjdk.org/jeps/439)
- [JEP 474: Generational ZGC Improvements](https://openjdk.org/jeps/474)
- [JEP 429: Generational Shenandoah](https://openjdk.org/jeps/429)
- [JEP 379: Shenandoah](https://openjdk.org/jeps/379)
- [JEP 333: ZGC](https://openjdk.org/jeps/333)
