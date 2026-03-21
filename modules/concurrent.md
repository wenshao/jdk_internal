# java.util.concurrent 模块分析

> Java 并发工具包，Doug Lea 主导设计的并发编程基础设施

---

## 1. 模块概述

`java.util.concurrent` (JUC) 位于 `java.base` 模块中，是 Java 并发编程的核心工具包。它提供了一套高性能、线程安全的并发工具，替代了早期的同步等待/通知机制。

### 模块定义

**文件**: `src/java.base/share/classes/module-info.java`

```java
module java.base {
    // 并发包
    exports java.util.concurrent;
    exports java.util.concurrent.atomic;
    exports java.util.concurrent.locks;

    // 并发流
    exports java.util.stream;
}
```

### 设计理念

| 原则 | 说明 |
|------|------|
| ** Happens-Before** | 明确的内存可见性保证 |
| **CAS 无锁** | 减少线程阻塞，提高吞吐量 |
| **线程池化** | 复用线程，降低创建开销 |
| **结构化并发** | JDK 21+ 引入，管理并发任务生命周期 |

---

## 2. 包结构

```
java.util.concurrent/
├── atomic/          # 原子类 (CAS 操作)
├── locks/           # 锁框架
├── Executor.java    # 执行器接口
├── ExecutorService.java
├── Executors.java   # 工厂方法
├── ThreadPoolExecutor.java  # 线程池实现
├── ForkJoinPool.java        # 分治线程池
├── CompletableFuture.java   # 异步编程
├── StructuredTaskScope.java # 结构化并发 (JDK 21)
└── ...              # 各种并发集合、同步器
```

---

## 3. 核心类分析

### 3.1 Executor 框架

**源码**: `java.base/share/classes/java/util/concurrent/Executor.java`

```java
public interface Executor {
    void execute(Runnable command);
}
```

**设计目的**: 将任务提交与任务执行解耦

**演进**:
```
Thread (JDK 1.0)
    ↓
Executor (JDK 5)
    ↓
ExecutorService (JDK 5)
    ↓
CompletableFuture (JDK 8)
    ↓
StructuredTaskScope (JDK 21+, Preview)
```

### 3.2 ThreadPoolExecutor

**源码**: `java.base/share/classes/java/util/concurrent/ThreadPoolExecutor.java`

**核心参数**:

| 参数 | 说明 | 默认值 |
|------|------|--------|
| corePoolSize | 核心线程数 | - |
| maximumPoolSize | 最大线程数 | - |
| keepAliveTime | 空闲线程存活时间 | 60s |
| workQueue | 任务队列 | - |
| threadFactory | 线程工厂 | Executors.defaultThreadFactory() |
| handler | 拒绝策略 | AbortPolicy |

**线程创建逻辑**:

```
任务提交
    ↓
当前线程 < corePoolSize?
    ├─ 是 → 创建新线程
    └─ 否 → 队列已满?
              ├─ 是 → 当前线程 < maximumPoolSize?
              │         ├─ 是 → 创建新线程
              │         └─ 否 → 拒绝策略
              └─ 否 → 加入队列
```

**JDK 26 优化**:
- 使用 `SharedThreadContainer` 支持虚拟线程
- 改进任务统计和监控

### 3.3 StructuredTaskScope (结构化并发)

**源码**: `java.base/share/classes/java/util/concurrent/StructuredTaskScope.java`

**JEP**: JEP 453 - Structured Concurrency (Preview)

**核心概念**:

```java
// 传统方式 - 任务生命周期不明确
ExecutorService executor = Executors.newCachedThreadPool();
Future<String> f1 = executor.submit(() -> query(left));
Future<String> f2 = executor.submit(() -> query(right));
// 需要手动管理关闭

// 结构化并发 - 明确的作用域
try (var scope = new StructuredTaskScope<String>()) {
    Subtask<String> subtask1 = scope.fork(() -> query(left));
    Subtask<String> subtask2 = scope.fork(() -> query(right));

    scope.join();  // 等待所有子任务完成

    return new MyResult(subtask1.get(), subtask2.get());
}  // 自动清理所有线程
```

