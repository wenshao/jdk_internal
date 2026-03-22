# Vector API (SIMD 向量化)

> **状态**: 🥚 Incubator | **模块**: jdk.incubator.vector | **JEP**: 338, 414, 417, 426, 438, 448, 460, 469, 489, 508, 529

[← 返回核心](..) | [时间线](timeline.md) | [使用指南](usage.md) | [平台支持](platform.md) | [贡献者](contributors.md) | [各版本详情](versions.md)

> **注意**: 研究者常见问题已整合到本文档中。**已删除**: ~~research-faq.md~~ (内容已整合到主文档)

---

## 目录

1. [一眼看懂](#一眼看懂)
2. [SIMD 基础](#simd-基础)
3. [概述](#概述)
4. [快速示例](#快速示例)
5. [核心概念](#核心概念-core-concepts)
6. [支持的类型与形状](#支持的类型与形状)
7. [支持的操作](#支持的操作)
8. [性能考量](#性能考量)
9. [与 C2 自动向量化对比](#与-c2-自动向量化对比)
10. [与 Valhalla 的协同](#与-valhalla-的协同)
11. [AI/ML 浮点格式](#aiml-浮点格式)
12. [C2 编译器内部](#c2-编译器内部)
13. [性能基准测试](#性能基准测试)
14. [Valhalla/Babylon 集成](#valhallababylon-集成)
15. [研究者常见问题](#研究者常见问题)
16. [运行要求](#运行要求)
17. [相关链接](#相关链接)
18. [版本状态](#版本状态)
19. [为什么孵化这么慢](#为什么孵化这么慢)
20. [平台支持详解](#平台支持详解)
21. [JEP 路线图](#jep-路线图)
---

## 1. 一眼看懂

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

**一句话总结**: Java 向量 API，让 Java 代码在支持 SIMD 的 CPU 上获得接近 C/C++ 的性能，无需编写本地代码

---

## 2. SIMD 基础

### 什么是 SIMD (Single Instruction Multiple Data)

SIMD 是一种 CPU 并行计算模式 (parallel computing paradigm)：一条指令同时操作多个数据元素。

```
标量执行 (Scalar / SISD):            SIMD 执行:
  a[0] + b[0] → c[0]   (1 条指令)      a[0..7] + b[0..7] → c[0..7]  (1 条指令)
  a[1] + b[1] → c[1]   (1 条指令)      ─── 同时完成 8 个加法 ───
  a[2] + b[2] → c[2]   (1 条指令)
  ...                                  吞吐量 (throughput): 8x
  a[7] + b[7] → c[7]   (1 条指令)
  ─── 共 8 条指令 ───
```

**关键术语**:
- **Lane (通道)**: 向量寄存器 (vector register) 中的一个数据槽位。256-bit 寄存器有 8 个 float lane
- **Vector width (向量宽度)**: 寄存器总位数，如 128/256/512-bit
- **Element type (元素类型)**: lane 中存放的数据类型 (byte/short/int/long/float/double)

### 为什么 Java 需要显式 Vector API

C/C++ 程序员可以依赖编译器自动向量化 (auto-vectorization)，也可以用内联汇编或 intrinsic 函数直接写 SIMD 代码。Java 之前两种方式都不可用：

| 方式 | C/C++ | Java (无 Vector API) | Java (有 Vector API) |
|------|-------|---------------------|---------------------|
| **编译器自动向量化** | GCC/Clang `-O2` 自动 | C2 SuperWord 有限支持 | 不依赖，显式编写 |
| **手写 SIMD intrinsic** | `_mm256_add_ps()` | ❌ 不可能 | `va.add(vb)` |
| **内联汇编** | `asm("vaddps ...")` | ❌ 不可能 | ❌ 不需要 |
| **可移植性** | ❌ 平台特定 | N/A | ✅ 跨平台 |

**C2 SuperWord 的局限性**:
1. **不可预测 (unpredictable)** — 微小代码改动可能导致向量化失败
2. **不支持复杂模式** — mask 操作、gather/scatter、跨 lane shuffle 无法自动向量化
3. **调试困难** — 需要查看汇编才能确认是否向量化
4. **性能不稳定** — 不同 JDK 版本行为可能不同

Vector API 的核心价值：**把向量化从"编译器可能做"变为"程序员明确写"**。

---

## 3. 概述

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
| **float16** | Float16 (标量值类) | N/A (JDK 24+ 支持) |

---

## 4. 快速示例

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
    VectorSpecies<Float> species = FloatVector.SPECIES_PREFERRED;
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
### 图像处理: Alpha Blending (透明度混合)
```java
/**
 * Alpha blending: result = src * alpha + dst * (1 - alpha)
 * 常用于图像合成 (image compositing)、UI 渲染
 */
static void alphaBlend(float[] src, float[] dst, float[] result, float alpha) {
    VectorSpecies<Float> species = FloatVector.SPECIES_PREFERRED;
    float oneMinusAlpha = 1.0f - alpha;
    int i = 0;
    int bound = species.loopBound(src.length);

    for (; i < bound; i += species.length()) {
        FloatVector vs = FloatVector.fromArray(species, src, i);
        FloatVector vd = FloatVector.fromArray(species, dst, i);
        // src * alpha + dst * (1 - alpha)
        vs.mul(alpha).add(vd.mul(oneMinusAlpha)).intoArray(result, i);
    }
    // 尾部处理 (tail processing)
    for (; i < src.length; i++) {
        result[i] = src[i] * alpha + dst[i] * oneMinusAlpha;
    }
}
```

### 字符串搜索: 向量化字节匹配
```java
/**
 * 使用向量化搜索字节数组中第一个出现的目标字节
 * 类似于 C 的 memchr()，但跨平台
 */
static int vectorFind(byte[] data, byte target) {
    VectorSpecies<Byte> species = ByteVector.SPECIES_PREFERRED;
    int i = 0;
    int bound = species.loopBound(data.length);

    for (; i < bound; i += species.length()) {
        ByteVector v = ByteVector.fromArray(species, data, i);
        // 比较每个 lane 是否等于 target
        VectorMask<Byte> mask = v.compare(VectorOperators.EQ, target);
        if (mask.anyTrue()) {
            // 找到匹配: 返回第一个 true lane 的索引
            return i + mask.firstTrue();
        }
    }
    // 尾部标量搜索
    for (; i < data.length; i++) {
        if (data[i] == target) return i;
    }
    return -1;  // 未找到
}
```

---

## 5. 核心概念 (Core Concepts)
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
### Lane 操作 (Lane-wise Operations)

向量操作按作用范围分为两类:

| 类型 | 说明 | 示例 |
|------|------|------|
| **Lane-wise (逐通道)** | 独立操作每个 lane | `add()`, `mul()`, `compare()` |
| **Cross-lane (跨通道)** | lane 之间交互 | `rearrange()`, `reduceLanes()`, `slice()` |

```java
// Lane-wise: 每个 lane 独立计算
FloatVector vc = va.add(vb);      // c[i] = a[i] + b[i]

// Cross-lane: 水平归约 (horizontal reduction)
float sum = va.reduceLanes(VectorOperators.ADD);  // sum = a[0]+a[1]+...+a[n]

// Cross-lane: 重排 (rearrange / permute)
VectorShuffle<Float> rev = VectorShuffle.fromValues(species, 3, 2, 1, 0);
FloatVector reversed = va.rearrange(rev);  // 反转 lane 顺序
```

---

## 6. 支持的类型与形状

### 类型 × 形状矩阵 (Type x Shape Matrix)

每种元素类型 (element type) 与向量形状 (vector shape) 的组合决定了每个向量的 lane 数:

| 类型 (Type) | 字节宽度 | 64-bit | 128-bit | 256-bit | 512-bit | 说明 |
|-------------|---------|--------|---------|---------|---------|------|
| `byte` | 1 | 8 lanes | 16 lanes | 32 lanes | 64 lanes | 图像像素、编码 |
| `short` | 2 | 4 lanes | 8 lanes | 16 lanes | 32 lanes | 音频采样、Float16 存储 |
| `int` | 4 | 2 lanes | 4 lanes | 8 lanes | 16 lanes | 哈希、索引 |
| `long` | 8 | 1 lane | 2 lanes | 4 lanes | 8 lanes | 位运算、大整数 |
| `float` | 4 | 2 lanes | 4 lanes | 8 lanes | 16 lanes | 科学计算、图形 |
| `double` | 8 | 1 lane | 2 lanes | 4 lanes | 8 lanes | 高精度数值 |

**公式**: `lane 数 = 向量位宽 / (元素字节数 × 8)`

### SPECIES_MAX vs SPECIES_PREFERRED

```java
// SPECIES_MAX: 硬件支持的最大向量宽度
//   x86 AVX-512 → 512-bit, ARM NEON → 128-bit
FloatVector.SPECIES_MAX

// SPECIES_PREFERRED: JVM 认为最优的宽度 (可能 < MAX)
//   例: AVX-512 CPU 上可能返回 256-bit (避免降频 / frequency throttling)
FloatVector.SPECIES_PREFERRED

// 推荐: 始终使用 PREFERRED，除非有特定理由
VectorSpecies<Float> species = FloatVector.SPECIES_PREFERRED;
```

---
## 7. 支持的操作
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
## 8. 性能考量
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

## 9. 与 C2 自动向量化对比

### 何时用 Vector API vs 依赖编译器

| 场景 | 推荐方式 | 理由 |
|------|---------|------|
| 简单数组加法/乘法 | C2 SuperWord (自动) | 编译器能可靠地自动向量化简单循环 |
| 带条件分支的循环 | **Vector API** | SuperWord 无法处理 `if/else`，Vector API 用 mask |
| Gather/Scatter (间接访问) | **Vector API** | `va.fromArray(species, data, offset, indices, 0)` |
| 性能可预测性要求高 | **Vector API** | 显式代码保证向量化，不依赖编译器启发式 |
| 库代码 (跨 JDK 版本) | **Vector API** | SuperWord 行为可能在不同 JDK 版本间变化 |
| 原型 / 快速开发 | C2 SuperWord (自动) | 无需额外 API 导入和模式 |

### SuperWord 自动向量化能处理的模式

```java
// ✅ SuperWord 通常能自动向量化
for (int i = 0; i < n; i++) { c[i] = a[i] + b[i]; }          // 简单加法
for (int i = 0; i < n; i++) { c[i] = Math.sqrt(a[i]); }      // 简单数学函数

// ❌ SuperWord 通常无法自动向量化
for (int i = 0; i < n; i++) {
    if (a[i] > 0) c[i] = a[i] * b[i];                         // 条件分支
    else c[i] = 0;
}
for (int i = 0; i < n; i++) { c[i] = a[indices[i]]; }         // 间接访问 (gather)
for (int i = 0; i < n; i++) { sum += a[i] * b[i]; }           // 归约 (reduction) — 部分支持
```

### Vector API 等价写法

```java
// 条件分支 → mask 操作
for (int i = 0; i < bound; i += species.length()) {
    FloatVector va = FloatVector.fromArray(species, a, i);
    FloatVector vb = FloatVector.fromArray(species, b, i);
    VectorMask<Float> positive = va.compare(VectorOperators.GT, 0f);
    va.mul(vb, positive).intoArray(c, i);  // mask=false 的 lane 写 0
}
```

---
## 10. 与 Valhalla 的协同
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
**当前状态**: Valhalla (JEP 401) 已在 JDK 26 提供 Early Access 构建，目标 2026 下半年合并到主 JDK
---
## 11. AI/ML 浮点格式
### 格式对比
| 格式 | 位宽 | 指数位 | 尾数位 | 精度 | 硬件支持 | JDK 支持 |
|------|------|--------|--------|------|----------|----------|
| **Float32** | 32 | 8 | 23 | 高 | 所有 GPU/CPU | ✅ 完整 |
| **Float16 (半精度)** | 16 | 5 | 10 | 中 | 现代 GPU/CPU | ✅ JDK 24+ |
| **BFloat16 (脑浮点)** | 16 | 8 | 7 | 低 | Google TPU, | ❌ 计划中 |
| **Float8** | 8 | 4 | 3 | 极低 | 实验性 | ❌ 未计划 |
| **Float4** | 4 | 2 | 2 | 极低 | 无 | ❌ 未计划 |
### Float16 (已支持)
JDK 24+ 支持 Float16 (IEEE 754 半精度浮点):
```java
import jdk.incubator.vector.Float16;
// 创建 Float16
Float16 value = Float16.valueOf(3.14159);
// 转换
float f = value.floatValue();
short bits = Float16.float16ToRawShortBits(value);
```
**注意**: Float16 向量操作 (Float16Vector) 尚未实现，计划在 Project Valhalla 完成后添加。

**Float16 特点**:
- 位宽: 16-bit (1 符号位, 5 指数位, 10 尾数位)
- 范围: ±65504, 精度约 3-4 位小数
- 用途: AI 推理、图像处理、游戏图形
### BFloat16 (计划中)
**BFloat16 (Brain Float)** 由 Google 为 TPU 设计:
| 特性 | Float16 | BFloat16 | Float32 |
|------|---------|---------|---------|
| 位宽 | 16 | 16 | 32 |
| 指数位 | 5 | 8 | 8 |
| 尾数位 | 10 | 7 | 23 |
| 精度 | 中 | 低 (与 Float32 相同指数) | 高 |
| 范围 | ±65504 | 与 Float32 相同 | ±3.4e38 |
**BFloat16 优势**:
- 与 Float32 相同的指数范围，避免溢出/下溢
- 深度学习训练中常用的梯度格式
- Google TPU、Intel AVX-512 BF16 原生支持
**Java 支持**: 目前 Float16 优先，BFloat16 可能在未来版本添加
### Float8/Float4 (未来)
**目前未计划支持**，原因:
- 硬件支持有限 (仅实验性 GPU)
- 精度损失过大，适用场景有限
- 业界标准尚未稳定
**可能的路线图**:
```
Float32 (现有) ─────────────────────────────────────►
Float16 (JDK 24+) ──────────────────────────────────►
BFloat16 (未来?) ───────────────────────────────────►
Float8 (未计划) ──────────────────────────────────────►
```
---
## 12. C2 编译器内部
### 编译流程
```
Java 代码
    │
    ▼
javac 编译 ──► 字节码 (.class)
    │
    ▼
JIT 编译
┌───────────────┬───────────────┐
│ C1 (客户端)    │ C2 (服务端)    │
│ 快速编译       │ 优化编译        │
└───────────────┴───────────────┘
    │
    ▼
Intrinsic 替换
┌───────────────────────────────────────────┐
│ VectorAPI ops ──► SIMD 指令            │
└───────────────────────────────────────────┘
    │
    ▼
机器码生成
┌───────────────────────────────────────────┐
│ VEX/EVEX 编码 (AVX/AVX-512)            │
│ SVE 编码 (ARM)                          │
│ V 扩展编码 (RISC-V)                     │
└───────────────────────────────────────────┘
```
### 关键 Intrinsic
| 操作 | Intrinsic | 状态 |
|------|-----------|------|
| 向量加法 | `_VectorAdd` | ✅ |
| 向量乘法 | `_VectorMul` | ✅ |
| 向量加载 | `_VectorLoad` | ✅ |
| 向量存储 | `_VectorStore` | ✅ |
| 向量归约 | `_VectorReduce` | ✅ |
| 向量比较 | `_VectorCompare` | ✅ |
| 向量 shuffle | `_VectorShuffle` | ✅ |
| 数学函数 (sin/cos) | `_VectorMath` | ✅ (FFM) |
### SuperWord 自动向量化
C2 编译器的 SuperWord 优化会自动将标量循环转换为向量指令:
```java
// 标量代码
for (int i = 0; i < n; i++) {
    c[i] = a[i] + b[i];
}
// C2 SuperWord 自动转换为向量指令 (如果满足条件)
// vmovups ymm0, [rdi+rax*4]
// vmovups ymm1, [rdi+rdx*4]
// vaddps ymm0, ymm0, ymm1
// vmovups [rdi+rcx*4], ymm0
```
**SuperWord vs Vector API**:
| 特性 | SuperWord (自动) | Vector API (显式) |
|------|------------------|-------------------|
| 控制力 | 低 | 高 |
| 可移植性 | 依赖编译器 | 代码保证 |
| 复杂操作 | 有限 | 丰富 |
| Mask 操作 | 不支持 | 完整支持 |
| 性能 | 相似 | 相似 |
### 汇编指令映射示例
**x86-64 AVX-512**:
```asm
// Java: FloatVector va = FloatVector.fromArray(species, a, 0);
vmovups   zmm0, [rdi + rax*4]     ; 加载 16 个 float
// Java: FloatVector vb = FloatVector.fromArray(species, b, 0);
vmovups   zmm1, [rdi + rdx*4]     ; 加载 16 个 float
// Java: FloatVector vc = va.add(vb);
vaddps    zmm0, zmm0, zmm1        ; 向量加法
// Java: vc.intoArray(c, 0);
vmovups   [rdi + rcx*4], zmm0    ; 存储 16 个 float
```
**ARM SVE**:
```asm
// 加载向量 (可变长度)
ld1w     z0.d, p0/zr, [x0, x1, lsl #2]
// 广播标量
fmov     s0, #2.0
// 向量乘法
fmul     z0.s, z0.s, s0.s
// 存储结果
st1w     z0.d, p0/zr, [x0, x1]
```
---
## 13. 性能基准测试
### SAXPY 性能 (1M 元素)
| 实现 | x86-64 SSE | x86-64 AVX2 | x86-64 AVX-512 | ARM NEON | ARM SVE-256 |
|------|------------|--------------|-----------------|-----------|--------------|
| 标量循环 | ~4ms | ~4ms | ~4ms | ~4ms | ~4ms |
| Vector API | ~1ms (4x) | ~0.5ms (8x) | ~0.25ms (16x) | ~1ms (4x) | ~0.5ms (8x) |
**加速比 = 向量宽度 / 标量宽度**
### 点积性能 (1M 元素)
| 实现 | 耗时 | 加速比 |
|------|------|--------|
| 标量循环 | ~8ms | 1x |
| Vector API (AVX2) | ~1ms | 8x |
| Vector API (AVX-512) | ~0.5ms | 16x |
### 内存带宽影响
| 数据规模 | 内存带宽需求 | 向量化收益 |
|----------|--------------|--------|
| < 1KB | 低 | 小/无 (开销大于收益) |
| 1KB - 100KB | 中 | 中等 |
| 100KB - 10MB | 高 | 高 |
| > 10MB | 很高 | 騰/内存带宽瓶颈 |
---
## 14. Valhalla/Babylon 集成
### 与 Valhalla 值类型
**协同效应**:
```
┌──────────────────────────────────────────────────────────────┐
│                    值类型 + Vector API 协同                    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  传统对象数组              值类型数组 (Valhalla)           │
│  ┌─────────────────┐        ┌─────────────────┐              │
│  │ 对象头 (12 bytes)│        │ 无对象头        │              │
│  │ 引用 (8 bytes)  │        │ 内联存储         │              │
│  │ 数据 (8 bytes)  │        │ 数据 (8 bytes)   │              │
│  └─────────────────┘        └─────────────────┘              │
│                                                              │
│  内存: 28 bytes/元素        内存: 8 bytes/元素         │
│  缓存效率: 低                 缓存效率: 高             │
│  向量加载: 非连续             向量加载: 连续           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```
**当前状态**: Valhalla (JEP 401) 已在 JDK 26 提供 Early Access，Vector API 集成待定
### 与 Babylon GPU Offload
**Project Babylon** 通过 HAT (Heterogeneous Accelerator Toolkit) 将 Vector API 操作卸载到 GPU:
```
┌─────────────────────────────────────────────────────────────────┐
│                    未来: GPU Offload 架构                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │ Vector API  │     │  Babylon    │     │    GPU      │      │
│  │  (前端)     │ ──► │  (中间层)   │ ──► │  (后端)     │      │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │ CPU 执行    │     │ 代码生成    │     │ CUDA/SPIR-V │      │
│  │ AVX/SVE     │     │ PTX/SPIR-V  │     │ 执行        │      │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
**预期时间线**:
| 功能 | 版本 | 状态 |
|------|------|------|
| Vector API CPU | JDK 16+ | ✅ 可用 |
| Valhalla 值类型 (JEP 401) | JDK 26+ (Early Access) | 🔄 预览 |
| Babylon HAT GPU Offload | 实验阶段 | 🔄 开发中 |
| 完整集成 | JDK 28+ | 📅 计划中 |
---
## 15. 研究者常见问题
### Q: Vector API vs C++ SIMD intrinsics 性能差距有多大？
**答案**: 差距在 5-20% 以内，某些场景甚至持平。
| 场景 | C++ AVX-512 | Java Vector API | 差距 |
|------|-------------|-----------------|------|
| 向量加法 | 1.0x (基准) | 1.05x | +5% |
| SAXPY | 1.0x | 1.08x | +8% |
| 点积 | 1.0x | 1.10x | +10% |
| 复杂 mask 操作 | 1.0x | 1.15x | +15% |
| Gather/Scatter | 1.0x | 1.20x | +20% |
**差距原因**:
1. **JIT 编译开销**: 首次执行需要编译
2. **边界检查**: Java 数组越界检查
3. **内存布局**: Java 数组可能有额外开销
4. **Intrinsic 覆盖**: 不是所有操作都有 intrinsic
### Q: 为什么不直接使用 JNI 调用 SIMD 库？
**答案**: JNI 开销太大，且破坏 Java 安全模型。
| 方案 | JNI 调用开销 | 安全性 | 可移植性 |
|------|-------------|--------|----------|
| JNI | 100-1000 ns | ❌ 低 | ❌ 平台特定 |
| Vector API | 0 ns | ✅ 高 | ✅ 跨平台 |
### Q: Vector API vs Python NumPy 性能对比？
**答案**: Vector API 在单线程下更快，但 NumPy 在多线程和复杂操作上有优势。
| 操作 | NumPy | Java Vector API | 说明 |
|------|-------|-----------------|------|
| 大数组加法 | 1.0x | 0.9x | Java 更快 |
| 矩阵乘法 | 1.0x | 1.2x | NumPy 优化更好 |
| FFT | 1.0x | 1.5x | NumPy 使用优化的库 |
| 自定义操作 | 1.0x | 0.5x | Java 更灵活 |
### Q: Vector API 什么时候毕业？
**答案**: 预计 JDK 27-28 (2026-2027)。
**毕业条件**:
| 条件 | 状态 | 说明 |
|------|------|------|
| 跨平台支持 | ✅ 90% | x86/ARM/RISC-V 基本完整 |
| API 稳定 | 🔄 80% | 仍有小幅调整 |
| 性能达标 | ✅ 95% | 接近手写 SIMD |
| 测试覆盖 | 🔄 85% | 持续增加 |
| 文档完善 | ✅ 90% | Javadoc 完整 |
### Q: 为什么 Vector API 孵化这么慢？
**深度分析**:
1. **SVE 可变长度的复杂性**
   - 128-2048 bits 运行时确定
   - 需要特殊的代码生成策略
   - 测试组合爆炸
2. **跨平台一致性挑战**
   - x86: 固定宽度 (128/256/512)
   - ARM SVE: 可变宽度
   - RISC-V V: 可变宽度
   - 每个平台有不同的指令语义
3. **C2 编译器负担**
   - 每个操作都需要 intrinsic
   - 代码生成复杂度高
   - 需要处理边界情况
4. **测试覆盖**
   - 平台数 × 操作数 × 数据类型数
   - 组合数量巨大
   - 硬件资源有限
### Q: Vector API 对 AI/ML 有什么价值？
**答案**: 数据预处理和小规模推理。
**应用场景**:
1. **数据预处理**: 特征归一化、数据增强
2. **小批量推理**: 矩阵向量乘法 (MLP 层)
3. **Float16 支持** (JDK 24+): 节省内存带宽
### Q: C2 编译器如何处理 Vector API？
**答案**: 通过 intrinsic 和机器码生成。
**编译流程**: 见 [C2 编译器内部](#c2-编译器内部)
### Q: SVE 可变长度如何处理？
**答案**: 通过 VectorSpecies 动态适应。
```java
// 问题: SVE 向量长度运行时确定 (128-2048 bits)
// 解决: 使用 SPECIES_PREFERRED
VectorSpecies<Float> species = FloatVector.SPECIES_PREFERRED;
// 运行时确定长度
int length = species.length();  // 可能是 4, 8, 16, 32...
// 代码自动适应
for (int i = 0; i < species.loopBound(array.length); i += species.length()) {
    // 处理向量
}
```
---
## 16. 运行要求
### 编译
```bash
# JDK 16+
javac --add-modules jdk.incubator.vector VectorAdd.java
```
### 运行
```bash
# JDK 16-26 (incubator)
java --add-modules jdk.incubator.vector VectorAdd
# JDK 27+ (可能不再是 incubator)
java VectorAdd
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
## 17. 相关链接
### 本地文档
- [Project Panama / FFM API](../panama/) - 外部函数与内存 API（JDK 26 深度集成）
- [时间线](timeline.md) - 版本演进历史
- [使用指南](usage.md) - 详细使用示例
- [各版本详情](versions.md) - 每个版本究竟做了什么
- [平台支持](platform.md) - 各平台 SIMD 支持
- [贡献者](contributors.md) - 贡献者分析

### 官方资源
- [JEP 338](/jeps/language/jep-338.md)
- [JEP 414](https://openjdk.org/jeps/414)
- [JEP 417](https://openjdk.org/jeps/417)
- [JEP 426](https://openjdk.org/jeps/426)
- [JEP 438](https://openjdk.org/jeps/438)
- [JEP 448](/jeps/tools/jep-448.md)
- [JEP 460](https://openjdk.org/jeps/460)
- [JEP 469](https://openjdk.org/jeps/469)
- [JEP 489](https://openjdk.org/jeps/489)
- [JEP 508](/jeps/concurrency/jep-508.md)
- [JEP 529](/jeps/language/jep-529.md)
- [JEP 401](/jeps/language/jep-401.md)

### 相关项目
- [Project Valhalla](https://openjdk.org/projects/valhalla/) - 值类型与值对象
- [Project Babylon](https://openjdk.org/projects/babylon/) - GPU 加速与异构计算

### 源码位置
- JDK 源码: `src/jdk.incubator.vector/share/classes/jdk/incubator/vector/`
- 测试: `test/jdk/jdk/incubator/vector/`
---
## 18. 版本状态
| 版本 | JEP | 状态 |
|------|-----|------|
| JDK 16 | 338 | 🥚 First Incubator |
| JDK 17 | 414 | 🥚 Second Incubator |
| JDK 18 | 417 | 🥚 Third Incubator |
| JDK 19 | 426 | 🥚 Fourth Incubator |
| JDK 20 | 438 | 🥚 Fifth Incubator |
| JDK 21 | 448 | 🥚 Sixth Incubator |
| JDK 22 | 460 | 🥚 Seventh Incubator |
| JDK 23 | 469 | 🥚 Eighth Incubator |
| JDK 24 | 489 | 🥚 Ninth Incubator + Float16 |
| JDK 25 | 508 | 🥚 Tenth Incubator + FFM 迁移, VectorShuffle + MemorySegment, Float16 自动向量化 |
| **JDK 26** | 529 | 🥚 **Eleventh Incubator (GA 2026-03-17)** - 无实质性 API 变更 |
| JDK 27 | - | 🔄 开发中 |
> **注意**: Vector API 在 JDK 26 GA 中仍然是 Incubator 状态
> 已孵化 **5 年** (JDK 16-26)，跨越 **11 个版本**，是 OpenJDK 历史上孵化时间最长的 API 之一
### JDK 25 重要更新 (JEP 508)
| 特性 | JBS | 描述 |
|------|-----|------|
| **FFM API 集成** | [8353786](https://bugs.openjdk.org/browse/JDK-8353786) | 迁移数学库支持到 FFM API |
| **VectorShuffle + MemorySegments** | [8351993](https://bugs.openjdk.org/browse/JDK-8351993) | 与 MemorySegments 交互 |
| **Float16 自动向量化** | - | x64 CPU 上 Float16 运算自动向量化 |

> **注意**: JDK 26 (JEP 529) 相比 JDK 25 无实质性 API 或实现变更
---
## 19. 为什么孵化这么慢？
Vector API 已孵化 5 年跨越 11 个版本 (JDK 16-26)，主要原因：
### 技术挑战
| 挑战 | 描述 | 状态 |
|------|------|------|
| **SVE 可变长度** | ARM SVE 向量长度运行时确定 (128-2048 bits) | 🔄 仍在处理 |
| **跨平台一致性** | x86/ARM/RISC-V 指令差异大 | 🔄 持续改进 |
| **C2 编译器** | 需要大量 intrinsic 实现 | 🔄 进行中 |
| **Valhalla 依赖** | 值类型可提升性能 | 🔄 等待 Valhalla |
| **API 稳定性** | 需要确保 API 不再变化 | 🔄 进行中 |
### 核心瓶颈: 依赖 Project Valhalla (value types)

Vector API 孵化最慢的根本原因是等待 Valhalla 值类型:

```
当前: Vector<Float> 是普通对象 (identity object)
      ┌──────────────────────────────┐
      │ Object header (12-16 bytes) │  ← 每次创建都需要堆分配
      │ float lane[0]               │
      │ float lane[1]               │
      │ ...                         │
      └──────────────────────────────┘

未来: Vector<float> 是值类型 (value type) — 需要 Valhalla
      ┌──────────────────────────────┐
      │ float lane[0]               │  ← 无对象头，可内联在栈上
      │ float lane[1]               │     逃逸分析更简单
      │ ...                         │     GC 压力为零
      └──────────────────────────────┘
```

**为什么值类型至关重要**:
1. **消除装箱 (boxing elimination)** — 当前 C2 必须通过逃逸分析 (escape analysis) 消除 Vector 对象分配，但复杂场景下会失败
2. **泛型特化 (generic specialization)** — 未来 `Vector<int>` 直接映射硬件寄存器，无需 `Vector<Integer>`
3. **API 最终形态** — Valhalla 改变了 Vector 的类型签名，API 不能在 Valhalla 之前最终确定

**时间线**:
- Valhalla JEP 401 (Value Classes): JDK 26 Early Access
- Vector API 可能在 Valhalla 正式发布后的 1-2 个版本毕业 (预计 JDK 27-28)

### 孵化时间对比
| API | 孵化时间 | 版本数 |
|-----|----------|--------|
| **Vector API** | 5 年 (JDK 16-26) | 11 个版本 |
| Foreign Function & Memory API | 3 年 (JDK 17-22) | 5 个版本 |
| Pattern Matching | 4 年 (JDK 16-21) | 5 个版本 |
| Records | 2 年 (JDK 14-16) | 3 个版本 |
| Sealed Classes | 2 年 (JDK 15-17) | 3 个版本 |
---

## 20. 平台支持详解

### x86-64: SSE → AVX → AVX-512

| 指令集 | 引入年份 | 寄存器宽度 | 寄存器数 | 代表 CPU |
|--------|---------|-----------|---------|---------|
| SSE2 | 2001 | 128-bit (xmm) | 16 | Pentium 4+ |
| AVX | 2011 | 256-bit (ymm) | 16 | Sandy Bridge |
| AVX2 | 2013 | 256-bit (ymm) | 16 | Haswell |
| AVX-512 | 2017 | 512-bit (zmm) | 32 | Skylake-SP, Ice Lake |

**注意**: AVX-512 在某些 CPU 上会导致降频 (frequency throttling)。`SPECIES_PREFERRED` 可能返回 256-bit 以规避此问题。

### AArch64: NEON → SVE → SVE2

| 指令集 | 寄存器宽度 | 特点 | 代表硬件 |
|--------|-----------|------|---------|
| NEON (ASIMD) | 固定 128-bit | 所有 ARMv8 CPU 标配 | Apple M1/M2, Cortex-A76 |
| SVE | 可变 128-2048 bit | 硬件可选宽度，运行时确定 | Fujitsu A64FX (512-bit) |
| SVE2 | 可变 128-2048 bit | SVE 超集，增加加密/DSP 指令 | Cortex-X2+, Neoverse V2 |

**SVE 的挑战**: 不同 CPU 实现不同宽度 (Graviton3 = 256-bit, A64FX = 512-bit)，代码必须在运行时适应。这正是 `SPECIES_PREFERRED` 的设计动机。

### RISC-V: V 扩展 (RVV)

| 版本 | 状态 | 特点 |
|------|------|------|
| RVV 1.0 | 已批准 (ratified) | 可变长度向量，LMUL 分组 |

**RISC-V 特殊性**:
- 向量长度由硬件的 VLEN 参数决定 (最小 128-bit)
- 支持 LMUL (length multiplier): 多个寄存器组合为更长向量
- JDK 中的支持仍在完善，基本操作已可用

### 各平台 Vector API 支持成熟度

| 特性 | x86 AVX2 | x86 AVX-512 | ARM NEON | ARM SVE/SVE2 | RISC-V V |
|------|----------|-------------|----------|--------------|----------|
| 基础算术 | ✅ 完整 | ✅ 完整 | ✅ 完整 | ✅ 完整 | 🔄 基本 |
| Mask 操作 | ✅ 模拟 | ✅ 原生 opmask | ✅ 模拟 | ✅ 原生 predicate | 🔄 基本 |
| Gather/Scatter | ✅ | ✅ 原生 | ❌ 模拟 | ✅ 原生 | 🔄 |
| 数学函数 | ✅ SVML | ✅ SVML | 🔄 部分 | 🔄 部分 | 🔄 部分 |
| Float16 向量 | 🔄 | ✅ AVX-512 FP16 | 🔄 | 🔄 | 🔄 |

---
## 21. JEP 路线图
```
JDK 16 (2021-03) ── JEP 338 ── First Incubator
    │
JDK 17 (2021-09) ── JEP 414 ── Second Incubator
    │                               ├── ARM SVE 支持
    │                               └── SVML 集成
JDK 18 (2022-03) ── JEP 417 ── Third Incubator
    │                               ├── 旋转操作
    │                               └── 无符号转换
JDK 19 (2022-09) ── JEP 426 ── Fourth Incubator
    │                               ├── MemorySegment 支持
    │                               └── SVE predicate
JDK 20 (2023-03) ── JEP 438 ── Fifth Incubator
    │                               ├── 间接加载
    │                               └── Shuffle 增强
JDK 21 (2023-09) ── JEP 448 ── Sixth Incubator
    │
JDK 22 (2024-03) ── JEP 460 ── Seventh Incubator
    │
JDK 23 (2024-09) ── JEP 469 ── Eighth Incubator
    │
JDK 24 (2025-03) ── JEP 489 ── Ninth Incubator
    │                               ├── Float16 支持
    │                               └── selectFrom/rearrange 改进
JDK 25 (2025-09) ── JEP 508 ── Tenth Incubator
    │                               ├── FFM API 集成
    │                               ├── VectorShuffle + MemorySegment
    │                               └── Float16 自动向量化 (x64)
JDK 26 (2026-03-17) ── JEP 529 ── Eleventh Incubator (GA)
    │                               └── 无实质性变更
JDK 27 (2026-09) ── 开发中
    │
    ▼
毕业? (预计 JDK 27-28)
```
---
> **最后更新**: 2026-03-22
