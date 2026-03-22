# 性能优化

> JIT、分层编译、逃逸分析、JFR、AOT 缓存演进历程

[← 返回核心平台](../)

---

## 目录

1. [TL;DR 快速概览](#1-tldr-快速概览)
2. [快速概览](#2-快速概览)
3. [核心技术](#3-核心技术)
4. [启动优化 Startup Optimization](#4-启动优化-startup-optimization)
5. [吞吐量优化 Throughput Optimization](#5-吞吐量优化-throughput-optimization)
6. [延迟优化 Latency Optimization](#6-延迟优化-latency-optimization)
7. [内存优化 Memory Optimization](#7-内存优化-memory-optimization)
8. [监控工具链 Observability Toolchain](#8-监控工具链-observability-toolchain)
9. [Benchmark 方法论 Benchmarking Methodology](#9-benchmark-方法论-benchmarking-methodology)
10. [性能最佳实践](#10-性能最佳实践)
11. [性能对比](#11-性能对比)
12. [重要 PR 分析](#12-重要-pr-分析)
13. [核心贡献者](#13-核心贡献者)
14. [相关链接](#14-相关链接)

---

## 1. TL;DR 快速概览

> **1 分钟了解 Java 性能优化**

### 快速决策树

```
性能问题？
  │
  ├─ 启动慢 (Slow Startup) → CDS/AppCDS/AOT Cache → 第 4 节
  │
  ├─ 吞吐量低 (Low Throughput) → GC 选择 + 编译器调优 → 第 5 节
  │
  ├─ 延迟高 (High Latency) → GC 暂停 + JIT 预热 → 第 6 节
  │
  ├─ 内存高 (High Memory) → 堆调优 + Compact Headers → 第 7 节
  │
  ├─ 需要诊断 (Need Profiling) → JFR + async-profiler → 第 8 节
  │
  └─ 需要基准测试 (Need Benchmarks) → JMH → 第 9 节
```

### 常用 VM 参数

```bash
# 堆内存设置 (Heap Sizing)
-Xms2g -Xmx2g

# GC 选择 (JDK 17+)
-XX:+UseZGC                    # 低延迟 (Low Latency)
-XX:+UseG1GC                   # 通用 (General Purpose)

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
JDK 1.0 ── JDK 5 ── JDK 7 ── JDK 8 ── JDK 17 ── JDK 21 ── JDK 24 ── JDK 25 ── JDK 26
   │         │        │        │        │        │        │        │         │
解释器    分层   G1 GC  Lambda  Graal  虚拟线程 AOT缓存  AOT简化    AOT对象
(纯解释)  编译   默认   Stream  (实验)  (正式) JEP483  JEP514/515  JEP516
                                                       紧凑对象头  基线缓存
                                                       JEP519     ZGC支持
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
| **AOT 类加载缓存** | JDK 24 | JEP 483 预加载类链接 | 新增 |
| **AOT 命令行简化** | JDK 25 | JEP 514 简化 AOT 缓存创建 | 新增 |
| **AOT 方法 Profiling** | JDK 25 | JEP 515 缓存方法 profiling 数据 | 新增 |
| **AOT 对象缓存** | JDK 26 | JEP 516 支持任意 GC, 内置基线缓存 | 新增 |

---

## 3. 核心技术

### JIT 编译 (Just-In-Time Compilation)

HotSpot VM 包含两个 JIT 编译器：

```
字节码 → 解释器 (Interpreter, 快速启动, 收集热点信息)
           │ 热点检测
           ▼
         C1 编译器 (Client, 简单优化, 快速编译)
           │ 更多调用
           ▼
         C2 编译器 (Server, 深度优化, 内联/循环优化/向量化, 峰值性能)
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

### 分层编译 (Tiered Compilation)

JDK 7+ 引入分层编译，结合 C1 和 C2 的优势：

```
编译层级 (Compilation Tiers):
Level 0: 解释执行 (Interpreter)
Level 1: C1 编译 (无 profiling)
Level 2: C1 编译 (有限 profiling)
Level 3: C1 编译 (完全 profiling) ← 收集调用计数、分支概率
Level 4: C2 编译 (完全优化)      ← 基于 profiling 数据深度优化
```

```bash
# 查看编译级别
-XX:+PrintCompilation -XX:+UnlockDiagnosticVMOptions -XX:+LogCompilation

# 设置分层编译阈值
-XX:Tier3CompileLevel=1000     # C1 → C2 阈值
-XX:Tier4CompileLevel=1500     # C2 编译阈值
```

### 逃逸分析 (Escape Analysis)

JDK 6+ 引入逃逸分析，优化对象分配：

```java
// 逃逸分析示例
public class EscapeAnalysis {
    // 对象未逃逸 (NoEscape) - 可以标量替换
    public int sum(int x, int y) {
        Point p = new Point(x, y);  // 可能完全消除
        return p.x + p.y;
    }

    // 对象逃逸 (GlobalEscape) - 必须堆上分配
    public Point createPoint(int x, int y) {
        return new Point(x, y);
    }

    // 对象未逃逸 (NoEscape) - 可以栈上分配
    public void method() {
        Point p = new Point(1, 2);
        // p 在此方法内不再使用
    }
}
```

**逃逸分析优化**:

1. **标量替换 (Scalar Replacement)**: 将对象分解为原始变量
2. **栈上分配 (Stack Allocation)**: 未逃逸对象分配在栈上
3. **锁消除 (Lock Elision)**: 未逃逸对象的锁无需同步

```bash
# 启用逃逸分析 (默认启用)
-XX:+DoEscapeAnalysis
-XX:+EliminateAllocations      # 标量替换
-XX:+EliminateLocks             # 锁消除
-XX:+PrintEliminateAllocations  # 查看消除详情
```

**实战案例**: [JDK-8366224 DecimalDigits.appendPair](/by-pr/8366/8366224.md) - 利用逃逸分析消除 `new byte[]` 临时对象，日期格式化 +12%。详见[第 12 节 PR 分析](#12-重要-pr-分析)。

---

## 4. 启动优化 Startup Optimization

### CDS / AppCDS / AOT Cache 演进

```
JDK 5     JDK 10     JDK 13      JDK 24       JDK 25       JDK 26
  │         │          │           │            │            │
 CDS     AppCDS    Dynamic     AOT Cache    AOT简化      AOT对象
(基础)   (应用类)   CDS归档    JEP 483     JEP 514/515   JEP 516
                  (自动生成)  (类加载链接)  (命令行简化)   (任意GC)
                                            (方法Profiling) (基线缓存)
```

### CDS 基础 (Class Data Sharing)

CDS 将类元数据预处理后存入共享归档文件 (shared archive)，多个 JVM 进程可共享该内存映射区域。

```bash
# 步骤 1: 生成默认共享归档
java -Xshare:dump

# 步骤 2: 使用共享归档启动
java -Xshare:on -jar app.jar

# 查看 CDS 加载情况
java -Xlog:class+load -jar app.jar 2>&1 | grep "shared objects"
```

### AppCDS (Application CDS)

AppCDS 扩展 CDS 支持应用程序类：

```bash
# 步骤 1: 记录类列表
java -Xshare:off -XX:DumpLoadedClassList=classes.lst \
     -jar app.jar

# 步骤 2: 创建应用归档
java -Xshare:dump -XX:SharedClassListFile=classes.lst \
     -XX:SharedArchiveFile=app-cds.jsa \
     -jar app.jar

# 步骤 3: 使用应用归档启动
java -Xshare:on -XX:SharedArchiveFile=app-cds.jsa \
     -jar app.jar
```

### AOT Cache (JDK 24+ / JEP 483, 514, 515, 516)

AOT Cache 是 CDS 的演进，将类加载、链接、甚至 JIT profiling 数据都缓存起来。

```bash
# === JDK 24 方式 (JEP 483) ===
# 步骤 1: 训练运行 (Training Run)，记录类加载行为
java -XX:AOTCacheConfiguration=aot_config.txt \
     -XX:StoreAOTCacheConfiguration \
     -jar app.jar

# 步骤 2: 生成 AOT 缓存
java -XX:AOTCacheConfiguration=aot_config.txt \
     -XX:PrintAOTSharedArchive \
     -jar app.jar

# 步骤 3: 使用 AOT 缓存运行
java -XX:AOTCacheConfiguration=aot_config.txt \
     -jar app.jar

# === JDK 25 简化方式 (JEP 514) ===
# 一行命令创建并使用 AOT 缓存
java -XX:AOTCache=app.aot -jar app.jar
```

**JEP 515: AOT Method Profiling** - JIT 在启动时立即使用缓存的 profiling 数据生成优化代码，部分程序比 JDK 24 训练后应用启动再快 **15-25%**。

**JEP 516 (JDK 26): AOT 对象缓存 + 任意 GC 支持**:
- 对象引用存储为逻辑索引而非物理地址，后台线程逐个材料化 (materialize) 对象
- JDK 26 自带覆盖 JDK 类的**基线 AOT 缓存** (Baseline AOT Cache)，即使不训练也有启动改善
- 消除 JDK 24/25 中 AOT 不支持 ZGC 的限制

### Spring Boot 启动优化实践

```bash
# 1. 使用 AOT Cache (JDK 25+)
java -XX:AOTCache=spring-app.aot -jar spring-app.jar

# 2. Spring Boot 3.x 自带 AOT 处理
./mvnw spring-boot:process-aot
java -Dspring.aot.enabled=true -jar spring-app.jar

# 3. 组合优化：AOT Cache + Spring AOT
java -XX:AOTCache=spring-app.aot \
     -Dspring.aot.enabled=true \
     -jar spring-app.jar

# 4. 惰性初始化 (Lazy Initialization) 减少启动加载
# application.properties
spring.main.lazy-initialization=true
```

**Spring Boot 启动优化效果**:

| 优化手段 | 启动时间 (典型 Web 应用) | 改善幅度 |
|----------|--------------------------|----------|
| 无优化 | ~3.5s | 基线 |
| AppCDS | ~2.8s | ~20% |
| AOT Cache (JDK 25) | ~2.0s | ~42% |
| AOT + Spring AOT | ~1.5s | ~57% |
| AOT + Lazy Init | ~1.2s | ~65% |

---

## 5. 吞吐量优化 Throughput Optimization

### GC 选择指南 (GC Selection Guide)

```
应用类型？
  │
  ├─ 批处理/大数据 (Batch/Big Data)
  │   └─ Parallel GC: -XX:+UseParallelGC
  │       最大吞吐量，STW 暂停可接受
  │
  ├─ 通用 Web 服务 (General Web Service)
  │   └─ G1 GC: -XX:+UseG1GC  (JDK 9+ 默认)
  │       吞吐量与延迟均衡
  │
  ├─ 低延迟交易系统 (Low-Latency Trading)
  │   └─ ZGC: -XX:+UseZGC
  │       亚毫秒暂停，堆大小无关
  │
  └─ 超大堆 (> 32GB) + 低延迟
      └─ ZGC: -XX:+UseZGC
          TB 级堆支持
```

**GC 性能对比 (JDK 25 基准)**:

| GC | 吞吐量 | 最大暂停 | 平均暂停 | 适用堆大小 | 适用场景 |
|----|--------|----------|----------|------------|----------|
| **Parallel GC** | 最高 | 100ms-1s+ | 50-200ms | 1-32GB | 批处理 |
| **G1 GC** | 高 | 10-100ms | 5-30ms | 4-64GB | 通用 |
| **ZGC** | 较高 | < 1ms | < 0.5ms | 8GB-16TB | 低延迟 |

```bash
# Parallel GC - 最大吞吐量
java -XX:+UseParallelGC \
     -XX:ParallelGCThreads=8 \
     -XX:MaxGCPauseMillis=200 \
     -jar app.jar

# G1 GC - 均衡配置
java -XX:+UseG1GC \
     -XX:MaxGCPauseMillis=50 \
     -XX:G1HeapRegionSize=16m \
     -XX:InitiatingHeapOccupancyPercent=45 \
     -jar app.jar

# ZGC - 低延迟 (JDK 21+ 分代 ZGC)
java -XX:+UseZGC \
     -XX:+ZGenerational \
     -jar app.jar
```

### 编译器调优 (Compiler Tuning)

```bash
# 查看热点编译活动
java -XX:+PrintCompilation -jar app.jar

# 输出格式:
#   时间戳  编译ID  属性  级别  方法名  大小  [deopt]
#   1234    567     b    4    com.example.App::hotMethod (52 bytes)
#   属性: b=阻塞 s=同步 %=OSR n=native !=(有异常处理)

# 增加编译线程数 (多核机器)
-XX:CICompilerCount=4

# 增大代码缓存 (大型应用)
-XX:ReservedCodeCacheSize=512m
-XX:InitialCodeCacheSize=128m

# 查看代码缓存使用情况
jcmd <pid> Compiler.codecache
```

### 内联优化 (Inlining Optimization)

内联 (Inlining) 是 JIT 最重要的优化之一，将被调用方法的代码直接嵌入调用方。

```bash
# 关键内联参数
-XX:MaxInlineSize=35          # 方法字节码 <= 35 字节 → 总是内联
-XX:FreqInlineSize=325        # 热点方法字节码 <= 325 字节 → 内联
-XX:MaxTrivialSize=6          # 简单方法 (getter/setter) → 总是内联
-XX:InlineSmallCode=2000      # 已编译代码 <= 2000 字节 → 可内联

# 查看内联决策
-XX:+PrintInlining -XX:+UnlockDiagnosticVMOptions
```

**内联优化实战 - JDK-8365186**:

```java
// 问题: adjust() 方法 382 字节 > 325 字节内联阈值 (FreqInlineSize)
// 解决: 拆分为三个方法，热路径降至 27 字节

// 优化前 - 单一大方法
TemporalAccessor adjust(TemporalAccessor temporal) {
    // 382 字节... 无法内联!
}

// 优化后 - 热路径方法仅 27 字节
TemporalAccessor adjust(TemporalAccessor temporal) {
    if (/* 常见情况 */) return temporal;  // 27 字节，轻松内联
    return adjustSlow(temporal);           // 冷路径分离
}
```

-> [详细分析](/by-pr/8365/8365186.md)

---

## 6. 延迟优化 Latency Optimization

### GC 暂停控制 (GC Pause Control)

```bash
# G1 暂停时间目标 (Pause-Time Target)
-XX:MaxGCPauseMillis=20       # 目标最大暂停 20ms (默认 200ms)
-XX:GCPauseIntervalMillis=200 # 暂停间隔至少 200ms

# ZGC 亚毫秒暂停 (Sub-millisecond Pauses)
-XX:+UseZGC
-XX:+ZGenerational             # JDK 21+ 分代 ZGC，降低内存开销

# G1 调优: 避免 Full GC
-XX:G1ReservePercent=15        # 保留堆百分比，避免 evacuation failure
-XX:G1MixedGCCountTarget=8    # Mixed GC 目标次数
-XX:G1HeapWastePercent=5       # 可回收堆浪费阈值

# GC 日志 (JDK 17+ 统一日志)
-Xlog:gc*:file=gc.log:time,uptime,level,tags:filecount=5,filesize=10m
```

**GC 日志分析关键指标**:

```
# 关注以下指标:
# 1. Pause Young (Normal)  - Young GC 暂停时间
# 2. Pause Young (Concurrent Start) - 触发并发标记
# 3. Pause Full            - Full GC (应避免!)
# 4. To-space Exhausted    - 空间不足 (需增大堆或调优)

# 快速分析 GC 日志
grep -E "Pause|Full|Exhausted" gc.log | tail -20
```

### JIT 预热 (JIT Warm-up)

JIT 预热 (Warm-up) 是指应用启动后 JIT 编译尚未完成、代码仍在解释执行的阶段，此时性能显著低于峰值。

```bash
# 策略 1: AOT Cache 缓存 profiling 数据 (JDK 25+ JEP 515)
# 训练运行后，JIT 启动时直接使用 profiling → 更快达到峰值
java -XX:AOTCache=app.aot -jar app.jar

# 策略 2: 预热脚本 - 在接受真实流量前发送预热请求
# warmup.sh
for i in $(seq 1 1000); do
    curl -s http://localhost:8080/api/health > /dev/null
    curl -s http://localhost:8080/api/critical-path > /dev/null
done
echo "Warm-up complete, ready for traffic"

# 策略 3: 调整编译阈值加快预热
-XX:CompileThreshold=1000     # 降低阈值，更早触发 C2 编译 (默认 10000)
-XX:Tier3InvocationThreshold=200   # 更早触发 C1 编译
```

### 分层编译调优 (Tiered Compilation Tuning)

```bash
# 查看分层编译状态
-XX:+PrintCompilation
# 输出中 Level 列: 0=解释, 1-3=C1, 4=C2

# 强制使用 C2 (牺牲启动换峰值，不推荐生产)
-XX:-TieredCompilation -XX:+UseCompactObjectHeaders

# 限制最高编译级别
-XX:TieredStopAtLevel=3       # 只用 C1, 快速编译、较低峰值

# C2 编译队列监控
jcmd <pid> Compiler.queue     # 查看待编译方法队列

# 如果编译队列积压严重，增加编译线程
-XX:CICompilerCount=8
```

**分层编译预热曲线**:

```
性能
 ▲
 │                    ┌──────────── Level 4 (C2 峰值)
 │                 ╱──┘
 │              ╱──
 │           ╱── Level 3 (C1 + profiling)
 │        ╱──
 │     ╱── Level 1-2 (C1 基础)
 │  ╱──
 │╱── Level 0 (解释执行)
 └──────────────────────────────────→ 时间
   0s    5s    15s    30s    60s
        ↑ 典型 Web 应用预热时间
```

---

## 7. 内存优化 Memory Optimization

### 堆大小调优 (Heap Sizing)

```bash
# 基本堆设置
-Xms4g -Xmx4g                 # 固定堆大小，避免堆扩缩开销
-XX:NewRatio=2                 # Old:Young = 2:1
-XX:SurvivorRatio=8            # Eden:Survivor = 8:1

# 容器环境 (Container-Aware, JDK 10+)
-XX:+UseContainerSupport       # 默认启用
-XX:MaxRAMPercentage=75.0      # 使用容器内存的 75%
-XX:InitialRAMPercentage=50.0  # 初始堆设为容器内存的 50%

# 监控堆使用
jcmd <pid> GC.heap_info
jcmd <pid> VM.native_memory summary
```

**堆大小选择原则**:

| 场景 | 推荐配置 | 理由 |
|------|----------|------|
| 微服务 (< 1GB) | `-Xms512m -Xmx512m` | 固定堆，快速启动 |
| Web 应用 (1-8GB) | `-Xms4g -Xmx4g` | 预分配避免扩容 |
| 大数据处理 (> 8GB) | `-Xms16g -Xmx16g -XX:+UseZGC` | 大堆 + 低暂停 |
| 容器化部署 | `-XX:MaxRAMPercentage=75.0` | 自动适配容器限制 |

### CompressedOops (压缩普通对象指针)

```bash
# CompressedOops: 64 位 JVM 使用 32 位引用，节省内存
# 堆 <= 32GB 时自动启用; 堆 > 32GB 时自动关闭
-XX:+UseCompressedOops          # 默认启用 (堆 <= 32GB)
-XX:+UseCompressedClassPointers # 默认启用

# 查看 CompressedOops 状态
java -XX:+PrintFlagsFinal -version 2>&1 | grep -i compress
```

**关键陷阱**: 堆大小跨越 32GB 边界时性能可能下降!

```
堆大小 vs 可用内存:
  28GB 堆 (压缩指针)  ≈ 等效于 36-40GB 堆 (无压缩)
  33GB 堆 (无压缩指针) < 28GB 堆 (压缩指针) 的可用空间!

  → 如果堆需要 30-35GB，考虑降到 31GB 以内保持压缩指针
  → 或直接跳到 40GB+ 以充分利用无压缩指针
```

### Compact Object Headers (紧凑对象头, JEP 519)

JDK 25 引入 (Project Lilliput)，对象头从 12 字节缩减到 8 字节:

```bash
# 启用紧凑对象头 (JDK 25+ 生产就绪，但非默认启用)
-XX:+UseCompactObjectHeaders
```

**内存节省**:
- 每个对象节省 4 字节
- SPECjbb2015: 堆空间减少 **22%**，CPU 时间减少 **8%**
- 含大量小对象的应用: 活跃数据减少 **10-20%**

```
标准对象头 (12 字节):          紧凑对象头 (8 字节):
┌────────────────────┐        ┌────────────────────┐
│ Mark Word (8 bytes)│        │ Mark Word (8 bytes) │
├────────────────────┤        │ (含压缩类指针)      │
│ Klass Ptr (4 bytes)│        └────────────────────┘
└────────────────────┘
```

### String Deduplication (字符串去重)

```bash
# G1 GC 自动字符串去重 (JDK 8u20+)
-XX:+UseG1GC -XX:+UseStringDeduplication

# 查看去重统计
-XX:+PrintStringDeduplicationStatistics

# ZGC 也支持字符串去重 (JDK 18+)
-XX:+UseZGC -XX:+UseStringDeduplication
```

**适用场景**: 应用中存在大量重复字符串 (如 XML/JSON 解析、日志字段名)。

```java
// 代码层面的字符串优化
// 1. String.intern() - 手动去重 (谨慎使用，可能导致 PermGen/Metaspace 增长)
String canonical = rawString.intern();

// 2. JDK 9+ Compact Strings - 自动使用 Latin-1 编码存储 ASCII 字符串
// 无需代码改动，String 内部自动选择 byte[] (Latin-1) 或 char[] (UTF-16)
// 内存节省约 10-20% (英文文本为主的应用)
```

---

## 8. 监控工具链 Observability Toolchain

### JFR + JMC 使用指南 (Java Flight Recorder + Mission Control)

JFR 是内建于 JVM 的低开销 (< 2%) 生产级性能分析工具。

**启动方式**:

```bash
# 方式 1: 启动时开启录制
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr \
     -XX:FlightRecorderOptions=samplethreads=true \
     -jar app.jar

# 方式 2: 运行时动态开启
jcmd <pid> JFR.start name=profile duration=120s filename=profile.jfr

# 方式 3: 持续录制 + 按需转储 (生产推荐)
java -XX:StartFlightRecording=disk=true,maxsize=500m,maxage=24h \
     -jar app.jar

# 按需转储最近数据
jcmd <pid> JFR.dump name=1 filename=dump.jfr

# 停止录制
jcmd <pid> JFR.stop name=1
```

**JFR 命令行分析**:

```bash
# 查看录制概要
jfr summary recording.jfr

# 打印特定事件
jfr print --events jdk.GCPhasePause recording.jfr
jfr print --events jdk.CPULoad recording.jfr
jfr print --events jdk.ThreadSleep recording.jfr

# 过滤指定时间范围
jfr print --events jdk.ExecutionSample \
     --start "2026-03-22 10:00:00" \
     --end "2026-03-22 10:05:00" \
     recording.jfr
```

**JMC 可视化分析**:

```bash
# 启动 JMC (需要图形界面)
jmc

# JMC 关键视图:
# 1. Automated Analysis   - 自动分析瓶颈 (推荐首先查看)
# 2. Java Application     - CPU、堆、线程概览
# 3. Method Profiling     - 热点方法分析
# 4. Memory               - 内存分配、GC 活动
# 5. Lock Instances       - 锁竞争分析
# 6. File I/O / Socket I/O - I/O 瓶颈
```

**JDK 25+ JFR 新功能**:

| JEP | 功能 | 用途 |
|-----|------|------|
| JEP 509 | CPU-Time Profiling | 精确 CPU 时间采样 (区分 CPU vs Wall-clock) |
| JEP 518 | Cooperative Sampling | 更安全的异步栈采样，减少采样偏差 |
| JEP 520 | Method Timing & Tracing | 方法级执行时间和调用追踪 |

```bash
# JDK 25: 启用 CPU 时间采样
java -XX:StartFlightRecording=jdk.CPUTimeSample#enabled=true \
     -jar app.jar

# JDK 25: 启用方法计时
java -XX:StartFlightRecording=jdk.MethodTiming#enabled=true \
     -jar app.jar
```

### async-profiler 使用指南

[async-profiler](https://github.com/async-profiler/async-profiler) 是低开销的采样分析器，支持 CPU、内存分配、锁分析，无 safepoint bias。

```bash
# 安装
# 下载: https://github.com/async-profiler/async-profiler/releases
tar xzf async-profiler-*.tar.gz

# CPU 采样 (30 秒)，输出火焰图
./asprof -d 30 -f cpu-flamegraph.html <pid>

# 内存分配采样 (Allocation Profiling)
./asprof -d 30 -e alloc -f alloc-flamegraph.html <pid>

# 锁竞争分析 (Lock Profiling)
./asprof -d 30 -e lock -f lock-flamegraph.html <pid>

# Wall-clock 采样 (包含等待时间，排查 I/O 阻塞)
./asprof -d 30 -e wall -f wall-flamegraph.html <pid>

# 作为 Java Agent 启动
java -agentpath:/path/to/libasyncProfiler.so=start,event=cpu,file=profile.html \
     -jar app.jar
```

### 火焰图解读 (Flame Graph Interpretation)

```
火焰图阅读方法:
  ┌─────────────────────────────────────────────┐
  │               main()                        │  ← 调用栈底部
  ├──────────────────────┬──────────────────────┤
  │    handleRequest()   │   processQueue()     │  ← 调用方法
  ├──────────┬───────────┤                      │
  │ doQuery()│ serialize()│                     │  ← 更深层调用
  ├──────────┤           │                      │
  │ SQL exec │           │                      │  ← 热点方法 (宽=耗时)
  └──────────┴───────────┴──────────────────────┘

  X 轴: 采样占比 (越宽=占用 CPU 越多)
  Y 轴: 调用栈深度 (底→顶 = 调用者→被调用者)
  颜色: 通常无特殊含义 (便于区分不同帧)

  关注点:
  1. 最宽的"平顶" (plateau) → CPU 热点方法
  2. 深而窄的"尖塔" (tower) → 深层递归，通常非瓶颈
  3. 突然变宽的层级 → 该方法调用了多个耗时子方法
```

---

## 9. Benchmark 方法论 Benchmarking Methodology

### JMH 使用指南 (Java Microbenchmark Harness)

JMH 是 OpenJDK 官方微基准测试框架，由 Aleksey Shipilev (JIT 编译器作者) 开发。

```bash
# 创建 JMH 项目
mvn archetype:generate \
    -DinteractiveMode=false \
    -DarchetypeGroupId=org.openjdk.jmh \
    -DarchetypeArtifactId=jmh-java-benchmark-archetype \
    -DgroupId=com.example \
    -DartifactId=benchmarks \
    -Dversion=1.0

# 编译并运行
cd benchmarks
mvn clean package
java -jar target/benchmarks.jar
```

**JMH 基准测试示例**:

```java
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
@State(Scope.Thread)
@Warmup(iterations = 5, time = 1)          // 预热 5 轮
@Measurement(iterations = 5, time = 1)     // 测量 5 轮
@Fork(2)                                    // 2 个 JVM 进程
public class StringBenchmark {

    private String data = "Hello, World!";

    @Benchmark
    public String concat() {
        return data + " suffix";
    }

    @Benchmark
    public String format() {
        return String.format("%s suffix", data);
    }

    @Benchmark
    public String builder() {
        return new StringBuilder(data).append(" suffix").toString();
    }
}
```

**常用 JMH 运行参数**:

```bash
# 运行指定 benchmark
java -jar benchmarks.jar StringBenchmark

# 指定模式: thrpt(吞吐量), avgt(平均时间), sample(采样), ss(单次)
java -jar benchmarks.jar -bm avgt

# 输出 JSON 结果 (可用于对比)
java -jar benchmarks.jar -rf json -rff results.json

# 配合 async-profiler 生成火焰图
java -jar benchmarks.jar -prof async:output=flamegraph

# 查看 GC 分配统计
java -jar benchmarks.jar -prof gc

# 查看 JIT 编译统计
java -jar benchmarks.jar -prof comp
```

### 常见 Benchmark 陷阱 (Common Pitfalls)

#### 陷阱 1: 死代码消除 (Dead Code Elimination)

```java
// 错误: JIT 会发现 result 未使用，直接消除计算
@Benchmark
public void wrong() {
    int result = data.hashCode();  // 被 JIT 消除!
}

// 正确: 通过 Blackhole 或返回值阻止消除
@Benchmark
public int correct() {
    return data.hashCode();        // 返回值不会被消除
}

@Benchmark
public void correctWithBlackhole(Blackhole bh) {
    bh.consume(data.hashCode());   // Blackhole 阻止消除
}
```

#### 陷阱 2: 常量折叠 (Constant Folding)

```java
// 错误: JIT 在编译时计算出结果，benchmark 测的是常量加载
@Benchmark
public int wrong() {
    return 42 * 37;  // JIT 直接替换为 1554
}

// 正确: 使用 @State 字段，阻止编译期常量折叠
@State(Scope.Thread)
public class MyBenchmark {
    int x = 42, y = 37;

    @Benchmark
    public int correct() {
        return x * y;  // 运行时计算
    }
}
```

#### 陷阱 3: 循环优化 (Loop Optimization)

```java
// 错误: JIT 可能优化掉整个循环或合并迭代
@Benchmark
public int wrong() {
    int sum = 0;
    for (int i = 0; i < 1000; i++) {
        sum += i;  // JIT 可能直接用公式替换: 1000*999/2
    }
    return sum;
}

// 正确: 让 JMH 控制迭代，每次 @Benchmark 只做一次操作
@Benchmark
public int correct() {
    return data[index++ % data.length];
}
```

#### 陷阱 4: 未预热 (No Warm-up)

```java
// 错误: 没有预热，测量的是解释执行 + JIT 编译的混合性能
@Warmup(iterations = 0)  // 不要这样做!
@Benchmark
public int wrong() { ... }

// 正确: 充分预热，确保 C2 编译完成
@Warmup(iterations = 5, time = 2)
@Measurement(iterations = 5, time = 2)
@Fork(2)  // 多 fork 消除 JVM 启动差异
@Benchmark
public int correct() { ... }
```

#### 陷阱 5: 忽略 GC 影响 (Ignoring GC Impact)

```bash
# 使用 -prof gc 查看分配率和 GC 时间
java -jar benchmarks.jar -prof gc MyBenchmark

# 输出示例:
# gc.alloc.rate       2048.000 MB/sec  ← 分配率过高!
# gc.count            12               ← benchmark 期间 GC 次数
# gc.time             45 ms            ← GC 总耗时

# 如果 gc.count > 0, 结果可能被 GC 干扰
# 解决: 增大堆 (-Xmx8g) 或优化分配
```

---

## 10. 性能最佳实践

### 方法设计原则

| 原则 | 说明 | JIT 效果 |
|------|------|----------|
| **保持简短** | 热方法 < 50 字节码 | 可内联 (MaxInlineSize=35) |
| **早期返回** | 常见情况优先 | 分支预测友好 |
| **冷热分离** | 异常路径拆为独立方法 | 不影响热路径内联 |
| **静态/final** | 消除虚调用 | 更容易去虚化+内联 |
| **重用对象** | 避免循环内分配 | 降低 GC 压力 |
| **集合指定容量** | `new ArrayList<>(n)` | 避免多次扩容拷贝 |
| **StringBuilder** | 循环拼接用 SB | 避免每次创建新 String |
| **虚拟线程** | I/O 密集型使用 (JDK 21+) | CPU 密集型无提升 |

---

## 11. 性能对比

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

## 12. 重要 PR 分析

### 逃逸分析实战

#### JDK-8366224: DecimalDigits.appendPair

> **Issue**: [JDK-8366224](https://bugs.openjdk.org/browse/JDK-8366224)
> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: +12% 日期格式化性能提升

**核心技巧**: 利用 JIT 逃逸分析消除临时对象

```java
// 看似创建临时对象...
public static void appendPair(StringBuilder buf, int v) {
    buf.append(
        JLA.uncheckedNewStringWithLatin1Bytes(
            new byte[] {(byte) packed, (byte) (packed >> 8)}));
}

// 但 JIT 会优化为直接内存写入，无任何分配!
```

**优化效果**:
- 日期格式化: +12%
- LocalDate.toString(): +11%
- 无 GC 压力增加
- 查找表 + 逃逸分析 = 高效组合

-> [详细分析](/by-pr/8366/8366224.md)

### JIT 内联优化

#### JDK-8365186: DateTimePrintContext 方法拆分

> **Issue**: [JDK-8365186](https://bugs.openjdk.org/browse/JDK-8365186)
> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: +3-12% 日期格式化性能提升

**问题**: `DateTimePrintContext.adjust` 方法 382 字节 > 325 字节内联阈值

**解决方案**: 拆分为三个方法，热路径降至 27 字节

**关键数据**:
- 方法大小：382 -> 27 字节（热路径）
- 多平台验证：+3% ~ +12% 性能提升
- 静态 final 场景：+11.66% 提升

-> [详细分析](/by-pr/8365/8365186.md)

### 字符串拼接优化

#### JDK-8355177: StringBuilder append(char[]) 优化

> **Issue**: [JDK-8355177](https://bugs.openjdk.org/browse/JDK-8355177)
> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: +15% 性能提升

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

-> [详细分析](/by-pr/8355/8355177.md)

#### JDK-8343650: StringConcatHelper 优化

> **Issue**: [JDK-8343650](https://bugs.openjdk.org/browse/JDK-8343650)
> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: +5-8% UTF16 拼接性能提升

复用 `StringLatin1.putCharsAt` 和 `StringUTF16.putCharsAt`：

**优化点**:
- 减少方法调用：4-5 次 -> 1 次
- 减少边界检查：4-5 次 -> 1 次
- 代码更简洁

-> [详细分析](/by-pr/8343/8343650.md)

### 启动性能优化

#### JDK-8349400: 消除匿名内部类

> **Issue**: [JDK-8349400](https://bugs.openjdk.org/browse/JDK-8349400)
> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: 类加载 -90%

将枚举匿名类转换为构造函数参数：

**效果**:
- 类加载数量：11 -> 1
- 元空间占用：22KB -> 4KB
- Java Agent 场景显著受益

-> [详细分析](/by-pr/8349/8349400.md)

### 字节码生成优化

#### JDK-8341906: ClassFile 写入合并

> **Issue**: [JDK-8341906](https://bugs.openjdk.org/browse/JDK-8341906)
> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: +28% 字节码写入性能

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

-> [详细分析](/by-pr/8341/8341906.md)

---

## 13. 核心贡献者

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

## 14. 相关链接

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
- [JMH Samples](https://github.com/openjdk/jmh/tree/master/jmh-samples)
- [async-profiler](https://github.com/async-profiler/async-profiler)

### 相关 JEP

| JEP | 标题 | 版本 | 状态 |
|-----|------|------|------|
| [JEP 483](/jeps/tools/jep-483.md) | Ahead-of-Time Class Loading & Linking | JDK 24 | Delivered |
| [JEP 509](/jeps/jfr/jep-509.md) | JFR CPU-Time Profiling | JDK 25 | Delivered |
| [JEP 514](/jeps/performance/jep-514.md) | Ahead-of-Time Command-Line Ergonomics | JDK 25 | Delivered |
| [JEP 515](/jeps/performance/jep-515.md) | Ahead-of-Time Method Analysis | JDK 25 | Delivered |
| [JEP 516](https://openjdk.org/jeps/516) | Ahead-of-Time Object Caching with Any GC | JDK 26 | Delivered |
| [JEP 518](/jeps/jfr/jep-518.md) | JFR Cooperative Sampling | JDK 25 | Delivered |
| [JEP 519](/jeps/gc/jep-519.md) | Compact Object Headers | JDK 25 | Delivered |
| [JEP 520](/jeps/jfr/jep-520.md) | JFR Method Timing & Tracing | JDK 25 | Delivered |
| [JEP 522](/jeps/gc/jep-522.md) | G1 GC: Improve Throughput by Reducing Synchronization | JDK 26 | Delivered |

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
./asprof -d 30 -f profile.html <pid>

# 查看 JIT 编译日志
java -XX:+PrintCompilation -XX:+UnlockDiagnosticVMOptions MyApp
```

---

**最后更新**: 2026-03-22
