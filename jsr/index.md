# JSR 索引

> Java Specification Requests — 共收录 **27 篇** JSR 分析文档，覆盖 Java 平台核心规范

[← 返回首页](../README.md)

---

## 目录

1. [什么是 JSR？](#1-什么是-jsr)
2. [JSR vs JEP](#2-jsr-vs-jep)
3. [按时代浏览](#3-按时代浏览)
4. [按主题浏览](#4-按主题浏览)
5. [JCP 治理演进](#5-jcp-治理演进)
6. [关键人物](#6-关键人物)
7. [相关链接](#7-相关链接)

---

## 1. 什么是 JSR？

JSR (Java Specification Request) 是通过 **JCP (Java Community Process)** 提交和审批的 Java 平台正式规范。每个 JSR 定义一组 API 契约或语言语法变更，需经过 JCP 执行委员会投票通过。

### JSR 生命周期

```
Draft Review → Early Draft → Public Review → Proposed Final → Final Release
   几周         1-3个月        30-90天          投票期           完成
```

| 状态 | 说明 |
|------|------|
| ✅ Final Release | 已发布的最终规范 |
| ❌ Withdrawn | 已撤回 |
| 💤 Dormant | 长期无进展 |

---

## 2. JSR vs JEP

| 维度 | JSR | JEP |
|------|-----|-----|
| **治理** | JCP 执行委员会投票 | OpenJDK 项目组决定 |
| **性质** | 规范 (Specification) | 实现 (Implementation) |
| **内容** | API 契约、语言语法、平台版本 | 实现细节、JVM 优化、工具 |
| **生命周期** | 独立编号 (JSR 335) | 绑定 JDK 版本 (JEP 444 = JDK 21) |
| **外部参与** | Expert Group（多组织） | 以 Oracle 为主 |

### 何时需要 JSR vs JEP？

| 变更类型 | JSR | JEP | 示例 |
|----------|-----|-----|------|
| 新语言语法 | ✅ | 同时 | Lambda (JSR 335 + JEP 126) |
| 新标准 API | ✅ | 同时 | java.time (JSR 310 + JEP 150) |
| 平台版本发布 | ✅ | - | Java SE 25 (JSR 400) |
| JVM 内部优化 | - | ✅ | ZGC (JEP 333), Virtual Threads (JEP 444) |
| GC / 编译器 | - | ✅ | AOT Cache (JEP 516) |
| 工具改进 | - | ✅ | jshell (JEP 222) |

### JSR-JEP 对照表

| 特性 | JSR | JEP | 关系 |
|------|-----|-----|------|
| Generics | [JSR 14](language/jsr-14.md) | - | JSR only (JDK 5) |
| Annotations | [JSR 175](language/jsr-175.md) | - | JSR only (JDK 5) |
| Concurrency | [JSR 166](api/jsr-166.md) | - | JSR only (JDK 5) |
| JMM | [JSR 133](language/jsr-133.md) | - | JSR only (JDK 5) |
| NIO | [JSR 51](api/jsr-51.md) | - | JSR only (JDK 1.4) |
| NIO.2 | [JSR 203](api/jsr-203.md) | - | JSR only (JDK 7) |
| invokedynamic | [JSR 292](language/jsr-292.md) | - | JSR only (JDK 7) |
| Lambda | [JSR 335](language/jsr-335.md) | [JEP 126](/jeps/language/jep-126.md) | JSR 定义语法 + JEP 实现 |
| Date/Time | [JSR 310](api/jsr-310.md) | [JEP 150](/jeps/language/jep-150.md) | JSR 定义 API + JEP 实现 |
| Modules | [JSR 376](platform/jsr-376.md) | [JEP 261](/jeps/language/jep-261.md) | JSR 定义规范 + JEP 实现 |
| Records | [JSR 395](language/jsr-395.md) | [JEP 395](/jeps/language/jep-395.md) | 同编号 |
| Sealed Classes | [JSR 397](language/jsr-397.md) | [JEP 409](/jeps/language/jep-409.md) | 不同编号 |
| Virtual Threads | 无 JSR | [JEP 444](/jeps/concurrency/jep-444.md) | 纯 JEP (JVM 实现) |
| ZGC | 无 JSR | [JEP 333](/jeps/gc/jep-333.md) | 纯 JEP (GC) |

> **趋势**: JDK 9 之后，越来越多特性跳过 JSR 直接通过 JEP 交付。平台版本 JSR (如 JSR 400) 仍然作为"伞规范"覆盖每个 LTS 版本的新增特性。

---

## 3. 按时代浏览

### JDK 5 — "现代 Java 的起点" (2004)

JDK 5 是 Java 语言最大的一次变革，通过 6 个 JSR 奠定了现代 Java 的基础：

| JSR | 标题 | 影响 |
|-----|------|------|
| [JSR 14](language/jsr-14.md) | **Generics** | 类型安全集合，消除强制转换 |
| [JSR 133](language/jsr-133.md) | **Java Memory Model** | 并发编程的理论基础 |
| [JSR 166](api/jsr-166.md) | **Concurrency Utilities** | java.util.concurrent，替代手写同步 |
| [JSR 175](language/jsr-175.md) | **Annotations** | @interface 语法，元编程基础 |
| [JSR 201](language/jsr-201.md) | **Enums, Autoboxing, Enhanced For** | 语法便利性 |

### JDK 6-7 — "工具与基础设施" (2006-2011)

| JSR | 标题 | 影响 |
|-----|------|------|
| [JSR 199](api/jsr-199.md) | Java Compiler API | javax.tools 编程式编译 |
| [JSR 223](api/jsr-223.md) | Scripting for Java | javax.script 脚本引擎 |
| [JSR 250](api/jsr-250.md) | Common Annotations | @Resource, @PostConstruct |
| [JSR 269](language/jsr-269.md) | Pluggable Annotation Processing | APT，编译时代码生成 |
| [JSR 221](api/jsr-221.md) | JDBC 4.0 | ServiceLoader 自动发现 |
| [JSR 173](api/jsr-173.md) | StAX | XMLStreamReader 拉式解析 |
| [JSR 51](api/jsr-51.md) | NIO | Channel/Buffer/Selector (JDK 1.4) |
| [JSR 203](api/jsr-203.md) | NIO.2 | java.nio.file, 异步 I/O (JDK 7) |
| [JSR 292](language/jsr-292.md) | **invokedynamic** | MethodHandle，Lambda 的基石 (JDK 7) |

### JDK 8 — "函数式革命" (2014)

| JSR | 标题 | 影响 |
|-----|------|------|
| [JSR 335](language/jsr-335.md) | **Lambda Expressions** | 函数式编程，Stream API |
| [JSR 308](language/jsr-308.md) | Annotations on Java Types | TYPE_USE 注解 |
| [JSR 310](api/jsr-310.md) | **Date and Time API** | java.time，替代 Date/Calendar |

### JDK 9-17 — "模块化与代数数据类型" (2017-2021)

| JSR | 标题 | 影响 |
|-----|------|------|
| [JSR 376](platform/jsr-376.md) | **Module System (JPMS)** | 模块化，强封装 (JDK 9) |
| [JSR 395](language/jsr-395.md) | Records | 不可变数据载体 (JDK 16) |
| [JSR 397](language/jsr-397.md) | Sealed Classes | 受限继承层次 (JDK 17) |

### JDK 25 — "最新 LTS 平台" (2025)

| JSR | 标题 | 影响 |
|-----|------|------|
| [JSR 400](platform/jsr-400.md) | **Java SE 25 Platform** | 伞规范，覆盖 JDK 22-25 所有新特性 |

### Java EE / Jakarta EE

| JSR | 标题 | 影响 |
|-----|------|------|
| [JSR 330](api/jsr-330.md) | Dependency Injection | @Inject, Spring/Guice 基础 |
| [JSR 250](api/jsr-250.md) | Common Annotations | @PostConstruct/@PreDestroy |
| [JSR 339](api/jsr-339.md) | JAX-RS 2.0 | RESTful Web Services |
| [JSR 354](api/jsr-354.md) | Money and Currency | MonetaryAmount (独立库) |
| [JSR 367](api/jsr-367.md) | JSON-B | 对象↔JSON 绑定 |
| [JSR 374](api/jsr-374.md) | JSON-P 1.1 | JsonPointer/JsonPatch |
| [JSR 380](api/jsr-380.md) | Bean Validation 2.0 | @NotNull/@Valid |

---

## 4. 按主题浏览

### 语言规范 (11 篇)

| JSR | 标题 | JDK | 说明 |
|-----|------|-----|------|
| [JSR 397](language/jsr-397.md) | Sealed Classes | 17 | 密封类，穷举 switch |
| [JSR 395](language/jsr-395.md) | Records | 16 | 记录类，不可变数据 |
| [JSR 335](language/jsr-335.md) | Lambda Expressions | 8 | Lambda、Stream、默认方法 |
| [JSR 308](language/jsr-308.md) | Type Annotations | 8 | TYPE_USE, Checker Framework |
| [JSR 292](language/jsr-292.md) | invokedynamic | 7 | MethodHandle, 动态语言 |
| [JSR 269](language/jsr-269.md) | Annotation Processing | 6 | APT, 编译时代码生成 |
| [JSR 201](language/jsr-201.md) | Enums, Autoboxing | 5 | 枚举、自动装箱、增强 for |
| [JSR 175](language/jsr-175.md) | Annotations | 5 | @interface, 元注解 |
| [JSR 133](language/jsr-133.md) | Java Memory Model | 5 | happens-before, volatile |
| [JSR 14](language/jsr-14.md) | Generics | 5 | 类型擦除、通配符、PECS |
| [Valhalla](language/valhalla-value-types.md) | Value Types | - | 进行中 (~~JSR 409~~ 已撤回) |

### API 规范 (15 篇)

| JSR | 标题 | JDK/EE | 说明 |
|-----|------|--------|------|
| [JSR 380](api/jsr-380.md) | Bean Validation 2.0 | EE 8 | @NotNull/@Valid |
| [JSR 374](api/jsr-374.md) | JSON-P 1.1 | EE 8 | JsonPointer/JsonPatch |
| [JSR 367](api/jsr-367.md) | JSON-B | EE 8 | 对象↔JSON 绑定 |
| [JSR 354](api/jsr-354.md) | Money & Currency | 独立 | MonetaryAmount |
| [JSR 339](api/jsr-339.md) | JAX-RS 2.0 | EE 7 | REST Web Services |
| [JSR 330](api/jsr-330.md) | Dependency Injection | EE 6 | @Inject/@Named |
| [JSR 310](api/jsr-310.md) | Date & Time API | 8 | java.time |
| [JSR 250](api/jsr-250.md) | Common Annotations | 6 | @Resource/@PostConstruct |
| [JSR 223](api/jsr-223.md) | Scripting | 6 | javax.script |
| [JSR 221](api/jsr-221.md) | JDBC 4.0 | 6 | ServiceLoader 发现 |
| [JSR 203](api/jsr-203.md) | NIO.2 | 7 | java.nio.file |
| [JSR 199](api/jsr-199.md) | Compiler API | 6 | javax.tools |
| [JSR 173](api/jsr-173.md) | StAX | 6 | XMLStreamReader |
| [JSR 166](api/jsr-166.md) | Concurrency | 5 | java.util.concurrent |
| [JSR 51](api/jsr-51.md) | NIO | 1.4 | Channel/Buffer/Selector |

### 平台规范 (2 篇)

| JSR | 标题 | 版本 | 说明 |
|-----|------|------|------|
| [JSR 400](platform/jsr-400.md) | Java SE 25 | 25 (LTS) | 最新 LTS 平台 |
| [JSR 376](platform/jsr-376.md) | Java SE 9 | 9 | 模块系统 (JPMS) |

---

## 5. JCP 治理演进

### 从 JCP 到 OpenJDK 的权力转移

```
2004-2010: JSR 主导时代
├── 所有语言变更和 API 必须通过 JSR
├── Expert Group 多组织参与
└── Sun/Oracle 掌控 JCP 执行委员会

2011-2017: 过渡时代
├── OpenJDK 成为 Java SE 参考实现
├── JEP 流程建立（JDK 8 开始）
├── JSR 仍用于语言/API 变更
└── 平台 JSR 开始作为"伞规范"

2017-至今: JEP 主导时代
├── JDK 9 后采用 6 个月发布节奏
├── 大多数特性直接通过 JEP 交付
├── 平台 JSR 仅覆盖 LTS 版本 (JSR 396/400)
├── 语言/API JSR 减少 (Records/Sealed 是最后两个)
└── Virtual Threads、ZGC、Panama 等均无 JSR
```

### 为什么 JSR 减少了？

| 因素 | 说明 |
|------|------|
| **发布节奏加快** | 6 个月 vs JSR 的年级审批周期 |
| **Preview 机制** | JEP Preview 替代了 JSR 的多轮审查 |
| **OpenJDK 主导** | Oracle 主导开发，外部参与通过 OpenJDK 而非 JCP |
| **API 稳定** | 新特性多为 JVM/编译器层面，不需要规范变更 |
| **Jakarta EE 分离** | 企业 API 迁移到 Eclipse Foundation |

---

## 6. 关键人物

| 人物 | 主要 JSR | 组织 | 贡献 |
|------|---------|------|------|
| [Doug Lea](/by-contributor/profiles/doug-lea.md) | JSR 133, 166 | SUNY Oswego | JMM + java.util.concurrent，并发编程之父 |
| [Brian Goetz](/by-contributor/profiles/brian-goetz.md) | JSR 335, 395, 397 | Oracle | Lambda + Records + Sealed Classes，Java 语言架构师 |
| [Joshua Bloch](https://en.wikipedia.org/wiki/Joshua_Bloch) | JSR 175, 201 | Google (前 Sun) | Annotations + Enums，《Effective Java》作者 |
| [Mark Reinhold](/by-contributor/profiles/mark-reinhold.md) | JSR 51, 376 | Oracle | NIO + Module System，Java 首席架构师 |
| [Stephen Colebourne](/by-contributor/profiles/stephen-colebourne.md) | JSR 310 | OpenGamma | java.time API，Joda-Time 创建者 |
| [Gilad Bracha](https://en.wikipedia.org/wiki/Gilad_Bracha) | JSR 14 | (前 Sun) | Generics 设计者，类型擦除决策 |
| [Bill Pugh](https://en.wikipedia.org/wiki/Bill_Pugh) | JSR 133 | UMD | Java Memory Model，FindBugs 创建者 |
| [John Rose](/by-contributor/profiles/john-rose.md) | JSR 292 | Oracle | invokedynamic，JVM 架构师 |
| [Bob Lee](https://en.wikipedia.org/wiki/Bob_Lee_(programmer)) | JSR 330 | Google (前) | @Inject，Guice 创建者 |
| [Gavin Bierman](/by-contributor/profiles/gavin-bierman.md) | JSR 395, 397 | Oracle | Records + Sealed Classes + Pattern Matching |

---

## 7. 相关链接

### 内部文档

- [JEP 索引](/jeps/) — 197 篇 JEP 分析文档
- [语言特性演进](/by-topic/language/)
- [核心平台](/by-topic/core/)

### 外部资源

- [JCP 官网](https://jcp.org/)
- [JSR 列表](https://jcp.org/en/jsr/all)
- [OpenJDK JEPs](https://openjdk.org/jeps/)
- [Jakarta EE Specifications](https://jakarta.ee/specifications/)
