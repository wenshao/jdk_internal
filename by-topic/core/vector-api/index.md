# Vector API (SIMD 向量化)

> **状态**: 🥚 Incubator | **模块**: jdk.incubator.vector | **JEP**: 338, 414, 417, 426, 448, 460

[← 返回核心](..) | [时间线](timeline.md) | [使用指南](usage.md)

---

## 一眼看懂

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Vector API 概览                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  传统标量计算                    Vector API 向量化                   │
│  ┌─────────────────┐            ┌─────────────────┐                │
│  │ for (int i=0;i<n;i++)        │ VectorSpecies    │                │
│  │   c[i]=a[i]+b[i] │   ───►    │ VectorMask       │                │
│  │   // 逐元素计算   │            │ 128/256/512 bit  │                │
│  └─────────────────┘            └─────────────────┘                │
│                                                                     │
│  性能提升: 2x - 8x (取决于 CPU 架构和向量宽度)                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 概述

Vector API 提供了一种在 Java 中编写可移植 SIMD (Single Instruction Multiple Data) 代码的方式，无需编写平台特定的本地代码。

### 核心优势

| 特性 | 说明 |
|------|------|
| **可移植性** | 一次编写，在任何支持 SIMD 的 CPU 上运行 |
| **类型安全** | 编译时类型检查，避免本地代码的错误 |
| **JIT 优化** | C2 编译器自动映射到最优向量指令 |
| **跨平台** | x86 (AVX/SSE), ARM (NEON/SVE), RISC-V (V) |

### 支持的类型

| 类型 | 向量类 | 位宽 |
|------|--------|------|
| byte | ByteVector | 64, 128, 256, 512, Max |
| short | ShortVector | 64, 128, 256, 512, Max |
| int | IntVector | 64, 128, 256, 512, Max |
| long | LongVector | 64, 128, 256, 512, Max |
| float | FloatVector | 64, 128, 256, 512, Max |
| double | DoubleVector | 64, 128, 256, 512, Max |

---

## 快速示例

### 基础向量加法

```java
import jdk.incubator.vector.*;

public class VectorAdd {
    static final VectorSpecies<Float> SPECIES = FloatVector.SPECIES_PREFERRED;
    
    public static void vectorAdd(float[] a, float[] b, float[] c) {
        int i = 0;
        int upperBound = SPECIES.loopBound(a.length);
        
        // 向量化循环
        for (; i < upperBound; i += SPECIES.length()) {
            FloatVector va = FloatVector.fromArray(SPECIES, a, i);
            FloatVector vb = FloatVector.fromArray(SPECIES, b, i);
            va.add(vb).intoArray(c, i);
        }
        
        // 处理尾部元素
        for (; i < a.length; i++) {
            c[i] = a[i] + b[i];
        }
    }
}
```

### 带 Mask 的条件计算

```java
static void vectorMulMasked(float[] a, float[] b, float[] c, boolean[] mask) {
    VectorSpecies<Float> species = FloatVector.SPECIES_256;
    VectorMask<Float> vmask = VectorMask.fromArray(species, mask, 0);
    
    FloatVector va = FloatVector.fromArray(species, a, 0);
    FloatVector vb = FloatVector.fromArray(species, b, 0);
    
    // 只对 mask 中为 true 的位置执行乘法
    va.mul(vb, vmask).intoArray(c, 0);
}
```

### 向量点积

```java
static float dotProduct(float[] a, float[] b) {
    VectorSpecies<Float> species = FloatVector.SPECIES_256;
    FloatVector sum = FloatVector.zero(species);
    
    int i = 0;
    for (; i < species.loopBound(a.length); i += species.length()) {
        FloatVector va = FloatVector.fromArray(species, a, i);
        FloatVector vb = FloatVector.fromArray(species, b, i);
        sum = sum.add(va.mul(vb));
    }
    
    // 水平归约
    float result = sum.reduceLanes(VectorOperators.ADD);
    
    // 尾部处理
    for (; i < a.length; i++) {
        result += a[i] * b[i];
    }
    
    return result;
}
```

