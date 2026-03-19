# JDK 13

> **发布日期**: 2019-09-17 | **类型**: Feature Release

---

## 核心特性

JDK 13 引入了文本块（预览）和动态 CDS 存档。

| 特性 | 影响 | 详情 |
|------|------|------|
| **文本块** | ⭐⭐⭐⭐⭐ | JEP 355，多行字符串 |
| **动态 CDS 存档** | ⭐⭐⭐⭐ | JEP 350 |
| **ZGC 释放未使用内存** | ⭐⭐⭐ | JEP 351 |
| **重新实现 Socket API** | ⭐⭐⭐ | JEP 353 |

---

## 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 355](https://openjdk.org/jeps/355) | Text Blocks (Preview) | 文本块 |
| [JEP 350](https://openjdk.org/jeps/350) | Dynamic CDS Archives | 动态 CDS 存档 |
| [JEP 351](https://openjdk.org/jeps/351) | ZGC: Uncommit Unused Memory | ZGC 释放内存 |
| [JEP 353](https://openjdk.org/jeps/353) | Reimplement the Legacy Socket API | 重新实现 Socket API |
| [JEP 354](https://openjdk.org/jeps/354) | Switch Expressions (Second Preview) | Switch 表达式（第2次预览） |
| [JEP 356](https://openjdk.org/jeps/356) | Enhanced Pseudo-Random Number Generators | 增强随机数生成器 |

---

## 代码示例

### 文本块（预览）

```java
// 之前
String json = "{\n" +
    "  \"name\": \"Alice\",\n" +
    "  \"age\": 30\n" +
    "}";

// JDK 13 (预览)
String json = """
    {
      "name": "Alice",
      "age": 30
    }
    """;
```

### 增强随机数生成器

```java
// 新的随机数 API
RandomGenerator generator = RandomGenerator.of("L32X64MixRandom");
int value = generator.nextInt(100);
```

---

## 相关链接

- [发布说明](https://openjdk.org/projects/jdk/13/)
