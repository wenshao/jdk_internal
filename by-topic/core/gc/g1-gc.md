# G1 GC 详解

> Garbage-First GC 架构、原理与 JDK 12-26 演进全解析 (基于 HotSpot 源码)

[← 返回 GC](../)

---

## 1. G1 架构原理

### 1.1 Region 布局 (区域化堆)

G1 将整个 Java Heap 划分为大小相等的独立区域 (Region)，取代了传统的物理连续分代布局。每个 Region 在逻辑上属于某一代，但物理上可以位于堆中任意位置。

```
┌─────────────────────────────────────────────────────────────────────┐
│                        G1 Heap Layout                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐    │
│  │ E  │ S  │ O  │ E  │ H  │ Hc │ O  │Free│ E  │ S  │ O  │Free│    │
│  └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘    │
│                                                                     │
│  E  = Eden Region         新对象分配 (TLAB 优先)                     │
│  S  = Survivor Region     存活对象晋升缓冲区                         │
│  O  = Old Region          长寿对象 / 经过多次 GC 存活                 │
│  H  = StartsHumongous     巨大对象起始 Region                        │
│  Hc = ContinuesHumongous  巨大对象后续 Region                        │
│  Free = 空闲 Region        可分配给任意角色                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

每个 Region 是独立的回收单元 --- G1 每次只回收价值最高（垃圾最多）的 Region 子集 (Collection Set / CSet)，这是 "Garbage-First" 名称的由来。

**源码定义**: `G1HeapRegion : public CHeapObj<mtGC>` (g1HeapRegion.hpp:71)

```cpp
// 每个 Region 的核心字段
HeapWord* const _bottom;           // Region 起始地址
HeapWord* const _end;              // Region 结束地址
Atomic<HeapWord*> _top;            // 已分配部分的末尾 (bump pointer)
G1BlockOffsetTable* _bot;          // 块偏移表，用于快速定位对象起始
G1HeapRegionType _type;            // 当前角色 (Eden/Survivor/Old/Humongous/Free)
Atomic<size_t> _pinned_object_count; // JEP 423 Region Pinning 计数器
```

### 1.2 Region 大小计算

Region 大小由 `G1HeapRegion::setup_heap_region_size()` 在 JVM 启动时确定 (g1HeapRegion.cpp:69)。

**计算规则**:

| 情况 | 逻辑 |
|------|------|
| 用户指定 `-XX:G1HeapRegionSize` | 直接使用 (向上对齐到 2 的幂) |
| 用户未指定 (值为 0) | `region_size = clamp(max_heap / 2048, 1MB, 32MB)` |

**边界常量** (g1HeapRegionBounds.hpp):

```cpp
static const size_t MIN_REGION_SIZE       = 1024 * 1024;        // 1 MB
static const size_t MAX_ERGONOMICS_SIZE   = 32 * 1024 * 1024;   // 32 MB (自动计算上限)
static const size_t MAX_REGION_SIZE       = 512 * 1024 * 1024;  // 512 MB (手动设置上限)
static const size_t TARGET_REGION_NUMBER  = 2048;                // 目标 Region 数量
```

关键实现:

```cpp
// g1HeapRegion.cpp:69-102
void G1HeapRegion::setup_heap_region_size(size_t max_heap_size) {
  size_t region_size = G1HeapRegionSize;
  if (region_size == 0) {  // 0 means ergonomic
    region_size = clamp(max_heap_size / G1HeapRegionBounds::target_number(),
                        G1HeapRegionBounds::min_size(),
                        G1HeapRegionBounds::max_ergonomics_size());
  }
  region_size = round_up_power_of_2(region_size);  // 必须是 2 的幂
  region_size = clamp(region_size,
                      G1HeapRegionBounds::min_size(),
                      G1HeapRegionBounds::max_size());
  // 设置全局常量
  GrainBytes = region_size;
  GrainWords = GrainBytes >> LogHeapWordSize;
  CardsPerRegion = GrainBytes >> G1CardTable::card_shift();  // 每 512 字节一个 Card
}
```

**常见配置对照**:

| 最大堆大小 | 自动 Region 大小 | Region 数量 |
|-----------|-----------------|------------|
| 512 MB    | 1 MB            | 512        |
| 2 GB      | 1 MB            | 2048       |
| 4 GB      | 2 MB            | 2048       |
| 8 GB      | 4 MB            | 2048       |
| 16 GB     | 8 MB            | 2048       |
| 32 GB     | 16 MB           | 2048       |
| 64 GB     | 32 MB           | 2048       |

### 1.3 G1HeapRegionType 枚举

Region 的类型通过位编码实现，高位为 major type，最低位为 minor type (g1HeapRegionType.hpp:34-74)。

```
位编码:                              十进制    语义
──────────────────────────────────────────────────────────────
00000 0  → FreeTag               = 0      空闲 Region
00001 0  → YoungMask / EdenTag   = 2      Eden Region
00001 1  → SurvTag               = 3      Survivor Region
00010 0  → HumongousMask /
           StartsHumongousTag    = 4      巨大对象起始 Region
