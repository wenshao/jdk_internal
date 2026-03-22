# IO 与 NIO

> File、Stream、Channel、Buffer 演进历程

[← 返回 API 框架](../)

---

## 1. 快速概览

```
JDK 1.0 ── JDK 1.1 ── JDK 1.4 ── JDK 7 ── JDK 11 ── JDK 21 ── JDK 22 ── JDK 25 ── JDK 26
   │         │         │        │        │        │        │        │        │
File     Reader/   NIO     NIO.2   Files   虚拟    Foreign  File行为  HTTP/3
Stream   Writer    Buffer  Path    增强    线程    Memory   对齐NIO  (JEP 517)
         (字符)    Channel Watch   readFile 支持   (JEP 454) java.io
                  Selector Service (Lazy)
```

### 核心演进

| 版本 | 特性 | 说明 | JSR |
|------|------|------|-----|
| **JDK 1.0** | Stream IO | InputStream/OutputStream | - |
| **JDK 1.0** | File API | java.io.File | - |
| **JDK 1.1** | Reader/Writer | 字符流 | - |
| **JDK 1.4** | NIO | Buffer, Channel, Selector | JSR 51 |
| **JDK 7** | NIO.2 | Path, Files, WatchService | JSR 203 |
| **JDK 11** | Files 增强 | readString, writeString | - |
| **JDK 21** | 虚拟线程 | 阻塞 IO 不阻塞平台线程 | JEP 444 |
| **JDK 22** | Foreign Memory | Foreign Function & Memory API 正式 | JEP 454 |
| **JDK 25** | File 行为对齐 | java.io.File 行为与 java.nio.file 对齐 | - |
| **JDK 25** | HTTP/3 | HTTP Client API 支持 HTTP/3 协议 | JEP 517 |

---

## 2. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### IO/NIO 团队 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Alan Bateman | 43 | Oracle | NIO, NIO.2 (JSR 51, JSR 203) |
| 2 | Chris Hegarty | 17 | Oracle | 网络基础 |
| 3 | [Brian Goetz](/by-contributor/profiles/brian-goetz.md) | 12 | Oracle | API 设计 |
| 4 | Henry Jen | 10 | Oracle | NIO.2 增强 |
| 5 | Paul Sandoz | 8 | Oracle | IO 增强 |
| 6 | Xueming Shen | 7 | Oracle | 字符编码 |

---

## 3. I/O 演进 (Evolution of Java I/O)

Java I/O 经历了四个主要阶段，每一阶段解决前一阶段的核心痛点 (pain point)。

### 3.1 第一阶段: java.io (JDK 1.0-1.1)

```
JDK 1.0                          JDK 1.1
┌──────────────────────┐        ┌──────────────────────┐
│  InputStream          │        │  Reader (字符输入)     │
│  OutputStream         │        │  Writer (字符输出)     │
│  File                 │        │  InputStreamReader    │
│  RandomAccessFile     │        │  OutputStreamWriter   │
│                       │        │  BufferedReader       │
│  字节流 (byte stream) │        │  字符流 (char stream) │
└──────────────────────┘        └──────────────────────┘
```

**痛点:**
- **阻塞模型 (blocking model)**: 每次 `read()`/`write()` 调用阻塞当前线程
- **一连接一线程 (thread-per-connection)**: 高并发场景线程数爆炸
- **File API 缺陷**: `File.delete()` 失败只返回 `false`，无异常信息
- **无文件属性 (file attributes)**: 无法获取创建时间、POSIX 权限等

### 3.2 第二阶段: java.nio (JDK 1.4, JSR 51)

```
┌─────────────────────────────────────────────────┐
│                    NIO 三大核心                    │
├─────────────────────────────────────────────────┤
│  Buffer (缓冲区)     面向块 (block-oriented)      │
│  Channel (通道)      双向、可配置阻塞/非阻塞        │
│  Selector (选择器)   单线程管理多 Channel           │
└─────────────────────────────────────────────────┘
```

