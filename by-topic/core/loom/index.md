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

**状态**: 虚拟线程已正式发布 (JDK 21)，结构化并发预览中

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

## 5. 结构化并发 (JEP 453)

### 基本概念

```java
// Java 21+ 预览特性
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    // 并发启动多个任务
    Supplier<String> user = scope.fork(() -> fetchUser());
    Supplier<Order> order = scope.fork(() -> fetchOrder());

    // 等待所有任务完成
    scope.join()           // 等待所有任务
         .throwIfFailed(); // 如果有失败则抛出异常

    // 组合结果
    return new Response(user.get(), order.get());

} // scope 关闭时，未完成的任务自动取消
```

### ShutdownOnSuccess

```java
// 返回第一个成功的结果
try (var scope = new StructuredTaskScope.SuccessOnSuccess<Object>()) {
    scope.fork(() -> fetchFromSourceA());
    scope.fork(() -> fetchFromSourceB());
    scope.fork(() -> fetchFromSourceC());

    scope.join();
    return scope.result();  // 第一个成功的结果

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
synchronized (lock) { // 不阻塞 Carrier Thread
    // ...
}
```

### Pinning 问题

```java
// ❌ 避免: native 代码或 synchronized 块中的阻塞
synchronized (lock) {
    Thread.sleep(1000);  // Pin Carrier!
}

// ✅ 推荐: 使用 ReentrantLock
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
| **2019** | JDK 13 | 虚拟线程原型 |
| **2020** | JDK 14 | 虚拟线程 (孵化器) |
| **2021** | JDK 15-16 | 虚拟线程 (孵化器) |
| **2022** | JDK 17 | 虚拟线程 (预览) |
| **2023** | JDK 19-20 | 虚拟线程 (预览) |
| **2023** | JDK 21 | **虚拟线程 (正式)** |
| **2024** | JDK 21 | 结构化并发 (预览) |

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

// 新代码: 虚拟线程
public Response handle(Request req) {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        var userTask = scope.fork(() -> service.getUser(req.getUserId()));
        var orderTask = scope.fork(() -> service.getOrder(req.getOrderId()));

        scope.join().throwIfFailed();
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

// ✅ 使用结构化并发管理任务组
try (var scope = new StructuredTaskScope<>()) {
    // ...
}
```

### DON'T

```java
// ❌ CPU 密集任务仍用 ForkJoinPool
// 虚拟线程不会加速 CPU 密集任务

// ❌ 在 synchronized 中阻塞
synchronized (lock) {
    Thread.sleep(1000);  // Pin Carrier
}

// ❌ 使用 ThreadLocal 存储大量数据
// 虚拟线程数量巨大，ThreadLocal 会浪费内存
```

---

## 12. 参考资料

- [Project Loom Official Page](https://openjdk.org/projects/loom/)
- [JEP 444](/jeps/concurrency/jep-444.md)
- [JEP 453](/jeps/concurrency/jep-453.md)
- [JEP 436](/jeps/concurrency/jep-436.md)

→ [时间线](timeline.md) | [并发主题](../../concurrency/)
