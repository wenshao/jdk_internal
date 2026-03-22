# JEP 522 深入分析: G1 GC Throughput Improvement

> 本文档基于 HotSpot 源码深入分析 JEP 522 的实现。核心优化是引入双卡表架构 (dual card
> table) 来消除 mutator 与并发优化线程之间的细粒度同步，从而提高 G1 GC 的吞吐量。
> 所有类名和数据结构均来自实际源码验证。

---

## 1. 问题分析 (Problem Analysis)

### 1.1 G1 GC 写屏障的传统开销

G1 使用写屏障 (write barrier) 跟踪跨 Region 的引用，以维护 Remembered Set (RSet)。
每次应用线程 (mutator) 执行引用写入时，写屏障标记卡表 (card table) 中对应的条目为脏 (dirty)。

传统设计中，mutator 和并发优化线程 (refinement thread) 共享同一张卡表：

```
传统架构 (JEP 522 之前):
┌───────────────────────────────────────────────────────┐
│              共享卡表 (Single Card Table)                │
│  [0][0][1][0][1][0][0][1][0][0][1][0][0][1][0][0]...  │
│      ↑       ↑       ↑       ↑                        │
│   Mutator  Mutator  Refine  Mutator                   │
│   Thread1  Thread2  Thread  Thread3                   │
│                                                       │
│  问题: Mutator 标记脏卡 vs Refinement 清除脏卡        │
│  需要同步机制保证一致性                                │
└───────────────────────────────────────────────────────┘
```

### 1.2 具体性能瓶颈

1. **每次写入的同步开销 (Per-write synchronization)**: Mutator 标记卡表项时需要考虑
   refinement 线程可能同时清除该项。传统实现需要条件检查和/或原子操作。

2. **Dirty Card Queue 开销**: 传统实现中 mutator 将脏卡放入线程本地的 dirty card queue，
   refinement 线程从全局队列中取出处理。这种队列传递机制本身有开销。

3. **Refinement 线程与 mutator 的竞争**: 当 refinement 线程处理脏卡同时 mutator 又
   标记新的脏卡时，存在读写竞争。

4. **GC 暂停期间的卡表合并**: GC 暂停时需要从各种来源合并脏卡到卡表，增加暂停时间。

---

## 2. 双卡表架构 (Dual Card Table Architecture)

### 2.1 核心设计思想

JEP 522 的核心创新是引入**双卡表架构**：mutator 和 refinement 线程各使用独立的卡表，
彼此不干扰：

```
JEP 522 架构:
┌───────────────────────────────────────────────────────┐
│           卡表 (Card Table) -- Mutator 使用            │
│  [0][0][1][0][1][0][0][1][0][0][1][0][0][1][0][0]...  │
│      ↑       ↑               ↑                        │
│   Mutator  Mutator         Mutator                    │
│   Thread1  Thread2         Thread3                    │
│                                                       │
│  Mutator 只写自己的卡表，无需与任何人同步              │
└───────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────┐
│       精炼表 (Refinement Table) -- Refinement 使用     │
│  [0][0][1][0][0][0][0][1][0][0][0][0][0][0][0][0]...  │
│              ↑           ↑                             │
│           Refine      Refine                          │
│           Thread1     Thread2                         │
│                                                       │
│  Refinement 线程处理上一轮交换过来的脏卡               │
└───────────────────────────────────────────────────────┘
```

当 refinement table 上的脏卡量超过阈值时，G1 **交换** (swap) 两张卡表的指针，
让 refinement 线程处理之前 mutator 积累的脏卡，同时 mutator 继续在（现在清空的）
另一张卡表上工作。

### 2.2 G1BarrierSet -- 双卡表管理

**文件**: `src/hotspot/share/gc/g1/g1BarrierSet.hpp`

源码中 `G1BarrierSet` 明确管理两张卡表：

