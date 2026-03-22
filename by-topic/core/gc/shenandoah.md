# Shenandoah GC 详解

> 低延迟并发垃圾收集器 (Low-Pause Concurrent GC)，最初由 Red Hat 贡献，Amazon 参与分代扩展

[← 返回 GC](../)

---
## 目录

1. [架构概览](#1-架构概览)
2. [Region 与堆布局](#2-region-与堆布局)
3. [转发指针 (Forwarding Pointer)](#3-转发指针-forwarding-pointer)
4. [屏障 (Barriers)](#4-屏障-barriers)
5. [GC 周期详解](#5-gc-周期详解)
6. [GC 模式 (Modes)](#6-gc-模式-modes)
7. [启发式 (Heuristics)](#7-启发式-heuristics)
8. [分代 Shenandoah (Generational)](#8-分代-shenandoah-generational)
9. [退化与完全 GC (Degenerated / Full GC)](#9-退化与完全-gc-degenerated--full-gc)
10. [GC 状态机 (GC State)](#10-gc-状态机-gc-state)
11. [关键调优参数](#11-关键调优参数)
12. [诊断与监控](#12-诊断与监控)
13. [JEP 演进](#13-jep-演进)
14. [vs G1 vs ZGC 对比](#14-vs-g1-vs-zgc-对比)
15. [源码导航](#15-源码导航)

---

## 1. 架构概览

### 核心定位

Shenandoah 是一个 **region-based、并发回收 (concurrent evacuation)** 的低延迟 GC。其核心类是 `ShenandoahHeap`，继承自 `CollectedHeap`：

```
源码: src/hotspot/share/gc/shenandoah/shenandoahHeap.hpp

// Shenandoah GC is low-pause concurrent GC that uses a load reference barrier
// for concurrent evacuation and a snapshot-at-the-beginning write barrier for
// concurrent marking. See ShenandoahControlThread for GC cycle structure.
class ShenandoahHeap : public CollectedHeap { ... }
```

### 与 G1 的核心区别

| 维度 | G1 GC | Shenandoah GC |
|------|-------|---------------|
| 回收 (Evacuation) | **STW** 期间复制存活对象 | **并发** 复制存活对象 |
| 暂停正比于 | 回收集合 (CSet) 大小 | GC root 数量 (与堆大小无关) |
| 引用更新 | STW 期间完成 | 并发阶段完成 |
| 读屏障 | 无 | Load Reference Barrier (LRB) |
| 写屏障 | 记忆集写屏障 | SATB 写屏障 (+ 分代模式下 card barrier) |
| 转发指针 | 在原对象内存中 | 存储在 mark word 内 |

### 设计哲学

```
G1 思路:           Shenandoah 思路:

  Mark ──► Evac     Mark ──────────────► Evac ──────────────► Update Refs
  (并发)   (STW)    (大部分并发)          (并发!)              (并发!)
                    ↑                    ↑                    ↑
                    极短 STW init/final   极短 STW init/final   极短 STW init/final
```

Shenandoah 的设计目标：**GC 暂停时间与堆大小无关**。不论堆是 200MB 还是 200GB，暂停时间都应在毫秒级。

---

## 2. Region 与堆布局

### Region 状态机

Shenandoah 将整个 Java 堆划分为固定大小的 Region。Region 状态由 `ShenandoahHeapRegion` 的内部枚举定义：

```
源码: src/hotspot/share/gc/shenandoah/shenandoahHeapRegion.hpp

enum RegionState {
    _empty_uncommitted,       // 空闲且内存未提交
    _empty_committed,         // 空闲且内存已提交
    _regular,                 // 用于常规分配
    _humongous_start,         // 巨型对象的起始 region
    _humongous_cont,          // 巨型对象的后续 region
    _pinned_humongous_start,  // 巨型起始 + 被 pin 住
    _cset,                    // 在回收集合 (collection set) 中
    _pinned,                  // 被 pin 住 (如 JNI critical)
    _pinned_cset,             // 在 CSet 中但被 pin (回收失败路径)
    _trash,                   // 仅包含垃圾，等待回收
};
```

完整状态转换图 (来自源码注释):

```
"Empty":
................................................................
.                                                               .
.         Uncommitted  <-------  Committed <-----------------------\
.              |                     |                          .   |
.              \---------v-----------/                          .   |
.                        |                                      .   |
.........................|.......................................   |
                         |                                          |
"Active":                |                                          |
.........................|.......................................   |
.                        |                                      .   |
.      /-----------------^-------------------\                  .   |
.      |                                     |                  .   |
.      v                                     v   "Humongous":   .   |
.   Regular ---\-----\     ..................O...............   .   |
.     |  ^     |     |     .                 |              .   .   |
.     |  |     |     |     .                 *--------\     .   .   |
.     v  |     |     |     .                 v        v     .   .   |
.    Pinned  Cset    |     .  HStart <--> H/Start  H/Cont  .   .   |
.       ^    / |     |     .  Pinned        v        |      .   .   |
.       |   /  |     |     .                *<-------/      .   .   |
.       |  v   |     |     .                |               .   .   |
.  CsetPinned  |     |     ..................O...............   .   |
.              |     |                       |                  .   |
.              \-----\---v-------------------/                  .   |
.                        |                                      .   |
.........................|.......................................   |
                         |                                          |
"Trash":                 |                                          |
.........................|.......................................   |
.                        v                                      .   |
.                      Trash ----------------------------------------/
.                                                               .
.................................................................
```

### Region 大小计算

Region 大小在 `ShenandoahHeapRegion::setup_sizes()` 中计算:

```
源码: src/hotspot/share/gc/shenandoah/shenandoahHeapRegion.cpp

计算逻辑:
1. 如果用户设置了 ShenandoahRegionSize, 直接使用
2. 否则: region_size = max_heap_size / ShenandoahTargetNumRegions (默认 2048)
3. 约束: MAX(ShenandoahMinRegionSize, region_size)   // 默认 256KB
         MIN(ShenandoahMaxRegionSize, region_size)   // 默认 32MB
4. 对齐到页大小, 然后向下取到 2 的幂
```

| 参数 | 默认值 | 含义 |
|------|--------|------|
| `ShenandoahRegionSize` | 0 (自动) | 手动指定 Region 大小 |
| `ShenandoahTargetNumRegions` | 2048 | 目标 Region 数量 |
| `ShenandoahMinRegionSize` | 256KB | 最小 Region 大小 |
| `ShenandoahMaxRegionSize` | 32MB | 最大 Region 大小 |
| `MIN_NUM_REGIONS` | 10 | 最少 Region 数量 (硬编码常量) |

### 巨型对象 (Humongous)

对象大于一个 Region 时被视为巨型对象 (humongous):

```
源码: shenandoahHeapRegion.hpp

inline static bool requires_humongous(size_t words) {
    return words > ShenandoahHeapRegion::RegionSizeWords;
}
```

注意与 G1 不同: G1 的阈值是 region_size / 2，Shenandoah 的阈值是整个 region size。巨型对象跨越 `_humongous_start` + N 个 `_humongous_cont` region。

### 分代模式下的 Region 所属关系 (Affiliation)

在分代模式下，每个 Region 有一个 affiliation 属性:

```
源码: src/hotspot/share/gc/shenandoah/shenandoahAffiliation.hpp

enum ShenandoahAffiliation {
    FREE,              // 空闲
    YOUNG_GENERATION,  // 年轻代
    OLD_GENERATION,    // 老年代
};
```

Region 还具有 age 属性 (`_age` 字段)，用于决定晋升 (promotion)。通过 `increment_age()` 在每个 GC 周期递增，上限为 `markWord::max_age` (15)。

---

## 3. 转发指针 (Forwarding Pointer)

### 历史演进

| 版本 | 方案 | 开销 |
|------|------|------|
| JDK 12-13 | Brooks pointer: 对象头前增加一个额外指针字 | 每对象 +8 字节 |
| JDK 14+ (JEP 325) | 将转发地址编码在 mark word 中 | 零额外空间开销 |

### 当前实现: mark word 中的转发

`ShenandoahForwarding` 类提供了转发指针的所有操作:

```cpp
// 源码: src/hotspot/share/gc/shenandoah/shenandoahForwarding.hpp

class ShenandoahForwarding {
public:
    static inline oop get_forwardee(oop obj);           // 获取转发目标
    static inline oop get_forwardee_mutator(oop obj);   // 仅 mutator 线程使用
    static inline oop get_forwardee_raw(oop obj);       // 原始值
    static inline bool is_forwarded(oop obj);           // 是否已转发
    static inline oop try_update_forwardee(oop obj, oop update);  // CAS 安装转发指针
};
```

核心实现在 `shenandoahForwarding.inline.hpp`:

```cpp
inline oop ShenandoahForwarding::get_forwardee_raw_unchecked(oop obj) {
    // JVMTI 和 JFR 也使用 mark word 做标记, 可能遇到 "marked" 对象但 fwdptr 为 null
    // 此时对象未被转发, 返回对象本身
    markWord mark = obj->mark();
    if (mark.is_marked()) {
        HeapWord* fwdptr = (HeapWord*) mark.clear_lock_bits().to_pointer();
        if (fwdptr != nullptr) {
            return cast_to_oop(fwdptr);
        }
    }
    return obj;
}

inline bool ShenandoahForwarding::is_forwarded(oop obj) {
    return obj->mark().is_marked();
}
```

**关键设计**: 利用 mark word 的 lock bits (`is_marked()`) 来表示"该对象已被转发"。`clear_lock_bits()` 后的地址就是新对象地址。

### CAS 安装转发指针

```cpp
inline oop ShenandoahForwarding::try_update_forwardee(oop obj, oop update) {
    markWord old_mark = obj->mark();
    if (old_mark.is_marked()) {
        // 其他线程已经安装了转发指针, 返回已有的 forwardee
        return cast_to_oop(...);
    }
    markWord new_mark = markWord::encode_pointer_as_mark(update);
    markWord prev_mark = obj->cas_set_mark(new_mark, old_mark);
    if (prev_mark == old_mark) {
        return update;   // CAS 成功, 本线程赢得竞争
    } else {
        return cast_to_oop(...);  // CAS 失败, 返回竞争对手安装的地址
    }
}
```

这保证了在并发回收期间，当多个线程同时尝试复制同一对象时，只有一个线程的副本会被采用。

---

## 4. 屏障 (Barriers)

### 屏障体系总览

`ShenandoahBarrierSet` 继承自 `BarrierSet`，在 HotSpot 的统一屏障框架下工作:

```
源码: src/hotspot/share/gc/shenandoah/shenandoahBarrierSet.hpp

class ShenandoahBarrierSet: public BarrierSet {
private:
    ShenandoahHeap* const _heap;
    ShenandoahCardTable* _card_table;                      // 分代模式使用
    ShenandoahSATBMarkQueueSet _satb_mark_queue_set;       // SATB 标记队列
public:
    // 核心屏障判断
    static bool need_load_reference_barrier(DecoratorSet decorators, BasicType type);
    static bool need_keep_alive_barrier(DecoratorSet decorators, BasicType type);
    static bool need_satb_barrier(DecoratorSet decorators, BasicType type);
    static bool need_card_barrier(DecoratorSet decorators, BasicType type);

    // Load Reference Barrier (LRB)
    inline oop load_reference_barrier(oop obj);
    template <class T>
    inline oop load_reference_barrier_mutator(oop obj, T* load_addr);

    // SATB 写屏障
    template <DecoratorSet decorators, typename T>
    inline void satb_barrier(T* field);
    inline void satb_enqueue(oop value);
};
```

### 4.1 Load Reference Barrier (LRB) - 加载引用屏障

LRB 是 Shenandoah 并发回收的核心机制。每次从堆中加载一个对象引用时，都经过 LRB:

```cpp
// 源码: shenandoahBarrierSet.inline.hpp

inline oop ShenandoahBarrierSet::load_reference_barrier(oop obj) {
    if (!ShenandoahLoadRefBarrier) {
        return obj;
    }
    if (_heap->has_forwarded_objects() && _heap->in_collection_set(obj)) {
        // obj 在回收集合中 → 需要处理
        oop fwd = resolve_forwarded_not_null(obj);
        if (obj == fwd && _heap->is_evacuation_in_progress()) {
            // 尚未转发, 且当前正在回收阶段 → 就地回收!
            Thread* t = Thread::current();
            ShenandoahEvacOOMScope oom_evac_scope(t);
            return _heap->evacuate_object(obj, t);
        }
        return fwd;
    }
    return obj;
}
```

**Mutator 版本** (更优化的快速路径):

```cpp
template <class T>
inline oop ShenandoahBarrierSet::load_reference_barrier_mutator(oop obj, T* load_addr) {
    oop fwd = resolve_forwarded_not_null_mutator(obj);
    if (obj == fwd) {
        // 对象尚未转发, 由 mutator 线程执行回收
        ShenandoahEvacOOMScope scope(t);
        fwd = _heap->evacuate_object(obj, t);
    }
    if (load_addr != nullptr && fwd != obj) {
        // 自愈 (self-healing): 更新引用位置, 下次直接拿到新地址
        ShenandoahHeap::atomic_update_oop(fwd, load_addr, obj);
    }
    return fwd;
}
```

**关键点**: LRB 不仅仅是读屏障 -- 当 mutator 线程发现引用指向 CSet 中的对象时, 它会**参与回收**:
1. 检查对象是否已转发
2. 如未转发, 当前线程复制对象到新 Region 并 CAS 安装转发指针
3. 更新引用源 (self-healing), 避免下次再触发屏障

### 4.2 SATB 写屏障

用于并发标记期间维护 Snapshot-At-The-Beginning (SATB) 不变量:

```cpp
template <DecoratorSet decorators, typename T>
inline void ShenandoahBarrierSet::satb_barrier(T* field) {
    // 在覆写一个引用字段之前, 将旧值入队到 SATB buffer
    T heap_oop = RawAccess<>::oop_load(field);
    if (!CompressedOops::is_null(heap_oop)) {
        oop prev_obj = CompressedOops::decode_not_null(heap_oop);
        satb_enqueue(prev_obj);
    }
}
```

### 4.3 Card Barrier (分代模式专用)

分代模式下增加了 card table barrier, 用于跟踪老年代到年轻代的引用:

```
源码: shenandoahBarrierSet.hpp

ShenandoahCardTable* _card_table;  // 仅当 ShenandoahCardBarrier=true 时启用

// 写入引用后标记 card
template <DecoratorSet decorators, typename T>
void write_ref_field_post(T* field);
```

### 4.4 引用强度分类

屏障根据引用强度区分处理:

```cpp
static bool is_strong_access(DecoratorSet decorators) {
    return (decorators & (ON_WEAK_OOP_REF | ON_PHANTOM_OOP_REF)) == 0;
}
static bool is_weak_access(DecoratorSet decorators) {
    return (decorators & ON_WEAK_OOP_REF) != 0;
}
static bool is_phantom_access(DecoratorSet decorators) {
    return (decorators & ON_PHANTOM_OOP_REF) != 0;
}
```

### 4.5 屏障开关标志

所有屏障都可通过 diagnostic 标志独立控制:

| 标志 | 默认 | 作用 |
|------|------|------|
| `ShenandoahLoadRefBarrier` | true | Load Reference Barrier |
| `ShenandoahSATBBarrier` | true | SATB 写屏障 |
| `ShenandoahCASBarrier` | true | CAS 操作屏障 |
| `ShenandoahCloneBarrier` | true | Object.clone() 屏障 |
| `ShenandoahStackWatermarkBarrier` | true | 栈水印屏障 |
| `ShenandoahCardBarrier` | false | Card barrier (分代模式自动开启) |

---

## 5. GC 周期详解

### 并发 GC 周期 (ShenandoahConcurrentGC)

完整周期由 `ShenandoahConcurrentGC::collect()` 编排 (源码位于 `shenandoahConcurrentGC.cpp`):

```
Phase 1: Reset (并发)                    entry_reset()
    └── 重置数据结构, 准备下一轮标记

Phase 2: Init Mark (STW, 极短)            vmop_entry_init_mark()
    └── 扫描 GC root, 设置 MARKING 状态位

Phase 3: Concurrent Mark (并发)
    ├── entry_scan_remembered_set()        扫描记忆集 (分代模式)
    ├── entry_mark_roots()                 并发扫描根
    └── entry_mark()                       并发标记遍历

Phase 4: Final Mark (STW, 极短)            vmop_entry_final_mark()
    ├── 完成标记 (drain satb buffers)
    ├── 选择回收集合 (collection set)
    └── 准备回收: 设置 EVACUATION 状态位

Phase 5: Concurrent Weak Processing (并发)
    ├── entry_thread_roots()               并发处理线程栈根
    ├── entry_weak_refs()                  处理弱引用
    ├── entry_weak_roots()                 处理弱根
    └── entry_class_unloading()            并发卸载类 (可选)

Phase 6: Cleanup Early (并发)              entry_cleanup_early()
    └── 回收仅含垃圾的 region (immediate garbage)

Phase 7: Concurrent Strong Roots (并发)    entry_strong_roots()
    └── 更新/回收强根中的引用

Phase 8: Concurrent Evacuation (并发!)     entry_evacuate()
    └── 将 CSet 中的存活对象复制到新 Region
        (mutator 通过 LRB 参与回收)

Phase 9: Concurrent Update References (并发)
    ├── entry_concurrent_update_refs_prepare()  准备: retire TLAB/GCLAB
    ├── entry_update_refs()                     扫描整个堆更新旧引用
    └── entry_update_thread_roots()             更新线程栈中的引用

Phase 10: Final Update Refs (STW, 极短)    vmop_entry_final_update_refs()
    └── 更新 region 状态, 完成引用更新

Phase 11: Cleanup Complete (并发)          entry_cleanup_complete()
    └── 回收已清空的 CSet region

Phase 12: Reset After Collect (并发)       entry_reset_after_collect()
    └── 预先重置, 加快下一次触发响应
```

### 简化 (Abbreviated) 周期

当 Final Mark 发现有足够的 immediate garbage (无需回收), 可跳过 evacuation/update refs:

```cpp
// 源码: shenandoahConcurrentGC.cpp

if (heap->is_evacuation_in_progress()) {
    entry_evacuate();          // 正常路径
    ...
} else {
    _abbreviated = true;       // 简化周期: 跳过回收和引用更新
    entry_final_roots();
}
```

### STW 与并发阶段分布

```
时间线:

  STW ■         ■                                      ■
      Init      Final                                  Final
      Mark      Mark                                   Update Refs
  ────┼──────────┼──────────────────────────────────────┼──────────────
  并发│← Mark  →│← Evac → ← Update Refs →             │← Cleanup →
      │          │                                      │

  典型 STW 时长: < 1ms (仅扫描 root set)
```

---

## 6. GC 模式 (Modes)

### 模式类层次

```
源码: src/hotspot/share/gc/shenandoah/mode/

ShenandoahMode (抽象基类)
├── ShenandoahSATBMode           "satb"          默认, 非分代
├── ShenandoahGenerationalMode   "generational"  分代模式
└── ShenandoahPassiveMode        "passive"       诊断/测试用
```

模式由 `-XX:ShenandoahGCMode` 选择:

```cpp
// 源码: shenandoahHeap.cpp

void ShenandoahHeap::initialize_mode() {
    if (strcmp(ShenandoahGCMode, "satb") == 0) {
        _gc_mode = new ShenandoahSATBMode();
    } else if (strcmp(ShenandoahGCMode, "passive") == 0) {
        _gc_mode = new ShenandoahPassiveMode();
    } else if (strcmp(ShenandoahGCMode, "generational") == 0) {
        _gc_mode = new ShenandoahGenerationalMode();
    }
}
```

### 6.1 SATB 模式 (默认)

```
源码: mode/shenandoahSATBMode.hpp

class ShenandoahSATBMode : public ShenandoahMode {
    const char* name()     { return "Snapshot-At-The-Beginning (SATB)"; }
    bool is_diagnostic()   { return false; }
    bool is_experimental() { return false; }
};
```

- 使用 SATB 写屏障 + LRB 读屏障
- 全堆统一收集 (non-generational): `ShenandoahGenerationType::NON_GEN`
- 启发式默认: `adaptive`

### 6.2 Generational 模式

```
源码: mode/shenandoahGenerationalMode.hpp

class ShenandoahGenerationalMode : public ShenandoahMode {
    const char* name()     { return "Generational"; }
    bool is_diagnostic()   { return false; }
    bool is_experimental() { return false; }
    bool is_generational() { return true; }
};
```

- 增加 card table barrier 追踪跨代引用
- 支持 Young / Old / Global 三种收集类型
- 使用 `ShenandoahGenerationalHeap` (继承 `ShenandoahHeap`)

### 6.3 Passive 模式 (诊断用)

```
源码: mode/shenandoahPassiveMode.hpp

class ShenandoahPassiveMode : public ShenandoahMode {
    const char* name()     { return "Passive"; }
    bool is_diagnostic()   { return true; }   // 需要 -XX:+UnlockDiagnosticVMOptions
    bool is_experimental() { return false; }
};
```

- 不执行并发 GC, 完全依赖 Degenerated GC 或 Full GC
- 用于测试和基准对比: 测量"没有并发 GC 时的表现"

---

## 7. 启发式 (Heuristics)

### 启发式类层次

```
源码: src/hotspot/share/gc/shenandoah/heuristics/

ShenandoahHeuristics (基类)
├── ShenandoahAdaptiveHeuristics        "adaptive"     默认
│   └── ShenandoahGenerationalHeuristics (分代扩展)
│       ├── ShenandoahGlobalHeuristics   全局收集启发式
│       └── ShenandoahYoungHeuristics    年轻代收集启发式
├── ShenandoahStaticHeuristics          "static"
├── ShenandoahCompactHeuristics         "compact"
├── ShenandoahAggressiveHeuristics      "aggressive"   诊断用
├── ShenandoahPassiveHeuristics         被动模式专用
└── ShenandoahOldHeuristics             老年代收集启发式
```

由 `-XX:ShenandoahGCHeuristics` 选择, 默认 `adaptive`。分代模式下固定使用 `adaptive`。

### 7.1 基类核心职责

```cpp
// 源码: heuristics/shenandoahHeuristics.hpp

class ShenandoahHeuristics : public CHeapObj<mtGC> {
    // 惩罚机制: 退化/Full GC 导致更积极的触发
    static const intx Degenerated_Penalty = 10;
    static const intx Full_Penalty        = 20;

    // 核心接口
    virtual bool should_start_gc();                            // 是否触发 GC
    virtual void choose_collection_set(ShenandoahCollectionSet*); // 选择回收集合
    virtual bool should_degenerate_cycle();                    // 是否退化

    // 记录 GC 结果, 用于自适应调整
    virtual void record_success_concurrent();
    virtual void record_degenerated();
    virtual void record_success_full();
};
```

### 7.2 Adaptive Heuristics (自适应)

最核心的启发式, 跟踪分配速率和 GC 周期时间:

```
源码: heuristics/shenandoahAdaptiveHeuristics.hpp

核心组件:
- ShenandoahAllocationRate: 维护分配速率采样历史 (TruncatedSeq)
- _margin_of_error_sd: 误差边界 (标准差倍数), 越大越保守
- _spike_threshold_sd: 分配尖峰检测阈值, 越小越敏感
- _headroom_adjustment: 触发 GC 的剩余空间阈值
```

**触发逻辑** (`should_start_gc()`):
1. **保证间隔 (guaranteed interval)**: 如果距上次 GC 超过 `ShenandoahGuaranteedGCInterval` (默认 5 分钟), 强制触发
2. **分配速率预测**: 基于分配速率 + 预测 GC 耗时, 估算"现在不触发会不会来不及"
3. **尖峰检测**: 如果分配速率突然飙升, 提前触发
4. **加速度检测**: 跟踪分配速率的二阶导 (加速度), 预测未来的分配压力

**回收集合选择** (`choose_collection_set_from_regiondata()`):
- 按垃圾量降序排序所有 Region
- 跳过垃圾占比低于 `ShenandoahGarbageThreshold` (默认 25%) 的 Region
- 选择 Region 直到回收预留空间 (evacuation reserve) 用尽

**自适应调整**:
- 并发 GC 成功 → 降低 `_margin_of_error_sd` (少触发), 提高 `_spike_threshold_sd` (不敏感)
- 退化 GC → 提高 `_margin_of_error_sd` (早触发), 降低 `_spike_threshold_sd` (更敏感)
- Full GC → 大幅提高 `_margin_of_error_sd`

### 7.3 Static Heuristics (静态)

在可用空间低于 `ShenandoahMinFreeThreshold` 或分配达到 `ShenandoahAllocationThreshold` 时触发。不做自适应调整。

### 7.4 Compact Heuristics (紧凑)

类似 Static, 但回收集合选择所有垃圾 > 0 的 region, 目标是最大化空间回收。

### 7.5 Aggressive Heuristics (激进)

诊断用, 每次都触发 GC, 每次都选择所有 region 进入 CSet。用于压力测试。

---

## 8. 分代 Shenandoah (Generational)

### 8.1 架构

分代模式使用 `ShenandoahGenerationalHeap` (继承 `ShenandoahHeap`):

```
源码: src/hotspot/share/gc/shenandoah/shenandoahGenerationalHeap.hpp

class ShenandoahGenerationalHeap : public ShenandoahHeap {
    ShenandoahSharedFlag  _is_aging_cycle;
    ShenandoahAgeCensus* _age_census;
    ShenandoahRegulatorThread* _regulator_thread;
    ...
};
```

### 8.2 代类型

```
源码: shenandoahGenerationType.hpp

enum ShenandoahGenerationType {
    NON_GEN,   // 非分代 (SATB 模式)
    GLOBAL,    // 全局收集 (分代模式下收集全堆)
    YOUNG,     // 年轻代收集
    OLD        // 老年代收集
};
```

代的抽象基类:

```
源码: shenandoahGeneration.hpp

class ShenandoahGeneration : public CHeapObj<mtGC>, public ShenandoahSpaceInfo {
    ShenandoahGenerationType const _type;
    ShenandoahObjToScanQueueSet* _task_queues;
    ShenandoahReferenceProcessor* const _ref_processor;
    size_t _evacuation_reserve;      // 回收预留空间
    ShenandoahFreeSet* _free_set;
    ShenandoahHeuristics* _heuristics;

    inline bool is_young() const { return _type == YOUNG; }
    inline bool is_old()   const { return _type == OLD; }
    inline bool is_global() const { return _type == GLOBAL || _type == NON_GEN; }
};
```

具体实现:

```
ShenandoahGeneration
├── ShenandoahYoungGeneration  (shenandoahYoungGeneration.hpp)
└── ShenandoahOldGeneration    (shenandoahOldGeneration.hpp)
```

### 8.3 分代收集类型

| 收集类型 | 触发条件 | 收集范围 |
|----------|----------|----------|
| Young GC | 年轻代空间不足 | 仅年轻代 Region |
| Mixed GC | 老年代标记完成后 | 年轻代 + 部分老年代 |
| Global GC | 极端情况 | 全堆 |
| Old GC | 老年代增长超阈值 | 并发老年代标记 |

### 8.4 对象晋升 (Promotion)

分代模式引入了对象年龄跟踪和晋升机制:

```
源码: shenandoahGenerationalHeap.hpp

inline bool is_tenurable(const ShenandoahHeapRegion* r) const;

// 回收时根据 FROM/TO 代决定行为
template<ShenandoahAffiliation FROM_REGION, ShenandoahAffiliation TO_REGION>
oop try_evacuate_object(oop p, Thread* thread, uint from_region_age);

// 整区就地晋升 (promote in place): 将整个年轻代 Region 重标记为老年代
void promote_regions_in_place(ShenandoahGeneration* generation, bool concurrent);
```

晋升参数:

| 参数 | 默认 | 含义 |
|------|------|------|
| `ShenandoahGenerationalAdaptiveTenuring` | true | 自适应调整晋升年龄 |
| `ShenandoahGenerationalMinTenuringAge` | 1 | 最小晋升年龄 |
| `ShenandoahGenerationalMaxTenuringAge` | 15 | 最大晋升年龄 |
| `ShenandoahAgingCyclePeriod` | 1 | 每隔几个 GC 周期增长 age |

### 8.5 Card Table 和 Remembered Set

分代模式通过 card table 追踪老年代→年轻代的引用:

```
源码: shenandoahCardTable.hpp / shenandoahBarrierSet.hpp

// ShenandoahCardBarrier 标志控制
product(bool, ShenandoahCardBarrier, false, DIAGNOSTIC,
        "true when ShenandoahGCMode is generational, false otherwise")
```

Remembered set 扫描在并发标记之前执行:

```cpp
// shenandoahConcurrentGC.cpp::collect()
entry_scan_remembered_set();   // 扫描 card table, 将脏卡片中的引用推入标记队列
entry_mark_roots();
entry_mark();
```

### 8.6 控制线程

分代模式使用专用的控制线程:

```
ShenandoahController (基类)
├── ShenandoahControlThread            // 非分代模式
└── ShenandoahGenerationalControlThread // 分代模式

ShenandoahRegulatorThread              // 调节器线程: 协调 young/old 收集节奏
```

### 8.7 为什么需要分代 Shenandoah?

非分代 Shenandoah 的问题:
1. **每次收集全堆**: 标记遍历整个堆, 即使大部分老对象不需要处理
2. **高分配速率下吞吐量下降**: 标记/回收全堆的 CPU 开销影响 mutator
3. **短命对象与长命对象混合收集**: 效率低

分代模式的优势:
- **Young GC 频率高但范围小**: 只标记/回收年轻代, 大幅减少标记工作量
- **Old GC 并发独立运行**: 不阻塞年轻代收集
- **更好的吞吐量**: 减少并发 GC 的 CPU 占用

---

## 9. 退化与完全 GC (Degenerated / Full GC)

### GC 升级链

```
源码: shenandoahGC.hpp

// GC 关系:
//
// ("normal" mode) ----> Concurrent GC ----> (finish)
//                            |
//                            | <upgrade>
//                            v
// ("passive" mode) ---> Degenerated GC ---> (finish)
//                            |
//                            | <upgrade>
//                            v
//                         Full GC --------> (finish)
```

### 退化点 (Degeneration Points)

当并发 GC 被取消 (例如分配速度超过 GC 速度), 系统从取消点进入退化 GC:

```cpp
// 源码: shenandoahGC.hpp

enum ShenandoahDegenPoint {
    _degenerated_unset,
    _degenerated_outside_cycle,   // 在周期外触发
    _degenerated_roots,           // 并发根扫描阶段取消
    _degenerated_mark,            // 并发标记阶段取消
    _degenerated_evac,            // 并发回收阶段取消
    _degenerated_update_refs,     // 并发引用更新阶段取消
};
```

退化 GC (`ShenandoahDegenGC`) 在 STW 下从取消点继续完成剩余工作:

```
源码: shenandoahDegeneratedGC.hpp

class ShenandoahDegenGC : public ShenandoahGC {
    const ShenandoahDegenPoint _degen_point;

    void op_reset();
    void op_mark();
    void op_finish_mark();
    void op_prepare_evacuation();
    void op_evacuate();
    void op_init_update_refs();
    void op_update_refs();
    void op_update_roots();
    void op_cleanup_complete();

    void upgrade_to_full();   // 退化 GC 也失败 → 升级为 Full GC
};
```

### Full GC 阈值

连续退化 GC 达到 `ShenandoahFullGCThreshold` (默认 3) 次后, 直接执行 Full GC。
连续无进展 GC 达到 `ShenandoahNoProgressThreshold` (默认 5) 次后, 也执行 Full GC。

---

## 10. GC 状态机 (GC State)

### GC 状态位

`ShenandoahHeap` 维护一个位图表示当前 GC 状态, 用于屏障快速判断:

```cpp
// 源码: shenandoahHeap.hpp

enum GCStateBitPos {
    HAS_FORWARDED_BITPOS   = 0,  // 堆中有转发对象: 需要 LRB
    MARKING_BITPOS         = 1,  // 正在标记: 需要 SATB 屏障
    EVACUATION_BITPOS      = 2,  // 正在回收: 需要 LRB (与 HAS_FORWARDED 同设)
    UPDATE_REFS_BITPOS     = 3,  // 正在更新引用: 无需额外屏障
    WEAK_ROOTS_BITPOS      = 4,  // 正在处理弱引用/根: 需要弱 LRB
    YOUNG_MARKING_BITPOS   = 5,  // 年轻代标记中 (分代)
    OLD_MARKING_BITPOS     = 6,  // 老年代标记中 (分代)
};

enum GCState {
    STABLE        = 0,                    // 稳定态: 无需任何屏障
    HAS_FORWARDED = 1 << 0,
    MARKING       = 1 << 1,
    EVACUATION    = 1 << 2,
    UPDATE_REFS   = 1 << 3,
    WEAK_ROOTS    = 1 << 4,
    YOUNG_MARKING = 1 << 5,
    OLD_MARKING   = 1 << 6,
};
```

**关键不变量**: 当 `gc_state == STABLE (0)` 时, 堆处于稳定状态, **无需任何屏障**。这是 JIT 编译器优化屏障的重要依据。

状态变更必须在 safepoint 进行, 然后通过 `propagate_gc_state_to_all_threads()` 同步到所有线程的 thread-local 副本, 实现屏障判断的无锁快速路径。

---

## 11. 关键调优参数

### 基础配置

```bash
# 启用 Shenandoah
-XX:+UseShenandoahGC

# 选择 GC 模式
-XX:ShenandoahGCMode=satb           # 默认: SATB 非分代
-XX:ShenandoahGCMode=generational   # 分代模式
-XX:ShenandoahGCMode=passive        # 被动模式 (需 UnlockDiagnosticVMOptions)

# 选择启发式 (非分代模式)
-XX:ShenandoahGCHeuristics=adaptive    # 默认
-XX:ShenandoahGCHeuristics=static
-XX:ShenandoahGCHeuristics=compact
-XX:ShenandoahGCHeuristics=aggressive  # 需 UnlockDiagnosticVMOptions
```

### Region 配置

| 参数 | 默认 | 含义 |
|------|------|------|
| `ShenandoahRegionSize` | 0 (自动) | Region 大小 (字节) |
| `ShenandoahTargetNumRegions` | 2048 | 目标 Region 数量 |
| `ShenandoahMinRegionSize` | 256K | Region 最小值 |
| `ShenandoahMaxRegionSize` | 32M | Region 最大值 |

### GC 触发参数

| 参数 | 默认 | 含义 |
|------|------|------|
| `ShenandoahMinFreeThreshold` | 10 | 最小空闲百分比阈值 |
| `ShenandoahInitFreeThreshold` | 70 | 初始空闲百分比阈值 |
| `ShenandoahGarbageThreshold` | 25 | Region 垃圾占比阈值 (%), 低于此值不加入 CSet |
| `ShenandoahGuaranteedGCInterval` | 300000 (5min) | 保证 GC 间隔 (ms) |
| `ShenandoahImmediateThreshold` | 70 | 垃圾占比超过此值的 Region 立即回收 |
| `ShenandoahAllocSpikeFactor` | 5 | 分配尖峰因子 |

### 回收 (Evacuation) 参数

| 参数 | 默认 | 含义 |
|------|------|------|
| `ShenandoahEvacReserve` | 5 | 回收预留空间占堆百分比 |
| `ShenandoahEvacWaste` | 1.2 | 回收浪费因子 (内部碎片) |
| `ShenandoahEvacReserveOverflow` | true | 允许超出回收预留 |

### 自适应启发式参数

| 参数 | 默认 | 含义 |
|------|------|------|
| `ShenandoahAdaptiveSampleFrequencyHz` | 10 | 分配速率采样频率 |
| `ShenandoahAdaptiveSampleSizeSeconds` | 10 | 采样窗口大小 (秒) |
| `ShenandoahAdaptiveInitialConfidence` | 1.8 | 初始置信度 (标准差倍数) |
| `ShenandoahAdaptiveInitialSpikeThreshold` | 1.8 | 初始尖峰检测阈值 |
| `ShenandoahAdaptiveDecayFactor` | 0.5 | 惩罚衰减因子 |
| `ShenandoahLearningSteps` | 5 | 学习阶段步数 |

### 退化/Full GC 参数

| 参数 | 默认 | 含义 |
|------|------|------|
| `ShenandoahDegeneratedGC` | true | 允许退化 GC |
| `ShenandoahFullGCThreshold` | 3 | 连续退化 GC 次数触发 Full GC |
| `ShenandoahNoProgressThreshold` | 5 | 无进展 GC 次数触发 Full GC |
| `ShenandoahCriticalFreeThreshold` | 1 | 临界空闲百分比 |

### 分代模式专用参数

| 参数 | 默认 | 含义 |
|------|------|------|
| `ShenandoahGuaranteedYoungGCInterval` | 300000 | Young GC 保证间隔 (ms) |
| `ShenandoahGuaranteedOldGCInterval` | 600000 | Old GC 保证间隔 (ms) |
| `ShenandoahOldGarbageThreshold` | 25 | 老年代垃圾回收阈值 (%) |
| `ShenandoahOldEvacPercent` | 75 | 老年代回收预留占比 |
| `ShenandoahOldEvacWaste` | 1.4 | 老年代回收浪费因子 |
| `ShenandoahPromoEvacWaste` | 1.2 | 晋升浪费因子 |
| `ShenandoahOldCompactionReserve` | 8 | 老年代压缩预留 Region 数 |

### 并发线程参数

```bash
-XX:ParallelGCThreads=N     # STW 阶段并行线程数 (默认 CPU 核数)
-XX:ConcGCThreads=N         # 并发 GC 线程数 (默认 ParallelGCThreads/4)
```

### 其他参数

| 参数 | 默认 | 含义 |
|------|------|------|
| `ShenandoahUncommit` | true | 空闲时释放内存给 OS |
| `ShenandoahUncommitDelay` | 300000 (5min) | Region 空闲多久后释放 |
| `ShenandoahHumongousMoves` | true | 允许移动巨型对象 |
| `ShenandoahSATBBufferSize` | 1024 | SATB buffer 大小 |
| `ShenandoahMarkScanPrefetch` | 32 | 标记扫描预取数 |
| `ShenandoahImplicitGCInvokesConcurrent` | false | System.gc() 是否触发并发 GC |

---

## 12. 诊断与监控

### GC 日志

```bash
# 基础 GC 日志
-Xlog:gc:file=gc.log:time,level,tags

# Shenandoah 详细日志
-Xlog:gc+ergo=debug           # 启发式决策 (触发原因, CSet 选择)
-Xlog:gc+stats=info           # 每周期统计: 阶段耗时
-Xlog:gc+heap=info            # 堆使用信息

# 屏障相关
-Xlog:gc+barrier=trace        # 屏障触发信息

# Region 信息
-Xlog:gc+region=trace         # Region 状态变更

# 分代信息
-Xlog:gc+generation=info      # 分代收集信息

# 全面日志 (调试用)
-Xlog:gc*=debug:file=shenandoah-debug.log:time,level,tags
```

### 日志输出示例

```
# 典型的一次并发 GC 周期
GC(42) Pause Init Mark (process weakrefs) 0.216ms
GC(42) Concurrent marking (process weakrefs) 14.830ms
GC(42) Pause Final Mark (process weakrefs) 0.402ms
GC(42) Concurrent thread roots 0.124ms
GC(42) Concurrent weak references 1.052ms
GC(42) Concurrent weak roots 0.086ms
GC(42) Concurrent cleanup 0.034ms
GC(42) Concurrent evacuation 3.412ms
GC(42) Concurrent update references 8.230ms
GC(42) Concurrent update thread roots 0.098ms
GC(42) Pause Final Update Refs 0.163ms
GC(42) Concurrent cleanup 0.026ms
```

### JFR 事件

Shenandoah 通过标准 GC JFR 事件报告:
- `jdk.GarbageCollection` - GC 周期
- `jdk.GCPhasePause` - STW 暂停阶段
- `jdk.GCPhaseConcurrent` - 并发阶段
- `jdk.GCHeapSummary` - 堆摘要

### 关键监控指标

| 指标 | 正常范围 | 异常信号 |
|------|----------|----------|
| STW 暂停时间 | < 5ms | > 10ms 频繁出现 |
| 并发 GC 周期时间 | 依赖堆大小和存活率 | 持续增长 |
| 退化 GC 频率 | 偶尔 | 频繁退化 |
| Full GC 频率 | 几乎没有 | 任何 Full GC |
| 分配速率 vs GC 速度 | GC 跟得上 | 分配持续超过 GC |
| 空闲 Region 数 | > ShenandoahMinFreeThreshold | 持续低于阈值 |

### 常见问题排查

```bash
# 1. 退化 GC 频繁
# 原因: 分配速率太快, 并发 GC 来不及完成
# 解决: 增加 ConcGCThreads, 增加堆大小, 或调低 ShenandoahMinFreeThreshold

# 2. STW 暂停偏长
# 原因: root set 大 (大量线程/JNI global refs)
# 排查:
-Xlog:gc+stats=info   # 查看各阶段耗时分布

# 3. 吞吐量不足
# 考虑: 切换到分代模式, 减少全堆标记的开销
-XX:ShenandoahGCMode=generational

# 4. OOM during evacuation
# 现象: "Out of memory for Shenandoah evacuation"
# 原因: 回收预留空间不足
# 解决: 增加 ShenandoahEvacReserve 或增加堆大小
```

---

## 13. JEP 演进

| JEP | 版本 | 内容 |
|-----|------|------|
| [JEP 189](https://openjdk.org/jeps/189) | JDK 12 | Shenandoah 作为 **experimental** 特性引入 |
| (JDK 14) | JDK 14 | 从 Brooks pointer 改为 mark word 转发 (大幅降低内存开销) |
| [JEP 379](https://openjdk.org/jeps/379) | JDK 15 | Shenandoah 升级为 **production** 特性 |
| [JEP 404](https://openjdk.org/jeps/404) | JDK 21+ | Generational Shenandoah (experimental) |
| [JEP 521](https://openjdk.org/jeps/521) | JDK 25 | Generational Shenandoah 升级为 production |

### 主要演进时间线

```
JDK 12 ─── JDK 14 ──── JDK 15 ──── JDK 21 ──── JDK 25
  │            │           │           │           │
  引入         去掉         Production   分代         分代
  (实验性)     Brooks ptr   Ready       (实验性)     Production
  +8字节/对象  → mark word
```

---

## 14. vs G1 vs ZGC 对比

### 架构对比

| 维度 | G1 | Shenandoah | ZGC |
|------|----|-----------:|-----|
| **堆布局** | Region-based | Region-based | Page-based |
| **回收方式** | STW evacuation | **并发** evacuation | **并发** relocation |
| **指针处理** | 无染色 | mark word 转发 | 染色指针 (colored pointer) |
| **读屏障** | 无 | Load Reference Barrier | Load barrier + 染色检查 |
| **写屏障** | 记忆集 + SATB | SATB (+ card barrier 分代) | Store barrier |
| **压缩 OOP** | 支持 | 支持 | 不支持 (需用完整 64-bit 指针) |
| **最大堆** | 无限制 | 无限制 | 16TB |
| **分代** | 有 (始终) | 可选 (JDK 25+ production) | 有 (JDK 21+) |
| **平台** | 所有 HotSpot 平台 | x86_64, aarch64, riscv64, ppc64le, s390x | x86_64, aarch64 |

### 暂停时间特性

| 场景 | G1 | Shenandoah | ZGC |
|------|----|-----------:|-----|
| STW 暂停与堆大小关系 | 正比 (CSet 大小) | **无关** | **无关** |
| 典型暂停时间 (参考) | 10-200ms | < 1-5ms | < 1-2ms |
| 暂停由什么决定 | CSet 中存活对象量 | Root set 大小 | Root set 大小 |

### 吞吐量影响

| 维度 | G1 | Shenandoah | ZGC |
|------|----|-----------:|-----|
| 屏障开销 | 低 (仅写) | 中 (读+写) | 中 (读+写) |
| 并发线程 CPU 消耗 | 中 | 中-高 | 中-高 |
| 内存额外开销 | 记忆集 ~5-10% | SATB buffers ~1-2% | 染色元数据 |

### 选型建议

| 场景 | 推荐 |
|------|------|
| 延迟最敏感, 亚毫秒级暂停 | ZGC |
| 低延迟 + 压缩 OOP + 广泛平台 | Shenandoah |
| 吞吐量优先, 暂停可容忍几百毫秒 | G1 |
| 堆 < 4GB, 简单场景 | G1 |
| 堆 > 32GB, 极低延迟 | ZGC 或 Shenandoah |

---

## 15. 源码导航

### 核心类 (210 个源文件)

```
src/hotspot/share/gc/shenandoah/
├── shenandoahHeap.hpp/.cpp               核心堆实现
├── shenandoahHeapRegion.hpp/.cpp          Region 定义与状态机
├── shenandoahBarrierSet.hpp/.cpp          屏障集合
├── shenandoahBarrierSet.inline.hpp        屏障内联实现 (LRB 等)
├── shenandoahForwarding.hpp               转发指针 API
├── shenandoahForwarding.inline.hpp        转发指针实现 (mark word)
├── shenandoahConcurrentGC.hpp/.cpp        并发 GC 周期编排
├── shenandoahConcurrentMark.hpp/.cpp      并发标记
├── shenandoahDegeneratedGC.hpp/.cpp       退化 GC
├── shenandoahFullGC.hpp/.cpp              Full GC
├── shenandoahGC.hpp                       GC 基类 + DegenPoint 枚举
├── shenandoahCollectionSet.hpp/.cpp       回收集合
├── shenandoahFreeSet.hpp/.cpp             空闲 Region 管理
├── shenandoahEvacOOMHandler.hpp/.cpp      回收 OOM 处理
├── shenandoahController.hpp/.cpp          控制线程基类
├── shenandoahControlThread.hpp/.cpp       非分代控制线程
├── shenandoahGeneration.hpp/.cpp          代抽象基类
├── shenandoahGenerationType.hpp           代类型枚举
├── shenandoahAffiliation.hpp              Region 所属代
├── shenandoahGenerationalHeap.hpp/.cpp    分代堆实现
├── shenandoahGenerationalControlThread.hpp/.cpp  分代控制线程
├── shenandoahYoungGeneration.hpp/.cpp     年轻代
├── shenandoahOldGeneration.hpp/.cpp       老年代
├── shenandoahOldGC.hpp/.cpp               老年代 GC
├── shenandoahCardTable.hpp/.cpp           卡表 (分代模式)
├── shenandoahRegulatorThread.hpp/.cpp     收集节奏调节器
├── shenandoahAgeCensus.hpp/.cpp           年龄统计 (自适应晋升)
├── shenandoahMmuTracker.hpp/.cpp          MMU (最小 mutator 利用率) 跟踪
├── shenandoah_globals.hpp                 所有 VM 参数定义
│
├── mode/                                  GC 模式
│   ├── shenandoahMode.hpp                 模式基类
│   ├── shenandoahSATBMode.hpp/.cpp        SATB 模式
│   ├── shenandoahGenerationalMode.hpp/.cpp 分代模式
│   └── shenandoahPassiveMode.hpp/.cpp     被动模式
│
├── heuristics/                            启发式
│   ├── shenandoahHeuristics.hpp/.cpp      基类
│   ├── shenandoahAdaptiveHeuristics.hpp/.cpp   自适应
│   ├── shenandoahStaticHeuristics.hpp/.cpp     静态
│   ├── shenandoahCompactHeuristics.hpp/.cpp    紧凑
│   ├── shenandoahAggressiveHeuristics.hpp/.cpp 激进
│   ├── shenandoahPassiveHeuristics.hpp/.cpp    被动
│   ├── shenandoahGenerationalHeuristics.hpp/.cpp 分代基类
│   ├── shenandoahGlobalHeuristics.hpp/.cpp     全局收集
│   ├── shenandoahYoungHeuristics.hpp/.cpp      年轻代
│   ├── shenandoahOldHeuristics.hpp/.cpp        老年代
│   └── shenandoahSpaceInfo.hpp                 空间信息接口
│
├── c1/                                    C1 编译器屏障
├── c2/                                    C2 编译器屏障
└── shenandoahBarrierSetAssembler*.hpp     汇编屏障 (各平台)
```

### 关键阅读路径

1. **理解 GC 周期**: `shenandoahConcurrentGC.cpp::collect()` -- 完整的并发 GC 流程
2. **理解屏障**: `shenandoahBarrierSet.inline.hpp` -- LRB 和 SATB 的核心逻辑
3. **理解转发**: `shenandoahForwarding.inline.hpp` -- mark word 编码/解码
4. **理解启发式**: `shenandoahAdaptiveHeuristics.cpp::should_start_gc()` -- 触发决策
5. **理解分代**: `shenandoahGenerationalHeap.hpp` + `shenandoahGeneration.hpp` -- 分代架构
6. **理解状态机**: `shenandoahHeap.hpp::GCStateBitPos` -- GC 状态位与屏障关系

---

## 相关链接

- [JEP 521](/jeps/gc/jep-521.md) - Generational Shenandoah (Production)
- [Shenandoah GC Wiki](https://wiki.openjdk.org/display/shenandoah/) - OpenJDK Wiki
- [GC 主题总览](../) - 其他 GC 专题
