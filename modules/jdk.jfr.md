---

# jdk.jfr 模块分析

> JDK Flight Recorder (JFR) — 低开销的持续监控和事件记录框架

---

## 1. 模块定义

**源文件**: `src/jdk.jfr/share/classes/module-info.java`

```
module jdk.jfr {
    exports jdk.jfr;
    exports jdk.jfr.consumer;
    exports jdk.jfr.internal.management to java.management;
}
```

### 核心包

| 包 | 用途 |
|---|---|
| `jdk.jfr` | 事件定义、注解、配置 |
| `jdk.jfr.consumer` | 事件消费（读取 .jfr 文件） |
| `jdk.jfr.internal.management` | JMX 管理（限定导出） |

---

## 2. 核心架构

### 2.1 JFR 事件生命周期

```
┌─────────────────────────────────────────────────────────┐
│                    JFR Architecture                     │
│                                                         │
│  ┌──────────────┐     ┌──────────────┐                 │
│  │  Event 定义   │────►│  Event 注册  │                 │
│  │  (@Name etc) │     │  (Metadata)  │                 │
│  └──────────────┘     └──────┬───────┘                 │
│                              │                          │
│  ┌──────────────┐     ┌──────▼───────┐                 │
│  │  Event 写入   │────►│  Buffer      │                 │
│  │  (commit())  │     │  (thread-local)│                │
│  └──────────────┘     └──────┬───────┘                 │
│                              │                          │
│  ┌──────────────┐     ┌──────▼───────┐                 │
│  │  Chunk 写入   │────►│  .jfr File   │                 │
│  │  (Disk/内存)  │     │  (Recording) │                 │
│  └──────────────┘     └──────────────┘                 │
└─────────────────────────────────────────────────────────┘
```

### 2.2 事件类型层次

```
jdk.jfr.Event (抽象基类)
├── JVM 内置事件 (~80 种)
│   ├── GC 事件: GCPhasePause, GCPhaseConcurrent
│   ├── JIT 事件: Compilation, SweepCodeCache
│   ├── 类加载: ClassLoad, ClassDefine
│   ├── 线程: ThreadStart, ThreadEnd, ThreadSleep
│   ├── 文件 I/O: FileRead, FileWrite
│   ├── Socket I/O: SocketRead, SocketWrite
│   ├── 内存: HeapSummary, MetaspaceSummary
│   └── 异常: ExceptionThrown, ErrorThrown
│
└── 自定义事件 (extends Event)
    └── 用户定义的业务事件
```

---

## 3. 核心 API

### 3.1 自定义事件

```java
// 定义自定义事件
@Name("com.example.OrderProcessed")
@Label("Order Processed")
@Category({"Business", "Orders"})
public class OrderProcessedEvent extends Event {
    @Label("Order ID")
    String orderId;

    @Label("Amount")
    @DataAmount
    double amount;

    @Label("Processing Time")
    @Timespan(Timespan.MILLISECONDS)
    long processingTime;
}

// 使用自定义事件
OrderProcessedEvent event = new OrderProcessedEvent();
event.orderId = "ORD-12345";
event.amount = 99.99;
event.begin();  // 开始计时
// ... 业务逻辑 ...
event.processingTime = event.elapsedTime();
event.commit(); // 提交事件
```

### 3.2 录制控制

```java
// 编程式控制录制
Configuration config = Configuration.getConfiguration("default");
Recording recording = new Recording(config);
recording.enable("jdk.CPULoad").withPeriod(Duration.ofSeconds(1));
recording.enable("jdk.GCPhasePause");
recording.enable("com.example.OrderProcessed");
recording.start();

// ... 运行一段时间 ...

recording.stop();
recording.dump(Paths.get("recording.jfr"));
```

### 3.3 事件消费

```java
// 读取 .jfr 文件
try (RecordingFile file = new RecordingFile(Paths.get("recording.jfr"))) {
    while (file.hasMoreEvents()) {
        RecordedEvent event = file.readEvent();
        if (event.getEventType().getName().equals("jdk.GCPhasePause")) {
            System.out.println("GC Pause: " + event.getDuration().toMillis() + "ms");
        }
    }
}
```

