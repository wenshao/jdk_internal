# Valhalla: Value Types (值类型)

> **状态**: 🚧 开发中 | **分支**: lworld | **仓库**: openjdk/valhalla

---

## 概述

Project Valhalla 是 OpenJDK 最重要的孵化项目之一，致力于为 Java 引入**值类型 (Value Types)**。这是 Java 语言自泛型以来最大的变革之一。

> **注意**: Value Types 目前尚未成为正式 JSR，仍在 OpenJDK Valhalla 项目中孵化。

---

## 历史背景

### 时间线

| 年份 | 里程碑 | 说明 |
|------|--------|------|
| **2014** | Valhalla 项目启动 | Brian Goetz 发起 |
| **2015** | JEP 169: Value Types | 早期探索 |
| **2017** | JEP 325: Value Types | 第一次正式提案 |
| **2018** | JEP 338: Value Types | 更新提案 |
| **2019** | JEP 390: Warnings for Value-Based Classes | 警告注解 |
| **2020** | 原型开发 | lworld 分支活跃开发 |
| **2021** | JEP 390 正式发布 | JDK 16 |
| **2022** | JEP 401: Value Classes | 新方向 |
| **2023** | JEP 401 预览 | 计划中 |
| **2026** | 目标发布 | JDK 25+ |

### 设计目标

1. **消除装箱开销**: 值类型没有对象头
2. **平坦化布局**: 值类型字段直接内联
3. **与泛型配合**: 泛型特化 (Specialization)
4. **保持对象语义**: equals, hashCode, toString

---

## 核心概念

### Identity vs Value

```
┌─────────────────────────────────────────────────────────────────┐
│                    Java 对象模型                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Identity Objects (身份对象)                                   │
│   ┌──────────────────┐                                         │
│   │ Object Header    │  ← 16 字节开销                          │
│   │ Fields...        │                                         │
│   └──────────────────┘                                         │
│   - 可比较身份 (==)                                             │
│   - 可变或不可变                                                │
│   - 同步、finalization                                         │
│                                                                 │
│   Value Objects (值对象)                                        │
│   ┌──────────────────┐                                         │
│   │ Fields...        │  ← 无对象头                             │
│   └──────────────────┘                                         │
│   - 无身份 (只有状态)                                           │
│   - 不可变                                                      │
│   - 无同步                                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 语法预览 (JEP 401)

```java
// 值类声明
value record Point(int x, int y) { }

// 或使用 value class
value class Complex {
    private final double re, im;
    
    public Complex(double re, double im) {
        this.re = re;
        this.im = im;
    }
    
    public double re() { return re; }
    public double im() { return im; }
}

// Null-Restricted 字段
class Container {
    @NullRestricted
    Point location;  // 不能为 null，平坦化存储
}
```

---

## 源码分析

### jdk.internal.value.ValueClass

```java
// 来源: src/java.base/share/classes/jdk/internal/value/ValueClass.java
package jdk.internal.value;

/**
 * 值类型工具类
 */
public final class ValueClass {
    
    /// 检查字段类型是否可存储值对象
    public static boolean isValueObjectCompatible(Class<?> fieldType) {
        return PreviewFeatures.isEnabled()
                && !fieldType.isPrimitive()
                && (!fieldType.isIdentity() || fieldType == Object.class);
    }
    
    /// 检查是否为具体值类
    public static boolean isConcreteValueClass(Class<?> clazz) {
        return clazz.isValue() && !Modifier.isAbstract(clazz.getModifiers());
    }
    
    /// 检查是否有二进制负载 (平坦化)
    public static boolean hasBinaryPayload(Class<?> c) {
        if (!ValueClass.isConcreteValueClass(c))
            return c.isPrimitive();
        return Unsafe.getUnsafe().isFlatPayloadBinary(c);
    }
    
    /// 分配 Null-Restricted 数组
    @IntrinsicCandidate
    public static native Object[] newNullRestrictedAtomicArray(
        Class<?> componentType, int length);
}
```

### LooselyConsistentValue 注解

```java
// 来源: src/java.base/share/classes/jdk/internal/vm/annotation/LooselyConsistentValue.java
/**
 * 标记一个值类可以容忍数据竞争导致的不一致。
 * 
 * 这允许 JVM 使用非原子策略读写平坦化字段和数组。
 */
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface LooselyConsistentValue { }
```

---

## 相关 JEP

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| JEP 169 | Value Types | - | 探索 |
| JEP 325 | Value Types | - | 草案 |
| JEP 338 | Value Types | - | 草案 |
| JEP 390 | Warnings for Value-Based Classes | 16 | ✅ 正式 |
| JEP 401 | Value Classes (Preview) | TBD | 🚧 开发中 |
| JEP 402 | Enhanced Value Types | TBD | 🚥 计划中 |

### JEP 390: Value-Based Classes

JDK 16 发布，为值类型做准备：

```java
@jdk.internal.ValueBased
public final class Optional<T> { ... }

@jdk.internal.ValueBased
public final class LocalDateTime { ... }
```

**警告**: 在值类型实例上使用同步会触发警告。

---

## 性能影响

### 内存布局对比

```
传统对象:
┌────────────────────────────────────┐
│ Mark Word (8 bytes)                │
│ Class Pointer (4/8 bytes)          │
│ Fields...                          │
└────────────────────────────────────┘

值对象:
┌────────────────────────────────────┐
│ Fields...                          │
└────────────────────────────────────┘
```

### 示例: Point 类

```java
// 传统类
class Point { int x, y; }  // 16 字节头 + 8 字节字段 = 24 字节

// 值类
value record Point(int x, int y) { }  // 8 字节字段 (无头)
```

### 数组布局

```java
// Point[1000] 传统数组
// 1000 * 24 bytes = 24 KB (加上引用)

// Point[1000] 值数组
// 1000 * 8 bytes = 8 KB (平坦化)
```

---

## 测试文件参考

```
test/jdk/valhalla/valuetypes/
├── NullRestrictedTest.java        # Null-Restricted 测试
├── NullRestrictedArraysTest.java  # Null-Restricted 数组
├── SubstitutabilityTest.java      # 可替代性测试
├── ValueClassPreviewTest.java     # 预览特性测试
├── Reflection.java                # 反射支持
├── MethodHandleTest.java          # MethodHandle 支持
└── StreamTest.java                # Stream 集成
```

---

## 开发进度

### lworld 分支活跃开发

```bash
# 最近提交 (2026-03)
8379863: C2: assert(!value->obj_is_scalar_replaced())
8380015: ValueRandomLayoutTest divides by zero
8343835: C2: assert fails with mismatched stores
8379333: JNI NewWeakGlobalRef should throw IdentityException
```

### 关键里程碑

- [x] 值类语法解析
- [x] 平坦化字段布局
- [x] Null-Restricted 支持
- [ ] 泛型特化
- [ ] 完整预览发布

---

## 与其他 JSR 的关系

| JSR | 关系 |
|-----|------|
| **JSR 395 (Records)** | Records 可以是值类 |
| **JSR 397 (Sealed)** | 值类可以是密封的 |
| **泛型特化** | 值类型启用 `List<int>` |

---

## 相关链接

- [OpenJDK Valhalla](https://openjdk.org/projects/valhalla/)
- [JEP 401: Value Classes](https://openjdk.org/jeps/401)
- [Valhalla Wiki](https://wiki.openjdk.org/display/valhalla/Main)
- [本地文档](/by-topic/core/valhalla/)

---

## 参考

- Brian Goetz, "Value Types: The Past, Present, and Future"
- John Rose, "Value Types HotSpot Implementation"
