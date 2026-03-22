# java.base 模块深度分析

> Java 平台的根基模块 (root module)。所有其他模块隐式 `requires java.base`，
> 它是唯一不能被用户代码替换、不能被 `--limit-modules` 排除的模块。

---

## 1. 模块定义 (Module Declaration)

**源文件**: `src/java.base/share/classes/module-info.java` (408 行)

### 1.1 无条件导出 (Unconditional Exports)

从实际 `module-info.java` 提取的完整公共 API 包列表：

```
java.io                          java.lang
java.lang.annotation             java.lang.classfile          (since 24)
java.lang.classfile.attribute    java.lang.classfile.constantpool
java.lang.classfile.instruction  java.lang.constant
java.lang.foreign                java.lang.invoke
java.lang.module                 java.lang.ref
java.lang.reflect                java.lang.runtime
java.math                        java.net
java.net.spi                     java.nio
java.nio.channels                java.nio.channels.spi
java.nio.charset                 java.nio.charset.spi
java.nio.file                    java.nio.file.attribute
java.nio.file.spi               java.security
java.security.cert               java.security.interfaces
java.security.spec               java.text
java.text.spi                    java.time
java.time.chrono                 java.time.format
java.time.temporal               java.time.zone
java.util                        java.util.concurrent
java.util.concurrent.atomic      java.util.concurrent.locks
java.util.function               java.util.jar
java.util.random                 java.util.regex
java.util.spi                    java.util.stream
java.util.zip                    javax.crypto
javax.crypto.interfaces          javax.crypto.spec
javax.net                        javax.net.ssl
javax.security.auth              javax.security.auth.callback
javax.security.auth.login        javax.security.auth.spi
javax.security.auth.x500         javax.security.cert
```

共计 **55 个**无条件导出的公共 API 包。

### 1.2 限定导出 (Qualified Exports)

java.base 通过 `exports ... to` 将大量内部包暴露给特定模块。主要类别：

| 内部包前缀 | 导出目标 (示例) | 用途 |
|-----------|----------------|------|
| `jdk.internal.access` | java.desktop, java.management, jdk.jfr 等 12 个 | 跨模块 SharedSecrets 访问 |
| `jdk.internal.misc` | java.desktop, jdk.compiler, jdk.unsupported 等 16 个 | Unsafe、CDS 支持 |
| `jdk.internal.vm` | java.management, jdk.jfr, jdk.internal.vm.ci | VM 运行时信息 |
| `jdk.internal.vm.annotation` | jdk.jfr, jdk.incubator.vector, jdk.unsupported | @Stable, @ForceInline 等 |
| `jdk.internal.module` | jdk.jlink, jdk.compiler, jdk.jfr | 模块系统内部 |
| `jdk.internal.reflect` | java.sql, jdk.dynalink, jdk.unsupported | 反射加速器 |
| `jdk.internal.foreign` | jdk.incubator.vector | FFM 内部实现 |
| `jdk.internal.javac` | java.compiler, jdk.compiler | 编译器合作接口 |
| `jdk.internal.loader` | java.instrument, java.logging, java.naming | 类加载器内部 |
| `jdk.internal.net.quic` | java.net.http | QUIC 协议内部支持 |
| `sun.nio.ch` | java.management, jdk.net, jdk.sctp | NIO Channel 实现 |
| `sun.security.*` | java.security.jgss, jdk.crypto.cryptoki 等 | 安全框架实现 |
| `sun.util.locale.provider` | java.desktop, jdk.localedata | 区域设置内部 |

### 1.3 服务声明 (Service Uses/Provides)

**消费的服务 (uses)** — 共 28 个，来自 module-info.java：

```java
// 公共 SPI
uses java.lang.System.LoggerFinder;
uses java.net.ContentHandlerFactory;
uses java.net.spi.InetAddressResolverProvider;
uses java.net.spi.URLStreamHandlerProvider;
uses java.nio.channels.spi.AsynchronousChannelProvider;
uses java.nio.channels.spi.SelectorProvider;
uses java.nio.charset.spi.CharsetProvider;
uses java.nio.file.spi.FileSystemProvider;
uses java.nio.file.spi.FileTypeDetector;
uses java.security.Provider;
uses java.text.spi.BreakIteratorProvider;
uses java.text.spi.CollatorProvider;
uses java.text.spi.DateFormatProvider;
uses java.text.spi.DateFormatSymbolsProvider;
uses java.text.spi.DecimalFormatSymbolsProvider;
uses java.text.spi.NumberFormatProvider;
uses java.time.chrono.AbstractChronology;
uses java.time.chrono.Chronology;
uses java.time.zone.ZoneRulesProvider;
uses java.util.spi.CalendarDataProvider;
uses java.util.spi.CalendarNameProvider;
uses java.util.spi.CurrencyNameProvider;
uses java.util.spi.LocaleNameProvider;
uses java.util.spi.ResourceBundleControlProvider;
uses java.util.spi.ResourceBundleProvider;
uses java.util.spi.TimeZoneNameProvider;
uses java.util.spi.ToolProvider;
uses javax.security.auth.spi.LoginModule;

// JDK 内部 SPI
uses jdk.internal.io.JdkConsoleProvider;
uses jdk.internal.logger.DefaultLoggerFinder;
uses sun.text.spi.JavaTimeDateTimePatternProvider;
uses sun.util.spi.CalendarProvider;
uses sun.util.locale.provider.LocaleDataMetaInfo;
uses sun.util.resources.LocaleData.LocaleDataResourceBundleProvider;
```