```cpp
// 源码注释原文：
// This barrier set is specialized to manage two card tables:
// * one the mutator is currently working on ("card table")
// * one the refinement threads or GC during pause are working on
//   ("refinement table")
//
// The card table acts like a regular card table where the mutator dirties
// cards containing potentially interesting references.
//
// When the amount of dirty cards on the card table exceeds a threshold,
// G1 swaps the card tables and has the refinement threads reduce them by
// "refining" them.
//
// This separation of data the mutator and refinement threads are working on
// removes the need for any fine-grained (per mutator write) synchronization
// between them, keeping the write barrier simple.

class G1BarrierSet: public CardTableBarrierSet {
private:
    BufferNode::Allocator _satb_mark_queue_buffer_allocator;
    G1SATBMarkQueueSet _satb_mark_queue_set;

    Atomic<G1CardTable*> _refinement_table;  // 精炼表指针 (原子访问)

public:
    G1BarrierSet(G1CardTable* card_table, G1CardTable* refinement_table);
};
```

关键要点：
- `_refinement_table` 使用 `Atomic<G1CardTable*>` 声明，支持原子交换
- 继承自 `CardTableBarrierSet`，基类持有当前 mutator 使用的卡表
- 两张卡表都是 `G1CardTable` 实例

### 2.3 G1CardTable -- 卡表值定义

**文件**: `src/hotspot/share/gc/g1/g1CardTable.hpp`

G1 卡表中每个条目是一个字节 (`CardValue`)，支持多种状态：

```cpp
class G1CardTable : public CardTable {
public:
    enum G1CardValues {
        // LSB=1 → 干净; LSB=0 → 脏
        // xxxxxxx1 - clean, already scanned (GC 期间使用)
        // 00000100 - dirty, from remembered set (GC 期间标记)
        // 00000010 - dirty, contains reference to collection set
        // 00000000 - dirty, needs to be scanned
    };
};
```

`g1_to_cset_card` (0x02) 标记包含指向回收集合 (collection set) 引用的卡。
Refinement 线程遇到此标记时会跳过（假设引用不会改变，GC 暂停时会扫描）。
`g1_card_already_scanned` (0x01) 标记已扫描的卡，避免增量疏散时重复扫描。

---

## 3. 并发精炼流程 (Concurrent Refinement Sweep)

### 3.1 G1ConcurrentRefineSweepState -- 精炼状态机

**文件**: `src/hotspot/share/gc/g1/g1ConcurrentRefine.hpp`

精炼过程通过严格的状态机管理，分为 7 个阶段：

```cpp
class G1ConcurrentRefineSweepState {
    enum class State : uint {
        Idle,                  // 空闲 -- 不做任何事
        SwapGlobalCT,          // 交换全局卡表指针
        SwapJavaThreadsCT,     // 交换 Java 线程的卡表指针
        SynchronizeGCThreads,  // 同步 GC 线程的内存视图
        SnapshotHeap,          // 对 Region 的 top() 值做快照
        SweepRT,               // 扫描精炼表上的脏卡
        CompleteRefineWork,    // 完成统计和清理，重置为 Idle
        Last
    } _state;

    G1CardTableClaimTable* _sweep_table;   // 当前堆快照
    G1ConcurrentRefineStats _stats;         // 统计数据
};
```

完整流程：

```
Step 1: SwapGlobalCT
┌──────────────────────────────────────────────────────┐
│ 交换 G1BarrierSet 中的全局卡表指针                    │
│ card_table ←→ refinement_table                       │
│ 此后新创建的线程将使用新的卡表                        │
└──────────────────────────────────────────────────────┘
         │
         ▼
Step 2: SwapJavaThreadsCT
┌──────────────────────────────────────────────────────┐
│ 遍历所有 Java 线程，交换每个线程缓存的卡表指针         │
│ 现有线程逐步切换到新卡表                              │
└──────────────────────────────────────────────────────┘
         │
         ▼
Step 3: SynchronizeGCThreads
┌──────────────────────────────────────────────────────┐
│ 确保内存可见性 -- 所有线程看到一致的卡表状态          │
│ 此后 mutator 不再标记精炼表                          │
└──────────────────────────────────────────────────────┘
         │
         ▼
Step 4: SnapshotHeap
┌──────────────────────────────────────────────────────┐
│ 记录每个 Region 的 top() 值                          │
│ 确定哪些 Region 需要被扫描                           │
│ (此步不可被安全点中断)                                │
└──────────────────────────────────────────────────────┘
         │
         ▼
Step 5: SweepRT
┌──────────────────────────────────────────────────────┐
│ 扫描精炼表中的非 Clean 卡                            │
│ 使用 G1ConcurrentRefineSweepTask (多线程并行)         │
│ 通过 G1CardTableClaimTable 实现区域认领               │
│ (可被安全点中断，GC 时回退到 Idle)                    │
└──────────────────────────────────────────────────────┘
         │
         ▼
Step 6: CompleteRefineWork
┌──────────────────────────────────────────────────────┐
│ 计算统计数据，用于 GC 策略决策                       │
│ 重置状态为 Idle                                      │
│ (可被安全点中断)                                      │
└──────────────────────────────────────────────────────┘
```

