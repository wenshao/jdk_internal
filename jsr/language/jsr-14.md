# JSR 14: Add Generic Types to the Java Programming Language

> **状态**: ✅ Final | **JDK**: 5 (2004) | **Specification Lead**: Gilad Bracha

[← 返回 JSR 索引](../index.md) | [外部链接](https://jcp.org/en/jsr/detail?id=14)

---
## 目录

1. [一眼看懂](#1-一眼看懂)
2. [概述](#2-概述)
3. [设计决策：类型擦除 vs 具体化](#3-设计决策类型擦除-vs-具体化)
4. [核心特性](#4-核心特性)
5. [通配符与 PECS 原则](#5-通配符与-pecs-原则)
6. [类型擦除的影响](#6-类型擦除的影响)
7. [桥接方法与原始类型](#7-桥接方法与原始类型)
8. [对 Java 生态的影响](#8-对-java-生态的影响)
9. [与其他 JSR/JEP 的关系](#9-与其他-jsrjep-的关系)
10. [最佳实践](#10-最佳实践)
11. [相关链接](#11-相关链接)
12. [参考资料](#12-参考资料)

---

## 1. 一眼看懂

```
┌─────────────────────────────────────────────────────────────────────┐
│                    JSR 14 核心内容                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. 泛型类/接口          List<String>, Map<K, V>                    │
│  2. 有界类型参数          <T extends Comparable<T>>                  │
│  3. 通配符               ? extends / ? super                        │
│  4. 泛型方法             <T> T max(Collection<? extends T> coll)    │
│  5. 类型擦除             编译后泛型信息被擦除                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. 概述

JSR 14 为 Java 引入了泛型（Generics），是 JDK 5 最具影响力的语言特性之一：

| 特性 | 说明 |
|------|------|
| **泛型类型** | 类和接口的参数化类型（Parameterized Types） |
| **有界类型参数** | 对类型参数施加约束（Bounded Type Parameters） |
| **通配符** | 灵活的类型子类化关系（Wildcards） |
| **泛型方法** | 方法级别的类型参数 |
| **类型擦除** | 编译期检查，运行时擦除（Type Erasure） |

---

## 3. 设计决策：类型擦除 vs 具体化

JSR 14 最关键也最具争议的决策——选择**类型擦除（Type Erasure）**而非 C# 的**具体化（Reification）**：

### 为什么选择擦除

| 考量因素 | 类型擦除 (Java) | 具体化 (C#) |
|----------|-----------------|-------------|
| **二进制兼容性** | ✅ 完全兼容旧字节码 | ❌ 需要新 CLR |
| **迁移兼容性** | ✅ `List` 和 `List<String>` 互操作 | ❌ `List` 与 `List<T>` 完全不同类型 |
| **JVM 改动** | ✅ 零改动 | ❌ 需要虚拟机支持 |
| **运行时类型信息** | ❌ 丢失泛型信息 | ✅ 完整保留 |
| **基本类型支持** | ❌ 不支持 `List<int>` | ✅ 支持 `List<int>` |

```java
// 擦除的本质：编译器视角 vs JVM 视角
// 源码
List<String> names = new ArrayList<>();
names.add("Java");
String s = names.get(0);

// 擦除后等价于 (JVM 看到的)
List names = new ArrayList();
names.add("Java");
String s = (String) names.get(0);  // 编译器自动插入 checkcast
```

Gilad Bracha 的设计哲学：**泛型应当是纯粹的编译期机制**，不应改变运行时语义。这保证了 JDK 5 之前的所有库和框架无需任何修改即可继续运行。

---

## 4. 核心特性

### 泛型类与接口

```java
// 泛型类
public class Pair<A, B> {
    private final A first;
    private final B second;
    public Pair(A first, B second) { this.first = first; this.second = second; }
    public A getFirst() { return first; }
    public B getSecond() { return second; }
}

// 泛型接口
public interface Comparable<T> {
    int compareTo(T o);
}
```

### 有界类型参数（Bounded Type Parameters）

```java
// 上界 (Upper Bound)
public <T extends Comparable<T>> T max(Collection<T> coll) {
    T result = null;
    for (T t : coll) {
        if (result == null || t.compareTo(result) > 0) result = t;
    }
    return result;
}

// 多重上界 (Multiple Bounds)
public <T extends Serializable & Comparable<T>> void process(T item) { ... }
// 注意: 类必须在第一个位置，接口在后
```

### 泛型方法

```java
// 类型推断 (Type Inference)
public static <T> List<T> singletonList(T item) {
    return Collections.singletonList(item);
}

// JDK 5 需要显式指定
List<String> list = Collections.<String>singletonList("hello");

// JDK 7+ 菱形推断
List<String> list = new ArrayList<>();

// JDK 8+ Lambda 推断进一步增强
```

---

## 5. 通配符与 PECS 原则

### 通配符类型（Wildcards）

```java
// 无界通配符 - 只读，类型未知
void printAll(List<?> list) {
    for (Object o : list) System.out.println(o);
}

// 上界通配符 (Upper Bounded) - 协变 (Covariant)
void sumOfNumbers(List<? extends Number> nums) {
    double sum = 0;
    for (Number n : nums) sum += n.doubleValue();
}

// 下界通配符 (Lower Bounded) - 逆变 (Contravariant)
void addIntegers(List<? super Integer> list) {
    list.add(1);
    list.add(2);
}
```

### PECS 原则 (Producer Extends, Consumer Super)

Joshua Bloch 在《Effective Java》中总结的黄金法则：

```java
// Producer Extends: 从集合读取 → 用 extends
public static <T> void copy(
    List<? super T> dest,        // Consumer: 写入 dest → super
    List<? extends T> src         // Producer: 读取 src  → extends
) { ... }

// 实际应用
List<Number> numbers = new ArrayList<>();
List<Integer> integers = Arrays.asList(1, 2, 3);
Collections.copy(numbers, integers);  // Integer extends Number
```

---

## 6. 类型擦除的影响

### 擦除导致的限制

```java
// ❌ 不能创建泛型数组
T[] arr = new T[10];                    // 编译错误

// ❌ 不能用 instanceof 检查泛型类型
if (obj instanceof List<String>) { }    // 编译错误

// ❌ 不能使用基本类型
List<int> list;                         // 编译错误，必须用 List<Integer>

// ❌ 运行时无法区分泛型类型
List<String>.class == List<Integer>.class  // true，都是 List.class

// ❌ 不能重载仅泛型参数不同的方法
void process(List<String> list) { }
void process(List<Integer> list) { }    // 编译错误: 擦除后签名相同
```

### 类型安全的数组替代

```java
// 数组是协变的 (有风险)
Object[] arr = new String[10];
arr[0] = 42;  // 运行时 ArrayStoreException!

// 泛型是不变的 (编译期安全)
List<Object> list = new ArrayList<String>();  // 编译错误 ✓
```

---

## 7. 桥接方法与原始类型

### 桥接方法（Bridge Methods）

```java
// 源码
public class StringComparable implements Comparable<String> {
    public int compareTo(String o) { return 0; }
}

// 编译器生成桥接方法保持多态
public class StringComparable implements Comparable {
    public int compareTo(String o) { return 0; }             // 真实方法
    public int compareTo(Object o) { return compareTo((String) o); }  // 桥接方法 (synthetic)
}
```

### 原始类型（Raw Types）

```java
// 原始类型: 向后兼容 JDK 1.4 代码
List rawList = new ArrayList();    // 原始类型，无泛型参数
rawList.add("hello");
rawList.add(42);                   // 编译器警告，但允许

// 泛型与原始类型的交互
List<String> typed = rawList;      // unchecked 警告
String s = typed.get(1);           // 运行时 ClassCastException!
```

---

## 8. 对 Java 生态的影响

### Collections Framework 重写

```java
// JDK 1.4 (无泛型)
List list = new ArrayList();
list.add("hello");
String s = (String) list.get(0);  // 需要强制转换

// JDK 5 (有泛型)
List<String> list = new ArrayList<String>();
list.add("hello");
String s = list.get(0);           // 无需转换，编译期类型安全
```

### 类型安全 API 设计

| 框架/API | 泛型应用 |
|----------|----------|
| **Collections** | `List<E>`, `Map<K,V>`, `Set<E>` |
| **Comparable/Comparator** | `Comparable<T>`, `Comparator<T>` |
| **Class 字面量** | `Class<T>` 类型令牌（Type Token） |
| **ThreadLocal** | `ThreadLocal<T>` |
| **Future/Callable** | `Future<V>`, `Callable<V>` |

---

## 9. 与其他 JSR/JEP 的关系

### 泛型的演进

| 版本 | 增强 | 说明 |
|------|------|------|
| JDK 5 | JSR 14 | 泛型基础 |
| JDK 7 | 菱形推断 | `new ArrayList<>()` |
| JDK 8 | 目标类型推断 | Lambda 上下文推断 |
| JDK 10 | `var` 局部变量 | 编译器推断泛型类型 |

### Valhalla 项目：泛型的未来

Project Valhalla（JEP 402: Enhanced Primitive Boxing / Unified Generics）计划解决类型擦除的历史遗留问题：

| 特性 | 说明 |
|------|------|
| **泛型特化** | `List<int>` 直接支持基本类型，无需装箱 |
| **值类型泛型** | Value Types 与泛型的统一 |
| **运行时泛型信息** | 部分恢复被擦除的类型信息 |

这将是 Java 泛型自 JSR 14 以来最大的革新，有望在 JDK 25+ 逐步交付。

---

## 10. 最佳实践

### 1. 优先使用泛型集合

```java
// 不推荐
List list = new ArrayList();

// 推荐
List<String> list = new ArrayList<>();
```

### 2. 遵循 PECS 原则设计 API

```java
// 不推荐: 限制过严
public void process(List<Number> nums) { }

// 推荐: 灵活的通配符
public void process(List<? extends Number> nums) { }
```

### 3. 使用类型令牌（Type Token）

```java
// 类型安全的异构容器
public class Favorites {
    private Map<Class<?>, Object> map = new HashMap<>();
    public <T> void put(Class<T> type, T instance) {
        map.put(type, type.cast(instance));
    }
    public <T> T get(Class<T> type) {
        return type.cast(map.get(type));
    }
}
```

---

## 11. 相关链接

### 官方资源

- [JSR 14 规范](https://jcp.org/en/jsr/detail?id=14)
- [Generics Tutorial (Oracle)](https://docs.oracle.com/javase/tutorial/java/generics/)
- [Generics FAQ - Angelika Langer](http://www.angelikalanger.com/GenericsFAQ/JavaGenericsFAQ.html)

### 本地文档

- [泛型深入分析](/by-topic/language/generics/)
- [JDK 5 新特性](/by-version/jdk5/)
- [Project Valhalla](/projects/valhalla/)

---

## 12. 参考资料

- **Gilad Bracha**, JSR 14 Specification Lead
- **Philip Wadler**, 泛型类型系统理论贡献
- 《Effective Java》第 5 章 - Joshua Bloch
- 《Java Generics and Collections》- Maurice Naftalin, Philip Wadler

---

> **最后更新**: 2026-03-22
