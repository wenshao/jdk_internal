# JDK 26 结构化并发深度分析

> **JEP**: 525 | **状态**: 第六次预览 | **Commit**: 0bae56b6149
> **作者**: Alan Bateman | **Reviewer**: Viktor Klang

---

## 目录

1. [概念与设计](#概念与设计)
2. [API 架构](#api-架构)
3. [Joiner 机制](#joiner-机制)
4. [源码分析](#源码分析)
5. [与虚拟线程集成](#与虚拟线程集成)
6. [预览历史](#预览历史)

---

## 1. 概念与设计

### 核心思想

结构化并发确保并发任务的生命周期与语法块绑定，类似于结构化编程中的顺序操作：

```java
// 传统并发 - 生命周期不受控
ExecutorService executor = Executors.newCachedThreadPool();
Future<String> f1 = executor.submit(() -> task1());
Future<Integer> f2 = executor.submit(() -> task2());

try {
    return combine(f1.get(), f2.get());
} catch (Exception e) {
    // task1 或 task2 仍在运行！需要手动取消
    f1.cancel(true);
    f2.cancel(true);
}

// 结构化并发 - 生命周期受控
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Subtask<String> t1 = scope.fork(() -> task1());
    Subtask<Integer> t2 = scope.fork(() -> task2());

    scope.join();         // 等待所有子任务
    scope.throwIfFailed(); // 任一失败则抛出异常

    return combine(t1.get(), t2.get());
} // 自动关闭，取消未完成任务
```

### 设计原则

1. **语法块作用域**：并发操作的生命周期受语法块限制
2. **所有权**：只有 owner 线程可以调用 fork/join/close
3. **自动清理**：离开作用域时自动取消未完成的子任务
4. **异常传播**：子任务异常自动传播到 owner

---

## 2. API 架构

### StructuredTaskScope 核心类

```java
// StructuredTaskScope.java
public class StructuredTaskScope<T> implements AutoCloseable {

    // 创建新的作用域
    public static <T> StructuredTaskScope<T> open() { ... }
    public static <T> StructuredTaskScope<T> open(Joiner<? super T, ?> joiner) { ... }

    // 创建带线程工厂的作用域
    public static <T> StructuredTaskScope<T> open(
        ThreadFactory factory, Joiner<? super T, ?> joiner) { ... }

    // Fork 子任务
    public Subtask<T> fork(Callable<? extends T> task) { ... }

    // 等待所有子任务完成
    public StructuredTaskScope<T> join() throws InterruptedException { ... }
    public StructuredTaskScope<T> joinUntil(Instant deadline)
        throws InterruptedException, TimeoutException { ... }

    // 关闭作用域
    public void close() { ... }

    // Joiner 接口
    public interface Joiner<T, R> {
        boolean onFork(Subtask<? extends T> subtask);
        boolean onComplete(Subtask<? extends T> subtask);
        void onTimeout();
        R result() throws Throwable;
    }

    // Subtask 接口
    public interface Subtask<T> {
        State state();
        T get() throws NoSuchElementException;
        Throwable exception();
    }

    // 子任务状态
    public enum State {
        UNAVAILABLE,   // 未完成
        SUCCESS,       // 成功完成
        FAILED         // 失败完成
    }
}
```

### 预定义策略

```java
// 1. 等待所有成功，任一失败则取消
try (var scope = StructuredTaskScope.open(
        Joiner.<String>allSuccessfulOrThrow())) {
    scope.fork(() -> task1());
    scope.fork(() -> task2());

    List<String> results = scope.join();  // 返回所有结果
}

// 2. 等待任一成功，成功后取消其他
try (var scope = StructuredTaskScope.open(
        Joiner.<String>anySuccessfulOrThrow())) {
    scope.fork(() -> task1());
    scope.fork(() -> task2());

    String first = scope.join();  // 返回第一个成功结果
}

// 3. 等待所有完成，不返回结果
try (var scope = StructuredTaskScope.open(
        Joiner.<String>awaitAllSuccessfulOrThrow())) {
    Subtask<String> t1 = scope.fork(() -> task1());
    Subtask<Integer> t2 = scope.fork(() -> task2());

    scope.join();
    // 使用 Subtask.get() 获取结果
    return combine(t1.get(), t2.get());
}

// 4. 等待所有完成，返回所有 Subtask
try (var scope = StructuredTaskScope.open(
        Joiner.awaitAll(StructuredTaskScope::join))) {
    scope.fork(() -> task1());
    scope.fork(() -> task2());

    List<Subtask<String>> subtasks = scope.join();
}
```

---

## 3. Joiner 机制

### Joiner 接口

```java
public interface Joiner<T, R> {
    /**
     * 子任务 fork 时调用
     * @return true 表示应该取消作用域
     */
    boolean onFork(Subtask<? extends T> subtask);

    /**
     * 子任务完成时调用
     * @return true 表示应该取消作用域
     */
    boolean onComplete(Subtask<? extends T> subtask);

    /**
     * 超时时调用
     */
    void onTimeout();

    /**
     * 返回 join() 的结果
     */
    R result() throws Throwable;
}
```

### 内置 Joiner 实现

#### AllSuccessful - 等待所有成功

```java
// Joiners.java
static final class AllSuccessful<T> implements Joiner<T, List<T>> {
    private static final VarHandle FIRST_EXCEPTION = ...;

    private List<Subtask<T>> subtasks;   // 延迟初始化
    private volatile Throwable firstException;

    @Override
    public boolean onFork(Subtask<T> subtask) {
        ensureUnavailable(subtask);
        if (subtasks == null) {
            subtasks = new ArrayList<>();
        }
        subtasks.add(subtask);
        return false;  // 不取消
    }

    @Override
    public boolean onComplete(Subtask<T> subtask) {
        Subtask.State state = ensureCompleted(subtask);
        // 第一个失败时取消作用域
        return (state == Subtask.State.FAILED)
                && (firstException == null)
                && FIRST_EXCEPTION.compareAndSet(this, null, subtask.exception());
    }

    @Override
    public List<T> result() throws Throwable {
        Throwable ex = firstException;
        if (ex != null) {
            throw ex;
        }
        return (subtasks != null)
                ? subtasks.stream().map(Subtask::get).toList()
                : List.of();
    }
}
```

#### AnySuccessful - 等待任一成功

```java
static final class AnySuccessful<T> implements Joiner<T, T> {
    private static final VarHandle SUBTASK = ...;

    // 状态比较: UNAVAILABLE < FAILED < SUCCESS
    private static final Comparator<Subtask.State> SUBTASK_STATE_COMPARATOR = ...;

    private volatile Subtask<T> subtask;

    @Override
    public boolean onComplete(Subtask<T> subtask) {
        Subtask.State state = ensureCompleted(subtask);
        Subtask<T> s;
        // CAS 更新：保留"最好"的状态
        while (((s = this.subtask) == null)
                || SUBTASK_STATE_COMPARATOR.compare(s.state(), state) < 0) {
            if (SUBTASK.compareAndSet(this, s, subtask)) {
                return (state == Subtask.State.SUCCESS);  // 成功则取消
            }
        }
        return false;
    }

    @Override
    public T result() throws Throwable {
        Subtask<T> subtask = this.subtask;
        if (subtask == null) {
            throw new NoSuchElementException("No subtasks completed");
        }
        return switch (subtask.state()) {
            case SUCCESS -> subtask.get();
            case FAILED  -> throw subtask.exception();
            default      -> throw new InternalError();
        };
    }
}
```

---

## 4. 源码分析

### 核心文件列表

```
src/java.base/share/classes/java/util/concurrent/
├── StructuredTaskScope.java         # 公共 API
├── StructuredTaskScopeImpl.java     # 内部实现
└── Joiners.java                     # Joiner 实现
```

### StructuredTaskScopeImpl - 内部实现

```java
// StructuredTaskScopeImpl.java (内部实现类)
final class StructuredTaskScopeImpl<T> extends StructuredTaskScope<T> {

    // Owner 线程
    private final Thread owner;

    // Fork 的子任务列表
    private final List<SubtaskImpl<? extends T>> subtasks = new ArrayList<>();

    // Joiner
    private final Joiner<? super T, ?> joiner;

    // 线程工厂
    private final ThreadFactory factory;

    // 作用域状态
    private static final int OPEN     = 0;  // 打开
    private static final int CLOSED   = 1;  // 已关闭
    private static final int SHUTDOWN = 2;  // 已关闭（取消）
    private volatile int state;

    // 计数器：已完成的子任务数
    private final AtomicInteger remainingCount = new AtomicInteger();

    // 同步锁
    private final Lock lock = new ReentrantLock();
    private final Condition condition = lock.newCondition();

    // Fork 子任务
    @Override
    public Subtask<T> fork(Callable<? extends T> task) {
        Objects.requireNonNull(task);
        ensureOwner();

        lock.lock();
        try {
            // 检查状态
            if (state >= SHUTDOWN) {
                throw new IllegalStateException("Scope is shutdown");
            }
            if (forked) {
                throw new IllegalStateException("Already joined");
            }

            // 创建子任务
            var subtask = new SubtaskImpl<>(task, this);
            subtasks.add(subtask);

            // 通知 Joiner
            if (joiner.onFork(subtask)) {
                shutdown();  // Joiner 要求关闭
            }

            // 启动线程
            Thread thread = factory.newThread(subtask);
            thread.start();

            return subtask;
        } finally {
            lock.unlock();
        }
    }

    // Join 等待
    @Override
    public StructuredTaskScope<T> join() throws InterruptedException {
        ensureOwner();
        lock.lock();
        try {
            forked = true;
            while (remainingCount.get() > 0 && state < SHUTDOWN) {
                condition.await();  // 等待所有子任务完成
            }
            // 获取结果
            handleResult();
            return this;
        } finally {
            lock.unlock();
        }
    }

    // 子任务完成回调
    void onSubtaskComplete(SubtaskImpl<?> subtask) {
        boolean shouldShutdown;
        lock.lock();
        try {
            // 通知 Joiner
            shouldShutdown = joiner.onComplete(subtask);

            // 减少计数
            int remaining = remainingCount.decrementAndGet();
            if (remaining == 0 || shouldShutdown) {
                condition.signalAll();  // 唤醒 join()
            }
        } finally {
            lock.unlock();
        }

        if (shouldShutdown) {
            shutdown();  // 取消作用域
        }
    }

    // 关闭作用域
    @Override
    public void close() {
        ensureOwner();
        int s = state;
        if (s == CLOSED) {
            return;
        }
        if (s == OPEN && !forked) {
            // 没有 fork 就直接关闭
            state = CLOSED;
            return;
        }

        // 等待所有子任务完成
        try {
            join();  // 可能抛出异常
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            shutdown();  // 确保关闭
        }
    }
}
```

### SubtaskImpl - 子任务实现

```java
final class SubtaskImpl<T> extends Subtask<T> implements Runnable {
    private final Callable<? extends T> task;
    private final StructuredTaskScopeImpl<? super T> scope;

    private volatile State state = State.UNAVAILABLE;
    private volatile T result;
    private volatile Throwable exception;
    private volatile Thread thread;

    @Override
    public void run() {
        this.thread = Thread.currentThread();
        try {
            // 执行任务
            T value = task.call();
            // 成功完成
            this.result = value;
            this.state = State.SUCCESS;
        } catch (Throwable e) {
            // 失败完成
            this.exception = e;
            this.state = State.FAILED;
        } finally {
            // 通知作用域
            scope.onSubtaskComplete(this);
        }
    }

    @Override
    public State state() {
        return state;
    }

    @Override
    public T get() {
        if (state != State.SUCCESS) {
            throw new IllegalStateException(...);
        }
        return result;
    }

    @Override
    public Throwable exception() {
        if (state != State.FAILED) {
            throw new IllegalStateException(...);
        }
        return exception;
    }
}
```

---

## 5. 与虚拟线程集成

### 推荐组合

```java
// 虚拟线程 + 结构化并发 = 简单高效的并发
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        // 每个子任务在独立的虚拟线程中运行
        Future<String> user = scope.fork(() -> fetchUser());
        Future<List<Order>> orders = scope.fork(() -> fetchOrders());

        scope.join();
        scope.throwIfFailed();

        return new Response(user.resultNow(), orders.resultNow());
    }
}
```

### 为什么是最佳组合

1. **轻量级**：虚拟线程创建成本低，可大规模创建
2. **阻塞友好**：虚拟线程阻塞不浪费平台线程
3. **自动清理**：结构化并发确保虚拟线程及时清理
4. **取消支持**：中断传播到虚拟线程

### 对比 CompletableFuture

```java
// CompletableFuture - 生命周期管理复杂
CompletableFuture<String> userFuture = CompletableFuture.supplyAsync(() -> fetchUser());
CompletableFuture<Integer> orderFuture = CompletableFuture.supplyAsync(() -> fetchOrder());

CompletableFuture<Response> result = userFuture.thenCombine(orderFuture, Response::new);

// 问题：userFuture 失败时，orderFuture 不会自动取消
// 需要手动实现取消逻辑

// StructuredTaskScope - 自动取消
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Subtask<String> user = scope.fork(() -> fetchUser());
    Subtask<Integer> order = scope.fork(() -> fetchOrder());

    scope.join();
    scope.throwIfFailed();

    return new Response(user.get(), order.get());
}
// 任一失败，另一个自动取消
```

---

## 6. 预览历史

```
JEP 428  (JDK 19) - Structured Concurrency (Incubator)
JEP 437  (JDK 20) - Structured Concurrency (Second Incubator)
JEP 453  (JDK 21) - Structured Concurrency (Preview)
JEP 461  (JDK 22) - Structured Concurrency (Second Preview)
JEP 481  (JDK 23) - Structured Concurrency (Third Preview)
JEP 505  (JDK 25) - Structured Concurrency (Fifth Preview)
JEP 525  (JDK 26) - Structured Concurrency (Sixth Preview)
```

### JDK 26 变化

1. **Joiner API 优化**：更清晰的接口设计
2. **内置 Joiner**：提供常用策略的工厂方法
3. **超时支持**：`joinUntil(Instant)` 方法
4. **状态枚举**：`Subtask.State` 枚举值

---

## 7. 最佳实践

### 1. 使用 try-with-resources

```java
// ✅ 推荐
try (var scope = StructuredTaskScope.open()) {
    // ...
}  // 自动关闭

// ❌ 避免
var scope = StructuredTaskScope.open();
// 忘记关闭
```

### 2. 配合虚拟线程

```java
// ✅ 推荐
try (var scope = StructuredTaskScope.open()) {
    scope.fork(() -> blockingIO());
    scope.join();
}

// ❌ 避免：用平台线程执行阻塞任务
```

### 3. 处理中断

```java
// ✅ 推荐：响应中断
Subtask<String> task = scope.fork(() -> {
    try {
        return fetchWithTimeout();
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
        return null;  // 或抛出异常
    }
});
```

### 4. 选择合适的 Joiner

```java
// 需要所有结果
Joiner.allSuccessfulOrThrow()

// 需要任一结果（竞速）
Joiner.anySuccessfulOrThrow()

// 只需等待完成
Joiner.awaitAllSuccessfulOrThrow()
```

---

## 8. 总结

JDK 26 的结构化并发（第六次预览）提供了一个简洁、安全、高效的并发编程模型：

1. **简洁性**：语法块作用域，自动清理
2. **安全性**：异常自动传播，资源自动释放
3. **高效性**：与虚拟线程完美配合
4. **灵活性**：可自定义 Joiner 策略

---

## 9. 相关链接

- [JEP 525 官方文档](https://openjdk.org/jeps/525)
- [Commit: 0bae56b6149](https://github.com/openjdk/jdk/commit/0bae56b6149)
- [虚拟线程文档](https://openjdk.org/jeps/444)
