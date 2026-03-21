# 增强泛型详解

原始类型特化、Any-generics 和统一泛型模型。

[← 返回 Valhalla](./)

---
## 目录

1. [TL;DR](#1-tldr)
2. [问题背景](#2-问题背景)
3. [解决方案: Primitive Specialization](#3-解决方案-primitive-specialization)
4. [实现策略](#4-实现策略)
5. [类型系统变化](#5-类型系统变化)
6. [核心库特化](#6-核心库特化)
7. [性能影响](#7-性能影响)
8. [特化约束](#8-特化约束)
9. [实现状态](#9-实现状态)
10. [当前最佳实践](#10-当前最佳实践)
11. [示例应用](#11-示例应用)
12. [参考资料](#12-参考资料)
13. [相关主题](#13-相关主题)

---


## 1. TL;DR

**增强泛型** (Enhanced Generics) 让 Java 泛型支持原始类型：

```java
// 当前: 只能用引用类型
List<Integer> boxed = ...;  // 装箱开销

// 未来: 原始类型特化
List<int> primitives = ...;  // 无装箱!
```

---

## 2. 问题背景

### 当前限制

```java
// ❌ 编译错误
List<int> intList = new ArrayList<>();  // 类型参数不能是原始类型

// ✅ 必须使用包装类型
List<Integer> integerList = new ArrayList<>();

// 性能问题
integerList.add(42);      // Integer.valueOf(42) - 装箱
int value = integerList.get(0);  // integerList.get(0).intValue() - 拆箱

// 内存问题
// Integer 对象 = 12(头) + 4(int) + 4(填充) = 20 字节
// int 值 = 4 字节
// 浪费 5倍内存!
```

### 类型擦除的代价

```java
// 源码
List<Integer> list = new ArrayList<>();
list.add(42);

// 编译后 (类型擦除)
List list = new ArrayList();
list.add(Integer.valueOf(42));

// 运行时无法优化为原始类型存储
```

### 装箱/拆箱开销

| 操作 | 开销 | 频率 |
|------|------|------|
| **装箱** | 分配对象 + 复制 | 每次 add |
| **拆箱** | 方法调用 + 类型转换 | 每次 get |
| **内存** | 对象头 + 引用 | 持续占用 |

---

## 3. 解决方案: Primitive Specialization

### 基本概念

```
┌─────────────────────────────────────────────────────────┐
│                    泛型特化                              │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   interface List<T>                                     │
│   ├── List<Integer>  → 引用类型特化                      │
│   ├── List<int>       → 原始类型特化                     │
│   └── List<String>    → 引用类型特化                     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 语法设计

```java
// Any-generics: T 可以是任何类型
interface Buffer<T> {
    void add(T value);
    T get(int index);
    int size();
}

// 原始类型特化
Buffer<int> intBuffer = new IntBuffer();  // 无装箱!
intBuffer.add(42);
int value = intBuffer.get(0);

// 引用类型特化 (现有行为)
Buffer<String> stringBuffer = new StringBuffer<>();
stringBuffer.add("hello");
String value = stringBuffer.get(0);

// 值类型特化 (Valhalla)
Buffer<Point> pointBuffer = new PointBuffer<>();
pointBuffer.add(new Point(1, 2));
Point value = pointBuffer.get(0);
```

---

## 4. 实现策略

### 特化模板

```java
// 源码: 通用接口
public interface List<T> {
    void add(T value);
    T get(int index);
}

// 编译器自动生成特化版本

// int 特化
public interface List<int> {
    void add(int value);      // 直接接受 int
    int get(int index);       // 直接返回 int
}

// Integer 特化
public interface List<Integer> {
    void add(Integer value);  // 引用类型
    Integer get(int index);
}

// String 特化
public interface List<String> {
    void add(String value);
    String get(int index);
}
```

### 字节码表示

```java
// 源码
Buffer<int> buffer = ...;

// 字节码 (提议)
// 描述符: Qjava/util/Buffer;<I>;
// 类型: QBuffer;<I>; (值类型描述符 + 原始类型参数)

// 方法调用
buffer.add(42);
// invokeinterface Buffer/add(I)V
// 注意: 无装箱/拆箱
```

### 描述符系统

```
当前描述符:
  Ljava/lang/String;  - 引用类型
  [I                 - int 数组

Valhalla 描述符:
  Qjava/lang/String;  - 值类型 (Inline Class)
  Qjava/util/List;<I> - 特化泛型 (int 参数)
```

---

## 5. 类型系统变化

### 类型参数约束

```java
// T 可以是: 引用类型、原始类型、值类型
interface Container<T> {
    T get();
    void set(T value);
}

// 泛型约束
interface NumberContainer<T extends Number> {
    // T 可以是 int, long, double, Integer, Double...
    T add(T a, T b);
}

// 无界类型参数
interface Any<T> {
    // T 可以是任何类型
    T transform(T value);
}
```

### 类型推断

```java
// 类型推断支持原始类型
var list = new ArrayList<int>();  // ArrayList<int>
list.add(42);

// 方法类型推断
static <T> List<T> of(T... values) {
    return List.of(values);
}

// 推断为 List<int>
var ints = of(1, 2, 3);  // List<int>

// 推断为 List<double>
var doubles = of(1.0, 2.0, 3.0);  // List<double>
```

### 类型层次

```
当前:
  Object
    ├── Number
    │   ├── Integer
    │   ├── Double
    │   └── ...
    └── 其他引用类型

Valhalla:
  Object
    ├── Number
    │   ├── Integer (引用)
    │   ├── Double (引用)
    │   └── ...
    ├── int (值类型)
    ├── double (值类型)
    └── Point (值类型)
```

---

## 6. 核心库特化

### 集合框架

```java
// List 接口特化
interface List<T> {
    // 通用方法
    int size();
    boolean isEmpty();

    // 特化方法 (原始类型时自动优化)
    void add(T value);
    T get(int index);
}

// Stream 特化
interface Stream<T> {
    Stream<T> filter(Predicate<T> predicate);
    <R> Stream<R> map(Function<T, R> mapper);
}

// 原始类型 Stream (现有 - 临时方案)
IntStream intStream();
LongStream longStream();
DoubleStream doubleStream();

// 未来: 统一 Stream
Stream<int> stream = List.of(1, 2, 3).stream();
```

### 函数式接口

```java
// 现有原始类型函数式接口 (临时方案)
IntFunction<Integer, String> intToIntString = i -> "Value: " + i;
IntPredicate intPredicate = i -> i > 0;
IntUnaryOperator intNegator = i -> -i;

// 未来: 统一函数式接口
Function<int, String> intToString = i -> "Value: " + i;
Predicate<int> isPositive = i -> i > 0;
UnaryOperator<int> negate = i -> -i;
```

---

## 7. 性能影响

### 内存对比

```java
// 当前: List<Integer>
List<Integer> boxed = new ArrayList<>(1000);
for (int i = 0; i < 1000; i++) {
    boxed.add(i);
}
// 内存: 1000 × 20 (Integer) + 8000 (引用) ≈ 28 KB

// 未来: List<int>
List<int> primitives = new ArrayList<>(1000);
for (int i = 0; i < 1000; i++) {
    primitives.add(i);
}
// 内存: 1000 × 4 (int) ≈ 4 KB
// 节省: 85%!
```

### 性能对比

```java
// 基准测试: 遍历 100万元素

// List<Integer> - 装箱
for (Integer i : boxedList) {
    sum += i;  // 拆箱开销
}
// ~50ms

// List<int> - 无装箱
for (int i : intList) {
    sum += i;  // 直接操作
}
// ~5ms (10x faster!)

// int[] - 原始数组
for (int i : intArray) {
    sum += i;
}
// ~4ms (与 List<int> 相当)
```

---

## 8. 特化约束

### 类型擦除兼容性

```java
// 兼容性问题
List<int> intList = ...;
List<Integer> integerList = ...;

// ❌ 不是子类型关系
// List<int> 不是 List<Integer> 的子类型

// ✅ 通过通配符
void process(List<? extends Number> list) {
    // 可以接受 List<Integer>, List<Double>
    // 可以接受 List<int>, List<double>
}
```

### 反射 API

```java
// 反射获取特化类型
Class<?> elementType = List.class.getTypeParameter("T");
// 对于 List<int>, 返回 int.class

// Method.getGenericParameterTypes()
Method add = List.class.getMethod("add", Object.class);
Type[] params = add.getGenericParameterTypes();
// 对于 List<int>, 返回 int.class
```

---

## 9. 实现状态

### JEP 402: Unified Generics

| 阶段 | 内容 | 状态 |
|------|------|------|
| **阶段 1** | 类型系统设计 | ✅ 完成 |
| **阶段 2** | 字节码扩展 | 🔄 进行中 |
| **阶段 3** | javac 实现 | 🔄 进行中 |
| **阶段 4** | 核心库特化 | 🔄 进行中 |
| **阶段 5** | JIT 优化 | ⏳ 待开始 |

### 特化优先级

| 优先级 | 类型 | 原因 |
|--------|------|------|
| **P0** | `int`, `long`, `double` | 最常用 |
| **P1** | `byte`, `short`, `float`, `char`, `boolean` | 次常用 |
| **P2** | 值类型 | 与 Valhalla 配合 |

---

## 10. 当前最佳实践

### 使用原始类型集合库

```java
// FastUtil - 高性能原始类型集合
import it.unimi.dsi.fastutil.ints.IntArrayList;
import it.unimi.dsi.fastutil.ints.Int2ObjectMap;
import it.unimi.dsi.fastutil.longs.LongArrayList;

// IntArrayList - 替代 List<Integer>
IntArrayList ints = new IntArrayList();
ints.add(42);
ints.add(100);
int sum = ints.stream().sum();  // 无装箱

// LongArrayList - 替代 List<Long>
LongArrayList longs = new LongArrayList();
longs.add(1_000_000L);

// Int2ObjectMap - 原始类型键 Map
Int2ObjectMap<String> map = new Int2ObjectOpenHashMap<>();
map.put(1, "one");
String value = map.get(1);
```

### Eclipse Collections

```java
// Eclipse Collections - 原始类型集合
import org.eclipse.collections.impl.list.mutable.primitive.IntArrayList;
import org.eclipse.collections.api.list.primitive.ImmutableIntList;

IntArrayList ints = new IntArrayList();
ints.addAllWith(1, 2, 3, 4, 5);

IntList immutable = ints.toImmutable();
int sum = ints.sum();  // 无装箱
```

### HPPC (High Performance Primitive Collections)

```java
// HPPC - 另一个高性能集合库
import com.carrotsearch.hppc.IntArrayList;
import com.carrotsearch.hppc.IntCursor;

IntArrayList ints = new IntArrayList();
ints.add(42);
ints.add(100);

IntCursor cursor = ints.cursor();
while (cursor.moveNext()) {
    System.out.println(cursor.value);
}
```

---

## 11. 示例应用

### 高性能集合

```java
// 金融计算: 使用原始类型集合
IntArrayList prices = new IntArrayList(1_000_000);
for (int i = 0; i < 1_000_000; i++) {
    prices.add((int)(Math.random() * 100));
}

// 计算 - 无装箱
int sum = prices.stream().sum();
int max = prices.stream().max();
```

### 科学计算

```java
// 矩阵运算
class Matrix {
    private final IntArrayList[] data;

    Matrix(int rows, int cols) {
        data = new IntArrayList[rows];
        for (int i = 0; i < rows; i++) {
            data[i] = new IntArrayList(cols);
        }
    }

    int get(int row, int col) {
        return data[row].getInt(col);
    }

    void set(int row, int col, int value) {
        data[row].set(col, value);
    }
}
```

---

## 12. 参考资料

### JEP 文档

- [JEP 402: Unified Generics](https://openjdk.org/jeps/402)
- [JEP 218: Generics over Primitive Types](https://openjdk.org/jeps/218)

### 技术论文

- [Universal Generics for Java](https://openjdk.org/jeps/402/spec)
- [Specialized Generic Classes](https://cr.openjdk.org/~briangoetz/valhalla/specialization-impactus.html)

### 邮件列表

- [Valhalla Spec Observers](https://mail.openjdk.org/pipermail/valhalla-spec-observers/)

---

## 13. 相关主题

- [值类型详解](value-types.md)
- [Project Amber](../amber/) - 语言特性配合
- [Project Loom](../loom/) - 性能配合

→ [返回 Valhalla](./)
