# HotSpot GC 组件分析

> 垃圾回收器实现分析 (Garbage Collector implementation analysis)

---

## 1. 概述

### 1.1 源码规模

**路径**: `src/hotspot/share/gc/`，共 **385 个 .cpp 文件**

| 目录 | 文件数 (cpp+hpp) | 说明 |
|------|-------------------|------|
| `shared/` | 209 | GC 公共框架: CollectedHeap、BarrierSet、CardTable |
| `g1/` | 257 | G1 Garbage-First 收集器 |
| `z/` | 237 | ZGC (Z Garbage Collector) |
| `shenandoah/` | 210 | Shenandoah 低延迟收集器 |
| `parallel/` | 52 | Parallel (吞吐量优先) 收集器 |
| `serial/` | 29 | Serial (单线程) 收集器 |
| `epsilon/` | 15 | Epsilon (无操作) 收集器 |

### 1.2 GC 对比总览

| GC | 引入版本 | 暂停目标 | 适用场景 | 默认 |
|----|----------|----------|----------|------|
| Serial | JDK 1.3 | 长 (数秒) | 小堆、嵌入式 | - |
| Parallel | JDK 5 | 中 (百毫秒) | 批处理、吞吐量 | - |
| G1 | JDK 7 (JDK 9 默认) | 可控 (200ms) | 通用 | 默认 (default) |
| ZGC | JDK 11 (JDK 15 GA) | 亚毫秒 (<1ms) | 大堆、低延迟 | - |
| Shenandoah | JDK 12 | 亚毫秒 (<10ms) | 低延迟 | - |
| Epsilon | JDK 11 | 无 GC | 测试、基准 | - |

---

## 2. GC 接口层 (GC Interface)

### 2.1 CollectedHeap — 所有 GC 的抽象基类

**源码**: `src/hotspot/share/gc/shared/collectedHeap.hpp:91`

```cpp
class CollectedHeap : public CHeapObj<mtGC> {
 public:
  // 内存分配 (Memory allocation)
  virtual HeapWord* mem_allocate(size_t size) = 0;
  virtual HeapWord* allocate_new_tlab(size_t min_size,
                                       size_t desired_size,
                                       size_t* actual_size) = 0;

  // GC 触发 (GC triggering)
  virtual void collect(GCCause::Cause cause) = 0;
  virtual void do_full_collection(bool clear_all_soft_refs) = 0;

  // 堆查询 (Heap queries)
  virtual size_t capacity() const = 0;
  virtual size_t used() const = 0;
  virtual size_t max_capacity() const = 0;
  virtual bool is_in(const void* p) const = 0;

  // GC 线程管理 (GC thread management)
  virtual void gc_threads_do(ThreadClosure* tc) const = 0;
  virtual WorkerThreads* safepoint_workers() { return nullptr; }
};
```

### 2.2 各 GC 的 Heap 实现类

| GC | Heap 类 | 源文件 |
|----|---------|--------|
| Serial | `SerialHeap` | `gc/serial/serialHeap.hpp:64` |
| Parallel | `ParallelScavengeHeap` | `gc/parallel/parallelScavengeHeap.hpp:69` |
| G1 | `G1CollectedHeap` | `gc/g1/g1CollectedHeap.hpp:149` |
| ZGC | `ZCollectedHeap` | `gc/z/zCollectedHeap.hpp:40` |
| Shenandoah | `ShenandoahHeap` | `gc/shenandoah/shenandoahHeap.hpp:142` |
| Epsilon | `EpsilonHeap` | `gc/epsilon/epsilonHeap.hpp:37` |

所有 Heap 类均 `: public CollectedHeap`。

### 2.3 BarrierSet — 屏障基础设施 (Barrier Infrastructure)

屏障是 GC 在引用读写时插入的额外代码，用于维护 GC 不变式。

**源码**: `src/hotspot/share/gc/shared/barrierSet.hpp:46`

