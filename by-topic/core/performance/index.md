# 性能优化

> JIT、分层编译、逃逸分析、JFR、AOT 缓存演进历程

[← 返回核心平台](../)

---

## 目录

1. [TL;DR 快速概览](#1-tldr-快速概览)
2. [快速概览](#2-快速概览)
3. [核心技术](#3-核心技术)
4. [性能工具](#4-性能工具)
5. [最新增强](#5-最新增强)
6. [核心贡献者](#6-核心贡献者)
7. [性能最佳实践](#7-性能最佳实践)
8. [性能对比](#8-性能对比)
9. [重要 PR 分析](#9-重要-pr-分析)
10. [性能优化最佳实践](#10-性能优化最佳实践)
11. [相关链接](#11-相关链接)

---

## 1. TL;DR 快速概览

> 💡 **1 分钟了解 Java 性能优化**

### 快速决策树

```
性能问题？
  │
  ├─ 启动慢 → 检查分层编译、类加载
  │
  ├─ 内存高 → 检查 GC、内存泄漏
  │
  ├─ CPU 高 → 检查算法、锁竞争
  │
  └─ 响应慢 → 检查 GC 停顿、I/O 阻塞
```

### 常用 VM 参数

```bash
# 堆内存设置
-Xms2g -Xmx2g

# GC 选择 (JDK 17+)
-XX:+UseZGC                    # 低延迟
-XX:+UseG1GC                   # 通用

# 性能调优
-XX:+UnlockDiagnosticVMOptions
-XX:+PrintGCDetails
-XX:+PrintCompilation
-XX:+PrintAssembly

# JFR 记录
-XX:StartFlightRecording=dump.jfr
```

### 性能工具

| 工具 | 用途 | 命令 |
|------|------|------|
| **JFR** | 生产监控 | `-XX:StartFlightRecording` |
| **JMC** | JVM 分析 | `jmc` |
| **JHSDB** | 热点调试 | `jhsdb` |
| **VisualVM** | 性能分析 | `visualvm` |

### 优化方向

| 问题 | 检查工具 | 解决方案 |
|------|----------|----------|
| GC 频繁 | JFR GC 日志 | 调整堆大小、切换 GC |
| CPU 高 | JFR CPU 采样 | 优化算法、使用并行流 |
| 内存泄漏 | JFR 内存 | Heap Dump 分析 |
| 锁竞争 | JFR 线程 | 优化锁粒度 |

---

## 2. 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 7 ── JDK 8 ── JDK 17 ── JDK 21 ── JDK 25 ── JDK 26
   │         │        │        │        │        │        │         │
解释器    分层   G1 GC  Lambda  Graal  虚拟线程  AOT缓存   HTTP/3
(纯解释)  编译   默认   Stream  (实验)  (正式)  (JEP483)  性能提升
```

### 核心技术演进

| 技术 | 首发版本 | 说明 | 状态 |
|------|----------|------|------|
| **解释器** | JDK 1.0 | 纯解释执行，快速启动 | 成熟 |
| **JIT 编译 (C1/C2)** | JDK 1.2 | HotSpot 编译器 | 成熟 |
| **分层编译** | JDK 7 | C1 + C2 组合 | 成熟 |
| **逃逸分析** | JDK 6 | 标量替换、栈上分配 | 成熟 |
| **Graal JIT** | JDK 9 | 实验性高性能 JIT | 实验中 |
| **JFR** | JDK 7 | Java Flight Recorder | 持续增强 |
| **AOT 缓存** | JDK 25 | JEP 483 预加载类链接 | 新增 |
| **Project Leyden** | JDK 26+ | 全面 AOT 编译 | 开发中 |

---

## 目录

- [核心技术](#核心技术)
  - [JIT 编译](#jit-编译)
  - [分层编译](#分层编译)
  - [逃逸分析](#逃逸分析)
- [性能工具](#性能工具)
  - [JFR](#jfr)
  - [JMC](#jmc)
- [最新增强](#最新增强)
  - [JDK 25 JFR 增强](#jdk-25-jfr-增强)
  - [JDK 25 AOT 缓存](#jdk-25-aot-缓存)
  - [JDK 26 性能改进](#jdk-26-性能改进)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 3. 核心技术

### JIT 编译

HotSpot VM 包含两个 JIT 编译器：

```
┌─────────────────────────────────────────────────────────┐
│                HotSpot 执行引擎                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Java 字节码                                            │
│       │                                                 │
│       ▼                                                 │
│  ┌─────────────────────────────────────────────┐        │
│  │            解释器 (Interpreter)            │        │
│  │  ├── Template Interpreter (x86/ARM/...)   │        │
│  │  ├── 快速启动                               │        │
│  │  ├── 即时执行                               │        │
│  │  └── 收集热点信息                           │        │
│  └─────────────────┬───────────────────────────┘        │
│                    │ (热点检测)                        │
│                    ▼                                   │
│  ┌─────────────────────────────────────────────┐        │
│  │            C1 编译器 (Client)               │        │
│  │  ├── 简单优化                               │        │
│  │  ├── 快速编译                               │        │
│  │  └── 启动性能                               │        │
│  └─────────────────┬───────────────────────────┘        │
│                    │ (更多调用)                       │
│                    ▼                                   │
│  ┌─────────────────────────────────────────────┐        │
│  │            C2 编译器 (Server)               │        │
│  │  ├── 深度优化                               │        │
│  │  ├── 内联                                   │        │
│  │  ├── 循环优化                               │        │
│  │  ├── 向量化                                 │        │
│  │  └── 峰值性能                               │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**关键参数**:

```bash
# 查看编译活动
-XX:+PrintCompilation
-XX:+UnlockDiagnosticVMOptions
-XX:+LogCompilation

# 编译阈值
-XX:CompileThreshold=10000              # C2 编译阈值 (调用次数)
-XX:FreqInlineSize=325                   # 热点方法内联大小限制
-XX:MaxInlineSize=35                     # 最大内联大小
-XX:MaxTrivialSize=6                     # 简单方法最大内联大小

# 禁用分层编译 (不推荐)
-XX:-TieredCompilation
```

### 分层编译

JDK 7+ 引入分层编译 (Tiered Compilation)，结合 C1 和 C2 的优势：

```
编译层级:
Level 0: 解释执行
Level 1: C1 编译 (无 profiling)
Level 2: C1 编译 (有限 profiling)
Level 3: C1 编译 (完全 profiling)
Level 4: C2 编译 (完全优化)
```

```java
// 查看编译级别
-XX:+PrintCompilation -XX:+UnlockDiagnosticVMOptions -XX:+LogCompilation

// 设置分层编译阈值
-XX:Tier3CompileLevel=1000     // C1 → C2 阈值
-XX:Tier4CompileLevel=1500     // C2 编译阈值
```

### 逃逸分析

JDK 6+ 引入逃逸分析 (Escape Analysis)，优化对象分配：

```java
// 逃逸分析示例
public class EscapeAnalysis {
    // 对象未逃逸 - 可以标量替换
    public int sum(int x, int y) {
        Point p = new Point(x, y);  // 可能完全消除
        return p.x + p.y;
    }

    // 对象逃逸 - 必须堆上分配
    public Point createPoint(int x, int y) {
        return new Point(x, y);
    }

    // 对象未逃逸 - 可以栈上分配
    public void method() {
        Point p = new Point(1, 2);
        // p 在此方法内不再使用
    }
}
```

**逃逸分析优化**:

1. **标量替换**: 将对象分解为原始变量
2. **栈上分配**: 未逃逸对象分配在栈上
3. **锁消除**: 未逃逸对象的锁无需同步

```bash
# 启用逃逸分析 (默认启用)
-XX:+DoEscapeAnalysis
-XX:+EliminateAllocations      # 标量替换
-XX:+EliminateLocks             # 锁消除
-XX:+PrintEliminateAllocations  # 查看消除详情
```

#### 实战案例：DecimalDigits.appendPair (JDK-8366224)

> **Issue**: [JDK-8366224](https://bugs.openjdk.org/browse/JDK-8366224)
> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ +12% 日期格式化性能提升

这是一个展示逃逸分析威力的完美案例：

```java
// DecimalDigits.java - 核心实现
public static void appendPair(StringBuilder buf, int v) {
    int packed = DIGITS[v & 0x7f];
    // 看似创建了临时 byte[] 对象...
    buf.append(
        JLA.uncheckedNewStringWithLatin1Bytes(
            new byte[] {(byte) packed, (byte) (packed >> 8)}));
}
```

**关键问题**: `new byte[] {...}` 会不会创建对象？

**答案**: 不会！JIT 的逃逸分析会优化为：

```java
// JIT 优化后的伪代码
// 直接在 StringBuilder 内部缓冲区写入，无任何对象分配
targetBuffer[pos++] = (byte) packed;
targetBuffer[pos++] = (byte) (packed >> 8);
```

**验证方法**:
```bash
# 查看编译后的代码
java -XX:+PrintCompilation -XX:+UnlockDiagnosticVMOptions \
     -XX:+PrintAssembly ...

# 输出显示：无分配指令，只有直接的内存写入
```

**性能影响**:
| 场景 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| LocalDate.toString() | 45 ns | 40 ns | **+11%** |
| MonthDay.toString() | 32 ns | 28 ns | **+13%** |
| 日期格式化 | 1000 ns | 880 ns | **+12%** |

→ [详细分析](/by-pr/8366/8366224.md)

---

## 4. 性能工具

### JFR

Java Flight Recorder (JFR) 是低开销的性能分析工具，JDK 7 引入。

**基本用法**:

```bash
# 启动时开始录制
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr \
     -XX:FlightRecorderOptions=samplethreads=true \
     MyApp

# 运行时控制
jcmd <pid> JFR.start
jcmd <pid> JFR.dump name=recording filename=recording.jfr
jcmd <pid> JFR.stop

# 分析 JFR 文件
jfr --summary recording.jfr
jfr --print recording.jfr
```

**JDK 25+ 新功能**:

- **JEP 509**: CPU-Time Profiling - 更准确的 CPU 时间采样
- **JEP 518**: Cooperative Sampling - 更安全的线程栈采样
- **JEP 520**: Method Timing & Tracing - 精确的方法级测量

### JMC

Java Mission Control (JMC) 是 JFR 的可视化工具。

```bash
# 启动 JMC
jmc
```

---

## 5. 最新增强

### JDK 25 JFR 增强

JDK 25 包含三个重要的 JEP，显著增强 JFR 功能：

#### JEP 509: JFR CPU-Time Profiling

```bash
# 启用 CPU 时间采样 (实验性)
java -XX:StartFlightRecording=jdk.CPUTimeSample#enabled=true ...
```

**新增事件**:
- `jdk.CPUTimeSample` - 记录 Java 和本地代码的 CPU 时间

#### JEP 518: JFR Cooperative Sampling

改进线程栈采样机制，提供更稳定的性能分析。

**改进点**:
- 更安全的异步采样
- 减少采样开销
- 更准确的栈追踪

#### JEP 520: JFR Method Timing & Tracing

```bash
# 启用方法计时
java -XX:StartFlightRecording=jdk.MethodTiming#enabled=true ...
```

**新增事件**:
- `jdk.MethodTiming` - 方法执行时间测量
- `jdk.MethodTrace` - 方法调用追踪

### JDK 25 AOT 缓存

JEP 483 引入 AOT (Ahead-of-Time) 类加载和链接缓存。

**性能提升**:
- 启动时间减少 **42%** (0.018秒 vs 基线)
- 某些场景高达 **59%** 启动时间减少

**创建 AOT 缓存**:

```bash
# 步骤 1: 训练运行，记录类加载行为
java -XX:AOTCacheConfiguration=aot_config.txt \
     -XX:StoreAOTCacheConfiguration \
     MyApp

# 步骤 2: 生成 AOT 缓存
java -XX:AOTCacheConfiguration=aot_config.txt \
     -XX:PrintAOTSharedArchive \
     MyApp

# 步骤 3: 使用 AOT 缓存运行
java -XX:AOTCacheConfiguration=aot_config.txt \
     MyApp
```

**限制**:
- 不支持动态 CDS 归档
- 需要训练运行来捕获类加载行为

### JDK 25 其他性能增强

#### JEP 514: Ahead-of-Time Command-Line Ergonomics

简化 AOT 缓存的命令行参数：

```bash
# JDK 25 简化后的 AOT 缓存创建
java -XX:AOTCache=cache.aot ...
```

#### JEP 515: Ahead-of-Time Method Profiling

AOT 方法 profiling 数据缓存，使 JIT 在启动时立即生成原生代码，部分程序比 JDK 24 训练后应用启动快 **15-25%**。

#### JEP 519: Compact Object Headers

紧凑对象头，减少内存占用：

```bash
# 启用紧凑对象头 (JDK 25+ 默认)
-XX:+UseCompactObjectHeaders
```

**内存节省**: 每个对象节省 8-16 字节

### JDK 26 性能改进

#### JEP 516: Ahead-of-Time Object Caching

进一步扩展 AOT 缓存能力，支持对象和元数据缓存。

**性能影响**: 启动时间减少 30-50%

#### JEP 522: G1 GC Throughput Improvement

G1 GC 吞吐量改进，详见 [GC 演进](../gc/)。

---

## 6. 核心贡献者

> **统计来源**: GitHub Integrated PRs
> **统计时间**: 2026-03-21

### JIT 编译器贡献者

| 排名 | 贡献者 | Integrated PRs | 组织 | 主要贡献 |
|------|--------|----------------|------|----------|
| 1 | [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | 803+ | Amazon | C2 编译器, JMH |
| 2 | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | 200+ | Oracle | C2 编译器优化 |
| 3 | [Tobias Hartmann](/by-contributor/profiles/tobias-hartmann.md) | 150+ | Oracle | JIT 编译器 |
| 4 | [Vladimir Kozlov](/by-contributor/profiles/vladimir-kozlov.md) | 100+ | Oracle | C2 架构 |
| 5 | [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | 90+ | Oracle | C1/C2 编译器 |

### 启动性能贡献者

| 排名 | 贡献者 | Integrated PRs | 组织 | 主要贡献 |
|------|--------|----------------|------|----------|
| 1 | [Ioi Lam](/by-contributor/profiles/ioi-lam.md) | 68 | Oracle | CDS, AOT |
| 2 | [Claes Redestad](/by-contributor/profiles/claes-redestad.md) | 150+ | Oracle | 字符串, 启动优化 |
| 3 | [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | 97 | Alibaba | 核心库性能优化 |
| 4 | [Thomas Stuefe](/by-contributor/profiles/thomas-stuefe.md) | 50+ | Red Hat | CDS, 归档 |

### JFR 贡献者

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| [Erik Gahlin](/by-contributor/profiles/erik-gahlin.md) | Oracle | JFR 架构师, JEP 520 Owner |
| [Markus Grönlund](/by-contributor/profiles/markus-gronlund.md) | Oracle | JFR 事件系统, JEP 518 Owner |
| [Jaroslav Bachorik](/by-contributor/profiles/jaroslav-bachorik.md) | DataDog | JFR 工具，BTrace 创始人 |

---

## 7. 性能最佳实践

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

### 使用虚拟线程 (JDK 21+)

```java
// ✅ 推荐: I/O 密集型任务
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

## 8. 性能对比

### JDK 版本性能对比

| 版本 | 启动时间 | 吞吐量 | 内存 | 主要改进 |
|------|----------|--------|------|----------|
| JDK 8 | 基准 | 基准 | 基准 | Lambda, Stream |
| JDK 11 | +10% | +5% | -10% | HTTP Client, var |
| JDK 17 | +15% | +10% | -15% | Records, 密封类 |
| JDK 21 | +20% | +8% | -20% | 虚拟线程, 分代 ZGC |
| JDK 25 | +35% | +12% | -22% | AOT 缓存, JFR 增强, 紧凑对象头 |
| JDK 26 | +40% | +15% | -25% | AOT 对象缓存, G1 吞吐量改进 |

> 注: 启动时间对比基于使用 AOT 缓存的场景

### 不同场景的性能选择

| 场景 | 推荐版本 | 理由 |
|------|----------|------|
| 微服务 | JDK 21+ | 虚拟线程, 快速启动 |
| 大数据处理 | JDK 17+ | Record, Pattern Matching |
| 云原生 | JDK 25+ | AOT 缓存, Project Leyden |
| 长运行服务 | JDK 17 LTS | 稳定性和性能平衡 |
| Serverless | JDK 25+ | AOT 缓存, 快速启动 |

---

## 9. 重要 PR 分析

### 逃逸分析实战

#### JDK-8366224: DecimalDigits.appendPair

> **Issue**: [JDK-8366224](https://bugs.openjdk.org/browse/JDK-8366224)
> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ +12% 日期格式化性能提升

**核心技巧**: 利用 JIT 逃逸分析消除临时对象

```java
// 看似创建临时对象...
public static void appendPair(StringBuilder buf, int v) {
    buf.append(
        JLA.uncheckedNewStringWithLatin1Bytes(
            new byte[] {(byte) packed, (byte) (packed >> 8)}));
}

// 但 JIT 会优化为直接内存写入，无任何分配！
```

**优化效果**:
- 日期格式化: +12%
- LocalDate.toString(): +11%
- 无 GC 压力增加
- 查找表 + 逃逸分析 = 高效组合

→ [详细分析](/by-pr/8366/8366224.md)

### JIT 内联优化

#### JDK-8365186: DateTimePrintContext 方法拆分

> **Issue**: [JDK-8365186](https://bugs.openjdk.org/browse/JDK-8365186)
> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ +3-12% 日期格式化性能提升

**问题**: `DateTimePrintContext.adjust` 方法 382 字节 > 325 字节内联阈值

**解决方案**: 拆分为三个方法，热路径降至 27 字节

**关键数据**:
- 方法大小：382 → 27 字节（热路径）
- 多平台验证：+3% ~ +12% 性能提升
- 静态 final 场景：+11.66% 提升

→ [详细分析](/by-pr/8365/8365186.md)

### 字符串拼接优化

#### JDK-8355177: StringBuilder append(char[]) 优化

> **Issue**: [JDK-8355177](https://bugs.openjdk.org/browse/JDK-8355177)
> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ +15% 性能提升

使用 `Unsafe.copyMemory` 替代 `System.arraycopy`：

**优化效果**:
- 消除 JNI 边界
- 消除冗余边界检查
- JIT 可完全内联

```java
// 优化前
System.arraycopy(str, 0, value, count, len);

// 优化后
UNSAFE.copyMemory(str, CHAR_ARRAY_BASE_OFFSET,
                  value, CHAR_ARRAY_BASE_OFFSET + (count << 1),
                  len << 1);
```

→ [详细分析](/by-pr/8355/8355177.md)

#### JDK-8343650: StringConcatHelper 优化

> **Issue**: [JDK-8343650](https://bugs.openjdk.org/browse/JDK-8343650)
> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ +5-8% UTF16 拼接性能提升

复用 `StringLatin1.putCharsAt` 和 `StringUTF16.putCharsAt`：

**优化点**:
- 减少方法调用：4-5 次 → 1 次
- 减少边界检查：4-5 次 → 1 次
- 代码更简洁

→ [详细分析](/by-pr/8343/8343650.md)

### 启动性能优化

#### JDK-8349400: 消除匿名内部类

> **Issue**: [JDK-8349400](https://bugs.openjdk.org/browse/JDK-8349400)
> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ 类加载 -90%

将枚举匿名类转换为构造函数参数：

**效果**:
- 类加载数量：11 → 1
- 元空间占用：22KB → 4KB
- Java Agent 场景显著受益

→ [详细分析](/by-pr/8349/8349400.md)

### 字节码生成优化

#### JDK-8341906: ClassFile 写入合并

> **Issue**: [JDK-8341906](https://bugs.openjdk.org/browse/JDK-8341906)
> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ +28% 字节码写入性能

通过写入合并减少方法调用：

```java
// 优化前：3 次调用
buf.writeU1(u1);
buf.writeU2(u2);
buf.writeU4(u4);

// 优化后：1 次调用
buf.writeU1U2U4(u1, u2, u4);
```

**性能分解**:
- 方法调用减少：15%
- 边界检查减少：8%
- 内联优化：3%
- 局部性：2%

→ [详细分析](/by-pr/8341/8341906.md)

---

## 10. 性能优化最佳实践

### 方法设计原则

| 原则 | 说明 | 示例 |
|------|------|------|
| **保持简短** | 热方法 < 50 字节 | JIT 可内联 |
| **早期返回** | 常见情况优先 | 分支预测友好 |
| **冷热分离** | 边界情况单独方法 | 不影响热路径优化 |
| **静态方法** | 消除虚调用 | 更容易内联 |

### 内存分配优化

```java
// ❌ 避免：循环内创建对象
for (int i = 0; i < 1000; i++) {
    String result = "prefix" + i;  // 每次创建新对象
}

// ✅ 推荐：重用对象
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.setLength(0);
    sb.append("prefix").append(i);
}
```

### 字符串拼接优化

```java
// ✅ 简单拼接：使用 +
String result = "Hello " + name;  // 编译器优化为 StringBuilder

// ✅ 循环拼接：使用 StringBuilder
StringBuilder sb = new StringBuilder();
for (String s : list) {
    sb.append(s);  // 受益于 JDK-8355177 优化
}

// ✅ 格式化：使用 String.format（静态 final 更优）
private static final DateTimeFormatter FORMATTER =
    DateTimeFormatter.ofPattern("yyyy-MM-dd");
String date = FORMATTER.format(LocalDate.now());  // 受益于 JIT 常量传播
```

---

## 11. 相关链接

### 内部文档

- [性能时间线](timeline.md) - 详细的历史演进
- [JVM 调优](../jvm/) - JVM 参数调优
- [内存管理](../memory/) - 堆、栈、Metaspace
- [GC 演进](../gc/) - 垃圾回收器演进

### 外部资源

- [Tuning Garbage Collectors](https://docs.oracle.com/en/java/javase/21/gctuning/)
- [Java Flight Recorder](https://docs.oracle.com/en/java/javase/21/docs/specs/man/jfr.html)
- [Inside Java: Performance Updates](https://inside.java/)
- [Project Leyden](https://openjdk.org/projects/leyden/)

### 相关 JEP

| JEP | 标题 | 版本 | 状态 |
|-----|------|------|------|
| [JEP 483](/jeps/tools/jep-483.md) | Ahead-of-Time Class Loading & Linking | JDK 25 | ✅ Delivered |
| [JEP 509](/jeps/jfr/jep-509.md) | JFR CPU-Time Profiling | JDK 25 | ✅ Delivered |
| [JEP 514](/jeps/performance/jep-514.md) | Ahead-of-Time Command-Line Ergonomics | JDK 25 | ✅ Delivered |
| [JEP 515](/jeps/performance/jep-515.md) | Ahead-of-Time Method Analysis | JDK 25 | ✅ Delivered |
| [JEP 516](https://openjdk.org/jeps/516) | Ahead-of-Time Object Caching with Any GC | JDK 26 | ✅ Delivered |
| [JEP 518](/jeps/jfr/jep-518.md) | JFR Cooperative Sampling | JDK 25 | ✅ Delivered |
| [JEP 519](/jeps/gc/jep-519.md) | Compact Object Headers | JDK 25 | ✅ Delivered |
| [JEP 520](/jeps/jfr/jep-520.md) | JFR Method Timing & Tracing | JDK 25 | ✅ Delivered |
| [JEP 522](/jeps/gc/jep-522.md) | G1 GC: Improve Throughput by Reducing Synchronization | JDK 26 | ✅ Delivered |

### Git 命令参考

```bash
# 查看 JIT 编译器相关提交
cd /root/git/jdk
git log --oneline -- src/hotspot/share/compiler/ | head -20

# 查看 JFR 相关提交
git log --oneline -- src/hotspot/share/jfr/ | head -20

# 查看 CDS/AOT 相关提交
git log --oneline -- src/hotspot/share/cds/ | head -20

# 查看 GC 相关提交
git log --oneline -- src/hotspot/share/gc/g1/ | head -20
```

### 性能测试命令

```bash
# 使用 JMH 运行基准测试
java -jar target/benchmarks.jar

# 使用 async-profiler 进行 CPU 采样
./profiler.sh -d 30 -f profile.html <pid>

# 查看 JIT 编译日志
java -XX:+PrintCompilation -XX:+UnlockDiagnosticVMOptions MyApp
```

---

**最后更新**: 2026-03-21
