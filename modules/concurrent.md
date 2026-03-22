# java.util.concurrent 并发工具包 (Concurrency Utilities)

> Doug Lea 主导设计的并发编程基础设施，位于 java.base 模块内，共 97 个源文件

---

## 1. 模块概述 (Overview)

`java.util.concurrent` (JUC) 不是独立模块，而是 `java.base` 模块导出的三个包：

**源码**: `src/java.base/share/classes/module-info.java`

```java
module java.base {
    exports java.util.concurrent;
    exports java.util.concurrent.atomic;
    exports java.util.concurrent.locks;
}
```

### 包文件统计 (Source File Counts)

| 包 (Package) | 文件数 | 说明 |
|---|---|---|
| `java.util.concurrent` | 79 | 主包：执行器、并发集合、同步器、结构化并发 |
| `java.util.concurrent.atomic` | 18 | 原子类 (Atomic Classes)：CAS 操作 |
| `java.util.concurrent.locks` | 11 | 锁框架 (Lock Framework)：AQS、ReentrantLock |
| **合计** | **97** | |

### 设计原则 (Design Principles)

| 原则 | 英文 | 说明 |
|---|---|---|
| Happens-Before 语义 | Memory Visibility | 明确的内存可见性保证 |
| CAS 无锁 (Lock-Free) | Compare-And-Swap | 减少线程阻塞，提高吞吐量 |
| 工作窃取 (Work-Stealing) | Fork/Join | ForkJoinPool 负载均衡 |
| 结构化并发 (Structured Concurrency) | Scoped Lifetime | 管理并发任务生命周期 (Preview) |

---

## 2. 完整类清单 (Complete Class Listing)

### 2.1 java.util.concurrent 主包 (Main Package)

**执行器框架 (Executor Framework)**:

| 类/接口 | 类型 | 说明 |
|---|---|---|
| `Executor` | interface | 任务执行器根接口 |
| `ExecutorService` | interface | 生命周期管理的执行器 |
| `ScheduledExecutorService` | interface | 定时/周期任务执行 |
| `AbstractExecutorService` | abstract class | ExecutorService 骨架实现 |
| `ThreadPoolExecutor` | class | 可配置线程池 |
| `ScheduledThreadPoolExecutor` | class | 定时线程池 |
| `ForkJoinPool` | class | 分治/工作窃取线程池 |
| `ForkJoinTask` | abstract class | ForkJoin 任务基类 |
| `ForkJoinWorkerThread` | class | ForkJoin 工作线程 |
| `RecursiveAction` | abstract class | 无返回值分治任务 |
| `RecursiveTask` | abstract class | 有返回值分治任务 |
| `CountedCompleter` | abstract class | 带完成触发的任务 |
| `Executors` | utility class | 执行器工厂方法 |
| `ThreadPerTaskExecutor` | class | 每任务一线程执行器 (虚拟线程适用) |
| `ThreadFactory` | interface | 线程工厂 |
| `RejectedExecutionHandler` | interface | 拒绝策略 |

**异步编程 (Asynchronous Programming)**:

| 类/接口 | 类型 | 说明 |
|---|---|---|
| `Future` | interface | 异步计算结果 |
| `RunnableFuture` | interface | 可运行的 Future |
| `ScheduledFuture` | interface | 可调度的 Future |
| `RunnableScheduledFuture` | interface | 可运行的调度 Future |
| `FutureTask` | class | Future 的标准实现 |
| `CompletableFuture` | class | 可组合的异步编程 |
| `CompletionStage` | interface | 异步计算阶段 |
| `CompletionService` | interface | 完成服务 |
| `ExecutorCompletionService` | class | CompletionService 实现 |
| `Callable` | interface | 有返回值的任务 |

**结构化并发 (Structured Concurrency, Preview)**:

| 类/接口 | 类型 | 说明 |
|---|---|---|
| `StructuredTaskScope` | sealed interface | 结构化任务作用域 |
| `StructuredTaskScope.Subtask` | sealed interface | 子任务句柄 |
| `StructuredTaskScope.Joiner` | interface | 子任务结果汇聚策略 |
| `StructuredTaskScope.Configuration` | sealed interface | 作用域配置 |
| `StructuredTaskScope.FailedException` | class | 子任务失败异常 |
| `StructuredTaskScope.TimeoutException` | class | 作用域超时异常 |
| `StructuredTaskScopeImpl` | class (internal) | 实现类 |
| `Joiners` | class (internal) | 内置 Joiner 实现 |
| `StructureViolationException` | class | 结构违规异常 |

**并发集合 (Concurrent Collections)**:

