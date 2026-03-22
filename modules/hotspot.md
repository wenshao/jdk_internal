# hotspot 模块分析

> HotSpot VM — OpenJDK 默认 Java 虚拟机实现 (Java Virtual Machine implementation)

---

## 1. 模块概述

HotSpot 是 OpenJDK 的默认 JVM 实现，名称来源于其"热点检测 (hot spot detection)"技术——通过运行时 profiling 找出频繁执行的代码路径并进行即时编译 (JIT compilation) 优化。

源码总量: 约 **1585 个 .cpp 文件** + **2234 个 .hpp 文件**，合计约 **3819 个源文件** (不含平台特定代码)。

### 架构总览

```
┌─────────────────────────────────────────────────────────┐
│                    Java 应用 (Application)               │
│  (字节码 bytecode)                                       │
├─────────────────────────────────────────────────────────┤
│                 类加载子系统 (Class Loading)              │
│  Bootstrap / Platform / Application ClassLoader          │
├─────────────────────────────────────────────────────────┤
│                   运行时数据区 (Runtime Data Areas)       │
│  堆 Heap / 元空间 Metaspace / PC / VM Stack / Native Stack│
├─────────────────────────────────────────────────────────┤
│                   执行引擎 (Execution Engine)             │
│  解释器 Interpreter → C1 编译器 → C2 编译器              │
│  (模板解释器)         (Client)      (Server/Opto)        │
├─────────────────────────────────────────────────────────┤
│                   本地接口 (Native Interface)             │
│  JNI / JVMTI / JVMCI                                    │
├─────────────────────────────────────────────────────────┤
│                   操作系统 (OS Abstraction)               │
│  linux / bsd / windows / aix / posix                     │
└─────────────────────────────────────────────────────────┘
```

---

## 2. 源码结构

### 2.1 顶层目录 (Top-level layout)

**路径**: `src/hotspot/`

```
hotspot/
├── share/          # 平台无关代码 (platform-independent)
├── cpu/            # CPU 架构相关 (CPU-specific)
│   ├── aarch64/    #   112 files
│   ├── arm/        #   94 files
│   ├── ppc/        #   105 files
│   ├── riscv/      #   107 files
│   ├── s390/       #   93 files
│   ├── x86/        #   137 files
│   └── zero/       #   76 files (零汇编解释器)
├── os/             # 操作系统适配 (OS-specific)
│   ├── aix/        #   21 files
│   ├── bsd/        #   17 files
│   ├── linux/      #   42 files
│   ├── posix/      #   26 files
│   └── windows/    #   47 files
└── os_cpu/         # OS + CPU 组合适配
```

### 2.2 share/ 子系统及文件数 (Subsystem file counts)

**路径**: `src/hotspot/share/`

以下为实际目录及其文件数量 (cpp + hpp):

| 目录 | 文件数 | 说明 |
|------|--------|------|
| `runtime/` | 207 | 运行时核心: 线程、同步、安全点 (safepoint)、栈 |
| `opto/` | 158 | C2 Server 编译器 (Ideal Graph IR) |
| `utilities/` | 139 | 工具类: 哈希表、位图、日志 |
| `oops/` | 125 | 对象模型 (Ordinary Object Pointers) |
| `cds/` | 95 | Class Data Sharing / AppCDS |
| `prims/` | 86 | JNI、JVMTI、Unsafe 等原语接口 |
| `classfile/` | 83 | 类文件解析、类加载器、系统字典 |
| `ci/` | 75 | 编译器接口 (Compiler Interface) |
| `memory/` | 50 | 内存管理: Metaspace、Arena |
| `code/` | 49 | CodeCache、nmethod、CodeBlob |
| `compiler/` | 46 | 编译调度: CompileBroker、CompileTask |
| `c1/` | 44 | C1 Client 编译器 |
| `nmt/` | 45 | Native Memory Tracking |
| `services/` | 39 | JMX、诊断命令 |
| `logging/` | 38 | 统一日志框架 (UL) |
| `interpreter/` | 36 | 模板解释器 (Template Interpreter) |
| `jvmci/` | 25 | JVM Compiler Interface (Graal 接入) |
| `adlc/` | 21 | Architecture Description Language Compiler |
| `gc/` | (子目录) | 垃圾回收器 — 见 hotspot-gc 模块 |
| `asm/` | 10 | 汇编器抽象层 |
| `jfr/` | 4 | JDK Flight Recorder 集成 |
| `libadt/` | 4 | 抽象数据类型 (VectorSet 等) |

