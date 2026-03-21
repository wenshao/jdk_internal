# JDK 24

> **发布日期**: 2025-03-18 | **类型**: Feature Release

---

## 核心特性

JDK 24 是 JDK 25 LTS 之前的最后一个功能版本，主要完善预览特性。

| 特性 | 影响 | 详情 |
|------|------|------|
| **Primitive Types in Patterns（第2次预览）** | ⭐⭐⭐⭐⭐ | JEP 488 |
| **Implicit Classes（第4次预览）** | ⭐⭐⭐⭐ | JEP 495，更名为 Simple Source Files |
| **Structured Concurrency（第4次预览）** | ⭐⭐⭐⭐⭐ | JEP 489 |
| **Scoped Values（第4次预览）** | ⭐⭐⭐⭐ | JEP 490 |
| **Class-File API（第4次预览）** | ⭐⭐⭐⭐ | JEP 491 |
| **Generational Shenandoah（正式版）** | ⭐⭐⭐⭐⭐ | JEP 505 |
| **Stream Gatherers（第3次预览）** | ⭐⭐⭐⭐ | JEP 504 |

---

## 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 488](https://openjdk.org/jeps/488) | Primitive Types in Patterns (Second Preview) | 原始类型模式匹配（第2次预览） |
| [JEP 495](https://openjdk.org/jeps/495) | Simple Source Files and Instance Main Methods (Fourth Preview) | 简化源文件（第4次预览） |
| [JEP 489](https://openjdk.org/jeps/489) | Structured Concurrency (Fourth Preview) | 结构化并发（第4次预览） |
| [JEP 490](https://openjdk.org/jeps/490) | Scoped Values (Fourth Preview) | 作用域值（第4次预览） |
| [JEP 491](https://openjdk.org/jeps/491) | Class-File API (Fourth Preview) | 类文件 API（第4次预览） |
| [JEP 505](https://openjdk.org/jeps/505) | Generational Shenandoah | 分代 Shenandoah（正式版） |
| [JEP 504](https://openjdk.org/jeps/504) | Stream Gatherers (Third Preview) | Stream 收集器（第3次预览） |
| [JEP 506](https://openjdk.org/jeps/506) | Grouped Signatures | 分组签名 |

---

## 代码示例

### Primitive Types in Patterns（第2次预览）

```java
// instanceof 支持原始类型
if (obj instanceof int i) {
    System.out.println("Integer value: " + i);
}

// switch 支持原始类型
String result = switch (value) {
    case int i -> "int: " + i;
    case long l -> "long: " + l;
    case double d -> "double: " + d;
    default -> "unknown";
};
```

### Implicit Classes（第4次预览，更名为 Simple Source Files）

```java
// 无需类声明
void main() {
    System.out.println("Hello, World!");
}

// 带参数
void main(String[] args) {
    for (String arg : args) {
        System.out.println(arg);
    }
}
```

### Structured Concurrency（第4次预览）

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Subtask<String> user = scope.fork(() -> fetchUser());
    Subtask<List<Order>> orders = scope.fork(() -> fetchOrders());

    scope.join();
    scope.throwIfFailed();

    return new Response(user.get(), orders.get());
}
```

---

## 相关链接

- [发布说明](https://openjdk.org/projects/jdk/24/)
