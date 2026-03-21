# JDK 15

> **发布日期**: 2020-09-15 | **类型**: Feature Release

---
## 目录

1. [核心特性](#1-核心特性)
2. [关键 JEP](#2-关键-jep)
3. [代码示例](#3-代码示例)
4. [移除的功能](#4-移除的功能)
5. [相关链接](#5-相关链接)

---


## 1. 核心特性

JDK 15 引入了 Text Blocks（正式版）、Records（第2次预览）和 Sealed Classes（第1次预览）。

| 特性 | 影响 | 详情 |
|------|------|------|
| **Text Blocks（正式版）** | ⭐⭐⭐⭐⭐ | JEP 378，多行字符串 |
| **Records（第2次预览）** | ⭐⭐⭐⭐⭐ | JEP 384，不可变数据类 |
| **Sealed Classes（第1次预览）** | ⭐⭐⭐⭐ | JEP 360，密封类 |
| **Pattern Matching for instanceof（第2次预览）** | ⭐⭐⭐⭐ | JEP 375 |
| **Hidden Classes** | ⭐⭐⭐ | JEP 371 |
| **ZGC（正式版）** | ⭐⭐⭐⭐ | JEP 377，低延迟 GC |
| **Shenandoah（正式版）** | ⭐⭐⭐⭐ | JEP 379 |
| **Foreign-Memory Access API（第2次孵化）** | ⭐⭐⭐ | JEP 383 |
| **EdDSA** | ⭐⭐⭐ | JEP 339，Edwards 曲线签名 |
| **禁用偏向锁** | ⭐⭐ | JEP 374 |
| **DatagramSocket 重新实现** | ⭐⭐ | JEP 373 |

---

## 2. 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 378](https://openjdk.org/jeps/378) | Text Blocks | 文本块（正式版） |
| [JEP 384](https://openjdk.org/jeps/384) | Records (Second Preview) | Records（第2次预览） |
| [JEP 360](https://openjdk.org/jeps/360) | Sealed Classes (Preview) | 密封类（第1次预览） |
| [JEP 375](https://openjdk.org/jeps/375) | Pattern Matching for instanceof (Second Preview) | instanceof 模式匹配（第2次预览） |
| [JEP 371](https://openjdk.org/jeps/371) | Hidden Classes | 隐藏类 |
| [JEP 372](https://openjdk.org/jeps/372) | Remove the Nashorn JavaScript Engine | 移除 Nashorn |
| [JEP 377](https://openjdk.org/jeps/377) | ZGC: A Scalable Low-Latency Garbage Collector | ZGC（正式版） |
| [JEP 379](https://openjdk.org/jeps/379) | Shenandoah: A Low-Pause-Time Garbage Collector | Shenandoah（正式版） |
| [JEP 383](https://openjdk.org/jeps/383) | Foreign-Memory Access API (Second Incubator) | 外部内存 API |
| [JEP 339](https://openjdk.org/jeps/339) | Edwards-Curve Digital Signature Algorithm (EdDSA) | EdDSA 签名 |
| [JEP 373](https://openjdk.org/jeps/373) | Reimplement the Legacy DatagramSocket API | DatagramSocket 重新实现 |
| [JEP 374](https://openjdk.org/jeps/374) | Disable and Deprecate Biased Locking | 禁用偏向锁 |
| [JEP 385](https://openjdk.org/jeps/385) | Deprecate RMI Activation for Removal | 废弃 RMI Activation |

---

## 3. 代码示例

### Text Blocks（正式版）

```java
String json = """
    {
        "name": "Alice",
        "age": 30
    }
    """;
```

### Sealed Classes（第1次预览）

```java
// JDK 15 (第1次预览)
public sealed interface Shape
    permits Circle, Rectangle, Triangle {
}

public final class Circle implements Shape { }
public final class Rectangle implements Shape { }
public final class Triangle implements Shape { }
```

### Hidden Classes

```java
// 动态生成无法直接访问的类
MethodHandles.Lookup lookup = MethodHandles.lookup();
Class<?> hiddenClass = lookup.defineHiddenClass(bytes, true);
```

---

## 4. 移除的功能

| 功能 | 替代方案 |
|------|----------|
| Nashorn JavaScript 引擎 | GraalJS |
| Solaris/SPARC 端口 | - |

---

## 5. 相关链接

- [发布说明](https://openjdk.org/projects/jdk/15/)
