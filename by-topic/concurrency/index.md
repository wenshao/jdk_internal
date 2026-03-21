# 并发网络

多线程、网络通信、异步编程。

[← 返回主题索引](../)

---
## 目录

1. [演进概览](#1-演进概览)
2. [OpenJDK 项目](#2-openjdk-项目)
3. [主题列表](#3-主题列表)
4. [核心贡献者](#4-核心贡献者)
5. [重要 PR 分析](#5-重要-pr-分析)
6. [内部开发者资源](#6-内部开发者资源)
7. [统计数据](#7-统计数据)
8. [学习路径](#8-学习路径)

---


## 1. 演进概览

```
JDK 1.0 ── JDK 5 ── JDK 7 ── JDK 11 ── JDK 19 ── JDK 21 ── JDK 24 ── JDK 25 ── JDK 26
   │          │          │          │          │          │          │          │          │
 Thread    Executor   NIO     HTTP Client Virtual    分代 ZGC   解除      Scoped    Structured
 Runnable  ForkJoin   AJS     Completable Thread     Structured  Pin 限制  Values   Concurrency
 Locks     Future     Async   Future(正式) (正式)    Concurrency JEP 491  (正式)    (正式)
                                                     预览                 JEP 506   JEP 507
```

### 版本里程碑

| 版本 | 主题 | 关键特性 |
|------|------|----------|
| **JDK 5** | 并发基础 | Executor 框架、并发集合、锁 |
| **JDK 7** | 异步 I/O | AsynchronousSocketChannel、Fork/Join |
| **JDK 8** | 函数式并发 | CompletableFuture、Parallel Stream |
| **JDK 11** | HTTP 标准化 | HTTP Client 正式版 |
| **JDK 19** | 虚拟线程预览 | Virtual Threads (预览) |
| **JDK 21** | 并发革命 | Virtual Threads (正式)、Scoped Values (预览) |
| **JDK 24** | Pin 问题修复 | 虚拟线程不再 Pin (JEP 491)、Structured Concurrency 第四次预览 (JEP 499) |
| **JDK 25** | 值类型正式化 | Scoped Values 正式版 (JEP 506)、Structured Concurrency 第五次预览 (JEP 505)、Stable Values 预览 (JEP 502) |
| **JDK 26** | 并发正式化 | Structured Concurrency 正式版 (JEP 507)、HTTP/3 预览 (JEP 517) |

---

## 2. OpenJDK 项目

### [Project Loom](../core/loom/)

虚拟线程和结构化并发。

| 特性 | 版本 | JEP |
|------|------|-----|
| 虚拟线程 | JDK 21 | JEP 444 |
| 虚拟线程不再 Pin | JDK 24 | JEP 491 |
| 结构化并发 (预览 → 正式) | JDK 21-25 预览, JDK 26 正式 | JEP 453→462→480→499→505→525→507 |
| Scoped Values (预览 → 正式) | JDK 21-24 预览, JDK 25 正式 | JEP 446→506 |
| Stable Values (预览) | JDK 25 | JEP 502 |

→ [Loom 时间线](../core/loom/timeline.md)

---

## 3. 主题列表

### [并发编程](concurrency/)

从 Thread 到 Virtual Thread 的演进。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 5 | Executor 框架 | JSR-166 |
| JDK 7 | Fork/Join 框架 | JSR-166y |
| JDK 8 | Lambda、Parallel Stream | JEP 126 |
| JDK 8 | CompletableFuture | JEP 155 |
| JDK 9 | CompletableFuture 改进、Reactive Streams | JEP 266 |
| JDK 19 | **Virtual Threads** (预览) | JEP 425 |
| JDK 20 | Virtual Threads (第二次预览) | JEP 436 |
| JDK 21 | **Virtual Threads** (正式)、**Structured Concurrency** (预览)、**Scoped Values** (预览) | JEP 444, JEP 453, JEP 446 |
| JDK 22-23 | Structured Concurrency (持续预览) | JEP 462, 480 |
| JDK 24 | **虚拟线程不再 Pin** (synchronized 不再阻塞载体线程)、Structured Concurrency 第四次预览 | JEP 491, JEP 499 |
| JDK 25 | **Scoped Values** (正式)、Structured Concurrency 第五次预览 (静态工厂方法替代构造器)、**Stable Values** 预览 | JEP 506, JEP 505, JEP 502 |
| JDK 26 | **Structured Concurrency** (正式, 新增 onTimeout() 方法) | JEP 507 |

→ [并发时间线](concurrency/timeline.md)

### [HTTP 客户端](http/)

从 HttpURLConnection 到 HTTP/3。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 1.0 | HttpURLConnection | - |
| JDK 9 | HTTP Client (孵化器) | JEP 110 |
| JDK 10 | HTTP Client (孵化器) | - |
| JDK 11 | **HTTP Client** (标准) | JEP 321 |
| JDK 22-23 | 连接复用优化 | - |
| JDK 26 | **HTTP/3** (预览) | JEP 517 |

→ [HTTP 演进时间线](http/timeline.md)

### [网络编程](network/)

Java 网络编程从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 1.0 | Socket/ServerSocket | TCP/UDP 基础 |
| JDK 1.1 | URL/HttpURLConnection | HTTP 支持 |
| JDK 5 | URLHandler | 自定义协议 |
| JDK 7 | Asynchronous I/O | 异步网络 |
| JDK 9 | HTTP/2 | 多路复用 |
| JDK 11 | HTTP Client 标准化 | 新 API |
| JDK 16 | Unix Domain Socket | 本地 IPC |

→ [网络编程时间线](network/timeline.md)

### [序列化](serialization/)

Java 序列化从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 1.0 | Serializable | 基础序列化 |
| JDK 5 | 枚举序列化 | Enum 支持 |
| JDK 7 | Externalizable 增强 | 自定义序列化 |
| JDK 17 | 密封序列化 | 序列化检查 |
| JDK 21 | Record 序列化 | 简化序列化 |

→ [序列化时间线](serialization/timeline.md)

---

## 4. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 并发编程 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Doug Lea | 65 | SUNY Oswego | JSR-166 (并发工具), ConcurrentHashMap |
| 2 | Alan Bateman | 43 | Oracle | NIO、NIO.2 (JSR 51, JSR 203) |
| 3 | Viktor Klang | 29 | Lightbend/Oracle | CompletableFuture |
| 4 | Martin Buchholz | 13 | Google | 并发工具, 算法 |
| 5 | Stuart Marks | 8 | Oracle | 集合, 并发 |
| 6 | David Holmes | 6 | Oracle | JSR-166 规范负责人 |
| 7 | Roger Riggs | 4 | Oracle | 工具类, 集合 |

### HTTP/网络 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Daniel Fuchs | 95 | Oracle | HTTP Client, HTTP/3 |
| 2 | Michael McMahon | 19 | Oracle | HTTP Client (JEP 321) |
| 3 | Jaikiran Pai | 18 | Red Hat/Oracle | HTTP/2, 网络层 |
| 4 | Volkan Yazıcı | 17 | Oracle | HTTP/3, WebSocket |
| 5 | Chris Hegarty | 17 | Oracle | HTTP Client 基础 |
| 6 | Daniel Jeliński | 16 | Oracle | HTTP/2, 连接池 |
| 7 | Conor Cleary | 14 | Oracle | HTTP/3 (QUIC) |

---

## 5. 重要 PR 分析

### 并发集合优化

#### JDK-8348880: ZoneOffset 缓存优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ +15-25% 时区偏移缓存性能

将 `ConcurrentHashMap<Integer, ZoneOffset>` 改为 `AtomicReferenceArray<ZoneOffset>`：

**核心改进**:
- 消除 `int` → `Integer` 自动装箱
- 数组访问比 HashMap 更快
- 内存占用减少 85%

```java
// 优化前
ConcurrentMap<Integer, ZoneOffset> cache = new ConcurrentHashMap<>();
Integer key = quarters;  // 装箱
ZoneOffset result = cache.get(key);

// 优化后
AtomicReferenceArray<ZoneOffset> cache = new AtomicReferenceArray<>(256);
int key = quarters & 0xff;  // 无装箱
ZoneOffset result = cache.getOpaque(key);
```

→ [详细分析](/by-pr/8348/8348880.md)

### 分布式系统优化

#### JDK-8353741: UUID.toString SWAR 优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ +40-60% UUID.toString 性能提升

使用 SWAR (SIMD Within A Register) 技术替代查找表：

**优化点**:
- 消除查找表缓存未命中
- 寄存器内并行计算
- 使用 `Long.expand` intrinsic

→ [详细分析](/by-pr/8353/8353741.md)

### 字节码生成优化

#### JDK-8340587: StackMapGenerator 优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐ +3-7% StackMap 生成性能

优化 `checkAssignableTo` 方法，避免空栈复制：

**优化点**:
- 空栈时跳过复制
- 用 `clone()` 替代 `Array.copyOf`
- 局部变量缓存

→ [详细分析](/by-pr/8340/8340587.md)

---

## 6. 内部开发者资源

### 源码结构

```
src/java.base/share/classes/java/util/concurrent/
├── atomic/                       # 原子类
│   ├── AtomicBoolean.java
│   ├── AtomicInteger.java
│   └── AtomicReference.java
├── locks/                        # 锁实现
│   ├── Lock.java
│   ├── ReentrantLock.java
│   ├── StampedLock.java
│   └── AbstractQueuedSynchronizer.java
├── ExecutorService.java          # 执行器接口
├── ForkJoinPool.java             # Fork/Join 池
├── CompletableFuture.java        # 异步编程
└── Flow.java                     # Reactive Streams

src/java.base/share/classes/java/lang/
├── Thread.java                   # 线程核心类
├── VirtualThread.java            # 虚拟线程 (JDK 21+)
└── ScopedValue.java              # 作用域值 (JDK 21+)

src/java.net.http/
├── HttpClient.java               # HTTP 客户端
├── HttpRequest.java
├── HttpResponse.java
└── WebSocket.java                # WebSocket 支持

src/java.base/share/classes/nio/
├── channels/                     # NIO 通道
│   ├── AsynchronousSocketChannel
│   ├── AsynchronousServerSocketChannel
│   └── SocketChannel
├── buffer/                       # NIO 缓冲区
└── file/                         # NIO.2 文件 API
```

### 关键内部类

| 类 | 作用 | 访问级别 |
|---|------|----------|
| `jdk.internal.vm.ScopedValueContainer` | Scoped Value 存储 | 内部 |
| `jdk.internal.misc.Blocker` | 虚拟线程 Pin 检测 | `@Restricted` |
| `jdk.internal.net.http.HttpClientImpl` | HTTP Client 实现 | 内部 |
| `java.util.concurrent.locks.AbstractQueuedSynchronizer` | AQS 同步器 | public |

### VM 参数速查

```bash
# 虚拟线程 (JDK 21+)
-Djdk.virtualThreadScheduler.parallelism=8  # 并发度
-Djdk.virtualThreadScheduler.maxPoolSize=256 # 最大载体线程

# Fork/Join Pool
-Djava.util.concurrent.ForkJoinPool.common.parallelism=8

# HTTP/2
-XX:MaxDirectMemorySize=512m     # 直接内存 (用于 NIO)
-Djdk.httpclient.connectionPoolSize=20

# 网络调试
-Djdk.httpclient.enableAllMethodRetry=true
-Djdk.httpclient.websocket.debug=true
-Djavax.net.debug=ssl             # SSL 调试
```

### 诊断工具

```bash
# 线程转储 (包含虚拟线程)
jcmd <pid> Thread.dump_to_file -format=json threads.json

# 虚拟线程统计
jcmd <pid> VM.native_memory summary

# HTTP Client 调试
-Djdk.httpclient.HttpClient.log=errors,requests,headers
```

---

## 7. 统计数据

| 指标 | 数值 |
|------|------|
| 并发 JEP (JDK 5-26) | 20+ |
| Loom 预览轮次 | Structured Concurrency 7 次 (JDK 19-25), Scoped Values 5 次 (JDK 20-24) |
| 并发工具类 | 50+ |
| HTTP 协议支持 | HTTP/1.1, HTTP/2, HTTP/3 (预览) |
| 虚拟线程 Pin 限制 | JDK 24 起仅类初始化期间会 Pin |

---

## 8. 学习路径

1. **入门**: [并发编程](concurrency/) → Executor 框架
2. **进阶**: [HTTP 客户端](http/) → [网络编程](network/) → 网络编程
3. **深入**: [并发编程](concurrency/) → Virtual Threads → 高并发
4. **实践**: [序列化](serialization/) → 数据交换
