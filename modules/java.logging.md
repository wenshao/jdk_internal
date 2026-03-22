# java.logging 模块分析 (Java Logging API)

> JDK 内置日志框架 (JUL - Java Util Logging)，23 个源文件

---

## 1. 模块概述 (Overview)

`java.logging` 是独立的 JDK 模块，提供 `java.util.logging` (JUL) 日志框架。自 JDK 9 模块化以来作为单独模块存在。

### 模块定义 (Module Declaration)

**源码**: `src/java.logging/share/classes/module-info.java`

```java
/**
 * Defines the Java Logging API.
 * @since 9
 */
module java.logging {
    exports java.util.logging;

    provides jdk.internal.logger.DefaultLoggerFinder with
        sun.util.logging.internal.LoggingProviderImpl;
}
```

**要点**:
- 只导出一个公开包: `java.util.logging`
- 通过 `provides` 声明将 JUL 注册为 `System.Logger` 的默认实现
- 当 `java.logging` 模块存在时，`System.getLogger()` 底层使用 JUL

### 完整文件清单 (All 23 Source Files)

**公开 API** (`java.util.logging` 包, 19 个文件):

| 文件 | 类型 | 说明 |
|---|---|---|
| `Logger.java` | class | 日志记录器，命名层次结构 |
| `LogManager.java` | class | Logger 管理器，全局单例 |
| `LogRecord.java` | class | 日志记录，封装一条日志的所有信息 |
| `Level.java` | class | 日志级别 |
| `Handler.java` | abstract class | 日志输出处理器基类 |
| `StreamHandler.java` | class | 流输出处理器 |
| `ConsoleHandler.java` | class | 控制台处理器 (输出到 System.err) |
| `FileHandler.java` | class | 文件处理器 (支持轮转) |
| `SocketHandler.java` | class | 网络套接字处理器 |
| `MemoryHandler.java` | class | 内存缓冲处理器 (循环缓冲区) |
| `Formatter.java` | abstract class | 日志格式化器基类 |
| `SimpleFormatter.java` | class | 简单文本格式化 |
| `XMLFormatter.java` | class | XML 格式化 |
| `Filter.java` | interface | 日志过滤器 |
| `ErrorManager.java` | class | Handler 内部错误管理 |
| `Logging.java` | class | LoggingMXBean 实现 |
| `LoggingMXBean.java` | interface | 日志管理 MXBean |
| `LoggingPermission.java` | class | 日志操作权限 |
| `package-info.java` | - | 包文档 |

**内部实现** (4 个文件):

| 文件 | 包 | 说明 |
|---|---|---|
| `LoggingProviderImpl.java` | `sun.util.logging.internal` | System.Logger 桥接实现 |
| `package-info.java` | `sun.util.logging.internal` | 内部包文档 |
| `HttpLogFormatter.java` | `sun.net.www.protocol.http.logging` | HTTP 协议日志格式化 |
| `module-info.java` | - | 模块描述 |

---

## 2. 架构 (Architecture)

### 2.1 组件关系图

```
┌───────────────────────────────────────────────────────┐
│                    应用代码 (Application)               │
│  Logger.getLogger("com.example").info("message")      │
├───────────────────────────────────────────────────────┤
│  Logger (日志记录器)                                    │
│  ├─ 命名层次: com → com.example → com.example.service │
│  ├─ 级别过滤 (Level Filtering)                         │
│  └─ Filter 自定义过滤                                  │
├───────────────────────────────────────────────────────┤
│  LogRecord (日志记录)                                   │
│  封装: 级别、消息、时间、线程、源类/方法、异常              │
├───────────────────────────────────────────────────────┤
│  Handler (输出处理器)                                   │
│  ├─ ConsoleHandler → System.err                       │
│  ├─ FileHandler → 文件 (支持轮转/追加)                  │
│  ├─ SocketHandler → TCP 套接字                         │
│  ├─ MemoryHandler → 内存缓冲 → 触发推送到目标 Handler    │
│  └─ StreamHandler → 任意 OutputStream                 │
├───────────────────────────────────────────────────────┤
│  Formatter (格式化器)                                   │
│  ├─ SimpleFormatter → 人类可读文本                      │
│  └─ XMLFormatter → XML 格式                            │
└───────────────────────────────────────────────────────┘
```

### 2.2 Logger 命名层次 (Naming Hierarchy)

