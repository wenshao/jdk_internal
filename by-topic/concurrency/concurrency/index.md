# 并发编程

> 从 Thread 到 Virtual Thread 的完整演进历程

[← 返回并发网络](../)

---

## 1. 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 7 ── JDK 8 ── JDK 19 ── JDK 21 ── JDK 23 ── JDK 25 ── JDK 26
   │         │        │        │        │        │        │        │        │
Thread    Executor ForkJoin Stream Virtual Structured Scoped  Lazy    Stable
Runnable  Future   Pool    Parallel Thread  Concurrency Values Constants Values
```

### 核心演进

| 版本 | 特性 | 说明 | 适用场景 |
|------|------|------|----------|
| **JDK 1.0** | Thread, Runnable | 基础线程 | 少量线程 |
| **JDK 5** | Executor 框架 | 线程池、并发集合 | 固定大小线程池 |
| **JDK 7** | Fork/Join 框架 | 工作窃取算法 | 分治任务 |
| **JDK 8** | CompletableFuture | 异步编程 | 组合式异步 |
| **JDK 19** | Virtual Threads (预览) | 轻量级线程 | 大量 I/O 任务 |
| **JDK 21** | Virtual Threads (正式) | 生产就绪 | 高并发服务 |
| **JDK 21** | Scoped Values (预览) | 线程局部变量替代 | 虚拟线程数据传递 |
| **JDK 23** | Structured Concurrency (预览) | 结构化并发 | 任务组管理 |
| **JDK 25** | Lazy Constants (预览) | 延迟初始化常量 | 性能优化 |
| **JDK 26** | Stable Values (预览) | 一次写入语义 | 线程安全 |

---

## 目录

- [基础 API](#2-基础-api)
- [Executor 框架](#3-executor-框架)
- [并发工具](#4-并发工具)
- [Virtual Threads](#5-virtual-threads)
- [Structured Concurrency](#6-structured-concurrency)
- [Scoped Values](#7-scoped-values)
- [最新增强](#8-最新增强)
- [并发调试](#9-并发调试)
- [核心贡献者](#10-核心贡献者)
- [相关链接](#11-相关链接)

### 深入专题

| 专题 | 说明 |
|------|------|
| [synchronized 内部实现](synchronized-internals.md) | Thin Lock / Fat Lock / Mark Word / 锁膨胀与降级 / JEP 374 偏向锁移除 |
| [java.util.concurrent 深入](juc-deep-dive.md) | AQS / ConcurrentHashMap 演进 / StampedLock / ForkJoinPool / CompletableFuture |
| [Virtual Threads 实践指南](virtual-threads-guide.md) | 何时使用 / 反模式 / 从线程池迁移 / 同步机制兼容性 |

---

## 2. 基础 API

### Thread 和 Runnable

**JDK 1.0 引入**

```java
// 创建线程的方式

// 方式 1: 继承 Thread
class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("Thread running");
    }
}

// 方式 2: 实现 Runnable
class MyRunnable implements Runnable {
    @Override
    public void run() {
        System.out.println("Runnable running");
    }
}

// 使用
Thread t1 = new MyThread();
Thread t2 = new Thread(new MyRunnable());
t1.start();
t2.start();
```

**线程状态 (Thread States)**:

```
┌─────────────────────────────────────────────────────────┐
│                   线程生命周期                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│    NEW ──► RUNNABLE ──► TERMINATED                    │
│             │                                          │
│             ▼                                          │
│        BLOCKED (等待锁)                                │
│             │                                          │
│             ▼                                          │
│        WAITING (wait(), join(), park())                 │
│             │                                          │
│             ▼                                          │
│        TIMED_WAITING (sleep(), wait(n))                 │
│             │                                          │
│             └──► 回到 RUNNABLE                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**常用方法**:

```java
Thread.sleep(1000);                    // 线程休眠（毫秒）
thread.join();                         // 等待线程结束
thread.join(1000);                     // 最多等待 1 秒
Thread current = Thread.currentThread(); // 获取当前线程
thread.setPriority(Thread.MAX_PRIORITY); // 线程优先级 (1-10, 默认 5)
thread.setDaemon(true);                // 守护线程
thread.interrupt();                    // 中断线程
```

### happens-before 关系

Java Memory Model (JMM) 定义了 happens-before 关系，保证内存可见性：

| 规则 | 说明 |
|------|------|
| **程序顺序** | 同一线程中，前面的操作 happens-before 后面的操作 |
| **Monitor 锁** | `unlock` happens-before 后续的 `lock` |
| **volatile** | `volatile` 写 happens-before 后续的 `volatile` 读 |
| **Thread.start()** | `start()` happens-before 新线程中的所有操作 |
| **Thread.join()** | 线程中的所有操作 happens-before `join()` 返回 |
| **传递性** | A happens-before B，B happens-before C → A happens-before C |