| 类/接口 | 类型 | 说明 |
|---|---|---|
| `ConcurrentMap` | interface | 并发 Map 接口 |
| `ConcurrentNavigableMap` | interface | 可导航并发 Map |
| `ConcurrentHashMap` | class | 高性能并发哈希表 |
| `ConcurrentSkipListMap` | class | 并发跳表 Map |
| `ConcurrentSkipListSet` | class | 并发跳表 Set |
| `ConcurrentLinkedQueue` | class | 无界非阻塞队列 |
| `ConcurrentLinkedDeque` | class | 无界非阻塞双端队列 |
| `CopyOnWriteArrayList` | class | 写时复制列表 |
| `CopyOnWriteArraySet` | class | 写时复制集合 |

**阻塞队列 (Blocking Queues)**:

| 类/接口 | 类型 | 说明 |
|---|---|---|
| `BlockingQueue` | interface | 阻塞队列接口 |
| `BlockingDeque` | interface | 阻塞双端队列接口 |
| `TransferQueue` | interface | 传输队列接口 |
| `ArrayBlockingQueue` | class | 有界数组阻塞队列 |
| `LinkedBlockingQueue` | class | 可选有界链表阻塞队列 |
| `LinkedBlockingDeque` | class | 可选有界双端阻塞队列 |
| `LinkedTransferQueue` | class | 无界传输队列 |
| `PriorityBlockingQueue` | class | 无界优先级阻塞队列 |
| `SynchronousQueue` | class | 零容量同步队列 |
| `DelayQueue` | class | 延迟元素队列 |
| `Delayed` | interface | 延迟元素接口 |

**同步器 (Synchronizers)**:

| 类/接口 | 类型 | 说明 |
|---|---|---|
| `CountDownLatch` | class | 倒计数门闩 |
| `CyclicBarrier` | class | 循环屏障 |
| `Semaphore` | class | 信号量 |
| `Phaser` | class | 可重用阶段同步器 |
| `Exchanger` | class | 线程间数据交换 |

**响应式流 (Reactive Streams)**:

| 类/接口 | 类型 | 说明 |
|---|---|---|
| `Flow` | class | 响应式流接口容器 (Publisher/Subscriber/Subscription/Processor) |
| `SubmissionPublisher` | class | Flow.Publisher 实现 |

**调度 (Scheduling)**:

| 类/接口 | 类型 | 说明 |
|---|---|---|
| `DelayScheduler` | class (internal) | ForkJoinPool 延迟调度线程 |

**工具/异常 (Utilities & Exceptions)**:

| 类 | 说明 |
|---|---|
| `TimeUnit` | 时间单位枚举 |
| `ThreadLocalRandom` | 线程本地随机数 |
| `Helpers` | 内部工具类 |
| `ExecutionException` | 执行异常 |
| `CancellationException` | 取消异常 |
| `TimeoutException` | 超时异常 |
| `RejectedExecutionException` | 拒绝执行异常 |
| `BrokenBarrierException` | 屏障破坏异常 |
| `CompletionException` | 完成异常 |

### 2.2 java.util.concurrent.atomic 原子包 (18 files)

| 类 | 说明 |
|---|---|
| `AtomicBoolean` | 原子布尔值 |
| `AtomicInteger` | 原子整数 |
| `AtomicLong` | 原子长整数 |
| `AtomicReference<V>` | 原子引用 |
| `AtomicIntegerArray` | 原子整数数组 |
| `AtomicLongArray` | 原子长整数数组 |
| `AtomicReferenceArray<E>` | 原子引用数组 |
| `AtomicIntegerFieldUpdater<T>` | 整数字段原子更新器 |
| `AtomicLongFieldUpdater<T>` | 长整数字段原子更新器 |
| `AtomicReferenceFieldUpdater<T,V>` | 引用字段原子更新器 |
| `AtomicMarkableReference<V>` | 带标记的原子引用 |
| `AtomicStampedReference<V>` | 带版本号的原子引用 (解决 ABA 问题) |
| `LongAdder` | 高竞争长整数累加器 |
| `LongAccumulator` | 高竞争长整数累积器 |
| `DoubleAdder` | 高竞争双精度累加器 |
| `DoubleAccumulator` | 高竞争双精度累积器 |
| `Striped64` | LongAdder/DoubleAdder 的内部基类 |

### 2.3 java.util.concurrent.locks 锁包 (11 files)

