# JDK 26 发布说明

> 基于 openjdk/jdk 仓库标签 `jdk-26+26` 分析

## 1. 概述

JDK 26 包含 **23 个 JEP**（JDK Enhancement Proposals），涵盖语言特性、API、性能优化、垃圾回收等多个领域。

---
## 目录

1. [概述](#1-概述)
2. [语言特性](#2-语言特性)
3. [核心库](#3-核心库)
4. [并发与多线程](#4-并发与多线程)
5. [性能与监控](#5-性能与监控)
6. [垃圾回收](#6-垃圾回收)
7. [网络](#7-网络)
8. [安全](#8-安全)
9. [移除与清理](#9-移除与清理)
10. [快速导航](#10-快速导航)
11. [相关链接](#11-相关链接)

---


## 2. 语言特性

### [JEP 511: Module Import Declarations](/jeps/language/jep-511.md) ⭐

**状态**: 正式发布  
**概述**: 允许使用 `import module <name>` 导入整个模块的所有导出包。

```java
import module java.base;  // 一行替代多个 import

void main() {
    List<String> list = new ArrayList<>();  // 直接使用
}
```

---

### [JEP 512: Compact Source Files and Instance Main Methods](/jeps/language/jep-512.md) ⭐

**状态**: 正式发布  
**概述**: 进一步简化 Java 入门体验，无需显式类声明。

```java
// Hello.java - 最简形式
void main() {
    println("Hello, World!");
}
```

---

### [JEP 530: Primitive Types in Patterns](/jeps/concurrency/jep-530.md)

**状态**: 第四次预览  
**概述**: 允许在模式匹配中使用原始类型。

```java
switch (value) {
    case int i -> System.out.println("int: " + i);
    case long l -> System.out.println("long: " + l);
    case double d -> System.out.println("double: " + d);
}
```

---

### [JEP 526: Lazy Constants](/jeps/concurrency/jep-526.md)

**状态**: 第二次预览  
**概述**: 引入延迟初始化的常量声明。

```java
private static lazy ExpensiveObject CACHE = new ExpensiveObject();
```

---

## 3. 核心库

### [JEP 502: Stable Values (Preview)](/jeps/performance/jep-502.md) ⭐

**状态**: 预览  
**概述**: 引入 `StableValue<T>` 类型，提供线程安全的一次写入语义。

```java
private final StableValue<Logger> logger = StableValue.of();

public Logger getLogger() {
    return logger.orElseSet(() -> Logger.getLogger("MyApp"));
}
```

---

### [JEP 506: Scoped Values](/jeps/concurrency/jep-506.md)

**状态**: 正式发布  
**概述**: Scoped Values 正式发布，提供线程局部变量的替代方案。

```java
private static final ScopedValue<User> CURRENT_USER = ScopedValue.create();

ScopedValue.where(CURRENT_USER, user).run(() -> {
    // 在此作用域内可访问 CURRENT_USER.get()
});
```

---

### [JEP 510: Key Derivation Function API](/jeps/security/jep-510.md)

**状态**: 正式发布  
**概述**: 提供标准化的密钥派生函数 (KDF) API。

```java
KDF kdf = KDF.getInstance("HKDF");
SecretKey key = kdf.deriveKey("HKDF-SHA256", params);
```

---

## 4. 并发与多线程

### [JEP 525: Structured Concurrency](/jeps/concurrency/jep-525.md)

**状态**: 第六次预览  
**概述**: 结构化并发继续预览，简化多线程编程模型。

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> user = scope.fork(() -> fetchUser());
    Future<Integer> order = scope.fork(() -> fetchOrder());
    scope.join();
    scope.throwIfFailed();
    return new Response(user.resultNow(), order.resultNow());
}
```

---

## 5. 性能与监控

### [JEP 509: JFR CPU-Time Profiling](/jeps/jfr/jep-509.md)

**状态**: 正式发布  
**概述**: JFR 支持 CPU 时间采样，提供更准确的性能分析数据。

---

### [JEP 514: AOT Command Line Ergonomics](/jeps/performance/jep-514.md)

**状态**: 正式发布  
**概述**: 改进 AOT 缓存的命令行参数处理，优化启动性能。

---

### [JEP 515: AOT Method Profiling](/jeps/performance/jep-515.md)

**状态**: 正式发布  
**概述**: 支持在 AOT 阶段收集方法分析数据，优化 JIT 编译决策。

---

### [JEP 518: JFR Cooperative Sampling](/jeps/jfr/jep-518.md)

**状态**: 正式发布  
**概述**: JFR 协作式采样，减少采样开销，提高准确性。

---

### [JEP 519: Compact Object Headers](/jeps/gc/jep-519.md)

**状态**: 正式发布  
**概述**: 压缩对象头，减少内存占用，提高缓存效率。

---

### [JEP 520: JFR Method Timing and Tracing](/jeps/jfr/jep-520.md)

**状态**: 正式发布  
**概述**: JFR 方法级计时和追踪，提供细粒度的性能分析能力。

---

## 6. 垃圾回收

### [JEP 521: Generational Shenandoah](/jeps/gc/jep-521.md)

**状态**: 正式发布  
**概述**: Shenandoah GC 支持分代模式，提升年轻代对象的处理效率。

---

### [JEP 522: G1 GC Throughput Improvement](/jeps/gc/jep-522.md) ⭐

**状态**: 正式发布  
**概述**: 优化 G1 GC 的同步机制，提升吞吐量 10-15%。

---

## 7. 网络

### [JEP 517: HTTP/3 for the HTTP Client API](/jeps/network/jep-517.md) ⭐

**状态**: 正式发布  
**概述**: HTTP Client API 正式支持 HTTP/3 (QUIC) 协议。

```java
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3)
    .build();
```

---

## 8. 安全

### [JEP 470: PEM Encodings](/jeps/security/jep-470.md)

**状态**: 预览  
**概述**: 支持 PEM 格式的加密对象编码/解码。

```java
PEMEncoder encoder = new PEMEncoder();
String pem = encoder.encode(privateKey);
```

---

### JEP 524: PEM Encodings (Second Preview)

**状态**: 第二次预览  
**概述**: JEP 470 的第二次预览，根据反馈进行改进。

---

## 9. 移除与清理

### [JEP 503: Remove the 32-bit x86 Port](/jeps/performance/jep-503.md)

**状态**: 正式移除  
**概述**: 正式移除 32位 x86 平台支持，删除 29,729 行代码。

---

### [JEP 504: Remove the Applet API](/jeps/performance/jep-504.md)

**状态**: 正式移除  
**概述**: 正式移除已废弃的 Applet API，包括 `java.applet` 包。

---

### [JEP 500: Prepare to Make Final Mean Final](/jeps/removed/jep-500.md)

**状态**: 正式发布  
**概述**: 为最终字段提供更强的不可变性保证，限制通过反射和 JNI 修改 final 字段。

---

## 10. 快速导航

| 类别 | JEP 数量 | 亮点 |
|------|----------|------|
| 语言特性 | 4 | 模块导入、紧凑源文件、原始类型模式、延迟常量 |
| 核心库 | 3 | StableValue、Scoped Values、KDF API |
| 并发 | 1 | 结构化并发 |
| 性能监控 | 6 | JFR 增强、AOT 优化、紧凑对象头 |
| 垃圾回收 | 2 | 分代 Shenandoah、G1 优化 |
| 网络 | 1 | HTTP/3 |
| 安全 | 2 | PEM 编码 |
| 移除 | 3 | 32位 x86、Applet API、Final 限制 |

---

## 11. 相关链接

- [OpenJDK JDK 26 项目页面](https://openjdk.org/projects/jdk/26/)
- [JDK 26 JEP 列表](https://openjdk.org/projects/jdk/26/spec/)
- [GitHub: openjdk/jdk](https://github.com/openjdk/jdk)