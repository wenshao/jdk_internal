# 内存管理

> 堆、栈、Metaspace、Compressed Oops 演进历程

[← 返回核心平台](../)

---

## 1. 快速概览

```
JDK 1.0 ── JDK 6u23 ── JDK 7 ── JDK 8 ── JDK 11 ── JDK 17 ── JDK 21 ── JDK 24 ── JDK 25
   │         │        │        │        │        │        │        │        │
堆/栈    Compressed  默认启用  元空间  ZGC    分代    AOT缓存  紧凑对象头
PermGen   Oops     Oops   字符串  低延迟  ZGC   JEP483   JEP519正式
```

### 核心演进

| 版本 | 特性 | 说明 | 内存节省 |
|------|------|------|----------|
| **JDK 6u23** | Compressed Oops | 压缩普通对象指针 | ~20-30% |
| **JDK 7** | Compressed Oops 默认 | 64位默认启用 | ~20-30% |
| **JDK 8** | 元空间 | 移除永久代 | 动态扩展 |
| **JDK 8u20** | String Deduplication | 字符串去重 | ~10% |
| **JDK 11** | ZGC | 低延迟 GC | 大内存友好 |
| **JDK 15** | ZGC 生产可用 | 正式版 | 稳定 |
| **JDK 21** | 分代 ZGC | 降低 GC 频率 | 更高效 |
| **JDK 24** | AOT 缓存 (JEP 483) | 预加载类链接 | 减少运行时分配 |
| **JDK 24** | 紧凑对象头实验 (JEP 450) | 实验性压缩对象头 | 需 UnlockExperimentalVMOptions |
| **JDK 25** | 紧凑对象头正式 (JEP 519) | 对象头 12→8 字节，生产就绪 | ~10-20% 堆内存节省 |

---

## 目录