| 类/接口 | 说明 |
|---|---|
| `Lock` | 锁接口 |
| `ReadWriteLock` | 读写锁接口 |
| `Condition` | 条件变量接口 |
| `ReentrantLock` | 可重入锁 |
| `ReentrantReadWriteLock` | 可重入读写锁 |
| `StampedLock` | 乐观读锁 (JDK 8+) |
| `LockSupport` | 线程阻塞/唤醒工具 (park/unpark) |
| `AbstractOwnableSynchronizer` | 同步器所有权基类 |
| `AbstractQueuedSynchronizer` (AQS) | 队列同步器框架 |
| `AbstractQueuedLongSynchronizer` | 长状态值的 AQS |

---

## 3. 核心类深入分析 (Key Class Deep Dive)

### 3.1 AbstractQueuedSynchronizer (AQS)

**源码**: `src/java.base/share/classes/java/util/concurrent/locks/AbstractQueuedSynchronizer.java`

AQS 是 JUC 锁框架的核心基础设施。ReentrantLock、Semaphore、CountDownLatch、ReentrantReadWriteLock 均基于 AQS 实现。

**核心机制**:
- `state` (int)：同步状态，通过 CAS 修改
- CLH 变体等待队列：FIFO 双向链表，节点代表等待线程
- `acquire/release`：模板方法模式，子类实现 `tryAcquire/tryRelease`

```
AQS 内部结构:
┌──────────────────────────────────────────────────┐
│  state (volatile int)                            │
│  通过 compareAndSetState(expect, update) 修改      │
├──────────────────────────────────────────────────┤
│  CLH 等待队列 (Wait Queue)                        │
│  head ← Node ↔ Node ↔ Node → tail               │
│  每个 Node 持有一个等待线程引用                      │
└──────────────────────────────────────────────────┘
```

**子类实现模式**:

| 同步组件 | tryAcquire 语义 | state 含义 |
|---|---|---|
| ReentrantLock | 获取锁 | 重入计数 |
| Semaphore | 获取许可 | 剩余许可数 |
| CountDownLatch | 始终失败 (等待 countDown) | 剩余计数 |
| ReentrantReadWriteLock | 获取读/写锁 | 高 16 位读，低 16 位写 |

### 3.2 ForkJoinPool 分治线程池

**源码**: `src/java.base/share/classes/java/util/concurrent/ForkJoinPool.java`

```java
public class ForkJoinPool extends AbstractExecutorService
    implements ScheduledExecutorService   // 现在也支持调度！
```

**工作窃取算法 (Work-Stealing)**:

```
┌────────────────────────────────────────────────┐
│ ForkJoinPool                                   │
│                                                │
│  Worker-0: [task3, task2, task1] ← 自己从尾部取  │
│  Worker-1: [task6, task5]                      │
│  Worker-2: [] ← 空闲，从 Worker-0 头部"窃取"     │
│  Worker-3: [task7]                             │
│                                                │
│  每个 Worker 有自己的双端队列 (deque)              │
│  自己 LIFO 取，窃取 FIFO 取                      │
└────────────────────────────────────────────────┘
```

**关键特性**:
- `commonPool()`: 全局共享池，`parallelStream()` 和 `CompletableFuture` 默认使用
- 默认并行度 = `Runtime.getRuntime().availableProcessors() - 1`
- 支持 `ManagedBlocker` 接口实现阻塞补偿
- 现已实现 `ScheduledExecutorService`，内部使用 `DelayScheduler` 线程

### 3.3 CompletableFuture 异步编程

**源码**: `src/java.base/share/classes/java/util/concurrent/CompletableFuture.java`

```java
public class CompletableFuture<T> implements Future<T>, CompletionStage<T>
```

**异步组合模式 (Composition Patterns)**:

```
thenApply(fn)         同步转换 (Map)
thenApplyAsync(fn)    异步转换
thenCompose(fn)       异步扁平映射 (FlatMap)
thenCombine(cf, fn)   两个 CF 结果合并
allOf(cfs...)         等待所有完成
anyOf(cfs...)         等待任一完成
exceptionally(fn)     异常恢复
handle(fn)            结果+异常处理
whenComplete(action)  完成时回调
```

**内部实现**: 使用 Treiber 栈管理依赖链，完成时触发栈中所有依赖动作。

### 3.4 StructuredTaskScope 结构化并发 (Preview)

**源码**: `src/java.base/share/classes/java/util/concurrent/StructuredTaskScope.java`
**版权**: Copyright (c) 2021, 2026, Oracle — 标注 `@PreviewFeature`

```java
public sealed interface StructuredTaskScope<T, R>
    extends AutoCloseable
```

**核心 API**:

