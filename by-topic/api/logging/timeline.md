# 日志框架演进时间线

Java 日志从 JDK 1.0 到 JDK 26 的完整演进历程。

---

## 时间线概览

```
JDK 1.0 ──── JDK 1.4 ──── JDK 5 ──── SLF4J ──── Logback ──── JDK 9 ──── JDK 26
 │             │           │        (2006)   (2007)      Console      增强日志
System.out    JUL         JCL      接口      实现        格式化      桥接
              Logging              (Apache)
```

---

## 日志体系结构

```
┌─────────────────────────────────────────────────────────┐
│                  Java 日志体系                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  应用层                                                 │
│      │                                                  │
│      ▼                                                  │
│  ┌─────────────────────────────────────────────┐        │
│  │              日志门面 (Facade)               │        │
│  │  SLF4J, Apache Commons Logging              │        │
│  └─────────────────┬───────────────────────────┘        │
│                    │                                    │
│         ┌──────────┴──────────┐                         │
│         │                     │                         │
│  ┌──────▼──────┐      ┌──────▼──────┐                 │
│  │  Logback    │      │  Log4j 2    │                 │
│  │  (推荐)     │      │  (流行)     │                 │
│  └─────────────┘      └──────┬──────┘                 │
│                              │                          │
│  ┌───────────────────────────┴─────────────────────┐  │
│  │            JUL (java.util.logging)              │  │
│  │            JDK 内置                               │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  输出: Console, File, Database, Syslog, Network...      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## JDK 1.0 - System.out

### 基础输出

```java
// 控制台输出 (不推荐用于生产)
System.out.println("Info message");
System.err.println("Error message");

// 问题:
// 1. 无法控制日志级别
// 2. 无法输出到文件
// 3. 性能差 (每次都输出)
// 4. 无法格式化
// 5. 无法按条件输出
```

---

## JDK 1.4 - JUL (java.util.logging)

### 基础配置

```java
import java.util.logging.*;

// 获取 Logger
Logger logger = Logger.getLogger(MyClass.class.getName());

// 日志级别
logger.severe("严重错误");
logger.warning("警告");
logger.info("信息");
logger.config("配置");
logger.fine("详细信息");
logger.finer("更详细信息");
logger.finest("最详细信息");

// 使用级别方法
logger.log(Level.SEVERE, "严重错误: {0}", errorMessage);
```

### Logger 层级

```
Logger
├── "" (根 Logger)
│   ├── "com"
│   │   ├── "com.example"
│   │   │   ├── "com.example.service"
│   │   │   └── "com.example.web"
│   │   └── "com.example.dao"
```

### 配置文件

```properties
# logging.properties

# 全局级别
.level=INFO

# Console Handler
handlers=java.util.logging.ConsoleHandler

# File Handler
handlers=java.util.logging.FileHandler
java.util.logging.FileHandler.pattern=%h/app%u.log
java.util.logging.FileHandler.limit=1000000
java.util.logging.FileHandler.count=3
java.util.logging.FileHandler.formatter=java.util.logging.SimpleFormatter

# 自定义 Logger 级别
com.example.level=FINE
com.example.service.level=FINER
```

### Handler

```java
// ConsoleHandler - 控制台输出
ConsoleHandler consoleHandler = new ConsoleHandler();
consoleHandler.setLevel(Level.ALL);
logger.addHandler(consoleHandler);

// FileHandler - 文件输出
try {
    FileHandler fileHandler = new FileHandler("app.log", true);
    fileHandler.setFormatter(new SimpleFormatter());
    logger.addHandler(fileHandler);
} catch (IOException e) {
    e.printStackTrace();
}

// 自定义 Handler
Handler handler = new Handler() {
    @Override
    public void publish(LogRecord record) {
        if (isLoggable(record)) {
            // 自定义输出逻辑
        }
    }

    @Override
    public void flush() {}

    @Override
    public void close() throws SecurityException {}
};
```

### Formatter

```java
// SimpleFormatter - 简单格式
// Formatter - 自定义格式
class MyFormatter extends Formatter {
    @Override
    public String format(LogRecord record) {
        return String.format(
            "[%1$tF %1$tT] [%2$-7s] %3$s %n",
            new Date(record.getMillis()),
            record.getLevel().getLocalizedName(),
            record.getMessage()
        );
    }
}

fileHandler.setFormatter(new MyFormatter());
```

---

## SLF4J - 日志门面

### 基础使用

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

// 获取 Logger
private static final Logger logger = LoggerFactory.getLogger(MyClass.class);

// 日志输出
logger.trace("详细日志");
logger.debug("调试日志");
logger.info("信息日志");
logger.warn("警告日志");
logger.error("错误日志");

// 参数化日志
logger.info("用户 {} 登录成功，IP: {}", username, ip);

// 异常日志
logger.error("处理失败", exception);
```

### 占位符

