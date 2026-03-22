# Virtual Threads 实践指南

> 何时使用、反模式、从线程池迁移

[← 返回并发编程](README.md)

---

## 1. 什么是 Virtual Threads（虚拟线程）

虚拟线程是轻量级线程，由 JVM 管理调度，不直接绑定 OS 线程。JDK 19 预览 (JEP 425)，JDK 21 正式发布 (JEP 444)。

```
传统线程模型:
  ┌─────────┐  ┌─────────┐  ┌─────────┐
  │Thread 1 │  │Thread 2 │  │Thread 3 │  ← OS 线程 (平台线程)
  └────┬────┘  └────┬────┘  └────┬────┘
       │            │            │
       ▼            ▼            ▼
  ┌──────────────────────────────────────┐
  │       Platform Threads (OS 线程)    │
  └──────────────────────────────────────┘

虚拟线程模型:
  ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐
  │VT1│ │VT2│ │VT3│ │VT4│ │VT5│ │...│  ← 数百万虚拟线程
  └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘ └───┘
    │     │     │     │     │
    └─────┴─────┴──┬──┴─────┘
                   ▼
  ┌──────────────────────────────────────┐
  │   Carrier Threads (ForkJoinPool)    │
  │       (默认: CPU 核心数)            │
  └──────────────────────────────────────┘
```

### 性能对比

| 特性 | 平台线程 (Platform Thread) | 虚拟线程 (Virtual Thread) |
|------|---------------------------|--------------------------|
| 创建成本 | 高 (~1-2ms) | 极低 (~1μs) |
| 内存占用 | ~2MB/线程 | ~KB/线程 |
| 最大数量 | ~数千 | 数百万 |
| 适用场景 | CPU 密集 | I/O 密集 |
| 阻塞操作 | 昂贵（占用 OS 线程） | 便宜（unmount 释放载体线程） |

---

## 2. 何时使用虚拟线程

### 适用场景

```java
// ✅ I/O 密集型任务：HTTP 请求、数据库查询、文件读写
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> httpClient.send(request));
    executor.submit(() -> db.query("SELECT * FROM users"));
    executor.submit(() -> Files.readString(path));
}

// ✅ 高并发服务：每个请求一个虚拟线程
// 传统模型需要 Reactive/异步框架，虚拟线程可用同步代码实现相同吞吐
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000_000; i++) {
        executor.submit(() -> handleRequest());
    }
}

// ✅ 结合 Structured Concurrency（结构化并发）
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    var user = scope.fork(() -> fetchUser(id));
    var orders = scope.fork(() -> fetchOrders(id));
    scope.join();
    scope.throwIfFailed();
    return new UserProfile(user.get(), orders.get());
}
```

### 不适用场景

```java
// ❌ CPU 密集型计算：虚拟线程无优势，应使用 ForkJoinPool
// 虚拟线程的优势在于 I/O 阻塞时释放载体线程
// CPU 密集任务不会阻塞，虚拟线程无法 unmount
ForkJoinPool pool = new ForkJoinPool(Runtime.getRuntime().availableProcessors());
pool.invoke(new RecursiveTask<>() { /* 计算任务 */ });

// ❌ 需要线程池限流的场景：虚拟线程不应池化
// 用 Semaphore 控制并发度
Semaphore semaphore = new Semaphore(100);  // 限制并发度
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> {
        semaphore.acquire();
        try { accessDatabase(); }
        finally { semaphore.release(); }
    });
}
```

---

## 3. 反模式 (Anti-patterns)

### 反模式 1: 池化虚拟线程

```java
// ❌ 不要池化虚拟线程 —— 虚拟线程创建极其廉价
ExecutorService pool = Executors.newFixedThreadPool(100,
    Thread.ofVirtual().factory());  // 错误！

// ✅ 每个任务一个虚拟线程
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
```

### 反模式 2: synchronized 中的阻塞 I/O（JDK 24 前）

