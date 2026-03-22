# CMS (Concurrent Mark Sweep) GC 详解

> HotSpot 第一个并发垃圾收集器：架构、原理、核心问题与历史遗产

[← 返回 GC](../)

---

## 1. CMS 概述与历史地位

### 1.1 什么是 CMS

CMS (Concurrent Mark Sweep) 是 HotSpot JVM 中第一个实现了**并发回收 (Concurrent Collection)** 的垃圾收集器。它的设计目标是**最小化老年代 GC 停顿时间 (STW pause)**，通过让大部分标记和清除工作与应用线程并发执行来实现这一目标。

```
启用方式: -XX:+UseConcMarkSweepGC
回收目标: 仅老年代 (Old Generation)
配合新生代: ParNew (并行复制收集器)
回收算法: Mark-Sweep (标记-清除，不压缩)
```

### 1.2 历史时间线

| 时间 | 版本 | 事件 |
|------|------|------|
| 2003 | JDK 1.4.2 | CMS 正式引入 HotSpot，成为第一个并发 GC |
| 2006 | JDK 6 | CMS 成为服务端应用的主流选择 |
| 2012 | JDK 7u4 | G1 GC 正式可用 |
| 2017 | JDK 9 | **JEP 291**: CMS 被废弃 (Deprecated) |
| 2017 | JDK 9 | G1 成为默认 GC (JEP 248)，CMS 继续可用但不推荐 |
| 2020 | JDK 14 | **JEP 363**: CMS 源码被完全移除 |

### 1.3 为什么 CMS 重要

尽管 CMS 已被移除，它在 GC 历史上的地位不可替代：

1. **开创并发回收范式** — CMS 证明了"在应用运行的同时回收垃圾"是可行的，后续所有低延迟 GC (G1、ZGC、Shenandoah) 都沿袭了这一思路
2. **Write Barrier 的先驱** — CMS 的 Card Marking write barrier 机制被 G1 继承并发展为 Remembered Set + SATB barrier
3. **教训驱动设计** — CMS 暴露的碎片化、Concurrent Mode Failure 等问题直接推动了 G1 的 Region 化设计和 Mixed GC 策略
4. **工业界广泛使用** — 在 JDK 6-8 时代，大量 Java 服务（特别是低延迟交易系统、Web 服务）使用 CMS

---

## 2. 堆布局 — 传统分代

CMS 使用传统的**物理连续分代 (Generational)** 堆布局，与 G1 的 Region 化布局截然不同。

### 2.1 堆结构概览

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       JVM Heap (传统分代布局)                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────────────────┐  ┌──────────────────────────────────┐ │
│  │        Young Generation       │  │         Old Generation           │ │
│  │     (ParNew 负责回收)          │  │        (CMS 负责回收)             │ │
│  │                               │  │                                  │ │
│  │  ┌───────┬───────┬───────┐   │  │  ┌──────────────────────────┐   │ │
│  │  │ Eden  │  S0   │  S1   │   │  │  │   Free-List 管理的连续空间  │   │ │
│  │  │       │(From) │ (To)  │   │  │  │   (Mark-Sweep, 不压缩)    │   │ │
│  │  └───────┴───────┴───────┘   │  │  └──────────────────────────┘   │ │
│  └──────────────────────────────┘  └──────────────────────────────────┘ │
│                                                                         │
│  ┌──────────────────────────────┐                                       │
│  │  Permanent Generation         │  ← JDK 7 及之前                      │
│  │  或 Metaspace (本地内存)       │  ← JDK 8+                           │
│  └──────────────────────────────┘                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 各区域职责

| 区域 | GC 收集器 | 回收方式 | 说明 |
|------|-----------|---------|------|
| Eden | ParNew (STW) | 复制 (Copying) | 新对象分配，满时触发 Young GC |
| S0 / S1 | ParNew (STW) | 复制 (Copying) | 交替作为 From/To，存活对象在此老化 |
| Old | CMS (Mostly Concurrent) | 标记-清除 (Mark-Sweep) | 长寿对象，CMS 并发回收 |
| Perm / Metaspace | Full GC (Serial Old) | 标记-压缩 | 类元数据、常量池等 |

### 2.3 CMS 只管理老年代

这是理解 CMS 的关键点：

- **Young GC 仍然是 STW 的** — 由 ParNew 收集器执行，使用多线程并行复制算法
- **CMS 仅负责老年代** — 当老年代占用率 (occupancy) 达到阈值时触发
- **CMS 不处理新生代** — 新生代对象不在 CMS 的回收范围内