```
"" (根 Logger, root)
├── "com"
│   └── "com.example"
│       ├── "com.example.service"
│       └── "com.example.dao"
├── "java"
│   └── "java.net.http"
└── "sun"
    └── "sun.net"
```

- 子 Logger 默认继承父 Logger 的级别和 Handler
- 可通过 `setUseParentHandlers(false)` 阻止向上传播
- `Logger.getLogger("")` 获取根 Logger

---

## 3. 核心类分析 (Key Class Analysis)

### 3.1 Logger

**源码**: `src/java.logging/share/classes/java/util/logging/Logger.java`

```java
public class Logger {
    // 获取/创建 Logger
    public static Logger getLogger(String name)
    public static Logger getLogger(String name, String resourceBundleName)
    public static Logger getAnonymousLogger()

    // 便捷日志方法 (Convenience Methods)
    public void severe(String msg)    // Level.SEVERE (1000)
    public void warning(String msg)   // Level.WARNING (900)
    public void info(String msg)      // Level.INFO (800)
    public void config(String msg)    // Level.CONFIG (700)
    public void fine(String msg)      // Level.FINE (500)
    public void finer(String msg)     // Level.FINER (400)
    public void finest(String msg)    // Level.FINEST (300)

    // 通用日志方法
    public void log(Level level, String msg)
    public void log(Level level, String msg, Object param1)
    public void log(Level level, String msg, Object[] params)
    public void log(Level level, String msg, Throwable thrown)
    public void log(LogRecord record)

    // Lambda 延迟求值 (JDK 8+)
    public void log(Level level, Supplier<String> msgSupplier)

    // 方法跟踪 (Method Tracing)
    public void entering(String sourceClass, String sourceMethod)
    public void exiting(String sourceClass, String sourceMethod)
    public void throwing(String sourceClass, String sourceMethod, Throwable thrown)

    // 级别检查 (避免不必要的字符串构建)
    public boolean isLoggable(Level level)

    // Handler 管理
    public void addHandler(Handler handler)
    public void removeHandler(Handler handler)
    public Handler[] getHandlers()

    // 配置
    public void setLevel(Level newLevel)
    public Level getLevel()
    public void setFilter(Filter newFilter)
    public void setUseParentHandlers(boolean useParentHandlers)
}
```

### 3.2 Level 日志级别

**源码**: `src/java.logging/share/classes/java/util/logging/Level.java`

| 级别 (Level) | 整数值 (Value) | 用途 (Usage) | 便捷方法 |
|---|---|---|---|
| `OFF` | Integer.MAX_VALUE | 关闭日志 | - |
| `SEVERE` | 1000 | 严重错误 | `severe()` |
| `WARNING` | 900 | 警告 | `warning()` |
| `INFO` | 800 | 一般信息 (默认级别) | `info()` |
| `CONFIG` | 700 | 配置信息 | `config()` |
| `FINE` | 500 | 调试信息 | `fine()` |
| `FINER` | 400 | 详细调试 | `finer()` |
| `FINEST` | 300 | 最详细调试 | `finest()` |
| `ALL` | Integer.MIN_VALUE | 记录所有 | - |

### 3.3 LogManager

**源码**: `src/java.logging/share/classes/java/util/logging/LogManager.java`

```java
public class LogManager {
    // 全局单例
    public static LogManager getLogManager()

    // Logger 注册
    public boolean addLogger(Logger logger)
    public Logger getLogger(String name)

    // 配置管理
    public void readConfiguration()   // 读取默认配置
    public void readConfiguration(InputStream ins)
    public void updateConfiguration(Function<String, BiFunction<String,String,String>> mapper)

    // 属性获取
    public String getProperty(String name)
}
```

**配置加载顺序**:
1. 系统属性 `java.util.logging.config.file` 指定的文件
2. 系统属性 `java.util.logging.config.class` 指定的类
3. `$JAVA_HOME/conf/logging.properties` 默认配置

### 3.4 Handler 处理器

**源码**: `src/java.logging/share/classes/java/util/logging/Handler.java`

```java
public abstract class Handler {
    public abstract void publish(LogRecord record);
    public abstract void flush();
    public abstract void close() throws SecurityException;

    public void setFormatter(Formatter newFormatter);
    public void setFilter(Filter newFilter);
    public void setLevel(Level newLevel);
    public void setEncoding(String encoding);
    public void setErrorManager(ErrorManager em);
}
```

