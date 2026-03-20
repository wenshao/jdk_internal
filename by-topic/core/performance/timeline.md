# 性能优化演进时间线

Java 性能优化从 JDK 1.0 到 JDK 26 的完整演进历程。

---

## 时间线概览

```
JDK 1.0 ──── JDK 5 ──── JDK 6 ──── JDK 7 ──── JDK 8 ──── JDK 17 ──── JDK 21 ──── JDK 25 ──── JDK 26
 │             │           │           │           │           │           │           │           │
解释器        JIT编译器    性能统计    Compressed- String      Escape    虚拟      AOT缓存     紧凑
执行         (HotSpot)    工具        Oops       Dedup      Analysis   线程      (JEP483)   对象头
```

---

## 目录

- [JVM 执行引擎](#jvm-执行引擎)
- [JIT 编译优化](#jit-编译优化)
- [版本演进](#版本演进)
  - [JDK 1.0-1.2](#jdk-10-12-解释器时代)
  - [JDK 5-6](#jdk-5-6-jit-成熟)
  - [JDK 7](#jdk-7-g1-gc-与分层编译)
  - [JDK 8](#jdk-8-lambda-与-string-dedup)
  - [JDK 11](#jdk-11-性能改进)
  - [JDK 17](#jdk-17-records-与模式匹配)
  - [JDK 21](#jdk-21-虚拟线程正式版)
  - [JDK 22-24](#jdk-22-24-持续优化)
  - [JDK 25](#jdk-25-aot-缓存与-jfr-增强)
  - [JDK 26](#jdk-26-性能持续改进)
- [性能工具演进](#性能工具演进)
- [Git 提交历史](#git-提交历史)
- [相关链接](#相关链接)

---

## JVM 执行引擎

### 解释器 vs JIT 编译器

```
┌─────────────────────────────────────────────────────────┐
│                HotSpot 执行引擎                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Java 字节码 (.class 文件)                              │
│       │                                                 │
│       ▼                                                 │
│  ┌─────────────────────────────────────────────┐        │
│  │         类加载器 (ClassLoader)              │        │
│  │   ├── 加载                                   │        │
│  │   ├── 验证                                   │        │
│  │   ├── 准备                                   │        │
│  │   └── 解析                                   │        │
│  └─────────────────┬───────────────────────────┘        │
│                    │                                    │
│                    ▼                                    │
│  ┌─────────────────────────────────────────────┐        │
│  │            解释器 (Interpreter)            │        │
│  │  ├── Template Interpreter (平台特定)       │        │
│  │  ├── x86_64: asm interpreter               │        │
│  │  ├── ARM: aarch64 interpreter              │        │
│  │  ├── RISC-V: riscv interpreter             │        │
│  │  ├── 快速启动                               │        │
│  │  ├── 即时执行                               │        │
│  │  └── 收集热点信息 (方法调用计数)            │        │
│  └─────────────────┬───────────────────────────┘        │
│                    │ (热点检测)                        │
│                    ▼                                   │
│  ┌─────────────────────────────────────────────┐        │
│  │            C1 编译器 (Client)               │        │
│  │  ├── 简单优化                               │        │
│  │  │   ├── 常量折叠                           │        │
│  │  │   ├── 死代码消除                         │        │
│  │  │   └── 内联小方法                         │        │
│  │  ├── 快速编译                               │        │
│  │  └── 启动性能                               │        │
│  └─────────────────┬───────────────────────────┘        │
│                    │ (更多调用)                       │
│                    ▼                                   │
│  ┌─────────────────────────────────────────────┐        │
│  │            C2 编译器 (Server)               │        │
│  │  ├── 深度优化                               │        │
│  │  │   ├── 激进内联                           │        │
│  │  │   ├── 循环优化                           │        │
│  │  │   │   ├── 循环展开                       │        │
│  │  │   │   ├── 循环向量化 (SIMD)              │        │
│  │  │   │   └── 循环不变量外提                 │        │
│  │  │   ├── 逃逸分析                           │        │
│  │  │   ├── 全局值编号                         │        │
│  │  │   └── 向量化                             │        │
│  │  └── 峰值性能                               │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 分层编译 (Tiered Compilation)

JDK 7+ 引入分层编译，结合 C1 和 C2 的优势：

```java
// JDK 7+ 分层编译
// Level 0: 解释执行
// Level 1: C1 编译 (带 profiling)
// Level 2: C1 编译 (有限 profiling)
// Level 3: C1 编译 (无 profiling)
// Level 4: C2 编译 (完全优化)

// 查看编译级别
-XX:+PrintCompilation -XX:+UnlockDiagnosticVMOptions -XX:+LogCompilation

// 禁用分层编译
-XX:-TieredCompilation

// 设置分层编译阈值
-XX:Tier3CompileLevel=1000     // C1 → C2 阈值 (调用次数)
-XX:Tier4CompileLevel=1500     // C2 编译阈值
-XX:CompileThreshold=10000     // 默认编译阈值
```

**分层编译优势**:
- 启动时使用 C1 快速编译
- 热点代码使用 C2 深度优化
- 平衡启动时间和峰值性能

---

## JIT 编译优化

### 方法内联

```java
// 内联优化示例
public class InlineExample {
    // 小方法会被内联 (默认 < 35 字节)
    private int add(int a, int b) {
        return a + b;
    }

    public int compute(int x, int y) {
        // 编译后可能变成: return x + y + 10;
        return add(x, y) + 10;
    }

    // 大方法不会被内联 (默认 > 325 字节)
    private int bigMethod(int a, int b) {
        // ... 大量代码
        return result;
    }
}

// 热点大小限制
-XX:FreqInlineSize=325          // 热点方法内联大小限制
-XX:MaxInlineSize=35            // 最大内联大小
-XX:MaxTrivialSize=6            // 简单方法最大内联大小
-XX:InlineSmallCode=1000        // 小代码方法内联阈值

// 查看内联信息
-XX:+PrintInlining
-XX:+PrintCompilation
```

### 循环优化

```java
// 循环展开 (Loop Unrolling)
for (int i = 0; i < 4; i++) {
    sum += array[i];
}
// 可能被优化为:
// sum += array[0];
// sum += array[1];
// sum += array[2];
// sum += array[3];

// 循环向量化 (SIMD)
for (int i = 0; i < array.length; i++) {
    array[i] *= 2;
}
// 使用 SIMD 指令并行处理 (AVX2/AVX-512)

// 控制循环优化
-XX:LoopUnrollLimit=60          // 循环展开限制
-XX:LoopMaxUnroll=16            // 最大展开次数
```

### 逃逸分析

```java
// 逃逸分析 - 标量替换
public class EscapeAnalysis {
    // 对象未逃逸，可以栈上分配或完全消除
    public int sum(int x, int y) {
        Point p = new Point(x, y);
        // JIT 可能优化为: return x + y;
        return p.x + p.y;
    }

    // 对象未逃逸，可以栈上分配
    public void method() {
        Point p = new Point(1, 2);
        int x = p.x;
        int y = p.y;
        // p 不再使用，可以完全消除
    }

    // 对象逃逸，必须在堆上分配
    public Point createPoint() {
        return new Point(1, 2);
    }
}

// 启用逃逸分析 (默认启用)
-XX:+DoEscapeAnalysis
-XX:+EliminateAllocations      // 标量替换
-XX:+EliminateLocks             // 锁消除
-XX:+PrintEliminateAllocations  // 查看消除详情
-XX:EscapeAnalysisTimeout=20    // 逃逸分析超时 (秒)
```

### 锁消除

```java
// 锁消除示例
public class LockElimination {
    private final Object lock = new Object();

    public void method() {
        // StringBuffer 的同步锁可以被消除
        StringBuffer sb = new StringBuffer();
        sb.append("Hello");
        sb.append(" World");
    }

    // JIT 优化后:
    public void method_optimized() {
        StringBuilder sb = new StringBuilder();  // 无锁版本
        sb.append("Hello");
        sb.append(" World");
    }
}

// 启用锁消除 (默认启用)
-XX:+EliminateLocks
```

---

## 版本演进

### JDK 1.0-1.2: 解释器时代

**JDK 1.0 (1996)**:
- 纯解释执行
- 启动快，执行慢
- 无 JIT 编译

**JDK 1.2 (1998)**:
- 引入 HotSpot VM
- 添加 JIT 编译器
- 自适应优化

### JDK 5-6: JIT 成熟

**JDK 5 (2004)**:
- **StringBuilder** 替代 StringBuffer (非同步版本)
- 类型配置文件 (types.config)
- 类数据共享 (CDS) 引入

```java
// JDK 5: StringBuilder 性能改进
String s = a + b + c;
// 编译为:
// new StringBuilder().append(a).append(b).append(c).toString();
```

**JDK 6 (2006)**:
- 分层编译引入
- 性能监控工具 (jstat, jmap)
- 逃逸分析引入

```bash
# JDK 6 新增工具
jstat -gcutil <pid> 1000 10      # GC 统计
jmap -histo:live <pid>            # 类直方图
jmap -dump:live,format=b,file=heap.hprof <pid>  # 堆转储
```

### JDK 7: G1 GC 与分层编译

**主要特性**:
- **G1 GC** 引入 (替代 CMS)
- **Compressed Oops** - 压缩普通对象指针
- **分层编译** 成为默认
- **InvokeDynamic** 指令 (为动态语言支持)

```java
// Compressed Oops - 压缩指针
// < 32GB: 使用 32 位指针
// >= 32GB: 使用 64 位指针

-XX:+UseCompressedOops           // 启用压缩指针
-XX:CompressedClassSpaceSize=1g   // 压缩类空间大小
```

### JDK 8: Lambda 与 String Dedup

**主要特性**:
- **Lambda 表达式** - invokedynamic 动态调用
- **String Deduplication** - G1 字符串去重
- **PermGen 移除** - 替换为 Metaspace

```java
// Lambda 性能特性
// 1. invokedynamic 动态调用
// 2. LambdaMetafactory 缓存
// 3. 方法句柄绑定

// Lambda vs 匿名类性能
// 首次调用: Lambda 较慢 (需要生成类)
// 后续调用: Lambda 更快 (直接方法句柄)

// String Dedup
-XX:+UseStringDeduplication       // 启用字符串去重
-XX:StringDeduplicationAgeThreshold=3  // 去重阈值
```

### JDK 11: 性能改进

**主要特性**:
- **HTTP Client** - 替代 HttpURLConnection
- **动态 CDS 归档** - 运行时创建归档
- **Epsilon GC** - 低开销 GC (实验性)

```bash
# 动态 CDS 归档
java -XX:ArchiveClassesAtExit=app.jsa \
     -Xshare:auto \
     MyApp

# Epsilon GC (无操作 GC)
-XX:+UnlockExperimentalVMOptions -XX:+UseEpsilonGC
```

### JDK 17: Records 与模式匹配

**主要特性**:
- **Records** - 比 POJO 性能更好
- **Pattern Matching** - instanceof 模式匹配
- **Sealed Classes** - 密封类
- **强封装** - JDK 内部 API 默认不可访问

```java
// Record 性能优势
record Point(int x, int y) { }

// vs 传统 POJO
class Point {
    private final int x;
    private final int y;
    // getter, setter, equals, hashCode, toString
}

// Record 优势:
// - 自动生成优化的字节码
// - 无 getter/setter 调用开销
// - 更好的内联
// - 更少的内存占用

// Pattern Matching 性能
if (obj instanceof String s) {
    // 无需强制转换
    System.out.println(s.length());
}
```

### JDK 21: 虚拟线程正式版

**主要特性**:
- **Virtual Threads** - 正式版 (JEP 444)
- **Scoped Values** - 预览版 (JEP 446)
- **Structured Concurrency** - 预览版 (JEP 453)
- **分代 ZGC** - 正式版 (JEP 439)

```java
// 虚拟线程性能
// I/O 密集型: 10-100x 性能提升
// CPU 密集型: 无提升

// 示例
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000_000; i++) {
        executor.submit(() -> {
            // I/O 操作
        });
    }
}

// 适用场景:
// ✅ I/O 密集型 (HTTP 请求, 数据库查询)
// ✅ 高并发服务器
// ❌ CPU 密集型 (计算密集任务)
```

### JDK 22-24: 持续优化

**JDK 22 (2024-03)**:
- **String Templates** - 预览版 (JEP 459)
- **Implicit Classes** - 预览版 (JEP 463)
- **Stream Gatherers** - 预览版 (JEP 461)

**JDK 23 (2024-09)**:
- **Markdown 文档注释** (JEP 467)
- **Flexible Constructors** (JEP 448)
- **Module Import Declarations** - 预览版 (JEP 476)

**JDK 24 (2025-03)**:
- **String Templates** - 第3次预览
- **Implicit Classes** - 第4次预览
- **Structured Concurrency** - 第4次预览

**性能改进** (JDK 22-24):
- C2 编译器优化 (内联改进)
- G1 GC 吞吐量提升
- ZGC 性能改进
- 启动时间优化

### JDK 25: AOT 缓存与 JFR 增强

**JEP 483: Ahead-of-Time Class Loading & Linking**

```bash
# 创建 AOT 缓存
# 步骤 1: 训练运行
java -XX:AOTCacheConfiguration=aot_config.txt \
     -XX:StoreAOTCacheConfiguration \
     MyApp

# 步骤 2: 生成缓存
java -XX:AOTCacheConfiguration=aot_config.txt \
     -XX:PrintAOTSharedArchive \
     MyApp

# 步骤 3: 使用缓存
java -XX:AOTCacheConfiguration=aot_config.txt \
     MyApp
```

**性能提升**:
- 启动时间减少 **42%** (0.018秒 vs 基线)
- 某些场景高达 **59%** 启动时间减少
- 消除类加载和链接延迟

**JEP 509: JFR CPU-Time Profiling (Experimental)**

```bash
# 启用 CPU 时间采样
java -XX:StartFlightRecording=jdk.CPUTimeSample#enabled=true ...
```

**新增事件**:
- `jdk.CPUTimeSample` - 记录 Java 和本地代码的 CPU 时间

**JEP 518: JFR Cooperative Sampling**

改进线程栈采样机制:
- 更安全的异步采样
- 减少采样开销
- 更准确的栈追踪

**JEP 520: JFR Method Timing & Tracing**

```bash
# 启用方法计时
java -XX:StartFlightRecording=jdk.MethodTiming#enabled=true ...
```

**新增事件**:
- `jdk.MethodTiming` - 方法执行时间测量
- `jdk.MethodTrace` - 方法调用追踪

**其他性能改进**:
- C2 编译器内联改进
- G1 GC 优化
- 启动时间优化
- String 优化

### JDK 26: 性能持续改进

**主要特性**:
- **HTTP/3** - 正式版 (JEP 517)
- **G1 GC 吞吐量提升** (JEP 522)
- **紧凑对象头** (JEP 519)

**JEP 514: AOT Command Line Ergonomics**

改进 AOT 缓存的命令行参数处理:
- 优化启动性能
- 更好的参数验证

**JEP 515: AOT Method Profiling**

支持在 AOT 阶段收集方法分析数据:
- 优化 JIT 编译决策
- 提前准备热点方法

**JEP 519: Compact Object Headers**

```bash
# 启用紧凑对象头 (默认)
-XX:+UseCompactObjectHeaders
```

**内存节省**: 每个对象节省 8-16 字节

**JEP 522: G1 GC Throughput Improvement**

优化 G1 GC 的同步机制:
- 提升吞吐量 10-15%
- 减少停顿时间

---

## 性能工具演进

### JFR (Java Flight Recorder)

**JDK 7**: 首次引入
- 低开销的性能分析
- 事件驱动的数据收集

**JDK 11**: 开源
- 从商业版变为开源
- 默认启用

**JDK 17**: 增强
- 更多事件类型
- 更好的 API

**JDK 25**: 重大增强 (JEP 509, 518, 520)
- CPU-Time Profiling
- Cooperative Sampling
- Method Timing & Tracing

```bash
# JFR 基本用法
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr \
     -XX:FlightRecorderOptions=samplethreads=true \
     MyApp

# 分析 JFR 文件
jfr --summary recording.jfr
jfr --print recording.jfr
```

### JMC (Java Mission Control)

**功能**:
- 可视化监控
- JFR 文件分析
- JVM 参数调优

```bash
# 启动 JMC
jmc
```

### async-profiler

**功能**:
- 采样分析
- CPU 采样
- 内存分配采样
- 火焰图生成

```bash
# CPU 采样
profiler.sh -d 30 -f profile.html <pid>

# 内存分配采样
profiler.sh -d 30 -e alloc <pid>
```

---

## Git 提交历史

> 基于 OpenJDK master 分支分析

### JIT 编译器改进 (2024-2026)

```bash
# C2 编译器优化
347aae64 8380011: Path-to-gcroots search should not trigger stack overflows
c6eda30 8345485: C2 MergeLoads: Fix diagnostic tag validation and clone
0681de6 8345485: C2 MergeLoads: Fix bugs and enable full Add operator merge
8e6ce20 8345485: C2 MergeLoads: merge adjacent array/native memory loads
45fc141 8379230: JFR: Do not store leak profiler context edge idx in markWord
f96974d 8373898: RepeatCompilation does not repeat compilation after bailout
e88bf99 8374307: Fix deoptimization storm caused by Action_none
d0e62e1 8351847: C2: Add "TraceSplitIf" flag for Split-If optimization
766959f 8371685: C2: Add flag to disable Loop Peeling
e99ed13 8379671: C2: Fix usage of PhaseGVN::transform in some intrinsics
```

### JFR 改进 (2024-2026)

```bash
# JFR 增强
f95e813 8379412: JfrJavaSupport::new_string should return early if pending exception
c3a698f 8377665: JFR: Symbol table not setup for early class unloading
7ec561f 8378178: Change Thread::_allocated_bytes from jlong to uint64_t
6627698 don't increment _num_objects_processed for follow-up chunks
af5c555 Update dfsClosure.cpp for leak profiler
e820ad5 small stack test
c85b20f fix windows build warning
```

### AOT/CDS 改进 (2024-2026)

```bash
# AOT 缓存和 CDS 归档
00c1f4b 8377512: AOT cache creation fails with invalid native pointer
ee90f00 8376822: UseCompactObjectHeaders: fill Klass gaps in AOT cache
a1e4621 8378152: Upstream AOT heap object improvements from Leyden repo
783a712 8378749: Early GC crash with unresolved AOT FMG subgraph classes
1ae2fee 8376125: Out of memory in CDS archive error with lot of classes
b41ba3a 8377932: AOT cache is not rejected when JAR file has changed
175bbb1 8375569: Store Java mirrors in AOT configuration file
a54ff1f 8376523: Move interned strings into AOT heap roots array
9fd86e3 8374639: Static archive with AOTClassLinking breaks dynamic archive
d9bc822 8369736: Add management interface for AOT cache creation
```

### 查看完整历史

```bash
# JIT 编译器
git log --oneline -- src/hotspot/share/compiler/

# JFR
git log --oneline -- src/hotspot/share/jfr/

# CDS/AOT
git log --oneline -- src/hotspot/share/cds/

# C2 编译器
git log --oneline -- src/hotspot/share/opto/
```

---

## 性能最佳实践

### 对象创建

```java
// ✅ 推荐: 重用对象
private static final DateFormat DATE_FORMAT =
    new SimpleDateFormat("yyyy-MM-dd");

// ❌ 避免: 重复创建
for (int i = 0; i < 1000; i++) {
    DateFormat df = new SimpleDateFormat("yyyy-MM-dd");
    df.format(date);
}
```

### 集合初始化

```java
// ✅ 推荐: 指定初始容量
List<String> list = new ArrayList<>(1000);
Map<String, Integer> map = new HashMap<>(1000);

// ❌ 避免: 默认容量导致扩容
List<String> list = new ArrayList<>();
for (int i = 0; i < 1000; i++) {
    list.add("item");  // 多次扩容
}
```

### 字符串拼接

```java
// ✅ 推荐: 使用 +
String result = "Hello " + name;  // 编译器优化

// ✅ 推荐: 循环中使用 StringBuilder
StringBuilder sb = new StringBuilder();
for (String s : list) {
    sb.append(s);
}

// ❌ 避免: 循环中使用 +
String result = "";
for (String s : list) {
    result += s;  // 每次创建新 String
}
```

### 并发处理

```java
// ✅ 推荐: 虚拟线程 (JDK 21+)
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 10_000; i++) {
        executor.submit(() -> {
            // I/O 操作
        });
    }
}

// ❌ 避免: CPU 密集型任务使用虚拟线程
// 虚拟线程对 CPU 密集型任务无性能提升
```

---

## 性能对比

### JDK 版本性能

| 版本 | 启动时间 | 吞吐量 | 内存 | 主要改进 |
|------|----------|--------|------|----------|
| JDK 8 | 基准 | 基准 | 基准 | Lambda, Stream |
| JDK 11 | +10% | +5% | -10% | HTTP Client, var |
| JDK 17 | +15% | +10% | -15% | Records, 密封类 |
| JDK 21 | +20% | +8% | -20% | 虚拟线程, 分代 ZGC |
| JDK 25 | +35% | +12% | -22% | AOT 缓存, JFR 增强 |
| JDK 26 | +40% | +15% | -25% | 紧凑对象头, HTTP/3 |

### 不同场景的性能选择

| 场景 | 推荐版本 | 理由 |
|------|----------|------|
| 微服务 | JDK 21+ | 虚拟线程, 快速启动 |
| 大数据处理 | JDK 17+ | Record, Pattern Matching |
| 云原生 | JDK 25+ | AOT 缓存, Project Leyden |
| 长运行服务 | JDK 17 LTS | 稳定性和性能平衡 |
| Serverless | JDK 25+ | AOT 缓存, 快速启动 |

---

## 时间线总结

| 版本 | 特性 | 说明 |
|------|------|------|
| JDK 1.0 | 解释器 | 纯解释执行 |
| JDK 1.2 | JIT 编译器 | HotSpot 引入 |
| JDK 5 | C1/C2 分层编译 | 性能大幅提升 |
| JDK 6 | 动态编译优化 | jstat/jmap |
| JDK 7 | G1 GC | Compressed Oops |
| JDK 8 | Lambda/String Dedup | invokedynamic |
| JDK 11 | 动态 CDS 归档 | HTTP Client |
| JDK 17 | Record/Pattern Matching | 编译器优化 |
| JDK 21 | 虚拟线程 | I/O 性能提升 |
| JDK 25 | AOT 缓存, JFR 增强 | 启动性能大幅提升 |
| JDK 26 | 紧凑对象头, HTTP/3 | 持续优化 |

---

## 相关链接

### 官方文档

- [Tuning Garbage Collectors](https://docs.oracle.com/en/java/javase/21/gctuning/)
- [Java Flight Recorder](https://docs.oracle.com/en/java/javase/21/docs/specs/man/jfr.html)
- [HotSpot VM Internals](https://openjdk.org/groups/hotspot/docs/)

### JEP 文档

- [JEP 483: AOT Class Loading](https://openjdk.org/jeps/483)
- [JEP 509: JFR CPU-Time Profiling](https://openjdk.org/jeps/509)
- [JEP 518: JFR Cooperative Sampling](https://openjdk.org/jeps/518)
- [JEP 520: JFR Method Timing & Tracing](https://openjdk.org/jeps/520)
- [JEP 519: Compact Object Headers](https://openjdk.org/jeps/519)
- [JEP 522: G1 GC Throughput Improvement](https://openjdk.org/jeps/522)

### 外部资源

- [Inside Java: Performance Updates](https://inside.java/)
- [Project Leyden](https://openjdk.org/projects/leyden/)
- [Performance Improvements in JDK 24](https://inside.java/2025/03/19/performance-improvements-in-jdk24/)
- [What's new for JFR in JDK 25](https://egahlin.github.io/2025/05/31/whats-new-in-jdk-25.html)

### Git 仓库

- [OpenJDK JDK Repository](https://github.com/openjdk/jdk)
- [OpenJDK Leyden Repository](https://github.com/openjdk/leyden)

---

**最后更新**: 2026-03-20

**Sources**:
- [Inside Java: Performance Improvements in JDK 24](https://inside.java/2025/03/19/performance-improvements-in-jdk24/)
- [JEP 483: AOT Class Loading](https://openjdk.org/jeps/483)
- [JEP 509: JFR CPU-Time Profiling](https://openjdk.org/jeps/509)
- [JEP 518: JFR Cooperative Sampling](https://openjdk.org/jeps/518)
- [JEP 520: JFR Method Timing & Tracing](https://openjdk.org/jeps/520)
- [Inside Java: Java Performance Update](https://inside.java/2025/01/26/devoxxbelgium-java-perfromance-update/)
- [Understanding and Finding JIT Compiler Performance Bugs](https://arxiv.org/html/2603.06551v1)
- [Project Leyden: Java Cloud-Native Optimization](https://blog.csdn.net/D1237890/article/details/155417254)
- [Let's Take a Look at JEP 483](https://www.reddit.com/r/java/comments/1jlv33y/lets_take_a_look_at_jep_483_aheadoftime_class/)
- [Hitchhiker's Guide to Java Performance](https://javapro.io/2025/04/07/hitchhikers-guide-to-java-performance/)