**解决的问题:**
- 非阻塞 I/O (non-blocking I/O) 支持高并发网络
- 直接内存 (direct memory) 减少数据拷贝
- 内存映射文件 (memory-mapped files) 处理大文件
- Scatter/Gather I/O 支持多缓冲区读写

### 3.3 第三阶段: NIO.2 / AIO (JDK 7, JSR 203)

```
┌─────────────────────────────────────────────────┐
│                    NIO.2 新增                     │
├─────────────────────────────────────────────────┤
│  Path          取代 java.io.File                 │
│  Files         丰富的静态工具方法                  │
│  WatchService  文件系统监控                       │
│  FileVisitor   目录树遍历                         │
│  AIO           AsynchronousFileChannel           │
│                AsynchronousSocketChannel          │
└─────────────────────────────────────────────────┘
```

**异步 I/O (Asynchronous I/O):**

```java
// JDK 7: AsynchronousFileChannel
AsynchronousFileChannel asyncChannel = AsynchronousFileChannel.open(
    Path.of("large.dat"), StandardOpenOption.READ);

ByteBuffer buffer = ByteBuffer.allocate(1024);

// 回调方式 (CompletionHandler)
asyncChannel.read(buffer, 0, buffer,
    new CompletionHandler<Integer, ByteBuffer>() {
        @Override
        public void completed(Integer bytesRead, ByteBuffer buf) {
            buf.flip();
            // 处理数据...
        }
        @Override
        public void failed(Throwable exc, ByteBuffer buf) {
            exc.printStackTrace();
        }
    });

// Future 方式
Future<Integer> future = asyncChannel.read(buffer, 0);
int bytesRead = future.get();  // 阻塞等待完成
```

### 3.4 第四阶段: 虚拟线程 I/O (JDK 21+, JEP 444)

```
┌─────────────────────────────────────────────────────────┐
│                虚拟线程改变 I/O 编程模型                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  JDK 1.0-20:                                            │
│    阻塞 IO → 消耗平台线程 → 必须用 NIO/AIO 应对高并发      │
│                                                         │
│  JDK 21+:                                               │
│    阻塞 IO → 虚拟线程自动 unmount → 不消耗平台线程          │
│    → 简单的同步代码即可实现高并发                            │
│                                                         │
│  结论: 异步 I/O (AIO) 的必要性大幅降低                     │
└─────────────────────────────────────────────────────────┘
```

### 各阶段对比

| 维度 | java.io | java.nio | NIO.2/AIO | 虚拟线程+IO |
|------|---------|----------|-----------|-------------|
| **编程模型** | 同步阻塞 | 同步非阻塞 | 异步回调 | 同步阻塞(表象) |
| **线程消耗** | 1:1 | 1:N (Selector) | 回调 | 极低 |
| **代码复杂度** | 低 | 高 | 很高 | 低 |
| **适用场景** | 简单应用 | 高并发网络 | 大文件异步 | 通用 |
| **API 包** | java.io | java.nio | java.nio.file | java.lang |

---

## 4. Stream IO (JDK 1.0)

### InputStream/OutputStream

```java
import java.io.*;

// 字节流
try (InputStream is = new FileInputStream("input.txt");
     OutputStream os = new FileOutputStream("output.txt")) {

    byte[] buffer = new byte[1024];
    int len;
    while ((len = is.read(buffer)) != -1) {
        os.write(buffer, 0, len);
    }
}
```

### Reader/Writer (JDK 1.1)

```java
import java.io.*;

// 字符流
try (Reader reader = new FileReader("input.txt");
     Writer writer = new FileWriter("output.txt")) {

    char[] buffer = new char[1024];
    int len;
    while ((len = reader.read(buffer)) != -1) {
        writer.write(buffer, 0, len);
    }
}
```

### 缓冲流

