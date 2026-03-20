# IO 与 NIO

> File、Stream、Channel、Buffer、Foreign Memory 演进历程

[← 返回 API 框架](../)

---

## 快速概览

```
JDK 1.0 ── JDK 1.4 ── JDK 7 ── JDK 11 ── JDK 17 ── JDK 22 ── JDK 23
   │         │        │        │        │        │        │
File     NIO     NIO.2   增强   增强   Foreign  FFM
Stream   Channel Path   Files  Record Memory  (JEP
         Selector  Files Stream API  API    454)
```

### 核心演进

| 版本 | 特性 | JEP | 说明 |
|------|------|-----|------|
| **JDK 1.0** | Stream IO | - | InputStream/OutputStream |
| **JDK 1.0** | File API | - | java.io.File |
| **JDK 1.4** | NIO | JSR 51 | Buffer, Channel, Selector |
| **JDK 5** | Scanner/Formatter | - | 简化 IO |
| **JDK 7** | NIO.2 | JSR 203 | Path, Files, WatchService |
| **JDK 11** | Files.readString | - | 简化文件读写 |
| **JDK 17** | Record Stream | - | 文件记录流 |
| **JDK 22** | Foreign Memory | JEP 454 | 外部内存 API 正式 |
| **JDK 23** | FFM 增强 | - | 继续改进 |

---

## 目录

