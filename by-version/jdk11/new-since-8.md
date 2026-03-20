# JDK 11 新特性（相比 JDK 8）

> **覆盖版本**: JDK 9、10、11 | **对比基准**: JDK 8u401 → JDK 11.0.20

---

## 模块系统 (JPMS) - JDK 9

### Java Platform Module System (JEP 261)

**核心概念**:
- **模块**: 具有名称、依赖和导出的代码单元
- **模块路径**: 替代类路径的模块化部署
- **强封装**: 显式声明导出的包

**module-info.java 示例**:
```java
module com.example.app {
    requires java.sql;
    requires com.fasterxml.jackson.databind;
    exports com.example.api;
    opens com.example.internal to com.example.test;
}
```

**关键命令**:
```bash
# 编译模块
javac --module-path lib -d out $(find src -name "*.java") module-info.java

# 运行模块
java --module-path out:lib -m com.example.app/com.example.Main

# 创建自定义运行时
jlink --module-path $JAVA_HOME/jmods:mods --add-modules com.example.app --output myruntime
```

### 模块化 JDK

**结构变化**:
- 原有 `rt.jar` 拆分为 75 个模块
- 核心模块: `java.base`, `java.sql`, `java.xml`
- 移除: Java EE 和 CORBA 模块

**影响**:
- 需要显式声明依赖
- 内部 API 访问受限
- 减少运行时大小

---

## 语言特性

### JDK 9 语言增强

1. **接口私有方法**:
```java
interface Calculator {
    default int add(int a, int b) {
        return a + b;
    }
    
    default int multiply(int a, int b) {
        return a * b;
    }
    
    // 私有方法 - 内部实现细节
    private void log(String message) {
        System.out.println(message);
    }
}
```

2. **try-with-resources 改进**:
```java
// JDK 8: 需要显式变量
try (BufferedReader br = new BufferedReader(new FileReader("file.txt"))) {
    // 使用 br
}

// JDK 9: 可以使用 final 或 effectively final 变量
BufferedReader br = new BufferedReader(new FileReader("file.txt"));
try (br) {  // br 是 effectively final
    // 使用 br
}
```

3. **钻石操作符增强**:
```java
// JDK 8: 匿名内部类不支持钻石操作符
List<String> list = new ArrayList<>() {  // 编译错误
    // 匿名类体
};

// JDK 9: 支持匿名内部类的钻石操作符
List<String> list = new ArrayList<>() {
    // 匿名类体 - 正常工作
};
```

4. **@SafeVarargs 应用于私有实例方法**:
```java
class Example {
    @SafeVarargs  // JDK 9: 允许在私有实例方法上使用
    private void safeMethod(List<String>... lists) {
        // 方法实现
    }
}
```

### JDK 10 语言增强

1. **局部变量类型推断 (JEP 286)**:
```java
// 使用 var 关键字
var list = new ArrayList<String>();  // ArrayList<String>
var stream = list.stream();          // Stream<String>
var path = Paths.get("file.txt");    // Path

// 限制: 必须初始化，不能为 null
var x;  // 编译错误: 需要初始化
var y = null;  // 编译错误: 无法推断类型
```

2. **应用场景**:
```java
// 减少样板代码
try (var input = new FileInputStream("file.txt");
     var output = new FileOutputStream("output.txt")) {
    // 自动推断类型
}

// 增强 for 循环
for (var item : collection) {
    // item 类型自动推断
}

// Lambda 参数
list.stream()
    .map((var s) -> s.toUpperCase())  // 显式 var 语法
    .collect(Collectors.toList());
```

### JDK 11 语言增强

1. **局部变量语法用于 Lambda 参数 (JEP 323)**:
```java
// 允许在 Lambda 参数中使用 var
(var x, var y) -> x + y

// 一致性: 所有参数必须使用 var
(var x, y) -> x + y  // 编译错误: 混合语法
```

2. **嵌套基于访问控制 (JEP 181)**:
- 简化私有成员访问
- 减少合成访问方法
- 改进反射性能

---

## API 增强

### JDK 9 集合工厂方法

