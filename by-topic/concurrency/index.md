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
JDK 1.0 ── JDK 5 ── JDK 7 ── JDK 8 ── JDK 9 ── JDK 19 ── JDK 21 ── JDK 24 ── JDK 25 ── JDK 26
   |          |         |         |        |         |          |          |          |          |
 Thread    Executor  Fork/Join Completable Flow    Virtual   Virtual    解除       Scoped    Structured
 Runnable  Framework Framework  Future     API     Threads   Threads    Pin 限制   Values   Concurrency
 synchronized (JSR-166) (JSR-166y) Parallel (JEP 266) (预览)   (正式)    JEP 491   (正式)    (第六次预览)
 wait/notify  Lock     |       Stream       |     JEP 425  JEP 444      |       JEP 506    JEP 525
              Atomic   |      (JEP 155)     |     Scoped   Scoped     Struct.   Stable      |
              Concurrent|                    |     Values   Values    Concur.   Values    onTimeout()
              Collections                    |     (孵化)   (预览)    第四预览  (预览)     Joiner 改进
                                             |                        JEP 499  JEP 502
                                             |
                                        Reactive Streams
```

### 版本里程碑

| 版本 | 年份 | 主题 | 关键特性 | 范式影响 |
|------|------|------|----------|----------|
| **JDK 1.0** | 1996 | 原始线程 | Thread, Runnable, synchronized, wait/notify | 操作系统线程 1:1 映射 |
| **JDK 1.2** | 1998 | 集合框架 | Collections.synchronizedXxx, Hashtable | 同步包装器 |
| **JDK 5** | 2004 | **并发革命** | Executor 框架、并发集合、Lock/Condition、原子变量 (JSR-166) | 线程池抽象 |
| **JDK 6** | 2006 | 并发增强 | Deque、NavigableMap/Set、ConcurrentSkipListMap | 无锁数据结构 |
| **JDK 7** | 2011 | 并行计算 | Fork/Join 框架 (JSR-166y)、Phaser、TransferQueue | 工作窃取并行 |
| **JDK 8** | 2014 | **函数式并发** | CompletableFuture (JEP 155)、Parallel Stream、StampedLock | 异步回调链 |
| **JDK 9** | 2017 | 响应式流 | Flow API / Reactive Streams (JEP 266)、CompletableFuture 增强 | 发布-订阅模型 |
| **JDK 11** | 2018 | HTTP 标准化 | HTTP Client 正式版 (JEP 321) | 异步 HTTP |
| **JDK 19** | 2022 | 虚拟线程预览 | Virtual Threads 预览 (JEP 425)、Structured Concurrency 孵化 (JEP 428) | 轻量级线程 |
| **JDK 20** | 2023 | 持续预览 | Virtual Threads 第二次预览 (JEP 436)、Scoped Values 孵化 (JEP 429) | - |
| **JDK 21** | 2023 | **并发新纪元 (LTS)** | Virtual Threads 正式 (JEP 444)、Structured Concurrency 预览 (JEP 453)、Scoped Values 预览 (JEP 446) | 百万级并发 |
| **JDK 22** | 2024 | API 稳定化 | Structured Concurrency 第二次预览 (JEP 462) | - |
| **JDK 23** | 2024 | 持续打磨 | Structured Concurrency 第三次预览 (JEP 480)、Scoped Values 第二次预览 (JEP 481) | - |
| **JDK 24** | 2025 | **Pin 问题修复** | 虚拟线程不再 Pin (JEP 491)、Structured Concurrency 第四次预览 (JEP 499) | synchronized 兼容 |
| **JDK 25** | 2025 | **Loom 成熟 (LTS)** | Scoped Values 正式 (JEP 506)、Structured Concurrency 第五次预览 (JEP 505)、Stable Values 预览 (JEP 502) | 静态工厂 + Joiner |
| **JDK 26** | 2026 | 并发完善 | Structured Concurrency 第六次预览 (JEP 525)、HTTP/3 预览 (JEP 517) | onTimeout + Joiner 改进 |

---

## 2. 核心并发模型深度解析

### 2.1 ExecutorService (JDK 5, JSR-166)

Doug Lea 设计的 `java.util.concurrent` 框架是 Java 并发编程的基石。核心抽象将任务提交与执行解耦：

- **ThreadPoolExecutor**: 可配置的通用线程池 (核心线程数、最大线程数、队列策略)
- **ScheduledThreadPoolExecutor**: 支持延迟和周期任务
- **Executors**: 工厂方法 (`newFixedThreadPool`, `newCachedThreadPool` 等)

关键并发工具：`ConcurrentHashMap`, `CopyOnWriteArrayList`, `BlockingQueue`, `CountDownLatch`, `CyclicBarrier`, `Semaphore`

### 2.2 ForkJoinPool (JDK 7, JSR-166y)

工作窃取 (work-stealing) 算法的分治并行框架：

- 每个工作线程维护本地双端队列
- 空闲线程从其他线程队列的尾部窃取任务
- `RecursiveTask<V>` (有返回值) 和 `RecursiveAction` (无返回值)
- JDK 8 起成为 Parallel Stream 和 CompletableFuture 的默认执行器 (`ForkJoinPool.commonPool()`)
- JDK 21 起也作为虚拟线程的载体线程调度器

### 2.3 CompletableFuture (JDK 8, JEP 155)

函数式异步编程的核心，支持链式组合：

- **转换**: `thenApply`, `thenCompose`, `thenCombine`
- **消费**: `thenAccept`, `thenRun`
- **异常处理**: `exceptionally`, `handle`, `whenComplete`
- **多 Future 组合**: `allOf`, `anyOf`
- JDK 9 增强 (JEP 266)：`orTimeout()`, `completeOnTimeout()`, `delayedExecutor()`

### 2.4 Virtual Threads (JDK 21, JEP 444)

Project Loom 的核心成果。虚拟线程是由 JVM 管理的轻量级线程，不由操作系统调度：

- **核心优势**: 创建成本极低 (约 1KB 栈空间 vs 平台线程 1MB)，支持百万级并发
- **调度器**: 运行在 `ForkJoinPool` 载体线程上，阻塞时自动卸载 (unmount)
- **兼容性**: 与现有 Thread API 完全兼容，`synchronized`、`ThreadLocal` 均可用
- **JDK 24 里程碑 (JEP 491)**: 解决 synchronized 导致的 pinning 问题，虚拟线程在 synchronized 块内阻塞时可以正常卸载载体线程

### 2.5 Structured Concurrency (JDK 19 孵化 → JDK 26 第六次预览)

将并发任务组织为结构化的作用域，确保子任务的生命周期与父作用域绑定：

- **核心类**: `StructuredTaskScope` -- 管理一组子任务的生命周期
- **JDK 25 重大改进 (JEP 505)**: 构造器替换为静态工厂方法 `StructuredTaskScope.open()`，引入 `Joiner` 接口定义任务完成策略
- **JDK 26 新增 (JEP 525)**: `onTimeout()` 回调让自定义 Joiner 在超时时返回部分结果或回退值，而非总是抛出 `TimeoutException`；`Joiner::allSuccessfulOrThrow()` 返回 List 而非 Stream；配置修改器改用 `UnaryOperator<Configuration>`

### 2.6 Scoped Values (JDK 21 预览 → JDK 25 正式, JEP 506)

取代 `ThreadLocal` 的不可变上下文传递机制：

- 生命周期与调用栈绑定，自动清理
- 不可变语义，天然线程安全
- 与虚拟线程和结构化并发深度集成
- 空间和时间开销远低于 `ThreadLocal`

### 2.7 Stable Values (JDK 25 预览, JEP 502)

延迟初始化的不可变值容器：

- `StableValue<T>` 持有单个数据值，首次访问前初始化，此后不可变
- JVM 将其视为常量，启用与 `final` 字段相同的优化
- 比 `final` 字段更灵活：初始化时机不受构造器约束
- 替代 double-checked locking 等易出错的延迟初始化模式

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
| JEP 517 | JDK 26 | HTTP/3 for the Java HTTP Client (Preview) | 预览 | Daniel Fuchs |

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
| JEP 446 | JDK 21 | Scoped Values (Preview) | 预览 | Andrew Haley |
| JEP 464 | JDK 22 | Scoped Values (Second Preview) | 预览 | Andrew Haley |
| JEP 481 | JDK 23 | Scoped Values (Third Preview) | 预览 | Andrew Haley |
| JEP 487 | JDK 24 | Scoped Values (Fourth Preview) | 预览 | Andrew Haley |
| JEP 506 | JDK 25 | Scoped Values | **正式** | Andrew Haley |

### Structured Concurrency (JDK 19-26)

| JEP | 版本 | 标题 | 状态 | 核心作者 |
|-----|------|------|------|----------|
| JEP 428 | JDK 19 | Structured Concurrency (Incubator) | 孵化 | Ron Pressler, Alan Bateman |
| JEP 437 | JDK 20 | Structured Concurrency (Second Incubator) | 孵化 | Ron Pressler, Alan Bateman |
| JEP 453 | JDK 21 | Structured Concurrency (Preview) | 预览 | Ron Pressler, Alan Bateman |
| JEP 462 | JDK 22 | Structured Concurrency (Second Preview) | 预览 | Ron Pressler, Alan Bateman |
| JEP 480 | JDK 23 | Structured Concurrency (Third Preview) | 预览 | Ron Pressler, Alan Bateman |
| JEP 499 | JDK 24 | Structured Concurrency (Fourth Preview) | 预览 | Ron Pressler, Alan Bateman |
| JEP 505 | JDK 25 | Structured Concurrency (Fifth Preview) | 预览 | Ron Pressler, Alan Bateman |
| JEP 525 | JDK 26 | Structured Concurrency (Sixth Preview) | 预览 | Ron Pressler, Alan Bateman |

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
| Virtual Threads | - | JDK 19-20 | **JDK 21** | JEP 444 |
| Virtual Threads 不再 Pin | - | - | **JDK 24** | JEP 491 |
| Scoped Values | JDK 20 | JDK 21-24 | **JDK 25** | JEP 506 |
| Structured Concurrency | JDK 19-20 | JDK 21-26 | 待定 | JEP 525 (第六次预览) |
| Stable Values | - | JDK 25 | 待定 | JEP 502 |

### JEP 491 深度解析: 虚拟线程 synchronized 不再 Pin

JDK 24 中的 JEP 491 是虚拟线程的重大里程碑。在此之前，虚拟线程进入 `synchronized` 方法/块后如果发生阻塞 (如 I/O)，会被"钉住" (pin) 在载体平台线程上，无法卸载，严重限制了并发可扩展性。

**JEP 491 解决方案**:
- 重新实现对象监视器 (object monitor)，允许虚拟线程在 `synchronized` 块内阻塞时释放载体线程
- 消除了几乎所有的 pinning 场景
- 唯一剩余的 pin 场景：类初始化器 (`<clinit>`) 执行期间和等待其他线程完成类初始化时

**影响**: 使用 `synchronized` 的现有代码库 (如 JDBC 驱动、传统库) 无需迁移到 `ReentrantLock` 即可充分利用虚拟线程。

> [Loom 时间线](../core/loom/timeline.md)

---

## 5. 代码演进示例

从 JDK 1.0 到 JDK 26，并发编程风格的完整演进。

### 5.1 JDK 1.0: 原始线程

```java
// 手动管理线程生命周期，无法控制并发度
Thread t1 = new Thread(() -> {
    String result = fetchFromService("serviceA");
    // 结果如何传递？需要共享可变状态
});
Thread t2 = new Thread(() -> {
    String result = fetchFromService("serviceB");
});
t1.start();
t2.start();
t1.join();  // 阻塞等待
t2.join();  // 如果 t1 抛异常，t2 仍在运行 -- 资源泄漏
```

### 5.2 JDK 5: ExecutorService + Future

```java
// 线程池抽象，但 Future.get() 仍然阻塞
ExecutorService executor = Executors.newFixedThreadPool(10);
Future<String> f1 = executor.submit(() -> fetchFromService("serviceA"));
Future<String> f2 = executor.submit(() -> fetchFromService("serviceB"));

