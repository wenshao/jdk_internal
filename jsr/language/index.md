# 语言规范 (Language) 索引

> Java 语言规范相关 JSR

---
## 目录

1. [概览](#1-概览)
2. [孵化项目](#2-孵化项目)
3. [详解](#3-详解)
4. [相关链接](#4-相关链接)

---


## 1. 概览

| JSR | 标题 | JDK | 状态 | 说明 |
|-----|------|-----|------|------|
| [JSR 335](jsr-335.md) ⭐ | Lambda Expressions | 8 | ✅ Final | 函数式接口、 Lambda |
| [JSR 394](https://jcp.org/en/jsr/detail?id=394) | Pattern Matching for instanceof | 16 | ✅ Final | 类型模式匹配 |
| [JSR 395](https://jcp.org/en/jsr/detail?id=395) | Records | 16 | ✅ Final | 记录类 |
| [JSR 397](https://jcp.org/en/jsr/detail?id=397) | Sealed Classes | 17 | ✅ Final | 密封类/接口 |
| [Valhalla](/by-topic/core/valhalla/) | Value Types | TBD | 🚧 开发中 | 值类型 (非正式 JSR) |

> ⭐ = 有本地详细文档

---

## 2. 孵化项目

### Project Valhalla (值类型)

> **状态**: 🚧 开发中 | **分支**: lworld

值类型是 Java 语言自泛型以来最大的变革，目标是消除装箱开销。

```java
value record Point(int x, int y) { }
```

**详见**: [Valhalla: Value Types](/by-topic/core/valhalla/)

---

## 3. 详解

- [JSR 335: Lambda Expressions](jsr-335.md) ⭐

### 外部链接

- [JSR 394: Pattern Matching for instanceof](https://jcp.org/en/jsr/detail?id=394)
- [JSR 395: Records](https://jcp.org/en/jsr/detail?id=395)
- [JSR 397: Sealed Classes](https://jcp.org/en/jsr/detail?id=397)

---

## 4. 相关链接

- [JCP JSR 列表](https://jcp.org/en/jsr/all)
- [OpenJDK JEPs](https://openjdk.org/jeps/)
- [JEP 索引](/jeps/)
- [Project Valhalla](https://openjdk.org/projects/valhalla/)
