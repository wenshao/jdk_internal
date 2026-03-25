# Johannes Bechberger

> **Organization**: SAP (SapMachine Team)
> **Role**: Java Runtime Engineer, JFR Developer
> **Mastodon**: [@parttimenerd](https://mastodon.social/@parttimenerd)
> **Blog**: [mostlynerdless.de](https://mostlynerdless.de/)

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [主要 JEP 贡献](#3-主要-jep-贡献)
4. [核心技术贡献](#4-核心技术贡献)
5. [技术专长](#5-技术专长)
6. [博客和技术分享](#6-博客和技术分享)
7. [相关链接](#7-相关链接)

---


## 1. 概述

Johannes Bechberger 是 SAP **SapMachine 团队** 的 Java 运行时工程师，专注于 **Java Flight Recorder (JFR)** 和性能分析工具。他是 **JEP 509 (JFR CPU-Time Profiling)** 的作者，对 JDK 的可观测性做出了重要贡献。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Johannes Bechberger |
| **当前组织** | SAP (SapMachine Team) |
| **职位** | Java Runtime Engineer |
| **专长** | JFR, Performance Analysis, Tooling |
| **Mastodon** | [@parttimenerd](https://mastodon.social/@parttimenerd) |
| **博客** | [mostlynerdless.de](https://mostlynerdless.de/) |
| **GitHub** | [parttimenerd](https://github.com/parttimenerd) |
| **JDK 26 贡献** | 21 commits (JFR) |

---

## 3. 主要 JEP 贡献

### JEP 509: JFR CPU-Time Profiling

| 属性 | 值 |
|------|-----|
| **角色** | Author |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 26 |

**影响**: 为 JFR 添加 CPU 时间分析能力：
- 支持线程 CPU 时间记录
- 改进性能分析精度
- 与现有 JFR 事件集成

---

## 4. 核心技术贡献

### 1. Java Flight Recorder (JFR)

Johannes Bechberger 是 JFR 的活跃贡献者：
- **CPU Profiling**: CPU 时间分析
- **事件扩展**: 新增 JFR 事件类型
- **工具集成**: JFR 与性能工具集成

```java
// JFR CPU Profiling 示例
// 记录启用后，JFR 会收集线程 CPU 时间信息
// jfr record --name=profiling --cpusamples=true
```

### 2. 性能分析工具

- **JMC Integration**: Java Mission Control 集成
- **Profiling**: 性能采样和分析
- **诊断工具**: 故障排查工具

### 3. SapMachine 贡献

作为 SAP SapMachine 团队成员：
- **维护**: SAP JDK 分支维护
- **移植**: 向后移植重要修复
- **测试**: 质量保证和测试

---

## 5. 技术专长

### JFR (Java Flight Recorder)

- **事件系统**: JFR 事件框架
- **记录**: 低开销性能记录
- **分析**: 性能数据分析

### 性能分析

- **CPU Profiling**: CPU 使用分析
- **内存分析**: Memory profiling
- **线程分析**: Thread profiling

---

## 6. 博客和技术分享

### 技术文章

Johannes Bechberger 在其博客上分享关于：
- JFR 使用技巧
- Java 性能分析
- SapMachine 更新

### 会议演讲

- **Java 技术会议**: JFR 相关主题
- **性能分析**: Profiling 最佳实践

---

## 7. 相关链接

### JEP 文档
- [JEP 509: JFR CPU-Time Profiling](https://openjdk.org/jeps/509)

### 社交媒体
- [Mastodon: @parttimenerd](https://mastodon.social/@parttimenerd)
- [GitHub: parttimenerd](https://github.com/parttimenerd)
- [Blog: mostlynerdless.de](https://johannesg1.github.io/)

### SAP SapMachine
- [SapMachine GitHub](https://github.com/SAP/SapMachine)
- [SapMachine Blog](https://sapmachine.io/)

---

**Sources**:
- [JEP 509: JFR CPU-Time Profiling](https://openjdk.org/jeps/509)
- [Mastodon: @parttimenerd](https://mastodon.social/@parttimenerd)
- [GitHub: parttimenerd](https://github.com/parttimenerd)
- [SapMachine](https://sapmachine.io/)
- [JDK 26 Top Contributors](./jdk26-top-contributors.md)

## 角色晋升 (CFV)

| 日期 | 角色 | 提名者 | 投票数 | 链接 |
|------|------|--------|--------|------|
| 2023-05-15 | Committer | Langer, Christoph | 13 | [CFV](https://mail.openjdk.org/pipermail/jdk-dev/2023-May/007780.html) |

**提名时统计**: 11 changes
**贡献领域**: JVM profiling; JEP 435
