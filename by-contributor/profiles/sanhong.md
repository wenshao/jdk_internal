# Sanhong Li (李三红)

> **Java Champion** | **Director of Runtime & Compiler, Alibaba Cloud** | **Dragonwell JDK Lead**

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [职业经历](#3-职业经历)
4. [主要贡献](#4-主要贡献)
5. [学术论文](#5-学术论文)
6. [技术演讲](#6-技术演讲)
7. [团队贡献者](#7-团队贡献者)
8. [相关链接](#8-相关链接)

---


## 1. 概述

Sanhong Li (李三红) 是 **Java Champion**，阿里巴巴云智能基础产品事业部 **Director of Runtime & Compiler**，担任 Chief JVM Architect。他自 2004 年开始从事 Java 相关工作，先后在 Intel 亚太研发实验室、IBM (J9VM 团队) 和阿里巴巴工作。2014 年加入阿里巴巴后，他领导了 Alibaba JDK (AJDK) 和开源 [Dragonwell JDK](https://dragonwell-jdk.io/) 的开发，该 JDK 运行在阿里巴巴 **100,000+ 台服务器**上，支撑淘宝、天猫、蚂蚁、菜鸟等核心业务。

他发表了 **10+ 篇学术论文** (ICSE, ASE, USENIX ATC, EuroSys, DAC 等顶会)，拥有 **20+ 项技术专利**，并在 JVM Language Summit、JavaOne、QCon、Joker 等国际会议上发表演讲。

**社区角色**:
- **Java Champion**
- **JCP Executive Committee** 阿里巴巴代表
- **GraalVM Project Advisory Board** 成员
- **Adoptium Summit 2025 Program Committee** 成员
- **上海 Java 用户组 ([GreenTeaJUG](http://greenteajug.cn/))** 联合负责人 (中国最大 JUG, 与[莫简豪](https://github.com/mojianhao)共同领导)
- **APMCon** 联合主席

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Sanhong Li (李三红) |
| **职位** | Java Champion, Director of Runtime & Compiler, Alibaba Cloud |
| **GitHub** | [@sanhong](https://github.com/sanhong), [@alijvm](https://github.com/alijvm) |
| **LinkedIn** | [linkedin.com/in/san-hong-li-443732a](https://www.linkedin.com/in/san-hong-li-443732a/) |
| **DBLP** | [Sanhong Li (10 篇)](https://dblp.org/pid/198/7528.html) |
| **主要领域** | Dragonwell JDK, JVM 架构, GC, Serverless Java, RISC-V, GraalVM |
| **论文** | 10+ 篇 (ICSE ×3, USENIX ATC, EuroSys, ASE, DAC, ICPE ×2, IEEE TC) |
| **专利** | 20+ 项技术专利 |
| **社区** | Java Champion, JCP EC, GraalVM Advisory Board, GreenTeaJUG 联合负责人 |
| **组织** | [Alibaba](../../contributors/orgs/alibaba.md) |

---

## 3. 职业经历

| 时间 | 组织 | 角色 | 工作内容 |
|------|------|------|----------|
| **2004** | Intel 亚太研发实验室 | 工程师 | 实现 JSR135 (Mobile Media API) |
| **2008** | IBM | 运行时安全工程师 | OSGi 平台运行时安全改进 |
| **2010** | IBM (J9VM) | JVM 开发者 | IBM J9 虚拟机开发，主导 JVM 多租户技术项目 |
| **2014-至今** | Alibaba | Chief JVM Architect → Director | 领导 AJDK/Dragonwell JDK, JVM 云计算优化 |

---

## 4. 主要贡献

### 4.1 Alibaba Dragonwell JDK
- 领导开发 AJDK (Alibaba/AlipayJDK)，托管淘宝、天猫、蚂蚁、菜鸟等核心应用
- 2015 年开始基于 OpenJDK 8 进行优化和定制
- 推动 Dragonwell JDK 开源 ([dragonwell-jdk.io](https://dragonwell-jdk.io/))
- 运行在 **100,000+ 服务器**上，针对电商、金融、物流场景优化
- 特色功能：ElasticHeap、JWarmUp、JFR 扩展、Compact Object Headers
- 支持版本：Dragonwell 8 / 11 / 17 / 21

→ [Dragonwell 介绍 PDF](https://assets.ctfassets.net/oxjq45e8ilak/T2zSvRNiiV7dKSixYpXij/03109f27cc33d87d85dff044f6dada90/100770_1555814710_Sanhong_li_Glimpse_into_Alibaba_Dragonwell_Towards_a_Java_runtime_for_cloud_computing.pdf)

### 4.2 GC 研究
- **Platinum GC** (USENIX ATC 2020): CPU-efficient concurrent GC for interactive services
  - 合作者包括 **Tongbao Zhang** (腾讯) 和 SJTU IPADS 实验室
- **Jade GC** (EuroSys 2024): 由团队成员 Denghui Dong, Liang Mao, Yude Lin, Xiaowei Lu 等贡献
- **JPDHeap** (DAC 2021): PM-DRAM 混合内存的 JVM 堆设计

### 4.3 RISC-V Java 移植
- 推动 Java on RISC-V 的 OpenJDK 移植工作
- [RISC-V Forum 2021 演讲](https://riscvforumdttc2021.sched.com/event/jGkK) (与 Kuai Wei 合作)

### 4.4 GraalVM / 静态编译
- GraalVM Project Advisory Board 成员
- 领导阿里巴巴大规模使用 GraalVM native-image 静态编译微服务
- [Static Compilation at Alibaba at Scale](https://medium.com/graalvm/static-compilation-of-java-applications-at-alibaba-at-scale-2944163c92e)

### 4.5 Java 安全
- **SafeCheck** (ICSE 2019): Java Unsafe API 安全增强
- **Lejacon** (ICSE 2023): SGX 上的轻量 Java 机密计算
- **SGX-Friendly Java Runtime** (IEEE TC 2024)

---

## 5. 学术论文

| 年份 | 会议 | 论文标题 | 合著者 (Alibaba 相关) |
|------|------|----------|----------------------|
| **2024** | IEEE TC | Toward an SGX-Friendly Java Runtime | Mingyu Wu (SJTU) |
| **2024** | EuroSys | [Jade: A High-throughput Concurrent Copying GC](https://dl.acm.org/doi/10.1145/3627703.3650087) | **Liang Mao, Yude Lin, Xiaowei Lu, Denghui Dong** |
| **2023** | ICSE | Lejacon: Lightweight Java Confidential Computing on SGX | — |
| **2023** | SIGMOD | Vineyard: Optimizing Data Sharing in Analytics | — |
| **2021** | ASE | Towards a Serverless Java Runtime | **Kuai Wei** |
| **2021** | DAC | JPDHeap: JVM Heap Design for PM-DRAM | — |
| **2020** | USENIX ATC | [Platinum: CPU-Efficient Concurrent GC for Tail-Reduction](https://www.usenix.org/conference/atc20/presentation/wu-mingyu) | **Tongbao Zhang** (Tencent!) |
| **2019** | ICSE | SafeCheck: Safety Enhancement of Java Unsafe API | — |
| **2018** | ICSE SEIP | [Java Performance Troubleshooting at Alibaba](https://2018.splashcon.org/profile/sanhongli) | **Denghui Dong** |
| **2018** | ICPE | Cloud-Scale Java Profiling at Alibaba | **Denghui Dong, Tongbao Zhang** |
| **2017** | ICPE | Developing Software Performance Training at Alibaba | **Tongbao Zhang** |

> **注**: 加粗的合著者是本项目中记录的 OpenJDK 上游贡献者。李三红与 [Denghui Dong](denghui-dong.md)、[Kuai Wei](kuai-wei.md)、[Tongbao Zhang](tongbao-zhang.md)、[Liang Mao](liang-mao.md)、[Yude Lin](yude-lin.md)、[Xiaowei Lu](xiaowei-lu.md) 均有学术合作。

---

## 6. 技术演讲

| 会议 | 年份 | 主题 | 链接 |
|------|------|------|------|
| JVM Language Summit | 多次 | Alibaba JDK / Dragonwell | - |
| JavaOne | 多次 | JVM 优化和云计算 | - |
| QCon | 多次 | Java 性能和 JVM 技术 | - |
| Joker 2019 | 2019 | Glimpse into Alibaba Dragonwell | [详情](https://2019.jokerconf.com/en/2019/talks/1yykjlq2gbnx9czwhwl0cq/) |
| SPLASH 2018 | 2018 | JVM 相关研究 | [Profile](https://2018.splashcon.org/profile/sanhongli) |
| ICSE 2019 | 2019 | SafeCheck 论文报告 | [Profile](https://2019.icse-conferences.org/profile/sanhongli) |
| ICSE 2023 | 2023 | Lejacon 论文 | [Profile](https://conf.researchr.org/profile/icse-2023/sanhongli) |
| RISC-V Forum 2021 | 2021 | Java on RISC-V: OpenJDK Porting | [Schedule](https://riscvforumdttc2021.sched.com/event/jGkK) |
| JCP EC | 2017 | Java at Alibaba | [PDF](https://jcp.org/aboutJava/communityprocess/ec-public/materials/2017-02-14/Java_at_Alibaba.pdf) |
| Extreme Scaling | - | Extreme Scaling with Alibaba JDK | [PDF](https://assets.ctfassets.net/oxjq45e8ilak/7J537sIeZisGIgwe4qyAE6/33503896530097133df7e7cdaa7837db/Sanhong_Extreme_Scaling_with_Alibaba_JDK.pdf) |

---

## 7. 团队贡献者

李三红作为 Alibaba JVM 团队负责人，指导以下贡献者的 OpenJDK 上游贡献：

| 贡献者 | PRs | 学术合作 | 详情 |
|--------|-----|----------|------|
| [Shaojin Wen](shaojin-wen.md) | 97 | - | 核心库优化 |
| [Yi Yang (杨易)](yi-yang.md) | 57 | - | C2 编译器, HeapDump |
| [Denghui Dong (董登辉)](denghui-dong.md) | 36 | ICSE 2018, ICPE 2018, EuroSys 2024 | C1, JFR, Eclipse Jifa |
| [Max Xing](max-xing.md) | 16 | - | RISC-V, C2 |
| [Kuai Wei](kuai-wei.md) | 13 | ASE 2021, RISC-V Forum 2021 | C2, MergeStore |
| [Yude Lin](yude-lin.md) | 8 | EuroSys 2024 | G1 GC, AArch64 |
| [Joshua Zhu](joshua-zhu.md) | 6 | - | AArch64, 编译器 |
| [Xiaowei Lu](xiaowei-lu.md) | 3 | EuroSys 2024 | ZGC |
| [Long Yang](long-yang.md) | 3 | - | JFR, Runtime |
| [sandlerwang](sandlerwang.md) | 3 | - | AArch64, GC |
| [Lingjun Cao](lingjun-cao.md) | 2 | - | DecimalFormat |
| [Liang Mao (毛亮)](liang-mao.md) | 2 | EuroSys 2024 | GC, Compact Object Headers |
| [SendaoYan](sendaoyan.md) | 202 | - | 编译器/GC 测试 (前员工) |

> 跨组织合作: Platinum GC (USENIX ATC 2020) 论文与 **[Tongbao Zhang](tongbao-zhang.md)** (Tencent) 合作。

---

## 8. 相关链接

### 个人
- [LinkedIn](https://www.linkedin.com/in/san-hong-li-443732a/)
- [GitHub @sanhong](https://github.com/sanhong)
- [GitHub @alijvm](https://github.com/alijvm)
- [DBLP 论文列表](https://dblp.org/pid/198/7528.html)

### 项目
- [Dragonwell JDK 官网](https://dragonwell-jdk.io/)
- [Dragonwell 8](https://github.com/dragonwell-project/dragonwell8) / [11](https://github.com/dragonwell-project/dragonwell11) / [17](https://github.com/dragonwell-project/dragonwell17) / [21](https://github.com/dragonwell-project/dragonwell21)
- [GraalVM Advisory Board](https://www.graalvm.org/)
- [Adoptium Summit 2025 Program Committee](https://www.eclipse.org/events/2025/adoptium-summit/program-committee/)

### 组织
- [Alibaba 组织页面](../../contributors/orgs/alibaba.md)
- [Dragonwell 团队](../../contributors/orgs/dragonwell.md)
- [GreenTeaJUG (上海 JUG)](http://greenteajug.cn/)
- [中国贡献者索引](chinese-contributors.md)

---

> **文档版本**: 3.0
> **最后更新**: 2026-03-23
> **本次更新**:
> - 新增 Java Champion 头衔
> - 新增 JCP Executive Committee, GraalVM Advisory Board, Adoptium Summit 2025 角色
> - 职位更新: Chief JVM Architect → Director of Runtime & Compiler
> - DBLP 论文从 4 篇扩展为完整 10 篇 (新增 Platinum/USENIX ATC, Jade/EuroSys, Lejacon/ICSE, SGX/IEEE TC, Vineyard/SIGMOD)
> - 新增 LinkedIn 链接
> - 新增演讲链接 (Joker 2019, JCP EC 2017, RISC-V Forum)
> - 新增团队贡献者表（含学术合作关系）
> - 新增跨组织合作发现: Platinum GC 论文与 Tongbao Zhang (Tencent) 合作
