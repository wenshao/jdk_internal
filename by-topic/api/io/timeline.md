# I/O 演进时间线

Java I/O 从 JDK 1.0 到 JDK 26 的完整演进历程。

---

## 时间线概览

```
JDK 1.0 ──── JDK 1.4 ──── JDK 5 ──── JDK 7 ──── JDK 11 ──── JDK 21 ──── JDK 26
 │             │             │            │           │            │            │
File/         NIO          Scanner     NIO.2      Files       Foreign      Memory
Stream        (New I/O)    Formatter   (JSR 203)  API         Access      Segment
              Channels/A                                 Access
              synchronous
             Selectors
```

---

## I/O 体系结构

```
┌─────────────────────────────────────────────────────────┐
│                    Java I/O 体系                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │              Bio (Blocking I/O)              │        │
│  │  InputStream/OutputStream                    │        │
│  │  Reader/Writer                               │        │
│  │  File                                       │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │              NIO (New I/O)                   │        │
│  │  Buffer (ByteBuffer, CharBuffer...)         │        │
│  │  Channel (FileChannel, SocketChannel...)    │        │
│  │  Selector                                   │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │              NIO.2 (JSR 203)                 │        │
│  │  Path/Paths                                 │        │
│  │  Files                                      │        │
│  │  FileSystem                                 │        │
│  │  AsynchronousFileChannel                    │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │         Foreign Memory Access (JDK 22+)     │        │
│  │  MemorySegment                              │        │
│  │  Arena                                      │        │
│  │  ValueLayout                                │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## JDK 1.0 - 传统 I/O

### InputStream/OutputStream

```java
// 字节流
try (InputStream is = new FileInputStream("input.txt");
     OutputStream os = new FileOutputStream("output.txt")) {

    byte[] buffer = new byte[1024];
    int bytesRead;
    while ((bytesRead = is.read(buffer)) != -1) {
        os.write(buffer, 0, bytesRead);
    }
}
```

### Reader/Writer

```java
// 字符流
try (Reader reader = new FileReader("input.txt");
     Writer writer = new FileWriter("output.txt")) {

    char[] buffer = new char[1024];
    int charsRead;
    while ((charsRead = reader.read(buffer)) != -1) {
        writer.write(buffer, 0, charsRead);
    }
}
```

### 过滤流

```java
// Buffered - 缓冲流
try (BufferedReader br = new BufferedReader(new FileReader("input.txt"));
     BufferedWriter bw = new BufferedWriter(new FileWriter("output.txt"))) {

    String line;
    while ((line = br.readLine()) != null) {
        bw.write(line);
        bw.newLine();
    }
}

// DataStream - 数据流
try (DataOutputStream dos = new DataOutputStream(
        new FileOutputStream("data.dat"))) {
    dos.writeInt(123);
    dos.writeDouble(3.14);
    dos.writeUTF("Hello");
}

try (DataInputStream dis = new DataInputStream(
        new FileInputStream("data.dat"))) {
    int i = dis.readInt();
    double d = dis.readDouble();
    String s = dis.readUTF();
}
```

---

## JDK 1.4 - NIO (New I/O)

### Buffer

```java
// ByteBuffer - 字节缓冲区
ByteBuffer buffer = ByteBuffer.allocate(1024);

// 写入数据
buffer.putInt(123);
buffer.putDouble(3.14);
buffer.put((byte) 1);

// 准备读取
buffer.flip();  // limit = position, position = 0

// 读取数据
int i = buffer.getInt();
double d = buffer.getDouble();
byte b = buffer.get();

// 清空缓冲区
buffer.clear();  // position = 0, limit = capacity

// Direct Buffer (堆外内存)
ByteBuffer directBuffer = ByteBuffer.allocateDirect(1024);
```

### Buffer 类型

| 类型 | 说明 | 大小 |
|------|------|------|
| ByteBuffer | 字节缓冲区 | 8-bit |
| CharBuffer | 字符缓冲区 | 16-bit |
| ShortBuffer | 短整型缓冲区 | 16-bit |
| IntBuffer | 整型缓冲区 | 32-bit |
| LongBuffer | 长整型缓冲区 | 64-bit |
| FloatBuffer | 浮点缓冲区 | 32-bit |
| DoubleBuffer | 双精度缓冲区 | 64-bit |

### Channel

```java
// FileChannel - 文件通道
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