String r1 = f1.get();  // 阻塞等待
String r2 = f2.get();  // 串行阻塞
executor.shutdown();
// 问题：如果 f1 失败，f2 不会自动取消
```

### 5.3 JDK 8: CompletableFuture

```java
// 异步回调链，但调试困难、错误传播复杂
CompletableFuture<String> cf1 = CompletableFuture
    .supplyAsync(() -> fetchFromService("serviceA"));
CompletableFuture<String> cf2 = CompletableFuture
    .supplyAsync(() -> fetchFromService("serviceB"));

CompletableFuture<String> combined = cf1.thenCombine(cf2,
    (r1, r2) -> r1 + " + " + r2);

combined.thenAccept(System.out::println)
        .exceptionally(ex -> { log(ex); return null; });
// 问题：回调地狱、堆栈跟踪丢失、线程上下文传播复杂
```

### 5.4 JDK 21: Virtual Threads

```java
// 轻量级线程，同步代码风格，百万级并发
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    Future<String> f1 = executor.submit(() -> fetchFromService("serviceA"));
    Future<String> f2 = executor.submit(() -> fetchFromService("serviceB"));

    String result = f1.get() + " + " + f2.get();
    // 每个虚拟线程约 1KB，可轻松创建数百万个
    // 阻塞时自动释放载体线程 (JDK 24 起 synchronized 也不再 pin)
}
```

### 5.5 JDK 25-26: Structured Concurrency + Scoped Values

```java
// 结构化并发：子任务生命周期与父作用域绑定
// 任一失败自动取消其余，堆栈跟踪完整保留

