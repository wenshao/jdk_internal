# Tobias Hartmann

> **GitHub**: [@thartmann](https://github.com/thartmann)
> **OpenJDK**: [@thartmann](https://openjdk.org/census#thartmann)
> **Organization**: Oracle (Java Platform Group)
> **Role**: Software Development Manager, HotSpot Compiler Engineer

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [职业经历](#3-职业经历)
4. [主要贡献](#4-主要贡献)
5. [学术研究](#5-学术研究)
6. [会议演讲](#6-会议演讲)
7. [技术专长](#7-技术专长)
8. [相关链接](#8-相关链接)

---


## 1. 概述

Tobias Hartmann 是 Oracle 的 **软件开发经理** 和 **编译器工程师**，在 **Java HotSpot VM Compiler Team** 工作。他对 Java 执行栈有深入理解，从底层编程和调试到 JVM 优化，是 OpenJDK 编译器领域的关键贡献者。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Tobias Hartmann |
| **当前组织** | Oracle (Java Platform Group) |
| **职位** | Software Development Manager, Compiler Engineer |
| **GitHub** | [@thartmann](https://github.com/thartmann) |
| **OpenJDK** | [@thartmann](https://openjdk.org/census#thartmann) |
| **邮件** | tobias.hartmann@oracle.com, thartmann@openjdk.org |
| **专长** | HotSpot Compiler, JIT Compilation, Code Cache, Profile-guided Optimization |
| **位置** | 瑞士 Baden (Rheinfelden) |
| **教育** | ETH Zürich 硕士 |

---

## 3. 职业经历

### Oracle (2013-至今)

- **职位**: Software Development Manager, Compiler Engineer
- **部门**: Java Platform Group, HotSpot Compiler Team
- **成为 JDK Committer**: 2014年7月 (JDK 9)
- **OpenJDK Members Group**: 2022年入选

### 教育背景

- **MSc**: ETH Zürich (瑞士联邦理工学院)
- **研究方向**: 编译器技术

---

## 4. 主要贡献

### 1. 分段代码缓存

- **首个贡献**: 分段代码缓存 (segmented code cache) 管理
- 改善了 HotSpot 的代码缓存效率

### 2. IR 框架

- **JDK-8254129**: 引入 IR (Intermediate Representation) 测试框架
- 支持在 JTreg 编译器测试中使用正则表达式匹配 IR

### 3. ZGC 相关工作

虽然主要专长是编译器技术，但也参与了 ZGC (Z Garbage Collector) 相关工作：
- 审查 ZGC 补丁
- 与 GC 团队协作

### 4. 重要 Bug 修复

- **JDK-8295210**: IR framework 不应白名单 -XX:-UseTLAB
- **JDK-8236136**: 使用 CompilationMode 的测试修复
- 多个编译器稳定性改进

---

## 5. 学术研究

### 发表论文

1. **"Efficient code management for dynamic multi-tiered compilation systems"** (ACM, 2014)
   - 硕士论文工作
   - ETH Zürich

2. **"Integrating Profile Caching into the HotSpot Multi-Tier Compilation System"**
   - 合作者: Zoltán Majó, Marcel Mohler, Thomas R. Gross

3. **"Exploring Impact of Profile Data on Code Quality in the HotSpot JVM"** (ACM, 2020)

### 引用统计

- Google Scholar: **85+ 引用**

---

## 6. 会议演讲

Tobias 在多个会议和大学发表技术演讲：

- **"The Java HotSpot VM Under the Hood"** (ETH Zürich, 2016-2020)
- **"Debugging the Java HotSpot VM"** (2020)
- ETH Zürich 编译器设计客座讲座

---

## 7. 技术专长

### Java 执行栈

从底层到高层的完整理解：
- **底层编程**: 多架构编程和调试
- **JIT 编译**: C1/C2 编译器
- **代码缓存**: 分段代码缓存管理
- **性能分析**: Profile-guided optimization

### HotSpot 编译器

- **分层编译**: C1 (Client) 和 C2 (Server) 编译器协作
- **代码生成**: 多架构后端
- **优化技术**: 方法内联、循环优化等

---

## 8. 相关链接

### 官方资料
- [LinkedIn Profile](https://ch.linkedin.com/in/tobihartmann)
- [OpenJDK Census - thartmann](https://openjdk.org/census#thartmann)

### 邮件列表
- [CFV: New JDK 9 Committer: Tobias Hartmann](https://mail.openjdk.org/pipermail/jdk9-dev/2014-July/001077.html)
- [JDK8u Committer Announcement](https://mail.openjdk.org/pipermail/jdk8u-dev/2014-October/000834.html)

### 论文
- [Efficient code management for dynamic multi-tiered compilation systems (ACM)](https://dl.acm.org/doi/10.1145/2684907)
- [Integrating Profile Caching into HotSpot](https://dl.acm.org/doi/10.1145/3546918.3546925)

---

**Sources**:
- [LinkedIn - Tobias Hartmann](https://ch.linkedin.com/in/tobihartmann)
- [OpenJDK Census - thartmann](https://openjdk.org/census#thartmann)
- [CFV: New JDK 9 Committer](https://mail.openjdk.org/pipermail/jdk9-dev/2014-July/001077.html)
- [ACM Paper - Efficient code management](https://dl.acm.org/doi/10.1145/2684907)
