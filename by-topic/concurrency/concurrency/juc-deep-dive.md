# java.util.concurrent 深入

> AQS、ConcurrentHashMap、StampedLock、ForkJoinPool、CompletableFuture 的内部实现

[← 返回并发编程](README.md)

---

## 1. AQS (AbstractQueuedSynchronizer) 原理

AQS 是 `java.util.concurrent` 中大多数同步器（ReentrantLock、Semaphore、CountDownLatch、ReentrantReadWriteLock 等）的基础框架，由 Doug Lea 设计。

### 核心结构

```
核心: volatile int state  ← 同步状态

CLH 变体等待队列 (双向链表):
  HEAD(哨兵) ◄──► Node(T1, WAITING) ◄──► Node(T2, WAITING) ◄──► TAIL(T3)

独占模式 (Exclusive): ReentrantLock, ReentrantReadWriteLock(写)
共享模式 (Shared): Semaphore, CountDownLatch, ReadLock
```

### state 字段语义

| 同步器 | state 含义 |
|--------|-----------|
| **ReentrantLock** | `0` = 无锁，`> 0` = 持有锁（值为重入次数） |
| **Semaphore** | 可用许可数 |
| **CountDownLatch** | 剩余计数 |
| **ReentrantReadWriteLock** | 高 16 位 = 读锁持有数，低 16 位 = 写锁重入数 |

### CLH 队列变体

经典 CLH 锁使用隐式链表（每个节点自旋在前驱的状态上），AQS 改为显式双向链表，支持取消 (cancellation) 和超时 (timeout)。JDK 9+ 的 AQS 重写（由 Doug Lea 完成）将 `Unsafe` 操作替换为 `VarHandle`，但 `prev`/`next` 双向链表结构仍然保留。

### 获取锁的流程（独占模式）

```
acquire(arg):
  1. tryAcquire(arg)          ← 子类实现，CAS 修改 state
  2. 如果失败 → 创建 Node，CAS 加入队列尾部
  3. 在队列中自旋：
     - 如果前驱是 head → 再次 tryAcquire
     - 否则 → park 当前线程 (LockSupport.park)
  4. 被 unpark 后重新尝试获取
```

---

## 2. ConcurrentHashMap 演进

### JDK 7: 分段锁 (Segment)

```
JDK 7: Segment[] (默认 16 个分段)
  每个 Segment 继承 ReentrantLock，内含 HashEntry 数组
  不同 Segment 可并发写入，并发度 = Segment 数量（创建后不可变）
```

### JDK 8+: CAS + synchronized（Node 粒度锁）

```
Node[] table:  [null] [Node→Node→null] [null] [TreeNode→...] ...

put 操作:
  1. hash 定位桶 → 桶为空 → CAS 插入首节点（无锁）
  2. 桶非空 → synchronized(桶头节点) 遍历链表/红黑树插入
  3. 链表长度 >= 8 且 table.length >= 64 → 树化 (treeifyBin)

扩容: 多线程协助迁移 (transfer)，每个线程负责一段桶
size(): 使用 baseCount + CounterCell[] (类似 LongAdder)
```

### 关键改进

- 锁粒度从 Segment（多个桶共享一把锁）细化到单个桶头节点
- 空桶插入使用无锁 CAS，减少锁竞争
- `size()` 使用分散计数器（`CounterCell[]`），避免全局 CAS 热点

---

## 3. StampedLock

**JDK 8 引入**，比 `ReentrantReadWriteLock` 提供更高的并发性能，支持乐观读 (optimistic read)。

### 基本用法

```java
StampedLock lock = new StampedLock();

// 乐观读 - 不阻塞写线程
long stamp = lock.tryOptimisticRead();    // 获取乐观读戳记（非阻塞）
double x = this.x, y = this.y;           // 读取共享数据
if (!lock.validate(stamp)) {             // 验证期间是否有写操作
    // 乐观读失败 → 退化为悲观读锁
    stamp = lock.readLock();
    try {
        x = this.x;
        y = this.y;
    } finally {
        lock.unlockRead(stamp);
    }
}

// 写锁
long stamp = lock.writeLock();
try {
    this.x = newX;
    this.y = newY;
} finally {
    lock.unlockWrite(stamp);
}

// 锁降级: 写锁 → 读锁
long ws = lock.writeLock();
try {
    this.x = newX;
    long rs = lock.tryConvertToReadLock(ws);  // 降级
    if (rs != 0L) {
        ws = rs;  // 降级成功
    } else {
        lock.unlockWrite(ws);
        ws = lock.readLock();
    }
    // 此处持有读锁
} finally {
    lock.unlock(ws);
}
```

### 内部实现

StampedLock 使用一个 `long state` 字段，高位记录写锁状态与版本号，低位记录读锁计数。乐观读只是记录当前版本号，`validate()` 检查版本号是否改变。

### 注意事项

- StampedLock **不可重入** (non-reentrant)
- 不支持 Condition
- 不支持虚拟线程中的 unmount（使用 `readLock()`/`writeLock()` 会 pin 虚拟线程）

---

## 4. ForkJoinPool 深入

### Work-Stealing 算法（工作窃取）

每个工作线程持有一个双端队列 (WorkQueue)：

```
Worker-0 Queue:  [A][B][C][D][E]  ← push/pop 从顶部 (LIFO, 本线程)
                  ↑ steal 从底部 (FIFO, 其他线程)

Worker-1 Queue:  [F][G]
Worker-2 Queue:  [空] ← 从其他 Worker 底部窃取任务
```

