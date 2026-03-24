# Sean Mullan

> **GitHub**: [@seanjmullan](https://github.com/seanjmullan)
> **Website**: [seanjmullan.org](https://seanjmullan.org/)
> **Inside.java**: [SeanMullan](https://inside.java/u/SeanMullan/)
> **LinkedIn**: [Sean Mullan](https://www.linkedin.com/in/sean-mullan-314694/)
> **Organization**: Oracle
> **Position**: Consulting Member of Technical Staff, Java Security Libraries Tech Lead
> **Location**: Cambridge, Massachusetts

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [核心技术贡献](#3-核心技术贡献)
4. [技术专长](#4-技术专长)
5. [合作关系](#5-合作关系)
6. [职业时间线](#6-职业时间线)
7. [Related Links](#7-related-links)

---


## 1. 概述

Sean Mullan 是 Oracle 的 **Consulting Member of Technical Staff**，担任 Java Security Libraries 团队的技术负责人，同时也是 **OpenJDK Security Group Lead**。他领导团队负责 Java 平台的加密和安全功能的规划与交付，包括后量子密码学 (Post-Quantum Cryptography) 和 Java Cryptographic Roadmap。他主导了 JEP 486（永久禁用 Security Manager）的实施，这是近年来 Java 安全架构最重大的变化之一。他拥有 Northeastern University 计算机科学硕士学位，曾在 Sun Microsystems 和 Hewlett Packard Enterprise 工作。他定期在个人博客 seanjmullan.org 上发布 JDK 安全增强的详细分析。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Sean Mullan |
| **当前组织** | Oracle (Java Platform Group) |
| **职位** | Consulting Member of Technical Staff |
| **GitHub** | [@seanjmullan](https://github.com/seanjmullan) |
| **LinkedIn** | [sean-mullan-314694](https://www.linkedin.com/in/sean-mullan-314694/) |
| **Website** | [seanjmullan.org](https://seanjmullan.org/) |
| **Inside.java** | [SeanMullan](https://inside.java/u/SeanMullan/) |
| **Mastodon** | [@seanjmullan@mastodon.world](https://mastodon.world/@seanjmullan) |
| **X/Twitter** | [@seanjmullan](https://x.com/seanjmullan) |
| **OpenJDK** | [@mullan](https://openjdk.org/census#mullan) |
| **角色** | OpenJDK Member, JDK Reviewer, JDK Updates Reviewer, Brisbane Reviewer, Security Group Lead |
| **专长** | Security Manager, Post-Quantum Cryptography, TLS, PKI, XML Security, Digital Signatures |
| **教育** | M.S. Computer Science, Northeastern University (1994-1997) |
| **JDK 26 贡献** | 3 commits (Security) |

> **数据来源**: [LinkedIn](https://www.linkedin.com/in/sean-mullan-314694/), [OpenJDK Census](https://openjdk.org/census#mullan), [Inside.java](https://inside.java/u/SeanMullan/), [seanjmullan.org](https://seanjmullan.org/)

---

## 3. 核心技术贡献

### 1. JEP 486: Permanently Disable the Security Manager

**JDK-8338411: Implement JEP 486: Permanently Disable the Security Manager**

Sean Mullan 主导实施了 JEP 486，永久禁用 Java Security Manager。这是一项重大变更，涉及 1889 个文件，62597 行删除：

- 移除 SecurityManager、Policy、AccessController 等 API 实现
- 约 95% 的变更为测试更新和 API 规范修改
- [PR #21498](https://github.com/openjdk/jdk/pull/21498)

### 2. Security Manager 依赖清理

**JDK-8344397: Remove Security Manager dependencies from java.security and sun.security packages**

- [PR #22418](https://github.com/openjdk/jdk/pull/22418)
- **JDK-8345502**: Remove doIntersectionPrivilege methods - [PR #22548](https://github.com/openjdk/jdk/pull/22548)

### 3. Post-Quantum Cryptography

参与 Java 后量子密码学路线图的规划与实施：
- **JEP 496**: Quantum-Resistant Module-Lattice-Based Key Encapsulation Mechanism (ML-KEM, JDK 24)
- **JEP 497**: Quantum-Resistant Module-Lattice-Based Digital Signature Algorithm (ML-DSA, JDK 24)
- **JEP 527**: Post-Quantum Hybrid Key Exchange for TLS 1.3 (JDK 27)

### 4. TLS 和加密标准

- **JDK-8283795**: Add TLSv1.3 and CNSA 1.0 algorithms to implementation requirements - [PR #22904](https://github.com/openjdk/jdk/pull/22904)
- XML 安全：XML 加密和签名
- PKI：公钥基础设施和证书管理

### 5. JDK 安全增强博客

在 seanjmullan.org 上定期发布 JDK 安全增强详细分析：
- [JDK 25 Security Enhancements](https://seanjmullan.org/blog/2025/09/23/jdk25)
- [JDK 23 Security Enhancements](https://seanjmullan.org/blog/2024/09/17/jdk23)
- [JDK 22 Security Enhancements](https://seanjmullan.org/blog/2024/03/20/jdk22)
- [JDK 19 Security Enhancements](https://seanjmullan.org/blog/2022/09/22/jdk19)
- [JDK 18 Security Enhancements](https://seanjmullan.org/blog/2022/03/23/jdk18)

---

## 4. 技术专长

### 安全

- **Security Manager**: 安全管理器架构与移除
- **Post-Quantum Cryptography**: ML-KEM, ML-DSA, 混合密钥交换
- **TLS**: Transport Layer Security 1.3
- **XML Security**: XML 加密和签名
- **PKI**: 公钥基础设施
- **Digital Signatures**: 数字签名
- **Java Cryptographic Roadmap**: 加密路线图规划

---

## 5. 合作关系

与以下安全开发者合作：
- **Valerie Peng**: Security Developer
- **Anthony Scarpino**: Security Developer
- **Hai-May Chao**: TLS Specialist

---

## 6. 职业时间线

| 时间 | 事件 | 详情 |
|------|------|------|
| **1994-1997** | Northeastern University | M.S. Computer Science |
| **~2000s** | Sun Microsystems / HPE | 安全相关开发 |
| **~2010s** | Oracle | Consulting Member of Technical Staff |
| **至今** | Security Group Lead | OpenJDK Security Group Lead, Java Security Libraries Tech Lead |
| **2024** | JEP 486 | 主导永久禁用 Security Manager |
| **2024-2025** | Post-Quantum Crypto | 推进后量子密码学路线图 |

---

## 7. Related Links

- **Website**: [seanjmullan.org](https://seanjmullan.org/)
- **GitHub**: [seanjmullan](https://github.com/seanjmullan)
- **Inside.java**: [SeanMullan](https://inside.java/u/SeanMullan/)
- **OpenJDK Census**: [mullan](https://openjdk.org/census#mullan)
- **OpenJDK Security Group**: [openjdk.org/groups/security](https://openjdk.org/groups/security/)
- **GitHub PRs**: [Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Aseanjmullan+is%3Aclosed+label%3Aintegrated)
- **JBS Issues**: [bugs.openjdk.org](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20mullan)
- **GitHub Commits**: [github.com/openjdk/jdk](https://github.com/openjdk/jdk/commits?author=seanjmullan)
- **Oracle Blog**: [blogs.oracle.com/mullan](https://blogs.oracle.com/mullan/)

---

**Sources**:
- [JDK 26 Top Contributors](./jdk26-top-contributors.md)
- [LinkedIn - Sean Mullan](https://www.linkedin.com/in/sean-mullan-314694/)
- [seanjmullan.org](https://seanjmullan.org/)
- [Inside.java - SeanMullan](https://inside.java/u/SeanMullan/)
- [OpenJDK Census](https://openjdk.org/census#mullan)
- [OpenJDK Security Group](https://openjdk.org/groups/security/)
- [JEP 486 PR #21498](https://github.com/openjdk/jdk/pull/21498)


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 457 |
| **活跃仓库数** | 2 |
