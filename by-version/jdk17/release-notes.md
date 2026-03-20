# JDK 17 发布说明

> **版本类型**: LTS (长期支持) | **发布日期**: 2021-09-14 | **支持截止**: 2029-10

[![OpenJDK](https://img.shields.io/badge/OpenJDK-17-orange)](https://openjdk.org/projects/jdk/17/)
[![License](https://img.shields.io/badge/License-GPLv2--with--Classpath--Exception-blue)](https://openjdk.org/projects/jdk/17/)

---

## 概述

JDK 17 是一个重要的 LTS 版本，引入了 **Records** 和 **Sealed Classes** 正式版，以及 **Pattern Matching for instanceof** 正式版。这些特性显著提升了 Java 的表达能力和类型安全性。

---

## 语言特性

### JEP 409: Sealed Classes (正式版) ⭐⭐

**状态**: 正式发布
**概述**: 密封类正式版，允许控制类的继承层次。

```java
// 密封接口
public sealed interface Shape
    permits Circle, Rectangle, Square { }

// 允许的实现类
public final class Circle implements Shape {
    private final double radius;
    // ...
}

public final class Rectangle implements Shape {
    private final double length, width;
    // ...
}

public non-sealed class Square implements Shape {
    // non-sealed 允许进一步继承
}
```

**优势**:
- 类型安全的代数数据类型
- 编译时检查继承关系
- 支持模式匹配的穷尽性检查

---

### JEP 395: Records (正式版) ⭐⭐

**状态**: 正式发布
**概述**: Record 正式版，简化数据载体类的定义。

```java
// 定义 Record
public record Person(String name, int age) {
    // 自动生成：
    // - 构造函数
    // - name() 和 age() 访问器
    // - equals(), hashCode(), toString()
}

// 使用 Record
Person person = new Person("Alice", 30);
System.out.println(person.name());  // Alice
System.out.println(person.age());   // 30

// Record 可以实现接口
public record Point(int x, int y) implements Comparable<Point> {
    @Override
    public int compareTo(Point other) {
        return Integer.compare(x + y, other.x + other.y);
    }
}

// 紧凑构造函数
public record Range(int min, int max) {
    public Range {
        if (min > max) {
            throw new IllegalArgumentException("min > max");
        }
    }
}
```

---

### JEP 394: Pattern Matching for instanceof (正式版) ⭐

**状态**: 正式发布
**概述**: instanceof 模式匹配正式版。

```java
// 之前
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.length());
}

// 现在
if (obj instanceof String s) {
    System.out.println(s.length());
}

// 带条件
if (obj instanceof String s && s.length() > 5) {
    System.out.println("Long string: " + s);
}
```

---

### JEP 406: Pattern Matching for switch (预览)

**状态**: 预览
**概述**: switch 模式匹配首次预览。

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
```

---

## 核心库

### JEP 306: Restore Always-Strict Floating-Point Semantics

**状态**: 正式发布
**概述**: 恢复严格的浮点语义，确保跨平台的一致性。

---

### JEP 382: New macOS Rendering Pipeline

**状态**: 正式发布
**概述**: 使用 Apple Metal 的新 macOS 渲染管道。

---

### JEP 415: Context-Specific Deserialization Filters

**状态**: 正式发布
**概述**: 上下文特定的反序列化过滤器，增强安全性。

```java
// 配置全局过滤器
ObjectInputFilter.Config.setSerialFilter(filter);

// 为特定流设置过滤器
ObjectInputStream ois = new ObjectInputStream(inputStream);
ois.setObjectInputFilter(filter);
```

---

## 性能与监控

### JEP 376: ZGC: Concurrent Thread-Stack Processing

**状态**: 正式发布
**概述**: ZGC 并发线程栈处理，降低 GC 停顿时间。

---

### JEP 411: Deprecate the Security Manager for Removal

**状态**: 正式发布
**概述**: 废弃 Security Manager，计划在未来的版本中移除。

---

## 安全

### JEP 412: Foreign Function & Memory API (孵化器)

**状态**: 孵化器
**概述**: 外部函数和内存 API 首次孵化。

```java
// 分配外部内存
MemorySegment segment = MemorySegment.allocateNative(100);

// 调用外部函数
Linker linker = Linker.getInstance();
MethodHandle strlen = linker.downcallHandle(
    SymbolLookup.loaderLookup().find("strlen").get(),
    FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
);
```

---

## 移除与清理

### JEP 398: Deprecate the Applet API for Removal

**状态**: 正式发布
**概述**: 废弃 Applet API，计划在未来的版本中移除。

---

### JEP 407: Remove RMI Activation

**状态**: 正式发布
**概述**: 移除 RMI 激活机制。

---

### JEP 410: Remove the Experimental AOT and JIT Compiler

**状态**: 正式发布
**概述**: 移除实验性的 AOT 和 JIT 编译器。

---

## 工具

### JEP 383: macOS/AArch64 Port

**状态**: 正式发布
**概述**: 支持 macOS AArch64 (Apple Silicon) 平台。

---

### JEP 392: Packaging Tool (正式版)

**状态**: 正式发布
**概述**: jpackage 打包工具正式版。

```bash
# 打包为原生安装包
jpackage --name MyApp --input input --main-jar app.jar --main-class com.example.Main

# 生成平台特定的安装包
# Windows: .exe 或 .msi
# macOS: .dmg 或 .pkg
# Linux: .deb 或 .rpm
```

---

### JEP 356: Enhanced Pseudo-Random Number Generators

**状态**: 正式发布
**概述**: 增强的伪随机数生成器。

```java
// 使用新的随机数生成器接口
RandomGeneratorFactory<RandomGenerator> factory = RandomGeneratorFactory.of("L32X64MixRandom");
RandomGenerator random = factory.create();

// 可用的算法
RandomGeneratorFactory.all()
    .map(RandomGeneratorFactory::name)
    .forEach(System.out::println);
// 输出: L32X64MixRandom, L64X128MixRandom, Xoroshiro128PlusPlus, ...
```

---

## JEP 汇总

| 类别 | JEP | 标题 | 状态 |
|------|-----|------|------|
| **语言** | JEP 409 | Sealed Classes | ✅ 正式 |
| | JEP 395 | Records | ✅ 正式 |
| | JEP 394 | Pattern Matching for instanceof | ✅ 正式 |
| | JEP 406 | Pattern Matching for switch | 🔍 预览 |
| **核心库** | JEP 306 | Always-Strict Floating-Point | ✅ 正式 |
| | JEP 382 | macOS Rendering Pipeline | ✅ 正式 |
| | JEP 415 | Deserialization Filters | ✅ 正式 |
| | JEP 356 | Enhanced PRNG | ✅ 正式 |
| **性能** | JEP 376 | ZGC Concurrent Thread-Stack | ✅ 正式 |
| **安全** | JEP 411 | Deprecate Security Manager | ✅ 正式 |
| | JEP 412 | Foreign Function & Memory | 🥚 孵化 |
| **移除** | JEP 398 | Deprecate Applet API | ✅ 正式 |
| | JEP 407 | Remove RMI Activation | ✅ 正式 |
| | JEP 410 | Remove AOT/JIT | ✅ 正式 |
| **工具** | JEP 383 | macOS/AArch64 Port | ✅ 正式 |
| | JEP 392 | Packaging Tool | ✅ 正式 |

> ✅ 正式版 | 🔍 预览版 | 🥚 孵化器

---

## 相比 JDK 11 的新特性

### 新增正式特性

| 特性 | 说明 |
|------|------|
| **Sealed Classes** | 控制类的继承层次 |
| **Records** | 简化数据载体类 |
| **Pattern Matching for instanceof** | 简化类型检查和转换 |
| **macOS/AArch64** | Apple Silicon 支持 |
| **jpackage** | 原生打包工具 |
| **Enhanced PRNG** | 增强的随机数生成器 |

### 新增预览/孵化特性

| 特性 | 说明 |
|------|------|
| Pattern Matching for switch | switch 模式匹配 |
| Foreign Function & Memory | 外部函数和内存 API |

---

## 升级建议

### 从 JDK 11 升级

JDK 17 与 JDK 11 具有良好的二进制兼容性：

```bash
# 直接替换 JDK 版本即可
java -version
# openjdk version "17" 2021-09-14
```

### 破坏性变更

| 变更 | 影响 | 建议 |
|------|------|------|
| Security Manager 废弃 | 使用 Security Manager 的应用 | 迁移到现代安全框架 |
| RMI Activation 移除 | 使用 RMI 激活的应用 | 使用其他分布式技术 |
| Applet API 废弃 | 使用 Applet 的应用 | 迁移到现代 Web 技术 |

### 推荐使用的新特性

| 场景 | 推荐特性 |
|------|----------|
| 数据建模 | Records |
| 类型安全 | Sealed Classes |
| 类型检查 | Pattern Matching for instanceof |
| 打包分发 | jpackage |

---

## 相关链接

- [OpenJDK JDK 17 项目页面](https://openjdk.org/projects/jdk/17/)
- [JDK 17 JEP 列表](https://openjdk.org/projects/jdk/17/spec/)
- [GitHub: openjdk/jdk](https://github.com/openjdk/jdk)
- [JDK 17 迁移指南](/by-version/jdk17/migration/from-11.md)