```
BarrierSet (gc/shared/barrierSet.hpp)
├── CardTableBarrierSet (gc/shared/cardTableBarrierSet.hpp)
│   用于 Serial、Parallel — 基于卡表 (Card Table) 的写屏障
├── G1BarrierSet (gc/g1/g1BarrierSet.hpp)
│   G1 SATB 写屏障 + 记忆集 (Remembered Set)
├── ShenandoahBarrierSet (gc/shenandoah/shenandoahBarrierSet.hpp)
│   Shenandoah 读/写屏障 (Brooks pointer + SATB)
└── ZBarrierSet (gc/z/zBarrierSet.hpp)
    ZGC 读屏障 (Load barrier, 染色指针 colored pointer)
```

**编译器集成**: 每个 BarrierSet 有对应的编译器扩展:
- `BarrierSetC1` — C1 编译器屏障注入 (`gc/shared/c1/barrierSetC1.hpp`)
- `BarrierSetC2` — C2 编译器屏障注入 (`gc/shared/c2/barrierSetC2.hpp`)
- `BarrierSetAssembler` — 汇编级屏障 (`gc/shared/barrierSetAssembler.hpp`)
- `BarrierSetNMethod` — nmethod 入口屏障 (`gc/shared/barrierSetNMethod.hpp`)

---

## 3. G1 GC (Garbage-First)

**源码**: `src/hotspot/share/gc/g1/`，257 文件

### 3.1 核心架构

G1 将堆划分为固定大小的 Region (通常 1-32MB):

```
┌─────────────────────────────────────────────────────────┐
│                    G1 堆布局 (Heap Layout)               │
│  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐    │
│  │  E  │  E  │  S  │  O  │  O  │  H  │  H  │ Free│    │
│  │Eden │Eden │Surv │ Old │ Old │Humon│Humon│     │    │
│  └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘    │
│  E = Eden, S = Survivor, O = Old, H = Humongous        │
│  Region 大小 = 堆 / 2048 (默认), 可用 -XX:G1HeapRegionSize 设置│
└─────────────────────────────────────────────────────────┘
```

### 3.2 关键源文件

| 文件 | 说明 |
|------|------|
| `g1CollectedHeap.cpp/hpp` | G1 堆实现，调度 Young/Mixed/Full GC |
| `g1ConcurrentMark.cpp` | 并发标记 (Concurrent Marking) |
| `g1ConcurrentMarkThread.hpp` | 并发标记线程 |
| `g1YoungCollector.cpp` | Young GC (Evacuation) |
| `g1FullCollector.cpp` | Full GC (压缩整理) |
| `g1Policy.cpp` | GC 策略: 选择回收集 (Collection Set) |
| `g1Analytics.cpp` | 暂停时间预测 |
| `g1RemSet.cpp` | 记忆集 (Remembered Set): 跨 Region 引用追踪 |
| `g1CardSet.cpp/hpp` | 卡集: 记忆集的底层数据结构 |
| `g1BarrierSet.cpp` | G1 屏障: SATB 写屏障 + 引用更新 |
| `g1Allocator.cpp` | TLAB 分配 + Region 分配 |
| `g1CardTable.cpp` | 卡表实现 |
| `g1CardTableClaimTable.hpp` | 卡表分块认领 (Claim Table) 优化 |

### 3.3 G1 GC 流程

```
Young GC (STW):
  1. 选择 Collection Set (所有 Eden + Survivor Region)
  2. 扫描 GC Roots + RSet → 标记存活对象
  3. 复制存活对象到 Survivor/Old Region (Evacuation)
  4. 回收空 Region

Concurrent Marking (并发):
  1. Initial Mark (STW, 搭载 Young GC)
  2. Concurrent Mark (并发扫描整个堆)
  3. Remark (STW, SATB 处理)
  4. Cleanup (STW, 回收空 Region)

Mixed GC (STW):
  Young GC + 选中的 Old Region (收益最高的优先 → "Garbage-First")
```

### 3.4 G1CardTableClaimTable

**源码**: `src/hotspot/share/gc/g1/g1CardTableClaimTable.hpp:44`