```java
// 缓冲字节流
try (BufferedInputStream bis = new BufferedInputStream(
        new FileInputStream("input.txt"));
     BufferedOutputStream bos = new BufferedOutputStream(
        new FileOutputStream("output.txt"))) {
    // 自动缓冲
}

// 缓冲字符流
try (BufferedReader br = new BufferedReader(new FileReader("input.txt"));
     BufferedWriter bw = new BufferedWriter(new FileWriter("output.txt"))) {

    // 按行读取
    String line;
    while ((line = br.readLine()) != null) {
        bw.write(line);
        bw.newLine();
    }
}
```

### InputStream/OutputStream 现代用法 (Modern Usage)

JDK 9+ 为传统流 API 添加了多个便捷方法，使其在现代 Java 中仍然实用。

```java
// === transferTo (JDK 9) ===
// 将输入流全部内容传输到输出流，替代手动循环
try (InputStream in = new FileInputStream("source.dat");
     OutputStream out = new FileOutputStream("target.dat")) {
    long bytes = in.transferTo(out);  // 返回传输字节数
}

// 常见用法: 下载文件
try (InputStream in = url.openStream();
     OutputStream out = Files.newOutputStream(Path.of("download.bin"))) {
    in.transferTo(out);
}

// === readAllBytes (JDK 9) ===
// 读取全部内容为 byte[]
try (InputStream in = new FileInputStream("small.dat")) {
    byte[] data = in.readAllBytes();  // 注意: 文件不能太大
}

// === readNBytes (JDK 9/11) ===
// 精确读取 N 个字节 (不像 read() 可能读取更少)
try (InputStream in = new FileInputStream("data.bin")) {
    // JDK 9: 读取到数组
    byte[] header = new byte[16];
    int n = in.readNBytes(header, 0, 16);  // 尽力读满 16 字节

    // JDK 11: 简化版本
    byte[] chunk = in.readNBytes(1024);  // 返回最多 1024 字节
}

// === nullOutputStream (JDK 11) ===
// 丢弃所有写入数据 (类似 /dev/null)
OutputStream devNull = OutputStream.nullOutputStream();
someStream.transferTo(devNull);  // 消费但不保存

// === readAllBytes 与 String 配合 ===
// 从 ClassPath 资源读取文本
String text = new String(
    getClass().getResourceAsStream("/config.txt").readAllBytes(),
    StandardCharsets.UTF_8
);
```

**readAllBytes vs readNBytes 对比:**

| 方法 | 行为 | 适用场景 |
|------|------|----------|
| `readAllBytes()` | 读取到 EOF | 小文件、资源文件 |
| `readNBytes(n)` | 精确读 n 字节 | 协议解析、定长记录 |
| `read(byte[])` | 读取 0 到 len 字节 | 传统循环读取 |
| `transferTo(out)` | 全部传输到输出流 | 文件复制、流转发 |

---

## 5. NIO Buffer 详解 (JDK 1.4)

### Buffer 核心概念: position / limit / capacity

Buffer 内部维护三个指针 (pointer)，理解它们是掌握 NIO 的关键:

```
写模式 (write mode):
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│ H │ e │ l │ l │ o │   │   │   │   │   │
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
  0   1   2   3   4   5                 9
                      ↑                 ↑
                   position          capacity
                                    = limit

调用 flip() 后 → 读模式 (read mode):
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│ H │ e │ l │ l │ o │   │   │   │   │   │
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
  0   1   2   3   4   5                 9
  ↑                   ↑                 ↑
position           limit            capacity

读取 2 个字节后:
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│ H │ e │ l │ l │ o │   │   │   │   │   │
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
  0   1   2   3   4   5                 9
          ↑           ↑                 ↑
       position    limit            capacity

调用 compact() 后 → 写模式 (保留未读数据):
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│ l │ l │ o │   │   │   │   │   │   │   │
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
  0   1   2   3                         9
              ↑                         ↑
           position                  capacity
                                    = limit
```

### flip() vs clear() vs compact() vs rewind()

