# Compact Object Headers 深度分析

> JDK 25 实验性特性 - JEP 519

---
## 目录

1. [概述](#1-概述)
2. [对象头布局演进](#2-对象头布局演进)
3. [紧凑布局设计](#3-紧凑布局设计)
4. [实现机制](#4-实现机制)
5. [内存节省分析](#5-内存节省分析)
6. [启用与验证](#6-启用与验证)
7. [限制与注意事项](#7-限制与注意事项)
8. [相关链接](#8-相关链接)

---


## 1. 概述

JEP 519 将 Java 对象的对象头从传统的 12-16 字节压缩至 8 字节，减少约 33-50% 的对象头开销。在对象密集型应用中，这可以显著降低堆内存使用和 GC 压力。

---

## 2. 对象头布局演进

### 传统布局 (JDK 24 及之前)

```
64-bit JVM (compressed oops):
┌───────────────────────────────────────────┐
│ Mark Word (8 bytes)                       │ ← 锁状态、GC 年龄、hashCode
├───────────────────────────────────────────┤
│ Klass Pointer (4 bytes, compressed)       │ ← 类型指针
├───────────────────────────────────────────┤
│ [Padding] (4 bytes, 如需对齐)              │
├───────────────────────────────────────────┤
│ Instance Fields...                        │
└───────────────────────────────────────────┘

总对象头: 12 bytes (+ 4 padding = 16 bytes aligned)
```

### Mark Word 位布局 (传统)

```
64-bit Mark Word:
┌──────────────────────────────────────────────────────────┐
│ unused:25 │ hashCode:31 │ unused:1 │ age:4 │ biased:1 │ lock:2 │
└──────────────────────────────────────────────────────────┘
```

---

## 3. 紧凑布局设计

### JEP 519 布局

```
Compact Object Header (8 bytes total):
┌───────────────────────────────────────────┐
│ Mark Word + Klass (8 bytes combined)      │
├───────────────────────────────────────────┤
│ Instance Fields...                        │
└───────────────────────────────────────────┘

总对象头: 8 bytes
```

### 紧凑 Mark Word 位布局

```
64-bit Compact Header:
┌─────────────────────────────────────────────────────────────┐
│ hashCode:25 │ age:4 │ self-fwd:1 │ narrowKlass:22 │ lock:2 │
│   或                                                        │
│ forwarding pointer:62                              │ lock:2 │
└─────────────────────────────────────────────────────────────┘
```

**关键设计决策**:
- `narrowKlass` (22 bits): 类型指针压缩编码，支持最多 ~400 万个类
- `hashCode` (25 bits): 缩短为 25 位（传统 31 位）
- `age` (4 bits): GC 分代年龄，不变
- `self-fwd` (1 bit): GC 转发标记
- `lock` (2 bits): 锁状态

---

## 4. 实现机制

### narrowKlass 编码

```cpp
// HotSpot 源码: src/hotspot/share/oops/compressedKlass.hpp
// 22 位可编码 4,194,304 个不同的 Klass*

// 编码
inline narrowKlass encode(Klass* klass) {
    return (narrowKlass)((uintptr_t)klass - _base) >> _shift;
}

// 解码
inline Klass* decode(narrowKlass v) {
    return (Klass*)(_base + ((uintptr_t)v << _shift));
}
```

### hashCode 处理

由于 hashCode 缩短为 25 位，`System.identityHashCode()` 的值域从 2^31 缩小为 2^25 (~3300 万)：

```java
// 碰撞概率分析
// 25-bit hashCode: 33,554,432 个可能值
// 在 10,000 个对象时碰撞概率 < 0.15%
// 在 100,000 个对象时碰撞概率 ~15%

// 对 HashMap 性能的影响:
// - 小型 HashMap (<10K entries): 基本无影响
// - 大型 HashMap (>100K entries): 略微增加碰撞，但链表/红黑树处理
```

### 锁状态编码

```
lock bits (2 bits):
  00 = Lightweight locked
  01 = Unlocked / Monitor-less
  10 = Monitor (heavyweight lock)
  11 = GC forwarded
```

偏向锁已在 JDK 15 移除，紧凑对象头不再为其预留空间。

---

## 5. 内存节省分析

### 每对象节省

| 场景 | 传统对象头 | 紧凑对象头 | 节省 |
|------|-----------|-----------|------|
| 对齐后 16 字节 | 16 bytes | 8 bytes | 8 bytes (50%) |
| 对齐后 12 字节 | 12 bytes | 8 bytes | 4 bytes (33%) |

### 典型数据结构影响

```
HashMap.Node (传统):
  对象头: 16 bytes
  hash:    4 bytes
  key:     8 bytes (ref)
  value:   8 bytes (ref)
  next:    8 bytes (ref)
  总计:    44 bytes → 对齐后 48 bytes

HashMap.Node (紧凑):
  对象头:  8 bytes
  hash:    4 bytes
  key:     8 bytes (ref)
  value:   8 bytes (ref)
  next:    8 bytes (ref)
  总计:    36 bytes → 对齐后 40 bytes

节省: 每个 Node 节省 8 bytes (17%)
```

---

## 6. 启用与验证

### 启用

```bash
java -XX:+UnlockExperimentalVMOptions \
     -XX:+UseCompactObjectHeaders \
     MyApp
```

### 验证

```bash
# 方法 1: JVM 启动日志
java -XX:+UnlockExperimentalVMOptions \
     -XX:+UseCompactObjectHeaders \
     -Xlog:oopsstorage \
     -version

# 方法 2: JOL (Java Object Layout)
# 添加依赖: org.openjdk.jol:jol-core:0.17
java -XX:+UnlockExperimentalVMOptions \
     -XX:+UseCompactObjectHeaders \
     -jar jol-cli.jar internals java.lang.String
```

---

## 7. 限制与注意事项

| 限制 | 说明 |
|------|------|
| 实验性 | 默认关闭，需显式启用 |
| hashCode 位宽 | 25 位 vs 传统 31 位，大量对象时碰撞率略高 |
| JNI 兼容 | 直接操作对象头的 JNI 代码需要适配 |
| Unsafe 访问 | `Unsafe.objectFieldOffset()` 偏移量可能变化 |
| APM 工具 | 部分字节码增强工具需要更新 |

---

## 8. 相关链接

- [JEP 519: Compact Object Headers](https://openjdk.org/jeps/519)
- [Compact Object Headers 完整实现分析](/deep-dive/jep-519-implementation.md)
- [JDK 25 性能调优](../performance.md)
- [内存管理演进](/by-topic/core/memory/)

---

[← 返回 JDK 25 深度分析](../)
