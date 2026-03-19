# JDK 24

> **发布日期**: 2025-03-18 | **类型**: Feature Release

---

## 核心特性

JDK 24 是 JDK 25 LTS 之前的最后一个功能版本，主要完善预览特性。

| 特性 | 影响 | 详情 |
|------|------|------|
| **String Templates（第3次预览）** | ⭐⭐⭐⭐⭐ | JEP 430 |
| **Implicit Classes（第4次预览）** | ⭐⭐⭐⭐ | JEP 463 |
| **Primitive Types in Patterns（第3次预览）** | ⭐⭐⭐⭐ | JEP 455 |
| **Structured Concurrency（第4次预览）** | ⭐⭐⭐⭐⭐ | JEP 452 |
| **Scoped Values（第4次预览）** | ⭐⭐⭐⭐ | JEP 446 |
| **Class-File API（第4次预览）** | ⭐⭐⭐⭐ | JEP 466 |

---

## 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 430](https://openjdk.org/jeps/430) | String Templates (Third Preview) | 字符串模板（第3次预览） |
| [JEP 463](https://openjdk.org/jeps/463) | Implicit Classes and Instance Main Methods (Third Preview) | 隐式类（第3次预览） |
| [JEP 455](https://openjdk.org/jeps/455) | Primitive Types in Patterns (Third Preview) | 原始类型模式匹配（第3次预览） |
| [JEP 452](https://openjdk.org/jeps/452) | Structured Concurrency (Fourth Preview) | 结构化并发（第4次预览） |
| [JEP 446](https://openjdk.org/jeps/446) | Scoped Values (Third Preview) | 作用域值（第3次预览） |
| [JEP 466](https://openjdk.org/jeps/466) | Class-File API (Third Preview) | 类文件 API（第3次预览） |
| [JEP 476](https://openjdk.org/jeps/476) | Module Import Declarations (Second Preview) | 模块导入声明（第2次预览） |
| [JEP 474](https://openjdk.org/jeps/474) | ZGC: Generational by Default | ZGC 默认分代 |
| [JEP 477](https://openjdk.org/jeps/477) | Unnamed Classes and Instance Main Methods (Fourth Preview) | 未命名类（第4次预览） |
| [JEP 478](https://openjdk.org/jeps/478) | Stream Gatherers (Third Preview) | Stream 收集器（第3次预览） |

---

## 代码示例

### String Templates（第3次预览）

```java
// STR 模板处理器
String name = "World";
String message = STR."Hello, \{name}!";

// FMT 格式化
String formatted = FMT."Value: \{42}%.2f";

// JSON 模板
String json = JSON."""
    {"name": "\{name}", "value": \{42}}
    """;
```

### Implicit Classes（第4次预览）

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

---

## 相关链接

- [发布说明](https://openjdk.org/projects/jdk/24/)