```
应用分配对象
    │
    ▼
  Eden 满了?
    │ YES
    ▼
  ParNew Young GC (STW)  ── 存活对象 → Survivor
    │                        │
    │                        │ 对象年龄达到阈值
    │                        ▼
    │                     晋升 (Promote) → Old Generation
    │
    ▼
  Old 占用率 > 阈值?
    │ YES
    ▼
  CMS Concurrent Collection  ── 并发标记 + 并发清除
```

### 2.4 老年代的空闲空间管理 — Free List

由于 CMS 使用 Mark-Sweep（不压缩），老年代的空闲空间不是一个连续的区域，而是由 **Free List (空闲链表)** 管理的多个碎片。

```
Old Generation (Mark-Sweep 后):

┌────────┬──────┬────────────┬──────┬──────────┬──────┬───────────┐
│ 存活A   │ 空闲  │  存活B      │ 空闲  │  存活C    │ 空闲  │  存活D     │
│ 256KB  │ 64KB │  512KB     │ 32KB │  128KB   │ 1MB  │  384KB    │
└────────┴──────┴────────────┴──────┴──────────┴──────┴───────────┘
           │                   │                  │
           └───────────────────┴──────────────────┘
                    Free List (空闲链表连接各碎片)

问题: 如果需要分配 100KB 的对象，虽然总空闲空间 > 100KB，
      但最大的连续空闲块可能不足 100KB → 分配失败 → Full GC!
```

这就是 CMS 最致命的设计缺陷 — **碎片化 (Fragmentation)**。

---

## 3. GC 周期 — CMS 的 7 个阶段

CMS 的一次完整回收周期包含 7 个阶段，其中只有 2 个需要 Stop-the-World (STW)。

### 3.1 周期总览

```
         应用线程运行状态
         ─────────────────────────────────────────────────────────
  时间 → ██████░░██████████████████████████████████░░██████████████

         │    │  │                                │  │
         │    │  │      并发阶段 (应用线程继续运行)    │  │
         │    │  │                                │  │
         │  STW1 │                              STW2 │
         │    │  │                                │  │
         ▼    ▼  ▼                                ▼  ▼

  ┌──────────┐ ┌──────────────┐ ┌────────────┐ ┌──────────────┐
  │ 1. Init  │ │ 2. Concurrent│ │3. Conc     │ │4. Conc       │
  │   Mark   │ │    Mark      │ │  Preclean  │ │  Abortable   │
  │  (STW)   │ │              │ │            │ │  Preclean    │
  └──────────┘ └──────────────┘ └────────────┘ └──────────────┘

  ┌──────────┐ ┌──────────────┐ ┌────────────┐
  │ 5. Final │ │ 6. Concurrent│ │7. Conc     │
  │  Remark  │ │    Sweep     │ │   Reset    │
  │  (STW)   │ │              │ │            │
  └──────────┘ └──────────────┘ └────────────┘
```

### 3.2 阶段详解

#### Phase 1: Initial Mark (初始标记) — STW

```
暂停时间: 通常 < 几毫秒
并行度:   单线程 (JDK 7 前) / 多线程 (JDK 8+, -XX:+CMSParallelInitialMarkEnabled)
```

**目标**: 标记 GC Roots 直接引用的老年代对象。

GC Roots 包括：
- 线程栈帧中的局部变量 (Stack Frames)
- 静态变量 (Static Fields)
- JNI 引用 (JNI References)
- 新生代中引用老年代的对象 (Young → Old 引用)

```
GC Roots
  │
  ├── Thread Stack → OldObj_A  ← 标记
  ├── Static Field → OldObj_B  ← 标记
  └── Young Gen    → OldObj_C  ← 标记
                       │
                       └── OldObj_D  ← 不标记 (Phase 2 处理)
```

由于只标记直接引用（不递归遍历），这个阶段非常快速。

#### Phase 2: Concurrent Mark (并发标记)

```
暂停时间: 0 (并发执行)
持续时间: 取决于存活对象图大小，可能几百毫秒到数秒
```

**目标**: 从 Phase 1 标记的根对象出发，**并发遍历整个对象图**，标记所有可达对象。

这是 CMS 最核心的阶段，也是耗时最长的阶段。GC 线程与应用线程同时运行。

**问题**: 由于应用线程在并发执行，对象引用关系可能在标记过程中发生变化：