// 文件复制
try (FileChannel src = FileChannel.open(Paths.get("src.txt"));
     FileChannel dest = FileChannel.open(Paths.get("dest.txt"),
         StandardOpenOption.CREATE, StandardOpenOption.WRITE)) {

    dest.transferFrom(src, 0, src.size());
}

// 内存映射
try (FileChannel channel = FileChannel.open(
        Paths.get("large.dat"),
        StandardOpenOption.READ, StandardOpenOption.WRITE)) {

    MappedByteBuffer mapped = channel.map(
        FileChannel.MapMode.READ_WRITE, 0, channel.size());

    // 直接操作内存
    mapped.putInt(0, 123);
}
```

### Selector

```java
// Selector - 多路复用选择器
Selector selector = Selector.open();

ServerSocketChannel serverChannel = ServerSocketChannel.open();
serverChannel.bind(new InetSocketAddress(8080));
serverChannel.configureBlocking(false);

serverChannel.register(selector, SelectionKey.OP_ACCEPT);

while (true) {
    selector.select();  // 阻塞直到有事件

    Set<SelectionKey> selectedKeys = selector.selectedKeys();
    Iterator<SelectionKey> iter = selectedKeys.iterator();

    while (iter.hasNext()) {
        SelectionKey key = iter.next();

        if (key.isAcceptable()) {
            // 接受连接
            SocketChannel client = serverChannel.accept();
            client.configureBlocking(false);
            client.register(selector, SelectionKey.OP_READ);
        }

        if (key.isReadable()) {
            // 读取数据
            SocketChannel client = (SocketChannel) key.channel();
            ByteBuffer buffer = ByteBuffer.allocate(1024);
            client.read(buffer);
        }

        iter.remove();
    }
}
```

---

## JDK 5 - Scanner 和 Formatter

### Scanner

```java
// Scanner - 解析输入
Scanner scanner = new Scanner(System.in);

// 读取各种类型
String line = scanner.nextLine();
int i = scanner.nextInt();
double d = scanner.nextDouble();
boolean b = scanner.nextBoolean();

// 从文件读取
Scanner fileScanner = new Scanner(new File("data.txt"));
while (fileScanner.hasNext()) {
    String token = fileScanner.next();
}

// 使用正则表达式
Scanner regexScanner = new Scanner("a1,b2,c3");
regexScanner.useDelimiter(",");
while (regexScanner.hasNext()) {
    System.out.println(regexScanner.next());
}
```

### Formatter

```java
// Formatter - 格式化输出
Formatter formatter = new Formatter("output.txt");

// 格式化输出
formatter.format("Hello %s%n", "World");
formatter.format("Pi = %.2f%n", Math.PI);
formatter.format("Date: %tF%n", new Date());

// System.out.printf (内部使用 Formatter)
System.out.printf("Name: %s, Age: %d%n", "Alice", 25);

// String.format
String result = String.format("x = %d, y = %d", 10, 20);
```

---

## JDK 7 - NIO.2 (JSR 203)

### Path 和 Paths

```java
// Path - 文件路径 (替代 File)
Path path = Paths.get("/home/user/documents/file.txt");

// 路径操作
Path parent = path.getParent();
Path fileName = path.getFileName();
Path root = path.getRoot();
boolean absolute = path.isAbsolute();

// 路径组合
Path base = Paths.get("/home/user");
Path resolved = base.resolve("documents/file.txt");

// 路径规范化
Path normalized = Paths.get("/a/b/../c/./d").normalize();

// 路径转换
Path absolutePath = path.toAbsolutePath();
Path realPath = path.toRealPath();