**不可变集合创建**:
```java
// 列表
List<String> list = List.of("a", "b", "c");
List<String> emptyList = List.of();

// 集合
Set<String> set = Set.of("a", "b", "c");

// 映射
Map<String, Integer> map = Map.of("a", 1, "b", 2);
Map<String, Integer> map2 = Map.ofEntries(
    Map.entry("a", 1),
    Map.entry("b", 2)
);
```

**特性**:
- 不可变 (Immutable)
- 空值不允许 (`NullPointerException`)
- 序列化友好

### JDK 9 Stream API 增强

1. **takeWhile/dropWhile**:
```java
List<Integer> numbers = List.of(1, 2, 3, 4, 5, 4, 3, 2, 1);

// takeWhile: 从开始取元素直到条件不满足
List<Integer> taken = numbers.stream()
    .takeWhile(n -> n < 4)  // [1, 2, 3]
    .collect(Collectors.toList());

// dropWhile: 从开始丢弃元素直到条件不满足
List<Integer> dropped = numbers.stream()
    .dropWhile(n -> n < 4)  // [4, 5, 4, 3, 2, 1]
    .collect(Collectors.toList());
```

2. **iterate 重载**:
```java
// JDK 8: 无限流
Stream.iterate(0, n -> n + 1)  // 0, 1, 2, 3, ...

// JDK 9: 有限流
Stream.iterate(0, n -> n < 10, n -> n + 1)  // 0, 1, 2, ..., 9
```

3. **ofNullable**:
```java
// 创建单元素流，null 时返回空流
Stream<String> stream = Stream.ofNullable(getNullableString());
```

### JDK 10 Optional 增强

**orElseThrow()**:
```java
// 替代 get()，更清晰的语义
String value = optional.orElseThrow();  // 无参版本

// 等价于
String value = optional.orElseThrow(
    () -> new NoSuchElementException("No value present")
);
```

### JDK 11 字符串增强

**新方法**:
```java
// 检查空白 (比 trim() 更准确)
boolean blank = "   ".isBlank();  // true

// 去除首尾空白 (Unicode 感知)
String stripped = "  hello  ".strip();  // "hello"

// 去除首部空白
String leading = "  hello".stripLeading();  // "hello"

// 去除尾部空白  
String trailing = "hello  ".stripTrailing();  // "hello"

// 重复字符串
String repeated = "Java ".repeat(3);  // "Java Java Java "

// 行流
String text = "line1\nline2\nline3";
long lineCount = text.lines().count();  // 3
```

---

## HTTP 客户端 (JEP 321) - JDK 11

### 从实验性到标准

**特性**:
- 同步和异步模式
- HTTP/1.1 和 HTTP/2 支持
- WebSocket 支持
- 响应式流

### 基本使用

```java
import java.net.http.*;
import java.net.URI;

// 同步请求
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .header("Accept", "application/json")
    .GET()
    .build();

HttpResponse<String> response = client.send(request, 
    HttpResponse.BodyHandlers.ofString());

System.out.println("Status: " + response.statusCode());
System.out.println("Body: " + response.body());

// 异步请求
CompletableFuture<HttpResponse<String>> future = client
    .sendAsync(request, HttpResponse.BodyHandlers.ofString());

future.thenApply(HttpResponse::body)
      .thenAccept(System.out::println)
      .join();
```

### 高级特性

```java
// 自定义客户端
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .connectTimeout(Duration.ofSeconds(10))
    .followRedirects(HttpClient.Redirect.NORMAL)
    .proxy(ProxySelector.of(new InetSocketAddress("proxy.example.com", 8080)))
    .authenticator(Authenticator.getDefault())
    .build();

// 发送 JSON 数据
String json = "{\"name\":\"John\",\"age\":30}";
HttpRequest postRequest = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/users"))
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString(json))
    .build();

// 处理响应流
HttpRequest streamingRequest = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/stream"))
    .GET()
    .build();

client.send(streamingRequest, HttpResponse.BodyHandlers.ofLines())
      .body()
      .forEach(System.out::println);
```

---

## 垃圾收集器增强

### ZGC (JEP 333) - JDK 11

