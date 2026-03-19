# java.logging 模块分析

> Java 日志框架 (JUL)，JDK 内置日志解决方案

---

## 1. 模块概述

`java.logging` 是 JDK 自带的日志框架，提供轻量级的日志记录功能。虽然不如 Log4j/SLF4J 流行，但作为 JDK 内置组件，无需额外依赖。

### 模块定义

**文件**: `src/java.logging/share/classes/module-info.java`

```java
module java.logging {
    exports java.util.logging;
}
```

### 架构

```
┌─────────────────────────────────────────────────────────┐
│                    应用代码                              │
│  Logger.log/info/warning/severe/...                      │
├─────────────────────────────────────────────────────────┤
│                   Logger                                 │
│  (命名层次结构, 日志级别过滤)                             │
├─────────────────────────────────────────────────────────┤
│                  Handler                                │
│  ConsoleHandler, FileHandler, SocketHandler, ...        │
├─────────────────────────────────────────────────────────┤
│                  Formatter                              │
│  SimpleFormatter, XMLFormatter                          │
├─────────────────────────────────────────────────────────┤
│                  Filter                                 │
│  自定义过滤逻辑                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 2. 核心类分析

### 2.1 Logger

**源码**: `src/java.logging/share/classes/java/util/logging/Logger.java`

```java
public class Logger {
    // 获取 Logger (命名层次)
    public static Logger getLogger(String name)
    public static Logger getLogger(String name, String resourceBundleName)

    // 日志方法
    public void severe(String msg)
    public void warning(String msg)
    public void info(String msg)
    public void config(String msg)
    public void fine(String msg)
    public void finer(String msg)
    public void finest(String msg)

    // 通用日志方法
    public void log(Level level, String msg)
    public void log(Level level, String msg, Object param1)
    public void log(Level level, String msg, Object[] params)
    public void log(LogRecord record)
}
```

### 2.2 Level (日志级别)

**源码**: `src/java.logging/share/classes/java/util/logging/Level.java`

| 级别 | 值 | 用途 | 常用方法 |
|------|-----|------|----------|
| SEVERE | 1000 | 错误 | `severe()` |
| WARNING | 900 | 警告 | `warning()` |
| INFO | 800 | 信息 | `info()` |
| CONFIG | 700 | 配置 | `config()` |
| FINE | 500 | 详细 | `fine()` |
| FINER | 400 | 更详细 | `finer()` |
| FINEST | 300 | 最详细 | `finest()` |

**级别继承**: 子 Logger 默认继承父 Logger 的级别配置

### 2.3 Handler

**源码**: `src/java.logging/share/classes/java/util/logging/Handler.java`

```java
public abstract class Handler {
    public abstract void publish(LogRecord record)
    public abstract void flush()
    public abstract void close() throws SecurityException

    // 配置
    public void setFormatter(Formatter newFormatter)
    public void setFilter(Filter newFilter)
    public void setLevel(Level newLevel)
}
```

**内置 Handler**:

| Handler | 输出 | 用途 |
|---------|------|------|
| ConsoleHandler | System.err | 控制台输出 |
| FileHandler | 文件 | 文件输出 (支持轮转) |
| StreamHandler | OutputStream | 自定义流 |
| SocketHandler | 网络 | 远程日志服务器 |
| MemoryHandler | 内存 | 循环缓冲区 |

### 2.4 Formatter

**源码**: `src/java.logging/share/classes/java/util/logging/Formatter.java`

```java
public abstract class Formatter {
    public abstract String format(LogRecord record)
    public String getHead(Handler h)
    public String getTail(Handler h)
}
```

**内置 Formatter**:

| Formatter | 格式 | 用途 |
|-----------|------|------|
| SimpleFormatter | 文本 | 人类可读 |
| XMLFormatter | XML | 日志分析工具 |

---

## 3. 配置

### 3.1 配置文件

**默认位置**: `$JAVA_HOME/conf/logging.properties`

```properties
# 全局级别
.level=INFO

# Console Handler
handlers=java.util.logging.ConsoleHandler
java.util.logging.ConsoleHandler.level=INFO
java.util.logging.ConsoleHandler.formatter=java.util.logging.SimpleFormatter

# File Handler (支持轮转)
handlers=java.util.logging.FileHandler
java.util.logging.FileHandler.pattern=%h/java%u.log
java.util.logging.FileHandler.limit=50000
java.util.logging.FileHandler.count=1
java.util.logging.FileHandler.formatter=java.util.logging.XMLFormatter

# 自定义 Logger
com.example.level=FINE
com.example.handlers=java.util.logging.ConsoleHandler
```

### 3.2 编程配置

```java
// 获取根 Logger
Logger root = Logger.getLogger("");

// 移除默认 Handler
root.setLevel(Level.ALL);

