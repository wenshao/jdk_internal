# JDK 25: Structured Concurrency 实现深度分析

> **JEP**: JEP 505 (第五次预览) | **状态**: 预览特性 | **API**: `java.util.concurrent.StructuredTaskScope`

---

## 1. 概述

Structured Concurrency 是 JDK 21 (JEP 453) 首次引入的预览特性，JDK 25 中是第五次预览 (JEP 505)。它将结构化编程的原则应用到并发编程中，确保子任务的生命周期被正确管理。

### 核心设计目标

| 目标 | 说明 |
|------|------|
| **清晰的所有权** | 父任务明确拥有子任务的生命周期 |
| **错误传播** | 子任务失败自动取消其他兄弟任务 |
| **资源安全** | 退出作用域时所有子任务已完成 |
| **可观测性** | 线程转储中显示任务层次结构 |

---

## 2. API 设计

### StructuredTaskScope 核心 API

```java
public final class StructuredTaskScope<C> implements AutoCloseable {
    
    // 工厂方法
    public static <T> StructuredTaskScope<T> open();
    public static <T> StructuredTaskScope<T> open(ThreadFactory factory);
    
    // 预定义策略
    public static <T> ShutdownOnSuccess<T> shutdownOnSuccess();
    public static <T> ShutdownOnFailure<T> shutdownOnFailure();
    
    // 任务提交
    public <U extends C> Subtask<U> fork(Callable<? extends U> task);
    
    // 等待与关闭
    public StructuredTaskScope<C> join() throws InterruptedException;
    public StructuredTaskScope<C> joinUntil(Instant deadline) throws InterruptedException, TimeoutException;
    public void close();
    
    // 结果获取
    public List<Subtask<C>> subtasks();
}
```

### Subtask 状态机

```
UNAVAILABLE ──fork()──> RUNNING ──success──> SUCCESS
                            │                    │
                            │                    └──> get() 返回结果
                            │
                            └──exception──> FAILED
                            │                   │
                            │                   └──> exception() 返回异常
                            │
                            └──cancel──> UNAVAILABLE
```

---

## 3. 实现原理

### 3.1 线程层次结构

```
StructuredTaskScope
├── Thread #1 (Virtual Thread)
│   └── Subtask<User>
├── Thread #2 (Virtual Thread)
│   └── Subtask<List<Order>>
└── Thread #3 (Virtual Thread)
    └── Subtask<List<Review>>
```

所有子线程都是虚拟线程，由 `ForkJoinPool` 调度。

### 3.2 内部数据结构

```java
// 简化的内部实现
public final class StructuredTaskScope<C> {
    private final ThreadFactory factory;
    private final ConcurrentLinkedQueue<Subtask<C>> subtasks = new ConcurrentLinkedQueue<>();
    private volatile boolean closed = false;
    
    // 用于 join() 的同步
    private final Object lock = new Object();
    private int unfinishedCount = 0;
}
```

### 3.3 fork() 实现

```java
public <U extends C> Subtask<U> fork(Callable<? extends U> task) {
    ensureOpen();
    
    // 创建 Subtask 占位符
    SubtaskImpl<U> subtask = new SubtaskImpl<>();
    subtasks.add(subtask);
    
    // 启动虚拟线程
    Thread.startVirtualThread(() -> {
        try {
            U result = task.call();
            subtask.success(result);
        } catch (Throwable e) {
            subtask.fail(e);
        } finally {
            signalCompletion();
        }
    });
    
    return subtask;
}
```

### 3.4 join() 实现

```java
public StructuredTaskScope<C> join() throws InterruptedException {
    synchronized (lock) {
        while (unfinishedCount > 0) {
            if (Thread.interrupted()) {
                handleInterrupt();
                throw new InterruptedException();
            }
            lock.wait();
        }
    }
    return this;
}
```

---

## 4. 预定义策略

### ShutdownOnSuccess

第一个子任务成功时，取消其他所有子任务：

```java
try (var scope = StructuredTaskScope.ShutdownOnSuccess.<Response>shutdownOnSuccess()) {
    scope.fork(() -> fetchUser(id));
    scope.fork(() -> fetchOrders(id));
    
    scope.join();
    
    // 获取第一个成功的结果
    Response response = scope.result();
}
```

**实现原理**:
```java
public static class ShutdownOnSuccess<T> extends StructuredTaskScope<T> {
    private volatile T result;
    
    @Override
    protected void handleSuccess(Subtask<? extends T> subtask) {
        result = subtask.get();
        shutdown();  // 取消其他子任务
    }
}
```

### ShutdownOnFailure

第一个子任务失败时，取消其他所有子任务：

```java
try (var scope = StructuredTaskScope.ShutdownOnFailure.shutdownOnFailure()) {
    scope.fork(() -> validateUser(id));
    scope.fork(() -> validatePermissions(id));
    
    scope.join();
    scope.throwIfFailed();
}
```

---

## 5. 与虚拟线程的集成

