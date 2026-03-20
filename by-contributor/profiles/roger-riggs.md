# Roger Riggs

> **GitHub**: [@RogerRiggs](https://github.com/RogerRiggs)
> **OpenJDK**: [@rriggs](https://openjdk.org/census#rriggs)
> **Organization**: Oracle
> **Location**: Burlington, Massachusetts, United States

---

## 概述

Roger Riggs 是 Oracle 的资深 JDK 工程师，专注于核心库的健壮性和安全性改进。他对 JDK 的主要贡献包括 StringBuilder 健壮性增强和状态一致性检查。他领导 client-libs 组，在 Java 客户端技术方面工作多年，从 Sun Microsystems 时代到 Oracle。

> **数据来源**: [CFV Valhalla Committer](https://mail.openjdk.org/pipermail/valhalla-dev/2019-April/005567.html), [LinkedIn](https://www.linkedin.com/in/roger-riggs-1803061), [OpenJDK GB 2024](https://openjdk.org/poll/gb/2024/)

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Roger Riggs |
| **当前组织** | Oracle |
| **位置** | Burlington, Massachusetts, USA |
| **GitHub** | [@RogerRiggs](https://github.com/RogerRiggs) |
| **LinkedIn** | [roger-riggs-1803061](https://www.linkedin.com/in/roger-riggs-1803061) |
| **OpenJDK** | [@rriggs](https://openjdk.org/census#rriggs) |
| **角色** | Valhalla Committer (2019-04), client-libs Group Lead |
| **主要领域** | Core Libraries, StringBuilder, Client Libraries |
| **经验** | Sun Microsystems → Oracle (pre-dating OpenJDK) |

---

## 主要贡献

### JDK 26 (2025-2026)

| PR/Issue | 标题 | 角色 |
|----------|------|------|
| [JDK-8351443](/by-pr/8351/8351443.md) | 改进 StringBuilder 的健壮性 | Author |

### 核心优化领域

| 领域 | 说明 |
|------|------|
| **StringBuilder 健壮性** | 状态一致性检查、并发安全增强 |
| **核心库** | java.lang 包改进 |
| **错误检测** | 早期发现内部状态不一致 |

---

## 分析的 PR

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

**文档**: [详细分析](/by-pr/8351/8351443.md)

---

## 外部资源

### 链接

- **GitHub**: [https://github.com/RogerRiggs](https://github.com/RogerRiggs)
- **OpenJDK Census**: [rriggs](https://openjdk.org/census#rriggs)
- **JDK-8351443 Commit**: [Mail Archive](https://mail.openjdk.org/pipermail/jdk-changes/2025-May/032004.html)

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-20
> **创建原因**: JDK-8351443 PR 分析