---

## 3. VM 启动流程 (VM Startup)

### 3.1 入口链 (Entry chain)

Java 程序启动经过以下关键入口点:

```
java 命令 (launcher)
  → JLI_Launch()                     # src/java.base/share/native/libjli/java.c:226
    → JavaMain()                     # src/java.base/share/native/libjli/java.c:468
      → JNI_CreateJavaVM()           # JNI 标准入口
        → Threads::create_vm()       # src/hotspot/share/runtime/threads.cpp:450
```

### 3.2 Threads::create_vm() 初始化序列

`Threads::create_vm()` 是 HotSpot 的核心启动函数，按以下顺序初始化各子系统:

```cpp
// src/hotspot/share/runtime/threads.cpp:450
jint Threads::create_vm(JavaVMInitArgs* args, bool* canTryAgain) {
    VM_Version::early_initialize();    // 1. CPU 特性检测
    ThreadLocalStorage::init();        // 2. TLS 初始化
    os::init();                        // 3. 操作系统模块初始化
    Arguments::parse(args);            // 4. 解析 JVM 参数
    MemTracker::initialize();          // 5. NMT 初始化
    Arguments::apply_ergo();           // 6. 人体工程学 (ergonomics) 调整
    SafepointMechanism::initialize();  // 7. 安全点机制
    // ... GC 堆初始化、类加载、编译器初始化 ...
}
```

关键初始化步骤:
1. **VM_Version**: 检测 CPU 指令集 (SSE/AVX/NEON 等)
2. **os::init()**: 页大小、时钟、信号处理器
3. **Arguments::parse()**: 解析 `-Xmx`、`-XX:` 等参数
4. **Arguments::apply_ergo()**: 根据硬件自动调整参数 (堆大小、GC 选择等)
5. **Universe::initialize_heap()**: 创建 GC 堆
6. **SystemDictionary**: 加载核心类 (`java.lang.Object` 等)
7. **CompileBroker::compilation_init()**: 启动编译线程

---

## 4. 线程模型 (Thread Model)

### 4.1 线程类层次 (Thread hierarchy)

源码中的线程类继承关系 (来自 `share/runtime/` 和 `share/compiler/`):

```
Thread (share/runtime/thread.hpp)
├── NonJavaThread (share/runtime/nonJavaThread.hpp)
│   ├── NamedThread
│   │   ├── VMThread              (share/runtime/vmThread.hpp)
│   │   │   执行 VM Operations (GC、偏向锁撤销等)
│   │   ├── ConcurrentGCThread    (share/gc/shared/concurrentGCThread.hpp)
│   │   │   GC 并发标记/清理线程
│   │   └── G1ConcurrentMarkThread (share/gc/g1/g1ConcurrentMarkThread.hpp)
│   └── WatcherThread             (share/runtime/nonJavaThread.hpp)
│       周期性任务 (采样、超时检查)
├── JavaThread (share/runtime/javaThread.hpp)
│   ├── CompilerThread            (share/compiler/compilerThread.hpp)
│   │   C1/C2 编译线程
│   ├── ServiceThread             (share/runtime/serviceThread.hpp)
│   │   内部服务 (引用处理、JVMTI 事件)
│   ├── MonitorDeflationThread    (share/runtime/monitorDeflationThread.hpp)
│   │   监视器 deflation
│   └── NotificationThread        (share/runtime/notificationThread.hpp)
│       JMX 通知
```

### 4.2 关键线程类型说明