---

## 核心概念

### VectorSpecies (向量种类)

定义向量的形状和元素类型：

```java
// 预定义种类
FloatVector.SPECIES_64     // 64-bit 向量 (2 floats)
FloatVector.SPECIES_128    // 128-bit 向量 (4 floats)
FloatVector.SPECIES_256    // 256-bit 向量 (8 floats)
FloatVector.SPECIES_512    // 512-bit 向量 (16 floats)
FloatVector.SPECIES_MAX    // 最大可用向量宽度
FloatVector.SPECIES_PREFERRED  // 平台最优宽度
```

### VectorMask (向量掩码)

控制哪些通道参与操作：

```java
// 创建 mask
VectorMask<Float> mask = VectorMask.ofTrue(species);       // 全 true
VectorMask<Float> mask = VectorMask.ofFalse(species);      // 全 false
VectorMask<Float> mask = VectorMask.fromArray(species, bools, 0);  // 从数组
VectorMask<Float> mask = va.compare(VectorOperators.GT, vb);  // 比较

// 使用 mask
va.add(vb, mask);  // 只在 mask=true 的位置相加
```

### VectorShuffle (向量重排)

重排向量元素：

```java
// 创建 shuffle
VectorShuffle<Float> shuffle = VectorShuffle.fromArray(species, indices, 0);

// 应用 shuffle
FloatVector rearranged = va.rearrange(shuffle);
```

---

## 支持的操作

### 算术运算

| 操作 | 方法 | 示例 |
|------|------|------|
| 加法 | `add()` | `va.add(vb)` |
| 减法 | `sub()` | `va.sub(vb)` |
| 乘法 | `mul()` | `va.mul(vb)` |
| 除法 | `div()` | `va.div(vb)` |
| 取负 | `neg()` | `va.neg()` |
| 绝对值 | `abs()` | `va.abs()` |

### 数学函数

| 函数 | 方法 |
|------|------|
| sin | `lanewise(VectorOperators.SIN)` |
| cos | `lanewise(VectorOperators.COS)` |
| sqrt | `lanewise(VectorOperators.SQRT)` |
| log | `lanewise(VectorOperators.LOG)` |
| exp | `lanewise(VectorOperators.EXP)` |

### 位运算

| 操作 | 方法 |
|------|------|
| AND | `and()` |
| OR | `or()` |
| XOR | `xor()` |
| NOT | `not()` |
| 左移 | `lanewise(VectorOperators.LSHL, n)` |
| 右移 | `lanewise(VectorOperators.LSHR, n)` |

### 比较操作

```java
VectorMask<Float> m1 = va.compare(VectorOperators.GT, vb);  // >
VectorMask<Float> m2 = va.compare(VectorOperators.EQ, vb);  // ==
VectorMask<Float> m3 = va.compare(VectorOperators.LT, vb);  // <
```

### 归约操作

```java
float sum = va.reduceLanes(VectorOperators.ADD);      // 求和
float max = va.reduceLanes(VectorOperators.MAX);      // 最大值
float min = va.reduceLanes(VectorOperators.MIN);      // 最小值
float xor = va.reduceLanes(VectorOperators.XOR);      // 异或
```

---

## 性能考量

### CPU 架构支持

| 架构 | 指令集 | 最大宽度 |
|------|--------|----------|
| x86-64 | SSE/AVX/AVX2/AVX-512 | 512-bit |
| ARM64 | NEON/SVE/SVE2 | 可变 (最多 2048-bit) |
| RISC-V | V 扩展 | 可变 |
| AArch64 | ASIMD | 128-bit |

### 性能建议

1. **使用 SPECIES_PREFERRED** - 让 JVM 选择最优宽度
2. **对齐数据** - 64 字节对齐可提升 AVX-512 性能
3. **避免频繁装箱** - 使用原始类型数组
4. **合理处理尾部** - `loopBound()` + 标量循环

