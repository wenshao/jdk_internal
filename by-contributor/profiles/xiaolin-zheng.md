# Xiaolin Zheng (郑晓林)

> Alibaba JVM 团队，RISC-V OpenJDK 移植贡献者，JEP 422 联合实现者，Dragonwell 开发者

---
## 目录

1. [基本信息](#1-基本信息)
2. [技术专长](#2-技术专长)
3. [贡献概览](#3-贡献概览)
4. [关键贡献详解](#4-关键贡献详解)
5. [开发风格](#5-开发风格)
6. [相关链接](#6-相关链接)

---

## 1. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Xiaolin Zheng (郑晓林) |
| **当前组织** | [Alibaba](../../contributors/orgs/alibaba.md) - JVM 团队 |
| **位置** | 中国 |
| **GitHub** | [@zhengxiaolinX](https://github.com/zhengxiaolinX) |
| **邮箱** | yunyao.zxl [at] alibaba-inc.com |
| **主要领域** | RISC-V 移植, JVM 内部实现, Dragonwell, Serverless Java |
| **代表性贡献** | JEP 422 (Linux/RISC-V Port) 联合实现者 |

> **数据来源**: [JEP 422](https://openjdk.org/jeps/422), [JDK-8276799](https://github.com/openjdk/jdk/commit/5905b02c0e2643ae8d097562f181953f6c88fc89), [OpenJDK RISC-V Port](https://wiki.openjdk.org/spaces/RISCVPort/overview)

---

## 2. 技术专长

`RISC-V` `JVM` `Dragonwell` `Serverless Java` `JIT Compiler` `Platform Porting`

Xiaolin Zheng 是 Alibaba JVM 团队的工程师，专注于 RISC-V 平台的 OpenJDK 移植工作。他是 JEP 422 (Linux/RISC-V Port) 的联合实现者之一，代表 Alibaba 参与了 RISC-V OpenJDK 的上游开发。他还参与了 Dragonwell JDK 的开发和 Serverless Java Runtime 的研究。

---

## 3. 贡献概览

### 关键成就

| 项目 | 贡献 | 影响 |
|------|------|------|
| **JEP 422** | Linux/RISC-V Port 联合实现者 | OpenJDK 19 正式集成 RISC-V 移植 |
| **Dragonwell** | JDK 开发和维护 | Alibaba 内部 10 万+ 服务器运行 |
| **Serverless Java** | "Towards a Serverless Java Runtime" 论文 | ASE 2021 Industry Showcase |
| **RISC-V 测试** | 定期构建和测试 | 保障 RISC-V 移植质量 |

### JEP 422 中的角色

Alibaba 是 JEP 422 (Linux/RISC-V Port) 的三大支持组织之一 (Huawei, Alibaba, Red Hat)。Xiaolin Zheng 代表 Alibaba 团队:
- 贡献 RISC-V 移植代码
- 定期在 Linux/RISC-V 和其他 JDK 平台上构建和测试
- 承诺通过定期更新和测试完全支持该移植

---

## 4. 关键贡献详解

### 1. JEP 422: Linux/RISC-V Port (OpenJDK 19)

**背景**: 2021 年，Huawei 毕昇 JDK 团队发起了 OpenJDK RISC-V 移植项目。Alibaba 是三大支持组织之一。

**贡献**: Xiaolin Zheng 代表 Alibaba 参与 RISC-V 移植的实现工作:
- 与 Huawei (Fei Yang, Yadong Wang 等) 和 Red Hat (Andrew Haley 等) 合作
- 贡献代码到 Template Interpreter、C1/C2 JIT 后端
- 支持 RV64G (IMAFD) 指令集

**影响**: JEP 422 在 OpenJDK 19 中正式集成，使 Java 成为首批完整支持 RISC-V 的主流语言运行时之一。

### 2. Dragonwell JDK

Dragonwell 是 Alibaba 的 OpenJDK 下游发行版，针对电商、金融、物流等场景优化:
- 在 Alibaba 内部 10 万+ 服务器上运行
- 支持 Alibaba 核心业务场景的 JVM 优化
- 开源发布于 GitHub (dragonwell-project)

### 3. Serverless Java Runtime 研究

Xiaolin Zheng 是 "Towards a Serverless Java Runtime" 论文的共同作者 (ASE 2021)，与 Alibaba 同事 Yifei Zhang, Tianxiao Gu, Lei Yu, Wei Kuai, Sanhong Li 合作，研究 Java 在 Serverless 场景下的运行时优化。

---

## 5. 开发风格

Xiaolin Zheng 的贡献特点:

1. **平台移植**: 专注于 RISC-V 等新兴架构的 JDK 移植
2. **企业驱动**: 从 Alibaba 大规模部署需求出发进行优化
3. **跨组织合作**: 与 Huawei、Red Hat 等组织紧密协作
4. **研究导向**: 发表学术论文，推动 Java 技术前沿

---

## 6. 相关链接

| 类型 | 链接 |
|------|------|
| **GitHub** | [@zhengxiaolinX](https://github.com/zhengxiaolinX) |
| **JEP 422** | [Linux/RISC-V Port](https://openjdk.org/jeps/422) |
| **Dragonwell** | [dragonwell-jdk.io](https://dragonwell-jdk.io/) |
| **Dragonwell GitHub** | [dragonwell-project](https://github.com/dragonwell-project) |
| **RISC-V Port Wiki** | [OpenJDK RISC-V Port](https://wiki.openjdk.org/spaces/RISCVPort/overview) |
| **Alibaba Cloud JDK** | [Alibaba Dragonwell](https://www.alibabacloud.com/blog/alibaba-makes-dragonwell-openjdk-open-source_594624) |

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-22
> **状态**: 初稿
