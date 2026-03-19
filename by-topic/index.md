# 按主题浏览

跨版本追踪某个技术领域的演进历程。

---

## 主题列表

### [GC 演进](gc/)

垃圾收集器的发展历程，从 Serial 到分代 ZGC。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 8 | G1 成为主流，CMS 标记废弃 | - |
| JDK 11 | ZGC 引入 (实验性) | JEP 333 |
| JDK 15 | ZGC 生产可用 | JEP 378 |
| JDK 17 | 并发线程栈扫描 | JEP 379 |
| JDK 21 | **分代 ZGC** (JEP 439)、分代 Shenandoah (JEP 429) | JEP 439, JEP 429 |
| JDK 23 | ZGC 分代改进 | JEP 474 |
| JDK 26 | G1 吞吐量提升 (JEP 522)、ZGC NUMA | JEP 522 |

→ [GC 时间线](gc/timeline.md)

### [并发编程](concurrency/)

从 Thread 到 Virtual Thread 的演进。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 5 | Executor 框架 | JSR-166 |
| JDK 7 | Fork/Join 框架 | JSR-166y |
| JDK 8 | Lambda、Parallel Stream | JEP 126 |
| JDK 8 | CompletableFuture | JEP 107 |
| JDK 9 | CompletableFuture 改进、Reactive Streams | JEP 266 |
| JDK 19 | **Virtual Threads** (预览) | JEP 425 |
| JDK 20 | Virtual Threads (第二次预览) | JEP 436 |
| JDK 21 | **Virtual Threads** (正式)、**Structured Concurrency** (预览)、**Scoped Values** (预览) | JEP 444, JEP 453, JEP 446 |
| JDK 22-26 | Structured Concurrency (持续预览) | JEP 462, 477, 483, 491, 493 |

→ [并发时间线](concurrency/timeline.md)

### [字符串处理](string/)

字符串相关优化和新特性。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 8 | StringJoiner | - |
| JDK 9 | **Compact Strings** (JEP 254)、invokedynamic 拼接 (JEP 280) | JEP 254, JEP 280 |
| JDK 11 | repeat()、strip()、isBlank()、lines() | - |
| JDK 15 | **Text Blocks** (正式) | JEP 378 |
| JDK 21 | String Templates (预览) | JEP 430 |
| JDK 24 | 隐藏类拼接策略 (+40% 启动性能) | JDK-8336856 |
| JDK 25 | String Templates (第二次预览) | JEP 459 |
| JDK 26 | Integer/Long.toString 优化 | JDK-8370503 |

→ [字符串优化时间线](string/timeline.md)

### [HTTP 客户端](http/)

从 HttpURLConnection 到 HTTP/3。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 1.0 | HttpURLConnection | - |
| JDK 9 | HTTP Client (孵化器) | JEP 110 |
| JDK 10 | HTTP Client (孵化器) | - |
| JDK 11 | **HTTP Client** (标准) | JEP 321 |
| JDK 16 | HTTP/2 支持 | - |
| JDK 22-23 | 连接复用优化 | - |
| JDK 26 | **HTTP/3** (预览) | JEP 517 |

→ [HTTP 演进时间线](http/timeline.md)

### [安全特性](security/)

加密、TLS、后量子密码。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 8 | TLS 1.2 (默认) | - |
| JDK 11 | **TLS 1.3** (默认)、ChaCha20-Poly1305 | JEP 332, JEP 329 |
| JDK 15 | 禁用弱签名算法 | - |
| JDK 17 | KMAC、SHA-3 家族 | JEP 370 |
| JDK 21 | 增强密码套件、HSS/LMS 签名 | - |
| JDK 22-23 | KDF API (预览) | JEP 495, JEP 508 |
| JDK 26 | **ML-DSA** 后量子签名、**KDF API** (正式)、**PEM 格式** | JEP 518, JEP 510, JEP 470 |

→ [安全特性时间线](security/timeline.md)

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

### [反射与元数据](reflection/)

