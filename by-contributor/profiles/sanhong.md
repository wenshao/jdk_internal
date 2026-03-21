# Sanhong Li

> **Chief JVM Architect, Alibaba Cloud** | **Dragonwell JDK Lead** | **ICSE/ASE Author**

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [职业经历](#3-职业经历)
4. [主要贡献](#4-主要贡献)
5. [学术论文](#5-学术论文)
6. [技术演讲](#6-技术演讲)
7. [社交网络关联](#7-社交网络关联)
8. [相关链接](#8-相关链接)

---


## 1. 概述

Sanhong Li (李三红) 是阿里巴巴云智能基础产品事业部的高级技术专家，担任 Chief JVM Architect。他自 2004 年开始从事 Java 相关工作，先后在 Intel 亚太研发实验室、IBM（J9VM 团队）和阿里巴巴工作。2014 年加入阿里巴巴后，他领导了 Alibaba JDK (AJDK) 和开源 Dragonwell JDK 的开发。他发表了超过 10 篇技术论文，拥有多项技术专利，并在 JVM Language Summit、JavaOne、QCon 等国际会议上发表演讲。他共同领导上海 Java 用户组 (GreenTeaJUG)，并共同主持 APMCon。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Sanhong Li (李三红) |
| **GitHub** | [@sanhong](https://github.com/sanhong), [@alijvm](https://github.com/alijvm) |
| **DBLP** | [Sanhong Li](https://dblp.org/pid/198/7528.html) |
| **职位** | Chief JVM Architect, Alibaba Cloud |
| **主要领域** | Dragonwell JDK, Serverless Java, JVM, RISC-V Porting, JVM Heap 设计 |
| **论文数** | 10+ 篇技术论文 |
| **专利** | 多项技术专利 |
| **社区角色** | 上海 Java 用户组 (GreenTeaJUG) 联合负责人, APMCon 联合主席 |

---

## 3. 职业经历

| 时间 | 组织 | 角色 | 工作内容 |
|------|------|------|----------|
| 2004 年 | Intel 亚太研发实验室 | 工程师 | 实现 JSR135 (Mobile Media API) |
| 2008 年 | IBM | 运行时安全工程师 | OSGi 平台运行时安全改进 |
| 2010 年 | IBM (J9VM) | JVM 开发者 | IBM J9 虚拟机开发，主导 JVM 多租户技术项目 |
| 2014 年至今 | Alibaba | Chief JVM Architect | 领导 AJDK/Dragonwell JDK 开发，JVM 云计算优化 |

---

## 4. 主要贡献

### 4.1 Alibaba Dragonwell JDK
- 领导开发 AJDK (Alibaba/AlipayJDK)，托管淘宝、天猫、蚂蚁、菜鸟等核心应用
- 2015 年开始基于 OpenJDK 8 进行优化和定制
- 推动 Dragonwell JDK 开源，作为 OpenJDK 的下游版本
- Dragonwell 针对在线电商、金融、物流应用优化，运行在 100,000+ 服务器上
- 支持 Dragonwell 8、11、17 多个版本

### 4.2 RISC-V Java 移植
- 推动 Java on RISC-V 的 OpenJDK 移植工作
- 在 RISC-V Forum: Developer Tools & Tool Chains (2021) 上展示移植进展

### 4.3 Serverless Java 运行时
- 研究面向无服务器计算的 Java 运行时优化
- ASE 2021 论文: "Towards a Serverless Java Runtime"

### 4.4 JVM 性能优化
- 面向云计算规模的 Java 性能调优
- ICSE (SEIP) 2018: "Java performance troubleshooting and optimization at alibaba"
- JVM 堆设计: PM-DRAM 混合内存的 JVM 堆设计 (JPDHeap, DAC 2021)

---

## 5. 学术论文

| 年份 | 会议 | 论文标题 |
|------|------|----------|
| 2021 | ASE | "Towards a Serverless Java Runtime" |
| 2021 | DAC | "JPDHeap: A JVM Heap Design for PM-DRAM Memories" |
| 2019 | ICSE | "SafeCheck: Safety Enhancement of Java Unsafe API" |
| 2018 | ICSE (SEIP) | "Java performance troubleshooting and optimization at alibaba" |

### 代表性论文详情

**SafeCheck (ICSE 2019)**:
- 作者: Shiyou Huang, Jianmei Guo, **Sanhong Li**, Xiang Li, Yumin Qi, Kingsum Chow, Jeff Huang
- 内容: Java Unsafe API 安全增强，解决第三方库大量使用 Unsafe API 带来的安全风险

**ASE 2021**: "Towards a Serverless Java Runtime"
- 作者: Yifei Zhang, Tianxiao Gu, Xiaolin Zheng, Lei Yu, **Wei Kuai**, **Sanhong Li**
- 单位: Alibaba Group
- DBLP: [记录](https://dblp.org/rec/conf/kbse/0001GZYKL21)

---

## 6. 技术演讲

| 会议 | 主题 |
|------|------|
| JVM Language Summit | Alibaba JDK / Dragonwell 相关 |
| JavaOne | JVM 优化和云计算 |
| QCon | Java 性能和 JVM 技术 |
| SPLASH 2018 | JVM 相关研究 |
| ICSE 2019 | SafeCheck 论文报告 |
| ICSE 2023 | 研究成果分享 |
| RISC-V Forum 2021 | Java on RISC-V: OpenJDK Porting Work Update |
| Alibaba Dragonwell Talk | "Glimpse into Alibaba Dragonwell: Towards a Java runtime for cloud computing" |

---

## 7. 社交网络关联

| 关联类型 | 用户 | 推断 |
|----------|------|------|
| **论文合著者** | kuaiwei | Kuai Wei, ASE 2021 论文合著者, RISC-V Forum 2021 共同演讲者 |
| **论文合著者** | Shiyou Huang | SafeCheck ICSE 2019 合著者 |
| **论文合著者** | Jianmei Guo | SafeCheck ICSE 2019 合著者 |

---

## 8. 相关链接

- [GitHub (personal): @sanhong](https://github.com/sanhong)
- [GitHub (team): @alijvm](https://github.com/alijvm)
- [DBLP 学术论文列表](https://dblp.org/pid/198/7528.html)
- [Dragonwell JDK 官网](https://dragonwell-jdk.io/)
- [Dragonwell 8 (GitHub)](https://github.com/dragonwell-project/dragonwell8)
- [Dragonwell 11 (GitHub)](https://github.com/dragonwell-project/dragonwell11)
- [Dragonwell 17 (GitHub)](https://github.com/dragonwell-project/dragonwell17)
- [Alibaba Dragonwell 开源博客](https://www.alibabacloud.com/blog/alibaba-makes-dragonwell-openjdk-open-source_594624)
- [GreenTeaJUG (上海 JUG)](http://greenteajug.cn/)
- [Kuai Wei](kuai-wei.md) - 阿里巴巴 C2 编译器专家
- [中国贡献者](chinese-contributors.md) - 中国 OpenJDK 贡献者

---

> **文档版本**: 2.0
> **最后更新**: 2026-03-22