| 线程类型 | 源文件 | 职责 |
|----------|--------|------|
| **JavaThread** | `javaThread.hpp` | 执行 Java 代码的线程，每个对应一个 `java.lang.Thread` |
| **VMThread** | `vmThread.hpp` | 单例，执行需要安全点的 VM 操作 (如 Full GC) |
| **CompilerThread** | `compilerThread.hpp` | JIT 编译线程，继承 JavaThread (可执行 Java 代码) |
| **ConcurrentGCThread** | `concurrentGCThread.hpp` | GC 并发阶段工作线程 |
| **WatcherThread** | `nonJavaThread.hpp` | 周期性任务: 采样 profiling、编译超时检测 |
| **ServiceThread** | `serviceThread.hpp` | 处理 GC 通知、JVMTI post、低内存检测 |

### 4.3 JavaThread 关键字段

```cpp
// src/hotspot/share/runtime/javaThread.hpp:86
class JavaThread: public Thread {
 private:
  JavaFrameAnchor  _anchor;          // 最后一个 Java 帧锚点 (last Java frame anchor)
  ThreadFunction   _entry_point;     // 线程入口函数
  JavaThreadState  _thread_state;    // 线程状态 (thread state)
  SafepointMechanism::ThreadData _poll_data;  // 安全点轮询数据
  oop              _threadObj;       // 关联的 java.lang.Thread 对象
  oop              _vthread;         // 虚拟线程对象 (Virtual Thread)
  JavaFrameAnchor* _jfa_for_escape;  // Continuation escape 支持
  // ...
};
```

**JavaThreadState** 状态机:
```
_thread_new → _thread_in_vm → _thread_in_Java ⇄ _thread_in_native
                    ↑                                    │
                    └────────── _thread_blocked ──────────┘
```

---

## 5. 核心子系统

### 5.1 对象模型 (Object Model — oops/)

**源码**: `src/hotspot/share/oops/`，125 文件

```cpp
// src/hotspot/share/oops/oop.hpp:47
class oopDesc {
 private:
  volatile markWord _mark;       // Mark Word: 锁状态、GC 年龄、哈希
  union _metadata {
    Klass*      _klass;          // 类元数据指针 (class metadata pointer)
    narrowKlass _compressed_klass; // 压缩类指针 (compressed class pointer)
  } _metadata;
  // 实例数据紧随其后 (instance data follows)
};
```

**Klass 层次** (类的元数据表示):
```
Metadata
└── Klass
    ├── InstanceKlass          # 普通 Java 类
    │   ├── InstanceMirrorKlass  # java.lang.Class 本身
    │   ├── InstanceRefKlass     # Reference 子类
    │   └── InstanceClassLoaderKlass
    ├── ArrayKlass
    │   ├── TypeArrayKlass     # 基本类型数组 (int[], byte[] 等)
    │   └── ObjArrayKlass      # 对象数组 (Object[] 等)
    └── (其他内部 Klass)
```

### 5.2 类加载子系统 (Class Loading — classfile/)

**源码**: `src/hotspot/share/classfile/`，83 文件

关键源文件:
- `classFileParser.hpp` — 解析 .class 文件字节流
- `classLoader.hpp` — ClassLoader 实现
- `classLoaderData.hpp` — 每个 ClassLoader 的元数据
- `dictionary.hpp` — 已加载类的哈希表
- `systemDictionary.hpp` — 全局类字典 (核心查找入口)

类加载流程:
```
SystemDictionary::resolve_or_fail()
  → SystemDictionary::resolve_instance_class_or_null()
    → ClassLoader::load_class()
      → ClassFileParser::parse_stream()          # 解析字节流
        → ClassFileParser::parse_fields()         # 解析字段
        → ClassFileParser::parse_methods()        # 解析方法
        → ClassFileParser::parse_classfile_attributes()
      → SystemDictionary::define_instance_class() # 注册到字典
        → InstanceKlass::link_class_impl()        # 链接 (验证 + 准备)
```

### 5.3 执行引擎 (Execution Engine)

**分层编译 (Tiered Compilation)** — 5 个层级:

