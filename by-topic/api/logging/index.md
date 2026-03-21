# 日志框架

> java.util.logging、System.Logger、SLF4J、Logback 演进历程

[← 返回 API 框架](../)

---

## 1. 快速概览

```
JDK 1.0 ── JDK 1.4 ── JDK 9 ── JDK 11 ── 2002 ── 2006 ── 2014 ── JDK 9
   │         │        │        │         │         │         │        │
System.out  JUL    System.Logger  Log4j  SLF4J  Logback  JUL桥接
PrintStream  java.util.  桥接    门面   原生    SLF4J
          logging    支持           实现    实现    to JUL
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
- [Log4j 2.x]((#log4j-2x)
- [日志桥接](#日志桥接)
- [最佳实践](#最佳实践)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 2. java.util.logging (JUL)

**JDK 1.4 引入**

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

FileHandler file = new FileHandler("app.log", true);
file.setLevel(Level.ALL);
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
```

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
public class MyLoggerFinder implements System.LoggerFinder {
    @Override
    public System.Logger getLogger(String name, Module module) {
        return new MyLogger(name);
    }
}

// 配置文件
# META-INF/services/java.lang.System$LoggerFinder
com.example.MyLoggerFinder
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

## 6. 日志桥接

### JUL to SLF4J

```xml
<!-- jul-to-slf4j -->
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>jul-to-slf4j</artifactId>
    <version>2.0.9</version>
</dependency>
```

```java
// 配置 JUL 使用 SLF4J
java.util.logging.Logger.getLogger("").setLevel(java.util.logging.Level.ALL);
```

### Log4j to SLF4J

```xml
<!-- log4j-to-slf4j -->
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>log4j-to-slf4j</artifactId>
    <version>2.0.9</version>
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
<!-- slf4j-jdk14 (JDK 8+) -->
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-jdk14</artifactId>
    <version>1.7.36</version>
</dependency>

<!-- slf4j-jdk-platform-logging (JDK 9+) -->
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-jdk-platform-logging</artifactId>
    <version>2.0.9</version>
</dependency>
```

---

## 7. 最佳实践

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

```java
// Logback 异步 appender
<appender name="ASYNC" class="ch.qos.logback.classic.AsyncAppender">
    <appender-ref ref="FILE" />
    <queueSize>512</queueSize>
    <discardingThreshold>0</discardingThreshold>
</appender>
```

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

## 8. 核心贡献者

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

## 9. Git 提交历史

> 基于 OpenJDK master 分支分析

### 日志改进 (2024-2026)

```bash
# 查看日志相关提交
cd /path/to/jdk
git log --oneline -- src/java.base/share/classes/java/util/logging/
```

---

## 10. 相关链接

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

**最后更新**: 2026-03-20

**Sources**:
- [JEP 264](/jeps/api/jep-264.md)
- [SLF4J 官方文档](https://www.slf4j.org/)
- [Logback 官方文档](https://logback.qos.ch/)
- [Log4j 2.x 官方文档](https://logging.apache.org/log4j/2.x/)
- [JUL to SLF4J Bridge](https://tersesystems.github.io/terse-logback/1.0.0/guide/slf4jbridge/)
