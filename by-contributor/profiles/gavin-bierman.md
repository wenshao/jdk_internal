# Gavin Bierman

> **Inside.java**: [GavinBierman](https://inside.java/u/GavinBierman/)
> **Organization**: Oracle (Java Platform Group) / Oracle Labs UK
> **Role**: Consulting Member of Technical Staff, Language Designer, Editor of the Java Language Specification

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [主要 JEP 贡献](#3-主要-jep-贡献)
4. [核心技术贡献](#4-核心技术贡献)
5. [研究背景](#5-研究背景)
6. [合作关系](#6-合作关系)
7. [相关链接](#7-相关链接)

---


## 1. 概述

Gavin Bierman 是 Oracle Java Platform Group 和 Oracle Labs UK 编程语言研究组的 **咨询技术 staff**。他是 **Java Language Specification (JLS) 的当前编辑**，也是 **Java 语言设计** 的关键贡献者，主导了 Pattern Matching、Records 和多个简化 Java 源代码的 JEP。在加入 Oracle 之前，他在 **Microsoft Research Cambridge** 担任高级研究员 (2004-2014)，更早之前是 **Cambridge 大学** 的讲师。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Gavin Bierman |
| **当前组织** | Oracle (Java Platform Group) / Oracle Labs UK |
| **职位** | Consulting Member of Technical Staff |
| **部门** | Programming Language Research Group |
| **位置** | Cambridge, UK |
| **GitHub** | [@GavinBierman](https://github.com/GavinBierman) |
| **LinkedIn** | [gavin-bierman](https://www.linkedin.com/in/gavin-bierman-a0173075/) |
| **教育** | PhD, University of Cambridge; BSc, Imperial College London |
| **前雇主** | Microsoft Research Cambridge (Senior Researcher, 2004-2014) |
| **更早经历** | Lecturer, University of Cambridge Computer Laboratory; Fellow & Director of Studies, St John's College, Cambridge |
| **专长** | Java Language Specification (JLS) Editor, Programming Language Theory, Java Language Design, Pattern Matching |

> **数据来源**: [Oracle Labs Bio](https://labs.oracle.com/pls/apex/f?p=labs:bio:0:2044), [GitHub](https://github.com/GavinBierman), [LinkedIn](https://www.linkedin.com/in/gavin-bierman-a0173075/), [Personal Page](https://gavinbierman.github.io/)

---

## 3. 主要 JEP 贡献

### JEP 440: Record Patterns

| 属性 | 值 |
|------|-----|
| **角色** | Author |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 21 |

**影响**: Record patterns 和 type patterns 可以嵌套，实现强大的数据导航和处理。

### JEP 432: Record Patterns (Second Preview)

| 属性 | 值 |
|------|-----|
| **角色** | Author |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 20 (Second Preview) |

### JEP 305: Pattern Matching for instanceof

| 属性 | 值 |
|------|-----|
| **角色** | Owner |
| **作者** | Brian Goetz |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 14 (Preview) → JDK 16 (Final) |

### JEP 441: Pattern Matching for switch

| 属性 | 值 |
|------|-----|
| **角色** | Author |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 21 |

### JEP 468: Derived Record Creation (Preview)

| 属性 | 值 |
|------|-----|
| **角色** | Author & Owner |
| **合作者** | Brian Goetz |
| **状态** | Preview |
| **发布版本** | JDK 24 |

**影响**: Derived creation 简化代码，通过仅指定不同组件从现有 record 派生新 record。

### JEP 513: Flexible Constructor Bodies

| 属性 | 值 |
|------|-----|
| **角色** | Author & Owner |
| **合作者** | Archie Cobbs |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 25 |

### JEP 512: Compact Source Files and Instance Main Methods

| 属性 | 值 |
|------|-----|
| **角色** | Author & Owner |
| **合作者** | Ron Pressler, Jim Laskey |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 25 |

### JEP 494: Module Import Declarations (Second Preview)

| 属性 | 值 |
|------|-----|
| **角色** | Author & Owner |
| **合作者** | Jim Laskey |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 23 |

### JEP 477: Implicitly Declared Classes and Instance Main Methods

| 属性 | 值 |
|------|-----|
| **角色** | Author |
| **合作者** | Ron Pressler 等 |
| **状态** | Closed / Delivered |
| **发布版本** | JDK 23 (Third Preview) |

---

## 4. 核心技术贡献

### 1. Pattern Matching

Gavin Bierman 是 Java Pattern Matching 特性的主要设计者：

```java
// instanceof pattern matching
if (obj instanceof String s && s.length() > 0) {
    System.out.println(s);
}

// switch pattern matching
String formatted = switch (obj) {
    case Integer i -> String.format("int %d", i);
    case Long l    -> String.format("long %d", l);
    case String s  -> s;
    default        -> "unknown";
};

// record patterns
record Point(int x, int y) {}
if (obj instanceof Point(int x, int y)) {
    System.out.println("x=" + x + ", y=" + y);
}
```

### 2. Records 和 Derived Creation

```java
// Derived record creation
record Point(int x, int y) {}
Point p = new Point(1, 2);
Point p2 = new Point(p, x = 3); // y=2, x=3
```

### 3. 简化 Java 源代码

Gavin Bierman 领导了多个旨在简化 Java 源代码的 JEP：
- **隐式声明类**: 无需 `public class` 包装
- **实例 main 方法**: 无需 `static` 关键字
- **紧凑源文件**: 单文件程序更简洁

```java
// 简化前
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello!");
    }
}

// 简化后
void main() {
    System.out.println("Hello!");
}
```

---

## 5. 研究背景

Gavin Bierman 拥有深厚的编程语言理论背景：
- **PhD**: University of Cambridge
- **BSc**: Imperial College London
- **Cambridge 大学讲师**: Computer Laboratory 讲师，St John's College Fellow & Director of Studies
- **Microsoft Research Cambridge**: 高级研究员 (2004-2014)，发表了关于 Java, C#, TypeScript, 数据库, 类型系统, 操作语义等方面的论文
- **Oracle (2014-至今)**: Java Platform Group，Programming Language Research Group 成员
- **JLS 编辑**: 当前 Java Language Specification 的编辑

---

## 6. 合作关系

与以下 Java 语言设计专家密切合作：
- **Brian Goetz**: Java 语言架构师
- **Ron Pressler**: Project Leyden 负责人
- **Jim Laskey**: Java 语言特性贡献者
- **Archie Cobbs**: Java 特性贡献者

---

## 7. 相关链接

### 官方资料
- [Inside.java - GavinBierman](https://inside.java/u/GavinBierman/)
- [Oracle Labs - Gavin Bierman](https://labs.oracle.com/pls/apex/f?p=labs:bio:0:2044)
- [Personal Page](https://gavinbierman.github.io/)
- [LinkedIn](https://www.linkedin.com/in/gavin-bierman-a0173075/)

### Podcast
- [Episode 17 "Pattern Matching for switch" with Gavin Bierman](https://inside.java/2021/06/13/podcast-017/)

### JEP 文档
- [JEP 305: Pattern Matching for instanceof](https://openjdk.org/jeps/305)
- [JEP 440: Record Patterns](https://openjdk.org/jeps/440)
- [JEP 441: Pattern Matching for switch](https://openjdk.org/jeps/441)
- [JEP 468: Derived Record Creation](https://openjdk.org/jeps/468)
- [JEP 512: Compact Source Files](https://openjdk.org/jeps/512)
- [JEP 513: Flexible Constructor Bodies](https://openjdk.org/jeps/513)

---

**Sources**:
- [Inside.java - GavinBierman](https://inside.java/u/GavinBierman/)
- [Oracle Labs - Gavin Bierman](https://labs.oracle.com/pls/apex/f?p=labs:bio:0:2044)
- [JEP 440: Record Patterns](https://openjdk.org/jeps/440)
- [JEP 441: Pattern Matching for switch](https://openjdk.org/jeps/441)
- [JEP 468: Derived Record Creation](https://openjdk.org/jeps/468)
- [JEP 512: Compact Source Files](https://openjdk.org/jeps/512)
