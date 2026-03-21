# Mark Reinhold

> Java Platform Chief Architect | Oracle
>
> Java 模块系统 (JPMS) 的总架构师，六个月发布节奏的推动者

---
## 目录

1. [概要](#1-概要)
2. [基本信息](#2-基本信息)
3. [职业时间线](#3-职业时间线)
4. [核心贡献](#4-核心贡献)
5. [OpenJDK 角色](#5-openjdk-角色)
6. [演讲与写作](#6-演讲与写作)
7. [设计哲学](#7-设计哲学)
8. [外部资源](#8-外部资源)

---


## 1. 概要

Mark Reinhold 是 Oracle 的 **Java Platform Group 首席架构师 (Chief Architect)**，自 1996 年加入 Sun Microsystems 以来，一直是 Java 平台演进的核心推动者。他拥有 MIT 计算机科学博士学位，研究方向涵盖垃圾回收、编译技术、类型系统与程序性能分析。

他最具影响力的两项工作是：主导 **Java 平台模块系统 (JPMS, Project Jigsaw)**，从根本上重构了 JDK 的架构；以及推动 **六个月发布节奏**，彻底改变了 Java 平台的交付方式。他目前领导 OpenJDK 社区的 JDK Project 和 Leyden Project，并担任 OpenJDK 理事会 (Governing Board) 成员。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Mark Reinhold |
| **组织** | [Oracle](/contributors/orgs/oracle.md) (Java Platform Group) |
| **角色** | Chief Architect, Java Platform Group |
| **教育背景** | Ph.D. Computer Science, MIT (垃圾回收、编译技术、类型系统) |
| **主要领域** | 平台架构、模块系统、发布策略、核心库 |
| **GitHub** | [@mbreinhold](https://github.com/mbreinhold) |
| **OpenJDK** | [mr](https://openjdk.org/census#mr) |
| **个人网站** | [mreinhold.org](https://mreinhold.org/) |
| **Inside.java** | [MarkReinhold](https://inside.java/u/MarkReinhold/) |
| **Mastodon** | [@mreinhold@mastodon.social](https://mastodon.social/@mreinhold) |
| **X (Twitter)** | [@mreinhold](https://x.com/mreinhold) |
| **活跃时间** | 1996 - 至今 (30 年) |

---

## 3. 职业时间线

| 年份 | 事件 | 详情 |
|------|------|------|
| **~1993** | MIT 博士学位 | 研究垃圾回收、编译技术、类型系统、程序性能可视化与分析 |
| **1996** | 加入 Sun Microsystems | 开始对 Java 平台的长期贡献 |
| **1998** | JDK 1.2 发布 | Lead Engineer，贡献 character-stream readers/writers |
| **2004** | JDK 5.0 发布 | Lead Engineer，推动 library generification |
| **2006** | Java SE 6 | Specification Lead |
| **2008** | Project Jigsaw 启动 | 开始 Java 模块化的长期规划 |
| **2010** | Sun 被 Oracle 收购 | 继续担任 Chief Architect |
| **2011** | JDK 7 发布 | Project Lead 和 Specification Lead |
| **2014** | JDK 8 发布 | Project Lead 和 Specification Lead |
| **2017-09** | JDK 9 发布 | JPMS 交付；提出六个月发布节奏 |
| **2018-至今** | 六个月发布节奏 | JDK 10 起每六个月发布一个 feature release |
| **2023** | Project Leyden | 领导 AOT/静态编译项目 |

---

## 4. 核心贡献

### 1. Java 平台模块系统 (JPMS / Project Jigsaw)

Mark Reinhold 最具标志性的工作。从 2008 年启动 Project Jigsaw，到 2017 年 JDK 9 正式交付，历时近十年。

| JEP/JSR | 名称 | 说明 |
|---------|------|------|
| **JSR 376** | Java Platform Module System | 模块系统规范，Mark Reinhold 任 Specification Lead |
| **JEP 200** | The Modular JDK | 定义 JDK 的模块化结构 (java.* 和 jdk.* 模块划分) |
| **JEP 201** | Modular Source Code | 将 JDK 源代码重构为模块化形式 (与 Alan Bateman 合作) |
| **JEP 261** | Module System | 模块系统的核心实现 |
| **JEP 220** | Modular Run-Time Images | 模块化运行时镜像 |
| **JEP 282** | jlink: The Java Linker | 自定义运行时镜像链接器 |

**核心目标**:
- **可靠的配置 (Reliable Configuration)**: 替代脆弱的 classpath 机制
- **强封装 (Strong Encapsulation)**: 模块内部实现细节不对外暴露
- **可扩展的平台 (Scalable Platform)**: JDK 可根据需要裁剪为更小的运行时

```java
// module-info.java 示例
module com.example.app {
    requires java.sql;
    requires java.logging;
    exports com.example.app.api;
}
```

### 2. 六个月发布节奏

2017 年 9 月，Mark Reinhold 正式提出将 Java 平台从传统的 **功能驱动、多年周期** 的发布模式，转变为 **严格的、基于时间的六个月发布** 模式。

| 要素 | 旧模式 | 新模式 (JDK 10 起) |
|------|--------|---------------------|
| **Feature Release** | 2-3 年 | 每 6 个月 (3月/9月) |
| **Update Release** | 不定期 | 每季度 |
| **LTS Release** | 无 | 每 2 年 (原为 3 年) |

**推动原因**:
- JDK 9 原计划 2.5 年交付，实际花费 3.5 年
- 功能驱动模式导致 release 不断延迟
- 开发者长期等待新特性，被迫大量 backport

**深远影响**:
- 使 Preview/Incubator 特性机制成为可能
- 新特性可以跨多个版本逐步成熟
- 大幅降低单次升级的风险和成本

### 3. 早期核心库贡献

在 JPMS 之前，Mark Reinhold 对 JDK 核心库有大量直接贡献：

| 特性 | JDK 版本 | 说明 |
|------|----------|------|
| **Character-stream readers/writers** | JDK 1.2 | 字符流 I/O 基础设施 |
| **Reference objects** | JDK 1.2 | SoftReference, WeakReference, PhantomReference |
| **Shutdown hooks** | JDK 1.3 | JVM 关闭时的清理机制 |
| **NIO (New I/O)** | JDK 1.4 | 高性能 I/O API (java.nio) |
| **Library generification** | JDK 5 | 核心库泛型化改造 |
| **Service loaders** | JDK 6 | java.util.ServiceLoader |

### 4. Project Leyden

当前正在领导的项目，目标是通过 AOT (Ahead-of-Time) 编译和静态分析技术改善 Java 应用的启动时间和性能：
- 与 [John Rose](./john-rose.md) 合作展示 Leyden 原型
- JVMLS 2023 演示中，Spring Boot 应用启动时间缩短 50-80%
- JEP 514 (AOT Command-Line Ergonomics) 和 JEP 515 (AOT Method Profiling) 是 Leyden 的成果

---

## 5. OpenJDK 角色

### 项目领导

| 项目/组 | 角色 |
|---------|------|
| **JDK Project** | Lead |
| **Jigsaw Project** | Lead |
| **Leyden Project** | Lead |
| **OpenJDK Governing Board** | Member (Oracle Lead) |

### JDK 版本领导历史

| JDK 版本 | 角色 |
|----------|------|
| **JDK 1.2** | Lead Engineer |
| **JDK 5.0** | Lead Engineer |
| **Java SE 6** | Specification Lead |
| **JDK 7** | Project Lead, Specification Lead |
| **JDK 8** | Project Lead, Specification Lead |
| **JDK 9** | Project Lead, Specification Lead |

---

## 6. 演讲与写作

### 重要演讲

| 演讲 | 场合 | 主题 |
|------|------|------|
| "The Modular JDK and Project Jigsaw" | Devoxx, JavaOne | JPMS 设计与实现 |
| "Moving Java Forward Faster" | 2017 | 六个月发布节奏提案 |
| "The State of OpenJDK" | FOSDEM 2008 | OpenJDK 社区状况 |
| "Project Leyden" | JVMLS 2023 | AOT 编译原型演示 (与 John Rose) |
| "Java, Today and Tomorrow" | FOSDEM 2025 | Java 平台现状与未来 |

### 博客

Mark Reinhold 在 [mreinhold.org/blog](https://mreinhold.org/blog/) 上发表关于 Java 平台方向的重要文章，是 Java 社区了解平台战略方向的重要窗口。

---

## 7. 设计哲学

### 平台级思维

Mark Reinhold 的工作始终以 **平台整体架构** 为出发点，而非单一特性。

| 原则 | 说明 | 案例 |
|------|------|------|
| **长期规划** | 愿意投入数年完成正确的设计 | Project Jigsaw 历时近 10 年 |
| **兼容性优先** | 大规模变更仍保持向后兼容 | JPMS 的 unnamed module 设计 |
| **流程创新** | 改进交付方式以改善平台演进 | 六个月发布节奏 + Preview 机制 |
| **实用主义** | 在理想与现实之间寻求平衡 | JPMS 的渐进式封装策略 |

---

## 8. 外部资源

| 类型 | 链接 |
|------|------|
| **个人网站** | [mreinhold.org](https://mreinhold.org/) |
| **Inside.java** | [MarkReinhold](https://inside.java/u/MarkReinhold/) |
| **GitHub** | [@mbreinhold](https://github.com/mbreinhold) |
| **Mastodon** | [@mreinhold@mastodon.social](https://mastodon.social/@mreinhold) |
| **X (Twitter)** | [@mreinhold](https://x.com/mreinhold) |
| **LinkedIn** | [markreinhold](https://www.linkedin.com/in/markreinhold/) |
| **OpenJDK Census** | [mr](https://openjdk.org/census#mr) |
| **博客** | [mreinhold.org/blog](https://mreinhold.org/blog/) |

### JEP/JSR 文档

- [JSR 376: Java Platform Module System](https://www.jcp.org/en/jsr/detail?id=376)
- [JEP 200: The Modular JDK](https://openjdk.org/jeps/200)
- [JEP 201: Modular Source Code](https://openjdk.org/jeps/201)
- [JEP 261: Module System](https://openjdk.org/jeps/261)
- [JEP 220: Modular Run-Time Images](https://openjdk.org/jeps/220)
- [JEP 282: jlink: The Java Linker](https://openjdk.org/jeps/282)

### 相关文章

- [Moving Java Forward Faster](https://mreinhold.org/blog/forward-faster) - 六个月发布节奏提案
- [Project Jigsaw: The Module System](https://mreinhold.org/blog/jigsaw-module-system) - 模块系统概述
- [Project Jigsaw](https://openjdk.org/projects/jigsaw/) - OpenJDK 项目页面

---

**来源**:
- [mreinhold.org](https://mreinhold.org/)
- [Inside.java - MarkReinhold](https://inside.java/u/MarkReinhold/)
- [GitHub - mbreinhold](https://github.com/mbreinhold)
- [OpenJDK Census](https://openjdk.org/census)
- [Crunchbase - Mark Reinhold](https://www.crunchbase.com/person/mark-reinhold)
- [FOSDEM 2025 - Mark Reinhold](https://archive.fosdem.org/2025/schedule/speaker/mark_reinhold/)
- [JCP - JSR 376](https://www.jcp.org/en/jsr/detail?id=376)

**最后更新**: 2026-03-22