除 Step 4 (SnapshotHeap) 外，所有步骤都可以被安全点中断。如果 GC 暂停发生，
状态机自动回退到 Idle。

### 3.2 G1ConcurrentRefine -- 精炼控制器

**文件**: `src/hotspot/share/gc/g1/g1ConcurrentRefine.hpp`

```cpp
class G1ConcurrentRefine : public CHeapObj<mtGC> {
    G1Policy* _policy;
    volatile uint _num_threads_wanted;         // 期望的工作线程数
    size_t _pending_cards_target;              // 目标待处理脏卡数
    bool _heap_was_locked;                     // 上次调整时堆是否被锁定

    G1ConcurrentRefineThreadsNeeded _threads_needed;  // 线程需求计算器
    G1ConcurrentRefineThreadControl _thread_control;  // 线程生命周期管理
    G1ConcurrentRefineSweepState _sweep_state;        // 扫描状态机

    // 特殊标记值：前几个 GC 周期没有目标（数据不足以预测）
    static const size_t PendingCardsTargetUninitialized = SIZE_MAX;
};
```

精炼控制器的核心职责：
1. **确定目标脏卡数**: 根据暂停时间预算 (`G1RSetUpdatingPauseTimePercent`) 计算
   下次 GC 开始时允许的待处理脏卡数量

2. **动态调整线程数**: `adjust_num_threads_periodically()` 周期性调整活跃的
   refinement 工作线程数量，以达到目标脏卡数

3. **管理扫描任务**: 通过 `sweep_state()` 驱动状态机，通过
   `run_with_refinement_workers()` 分配并行扫描任务

### 3.3 G1ConcurrentRefineThreadControl -- 线程管理

```cpp
class G1ConcurrentRefineThreadControl {
    G1ConcurrentRefine* _cr;
    G1ConcurrentRefineThread* _control_thread;  // 控制线程 (单个)
    WorkerThreads* _workers;                    // 工作线程池
    uint _max_num_threads;

    // 通过 -XX:G1ConcRefinementThreads 配置
    // 为 0 时不执行任何并发精炼
};
```

线程架构采用 1 + N 模式：
- 1 个控制线程 (control thread): 周期性唤醒，评估是否需要精炼工作
- N 个工作线程 (worker threads): 实际执行脏卡扫描和 RSet 更新

---

## 4. G1CardTableClaimTable -- 区域认领机制 (Region Claiming)

### 4.1 设计原理

**文件**: `src/hotspot/share/gc/g1/g1CardTableClaimTable.hpp`

并行扫描精炼表时，多个工作线程需要安全地划分工作。`G1CardTableClaimTable`
为每个 Region 维护一个原子计数器，实现无锁的区域认领：