**Handler 继承关系**:

```
Handler (abstract)
├── StreamHandler          → OutputStream 输出
│   ├── ConsoleHandler     → System.err
│   ├── FileHandler        → 文件 (轮转/追加)
│   └── SocketHandler      → TCP 套接字
└── MemoryHandler          → 内存缓冲 → 目标 Handler
```

### 3.5 FileHandler 文件轮转

**源码**: `src/java.logging/share/classes/java/util/logging/FileHandler.java`

```java
// 构造参数
FileHandler(String pattern,     // 文件模式
            long limit,          // 单文件大小限制 (字节)
            int count,           // 轮转文件数量
            boolean append)      // 是否追加

// 模式替换变量 (Pattern Variables)
// %h = 用户主目录 (user.home)
// %t = 系统临时目录 (java.io.tmpdir)
// %u = 唯一编号 (解决冲突)
// %g = 轮转编号 (generation number)
// %% = 百分号字面量
```

### 3.6 Formatter 格式化器

**源码**: `src/java.logging/share/classes/java/util/logging/Formatter.java`

```java
public abstract class Formatter {
    public abstract String format(LogRecord record);
    public String getHead(Handler h);     // 文档头 (XMLFormatter 使用)
    public String getTail(Handler h);     // 文档尾
    public String formatMessage(LogRecord record);  // 格式化消息 (处理参数替换)
}
```

**SimpleFormatter 格式** (可通过系统属性定制):

```properties
# 默认格式
java.util.logging.SimpleFormatter.format=%1$tb %1$td, %1$tY %1$tl:%1$tM:%1$tS %1$Tp %2$s%n%4$s: %5$s%6$s%n

# 自定义紧凑格式
java.util.logging.SimpleFormatter.format=[%1$tF %1$tT] [%4$-7s] %5$s %n
```

### 3.7 Filter 过滤器

**源码**: `src/java.logging/share/classes/java/util/logging/Filter.java`

```java
@FunctionalInterface
public interface Filter {
    boolean isLoggable(LogRecord record);
}
```

---

## 4. System.Logger 桥接 (Platform Logging Bridge)

JDK 9 引入了 `System.Logger` 作为平台日志 API，当 `java.logging` 模块在模块路径中时，`System.getLogger()` 返回的 Logger 底层使用 JUL。

**桥接实现**: `sun.util.logging.internal.LoggingProviderImpl`

```java
// System.Logger (java.base 中定义)
System.Logger logger = System.getLogger("com.example");
logger.log(System.Logger.Level.INFO, "Message: {0}", arg);

// 底层委托给 java.util.logging.Logger
// System.Logger.Level 映射到 java.util.logging.Level
```

**级别映射 (Level Mapping)**:

| System.Logger.Level | java.util.logging.Level |
|---|---|
| `ALL` | `ALL` |
| `TRACE` | `FINER` |
| `DEBUG` | `FINE` |
| `INFO` | `INFO` |
| `WARNING` | `WARNING` |
| `ERROR` | `SEVERE` |
| `OFF` | `OFF` |

---

## 5. 配置 (Configuration)

### 5.1 logging.properties 配置文件

**默认位置**: `$JAVA_HOME/conf/logging.properties`

```properties
# 根 Logger 的 Handler
handlers=java.util.logging.ConsoleHandler

# 根 Logger 级别
.level=INFO

# ConsoleHandler 配置
java.util.logging.ConsoleHandler.level=INFO
java.util.logging.ConsoleHandler.formatter=java.util.logging.SimpleFormatter

# FileHandler 配置 (文件轮转)
# java.util.logging.FileHandler.pattern=%h/java%u.log
# java.util.logging.FileHandler.limit=50000
# java.util.logging.FileHandler.count=1
# java.util.logging.FileHandler.maxLocks=100
# java.util.logging.FileHandler.formatter=java.util.logging.XMLFormatter

# 特定 Logger 配置
# com.example.level=FINE
# com.example.handlers=java.util.logging.FileHandler
```

### 5.2 编程配置 (Programmatic Configuration)

