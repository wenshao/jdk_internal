# Project Loom 时间线

虚拟线程和结构化并发从 2017 年至今的完整发展历程。

[← 返回 Loom](./)

---

## 2017: 项目启动

### 项目宣布

- **日期**: 2017-10
- **事件**: Ron Pressler 在 JVM Language Summit 宣布 Project Loom
- **目标**: "让并发编程像顺序编程一样简单"
- **核心问题**:
  - 平台线程昂贵
  - 异步编程复杂
  - 回调地狱

---

## 2018: Continuations 原型

### 核心机制实现

- **日期**: 2018-06
- **内容**: 实现 Continuations 作为底层机制
- **API**:

```java
// 早期原型 API
class Continuation {
    public Continuation(ContinuationScope scope, Runnable target);
    public void run();
    public static void yield(ContinuationScope scope);
}
```

---

## 2019: JDK 13-14 - 早期孵化

### JEP Draft: Virtual Threads

- **日期**: 2019-06
- **状态**: Draft
- **特性**:
  - `java.lang.VirtualThread` 类
  - Fiber 虚拟线程 (早期命名)

### 原型发布

- **日期**: 2019-09
- **里程碑**: JDK 13 包含 Loom 原型
- **标志**: `-XX:+EnableValhalla` (早期复用标志)

---

## 2020: JDK 14 - 孵化器

### 虚拟线程孵化器

- **日期**: 2020-03 (JDK 14)
- **包**: `jdk.incubator.concurrent`
- **类**: `java.lang.Fiber` (早期命名)

```java
// JDK 14 示例
Fiber f = Fiber.schedule(() -> {
    System.out.println("Hello from Fiber!");
});
```

---

## 2021: JDK 15-16 - 继续孵化

### API 重命名

- **日期**: 2021-03
- **变更**: Fiber → VirtualThread
- **原因**: 避免与网络 fiber 混淆

```java
// JDK 15/16 API
Thread vThread = Thread.builder()
    .virtual()
    .task(() -> doWork())
    .build();
vThread.start();
```

### 性能优化

- **日期**: 2021-09
- **改进**:
  - 减少 Carrier Thread 切换开销
  - 优化 synchronized 处理
  - 改进 ThreadLocal 支持

---

## 2022: JDK 17-18 - 预览版本

### JEP 425: Virtual Threads (Preview)

- **日期**: 2022-06 (JDK 19 预览)
- **包**: 无需孵化器，直接 `java.lang`
- **API**:

```java
// JDK 19 预览 API
Thread.ofVirtual().start(() -> {
    System.out.println("Virtual thread");
});

// ExecutorService
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> task());
}
```

### JEP 436: Virtual Threads (Second Preview)

- **日期**: 2022-09 (JDK 20 第二预览)
- **改进**:
  - API 细节调整
  - 性能优化
  - 文档完善

---

## 2023: JDK 21 - 正式发布

### JEP 444: Virtual Threads

- **日期**: 2023-09 (JDK 21 正式)
- **里程碑**: 虚拟线程正式发布
- **API**: `java.lang.Thread` 新方法

```java
// JDK 21 正式 API
Thread vThread = Thread.startVirtualThread(() -> {
    System.out.println("Hello!");
});

// 创建大量虚拟线程
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000_000; i++) {
        executor.submit(() -> task());
    }
}
```

### 结构化并发预览

- **日期**: 2023-09 (JDK 21)
- **JEP**: JEP 453 (预览)
- **包**: `java.util.concurrent.StructuredTaskScope`

```java
// JDK 21 预览 API
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Supplier<String> user = scope.fork(() -> fetchUser());
    Supplier<Order> order = scope.fork(() -> fetchOrder());

    scope.join().throwIfFailed();
    return new Response(user.get(), order.get());
}
```

---

## 2024-2025: 结构化并发演进

### JEP 453: Structured Concurrency (Preview)

- **日期**: 2024-03 (JDK 22 预览)
- **改进**:
  - 更清晰的作用域语义
  - 更好的错误传播
  - 性能优化

### JEP 464: Structured Concurrency (Second Preview)

- **日期**: 2025 (JDK 23 第二预览)
- **状态**: 进行中

---

## API 演进历史

### Thread API

| 版本 | API | 变化 |
|------|-----|------|
| JDK 14 | `Fiber` | 首次孵化器 |
| JDK 15 | `VirtualThread` | 重命名 |
| JDK 19 | `Thread.ofVirtual()` | 预览版 |
| JDK 21 | `Thread.startVirtualThread()` | 正式版 |

### ExecutorService

| 版本 | API | 变化 |
|------|-----|------|
| JDK 19 | `newVirtualThreadPerTaskExecutor()` | 预览版 |
| JDK 21 | `newVirtualThreadPerTaskExecutor()` | 正式版 |

---

## 时间线总览

```
2017 ── 2019 ── 2020 ── 2022 ── 2023 ── 2025
  │        │        │        │        │        │
启动    Continuations  Fiber   预览    正式    结构化
        原型     孵化器   JDK19   JDK21   并发
                                  Virtual  Structured
                                  Threads  Concurrency
```

---

## 里程碑总结

| 里程碑 | 版本 | 影响 |
|--------|------|------|
| **Continuations 原型** | 2018 | 底层机制 |
| **Fiber 孵化器** | JDK 14 | 首次公开 API |
| **Virtual Thread 预览** | JDK 19 | 移除孵化器 |
| **正式发布** | JDK 21 | 生产就绪 |
| **结构化并发预览** | JDK 21+ | 作用域管理 |

---

## 性能演进

| 版本 | 启动开销 | 阻塞开销 | 最大线程数 |
|------|----------|----------|------------|
| **JDK 14** | ~1μs | ~100ns | 10万+ |
| **JDK 19** | ~200ns | ~10ns | 100万+ |
| **JDK 21** | ~100ns | ~5ns | 无限制 |

---

## 相关项目

| 项目 | 关系 |
|------|------|
| **Project Panama** | 外部函数与虚拟线程配合 |
| **Project Valhalla** | 值类型减少线程开销 |
| **Reactive Streams** | 替代方案，Loom 更简单 |

→ [返回 Loom](./)
