# JDK 22

> **发布日期**: 2024-03-19 | **类型**: Feature Release

---

## 核心特性

JDK 22 引入了 String Templates（第2次预览）、Implicit Classes（第2次预览）、Stream Gatherers（预览）和Unnamed Variables（正式版）。

| 特性 | 影响 | 详情 |
|------|------|------|
| **String Templates（第2次预览）** | ⭐⭐⭐⭐⭐ | JEP 459 |
| **Implicit Classes（第2次预览）** | ⭐⭐⭐⭐ | JEP 463 |
| **Stream Gatherers（预览）** | ⭐⭐⭐⭐ | JEP 461 |
| **Unnamed Variables（正式版）** | ⭐⭐⭐⭐ | JEP 456 |
| **Structured Concurrency（第3次预览）** | ⭐⭐⭐⭐⭐ | JEP 462 |
| **Scoped Values（第2次预览）** | ⭐⭐⭐⭐ | JEP 464 |
| **Foreign Function & Memory API（第3次预览）** | ⭐⭐⭐⭐ | JEP 454 |
| **Launch Multi-File Source-Code Programs** | ⭐⭐⭐ | JEP 458 |

---

## 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 459](https://openjdk.org/jeps/459) | String Templates (Second Preview) | 字符串模板（第2次预览） |
| [JEP 463](https://openjdk.org/jeps/463) | Implicit Classes and Instance Main Methods (Second Preview) | 隐式类（第2次预览） |
| [JEP 461](https://openjdk.org/jeps/461) | Stream Gatherers (Preview) | Stream 收集器 |
| [JEP 456](https://openjdk.org/jeps/456) | Unnamed Variables and Patterns | 未命名变量（正式版） |
| [JEP 462](https://openjdk.org/jeps/462) | Structured Concurrency (Third Preview) | 结构化并发（第3次预览） |
| [JEP 464](https://openjdk.org/jeps/464) | Scoped Values (Second Preview) | 作用域值（第2次预览） |
| [JEP 454](https://openjdk.org/jeps/454) | Foreign Function & Memory API (Third Preview) | FFM API（第3次预览） |
| [JEP 458](https://openjdk.org/jeps/458) | Launch Multi-File Source-Code Programs | 启动多文件源程序 |

---

## 代码示例

### String Templates（预览）

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

### Stream Gatherers（预览）

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

## 相关链接

- [发布说明](https://openjdk.org/projects/jdk/22/)