```cpp
// 用于并行扫描卡表时的分块认领，避免线程竞争
class G1CardTableClaimTable : public CHeapObj<mtGC> {
    // 每个 Region 的卡表分成多个 chunk
    // 线程通过原子操作认领 chunk，减少竞争
    bool has_unclaimed_cards(uint region);
    void reset_to_unclaimed(uint region);
    uint claim_cards(uint region, uint increment);
    uint claim_chunk(uint region);
};
```

---

## 4. ZGC (Z Garbage Collector)

**源码**: `src/hotspot/share/gc/z/`，237 文件

### 4.1 核心特性

- 暂停时间与堆大小无关 (pause times independent of heap size)
- 支持 TB 级堆 (supports multi-terabyte heaps)
- 并发执行几乎所有 GC 工作
- 使用染色指针 (colored pointers) 和读屏障 (load barriers)

### 4.2 ZPage — 内存管理单元

**源码**: `src/hotspot/share/gc/z/zPage.hpp:39`

```cpp
// ZPageType — 三种页面类型
enum class ZPageType : uint8_t {
  small,    // 小页面 (2MB, 用于 ≤ 256 字节对象)
  medium,   // 中页面 (32MB, 用于 ≤ 4KB 对象)
  large     // 大页面 (N * 2MB, 用于 > 4KB 对象)
};

class ZPage : public CHeapObj<mtGC> {
  const ZPageType  _type;        // 页面类型
  ZPageAge         _age;         // 分代年龄
  ZVirtualMemory   _vmem;        // 虚拟内存映射
  // ...
};
```

### 4.3 染色指针 (Colored Pointers)

```
64 位指针布局:
┌──────────────────────────────────────────────────────────┐
│ 0000 0000 0000 0000 │ F │ R │ M1│ M0│    地址 (44位)    │
└──────────────────────────────────────────────────────────┘
  F  = Finalizable 标记
  R  = Remapped 标记 (重定位完成)
  M0/M1 = 标记位 (Mark bits, 交替使用)
  地址 = 对象实际地址 (支持 16TB 堆空间)
```

### 4.4 关键源文件

| 文件 | 说明 |
|------|------|
| `zCollectedHeap.cpp` | ZGC 堆实现 (继承 CollectedHeap) |
| `zDriver.cpp` | GC 驱动: 调度各 GC 阶段 |
| `zMark.cpp` | 并发标记 (Concurrent Marking) |
| `zRelocate.cpp` | 并发重定位 (Concurrent Relocation) |
| `zPage.cpp/hpp` | ZPage 内存页管理 |
| `zPageAllocator.cpp` | 页面分配器 |
| `zBarrier.cpp/hpp` | 读屏障 (Load Barrier) 实现 |
| `zBarrierSet.cpp` | 屏障集成 (与解释器/编译器对接) |
| `zAddress.hpp` | 染色指针地址操作 |
| `zForwarding.cpp` | 转发表 (Forwarding Table) |
| `zGeneration.cpp` | 分代 ZGC (ZGenerational) 支持 |
| `zNMethodTable.cpp` | nmethod 根扫描 |

### 4.5 ZGC 并发阶段

```
1. Pause Mark Start (STW, 极短)     — 标记 GC Roots
2. Concurrent Mark                   — 并发遍历对象图
3. Pause Mark End (STW, 极短)        — 处理引用
4. Concurrent Process Non-Strong Refs — 处理弱引用等
5. Concurrent Reset Relocation Set   — 重置重定位集
6. Concurrent Select Relocation Set  — 选择需要重定位的页面
7. Pause Relocate Start (STW, 极短)  — 重定位 GC Roots
8. Concurrent Relocate              — 并发重定位对象
```

---

## 5. Shenandoah GC

**源码**: `src/hotspot/share/gc/shenandoah/`，210 文件

### 5.1 核心特性

- 并发压缩 (concurrent compaction)
- 使用 Brooks 转发指针 (forwarding pointer)
- 支持分代模式 (Generational Mode)

### 5.2 运行模式 (GC Modes)

**源码**: `src/hotspot/share/gc/shenandoah/mode/`