```
并发标记开始时:          并发标记期间应用线程修改引用:

   A → B → C               A → B ─×─ C    (A.field = null, B 不再引用 C)
                            A ──────→ D    (A.field2 = new D(), 新增引用)
```

CMS 使用 **Incremental Update (增量更新)** 写屏障来处理这个问题：当应用线程修改引用时，通过 write barrier 将被修改的 card 标记为 dirty。

```
Card Table (卡表):
┌───┬───┬───┬───┬───┬───┬───┬───┐
│ 0 │ 0 │ 1 │ 0 │ 1 │ 0 │ 0 │ 0 │  1 = dirty card (引用被修改)
└───┴───┴───┴───┴───┴───┴───┴───┘
每个 card 覆盖 512 字节的堆内存
```

#### Phase 3: Concurrent Preclean (并发预清理)

```
暂停时间: 0 (并发执行)
```

**目标**: 处理 Phase 2 期间产生的 dirty cards，重新扫描被修改的区域。

这个阶段的目的是**减轻 Final Remark 阶段的工作量**。通过提前处理 dirty cards，可以缩短后续 STW 暂停的时间。

```
Preclean 工作流程:

1. 扫描 Card Table，找到所有 dirty cards
2. 对每个 dirty card 覆盖的内存区域重新扫描
3. 标记新发现的可达对象
4. 清除 card 的 dirty 标记
```

#### Phase 4: Concurrent Abortable Preclean (可中止的并发预清理)

```
暂停时间: 0 (并发执行)
持续条件: 直到 Eden 占用率达到 CMSScheduleRemarkEdenPenetration (默认 50%)
超时时间: CMSMaxAbortablePrecleanTime (默认 5 秒)
```

**目标**: 继续处理 dirty cards，同时**等待一次 Young GC 发生**。

为什么要等待 Young GC？因为 Final Remark 阶段需要扫描新生代中指向老年代的引用。如果在 Final Remark 前刚好发生了一次 Young GC，新生代中的存活对象会大量减少，从而显著缩短 Final Remark 的暂停时间。

**中止条件**: Eden 占用率 > `CMSScheduleRemarkEdenPenetration` (50%) 或超过 `CMSMaxAbortablePrecleanTime` (5 秒)。

#### Phase 5: Final Remark (最终标记) — STW

```
暂停时间: 通常几毫秒到几十毫秒
并行度:   多线程 (-XX:ParallelGCThreads)
```

**目标**: 完成标记过程，确保所有存活对象都被正确标记。

这是 CMS 的第二个 STW 阶段，需要处理：

1. **剩余的 dirty cards** — Phase 3/4 未完全处理的
2. **新生代对老年代的引用** — 扫描整个新生代 (这就是为什么之前要等 Young GC)
3. **Reference Processing** — 处理 SoftReference、WeakReference、PhantomReference
4. **Class Unloading** — 卸载不再使用的类 (如果启用 -XX:+CMSClassUnloadingEnabled)

**优化参数**: `-XX:+CMSScavengeBeforeRemark` — 在 Final Remark 前强制执行一次 Young GC，减少需要扫描的新生代对象数量。

```
CMSScavengeBeforeRemark 的效果:

不使用:  Final Remark 需要扫描整个 Young Gen (可能很大)
         → 较长的 STW 暂停

使用:    Young GC 先清理新生代 → Final Remark 只需扫描少量存活对象
         → 较短的 STW 暂停 (但多了一次 Young GC 暂停)
```

#### Phase 6: Concurrent Sweep (并发清除)

```
暂停时间: 0 (并发执行)
```

**目标**: 清除所有未被标记的死亡对象，回收内存空间。

与标记-压缩 (Mark-Compact) 不同，CMS 的清除阶段**不移动存活对象**。死亡对象所占的空间直接被归还到 Free List。

```
Sweep 前:
┌──────┬──────┬──────┬──────┬──────┬──────┐
│ 存活  │ 死亡  │ 存活  │ 死亡  │ 死亡  │ 存活  │
│  A   │  B   │  C   │  D   │  E   │  F   │
└──────┴──────┴──────┴──────┴──────┴──────┘

Sweep 后:
┌──────┬──────┬──────┬──────┬──────┬──────┐
│ 存活  │ 空闲  │ 存活  │    空闲        │ 存活  │
│  A   │      │  C   │  (D+E 合并)    │  F   │
└──────┴──────┴──────┴──────┬──────┴──────┘
           │                │
           └────────────────┘
                Free List 连接
```

