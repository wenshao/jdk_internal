# Jaroslav Bachorik

> **JFR/JMX 专家** | **BTrace 联合创始人** | **Datadog** (前 Oracle)

---

## 个人简介

**Jaroslav Bachorik** 是 Java 性能分析和追踪领域的知名专家，目前任职于 **Datadog** (Staff Software Engineer)。此前他曾在 **Oracle** 的 Java Serviceability 团队工作，担任 **JMX 技术负责人**。他是 **BTrace** 项目的联合创始人和维护者，也是 OpenJDK JFR（Java Flight Recorder）和 JMX 的重要贡献者。他在 2014 年被提名为 jdk9 Reviewer，在此之前已向 jdk 仓库贡献了 81 个 changeset。

| 项目 | 信息 |
|------|------|
| **GitHub** | [@jbachorik](https://github.com/jbachorik) (34 repositories) |
| **Twitter** | [@BachorikJ](https://twitter.com/BachorikJ) |
| **所在地** | 捷克，布拉格 |
| **当前组织** | Datadog |
| **前组织** | Oracle (Java Serviceability Team) |
| **OpenJDK 角色** | jdk9 Reviewer, jdk7u/jdk8/jdk8u/jdk9 Committer |
| **主要贡献** | JFR、JMX (Technical Lead)、BTrace、JVM 诊断工具、JPDA |

---

## 关键指标

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 6 |
| **OpenJDK Changesets** | 81+ (jdk repo, pre-GitHub era) |
| **主要领域** | JFR、JMX (Tech Lead)、JVM 诊断、JPDA、性能分析 |
| **代表作品** | BTrace (6k+ stars) |
| **职位** | Staff Software Engineer @ Datadog |

> **统计来源**: [GitHub Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Ajbachorik+label%3Aintegrated+is%3Aclosed)

---

## Integrated PRs 统计

### 按组件分布

| 组件 | PR 数量 | 说明 |
|------|--------|------|
| **JFR** | 4+ | Java Flight Recorder 核心功能 |
| **JVM 诊断** | 2+ | AsyncGetCallTrace、方法迭代器 |

### 代表性 PRs

| Issue | 标题 | 影响 |
|-------|------|------|
| [JDK-8329995](https://github.com/openjdk/jdk/pull/18775) | Restricted access to `/proc` can cause JFR initialization to crash | 🔒 容器环境 JFR 稳定性 |
| [JDK-8313816](https://github.com/openjdk/jdk/pull/16662) | Accessing jmethodID might lead to spurious crashes | 🔒 JVM 崩溃修复 |
| [JDK-8283849](https://github.com/openjdk/jdk/pull/8549) | AsyncGetCallTrace may crash JVM on guarantee | 🔒 性能分析工具稳定性 |
| [JDK-8261354](https://github.com/openjdk/jdk/pull/4143) | SIGSEGV at MethodIteratorHost | 🔒 JVM 崩溃修复 |
| [JDK-8203359](https://github.com/openjdk/jdk/pull/3126) | Container level resources events | 📦 容器支持 |
| [JDK-8258396](https://github.com/openjdk/jdk/pull/1823) | SIGILL in jdk.jfr.internal.PlatformRecorder.rotateDisk() | 🔒 JFR 崩溃修复 |

---

## 主要贡献领域

### 1. JFR（Java Flight Recorder）

Jaroslav 是 JFR 核心贡献者之一，专注于：

- **JFR 稳定性改进**：修复多个 JFR 相关的 JVM 崩溃问题
- **容器支持**：为 JFR 添加容器级别资源事件支持
- **磁盘轮转**：改进 JFR 磁盘录制轮转机制

### 2. JVM 诊断工具

- **AsyncGetCallTrace 修复**：修复了性能分析工具使用的关键 API 的崩溃问题
- **MethodIteratorHost**：修复了方法迭代器的 SIGSEGV 问题
- **jmethodID 访问**：修复了可能导致随机崩溃的 jmethodID 访问问题

### 3. BTrace 项目

**BTrace** 是 Jaroslav 创建的开源项目，是一个安全的 Java 动态追踪工具：

- **GitHub Stars**: 6,000+
- **Forks**: 960+
- **定位**: 类似于 DTrace，但专为 Java 平台设计
- **特点**: 安全、动态、无需重启 JVM

→ [BTrace GitHub](https://github.com/btraceio/btrace)

---

## 技术专长

| 领域 | 技能 |
|------|------|
| **JVM 内部** | JFR 架构、AsyncGetCallTrace、方法迭代器 |
| **性能分析** | 低开销采样、容器环境诊断 |
| **诊断工具** | BTrace、JFR 事件系统、动态追踪 |
| **编程语言** | Java、C++、JavaScript |

---

## 职业背景

### 当前职位

**Datadog** - Staff Software Engineer，性能监控和可观测性平台

- 专注于 JVM 性能分析和诊断 (dd-trace-java)
- 将 JFR 和 BTrace 的专业知识应用于产品
- 在 jFokus 2024 和 JavaOne 2025 等会议上发表关于 JVM 分析的演讲

### 前职位

**Oracle** - Java Serviceability Team

- JMX 技术负责人 (Technical Lead)
- 贡献于 JMX、JPDA (Java Platform Debugger Architecture)
- 实现和清理大量测试用例
- 2014 年被提名为 jdk9 Reviewer

### 开源贡献

| 项目 | 角色 | 说明 |
|------|------|------|
| **BTrace** | 联合创始人/维护者 | Java 动态追踪工具 |
| **OpenJDK** | Reviewer / Committer | JFR、JMX 和 JVM 诊断 |
| **jvmasm** | 作者 | JVM 符号汇编 DSL |
| **btracel** | 作者 | BTrace 单行工具 |

---

## 外部链接

- **GitHub**: https://github.com/jbachorik
- **BTrace**: https://github.com/btraceio/btrace
- **Twitter**: https://twitter.com/BachorikJ
- **LinkedIn**: https://www.linkedin.com/in/jbachorik/
- **Foojay**: https://foojay.io/today/author/jaroslav-bachorik/
- **CFV: jdk9 Reviewer**: http://mail.openjdk.java.net/pipermail/jdk9-dev/2014-July/000924.html
- **Datadog Open Source**: https://opensource.datadoghq.com/projects/openjdk/
- **JavaOne 2025**: https://speakerdeck.com/jbachorik/javaone-2025-advancing-java-profiling
- **OpenJDK PRs**: https://github.com/openjdk/jdk/pulls?q=author%3Ajbachorik

---

## 相关文档

- [Erik Gahlin](erik-gahlin.md) - JFR 架构师 (Oracle)
- [Markus Grönlund](markus-gronlund.md) - JFR 事件系统 (Oracle)
- [性能优化](/by-topic/core/performance/) - JFR 性能分析

---

**最后更新**: 2026-03-21


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 41 |
| **活跃仓库数** | 5 |
