# Project Loom

虚拟线程 - 轻量级并发，百万级线程无压力。

[← 返回核心平台](../)

---
## 目录

1. [TL;DR](#1-tldr)
2. [项目概述](#2-项目概述)
3. [虚拟线程](#3-虚拟线程)
4. [工作原理](#4-工作原理)
5. [结构化并发 (JEP 453)](#5-结构化并发-jep-453)
6. [性能特性](#6-性能特性)
7. [时间线](#7-时间线)
8. [核心贡献者](#8-核心贡献者)
9. [迁移指南](#9-迁移指南)
10. [监控与调试](#10-监控与调试)
11. [最佳实践](#11-最佳实践)
12. [参考资料](#12-参考资料)

---


## 1. TL;DR

**Project Loom** 是 OpenJDK 的并发项目，提供：
- **虚拟线程** - 轻量级线程，由 JVM 管理
- **结构化并发** (Structured Concurrency) - 作用域内并发任务管理
- **Continuations** - 底层暂停/恢复机制

**状态**:
- **虚拟线程**: 正式发布 (JDK 21, JEP 444)；JDK 24 消除 synchronized 固定问题 (JEP 491)
- **结构化并发**: 预览中 (JDK 26 第六次预览, JEP 525)
- **Scoped Values**: 正式发布 (JDK 25, JEP 506)

---

## 2. 项目概述

### 解决的问题

| 问题 | 描述 | Loom 解决方案 |
|------|------|---------------|
| **平台线程昂贵** | 每线程 ~1MB 栈内存 | 虚拟线程 ~几 KB |
| **线程数量受限** | 几千线程已达上限 | 百万级虚拟线程 |
| **异步编程复杂** | 回调地狱、响应式流 | 直接写同步代码 |
| **阻塞开销大** | 阻塞浪费线程资源 | 阻塞几乎无开销 |

### 核心特性

```
┌─────────────────────────────────────────────────────────┐
│                    Project Loom                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  Virtual Threads│  │  Structured     │              │
│  │  (虚拟线程)      │  │  Concurrency    │              │
│  ├─────────────────┤  │  (结构化并发)    │              │
│  │ • 轻量级        │  ├─────────────────┤              │
│  │ • 百万级        │  │ • 作用域管理     │              │
│  │ • 阻塞无开销     │  │ • 错误传播       │              │
│  └─────────────────┘  │ • 取消传播       │              │
│                       └─────────────────┘              │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 3. 虚拟线程

### 基本用法

```java
// 创建虚拟线程
Thread vThread = Thread.startVirtualThread(() -> {
    System.out.println("Hello from virtual thread!");
});

// 或者使用 ExecutorService
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000_000; i++) {
        executor.submit(() -> {
            // 阻塞操作不会阻塞平台线程
            Thread.sleep(1000);
            processRequest();
        });
    }
}
```

### 平台线程 vs 虚拟线程

| 特性 | 平台线程 | 虚拟线程 |
|------|----------|----------|
| **创建成本** | 高 (~1MB 栈) | 低 (~几 KB) |
| **数量限制** | 几千 | 百万级 |
| **阻塞开销** | 高 (浪费线程) | 极低 (挂起虚拟线程) |
| **调度** | OS 调度 | JVM 调度 |
| **适用场景** | CPU 密集 | I/O 密集 |

### 示例对比

```java
// 平台线程 - 有限制
try (var executor = Executors.newFixedThreadPool(200)) {
    for (int i = 0; i < 10_000; i++) {
        executor.submit(() -> blockingIO());  // 可能队列满
    }
}

// 虚拟线程 - 无限制
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000_000; i++) {
        executor.submit(() -> blockingIO());  // 无压力
    }
}
```

---

## 4. 工作原理

### Carrier Thread 模型

```
┌─────────────────────────────────────────────────────────┐
│                    JVM 线程模型                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   平台线程 (Carrier)                                     │
│   │                                                      │
│   ├── 虚拟线程 1 ──阻塞───▶ 挂起                         │
│   ├── 虚拟线程 2 ──运行───▶ 执行                         │
│   ├── 虚拟线程 3 ──运行───▶ 执行                         │
│   └── 虚拟线程 4 ──阻塞───▶ 挂起                         │
│                                                          │
│   虚拟线程阻塞时，Carrier 继续执行其他虚拟线程            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Continuations

```java
// 底层机制 (通常不需要直接使用)
class ContinuationExample {
    public static void main(String[] args) {
        var scope = new ContinuationScope("example");
        var cont = new Continuation(scope, () -> {
            System.out.println("Step 1");
            Continuation.yield(scope);
            System.out.println("Step 2");
        });

        // 第一次运行 - 打印 Step 1 然后 yield
        cont.run();

        // 第二次运行 - 从 yield 处继续，打印 Step 2
        cont.run();
    }
}
```

---

## 5. 结构化并发

### API 演进

| 版本 | JEP | 变化 |
|------|-----|------|
| JDK 21 | JEP 453 | 第一次预览 |
| JDK 22 | JEP 462 | 第二次预览 |
| JDK 23 | JEP 480 | 第三次预览 |
| JDK 24 | JEP 499 | 第四次预览 |
| JDK 25 | JEP 505 | 第五次预览 - 重大 API 重构：构造函数改为静态工厂方法，引入 Joiner 接口 |
| JDK 26 | JEP 525 | 第六次预览 - 新增 `Joiner.onTimeout()`，`allSuccessfulOrThrow()` 返回 List 而非 Stream |

### 基本概念 (JDK 25+ API)

```java
// JDK 25+: 使用静态工厂方法 open() 创建 scope
try (var scope = StructuredTaskScope.open()) {
    // 并发启动多个任务 - fork() 返回 Subtask 而非 Future
    Subtask<String> user = scope.fork(() -> fetchUser());
    Subtask<Order> order = scope.fork(() -> fetchOrder());

    // 等待所有任务完成
    scope.join();

    // 组合结果 - Subtask.get() 类似 Future.resultNow()
    return new Response(user.get(), order.get());

} // scope 关闭时，未完成的任务自动取消
```

### 使用 Joiner (JDK 25+)

```java
// 返回第一个成功的结果 - 使用 Joiner
try (var scope = StructuredTaskScope.open(
        Joiner.anySuccessfulOrThrow())) {  // JDK 26 重命名
    scope.fork(() -> fetchFromSourceA());
    scope.fork(() -> fetchFromSourceB());
    scope.fork(() -> fetchFromSourceC());

    return scope.join();  // 返回第一个成功的结果

} catch (InterruptedException e) {
    throw new RuntimeException(e);
}
```

---

## 6. 性能特性

### 阻塞无开销

```java
// 虚拟线程阻塞
Thread.sleep(1000);  // 不阻塞 Carrier Thread

// Socket 阻塞
socket.read(buffer); // 不阻塞 Carrier Thread

// 锁阻塞
synchronized (lock) { // JDK 21-23 会 Pin; JDK 24+ 不再 Pin (JEP 491)
    // ...
}
```

### Pinning 问题

> **JDK 24 重大改进 (JEP 491)**: `synchronized` 块内的阻塞不再固定虚拟线程到载体线程。JVM 内部重构了 monitor 实现，使用虚拟线程 ID 追踪 monitor 持有者，虚拟线程可在持有 monitor 时独立于载体线程进行挂起和恢复。仅少数边缘情况（native/VM 帧、类初始化器内阻塞）仍会导致 pinning。系统属性 `jdk.tracePinnedThreads` (JEP 444 引入) 已移除，改用 JFR 事件 `jdk.VirtualThreadPinned` 监控剩余 pinning 场景。

```java
// JDK 21-23: ❌ 会 Pin Carrier
// JDK 24+:   ✅ 不再 Pin (JEP 491)
synchronized (lock) {
    Thread.sleep(1000);  // JDK 24 起虚拟线程可正常挂起
}

// ReentrantLock 在所有版本中均不 Pin
ReentrantLock lock = new ReentrantLock();
lock.lock();
try {
    Thread.sleep(1000);  // 不 Pin
} finally {
    lock.unlock();
}
```

---

## 7. 时间线

| 年份 | 版本 | 里程碑 |
|------|------|--------|
| **2017** | - | Project Loom 启动 |
| **2018** | - | Continuations 原型 |
| **2018-2019** | - | 虚拟线程原型 (独立 EA 构建) |
| **2020-2021** | - | 虚拟线程开发 (独立 EA 构建) |
| **2022** | JDK 19 | 虚拟线程 (第一次预览, JEP 425) |
| **2023** | JDK 20 | 虚拟线程 (第二次预览, JEP 436) |
| **2023** | JDK 21 | **虚拟线程 (正式, JEP 444)** |
| **2023** | JDK 21 | 结构化并发 (第一预览, JEP 453) |
| **2024** | JDK 22 | 结构化并发 (第二预览, JEP 462) |
| **2024** | JDK 22 | Scoped Values (第二预览, JEP 464) |
| **2024** | JDK 23 | 结构化并发 (第三预览, JEP 480) |
| **2024** | JDK 23 | Scoped Values (第三预览, JEP 481) |
| **2025** | JDK 24 | **虚拟线程不再 Pin synchronized (JEP 491)** |
| **2025** | JDK 24 | 结构化并发 (第四预览, JEP 499) |
| **2025** | JDK 24 | Scoped Values (第四预览, JEP 487) |
| **2025** | JDK 25 | **Scoped Values (正式, JEP 506)** |
| **2025** | JDK 25 | 结构化并发 (第五预览, JEP 505) - API 重构 |
| **2026** | JDK 26 | 结构化并发 (第六预览, JEP 525) |


→ [完整时间线](timeline.md)

---

## 8. 核心贡献者

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| [Ron Pressler](/by-contributor/profiles/ron-pressler.md) | Oracle | 项目领导人 |
| [Alan Bateman](/by-contributor/profiles/alan-bateman.md) | Oracle | 并发基础设施 |
| [David Holmes](/by-contributor/profiles/david-holmes.md) | Oracle | 线程实现 |

---

## 9. 迁移指南

### 从线程池迁移

```java
// 旧代码
ExecutorService executor = Executors.newFixedThreadPool(200);

// 新代码
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
```

### 从异步 API 迁移

```java
// 旧代码: CompletableFuture
public CompletableFuture<String> fetchData() {
    return CompletableFuture.supplyAsync(() -> {
        return blockingIO();
    }, executor);
}

// 新代码: 虚拟线程
public String fetchData() {
    // 直接写同步代码
    return blockingIO();
}
```

### 从响应式迁移

```java
// 旧代码: WebFlux
public Mono<Response> handle(Request req) {
    return service.getUser(req.getUserId())
        .zipWith(service.getOrder(req.getOrderId()))
        .map(tuple -> new Response(tuple.getT1(), tuple.getT2()));
}

// 新代码: 虚拟线程 + 结构化并发 (JDK 25+ API)
public Response handle(Request req) {
    try (var scope = StructuredTaskScope.open()) {
        var userTask = scope.fork(() -> service.getUser(req.getUserId()));
        var orderTask = scope.fork(() -> service.getOrder(req.getOrderId()));

        scope.join();
        return new Response(userTask.get(), orderTask.get());
    }
}
```

---

## 10. 监控与调试

### JFR 事件

```bash
# 启用虚拟线程 JFR 记录
java -XX:StartFlightRecording=filename=vthreads.jfr \
     -XX:FlightRecorderOptions=vthread=true \
     MyApp
```

### 线程转储

```bash
# jstack 显示虚拟线程
jstack <pid>

# 输出包含:
# "VirtualThread-123" #123 runnable
#    - java.lang.VirtualThread.mount
#    - blockingOperation
```

### 监控 API

```java
// 检查是否为虚拟线程
Thread thread = Thread.currentThread();
boolean isVirtual = thread.isVirtual();

// 获取虚拟线程数量
long vthreadCount = Thread.getAllStackTraces().keySet().stream()
    .filter(Thread::isVirtual)
    .count();
```

---

## 11. 最佳实践

### DO

```java
// ✅ I/O 密集任务使用虚拟线程
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> handleHttpRequest());
}

// ✅ 使用结构化并发管理任务组 (JDK 25+ API)
try (var scope = StructuredTaskScope.open()) {
    // ...
}
```

### DON'T

```java
// ❌ CPU 密集任务仍用 ForkJoinPool
// 虚拟线程不会加速 CPU 密集任务

// ❌ 在 synchronized 中阻塞 (JDK 21-23; JDK 24+ 已修复此问题)
synchronized (lock) {
    Thread.sleep(1000);  // JDK 24 前会 Pin Carrier
}

// ❌ 使用 ThreadLocal 存储大量数据
// 虚拟线程数量巨大，ThreadLocal 会浪费内存
```

---

## 12. 参考资料

- [Project Loom Official Page](https://openjdk.org/projects/loom/)
- [JEP 444](/jeps/concurrency/jep-444.md) - 虚拟线程 (正式, JDK 21)
- [JEP 453](/jeps/concurrency/jep-453.md) - 结构化并发 (第一预览, JDK 21)
- [JEP 436](/jeps/concurrency/jep-436.md) - 虚拟线程 (第二预览, JDK 20)
- [JEP 462](https://openjdk.org/jeps/462) - 结构化并发 (第二预览, JDK 22)
- [JEP 480](https://openjdk.org/jeps/480) - 结构化并发 (第三预览, JDK 23)
- [JEP 491](https://openjdk.org/jeps/491) - 虚拟线程不再 Pin synchronized (JDK 24)
- [JEP 499](https://openjdk.org/jeps/499) - 结构化并发 (第四预览, JDK 24)
- [JEP 506](https://openjdk.org/jeps/506) - Scoped Values (正式, JDK 25)
- [JEP 505](https://openjdk.org/jeps/505) - 结构化并发 (第五预览, JDK 25)
- [JEP 525](https://openjdk.org/jeps/525) - 结构化并发 (第六预览, JDK 26)

→ [时间线](timeline.md) | [并发主题](../../concurrency/)