```java
// SLF4J 占位符
logger.info("Hello {}", "World");  // Hello World

// 多个参数
logger.info("User: {}, Age: {}, IP: {}", name, age, ip);

// 异常作为最后一个参数
logger.error("Failed to process: {}", id, exception);

// 转义
logger.debug("Value: {}", value.replace("{}", "\\{}"));
```

### Markers

```java
import org.slf4j.Marker;
import org.slf4j.MarkerFactory;

// Marker - 标记特殊日志
Marker important = MarkerFactory.getMarker("IMPORTANT");
Marker database = MarkerFactory.getMarker("DATABASE");

important.add(database);

logger.error(important, "数据库连接失败");

// 使用 Marker 过滤
<configuration>
  <appender name="FILE" class="ch.qos.logback.core.FileAppender">
    <filter class="ch.qos.logback.core.filter.EvaluatorFilter">
      <evaluator class="ch.qos.logback.classic.boolex.OnMarkerEvaluator">
        <marker>IMPORTANT</marker>
      </evaluator>
      <onMatch>ACCEPT</onMatch>
      <onMismatch>DENY</onMismatch>
    </filter>
  </appender>
</configuration>
```

---

## Logback - 推荐实现

### logback.xml 配置

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>

  <!-- 控制台输出 -->
  <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
    <encoder>
      <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
      <charset>UTF-8</charset>
    </encoder>
  </appender>

  <!-- 文件输出 -->
  <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>logs/app.log</file>
    <encoder>
      <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
    </encoder>

    <!-- 滚动策略 -->
    <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
      <fileNamePattern>logs/app.%d{yyyy-MM-dd}.log</fileNamePattern>
      <maxHistory>30</maxHistory>
      <totalSizeCap>1GB</totalSizeCap>
    </rollingPolicy>
  </appender>

  <!-- 异步输出 -->
  <appender name="ASYNC_FILE" class="ch.qos.logback.classic.AsyncAppender">
    <appender-ref ref="FILE" />
    <queueSize>512</queueSize>
    <discardingThreshold>0</discardingThreshold>
  </appender>

  <!-- 根 Logger -->
  <root level="INFO">
    <appender-ref ref="CONSOLE" />
    <appender-ref ref="ASYNC_FILE" />
  </root>

  <!-- 特定 Logger -->
  <logger name="com.example" level="DEBUG" />
  <logger name="org.hibernate" level="WARN" />
  <logger name="org.springframework" level="INFO" />

</configuration>
```

### Logback 配置类

```java
import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.LoggerContext;
import ch.qos.logback.classic.encoder.PatternLayoutEncoder;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.ConsoleAppender;
import ch.qos.logback.core.FileAppender;
import ch.qos.logback.core.rolling.RollingFileAppender;
import ch.qos.logback.core.rolling.TimeBasedRollingPolicy;
import org.slf4j.LoggerFactory;

// 编程式配置
public class LogbackConfig {
    public static void configure() {
        LoggerContext loggerContext = (LoggerContext) LoggerFactory.getILoggerFactory();

        // Console Appender
        ConsoleAppender<ILoggingEvent> consoleAppender = new ConsoleAppender<>();
        consoleAppender.setContext(loggerContext);
        consoleAppender.setName("console");

        PatternLayoutEncoder encoder = new PatternLayoutEncoder();
        encoder.setContext(loggerContext);
        encoder.setPattern("%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n");
        encoder.start();

        consoleAppender.setEncoder(encoder);
        consoleAppender.start();

        // File Appender
        RollingFileAppender<ILoggingEvent> fileAppender = new RollingFileAppender<>();
        fileAppender.setContext(loggerContext);
        fileAppender.setName("file");
        fileAppender.setFile("logs/app.log");

        // Rolling Policy
        TimeBasedRollingPolicy<ILoggingEvent> rollingPolicy =
            new TimeBasedRollingPolicy<>();
        rollingPolicy.setContext(loggerContext);
        rollingPolicy.setFileNamePattern("logs/app.%d{yyyy-MM-dd}.log");
        rollingPolicy.setMaxHistory(30);
        rollingPolicy.setParent(fileAppender);
        rollingPolicy.start();

        fileAppender.setRollingPolicy(rollingPolicy);
        fileAppender.setEncoder(encoder);
        fileAppender.start();

        // Root Logger
        ch.qos.logback.classic.Logger rootLogger =
            loggerContext.getLogger(Logger.ROOT_LOGGER_NAME);
        rootLogger.setLevel(Level.INFO);
        rootLogger.addAppender(consoleAppender);
        rootLogger.addAppender(fileAppender);
    }
}
```

---

## Log4j 2 - 流行实现

### log4j2.xml 配置

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="WARN">
  <Appenders>
    <!-- Console -->
    <Console name="Console" target="SYSTEM_OUT">
      <PatternLayout pattern="%d{HH:mm:ss.SSS} [%t] %-5level %logger{36} - %msg%n"/>
    </Console>

    <!-- File -->
    <RollingFile name="File" fileName="logs/app.log"
                 filePattern="logs/app-%d{yyyy-MM-dd}-%i.log">
      <PatternLayout pattern="%d{yyyy-MM-dd HH:mm:ss.SSS} [%t] %-5level %logger{36} - %msg%n"/>

      <Policies>
        <TimeBasedTriggeringPolicy interval="1" modulate="true"/>
        <SizeBasedTriggeringPolicy size="100 MB"/>
      </Policies>

      <DefaultRolloverStrategy max="30"/>
    </RollingFile>

    <!-- Async -->
    <Async name="Async">
      <AppenderRef ref="File"/>
    </Async>
  </Appenders>

  <Loggers>
    <Root level="info">
      <AppenderRef ref="Console"/>
      <AppenderRef ref="Async"/>
    </Root>

    <Logger name="com.example" level="debug" additivity="false">
      <AppenderRef ref="Console"/>
      <AppenderRef ref="Async"/>
    </Logger>
  </Loggers>
</Configuration>
```

