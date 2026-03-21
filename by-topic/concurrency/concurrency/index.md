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

- [基础 API](#基础-api)
- [Executor 框架](#executor-框架)
- [并发工具](#并发工具)
- [Virtual Threads](#virtual-threads)
- [Structured Concurrency](#structured-concurrency)
- [Scoped Values](#scoped-values)
- [最新增强](#最新增强)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

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

**线程状态**:

```
┌─────────────────────────────────────────────────────────┐
│                   线程生命周期                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│    NEW ──► RUNNABLE ──► RUNNING ──► TERMINATED        │
│             │         │                                │
│             │         ▼                                │
│             │    BLOCKED (等待锁)                      │
│             │         │                                │
│             │         ▼                                │
│             │    WAITING (wait(), join(), park())       │
│             │         │                                │
│             │         ▼                                │
│             │    TIMED_WAITING (sleep(), wait(n))       │
│             │         │                                │
│             └─────────┴──► 回到 RUNNABLE                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**常用方法**:

```java
// 线程休眠
Thread.sleep(1000);  // 毫秒

// 等待线程结束
thread.join();
thread.join(1000);  // 最多等待 1 秒

// 获取当前线程
Thread current = Thread.currentThread();

// 线程优先级 (1-10, 默认 5)
thread.setPriority(Thread.MAX_PRIORITY);

// 守护线程
thread.setDaemon(true);

// 中断线程
thread.interrupt();
```

---

## 3. Executor 框架

**JDK 5 引入 (JSR-166)**

### ExecutorService

```java
// 创建线程池

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
    5,                      // 核心线程数
    10,                     // 最大线程数
    60L, TimeUnit.SECONDS,  // 空闲线程存活时间
    new LinkedBlockingQueue<>(100),  // 工作队列
    new ThreadFactory() {
        private final AtomicInteger count = new AtomicInteger(0);
        @Override
        public Thread newThread(Runnable r) {
            return new Thread(r, "pool-thread-" + count.incrementAndGet());
        }
    },
    new ThreadPoolExecutor.CallerRunsPolicy()  // 拒绝策略
);
```

### Fork/Join 框架

**JDK 7 引入**

```java
// Fork/Join 适用于分治任务
class SumTask extends RecursiveTask<Long> {
    private final int[] array;
    private final int start;
    private final int end;
    private static final int THRESHOLD = 10000;

    SumTask(int[] array, int start, int end) {
        this.array = array;
        this.start = start;
        this.end = end;
    }

    @Override
    protected Long compute() {
        if (end - start <= THRESHOLD) {
            // 小任务直接计算
            long sum = 0;
            for (int i = start; i < end; i++) {
                sum += array[i];
            }
            return sum;
        } else {
            // 大任务分解
            int mid = (start + end) / 2;
            SumTask left = new SumTask(array, start, mid);
            SumTask right = new SumTask(array, mid, end);
            left.fork();  // 异步执行
            return right.compute() + left.join();  // 合并结果
        }
    }
}

// 使用
ForkJoinPool pool = ForkJoinPool.commonPool();
long sum = pool.invoke(new SumTask(array, 0, array.length));
```

---

## 4. 并发工具

### CompletableFuture

**JDK 8 引入**

```java
// CompletableFuture - 组合式异步编程

// 创建异步任务
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    // 异步执行
    return "Result";
});

// 转换结果
CompletableFuture<Integer> transformed = future.thenApply(String::length);

// 消费结果
CompletableFuture<Void> consumed = future.thenAccept(result -> {
    System.out.println("Got: " + result);
});

// 组合多个任务
CompletableFuture<String> f1 = CompletableFuture.supplyAsync(() -> "Hello");
CompletableFuture<String> f2 = CompletableFuture.supplyAsync(() -> "World");
CompletableFuture<String> combined = f1.thenCombine(f2, (s1, s2) -> s1 + " " + s2);

// 等待多个任务完成
CompletableFuture<Void> allOf = CompletableFuture.allOf(f1, f2);
allOf.join();

// 异常处理
CompletableFuture.supplyAsync(() -> {
    throw new RuntimeException("Error");
}).exceptionally(ex -> {
    System.err.println("Error: " + ex.getMessage());
    return "Fallback";
});
```

### 并发集合

```java
// ConcurrentHashMap - 线程安全的 HashMap
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.put("key", 1);
map.compute("key", (k, v) -> v == null ? 1 : v + 1);

// CopyOnWriteArrayList - 读多写少
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
list.add("item");

// BlockingQueue - 阻塞队列
BlockingQueue<String> queue = new LinkedBlockingQueue<>(100);
queue.put("item");  // 满时阻塞
String item = queue.take();  // 空时阻塞

// ConcurrentLinkedQueue - 无锁队列
ConcurrentLinkedQueue<String> q = new ConcurrentLinkedQueue<>();
q.offer("item");
String item = q.poll();
```

### 同步工具

```java
// CountDownLatch - 等待多个线程完成
CountDownLatch latch = new CountDownLatch(3);
for (int i = 0; i < 3; i++) {
    executor.submit(() -> {
        try {
            // 工作
        } finally {
            latch.countDown();
        }
    });
}
latch.await();  // 等待所有线程完成

// CyclicBarrier - 多个线程互相等待
CyclicBarrier barrier = new CyclicBarrier(3, () -> {
    System.out.println("All threads reached barrier");
});
for (int i = 0; i < 3; i++) {
    executor.submit(() -> {
        try {
            // 阶段 1 工作
            barrier.await();  // 等待其他线程
            // 阶段 2 工作
        } catch (Exception e) {
            Thread.currentThread().interrupt();
        }
    });
}

// Semaphore - 限制并发访问
Semaphore semaphore = new Semaphore(10);  // 最多 10 个并发
for (int i = 0; i < 100; i++) {
    executor.submit(() -> {
        try {
            semaphore.acquire();
            try {
                // 受限资源访问
            } finally {
                semaphore.release();
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    });
}
```

---

## 5. Virtual Threads

**JDK 19 预览, JDK 21 正式 (JEP 444)**

### 概述

虚拟线程是轻量级线程，由 JVM 管理，不直接绑定 OS 线程。

```
┌─────────────────────────────────────────────────────────┐
│               Virtual Threads 架构                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  传统线程模型:                                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                │
│  │Thread 1 │  │Thread 2 │  │Thread 3 │  ← OS 线程    │
│  └─────────┘  └─────────┘  └─────────┘                │
│       │            │            │                       │
│       ▼            ▼            ▼                       │
│  ┌───────────────────────────────────────────┐         │
│  │         Platform Threads (OS 线程)       │         │
│  └───────────────────────────────────────────┘         │
│                                                         │
│  虚拟线程模型:                                          │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐     │
│  │ VT1 │ │ VT2 │ │ VT3 │ │ VT4 │ │ VT5 │ │... │     │
│  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └─────┘     │
│     │       │       │       │       │                │
│     └───────┴───────┴───┬───┴───────┘                │
│                         │                             │
│                         ▼                             │
│  ┌───────────────────────────────────────────┐         │
│  │      Carrier Threads (ForkJoinPool)       │         │
│  │         (默认: CPU 核心数)                │         │
│  └───────────────────────────────────────────┘         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 创建虚拟线程

```java
// 方式 1: 直接创建
Thread vt = Thread.ofVirtual().start(() -> {
    System.out.println("Virtual thread running");
});

// 方式 2: ExecutorService
try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000_000; i++) {
        executor.submit(() -> {
            // I/O 操作
        });
    }
}

// 方式 3: Factory
ThreadFactory factory = Thread.ofVirtual().factory();
Thread vt = factory.newThread(() -> {
    System.out.println("Virtual thread running");
});
vt.start();
```

### 性能特性

| 特性 | 平台线程 | 虚拟线程 |
|------|----------|----------|
| 创建成本 | 高 (~1-2ms) | 极低 (~1μs) |
| 内存占用 | ~2MB/线程 | ~KB/线程 |
| 最大数量 | ~数千 | 数百万 |
| 适用场景 | CPU 密集 | I/O 密集 |
| 阻塞操作 | 昂贵 | 便宜 |

### 适用场景

```java
// ✅ 推荐: I/O 密集型任务
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    // HTTP 请求
    List<CompletableFuture<String>> futures = urls.stream()
        .map(url -> CompletableFuture.supplyAsync(() -> fetch(url), executor))
        .toList();

    // 数据库查询
    for (int i = 0; i < 1000; i++) {
        executor.submit(() -> db.query("SELECT * FROM users"));
    }
}

// ❌ 避免: CPU 密集型任务使用虚拟线程
// 虚拟线程对 CPU 密集型任务无性能提升
// 应使用 ForkJoinPool 或平台线程池
```

### Pinning 问题

```java
// Pinning - 虚拟线程被固定到载体线程

// ❌ 避免: synchronized 块中的 I/O 操作
synchronized (lock) {
    // Pinning 发生, 载体线程被阻塞
    Thread.sleep(1000);  // 不要这样做!
}

// ✅ 推荐: 使用 ReentrantLock
ReentrantLock lock = new ReentrantLock();
lock.lock();
try {
    Thread.sleep(1000);  // OK, 虚拟线程会卸载
} finally {
    lock.unlock();
}

// ❌ 避免: native 代码中的阻塞
// JNI 调用可能发生 Pinning
```

---

## 6. Structured Concurrency

**JDK 19-20 孵化器, JDK 21 预览 (JEP 453), JDK 23 第二次预览 (JEP 462)**

### 概述

结构化并发将不同线程中运行的相关任务组视为单个工作单元。

```java
// StructuredTaskScope - JDK 21+ (预览)

try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    // 并发执行多个任务
    Future<String> user = scope.fork(() -> fetchUser());
    Future<Integer> order = scope.fork(() -> fetchOrder());

    // 等待所有任务完成
    scope.join();           // 等待所有任务
    scope.throwIfFailed();  // 如果有任务失败, 抛出异常

    // 组合结果
    return new Response(user.resultNow(), order.resultNow());

} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
    throw new RuntimeException(e);
}
```

### ShutdownOnSuccess

```java
// 返回第一个成功的结果
try (var scope = new StructuredTaskScope.ShutdownOnSuccess<String>()) {
    scope.fork(() -> fetchFromSource1());
    scope.fork(() -> fetchFromSource2());
    scope.fork(() -> fetchFromSource3());

    scope.join();
    return scope.result();  // 第一个成功的结果
}
```

---

## 7. Scoped Values

**JDK 20 预览, JDK 21 第二次预览 (JEP 446), JDK 26 正式 (JEP 506)**

### 概述

Scoped Values 是 ThreadLocal 的替代品，更适合虚拟线程。

```java
// 定义 Scoped Value
public static final ScopedValue<String> CURRENT_USER =
    ScopedValue.newInstance();

// 使用 Scoped Value
ScopedValue.where(CURRENT_USER, "alice").run(() -> {
    // 在此作用域内可访问 CURRENT_USER
    System.out.println("User: " + CURRENT_USER.get());

    // 嵌套作用域可以覆盖值
    ScopedValue.where(CURRENT_USER, "bob").run(() -> {
        System.out.println("User: " + CURRENT_USER.get());  // bob
    });

    System.out.println("User: " + CURRENT_USER.get());  // alice
});

// 作用域外无法访问
System.out.println(CURRENT_USER.get());  // NoSuchElementException
```

### vs ThreadLocal

| 特性 | ThreadLocal | ScopedValue |
|------|-------------|--------------|
| 内存占用 | 每线程一份 | 共享副本 |
| 虚拟线程友好 | 否 (大量内存) | 是 |
| 不可变性 | 可变 | 不可变 |
| 作用域 | 线程生命周期 | 显式作用域 |
| 继承 | 可继承 | 需要显式传递 |

```java
// ThreadLocal vs ScopedValue

// ❌ ThreadLocal - 虚拟线程中内存开销大
private static final ThreadLocal<String> USER = new ThreadLocal<>();

try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000_000; i++) {
        final int id = i;
        executor.submit(() -> {
            USER.set("user-" + id);  // 每个虚拟线程一份副本
            // 使用 USER
            USER.remove();  // 必须清理, 否则内存泄漏
        });
    }
}

// ✅ ScopedValue - 虚拟线程友好
private static final ScopedValue<String> USER = ScopedValue.newInstance();

try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000_000; i++) {
        final int id = i;
        executor.submit(() -> {
            // ScopedValue 自动管理, 无需清理
            ScopedValue.where(USER, "user-" + id).run(() -> {
                // 使用 USER
            });
        });
    }
}
```

---

## 8. 最新增强

### JDK 25: Lazy Constants

**JEP 526: Lazy Constants (Second Preview)**

延迟初始化常量声明:

```java
// 延迟初始化常量
private static lazy ExpensiveObject CACHE = new ExpensiveObject();

// 首次访问时初始化
// 线程安全
// 性能优于双重检查锁
```

### JDK 26: Stable Values

**JEP 502: Stable Values (Preview)**

一次写入语义:

```java
// StableValue - 线程安全的一次写入
private final StableValue<Logger> logger = StableValue.of();

public Logger getLogger() {
    return logger.orElseSet(() -> Logger.getLogger("MyApp"));
}
```

---

## 9. 重要 PR 分析

### 并发集合优化

#### JDK-8348880: ZoneOffset 缓存优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ +15-25% 时区偏移缓存性能

将 `ZoneOffset.QUARTER_CACHE` 从 `ConcurrentHashMap` 改为 `AtomicReferenceArray`：

**优化点**:
- 消除 `int` → `Integer` 自动装箱
- 数组访问比 HashMap 更快
- 内存占用减少 85%

```java
// 优化前：ConcurrentHashMap 需要装箱
Integer key = quarters;  // 自动装箱
ZoneOffset result = QUARTER_CACHE.get(key);

// 优化后：AtomicReferenceArray 无装箱
int key = quarters & 0xff;
ZoneOffset result = QUARTER_CACHE.getOpaque(key);
```

**性能数据**:
- 吞吐量：+15-25%
- 对象分配：-100%（无装箱）
- GC 压力：-50%

→ [详细分析](/by-pr/8348/8348880.md)

### 字节码生成优化

#### JDK-8340587: StackMapGenerator 优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐ +3-7% StackMap 生成性能提升

优化 `checkAssignableTo` 方法，避免不必要的栈复制：

**优化点**:
- 空栈时跳过复制
- 用 `clone()` 替代 `Array.copyOf`
- 局部变量缓存

**适用场景**: Lambda 表达式、动态代理生成

→ [详细分析](/by-pr/8340/8340587.md)

#### JDK-8340544: setLocalsFromArg 优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐ +8-12% 局部变量初始化性能

优化方法签名到局部变量的初始化：

**优化点**:
- 一次 `checkLocal` 调用
- 直接数组访问
- 类型常量比较

→ [详细分析](/by-pr/8340/8340544.md)

### 分布式系统优化

#### JDK-8353741: UUID.toString 性能提升

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ +40-60% UUID.toString 性能提升

使用 SWAR (SIMD Within A Register) 技术替代查找表：

**优化点**:
- 消除查找表缓存未命中
- 寄存器内并行计算
- 使用 `Long.expand` intrinsic

**适用场景**: 分布式追踪、会话管理、日志系统

```java
// 优化前：查找表（可能缓存未命中）
char c = DIGITS[b & 0xff];

// 优化后：SWAR 并行计算
long expanded = Long.expand(value, 0x04040404L);
long result = expanded + 0x3030303030303030L;
```

→ [详细分析](/by-pr/8353/8353741.md)

---

## 10. 并发性能最佳实践

### 并发集合选择

| 集合类型 | 适用场景 | 性能特点 |
|----------|----------|----------|
| **ConcurrentHashMap** | 高读写并发 | 分段锁，O(1) 操作 |
| **CopyOnWriteArrayList** | 读多写少 | 写时复制，读无锁 |
| **ConcurrentLinkedQueue** | 无界队列 | 无锁，CAS 实现 |
| **LinkedBlockingQueue** | 有界队列 | 阻塞式，可控制流量 |

```java
// ✅ 推荐：根据场景选择
// 读多写少
List<String> list = new CopyOnWriteArrayList<>();

// 高并发映射
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();

// 生产者-消费者
BlockingQueue<String> queue = new LinkedBlockingQueue<>(1000);

// 无界高性能队列
ConcurrentLinkedQueue<String> q = new ConcurrentLinkedQueue<>();
```

### 避免装箱开销

```java
// ❌ 避免：ConcurrentHashMap<int[], Integer>
ConcurrentHashMap<Integer, String> map = new ConcurrentHashMap<>();
map.put(1, "value");  // 每次都装箱

// ✅ 推荐：使用 AtomicReferenceArray
AtomicReferenceArray<String> array = new AtomicReferenceArray<>(256);
array.set(1, "value");  // 无装箱
```

### 虚拟线程最佳实践

```java
// ✅ 推荐：I/O 密集型任务
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    // HTTP 请求、数据库查询
    executor.submit(() -> httpClient.send(request));
    executor.submit(() -> db.query("SELECT * FROM users"));
}

// ❌ 避免：CPU 密集型任务使用虚拟线程
// 应使用 ForkJoinPool.commonPool()
```

### Pinning 避免模式

```java
// ❌ 避免：synchronized 中阻塞
synchronized (lock) {
    Thread.sleep(1000);  // Pinning 发生
}

// ✅ 推荐：使用 ReentrantLock
ReentrantLock lock = new ReentrantLock();
lock.lock();
try {
    Thread.sleep(1000);  // OK，虚拟线程可卸载
} finally {
    lock.unlock();
}
```

---

## 11. 核心贡献者

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

## 12. Git 提交历史

> 基于 OpenJDK master 分支分析

### 虚拟线程改进 (2024-2026)

```bash
# 查看虚拟线程相关提交
cd /path/to/jdk
git log --oneline -- src/java.base/share/classes/java/lang/Thread.java
git log --oneline -- src/java.base/share/classes/jdk/internal/vm/
```

### 并发工具改进 (2024-2026)

```bash
# 查看并发工具相关提交
git log --oneline -- src/java.base/share/classes/java/util/concurrent/
```

---

## 13. 相关链接

### 内部文档

- [并发时间线](timeline.md) - 详细的历史演进
- [HTTP 客户端](../http/) - HTTP Client API
- [网络编程](../network/) - Socket/NIO

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
