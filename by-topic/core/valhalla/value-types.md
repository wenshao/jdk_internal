# 值类型详解

Inline Classes、L-World 和值语义的深入分析。

[← 返回 Valhalla](./)

---

## TL;DR

**值类型** (Value Types) 是用户定义的类型，具有：
- **无对象头** - 内存布局扁平化
- **值语义** - 无标识，按值比较
- **内联存储** - 可以嵌入其他对象/数组

---

## 概念对比

### 引用类型 vs 值类型

| 特性 | 引用类型 | 值类型 (Inline Class) |
|------|----------|----------------------|
| **内存布局** | 引用 + 堆对象 | 扁平化，无引用 |
| **对象头** | 12-16 字节 | 0 字节 |
| **标识** | 有 (identity) | 无 (identity-free) |
| **null** | 可以为 null | 不能为 null |
| **比较** | `==` 比较引用 | `==` 比较值 |
| **默认值** | `null` | 类的默认值 |
| **锁定** | 可 synchronized | 不支持 |

---

## Inline Classes 语法

### 定义

```java
// JDK 未来语法 (Proposed)
public inline class Point {
    public final int x;
    public final int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    // 值类型自动生成的 equals/hashCode
    // 可以重写但不能依赖标识
}

// 使用
Point p1 = new Point(1, 2);
Point p2 = new Point(1, 2);

// p1 == p2  → true (值比较，非引用比较)
```

### 值类型约束

```java
// ✅ 允许
public inline class Valid {
    // final 字段
    public final int value;

    // 不可变对象引用
    public final String name;

    // 其他值类型
    public final Point point;
}

// ❌ 不允许
public inline class Invalid {
    // 可变字段
    public int counter;  // 编译错误!

    // 自引用 (破坏值语义)
    public Invalid self;  // 编译错误!

    // 继承
    public inline class Child extends Invalid {}  // 编译错误!
}
```

---

## 内存布局

### 引用类型数组

```
Integer[] array = new Integer[3];
array[0] = Integer.valueOf(1);
array[1] = Integer.valueOf(2);
array[2] = Integer.valueOf(3);

内存布局:
┌─────────────────────────────────────┐
│  array (引用数组)                    │
│  [ref1][ref2][ref3]                 │
└─────────────────────────────────────┘
         │      │      │
         ▼      ▼      ▼
┌─────────────────────────────────────┐
│  堆对象 (每个 Integer)               │
│  [header][int value]                │
│  [header][int value]                │
│  [header][int value]                │
└─────────────────────────────────────┘

总内存: 3×4(引用) + 3×16(对象) = 60 字节
```

### 值类型数组

```
Point[] array = new Point[3];
array[0] = new Point(1, 2);
array[1] = new Point(3, 4);
array[2] = new Point(5, 6);

内存布局:
┌─────────────────────────────────────┐
│  array (扁平化数组)                  │
│  [x:1][y:2][x:3][y:4][x:5][y:6]     │
└─────────────────────────────────────┘

总内存: 3×8(两个int) = 24 字节
节省: 60%!
```

---

## L-World

### 统一对象模型

L-World 是 Valhalla 的核心设计，统一了引用类型和值类型：

```
L-World 类型层次:

           Object
           /    \
          /      \
   Reference     Value
   (引用类型)    (值类型)

• Reference: 可以为 null，有标识
• Value: 不能为 null，无标识
```

### 类型描述符

| 类型 | 描述符 | 示例 |
|------|--------|------|
| 引用类型 | `Ltype;` | `Ljava/lang/String;` |
| 值类型 | `Qtype;` | `QPoint;` |
| 原始类型 | `I` (int) | `[I` (int[]) |

---

## 默认值

### 值类型的默认值

```java
public inline class Complex {
    public final double re;
    public final double im;

    public Complex(double re, double im) {
        this.re = re;
        this.im = im;
    }

    // 默认值工厂方法
    public static Complex $default$() {
        return new Complex(0.0, 0.0);
    }
}

// 数组初始化
Complex[] array = new Complex[10];
// 所有元素初始化为 Complex(0.0, 0.0)
```

