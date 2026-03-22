# Project Valhalla

值类型、泛型特化等 JVM 重大演进项目。

[← 返回核心平台](../)

---
## 目录

1. [核心文档](#1-核心文档)
2. [TL;DR](#2-tldr)
3. [项目概述与目标](#3-项目概述与目标)
4. [Value Classes (JEP 401, JDK 26 Preview)](#4-value-classes-jep-401-jdk-26-preview)
5. [Unified Generics (JEP 402, 草案)](#5-unified-generics-jep-402-草案)
6. [Compact Object Headers (JEP 519)](#6-compact-object-headers-jep-519)
7. [L-World](#7-l-world)
8. [性能影响预估](#8-性能影响预估)
9. [时间线与现状 (2014-2026)](#9-时间线与现状-2014-2026)
10. [JEP 进展](#10-jep-进展)
11. [迁移准备](#11-迁移准备)
12. [核心贡献者](#12-核心贡献者)
13. [示例对比](#13-示例对比)
14. [当前最佳实践](#14-当前最佳实践)
15. [相关项目](#15-相关项目)
16. [参考资料](#16-参考资料)

---


## 1. 核心文档

- **[架构与源码分析](architecture.md)** - 分层架构、核心类分析、C2 优化、字段布局
- **[值类型详解](value-types.md)** - Inline Classes、L-World、内存布局
- **[泛型特化详解](generics.md)** - 原始类型泛型、Any-generics
- **[时间线](timeline.md)** - 2014-2026 完整发展历程
- **[开发活动分析](development.md)** - GitHub PR 分析、贡献者统计

---

## 2. TL;DR

**Project Valhalla** 是 OpenJDK 的长期项目，旨在解决 Java 的两个核心问题：

1. **值类型** - 让用户定义像 `int` 一样高效的值类型，消除对象头开销
2. **泛型特化** - 支持 `List<int>` 原始类型泛型，避免装箱/拆箱

**核心口号**: **"Codes like a class, works like an int"** — 写起来像类，跑起来像 int

**状态**: 长期开发中 (2014-至今)，JEP 401 (Value Classes) 在 JDK 26 首次预览

---

## 3. 项目概述与目标

### "Codes like a class, works like an int"

Project Valhalla 的核心目标可以用一句话概括：**消除原始类型 (primitive types) 和引用类型 (reference types) 之间的鸿沟**。

在当前 Java 中，类型系统存在一道根本性的裂缝：

```
┌─────────────────────────────────────────────────────────────────┐
│                  Java 类型系统的"大裂缝"                         │
├─────────────────────────────┬───────────────────────────────────┤
│     原始类型 (Primitives)    │      引用类型 (References)        │
├─────────────────────────────┼───────────────────────────────────┤
│ int, long, double, ...      │ Integer, String, Object, ...     │
│ 栈分配，无对象头              │ 堆分配，有 12-16 字节对象头        │
│ 值语义 (== 比较值)           │ 引用语义 (== 比较引用)             │
│ 不能做泛型参数                │ 可以做泛型参数                    │
│ 不能为 null                 │ 可以为 null                       │
│ 8 种固定类型                 │ 用户可定义                        │
│ 高性能                      │ 灵活但有开销                      │
└─────────────────────────────┴───────────────────────────────────┘
```

这道裂缝意味着：你要么选择性能 (原始类型)，要么选择抽象 (引用类型)，不能兼得。Valhalla 的目标就是让用户定义**新的值类型**——它们写起来像普通的 class，但在运行时像 int 一样高效。

### 解决的问题

| 问题 | 描述 | 影响 |
|------|------|------|
| **对象头开销** | 每个 Java 对象有 12-16 字节对象头 (mark word + klass pointer) | 小对象内存占用增加 30-50% |
| **引用间接性** | 对象通过引用访问，每次访问需指针解引用 | CPU 缓存未命中 (cache miss)，性能下降 |
| **泛型擦除** | `List<Integer>` 无法优化为 `List<int>` | 装箱开销、内存浪费 |
| **原始/引用割裂** | `int[]` 和 `Integer[]` 类型不兼容 | API 设计困难，需要为每种原始类型写特化方法 |

### Valhalla 三大支柱

```
┌─────────────────────────────────────────────────────────────────┐
│                     Project Valhalla                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│  │  Value Classes   │  │ Unified Generics │  │ Null Restriction│ │
│  │  (JEP 401)       │  │ (JEP 402)        │  │                │ │
│  ├──────────────────┤  ├──────────────────┤  ├────────────────┤ │
│  │ • value class    │  │ • List<int>      │  │ • 非 null 值类  │ │
│  │ • 无 identity    │  │ • 泛型特化       │  │ • ! 后缀标记    │ │
│  │ • 扁平化存储     │  │ • 消除装箱       │  │ • 默认值语义    │ │
│  └──────────────────┘  └──────────────────┘  └────────────────┘ │
│                                                                   │
│  JDK 26 Preview ──────── 草案阶段 ──────── 与 JEP 401 一起       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Value Classes (JEP 401, JDK 26 Preview)

Value Classes 是 Valhalla 第一个正式进入预览的特性，在 JDK 26 (2026-03-17 GA) 中以 Preview 形式发布。

### 4.1 value class 语法和语义

使用 `value` 修饰符声明一个值类：

```java
// value class 基本语法 (JDK 26+, --enable-preview)
public value class Point {
    int x;  // 字段隐式 final — 值类中所有实例字段自动为 final
    int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public double distanceTo(Point other) {
        double dx = this.x - other.x;
        double dy = this.y - other.y;
        return Math.sqrt(dx * dx + dy * dy);
    }
}
```

**关键语义规则**:

| 规则 | 说明 | 对比普通 class |
|------|------|---------------|
| **隐式 final 字段** | 所有实例字段自动 `final`，不需要显式声明 | 普通 class 需要显式 `final` |
| **隐式 final 类** | value class 本身隐式 `final`，不可被继承 | 普通 class 默认可继承 |
| **无 identity** | 没有对象标识 (identity)，无法区分"同一个对象" | 普通 class 每个实例有唯一标识 |
| **可实现接口** | value class 可以 `implements` 接口 | 相同 |
| **不可继承类** | value class 不能 `extends` 其他类 (除 Object) | 普通 class 可以继承 |
| **不可声明同步方法** | 不能使用 `synchronized` 方法或块 | 普通 class 可以 |

```java
// value class 可以实现接口
public value class Complex implements Comparable<Complex> {
    double re;
    double im;

    public Complex(double re, double im) {
        this.re = re;
        this.im = im;
    }

    public double magnitude() {
        return Math.sqrt(re * re + im * im);
    }

    @Override
    public int compareTo(Complex other) {
        return Double.compare(this.magnitude(), other.magnitude());
    }
}
```

### 4.2 无 identity — 核心区别

**Identity (对象标识)** 是 Java 对象模型的基础概念。普通对象即使字段值完全相同，仍然是"不同的对象"。value class 放弃了这一概念：

```java
// 普通 class — 有 identity
class RegularPoint {
    final int x, y;
    RegularPoint(int x, int y) { this.x = x; this.y = y; }
}

RegularPoint a = new RegularPoint(1, 2);
RegularPoint b = new RegularPoint(1, 2);
System.out.println(a == b);       // false — 不同的对象标识
System.out.println(a.equals(b));  // false (除非重写 equals)

// value class — 无 identity
value class ValPoint {
    int x, y;
    ValPoint(int x, int y) { this.x = x; this.y = y; }
}

ValPoint c = new ValPoint(1, 2);
ValPoint d = new ValPoint(1, 2);
System.out.println(c == d);  // true — 按值比较！就像 int
```

**放弃 identity 的直接后果**:

```java
value class Amount {
    double value;
    String currency;
    Amount(double value, String currency) {
        this.value = value;
        this.currency = currency;
    }
}

Amount amt = new Amount(100.0, "USD");

// ❌ 编译错误: value class 不支持 synchronized
synchronized (amt) {  // Cannot synchronize on a value class instance
    // ...
}

// ❌ 编译错误: 不能用 identity-sensitive 操作
System.identityHashCode(amt);  // 警告: 对 value class 实例调用

// ✅ == 比较字段值 (而不是引用)
Amount amt2 = new Amount(100.0, "USD");
System.out.println(amt == amt2);  // true
```

### 4.3 扁平化存储 (Flattening)

扁平化是 value class 最重要的性能优势。JVM 可以将值对象直接**内联**到容器中，消除引用间接性和对象头开销：

```
普通 class 数组 (RegularPoint[3]):
  [ref1][ref2][ref3]  → 每个 ref 指向堆上独立对象 (header+x+y)
  总计: 24(引用) + 36(对象头) + 24(字段) = 84 字节 + 数组头

value class 扁平化数组 (ValPoint[3]):
  [x1|y1|x2|y2|x3|y3]  → 直接内联，无引用，无对象头
  总计: 24 字节 + 数组头 → 节省 76%!
```

**字段扁平化同样适用**:

```java
// 普通 class 中嵌套 value class
class Particle {
    ValPoint position;  // 扁平化: 直接存储 x, y，而非引用
    ValPoint velocity;  // 扁平化: 直接存储 x, y
    double mass;
}

// 内存布局 (扁平化后):
// ┌──────────────────────────────────────────┐
// │ [header]  [pos.x][pos.y][vel.x][vel.y][mass] │
// │  12 bytes   4+4      4+4       8       │
// │  总计: 12 + 8 + 8 + 8 = 36 字节         │
// └──────────────────────────────────────────┘
//
// 不扁平化时: 12(header) + 8(两个引用) + 8 + 2×(12+8) = 68 字节
```

**堆扁平化 (Heap Flattening) 与标量化 (Scalarization)**:
- **堆扁平化**: 值对象直接嵌入到容器字段和数组中，减少堆上的内存占用和缓存压力
- **标量化**: JIT 编译器在方法内部将值对象拆解为独立的标量值 (scalar values)，完全避免堆分配

```java
// 标量化示例 — JIT 编译器优化
value class Vec2 { double x, y; Vec2(double x, double y) { this.x = x; this.y = y; } }

// 源代码
Vec2 add(Vec2 a, Vec2 b) {
    return new Vec2(a.x + b.x, a.y + b.y);
}

// JIT 编译后 (概念上): 完全不分配对象
// 参数 a 拆为 a_x, a_y; 参数 b 拆为 b_x, b_y
// 返回值拆为 result_x = a_x + b_x, result_y = a_y + b_y
// → 零堆分配！
```

### 4.4 Null 约束与 ! 后缀

Value class 引入了新的 null 处理机制。默认情况下 value class 变量**可以为 null**（与引用类型一致），但可以使用 `!` 后缀声明**非 null 约束**：

```java
value class Color {
    int r, g, b;
    Color(int r, int g, int b) { this.r = r; this.g = g; this.b = b; }
}

// 默认: 可以为 null (与引用类型一致)
Color c1 = null;          // ✅ 合法
Color c2 = new Color(255, 0, 0);

// 使用 ! 后缀: 不可为 null
Color! c3 = new Color(0, 255, 0);  // ✅
Color! c4 = null;                   // ❌ 编译错误

// 非 null 值类型有默认值 (零值)
Color! c5;  // 默认值: Color(0, 0, 0) — 所有字段为零值

// 在数组中使用
Color![] colors = new Color![100];
// 每个元素自动初始化为 Color(0, 0, 0)，而非 null
// 数组可以被扁平化存储 — 100×12 字节 = 1200 字节
```

**null 约束对扁平化的影响**:

| 声明 | 可为 null？ | 默认值 | 可扁平化？ | 说明 |
|------|-----------|--------|-----------|------|
| `Color c` | 是 | `null` | 有条件 | JVM 需要额外标记位表示 null |
| `Color! c` | 否 | `Color(0,0,0)` | 是 | 完全扁平化，性能最佳 |

### 4.5 与 Records 的关系 — value record

Records (JDK 16 正式版) 和 Value Classes 是正交的特性，可以组合使用：

```java
// 普通 record — 有 identity，透明数据载体
record RegularPoint(int x, int y) {}

// value record — 无 identity + 透明数据载体
// 结合两者优势: record 的简洁语法 + value class 的性能
value record Point(int x, int y) {}

// value record 等价于:
value class Point {
    final int x;
    final int y;
    Point(int x, int y) { this.x = x; this.y = y; }
    // + 自动生成 equals(), hashCode(), toString()
    // + 自动生成 accessor 方法 x(), y()
}
```

**对比矩阵**:

| 特性 | `class` | `record` | `value class` | `value record` |
|------|---------|----------|---------------|----------------|
| Identity | 有 | 有 | **无** | **无** |
| 字段声明 | 显式 | 组件列表 | 显式 (隐式 final) | 组件列表 |
| 继承 | 可以 | 不可以 | 不可以 | 不可以 |
| `equals`/`hashCode` | 手动重写 | 自动生成 | `==` 按值比较 | 自动生成 + `==` 按值 |
| 扁平化存储 | 不可以 | 不可以 | **可以** | **可以** |
| synchronized | 可以 | 可以 | **不可以** | **不可以** |
| 可为 null | 是 | 是 | 是 (除非 `!`) | 是 (除非 `!`) |

```java
// 实际使用推荐: value record 是定义轻量数据类型的最佳选择
value record Money(long cents, String currency) {
    // 紧凑构造器做验证
    Money {
        if (cents < 0) throw new IllegalArgumentException("Negative amount");
        Objects.requireNonNull(currency);
    }

    public Money add(Money other) {
        if (!this.currency.equals(other.currency))
            throw new IllegalArgumentException("Currency mismatch");
        return new Money(this.cents + other.cents, this.currency);
    }
}

// 使用: 像 int 一样高效，像 class 一样有行为
Money! price = new Money(999, "USD");   // 不可为 null
Money! tax = new Money(80, "USD");
Money! total = price.add(tax);          // 零堆分配 (JIT 标量化)
```

### 4.6 已迁移的 JDK 类

JDK 26 预览中，以下 JDK 类在 `--enable-preview` 模式下已声明为 `value class`:

| 类 | 说明 | 预期收益 |
|----|------|---------|
| `java.time.LocalDate` | 日期 | 数组操作提速近 3x |
| `java.time.LocalTime` | 时间 | 减少内存占用 |
| `java.time.LocalDateTime` | 日期时间 | 扁平化存储 |
| `java.time.Instant` | 时间戳 | 消除对象头 |
| `java.lang.Integer` | int 包装类 | 未来配合 Unified Generics |
| `java.lang.Long` | long 包装类 | 同上 |
| 其他包装类 | Boolean, Byte, Short, etc. | 同上 |

### 4.7 编译与运行

```bash
# JDK 26+ 编译和运行 value class
javac --enable-preview --release 26 MyValueApp.java
java --enable-preview MyValueApp

# 或使用 Valhalla EA 构建 (基于 JDK 27 开发中)
# 下载: https://jdk.java.net/valhalla/

# 使用 jshell 交互式体验
jshell --enable-preview
jshell> value record Point(int x, int y) {}
jshell> Point! p = new Point(3, 4);
jshell> System.out.println(p);  // Point[x=3, y=4]
```

---

## 5. Unified Generics (JEP 402, 草案)

Unified Generics (统一泛型) 是 Valhalla 的第二大支柱，目标是允许泛型类型参数接受**所有类型**，包括原始类型和值类型。

### 5.1 泛型特化: `List<int>` 而非 `List<Integer>`

```java
// 当前 Java: 必须装箱
List<Integer> boxed = new ArrayList<>();
boxed.add(42);              // 自动装箱: Integer.valueOf(42)
int v = boxed.get(0);       // 自动拆箱: .intValue()
// 每个 Integer 对象: 16-20 字节 (对象头 + 4 字节 int + 填充)
// 100 万个元素: ~20 MB (vs. int[] 的 ~4 MB)

// Valhalla 未来: 直接使用原始类型
List<int> direct = new ArrayList<>();
direct.add(42);             // 无装箱！直接存储 4 字节
int v = direct.get(0);      // 无拆箱！直接读取
// 100 万个元素: ~4 MB — 节省 80% 内存

// 值类型也适用
List<Point!> points = new ArrayList<>();
points.add(new Point(1, 2));  // 扁平化存储 8 字节
```

### 5.2 擦除 vs 特化 的技术挑战

这是 Unified Generics 最困难的设计问题。Java 现有的泛型基于**类型擦除 (type erasure)**，而原始类型特化需要某种形式的**特化 (specialization)**：

```java
// 类型擦除 (Java 现行方案)
// 源码:
class Box<T> { T value; }
Box<String> box = new Box<>();

// 编译后 (字节码):
class Box { Object value; }  // T 被擦除为 Object
Box box = new Box();

// 问题: int 不是 Object 的子类！
Box<int> intBox = ???  // 擦除后 Box { Object value; } — 无法存 int
```

**可能的解决方案对比**:

| 方案 | 描述 | 优点 | 缺点 |
|------|------|------|------|
| **全特化** | 每种类型生成独立的类 | 最佳性能 | 类爆炸、代码膨胀 |
| **部分特化** | 原始类型特化，引用类型擦除 | 平衡性能和兼容性 | 实现复杂 |
| **JVM 层面特化** | JVM 在运行时按需特化 | 无类爆炸 | JVM 实现极复杂 |
| **擦除 + 桥接** | 保持擦除，但为原始类型插入桥接代码 | 最大兼容性 | 性能提升有限 |

**当前 Valhalla 的方向**: 采用一种混合方案 — 在字节码层面保留擦除，但允许 JVM 在运行时根据类型参数进行特化。JEP 402 仍在设计阶段，具体实现细节可能演变。

### 5.3 与 C# 泛型的对比

C# 从 2.0 (2005) 起就有完整的泛型特化 (reified generics)。Java 选择了不同的路径：

| 特性 | Java (当前) | Java (Valhalla) | C# |
|------|------------|-----------------|-----|
| 泛型实现 | 类型擦除 | 擦除 + 运行时特化 | 具化泛型 (reified) |
| `List<int>` | ❌ 不支持 | ✅ 将支持 | ✅ 已支持 (2005) |
| 运行时类型信息 | 无 (`T` 被擦除) | 部分保留 | 完整保留 |
| `new T()` | ❌ 不支持 | 待定 | ✅ 支持 (有约束时) |
| `T[]` 原始类型 | ❌ 不支持 | ✅ 将支持 | ✅ 已支持 |
| 向后兼容性 | 完全兼容 Java 1.4 | 保持兼容 | N/A (2.0 引入) |
| 值类型泛型 | ❌ | ✅ `List<Point!>` | ✅ `List<Vector3>` |

**为什么 Java 不直接采用 C# 方案？** 主要原因: (1) 20+ 年字节码兼容性承诺不能破坏 (2) Java 独立编译模型与运行时特化冲突 (3) ClassLoader 体系增加复杂度 (4) 完全具化泛型对 JVM 改动太大，Valhalla 采用渐进方案

```java
// C# 中的值类型泛型 (已可用)
List<int> nums = new List<int>();    // 内部用 int[] 存储
List<Vector3> vecs = new List<Vector3>();  // 内部用 Vector3[] 存储

// Java Valhalla (未来)
List<int> nums = new ArrayList<>();      // 同样的目标
List<Point!> points = new ArrayList<>();  // 扁平化存储
// 关键区别: Java 需要保持与现有 ArrayList<Integer> 的二进制兼容性
```

### 5.4 Unified Generics 的预期语法

```java
// 统一的泛型接口 — T 可以是任何类型
interface Summable<T> {
    T zero();
    T add(T a, T b);
}

// 对原始类型也适用
class IntSum implements Summable<int> {
    public int zero() { return 0; }
    public int add(int a, int b) { return a + b; }
}

// 泛型方法适用于所有类型
<T> T[] toArray(List<T> list) { ... }

int[] intArray = toArray(List.of(1, 2, 3));         // T = int
String[] strArray = toArray(List.of("a", "b"));      // T = String
Point![] ptArray = toArray(List.of(p1, p2));          // T = Point!
```

---

## 6. Compact Object Headers (JEP 519)

### 与 Valhalla 的关系

JEP 519 (Compact Object Headers) 将对象头从 **12 字节压缩到 8 字节**，虽然这是一个独立于 Valhalla 的优化，但两者紧密关联：

```
当前对象头 (12B):  [Mark Word 8B][Klass Pointer 4B] + 可能 4B 对齐填充
JEP 519 (8B):     [Combined Header 8B] — klass 编码进 mark word，每对象省 4B
Valhalla (0B):    [直接存储字段] — 无对象头，每实例省 12-16B
```
```

**JEP 519 与 Valhalla 的协同**:

| 场景 | 当前 | JEP 519 | Valhalla (value class) |
|------|------|---------|----------------------|
| `new Object()` | 16 字节 | 12 字节 (-25%) | N/A (不能是 value) |
| `new Point(x,y)` (class) | 24 字节 | 20 字节 (-17%) | **8 字节** (-67%) |
| `Point[1000]` (class) | ~32 KB | ~28 KB | **~8 KB** (-75%) |
| 包装类 `Integer` | 16 字节 | 12 字节 | **4 字节** (value class) |

JEP 519 在 JDK 25 (2025-09) 中已处于实验阶段。它为**不能**成为 value class 的普通对象减少开销，与 Valhalla 互补。

---

## 7. L-World

### 统一对象模型

L-World 是 Valhalla 的底层实现模型，统一了值类型和引用类型在 JVM 中的表示。名字来源于 JVM 类型描述符中的 `L` 前缀 (如 `Ljava/lang/String;`)。

| 特性 | 引用类型 | 值类型 (L-World) |
|------|----------|------------------|
| 默认值 | `null` | 类的默认值 (零值) |
| 标识 | 对象标识 | 无标识 (值语义) |
| 比较 | `==` 比较引用 | `==` 比较值 |
| `null` | 可以 | 取决于声明 |

---

## 8. 性能影响预估

> **重要说明**: 以下性能数据基于 Valhalla EA 构建和 JDK 26 预览版的早期测试。Valhalla 仍在开发中，最终性能会随实现成熟而变化。具体收益取决于工作负载特征。

### 8.1 消除 boxing/unboxing 开销

装箱/拆箱是 Java 性能的隐形杀手，尤其在数值密集型计算中：

```java
// 当前: 每次 add/get 触发 boxing/unboxing
List<Integer> list = new ArrayList<>();
for (int i = 0; i < 1_000_000; i++) {
    list.add(i);  // Integer.valueOf(i) — 分配对象或缓存查找
}
int sum = 0;
for (int v : list) {
    sum += v;     // .intValue() + 拆箱
}

// Valhalla (预期): 零 boxing/unboxing
List<int> list = new ArrayList<>();  // 内部直接存储 int
for (int i = 0; i < 1_000_000; i++) {
    list.add(i);  // 直接存储，无对象分配
}
```

**预期影响**:

| 指标 | 当前 (boxing) | Valhalla (预期) | 改进 |
|------|--------------|----------------|------|
| 每元素内存 | ~20 字节 (Integer) | 4 字节 (int) | **~5x** |
| GC 压力 | 大量短命对象 | 无额外对象 | **显著减少** |
| add() 延迟 | ~5-10 ns (分配) | ~1-2 ns (复制) | **~3-5x** |

### 8.2 数组扁平化减少缓存未命中

扁平化存储最大的好处是**缓存友好性 (cache friendliness)**：

```
// 普通对象数组: 引用分散在堆上
Point[] array = { ref→heap₁, ref→heap₂, ref→heap₃, ... }
                   ↓           ↓           ↓
              [header|x|y] [header|x|y] [header|x|y]
              (可能散布在不同的 cache line 中)

// 扁平化 value class 数组: 数据连续存储
Point![] array = [x₁|y₁|x₂|y₂|x₃|y₃|...]
                 (连续内存，顺序遍历完美利用 CPU 预取)
```

**缓存未命中对比** (概念估算):

| 场景 | 普通对象数组 | 扁平化数组 | 说明 |
|------|------------|-----------|------|
| 顺序遍历 1M 元素 | ~250K cache misses | ~30K cache misses | **~8x 更少** |
| 随机访问 | 每次几乎必中 miss | 索引可直接计算 | **显著改善** |
| 内存带宽利用率 | ~30% (对象头是浪费) | ~95% (全是有效数据) | **~3x 更高效** |

**JDK 26 中的实测数据** (来自 inside.java 报告):
- `LocalDate[]` 数组操作: **提速近 3x** (在预览模式下 LocalDate 为 value class)

### 8.3 内存占用减少

```java
// 场景: 金融交易系统，存储 1000 万条价格记录
value record PricePoint(long timestamp, double price, int volume) {}

// 当前 (普通 record):
// 每实例: 12(header) + 8(long) + 8(double) + 4(int) + 4(padding) = 36 字节
// 1000 万条: 360 MB + 引用数组 80 MB = ~440 MB

// Valhalla (value record, 扁平化):
// 每实例: 8(long) + 8(double) + 4(int) = 20 字节 (无 header，可能有 padding)
// 1000 万条: ~200 MB (无需引用数组)
// 节省: ~55%

// 场景: 3D 游戏引擎，100 万个粒子 (7 个 float = 28 字节)
// 普通 class: ~44 字节/实例 (含 header + padding) → 44 MB
// value record: 28 字节/实例 → 28 MB (节省 36%) + 缓存友好性大幅提升
```

### 8.4 限定词与注意事项

Valhalla 的性能提升**并非万能**:

| 场景 | 预期收益 | 原因 |
|------|---------|------|
| 小型值类 (2-4 字段) | ⬆⬆⬆ 大幅提升 | 对象头占比大，扁平化效果好 |
| 大型值类 (10+ 字段) | ⬆ 适度提升 | 复制成本增加，扁平化收益被稀释 |
| 频繁创建临时对象 | ⬆⬆⬆ 大幅提升 | JIT 标量化消除分配 |
| 长寿命单例对象 | → 几乎无影响 | 对象头开销可忽略 |
| 需要 identity 的场景 | → 无法使用 | 必须继续使用普通 class |
| I/O 密集型代码 | → 无影响 | 瓶颈不在对象分配 |

---

## 9. 时间线与现状 (2014-2026)

### 为什么 Valhalla 花了这么长时间？

Project Valhalla 从 2014 年启动到 2026 年首次预览，经历了 **12 年**。这在 OpenJDK 项目中非常罕见（对比 Project Loom: 2017-2023，6 年）。原因在于 Valhalla 要求的变更深度：

**JVM 层面的深度变更**:

1. **对象模型重设计**: Java 从 1.0 起就假设"所有对象都有 identity"。移除这个假设影响对象头布局、GC 遍历、锁实现 (synchronized 依赖 mark word)、`==` 语义 — JVM 的每一层都受影响

2. **数组扁平化**: 当前 JVM 数组假设元素要么是固定宽度原始类型，要么是引用。值类型数组需要可变宽度内联对象，影响分配、边界检查、GC 扫描

3. **泛型特化**: 类型擦除是 Java 5 以来的基石。在不破坏兼容性的前提下支持 `List<int>`，需要同时改变编译器和 JVM

4. **多次设计方向调整**: Q-World (2014) → L-World (2017) → Inline Classes → Primitive Classes → Value Classes (2022) → 分阶段交付 (2023)

### 完整时间线

| 年份 | 里程碑 | 说明 |
|------|--------|------|
| **2014** | Project Valhalla 启动 | John Rose 宣布项目，发表 "State of the Values" |
| **2015** | Value Types 原型 | JVM 原型实现 (Q-World) |
| **2016** | JEP 169 (Value Objects) | 初始 JEP 提案 |
| **2017** | LW1 (L-World 1) | 放弃 Q-World，统一到 L-World 模型 |
| **2018** | LW2 | 实验性实现 |
| **2020** | LW3 | 内联类原型 |
| **2021** | JEP 390 (JDK 16) | ⚠️ Value-Based Classes 警告 — 为 Valhalla 铺路 |
| **2021** | Inline Classes (JEP 401) | 进入候选阶段 |
| **2022** | Primitive Classes (JEP 401 更新) | 重命名为 Primitive Classes |
| **2023** | Universal Generics | 泛型特化原型 |
| **2024** | 逐步交付策略 | 确定分阶段发布计划: Value Classes 先行 |
| **2025** | JDK 25 LTS | 继续完善原型；EA 构建发布 |
| **2025-10** | JEP 401 EA 构建发布 | inside.java 发布可试用的 Value Classes 构建 |
| **2026-03** | JDK 26: JEP 401 (Preview) | **Value Classes and Objects 首次预览** |
| **2026-03** | JDK 26: JEP 530 (4th Preview) | Primitive Patterns 第四预览 |
| **2027+** | 逐步交付 | Value Classes 正式版、Unified Generics 预览 |

→ [完整时间线](timeline.md)

### JDK 26 当前状态 (2026-03-17 GA)

**已交付特性**:

| 特性 | 版本 | 状态 |
|------|------|------|
| **Record Patterns** | JDK 21 | 正式版 |
| **Unnamed Patterns** | JDK 22 | 正式版 |
| **JEP 390 警告** | JDK 16 | 正式版 |

**JDK 26 新增**:

| 特性 | JEP | 状态 |
|------|-----|------|
| **Value Classes and Objects** | JEP 401 (Preview) | 首次预览 |
| **Primitive Patterns** | JEP 530 (4th Preview) | 第四预览 |

**开发中**:

| 特性 | JEP | 目标版本 | 状态 |
|------|-----|----------|------|
| **Value Classes** 正式版 | JEP 401 | JDK 27-28 | 预览迭代中 |
| **Unified Generics** | JEP 402 | JDK 28+ | 草案 / 开发中 |

---

## 10. JEP 进展

| JEP | 标题 | 状态 | 目标版本 |
|-----|------|------|----------|
| **JEP 401** | Value Classes and Objects (Preview) | JDK 26 预览 | JDK 26 |
| **JEP 402** | Unified Generics | 持续开发 | JDK 28+ |
| **JEP 519** | Compact Object Headers | 实验阶段 | JDK 25 |
| **JEP 530** | Primitive Patterns (4th Preview) | 第四预览 | JDK 26 |
| **JEP 390** | Warnings for Value-Based Classes | 已交付 | JDK 16 |
| **JEP 218** | Generics over Primitive Types | 早期设计 | - |

---

## 11. 迁移准备

### 11.1 JEP 390: Value-Based Classes 警告

JEP 390 (JDK 16) 是为 Valhalla 做的**提前准备**。它为"基于值的类" (Value-Based Classes) 添加了编译期和运行期警告：

```java
// JDK 16+ 编译警告
Integer val = Integer.valueOf(42);
synchronized (val) {
    // ⚠️ 警告: Synchronization on an instance of a value-based class
    // 未来 Integer 可能成为 value class，届时 synchronized 会失败
}

// 运行时警告 (使用 -XX:+DiagnoseValueBasedClasses)
java -XX:DiagnoseValueBasedClasses MyApp
// 运行时检测对 value-based class 实例的 identity-sensitive 操作
```

**受影响的 JDK 类** (标注了 `@jdk.internal.ValueBased`):

- 所有原始包装类: `Integer`, `Long`, `Double`, `Boolean`, `Byte`, `Short`, `Float`, `Character`
- `java.time` 所有类: `LocalDate`, `LocalTime`, `Instant`, `Duration`, ...
- `java.util.Optional` 系列: `Optional`, `OptionalInt`, `OptionalLong`, `OptionalDouble`
- `ProcessHandle` 的实现

### 11.2 迁移清单: 如何为 Valhalla 做准备

**立即可做** (JDK 16+):

```java
// 1. 消除对 value-based class 的 synchronized 使用
// ❌ 避免
synchronized (Integer.valueOf(42)) { ... }
synchronized (LocalDate.now()) { ... }
synchronized (Optional.of("x")) { ... }

// ✅ 改为使用显式锁
private final Object lock = new Object();
synchronized (lock) { ... }
// 或使用 ReentrantLock
private final ReentrantLock lock = new ReentrantLock();

// 2. 避免对 value-based class 使用 == 比较引用
Integer a = Integer.valueOf(200);
Integer b = Integer.valueOf(200);
if (a == b) { ... }     // ❌ 依赖 identity — 未来行为会变
if (a.equals(b)) { ... } // ✅ 用 equals()

// 3. 避免依赖 System.identityHashCode()
int hash = System.identityHashCode(LocalDate.now());  // ❌
int hash = LocalDate.now().hashCode();                  // ✅
```

**设计层面的准备**:

```java
// 4. 使用 Record 替代 POJO — Record 最容易迁移为 value record
// ❌ 手动 POJO
class Point {
    private final int x, y;
    Point(int x, int y) { this.x = x; this.y = y; }
    int x() { return x; }
    int y() { return y; }
    // equals, hashCode, toString...
}

// ✅ Record — 未来只需加 value 前缀
record Point(int x, int y) {}
// 将来: value record Point(int x, int y) {}

// 5. 使用原始类型集合库减少 boxing
// 替代 List<Integer> 使用:
import it.unimi.dsi.fastutil.ints.IntArrayList;
IntArrayList list = new IntArrayList();
list.add(42);  // 无装箱

// 或 Eclipse Collections:
import org.eclipse.collections.api.list.primitive.IntList;
import org.eclipse.collections.impl.factory.primitive.IntLists;
IntList list = IntLists.mutable.of(1, 2, 3);
```

**代码审查清单**:

- [ ] 搜索代码中对 `Integer`, `Long`, `Double` 等的 `synchronized` 使用
- [ ] 搜索 `==` 比较 `Optional`, `LocalDate` 等 value-based 类的实例
- [ ] 搜索 `System.identityHashCode()` 对 value-based 类实例的调用
- [ ] 将不可变 POJO 重构为 Record
- [ ] 评估是否可以使用原始类型集合库 (FastUtil, Eclipse Collections)
- [ ] 运行 `javac -Xlint:synchronization` 检查同步警告
- [ ] 使用 `-XX:+DiagnoseValueBasedClasses` 运行测试套件

```bash
# 检测工具命令
# 编译期检查
javac -Xlint:synchronization MyApp.java

# 运行期检查
java -XX:+DiagnoseValueBasedClasses -cp . MyApp

# 在 CI 中启用检查
# build.gradle
tasks.withType(JavaCompile) {
    options.compilerArgs += ['-Xlint:synchronization']
}
```

---

## 12. 核心贡献者

### 项目领导

| 贡献者 | 组织 | 角色 |
|--------|------|------|
| John Rose | Oracle | 项目创始人、架构师 |
| [David Holmes](/by-contributor/profiles/david-holmes.md) | Oracle | 运行时架构、技术领导 |
| [Brian Goetz](/by-contributor/profiles/brian-goetz.md) | Oracle | Java 语言架构师 |

### JVM 实现

Tobias Hartmann, Christian Hagedorn, Vladimir Kozlov (C2 JIT), Stefan Karlsson (GC/数组), [Roman Kennke](/by-contributor/profiles/roman-kennke.md) (JIT/Shenandoah), [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) (类加载), [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) (内存管理)

### 语言特性

[Chen Liang](/by-contributor/profiles/chen-liang.md) (javac), Vicente Romero (javac), [David Beaumont](/by-contributor/profiles/david-beaumont.md) (javac/构建), Gavin Bierman (语言规范), Maurizio Cimadamore (类型系统), [Jan Lahoda](/by-contributor/profiles/jan-lahoda.md) (javac)

### 核心库

[Roger Riggs](/by-contributor/profiles/roger-riggs.md) (核心库/序列化), Frederic Parain (字段/JNI), Daniel D. Daugherty (测试), Markus Grönlund (JFR)

### 其他贡献者

活跃社区贡献者包括 Quan Anh Mai (C2 JIT)、Axel Boldt-Christmas (GC)、Ivan Walulya (字段布局)、Alex Menkov (JDWP/JVMTI) 等。历史贡献者包括 Aleks Seovic (早期原型)、Srikanth Adayapalam (语言设计)、Harold Seigel (JVM 实现) 等。

→ [开发活动详情](development.md)

---

## 13. 示例对比

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

### Valhalla Value Classes (JEP 401, JDK 26 Preview)

```java
// 内存高效 - 使用 value 修饰符 (JDK 26+ --enable-preview)
public value class Complex {
    double re;  // 隐式 final
    double im;

    public Complex(double re, double im) {
        this.re = re;
        this.im = im;
    }

    public Complex add(Complex other) {
        return new Complex(this.re + other.re, this.im + other.im);
    }

    public Complex multiply(Complex other) {
        return new Complex(
            this.re * other.re - this.im * other.im,
            this.re * other.im + this.im * other.re
        );
    }

    public double magnitude() {
        return Math.sqrt(re * re + im * im);
    }
}

// 使用
Complex![] values = new Complex![1000];
// 堆扁平化: 每个实例 16 字节 (2×double)，无对象头
// 1000 个实例: 16,000 字节
// 节省: 60% 内存!

// FFT (快速傅里叶变换) 性能对比:
// 普通 class Complex: ~150 ms (大量 GC，缓存不友好)
// value class Complex: ~50 ms (零 GC，连续内存访问)  [预期]
```

### 综合示例: 从当前到未来

```java
// ── 第一步: 当前 Java (JDK 21+) ──
record Point(int x, int y) {}

List<Point> points = new ArrayList<>();           // 引用类型，有 boxing
points.stream().map(p -> p.x() + p.y()).sum();    // 需要 mapToInt

// ── 第二步: JDK 26 Preview ──
value record Point(int x, int y) {}

Point![] points = new Point![1000];               // 扁平化数组
// == 按值比较，无 identity，性能大幅提升

// ── 第三步: Unified Generics (未来) ──
value record Point(int x, int y) {}

List<Point!> points = new ArrayList<>();          // 泛型 + 值类型
List<int> values = new ArrayList<>();             // 泛型 + 原始类型
// 完全消除原始类型与引用类型的鸿沟
```

---

## 14. 当前最佳实践

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

// 虽然仍是引用类型，但语义上最接近 value class
// 未来迁移: 只需添加 value 前缀
// public value record Point(int x, int y) {}
```

---

## 15. 相关项目

| 项目 | 关系 |
|------|------|
| **Project Amber** | 语言特性配合 (模式匹配、Records、Primitive Patterns) |
| **Project Loom** | 虚拟线程配合 (减少栈帧开销) |
| **Project Panama** | 外部函数接口配合 (值类型表示 native struct) |
| **Project Leyden** | AOT 编译配合 (值类型可以更好地静态优化) |
| **GraalVM** | 值类型 JIT 优化 |
| **JEP 519** | Compact Object Headers — 对非 value class 对象也减少对象头开销 |

---

## 16. 参考资料

- [Project Valhalla Wiki](https://openjdk.org/projects/valhalla/)
- [JEP 401: Value Classes and Objects](/jeps/language/jep-401.md)
- [JEP 402: Unified Generics](/jeps/language/jep-402.md)
- [JEP 390: Warnings for Value-Based Classes](https://openjdk.org/jeps/390)
- [JEP 519: Compact Object Headers](https://openjdk.org/jeps/519)
- [Brian Goetz - "State of Valhalla" (2024)](https://openjdk.org/projects/valhalla/design-notes/state-of-valhalla/03-vm-model)
- [Value Types: Reviving Java's Original Ideal](https://cr.openjdk.org/~jrose/papers/valhalla/valhalla-2014-slides.pdf)

→ [值类型详解](value-types.md) | [泛型特化详解](generics.md) | [开发活动分析](development.md)