反射、注解和字节码操作的演进。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 1.0 | 反射 API | - |
| JDK 5 | Annotations (JSR 175) | JSR 175 |
| JDK 6 | Pluggable Annotation Processing | JSR 269 |
| JDK 7 | MethodHandle (JSR 292) | JSR 292 |
| JDK 8 | Lambda invokedynamic, Parameter 反射 | - |
| JDK 11 | Constable/ConstantDesc | - |
| JDK 16 | ClassFile API | JEP 395 |
| JDK 26 | Mirror API | - |

→ [反射时间线](reflection/timeline.md)

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

### [模块系统](modules/)

Java 模块系统 (JPMS) 从 JDK 9 到现在的完整演进。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 9 | **JPMS** (JEP 261) | 模块化系统 |
| JDK 11 | jlink 定制运行时 | - |
| JDK 16 | 强封装 | - |
| JDK 17 | 遗留封装 | - |
| JDK 21 | 动态模块加载 | - |

→ [模块系统时间线](modules/timeline.md)

### [性能优化](performance/)

Java 性能优化从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 1.0 | 解释器执行 | 纯解释 |
| JDK 5 | JIT 编译器 (HotSpot) | 分层编译 |
| JDK 6 | 性能统计工具 | jstat/jmap |
| JDK 7 | G1 GC、Compressed Oops | 内存优化 |
| JDK 8 | Lambda/String Dedup | 编译优化 |
| JDK 17 | Record/Pattern Matching | 编译器优化 |
| JDK 21 | 虚拟线程 | I/O 性能提升 |

→ [性能优化时间线](performance/timeline.md)

### [内存管理](memory/)

Java 内存管理从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 5 | WeakReference 等 | 引用类型 |
| JDK 6 | Compressed Oops | 压缩指针 |
| JDK 8 | 元空间、String Dedup | 永久代移除 |
| JDK 11 | ZGC | 低延迟 GC |
| JDK 15 | ZGC 生产可用 | 正式版 |
| JDK 21 | 分代 ZGC | 降低 GC 频率 |
| JDK 22 | Foreign Memory Access | 堆外内存 |

→ [内存管理时间线](memory/timeline.md)

### [网络编程](network/)

Java 网络编程从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 1.0 | Socket/ServerSocket | TCP/UDP 基础 |
| JDK 1.1 | URL/HttpURLConnection | HTTP 支持 |
| JDK 5 | URLHandler | 自定义协议 |
| JDK 7 | Asynchronous I/O | 异步网络 |
| JDK 9 | HTTP/2 | 多路复用 |
| JDK 11 | HTTP Client 标准化 | 新 API |
| JDK 18 | Unix Domain Socket | 本地 IPC |

→ [网络编程时间线](network/timeline.md)

### [类加载器](classloading/)

Java 类加载器从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 1.0 | Bootstrap/Extension/Application | 三层类加载 |
| JDK 1.2 | 自定义 ClassLoader | 用户类加载 |
| JDK 5 | ContextClassLoader | SPI 支持 |
| JDK 6 | Instrumentation | Java Agent |
| JDK 6 | ServiceLoader | SPI 标准化 |
| JDK 9 | Platform ClassLoader | 模块化 |
| JDK 17 | 强封装 | 内部 API 限制 |

→ [类加载器时间线](classloading/timeline.md)

### [序列化](serialization/)

Java 序列化从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 1.0 | Serializable | 基础序列化 |
| JDK 5 | 枚举序列化 | Enum 支持 |
| JDK 7 | Externalizable 增强 | 自定义序列化 |
| JDK 17 | 密封序列化 | 序列化检查 |
| JDK 21 | Record 序列化 | 简化序列化 |

→ [序列化时间线](serialization/timeline.md)

### [国际化](i18n/)