### 为什么不能为 null

```java
// 引用类型
String s = null;      // ✅ 允许
// s.length() → NullPointerException

// 值类型
Point p = null;       // ❌ 编译错误
// 值类型总是有值，无需 null 检查
```

---

## 性能特性

### 缓存友好

```java
// 引用类型数组 - 缓存不友好
Integer[] boxed = new Integer[1000];
for (int i = 0; i < 1000; i++) {
    sum += boxed[i];  // 每次访问可能缓存未命中
}

// 值类型数组 - 缓存友好
int[] primitives = new int[1000];
for (int i = 0; i < 1000; i++) {
    sum += primitives[i];  // 连续内存，缓存命中率高
}

// Inline class - 同样缓存友好
inline class IntBox { public final int value; }
IntBox[] values = new IntBox[1000];
// 扁平化存储，与 int[] 相同的缓存行为
```

### 消除虚方法调用

```java
// 引用类型 - 虚方法调用
String s = "hello";
int len = s.length();  // invokevirtual Object.length()

// 值类型 - 静态分发
inline class StringLike {
    public final byte[] data;
    public int length() { return data.length; }  // 内联
}

StringLike s = ...;
int len = s.length();  // 直接内联，无虚调用
```

---

## JIT 编译优化

### C2 支持

| 优化 | 引用类型 | 值类型 |
|------|----------|--------|
| **标量替换** | 逃逸分析后 | 始终 |
| **字段扁平化** | 可能 | 始终 |
| **循环向量化** | 困难 | 容易 |
| **寄存器分配** | 间接 | 直接 |

### 示例: 向量化

```java
// 引用类型 - 难以向量化
Point[] points = ...;
for (int i = 0; i < points.length; i++) {
    points[i].x += 1;  // 可能需要解引用
}

// 值类型 - 容易向量化
inline class Point { public int x, y; }
Point[] points = ...;
for (int i = 0; i < points.length; i++) {
    points[i].x += 1;  // SIMD 指令优化
}
```

---

## 限制和注意事项

### 不支持的操作

```java
public inline class Point {
    public final int x, y;

    // ❌ 不支持 synchronized
    public synchronized void move(int dx, int dy) { ... }

    // ❌ 不支持作为锁对象
    // synchronized (point) { ... }

    // ❌ 不支持 WeakReference
    // WeakReference<Point> ref = ...;

    // ❌ 不支持 == 比较 null
    // if (point == null) { ... }
}
```

### 设计权衡

| 决策 | 理由 |
|------|------|
| 不可变优先 | 简化推理，更好的优化 |
| 无标识 | 避免别名问题 |
| 不可为 null | 消除 NPE 风险 |
| 禁止锁 | 避免同步开销 |

---

## 实际应用场景

### 数值计算

```java
public inline class Complex {
    public final double re, im;

    public Complex plus(Complex other) {
        return new Complex(re + other.re, im + other.im);
    }

    public Complex times(Complex other) {
        return new Complex(
            re * other.re - im * other.im,
            re * other.im + im * other.re
        );
    }
}

// 使用
Complex[] data = new Complex[1024];
// 扁平化存储，SIMD 优化潜力
```

### 日期时间

```java
public inline class LocalDate {
    public final int year;
    public final int month;
    public final int day;

    // 无对象头，大量实例时节省内存
}

public inline class Instant {
    public final long seconds;
    public final int nanos;
}
```

### 几何类型

```java
public inline class Rectangle {
    public final double x, y, width, height;

    public boolean contains(Point p) {
        return p.x >= x && p.x < x + width &&
               p.y >= y && p.y < y + height;
    }
}
```

---

## 参考资料

- [JEP 401: Primitive Classes](https://openjdk.org/jeps/401)
- [Value Types: One Path to Valhalla](https://openjdk.org/jeps/401)
- [L-World Design Notes](https://openjdk.org/projects/valhalla/design-notes/)

→ [返回 Valhalla](./) | [泛型特化详解](generics.md)
