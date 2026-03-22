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
| **Switch 表达式（正式版）** | ⭐⭐⭐⭐ | [JEP 361](/jeps/language/jep-361.md) |
| **文本块（第2次预览）** | ⭐⭐⭐⭐ | [JEP 368](/jeps/language/jep-368.md) |
| **Packaging Tool（孵化器）** | ⭐⭐⭐ | JEP 343，打包工具 |
| **JFR 事件流** | ⭐⭐⭐ | JEP 349 |
| **Foreign-Memory Access API（孵化器）** | ⭐⭐⭐ | [JEP 370](/jeps/ffi/jep-370.md) |
| **非易失性映射字节缓冲区** | ⭐⭐⭐ | JEP 352 |
| **ZGC on macOS** | ⭐⭐⭐ | [JEP 364](/jeps/platform/jep-364.md) |
| **ZGC on Windows** | ⭐⭐⭐ | [JEP 365](/jeps/platform/jep-365.md) |
| **移除 CMS GC** | ⭐⭐ | [JEP 363](/jeps/gc/jep-363.md) |
| **移除 Pack200** | ⭐⭐ | JEP 367 |

---

## 2. 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 359](/jeps/language/jep-359.md) | Records (Preview) | Records |
| [JEP 305](/jeps/language/jep-305.md) | Pattern Matching for instanceof (Preview) | instanceof 模式匹配 |
| [JEP 358](/jeps/platform/jep-358.md) | Helpful NullPointerExceptions | Helpful NPE |
| [JEP 361](/jeps/language/jep-361.md) | Switch Expressions | Switch 表达式（正式版） |
| [JEP 368](/jeps/language/jep-368.md) | Text Blocks (Second Preview) | 文本块（第2次预览） |
| [JEP 343](/jeps/tools/jep-343.md) | Packaging Tool | 打包工具 |
| [JEP 345](/jeps/gc/jep-345.md) | NUMA-Aware Memory Allocation for G1 | G1 NUMA 感知 |
| [JEP 349](https://openjdk.org/jeps/349) | JFR Event Streaming | JFR 事件流 |
| [JEP 370](/jeps/ffi/jep-370.md) | Foreign-Memory Access API (Incubator) | 外部内存 API |
| [JEP 352](https://openjdk.org/jeps/352) | Non-Volatile Mapped Byte Buffers | 非易失性映射字节缓冲区 |
| [JEP 364](/jeps/platform/jep-364.md) | ZGC on macOS | ZGC macOS 支持 |
| [JEP 365](/jeps/platform/jep-365.md) | ZGC on Windows | ZGC Windows 支持 |
| [JEP 363](/jeps/gc/jep-363.md) | Remove the Concurrent Mark Sweep (CMS) Garbage Collector | 移除 CMS GC |
| [JEP 367](https://openjdk.org/jeps/367) | Remove the Pack200 Tools and API | 移除 Pack200 |
| [JEP 362](/jeps/platform/jep-362.md) | Deprecate the Solaris and SPARC Ports | 废弃 Solaris/SPARC |
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
