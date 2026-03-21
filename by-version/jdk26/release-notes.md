# JDK 26 发布说明

> 基于 openjdk/jdk 仓库标签 `jdk-26+26` 分析

## 1. 概述

JDK 26 包含 **10 个 JEP**（JDK Enhancement Proposals），涵盖语言特性、API、性能优化、垃圾回收等多个领域。

---
## 目录

1. [概述](#1-概述)
2. [语言特性](#2-语言特性)
3. [并发与多线程](#3-并发与多线程)
4. [性能与监控](#4-性能与监控)
5. [网络](#5-网络)
6. [安全](#6-安全)
7. [移除与清理](#7-移除与清理)
8. [快速导航](#8-快速导航)
9. [相关链接](#9-相关链接)

---


## 2. 语言特性

### [JEP 530: Primitive Types in Patterns](/jeps/language/jep-530.md)

**状态**: 第四次预览  
**概述**: 允许在模式匹配中使用原始类型。

```java
switch (value) {
    case int i -> System.out.println("int: " + i);
    case long l -> System.out.println("long: " + l);
    case double d -> System.out.println("double: " + d);
}
```

---

### [JEP 526: Lazy Constants](/jeps/tools/jep-526.md)

**状态**: 第二次预览  
**概述**: 引入延迟初始化的常量声明。

```java
private static lazy ExpensiveObject CACHE = new ExpensiveObject();
```

---

## 3. 并发与多线程

### [JEP 525: Structured Concurrency](/jeps/concurrency/jep-525.md)

**状态**: 第六次预览  
**概述**: 结构化并发继续预览，简化多线程编程模型。

```java
try (var scope = StructuredTaskScope.open()) {
    Subtask<String> user = scope.fork(() -> fetchUser());
    Subtask<Integer> order = scope.fork(() -> fetchOrder());
    scope.join();
    return new Response(user.get(), order.get());
}
```

---

## 4. 性能与监控

### [JEP 522: G1 GC Throughput Improvement](/jeps/gc/jep-522.md) ⭐

**状态**: 正式发布  
**概述**: 优化 G1 GC 的同步机制，提升吞吐量 10-20%。

---

## 5. 网络

### [JEP 517: HTTP/3 for the HTTP Client API](/jeps/network/jep-517.md) ⭐

**状态**: 正式发布  
**概述**: HTTP Client API 正式支持 HTTP/3 (QUIC) 协议。

```java
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3)
    .build();
```

---

## 6. 安全

### JEP 524: PEM Encodings (Second Preview)

**状态**: 第二次预览  
**概述**: JEP 470 的第二次预览，根据反馈进行改进。

---

## 7. 移除与清理

### [JEP 504: Remove the Applet API](/jeps/removed/jep-504.md)

**状态**: 正式移除  
**概述**: 正式移除已废弃的 Applet API，包括 `java.applet` 包。

---

### [JEP 500: Prepare to Make Final Mean Final](/jeps/removed/jep-500.md)

**状态**: 正式发布  
**概述**: 为最终字段提供更强的不可变性保证，限制通过反射和 JNI 修改 final 字段。

---

## 8. 快速导航

| 类别 | JEP 数量 | 亮点 |
|------|----------|------|
| 语言特性 | 2 | 原始类型模式、延迟常量 |
| 并发 | 1 | 结构化并发 |
| 性能 | 3 | G1 优化、AOT 对象缓存、Vector API |
| 网络 | 1 | HTTP/3 |
| 安全 | 1 | PEM 编码 |
| 移除与清理 | 2 | Applet API、Final 限制 |

---

## 9. 相关链接

- [OpenJDK JDK 26 项目页面](https://openjdk.org/projects/jdk/26/)
- [JDK 26 JEP 列表](https://openjdk.org/projects/jdk/26/spec/)
- [GitHub: openjdk/jdk](https://github.com/openjdk/jdk)