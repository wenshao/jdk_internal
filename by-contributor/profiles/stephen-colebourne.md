# Stephen Colebourne

> OpenGamma Engineering Lead | Java Champion | JavaOne Rock Star
>
> Joda-Time 创始人、JSR 310 Spec Lead、java.time API 设计者

---
## 目录

1. [概要](#1-概要)
2. [职业时间线](#2-职业时间线)
3. [Joda-Time：改变 Java 日期时间编程的库](#3-joda-time改变-java-日期时间编程的库)
4. [JSR 310 与 java.time：从社区项目到平台标准](#4-jsr-310-与-javatimefrom-社区项目到平台标准)
5. [ThreeTen 生态系统](#5-threeten-生态系统)
6. [Joda 开源项目家族](#6-joda-开源项目家族)
7. [OpenGamma Strata](#7-opengamma-strata)
8. [OpenJDK 贡献](#8-openjdk-贡献)
9. [演讲与社区影响](#9-演讲与社区影响)
10. [对 Java 生态的深远影响](#10-对-java-生态的深远影响)
11. [外部资源](#11-外部资源)

---

## 1. 概要

Stephen Colebourne 是 Java 生态系统中最具影响力的独立贡献者之一。他在 2002 年创建了 **Joda-Time**，这个第三方日期时间库迅速成为 Java 社区的事实标准 (de-facto standard)，解决了 `java.util.Date` 和 `java.util.Calendar` 长期被诟病的设计缺陷。随后，他作为 **JSR 310** 的 Specification Lead，将 Joda-Time 的核心理念提炼并重新设计为 `java.time` 包，通过 **JEP 150** 纳入 JDK 8，成为 Java 平台日期时间处理的永久标准。

他同时是 Apache Software Foundation 成员、Java Champion、JavaOne Rock Star 演讲者，以及金融分析公司 OpenGamma 的 Engineering Lead。

### 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Stephen Colebourne |
| **组织** | OpenGamma |
| **职位** | Engineering Lead |
| **所在地** | London, UK |
| **专长** | 日期时间 API 设计、金融分析、开源治理 |
| **GitHub** | [@jodastephen](https://github.com/jodastephen) |
| **博客** | [blog.joda.org](https://blog.joda.org/) |
| **荣誉** | Java Champion, JavaOne Rock Star, Apache Software Foundation Member |

---

## 2. 职业时间线

| 年份 | 事件 | 详情 |
|------|------|------|
| **2002** | 创建 Joda-Time | 为 Java 提供不可变、线程安全的日期时间 API |
| **2007** | 发起 JSR 310 | 提交 Date and Time API 规范请求，与 Michael Nascimento Santos 共同担任 Spec Lead |
| **2009** | 发表 "Why JSR-310 isn't Joda-Time" | 在博客阐述 java.time 从 Joda-Time 汲取教训但重新设计的理念 |
| **~2012** | 加入 OpenGamma | 担任 Engineering Lead，领导金融分析开源项目 |
| **2014 (JDK 8)** | java.time 正式发布 | JEP 150 / JSR 310 随 JDK 8 交付，彻底替代旧日期时间 API |
| **2014** | 发布迁移指南 | 在博客详细记录从 Joda-Time 迁移到 java.time 的路径 |
| **2017** | java.time JDK 9 增强 | 博客总结 JDK 9 对 java.time 的改进 |
| **2019** | Joda 项目商业支持 | 通过 Tidelift 为 Joda 和 ThreeTen 项目提供商业支持 |
| **持续至今** | 维护 ThreeTen 和 Joda 生态 | 持续维护 ThreeTen-Extra、Joda-Money、Joda-Beans 等项目 |

---

## 3. Joda-Time：改变 Java 日期时间编程的库

Java 原生的 `java.util.Date`（JDK 1.0）和 `java.util.Calendar`（JDK 1.1）存在可变性 (Mutable)、月份从 0 开始、`SimpleDateFormat` 线程不安全等众所周知的缺陷。Joda-Time 通过不可变对象 (Immutable)、清晰的类型分离（`LocalDate`、`LocalTime`、`DateTime` 等）、Fluent API 和可插拔日历系统 (Chronology) 彻底解决了这些问题，成为 Java 社区事实上的日期时间标准。

这种广泛采用直接促成了 JSR 310 的诞生——社区认为这些能力应该成为 Java 平台的一部分。

---

## 4. JSR 310 与 java.time：从社区项目到平台标准

### 4.1 JSR 310 的诞生

2007 年，Stephen Colebourne 提交了 JSR 310 (Date and Time API) 规范请求。他与 **Michael Nascimento Santos** 共同担任 Specification Lead，Oracle 的 **Roger Riggs** 则是实现层面的主要贡献者。

### 4.2 "Inspired by Joda-Time, not derived from it"

Stephen 在博客文章 "Why JSR-310 isn't Joda-Time" 中明确阐述：java.time 是受 Joda-Time 启发 (inspired by)，而非直接衍生 (derived from)。JSR 310 从 Joda-Time 的实践中汲取了大量教训，但进行了重要的重新设计：

| 方面 | Joda-Time | JSR 310 (java.time) |
|------|-----------|---------------------|
| **Null 处理** | 接受 null，用默认值替代 | 拒绝 null，抛出 NullPointerException |
| **内部实现** | 基于毫秒时间戳统一存储 | 各类型独立存储字段（年/月/日等） |
| **Chronology** | 复杂的可插拔日历系统 | 简化为 `java.time.chrono` 包 |
| **精度** | 毫秒 | 纳秒 |
| **与旧 API 互操作** | 提供转换方法 | 在旧类上添加桥接方法（如 `Date.toInstant()`） |

### 4.3 JEP 150：Date & Time API

| 属性 | 值 |
|------|-----|
| **JEP** | [JEP 150](https://openjdk.org/jeps/150) |
| **JSR** | [JSR 310](https://jcp.org/en/jsr/detail?id=310) |
| **JDK 版本** | JDK 8 (2014-03) |
| **状态** | Final |
| **Lead** | Stephen Colebourne (Independent) |

JEP 150 引入的 `java.time` 包核心类型包括 `LocalDate`、`LocalTime`、`LocalDateTime`、`ZonedDateTime`、`Instant`、`Duration`、`Period` 和 `DateTimeFormatter`。Stephen 为 java.time 确立的核心设计原则——不可变性 (Immutability)、人类时间与机器时间分离、ISO-8601 默认标准、Fluent API、明确拒绝 null——深刻影响了 Java API 设计的后续发展。

---

## 5. ThreeTen 生态系统

"ThreeTen" 这个名字来自 JSR **310** 的编号。Stephen Colebourne 围绕 java.time 建立了一个完整的生态系统：

### 5.1 ThreeTen-Extra

**仓库**: [ThreeTen/threeten-extra](https://github.com/ThreeTen/threeten-extra)

为 `java.time` 提供补充类型，这些类型因过于专业化而未被纳入 JDK 标准库：

| 类型 | 用途 |
|------|------|
| `Interval` | 时间区间（两个 Instant 之间） |
| `YearQuarter` | 年份 + 季度 |
| `YearWeek` | ISO 年份 + 周数 |
| `DayOfMonth` | 月份中的日 |
| `Days`, `Weeks`, `Months`, `Years` | 单一单位的时间量 |
| `PeriodDuration` | 组合 Period 和 Duration |

### 5.2 ThreeTen-Backport

**仓库**: [ThreeTen/threetenbp](https://github.com/ThreeTen/threetenbp)

将 java.time API 反向移植 (backport) 到 JDK 6 和 JDK 7。在 Android 生态中尤其重要——早期 Android 版本不支持 JDK 8 API，ThreeTen-Backport 配合 Jake Wharton 的 **ThreeTenABP** 成为 Android 开发者处理日期时间的标准方案。

Jake Wharton 的 [ThreeTenABP](https://github.com/JakeWharton/ThreeTenABP) 将 ThreeTen-Backport 适配到 Android 平台，进一步扩大了 java.time 设计在移动端的影响力。

---

## 6. Joda 开源项目家族

除了 Joda-Time，Stephen Colebourne 还创建和维护了一系列以 "Joda" 命名的高质量 Java 库：

| 项目 | 用途 | 仓库 |
|------|------|------|
| **Joda-Time** | 日期时间处理（JDK 8 前的标准） | [JodaOrg/joda-time](https://github.com/JodaOrg/joda-time) |
| **Joda-Money** | 货币与金额处理 | [JodaOrg/joda-money](https://github.com/JodaOrg/joda-money) |
| **Joda-Beans** | Java Bean 代码生成与属性系统 | [JodaOrg/joda-beans](https://github.com/JodaOrg/joda-beans) |
| **Joda-Convert** | 类型到字符串的转换框架 | [JodaOrg/joda-convert](https://github.com/JodaOrg/joda-convert) |
| **Joda-Collect** | 集合扩展工具 | [JodaOrg/joda-collect](https://github.com/JodaOrg/joda-collect) |

这些项目通过 Tidelift 提供商业支持，始终以宽松许可证 (permissive licence) 开源。

---

## 7. OpenGamma Strata

Stephen Colebourne 在 **OpenGamma** 担任 Engineering Lead，领导开发 **Strata**——一个现代化的开源金融市场风险分析库 (market risk library)，提供利率曲线构建、衍生品定价、市场风险计量等功能，基于 java.time 和 Joda-Beans 构建。Strata 是 Stephen 将 Java 开源理念应用于金融行业的实践。

---

## 8. OpenJDK 贡献

Stephen 对 OpenJDK 的贡献主要集中在 **JDK 8 开发周期**（java.time 的实现与集成）。由于 java.time 在 JDK 8 后已非常稳定，后续 PR 活动较少。他的贡献更偏向**规范设计层面**：作为 JSR 310 Spec Lead 定义 API 语义，与 Oracle 工程师（特别是 Roger Riggs）合作实现，并在 JDK 9 中推进增量改进。

---

## 9. 演讲与社区影响

### 9.1 主要演讲

| 演讲 | 场合 | 主题 |
|------|------|------|
| Date and Time API | JavaOne | JSR 310 设计理念与使用方式（JavaOne Rock Star 奖） |
| The New Java Best Practices | Devoxx Belgium | Java 最佳实践的现代演进 |
| Java Time | GOTO Amsterdam 2018 | 日期时间 API 设计经验 |
| 多次演讲 | JAX London, JAX Finance | Java 与金融技术 |
| 社区活动 | Paris JUG, London JUG | Java 生态与开源治理 |

### 9.2 博客：blog.joda.org

Stephen 的博客 [blog.joda.org](https://blog.joda.org/) 是 Java 社区的重要参考资源，涵盖：

- java.time 设计决策的深入解释
- Joda-Time 到 java.time 的迁移指南
- Java 语言演进的观点与评论
- 开源项目维护与商业可持续性的思考

### 9.3 社区角色

- **Java Champion**：Java 社区技术领袖荣誉
- **JavaOne Rock Star**：JavaOne 最受欢迎演讲者
- **Apache Software Foundation Member**：Apache 基金会成员
- **JCP Expert Group**：JSR 310 Expert Group 领导者

---

## 10. 对 Java 生态的深远影响

### 10.1 "社区驱动标准化"的典范

Stephen Colebourne 的贡献路径——从个人开源项目 (Joda-Time) 到 JCP 规范 (JSR 310) 再到平台标准 (java.time)——是 Java 社区驱动标准化的最佳案例之一。这条路径证明了：

1. **优秀的社区库可以推动平台演进**：Joda-Time 的广泛采用证明了旧 API 的不足
2. **规范化需要重新设计**：java.time 并非简单移植 Joda-Time，而是汲取教训后的全新设计
3. **独立贡献者可以主导核心 API**：Stephen 不是 Oracle 员工，但主导了 JDK 最重要的 API 之一

### 10.2 影响范围

| 领域 | 影响 |
|------|------|
| **JDK 标准库** | java.time 成为 JDK 8+ 日期时间处理的唯一推荐方案 |
| **Android 开发** | 通过 ThreeTen-Backport/ThreeTenABP 影响了数百万 Android 应用 |
| **API 设计理念** | 不可变性、Fluent API、null 拒绝等原则被后续 JDK API 广泛采用 |
| **金融行业** | OpenGamma Strata 将 Java 开源理念引入金融分析领域 |
| **生态迁移** | 推动了 Java 社区从旧 Date/Calendar 到 java.time 的大规模迁移 |

### 10.3 Joda-Time 到 java.time 的迁移故事

Stephen 没有将 Joda-Time 直接纳入 JDK，而是基于实践经验重新设计了全新 API，修正了已知缺陷。他于 2014 年发布了详尽的 [Converting from Joda-Time to java.time](https://blog.joda.org/2014/11/converting-from-joda-time-to-javatime.html) 迁移指南。Joda-Time 官方现在明确建议新项目使用 java.time。

---

## 11. 外部资源

| 类型 | 链接 |
|------|------|
| **GitHub** | [@jodastephen](https://github.com/jodastephen) |
| **博客** | [blog.joda.org](https://blog.joda.org/) |
| **Joda 项目主页** | [www.joda.org](https://www.joda.org/) |
| **ThreeTen 项目** | [www.threeten.org](https://www.threeten.org/) |
| **OpenGamma Strata** | [strata.opengamma.io](https://strata.opengamma.io/) |
| **SlideShare** | [scolebourne](https://www.slideshare.net/scolebourne) |
| **JEP 150** | [openjdk.org/jeps/150](https://openjdk.org/jeps/150) |
| **JSR 310** | [jcp.org/en/jsr/detail?id=310](https://jcp.org/en/jsr/detail?id=310) |
| **Heroes of Java 专访** | [blog.eisele.net](https://blog.eisele.net/2012/09/the-heroes-of-java-stephen-colebourne.html) |
| **Tidelift (商业支持)** | [opencollective.com/joda](https://opencollective.com/joda) |

---

> **数据调查时间**: 2026-03-22
> **文档版本**: 1.0