**提供的服务 (provides)** — 仅 1 个：

```java
provides java.nio.file.spi.FileSystemProvider with
    jdk.internal.jrtfs.JrtFileSystemProvider;  // jrt:/ 文件系统
```

---

## 2. 源码规模统计 (Source Statistics)

基于 `src/java.base/` 目录的实际文件计数：

### 2.1 总量

| 维度 | 数值 |
|------|------|
| 总 `.java` 文件数 | **3,307** |
| `module-info.java` 行数 | 408 |
| 平台目录 | share, unix, linux, windows, macosx, aix |

### 2.2 按包统计

| 包层级 | 文件数 | 说明 |
|--------|--------|------|
| `java.lang.*` (全部子包) | 460 | 语言核心 + classfile + foreign + invoke + reflect |
| `java.lang` (直接) | 135 | Object, String, Thread, Class, Math 等 |
| `java.lang.invoke` | 54 | MethodHandle, VarHandle, LambdaMetafactory |
| `java.lang.classfile.*` | 161 | Class-File API (since 24) |
| `java.lang.foreign` | 16 | Foreign Function & Memory API |
| `java.lang.reflect` | 36 | 反射体系 |
| `java.lang.ref` | 10 | Reference 体系 |
| `java.lang.constant` | 12 | 常量 API (Constable, ConstantDesc) |
| `java.lang.annotation` | 13 | 注解类型 |
| `java.lang.runtime` | 5 | 运行时引导方法 (SwitchBootstraps 等) |
| `java.util.*` (全部子包) | 370 | 集合 + 并发 + Stream + function |
| `java.util` (直接) | 129 | HashMap, ArrayList, Collections, Arrays 等 |
| `java.util.concurrent.*` | 97 | JUC 并发框架 |
| `java.util.stream` | 40 | Stream API + Gatherer |
| `java.util.function` | 44 | 函数式接口 |
| `java.util.random` | 3 | 随机数生成器 (since 17) |
| `java.io` | 94 | 传统 I/O |
| `java.nio.*` | 166 | NIO 体系 |
| `java.time.*` | 87 | Date/Time API |
| `java.net.*` | 82 | 网络 |
| `java.security.*` | 190 | 安全框架 |
| `java.math` | 8 | BigInteger, BigDecimal 等 |
| `java.text.*` | 45 | 格式化 / 解析 |
| `jdk.internal.*` | 561 | JDK 内部实现 |
| `sun.*` | 1,086 | 遗留内部实现 |

### 2.3 平台特定代码

| 平台目录 | 文件数 | 典型内容 |
|----------|--------|---------|
| `share/` | 大部分 | 跨平台公共代码 |
| `unix/` | 52 | POSIX 文件系统、信号处理 |
| `linux/` | 32 | epoll、cgroup、procfs |
| `windows/` | 70 | IOCP、注册表、WinNT 安全 |
| `macosx/` | 36 | kqueue、Keychain |
| `aix/` | 15 | AIX 特有 pollset |

---

## 3. 核心包深入分析

### 3.1 java.lang — 语言核心 (135 个直接文件)

#### Object (59 行源码，但定义了 JVM 的根)

```java
// src/java.base/share/classes/java/lang/Object.java
public class Object {
    @IntrinsicCandidate
    public Object() {}                              // JVM 内联分配

    @IntrinsicCandidate
    public final native Class<?> getClass();        // 获取运行时类型

    @IntrinsicCandidate
    public native int hashCode();                   // identity hash

    public boolean equals(Object obj) {             // 默认 == 比较
        return (this == obj);
    }

    @IntrinsicCandidate
    protected native Object clone()                 // 浅拷贝
        throws CloneNotSupportedException;

    public String toString() {                      // 类名@哈希
        return getClass().getName() + "@" +
            Integer.toHexString(hashCode());
    }

    @IntrinsicCandidate
    public final native void notify();              // 监视器通知
    @IntrinsicCandidate
    public final native void notifyAll();
    public final void wait() throws InterruptedException { ... }
}
```

关键点：标注 `@IntrinsicCandidate` 的方法由 JIT 编译器提供 intrinsic 实现，
不走常规 JNI 调用路径。

#### String (5,364 行) — Compact Strings (JEP 254)

