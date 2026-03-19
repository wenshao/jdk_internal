# 性能优化演进时间线

Java 性能优化从 JDK 1.0 到 JDK 26 的完整演进历程。

---

## 时间线概览

```
JDK 1.0 ──── JDK 5 ──── JDK 6 ──── JDK 7 ──── JDK 8 ──── JDK 17 ──── JDK 26
 │             │           │           │           │           │           │
解释器        JIT编译器    性能统计    Compressed- String      Escape    Lock
执行         (HotSpot)    工具        Oops       Dedup      Analysis    Elision
```

---

## JVM 执行引擎

### 解释器 vs JIT 编译器

```
┌─────────────────────────────────────────────────────────┐
│                HotSpot 执行引擎                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Java 字节码                                            │
│       │                                                 │
│       ▼                                                 │
│  ┌─────────────────────────────────────────────┐        │
│  │            解释器 (Interpreter)            │        │
│  │  ├── 快速启动                               │        │
│  │  ├── 即时执行                               │        │
│  │  └── 收集热点信息                           │        │
│  └─────────────────┬───────────────────────────┘        │
│                    │                                    │
│                    ▼ (热点检测)                        │
│  ┌─────────────────────────────────────────────┐        │
│  │            C1 编译器 (Client)               │        │
│  │  ├── 简单优化                               │        │
│  │  ├── 快速编译                               │        │
│  │  └── 启动性能                               │        │
│  └─────────────────┬───────────────────────────┘        │
│                    │ (更多调用)                       │
│                    ▼                                   │
│  ┌─────────────────────────────────────────────┐        │
│  │            C2 编译器 (Server)               │        │
│  │  ├── 深度优化                               │        │
│  │  ├── 内联                                   │        │
│  │  ├── 循环优化                               │        │
│  │  └── 峰值性能                               │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 分层编译 (Tiered Compilation)

```java
// JDK 7+ 分层编译
// 0: 解释执行
// 1: C1 编译 (带 profiling)
// 2: C1 编译 (无 profiling)
// 3: C2 编译

// 查看编译级别
-XX:+PrintCompilation -XX:+UnlockDiagnosticVMOptions -XX:+LogCompilation

// 禁用分层编译
-XX:-TieredCompilation

// 设置分层编译阈值
-XX:Tier3CompileLevel=1000     // C1 → C2 阈值 (调用次数)
-XX:Tier4CompileLevel=1500     // C2 编译阈值
```

---

## JIT 编译优化

### 方法内联

```java
// 内联优化示例
public class InlineExample {
    // 小方法会被内联
    private int add(int a, int b) {
        return a + b;
    }

    public int compute(int x, int y) {
        // 编译后可能变成: return x + y + 10;
        return add(x, y) + 10;
    }
}

// 热点大小限制
-XX:FreqInlineSize=325          // 默认 325 字节
-XX:MaxInlineSize=35            // 最大内联大小
-XX:MaxTrivialSize=6            // 简单方法最大内联大小
```

### 循环优化

```java
// 循环展开 (Loop Unrolling)
for (int i = 0; i < 4; i++) {
    sum += array[i];
}
// 可能被优化为:
// sum += array[0];
// sum += array[1];
// sum += array[2];
// sum += array[3];

// 循环向量化 (SIMD)
for (int i = 0; i < array.length; i++) {
    array[i] *= 2;
}
// 使用 SIMD 指令并行处理
```

### 逃逸分析

```java
// 逃逸分析 - 标量替换
public class EscapeAnalysis {
    public void method() {
        // 对象未逃逸，可以栈上分配
        Point p = new Point(1, 2);
        int x = p.x;
        int y = p.y;
        // p 不再使用，可以完全消除
    }

    public Point createPoint() {
        // 对象逃逸，必须在堆上分配
        return new Point(1, 2);
    }
}

// 启用逃逸分析 (默认启用)
-XX:+DoEscapeAnalysis
-XX:+EliminateAllocations      // 标量替换
-XX:+EliminateLocks              // 锁消除
```

---

## JDK 5 - 性能改进

### StringBuilder

```java
// JDK 5: StringBuilder 替代 StringBuffer
// 非同步版本，性能更好

// 编译器优化
String s = a + b + c;
// 编译为:
// new StringBuilder().append(a).append(b).append(c).toString();
```

### 类型配置文件

```bash
# types.config - 类型配置
# 用于 JIT 编译器优化
[ hotspot ]
int 100
java.lang.String 200
```

---

## JDK 6 - 性能监控

### jstat

```bash
# JVM 统计监控
jstat -gcutil <pid> 1000 10

# 输出:
#  S0     S1     E      O      M     CCS     YGC     YGCT    FGC    FGCT     GCT
#  0.00   0.00   0.00  10.00  10.00   0.00      1    0.050     0    0.000    0.050
```

### jmap

```bash
# 堆转储
jmap -dump:live,format=b,file=heap.hprof <pid>

