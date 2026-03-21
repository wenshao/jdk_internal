# Volker Simonis

> **GitHub**: [@simonis](https://github.com/simonis)
> **OpenJDK**: [@simonis](https://openjdk.org/census#simonis)
> **Organization**: Amazon Web Services (前 SAP)
> **Role**: Principal Software Engineer, OpenJDK PowerPC/AIX & s390x Port Project Lead

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [职业历程](#3-职业历程)
4. [主要贡献](#4-主要贡献)
5. [核心技术贡献](#5-核心技术贡献)
6. [技术演讲](#6-技术演讲)
7. [技术专长](#7-技术专长)
8. [协作网络](#8-协作网络)
9. [相关链接](#9-相关链接)

---


## 1. 概述

Volker Simonis 是 **Amazon Web Services Corretto 团队**的 Principal Software Engineer，此前长期在 **SAP JVM Technology Group** 担任 OpenJDK 负责人。他于 2007 年 OpenJDK 项目创立之初即加入社区，是 OpenJDK 最早期的外部贡献者之一。他是 **OpenJDK PowerPC/AIX Port** 和 **s390x Port** 项目的 Project Lead，领导了第一个被集成到 OpenJDK 主线的外部硬件平台移植项目，为后续的 AArch64 等移植铺平了道路。他拥有图宾根大学 (University of Tubingen) 计算机科学硕士和博士学位，曾在 OpenJDK Governing Board 任职，并担任 JCP Executive Committee 代表。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Volker Simonis |
| **当前组织** | Amazon Web Services (Corretto 团队) |
| **前组织** | SAP (JVM Technology Group) |
| **职位** | Principal Software Engineer |
| **GitHub** | [@simonis](https://github.com/simonis) |
| **OpenJDK** | [@simonis](https://openjdk.org/census#simonis) |
| **个人主页** | [progdoc.de](https://progdoc.de/) / [simonis.io](https://simonis.io/) |
| **角色** | OpenJDK Member, Reviewer, Committer; 前 Governing Board 成员 |
| **教育背景** | 图宾根大学 (Universitat Tubingen) 计算机科学硕士和博士 |
| **主要领域** | PowerPC/AIX Port, s390x Port, SapMachine, CRaC, CDS |
| **早期经历** | Sun Microsystems, 图宾根大学 |

> **数据来源**: [GitHub](https://github.com/simonis), [FOSDEM Speaker Profile](https://archive.fosdem.org/2024/schedule/speaker/ZZTDLL/), [JeeConf Speaker Profile](https://jeeconf.com/speaker/volker-simonis/), [Crunchbase](https://www.crunchbase.com/person/volker-simonis)

---

## 3. 职业历程

| 时间 | 事件 | 详情 |
|------|------|------|
| **~1990s-2000s** | 图宾根大学 | 计算机科学硕士和博士，Wilhelm-Schickard-Institut fur Informatik |
| **早期** | Sun Microsystems | 早期 JVM 经验 |
| **2007** | 加入 OpenJDK 社区 | 项目创立之初即参与 |
| **~2007-2023** | SAP JVM Technology Group | SAP 的 OpenJDK 负责人，JCP EC 代表 |
| **2012-06** | PowerPC/AIX Port 项目启动 | 与 IBM 合作发起移植项目 |
| **2013-02** | FOSDEM 2013 演讲 | "Power to the People - the OpenJDK PowerPC/AIX Port" |
| **2014-02** | FOSDEM 2014 演讲 | "The OpenJDK PowerPC/AIX Port Endgame" |
| **JDK 9** | PowerPC/AIX Port 集成 | 移植代码成功合并到 OpenJDK 主线 |
| **2016-05** | s390x Port 项目创建 | 发起 Linux/s390x 移植项目并担任 Lead |
| **JDK 9** | JEP 294: Linux/s390x Port | s390x 移植代码集成到 JDK 9 |
| **~2023** | 加入 Amazon Web Services | Corretto 团队 Principal Software Engineer |
| **2024-05** | 辞任 s390x Port Lead | 移交项目领导权 |

---

## 4. 主要贡献

### OpenJDK PowerPC/AIX Port

| 属性 | 值 |
|------|-----|
| **角色** | Project Lead |
| **合作方** | IBM, SAP |
| **状态** | Integrated |

**影响**: 这是第一个被集成到 OpenJDK 主线的外部贡献的硬件平台移植。项目由 IBM 和 SAP 联合驱动，目标是在 Linux/PowerPC 和 AIX/PowerPC 平台上提供完整的、可认证的 OpenJDK 版本。该项目的成功为后续 AArch64、s390x 等平台移植建立了流程和先例。

### JEP 294: Linux/s390x Port

| 属性 | 值 |
|------|-----|
| **角色** | Project Lead |
| **状态** | Delivered |
| **发布版本** | JDK 9 |

**影响**: 将 SAP 多年在生产环境中使用的 Linux/s390x (IBM System z) 完整移植集成到 OpenJDK，包括模板解释器、C1 和 C2 JIT 编译器。

### SapMachine

作为 SAP OpenJDK 负责人期间，推动了 **SapMachine** 的发展：
- SapMachine 是 SAP 维护和支持的 OpenJDK 发行版
- 编写和维护 [SapMachine 与 OpenJDK 差异文档](https://github.com/SAP/SapMachine/wiki/Differences-between-SapMachine-and-OpenJDK)
- 贡献 SapMachine 演讲资料

---

## 5. 核心技术贡献

### 1. 平台移植

- **PowerPC 后端**: HotSpot 的 PowerPC 机器码生成和优化
- **AIX 支持**: JDK 在 IBM AIX 操作系统上的适配
- **s390x 后端**: System z 架构的模板解释器和 JIT 编译器
- **跨平台构建**: 多平台构建系统的维护

### 2. OpenJDK 治理

- **Governing Board 成员**: 参与 OpenJDK 项目治理决策
- **JCP Executive Committee**: 代表 SAP 参与 Java 标准制定 (Java SE 9-13)
- **社区建设**: 帮助 SAP 全面参与 OpenJDK 社区

### 3. JVM 内部机制

- **Class Data Sharing (CDS)**: 研究和演讲 HotSpot CDS 技术
- **JVM Internals**: 多次在技术大会分享 OpenJDK JVM 内部机制
- **CRaC (Coordinated Restore at Checkpoint)**: FireCRaCer 相关工作

---

## 6. 技术演讲

| 标题 | 时间 | 场合 |
|------|------|------|
| **Power to the People - the OpenJDK PowerPC/AIX Port** | 2013-02 | FOSDEM 2013 |
| **The OpenJDK PowerPC/AIX Port Endgame** | 2014-02 | FOSDEM 2014 |
| **OpenJDK JVM Internals** | 2012 | JAX Conference |
| **All Power to OpenJDK** | 2012 | JavaOne Conference |
| **How "final" is final?** | 2015 | JET Conference |
| **Class Data Sharing in the HotSpot VM** | 多次 | JeeConf, 其他技术大会 |
| **FireCRaCer: The Best Of Both Worlds** | 2023 | jProfessionals |
| **FOSDEM 2017, 2019, 2023, 2024** | 多年 | FOSDEM Free Java DevRoom |
| **Joker Conference** | 2022, 2023 | Joker (圣彼得堡) |

> **演讲资料**: [progdoc.de/papers](http://www.progdoc.de/papers.htm), [simonis.io/conferences](https://simonis.io/conferences/), [SapMachine Wiki - Presentations](https://github.com/SAP/SapMachine/wiki/Presentations)

---

## 7. 技术专长

### 平台移植

- **处理器架构**: PowerPC, s390x, x86, AArch64
- **操作系统**: AIX, Linux, Windows
- **JIT 编译器移植**: C1/C2 后端适配

### JVM 内部

- **HotSpot Runtime**: JVM 运行时子系统
- **CDS / AppCDS**: 类数据共享技术
- **CRaC**: 检查点/恢复技术

### 社区与生态

- **SapMachine**: OpenJDK 发行版维护
- **Amazon Corretto**: OpenJDK 发行版
- **OpenJDK 治理**: 项目管理和标准制定

---

## 8. 协作网络

| 协作者 | 合作领域 |
|--------|----------|
| [Goetz Lindenmaier](/by-contributor/profiles/goetz-lindenmaier.md) | SAP OpenJDK 团队, PowerPC/AIX 移植 |
| [Thomas Stuefe](/by-contributor/profiles/thomas-stuefe.md) | SAP HotSpot, 诊断和调优 |
| Matthias Baesken | SAP JVM 团队, 构建系统 |
| Steve Poole (IBM) | PowerPC/AIX 移植合作 |
| Martin Doerr (SAP) | PowerPC/s390x 编译器后端 |

---

## 9. 相关链接

### 官方资料
- [GitHub - simonis](https://github.com/simonis)
- [OpenJDK Census - simonis](https://openjdk.org/census#simonis)
- [个人主页 (progdoc.de)](https://progdoc.de/)
- [会议页面 (simonis.io)](https://simonis.io/conferences/)

### OpenJDK 项目
- [OpenJDK PowerPC/AIX Port Project](https://openjdk.org/projects/ppc-aix-port/)
- [OpenJDK s390x Port Project](https://openjdk.org/projects/s390x-port/)
- [JEP 294: Linux/s390x Port](https://openjdk.org/jeps/294)

### 演讲与论文
- [FOSDEM 2013: Power to the People](https://archive.fosdem.org/2013/schedule/event/power_to_the_people/)
- [FOSDEM 2014: PowerPC/AIX Port Endgame](https://progdoc.de/papers/FOSDEM2014/index.html)
- [JavaOne 2012: All Power to OpenJDK](https://progdoc.de/papers/JavaOne2012/javaone2012.html)
- [论文与演讲列表](http://www.progdoc.de/papers.htm)
- [SapMachine Presentations](https://github.com/SAP/SapMachine/wiki/Presentations)

### 其他
- [SapMachine vs OpenJDK 差异](https://github.com/SAP/SapMachine/wiki/Differences-between-SapMachine-and-OpenJDK)
- [OpenJDK Wiki - PowerPC/AIX Port](https://wiki.openjdk.org/display/PPCAIXPort/)
- [OpenJDK 2022 Governing Board Election](https://openjdk.org/poll/gb/2022/)

---

**Sources**:
- [GitHub - simonis](https://github.com/simonis)
- [OpenJDK PowerPC/AIX Port Project](https://openjdk.org/projects/ppc-aix-port/)
- [FOSDEM 2013 Speaker Profile](https://archive.fosdem.org/2013/schedule/speaker/volker_simonis/)
- [FOSDEM 2024 Speaker Profile](https://archive.fosdem.org/2024/schedule/speaker/ZZTDLL/)
- [JeeConf Speaker Profile](https://jeeconf.com/speaker/volker-simonis/)
- [JEP 294: Linux/s390x Port](https://openjdk.org/jeps/294)
- [Crunchbase - Volker Simonis](https://www.crunchbase.com/person/volker-simonis)
- [progdoc.de Papers](http://www.progdoc.de/papers.htm)