| 方法 | position | limit | 用途 |
|------|----------|-------|------|
| `flip()` | → 0 | → 旧 position | 写模式切读模式 |
| `clear()` | → 0 | → capacity | 丢弃所有数据，重新写 |
| `compact()` | → remaining | → capacity | 保留未读数据，继续写 |
| `rewind()` | → 0 | 不变 | 重读已有数据 |
| `mark()/reset()` | → mark 位置 | 不变 | 标记/回跳 |

### ByteBuffer: Direct (直接) vs Heap (堆内)

```java
// 堆内缓冲区 (Heap Buffer)
ByteBuffer heap = ByteBuffer.allocate(1024);
// - 底层是 byte[] 数组，位于 JVM 堆上
// - 分配快、GC 管理
// - I/O 操作时需要额外拷贝到本地内存

// 直接缓冲区 (Direct Buffer)
ByteBuffer direct = ByteBuffer.allocateDirect(1024);
// - 分配在 JVM 堆外的本地内存 (native memory)
// - 分配/释放成本高 (通过 malloc/free)
// - I/O 操作零拷贝 (zero-copy)，性能更好
// - 不受 GC 直接管理，通过 Cleaner 回收
```

**选择原则 (selection guideline):**

| 场景 | 推荐 | 原因 |
|------|------|------|
| 短生命周期、小数据 | Heap Buffer | 分配快，GC 友好 |
| 长期复用的 I/O 缓冲 | Direct Buffer | 避免反复拷贝 |
| 网络服务 (Netty 等) | Direct + 池化 | 性能最优 |
| 内存映射文件 | Direct (自动) | MappedByteBuffer 必然是 direct |

### ByteBuffer 基本操作

```java
import java.nio.*;

// 创建 Buffer
ByteBuffer buffer = ByteBuffer.allocate(1024);

// 写入模式
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

// Compact (保留未读数据)
buffer.compact();
```

### Buffer 类型与视图 (View Buffer)

```java
// 7 种 Buffer: ByteBuffer, CharBuffer, ShortBuffer,
//              IntBuffer, LongBuffer, FloatBuffer, DoubleBuffer
// ByteBuffer 是最常用的，其他可通过视图获取:
ByteBuffer raw = ByteBuffer.allocate(1024);
IntBuffer intView = raw.asIntBuffer();     // 每 4 字节视为一个 int
LongBuffer longView = raw.asLongBuffer();  // 每 8 字节视为一个 long
CharBuffer charView = raw.asCharBuffer();  // 每 2 字节视为一个 char
// 视图与原 Buffer 共享底层数据
```

---

## 6. NIO Channel 架构 (JDK 1.4)

### Channel 类型体系

```
Channel (接口)
 ├── FileChannel          ← 文件 I/O
 ├── SocketChannel        ← TCP 客户端
 ├── ServerSocketChannel  ← TCP 服务端
 └── DatagramChannel      ← UDP
```

### FileChannel

```java
import java.nio.channels.*;
import java.nio.*;

// FileChannel — 文件读写
try (FileChannel channel = FileChannel.open(
        Paths.get("input.txt"),
        StandardOpenOption.READ)) {

    ByteBuffer buffer = ByteBuffer.allocate(1024);
    while (channel.read(buffer) != -1) {
        buffer.flip();
        // 处理数据
        buffer.clear();
    }
}
```

### SocketChannel 与 ServerSocketChannel

```java
// ServerSocketChannel — 服务端
ServerSocketChannel server = ServerSocketChannel.open();
server.bind(new InetSocketAddress(8080));
server.configureBlocking(false);  // 非阻塞模式

// SocketChannel — 客户端连接
SocketChannel client = SocketChannel.open();
client.configureBlocking(false);
client.connect(new InetSocketAddress("localhost", 8080));

// 非阻塞: 需要检查连接是否完成
while (!client.finishConnect()) {
    // 等待连接完成...
}
```

### Selector (多路复用器)

单个线程通过 Selector 监控多个 Channel 的就绪事件 (readiness event):