**设计目标**:
- 亚毫秒级暂停时间 (<10ms)
- 处理大堆 (TB 级)
- 最小吞吐量影响 (<15%)

**启用**:
```bash
# Linux/macOS
java -XX:+UseZGC -Xmx16g -jar app.jar

# 调优参数
-XX:+UseZGC
-XX:+UnlockExperimentalVMOptions
-XX:MaxGCPauseMillis=10
-XX:ConcGCThreads=4
-XX:ZAllocationSpikeTolerance=2.0
```

**监控**:
```bash
# GC 日志
-Xlog:gc*,safepoint:file=gc.log:time,level,tags

# ZGC 特定日志
-Xlog:gc+heap=debug,gc+phases=debug
```

### Shenandoah GC (JEP 189) - JDK 12 (JDK 11 可 backport)

**特点**:
- 并发压缩
- 低暂停时间
- 适用于大堆

**启用**:
```bash
java -XX:+UseShenandoahGC -jar app.jar
```

### Epsilon GC (JEP 318) - JDK 11

**无操作垃圾收集器**:
- 不进行垃圾回收
- 用于性能测试和短期任务

**使用场景**:
```bash
# 性能测试基准
java -XX:+UseEpsilonGC -Xmx1g -jar benchmark.jar

# 短期任务
java -XX:+UseEpsilonGC -Xmx100m -jar short-task.jar
```

### G1 增强

**JDK 9 改进**:
- 并行 Full GC (JEP 307)
- 更精确的暂停时间预测

**JDK 10 改进**:
- 并行 Full GC 优化
- 应用线程并行化

**JDK 11 改进**:
- 自动堆大小调整优化
- 改进的混合垃圾收集

---

## 工具和诊断

### Java Flight Recorder (JFR) - JDK 11

**从商业特性变为开源**:
- 生产环境性能分析
- 低开销 (<1%)
- 事件流 API

**启用**:
```bash
# 启动时记录
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr -jar app.jar

# 动态记录
jcmd <pid> JFR.start duration=60s filename=recording.jfr
jcmd <pid> JFR.dump filename=recording.jfr
jcmd <pid> JFR.stop
```

**分析**:
```bash
# 命令行分析
jfr print recording.jfr

# 使用 JDK Mission Control (JMC)
jmc recording.jfr
```

### 统一日志系统 (JEP 158) - JDK 9

**统一日志格式**:
```bash
# 启用统一日志
-Xlog:gc*,safepoint:file=gc.log:time,level,tags

# 详细配置
-Xlog:all=warning:stdout:uptime,level,tags
-Xlog:gc=debug:file=gc.log:time,pid,tid,level
-Xlog:class+load=info,class+unload=warning
```

### jshell (JEP 222) - JDK 9

**交互式 Java REPL**:
```bash
# 启动 jshell
jshell

# 示例使用
jshell> String greeting = "Hello, World!"
greeting ==> "Hello, World!"

jshell> void printGreeting(String name) {
   ...>     System.out.println("Hello, " + name);
   ...> }
|  创建了方法 printGreeting(String)

jshell> printGreeting("Java")
Hello, Java

jshell> /exit
```

### 新的打包工具 (JEP 343) - JDK 14 (未来方向)

**注意**: 实际在 JDK 14 引入，但 JDK 11 用户需要了解趋势

```bash
# 创建自包含应用
jpackage --name MyApp --input lib --main-jar app.jar --main-class com.example.Main
```

---

## 安全性增强

### TLS 1.3 (JEP 332) - JDK 11

**新特性**:
- 1-RTT 握手 (0-RTT 可选)
- 增强的前向安全性
- 简化密码套件

**启用**:
```java
// 编程方式启用
SSLContext sslContext = SSLContext.getInstance("TLSv1.3");
sslContext.init(null, null, null);

// 系统属性
-Djdk.tls.client.protocols=TLSv1.3
```

### 加密算法更新

**新增**:
- ChaCha20 和 Poly1305 算法
- SHA-3 哈希函数支持

**废弃/移除**:
- RC4 流密码
- DES、3DES (部分模式)
- MD5 签名

