# JDK 16

> **发布日期**: 2021-03-16 | **类型**: Feature Release

---
## 目录

1. [核心特性](#1-核心特性)
2. [关键 JEP](#2-关键-jep)
3. [代码示例](#3-代码示例)
4. [相关链接](#4-相关链接)

---


## 1. 核心特性

JDK 16 引入了 Records（正式版）、Pattern Matching for instanceof（正式版）和 Vector API（孵化器）。

| 特性 | 影响 | 详情 |
|------|------|------|
| **Records（正式版）** | ⭐⭐⭐⭐⭐ | JEP 395，不可变数据类 |
| **Pattern Matching for instanceof（正式版）** | ⭐⭐⭐⭐⭐ | JEP 394，模式匹配 |
| **Vector API（孵化器）** | ⭐⭐⭐⭐ | JEP 338，SIMD 编程 |
| **Foreign Linker API（孵化器）** | ⭐⭐⭐⭐ | JEP 389，原生互连 |
| **Unix Domain Sockets** | ⭐⭐⭐ | [JEP 380](/jeps/network/jep-380.md) |
| **Warnings for Value-Based Classes** | ⭐⭐⭐ | [JEP 390](/jeps/language/jep-390.md) |
| **弹性元空间** | ⭐⭐⭐ | [JEP 387](/jeps/performance/jep-387.md) |
| **ZGC 并发线程栈处理** | ⭐⭐⭐ | JEP 376 |
| **Foreign-Memory Access API（第3次孵化）** | ⭐⭐⭐ | [JEP 393](/jeps/ffi/jep-393.md) |
| **Alpine Linux 端口** | ⭐⭐ | [JEP 386](/jeps/platform/jep-386.md) |
| **Windows/AArch64 端口** | ⭐⭐ | [JEP 388](/jeps/platform/jep-388.md) |
| **Sealed Classes（第2次预览）** | ⭐⭐⭐⭐ | [JEP 397](/jeps/language/jep-397.md) |

---

## 2. 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 395](/jeps/language/jep-395.md) | Records | Records（正式版） |
| [JEP 394](/jeps/language/jep-394.md) | Pattern Matching for instanceof | instanceof 模式匹配（正式版） |
| [JEP 338](/jeps/language/jep-338.md) | Vector API (Incubator) | Vector API |
| [JEP 380](/jeps/network/jep-380.md) | Unix Domain Sockets | Unix 域套接字 |
| [JEP 390](/jeps/language/jep-390.md) | Warnings for Value-Based Classes | 值类警告 |
| [JEP 387](/jeps/performance/jep-387.md) | Elastic Metaspace | 弹性元空间 |
| [JEP 393](/jeps/ffi/jep-393.md) | Foreign-Memory Access API (Third Incubator) | 外部内存 API |
| [JEP 392](/jeps/tools/jep-392.md) | Packaging Tool | 打包工具 |
| [JEP 396](/jeps/language/jep-396.md) | Strongly Encapsulate JDK Internals | 强封装 JDK 内部 |
| [JEP 397](/jeps/language/jep-397.md) | Sealed Classes (Second Preview) | 密封类（第2次预览） |
| [JEP 389](/jeps/ffi/jep-389.md) | Foreign Linker API (Incubator) | 外部链接器 API |
| [JEP 376](https://openjdk.org/jeps/376) | ZGC: Concurrent Thread-Stack Processing | ZGC 并发线程栈处理 |
| [JEP 388](/jeps/platform/jep-388.md) | Windows/AArch64 Port | Windows ARM64 |
| [JEP 386](/jeps/platform/jep-386.md) | Alpine Linux Port | Alpine Linux |
| [JEP 347](https://openjdk.org/jeps/347) | Enable C++14 Language Features | 启用 C++14 |
| [JEP 369](https://openjdk.org/jeps/369) | Migrate to GitHub | 迁移到 GitHub |

---

## 3. 代码示例

### Records（正式版）

```java
// 正式版
record Point(int x, int y) { }

// 带验证
record Range(int min, int max) {
    public Range {
        if (min > max)
            throw new IllegalArgumentException();
    }
}
```

### instanceof 模式匹配（正式版）

```java
// 正式版
if (obj instanceof String s) {
    System.out.println(s.length());
}

// 与条件结合
if (obj instanceof String s && s.length() > 5) {
    System.out.println("Long string: " + s);
}
```

### Vector API

```java
import jdk.incubator.vector.*;

static final VectorSpecies<Float> SPECIES = FloatVector.SPECIES_256;

void vectorComputation(float[] a, float[] b, float[] c) {
    int i = 0;
    int upperBound = SPECIES.loopBound(a.length);
    for (; i < upperBound; i += SPECIES.length()) {
        FloatVector va = FloatVector.fromArray(SPECIES, a, i);
        FloatVector vb = FloatVector.fromArray(SPECIES, b, i);
        FloatVector vc = va.mul(va).add(vb.mul(vb));
        vc.intoArray(c, i);
    }
}
```

---

## 4. 相关链接

- [发布说明](https://openjdk.org/projects/jdk/16/)
