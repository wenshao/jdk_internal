# John Rose

> **Inside.java**: [JohnRose](https://inside.java/u/JohnRose/)
> **OpenJDK**: [jrose](https://openjdk.org/census#jrose)
> **GitHub**: [rose00](https://github.com/rose00)
> **X (Twitter)**: [@JohnRose00](https://x.com/JohnRose00)
> **Oracle Blog**: [blogs.oracle.com/jrose](https://blogs.oracle.com/jrose/)
> **Organization**: [Oracle](../../contributors/orgs/oracle.md) (Java Platform Group)
> **Role**: Senior Architect, Java Virtual Machine

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [主要 JEP 贡献](#3-主要-jep-贡献)
4. [核心技术贡献](#4-核心技术贡献)
5. [协作网络](#5-协作网络)
6. [学术贡献](#6-学术贡献)
7. [开发风格](#7-开发风格)
8. [技术影响力](#8-技术影响力)
9. [相关链接](#9-相关链接)

---


## 1. 概述

John Rose (OpenJDK 用户名：**jrose**) 是 Oracle 的 **JVM 高级架构师 (Senior Architect)**，自 1995 年起在 Sun Microsystems（后归入 Oracle）从事 Java 技术工作，涵盖从硬件架构、代码生成器到库和编程语言等广泛领域。在加入 Sun 之前，他曾在 Thinking Machines Corporation 与 Guy Steele、Stephen Wolfram 共同发明了 C* 并行编程语言。

他是 JVM 动态语言支持的奠基人，主导了 **invokedynamic** 字节码指令 (JSR 292) 和 **method handles** 的设计与实现，使 Java 平台能够高效支持动态语言。他还是多个重大 OpenJDK 项目的 Lead/Guide，包括 **Da Vinci Machine**、**Project Panama**、**Project Valhalla**、**Project Metropolis** 和 **Project Leyden**。

他的工作为 Lambda 表达式、Stream API、以及现代 JVM 上的动态语言（如 JRuby、Jython、Nashorn）奠定了技术基础。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | John Rose |
| **OpenJDK 用户名** | jrose |
| **当前组织** | [Oracle](../../contributors/orgs/oracle.md) (Java Platform Group) |
| **职位** | Senior Architect, Java Virtual Machine |
| **位置** | San Jose, California, USA |
| **工作时间** | 1995 - 至今 (30+ years) |
| **早期经历** | Thinking Machines Corporation (C* 并行语言, ~1987) |
| **专长领域** | JVM architecture, invokedynamic, method handles, bytecode, Vector API, AOT compilation |
| **邮件** | john.rose@oracle.com (前身为 sun.com) |
| **GitHub** | [rose00](https://github.com/rose00) (Oracle org member; valhalla, panama-foreign, panama-vector 等仓库) |
| **X (Twitter)** | [@JohnRose00](https://x.com/JohnRose00) |
| **Oracle Blog** | [blogs.oracle.com/jrose](https://blogs.oracle.com/jrose/) |

---

## 3. 主要 JEP 贡献

### JEP 160: Lambda-Form Representation for Method Handles (JDK 8)

| 属性 | 值 |
|------|-----|
| **角色** | Author |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 8 |
| **文档** | [JEP 160](/jeps/language/jep-160.md) |

**影响**: 创建了名为 "lambda form" 的新中间表示，用于 method handles：
- 可直接执行
- 可直接编译
- 可缓存和重用
- 用 JIT 技术替换汇编语言路径

### JEP 309: Dynamic Class-File Constants (JDK 11)

| 属性 | 值 |
|------|-----|
| **角色** | Author |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 11 |
| **文档** | [JEP 309](/jeps/language/jep-309.md) |

**影响**: 扩展类文件常量池，支持运行时解析，提高引导性能。

### JEP 514: AOT Command-Line Ergonomics (JDK 25)

| 属性 | 值 |
|------|-----|
| **角色** | Author |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 25 |
| **文档** | [JEP 514](/jeps/performance/jep-514.md) |

**影响**: 改进 AOT 编译的命令行体验，启动时间提升 30-40%。

### JEP 515: Ahead-of-Time Method Profiling (JDK 25)

| 属性 | 值 |
|------|-----|
| **角色** | Co-Author (与 Igor Veresov) |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 25 |
| **文档** | [JEP 515](https://openjdk.org/jeps/515) |

**影响**: 将方法执行配置文件从前一次运行保存到 AOT 缓存中，使 HotSpot JVM 启动时即可获取配置数据，显著改善应用热身时间。

### JSR 292: invokedynamic (JDK 7)

| 属性 | 值 |
|------|-----|
| **角色** | Lead Architect |
| **发布版本** | JDK 7 |
| **影响** | 引入 invokedynamic 字节码指令 |

**影响**: 引入了新的字节码指令 `invokedynamic`，为 JVM 上的动态语言提供支持。

---

## 4. 核心技术贡献

### 1. invokedynamic 字节码指令

设计了 invokedynamic 指令作为动态调用站点的通用原语：
- 作为字节码和中间语言之间的连接点
- 不依赖于任何特定编程语言的语义
- 使 JVM 能够高效支持动态语言（如 Ruby、Python、JavaScript）
- 为 Lambda 表达式提供底层支持

```java
// invokedynamic 使用示例
// Lambda 表达式编译为 invokedynamic 调用点
list.forEach(s -> System.out.println(s));

// 字节码：
// invokedynamic #1,  0, InvokeDynamic #0:accept:()Ljava/util/function/Consumer;
```

### 2. Method Handles

提供了直接、安全、高效的方法和构造函数引用机制：
- 与反射 API 相比性能更优
- 是 invokedynamic 实现的基础
- 支持 lambda 表达式的底层实现
- 支持方法组合和转换

```java
// MethodHandle 示例
MethodHandles.Lookup lookup = MethodHandles.lookup();
MethodHandle mh = lookup.findVirtual(String.class, "toUpperCase", 
                                      MethodType.methodType(String.class));
String result = (String) mh.invokeExact("hello");  // "HELLO"
```

### 3. Lambda-Form 中间表示

创建了 lambda form 作为 method handles 的中间表示：
- 比 JVM 字节码更抽象
- 比 Java 源代码更底层
- 支持 JIT 优化
- 支持缓存和重用

### 4. Project Panama 贡献

- **Token Codes**: 为 Project Panama 定义了 lambda bodies 的新表示
- 介于 JVM 字节码和 Java 源代码之间的复杂度
- 支持外部函数和内存 API

### 5. Vector API (与 Vladimir Kozlov 合作)

与 [Vladimir Kozlov](../../by-contributor/profiles/vladimir-kozlov.md) 合作开发 Vector API，为 Java 提供 SIMD 向量计算能力：
- JEP 338: Vector API (Incubator) - JDK 16
- JEP 414: Vector API (Second Incubator) - JDK 17
- JEP 417: Vector API (Third Incubator) - JDK 18
- JEP 426: Vector API (Fourth Incubator) - JDK 19
- JEP 438: Vector API (Fifth Incubator) - JDK 20
- JEP 448: Vector API (Sixth Incubator) - JDK 21

### 6. Value Types (Project Valhalla)

与 [Brian Goetz](../../by-contributor/profiles/brian-goetz.md)、Guy Steele 共同起草了 Java Value Types 的增强提案：
- 扁平化对象表示
- 消除对象头开销
- 支持泛型特化

### 7. AOT 编译与 Project Leyden (JDK 23-25)

- JEP 514: AOT Command-Line Ergonomics
- JEP 515: Ahead-of-Time Method Profiling (与 Igor Veresov 合作)
- 改进 AOT 编译体验
- 启动时间提升 30-40%
- 与 Mark Reinhold 在 JVMLS 2023 共同展示 Project Leyden 原型

### 8. 早期历史贡献

在 JVM/Java 架构之外，John Rose 还有大量早期贡献：
- **HotSpot 初始移植**: 完成 HotSpot VM 到 SPARC 架构的首次移植
- **sun.misc.Unsafe API**: 设计并实现了 Unsafe API，被大量高性能框架广泛使用
- **Java 内部类 (Inner Classes)**: 参与设计 Java 1.1 的内部类机制
- **Pack200 压缩算法**: 设计了 JAR 归档文件的高效压缩格式 (JSR 200)
- **Profile-driven JIT 优化**: 基于运行时配置的 JIT 编译优化
- **C* 并行语言**: 在 Thinking Machines Corporation 与 Guy Steele、Stephen Wolfram 共同发明 (1987)
- **动态语言实现**: Common Lisp、Scheme ("esh")、C++ 动态绑定

---

## 5. 协作网络

### 核心协作者

| 协作者 | 组织 | 合作领域 | 关系 |
|--------|------|----------|------|
| [Brian Goetz](../../by-contributor/profiles/brian-goetz.md) | Oracle | Lambda, Valhalla, Loom | 语言设计合作 |
| [Vladimir Kozlov](../../by-contributor/profiles/vladimir-kozlov.md) | Oracle | Vector API | 联合作者 |
| Guy Steele | Oracle | Valhalla, Value Types | 技术合作 |
| [Chen Liang](../../by-contributor/profiles/chen-liang.md) | Oracle | ClassFile API, Method Handles | 技术导师 |
| [Mark Reinhold](../../by-contributor/profiles/mark-reinhold.md) | Oracle | Project Leyden, JDK Architecture | 架构合作 |
| Igor Veresov | Oracle | AOT Method Profiling (JEP 515) | 联合作者 |

### OpenJDK 社区角色

| 项目/组 | 角色 |
|---------|------|
| **Da Vinci Machine Project** | Lead |
| **Project Panama** | Lead/Guide |
| **Project Valhalla** | Lead/Guide |
| **Project Metropolis** | Lead/Guide |
| **Compiler Group** | Member |
| **HotSpot Group** | Member |
| **Amber Project** | Reviewer |
| **Graal Project** | Committer |
| **Galahad Project** | Committer |

### 协作模式

```
John Rose (jrose)
    │
    ├─ Brian Goetz ───── Lambda, Valhalla, Loom
    │
    ├─ Vladimir Kozlov ─ Vector API
    │
    ├─ Guy Steele ────── Value Types, C*
    │
    ├─ Mark Reinhold ─── Project Leyden
    │
    ├─ Igor Veresov ──── AOT Method Profiling
    │
    └─ Chen Liang ────── ClassFile API
```

---

## 6. 学术贡献

### 发表论文

- **"Bytecodes meet Combinators: invokedynamic on the JVM"** (VMIL 2009)
  - 讨论了 invokedynamic 的设计和实现
  - 被多篇学术论文引用
  - [ACM Digital Library](https://dl.acm.org/doi/10.1145/1711506.1711508) (可能需要机构访问)

### 技术演讲

- **Inside.java Podcast Episode 42** (2025-12): "From Sumatra to Panama, from Babylon to Valhalla" — 讨论特性设计、技术债务、Rice 定理与静态/动态检查的关系
- **JVMLS 2023**: 与 Mark Reinhold 共同展示 Project Leyden 原型，Spring Boot 应用启动时间缩短 50-80%
- **Devoxx/Conference Talk**: "Your next JVM: Panama, Valhalla, Metropolis" — 阐述 JVM 未来架构方向
- **Jfokus 2011**: "Method Handles and invokedynamic"
- **JVMLS 2008**: JVM Language Summit 初始演讲，发表 Da Vinci Machine 愿景
- **JavaOne 多次演讲**: JVM 内部机制、动态语言支持

---

## 7. 开发风格

### 技术特点

1. **深度架构思维**: 从底层字节码到高层语言设计的全方位理解
2. **性能导向**: 所有设计都考虑性能和可维护性的平衡
3. **通用性原则**: invokedynamic 不绑定特定语言，提供通用原语
4. **渐进式演进**: 通过孵化器和预览机制收集反馈

### 设计理念

> "invokedynamic 不应该绑定任何特定语言的语义，它应该是一个通用的动态调用原语。"
> — John Rose

---

## 8. 技术影响力

### 受 John Rose 工作影响的关键特性

| 特性 | JDK 版本 | 关系 |
|------|----------|------|
| **Lambda 表达式** | JDK 8 | 底层使用 invokedynamic |
| **Stream API** | JDK 8 | 依赖 Lambda 和方法引用 |
| **动态语言支持** | JDK 7+ | JRuby, Jython, Nashorn |
| **Vector API** | JDK 16-21 | 与 Vladimir Kozlov 合作 |
| **AOT 编译 (Leyden)** | JDK 24-25 | JEP 514, JEP 515 |
| **Value Types** | 开发中 | Project Valhalla |
| **Foreign Function & Memory** | JDK 16-22 | Project Panama |

### 社区影响

- **JVM 动态语言生态**: JRuby、Jython、Nashorn 等项目的技术基础
- **函数式编程**: Lambda 表达式的底层实现
- **编译器开发**: GraalVM、Truffle 等项目的技术参考

---

## 9. 相关链接

### 官方资料
- [Inside.java Profile](https://inside.java/u/JohnRose/)
- [OpenJDK Census: jrose](https://openjdk.org/census#jrose)
- [GitHub: rose00](https://github.com/rose00)
- [Oracle Blog](https://blogs.oracle.com/jrose/)
- [X (Twitter): @JohnRose00](https://x.com/JohnRose00)

### JEP 文档
- [JEP 160: Lambda-Form Representation](/jeps/language/jep-160.md)
- [JEP 309: Dynamic Class-File Constants](/jeps/language/jep-309.md)
- [JEP 514: AOT Command-Line Ergonomics](/jeps/performance/jep-514.md)
- [JEP 515: Ahead-of-Time Method Profiling](https://openjdk.org/jeps/515)

### 技术文档
- [Method handles and invokedynamic - OpenJDK Wiki](https://wiki.openjdk.org/spaces/HotSpot/pages/11829269/Method+handles+and+invokedynamic)
- [Token Codes: IR for Liftable Lambdas](https://cr.openjdk.org/~jrose/panama/token-codes.html)
- [Value Types for Java](https://cr.openjdk.org/~jrose/values/values-0.html)
- [Project Metropolis Proposal](https://cr.openjdk.org/~jrose/metropolis/Metropolis-Proposal.html)

### 论文
- [Bytecodes meet Combinators: invokedynamic on the JVM (ACM)](https://dl.acm.org/doi/10.1145/1711506.1711508) (可能需要机构访问)

### 演讲录音/播客
- [Inside.java Podcast Ep. 42: From Sumatra to Panama, from Babylon to Valhalla](https://inside.java/2025/12/10/podcast-042/)

---

**Sources**:
- [Inside.java - JohnRose](https://inside.java/u/JohnRose/)
- [OpenJDK Census: jrose](https://openjdk.org/census#jrose)
- [GitHub: rose00](https://github.com/rose00)
- [Oracle Blog: jrose](https://blogs.oracle.com/jrose/)
- [JEP 160](/jeps/language/jep-160.md)
- [JEP 309](/jeps/language/jep-309.md)
- [JEP 514](/jeps/performance/jep-514.md)
- [JEP 515](https://openjdk.org/jeps/515)
- [ACM Paper - invokedynamic](https://dl.acm.org/doi/10.1145/1711506.1711508)
- [OpenJDK Wiki - Method handles and invokedynamic](https://wiki.openjdk.org/spaces/HotSpot/pages/11829269/Method+handles+and+invokedynamic)
- [Da Vinci Machine - Wikipedia](https://en.wikipedia.org/wiki/Da_Vinci_Machine)
- [Inside.java Podcast Ep. 42](https://inside.java/2025/12/10/podcast-042/)
