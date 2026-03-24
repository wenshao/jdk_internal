# David Holmes

> **JVM 运行时专家，《Java Concurrency in Practice》共同作者，JSR-166 规范贡献者**

---
## 目录

1. [基本信息](#1-基本信息)
2. [职业背景](#2-职业背景)
3. [技术影响力](#3-技术影响力)
4. [代表性工作](#4-代表性工作)
5. [PR 列表](#5-pr-列表)
6. [演讲与著作](#6-演讲与著作)
7. [相关链接](#7-相关链接)

---


## 1. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | David Holmes |
| **当前组织** | [Oracle](../../contributors/orgs/oracle.md) |
| **位置** | Brisbane, Australia (UTC+10) |
| **GitHub** | [@dholmes-ora](https://github.com/dholmes-ora) |
| **OpenJDK** | [@dholmes](https://openjdk.org/census#dholmes) |
| **角色** | JDK Reviewer |
| **PRs** | 720+ (累计) |
| **JDK 26 Commits** | 50 (排名 #18) |
| **主要领域** | 并发, 线程管理, JVM Runtime, JVMTI, JNI |
| **规范贡献** | JSR-166 (Concurrency Utilities) |
| **著作** | 《Java Concurrency in Practice》(共同作者), 《The Java Programming Language》(共同作者) |
| **活跃时间** | 2000 - 至今 |

> **数据来源**: [OpenJDK Census](https://openjdk.org/census#dholmes), [GitHub](https://github.com/dholmes-ora), [Amazon Author](https://www.amazon.com/Java-Concurrency-Practice-Brian-Goetz/dp/0321349601)

---

## 2. 职业背景

David Holmes 是 JVM 运行时和并发领域的资深专家，Director of DLTeCH Pty Ltd (Brisbane, Australia)，自 2000 年代初就参与 Java 平台开发。他是 JSR-166 专家组成员，也是 Real-Time Specification for Java (RTSJ) 的贡献者。他专注于：

- **线程管理**: Java 线程实现、调度
- **同步机制**: synchronized, volatile 实现
- **JVM Runtime**: 启动、初始化、信号处理
- **规范贡献**: JSR-166 并发工具

### 著作

| 书名 | 共同作者 | 出版年 |
|------|----------|--------|
| **Java Concurrency in Practice** | Brian Goetz, Tim Peierls, Joshua Bloch, Joseph Bowbeer, Doug Lea | 2006 |
| **The Java Programming Language** (4th Ed) | Ken Arnold, James Gosling | 2005 |

### 职业时间线

| 时间 | 事件 | 详情 |
|------|------|------|
| **2000+** | Java Contributor | 参与 JSR-166 规范; RTSJ 贡献者 |
| **2005** | 《The Java Programming Language》 | 与 Ken Arnold, James Gosling 共同著作 (第4版) |
| **2006** | 《Java Concurrency in Practice》 | 与 Brian Goetz, Doug Lea 等共同著作 |
| **2010+** | Oracle HotSpot | JVM Runtime 开发 |
| **JDK 26** | 50 commits | 并发领域排名第 1 |

---

## 3. 技术影响力

| 指标 | 值 |
|------|-----|
| **累计 PRs** | 720+ |
| **JDK 26 Commits** | 50 |
| **排名** | #18 (JDK 26) |
| **主要贡献** | 并发, 线程, JVM Runtime |

### 影响的主要领域

| 领域 | 贡献数 | 说明 |
|------|--------|------|
| 并发/线程 | 200+ | 线程实现, 同步机制 |
| JVM Runtime | 150+ | 启动, 初始化 |
| JNI/JVMTI | 100+ | 原生接口 |

---

## 4. 代表性工作

### 1. 线程管理
- ThreadsListHandle 实现
- 线程安全改进
- Virtual Thread 支持

### 2. Valhalla 项目贡献
**JNI 相关 Issues**:
- 8379365: JNI IsValueObject 新增
- 8379333: JNI NewWeakGlobalRef IdentityException
- 8379012: JNI MonitorEnter 异常消息
- 8378609: JNI AllocObject/NewObject 恢复

### 3. 信号处理
- POSIX 信号处理安全
- 信号处理器实现

### 4. JVM 启动
- 启动流程优化
- 参数解析改进

---

## 5. PR 列表

### JDK 26 Top PRs

| Issue | 标题 | 描述 |
|-------|------|------|
| 8361912 | ThreadsListHandle fix | 线程列表处理修复 |
| 8367035 | ExecuteWithLog backout | 日志执行保护 |

### Valhalla 相关 PRs

| Issue | 标题 | 描述 |
|-------|------|------|
| 8379365 | JNI IsValueObject | 新增 JNI 方法 |
| 8379333 | NewWeakGlobalRef REDO | JNI 弱引用修复 |
| 8379012 | MonitorEnter exception | 监视器异常消息 |
| 8378609 | AllocObject/NewObject | JNI 对象分配恢复 |

---

## 6. 演讲与著作

### 著作

- **《Java Concurrency in Practice》** (Addison-Wesley, 2006) - 与 Brian Goetz, Tim Peierls, Joshua Bloch, Joseph Bowbeer, Doug Lea 共同著作。Java 并发编程领域的经典参考书。
- **《The Java Programming Language》** (4th Edition, Addison-Wesley, 2005) - 与 Ken Arnold, James Gosling 共同著作。

### JavaOne 演讲

| 年份 | 主题 |
|------|------|
| 2019 | Java Concurrency |

### JVM Language Summit

| 年份 | 主题 |
|------|------|
| 多届 | 并发编程, JVM Runtime |

---

## 7. 相关链接

| 类型 | 链接 |
|------|------|
| **GitHub** | [@dholmes-ora](https://github.com/dholmes-ora) |
| **OpenJDK Census** | [dholmes](https://openjdk.org/census#dholmes) |
| **JBS Issues** | [dholmes](https://bugs.openjdk.org/issues/?jql=assignee%20%3D%20dholmes) |
| **著作** | [Java Concurrency in Practice](https://www.amazon.com/Java-Concurrency-Practice-Brian-Goetz/dp/0321349601), [The Java Programming Language](https://www.amazon.com/Java-Programming-Language-4th/dp/0321349806) |
| **协作者** | Coleen Phillimore, Kim Barrett, Andrew Dinn |

---

> **文档版本**: 2.0
> **最后更新**: 2026-03-22
> **更新内容**: 修正位置 (Brisbane, Australia, 非 USA)、添加 GitHub (@dholmes-ora)、添加著作 (Java Concurrency in Practice, The Java Programming Language)、添加 DLTeCH Pty Ltd 背景、添加 RTSJ 贡献


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 2533 |
| **活跃仓库数** | 5 |