Java 国际化 (i18n) 从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 1.0 | Locale, ResourceBundle | 基础 i18n |
| JDK 1.1 | DecimalFormat, SimpleDateFormat | 格式化 |
| JDK 5 | Formatter, MessageFormat | 增强格式化 |
| JDK 6 | Unicode 4.0 | 规范化 |
| JDK 8 | CLDR 数据 | 更准确本地化 |
| JDK 13 | Unicode 13 | 新字符支持 |
| JDK 18 | Unicode 扩展 | EAI 支持 |

→ [国际化时间线](i18n/timeline.md)

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

---

## 特性首发版本速查

### 语言特性

| 特性 | 首发版本 | 预览次数 | 正式版本 | JEP |
|------|----------|----------|----------|-----|
| Lambda | JDK 8 | - | JDK 8 | JEP 126 |
| Stream API | JDK 8 | - | JDK 8 | JEP 107 |
| Optional | JDK 8 | - | JDK 8 | JEP 150 |
| Module System | JDK 9 | - | JDK 9 | JEP 261 |
| Local Variable Type Inference | JDK 10 | - | JDK 10 | JEP 286 |
| Var Handles | JDK 9 | - | JDK 9 | JEP 193 |
| Records | JDK 14 | 2 | JDK 16 | JEP 395, JEP 384 |
| Pattern Matching for instanceof | JDK 14 | 2 | JDK 16 | JEP 375, JEP 305 |
| Sealed Classes | JDK 15 | 2 | JDK 17 | JEP 409, JEP 360 |
| Pattern Matching for switch | JDK 17 | 3 | JDK 21 | JEP 406, JEP 420, JEP 441 |
| Record Patterns | JDK 19 | 2 | JDK 21 | JEP 405, JEP 432, JEP 440 |
| String Templates | JDK 21 | 2+ | JDK 26+ | JEP 430, JEP 459 |
| Flexible Constructor Bodies | JDK 21 | 3 | JDK 25 | JEP 447, JEP 482, JEP 513 |
| Primitive Types in Patterns | JDK 23 | - | JDK 26 | JEP 455 |
| Implicit Classes | JDK 21 | 3 | JDK 23 | JEP 443, JEP 463, JEP 469 |
| Class File API | JDK 22 | - | JDK 23 | JEP 484 |

### 并发特性

| 特性 | 首发版本 | 预览次数 | 正式版本 | JEP |
|------|----------|----------|----------|-----|
| Virtual Threads | JDK 19 | 2 | JDK 21 | JEP 425, JEP 436, JEP 444 |
| Scoped Values | JDK 20 | 4+ | JDK 23+ | JEP 429, JEP 446, JEP 464, JEP 467 |
| Structured Concurrency | JDK 21 | 6+ | JDK 27+ | JEP 453, 462, 477, 483, 491, 493 |

### GC 特性

| 特性 | 首发版本 | 状态 | JEP |
|------|----------|------|-----|
| G1 GC | JDK 6 | 生产 | - |
| ZGC | JDK 11 | 生产 | JEP 333 |
| Shenandoah | JDK 12 | 生产 | JEP 379 |
| Generational ZGC | JDK 21 | 生产 | JEP 439 |
| Generational Shenandoah | JDK 21 | 生产 | JEP 429 |
| G1 Throughput Improvement | JDK 26 | 生产 | JEP 522 |

### 安全特性

| 特性 | 首发版本 | 状态 | JEP |
|------|----------|------|-----|
| TLS 1.3 | JDK 11 | 生产 | JEP 332 |
| ChaCha20-Poly1305 | JDK 11 | 生产 | JEP 329 |
| KMAC | JDK 17 | 生产 | JEP 370 |
| ML-DSA (后量子) | JDK 26 | 生产 | JEP 518 |
| ML-KEM (后量子) | JDK 26 | 生产 | - |
| KDF API | JDK 22 | 预览→正式JDK26 | JEP 495, 508, 510 |
| PEM Encodings | JDK 26 | 生产 | JEP 470 |

### API 特性

