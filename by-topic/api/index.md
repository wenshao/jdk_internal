# API 框架

> 集合框架、I/O 处理、日期时间、JDBC、日志、XML/JSON、异常处理

[← 返回主题索引](../)

---
## 目录

1. [演进概览](#1-演进概览)
2. [主题列表](#2-主题列表)
3. [核心贡献者](#3-核心贡献者)
4. [内部开发者资源](#4-内部开发者资源)
5. [统计数据](#5-统计数据)
6. [学习路径](#6-学习路径)
7. [相关链接](#7-相关链接)

---


## 1. 演进概览

```
JDK 1.0 ─── JDK 5 ─── JDK 8 ─── JDK 11 ─── JDK 21 ─── JDK 22 ─── JDK 24 ─── JDK 26
   │           │           │            │            │            │           │
 集合框架    泛型       Stream      HTTP Client  Sequenced   Stream     Stream
 I/O流      EnumSet/Map Optional    标准化     Collection Gatherers  增强
 Date       NIO        java.time   Collections  (JEP 431)  (JEP 485)  (最新)
```

### 版本里程碑

| 版本 | 主题 | 关键特性 | JEP |
|------|------|----------|-----|
| **JDK 1.2** | 集合框架 | Collections Framework 引入 | - |
| **JDK 1.4** | NIO | Buffer, Channel, Selector | JSR 51 |
| **JDK 5** | 类型安全 | 泛型、EnumSet/EnumMap、并发集合 | JSR 14 |
| **JDK 7** | NIO.2 | Path, Files, WatchService | JSR 203 |
| **JDK 8** | 函数式 API | Stream API、Optional、java.time | JEP 107, JSR 310 |
| **JDK 9** | 不可变集合 | List.of/Set.of/Map.of | - |
| **JDK 11** | HTTP 标准化 | HTTP Client 正式版 | JEP 321 |
| **JDK 16** | Stream 简化 | Stream.toList() | - |
| **JDK 17** | 增强随机数 | RandomGenerator | JEP 356 |
| **JDK 21** | 有序集合 | SequencedCollection | JEP 431 |
| **JDK 22** | 外部内存 | Foreign Memory API 正式 | JEP 454 |
| **JDK 24** | Stream 增强 | Stream Gatherers 正式 | JEP 485 |

---

## 2. 主题列表

### [集合框架](collections/)

Java 集合框架从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 1.0 | Vector, Hashtable | - |
| JDK 1.2 | Collections Framework | - |
| JDK 5 | Generics, EnumSet/EnumMap, Queue | JSR 14 |
| JDK 6 | NavigableSet/Map, BlockingQueue | - |
| JDK 8 | Stream API | JEP 107 |
| JDK 9 | List.of/Set.of/Map.of | - |
| JDK 16 | Stream.toList() | - |
| JDK 21 | SequencedCollection | JEP 431 |
| JDK 22 | Stream Gatherers (预览) | JEP 461 |
| JDK 24 | Stream Gatherers (正式) | JEP 485 |

→ [集合框架文档](collections/)

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

→ [I/O 演进文档](io/)

### [日期时间](datetime/)

java.time API 从旧 API 到现代日期时间处理的演进。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 1.0 | Date | - |
| JDK 1.1 | Calendar | - |
| JDK 8 | **java.time** (JSR 310) | JSR 310 |
| JDK 16 | Timeline Format | - |
| JDK 21 | Date/Calendar 废弃 | - |

→ [日期时间文档](datetime/)

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

→ [JDBC 文档](jdbc/)

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

→ [日志框架文档](logging/)

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

→ [XML/JSON 文档](xml-json/)

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

→ [异常处理文档](exceptions/)

---

## 3. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 集合/I/O (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Brian Burkhalter | 90 | Oracle | I/O, 字符串 |
| 2 | [Naoto Sato](/by-contributor/profiles/naoto-sato.md) | 84 | Oracle | 国际化, java.time |
| 3 | Doug Lea | 73 | SUNY Oswego | 并发集合 |
| 4 | [Claes Redestad](/by-contributor/profiles/claes-redestad.md) | 66 | Oracle | 性能优化 |
| 5 | Roger Riggs | 56 | Oracle | I/O, 工具类 |
| 6 | [Justin Lu](/by-contributor/profiles/justin-lu.md) | 52 | Oracle | 本地化 |
| 7 | Viktor Klang | 44 | Lightbend/Oracle | CompletableFuture |
| 8 | Stuart Marks | 44 | Oracle | 集合框架 |

### 日期时间 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | [Naoto Sato](/by-contributor/profiles/naoto-sato.md) | 64 | Oracle | java.time 主维护者 |
| 2 | [Shaojin Wen (温绍锦)](../../by-contributor/profiles/shaojin-wen.md) | 12 | Alibaba | 性能优化 |
| 3 | Roger Riggs | 12 | Oracle | 日期时间 |
| 4 | Claes Redestad | 8 | Oracle | 启动优化 |
| 5 | Andrey Turbanov | 7 | Oracle | 格式化 |

### 历史贡献者

| 贡献者 | 公司/机构 | 主要贡献 |
|--------|----------|----------|
| **Joshua Bloch** | Google/Sun | Collections Framework 设计 |
| **Doug Lea** | SUNY Oswego | 并发集合、ConcurrentHashMap |
| **Guy Steele** | Oracle | Stream API (JEP 107) |
| **Stephen Colebourne** | | JSR-310 (java.time) 规范负责人 |
| **Michael Nascimento** | | ThreeTen Extra 扩展库 |
| **Maurizio Cimadamore** | Oracle | Panama/Foreign Memory (JEP 454) |
| **Vladimir Ivanov** | Oracle | JIT 优化、Foreign 接口 |

---

## 4. 内部开发者资源

### 源码结构

```
src/java.base/share/classes/java/util/
├── ArrayList.java               # 数组列表
├── HashMap.java                 # 哈希表
├── ConcurrentHashMap.java       # 并发哈希表
├── stream/                      # Stream API
│   ├── Stream.java
│   ├── Collectors.java
│   └── Gatherer.java            # JDK 24+
├── ImmutableCollections.java    # 不可变集合
└── zip/                         # ZIP 压缩

src/java.base/share/classes/java/time/
├── LocalDate.java               # 本地日期
├── Instant.java                 # 时间戳
├── ZonedDateTime.java           # 时区日期时间
├── format/                      # 格式化
└── chrono/                      # 日历系统

src/java.base/share/classes/java/io/
├── InputStream.java             # 输入流
├── OutputStream.java            # 输出流
├── BufferedReader.java          # 缓冲读取
└── StringWriter.java            # 字符串写入

src/java.base/share/classes/nio/
├── ByteBuffer.java              # 字节缓冲区
├── channels/                    # 通道
├── file/                        # NIO.2 文件 API
└── charset/                     # 字符集

src/java.base/share/classes/jdk/internal/foreign/  # Foreign Memory 内部实现
```

### 关键内部类

| 类 | 作用 | 访问级别 |
|---|------|----------|
| `java.util.ImmutableCollections` | 不可变集合内部实现 | 包级私有 |
| `java.util.stream.Nodes` | Stream 中间节点 | 内部 |
| `java.util.stream.Gatherers` | Gatherer 实现 | 公共 (JDK 24+) |
| `jdk.internal.misc.Cleaner` | 清理器 (替代 finalize) | `@Restricted` |
| `jdk.internal.foreign.MemoryImpl` | Foreign Memory 实现 | 内部 |

### VM 参数速查

```bash
# Stream API
-Djava.util.stream.parallelism=8  # 并行流默认并行度

# I/O
-XX:MaxDirectMemorySize=512m     # 直接内存大小 (用于 NIO)

# Foreign Memory API
-XX:MaxDirectMemorySize=1G       # 外部内存限制

# 日期时间
-Duser.timezone=Asia/Shanghai    # 默认时区
-Djava.locale.providers=CLDR     # 使用 CLDR 本地化数据
```

---

## 5. 统计数据

| 指标 | 数值 |
|------|------|
| 集合实现类 | 40+ |
| Stream 操作符 | 50+ |
| java.time 类 | 30+ |
| I/O 实现类 | 60+ |
| JDBC 驱动类型 | 20+ |

---

## 6. 学习路径

1. **入门**: [集合框架](collections/) → [日期时间](datetime/) → 常用 API
2. **进阶**: [I/O 处理](io/) → [异常处理](exceptions/) → 核心编程能力
3. **深入**: [JDBC 数据库](jdbc/) → [XML/JSON](xml-json/) → 数据处理
4. **实践**: [日志框架](logging/) → 生产必备

---

## 7. 相关链接

### 外部资源

- [JEP 107: Stream API](https://openjdk.org/jeps/107)
- [JEP 356: Enhanced Random Number Generator](https://openjdk.org/jeps/356)
- [JEP 321: HTTP Client](https://openjdk.org/jeps/321)
- [JEP 431: Sequenced Collections](https://openjdk.org/jeps/431)
- [JEP 454](/jeps/ffi/jep-454.md)
- [JEP 485](/jeps/tools/jep-485.md)
- [JSR 310: Date and Time API](https://jcp.org/en/jsr/detail?id=310)
- [JSR 203: More New I/O APIs](https://jcp.org/en/jsr/detail?id=203)
- [JSR 221: JDBC 4.0](https://jcp.org/en/jsr/detail?id=221)

---

**最后更新**: 2026-03-20
