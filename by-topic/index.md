# 按主题浏览

跨版本追踪某个技术领域的演进历程。

---

## 分类导航

### [核心平台](core/)

JVM、内存、性能、模块系统等底层技术。

| 主题 | 说明 | 首发版本 |
|------|------|----------|
| [GC 演进](core/gc/) | 垃圾收集器发展历程 | JDK 1.0 |
| [内存管理](core/memory/) | 堆、栈、Metaspace、Compressed Oops | JDK 1.0 |
| [JIT 编译](core/jit/) | C2 编译器、分层编译、内联优化 | JDK 1.0 |
| [性能优化](core/performance/) | 逃逸分析、JFR、性能调优 | JDK 1.0 |
| [类加载器](core/classloading/) | 双亲委派、模块化加载、Instrumentation | JDK 1.0 |
| [模式匹配](core/patterns/) | 类型模式、Record 模式、解构 | JDK 14 |
| [泛型系统](core/generics/) | 类型参数、通配符、类型擦除 | JDK 5 |
| [Record 类型](core/records/) | 不可变数据载体、Compact Constructor | JDK 14 |
| [模块系统](core/modules/) | JPMS、module-info、jlink | JDK 9 |

### [语言特性](language/)

语法、类型、反射等语言层面演进。

| 主题 | 说明 | 首发版本 |
|------|------|----------|
| [字符串处理](language/string/) | String、StringBuilder、Text Blocks | JDK 1.0 |
| [反射与元数据](language/reflection/) | 反射、注解、MethodHandle | JDK 1.0 |
| [语法演进](language/syntax/) | 泛型、枚举、Lambda、Record、Pattern Matching | - |
| [Lambda 表达式](language/lambda/) | 函数式接口、方法引用、闭包 | JDK 8 |
| [Stream API](language/streams/) | 函数式数据处理、流式操作 | JDK 8 |
| [注解与元编程](language/annotations/) | 注解处理器、编译期元编程 | JDK 5 |
| [Class File API](language/classfile/) | Class 文件读写 API | JDK 22 |

### [API 框架](api/)

标准库框架和工具类。

| 主题 | 说明 | 首发版本 |
|------|------|----------|
| [集合框架](api/collections/) | List、Set、Map、Stream API | JDK 1.0 |
| [I/O 处理](api/io/) | BIO、NIO、NIO.2、Foreign Memory | JDK 1.0 |
| [JDBC 数据库](api/jdbc/) | JDBC 1.x → JDBC 4.4 | JDK 1.1 |
| [日志框架](api/logging/) | System.out → JUL → SLF4J/Logback | JDK 1.0 |
| [XML/JSON](api/xml-json/) | DOM/SAX/StAX、Jackson、Gson | JDK 1.4 |

### [日期时间](datetime/)

现代日期时间处理 API。

| 主题 | 说明 | 首发版本 |
|------|------|----------|
| [java.time](datetime/) | JSR 310、LocalDate、ZonedDateTime | JDK 8 |

### [并发网络](concurrency/)

多线程、网络通信、异步编程。

| 主题 | 说明 | 首发版本 |
|------|------|----------|
| [并发编程](concurrency/concurrency/) | Thread、Executor、Virtual Threads | JDK 1.0 |
| [HTTP 客户端](concurrency/http/) | HttpURLConnection → HTTP/3 | JDK 1.0 |
| [网络编程](concurrency/network/) | Socket、NIO、Unix Domain Socket | JDK 1.0 |
| [序列化](concurrency/serialization/) | Serializable、Externalizable | JDK 1.0 |

### [安全国际化](security/)

加密、TLS、本地化等。

| 主题 | 说明 | 首发版本 |
|------|------|----------|
| [安全特性](security/security/) | 加密、TLS、后量子密码 | JDK 1.0 |
| [国际化](security/i18n/) | Locale、ResourceBundle、Unicode | JDK 1.0 |

### [专题深入](net/)

网络、I/O、加密、数学等核心技术深入讲解。

| 主题 | 说明 | 首发版本 |
|------|------|----------|
| [网络编程](net/) | Socket、HTTP Client、WebSocket | JDK 1.0 |
| [NIO 新 I/O](nio/) | Buffer、Channel、Selector、NIO.2 | JDK 1.4 |
| [加密与安全](crypto/) | JCE、Cipher、Signature、SSL/TLS | JDK 1.0 |
| [数学计算](math/) | BigDecimal、BigInteger、Random | JDK 1.0 |

---

## 学习路径

### 初级路径

```
1. language/syntax/     → 基础语法
2. language/string/     → 字符串使用
3. api/collections/     → 集合操作
4. datetime/            → 日期处理
```

### 中级路径

```
1. api/io/              → I/O 编程
2. concurrency/concurrency/ → 多线程基础
3. concurrency/http/    → HTTP 客户端
4. api/xml-json/        → 数据格式
```

### 高级路径

```
1. core/gc/             → GC 调优
2. core/memory/         → 内存管理
3. core/performance/    → 性能优化
4. core/modules/        → 模块化
```

### 专家路径

```
1. core/classloading/   → 类加载机制
2. security/security/   → 安全加密
3. concurrency/concurrency/ → Virtual Threads
4. language/reflection/ → 元编程
```

---

## 场景索引

### "我要优化性能..."

| 场景 | 查看 |
|------|------|
| 应用启动慢 | core/performance/ → JIT 编译 |
| 内存占用高 | core/memory/ → Compressed Oops |
| GC 频繁停顿 | core/gc/ → G1/ZGC/Shenandoah |
| 字符串内存大 | language/string/ → Compact Strings |

### "我要做并发编程..."

| 场景 | 查看 |
|------|------|
| 普通多线程 | concurrency/concurrency/ → Executor |
| 高并发 I/O | concurrency/concurrency/ → Virtual Threads |
| 异步网络 | concurrency/network/ → Asynchronous I/O |
| HTTP 调用 | concurrency/http/ → HTTP Client |

### "我要做数据持久化..."

| 场景 | 查看 |
|------|------|
| 数据库访问 | api/jdbc/ |
| 对象序列化 | concurrency/serialization/ |
| JSON 处理 | api/xml-json/ |
| 文件 I/O | api/io/ |

### "我要升级 JDK..."

| 场景 | 查看 |
|------|------|
| 8 → 11 | core/modules/ → JPMS 基础 |
| 8 → 17 | api/datetime/ → Date 废弃 |
| 11 → 21 | concurrency/concurrency/ → Virtual Threads |
| 17 → 26 | concurrency/http/ → HTTP/3 |

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