### 线程工厂集成

```java
// 使用自定义 ThreadFactory
ThreadFactory factory = Thread.ofVirtual()
    .name("worker-", 0)
    .uncaughtExceptionHandler((t, e) -> log.error("Thread {} failed", t, e))
    .factory();

try (var scope = StructuredTaskScope.open(factory)) {
    scope.fork(() -> task1());
    scope.fork(() -> task2());
    scope.join();
}
```

### 线程转储增强

```
"main" #1 [0x00007f8a1c001000] java.lang.Thread.State: RUNNABLE
  - waiting on <0x0000000700a00100> (a java.util.concurrent.StructuredTaskScope)
  at java.lang.VirtualThread.join(VirtualThread.java:xxx)
  at java.util.concurrent.StructuredTaskScope.join(StructuredTaskScope.java:xxx)

"scope-1/fork-1" #12 [0x00007f8a1c002000] VirtualThread
  - parent: "main" #1
  - scope: StructuredTaskScope@0x0000000700a00100
  at com.example.MyClass.fetchUser(MyClass.java:42)
```

---

## 6. 性能特性

### 创建开销

| 操作 | 耗时 (ns) | 说明 |
|------|-----------|------|
| `fork()` 调用 | ~500 | 虚拟线程创建 |
| `join()` 等待 | 取决于任务 | 阻塞直到所有子任务完成 |
| `close()` | ~100 | 清理资源 |

### 与 CompletableFuture 对比

| 特性 | StructuredTaskScope | CompletableFuture |
|------|---------------------|-------------------|
| **错误处理** | 自动传播 | 需要 `exceptionally()` |
| **资源泄漏** | 不可能 | 可能（忘记 join） |
| **线程转储** | 显示层次结构 | 扁平化 |
| **取消传播** | 自动 | 手动 |
| **性能开销** | 低（虚拟线程） | 中等 |

---

## 7. 最佳实践

### 7.1 正确使用模式

```java
// ✅ 推荐：try-with-resources
try (var scope = StructuredTaskScope.open()) {
    Subtask<User> user = scope.fork(() -> fetchUser(id));
    Subtask<List<Order>> orders = scope.fork(() -> fetchOrders(id));
    
    scope.join();
    
    return new Response(user.get(), orders.get());
}

// ❌ 错误：忘记 close()
var scope = StructuredTaskScope.open();
Subtask<User> user = scope.fork(() -> fetchUser(id));
scope.join();
// 忘记 scope.close()，可能泄漏资源
```

### 7.2 错误处理

```java
// ✅ 使用 ShutdownOnFailure 处理多任务验证
try (var scope = StructuredTaskScope.ShutdownOnFailure.shutdownOnFailure()) {
    scope.fork(() -> validateUser(id));
    scope.fork(() -> validatePermissions(id));
    scope.fork(() -> validateSubscription(id));
    
    scope.join();
    scope.throwIfFailed();  // 自动抛出第一个异常
    
    return "All validations passed";
} catch (ExecutionException e) {
    return "Validation failed: " + e.getCause().getMessage();
}
```

### 7.3 超时处理

```java
// ✅ 使用 joinUntil 设置超时
try (var scope = StructuredTaskScope.open()) {
    scope.fork(() -> fetchFromRemote(id));
    scope.fork(() -> fetchFromCache(id));
    
    scope.joinUntil(Instant.now().plusSeconds(5));
    
    return scope.subtasks().stream()
        .filter(Subtask::isSuccess)
        .map(Subtask::get)
        .findFirst()
        .orElseThrow();
} catch (TimeoutException e) {
    return "Request timed out";
}
```

---

## 8. 已知限制

| 限制 | 说明 |  workaround |
|------|------|-------------|
| **预览 API** | 需要 `--enable-preview` | 做好跟随版本升级准备 |
| **不支持嵌套 Scope** | 不能在 fork 的任务中创建新 Scope | 使用线程局部变量传递 |
| **异常聚合** | 多个失败时只抛出第一个 | 使用 `subtasks()` 遍历所有结果 |
| **不支持优先级** | 所有 fork 的任务平等 | 按顺序 fork 重要任务 |

---

## 9. 未来展望

### JDK 26 预期变化

- 可能进入正式发布（Final）
- API 预计稳定，不会有重大变更
- 可能增加更多预定义策略

### 长期方向

- 与 Virtual Threads 更深度集成
- 支持结构化并发与结构化异常的协同
- 可能引入 `StructuredExecutor` 的更高级变体

---

## 10. 相关资源

- [JEP 505: Structured Concurrency](https://openjdk.org/jeps/505)
- [JEP 453: Structured Concurrency (JDK 21)](https://openjdk.org/jeps/453)
- [StructuredTaskScope API 文档](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/StructuredTaskScope.html)
- [JDK 25 主页](../README.md)
- [虚拟线程实现](/deep-dive/virtual-thread-implementation.md)

---

*最后更新: 2026-04-02*