00010 1  → ContinuesHumongousTag = 5      巨大对象后续 Region
00100 0  → OldMask / OldTag      = 8      老年代 Region
```

利用掩码实现快速类型判定:

```cpp
bool is_young()    const { return (get() & YoungMask) != 0; }      // Eden 或 Survivor
bool is_eden()     const { return get() == EdenTag; }               // 仅 Eden
bool is_survivor() const { return get() == SurvTag; }               // 仅 Survivor
bool is_humongous()const { return (get() & HumongousMask) != 0; }   // 任意 Humongous
bool is_old()      const { return (get() & OldMask) != 0; }         // Old (含 Humongous)
bool is_old_or_humongous() const { return (get() & (OldMask | HumongousMask)) != 0; }
```

**类型转换规则** (set_from 方法强制前置条件检查):

```
Free → Eden, Survivor, Old, StartsHumongous, ContinuesHumongous  (合法)
Survivor → Eden  (Pre-GC relabel, set_eden_pre_gc)
Eden/Survivor/Free → Old  (relabel_as_old, 在 Full GC 中使用)
```

### 1.4 Humongous 对象

对象大小超过 Region 容量的一半时被视为 Humongous 对象。

```cpp
// g1CollectedHeap.hpp:1220
static size_t humongous_threshold_for(size_t region_size) {
    return (region_size / 2);  // 50% of region capacity in words
}
```

Humongous 对象的存储方式:
- 第一个 Region 类型为 `StartsHumongous`，`top()` 指向对象末尾或 Region 末尾
- 如果对象跨多个 Region，后续 Region 类型为 `ContinuesHumongous`
- 最后一个 ContinuesHumongous Region 的 `top()` 指向对象实际末尾
- Humongous 对象直接分配在老年代，不经过 Eden

**影响**:
- Humongous 对象可能导致堆碎片化，因为它们占据整个 Region 或多个连续 Region
- 回收 Humongous 对象时需要特殊处理 (`EagerlyReclaimHumongousObjects` 阶段)
- 如果 Humongous 分配频繁，建议增大 `-XX:G1HeapRegionSize`

---

## 2. GC 周期详解

G1 的回收活动分为四种模式: Young GC、Concurrent Marking Cycle、Mixed GC 和 Full GC。

### 2.1 Young GC (Evacuation Pause)

**触发条件**: Eden Region 用尽时触发。所有 Eden 和 Survivor Region 构成 Collection Set (CSet)。

**执行者**: `G1YoungCollector::collect()` (g1YoungCollector.hpp:142)，STW (Stop-The-World) 暂停。

**详细步骤**:

```
                     Young GC STW Pause
                     ═══════════════════
  ┌─────────────────────────────────────────────────────────┐
  │  Phase 1: RetireTLABs                                   │
  │    回收线程本地分配缓冲区 (TLAB)                          │
  ├─────────────────────────────────────────────────────────┤
  │  Phase 2: ExtRootScan (外部根扫描)                       │
  │    ├── ThreadRoots         (线程栈中的引用)               │
  │    ├── CLDGRoots           (类加载器数据图)               │
  │    ├── CMRefRoots          (并发标记引用)                 │
  │    ├── StrongOopStorageSetRoots  (JNI Global 等)         │
  │    └── CodeRoots           (已编译代码中的引用)           │
  ├─────────────────────────────────────────────────────────┤
  │  Phase 3: MergeRS + ScanHR (合并 & 扫描堆引用)           │
  │    ├── MergeER             (合并紧急精炼任务)             │
  │    ├── MergeRS             (合并 Remembered Set)          │
  │    └── ScanHR              (扫描老年代→年轻代的引用)      │
  ├─────────────────────────────────────────────────────────┤
  │  Phase 4: ObjCopy (对象复制)                             │
  │    将存活对象从 CSet 复制到 Survivor 或 Old Region        │
  ├─────────────────────────────────────────────────────────┤
  │  Phase 5: Termination (工作窃取终止)                     │
  │    并行 GC 线程之间的负载均衡与终止协议                   │
  ├─────────────────────────────────────────────────────────┤
  │  Phase 6: Post-Evacuation (收尾)                         │
  │    ├── FreeCollectionSet    (释放 CSet 中的 Region)      │
  │    ├── RebuildFreeList      (重建空闲列表)               │
  │    ├── ClearCardTable       (清理卡表)                   │
  │    ├── EagerlyReclaimHumongousObjects                    │
  │    └── MergePSS             (合并 Per-Thread 状态)       │
  └─────────────────────────────────────────────────────────┘
```

**GC Phase 枚举** (g1GCPhaseTimes.hpp:48-92 的 `GCParPhases`):

```cpp
enum GCParPhases {
  RetireTLABs,        // TLAB 回收
  GCWorkerStart,      // GC 工作线程启动
  ExtRootScan,        // 外部根扫描
  ThreadRoots,        // 线程根
  CLDGRoots,          // ClassLoaderData 根
  CMRefRoots,         // 并发标记引用根
  StrongOopStorageSetRoots, // 强 OopStorage 根
  MergeER,            // 合并紧急精炼
  MergeRS,            // 合并 Remembered Set
  OptMergeRS,         // 可选合并 (Mixed GC)
  SweepRT,            // 扫描 Refinement Table
  ScanHR,             // 扫描堆 Region
  OptScanHR,          // 可选扫描 (Mixed GC)
  CodeRoots,          // 代码根
  ObjCopy,            // 对象复制
  OptObjCopy,         // 可选对象复制
  Termination,        // 终止协议
  // ... (约 30 个子阶段)
  EagerlyReclaimHumongousObjects,  // 急切回收 Humongous
  GCParPhasesSentinel              // 哨兵值
};
```

### 2.2 Concurrent Marking Cycle (并发标记周期)

**触发条件**: 老年代堆占用达到 IHOP (Initiating Heap Occupancy Percent) 阈值时启动。

**执行者**: `G1ConcurrentMarkThread::concurrent_mark_cycle_do()` (g1ConcurrentMarkThread.cpp:265)

**核心数据结构** (g1ConcurrentMark.hpp:346):

```cpp
class G1ConcurrentMark : public CHeapObj<mtGC> {
  G1ConcurrentMarkThread* _cm_thread;      // 执行并发标记的线程
  G1CMBitMap              _mark_bitmap;     // 标记位图: 1 bit 对应 1 个对象
  G1CMRootMemRegions      _root_regions;    // Root Region 扫描追踪
  G1CMMarkStack           _global_mark_stack; // 灰色对象全局栈
  Atomic<HeapWord*>       _finger;          // 全局扫描指针 (Region 对齐)
  uint                    _num_active_tasks; // 当前活跃标记任务数
  G1CMTask**              _tasks;           // 每个 worker 的本地任务
  G1CMTaskQueueSet*       _task_queues;     // 任务队列集
  TaskTerminator          _terminator;      // 终止协议
  PartialArrayStateManager* _partial_array_state_manager;  // 大数组分片标记
};
```

**7 个阶段详解**:

```
                    Concurrent Marking Cycle
    ════════════════════════════════════════════════

    Phase 1: Scan Root Regions                    [并发]
    ──────────────────────────────────────────────
    扫描 Survivor Region 中可能指向老年代的引用。
    必须在下一次 Young GC 之前完成。
    源码: G1ConcurrentMarkThread::phase_scan_root_regions()

    Phase 2: Concurrent Mark Loop                 [并发]
    ──────────────────────────────────────────────
    2a. Mark From Roots: 从根出发遍历对象图
        多个 CM 线程并行标记，使用 _finger 指针划分工作区域
        标记状态记录在 _mark_bitmap 中
        源码: subphase_mark_from_roots()

    2b. Preclean (预清理): 处理 SATB 队列中积累的引用变更
        减少后续 Remark 阶段的工作量
        源码: subphase_preclean()

    Phase 3: Remark                               [STW]
    ──────────────────────────────────────────────
    处理 SATB 队列中残余的引用变更，完成最终标记。
    处理弱引用 (WeakRef/SoftRef/PhantomRef)。
    源码: subphase_remark() → VM_G1PauseRemark

    Phase 4: Rebuild Remembered Sets & Scrub      [并发]
    ──────────────────────────────────────────────
    为存活对象重建 Remembered Set。
    清除死亡对象所在的区域 (Scrub Regions)。
    源码: phase_rebuild_and_scrub()

    Phase 5: Cleanup                              [STW]
    ──────────────────────────────────────────────
    统计每个 Region 的存活率。
    完全空的 Region 直接回收到 Free List。
    识别可作为 Mixed GC 候选的 Old Region。
    源码: phase_cleanup() → VM_G1PauseCleanup

    Phase 6: Clear CLD Claimed Marks              [并发]
    ──────────────────────────────────────────────
    清除 ClassLoaderData 的标记位。

    Phase 7: Clear Bitmap for Next Mark            [并发]
    ──────────────────────────────────────────────
    清理标记位图，为下次并发标记做准备。
    源码: phase_clear_bitmap_for_next_mark()