```java
// src/java.base/share/classes/java/lang/String.java
public final class String
    implements Serializable, Comparable<String>, CharSequence,
               Constable, ConstantDesc {

    @Stable
    private final byte[] value;          // JDK 9+ : byte[] 替代 char[]

    private final byte coder;            // LATIN1 (0) 或 UTF16 (1)

    @Stable
    private int hash;                    // 缓存的 hashCode

    static final boolean COMPACT_STRINGS; // 编译期常量，默认 true
    static {
        COMPACT_STRINGS = true;          // VM 可通过 -XX:-CompactStrings 覆盖
    }
}
```

**Compact Strings 设计要点**：
- Latin1 字符串 (ASCII + ISO-8859-1) 使用 1 byte/char，内存节省 50%
- UTF16 字符串仍使用 2 bytes/char
- `coder` 字段在每次操作前检查，JIT 会将 `COMPACT_STRINGS` 常量折叠
- 所有字符串操作委托到 `StringLatin1` 或 `StringUTF16` helper 类
- 编码选择模式：

```java
// 典型的内部分发模式
if (COMPACT_STRINGS && coder == LATIN1) {
    return StringLatin1.indexOf(value, ch, fromIndex, length);
} else {
    return StringUTF16.indexOf(value, ch, fromIndex, length);
}
```

#### Thread (2,000+ 行) 与 VirtualThread (1,445 行)

```java
// src/java.base/share/classes/java/lang/Thread.java
public class Thread implements Runnable {
    private volatile String name;
    private volatile long eetop;                   // JVM 内部线程指针
    private volatile ClassLoader contextClassLoader;

    ThreadLocal.ThreadLocalMap threadLocals;
    ThreadLocal.ThreadLocalMap inheritableThreadLocals;

    // JDK 21+: Builder API
    public static Builder.OfPlatform ofPlatform() { ... }
    public static Builder.OfVirtual ofVirtual() { ... }

    // 便捷方法
    public static Thread startVirtualThread(Runnable task) { ... }
}
```

```java
// src/java.base/share/classes/java/lang/VirtualThread.java
final class VirtualThread extends BaseVirtualThread {
    // 不是 public API — 通过 Thread.ofVirtual() 创建
    // 在 ForkJoinPool 的载体线程 (carrier thread) 上调度
    // 状态机: NEW -> STARTED -> RUNNING -> PARKING -> PARKED -> ...
    // 遇到阻塞操作时自动 yield (unmount from carrier)
}
```

**虚拟线程要点**：
- `VirtualThread` 是包私有类，继承自包私有 `BaseVirtualThread`
- 使用 continuation (由 JVM 实现的 `Continuation` 类) 实现挂起/恢复
- 默认调度器是 `ForkJoinPool.commonPool()` 的一个专用实例
- 挂起时不占用操作系统线程，可创建数百万个并发虚拟线程

#### ScopedValue (890 行, @since 25)

```java
// src/java.base/share/classes/java/lang/ScopedValue.java
public final class ScopedValue<T> {

    // 创建新实例
    public static <T> ScopedValue<T> newInstance();

    // 绑定值并执行
    public static <T> Carrier where(ScopedValue<T> key, T value);

    // 读取当前绑定
    public T get();
    public boolean isBound();
    public T orElse(T other);
    public <X extends Throwable> T orElseThrow(Supplier<X> supplier) throws X;

    // Carrier: 可链式绑定多个 ScopedValue
    public static final class Carrier {
        public <T> Carrier where(ScopedValue<T> key, T value);
        public <R, X extends Throwable> R call(CallableOp<? extends R, X> op) throws X;
        public void run(Runnable op);
    }

    // 函数式接口，支持受检异常
    public interface CallableOp<T, X extends Throwable> {
        T call() throws X;
    }

    // 内部: 快照绑定链
    static final class Snapshot { ... }
}
```

ScopedValue 在 JDK 25 中成为正式 API (`@since 25`)，是 `ThreadLocal` 的
结构化替代品。设计优势：
- 不可变绑定 (immutable binding)，避免 ThreadLocal 的内存泄漏
- 自动继承到子虚拟线程（与 StructuredTaskScope 配合）
- 基于栈帧语义，离开作用域自动清除

### 3.2 java.lang.invoke — 方法句柄体系

| 类 | 行数 | 职责 |
|----|------|------|
| `MethodHandle` | 1,908 | 类型安全的函数指针抽象 |
| `MethodHandles` | 7,888 | 工厂/组合器 (Lookup, filter, fold, ...) |
| `VarHandle` | 2,467 | 变量的原子/有序访问 |
| `LambdaMetafactory` | — | Lambda 表达式的引导方法 |
| `StringConcatFactory` | — | 字符串拼接的引导方法 |
| `CallSite` / `MutableCallSite` | — | invokedynamic 调用点 |

MethodHandle 是 `invokedynamic` 指令的基础，Lambda 表达式、字符串拼接、
`switch` 的模式匹配都通过它在运行时链接。

