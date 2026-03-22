# JDK 版本迁移实战指南

从 JDK 8 到 JDK 26 的完整迁移路径，覆盖每个 LTS 跳转的破坏性变更、迁移命令和常见报错解决方案。

---
## 目录

1. [迁移工具总览](#1-迁移工具总览)
2. [JDK 8 → 11: 模块化革命](#2-jdk-8--11-模块化革命)
3. [JDK 11 → 17: 强封装与现代语法](#3-jdk-11--17-强封装与现代语法)
4. [JDK 17 → 21: 虚拟线程时代](#4-jdk-17--21-虚拟线程时代)
5. [JDK 21 → 25: LTS 到 LTS](#5-jdk-21--25-lts-到-lts)
6. [JDK 25 → 26: 功能版本升级](#6-jdk-25--26-功能版本升级)

> **常见直升路径**: 从 JDK 17 直接升级到 JDK 25？请参考 [JDK 17→25 LTS 直升指南](/by-version/jdk25/migration/from-17.md)，整合了第 4、5 节的所有破坏性变更和新特性。
7. [通用升级步骤](#7-通用升级步骤)
8. [回滚计划](#8-回滚计划)
9. [检查清单](#9-检查清单)

---

## 1. 迁移工具总览

升级前必须使用的诊断工具 (diagnostic tools):

### jdeps -- 依赖分析 (dependency analysis)

```bash
# 检查对 JDK 内部 API 的依赖
jdeps --jdk-internals myapp.jar

# 指定目标版本分析
jdeps --multi-release 17 --ignore-missing-deps myapp.jar

# 生成模块描述符
jdeps --generate-module-info . myapp.jar

# 输出依赖关系图 (dependency graph)
jdeps -dotoutput deps --multi-release 11 myapp.jar
```

输出示例:
```
myapp.jar -> java.base
myapp.jar -> jdk.unsupported
  com.example.util.FastAccess -> sun.misc.Unsafe  JDK internal API (jdk.unsupported)
```

### jdeprscan -- 废弃 API 检查 (deprecated API scan)

```bash
# 扫描已标记为移除的 API
jdeprscan --release 17 --for-removal myapp.jar

# 扫描所有废弃 API
jdeprscan --release 21 myapp.jar
```

### 风险评估矩阵 (risk matrix)

| 风险级别 | 场景 | 建议 |
|----------|------|------|
| 低 | 仅使用标准公开 API | 直接升级，运行测试 |
| 中 | 使用已废弃 API 或 --add-opens | 先替换废弃 API，再升级 |
| 高 | 依赖内部 API (sun.misc.*) 或反射修改 final | 需要重构代码 |

---

## 2. JDK 8 → 11: 模块化革命

> **迁移复杂度**: 高 | **建议时间**: 4-8 周 | **关键变革**: JPMS 模块系统 (JEP 261)

### 2.1 模块系统影响 (Module System / JPMS)

JDK 9 引入 Java Platform Module System (JPMS, JEP 261)，JDK 11 是第一个包含模块系统的 LTS。

**类路径模式 (classpath mode) -- 推荐初始迁移**:
```bash
# 不使用模块系统，保持类路径方式运行
java --class-path app.jar:lib/* com.example.Main
```

**处理内部 API 访问**:
```bash
# 允许反射访问被封装的内部 API
java --add-opens java.base/sun.misc=ALL-UNNAMED \
     --add-opens java.base/java.lang=ALL-UNNAMED \
     -jar app.jar

# 允许代码访问非导出包
java --add-exports java.base/sun.nio.ch=ALL-UNNAMED -jar app.jar
```

**常见报错**:
```bash
# 报错: InaccessibleObjectException
java.lang.reflect.InaccessibleObjectException:
  Unable to make field private final ... accessible

# 解决: 添加 --add-opens 参数
--add-opens java.base/java.lang=ALL-UNNAMED

# 报错: module not found
Error: module not found: java.xml.bind

# 解决: 添加 Maven 依赖 (见下方 Java EE 移除)
```

### 2.2 Java EE 模块移除 (JEP 320)

JDK 11 移除了以下内置 Java EE 模块:

| 移除的模块 | 影响 | Maven 替代依赖 |
|------------|------|----------------|
| `java.xml.bind` (JAXB) | XML 绑定 | `javax.xml.bind:jaxb-api:2.3.1` + `com.sun.xml.bind:jaxb-impl:2.3.1` |
| `java.xml.ws` (JAX-WS) | Web Service | `com.sun.xml.ws:jaxws-ri:2.3.3` |
| `java.activation` (JAF) | 激活框架 | `javax.activation:javax.activation-api:1.2.0` |
| `java.xml.ws.annotation` | 注解 | `javax.annotation:javax.annotation-api:1.3.2` |
| `java.corba` (CORBA) | 远程调用 | 迁移到 gRPC 或 REST |
| `java.transaction` (JTA) | 事务 | `javax.transaction:javax.transaction-api:1.3` |

**Maven 依赖添加示例**:
```xml
<!-- JAXB 替代 -->
<dependency>
    <groupId>javax.xml.bind</groupId>
    <artifactId>jaxb-api</artifactId>
    <version>2.3.1</version>
</dependency>
<dependency>
    <groupId>com.sun.xml.bind</groupId>
    <artifactId>jaxb-impl</artifactId>
    <version>2.3.1</version>
</dependency>

<!-- JAF 替代 -->
<dependency>
    <groupId>javax.activation</groupId>
    <artifactId>javax.activation-api</artifactId>
    <version>1.2.0</version>
</dependency>

<!-- JAX-WS 替代 -->
<dependency>
    <groupId>com.sun.xml.ws</groupId>
    <artifactId>jaxws-ri</artifactId>
    <version>2.3.3</version>
    <type>pom</type>
</dependency>
```

### 2.3 其他重要 API 变更

| 移除/变更的 API | 替代方案 |
|-----------------|----------|
| `sun.misc.BASE64Encoder` | `java.util.Base64` |
| `sun.misc.Unsafe` (受限访问) | `java.lang.invoke.VarHandle` |
| `com.sun.image.codec.jpeg` | `javax.imageio.ImageIO` |
| Nashorn JavaScript 引擎 (JEP 335 废弃) | GraalVM JavaScript 或纯 Java 逻辑 |
| `-XX:PermSize` / `-XX:MaxPermSize` | `-XX:MetaspaceSize` / `-XX:MaxMetaspaceSize` |

```java
// 旧: sun.misc.BASE64Encoder
sun.misc.BASE64Encoder encoder = new sun.misc.BASE64Encoder();
String encoded = encoder.encode(data);

// 新: java.util.Base64
String encoded = Base64.getEncoder().encodeToString(data);
```

### 2.4 Security Manager 变化

JDK 11 中 Security Manager 仍正常工作，但 TLS 配置有重要变更:

```bash
# TLS 1.3 支持 (JDK 11 新增)
-Djdk.tls.client.protocols=TLSv1.2,TLSv1.3

# 容器支持 (Docker/Kubernetes)
-XX:+UseContainerSupport          # 默认启用
-XX:MaxRAMPercentage=75.0         # 堆内存占容器内存的比例
-XX:InitialRAMPercentage=50.0
```

### 2.5 JVM 参数迁移

| JDK 8 参数 | JDK 11 状态 | 替代方案 |
|------------|-------------|----------|
| `-XX:+AggressiveOpts` | 已移除 | 使用默认优化 |
| `-XX:+UseConcMarkSweepGC` | 已废弃 | `-XX:+UseG1GC` 或 `-XX:+UseZGC` |
| `-XX:+UseParNewGC` | 已废弃 | `-XX:+UseG1GC` |
| `-Xincgc` | 已移除 | `-XX:+UseG1GC` |
| `-XX:PermSize` | 已移除 | `-XX:MetaspaceSize` |
| `-XX:MaxPermSize` | 已移除 | `-XX:MaxMetaspaceSize` |

```bash
# GC 日志格式从 -XX:+PrintGCDetails 变为统一日志
# 旧
-XX:+PrintGCDetails -XX:+PrintGCDateStamps -Xloggc:gc.log

# 新
-Xlog:gc*,safepoint:file=gc.log:time,level,tags:filecount=5,filesize=10m
```

### 2.6 构建配置更新

```xml
<!-- Maven pom.xml -->
<properties>
    <maven.compiler.source>11</maven.compiler.source>
    <maven.compiler.target>11</maven.compiler.target>
    <maven.compiler.release>11</maven.compiler.release>
</properties>

<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.10.0</version>
    <configuration>
        <release>11</release>
    </configuration>
</plugin>
```

```groovy
// Gradle build.gradle
java {
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11
}

tasks.withType(JavaCompile) {
    options.compilerArgs += ['--release', '11']
}
```

### 2.7 第三方库最低版本

| 库/框架 | JDK 11 最小版本 |
|---------|-----------------|
| Spring Framework | 5.1+ |
| Spring Boot | 2.1+ |
| Hibernate | 5.4+ |
| Jackson | 2.10+ |
| Log4j | 2.11+ (Log4j 1.x 不兼容) |
| Apache HttpClient | 4.5+ |

---

## 3. JDK 11 → 17: 强封装与现代语法

> **迁移复杂度**: 中 | **建议时间**: 2-4 周 | **关键变革**: 强封装 (JEP 396/403), Records, Sealed Classes

### 3.1 强封装 (Strong Encapsulation)

**JEP 396 (JDK 16) + JEP 403 (JDK 17): `--illegal-access` 变化**:

| 版本 | `--illegal-access` 默认值 | 行为 |
|------|--------------------------|------|
| JDK 9-15 | `permit` | 允许反射访问内部 API，首次访问打印警告 |
| JDK 16 (JEP 396) | `deny` | 默认拒绝，需要显式 `--add-opens` |
| JDK 17 (JEP 403) | 参数移除 | `--illegal-access` 参数本身被移除 |

**常见报错**:
```bash
# 报错: JDK 17 中 --illegal-access 无效
OpenJDK 64-Bit Server VM warning:
  Option --illegal-access is no longer supported.

# 解决: 移除 --illegal-access=permit，改用 --add-opens
java --add-opens java.base/java.lang=ALL-UNNAMED \
     --add-opens java.base/java.lang.reflect=ALL-UNNAMED \
     --add-opens java.base/sun.nio.ch=ALL-UNNAMED \
     -jar app.jar
```

**影响最大的框架**: Spring (4.x 无法在 JDK 17 上运行), Hibernate (5.2 以下), Mockito (旧版本)

### 3.2 Records -- 不可变数据类 (JEP 395, JDK 16 正式)

```java
// JDK 11: 手动编写样板代码 (boilerplate)
public class Person {
    private final String name;
    private final int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String name() { return name; }
    public int age() { return age; }

    @Override public boolean equals(Object o) { /* ... */ }
    @Override public int hashCode() { /* ... */ }
    @Override public String toString() { /* ... */ }
}

// JDK 17: Record 自动生成 equals/hashCode/toString
public record Person(String name, int age) {
    // 紧凑构造器 (compact constructor) 用于验证
    public Person {
        if (age < 0) throw new IllegalArgumentException("age < 0");
    }

    // 可以添加方法
    public boolean isAdult() { return age >= 18; }
}
```

### 3.3 Sealed Classes -- 受控继承 (JEP 409, JDK 17 正式)

```java
// 密封接口: 只允许指定的子类
public sealed interface Shape
    permits Circle, Rectangle, Triangle { }

public record Circle(double radius) implements Shape { }
public record Rectangle(double w, double h) implements Shape { }
public non-sealed class Triangle implements Shape { /* ... */ }

// 配合 pattern matching 使用
double area = switch (shape) {
    case Circle c    -> Math.PI * c.radius() * c.radius();
    case Rectangle r -> r.w() * r.h();
    case Triangle t  -> /* ... */;
    // 编译器知道所有情况已覆盖，无需 default
};
```

### 3.4 Text Blocks -- 多行字符串 (JEP 378, JDK 15 正式)

```java
// JDK 11: 字符串拼接
String json = "{\n" +
    "  \"name\": \"Alice\",\n" +
    "  \"age\": 30\n" +
    "}";

// JDK 17: Text Block
String json = """
    {
      "name": "Alice",
      "age": 30
    }
    """;
```

### 3.5 Pattern Matching for instanceof (JEP 394, JDK 16 正式)

```java
// JDK 11: 需要显式转换
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.length());
}

// JDK 17: 绑定变量 (binding variable)
if (obj instanceof String s) {
    System.out.println(s.length());
}

// 可以带条件
if (obj instanceof String s && s.length() > 5) {
    System.out.println("Long string: " + s);
}
```

### 3.6 Switch Expressions (JEP 361, JDK 14 正式)

```java
// JDK 11: switch 语句
int numLetters;
switch (day) {
    case MONDAY: case FRIDAY: case SUNDAY:
        numLetters = 6; break;
    case TUESDAY:
        numLetters = 7; break;
    default:
        numLetters = -1;
}

// JDK 17: switch 表达式 (expression)
int numLetters = switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> 6;
    case TUESDAY                -> 7;
    default                     -> -1;
};
```

### 3.7 新 API

```java
// Stream.toList() -- JDK 16 新增
List<String> list = stream.toList();  // 返回不可变 List
// 注意: 与 .collect(Collectors.toList()) 不同，返回的是不可变的

// 新的随机数生成器框架 -- JDK 17 (JEP 356)
RandomGenerator rng = RandomGenerator.of("L64X128MixRandom");

// 上下文特定的反序列化过滤器 -- JDK 17 (JEP 415)
ObjectInputFilter filter = ObjectInputFilter.allowFilter(
    cl -> cl.getName().startsWith("com.example."),
    ObjectInputFilter.Status.REJECTED
);
```

### 3.8 移除的功能

| 移除/废弃 | JEP | 说明 |
|-----------|-----|------|
| RMI Activation | JEP 407 | 完全移除 `java.rmi.activation` 包 |
| Applet API | JEP 398 | 标记为废弃，JDK 26 正式移除 |
| Security Manager | JEP 411 | 标记为废弃 |
| 实验性 AOT/Graal JIT | JEP 410 | 移除 `jaotc` 工具和 `jdk.aot` 模块 |
| Biased Locking | JEP 374 | 默认禁用 `-XX:+UseBiasedLocking` |

### 3.9 JVM 参数变更

```bash
# ZGC 不再是实验性 (JDK 15 起)
-XX:+UseZGC          # 不再需要 -XX:+UnlockExperimentalVMOptions

# 废弃参数处理
-XX:+UseBiasedLocking     # JDK 15 废弃，JDK 18 移除
-XX:+UseConcMarkSweepGC   # JDK 14 移除
```

### 3.10 第三方库最低版本

| 库/框架 | JDK 17 最小版本 |
|---------|-----------------|
| Spring Framework | 5.3+ (推荐 Spring 6.x) |
| Spring Boot | 2.5+ (推荐 Spring Boot 3.x) |
| Hibernate | 5.6+ |
| Jackson | 2.13+ |
| Log4j 2 | 2.17+ (安全修复) |
| JUnit | 5.8+ |
| Mockito | 4.0+ |

---

## 4. JDK 17 → 21: 虚拟线程时代

> **迁移复杂度**: 中高 | **建议时间**: 4-8 周 | **关键变革**: Virtual Threads (JEP 444)

### 4.1 Virtual Threads -- 虚拟线程 (JEP 444, 正式版)

```java
// JDK 17: 平台线程 (platform thread), 1:1 映射到 OS 线程
ExecutorService executor = Executors.newFixedThreadPool(200);

// JDK 21: 虚拟线程 (virtual thread), JVM 管理的轻量级线程
// 可以创建数百万个，不阻塞 OS 线程
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 100_000; i++) {
        executor.submit(() -> {
            Thread.sleep(Duration.ofSeconds(1)); // 不阻塞 OS 线程
            return fetchFromDB();
        });
    }
}

// 直接创建虚拟线程
Thread vthread = Thread.ofVirtual().start(() -> {
    System.out.println("Hello from virtual thread");
});
```

**适用性评估**:

| 应用类型 | Virtual Threads 适用性 | 预期收益 |
|----------|------------------------|----------|
| REST API / 微服务 | 极高 | 吞吐量 2-5x 提升 |
| 数据库密集型 | 高 | 减少连接池需求 |
| 消息队列消费者 | 高 | 增加并发消费者数量 |
| CPU 密集型计算 | 低 | 无收益，仍应使用平台线程 |

**注意事项**:
- `synchronized` 块在虚拟线程中会导致 pinning (固定到载体线程)，优先使用 `ReentrantLock`
- `ThreadLocal` 在虚拟线程中仍可工作，但每个虚拟线程一份拷贝，需注意内存消耗

### 4.2 Pattern Matching for switch (JEP 441, 正式版)

```java
// JDK 21: switch 支持模式匹配 + guarded patterns
String describe(Object obj) {
    return switch (obj) {
        case Integer i when i > 0 -> "positive int: " + i;
        case Integer i            -> "other int: " + i;
        case String s             -> "string: " + s;
        case null                 -> "null";
        default                   -> "unknown: " + obj;
    };
}
```

### 4.3 Record Patterns (JEP 440, 正式版)

```java
// 嵌套解构 (nested deconstruction)
record Point(int x, int y) {}
record Line(Point start, Point end) {}

if (obj instanceof Line(Point(int x1, int y1), Point(int x2, int y2))) {
    double length = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
}
```

### 4.4 Sequenced Collections (JEP 431)

```java
// 新接口: SequencedCollection, SequencedSet, SequencedMap
// 提供统一的有序访问 API

SequencedCollection<String> seq = new LinkedHashSet<>();
seq.addFirst("a");
seq.addLast("z");
String first = seq.getFirst();  // "a"
String last  = seq.getLast();   // "z"
seq.reversed().forEach(System.out::println); // 反向遍历
```

### 4.5 Generational ZGC (JEP 439)

```bash
# JDK 21: 启用分代 ZGC (需要显式参数)
-XX:+UseZGC -XX:+ZGenerational

# 注意: JDK 23 起分代模式成为默认，无需 -XX:+ZGenerational
```

### 4.6 Foreign Function & Memory API (JEP 442, 第三次预览)

```java
// 替代 JNI 的更安全方式调用本地代码
// JDK 21 中是预览特性，JDK 22 正式
```

### 4.7 破坏性变更

| 变更 | 影响 |
|------|------|
| `Thread.stop()` 抛出 `UnsupportedOperationException` | 使用 `Thread.interrupt()` 替代 |
| 动态代理 `Proxy` 行为变更 | 检查自定义代理代码 |
| `IdentityHashMap` 行为微调 | 极少数情况下影响 |

### 4.8 构建配置更新

```xml
<!-- Maven -->
<properties>
    <maven.compiler.release>21</maven.compiler.release>
</properties>

<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.11.0</version>
    <configuration>
        <release>21</release>
    </configuration>
</plugin>
```

---

## 5. JDK 21 → 25: LTS 到 LTS

> **迁移复杂度**: 低-中 | **建议时间**: 1-2 周 | **关键变革**: Scoped Values 正式版, Compact Source Files, AOT 优化

JDK 25 是继 JDK 21 之后的下一个 LTS 版本 (GA 2025-09-16)。

### 5.1 新的正式特性 (Final Features)

**Scoped Values (JEP 506) -- 虚拟线程场景下 ThreadLocal 的替代方案**:

```java
// JDK 21: ThreadLocal (在虚拟线程场景下内存消耗大)
private static final ThreadLocal<User> CURRENT_USER = new ThreadLocal<>();
CURRENT_USER.set(user);
try {
    processRequest();
} finally {
    CURRENT_USER.remove();  // 必须清理
}

// JDK 25: ScopedValue (正式版，自动清理，虚拟线程友好)
private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();
ScopedValue.where(CURRENT_USER, user).run(() -> {
    processRequest();  // 作用域结束自动清理
});
```

**Compact Source Files (JEP 512) -- 简化入口程序**:

```java
// 无需 public class 声明，无需 public static void main(String[] args)
void main() {
    System.out.println("Hello, World!");
}
```

```bash
java Hello.java  # 直接运行单文件
```

**Module Import Declarations (JEP 511)**:

```java
// 旧: 逐个导入
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

// 新: 模块级导入
import module java.base;
```

**Flexible Constructor Bodies (JEP 513)**:

```java
class Sub extends Base {
    Sub(int value) {
        // 可以在 super() 或 this() 之前执行语句
        int validated = validate(value);
        super(validated);
    }
}
```

### 5.2 性能改进

**Compact Object Headers (JEP 519, 实验性)**:

```bash
# 启用紧凑对象头: 对象头从 12-16 字节压缩至 8 字节
-XX:+UnlockExperimentalVMOptions -XX:+UseCompactObjectHeaders
```

**AOT 命令行优化 (JEP 514 + JEP 515)**:

```bash
# 新的 AOT 工作流
# 第一步: 录制 AOT 配置
java -XX:AOTConfiguration=app.aotconf -jar myapp.jar

# 第二步: 生成 AOT 缓存
java -XX:AOTCache=app.aot -XX:AOTConfiguration=app.aotconf -jar myapp.jar

# 第三步: 使用 AOT 缓存启动
java -XX:AOTCache=app.aot -jar myapp.jar
```

**ZGC 分代模式已是默认 (JDK 23 起)**:

```bash
# JDK 25 中使用 ZGC 自动启用分代模式
-XX:+UseZGC    # 分代模式已是默认，无需 -XX:+ZGenerational
```

### 5.3 安全特性

**KDF API (JEP 510) -- 密钥派生函数**:

```java
KDF kdf = KDF.getInstance("HKDF-SHA256");

HKDFParameterSpec params = HKDFParameterSpec.ofExtract()
    .addSalt(salt)
    .extract(ikm)
    .expand(info, 32);

SecretKey key = kdf.deriveKey("AES", params);
```

### 5.4 破坏性变更

| 变更 | 影响 | 建议 |
|------|------|------|
| 32-bit x86 移除 (JEP 503) | 运行在 32 位 x86 平台的应用 | 迁移到 64 位 |
| String Templates 撤销 | 使用了 JDK 21-22 预览版 String Templates 的代码 | 改用传统字符串拼接 |
| Security Manager 进一步限制 | 依赖 Security Manager 的应用 | 迁移至其他安全机制 |

```bash
# 检查当前架构
uname -m
# i686, i386 = 32位 (受 JEP 503 影响)
# x86_64, aarch64 = 64位 (不受影响)
```

### 5.5 JFR 增强

```bash
# JFR Method Timing (JEP 520) -- 方法级性能追踪
# 在 JFC 配置文件中启用 jdk.MethodTiming

# JFR CPU-Time Profiling (JEP 509, 实验性)
# 在 JFC 配置文件中启用 jdk.CPUTimeSample
```

---

## 6. JDK 25 → 26: 功能版本升级

> **迁移复杂度**: 低 | **建议时间**: 1 周 | **关键变革**: HTTP/3, G1 GC 吞吐量提升, AOT 对象缓存

JDK 26 是 JDK 25 (LTS) 之后的首个功能版本 (GA 2026-03-17)。

### 6.1 HTTP/3 支持 (JEP 517, 正式版)

```java
// 基于 QUIC 协议，支持会话恢复时 0-RTT
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3)  // 新增枚举值
    .connectTimeout(Duration.ofSeconds(10))
    .build();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com"))
    .build();

HttpResponse<String> response = client.send(
    request, HttpResponse.BodyHandlers.ofString()
);

System.out.println("Protocol: " + response.version()); // HTTP_3
```

### 6.2 G1 GC 吞吐量提升 (JEP 522)

```bash
# 自动获得 10-20% 吞吐量提升，无需额外参数
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200

# JEP 522 通过减少同步开销 (Claim Table 机制) 提升吞吐量
# 在高并发标记阶段效果最显著
```

### 6.3 AOT 对象缓存 (JEP 516)

```bash
# 支持任意 GC 的 AOT 对象缓存 (之前仅支持特定 GC)
java -XX:AOTCache=app.aot MyApp

# 先录制再使用的工作流
java -XX:AOTConfiguration=app.aotconf MyApp
java -XX:AOTCache=app.aot -XX:AOTConfiguration=app.aotconf MyApp
```

### 6.4 严格 final 语义 (JEP 500)

```java
// JDK 26: 通过反射修改 final 字段默认失败
public class Config {
    private final int timeout = 30;

    public void hack() throws Exception {
        Field f = getClass().getDeclaredField("timeout");
        f.setAccessible(true);
        f.set(this, 60);  // JDK 26 抛出异常
    }
}

// 迁移方案 1: 移除 final 修饰符
private int timeout = 30;

// 迁移方案 2: 使用 AtomicReference
private final AtomicReference<Integer> timeout = new AtomicReference<>(30);

// 迁移方案 3: 使用可变容器
private final int[] timeout = {30};
```

**检查受影响的代码**:
```bash
grep -r "setAccessible" src/ | grep -i field
grep -r "Field.set" src/
```

### 6.5 Applet API 正式移除 (JEP 504)

```bash
# 检查 Applet 相关代码
grep -r "import java.applet" src/
grep -r "extends Applet" src/
grep -r "extends JApplet" src/
```

迁移方案:

| 原方案 | 替代方案 |
|--------|----------|
| Applet | JavaFX / Swing 桌面应用 |
| Web Applet | JavaScript + WebAssembly |

### 6.6 预览特性

以下特性需要 `--enable-preview`:

| JEP | 特性 | 预览次数 |
|-----|------|----------|
| JEP 525 | Structured Concurrency 结构化并发 | 第 6 次 |
| JEP 530 | Primitive Types in Patterns 原始类型模式匹配 | 第 4 次 |
| JEP 526 | Lazy Constants 延迟常量 | 第 2 次 |
| JEP 524 | PEM Encodings 加密对象 PEM 编码 | 第 2 次 |

### 6.7 其他改进

| 改进 | 说明 |
|------|------|
| Generational Shenandoah (JEP 521) | 分代 Shenandoah GC (实验性) |
| Vector API (JEP 529) | 第 11 次孵化 |
| Unicode 17.0.0 | 最新 Unicode 支持 |
| CLDR 48.0 | 本地化数据更新 |

---

## 7. 通用升级步骤

### 1. 准备阶段

```bash
# 1.1 备份
cp -r /path/to/app /path/to/app.backup

# 1.2 创建升级分支
git checkout -b upgrade-jdk-XX

# 1.3 分析依赖
jdeps --jdk-internals myapp.jar
jdeprscan --release XX --for-removal myapp.jar
```

### 2. 编译阶段

```bash
# Maven
mvn versions:display-property-updates
mvn versions:update-properties
mvn clean compile

# Gradle
./gradlew dependencyUpdates
./gradlew clean build
```

### 3. 测试阶段

```bash
# 单元测试
mvn test

# 集成测试
mvn verify

# 性能基准测试 (JMH)
java -jar target/benchmarks.jar -rf json -rff results.json
```

### 4. 部署阶段

```dockerfile
# 更新 Docker 基础镜像
FROM eclipse-temurin:26-jdk
COPY app.jar /app/app.jar
ENTRYPOINT ["java", "-XX:+UseG1GC", "-jar", "/app/app.jar"]
```

---

## 8. 回滚计划

如果升级后出现问题:

```bash
# 1. 代码回滚
git checkout main

# 2. 容器部署回滚
kubectl scale deployment app-new --replicas=0
kubectl scale deployment app-old --replicas=3

# 3. SDKMAN 切换版本
sdk default java 21

# 4. 验证
curl -f http://app/health
```

**快速回滚条件**:
- 应用无法启动 (模块解析失败)
- 性能下降超过 20%
- 关键功能故障
- 安全连接失败

---

## 9. 检查清单

### 通用清单 (每次升级)

- [ ] jdeps 分析完成，无 JDK 内部 API 依赖
- [ ] jdeprscan 扫描完成，废弃 API 已替换
- [ ] 构建配置 (Maven/Gradle) 已更新
- [ ] JVM 参数检查，移除废弃参数
- [ ] 第三方库升级到兼容版本
- [ ] 所有单元测试通过
- [ ] 集成测试通过
- [ ] 性能基准测试符合预期
- [ ] Docker 基础镜像已更新
- [ ] 回滚计划已制定

### JDK 8 → 11 专项

- [ ] Java EE 依赖 (JAXB/JAX-WS) 已添加 Maven 依赖
- [ ] --add-opens / --add-exports 参数已配置
- [ ] GC 日志格式已迁移到 -Xlog
- [ ] PermSize → MetaspaceSize 参数已替换

### JDK 11 → 17 专项

- [ ] --illegal-access=permit 参数已移除
- [ ] Security Manager 使用已评估
- [ ] CMS GC 参数已移除

### JDK 17 → 21 专项

- [ ] Virtual Threads 适用性已评估
- [ ] synchronized 导致的 pinning 已检查
- [ ] Thread.stop() 调用已替换

### JDK 21 → 25 专项

- [ ] 32 位 x86 平台影响已确认
- [ ] String Templates 预览代码已清理
- [ ] ZGC -XX:+ZGenerational 参数已移除 (默认启用)

### JDK 25 → 26 专项

- [ ] Applet API 代码已移除
- [ ] 反射修改 final 字段的代码已重构
- [ ] HTTP/3 兼容性已测试
