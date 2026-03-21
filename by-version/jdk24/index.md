# JDK 24

> **发布日期**: 2025-03-18 | **类型**: Feature Release

---

## 核心特性

JDK 24 是 JDK 25 LTS 之前的最后一个功能版本，主要完善预览特性。

| 特性 | 影响 | 详情 |
|------|------|------|
| **Primitive Types in Patterns（第2次预览）** | ⭐⭐⭐⭐⭐ | JEP 488 |
| **Simple Source Files（第4次预览）** | ⭐⭐⭐⭐ | JEP 495 |
| **Structured Concurrency（第4次预览）** | ⭐⭐⭐⭐⭐ | JEP 499 |
| **Scoped Values（第4次预览）** | ⭐⭐⭐⭐ | JEP 487 |
| **Class-File API（正式版）** | ⭐⭐⭐⭐ | JEP 484 |
| **Stream Gatherers（正式版）** | ⭐⭐⭐⭐ | JEP 485 |
| **ZGC 移除非分代模式** | ⭐⭐⭐⭐⭐ | JEP 490 |
| **Synchronize Virtual Threads without Pinning** | ⭐⭐⭐⭐ | JEP 491 |

---

## 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 488](https://openjdk.org/jeps/488) | Primitive Types in Patterns (Second Preview) | 原始类型模式匹配（第2次预览） |
| [JEP 495](https://openjdk.org/jeps/495) | Simple Source Files and Instance Main Methods (Fourth Preview) | 简化源文件（第4次预览） |
| [JEP 499](https://openjdk.org/jeps/499) | Structured Concurrency (Fourth Preview) | 结构化并发（第4次预览） |
| [JEP 487](https://openjdk.org/jeps/487) | Scoped Values (Fourth Preview) | 作用域值（第4次预览） |
| [JEP 484](https://openjdk.org/jeps/484) | Class-File API | 类文件 API（正式版） |
| [JEP 485](https://openjdk.org/jeps/485) | Stream Gatherers | Stream 收集器（正式版） |
| [JEP 490](https://openjdk.org/jeps/490) | ZGC: Remove the Non-Generational Mode | ZGC 移除非分代模式 |
| [JEP 491](https://openjdk.org/jeps/491) | Synchronize Virtual Threads without Pinning | 虚拟线程同步优化 |
| [JEP 494](https://openjdk.org/jeps/494) | Module Import Declarations (Second Preview) | 模块导入声明（第2次预览） |
| [JEP 492](https://openjdk.org/jeps/492) | Flexible Constructor Bodies (Third Preview) | 灵活构造器（第3次预览） |
| [JEP 489](https://openjdk.org/jeps/489) | Vector API (Ninth Incubator) | Vector API（第9次孵化） |
| [JEP 478](https://openjdk.org/jeps/478) | Key Derivation Function API (Preview) | 密钥派生函数 API（预览） |
| [JEP 483](https://openjdk.org/jeps/483) | Ahead-of-Time Class Loading & Linking | AOT 类加载和链接 |
| [JEP 486](https://openjdk.org/jeps/486) | Permanently Disable the Security Manager | 永久禁用 Security Manager |
| [JEP 493](https://openjdk.org/jeps/493) | Linking Run-Time Images without JMODs | 无需 JMOD 链接运行时镜像 |
| [JEP 496](https://openjdk.org/jeps/496) | Quantum-Resistant KEM | 量子抗性密钥封装机制 |
| [JEP 497](https://openjdk.org/jeps/497) | Quantum-Resistant Digital Signature | 量子抗性数字签名 |
| [JEP 498](https://openjdk.org/jeps/498) | Warn upon Use of Memory-Access Methods in sun.misc.Unsafe | 警告 Unsafe 内存访问 |
| [JEP 501](https://openjdk.org/jeps/501) | Deprecate the 32-bit x86 Port for Removal | 废弃 32 位 x86 端口 |
| [JEP 479](https://openjdk.org/jeps/479) | Remove the Windows 32-bit x86 Port | 移除 Windows 32 位 x86 端口 |
| [JEP 472](https://openjdk.org/jeps/472) | Prepare to Restrict the Use of JNI | 准备限制 JNI 使用 |
| [JEP 475](https://openjdk.org/jeps/475) | Late Barrier Expansion for G1 | G1 延迟屏障扩展 |
| [JEP 404](https://openjdk.org/jeps/404) | Generational Shenandoah (Experimental) | 分代 Shenandoah（实验性） |
| [JEP 450](https://openjdk.org/jeps/450) | Compact Object Headers (Experimental) | 紧凑对象头（实验性） |

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

### Simple Source Files（第4次预览）

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

### Stream Gatherers（正式版）

```java
// 自定义中间操作
List<Integer> result = Stream.of(1, 2, 3, 4, 5)
    .gather(Gatherers.fold(() -> 0, Integer::sum))
    .toList();
```

### Module Import Declarations（第2次预览）

```java
// 之前
import java.util.List;
import java.util.ArrayList;
import java.util.stream.Collectors;
// ...

// JDK 24 (预览)
import module java.base;
```

---

## 相关链接

- [发布说明](https://openjdk.org/projects/jdk/24/)
