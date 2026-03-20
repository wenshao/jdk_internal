# John Rose

> **Inside.java**: [JohnRose](https://inside.java/u/JohnRose/)
> **Organization**: Oracle (Java Platform Group)
> **Role**: JVM Architect

---

## 概述

John Rose 是 Oracle 的 **JVM 架构师**，自 1995 年起开始从事 Java 技术工作。他是 JVM 动态语言支持的奠基人，主导了 **invokedynamic** 字节码指令和 **method handles** 的设计与实现，使 Java 平台能够高效支持动态语言。

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | John Rose |
| **当前组织** | Oracle (Java Platform Group) |
| **职位** | JVM Architect |
| **工作时间** | 1995 - 至今 |
| **专长** | JVM architecture, invokedynamic, method handles, bytecode |
| **邮件** | john.rose@oracle.com (前身为 sun.com) |

---

## 主要 JEP 贡献

### JEP 160: Lambda-Form Representation for Method Handles (JDK 8)

| 属性 | 值 |
|------|-----|
| **角色** | Author |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 8 |

**影响**: 创建了名为 "lambda form" 的新中间表示，用于 method handles：
- 可直接执行
- 可直接编译
- 可缓存和重用
- 用 JIT 技术替换汇编语言路径

### JSR 292: invokedynamic

- **角色**: Lead Architect
- **发布版本**: JDK 7
- **影响**: 引入了新的字节码指令 `invokedynamic`，为 JVM 上的动态语言提供支持

---

## 核心技术贡献

### 1. invokedynamic 字节码指令

设计了 invokedynamic 指令作为动态调用站点的通用原语：
- 作为字节码和中间语言之间的连接点
- 不依赖于任何特定编程语言的语义
- 使 JVM 能够高效支持动态语言（如 Ruby、Python、JavaScript）

### 2. Method Handles

提供了直接、安全、高效的方法和构造函数引用机制：
- 与反射 API 相比性能更优
- 是 invokedynamic 实现的基础
- 支持 lambda 表达式的底层实现

### 3. JVM 性能优化

对 JDK 栈的各个方面进行了性能优化：
- 低级字节码和指令集设计
- JVM 运行时优化
- 动态语言支持的性能提升

### 4. Project Panama 贡献

- **Token Codes**: 为 Project Panama 定义了 lambda bodies 的新表示
- 介于 JVM 字节码和 Java 源代码之间的复杂度

### 5. Value Types 草案

与 Brian Goetz、Guy Steele 共同起草了 Java Value Types 的增强提案。

---

## 学术贡献

### 发表论文

- **"Bytecodes meet Combinators: invokedynamic on the JVM"** (VMIL 2009)
  - 讨论了 invokedynamic 的设计和实现
  - 被多篇学术论文引用

### 技术博客

在 Oracle 技术博客发表多篇关于 JVM 内部机制的文章。

---

## 开发风格

### 技术特点

1. **深度架构思维**: 从底层字节码到高层语言设计的全方位理解
2. **性能导向**: 所有设计都考虑性能和可维护性的平衡
3. **通用性原则**: invokedynamic 不绑定特定语言，提供通用原语

### 影响力

John Rose 的工作为以下 Java 特性奠定了基础：
- Lambda 表达式 (JSR 335)
- Stream API
- 动态语言在 JVM 上的高效运行

---

## 相关链接

### 官方资料
- [Inside.java Profile](https://inside.java/u/JohnRose/)
- [JEP 160: Lambda-Form Representation](https://openjdk.org/jeps/160)

### 技术文档
- [Method handles and invokedynamic - OpenJDK Wiki](https://wiki.openjdk.org/spaces/HotSpot/pages/11829269/Method+handles+and+invokedynamic)
- [Token Codes: IR for Liftable Lambdas](https://cr.openjdk.org/~jrose/panama/token-codes.html)
- [Value Types for Java](https://cr.openjdk.org/~jrose/values/values-0.html)

### 论文
- [Bytecodes meet Combinators: invokedynamic on the JVM (ACM)](https://dl.acm.org/doi/10.1145/1711506.1711508)

---

**Sources**:
- [Inside.java - JohnRose](https://inside.java/u/JohnRose/)
- [OpenJDK JEP 160](https://openjdk.org/jeps/160)
- [ACM Paper - invokedynamic](https://dl.acm.org/doi/10.1145/1711506.1711508)
- [OpenJDK Wiki - Method handles and invokedynamic](https://wiki.openjdk.org/spaces/HotSpot/pages/11829269/Method+handles+and+invokedynamic)