### 3.3 java.lang.classfile — Class-File API (since 24, JEP 457)

**161 个源文件**，提供读写 JVM class 文件的标准 API，替代 ASM 第三方库。

```java
// src/java.base/share/classes/java/lang/classfile/ClassFile.java
public sealed interface ClassFile
    permits ClassFileImpl {

    // 解析 class 文件
    static ClassFile of() { ... }
    ClassModel parse(byte[] bytes);

    // 生成 class 文件
    byte[] build(ClassDesc thisClass,
                 Consumer<? super ClassBuilder> handler);

    // 转换 class 文件
    byte[] transformClass(ClassModel model,
                          ClassTransform transform);
}
```

核心类型层级：
- `ClassFile` — 入口接口
- `ClassModel` / `MethodModel` / `FieldModel` — 解析后的只读模型
- `ClassBuilder` / `MethodBuilder` / `CodeBuilder` — 生成/转换构建器
- `Attribute` 子类型 (在 `java.lang.classfile.attribute` 中)
- `Instruction` 子类型 (在 `java.lang.classfile.instruction` 中)
- `ConstantPoolEntry` 子类型 (在 `java.lang.classfile.constantpool` 中)

### 3.4 java.lang.foreign — Foreign Function & Memory API (since 22, JEP 454)

**16 个公共源文件**，核心类型：

| 类/接口 | 职责 |
|---------|------|
| `MemorySegment` (2,810 行) | 统一表示堆内/堆外/映射内存 |
| `Arena` | 内存生命周期管理 (confined, shared, auto, global) |
| `MemoryLayout` / `StructLayout` / `UnionLayout` | 内存布局描述 |
| `ValueLayout` | 基本值类型布局 (JAVA_INT, JAVA_LONG, ADDRESS 等) |
| `SequenceLayout` / `PaddingLayout` | 数组布局 / 填充 |
| `Linker` (sealed) | 本地函数链接器 |
| `FunctionDescriptor` | 本地函数签名描述 |
| `SymbolLookup` | 本地符号查找 |
| `SegmentAllocator` | 段分配策略 |
| `AddressLayout` | 指针布局 |

**典型用法 — 调用 C 函数**：

```java
Linker linker = Linker.nativeLinker();
SymbolLookup stdlib = linker.defaultLookup();
MethodHandle strlen = linker.downcallHandle(
    stdlib.find("strlen").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
);
try (Arena arena = Arena.ofConfined()) {
    MemorySegment str = arena.allocateFrom("Hello");
    long len = (long) strlen.invokeExact(str);  // -> 5
}
```

### 3.5 java.util — 集合框架 (129 个直接文件)

关键实现类的代码规模：

| 类 | 行数 | 数据结构 |
|----|------|---------|
| `HashMap` | 2,588 | 数组 + 链表 + 红黑树 (>= 8 个节点树化) |
| `TreeMap` | 3,384 | 红黑树 |
| `ArrayList` | 1,834 | 动态数组 (默认容量 10, 1.5x 增长) |
| `LinkedList` | 1,540 | 双向链表 |
| `Collections` | 6,282 | 不可变包装、同步包装、工具方法 |
| `Arrays` | 8,756 | 排序、搜索、并行操作 |

集合层次的设计关键：
- `Iterable` -> `Collection` -> `List` / `Set` / `Queue`
- `Map` 独立层次
- JDK 9+ 的 `List.of()` / `Map.of()` 工厂方法返回不可变集合
- JDK 10+ 的 `List.copyOf()` / `Collectors.toUnmodifiableList()` 等
- JDK 21+ 的 `SequencedCollection` / `SequencedMap` 接口

### 3.6 java.util.stream — Stream API + Gatherer (40 个文件)

核心类型：

| 类型 | 角色 |
|------|------|
| `Stream<T>` | 引用类型流 |
| `IntStream` / `LongStream` / `DoubleStream` | 原始类型流 |
| `Collector<T,A,R>` | 可变归约操作 |
| `Collectors` | 预定义 Collector 工厂 |
| `Gatherer<T,A,R>` (@since 24) | 中间操作的通用抽象 |
| `Gatherers` (@since 24) | 预定义 Gatherer 工厂 |

**Gatherer API (JEP 485, since 24)** 填补了 Stream 中间操作不可自定义的空白：

```java
// Gatherer 接口 — 类比 Collector 之于终端操作
public interface Gatherer<T, A, R> {
    Supplier<A> initializer();                    // 创建状态
    Integrator<A, T, R> integrator();             // 逐元素处理
    BinaryOperator<A> combiner();                 // 并行合并
    BiConsumer<A, Downstream<? super R>> finisher(); // 结束处理
}

// 预定义 Gatherers
stream.gather(Gatherers.windowFixed(3))      // 固定窗口
stream.gather(Gatherers.windowSliding(3))    // 滑动窗口
stream.gather(Gatherers.fold(() -> init, folder)) // 有状态折叠
stream.gather(Gatherers.scan(() -> init, scanner)) // 前缀扫描
stream.gather(Gatherers.mapConcurrent(limit, fn)) // 并发映射
```

