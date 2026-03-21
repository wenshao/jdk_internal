# JDK 25 JEP 汇总

> JDK 25 包含的所有 JEP (JDK Enhancement Proposals) 详细列表

---
## 目录

1. [语言特性](#1-语言特性)
2. [性能](#2-性能)
3. [并发](#3-并发)
4. [安全](#4-安全)
5. [JEP 完整列表](#5-jep-完整列表)

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

### JEP 512: Compact Source Files (第四次预览)

**状态**: 🔍 Preview

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

## 2. 性能

### JEP 448: JVM Code Heap Segmentation

**状态**: ✅ Final

JVM 代码堆分段，优化启动时间和内存占用。

**改进**:
- 更快的方法查找
- 更低的代码缓存占用
- 更好的 JIT 编译器性能

---

### JEP 449: Barrier-Based C2 Compilation

**状态**: ✅ Final

C2 编译器使用内存屏障优化，提升吞吐量。

**改进**: 3-5% 吞吐量提升

---

## 3. 并发

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

## 4. 安全

### JEP 451: Prepare to Restrict Dynamic Loading of Agents

**状态**: ⚠️ Deprecated

准备限制代理的动态加载，提升安全性。

**影响**: 使用 `javaagent` 的应用需要评估

---

## 5. JEP 完整列表

| JEP | 标题 | 状态 |
|-----|------|------|
| 448 | JVM Code Heap Segmentation | ✅ |
| 449 | Barrier-Based C2 Compilation | ✅ |
| 451 | Prepare to Restrict Dynamic Loading | ⚠️ |
| 505 | Structured Concurrency | 🔍 |
| 506 | Scoped Values | ✅ |
| 507 | Primitive Types in Patterns | 🔍 |
| 512 | Compact Source Files | 🔍 |

> 图例: ✅ Final | 🔍 Preview | ⚠️ Deprecated