// Path 转 File (遗留代码兼容)
File file = path.toFile();
```

### Files 工具类

```java
Path path = Paths.get("test.txt");

// 文件检查
boolean exists = Files.exists(path);
boolean notExists = Files.notExists(path);
boolean isDirectory = Files.isDirectory(path);
boolean isRegularFile = Files.isRegularFile(path);
boolean isReadable = Files.isReadable(path);
boolean isWritable = Files.isWritable(path);
boolean isExecutable = Files.isExecutable(path);

// 文件属性
long size = Files.size(path);
BasicFileAttributes attrs = Files.readAttributes(
    path, BasicFileAttributes.class);
FileTime lastModified = attrs.lastModifiedTime();
boolean isDirectory = attrs.isDirectory();

// 文件操作
Files.createFile(path);
Files.createDirectory(path);
Files.createDirectories(path);
Files.delete(path);
Files.deleteIfExists(path);

// 文件复制
Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);

// 文件移动
Files.move(source, target, StandardCopyOption.REPLACE_EXISTING);

// 读取/写入
List<String> lines = Files.readAllLines(path);
String content = Files.readString(path);
byte[] bytes = Files.readAllBytes(path);

Files.writeString(path, "Hello");
Files.write(path, bytes);
```

### DirectoryStream

```java
// DirectoryStream - 目录遍历
try (DirectoryStream<Path> stream = Files.newDirectoryStream(
        Paths.get("/home/user"))) {
    for (Path entry : stream) {
        System.out.println(entry.getFileName());
    }
}

// 使用 glob 过滤
try (DirectoryStream<Path> stream = Files.newDirectoryStream(
        Paths.get("/home/user"), "*.txt")) {
    for (Path entry : stream) {
        System.out.println(entry.getFileName());
    }
}
```

### WatchService

```java
// WatchService - 文件监控
WatchService watchService = FileSystems.getDefault().newWatchService();

Path dir = Paths.get("/home/user");
dir.register(watchService,
    StandardWatchEventKinds.ENTRY_CREATE,
    StandardWatchEventKinds.ENTRY_DELETE,
    StandardWatchEventKinds.ENTRY_MODIFY);

while (true) {
    WatchKey key = watchService.take();
    for (WatchEvent<?> event : key.pollEvents()) {
        WatchEvent.Kind<?> kind = event.kind();
        Path fileName = (Path) event.context();
        System.out.println(kind + ": " + fileName);
    }
    key.reset();
}
```

### AsynchronousFileChannel

```java
// AsynchronousFileChannel - 异步文件 I/O
try (AsynchronousFileChannel channel = AsynchronousFileChannel.open(
        Paths.get("input.txt"),
        StandardOpenOption.READ)) {

    ByteBuffer buffer = ByteBuffer.allocate(1024);
    Future<Integer> operation = channel.read(buffer, 0);

    while (!operation.isDone()) {
        // 做其他事情
    }

    int bytesRead = operation.get();
    buffer.flip();
}
```

---

## JDK 11 - Files 改进

### 新增方法

```java
// Files.readString - 读取整个文件为字符串
String content = Files.readString(Path.of("input.txt"));

// Files.writeString - 写入字符串
Files.writeString(Path.of("output.txt"), "Hello, World!");

// 指定字符集
Files.writeString(Path.of("output.txt"), "Hello",
    StandardCharsets.UTF_8);

// 简化的文件创建
Path path = Files.createString(Path.of("test.txt"), "content");
```

---

## JDK 21+ - Foreign Memory Access

### MemorySegment

```java
// Foreign Memory Access (JEP 454)
import jdk.incubator.foreign.*;

// 创建内存段
try (Arena arena = Arena.ofConfined()) {
    // 分配原生内存
    MemorySegment segment = arena.allocate(100);

    // 写入数据
    segment.set(ValueLayout.JAVA_INT, 0, 42);
    segment.set(ValueLayout.JAVA_DOUBLE, 8, 3.14);

    // 读取数据
    int i = segment.get(ValueLayout.JAVA_INT, 0);
    double d = segment.get(ValueLayout.JAVA_DOUBLE, 8);
}
```

### ValueLayout

```java
// ValueLayout - 定义数据布局
ValueLayout.OfInt intLayout = ValueLayout.JAVA_INT;
ValueLayout.OfDouble doubleLayout = ValueLayout.JAVA_DOUBLE;

