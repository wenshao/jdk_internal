# JDK 8-26 速查表 (Cheat Sheet)

快速参考卡片，覆盖 JDK 8 到 JDK 26 的语法、API、JVM 参数和诊断命令。

---
## 目录

1. [版本特性一览表](#1-版本特性一览表)
2. [语法速查 (Syntax)](#2-语法速查-syntax)
3. [API 速查 (Standard Library)](#3-api-速查-standard-library)
4. [JVM 参数速查 (JVM Flags)](#4-jvm-参数速查-jvm-flags)
5. [GC 选择指南](#5-gc-选择指南)
6. [诊断命令速查 (Diagnostic Tools)](#6-诊断命令速查-diagnostic-tools)
7. [JDK 26 新特性速查](#7-jdk-26-新特性速查)
8. [常用代码片段](#8-常用代码片段)

---

## 1. 版本特性一览表

| 版本 | 类型 | GA 日期 | 一行总结 |
|------|------|---------|----------|
| **JDK 8** | LTS | 2014-03 | Lambda 表达式, Stream API, java.time, Optional |
| **JDK 9** | Feature | 2017-09 | JPMS 模块系统 (Jigsaw), JShell |
| **JDK 10** | Feature | 2018-03 | var 局部变量类型推断, G1 并行 Full GC |
| **JDK 11** | LTS | 2018-09 | HttpClient 正式版, Java EE 移除, ZGC 实验性 |
| **JDK 12** | Feature | 2019-03 | Switch Expressions 预览, Shenandoah GC |
| **JDK 13** | Feature | 2019-09 | Text Blocks 预览, ZGC 返回未使用内存 |
| **JDK 14** | Feature | 2020-03 | Records 预览, instanceof 模式匹配预览, CMS 移除 |
| **JDK 15** | Feature | 2020-09 | Sealed Classes 预览, ZGC/Shenandoah 正式, Nashorn 移除 |
| **JDK 16** | Feature | 2021-03 | Records 正式, Pattern Matching instanceof 正式, Stream.toList() |
| **JDK 17** | LTS | 2021-09 | Sealed Classes 正式, 强封装 (JEP 403), Security Manager 废弃 |
| **JDK 18** | Feature | 2022-03 | UTF-8 默认编码, Simple Web Server |
| **JDK 19** | Feature | 2022-09 | Virtual Threads 预览, Structured Concurrency 预览 |
| **JDK 20** | Feature | 2023-03 | Scoped Values 预览, Record Patterns 第二次预览 |
| **JDK 21** | LTS | 2023-09 | Virtual Threads 正式, Pattern Matching switch 正式, 分代 ZGC |
| **JDK 22** | Feature | 2024-03 | FFM API 正式, Unnamed Variables 正式 |
| **JDK 23** | Feature | 2024-09 | ZGC 分代模式默认, Markdown Javadoc |
| **JDK 24** | Feature | 2025-03 | Stream Gatherers 正式, 64 位寻址 CDS 归档 |
| **JDK 25** | LTS | 2025-09 | Scoped Values 正式, Compact Source Files, Compact Object Headers (实验), AOT 优化 |
| **JDK 26** | Feature | 2026-03 | HTTP/3, G1 吞吐量 +10-20%, AOT 对象缓存, Final 语义更严格 |

---

## 2. 语法速查 (Syntax)

### var -- 局部变量类型推断 (JDK 10+)

```java
var list = new ArrayList<String>();     // 推断为 ArrayList<String>
var map  = Map.of("a", 1, "b", 2);     // 推断为 Map<String, Integer>
var stream = list.stream();             // 推断为 Stream<String>

// 适用场景: 类型明显时使用
var response = client.send(request, BodyHandlers.ofString());

// 不适用: 类型不明显时保留显式声明
UserService service = createService();  // 比 var 更清晰
```

**限制**: 仅用于局部变量，不能用于字段、方法参数、返回类型。

### Switch Expressions (JDK 14+)

```java
// 箭头语法 (arrow syntax) + 表达式
int numLetters = switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> 6;
    case TUESDAY                -> 7;
    case THURSDAY, SATURDAY     -> 8;
    case WEDNESDAY              -> 9;
};

// yield 关键字用于块表达式
String result = switch (code) {
    case 200 -> "OK";
    case 404 -> "Not Found";
    default -> {
        log("Unknown code: " + code);
        yield "Unknown";
    }
};
```

### Text Blocks -- 多行字符串 (JDK 15+)

```java
// 三引号语法
String json = """
    {
      "name": "Alice",
      "age": 30
    }
    """;

String sql = """
    SELECT id, name, email
    FROM users
    WHERE status = 'ACTIVE'
    ORDER BY name
    """;

// 尾部的 """ 缩进决定公共前缀的去除量
```

### Records -- 不可变数据类 (JDK 16+)

```java
// 自动生成: 构造器, getter, equals, hashCode, toString
public record Point(int x, int y) { }

// 紧凑构造器 (compact constructor) 用于验证
public record Range(int min, int max) {
    public Range {
        if (min > max) throw new IllegalArgumentException("min > max");
    }
}

// 自定义方法
public record Person(String name, int age) {
    public boolean isAdult() { return age >= 18; }
}
```

### Sealed Classes -- 密封类 (JDK 17+)

```java
// 限制继承: 只有 permits 列出的类可以继承
public sealed interface Shape
    permits Circle, Rectangle, Triangle { }

public record Circle(double r) implements Shape { }
public record Rectangle(double w, double h) implements Shape { }
public non-sealed class Triangle implements Shape { /* 开放继承 */ }
```

### Pattern Matching (JDK 16+ instanceof, JDK 21+ switch)

```java
// instanceof 模式匹配 (JDK 16+)
if (obj instanceof String s && s.length() > 5) {
    System.out.println(s.toUpperCase());
}

// switch 模式匹配 (JDK 21+)
String describe(Object obj) {
    return switch (obj) {
        case Integer i when i > 0  -> "positive: " + i;
        case Integer i             -> "non-positive: " + i;
        case String s              -> "string: " + s;
        case Point(int x, int y)   -> "point(%d,%d)".formatted(x, y);
        case null                  -> "null";
        default                    -> obj.toString();
    };
}
```

### Record Patterns -- 解构 (JDK 21+)

```java
record Point(int x, int y) { }

// 直接解构 record 的组件
if (obj instanceof Point(int x, int y)) {
    System.out.println("x=" + x + ", y=" + y);
}

// 嵌套解构
record Line(Point start, Point end) { }
if (obj instanceof Line(Point(int x1, int y1), Point(int x2, int y2))) {
    // 直接访问 x1, y1, x2, y2
}
```

### Compact Source Files (JDK 25+)

```java
// 无需 class 声明的单文件程序
void main() {
    System.out.println("Hello!");
}

// 带参数
void main(String[] args) {
    for (var arg : args) {
        System.out.println(arg);
    }
}
```

```bash
java Hello.java  # 直接运行，无需 javac
```

### Module Import Declarations (JDK 25+)

```java
// 旧: 逐个导入
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.io.IOException;

// 新: 模块级导入
import module java.base;
// 一次导入整个模块的所有公开 API
```

---

## 3. API 速查 (Standard Library)

### 集合工厂方法 (JDK 9+)

```java
// 不可变集合创建 (immutable collections)
List<String> list     = List.of("a", "b", "c");
Set<String> set       = Set.of("a", "b", "c");
Map<String, Integer> map = Map.of("a", 1, "b", 2);

// 大 Map 用 ofEntries
Map<String, Integer> bigMap = Map.ofEntries(
    Map.entry("a", 1),
    Map.entry("b", 2),
    Map.entry("c", 3)
);

// 从可变集合转为不可变
List<String> immutable = List.copyOf(mutableList);
```

### Stream API 增强

```java
// Stream.toList() -- JDK 16+ (返回不可变 List)
List<String> result = stream.toList();

// takeWhile / dropWhile -- JDK 9+
list.stream()
    .takeWhile(s -> s.length() > 0)  // 取直到条件不满足
    .toList();

list.stream()
    .dropWhile(s -> s.startsWith("#"))  // 跳过直到条件不满足
    .toList();

// Stream.ofNullable -- JDK 9+
Stream.ofNullable(nullableValue)  // 空则返回空 Stream

// Collectors.teeing -- JDK 12+
var result = stream.collect(Collectors.teeing(
    Collectors.counting(),
    Collectors.summingInt(Integer::intValue),
    (count, sum) -> "count=%d, sum=%d".formatted(count, sum)
));

// Stream.mapMulti -- JDK 16+
stream.mapMulti((item, consumer) -> {
    if (item > 0) {
        consumer.accept(item);
        consumer.accept(item * 2);
    }
}).toList();
```

### String 新方法

```java
// JDK 11+
"  hello  ".strip();        // "hello" (Unicode 感知的 trim)
"  hello  ".stripLeading(); // "hello  "
"  hello  ".stripTrailing();// "  hello"
"".isBlank();               // true (空白检测)
"abc\ndef".lines();         // Stream<String> 按行分割
"ha".repeat(3);             // "hahaha"

// JDK 12+
"hello".indent(4);          // "    hello\n"
"hello".transform(s -> s.toUpperCase()); // "HELLO"

// JDK 15+
"hello".formatted();        // 等同于 String.format (实例方法)
"%s=%d".formatted("a", 1);  // "a=1"
```

### Optional 增强

```java
// JDK 9+
optional.ifPresentOrElse(
    val -> process(val),
    () -> handleEmpty()
);
optional.or(() -> Optional.of(defaultValue));
optional.stream();  // Optional → Stream (0 或 1 个元素)

// JDK 10+
var val = optional.orElseThrow();  // 无参版，抛 NoSuchElementException
```

### HttpClient (JDK 11+)

```java
// 创建客户端
HttpClient client = HttpClient.newBuilder()
    .connectTimeout(Duration.ofSeconds(5))
    .followRedirects(HttpClient.Redirect.NORMAL)
    .build();

// GET 请求
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .header("Accept", "application/json")
    .timeout(Duration.ofSeconds(10))
    .GET()
    .build();

// 同步发送
HttpResponse<String> response = client.send(
    request, HttpResponse.BodyHandlers.ofString()
);

// 异步发送
CompletableFuture<HttpResponse<String>> future =
    client.sendAsync(request, HttpResponse.BodyHandlers.ofString());

// POST JSON
HttpRequest postReq = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/users"))
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString("""
        {"name": "Alice", "age": 30}
        """))
    .build();
```

### java.time 常用操作 (JDK 8+)

```java
// 当前时间
LocalDate today      = LocalDate.now();           // 2026-03-22
LocalTime now        = LocalTime.now();            // 14:30:45
LocalDateTime ldt    = LocalDateTime.now();        // 2026-03-22T14:30:45
ZonedDateTime zdt    = ZonedDateTime.now();        // 带时区
Instant instant      = Instant.now();              // UTC 时间戳

// 创建
LocalDate date = LocalDate.of(2026, 3, 17);
LocalTime time = LocalTime.of(14, 30, 0);

// 格式化
DateTimeFormatter fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
String formatted = ldt.format(fmt);  // "2026-03-22 14:30:45"
LocalDateTime parsed = LocalDateTime.parse("2026-03-22 14:30:45", fmt);

// 计算
LocalDate nextWeek = today.plusWeeks(1);
LocalDate lastMonth = today.minusMonths(1);
long daysBetween = ChronoUnit.DAYS.between(date1, date2);
Period period = Period.between(date1, date2);      // 年月日差
Duration duration = Duration.between(time1, time2); // 时分秒差

// 时区转换
ZonedDateTime shanghai = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));
ZonedDateTime utc = shanghai.withZoneSameInstant(ZoneOffset.UTC);

// Instant ↔ 旧 Date 互转
Date oldDate = Date.from(instant);
Instant fromOld = oldDate.toInstant();
```

### Sequenced Collections (JDK 21+)

```java
// 统一的有序访问 API
SequencedCollection<String> seq = new LinkedHashSet<>();
seq.addFirst("first");
seq.addLast("last");
String first = seq.getFirst();
String last  = seq.getLast();
seq.reversed().forEach(System.out::println);

// SequencedMap
SequencedMap<String, Integer> map = new LinkedHashMap<>();
map.putFirst("a", 1);
map.putLast("z", 26);
var firstEntry = map.firstEntry();
var lastEntry  = map.lastEntry();
```

---

## 4. JVM 参数速查 (JVM Flags)

### 内存配置 (Memory)

```bash
-Xms4g                           # 初始堆大小 (initial heap)
-Xmx4g                           # 最大堆大小 (max heap)
-XX:MetaspaceSize=128m           # 初始 Metaspace (JDK 8+ 替代 PermGen)
-XX:MaxMetaspaceSize=256m        # 最大 Metaspace
-XX:+UseCompressedOops           # 压缩对象指针 (< 32GB 堆自动启用)
-XX:+UseCompressedClassPointers  # 压缩类指针
```

### GC 选择 (Garbage Collector)

```bash
# G1 GC -- 通用推荐 (JDK 9+ 默认)
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200          # 目标暂停时间
-XX:G1HeapRegionSize=32m          # Region 大小

# ZGC -- 极低延迟 (<1ms 暂停)
-XX:+UseZGC                       # JDK 15+ 不需要 UnlockExperimental
# JDK 23+ 分代模式已是默认，无需额外参数

# Shenandoah -- 低延迟
-XX:+UseShenandoahGC
-XX:ShenandoahGCMode=generational  # JDK 25+ 分代模式

# Parallel GC -- 最大吞吐量
-XX:+UseParallelGC
-XX:ParallelGCThreads=8
```

### 容器参数 (Container / Docker / Kubernetes)

```bash
-XX:+UseContainerSupport          # 默认启用，自动感知容器资源限制
-XX:MaxRAMPercentage=75.0         # 堆占容器内存的百分比
-XX:InitialRAMPercentage=50.0     # 初始堆占比
-XX:ActiveProcessorCount=4        # 覆盖 CPU 核心数检测
```

### AOT / CDS (启动优化)

```bash
# CDS 归档 (Class Data Sharing)
java -Xshare:dump -XX:SharedArchiveFile=app.jsa -jar app.jar
java -Xshare:on  -XX:SharedArchiveFile=app.jsa -jar app.jar

# AOT 缓存 (JDK 25+)
java -XX:AOTConfiguration=app.aotconf -jar app.jar   # 录制
java -XX:AOTCache=app.aot -XX:AOTConfiguration=app.aotconf -jar app.jar  # 生成
java -XX:AOTCache=app.aot -jar app.jar                # 使用

# AOT 对象缓存 (JDK 26+, 支持任意 GC)
java -XX:AOTCache=app.aot -jar app.jar
```

### JFR (Java Flight Recorder)

```bash
# 启动时开始录制
-XX:StartFlightRecording=settings=profile,filename=recording.jfr,duration=60s

# 持续录制 (生产环境)
-XX:StartFlightRecording=maxsize=100m,maxage=24h,disk=true,settings=profile

# 调整采样栈深度
-XX:FlightRecorderOptions=stackdepth=256
```

### 其他常用参数

```bash
# 启用预览特性
--enable-preview

# 模块系统兼容
--add-opens java.base/java.lang=ALL-UNNAMED
--add-exports java.base/sun.nio.ch=ALL-UNNAMED

# GC 日志 (统一日志格式, JDK 9+)
-Xlog:gc*,safepoint:file=gc.log:time,level,tags:filecount=5,filesize=10m

# 远程调试
-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005

# JMX 远程监控
-Dcom.sun.management.jmxremote
-Dcom.sun.management.jmxremote.port=9010
-Dcom.sun.management.jmxremote.authenticate=false
-Dcom.sun.management.jmxremote.ssl=false
```

---

## 5. GC 选择指南

### 对比表

| GC | 暂停时间 | 吞吐量 | 内存开销 | 适用场景 | 最低版本 |
|----|----------|--------|----------|----------|----------|
| **G1** | 50-200ms | 高 | 中 | 通用，默认推荐 | JDK 9 默认 |
| **ZGC** | <1ms | 中高 | 高 | 极低延迟，大堆 (>8GB) | JDK 15 正式 |
| **Shenandoah** | <10ms | 中高 | 中 | 低延迟 | JDK 15 正式 |
| **Parallel** | 较长 | 最高 | 低 | 批处理，吞吐量优先 | JDK 8+ |

### 选择决策树 (Decision Tree)

```
暂停时间要求 <1ms?
├── 是 → ZGC (-XX:+UseZGC)
└── 否
    ├── 暂停时间要求 <10ms? → Shenandoah (-XX:+UseShenandoahGC)
    └── 否
        ├── 吞吐量最重要? → Parallel (-XX:+UseParallelGC)
        └── 否 → G1 (-XX:+UseG1GC, 默认)
```

### JDK 26 GC 改进

| GC | JDK 26 改进 |
|----|-------------|
| G1 | JEP 522: 吞吐量 +10-20% (Claim Table 减少同步) |
| ZGC | 分代模式已为默认 (JDK 23 起) |
| Shenandoah | JEP 521: 分代模式 (实验性) |

---

## 6. 诊断命令速查 (Diagnostic Tools)

### jcmd -- 通用诊断 (推荐)

```bash
# 列出所有 Java 进程
jcmd -l

# 查看 JVM 信息
jcmd <pid> VM.info
jcmd <pid> VM.version
jcmd <pid> VM.flags               # 查看所有 JVM 参数
jcmd <pid> VM.system_properties   # 系统属性

# GC 诊断
jcmd <pid> GC.heap_info           # 堆信息
jcmd <pid> GC.run                 # 触发 Full GC
jcmd <pid> GC.class_histogram     # 类直方图 (内存占用)

# 线程诊断
jcmd <pid> Thread.print           # 打印线程堆栈 (等同 jstack)

# JFR 操作
jcmd <pid> JFR.start name=rec settings=profile duration=60s filename=rec.jfr
jcmd <pid> JFR.dump name=rec filename=dump.jfr
jcmd <pid> JFR.stop name=rec

# 编译器诊断
jcmd <pid> Compiler.queue         # JIT 编译队列
jcmd <pid> Compiler.codecache     # 代码缓存状态
```

### jstack -- 线程堆栈 (Thread Dump)

```bash
# 打印线程堆栈
jstack <pid>

# 包含锁信息
jstack -l <pid>

# 输出到文件
jstack -l <pid> > threaddump.txt

# 检测死锁
jstack <pid> | grep -A5 "Found.*deadlock"
```

### jmap -- 内存分析 (Heap)

```bash
# 堆信息摘要
jmap -heap <pid>

# 堆直方图 (不触发 GC)
jmap -histo <pid> | head -20

# 堆直方图 (触发 GC)
jmap -histo:live <pid> | head -20

# 导出堆转储 (heap dump)
jmap -dump:format=b,file=heapdump.hprof <pid>
jmap -dump:live,format=b,file=heapdump.hprof <pid>  # 仅存活对象

# JDK 11+ 推荐使用 jcmd 替代
jcmd <pid> GC.heap_dump heapdump.hprof
```

### jfr -- Flight Recorder 分析

```bash
# 命令行录制
jfr record --duration 60s --filename recording.jfr MainClass

# 打印录制内容
jfr print recording.jfr
jfr print --events jdk.GCHeapSummary recording.jfr
jfr print --events jdk.ThreadSleep recording.jfr

# 查看元数据
jfr metadata recording.jfr

# 摘要
jfr summary recording.jfr

# 查看特定事件
jfr print --events jdk.CPULoad recording.jfr
jfr print --events jdk.GarbageCollection recording.jfr
```

### jstat -- GC 统计

```bash
# GC 统计 (每 1 秒, 共 10 次)
jstat -gcutil <pid> 1000 10

# 输出列: S0 S1 E O M CCS YGC YGCT FGC FGCT GCT
# S0/S1: Survivor 区使用率
# E: Eden 区使用率
# O: Old 区使用率
# M: Metaspace 使用率
# YGC/FGC: Young/Full GC 次数
# YGCT/FGCT/GCT: 各阶段累计 GC 时间 (秒)

# GC 容量详情
jstat -gc <pid> 1000

# Metaspace 容量
jstat -gcmetacapacity <pid>
```

### jconsole -- 可视化监控

```bash
# 启动 GUI 监控工具
jconsole <pid>
jconsole <host>:<port>  # 远程连接

# 功能: 内存、线程、类、MBean 监控
# 需要 JMX 支持 (图形界面)
```

### jdeps / jdeprscan -- 依赖分析

```bash
# 分析 JDK 内部 API 依赖
jdeps --jdk-internals myapp.jar

# 多版本分析
jdeps --multi-release 17 --ignore-missing-deps myapp.jar

# 废弃 API 扫描
jdeprscan --release 21 myapp.jar
jdeprscan --release 21 --for-removal myapp.jar
```

### jlink -- 自定义运行时 (Custom Runtime)

```bash
# 创建最小化 JRE (只包含需要的模块)
jlink --module-path $JAVA_HOME/jmods \
      --add-modules java.base,java.sql,java.net.http \
      --output custom-jre \
      --strip-debug \
      --compress zip-6

# 使用自定义 JRE
./custom-jre/bin/java -jar myapp.jar
```

---

## 7. JDK 26 新特性速查

### 正式特性 (Final)

| JEP | 特性 | 说明 |
|-----|------|------|
| 517 | HTTP/3 | HttpClient 支持 QUIC 协议，会话恢复时 0-RTT |
| 522 | G1 GC 吞吐量提升 | 减少同步开销，特定工作负载 +10-20% |
| 516 | AOT 对象缓存 | 支持任意 GC 的 AOT 缓存 |
| 500 | Final 语义更严格 | 禁止反射修改 final 字段 |
| 504 | 移除 Applet API | java.applet 包完全移除 |

### 预览特性 (Preview, 需要 `--enable-preview`)

| JEP | 特性 | 预览次数 |
|-----|------|----------|
| 525 | Structured Concurrency 结构化并发 | 第 6 次 |
| 530 | Primitive Types in Patterns 原始类型模式匹配 | 第 4 次 |
| 526 | Lazy Constants 延迟常量 | 第 2 次 |
| 524 | PEM Encodings PEM 编解码 | 第 2 次 |

### 孵化特性 (Incubator)

| JEP | 特性 | 孵化次数 |
|-----|------|----------|
| 529 | Vector API 向量 API | 第 11 次 |

---

## 8. 常用代码片段

### HTTP/3 客户端 (JDK 26)

```java
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3)
    .connectTimeout(Duration.ofSeconds(10))
    .build();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com"))
    .build();

HttpResponse<String> response = client.send(
    request, HttpResponse.BodyHandlers.ofString()
);
System.out.println("Protocol: " + response.version());
```

### Scoped Values (JDK 25+)

```java
static final ScopedValue<String> USER = ScopedValue.newInstance();

// 在作用域内绑定值
ScopedValue.where(USER, "alice").run(() -> {
    System.out.println(USER.get()); // "alice"
    // 子虚拟线程也可以访问
    Thread.ofVirtual().start(() -> {
        System.out.println(USER.get()); // "alice"
    });
});
```

### 结构化并发 (JDK 26 预览)

```java
try (var scope = StructuredTaskScope.open(Joiner.allSuccessfulOrThrow())) {
    Subtask<String> user = scope.fork(() -> fetchUser());
    Subtask<List<Order>> orders = scope.fork(() -> fetchOrders());

    scope.join();

    return new Response(user.get(), orders.get());
}  // 自动关闭，取消未完成的任务
```

### Virtual Threads (JDK 21+)

```java
// 创建虚拟线程
Thread vthread = Thread.ofVirtual().start(() -> {
    System.out.println("Hello from virtual thread");
});

// 虚拟线程池
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 100_000; i++) {
        executor.submit(() -> processRequest());
    }
}
```

### KDF 密钥派生 (JDK 25+)

```java
KDF kdf = KDF.getInstance("HKDF-SHA256");

HKDFParameterSpec params = HKDFParameterSpec.ofExtract()
    .addSalt(salt)
    .extract(ikm)
    .expand(info, 32);

SecretKey key = kdf.deriveKey("AES", params);
```

### PEM 编解码 (JDK 26 预览)

```java
// 编码
PEMEncoder encoder = new PEMEncoder();
String pem = encoder.encode(privateKey);

// 解码
PEMDecoder decoder = new PEMDecoder();
PrivateKey key = decoder.decode(pem, PrivateKey.class);
```

### Stable Value (JDK 25 预览)

```java
// 线程安全的延迟初始化，无需 volatile + double-check locking
private final StableValue<Logger> logger = StableValue.of();

public Logger getLogger() {
    return logger.orElseSet(() -> Logger.getLogger("MyApp"));
}
```

### 常用集合操作合集

```java
// 不可变集合 (JDK 9+)
var list = List.of("a", "b", "c");
var set  = Set.of("x", "y");
var map  = Map.of("k", 1);

// Stream → 不可变 List (JDK 16+)
var result = stream.toList();

// Sequenced Collections (JDK 21+)
var seq = new LinkedHashSet<String>();
seq.addFirst("first");
seq.addLast("last");
seq.getFirst();
seq.getLast();
seq.reversed();
```