### volatile 关键字

```java
// volatile 保证可见性和有序性，但不保证原子性
private volatile boolean running = true;

// ✅ 适用：状态标志
// ❌ 不适用：i++ 等复合操作（不是原子的）

// 对于复合操作，使用 Atomic 类
private final AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet();  // 原子性 i++
```

---

## 3. Executor 框架

**JDK 5 引入 (JSR-166)**

### ExecutorService

```java
// 固定大小线程池
ExecutorService fixedPool = Executors.newFixedThreadPool(10);

// 缓存线程池
ExecutorService cachedPool = Executors.newCachedThreadPool();

// 单线程池
ExecutorService singlePool = Executors.newSingleThreadExecutor();

// 提交任务
Future<String> future = fixedPool.submit(() -> {
    Thread.sleep(1000);
    return "Result";
});

// 获取结果
String result = future.get();      // 阻塞等待
String result = future.get(2, TimeUnit.SECONDS);  // 超时等待

// 关闭线程池
fixedPool.shutdown();
fixedPool.awaitTermination(1, TimeUnit.MINUTES);
```

### ThreadPoolExecutor

```java
// 推荐使用 ThreadPoolExecutor 而不是 Executors
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    5,                      // 核心线程数 (corePoolSize)
    10,                     // 最大线程数 (maximumPoolSize)
    60L, TimeUnit.SECONDS,  // 空闲线程存活时间 (keepAliveTime)
    new LinkedBlockingQueue<>(100),  // 工作队列 (workQueue)
    new ThreadFactory() {
        private final AtomicInteger count = new AtomicInteger(0);
        @Override
        public Thread newThread(Runnable r) {
            return new Thread(r, "pool-thread-" + count.incrementAndGet());
        }
    },
    new ThreadPoolExecutor.CallerRunsPolicy()  // 拒绝策略 (RejectedExecutionHandler)
);
```

### Fork/Join 框架

**JDK 7 引入**

```java
// Fork/Join 适用于分治任务 (divide-and-conquer)
class SumTask extends RecursiveTask<Long> {
    private final int[] array;
    private final int start, end;
    private static final int THRESHOLD = 10000;

    @Override
    protected Long compute() {
        if (end - start <= THRESHOLD) {
            long sum = 0;
            for (int i = start; i < end; i++) sum += array[i];
            return sum;
        } else {
            int mid = (start + end) / 2;
            SumTask left = new SumTask(array, start, mid);
            SumTask right = new SumTask(array, mid, end);
            left.fork();  // 异步执行
            return right.compute() + left.join();  // 合并结果
        }
    }
}

ForkJoinPool pool = ForkJoinPool.commonPool();
long sum = pool.invoke(new SumTask(array, 0, array.length));
```

