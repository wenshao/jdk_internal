# ZGC 详解

> **30 秒速读**
> - 亚毫秒级 GC 暂停 (<1ms)，暂停时间不随堆大小或存活对象数量增长
> - 支持 TB 级堆内存，几乎所有 GC 操作并发执行 (标记、重定位、引用处理、类卸载)
> - 核心技术: Colored Pointers (着色指针) + Load Barrier (读屏障)
> - JDK 21 分代 ZGC 正式发布，分 Young/Old 两代独立收集，降低回收频率
> - ZPage 三种类型: Small (2MB)、Medium (32MB)、Large (动态)
> - ZDirector 以 100Hz 频率评估 GC 触发决策，源码约 237 个 .cpp/.hpp 文件

> Z Garbage Collector: 低延迟垃圾收集器 -- 亚毫秒级暂停, 不随堆大小增长

[← 返回 GC](../)

---
## 目录

1. [ZGC 架构概览](#1-zgc-架构概览)
2. [ZPage: Region-Based 内存管理](#2-zpage-region-based-内存管理)
3. [Colored Pointers (着色指针)](#3-colored-pointers-着色指针)
4. [Load Barrier (读屏障)](#4-load-barrier-读屏障)
5. [Store Barrier (写屏障) -- 分代模式](#5-store-barrier-写屏障----分代模式)
6. [GC 周期详解 -- Young Generation](#6-gc-周期详解----young-generation)
7. [GC 周期详解 -- Old Generation](#7-gc-周期详解----old-generation)
8. [分代 ZGC (Generational ZGC)](#8-分代-zgc-generational-zgc)
9. [JEP 演进历史](#9-jep-演进历史)
10. [关键调优参数](#10-关键调优参数)
11. [性能特性与对比](#11-性能特性与对比)
12. [诊断与故障排除](#12-诊断与故障排除)
13. [源码结构](#13-源码结构)

---

## 1. ZGC 架构概览

### 1.1 设计哲学

ZGC 的核心设计目标是 **亚毫秒级 GC 暂停** (sub-millisecond pause times), 且暂停时间不随堆大小 (heap size) 或存活对象数量 (live set size) 增长。为实现这一目标, ZGC 将几乎所有 GC 操作都设计为并发 (concurrent) 执行:

- **并发标记** (Concurrent Marking) -- 与应用线程同时遍历对象图
- **并发重定位** (Concurrent Relocation) -- 与应用线程同时移动对象
- **并发引用处理** (Concurrent Reference Processing) -- 并发处理 weak/soft/phantom references
- **并发类卸载** (Concurrent Class Unloading) -- 并发卸载不再使用的类

仅有极少数操作需要 STW (Stop-The-World) 暂停, 且每次暂停时间通常在 1ms 以内。

### 1.2 核心组件层次

```
源码: src/hotspot/share/gc/z/   (约 237 个 .cpp/.hpp 文件)

┌──────────────────────────────────────────────────────────────────┐
│                     ZCollectedHeap                              │
│         (CollectedHeap 子类, JVM GC 接口入口)                    │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                       ZHeap                               │   │
│  │  (堆管理: 页表 ZPageTable + 分配器 ZObjectAllocator)      │   │
│  │                                                           │   │
│  │  ┌──────────────┐  ┌────────────────────────────────┐    │   │
│  │  │ ZGenerationYoung  │ ZGenerationOld               │    │   │
│  │  │ (Young 代)   │  │ (Old 代)                       │    │   │
│  │  │ - ZMark      │  │ - ZMark                        │    │   │
│  │  │ - ZRelocate  │  │ - ZRelocate                    │    │   │
│  │  │ - ZRemembered│  │ - ZReferenceProcessor          │    │   │
│  │  └──────────────┘  │ - ZWeakRootsProcessor          │    │   │
│  │                     │ - ZUnload (类卸载)             │    │   │
│  │                     └────────────────────────────────┘    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐    │
│  │ ZDriverMinor  │  │ ZDriverMajor │  │ ZDirector          │    │
│  │ (Minor GC    │  │ (Major GC    │  │ (GC 调度决策       │    │
│  │  驱动线程)    │  │  驱动线程)    │  │  100Hz 评估规则)   │    │
│  └──────────────┘  └──────────────┘  └────────────────────┘    │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ ZBarrierSet + ZBarrier (读屏障/写屏障/标记屏障)           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ ZPageAllocator (页分配器: 物理/虚拟内存管理)              │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

**关键类定义** (来自源码):

```cpp
// zCollectedHeap.hpp -- JVM 顶层入口
class ZCollectedHeap : public CollectedHeap {
  ZBarrierSet       _barrier_set;
  ZHeap             _heap;
  ZDriverMinor*     _driver_minor;   // Minor (Young) GC 驱动线程
  ZDriverMajor*     _driver_major;   // Major (Old) GC 驱动线程
  ZDirector*        _director;       // GC 调度决策
  ZRuntimeWorkers   _runtime_workers;
};

// zHeap.hpp -- 堆管理
class ZHeap {
  ZPageAllocator   _page_allocator;
  ZPageTable       _page_table;
  ZObjectAllocator _object_allocator;
  ZGenerationOld   _old;
  ZGenerationYoung _young;
};
```

### 1.3 线程模型

ZGC 使用多线程协作模型:

| 线程 | 类 | 说明 |
|------|------|------|
| ZDriverMinor | `ZDriverMinor` | Minor Collection 驱动, 负责 young generation GC |
| ZDriverMajor | `ZDriverMajor` | Major Collection 驱动, 负责 old generation GC |
| ZDirector | `ZDirector` | GC 决策线程, 以 100Hz 频率评估是否需要触发 GC |
| GC Workers | `ZWorkers` | 可配置数量的 GC 工作线程, 执行并发标记/重定位等 |
| Application | 应用线程 | 通过 barrier (屏障) 与 GC 协作 |

```cpp
// zDirector.hpp
class ZDirector : public ZThread {
  static const uint64_t DecisionHz = 100;  // 每秒评估 100 次
};
```

---

## 2. ZPage: Region-Based 内存管理

### 2.1 ZPage 类型

ZGC 将堆划分为多个 **ZPage** (类似 G1 的 Region, 但大小更灵活)。ZPage 有三种类型:

```cpp
// zPageType.hpp
enum class ZPageType : uint8_t {
  small,
  medium,
  large
};
```

| 类型 | 大小 | 对象大小限制 | 说明 |
|------|------|-------------|------|
| **Small** | 2MB (固定) | <= 256KB (页大小的 1/8) | 小对象分配, 最常用 |
| **Medium** | 动态, 最大约 32MB | <= medium page size / 8 | 中等对象, 大小根据堆大小自动调整 |
| **Large** | N x 2MB (granule 的倍数) | 无限制 | 大对象, 每个 page 仅存放一个对象 |

**关键常量** (来自 `zGlobals.hpp`):

```cpp
// zGlobals.hpp
const size_t ZGranuleSizeShift = 21;                    // 2MB
const size_t ZGranuleSize      = (size_t)1 << 21;      // 2MB -- 所有页的基本粒度

const int    ZPageSizeSmallShift = (int)ZGranuleSizeShift;  // Small = 1 granule = 2MB
const size_t ZPageSizeSmall      = (size_t)1 << ZPageSizeSmallShift;

// Medium 页大小动态确定, 不超过堆的 3.125%
extern size_t ZPageSizeMediumMax;   // 通常 32MB (最大堆足够大时)
extern size_t ZPageSizeMediumMin;   // 范围模式下的最小值

const size_t ZObjectSizeLimitSmall = ZPageSizeSmall / 8;  // 256KB -- 12.5% max waste
extern size_t ZObjectSizeLimitMedium;                      // medium page / 8
```

**Medium 页大小的动态计算** (来自 `zHeuristics.cpp`):

```cpp
// Medium 页大小设为不超过最大堆的 3.125%
// 例如: 1GB 堆 → medium = 32MB; 256MB 堆 → medium = 8MB
void ZHeuristics::set_medium_page_size() {
  ZPageSizeMediumMax      = size;          // 根据堆大小计算
  ZPageSizeMediumMaxShift = log2i_exact(ZPageSizeMediumMax);
  ZObjectSizeLimitMedium  = ZPageSizeMediumMax / 8;
}
```

### 2.2 ZPage 内部结构

```cpp
// zPage.hpp
class ZPage : public CHeapObj<mtGC> {
  const ZPageType               _type;              // small/medium/large
  ZGenerationId                 _generation_id;      // young 或 old
  ZPageAge                      _age;                // eden / survivor1-14 / old
  uint32_t                      _seqnum;             // GC 序列号
  const ZVirtualMemory          _virtual;            // 虚拟内存描述
  volatile zoffset_end          _top;                // 当前分配位置 (bump pointer)
  ZLiveMap                      _livemap;            // 存活对象位图
  ZRememberedSet                _remembered_set;     // 记忆集 (old→young 引用)
  volatile bool                 _relocate_promoted;  // 是否正在重定位已提升对象
};
```

### 2.3 Page Age (页龄) 与分代

ZGC 支持精细化的对象年龄追踪, 最多 14 个 survivor 代:

```cpp
// zPageAge.hpp
enum class ZPageAge : uint8_t {
  eden,           // 新分配
  survivor1,      // 经历 1 次 young GC
  survivor2,      // 经历 2 次 young GC
  // ...
  survivor14,     // 经历 14 次 young GC
  old             // 提升到 old generation
};
```

对象通过 **tenuring threshold** (晋升阈值) 从 young 代提升到 old 代:

```
Eden → Survivor1 → Survivor2 → ... → SurvivorN → Old
                                                    ↑
                                          tenuring threshold
```

### 2.4 对象分配

ZGC 使用 **TLAB (Thread-Local Allocation Buffer)** 进行快速分配。分配路径:

```
应用线程分配 → TLAB 快速分配 (bump pointer)
                → TLAB 耗尽 → 从 ZPage 分配新 TLAB
                   → ZPage 满 → ZPageAllocator 分配新 ZPage
                      → 物理内存不足 → 触发 GC 或 uncommit 回收
```

```cpp
// zHeap.hpp
class ZHeap {
  zaddress alloc_object(size_t size);           // 普通对象分配
  zaddress alloc_tlab(size_t size);             // TLAB 分配
  zaddress alloc_object_for_relocation(size_t size, ZPageAge age);  // 重定位分配
};
```

---

## 3. Colored Pointers (着色指针)

### 3.1 核心创新

着色指针 (Colored Pointers) 是 ZGC 最核心的技术创新。与传统 GC 在对象头 (object header) 或辅助数据结构中存储 GC 元数据不同, ZGC 直接在 **64 位对象指针本身** 中嵌入元数据位 (metadata bits)。

### 3.2 指针布局

ZGC 的着色指针 (`zpointer`) 由地址位 (address bits) + 元数据字节 (metadata bytes) 组成:

```
来自 zAddress.hpp 的精确布局:

                    地址位                          元数据位
    ┌───────────────────────────────┐  ┌─────────────────────────────┐
    aaa...aaa                          RRRR  MM  mm  FF  rr  0000
    └─address─┘                        │     │   │   │   │   └─Reserved (4 bits)
                                       │     │   │   │   └─ Remembered[0,1] (2 bits)
                                       │     │   │   └─ Finalizable[0,1] (2 bits)
                                       │     │   └─ MarkedYoung[0,1] (2 bits)
                                       │     └─ MarkedOld[0,1] (2 bits)
                                       └─ Remapped[00,01,10,11] (4 bits)

位模式:  RRRRMMmmFFrr0000
         ****                  ← Load barrier 使用
         **********            ← Mark barrier 使用
         ************          ← Store barrier 使用
                     ****      ← Reserved bits
```

### 3.3 元数据位详解

```cpp
// zAddress.hpp -- 精确的位定义

// Reserved bits (bits 0-3)
const size_t    ZPointerReservedShift   = 0;
const size_t    ZPointerReservedBits    = 4;

// Remembered set bits (bits 4-5) -- 分代 GC 使用
const size_t    ZPointerRememberedShift = 4;  // = Reserved(4)
const size_t    ZPointerRememberedBits  = 2;
const uintptr_t ZPointerRemembered0     = 1 << 4;   // bit 4
const uintptr_t ZPointerRemembered1     = 1 << 5;   // bit 5

// Marked bits (bits 6-11) -- 包含 Finalizable + MarkedYoung + MarkedOld
const size_t    ZPointerMarkedShift     = 6;  // = Reserved(4) + Remembered(2)
const size_t    ZPointerMarkedBits      = 6;

const uintptr_t ZPointerFinalizable0    = 1 << 6;   // bit 6
const uintptr_t ZPointerFinalizable1    = 1 << 7;   // bit 7
const uintptr_t ZPointerMarkedYoung0    = 1 << 8;   // bit 8
const uintptr_t ZPointerMarkedYoung1    = 1 << 9;   // bit 9
const uintptr_t ZPointerMarkedOld0      = 1 << 10;  // bit 10
const uintptr_t ZPointerMarkedOld1      = 1 << 11;  // bit 11

// Remapped bits (bits 12-15) -- Load barrier 核心
const size_t    ZPointerRemappedShift   = 12;  // = Reserved(4) + Remembered(2) + Marked(6)
const size_t    ZPointerRemappedBits    = 4;
const uintptr_t ZPointerRemapped00      = 1 << 12;
const uintptr_t ZPointerRemapped01      = 1 << 13;
const uintptr_t ZPointerRemapped10      = 1 << 14;
const uintptr_t ZPointerRemapped11      = 1 << 15;
```

### 3.4 Barrier 元数据掩码

不同的 barrier 关注不同层次的元数据位:

```cpp
// zAddress.hpp
const uintptr_t ZPointerLoadMetadataMask  = ZPointerRemappedMask;          // Remapped 位
const uintptr_t ZPointerMarkMetadataMask  = ZPointerLoadMetadataMask       // + Marked 位
                                          | ZPointerMarkedMask;
const uintptr_t ZPointerStoreMetadataMask = ZPointerMarkMetadataMask       // + Remembered 位
                                          | ZPointerRememberedMask;
const uintptr_t ZPointerAllMetadataMask   = ZPointerStoreMetadataMask;
```

这形成了一个严格的 "强度层级" (strength hierarchy):
```
Load Good ⊂ Mark Good ⊂ Store Good
   (最弱)     (中等)      (最强)
```

### 3.5 Colored/Uncolored 指针类型

源码定义了严格的类型区分:

```cpp
// zAddress.hpp

// 着色指针 (colored oop) -- 包含元数据, 不能直接解引用
enum class zpointer  : uintptr_t { null = 0 };

// 去色指针 (uncolored oop) -- 安全的, 可以解引用
enum class zaddress  : uintptr_t { null = 0 };

// 去色但不安全的指针 -- 可能指向已 uncommit 的内存
enum class zaddress_unsafe : uintptr_t { null = 0 };
```

**指针操作类**:

```cpp
// zAddress.hpp
class ZPointer : public AllStatic {
  // 去色: 从 zpointer 提取实际地址
  static zaddress uncolor(zpointer ptr);
  static zaddress_unsafe uncolor_unsafe(zpointer ptr);

  // 状态检查
  static bool is_load_good(zpointer ptr);      // Remapped 位正确?
  static bool is_mark_good(zpointer ptr);       // Remapped + Marked 位正确?
  static bool is_store_good(zpointer ptr);      // 所有元数据位正确?
  static bool is_marked_young(zpointer ptr);    // 被 young marking 标记?
  static bool is_marked_old(zpointer ptr);      // 被 old marking 标记?
  static bool is_marked_finalizable(zpointer ptr);
  static bool is_remapped(zpointer ptr);
  static bool is_remembered_exact(zpointer ptr);
};

class ZAddress : public AllStatic {
  // 着色: 给地址附加元数据
  static zpointer color(zaddress addr, uintptr_t color);
  static zpointer load_good(zaddress addr, zpointer prev);
  static zpointer mark_good(zaddress addr, zpointer prev);
  static zpointer store_good(zaddress addr);
};
```

### 3.6 Remapped 位的交替 (Flip) 机制

Remapped 位用 4 个位编码 Young 和 Old 两代的 remap 状态。每次 GC 阶段切换时, 通过 "flip" 改变当前 "good" 位:

```cpp
// zAddress.hpp
// RemappedOldMask 在两种模式间交替:
//   RemappedOld0 => 0011    RemappedOld1 => 1100

// RemappedYoungMask 在两种模式间交替:
//   RemappedYoung0 => 0101  RemappedYoung1 => 1010

// 交集产生 4 种组合:
//   Old0 & Young0 = 0001 = Remapped00
//   Old0 & Young1 = 0010 = Remapped01
//   Old1 & Young0 = 0100 = Remapped10
//   Old1 & Young1 = 1000 = Remapped11
```

```cpp
// zAddress.hpp
class ZGlobalsPointers : public AllStatic {
  static void flip_young_mark_start();       // Young GC 标记开始时翻转
  static void flip_young_relocate_start();   // Young GC 重定位开始时翻转
  static void flip_old_mark_start();         // Old GC 标记开始时翻转
  static void flip_old_relocate_start();     // Old GC 重定位开始时翻转
};
```

### 3.7 x86 上地址位与元数据位的重叠

在 x86 平台上, 地址位紧接在 load-good 位之后开始, 允许将 good-bit 检查和元数据去除合并为一条 **speculative shift** 指令:

```
x86 平台上不同 Remapped 位的指针布局:

             vvv- overlapping zeros
    aaa...aaa0001MMmmFFrr0000 = Remapped00 zpointer

             vv-- overlapping zeros
   aaa...aaa00010MMmmFFrr0000 = Remapped01 zpointer

             v--- overlapping zero
  aaa...aaa000100MMmmFFrr0000 = Remapped10 zpointer

             ---- no overlapping zeros
 aaa...aaa0001000MMmmFFrr0000 = Remapped11 zpointer
```

AArch64 平台不使用此重叠优化, 而是使用补码 (complement) 方式 -- 3 个 good 位 + 1 个 bad 位。

### 3.8 与 Compressed Oops 的关系

早期 ZGC (JDK 11-14) 不兼容 Compressed Oops, 因为着色指针占用了高位, 而 Compressed Oops 也需要利用 64 位指针的特定位。

- **Generational ZGC (JDK 21+)**: 元数据位从高位重新设计到低位, 消除了 multi-mapping 的需求
- **CompressedOops**: ZGC 始终不支持 CompressedOops (显式禁用), 因为着色指针与压缩指针在架构上不兼容
- **当前实现**: 元数据位位于指针低位 (bits 0-3), 地址位在高位, 通过 shift 操作在 barrier 中高效处理

---

## 4. Load Barrier (读屏障)

### 4.1 基本原理

ZGC 的读屏障在每次 **加载对象引用** 时触发。读屏障检查指针的元数据位是否满足当前 GC 阶段的 "good" 条件, 如果不满足则进入 slow path 修复指针。

```cpp
// zBarrier.hpp 中的核心模板方法
template <typename ZBarrierSlowPath>
static zaddress barrier(
    ZBarrierFastPath fast_path,   // 快速检查函数
    ZBarrierSlowPath slow_path,   // 慢速处理函数
    ZBarrierColor color,          // 着色函数
    volatile zpointer* p,         // 指针位置 (用于 self-heal)
    zpointer o,                   // 原始着色指针
    bool allow_null = false
);
```

### 4.2 Barrier 执行流程

```cpp
// zBarrier.inline.hpp -- 完整的 barrier 流程
template <typename ZBarrierSlowPath>
inline zaddress ZBarrier::barrier(ZBarrierFastPath fast_path,
                                   ZBarrierSlowPath slow_path,
                                   ZBarrierColor color,
                                   volatile zpointer* p,
                                   zpointer o,
                                   bool allow_null) {
  // Step 1: Fast path -- 检查指针是否已经是 "good" 状态
  if (fast_path(o)) {
    return ZPointer::uncolor(o);    // 直接去色返回
  }

  // Step 2: Make load good -- 确保地址正确 (可能需要查询 forwarding table)
  const zaddress load_good_addr = make_load_good(o);

  // Step 3: Slow path -- 执行额外操作 (标记/记忆等)
  const zaddress good_addr = slow_path(load_good_addr);

  // Step 4: Self heal -- 修复原始指针位置
  if (p != nullptr) {
    const zpointer good_ptr = color(good_addr, o);
    self_heal(fast_path, p, o, good_ptr, allow_null);
  }

  return good_addr;
}
```

### 4.3 Load Barrier 的 Fast Path

Load barrier 的 fast path 极为轻量 -- 只需检查 Remapped 位:

```cpp
// zBarrier.inline.hpp
inline bool ZBarrier::is_load_good_or_null_fast_path(zpointer ptr) {
  return ZPointer::is_load_good_or_null(ptr);
}

// Load barrier 入口
inline zaddress ZBarrier::load_barrier_on_oop_field_preloaded(
    volatile zpointer* p, zpointer o) {
  auto slow_path = [](zaddress addr) -> zaddress {
    return addr;    // load barrier 的 slow path 很简单: 地址本身就是结果
  };
  return barrier(is_load_good_or_null_fast_path, slow_path,
                 color_load_good, p, o);
}
```

### 4.4 Make Load Good -- 对象重定位查找

当指针不是 load-good 时, 需要确定对象是否已被移动:

```cpp
// zBarrier.inline.hpp
inline zaddress ZBarrier::make_load_good(zpointer o) {
  if (is_null_any(o)) {
    return zaddress::null;
  }

  if (ZPointer::is_load_good_or_null(o)) {
    return ZPointer::uncolor(o);       // 已经是 good, 直接去色
  }

  // 指针是 bad -- 需要查询 forwarding table 确认对象新位置
  return relocate_or_remap(ZPointer::uncolor_unsafe(o), remap_generation(o));
}
```

### 4.5 Self-Healing (自修复)

Self-healing 是 ZGC 读屏障的关键优化: 当一个指针被发现是 "bad" 状态时, barrier 不仅返回正确的地址, 还会 **原子地修复** 内存中的指针, 使后续访问无需再次触发 slow path。

```cpp
// zBarrier.inline.hpp
inline void ZBarrier::self_heal(ZBarrierFastPath fast_path,
                                 volatile zpointer* p,
                                 zpointer ptr,
                                 zpointer heal_ptr,
                                 bool allow_null) {
  // Self-heal 必须保证元数据位的单调递增性 (monotonicity)
  // Load Good → Mark Good → Store Good 只能升级不能降级

  for (;;) {
    assert_transition_monotonicity(ptr, heal_ptr);

    // CAS 原子修复指针
    const zpointer prev_ptr = AtomicAccess::cmpxchg(p, ptr, heal_ptr,
                                                      memory_order_relaxed);
    if (prev_ptr == ptr) {
      return;  // 修复成功
    }

    if (fast_path(prev_ptr)) {
      return;  // 其他线程已修复到更好的状态
    }

    // 其他 barrier 已修复但仍需升级, 重试
    ptr = prev_ptr;
  }
}
```

### 4.6 转换单调性 (Transition Monotonicity)

Self-heal 必须遵守严格的单调性规则 -- 指针状态只能升级:

```cpp
// zBarrier.inline.hpp
inline void ZBarrier::assert_transition_monotonicity(zpointer old_ptr,
                                                      zpointer new_ptr) {
  assert(!old_is_load_good  || new_is_load_good,  "non-monotonic load good");
  assert(!old_is_mark_good  || new_is_mark_good,  "non-monotonic mark good");
  assert(!old_is_store_good || new_is_store_good,  "non-monotonic store good");
  assert(!old_is_marked_young || new_is_marked_young, "non-monotonic marked young");
  assert(!old_is_marked_old   || new_is_marked_old,   "non-monotonic marked old");
}
```

### 4.7 nmethod (JIT 编译代码) 中的优化 Load Barrier

对于 JIT 编译的代码, ZGC 使用更激进的优化:

```
来自 zBarrier.hpp 的注释:

nmethod load barrier 将 good-bit 检查和元数据去除合并为一条 shift 指令:
1. 用当前 "good" shift 值移位指针
2. 如果结果为 0 (ZF=1) → null, 正常路径
3. 如果最后移出的位是 1 (CF=1) → good 指针, 正常路径
4. 如果 CF=0 且 ZF=0 → bad 指针, 进入 slow path

这种 speculative 优化利用了大多数指针都是 load-good 的假设。
```

**限制** (来自源码注释):
1. Load barrier 只能识别 4 种不同的 good 模式 (对应 4 个 Remapped 位)
2. 这些位模式必须只有单个位被设置 (single bit set)
3. 进入 slow path 后必须重新加载 oop (因为 shift 后的值已损坏)

---

## 5. Store Barrier (写屏障) -- 分代模式

### 5.1 为什么分代 ZGC 需要写屏障

在非分代 (single-generation) 模式下, ZGC 只需要读屏障。但分代 ZGC 需要追踪 old→young 的跨代引用, 因此引入了 **写屏障** (store barrier)。

### 5.2 Store Barrier 实现

```cpp
// zBarrier.inline.hpp
inline void ZBarrier::store_barrier_on_heap_oop_field(volatile zpointer* p,
                                                       bool heal) {
  const zpointer prev = load_atomic(p);

  auto slow_path = `[=](zaddress addr)` -> zaddress {
    return ZBarrier::heap_store_slow_path(p, addr, prev, heal);
  };

  if (heal) {
    barrier(is_store_good_fast_path, slow_path, color_store_good, p, prev);
  } else {
    barrier(is_store_good_or_null_fast_path, slow_path,
            color_store_good, nullptr, prev);
  }
}
```

**Store barrier 的职责**:
1. **确保前值 (previous value) 被正确处理** -- SATB 快照语义
2. **更新 Remembered Set** -- 如果写入 old 代对象中, 记录跨代引用
3. **标记前值** -- 如果在标记阶段, 确保前值被标记

### 5.3 ZStoreBarrierBuffer

Store barrier 使用一个线程本地缓冲区来延迟处理:

```cpp
// zStoreBarrierBuffer.hpp
class ZStoreBarrierBuffer : public CHeapObj<mtGC> {
  // 收集待处理的 store barrier 操作
  // 批量处理以提高效率
  static ZStoreBarrierBuffer* buffer_for_store(bool heal);
};
```

### 5.4 Remembered Set

Remembered Set 追踪从 old generation 指向 young generation 的引用:

```cpp
// zRemembered.hpp
class ZRemembered {
  ZPageTable* const             _page_table;
  const ZForwardingTable* const _old_forwarding_table;

  // 添加记忆集条目
  void remember(volatile zpointer* p) const;

  // 扫描所有记忆集并追踪
  void scan_and_follow(ZMark* mark);

  // 保存当前记忆集, 切换到空的记忆集
  void flip();

  // 扫描单个记忆集条目
  bool scan_field(volatile zpointer* p) const;
};
```

每个 ZPage 都有自己的 remembered set (位图实现):

```cpp
// zPage.hpp
class ZPage : public CHeapObj<mtGC> {
  ZRememberedSet _remembered_set;  // 位图, 记录哪些 oop* 指向 young 代
  // ...
  void remember(volatile zpointer* p);  // 添加条目
  void swap_remset_bitmaps();            // 双缓冲翻转
};
```

### 5.5 Remember 位的语义

着色指针中的 Remembered 位 (2 bits) 有特殊含义:

```
来自 zBarrier.inline.hpp 的注释:

- 执行 store barrier 时 → heal with 单个 remember 位
- young 标记对象时 → heal with 单个 remember 位
- 非 young 代执行非 store barrier 时 → heal with 双 remember 位
- "remset forget" old 代指针时 → heal with 双 remember 位

双 remember 位确保后续每次 store 都进入 slow path
```

---

## 6. GC 周期详解 -- Young Generation

### 6.1 Young Collection 完整流程

```cpp
// zGeneration.cpp
void ZGenerationYoung::collect(ZYoungType type, ConcurrentGCTimer* timer) {
  // Phase 1: Pause Mark Start          -- STW
  pause_mark_start();

  // Phase 2: Concurrent Mark           -- 并发
  concurrent_mark();

  // Phase 3: Pause Mark End            -- STW
  while (!pause_mark_end()) {
    // Phase 3.5: Concurrent Mark Continue  -- 并发 (如果标记未完成)
    concurrent_mark_continue();
  }

  // Phase 4: Concurrent Mark Free      -- 并发
  concurrent_mark_free();

  // Phase 5: Concurrent Reset Relocation Set  -- 并发
  concurrent_reset_relocation_set();

  // Phase 6: Concurrent Select Relocation Set -- 并发
  concurrent_select_relocation_set();

  // Phase 7: Pause Relocate Start      -- STW
  pause_relocate_start();

  // Phase 8: Concurrent Relocate       -- 并发
  concurrent_relocate();
}
```

### 6.2 各阶段详解

```
时间线:
──┬──────────┬───────────────────────┬──────────┬──────────────────
  │ STW <1ms │     Concurrent        │ STW <1ms │   Concurrent
  │          │                       │          │
  │ Pause    │  Concurrent Mark      │ Pause    │  Concurrent
  │ Mark     │  ├─ Mark Roots        │ Mark     │  Mark Free
  │ Start    │  └─ Mark Follow       │ End      │
  │          │                       │          │
──┴──────────┴───────────────────────┴──────────┴──────────────────

──────────────────────┬──────────────────────┬──────────┬──────────
    Concurrent        │     Concurrent       │ STW <1ms │ Concurrent
                      │                      │          │
    Reset Relocation  │  Select Relocation   │ Pause    │ Concurrent
    Set               │  Set                 │ Relocate │ Relocate
                      │  (选择要回收的页面)    │ Start    │
                      │                      │          │
──────────────────────┴──────────────────────┴──────────┴──────────
```

**Phase 1: Pause Mark Start (STW)**

```cpp
void ZGenerationYoung::pause_mark_start() {
  // 触发 safepoint, 执行 VM_ZMarkStartYoung 或 VM_ZMarkStartYoungAndOld
  // 如果是 Major GC, 同时启动 Old 代标记
}

// 在 safepoint 中:
void VM_ZMarkStartYoung::do_operation() {
  ZCollectedHeap::heap()->increment_total_collections(false);
  ZGeneration::young()->mark_start();
  // mark_start() 内部:
  //   1. flip_mark_start() -- 翻转 Remapped 位的 "good" 定义
  //   2. ZBarrierSet::assembler()->patch_barriers() -- 更新 JIT 代码中的 barrier
}
```

**Phase 2: Concurrent Mark**

```cpp
void ZGenerationYoung::concurrent_mark() {
  mark_roots();   // 从 GC roots 开始标记
  mark_follow();  // 遍历对象图, 标记所有可达对象
}
```

**Phase 3: Pause Mark End (STW)**

```cpp
bool ZGenerationYoung::pause_mark_end() {
  // 在 safepoint 中尝试终止标记
  // 如果还有未处理的标记工作, 返回 false → 继续 concurrent_mark_continue()
  return ZGeneration::young()->mark_end();
}
```

**Phase 7: Pause Relocate Start (STW)**

```cpp
void ZGenerationYoung::pause_relocate_start() {
  // 翻转 Relocate 位
  // flip_relocate_start() → ZGlobalsPointers::flip_young_relocate_start()
  // 更新 barrier 使所有旧地址变为 "bad"
}
```

### 6.3 Young Collection 类型

Young GC 有多种子类型, 取决于是否配合 Major GC:

```cpp
// zGeneration.hpp
enum class ZYoungType {
  minor,                  // 独立的 Minor GC
  major_full_preclean,    // Major GC 预清理 (提升所有到 old)
  major_full_roots,       // Major GC 收集根 (含预清理后)
  major_partial_roots,    // Major GC 收集根 (无预清理)
  none
};
```

---

## 7. GC 周期详解 -- Old Generation

### 7.1 Old Collection 完整流程

Old generation 的收集更复杂, 包含更多阶段:

```cpp
// zGeneration.cpp
void ZGenerationOld::collect(ConcurrentGCTimer* timer) {
  // Phase 1: Concurrent Mark                      -- 并发
  concurrent_mark();

  // Phase 2: Pause Mark End                       -- STW
  while (!pause_mark_end()) {
    // Phase 2.5: Concurrent Mark Continue         -- 并发
    concurrent_mark_continue();
  }

  // Phase 3: Concurrent Mark Free                 -- 并发
  concurrent_mark_free();

  // Phase 4: Concurrent Process Non-Strong Refs   -- 并发
  concurrent_process_non_strong_references();

  // Phase 5: Concurrent Reset Relocation Set      -- 并发
  concurrent_reset_relocation_set();

  // Phase 6: Pause Verify                         -- STW (仅调试)
  pause_verify();

  // Phase 7: Concurrent Select Relocation Set     -- 并发
  concurrent_select_relocation_set();

  // Phase 8: Concurrent Remap Young Roots         -- 并发 (持有 driver lock)
  concurrent_remap_young_roots();

  // Phase 9: Pause Relocate Start                 -- STW
  pause_relocate_start();

  // Phase 10: Concurrent Relocate                 -- 并发
  concurrent_relocate();
}
```

### 7.2 Old Generation 特有阶段

**Concurrent Process Non-Strong References**:

```cpp
// Old 代独有: 处理 weak/soft/phantom 引用和类卸载
void ZGenerationOld::concurrent_process_non_strong_references() {
  process_non_strong_references();
  // 内部调用:
  //   ZReferenceProcessor  -- 处理 Java Reference 对象
  //   ZWeakRootsProcessor  -- 处理弱根
  //   ZUnload              -- 并发类卸载
}
```

**Concurrent Remap Young Roots**:

```cpp
// Old 代独有: 在 old relocate 前重映射 young 代的根引用
void ZGenerationOld::concurrent_remap_young_roots() {
  remap_young_roots();
  // 确保所有 young 代的根指针在 old relocate 前是正确的
  // 这个阶段持有 ZDriverLocker, 阻止 young GC 同时运行
}
```

### 7.3 Major Collection 协调

Major GC 由 `ZDriverMajor` 驱动, 它协调 Young 和 Old 代:

```cpp
// zDriver.cpp
void ZDriverMajor::gc(const ZDriverRequest& request) {
  ZDriverScopeMajor scope(request, &_gc_timer);

  // 第一步: 收集 young generation
  collect_young(request);

  // 第二步: 收集 old generation
  collect_old();
}

void ZDriverMajor::collect_young(const ZDriverRequest& request) {
  if (should_preclean_young(request.cause())) {
    // 先预清理: 提升所有 young 对象到 old
    ZGeneration::young()->collect(ZYoungType::major_full_preclean, &_gc_timer);
    // 再收集根
    ZGeneration::young()->collect(ZYoungType::major_full_roots, &_gc_timer);
  } else {
    // 直接收集根
    ZGeneration::young()->collect(ZYoungType::major_partial_roots, &_gc_timer);
  }
}
```

### 7.4 GC 触发原因

```cpp
// zDriver.cpp -- 不同原因触发不同类型的 GC

// Minor GC 触发原因:
case GCCause::_z_timer:               // 定时器触发
case GCCause::_z_allocation_rate:     // 分配速率过高
case GCCause::_z_allocation_stall:    // 分配阻塞
case GCCause::_z_high_usage:          // 使用率过高

// Major GC 触发原因 (同步):
case GCCause::_java_lang_system_gc:   // System.gc()
case GCCause::_heap_dump:             // jmap -dump
case GCCause::_wb_full_gc:            // 白盒测试
case GCCause::_jvmti_force_gc:       // JVMTI
case GCCause::_metadata_GC_clear_soft_refs:

// Major GC 触发原因 (异步):
case GCCause::_z_timer:              // 定时器
case GCCause::_z_warmup:             // 预热
case GCCause::_z_allocation_rate:    // 分配速率
case GCCause::_z_allocation_stall:   // 分配阻塞
case GCCause::_z_proactive:          // 主动回收
case GCCause::_metadata_GC_threshold:
```

### 7.5 Soft Reference 清理策略

```cpp
// zDriver.cpp
static bool should_clear_all_soft_references(GCCause::Cause cause) {
  switch (cause) {
  case GCCause::_wb_full_gc:
  case GCCause::_metadata_GC_clear_soft_refs:
  case GCCause::_z_allocation_stall:        // 分配阻塞时清理所有 soft refs
    return true;
  // ...
  }
  // 如果线程因等待 old collection 而阻塞, 也清理
  if (ZHeap::heap()->is_alloc_stalling_for_old()) {
    return true;
  }
  return false;
}
```

---

## 8. 分代 ZGC (Generational ZGC)

### 8.1 为什么需要分代

非分代 ZGC 每次 GC 都扫描整个堆, 包括标记所有存活对象。对于大堆, 标记阶段的 CPU 开销可观。分代设计利用 **弱分代假说** (Weak Generational Hypothesis):

- 大多数对象在创建后很快死亡 (infant mortality)
- 频繁 Minor GC 只扫描 young 代 (通常较小), 开销低
- 不频繁 Major GC 才扫描 old 代, 减少总体标记工作量

### 8.2 架构

```cpp
// zGeneration.hpp -- 分代类层次

class ZGeneration {                          // 抽象基类
  Phase                 _phase;              // Mark / MarkComplete / Relocate
  ZMark                 _mark;               // 标记器
  ZRelocate             _relocate;           // 重定位器
  ZRelocationSet        _relocation_set;     // 重定位集合
  ZWorkers              _workers;            // GC 工作线程
};

class ZGenerationYoung : public ZGeneration {
  ZYoungType   _active_type;                 // minor / major_full_preclean / ...
  uint         _tenuring_threshold;          // 晋升阈值
  ZRemembered  _remembered;                  // 记忆集管理
  // 独有方法:
  void flip_promote(ZPage* from_page, ZPage* to_page);
  void register_flip_promoted(const ZArray<ZPage*>& pages);
  void remember(volatile zpointer* p);       // 添加记忆集条目
  void scan_remembered_field(volatile zpointer* p);
};

class ZGenerationOld : public ZGeneration {
  ZReferenceProcessor _reference_processor;  // Reference 处理
  ZWeakRootsProcessor _weak_roots_processor; // 弱根处理
  ZUnload             _unload;               // 并发类卸载
  // 独有方法:
  void process_non_strong_references();
  void remap_young_roots();
};
```

### 8.3 Young 与 Old 的独立 GC 周期

分代 ZGC 中, Young 和 Old 代有独立的 GC 驱动线程:

```cpp
// zDriver.cpp
class ZDriverMinor : public ZDriver {      // 驱动 Young GC
  void gc(const ZDriverRequest& request) {
    ZGeneration::young()->collect(ZYoungType::minor, &_gc_timer);
  }
};

class ZDriverMajor : public ZDriver {      // 驱动 Old GC (含 Young 预处理)
  void gc(const ZDriverRequest& request) {
    collect_young(request);  // 先处理 young
    collect_old();           // 再处理 old
  }
};
```

### 8.4 对象提升 (Promotion)

对象从 young 代提升到 old 代有两种方式:

```cpp
// zGeneration.hpp
class ZGenerationYoung : public ZGeneration {
  // 翻转提升: 整个 page 从 young 变为 old
  void flip_promote(ZPage* from_page, ZPage* to_page);

  // 原地重定位提升: 在重定位过程中提升
  void in_place_relocate_promote(ZPage* from_page, ZPage* to_page);

  // 动态计算晋升阈值
  uint compute_tenuring_threshold(ZRelocationSetSelectorStats stats);
};
```

### 8.5 并发性保证

Young GC 和 Old GC 可以交替运行, 但某些关键阶段需要互斥:

```cpp
// zDriver.cpp -- Old GC 的 remap_young_roots 和 relocate_start 需要持有锁
void ZGenerationOld::collect(ConcurrentGCTimer* timer) {
  // ...
  {
    ZDriverLocker locker;                    // 阻止 young GC 同时运行
    concurrent_remap_young_roots();          // 重映射 young 根
    pause_relocate_start();                  // STW: 开始重定位
  }
  concurrent_relocate();                     // 释放锁后并发重定位
}
```

---

## 9. JEP 演进历史

| JEP | JDK | 状态 | 内容 |
|-----|-----|------|------|
| **JEP 333** | JDK 11 | Experimental | ZGC 首次引入, 仅 Linux/x64, 实验性 |
| **JEP 351** | JDK 13 | -- | 支持 uncommit 未使用内存归还 OS |
| **JEP 364** | JDK 14 | -- | 支持 macOS |
| **JEP 365** | JDK 14 | -- | 支持 Windows |
| **JEP 377** | JDK 15 | Production | ZGC 正式成为生产就绪 (production-ready) |
| **JEP 376** | JDK 15 | -- | ZGC 并发线程栈处理 (消除最后的栈扫描 STW) |
| **JEP 439** | JDK 21 | -- | 分代 ZGC (Generational ZGC) 引入 |
| **JEP 474** | JDK 23 | -- | 分代 ZGC 成为默认模式 (-XX:+UseZGC 即为分代) |
| **JEP 490** | JDK 24 | -- | 移除非分代 ZGC (non-generational ZGC 被删除) |

### 关键里程碑

**JDK 11 (JEP 333)**: 初始实现
- 单代 (single generation), 仅 Linux/x64
- 核心技术: 着色指针 + 读屏障 + 并发标记/重定位
- 需要 `-XX:+UnlockExperimentalVMOptions -XX:+UseZGC`

**JDK 15 (JEP 377)**: 生产就绪
- 移除 Experimental 标记
- 仅需 `-XX:+UseZGC`
- 解决了与 Compressed Oops 的兼容性问题

**JDK 21 (JEP 439)**: 分代引入
- Young / Old 两代独立 GC
- 引入写屏障 (store barrier) 和 remembered set
- 需要 `-XX:+UseZGC -XX:+ZGenerational`
- 显著减少大堆场景下的标记开销

**JDK 23 (JEP 474)**: 分代成为默认
- `-XX:+UseZGC` 直接启用分代模式
- 非分代模式需要 `-XX:+UseZGC -XX:-ZGenerational`

**JDK 24 (JEP 490)**: 非分代移除
- 彻底移除非分代 ZGC 代码
- `-XX:+UseZGC` 是唯一选项, 无需额外标志

---

## 10. 关键调优参数

### 10.1 基础配置

```bash
# 启用 ZGC (JDK 24+ 自动为分代模式)
-XX:+UseZGC

# JDK 21-22: 显式启用分代模式
-XX:+UseZGC -XX:+ZGenerational

# 堆大小
-Xms4g -Xmx16g

# 软最大堆大小 -- ZGC 的核心调优参数
# ZGC 会尝试将堆使用量控制在此值以下
# 但在需要时可以增长到 -Xmx
-XX:SoftMaxHeapSize=12g
```

### 10.2 GC 触发控制

```bash
# 分配尖刺容忍度 (默认 2.0)
# 值越大, ZGC 越保守 (更早触发 GC)
-XX:ZAllocationSpikeTolerance=2.0

# 定时 GC 间隔 (秒, 默认 0 = 禁用)
# 设置后, ZGC 会周期性执行 GC, 即使没有内存压力
# 有助于保持 RSS 较低
-XX:ZCollectionInterval=300
```

### 10.3 内存管理

```bash
# 未使用内存归还 OS 的延迟 (秒, 默认 300)
-XX:ZUncommitDelay=300

# GC 线程数
-XX:ParallelGCThreads=4       # STW 阶段的并行线程数
-XX:ConcGCThreads=2           # 并发阶段的 GC 线程数
# 通常 ZGC 会自动选择合适的线程数, 无需手动设置

# NUMA 支持 (自动检测并启用)
-XX:+UseNUMA
```

### 10.4 Large Pages (大页) 配置

```bash
# 透明大页 (推荐)
-XX:+UseTransparentHugePages

# 或显式大页 (需要 OS 配置)
-XX:+UseLargePages
```

### 10.5 参数总结表

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-XX:+UseZGC` | -- | 启用 ZGC |
| `-XX:SoftMaxHeapSize` | = -Xmx | 软最大堆, GC 努力保持使用量在此以下 |
| `-XX:ZAllocationSpikeTolerance` | 2.0 | 分配尖刺容忍度, 越大越早触发 GC |
| `-XX:ZCollectionInterval` | 0 (禁用) | 强制 GC 间隔 (秒) |
| `-XX:ZUncommitDelay` | 300 | 内存归还 OS 延迟 (秒) |
| `-XX:ParallelGCThreads` | auto | STW 并行线程数 |
| `-XX:ConcGCThreads` | auto | 并发 GC 线程数 |

---

## 11. 性能特性与对比

### 11.1 亚毫秒暂停

ZGC 的核心承诺: **STW 暂停时间不随堆大小增长**。

3 个 STW 暂停点 (young GC):
- **Pause Mark Start**: 翻转颜色位, 更新 barrier
- **Pause Mark End**: 终止标记 (如果未完成则重试)
- **Pause Relocate Start**: 翻转重定位位

每个暂停通常在 **O(1)** 时间内完成 (不依赖堆大小或存活对象数量)。

### 11.2 支持的堆大小范围

- **最小**: 几百 MB (但小堆场景 G1 可能更合适)
- **最大**: 多 TB 级别 (16TB 理论上限, 取决于平台)
- **最佳适用**: 中大堆 (8GB+), 对延迟敏感的应用

### 11.3 吞吐量代价

ZGC 的并发设计带来一定的吞吐量代价:

1. **Barrier 开销**: 每次对象引用加载/存储都有 barrier 检查
   - Load barrier: 检查 Remapped 位 (极轻量)
   - Store barrier (分代模式): 检查并可能更新 remembered set
2. **并发 GC 线程**: 与应用争抢 CPU 资源
3. **内存开销**: 着色指针需要额外的虚拟地址空间

**典型吞吐量影响**: 相比 G1, ZGC 吞吐量可能低 5-15%, 但分代 ZGC (JDK 21+) 显著缩小了这个差距。

### 11.4 ZGC vs G1 vs Shenandoah

| 维度 | ZGC | G1 | Shenandoah |
|------|-----|-----|------------|
| **设计目标** | 超低延迟 | 平衡延迟/吞吐 | 低延迟 |
| **暂停时间** | <1ms (不随堆增长) | 10-500ms (与堆大小相关) | <10ms (不随堆增长) |
| **暂停次数/GC周期** | 3 次 STW | 多次 STW (包含 mixed GC) | 2-3 次 STW |
| **堆大小适用** | 中大堆 (8GB-TB级) | 中堆 (4-64GB) | 中大堆 (4GB-TB级) |
| **吞吐量** | 中等 | 高 | 中等 |
| **核心技术** | 着色指针 + 读屏障 | 写屏障 + SATB | Mark Word 转发 + 读屏障 (LRB) |
| **分代支持** | JDK 21+ | 始终分代 | JDK 21+ (实验), JDK 25 (正式) |
| **内存开销** | 中等 (额外虚拟地址) | 较低 | 中等 (remembered sets) |
| **CompressedOops** | 不支持 (显式禁用) | 支持 | 支持 |
| **JDK 状态** | Production (JDK 15+) | 默认 GC | Experimental→Production |

### 11.5 何时选择 ZGC

**推荐 ZGC**:
- 延迟敏感的在线服务 (P99 延迟要求严格)
- 大堆应用 (8GB+)
- 堆大小可能变化的云原生应用 (利用 SoftMaxHeapSize)
- 需要亚毫秒级 GC 暂停的场景

**不推荐 ZGC**:
- 堆很小 (<2GB) 且吞吐量优先
- 批处理 / 离线计算 (吞吐量优先 → 考虑 G1 或 Parallel GC)
- CPU 资源极度受限 (ZGC 并发线程需要 CPU)

---

## 12. 诊断与故障排除

### 12.1 GC 日志配置

```bash
# 基础 GC 日志
-Xlog:gc:file=gc.log:time,uptime,level,tags

# 详细 GC 日志 (含各阶段耗时)
-Xlog:gc*:file=gc.log:time,uptime,level,tags

# 重点关注的 tag 组合
-Xlog:gc,gc+phases:file=gc.log:time,uptime,level,tags

# 堆使用详情
-Xlog:gc+heap=debug:file=gc.log

# 暂停时间详情
-Xlog:gc+phases=debug:file=gc.log

# 完整调试日志 (会产生大量输出)
-Xlog:gc*=debug:file=gc-debug.log:time,uptime,level,tags:filecount=10,filesize=100m
```

### 12.2 典型日志输出解读

```
[info][gc] GC(3) Minor Collection (Allocation Rate)
[info][gc,phases] GC(3) Y: Pause Mark Start 0.015ms
[info][gc,phases] GC(3) Y: Concurrent Mark 12.345ms
[info][gc,phases] GC(3) Y: Pause Mark End 0.008ms
[info][gc,phases] GC(3) Y: Concurrent Mark Free 0.123ms
[info][gc,phases] GC(3) Y: Concurrent Reset Relocation Set 0.045ms
[info][gc,phases] GC(3) Y: Concurrent Select Relocation Set 1.234ms
[info][gc,phases] GC(3) Y: Pause Relocate Start 0.012ms
[info][gc,phases] GC(3) Y: Concurrent Relocate 5.678ms
[info][gc] GC(3) Minor Collection (Allocation Rate) 128M(12%)->96M(9%)
```

关键指标:
- **Pause Mark Start / End / Relocate Start**: 这三个暂停时间应在 1ms 以内
- **Minor Collection vs Major Collection**: Minor = Young GC, Major = Young + Old GC
- **Allocation Rate**: 表明此次 GC 由分配速率触发

### 12.3 JFR 事件

ZGC 发出的 JFR (Java Flight Recorder) 事件:

```
jdk.ZYoungGarbageCollection    -- Young GC 完成
jdk.ZOldGarbageCollection      -- Old GC 完成
jdk.GCPhasePause               -- STW 暂停详情
jdk.GCPhaseConcurrent          -- 并发阶段详情
```

```bash
# 使用 JFR 记录 GC 事件
java -XX:+UseZGC \
     -XX:StartFlightRecording=filename=recording.jfr,duration=60s \
     -jar app.jar
```

### 12.4 常见问题与解决

**问题 1: 分配阻塞 (Allocation Stall)**

症状: 日志出现 `GCCause::_z_allocation_stall`

```
[warning][gc] Allocation Stall (main) 45.234ms
```

原因: GC 回收速度跟不上分配速度

解决:
- 增加堆大小 (`-Xmx`)
- 增加 GC 线程 (`-XX:ConcGCThreads`)
- 降低 `ZAllocationSpikeTolerance` (更早触发 GC)
- 检查应用是否存在内存泄漏

**问题 2: 暂停时间异常**

症状: STW 暂停 > 1ms

排查:
```bash
-Xlog:gc+phases=debug:file=gc.log
# 查看具体是哪个暂停阶段耗时长
# 如果是 Pause Mark End 反复重试 → concurrent_mark_continue 被反复调用
# → 应用在标记期间产生了大量新引用, 标记跟不上
```

解决:
- 增加并发 GC 线程
- 检查是否有大量 finalizer 或 weak reference 处理

**问题 3: RSS (Resident Set Size) 过高**

原因: ZGC 在虚拟地址空间中使用多重映射

解决:
- 调低 `-XX:ZUncommitDelay` (更快归还未使用内存)
- 设置 `-XX:SoftMaxHeapSize` (引导 ZGC 保持较低堆使用)
- 使用 `-XX:ZCollectionInterval` 触发定期 GC

---

## 13. 源码结构

### 13.1 核心文件清单

```
src/hotspot/share/gc/z/   (~237 个文件)

堆管理:
├── zCollectedHeap.hpp/cpp      CollectedHeap 子类, JVM 入口
├── zHeap.hpp/cpp               ZGC 堆实现, 持有 PageAllocator/PageTable/Generations
├── zPage.hpp/cpp               Page 抽象: small/medium/large
├── zPageType.hpp               Page 类型枚举
├── zPageAge.hpp                Page 年龄 (eden → survivor1-14 → old)
├── zPageAllocator.hpp/cpp      物理/虚拟内存管理, Page 分配/回收
├── zPageTable.hpp/cpp          Page 查找表
├── zGlobals.hpp                全局常量 (granule 大小/page 大小等)

着色指针:
├── zAddress.hpp/cpp            指针布局定义, 着色/去色操作
├── zAddress.inline.hpp         内联实现

屏障:
├── zBarrier.hpp/cpp            核心 Barrier 逻辑 (load/store/mark)
├── zBarrier.inline.hpp         Barrier 内联实现 (fast path + slow path)
├── zBarrierSet.hpp/cpp         BarrierSet 子类, JVM 屏障接口
├── zBarrierSetAssembler.hpp    JIT 代码中的 barrier 补丁
├── zBarrierSetNMethod.hpp      nmethod entry barrier
├── zBarrierSetRuntime.hpp      Runtime barrier 入口
├── zStoreBarrierBuffer.hpp     Store barrier 延迟处理缓冲

分代:
├── zGeneration.hpp/cpp         Generation 基类 + Young/Old 子类
├── zGenerationId.hpp           Generation ID 枚举 (young/old)
├── zRemembered.hpp/cpp         记忆集管理 (old→young 引用追踪)
├── zRememberedSet.hpp          Per-page 记忆集 (位图)

标记:
├── zMark.hpp/cpp               并发标记实现
├── zLiveMap.hpp                Per-page 存活对象位图

重定位:
├── zRelocate.hpp/cpp           并发重定位实现
├── zRelocationSet.hpp/cpp      重定位集合 (要回收的 page 集合)
├── zRelocationSetSelector.hpp  选择要回收的 page 的策略
├── zForwarding.hpp/cpp         转发表 (旧地址 → 新地址映射)
├── zForwardingTable.hpp        转发表查找

引用处理:
├── zReferenceProcessor.hpp/cpp 处理 Weak/Soft/Phantom Reference
├── zWeakRootsProcessor.hpp     处理弱根
├── zUnload.hpp/cpp             并发类卸载

GC 驱动:
├── zDriver.hpp/cpp             GC 驱动线程 (Minor/Major)
├── zDirector.hpp/cpp           GC 决策调度 (100Hz 评估)

平台相关:
├── c1/                         C1 编译器 barrier 生成
├── c2/                         C2 编译器 barrier 生成
└── (CPU_HEADER)                平台特定实现 (x86/aarch64)
```

### 13.2 关键调用链

**对象加载时**:
```
应用代码 oop_load
  → ZBarrierSet::AccessBarrier::oop_load_in_heap()
    → ZBarrier::load_barrier_on_oop_field_preloaded()
      → fast_path: ZPointer::is_load_good_or_null()  → 直接返回
      → slow_path: make_load_good() → relocate_or_remap()
      → self_heal() → CAS 修复指针
```

**对象存储时 (分代模式)**:
```
应用代码 oop_store
  → ZBarrierSet::AccessBarrier::oop_store_in_heap()
    → store_barrier_heap_with_healing()
      → ZBarrier::store_barrier_on_heap_oop_field()
        → fast_path: ZPointer::is_store_good()  → 直接写入
        → slow_path: heap_store_slow_path()
          → 标记前值 (SATB)
          → 更新 remembered set (如果 old→young)
        → self_heal()
    → 写入新值 (store_good 着色)
```

**Minor GC 周期**:
```
ZDirector::evaluate_rules()  [100Hz 评估]
  → ZDriverMinor::collect(request)
    → ZDriverMinor::gc(request)
      → ZGenerationYoung::collect(ZYoungType::minor)
        → pause_mark_start()        [STW: flip 颜色位]
        → concurrent_mark()         [并发: 标记存活对象]
        → pause_mark_end()          [STW: 终止标记]
        → concurrent_mark_free()    [并发: 释放无存活对象的 page]
        → concurrent_reset_relocation_set()
        → concurrent_select_relocation_set()
        → pause_relocate_start()    [STW: flip 重定位位]
        → concurrent_relocate()     [并发: 移动对象]
```

---

## 推荐阅读

- [G1 GC 深入](g1-gc.md) — 最广泛使用的 GC，与 ZGC 对比选型的基准
- [Shenandoah GC](shenandoah.md) — 另一款低暂停 GC，并发策略与 ZGC 不同
- [G1 vs ZGC vs Shenandoah 对比](/guides/comparisons/g1-vs-zgc-vs-shenandoah.md) — 三大 GC 全面对比指南
- [GC 调优实践](tuning.md) — GC 参数调优案例与最佳实践
- [内存管理主题](../memory/) — 堆外内存、Metaspace 等内存管理全景