| Level | 描述 | 实现 |
|-------|------|------|
| 0 | 解释执行 (Interpreter) | `share/interpreter/` |
| 1 | C1 编译，无 profiling | `share/c1/` |
| 2 | C1 编译，有限 profiling | `share/c1/` |
| 3 | C1 编译，完整 profiling | `share/c1/` |
| 4 | C2 编译，完全优化 | `share/opto/` |

**模板解释器 (Template Interpreter)**:
- `share/interpreter/templateTable.cpp` — 每个字节码对应一段手写汇编模板
- `share/interpreter/templateInterpreter.cpp` — 解释器主循环
- 启动时生成到 CodeCache 中，而非逐条解释

**编译调度 (Compilation Scheduling)**:
```cpp
// src/hotspot/share/compiler/compileBroker.cpp
CompileBroker::compile_method()
  → CompileTask 入队 (enqueue compile task)
    → CompilerThread 从队列取出任务
      → C1Compiler::compile_method()   // Level 1-3
      → C2Compiler::compile_method()   // Level 4
        → Compile::Compile()           // 创建 Compile 上下文
          → Compile::Optimize()        // 优化阶段
          → Compile::Code_Gen()        // 代码生成阶段
```

### 5.4 运行时数据区 (Runtime Data Areas)

| 区域 | 实现类 | 源码位置 | 说明 |
|------|--------|----------|------|
| Java 堆 (Heap) | `CollectedHeap` 子类 | `gc/shared/collectedHeap.hpp` | 对象分配，GC 管理 |
| 元空间 (Metaspace) | `Metaspace` | `memory/metaspace.cpp` | 类元数据 (取代 PermGen) |
| 代码缓存 (CodeCache) | `CodeCache` | `code/codeCache.cpp` | JIT 编译后的机器码 |
| 线程栈 (Thread Stack) | `JavaThread::_stack` | `runtime/javaThread.hpp` | Java 帧 + Native 帧 |
| PC 寄存器 | 线程内部 | — | 当前字节码指令地址 |

### 5.5 安全点 (Safepoint)

**源码**: `src/hotspot/share/runtime/safepoint.cpp`

安全点是 VM 暂停所有 Java 线程的机制，用于 GC、去优化 (deoptimization)、线程 dump 等。

```
VMThread 发起 safepoint 请求
  → SafepointSynchronize::begin()
    → 设置 polling page 为不可读
    → 每个 JavaThread 在下一个安全点检查时触发 SIGSEGV
    → 所有线程到达安全点后，VMThread 执行 VM_Operation
  → SafepointSynchronize::end()
    → 恢复 polling page，唤醒所有线程
```

### 5.6 Continuation (虚拟线程支持)

**源码**: `src/hotspot/share/runtime/continuation.cpp`

```cpp
// Continuation 冻结/解冻 (freeze/thaw) — 虚拟线程的核心机制
Continuation::freeze()   // 将 Java 栈帧保存到堆上的 StackChunk
Continuation::thaw()     // 从堆上的 StackChunk 恢复栈帧到线程栈
```

---

## 6. 关键源文件索引

### 6.1 runtime/ 核心文件 (207 files)

| 文件 | 说明 |
|------|------|
| `threads.cpp` | VM 生命周期: `create_vm()`, `destroy_vm()` |
| `javaThread.cpp/hpp` | JavaThread 实现 |
| `vmThread.cpp/hpp` | VMThread 和 VM_Operation 执行 |
| `thread.cpp/hpp` | Thread 基类 |
| `safepoint.cpp` | 安全点同步 |
| `arguments.cpp` | JVM 参数解析 |
| `java.cpp` | `vm_exit()`, JVM 退出处理 |
| `continuation.cpp` | Continuation freeze/thaw |
| `deoptimization.cpp` | 去优化 (compiled → interpreted) |
| `synchronizer.cpp` | 对象监视器、锁膨胀 |
| `sharedRuntime.cpp` | 运行时桩 (runtime stubs) |

### 6.2 compiler/ 核心文件 (46 files)

