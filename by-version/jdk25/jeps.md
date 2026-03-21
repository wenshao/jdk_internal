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

### JEP 454: Foreign Function & Memory API (正式版)

**状态**: ✅ Final

FFM API 允许 Java 代码安全地与本地代码和内存交互。

```java
import java.lang.foreign.*;

// 分配本地内存
try (Arena arena = Arena.ofConfined()) {
    MemorySegment segment = arena.allocate(100);
    segment.set(ValueLayout.JAVA_INT, 0, 42);
}

// 调用本地函数
Linker linker = Linker.nativeLinker();
SymbolLookup stdlib = linker.defaultLookup();
MethodHandle strlen = linker.downcallHandle(
    stdlib.find("strlen").get(),
    FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
);
```

**相关**: [JEP 文档](https://openjdk.org/jeps/454)

---

## 2. 性能

### JEP 468: Generational ZGC

**状态**: ✅ Final

分代 ZGC 将堆分为年轻代和老年代，大幅降低 GC 开销。

| 指标 | 改进 |
|------|------|
| GC 开销 | -50% |
| 吞吐量 | +10-20% |
| 堆占用 | -30% |

```bash
# 启用分代 ZGC
java -XX:+UseZGC -XX:+ZGenerational MyApp
```

**相关**: [JEP 文档](https://openjdk.org/jeps/468)

---

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

### JEP 462: Structured Concurrency (第五次预览)

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

**相关**: [JEP 文档](https://openjdk.org/jeps/462)

---

### JEP 467: Scoped Values (第三次预览)

**状态**: 🔍 Preview

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

**相关**: [JEP 文档](https://openjdk.org/jeps/467)

---

### JEP 444: Virtual Threads (正式版)

**状态**: ✅ Final

虚拟线程正式版，轻量级线程实现。

```java
// 创建虚拟线程
Thread vthread = Thread.ofVirtual().start(() -> {
    System.out.println("Hello from virtual thread");
});

// 使用 ExecutorService
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1000; i++) {
        executor.submit(() -> {
            // 任务
        });
    }
}
```

**相关**: [JEP 文档](https://openjdk.org/jeps/444)

---

## 4. 安全

### JEP 452: Key Encapsulation Mechanism API

**状态**: ✅ Final

KEM API 提供密钥封装机制的标准接口。

```java
import javax.crypto.KEM;

// 发送方
KEM kem = KEM.getInstance("DHKEM");
KEM.Encapsulator enc = kem.newEncapsulator(receiverPublicKey);
KEM.Encapsulated encap = enc.encapsulate();
byte[] ciphertext = encap.encapsulation();
SecretKey sharedKey = encap.key();

// 接收方
KEM.Decapsulator dec = kem.newDecapsulator(receiverPrivateKey);
SecretKey sharedKey = dec.decapsulate(ciphertext);
```

**相关**: [JEP 文档](https://openjdk.org/jeps/452)

---

### JEP 451: Prepare to Restrict Dynamic Loading of Agents

**状态**: ⚠️ Deprecated

准备限制代理的动态加载，提升安全性。

**影响**: 使用 `javaagent` 的应用需要评估

---

## 5. JEP 完整列表

| JEP | 标题 | 状态 |
|-----|------|------|
| 430 | String Templates | ✅ |
| 444 | Virtual Threads | ✅ |
| 448 | JVM Code Heap Segmentation | ✅ |
| 449 | Barrier-Based C2 Compilation | ✅ |
| 451 | Prepare to Restrict Dynamic Loading | ⚠️ |
| 452 | Key Encapsulation Mechanism API | ✅ |
| 454 | Foreign Function & Memory API | ✅ |
| 507 | Primitive Types in Patterns | 🔍 |
| 462 | Structured Concurrency | 🔍 |
| 466 | Class-File API | 🔍 |
| 467 | Scoped Values | 🔍 |
| 468 | Generational ZGC | ✅ |
| 469 | Implicit Classes and Instance Main Methods | 🔍 |

> 图例: ✅ Final | 🔍 Preview | ⚠️ Deprecated
