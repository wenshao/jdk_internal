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
| **2025** | JDK 24 优化 | 继续完善原型 |
| **2026** | JDK 26 Primitive Patterns | 原始类型模式匹配 (JEP 455) |
| **2027+** | 逐步交付 | Primitive Classes 正式版 |

→ [完整时间线](timeline.md)

---

## 当前状态 (2025-2026)

### 已交付特性

| 特性 | 版本 | 状态 |
|------|------|------|
| **Primitive Patterns** | JDK 26 | ✅ 正式版 (JEP 455) |
| **Record Patterns** | JDK 21 | ✅ 正式版 |
| **Unnamed Patterns** | JDK 21 | ✅ 正式版 |

### 开发中特性

| 特性 | JEP | 目标版本 | 状态 |
|------|-----|----------|------|
| **Primitive Classes** | JEP 401 | JDK 27+ | 🔨 开发中 |
| **Unified Generics** | JEP 402 | JDK 28+ | 🔨 开发中 |
| **Value Classes** | - | JDK 27+ | 🔨 原型 |

### 实验性功能

```bash
# 启用值类型原型 (JDK 构建)
--enable-preview -XX:+EnableValhalla

# 注意: 这些是实验性功能，不应用于生产
```

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

### 项目领导

| 贡献者 | 组织 | 角色 |
|--------|------|------|
| [John Rose](/by-contributor/profiles/john-rose.md) | Oracle | 项目创始人、架构师 |
| [David Holmes](/by-contributor/profiles/david-holmes.md) | Oracle | 运行时架构、技术领导 |
| [Brian Goetz](/by-contributor/profiles/brian-goetz.md) | Oracle | Java 语言架构师 |

### JVM 实现

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| [Tobias Hartmann](/by-contributor/profiles/tobias-hartmann.md) | Oracle | C2 JIT 编译器 |
| [Christian Hagedorn](/by-contributor/profiles/christian-hagedorn.md) | Oracle | C2 JIT 编译器 |
| [Stefan Karlsson](/by-contributor/profiles/stefan-karlsson.md) | Oracle | GC、数组 |
| [Vladimir Kozlov](/by-contributor/profiles/vladimir-kozlov.md) | Oracle | C2 编译器优化 |
| [Roman Kennke](/by-contributor/profiles/roman-kennke.md) | Red Hat | JIT 编译、Shenandoah |
| [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | Oracle | 类加载、SA |
| [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | Oracle | 内存管理、测试 |

### 语言特性

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| [Chen Liang](/by-contributor/profiles/chen-liang.md) (liach) | Oracle | javac、语言特性 |
| [Vicente Romero](/by-contributor/profiles/vicente-romero.md) | Oracle | javac 编译器 |
| [David Beaumont](/by-contributor/profiles/david-beaumont.md) | Oracle | javac、构建系统 |
| [Gavin Bierman](/by-contributor/profiles/gavin-bierman.md) | Oracle | 语言规范 |
| [Maurizio Cimadamore](/by-contributor/profiles/maurizio-cimadamore.md) | Oracle | 类型系统 |
| [Jan Lahoda](/by-contributor/profiles/jan-lahoda.md) | Oracle | javac 编译器 |

### 核心库与 JNI

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| [Roger Riggs](/by-contributor/profiles/roger-riggs.md) | Oracle | 核心库、序列化 |
| [Frederic Parain](/by-contributor/profiles/frederic-parain.md) | Oracle | 字段、JNI |
| [Daniel D. Daugherty](/by-contributor/profiles/daniel-daugherty.md) | Oracle | 测试基础设施 |
| [Markus Grönlund](/by-contributor/profiles/markus-gronlund.md) | Oracle | JFR |

### 活跃社区贡献者

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| Quan Anh Mai (merykitty) | Oracle | C2 JIT 编译器 |
| Axel Boldt-Christmas (xmas92) | Oracle | GC、内存屏障 |
| Ivan Walulya (walulyai) | Oracle | 字段布局 |
| Benoît Maillard (benoitmaillard) | Oracle | C2 JIT 编译器 |
| Alex Menkov (alexmenkov) | Oracle | JDWP、JVMTI |
| Marc Chevalier (marc-chevalier) | Oracle | 测试 |

### 历史贡献者

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| [John Rose](/by-contributor/profiles/john-rose.md) | Oracle | 项目创始人 |
| [Aleks Seovic](/by-contributor/profiles/aleks-seovic.md) | - | 早期值类型原型 |
| Srikanth Adayapalam | Oracle | 早期语言设计 |
| Harold Seigel | Oracle | 早期 JVM 实现 |

→ [开发活动详情](development.md)

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

## 当前最佳实践

### 使用原始类型数组

```java
// 推荐: 直接使用原始类型数组
int[] keys = new int[1000];
long[] values = new long[1000];

// 避免: 使用包装类型数组
Integer[] boxedKeys = new Integer[1000];  // 装箱开销
```

### 使用第三方库

```java
// 使用 FastUtil 等高性能集合库
import it.unimi.dsi.fastutil.ints.Int2ObjectMap;
import it.unimi.dsi.fastutil.ints.Int2ObjectOpenHashMap;

Int2ObjectMap<String> map = new Int2ObjectOpenHashMap<>();
// 避免装箱，性能接近 Valhalla 目标
```

### 使用 Record (JDK 16+)

```java
// Record 是迈向值类型的一步
public record Point(int x, int y) {}

// 虽然仍是引用类型，但更紧凑
// 等待 Valhalla 的 inline class
```

---

## 迁移准备

### 代码审查清单

- [ ] 避免过度使用包装类型 (Integer, Long 等)
- [ ] 使用原始类型集合库 (FastUtil, Eclipse Collections)
- [ ] 减少对象创建，重用对象
- [ ] 考虑使用 Record 替代 POJO
- [ ] 关注 Valhalla 进展，准备迁移

### 设计考虑

```java
// 当前设计 - 使用原始类型数组
public class PointCollection {
    private final int[] x;
    private final int[] y;

    public PointCollection(int size) {
        x = new int[size];
        y = new int[size];
    }
}

// 未来 Valhalla 设计
public inline class Point {
    public final int x;
    public final int y;
}

// 直接使用值类型数组
Point[] points = new Point[1000];  // 扁平化存储
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

→ [值类型详解](value-types.md) | [泛型特化详解](generics.md) | [开发活动分析](development.md)
