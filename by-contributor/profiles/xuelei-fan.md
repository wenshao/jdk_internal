# Xuelei Fan

> **Organization**: Salesforce (formerly Oracle)
> **Role**: Security Engineer, TLS/JSSE Expert

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [核心技术贡献](#3-核心技术贡献)
4. [技术专长](#4-技术专长)
5. [合作关系](#5-合作关系)

---


## 1. 概述

Xuelei Fan (范学雷, also known as Xue-Lei Andrew Fan) 是一位资深 **Java 安全工程师**，曾在 Oracle Java Security Team 工作约 7-8 年，现任职于 Salesforce。他是 Java TLS/SSL 实现的核心开发者，主导了 **JEP 332: TLS 1.3** 的实现，重新设计了整个 TLS 协议栈。毕业于清华大学。在 JDK 26 中以 3 次提交贡献于安全模块。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Xuelei Fan (范学雷 / Xue-Lei Andrew Fan) |
| **当前组织** | Salesforce |
| **前组织** | Oracle (Java Platform Group, Java Security Team, ~7-8 年) |
| **教育** | 清华大学 (Tsinghua University) |
| **OpenJDK 角色** | Reviewer |
| **专长** | SSL/TLS, JSSE, DTLS, SNI, Security, Cryptography |
| **JDK 26 贡献** | 3 commits (Security) |

---

## 3. 核心技术贡献

### 1. TLS 1.3 实现 (JEP 332)

Xuelei Fan 主导了 Java 平台 TLS 1.3 协议的实现，这是他在 Oracle 期间最重要的贡献之一：
- **重新实现 TLS 协议栈**: 重新设计 TLS 握手代码，使其更可扩展和高性能
- **JEP 332**: Transport Layer Security (TLS) 1.3 — 在 JDK 11 中发布
- **JSSE 架构**: 重构 Java Secure Socket Extension 框架

### 2. DTLS 和 SNI 支持

- **DTLS API**: 定义了 Datagram Transport Layer Security (DTLS) 1.0/1.2 API
- **SNI Extension**: 添加 TLS Server Name Indication 扩展支持，改善安全虚拟主机能力
- **X25519/X448**: TLS 中的现代密钥交换算法支持

### 3. 持续贡献

- **Cipher Suites**: 加密套件管理和优化
- **安全审查**: 作为 OpenJDK Reviewer 持续审查安全相关代码

---

## 4. 技术专长

### 安全通信

- **SSL/TLS**: 安全传输层 (TLS 1.0-1.3)
- **DTLS**: 数据报传输层安全
- **JSSE**: Java 安全套接字扩展 (架构重构)
- **HTTPS**: 安全 HTTP
- **密码学**: 密钥交换、证书验证、加密算法

---

## 5. 合作关系

与以下安全开发者合作：
- **Hai-May Chao**: TLS 1.3 Hybrid KE Author
- **Valerie Peng**: Security Lead
- **Sean Mullan**: Security Developer

---

**Sources**:
- [JDK 26 Top Contributors](./jdk26-top-contributors.md)