```cpp
class G1CardTableClaimTable : public CHeapObj<mtGC> {
    uint _max_reserved_regions;

    // 每个 Region 的认领进度 (原子计数器)
    // 从 0 (完全未认领) 到 >= CardsPerRegion (完全认领)
    Atomic<uint>* _card_claims;

    uint _cards_per_chunk;  // 每次认领的卡数 (chunk 大小)

    // 认领 increment 张卡，返回之前的认领值
    inline uint claim_cards(uint region, uint increment);

public:
    // 认领整个 Region 的所有卡
    inline uint claim_all_cards(uint region);

    // 认领一个 chunk
    inline uint claim_chunk(uint region);

    // 检查是否还有未认领的卡
    inline bool has_unclaimed_cards(uint region);

    // 按 worker_id 偏移遍历 Region
    void heap_region_iterate_from_worker_offset(
        G1HeapRegionClosure* cl, uint worker_id, uint max_workers);
};
```

认领机制关键点：
- 使用 `Atomic<uint>` 实现原子递增，无需锁
- 每次认领一个 chunk（而非单张卡），减少原子操作次数
- `heap_region_iterate_from_worker_offset` 让不同 worker 从不同偏移开始，减少竞争

### 4.2 G1CardTableChunkClaimer -- Chunk 级别认领

```cpp
class G1CardTableChunkClaimer {
    G1CardTableClaimTable* _claim_values;
    uint _region_idx;
    uint _cur_claim;  // 当前已认领到的位置

public:
    // 尝试认领下一个 chunk，返回是否成功
    inline bool has_next();
    // 当前 chunk 的起始卡索引
    inline uint value() const;
    // chunk 大小
    inline uint size() const;
};
```

### 4.3 G1ChunkScanner -- 脏卡扫描器

```cpp
class G1ChunkScanner {
    using Word = size_t;
    using CardValue = G1CardTable::CardValue;

    CardValue* const _start_card;   // chunk 起始
    CardValue* const _end_card;     // chunk 结束

    // 字级别扫描：一次检查 sizeof(size_t) 张卡
    static const size_t ExpandedToScanMask = G1CardTable::WordAlreadyScanned;
    static const size_t ToScanMask = G1CardTable::g1_card_already_scanned;

    // 查找第一张脏卡 / 第一张非脏卡
    inline CardValue* find_first_dirty_card(CardValue* i_card) const;
    inline CardValue* find_first_non_dirty_card(CardValue* i_card) const;

public:
    // 遍历所有连续脏卡段
    template<typename Func>
    void on_dirty_cards(Func&& f) {
        for (CardValue* cur_card = _start_card; cur_card < _end_card;) {
            CardValue* dirty_l = find_first_dirty_card(cur_card);
            CardValue* dirty_r = find_first_non_dirty_card(dirty_l);
            if (dirty_l == dirty_r) return;
            f(dirty_l, dirty_r);
            cur_card = dirty_r + 1;
        }
    }
};
```

`G1ChunkScanner` 使用字级别 (word-level) 扫描优化：通过将多个 `CardValue`
（1 字节）组合成 `size_t` 大小的字来批量检查，利用位掩码快速定位脏卡段的起止位置。
这大幅减少了逐字节检查的开销。

### 4.4 G1ConcurrentRefineSweepTask -- 并行扫描任务

**文件**: `src/hotspot/share/gc/g1/g1ConcurrentRefineSweepTask.hpp`

```cpp
class G1ConcurrentRefineSweepTask : public WorkerTask {
    G1CardTableClaimTable* _scan_state;   // 区域认领状态
    G1ConcurrentRefineStats* _stats;      // 累计统计
    uint _max_workers;                    // 最大并行度
    bool _sweep_completed;                // 扫描是否完成

public:
    void work(uint worker_id) override;   // 工作线程入口
    bool sweep_completed() const;
};
```

---

## 5. Remembered Set 与卡表精炼 (RSet and Card Refinement)

### 5.1 G1HeapRegionRemSet -- 每 Region 的 Remembered Set

**文件**: `src/hotspot/share/gc/g1/g1HeapRegionRemSet.hpp`

```cpp
class G1HeapRegionRemSet : public CHeapObj<mtGC> {
    G1CodeRootSet _code_roots;                 // 代码根集合
    G1CSetCandidateGroup* _cset_group;         // 回收集合候选组
    G1HeapRegion* _hr;                         // 所属 Region
    static HeapWord* _heap_base_address;       // 堆基地址缓存

    // 卡集合通过 cset_group 间接管理
    G1CardSet* card_set();
};
```

