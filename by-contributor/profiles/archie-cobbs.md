# Archie Cobbs

> **GitHub**: [@archiecobbs](https://github.com/archiecobbs)
> **Organization**: 独立贡献者 (Independent Contributor)
> **Role**: JEP 447 Author & Owner, Flexible Constructor Bodies 提案者

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [主要 JEP 贡献](#3-主要-jep-贡献)
4. [核心技术贡献](#4-核心技术贡献)
5. [开源项目](#5-开源项目)
6. [社区活动](#6-社区活动)
7. [技术专长](#7-技术专长)
8. [相关链接](#8-相关链接)

---


## 1. 概述

Archie L. Cobbs 是一位资深的独立 Java 开发者和 OpenJDK 贡献者。他最为人知的贡献是作为 **JEP 447: Statements before super(...)** 的 Author 和 Owner，该提案允许在构造函数中的 `super()` 或 `this()` 调用之前执行语句。该特性经过多轮 Preview (JEP 447 → JEP 482 → JEP 492)，最终以 **JEP 513: Flexible Constructor Bodies** 的名称在 JDK 23 中正式发布。作为 OpenJDK 社区中少数以独立贡献者身份成功推动重要语言特性的开发者之一，他的贡献尤为引人注目。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Archie L. Cobbs |
| **身份** | 独立贡献者 (Independent Contributor) |
| **GitHub** | [@archiecobbs](https://github.com/archiecobbs) (53 followers, 58 repos) |
| **专长** | Java 语言特性, 构造函数语义, 持久化框架, 开源工具 |
| **代表作** | JEP 447 (Statements before super), Permazen, s3backer |

> **数据来源**: [GitHub](https://github.com/archiecobbs), [JEP 447](https://openjdk.org/jeps/447), [JEP 513](https://openjdk.org/jeps/513)

---

## 3. 主要 JEP 贡献

### JEP 447: Statements before super(...) (Preview) - JDK 22

| 属性 | 值 |
|------|-----|
| **角色** | Author & Owner |
| **合作者** | Gavin Bierman (Co-author) |
| **状态** | Preview |
| **发布版本** | JDK 22 |

**影响**: 首次允许在构造函数的 `super()` 或 `this()` 调用之前放置不引用正在构造对象的语句，打破了 Java 自诞生以来的限制。

### JEP 482: Flexible Constructor Bodies (Second Preview) - JDK 23

| 属性 | 值 |
|------|-----|
| **角色** | Co-author |
| **合作者** | Gavin Bierman |
| **状态** | Second Preview |

**影响**: 修订并扩展了原始提案，更名为 "Flexible Constructor Bodies"，进一步放宽了构造函数体中的限制。

### JEP 492: Flexible Constructor Bodies (Third Preview) - JDK 24

| 属性 | 值 |
|------|-----|
| **角色** | Co-author |
| **合作者** | Gavin Bierman |
| **状态** | Third Preview (无变更) |

### JEP 513: Flexible Constructor Bodies (Final) - JDK 25

| 属性 | 值 |
|------|-----|
| **角色** | Co-author |
| **Owner** | Gavin Bierman |
| **Endorsed by** | Brian Goetz |
| **Reviewed by** | Alex Buckley, Brian Goetz |
| **状态** | Final |
| **发布版本** | JDK 25 |

**影响**: 该特性正式成为 Java 语言标准的一部分，允许开发者在构造函数中更灵活地组织代码，简化参数验证和字段初始化。

---

## 4. 核心技术贡献

### 1. Flexible Constructor Bodies

Archie Cobbs 提出并推动了 Java 构造函数语义的重大改进：

**问题**: Java 长期要求 `super()` 或 `this()` 必须是构造函数体中的第一条语句，导致以下常见模式无法直接表达：
- 在调用父类构造函数之前验证参数
- 在调用父类构造函数之前准备参数值
- 在调用父类构造函数之前共享参数验证逻辑

```java
// JEP 513 之前 — 需要变通方案
public class PositiveInteger extends Number {
    public PositiveInteger(int value) {
        super(validate(value));  // 必须使用静态辅助方法
    }
    private static int validate(int value) {
        if (value <= 0) throw new IllegalArgumentException();
        return value;
    }
}

// JEP 513 之后 — 直接在 super() 之前验证
public class PositiveInteger extends Number {
    public PositiveInteger(int value) {
        if (value <= 0)
            throw new IllegalArgumentException("must be positive");
        super(value);
    }
}
```

**关键规则**: 在 `super()` 之前的语句不能引用正在构造的实例 (`this`)，但可以初始化其字段并执行其他安全计算。

### 2. Project Amber 协作

Archie Cobbs 与 Project Amber 团队紧密合作：
- 与 **Gavin Bierman** 共同撰写 JEP 和语言规范
- 参与 **amber-spec-experts** 邮件列表讨论
- 与 **Brian Goetz** 等 Java 语言架构师协调设计决策

---

## 5. 开源项目

### Permazen
- **描述**: 基于有序键值存储的 Java 语言原生持久化层
- **特性**: 类型安全、语言驱动的持久化框架
- **GitHub**: [permazen/permazen](https://github.com/permazen/permazen)

### s3backer
- **描述**: 通过 Amazon S3 的 FUSE/NBD 单文件后端存储
- **用途**: 将 S3 作为块设备使用

### QueryStream
- **描述**: 使用类似 Stream 的 API 构建 JPA Criteria 查询
- **技术**: JPA Criteria API 的流式封装

### 其他项目
- **Dellroad-stuff**: Java 项目通用工具集
- **Java Console Toolkit**: Java 命令行界面工具包
- **JavaBox**: Java 脚本化工具
- **nvt4j**: Java 网络虚拟终端

---

## 6. 社区活动

### 邮件列表

在 OpenJDK 邮件列表中积极参与：
- **amber-spec-experts**: Java 语言规范讨论，参与 Flexible Constructor Bodies 等特性的设计
- **amber-dev**: Project Amber 开发讨论
- 参与了包括 Implicit Classes、String Templates 等其他 JEP 的讨论

### OpenJDK 审查

- 参与 JEP 规范草案的审查和反馈
- 积极回应社区关于构造函数语义的技术讨论

---

## 7. 技术专长

### Java 语言

- **构造函数语义**: 构造函数体、super() 调用、字段初始化
- **语言规范**: JLS (Java Language Specification) 理解和改进
- **Project Amber**: 语言特性演进

### 持久化与数据库

- **Permazen**: 语言原生持久化
- **JPA**: Java Persistence API
- **键值存储**: 有序键值存储抽象

### 系统编程

- **FUSE**: 用户空间文件系统
- **Amazon S3**: 云存储集成
- **NBD**: 网络块设备

---

## 8. 相关链接

### 官方资料
- [GitHub - archiecobbs](https://github.com/archiecobbs)

### JEP 文档
- [JEP 447: Statements before super(...) (Preview)](https://openjdk.org/jeps/447)
- [JEP 482: Flexible Constructor Bodies (Second Preview)](https://openjdk.org/jeps/482)
- [JEP 492: Flexible Constructor Bodies (Third Preview)](https://openjdk.org/jeps/492)
- [JEP 513: Flexible Constructor Bodies](https://openjdk.org/jeps/513)

### 项目
- [Permazen](https://github.com/permazen/permazen)
- [s3backer](https://github.com/archiecobbs/s3backer)
- [QueryStream](https://github.com/archiecobbs/querystream)

---

**Sources**:
- [GitHub - archiecobbs](https://github.com/archiecobbs)
- [JEP 447: Statements before super(...)](https://openjdk.org/jeps/447)
- [JEP 482: Flexible Constructor Bodies (Second Preview)](https://openjdk.org/jeps/482)
- [JEP 492: Flexible Constructor Bodies (Third Preview)](https://openjdk.org/jeps/492)
- [JEP 513: Flexible Constructor Bodies](https://openjdk.org/jeps/513)
- [Permazen Wiki](https://github.com/permazen/permazen/wiki)
- [amber-spec-experts Mailing List](https://www.mail-archive.com/amber-spec-experts@openjdk.org/)

## 角色晋升 (CFV)

| 日期 | 角色 | 提名者 | 投票数 | 链接 |
|------|------|--------|--------|------|
| 2024-06-26 | Committer | Vicente Romero | 14 | [CFV](https://mail.openjdk.org/pipermail/jdk-dev/2024-June/009168.html) |


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 76 |
| **活跃仓库数** | 1 |