// 添加自定义 Handler
ConsoleHandler console = new ConsoleHandler();
console.setLevel(Level.ALL);
console.setFormatter(new SimpleFormatter() {
    @Override
    public String format(LogRecord r) {
        return String.format("[%1$tF %1$tT] [%2$-7s] %3$s %n",
            new Date(r.getMillis()),
            r.getLevel().getLocalizedName(),
            r.getMessage());
    }
});
root.addHandler(console);

// 配置文件输出
try {
    FileHandler file = new FileHandler("%h/app%g.log", 1000000, 5, true);
    file.setFormatter(new SimpleFormatter());
    root.addHandler(file);
} catch (IOException e) {
    Logger.getLogger(getClass().getName()).log(Level.SEVERE, "Failed to add file handler", e);
}
```

---

## 4. JDK 26 变更

### 4.1 性能改进

- 减少 Logger 获取的同步开销
- 优化日志格式化性能

### 4.2 功能增强

- 改进 `LogRecord` 的线程安全性
- 支持 `java.util.stream` 风格的日志处理

### 4.3 与平台日志集成

JDK 26 改进了 `System.Logger` 与 JUL 的集成：

```java
// 使用 Platform Logging API (推荐)
System.Logger logger = System.getLogger("com.example");
logger.log(System.Logger.Level.INFO, "Message {0}", arg);
```

---

## 5. 使用示例

### 5.1 基本使用

```java
import java.util.logging.*;

public class LoggingExample {
    // 每个类使用独立的 Logger
    private static final Logger LOGGER = Logger.getLogger(LoggingExample.class.getName());

    public void doWork() {
        LOGGER.entering("LoggingExample", "doWork");

        try {
            LOGGER.info("Starting work");
            // ...
            LOGGER.exiting("LoggingExample", "doWork");
        } catch (Exception e) {
            LOGGER.log(Level.WARNING, "Work failed", e);
            LOGGER.throwing("LoggingExample", "doWork", e);
        }
    }
}
```

### 5.2 参数化日志

```java
LOGGER.log(Level.INFO, "Processing {0} items, status: {1}", count, status);
```

### 5.3 自定义 Filter

```java
public class MyFilter implements Filter {
    @Override
    public boolean isLoggable(LogRecord record) {
        // 只记录特定来源的日志
        return record.getLoggerName().startsWith("com.example.important");
    }
}

// 使用
logger.setFilter(new MyFilter());
```

### 5.4 文件轮转

```java
// %h = 用户主目录, %u = 唯一编号, %g = 轮转编号
FileHandler handler = new FileHandler("%h/app%u.%g.log",  // 文件模式
                                       1000000,             // 每个文件 1MB
                                       5,                   // 保留 5 个文件
                                       true);               // 追加模式
```

---

## 6. 日志最佳实践

### 6.1 Logger 命名

```java
// 推荐: 使用类全名作为 Logger 名称
private static final Logger LOGGER = Logger.getLogger(MyClass.class.getName());

// 推荐: 使用包名作为共享 Logger
private static final Logger LOGGER = Logger.getLogger("com.example.service");
```

### 6.2 级别选择

| 场景 | 级别 |
|------|------|
| 生产环境 | INFO / WARNING |
| 开发环境 | FINE / FINER |
| 问题排查 | FINEST |
| 性能分析 | FINE |

### 6.3 异常日志

```java
// 推荐: 包含异常对象
try {
    // ...
} catch (Exception e) {
    LOGGER.log(Level.SEVERE, "Operation failed", e);
}

// 避免: 只记录异常消息
catch (Exception e) {
    LOGGER.severe("Operation failed: " + e.getMessage());  // 丢失堆栈
}
```

### 6.4 性能考虑

```java
// 检查级别避免不必要的字符串拼接
if (LOGGER.isLoggable(Level.FINE)) {
    LOGGER.fine("Expensive operation: " + expensiveOperation());
}

// 使用参数化日志
LOGGER.log(Level.FINE, "Value: {0}", getValue());  // 延迟求值
```

---

## 7. 与其他日志框架对比

| 特性 | JUL | Log4j 2 | Logback |
|------|-----|---------|---------|
| 依赖 | 无 | 外部 | 外部 |
| 性能 | 中 | 高 | 高 |
| 配置 | properties | XML/JSON/YAML | XML/Groovy |
| 异步日志 | ❌ | ✓ | ✓ |
| Appender | Handler | Appender | Appender |
| JDK 26 支持 | ✓ | ✓ | ✓ |

**JDK 26 建议**:
- 简单应用: 使用 JUL
- 企业应用: 使用 Log4j 2 / Logback

---

## 8. 相关链接

- [JUL 官方文档](https://docs.oracle.com/en/java/javase/26/core/java-logging-overview.html)
- [logging.properties 示例](https://github.com/openjdk/jdk/blob/master/src/java.logging/share/conf/logging.properties)
- [源码](https://github.com/openjdk/jdk/tree/master/src/java.logging/share/classes/java/util/logging)
