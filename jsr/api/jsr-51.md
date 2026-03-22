# JSR 51: New I/O APIs for the Java Platform

> **状态**: ✅ Final | **JDK**: 1.4 (2002) | **Specification Lead**: Mark Reinhold (Sun Microsystems)

[← 返回 JSR 索引](../index.md) | [外部链接](https://jcp.org/en/jsr/detail?id=51)

---
## 目录

1. [一眼看懂](#1-一眼看懂)
2. [概述](#2-概述)
3. [核心组件](#3-核心组件)
4. [Buffer 体系](#4-buffer-体系)
5. [Channel 体系](#5-channel-体系)
6. [Selector 与非阻塞 I/O](#6-selector-与非阻塞-io)
7. [内存映射文件](#7-内存映射文件)
8. [Charset 编解码](#8-charset-编解码)
9. [与传统 I/O 对比](#9-与传统-io-对比)
10. [后续演进](#10-后续演进)
11. [最佳实践](#11-最佳实践)
12. [与其他 JSR/JEP 的关系](#12-与其他-jsrjep-的关系)
13. [相关链接](#13-相关链接)
14. [参考资料](#14-参考资料)

---

## 1. 一眼看懂

```
┌─────────────────────────────────────────────────────────────────────┐
│                    JSR 51 核心内容                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. Buffer (缓冲区)      ByteBuffer, CharBuffer, IntBuffer...      │
│  2. Channel (通道)       FileChannel, SocketChannel, Pipe          │
│  3. Selector (选择器)    多路复用 (Multiplexing), 非阻塞 I/O        │
│  4. Charset (字符集)     编码/解码, CharsetEncoder/Decoder          │
│  5. Direct Buffer        堆外内存, 零拷贝                           │
│  6. MappedByteBuffer     内存映射文件                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. 概述

JSR 51 引入了 `java.nio` 包（New I/O），为 Java 提供了高性能、可扩展的 I/O 操作能力。在此之前，Java 只有基于流（stream）的阻塞式 I/O（`java.io`），每个连接需要一个线程，无法支撑高并发服务器。

| 特性 | 说明 |
|------|------|
| **Buffer** | 面向缓冲区的 I/O，替代逐字节读写 |
| **Channel** | 双向数据传输通道，替代单向 InputStream/OutputStream |
| **Selector** | 单线程管理多个 Channel，实现 I/O 多路复用 |
| **Direct Buffer** | 堆外内存分配，减少数据拷贝 |
| **Memory-Mapped File** | 将文件映射到内存，高效处理大文件 |
| **Charset** | 统一的字符集编解码框架 |

---

## 3. 核心组件

### java.nio 包结构

```
java.nio
├── Buffer / ByteBuffer / CharBuffer / IntBuffer / ...
├── ByteOrder                          (字节序)
├── MappedByteBuffer                   (内存映射)
├── channels/
│   ├── Channel / ReadableByteChannel / WritableByteChannel
│   ├── FileChannel
│   ├── SocketChannel / ServerSocketChannel
│   ├── DatagramChannel
│   ├── Pipe
│   ├── Selector / SelectionKey
│   └── FileLock
└── charset/
    ├── Charset
    ├── CharsetEncoder / CharsetDecoder
    └── CoderResult
```

---

## 4. Buffer 体系

### 核心概念

```java
// Buffer 的四个关键属性
// capacity >= limit >= position >= mark
ByteBuffer buf = ByteBuffer.allocate(1024);  // 堆内缓冲区

buf.put((byte) 42);      // 写入数据, position++
buf.flip();               // 切换到读模式: limit=position, position=0
byte b = buf.get();       // 读取数据, position++
buf.clear();              // 重置: position=0, limit=capacity
buf.compact();            // 压缩: 未读数据移到开头
```

### Direct Buffer (直接缓冲区)

```java
// 堆外内存，避免 JVM 堆与操作系统之间的数据拷贝
ByteBuffer direct = ByteBuffer.allocateDirect(1024);

// 优势：I/O 操作更快 (减少一次拷贝)
// 劣势：分配/回收成本高，不受 GC 直接管理
// 适用于：长期存活的大缓冲区，频繁 I/O 操作
```

---

## 5. Channel 体系

### FileChannel

```java
// 文件通道：支持读、写、映射、锁定
try (FileChannel ch = FileChannel.open(path, READ, WRITE)) {
    ByteBuffer buf = ByteBuffer.allocate(4096);
    int bytesRead = ch.read(buf);       // 读取
    buf.flip();
    ch.write(buf);                       // 写入
    ch.position(0);                      // 定位

    // 文件传输 (零拷贝优化)
    ch.transferTo(0, ch.size(), targetChannel);
}
```

### SocketChannel (非阻塞)

```java
// 非阻塞套接字通道
SocketChannel sc = SocketChannel.open();
sc.configureBlocking(false);             // 设置非阻塞模式
sc.connect(new InetSocketAddress("host", 8080));

while (!sc.finishConnect()) {
    // 连接尚未完成，可做其他事
}

ByteBuffer buf = ByteBuffer.allocate(1024);
int n = sc.read(buf);   // 非阻塞：可能返回 0 (无数据可读)
```

---

## 6. Selector 与非阻塞 I/O

### 多路复用模型

```java
// 一个线程管理成千上万个连接
Selector selector = Selector.open();

ServerSocketChannel server = ServerSocketChannel.open();
server.configureBlocking(false);
server.bind(new InetSocketAddress(8080));
server.register(selector, SelectionKey.OP_ACCEPT);

while (true) {
    selector.select();  // 阻塞直到有事件就绪
    Set<SelectionKey> keys = selector.selectedKeys();
    for (SelectionKey key : keys) {
        if (key.isAcceptable()) {
            SocketChannel client = server.accept();
            client.configureBlocking(false);
            client.register(selector, SelectionKey.OP_READ);
        } else if (key.isReadable()) {
            SocketChannel client = (SocketChannel) key.channel();
            ByteBuffer buf = ByteBuffer.allocate(1024);
            client.read(buf);
            // 处理数据...
        }
    }
    keys.clear();
}
```

---

## 7. 内存映射文件

```java
// 将文件直接映射到进程地址空间
try (FileChannel ch = FileChannel.open(path, READ, WRITE)) {
    MappedByteBuffer mmap = ch.map(
        FileChannel.MapMode.READ_WRITE, 0, ch.size()
    );

    // 像操作内存一样操作文件
    mmap.putInt(0, 42);
    int value = mmap.getInt(0);
    mmap.force();  // 强制刷盘
}
// 适用于：大文件处理、进程间共享内存、数据库引擎
```

---

## 8. Charset 编解码

```java
Charset utf8 = Charset.forName("UTF-8");

// 编码: String → ByteBuffer
ByteBuffer encoded = utf8.encode("你好世界");

// 解码: ByteBuffer → CharBuffer
CharBuffer decoded = utf8.decode(encoded);
```

---

## 9. 与传统 I/O 对比

| 特性 | java.io (传统) | java.nio (JSR 51) |
|------|----------------|-------------------|
| 模型 | 面向流 (Stream) | 面向缓冲区 (Buffer) |
| 方向 | 单向 (Input/Output) | 双向 (Channel) |
| 阻塞 | 阻塞式 | 支持非阻塞 |
| 多路复用 | 不支持 | Selector |
| 内存 | 堆内 | 堆内 + 堆外 (Direct) |
| 线程模型 | 一连接一线程 | 一线程管理多连接 |

---

## 10. 后续演进

| 版本 | 特性 | 说明 |
|------|------|------|
| JDK 1.4 | JSR 51 (NIO) | Buffer, Channel, Selector |
| JDK 7 | JSR 203 (NIO.2) | Path/Files API, 异步 Channel, WatchService |
| JDK 7 | try-with-resources | 简化 Channel 资源管理 |
| JDK 13 | JEP 353 | Socket API 重新实现 (基于 NIO) |
| JDK 16 | JEP 380 | Unix-Domain Socket Channels |

### 产业影响

JSR 51 的非阻塞 I/O 模型催生了一批高性能网络框架：

- **Apache MINA** — 早期 NIO 框架
- **Netty** — 最流行的异步事件驱动网络框架
- **Grizzly** — GlassFish 的 NIO 框架
- **Vert.x** — 响应式应用工具包，底层基于 Netty

---

## 11. 最佳实践

### 1. 长连接服务器使用 Selector

```java
// 不推荐：一连接一线程 (C10K 问题)
new Thread(() -> handleClient(socket)).start();

// 推荐：Selector 多路复用 (或使用 Netty 等框架)
selector.select();
```

### 2. Direct Buffer 适当使用

```java
// 不推荐：频繁创建/销毁 Direct Buffer
ByteBuffer buf = ByteBuffer.allocateDirect(64);  // 开销大

// 推荐：复用 Direct Buffer，或用于长期大块 I/O
private static final ByteBuffer REUSABLE = ByteBuffer.allocateDirect(8192);
```

### 3. 使用 transferTo 实现零拷贝

```java
// 不推荐：手动循环拷贝
while (src.read(buf) != -1) { buf.flip(); dst.write(buf); buf.clear(); }

// 推荐：零拷贝传输
src.transferTo(0, src.size(), dst);
```

---

## 12. 与其他 JSR/JEP 的关系

| JSR/JEP | 说明 |
|---------|------|
| JSR 203 | NIO.2 (JDK 7)，Path/Files/AsynchronousChannel |
| JSR 166 | Concurrency Utilities (JDK 5)，与 NIO 配合实现高性能服务器 |
| JEP 353 | Reimplement Legacy Socket API (JDK 13) |
| JEP 380 | Unix-Domain Socket Channels (JDK 16) |

---

## 13. 相关链接

### 官方资源

- [JSR 51 规范](https://jcp.org/en/jsr/detail?id=51)
- [Package java.nio](https://docs.oracle.com/javase/8/docs/api/java/nio/package-summary.html)
- [Java NIO Tutorial — Oracle](https://docs.oracle.com/javase/tutorial/essential/io/fileio.html)

### 本地文档

- [NIO 专题](/by-topic/api/nio/)
- [JDK 1.4 新特性](/by-version/jdk1.4/)
- [JSR 203 (NIO.2)](/jsr/api/jsr-203.md)

---

## 14. 参考资料

- **Mark Reinhold**, JSR 51 Specification Lead, Sun Microsystems
- 《Java NIO》- Ron Hitchens (O'Reilly)
- 《Netty in Action》- Norman Maurer, Marvin Allen Wolfthal

---

> **最后更新**: 2026-03-22
