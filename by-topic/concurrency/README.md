# 并发网络

多线程、网络通信、异步编程 -- 从 JDK 1.0 原始线程到 JDK 26 结构化并发的完整演进。

[← 返回主题索引](../)

---
## 目录

1. [演进概览](#1-演进概览)
2. [核心并发模型深度解析](#2-核心并发模型深度解析)
3. [完整 JEP 总表](#3-完整-jep-总表)
4. [OpenJDK 项目: Project Loom](#4-openjdk-项目-project-loom)
5. [代码演进示例](#5-代码演进示例)
6. [主题列表](#6-主题列表)
7. [核心贡献者](#7-核心贡献者)
8. [重要 PR 分析](#8-重要-pr-分析)
9. [内部开发者资源](#9-内部开发者资源)
10. [性能对比指南](#10-性能对比指南)
11. [统计数据](#11-统计数据)
12. [学习路径](#12-学习路径)

---


## 1. 演进概览

Java 并发模型经历了四个重大范式转变：从原始线程模型 (JDK 1.0) 到线程池抽象 (JDK 5)，从异步回调链 (JDK 8) 到轻量级虚拟线程 (JDK 21)，最终在 JDK 25-26 完成结构化并发的正式化。

```
JDK 1.0 ─── JDK 5 ─── JDK 7 ─── JDK 8 ─── JDK 9 ─── JDK 19 ── JDK 21 ── JDK 24 ── JDK 25 ── JDK 26
   |           |          |          |          |          |          |         |          |          |
 Thread     Executor   Fork/Join  Completable  Flow     Virtual   Virtual   解除Pin    Scoped    Structured
 Runnable   JSR-166    JSR-166y   Future       API      Threads   Threads   JEP 491   Values   Concurrency
 wait/notify Lock,Atomic           Parallel    JEP 266  (预览)    (正式)              (正式)    (第六预览)
             ConcurrentCollections Stream                JEP 425  JEP 444             JEP 506   JEP 525
```

### 版本里程碑

| 版本 | 年份 | 主题 | 关键特性 | 范式影响 |
|------|------|------|----------|----------|
| **JDK 1.0** | 1996 | 原始线程 | Thread, Runnable, synchronized, wait/notify | OS 线程 1:1 映射 |
| **JDK 5** | 2004 | **并发革命** | Executor、并发集合、Lock/Condition、原子变量 (JSR-166) | 线程池抽象 |
| **JDK 7** | 2011 | 并行计算 | Fork/Join (JSR-166y)、Phaser、TransferQueue | 工作窃取并行 |
| **JDK 8** | 2014 | **函数式并发** | CompletableFuture (JEP 155)、Parallel Stream、StampedLock | 异步回调链 |
| **JDK 9** | 2017 | 响应式流 | Flow API (JEP 266)、CompletableFuture 增强 | 发布-订阅模型 |
| **JDK 11** | 2018 | HTTP 标准化 | HTTP Client 正式版 (JEP 321) | 异步 HTTP |
| **JDK 19-20** | 2022-23 | Loom 预览 | Virtual Threads 预览 (JEP 425/436)、SC 孵化 (JEP 428/437) | 轻量级线程 |
| **JDK 21** | 2023 | **并发新纪元 (LTS)** | Virtual Threads 正式 (JEP 444)、SC 预览 (JEP 453)、Scoped Values 预览 (JEP 446) | 百万级并发 |
| **JDK 22-23** | 2024 | API 打磨 | SC 第二/三次预览 (JEP 462/480)、Scoped Values 持续预览 | - |
| **JDK 24** | 2025 | **Pin 问题修复** | 虚拟线程不再 Pin (JEP 491)、SC 第四次预览 (JEP 499) | synchronized 兼容 |
| **JDK 25** | 2025 | **Loom 成熟 (LTS)** | Scoped Values 正式 (JEP 506)、SC 第五次预览 (JEP 505)、Stable Values 预览 (JEP 502) | 静态工厂 + Joiner |
| **JDK 25** | 2026 | 并发完善 | SC 第六次预览 (JEP 525)、HTTP/3 预览 (JEP 517) | onTimeout + Joiner 改进 |

> SC = Structured Concurrency

---

## 2. 核心并发模型深度解析

### 2.1 ExecutorService (JDK 5, JSR-166)

Doug Lea 设计的 `java.util.concurrent` 框架，将任务提交与执行解耦。`ThreadPoolExecutor` 提供可配置线程池，`ScheduledThreadPoolExecutor` 支持延迟/周期任务。关键并发工具：`ConcurrentHashMap`, `BlockingQueue`, `CountDownLatch`, `CyclicBarrier`, `Semaphore`, `ReentrantLock`。

### 2.2 ForkJoinPool (JDK 7, JSR-166y)

工作窃取 (work-stealing) 分治并行框架。每个工作线程维护本地双端队列，空闲线程从其他线程队列窃取任务。JDK 8 起成为 `Parallel Stream` 和 `CompletableFuture` 的默认执行器 (`commonPool()`)，JDK 21 起也作为虚拟线程载体线程调度器。

### 2.3 CompletableFuture (JDK 8, JEP 155)

函数式异步编程核心。链式组合：`thenApply`/`thenCompose`/`thenCombine`；异常处理：`exceptionally`/`handle`；多 Future：`allOf`/`anyOf`。JDK 9 增强 (JEP 266)：`orTimeout()`, `completeOnTimeout()`, `delayedExecutor()`。

### 2.4 Virtual Threads (JDK 21, JEP 444)

Project Loom 核心成果。JVM 管理的轻量级线程 (~1KB 栈空间 vs 平台线程 ~1MB)，运行在 `ForkJoinPool` 载体线程上，阻塞时自动卸载 (unmount)。与现有 Thread API 完全兼容。**JDK 24 里程碑 (JEP 491)**: 解决 synchronized 导致的 pinning，虚拟线程在 synchronized 块内阻塞时可正常卸载载体线程。

### 2.5 Structured Concurrency (JDK 19 孵化 -> JDK 26 第六次预览)

`StructuredTaskScope` 管理子任务生命周期，确保与父作用域绑定。**JDK 25 (JEP 505)**: 静态工厂 `StructuredTaskScope.open()` + `Joiner` 接口。**JDK 26 (JEP 525)**: `onTimeout()` 回调允许超时时返回部分结果；`allSuccessfulOrThrow()` 返回 List；配置修改器改用 `UnaryOperator<Configuration>`。

### 2.6 Scoped Values (JDK 25 正式, JEP 506)

取代 `ThreadLocal` 的不可变上下文传递。生命周期与调用栈绑定、自动清理、天然线程安全，与虚拟线程和结构化并发深度集成，空间和时间开销远低于 `ThreadLocal`。

### 2.7 Stable Values (JDK 25 预览, JEP 502)

延迟初始化的不可变值容器。`StableValue<T>` 首次访问前初始化、此后不可变。JVM 视其为常量并启用常量折叠优化。比 `final` 字段更灵活 (初始化时机不受构造器约束)，替代 double-checked locking。

---

## 3. 完整 JEP 总表

Java 并发相关的所有 JEP，从 JDK 5 到 JDK 26。

### 基础并发 (JDK 5-9)

| JEP/JSR | 版本 | 标题 | 状态 | 核心作者 |
|---------|------|------|------|----------|
| JSR-166 | JDK 5 | Concurrency Utilities | 正式 | Doug Lea |
| JSR-166y | JDK 7 | Fork/Join Framework | 正式 | Doug Lea |
| JEP 155 | JDK 8 | Concurrency Updates (CompletableFuture, StampedLock) | 正式 | Doug Lea |
| JEP 266 | JDK 9 | More Concurrency Updates (Flow API, CF 增强) | 正式 | Doug Lea |

### HTTP Client (JDK 9-26)

| JEP | 版本 | 标题 | 状态 | 核心作者 |
|-----|------|------|------|----------|
| JEP 110 | JDK 9 | HTTP/2 Client (Incubator) | 孵化 | Michael McMahon |
| JEP 321 | JDK 11 | HTTP Client (Standard) | 正式 | Chris Hegarty |
| JEP 517 | JDK 25 | HTTP/3 for the Java HTTP Client (Preview) | 预览 | Daniel Fuchs |

### Virtual Threads (JDK 19-24)

| JEP | 版本 | 标题 | 状态 | 核心作者 |
|-----|------|------|------|----------|
| JEP 425 | JDK 19 | Virtual Threads (Preview) | 预览 | Ron Pressler, Alan Bateman |
| JEP 436 | JDK 20 | Virtual Threads (Second Preview) | 预览 | Ron Pressler, Alan Bateman |
| JEP 444 | JDK 21 | Virtual Threads | **正式** | Ron Pressler, Alan Bateman |
| JEP 491 | JDK 24 | Synchronize Virtual Threads without Pinning | **正式** | Alan Bateman, Ron Pressler |

### Scoped Values (JDK 20-25)

| JEP | 版本 | 标题 | 状态 | 核心作者 |
|-----|------|------|------|----------|
| JEP 429 | JDK 20 | Scoped Values (Incubator) | 孵化 | Andrew Haley |
| JEP 446/464/481/487 | JDK 21-24 | Scoped Values (Preview 1-4) | 预览 | Andrew Haley |
| JEP 506 | JDK 25 | Scoped Values | **正式** | Andrew Haley |

### Structured Concurrency (JDK 19-26)

| JEP | 版本 | 标题 | 状态 | 核心作者 |
|-----|------|------|------|----------|
| JEP 428/437 | JDK 19-20 | Structured Concurrency (Incubator 1-2) | 孵化 | Ron Pressler, Alan Bateman |
| JEP 453/462/480/499 | JDK 21-24 | Structured Concurrency (Preview 1-4) | 预览 | Ron Pressler, Alan Bateman |
| JEP 505 | JDK 25 | Structured Concurrency (5th Preview, Joiner API) | 预览 | Ron Pressler, Alan Bateman |
| JEP 525 | JDK 26 | Structured Concurrency (6th Preview, onTimeout) | 预览 | Ron Pressler, Alan Bateman |

### Stable Values (JDK 25+)

| JEP | 版本 | 标题 | 状态 | 核心作者 |
|-----|------|------|------|----------|
| JEP 502 | JDK 25 | Stable Values (Preview) | 预览 | Per Liden |

---

## 4. OpenJDK 项目: Project Loom

Project Loom 是 Java 并发模型的根本性变革，目标是在 JVM 中实现轻量级用户态线程 (虚拟线程)、分界延续 (delimited continuations) 及相关特性。

> **项目主页**: [https://openjdk.org/projects/loom/](https://openjdk.org/projects/loom/)
> **技术负责人**: Ron Pressler (Oracle)
> **核心架构师**: Alan Bateman (Oracle)

### Loom 特性交付状态

| 特性 | 孵化 | 预览 | 正式 | 最终 JEP |
|------|------|------|------|----------|
| Virtual Threads | - | JDK 21-20 | **JDK 21** | JEP 444 |
| Virtual Threads 不再 Pin | - | - | **JDK 24** | JEP 491 |
| Scoped Values | JDK 25 | JDK 21-24 | **JDK 25** | JEP 506 |
| Structured Concurrency | JDK 19-20 | JDK 21-26 | 待定 | JEP 525 (第六次预览) |
| Stable Values | - | JDK 25 | 待定 | JEP 502 |

### JEP 491 深度解析: 虚拟线程 synchronized 不再 Pin

JDK 24 中的 JEP 491 是虚拟线程的重大里程碑。在此之前，虚拟线程进入 `synchronized` 方法/块后如果发生阻塞 (如 I/O)，会被"钉住" (pin) 在载体平台线程上，无法卸载，严重限制了并发可扩展性。

**解决方案**: 重新实现对象监视器 (object monitor)，允许虚拟线程在 `synchronized` 块内阻塞时释放载体线程。消除几乎所有 pinning 场景 (仅类初始化 `<clinit>` 期间例外)。**影响**: 使用 `synchronized` 的现有代码库 (JDBC 驱动、传统库) 无需迁移到 `ReentrantLock` 即可充分利用虚拟线程。

> [Loom 时间线](../core/loom/timeline.md)

---

## 5. 代码演进示例

从 JDK 1.0 到 JDK 26，并发编程风格的完整演进。

### 5.1 JDK 1.0: 原始线程

```java
// 手动管理线程生命周期，无法控制并发度
Thread t1 = new Thread(() -> { result1 = fetchFromService("A"); });
Thread t2 = new Thread(() -> { result2 = fetchFromService("B"); });
t1.start(); t2.start();
t1.join(); t2.join();  // 如果 t1 抛异常，t2 仍在运行 -- 资源泄漏
```

### 5.2 JDK 5: ExecutorService + Future

```java
// 线程池抽象，但 Future.get() 仍然阻塞
ExecutorService executor = Executors.newFixedThreadPool(10);
Future<String> f1 = executor.submit(() -> fetchFromService("A"));
Future<String> f2 = executor.submit(() -> fetchFromService("B"));
String r1 = f1.get();  // 阻塞等待
String r2 = f2.get();  // 如果 f1 失败，f2 不会自动取消
executor.shutdown();
```

### 5.3 JDK 8: CompletableFuture

```java
// 异步回调链，但调试困难、错误传播复杂
var cf1 = CompletableFuture.supplyAsync(() -> fetchFromService("A"));
var cf2 = CompletableFuture.supplyAsync(() -> fetchFromService("B"));
cf1.thenCombine(cf2, (r1, r2) -> r1 + " + " + r2)
   .thenAccept(System.out::println)
   .exceptionally(ex -> { log(ex); return null; });
// 问题：回调地狱、堆栈跟踪丢失、线程上下文传播复杂
```

### 5.4 JDK 21: Virtual Threads

```java
// 轻量级线程，同步代码风格，百万级并发
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    Future<String> f1 = executor.submit(() -> fetchFromService("A"));
    Future<String> f2 = executor.submit(() -> fetchFromService("B"));
    String result = f1.get() + " + " + f2.get();
    // 每个虚拟线程约 1KB; JDK 24 起 synchronized 也不再 pin
}
```

### 5.5 JDK 25-26: Structured Concurrency + Scoped Values

```java
// 结构化并发：子任务生命周期与父作用域绑定，任一失败自动取消其余
static final ScopedValue<UserContext> USER = ScopedValue.newInstance();

ScopedValue.runWhere(USER, currentUser, () -> {
    try (var scope = StructuredTaskScope.open(
            Joiner.allSuccessfulOrThrow(),  // JDK 25: 静态工厂 + Joiner
            cfg -> cfg.withTimeout(Duration.ofSeconds(5)))) {
        Subtask<String> s1 = scope.fork(() -> fetchFromService("A")); // 继承 ScopedValue
        Subtask<String> s2 = scope.fork(() -> fetchFromService("B"));
        scope.join();
        String result = s1.get() + " + " + s2.get();
        // 超时 -> JDK 26 onTimeout() 可返回回退值而非抛异常
    }
});
```

### 5.6 编程模型对比总结

| 特性 | Thread | ExecutorService | CompletableFuture | Virtual Threads | Structured Concurrency |
|------|--------|----------------|-------------------|-----------------|----------------------|
| 版本 | JDK 1.0 | JDK 5 | JDK 8 | JDK 21 | JDK 25-26 |
| 代码风格 | 命令式 | 线程池 | 回调链 | 同步式 | 结构化 |
| 并发量级 | 数千 | 数百 (受池大小限制) | 数千 | **百万级** | **百万级** |
| 错误传播 | 手动 | 手动 | 链式 | 手动 | **自动** |
| 取消传播 | 手动 | 手动 | 手动 | 手动 | **自动** |
| 调试友好 | 一般 | 一般 | 差 (异步栈) | **好** | **好** |
| 上下文传播 | ThreadLocal | ThreadLocal | 手动传递 | ThreadLocal | **ScopedValue** |

---

## 6. 主题列表

### [并发编程](concurrency/)

从 Thread 到 Virtual Thread 的演进。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 5 | Executor 框架 | JSR-166 |
| JDK 7 | Fork/Join 框架 | JSR-166y |
| JDK 8 | CompletableFuture、StampedLock | JEP 155 |
| JDK 9 | CompletableFuture 增强、Flow API (Reactive Streams) | JEP 266 |
| JDK 19 | **Virtual Threads** (预览) | JEP 425 |
| JDK 20 | Virtual Threads (第二次预览) | JEP 436 |
| JDK 21 | **Virtual Threads** (正式)、**Structured Concurrency** (预览)、**Scoped Values** (预览) | JEP 444, JEP 453, JEP 446 |
| JDK 23-23 | Structured Concurrency (持续预览) | JEP 462, JEP 480 |
| JDK 24 | **虚拟线程不再 Pin** (synchronized 不再阻塞载体线程)、Structured Concurrency 第四次预览 | JEP 491, JEP 499 |
| JDK 25 | **Scoped Values** (正式)、Structured Concurrency 第五次预览 (静态工厂方法 + Joiner)、**Stable Values** 预览 | JEP 506, JEP 505, JEP 502 |
| JDK 26 | Structured Concurrency 第六次预览 (onTimeout() + Joiner 改进) | JEP 525 |

> [并发时间线](concurrency/timeline.md)

### [HTTP 客户端](http/)

从 HttpURLConnection 到 HTTP/3。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 1.0 | HttpURLConnection | - |
| JDK 9 | HTTP Client (孵化器) | JEP 110 |
| JDK 10 | HTTP Client (孵化器) | - |
| JDK 11 | **HTTP Client** (标准) | JEP 321 |
| JDK 22-23 | 连接复用优化 | - |
| JDK 25 | **HTTP/3** (预览) | JEP 517 |

> [HTTP 演进时间线](http/timeline.md)

### [网络编程](network/)

Java 网络编程从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 1.0 | Socket/ServerSocket | TCP/UDP 基础 |
| JDK 1.1 | URL/HttpURLConnection | HTTP 支持 |
| JDK 5 | URLHandler | 自定义协议 |
| JDK 7 | Asynchronous I/O | 异步网络 |
| JDK 9 | HTTP/2 | 多路复用 |
| JDK 11 | HTTP Client 标准化 | 新 API |
| JDK 16 | Unix Domain Socket | 本地 IPC |

> [网络编程时间线](network/timeline.md)

### [序列化](serialization/)

Java 序列化从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 1.0 | Serializable | 基础序列化 |
| JDK 5 | 枚举序列化 | Enum 支持 |
| JDK 7 | Externalizable 增强 | 自定义序列化 |
| JDK 17 | 密封序列化 | 序列化检查 |
| JDK 21 | Record 序列化 | 简化序列化 |

> [序列化时间线](serialization/timeline.md)

---

## 7. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### Project Loom 核心团队

| 贡献者 | 组织 | 角色 | 核心贡献 |
|--------|------|------|----------|
| **Ron Pressler** | Oracle | Loom 技术负责人 | Virtual Threads 架构设计、Structured Concurrency JEP 作者、Continuation 实现 |
| **Alan Bateman** | Oracle | JDK 架构师 | Virtual Threads 实现、NIO/NIO.2 架构 (JSR 51/203)、JEP 491 Pin 修复、Structured Concurrency JEP 共同作者 |
| **Andrew Haley** | Red Hat | Scoped Values 负责人 | Scoped Values JEP 429/446/464/481/487/506 全部预览到正式的作者 |
| **Doug Lea** | SUNY Oswego | 并发框架之父 | JSR-166 整体设计、ConcurrentHashMap、ForkJoinPool、CompletableFuture 基础架构 |

### 并发编程 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Doug Lea | 65 | SUNY Oswego | JSR-166 (并发工具), ConcurrentHashMap, ForkJoinPool |
| 2 | Alan Bateman | 43 | Oracle | NIO/NIO.2, Virtual Threads, JEP 491 |
| 3 | Viktor Klang | 29 | Oracle | CompletableFuture 增强 |
| 4 | Martin Buchholz | 13 | Google | 并发工具, 算法优化 |
| 5 | Stuart Marks | 8 | Oracle | 集合, 并发 |
| 6 | David Holmes | 6 | Oracle | JSR-166 规范负责人, HotSpot 同步原语 |
| 7 | Roger Riggs | 4 | Oracle | 工具类, 集合 |

### HTTP/网络 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Daniel Fuchs | 95 | Oracle | HTTP Client, HTTP/3 |
| 2 | Michael McMahon | 19 | Oracle | HTTP Client (JEP 321) |
| 3 | Jaikiran Pai | 18 | Red Hat/Oracle | HTTP/2, 网络层 |
| 4 | Volkan Yazici | 17 | Oracle | HTTP/3, WebSocket |
| 5 | Chris Hegarty | 17 | Oracle | HTTP Client 基础 |
| 6 | Daniel Jelinski | 16 | Oracle | HTTP/2, 连接池 |
| 7 | Conor Cleary | 14 | Oracle | HTTP/3 (QUIC) |

---

## 8. 重要 PR 分析

### 并发集合优化

#### JDK-8348880: ZoneOffset 缓存优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: +15-25% 时区偏移缓存性能

将 `ConcurrentHashMap<Integer, ZoneOffset>` 改为 `AtomicReferenceArray<ZoneOffset>`：

**核心改进**:
- 消除 `int` -> `Integer` 自动装箱
- 数组访问比 HashMap 更快
- 内存占用减少 85%

```java
// 优化前
ConcurrentMap<Integer, ZoneOffset> cache = new ConcurrentHashMap<>();
Integer key = quarters;  // 装箱
ZoneOffset result = cache.get(key);

// 优化后
AtomicReferenceArray<ZoneOffset> cache = new AtomicReferenceArray<>(256);
int key = quarters & 0xff;  // 无装箱
ZoneOffset result = cache.getOpaque(key);
```

> [详细分析](/by-pr/8348/8348880.md)

### 分布式系统优化

#### JDK-8353741: UUID.toString SWAR 优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: +40-60% UUID.toString 性能提升

使用 SWAR (SIMD Within A Register) 技术替代查找表：

**优化点**:
- 消除查找表缓存未命中
- 寄存器内并行计算
- 使用 `Long.expand` intrinsic

> [详细分析](/by-pr/8353/8353741.md)

### 字节码生成优化

#### JDK-8340587: StackMapGenerator 优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: +3-7% StackMap 生成性能

优化 `checkAssignableTo` 方法，避免空栈复制：

**优化点**:
- 空栈时跳过复制
- 用 `clone()` 替代 `Array.copyOf`
- 局部变量缓存

> [详细分析](/by-pr/8340/8340587.md)

---

## 9. 内部开发者资源

### 源码结构

```
src/java.base/share/classes/java/util/concurrent/
├── atomic/                           # AtomicBoolean, AtomicInteger, AtomicReference...
├── locks/                            # Lock, ReentrantLock, StampedLock, AQS
├── ExecutorService.java              # 执行器接口
├── ThreadPoolExecutor.java           # 线程池实现
├── ForkJoinPool.java                 # Fork/Join 池 (也是虚拟线程载体调度器)
├── CompletableFuture.java            # 异步编程
├── ConcurrentHashMap.java            # 并发 Map
├── StructuredTaskScope.java          # 结构化并发 (JDK 21+)
└── Flow.java                         # Reactive Streams (JDK 9+)

src/java.base/share/classes/java/lang/
├── Thread.java                       # 线程核心类
├── VirtualThread.java                # 虚拟线程 (JDK 21+, 内部)
├── ScopedValue.java                  # 作用域值 (JDK 25+ 正式)
└── StableValue.java                  # 稳定值 (JDK 25+ 预览)

src/java.net.http/                    # HttpClient, HttpRequest, HttpResponse, WebSocket
src/java.base/share/classes/java/nio/ # channels/, ByteBuffer, file/ (NIO.2)
```

### 关键内部类

| 类 | 作用 | 访问级别 |
|---|------|----------|
| `jdk.internal.vm.Continuation` | 虚拟线程 continuation 实现 | 内部 |
| `jdk.internal.vm.ScopedValueContainer` | Scoped Value 存储 | 内部 |
| `jdk.internal.misc.Blocker` | 虚拟线程 Pin 检测 | `@Restricted` |
| `jdk.internal.net.http.HttpClientImpl` | HTTP Client 实现 | 内部 |
| `java.util.concurrent.locks.AbstractQueuedSynchronizer` | AQS 同步器 | public |
| `java.util.concurrent.ForkJoinPool.WorkQueue` | 工作窃取队列 | 内部 |

### VM 参数速查

```bash
# 虚拟线程 (JDK 21+)
-Djdk.virtualThreadScheduler.parallelism=8  # 载体线程并发度 (默认=CPU 核数)
-Djdk.virtualThreadScheduler.maxPoolSize=256 # 最大载体线程数
-Djdk.tracePinnedThreads=full               # 追踪 pinning (JDK 21-23, 24 起大部分场景已修复)

# Fork/Join Pool
-Djava.util.concurrent.ForkJoinPool.common.parallelism=8

# HTTP Client
-XX:MaxDirectMemorySize=512m     # 直接内存 (用于 NIO)
-Djdk.httpclient.connectionPoolSize=20

# 网络调试
-Djdk.httpclient.enableAllMethodRetry=true
-Djdk.httpclient.websocket.debug=true
-Djavax.net.debug=ssl             # SSL 调试
```

### 诊断工具

```bash
# 线程转储 (包含虚拟线程, JDK 21+)
jcmd <pid> Thread.dump_to_file -format=json threads.json

# JFR 虚拟线程事件 (jdk.VirtualThreadStart, jdk.VirtualThreadEnd, jdk.VirtualThreadPinned)
jcmd <pid> JFR.start name=vthread settings=profile

# HTTP Client 调试
-Djdk.httpclient.HttpClient.log=errors,requests,headers
```

---

## 10. 性能对比指南

### 吞吐量对比 (I/O 密集场景)

| 场景 | 平台线程 (池 200) | 虚拟线程 | 提升 |
|------|-------------------|----------|------|
| 10K 并发 HTTP 请求 | ~200 req/s | ~8,000+ req/s | ~40x |
| 100K 并发连接保持 | OOM/拒绝 | 正常运行 | N/A |
| CPU 密集计算 | ~CPU 核数 | ~CPU 核数 | ~1x |

### 场景选型

| 场景 | 推荐方案 | 原因 |
|------|----------|------|
| I/O 密集服务 | Virtual Threads | 阻塞时释放载体线程 |
| CPU 密集计算 | ForkJoinPool / Parallel Stream | 工作窃取更高效 |
| 异步事件处理 | CompletableFuture | 回调链式组合 |
| 多子任务聚合 | Structured Concurrency | 自动取消 + 错误传播 |
| 上下文传递 | ScopedValue | 不可变、自动清理、低开销 |
| 延迟初始化 | StableValue | JVM 常量折叠优化 |

> **虚拟线程不适用**: CPU 密集计算 (不会主动让出)、需要线程亲和性、大量 `ThreadLocal` 可变状态 (建议迁移到 ScopedValue)

---

## 11. 统计数据

| 指标 | 数值 |
|------|------|
| 并发相关 JEP/JSR (JDK 5-26) | 30+ |
| Loom 预览轮次 | Virtual Threads 2 次 (JDK 19-20), Structured Concurrency 8 次 (孵化 2 + 预览 6, JDK 19-26), Scoped Values 6 次 (孵化 1 + 预览 5, JDK 20-25) |
| j.u.c 工具类 | 50+ |
| HTTP 协议支持 | HTTP/1.1, HTTP/2, HTTP/3 (预览) |
| 虚拟线程 Pin 限制 | JDK 24 起仅类初始化期间会 Pin (JEP 491) |
| Scoped Values 状态 | JDK 25 正式化 (JEP 506) |
| Stable Values 状态 | JDK 25 首次预览 (JEP 502) |
| Structured Concurrency 状态 | JDK 26 第六次预览 (JEP 525), 引入 onTimeout() |

---

## 12. 学习路径

1. **入门**: [并发编程](concurrency/) -- Thread, synchronized, Executor 框架 (JSR-166)
2. **进阶**: CompletableFuture -> Virtual Threads -> Scoped Values
3. **深入**: Structured Concurrency (Joiner/超时) -> JEP 491 Pin 原理 -> ForkJoinPool 工作窃取
4. **网络**: [HTTP 客户端](http/) -> [网络编程](network/) -> [序列化](serialization/)

**推荐阅读**: [State of Loom](https://cr.openjdk.org/~rpressler/loom/loom/sol1_part1.html) | [Project Loom](https://openjdk.org/projects/loom/) | [Inside.java Loom](https://inside.java/tag/loom/)
