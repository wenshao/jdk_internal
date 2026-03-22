# NIO 新 I/O

> Buffer, Channel, Selector, NIO.2 — 从 JSR 51 到 Virtual Threads 的完整演进

[← 返回主题索引](../)

---

## 目录

- [1. 架构与演进](#1-架构与演进)
- [2. Buffer 深入](#2-buffer-深入)
- [3. Channel 深入](#3-channel-深入)
- [4. Selector 多路复用深入](#4-selector-多路复用深入)
- [5. NIO.2 文件 API](#5-nio2-文件-api)
- [6. 虚拟线程与 NIO](#6-虚拟线程与-nio)
- [7. MemorySegment 与 ByteBuffer](#7-memorysegment-与-bytebuffer)
- [8. 性能最佳实践](#8-性能最佳实践)
- [9. 核心贡献者](#9-核心贡献者)
- [10. 相关链接](#10-相关链接)

---

## 1. 架构与演进

### 三个时代

```
JDK 1.0          JDK 1.4           JDK 7             JDK 21          JDK 22+
  │               │                 │                  │               │
  │  java.io      │  JSR 51 (NIO)   │  JSR 203 (NIO.2) │  Loom         │  FFM
  │  Stream/File  │  Buffer/Channel │  Path/Files       │  Virtual      │  MemorySegment
  │  阻塞 I/O     │  Selector       │  WatchService     │  Threads      │  替代 ByteBuffer
```

### 核心演进时间线

| 版本 | 规范 | 核心特性 | 设计动机 |
|------|------|----------|----------|
| **JDK 1.0** | - | `InputStream`/`OutputStream`, `java.io.File` | 基本 I/O |
| **JDK 1.4** | JSR 51 | Buffer, Channel, Selector, Charset | 解决 C10K: 单线程管理多连接 |
| **JDK 7** | JSR 203 | Path, Files, WatchService, AsynchronousChannel | 替代 `java.io.File` 的缺陷; 真正的异步 I/O |
| **JDK 11** | - | `Files.readString()`/`writeString()` | 简化常见文件操作 |
| **JDK 13** | JEP 353 | `SocketChannel` 重新实现 (替换旧 `PlainSocketImpl`) | 为 Loom 做准备 |
| **JDK 16** | JEP 380 | Unix-Domain Socket Channels | `SocketChannel` 支持 `AF_UNIX` |
| **JDK 21** | JEP 444 | Virtual Threads GA — NIO Channel 自动与虚拟线程协作 | 同步风格 + 异步性能 |
| **JDK 22** | JEP 454 | Foreign Function & Memory API (GA) — `MemorySegment` | 替代 `ByteBuffer` 做 off-heap |

### NIO 三大组件关系

```
  应用代码
     │
     ▼
  Buffer (数据容器) ◄──read/write──► Channel (I/O 通道)
                                        │ register
                                        ▼
                                    Selector (多路复用器)
                                        │
                                        ▼
                                  OS Kernel I/O
                            (epoll / kqueue / wepoll)
```

### IO vs NIO vs NIO.2 对比

| 特性 | java.io (BIO) | java.nio (NIO) | java.nio.2 (NIO.2) |
|------|---------------|----------------|---------------------|
| **模型** | 阻塞 (Blocking) | 非阻塞 (Non-blocking) | 异步 (Asynchronous) |
| **数据方向** | 单向 (Stream) | 双向 (Channel) | 双向 + 回调 |
| **缓冲** | 无内置 Buffer | Buffer-oriented | Buffer + CompletionHandler |
| **多路复用** | 不支持 | Selector | OS 异步 I/O (IOCP/io_uring) |
| **文件 API** | `java.io.File` | FileChannel | Path, Files, WatchService |
| **线程模型** | 一连接一线程 | 单线程多连接 | 线程池 + 回调 |

---

## 2. Buffer 深入

### Buffer 类型层次

源码中 `Buffer` 是 `sealed` 类 (JDK 17+), 只允许 7 个子类:

```
Buffer (abstract sealed class)                     ← java.nio.Buffer
    │
    │  permits: ByteBuffer, CharBuffer, DoubleBuffer,
    │           FloatBuffer, IntBuffer, LongBuffer, ShortBuffer
    │
    ├── ByteBuffer (abstract sealed)               ← 最重要, 最常用
    │       ├── HeapByteBuffer                     ← 堆内存, byte[] 支撑
    │       ├── DirectByteBuffer                   ← 堆外内存, native memory
    │       └── MappedByteBuffer (abstract sealed) ← 内存映射文件
    │               └── DirectByteBuffer           ← 实际实现
    │
    ├── CharBuffer
    ├── ShortBuffer
    ├── IntBuffer
    ├── LongBuffer
    ├── FloatBuffer
    └── DoubleBuffer
```

> **源码验证**: `Buffer.java` 第 202-204 行:
> `public abstract sealed class Buffer permits ByteBuffer, CharBuffer, DoubleBuffer, FloatBuffer, IntBuffer, LongBuffer, ShortBuffer`

### ByteBuffer 内部结构

`Buffer` 的核心字段 (来源: `Buffer.java` 第 217-233 行):

```java
// Invariants: mark <= position <= limit <= capacity
private int mark = -1;        // 标记位置, 用于 reset()
private int position = 0;     // 当前读写位置
private int limit;            // 读写上界
private final int capacity;   // 总容量 (不可变)

long address;                 // 堆外内存地址 (Direct Buffer)
                              // 或堆内 byte[] 的基地址偏移
final MemorySegment segment;  // JEP-370 内存访问 API 集成
```

不变式 (invariant):

```
0 <= mark <= position <= limit <= capacity
```

### Buffer 状态转换 (ASCII 图示)

以 capacity=10 的 Buffer 为例, 写入 5 字节后的各种操作:

以 capacity=10 的 Buffer, 写入 5 字节 "ABCDE" 后的各操作:

```
1. 写入后:        pos=5, lim=10
   ┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
   │A│B│C│D│E│ │ │ │ │ │    position ▲        limit/capacity ▲
   └─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘
    0 1 2 3 4 5 6 7 8 9

2. flip():        pos=0, lim=5 (写→读切换)
   ┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
   │A│B│C│D│E│ │ │ │ │ │    ▲position   ▲limit       ▲capacity
   └─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘

3. 读3字节后:      pos=3, lim=5
   ┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
   │A│B│C│D│E│ │ │ │ │ │         ▲pos  ▲lim
   └─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘

4. compact():     pos=2, lim=10 (未读数据移到开头, 准备追加写)
   ┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
   │D│E│ │ │ │ │ │ │ │ │    ▲pos                     ▲lim
   └─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘

5. clear():       pos=0, lim=10 (逻辑重置, 数据仍在)
6. rewind():      pos=0, lim不变 (重读)
```

### 操作方法源码总结

| 方法 | 源码实现 (Buffer.java) | 效果 |
|------|------------------------|------|
| `flip()` | `limit = position; position = 0; mark = -1;` | 写→读切换 |
| `clear()` | `position = 0; limit = capacity; mark = -1;` | 逻辑重置, 准备写入 |
| `rewind()` | `position = 0; mark = -1;` | 重读 (limit 不变) |
| `compact()` | 将 `[position, limit)` 数据移到 `[0, remaining)`, 然后 `position = remaining; limit = capacity;` | 压缩未读数据, 准备追加写入 |
| `mark()` | `mark = position;` | 记录当前位置 |
| `reset()` | `position = mark;` | 回到 mark 位置 |

### Direct Buffer vs Heap Buffer

```
┌────────────────────────────────────────────────────────────────┐
│                    Heap Buffer (堆内)                           │
│                                                                │
│   ByteBuffer.allocate(1024)                                    │
│                                                                │
│   JVM Heap                                                     │
│   ┌────────────────────┐                                       │
│   │  byte[] hb         │ ← 数据存储在堆上的 byte 数组           │
│   │  (受 GC 管理)       │                                       │
│   └────────────────────┘                                       │
│                                                                │
│   优点: 分配/回收快, GC 自动管理                                 │
│   缺点: I/O 时需要拷贝到临时 Direct Buffer (JNI 边界)           │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│                    Direct Buffer (堆外)                         │
│                                                                │
│   ByteBuffer.allocateDirect(1024)                              │
│                                                                │
│   Native Memory                                                │
│   ┌────────────────────┐                                       │
│   │  malloc() 分配      │ ← 数据在 JVM 堆外, 通过 address 字段访问│
│   │  (Cleaner 回收)     │                                       │
│   └────────────────────┘                                       │
│                                                                │
│   优点: I/O 零拷贝 (无需 JNI 临时 Buffer), 不受 GC 移动影响      │
│   缺点: 分配/回收慢, 需要 Cleaner (PhantomReference) 机制回收    │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

#### Cleaner 回收机制

Direct Buffer 不由 GC 直接回收其 native memory. 源码中使用 `BufferCleaner` (基于 `PhantomReference`):

```
DirectByteBuffer 分配流程:
  1. Unsafe.allocateMemory(size)          → 分配 native memory
  2. BufferCleaner.register(this, ...)    → 注册 PhantomReference
  3. 当 DirectByteBuffer 对象被 GC 时:
     → PhantomReference 入队
     → Cleaner 线程调用 Deallocator.run()
     → Unsafe.freeMemory(address)
```

> **源码验证**: `Direct-X-Buffer.java.template` 第 126 行:
> `cleaner = BufferCleaner.register(this, new Deallocator(base, size, cap));`

#### I/O 路径对比

```
Heap Buffer 写入 Channel:                Direct Buffer 写入 Channel:

  HeapByteBuffer                           DirectByteBuffer
       │                                        │
       ▼                                        ▼
  复制到临时 Direct Buffer                  直接传给 OS
       │                                        │
       ▼                                        ▼
  系统调用 write()                          系统调用 write()
       │                                        │
       ▼                                        ▼
    内核缓冲区                               内核缓冲区
```

### MappedByteBuffer: 内存映射文件

`MappedByteBuffer` 通过 `mmap()` 系统调用将文件直接映射到进程地址空间, 实现真正的零拷贝:

```java
try (FileChannel channel = FileChannel.open(Path.of("large.bin"),
        StandardOpenOption.READ, StandardOpenOption.WRITE)) {

    // 映射整个文件到内存
    MappedByteBuffer mapped = channel.map(
        FileChannel.MapMode.READ_WRITE, 0, channel.size());

    // 像操作普通 ByteBuffer 一样操作文件
    mapped.putInt(0, 0xCAFEBABE);
    int magic = mapped.getInt(0);

    // 关键方法:
    mapped.load();            // 预加载到物理内存 (避免缺页中断)
    mapped.isLoaded();        // 检查是否已加载到物理内存
    mapped.force();           // 强制刷新到磁盘 (类似 fsync)
    mapped.force(0, 4096);    // 部分刷新 (JDK 13+)
}
```

映射模式 (`FileChannel.MapMode`):

| 模式 | 说明 | OS 调用 |
|------|------|---------|
| `READ_ONLY` | 只读映射 | `mmap(PROT_READ)` |
| `READ_WRITE` | 读写映射, 修改直接写入文件 | `mmap(PROT_READ\|PROT_WRITE)` |
| `PRIVATE` | 写时复制 (Copy-on-Write), 修改不写入文件 | `mmap(MAP_PRIVATE)` |

### ByteOrder: 字节序

```java
// ByteOrder 是 enum (JDK 源码: ByteOrder.java)
// 两个值: BIG_ENDIAN, LITTLE_ENDIAN

// 查看平台原生字节序
ByteOrder order = ByteOrder.nativeOrder();
// 大多数现代平台 (x86, ARM) 返回 LITTLE_ENDIAN

// 设置 ByteBuffer 字节序
ByteBuffer buffer = ByteBuffer.allocate(4);
buffer.order(ByteOrder.BIG_ENDIAN);     // 网络字节序 (默认)
buffer.putInt(0x01020304);
// 内存布局: [01] [02] [03] [04]

buffer.clear();
buffer.order(ByteOrder.LITTLE_ENDIAN);
buffer.putInt(0x01020304);
// 内存布局: [04] [03] [02] [01]
```

> **源码验证**: `ByteOrder.java` 是 `enum`, 通过 `Unsafe.getUnsafe().isBigEndian()` 判断原生字节序.

### Buffer 视图与类型转换

```java
ByteBuffer buf = ByteBuffer.allocate(1024).order(ByteOrder.nativeOrder());

IntBuffer intView = buf.asIntBuffer();      // 类型视图 — 共享数据, 独立游标
ByteBuffer dup = buf.duplicate();           // 共享数据, 独立 position/limit
ByteBuffer slice = buf.slice(10, 40);       // 子区间视图 (JDK 13+)
```

---

## 3. Channel 深入

### Channel 接口层次

```
Channel (接口)                                  ← isOpen(), close()
    │
    ├── ReadableByteChannel                     ← read(ByteBuffer)
    │       │
    │       └── ScatteringByteChannel           ← read(ByteBuffer[])  分散读
    │
    ├── WritableByteChannel                     ← write(ByteBuffer)
    │       │
    │       └── GatheringByteChannel            ← write(ByteBuffer[]) 聚集写
    │
    ├── ByteChannel                             ← extends Readable + Writable
    │
    ├── SeekableByteChannel                     ← position(), size(), truncate()
    │
    ├── InterruptibleChannel                    ← 可被 Thread.interrupt() 中断
    │
    ├── NetworkChannel                          ← bind(), getLocalAddress()
    │
    ├── SelectableChannel                       ← register(Selector), configureBlocking()
    │       │
    │       └── AbstractSelectableChannel
    │               ├── SocketChannel           ← TCP 客户端
    │               ├── ServerSocketChannel     ← TCP 服务端
    │               ├── DatagramChannel         ← UDP
    │               └── Pipe.SourceChannel/SinkChannel
    │
    ├── AsynchronousChannel                     ← 异步 I/O (NIO.2)
    │       ├── AsynchronousSocketChannel
    │       ├── AsynchronousServerSocketChannel
    │       └── AsynchronousFileChannel
    │
    └── FileChannel                             ← 文件 I/O (不可 select)
            extends AbstractInterruptibleChannel
            implements SeekableByteChannel,
                       GatheringByteChannel,
                       ScatteringByteChannel
```

### FileChannel: 文件 I/O 核心

```java
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.*;

// 打开方式
FileChannel ch = FileChannel.open(Path.of("data.bin"),
    StandardOpenOption.READ,
    StandardOpenOption.WRITE,
    StandardOpenOption.CREATE);

// ─── 基本读写 ───
ByteBuffer buf = ByteBuffer.allocateDirect(8192);
int bytesRead = ch.read(buf);           // 读取到 buffer
buf.flip();
int bytesWritten = ch.write(buf);       // 从 buffer 写出

// ─── 定位读写 (不影响 channel position) ───
ch.read(buf, 1024);   // 从文件偏移 1024 读取
ch.write(buf, 2048);  // 写到文件偏移 2048

// ─── Scatter/Gather I/O (向量化 I/O) ───
ByteBuffer header = ByteBuffer.allocate(128);
ByteBuffer body = ByteBuffer.allocate(4096);
ch.read(new ByteBuffer[]{header, body});     // 分散读: 先填 header, 再填 body
ch.write(new ByteBuffer[]{header, body});    // 聚集写: 依次写 header 和 body

// ─── 文件锁 ───
FileLock lock = ch.lock();                   // 独占锁 (阻塞)
FileLock lock = ch.tryLock();                // 非阻塞尝试
FileLock lock = ch.lock(0, 1024, true);      // 共享锁, 锁定前 1024 字节
lock.release();

// ─── 强制刷盘 ───
ch.force(true);   // true = 同时刷新元数据 (类似 fsync)
ch.force(false);  // 只刷新数据 (类似 fdatasync)

// ─── 截断 ───
ch.truncate(1024);  // 截断到 1024 字节
```

### transferTo/transferFrom: 零拷贝 (Zero-Copy)

`FileChannel.transferTo()` 在 Linux 上使用 `sendfile()` 或 `copy_file_range()` 系统调用, 实现内核态直接传输:

```
传统复制 (4 次拷贝, 4 次上下文切换):
  磁盘 → 内核缓冲区 → 用户空间 → Socket 缓冲区 → 网卡

零拷贝 sendfile (2 次拷贝, 2 次上下文切换):
  磁盘 → 内核缓冲区 ──────────────────────────→ 网卡
                     (DMA 直接传输, 不经过用户空间)
```

> **源码验证**: `FileChannelImpl.java` 第 791 行注释:
> "implementation uses sendfile, copy_file_range or equivalent"
> 第 799-800 行通过 pattern matching 分发:
> `case FileChannelImpl fci -> transferToFileChannel(...)` 和
> `case SocketChannelImpl sci -> transferToSocketChannel(...)`

```java
// 文件到文件零拷贝
try (FileChannel src = FileChannel.open(Path.of("input.bin"), READ);
     FileChannel dst = FileChannel.open(Path.of("output.bin"), CREATE, WRITE)) {

    long transferred = src.transferTo(0, src.size(), dst);
    // 或反方向:
    // dst.transferFrom(src, 0, src.size());
}

// 文件到 Socket 零拷贝 (最典型的 sendfile 场景)
try (FileChannel file = FileChannel.open(Path.of("video.mp4"), READ);
     SocketChannel socket = SocketChannel.open(
         new InetSocketAddress("client", 8080))) {

    long position = 0;
    long remaining = file.size();
    while (remaining > 0) {
        long sent = file.transferTo(position, remaining, socket);
        position += sent;
        remaining -= sent;
    }
}
```

### SocketChannel/ServerSocketChannel: 非阻塞 TCP

```java
// 非阻塞服务端
ServerSocketChannel server = ServerSocketChannel.open();
server.bind(new InetSocketAddress(8080));
server.configureBlocking(false);
SocketChannel client = server.accept();  // 立即返回, 无连接时返回 null

// 非阻塞客户端
SocketChannel socket = SocketChannel.open();
socket.configureBlocking(false);
boolean connected = socket.connect(new InetSocketAddress("server", 8080));
if (!connected) {
    // 注册 OP_CONNECT 到 Selector, 或轮询 finishConnect()
    while (!socket.finishConnect()) { /* ... */ }
}

// 非阻塞读写
ByteBuffer buf = ByteBuffer.allocate(4096);
int n = socket.read(buf);     // -1 (EOF), 0 (无数据), >0 (读到数据)
buf.flip();
int w = socket.write(buf);    // 可能 < buf.remaining() (缓冲区满)
```

### DatagramChannel: UDP

```java
DatagramChannel udp = DatagramChannel.open();
udp.bind(new InetSocketAddress(9999));
udp.configureBlocking(false);

ByteBuffer buf = ByteBuffer.allocate(1024);
SocketAddress sender = udp.receive(buf);   // 非阻塞, 无数据返回 null
if (sender != null) {
    buf.flip();
    // 处理后回复
    udp.send(ByteBuffer.wrap("ACK".getBytes()), sender);
}

// "已连接" 模式 — 限定收发地址, 可用 read()/write()
udp.connect(new InetSocketAddress("target", 9999));
udp.write(buf);   // 不需要指定地址
udp.read(buf);    // 只接收来自 target 的数据
```

### AsynchronousChannel (NIO.2 异步通道)

JDK 7 引入, 提供两种异步模式: `Future` 和 `CompletionHandler`:

```java
AsynchronousFileChannel afc = AsynchronousFileChannel.open(
    Path.of("data.bin"), StandardOpenOption.READ);
ByteBuffer buf = ByteBuffer.allocate(4096);

// 方式 1: Future
Future<Integer> future = afc.read(buf, 0);
int bytesRead = future.get();  // 阻塞等待完成

// 方式 2: CompletionHandler (回调)
afc.read(buf, 0, buf, new CompletionHandler<Integer, ByteBuffer>() {
    @Override
    public void completed(Integer result, ByteBuffer attachment) {
        attachment.flip();
        // 处理数据...
    }
    @Override
    public void failed(Throwable exc, ByteBuffer attachment) {
        exc.printStackTrace();
    }
});

// AsynchronousSocketChannel 类似, 支持超时:
// asc.read(buf, 30, TimeUnit.SECONDS, null, handler);
```

### Pipe: 线程间通信

```java
Pipe pipe = Pipe.open();
Pipe.SinkChannel sink = pipe.sink();        // 写端 (可注册到 Selector)
Pipe.SourceChannel source = pipe.source();  // 读端 (可注册到 Selector)

sink.write(ByteBuffer.wrap("message".getBytes()));

ByteBuffer buf = ByteBuffer.allocate(1024);
source.read(buf);
```

---

## 4. Selector 多路复用深入

### Selector 工作原理

```
  Selector.select()  ──── 调用 OS 多路复用 API ────►  就绪事件
       │
       ├── Channel A (OP_ACCEPT) ── 就绪 ──► selectedKeys
       ├── Channel B (OP_READ)   ── 就绪 ──► selectedKeys
       ├── Channel C (OP_WRITE)  ── 未就绪
       └── Channel D (OP_READ)   ── 就绪 ──► selectedKeys
                                              select() 返回 3
```

### SelectionKey 事件类型

源码中 `SelectionKey` 的四个常量 (位掩码):

| 常量 | 值 | 适用 Channel | 含义 |
|------|----|-------------|------|
| `OP_READ` | `1 << 0` = 1 | SocketChannel, DatagramChannel | 有数据可读 |
| `OP_WRITE` | `1 << 2` = 4 | SocketChannel, DatagramChannel | 可以写出数据 |
| `OP_CONNECT` | `1 << 3` = 8 | SocketChannel | 连接建立完成 |
| `OP_ACCEPT` | `1 << 4` = 16 | ServerSocketChannel | 有新连接到达 |

> **注意**: `OP_WRITE` 几乎总是就绪的 (只要 socket 发送缓冲区未满), 因此不要一开始就注册 `OP_WRITE`, 否则 `select()` 会立即返回造成忙轮询. 只在 `write()` 返回 0 (缓冲区满) 时才注册 `OP_WRITE`.

### 完整的 Selector 事件循环 (Echo Server)

```java
Selector selector = Selector.open();
ServerSocketChannel server = ServerSocketChannel.open();
server.bind(new InetSocketAddress(8080));
server.configureBlocking(false);
server.register(selector, SelectionKey.OP_ACCEPT);

while (true) {
    selector.select();  // 阻塞等待事件
    Iterator<SelectionKey> iter = selector.selectedKeys().iterator();
    while (iter.hasNext()) {
        SelectionKey key = iter.next();
        iter.remove();  // 必须手动移除!

        if (key.isAcceptable()) {
            SocketChannel client = ((ServerSocketChannel) key.channel()).accept();
            client.configureBlocking(false);
            client.register(selector, SelectionKey.OP_READ, ByteBuffer.allocate(4096));
        }
        if (key.isReadable()) {
            SocketChannel client = (SocketChannel) key.channel();
            ByteBuffer buf = (ByteBuffer) key.attachment();
            if (client.read(buf) == -1) { key.cancel(); client.close(); }
            else { buf.flip(); key.interestOps(SelectionKey.OP_WRITE); }
        }
        if (key.isWritable()) {
            SocketChannel client = (SocketChannel) key.channel();
            ByteBuffer buf = (ByteBuffer) key.attachment();
            client.write(buf);
            if (!buf.hasRemaining()) { buf.clear(); key.interestOps(SelectionKey.OP_READ); }
        }
    }
}
```

### 平台实现: epoll / kqueue / wepoll

Selector 的底层实现因操作系统不同而异. JDK 源码中有明确的平台分支:

```
Selector (abstract)                           java.nio.channels.Selector
    │
    └── SelectorImpl (abstract)               sun.nio.ch.SelectorImpl
            │
            ├── EPollSelectorImpl             sun.nio.ch.EPollSelectorImpl     (Linux)
            │       └── 使用 epoll_create / epoll_ctl / epoll_wait
            │
            ├── KQueueSelectorImpl            sun.nio.ch.KQueueSelectorImpl    (macOS)
            │       └── 使用 kqueue / kevent
            │
            ├── WEPollSelectorImpl            sun.nio.ch.WEPollSelectorImpl    (Windows)
            │       └── 使用 wepoll (基于 Windows IOCP 的 epoll 兼容层)
            │
            └── PollSelectorImpl              sun.nio.ch.PollSelectorImpl      (通用 Unix)
                    └── 使用 poll() (fallback)
```

> **源码验证**:
> - `linux/classes/sun/nio/ch/EPollSelectorImpl.java` 第 49 行: `class EPollSelectorImpl extends SelectorImpl`
> - `macosx/classes/sun/nio/ch/KQueueSelectorImpl.java` 第 48 行: `class KQueueSelectorImpl extends SelectorImpl`
> - `windows/classes/sun/nio/ch/WEPollSelectorImpl.java` 第 47 行: `class WEPollSelectorImpl extends SelectorImpl`

#### 各平台 I/O 多路复用对比

| 特性 | `poll()` | `epoll` (Linux) | `kqueue` (macOS/BSD) | `wepoll` (Windows) |
|------|----------|-----------------|----------------------|--------------------|
| **时间复杂度** | O(n) 每次扫描全部 fd | O(1) 事件就绪通知 | O(1) 事件就绪通知 | O(1) 基于 IOCP |
| **最大 fd 数** | 无硬限制 | 无硬限制 | 无硬限制 | 无硬限制 |
| **触发模式** | 水平触发 (LT) | LT + 边缘触发 (ET) | LT + ET | LT |
| **数据结构** | 线性数组 | 红黑树 + 就绪链表 | 内核事件队列 | 完成端口 |
| **JDK 使用** | fallback | 默认 Linux impl | 默认 macOS impl | JDK 17+ 替代旧 `WindowsSelectorImpl` |

### Reactor 模式

NIO Selector 是实现 Reactor 模式的基础. 以下是从单线程到多线程的演进:

```
┌──────────────────┬──────────────────────┬───────────────────────────┐
│  单线程 Reactor   │  多线程 Reactor       │  主从 Reactor (Netty)      │
├──────────────────┼──────────────────────┼───────────────────────────┤
│                  │                      │                           │
│  ┌────────────┐  │  ┌──────────┐        │  ┌─────────────┐          │
│  │  Reactor   │  │  │ Reactor  │        │  │ Main Reactor│ accept   │
│  │ accept+I/O │  │  │ accept   │        │  └──────┬──────┘          │
│  │ +compute   │  │  │ +I/O     │        │    ┌────┼────┐            │
│  └────────────┘  │  └────┬─────┘        │    ▼    ▼    ▼            │
│                  │       ▼              │  Sub  Sub  Sub  (I/O)     │
│ 适用: Redis 等   │  Worker 线程池        │       ▼                   │
│ 问题: 阻塞       │  (decode+compute)    │  Worker 线程池 (业务)      │
└──────────────────┴──────────────────────┴───────────────────────────┘
```

#### Netty 与 JDK NIO 的关系

| 层面 | JDK NIO | Netty |
|------|---------|-------|
| **Selector** | 原生 `Selector.open()` | 封装为 `NioEventLoop`, 修复了 epoll 空轮询 bug |
| **Buffer** | `ByteBuffer` (flip/compact 易出错) | `ByteBuf` (读写双指针, 引用计数, 池化) |
| **Channel** | `SocketChannel` | `NioSocketChannel` (增加 pipeline, 编解码) |
| **线程模型** | 需要自行实现 | `EventLoopGroup` (主从 Reactor 开箱即用) |
| **零拷贝** | `FileChannel.transferTo()` | `FileRegion` + `CompositeByteBuf` |

---

## 5. NIO.2 文件 API

### Path vs java.io.File: 为什么替代

| 缺陷 | `java.io.File` | `java.nio.file.Path` |
|------|----------------|---------------------|
| **错误处理** | 返回 `boolean` (失败无原因) | 抛异常 (含详细原因) |
| **符号链接** | 不支持 | 完整支持 |
| **文件属性** | 只有基本属性 | POSIX, DOS, ACL 等 |
| **文件系统** | 只支持本地 | 可扩展 (ZIP, 内存, 远程) |
| **原子操作** | 不支持 | 原子移动, 原子创建 |
| **监控** | 不支持 | WatchService |
| **遍历** | 只有 `list()` 返回 `String[]` | Stream-based `walk()`, `find()`, `list()` |

### Path 操作

```java
Path path = Path.of("/etc", "hosts");                 // JDK 11+ (推荐, 而非 Paths.get())

path.getRoot();        // "/"               path.getParent();    // "/etc"
path.getFileName();    // "hosts"           path.toAbsolutePath();

path.resolve("backup");                 // /etc/hosts/backup
path.resolveSibling("hostname");        // /etc/hostname
path.relativize(Path.of("/etc/ssl"));   // "../ssl"
path.normalize();                       // 去掉 "." 和 ".."
path.toRealPath();                      // 解析符号链接
path.toFile();  /* ↔ */  file.toPath(); // 互转
```

### Files 工具类

```java
// ─── 读写 (JDK 11+ 简化 API) ───
String text = Files.readString(Path.of("config.txt"));
Files.writeString(Path.of("output.txt"), "content",
    StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING);

// ─── 读写 (字节/行) ───
byte[] bytes = Files.readAllBytes(Path.of("binary.dat"));
List<String> lines = Files.readAllLines(Path.of("data.csv"));
Files.write(Path.of("out.dat"), bytes);
Files.write(Path.of("log.txt"), lines, StandardOpenOption.APPEND);

// ─── 流式读取 (大文件, 惰性) ───
try (Stream<String> lines = Files.lines(Path.of("huge.log"))) {
    long errorCount = lines.filter(l -> l.contains("ERROR")).count();
}

// ─── 复制/移动/删除 ───
Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);
Files.copy(inputStream, target);                     // InputStream → 文件
Files.copy(source, outputStream);                    // 文件 → OutputStream
Files.move(source, target,
    StandardCopyOption.ATOMIC_MOVE);                  // 原子移动
Files.delete(path);                                   // 不存在则抛异常
Files.deleteIfExists(path);                           // 不存在不报错

// ─── 创建 ───
Files.createFile(path);
Files.createDirectories(Path.of("a/b/c/d"));         // 递归创建
Files.createTempFile("prefix", ".tmp");
Files.createSymbolicLink(link, target);

// ─── 属性查询 ───
Files.exists(path);  Files.isDirectory(path);  Files.isRegularFile(path);
Files.isSymbolicLink(path);  Files.size(path);
Files.getLastModifiedTime(path);
```

### 文件遍历: walk / find / walkFileTree

```java
// ─── walk(): 返回 Stream<Path> (深度优先) ───
try (Stream<Path> paths = Files.walk(Path.of("/var/log"), 3)) {  // 最大深度 3
    List<Path> javaFiles = paths
        .filter(p -> p.toString().endsWith(".log"))
        .toList();
}

// ─── find(): walk + 内置过滤 ───
try (Stream<Path> found = Files.find(Path.of("/src"), 10,
        (path, attrs) -> attrs.isRegularFile()
                      && path.toString().endsWith(".java")
                      && attrs.size() > 1024)) {
    found.forEach(System.out::println);
}

// ─── walkFileTree(): 更精细控制 (FileVisitor 模式) ───
// 示例: 递归删除目录
Files.walkFileTree(Path.of("build"), new SimpleFileVisitor<>() {
    @Override
    public FileVisitResult visitFile(Path file, BasicFileAttributes attrs)
            throws IOException {
        Files.delete(file);
        return FileVisitResult.CONTINUE;
    }

    @Override
    public FileVisitResult postVisitDirectory(Path dir, IOException exc)
            throws IOException {
        Files.delete(dir);
        return FileVisitResult.CONTINUE;
    }
});
```

### WatchService: 文件系统事件监控

```java
WatchService watcher = FileSystems.getDefault().newWatchService();

Path dir = Path.of("/var/log");
WatchKey key = dir.register(watcher,
    StandardWatchEventKinds.ENTRY_CREATE,
    StandardWatchEventKinds.ENTRY_DELETE,
    StandardWatchEventKinds.ENTRY_MODIFY);

while (true) {
    WatchKey k = watcher.take();             // 阻塞等待事件
    // 或: watcher.poll(5, TimeUnit.SECONDS)  // 超时等待

    for (WatchEvent<?> event : k.pollEvents()) {
        WatchEvent.Kind<?> kind = event.kind();

        if (kind == StandardWatchEventKinds.OVERFLOW) {
            continue;  // 事件丢失 (系统过载)
        }

        Path changed = (Path) event.context();       // 相对路径
        Path fullPath = dir.resolve(changed);         // 完整路径

        System.out.printf("%s: %s%n", kind.name(), fullPath);
    }

    boolean valid = k.reset();  // 必须 reset, 否则不再接收事件
    if (!valid) break;          // 目录被删除或不可访问
}
```

> **实现细节**: Linux 使用 `inotify`, macOS 使用 `kqueue` + `FSEvents`, 某些系统可能退化为 `PollingWatchService` (轮询).

### FileAttribute 与 POSIX 权限

```java
// 创建文件时指定权限
Set<PosixFilePermission> perms = PosixFilePermissions.fromString("rwxr-x---");
Files.createFile(Path.of("script.sh"),
    PosixFilePermissions.asFileAttribute(perms));

// 读取/修改权限
Set<PosixFilePermission> current = Files.getPosixFilePermissions(path);
current.add(PosixFilePermission.OTHERS_READ);
Files.setPosixFilePermissions(path, current);

// 读取详细属性
BasicFileAttributes basic = Files.readAttributes(path, BasicFileAttributes.class);
// basic.creationTime(), lastModifiedTime(), size(), isSymbolicLink()

PosixFileAttributes posix = Files.readAttributes(path, PosixFileAttributes.class);
// posix.owner(), group(), permissions()
```

---

## 6. 虚拟线程与 NIO

### 虚拟线程使 Selector 不再必要

| 方案 | 代码风格 | 性能 | 复杂度 |
|------|---------|------|--------|
| A. BIO (一连接一线程) | 同步简单 | 差 (线程数=连接数) | 低 |
| B. NIO Selector | 事件驱动 | 好 | 高 (状态机, 回调) |
| C. NIO.2 异步 | 回调/Future | 好 | 高 (回调嵌套) |
| **D. 虚拟线程 (JDK 21)** | **同步简单** | **好** | **低** |

方案 D = 方案 A 的简洁性 + 方案 B 的性能.

```java
// JDK 21+: 用虚拟线程替代 Selector
try (var server = ServerSocketChannel.open()) {
    server.bind(new InetSocketAddress(8080));
    // 注意: 保持阻塞模式 (blocking = true)

    while (true) {
        SocketChannel client = server.accept();  // 阻塞 accept — 虚拟线程自动 unmount

        Thread.startVirtualThread(() -> {
            try (client) {
                ByteBuffer buf = ByteBuffer.allocate(4096);
                while (client.read(buf) > 0) {   // 阻塞 read — 虚拟线程自动 unmount
                    buf.flip();
                    client.write(buf);            // 阻塞 write — 虚拟线程自动 unmount
                    buf.clear();
                }
            } catch (IOException e) {
                // handle error
            }
        });
    }
}
```

### NIO Channel 在虚拟线程上的行为

当虚拟线程执行阻塞 I/O 时, JDK 内部的 `Poller` 机制自动介入:

```
虚拟线程执行 channel.read(buf):
  1. 系统调用 read() 返回 EAGAIN (无数据)
  2. 虚拟线程 unmount (释放载体线程 / carrier thread)
  3. fd 注册到 Poller (内部 epoll/kqueue)
  4. 当数据到达, Poller 检测到 fd 就绪
  5. 虚拟线程 unpark, 重新 mount 到某个载体线程
  6. 继续执行 read()
```

> **源码验证**: `Poller.java` 第 50 行:
> "I/O poller to allow virtual threads park until a file descriptor is ready for I/O."
> 第 78-81 行: "Read and write pollers are virtual threads that poll for events, yielding between polls and unparking virtual threads when file descriptors are ready for I/O."

### 何时仍然需要 NIO

虚拟线程并不让 NIO 完全过时. 以下场景仍需直接使用 NIO:

| 场景 | 原因 |
|------|------|
| **内存映射文件** (`MappedByteBuffer`) | 虚拟线程无法替代 `mmap()` 的零拷贝文件访问 |
| **零拷贝传输** (`transferTo/transferFrom`) | 内核态直接传输, 不经过用户空间 |
| **Scatter/Gather I/O** | 多 Buffer 向量化读写 |
| **文件锁** (`FileLock`) | 进程间文件协调 |
| **精细超时控制** | `Selector.select(timeout)` 提供精确超时 |
| **UDP 多播** (`MulticastChannel`) | 虚拟线程不改变 UDP 编程模型 |
| **已有 Netty/Mina 代码** | 不值得重写 |

---

## 7. MemorySegment 与 ByteBuffer

### JDK 22+ Foreign Function & Memory API (JEP 454)

`MemorySegment` 是 `ByteBuffer` 的现代替代方案, 解决了 `ByteBuffer` 的几个根本限制:

| 限制 | ByteBuffer | MemorySegment |
|------|------------|---------------|
| **最大容量** | `int` → 2 GB | `long` → 理论无限制 |
| **生命周期** | GC + Cleaner (不确定) | `Arena` 确定性释放 |
| **安全性** | 关闭后仍可能访问 (dangling) | 关闭后访问抛异常 |
| **类型灵活性** | 只有固定的 7 种 Buffer | 任意布局 (struct, array, ...) |
| **与 native 互操作** | JNI + `GetDirectBufferAddress` | 原生支持, 无需 JNI |

```java
import java.lang.foreign.*;

// ─── 分配堆外内存 ───
try (Arena arena = Arena.ofConfined()) {
    // 分配 1MB (确定性释放, 无需 Cleaner)
    MemorySegment segment = arena.allocate(1024 * 1024);

    // 类型化访问 (无需 flip/clear/compact)
    segment.set(ValueLayout.JAVA_INT, 0, 42);
    segment.set(ValueLayout.JAVA_LONG, 4, 100L);

    int value = segment.get(ValueLayout.JAVA_INT, 0);    // 42
    long lval = segment.get(ValueLayout.JAVA_LONG, 4);   // 100

    // 批量操作
    MemorySegment.copy(segment, 0, segment, 1024, 512);

    // 转为 ByteBuffer (互操作)
    ByteBuffer buf = segment.asByteBuffer();
}
// arena 关闭, 内存立即释放

// ─── 内存映射文件 (替代 MappedByteBuffer) ───
try (Arena arena = Arena.ofConfined();
     FileChannel channel = FileChannel.open(Path.of("data.bin"), READ, WRITE)) {

    MemorySegment mapped = channel.map(
        FileChannel.MapMode.READ_WRITE, 0, channel.size(), arena);

    // 大文件 (> 2GB) 也可以完整映射
    mapped.set(ValueLayout.JAVA_INT, 3_000_000_000L, 42);  // offset > 2GB
}
```

### 何时用 ByteBuffer vs MemorySegment

| 场景 | 推荐 | 原因 |
|------|------|------|
| NIO Channel `read()`/`write()` | `ByteBuffer` | Channel API 要求 ByteBuffer |
| Off-heap 大内存 (> 2GB) | `MemorySegment` | ByteBuffer 有 2GB 限制 |
| 与 native 库交互 (FFM) | `MemorySegment` | 原生支持, 无需 JNI |
| 确定性释放需求 | `MemorySegment` + `Arena` | 避免 Cleaner 的延迟 |
| 现有代码 / Netty | `ByteBuffer` | 兼容性 |

---

## 8. 性能最佳实践

### Direct Buffer 池化

Direct Buffer 分配慢 (`malloc` 系统调用), 但 I/O 快 (零拷贝). 高频场景应池化复用:

```java
public class BufferPool {
    private final Queue<ByteBuffer> pool = new ConcurrentLinkedQueue<>();
    private final int bufferSize;

    public BufferPool(int bufferSize, int count) {
        this.bufferSize = bufferSize;
        for (int i = 0; i < count; i++)
            pool.offer(ByteBuffer.allocateDirect(bufferSize));
    }

    public ByteBuffer acquire() {
        ByteBuffer buf = pool.poll();
        return (buf != null) ? (ByteBuffer) buf.clear() : ByteBuffer.allocateDirect(bufferSize);
    }

    public void release(ByteBuffer buf) {
        if (buf.isDirect() && buf.capacity() == bufferSize) { buf.clear(); pool.offer(buf); }
    }
}
```

### 零拷贝总结

| 技术 | JDK API | OS 机制 | 适用场景 |
|------|---------|---------|----------|
| `FileChannel.transferTo()` | `channel.transferTo(pos, count, dest)` | `sendfile()` / `copy_file_range()` | 文件→Socket, 文件→文件 |
| `MappedByteBuffer` | `channel.map(mode, pos, size)` | `mmap()` | 大文件随机读写 |
| Direct Buffer | `ByteBuffer.allocateDirect()` | 堆外内存 | 避免 JNI 边界拷贝 |
| Scatter/Gather | `channel.read(ByteBuffer[])` | `readv()` / `writev()` | 向量化 I/O |

### Buffer 大小选择

```
推荐 Buffer 大小:

  网络 I/O:
    ├── 小消息 (协议头): 128 - 512 bytes
    ├── 通用: 4 KB - 8 KB (一个内存页)
    └── 大数据传输: 64 KB - 256 KB

  文件 I/O:
    ├── 顺序读写: 8 KB - 64 KB
    ├── 大文件: 使用 MappedByteBuffer (mmap)
    └── transferTo: 无需 Buffer

  原则:
    ├── Buffer 太小 → 系统调用次数多
    ├── Buffer 太大 → 内存浪费, cache 不友好
    └── Direct Buffer: 4 KB 的倍数 (对齐内存页)
```

### 常见陷阱

```java
// ❌ 错误 1: 忘记 flip()
ByteBuffer buf = ByteBuffer.allocate(1024);
buf.put("Hello".getBytes());
channel.write(buf);          // 写入 0 字节! position=5, limit=1024, 写的是空区域
// ✅ 正确:
buf.flip();                  // position=0, limit=5
channel.write(buf);

// ❌ 错误 2: 不移除 selectedKeys
for (SelectionKey key : selector.selectedKeys()) {
    // 处理...
}
// 下次 select() 时, 旧的 key 仍在 selectedKeys 中!
// ✅ 正确: 使用 iterator 并 remove()

// ❌ 错误 3: 频繁分配 Direct Buffer
while (true) {
    ByteBuffer buf = ByteBuffer.allocateDirect(8192);  // 每次都 malloc!
    channel.read(buf);
}
// ✅ 正确: 复用或池化

// ❌ 错误 4: 一开始就注册 OP_WRITE
channel.register(selector, OP_READ | OP_WRITE);  // OP_WRITE 几乎总就绪 → 忙轮询
// ✅ 正确: 只在 write() 返回 0 时才注册 OP_WRITE

// ❌ 错误 5: MappedByteBuffer 不 force()
MappedByteBuffer mapped = channel.map(READ_WRITE, 0, size);
mapped.putInt(0, 42);
// 进程崩溃时数据可能丢失!
// ✅ 正确:
mapped.force();  // 刷盘
```

---

## 9. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### NIO/NIO.2 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Alan Bateman | 40+ | Oracle | NIO 架构师, JSR 51 / JSR 203 规范负责人, Virtual Thread I/O 集成 |
| 2 | Brian Burkhalter | 15+ | Oracle | FileChannel, Files 工具类增强 |
| 3 | Henry Jen | 8+ | Oracle | NIO.2 增强 |
| 4 | Paul Sandoz | 5+ | Oracle | Buffer, I/O 增强 |

### 历史贡献者

| 贡献者 | 机构 | 主要贡献 |
|--------|------|----------|
| **Mark Reinhold** | Oracle | NIO 初始设计, ByteOrder 作者 (`@author` 标注) |
| **Doug Lea** | SUNY Oswego | Reactor 模式论文, NIO 并发设计影响 |
| **Alan Bateman** | Oracle | NIO/NIO.2/Loom I/O 全栈, 持续维护至今 |

---

## 10. 相关链接

### 内部文档

- [I/O 处理](../api/io/) - 传统 java.io
- [网络编程](../net/) - Socket, HTTP Client
- [并发编程](../concurrency/) - 虚拟线程, 线程池

### 外部资源

- [JSR 51: New I/O APIs for the Java Platform](https://jcp.org/en/jsr/detail?id=51)
- [JSR 203: More New I/O APIs for the Java Platform](https://jcp.org/en/jsr/detail?id=203)
- [JEP 353: Reimplement the Legacy Socket API](https://openjdk.org/jeps/353)
- [JEP 380: Unix-Domain Socket Channels](https://openjdk.org/jeps/380)
- [JEP 444: Virtual Threads](https://openjdk.org/jeps/444)
- [JEP 454: Foreign Function & Memory API](https://openjdk.org/jeps/454)
- [Doug Lea - Scalable IO in Java (Reactor 论文)](http://gee.cs.oswego.edu/dl/cpjslides/nio.pdf)

---

**最后更新**: 2026-03-22