### 3.7 java.io / java.nio — I/O 体系

#### java.io (94 个文件) — 阻塞式字节/字符流

```
InputStream (抽象)
├── FileInputStream          // 文件字节输入
├── BufferedInputStream      // 缓冲装饰器
├── ByteArrayInputStream     // 内存字节数组
├── DataInputStream          // 基本类型读取
├── ObjectInputStream        // 对象反序列化
└── PipedInputStream         // 管道

OutputStream (抽象)
├── FileOutputStream
├── BufferedOutputStream
├── PrintStream              // System.out 的类型
└── ObjectOutputStream

Reader / Writer              // 字符流，同构层次
```

#### java.nio (166 个文件) — 非阻塞 / 内存映射 / 文件系统

```
Buffer
├── ByteBuffer               // 核心: 堆内 / 堆外
├── CharBuffer / IntBuffer / LongBuffer / ...

Channel
├── FileChannel              // 文件通道 (支持内存映射, transferTo)
├── SocketChannel            // TCP 通道
├── ServerSocketChannel      // TCP 监听
├── DatagramChannel          // UDP 通道
└── AsynchronousSocketChannel // 异步通道 (IOCP/epoll)

Selector                     // I/O 多路复用 (epoll/kqueue/IOCP)

java.nio.file
├── Path / Paths / Files     // 现代文件 API (since 7)
├── FileSystem / FileSystems // 文件系统抽象 (zip, jrt, ...)
└── WatchService             // 文件系统事件监听
```

### 3.8 java.time — Date/Time API (JSR 310, 87 个文件)

核心类分布在 4 个子包中：

```
java.time (22 个类)
├── Instant           // 时间线上的瞬间 (epoch-based)
├── LocalDate         // 无时区日期 (2024-03-15)
├── LocalTime         // 无时区时间 (10:15:30)
├── LocalDateTime     // 无时区日期时间
├── ZonedDateTime     // 带时区日期时间
├── OffsetDateTime    // 带偏移日期时间
├── Duration          // 基于秒的时间量
├── Period            // 基于日期的时间量 (年/月/日)
├── Year / YearMonth / MonthDay / Month / DayOfWeek
├── ZoneId / ZoneOffset
├── Clock / InstantSource
└── DateTimeException

java.time.format
├── DateTimeFormatter      // 格式化/解析
└── DateTimeFormatterBuilder

java.time.temporal
├── Temporal / TemporalAccessor / TemporalAdjuster
├── ChronoField / ChronoUnit
└── TemporalQueries

java.time.chrono
├── Chronology / IsoChronology
├── JapaneseChronology / ThaiBuddhistChronology / ...
└── ChronoLocalDate / ChronoZonedDateTime

java.time.zone
├── ZoneRules / ZoneRulesProvider
└── ZoneOffsetTransition
```

### 3.9 java.util.concurrent — JUC 并发框架 (97 个文件)

关键实现的代码规模反映了并发编程的复杂度：

| 类 | 行数 | 用途 |
|----|------|------|
| `ConcurrentHashMap` | 6,413 | 分段锁 -> CAS 的并发哈希表 |
| `ForkJoinPool` | 4,425 | 工作窃取线程池 (虚拟线程调度器基础) |
| `CompletableFuture` | 3,042 | 异步编程组合器 |
| `StructuredTaskScope` | 1,155 | 结构化并发 (preview) |
| `AbstractExecutorService` | 345 | 线程池抽象基类 |
| `ExecutorService` | 410 | 线程池接口 |
| `Future` | 323 | 异步结果接口 |

**子包结构**：

```
java.util.concurrent
├── locks/                   // ReentrantLock, StampedLock,
│                            // AbstractQueuedSynchronizer (AQS)
└── atomic/                  // AtomicInteger, AtomicReference,
                             // LongAdder, AtomicReferenceFieldUpdater
```

**AQS (AbstractQueuedSynchronizer)** 是锁框架的核心，ReentrantLock、
Semaphore、CountDownLatch、ReentrantReadWriteLock 都基于它实现。

#### StructuredTaskScope (preview, 1,155 行)

JDK 当前版本中仍为 preview (`@PreviewFeature(feature = STRUCTURED_CONCURRENCY)`)。
API 基于 `Joiner` 模式重新设计：

