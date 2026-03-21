# Maurizio Cimadamore

> **GitHub**: [@mcimadamore](https://github.com/mcimadamore)
> **Inside.java**: [mcimadamore](https://inside.java/u/mcimadamore/)
> **Organization**: Oracle (Java Platform Group)
> **Role**: Java Compiler Architect, Project Panama Lead

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [主要 JEP 贡献](#3-主要-jep-贡献)
4. [核心技术贡献](#4-核心技术贡献)
5. [职业经历](#5-职业经历)
6. [社区活动](#6-社区活动)
7. [技术专长](#7-技术专长)
8. [相关链接](#8-相关链接)

---


## 1. 概述

Maurizio Cimadamore 是 Oracle 的 **Java 编译器架构师** 和 **Project Panama 的技术负责人**。他是 Java 编译器 (javac) 的关键贡献者，主导了 Lambda 表达式在 javac 中的实现，并正在领导 Project Panama，重新定义 Java 与本地代码和内存的互操作。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Maurizio Cimadamore |
| **当前组织** | Oracle (Java Platform Group) |
| **职位** | Java Compiler Architect, Project Panama Lead |
| **GitHub** | [@mcimadamore](https://github.com/mcimadamore) |
| **LinkedIn** | [mcimadamore](https://ie.linkedin.com/in/mcimadamore) |
| **教育** | University of Bologna |
| **专长** | javac Compiler, Lambda Expressions, Project Panama, Foreign Function & Memory API |
| **职业经历** | Sun Microsystems → Oracle |

> **数据来源**: [LinkedIn](https://ie.linkedin.com/in/mcimadamore), [nipafx.dev Interview](https://nipafx.dev/maurizio-cimadamore-26h/)

---

## 3. 主要 JEP 贡献

### Project Panama 系列

#### JEP 454: Foreign Function & Memory API (Final)

| 属性 | 值 |
|------|-----|
| **角色** | Lead |
| **状态** | Final |
| **发布版本** | JDK 22 |

**影响**: FFM API 正式发布，提供高效的 Java 与本地代码互操作。

#### JEP 444: Virtual Threads

| 属性 | 值 |
|------|-----|
| **角色** | Contributor |
| **状态** | Final |
| **发布版本** | JDK 21 |

#### JEP 412: Foreign Function & Memory API (Third Preview)

#### JEP 424: Foreign Function & Memory API (Second Preview)

#### JEP 394: Pattern Matching for instanceof

| 属性 | 值 |
|------|-----|
| **角色** | Contributor |
| **状态** | Final |
| **发布版本** | JDK 16 |

#### JEP 389: Foreign Linker API (Incubator)

#### JEP 383: Foreign Memory Access API (Second Incubator)

#### JEP 370: Foreign Memory Access API (Incubator)

#### JEP 217: Annotations Pipeline (JDK 9)

| 属性 | 值 |
|------|-----|
| **角色** | Contributor |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 9 |

**影响**: 重新设计 javac 注解处理管道。

### JEP 531: Lazy Constants (Preview)

| 属性 | 值 |
|------|-----|
| **角色** | Co-author |
| **合作者** | Per Minborg |
| **状态** | Preview |
| **发布版本** | JDK 26 |

### JEP 471: Deprecating memory-access methods in sun.misc.Unsafe

| 属性 | 值 |
|------|-----|
| **角色** | Contributor |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 22 |

---

## 4. 核心技术贡献

### 1. Lambda 表达式实现

Maurizio Cimadamore 在 **Project Lambda** 中发挥了关键作用：
- 设计和实现了 javac 中的 Lambda 表达式
- 从最早阶段开始参与 Lambda 表达式开发
- 被称为 Project Lambda 的 "英雄" 贡献者

### 2. Project Panama 领导

作为 Project Panama 的技术负责人：
- **Foreign Function & Memory (FFM) API**: Java 与本地代码互操作
- **目标**: 替代 JNI (Java Native Interface)
- **使命**: 重新构想 Java 应用与本地函数和数据结构的通信方式

```java
// FFM API 示例
import java.lang.foreign.*;
import java.lang.invoke.*;

Linker linker = Linker.nativeLinker();
SymbolLookup stdlib = linker.defaultLookup();

MemorySession session = MemorySession.auto();
Linker.Option[] options = {};

MethodHandle strlen = linker.downcallHandle(
    stdlib.find("strlen").get(),
    FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
);

try (Arena arena = Arena.ofConfined()) {
    MemorySegment cString = arena.allocateFrom("Hello");
    long len = (long) strlen.invoke(cString);
}
```

### 3. javac 编译器架构

- **Lambda 表达式**: 编译器实现
- **注解管道**: JEP 217 重新设计
- **类型推断**: 改进编译器类型推断

### 4. Pattern Matching

- instanceof 模式匹配的编译器实现
- 类型模式支持

---

## 5. 职业经历

### Sun Microsystems → Oracle

早期职业生涯在 Sun Microsystems，后来随 Sun 被收购加入 Oracle。

### Oracle (当前)

继续领导 Project Panama 和 Java 编译器开发。

---

## 6. 社区活动

### 邮件列表

在 OpenJDK 邮件列表中活跃：
- **compiler-dev**: 编译器开发讨论
- **lambda-dev**: Lambda 表达式讨论 (历史)

### Inside.java Podcast

- **Episode 9** (2020-12-11): "Project Panama - The Foreign Memory Access API"
  - 与 David Delabassee 讨论 Project Panama
  - 与 Jorn Vernee 一起介绍 FFM API

### 会议演讲

定期在 Java 会议发表关于编译器和 Project Panama 的演讲。

---

## 7. 技术专长

### 编译器技术

- **javac**: Java 编译器架构
- **Lambda 表达式**: 编译器实现
- **类型系统**: Java 类型推断

### 本地互操作

- **JNI**: 传统 Java Native Interface
- **FFM API**: 新一代互操作 API
- **Foreign Memory**: 访问本地内存

---

## 8. 相关链接

### 官方资料
- [Inside.java - mcimadamore](https://inside.java/u/mcimadamore/)
- [GitHub Profile](https://github.com/mcimadamore)
- [Oracle Labs - Maurizio Cimadamore](https://www.getprog.ai/profile/54672762)

### JEP 文档
- [JEP 454: Foreign Function & Memory API](https://openjdk.org/jeps/454)
- [JEP 424: FFM API (Second Preview)](https://openjdk.org/jeps/424)
- [JEP 394: Pattern Matching for instanceof](https://openjdk.org/jeps/394)
- [JEP 217: Annotations Pipeline](https://openjdk.org/jeps/217)

### 媒体
- [Inside Java Podcast Episode 9: Project Panama](https://inside.java/2020/12/11/podcast-009/)

---

**Sources**:
- [Inside.java - mcimadamore](https://inside.java/u/mcimadamore/)
- [GitHub - mcimadamore](https://github.com/mcimadamore)
- [Inside Java Podcast Episode 9](https://inside.java/2020/12/11/podcast-009/)
- [JEP 454: FFM API](https://openjdk.org/jeps/454)
- [JEP 394: Pattern Matching](https://openjdk.org/jeps/394)
- [Project Lambda PDF](https://jcp.org/aboutJava/communityprocess/ec-public/materials/2011-01-1112/2011-01_JCP_EC_ProjectLambda.pdf)