```

### 2.3 Mixed GC (混合回收)

并发标记完成后，G1 获得了每个 Old Region 的存活率数据。接下来的若干次 GC 暂停变为 Mixed GC --- 除了回收全部 Young Region，还选择若干个垃圾比例最高的 Old Region 一起回收。

**选择逻辑** (g1CollectionSet.cpp):

```
Collection Set 构建流程:
═══════════════════════
1. finalize_young_part()
   → 所有 Eden + Survivor 加入 CSet
   → 计算预测耗时，得到剩余时间 time_remaining_ms

2. select_candidates_from_marking(time_remaining_ms)
   → 从标记阶段识别的候选 Region 中选择
   → 按回收价值排序 (Garbage-First!)
   → 在时间预算内尽量多选

3. select_candidates_from_retained(time_remaining_ms)
   → 从上一轮 Mixed GC 保留的候选中继续选择

4. select_optional_groups(time_remaining_ms)
   → 可选的额外 Old Region (JEP 344 Abortable Mixed Collections)
   → 如果时间充裕就回收，超时则中止
```

源码中的关键字段 (g1CollectionSet.hpp:133):

```cpp
class G1CollectionSet {
  G1CollectionSetCandidates _candidates;   // 所有候选老年代 Region
  uint* _regions;                          // CSet 中的 Region 索引数组
  volatile uint _regions_cur_length;       // 当前 CSet 大小

  uint _eden_region_length;                // CSet 中 Eden Region 数
  uint _survivor_region_length;            // CSet 中 Survivor Region 数
  uint _initial_old_region_length;         // CSet 中必选 Old Region 数

  G1CSetCandidateGroupList _groups;        // 已选择的老年代 Region 组
  G1CSetCandidateGroupList _optional_groups; // 可选的老年代 Region 组 (可中止)
};
```

**Mixed GC 轮数**: 由 `-XX:G1MixedGCCountTarget` (默认 8) 控制。标记后识别的候选 Old Region 分散到多次 Mixed GC 中逐步回收。

### 2.4 Full GC

Full GC 是 G1 的最后手段，使用单线程或多线程 Serial/Parallel 算法对整个堆进行 Mark-Compact。

**执行者**: `G1FullCollector` (g1FullCollector.hpp:62)

**触发场景**:
- Evacuation Failure: Young/Mixed GC 时无法找到足够 Free Region 容纳存活对象
- Humongous 分配失败: 无法找到足够连续的 Free Region
- 元空间 (Metaspace) 耗尽
- `System.gc()` 调用 (除非 `-XX:+ExplicitGCInvokesConcurrent`)
- 并发标记来不及完成，老年代已满

**为什么要避免 Full GC**:
- 完全 STW，暂停时间与堆大小成正比
- 大堆 (数十 GB) 下 Full GC 可达数十秒
- 常见应对: 降低 IHOP 以更早启动并发标记；增大堆容量；避免大量 Humongous 分配

---

## 3. Remembered Sets (RSet) 与 Card Table

### 3.1 为什么需要 RSet

G1 回收某个 Region 时，需要知道堆中其他 Region 是否有引用指向该 Region。如果没有 RSet，就必须扫描整个堆才能找到这些跨 Region 引用，这在大堆环境下代价极高。

RSet 的核心思想是 **"记录谁引用了我"** --- 每个 Region 维护一个 RSet，记录了哪些外部 Card 包含指向本 Region 的引用。

```
  Old Region A              Old Region B             Young Region C
  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
  │  obj_x ──────┼────────►│  obj_y       │         │  obj_z       │
  │              │         │     │        │         │              │
  │              │         │     └────────┼────────►│              │
  └──────────────┘         └──────────────┘         └──────────────┘
                            RSet of B:               RSet of C:
                            {Region A, Card X}       {Region B, Card Y}
```

**源码结构** (g1HeapRegionRemSet.hpp:41):

```cpp
class G1HeapRegionRemSet : public CHeapObj<mtGC> {
  G1CodeRootSet _code_roots;           // 编译代码中指向本 Region 的引用
  G1CSetCandidateGroup* _cset_group;   // 所属的 CSet 候选组
  G1HeapRegion* _hr;                   // 所属 Region
  // RSet 实际数据存储在 _cset_group->card_set() 中
};
```

### 3.2 G1CardSet 多级容器结构

G1CardSet 使用自适应的多级容器来存储引用信息，从紧凑到稀疏逐级粗化 (coarsening)，以平衡内存占用和查询效率。

**ContainerPtr 编码** (g1CardSet.hpp:246-256):

```cpp
using ContainerPtr = void*;
static const uintptr_t ContainerInlinePtr    = 0x0;  // LSB 00: 内联指针
static const uintptr_t ContainerArrayOfCards = 0x1;  // LSB 01: 卡数组
static const uintptr_t ContainerBitMap       = 0x2;  // LSB 10: 位图
static const uintptr_t ContainerHowl         = 0x3;  // LSB 11: Howl 容器
static constexpr ContainerPtr FreeCardSet    = nullptr;
static ContainerPtr FullCardSet;                      // 全部位设置 (0xFFFF...FFFF)
```

**粗化升级路径**:

```
    顶层 (Region 级别):
    ────────────────────────────────────────────────────────
    ContainerInlinePtr → ContainerArrayOfCards → ContainerHowl → Full

    Howl 内部 (子区域级别):
    ────────────────────────────────────────────────────────
    Free → ContainerInlinePtr → ContainerArrayOfCards → ContainerBitMap → Full