| 文件 | 说明 |
|------|------|
| `compileBroker.cpp` | 编译任务调度、编译队列 |
| `compilerThread.hpp` | CompilerThread 定义 |
| `compilationPolicy.cpp` | 编译策略 (何时触发编译) |
| `compileTask.cpp` | 单个编译任务 |
| `abstractCompiler.hpp` | 编译器抽象接口 |

### 6.3 code/ 核心文件 (49 files)

| 文件 | 说明 |
|------|------|
| `codeCache.cpp` | 代码缓存管理 (分段: non-method / profiled / non-profiled) |
| `nmethod.cpp` | 编译后的 Java 方法 (native method) |
| `codeBlob.cpp` | CodeCache 中的代码块基类 |
| `compiledIC.cpp` | 编译后的内联缓存 (Inline Cache) |

---

## 7. JVM 选项参考

### 7.1 内存相关

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `-Xms` | 物理内存 1/64 | 初始堆大小 (initial heap size) |
| `-Xmx` | 物理内存 1/4 | 最大堆大小 (maximum heap size) |
| `-XX:MetaspaceSize` | 平台相关 | 元空间初始大小 |
| `-XX:MaxMetaspaceSize` | 无限制 | 元空间最大大小 |
| `-XX:ReservedCodeCacheSize` | 240MB | 代码缓存保留大小 |

### 7.2 GC 相关

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `-XX:+UseG1GC` | 默认开启 | 使用 G1 GC |
| `-XX:+UseZGC` | - | 使用 ZGC |
| `-XX:+UseShenandoahGC` | - | 使用 Shenandoah GC |
| `-XX:+UseParallelGC` | - | 使用 Parallel GC |
| `-XX:+UseSerialGC` | - | 使用 Serial GC |
| `-XX:MaxGCPauseMillis` | 200 | 最大 GC 暂停目标 (G1) |

### 7.3 编译相关

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `-XX:+TieredCompilation` | 默认开启 | 分层编译 |
| `-XX:TieredStopAtLevel` | 4 | 最高编译层级 |
| `-XX:CompileThreshold` | 10000 | 非分层模式编译阈值 |
| `-XX:ReservedCodeCacheSize` | 240MB | 代码缓存大小 |
| `-XX:+PrintCompilation` | - | 打印编译事件 |

### 7.4 诊断选项 (需 `-XX:+UnlockDiagnosticVMOptions`)

```bash
# 编译日志
java -XX:+UnlockDiagnosticVMOptions -XX:+LogCompilation -XX:LogFile=compilation.log

# 打印生成的汇编码 (需 hsdis 插件)
java -XX:+UnlockDiagnosticVMOptions -XX:+PrintAssembly

# GC 日志
java -Xlog:gc*:file=gc.log:time,uptime,level,tags

# 安全点统计
java -Xlog:safepoint*=debug
```

---

## 8. 性能调优指南

### 8.1 内存调优

```bash
# 推荐: Xms = Xmx 避免堆扩缩开销
java -Xms4g -Xmx4g -jar app.jar

# 元空间设置 (避免频繁 Full GC)
java -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m -jar app.jar
```

### 8.2 GC 调优

```bash
# G1 GC (通用推荐)
java -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -jar app.jar

# ZGC (超低延迟, 大堆)
java -XX:+UseZGC -XX:+ZGenerational -jar app.jar

# Shenandoah (低延迟)
java -XX:+UseShenandoahGC -XX:ShenandoahGCMode=generational -jar app.jar
```

### 8.3 JIT 调优

```bash
# 代码缓存 (防止 CodeCache 满导致去优化)
java -XX:ReservedCodeCacheSize=512m -jar app.jar

# 预热: 提前编译关键方法
java -XX:CompileCommand=compileonly,com.example.HotMethod::* -jar app.jar
```

---

## 9. 相关模块链接

- [HotSpot GC 组件分析](hotspot-gc.md) — 各 GC 实现详解
- [HotSpot C2 编译器分析](hotspot-c2.md) — C2 Server 编译器深入分析
- [源码浏览](https://github.com/openjdk/jdk/tree/master/src/hotspot)
