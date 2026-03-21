# Jesper Wilhelmsson

> **GitHub**: [@JesperIRL](https://github.com/JesperIRL)
> **Inside.java**: [JesperWilhelmsson](https://inside.java/u/JesperWilhelmsson/)
> **Organization**: Oracle (Java Platform Group)
> **Role**: Software Development Manager, JDK GateKeeper, OpenJDK Developers' Guide Project Lead
> **Website**: [fantasi.se](http://www.fantasi.se)

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [核心技术贡献](#3-核心技术贡献)
4. [职业经历](#4-职业经历)
5. [社区活动](#5-社区活动)
6. [技术专长](#6-技术专长)
7. [相关链接](#7-相关链接)

---


## 1. 概述

Jesper Wilhelmsson 是 Oracle Java Platform Group 的 **Software Development Manager**，担任 **JDK GateKeeper** 和 **OpenJDK Developers' Guide 项目负责人**。他拥有 Uppsala University 的博士研究背景，专攻虚拟机内存管理和垃圾回收算法。他设计了 **Mark and Split** 垃圾回收算法并在 JRockit JVM 中实现。如今，他的工作重心在 JDK 全局流程管理、JVM 安全性和 JDK 代码入库把关方面，致力于简化和统一 OpenJDK 社区的开发流程。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Jesper Wilhelmsson |
| **当前组织** | Oracle (Java Platform Group) |
| **职位** | Software Development Manager |
| **位置** | Uppsala, Sweden |
| **GitHub** | [@JesperIRL](https://github.com/JesperIRL) (23 followers) |
| **OpenJDK** | [@jwilhelm](https://openjdk.org/census#jwilhelm) |
| **Inside.java** | [JesperWilhelmsson](https://inside.java/u/JesperWilhelmsson/) |
| **Website** | [fantasi.se](http://www.fantasi.se) |
| **教育** | Uppsala University (博士研究, 内存管理与垃圾回收) |
| **专长** | JDK GateKeeping, 开发流程管理, GC 算法, JVM 安全, HotSpot Engineering |

> **数据来源**: [GitHub](https://github.com/JesperIRL), [Inside.java](https://inside.java/u/JesperWilhelmsson/), [PLDI 2020](https://pldi20.sigplan.org/profile/jesperwilhelmsson)

---

## 3. 核心技术贡献

### 1. JDK GateKeeper

Jesper Wilhelmsson 担任 JDK GateKeeper，负责 JDK 代码库的入库质量控制：
- **代码入库审核**: 确保提交到 JDK 主线的变更满足质量标准
- **构建稳定性**: 监控和维护 JDK 构建系统的稳定性
- **前向移植 (Forwardport)**: 协调跨版本的代码合并，例如 JDK 18 → JDK 19 的合并
- **流程把关**: 确保所有变更遵循 OpenJDK 开发流程

### 2. OpenJDK Developers' Guide

作为 OpenJDK Developers' Guide 项目的负责人：
- **项目创建**: 将贡献指南升级为 OpenJDK 内的正式项目
- **文档现代化**: 将 Developers' Guide 更新至符合当前 OpenJDK 开发实践
- **流程简化**: 简化、澄清和统一 OpenJDK 社区的开发流程
- **GitHub 仓库**: [openjdk/guide](https://github.com/openjdk/guide)

### 3. HotSpot Engineering Process

- 在 OpenJDK Wiki 上编写了 HotSpot 工程流程文档
- 定义了 HotSpot JVM 开发的规范和最佳实践
- 帮助标准化 JVM 开发团队的工作流程

### 4. JDK 全局流程管理

Jesper Wilhelmsson 负责 JDK 开发的全局流程管理：
- **跨团队协调**: 在 Oracle 内部和 OpenJDK 社区之间协调开发流程
- **发布流程**: 参与 JDK 发布周期管理
- **JVM 安全性**: JVM 安全相关事务管理

### 5. Mark and Split 垃圾回收算法

Jesper Wilhelmsson 在学术研究阶段设计了 Mark and Split 算法：
- **算法特性**: 非移动式垃圾回收算法，在标记阶段通过维护和分割空闲区间来构建空闲列表
- **创新点**: 消除了传统 mark-sweep 算法的清扫阶段
- **性能优势**: 回收成本与存活数据集大小成正比，而非堆大小
- **实现**: 在 JRockit JVM 中实现

---

## 4. 职业经历

### Uppsala University (学术研究)

- **HiPE 团队**: 参与 High-Performance Erlang 编译器团队
- **Erlang VM**: 实验不同的内存模型
- **垃圾回收**: 设计 Mark and Split 算法
- **跨语言研究**: 将 GC 研究成果从 Erlang VM 应用到 JVM

### Oracle (当前)

- **GC 团队负责人**: 曾担任 Oracle JVM 垃圾回收团队负责人
- **JRockit & HotSpot**: 协调两个 JVM 的 GC 开发
- **Software Development Manager**: 当前职位，负责 JDK 流程管理
- **JDK GateKeeper**: JDK 代码入库质量把关
- **Developers' Guide Lead**: OpenJDK 开发者指南项目负责人

---

## 5. 社区活动

### Inside Java Podcast

- **Episode 11** (2021-01-29): "How to contribute to OpenJDK" — 与 Stuart Marks 一起介绍如何参与 OpenJDK 贡献，讨论开发流程和最佳实践

### 学术会议

- **PLDI 2020**: Programming Language Design and Implementation 会议参与者
- **Erlang User Conference 2012**: "I have the solution, now I only need to find the problem" — 讨论垃圾回收算法研究
- **学术合作**: Oracle、Uppsala University 和 KTH 的联合 JVM 研究项目

### 邮件列表

- **jdk-dev**: JDK 开发流程讨论
- **jdk-updates-dev**: JDK 更新版本维护讨论
- **hotspot-dev**: HotSpot JVM 开发

---

## 6. 技术专长

### 开发流程管理

- **JDK GateKeeping**: 代码入库审核和质量控制
- **发布管理**: JDK 发布周期和版本管理
- **流程文档**: OpenJDK Developers' Guide 维护
- **前向移植**: 跨版本代码合并协调

### 垃圾回收

- **Mark and Split**: 非移动式 GC 算法设计者
- **JRockit GC**: JRockit JVM 垃圾回收开发
- **HotSpot GC**: HotSpot JVM 垃圾回收协调
- **内存管理**: 虚拟机内存管理研究

### JVM 安全

- **JVM 安全性**: JVM 安全事务管理
- **安全审查**: 安全相关变更审核

---

## 7. 相关链接

### 官方资料
- [Inside.java - JesperWilhelmsson](https://inside.java/u/JesperWilhelmsson/)
- [GitHub - JesperIRL](https://github.com/JesperIRL)
- [OpenJDK Wiki - jwilhelm](https://wiki.openjdk.org/display/~jwilhelm)
- [PLDI 2020 Profile](https://pldi20.sigplan.org/profile/jesperwilhelmsson)
- [Personal Website](http://www.fantasi.se)

### OpenJDK 项目
- [OpenJDK Developers' Guide](https://openjdk.org/guide/)
- [openjdk/guide (GitHub)](https://github.com/openjdk/guide)
- [JDK Updates Project](https://openjdk.org/projects/jdk-updates/)

### Podcast & 演讲
- [Inside Java Podcast Episode 11: How to contribute to OpenJDK](https://inside.java/2021/01/29/podcast-011/)
- [Erlang User Conference 2012](https://www.erlang-factory.com/conference/ErlangUserConference2012/speakers/JesperWilhelmsson)

### 学术资料
- [Oracle, Uppsala University, and KTH Joint Research](https://inside.java/2020/06/12/joint-research-projects/)
- [Mark and Split (DeepDyve)](https://www.deepdyve.com/lp/association-for-computing-machinery/mark-and-split-jfBa4Ba0y0)

---

**Sources**:
- [Inside.java - JesperWilhelmsson](https://inside.java/u/JesperWilhelmsson/)
- [GitHub - JesperIRL](https://github.com/JesperIRL)
- [OpenJDK Wiki - jwilhelm](https://wiki.openjdk.org/display/~jwilhelm)
- [PLDI 2020 Profile](https://pldi20.sigplan.org/profile/jesperwilhelmsson)
- [Inside Java Podcast Episode 11](https://inside.java/2021/01/29/podcast-011/)
- [Erlang Factory 2012](https://www.erlang-factory.com/conference/ErlangUserConference2012/speakers/JesperWilhelmsson)
- [InfoQ: Return of the OpenJDK Developers' Guide](https://www.infoq.com/news/2020/07/openjdk-dev-guide/)
- [Mark and Split Algorithm](https://www.deepdyve.com/lp/association-for-computing-machinery/mark-and-split-jfBa4Ba0y0)
