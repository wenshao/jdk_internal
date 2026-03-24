# Anthony Scarpino

> **Organization**: Oracle
> **Role**: Security Lead
> **LinkedIn**: [izick](https://www.linkedin.com/in/izick/)
> **OpenJDK**: [@ascarpino](https://openjdk.org/census#ascarpino)
> **Inside.java**: [AnthonyScarpino](https://inside.java/u/AnthonyScarpino/)

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [主要 JEP 贡献](#3-主要-jep-贡献)
4. [核心技术贡献](#4-核心技术贡献)
5. [技术专长](#5-技术专长)
6. [合作关系](#6-合作关系)
7. [相关链接](#7-相关链接)

---


## 1. 概述

Anthony Scarpino 是 Oracle 的 **安全模块负责人**，专注于 Java 加密和安全框架。他是 **JEP 524 (PEM Encodings)** 的作者，在 JDK 26 中以 14 次提交贡献于安全功能。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Anthony Scarpino |
| **当前组织** | Oracle (Java Platform Group) |
| **职位** | Principal Member of Technical Staff |
| **OpenJDK** | [@ascarpino](https://openjdk.org/census#ascarpino) |
| **角色** | Reviewer, Committer |
| **LinkedIn** | [izick](https://www.linkedin.com/in/izick/) |
| **专长** | Security, Cryptography, PKI, PEM Encodings |
| **JDK 26 贡献** | 14 commits (Security) |

---

## 3. 主要 JEP 贡献

### JEP 524: PEM Encodings

| 属性 | 值 |
|------|-----|
| **角色** | Author |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 26 |

**影响**: 为 Java 安全模块添加 PEM (Privacy-Enhanced Mail) 编码支持：
- 支持标准 PEM 格式
- 简化密钥和证书导入
- 增强与 OpenSSL 等工具的互操作性

```java
// PEM 格式支持示例
// 之前需要 Base64 解码，现在可以直接使用 PEM 格式
String pemKey = """
    -----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQ...
    -----END PRIVATE KEY-----
    """;
```

---

## 4. 核心技术贡献

### 1. 安全框架

Anthony Scarpino 负责 Java 安全框架：
- **java.security**: 安全基础类
- **java.crypto**: 加密服务
- **PKI**: 公钥基础设施

### 2. PEM 支持

- **PEM Parser**: PEM 格式解析器
- **Key Encoding**: 密钥编码
- **Certificate**: 证书处理

---

## 5. 技术专长

### 安全

- **Cryptography**: 加密算法
- **PKI**: 公钥基础设施
- **TLS**: 安全传输层
- **PEM**: PEM 编码格式

---

## 6. 合作关系

与以下安全开发者合作：
- **Hai-May Chao**: TLS 1.3 Hybrid Key Exchange (JEP 527)
- **Weijun Wang**: Security Developer
- **Sean Mullan**: Security Developer
- **Valerie Peng**: Security Developer

---

## 7. 相关链接

### JEP 文档
- [JEP 524: PEM Encodings](https://openjdk.org/jeps/524)

---

**Sources**:
- [JEP 524: PEM Encodings](https://openjdk.org/jeps/524)
- [JDK 26 Top Contributors](./jdk26-top-contributors.md)


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 119 |
| **活跃仓库数** | 2 |