| 特性 | 首发版本 | 状态 | JEP |
|------|----------|------|-----|
| HTTP Client | JDK 11 | 生产 | JEP 321 |
| HTTP/3 | JDK 26 | 预览 | JEP 517 |
| Foreign Function & Memory API | JDK 22 | 生产 | JEP 454 |
| Vector API | JDK 16 | 预览→正式JDK23 | JEP 338, 417, 426, 448 |
| Stream API | JDK 8 | 生产 | JEP 107 |
| NIO.2 | JDK 7 | 生产 | JSR 203 |
| java.time | JDK 8 | 生产 | JSR 310 |

---

## 版本选择指南

### LTS 版本

| 版本 | 发布时间 | 支持状态 | 推荐场景 |
|------|----------|----------|----------|
| JDK 8 | 2014-03 | LTS (至 2030) | 遗留系统维护 |
| JDK 11 | 2018-09 | LTS (至 2032) | 稳定生产环境 |
| JDK 17 | 2021-09 | LTS (至 2029) | 现代应用首选 |
| JDK 21 | 2023-09 | LTS (至 2031) | 虚拟线程生产 |
| JDK 25 | 2025-09 | LTS | 当前 LTS |

### 选择决策树

```
┌─────────────────────────────────────────────────────────┐
│                    需求分析                              │
└─────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
        需要虚拟线程?                     其他需求
              │                               │
      ┌───────┴────────┐             ┌────────┴────────┐
      │                │             │                 │
     是                否          需要低延迟        需要HTTP/3
      │                │             │                 │
      ▼                ▼             ▼                 ▼
  JDK 21+          JDK 17+       JDK 21+           JDK 26+
  (推荐 25 LTS)    (稳定)        (分代ZGC)         (预览)
```

---

## 按领域选择 JDK 版本

### Web 应用

| 需求 | 推荐版本 | 理由 |
|------|----------|------|
| 传统应用 | JDK 11/17 | 稳定 LTS |
| 高并发 I/O | JDK 21+ | 虚拟线程 |
| 低延迟 GC | JDK 21+ | 分代 ZGC |
| 最新 HTTP | JDK 26 | HTTP/3 |

### 大数据处理

| 需求 | 推荐版本 | 理由 |
|------|----------|------|
| 传统批处理 | JDK 8/11 | 兼容性好 |
| 现代流处理 | JDK 17+ | Stream API 增强 |
| GPU 加速 | JDK 23+ | Vector API 正式 |

### 微服务

| 需求 | 推荐版本 | 理由 |
|------|----------|------|
| Spring Boot 3.x | JDK 17+ | 基线要求 |
| 虚拟线程支持 | JDK 21+ | Virtual Threads |
| 快速启动 | JDK 21+ | AOT 优化 |
| 低内存占用 | JDK 21+ | 分代 ZGC |

### 云原生

| 需求 | 推荐版本 | 理由 |
|------|----------|------|
| 容器优化 | JDK 17+ | 内存感知 |
| 快速启动 | JDK 21+ | AppCDS |
| 小镜像 | JDK 21+ | jlink 增强 |

---

## 性能提升汇总

### 启动性能

| 版本 | 特性 | 提升 |
|------|------|------|
| JDK 9 | AppCDS | +20% |
| JDK 12 | CDS 归档改进 | +10% |
| JDK 24 | 字符串拼接优化 | +40% |
| JDK 25 | 启动时间优化 | +15% |

### 吞吐量

| 版本 | 特性 | 提升 |
|------|------|------|
| JDK 24 | 隐藏类拼接 | +15% |
| JDK 25 | StringBuilder 优化 | +15% |
| JDK 26 | G1 Claim Table | +10-20% |

### 内存

| 版本 | 特性 | 节省 |
|------|------|------|
| JDK 9 | Compact Strings | -50% (ASCII) |
| JDK 21 | 分代 ZGC | -30% (大堆) |

---

## 相关链接

- [按版本浏览](/by-version/)
- [JEP 索引](/jeps/)
- [PR 分析](/by-pr/)
