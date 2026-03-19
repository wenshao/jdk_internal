# API 框架

标准库框架和工具类。

---

## 主题列表

### [集合框架](collections/)

Java 集合框架从 JDK 1.0 到现在的完整演进。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 1.0 | Vector, Hashtable | - |
| JDK 1.2 | Collections Framework | - |
| JDK 5 | Generics, EnumSet/EnumMap, Queue | JSR 14 |
| JDK 6 | NavigableSet/Map, BlockingQueue | - |
| JDK 8 | Stream API | JEP 107 |
| JDK 9 | List.of/Set.of/Map.of | - |
| JDK 16 | Stream.toList() | - |
| JDK 21 | Stream Gatherers (预览) | JEP 461 |

→ [集合框架时间线](collections/timeline.md)

### [I/O 处理](io/)

Java I/O 从传统 BIO 到 Foreign Memory Access 的演进。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 1.0 | InputStream/OutputStream, Reader/Writer | - |
| JDK 1.4 | NIO (Buffer, Channel, Selector) | JSR 51 |
| JDK 5 | Scanner, Formatter | - |
| JDK 7 | NIO.2 (Path, Files, WatchService) | JSR 203 |
| JDK 11 | Files.readString/writeString | - |
| JDK 22 | Foreign Memory Access | JEP 454 |

→ [I/O 演进时间线](io/timeline.md)

### [日期时间](datetime/)

java.time API 从旧 API 到现代日期时间处理的演进。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 1.0 | Date | - |
| JDK 1.1 | Calendar | - |
| JDK 8 | **java.time** (JSR 310) | JSR 310 |
| JDK 16 | Timeline Format | - |
| JDK 21 | Date/Calendar 废弃 | - |

→ [日期时间时间线](datetime/timeline.md)

### [JDBC 数据库](jdbc/)

数据库连接从 JDBC 1.x 到 JDBC 4.4 的演进。

| 版本 | 主要变化 | JSR |
|------|----------|-----|
| JDK 1.1 | JDBC 1.x | - |
| JDK 4 | JDBC 3.0 | JSR 114 |
| JDK 5 | JDBC 4.0 | JSR 221 |
| JDK 7 | JDBC 4.1 | JSR 221 |
| JDK 11 | JDBC 4.3 | JSR 221 |
| JDK 26 | JDBC 4.4 | JSR 221 |

→ [JDBC 时间线](jdbc/timeline.md)

### [日志框架](logging/)

从 System.out 到 Logback 的日志演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 1.0 | System.out | 控制台输出 |
| JDK 1.4 | JUL (java.util.logging) | 内置日志 |
| 2002 | Log4j 1.x | Apache 日志框架 |
| 2005 | SLF4J | 日志门面 |
| 2006 | Logback | SLF4J 原生实现 |
| 2014 | Log4j 2.x | 重写版本 |
| JDK 9 | System.Logger | 统一日志接口 |

→ [日志框架时间线](logging/timeline.md)

### [XML/JSON 处理](xml-json/)

XML 和 JSON 处理从 DOM 到现代 API 的演进。

| 版本 | 主要变化 | JSR |
|------|----------|-----|
| JDK 4 | DOM/SAX | - |
| JDK 5 | JAXB 1.0 | JSR 31 |
| JDK 6 | StAX | JSR 173 |
| JDK 7 | JSON-P 1.0 | JSR 353 |
| JDK 9 | JAXB 标记废弃 | - |
| JDK 11 | JSON-P 1.1 | - |
| JDK 21 | JSON-P 2.1 | - |

→ [XML/JSON 时间线](xml-json/timeline.md)

### [异常处理](exceptions/)

异常处理从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 1.0 | try-catch-finally | 基础异常处理 |
| JDK 1.4 | 异常链 | getCause() |
| JDK 7 | Try-with-resources | 自动资源管理 |
| JDK 7 | 多异常捕获 | catch (A \| B e) |
| JDK 16 | 异常记录 SPI | 自定义异常处理 |
| JDK 21 | 模式匹配异常 | instanceof with pattern |

→ [异常处理时间线](exceptions/timeline.md)

---

## 学习路径

1. **入门**: [集合框架](collections/) → [日期时间](datetime/) → 常用 API
2. **进阶**: [I/O 处理](io/) → [异常处理](exceptions/) → 核心编程能力
3. **深入**: [JDBC 数据库](jdbc/) → [XML/JSON](xml-json/) → 数据处理
4. **实践**: [日志框架](logging/) → 生产必备