`G1HeapRegionRemSet` 不再直接持有 `G1CardSet`，而是通过 `G1CSetCandidateGroup` 间接访问。
这种设计让相关 Region 可以共享卡集合基础设施。

### 5.2 G1CardSet -- 多层卡集合

**文件**: `src/hotspot/share/gc/g1/g1CardSet.hpp`

`G1CardSet` 使用多层次数据结构存储脏卡索引，根据脏卡数量自动粗化 (coarsen)：

```cpp
class G1CardSetConfiguration {
    uint _inline_ptr_bits_per_card;         // 内联指针中每张卡的位数
    uint _max_cards_in_array;               // Array of Cards 最大卡数
    uint _num_buckets_in_howl;              // Howl 容器的桶数
    uint _max_cards_in_card_set;            // 整个卡集合的最大卡数
    uint _cards_in_howl_threshold;          // 粗化到 Howl 的阈值
    uint _max_cards_in_howl_bitmap;         // Howl 位图最大卡数
    uint _cards_in_howl_bitmap_threshold;   // 粗化到 Howl 位图的阈值
};
```

多层存储粗化路径：

```
Inline Pointer → Array of Cards → Howl (bitmap per bucket) → Full
    (极少卡)      (少量卡)         (中等卡数)                (全部标记)

每层自动晋升到下一层，无需外部控制
```

`G1AddCardResult` 枚举描述添加结果：
- `Added`: 成功添加
- `Found`: 卡已存在
- `Overflow`: 需要粗化并重试

### 5.3 G1RemSet -- 精炼入口

**文件**: `src/hotspot/share/gc/g1/g1RemSet.hpp`

```cpp
class G1RemSet: public CHeapObj<mtGC> {
    G1RemSetScanState* _scan_state;

    // 合并来自各来源的脏卡 (remembered sets, log buffers)
    // 计算后续 scan_heap_roots() 需要扫描的卡
    void merge_heap_roots(bool initial_evacuation);

    // 扫描非回收集合区域中的卡，寻找指向回收集合的引用
    void scan_heap_roots(G1ParScanThreadState* pss,
                         uint worker_id,
                         G1GCPhaseTimes::GCParPhases scan_phase,
                         G1GCPhaseTimes::GCParPhases objcopy_phase,
                         bool remember_already_scanned_cards);
};
```

在 JEP 522 的架构下，`merge_heap_roots` 需要处理精炼表可能非空的情况。
如果精炼表已知非空，G1 在 GC 暂停期间将精炼表合并回 (merge back) 卡表，
然后扫描卡表上的脏卡。

---

## 6. G1HeapRegionManager -- Region 管理 (Region Management)

### 6.1 区域管理器

**文件**: `src/hotspot/share/gc/g1/g1HeapRegionManager.hpp`

```cpp
class G1HeapRegionManager: public CHeapObj<mtGC> {
    G1RegionToSpaceMapper* _bot_mapper;             // Block Offset Table 映射
    G1RegionToSpaceMapper* _card_table_mapper;      // 卡表映射
    G1RegionToSpaceMapper* _refinement_table_mapper; // 精炼表映射 ← JEP 522 新增

    G1CommittedRegionMap _committed_map;   // 已提交 Region 追踪
    G1HeapRegionTable _regions;            // Region 数组 (按地址排序)
    G1FreeRegionList _free_list;           // 空闲 Region 链表
};
```

注意 `_refinement_table_mapper` 字段：这是双卡表架构在 Region 管理器中的体现。
Region 提交 (commit) 和反提交 (uncommit) 时需要同时管理两张卡表的映射。

`initialize()` 方法签名包含 refinement_table 参数：

```cpp
void initialize(G1RegionToSpaceMapper* heap_storage,
                G1RegionToSpaceMapper* bitmap,
                G1RegionToSpaceMapper* bot,
                G1RegionToSpaceMapper* card_table,
                G1RegionToSpaceMapper* refinement_table);  // ← 双卡表
```

### 6.2 G1HeapRegionClaimer -- Region 并行遍历

