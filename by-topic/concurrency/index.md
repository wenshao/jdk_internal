# 并发网络

多线程、网络通信、异步编程。

---

## 主题列表

### [并发编程](concurrency/)

从 Thread 到 Virtual Thread 的演进。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 5 | Executor 框架 | JSR-166 |
| JDK 7 | Fork/Join 框架 | JSR-166y |
| JDK 8 | Lambda、Parallel Stream | JEP 126 |
| JDK 8 | CompletableFuture | JEP 107 |
| JDK 9 | CompletableFuture 改进、Reactive Streams | JEP 266 |
| JDK 19 | **Virtual Threads** (预览) | JEP 425 |
| JDK 20 | Virtual Threads (第二次预览) | JEP 436 |
| JDK 21 | **Virtual Threads** (正式)、**Structured Concurrency** (预览)、**Scoped Values** (预览) | JEP 444, JEP 453, JEP 446 |
| JDK 22-26 | Structured Concurrency (持续预览) | JEP 462, 477, 483, 491, 493 |

→ [并发时间线](concurrency/timeline.md)

### [HTTP 客户端](http/)

从 HttpURLConnection 到 HTTP/3。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 1.0 | HttpURLConnection | - |
| JDK 9 | HTTP Client (孵化器) | JEP 110 |
| JDK 10 | HTTP Client (孵化器) | - |
| JDK 11 | **HTTP Client** (标准) | JEP 321 |
| JDK 16 | HTTP/2 支持 | - |
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
| JDK 18 | Unix Domain Socket | 本地 IPC |

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

## 学习路径

1. **入门**: [并发编程](concurrency/) → Executor 框架
2. **进阶**: [HTTP 客户端](http/) → [网络编程](network/) → 网络编程
3. **深入**: [并发编程](concurrency/) → Virtual Threads → 高并发
4. **实践**: [序列化](serialization/) → 数据交换
