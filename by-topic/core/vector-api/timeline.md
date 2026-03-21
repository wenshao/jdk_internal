# Vector API 时间线

> 跨版本演进追踪 (JDK 16 - JDK 26+)

[← 返回 Vector API](./)

---

## 演进概览

```
JDK 16 (2021-03) ── JEP 338 ── First Incubator
    │
JDK 17 (2021-09) ── JEP 414 ── Second Incubator
    │                               ├── ARM SVE 支持
    │                               └── 更多向量操作
JDK 18 (2022-03) ── JEP 417 ── Third Incubator
    │                               ├── 增强 ARM 支持
    │                               └── 新操作符
JDK 19 (2022-09) ── JEP 426 ── Fourth Incubator
    │                               ├── 重构 API
    │                               └── 性能优化
JDK 20 (2023-03) ── JEP 438 ── Fifth Incubator
    │                               ├── 增强 VectorMask
    │                               └── 更多测试
JDK 21 (2023-09) ── JEP 448 ── Sixth Incubator
    │                               ├── Float16 支持
    │                               └── 继续优化
JDK 22 (2024-03) ──────────── 继续孵化
    │
JDK 23 (2024-09) ──────────── 继续孵化
    │
JDK 24 (2025-03) ──────────── 继续孵化
    │
JDK 26 (2026-03-17) ──────── GA 发布，仍为 Incubator
    │
JDK 27 (2026-09) ──────────── 开发中
```

> **重要**: Vector API 在 JDK 26 GA 中仍然是 Incubator 状态，已孵化 **5 年跨越 11 个版本**

---

## 版本详情

### JDK 16: JEP 338 (First Incubator)

**发布**: 2021-03-16

**初始功能**:
- 基础向量类型: `ByteVector`, `ShortVector`, `IntVector`, `LongVector`, `FloatVector`, `DoubleVector`
- `VectorSpecies` 定义向量形状
- `VectorMask` 条件操作
- `VectorShuffle` 元素重排
- 基本算术运算

**支持平台**:
- x86-64: SSE, AVX, AVX2
- AArch64: NEON

**示例**:
```java
// JDK 16 初始 API
VectorSpecies<Integer> species = IntVector.SPECIES_256;
IntVector a = IntVector.fromArray(species, array, 0);
IntVector b = a.add(IntVector.fromArray(species, array, 8));
```

---

### JDK 17: JEP 414 (Second Incubator)

**发布**: 2021-09-14

**新增功能**:
- ARM SVE (Scalable Vector Extension) 初始支持
- 新增向量操作符
- 改进 `VectorMask` API
- 性能优化

**API 变更**:
```java
// 新增操作
Vector.broadcast(species, value);  // 广播值到所有通道
VectorMask.fromLong(species, bits);  // 从 long 创建 mask
```

---

### JDK 18: JEP 417 (Third Incubator)

**发布**: 2022-03-22

**新增功能**:
- 增强 ARM SVE 支持
- 更多跨车道操作
- 新增 `slice()` 和 `unslice()` 方法
- 改进向量存储/加载

**API 变更**:
```java
// 跨车道操作
FloatVector rotated = va.rotateLanesToLeft(2);
FloatVector reversed = va.rearrange(va.species().laneReversingShuffle());

// slice/unslice (用于滑动窗口)
FloatVector sliced = va.slice(1, vb);  // 跨向量切片
```

---

### JDK 19: JEP 426 (Fourth Incubator)

**发布**: 2022-09-20

**重大变更**:
- API 重构: 统一 `Vector<E>` 超类
- 增强向量转换操作
- 改进内存访问
- 更好的 C2 编译器集成

**API 变更**:
```java
// 向量类型转换
IntVector iv = ...;
FloatVector fv = iv.castShape(FloatVector.SPECIES_256, 0);

// 改进的内存加载
FloatVector.fromMemorySegment(species, memorySegment, offset, ByteOrder.NATIVE_ORDER);
```

---

### JDK 20: JEP 438 (Fifth Incubator)

**发布**: 2023-03-21

**新增功能**:
- 增强 `VectorMask` 操作
- 更多 `VectorShuffle` 功能
- ARM SVE2 指令支持
- 性能优化

**API 变更**:
```java
// Mask 操作增强
VectorMask<Float> notMask = mask.not();  // 取反
VectorMask<Float> andMask = mask1.and(mask2);  // 与
VectorMask<Float> orMask = mask1.or(mask2);    // 或

// 从索引数组加载
IntVector.fromArray(species, array, 0, indexes, 0);  // 间接加载
```

---

### JDK 21: JEP 448 (Sixth Incubator)

**发布**: 2023-09-19

**新增功能**:
- `Float16` (半精度浮点) 支持
- 新增 `CPUFeatures` API
- 更多数学函数
- 改进 RISC-V V 扩展支持

**API 变更**:
```java
// Float16 支持
Float16 value = Float16.valueOf(3.14159f);
float f = value.floatValue();

// CPU 特性检测
CPUFeatures features = CPUFeatures.getCPUFeatures();
boolean hasAVX512 = features.hasFeature("avx512f");
```

---

### JDK 22 (2024-03)

**继续孵化**

**改进**:
- 更多向量化模式
- C2 编译器优化增强
- 错误修复

---

### JDK 23 (2024-09)

**继续孵化**

**改进**:
- 继续增强 ARM SVE 支持
- 改进向量寄存器分配
- 性能调优

