# JDK 25 JEP 汇总

> JDK 25 包含的所有 JEP (JDK Enhancement Proposals) 详细列表

---
## 目录

1. [语言特性](#1-语言特性)
2. [并发](#2-并发)
3. [JEP 完整列表](#3-jep-完整列表)

---


## 1. 语言特性

### JEP 507: Primitive Types in Patterns (第三次预览)

**状态**: 🔍 Preview

模式匹配支持原始类型，无需包装类。

```java
// switch 支持原始类型
String formatted = switch (value) {
    case int i -> "int: " + i;
    case long l -> "long: " + l;
    case double d -> "double: " + d;
    case float f -> "float: " + f;
    default -> "unknown";
};

// instanceof 支持原始类型
if (obj instanceof int i) {
    System.out.println("Integer value: " + i);
}
```

**相关**: [JEP 文档](https://openjdk.org/jeps/507)

---

### JEP 512: Compact Source Files (正式版)

**状态**: ✅ Final

简化单文件程序的编写，无需显式类声明。

```java
// 隐式类 - 无需 public class
void main() {
    System.out.println("Hello, World!");
}

// 带参数的 main
void main(String[] args) {
    for (String arg : args) {
        System.out.println(arg);
    }
}
```

**相关**: [JEP 文档](https://openjdk.org/jeps/512)

---

## 2. 并发

### JEP 505: Structured Concurrency (第五次预览)

**状态**: 🔍 Preview

结构化并发简化并发任务管理。

```java
try (var scope = new StructuredTaskScope<Object>()) {
    Subtask<String> user = scope.fork(() -> fetchUser(id));
    Subtask<List<Order>> orders = scope.fork(() -> fetchOrders(id));

    scope.join();
    scope.throwIfFailed();

    return new Response(user.get(), orders.get());
}
```

**相关**: [JEP 文档](https://openjdk.org/jeps/505)

---

### JEP 506: Scoped Values (正式版)

**状态**: ✅ Final

作用域值提供线程安全的隐式参数传递。

```java
public static final ScopedValue<String> USER = ScopedValue.newInstance();

// 在作用域内设置值
ScopedValue.where(USER, "alice")
    .run(() -> {
        // 在这里可以访问 USER
        System.out.println(USER.get()); // "alice"
    });
```

**相关**: [JEP 文档](https://openjdk.org/jeps/506)

---

## 3. JEP 完整列表

| JEP | 标题 | 状态 |
|-----|------|------|
| 505 | Structured Concurrency | 🔍 |
| 506 | Scoped Values | ✅ |
| 507 | Primitive Types in Patterns | 🔍 |
| 512 | Compact Source Files | ✅ |

> 图例: ✅ Final | 🔍 Preview | ⚠️ Deprecated
