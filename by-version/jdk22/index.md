# JDK 22

> **发布日期**: 2024-03-19 | **类型**: Feature Release

---
## 目录

1. [核心特性](#1-核心特性)
2. [关键 JEP](#2-关键-jep)
3. [代码示例](#3-代码示例)
4. [相关链接](#4-相关链接)

---


## 1. 核心特性

JDK 22 是一个功能丰富的版本，包含 12 个 JEP，重点完善预览特性。

| 特性 | 影响 | 详情 |
|------|------|------|
| **String Templates（第2次预览）** | ⭐⭐⭐⭐⭐ | JEP 459，后于 JDK 23 撤销 |
| **Unnamed Variables（正式版）** | ⭐⭐⭐⭐ | JEP 456 |
| **Statements before super(...)（预览）** | ⭐⭐⭐⭐ | JEP 447 |
| **Stream Gatherers（预览）** | ⭐⭐⭐⭐ | JEP 461 |
| **Implicit Classes（第2次预览）** | ⭐⭐⭐⭐ | JEP 463 |
| **Structured Concurrency（第2次预览）** | ⭐⭐⭐⭐⭐ | JEP 462 |
| **Scoped Values（第2次预览）** | ⭐⭐⭐⭐ | JEP 464 |
| **Foreign Function & Memory API（正式版）** | ⭐⭐⭐⭐ | JEP 454 |
| **Class-File API（预览）** | ⭐⭐⭐⭐ | JEP 457 |
| **Launch Multi-File Source-Code Programs** | ⭐⭐⭐ | JEP 458 |
| **Vector API（第7次孵化）** | ⭐⭐⭐ | JEP 460 |
| **Region Pinning for G1** | ⭐⭐⭐ | JEP 423 |

---

## 2. 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 447](https://openjdk.org/jeps/447) | Statements before super(...) (Preview) | 构造器中 super 前语句 |
| [JEP 454](https://openjdk.org/jeps/454) | Foreign Function & Memory API | FFM API（正式版） |
| [JEP 456](https://openjdk.org/jeps/456) | Unnamed Variables and Patterns | 未命名变量（正式版） |
| [JEP 457](https://openjdk.org/jeps/457) | Class-File API (Preview) | 类文件 API（预览） |
| [JEP 458](https://openjdk.org/jeps/458) | Launch Multi-File Source-Code Programs | 启动多文件源程序 |
| [JEP 459](https://openjdk.org/jeps/459) | String Templates (Second Preview) | 字符串模板（第2次预览） |
| [JEP 461](https://openjdk.org/jeps/461) | Stream Gatherers (Preview) | Stream 收集器 |
| [JEP 462](https://openjdk.org/jeps/462) | Structured Concurrency (Second Preview) | 结构化并发（第2次预览） |
| [JEP 463](https://openjdk.org/jeps/463) | Implicit Classes and Instance Main Methods (Second Preview) | 隐式类（第2次预览） |
| [JEP 464](https://openjdk.org/jeps/464) | Scoped Values (Second Preview) | 作用域值（第2次预览） |
| [JEP 460](https://openjdk.org/jeps/460) | Vector API (Seventh Incubator) | Vector API（第7次孵化） |
| [JEP 423](https://openjdk.org/jeps/423) | Region Pinning for G1 | G1 区域锁定 |

---

## 3. 代码示例

### Statements before super(...)（预览）

```java
class MyClass extends BaseClass {
    private final int computed;

    // JDK 22 之前：必须在 super() 之前初始化字段
    MyClass(int value) {
        super(); // 必须是第一行
        this.computed = value * 2; // 字段初始化在 super 之后
    }

    // JDK 22：可以在 super() 之前执行语句
    MyClass(int value) {
        int temp = computeValue(value); // 可以在 super 之前
        super(temp);
        this.computed = temp;
    }

    private static int computeValue(int value) {
        return value * 2;
    }
}
```

### String Templates（第2次预览，后于 JDK 23 撤销）

```java
// STR 模板
String name = "World";
String message = STR."Hello, \{name}!";

// JSON 模板
String json = JSON."""
    {
        "name": "\{name}",
        "value": \{42}
    }
    """;
```

### Stream Gatherers（第1次预览，JDK 24 正式版）

```java
// 自定义中间操作
List<Integer> result = Stream.of(1, 2, 3, 4, 5)
    .gather(Gatherers.fold(() -> 0, Integer::sum))
    .toList();
```

### 未命名变量（正式版）

```java
// _ 作为未命名变量
try (var _ = ScopedValue.where(USER, "alice")) {
    // ...
} catch (Exception _) {
    // 忽略异常
}

// 在 lambda 中
BiFunction<Integer, Integer, String> add = (x, _) -> "x + y = " + (x + 10);

// 在增强 for 中
for (String _ : list) {
    count++;  // 只关心数量
}
```

---

## 4. 相关链接

- [发布说明](https://openjdk.org/projects/jdk/22/)
