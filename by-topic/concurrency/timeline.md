# 并发编程演进时间线

从 Thread 到 Virtual Thread 的演进历程。

---

## 时间线概览

```
JDK 8 ───── JDK 11 ───── JDK 17 ───── JDK 21 ───── JDK 26
│              │              │              │              │
Lambda/Stream  CompletableFuture  Var Handler    Virtual      Structured
改进          改进           简化           Threads 正式   Concurrency
                             CompletionStage  (预览→正式)   (第六次预览)
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

### JDK 5 - Executor 框架

```java
// 线程池
ExecutorService executor = Executors.newFixedThreadPool(10);
executor.submit(() -> task());
```

---

## 异步编程演进

### JDK 8 - Lambda + Stream

```java
// 并行流
list.parallelStream()
    .map(this::process)
    .collect(Collectors.toList());
```

### JDK 8 - CompletableFuture

```java
CompletableFuture.supplyAsync(() -> fetchUser())
    .thenCompose(user -> fetchOrders(user))
    .thenAccept(orders -> process(orders));
```

### JDK 9 - Reactive Streams

```java
// Flow API (响应式流)
Flow.Publisher<String> publisher = ...;
publisher.subscribe(subscriber);
```

---

## 结构化并发

### JDK 21 - Structured Concurrency (预览)

```java
try (var scope = new StructuredTaskScope<>()) {
    Subtask<String> t1 = scope.fork(() -> task1());
    Subtask<Integer> t2 = scope.fork(() -> task2());
    scope.join();
}
```

### JDK 26 - Structured Concurrency (第六次预览)

- 新增 Joiner API
- 内置策略：allSuccessfulOrThrow, anySuccessfulOrThrow
- 更好的异常处理

---

## 虚拟线程

### JDK 19 - 虚拟线程 (预览)

### JDK 20 - 虚拟线程 (第二次预览)

### JDK 21 - 虚拟线程 (正式)

```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> task());
}
```

### 特性

| 特性 | 平台线程 | 虚拟线程 |
|------|----------|----------|
| 创建成本 | 高 | 极低 |
| 数量限制 | 数千 | 数百万 |
| 阻塞处理 | 线程挂起 | 协程挂载 |
| 适用场景 | CPU 密集 | I/O 密集 |

---

## Scoped Values

### JDK 20 - Scoped Value (预览)

### JDK 21 - Scoped Value (第二次预览)

### JDK 26 - Scoped Value (继续预览)

```java
private static final ScopedValue<User> CURRENT_USER = ScopedValue.create();

try (var __ = ScopedValue.where(CURRENT_USER, user).bind()) {
    // implicit access
    processRequest();
}
```

---

## 时间线总结

| 版本 | 特性 | 影响 |
|------|------|------|
| JDK 5 | Executor 框架 | 简化线程管理 |
| JDK 7 | Fork/Join 框架 | 工作窃取 |
| JDK 8 | Lambda + Stream | 函数式集合操作 |
| JDK 8 | CompletableFuture | 异步编程基础 |
| JDK 9 | Flow API | 响应式流 |
| JDK 19 | 虚拟线程预览 | 革命性并发模型 |
| JDK 21 | **虚拟线程正式** | 生产可用 |
| JDK 21 | Scoped Value 预览 | 隐式参数传递 |
| JDK 26 | Structured Concurrency 预览 | 结构化并发 |

---

## 相关链接

- [虚拟线程文档](https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html)
- [Structured Concurrency](../../by-version/jdk26/deep-dive/structured-concurrency.md)
- [JEP 444: Virtual Threads](https://openjdk.org/jeps/444)
- [JEP 453: Structured Concurrency (Preview)](https://openjdk.org/jeps/453)
