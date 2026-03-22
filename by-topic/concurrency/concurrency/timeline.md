# 并发编程演进时间线

从 Thread 到 Virtual Thread 的演进历程。

---
## 目录

1. [时间线概览](#1-时间线概览)
2. [并发编程模型演进](#2-并发编程模型演进)
3. [Thread 基础](#3-thread-基础)
4. [Executor 框架 (JDK 5, JSR-166)](#4-executor-框架-jdk-5-jsr-166)
5. [Fork/Join 框架 (JDK 7, JSR-166y)](#5-forkjoin-框架-jdk-7-jsr-166y)
6. [CompletableFuture (JDK 8, JEP 107)](#6-completablefuture-jdk-8-jep-107)
7. [Flow API (JDK 9, JEP 266)](#7-flow-api-jdk-9-jep-266)
8. [虚拟线程 (Virtual Threads)](#8-虚拟线程-virtual-threads)
9. [Scoped Values](#9-scoped-values)
10. [Structured Concurrency](#10-structured-concurrency)
11. [并发工具选择指南](#11-并发工具选择指南)
12. [性能对比](#12-性能对比)
13. [最佳实践](#13-最佳实践)
14. [时间线总结](#14-时间线总结)
15. [相关链接](#15-相关链接)

---


## 1. 时间线概览

```
JDK 5 ───── JDK 7 ───── JDK 8 ───── JDK 9 ───── JDK 19 ───── JDK 21 ───── JDK 26
 │              │              │              │              │              │
Executor       Fork/Join      CompletableFuture  Reactive      Virtual       Structured
框架            框架           改进             Streams        Threads 正式    Concurrency
(JSR-166)     (JSR-166y)     (JEP 107)       (JEP 266)      (JEP 444)      (第六次预览)
                                                                        (JEP 493)
```

---

## 2. 并发编程模型演进

```
┌─────────────────────────────────────────────────────────┐
│               并发编程模型演进                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 线程-per-请求 (JDK 1.0-5)                           │
│     ├── Thread                                         │
│     └── Runnable                                       │
│                                                         │
│  2. 线程池 (JDK 5)                                      │
│     ├── ExecutorService                                │
│     └── ThreadPoolExecutor                              │
│                                                         │
│  3. 异步编程 (JDK 8)                                    │
│     ├── CompletableFuture                              │
│     └── CompletionStage                                │
│                                                         │
│  4. 响应式编程 (JDK 9)                                  │
│     └── Flow API                                       │
│                                                         │
│  5. 虚拟线程 (JDK 21)                                   │
│     ├── Virtual Threads                                │
│     └── Structured Concurrency                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Thread 基础

### JDK 1.0 - Thread 类引入

```java
// 传统线程创建
Thread thread = new Thread(() -> {
    System.out.println("Hello from thread");
});
thread.start();
thread.join();  // 等待线程结束

// 线程属性
Thread.currentThread().getName();     // 线程名
Thread.currentThread().getPriority(); // 优先级 (1-10)
Thread.currentThread().isAlive();     // 是否存活
```

**特点**：
- 1:1 映射到操作系统线程
- 创建成本高 (~1MB 栈内存)
- 上下文切换开销大 (~10-100μs)
- 数量受限 (~几千个)

### JDK 1.2 - ThreadLocal

```java
// 线程局部变量
private static final ThreadLocal<User> CURRENT_USER = ThreadLocal.withInitial(() -> null);

// 设置值
CURRENT_USER.set(new User("alice"));

// 获取值
User user = CURRENT_USER.get();

// 清理 (重要!)
CURRENT_USER.remove();
```

**问题**：
- 内存泄漏风险 (必须手动 remove)
- 虚拟线程中效率低
- 不可变，不支持值传递

---

## 4. Executor 框架 (JDK 5, JSR-166)

### 基础用法

```java
// 创建线程池
ExecutorService executor = Executors.newFixedThreadPool(10);
ExecutorService executor = Executors.newCachedThreadPool();
ExecutorService executor = Executors.newSingleThreadExecutor();

// 提交任务
Future<String> future = executor.submit(() -> {
    Thread.sleep(1000);
    return "result";
});

// 获取结果 (阻塞)
String result = future.get();

// 获取结果 (带超时)
String result = future.get(5, TimeUnit.SECONDS);

// 取消任务
future.cancel(true);
```

### ThreadPoolExecutor 原理

```
┌─────────────────────────────────────────────────────────┐
│              ThreadPoolExecutor 架构                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────┐    ┌─────────────────┐    ┌─────────┐    │
│  │ 新任务   │───>│   Core Pool     │───>│ 任务队列 │    │
│  └─────────┘    │   (核心线程)     │    └─────────┘    │
│                 └─────────────────┘         │           │
│                                           │            │
│                         ┌─────────────────┘            │
│                         ▼                              │
│                 ┌─────────────────┐                    │
│                 │   Maximum Pool  │                    │
│                 │   (最大线程)     │                    │
│                 └─────────────────┘                    │
│                         │                              │
│                         ▼                              │
│                 ┌─────────────────┐                    │
│                 │   拒绝策略       │                    │
│                 └─────────────────┘                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 自定义线程池

```java
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    4,                      // corePoolSize (核心线程数)
    20,                     // maximumPoolSize (最大线程数)
    60L, TimeUnit.SECONDS,  // keepAliveTime
    new LinkedBlockingQueue<>(100),  // workQueue
    new ThreadFactory() {   // threadFactory
        private final AtomicInteger counter = new AtomicInteger(0);
        @Override
        public Thread newThread(Runnable r) {
            return new Thread(r, "worker-" + counter.incrementAndGet());
        }
    },
    new ThreadPoolExecutor.CallerRunsPolicy()  // handler (拒绝策略)
);

// 拒绝策略
// - CallerRunsPolicy: 由调用线程执行
// - AbortPolicy: 抛异常 (默认)
// - DiscardPolicy: 静默丢弃
// - DiscardOldestPolicy: 丢弃最老的任务
```

---

## 5. Fork/Join 框架 (JDK 7, JSR-166y)

### 工作窃取 (Work Stealing)

```
┌─────────────────────────────────────────────────────────┐
│              Fork/Join 工作窃取                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Thread 1         Thread 2         Thread 3            │
│  ┌──────┐         ┌──────┐         ┌──────┐            │
│  │ Task │         │ Task │         │      │            │
│  │ Task │         │ Task │         │(空)  │←───┐       │
│  │ Task │         │(空)  │         │      │     │       │
│  └──────┘         └──────┘         └──────┘     │       │
│     ▲                                   │       │       │
│     └───────────────────────────────────┴───────┘       │
│                    窃取任务                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### ForkJoinTask 使用

```java
class Fibonacci extends RecursiveTask<Integer> {
    private final int n;

    Fibonacci(int n) { this.n = n; }

    @Override
    protected Integer compute() {
        if (n <= 1) return n;

        // 创建子任务
        Fibonacci f1 = new Fibonacci(n - 1);
        Fibonacci f2 = new Fibonacci(n - 2);

        // 异步执行 f1
        f1.fork();

        // 同步执行 f2，然后等待 f1
        return f2.compute() + f1.join();
    }
}

// 使用
ForkJoinPool pool = ForkJoinPool.commonPool();
int result = pool.invoke(new Fibonacci(10));
```

### 并行流底层

```java
// 并行流使用 ForkJoinPool.commonPool()
List<Integer> result = IntStream.range(0, 1000)
    .parallel()  // 使用 commonPool
    .map(x -> x * 2)
    .boxed()
    .toList();

// 查看 commonPool 并行度
System.out.println(ForkJoinPool.getCommonPoolParallelism());
// 默认 = CPU 核心数 - 1
```

---

## 6. CompletableFuture (JDK 8, JEP 107)

### 基础用法

```java
// 创建
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    return "result";
});

// 链式调用
CompletableFuture.supplyAsync(() -> fetchUser())
    .thenCompose(user -> fetchOrders(user))  // 依赖上一步结果
    .thenApply(orders -> process(orders))    // 转换结果
    .thenAccept(result -> save(result))      // 消费结果
    .exceptionally(e -> {
        log.error("Failed", e);
        return fallback;
    });
```

### 组合多个 Future

```java
// allOf - 全部完成
CompletableFuture<Void> all = CompletableFuture.allOf(
    supplyAsync(() -> task1()),
    supplyAsync(() -> task2()),
    supplyAsync(() -> task3())
);

all.thenRun(() -> System.out.println("All done"));

// anyOf - 任一完成
CompletableFuture<Object> any = CompletableFuture.anyOf(
    supplyAsync(() -> task1()),
    supplyAsync(() -> task2())
);

any.thenAccept(result -> System.out.println("First: " + result));

// 组合结果
CompletableFuture<String> f1 = supplyAsync(() -> "Hello");
CompletableFuture<String> f2 = supplyAsync(() -> "World");

f1.thenCombine(f2, (s1, s2) -> s1 + " " + s2)
  .thenAccept(System.out::println);
```

### 自定义线程池

```java
ExecutorService executor = Executors.newFixedThreadPool(10);

CompletableFuture.supplyAsync(() -> task(), executor)
    .thenApplyAsync(result -> process(result), executor)
    .thenAcceptAsync(result -> save(result), executor);
```

---

## 7. Flow API (JDK 9, JEP 266)

### 响应式流

```java
// 发布者
SubmissionPublisher<String> publisher = new SubmissionPublisher<>();

// 订阅者
publisher.subscribe(new Subscriber<>() {
    private Subscription subscription;

    @Override
    public void onSubscribe(Subscription sub) {
        this.subscription = sub;
        sub.request(1);  // 请求数据
    }

    @Override
    public void onNext(String item) {
        System.out.println("Received: " + item);
        subscription.request(1);  // 继续请求
    }

    @Override
    public void onError(Throwable t) {
        t.printStackTrace();
    }

    @Override
    public void onComplete() {
        System.out.println("Done");
    }
});

// 发布数据
publisher.submit("Hello");
publisher.submit("World");
publisher.close();
```

### 处理器 (Processor)

```java
class TransformProcessor<T, R> extends SubmissionPublisher<R>
    implements Processor<T, R> {

    @Override
    public void onSubscribe(Subscription sub) {
        sub.request(Long.MAX_VALUE);
    }

    @Override
    public void onNext(T item) {
        submit(transform(item));  // 转换并提交
    }

    @Override
    public void onError(Throwable t) {
        t.printStackTrace();
    }

    @Override
    public void onComplete() {
        close();
    }

    private R transform(T item) {
        // 转换逻辑
        return (R) (item.toString().toUpperCase());
    }
}
```

---

## 8. 虚拟线程 (Virtual Threads)

### 演进历程

| 版本 | 状态 | JEP |
|------|------|-----|
| JDK 19 | 预览 | JEP 425 |
| JDK 20 | 第二次预览 | JEP 436 |
| JDK 21 | **正式版** | JEP 444 |

### 虚拟线程原理

```
┌─────────────────────────────────────────────────────────┐
│               平台线程 vs 虚拟线程                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  平台线程 (传统)                     虚拟线程 (JDK 21+)    │
│  ┌───────────┐                   ┌───────────┐          │
│  │ OS Thread │                   │Virtual    │          │
│  │ ~1MB 栈   │                   │Thread     │          │
│  │           │                   │~KB 栈     │          │
│  └───────────┘                   └─────┬─────┘          │
│                                         │                │
│                                         ▼                │
│                                   ┌───────────┐          │
│                                   │Carrier    │          │
│                                   │Thread     │          │
│                                   │(ForkJoin) │          │
│                                   └───────────┘          │
│                                         │                │
│                                         ▼                │
│                                   ┌───────────┐          │
│                                   │ OS Thread │          │
│                                   └───────────┘          │
│                                                         │
│  M:1 (多虚拟线程共享一个载体线程)                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 虚拟线程创建

```java
// 1. 直接创建
Thread vthread = Thread.ofVirtual().start(() -> {
    System.out.println("Hello from virtual thread");
});

// 2. 使用 Executor (推荐)
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000_000; i++) {
        executor.submit(() -> {
            Thread.sleep(1000);
            return "done";
        });
    }
}

// 3. 使用工厂
ThreadFactory factory = Thread.ofVirtual().factory();
Thread vthread = factory.newThread(() -> task());
vthread.start();
```

### 虚拟线程 vs 平台线程

| 特性 | 平台线程 | 虚拟线程 |
|------|----------|----------|
| 创建成本 | 高 (~1-2MB 栈) | 极低 (~KB 栈) |
| 创建速度 | ~1000 μs | ~1 μs |
| 数量限制 | 数千 | 数百万 |
| 阻塞处理 | 线程挂起 | 卸载 (mount/unmount) |
| 调度 | OS 调度器 | JVM 调度器 |
| 适用场景 | CPU 密集 | I/O 密集 |

### 虚拟线程适用场景

```java
// ✅ 适合: I/O 密集型
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    // HTTP 请求
    List<CompletableFuture<Response>> futures = urls.stream()
        .map(url -> CompletableFuture.supplyAsync(() ->
            httpClient.send(request), executor))
        .toList();

    // 数据库查询
    futures = queries.stream()
        .map(query -> CompletableFuture.supplyAsync(() ->
            db.query(query), executor))
        .toList();

    // 文件操作
    futures = files.stream()
        .map(file -> CompletableFuture.supplyAsync(() ->
            Files.readString(file), executor))
        .toList();
}

// ❌ 不适合: CPU 密集型
// 虚拟线程不会加速计算，反而增加调度开销
for (int i = 0; i < 1000; i++) {
    executor.submit(() -> {
        // CPU 密集计算
        BigInteger result = BigInteger.probablePrime(2048, new Random());
    });
}
```

### 虚拟线程调试

```java
// 获取当前线程信息
Thread thread = Thread.currentThread();
System.out.println("Is virtual: " + thread.isVirtual());
System.out.println("Thread name: " + thread.getName());
System.out.println("Carrier thread: " + Thread.currentThread().toString());

// 线程 dump (jcmd)
// jcmd <pid> Thread.dump_to_file -format=json dump.json
```

---

## 9. Scoped Values

### 演进历程

| 版本 | 状态 | JEP |
|------|------|-----|
| JDK 20 | 预览 | JEP 429 |
| JDK 21 | 第二次预览 | JEP 446 |
| JDK 22 | 第三次预览 | JEP 464 |
| JDK 23 | 第四次预览 | JEP 467 |

### Scoped Values 原理

```
┌─────────────────────────────────────────────────────────┐
│           Scoped Values 隐式传递                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Main Thread                                            │
│  │                                                       │
│  │ ScopedValue.where(USER, alice)                       │
│  │   .run(() -> {                                       │
│  │     │                                                 │
│  │     │  Virtual Thread 1    Virtual Thread 2          │
│  │     │  │                   │                         │
│  │     │  │ USER.get() = alice │ USER.get() = alice      │
│  │     │  │                   │                         │
│  │     │  ▼                   ▼                         │
│  │     │ process1()          process2()                  │
│  │     │                                                 │
│  │   })                                                  │
│  │                                                       │
│  │ // 自动清理，无需 remove                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Scoped Values 使用

```java
// 定义 Scoped Value
public static final ScopedValue<String> CONTEXT = ScopedValue.newInstance();
public static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();
public static final ScopedValue<Request> REQUEST = ScopedValue.newInstance();

// 绑定值
ScopedValue.where(CURRENT_USER, user).where(REQUEST, request).run(() -> {
    // 在此作用域内，子线程可隐式访问
    processRequest();
});

// 跨虚拟线程传递
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    ScopedValue.where(CURRENT_USER, user).run(() -> {
        // 虚拟线程自动继承
        for (int i = 0; i < 100; i++) {
            executor.submit(() -> {
                // 隐式访问
                User u = CURRENT_USER.get();
                process(u);
            });
        }
    });
}

// 返回值
String result = ScopedValue.where(CONTEXT, "value")
    .call(() -> CONTEXT.get() + "!");
```

### Scoped Values vs ThreadLocal

| 特性 | ThreadLocal | ScopedValue |
|------|-------------|-------------|
| 传递方式 | 显式 | 隐式 |
| 生命周期 | 线程结束 | 作用域结束 |
| 内存泄漏风险 | 有 (必须 remove) | 无 (自动清理) |
| 虚拟线程支持 | 差 (每个虚拟线程一份) | 优 (共享) |
| 不可变性 | 可变 | 不可变 |
| 继承 | 子线程可继承 | 子线程可继承 |

```java
// ThreadLocal (旧方式)
private static final ThreadLocal<User> USER = new ThreadLocal<>();

// 需要清理
try {
    USER.set(user);
    process();
} finally {
    USER.remove();  // 必须清理，否则内存泄漏
}

// ScopedValue (新方式)
private static final ScopedValue<User> USER = ScopedValue.newInstance();

// 自动清理，无需 finally
ScopedValue.where(USER, user).run(() -> process());
```

---

## 10. Structured Concurrency

### 演进历程

| 版本 | 状态 | JEP |
|------|------|-----|
| JDK 21 | 预览 | JEP 453 |
| JDK 22 | 第二次预览 | JEP 462 |
| JDK 23 | 第三次预览 | JEP 477 |
| JDK 24 | 第四次预览 | JEP 483 |
| JDK 24 | 第五次预览 | JEP 491 |
| JDK 24 | 第六次预览 | JEP 493 |

### Structured Concurrency 原理

```
┌─────────────────────────────────────────────────────────┐
│           结构化并发 vs 非结构化并发                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  非结构化 (传统)                    结构化 (JDK 21+)     │
│                                                         │
│  main                            ┌─────────────────┐    │
│   │                               │  parent scope  │    │
│   ├─ task1 ────────────┐          │  ├─ task1       │    │
│   │                     │          │  ├─ task2       │    │
│   ├─ task2 ─────┐      │          │  ├─ task3       │    │
│   │             │      │          │  └──────────────┤    │
│   └─ task3 ─────┼──────┼          │       │          │    │
│                 │      │          │       ▼          │    │
│   无法统一管理   │      │          │  join() 等待全部  │    │
│   错误处理复杂   │      │          │  自动取消子任务    │    │
│                 │      │          └─────────────────┘    │
│                 ▼      │                                  │
│              线程泄漏风险│                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### StructuredTaskScope 基础用法

```java
import java.util.concurrent.StructuredTaskScope;
import java.util.concurrent.Future;

// JDK 21+ (预览)
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    // 并发执行多个任务
    StructuredTaskScope.Subtask<String> userTask =
        scope.fork(() -> fetchUser(userId));

    StructuredTaskScope.Subtask<List<Order>> ordersTask =
        scope.fork(() -> fetchOrders(userId));

    StructuredTaskScope.Subtask<Cart> cartTask =
        scope.fork(() -> fetchCart(userId));

    // 等待所有任务完成或任一失败
    scope.join().throwIfFailed();

    // 组合结果
    return new Response(
        userTask.get(),
        ordersTask.get(),
        cartTask.get()
    );

}  // 自动清理所有子任务
```

### Joiner API (JDK 23+)

```java
// JDK 23+ 新增 Joiner API
import java.util.concurrent.StructuredTaskScope.Joiner;

// 1. allSuccessfulOrThrow - 全部成功或抛异常
try (var scope = new StructuredTaskScope<>()) {
    StructuredTaskScope.Subtask<String> t1 = scope.fork(() -> task1());
    StructuredTaskScope.Subtask<String> t2 = scope.fork(() -> task2());

    String result = scope.join(Joiner.allSuccessfulOrThrow())
        .stream()
        .map(StructuredTaskScope.Subtask::get)
        .collect(Collectors.joining());

} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}

// 2. anySuccessfulOrThrow - 任一成功即返回
try (var scope = new StructuredTaskScope<>()) {
    scope.fork(() -> fetchFromPrimary());
    scope.fork(() -> fetchFromBackup());
    scope.fork(() -> fetchFromCache());

    // 返回第一个成功的结果
    String result = scope.join(Joiner.anySuccessfulOrThrow())
        .get()
        .get();

} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}

// 3. awaitAll - 等待全部完成
try (var scope = new StructuredTaskScope<>()) {
    scope.fork(() -> task1());
    scope.fork(() -> task2());

    scope.join(Joiner.awaitAll());  // 等待全部，不抛异常

} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}
```

### 自定义 Joiner

```java
// 自定义 Joiner - 收集所有成功和失败的结果
class CollectAll<T> implements StructuredTaskScope.Joiner<Result<T>> {
    @Override
    public Result<T> join(List<StructuredTaskScope.Subtask<? extends T>> subtasks)
        throws InterruptedException {

        List<T> successes = new ArrayList<>();
        List<Throwable> failures = new ArrayList<>();

        for (var subtask : subtasks) {
            switch (subtask.state()) {
                case SUCCESS -> successes.add(subtask.get());
                case FAILED -> failures.add(subtask.exception());
                case UNAVAILABLE -> {}
            }
        }

        return new Result<>(successes, failures);
    }
}

record Result<T>(List<T> successes, List<Throwable> failures) {}

// 使用
try (var scope = new StructuredTaskScope<>()) {
    scope.fork(() -> task1());
    scope.fork(() -> task2());

    Result<String> result = scope.join(new CollectAll<>());
    System.out.println("Successes: " + result.successes());
    System.out.println("Failures: " + result.failures().size());
}
```

### 结构化并发优势

```java
// 传统方式 (复杂)
ExecutorService executor = Executors.newFixedThreadPool(10);
List<Future<String>> futures = new ArrayList<>();

try {
    futures.add(executor.submit(() -> task1()));
    futures.add(executor.submit(() -> task2()));
    futures.add(executor.submit(() -> task3()));

    // 需要手动处理异常和取消
    for (Future<String> future : futures) {
        try {
            future.get();
        } catch (Exception e) {
            // 手动取消其他任务
            futures.forEach(f -> f.cancel(true));
            throw e;
        }
    }
} finally {
    executor.shutdown();  // 需要手动关闭
}

// Structured Concurrency (简洁)
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    scope.fork(() -> task1());
    scope.fork(() -> task2());
    scope.fork(() -> task3());

    scope.join().throwIfFailed();  // 自动处理取消
}  // 自动清理所有子任务
```

---

## 11. 并发工具选择指南

### 场景 vs 工具

| 场景 | 推荐工具 | 说明 |
|------|----------|------|
| 简单并发任务 | ExecutorService | 传统线程池 |
| I/O 密集型 | 虚拟线程 | 百万级并发 |
| 异步编排 | CompletableFuture | 链式调用 |
| 结构化任务 | StructuredTaskScope | 统一生命周期 |
| 隐式传递 | ScopedValue | 替代 ThreadLocal |
| CPU 并行 | Parallel Stream | ForkJoinPool |
| 工作窃取 | ForkJoinPool | 递归任务 |

### 决策流程

```
┌─────────────────────────────────────────────────────────┐
│                     任务类型?                            │
└─────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
         CPU 密集                       I/O 密集
              │                               │
              ▼                               ▼
    ┌─────────────────┐           ┌─────────────────────┐
    │ Parallel Stream │           │ Virtual Threads     │
    │ ForkJoinPool    │           │ (百万级并发)        │
    └─────────────────┘           └─────────────────────┘
                                              │
                                    ┌─────────┴─────────┐
                                    │                   │
                              简单异步编排          结构化任务
                                    │                   │
                                    ▼                   ▼
                          ┌───────────────┐   ┌──────────────┐
                          │CompletableFuture│ │StructuredTask│
                          └───────────────┘   └──────────────┘
```

---

## 12. 性能对比

### 线程类型性能

| 指标 | 平台线程 | 虚拟线程 |
|------|----------|----------|
| 创建时间 | ~1000 μs | ~1 μs |
| 内存占用 | ~1MB | 几 KB |
| 最大数量 | ~10,000 | ~10,000,000 |
| 上下文切换 | ~10-100 μs | ~纳秒级 |
| 阻塞开销 | 高 (挂起 OS 线程) | 低 (卸载虚拟线程) |

### 并发模型对比

| 模型 | 吞吐量 | 延迟 | 复杂度 |
|------|--------|------|--------|
| 线程池 | 中 | 中 | 低 |
| 虚拟线程 | 高 (I/O) | 低 | 低 |
| CompletableFuture | 中 | 中 | 中 |
| Structured Concurrency | 高 | 低 | 中 |
| Reactive (Flow) | 高 | 低 | 高 |

---

## 13. 最佳实践

### 1. 使用虚拟线程处理 I/O

```java
// ✅ 推荐
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<String> results = urls.stream()
        .map(url -> executor.submit(() -> httpClient.get(url)))
        .map(Future::join)
        .toList();
}
```

### 2. 使用结构化并发管理相关任务

```java
// ✅ 推荐
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    var user = scope.fork(() -> fetchUser(id));
    var orders = scope.fork(() -> fetchOrders(id));

    scope.join().throwIfFailed();
    return new Response(user.get(), orders.get());
}
```

### 3. 使用 ScopedValue 替代 ThreadLocal

```java
// ✅ 推荐
ScopedValue.where(CONTEXT, context).run(() -> {
    // 隐式传递
    process();
});
```

### 4. 避免在虚拟线程中执行 CPU 密集任务

```java
// ❌ 避免
executor.submit(() -> {
    BigInteger.probablePrime(2048, new Random());  // CPU 密集
});

// ✅ 改用 ForkJoinPool
ForkJoinPool.commonPool().submit(() -> {
    BigInteger.probablePrime(2048, new Random());
});
```

---

## 14. 时间线总结

| 版本 | 特性 | JEP | 影响 |
|------|------|-----|------|
| JDK 5 | Executor 框架 | JSR-166 | 简化线程管理 |
| JDK 7 | Fork/Join 框架 | JSR-166y | 工作窃取算法 |
| JDK 8 | Lambda + Stream | JEP 126 | 函数式集合操作 |
| JDK 8 | CompletableFuture | JEP 107 | 异步编程基础 |
| JDK 9 | Flow API | JEP 266 | 响应式流 |
| JDK 19 | 虚拟线程预览 | JEP 425 | 革命性并发模型 |
| JDK 20 | 虚拟线程二次预览 | JEP 436 | 改进 |
| JDK 21 | **虚拟线程正式** | JEP 444 | 生产可用 |
| JDK 21 | Scoped Value 预览 | JEP 446 | 隐式参数传递 |
| JDK 21 | Structured Concurrency 预览 | JEP 453 | 结构化并发 |
| JDK 23 | Scoped Value 四次预览 | JEP 467 | 持续改进 |
| JDK 24 | Structured Concurrency 六次预览 | JEP 493 | 持续改进 |

---

## 15. 相关链接

- [虚拟线程文档](https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html)
- [JEP 444](/jeps/concurrency/jep-444.md)
- [JEP 453](/jeps/concurrency/jep-453.md)
- [JEP 446](/jeps/concurrency/jep-446.md)
- [JEP 493](/jeps/tools/jep-493.md)