# 类直方图
jmap -histo:live <pid>
```

---

## JDK 7 - G1 GC

### Compressed Oops

```java
// 压缩普通对象指针
// 32位指针支持更大堆

// 启用压缩指针 (默认启用)
-XX:+UseCompressedOops

// 堆大小限制
// < 32GB: 32位指针
// >= 32GB: 64位指针
```

---

## JDK 8 - 性能改进

### Lambda 性能

```java
// Lambda 性能特性:
// 1. invokedynamic 动态调用
// 2. LambdaMetafactory 缓存
// 3. 方法句柄绑定

// Lambda vs 匿名类性能
// 首次调用: Lambda 较慢 (需要生成类)
// 后续调用: Lambda 更快 (直接方法句柄)
```

### String Dedup

```java
// G1 字符串去重
// 自动去除重复的 String

// 启用
-XX:+UseStringDeduplication

// 去重阈值
-XX:StringDeduplicationAgeThreshold=3
```

---

## JDK 17+ - 性能改进

### Record 性能

```java
// Record 比 POJO 性能更好
// - 自动生成优化的字节码
// - 无 getter/setter 调用开销
// - 更好的内联

record Point(int x, int y) { }

// 传统 POJO
class Point {
    private final int x;
    private final int y;
    // getter, setter, equals, hashCode, toString
}
```

### Pattern Matching 性能

```java
// Pattern Matching 编译为优化的字节码
if (obj instanceof String s) {
    // 无需强制转换
    System.out.println(s.length());
}
```

---

## JDK 21+ - 虚拟线程性能

### Virtual Threads 性能

```java
// 虚拟线程适用场景
// I/O 密集型: 10-100x 性能提升
// CPU 密集型: 无提升

// 示例
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000_000; i++) {
        executor.submit(() -> {
            // I/O 操作
        });
    }
}
```

---

## 性能调优工具

### JFR (Java Flight Recorder)

```bash
# JFR - 低开销的性能分析
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr \
     -XX:FlightRecorderOptions=samplethreads=true \
     MyApp

# 分析 JFR 文件
jfr --summary recording.jfr
jfr --print recording.jfr
```

### JMC (Java Mission Control)

```bash
# JMC - JVM 监控工具
# 可视化监控、分析
jmc
```

### async-profiler

```bash
# async-profiler - 采样分析
profiler.sh -d 30 -f profile.html <pid>

# CPU 采样
profiler.sh -d 30 -e cpu <pid>

# 内存分配采样
profiler.sh -d 30 -e alloc <pid>
```

---

## 性能最佳实践

### 对象创建

```java
// ✅ 推荐: 重用对象
private static final DateFormat DATE_FORMAT =
    new SimpleDateFormat("yyyy-MM-dd");

// ❌ 避免: 重复创建
for (int i = 0; i < 1000; i++) {
    DateFormat df = new SimpleDateFormat("yyyy-MM-dd");
    df.format(date);
}
```

### 集合初始化

```java
// ✅ 推荐: 指定初始容量
List<String> list = new ArrayList<>(1000);
Map<String, Integer> map = new HashMap<>(1000);

// ❌ 避免: 默认容量导致扩容
List<String> list = new ArrayList<>();
for (int i = 0; i < 1000; i++) {
    list.add("item");  // 多次扩容
}
```

### 字符串拼接

```java
// ✅ 推荐: 使用 +
String result = "Hello " + name;  // 编译器优化

// ✅ 推荐: 循环中使用 StringBuilder
StringBuilder sb = new StringBuilder();
for (String s : list) {
    sb.append(s);
}

// ❌ 避免: 循环中使用 +
String result = "";
for (String s : list) {
    result += s;  // 每次创建新 String
}
```

---

## 性能对比

### JDK 版本性能

| 版本 | 启动时间 | 吞吐量 | 内存 |
|------|----------|--------|------|
| JDK 8 | 基准 | 基准 | 基准 |
| JDK 11 | +10% | +5% | -10% |
| JDK 17 | +15% | +10% | -15% |
| JDK 21 | +20% | +8% | -20% |
| JDK 26 | +25% | +12% | -22% |

---

## 时间线总结

| 版本 | 特性 | 说明 |
|------|------|------|
| JDK 1.0 | 解释器 | 纯解释执行 |
| JDK 1.2 | JIT 编译器 | HotSpot 引入 |
| JDK 5 | C1/C2 分层编译 | 性能大幅提升 |
| JDK 6 | 动态编译优化 | jstat/jmap |
| JDK 7 | G1 GC | Compressed Oops |
| JDK 8 | Lambda/String Dedup | invokedynamic |
| JDK 17 | Record/Pattern Matching | 编译器优化 |
| JDK 21 | 虚拟线程 | I/O 性能提升 |
| JDK 26 | 多项性能改进 | 持续优化 |

---

## 相关链接

- [Tuning Garbage Collectors](https://docs.oracle.com/en/java/javase/21/gctuning/)
- [Java Flight Recorder](https://docs.oracle.com/en/java/javase/21/docs/specs/man/jfr.html)
