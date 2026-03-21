# JDK 21 发布说明

> **版本类型**: LTS (长期支持) | **发布日期**: 2023-09-19 | **支持截止**: 2031-10

[![OpenJDK](https://img.shields.io/badge/OpenJDK-21-orange)](https://openjdk.org/projects/jdk/21/)
[![License](https://img.shields.io/badge/License-GPLv2--with--Classpath--Exception-blue)](https://openjdk.org/projects/jdk/21/)

---
## 目录

1. [概述](#1-概述)
2. [语言特性](#2-语言特性)
3. [核心库](#3-核心库)
4. [并发与多线程](#4-并发与多线程)
5. [性能与监控](#5-性能与监控)
6. [安全](#6-安全)
7. [移除与清理](#7-移除与清理)
8. [JEP 汇总](#8-jep-汇总)
9. [相比 JDK 17 的变化](#9-相比-jdk-17-的变化)
10. [升级建议](#10-升级建议)
11. [相关链接](#11-相关链接)

---


## 1. 概述

JDK 21 是一个里程碑式的 LTS 版本，引入了 **Virtual Threads** 正式版，这是 Java 并发编程的重大变革。此外还包含分代 ZGC、Record Patterns、Pattern Matching for switch 等重要特性。

---

## 2. 语言特性

### JEP 444: Virtual Threads (正式版) ⭐⭐⭐

**状态**: 正式发布
**概述**: 虚拟线程正式版，彻底改变 Java 并发编程模型。

```java
// 创建虚拟线程
Thread virtualThread = Thread.ofVirtual().start(() -> {
    System.out.println("Hello from virtual thread");
});

// 使用 ExecutorService
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 10_000).forEach(i -> {
        executor.submit(() -> {
            Thread.sleep(Duration.ofSeconds(1));
            return i;
        });
    });
}  // 自动关闭

// 创建一百万个虚拟线程
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    var futures = IntStream.range(0, 1_000_000)
        .mapToObj(i -> executor.submit(() -> {
            Thread.sleep(Duration.ofSeconds(1));
            return i;
        }))
        .toList();
}
```

**优势**:
- 轻量级：每个虚拟线程只占用几 KB 内存
- 高并发：可以创建数百万个虚拟线程
- 简化编程：使用同步风格编写异步代码
- 兼容性：现有代码无需修改即可受益

---

### JEP 440: Record Patterns (正式版) ⭐

**状态**: 正式发布
**概述**: Record 模式匹配正式版，支持解构 Record。

```java
record Point(int x, int y) {}
record Rectangle(Point upperLeft, Point lowerRight) {}

// instanceof 模式匹配
if (obj instanceof Point(int x, int y)) {
    System.out.println("x=" + x + ", y=" + y);
}

// 嵌套解构
if (obj instanceof Rectangle(Point(int x1, int y1), Point(int x2, int y2))) {
    System.out.println("Rectangle from (" + x1 + "," + y1 + ") to (" + x2 + "," + y2 + ")");
}

// switch 模式匹配
switch (obj) {
    case Point(int x, int y) -> System.out.println("Point at " + x + ", " + y);
    case Rectangle(Point ul, Point lr) -> System.out.println("Rectangle");
    default -> System.out.println("Unknown");
}
```

---

### JEP 441: Pattern Matching for switch (正式版) ⭐

**状态**: 正式发布
**概述**: switch 模式匹配正式版。

```java
static String formatter(Object obj) {
    return switch (obj) {
        case Integer i -> String.format("int %d", i);
        case Long l    -> String.format("long %d", l);
        case Double d  -> String.format("double %f", d);
        case String s  -> String.format("String %s", s);
        default        -> obj.toString();
    };
}

// 带守卫条件
switch (obj) {
    case String s && s.length() > 5 -> "Long string: " + s;
    case String s                   -> "Short string: " + s;
    default                         -> "Not a string";
}
```

---

### JEP 445: Unnamed Classes and Instance Main Methods (预览)

**状态**: 预览
**概述**: 简化 Java 入门体验，无需显式类声明。

```java
// Hello.java - 最简形式
void main() {
    println("Hello, World!");
}
```

---

### JEP 430: String Templates (预览)

**状态**: 预览
**概述**: 字符串模板首次预览。

```java
String name = "World";
String message = STR."Hello, \{name}!";
```

---

## 3. 核心库

### JEP 431: Sequenced Collections ⭐

**状态**: 正式发布
**概述**: 引入新的集合接口，提供统一的顺序访问 API。

```java
interface SequencedCollection<E> extends Collection<E> {
    SequencedCollection<E> reversed();
    void addFirst(E e);
    void addLast(E e);
    E getFirst();
    E getLast();
    E removeFirst();
    E removeLast();
}

// 使用示例
SequencedCollection<String> list = new ArrayList<>(List.of("a", "b", "c"));
list.getFirst();  // "a"
list.getLast();   // "c"
list.addFirst("z");  // ["z", "a", "b", "c"]
list.reversed();  // ["c", "b", "a", "z"]
```

---

### JEP 443: Unnamed Patterns and Variables (预览)

**状态**: 预览
**概述**: 允许使用下划线 `_` 表示不需要的变量或模式。

```java
// 未命名变量
var _ = compute();  // 忽略返回值

// 未命名模式
if (obj instanceof Point(int x, _)) {
    System.out.println("x = " + x);  // 只使用 x，忽略 y
}

// 增强 for 循环
for (var _ : list) {
    // 只关心迭代次数，不关心元素
}
```

---

### JEP 446: Scoped Values (预览)

**状态**: 预览
**概述**: 引入作用域值，替代 ThreadLocal 在虚拟线程场景的使用。

```java
private static final ScopedValue<User> CURRENT_USER = ScopedValue.create();

ScopedValue.where(CURRENT_USER, user).run(() -> {
    // 在此作用域内可访问 CURRENT_USER.get()
    processRequest();
});
```

---

## 4. 并发与多线程

### JEP 453: Structured Concurrency (预览)

**状态**: 预览
**概述**: 结构化并发首次预览，简化多线程编程模型。

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> user = scope.fork(() -> fetchUser());
    Future<List<Order>> orders = scope.fork(() -> fetchOrders());

    scope.join();
    scope.throwIfFailed();

    return new Response(user.resultNow(), orders.resultNow());
}  // 自动关闭，取消未完成的任务
```

---

## 5. 性能与监控

### JEP 439: Generational ZGC (正式版) ⭐⭐

**状态**: 正式发布
**概述**: 分代 ZGC 正式版，显著提升 GC 性能。

```bash
# 启用分代 ZGC
java -XX:+UseZGC -XX:+ZGenerational MyApp
```

**性能数据**:
| 场景 | 非分代 | 分代 ZGC | 改善 |
|------|--------|----------|------|
| 吞吐量下降 | 5-10% | < 5% | **+50%** |
| GC 频率 | 基准 | -50% | **-50%** |
| Pause 时间 | < 1ms | < 1ms | 持平 |

---

### JEP 452: Key Encapsulation Mechanism API

**状态**: 正式发布
**概述**: 提供标准的密钥封装机制 API。

```java
KEM kem = KEM.getInstance("DHKEM");
KEM.Encapsulator encapsulator = kem.newEncapsulator(publicKey);
KEM.Encapsulated encapsulated = encapsulator.encapsulate();
```

---

## 6. 安全

### JEP 451: Prepare to Disallow the Dynamic Loading of Agents

**状态**: 正式发布
**概述**: 准备禁止动态加载代理，增强安全性。

---

## 7. 移除与清理

### JEP 448: Vector API (第六次孵化)

**状态**: 孵化器
**概述**: Vector API 继续孵化，提供 SIMD 向量计算支持。

```java
static final VectorSpecies<Float> SPECIES = FloatVector.SPECIES_256;

void vectorComputation(float[] a, float[] b, float[] c) {
    int i = 0;
    int upperBound = SPECIES.loopBound(a.length);
    for (; i < upperBound; i += SPECIES.length()) {
        var va = FloatVector.fromArray(SPECIES, a, i);
        var vb = FloatVector.fromArray(SPECIES, b, i);
        var vc = va.mul(va).add(vb.mul(vb)).neg();
        vc.intoArray(c, i);
    }
    // 处理剩余元素
}
```

---

### JEP 449: Deprecate the Windows 32-bit x86 Port for Removal

**状态**: 正式发布
**概述**: 废弃 Windows 32位 x86 端口，计划在未来的版本中移除。

---

## 8. JEP 汇总

| JEP | 标题 | 状态 |
|-----|------|------|
| JEP 430 | String Templates (Preview) | 🔍 预览 |
| JEP 431 | Sequenced Collections | ✅ 正式 |
| JEP 439 | Generational ZGC | ✅ 正式 |
| JEP 440 | Record Patterns | ✅ 正式 |
| JEP 441 | Pattern Matching for switch | ✅ 正式 |
| JEP 443 | Unnamed Patterns and Variables (Preview) | 🔍 预览 |
| JEP 444 | Virtual Threads | ✅ 正式 |
| JEP 445 | Unnamed Classes and Instance Main Methods (Preview) | 🔍 预览 |
| JEP 446 | Scoped Values (Preview) | 🔍 预览 |
| JEP 448 | Vector API (Sixth Incubator) | 🥚 孵化 |
| JEP 449 | Deprecate the Windows 32-bit x86 Port for Removal | ✅ 正式 |
| JEP 451 | Prepare to Disallow the Dynamic Loading of Agents | ✅ 正式 |
| JEP 452 | Key Encapsulation Mechanism API | ✅ 正式 |
| JEP 453 | Structured Concurrency (Preview) | 🔍 预览 |

> ✅ 正式 | 🔍 预览 | 🥚 孵化

---

## 9. 相比 JDK 17 的变化

### 新增正式特性

| 特性 | 说明 |
|------|------|
| **Virtual Threads** | 轻量级线程，革命性并发改进 |
| **Record Patterns** | Record 解构模式匹配 |
| **Pattern Matching for switch** | switch 模式匹配 |
| **Sequenced Collections** | 统一的顺序集合 API |
| **分代 ZGC** | 显著提升 GC 性能 |

### 新增预览特性

| 特性 | 说明 |
|------|------|
| String Templates | 字符串模板 |
| Scoped Values | 作用域值 |
| Structured Concurrency | 结构化并发 |
| Unnamed Classes | 未命名类 |
| Unnamed Patterns | 未命名模式 |

---

## 10. 升级建议

### 从 JDK 17 升级

JDK 21 与 JDK 17 具有良好的二进制兼容性：

```bash
# 直接替换 JDK 版本即可
java -version
# openjdk version "21" 2023-09-19
```

### 推荐使用的新特性

| 场景 | 推荐特性 |
|------|----------|
| 高并发 I/O | 虚拟线程 |
| 大内存应用 | 分代 ZGC |
| 数据处理 | Record Patterns |
| 简化代码 | Pattern Matching for switch |

### JVM 参数建议

```bash
# 虚拟线程应用
java -XX:+UseVirtualThreads MyApp

# 大内存应用
java -XX:+UseZGC -XX:+ZGenerational MyApp

# 低延迟场景
java -XX:+UseShenandoahGC MyApp
```

---

## 11. 相关链接

- [OpenJDK JDK 21 项目页面](https://openjdk.org/projects/jdk/21/)
- [JDK 21 JEP 列表](https://openjdk.org/projects/jdk/21/spec/)
- [GitHub: openjdk/jdk](https://github.com/openjdk/jdk)
- [JDK 21 迁移指南](/by-version/jdk21/migration/from-17.md)
