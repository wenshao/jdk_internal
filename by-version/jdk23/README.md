# JDK 23

> **发布日期**: 2024-09-17 | **类型**: Feature Release

---
## 目录

1. [核心特性](#1-核心特性)
2. [关键 JEP](#2-关键-jep)
3. [代码示例](#3-代码示例)
4. [相关链接](#4-相关链接)

---


## 1. 核心特性

JDK 23 引入了 Module Import Declarations（预览）、Markdown 文档注释和 Primitive Types in Patterns（首次预览）。

| 特性 | 影响 | 详情 |
|------|------|------|
| **Primitive Types in Patterns（第1次预览）** | ⭐⭐⭐⭐⭐ | [JEP 455](/jeps/tools/jep-455.md) |
| **Module Import Declarations（预览）** | ⭐⭐⭐⭐ | [JEP 476](/jeps/language/jep-476.md) |
| **Markdown 文档注释** | ⭐⭐⭐⭐ | [JEP 467](/jeps/tools/jep-467.md) |
| **Flexible Constructors（第2次预览）** | ⭐⭐⭐ | [JEP 482](/jeps/language/jep-482.md) |
| **Implicit Classes（第3次预览）** | ⭐⭐⭐ | [JEP 477](/jeps/language/jep-477.md) |
| **ZGC 默认分代模式** | ⭐⭐⭐⭐⭐ | [JEP 474](/jeps/gc/jep-474.md) |
| **Class-File API（第2次预览）** | ⭐⭐⭐⭐ | [JEP 466](/jeps/tools/jep-466.md) |
| **Stream Gatherers（第2次预览）** | ⭐⭐⭐⭐ | [JEP 473](/jeps/language/jep-473.md) |
| **Structured Concurrency（第3次预览）** | ⭐⭐⭐⭐⭐ | [JEP 480](/jeps/concurrency/jep-480.md) |
| **Scoped Values（第3次预览）** | ⭐⭐⭐⭐ | [JEP 481](/jeps/concurrency/jep-481.md) |
| **Vector API（第8次孵化）** | ⭐⭐⭐ | [JEP 469](/jeps/tools/jep-469.md) |

---

## 2. 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 455](/jeps/tools/jep-455.md) | Primitive Types in Patterns (First Preview) | 原始类型模式匹配（第1次预览） |
| [JEP 476](/jeps/language/jep-476.md) | Module Import Declarations (Preview) | 模块导入声明 |
| [JEP 467](/jeps/tools/jep-467.md) | Markdown Documentation Comments | Markdown 文档注释 |
| [JEP 482](/jeps/language/jep-482.md) | Flexible Constructor Bodies (Preview) | 灵活构造器 |
| [JEP 477](/jeps/language/jep-477.md) | Implicit Classes and Instance Main Methods (Third Preview) | 隐式类（第3次预览） |
| [JEP 466](/jeps/tools/jep-466.md) | Class-File API (Second Preview) | 类文件 API（第2次预览） |
| [JEP 474](/jeps/gc/jep-474.md) | ZGC: Generational by Default | ZGC 默认分代模式 |
| [JEP 473](/jeps/language/jep-473.md) | Stream Gatherers (Second Preview) | Stream 收集器（第2次预览） |
| [JEP 469](/jeps/tools/jep-469.md) | Vector API (Eighth Incubator) | Vector API（第8次孵化） |
| [JEP 480](/jeps/concurrency/jep-480.md) | Structured Concurrency (Third Preview) | 结构化并发（第3次预览） |
| [JEP 481](/jeps/concurrency/jep-481.md) | Scoped Values (Third Preview) | 作用域值（第3次预览） |
| [JEP 471](/jeps/api/jep-471.md) | Deprecate the Memory-Access Methods in sun.misc.Unsafe | 废弃 Unsafe 内存访问 |
| [JEP 472](/jeps/ffi/jep-472.md) | Prepare to Restrict the Use of JNI | 准备限制 JNI 的使用 |

---

## 3. 代码示例

### Primitive Types in Patterns（第1次预览）

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

### Module Import Declarations（预览）

```java
// 之前
import java.util.List;
import java.util.ArrayList;
import java.util.stream.Collectors;
// ...

// JDK 23 (预览)
import module java.base;
```

### Markdown 文档注释

```java
/// ## Summary
///
/// This class does something.
///
/// ### Example
/// ```java
/// var instance = new MyClass();
/// ```
public class MyClass { }
```

### Flexible Constructors（预览）

```java
// 构造器可以调用其他构造器之前执行语句
class MyClass {
    private final int value;

    MyClass(int value) {
        this.value = value;
    }

    MyClass() {
        // 可以在 this() 之前执行语句
        int computed = computeValue();
        this(computed);
    }

    private static int computeValue() {
        return 42;
    }
}
```

---

## 4. 相关链接

- [发布说明](https://openjdk.org/projects/jdk/23/)