```
    Thread
      │
      ▼
  ┌────────┐     OP_ACCEPT    ┌─────────────────────┐
  │Selector├────────────────►│ ServerSocketChannel   │
  │        │     OP_READ      ├─────────────────────┤
  │  单线程 ├────────────────►│ SocketChannel #1     │
  │  管理   │     OP_READ      ├─────────────────────┤
  │  多连接 ├────────────────►│ SocketChannel #2     │
  │        │     OP_WRITE     ├─────────────────────┤
  │        ├────────────────►│ SocketChannel #3     │
  └────────┘                 └─────────────────────┘
```

**SelectionKey 事件类型:**

| 常量 | 值 | 含义 | 适用 Channel |
|------|------|------|-------------|
| `OP_ACCEPT` | 16 | 可接受连接 | ServerSocketChannel |
| `OP_CONNECT` | 8 | 连接就绪 | SocketChannel |
| `OP_READ` | 1 | 可读 | SocketChannel |
| `OP_WRITE` | 4 | 可写 | SocketChannel |

```java
// Selector 典型使用模式
Selector selector = Selector.open();

ServerSocketChannel server = ServerSocketChannel.open();
server.bind(new InetSocketAddress(8080));
server.configureBlocking(false);
server.register(selector, SelectionKey.OP_ACCEPT);

while (true) {
    int ready = selector.select();  // 阻塞直到有事件
    if (ready == 0) continue;

    Set<SelectionKey> keys = selector.selectedKeys();
    Iterator<SelectionKey> it = keys.iterator();

    while (it.hasNext()) {
        SelectionKey key = it.next();
        it.remove();  // 必须手动移除

        if (key.isAcceptable()) {
            SocketChannel client = server.accept();
            client.configureBlocking(false);
            client.register(selector, SelectionKey.OP_READ);
        } else if (key.isReadable()) {
            SocketChannel client = (SocketChannel) key.channel();
            ByteBuffer buf = ByteBuffer.allocate(256);
            int n = client.read(buf);
            if (n == -1) { key.cancel(); client.close(); }
            else { buf.flip(); /* 处理数据 */ }
        }
    }
}
```

### Channel 间传输 (零拷贝)

```java
// 零拷贝传输 (zero-copy transfer)
try (FileChannel src = FileChannel.open(Paths.get("src.txt"),
        StandardOpenOption.READ);
     FileChannel dest = FileChannel.open(Paths.get("dest.txt"),
        StandardOpenOption.WRITE,
        StandardOpenOption.CREATE)) {

    // 直接传输，不经过用户空间 (user space)
    // 底层使用 sendfile() 系统调用 (Linux)
    src.transferTo(0, src.size(), dest);
}

// 大文件需要分段传输 (> 2GB)
long position = 0;
long remaining = src.size();
while (remaining > 0) {
    long transferred = src.transferTo(position, remaining, dest);
    position += transferred;
    remaining -= transferred;
}
```

---

## 7. 内存映射文件 (Memory-Mapped Files)

### FileChannel.map() 原理

内存映射将文件直接映射到进程的虚拟地址空间 (virtual address space)，
通过 `mmap()` 系统调用实现。读写映射区域等同于读写文件，由操作系统管理
页面缓存 (page cache) 和磁盘同步。

```java
// MappedByteBuffer — 内存映射文件
try (FileChannel channel = FileChannel.open(Paths.get("large.dat"),
        StandardOpenOption.READ,
        StandardOpenOption.WRITE)) {

    // 映射模式:
    // READ_ONLY   — 只读映射
    // READ_WRITE  — 读写映射，修改会写回文件
    // PRIVATE     — 写时复制 (copy-on-write)，修改不影响文件
    MappedByteBuffer mapped = channel.map(
        FileChannel.MapMode.READ_WRITE, 0, channel.size());

    // 直接访问内存 — 无需 read()/write() 系统调用
    mapped.putInt(0, 0xCAFEBABE);
    int magic = mapped.getInt(0);

    // 强制刷盘 (flush to disk)
    mapped.force();
}
```

### MappedByteBuffer 与 MemorySegment (Panama)

