# IO 与 NIO

> File、Stream、Channel、Buffer 演进历程

[← 返回 API 框架](../)

---

## 1. 快速概览

```
JDK 1.0 ── JDK 1.1 ── JDK 1.4 ── JDK 7 ── JDK 11 ── JDK 21
   │         │         │        │        │        │
File     Reader/   NIO     NIO.2   Files   虚拟
Stream   Writer    Buffer  Path    增强    线程
         (字符)    Channel Watch   readFile 支持
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

## 3. Stream IO (JDK 1.0)

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

---

## 4. NIO Buffer (JDK 1.4)

### ByteBuffer

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

### Buffer 类型

```java
// ByteBuffer
ByteBuffer byteBuffer = ByteBuffer.allocate(1024);

// CharBuffer
CharBuffer charBuffer = CharBuffer.allocate(512);

// ShortBuffer
ShortBuffer shortBuffer = ShortBuffer.allocate(256);

// IntBuffer
IntBuffer intBuffer = IntBuffer.allocate(128);

// LongBuffer
LongBuffer longBuffer = LongBuffer.allocate(64);

// FloatBuffer
FloatBuffer floatBuffer = FloatBuffer.allocate(32);

// DoubleBuffer
DoubleBuffer doubleBuffer = DoubleBuffer.allocate(16);
```

### 直接 Buffer

```java
// 堆外内存
ByteBuffer direct = ByteBuffer.allocateDirect(1024);

// 优势:
// - 避免 JVM 堆与本地内存复制
// - 适合大文件、网络 I/O

// 劣势:
// - 分配/释放成本高
// - 不受 GC 直接管理
```

---

## 5. NIO Channel (JDK 1.4)

### FileChannel

```java
import java.nio.channels.*;
import java.nio.*;

// FileChannel
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

### Channel 间传输

```java
// 零拷贝传输
try (FileChannel src = FileChannel.open(Paths.get("src.txt"),
        StandardOpenOption.READ);
     FileChannel dest = FileChannel.open(Paths.get("dest.txt"),
        StandardOpenOption.WRITE,
        StandardOpenOption.CREATE)) {

    // 直接传输，不经过用户空间
    src.transferTo(0, src.size(), dest);
}
```

---

## 6. NIO.2 (JDK 7+)

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
Path copy = Files.copy(path, Paths.get("/tmp/copy.txt"),
    StandardCopyOption.REPLACE_EXISTING);

// 移动文件
Files.move(path, Paths.get("/tmp/moved.txt"),
    StandardCopyOption.REPLACE_EXISTING);

// 删除文件
Files.deleteIfExists(path);
```

### 目录操作

```java
// 创建目录
Path dir = Paths.get("/tmp/test");
Files.createDirectories(dir);

// 遍历目录
try (Stream<Path> stream = Files.walk(dir)) {
    stream.filter(Files::isRegularFile)
          .forEach(System.out::println);
}

// 查找文件
try (Stream<Path> stream = Files.find(dir, 10,
        (path, attrs) -> path.toString().endsWith(".txt"))) {
    stream.forEach(System.out::println);
}
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

### 文件属性

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

## 7. Files 增强 (JDK 11+)

### 便捷方法

```java
// 读文件
String content = Files.readString(Paths.get("file.txt"));
List<String> lines = Files.readAllLines(Paths.get("file.txt"));

// 写文件
Files.writeString(Paths.get("output.txt"), "Hello JDK 11");

// 带 Charset
String content = Files.readString(Paths.get("file.txt"),
    StandardCharsets.UTF_8);

// 写入并创建
Files.writeString(Paths.get("new.txt"), "content",
    StandardOpenOption.CREATE,
    StandardOpenOption.TRUNCATE_EXISTING);
```

---

## 8. 虚拟线程 IO (JDK 21+)

### 阻塞 IO 不阻塞平台线程

```java
import java.util.concurrent.*;

// 虚拟线程中的阻塞 IO
try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> {
        // 阻塞读操作不阻塞平台线程
        String content = Files.readString(Paths.get("large.txt"));
        System.out.println(content);
    });
}
```

---

## 9. 性能优化

### Buffer 池化

```java
// 复用 Buffer
private static final ByteBuffer REUSABLE_BUFFER =
    ByteBuffer.allocateDirect(8192);

public void processData() {
    REUSABLE_BUFFER.clear();
    // 使用 Buffer
    REUSABLE_BUFFER.flip();
    // 读取数据
}
```

### 零拷贝

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

### 内存映射

```java
// MappedByteBuffer
try (FileChannel channel = FileChannel.open(Paths.get("large.dat"),
        StandardOpenOption.READ,
        StandardOpenOption.WRITE)) {

    MappedByteBuffer mapped = channel.map(
        FileChannel.MapMode.READ_WRITE, 0, channel.size());

    // 直接访问内存
    mapped.put(0, (byte) 42);
    byte value = mapped.get(0);
}
```

---

## 10. 相关链接

### 本地文档

- [网络编程](../../concurrency/network/) - Socket Channel
- [序列化](../../concurrency/serialization/) - IO 序列化

### 外部参考

**JSR 文档:**
- [JSR 51: New I/O APIs](https://jcp.org/en/jsr/detail?id=51)
- [JSR 203: More New I/O APIs](https://jcp.org/en/jsr/detail?id=203)

**技术文档:**
- [Java NIO Tutorial](https://docs.oracle.com/javase/tutorial/essential/io/)
- [File API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/file/package-summary.html)