---

## 4. 内置事件速查

### 高频使用的内置事件

| 事件名 | 类别 | 用途 |
|--------|------|------|
| `jdk.CPULoad` | OS | CPU 使用率（进程/系统） |
| `jdk.GCPhasePause` | GC | GC STW 暂停时间 |
| `jdk.GCPhaseConcurrent` | GC | GC 并发阶段时间 |
| `jdk.JavaMonitorWait` | 线程 | 监视器等待（锁竞争） |
| `jdk.JavaMonitorBlocked` | 线程 | 监视器阻塞 |
| `jdk.ThreadAllocationStatistics` | 线程 | 线程内存分配 |
| `jdk.FileRead` / `jdk.FileWrite` | I/O | 文件读写 |
| `jdk.SocketRead` / `jdk.SocketWrite` | I/O | 网络读写 |
| `jdk.ExceptionThrown` | 异常 | 异常抛出统计 |
| `jdk.Compilation` | JIT | JIT 编译事件 |
| `jdk.ClassLoad` | 类加载 | 类加载统计 |
| `jdk.HeapSummary` | 内存 | 堆使用概要 |
| `jdk.MetaspaceSummary` | 内存 | Metaspace 概要 |
| `jdk.OldObjectSample` | 内存 | 长寿对象采样（泄漏检测） |
| `jdk.VirtualThreadPinned` | 线程 | 虚拟线程钉住 |
| `jdk.VirtualThreadSubmitFailed` | 线程 | 虚拟线程提交失败 |

---

## 5. 配置选项

### 启动参数

```bash
# 启动时自动开始录制
-XX:StartFlightRecording=duration=60s,filename=app.jfr,settings=profile

# 常用 settings
#   default  — 低开销（<1%），适合生产
#   profile  — 更详细（<2%），适合性能分析

# 磁盘存储配置
-XX:FlightRecorderOptions=repository=/tmp/jfr,maxchunksize=10m,disk=true
```

### jcmd 命令

```bash
# 开始录制
jcmd <pid> JFR.start name=profiling settings=profile duration=60s filename=recording.jfr

# 查看正在进行的录制
jcmd <pid> JFR.check

# 停止并保存
jcmd <pid> JFR.stop name=profiling filename=recording.jfr

# 转储当前录制
jcmd <pid> JFR.dump name=profiling filename=dump.jfr

# 动态启用/禁用事件
jcmd <pid> JFR.configure enabled=true jdk.OldObjectSample#cutoff=10m
```

---

## 6. 性能特征

| 配置 | CPU 开销 | 内存开销 | 适用场景 |
|------|---------|---------|---------|
| `default` | <1% | ~10MB | 生产环境持续监控 |
| `profile` | 1-2% | ~30MB | 性能问题排查 |
| 自定义 (仅业务事件) | <0.1% | ~1MB | 业务指标采集 |
| OldObjectSample | 2-5% | ~50MB | 内存泄漏排查（短期使用） |

---

## 7. 与其他工具对比

| 特性 | JFR | async-profiler | JMC | jstat/jmap |
|------|-----|----------------|-----|------------|
| 开销 | <2% | <5% | N/A (消费端) | STW (jmap) |
| 实时性 | 持续录制 | 按需采样 | 事后分析 | 按需执行 |
| 事件类型 | JVM + 自定义 | CPU/Alloc/Wall | 可视化分析 | 内存统计 |
| 生产安全 | ✅ | ⚠️ (JNI agent) | ✅ | ⚠️ (STW) |
| JDK 内置 | ✅ | ❌ | ✅ | ✅ |

---

## 8. 相关链接

- [JFR 指南](/guides/jfr.md)
- [GC 调优案例](/cases/gc-tuning-case.md)
- [内存泄漏诊断](/cases/memory-leak-diagnosis.md)
- [HotSpot 总体架构](hotspot.md)