### 性能对比示例

```java
// 标量版本
void scalarSAXPY(float[] a, float[] x, float[] y, float alpha) {
    for (int i = 0; i < a.length; i++) {
        a[i] = alpha * x[i] + y[i];
    }
}

// 向量版本 (AVX-512: 16 floats/iteration)
void vectorSAXPY(float[] a, float[] x, float[] y, float alpha) {
    VectorSpecies<Float> species = FloatVector.SPECIES_PREFERRED;
    int i = 0;
    int bound = species.loopBound(a.length);
    
    for (; i < bound; i += species.length()) {
        FloatVector vx = FloatVector.fromArray(species, x, i);
        FloatVector vy = FloatVector.fromArray(species, y, i);
        FloatVector va = vx.mul(alpha).add(vy);
        va.intoArray(a, i);
    }
    
    for (; i < a.length; i++) {
        a[i] = alpha * x[i] + y[i];
    }
}

// 性能: 向量版比标量版快 4-8 倍 (取决于向量宽度)
```

---

## 与 Valhalla 的协同

Vector API 与 Valhalla 值类型天然契合：

```java
// 未来: 值类型 + 向量化
value record Point(float x, float y) {}

// 期望的向量化操作
Point[] points = ...;
FloatVector vx = FloatVector.fromArray(species, points.xArray(), 0);
FloatVector vy = FloatVector.fromArray(species, points.yArray(), 0);
```

**协同优势**:
- 扁平化数组 → 连续内存 → 高效向量加载
- 无对象头开销 → 更好的缓存利用
- 值类型内联 → 减少间接访问

---

## 运行要求

### 编译

```bash
# JDK 16+
javac --add-modules jdk.incubator.vector VectorAdd.java
```

### 运行

```bash
# JDK 16-23 (incubator)
java --add-modules jdk.incubator.vector --enable-preview VectorAdd

# JDK 24+ (可能不再是 incubator)
java --add-modules jdk.incubator.vector VectorAdd
```

### JVM 参数

```bash
# 禁用向量化 (调试用)
-XX:UseVectorStubs=0

# 打印向量指令
-XX:+PrintAssembly

# 限制向量宽度
-XX:MaxVectorSize=256
```

---

## 相关链接

### 官方资源

- [JEP 338: Vector API (Incubator)](https://openjdk.org/jeps/338)
- [JEP 414: Vector API (Second Incubator)](https://openjdk.org/jeps/414)
- [JEP 417: Vector API (Third Incubator)](https://openjdk.org/jeps/417)
- [JEP 426: Vector API (Fourth Incubator)](https://openjdk.org/jeps/426)
- [JEP 448: Vector API (Fifth Incubator)](https://openjdk.org/jeps/448)
- [JEP 460: Vector API (Sixth Incubator)](https://openjdk.org/jeps/460)

### 本地文档

- [时间线](timeline.md) - 版本演进历史
- [使用指南](usage.md) - 详细使用示例

### 源码位置

- JDK 源码: `src/jdk.incubator.vector/share/classes/jdk/incubator/vector/`
- 测试: `test/jdk/jdk/incubator/vector/`

---

## 版本状态

| 版本 | JEP | 状态 |
|------|-----|------|
| JDK 16 | 338 | 🥚 First Incubator |
| JDK 17 | 414 | 🥚 Second Incubator |
| JDK 18 | 417 | 🥚 Third Incubator |
| JDK 19 | 426 | 🥚 Fourth Incubator |
| JDK 20 | 448 | 🥚 Fifth Incubator |
| JDK 21 | 460 | 🥚 Sixth Incubator |
| JDK 22-24 | - | 🥚 继续孵化中 |
| JDK 25+ | - | ⏳ 期望成为标准 API |

---

> **最后更新**: 2026-03-20