---

### JDK 24 (2025-03)

**继续孵化**

**预期改进**:
- 更完整的跨平台支持
- 与 Panama FFI 更好集成
- 性能优化

---

### JDK 26 (2026-03-17) - GA 已发布

**继续孵化**

**重要更新**:
- **FFM API 集成**: 迁移数学库支持到 FFM API ([JDK-8353786](https://bugs.openjdk.org/browse/JDK-8353786))
- **VectorShuffle + MemorySegments**: 支持与 MemorySegments 交互 ([JDK-8351993](https://bugs.openjdk.org/browse/JDK-8351993))
- **Float16 增强**: 多项 Float16 重构和优化
- **UMIN/UMAX 归约**: 无符号最小/最大归约支持 ([JDK-8362279](https://bugs.openjdk.org/browse/JDK-8362279))
- **VectorShape 公开**: `largestShapeFor()` 方法公开访问 ([JDK-8356634](https://bugs.openjdk.org/browse/JDK-8356634))
- **子字 gather 加载**: 重构子字 gather 加载 API ([JDK-8355563](https://bugs.openjdk.org/browse/JDK-8355563))

---

### JDK 27 (2026-09) - 开发中

**预期改进**:
- 继续 FFM API 深度集成
- 更多平台支持优化
- 性能增强

---

## 各版本 API 对比

### 创建向量

```java
// JDK 16+
IntVector v1 = IntVector.fromArray(species, array, 0);

// JDK 19+ 增加
IntVector v2 = IntVector.fromMemorySegment(species, segment, 0, order);

// JDK 20+ 增加间接加载
IntVector v3 = IntVector.fromArray(species, array, 0, indexes, 0);
```

### Mask 操作

```java
// JDK 16+
VectorMask<Integer> m1 = VectorMask.fromArray(species, bools, 0);

// JDK 17+ 增加
VectorMask<Integer> m2 = VectorMask.fromLong(species, 0xFF);

// JDK 20+ 增加
VectorMask<Integer> m3 = m1.and(m2);
VectorMask<Integer> m4 = m1.or(m2);
VectorMask<Integer> m5 = m1.not();
```

### 数学函数

```java
// JDK 16+ 基础运算
IntVector sum = a.add(b);
IntVector prod = a.mul(b);

// JDK 21+ 更多数学函数
FloatVector s = a.lanewise(VectorOperators.SIN);
FloatVector c = a.lanewise(VectorOperators.COS);
FloatVector sqrt = a.lanewise(VectorOperators.SQRT);
```

---

## 平台支持演进

| 平台 | JDK 16 | JDK 17 | JDK 18 | JDK 19 | JDK 20 | JDK 21 | JDK 22-26 |
|------|--------|--------|--------|--------|--------|--------|-----------|
| x86-64 SSE | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| x86-64 AVX | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| x86-64 AVX2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| x86-64 AVX-512 | 🔄 | 🔄 | ✅ | ✅ | ✅ | ✅ | ✅ |
| AArch64 NEON | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| ARM SVE | ❌ | 🔄 | 🔄 | ✅ | ✅ | ✅ | ✅ |
| ARM SVE2 | ❌ | ❌ | ❌ | ❌ | 🔄 | ✅ | ✅ |
| RISC-V V | ❌ | ❌ | ❌ | 🔄 | 🔄 | ✅ | ✅ |
| LoongArch LSX | ❌ | ❌ | ❌ | ❌ | ❌ | 🔄 | ✅ |

---

## 性能演进

### 基准测试: 向量加法 (1M 元素)

| 版本 | 相对性能 |
|------|----------|
| JDK 16 | 1.0x (基准) |
| JDK 17 | 1.1x |
| JDK 18 | 1.2x |
| JDK 19 | 1.4x |
| JDK 20 | 1.5x |
| JDK 21 | 1.6x |

*测试环境: Intel Xeon (AVX-512), FloatVector.SPECIES_512*

---

## 未来方向

### 短期 (JDK 24-25)

1. **API 稳定化** - 减少破坏性变更
2. **完整 SVE 支持** - 可变向量长度
3. **GPU 卸载** - 与 Project Babylon 集成

### 中期 (JDK 26-27)

1. **从 Incubator 毕业** - 成为标准 API
2. **与 Valhalla 集成** - 值类型向量化
3. **自动向量化改进** - 更多自动向量化场景

### 长期

1. **分布式向量计算** - 多节点协同
2. **AI/ML 集成** - 与矩阵 API 协同
3. **新硬件支持** - Intel APX, ARM v9.2

---

## 相关 JEP

| JEP | 版本 | 标题 |
|-----|------|------|
| 338 | 16 | Vector API (Incubator) |
| 414 | 17 | Vector API (Second Incubator) |
| 417 | 18 | Vector API (Third Incubator) |
| 426 | 19 | Vector API (Fourth Incubator) |
| 438 | 20 | Vector API (Fifth Incubator) |
| 448 | 21 | Vector API (Sixth Incubator) |
| - | 22 | Vector API (Seventh Incubator) |
| - | 23 | Vector API (Eighth Incubator) |
| - | 24 | Vector API (Ninth Incubator) |
| 508 | 25 | Vector API (Tenth Incubator) |
| 529 | 26 | Vector API (Eleventh Incubator) |

---

> **最后更新**: 2026-03-21