```

各容器详解:

| 容器类型 | 数据结构 | 容量 | 内存开销 | 使用场景 |
|---------|---------|------|---------|---------|
| **InlinePtr** | 直接在指针的高位中编码几个 Card 索引 | 2-3 个 Card | 0 额外内存 | 极少量跨 Region 引用 |
| **ArrayOfCards** | 连续数组存储 Card 索引 | 可配置 (默认 ~16) | 数十字节 | 少量引用 |
| **Howl** | 二级结构: 数组 of ContainerPtr，每个子 ContainerPtr 覆盖子区域 | 数千 Card | 数百字节~数 KB | 中等引用 |
| **Howl 内 BitMap** | 位图，每 bit 对应一个 Card | 子区域内所有 Card | 固定 | Howl 子区域引用多 |
| **Full** | 标记整个区域 (或 Howl 子区域) 为"全脏" | 全覆盖 | 0 额外内存 | 几乎全部 Card 被引用 |

**配置参数** (g1CardSet.hpp 中的 `G1CardSetConfiguration`):

```cpp
class G1CardSetConfiguration {
  uint _inline_ptr_bits_per_card;          // InlinePtr 中每个 Card 占用的位数
  uint _max_cards_in_array;                // ArrayOfCards 最大容量
  uint _num_buckets_in_howl;               // Howl 中的桶数 (子 ContainerPtr 数)
  uint _max_cards_in_howl_bitmap;          // Howl 子位图中的最大 Card 数
  uint _cards_in_howl_threshold;           // Howl → Full 的阈值
  uint _cards_in_howl_bitmap_threshold;    // Howl 子位图 → Howl Full 的阈值
  uint _max_cards_in_card_set;             // 单个 Card Region 的最大 Card 数
  // num_mem_object_types() = 4: CHT-Nodes, ArrayOfCards, BitMaps, Howl
};
```

### 3.3 Card Table

G1 的 Card Table 将堆内存按 512 字节一个 Card 进行划分，每个 Card 用一个字节 (CardValue) 表示状态。

**Card 值定义** (g1CardTable.hpp:53-94):

```cpp
enum G1CardValues {
  g1_dirty_card          = 0x00,  // 脏: 需要扫描 (Mutator 写脏)
  g1_card_already_scanned = 0x01, // 已扫描: GC 期间标记，不需再扫
  g1_to_cset_card        = 0x02,  // 指向 CSet: 引用了 CSet 中的对象
  g1_from_remset_card    = 0x04   // 来自 RSet: 由 RSet 生成，非 Mutator
};
```

LSB 语义: LSB 为 1 表示 Clean (已扫描)，为 0 表示 Non-clean (需扫描)。

**Dual Card Table (JDK 26 / JEP 522)**:

从 JDK 26 开始，G1 维护两张卡表 (g1BarrierSet.hpp:38-65):

```cpp
class G1BarrierSet: public CardTableBarrierSet {
  G1SATBMarkQueueSet _satb_mark_queue_set;
  Atomic<G1CardTable*> _refinement_table;  // 第二张卡表

  // Mutator 写脏 card_table (当前表)
  // Refinement 线程处理 refinement_table (另一张表)
  // 阈值触发时交换两张表
  void swap_global_card_table();
};
```

分离的好处:
- Mutator 线程和 Refinement 线程各自操作不同的卡表
- **消除了 per-write 的细粒度同步** (不再需要 CAS 或 memory barrier)
- 写屏障可以使用简单的 `mov` 指令代替 `lock cmpxchg`

### 3.4 写屏障 (Write Barrier)

G1 使用两种写屏障:

**Pre-Write Barrier (SATB 屏障)**:

```
伪代码:
if (marking_active) {
    oop old_value = *field;       // 读取被覆盖的旧引用
    if (old_value != null) {
        satb_enqueue(old_value);  // 压入 SATB 队列
    }
}
*field = new_value;               // 执行实际赋值
```

**Post-Write Barrier (Card Marking 屏障)**:

```
伪代码 (JDK 26+ Dual Card Table):
*field = new_value;                         // 执行实际赋值
CardValue* card = card_table_base + ((uintptr_t)field >> 9);  // 512 字节/Card
if (*card != dirty) {
    *card = dirty;                          // 简单 store, 无原子操作
}
```

**源码入口** (g1BarrierSet.hpp:101-107):

```cpp
template <DecoratorSet decorators, typename T>
void write_ref_field_pre(T* field);   // SATB pre-barrier

template <DecoratorSet decorators = DECORATORS_NONE, typename T>
void write_ref_field_post(T* field);  // Card marking post-barrier
```

### 3.5 Refinement (并发卡表精炼)

Refinement 线程负责将脏 Card 信息转换为 RSet 条目:

```
  Mutator Thread            Refinement Thread          G1 GC Pause
  ─────────────            ──────────────────          ────────────
  obj.field = ref;
  → 写脏 card_table         card_table swap 后
                            处理 refinement_table:
                            → 找到脏 Card
                            → 确定引用的目标 Region
                            → 更新目标 Region 的 RSet     扫描 RSet
                                                          → 定位跨 Region 引用
                                                          → 作为 GC Root
```

**Claim Table** (JEP 522, g1CardTableClaimTable.hpp:44):

```cpp
class G1CardTableClaimTable : public CHeapObj<mtGC> {
  uint _max_reserved_regions;
  Atomic<uint>* _card_claims;  // 每个 Region 一个原子计数器
  uint _cards_per_chunk;       // Chunk 粒度