**注意**: 在并发清除期间，应用线程可能在分配新的老年代对象。CMS 使用 Free List 的并发安全分配来支持这一点。

#### Phase 7: Concurrent Reset (并发重置)

```
暂停时间: 0 (并发执行)
```

**目标**: 重置 CMS 内部数据结构（如标记位图 Marking Bitmap），为下一次 CMS 周期做准备。

### 3.3 GC 日志示例 (关键行)

```
[GC (CMS Initial Mark) [1 CMS-initial-mark: 6844K(9216K)] 7064K(19456K), 0.0003 secs]
[CMS-concurrent-mark: 0.009/0.009 secs]
[CMS-concurrent-preclean: 0.001/0.001 secs]
[CMS-concurrent-abortable-preclean: 0.003/0.130 secs]
[GC (CMS Final Remark) [YG occupancy: 3200K (10240K)]
    [Rescan (parallel), 0.0008 secs] [weak refs processing, 0.0000 secs]
    [1 CMS-remark: 6844K(9216K)] 10044K(19456K), 0.0018 secs]
[CMS-concurrent-sweep: 0.004/0.004 secs]
[CMS-concurrent-reset: 0.001/0.001 secs]
```

---

## 4. 写屏障与并发正确性

### 4.1 Incremental Update (增量更新)

CMS 使用 **Incremental Update** 写屏障来处理并发标记期间的引用变化。这与 G1 使用的 **SATB (Snapshot-At-The-Beginning)** 是不同的策略。

```
写屏障伪代码 (CMS Incremental Update):

void oop_field_store(oop* field, oop new_value) {
    *field = new_value;                    // 先执行实际的引用写入
    if (is_in_old_gen(field)) {
        mark_card_dirty(field);            // 将包含 field 的 card 标记为 dirty
    }
}
```

**Incremental Update vs SATB 对比**:

| 特性 | CMS (Incremental Update) | G1 (SATB) |
|------|--------------------------|-----------|
| 记录时机 | 写入后 (post-write) | 写入前 (pre-write) |
| 记录内容 | 被修改的 card 位置 | 被覆盖的旧引用值 |
| Remark 需要 | 重新扫描 dirty cards | 处理 SATB buffer |
| 浮动垃圾 | 较少 | 较多 (旧引用保留至本轮) |
| Remark 耗时 | 较长 (可能需重新遍历) | 较短 (只处理 buffer) |

### 4.2 Card Table (卡表)

CMS 使用 Card Table 来跟踪老年代中哪些区域的引用被修改过。

```
Card Table 结构:

堆内存:      [  0KB  |  512B  | 1024B  | 1536B  | 2048B  | ...  ]
Card Table:  [   0   |   1    |   0    |   0    |   1    | ...  ]
                      dirty                       dirty

每个 card entry (1 byte) 覆盖 512 bytes 的堆内存
Card Table 大小 = 堆大小 / 512
```

Card Table 同时也用于跟踪**跨代引用 (Cross-Generation References)**: 当老年代对象引用新生代对象时，对应的 card 也会被标记为 dirty，这样 Young GC 时不需要扫描整个老年代。

---

## 5. 核心问题 — 为什么 CMS 被移除

### 5.1 碎片化 (Fragmentation)

CMS 最致命的问题。由于使用 Mark-Sweep 不压缩，老年代会逐渐产生大量内存碎片。

```
                     CMS 碎片化演进

Round 1 (初始状态, 较紧凑):
┌──────────────┬──────────────────────────────────────────────┐
│ 存活对象 ...  │            连续空闲空间                        │
└──────────────┴──────────────────────────────────────────────┘

Round 10 (多次 CMS 周期后):
┌───┬──┬────┬──┬───┬──┬──────┬──┬────┬──┬───┬──┬──────┬──┬──┐
│ A │空│ B  │空│ C │空│  D   │空│ E  │空│ F │空│  G   │空│H │
└───┴──┴────┴──┴───┴──┴──────┴──┴────┴──┴───┴──┴──────┴──┴──┘
     8K       4K     2K       16K     4K     8K       12K  2K

总空闲: 56KB  但最大连续空闲块: 16KB
如果需要分配一个 20KB 的对象 → 失败! → 触发 Full GC
```