> 更多 ForkJoinPool 内部实现（Work-Stealing、ManagedBlocker、Common Pool）见 [juc-deep-dive.md](juc-deep-dive.md#4-forkjoinpool-深入)

---

## 4. 并发工具

### CompletableFuture

**JDK 8 引入**

```java
// 创建异步任务
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> "Result");

// 转换结果
CompletableFuture<Integer> transformed = future.thenApply(String::length);

// 组合多个任务
CompletableFuture<String> f1 = CompletableFuture.supplyAsync(() -> "Hello");
CompletableFuture<String> f2 = CompletableFuture.supplyAsync(() -> "World");
CompletableFuture<String> combined = f1.thenCombine(f2, (s1, s2) -> s1 + " " + s2);

// 等待多个任务完成
CompletableFuture.allOf(f1, f2).join();

// 异常处理
future.exceptionally(ex -> "Fallback");
```

> CompletableFuture 完成链、thenCompose vs thenApply、异常处理策略见 [juc-deep-dive.md](juc-deep-dive.md#5-completablefuture-深入)

### 并发集合 (Concurrent Collections)

```java
// ConcurrentHashMap - 线程安全的 HashMap
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.compute("key", (k, v) -> v == null ? 1 : v + 1);

// CopyOnWriteArrayList - 读多写少 (copy-on-write)
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();

// BlockingQueue - 阻塞队列 (生产者-消费者模式)
BlockingQueue<String> queue = new LinkedBlockingQueue<>(100);
queue.put("item");   // 满时阻塞
String item = queue.take();  // 空时阻塞

// ConcurrentLinkedQueue - 无锁队列 (lock-free)
ConcurrentLinkedQueue<String> q = new ConcurrentLinkedQueue<>();
```

### 同步工具 (Synchronizers)

```java
// CountDownLatch - 等待多个线程完成 (一次性)
CountDownLatch latch = new CountDownLatch(3);
// ... latch.countDown() in each thread ...
latch.await();

// CyclicBarrier - 多个线程互相等待 (可重用)
CyclicBarrier barrier = new CyclicBarrier(3, () -> {
    System.out.println("All threads reached barrier");
});

// Semaphore - 限制并发访问数
Semaphore semaphore = new Semaphore(10);
semaphore.acquire();
try { /* 受限资源 */ } finally { semaphore.release(); }
```

> AQS 原理、ConcurrentHashMap JDK 7→8 演进、StampedLock 详解见 [juc-deep-dive.md](juc-deep-dive.md)

---

## 5. Virtual Threads

**JDK 19 预览 (JEP 425), JDK 21 正式 (JEP 444)**

虚拟线程是轻量级线程，由 JVM 管理，不直接绑定 OS 线程。适用于 I/O 密集型高并发场景。

### 创建虚拟线程

```java
// 方式 1: 直接创建
Thread vt = Thread.ofVirtual().start(() -> {
    System.out.println("Virtual thread running");
});

// 方式 2: ExecutorService（推荐）
try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000_000; i++) {
        executor.submit(() -> {
            // I/O 操作
        });
    }
}

// 方式 3: Factory
ThreadFactory factory = Thread.ofVirtual().factory();
Thread vt = factory.newThread(() -> System.out.println("Running"));
vt.start();
```

### 性能特性

| 特性 | 平台线程 (Platform Thread) | 虚拟线程 (Virtual Thread) |
|------|---------------------------|--------------------------|
| 创建成本 | 高 (~1-2ms) | 极低 (~1μs) |
| 内存占用 | ~2MB/线程 | ~KB/线程 |
| 最大数量 | ~数千 | 数百万 |
| 适用场景 | CPU 密集 | I/O 密集 |

> 何时使用、反模式、迁移指南见 [virtual-threads-guide.md](virtual-threads-guide.md)

---

## 6. Structured Concurrency

**JDK 21 预览 (JEP 453), JDK 22 第二次预览 (JEP 462)**

结构化并发 (Structured Concurrency) 将不同线程中运行的相关任务组视为单个工作单元。

```java
// StructuredTaskScope - JDK 21+ (预览)
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> user = scope.fork(() -> fetchUser());
    Future<Integer> order = scope.fork(() -> fetchOrder());

    scope.join();           // 等待所有任务
    scope.throwIfFailed();  // 如果有任务失败, 抛出异常

    return new Response(user.resultNow(), order.resultNow());
}

// ShutdownOnSuccess - 返回第一个成功的结果
try (var scope = new StructuredTaskScope.ShutdownOnSuccess<String>()) {
    scope.fork(() -> fetchFromSource1());
    scope.fork(() -> fetchFromSource2());
    scope.join();
    return scope.result();
}
```

---

## 7. Scoped Values

**JDK 21 预览, JDK 25 正式 (JEP 506)**

Scoped Values 是 ThreadLocal 的替代品，更适合虚拟线程。

```java
// 定义 Scoped Value
public static final ScopedValue<String> CURRENT_USER = ScopedValue.newInstance();

// 使用 Scoped Value
ScopedValue.where(CURRENT_USER, "alice").run(() -> {
    System.out.println("User: " + CURRENT_USER.get());  // alice
});
```

### vs ThreadLocal

| 特性 | ThreadLocal | ScopedValue |
|------|-------------|--------------|
| 内存占用 | 每线程一份 | 共享副本 |
| 虚拟线程友好 | 否 (大量内存) | 是 |
| 不可变性 | 可变 | 不可变 (immutable) |
| 作用域 | 线程生命周期 | 显式作用域 (explicit scope) |
| 继承 | 可继承 | 需要显式传递 |

---

## 8. 最新增强

### JDK 25: Lazy Constants

**JEP 526: Lazy Constants (Second Preview)**

```java
// 延迟初始化常量 (提案中的语法，尚未实现)
private static lazy ExpensiveObject CACHE = new ExpensiveObject();
// 首次访问时初始化，线程安全，性能优于双重检查锁
```

### JDK 26: Stable Values

**JEP 502: Stable Values (Preview)**

```java
// StableValue - 线程安全的一次写入
private final StableValue<Logger> logger = StableValue.of();

public Logger getLogger() {
    return logger.orElseSet(() -> Logger.getLogger("MyApp"));
}
```

---

## 9. 并发调试

### Thread Dump 分析

```bash
# 获取 Thread Dump
jcmd <pid> Thread.dump_to_file -format=json output.json   # JDK 21+ JSON 格式
jcmd <pid> Thread.print                                    # 传统文本格式
jstack <pid>                                               # 经典工具
kill -3 <pid>                                              # SIGQUIT
```

**关键状态标识**：
- `BLOCKED (on object monitor)` --- 等待获取 monitor 锁
- `WAITING` / `TIMED_WAITING` --- `wait()`, `park()`, `sleep()` 等
- `waiting to lock <addr>` --- 等待获取的锁对象地址
- `locked <addr>` --- 当前持有的锁对象地址

### 死锁检测 (Deadlock Detection)

```java
// 编程方式检测死锁
ThreadMXBean tmx = ManagementFactory.getThreadMXBean();
long[] deadlockedIds = tmx.findDeadlockedThreads();
if (deadlockedIds != null) {
    ThreadInfo[] infos = tmx.getThreadInfo(deadlockedIds, true, true);
    for (ThreadInfo info : infos) {
        System.err.println(info);
    }
}
```

### JFR 并发事件

Java Flight Recorder (JFR) 提供多种并发相关事件：

| JFR 事件 | 说明 | 默认阈值 |
|----------|------|----------|
| `jdk.JavaMonitorWait` | `Object.wait()` 调用 | 20 ms |
| `jdk.JavaMonitorEnter` | 进入 synchronized 块的等待 | 20 ms |
| `jdk.ThreadPark` | `LockSupport.park()` 调用 | 20 ms |
| `jdk.VirtualThreadPinned` | 虚拟线程被 pin | 20 ms |
| `jdk.VirtualThreadSubmitFailed` | 虚拟线程提交失败 | 无阈值 |

```bash
# 启动 JFR 记录
jcmd <pid> JFR.start settings=profile duration=60s filename=concurrency.jfr

# 分析锁竞争和 Pinning
jfr print --events jdk.JavaMonitorEnter concurrency.jfr
jfr print --events jdk.VirtualThreadPinned concurrency.jfr
```

---

## 10. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 并发基础 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Doug Lea | 65 | SUNY Oswego | JSR-166, ConcurrentHashMap |
| 2 | Alan Bateman | 43 | Oracle | NIO, Thread |
| 3 | Viktor Klang | 29 | Lightbend/Oracle | CompletableFuture |
| 4 | Martin Buchholz | 13 | Google | 并发工具, 算法 |
| 5 | Stuart Marks | 8 | Oracle | 集合, 并发 |

### Thread/Virtual Thread (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Alan Bateman | 43 | Oracle | Virtual Threads 实现 |
| 2 | Serguei Spitsyn | 6 | Oracle | JVMTI, 线程 |
| 3 | Patricio Chilano Mateo | 5 | Oracle | JVM 运行时 |
| 4 | David Holmes | 4 | Oracle | 并发规范 |
| 5 | Mandy Chung | 2 | Oracle | 监控, JFR |

---

## 11. 相关链接

### 内部文档

- [并发时间线](timeline.md) - 详细的历史演进
- [HTTP 客户端](../http/) - HTTP Client API
- [网络编程](../network/) - Socket/NIO

### 深入专题

- [synchronized 内部实现](synchronized-internals.md) - Mark Word / Thin Lock / Fat Lock / 锁膨胀降级
- [java.util.concurrent 深入](juc-deep-dive.md) - AQS / ConcurrentHashMap / StampedLock / ForkJoinPool / CompletableFuture
- [Virtual Threads 实践指南](virtual-threads-guide.md) - 何时使用 / 反模式 / 线程池迁移

### 外部资源

- [JEP 444](/jeps/concurrency/jep-444.md)
- [JEP 453](/jeps/concurrency/jep-453.md)
- [JEP 462](/jeps/concurrency/jep-462.md)
- [JEP 446](/jeps/concurrency/jep-446.md)
- [JEP 506](/jeps/concurrency/jep-506.md)
- [JEP 526](/jeps/tools/jep-526.md)
- [JEP 502](/jeps/performance/jep-502.md)
- [Project Loom](https://openjdk.org/projects/loom/)
- [Inside Java: Project Loom Updates](https://inside.java/2025/02/22/devoxxbelgium-loom-next/)

---

**最后更新**: 2026-03-20

**Sources**:
- [JEP 444](/jeps/concurrency/jep-444.md)
- [JEP 462](/jeps/concurrency/jep-462.md)
- [JEP 506](/jeps/concurrency/jep-506.md)
- [Project Loom and Virtual Threads Best Practices](https://metadesignsolutions.com/reactive-java-2025-project-loom-virtual-threads-best-practices/)
- [Virtual Threads Improvements 2024](https://www.jvm-weekly.com/p/loom-strikes-again-what-improvements)
- [Java Virtual Threads Complete Guide](https://blog.marcnuri.com/java-virtual-threads-project-loom-complete-guide)