```java
// ❌ Pinning: synchronized + 阻塞 I/O（JDK 24 之前）
synchronized (lock) {
    socket.read(buffer);  // 载体线程被 pin，无法复用
}

// ✅ 使用 ReentrantLock 替代
ReentrantLock lock = new ReentrantLock();
lock.lock();
try {
    socket.read(buffer);  // 虚拟线程可 unmount
} finally {
    lock.unlock();
}

// 检测 Pinning:
// -Djdk.tracePinnedThreads=full   打印完整堆栈
// -Djdk.tracePinnedThreads=short  打印摘要
```

> **JDK 24+**: JEP 491 解决了大部分 synchronized pinning 问题，但 JNI 关键区仍会导致 pinning。

### 反模式 3: ThreadLocal 滥用

```java
// ❌ ThreadLocal 在虚拟线程中浪费内存（每个虚拟线程一份副本）
private static final ThreadLocal<String> USER = new ThreadLocal<>();

// ✅ 使用 ScopedValue（JDK 25 正式，JEP 506）
private static final ScopedValue<String> USER = ScopedValue.newInstance();
ScopedValue.where(USER, "alice").run(() -> {
    // 在此作用域内可访问 USER
    processRequest();
});
```

### 反模式 4: 在虚拟线程中使用 StampedLock

```java
// ❌ StampedLock 内部使用忙等待 (busy-wait)，会 pin 虚拟线程
StampedLock lock = new StampedLock();
long stamp = lock.readLock();  // 会 pin

// ✅ 对读多写少场景，使用 ReentrantReadWriteLock 或乐观读
long stamp = lock.tryOptimisticRead();  // 乐观读不 pin
// ... 读取数据 ...
if (!lock.validate(stamp)) {
    // 退化为其他策略
}
```

---

## 4. 从线程池迁移

### 迁移步骤

```java
// 步骤 1: 替换 ExecutorService
// 迁移前
ExecutorService pool = Executors.newFixedThreadPool(200);

// 迁移后
ExecutorService pool = Executors.newVirtualThreadPerTaskExecutor();

// 步骤 2: 如需限流，用 Semaphore 替代线程池大小限制
Semaphore limit = new Semaphore(200);
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (var task : tasks) {
        executor.submit(() -> {
            limit.acquire();
            try { task.run(); }
            finally { limit.release(); }
        });
    }
}

// 步骤 3: 替换 ThreadLocal 为 ScopedValue
// 步骤 4: 检查 synchronized 块中的阻塞 I/O（JDK 24 前需替换为 ReentrantLock）
```

### 同步机制兼容性速查表

| 同步机制 | 虚拟线程兼容性 | 说明 |
|----------|---------------|------|
| **synchronized** | JDK 24 前会 pin | JDK 24+ 通过 JEP 491 解决 |
| **ReentrantLock** | 完全兼容 | 基于 AQS + `LockSupport.park()` |
| **Semaphore** | 完全兼容 | 基于 AQS |
| **CountDownLatch** | 完全兼容 | 基于 AQS |
| **StampedLock** | 会 pin | 内部使用忙等待 (busy-wait) |
| **ThreadLocal** | 功能正常但浪费内存 | 推荐用 ScopedValue 替代 |

### 迁移检查清单

1. 将 `Executors.newFixedThreadPool()` / `newCachedThreadPool()` 替换为 `newVirtualThreadPerTaskExecutor()`
2. 将线程池大小限制改为 `Semaphore` 控制并发度
3. 将 `ThreadLocal` 替换为 `ScopedValue`（JDK 25+）
4. 检查 `synchronized` 块中的阻塞 I/O（JDK 24 前替换为 `ReentrantLock`）
5. 检查第三方库是否使用 `synchronized` + I/O（JDBC 驱动、HTTP 客户端等）
6. 使用 `-Djdk.tracePinnedThreads=short` 运行测试，检测 pinning
7. 使用 JFR 事件 `jdk.VirtualThreadPinned` 监控生产环境

---

**最后更新**: 2026-03-20

[← 返回并发编程](README.md)
