# JFR (Java Flight Recorder) 实战指南

> Java Flight Recorder 是 JDK 内置的低开销生产级性能诊断工具，是每个 Java 开发者的必备技能。

---
## 目录

1. [什么是 JFR](#1-什么是-jfr)
2. [启动方式](#2-启动方式)
3. [常用事件类型](#3-常用事件类型)
4. [JFR 配置](#4-jfr-配置)
5. [JMC (Java Mission Control)](#5-jmc-java-mission-control)
6. [JFR Streaming API (JDK 14+)](#6-jfr-streaming-api-jdk-14)
7. [JDK 25 新特性](#7-jdk-25-新特性)
8. [实际案例](#8-实际案例)
9. [jfr 命令行工具](#9-jfr-命令行工具)
10. [自定义事件](#10-自定义事件)
11. [最佳实践](#11-最佳实践)
12. [相关资源](#12-相关资源)

---

## 1. 什么是 JFR

JFR (Java Flight Recorder) 是 JDK 内置的诊断和性能分析框架。它通过在 JVM 和 JDK 库中埋点 (instrumentation)，持续收集运行时事件数据，并以极低的开销写入高效的二进制格式。

### 核心特点

| 特点 | 说明 |
|------|------|
| **低开销 (Low Overhead)** | 生产环境开销通常 < 2%，default 配置下 < 1% |
| **Always-On 能力** | 可在生产环境 7x24 持续运行，不影响业务 |
| **内置于 JDK** | JDK 11+ 完全开源内置 (之前是 Oracle 商业特性)，无需额外 agent 或依赖 |
| **丰富的事件模型** | 数百种内置事件，覆盖 CPU、内存、GC、IO、线程、类加载等 |
| **环形缓冲区 (Circular Buffer)** | 支持持续录制，旧数据自动覆盖，控制磁盘占用 |
| **事件流 (Event Streaming)** | JDK 14+ 支持实时消费事件，无需落盘 |

### JFR 与其他工具的对比

| 工具 | 开销 | 侵入性 | 生产环境 | 事件丰富度 |
|------|------|--------|---------|-----------|
| JFR | < 2% | 无需 agent | 适合 | 非常丰富 (数百种) |
| async-profiler | < 5% | 需 native agent | 需评估 | CPU/Alloc/Lock |
| VisualVM | 5-20% | JVMTI agent | 不推荐 | 中等 |
| JMX + MBeans | < 1% | 内置 | 适合 | 仅指标级别 |
| BPF/perf | < 1% | 内核级 | 适合 | 系统级，不含 Java 语义 |

### JFR 架构简述

```
┌─────────────────────────────────────────────┐
│                  JVM 进程                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ 应用线程  │  │ GC 线程   │  │ JIT 线程  │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       │ emit         │ emit        │ emit    │
│  ┌────▼──────────────▼─────────────▼─────┐  │
│  │        Thread-Local Buffers            │  │
│  └────────────────┬──────────────────────┘  │
│                   │ flush                    │
│  ┌────────────────▼──────────────────────┐  │
│  │        Global Ring Buffer              │  │
│  └────────────────┬──────────────────────┘  │
│                   │ dump                     │
│  ┌────────────────▼──────────────────────┐  │
│  │          .jfr 文件 / Stream             │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

每个线程有自己的本地缓冲区 (thread-local buffer)，事件写入是无锁操作，这就是低开销的关键。

---

## 2. 启动方式

JFR 提供三种启动方式：JVM 启动参数、jcmd 动态控制、以及 Java API。

### 2.1 命令行启动 (-XX:StartFlightRecording)

在 JVM 启动时通过参数启用 JFR：

```bash
# 基本录制：录制 60 秒，写入文件
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr \
     -jar myapp.jar

# 使用 profile 配置（更详细的事件采集）
java -XX:StartFlightRecording=duration=120s,filename=profile.jfr,settings=profile \
     -jar myapp.jar

# 持续录制 (continuous recording)：限制最大 500MB，循环覆盖
java -XX:StartFlightRecording=disk=true,maxsize=500m,maxage=1h,name=continuous \
     -jar myapp.jar

# 多个录制同时运行
java -XX:StartFlightRecording=name=default_rec,settings=default \
     -XX:StartFlightRecording=name=profile_rec,settings=profile,duration=300s,filename=deep.jfr \
     -jar myapp.jar

# 延迟启动：JVM 启动 30 秒后开始录制
java -XX:StartFlightRecording=delay=30s,duration=60s,filename=delayed.jfr \
     -jar myapp.jar
```

常用参数一览：

| 参数 | 说明 | 示例 |
|------|------|------|
| `name` | 录制名称 | `name=my_recording` |
| `settings` | 配置文件 | `settings=profile` |
| `duration` | 录制时长 | `duration=60s` |
| `filename` | 输出文件 | `filename=/tmp/rec.jfr` |
| `maxsize` | 最大文件大小 | `maxsize=500m` |
| `maxage` | 最大保留时间 | `maxage=1h` |
| `delay` | 延迟启动 | `delay=30s` |
| `disk` | 是否写盘 | `disk=true` |
| `dumponexit` | 退出时 dump | `dumponexit=true` |

### 2.2 jcmd 动态控制

jcmd 是最灵活的方式，可以在运行中的 JVM 上随时启停录制：

```bash
# 查看进程列表
jcmd -l

# 启动录制
jcmd <pid> JFR.start name=profiling settings=profile duration=120s

# 查看当前录制列表
jcmd <pid> JFR.check

# 手动 dump 当前数据（不停止录制）
jcmd <pid> JFR.dump name=profiling filename=/tmp/snapshot.jfr

# 停止录制并保存
jcmd <pid> JFR.stop name=profiling filename=/tmp/final.jfr

# dump 指定时间范围的数据
jcmd <pid> JFR.dump begin=2025-01-15T10:00:00 end=2025-01-15T10:05:00 \
     filename=/tmp/range.jfr

# 只 dump 最近 60 秒的数据
jcmd <pid> JFR.dump maxage=60s filename=/tmp/last_minute.jfr

# 启动持续录制（无 duration 则一直运行）
jcmd <pid> JFR.start name=monitor settings=default maxsize=200m

# 查看 JFR 配置元信息
jcmd <pid> JFR.configure
```

**典型工作流：在生产环境发现问题后临时抓取数据**

```bash
# 1. 发现服务响应变慢，启动 profile 级别录制
jcmd $(pgrep -f myapp) JFR.start name=issue_123 settings=profile

# 2. 等待复现（比如 2 分钟）
sleep 120

# 3. dump 并停止
jcmd $(pgrep -f myapp) JFR.stop name=issue_123 filename=/tmp/issue_123.jfr

# 4. 下载分析
scp prod-server:/tmp/issue_123.jfr .
```

### 2.3 Java API (jdk.jfr)

通过代码精确控制录制：

```java
import jdk.jfr.Configuration;
import jdk.jfr.Recording;
import java.nio.file.Path;

// 使用预设配置启动录制
Configuration config = Configuration.getConfiguration("profile");
try (Recording recording = new Recording(config)) {
    recording.setMaxSize(100 * 1024 * 1024);  // 100MB 上限
    recording.setMaxAge(java.time.Duration.ofMinutes(5));
    recording.setDestination(Path.of("/tmp/api_recording.jfr"));

    recording.start();

    // ... 执行需要分析的业务逻辑 ...
    runBusinessLogic();

    recording.stop();
    // 录制自动写入 destination
}

// 或者手动 dump 到指定位置
try (Recording recording = new Recording()) {
    recording.enable("jdk.ExecutionSample").withPeriod(java.time.Duration.ofMillis(10));
    recording.enable("jdk.ObjectAllocationSample").withThreshold(java.time.Duration.ZERO);
    recording.start();

    runBusinessLogic();

    recording.dump(Path.of("/tmp/manual_dump.jfr"));
    recording.stop();
}
```

**精细控制单个事件的启用/禁用：**

```java
try (Recording recording = new Recording()) {
    // 启用 CPU 采样，每 10ms 采一次
    recording.enable("jdk.ExecutionSample")
             .withPeriod(java.time.Duration.ofMillis(10));

    // 启用对象分配采样，无阈值（记录所有分配）
    recording.enable("jdk.ObjectAllocationSample")
             .withThreshold(java.time.Duration.ZERO);

    // 启用文件 IO 事件，只记录超过 1ms 的
    recording.enable("jdk.FileRead")
             .withThreshold(java.time.Duration.ofMillis(1));
    recording.enable("jdk.FileWrite")
             .withThreshold(java.time.Duration.ofMillis(1));

    // 禁用不需要的事件
    recording.disable("jdk.ClassLoad");

    recording.start();
    // ...
}
```

---

## 3. 常用事件类型

JFR 内置数百种事件，以下是实际排障中最常用的分类。

### 3.1 CPU Profiling

| 事件 | 说明 | 类型 |
|------|------|------|
| `jdk.ExecutionSample` | 线程执行采样 (wall-clock)，定期记录线程栈 | 周期性 |
| `jdk.NativeMethodSample` | Native 方法执行采样 | 周期性 |
| `jdk.CPUTimeSample` | CPU 时间采样 (JDK 25+, JEP 509) | 周期性 |
| `jdk.MethodTiming` | 方法耗时统计 (JDK 25+, JEP 520) | 即时 |
| `jdk.ThreadCPULoad` | 每线程 CPU 负载 | 周期性 |
| `jdk.CPULoad` | 系统/进程 CPU 负载 | 周期性 |

`jdk.ExecutionSample` 是最常用的 CPU profiling 事件。它在 default 配置下每 20ms 采样一次，profile 配置下每 10ms 采样。

### 3.2 GC (垃圾收集)

| 事件 | 说明 |
|------|------|
| `jdk.GarbageCollection` | GC 事件总览 (包含 cause, 耗时) |
| `jdk.GCPhasePause` | GC 暂停阶段 (STW 阶段详情) |
| `jdk.YoungGarbageCollection` | Young GC |
| `jdk.OldGarbageCollection` | Old GC / Full GC |
| `jdk.GCHeapSummary` | GC 前后堆内存摘要 |
| `jdk.GCHeapConfiguration` | 堆配置 (Xmx, Xms 等) |
| `jdk.GCReferenceStatistics` | 引用处理统计 (SoftRef, WeakRef 等) |
| `jdk.ZAllocationStall` | ZGC 分配停顿 |
| `jdk.G1GarbageCollection` | G1 专属事件 |

### 3.3 内存分配 (Memory Allocation)

| 事件 | 说明 |
|------|------|
| `jdk.ObjectAllocationSample` | 对象分配采样 (JDK 16+, 轻量级) |
| `jdk.ObjectAllocationInNewTLAB` | 触发新 TLAB 分配的对象 |
| `jdk.ObjectAllocationOutsideTLAB` | TLAB 外分配（大对象） |
| `jdk.OldObjectSample` | 老年代对象采样 (用于泄漏检测) |
| `jdk.ThreadAllocationStatistics` | 每线程累计分配字节数 |

**注意**: `jdk.ObjectAllocationSample` (JDK 16+) 替代了之前基于 TLAB 的分配事件，开销更低。

### 3.4 IO (文件与网络)

| 事件 | 说明 |
|------|------|
| `jdk.FileRead` | 文件读取 (包含文件路径、读取字节数、耗时) |
| `jdk.FileWrite` | 文件写入 |
| `jdk.FileForce` | 文件 fsync |
| `jdk.SocketRead` | Socket 读取 (包含远端地址、字节数、耗时) |
| `jdk.SocketWrite` | Socket 写入 |

IO 事件默认有阈值 (threshold)。在 default 配置下，只记录超过 20ms 的 IO 操作；profile 配置下阈值为 10ms。

### 3.5 线程 (Thread)

| 事件 | 说明 |
|------|------|
| `jdk.ThreadPark` | 线程 park (LockSupport.park) |
| `jdk.ThreadSleep` | Thread.sleep |
| `jdk.JavaMonitorWait` | Object.wait() |
| `jdk.JavaMonitorEnter` | synchronized 锁竞争 |
| `jdk.ThreadStart` / `jdk.ThreadEnd` | 线程创建/销毁 |
| `jdk.VirtualThreadStart` / `jdk.VirtualThreadEnd` | 虚拟线程生命周期 (JDK 21+) |
| `jdk.VirtualThreadPinned` | 虚拟线程被 pin 住 (JDK 21+) |
| `jdk.VirtualThreadSubmitFailed` | 虚拟线程提交失败 (JDK 21+) |

`jdk.VirtualThreadPinned` 在调试虚拟线程时非常重要——当虚拟线程在 synchronized 块或 native 调用中阻塞时，它会被 pin 到载体线程 (carrier thread)，此事件可以帮助识别这些位置。

### 3.6 JIT 编译与类加载

| 事件 | 说明 |
|------|------|
| `jdk.Compilation` | JIT 编译事件 |
| `jdk.CompilerFailure` | 编译失败 |
| `jdk.Deoptimization` | 去优化 |
| `jdk.ClassLoad` | 类加载 |
| `jdk.ClassDefine` | 类定义 |

---

## 4. JFR 配置

### 4.1 default.jfc vs profile.jfc

JDK 内置两个 `.jfc` 配置文件，位于 `$JAVA_HOME/lib/jfr/`：

| 配置 | 文件 | 开销 | 适用场景 |
|------|------|------|---------|
| `default` | `default.jfc` | < 1% | 生产环境持续监控 |
| `profile` | `profile.jfc` | 1-2% | 性能分析、排障 |

两者的主要差异：

| 事件/参数 | default | profile |
|----------|---------|---------|
| `jdk.ExecutionSample` 周期 | 20ms | 10ms |
| `jdk.ObjectAllocationSample` 阈值 | 512B | 256B |
| `jdk.FileRead` 阈值 | 20ms | 10ms |
| `jdk.SocketRead` 阈值 | 20ms | 10ms |
| `jdk.JavaMonitorEnter` 阈值 | 20ms | 10ms |
| `jdk.ThreadPark` 阈值 | 20ms | 10ms |
| `jdk.OldObjectSample` | 禁用 | 启用 (cutoff=0) |

### 4.2 自定义 .jfc 配置

可以基于内置配置修改，创建自定义 `.jfc` 文件 (XML 格式)：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration version="2.0" label="My Custom Config"
               description="针对延迟敏感应用的自定义配置">

  <!-- 启用 CPU 采样，每 5ms 采一次 -->
  <event name="jdk.ExecutionSample">
    <setting name="enabled">true</setting>
    <setting name="period">5 ms</setting>
  </event>

  <!-- 启用所有 IO 事件，阈值降到 1ms -->
  <event name="jdk.FileRead">
    <setting name="enabled">true</setting>
    <setting name="threshold">1 ms</setting>
    <setting name="stackTrace">true</setting>
  </event>
  <event name="jdk.FileWrite">
    <setting name="enabled">true</setting>
    <setting name="threshold">1 ms</setting>
    <setting name="stackTrace">true</setting>
  </event>
  <event name="jdk.SocketRead">
    <setting name="enabled">true</setting>
    <setting name="threshold">1 ms</setting>
    <setting name="stackTrace">true</setting>
  </event>
  <event name="jdk.SocketWrite">
    <setting name="enabled">true</setting>
    <setting name="threshold">1 ms</setting>
    <setting name="stackTrace">true</setting>
  </event>

  <!-- 启用对象分配采样，无阈值 -->
  <event name="jdk.ObjectAllocationSample">
    <setting name="enabled">true</setting>
    <setting name="throttle">300/s</setting>
  </event>

  <!-- 启用 GC 事件 -->
  <event name="jdk.GCPhasePause">
    <setting name="enabled">true</setting>
    <setting name="threshold">0 ms</setting>
  </event>

  <!-- 启用虚拟线程 pin 检测 -->
  <event name="jdk.VirtualThreadPinned">
    <setting name="enabled">true</setting>
    <setting name="threshold">20 ms</setting>
    <setting name="stackTrace">true</setting>
  </event>

  <!-- 启用老年代对象采样，用于泄漏检测 -->
  <event name="jdk.OldObjectSample">
    <setting name="enabled">true</setting>
    <setting name="stackTrace">true</setting>
    <setting name="cutoff">0</setting>
  </event>

</configuration>
```

使用自定义配置：

```bash
# 命令行
java -XX:StartFlightRecording=settings=/path/to/custom.jfc -jar myapp.jar

# jcmd
jcmd <pid> JFR.start settings=/path/to/custom.jfc
```

### 4.3 事件阈值 (Threshold) 调优

阈值是性能开销与数据量的关键平衡点：

```bash
# 查看所有事件及其当前设置
jcmd <pid> JFR.check verbose=true

# 通过 jcmd 动态调整阈值 (结合 .jfc 配置)
# 注意：jcmd 不能单独修改某个事件阈值，需要通过完整 settings 指定
```

**阈值选择建议：**

| 场景 | IO 阈值 | 锁阈值 | 采样周期 |
|------|---------|--------|---------|
| 生产环境长期监控 | 20ms | 20ms | 20ms |
| 性能分析 | 10ms | 10ms | 10ms |
| 延迟问题排查 | 1ms | 1ms | 5ms |
| 深度诊断 (短时间) | 0ms | 0ms | 1ms |

---

## 5. JMC (Java Mission Control)

JMC 是 JFR 数据的官方图形化分析工具，能可视化展示录制数据。

### 5.1 安装与连接

```bash
# JMC 需要单独下载 (不再内置于 JDK)
# 下载地址: https://www.oracle.com/java/technologies/jdk-mission-control.html
# 或使用 Adoptium 构建: https://adoptium.net/jmc/

# 打开 .jfr 文件
jmc -open recording.jfr

# 远程连接运行中的 JVM (通过 JMX)
# 目标 JVM 需添加:
# -Dcom.sun.management.jmxremote.port=7091
# -Dcom.sun.management.jmxremote.authenticate=false
# -Dcom.sun.management.jmxremote.ssl=false
```

### 5.2 关键视图

JMC 打开 .jfr 文件后提供以下关键分析视图：

**Automated Analysis (自动分析)**
- 自动检测潜在问题，评分 0-100
- 包括：GC 暂停评估、锁竞争检测、IO 瓶颈、代码热点

**Java Application (应用程序)**
- **火焰图 (Flame Graph)**: 可视化 CPU 热点调用栈，最直观的性能分析视图
- **方法分析 (Method Profiling)**: 按方法统计 CPU 采样命中数
- **热点方法列表**: 按采样频率排序

**Memory (内存)**
- 堆使用趋势图
- GC 暂停时间分布
- 对象分配热点 (哪些代码路径分配最多)
- 老年代对象引用链 (用于泄漏分析)

**I/O (输入输出)**
- 文件 IO 统计：按文件路径聚合读写次数和耗时
- 网络 IO 统计：按远端地址聚合
- IO 操作的调用栈分析

**Threads (线程)**
- 线程生命周期视图
- 锁竞争分析
- 线程状态时间分布 (Running / Sleeping / Waiting / Blocked)

---

## 6. JFR Streaming API (JDK 14+)

JDK 14 引入了 JFR Event Streaming (JEP 349)，允许应用程序实时消费 JFR 事件，无需先写入文件再分析。

### 6.1 基本用法：RecordingStream

```java
import jdk.jfr.consumer.RecordingStream;
import java.time.Duration;

// 创建实时事件流
try (var stream = new RecordingStream()) {
    // 启用并配置事件
    stream.enable("jdk.CPULoad").withPeriod(Duration.ofSeconds(1));
    stream.enable("jdk.GCPhasePause").withThreshold(Duration.ZERO);
    stream.enable("jdk.JavaMonitorEnter").withThreshold(Duration.ofMillis(10));

    // 注册事件处理器 (handler)
    stream.onEvent("jdk.CPULoad", event -> {
        double jvmUser = event.getFloat("jvmUser");
        double jvmSystem = event.getFloat("jvmSystem");
        double machineTotal = event.getFloat("machineTotal");
        System.out.printf("CPU - JVM User: %.1f%%, System: %.1f%%, Machine: %.1f%%%n",
                          jvmUser * 100, jvmSystem * 100, machineTotal * 100);
    });

    stream.onEvent("jdk.GCPhasePause", event -> {
        long durationMs = event.getDuration().toMillis();
        String name = event.getString("name");
        if (durationMs > 50) {
            System.out.printf("⚠ GC Pause: %s took %d ms%n", name, durationMs);
        }
    });

    stream.onEvent("jdk.JavaMonitorEnter", event -> {
        long durationMs = event.getDuration().toMillis();
        String monitorClass = event.getClass("monitorClass").getName();
        System.out.printf("Lock contention on %s: %d ms%n", monitorClass, durationMs);
    });

    // 启动流 (阻塞当前线程)
    stream.start();
}
```

### 6.2 非阻塞启动

```java
try (var stream = new RecordingStream()) {
    stream.enable("jdk.CPULoad").withPeriod(Duration.ofSeconds(1));

    stream.onEvent("jdk.CPULoad", event -> {
        // 处理事件
    });

    // 在后台线程启动流，不阻塞当前线程
    stream.startAsync();

    // 主线程继续做其他事情
    runApplication();
}
// try-with-resources 关闭时自动停止流
```

### 6.3 实时监控告警

```java
import jdk.jfr.consumer.RecordingStream;
import java.time.Duration;
import java.util.concurrent.atomic.AtomicLong;

public class JfrMonitor {
    private static final AtomicLong gcPauseCount = new AtomicLong();
    private static final long GC_PAUSE_THRESHOLD_MS = 200;
    private static final double CPU_ALERT_THRESHOLD = 0.8;

    public static void startMonitoring() {
        var stream = new RecordingStream();

        stream.enable("jdk.CPULoad").withPeriod(Duration.ofSeconds(5));
        stream.enable("jdk.GCPhasePause").withThreshold(Duration.ZERO);
        stream.enable("jdk.ObjectAllocationSample");
        stream.enable("jdk.VirtualThreadPinned").withThreshold(Duration.ofMillis(20));

        // CPU 告警
        stream.onEvent("jdk.CPULoad", event -> {
            double machineTotal = event.getFloat("machineTotal");
            if (machineTotal > CPU_ALERT_THRESHOLD) {
                alert("CPU usage high: " + (int)(machineTotal * 100) + "%");
            }
        });

        // GC 暂停告警
        stream.onEvent("jdk.GCPhasePause", event -> {
            long pauseMs = event.getDuration().toMillis();
            if (pauseMs > GC_PAUSE_THRESHOLD_MS) {
                gcPauseCount.incrementAndGet();
                alert("Long GC pause: " + pauseMs + "ms, cause: " + event.getString("name"));
            }
        });

        // 虚拟线程 pinning 告警
        stream.onEvent("jdk.VirtualThreadPinned", event -> {
            long durationMs = event.getDuration().toMillis();
            alert("Virtual thread pinned for " + durationMs + "ms at: "
                  + event.getStackTrace());
        });

        stream.startAsync();
    }

    private static void alert(String message) {
        // 发送到监控系统 (Prometheus, Grafana, 钉钉/Slack 等)
        System.err.println("[JFR ALERT] " + message);
    }
}
```

### 6.4 读取外部 JFR 文件

```java
import jdk.jfr.consumer.RecordingFile;
import java.nio.file.Path;

// 读取并分析已有的 .jfr 文件
try (var recordingFile = new RecordingFile(Path.of("recording.jfr"))) {
    while (recordingFile.hasMoreEvents()) {
        var event = recordingFile.readEvent();

        if (event.getEventType().getName().equals("jdk.ExecutionSample")) {
            var stackTrace = event.getStackTrace();
            if (stackTrace != null) {
                var topFrame = stackTrace.getFrames().getFirst();
                System.out.println("Hot method: "
                    + topFrame.getMethod().getType().getName()
                    + "." + topFrame.getMethod().getName());
            }
        }
    }
}
```

---

## 7. JDK 25 新特性

### 7.1 JEP 509: JFR CPU-Time Profiling

传统的 `jdk.ExecutionSample` 是 wall-clock 采样——它按固定时间间隔采样所有线程，不区分线程是否真正在 CPU 上执行。这意味着等待 IO、sleep、park 的线程也会被采样到。

JDK 25 的 `jdk.CPUTimeSample` 只在线程真正消耗 CPU 时间时采样，能更准确地反映 CPU 热点。

```bash
# 启用 CPU 时间采样
jcmd <pid> JFR.start settings=profile

# 或通过命令行
java -XX:StartFlightRecording=settings=profile -jar myapp.jar
```

**Wall-Clock vs CPU-Time 对比：**

| 对比维度 | `jdk.ExecutionSample` | `jdk.CPUTimeSample` |
|---------|----------------------|---------------------|
| 采样方式 | 按时钟时间采样 | 按 CPU 时间采样 |
| 采样对象 | 所有线程 (含等待中的) | 仅消耗 CPU 的线程 |
| 适用场景 | 延迟分析 (线程在做什么) | CPU 热点分析 (CPU 花在哪) |
| 能否发现 IO 等待 | 能 | 不能 |
| 能否精确反映 CPU 热点 | 不精确 (含等待噪音) | 精确 |

```java
// 通过 API 启用
try (var recording = new Recording()) {
    recording.enable("jdk.CPUTimeSample")
             .withPeriod(Duration.ofMillis(10));
    recording.start();
    // ...
}
```

### 7.2 JEP 520: Method Timing

JEP 520 允许对指定方法进行耗时统计，不需要修改应用代码：

```bash
# 通过 .jfc 配置指定要监控的方法
# 在 .jfc 文件中:
```

```xml
<event name="jdk.MethodTiming">
  <setting name="enabled">true</setting>
  <setting name="filter">com.myapp.service.OrderService#processOrder</setting>
  <setting name="period">endChunk</setting>
</event>
```

`jdk.MethodTiming` 事件报告指定方法的调用次数和累计耗时，无需在代码中手动埋点，是生产环境方法级性能监控的利器。

---

## 8. 实际案例

### 8.1 排查内存泄漏 (Memory Leak)

**症状**: 应用运行数小时后 OOM，堆内存持续增长。

**Step 1: 启动包含老年代采样的录制**

```bash
# 启用 OldObjectSample 事件（关键！它追踪老年代中长期存活的对象）
jcmd <pid> JFR.start name=leak settings=profile
```

或使用自定义配置确保 `jdk.OldObjectSample` 启用：

```xml
<event name="jdk.OldObjectSample">
  <setting name="enabled">true</setting>
  <setting name="stackTrace">true</setting>
  <setting name="cutoff">0</setting>  <!-- 0 表示记录完整引用链 -->
</event>
```

**Step 2: 等待内存增长后 dump**

```bash
# 等待一段时间，让内存增长
jcmd <pid> JFR.dump name=leak filename=/tmp/leak_analysis.jfr
```

**Step 3: 用 JMC 分析**

在 JMC 中打开 `leak_analysis.jfr`，进入 Memory 视图：

- 查看 **Old Object Sample**：它显示老年代中长期存活对象的分配栈和引用链
- 查看 **GC Heap Summary** 趋势：确认堆内存是否持续增长
- 查看 **Object Allocation** 热点：找到分配最频繁的代码路径

**Step 4: 用代码分析 OldObjectSample**

```java
try (var file = new RecordingFile(Path.of("/tmp/leak_analysis.jfr"))) {
    while (file.hasMoreEvents()) {
        var event = file.readEvent();
        if (event.getEventType().getName().equals("jdk.OldObjectSample")) {
            System.out.println("Type: " + event.getClass("objectClass").getName());
            System.out.println("Alloc Size: " + event.getLong("objectSize"));
            System.out.println("Alloc Time: " + event.getStartTime());
            var stack = event.getStackTrace();
            if (stack != null) {
                stack.getFrames().stream().limit(5).forEach(frame ->
                    System.out.println("  at " + frame.getMethod().getType().getName()
                                       + "." + frame.getMethod().getName())
                );
            }
            System.out.println("---");
        }
    }
}
```

### 8.2 排查延迟毛刺 (Latency Spike)

**症状**: P99 延迟偶尔飙升到秒级，正常情况下 P99 < 50ms。

**Step 1: 启动低阈值录制**

```bash
jcmd <pid> JFR.start name=latency settings=profile
```

同时用自定义配置降低 IO 和锁的阈值：

```xml
<!-- 降低 IO 阈值到 1ms -->
<event name="jdk.FileRead">
  <setting name="threshold">1 ms</setting>
</event>
<event name="jdk.SocketRead">
  <setting name="threshold">1 ms</setting>
</event>

<!-- 降低锁阈值 -->
<event name="jdk.JavaMonitorEnter">
  <setting name="threshold">1 ms</setting>
</event>
<event name="jdk.ThreadPark">
  <setting name="threshold">1 ms</setting>
</event>

<!-- 启用 GC 暂停检测 -->
<event name="jdk.GCPhasePause">
  <setting name="threshold">0 ms</setting>
</event>
```

**Step 2: 分析可能的原因**

延迟毛刺常见原因及对应 JFR 事件：

| 可能原因 | 关键事件 | 排查方法 |
|---------|---------|---------|
| GC 暂停 | `jdk.GCPhasePause` | 检查暂停时间是否与延迟毛刺时间吻合 |
| 锁竞争 | `jdk.JavaMonitorEnter` | 检查长时间的锁等待 |
| IO 阻塞 | `jdk.FileRead`, `jdk.SocketRead` | 检查异常慢的 IO 操作 |
| JIT 编译 | `jdk.Compilation` | 检查是否有大型编译导致暂停 |
| 线程饥饿 | `jdk.ThreadPark`, `jdk.ExecutionSample` | 检查线程等待模式 |

**Step 3: 用代码自动检测**

```java
try (var file = new RecordingFile(Path.of("/tmp/latency.jfr"))) {
    while (file.hasMoreEvents()) {
        var event = file.readEvent();
        long durationMs = event.getDuration().toMillis();
        String eventName = event.getEventType().getName();

        // 找出所有超过 100ms 的事件
        if (durationMs > 100) {
            System.out.printf("[%s] %s: %d ms%n",
                event.getStartTime(), eventName, durationMs);
            if (event.getStackTrace() != null) {
                event.getStackTrace().getFrames().stream().limit(3).forEach(f ->
                    System.out.println("    at " + f.getMethod().getType().getName()
                                       + "." + f.getMethod().getName()));
            }
        }
    }
}
```

### 8.3 排查 CPU 热点 (CPU Hotspot)

**症状**: 应用 CPU 使用率持续 80%+，需要找到消耗 CPU 最多的代码。

**Step 1: 启动 CPU profiling 录制**

```bash
# 使用 profile 配置，10ms 采样间隔
jcmd <pid> JFR.start name=cpu settings=profile duration=120s filename=/tmp/cpu.jfr
```

**Step 2: 用 JMC 查看火焰图**

在 JMC 中打开文件，进入 Java Application > Method Profiling，切换到火焰图视图，即可看到 CPU 时间的分布。

**Step 3: 用 jfr 命令行快速定位热点方法**

```bash
# 打印 ExecutionSample 事件的栈顶方法
jfr print --events jdk.ExecutionSample --stack-depth 5 /tmp/cpu.jfr | \
    grep "at " | sort | uniq -c | sort -rn | head -20
```

**Step 4: JDK 25+ 使用 CPU-Time Profiling**

```bash
# JDK 25+：使用 CPUTimeSample 获得更精确的 CPU 热点
java -XX:StartFlightRecording=settings=profile -jar myapp.jar
```

在 JMC 中使用 `jdk.CPUTimeSample` 事件查看火焰图，排除了 IO 等待的噪音，结果更精确。

---

## 9. jfr 命令行工具

JDK 内置 `jfr` 命令行工具，可以在不安装 JMC 的情况下快速分析 `.jfr` 文件。

### 9.1 jfr print

```bash
# 打印所有事件
jfr print recording.jfr

# 只打印指定事件类型
jfr print --events jdk.GCPhasePause recording.jfr

# 多个事件类型
jfr print --events jdk.GCPhasePause,jdk.GarbageCollection recording.jfr

# 按事件名称模式匹配 (通配符)
jfr print --events 'jdk.GC*' recording.jfr

# 限制栈深度
jfr print --stack-depth 10 --events jdk.ExecutionSample recording.jfr

# 输出为 JSON 格式 (方便程序处理)
jfr print --json --events jdk.CPULoad recording.jfr

# 输出为 XML 格式
jfr print --xml --events jdk.GCPhasePause recording.jfr

# 按时间范围过滤 (JDK 19+)
jfr print --events jdk.ExecutionSample \
          --start 2025-01-15T10:00:00 \
          --end 2025-01-15T10:05:00 \
          recording.jfr
```

### 9.2 jfr summary

```bash
# 查看录制摘要：事件统计、时间范围、JVM 信息
jfr summary recording.jfr
```

输出示例：

```
 Version: 2.1
 Chunks: 1
 Start: 2025-01-15 10:00:00 (UTC)

 Event Type                            Count  Size (bytes)
======================================================================
 jdk.ExecutionSample                  12345        456789
 jdk.ObjectAllocationSample            8901        234567
 jdk.GCPhasePause                        42          3150
 jdk.CPULoad                            120          4800
 jdk.ThreadPark                        5678        198730
 ...
```

### 9.3 jfr metadata

```bash
# 查看录制中包含的所有事件类型及其字段定义
jfr metadata recording.jfr
```

### 9.4 jfr view (JDK 21+)

JDK 21 引入了 `jfr view` 命令，提供预定义的分析视图：

```bash
# 查看可用的视图列表
jfr view --list recording.jfr

# 查看 GC 暂停视图
jfr view gc-pauses recording.jfr

# 查看热点方法
jfr view hot-methods recording.jfr

# 查看内存分配热点
jfr view allocation-by-site recording.jfr

# 查看最长的 IO 操作
jfr view longest-io recording.jfr

# 查看线程 CPU 负载
jfr view thread-cpu-load recording.jfr

# 查看锁竞争
jfr view contention-by-site recording.jfr

# 查看异常统计
jfr view exception-count recording.jfr
```

### 9.5 jfr configure (JDK 20+)

```bash
# 基于已有配置创建自定义 .jfc
jfr configure --input default \
              --output custom.jfc \
              jdk.ExecutionSample#period=5ms \
              jdk.FileRead#threshold=1ms
```

---

## 10. 自定义事件

JFR 允许应用程序定义自己的事件类型，将业务指标纳入 JFR 统一分析。

### 10.1 定义自定义事件

```java
import jdk.jfr.*;

@Name("com.myapp.OrderProcessed")
@Label("Order Processed")
@Description("订单处理完成事件")
@Category({"My Application", "Orders"})
@StackTrace(false)  // 不需要栈追踪，减少开销
public class OrderProcessedEvent extends Event {

    @Label("Order ID")
    public String orderId;

    @Label("Customer ID")
    public String customerId;

    @Label("Amount")
    @DataAmount(DataAmount.BYTES)  // 可选：标注数据语义
    public long amount;

    @Label("Item Count")
    public int itemCount;

    @Label("Processing Time (ms)")
    @Timespan(Timespan.MILLISECONDS)
    public long processingTimeMs;
}
```

### 10.2 使用自定义事件

```java
public class OrderService {
    public void processOrder(Order order) {
        var event = new OrderProcessedEvent();
        event.begin();  // 记录开始时间

        try {
            // 业务逻辑
            validateOrder(order);
            chargePayment(order);
            updateInventory(order);

            event.orderId = order.getId();
            event.customerId = order.getCustomerId();
            event.amount = order.getTotalAmount();
            event.itemCount = order.getItems().size();
        } finally {
            event.end();  // 记录结束时间
            event.processingTimeMs = event.getDuration().toMillis();
            event.commit();  // 提交事件到 JFR
        }
    }
}
```

### 10.3 通过 Streaming API 实时消费自定义事件

```java
try (var stream = new RecordingStream()) {
    stream.enable("com.myapp.OrderProcessed");

    stream.onEvent("com.myapp.OrderProcessed", event -> {
        String orderId = event.getString("orderId");
        long processingTimeMs = event.getLong("processingTimeMs");
        if (processingTimeMs > 1000) {
            System.out.printf("Slow order: %s took %d ms%n", orderId, processingTimeMs);
        }
    });

    stream.startAsync();
}
```

---

## 11. 最佳实践

### 生产环境建议

1. **始终开启 default 录制**: 开销 < 1%，出问题时有数据可查
2. **使用环形缓冲区**: 设置 `maxsize` 和 `maxage`，避免磁盘占满
3. **按需升级到 profile**: 只在排障时临时切换到 profile 配置
4. **JDK 14+ 用 Streaming**: 将 JFR 事件接入监控系统，替代部分自定义指标

```bash
# 生产环境推荐启动参数
java -XX:StartFlightRecording=disk=true,maxsize=500m,maxage=6h,name=prod,settings=default,dumponexit=true,filename=/var/log/jfr/dump_on_exit.jfr \
     -jar myapp.jar
```

### 性能分析建议

1. **先 summary 再 detail**: 用 `jfr summary` 和 `jfr view` 快速定位方向
2. **Wall-Clock + CPU-Time 结合**: 同时使用两种采样，分别定位延迟和 CPU 热点
3. **对比分析**: 录制正常状态和异常状态的数据，在 JMC 中对比
4. **关注 GC**: 很多性能问题的根因是 GC，优先检查 `jdk.GCPhasePause`

### 虚拟线程调试建议 (JDK 21+)

```bash
# 检测 virtual thread pinning
jfr print --events jdk.VirtualThreadPinned recording.jfr
```

pinning 的常见原因：
- `synchronized` 块中执行阻塞操作 → 改用 `ReentrantLock`
- native 方法中阻塞 → 考虑异步替代

---

## 12. 相关资源

- [JDK Mission Control 下载](https://www.oracle.com/java/technologies/jdk-mission-control.html)
- [JFR API 文档 (javadoc)](https://docs.oracle.com/en/java/javase/21/docs/api/jdk.jfr/jdk/jfr/package-summary.html)
- [JEP 349: JFR Event Streaming](https://openjdk.org/jeps/349)
- [JEP 509: JFR CPU-Time Profiling](https://openjdk.org/jeps/509)
- [JEP 520: JFR Method Timing](https://openjdk.org/jeps/520)
- [JFR 配置参考 (.jfc)](https://docs.oracle.com/en/java/javase/21/jfapi/)