**规则**：
- 本线程 push/pop 从队列顶部操作（LIFO）--- 缓存友好
- 窃取从队列底部操作（FIFO）--- 窃取大任务，减少窃取频率
- push/pop 使用无锁操作，steal 需要 CAS

### ManagedBlocker

当 ForkJoinPool 中的任务需要执行阻塞操作（如 I/O）时，使用 `ManagedBlocker` 避免线程饥饿：

```java
// ForkJoinPool.ManagedBlocker 接口
ForkJoinPool.managedBlock(new ForkJoinPool.ManagedBlocker() {
    private boolean done = false;

    @Override
    public boolean block() throws InterruptedException {
        // 执行阻塞操作
        result = blockingCall();
        done = true;
        return true;
    }

    @Override
    public boolean isReleasable() {
        return done;  // 是否已完成或无需阻塞
    }
});
```

**工作机制**：`managedBlock()` 在阻塞前检查是否需要补偿线程。如果当前线程是 ForkJoinPool 的工作线程且池中活跃线程不足，会创建额外的补偿线程 (compensation thread) 以维持并行度。

### Common Pool

`ForkJoinPool.commonPool()` 是 JVM 全局共享的 ForkJoinPool，被 `CompletableFuture`、`parallel()` Stream 等使用：

```java
// 默认并行度 = Runtime.getRuntime().availableProcessors() - 1
// 可通过系统属性调整:
// -Djava.util.concurrent.ForkJoinPool.common.parallelism=16
// -Djava.util.concurrent.ForkJoinPool.common.threadFactory=...

// Common Pool 的生命周期与 JVM 一致，不可 shutdown
ForkJoinPool common = ForkJoinPool.commonPool();
common.shutdown();  // 无效，Common Pool 忽略 shutdown 调用
```

**注意**：所有使用 Common Pool 的代码共享同一组线程，长时间运行的任务会影响其他使用者（如 parallel Stream）。建议为独立的计算密集型任务创建专用 ForkJoinPool。

---

## 5. CompletableFuture 深入

### 完成链 (Completion Chain)

CompletableFuture 内部使用栈式链表 (Completion stack) 管理依赖关系：

```java
CompletableFuture<String> cf1 = supplyAsync(() -> "hello");
CompletableFuture<Integer> cf2 = cf1.thenApply(String::length);
CompletableFuture<Void> cf3 = cf2.thenAccept(System.out::println);
```

```
内部结构 (栈式链表):
  cf1 (result: "hello")  → stack: UniApply(cf2)  → null
  cf2 (result: 5)        → stack: UniAccept(cf3) → null
  cf3 (result: null)

当 cf1 完成时，触发 stack 中所有 Completion 依次执行
```

### thenCompose vs thenApply

```java
// thenApply: 同步转换，Function<T, U>
// 返回 CompletableFuture<U>
CompletableFuture<String> cf = CompletableFuture.supplyAsync(() -> 42)
    .thenApply(n -> "Value: " + n);  // 同步转换

// thenCompose: 异步展平，Function<T, CompletableFuture<U>>
// 类似 flatMap，避免 CompletableFuture<CompletableFuture<U>>
CompletableFuture<String> cf = CompletableFuture.supplyAsync(() -> 42)
    .thenCompose(n -> fetchAsync(n));  // 返回新的 CompletableFuture

// 错误示范: thenApply + 异步操作 → 嵌套 CompletableFuture
CompletableFuture<CompletableFuture<String>> nested =
    CompletableFuture.supplyAsync(() -> 42)
        .thenApply(n -> fetchAsync(n));  // ❌ 嵌套了

// 正确: thenCompose 展平
CompletableFuture<String> flat =
    CompletableFuture.supplyAsync(() -> 42)
        .thenCompose(n -> fetchAsync(n));  // ✅ 展平
```

### 异常处理策略

```java
CompletableFuture<String> cf = CompletableFuture.supplyAsync(() -> {
    if (error) throw new RuntimeException("failed");
    return "ok";
});

// 方式 1: exceptionally - 异常时提供默认值
cf.exceptionally(ex -> "fallback");

// 方式 2: handle - 同时处理正常值和异常（二选一）
cf.handle((result, ex) -> {
    if (ex != null) return "error: " + ex.getMessage();
    return result.toUpperCase();
});

// 方式 3: whenComplete - 无论成功失败都执行，不改变结果
cf.whenComplete((result, ex) -> {
    if (ex != null) log.error("Failed", ex);
    else log.info("Got: " + result);
});

// 异常传播: 链中的异常会沿着完成链传播
CompletableFuture.supplyAsync(() -> { throw new RuntimeException("A"); })
    .thenApply(s -> s + "B")      // 跳过（上游异常）
    .thenApply(s -> s + "C")      // 跳过
    .exceptionally(ex -> "recovered");  // 在这里捕获

// JDK 12+: exceptionallyCompose - 异常时返回新的 CompletableFuture
cf.exceptionallyCompose(ex -> fetchFallbackAsync());
```

---

## 6. 相关 PR 分析

### JDK-8348880: ZoneOffset 缓存优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: +15-25% 时区偏移缓存性能

将 `ZoneOffset.QUARTER_CACHE` 从 `ConcurrentHashMap` 改为 `AtomicReferenceArray`：

- 消除 `int` → `Integer` 自动装箱
- 数组访问比 HashMap 更快
- 内存占用减少 85%

> [详细分析](/by-pr/8348/8348880.md)

---

**最后更新**: 2026-03-20

[← 返回并发编程](README.md)