**后果**: 当碎片化严重到无法分配对象时，CMS 会退化为 **Serial Old (单线程标记-压缩)**，执行一次 Full GC。这个 Full GC 是单线程的，对于大堆来说可能暂停数秒甚至数十秒。

### 5.2 浮动垃圾 (Floating Garbage)

在 CMS 并发标记阶段，应用线程仍在运行并可能产生新的垃圾。这些在并发标记开始后才变成垃圾的对象，在本轮 CMS 周期中无法被回收，称为 **浮动垃圾 (Floating Garbage)**。

```
并发标记开始时:                 并发标记期间:

  Root → A → B                  Root → A ─×─ B  (A.field = null)
                                B 已死亡，但已被标记为存活
                                → B 成为浮动垃圾，需等下一轮回收
```

浮动垃圾的存在意味着 CMS 必须**预留足够的老年代空间**，不能等到老年代完全满了才触发 CMS。这就是 `CMSInitiatingOccupancyFraction` 参数的由来。

### 5.3 Concurrent Mode Failure (并发模式失败)

这是 CMS 用户最常遇到也最致命的问题。发生条件：

1. **CMS 周期进行中**，老年代空间不足以容纳新晋升的对象
2. **老年代碎片化**，无法找到足够大的连续空间分配对象

```
Concurrent Mode Failure 触发流程:

┌─────────────────────┐
│ CMS 正在并发清除 ...  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Young GC: 需要晋升    │
│ 对象到 Old Gen        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐    ┌─────────────────────────────────┐
│ Old Gen 空间不足!     │───→│ Concurrent Mode Failure!         │
│ (空间不够 或 碎片化)   │    │ 中止 CMS → Serial Old Full GC   │
└─────────────────────┘    │ → 单线程 Mark-Compact             │
                           │ → 暂停时间可能数秒到数十秒!         │
                           └─────────────────────────────────┘
```

GC 日志中的表现：

```
[GC (CMS Initial Mark) ...]
[CMS-concurrent-mark: ...]
...
(concurrent mode failure):
 6810K->4801K(9216K), 0.1280730 secs]
 10878K->4801K(19456K),
 [Metaspace: 3092K->3092K(1056768K)], 0.1281860 secs]
 [Times: user=0.13 sys=0.00, real=0.13 secs]
```

### 5.4 Promotion Failure (晋升失败)

与 Concurrent Mode Failure 类似，但发生在 Young GC 期间：

```
Promotion Failure:

Young GC 试图将存活对象从 Survivor 晋升到 Old Gen
→ Old Gen 空间不足 (通常因碎片化)
→ 触发 Full GC (Serial Old)
```

### 5.5 代码维护负担

从 OpenJDK 开发者的角度：

1. **CMS 与其他 GC 共享大量代码**，但 CMS 的并发需求导致许多特殊路径
2. **write barrier 在不同 GC 中有不同实现**，增加了 JIT 编译器的复杂度
3. **内存管理的 Free List 逻辑**与其他使用 bump-pointer 的 GC 不同
4. **移除 CMS 后，G1 的开发速度明显加快** (JDK 14 之后 G1 的改进更频繁)

JEP 363 原文指出：

> "The two listeners (CMS and G1) of the GC interface complicate the maintenance
> of this interface and slow down changes to it."

---

## 6. 关键参数

### 6.1 基本配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-XX:+UseConcMarkSweepGC` | false | 启用 CMS (隐式启用 ParNew 作为 Young GC) |
| `-XX:ParallelGCThreads=N` | CPU 核数相关 | ParNew 和 CMS STW 阶段的并行线程数 |
| `-XX:ConcGCThreads=N` | `(ParallelGCThreads + 3) / 4` | CMS 并发阶段的线程数 |

### 6.2 触发阈值

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-XX:CMSInitiatingOccupancyFraction=N` | 92 (JDK 8) | 老年代占用率达到 N% 时触发 CMS |
| `-XX:+UseCMSInitiatingOccupancyOnly` | false | 禁止 JVM 自适应调整阈值，只使用上述固定值 |

**推荐搭配使用**:

```bash
# 典型低延迟服务配置
-XX:+UseConcMarkSweepGC
-XX:CMSInitiatingOccupancyFraction=70
-XX:+UseCMSInitiatingOccupancyOnly
```

如果不设置 `UseCMSInitiatingOccupancyOnly`，JVM 会根据历史统计数据自适应调整触发阈值。虽然自适应通常是好的，但在某些场景下可能导致 CMS 触发过晚而引发 Concurrent Mode Failure。

### 6.3 优化参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-XX:+CMSScavengeBeforeRemark` | false | Final Remark 前执行 Young GC |
| `-XX:+CMSParallelInitialMarkEnabled` | true (JDK 8) | Initial Mark 使用多线程 |
| `-XX:+CMSParallelRemarkEnabled` | true | Final Remark 使用多线程 |
| `-XX:+CMSClassUnloadingEnabled` | true (JDK 8) | CMS 周期中卸载不用的类 |
| `-XX:+ExplicitGCInvokesConcurrent` | false | System.gc() 触发 CMS 而非 Full GC |