### 安全性管理器改进

**更细粒度的控制**:
- 模块化权限检查
- 改进的策略文件语法
- 动态权限管理

---

## 移除和废弃

### 已移除的组件

| 组件 | 移除版本 | 替代方案 |
|------|----------|----------|
| Java EE 模块 | JDK 9 | 单独下载或 Maven 依赖 |
| CORBA 模块 | JDK 11 | 无，使用其他 RPC 技术 |
| JavaFX | JDK 11 | 单独下载 |
| Nashorn JavaScript | JDK 15 | GraalVM JavaScript |
| Pack200 | JDK 11 | 标准压缩算法 |

### 已废弃的 API

| API | 废弃版本 | 建议替代 |
|-----|----------|----------|
| `finalize()` 方法 | JDK 9 | `Cleaner` API, `try-with-resources` |
| `Thread.stop()` | JDK 1.2 | 中断机制 |
| `Thread.suspend()` | JDK 1.2 | 并发工具类 |
| `Runtime.runFinalizersOnExit()` | JDK 1.2 | `ShutdownHook` |

---

## 性能改进

### 启动性能

**类数据共享 (CDS) 增强**:
```bash
# 创建共享归档
java -Xshare:dump -XX:SharedArchiveFile=app.jsa -jar app.jar

# 使用共享归档
java -Xshare:on -XX:SharedArchiveFile=app.jsa -jar app.jar

# 应用类共享
java -XX:SharedArchiveFile=app.jsa -Xshare:auto -jar app.jar
```

**AOT 编译 (实验性)**:
```bash
# 生成 AOT 库
jaotc --output libApp.so --module java.base --module app.module

# 使用 AOT 库
java -XX:AOTLibrary=./libApp.so -jar app.jar
```

### 运行时性能

**字符串压缩**:
- 从 `char[]` 到 `byte[]` 的压缩存储
- 拉丁-1 字符减少 50% 内存
- 自动检测和转换

**改进的容器支持**:
```bash
# 自动检测容器限制
-XX:+UseContainerSupport  # 默认启用

# 基于百分比的内存配置
-XX:MaxRAMPercentage=75.0
-XX:InitialRAMPercentage=50.0
```

---

## 迁移建议

### 逐步迁移策略

1. **第一阶段: 类路径模式**
```bash
# 使用 --class-path 而非 --module-path
java --class-path app.jar:lib/* com.example.Main
```

2. **第二阶段: 自动模块**
```java
// 简单的 module-info.java
module com.example.app {
    requires java.base;
    // 自动模块依赖
}
```

3. **第三阶段: 完全模块化**
- 分析依赖关系
- 设计模块边界
- 重构包结构

### 兼容性工具

1. **jdeps** - 依赖分析:
```bash
jdeps --multi-release 11 --ignore-missing-deps app.jar
jdeps -jdkinternals app.jar
```

2. **jdeprscan** - 废弃 API 扫描:
```bash
jdeprscan --release 11 --for-removal app.jar
```

3. **jlink** - 创建自定义运行时:
```bash
jlink --module-path $JAVA_HOME/jmods:mods \
      --add-modules java.base,java.sql,com.example.app \
      --output custom-jre
```

---

## 资源

### 官方文档
- [JDK 11 发布说明](https://openjdk.org/projects/jdk/11/)
- [从 JDK 8 迁移指南](https://docs.oracle.com/en/java/javase/11/migrate/)
- [模块系统快速入门](https://openjdk.org/projects/jigsaw/quick-start)

### 性能指南
- [ZGC 调优指南](https://wiki.openjdk.org/display/zgc)
- [G1 GC 调优指南](https://docs.oracle.com/javase/9/gctuning/g1-garbage-collector.htm)
- [JFR 文档](https://docs.oracle.com/javacomponents/jmc-5-5/jfr-runtime-guide/about.htm)

### 社区资源
- [Java Champions 博客](https://inside.java/)
- [Java Magazine](https://blogs.oracle.com/javamagazine/)
- [Stack Overflow JDK 11 标签](https://stackoverflow.com/questions/tagged/java-11)