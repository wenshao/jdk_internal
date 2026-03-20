# Project Valhalla

值类型、泛型特化等 JVM 重大演进项目。

[← 返回核心平台](../)

---

## TL;DR

**Project Valhalla** 是 OpenJDK 的长期项目，旨在解决 Java 的两个核心问题：

1. **值类型** - 让用户定义像 `int` 一样高效的值类型，消除对象头开销
2. **泛型特化** - 支持 `List<int>` 原始类型泛型，避免装箱/拆箱

**状态**: 长期开发中 (2014-至今)，预计 JDK 27+ 开始逐步交付

---

## 项目概述

### 解决的问题

| 问题 | 描述 | 影响 |
|------|------|------|
| **对象头开销** | 每个 Java 对象有 12-16 字节对象头 | 内存占用增加 30-50% |
| **引用间接性** | 对象通过引用访问，破坏缓存局部性 | 性能下降 |
| **泛型擦除** | `List<Integer>` 无法优化为 `List<int>` | 装箱开销、内存浪费 |
| **原始类型数组** | `int[]` 和 `Integer[]` 类型不兼容 | API 设计困难 |

### 核心特性

```
┌─────────────────────────────────────────────────────────────┐
│                    Project Valhalla                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐         ┌─────────────────┐            │
│  │  Value Types    │         │ Enhanced Generics│            │
│  │  (值类型)       │         │ (增强泛型)       │            │
│  ├─────────────────┤         ├─────────────────┤            │
│  │ • Inline Classes│         │ • List<int>     │            │
│  │ • Primitive Objects      │ • Primitive Specialization    │
│  │ • L-World        │         │ • Specialized Generics      │
│  └─────────────────┘         └─────────────────┘            │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 值类型 (Value Types)

### Inline Classes

```java
// 值类型示例 (未来语法)
public inline class Point {
    public final int x;
    public final int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }
}

// 编译后行为
Point[] points = new Point[1000];
// 无对象头！每个 Point 只占用 8 字节 (2 个 int)
// 相比普通类节省 ~16 字节/实例
```

### 内存对比

| 类型 | 每实例大小 | 1000万实例内存 |
|------|-----------|---------------|
| `class Point` | 24 字节 (12 头 + 2×4 字段 + 4 填充) | ~240 MB |
| `inline class Point` | 8 字节 (2×4 字段) | ~80 MB |
| `int[2]` | 8 字节 | ~80 MB |

---

## 增强泛型

### 原始类型特化

```java
// 当前: 需要装箱
List<Integer> list = new ArrayList<>();
list.add(42);        // Integer.valueOf(42)
int value = list.get(0);  // list.get(0).intValue()

// 未来: 原始类型特化
List<int> primitives = new ArrayList<>();  // 无装箱!
primitives.add(42);   // 直接存储 int
int value = primitives.get(0);  // 直接返回 int
```

### Any-generics

```java
// T 可以是任何类型，包括原始类型
interface Buffer<T> {
    void add(T value);
    T get(int index);
}

// 使用
Buffer<int> intBuffer = ...;     // 原始类型
Buffer<String> stringBuffer = ...;  // 引用类型
Buffer<Point> pointBuffer = ...;    // 值类型
```

---

## L-World

### 统一对象模型

L-World 是 Valhalla 的底层实现，统一了值类型和引用类型的表示：

| 特性 | 引用类型 | 值类型 (L-World) |
|------|----------|------------------|
| 默认值 | `null` | 类的默认值 (零值) |
| 标识 | 对象标识 | 无标识 (值语义) |
| 比较 | `==` 比较引用 | `==` 比较值 |
| `null` | 可以 | 不可以 |

---

## 时间线

| 年份 | 里程碑 | 说明 |
|------|--------|------|
| **2014** | Project Valhalla 启动 | John Rose 宣布项目 |
| **2015** | Value Types 原型 | JVM 原型实现 |
| **2017** | LW1 (L-World 1) | 统一对象模型设计 |
| **2018** | LW2 | 实验性实现 |
| **2020** | LW3 | 内联类原型 |
| **2021** | Inline Classes (JEP 401) | 进入候选阶段 |
| **2022** | Primitive Classes (JEP 401 更新) | 重命名为 Primitive Classes |
| **2023** | Universal Generics | 泛型特化原型 |
| **2024** | 逐步交付策略 | 分阶段发布计划 |

→ [完整时间线](timeline.md)

---

## JEP 进展

| JEP | 标题 | 状态 | 目标版本 |
|-----|------|------|----------|
| **JEP 401** | Primitive Classes | 持续开发 | JDK 27+ |
| **JEP 402** | Unified Generics | 持续开发 | JDK 28+ |
| **JEP 455** | Primitive Patterns (JDK 26) | ✅ 已交付 | JDK 26 |
| **JEP 218** | Generics over Primitive Types | 早期设计 | - |

---

## 核心贡献者

| 贡献者 | 组织 | 角色 |
|--------|------|------|
| [John Rose](/by-contributor/profiles/john-rose.md) | Oracle | 项目创始人 |
| [Brian Goetz](/by-contributor/profiles/brian-goetz.md) | Oracle | 语言架构师 |
| [Aleks Seovic](/by-contributor/profiles/aleks-seovic.md) | - | 值类型实现 |
| [Tobias Hartmann](/by-contributor/profiles/tobias-hartmann.md) | Oracle | JIT 编译 |
| [Vladimir Kozlov](/by-contributor/profiles/vladimir-kozlov.md) | Oracle | C2 编译器 |

---

## 示例对比

### 当前 Java

```java
// 内存低效
public final class Complex {
    private final double re;
    private final double im;

    public Complex(double re, double im) {
        this.re = re;
        this.im = im;
    }
    // equals, hashCode, toString...
}

// 使用
Complex[] values = new Complex[1000];
// 每个实例: 12(头) + 16(字段) + 4(填充) = 32 字节
// 1000 个实例: 32,000 字节 + 8,000 引用 = 40 KB
```

### Valhalla Inline Classes

```java
// 内存高效
public inline class Complex {
    public final double re;
    public final double im;

    public Complex(double re, double im) {
        this.re = re;
        this.im = im;
    }
}

// 使用
Complex[] values = new Complex[1000];
// 每个实例: 16 字节 (2×double)
// 1000 个实例: 16,000 字节
// 节省: 60% 内存!
```

---

## 相关项目

| 项目 | 关系 |
|------|------|
| **Project Amber** | 语言特性配合 (模式匹配、Records) |
| **Project Loom** | 虚拟线程配合 (减少栈帧开销) |
| **Project Panama** | 外部函数接口配合 |
| **GraalVM** | 值类型 JIT 优化 |

---

## 参考资料

- [Project Valhalla Wiki](https://openjdk.org/projects/valhalla/)
- [JEP 401: Primitive Classes](https://openjdk.org/jeps/401)
- [JEP 402: Unified Generics](https://openjdk.org/jeps/402)
- [Value Types: Reviving Java's Original Ideal](https://cr.openjdk.org/~jrose/papers/valhalla/valhalla-2014-slides.pdf)

→ [值类型详解](value-types.md) | [泛型特化详解](generics.md)