// Scoped Values 传递上下文 (替代 ThreadLocal)
static final ScopedValue<UserContext> USER = ScopedValue.newInstance();

ScopedValue.runWhere(USER, currentUser, () -> {
    try (var scope = StructuredTaskScope.open(
            Joiner.allSuccessfulOrThrow(),  // JDK 25: 静态工厂 + Joiner
            cfg -> cfg.withTimeout(Duration.ofSeconds(5)))) {

        // 子任务自动继承 ScopedValue
        Subtask<String> s1 = scope.fork(() -> fetchFromService("serviceA"));
        Subtask<String> s2 = scope.fork(() -> fetchFromService("serviceB"));

        scope.join();  // 等待所有子任务完成

        String result = s1.get() + " + " + s2.get();
        // 如果任一子任务失败 → 自动取消其余并传播异常
        // 超时 → JDK 26 onTimeout() 可返回回退值
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
| JDK 22-23 | Structured Concurrency (持续预览) | JEP 462, JEP 480 |
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
| JDK 26 | **HTTP/3** (预览) | JEP 517 |

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
├── atomic/                       # 原子类
│   ├── AtomicBoolean.java
│   ├── AtomicInteger.java
│   ├── AtomicLong.java
│   ├── AtomicReference.java
│   └── AtomicReferenceArray.java
├── locks/                        # 锁实现
│   ├── Lock.java
│   ├── ReentrantLock.java
│   ├── ReentrantReadWriteLock.java
│   ├── StampedLock.java          # JDK 8+
│   └── AbstractQueuedSynchronizer.java
├── ExecutorService.java          # 执行器接口
├── ThreadPoolExecutor.java       # 线程池实现
├── ScheduledThreadPoolExecutor.java
├── ForkJoinPool.java             # Fork/Join 池 (虚拟线程载体线程调度器)
├── ForkJoinTask.java
├── CompletableFuture.java        # 异步编程
├── ConcurrentHashMap.java        # 并发 Map
├── ConcurrentLinkedQueue.java
├── StructuredTaskScope.java      # 结构化并发 (JDK 21+)
└── Flow.java                     # Reactive Streams (JDK 9+)

src/java.base/share/classes/java/lang/
├── Thread.java                   # 线程核心类
├── VirtualThread.java            # 虚拟线程 (JDK 21+, 内部)
├── ScopedValue.java              # 作用域值 (JDK 25+ 正式)
└── StableValue.java              # 稳定值 (JDK 25+ 预览)

src/java.net.http/
├── HttpClient.java               # HTTP 客户端
├── HttpRequest.java
├── HttpResponse.java
└── WebSocket.java                # WebSocket 支持

src/java.base/share/classes/java/nio/
├── channels/                     # NIO 通道
│   ├── AsynchronousSocketChannel.java
│   ├── AsynchronousServerSocketChannel.java
│   └── SocketChannel.java
├── ByteBuffer.java               # NIO 缓冲区
└── file/                         # NIO.2 文件 API
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

# 虚拟线程统计
jcmd <pid> VM.native_memory summary

# 结构化并发作用域查看
jcmd <pid> Thread.dump_to_file -format=json -filter=virtual threads.json

# HTTP Client 调试
-Djdk.httpclient.HttpClient.log=errors,requests,headers

# JFR 虚拟线程事件
jcmd <pid> JFR.start name=vthread settings=profile
# 分析事件: jdk.VirtualThreadStart, jdk.VirtualThreadEnd, jdk.VirtualThreadPinned
```

---

## 10. 性能对比指南

### 线程模型吞吐量对比

| 场景 | 平台线程 (池大小 200) | 虚拟线程 | 提升倍数 |
|------|---------------------|----------|----------|
| 10K 并发 HTTP 请求 (I/O 密集) | ~200 req/s (受池限制) | ~8,000+ req/s | ~40x |
| 100K 并发连接保持 | OOM 或拒绝连接 | 正常运行 | N/A |
| CPU 密集型计算 | 与 CPU 核数成正比 | 与 CPU 核数成正比 | ~1x |
| 短生命周期任务 (μs 级) | 线程创建开销大 | 创建开销极低 | ~10x |

### 使用场景推荐

| 场景 | 推荐方案 | 原因 |
|------|----------|------|
| I/O 密集型服务 | Virtual Threads | 阻塞时自动释放载体线程 |
| CPU 密集型计算 | ForkJoinPool / Parallel Stream | 工作窃取算法更高效 |
| 异步事件处理 | CompletableFuture | 回调链式组合 |
| 多子任务聚合 | Structured Concurrency | 自动取消和错误传播 |
| 上下文传递 | ScopedValue (替代 ThreadLocal) | 不可变、自动清理、更低开销 |
| 延迟初始化常量 | StableValue | JVM 常量折叠优化 |
| 发布-订阅数据流 | Flow API (Reactive Streams) | 背压控制 |

### 虚拟线程适用与不适用场景

**适用**:
- Web 服务器请求处理 (thread-per-request 模型)
- 数据库连接和查询
- 微服务间 RPC 调用
- 文件 I/O 操作
- 任何以阻塞 I/O 为主的并发任务

**不适用**:
- 长时间 CPU 密集计算 (不会主动让出载体线程)
- 需要精确控制线程亲和性的场景
- 依赖 `ThreadLocal` 大量可变状态的遗留代码 (建议迁移到 ScopedValue)

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

### 入门路线

1. **Java 并发基础**: [并发编程](concurrency/) -- Thread, synchronized, wait/notify
2. **线程池与工具**: Executor 框架, Lock/Condition, 并发集合 (JSR-166)
3. **异步编程**: CompletableFuture 链式组合, Flow API

### 进阶路线

4. **Virtual Threads**: 虚拟线程原理、调度器、与平台线程对比
5. **Scoped Values**: 替代 ThreadLocal, 不可变上下文传递
6. **Structured Concurrency**: StructuredTaskScope, Joiner, 超时处理

### 深入路线

7. **JEP 491 原理**: 对象监视器重实现、Pin 检测与消除
8. **ForkJoinPool 内部**: 工作窃取算法、虚拟线程载体调度
9. **网络层**: [HTTP 客户端](http/) -- HTTP/2, HTTP/3 (QUIC)
10. **序列化**: [序列化](serialization/) -- 数据交换与安全

### 推荐阅读

- Ron Pressler, [State of Loom](https://cr.openjdk.org/~rpressler/loom/loom/sol1_part1.html)
- [Project Loom 官方页面](https://openjdk.org/projects/loom/)
- [Inside.java Loom 专栏](https://inside.java/tag/loom/)
