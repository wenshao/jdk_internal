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
| **Unix Domain Sockets** | ⭐⭐⭐ | JEP 380 |
| **Warnings for Value-Based Classes** | ⭐⭐⭐ | JEP 390 |
| **弹性元空间** | ⭐⭐⭐ | JEP 387 |
| **ZGC 并发线程栈处理** | ⭐⭐⭐ | JEP 376 |
| **Foreign-Memory Access API（第3次孵化）** | ⭐⭐⭐ | JEP 393 |
| **Alpine Linux 端口** | ⭐⭐ | JEP 386 |
| **Windows/AArch64 端口** | ⭐⭐ | JEP 388 |
| **Sealed Classes（第2次预览）** | ⭐⭐⭐⭐ | JEP 397 |

---

## 2. 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 395](https://openjdk.org/jeps/395) | Records | Records（正式版） |
| [JEP 394](https://openjdk.org/jeps/394) | Pattern Matching for instanceof | instanceof 模式匹配（正式版） |
| [JEP 338](https://openjdk.org/jeps/338) | Vector API (Incubator) | Vector API |
| [JEP 380](https://openjdk.org/jeps/380) | Unix Domain Sockets | Unix 域套接字 |
| [JEP 390](https://openjdk.org/jeps/390) | Warnings for Value-Based Classes | 值类警告 |
| [JEP 387](https://openjdk.org/jeps/387) | Elastic Metaspace | 弹性元空间 |
| [JEP 393](https://openjdk.org/jeps/393) | Foreign-Memory Access API (Second Incubator) | 外部内存 API |
| [JEP 392](https://openjdk.org/jeps/392) | Packaging Tool | 打包工具 |
| [JEP 396](https://openjdk.org/jeps/396) | Strongly Encapsulate JDK Internals | 强封装 JDK 内部 |
| [JEP 397](https://openjdk.org/jeps/397) | Sealed Classes (Second Preview) | 密封类（第2次预览） |
| [JEP 389](https://openjdk.org/jeps/389) | Foreign Linker API (Incubator) | 外部链接器 API |
| [JEP 376](https://openjdk.org/jeps/376) | ZGC: Concurrent Thread-Stack Processing | ZGC 并发线程栈处理 |
| [JEP 388](https://openjdk.org/jeps/388) | Windows/AArch64 Port | Windows ARM64 |
| [JEP 386](https://openjdk.org/jeps/386) | Alpine Linux Port | Alpine Linux |
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