  // GC 工作线程按 chunk 认领脏卡段
  inline uint claim_chunk(uint region);
  inline uint claim_all_cards(uint region);
};
```

`G1CardTableChunkClaimer` 和 `G1ChunkScanner` 配合实现高效的脏卡扫描:
- `G1CardTableChunkClaimer`: 按 chunk 认领 Region 内的卡段，避免线程竞争
- `G1ChunkScanner`: 在 chunk 内快速定位连续脏卡区间

---

## 4. SATB (Snapshot-At-The-Beginning)

### 4.1 三色标记与并发标记的挑战

G1 的并发标记使用经典的三色标记法:
- **白色**: 未被访问的对象 (标记结束后仍为白色的对象是垃圾)
- **灰色**: 已被访问但其引用字段尚未完全扫描
- **黑色**: 已被访问且其所有引用字段已扫描完毕

并发标记与 Mutator 同时运行时，存在**对象消失 (Lost Object) 问题**:

```
初始状态:            Mutator 操作后:           结果:
A (黑) → B (灰)     A (黑) → C (白)           C 应该存活但被漏标!
B (灰) → C (白)     B (灰) -x→ C              (对象消失)

条件 (Wilson & Johnstone, 1994):
1. 黑色对象插入了一条指向白色对象的新引用  (Insertion)
2. 同时灰色对象删除了指向该白色对象的引用  (Deletion)
两个条件同时满足才会导致对象消失。
```

### 4.2 SATB 不变量

SATB 通过**打破条件 2** 来保证正确性: 当 Mutator 覆盖一个引用时，旧值被保存 (snapshot)，确保标记开始时的对象图快照中所有可达对象都不会被漏标。

```
SATB 语义:
  标记开始时的存活对象 + 标记期间新分配的对象 = 标记结果中的存活对象
```

### 4.3 Pre-Write Barrier 实现

```cpp
// 概念实现 (g1BarrierSet.hpp:92-93)
template <class T> static void enqueue(T* dst);       // 将被覆盖的旧值入队
static void enqueue_preloaded(oop pre_val);            // 直接将 oop 入队
```

每个 Java 线程维护一个线程本地的 SATB 缓冲区 (SATBMarkQueue)。当缓冲区满时，整块提交到全局的 `G1SATBMarkQueueSet` 中。Remark 阶段 (STW) 处理所有未处理的 SATB 缓冲区。

```
  Thread 1          Thread 2          SATB Global Queue
  ────────          ────────          ─────────────────
  obj.f = new_ref;
  enqueue(old_ref)
  → [SATB Buffer 1]  obj.g = null;
                      enqueue(old_ref2)
                      → [SATB Buffer 2]
                                        ← Buffer 1 (满了提交)
                                        ← Buffer 2 (满了提交)
                                        ...
                                        Remark 时全部处理
```

### 4.4 为什么选择 SATB 而非 Incremental Update

| 维度 | SATB (G1/Shenandoah) | Incremental Update (CMS) |
|------|---------------------|-------------------------|
| **打破的条件** | 条件 2 (捕获删除) | 条件 1 (捕获插入) |
| **Barrier 位置** | Pre-write | Post-write |
| **Remark 工作量** | 仅处理 SATB 队列 | 需要重新扫描脏 Card |
| **Remark 暂停** | 更短且可预测 | 与脏 Card 数量相关，可能很长 |
| **浮动垃圾** | 标记期间变为垃圾的对象在本轮存活 | 同样有浮动垃圾 |
| **精度** | 稍保守 (多保留对象) | 稍精确 |

SATB 的关键优势: **Remark 暂停时间短且可预测**。这对 G1 的 "可预测停顿" 目标至关重要。Incremental Update (如 CMS) 的 Final Remark 可能因 Mutator 频繁写引用而大幅延长。

---

## 5. JEP 演进 (从源码验证)

### 5.1 JEP 344 (JDK 12): Abortable Mixed Collections

**问题**: Mixed GC 选入过多 Old Region 时，暂停时间可能超出目标。

**解决方案**: 将 Mixed GC 的 Old Region 分为 mandatory (必选) 和 optional (可选) 两组。必选组先处理，可选组按时间预算逐个处理，超时即中止。

**源码验证** (g1CollectionSet.hpp:166):

```cpp
// 可选的老年代 Region 组 --- JEP 344 的核心机制
G1CSetCandidateGroupList _optional_groups;

// 选择可选组 (g1CollectionSet.cpp:672)
uint G1CollectionSet::select_optional_groups(double time_remaining_ms);
double G1CollectionSet::select_candidates_from_optional_groups(
    double time_remaining_ms, uint& num_groups_selected);
```

### 5.2 JEP 345 (JDK 14): NUMA-Aware Memory Allocation

**目标**: 在多 NUMA 节点系统上，尽量将 Eden Region 分配到线程所在的 NUMA 节点。

**源码验证** (g1NUMA.hpp):

```cpp
class G1NUMA: public CHeapObj<mtGC> {
  static G1NUMA* _inst;
  G1NUMAStats* _stats;         // NUMA 统计信息

  void initialize(bool use_numa);
  static G1NUMA* numa() { return _inst; }
};
```

使用 `-XX:+UseNUMA` 启用 (需 Linux 或 Solaris)。G1CollectedHeap 中通过 `_numa` 字段引用 (g1CollectedHeap.hpp:239)。

### 5.3 JEP 346 (JDK 12): Promptly Return Unused Committed Memory

**目标**: G1 在空闲时 (低负载或 idle) 主动向操作系统释放 (uncommit) 未使用的 Region 内存。

**源码验证** (g1CollectedHeap.hpp:604-606):

```cpp
void uncommit_regions_if_necessary();
uint uncommit_regions(uint region_limit);
```

配合 `G1PeriodicGCInterval` 参数触发周期性 GC，回收后的空 Region 可以 uncommit。

### 5.4 JEP 423 (JDK 22): Region Pinning for G1

**问题**: JNI GetPrimitiveArrayCritical 获取直接指针后，传统做法是禁用整个 GC 直到 ReleasePrimitiveArrayCritical 调用。这严重影响 GC 延迟。

**解决方案**: 只固定 (pin) 包含 JNI critical 对象的 Region，允许 GC 继续回收其他 Region。

**源码验证** (g1HeapRegion.hpp:252-253, 397-398):

```cpp
// Region 级别的 pin 计数器
Atomic<size_t> _pinned_object_count;

