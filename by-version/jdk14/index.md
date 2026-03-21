# JDK 14

> **发布日期**: 2020-03-17 | **类型**: Feature Release

---
## 目录

1. [核心特性](#1-核心特性)
2. [关键 JEP](#2-关键-jep)
3. [代码示例](#3-代码示例)
4. [相关链接](#4-相关链接)

---


## 1. 核心特性

JDK 14 引入了 Records（第1次预览）、Pattern Matching for instanceof（第1次预览）和 Helpful NPE。

| 特性 | 影响 | 详情 |
|------|------|------|
| **Records（第1次预览）** | ⭐⭐⭐⭐⭐ | JEP 359，不可变数据类 |
| **Pattern Matching for instanceof（第1次预览）** | ⭐⭐⭐⭐ | JEP 305，模式匹配 |
| **Helpful NPE** | ⭐⭐⭐⭐ | JEP 358，更清晰的空指针异常 |
| **Switch 表达式（正式版）** | ⭐⭐⭐⭐ | JEP 361 |
| **文本块（第2次预览）** | ⭐⭐⭐⭐ | JEP 368 |
| **Packaging Tool（孵化器）** | ⭐⭐⭐ | JEP 343，打包工具 |
| **JFR 事件流** | ⭐⭐⭐ | JEP 349 |
| **Foreign-Memory Access API（孵化器）** | ⭐⭐⭐ | JEP 370 |
| **非易失性映射字节缓冲区** | ⭐⭐⭐ | JEP 352 |
| **ZGC on macOS** | ⭐⭐⭐ | JEP 364 |
| **ZGC on Windows** | ⭐⭐⭐ | JEP 365 |
| **移除 CMS GC** | ⭐⭐ | JEP 363 |
| **移除 Pack200** | ⭐⭐ | JEP 367 |

---

## 2. 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 359](https://openjdk.org/jeps/359) | Records (Preview) | Records |
| [JEP 305](https://openjdk.org/jeps/305) | Pattern Matching for instanceof (Preview) | instanceof 模式匹配 |
| [JEP 358](https://openjdk.org/jeps/358) | Helpful NullPointerExceptions | Helpful NPE |
| [JEP 361](https://openjdk.org/jeps/361) | Switch Expressions | Switch 表达式（正式版） |
| [JEP 368](https://openjdk.org/jeps/368) | Text Blocks (Second Preview) | 文本块（第2次预览） |
| [JEP 343](https://openjdk.org/jeps/343) | Packaging Tool | 打包工具 |
| [JEP 345](https://openjdk.org/jeps/345) | NUMA-Aware Memory Allocation for G1 | G1 NUMA 感知 |
| [JEP 349](https://openjdk.org/jeps/349) | JFR Event Streaming | JFR 事件流 |
| [JEP 370](https://openjdk.org/jeps/370) | Foreign-Memory Access API (Incubator) | 外部内存 API |
| [JEP 352](https://openjdk.org/jeps/352) | Non-Volatile Mapped Byte Buffers | 非易失性映射字节缓冲区 |
| [JEP 364](https://openjdk.org/jeps/364) | ZGC on macOS | ZGC macOS 支持 |
| [JEP 365](https://openjdk.org/jeps/365) | ZGC on Windows | ZGC Windows 支持 |
| [JEP 363](https://openjdk.org/jeps/363) | Remove the Concurrent Mark Sweep (CMS) Garbage Collector | 移除 CMS GC |
| [JEP 367](https://openjdk.org/jeps/367) | Remove the Pack200 Tools and API | 移除 Pack200 |
| [JEP 362](https://openjdk.org/jeps/362) | Deprecate the Solaris and SPARC Ports | 废弃 Solaris/SPARC |
| [JEP 366](https://openjdk.org/jeps/366) | Deprecate the ParallelScavenge + SerialOld GC Combination | 废弃 PS+SerialOld |

---

## 3. 代码示例

### Records（第1次预览）

```java
// 之前
class Point {
    private final int x;
    private final int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() { return x; }
    public int getY() { return y; }

    @Override
    public boolean equals(Object o) { /* ... */ }
    @Override
    public int hashCode() { /* ... */ }
}

// JDK 14 (第1次预览)
record Point(int x, int y) { }
```

### instanceof 模式匹配（第1次预览）

```java
// 之前
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.length());
}

// JDK 14 (第1次预览)
if (obj instanceof String s) {
    System.out.println(s.length());
}
```

### Helpful NPE

```java
// 之前: NullPointerException
// JDK 14: Cannot invoke "String.length()" because "name" is null
String name = null;
name.length();  // 清晰的错误信息
```

---

## 4. 相关链接

- [发布说明](https://openjdk.org/projects/jdk/14/)