JDK 22 的 Foreign Memory API 提供了更安全的替代方案:

```java
import java.lang.foreign.*;
import java.nio.channels.FileChannel;

// JDK 22+: 使用 MemorySegment 映射文件
try (FileChannel channel = FileChannel.open(Path.of("data.bin"),
        StandardOpenOption.READ, StandardOpenOption.WRITE);
     Arena arena = Arena.ofConfined()) {

    // FileChannel.map() 返回 MemorySegment (新重载)
    MemorySegment segment = channel.map(
        FileChannel.MapMode.READ_WRITE, 0, channel.size(), arena);

    // 类型安全的访问 (type-safe access)
    segment.set(ValueLayout.JAVA_INT, 0, 42);
    int value = segment.get(ValueLayout.JAVA_INT, 0);

    // 优势 vs MappedByteBuffer:
    // - 不受 Integer.MAX_VALUE 大小限制
    // - 确定性释放 (Arena 关闭时 unmap)
    // - 更安全 — Arena 关闭后访问抛异常
}
```

**MappedByteBuffer vs MemorySegment 对比:**

| 维度 | MappedByteBuffer | MemorySegment (JDK 22+) |
|------|------------------|------------------------|
| 最大映射大小 | ~2 GB (int 索引) | 无限制 (long 索引) |
| 释放 (unmap) | 不确定 (靠 GC) | 确定性 (Arena.close()) |
| 越界访问 | undefined behavior | 抛 IllegalStateException |
| API 风格 | get/put | ValueLayout 类型安全 |

---

## 8. Path/Files API (NIO.2, JDK 7+)

### Path vs java.io.File

```java
// 旧: java.io.File (JDK 1.0)
File file = new File("/tmp/example.txt");
boolean ok = file.delete();        // 失败只返回 false，无原因
File parent = file.getParentFile(); // 可能返回 null

// 新: java.nio.file.Path (JDK 7+)
Path path = Path.of("/tmp/example.txt");     // JDK 11+
Path path2 = Paths.get("/tmp/example.txt");  // JDK 7+
Files.delete(path);                // 失败抛异常 (NoSuchFileException 等)
Path parent = path.getParent();    // 明确的路径操作
```

**File → Path 迁移理由:**

| 维度 | java.io.File | java.nio.file.Path |
|------|-------------|-------------------|
| 错误处理 | 返回 boolean | 抛有意义的异常 |
| 符号链接 | 不支持 | 完整支持 |
| 文件属性 | 有限 | 丰富 (POSIX, DOS, 自定义) |
| 文件系统 | 仅本地 | 可插拔 (zip, memory, 远程) |
| 原子操作 | 不支持 | 原子移动/替换 |
| 互操作 | - | `file.toPath()` / `path.toFile()` |

### Files 常用操作

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
Path copy = Files.copy(path, Paths.get("/tmp/copy.txt"),
    StandardCopyOption.REPLACE_EXISTING);

// 移动文件 (原子操作)
Files.move(path, Paths.get("/tmp/moved.txt"),
    StandardCopyOption.ATOMIC_MOVE);

// 删除文件
Files.deleteIfExists(path);
```

### Files.walk / readAllLines / writeString

```java
// === 目录遍历 ===
// walk(): 深度优先遍历目录树
Path dir = Paths.get("/tmp/test");
try (Stream<Path> stream = Files.walk(dir)) {
    stream.filter(Files::isRegularFile)
          .filter(p -> p.toString().endsWith(".java"))
          .forEach(System.out::println);
}

// walk() 指定深度
try (Stream<Path> stream = Files.walk(dir, 2)) {  // 最多 2 层
    stream.forEach(System.out::println);
}

// find(): 带属性的查找
try (Stream<Path> stream = Files.find(dir, 10,
        (path, attrs) -> attrs.isRegularFile()
            && attrs.size() > 1024
            && path.toString().endsWith(".txt"))) {
    stream.forEach(System.out::println);
}