### 6.4 碎片化相关

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-XX:+UseCMSCompactAtFullCollection` | true | Full GC 时执行压缩 |
| `-XX:CMSFullGCsBeforeCompaction=N` | 0 | 每 N 次 Full GC 后执行一次压缩 (0 = 每次) |

### 6.5 典型生产配置

```bash
# 4GB 堆，低延迟 Web 服务 (JDK 8)
java -Xms4g -Xmx4g \
     -Xmn1536m \
     -XX:+UseConcMarkSweepGC \
     -XX:+UseParNewGC \
     -XX:CMSInitiatingOccupancyFraction=70 \
     -XX:+UseCMSInitiatingOccupancyOnly \
     -XX:+CMSScavengeBeforeRemark \
     -XX:+CMSParallelRemarkEnabled \
     -XX:+CMSClassUnloadingEnabled \
     -XX:+ExplicitGCInvokesConcurrent \
     -XX:ParallelGCThreads=8 \
     -XX:ConcGCThreads=2 \
     -XX:+PrintGCDetails \
     -XX:+PrintGCDateStamps \
     -Xloggc:/var/log/gc.log \
     -jar myapp.jar
```

---

## 7. CMS vs G1 对比

### 7.1 设计理念对比

```
CMS 设计理念:                        G1 设计理念:
"尽量并发，减少暂停"                   "可预测暂停时间，避免碎片"

┌────────────────────────┐          ┌────────────────────────┐
│ 传统分代，物理连续       │          │ Region 化，逻辑分代      │
│ Mark-Sweep, 不压缩      │          │ Mark-Compact, 无碎片     │
│ Free List 分配          │          │ Bump Pointer 分配        │
│ 不可预测暂停时间         │          │ MaxGCPauseMillis 目标    │
│ 只管老年代              │          │ 管理整个堆               │
│ 碎片化 → Full GC 退化   │          │ Mixed GC 增量回收        │
└────────────────────────┘          └────────────────────────┘
```

### 7.2 详细对比表

| 维度 | CMS | G1 |
|------|-----|-----|
| **堆布局** | 连续的 Young + Old | Region 化 (1-32MB/region) |
| **回收算法** | Mark-Sweep (不压缩) | Mark-Compact (复制/压缩) |
| **碎片化** | 严重，导致 Full GC | 基本无碎片 (Region 内 compact) |
| **暂停时间** | 不可预测 | 可通过 `-XX:MaxGCPauseMillis` 控制 |
| **老年代回收** | 整个老年代并发 sweep | Mixed GC 选择性回收部分 Region |
| **Young GC** | ParNew (独立) | G1 Young GC (Region 粒度) |
| **写屏障** | Incremental Update | SATB (Snapshot-At-The-Beginning) |
| **Full GC** | Serial Old (单线程!) | 并行 Full GC (JDK 10+, JEP 307) |
| **大对象处理** | 无特殊处理 | Humongous Region |
| **默认 GC** | 从未作为默认 | JDK 9+ 默认 |
| **维护状态** | JDK 14 移除 | 持续优化中 |

### 7.3 为什么 G1 替代了 CMS

1. **碎片化问题根除**: G1 使用 Region 粒度的复制/压缩，不会产生碎片
2. **可预测的暂停时间**: `-XX:MaxGCPauseMillis` 让 G1 能在暂停时间和吞吐量之间权衡
3. **Mixed GC 增量回收**: G1 不需要一次性回收整个老年代，而是每次选择一部分 Region 回收
4. **更好的 Full GC**: 即使发生 Full GC，G1 (JDK 10+) 也是并行的
5. **统一管理整个堆**: G1 不需要单独的 ParNew，简化了 GC 子系统

---

## 8. CMS 的遗产 — 对后续 GC 的影响

### 8.1 并发标记思想的传承

CMS 证明了在应用运行时执行垃圾标记是可行的。这一思想被所有后续低延迟 GC 继承：

```
CMS (2003)                        开创并发标记
  │
  ├── G1 (2012)                   并发标记 + SATB + Region 化
  │
  ├── ZGC (2018, JEP 333)         并发标记 + 并发压缩 + 着色指针
  │
  └── Shenandoah (2019, JEP 189)  并发标记 + 并发压缩 + Brooks Pointer
