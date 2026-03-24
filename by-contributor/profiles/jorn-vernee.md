# Jorn Vernee

> **GitHub**: [@JornVernee](https://github.com/JornVernee)
> **Inside.java**: [JornVernee](https://inside.java/u/JornVernee/)
> **Organization**: Oracle (Java Platform Group)
> **Role**: Project Panama 核心贡献者, Foreign Function & Memory API 实现者
> **Blog**: [jornvernee.github.io](https://jornvernee.github.io/)
> **Mastodon**: [@jornvernee@mastodon.social](https://mastodon.social/@jornvernee)

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [主要 JEP 贡献](#3-主要-jep-贡献)
4. [核心技术贡献](#4-核心技术贡献)
5. [职业经历](#5-职业经历)
6. [社区活动](#6-社区活动)
7. [技术专长](#7-技术专长)
8. [相关链接](#8-相关链接)

---


## 1. 概述

Jorn Vernee 是 Oracle Java Platform Group 的工程师，也是 **Project Panama** 的核心贡献者和 **Foreign Function & Memory (FFM) API** 的主要实现者之一。他与 Maurizio Cimadamore 紧密合作，共同推动 FFM API 从孵化阶段到 JDK 22 正式发布。他同时是 **jextract** 工具的贡献者，该工具可以从本地库头文件自动生成 Java 绑定代码。他的技术兴趣集中在 Java 与本地代码互操作、JVM 和虚拟机技术方面。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Jorn Vernee |
| **当前组织** | Oracle (Java Platform Group) |
| **GitHub** | [@JornVernee](https://github.com/JornVernee) (49 followers, 26 repos) |
| **OpenJDK** | [@jvernee](https://openjdk.org/census#jvernee) |
| **Inside.java** | [JornVernee](https://inside.java/u/JornVernee/) |
| **Blog** | [jornvernee.github.io](https://jornvernee.github.io/) |
| **Mastodon** | [@jornvernee](https://mastodon.social/@jornvernee) |
| **专长** | Foreign Function & Memory API, Project Panama, jextract, MethodHandle, Downcall/Upcall, JVM Internals |

> **数据来源**: [GitHub](https://github.com/JornVernee), [Inside.java](https://inside.java/u/JornVernee/), [OpenJDK Wiki](https://wiki.openjdk.org/display/~jvernee)

---

## 3. 主要 JEP 贡献

### JEP 454: Foreign Function & Memory API (Final) - JDK 22

| 属性 | 值 |
|------|-----|
| **角色** | Reviewer / 核心实现者 |
| **Owner** | Maurizio Cimadamore |
| **状态** | Final |
| **发布版本** | JDK 22 |

**影响**: FFM API 正式发布，为 Java 提供高效、安全的本地代码互操作能力，替代传统 JNI。Jorn Vernee 作为核心实现者和 Reviewer 参与了整个开发周期。

### JEP 442: Foreign Function & Memory API (Third Preview) - JDK 21

| 属性 | 值 |
|------|-----|
| **角色** | 核心实现者 |
| **状态** | Preview |

### JEP 434: Foreign Function & Memory API (Second Preview) - JDK 20

| 属性 | 值 |
|------|-----|
| **角色** | Co-author (实现) |
| **状态** | Preview |

### JEP 424: Foreign Function & Memory API (Preview) - JDK 19

| 属性 | 值 |
|------|-----|
| **角色** | 核心实现者 |
| **状态** | Preview |

### JEP 389: Foreign Linker API (Incubator) - JDK 16

| 属性 | 值 |
|------|-----|
| **角色** | Reviewer |
| **Owner** | Maurizio Cimadamore |
| **状态** | Delivered |
| **发布版本** | JDK 16 |

**影响**: Foreign Linker API 首次以孵化模块形式发布，为后续 FFM API 和 jextract 工具奠定基础。

---

## 4. 核心技术贡献

### 1. Foreign Function & Memory API 实现

Jorn Vernee 是 FFM API 的核心实现者，与 Maurizio Cimadamore 协作：
- **Downcall Method Handles**: 从 Java 代码调用本地函数的方法句柄实现
- **Upcall Stubs**: 从本地代码回调 Java 的函数指针机制
- **Memory Segments**: 安全访问 JVM 管理外内存的 API
- **Arena API**: 内存生命周期管理
- **性能基准测试**: 添加 upcall 基准测试，对比 JNI 与 Panama 调用开销

```java
// FFM API Downcall 示例
Linker linker = Linker.nativeLinker();
SymbolLookup stdlib = linker.defaultLookup();

MethodHandle strlen = linker.downcallHandle(
    stdlib.find("strlen").get(),
    FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
);

try (Arena arena = Arena.ofConfined()) {
    MemorySegment cString = arena.allocateFrom("Hello Panama");
    long len = (long) strlen.invoke(cString);
}
```

### 2. jextract 工具

jextract 是 Project Panama 的配套工具：
- **功能**: 从本地库的 C 头文件自动生成 Java 绑定代码
- **技术**: 利用 clang C API 解析头文件，生成基于 FFM API 的 downcall method handles
- **目标**: 让开发者无需手写 JNI 代码即可与本地库互操作

### 3. MethodHandle 与 JVM 内部机制

Jorn Vernee 对 JVM 内部机制有深入理解：
- **MethodHandle 优化**: FFM downcall handles 是可优化的 MethodHandle
- **HotSpot C2 编译器**: JIT 编译器可以内联和优化 downcall 路径
- **技术博客**: 发表了关于 MethodHandle 入门和 HotSpot JIT 编译调试的文章

### 4. Rust-Panama 互操作

- 在个人博客中演示了如何通过 Panama FFI 调用 Rust 库
- 展示了 FFM API 不仅限于 C 库，可与任何遵循 C ABI 的语言互操作

---

## 5. 职业经历

### Oracle (当前)

Jorn Vernee 在 Oracle Java Platform Group 工作：
- **Project Panama 核心团队**: 与 Maurizio Cimadamore 合作开发 FFM API
- **JDK Committer**: openjdk/jdk 和 openjdk/panama-foreign 项目的活跃贡献者
- **jextract 维护者**: 参与 jextract 工具开发

---

## 6. 社区活动

### Inside Java Podcast

- **Episode 9** (2020-12-11): "Project Panama - The Foreign Memory Access API" — 与 Maurizio Cimadamore 一起讨论 FFM API 的设计和迭代
- **Episode 10** (2020-12-21): "Project Panama - The Foreign Linker API" — 与 Maurizio Cimadamore 深入讨论 Foreign Linker API
- **Episode 32** (2024-01-08): "The Panama Effect" — 独立嘉宾，讨论 FFM API 在生态系统中的采用和性能提升

### 技术博客

在个人博客 [jornvernee.github.io](https://jornvernee.github.io/) 发表技术文章：
- MethodHandle 入门指南
- HotSpot JIT 编译调试笔记
- 通过 Panama FFI 调用 Rust 库教程

### 邮件列表

- **panama-dev**: Project Panama 开发讨论
- **core-libs-dev**: 核心库开发

---

## 7. 技术专长

### 本地互操作

- **FFM API**: Foreign Function & Memory API 设计和实现
- **Downcall/Upcall**: Java ↔ Native 调用机制
- **jextract**: 自动生成本地库 Java 绑定
- **JNI 替代**: 新一代本地互操作方案

### JVM 内部

- **MethodHandle**: 方法句柄优化
- **HotSpot C2**: JIT 编译器向量化和优化
- **内存管理**: MemorySegment 和 Arena 生命周期

---

## 8. 相关链接

### 官方资料
- [Inside.java - JornVernee](https://inside.java/u/JornVernee/)
- [GitHub - JornVernee](https://github.com/JornVernee)
- [OpenJDK Wiki - jvernee](https://wiki.openjdk.org/display/~jvernee)
- [Personal Blog](https://jornvernee.github.io/)
- [Mastodon](https://mastodon.social/@jornvernee)

### JEP 文档
- [JEP 454: Foreign Function & Memory API](https://openjdk.org/jeps/454)
- [JEP 442: FFM API (Third Preview)](https://openjdk.org/jeps/442)
- [JEP 434: FFM API (Second Preview)](https://openjdk.org/jeps/434)
- [JEP 424: FFM API (Preview)](https://openjdk.org/jeps/424)
- [JEP 389: Foreign Linker API (Incubator)](https://openjdk.org/jeps/389)

### Podcast
- [Inside Java Podcast Episode 9: Foreign Memory Access API](https://inside.java/2020/12/11/podcast-009/)
- [Inside Java Podcast Episode 10: Foreign Linker API](https://inside.java/2020/12/21/podcast-010/)
- [Inside Java Podcast Episode 32: The Panama Effect](https://inside.java/2024/01/08/podcast-032/)

### 项目
- [openjdk/panama-foreign](https://github.com/openjdk/panama-foreign)
- [openjdk/jextract](https://github.com/openjdk/jextract)

---

**Sources**:
- [GitHub - JornVernee](https://github.com/JornVernee)
- [Inside.java - JornVernee](https://inside.java/u/JornVernee/)
- [JEP 454: Foreign Function & Memory API](https://openjdk.org/jeps/454)
- [JEP 389: Foreign Linker API](https://openjdk.org/jeps/389)
- [Inside Java Podcast Episode 9](https://inside.java/2020/12/11/podcast-009/)
- [Inside Java Podcast Episode 10](https://inside.java/2020/12/21/podcast-010/)
- [Inside Java Podcast Episode 32](https://inside.java/2024/01/08/podcast-032/)
- [OpenJDK Wiki - jvernee](https://wiki.openjdk.org/display/~jvernee)
- [Jorn Vernee Blog](https://jornvernee.github.io/)
- [Calling Rust from Panama](https://jornvernee.github.io/java/panama/rust/panama-ffi/2021/09/03/rust-panama-helloworld.html)

## 角色晋升 (CFV)

| 日期 | 角色 | 提名者 | 投票数 | 链接 |
|------|------|--------|--------|------|
| 2020-06-04 | Committer | Claes Redestad | 36 | [CFV](https://mail.openjdk.org/pipermail/jdk-dev/2020-June/004351.html) |
| 2021-04-19 | Reviewer | Claes Redestad | 26 | [CFV](https://mail.openjdk.org/pipermail/jdk-dev/2021-April/005313.html) |


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 593 |
| **活跃仓库数** | 2 |