// 操作 API
inline void add_pinned_object_count(size_t value);
inline size_t pinned_count() const;
inline bool has_pinned_objects() const;
```

被 pin 的 Region 不会被加入 Collection Set，GC 期间跳过该 Region 的 evacuation。

### 5.5 JEP 475 (JDK 24): Late Barrier Expansion

**目标**: 将 GC 写屏障的生成推迟到 C2 编译管线的后期阶段 (Late Barrier Expansion)。

**优点**:
- C2 优化器可以在更长窗口内优化应用代码，不被屏障代码干扰
- 屏障代码可以受益于更多寄存器分配优化
- 减少了屏障与应用代码交织导致的编译复杂度

该 JEP 是编译器层面的改进，不直接修改 G1 的 runtime 源码文件，主要影响 `c2_BarrierSetSpecific` 相关的编译器后端代码。

### 5.6 JEP 522 (JDK 26): Improve G1 Throughput with a Dual Card Table

**核心改进**: 引入 Dual Card Table + ClaimTable 机制，大幅降低写屏障和 Refinement 的同步开销。

**Dual Card Table 架构** (g1BarrierSet.hpp:38-64):

```
┌─────────────────────────────────────────────────────────────────┐
│                    Dual Card Table 架构                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Card Table A (当前)        Card Table B (精炼)                  │
│  ┌──────────────────┐      ┌──────────────────┐                 │
│  │ Mutator 线程写脏  │      │ Refinement 处理  │                 │
│  │ 简单 store, 无 CAS │      │ 更新 RSet        │                 │
│  └──────────────────┘      └──────────────────┘                 │
│           │                         │                           │
│           └── 阈值触发 swap_global_card_table() ──┘              │
│                                                                 │
│  ClaimTable (认领表)                                             │
│  ┌──────────────────┐                                           │
│  │ 每 Region 一个    │ GC Worker 按 chunk 认领脏卡段              │
│  │ Atomic<uint>     │ 避免并行扫描时的竞争                        │
│  └──────────────────┘                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**性能收益** (基于 SPECjbb2015):

| 指标 | 改进幅度 | 说明 |
|------|---------|------|
| max-jOPS | +15.6% | 峰值吞吐量 |
| critical-jOPS | +16.7% | 低延迟吞吐量 |
| GC 暂停时间 | -20.8% | 平均暂停缩短 |
| 写屏障 CPU 占比 | 8% → 3% | 大幅释放计算资源 |

**汇编级对比** (x86-64):

| 方面 | JDK 25 及之前 | JDK 26 (JEP 522) |
|------|-------------|------------------|
| 核心指令 | `lock cmpxchg` (原子 CAS) | `cmp` + `mov` (普通 load/store) |
| 约指令数 | ~50 | ~12 |
| Mutator/Refinement 同步 | 共享同一卡表，存在竞争 | 各用各的卡表，近乎零竞争 |

**关键源码文件**:
- `g1CardTableClaimTable.hpp/cpp`: ClaimTable 的核心实现
- `g1BarrierSet.hpp`: Dual Card Table 管理 (`_refinement_table`, `swap_global_card_table()`)
- `g1CardTable.hpp`: Card 值定义与扫描逻辑

---

## 6. 关键调优参数

### 6.1 核心参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-XX:+UseG1GC` | JDK 9+ 默认 | 启用 G1 收集器 |
| `-XX:MaxGCPauseMillis=<ms>` | 200 | 目标最大停顿时间 (软目标) |
| `-XX:G1HeapRegionSize=<size>` | 自动 | Region 大小 (1MB~32MB, 手动可到 512MB, 必须 2 的幂) |

### 6.2 年轻代大小

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-XX:G1NewSizePercent` | 5 | 年轻代最小占比 (堆的百分比) |
| `-XX:G1MaxNewSizePercent` | 60 | 年轻代最大占比 |

G1 在每次 GC 后动态调整年轻代大小以满足 `MaxGCPauseMillis` 目标。年轻代过小会增加 GC 频率；过大会延长单次暂停时间。

### 6.3 IHOP (Initiating Heap Occupancy Percent)

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-XX:InitiatingHeapOccupancyPercent` | 45 | 并发标记触发阈值 (老年代占比) |
| `-XX:G1UseAdaptiveIHOP` | true | 启用自适应 IHOP |

**Adaptive IHOP** (g1IHOPControl.hpp:39):

自适应 IHOP 根据历史数据动态调整阈值:

```cpp
class G1IHOPControl : public CHeapObj<mtGC> {
  const bool _is_adaptive;                // 是否启用自适应
  double _initial_ihop_percent;           // 初始 IHOP 值
  size_t _target_occupancy;              // 目标最大堆占用
  TruncatedSeq _marking_times_s;         // 标记耗时历史
  TruncatedSeq _allocation_rate_s;       // 分配速率历史
  size_t _last_unrestrained_young_size;  // 最近的无约束年轻代大小

  // 核心: 根据历史预测何时应启动标记
  size_t get_conc_mark_start_threshold();
};
```

自适应逻辑: 追踪标记耗时和 Mutator 分配速率，预测"从启动标记到标记完成期间，老年代会增长多少"，据此提前或推迟启动并发标记。

### 6.4 Mixed GC 控制

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-XX:G1MixedGCCountTarget` | 8 | 标记后的候选 Old Region 分几轮 Mixed GC 回收 |
| `-XX:G1MixedGCLiveThresholdPercent` | 85 | 存活率高于此值的 Old Region 不纳入候选 |
| `-XX:G1HeapWastePercent` | 5 | 可回收空间低于此值时停止 Mixed GC 周期 |
| `-XX:G1OldCSetRegionThresholdPercent` | 10 | 单次 Mixed GC 中 Old Region 占比上限 |

### 6.5 Refinement 线程

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-XX:G1ConcRefinementThreads` | 自动 | 并发精炼线程数 |

### 6.6 Humongous 优化

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-XX:G1HeapRegionSize` | 自动 | 增大 Region Size 可减少 Humongous 分配 |
| `-XX:+G1EagerReclaimHumongousObjects` | true | Young GC 时急切回收无引用的 Humongous |

### 6.7 配置示例

```bash
# 常规 Web 应用 (8 GB 堆, 目标 100ms 暂停)
java -XX:+UseG1GC \
     -Xms8g -Xmx8g \
     -XX:MaxGCPauseMillis=100 \
     -XX:G1HeapRegionSize=4m \
     -XX:InitiatingHeapOccupancyPercent=40 \
     -Xlog:gc*:file=gc.log:time,uptime,level,tags