```

### 8.2 Write Barrier 策略的演进

CMS 的 Incremental Update 策略有一个问题：Final Remark 阶段可能需要重新遍历大量被修改的 cards，导致 STW 暂停较长。G1 吸取这一教训，选择了 SATB 策略：

```
CMS (Incremental Update):
- 优点: 浮动垃圾较少
- 缺点: Remark 阶段可能很长 (需要重新扫描 dirty cards)

G1 (SATB):
- 优点: Remark 阶段快且可预测 (只需处理 SATB buffer)
- 缺点: 浮动垃圾较多 (但 G1 可以用 Mixed GC 渐进回收)

ZGC / Shenandoah:
- 使用 Load Barrier 而非 Store Barrier
- 彻底解决了 Remark 暂停问题
```

### 8.3 Concurrent Mode Failure 的教训

CMS 的 Concurrent Mode Failure 暴露了"回收速度跟不上分配速度"的根本问题。后续 GC 用不同方式解决：

| GC | 解决方案 |
|-----|---------|
| G1 | Mixed GC — 增量回收老年代 Region，不需要一次性回收全部；pacing 控制分配速率 |
| ZGC | 并发压缩 — 回收速度快到几乎不会跟不上分配 |
| Shenandoah | 并发压缩 + Pacing — 如果回收跟不上分配，主动降低应用线程的分配速率 |

### 8.4 碎片化教训

CMS 的碎片化问题直接推动了后续 GC 的设计决策：

```
CMS: Mark-Sweep → 碎片化 → Full GC (灾难)
     │
     └── 教训: 必须有压缩机制

G1:  Region 化 + 复制 → 每个 Region 内无碎片
     │
ZGC: 并发压缩 → 完全消除碎片，且不暂停
     │
Shenandoah: 并发压缩 → 同上
```

---

## 9. 迁移建议 — 从 CMS 迁移到什么

### 9.1 迁移决策树

```
从 CMS 迁移到什么 GC？

┌──────────────────────┐
│ 你的 JDK 版本是？      │
└──────────┬───────────┘
           │
     ┌─────┴─────┐
     │           │
  JDK 8       JDK 11+
     │           │
     ▼           ▼
  继续使用     ┌──────────────────────┐
  CMS 或      │ 你的延迟需求是？        │
  升级 JDK    └──────────┬───────────┘
                        │
              ┌─────────┼──────────┐
              │         │          │
         一般延迟    低延迟      超低延迟
         (< 200ms)  (< 20ms)   (< 1ms)
              │         │          │
              ▼         ▼          ▼
            G1 GC    G1 GC      ZGC 或
          (默认即可)  (调优后)   Shenandoah
