# Per Minborg (Per-Åke Minborg)

> Java 核心库开发者，JEP 526 主导者，Speedment 创始人

---
## 目录

1. [基本信息](#1-基本信息)
2. [职业里程碑](#2-职业里程碑)
3. [贡献概述](#3-贡献概述)
4. [主要项目](#4-主要项目)
5. [关键贡献](#5-关键贡献)
6. [演讲和会议](#6-演讲和会议)
7. [开发风格](#7-开发风格)
8. [外部资源](#8-外部资源)
9. [相关链接](#9-相关链接)

---


## 1. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Per-Åke Minborg |
| **当前组织** | Oracle (Consulting Member of Technical Staff) |
| **位置** | Palo Alto, California, 美国 |
| **GitHub** | [@pminborg](https://github.com/pminborg) |
| **GitHub (个人)** | [@minborg](https://github.com/minborg) |
| **Email** | per.minborg@oracle.com |
| **OpenJDK** | [@pminborg](https://openjdk.org/census#pminborg) |
| **角色** | JDK Committer (2022-12), JDK Reviewer |
| **主要领域** | Core Libraries, Project Panama, Project Amber |
| **活跃时间** | 2016+ |

### 经验背景

| 属性 | 值 |
|------|-----|
| **Java 开发经验** | 20+ 年 (从 Java 1.0 开始) |
| **首次计算机** | 14 岁时 (1980 年代初) |
| **Oracle 经验** | Sun Microsystems 时代延续至今 |
| **会议演讲** | JavaOne Alumni, Jfokus, Devoxx Belgium |

> **数据来源**: [Inside.java](https://inside.java/u/Per-AkeMinborg/), [CFV: New JDK Committer](https://mail.openjdk.org/pipermail/jdk-dev/2022-December/007268.html), [CFV: New JDK Reviewer](https://mail.openjdk.org/pipermail/jdk-dev/2023/msg/4ZNHONUC7PGMZP4NRZKCRLTLBEOG5RE4/), [Foojay](https://foojay.io/today/author/per-minborg/)

---

## 2. 职业里程碑

| 日期 | 事件 | 详情 |
|------|------|------|
| **1980s** | 首次接触计算机 | 14 岁时组装第一台计算机 |
| **1990s** | 开始 Java 开发 | 从 Java 1.0 开始 |
| **Sun 时代** | 加入 Sun Microsystems | Java 客户端技术工作 |
| **Oracle 时代** | 并入 Oracle | 继续核心库开发 |
| **2016+** | OpenJDK 贡献 | 核心库、Project Panama |
| **2022-12** | 被提名为 JDK Committer | 由 Alan Bateman 提名，Andrew Dinn 发起 CFV |
| **2023** | 被提名为 JDK Reviewer | 58+ commits 提交后 |
| **2025** | JavaOne 演讲者 | Project Panama 主题 |

---

## 3. 贡献概述

### JDK 贡献统计

| 指标 | 数值 |
|------|------|
| **Commits** | 58+ (jdk 仓库) |
| **主要变更** | 14+ 直接贡献 + 3 个合作主要变更 |
| **核心库** | java.base 改进 |
| **FFM API** | Foreign Function & Memory API |

### 重要 Bug/Enhancement 修复

| Issue | 标题 | 日期 |
|-------|------|------|
| [JDK-8324383](https://bugs.openjdk.org/browse/JDK-8324383) | SegmentAllocator:allocateFrom(ValueLayout...) | 2024-01-12 |
| [JDK-8323552](https://bugs.openjdk.org/browse/JDK-8323552) | AbstractMemorySegmentImpl#mismatch | 2024-03-25 |
| [JDK-8339531](https://bugs.openjdk.org/browse/JDK-8339531) | Improve MemorySegment::mismatch performance | 2024 |

### 技术文章

| 主题 | 链接 |
|------|------|
| Java 22: Panama FFM 性能基准测试 | [博客](http://minborgsjavapot.blogspot.com/2023/08/java-22-panama-ffm-provides-massive.html) |
| Java 22 FFM API 视频演讲 | [YouTube](https://www.youtube.com/watch?v=xlrRwaq1n2s) |
| FFM API 预览特性 (Java 20) | [YouTube](https://www.youtube.com/watch?v=8sFt1_7RxGk) |

### JEP 贡献

| JEP | 标题 | 角色 | 状态 |
|-----|------|------|------|
| [JEP 526](https://openjdk.org/jeps/526) | Lazy Constants | Lead | JDK 26 |
| JEP Draft 8312611 | Computed Constants | Co-author | Draft |

### 技术领域

- **Core Libraries**: java.base 改进
- **Project Panama**: Foreign Function & Memory API
- **Project Amber**: 语言特性增强
- **Project Leyden**: 启动时间和性能改进
- **Records**: Java records 实现
- **Pattern Matching**: 模式匹配特性

---

## 4. 主要项目

### Speedment

**类型**: 开源创业项目

Java Stream ORM 工具包和运行时，可以直接从数据库模式生成代码。

- **GitHub**: [speedment/speedment](https://github.com/speedment/speedment)
- **官网**: [speedment.com](https://speedment.com)
- **功能**:
  - 将 Hibernate/JPA 查询表示为 Java Streams
  - 内存加速技术 (最高 1000x 加速)
  - 超低延迟 (200 纳秒内流处理)

### JPAStreamer

**类型**: 开源库

扩展 Hibernate/JPA 以支持 Java Stream API 的轻量级开源扩展。

- **功能**: 使用标准 Java Stream API 表达数据库查询
- **类型安全**: 提供类型安全的查询构造
- **集成**: Quarkus 扩展 (`quarkus-jpastreamer`)
- **版本**: 3.0.0+ 支持 Hibernate 6 和 Spring Boot 3
- **价值**: 保持使用 Hibernate/JPA，同时用 Java Stream API 编写查询

### Minborg's Java Pot

**类型**: 个人技术博客

面向中高级 Java 开发者的技术和技巧博客。

- **博客**: [minborgsjavapot.blogspot.com](http://minborgsjavapot.blogspot.com/)
- **描述**: "This is my Java blog with various tips and tricks that are targeted for medium and advanced Java users"

### GitHub 文章仓库

- **仓库**: [minborg/articles](https://github.com/minborg/articles)
- **描述**: 关于 Java 内部工作的文章集合

---

## 5. 关键贡献

### JEP 526: Lazy Constants

主导 JDK 26 中的惰性常量实现：

- **启动性能**: 改善启动时间
- **内存占用**: 减少内存占用
- **延迟初始化**: 推迟初始化优化

### Project Panama: Foreign Function & Memory API

参与 Project Panama 的 FFM API 开发：

- **JEP 454**: Foreign Function & Memory API (JDK 22)
- **性能提升**: FFM: 43 ns/op vs JNI: 144 ns/op
- **无需 C 包装**: 不需要编写 C 包装代码

### Project Leyden

参与 Project Leyden，专注于改善 Java 启动时间和性能。

---

## 6. 演讲和会议

Per Minborg 经常在各大 Java 会议发表演讲：

| 会议 | 主题 |
|------|------|
| **JavaOne 2025** | Function and Memory Access in Pure Java |
| **JavaOne 2026** | (计划中) |
| **Devoxx Belgium** | Java 性能优化 |
| **Jfokus** (瑞典) | Java 技术演讲 |
| **IMCSNA18** | 超低延迟 Java 11 |

---

## 7. 开发风格

- **语言人机工程**: 关注语言易用性
- **性能意识 API 设计**: 性能导向的 API 设计
- **开发者体验**: 改善开发者体验
- **基准测试驱动**: 使用基准测试验证性能改进

---

## 8. 外部资源

| 类型 | 链接 |
|------|------|
| **OpenJDK Profile** | [pminborg](https://openjdk.org/census#pminborg) |
| **GitHub (Oracle)** | [@pminborg](https://github.com/pminborg) |
| **GitHub (个人)** | [@minborg](https://github.com/minborg) |
| **个人博客** | [Minborg's Java Pot](http://minborgsjavapot.blogspot.com/) |
| **文章仓库** | [minborg/articles](https://github.com/minborg/articles) |
| **Speedment** | [speedment.com](https://speedment.com) |
| **Inside.java** | [Per-Åke Minborg](https://inside.java/u/Per-AkeMinborg/) |
| **Foojay 作者页** | [foojay.io](https://foojay.io/today/author/per-minborg/) |

---

## 9. 相关链接

- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=pminborg)
- [JDK Commits (2022)](https://mail.openjdk.org/pipermail/jdk-dev/2022-December/007268.html)
- [JDK Reviewer CFV](https://mail.openjdk.org/pipermail/jdk-dev/2023/msg/4ZNHONUC7PGMZP4NRZKCRLTLBEOG5RE4/)
- [JEP 526: Lazy Constants](https://openjdk.org/jeps/526)

---

> **文档版本**: 2.0
> **最后更新**: 2026-03-20
> **更新内容**:
> - 添加全名 Per-Åke Minborg
> - 添加 Oracle 职位详情 (Consulting MTS)
> - 添加 20+ 年 Java 开发经验
> - 添加 JDK Committer/Reviewer 提名信息
> - 添加 Speedment 项目详情
> - 添加 Minborg's Java Pot 博客
> - 添加 GitHub 文章仓库
> - 添加会议演讲列表
> - 添加 FFM API 性能对比数据
> - 添加 Inside.java 和 Foojay 链接
