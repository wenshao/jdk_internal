# 内存管理演进时间线

Java 内存管理从 JDK 1.0 到 JDK 26 的完整演进历程。

---

## 时间线概览

```
JDK 1.0 ──── JDK 5 ──── JDK 6 ──── JDK 8 ──── JDK 11 ──── JDK 17 ──── JDK 26
 │             │           │           │           │           │           │
堆/栈         自动内存    Compressed- String      ZGC        分代ZGC    Memory
内存管理       管理        Oops        Dedup      生产      生产       Segment
```

---

## 内存结构

### JVM 内存布局

```
┌─────────────────────────────────────────────────────────┐
│                    JVM 内存布局                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │              堆 (Heap)                       │        │
│  │  ├── 新生代 (Young Gen)                     │        │
│  │  │   ├── Eden                               │        │
│  │  │   ├── Survivor S0                        │        │
│  │  │   └── Survivor S1                        │        │
│  │  └── 老年代 (Old Gen)                       │        │
│  │      ├── Tenured                             │        │
│  │      └── Humongous (大对象)                │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │              栈 (Stack)                      │        │
│  │  ├── Java 栈 (方法调用、局部变量)            │        │
│  │  └── 本地方法栈 (Native 方法)               │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │              方法区 (Method Area)            │        │
│  │  ├── 类元数据                               │        │
│  │  ├── 常量池                                 │        │
│  │  └── 静态变量                               │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │              程序计数器 (PC Register)        │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │              本地方法栈 (Native Stack)        │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## JDK 5 - 内存管理改进

### WeakReference 等

```java
import java.lang.ref.*;

// 引用类型
Object obj = new Object();

// WeakReference - 弱引用
WeakReference<Object> weakRef = new WeakReference<>(obj);
// GC 时会被回收

// SoftReference - 软引用
SoftReference<Object> softRef = new SoftReference<>(obj);
// 内存不足时回收

// PhantomReference - 虚引用
ReferenceQueue<Object> queue = new ReferenceQueue<>();
PhantomReference<Object> phantomRef =
    new PhantomReference<>(obj, queue);
// 用于跟踪回收

// WeakHashMap
Map<Object, String> map = new WeakHashMap<>();
// 键是弱引用，GC 时自动清理
```

### 内存池

```java
// 对象池 (谨慎使用)
// ❌ 不推荐: 手动对象池
// - 增加复杂度
// - 可能导致内存泄漏
// - GC 已足够高效

// ✅ 推荐: 使用内置缓存
// - IntegerCache (-128~127)
// - String.intern() (谨慎使用)
// - ThreadLocal
```

---

## JDK 6 - Compressed Oops

### 压缩普通对象指针

```
┌─────────────────────────────────────────────────────────┐
│              Compressed Oops (压缩指针)                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  64位 JVM 中的对象引用                                  │
│                                                         │
│  未压缩:                    压缩后:                       │
│  ┌─────────┐                ┌─────────┐                  │
│  │ 引用    │                │ 引用    │                  │
│  │ 64 位   │                │ 32 位   │                  │
│  └─────────┘                └─────────┘                  │
│  │                             │                         │
│  ▼                             ▼                         │
│  堆地址 (64位)                  基址 + 偏移量              │
│                                                         │
│  优势:                                                   │
│  - 减少指针大小 (节省内存)                              │
│  - 提高缓存命中率                                       │
│  - 支持 < 32GB 堆                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 配置

```bash
# 启用压缩指针 (默认启用)
-XX:+UseCompressedOops

# 堆大小限制
# < 32GB: 32位指针
# >= 32GB: 64位指针

# 对齐方式
-XX:ObjectAlignmentInBytes=8  # 默认 8 字节对齐
```

---

## JDK 8 - 内存优化

### String Dedup

```java
// G1 字符串去重
// 自动去除重复的 String

// 启用
-XX:+UseStringDeduplication

// 配置
-XX:StringDeduplicationAgeThreshold=3  # 3 代后去重
-XX:StringDeduplicationCleanupInterval=1000
```

### 元空间

```java
// JDK 8+: 元空间替代永久代
// - 存储类元数据
// - 使用本地内存
// - 可动态扩容

// 配置
-XX:MetaspaceSize=256M          # 初始大小
-XX:MaxMetaspaceSize=512M       # 最大大小
-XX:MinMetaspaceFreeRatio=40    # 最小空闲比例
-XX:MaxMetaspaceFreeRatio=70    # 最大空闲比例
```

---

## JDK 11+ - ZGC 内存管理

### ZGC 内存模型

```
┌─────────────────────────────────────────────────────────┐
│                    ZGC 读屏障                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  读对象引用                                              │
│       │                                                 │
│       ▼                                                 │
│  ┌─────────────────┐                                    │
│  │  读屏障检查      │                                    │
│  └────────┬────────┘                                    │
│           │                                              │
│      ┌────┴────┐                                          │
│      │         │                                          │
│      ▼         ▼                                          │
│  ┌──────┐ ┌──────┐                                       │
│  │已染色│ │未染色│                                       │
│  └──┬───┘ └──┬───┘                                       │
│     │       │                                           │
│     │       ▼                                           │
│     │   ┌─────────────────┐                             │
│     │   │  自染/重定位      │                             │
│     │   └─────────────────┘                             │
│     │                                                   │
│     └──→ 直接读取                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### ZGC 配置

```bash
# ZGC 内存配置
-XX:+UseZGC