```java
// 核心接口
sealed interface Subtask<T> extends Supplier<T> {
    enum State { UNAVAILABLE, SUCCESS, FAILED }
    State state();
    T get();           // 仅在 SUCCESS 时可调用
    Throwable exception(); // 仅在 FAILED 时可调用
}

interface Joiner<T, R> {
    boolean onComplete(Subtask<? extends T> subtask);
    R result() throws Throwable;

    // 预定义 Joiner 工厂方法
    static <T> Joiner<T, List<T>> allSuccessfulOrThrow();
    static <T> Joiner<T, T> anySuccessfulOrThrow();
    static <T> Joiner<T, Void> awaitAllSuccessfulOrThrow();
    static <T> Joiner<T, Void> awaitAll();
    static <T> Joiner<T, List<T>> allUntil(Predicate<Subtask<T>> p);
}

// 使用示例
try (var scope = StructuredTaskScope.open(
        Joiner.<String>anySuccessfulOrThrow())) {
    scope.fork(() -> fetchFromServiceA());
    scope.fork(() -> fetchFromServiceB());
    String first = scope.join();   // 返回最先成功的结果
}
```

### 3.10 java.security — 安全框架 (190 个文件)

```
java.security
├── Provider / Security       // 安全提供者注册
├── MessageDigest             // 哈希 (SHA-256, SHA-3, ...)
├── Signature                 // 数字签名
├── KeyPairGenerator          // 密钥对生成
├── KeyStore                  // 密钥存储
├── SecureRandom              // 加密安全随机数
├── cert/                     // X.509 证书
├── interfaces/               // DSA/RSA/EC 密钥接口
└── spec/                     // 密钥/参数规格

javax.crypto                  // (也在 java.base 中!)
├── Cipher                    // 对称/非对称加密
├── Mac                       // 消息认证码
├── KeyGenerator              // 对称密钥生成
├── KeyAgreement              // 密钥协商 (DH, ECDH)
├── spec/                     // CipherSpec 等
└── interfaces/               // DHKey 等

javax.net.ssl                 // TLS/SSL
├── SSLContext / SSLEngine
├── SSLSocket / SSLServerSocket
├── TrustManager / KeyManager
└── X509TrustManager
```

java.base 内置的安全提供者：
- `sun.security.provider.Sun` — MessageDigest, SecureRandom, CertificateFactory
- `com.sun.crypto.provider.SunJCE` — Cipher, Mac, KeyGenerator (100 个文件)
- `sun.security.ssl.HybridProvider` — TLS 实现

---

## 4. 内部 API (Internal APIs)

### 4.1 jdk.internal.* (561 个文件)

| 子包 | 文件数 | 职责 |
|------|--------|------|
| `jdk.internal.misc` | ~30 | `Unsafe` (3,906 行), `VM`, `Signal`, `CDS` |
| `jdk.internal.access` | ~30 | `SharedSecrets` — 跨模块友元访问 |
| `jdk.internal.classfile` | ~80 | Class-File API 的内部实现 |
| `jdk.internal.foreign` | ~40 | FFM API 的内部实现 |
| `jdk.internal.vm` | ~20 | VM 信息, 注解 (@Stable, @ForceInline, @IntrinsicCandidate) |
| `jdk.internal.reflect` | ~20 | 反射加速: MethodAccessor, ConstructorAccessor |
| `jdk.internal.loader` | ~15 | BuiltinClassLoader, ClassLoaders |
| `jdk.internal.module` | ~15 | 模块描述符解析, 层 (Layer) 管理 |
| `jdk.internal.math` | ~5 | FloatingDecimal, DoubleConsts |
| `jdk.internal.jimage` | ~10 | jimage 格式 (运行时镜像) |
| `jdk.internal.jrtfs` | ~5 | jrt:/ FileSystemProvider |
| `jdk.internal.org` | ~20 | 嵌入的 ASM (供 jdk.jfr 等使用) |
| `jdk.internal.util` | ~15 | ArraysSupport, Preconditions |
| `jdk.internal.random` | ~10 | 随机数算法内部实现 |
| `jdk.internal.net.quic` | 8 | QUIC 协议 TLS 层内部支持 |
| `jdk.internal.event` | ~5 | JFR 事件基础设施 |
| `jdk.internal.io` | ~3 | JdkConsoleProvider |
| `jdk.internal.perf` | ~3 | PerfCounter (jvmstat 数据) |
| `jdk.internal.platform` | ~5 | 容器感知 (cgroup) |
| `jdk.internal.icu` | ~10 | Unicode 支持 (ICU 子集) |
| `jdk.internal.logger` | ~5 | System.Logger 默认实现 |

#### Unsafe (3,906 行) — JDK 内部的"瑞士军刀"