**文件**: `src/hotspot/share/gc/g1/g1HeapRegionManager.hpp`

```cpp
class G1HeapRegionClaimer : public StackObj {
    uint _n_workers;
    uint _n_regions;
    Atomic<uint>* _claims;     // 每个 Region 一个原子标志

    static const uint Unclaimed = 0;
    static const uint Claimed   = 1;

    // 根据 worker_id 计算起始偏移，分散竞争
    uint offset_for_worker(uint worker_id) const;
    // 原子认领
    bool claim_region(uint region_index);
};
```

`G1HeapRegionClaimer` 用于 GC 暂停期间的并行 Region 遍历，与 `G1CardTableClaimTable`
的并发精炼认领是不同的使用场景（前者在安全点内，后者在安全点外）。

---

## 7. 写屏障优化细节 (Write Barrier Optimization)

### 7.1 简化的写屏障

双卡表架构的核心优势是简化写屏障。源码注释明确指出：

```cpp
// 源码注释原文 (g1BarrierSet.hpp):
// This separation of data the mutator and refinement threads are working on
// removes the need for any fine-grained (per mutator write) synchronization
// between them, keeping the write barrier simple.
```

**优化前** (传统 G1):
```
写屏障伪代码:
1. 计算卡表索引
2. 检查卡是否已脏 (需要读取共享卡表)
3. 如果未脏，标记为脏 (可能需要原子操作或条件存储)
4. 将卡索引加入线程本地 dirty card queue
5. 检查队列是否满 → 可能触发 queue 刷新
```

**优化后** (JEP 522):
```
写屏障伪代码:
1. 计算卡表索引
2. 直接标记卡为脏 (简单存储，无需同步)
   因为只有 mutator 写这张表，refinement 在另一张表上工作
```

不再需要 dirty card queue 的入队操作，因为 refinement 线程直接扫描交换过来的整张卡表。

### 7.2 Collection Set 卡的特殊处理

```cpp
// 源码注释 (g1BarrierSet.hpp):
// The refinement threads mark cards in the current collection set specially
// on the card table - this is fine wrt synchronization with the mutator,
// because at most the mutator will overwrite it again if there is a race,
// as G1 will scan the entire card either way during the GC pause.
```

Refinement 线程在 mutator 的卡表上标记回收集合卡 (`g1_to_cset_card = 0x04`)。
这与 mutator 的写入存在竞争，但是安全的：最坏情况是 mutator 覆盖该标记，
而 GC 暂停时会完整扫描该卡。

### 7.3 GC 暂停期间的卡表合并

```cpp
// 源码注释 (g1BarrierSet.hpp):
// During garbage collection, if the refinement table is known to be non-empty,
// G1 merges it back (and cleaning it) to the card table which is scanned
// for dirty cards.
```

如果 GC 暂停发生时精炼表还有未处理的脏卡，G1 将精炼表合并回卡表。
`G1ConcurrentRefine::sweep_state_for_merge()` 提供合并所需的状态。
`G1RemSet::merge_heap_roots()` 执行实际的合并操作。

---

## 8. G1CollectedHeap 中的同步变化 (Synchronization Changes)

### 8.1 堆锁使用

**文件**: `src/hotspot/share/gc/g1/g1CollectedHeap.hpp`

```cpp
// 堆锁断言宏 (源码)
#define assert_heap_locked()
    assert(Heap_lock->owned_by_self(),
           "should be holding the Heap_lock");

#define assert_heap_locked_or_at_safepoint(_should_be_vm_thread_)
    assert(Heap_lock->owned_by_self() ||
           (SafepointSynchronize::is_at_safepoint() && ...),
           "should be holding the Heap_lock or at safepoint");
```

JEP 522 减少了 Heap_lock 的持有时间。`G1ConcurrentRefine` 中的
`_heap_was_locked` 字段追踪上次调整时堆是否被锁定，如果锁竞争激烈，
调整操作会被延迟 (deferred) 而非阻塞。

### 8.2 区域状态追踪

