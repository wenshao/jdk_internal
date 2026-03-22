# 网络编程

> Socket、NIO、HTTP Client、Unix Domain Socket 演进历程

[← 返回并发网络](../)

---
## 目录

1. [快速概览](#1-快速概览)
2. [核心贡献者](#2-核心贡献者)
3. [Socket API 演进](#3-socket-api-演进)
4. [NIO (JDK 1.4+)](#4-nio-jdk-14)
5. [NIO.2 与 AsynchronousSocketChannel (JDK 7+)](#5-nio2-与-asynchronoussocketchannel-jdk-7)
6. [Socket/DatagramSocket 重实现 (JEP 353/373)](#6-socketdatagramsocket-重实现-jep-353373)
7. [Unix Domain Sockets (JEP 380, JDK 16+)](#7-unix-domain-sockets-jep-380-jdk-16)
8. [HTTP Client (JEP 321, JDK 11+)](#8-http-client-jep-321-jdk-11)
9. [HTTP/3 (JEP 517, JDK 26)](#9-http3-jep-517-jdk-26)
10. [Virtual Threads 与网络 I/O (JDK 21+)](#10-virtual-threads-与网络-io-jdk-21)
11. [DNS 解析与 InetAddress](#11-dns-解析与-inetaddress)
12. [性能优化](#12-性能优化)
13. [重要 PR 分析](#13-重要-pr-分析)
14. [网络编程最佳实践](#14-网络编程最佳实践)
15. [相关链接](#15-相关链接)

---


## 1. 快速概览

```
JDK 1.0 ── JDK 1.4 ── JDK 7 ── JDK 11 ── JDK 13/15 ── JDK 16 ── JDK 21 ── JDK 26
   │         │         │        │          │            │        │        │
Socket/   NIO      NIO.2   HTTP      Socket/       Unix     Virtual  HTTP/3
ServerSocket Channel  Async  Client   Datagram      Domain   Threads  (预览)
           Selector  Group  (JEP 321) Reimpl       Sockets           JEP 517
           (JSR 51) (AIO)            (JEP 353/373) (JEP 380)  Loom
```

### 核心演进

| 版本 | 特性 | 说明 | JEP |
|------|------|------|-----|
| **JDK 1.0** | Socket/ServerSocket | TCP/UDP 基础, 阻塞 I/O (BIO) | - |
| **JDK 1.4** | NIO | Buffer, Channel, Selector 非阻塞 I/O | JSR 51 |
| **JDK 7** | NIO.2 | AsynchronousChannel, Path, Files | JSR 203 |
| **JDK 11** | HTTP Client | 新 HTTP API 标准化, 支持 HTTP/2 | JEP 321 |
| **JDK 13** | Socket 重实现 | NioSocketImpl 替换 PlainSocketImpl | JEP 353 |
| **JDK 15** | DatagramSocket 重实现 | NIO 后端替换旧的 DatagramSocket | JEP 373 |
| **JDK 16** | Unix Domain Socket | 本地 IPC, AF_UNIX 支持 | JEP 380 |
| **JDK 21** | Virtual Threads | 轻量级线程, 阻塞 I/O 不阻塞平台线程 | JEP 444 |
| **JDK 25** | HTTP/3 | 基于 QUIC 协议 (预览) | JEP 517 |

---

## 2. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 网络/并发团队 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Alan Bateman | 43 | Oracle | NIO, NIO.2 (JSR 51, JSR 203), JEP 380 |
| 2 | Viktor Klang | 44 | Lightbend/Oracle | CompletableFuture |
| 3 | Jaikiran Pai | 34 | Red Hat/Oracle | HTTP/2, 网络层 |
| 4 | Chris Hegarty | 17 | Oracle | HTTP Client 基础 |
| 5 | Daniel Jeliński | 16 | Oracle | HTTP/2, 连接池 |
| 6 | Michael McMahon | 19 | Oracle | HTTP Client, Socket 重实现 |
| 7 | [Brian Goetz](/by-contributor/profiles/brian-goetz.md) | 12 | Oracle | 并发架构 |

---

## 3. Socket API 演进

### 三代 Socket API 对比

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Socket API 演进 (Evolution)                          │
├──────────────────┬──────────────────┬───────────────────────────────────┤
│  第一代: BIO      │  第二代: NIO      │  第三代: Virtual Threads          │
│  JDK 1.0 (1996)  │  JDK 1.4 (2002)  │  JDK 21 (2023)                  │
├──────────────────┼──────────────────┼───────────────────────────────────┤
│  Socket          │  SocketChannel   │  Socket + Virtual Thread          │
│  ServerSocket    │  ServerSocket-   │  (阻塞式代码,                     │
│  每连接一线程     │   Channel        │   非阻塞执行)                     │
│  (thread-per-    │  Selector        │                                   │
│   connection)    │  (event-driven)  │  "回到简单"                       │
└──────────────────┴──────────────────┴───────────────────────────────────┘
```

### 第一代: 传统 Socket (BIO, Blocking I/O)

```java
import java.net.*;
import java.io.*;

// TCP 客户端 — 最基础的阻塞式网络编程
try (Socket socket = new Socket("example.com", 80)) {
    OutputStream out = socket.getOutputStream();
    out.write("GET / HTTP/1.1\r\nHost: example.com\r\n\r\n".getBytes());

    InputStream in = socket.getInputStream();
    byte[] buffer = new byte[1024];
    int len;
    while ((len = in.read(buffer)) != -1) {  // 阻塞在此
        System.out.write(buffer, 0, len);
    }
}
```

```java
// TCP 服务器 — thread-per-connection 模型
try (ServerSocket server = new ServerSocket(8080)) {
    while (true) {
        Socket client = server.accept();  // 阻塞等待连接
        new Thread(() -> handle(client)).start();  // 每连接一线程
    }
}
```

### UDP Socket

```java
// UDP 发送 — 无连接, 不可靠传输
try (DatagramSocket socket = new DatagramSocket()) {
    byte[] data = "Hello UDP".getBytes();
    InetAddress address = InetAddress.getByName("example.com");
    DatagramPacket packet = new DatagramPacket(
        data, data.length, address, 8080);
    socket.send(packet);
}
```

### BIO 的问题

| 问题 | 说明 |
|------|------|
| **阻塞 I/O** | `read()` / `accept()` 阻塞调用线程 |
| **线程开销** | 每个连接需要独立线程, 1 万连接 = 1 万线程 |
| **C10K 问题** | 上下文切换 (context switch) 成本过高 |
| **资源浪费** | 多数线程在等待 I/O, 占用内存但不做有用工作 |

### 第二代: NIO SocketChannel (非阻塞)

```java
// NIO 客户端 — 非阻塞模式
SocketChannel channel = SocketChannel.open();
channel.configureBlocking(false);  // 关键: 非阻塞
channel.connect(new InetSocketAddress("example.com", 80));

while (!channel.finishConnect()) {
    // 连接尚未完成, 可以做其他事
}

ByteBuffer buffer = ByteBuffer.wrap("GET / HTTP/1.1\r\n\r\n".getBytes());
channel.write(buffer);
```

### 第三代: Virtual Thread + 传统 Socket

```java
// JDK 21+: 写阻塞代码, 享受非阻塞性能
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 100_000; i++) {
        executor.submit(() -> {
            // 阻塞代码 — 但虚拟线程在 I/O 阻塞时自动 unmount
            try (Socket socket = new Socket("example.com", 80)) {
                InputStream in = socket.getInputStream();
                in.read(new byte[1024]);  // 不阻塞平台线程!
            }
            return null;
        });
    }
}
// 10 万并发连接, 仅需少量平台线程
```

**核心思想**: 虚拟线程让开发者回到 "每连接一线程" 的简单模型, 但底层使用 NIO 机制, 不再有 C10K 问题。

---

## 4. NIO (JDK 1.4+)

### 核心组件

```
┌─────────────────────────────────────────────────────────┐
│                      NIO 架构                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Buffer (缓冲区)                                         │
│  ├── ByteBuffer (最常用)                                 │
│  ├── CharBuffer                                         │
│  └── DirectByteBuffer (堆外内存, off-heap)              │
│                                                         │
│  Channel (通道)                                          │
│  ├── SocketChannel         ← TCP 客户端                  │
│  ├── ServerSocketChannel   ← TCP 服务器                  │
│  ├── DatagramChannel       ← UDP                        │
│  └── FileChannel           ← 文件 I/O                   │
│                                                         │
│  Selector (选择器, 多路复用器)                             │
│  └── 单线程监控多个 Channel 的 I/O 事件                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### ByteBuffer 核心操作

```java
ByteBuffer buffer = ByteBuffer.allocate(1024);       // 堆内 (heap)
ByteBuffer direct = ByteBuffer.allocateDirect(1024); // 堆外 (direct, off-heap)

buffer.put("Hello NIO".getBytes(StandardCharsets.UTF_8));
buffer.flip();    // 切换读模式 (position → 0, limit → 之前 position)
while (buffer.hasRemaining()) { byte b = buffer.get(); }
buffer.clear();   // 重置为写模式
```

### Selector 多路复用 (I/O Multiplexing)

```java
// NIO Server — 单线程处理多个连接
ServerSocketChannel server = ServerSocketChannel.open();
server.configureBlocking(false);
server.bind(new InetSocketAddress(8080));

Selector selector = Selector.open();
server.register(selector, SelectionKey.OP_ACCEPT);

while (true) {
    selector.select();  // 阻塞, 直到有事件就绪

    for (SelectionKey key : selector.selectedKeys()) {
        if (key.isAcceptable()) {
            SocketChannel client = server.accept();
            client.configureBlocking(false);
            client.register(selector, SelectionKey.OP_READ);
        }
        if (key.isReadable()) {
            SocketChannel client = (SocketChannel) key.channel();
            ByteBuffer buffer = ByteBuffer.allocate(1024);
            int bytesRead = client.read(buffer);
            if (bytesRead == -1) {
                key.cancel();
                client.close();
            }
        }
    }
    selector.selectedKeys().clear();
}
```

**底层机制**: Linux 使用 `epoll`, macOS 使用 `kqueue`, Windows 使用 `IOCP`。

---

## 5. NIO.2 与 AsynchronousSocketChannel (JDK 7+)

### AsynchronousSocketChannel (异步 Socket)

NIO.2 引入了真正的异步 I/O (AIO), 基于操作系统级别的异步机制:

```java
import java.nio.channels.*;
import java.util.concurrent.*;

// 异步 Socket 连接 — 使用 Future
AsynchronousSocketChannel client = AsynchronousSocketChannel.open();
Future<Void> connect = client.connect(
    new InetSocketAddress("example.com", 80));
connect.get();  // 等待连接完成

// 异步读取 — 使用 CompletionHandler (回调模式)
ByteBuffer buffer = ByteBuffer.allocate(1024);
client.read(buffer, null, new CompletionHandler<Integer, Void>() {
    @Override
    public void completed(Integer bytesRead, Void attachment) {
        buffer.flip();
        System.out.println("Read " + bytesRead + " bytes");
    }

    @Override
    public void failed(Throwable exc, Void attachment) {
        exc.printStackTrace();
    }
});
```

### 虚拟线程使 AIO 过时 (Virtual Threads Obsolete AIO)

AIO 的回调模式复杂且难以调试。JDK 21 虚拟线程的出现改变了这一格局:

```
┌──────────────────────────────────────────────────────────────────┐
│            为什么虚拟线程取代 AIO?                                │
├──────────────────────────────┬───────────────────────────────────┤
│  NIO.2 AIO (回调模式)         │  Virtual Thread + 同步 I/O        │
├──────────────────────────────┼───────────────────────────────────┤
│  client.read(buf, handler)   │  int n = channel.read(buf);      │
│  → 回调地狱 (callback hell)   │  → 线性代码, 易读易调试            │
│  → 异常处理分散               │  → try-catch 正常工作              │
│  → 调试困难 (栈帧丢失)        │  → 完整调用栈                     │
│  → AsynchronousChannelGroup  │  → 无需管理线程组                  │
│    线程池管理                 │                                   │
└──────────────────────────────┴───────────────────────────────────┘
```

```java
// ❌ AIO 风格 — 嵌套回调, 难以维护
client.read(buf1, null, new CompletionHandler<>() {
    public void completed(Integer r, Void a) {
        client.read(buf2, null, new CompletionHandler<>() {
            public void completed(Integer r2, Void a2) {
                // callback hell...
            }
            public void failed(Throwable e, Void a2) { }
        });
    }
    public void failed(Throwable e, Void a) { }
});

// ✅ 虚拟线程风格 — 同步代码, 同样高效
Thread.ofVirtual().start(() -> {
    int n1 = channel.read(buf1);   // 虚拟线程 unmount, 不阻塞平台线程
    int n2 = channel.read(buf2);   // 线性执行, 易于理解
    process(buf1, buf2);
});
```

**结论**: JDK 21+ 推荐使用 **同步 I/O + 虚拟线程**, 而非 NIO.2 的 AsynchronousChannel。AIO 仍然可用, 但不再是高并发场景的首选方案。

---

## 6. Socket/DatagramSocket 重实现 (JEP 353/373)

### JEP 353: 重新实现旧版 Socket API (JDK 13)

JDK 13 将 `Socket` / `ServerSocket` 的底层实现从 `PlainSocketImpl` 替换为 `NioSocketImpl`:

| 方面 | 旧实现 PlainSocketImpl | 新实现 NioSocketImpl |
|------|------------------------|----------------------|
| **代码来源** | JDK 1.0, Java + C 混合 | 纯 Java, 基于 NIO 内部机制 |
| **线程安全** | 依赖平台原生锁 (native lock) | Java ReentrantLock |
| **可维护性** | 脆弱, 边界条件多 | 清晰, 测试充分 |
| **虚拟线程** | 不兼容 (阻塞平台线程) | **天然兼容** (可 unmount) |
| **缓冲区** | 内部使用 `SocketInputStream` | 使用 NIO `ByteBuffer` |

```java
// 对应用代码完全透明 — 无需任何修改
// JDK 13 之前: PlainSocketImpl (C 代码)
// JDK 13+: NioSocketImpl (Java 代码)
Socket socket = new Socket("example.com", 80);  // 底层自动使用新实现

// JDK 13-17 可回退到旧实现 (后已移除):
// java -Djdk.net.usePlainSocketImpl=true MyApp
```

### JEP 373: 重新实现 DatagramSocket API (JDK 15)

同样, `DatagramSocket` 和 `MulticastSocket` 也被替换为 NIO 后端:

```java
// DatagramSocket 重实现 — 同样对应用透明
DatagramSocket socket = new DatagramSocket(9999);

// 新实现特性:
// 1. 内部使用 DatagramChannel
// 2. 支持虚拟线程 (Virtual Thread compatible)
// 3. 移除了过时的 peek/peekData 原生方法
// 4. MulticastSocket 行为更一致
```

**连锁效应**: JEP 353/373 的重实现是 Virtual Threads (JEP 444) 的前置条件 -- 只有基于 NIO 的实现才能在 I/O 阻塞时让虚拟线程 unmount, 使 BIO 代码无缝运行在虚拟线程上。

---

## 7. Unix Domain Sockets (JEP 380, JDK 16+)

### UnixDomainSocketAddress

JDK 16 为 `SocketChannel` 和 `ServerSocketChannel` 添加 AF_UNIX 支持, 使用文件系统路径而非 IP + 端口:

```java
import java.net.UnixDomainSocketAddress;
import java.nio.channels.*;
import java.nio.ByteBuffer;
import java.nio.file.*;

// 创建地址 — 使用文件路径而非 host:port
UnixDomainSocketAddress address =
    UnixDomainSocketAddress.of("/tmp/my-server.sock");
```

### 服务端

```java
// Unix Domain Socket 服务器
Path socketPath = Path.of("/tmp/my-server.sock");
Files.deleteIfExists(socketPath);  // 清理旧的 socket 文件

try (ServerSocketChannel server =
         ServerSocketChannel.open(StandardProtocolFamily.UNIX)) {
    server.bind(UnixDomainSocketAddress.of(socketPath));

    while (true) {
        try (SocketChannel client = server.accept()) {
            ByteBuffer buffer = ByteBuffer.allocate(1024);
            client.read(buffer);
            buffer.flip();
            // 处理数据, 发送响应
            client.write(ByteBuffer.wrap("OK".getBytes()));
        }
    }
} finally {
    Files.deleteIfExists(socketPath);
}
```

### 客户端

```java
// Unix Domain Socket 客户端
try (SocketChannel channel =
         SocketChannel.open(StandardProtocolFamily.UNIX)) {
    channel.connect(UnixDomainSocketAddress.of("/tmp/my-server.sock"));

    channel.write(ByteBuffer.wrap("Hello UDS".getBytes()));

    ByteBuffer response = ByteBuffer.allocate(256);
    channel.read(response);
    response.flip();
}
```

### 容器间通信 (Container IPC)

Unix Domain Socket 在容器化环境中特别有用 -- 通过共享卷 (volume mount) 挂载 socket 文件, 容器间无需暴露端口即可通信, 且受文件系统权限保护。

### TCP Loopback vs Unix Domain Socket

| 方面 | TCP Loopback (127.0.0.1) | Unix Domain Socket |
|------|--------------------------|-------------------|
| **性能** | 经过完整 TCP/IP 栈 | 绕过网络栈, 快 30-50% |
| **安全** | 需要防火墙规则, 端口暴露 | 文件系统权限 (chmod) |
| **寻址** | IP + Port | 文件路径 |
| **跨平台** | 所有平台 | Linux, macOS, Windows 10+ |
| **容器** | 需要端口映射 | 卷挂载即可 |

---

## 8. HTTP Client (JEP 321, JDK 11+)

### HttpClient 创建

```java
import java.net.URI;
import java.net.http.*;
import java.time.Duration;

// 方式 1: 默认配置
HttpClient client = HttpClient.newHttpClient();

// 方式 2: 自定义配置
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)       // 协议版本
    .connectTimeout(Duration.ofSeconds(10))    // 连接超时
    .followRedirects(HttpClient.Redirect.NORMAL) // 重定向策略
    .proxy(ProxySelector.getDefault())         // 代理
    .executor(Executors.newFixedThreadPool(4)) // 自定义线程池
    .build();
```

### 同步请求 (Synchronous)

```java
// 同步 GET — 阻塞当前线程直到响应返回
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/users"))
    .header("Accept", "application/json")
    .timeout(Duration.ofSeconds(5))
    .GET()
    .build();

HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());

System.out.println("Status: " + response.statusCode());
System.out.println("Body: " + response.body());
System.out.println("Headers: " + response.headers().map());
```

### 异步请求 (Asynchronous)

```java
// 异步 GET — 返回 CompletableFuture, 不阻塞
CompletableFuture<HttpResponse<String>> future =
    client.sendAsync(request, HttpResponse.BodyHandlers.ofString());

future
    .thenApply(HttpResponse::body)
    .thenAccept(body -> System.out.println("Got: " + body))
    .exceptionally(e -> {
        System.err.println("Error: " + e.getMessage());
        return null;
    });
```

### POST 请求

```java
// JSON POST
String json = """
    {"name": "Alice", "email": "alice@example.com"}
    """;

HttpRequest postRequest = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/users"))
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString(json))
    .build();

HttpResponse<String> response = client.send(postRequest,
    HttpResponse.BodyHandlers.ofString());
```

### HTTP/2 多路复用 (Multiplexing)

HttpClient 默认优先使用 HTTP/2, 支持单连接上的多路复用:

```
┌──────────────────────────────────────────────────────────────┐
│                   HTTP/2 多路复用                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  单个 TCP 连接:                                              │
│  ┌──────┐  ┌──────┐  ┌──────┐                               │
│  │Stream│  │Stream│  │Stream│   ← 多个请求并行传输            │
│  │  1   │  │  2   │  │  3   │     (无需多个 TCP 连接)         │
│  └──┬───┘  └──┬───┘  └──┬───┘                               │
│     └─────────┼─────────┘                                    │
│               ▼                                              │
│      ┌──────────────┐                                        │
│      │ TCP Connection│   ← 所有 Stream 共享一个 TCP 连接      │
│      └──────────────┘                                        │
│                                                              │
│  问题: TCP 层丢包 → 所有 Stream 阻塞 (队头阻塞)              │
│  (Head-of-Line Blocking at TCP layer)                        │
└──────────────────────────────────────────────────────────────┘
```

```java
// HTTP/2 多路复用 — 并发发送多个请求, 共享连接
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .build();

// 多个异步请求 — 自动复用同一个 TCP 连接
List<CompletableFuture<HttpResponse<String>>> futures =
    IntStream.range(0, 10)
        .mapToObj(i -> HttpRequest.newBuilder()
            .uri(URI.create("https://api.example.com/item/" + i))
            .build())
        .map(req -> client.sendAsync(req, HttpResponse.BodyHandlers.ofString()))
        .toList();

CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();
```

### 连接池 (Connection Pool)

HttpClient 内部自动管理连接池:

```java
// HttpClient 的连接池行为:
// 1. 自动保持连接 (keep-alive)
// 2. 相同 host:port 复用连接
// 3. HTTP/2 下单连接多路复用
// 4. 空闲连接超时后自动关闭

HttpClient client = HttpClient.newBuilder()
    .connectTimeout(Duration.ofSeconds(10))
    .build();

// 重复使用同一个 client 实例 — 连接自动复用
for (int i = 0; i < 100; i++) {
    HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create("https://api.example.com/data"))
        .build();
    client.send(request, HttpResponse.BodyHandlers.ofString());
    // 底层复用连接, 不会创建 100 个 TCP 连接
}

// ⚠️ 反模式: 每次请求创建新 client
// for (...) {
//     HttpClient c = HttpClient.newHttpClient();  // ❌ 浪费资源
//     c.send(request, ...);
// }
```

---

## 9. HTTP/3 (JEP 517, JDK 26)

### QUIC 协议基础

HTTP/3 基于 QUIC (Quick UDP Internet Connections), 使用 UDP 而非 TCP:

```
┌────────────────────────────────────────────────────────────────────┐
│                  HTTP 协议栈对比                                    │
├────────────────────┬───────────────────┬───────────────────────────┤
│   HTTP/1.1         │   HTTP/2          │   HTTP/3                  │
├────────────────────┼───────────────────┼───────────────────────────┤
│   HTTP/1.1         │   HTTP/2          │   HTTP/3                  │
│   ─────────        │   ─────────       │   ─────────              │
│   TLS 1.2+         │   TLS 1.2+       │   QUIC (内置 TLS 1.3)     │
│   ─────────        │   ─────────       │   ─────────              │
│   TCP              │   TCP             │   UDP                     │
├────────────────────┼───────────────────┼───────────────────────────┤
│  连接建立:          │  连接建立:         │  连接建立:                 │
│  TCP 3-way + TLS   │  TCP 3-way + TLS  │  0-RTT 或 1-RTT          │
│  = 2-3 RTT         │  = 2-3 RTT        │  (首次 1-RTT, 恢复 0-RTT) │
└────────────────────┴───────────────────┴───────────────────────────┘
```

### HTTP/3 vs HTTP/2 核心差异

| 特性 | HTTP/2 | HTTP/3 |
|------|--------|--------|
| **传输层** | TCP | QUIC (UDP) |
| **加密** | TLS 1.2+ (可选) | TLS 1.3 (内置, 强制) |
| **多路复用** | 有, 但 TCP 队头阻塞 | 有, **无队头阻塞** |
| **连接建立** | 2-3 RTT | 1 RTT (首次), **0-RTT** (恢复) |
| **连接迁移** | 不支持 (IP 变 = 断连) | 支持 (Connection ID) |
| **头部压缩** | HPACK | QPACK |
| **丢包影响** | 所有 Stream 阻塞 | 仅影响丢包的 Stream |
| **JDK 支持** | JDK 11+ | JDK 25+ (预览) |

### 0-RTT 连接恢复

```
首次连接 (1-RTT):
  Client ──── ClientHello + QUIC params ────→ Server
  Client ←─── ServerHello + TLS data    ←──── Server
  Client ──── 应用数据 ──────────────────────→ Server

恢复连接 (0-RTT):
  Client ──── ClientHello + 应用数据 ────────→ Server  ← 首包即携带数据!
  (使用之前保存的 session ticket)
```

### 使用方式

```java
// JDK 26 HTTP/3 — API 完全透明, 与 HTTP/2 相同
// 需要: --enable-preview
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)  // 会自动协商升级到 HTTP/3
    .connectTimeout(Duration.ofSeconds(10))
    .build();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .GET()
    .build();

HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());

// 检查实际使用的协议版本
System.out.println("Protocol: " + response.version());
// 可能输出: HTTP_2 或 HTTP_3 (取决于服务器支持)
```

### 协议升级流程 (Alt-Svc Discovery)

客户端先用 HTTP/2 (TCP) 连接服务器。服务器通过 `Alt-Svc: h3=":443"` 响应头声明 HTTP/3 支持。客户端记录此信息, 下次请求尝试 QUIC。若 QUIC 成功则使用 HTTP/3, 若失败 (如防火墙阻止 UDP) 则回退到 HTTP/2。

---

## 10. Virtual Threads 与网络 I/O (JDK 21+)

### 虚拟线程如何改变网络编程

```
┌─────────────────────────────────────────────────────────────────┐
│             传统线程 vs 虚拟线程 网络 I/O                         │
├───────────────────────────┬─────────────────────────────────────┤
│  Platform Thread          │  Virtual Thread                     │
│                           │                                     │
│  socket.read()            │  socket.read()                      │
│    ↓ 阻塞平台线程          │    ↓ 虚拟线程 unmount                │
│    OS 线程被占用            │    ↓ 平台线程被释放                  │
│    等待数据到达             │    ↓ 平台线程去执行其他虚拟线程       │
│    ↓ 数据到达              │    ↓ 数据到达                       │
│    ↓ 继续执行              │    ↓ 虚拟线程 re-mount              │
│                           │    ↓ 继续执行                       │
├───────────────────────────┼─────────────────────────────────────┤
│  1 万连接 = 1 万线程       │  1 万连接 = 1 万虚拟线程             │
│  = ~10GB 内存              │  = ~几十 MB 内存                    │
│  = 大量上下文切换           │  = 少量平台线程切换                  │
└───────────────────────────┴─────────────────────────────────────┘
```

### 虚拟线程 + Socket 实战

```java
// 高并发 TCP 服务器 — 虚拟线程版本
try (ServerSocket server = new ServerSocket(8080);
     var executor = Executors.newVirtualThreadPerTaskExecutor()) {

    while (true) {
        Socket client = server.accept();
        executor.submit(() -> {
            try (client;
                 var in = new BufferedReader(
                     new InputStreamReader(client.getInputStream()));
                 var out = new PrintWriter(
                     client.getOutputStream(), true)) {

                String line;
                while ((line = in.readLine()) != null) {
                    out.println("Echo: " + line);
                    // readLine() 阻塞时, 虚拟线程 unmount
                    // 平台线程可以服务其他虚拟线程
                }
            }
            return null;
        });
    }
}
```

### Pinning 问题 (虚拟线程的陷阱)

```java
// ⚠️ synchronized 块中的 I/O 会导致虚拟线程 pinning
// pinning = 虚拟线程无法 unmount, 占用平台线程
synchronized (lock) {
    socket.read(buffer);  // ❌ pinning! 平台线程被阻塞
}

// ✅ 解决方案: 使用 ReentrantLock
ReentrantLock lock = new ReentrantLock();
lock.lock();
try {
    socket.read(buffer);  // ✅ 虚拟线程正常 unmount
} finally {
    lock.unlock();
}
```

---

## 11. DNS 解析与 InetAddress

### InetAddress 基础

```java
import java.net.InetAddress;

// DNS 解析 (域名 → IP)
InetAddress addr = InetAddress.getByName("example.com");
System.out.println(addr.getHostAddress());  // 93.184.216.34

// 获取所有 IP (多 A 记录)
InetAddress[] addrs = InetAddress.getAllByName("google.com");
for (InetAddress a : addrs) {
    System.out.println(a.getHostAddress());
}

// 反向 DNS (IP → 域名)
InetAddress addr = InetAddress.getByName("8.8.8.8");
System.out.println(addr.getHostName());  // dns.google
```

### InetAddress 缓存 (DNS Caching)

JVM 内部维护 DNS 缓存, 由安全管理器策略控制:

```java
// DNS 缓存配置 — 通过安全属性
// java.security 文件或 Security.setProperty()

// 成功解析的缓存时间 (秒), -1 = 永不过期, 0 = 不缓存
// 默认: 安装 SecurityManager 时为 -1, 否则为 30
Security.setProperty("networkaddress.cache.ttl", "60");

// 失败解析的缓存时间 (秒), 0 = 不缓存
// 默认: 10
Security.setProperty("networkaddress.cache.negative.ttl", "5");
```

```
┌─────────────────────────────────────────────────────────┐
│              InetAddress DNS 缓存流程                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  InetAddress.getByName("example.com")                   │
│       │                                                 │
│       ▼                                                 │
│  ┌─────────────┐    命中                                │
│  │  JVM 缓存    │──────────→ 返回缓存的 IP               │
│  └─────┬───────┘                                        │
│        │ 未命中                                          │
│        ▼                                                │
│  ┌─────────────┐                                        │
│  │  系统 DNS    │──→ /etc/resolv.conf (Linux)            │
│  │  解析器      │──→ 系统 DNS 缓存                       │
│  └─────┬───────┘                                        │
│        │                                                │
│        ▼                                                │
│  ┌─────────────┐                                        │
│  │  DNS 服务器  │   递归查询                              │
│  └─────────────┘                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 虚拟线程下的 DNS 行为

DNS 解析涉及网络 I/O, 在虚拟线程中有特殊考虑:

```java
// DNS 解析在虚拟线程中的行为:
//
// 1. InetAddress.getByName() 底层调用系统 getaddrinfo()
// 2. getaddrinfo() 是阻塞的系统调用 (native call)
// 3. JDK 21+ 中, 虚拟线程执行 DNS 解析时:
//    - 不会 unmount (因为是 native 阻塞, 非 Java I/O 阻塞)
//    - 会临时 pin 到平台线程
// 4. 大量并发 DNS 解析可能耗尽平台线程池

// ⚠️ 高并发 DNS 解析的注意事项
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 10_000; i++) {
        executor.submit(() -> {
            // DNS 解析会暂时 pin 虚拟线程
            InetAddress addr = InetAddress.getByName("example.com");
            // 后续 Socket I/O 可以正常 unmount
            try (Socket s = new Socket(addr, 80)) {
                s.getInputStream().read(new byte[1024]);
            }
            return null;
        });
    }
}

// ✅ 缓解策略:
// 1. 提前解析并缓存 IP (warm up DNS cache)
// 2. 增大 networkaddress.cache.ttl
// 3. 使用应用层 DNS 缓存 (如 Caffeine + DNS)
// 4. JDK 未来版本可能引入异步 DNS 解析
```

---

## 12. 性能优化

### I/O 模型对比

| 模型 | 线程数 | 内存 | 代码复杂度 | 适用场景 |
|------|--------|------|-----------|---------|
| **BIO** | 每连接一线程 | 高 | 低 | 简单应用, 少量连接 |
| **NIO Selector** | 固定少量 | 低 | 高 | 高并发, 框架内部 |
| **NIO.2 AIO** | 线程组 | 中 | 高 | 已被虚拟线程取代 |
| **Virtual Thread + BIO** | 每连接一虚拟线程 | 低 | **低** | **JDK 21+ 推荐** |

### Buffer 优化

```java
// 使用直接 Buffer (堆外内存, off-heap)
ByteBuffer direct = ByteBuffer.allocateDirect(8192);
// 优点: 避免堆内→堆外复制, I/O 性能更好
// 缺点: 分配/回收成本高, 适合长期复用

// ✅ Buffer 池化复用
private static final ThreadLocal<ByteBuffer> BUFFER_POOL =
    ThreadLocal.withInitial(() -> ByteBuffer.allocateDirect(8192));

ByteBuffer buf = BUFFER_POOL.get();
buf.clear();
channel.read(buf);
```

---

## 13. 重要 PR 分析

### NIO 性能优化

#### JDK-8348880: AtomicReferenceArray 优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: +15-25% 缓存访问性能

将 `ConcurrentHashMap` 替换为 `AtomicReferenceArray`:

**优化点**:
- 消除 `int` → `Integer` 装箱 (autoboxing)
- 数组访问比 HashMap 快
- 内存占用减少 85%

```java
// 优化前：需要装箱
ConcurrentMap<Integer, ZoneOffset> cache = new ConcurrentHashMap<>();
Integer key = index;  // 装箱
ZoneOffset value = cache.get(key);

// 优化后：无装箱
AtomicReferenceArray<ZoneOffset> cache = new AtomicReferenceArray<>(256);
int key = index & 0xff;
ZoneOffset value = cache.getOpaque(key);
```

→ [详细分析](/by-pr/8348/8348880.md)

### UUID 性能优化

#### JDK-8353741: UUID.toString SWAR 优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: +40-60% 性能提升

使用 SWAR (SIMD Within A Register) 技术:

**优化点**:
- 消除查找表
- 寄存器内并行计算
- 使用 `Long.expand` intrinsic

→ [详细分析](/by-pr/8353/8353741.md)

---

## 14. 网络编程最佳实践

### I/O 模型选择

| 场景 | 推荐方案 | 说明 |
|------|----------|------|
| **简单应用** | BIO (Socket) | 代码简单, 易于理解 |
| **高并发服务器** | Virtual Thread + BIO | JDK 21+, 最佳选择 |
| **框架内部** | NIO + Selector | Netty, Undertow 等 |
| **本地 IPC** | Unix Domain Socket | 比 TCP loopback 快 30-50% |
| **HTTP 通信** | HttpClient | 内置连接池, HTTP/2 支持 |

### 虚拟线程网络编程 (JDK 21+)

```java
// ✅ 推荐: 虚拟线程 + 阻塞 I/O
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (String host : hosts) {
        executor.submit(() -> {
            try (Socket socket = new Socket(host, 80)) {
                // 阻塞 I/O — 虚拟线程自动 unmount
                InputStream in = socket.getInputStream();
                in.read(new byte[1024]);
            } catch (IOException e) {
                e.printStackTrace();
            }
        });
    }
}
```

### 超时设置清单

```java
// Socket
socket.setSoTimeout(5000);              // 读超时 (read timeout, ms)
socket.connect(addr, 3000);             // 连接超时 (connect timeout, ms)

// HttpClient
HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(10));  // 连接超时
HttpRequest.newBuilder().timeout(Duration.ofSeconds(5));          // 请求超时

// NIO Selector
selector.select(1000);  // select 超时 (ms)
```

---

## 15. 相关链接

### 本地文档

- [HTTP 客户端](../http/) - HTTP Client 详解
- [并发编程](../concurrency/) - 线程、虚拟线程
- 网络时间线 - 详细历史演进

### 外部参考

**JEP 文档:**
- [JEP 321: HTTP Client](https://openjdk.org/jeps/321) - HTTP/2 Client API
- [JEP 353: Reimplement the Legacy Socket API](https://openjdk.org/jeps/353) - NioSocketImpl
- [JEP 373: Reimplement the Legacy DatagramSocket API](https://openjdk.org/jeps/373)
- [JEP 380: Unix-Domain Socket Channels](https://openjdk.org/jeps/380)
- [JEP 425: Virtual Threads (First Preview)](https://openjdk.org/jeps/425)
- [JEP 444: Virtual Threads (Final)](https://openjdk.org/jeps/444)
- [JEP 517: HTTP/3 for the HTTP Client API (Preview)](https://openjdk.org/jeps/517)

**技术文档:**
- [Java NIO Tutorial](https://docs.oracle.com/javase/tutorial/essential/io/)
- [Socket API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/net/package-summary.html)
- [QUIC RFC 9000](https://www.rfc-editor.org/rfc/rfc9000)
- [HTTP/3 RFC 9114](https://www.rfc-editor.org/rfc/rfc9114)