- [内存区域](#2-内存区域)
- [内存区域详解](#25-内存区域详解)
- [内存分配](#3-内存分配)
- [内存优化](#4-内存优化)
- [CompressedOops 深入](#41-compressed-oops-深入)
- [Compact Object Headers 深入](#42-compact-object-headers-深入)
- [内存屏障与 JMM](#43-内存屏障与-jmm)
- [NMT 实践](#44-nmt-实践)
- [容器环境内存管理](#45-容器环境内存管理)
- [最新增强](#5-最新增强)
- [核心贡献者](#6-核心贡献者)
- [相关链接](#9-相关链接)

---

## 2. 内存区域

### JVM 内存结构

```
┌─────────────────────────────────────────────────────────┐
│                     JVM 内存结构                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────┐       │
│  │              堆内存 (Heap)                 │       │
│  │  ├── 年轻代 (Young Generation)              │       │
│  │  │   ├── Eden 区                            │       │
│  │  │   └── Survivor 区 (S0, S1)               │       │
│  │  └── 老年代 (Old Generation)                │       │
│  │      ├── 存活期长的对象                      │       │
│  │      └── 大对象直接分配                      │       │
│  └─────────────────────────────────────────────┘       │
│                                                         │
│  ┌─────────────────────────────────────────────┐       │
│  │            栈内存 (Stack)                   │       │
│  │  ├── Java 栈 (每线程一个)                   │       │
│  │  │   ├── 栈帧 (方法调用)                    │       │
│  │  │   ├── 局部变量                           │       │
│  │  │   └── 操作数栈                           │       │
│  │  └── 本地方法栈 (Native Stack)              │       │
│  └─────────────────────────────────────────────┘       │
│                                                         │
│  ┌─────────────────────────────────────────────┐       │
│  │          方法区 (Method Area)               │       │
│  │  ├── 元空间 (Metaspace, JDK 8+)            │       │
│  │  │   ├── 类元数据                           │       │
│  │  │   ├── 方法元数据                         │       │
│  │  │   └── 常量池                             │       │
│  │  └── 永久代 (PermGen, JDK 7-)              │       │
│  └─────────────────────────────────────────────┘       │
│                                                         │
│  ┌─────────────────────────────────────────────┐       │
│  │         本地内存 (Native Memory)            │       │
│  │  ├── 直接内存 (Direct Memory)               │       │
│  │  │   └── NIO 缓冲区                         │       │
│  │  ├── 线程栈                                 │       │
│  │  ├── 代码缓存 (Code Cache)                  │       │
│  │  └── GC 工作内存                            │       │
│  └─────────────────────────────────────────────┘       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 堆内存

**特点**:
- 线程共享
- 存储对象实例
- GC 主要区域

**配置参数**:

```bash
# 堆内存大小
-Xms4g          # 初始堆大小
-Xmx4g          # 最大堆大小
-XX:NewRatio=2  # 年轻代/老年代比例

# 年轻代配置
-Xmn2g          # 年轻代大小
-XX:SurvivorRatio=8    # Eden/S0/S1 比例

# 大对象直接进入老年代
-XX:PretenureSizeThreshold=3m  # 大对象阈值
```

### 栈内存

**特点**:
- 线程私有
- 存储局部变量和方法调用
- 自动管理 (方法出栈自动释放)

**配置参数**:

```bash
# 栈内存大小
-Xss1m          # 每线程栈大小 (JDK 8+)
-XX:ThreadStackSize=1024  # 每线程栈大小 (KB)

# 栈深度监控
-XX:MaxRecursiveInlineLevel=20  # 最大递归内联层级
```

**栈溢出**: 递归过深或栈帧过大导致 `StackOverflowError`。增大 `-Xss` 可缓解，但根本解决需减少递归深度或改用迭代。

### 元空间 (Metaspace)

**JDK 8+ 变化**:

| 特性 | 永久代 (PermGen) | 元空间 (Metaspace) |
|------|------------------|-------------------|
| 位置 | 堆内 | 本地内存 |
| 大小 | 固定 | 动态扩展 |
| 垃圾回收 | 需要Full GC | 自动触发 |
| 默认大小 | 固定 | 无限制 |
| 调整困难 | 是 | 否 |

**配置参数**:

```bash
# 元空间大小
-XX:MetaspaceSize=256m           # 初始元空间大小
-XX:MaxMetaspaceSize=512m        # 最大元空间大小
-XX:CompressedClassSpaceSize=1g  # 压缩类空间大小

# 监控元空间
-XX:+PrintGCDetails              # 打印 GC 详情
-XX:+PrintGCTimeStamps           # 打印 GC 时间戳
```

**类卸载**: 需同时满足三条件: (1) 类的所有实例已回收, (2) 加载该类的 ClassLoader 已回收, (3) Class 对象无强引用。详见 [内存区域详解](#25-内存区域详解)。

### 直接内存

**特点**:
- 不在堆上分配
- 避免 JVM 堆与本地内存之间复制
- 用于 NIO 操作

**配置参数**:

```bash
# 直接内存大小
-XX:MaxDirectMemorySize=1g  # 最大直接内存 (默认 ≈ 堆大小)

# 监控直接内存
-XX:+PrintGCDetails         # 包含直接内存信息
```

**使用示例**:

```java
// 分配直接内存
ByteBuffer buffer = ByteBuffer.allocateDirect(1024 * 1024);

// vs 堆内存
ByteBuffer heapBuffer = ByteBuffer.allocate(1024 * 1024);
```

---

## 2.5 内存区域详解

### Java Heap 详解

#### 新生代 (Young Generation)

```
┌───────────────────────────────────────────────────────────────────┐
│                     Young Generation                              │
│                                                                   │
│  ┌───────────────────────────┬──────────┬──────────┐             │
│  │       Eden (80%)          │  S0 (10%)│  S1 (10%)│             │
│  │                           │(From)    │(To)      │             │
│  │  新对象在此分配            │          │          │             │
│  │  (TLAB 快速路径)           │ 存活对象  │ 复制目标  │             │
│  │                           │ 来源     │          │             │
│  └───────────────────────────┴──────────┴──────────┘             │
│                                                                   │
│  Minor GC 流程:                                                   │
│  1. Eden 满 → 触发 Young GC                                      │
│  2. Eden + S0(From) 中存活对象复制到 S1(To)                       │
│  3. 存活年龄 (age) +1                                             │
│  4. 年龄超过 MaxTenuringThreshold → 晋升老年代 (Promotion)        │
│  5. S0/S1 角色互换                                                │
└───────────────────────────────────────────────────────────────────┘
```

**关键参数**:

```bash
-XX:SurvivorRatio=8          # Eden:S0:S1 = 8:1:1
-XX:MaxTenuringThreshold=15  # 最大晋升年龄 (默认 15, G1 默认 15)
-XX:+UseAdaptiveSizePolicy   # 自适应调整各区比例 (默认启用)
-XX:TargetSurvivorRatio=50   # Survivor 目标使用率，超过则动态降低晋升年龄
```

#### 老年代 (Old Generation)

存放长期存活对象和大对象。当老年代空间不足时触发 Mixed GC (G1) 或 Full GC。

**直接进入老年代的情况**:
- 大对象: 超过 `-XX:PretenureSizeThreshold` (仅 Serial/ParNew 有效)
- 长期存活: age 超过 `MaxTenuringThreshold`
- 动态年龄判断: 同龄对象总大小 > Survivor 空间的 `TargetSurvivorRatio%`
- Survivor 空间不足 (分配担保失败)

#### G1 Humongous 区域

在 G1 GC 中，超过 Region 大小 50% 的对象被视为 **Humongous Object (巨型对象)**，直接分配在连续的 Humongous Region 中：

```bash
# G1 Region 大小 (自动根据堆大小计算, 范围 1MB~32MB)
-XX:G1HeapRegionSize=16m

# 巨型对象阈值 = G1HeapRegionSize / 2
# 例如 RegionSize=16MB, 则 > 8MB 的对象为 Humongous
```

**注意**: Humongous 对象在 G1 中只能在 Full GC 或 Concurrent Cycle cleanup 阶段回收 (JDK 8u40+ 支持在 Young GC 中回收无引用的 Humongous 对象)。频繁分配 Humongous 对象会导致堆碎片化，应通过增大 `G1HeapRegionSize` 或减少大对象分配来优化。

### Metaspace 详解

#### PermGen → Metaspace 演进

```
JDK 7-:  ┌─────────┐    JDK 8+:  ┌───────────────────┐
          │ PermGen │             │    Metaspace       │
          │ (堆内)   │             │  (Native Memory)   │
          │ 固定大小  │    ──→     │  动态扩展           │
          │ OOM常见  │             │  弹性伸缩 (JDK 16+)│
          └─────────┘             └───────────────────┘
```

#### Elastic Metaspace (JEP 387, JDK 16)

JDK 16 引入 **Elastic Metaspace**，由 Thomas Stuefe (Red Hat) 主导，解决旧版 Metaspace "只增不减" 的内存归还问题：

**核心设计**:
- **Buddy Allocation (伙伴分配)**: 内存块大小为 2 的幂次方，释放时自动合并相邻伙伴块，减少碎片化
- **Granule-Based 组织**: 以固定大小的 granule (通常 64KB) 为 commit/uncommit 最小单位
- **内存归还**: ClassLoader 卸载后，通过 `madvise(MADV_DONTNEED)` (Linux) 将空闲 granule 物理内存归还 OS

```bash
# Elastic Metaspace 调优
-XX:MetaspaceReclaimPolicy=balanced  # 回收策略 (JDK 21+: aggressive/balanced/none)
```

#### 类卸载 (Class Unloading)

类卸载发生在 GC 阶段，必须同时满足三个条件：
1. 该类的所有实例已被回收
2. 加载该类的 `ClassLoader` 已被回收
3. 该类的 `java.lang.Class` 对象无强引用

**系统类 (由 Bootstrap/Platform ClassLoader 加载) 永远不会被卸载**。只有自定义 ClassLoader 加载的类才可能被卸载。典型场景: OSGi 容器、热部署应用服务器、动态代理框架。

### 线程栈详解

#### 平台线程栈 (Platform Thread Stack)

每个平台线程在创建时分配固定大小的栈空间 (native memory):

```bash
-Xss1m                      # 默认栈大小 (Linux/x64 默认 1MB)
-XX:ThreadStackSize=1024    # 等效写法 (单位 KB)
```

**栈空间组成**:
- 栈帧 (Stack Frame): 局部变量表 (Local Variables)、操作数栈 (Operand Stack)、返回地址
- Guard Pages: 栈底的保护页，触发 StackOverflowError 而非段错误
- 每个平台线程固定占用 ~1MB native memory (即使栈实际使用量很小)

**1000 个平台线程 = ~1GB 栈内存**，这是传统 thread-per-request 模型的核�瓶颈。

#### 虚拟线程栈 (Virtual Thread Stack, JDK 21+)

虚拟线程的栈存储在 **Java 堆** 上，以 `StackChunk` 对象链表形式管理：

```
虚拟线程栈 (堆上):
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ StackChunk 0 │────▶│ StackChunk 1 │────▶│ StackChunk 2 │
│ (栈帧数据)    │     │ (栈帧数据)    │     │ (栈帧数据)    │
└──────────────┘     └──────────────┘     └──────────────┘
```

**内存优势**:
- 初始栈大小极小 (几百字节)，按需增长
- 挂起 (yield) 时栈帧冻结 (freeze) 到堆上的 StackChunk 对象
- 恢复 (resume) 时从 StackChunk 拷贝回 carrier 线程的 native 栈
- StackChunk 作为普通 Java 对象受 GC 管理，不需要的栈数据自动回收
- 百万级虚拟线程仅占用少量堆内存 (按实际栈深度计费)

### Code Cache 详解

JIT 编译器将热点方法编译为机器码，存储在 Code Cache (native memory) 中。

#### 分段 Code Cache (Segmented Code Cache, JDK 9+)

JDK 9 将 Code Cache 分为三个独立的段 (heap):

```
┌───────────────────────────────────────────────────────────────────┐
│                     Code Cache (分段)                              │
├────────────────────┬───────────────────┬──────────────────────────┤
│ Non-method (非方法) │ Profiled (有剖析)  │ Non-profiled (无剖析)    │
│                    │                   │                          │
│ VM 生成的代码:     │ C1 编译 + 剖析:    │ C2 编译 (优化后):         │
│ - Stubs           │ - 含类型剖析信息   │ - 完全优化的机器码        │
│ - Adapters        │ - 可能被去优化     │ - 长期驻留               │
│ - Deoptimization  │ - 生命周期较短     │ - 不含剖析数据           │
├────────────────────┼───────────────────┼──────────────────────────┤
│ ~3MB (默认)        │ ~122MB (默认)     │ ~122MB (默认)            │
└────────────────────┴───────────────────┴──────────────────────────┘
```

**配置参数**:

```bash
-XX:ReservedCodeCacheSize=512m       # Code Cache 总大小 (默认 ~240MB)
-XX:NonMethodCodeHeapSize=5m         # 非方法段
-XX:ProfiledCodeHeapSize=240m        # 有剖析段
-XX:NonProfiledCodeHeapSize=240m     # 无剖析段
-XX:+SegmentedCodeCache              # 启用分段 (JDK 9+ 默认)

# Code Cache 满时的行为
-XX:+UseCodeCacheFlushing            # 启用清除 (默认)
```

**分段优势**: 减少不同生命周期代码之间的碎片化，提高清除效率，改善 I-Cache 局部性。

### 直接内存详解 (Direct Memory)

#### DirectByteBuffer

`java.nio.DirectByteBuffer` 通过 `Unsafe.allocateMemory()` 在 native 堆上分配内存，避免堆内 (HeapByteBuffer) 与 native 之间的数据拷贝:

```java
// 分配直接内存 (off-heap)
ByteBuffer direct = ByteBuffer.allocateDirect(64 * 1024 * 1024); // 64MB

// 堆内缓冲 (on-heap, 需拷贝到 native 才能执行 I/O)
ByteBuffer heap = ByteBuffer.allocate(64 * 1024 * 1024);
```

**生命周期**: DirectByteBuffer 对象在堆上, 但引用的内存在 native 堆。对象被 GC 回收时通过 `Cleaner` 机制释放 native 内存。如果 DirectByteBuffer 晋升到老年代但 Full GC 迟迟不触发, 可能造成 native 内存泄漏。

```bash
-XX:MaxDirectMemorySize=2g    # 最大直接内存 (默认 ≈ -Xmx)
```

**排查直接内存泄漏**:
- NMT 中查看 `Internal` 标签增长
- `jcmd <pid> VM.native_memory summary` 查看 committed 增长
- 代码层面: 确保 `DirectByteBuffer` 及时释放或使用 `try-with-resources` + `Arena` (JDK 22+)

---

## 3. 内存分配

### 对象分配过程

```
┌─────────────────────────────────────────────────────────┐
│                 对象分配过程                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 类加载检查                                          │
│     ├── 类是否已加载                                   │
│     └── 类元数据是否准备                               │
│                                                         │
│  2. 对象大小计算                                        │
│     ├── 实例数据大小                                   │
│     ├── 对象头大小                                     │
│     └── 对齐填充                                       │
│                                                         │
│  3. 选择分配方式                                        │
│     ├── TLAB (线程本地分配缓冲)                        │
│     └── 直接在 Eden 分配                               │
│                                                         │
│  4. 内存空间初始化                                      │
│     ├── 清零内存                                       │
│     └── 设置对象头                                     │
│                                                         │
│  5. 构造方法调用                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### TLAB (Thread-Local Allocation Buffer)

**特点**:
- 线程私有
- 无锁分配
- 提高分配效率

**配置参数**:

```bash
# TLAB 配置
-XX:+UseTLAB                     # 启用 TLAB (默认)
-XX:TLABSize=256k                # TLAB 初始大小
-XX:TLABWasteTargetPercent=1     # TLAB 浪费目标比例
-XX:ResizeTLAB                   # 动态调整 TLAB 大小
```

### 对象内存布局

```
┌─────────────────────────────────────────────────────────┐
│                  对象内存布局                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  普通对象 (JDK 25 JEP 519 紧凑对象头, 需 -XX:+UseCompactObjectHeaders): │
│  ┌───────────────────────────────────────────┐         │
│  │  Mark Word (8 bytes, 含类信息)            │         │
│  │  ├── 锁状态                               │         │
│  │  ├── GC 标记                              │         │
│  │  ├── HashCode                             │         │
│  │  └── 类指针 (合并在 Mark Word 中)         │         │
│  ├───────────────────────────────────────────┤         │
│  │  Fields                                  │         │
│  │  ├── 实例数据                             │         │
│  │  └── 对齐填充                             │         │
│  └───────────────────────────────────────────┘         │
│                                                         │
│  数组对象:                                              │
│  ┌───────────────────────────────────────────┐         │
│  │  Mark Word (8 bytes, 含类信息)            │         │
│  ├───────────────────────────────────────────┤         │
│  │  Array Length (4 bytes)                   │         │
│  ├───────────────────────────────────────────┤         │
│  │  Array Elements                          │         │
│  │  └── 数组元素                             │         │
│  └───────────────────────────────────────────┘         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 对象头 (Mark Word)

```
┌─────────────────────────────────────────────────────────┐
│                 Mark Word 结构                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  64 位 JVM:                                            │
│  │ unused:25│ hashcode:31│ unused:1│ age:4│ biased:1│01││
│                                                         │
│  32 位 JVM:                                            │
│  │ thread:13│ epoch:2│ age:4│ biased:1│01│ size:1│00││
│                                                         │
│  锁状态:                                               │
│  ├── 01 - 无锁或偏向锁                                  │
│  ├── 00 - 轻量级锁                                      │
│  ├── 10 - 重量级锁 (Monitor)                            │
│  └── 11 - GC 标记                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 4. 内存优化

### 4.1 Compressed Oops 深入

**压缩普通对象指针 (Compressed Ordinary Object Pointers)**

#### 地址计算原理

64 位 JVM 中，对象指针本应占 8 字节。CompressedOops 利用对象 **8 字节对齐 (Object Alignment)** 的特性，将 64 位地址压缩为 32 位:

```
地址解码公式:
  实际地址 (real address) = base + (compressed_oop << shift)

其中:
  base  = 堆起始地址 (HeapBaseMinAddress)
  shift = 对齐位数 (通常为 3, 即 8 字节对齐, 2^3 = 8)
```

由于对象始终 8 字节对齐，地址低 3 位恒为 0，存储时右移 3 位丢弃，解码时左移 3 位恢复。32 位 compressed oop 可寻址 2^32 * 8 = **32GB** 堆空间。

#### 零基压缩 (Zero-Based Compressed Oops)

当堆起始地址为 0 (或足够低) 时，`base = 0`，解码简化为:

```
实际地址 = compressed_oop << 3    (无需加 base, 省一条指令)
```

HotSpot 优先尝试在低地址分配堆以实现零基压缩。Linux 上通过 `mmap` 在低虚拟地址区域请求堆内存。

#### 32GB / 64GB 边界

| 堆大小 | 压缩模式 | base | shift | 说明 |
|--------|----------|------|-------|------|
| < ~4GB | 零基, 无移位 | 0 | 0 | 32 位直接寻址, 最高效 |
| < ~32GB | 零基, 3 位移位 | 0 | 3 | `addr = oop << 3`, 高效 |
| < ~32GB (堆地址高) | 非零基, 3 位移位 | 非零 | 3 | `addr = base + (oop << 3)` |
| 32GB~64GB | 非零基, 更大 shift | 非零 | >3 | 需 16 字节对齐 (`-XX:ObjectAlignmentInBytes=16`) |
| > 64GB | 不可压缩 | N/A | N/A | 使用 64 位指针, 内存开销增加 ~40% |

**最佳实践**: 堆大小控制在 **31GB** 以内 (`-Xmx31g`) 以确保零基压缩。设置 32GB 反而可能因跨越边界而失去压缩，实际可用空间不增反降。

```bash
# 启用压缩指针 (堆 < 32GB 时默认启用)
-XX:+UseCompressedOops

# 验证压缩模式
-XX:+PrintCompressedOopsMode    # 打印实际使用的压缩模式

# 调整对齐以扩大寻址范围 (代价: 每个对象更多 padding 浪费)
-XX:ObjectAlignmentInBytes=16   # 16 字节对齐, 可寻址 64GB
```

**Compressed Class Pointers (CompressedClassPointers)**: 与 CompressedOops 类似但独立，用于压缩对象头中的 Klass 指针。JDK 15+ 即使关闭 CompressedOops 也可以独立使用 CompressedClassPointers。

```bash
-XX:+UseCompressedClassPointers           # 默认启用
-XX:CompressedClassSpaceSize=1g           # 压缩类空间大小 (默认 1GB)
```

### String Deduplication

**字符串去重**

**原理**:
- G1 GC 识别重复字符串
- 保留一个副本，其他指向该副本
- 减少内存占用

**配置参数**:

```bash
# 启用字符串去重 (默认未启用)
-XX:+UseStringDeduplication

# 去重阈值
-XX:StringDeduplicationAgeThreshold=3

# 支持 G1、ZGC 和 Parallel GC (JDK 18+)
-XX:+UseG1GC
```

### 对象池与集合优化

```java
// ✅ 重用昂贵对象 (对象池模式)
private static final DateTimeFormatter FORMATTER =
    DateTimeFormatter.ofPattern("yyyy-MM-dd");

// ✅ 指定初始容量避免扩容
List<String> list = new ArrayList<>(1000);
Map<String, Integer> map = new HashMap<>(1000);
```

### 引用类型与内存回收

| 引用类型 | 回收时机 | 典型用途 |
|----------|----------|----------|
| Strong Reference | 不会被 GC 回收 | 普通对象引用 |
| `SoftReference` | 内存不足时回收 | 缓存 |
| `WeakReference` | 下次 GC 时回收 | WeakHashMap, 监听器 |
| `PhantomReference` | 对象被回收后入队 | 资源清理 (替代 finalize) |

### 4.2 Compact Object Headers 深入 (JEP 519 / Project Lilliput)

#### 传统对象头 vs 紧凑对象头

```
传统对象头 (64-bit JVM, CompressedOops on):

  ┌─────────────────────────────┬──────────────────────┐
  │    Mark Word (8 bytes)      │ Klass Pointer (4 B)  │  = 12 bytes
  │ [hash:31|age:4|lock:2|...]  │ [compressed klass]   │  + 4B padding = 16B
  └─────────────────────────────┴──────────────────────┘

紧凑对象头 (JEP 519, -XX:+UseCompactObjectHeaders):

  ┌─────────────────────────────────────────────────────┐
  │          Compact Header (8 bytes)                    │  = 8 bytes
  │ [size:22 | klass:32 | age:6 | lock:4]               │  无需额外 padding
  └─────────────────────────────────────────────────────┘
```

#### Klass Pointer 在 Mark Word 中的编码

紧凑对象头的核心创新是将 **Klass 指针嵌入 Mark Word**，消除独立的 Klass Pointer 字段:

- **[63:42] 22 bits**: 对象大小 (用于 GC 遍历时跳过对象，无需查 Klass 的 layout 信息)
- **[41:10] 32 bits**: 压缩的 Klass 指针 (与 CompressedClassPointers 共享编码)
- **[9:4] 6 bits**: GC 年龄 (最大 63，传统头部仅 4 bits/最大 15)
- **[3:0] 4 bits**: 锁状态与标志位

#### hashCode 的处理

传统 Mark Word 中有 31 bits 存储 identity hashCode。紧凑头部中 **没有空间存储 hashCode**。解决方案:

- 首次调用 `System.identityHashCode()` 或 `Object.hashCode()` 时，在对象外部 (side table 或对象尾部) 存储 hashCode
- 已计算 hashCode 的对象通过 Mark Word 中的标志位标识

#### 对堆大小的影响

紧凑对象头对小对象密集型应用效果显著:

| 对象类型 | 传统大小 | 紧凑后大小 | 节省 |
|----------|----------|-----------|------|
| `java.lang.Object` | 16 B | 12 B (对齐后 16 B) | 0~25% |
| 只含 1 个 int 字段 | 16 B | 12 B (对齐后 16 B) | 0% |
| 只含 1 个 long 字段 | 24 B | 16 B | 33% |
| `HashMap$Node` | 32 B | 28 B (对齐后 32 B) | 0~12% |
| 空数组 `new byte[0]` | 16 B | 12 B (对齐后 16 B) | 0~25% |

> **注意**: 实际节省取决于对齐要求。8 字节对齐下，部分对象的节省被 padding 抵消。但统计上，SPECjbb2015 实测堆空间减少 **~22%**。

#### 与 GC 的兼容性

所有主流 GC 均支持紧凑对象头: Serial, Parallel, G1, ZGC, Shenandoah。JDK 25 (JEP 519) 为正式特性 (非默认启用)，需 `-XX:+UseCompactObjectHeaders` 显式开启。

---

### 4.3 内存屏障与 JMM

#### Java Memory Model (JMM) 与 happens-before

JMM (JSR-133, JDK 5) 定义了多线程环境下共享变量的可见性规则。核心概念是 **happens-before 关系**:

| happens-before 规则 | 说明 |
|---------------------|------|
| 程序顺序规则 | 同一线程内，前面的操作 happens-before 后面的操作 |
| Monitor 锁规则 | unlock happens-before 后续对同一锁的 lock |
| volatile 规则 | volatile 写 happens-before 后续对同一 volatile 的读 |
| 线程启动规则 | `Thread.start()` happens-before 该线程的任何操作 |
| 线程终止规则 | 线程的任何操作 happens-before 其他线程检测到该线程终止 |
| 传递性 | A happens-before B, B happens-before C => A happens-before C |

#### volatile 实现与内存屏障 (Memory Barriers)

JMM 将内存屏障 (fence) 分为四类:

| 屏障类型 | 语义 | 用途 |
|----------|------|------|
| **LoadLoad** | Load1; LoadLoad; Load2 | Load2 不会在 Load1 完成前执行 |
| **StoreStore** | Store1; StoreStore; Store2 | Store2 不会在 Store1 刷新前执行 |
| **LoadStore** | Load1; LoadStore; Store2 | Store2 不会在 Load1 完成前执行 |
| **StoreLoad** | Store1; StoreLoad; Load2 | Load2 不会在 Store1 刷新前执行 (最重量级) |

**volatile 写/读的屏障插入**:

```
volatile 写 (volatile store):
  StoreStore barrier
  [volatile store]
  StoreLoad barrier       ← 最昂贵, 确保写对所有后续读可见

volatile 读 (volatile load):
  [volatile load]
  LoadLoad barrier
  LoadStore barrier
```

#### 在 x86 与 AArch64 上的映射

| JMM 屏障 | x86/x64 | AArch64 |
|-----------|---------|---------|
| LoadLoad | 无需 (硬件保证) | `dmb ishld` |
| StoreStore | 无需 (硬件保证) | `dmb ishst` |
| LoadStore | 无需 (硬件保证) | `dmb ishld` |
| StoreLoad | `lock addl $0, (%rsp)` 或 `mfence` | `dmb ish` |

**x86 TSO (Total Store Order)**: x86 硬件提供较强的内存序，仅 StoreLoad 需要显式屏障。因此 volatile 在 x86 上性能开销主要来自 StoreLoad 屏障。

**AArch64 弱内存序**: ARM 架构需要更多显式屏障。HotSpot 在 AArch64 上通过 `dmb` (Data Memory Barrier) 指令实现，开销相对更高。JDK 持续优化 AArch64 的屏障生成 (例如合并相邻屏障、利用 `ldar`/`stlr` acquire/release 语义减少 full barrier)。

```java
// volatile 示例: 双重检查锁定 (Double-Checked Locking)
class Singleton {
    private static volatile Singleton instance;  // volatile 确保可见性

    public static Singleton getInstance() {
        if (instance == null) {                  // 第一次检查 (无锁)
            synchronized (Singleton.class) {
                if (instance == null) {          // 第二次检查 (有锁)
                    instance = new Singleton();  // volatile 写 + StoreLoad barrier
                }
            }
        }
        return instance;                         // volatile 读
    }
}
```

---

### 4.4 NMT 实践

#### 启用与基本使用

```bash
# 启用 NMT (必须在启动时指定, 无法运行时开启)
java -XX:NativeMemoryTracking=summary -jar app.jar   # ~5% 性能开销
java -XX:NativeMemoryTracking=detail -jar app.jar    # ~10% 开销, 含调用栈
```

#### 内存泄漏排查工作流

**Step 1: 建立基线 (baseline)**

```bash
# 应用稳定运行后, 建立基线
jcmd <pid> VM.native_memory baseline
```

**Step 2: 等待一段时间后对比 (diff)**

```bash
# 数小时或数天后, 查看与基线的差异
jcmd <pid> VM.native_memory summary.diff scale=MB
```

**Step 3: 分析 diff 输出**

```
Native Memory Tracking:
  Total: reserved=4523MB +120MB, committed=1234MB +85MB    ← 关注 committed 增长

  -  Java Heap (reserved=2048MB, committed=1024MB)          ← 未增长: 正常
  -       Class (reserved=1056MB, committed=12MB +8MB)      ← 增长: 类加载泄漏?
  -      Thread (reserved=128MB +32MB, committed=128MB +32MB) ← 增长: 线程泄漏?
  -        Code (reserved=250MB, committed=45MB +5MB)       ← 增长: JIT 编译增加
  -    Internal (reserved=5MB +40MB, committed=5MB +40MB)   ← 异常增长: Direct Memory 泄漏!
```

**Step 4: 深入定位 (detail 模式)**

```bash
# detail.diff 可显示每个内存分配的调用栈
jcmd <pid> VM.native_memory detail.diff scale=KB
```

#### 常见泄漏模式与诊断

| 增长区域 | 常见原因 | 排查方向 |
|----------|----------|----------|
| `Class/Metaspace` | ClassLoader 泄漏, 动态代理过多 | 检查自定义 ClassLoader 生命周期 |
| `Thread/ThreadStack` | 线程未关闭, 线程池配置不当 | `jstack` 检查线程数 |
| `Internal` | DirectByteBuffer 泄漏, JNI 内存 | 检查 NIO 代码, `Unsafe.allocateMemory` |
| `Code` | 大量热点方法编译, 去优化循环 | `-XX:+PrintCompilation` |
| `GC` | 堆过大导致 GC 数据结构增长 | 正常现象, 与堆大小成正比 |

---

### 4.5 容器环境内存管理

#### JVM 容器感知 (Container Awareness)

JDK 8u191+ / JDK 10+ 引入容器感知功能，JVM 自动读取 cgroup 限制:

```bash
# 默认启用 (JDK 10+)
-XX:+UseContainerSupport    # 默认 true

# 禁用容器感知 (使用物理机内存)
-XX:-UseContainerSupport
```

**容器感知读取的 cgroup 信息**:
- `memory.limit_in_bytes` (cgroup v1) / `memory.max` (cgroup v2): 内存限制
- `cpu.cfs_quota_us` / `cpu.cfs_period_us`: CPU 配额 (影响 GC 线程数)

#### MaxRAMPercentage 配置

在容器中，推荐使用百分比而非固定值配置堆大小:

```bash
# 容器推荐配置 (堆占容器内存的 75%)
java -XX:MaxRAMPercentage=75.0 \
     -XX:InitialRAMPercentage=50.0 \
     -XX:MinRAMPercentage=50.0 \      # 小内存 (< 256MB) 时的最大堆百分比
     -jar app.jar
```

**参数说明**:

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `MaxRAMPercentage` | 25.0% | 可用内存 > 256MB 时，最大堆占比 |
| `MinRAMPercentage` | 50.0% | 可用内存 <= 256MB 时，最大堆占比 (名字有误导性) |
| `InitialRAMPercentage` | 1.5625% | 初始堆占比 |

> **注意**: `-Xmx` 如果显式指定，会覆盖 `MaxRAMPercentage`。

#### 容器内存预算分配

容器内存不仅仅是 Java 堆，还包含非堆内存。典型 2GB 容器的内存预算:

```
容器内存限制: 2048 MB
├── Java Heap (-Xmx):              ~1400 MB (68%)
├── Metaspace:                     ~100 MB  (5%)
├── Thread Stacks (200 线程 * 1MB): ~200 MB  (10%)
├── Code Cache:                    ~100 MB  (5%)
├── GC 数据结构:                    ~50 MB   (2%)
├── Direct Memory / NIO:           ~100 MB  (5%)
└── OS / 其他:                      ~98 MB   (5%)
```

**OOMKilled 排查**: 容器被 OOMKilled 而 JVM 未报 `OutOfMemoryError`，通常是非堆内存 (native memory) 超出容器限制。使用 NMT 监控总 committed 内存，确保不超过容器 `memory.limit`。

```bash
# 容器安全配置示例 (2GB 容器)
java -XX:+UseContainerSupport \
     -XX:MaxRAMPercentage=65.0 \
     -XX:MaxMetaspaceSize=256m \
     -XX:MaxDirectMemorySize=256m \
     -XX:ReservedCodeCacheSize=128m \
     -Xss512k \
     -XX:NativeMemoryTracking=summary \
     -jar app.jar
```

---

## 5. 最新增强

### JDK 24: AOT 缓存

**JEP 483: Ahead-of-Time Class Loading & Linking**

减少运行时内存分配：

```bash
# 创建 AOT 缓存
java -XX:AOTCacheConfiguration=aot_config.txt \
     -XX:StoreAOTCacheConfiguration \
     MyApp

# 使用 AOT 缓存
java -XX:AOTCacheConfiguration=aot_config.txt \
     MyApp
```

**内存优势**:
- 减少类加载期间内存分配
- 减少元空间使用
- 降低 GC 压力

### JDK 24: 紧凑对象头 (实验)

**JEP 450: Compact Object Headers (Experimental)**

```bash
# JDK 24: 需要 UnlockExperimentalVMOptions
-XX:+UnlockExperimentalVMOptions -XX:+UseCompactObjectHeaders
```

### JDK 25: 紧凑对象头 (正式)

**JEP 519: Compact Object Headers** — Project Lilliput 首个正式集成特性

```bash
# JDK 25+: 生产就绪，不再需要 UnlockExperimentalVMOptions
# 注意: 非默认启用，需显式开启
-XX:+UseCompactObjectHeaders
```

**演进路线**:
- JDK 22: Object Monitor Tables 基础设施
- JDK 24 (JEP 450): 实验性紧凑对象头
- JDK 25 (JEP 519): 正式生产就绪特性 (非默认启用)
- 未来版本: 计划默认启用

**内存节省**:
- 对象头从 12 字节减少到 8 字节 (类指针合并到 Mark Word)
- SPECjbb2015: 堆空间减少 **22%**, CPU 时间减少 **8%**
- 含大量小对象的应用: 总活跃数据内存减少 **10-20%**
- GC 改进: SPECjbb2015 中 G1/Parallel 收集器 GC 周期减少约 **15%**, 标记阶段缩短, GC 暂停减少 **10-15%**

**生产验证**: Amazon 已将此特性反向移植至 JDK 17/21 并在数百个生产服务中部署，测量到一致的效率提升且无回归

---

## 6. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 内存管理 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | 317 | Oracle | 类加载, 运行时 |
| 2 | [Ioi Lam](/by-contributor/profiles/ioi-lam.md) | 215 | Oracle | CDS, AOT, 内存 |
| 3 | [David Holmes](/by-contributor/profiles/david-holmes.md) | 174 | Oracle | 并发, 线程 |
| 4 | Thomas Stuefe | 163 | Red Hat | 内存, 跨平台 |
| 5 | Stefan Karlsson | 149 | Oracle | 并发 GC |
| 6 | Kim Barrett | 113 | Oracle | C++ 现代化 |
| 7 | [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | 112 | Amazon | 性能基准 |
| 8 | Robbin Ehn | 77 | Oracle | 并发, 锁 |
| 9 | Calvin Cheung | 77 | Oracle | 类加载 |
| 10 | Patricio Chilano Mateo | 76 | Oracle | 运行时 |

---

## 7. 重要 PR 分析

### 元空间优化

#### JDK-8349400: 消除匿名内部类

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ 元空间占用 -82%

通过消除枚举中的匿名内部类来减少元空间占用：

**问题**: `KnownOIDs` 枚举有 10 个匿名内部类，每个占用约 1-2KB 元空间

**解决方案**: 将方法覆盖转换为构造函数参数

```java
// 优化前：匿名内部类
KP_TimeStamping("1.3.6.1.5.5.7.3.8", "timeStamping") {
    @Override
    boolean registerNames() { return false; }
}

// 优化后：构造函数参数
KP_TimeStamping("1.3.6.1.5.5.7.3.8", "timeStamping", false)
```

**效果**:
- 类加载数量：11 → 1（-90%）
- 元空间占用：22KB → 4KB（-82%）

→ [详细分析](/by-pr/8349/8349400.md)

### 字符串内存优化

#### JDK-8334328: FloatToDecimal/DoubleToDecimal 优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ +30-50% 性能提升

重构浮点数转字符串实现，减少对象分配：

**优化点**:
- 创建共享实例 (`LATIN1`, `UTF16`)
- 无状态方法设计
- 直接写入 StringBuilder 内部数组

→ [详细分析](/by-pr/8334/8334328.md)

### StringBuilder 内存优化

#### JDK-8355177: append(char[]) 优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ +15% 性能提升

使用 `Unsafe.copyMemory` 替代 `System.arraycopy`：

**内存优势**:
- 减少临时对象创建
- 消除 JNI 边界跨越
- 更好的缓存局部性

→ [详细分析](/by-pr/8355/8355177.md)

---

## 8. 内存优化最佳实践

### 减少元空间占用

```java
// ❌ 避免：匿名内部类
enum MyEnum {
    VALUE {
        @Override
        void method() { /* ... */ }
    }
}

// ✅ 推荐：使用枚举字段或构造函数参数
enum MyEnum {
    VALUE(false);  // 通过参数控制行为
    final boolean flag;
    MyEnum(boolean flag) { this.flag = flag; }
}
```

### 减少对象分配

```java
// ❌ 避免：循环内创建对象
for (int i = 0; i < 1000; i++) {
    String result = prefix + i + suffix;  // 每次创建新对象
}

// ✅ 推荐：使用 StringBuilder
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.setLength(0);
    sb.append(prefix).append(i).append(suffix);
}
```

### 使用对象池

```java
// ✅ 推荐：重用昂贵对象
private static final DateTimeFormatter DATE_FORMATTER =
    DateTimeFormatter.ofPattern("yyyy-MM-dd");

// ❌ 避免：重复创建
for (LocalDate date : dates) {
    DateTimeFormatter formatter =
        DateTimeFormatter.ofPattern("yyyy-MM-dd");  // 每次创建
}
```

---

## 9. 相关链接

### 内部文档

- [内存时间线](timeline.md) - 详细的历史演进
- [Arena 详解](../panama/arena.md) - 堆外内存生命周期管理
- [GC 演进](../gc/) - 垃圾回收器
- [JVM 调优](../jvm/) - JVM 参数调优
- [性能优化](../performance/) - JIT 编译

### 外部资源

- [Tuning Garbage Collectors](https://docs.oracle.com/en/java/javase/21/gctuning/)
- [Java HotSpot VM Options](https://docs.oracle.com/en/java/javase/21/vm-options/)
- [Understanding Metaspace](https://oracle.com/technical-resources/articles/java/javadependencies.html)

### Git 仓库

```bash
# 查看内存管理相关提交
git log --oneline -- src/hotspot/share/memory/
git log --oneline -- src/hotspot/share/oops/
git log --oneline -- src/hotspot/share/classfile/
```

---

**最后更新**: 2026-03-22
