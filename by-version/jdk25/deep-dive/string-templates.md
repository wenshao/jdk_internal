# String Templates 深度分析

> JDK 25 正式特性 - JEP 430

---
## 目录

1. [概述](#1-概述)
2. [核心概念](#2-核心概念)
3. [实现原理](#3-实现原理)
4. [使用示例](#4-使用示例)
5. [自定义模板处理器](#5-自定义模板处理器)
6. [性能特性](#6-性能特性)
7. [安全特性](#7-安全特性)
8. [最佳实践](#8-最佳实践)
9. [相关链接](#9-相关链接)

---


## 1. 概述

String Templates（字符串模板）是 JDK 25 正式引入的特性，提供了一种安全、易读的字符串插值方式。

---

## 2. 核心概念

### 模板表达式

```java
String name = "World";
String message = STR."Hello, \{name}!";
// 等价于: "Hello, " + name + "!"
```

### 内置模板处理器

| 处理器 | 用途 | 示例 |
|--------|------|------|
| STR | 普通字符串 | `STR."Value: \{x}"` |
| FMT | 格式化字符串 | `FMT."Value: \{x}%d"` |
| JSON | JSON 格式 | `JSON."\{\"key\": \{x}\}"` |
| RAW | 原始字符串 | `RAW."Line1\nLine2"` |

---

## 3. 实现原理

### 编译时转换

```java
// 源码
String s = STR."Hello \{name}!";

// 编译后 (简化)
String s = STR.process("\1s\1s", "Hello ", name, "!");
```

### 模板处理器接口

```java
public interface StringProcessor {
    String process(String[] segments, Object... values)
        throws IllegalArgumentException;
}
```

---

## 4. 使用示例

### 基础用法

```java
// 变量插值
int x = 10, y = 20;
String result = STR."\{x} + \{y} = \{x + y}";
// "10 + 20 = 30"

// 表达式求值
String status = STR."User: \{user.getName()}, Age: \{user.getAge()}";

// 多行模板
String json = STR."""
    {
        "name": "\{name}",
        "age": \{age},
        "active": \{active}
    }
    """;
```

### JSON 模板

```java
// JSON 处理器自动转义
String name = "Alice \"The Great\"";
String json = JSON."""
    {
        "name": "\{name}",
        "value": \{42}
    }
    """;
// {"name": "Alice \"The Great\"", "value": 42}
```

### 格式化模板

```java
// FMT 处理器
double pi = Math.PI;
String formatted = FMT."Pi ≈ \{pi}%.2f";
// "Pi ≈ 3.14"

// 对齐
String table = FMT."""
    Name: \{name}%-20s Age: \{age}%3d
    """;
```

---

## 5. 自定义模板处理器

```java
// SQL 安全处理器 (防止 SQL 注入)
public class SQLProcessor implements StringProcessor {
    public String process(String[] segments, Object... values) {
        StringBuilder sb = new StringBuilder(segments[0]);
        for (int i = 0; i < values.length; i++) {
            sb.append("?");  // 使用参数化查询
            sb.append(segments[i + 1]);
        }
        return sb.toString();
    }
}

// 使用
SQLProcessor SQL = new SQLProcessor();
String name = "Alice";
String query = SQL."SELECT * FROM users WHERE name = '\{name}'";
// "SELECT * FROM users WHERE name = ?"
```

---

## 6. 性能特性

### 与字符串拼接对比

| 操作 | 拼接 | 模板 | 性能 |
|------|------|------|------|
| 编译时常量 | 相同 | 相同 | 相同 |
| 运行时变量 | 慢 | 快 | 模板更快 |
| 复杂表达式 | 慢 | 快 | 模板更快 |

### 编译优化

```java
// 编译时常量折叠
String s = STR."Hello" + " World";
// 优化为: "Hello World"

// StringBuilder 优化
String s = STR."A\{x}B\{y}C";
// 优化为: StringBuilder 类似实现
```

---

## 7. 安全特性

### 自动转义

```java
// JSON 模板自动转义特殊字符
String input = "<script>alert('XSS')</script>";
String json = JSON."{\"content\": \"\{input}\"}";
// {"content": "<script>alert('XSS')</script>"}
```

### SQL 注入防护

```java
// 使用模板处理器 + PreparedStatement
String name = userInput;
String query = SQL."SELECT * FROM users WHERE name = '\{name}'";
// 返回参数化查询，而非直接拼接
```

---

## 8. 最佳实践

### 推荐用法

```java
// ✓ 推荐: 使用模板
String message = STR."Hello, \{name}!";

// ✓ 推荐: JSON 处理
String json = JSON."""
    {"key": "\{value}"}
    """;

// ✓ 推荐: 格式化
String formatted = FMT."Value: \{value}%.2f";
```

### 避免用法

```java
// ✗ 避免: 复杂逻辑放在模板中
String s = STR."Result: \{complexCalculation()}";

// 更好: 提前计算
int result = complexCalculation();
String s = STR."Result: \{result}";
```

---

## 9. 相关链接

- [JEP 430: String Templates](https://openjdk.org/jeps/430)
- [Javadoc: java.lang.string.template](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/template/package-summary.html)
