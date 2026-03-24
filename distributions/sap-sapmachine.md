# SAPMachine

> SAP 提供的 OpenJDK 发行版

[← 返回发行版](../distributions/)

---
## 目录

1. [概述](#1-概述)
2. [特点](#2-特点)
3. [版本支持](#3-版本支持)
4. [安装](#4-安装)
5. [适用场景](#5-适用场景)
6. [相关链接](#6-相关链接)

---


## 1. 概述

SAPMachine 是 SAP 提供的 OpenJDK 发行版，针对 SAP 应用和 SAP 环境优化。

| 属性 | 值 |
|------|-----|
| **组织** | SAP |
| **官网** | https://sap.github.io/SapMachine/ |
| **下载** | https://github.com/SAP/SapMachine/releases |
| **许可证** | GPLv2 + CPEx |
| **商业支持** | ✅ (SAP 支持) |

---

## 2. 特点

- ✅ **SAP 优化**: 针对 SAP 应用优化
- ✅ **长期支持**: 与 SAP 产品版本同步
- ✅ **SAP 集成**: 与 SAP 技术栈深度集成

---

## 3. 版本支持

| 版本 | 支持截止 |
|------|----------|
| SAPMachine 8 | 2030-12 |
| SAPMachine 11 | 2027-10 |
| SAPMachine 17 | 2029-10 |
| SAPMachine 21 | 2031-10 |

---

## 4. 安装

```bash
# SDKMAN
sdk install java 21-sap

# Docker
docker pull ghcr.io/sapmachine/sapmachine:21
```

---

## 5. 适用场景

| 场景 | 理由 |
|------|------|
| SAP 应用 | SAP 优化 |
| SAP 环境 | 深度集成 |

---

## 6. 上游维护团队

SAP 是 **OpenJDK LTS 维护分支最大的贡献组织**，在 jdk17u/21u/11u/25u 四个维护分支合计贡献 **5,187 个 Integrated PRs**。

### 维护分支贡献统计

| 贡献者 | 角色 | jdk17u | jdk21u | jdk11u | jdk25u | 总计 |
|--------|------|--------|--------|--------|--------|------|
| [GoeLin](../by-contributor/profiles/goetz-lindenmaier.md) | Lead Maintainer | 1,951 | 1,114 | 785 | 65 | **3,915** |
| [MBaesken](../by-contributor/profiles/matthias-baesken.md) | Reviewer | 212 | 165 | 95 | 27 | **499** |
| [TheRealMDoerr](../by-contributor/profiles/martin-doerr.md) | Committer | 187 | 89 | 149 | 4 | **429** |
| [RealCLanger](../by-contributor/profiles/christoph-langer.md) | SapMachine Lead | 65 | 21 | 190 | 1 | **277** |
| 其他 SAP | — | 31 | 17 | 11 | 8 | 67 |
| **合计** | | **2,446** | **1,406** | **1,230** | **105** | **5,187** |

> [GoeLin](../by-contributor/profiles/goetz-lindenmaier.md) (Götz Lindenmaier) 是 OpenJDK 历史上最大的 LTS 维护贡献者，一人贡献了 3,915 个 backport PR。

### 主线上游贡献

SAP 在 openjdk/jdk 主线也有 **999+ PRs**，主要领域: PPC 移植, AIX, 构建系统, HotSpot Runtime。

SAP 在 JDK Mission Control (JMC) 项目中也有贡献 (RealCLanger 31 PRs)，但 JMC 主要由 Datadog 主导。

> 详情: [SAP 组织页面](../contributors/orgs/sap.md)

---

## 7. 相关链接

- [SAPMachine 官网](https://sap.github.io/SapMachine/)
- [SAPMachine GitHub](https://github.com/SAP/SapMachine)

---

**最后更新**: 2026-03-20