// 结构体布局
struct Point {
    int x;
    int y;
}

MemoryLayout pointLayout = MemoryLayout.structLayout(
    ValueLayout.JAVA_INT.withName("x"),
    ValueLayout.JAVA_INT.withName("y")
);
```

### Arena

```java
// Arena - 管理内存段生命周期
// 1. Confined Arena - 单线程
try (Arena arena = Arena.ofConfined()) {
    MemorySegment segment = arena.allocate(1024);
}

// 2. Shared Arena - 多线程
try (Arena arena = Arena.ofShared()) {
    MemorySegment segment = arena.allocate(1024);
}

// 3. Automatic Arena - 自动清理 (JDK 22+)
Arena arena = Arena.ofAuto();
MemorySegment segment = arena.allocate(1024);
// GC 自动清理
```

---

## I/O 选择指南

### 场景选择

| 场景 | 推荐 API | 说明 |
|------|----------|------|
| 简单文件读写 | Files | 最简洁 |
| 大文件处理 | Stream/FileChannel | 流式处理 |
| 高性能网络 | NIO Selector | 多路复用 |
| 内存文件映射 | FileChannel.map | 零拷贝 |
| 异步 I/O | AsynchronousFileChannel | 非阻塞 |
| 原生内存操作 | Foreign Memory Access | 堆外内存 |

### 性能对比

| 操作 | BIO | NIO | NIO.2 | Foreign Memory |
|------|-----|-----|-------|----------------|
| 小文件读写 | 中 | 低 | 高 | - |
| 大文件读写 | 低 | 高 | 高 | 高 |
| 网络并发 | 低 | 高 | 高 | - |
| 内存访问 | 中 | 中 | 中 | 最高 |

---

## 最佳实践

### 使用 try-with-resources

```java
// ✅ 推荐: 自动关闭资源
try (InputStream is = new FileInputStream("input.txt")) {
    // 使用
}

// ❌ 避免: 手动关闭
InputStream is = new FileInputStream("input.txt");
try {
    // 使用
} finally {
    is.close();  // 可能抛异常
}
```

### 使用 Buffer

```java
// ✅ 推荐: 使用缓冲流
try (BufferedReader br = new BufferedReader(new FileReader("input.txt"))) {
    br.lines().forEach(System.out::println);
}

// ❌ 避免: 逐字节读取
try (FileInputStream fis = new FileInputStream("input.txt")) {
    int b;
    while ((b = fis.read()) != -1) {
        // 每次只读一个字节
    }
}
```

### 使用 NIO.2

```java
// ✅ 推荐: 使用 Path 和 Files
Path path = Path.of("input.txt");
List<String> lines = Files.readAllLines(path);

// ❌ 避免: 使用 File
File file = new File("input.txt");
try (BufferedReader br = new BufferedReader(new FileReader(file))) {
    // ...
}
```

---

## 时间线总结

| 版本 | 特性 | 说明 |
|------|------|------|
| JDK 1.0 | InputStream/OutputStream | 传统 I/O |
| JDK 1.0 | Reader/Writer | 字符流 |
| JDK 1.4 | NIO | Buffer, Channel, Selector |
| JDK 5 | Scanner/Formatter | 解析和格式化 |
| JDK 7 | NIO.2 | Path, Files, WatchService |
| JDK 11 | Files.readString/writeString | 简化文件操作 |
| JDK 22 | Foreign Memory Access | 原生内存访问 |

---

## 相关链接

- [I/O Streams](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/io/package-summary.html)
- [NIO](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/package-summary.html)
- [NIO.2](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/file/package-summary.html)
- [JEP 454: Foreign Memory Access](https://openjdk.org/jeps/454)
