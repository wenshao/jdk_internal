# 并发编程演进时间线

从 Thread 到 Virtual Thread 的演进历程。

---

## 时间线概览

```
JDK 5 ───── JDK 7 ───── JDK 8 ───── JDK 9 ───── JDK 19 ───── JDK 21 ───── JDK 26
 │              │              │              │              │              │
Executor       Fork/Join      CompletableFuture  Reactive      Virtual       Structured
框架            框架           改进             Streams        Threads 正式    Concurrency
(JSR-166)     (JSR-166y)     (JEP 107)       (JEP 266)      (JEP 444)      (第六次预览)
                                                                        (JEP 493)
```

---

## Thread 基础

### JDK 1.0 - Thread 类引入

```java
// 传统线程
Thread thread = new Thread(() -> {
    System.out.println("Hello");
});
thread.start();
```

**特点**：
- 1:1 映射到操作系统线程
- 创建成本高
- 上下文切换开销大

### JDK 5 - Executor 框架 (JSR-166)

```java
// 线程池
ExecutorService executor = Executors.newFixedThreadPool(10);
executor.submit(() -> task());

// Future
Future<String> future = executor.submit(() -> "result");
String result = future.get();  // 阻塞获取
```

**特点**：
- 线程复用
- 统一的生命周期管理
- 异步任务执行

---

## 异步编程演进

### JDK 7 - Fork/Join 框架 (JSR-166y)

```java
// 工作窃取
class Fibonacci extends RecursiveTask<Integer> {
    protected Integer compute() {
        if (n <= 1) return n;
        Fibonacci f1 = new Fibonacci(n - 1);
        f1.fork();  // 异步执行
        Fibonacci f2 = new Fibonacci(n - 2);
        return f2.compute() + f1.join();  // 等待结果
    }
}
```

### JDK 8 - Lambda + Stream

```java
// 并行流
list.parallelStream()
    .map(this::process)
    .collect(Collectors.toList());

// 底层使用 ForkJoinPool.commonPool()
```

### JDK 8 - CompletableFuture (JEP 107)

```java
// 链式调用
CompletableFuture.supplyAsync(() -> fetchUser())
    .thenCompose(user -> fetchOrders(user))
    .thenApply(orders -> process(orders))
    .exceptionally(e -> {
        log.error("Failed", e);
        return fallback;
    });

// 组合多个 Future
CompletableFuture.allOf(future1, future2, future3)
    .thenRun(() -> System.out.println("All done"));
```

### JDK 9 - Reactive Streams (JEP 266)

```java
// Flow API (响应式流)
SubmissionPublisher<String> publisher = new SubmissionPublisher<>();
publisher.subscribe(new Subscriber<>() {
    public void onSubscribe(Subscription sub) {
        sub.request(1);  // 请求数据
    }
    public void onNext(String item) {
        System.out.println(item);
    }
    public void onError(Throwable t) { }
    public void onComplete() { }
});

publisher.submit("Hello");
publisher.close();
```

---

## 虚拟线程 (Virtual Threads)

### 演进历程

| 版本 | 状态 | JEP |
|------|------|-----|
| JDK 19 | 预览 | JEP 425 |
| JDK 20 | 第二次预览 | JEP 436 |
| JDK 21 | **正式版** | JEP 444 |

### 虚拟线程示例

```java
// 创建虚拟线程
Thread vthread = Thread.ofVirtual().start(() -> {
    System.out.println("Hello from virtual thread");
});

// 使用虚拟线程池
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000_000; i++) {
        executor.submit(() -> {
            // I/O 操作不会阻塞平台线程
            Thread.sleep(1000);
            return "done";
        });
    }
}

// 与传统线程池对比
// 传统: Executors.newFixedThreadPool(200)  // 约 200 线程上限
// 虚拟: Executors.newVirtualThreadPerTaskExecutor()  // 百万级
```

### 虚拟线程 vs 平台线程

| 特性 | 平台线程 | 虚拟线程 |
|------|----------|----------|
| 创建成本 | 高 (~1-2MB) | 极低 (~KB) |
| 数量限制 | 数千 | 数百万 |
| 阻塞处理 | 线程挂起 | 协程挂载 |
| 适用场景 | CPU 密集 | I/O 密集 |
| 调度 | OS 调度 | JVM 调度 |

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
}

// ❌ 不适合: CPU 密集型
// 虚拟线程不会加速计算，反而增加调度开销
```

---

## Scoped Values

### 演进历程

| 版本 | 状态 | JEP |
|------|------|-----|
| JDK 20 | 预览 | JEP 429 |
| JDK 21 | 第二次预览 | JEP 446 |
| JDK 22 | 第三次预览 | JEP 464 |
| JDK 23 | 第四次预览 | JEP 467 |

### Scoped Values 示例

```java
// 定义 Scoped Value
private static final ScopedValue<User> CURRENT_USER = ScopedValue.create();
private static final ScopedValue<Request> REQUEST = ScopedValue.create();

