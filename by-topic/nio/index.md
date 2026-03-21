# NIO 新 I/O

> Buffer, Channel, Selector, NIO.2 演进历程

[← 返回主题索引](../)

---

## 1. 快速概览

```
JDK 1.0 ── JDK 1.4 ── JDK 7 ── JDK 11 ── JDK 21
   │         │        │        │        │
IO流     NIO     NIO.2   增强   虚拟线程
Stream   Channel  Path    Files  优化
File     Selector WatchService  List
```

### 核心演进

| 版本 | 特性 | JEP | 说明 |
|------|------|-----|------|
| **JDK 1.0** | Stream IO | - | InputStream/OutputStream |
| **JDK 1.4** | NIO | JSR 51 | Buffer, Channel, Selector |
| **JDK 7** | NIO.2 | JSR 203 | Path, Files, WatchService |
| **JDK 11** | 增强 | - | Files.readString/writeString |
| **JDK 21** | 虚拟线程 | - | 并发优化 |
| **JDK 22** | Foreign Memory | JEP 454 | 外部内存 API |

---

## 2. OpenJDK 项目

### [Project Panama](../core/panama/)

外部函数接口和外部内存器。

| 特性 | 版本 | JEP |
|------|------|-----|
| Foreign Memory Access API | JDK 22 | JEP 454 |
| Foreign Function Interface | JDK 22 | JEP 454 |

→ [Panama 时间线](../core/panama/timeline.md)

---

## 目录