```

### 9.2 大多数场景 → G1

G1 是 CMS 最自然的替代品，也是 JDK 9+ 的默认 GC。

**迁移优势**: 无碎片化、可预测暂停时间、并行 Full GC、参数更少。
**迁移注意**: G1 吞吐量可能略低 (约 5-10%)，内存占用略高 (Remembered Set 开销)。

### 9.3 超低延迟 → ZGC 或 Shenandoah

如果你使用 CMS 的原因是追求低延迟，ZGC 和 Shenandoah 是更好的选择。

| 特性 | CMS | ZGC (JDK 21+) | Shenandoah (JDK 17+) |
|------|-----|---------------|---------------------|
| 最大暂停 | 数百毫秒到数秒 | < 1ms (亚毫秒级) | < 10ms |
| 碎片化 | 严重 | 无 (并发压缩) | 无 (并发压缩) |
| 堆大小范围 | < 8GB 最佳 | 8MB - 16TB | 任意 |
| CPU 开销 | 中等 | 较高 | 较高 |

### 9.4 参数映射表

从 CMS 迁移到 G1 时的参数映射：

| CMS 参数 | G1 对应 | 说明 |
|----------|---------|------|
| `-XX:+UseConcMarkSweepGC` | `-XX:+UseG1GC` | JDK 9+ 默认无需指定 |
| `-XX:+UseParNewGC` | (不需要) | G1 自带 Young GC |
| `-XX:CMSInitiatingOccupancyFraction=70` | `-XX:InitiatingHeapOccupancyPercent=45` | G1 默认 45%，通常不需改 |
| `-XX:+UseCMSInitiatingOccupancyOnly` | (不需要) | G1 自适应调整通常效果好 |
| `-XX:+CMSScavengeBeforeRemark` | (不需要) | G1 的 Remark 设计不需要 |
| `-XX:ParallelGCThreads=N` | `-XX:ParallelGCThreads=N` | 含义相同 |
| `-XX:ConcGCThreads=N` | `-XX:ConcGCThreads=N` | 含义相同 |
| `-Xmn` (新生代大小) | (不推荐设置) | G1 自动调整新生代大小 |
| `-XX:+CMSClassUnloadingEnabled` | `-XX:+ClassUnloadingWithConcurrentMark` | G1 默认开启 |

### 9.5 迁移示例

```bash
# CMS 配置 (JDK 8):
java -Xms4g -Xmx4g -Xmn1536m \
     -XX:+UseConcMarkSweepGC \
     -XX:+UseParNewGC \
     -XX:CMSInitiatingOccupancyFraction=70 \
     -XX:+UseCMSInitiatingOccupancyOnly \
     -XX:+CMSScavengeBeforeRemark \
     -XX:ParallelGCThreads=8 \
     -XX:ConcGCThreads=2 \
     -jar myapp.jar

# G1 配置 (JDK 17+):
java -Xms4g -Xmx4g \
     -XX:MaxGCPauseMillis=200 \
     -XX:ParallelGCThreads=8 \
     -XX:ConcGCThreads=2 \
     -Xlog:gc*:file=/var/log/gc.log:time,uptime,level,tags \
     -jar myapp.jar

# ZGC 配置 (JDK 21+):
java -Xms4g -Xmx4g \
     -XX:+UseZGC \
     -XX:+ZGenerational \
     -Xlog:gc*:file=/var/log/gc.log:time,uptime,level,tags \
     -jar myapp.jar
```

---

## 10. CMS 相关的 JEP

| JEP | JDK | 标题 | 影响 |
|-----|-----|------|------|
| [JEP 248](https://openjdk.org/jeps/248) | 9 | Make G1 the Default Garbage Collector | G1 取代 CMS 成为默认 |
| [JEP 291](https://openjdk.org/jeps/291) | 9 | Deprecate the Concurrent Mark Sweep (CMS) GC | CMS 正式废弃 |
| [JEP 307](https://openjdk.org/jeps/307) | 10 | Parallel Full GC for G1 | G1 Full GC 并行化，解决 CMS 的单线程 Full GC 遗留问题 |
| [JEP 333](https://openjdk.org/jeps/333) | 11 | ZGC: A Scalable Low-Latency GC (Experimental) | 下一代低延迟 GC，CMS 的终极替代 |
| [JEP 363](https://openjdk.org/jeps/363) | 14 | Remove the Concurrent Mark Sweep (CMS) GC | CMS 源码彻底移除 |

---

## 11. 总结

```
CMS 的一生:

2003 ────────────── 2017 ─── 2020
 │     黄金时代      │ 废弃  │ 移除
 │                   │       │
 │  "第一个并发 GC"   │       │
 │  "低延迟服务标配"  │       │
 │  "开创并发范式"    │       │
 │                   │       │
 │  但碎片化、CMF     │       │
 │  等问题无解 ...    │       │
 │                   │       │
 └──── 遗产 ─────────┴───────┘
       │
       ├── 并发标记 → G1, ZGC, Shenandoah 继承
       ├── Write Barrier → SATB 改进
       ├── CMF 教训 → Mixed GC / 并发压缩
       └── 碎片化教训 → Region 化 / 并发压缩
```

CMS 虽已成为历史，但它开创的并发回收范式深刻影响了 Java GC 的发展方向。理解 CMS 的设计与缺陷，是理解现代 GC (G1、ZGC、Shenandoah) 设计动机的最佳途径。

---

> 本文档基于 OpenJDK 源码 (JDK 8 ~ JDK 13 中的 CMS 实现) 及 JEP 291/363 整理。
> CMS 源码已在 JDK 14 中被移除，如需查看原始实现请参考 JDK 13 及之前版本。