```java
// 获取根 Logger 并清除默认 Handler
Logger root = Logger.getLogger("");
for (Handler h : root.getHandlers()) root.removeHandler(h);
root.setLevel(Level.ALL);

// 添加自定义 ConsoleHandler
ConsoleHandler console = new ConsoleHandler();
console.setLevel(Level.ALL);
console.setFormatter(new SimpleFormatter());
root.addHandler(console);

// 添加 FileHandler (5 个轮转文件, 每个 1MB)
FileHandler file = new FileHandler("%h/app%g.log", 1_000_000, 5, true);
file.setFormatter(new SimpleFormatter());
root.addHandler(file);
```

### 5.3 JVM 参数指定配置文件

```bash
java -Djava.util.logging.config.file=/path/to/logging.properties -jar app.jar
```

---

## 6. 使用示例 (Usage Examples)

### 6.1 基本使用

```java
public class MyService {
    private static final Logger LOGGER = Logger.getLogger(MyService.class.getName());

    public void process(String id) {
        LOGGER.entering("MyService", "process", id);
        try {
            LOGGER.info("Processing: " + id);
            // ... 业务逻辑
            LOGGER.fine("Processing detail: ...");
            LOGGER.exiting("MyService", "process");
        } catch (Exception e) {
            LOGGER.log(Level.SEVERE, "Processing failed for " + id, e);
            LOGGER.throwing("MyService", "process", e);
        }
    }
}
```

### 6.2 参数化日志 (避免字符串拼接开销)

```java
// JUL 使用 {0}, {1} 占位符 (MessageFormat 风格)
LOGGER.log(Level.INFO, "User {0} logged in from {1}", new Object[]{user, ip});

// Lambda 延迟求值 (JDK 8+)
LOGGER.fine(() -> "Expensive: " + computeExpensiveValue());

// 级别检查 (传统方式)
if (LOGGER.isLoggable(Level.FINE)) {
    LOGGER.fine("Detail: " + computeExpensiveValue());
}
```

### 6.3 自定义 Filter

```java
Filter securityFilter = record ->
    !record.getMessage().contains("password")
    && !record.getMessage().contains("secret");

logger.setFilter(securityFilter);
```

### 6.4 System.Logger (推荐的平台日志 API)

```java
// 不直接依赖 java.logging 模块
System.Logger logger = System.getLogger("com.example");
logger.log(System.Logger.Level.INFO, "Message: {0}", value);
logger.log(System.Logger.Level.ERROR, "Failed", exception);
```

---

## 7. 与其他日志框架对比 (Comparison)

| 特性 | JUL | Log4j 2 | SLF4J + Logback |
|---|---|---|---|
| 外部依赖 | 无 (JDK 内置) | 需要引入 | 需要引入 |
| 性能 | 中等 | 高 (异步) | 高 |
| 配置格式 | .properties | XML/JSON/YAML | XML/Groovy |
| 异步日志 (Async) | 无 (需自定义) | 内置 AsyncAppender | 内置 AsyncAppender |
| 结构化日志 | 无 | 支持 | 支持 |
| 参数化消息 | `{0}` MessageFormat | `{}` 占位符 | `{}` 占位符 |
| Handler/Appender 数量 | 5 个内置 | 丰富 | 丰富 |

**选择建议**:
- 简单应用/JDK 内部使用: JUL
- 平台无关日志接口: `System.Logger` (JDK 9+)
- 企业应用: Log4j 2 或 SLF4J + Logback

---

## 8. LoggingMXBean 监控 (JMX Integration)

**源码**: `src/java.logging/share/classes/java/util/logging/LoggingMXBean.java`

```java
public interface LoggingMXBean {
    List<String> getLoggerNames();
    String getLoggerLevel(String loggerName);
    void setLoggerLevel(String loggerName, String levelName);
    String getParentLoggerName(String loggerName);
}
```

可通过 JMX 在运行时动态调整日志级别，ObjectName: `java.util.logging:type=Logging`。

---

## 9. 相关链接 (References)

- [Java Logging Overview](https://docs.oracle.com/en/java/javase/21/core/java-logging-overview.html)
- [logging.properties 默认配置](https://github.com/openjdk/jdk/blob/master/src/java.logging/share/conf/logging.properties)
- [JEP 264: Platform Logging API and Service](https://openjdk.org/jeps/264)
- [源码](https://github.com/openjdk/jdk/tree/master/src/java.logging/share/classes/java/util/logging)
- 本地源码: `src/java.logging/share/classes/`
