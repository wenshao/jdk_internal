# 核心平台

JVM、内存、性能、模块系统等底层技术。

[← 返回主题索引](../) | [深度分析](deep-dive.md)

---
## 目录

1. [演进概览](#1-演进概览)
2. [主题列表](#2-主题列表)
3. [OpenJDK 重大项目](#3-openjdk-重大项目)
4. [核心贡献者](#4-核心贡献者)
5. [内部开发者资源](#5-内部开发者资源)
6. [统计数据](#6-统计数据)
7. [学习路径](#7-学习路径)
8. [深度分析](#8-深度分析)

---


## 1. 演进概览

```
JDK 1.0 ─── JDK 5 ─── JDK 8 ─── JDK 11 ─── JDK 17 ─── JDK 21 ─── JDK 26
   │           │           │            │            │            │           │
 解释器      分层编译    元空间      ZGC         强封装      虚拟线程    分代 ZGC
 Serial GC   G1 GC      Lambda      JFR         内部API     Project Loom G1优化
```

### 版本里程碑

| 版本 | 主题 | 关键特性 |
|------|------|----------|
| **JDK 5** | 性能革命 | 分层编译、JMX、并发工具 |
| **JDK 8** | 内存模型 | 元空间、Lambda、Compressed Oops |
| **JDK 11 LTS** | 低延迟 | ZGC (实验)、JFR、HTTP Client |
| **JDK 17 LTS** | 强封装 | 遗留封装限制、JDK 内部 API 封装 |
| **JDK 21 LTS** | 高并发 | 虚拟线程、分代 ZGC |
| **JDK 26** | 性能优化 | G1 +10-20%、ZGC NUMA |

---

## 2. 主题列表

### [GC 演进](gc/)

垃圾收集器的发展历程，从 Serial 到分代 ZGC。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 8 | G1 成为主流，CMS 标记废弃 | - |
| JDK 11 | ZGC 引入 (实验性) | JEP 333 |
| JDK 15 | ZGC 生产可用 | JEP 377 |
| JDK 17 | 并发线程栈扫描 | JEP 379 |
| JDK 21 | **分代 ZGC** (JEP 439)、分代 Shenandoah (JEP 429) | JEP 439, JEP 429 |
| JDK 23 | ZGC 分代改进 | JEP 474 |
| JDK 26 | G1 吞吐量提升 (JEP 522)、ZGC NUMA | JEP 522 |

→ [GC 时间线](gc/timeline.md)

### [内存管理](memory/)

Java 内存管理从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 5 | WeakReference 等 | 引用类型 |
| JDK 6 | Compressed Oops | 压缩指针 |
| JDK 8 | 元空间、String Dedup | 永久代移除 |
| JDK 11 | ZGC | 低延迟 GC |
| JDK 15 | ZGC 生产可用 | 正式版 |
| JDK 21 | 分代 ZGC | 降低 GC 频率 |
| JDK 22 | Foreign Memory Access | 堆外内存 |

→ [内存管理时间线](memory/timeline.md)

### [性能优化](performance/)

Java 性能优化从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 1.0 | 解释器执行 | 纯解释 |
| JDK 5 | JIT 编译器 (HotSpot) | 分层编译 |
| JDK 6 | 性能统计工具 | jstat/jmap |
| JDK 7 | G1 GC、Compressed Oops | 内存优化 |
| JDK 8 | Lambda/String Dedup | 编译优化 |
| JDK 17 | Record/Pattern Matching | 编译器优化 |
| JDK 21 | 虚拟线程 | I/O 性能提升 |

→ [性能优化时间线](performance/timeline.md)

### [JIT 编译](jit/)

C1、C2、Graal JIT 编译器从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 1.0 | 解释器 | 纯解释执行 |
| JDK 1.3 | C2 (Server Compiler) | 高性能编译器 |
| JDK 1.4 | C1 (Client Compiler) | 快速启动编译器 |
| JDK 5 | C1/C2 分离 | -client/-server |
| JDK 6 | 分层编译 | C1 + C2 组合 |
| JDK 9 | Graal JIT | 实验性高性能 JIT |
| JDK 23 | Graal 优化 | 性能提升 |

→ [JIT 编译详情](jit/)

### [Vector API (SIMD)](vector-api/)

SIMD 向量化计算 API，从 JDK 16 开始孵化。

| 版本 | JEP | 状态 |
|------|-----|------|
| JDK 16 | JEP 338 | 🥚 First Incubator |
| JDK 17 | JEP 414 | 🥚 Second Incubator |
| JDK 18 | JEP 417 | 🥚 Third Incubator |
| JDK 19 | JEP 426 | 🥚 Fourth Incubator |
| JDK 20 | JEP 448 | 🥚 Fifth Incubator |
| JDK 21 | JEP 460 | 🥚 Sixth Incubator + Float16 |
| JDK 22-23 | - | 🥚 继续孵化 |
| JDK 24 | - | 🥚 继续孵化 |
| **JDK 26** | - | 🥚 **继续孵化** (GA 2026-03) |

**性能提升**: 2x-8x (取决于 CPU 向量宽度)

**为什么孵化这么慢？**
- 跨平台指令集差异 (x86 AVX vs ARM SVE vs RISC-V V)
- ARM SVE 可变向量长度的复杂性
- C2 编译器需要大量适配
- 与 Valhalla 的协同设计

→ [Vector API 详情](vector-api/) | [时间线](vector-api/timeline.md) | [使用指南](vector-api/usage.md) | [平台支持](vector-api/platform.md)

---

## 3. OpenJDK 重大项目

### [Project Amber](amber/)

Java 语言特性演进项目：更简洁、更安全、更易表达。

| 特性 | 版本 | JEP |
|------|------|-----|
| Local Variable Type Inference (var) | JDK 10 | JEP 286 |
| Switch Expressions | JDK 14 | JEP 361 |
| Text Blocks | JDK 15 | JEP 378 |
| Records | JDK 16 | JEP 395 |
| Pattern Matching for instanceof | JDK 16 | JEP 394 |
| Sealed Classes | JDK 17 | JEP 409 |
| Pattern Matching for switch | JDK 21 | JEP 441 |
| Record Patterns | JDK 21 | JEP 440 |
| Unnamed Patterns & Variables | JDK 21 | JEP 443 |
| Primitive Patterns | JDK 26 | JEP 455 |

→ [Amber 时间线](amber/timeline.md)

### [Project Loom](loom/)

虚拟线程和结构化并发：轻量级并发，百万级线程无压力。

| 特性 | 版本 | JEP |
|------|------|-----|
| 虚拟线程 | JDK 21 | JEP 444 |
| 结构化并发 (预览) | JDK 21+ | JEP 453 |

**核心优势**:
- 虚拟线程: ~几 KB 内存，vs 平台线程 ~1MB
- 阻塞无开销: 阻塞时不阻塞 Carrier Thread
- 同步式编程: 不再需要回调地狱

→ [Loom 时间线](loom/timeline.md)

### [Project Panama](panama/)

外部函数接口和外部内存器：与原生代码的无缝互操作。

| 特性 | 版本 | JEP |
|------|------|-----|
| Foreign Memory Access API | JDK 22 | JEP 454 |
| Foreign Function Interface | JDK 22 | JEP 454 |

**核心优势**:
- 替代 JNI: 无需生成胶水代码
- 类型安全: 编译时检查
- 零拷贝: 直接访问堆外内存
- 性能: 接近原生调用

→ [Panama 时间线](panama/timeline.md)

### [Project Valhalla](valhalla/)

值类型和泛型特化：让 Java 拥有像 C++ 一样高效的值类型。

| 特性 | 状态 | JEP |
|------|------|-----|
| Inline Classes / Primitive Classes | 开发中 | JEP 401 |
| 增强泛型 (List<int>) | 开发中 | JEP 402 |
| Primitive Patterns | JDK 26 | JEP 455 |

**核心优势**:
- 消除对象头: 节省 30-50% 内存
- 原始类型特化: `List<int>` 无装箱
- 缓存友好: 扁平化内存布局

→ [Valhalla 时间线](valhalla/timeline.md) | [进度追踪](valhalla/progress.md) | [架构分析](valhalla/architecture.md)

**为什么进度这么慢？**
- 需要修改 JVM 核心层 (Klass 系统、对象布局)
- 修改 2000+ 文件，涉及所有 GC
- 与现有生态兼容 (反射、序列化、JNI、JVMTI)
- 泛型特化需要语言层面重大变更
- 已开发 10+ 年，预计 JDK 27-28

---

### [GraalVM](graalvm/)

Oracle Labs 开发的高性能 JDK 发行版。

| 特性 | 说明 |
|------|------|
| **Graal JIT** | 用 Java 编写的高性能 JIT 编译器 |
| **Native Image** | AOT 编译，毫秒级启动 |
| **Truffle** | 多语言运行时框架 |
| **Polyglot** | JavaScript/Python/Ruby/R 等语言支持 |

| 版本 | JDK 基线 | 主要特性 |
|------|----------|----------|
| GraalVM 19 | JDK 11 | 首个社区版本 |
| GraalVM 22 | JDK 17 | Native Image 性能提升 |
| GraalVM 24 | JDK 21 | JDK 21 基线 |

→ [GraalVM 详情](graalvm/)

### [CPU 架构](arch/)

OpenJDK 支持的 CPU 架构演进。

| 架构 | 引入版本 | 状态 | 说明 |
|------|----------|------|------|
| **x86_64** | JDK 5 | ✅ 主流 | Intel/AMD 64位 |
| **x86_32** | JDK 1.0 | ⚠️ JDK 26 移除 | 32位 x86 |
| **AArch64** | JDK 9 | ✅ 主流 | ARM 64位, Apple Silicon |
| **RISC-V** | JDK 19 | ✅ 活跃 | 开源指令集 |
| **LoongArch** | JDK 21 | ✅ 活跃 | 龙芯架构 |
| **PPC64** | JDK 9 | ✅ 维护 | PowerPC |
| **s390x** | JDK 9 | ✅ 维护 | IBM 大型机 |

→ [CPU 架构详情](arch/)

### [类加载器](classloading/)

Java 类加载器从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 1.0 | Bootstrap/Extension/Application | 三层类加载 |
| JDK 1.2 | 自定义 ClassLoader | 用户类加载 |
| JDK 5 | ContextClassLoader | SPI 支持 |
| JDK 6 | Instrumentation | Java Agent |
| JDK 6 | ServiceLoader | SPI 标准化 |
| JDK 9 | Platform ClassLoader | 模块化 |
| JDK 17 | 强封装 | 内部 API 限制 |

→ [类加载器时间线](classloading/timeline.md)

### [模式匹配](patterns/)

类型模式、Record 模式、解构模式从 JDK 14 到 JDK 26 的演进。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 14 | instanceof 模式 (预览) | JEP 305 |
| JDK 15 | instanceof 模式 (二次预览) | JEP 375 |
| JDK 16 | instanceof 模式 (正式) | JEP 394 |
| JDK 17 | switch 模式 (预览) | JEP 406 |
| JDK 19 | Record 模式 (预览) | JEP 405 |
| JDK 21 | Record/switch 模式 (正式) | JEP 440, JEP 441 |
| JDK 23 | Switch Guards | JEP 456 |
| JDK 26 | 原始类型模式 | JEP 455 |

### [泛型系统](generics/)

类型参数、泛型方法、通配符从 JDK 5 到现在的演进。

| 版本 | 主要变化 | JSR |
|------|----------|-----|
| JDK 5 | 泛型引入 | JSR 14 |
| JDK 5 | 泛型方法、通配符 | - |
| JDK 7 | Diamond 操作符 | - |
| JDK 8 | 类型注解 | - |
| JDK 17 | var 增强 | - |

### [Record 类型](records/)

不可变数据载体从 JDK 14 到现在的演进。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 14 | Record (预览) | JEP 359 |
| JDK 15 | Record (二次预览) | JEP 384 |
| JDK 16 | Record (正式) | JEP 395 |
| JDK 21 | Record 模式 | JEP 440 |

### [模块系统](modules/)

Java 模块系统 (JPMS) 从 JDK 9 到现在的完整演进。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 9 | **JPMS** (JEP 261) | 模块化系统 |
| JDK 9 | jlink 定制运行时 | JEP 282 |
| JDK 16 | 强封装默认 | JEP 396 |
| JDK 17 | 完全强封装 | JEP 403 |
| JDK 23 | 模块导入声明 (预览) | JEP 476 |
| JDK 25 | 模块导入声明 (正式) | JEP 511 |

→ [模块系统详情](modules/)

### [JVM 调优与监控](jvm/)

JVM 参数、调优工具和监控技术从 JDK 1.0 到 JDK 26 的演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 1.0 | 基础参数 (-Xmx, -Xms) | 内存配置 |
| JDK 5 | JMX, jconsole | 监控工具 |
| JDK 6 | jstat, jmap, jstack | 诊断工具 |
| JDK 7 | G1 GC | 新 GC 算法 |
| JDK 8 | Metaspace | 永久代移除 |
| JDK 9 | G1 成为默认 | GC 默认值 |
| JDK 11 | ZGC, JFR | 低延迟 GC |
| JDK 21 | 分代 ZGC | 生产就绪 |

→ [JVM 调优时间线](jvm/timeline.md)

---

## 4. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### GC 团队 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Albert Mingkun Yang | 681 | Oracle | G1 GC, 内存管理 |
| 2 | [Thomas Schatzl](/by-contributor/profiles/thomas-schatzl.md) | 674 | Oracle | G1 GC 维护者 |
| 3 | [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | 324 | Amazon | 性能基准, 内存 |
| 4 | Zhengyu Gu | 252 | Oracle | JVM 运行时 |
| 5 | [Kim Barrett](/by-contributor/profiles/kim-barrett.md) | 235 | Oracle | C++ 现代化 |
| 6 | Stefan Karlsson | 229 | Oracle | 分代 ZGC (JEP 439) |
| 7 | Per Lidén | 198 | Oracle | ZGC 创始人 |
| 8 | Roman Kennke | 163 | Red Hat | Shenandoah GC |
| 9 | William Kemper | 112 | Amazon | 分代 Shenandoah (JEP 521) |

### JVM/性能团队 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | 333 | Oracle | 类加载, 运行时 |
| 2 | [David Holmes](/by-contributor/profiles/david-holmes.md) | 201 | Oracle | 并发, 线程 |
| 3 | [Ioi Lam](/by-contributor/profiles/ioi-lam.md) | 167 | Oracle | CDS, AOT |
| 4 | [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | 123 | Amazon | 性能基准 |
| 5 | Kim Barrett | 115 | Oracle | C++ 现代化 |
| 6 | [Thomas Stuefe](/by-contributor/profiles/thomas-stuefe.md) | 112 | IBM | 内存, 跨平台 |
| 7 | Serguei Spitsyn | 107 | Oracle | JVMTI, JFR |

### 模块系统

| 贡献者 | 公司 | 主要贡献 |
|--------|------|----------|
| **Mark Reinhold** | Oracle | JPMS (JEP 261) 首席架构师 |
| **Alex Buckley** | Oracle | JLS/JVMS 规范维护 |

---

## 5. 内部开发者资源

### HotSpot 源码结构

```
src/hotspot/share/
├── gc/                          # GC 实现
│   ├── g1/                      # G1 GC
│   ├── shenandoah/              # Shenandoah GC
│   ├── z/                       # ZGC
│   ├── parallel/                # Parallel GC
│   ├── serial/                  # Serial GC
│   └── shared/                  # GC 共享代码
├── interpreter/                 # 解释器
├── compiler/                    # JIT 编译器
│   ├── c1/                      # C1 (Client Compiler)
│   ├── c2/                      # C2 (Server Compiler)
│   └── graal/                   # Graal JIT (可选)
├── oops/                        # 对象模型
│   ├── instanceKlass.cpp        # 类元数据
│   ├── arrayKlass.cpp           # 数组类
│   └── symbol.cpp               # 符号表
├── memory/                      # 内存管理
│   ├── metaspace.cpp            # 元空间
│   ├── universe.cpp             # 堆初始化
│   └── virtualspace.cpp         # 虚拟内存
├── classfile/                   # 类文件处理
├── classloader/                 # 类加载器
├── prims/                       # JVM 内部原语
│   ├── jni.cpp                  # JNI 实现
│   ├── jvmti.cpp                # JVMTI 实现
│   └── jvm.cpp                  # JVM 接口
└── runtime/                     # 运行时
    ├── thread.cpp               # 线程实现
    ├── mutex.cpp                # 锁实现
    └── safepoint.cpp            # Safepoint
```

### 关键内部类

| 类 | 作用 | 访问级别 |
|---|------|----------|
| `jdk.internal.misc.Unsafe` | 直接内存访问 | `@Restricted` |
| `jdk.internal.vm.VectorSupport` | Vector API 支持 | 内部 |
| `jdk.internal.access.JavaLangAccess` | 内部访问 | `@Restricted` |
| `jdk.internal.misc.Signal` | Unix 信号 | 内部 |

### VM 参数速查

```bash
# GC 选择
-XX:+UseG1GC                    # G1 (默认 JDK 9+)
-XX:+UseZGC                     # ZGC
-XX:+UseShenandoahGC            # Shenandoah
-XX:+UseParallelGC              # Parallel
-XX:+UseSerialGC                # Serial

# 内存配置
-Xms4g                          # 初始堆
-Xmx8g                          # 最大堆
-XX:MetaspaceSize=256m          # 元空间初始大小
-XX:MaxMetaspaceSize=512m       # 元空间最大值
-XX:CompressedClassSpaceSize=1g # 压缩类空间

# GC 调优
-XX:MaxGCPauseMillis=200        # G1 目标暂停时间
-XX:G1HeapRegionSize=16m        # G1 Region 大小
-XX:ConcGCThreads=4             # 并发 GC 线程
-XX:ParallelGCThreads=8         # 并行 GC 线程

# 性能诊断
-XX:+PrintGCDetails             # GC 详细日志
-XX:+PrintGCTimeStamps          # GC 时间戳
-Xlog:gc*:file=gc.log           # JDK 9+ 统一日志
-XX:+UseStringDeduplication     # 字符串去重

# JIT 编译
-XX:TieredStopAtLevel=3         # 分层编译级别
-XX:CompileThreshold=10000      # C2 编译阈值
-XX:+PrintCompilation           # 打印编译信息
-XX:+UnlockDiagnosticVMOptions  # 解锁诊断选项
-XX:+LogCompilation             # 记录编译日志
```

### 诊断工具

```bash
# jstat - GC 统计
jstat -gcutil <pid> 1000 10

# jmap - 堆转储
jmap -dump:live,format=b,file=heap.hprof <pid>

# jstack - 线程转储
jstack -l <pid>

# jinfo - VM 参数
jinfo -flags <pid>

# jcmd - JVM 诊断
jcmd <pid> GC.heap_info
jcmd <pid> VM.flags
jcmd <pid> Thread.print

# JFR (JDK 11+)
jcmd <pid> JFR.start name=myrecording
jcmd <pid> JFR.dump name=myrecording filename=recording.jfr
```

---

## 6. 统计数据

| 指标 | 数值 |
|------|------|
| GC 算法 | 5 (Serial, Parallel, G1, ZGC, Shenandoah) |
| JIT 编译器 | 2 (C1, C2) + Graal |
| 类加载器层次 | 3 (Bootstrap, Platform, Application) |
| JFR 事件类型 | 200+ |

---

## 7. 学习路径

1. **入门**: [性能优化](performance/) → 了解 JVM 执行模型
2. **进阶**: [内存管理](memory/) → [GC 演进](gc/) → 理解内存和 GC
3. **深入**: [类加载器](classloading/) → [模块系统](modules/) → 理解类加载机制
4. **专家**: [JVM 调优](jvm/) → 掌握生产调优

---

## 8. 深度分析

→ [核心平台深度分析](deep-dive.md) - 技术挑战、设计权衡与项目依赖

**核心话题**:
- [为什么 Vector API 孵化这么慢？](deep-dive.md#为什么-vector-api-孵化这么慢)
- [为什么 Valhalla 进度缓慢？](deep-dive.md#为什么-valhalla-进度缓慢)
- [Float16 深度分析](deep-dive.md#float16-深度分析) - AI/ML 的 Java 就绪
- [项目依赖关系图](deep-dive.md#项目依赖关系图)
- [技术挑战与权衡](deep-dive.md#技术挑战与权衡)