// === 文件读写 ===
// readAllLines: 读取所有行 (JDK 7)
List<String> lines = Files.readAllLines(Path.of("data.csv"));

// lines(): 惰性按行读取 (JDK 8, 推荐大文件)
try (Stream<String> stream = Files.lines(Path.of("big.log"))) {
    long errorCount = stream
        .filter(line -> line.contains("ERROR"))
        .count();
}

// readString / writeString (JDK 11)
String text = Files.readString(Path.of("config.json"));
Files.writeString(Path.of("output.txt"), "Hello JDK 11",
    StandardOpenOption.CREATE,
    StandardOpenOption.TRUNCATE_EXISTING);

// 带字符集
String content = Files.readString(Path.of("gbk.txt"),
    Charset.forName("GBK"));
```

### WatchService (文件系统监控)

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

### 文件属性 (File Attributes)

```java
// 读取属性
Path path = Paths.get("file.txt");
BasicFileAttributes attrs = Files.readAttributes(path,
    BasicFileAttributes.class);

System.out.println("Size: " + attrs.size());
System.out.println("Created: " + attrs.creationTime());
System.out.println("Modified: " + attrs.lastModifiedTime());
System.out.println("Is Directory: " + attrs.isDirectory());

// POSIX 属性
PosixFileAttributes posixAttrs = Files.readAttributes(path,
    PosixFileAttributes.class);
System.out.println("Permissions: " + posixAttrs.permissions());
```

---

## 9. 虚拟线程与 I/O (Virtual Threads and I/O, JDK 21+)

### 同步 I/O 在虚拟线程上的表现

虚拟线程 (virtual thread) 的核心价值: **阻塞操作不消耗平台线程 (carrier thread)**。
当虚拟线程执行阻塞 I/O 时，JVM 自动将其从 carrier thread 上卸载 (unmount)，
carrier thread 可以运行其他虚拟线程。

```java
import java.util.concurrent.*;

// 传统方式: 10000 个连接需要 10000 个平台线程
// 虚拟线程: 10000 个连接只需要少量 carrier thread (通常 = CPU 核数)

try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 10_000; i++) {
        executor.submit(() -> {
            // 阻塞 I/O — 虚拟线程自动 unmount
            String content = Files.readString(Path.of("data.txt"));
            // 网络 I/O — 同样自动 unmount
            try (var socket = new Socket("example.com", 80)) {
                socket.getOutputStream().write("GET / HTTP/1.1\r\n\r\n".getBytes());
                byte[] response = socket.getInputStream().readAllBytes();
            }
            return content;
        });
    }
}
```

### 为什么异步 I/O 不再必要

```
JDK 1.4-20 时代的选择:
┌────────────────────────────────────────────────────┐
│  要高并发?                                          │
│    ├─ 方案 A: NIO + Selector (复杂，手动状态管理)    │
│    ├─ 方案 B: AIO + CompletionHandler (回调地狱)    │
│    └─ 方案 C: Netty 等框架 (封装复杂性)              │
└────────────────────────────────────────────────────┘

JDK 21+ 时代:
┌────────────────────────────────────────────────────┐
│  要高并发?                                          │
│    └─ 方案: 普通阻塞 I/O + 虚拟线程 (简单直接)       │
│                                                    │
│  Selector 仍然有价值的场景:                          │
│    - 需要精细控制网络协议的框架 (如 Netty)            │
│    - 非 Java 平台集成                               │
│    - 已有 NIO 代码库的维护                           │
└────────────────────────────────────────────────────┘
```

### I/O 操作的虚拟线程兼容性

| I/O 操作 | 虚拟线程行为 | 说明 |
|----------|-------------|------|
| `InputStream.read()` | 自动 unmount | JDK 21 优化 |
| `OutputStream.write()` | 自动 unmount | JDK 21 优化 |
| `Socket` 读写 | 自动 unmount | JDK 21 重构 |
| `Files.readString()` | 自动 unmount | 底层使用优化的 I/O |
| `FileChannel` 操作 | **pin carrier** | 文件锁等场景仍会 pin |
| `synchronized` 块内 I/O | **pin carrier** | 建议用 `ReentrantLock` 替代 |

**注意事项:**
- `FileChannel` 的部分操作（如 `lock()`）会 pin carrier thread
- `synchronized` 块中的 I/O 会 pin carrier thread（JDK 24 的 JEP 491 移除了此限制）
- 建议使用 `java.util.concurrent.locks.ReentrantLock` 替代 `synchronized`

---

## 10. Foreign Memory API (JDK 22+)

> Foreign Function & Memory API (JEP 454) 经过 8 轮孵化与预览后在 JDK 22 正式发布。
> 提供安全、高效的堆外内存访问，替代 `sun.misc.Unsafe` 和 JNI。

```java
import java.lang.foreign.*;
import java.lang.foreign.MemorySegment;