```java
// 打开作用域
StructuredTaskScope<String, List<String>> scope =
    StructuredTaskScope.open(Joiner.allSuccessfulOrThrow());

// fork 子任务
Subtask<String> sub1 = scope.fork(() -> query(left));
Subtask<String> sub2 = scope.fork(() -> query(right));

// 等待所有子任务
scope.join();          // 阻塞直到 Joiner 决定完成
List<String> result = scope.result();  // 获取汇聚结果

scope.close();         // 清理所有线程
```

**内置 Joiner 策略** (在 `Joiners` 内部类中实现):

| Joiner | 行为 |
|---|---|
| `allSuccessfulOrThrow()` | 收集所有成功结果，任一失败则抛出异常 |
| `anySuccessfulResultOrThrow()` | 返回第一个成功结果，取消其余 |
| `awaitAllSuccessfulOrThrow()` | 等待所有成功，返回 Void |
| `allSubtasks()` | 收集所有 Subtask (含失败)，不取消任何任务 |

**与传统方式对比**:

```
传统 ExecutorService:         结构化并发:
┌──────────────────┐        ┌──────────────────┐
│ submit task1     │        │ try (scope) {    │
│ submit task2     │        │   fork task1     │
│ ... 可能忘记关闭 │        │   fork task2     │
│ shutdown?        │        │   join()         │
└──────────────────┘        │ } // 自动清理     │
                            └──────────────────┘
```

### 3.5 ConcurrentHashMap 并发哈希表

**源码**: `src/java.base/share/classes/java/util/concurrent/ConcurrentHashMap.java`

**数据结构演进**:

| JDK 版本 | 实现方式 |
|---|---|
| JDK 5-6 | 分段锁 Segment (默认 16 段) |
| JDK 7 | 改进分段锁 |
| JDK 8+ | CAS + synchronized (Node 数组 + 链表/红黑树) |

**JDK 8+ 内部结构**:

```
table (Node<K,V>[])
├── [0] → null
├── [1] → Node → Node → Node  (链表, 长度 < 8)
├── [2] → TreeBin → TreeNode  (红黑树, 链表长度 >= 8 且表容量 >= 64)
├── [3] → ForwardingNode      (正在扩容时的转发节点)
└── ...
```

**并行批量操作 (JDK 8+)**: `forEach`, `search`, `reduce` 支持并行阈值参数。

---

## 4. ThreadPoolExecutor 线程池详解

**源码**: `src/java.base/share/classes/java/util/concurrent/ThreadPoolExecutor.java`

**核心参数 (Core Parameters)**:

| 参数 | 类型 | 说明 |
|---|---|---|
| `corePoolSize` | int | 核心线程数 |
| `maximumPoolSize` | int | 最大线程数 |
| `keepAliveTime` | long | 非核心线程空闲存活时间 |
| `workQueue` | BlockingQueue | 任务等待队列 |
| `threadFactory` | ThreadFactory | 线程创建工厂 |
| `handler` | RejectedExecutionHandler | 拒绝策略 (Rejection Policy) |

**任务提交流程 (Task Submission Flow)**:

```
任务提交 execute(Runnable)
    │
    ├─ 当前线程数 < corePoolSize → 创建核心线程
    │
    ├─ workQueue.offer(task) 成功 → 加入队列等待
    │
    ├─ 当前线程数 < maximumPoolSize → 创建非核心线程
    │
    └─ handler.rejectedExecution() → 执行拒绝策略
```

**内置拒绝策略 (Built-in Rejection Policies)**:

| 策略 | 行为 |
|---|---|
| `AbortPolicy` (默认) | 抛出 RejectedExecutionException |
| `CallerRunsPolicy` | 调用者线程执行任务 |
| `DiscardPolicy` | 静默丢弃 |
| `DiscardOldestPolicy` | 丢弃队列头部最旧任务 |

**Executors 工厂方法**:

| 方法 | 核心/最大 | 队列 | 适用场景 |
|---|---|---|---|
| `newFixedThreadPool(n)` | n/n | LinkedBlockingQueue | 固定并发控制 |
| `newCachedThreadPool()` | 0/MAX | SynchronousQueue | 短期异步任务 |
| `newSingleThreadExecutor()` | 1/1 | LinkedBlockingQueue | 顺序执行 |
| `newScheduledThreadPool(n)` | n/MAX | DelayedWorkQueue | 定时任务 |
| `newVirtualThreadPerTaskExecutor()` | - | - | 虚拟线程 (JDK 21+) |

---

## 5. 虚拟线程集成 (Virtual Thread Integration)

JDK 21 引入虚拟线程后，JUC 的多个组件进行了适配：

