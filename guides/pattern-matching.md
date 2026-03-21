# Java 模式匹配指南

> Java 模式匹配特性完整指南

---
## 目录

1. [概述](#1-概述)
2. [instanceof 模式匹配](#2-instanceof-模式匹配)
3. [switch 模式匹配](#3-switch-模式匹配)
4. [Record Patterns](#4-record-patterns)
5. [原始类型模式 (JDK 26)](#5-原始类型模式-jdk-26)
6. [最佳实践](#6-最佳实践)
7. [相关资源](#7-相关资源)

---


## 1. 概述

模式匹配是 Java 的现代特性，简化了类型检查和提取的逻辑。

### 演进历史

| 版本 | 特性 | JEP |
|------|------|-----|
| Java 16 | instanceof 模式匹配 | JEP 394 |
| Java 17 | switch 模式匹配 (Preview) | JEP 406 |
| Java 21 | Record Patterns | JEP 440 |
| Java 23 | 原始类型模式 (Preview) | JEP 455 |
| Java 26 | 原始类型模式 (4th Preview) | JEP 530 |

---

## 2. instanceof 模式匹配

### 传统写法

```java
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.length());
}
```

### 模式匹配写法

```java
if (obj instanceof String s) {
    System.out.println(s.length());
}
```

### 带守卫条件

```java
if (obj instanceof String s && s.length() > 5) {
    System.out.println("Long string: " + s);
}
```

---

## 3. switch 模式匹配

### 基本语法

```java
switch (obj) {
    case Integer i -> System.out.println("Integer: " + i);
    case Long l    -> System.out.println("Long: " + l);
    case Double d  -> System.out.println("Double: " + d);
    case String s  -> System.out.println("String: " + s);
    default        -> System.out.println("Other");
}
```

### 带守卫条件

```java
switch (obj) {
    case String s when s.isEmpty() -> "Empty string";
    case String s                  -> "String: " + s;
    default                        -> "Other";
}
```

---

## 4. Record Patterns

### 匹配 Record 组件

```java
record Point(int x, int y) {}

// 传统写法
if (obj instanceof Point p) {
    int x = p.x();
    int y = p.y();
}

// Record Pattern
if (obj instanceof Point(int x, int y)) {
    System.out.println("x=" + x + ", y=" + y);
}
```

### 嵌套模式

```java
record Box(Point p) {}

if (obj instanceof Box(Point(int x, int y))) {
    System.out.println("Box contains Point(" + x + ", " + y + ")");
}
```

---

## 5. 原始类型模式 (JDK 26)

### instanceof 支持原始类型

```java
if (obj instanceof int i) {
    System.out.println("Integer value: " + i);
}
```

### switch 支持原始类型模式

```java
switch (value) {
    case int i    -> System.out.println("int: " + i);
    case long l   -> System.out.println("long: " + l);
    case double d -> System.out.println("double: " + d);
    default       -> System.out.println("other");
}
```

---

## 6. 最佳实践

### 1. 优先使用模式匹配

```java
// 推荐
if (obj instanceof String s) { ... }

// 不推荐
if (obj instanceof String) {
    String s = (String) obj;
    ...
}
```

### 2. 利用守卫条件简化逻辑

```java
// 推荐
switch (obj) {
    case String s when s.length() > 10 -> processLongString(s);
    case String s                      -> processString(s);
    default                            -> processOther(obj);
}
```

### 3. Record 模式解构

```java
// 推荐
if (obj instanceof Point(int x, int y)) {
    // 直接使用 x, y
}
```

---

## 7. 相关资源

- [JEP 394: Pattern Matching for instanceof](https://openjdk.org/jeps/394)
- [JEP 441: Pattern Matching for switch](https://openjdk.org/jeps/441)
- [JEP 440: Record Patterns](https://openjdk.org/jeps/440)
- [JEP 530: Primitive Types in Patterns](https://openjdk.org/jeps/530)