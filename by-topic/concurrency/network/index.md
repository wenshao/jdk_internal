# 网络编程

> Socket、NIO、Unix Domain Socket 演进历程

[← 返回并发网络](../)

---
## 目录

1. [快速概览](#1-快速概览)
2. [核心贡献者](#2-核心贡献者)
3. [传统 Socket (BIO)](#3-传统-socket-bio)
4. [NIO (JDK 1.4+)](#4-nio-jdk-14)
5. [NIO.2 (JDK 7+)](#5-nio2-jdk-7)
6. [Unix Domain Socket (JDK 16+)](#6-unix-domain-socket-jdk-16)
7. [Virtual Threads (JDK 21+)](#7-virtual-threads-jdk-21)
8. [Sockets API 现代化 (JDK 24+)](#8-sockets-api-现代化-jdk-24)
9. [性能优化](#9-性能优化)
10. [重要 PR 分析](#10-重要-pr-分析)
11. [网络编程最佳实践](#11-网络编程最佳实践)
12. [相关链接](#12-相关链接)

---


## 1. 快速概览

```
JDK 1.0 ── JDK 1.4 ── JDK 7 ── JDK 11 ── JDK 16 ── JDK 18 ── JDK 21 ── JDK 26
   │         │         │        │        │        │        │        │
Socket/   NIO      NIO.2   HTTP   Unix    Structured  Virtual  HTTP/3
ServerSocket Channel  Async  Client Domain  Concurrency Threads  (预览)
           Selector  Group  (JEP 321) Socket              Loom    JEP 517
           (JSR 51) (AIO)
```

### 核心演进

| 版本 | 特性 | 说明 | JEP |
|------|------|------|-----|
| **JDK 1.0** | Socket/ServerSocket | TCP/UDP 基础 | - |
| **JDK 1.4** | NIO | Buffer, Channel, Selector | JSR 51 |
| **JDK 7** | NIO.2 | Path, Files, AsynchronousChannel | JSR 203 |
| **JDK 11** | HTTP Client | 新 API 标准化 | JEP 321 |
| **JDK 16** | Unix Domain Socket | 本地 IPC | JEP 380 |
| **JDK 21** | Virtual Threads | 轻量级网络 | JEP 444 |
| **JDK 26** | HTTP/3 | 基于 QUIC | JEP 517 |

---

## 2. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 网络/并发团队 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Alan Bateman | 43 | Oracle | NIO, NIO.2 (JSR 51, JSR 203) |
| 2 | Viktor Klang | 44 | Lightbend/Oracle | CompletableFuture |
| 3 | Jaikiran Pai | 34 | Red Hat/Oracle | HTTP/2, 网络层 |
| 4 | Chris Hegarty | 17 | Oracle | HTTP Client 基础 |
| 5 | Daniel Jeliński | 16 | Oracle | HTTP/2, 连接池 |
| 6 | Michael McMahon | 19 | Oracle | HTTP Client, NIO |
| 7 | [Brian Goetz](/by-contributor/profiles/brian-goetz.md) | 12 | Oracle | 并发架构 |

---

## 3. 传统 Socket (BIO)

### TCP Socket

```java
import java.net.*;

// TCP 客户端
try (Socket socket = new Socket("example.com", 80)) {
    // 输出流
    OutputStream out = socket.getOutputStream();
    out.write("GET / HTTP/1.1\r\n\r\n".getBytes());

    // 输入流
    InputStream in = socket.getInputStream();
    byte[] buffer = new byte[1024];
    int len;
    while ((len = in.read(buffer)) != -1) {
        System.out.write(buffer, 0, len);
    }
}
```

### TCP Server

```java
import java.net.*;

// TCP 服务器
try (ServerSocket server = new ServerSocket(8080)) {
    while (true) {
        // 阻塞等待连接
        Socket client = server.accept();
        // 处理连接
        handle(client);
    }
}
```

### UDP Socket

```java
import java.net.*;

// UDP 发送
try (DatagramSocket socket = new DatagramSocket()) {
    byte[] data = "Hello UDP".getBytes();
    InetAddress address = InetAddress.getByName("example.com");
    DatagramPacket packet = new DatagramPacket(
        data, data.length, address, 8080);
    socket.send(packet);
}
```

### 问题

1. **阻塞 I/O**: 每个连接一个线程
2. **资源浪费**: 线程上下文切换开销
3. **扩展性差**: C10K 问题

---

## 4. NIO (JDK 1.4+)

### 核心组件

```
┌─────────────────────────────────────────────────────────┐
│                      NIO 架构                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Buffer (缓冲区)                                         │
│  ├── ByteBuffer                                        │
│  ├── CharBuffer                                         │
│  └── ...                                               │
│                                                         │
│  Channel (通道)                                          │
│  ├── FileChannel                                        │
│  ├── SocketChannel                                      │
│  ├── ServerSocketChannel                                │
│  └── DatagramChannel                                    │
│                                                         │
│  Selector (选择器)                                       │
│  └── 多路复用 I/O                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### ByteBuffer

```java
// 创建 Buffer
ByteBuffer buffer = ByteBuffer.allocate(1024);

// 写入数据
buffer.put("Hello NIO".getBytes(StandardCharsets.UTF_8));

// 切换读模式
buffer.flip();

// 读取数据
while (buffer.hasRemaining()) {
    byte b = buffer.get();
    System.out.print((char) b);
}

// 清空 Buffer
buffer.clear();

// 直接 Buffer (堆外内存)
ByteBuffer direct = ByteBuffer.allocateDirect(1024);
```

### SocketChannel

```java
import java.nio.*;
import java.nio.channels.*;

// 客户端
SocketChannel channel = SocketChannel.open();
channel.configureBlocking(false);  // 非阻塞
channel.connect(new InetSocketAddress("example.com", 80));

while (!channel.finishConnect()) {
    // 等待连接完成
}

// 写入数据
ByteBuffer buffer = ByteBuffer.wrap("GET / HTTP/1.1\r\n\r\n".getBytes());
channel.write(buffer);

// 读取数据
ByteBuffer response = ByteBuffer.allocate(1024);
channel.read(response);

channel.close();
```

### ServerSocketChannel

```java
import java.nio.*;
import java.nio.channels.*;

// 服务器
ServerSocketChannel server = ServerSocketChannel.open();
server.configureBlocking(false);
server.bind(new InetSocketAddress(8080));

Selector selector = Selector.open();
server.register(selector, SelectionKey.OP_ACCEPT);

while (true) {
    // 阻塞等待事件
    selector.select();

    for (SelectionKey key : selector.selectedKeys()) {
        if (key.isAcceptable()) {
            // 接受新连接
            SocketChannel client = server.accept();
            client.configureBlocking(false);
            client.register(selector, SelectionKey.OP_READ);
        }
        if (key.isReadable()) {
            // 读取数据
            SocketChannel client = (SocketChannel) key.channel();
            ByteBuffer buffer = ByteBuffer.allocate(1024);
            client.read(buffer);
        }
    }
    selector.selectedKeys().clear();
}
```

### Selector 多路复用

```java
// 注册多个 Channel
Selector selector = Selector.open();

SocketChannel channel1 = SocketChannel.open();
channel1.configureBlocking(false);
channel1.register(selector, SelectionKey.OP_CONNECT);

SocketChannel channel2 = SocketChannel.open();
channel2.configureBlocking(false);
channel2.register(selector, SelectionKey.OP_CONNECT);

// 单线程处理多个连接
while (true) {
    int ready = selector.select();
    if (ready == 0) continue;

    for (SelectionKey key : selector.selectedKeys()) {
        if (key.isConnectable()) {
            // 处理连接
        }
        if (key.isReadable()) {
            // 处理读取
        }
        if (key.isWritable()) {
            // 处理写入
        }
    }
}
```

---

## 5. NIO.2 (JDK 7+)

### Path 和 Files

```java
import java.nio.file.*;

// Path 操作
Path path = Paths.get("/tmp/example.txt");

// 文件操作
if (!Files.exists(path)) {
    Files.createFile(path);
}

// 写入文件
Files.writeString(path, "Hello NIO.2");

// 读取文件
String content = Files.readString(path);

// 复制文件
Path copy = Files.copy(path, Paths.get("/tmp/copy.txt"));

// 移动文件
Files.move(path, Paths.get("/tmp/moved.txt"));

// 删除文件
Files.deleteIfExists(path);
```

### WatchService

```java
import java.nio.file.*;

// 监控文件变化
Path dir = Paths.get("/tmp");
WatchService watcher = FileSystems.getDefault().newWatchService();
WatchKey key = dir.register(watcher,
    StandardWatchEventKinds.ENTRY_CREATE,
    StandardWatchEventKinds.ENTRY_DELETE,
    StandardWatchEventKinds.ENTRY_MODIFY);

while (true) {
    WatchKey watchKey = watcher.take();
    for (WatchEvent<?> event : watchKey.pollEvents()) {
        System.out.println(event.kind() + ": " + event.context());
    }
    watchKey.reset();
}
```

### AsynchronousChannel

```java
import java.nio.channels.*;
import java.util.concurrent.*;

// 异步文件通道
AsynchronousFileChannel file = AsynchronousFileChannel.open(
    Paths.get("example.txt"),
    StandardOpenOption.READ);

Future<Integer> operation = file.read(ByteBuffer.allocate(1024), 0);

while (!operation.isDone()) {
    // 等待完成
}

Integer bytesRead = operation.get();
```

### 异步 Socket

```java
import java.nio.channels.*;
import java.util.concurrent.*;

// 异步 Socket
AsynchronousSocketChannel client =
    AsynchronousSocketChannel.open();

// 连接
Future<Void> connect = client.connect(
    new InetSocketAddress("example.com", 80));

// 等待连接完成
connect.get();

// 异步读取
ByteBuffer buffer = ByteBuffer.allocate(1024);
Future<Integer> read = client.read(buffer);

// 使用 CompletionHandler
client.read(buffer, null, new CompletionHandler<Integer, Void>() {
    @Override
    public void completed(Integer result, Void attachment) {
        System.out.println("Read " + result + " bytes");
    }

    @Override
    public void failed(Throwable exc, Void attachment) {
        exc.printStackTrace();
    }
});
```

---

## 6. Unix Domain Socket (JDK 16+)

### JEP 380: Unix Domain Sockets

**特性**:
- 本地进程间通信
- 比 TCP loopback 更高效
- 文件系统权限控制

### 使用

```java
import java.net.*;
import java.nio.channels.*;

// Unix Domain Socket 客户端 (JDK 16+)
SocketChannel channel = SocketChannel.open(
    StandardProtocolFamily.UNIX);
channel.connect(UnixDomainSocketAddress.of(
    new File("/tmp/socket.sock")));

ByteBuffer buffer = ByteBuffer.wrap("Hello UDS".getBytes());
channel.write(buffer);

channel.close();
```

```java
// Unix Domain Socket 服务器
ServerSocketChannel server = ServerSocketChannel.open(
    StandardProtocolFamily.UNIX);
server.bind(UnixDomainSocketAddress.of(
    new File("/tmp/socket.sock")));

SocketChannel client = server.accept();
ByteBuffer buffer = ByteBuffer.allocate(1024);
client.read(buffer);
```

---

## 7. Virtual Threads (JDK 21+)

### 传统线程问题

```java
// 每个请求一个线程
ExecutorService executor = Executors.newFixedThreadPool(200);

executor.submit(() -> {
    // 阻塞 I/O
    Socket socket = new Socket("example.com", 80);
    // ...
});
```

### Virtual Thread 方案

```java
import java.util.concurrent.*;

// Virtual Thread (JDK 21+)
try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> {
        // 阻塞 I/O 不阻塞平台线程
        try (Socket socket = new Socket("example.com", 80)) {
            // ...
        }
    });
}
```

### 创建 Virtual Thread

```java
// 方式 1: ExecutorService
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();

// 方式 2: 直接创建
Thread vThread = Thread.ofVirtual()
    .name("virtual-thread")
    .start(() -> {
        // 任务
    });

// 方式 3: Factory
ThreadFactory factory = Thread.ofVirtual().factory();
Thread vThread = factory.newThread(() -> {
    // 任务
});
vThread.start();
```

---

## 8. Sockets API 现代化 (JDK 24+)

### JEP 521: Structured Concurrency

```java
// Structured Concurrency (JDK 24+ 预览)
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Supplier<String> url1 = scope.fork(() -> fetch("url1"));
    Supplier<String> url2 = scope.fork(() -> fetch("url2"));

    scope.join();          // 等待所有任务
    scope.throwIfFailed(); // 检查异常

    String result = url1.get() + url2.get();
}
```

---

## 9. 性能优化

### NIO vs BIO

| 特性 | BIO | NIO |
|------|-----|-----|
| 线程模型 | 每连接一线程 | 单线程多连接 |
| 内存占用 | 高 (线程栈) | 低 |
| CPU 开销 | 上下文切换 | 少 |
| 适用场景 | 简单应用 | 高并发 |

### Buffer 优化

```java
// 使用直接 Buffer (堆外内存)
ByteBuffer direct = ByteBuffer.allocateDirect(1024);

// 使用内存池
ByteBuffer buffer = ByteBuffer.allocateDirect(1024 * 1024);

// 避免频繁分配
private static final ByteBuffer REUSABLE_BUFFER =
    ByteBuffer.allocateDirect(8192);
```

### Selector 优化

```java
// 减少 select() 调用
while (true) {
    int ready = selector.select(1000);  // 超时 1 秒
    // 处理事件
}

// 使用多个 Selector
Selector[] selectors = new Selector[Runtime.getRuntime().availableProcessors()];
```

---

## 10. 重要 PR 分析

### NIO 性能优化

#### JDK-8348880: AtomicReferenceArray 优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ +15-25% 缓存访问性能

将 `ConcurrentHashMap` 替换为 `AtomicReferenceArray`：

**优化点**:
- 消除 `int` → `Integer` 装箱
- 数组访问比 HashMap 快
- 内存占用减少 85%

**适用场景**: 高频访问的缓存结构

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
> **影响**: ⭐⭐⭐⭐ +40-60% 性能提升

使用 SWAR (SIMD Within A Register) 技术：

**优化点**:
- 消除查找表
- 寄存器内并行计算
- 使用 `Long.expand` intrinsic

**适用场景**: 分布式追踪、会话管理

→ [详细分析](/by-pr/8353/8353741.md)

---

## 11. 网络编程最佳实践

### I/O 模型选择

| 场景 | 推荐方案 | 说明 |
|------|----------|------|
| **简单应用** | BIO | 代码简单，易于理解 |
| **高并发** | NIO + Selector | 单线程处理多连接 |
| **极高并发** | 虚拟线程 + BIO | JDK 21+，简化异步代码 |
| **本地 IPC** | Unix Domain Socket | 比 TCP loopback 更快 |

### 虚拟线程网络编程 (JDK 21+)

```java
// ✅ 推荐：虚拟线程处理阻塞 I/O
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (String url : urls) {
        executor.submit(() -> {
            try (Socket socket = new Socket(host, port)) {
                // 阻塞 I/O 不阻塞平台线程
                // 处理请求
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

### NIO + 虚拟线程混合模式

```java
// NIO 处理连接
ServerSocketChannel server = ServerSocketChannel.open();
server.configureBlocking(false);
Selector selector = Selector.open();
server.register(selector, SelectionKey.OP_ACCEPT);

// 虚拟线程处理 I/O
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    while (true) {
        selector.select(1000);
        for (SelectionKey key : selector.selectedKeys()) {
            if (key.isAcceptable()) {
                SocketChannel client = server.accept();
                executor.submit(() -> handleConnection(client));
            }
        }
    }
}
```

### Unix Domain Socket 优化 (JDK 16+)

```java
// ✅ 推荐：本地通信使用 UDS
SocketChannel channel = SocketChannel.open(StandardProtocolFamily.UNIX);
channel.connect(UnixDomainSocketAddress.of(new File("/tmp/my.sock")));

// 比 TCP loopback 快 2-3 倍
// 无网络协议栈开销
```

---

## 12. 相关链接

### 本地文档

- [HTTP 客户端](../http/) - HTTP/2, HTTP/3
- [并发编程](../concurrency/) - 线程、虚拟线程

### 外部参考

**JEP 文档:**
- [JEP 380: Unix Domain Sockets](https://openjdk.org/jeps/380)
- [JEP 426: Virtual Threads](https://openjdk.org/jeps/426)
- [JEP 521: Structured Concurrency](https://openjdk.org/jeps/521)

**技术文档:**
- [Java NIO Tutorial](https://docs.oracle.com/javase/tutorial/essential/io/)
- [Socket API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/net/package-summary.html)
