---

# JEP 401: Value Classes (Preview) 实现分析

> JEP 401 | Brian Goetz (Oracle) | JDK 26 (Preview) | Valhalla 项目

---

## 目录

1. [概述](#1-概述)
2. [Valhalla 项目背景](#2-valhalla-项目背景)
3. [Value Classes vs Records vs Primitives](#3-value-classes-vs-records-vs-primitives)
4. [语言模型](#4-语言模型)
5. [JVM 实现 (Q-Types)](#5-jvm-实现-q-types)
6. [性能模型](#6-性能模型)
7. [当前限制](#7-当前限制)
8. [演进路线](#8-演进路线)

---

## 1. 概述

Value Classes 是 Valhalla 项目的核心特性，引入了**无标识（identity-free）**的类类型。Value class 实例没有对象头（object header），可以扁平化存储在数组和字段中，显著减少内存占用和间接访问开销。

| 属性 | 值 |
|------|-----|
| **JEP** | [JEP 401](https://openjdk.org/jeps/401) |
| **作者** | Brian Goetz |
| **目标版本** | JDK 26 (Preview) |
| **状态** | Preview |
| **前置** | JEP 401 (Value Classes) |

---

## 2. Valhalla 项目背景

### 2.1 为什么需要 Value Classes?

Java 的对象模型基于"引用语义"——每个对象有唯一标识（identity）、对象头（mark word + klass pointer）、存储在堆上、通过引用访问。

```
传统 Java 对象 (有标识):
┌─────────────────────────────┐
│ Reference (8 bytes, 堆上)   │
│    │                        │
│    ▼                        │
│ ┌──────────────────────┐   │
│ │ Mark Word    (8 bytes)│   │
│ │ Klass Pointer (4 bytes)│  │  ← 对象头 = 12-16 bytes
│ ├──────────────────────┤   │
│ │ Field 1: int  (4 bytes)│  │
│ │ Field 2: int  (4 bytes)│  │
│ └──────────────────────┘   │
│                             │
│ 总开销: 16 (header) + 8 (data) = 24 bytes │
│ 实际有效数据仅 8 bytes (33%)              │
└─────────────────────────────┘

Value Class (无标识):
┌─────────────────────────────┐
│ Field 1: int  (4 bytes)     │  ← 无对象头!
│ Field 2: int  (4 bytes)     │
│                             │
│ 总开销: 8 bytes (100% 有效) │
│ 节省: 16 bytes (-67%)       │
└─────────────────────────────┘
```

### 2.2 "双赢"目标

```
"Codes like a class, works like an int"
                  — Brian Goetz

Value Classes 的设计目标:
┌────────────────────┬────────────────────┐
│  像 class          │  像 int            │
├────────────────────┼────────────────────┤
│  有方法            │  无对象头          │
│  有字段            │  扁平化存储        │
│  有泛型            │  无标识 (identity) │
│  有封装            │  按值传递          │
│  有接口            │  高性能            │
└────────────────────┴────────────────────┘
```

---

## 3. Value Classes vs Records vs Primitives

| 特性 | Primitive | Value Class | Record | Regular Class |
|------|-----------|-------------|--------|---------------|
| **标识 (Identity)** | 无 | 无 | 有 | 有 |
| **对象头** | 无 | 无 | 有 | 有 |
| **可变 (Mutable)** | N/A | 否 | 否 | 是 |
| **字段类型** | 固定 | 自定义 | 自定义 | 自定义 |
| **方法** | 无 | 有 | 有 | 有 |
| **接口** | 无 | 可实现 | 可实现 | 可实现 |
| **泛型支持** | 需装箱 | 直接 | 直接 | 直接 |
| **数组存储** | 扁平 | 扁平 | 引用 | 引用 |
| **== 语义** | 值比较 | 值比较 | 引用比较 | 引用比较 |
| **null** | 不可 | 不可 (null-restricted) | 可 | 可 |
| **同步** | 不可 | 不可 | 可 | 可 |

---

## 4. 语言模型

### 4.1 声明 Value Class

```java
// 使用 value 修饰符声明
value class Point implements Printable {
    int x;
    int y;

    // 可以有方法
    double distanceTo(Point other) {
        int dx = x - other.x;
        int dy = y - other.y;
        return Math.sqrt(dx * dx + dy * dy);
    }

    // 可以实现接口
    @Override
    public String print() {
        return "(" + x + ", " + y + ")";
    }
}
```

### 4.2 Null-Restricted Types

```java
// 使用 ! 标记 null-restricted
value class Point { int x; int y; }

// 普通引用: 可以为 null
Point maybeNull = null;  // ✅

// null-restricted: 不可以为 null
Point! notNull = Point.of(1, 2);  // ✅
Point! notNull = null;             // ❌ 编译错误
```

### 4.3 扁平化数组

```java
// 传统对象数组: 引用数组
Point[] points = new Point[1000];
// 每个元素 = 8 bytes 引用 + 24 bytes 对象 = 32KB 总计

// Value class 数组: 扁平化存储
Point![] flatPoints = new Point![1000];
// 每个元素 = 8 bytes 内联数据 = 8KB 总计
// 节省 75% 内存!
```

---

## 5. JVM 实现 (Q-Types)

### 5.1 Q-Types vs L-Types

```
传统类 (L-Types):
  Descriptor: Lcom/example/Point;
  存储: 堆上对象 + 引用

Value Classes (Q-Types):
  Descriptor: Qcom/example/Point;
  存储: 扁平化内联 (无引用间接)
```

### 5.2 字节码层面的变化

```
// 传统类的字段访问
getfield #Field com/example/Point.x  // 通过引用间接访问

// Value class 的字段访问
getfield #Field com/example/Point.x  // 直接内联访问 (无间接)

// 方法签名
// 传统: (Lcom/example/Point;)D
// Value: (Qcom/example/Point;)D
```

### 5.3 加载和链接

```
JVM 加载 value class:
┌─────────────────────────────────────────────────┐
│ 1. ClassParser 检查 value 修饰符                │
│ 2. 验证:                                        │
│    - 无 synchronized 方法                       │
│    - 无 wait/notify 调用                        │
│    - 所有字段为 final                           │
│    - 无父类 (extends Object 不允许, 隐式)       │
│    - 构造函数不使用 this 之前有 super()          │
│ 3. 创建 Q-type 类元数据                         │
│ 4. 生成内联存取字节码                           │
└─────────────────────────────────────────────────┘
```

---

## 6. 性能模型

### 6.1 内存节省

```
示例: 100 万个 Point 对象

Regular Class:
  1,000,000 × (16 header + 8 data) = 24MB
  + 数组引用: 1,000,000 × 8 = 8MB
  总计: ~32MB

Value Class:
  1,000,000 × 8 (data only) = 8MB
  总计: ~8MB
  节省: 75%
```

### 6.2 缓存局部性

```
Regular Class 数组 (引用):
┌──────┐     ┌─────────────────┐
│ ref0 │────►│ obj0 (heap)     │
│ ref1 │────►│ obj1 (heap)     │  ← 缓存不友好
│ ref2 │────►│ obj2 (heap)     │     (间接访问)
│ ...  │     │ ...             │
└──────┘     └─────────────────┘

Value Class 数组 (扁平):
┌──────────────────────────────┐
│ data0 | data1 | data2 | ... │  ← 缓存友好
└──────────────────────────────┘     (连续内存)
```

### 6.3 预期性能提升

| 场景 | 提升来源 | 预期改善 |
|------|---------|---------|
| 大数组遍历 | 缓存局部性 | 2-5x |
| 通用数据结构 (Optional, etc.) | 消除装箱 | 1.5-3x |
| Complex number 运算 | 扁平化 + 内联 | 3-10x |
| 泛型特化 | 消除装箱 | 2-5x |

---

## 7. 当前限制 (Preview)

JDK 26 的 Value Classes Preview 有以下限制：

| 限制 | 说明 |
|------|------|
| **不支持泛型特化** | `List<Point!>` 仍会装箱 (未来版本) |
| **不支持作为泛型类型参数** | 部分泛型场景受限 |
| **Preview 特性** | 需要 `--enable-preview` |
| **不支持同步** | value class 不能有 synchronized 方法 |
| **不支持 identity 操作** | 不能使用 `System.identityHashCode()`、`==` 引用比较 |
| **CDS 有限支持** | value class 的 CDS 归档支持有限 |

---

## 8. 演进路线

```
Valhalla 项目路线 (示意):
JDK 26 (2026-03)     Value Classes Preview (JEP 401)
        │
JDK 27 (2026-09)     Value Classes Second Preview
        │
JDK 28+              Value Classes Final
        │
Future               Specialized Generics (泛型特化)
                     (List<int>, List<Point!> 等)
```

### 历史演进

| 阶段 | 时间 | 里程碑 |
|------|------|--------|
| 提案 | 2017 | Brian Goetz 发布 "State of Valhalla" |
| 原型 | 2019 | LW1/LW2 原型 (内联类型) |
| 重新设计 | 2021 | 从 "Inline Types" 转向 "Value Classes" |
| JEP 草案 | 2023 | JEP 401 草案发布 |
| Preview | 2026 | JDK 26 Preview |

---

## 相关链接

- [Valhalla 主题](/by-topic/core/valhalla/)
- [Records 编译器实现](records-compiler-implementation.md)
- [Compact Object Headers (JEP 519)](jep-519-implementation.md)
- [内存管理主题](/by-topic/core/memory/)