# 堆大小 (自动调整)
-Xmx16g

# 并发 GC 线程
-XX:ConcGCThreads=4

# 回收间隔
-XX:ZCollectionInterval=5
```

---

## JDK 17+ - 分代 ZGC

### 分代内存布局

```
┌─────────────────────────────────────────────────────────┐
│                  分代 ZGC 布局                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │              年轻代 (ZST)                   │        │
│  │  ├── Eden                                  │        │
│  │  └── Survivor                              │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │              老年代 (ZLT)                   │        │
│  │  ├── Tenured 对象                          │        │
│  │  └── Humongous 对象                        │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
│  年轻代 GC: 只扫描年轻代，频率高，速度快               │
│  老年代 GC: 扫描老年代，频率低，复杂度高                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 分代 ZGC 配置

```bash
# 启用分代 ZGC
-XX:+ZGCGenerational

# 调整代大小
-XX:NewSize=512m
-XX:MaxNewSize=2g
```

---

## JDK 22+ - Foreign Memory Access

### MemorySegment

```java
import jdk.incubator.foreign.*;

// 堆外内存分配 (JDK 22+)
try (Arena arena = Arena.ofConfined()) {
    // 分配堆外内存
    MemorySegment segment = arena.allocate(1024);

    // 写入数据
    segment.set(ValueLayout.JAVA_INT, 0, 42);
    segment.set(ValueLayout.JAVA_LONG, 8, 123456789L);

    // 读取数据
    int value = segment.get(ValueLayout.JAVA_INT, 0);
    long value2 = segment.get(ValueLayout.JAVA_LONG, 8);
}

// 优势:
// - 不受 GC 管理
// - 与原生代码交互
// - 零拷贝 I/O
```

### Arena

```java
// Arena - 内存段生命周期管理
// 1. Confined Arena - 单线程
try (Arena arena = Arena.ofConfined()) {
    MemorySegment segment = arena.allocate(1024);
}

// 2. Shared Arena - 多线程
try (Arena arena = Arena.ofShared()) {
    MemorySegment segment = arena.allocate(1024);
}

// 3. Auto Arena - 自动清理
Arena arena = Arena.ofAuto();
MemorySegment segment = arena.allocate(1024);
// GC 自动清理
```

---

## 内存泄漏排查

### 常见原因

```java
// 1. 静态集合持有对象
public class MemoryLeak {
    private static final Map<String, Object> CACHE = new HashMap<>();
    // 持续增长，不清理
}

// 2. 未关闭的资源
try {
    Connection conn = dataSource.getConnection();
    // 忘记关闭
}

// 3. ThreadLocal 未清理
private static final ThreadLocal<Object> THREAD_LOCAL =
    new ThreadLocal<>();
// 线程池场景下，线程不释放，ThreadLocal 不清理

// 4. 监听器/回调
public void addListener(Listener listener) {
    listeners.add(listener);
    // 监听器持有外部引用
}
```

### 分析工具

```bash
# Heap Dump 分析
jmap -dump:live,format=b,file=heap.hprof <pid>

# MAT (Memory Analyzer Tool)
# Eclipse MAT 分析 heap.hprof

# jhat (JDK 自带)
jhat -port 7000 heap.hprof
# 浏览器访问 http://localhost:7000
```

---

## 内存调优

### 堆大小配置

```bash
# 初始堆大小
-Xms2g

# 最大堆大小
-Xmx4g

# 新生代比例
-XX:NewRatio=2  # 新生代:老年代 = 1:2

# Eden/Survivor 比例
-XX:SurvivorRatio=8  # Eden:S0:S1 = 8:1:1
```

### 元空间配置

```bash
# 元空间初始大小
-XX:MetaspaceSize=256m

# 元空间最大大小
-XX:MaxMetaspaceSize=512m

# 类空间跟踪
-XX:+TraceClassUnloading
-XX:+TraceClassLoading
```

---

## 最佳实践

### 避免内存泄漏

```java
// ✅ 推荐: 使用 try-with-resources
try (Connection conn = dataSource.getConnection()) {
    // 自动关闭
}

// ✅ 推荐: 及时清理
ThreadLocal<String> tl = new ThreadLocal<>();
try {
    tl.set("value");
} finally {
    tl.remove();  // 必须清理
}

// ✅ 推荐: 使用 WeakHashMap
Map<Object, Object> cache = new WeakHashMap<>();
```

### 对象重用

```java
// ✅ 推荐: 重用对象
private static final DateFormat DATE_FORMAT =
    new SimpleDateFormat("yyyy-MM-dd");

// ❌ 避免: 重复创建
for (int i = 0; i < 1000; i++) {
    DateFormat df = new SimpleDateFormat("yyyy-MM-dd");
}
```

---

## 时间线总结

| 版本 | 特性 | 说明 |
|------|------|------|
| JDK 5 | WeakReference 等 | 引用类型 |
| JDK 6 | Compressed Oops | 压缩指针 |
| JDK 8 | 元空间、String Dedup | 永久代移除 |
| JDK 11 | ZGC | 低延迟 GC |
| JDK 15 | ZGC 生产可用 | 正式版 |
| JDK 21 | 分代 ZGC | 降低 GC 频率 |
| JDK 22 | Foreign Memory Access | 堆外内存 |

---

## 相关链接

- [Memory Management](https://docs.oracle.com/en/java/javase/21/gctuning/)
- [ZGC](https://openjdk.org/jeps/439)