**保证**:
1. 所有子任务必须在 scope 关闭前完成
2. 异常传播和错误处理更清晰
3. 线程泄漏风险降低

### 3.4 ConcurrentHashMap

**演进**:

| JDK | 实现 |
|-----|------|
| 5-6 | 分段锁 (Segment) |
| 7+ | CAS + synchronized (Node 数组) |
| 8 | 优化红黑树转换 |
| 21+ | 支持虚拟线程友好操作 |

**主要方法** (JDK 8+):
```java
// 自 JDK 8 起可用
V computeIfAbsent(K key, Function<? super K, ? extends V> mappingFunction)
V computeIfPresent(K key, BiFunction<? super K, ? super V, ? extends V> remappingFunction)
```

---

## 4. JDK 26 变更

### 4.1 结构化并发

| 特性 | 状态 |
|------|------|
| StructuredTaskScope | Preview |
| ScopedValue | Preview |

### 4.2 虚拟线程集成

所有 JUC 类都已适配虚拟线程:
- `ThreadPerTaskExecutor` 使用虚拟线程
- `ForkJoinPool` 支持虚拟线程工作窃取
- 阻塞操作不再阻塞平台线程

### 4.3 性能改进

- `AtomicLong` 使用 `VarHandle` 优化
- `ConcurrentHashMap` 减少内存占用
- `ThreadPoolExecutor` 统计信息优化

---

## 5. 使用示例

### 5.1 线程池配置

```java
// CPU 密集型
ThreadPoolExecutor cpuBound = new ThreadPoolExecutor(
    Runtime.getRuntime().availableProcessors(),
    Runtime.getRuntime().availableProcessors(),
    0L, TimeUnit.MILLISECONDS,
    new LinkedBlockingQueue<Runnable>()
);

// IO 密集型
ThreadPoolExecutor ioBound = new ThreadPoolExecutor(
    50, 200,
    60L, TimeUnit.SECONDS,
    new LinkedBlockingQueue<Runnable>(1000),
    new ThreadPoolExecutor.CallerRunsPolicy()
);
```

### 5.2 结构化并发

```java
try (var scope = new StructuredTaskScope<Object>()) {
    Subtask<User> userTask = scope.fork(() -> fetchUser(id));
    Subtask<List<Order>> ordersTask = scope.fork(() -> fetchOrders(id));

    scope.join();

    return new UserOrders(userTask.get(), ordersTask.get());
}
```

### 5.3 CompletableFuture 链式调用

```java
CompletableFuture.supplyAsync(() -> fetchUser(id))
    .thenCompose(user -> fetchOrders(user.id))
    .thenApply(orders -> process(orders))
    .exceptionally(ex -> handleError(ex));
```

---

## 6. 性能特性

### 6.1 CAS vs 锁

| 操作 | CAS | synchronized |
|------|-----|--------------|
| 无竞争 | O(1) | O(1) |
| 低竞争 | O(1) | O(1) |
| 高竞争 | 自旋消耗 | 上下文切换 |

### 6.2 线程池选择指南

| 场景 | 推荐 |
|------|------|
| 异步任务 | `newCachedThreadPool()` + 虚拟线程 |
| 并发控制 | `newFixedThreadPool(n)` |
| 定时任务 | `ScheduledThreadPoolExecutor` |
| 分治算法 | `ForkJoinPool` |
| 结构化并发 | `StructuredTaskScope` |

---

## 7. 相关链接

- [JEP 453: Structured Concurrency (Preview)](https://openjdk.org/jeps/453)
- [JEP 444: Virtual Threads](https://openjdk.org/jeps/444)
- [JEP 446: Scoped Values (Preview)](https://openjdk.org/jeps/446)
- [源码](https://github.com/openjdk/jdk/tree/master/src/java.base/share/classes/java/util/concurrent)