# 大堆低延迟 (32 GB 堆, 目标 50ms 暂停)
java -XX:+UseG1GC \
     -Xms32g -Xmx32g \
     -XX:MaxGCPauseMillis=50 \
     -XX:G1HeapRegionSize=16m \
     -XX:G1NewSizePercent=10 \
     -XX:G1MaxNewSizePercent=40 \
     -XX:+UseNUMA

# 解决 Full GC 频繁的场景
java -XX:+UseG1GC \
     -Xms16g -Xmx16g \
     -XX:InitiatingHeapOccupancyPercent=35 \
     -XX:G1MixedGCCountTarget=4 \
     -XX:G1HeapWastePercent=3
```

---

## 7. G1 vs ZGC vs Shenandoah 对比

| 维度 | G1 GC | ZGC | Shenandoah |
|------|-------|-----|------------|
| **引入版本** | JDK 7u4 (JDK 9 默认) | JDK 15 (Production) | JDK 15 (Production) |
| **设计目标** | 可预测停顿 + 高吞吐 | 亚毫秒级停顿 | 低停顿 |
| **最大暂停 (典型)** | 数十~数百 ms | <1 ms | <10 ms |
| **堆大小支持** | 数 MB ~ 数 TB | 8 MB ~ 16 TB | 数 MB ~ 数 TB |
| **算法** | 分代 Region 标记-复制 | Colored Pointer + Load Barrier | Brooks Pointer + 并发复制 |
| **并发标记** | SATB | Colored Pointer | SATB (同 G1) |
| **并发压缩 (evacuation)** | 否 (STW evacuation) | 是 (并发 relocation) | 是 (并发 evacuation) |
| **分代** | 是 (逻辑分代) | JDK 21+ 分代 ZGC | 否 (单代) |
| **写屏障** | Pre (SATB) + Post (Card) | 无写屏障 | Pre (SATB) + Read (Brooks) |
| **读屏障** | 无 | Load Barrier (Colored Ptr) | 无 (JDK 17+ 去除) |
| **吞吐量** | 高 (JEP 522 后更优) | 中 (Load Barrier 开销) | 中 |
| **CPU 开销** | 中 (写屏障 + Refinement) | 低~中 (Load Barrier) | 中 (并发复制) |
| **内存开销** | 中 (RSet ~5-20%) | 低 (无 RSet) | 中 (forwarding ptr) |
| **适用场景** | 通用服务端, 大多数工作负载 | 超大堆, 延迟敏感 | 低延迟, Mutator 密集 |
| **推荐使用** | 默认首选 | 需要亚毫秒暂停时 | 需要低暂停 + 非 Oracle JDK |
| **JNI Critical** | JEP 423 Region Pinning | 原生支持 | 需要 Full GC 退化 |

**选择建议**:
- **默认选择 G1**: 兼顾吞吐量和停顿时间，生态最成熟，JEP 522 后吞吐量与 Parallel GC 接近
- **选择 ZGC**: 堆 >16 GB 且对尾延迟极度敏感 (如金融交易)，可接受少量吞吐损失
- **选择 Shenandoah**: 与 ZGC 类似的低延迟需求，但使用非 Oracle JDK (如 Red Hat)

---

## 8. 诊断与监控

### 8.1 GC 日志 (-Xlog)

JDK 9+ 使用统一日志框架:

```bash
# 基本 GC 日志
-Xlog:gc:file=gc.log:time,uptime,level,tags

# 详细的 GC 阶段耗时 (推荐)
-Xlog:gc*:file=gc.log:time,uptime,level,tags

# GC 阶段子阶段详情
-Xlog:gc+phases=debug

# RSet 更新和扫描详情
-Xlog:gc+remset=trace

# Concurrent Marking 详情
-Xlog:gc+marking=debug

# Humongous 分配追踪
-Xlog:gc+humongous=debug

# Region 摘要 (每次 GC 后)
-Xlog:gc+heap=info

# IHOP 决策过程
-Xlog:gc+ihop=debug

# Card Table / Refinement 详情 (JDK 26+)
-Xlog:gc+refine=debug

# 组合: 全部 debug 级别输出到文件 (生产环境慎用)
-Xlog:gc*=debug:file=gc-debug.log:time,uptime,level,tags:filecount=5,filesize=100m
```

### 8.2 GC 日志解读示例

**Young GC 日志**:

```
[2.345s][info][gc] GC(12) Pause Young (Normal) (G1 Evacuation Pause)
                       25M->12M(256M) 8.123ms
```

关键字段:
- `Pause Young (Normal)`: 普通 Young GC
- `Pause Young (Concurrent Start)`: Young GC + 启动并发标记
- `Pause Young (Mixed)`: Mixed GC
- `Pause Young (Prepare Mixed)`: 准备进入 Mixed GC 阶段
- `25M->12M(256M)`: GC 前堆使用 → GC 后堆使用 (堆容量)
- `8.123ms`: 暂停时间

**gc+phases=debug 输出**:

```
[gc,phases] GC(12)   Pre Evacuate Collection Set: 0.2ms
[gc,phases] GC(12)     Retire TLABs: 0.0ms
[gc,phases] GC(12)   Merge Heap Roots: 1.2ms
[gc,phases] GC(12)     Merge Remembered Sets: 0.8ms
[gc,phases] GC(12)   Evacuate Collection Set: 5.3ms
[gc,phases] GC(12)     Ext Root Scanning: 0.5ms
[gc,phases] GC(12)     Scan Heap Roots: 1.2ms
[gc,phases] GC(12)     Object Copy: 3.1ms
[gc,phases] GC(12)     Termination: 0.1ms
[gc,phases] GC(12)   Post Evacuate Collection Set: 1.4ms
[gc,phases] GC(12)     Free Collection Set: 0.3ms
[gc,phases] GC(12)     Clear Card Table: 0.2ms
[gc,phases] GC(12)     Rebuild Free List: 0.1ms
```

### 8.3 JFR (Java Flight Recorder) GC 事件

```bash
# 启动 JFR 录制
java -XX:StartFlightRecording=filename=gc.jfr,settings=profile ...

