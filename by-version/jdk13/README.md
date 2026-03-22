# JDK 13

> **发布日期**: 2019-09-17 | **类型**: Feature Release

---
## 目录

1. [核心特性](#1-核心特性)
2. [关键 JEP](#2-关键-jep)
3. [代码示例](#3-代码示例)
4. [相关链接](#4-相关链接)

---


## 1. 核心特性

JDK 13 引入了文本块（第1次预览）和动态 CDS 存档。

| 特性 | 影响 | 详情 |
|------|------|------|
| **文本块（第1次预览）** | ⭐⭐⭐⭐⭐ | JEP 355，多行字符串 |
| **动态 CDS 存档** | ⭐⭐⭐⭐ | [JEP 350](/jeps/performance/jep-350.md) |
| **ZGC 释放未使用内存** | ⭐⭐⭐ | [JEP 351](/jeps/gc/jep-351.md) |
| **重新实现 Socket API** | ⭐⭐⭐ | [JEP 353](/jeps/api/jep-353.md) |
| **Switch 表达式（第2次预览）** | ⭐⭐⭐⭐ | [JEP 354](/jeps/language/jep-354.md) |

---

## 2. 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 355](/jeps/language/jep-355.md) | Text Blocks (Preview) | 文本块 |
| [JEP 350](/jeps/performance/jep-350.md) | Dynamic CDS Archives | 动态 CDS 存档 |
| [JEP 351](/jeps/gc/jep-351.md) | ZGC: Uncommit Unused Memory | ZGC 释放内存 |
| [JEP 353](/jeps/api/jep-353.md) | Reimplement the Legacy Socket API | 重新实现 Socket API |
| [JEP 354](/jeps/language/jep-354.md) | Switch Expressions (Second Preview) | Switch 表达式（第2次预览） |

---

## 3. 代码示例

### 文本块（第1次预览）

```java
// 之前
String json = "{\n" +
    "  \"name\": \"Alice\",\n" +
    "  \"age\": 30\n" +
    "}";

// JDK 13 (第1次预览)
String json = """
    {
      "name": "Alice",
      "age": 30
    }
    """;
```

---

## 4. 相关链接

- [发布说明](https://openjdk.org/projects/jdk/13/)
