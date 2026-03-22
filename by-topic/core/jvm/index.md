# JVM 内部机制与调优

> **30 秒速读**
> - 执行路径: Template Interpreter → C1 (快速编译) → C2 (深度优化)，分层编译 5 级 (Level 0-4)
> - 对象头: Mark Word 8B + Klass Pointer 4B = 12B (压缩指针)；Compact Headers (JEP 519) 压缩至 8B
> - Safepoint: GC 发起 STW 暂停的协调机制，所有 Java 线程必须到达安全点
> - 核心诊断工具: jcmd (统一诊断)、JFR (飞行记录)、jmap (堆转储)、jstack (线程转储)
> - NMT (Native Memory Tracking): 追踪 JVM 非堆内存使用，定位原生内存泄漏
> - 类加载三层: Bootstrap → Platform → App ClassLoader

> HotSpot 架构、对象模型、字节码执行、Safepoint、NMT、线程模型、启动过程、诊断工具

[← 返回核心平台](../)

---
## 目录

1. [快速概览](#1-快速概览)
2. [核心贡献者](#2-核心贡献者)
3. [HotSpot 架构](#3-hotspot-架构)
4. [对象模型](#4-对象模型)
5. [类加载子系统](#5-类加载子系统)
6. [字节码执行与分层编译](#6-字节码执行与分层编译)
7. [Safepoint 机制](#7-safepoint-机制)
8. [Native Memory Tracking (NMT)](#8-native-memory-tracking-nmt)
9. [线程模型](#9-线程模型)
10. [JVM 启动过程](#10-jvm-启动过程)
11. [JVM 参数](#11-jvm-参数)
12. [诊断工具](#12-诊断工具)
13. [JFR (Java Flight Recorder)](#13-jfr-java-flight-recorder)
14. [JMX 监控](#14-jmx-监控)
15. [常见问题诊断](#15-常见问题诊断)
16. [性能调优](#16-性能调优)
17. [hsdb (HotSpot Debugger)](#17-hsdb-hotspot-debugger)
18. [相关链接](#18-相关链接)

---


## 1. 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 6 ── JDK 7 ── JDK 8 ── JDK 11 ── JDK 17 ── JDK 21 ── JDK 26
   │         │        │        │        │        │        │        │        │
基础参数   JMX    jstat   G1 GC  元空间   ZGC     外部    分代    CDS
-Xmx/-Xms  jconsole jmap   默认  Metaspace 低延迟   函数    ZGC     简化
          jstack  jinfo   JFR   字符串   生产就绪  (FFM)  生产     (JEP 467)
```

### 核心工具

| 工具 | 首发版本 | 用途 | 类型 |
|------|----------|------|------|
| **jstat** | JDK 6 | GC 统计 | 命令行 |
| **jmap** | JDK 6 | 堆转储 | 命令行 |
| **jstack** | JDK 5 | 线程转储 | 命令行 |
| **jinfo** | JDK 5 | JVM 配置 | 命令行 |
| **jcmd** | JDK 7 | 统一诊断 | 命令行 |
| **jconsole** | JDK 5 | JMX 监控 | GUI |
| **jvisualvm** | JDK 6 (JDK 9 起移除，改为独立项目 VisualVM) | 综合分析 | GUI |
| **JFR** | JDK 7u40 (商业), JDK 11 (开源, JEP 328) | 飞行记录 | 生产级 |
| **JMC** | JDK 7 | Mission Control | GUI |

---

## 2. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### JVM 运行时团队 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | 317 | Oracle | 类加载, 运行时核心 |
| 2 | [Ioi Lam](/by-contributor/profiles/ioi-lam.md) | 215 | Oracle | CDS, AOT, 运行时 |
| 3 | [David Holmes](/by-contributor/profiles/david-holmes.md) | 174 | Oracle | 并发, 线程, 规范 |
| 4 | Thomas Stuefe | 163 | Red Hat | 内存, 跨平台 |
| 5 | Stefan Karlsson | 149 | Oracle | 并发 GC |
| 6 | Kim Barrett | 113 | Oracle | C++ 现代化 |
| 7 | [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | 112 | Amazon | 性能基准 |
| 8 | Daniel D. Daugherty | 87 | Oracle | JVMTI, 调试 |
| 9 | Robbin Ehn | 77 | Oracle | 并发, 锁 |
| 10 | Calvin Cheung | 77 | Oracle | 类加载 |

---

## 3. HotSpot 架构

HotSpot VM 是 OpenJDK 的核心执行引擎，内部由多个紧密协作的子系统组成。

### 子系统总览

```
┌─────────────────────────────────────────────────────────────────┐
│                        Java Application                         │
├─────────────────────────────────────────────────────────────────┤
│                     Class Loading Subsystem                     │
│              (Bootstrap / Platform / App ClassLoader)           │
├──────────┬──────────────────────────────────┬───────────────────┤
│          │        Execution Engine          │                   │
│ Runtime  │  ┌────────────┐  ┌───────────┐  │  Memory Manager   │
│ System   │  │ Interpreter│  │ JIT       │  │  ┌─────────────┐  │
│          │  │ (Template) │  │ Compilers │  │  │ GC Subsystem│  │
│ Safepoint│  │            │→ │ C1 → C2   │  │  │ G1/ZGC/...  │  │
│ Thread   │  └────────────┘  └───────────┘  │  └─────────────┘  │
│ Sync     │                                 │  Heap / Metaspace │
│ JVMTI    │        Code Cache               │  NMT              │
├──────────┴──────────────────────────────────┴───────────────────┤
│                          OS Interface                           │
│              (Thread, Memory, Signal, I/O)                      │
└─────────────────────────────────────────────────────────────────┘
```

### 解释器 (Template Interpreter)

HotSpot 使用 **Template Interpreter** 而非传统的 switch-case 解释器。启动时，解释器为每个字节码指令预生成一段本地机器码模板 (template)，存储在一块连续的内存区域中。执行字节码时，直接跳转到对应模板的入口地址，避免了 switch 分发的开销。

**源码位置**: `src/hotspot/share/interpreter/templateInterpreter.cpp`, `templateTable.cpp`

关键流程:
1. `TemplateTable::initialize()` — 在 VM 启动时注册每个字节码对应的生成函数
2. `TemplateInterpreterGenerator::generate_all()` — 遍历所有字节码，调用生成函数输出机器码
3. 运行时通过 dispatch table (分发表) 直接索引到模板入口

### JIT 编译器 (C1 / C2)

| 属性 | C1 (Client Compiler) | C2 (Server Compiler) |
|------|----------------------|----------------------|
| 编译速度 | 快 | 慢 |
| 优化深度 | 基础优化 | 激进优化 (逃逸分析、标量替换、循环展开) |
| 代码质量 | 中等 | 高 |
| 典型用途 | 快速启动、短生命周期方法 | 热点方法的深度优化 |

分层编译 (Tiered Compilation) 默认启用，编译级别定义于 `src/hotspot/share/compiler/compilerDefinitions.hpp`:

| 级别 | 名称 | 含义 |
|------|------|------|
| 0 | `CompLevel_none` | 纯解释执行 (Interpreter) |
| 1 | `CompLevel_simple` | C1 编译，无 profiling |
| 2 | `CompLevel_limited_profile` | C1 编译 + 调用计数器 & 回边计数器 |
| 3 | `CompLevel_full_profile` | C1 编译 + 完整 profiling (含 MDO) |
| 4 | `CompLevel_full_optimization` | C2 或 JVMCI 完全优化编译 |

### 运行时系统 (Runtime)

运行时系统提供 JVM 运行所需的核心服务，源码集中在 `src/hotspot/share/runtime/`:

- **thread.cpp / threads.cpp** — 线程生命周期管理
- **safepoint.cpp** — Safepoint 协调
- **deoptimization.cpp** — 逆优化 (从编译代码回退到解释器)
- **continuation.cpp** — Virtual Thread 的 continuation 实现
- **frame.cpp** — 栈帧管理

### GC 子系统

GC 子系统独立于执行引擎，但通过 Safepoint 和 Barrier 与之协作:

- **Safepoint** — GC 发起 STW (Stop-The-World) 暂停时，通过 safepoint 使所有 Java 线程到达安全点
- **Write Barrier** — ZGC、G1 等收集器在对象引用写入时插入屏障，维护 remembered set 或 colored pointer
- **Read Barrier** — ZGC 使用 load barrier 支持并发 relocation

---

## 4. 对象模型

### 对象内存布局

每个 Java 对象在堆中的布局由三部分组成:

```
┌──────────────────────────────────────────────┐
│              Object Header                    │
│  ┌──────────────────────────────────────────┐ │
│  │  Mark Word (8 bytes on 64-bit)          │ │
│  ├──────────────────────────────────────────┤ │
│  │  Klass Pointer (4 or 8 bytes)           │ │
│  └──────────────────────────────────────────┘ │
├──────────────────────────────────────────────┤
│            Instance Fields                    │
│         (按对齐规则排列)                       │
├──────────────────────────────────────────────┤
│              Padding                          │
│         (补齐到 8 字节对齐)                    │
└──────────────────────────────────────────────┘
```

### Mark Word 详解

Mark Word 是对象头的第一个机器字 (machine word)，定义于 `src/hotspot/share/oops/markWord.hpp`。64 位 JVM 上的位布局:

```
普通对象 (64 bits):
unused:22  hash:31 ──→  unused_gap:4  age:4  self-fwd:1  lock:2

压缩对象头 (64 bits, Compact Headers):
klass:22   hash:31 ──→  unused_gap:4  age:4  self-fwd:1  lock:2
```

**lock 位编码**:

| 位模式 | 状态 | 含义 |
|--------|------|------|
| `00` | locked | Stack-locking: mark word 指向栈上的 BasicLock 副本; Fast-locking: 直接锁定的 header |
| `01` | unlocked | 正常未锁定状态 |
| `10` | monitor | 膨胀锁 (inflated lock)，关联 ObjectMonitor |
| `11` | marked | GC 标记用 |

**关键字段**:
- **hash (31 bits)** — identity hash code，首次调用 `System.identityHashCode()` 时计算并缓存
- **age (4 bits)** — GC 分代年龄，最大 15 (即 `-XX:MaxTenuringThreshold` 的上限)
- **self-fwd (1 bit)** — 自转发标记，GC relocation 使用

### Klass Pointer

对象头的第二部分是 Klass Pointer，指向该对象的类元数据 (`Klass` 结构，存储在 Metaspace 中)。

- 未压缩时: 8 字节 (64-bit 指针)
- 压缩时 (`-XX:+UseCompressedClassPointers`): 4 字节 (32-bit narrowKlass)

### 压缩指针 (CompressedOops)

当堆大小 < 32 GB 时，JVM 自动启用 CompressedOops (`-XX:+UseCompressedOops`)，将 64 位对象引用压缩为 32 位:

```
实际地址 = narrowOop << 3 + base
```

- **Zero-based**: 如果堆起始地址 = 0 且堆 < 4 GB，base = 0，shift = 0
- **Zero-based + shift**: 堆 < 32 GB，base = 0，shift = 3 (因为对象 8 字节对齐)
- **Non-zero-based**: 堆起始地址 ≠ 0，需要 base + shift

压缩类指针 (`UseCompressedClassPointers`) 的编码原理类似，但作用于 Klass Pointer。编码方案定义于 `src/hotspot/share/oops/compressedKlass.hpp`:
- Encoding Range 覆盖整个 Klass Range (CDS + class space)
- 支持 zero-based 和 non-zero-based 两种模式

### 压缩对象头 — Compact Object Headers (JEP 450 / Lilliput)

传统对象头 = Mark Word (8 bytes) + Klass Pointer (4 bytes, 压缩) = **12 bytes**，加上 padding 对齐到 **16 bytes**。

Compact Object Headers 将 Klass 信息 (22 bits) 编码进 Mark Word 的高位，从而将对象头压缩到 **8 bytes**:

```
压缩前: [mark word: 8B] [klass ptr: 4B] [padding: 4B] = 16B 最小对象
压缩后: [mark word + klass: 8B]                        =  8B 最小对象
```

- **JDK 24**: JEP 450 实验性引入 (`-XX:+UnlockExperimentalVMOptions -XX:+UseCompactObjectHeaders`)
- **JDK 26**: 实验性 (`-XX:+UnlockExperimentalVMOptions -XX:+UseCompactObjectHeaders`)，参见 JEP 519

**内存节省**: 典型应用中，对象头开销占堆的 10-20%，压缩后可节省 ~10% 堆空间。

### 对象对齐

- 默认对象对齐: 8 字节 (`-XX:ObjectAlignmentInBytes=8`)
- 可配置值: 8, 16, 32, ... , 256
- 增大对齐值可扩大 CompressedOops 的寻址范围 (例如 16 字节对齐支持 64 GB 堆)，但会增加内存浪费
- 数组的元素按自然对齐排列 (int 按 4 字节, long 按 8 字节)

---

## 5. 类加载子系统

### 三层 ClassLoader 架构

```
┌─────────────────────────────────────┐
│       Bootstrap ClassLoader         │  (C++ 实现, 加载 java.base 等核心模块)
│       加载: java.lang.*, etc.       │
├─────────────────────────────────────┤
│        Platform ClassLoader         │  (JDK 9+ 替代 Extension ClassLoader)
│       加载: java.sql, java.xml, etc.│
├─────────────────────────────────────┤
│      Application ClassLoader        │  (加载 classpath / modulepath 上的类)
│       加载: 用户应用类               │
└─────────────────────────────────────┘
```

**源码位置**: `src/hotspot/share/classfile/classLoader.cpp`, `classLoaderData.cpp`

### 双亲委派模型 (Parent Delegation Model)

```
加载请求 → Application ClassLoader
               ↓ 委派给 parent
           Platform ClassLoader
               ↓ 委派给 parent
           Bootstrap ClassLoader
               ↓ 尝试加载
           如果 Bootstrap 找到 → 返回
           否则回退到 Platform → 尝试加载
           否则回退到 Application → 尝试加载
           都找不到 → ClassNotFoundException
```

核心目的:
1. **安全性** — 防止用户代码替换核心类 (如 `java.lang.String`)
2. **唯一性** — 同一个类只被一个 ClassLoader 加载一次
3. **可见性** — 子 loader 可看到父 loader 的类，反之不行

### 模块化后的变化 (JPMS, JDK 9+)

JDK 9 引入 Java Platform Module System 后，类加载发生了重要变化:

| 变化 | JDK 8 及之前 | JDK 9+ |
|------|-------------|--------|
| Extension ClassLoader | 加载 `jre/lib/ext/` 下的 JAR | 改名为 **Platform ClassLoader**，加载平台模块 |
| Bootstrap 加载范围 | `rt.jar` (整个核心库) | 仅加载 `java.base` 等关键模块 |
| 类路径 | 单一 classpath | classpath + modulepath 双路径 |
| 可见性 | 基于 ClassLoader 层级 | 基于 `module-info.java` 中的 `exports` / `opens` 声明 |

### 类加载过程

```
Loading (加载) → Linking (链接) → Initialization (初始化)
                    │
         ┌──────────┼──────────┐
    Verification  Preparation  Resolution
    (校验字节码)  (分配静态字段)  (符号→直接引用)
```

- **Loading**: 读取 `.class` 文件，创建 `InstanceKlass` 对象 (源码: `classFileParser.cpp`)
- **Verification**: 校验字节码合法性 (魔数、版本、类型安全)
- **Preparation**: 为静态字段分配内存并赋零值
- **Resolution**: 将常量池中的符号引用解析为直接引用 (可延迟到首次使用)
- **Initialization**: 执行 `<clinit>` (类初始化方法)

### ClassLoaderData

HotSpot 内部使用 `ClassLoaderData` (CLD) 结构管理每个 ClassLoader 加载的所有类元数据。CLD 构成一个全局链表 (`ClassLoaderDataGraph`)，GC 通过遍历此链表判断哪些类/元数据可以卸载。

**源码位置**: `src/hotspot/share/classfile/classLoaderData.cpp`, `classLoaderDataGraph.cpp`

---

## 6. 字节码执行与分层编译

### Template Interpreter 工作原理

Template Interpreter 在 VM 启动时为每个字节码生成一段平台相关的机器码:

```
  字节码           Template (机器码片段)
┌─────────┐     ┌──────────────────────┐
│ iload_0 │ →   │ mov eax, [rbx+off]   │  (从局部变量表加载 int)
│ iload_1 │ →   │ mov ecx, [rbx+off+4] │
│ iadd    │ →   │ add eax, ecx         │  (栈顶两个 int 相加)
│ ireturn │ →   │ ... return sequence  │
└─────────┘     └──────────────────────┘
```

**Dispatch 机制**: 每个模板的末尾包含一个 dispatch 序列 — 读取下一个字节码，查 dispatch table 获取目标模板地址，直接跳转。这实现了线程化解释 (threaded interpretation)，避免了回到中央分发循环的开销。

**源码位置**: `src/hotspot/share/interpreter/templateTable.cpp` (平台无关), `src/hotspot/cpu/x86/templateTable_x86.cpp` (x86 平台实现)

### 分层编译触发流程

```
方法首次调用
    │
    ▼
Level 0: Interpreter ─── 收集调用计数 (invocation counter)
    │                      和回边计数 (backedge counter)
    │ 达到阈值
    ▼
Level 3: C1 + Full Profile ─── 收集完整 profiling 数据
    │                            (类型信息、分支概率、MDO)
    │ 达到阈值 + 足够 profile
    ▼
Level 4: C2 Full Optimization ─── 基于 profile 进行激进优化
                                    (逃逸分析、内联、循环优化)
```

**注意**: 编译策略并非总是 0→3→4 的线性路径。`CompilationPolicy` 会根据情况选择:
- **0→1**: 简单方法直接 C1 编译 (无需 profiling)
- **0→3→4**: 标准热点方法路径
- **0→2→4**: 中间 profiling 路径
- **4→0 (Deoptimization)**: 当 C2 的推测性优化 (speculative optimization) 失败时，逆优化回解释器

### On-Stack Replacement (OSR)

对于长时间运行的循环，JVM 不等循环结束就将其编译并替换 — 在循环 **运行过程中** 从解释器切换到编译代码。触发条件由回边计数器 (backedge counter) 控制，参数 `-XX:OnStackReplacePercentage` 调整阈值。

### Deoptimization (逆优化)

当编译代码中的假设不再成立时 (如类层次结构变化导致虚方法调用去虚化失败)，JVM 会:

1. 在下一个 safepoint 暂停编译代码的执行
2. 将编译帧 (compiled frame) 转换为解释帧 (interpreter frame)
3. 从解释器继续执行
4. 后续可能重新触发编译

**源码位置**: `src/hotspot/share/runtime/deoptimization.cpp`

---

## 7. Safepoint 机制

### 什么是 Safepoint

Safepoint (安全点) 是程序执行中的特定位置，此时:
- 所有 GC root 都是已知的
- 所有对象引用都在确定的位置 (寄存器、栈、内存)
- JVM 可以安全地检查和修改堆

**源码位置**: `src/hotspot/share/runtime/safepoint.cpp`, `safepointMechanism.cpp`

### 为什么需要 STW (Stop-The-World)

某些 VM 操作需要**全局一致视图** (consistent view)，必须暂停所有 Java 线程:

| STW 操作 | 原因 |
|-----------|------|
| GC 标记根 | 需要准确的 root set |
| Deoptimization | 需要修改线程栈帧 |
| 线程转储 | 需要稳定的栈快照 |
| 偏向锁撤销 (已移除) | 需要修改对象头 |
| 类重定义 (JVMTI) | 需要替换方法入口 |
| 代码缓存清理 | 需要确保无线程执行被清理的代码 |

### Safepoint 状态机

VMThread 通过 `SafepointSynchronize` 管理全局安全点，三个状态定义于 `safepoint.hpp`:

```
_not_synchronized (0) ─→ _synchronizing (1) ─→ _synchronized (2)
       ↑                                              │
       └──────────────────────────────────────────────┘
```

- `_not_synchronized`: 正常执行，线程自由运行
- `_synchronizing`: VMThread 发起 safepoint 请求，等待所有 Java 线程到达安全点
- `_synchronized`: 所有 Java 线程已停在安全点，VMThread 执行 VM 操作

### Polling 机制

HotSpot 使用 **thread-local poll** 机制实现 safepoint (源码: `safepointMechanism.hpp`):

```
每个 JavaThread 持有:
  _polling_word  ─ 轮询字
  _polling_page  ─ 轮询页地址

正常状态: polling_page 指向可读的 good page
ARM 状态:  polling_page 指向不可读的 bad page → 触发 SIGSEGV → 进入 safepoint handler
```

**插入 poll 的位置** (编译器生成的代码中):
- 方法返回 (return)
- 回边 (backedge，即循环跳转)
- JNI 方法调用返回后

### Safepoint poll 在解释器 vs 编译代码中的区别

| 执行模式 | 检查方式 |
|----------|---------|
| Interpreter | 在 dispatch 时检查 `_polling_word` |
| C1/C2 编译代码 | 在方法出口和循环回边插入 poll 指令 (load from polling page) |
| JNI 代码 | 从 native 返回时检查 |
| 阻塞在 OS (sleep/wait) | 已处于安全状态，无需 poll |

### Time-to-Safepoint (TTSP) 优化

TTSP 是从发起 safepoint 请求到所有线程到达安全点的时间。高 TTSP 会增加暂停延迟。

**常见 TTSP 瓶颈**:
- **Counted loops**: 没有 safepoint poll 的计数循环 (C2 优化去掉了 poll)
- **长时间 JNI 调用**: 线程在 native 代码中不响应 safepoint
- **大量线程**: 需要等待所有线程到达

**诊断**: 使用 `-Xlog:safepoint` 查看 safepoint 时间:

```bash
# 输出 safepoint 详细信息
-Xlog:safepoint=debug

# JFR 事件
jfr print --events jdk.SafepointBegin,jdk.SafepointEnd recording.jfr
```

**JDK 优化历史**:
- JDK 10: Loop strip mining (JDK-8186027) — 将大循环拆分为带 safepoint poll 的外层循环
- JDK 10+: Thread-local handshake (JEP 312) — 允许对单个线程执行操作，无需全局 STW

---

## 8. Native Memory Tracking (NMT)

### 启用 NMT

NMT 跟踪 JVM **本地内存** (非堆内存) 的分配，帮助分析内存泄漏和调优。

```bash
# Summary 模式 (性能开销 ~5%)
java -XX:NativeMemoryTracking=summary -jar app.jar

# Detail 模式 (性能开销 ~10%，记录调用栈)
java -XX:NativeMemoryTracking=detail -jar app.jar
```

**注意**: NMT 必须在启动时通过 `-XX:NativeMemoryTracking` 开启，无法运行时动态开启。

### 使用 jcmd 查看 NMT 数据

```bash
# 查看内存概要
jcmd <pid> VM.native_memory summary

# 查看详细信息 (含调用栈)
jcmd <pid> VM.native_memory detail

# 设置基线 (用于对比)
jcmd <pid> VM.native_memory baseline

# 与基线对比 (发现内存增长)
jcmd <pid> VM.native_memory summary.diff
jcmd <pid> VM.native_memory detail.diff

# 按比例缩放输出单位
jcmd <pid> VM.native_memory summary scale=MB
```

### 内存区域分类

NMT 按内存标签 (MemTag) 分类，定义于 `src/hotspot/share/nmt/memTag.hpp`:

| MemTag | 中文名称 | 包含内容 |
|--------|----------|----------|
| `mtJavaHeap` | Java 堆 | 对象实例、数组 |
| `mtClass` | 类 | Klass 结构、常量池、方法元数据 |
| `mtThread` | 线程 | 线程对象本身的内存 |
| `mtThreadStack` | 线程栈 | 每个线程的栈空间 (由 `-Xss` 控制) |
| `mtCode` | 代码 | JIT 编译的机器码 (Code Cache) |
| `mtGC` | GC | GC 数据结构 (card table, remembered set) |
| `mtGCCardSet` | GC Card Set | G1 card set remembered set |
| `mtCompiler` | 编译器 | C1/C2 编译器工作内存 |
| `mtInternal` | 内部 | VM 内部使用的其他内存 |
| `mtSymbol` | 符号 | 字符串表、符号表 |
| `mtMetaspace` | Metaspace | 类元数据空间 |
| `mtNMT` | NMT | NMT 自身的簿记开销 |
| `mtClassShared` | 共享类空间 | CDS (Class Data Sharing) 映射 |
| `mtModule` | 模块 | JPMS 模块数据 |
| `mtSafepoint` | Safepoint | Safepoint 机制数据 |
| `mtSynchronizer` | 同步 | ObjectMonitor 等同步结构 |
| `mtServiceability` | 服务性 | JVMTI、诊断命令 |
| `mtStringDedup` | 字符串去重 | G1 字符串去重数据 |

### NMT 输出示例解读

```
Native Memory Tracking:
  Total: reserved=4523MB, committed=1234MB

  -  Java Heap (reserved=2048MB, committed=1024MB)   ← 堆内存
  -       Class (reserved=1056MB, committed=12MB)     ← 类元数据
  -      Thread (reserved=128MB,  committed=128MB)    ← 线程栈
  -        Code (reserved=250MB,  committed=45MB)     ← Code Cache
  -          GC (reserved=85MB,   committed=23MB)     ← GC 数据
  -    Internal (reserved=5MB,    committed=5MB)      ← 内部
  -      Symbol (reserved=10MB,   committed=10MB)     ← 符号表
```

- **reserved**: 已预留的虚拟地址空间 (未必有物理内存支撑)
- **committed**: 已提交的内存 (有物理内存或 swap 支撑)

---

## 9. 线程模型

### OS Thread vs Virtual Thread

| 属性 | Platform Thread (OS Thread) | Virtual Thread (JDK 21+) |
|------|----------------------------|--------------------------|
| 实现 | 1:1 映射到 OS 线程 | M:N 调度在 carrier thread 上 |
| 栈大小 | 默认 1 MB (`-Xss`) | 动态增长，初始很小 |
| 创建开销 | 重量级 (OS 资源) | 轻量级 (堆上分配) |
| 数量限制 | 通常 < 数千 | 可达百万级 |
| 调度 | OS 调度器 | JVM ForkJoinPool |
| 典型用途 | CPU 密集型 | I/O 密集型、高并发服务 |

Virtual Thread 的核心机制是 **Continuation** (续体): 当虚拟线程阻塞在 I/O 时，JVM 将其栈帧从 carrier thread 上 "卸载" (unmount) 到堆中，carrier thread 可以运行其他虚拟线程。I/O 完成后，虚拟线程被 "装载" (mount) 到某个 carrier thread 上继续执行。

**源码位置**: `src/hotspot/share/runtime/continuation.cpp`, `continuationFreezeThaw.cpp`

### Thread 状态机

Java 线程在 JVM 内部有两套状态体系:

**Java 层 (`Thread.State`)**:
```
NEW → RUNNABLE → { BLOCKED | WAITING | TIMED_WAITING } → TERMINATED
```

**JVM 内部 (`JavaThreadState`)**:
```
_thread_new          → 刚创建
_thread_in_vm        → 执行 VM 代码 (runtime calls)
_thread_in_Java      → 执行 Java 代码 (解释器或编译代码)
_thread_in_native    → 执行 JNI native 代码
_thread_blocked      → 阻塞 (在 OS 原语上)
```

**状态转换与 Safepoint 的关系**:
- `_thread_in_Java` → 需要在 safepoint poll 处检查
- `_thread_in_native` → 被视为安全状态 (GC 不移动 JNI 直接引用的对象)
- `_thread_in_vm` → 在 VM 代码中可能需要检查 safepoint
- `_thread_blocked` → 已安全

### 线程栈管理

```
┌──────────────────┐  ← 栈顶 (低地址)
│   Guard Pages    │  ← 防止栈溢出 (SIGSEGV)
│  (Yellow + Red)  │
├──────────────────┤
│                  │
│   Stack Frames   │  ← 方法调用帧 (局部变量, 操作数栈)
│                  │
├──────────────────┤
│   Reserved Zone  │  ← 保留区域 (用于关键代码的栈空间)
└──────────────────┘  ← 栈底 (高地址)
```

- **Yellow Guard Page**: 首次触及时抛出 `StackOverflowError`，允许异常处理
- **Red Guard Page**: 最终保护，触及时直接终止 VM
- 栈大小由 `-Xss` 控制 (默认 1 MB，平台相关)

---

## 10. JVM 启动过程

JVM 启动由 `Threads::create_vm()` 驱动 (源码: `src/hotspot/share/runtime/threads.cpp`)，主要流程:

```
JNI_CreateJavaVM()
    │
    ▼
Threads::create_vm()
    │
    ├── VM_Version::early_initialize()      ← CPU 特性检测
    ├── os::init()                          ← OS 层初始化
    ├── Arguments::parse(args)              ← 解析 JVM 参数
    ├── MemTracker::initialize()            ← 初始化 NMT
    ├── Arguments::apply_ergo()             ← 应用人体工程学默认值
    ├── os::init_2()                        ← OS 深度初始化
    ├── SafepointMechanism::initialize()    ← 初始化 safepoint polling page
    ├── JvmtiAgentList::load_agents()       ← 加载 JVMTI agent
    │
    ├── vm_init_globals()                   ← 初始化全局数据结构
    │      ├── 创建主线程 JavaThread
    │      ├── ObjectMonitor::Initialize()
    │      └── ObjectSynchronizer::initialize()
    │
    ├── init_globals()                      ← 初始化核心子系统
    │      ├── Universe::initialize_heap()  ← 创建堆 (选择 GC)
    │      ├── Interpreter::initialize()    ← 生成解释器模板
    │      ├── CodeCache::initialize()      ← 初始化代码缓存
    │      └── CompileBroker::init()        ← 初始化编译器线程
    │
    ├── WatcherThread::start()              ← 启动看门狗线程
    │
    ├── init_globals2()                     ← 二阶段初始化
    │      ├── 初始化 java.lang.Class 等核心类
    │      ├── 创建 system ThreadGroup
    │      └── 创建 main Thread 对象
    │
    ├── JFR::on_create_vm_1/2/3()           ← JFR 初始化
    │
    └── 调用 Java main() 方法               ← 进入用户代码
```

### 关键阶段说明

1. **参数解析阶段**: 解析 `-XX:` 标志，应用 ergonomics (自动根据硬件调整参数)
2. **堆初始化**: 根据 GC 策略创建堆结构 (G1 的 Region, ZGC 的 colored pages 等)
3. **解释器生成**: Template Interpreter 为所有字节码生成机器码模板
4. **核心类加载**: Bootstrap ClassLoader 加载 `java.lang.Object`, `java.lang.Class`, `java.lang.String` 等基础类
5. **编译器线程启动**: C1/C2 编译器线程开始监听编译请求队列

---

## 11. JVM 参数

### 内存参数

```bash
# 堆内存
-Xms2g                    # 初始堆大小
-Xmx4g                    # 最大堆大小
-XX:NewSize=512m          # 新生代大小
-XX:MaxNewSize=1g         # 最大新生代
-XX:MetaspaceSize=256m    # 元空间初始大小
-XX:MaxMetaspaceSize=512m # 元空间最大大小

# 线程栈
-Xss1m                    # 线程栈大小

# 本地内存
-XX:MaxDirectMemorySize=1g # 直接内存最大值
```

### GC 参数

```bash
# GC 选择
-XX:+UseG1GC              # G1 GC (JDK 9+ 默认)
-XX:+UseZGC               # ZGC
-XX:+UseShenandoahGC      # Shenandoah GC
-XX:+UseSerialGC          # Serial GC
-XX:+UseParallelGC        # Parallel GC

# G1 调优
-XX:MaxGCPauseMillis=200  # 目标暂停时间
-XX:G1HeapRegionSize=16m  # Region 大小
-XX:G1ReservePercent=10   # 保留堆比例

# ZGC 调优
                              # 分代 ZGC: JDK 21 -XX:+ZGenerational, JDK 24 起默认分代 (该 flag 已移除)
-XX:ZCollectionInterval=5 # GC 间隔
```

### JIT 参数

```bash
# 编译器
-XX:+UseTieredCompilation # 分层编译 (默认)
-XX:TieredStopAtLevel=4   # 最高编译级别

# 代码缓存
-XX:ReservedCodeCacheSize=256m # 代码缓存大小
-XX:InitialCodeCacheSize=32m   # 初始代码缓存

# 编译阈值
-XX:CompileThreshold=10000     # C2 编译阈值
-XX:OnStackReplacePercentage=140  # OSR 百分比
```

### 性能参数

```bash
# 字符串去重 (JDK 8u20+)
-XX:+UseStringDeduplication

# 压缩普通对象指针
-XX:+UseCompressedOops       # 自动启用 (<32GB)
-XX:+UseCompressedClassPointers  # 压缩类指针

# 紧凑对象头 (JDK 26)
-XX:+UseCompactObjectHeaders

# 偏向锁 (已废弃: JDK 15 废弃, JDK 18 移除)
# 注意: 以下参数在 JDK 18+ 中不再可用
# -XX:+UseBiasedLocking
# -XX:BiasedLockingStartupDelay=0
```

### 日志参数

```bash
# JDK 9+ 统一日志
-Xlog:gc                    # GC 日志
-Xlog:gc*:file=gc.log:time,level,tags  # 详细 GC 日志

# 类加载日志
-Xlog:class+load=info

# JIT 编译日志
-Xlog:compilation

# Safepoint 日志
-Xlog:safepoint

# 错误日志
-XX:ErrorFile=/var/log/java/hs_err_pid%p.log
```

---

## 12. 诊断工具

### jcmd — 统一诊断命令 (推荐)

`jcmd` 是 JDK 7+ 引入的统一诊断接口，可替代 jmap、jstack、jinfo 的大部分功能。

```bash
# 查看所有可用命令
jcmd <pid> help

# GC 相关
jcmd <pid> GC.heap_dump /tmp/heap.hprof   # 堆转储
jcmd <pid> GC.heap_info                    # 堆概览
jcmd <pid> GC.run                          # 触发 GC

# 线程相关
jcmd <pid> Thread.print                    # 线程转储 (含虚拟线程)

# 类加载
jcmd <pid> VM.classloader_stats            # ClassLoader 统计

# VM 信息
jcmd <pid> VM.info                         # 综合 VM 信息
jcmd <pid> VM.version                      # 版本信息
jcmd <pid> VM.command_line                 # 启动命令行
jcmd <pid> VM.system_properties            # 系统属性
jcmd <pid> VM.flags                        # 所有 VM flags

# 动态设置标志
jcmd <pid> VM.set_flag PrintGCDetails true  # 注意: PrintGCDetails 已废弃 (JDK 9+), 推荐使用 -Xlog:gc*

# NMT (需启动时开启 NativeMemoryTracking)
jcmd <pid> VM.native_memory summary        # NMT 概要
jcmd <pid> VM.native_memory detail         # NMT 详细
jcmd <pid> VM.native_memory baseline       # 设置基线
jcmd <pid> VM.native_memory summary.diff   # 与基线对比
```

### jinfo — JVM 配置查看与动态修改

```bash
# 查看所有 JVM 参数
jinfo -flags <pid>

# 查看特定参数
jinfo -flag UseG1GC <pid>

# 动态修改可写参数 (manageable 标志)
jinfo -flag +PrintGCDetails <pid>
jinfo -flag -PrintGCDetails <pid>

# 查看系统属性
jinfo -sysprops <pid>
```

### jmap — 堆内存分析

```bash
# 生成堆转储 (hprof 格式)
jmap -dump:format=b,file=heap.hprof <pid>

# 仅转储存活对象 (先触发 Full GC)
jmap -dump:live,format=b,file=heap_live.hprof <pid>

# 查看堆配置和使用情况
jmap -heap <pid>

# 查看类加载器统计
jmap -clstats <pid>

# 查看等待 finalization 的对象
jmap -finalizerinfo <pid>
```

**注意**: 在生产环境中优先使用 `jcmd <pid> GC.heap_dump`，因为 jmap 在某些情况下可能导致目标 JVM 暂停较长时间。

### jstack — 线程转储

```bash
# 基本线程转储
jstack <pid>

# 包含锁信息的线程转储
jstack -l <pid>

# 输出到文件
jstack <pid> > thread_dump.txt

# 多次采样分析热点
for i in {1..5}; do jstack <pid> > td_$i.txt; sleep 3; done
```

### jstat — GC 和 JIT 统计

```bash
# GC 统计 (每秒更新, 10 次)
jstat -gc <pid> 1000 10

# 类加载统计
jstat -class <pid> 1000

# 编译统计
jstat -compiler <pid>

# 各代容量统计
jstat -gccapacity <pid>

# 新生代统计
jstat -gcnew <pid>

# GC 原因统计
jstat -gccause <pid> 1000
```

---

## 13. JFR (Java Flight Recorder)

### 启用 JFR

```bash
# 启动时启用
java -XX:StartFlightRecording=filename=recording.jfr,duration=60s ...

# 运行时启用
jcmd <pid> JFR.start name=myrecording dumponexit=true

# 停止并导出
jcmd <pid> JFR.stop name=myrecording
jcmd <pid> JFR.dump name=myrecording filename=recording.jfr
```

### JFR 分析

```bash
# 使用 JDK Mission Control
jmc

# 命令行打印
jfr print recording.jfr

# 打印特定事件
jfr print --events jdk.GarbageCollection recording.jfr

# 汇总
jfr summary recording.jfr

# 按线程过滤
jfr print --events jdk.ExecutionSample --stack-depth 10 recording.jfr
```

---

## 14. JMX 监控

### 启用 JMX

```bash
# 本地监控
java -Dcom.sun.management.jmxremote ...

# 远程监控 (不安全)
java -Dcom.sun.management.jmxremote.port=9010 \
     -Dcom.sun.management.jmxremote.authenticate=false \
     -Dcom.sun.management.jmxremote.ssl=false ...

# 远程监控 (安全)
java -Dcom.sun.management.jmxremote.port=9010 \
     -Dcom.sun.management.jmxremote.authenticate=true \
     -Dcom.sun.management.jmxremote.password.file=jmxremote.password \
     -Dcom.sun.management.jmxremote.access.file=jmxremote.access \
     -Dcom.sun.management.jmxremote.ssl=true \
     ...
```

---

## 15. 常见问题诊断

### 内存泄漏

**症状**: OOM: Java heap space

**诊断**:
```bash
# 1. 堆转储
jmap -dump:format=b,file=heap.hprof <pid>

# 2. 使用 MAT/Eclipse 分析
# 3. 查找 Dominator Tree
# 4. 查找 Leak Suspects
```

### 本地内存泄漏

**症状**: RSS 持续增长，但堆使用正常

**诊断**:
```bash
# 1. 启动时开启 NMT
java -XX:NativeMemoryTracking=detail -jar app.jar

# 2. 设置基线
jcmd <pid> VM.native_memory baseline

# 3. 一段时间后对比
jcmd <pid> VM.native_memory detail.diff

# 4. 关注 committed 持续增长的区域
```

### Safepoint 延迟

**症状**: 应用出现周期性卡顿，GC 日志显示暂停时间正常

**诊断**:
```bash
# 1. 开启 safepoint 日志
-Xlog:safepoint=debug

# 2. 使用 JFR 分析
jfr print --events jdk.SafepointBegin recording.jfr

# 3. 关注 "Reaching safepoint" 耗时
# 4. 检查是否有长时间 counted loop 或 JNI 调用
```

---

## 16. 性能调优

### 启动优化

```bash
# AppCDS (应用类数据共享)
java -XX:DumpLoadedClassList=classes.lst -cp app.jar Main
java -Xshare:dump -XX:SharedClassListFile=classes.lst \
    -XX:SharedArchiveFile=app.jsa -cp app.jar
java -Xshare:on -XX:SharedArchiveFile=app.jsa -cp app.jar Main

# AOT 编译 (JDK 26+)
java -XX:AOTMode=create -jar app.jar
java -XX:AOTMode=use -jar app.jar
```

### 吞吐量优化

```bash
# 堆大小
-Xms4g -Xmx4g              # 避免动态调整

# GC
-XX:+UseParallelGC         # 吞吐优先
-XX:GCTimeRatio=99         # GC 时间 <1%

# JIT
-XX:CompileThreshold=8000  # 提前编译
```

### 延迟优化

```bash
# GC
-XX:+UseZGC                # 低延迟 GC
-XX:MaxGCPauseMillis=50    # 目标暂停

# JIT
-XX:CompileThreshold=10000 # 延迟编译
```

### 内存占用优化

```bash
# 压缩对象头 (JDK 24+ 实验性, JDK 26 默认)
-XX:+UseCompactObjectHeaders   # ~10% 堆节省

# 字符串去重
-XX:+UseStringDeduplication    # 适合大量重复字符串

# 压缩指针
-XX:+UseCompressedOops         # 堆 <32GB 自动启用

# 小堆优化
-XX:+UseSerialGC               # 最小 GC 开销 (单线程场景)
```

---

## 17. hsdb (HotSpot Debugger)

```bash
# JDK 9+ 命令行模式
jhsdb clhsdb --pid <pid>

# GUI 模式
jhsdb hsdb --pid <pid>

# 使用 core 文件
jhsdb clhsdb --exe <java> --core <core>
```

常用命令: `threads` (线程栈), `printcodecache` (代码缓存), `inspect <addr>` (查看对象), `heapdump <file>` (堆转储), `class <name>` (类信息)。

---

## 18. 相关链接

### 本地文档

- [GC 演进](../gc/) - GC 调优
- [内存管理](../memory/) - 堆、Metaspace
- [性能优化](../performance/) - 性能分析

### 外部参考

**工具文档:**
- [JFR Documentation](https://docs.oracle.com/javacomponents/jmc-5-4/jfr-runtime-guide/about.htm)
- [Mission Control](https://docs.oracle.com/javacomponents/jmc-5-4/jmc-user-guide/about.htm)

**调优指南:**
- [Java Tuning Guide](https://docs.oracle.com/en/java/javase/21/gctuning/)
- [Tool Documentation](https://docs.oracle.com/en/java/javase/21/docs/specs/man/tools.html)

**HotSpot 内部:**
- [HotSpot Wiki](https://wiki.openjdk.org/display/HotSpot)
- [Lilliput Project (Compact Object Headers)](https://wiki.openjdk.org/display/lilliput)
- [Loom Project (Virtual Threads)](https://wiki.openjdk.org/display/loom)

---

## 推荐阅读

- [JIT 编译器主题](../jit/) — C1/C2/Graal 编译器与运行时优化
- [GC 演进主题](../gc/) — 垃圾收集器实现与调优
- [内存管理主题](../memory/) — 堆、Metaspace、NMT 内存追踪
- [类加载机制](../classloading/) — ClassLoader 层次结构与模块化加载