- [传统 IO](#传统-io)
- [NIO](#nio)
- [NIO.2](#nio2)
- [Foreign Memory API](#foreign-memory-api)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 传统 IO

### InputStream/OutputStream

```java
// 字节流
InputStream is = new FileInputStream("input.txt");
OutputStream os = new FileOutputStream("output.txt");

// 读写
int b;
while ((b = is.read()) != -1) {
    os.write(b);
}

// 缓冲区
byte[] buffer = new byte[1024];
int n;
while ((n = is.read(buffer)) != -1) {
    os.write(buffer, 0, n);
}

// 自动关闭 (JDK 7+)
try (InputStream is2 = new FileInputStream("input.txt")) {
    // 使用
}
```

### Reader/Writer

```java
// 字符流
Reader reader = new FileReader("input.txt");
Writer writer = new FileWriter("output.txt");

// 缓冲
BufferedReader br = new BufferedReader(reader);
BufferedWriter bw = new BufferedWriter(writer);

// 读取行
String line;
while ((line = br.readLine()) != null) {
    System.out.println(line);
}

// JDK 8+ Lines
br.lines().forEach(System.out::println);
```

### Scanner (JDK 5)

```java
// 简化输入
Scanner scanner = new Scanner(System.in);
String input = scanner.nextLine();
int number = scanner.nextInt();

// 文件扫描
Scanner fileScanner = new Scanner(new File("input.txt"));
while (fileScanner.hasNextLine()) {
    String line = fileScanner.nextLine();
}
```

---

## NIO

**JDK 1.4 引入 (JSR 51)**

### Buffer

```java
// ByteBuffer
ByteBuffer buffer = ByteBuffer.allocate(1024);

// 写入
buffer.putInt(123);
buffer.putChar('A');

// 读取
buffer.flip();  // 切换到读模式
int i = buffer.getInt();
char c = buffer.getChar();

// 直接缓冲区
ByteBuffer direct = ByteBuffer.allocateDirect(1024);
```

### Channel

```java
// FileChannel
try (FileChannel channel = FileChannel.open(
        Paths.get("input.txt"),
        StandardOpenOption.READ)) {

    ByteBuffer buffer = ByteBuffer.allocate(1024);
    int n = channel.read(buffer);

    buffer.flip();
    while (buffer.hasRemaining()) {
        System.out.print((char) buffer.get());
    }
}

// 文件复制
try (FileChannel src = FileChannel.open(Paths.get("src.txt"));
     FileChannel dest = FileChannel.open(Paths.get("dest.txt"),
         StandardOpenOption.CREATE, StandardOpenOption.WRITE)) {
    dest.transferFrom(src, 0, src.size());
}
```

### Selector

```java
// 多路复用
Selector selector = Selector.open();

ServerSocketChannel server = ServerSocketChannel.open();
server.bind(new InetSocketAddress(8080));
server.configureBlocking(false);
server.register(selector, SelectionKey.OP_ACCEPT);

while (true) {
    selector.select();
    Set<SelectionKey> keys = selector.selectedKeys();

    for (SelectionKey key : keys) {
        if (key.isAcceptable()) {
            // 接受连接
        }
        if (key.isReadable()) {
            // 读取数据
        }
    }
    keys.clear();
}
```

---

## NIO.2

**JDK 7 引入 (JSR 203)**

### Path

```java
// Path - 文件路径
Path path = Paths.get("dir", "subdir", "file.txt");

// 路径操作
Path parent = path.getParent();      // 父路径
Path fileName = path.getFileName();  // 文件名
Path root = path.getRoot();          // 根路径

// 路径解析
Path resolved = path.resolve("other.txt");
Path normalized = path.normalize();  // 规范化
Path absolute = path.toAbsolutePath(); // 绝对路径

// 比较路径
Path other = Paths.get("other.txt");
boolean starts = path.startsWith(other);
```

### Files

```java
// 文件操作
Path path = Paths.get("file.txt");

// 读写
String content = Files.readString(path);
Files.writeString(path, "Hello");

// 复制移动
Files.copy(path, Paths.get("copy.txt"));
Files.move(path, Paths.get("new.txt"), StandardCopyOption.REPLACE_EXISTING);

// 创建删除
Files.createFile(path);
Files.createDirectory(path);
Files.createDirectories(path);
Files.delete(path);

// 属性
boolean exists = Files.exists(path);
boolean isDirectory = Files.isDirectory(path);
long size = Files.size(path);
```

### WatchService

```java
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
        Path changed = (Path) event.context();
        System.out.println(changed + ": " + event.kind());
    }
    key.reset();
}
```

---

## Foreign Memory API

**JDK 22 正式 (JEP 454)**

### MemorySegment

```java
// 分配外部内存
try (MemorySession session = MemorySession.openConfined()) {
    // 分配内存
    MemorySegment segment = session.allocate(100);

    // 写入数据
    segment.set(ValueLayout.JAVA_INT, 0, 42);
    segment.set(ValueLayout.JAVA_LONG, 8, 123456789L);

    // 读取数据
    int intValue = segment.get(ValueLayout.JAVA_INT, 0);
    long longValue = segment.get(ValueLayout.JAVA_LONG, 8);

    // 字节数组
    byte[] bytes = "Hello".getBytes(StandardCharsets.UTF_8);
    MemorySegment fromArray = MemorySegment.ofArray(bytes);
}  // 自动释放内存
```

### MemorySession

```java
// 内存会话管理
// 1. Confined - 单线程
try (MemorySession session = MemorySession.openConfined()) {
    MemorySegment segment = session.allocate(1024);
    // ...
}

// 2. Shared - 多线程
try (MemorySession session = MemorySession.openShared()) {
    MemorySegment segment = session.allocate(1024);
    // ...
}

// 3. Global - 全局
MemorySegment global = MemorySegment.GlobalScope().allocate(1024);
```

### Slicing

```java
// 内存切片
MemorySegment segment = MemorySession.openConfined()
    .allocate(100);

// 切片
MemorySegment slice = segment.asSlice(10, 20);
// 从偏移 10 开始, 长度 20

// 只读视图
MemorySegment readOnly = segment.asReadOnly();
```

---

## Foreign Function Interface

**JDK 22 正式 (JEP 454)**

### Linker 和 SymbolLookup

```java
// 调用 C 函数
Linker linker = Linker.nativeLinker();

// 查找符号
SymbolLookup stdlib = linker.defaultLookup();

// strlen 函数描述符
FunctionDescriptor strlenDesc = FunctionDescriptor.of(
    ValueLayout.JAVA_LONG,
    ValueLayout.ADDRESS
);

// 创建 downcall handle
MethodHandle strlen = linker.downcallHandle(
    stdlib.find("strlen").orElseThrow(),
    strlenDesc
);

// 调用
try (MemorySession session = MemorySession.openConfined()) {
    MemorySegment str = session.allocateUtf8String("Hello");
    long len = (long) strlen.invokeExact(str);
    System.out.println("Length: " + len);
}
```

### Upcall

```java
// Java 回调 C
// 创建 upcall stub
FunctionDescriptor callbackDesc = FunctionDescriptor.of(
    ValueLayout.JAVA_INT,
    ValueLayout.JAVA_INT,
    ValueLayout.JAVA_INT
);

MethodHandle callback = MethodHandles.lookup()
    .findStatic(MyClass.class, "callback",
        MethodType.methodType(int.class, int.class, int.class));

MemorySession session = MemorySession.openConfined();
MemorySession.SessionStub upcallStub = session.upcallStub(
    callback,
    callbackDesc
);
```

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### IO/NIO (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Alan Bateman | 43 | Oracle | NIO, NIO.2 (JSR 51, JSR 203) |
| 2 | Chris Hegarty | 17 | Oracle | 网络基础 |
| 3 | Brian Goetz | 12 | Oracle | API 设计 |
| 4 | Henry Jen | 10 | Oracle | NIO.2 增强 |
| 5 | Paul Sandoz | 8 | Oracle | IO 增强 |

### Foreign Memory API

| 贡献者 | 公司 | 主要贡献 |
|--------|------|----------|
| **Maurizio Cimadamore** | Oracle | Panama/Foreign Memory (JEP 454) |
| **Vladimir Ivanov** | Oracle | JIT 优化、Foreign 接口 |

---

## Git 提交历史

> 基于 OpenJDK master 分支分析

### IO/NIO 改进 (2024-2026)

```bash
# 查看 IO 相关提交
cd /path/to/jdk
git log --oneline -- src/java.base/share/classes/java/io/
git log --oneline -- src/java.base/share/classes/java/nio/
git log --oneline -- src/java.base/share/classes/jdk/internal/foreign/
```

---

## 相关链接

### 内部文档

- [IO 时间线](timeline.md) - 详细的历史演进
- [核心 API](../)
- [网络编程](../../concurrency/network/)
- [HTTP 客户端](../../concurrency/http/)

### 外部资源

- [JSR 51: New I/O APIs](https://jcp.org/en/jsr/detail?id=51)
- [JSR 203: More New I/O APIs](https://jcp.org/en/jsr/detail?id=203)
- [JEP 454: Foreign Function & Memory API](https://openjdk.org/jeps/454)
- [Foreign Memory API Tutorial](https://openjdk.org/projects/panama/)
- [Accessing Native C Functions](https://bazlur.ca/2023/10/16/accessing-native-c-functions-from-java-using-openjdks-jep-454-foreign-function-memory-api/)

### Git 仓库

```bash
# 查看 IO 相关提交
git log --oneline -- src/java.base/share/classes/java/io/
git log --oneline -- src/java.base/share/classes/java/nio/
```

---

**最后更新**: 2026-03-20

**Sources**:
- [JEP 454: Foreign Function & Memory API](https://openjdk.org/jeps/454)
- [JSR 51: New I/O APIs](https://jcp.org/en/jsr/detail?id=51)
- [JSR 203: More New I/O APIs](https://jcp.org/en/jsr/detail?id=203)
- [JDK 22 Foreign Function & Memory API](https://www.infoq.com/news/2024/03/java22-released/)
- [JDK 22 FFM API Deep Dive](https://cyberjos.blog/java/se/jdk-22-jep-454-foreign-function-memory/)