| 模式类 | 说明 |
|--------|------|
| `ShenandoahSATBMode` | SATB 模式 (默认, 非分代) |
| `ShenandoahGenerationalMode` | 分代模式 (年轻代 + 老年代) |
| `ShenandoahPassiveMode` | 被动模式 (仅 Full GC, 用于调试) |

```
ShenandoahMode (mode/shenandoahMode.hpp)
├── ShenandoahSATBMode         # SATB 标记模式
├── ShenandoahGenerationalMode # 分代模式
└── ShenandoahPassiveMode      # 被动模式
```

### 5.3 分代支持 (Generational Shenandoah)

**源码**:
- `shenandoahGeneration.hpp:44` — `ShenandoahGeneration` 基类
- `shenandoahYoungGeneration.hpp:31` — `ShenandoahYoungGeneration`
- `shenandoahOldGeneration.hpp:40` — `ShenandoahOldGeneration`
- `shenandoahGlobalGeneration.hpp:33` — `ShenandoahGlobalGeneration`

```cpp
// 分代层次
class ShenandoahGeneration : public CHeapObj<mtGC>, public ShenandoahSpaceInfo {
    // 每一代的回收策略
};

class ShenandoahYoungGeneration : public ShenandoahGeneration {
    // 年轻代: 频繁回收短命对象
};

class ShenandoahOldGeneration : public ShenandoahGeneration {
    // 老年代: 较少回收长寿对象
};

class ShenandoahGlobalGeneration : public ShenandoahGeneration {
    // 全局代: 非分代模式时使用
};
```

### 5.4 关键源文件

| 文件 | 说明 |
|------|------|
| `shenandoahHeap.cpp/hpp` | 堆实现 (继承 CollectedHeap) |
| `shenandoahConcurrentGC.cpp` | 并发 GC 周期 |
| `shenandoahConcurrentMark.cpp` | 并发标记 |
| `shenandoahBarrierSet.cpp/hpp` | 读/写屏障 |
| `shenandoahControlThread.cpp` | GC 控制线程 |
| `shenandoahGenerationalControlThread.hpp` | 分代模式控制线程 |
| `shenandoahCollectionSet.cpp` | 回收集管理 |
| `shenandoahForwarding.hpp` | Brooks 转发指针 |
| `shenandoahGeneration.hpp` | 代 (Generation) 基类 |
| `shenandoahRegulatorThread.hpp` | 分代模式调节线程 |
| `shenandoahMmuTracker.hpp` | MMU (Minimum Mutator Utilization) 跟踪 |

### 5.5 Shenandoah 并发阶段

```
1. Init Mark (STW, 短)             — 标记 GC Roots
2. Concurrent Mark                  — 并发遍历对象图 (SATB)
3. Final Mark (STW, 短)            — 完成标记, 选择回收集
4. Concurrent Cleanup               — 回收无存活对象的 Region
5. Concurrent Evacuation            — 并发复制存活对象 (Brooks pointer)
6. Init Update Refs (STW, 短)      — 准备引用更新
7. Concurrent Update Refs           — 并发更新所有引用
8. Final Update Refs (STW, 短)     — 完成引用更新, 回收旧 Region
```

---

## 6. Parallel GC

**源码**: `src/hotspot/share/gc/parallel/`，52 文件

### 6.1 核心设计

吞吐量优先 (throughput-first)，使用多个 GC 线程并行工作。

**Heap 类**: `ParallelScavengeHeap` (parallelScavengeHeap.hpp:69)

```
堆布局:
┌─────────────────────┬───────────────────────────┐
│      Young Gen      │        Old Gen            │
│  ┌─────┬─────────┐  │                           │
│  │Eden │ Survivor │  │                           │
│  │     │ S0 │ S1  │  │                           │
│  └─────┴────┴─────┘  │                           │
└─────────────────────┴───────────────────────────┘
```

### 6.2 关键源文件

