# 字符串处理时间线

> Java String 从 JDK 1.0 到 JDK 26 的完整演进历程

---
## 目录

1. [时间线概览](#1-时间线概览)
2. [版本演进](#2-版本演进)
3. [性能汇总](#3-性能汇总)
4. [相关 JEP](#4-相关-jep)
5. [更多文档](#5-更多文档)

---


## 1. 时间线概览

```
JDK 1.0 ──── JDK 5 ──── JDK 6u32 ──── JDK 9 ──── JDK 11 ──── JDK 15 ──── JDK 21 ──── JDK 24 ──── JDK 26
   │           │           │            │          │           │           │           │           │
 String     StringBuilder  Substring   Compact    repeat()   Text Blocks  String     Hidden     toString
 诞生        无同步        修复        Strings    strip()     (JEP 378)  Templates  Class      优化
 常量池                                (JEP 254)                         (JEP 430)  Strategy
                                                                                     (+40%启动)
```

---

## 2. 版本演进

### JDK 1.0 (1996)

**String 诞生**

- 不可变设计
- char[] 存储 (UTF-16)
- 字符串常量池
- intern() 方法

**问题**: substring() 共享原数组，可能导致内存泄漏

---

### JDK 5 (2004)

**StringBuilder 引入**

| 类 | 线程安全 | 性能 |
|---|---------|------|
| StringBuffer | 是 | 基准 |
| StringBuilder | 否 | **+2.8x** |

---

### JDK 6u32 (2012)

**substring() 内存泄漏修复**

```java
// 之前: 共享数组
return new String(offset, len, value);

// 之后: 复制数组
return new String(value, off, len);
```

---

### JDK 8u20 (2014)

**String Deduplication (JEP 192)**

- G1 GC 自动去重
- 节省 10-30% 堆内存
- 完全自动化

→ [详细说明](optimization.md#string-deduplication-jep-192)

---

### JDK 9 (2017)

**Compact Strings (JEP 254)**

| 特性 | 说明 |
|------|------|
| 存储 | char[] → byte[] |
| ASCII 内存 | 节省 **50%** |
| coder 标志 | 0=LATIN1, 1=UTF16 |

**invokedynamic 拼接 (JEP 280)**

- 字符串拼接使用 invokedynamic
- +10% 启动性能

→ [详细说明](implementation.md#compact-strings-jep-254)

---

### JDK 11 (2018)

**新增方法**

```java
str.repeat(3);      // 重复字符串
str.strip();        // Unicode 去空格
str.stripLeading();
str.stripTrailing();
str.isBlank();      // 检查空白
```

**StringJoiner**

```java
String.join(", ", list);
```

---

### JDK 15 (2020)

**Text Blocks (JEP 378)**

```java
String html = """
    <html>
        <body>Hello</body>
    </html>
    """;
```

---

### JDK 21 (2023)

**String Templates (JEP 430) - 预览**

```java
String message = STR."Hello \{name}, you have \{count} messages.";
```

---

### JDK 24 (2025)

**隐藏类拼接策略 (JDK-8336856)**

| 指标 | 提升 |
|------|------|
| 启动性能 | **+40%** |
| 类加载时间 | -50% |
| 元空间占用 | -60% |

**贡献者**: Shaojin Wen (温绍锦, Alibaba), Claes Redestad (Oracle)

→ [详细说明](optimization.md#贡献者)

---

### JDK 25 (2025)

**StringBuilder 优化 (JDK-8355177)**

- 使用 Unsafe.copyMemory
- **+15%** 吞吐量

**贡献者**: Shaojin Wen (温绍锦, Alibaba)

---

### JDK 26 (2026)

**Integer/Long.toString 优化 (JDK-8370503)**

- 专用 LATIN1 路径
- **+16%** C1 编译性能

**贡献者**: Shaojin Wen (温绍锦, Alibaba)

---

## 3. 性能汇总

| 版本 | 特性 | 内存 | 启动 | 运行时 |
|------|------|------|------|--------|
| JDK 8 | char[] | 基准 | 基准 | 基准 |
| JDK 9 | Compact Strings | -50% (ASCII) | +5% | +2% |
| JDK 9 | invokedynamic | - | +10% | +3% |
| JDK 24 | 隐藏类拼接 | - | **+40%** | +5% |
| JDK 25 | StringBuilder 优化 | - | - | +15% |
| JDK 26 | toString 优化 | - | - | +16% (C1) |

---

## 4. 相关 JEP

| JEP | 标题 | 版本 |
|-----|------|------|
| [JEP 254](/jeps/language/jep-254.md) | Compact Strings | JDK 9 |
| [JEP 280](/jeps/language/jep-280.md) | Indify String Concatenation | JDK 9 |
| [JEP 192](https://openjdk.org/jeps/192) | String Deduplication | JDK 8 |
| [JEP 378](/jeps/language/jep-378.md) | Text Blocks | JDK 15 |
| [JEP 430](/jeps/language/jep-430.md) | String Templates | JDK 21 |

---

## 5. 更多文档

- [内部实现](implementation.md) - Compact Strings、StringLatin1、StringUTF16
- [性能优化](optimization.md) - String Deduplication、VM 调优、最佳实践
- [返回概览](index.md)

---

> **最后更新**: 2026-03-20
