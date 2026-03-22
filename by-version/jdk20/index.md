# JDK 20

> **发布日期**: 2023-03-21 | **类型**: Feature Release

---
## 目录

1. [核心特性](#1-核心特性)
2. [关键 JEP](#2-关键-jep)
3. [代码示例](#3-代码示例)
4. [相关链接](#4-相关链接)

---


## 1. 核心特性

JDK 20 是一个相对较小的版本，主要改进预览特性。

| 特性 | 影响 | 详情 |
|------|------|------|
| **Virtual Threads（第2次预览）** | ⭐⭐⭐⭐⭐ | [JEP 436](/jeps/concurrency/jep-436.md) |
| **Structured Concurrency（第2次孵化）** | ⭐⭐⭐⭐⭐ | JEP 437 |
| **Record Patterns（第2次预览）** | ⭐⭐⭐⭐ | JEP 432 |
| **Pattern Matching for switch（第4次预览）** | ⭐⭐⭐⭐ | JEP 433 |
| **Foreign Function & Memory API（第2次预览）** | ⭐⭐⭐⭐ | JEP 434 |
| **Scoped Values（孵化器）** | ⭐⭐⭐⭐ | JEP 429 |
| **Vector API（第5次孵化）** | ⭐⭐⭐ | JEP 438 |

---

## 2. 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 429](https://openjdk.org/jeps/429) | Scoped Values (Incubator) | 作用域值（孵化器） |
| [JEP 432](https://openjdk.org/jeps/432) | Record Patterns (Second Preview) | Record 模式匹配（第2次预览） |
| [JEP 433](https://openjdk.org/jeps/433) | Pattern Matching for switch (Fourth Preview) | switch 模式匹配（第4次预览） |
| [JEP 434](https://openjdk.org/jeps/434) | Foreign Function & Memory API (Second Preview) | FFM API（第2次预览） |
| [JEP 436](/jeps/concurrency/jep-436.md) | Virtual Threads (Second Preview) | 虚拟线程（第2次预览） |
| [JEP 437](https://openjdk.org/jeps/437) | Structured Concurrency (Second Incubator) | 结构化并发（第2次孵化） |
| [JEP 438](https://openjdk.org/jeps/438) | Vector API (Fifth Incubator) | Vector API（第5次孵化） |

---

## 3. 代码示例

### Scoped Values（孵化器）

```java
// 替代 ThreadLocal
public static final ScopedValue<String> USER = ScopedValue.newInstance();

ScopedValue.where(USER, "alice")
    .run(() -> {
        System.out.println(USER.get()); // "alice"
    });
```

### Record Patterns（第2次预览）

```java
record Point(int x, int y) { }
record Rectangle(Point topLeft, Point bottomRight) { }

// JDK 20 (第2次预览)
if (obj instanceof Rectangle(Point(int x1, int y1), Point(int x2, int y2))) {
    System.out.println("Rectangle from (" + x1 + "," + y1 + ") to (" + x2 + "," + y2 + ")");
}
```

---

## 4. 相关链接

- [发布说明](https://openjdk.org/projects/jdk/20/)