// 绑定值
ScopedValue.where(CURRENT_USER, user).where(REQUEST, request).run(() -> {
    // 在此作用域内，子线程可隐式访问
    processRequest();
});

// 跨虚拟线程传递
ScopedValue.where(CURRENT_USER, user).run(() -> {
    // 虚拟线程自动继承
    executor.submit(() -> {
        User u = CURRENT_USER.get();  // 隐式访问
    });
});
```

### Scoped Values vs ThreadLocal

| 特性 | ThreadLocal | ScopedValue |
|------|-------------|-------------|
| 传递方式 | 显式 | 隐式 |
| 生命周期 | 线程结束 | 作用域结束 |
| 内存泄漏风险 | 有 | 无 |
| 虚拟线程支持 | 差 | 优 |
| 不可变性 | 可变 | 不可变 |

```java
// ThreadLocal (旧方式)
private static final ThreadLocal<User> USER = new ThreadLocal<>();

// 需要清理
try {
    USER.set(user);
    process();
} finally {
    USER.remove();  // 必须清理
}

// ScopedValue (新方式)
private static final ScopedValue<User> USER = ScopedValue.create();

// 自动清理，无需 finally
ScopedValue.where(USER, user).run(() -> process());
```

---

## Structured Concurrency

### 演进历程

| 版本 | 状态 | JEP |
|------|------|-----|
| JDK 21 | 预览 | JEP 453 |
| JDK 22 | 第二次预览 | JEP 462 |
| JDK 23 | 第三次预览 | JEP 477 |
| JDK 24 | 第四次预览 | JEP 483 |
| JDK 25 | 第五次预览 | JEP 491 |
| JDK 26 | 第六次预览 | JEP 493 |

### Structured Concurrency 示例

```java
// JDK 21+ (使用 StructuredTaskScope)
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    // 并发执行多个任务
    Subtask<String> user = scope.fork(() -> fetchUser(userId));
    Subtask<List<Order>> orders = scope.fork(() -> fetchOrders(userId));
    Subtask<Cart> cart = scope.fork(() -> fetchCart(userId));

    // 等待所有任务完成或任一失败
    scope.join().throwIfFailed();

    // 组合结果
    return new Response(user.get(), orders.get(), cart.get());

}  // 自动清理所有子任务
```

### Joiner API (JDK 23+)

```java
// JDK 23+ 新增 Joiner API
try (var scope = new StructuredTaskScope<>()) {
    Subtask<String> t1 = scope.fork(() -> task1());
    Subtask<String> t2 = scope.fork(() -> task2());

    // 使用 Joiner 策略
    String result = scope.join(Joiner.allSuccessfulOrThrow())
        .stream()
        .map(Subtask::get)
        .collect(Collectors.joining());

} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}
```

### 内置策略

| 策略 | 行为 |
|------|------|
| `allSuccessfulOrThrow()` | 全部成功或抛异常 |
| `anySuccessfulOrThrow()` | 任一成功即返回 |
| `awaitAll()` | 等待全部完成 |

### 结构化并发优势

```java
// 传统方式 (复杂)
ExecutorService executor = Executors.newFixedThreadPool(10);
List<Future<String>> futures = new ArrayList<>();
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

// Structured Concurrency (简洁)
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    scope.fork(() -> task1());
    scope.fork(() -> task2());
    scope.fork(() -> task3());

    scope.join().throwIfFailed();  // 自动处理取消
}
```

---

## 时间线总结

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
| JDK 26 | Structured Concurrency 六次预览 | JEP 493 | 持续改进 |

---

## 并发工具选择

| 场景 | 推荐工具 | 说明 |
|------|----------|------|
| 简单并发任务 | ExecutorService | 传统线程池 |
| I/O 密集型 | 虚拟线程 | 百万级并发 |
| 异步编排 | CompletableFuture | 链式调用 |
| 结构化任务 | StructuredTaskScope | 统一生命周期 |
| 隐式传递 | ScopedValue | 替代 ThreadLocal |
| CPU 并行 | Parallel Stream | ForkJoinPool |

---

## 相关链接

- [虚拟线程文档](https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html)
- [JEP 444: Virtual Threads](https://openjdk.org/jeps/444)
- [JEP 453: Structured Concurrency (Preview)](https://openjdk.org/jeps/453)
- [JEP 446: Scoped Values (Preview)](https://openjdk.org/jeps/446)
- [JEP 493: Structured Concurrency (Preview)](https://openjdk.org/jeps/493)