`G1CommittedRegionMap` 追踪 Region 的提交状态（活跃/不活跃），
通过文档注释中提到的锁协议 (`guarantee_mt_safety_*`) 确保多线程安全：

```cpp
// 源码注释 (g1HeapRegionManager.hpp):
// G1RegionCommittedMap helpers. These functions do the work that comes with
// the state changes tracked by G1CommittedRegionMap. To make sure this is
// safe from a multi-threading point of view there are two lock protocols in
// G1RegionCommittedMap::guarantee_mt_safety_* that are enforced.
```

---

## 9. 具体优化效果分析 (Performance Impact Analysis)

### 9.1 消除的同步操作

| 操作 | 优化前 | 优化后 |
|------|--------|--------|
| 卡表标记 | 条件检查 + 可能的原子操作 | 简单字节存储 |
| Dirty card queue 入队 | 线程本地缓冲区 → 全局队列 | 不需要（直接扫描卡表） |
| Refinement 处理 | 从队列取出 → 处理 → 清除 | 直接扫描精炼表 |
| 卡表状态检查 | 共享读取（与 refinement 竞争） | 独占读取（无竞争） |
| GC 暂停合并 | 从多个队列合并 | 最多合并一张精炼表 |

### 9.2 新增的开销

| 开销 | 频率 | 影响 |
|------|------|------|
| 卡表交换 (SwapGlobalCT) | 每次精炼周期 | 指针原子交换，微秒级 |
| 线程卡表更新 (SwapJavaThreadsCT) | 每次精炼周期 | 遍历所有 Java 线程 |
| GC 线程同步 (SynchronizeGCThreads) | 每次精炼周期 | 内存屏障 |
| 双倍卡表内存 | 持续 | 额外一张卡表（堆大小/512 字节） |

对于 32GB 堆，额外内存 = 32GB / 512 = 64MB，是可接受的开销。

### 9.3 吞吐量提升场景

双卡表架构的收益主要来自：

1. **高写入率场景**: 写屏障开销的绝对降低。每次引用写入节省的条件分支和
   可能的原子操作，在高频写入时累积效果显著。

2. **高并发场景**: 消除 mutator 与 refinement 线程之间的竞争。
   线程数越多，竞争越严重，优化效果越明显。

3. **大堆场景**: 脏卡数量多，refinement 工作量大，消除细粒度同步
   对 refinement 线程吞吐量提升明显。

---

## 10. 配置选项 (Configuration Options)

### 10.1 现有参数

```bash
# G1 并发精炼线程数（0 表示不做并发精炼）
-XX:G1ConcRefinementThreads=<N>

# RSet 更新在 GC 暂停中的时间预算百分比
-XX:G1RSetUpdatingPauseTimePercent=<N>

# Region 大小
-XX:G1HeapRegionSize=<size>

# 最大 GC 暂停目标
-XX:MaxGCPauseMillis=<ms>
```

### 10.2 端点配置

```bash
# QUIC 端点数（非 G1 参数，仅列出以避免混淆）
# 双卡表架构的端点配置通过内部 JDK 属性控制
```

JEP 522 的优化默认启用，无需额外 JVM 参数。双卡表架构是 G1 GC 实现细节的
内部变更，不影响用户可见的 API 或配置。

---

## 11. 与其他 GC 的写屏障对比 (Write Barrier Comparison)

| GC | 写屏障类型 | 精炼方式 | mutator 同步开销 |
|----|-----------|----------|-----------------|
| Serial | 简单卡表标记 | GC 暂停时处理 | 无 (单线程) |
| Parallel | 简单卡表标记 | GC 暂停时处理 | 无 (仅 STW 时扫描) |
| G1 (传统) | 卡表标记 + SATB + dirty card queue | 并发 refinement | 每次写入有条件检查和可能的原子操作 |
| **G1 (JEP 522)** | **卡表标记 + SATB (双卡表)** | **并发 sweep** | **简单存储，无同步** |
| ZGC | 染色指针 (colored pointer) | 并发处理 | 染色指针读取时检查 |
| Shenandoah | 加载引用屏障 (load-reference barrier) | 并发处理 | 每次加载时检查 |

