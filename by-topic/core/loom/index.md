# Project Loom

虚拟线程 - 轻量级并发，百万级线程无压力。

[← 返回核心平台](../)

---
## 目录

1. [TL;DR](#1-tldr)
2. [项目概述](#2-项目概述)
3. [虚拟线程基础](#3-虚拟线程基础)
4. [虚拟线程内部实现](#4-虚拟线程内部实现)
5. [JEP 491 深入: Monitor 重新实现](#5-jep-491-深入-monitor-重新实现)
6. [结构化并发](#6-结构化并发)
7. [Scoped Values 深入 (JEP 506)](#7-scoped-values-深入-jep-506)
8. [性能基准](#8-性能基准)
9. [生态系统适配](#9-生态系统适配)
10. [陷阱与反模式](#10-陷阱与反模式)
11. [时间线](#11-时间线)
12. [核心贡献者](#12-核心贡献者)
13. [迁移指南](#13-迁移指南)
14. [监控与调试](#14-监控与调试)
15. [最佳实践](#15-最佳实践)
16. [参考资料](#16-参考资料)

---


## 1. TL;DR

**Project Loom** 是 OpenJDK 的并发项目，提供：
- **虚拟线程** - 轻量级线程，由 JVM 管理，栈帧存储在堆上
- **结构化并发** (Structured Concurrency) - 作用域内并发任务管理
- **Scoped Values** - 不可变的线程作用域数据传递机制
- **Continuations** - 底层栈帧冻结/恢复机制 (内部 API，不对外暴露)

**状态**:
- **虚拟线程**: 正式发布 (JDK 21, JEP 444)；JDK 24 消除 synchronized 固定问题 (JEP 491)
- **Scoped Values**: 正式发布 (JDK 25, JEP 506)
- **结构化并发**: 预览中 (JDK 26 第六次预览, JEP 525)

---

## 2. 项目概述

### 解决的问题

| 问题 | 描述 | Loom 解决方案 |
|------|------|---------------|
| **平台线程昂贵** | 每线程 ~1MB 栈内存，创建需要系统调用 | 虚拟线程 ~几 KB，纯 Java 对象 |
| **线程数量受限** | 几千线程已达 OS 上限 | 百万级虚拟线程 |
| **异步编程复杂** | 回调地狱、响应式流、丢失堆栈 | 直接写同步代码，堆栈完整 |
| **阻塞开销大** | 阻塞浪费宝贵的平台线程资源 | 阻塞仅挂起虚拟线程，释放 carrier（载体线程） |
| **并发错误处理** | 手动管理子任务生命周期 | 结构化并发自动传播取消/错误 |

### 核心组件

```
┌─────────────────────────────────────────────────────────────────┐
│                       Project Loom                              │
├─────────────┬──────────────────┬────────────────────────────────┤
│             │                  │                                │
│  Virtual    │  Structured      │  Scoped Values                 │
│  Threads    │  Concurrency     │  (JEP 506)                     │
│  (JEP 444) │  (JEP 525)       │                                │
│             │                  │                                │
│  • 轻量级   │  • 作用域管理     │  • 不可变绑定                   │
│  • 百万级   │  • 错误传播       │  • 自动继承                     │
│  • 阻塞无开销│  • 取消传播       │  • 零拷贝传递                   │
│             │  • Joiner 模式   │  • 替代 ThreadLocal            │
├─────────────┴──────────────────┴────────────────────────────────┤
│  Continuations (内部 API)                                       │
│  • 栈帧 freeze（冻结）/ thaw（解冻）                              │
│  • v-stack ↔ h-stack 拷贝                                      │
│  • StackChunk 链表管理                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. 虚拟线程基础

### 基本用法

```java
// 方式 1: Thread.startVirtualThread()
Thread vThread = Thread.startVirtualThread(() -> {
    System.out.println("Hello from virtual thread!");
});

// 方式 2: Thread.ofVirtual() builder
Thread vThread = Thread.ofVirtual()
    .name("my-vthread")
    .start(() -> {
        System.out.println("Named virtual thread");
    });

// 方式 3: ExecutorService (推荐用于批量任务)
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000_000; i++) {
        executor.submit(() -> {
            // 阻塞操作不会阻塞平台线程
            Thread.sleep(Duration.ofSeconds(1));
            processRequest();
        });
    }
} // try-with-resources 自动关闭，等待所有任务完成
```

### 平台线程 vs 虚拟线程

| 特性 | 平台线程 | 虚拟线程 |
|------|----------|----------|
| **底层映射** | 1:1 映射到 OS 线程 | M:N 映射，多个虚拟线程复用少量 carrier |
| **栈内存** | 固定 ~1MB (可配置) | 初始 ~几百字节，按需增长，存储在堆上 |
| **创建成本** | 高 (系统调用 + 内存分配) | 低 (普通 Java 对象分配) |
| **数量限制** | 受 OS 限制，通常几千 | 百万级，受堆内存限制 |
| **阻塞行为** | 阻塞 OS 线程 | 仅挂起虚拟线程，释放 carrier |
| **调度** | OS 内核调度器 | JVM 内部 ForkJoinPool 调度 |
| **适用场景** | CPU 密集型计算 | I/O 密集型操作 |
| **ThreadLocal** | 正常使用 | 可用但不推荐大量数据 |
| **Thread identity** | 有固定 OS thread ID | 仅有 Java thread ID |

### 示例对比

```java
// 平台线程方案 - 受限于线程池大小
// 10,000 个请求排队等待 200 个线程
try (var executor = Executors.newFixedThreadPool(200)) {
    for (int i = 0; i < 10_000; i++) {
        executor.submit(() -> blockingIO());  // 大量任务排队等待
    }
}

// 虚拟线程方案 - 每个任务一个线程
// 1,000,000 个请求各自拥有独立虚拟线程
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000_000; i++) {
        executor.submit(() -> blockingIO());  // 全部并发执行
    }
}
```

---

## 4. 虚拟线程内部实现

### Continuation 栈帧冻结/恢复机制

虚拟线程的核心是 **Continuation** 机制：能够在任意 yield point 暂停线程执行，将栈帧保存到堆上，稍后再恢复执行。这一机制涉及两种栈的协作：

**v-stack vs h-stack**:
- **v-stack** (vertical stack / OS stack): 平台线程 (carrier thread) 的操作系统栈。虚拟线程运行时，其栈帧位于 carrier 的 v-stack 上
- **h-stack** (heap stack): 堆上存储的栈帧数据。虚拟线程挂起时，栈帧从 v-stack 拷贝到 h-stack

**StackChunk 对象链表结构**:

```
虚拟线程挂起后的堆上表示:

  Continuation 对象
       │
       ▼
  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
  │ StackChunk 0 │────▶│ StackChunk 1 │────▶│ StackChunk 2 │
  │ (最近帧)     │     │ (中间帧)     │     │ (最早帧)     │
  │              │     │              │     │              │
  │ frame A      │     │ frame D      │     │ frame G      │
  │ frame B      │     │ frame E      │     │ frame H      │
  │ frame C      │     │ frame F      │     │              │
  └─────────────┘     └─────────────┘     └─────────────┘
```

每个 `StackChunk` 是一个 Java 对象 (继承自 `jdk.internal.vm.StackChunk`)，包含一段连续的栈帧数据。多个 StackChunk 通过 `parent` 指针形成链表。StackChunk 作为普通 Java 对象受 GC 管理，不需要的栈数据自然被回收。

**Freezing (冻结 / unmounting)**:

当虚拟线程遇到阻塞操作 (如 I/O、`Thread.sleep()`、`LockSupport.park()`)，执行 unmount 流程：

1. 虚拟线程调用 `Continuation.yield()`
2. JVM 将 v-stack 上属于该虚拟线程的栈帧拷贝到堆上的 StackChunk 对象中
3. 更新 Continuation 对象的内部指针，指向 StackChunk 链表头
4. Carrier thread 的 v-stack 被释放，可以运行其他虚拟线程

**Thawing (解冻 / mounting)**:

当虚拟线程被唤醒 (如 I/O 完成、sleep 到期、被 `unpark()`)，执行 mount 流程：

1. 调度器选择一个空闲的 carrier thread
2. 从 StackChunk 链表中将栈帧数据拷贝回 carrier 的 v-stack
3. 恢复 CPU 寄存器状态 (stack pointer, program counter 等)
4. 虚拟线程从上次 yield 的位置继续执行

**快速路径 vs 慢速路径**:

- **快速路径 (fast path)**: 栈帧数据量小 (通常 < 几十个帧)，所有帧都在一个 StackChunk 中，无需 GC barrier，可以直接 `memcpy` 式拷贝。大多数实际场景走快速路径
- **慢速路径 (slow path)**: 栈帧数据量大或跨多个 StackChunk，需要遍历链表；包含 oop (对象引用) 需要 GC barrier 处理；首次 freeze 需要分配新的 StackChunk 对象

```
Freeze/Thaw 流程:

  ┌─────────────────────┐         ┌──────────────────────┐
  │   v-stack (carrier)  │         │   h-stack (heap)     │
  │                      │  freeze │                      │
  │   ┌──────────────┐  │ ──────▶ │   StackChunk chain   │
  │   │ VT 栈帧      │  │         │   (Java 对象)        │
  │   │ frame A      │  │         │                      │
  │   │ frame B      │  │ ◀────── │                      │
  │   │ frame C      │  │  thaw   │                      │
  │   └──────────────┘  │         │                      │
  └─────────────────────┘         └──────────────────────┘
```

### VirtualThread 状态机

`java.lang.VirtualThread` 内部使用一个 `int` 字段 `state` 管理生命周期，定义了以下状态：

| 状态常量 | 值 | 含义 |
|----------|-----|------|
| `NEW` | 0 | 刚创建，尚未启动 |
| `STARTED` | 1 | 已启动，正在初始化 |
| `RUNNING` | 2 | 正在 carrier 上运行 (runnable-mounted) |
| `PARKING` | 3 | 正在执行 park (yield 中) |
| `PARKED` | 4 | 已 park，等待 unpark (unmounted) |
| `PINNED` | 5 | 被 pin 到 carrier (mounted, 无法 yield) |
| `TIMED_PARKING` | 6 | 正在执行带超时的 park |
| `TIMED_PARKED` | 7 | 已 park，带超时 (unmounted) |
| `TIMED_PINNED` | 8 | 被 pin，带超时 (mounted) |
| `UNPARKED` | 9 | 已 unpark，等待重新调度 (unmounted but runnable) |
| `YIELDING` | 10 | 正在让出 carrier |
| `YIELDED` | 11 | 已让出 (unmounted but runnable) |
| `BLOCKING` | 12 | 正在阻塞获取 monitor (JDK 24+, JEP 491) |
| `BLOCKED` | 13 | 已阻塞在 monitor 获取上 (unmounted, JDK 24+, JEP 491) |
| `UNBLOCKED` | 14 | 从 monitor 阻塞中恢复 (unmounted but runnable, JDK 24+, JEP 491) |
| `WAITING` | 15 | 在 Object.wait() 中等待 (JDK 24+, JEP 491) |
| `WAIT` | 16 | 已进入 wait 状态 (waiting in Object.wait, JDK 24+, JEP 491) |
| `TIMED_WAITING` | 17 | 带超时的 Object.wait() (JDK 24+) |
| `TIMED_WAIT` | 18 | 已进入带超时的 wait (waiting in timed-Object.wait, JDK 24+) |
| `TERMINATED` | 99 | 已终止 |

状态转换主要路径:

```
NEW → STARTED → RUNNING ─┬─→ PARKING → PARKED → (unpark) → UNPARKED → RUNNING
                         ├─→ BLOCKING → BLOCKED → UNBLOCKED → RUNNING  (JEP 491)
                         ├─→ WAITING → WAIT → (notify) → RUNNING      (JEP 491)
                         ├─→ YIELDING → YIELDED → RUNNING
                         ├─→ PINNED (无法 unmount)
                         └─→ TERMINATED
```

### ForkJoinPool 调度器

虚拟线程使用专用的 `ForkJoinPool` 作为默认调度器 (与 `ForkJoinPool.commonPool()` 是不同实例)。

**默认配置**:
- **并行度 (parallelism)**: `Runtime.getRuntime().availableProcessors()`，即 CPU 核心数
- **最大池大小 (maximumPoolSize)**: `Math.max(parallelism, 256)`
- **最小可运行数 (minRunnable)**: `Math.max(parallelism / 2, 1)`

**Work-stealing（工作窃取）算法**:

调度器基于 work-stealing 实现高效任务分配：
- 每个 worker thread (即 carrier thread) 维护自己的本地双端队列 (deque)
- 虚拟线程被 unpark 时，优先提交到上次运行的 carrier 的本地队列 (locality 优化)
- 空闲 carrier 从其他 carrier 的队列末端 "偷取" 任务
- 减少锁竞争，提高缓存命中率

**补偿并行度 (Compensating parallelism)**:

当虚拟线程被 pin 到 carrier (无法 unmount) 时，调度器会检测到活跃 carrier 数量下降。如果低于 `minRunnable` 阈值，调度器会临时创建新的 carrier thread 来补偿，确保其他虚拟线程不会饥饿 (starvation)。这就是最大池大小设为 256 的原因——为 pinning 场景预留余量。

**系统属性配置**:

```bash
# 设置调度器并行度 (carrier thread 数量)
-Djdk.virtualThreadScheduler.parallelism=16

# 设置最大池大小 (含补偿线程)
-Djdk.virtualThreadScheduler.maxPoolSize=512

# 设置最小可运行线程数 (低于此值触发补偿)
-Djdk.virtualThreadScheduler.minRunnable=4
```

### CarrierThread 工作原理

Carrier thread 是实际执行虚拟线程代码的平台线程。它是 `ForkJoinWorkerThread` 的子类 `CarrierThread`。

```
// 伪代码 (pseudocode)
CarrierThread 运行循环 (简化):

while (true) {
    VirtualThread vt = scheduler.poll();  // 获取待运行的虚拟线程
    if (vt != null) {
        vt.mount(this);                   // 将虚拟线程挂载到当前 carrier
        vt.continuation.run();            // 执行虚拟线程代码
        // 如果 continuation yield 了，虚拟线程已 unmount
        // 如果 continuation 完成了，虚拟线程终止
    } else {
        stealWork();                      // 从其他 carrier 偷取任务
    }
}
```

**Mount / Unmount 过程**:
- **Mount**: 将虚拟线程的 `Thread.currentThread()` 设置为该虚拟线程 (而非 carrier)，恢复 h-stack 到 v-stack
- **Unmount**: 保存 v-stack 到 h-stack，将 `Thread.currentThread()` 恢复为 carrier thread 本身

`Thread.currentThread()` 在虚拟线程运行期间返回虚拟线程对象，而非底层 carrier。这保证了现有代码的兼容性——代码无需知道自己运行在虚拟线程还是平台线程上。

---

## 5. JEP 491 深入: Monitor 重新实现

### 旧实现的问题 (JDK 21-23)

在 JDK 21-23 中，`synchronized` 块使用 OS 级别的 monitor 实现。monitor 的所有权与 OS 线程 (即 carrier thread) 绑定。当虚拟线程进入 `synchronized` 块后：

- Monitor 记录的 owner 是 carrier thread 的 OS thread ID
- 虚拟线程无法从 carrier 上 unmount (因为 monitor 不认识虚拟线程)
- 如果在 `synchronized` 块内执行阻塞操作，carrier thread 被白白占用
- 这就是 **pinning（固定）** 问题：虚拟线程被 "钉" 在 carrier 上

```java
// JDK 21-23: 这段代码会导致 pinning
synchronized (sharedResource) {
    // carrier thread 被占用，无法服务其他虚拟线程
    var result = httpClient.send(request, bodyHandler);  // 阻塞!
}
```

在高并发场景下，大量虚拟线程被 pin，会耗尽 carrier pool，导致性能严重退化。

### 新实现 (JDK 24, JEP 491)

JEP 491 从根本上重构了 monitor 实现，使虚拟线程可以在持有 monitor 的情况下挂起和恢复。

**核心变化: LockStack 冻结到 StackChunk**

新实现引入了 **LockStack** 概念——一个轻量级的数据结构，记录当前线程持有的所有 monitor。当虚拟线程执行 unmount 时：

1. LockStack 中记录的 monitor 所有权信息被保存到 StackChunk 中 (随栈帧一起冻结)
2. Monitor 的 owner 从 carrier thread 转移为虚拟线程的 identity
3. Carrier thread 被释放，可以运行其他虚拟线程
4. 当虚拟线程恢复时，LockStack 和 monitor 所有权一并恢复

**4 个核心实现提交**:

| 提交 | 内容 | 说明 |
|------|------|------|
| #1 | Unmount with monitors held | 允许持有 monitor 的虚拟线程 unmount |
| #2 | Blocked on monitor acquire | 虚拟线程在等待获取 monitor 时可以 unmount |
| #3 | Object.wait() support | `Object.wait()` 在虚拟线程中正确释放 monitor 并 unmount |
| #4 | Tests and diagnostics | 全面的测试覆盖和诊断支持 |

### JEP 491 新增的 VirtualThread 状态

为支持 monitor 操作的正确语义，新增了以下状态：

- **BLOCKING**: 虚拟线程正在尝试获取一个被其他线程持有的 monitor，正在执行 unmount
- **BLOCKED**: 虚拟线程已 unmount，等待 monitor 可用
- **UNBLOCKED**: monitor 已可用，虚拟线程等待被重新调度到 carrier 上
- **WAITING**: 虚拟线程调用了 `Object.wait()`，正在执行 unmount
- **WAIT**: 虚拟线程已 unmount，等待 `Object.notify()` / `notifyAll()`

### Object.wait() 行为变化

JDK 24 之前，虚拟线程在 `synchronized` 块内调用 `Object.wait()` 会导致 pinning。JDK 24+ 中：

```java
// JDK 24+: Object.wait() 正确释放 monitor 并 unmount 虚拟线程
synchronized (obj) {
    while (!condition) {
        obj.wait();  // 虚拟线程 unmount，carrier 被释放
    }
}
```

`Object.wait()` 现在会：
1. 释放 monitor
2. 将虚拟线程的栈帧和 LockStack 冻结到 StackChunk
3. Unmount 虚拟线程
4. 当 `notify()` 被调用时，虚拟线程重新进入调度队列
5. 被调度后 mount 到 carrier，重新获取 monitor，从 `wait()` 返回

### 剩余 pinning 场景

JEP 491 解决了 `synchronized` 的 pinning 问题，但以下场景仍会导致 pinning：

| 场景 | 原因 | 建议 |
|------|------|------|
| **Native/JNI 帧在栈上** | native 代码的栈帧无法安全地冻结/恢复 | 避免在虚拟线程中长时间执行 native 调用 |
| **Foreign Function & Memory (FFM) API** | 与 native 相同的限制 | 使用专用平台线程调用 foreign function |
| **类加载过程中** | 类加载涉及复杂的 JVM 内部锁 | 通常是短暂的，影响有限 |
| **类初始化器 (class initializer)** | `<clinit>` 方法执行期间持有初始化锁 | 避免在类初始化器中执行阻塞操作 |

**监控 pinning**: JEP 444 引入的系统属性 `jdk.tracePinnedThreads` 在 JDK 24 中已移除。改用 JFR 事件 `jdk.VirtualThreadPinned` 监控剩余 pinning 场景。

```bash
# 使用 JFR 监控 pinning
java -XX:StartFlightRecording=filename=pinning.jfr,settings=profile MyApp

# 事后分析
jfr print --events jdk.VirtualThreadPinned pinning.jfr
```

---

## 6. 结构化并发

### API 演进

| 版本 | JEP | 变化 |
|------|-----|------|
| JDK 21 | JEP 453 | 第一次预览 |
| JDK 22 | JEP 462 | 第二次预览 |
| JDK 23 | JEP 480 | 第三次预览 |
| JDK 24 | JEP 499 | 第四次预览 |
| JDK 25 | JEP 505 | 第五次预览 - 重大 API 重构：构造函数改为静态工厂方法，引入 Joiner 接口 |
| JDK 26 | JEP 525 | 第六次预览 |

### 核心概念 (JDK 25+ API)

结构化并发的核心思想：并发任务的生命周期与代码的词法作用域 (lexical scope) 一致。子任务不能逃逸出父作用域，父作用域关闭时所有子任务必须已完成。

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

Joiner 定义了子任务的完成策略。JDK 25+ 提供多种内置 Joiner：

```java
// 1. anySuccessfulOrThrow: 返回第一个成功的结果，取消其余
try (var scope = StructuredTaskScope.open(
        Joiner.anySuccessfulOrThrow())) {
    scope.fork(() -> fetchFromSourceA());
    scope.fork(() -> fetchFromSourceB());
    scope.fork(() -> fetchFromSourceC());

    return scope.join();  // 返回最先成功的结果

} catch (InterruptedException e) {
    throw new RuntimeException(e);
}

// 2. allSuccessfulOrThrow: 等待全部完成，任一失败则抛异常
try (var scope = StructuredTaskScope.open(
        Joiner.allSuccessfulOrThrow())) {
    scope.fork(() -> validateA());
    scope.fork(() -> validateB());

    List<ValidationResult> results = scope.join();
}

// 3. 带超时的 scope: 使用 Configuration.withTimeout()
try (var scope = StructuredTaskScope.open(
        Joiner.allSuccessfulOrThrow(),
        cf -> cf.withTimeout(Duration.ofSeconds(5)))) {
    scope.fork(() -> slowOperation());
    return scope.join();  // 超时后抛出 TimeoutException
}
```

### 与 ScopedValue 的协作

结构化并发中的子任务自动继承父任务的 ScopedValue 绑定：

```java
static final ScopedValue<UserContext> CTX = ScopedValue.newInstance();

void handleRequest(UserContext ctx) {
    ScopedValue.where(CTX, ctx).run(() -> {
        try (var scope = StructuredTaskScope.open()) {
            // 子任务自动继承 CTX 绑定
            scope.fork(() -> {
                UserContext inherited = CTX.get();  // 可以访问!
                return processWithContext(inherited);
            });
            scope.join();
        }
    });
}
```

---

## 7. Scoped Values 深入 (JEP 506)

### vs ThreadLocal 详细对比

| 维度 | ThreadLocal | ScopedValue |
|------|-------------|-------------|
| **可变性** | 可变 (`set()` 可随时修改) | 不可变 (绑定后不可修改) |
| **生命周期** | 无限制 (直到 `remove()` 或线程终止) | 有界 (`where().run()` 的作用域) |
| **继承** | `InheritableThreadLocal` 需拷贝 | 零拷贝自动继承到子虚拟线程 |
| **性能** | 每次 `get()` 需要查找 ThreadLocalMap | 编译器优化，接近直接字段访问 |
| **内存** | 百万虚拟线程 x per-thread 存储 = 内存爆炸 | 共享绑定对象，内存恒定 |
| **内存泄漏** | 常见 (忘记 `remove()`) | 不可能 (作用域结束自动清理) |
| **重绑定 (rebinding)** | `set()` 随意修改 | 只能在嵌套作用域中遮蔽 (shadow) |
| **数据流向** | 不确定 (任何代码都可修改) | 明确 (从 `where()` 到 `run()`) |

### ScopedValue.where().run() 机制

```java
// 声明一个 ScopedValue (通常是 static final)
static final ScopedValue<String> REQUEST_ID = ScopedValue.newInstance();

// 绑定值并执行
ScopedValue.where(REQUEST_ID, "req-12345").run(() -> {
    // 在此作用域内，REQUEST_ID 绑定到 "req-12345"
    handleRequest();
});

// 作用域外，REQUEST_ID 未绑定
// REQUEST_ID.get() 会抛 NoSuchElementException

// 嵌套绑定 (遮蔽外层)
ScopedValue.where(REQUEST_ID, "req-outer").run(() -> {
    System.out.println(REQUEST_ID.get());  // "req-outer"

    ScopedValue.where(REQUEST_ID, "req-inner").run(() -> {
        System.out.println(REQUEST_ID.get());  // "req-inner" (遮蔽外层)
    });

    System.out.println(REQUEST_ID.get());  // "req-outer" (恢复)
});

// 多个绑定可以链式调用
ScopedValue.where(REQUEST_ID, "req-123")
           .where(USER_NAME, "Alice")
           .run(() -> {
               // 两个值都可用
           });
```

### 与 StructuredTaskScope 的交互

ScopedValue 的绑定在 `StructuredTaskScope.fork()` 创建的子任务中**自动继承**，无需额外操作：

```java
static final ScopedValue<Principal> PRINCIPAL = ScopedValue.newInstance();

Response serve(Request request) {
    Principal user = authenticate(request);

    return ScopedValue.where(PRINCIPAL, user).call(() -> {
        try (var scope = StructuredTaskScope.open(
                Joiner.allSuccessfulOrThrow())) {

            // 每个 fork 的子任务都可以访问 PRINCIPAL
            scope.fork(() -> authorize(PRINCIPAL.get()));
            scope.fork(() -> fetchData(PRINCIPAL.get()));
            scope.fork(() -> auditLog(PRINCIPAL.get()));

            return scope.join();
        }
    });
}
```

这种设计是刻意的：ScopedValue 与结构化并发共同构成一个完整的并发编程模型。绑定沿着任务树向下传播，而任务的生命周期受 scope 约束。

### 为什么 ThreadLocal 在虚拟线程环境下有问题

```java
// 问题场景: Web 服务器每请求一个虚拟线程
static final ThreadLocal<RequestContext> CTX = new ThreadLocal<>();

void handleRequest(Request req) {
    CTX.set(new RequestContext(req));  // 每线程一份
    try {
        process();
    } finally {
        CTX.remove();  // 容易忘记!
    }
}

// 如果有 1,000,000 个并发虚拟线程:
// - 1,000,000 个 ThreadLocalMap 实例
// - 1,000,000 个 RequestContext 对象
// - 即使 RequestContext 很小 (如 100 bytes)，也需要 ~100MB

// ScopedValue 方案:
static final ScopedValue<RequestContext> CTX = ScopedValue.newInstance();

void handleRequest(Request req) {
    ScopedValue.where(CTX, new RequestContext(req)).run(() -> {
        process();  // 无内存泄漏风险，作用域结束自动清理
    });
}
```

此外，`InheritableThreadLocal` 在创建子线程时需要**拷贝**父线程的所有 ThreadLocal 数据。百万级虚拟线程场景下，这个拷贝开销巨大。ScopedValue 则是零拷贝——子任务直接引用父任务的绑定栈。

---

## 8. 性能基准

> **注意**: 性能数据高度依赖具体工作负载、硬件配置和 JVM 版本。以下数据来自各项目官方发布的基准测试，仅供参考。实际性能请以自身应用的测试结果为准。

### I/O 密集型场景

**Spring Boot 虚拟线程基准** (来源: Spring 团队 2023 年博客及社区基准测试):
- 典型 Web 应用 (数据库查询 + HTTP 调用) 在特定工作负载下：
  - 吞吐量提升约 2-3x (因减少了线程切换和排队等待)
  - P99 延迟降低约 50-60% (因消除了线程池排队延迟)
- 关键前提: 应用确实是 I/O bound，且原有线程池是瓶颈

**Helidon 4 基准** (来源: Oracle Helidon 团队发布):
- Helidon 4 SE (虚拟线程) vs Helidon 3 MP (传统线程池): 在特定 REST 微服务工作负载下吞吐量提升约 3-4x
- 原因: Helidon 4 完全移除了 Netty reactive pipeline，改用虚拟线程的阻塞 I/O，减少了 reactive 编程模型的调度开销

### CPU 密集型场景

虚拟线程在 CPU 密集型任务中**不会**带来性能提升：
- 虚拟线程的优势在于挂起/恢复 (避免阻塞 carrier)
- CPU 密集任务不会挂起，虚拟线程始终占用 carrier
- 性能与使用等量平台线程基本相当
- 额外的 mount/unmount 和调度开销可能导致**轻微**性能下降 (通常 < 5%)

### 内存效率

| 指标 | 平台线程 | 虚拟线程 |
|------|----------|----------|
| **10,000 线程内存** | ~10 GB (1MB x 10K) | ~几十 MB (取决于栈深度) |
| **创建 100K 线程耗时** | 数十秒或失败 | 约 1-2 秒 (特定硬件下) |
| **上下文切换** | OS 级切换 (~1-10us) | JVM 内部切换 (~ns 级别) |

### 何时有效 / 何时无效

```
有效场景 (I/O bound):              无效场景 (CPU bound):
┌─────────────────────────┐        ┌─────────────────────────┐
│ Web 服务 (REST/gRPC)    │        │ 科学计算               │
│ 数据库访问              │        │ 图像/视频处理           │
│ 微服务间调用            │        │ 加密运算               │
│ 文件 I/O               │        │ 数据压缩               │
│ 消息队列消费            │        │ ML 推理                │
└─────────────────────────┘        └─────────────────────────┘
```

---

## 9. 生态系统适配

### Spring Boot

Spring Boot 从 3.2 开始支持虚拟线程，4.0 进一步增强：

```properties
# Spring Boot 3.2+: 启用虚拟线程
spring.threads.virtual.enabled=true
```

启用后，嵌入式 Tomcat/Jetty/Undertow 会使用虚拟线程处理请求，`@Async` 方法也在虚拟线程上执行。

```java
// Spring Boot 自动配置后，每个请求在虚拟线程中处理
@RestController
public class UserController {
    @GetMapping("/users/{id}")
    public User getUser(@PathVariable Long id) {
        // 同步阻塞代码，虚拟线程自动处理
        return userRepository.findById(id).orElseThrow();
    }
}
```

**注意事项**:
- JDBC 连接池 (如 HikariCP) 的最大连接数成为新瓶颈——虚拟线程无限但数据库连接有限
- 需要配置 `spring.datasource.hikari.maximum-pool-size` 与实际数据库负载匹配
- Spring WebFlux (响应式) 与虚拟线程是互斥的方案，不应同时使用

### Quarkus

Quarkus 通过 `@RunOnVirtualThread` 注解支持虚拟线程：

```java
@Path("/users")
public class UserResource {

    @GET
    @RunOnVirtualThread  // Quarkus 特有注解
    public List<User> list() {
        return userRepository.listAll();  // 阻塞操作在虚拟线程上执行
    }
}
```

Quarkus 团队正在考虑在未来版本中将虚拟线程作为默认执行模型 (取代当前的 Vert.x event loop + worker thread pool 混合模型)。

### Helidon 4

Helidon 4 是第一个完全基于虚拟线程构建的 Java 框架：

- **完全移除 Netty**: 使用基于虚拟线程的阻塞 HTTP server 替代 Netty reactive pipeline
- **SE 和 MP 统一**: Helidon SE (functional) 和 MP (MicroProfile) 共享同一虚拟线程运行时
- **开发者体验**: 无需了解 reactive 概念，直接写阻塞代码

```java
// Helidon 4 SE: 简单阻塞式 HTTP server
WebServer.builder()
    .routing(rules -> rules
        .get("/hello", (req, res) -> {
            // 每个请求在独立虚拟线程中处理
            String data = blockingDatabaseCall();
            res.send(data);
        }))
    .build()
    .start();
```

### JDBC / 数据库驱动兼容性

| 驱动 | 虚拟线程兼容性 | 备注 |
|------|---------------|------|
| **HikariCP** | 兼容 | 连接池大小成为瓶颈，需合理配置 |
| **PostgreSQL JDBC** | 兼容 | 42.6.0+ 优化了虚拟线程支持 |
| **MySQL Connector/J** | 兼容 | 8.1+ 改善了 pinning 行为 |
| **Oracle JDBC** | 兼容 | 23c 驱动优化了虚拟线程体验 |
| **R2DBC (响应式)** | 不适用 | 虚拟线程方案无需使用 R2DBC |

**关键陷阱**: 虚拟线程数量不受限，但数据库连接数有限。必须使用连接池 (如 HikariCP) 限制并发数据库连接。否则可能导致数据库连接池被瞬间耗尽。

→ 详见 [Section 10.6 反模式 6](#反模式-6-忽视背压-backpressure) 的 Semaphore 背压模式。

### 日志框架注意事项

- **Thread name**: 虚拟线程默认名称为空字符串，日志中 `%t` 显示为空。建议使用 `Thread.ofVirtual().name("worker-", 0)` 命名
- **MDC (Mapped Diagnostic Context)**: MDC 基于 ThreadLocal，百万虚拟线程场景下可能导致内存问题。部分框架 (如 Log4j2 3.x) 正在适配 ScopedValue
- **日志量**: 百万虚拟线程可能产生巨大日志量，需注意日志级别和异步日志配置

---

## 10. 陷阱与反模式

### 反模式 1: 池化虚拟线程

```java
// !! 池化虚拟线程完全违背设计初衷
ExecutorService pool = Executors.newFixedThreadPool(100,
    Thread.ofVirtual().factory());  // 用虚拟线程工厂创建固定大小线程池

// 问题:
// - 虚拟线程极其轻量，无需复用
// - 固定池大小重新引入了虚拟线程要解决的问题 (线程数限制)
// - 池化带来不必要的管理开销

// 正确做法: 每个任务一个虚拟线程
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
```

**原因**: 虚拟线程的设计哲学是 "one task, one thread"。创建和销毁虚拟线程的成本极低，池化节省不了什么，反而限制了并发度。

### 反模式 2: CPU 密集任务使用虚拟线程

```java
// !! CPU 密集任务不应使用虚拟线程
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1000; i++) {
        executor.submit(() -> {
            // 纯 CPU 计算，不会 yield
            return fibonacci(1_000_000);
        });
    }
}

// 问题:
// - 虚拟线程不会挂起 (没有 I/O 或阻塞操作)
// - 大量虚拟线程争抢有限的 carrier，增加调度开销
// - 无法利用虚拟线程的核心优势

// 正确做法: CPU 密集任务使用 ForkJoinPool 或固定大小平台线程池
ForkJoinPool pool = new ForkJoinPool(Runtime.getRuntime().availableProcessors());
pool.submit(() -> {
    return fibonacci(1_000_000);
});
```

### 反模式 3: 大量 ThreadLocal 数据

```java
// !! 每个虚拟线程独立的 ThreadLocal 副本
static final ThreadLocal<byte[]> BUFFER = ThreadLocal.withInitial(() -> new byte[1024 * 1024]);

void processRequest() {
    byte[] buf = BUFFER.get();  // 每个虚拟线程分配 1MB
    // 1,000,000 虚拟线程 × 1MB = ~1TB 内存!
}

// 正确做法 1: 使用 ScopedValue
static final ScopedValue<byte[]> BUFFER = ScopedValue.newInstance();

void processRequest() {
    byte[] shared = acquireBuffer();  // 从池中获取
    ScopedValue.where(BUFFER, shared).run(() -> {
        // 使用 BUFFER.get()
    });
    releaseBuffer(shared);
}

// 正确做法 2: 使用局部变量
void processRequest() {
    byte[] buf = new byte[4096];  // 栈上分配，虚拟线程栈按需增长
    // ...
}
```

### 反模式 4: Thread.yield() 期望

```java
// !! Thread.yield() 在虚拟线程中的行为
Thread.startVirtualThread(() -> {
    while (computing) {
        compute();
        Thread.yield();  // 期望让出 carrier 给其他虚拟线程
    }
});

// 问题:
// - Thread.yield() 对虚拟线程的效果取决于 JVM 实现
// - 虚拟线程的调度由 ForkJoinPool 控制，yield 可能没有预期效果
// - 不应依赖 yield 来实现协作调度

// 如果需要让出执行:
// - I/O 操作自然会让出 carrier
// - 可以使用 Thread.sleep(Duration.ZERO) 或 LockSupport.park()
```

### 反模式 5: 假设虚拟线程绑定到固定 carrier

```java
// !! 假设 carrier 不变
Thread.startVirtualThread(() -> {
    long carrierId = getCarrierThreadId();  // 第一次获取 carrier ID
    doSomeIO();                              // 阻塞操作导致 unmount + remount
    assert carrierId == getCarrierThreadId();  // 可能失败!
});

// 问题:
// - 虚拟线程在每次 unmount/remount 后可能运行在不同的 carrier 上
// - 任何依赖 carrier 线程 identity 的逻辑都是错误的
// - 例如: 某些 native 库使用 OS thread ID 做缓存 key

// 正确做法: 使用虚拟线程自己的 ID
long threadId = Thread.currentThread().threadId();  // 虚拟线程 ID 是稳定的
```

### 反模式 6: 忽视背压 (backpressure)

```java
// !! 无限制创建虚拟线程 + 有限下游资源
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (var message : messageQueue) {  // 可能有数百万消息
        executor.submit(() -> {
            // 所有虚拟线程同时冲击数据库
            database.insert(transform(message));  // 数据库崩溃!
        });
    }
}

// 正确做法: 使用 Semaphore 控制背压
Semaphore permits = new Semaphore(100);  // 最多 100 并发

try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (var message : messageQueue) {
        permits.acquire();  // throws InterruptedException
        executor.submit(() -> {
            try {
                database.insert(transform(message));
            } finally {
                permits.release();
            }
        });
    }
} // 注意: 外层方法需声明 throws InterruptedException 或添加 try-catch
```

---

## 11. 时间线

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
| **2023** | JDK 21 | Scoped Values (第一预览, JEP 446) |
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


> [完整时间线](timeline.md)

---

## 12. 核心贡献者

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| [Ron Pressler](/by-contributor/profiles/ron-pressler.md) | Oracle | 项目领导人，Continuation 实现 |
| [Alan Bateman](/by-contributor/profiles/alan-bateman.md) | Oracle | 并发基础设施，VirtualThread 类 |
| [David Holmes](/by-contributor/profiles/david-holmes.md) | Oracle | 线程实现，monitor 重构 |

---

## 13. 迁移指南

### 从线程池迁移

```java
// 旧代码
ExecutorService executor = Executors.newFixedThreadPool(200);

// 新代码 - 直接替换
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
```

> 注意: 如果原有线程池大小是有意限制并发度 (如保护数据库)，迁移到虚拟线程后需要使用 `Semaphore` 替代线程池的限流作用。

### 从异步 API 迁移

```java
// 旧代码: CompletableFuture 链式调用
public CompletableFuture<Response> fetchData(Request req) {
    return CompletableFuture.supplyAsync(() -> fetchUser(req), executor)
        .thenCombine(
            CompletableFuture.supplyAsync(() -> fetchOrder(req), executor),
            (user, order) -> new Response(user, order)
        );
}

// 新代码: 虚拟线程 + 结构化并发
public Response fetchData(Request req) {
    try (var scope = StructuredTaskScope.open()) {
        var user = scope.fork(() -> fetchUser(req));
        var order = scope.fork(() -> fetchOrder(req));
        scope.join();
        return new Response(user.get(), order.get());
    }
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

### 迁移检查清单

| 检查项 | 说明 |
|--------|------|
| ThreadLocal 用量 | 评估是否可迁移到 ScopedValue |
| synchronized 用量 | JDK 24+ 无需修改；JDK 21-23 考虑改用 ReentrantLock |
| 线程池大小依赖 | 如果线程池大小用于限流，改用 Semaphore |
| Native/JNI 调用 | 评估 pinning 影响，考虑隔离到平台线程 |
| 连接池配置 | 虚拟线程无限但连接有限，调整连接池参数 |
| 日志配置 | 确认 MDC、线程名在虚拟线程下正常工作 |

---

## 14. 监控与调试

### JFR 事件

```bash
# 启用虚拟线程相关 JFR 记录
java -XX:StartFlightRecording=filename=vthreads.jfr \
     -XX:FlightRecorderOptions=vthread=true \
     MyApp
```

相关 JFR 事件:
- `jdk.VirtualThreadStart` / `jdk.VirtualThreadEnd`: 虚拟线程生命周期
- `jdk.VirtualThreadPinned`: 虚拟线程被 pin 到 carrier (JDK 24+)
- `jdk.VirtualThreadSubmitFailed`: 虚拟线程无法提交到调度器

### 线程转储

```bash
# jcmd JSON 格式线程转储 (推荐，结构化输出)
jcmd <pid> Thread.dump_to_file -format=json vthreads.json

# jstack 传统格式
jstack <pid>

# 输出包含:
# "VirtualThread-123" #123 virtual
#    java.base/java.lang.VirtualThread.park(VirtualThread.java:...)
#    java.base/java.lang.System$2.parkVirtualThread(System.java:...)
#    java.base/jdk.internal.misc.VirtualThreads.park(VirtualThreads.java:...)
```

### 监控 API

```java
// 检查是否为虚拟线程
Thread thread = Thread.currentThread();
boolean isVirtual = thread.isVirtual();

// 虚拟线程不支持 ThreadGroup (总是返回 VirtualThreads 组)
ThreadGroup group = thread.getThreadGroup();  // "VirtualThreads"

// 虚拟线程不支持 setDaemon() (总是 daemon)
thread.isDaemon();  // 总是 true

// 虚拟线程不支持 setPriority() (总是 NORM_PRIORITY)
thread.getPriority();  // 总是 Thread.NORM_PRIORITY
```

### 调试技巧

```bash
# 1. 查看调度器状态 (carrier 线程数)
jcmd <pid> Thread.print | grep "ForkJoinPool-"

# 2. JFR 分析 pinning 热点
jfr print --events jdk.VirtualThreadPinned --stack-depth 20 recording.jfr

# 3. 使用 -Djdk.tracePinnedThreads=full (仅 JDK 21-23)
# JDK 24+ 已移除此选项，使用 JFR 替代
```

---

## 15. 最佳实践

### DO

```java
// 1. I/O 密集任务使用虚拟线程
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> handleHttpRequest());
}

// 2. 使用结构化并发管理任务组 (JDK 25+ API)
try (var scope = StructuredTaskScope.open()) {
    var a = scope.fork(() -> fetchA());
    var b = scope.fork(() -> fetchB());
    scope.join();
    return combine(a.get(), b.get());
}

// 3. 使用 ScopedValue 替代 ThreadLocal (JDK 25+)
static final ScopedValue<Context> CTX = ScopedValue.newInstance();
ScopedValue.where(CTX, context).run(() -> handle());

// 4. 使用 Semaphore 保护有限资源
//    → 详见 Section 10.6 反模式 6

// 5. 给虚拟线程命名以便调试
Thread.ofVirtual().name("request-handler-", 0).start(task);
```

### DON'T

```java
// 1. 不要池化虚拟线程
Executors.newFixedThreadPool(100, Thread.ofVirtual().factory());

// 2. 不要对 CPU 密集任务使用虚拟线程
// 使用 ForkJoinPool 或平台线程

// 3. 不要在虚拟线程中使用大的 ThreadLocal
ThreadLocal<byte[]> BIG = ThreadLocal.withInitial(() -> new byte[1_000_000]);

// 4. 不要假设 carrier 线程不变
// 每次阻塞后虚拟线程可能在不同 carrier 上恢复

// 5. 不要忽略背压
// 虚拟线程无限 + 有限下游资源 = 灾难

// 6. 不要在 JDK 21-23 的 synchronized 中做长时间阻塞 (JDK 24+ 已修复)
```

---

## 16. 参考资料

### JEP 引用

- [JEP 425](https://openjdk.org/jeps/425) - 虚拟线程 (第一预览, JDK 19)
- [JEP 436](/jeps/concurrency/jep-436.md) - 虚拟线程 (第二预览, JDK 20)
- [JEP 444](/jeps/concurrency/jep-444.md) - 虚拟线程 (正式, JDK 21)
- [JEP 453](/jeps/concurrency/jep-453.md) - 结构化并发 (第一预览, JDK 21)
- [JEP 462](https://openjdk.org/jeps/462) - 结构化并发 (第二预览, JDK 22)
- [JEP 464](https://openjdk.org/jeps/464) - Scoped Values (第二预览, JDK 22)
- [JEP 480](https://openjdk.org/jeps/480) - 结构化并发 (第三预览, JDK 23)
- [JEP 481](https://openjdk.org/jeps/481) - Scoped Values (第三预览, JDK 23)
- [JEP 487](https://openjdk.org/jeps/487) - Scoped Values (第四预览, JDK 24)
- [JEP 491](https://openjdk.org/jeps/491) - 虚拟线程不再 Pin synchronized (JDK 24)
- [JEP 499](https://openjdk.org/jeps/499) - 结构化并发 (第四预览, JDK 24)
- [JEP 505](https://openjdk.org/jeps/505) - 结构化并发 (第五预览, JDK 25)
- [JEP 506](https://openjdk.org/jeps/506) - Scoped Values (正式, JDK 25)
- [JEP 525](https://openjdk.org/jeps/525) - 结构化并发 (第六预览, JDK 26)

### 外部资料

- [Project Loom Official Page](https://openjdk.org/projects/loom/)
- [Ron Pressler - "Loom: Bringing Lightweight Threads to Java" (JVM Language Summit)](https://www.youtube.com/results?search_query=ron+pressler+loom+jvmls)
- [Inside Java - Virtual Threads](https://inside.java/tag/loom)
- [Spring Boot Virtual Threads Documentation](https://docs.spring.io/spring-boot/reference/features/task-execution-and-scheduling.html)
- [Helidon 4 Architecture](https://helidon.io/docs/v4/about/architecture)

> [时间线](timeline.md) | [并发主题](../../concurrency/)