# 或运行时启动
jcmd <pid> JFR.start filename=gc.jfr duration=60s settings=profile
```

**关键 GC 事件** (可在 JMC 中分析):

| JFR 事件 | 说明 |
|----------|------|
| `jdk.GarbageCollection` | GC 暂停概要 (原因、时间、前后堆使用) |
| `jdk.YoungGarbageCollection` | Young/Mixed GC 详情 |
| `jdk.OldGarbageCollection` | Full GC 详情 |
| `jdk.G1GarbageCollection` | G1 特定详情 (CSet 大小等) |
| `jdk.GCPhasePause` | 各阶段暂停时间 |
| `jdk.GCPhaseConcurrent` | 并发阶段耗时 |
| `jdk.G1HeapSummary` | GC 前后的堆分区摘要 |
| `jdk.G1HeapRegionTypeChange` | Region 类型变更事件 |
| `jdk.PromoteObjectInNewPLAB` | 对象晋升事件 |
| `jdk.EvacuationFailed` | Evacuation 失败事件 |
| `jdk.ConcurrentModeFailure` | 并发模式失败 |

### 8.4 jstat 实时监控

```bash
# 每秒输出 GC 统计
jstat -gcutil <pid> 1000

# 输出示例:
#  S0     S1     E      O      M      CCS    YGC  YGCT   FGC  FGCT   CGC  CGCT   GCT
#  0.00  45.23  67.89  32.10  95.67  92.34   42   0.856   0   0.000   3   0.234  1.090

# 关键列:
# E  = Eden 使用率
# O  = Old 使用率
# YGC / YGCT = Young GC 次数 / 累计时间
# FGC / FGCT = Full GC 次数 / 累计时间 (期望 FGC=0)
# CGC / CGCT = Concurrent GC 次数 / 累计时间
```

### 8.5 常见问题诊断

**问题 1: Full GC 频繁**

```
症状: 日志中出现 "Pause Full" 且 FGC 持续增长
原因: 并发标记来不及完成, Evacuation Failure
诊断: -Xlog:gc+heap=info 查看每次 GC 前后的 Old 占比
方案:
  1. 降低 IHOP: -XX:InitiatingHeapOccupancyPercent=35
  2. 增加堆大小
  3. 减少 Humongous 分配
```

**问题 2: 暂停时间超出目标**

```
症状: Pause Young 经常 > MaxGCPauseMillis
原因: CSet 过大 / RSet 扫描耗时 / 对象复制耗时
诊断: -Xlog:gc+phases=debug 找到最耗时的子阶段
方案:
  1. 若 Scan Heap Roots 耗时 → RSet 过大, 检查跨 Region 引用模式
  2. 若 Object Copy 耗时 → 存活率高, 考虑减少 G1MaxNewSizePercent
  3. 若 Merge Remembered Sets 耗时 → 增加 G1ConcRefinementThreads
```

**问题 3: Humongous 分配频繁**

```
症状: -Xlog:gc+humongous=debug 大量 "Humongous Allocation" 日志
原因: 对象 > 50% Region Size
方案:
  1. 增大 Region Size: -XX:G1HeapRegionSize=32m
  2. 检查应用代码中的大数组分配
  3. 确保 G1EagerReclaimHumongousObjects 已启用 (默认)
```

**问题 4: 长时间的 Concurrent Marking**

```
症状: "Concurrent Mark Cycle" 耗时数秒
原因: 存活对象多, 标记线程不足
诊断: -Xlog:gc+marking=debug
方案:
  1. 增加 ConcGCThreads (默认为 ParallelGCThreads/4)
  2. 降低 IHOP 以更早启动
```

---

## 9. 源码导航

G1 GC 核心源码位于 `src/hotspot/share/gc/g1/` (约 257 个 .hpp/.cpp 文件)。

| 文件 | 说明 |
|------|------|
| `g1CollectedHeap.hpp/cpp` | G1 堆管理入口, `G1CollectedHeap` 类 |
| `g1HeapRegion.hpp/cpp` | Region 定义, 地址计算, 大小设置 |
| `g1HeapRegionType.hpp` | Region 类型枚举 (Free/Eden/Survivor/Old/Humongous) |
| `g1HeapRegionBounds.hpp` | Region 大小边界常量 |
| `g1HeapRegionRemSet.hpp` | 每个 Region 的 Remembered Set |
| `g1CardSet.hpp/cpp` | 多级 Card Set 容器 (InlinePtr/Array/Howl/BitMap/Full) |
| `g1CardSetContainers.hpp/cpp` | Card Set 容器实现 |
| `g1CardTable.hpp/cpp` | Card Table 及 Card 值定义 |
| `g1CardTableClaimTable.hpp/cpp` | JEP 522 ClaimTable 实现 |
| `g1BarrierSet.hpp/cpp` | 写屏障, Dual Card Table 管理, SATB 队列 |
| `g1RemSet.hpp/cpp` | Remembered Set 整体管理, merge/scan |
| `g1ConcurrentMark.hpp/cpp` | 并发标记核心逻辑 |
| `g1ConcurrentMarkThread.cpp` | 并发标记线程, 7 阶段调度 |
| `g1CollectionSet.hpp/cpp` | Collection Set 构建与 Region 选择 |
| `g1Policy.hpp/cpp` | GC 策略: 暂停时间预测, IHOP, 年轻代调整 |
| `g1IHOPControl.hpp/cpp` | Adaptive IHOP 控制器 |
| `g1YoungCollector.hpp/cpp` | Young/Mixed GC 执行逻辑 |
| `g1FullCollector.hpp/cpp` | Full GC 执行逻辑 |
| `g1GCPhaseTimes.hpp/cpp` | GC 阶段计时与统计 |
| `g1NUMA.hpp/cpp` | NUMA 感知内存分配 |
| `g1Allocator.hpp/cpp` | Region 分配器 (Eden/Survivor/Old) |

---

## 相关链接

- [GC 演进时间线](timeline.md)
- [VM 参数完整参考](vm-parameters.md)
- [G1 GC 源码 (GitHub)](https://github.com/openjdk/jdk/tree/master/src/hotspot/share/gc/g1)