JEP 522 使 G1 的写屏障开销接近 Serial/Parallel GC 的水平，同时保留了 G1 的
并发精炼能力和 Region 化内存管理。

---

## 12. 相关源码文件索引 (Source File Index)

```
src/hotspot/share/gc/g1/
├── g1BarrierSet.hpp / .cpp / .inline.hpp       # 双卡表写屏障管理
├── g1CardTable.hpp / .cpp / .inline.hpp        # 卡表定义 (卡值、状态)
├── g1CardTableClaimTable.hpp / .inline.hpp     # 区域认领机制 (Chunk Claimer + Scanner)
├── g1ConcurrentRefine.hpp / .cpp              # 精炼控制器 + 状态机
├── g1ConcurrentRefineThread.hpp / .cpp        # 精炼线程
├── g1ConcurrentRefineStats.hpp / .inline.hpp  # 精炼统计
├── g1ConcurrentRefineSweepTask.hpp / .cpp     # 并行扫描任务
├── g1ConcurrentRefineThreadsNeeded.hpp        # 线程需求计算
├── g1RemSet.hpp / .cpp                        # Remembered Set 管理 (merge + scan)
├── g1HeapRegionRemSet.hpp / .cpp              # 每 Region RSet
├── g1CardSet.hpp / .cpp / .inline.hpp         # 多层卡集合 (inline → array → howl)
├── g1CardSetContainers.hpp / .inline.hpp      # 卡集合容器
├── g1CardSetMemory.hpp / .inline.hpp          # 卡集合内存管理
├── g1HeapRegionManager.hpp / .inline.hpp      # Region 管理 (含 refinement_table)
├── g1HeapRegionSet.hpp / .inline.hpp          # Region 集合 (FreeRegionList 等)
├── g1CommittedRegionMap.hpp / .inline.hpp     # 已提交 Region 追踪
├── g1CollectedHeap.hpp / .cpp / .inline.hpp   # G1 堆 (Heap_lock 相关)
├── g1FromCardCache.hpp                         # From Card Cache (避免重复精炼)
├── g1HeapRegion.hpp / .cpp / .inline.hpp      # Region 定义 (CardsPerRegion 等)
├── g1Policy.hpp / .cpp                        # GC 策略 (暂停目标、Region 选择)
├── g1Analytics.hpp / .cpp                     # GC 分析 (预测模型)
└── g1MonitoringSupport.hpp / .cpp             # 监控支持

src/hotspot/cpu/*/gc/g1/
├── g1BarrierSetAssembler_*.hpp / .cpp         # 平台相关写屏障汇编
└── (各架构: x86, aarch64, riscv, ppc, s390)
```

---

## 13. 总结 (Summary)

JEP 522 通过双卡表架构从根本上重新设计了 G1 GC 的写屏障和并发精炼机制：

### 核心变更

1. **双卡表 (Dual Card Table)**: `G1BarrierSet` 管理两张独立的 `G1CardTable`，
   mutator 和 refinement 线程各使用一张，消除细粒度同步

2. **状态机驱动的精炼 (State Machine Sweep)**: `G1ConcurrentRefineSweepState`
   定义 7 阶段精炼流程，支持安全点中断和 GC 打断后的优雅回退

3. **区域认领 (Chunk Claiming)**: `G1CardTableClaimTable` + `G1ChunkScanner`
   实现无锁的并行扫描，字级别批量脏卡检测

4. **Region 管理集成**: `G1HeapRegionManager` 新增 `_refinement_table_mapper`
   字段，统一管理双卡表的提交/反提交

### 关键收益

- 写屏障简化为简单字节存储（无条件分支、无原子操作、无队列入队）
- 消除 mutator 与 refinement 线程之间的所有每次写入同步
- 额外内存开销仅为堆大小 / 512 字节

### 设计原则

- 保持 G1 GC 现有语义和行为不变
- 不引入新的用户可见参数
- 兼容所有 CPU 架构（x86、aarch64、riscv、ppc、s390）
- 最大化利用并行性（区域认领 + 字级别扫描）