### Lambda 支持

```java
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

// Log4j 2 Lambda 支持
private static final Logger logger = LogManager.getLogger(MyClass.class);

// Lambda 延迟计算
logger.debug(() -> expensiveOperation());

// 传统方式
if (logger.isDebugEnabled()) {
    logger.debug(expensiveOperation());
}
```

---

## JDK 9+ - Console 格式化

### Console 格式化

```java
// JDK 9+ - System.Logger (JEP 264)
System.Logger logger = System.getLogger("com.example.MyClass");

logger.log(System.Logger.Level.INFO, "Hello {0}", "World");

// 自定义格式化
// -Djava.util.logging.SimpleFormatter.format=
// "[%1$tF %1$tT] [%4$s] %5$s%6$s%n"
```

---

## 日志级别

### 级别对应

| SLF4J | Logback | Log4j 2 | JUL | 说明 |
|-------|---------|---------|-----|------|
| OFF | OFF | OFF | OFF | 关闭 |
| ERROR | ERROR | ERROR | SEVERE | 错误 |
| WARN | WARN | WARN | WARNING | 警告 |
| INFO | INFO | INFO | INFO | 信息 |
| DEBUG | DEBUG | DEBUG | FINE | 调试 |
| TRACE | TRACE | TRACE | FINEST | 跟踪 |

### 级别选择

```java
// 生产环境
logger.setLevel(Level.INFO);

// 开发环境
logger.setLevel(Level.DEBUG);

// 性能测试
logger.setLevel(Level.ERROR);
```

---

## 最佳实践

### 使用占位符

```java
// ✅ 推荐: 占位符
logger.info("User: {}, Age: {}", name, age);

// ❌ 避免: 字符串拼接
logger.info("User: " + name + ", Age: " + age);
```

### 条件日志

```java
// ✅ 推荐: 使用占位符 (内部自动判断)
logger.debug("Value: {}", expensiveMethod());

// ❌ 避免: 手动判断
if (logger.isDebugEnabled()) {
    logger.debug("Value: " + expensiveMethod());
}
```

### 异常日志

```java
// ✅ 推荐: 包含异常
logger.error("Failed to process", exception);

// ✅ 推荐: 带消息
logger.error("Failed to process user: {}", userId, exception);

// ❌ 避免: 只记录消息
logger.error("Failed: " + exception.getMessage());
```

### 静态 Logger

```java
// ✅ 推荐: 静态 final
private static final Logger logger = LoggerFactory.getLogger(MyClass.class);

// ❌ 避免: 每次创建
public void method() {
    Logger logger = LoggerFactory.getLogger(this.getClass());
}
```

---

## 日志桥接

### JUL 到 SLF4J

```xml
<!-- jul-to-slf4j -->
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>jul-to-slf4j</artifactId>
    <version>2.0.9</version>
</dependency>
```

### Log4j 到 SLF4J

```xml
<!-- log4j-over-slf4j -->
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>log4j-over-slf4j</artifactId>
    <version>2.0.9</version>
</dependency>
```

---

## 时间线总结

| 版本 | 特性 | 说明 |
|------|------|------|
| JDK 1.0 | System.out | 控制台输出 |
| JDK 1.4 | JUL (java.util.logging) | 内置日志 |
| 2002 | Log4j 1.x | Apache 日志框架 |
| 2005 | SLF4J | 日志门面 |
| 2006 | Logback | SLF4J 原生实现 |
| 2014 | Log4j 2.x | 重写版本 |
| JDK 9 | System.Logger | 统一日志接口 |
| JDK 26 | 增强日志桥接 | 更好的互操作性 |

---

## 相关链接

- [SLF4J Manual](http://www.slf4j.org/manual.html)
- [Logback Manual](http://logback.qos.ch/manual/)
- [Log4j 2 Manual](https://logging.apache.org/log4j/2.x/manual.html)