| 文件 | 说明 |
|------|------|
| `parallelScavengeHeap.cpp` | 堆管理 |
| `psScavenge.cpp` | Young GC (Parallel Scavenge) |
| `psCompact.cpp` | Full GC (Mark-Compact) |
| `psParallelCompact.cpp` | 并行压缩 |
| `psAdaptiveSizePolicy.cpp` | 自适应大小策略 |

---

## 7. Serial GC

**源码**: `src/hotspot/share/gc/serial/`，29 文件

最简单的 GC 实现。单线程 (single-threaded)，适用于小堆和客户端应用。

**Heap 类**: `SerialHeap` (serialHeap.hpp:64)

关键文件:
- `serialHeap.cpp` — 堆管理
- `defNewGeneration.cpp` — 年轻代 (DefNew = Default New Generation)
- `tenuredGeneration.cpp` — 老年代
- `markSweep.cpp` — Full GC 标记清除

---

## 8. Epsilon GC

**源码**: `src/hotspot/share/gc/epsilon/`，15 文件

无操作 (no-op) GC: 只分配不回收，堆满即 OOM。用于性能测试基准和极短生命周期应用。

**Heap 类**: `EpsilonHeap` (epsilonHeap.hpp:37)

```bash
# 启用 Epsilon GC
java -XX:+UnlockExperimentalVMOptions -XX:+UseEpsilonGC -jar app.jar
```

---

## 9. GC 共享框架 (gc/shared/)

**源码**: `src/hotspot/share/gc/shared/`，209 文件

核心共享组件:

| 文件 | 说明 |
|------|------|
| `collectedHeap.hpp` | 堆抽象基类 |
| `barrierSet.hpp` | 屏障集抽象基类 |
| `cardTable.hpp` | 卡表 (Card Table): 512 字节一张卡 |
| `cardTableBarrierSet.hpp` | 基于卡表的写屏障 |
| `concurrentGCThread.hpp` | GC 并发线程基类 |
| `gcCause.hpp` | GC 触发原因枚举 |
| `ageTable.hpp` | 对象年龄表 (晋升决策) |
| `adaptiveSizePolicy.hpp` | 自适应大小策略 |
| `blockOffsetTable.hpp` | 块偏移表 (快速定位对象起始) |
| `copyFailedInfo.hpp` | 复制失败处理 |
| `bufferNode.hpp` | SATB/Dirty Card 缓冲队列节点 |

---

## 10. GC 选择与调优

### 10.1 选择决策树

```
需要最低延迟 (<1ms)?
  └── 是 → ZGC (-XX:+UseZGC -XX:+ZGenerational)

需要低延迟 (<10ms)?
  └── 是 → Shenandoah (-XX:+UseShenandoahGC)

需要最大吞吐量?
  └── 是 → Parallel GC (-XX:+UseParallelGC)

堆 < 100MB 或单核?
  └── 是 → Serial GC (-XX:+UseSerialGC)

通用场景 (默认):
  └── G1 GC (-XX:+UseG1GC)
```

### 10.2 G1 调优

```bash
# 基本配置
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200        # 暂停时间目标 (默认 200ms)
-XX:G1HeapRegionSize=4m         # Region 大小 (1m-32m, 2 的幂)
-XX:InitiatingHeapOccupancyPercent=45  # 触发并发标记的堆占用率

# 调试
-Xlog:gc*:file=gc.log:time,uptime,level,tags
```

### 10.3 ZGC 调优

```bash
-XX:+UseZGC
-XX:+ZGenerational              # 启用分代 ZGC
-XX:SoftMaxHeapSize=8g          # 软最大堆 (ZGC 会尽量不超过)
-Xlog:gc*:file=gc.log
```

### 10.4 Shenandoah 调优

```bash
-XX:+UseShenandoahGC
-XX:ShenandoahGCMode=generational   # 分代模式
-XX:ShenandoahGCHeuristics=adaptive # 启发式策略 (默认)
-Xlog:gc*:file=gc.log
```

---

## 11. 相关链接

- [HotSpot 模块总览](hotspot.md)
- [源码浏览](https://github.com/openjdk/jdk/tree/master/src/hotspot/share/gc)