```java
// src/java.base/share/classes/jdk/internal/misc/Unsafe.java
public final class Unsafe {
    // 内存操作
    public native long allocateMemory(long bytes);
    public native void freeMemory(long address);
    public native void copyMemory(Object src, long srcOff, Object dst, long dstOff, long bytes);

    // CAS 操作 (并发基础设施)
    @IntrinsicCandidate
    public final native boolean compareAndSetInt(Object o, long offset, int expected, int x);
    @IntrinsicCandidate
    public final native boolean compareAndSetLong(Object o, long offset, long expected, long x);
    @IntrinsicCandidate
    public final native boolean compareAndSetReference(Object o, long offset, Object expected, Object x);

    // 有序/volatile 写
    public native void putIntVolatile(Object o, long offset, int x);
    public native void putOrderedInt(Object o, long offset, int x);

    // 对象字段偏移量
    public native long objectFieldOffset(Field f);

    // 类初始化
    public native void ensureClassInitialized(Class<?> c);

    // 内存屏障
    @IntrinsicCandidate
    public native void loadFence();
    @IntrinsicCandidate
    public native void storeFence();
    @IntrinsicCandidate
    public native void fullFence();
}
```

`Unsafe` 被限定导出给 16 个模块 (jdk.compiler, jdk.jfr, jdk.unsupported 等)。
外部库通过 `jdk.unsupported` 模块的 `sun.misc.Unsafe` (已废弃的桥接类) 间接使用。
`VarHandle` 和 `MemorySegment` 是其正式替代品。

#### SharedSecrets — 跨模块友元模式

```java
// src/java.base/share/classes/jdk/internal/access/SharedSecrets.java
public class SharedSecrets {
    // 每个需要跨模块访问的包注册一个 Access 接口
    public static void setJavaLangAccess(JavaLangAccess jla) { ... }
    public static JavaLangAccess getJavaLangAccess() { ... }

    public static void setJavaNetUriAccess(JavaNetUriAccess jnua) { ... }
    public static void setJavaUtilJarAccess(JavaUtilJarAccess access) { ... }
    // ... 20+ 对 get/set 方法
}
```

这是模块系统下的 "friend class" 模式：java.lang 包在初始化时注册
`JavaLangAccess` 实现，让 jdk.jfr 等模块通过 SharedSecrets 访问
java.lang 的包私有方法。

### 4.2 sun.* (1,086 个文件)

| 子包 | 职责 |
|------|------|
| `sun.security.*` | 完整的安全/加密实现 (SSL, X.509, PKCS, RSA, DSA) |
| `sun.nio.ch` | Channel/Selector 的平台实现 (EPollSelectorImpl 等) |
| `sun.nio.cs` | 字符集编解码器 (UTF-8, ISO-8859-1, US-ASCII) |
| `sun.nio.fs` | 文件系统实现 (UnixFileSystem, WindowsFileSystem) |
| `sun.net.*` | 网络协议实现 (HTTP, DNS, SOCKS) |
| `sun.invoke.*` | MethodHandle 链接器内部 |
| `sun.reflect.*` | 注解解析, 泛型反射 |
| `sun.text.*` | 文本/区域资源 |
| `sun.util.*` | CLDR 数据、日历、区域设置 |
| `sun.launcher` | java 启动器支持 |

---

## 5. JDK 24-25 主要变更

### 5.1 正式化的 API (Finalized)

| 特性 | JEP | 正式版本 | 说明 |
|------|-----|---------|------|
| Class-File API | 457 | JDK 24 | 读写 class 文件的标准 API |
| Stream Gatherers | 485 | JDK 24 | 自定义中间流操作 |
| Scoped Values | 487 | JDK 25 | ThreadLocal 的结构化替代 |

### 5.2 仍在 Preview 的特性

| 特性 | JEP | 状态 | 说明 |
|------|-----|------|------|
| Structured Concurrency | 505 | Preview (多轮) | StructuredTaskScope + Joiner |
| Flexible Constructor Bodies | 513 | Preview | 构造器中 super() 前可执行语句 |

### 5.3 新增内部基础设施

| 组件 | 位置 | 说明 |
|------|------|------|
| QUIC 内部支持 | `jdk.internal.net.quic` (8 文件) | HTTP/3 的底层传输 |
| Classfile 内部实现 | `jdk.internal.classfile` (~80 文件) | ClassFile API 的实现层 |
| 容器感知增强 | `jdk.internal.platform` | 改进 cgroup v2 支持 |

---

## 6. 关键设计决策

### 6.1 为什么 java.base 不可替换

java.base 是模块图的根：
1. **编译器硬编码**: `javac` 将 `java.lang.*` 自动导入每个编译单元
2. **JVM 硬编码**: 类加载器、对象布局、GC 根扫描都假定 `java.lang.Object` 等类的存在
3. **隐式依赖**: 所有模块的 `requires java.base` 是自动添加的，无法去除
4. **`--limit-modules` 排除**: 即使用 `--limit-modules` 限制模块，java.base 始终存在
5. **引导类路径**: java.base 的类由引导类加载器 (bootstrap class loader) 加载，
   这是 JVM 启动时最先初始化的类加载器

### 6.2 模块的层次地位

```
java.base (根模块 — 所有模块隐式依赖)
├── java.logging
├── java.sql ──── requires java.logging
├── java.net.http ──── requires java.base (显式 uses Unsafe)
├── java.desktop
├── jdk.compiler
├── jdk.jfr
└── ... (所有其他模块)
```