// 分配堆外内存
try (Arena arena = Arena.ofConfined()) {
    MemorySegment segment = arena.allocate(1024);
    segment.set(ValueLayout.JAVA_INT, 0, 42);
    int value = segment.get(ValueLayout.JAVA_INT, 0);
}
```

---

## 11. JDK 25-26 IO 增强

### java.io.File 行为对齐 (JDK 25)

JDK 25 修复了 `java.io.File` 对空路径名的长期行为不一致问题，使 `canRead()`、
`exists()`、`isDirectory()` 等方法的行为与 `java.nio.file` API 保持一致。

### HTTP/3 支持 (JDK 25, JEP 517)

JDK 26 为 HTTP Client API 添加 HTTP/3 协议支持。HTTP/3 基于 QUIC (UDP)
传输，提供更快的握手、消除队头阻塞等优势。

```java
// JDK 26: HTTP/3 客户端
var client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3)
    .build();

var request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com"))
    .build();

var response = client.send(request,
    HttpResponse.BodyHandlers.ofString());
```

---

## 12. 性能优化

### Buffer 池化 (Buffer Pooling)

```java
// 复用 Buffer — 避免反复分配 Direct Buffer
private static final ThreadLocal<ByteBuffer> BUFFER_POOL =
    ThreadLocal.withInitial(() -> ByteBuffer.allocateDirect(8192));

public void processData(FileChannel channel) throws IOException {
    ByteBuffer buffer = BUFFER_POOL.get();
    buffer.clear();
    while (channel.read(buffer) != -1) {
        buffer.flip();
        // 处理数据...
        buffer.clear();
    }
}
```

### 零拷贝 (Zero-Copy)

```java
// Channel 间直接传输
try (FileChannel src = FileChannel.open(Paths.get("src.txt"),
        StandardOpenOption.READ);
     FileChannel dest = FileChannel.open(Paths.get("dest.txt"),
        StandardOpenOption.WRITE,
        StandardOpenOption.CREATE)) {

    // 零拷贝传输
    src.transferTo(0, src.size(), dest);
}
```

---

## 13. 相关链接

### 本地文档

- [NIO 专题](/by-topic/nio/) - Buffer, Channel, Selector 详解
- [网络编程](../../concurrency/network/) - Socket Channel
- [序列化](../../concurrency/serialization/) - IO 序列化

### 外部参考

**JSR 文档:**
- [JSR 51: New I/O APIs](https://jcp.org/en/jsr/detail?id=51)
- [JSR 203: More New I/O APIs](https://jcp.org/en/jsr/detail?id=203)

**JEP 文档:**
- [JEP 444: Virtual Threads](https://openjdk.org/jeps/444)
- [JEP 454: Foreign Function & Memory API](https://openjdk.org/jeps/454)
- [JEP 491: Synchronize Virtual Threads without Pinning](https://openjdk.org/jeps/491)
- [JEP 517: HTTP/3 for the HTTP Client API](https://openjdk.org/jeps/517)

**技术文档:**
- [Java NIO Tutorial](https://docs.oracle.com/javase/tutorial/essential/io/)
- [File API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/file/package-summary.html)