- [NIO 核心](#nio-核心)
- [Buffer 详解](#buffer-详解)
- [Channel 详解](#channel-详解)
- [Selector 多路复用](#selector-多路复用)
- [NIO.2 文件 API](#nio2-文件-api)
- [最佳实践](#最佳实践)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 3. NIO 核心

### 三大组件

```
┌─────────────────────────────────────────────────┐
│                    NIO 架构                       │
├─────────────────────────────────────────────────┤
│                                                 │
│  Buffer    ←→    Channel    ←→    Selector     │
│  (数据)    ←→    (通道)      ←→    (多路复用)   │
│                                                 │
│  ByteBuffer      FileChannel                   │
│  CharBuffer      SocketChannel                  │
│  ShortBuffer     ServerSocketChannel            │
│  IntBuffer      DatagramChannel                 │
│  LongBuffer                                    │
│  DoubleBuffer                                   │
│                                                 │
└─────────────────────────────────────────────────┘
```

### IO vs NIO

| 特性 | IO | NIO |
|------|----|----|
| 模型 | 阻塞 | 非阻塞 |
| 方向 | 单向 | 双向 |
| 缓冲 | 无 | Buffer |
| 处理 | 字节流 | 块 |
| 用途 | 简单应用 | 高并发 |

---

## 4. Buffer 详解

### Buffer 层次

```
Buffer (抽象类)
    │
    ├── ByteBuffer    ← 最常用
    ├── CharBuffer
    ├── ShortBuffer
    ├── IntBuffer
    ├── LongBuffer
    ├── FloatBuffer
    └── DoubleBuffer
```

### ByteBuffer 使用

```java
import java.nio.*;

// 分配 Buffer
ByteBuffer buffer = ByteBuffer.allocate(1024);      // 堆内
ByteBuffer direct = ByteBuffer.allocateDirect(1024); // 堆外

// 写入
buffer.putInt(123);
buffer.putChar('A');
buffer.putDouble(3.14);

// 切换到读模式
buffer.flip();

// 读取
int i = buffer.getInt();
char c = buffer.getChar();
double d = buffer.getDouble();

System.out.println(i + ", " + c + ", " + d);  // 123, A, 3.14
```

### Buffer 核心属性

```java
ByteBuffer buffer = ByteBuffer.allocate(1024);

// 核心属性
int capacity = buffer.capacity();  // 容量 (固定)
int position = buffer.position();  // 位置 (当前读写位置)
int limit = buffer.limit();        // 限制 (读写边界)

// 操作
buffer.flip();   // limit = position, position = 0 (写→读)
buffer.clear();  // limit = capacity, position = 0 (重置)
buffer.rewind(); // position = 0, limit 不变 (重读)
buffer.compact(); // 压缩未读数据
```

### Buffer 视图

```java
ByteBuffer buffer = ByteBuffer.allocate(1024);

// 字节视图
ByteBuffer byteView = buffer.duplicate();

// 基本类型视图
IntBuffer intView = buffer.asIntBuffer();
LongBuffer longView = buffer.asLongBuffer();

// 直接操作
intView.put(100);
longView.put(1000L);
```

---

## 5. Channel 详解

### Channel 类型

```
Channel (接口)
    │
    ├── FileChannel       ← 文件
    ├── SocketChannel      ← TCP Socket
    ├── ServerSocketChannel ← TCP Server
    └── DatagramChannel   ← UDP
```

### FileChannel

```java
import java.nio.*;
import java.io.*;

// 读写文件
try (RandomAccessFile file = new RandomAccessFile("data.txt", "rw")) {
    FileChannel channel = file.getChannel();

    // 写入
    ByteBuffer buffer = ByteBuffer.allocate(1024);
    buffer.put("Hello, NIO!".getBytes());
    buffer.flip();
    channel.write(buffer);

    // 定位
    channel.position(0);

    // 读取
    buffer.clear();
    int bytesRead = channel.read(buffer);
    buffer.flip();
    System.out.println(new String(buffer.array(), 0, bytesRead));

    // 文件截断
    channel.truncate(100);

    // 强制写入磁盘
    channel.force(true);
}
```

### 文件复制

```java
// FileChannel 高效复制
try (FileChannel src = FileChannel.open(Path.of("input.txt"));
     FileChannel dest = FileChannel.open(Path.of("output.txt"),
         StandardOpenOption.CREATE, StandardOpenOption.WRITE)) {

    // 方式 1: transferFrom
    long transferred = src.transferTo(0, src.size(), dest);

    // 方式 2: 直接缓冲区
    long transferred = dest.transferFrom(src, 0, src.size());
}
```

### SocketChannel

```java
// NIO TCP Client
SocketChannel client = SocketChannel.open();
client.configureBlocking(false);
client.connect(new InetSocketAddress("localhost", 8080));

// 非阻塞连接
if (!client.finishConnect()) {
    // 注册到 Selector...
}

// 读写
ByteBuffer buffer = ByteBuffer.allocate(256);
buffer.put("Hello, Server!".getBytes());
buffer.flip();
while (buffer.hasRemaining()) {
    client.write(buffer);
}

buffer.clear();
int bytesRead = client.read(buffer);
```

### ServerSocketChannel

```java
// NIO TCP Server
ServerSocketChannel server = ServerSocketChannel.open();
server.bind(new InetSocketAddress(8080));
server.configureBlocking(false);

// 接受连接
SocketChannel client = server.accept();

// 读写
ByteBuffer buffer = ByteBuffer.allocate(256);
int bytesRead = client.read(buffer);
```

---

## 6. Selector 多路复用

### Selector 工作原理

```
                    ┌──────────────────┐
                    │    Selector      │
                    │  (多路复用器)      │
                    └────────┬─────────┘
                             │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
    │ Channel │    │ Channel │    │ Channel │
    │   (可读) │    │  (可写) │    │  (接受) │
    └─────────┘    └─────────┘    └─────────┘
```

### Selector 使用

```java
import java.nio.*;
import java.nio.channels.*;
import java.net.*;

// 创建 Selector
Selector selector = Selector.open();

// 配置 ServerSocketChannel
ServerSocketChannel server = ServerSocketChannel.open();
server.bind(new InetSocketAddress(8080));
server.configureBlocking(false);
server.register(selector, SelectionKey.OP_ACCEPT);

// 配置 SocketChannel
SocketChannel client = SocketChannel.open();
client.configureBlocking(false);
client.connect(new InetSocketAddress("localhost", 8080));
client.register(selector, SelectionKey.OP_CONNECT |
                         SelectionKey.OP_READ |
                         SelectionKey.OP_WRITE);

// 事件循环
while (true) {
    int readyCount = selector.select();  // 阻塞直到有事件
    if (readyCount == 0) continue;

    Set<SelectionKey> keys = selector.selectedKeys();

    for (SelectionKey key : keys) {
        if (key.isAcceptable()) {
            // 接受连接
            ServerSocketChannel server = (ServerSocketChannel) key.channel();
            SocketChannel client = server.accept();
            client.configureBlocking(false);
            client.register(selector, SelectionKey.OP_READ);
        }

        if (key.isConnectable()) {
            // 连接完成
            SocketChannel client = (SocketChannel) key.channel();
            try {
                client.finishConnect();
            } catch (IOException e) {
                key.cancel();
            }
        }

        if (key.isReadable()) {
            // 可读
            SocketChannel client = (SocketChannel) key.channel();
            ByteBuffer buffer = ByteBuffer.allocate(256);
            int bytesRead = client.read(buffer);

            if (bytesRead == -1) {
                key.cancel();
            } else {
                buffer.flip();
                // 处理数据...
            }
        }

        if (key.isWritable()) {
            // 可写
            SocketChannel client = (SocketChannel) key.channel();
            ByteBuffer buffer = (ByteBuffer) key.attachment();
            if (buffer != null) {
                client.write(buffer);
            }
        }
    }
    keys.clear();
}
```

### SelectionKey 附加数据

```java
// 附加数据到 SelectionKey
SelectionKey key = channel.register(selector, SelectionKey.OP_READ);
key.attach("Connection data");  // 附加对象

// 获取附加数据
Object data = key.attachment();
```

---

## 7. NIO.2 文件 API

**JDK 7 (JSR 203)**

### Path

```java
import java.nio.file.*;

// Path - 文件路径
Path path = Paths.get("dir", "subdir", "file.txt");

// 路径操作
Path parent = path.getParent();
Path fileName = path.getFileName();
Path root = path.getRoot();

Path resolved = path.resolve("other.txt");
Path normalized = path.normalize();
Path absolute = path.toAbsolutePath();
Path relative = path.relativize(Paths.get("base"));
```

### Files

```java
import java.nio.file.*;

// 文件操作
Path path = Paths.get("file.txt");

// 读写 (JDK 11+)
String content = Files.readString(path);
Files.writeString(path, "Hello");

// 复制/移动
Files.copy(path, Paths.get("copy.txt"));
Files.move(path, Paths.get("new.txt"), StandardCopyOption.REPLACE_EXISTING);

// 创建/删除
Files.createFile(path);
Files.createDirectory(path);
Files.createDirectories(path);
Files.delete(path);

// 属性
boolean exists = Files.exists(path);
boolean isDirectory = Files.isDirectory(path);
long size = Files.size(path);

// 权限
Set<PosixFilePermission> permissions = Files.getPosixFilePermissions(path);
permissions.add(PosixFilePermission.OWNER_WRITE);
Files.setPosixFilePermissions(path, permissions);
```

### WatchService

```java
import java.nio.file.*;

// 文件监控
WatchService watcher = FileSystems.getDefault().newWatchService();
Path dir = Paths.get(".");
dir.register(watcher,
    StandardWatchEventKinds.ENTRY_CREATE,
    StandardWatchEventKinds.ENTRY_DELETE,
    StandardWatchEventKinds.ENTRY_MODIFY);

while (true) {
    WatchKey key = watcher.take();
    for (WatchEvent<?> event : key.pollEvents()) {
        WatchEvent.Kind<?> kind = event.kind();
        Path changed = (Path) event.context();
        System.out.println(changed + ": " + kind);
    }
    key.reset();
}
```

### DirectoryStream

```java
// 遍历目录
Path dir = Paths.get(".");
try (DirectoryStream<Path> stream = Files.newDirectoryStream(dir)) {
    for (Path path : stream) {
        System.out.println(path);
    }
}

// 过滤
try (DirectoryStream<Path> stream = Files.newDirectoryStream(dir,
        "*.txt", "*.md")) {
    for (Path path : stream) {
        System.out.println(path);
    }
}
```

### FileVisitor

```java
// 遍历目录树
Files.walkFileTree(Paths.get("."), new SimpleFileVisitor<Path>() {
    @Override
    public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) {
        System.out.println(file);
        return FileVisitResult.CONTINUE;
    }

    @Override
    public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) {
        System.out.println("Entering: " + dir);
        return FileVisitResult.CONTINUE;
    }

    @Override
    public FileVisitResult visitFileFailed(Path file, IOException exc) {
        System.err.println("Failed: " + file);
        return FileVisitResult.CONTINUE;
    }
});

// 或使用 Stream
Files.walk(Paths.get("."))
    .filter(Files::isRegularFile)
    .forEach(System.out::println);
```

---

## 8. 最佳实践

### 直接缓冲 vs 堆内缓冲

```java
// 堆内缓冲 - 快速分配，适合小数据
ByteBuffer heap = ByteBuffer.allocate(1024);

// 直接缓冲 - 零拷贝，适合 I/O
ByteBuffer direct = ByteBuffer.allocateDirect(1024);
```

### 使用 MappedByteBuffer

```java
// 内存映射文件 (大文件处理)
try (FileChannel channel = FileChannel.open(Path.of("large.bin"),
        StandardOpenOption.READ, StandardOpenOption.WRITE)) {

    MappedByteBuffer mapped = channel.map(
        FileChannel.MapMode.READ_WRITE, 0, channel.size());

    // 直接访问
    mapped.put(0, (byte) 42);
    byte value = mapped.get(0);
}
```

### 性能优化

```java
// 1. 复用 Buffer
ByteBuffer buffer = ByteBuffer.allocateDirect(8192);

// 2. 批量操作
channel.write(new ByteBuffer[] {buffer1, buffer2, buffer3});

// 3. 使用 transferTo/transferFrom
long transferred = src.transferTo(0, src.size(), dest);

// 4. 调整 Buffer 大小
int optimalSize = 8192;  // 根据系统调整
```

---

## 9. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### NIO/NIO.2 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Alan Bateman | 40+ | Oracle | NIO, NIO.2 (JSR 51, JSR 203) |
| 2 | [Brian Goetz](/by-contributor/profiles/brian-goetz.md) | 10+ | Oracle | API 设计 |
| 3 | Henry Jen | 8+ | Oracle | NIO.2 增强 |
| 4 | Paul Sandoz | 5+ | Oracle | I/O 增强 |
| 5 | Xu Shen | 5+ | Oracle | HTTP/2 |

### 历史贡献者

| 贡献者 | 公司/机构 | 主要贡献 |
|--------|----------|----------|
| **Alan Bateman** | Oracle | NIO/NIO.2 规范负责人 |
| **Mark Reinhold** | Oracle | 早期设计 |

---

## 10. 相关链接

### 内部文档

- [NIO 时间线](timeline.md) - 详细的历史演进
- [I/O 处理](../api/io/) - 传统 I/O
- [网络编程](../net/) - Socket, HTTP Client
- [文件 I/O](../api/io/) - Files, Path

### 外部资源

- [JSR 51: New I/O APIs](https://jcp.org/en/jsr/detail?id=51)
- [JSR 203: More New I/O APIs](https://jcp.org/en/jsr/detail?id=203)
- [Java NIO Tutorial](https://docs.oracle.com/javase/tutorial/essential/io/)
- [Java NIO.2 APIs](https://docs.oracle.com/javase/8/docs/technotes/guides/io/nio2.html)

---

**最后更新**: 2026-03-20