没有任何模块可以声明 `requires java.base` 之外的对 java.base 的依赖关系 —
这种依赖是隐式且不可选的。java.base 本身没有 `requires` 任何其他模块。

### 6.3 强封装 (Strong Encapsulation) 策略

JDK 9-16 期间，`--illegal-access=permit` 允许反射访问内部 API。
JDK 17+ 默认 `--illegal-access=deny`（已移除该选项）。

访问内部 API 的合法途径：
1. **限定导出** (`exports ... to`): 编译期可见
2. **`--add-exports`**: 命令行打开特定包
3. **`--add-opens`**: 命令行打开深度反射
4. **`jdk.unsupported` 模块**: 提供 `sun.misc.Unsafe` 等桥接

### 6.4 `@Stable` / `@ForceInline` / `@IntrinsicCandidate`

这些 `jdk.internal.vm.annotation` 中的注解是 JIT 优化的关键：

| 注解 | 效果 |
|------|------|
| `@Stable` | 告诉 JIT 字段初始化后不会改变，可将其值当作编译期常量 |
| `@ForceInline` | 强制内联，忽略 JIT 的大小启发式 |
| `@IntrinsicCandidate` | JIT 对该方法有手工编写的汇编实现 |
| `@Contended` | 防止伪共享，填充 cache line |
| `@Hidden` | 对堆栈遍历不可见 |
| `@ReservedStackAccess` | 在栈溢出时保留额外空间 |

### 6.5 Compact Strings 的工程权衡

JEP 254 (JDK 9) 的 Compact Strings 用 `byte[]` 替代 `char[]`：

**收益**:
- 英文/ASCII 为主的应用节省约 30-40% 堆内存
- 改善 GC 压力和 cache 利用率

**代价**:
- 每次字符操作需要检查 `coder` 字段
- JIT 通过常量折叠 `COMPACT_STRINGS` 消除分支开销
- 纯 CJK 文本无节省（仍用 UTF16 编码）

---

## 7. 源码导航指南

### 快速定位

```bash
# 模块声明
src/java.base/share/classes/module-info.java

# 核心类
src/java.base/share/classes/java/lang/Object.java
src/java.base/share/classes/java/lang/String.java       # 5,364 行
src/java.base/share/classes/java/lang/Thread.java
src/java.base/share/classes/java/lang/VirtualThread.java # 1,445 行
src/java.base/share/classes/java/lang/Class.java
src/java.base/share/classes/java/lang/System.java
src/java.base/share/classes/java/lang/ScopedValue.java   # 890 行, @since 25

# 方法句柄
src/java.base/share/classes/java/lang/invoke/MethodHandles.java  # 7,888 行

# 集合
src/java.base/share/classes/java/util/HashMap.java      # 2,588 行
src/java.base/share/classes/java/util/Arrays.java        # 8,756 行

# 并发
src/java.base/share/classes/java/util/concurrent/ConcurrentHashMap.java  # 6,413 行
src/java.base/share/classes/java/util/concurrent/ForkJoinPool.java       # 4,425 行
src/java.base/share/classes/java/util/concurrent/CompletableFuture.java  # 3,042 行
src/java.base/share/classes/java/util/concurrent/StructuredTaskScope.java # 1,155 行

# FFM
src/java.base/share/classes/java/lang/foreign/MemorySegment.java  # 2,810 行
src/java.base/share/classes/java/lang/foreign/Linker.java

# Class-File API
src/java.base/share/classes/java/lang/classfile/ClassFile.java  # 1,076 行

# 内部
src/java.base/share/classes/jdk/internal/misc/Unsafe.java       # 3,906 行
src/java.base/share/classes/jdk/internal/access/SharedSecrets.java
```

### 平台特定实现

```bash
# Linux epoll
src/java.base/linux/classes/sun/nio/ch/EPollSelectorImpl.java

# macOS kqueue
src/java.base/macosx/classes/sun/nio/ch/KQueueSelectorImpl.java

# Windows IOCP
src/java.base/windows/classes/sun/nio/ch/WindowsSelectorImpl.java

# Unix 文件系统
src/java.base/unix/classes/sun/nio/fs/UnixFileSystem.java
```

---

## 8. 相关链接

- [java.base API 文档 (JDK 25)](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/module-summary.html)
- [源码浏览 (OpenJDK master)](https://github.com/openjdk/jdk/tree/master/src/java.base)
- [JEP 254: Compact Strings](https://openjdk.org/jeps/254)
- [JEP 454: Foreign Function & Memory API](https://openjdk.org/jeps/454)
- [JEP 457: Class-File API](https://openjdk.org/jeps/457)
- [JEP 462: Structured Concurrency](https://openjdk.org/jeps/462)
- [JEP 487: Scoped Values](https://openjdk.org/jeps/487)
- [JEP 485: Stream Gatherers](https://openjdk.org/jeps/485)
