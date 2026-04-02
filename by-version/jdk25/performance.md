# JDK 25 性能调优指南

> **版本**: JDK 25 (LTS) | **发布日期**: 2025-09-16

---
## 目录

1. [性能改进总览](#1-性能改进总览)
2. [GC 选择与调优](#2-gc-选择与调优)
3. [Compact Object Headers](#3-compact-object-headers)
4. [AOT 与启动优化](#4-aot-与启动优化)
5. [JFR 性能监控](#5-jfr-性能监控)
6. [虚拟线程性能](#6-虚拟线程性能)
7. [推荐 JVM 配置](#7-推荐-jvm-配置)
8. [相关链接](#8-相关链接)

---


## 1. 性能改进总览

| 领域 | JEP | 改进 | 受益场景 |
|------|-----|------|----------|
| **内存** | JEP 519 | 对象头 12-16 → 8 字节 | 对象密集型应用 |
| **GC** | JEP 468(JDK 21) | 分代 ZGC 默认启用 | 大内存低延迟 |
| **GC** | JEP 521 | 分代 Shenandoah (实验) | 低延迟替代方案 |
| **启动** | JEP 514/515 | AOT 命令行优化 + 方法分析 | 微服务/Serverless |
| **监控** | JEP 520 | JFR 方法级计时 | 性能分析 |
| **并发** | JEP 506 | Scoped Values 正式版 | 虚拟线程场景 |

---

## 2. GC 选择与调优

### 选择决策树

```
应用场景是什么？
├── 低延迟 (<10ms P99)
│   ├── 堆 >8GB → 分代 ZGC (-XX:+UseZGC)
│   └── 堆 <8GB → Shenandoah (-XX:+UseShenandoahGC)
├── 高吞吐量
│   └── G1 GC (-XX:+UseG1GC)  ← 默认
├── 微服务 (小堆 <512MB)
│   └── Serial GC (-XX:+UseSerialGC)
└── 超大堆 (>32GB)
    └── 分代 ZGC (-XX:+UseZGC)
```

### 分代 ZGC 调优

JDK 25 中分代 ZGC 已是默认模式：

```bash
# 基本配置
java -XX:+UseZGC -Xmx16g MyApp

# 调优参数
java -XX:+UseZGC \
     -Xmx16g \
     -XX:SoftMaxHeapSize=12g \        # 软上限，ZGC 尽量不超过
     -XX:ConcGCThreads=4 \            # 并发 GC 线程数
     -Xlog:gc*:gc.log:time,level,tags \
     MyApp
```

### G1 GC 调优

```bash
# G1 高吞吐配置
java -XX:+UseG1GC \
     -Xmx8g \
     -XX:MaxGCPauseMillis=200 \      # 目标暂停时间
     -XX:G1HeapRegionSize=16m \      # Region 大小
     -XX:InitiatingHeapOccupancyPercent=45 \
     MyApp
```

### GC 性能对比 (JDK 25)

| 指标 | G1 | 分代 ZGC | Shenandoah |
|------|-----|----------|------------|
| 吞吐量 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| P99 延迟 | 10-200ms | <1ms | <10ms |
| 内存开销 | 低 | 中 | 中 |
| 适用堆大小 | 1-32GB | 8-16TB | 1-64GB |

---

## 3. Compact Object Headers

### JEP 519 (实验性)

将对象头从 12-16 字节压缩至 8 字节，可显著减少对象密集型应用的内存占用。

**启用方式**:
```bash
java -XX:+UnlockExperimentalVMOptions \
     -XX:+UseCompactObjectHeaders \
     MyApp
```

**内存节省估算**:

| 场景 | 对象数量 | 传统对象头 | 紧凑对象头 | 节省 |
|------|----------|-----------|-----------|------|
| HashMap<String,String> 100万条 | ~400万对象 | ~48MB | ~32MB | ~33% |
| ArrayList<Integer> 100万 | ~100万对象 | ~12MB | ~8MB | ~33% |
| 大量 POJO 对象 | 不定 | 每对象 12-16B 头 | 每对象 8B 头 | 33-50% |

**验证效果**:
```bash
# 使用 JOL 工具查看对象布局
java -XX:+UnlockExperimentalVMOptions -XX:+UseCompactObjectHeaders \
     -jar jol-cli.jar internals java.lang.Object
```

**注意**: 实验性特性，建议先在测试环境验证，确认无兼容性问题后再上生产。

---

## 4. AOT 与启动优化

### JEP 514: AOT 命令行优化

简化了 AOT 缓存的使用流程：

```bash
# 步骤 1: 录制训练数据
java -XX:AOTConfiguration=app.aotconf -jar myapp.jar

# 步骤 2: 生成 AOT 缓存
java -XX:AOTCache=app.aot -XX:AOTConfiguration=app.aotconf -jar myapp.jar

# 步骤 3: 使用缓存启动
java -XX:AOTCache=app.aot -jar myapp.jar
```

### JEP 515: AOT 方法分析

结合方法级 profiling 数据提升 AOT 编译质量：

```bash
# 录制含 profiling 数据的缓存
java -XX:AOTConfiguration=app.aotconf \
     -XX:+AOTMethodProfiling \
     -jar myapp.jar

# 后续启动更快
java -XX:AOTCache=app.aot -jar myapp.jar
```

### AppCDS 快速配置

```bash
# 动态 CDS 归档
java -XX:ArchiveClassesAtExit=app.jsa -jar myapp.jar

# 使用归档启动
java -XX:SharedArchiveFile=app.jsa -jar myapp.jar
```

### 启动时间对比

| 方案 | 冷启动 | 热启动 | 适用场景 |
|------|--------|--------|----------|
| 默认 | 基准 | 基准 | 通用 |
| AppCDS | -20~30% | -10% | 所有应用 |
| AOT Cache | -40~60% | -20% | 微服务 |
| AOT + Profiling | -50~70% | -30% | Serverless |

---

## 5. JFR 性能监控

### JEP 520: JFR Method Timing

低开销的方法级性能追踪：

```bash
# 启用 JFR 方法计时
java -XX:StartFlightRecording=settings=profile,filename=app.jfr \
     -XX:+FlightRecorderMethodSampling \
     MyApp
```

### JFR 常用事件

```bash
# 录制 GC 和线程事件
java -XX:StartFlightRecording=\
name=myrecording,\
settings=default,\
duration=60s,\
filename=recording.jfr \
MyApp

# 分析录制文件
jfr print --events "jdk.GCPhase*" recording.jfr
jfr print --events "jdk.VirtualThreadStart" recording.jfr
```

### 运行时启动/停止

```bash
# 查看进程
jcmd <pid> JFR.check

# 开始录制
jcmd <pid> JFR.start name=perf settings=profile duration=120s

# 导出数据
jcmd <pid> JFR.dump name=perf filename=perf.jfr

# 停止录制
jcmd <pid> JFR.stop name=perf
```

---

## 6. 虚拟线程性能

### Scoped Values vs ThreadLocal

JDK 25 Scoped Values 正式版在虚拟线程场景下性能显著优于 ThreadLocal：

```java
// ❌ 虚拟线程中性能差
static final ThreadLocal<User> CURRENT_USER = new ThreadLocal<>();

// ✅ 虚拟线程中推荐
static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();
```

**性能差异**: Scoped Values 在虚拟线程中无继承开销，绑定/解绑接近零成本。

### 虚拟线程调优

```bash
# 调整虚拟线程调度器并行度（默认 = CPU 核数）
java -Djdk.virtualThreadScheduler.parallelism=8 MyApp

# 监控虚拟线程
jcmd <pid> Thread.dump_to_file -format=json threads.json
```

### 虚拟线程最佳实践

```java
// ✅ I/O 密集型：直接创建虚拟线程
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<Response>> futures = requests.stream()
        .map(req -> executor.submit(() -> httpClient.send(req)))
        .toList();
}

// ⚠️ 避免在虚拟线程中使用 synchronized（pin 到平台线程）
// 使用 ReentrantLock 替代
private final ReentrantLock lock = new ReentrantLock();
```

---

## 7. 推荐 JVM 配置

### Web 应用 (Spring Boot)

```bash
java -XX:+UseZGC \
     -Xmx4g \
     -XX:+UseCompactObjectHeaders \       # 实验性，先测试
     -XX:AOTCache=app.aot \               # AOT 缓存
     -Djdk.virtualThreadScheduler.parallelism=4 \
     -jar myapp.jar
```

### 高吞吐批处理

```bash
java -XX:+UseG1GC \
     -Xmx16g \
     -XX:MaxGCPauseMillis=500 \
     -XX:+UseStringDeduplication \
     -jar batch.jar
```

### 低延迟交易系统

```bash
java -XX:+UseZGC \
     -Xmx32g \
     -XX:SoftMaxHeapSize=24g \
     -XX:ConcGCThreads=4 \
     -XX:+AlwaysPreTouch \
     -jar trading.jar
```

### 微服务 / Serverless

```bash
java -XX:+UseSerialGC \
     -Xmx256m \
     -XX:AOTCache=app.aot \
     -XX:+TieredCompilation \
     -XX:TieredStopAtLevel=1 \
     -jar lambda.jar
```

---

## 8. 相关链接

- [JDK 25 主页](./README.md)
- [分代 ZGC 深度分析](./deep-dive/generational-zgc.md)
- [Compact Object Headers 实现](/deep-dive/jep-519-implementation.md)
- [Scoped Values 实现](/deep-dive/jep-506-implementation.md)
- [GC 调优实战案例](/cases/gc-tuning-case.md)
- [启动优化案例](/cases/startup-optimization.md)
- [GC 演进时间线](/by-topic/core/gc/timeline.md)

---

[← 返回 JDK 25](../README.md)