| 组件 | 虚拟线程适配 |
|---|---|
| `ThreadPerTaskExecutor` | 为虚拟线程设计的执行器 |
| `ForkJoinPool` | commonPool 支持虚拟线程工作窃取 |
| `ReentrantLock` | 虚拟线程阻塞时释放载体线程 (carrier thread) |
| `Semaphore` | 虚拟线程友好的许可获取 |
| `StructuredTaskScope` | fork 创建虚拟线程执行子任务 |
| 阻塞队列 | 阻塞操作不再固定 (pin) 载体线程 |

---

## 6. 性能特性 (Performance Characteristics)

### 6.1 CAS vs synchronized vs StampedLock

| 场景 | AtomicLong (CAS) | synchronized | StampedLock |
|---|---|---|---|
| 无竞争 | 极快 | 偏向锁级别 | 极快 |
| 低竞争 | 快 | 轻量级锁 | 快 (乐观读) |
| 高竞争 | 自旋消耗 CPU | 上下文切换 | 需回退 |
| 高竞争累加 | 用 LongAdder | - | - |

### 6.2 并发集合选择指南 (Collection Selection Guide)

| 需求 | 推荐 |
|---|---|
| 高频读/低频写 Map | `ConcurrentHashMap` |
| 需要排序的并发 Map | `ConcurrentSkipListMap` |
| 高频读/极低频写 List | `CopyOnWriteArrayList` |
| 生产者-消费者 | `LinkedBlockingQueue` 或 `ArrayBlockingQueue` |
| 多生产者-单消费者 | `LinkedTransferQueue` |
| 延迟执行 | `DelayQueue` |
| 线程间交换 | `SynchronousQueue` |

### 6.3 线程池选择指南 (Thread Pool Selection)

| 场景 | 推荐 |
|---|---|
| CPU 密集型计算 | `ForkJoinPool` (并行度 = CPU 核心数) |
| IO 密集型任务 | 虚拟线程 `newVirtualThreadPerTaskExecutor()` |
| 定时/周期任务 | `ScheduledThreadPoolExecutor` 或 `ForkJoinPool` (新增调度能力) |
| 结构化并发子任务 | `StructuredTaskScope` |
| 固定并发控制 | `ThreadPoolExecutor` + 有界队列 |

---

## 7. 使用示例 (Usage Examples)

### 7.1 结构化并发 (JDK 21+ Preview)

```java
// 使用 allSuccessfulOrThrow Joiner
try (var scope = StructuredTaskScope.open(
        Joiner.<String>allSuccessfulOrThrow())) {
    Subtask<String> user = scope.fork(() -> fetchUser(id));
    Subtask<String> orders = scope.fork(() -> fetchOrders(id));
    scope.join();
    List<String> results = scope.result();
}

// 使用 anySuccessfulResultOrThrow (竞速模式)
try (var scope = StructuredTaskScope.open(
        Joiner.<String>anySuccessfulResultOrThrow())) {
    scope.fork(() -> queryMirror1(req));
    scope.fork(() -> queryMirror2(req));
    scope.join();
    String fastest = scope.result();  // 第一个成功的结果
}
```

### 7.2 CompletableFuture 组合

```java
CompletableFuture<User> userFuture =
    CompletableFuture.supplyAsync(() -> fetchUser(id));
CompletableFuture<List<Order>> ordersFuture =
    CompletableFuture.supplyAsync(() -> fetchOrders(id));

CompletableFuture<UserProfile> profile =
    userFuture.thenCombine(ordersFuture,
        (user, orders) -> new UserProfile(user, orders));

profile.exceptionally(ex -> {
    log.warning("Failed: " + ex.getMessage());
    return UserProfile.empty();
});
```

### 7.3 ForkJoin 分治任务

```java
class SumTask extends RecursiveTask<Long> {
    private final long[] array;
    private final int lo, hi;
    static final int THRESHOLD = 10_000;

    protected Long compute() {
        if (hi - lo < THRESHOLD) {
            long sum = 0;
            for (int i = lo; i < hi; i++) sum += array[i];
            return sum;
        }
        int mid = (lo + hi) >>> 1;
        SumTask left = new SumTask(array, lo, mid);
        left.fork();
        SumTask right = new SumTask(array, mid, hi);
        return right.compute() + left.join();
    }
}
```

---

## 8. 相关链接 (References)

- [JEP 505: Structured Concurrency (Fifth Preview)](https://openjdk.org/jeps/505)
- [JEP 444: Virtual Threads](https://openjdk.org/jeps/444)
- [JEP 487: Scoped Values (Fifth Preview)](https://openjdk.org/jeps/487)
- [源码路径](https://github.com/openjdk/jdk/tree/master/src/java.base/share/classes/java/util/concurrent)
- 本地源码: `src/java.base/share/classes/java/util/concurrent/`
