# JDK 25 发布说明

> **版本类型**: LTS (长期支持) | **发布日期**: 2025-09-16 | **支持截止**: 2032+

[![OpenJDK](https://img.shields.io/badge/OpenJDK-25-orange)](https://openjdk.org/projects/jdk/25/)
[![License](https://img.shields.io/badge/License-GPLv2--with--Classpath--Exception-blue)](https://openjdk.org/projects/jdk/25/)

---
## 目录

1. [概述](#1-概述)
2. [语言特性](#2-语言特性)
3. [核心库](#3-核心库)
4. [并发与多线程](#4-并发与多线程)
5. [性能与监控](#5-性能与监控)
6. [安全](#6-安全)
7. [移除与清理](#7-移除与清理)
8. [JEP 汇总](#8-jep-汇总)
9. [相比 JDK 21 的变化](#9-相比-jdk-21-的变化)
10. [升级建议](#10-升级建议)
11. [相关链接](#11-相关链接)

---


## 1. 概述

JDK 25 是继 JDK 21 之后的下一个 LTS 版本，包含大量语言增强、性能优化和 API 改进。

---

## 2. 语言特性

### JEP 455: Primitive Types in Patterns (第三次预览)

**状态**: 第三次预览
**概述**: 允许在模式匹配中使用原始类型。

```java
switch (value) {
    case int i -> System.out.println("int: " + i);
    case long l -> System.out.println("long: " + l);
    case double d -> System.out.println("double: " + d);
    default -> System.out.println("unknown");
}
```

---

### JEP 513: Flexible Constructor Bodies (正式版)

**状态**: 正式发布
**概述**: 允许在构造函数中更灵活地初始化字段。

```java
class Person {
    final String name;
    final int age;

    Person(String name, int age) {
        // 可以在 super() 之前执行逻辑
        if (age < 0) throw new IllegalArgumentException();
        this.name = name;
        this.age = age;
    }
}
```

---

### JEP 512: Compact Source Files (正式版)

**状态**: 正式发布
**概述**: 简化 Java 入门体验。

```java
// Hello.java - 无需类声明
void main() {
    println("Hello, World!");
}
```

---

## 3. 核心库

### JEP 521: Generational Shenandoah (正式版) ⭐

**状态**: 正式发布
**概述**: Shenandoah GC 支持分代模式，显著降低 GC 开销。

```bash
# 启用分代 Shenandoah
java -XX:+UseShenandoahGC -XX:ShenandoahGCMode=generational MyApp
```

**性能提升**:
- GC 开销降低 30-50%
- 更适合对象生命周期短的应用

---

### JEP 506: Scoped Values (正式版)

**状态**: 正式发布
**概述**: Scoped Values 正式版，提供比 ThreadLocal 更好的替代方案。

```java
private static final ScopedValue<User> CURRENT_USER = ScopedValue.create();

ScopedValue.where(CURRENT_USER, user).run(() -> {
    // 在此作用域内可访问 CURRENT_USER.get()
    processRequest();
});
```

---

## 4. 并发与多线程

### JEP 505: Structured Concurrency (第五次预览)

**状态**: 第五次预览
**概述**: 结构化并发继续预览。

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> user = scope.fork(() -> fetchUser());
    Future<List<Order>> orders = scope.fork(() -> fetchOrders());

    scope.join();
    scope.throwIfFailed();

    return new Response(user.resultNow(), orders.resultNow());
}
```

---

## 5. 性能与监控

## 6. 安全

### JEP 451: Prepare to Disallow the Dynamic Loading of Agents

**状态**: 正式发布
**概述**: 准备禁止动态加载代理，增强安全性。

---

## 7. 移除与清理

### JEP 411: Deprecate the Security Manager for Removal

**状态**: 继续废弃
**概述**: Security Manager 继续废弃，计划在未来的版本中移除。

---

## 8. JEP 汇总

### 语言特性

| JEP | 标题 | 状态 |
|-----|------|------|
| JEP 455 | Primitive Types in Patterns | 🔍 预览 |
| JEP 512 | Compact Source Files | ✅ 正式 |
| JEP 513 | Flexible Constructor Bodies | ✅ 正式 |

### 核心库

| JEP | 标题 | 状态 |
|-----|------|------|
| JEP 506 | Scoped Values | ✅ 正式 |
| JEP 521 | Generational Shenandoah | ✅ 正式 |

### 并发

| JEP | 标题 | 状态 |
|-----|------|------|
| JEP 505 | Structured Concurrency | 🔍 预览 |

### GC

| JEP | 标题 | 状态 |
|-----|------|------|

---

## 9. 相比 JDK 21 的变化

### 新增正式特性

| 特性 | 说明 |
|------|------|
| **分代 Shenandoah** | 降低 GC 开销 |
| **Scoped Values** | ThreadLocal 的替代方案 |
| **Compact Source Files** | 简化 Java 入门体验 |
| **Flexible Constructor Bodies** | 更灵活的构造函数 |

### 继续预览的特性

| 特性 | 预览次数 |
|------|----------|
| Structured Concurrency | 第5次 |
| Primitive Types in Patterns | 第3次 |

---

## 10. 升级建议

### 从 JDK 21 升级

JDK 25 与 JDK 21 具有良好的二进制兼容性：

```bash
# 直接替换 JDK 版本即可
java -version
# openjdk version "25" 2025-09-16
```

### 推荐使用的新特性

| 场景 | 推荐特性 |
|------|----------|
| 大内存应用 | 分代 ZGC |
| 低延迟场景 | 分代 Shenandoah |
| 高并发 I/O | 虚拟线程 |

---

## 11. 相关链接

- [OpenJDK JDK 25 项目页面](https://openjdk.org/projects/jdk/25/)
- [JDK 25 JEP 列表](https://openjdk.org/projects/jdk/25/spec/)
- [GitHub: openjdk/jdk](https://github.com/openjdk/jdk)
- [JDK 25 迁移指南](/by-version/jdk25/migration/from-21.md)
