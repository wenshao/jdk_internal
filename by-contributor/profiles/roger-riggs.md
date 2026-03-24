# Roger Riggs

> **GitHub**: [@RogerRiggs](https://github.com/RogerRiggs)
> **OpenJDK**: [@rriggs](https://openjdk.org/census#rriggs)
> **OpenJDK Wiki**: [rriggs](https://wiki.openjdk.org/display/~rriggs)
> **Organization**: Oracle (Java Core Libraries Team, Java Products Group)
> **Location**: Burlington, Massachusetts, United States

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [主要贡献](#3-主要贡献)
4. [分析的 PR](#4-分析的-pr)
5. [外部资源](#5-外部资源)

---


## 1. 概述

Roger Riggs 是 Oracle Java Core Libraries Team 的资深 JDK 工程师，专注于核心库的健壮性和安全性改进。他的主要贡献包括 JEP 102 (Process API Updates)、JEP 290/415 (Serialization Filtering)、StringBuilder 健壮性增强、以及 JSR 310 (Date/Time API) 相关工作。他是 Valhalla Committer，从 Sun Microsystems 时代即参与 JDK 开发。

> **数据来源**: [CFV Valhalla Committer](https://mail.openjdk.org/pipermail/valhalla-dev/2019-April/005567.html), [LinkedIn](https://www.linkedin.com/in/roger-riggs-1803061), [OpenJDK GB 2024](https://openjdk.org/poll/gb/2024/)

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Roger Riggs |
| **当前组织** | Oracle |
| **位置** | Burlington, Massachusetts, USA |
| **GitHub** | [@RogerRiggs](https://github.com/RogerRiggs) |
| **LinkedIn** | [roger-riggs-1803061](https://www.linkedin.com/in/roger-riggs-1803061) |
| **OpenJDK** | [@rriggs](https://openjdk.org/census#rriggs) |
| **OpenJDK Wiki** | [rriggs](https://wiki.openjdk.org/display/~rriggs) |
| **角色** | Valhalla Committer (2019-04), Core Libraries Engineer |
| **主要领域** | Core Libraries, Serialization, Process API, Date/Time |
| **经验** | Sun Microsystems → Oracle (pre-dating OpenJDK) |

---

## 3. 主要贡献

### JDK 26 (2025-2026)

| PR/Issue | 标题 | 角色 |
|----------|------|------|
| [JDK-8351443](../../by-pr/8351/8351443.md) | 改进 StringBuilder 的健壮性 | Author |

### JEP 贡献

| JEP | 标题 | JDK 版本 |
|-----|------|----------|
| [JEP 102](https://openjdk.org/jeps/102) | Process API Updates | JDK 9 |
| [JEP 290](https://openjdk.org/jeps/290) | Filter Incoming Serialization Data | JDK 9 |
| [JEP 415](https://openjdk.org/jeps/415) | Context-Specific Deserialization Filters | JDK 17 |

### 核心优化领域

| 领域 | 说明 |
|------|------|
| **Serialization Filtering** | ObjectInputFilter API, 反序列化安全过滤 (JEP 290/415) |
| **Process API** | ProcessHandle, 进程管理改进 (JEP 102) |
| **StringBuilder 健壮性** | 状态一致性检查、并发安全增强 |
| **Date/Time** | JSR 310 (java.time) 相关贡献 |
| **Cleaners** | Replacing Finalizers with Cleaners |

---

## 4. 分析的 PR

### JDK-8351443: 改进 StringBuilder 的健壮性

增强了 StringBuilder 的内部状态一致性检查，提前发现状态不一致问题。

**关键改进**:
- 检查 `count ≤ capacity` 约束
- 检查 `count ≤ value.length` 约束
- 检查 `coder` 与实际内容一致
- 提供清晰的错误信息

**技术细节**:
- 在 `AbstractStringBuilder` 关键方法中添加状态检查
- 检测并发修改导致的状态不一致
- 抛出 `IllegalStateException` 而非静默错误

**文档**: [详细分析](../../by-pr/8351/8351443.md)

---

## 5. 外部资源

### 链接

- **GitHub**: [https://github.com/RogerRiggs](https://github.com/RogerRiggs)
- **OpenJDK Census**: [rriggs](https://openjdk.org/census#rriggs)
- **OpenJDK Wiki**: [rriggs](https://wiki.openjdk.org/display/~rriggs)
- **LinkedIn**: [roger-riggs-1803061](https://www.linkedin.com/in/roger-riggs-1803061)
- **JEP 102**: [Process API Updates](https://openjdk.org/jeps/102)
- **JEP 290**: [Filter Incoming Serialization Data](https://openjdk.org/jeps/290)
- **JEP 415**: [Context-Specific Deserialization Filters](https://openjdk.org/jeps/415)
- **JDK-8351443 Commit**: [Mail Archive](https://mail.openjdk.org/pipermail/jdk-changes/2025-May/032004.html)

---

> **文档版本**: 1.1
> **最后更新**: 2026-03-22
> **更新内容**:
> - 修正组织描述: "Java Core Libraries Team" (非 "client-libs Group Lead")
> - 添加 JEP 贡献: JEP 102 (Process API), JEP 290/415 (Serialization Filtering)
> - 添加 OpenJDK Wiki 链接
> - 扩展核心领域: Serialization Filtering, Process API, Date/Time, Cleaners
> - 修正概述以反映完整贡献范围


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 988 |
| **活跃仓库数** | 5 |
