# JDK 23

> **发布日期**: 2024-09-17 | **类型**: Feature Release

---

## 核心特性

JDK 23 引入了 Module Import Declarations（预览）、Markdown 文档注释和 Primitive Types in Patterns（首次预览）。

| 特性 | 影响 | 详情 |
|------|------|------|
| **Primitive Types in Patterns（第1次预览）** | ⭐⭐⭐⭐⭐ | JEP 455 |
| **Module Import Declarations（预览）** | ⭐⭐⭐⭐ | JEP 476 |
| **Markdown 文档注释** | ⭐⭐⭐⭐ | JEP 467 |
| **Flexible Constructors（预览）** | ⭐⭐⭐ | JEP 482 |
| **Implicit Classes（第3次预览）** | ⭐⭐⭐ | JEP 477 |
| **ZGC 默认分代模式** | ⭐⭐⭐⭐⭐ | JEP 474 |
| **Class-File API（第2次预览）** | ⭐⭐⭐⭐ | JEP 466 |
| **Stream Gatherers（第2次预览）** | ⭐⭐⭐⭐ | JEP 473 |

---

## 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 455](https://openjdk.org/jeps/455) | Primitive Types in Patterns (First Preview) | 原始类型模式匹配（第1次预览） |
| [JEP 476](https://openjdk.org/jeps/476) | Module Import Declarations (Preview) | 模块导入声明 |
| [JEP 467](https://openjdk.org/jeps/467) | Markdown Documentation Comments | Markdown 文档注释 |
| [JEP 482](https://openjdk.org/jeps/482) | Flexible Constructor Bodies (Preview) | 灵活构造器 |
| [JEP 477](https://openjdk.org/jeps/477) | Implicit Classes and Instance Main Methods (Third Preview) | 隐式类（第3次预览） |
| [JEP 466](https://openjdk.org/jeps/466) | Class-File API (Second Preview) | 类文件 API（第2次预览） |
| [JEP 474](https://openjdk.org/jeps/474) | ZGC: Generational by Default | ZGC 默认分代模式 |
| [JEP 473](https://openjdk.org/jeps/473) | Stream Gatherers (Second Preview) | Stream 收集器（第2次预览） |
| [JEP 471](https://openjdk.org/jeps/471) | Deprecate the Memory-Access Methods in sun.misc.Unsafe | 废弃 Unsafe 内存访问 |
| [JEP 472](https://openjdk.org/jeps/472) | Prepare to Disallow the Dynamic Loading of Agents | 准备禁止动态加载代理 |

---

## 代码示例

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
/**
 * ## Summary
 *
 * This class does something.
 *
 * ### Example
 * ```java
 * var instance = new MyClass();
 * ```
 */
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

## 相关链接

- [发布说明](https://openjdk.org/projects/jdk/23/)
