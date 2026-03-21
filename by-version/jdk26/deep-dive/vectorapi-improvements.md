# JDK 26 VectorAPI 改进深度分析

> **JEP**: 529 (第11次孵化) | **Commit**: 8376186, 8377447, 8378758 | **代码量**: +35,619 / -17,810 行
> **作者**: Jatin Bhateja, Eric Fang 等

---

## 目录

1. [改进概述](#改进概述)
2. [API 命名变更](#api-命名变更)
3. [新增操作](#新增操作)
4. [Float16 支持](#float16-支持)
5. [源码分析](#源码分析)
6. [C2 编译器优化](#c2-编译器优化)

---

## 1. 改进概述

### 主要变更

JDK 26 对 VectorAPI 进行了重大改进：

| 变更类型 | 描述 |
|---------|------|
| **命名规范化** | 统一 Vector 类和方法的命名 |
| **UMIN/UMAX** | 无符号最小/最大操作 |
| **Float16** | 半精度浮点支持 |
| **Mask 操作** | 改进的掩码操作 |

### 影响范围

```
src/jdk.incubator.vector/share/classes/jdk/incubator/vector/
├── Vector.java                 # 核心向量接口
├── VectorOperators.java        # 操作符定义
├── VectorSpecies.java          # 向量形状
├── VectorMask.java             # 掩码
├── VectorShuffle.java          # 洗牌
├── ByteVector.java             # Byte 向量
├── ShortVector.java            # Short 向量
├── IntVector.java              # Int 向量
├── LongVector.java             # Long 向量
├── FloatVector.java            # Float 向量
├── DoubleVector.java           # Double 向量
├── Float16.java                # Float16 支持
└── Float16Consts.java          # Float16 常量
```

---

## 2. API 命名变更

### 重命名规则

JDK 26 统一了 VectorAPI 的命名约定：

```java
// 之前 (不一致的命名)
FloatVector.Float256Vector
IntVector.Int128Vector
DoubleVector.Double512Vector

// 之后 (统一的命名)
FloatVector256
IntVector128
DoubleVector512
```

### 类层次结构

```java
// 核心接口
public interface Vector<E> {

    // 向量形状
    VectorShape shape();
    int length();           // 车道数
    int bitSize();          // 总位数
    Class<E> elementType();

    // 车道操作
    Vector<E> add(Vector<E> v);
    Vector<E> mul(Vector<E> v);
    Vector<E> lanewise(VectorOperators.Binary op, Vector<E> v);

    // 归约
    E reduceLanes(VectorOperators.Associative op);
}

// 类型特定向量
public abstract class FloatVector extends Vector<Float> {
    public abstract FloatVector add(FloatVector v);
    public abstract FloatVector mul(FloatVector v);
    public abstract FloatVector sqrt();
}

// 形状特定向量
public abstract class FloatVector256 extends FloatVector {
    // 256 位 Float 向量 (8 个 float)
}
```

---

## 3. 新增操作

### UMIN/UMAX - 无符号最小/最大

```java
// VectorOperators.java

// 无符号最小值
public static final Binary UMIN =
    new Binary("UMIN", "Math.min(intVal(a), intVal(b))", int.class, long.class);

// 无符号最大值
public static final Binary UMAX =
    new Binary("UMAX", "Math.max(intVal(a), intVal(b))", int.class, long.class);

// 使用示例
IntVector a = IntVector.fromArray(IntVector.SPECIES_256, array1, 0);
IntVector b = IntVector.fromArray(IntVector.SPECIES_256, array2, 0);

// 无符号比较
IntVector min = a.lanewise(VectorOperators.UMIN, b);
IntVector max = a.lanewise(VectorOperators.UMAX, b);
```

### 其他新增操作

```java
// SUADD - 饱和加法
public static final Binary SUADD =
    new Binary("SUADD", "saturatingAdd(a, b)", byte.class, short.class);

// SUSUB - 饱和减法
public static final Binary SUSUB =
    new Binary("SUSUB", "saturatingSub(a, b)", byte.class, short.class);

// 绝对差值
public static final Binary ABSD =
    new Binary("ABSD", "Math.abs(a - b)", int.class, long.class);
```

---

## 4. Float16 支持

### Float16 类

```java
// Float16.java - 半精度浮点

/**
 * 半精度浮点数 (16 位)
 * - 符号位: 1 位
 * - 指数: 5 位
 * - 尾数: 10 位
 */
public final class Float16 {
    private final short value;

    // 最小/最大值
    public static final float MIN_VALUE = 0x1.0p-14f;
    public static final float MAX_VALUE = 65504.0f;

    // NaN
    public static final float NaN = Float.intBitsToFloat(0x7fc00000);

    // 转换方法
    public static float toFloat(short f16);
    public static short toFloat16(float f32);

    // 向量支持
    public static final Float16Vector.SPECIES_256 SPECIES_256;
}
```

### Float16 向量

```java
// Float16Vector.java (新增)

public abstract class Float16Vector extends Vector<Float> {
    // 半精度浮点向量
    // 256 位 = 16 个 Float16

    public abstract Float16Vector add(Float16Vector v);
    public abstract Float16Vector mul(Float16Vector v);

    // 转换到 Float32
    public abstract FloatVector convertToFloat();
}
```

---

## 5. 源码分析

### Vector 核心接口

```java
// Vector.java

public interface Vector<E> {
    // 车道类型
    LaneType elementType();

    // 向量形状
    VectorShape shape();

    // 车道数
    int length();

    // 总位数
    int bitSize();

    // 向量种类
    VectorSpecies<E> species();

    // 基本操作
    Vector<E> add(Vector<E> v);
    Vector<E> sub(Vector<E> v);
    Vector<E> mul(Vector<E> v);
    Vector<E> div(Vector<E> v);

    // 通用车道操作
    Vector<E> lanewise(VectorOperators.Unary op);
    Vector<E> lanewise(VectorOperators.Binary op, Vector<E> v);
    Vector<E> lanewise(VectorOperators.Ternary op, Vector<E> v1, Vector<E> v2);

    // 掩码操作
    Vector<E> blend(Vector<E> v, VectorMask<E> m);

    // 归约
    E reduceLanes(VectorOperators.Associative op);

    // 比较生成掩码
    VectorMask<E> compare(VectorOperators.Comparison op, Vector<E> v);
}
```

### VectorOperators 操作符

```java
// VectorOperators.java

public final class VectorOperators {
    // 一元操作
    public static final Unary ABS = ...;
    public static final Unary NEG = ...;
    public static final Unary SQRT = ...;
    public static final Unary SIN = ...;
    public static final Unary COS = ...;

    // 二元操作
    public static final Binary ADD = ...;
    public static final Binary SUB = ...;
    public static final Binary MUL = ...;
    public static final Binary DIV = ...;
    public static final Binary MIN = ...;
    public static final Binary MAX = ...;
    public static final Binary UMIN = ...;  // 新增：无符号最小
    public static final Binary UMAX = ...;  // 新增：无符号最大

    // 比较操作
    public static final Comparison EQ = ...;
    public static final Comparison NE = ...;
    public static final Comparison LT = ...;
    public static final Comparison LE = ...;
    public static final Comparison GT = ...;
    public static final Comparison GE = ...;

    // 转换操作
    public static final Conversion REINTERPRET = ...;
}
```

### VectorSpecies 向量种类

```java
// VectorSpecies.java

public interface VectorSpecies<E> {
    // 元素类型
    Class<E> elementType();

    // 向量形状
    VectorShape shape();

    // 车道数
    int length();

    // 推荐的物种实例
    static <E> VectorSpecies<E> ofPreferred(Class<E> elementType);

    // 创建向量
    Vector<E> fromArray(byte[] a, int offset);
    Vector<E> fromByteArray(byte[] a, int offset);
    Vector<E> broadcast(long e);

    // 零向量
    Vector<E> zero();
}
```

---

## 6. C2 编译器优化

### SuperWord 优化

```cpp
// src/hotspot/share/opto/superword.cpp

// JDK 26 改进的 SuperWord 优化
class SuperWord {
  // 向量化候选分析
  bool is_vectorizable(CountedLoopNode* cl);

  // Pack 操作
  PackSet* filter_packs();

  // 内存别名分析
  AliasChecker* alias_checker();

  // SIMD 指令生成
  void generate_vector_instruction(Node* n);
};
```

### SuperWord 别名分析

```cpp
// JDK 26 新增：运行时别名检查

// 之前：保守的别名检查
// 如果可能存在别名，不向量化

// 之后：运行时检查
// 生成运行时别名检查代码
// 如果无别名，使用向量化路径
// 如果有别名，回退到标量路径

void SuperWord::runtime_alias_check() {
  // 生成检查代码
  // if (arrays are disjoint) {
  //   vectorized_path
  // } else {
  //   scalar_path
  // }
}
```

### CPU 特性检测

```cpp
// src/hotspot/cpu/x86/vm_version_x86.hpp

class VM_Version_Ext {
  // SIMD 特性检测
  bool supports_avx();
  bool supports_avx2();
  bool supports_avx512();
  bool supports_sse();
  bool supports_neon();

  // VectorAPI 特性
  bool supports_vector_api();
};
```

---

## 7. 使用示例

### 基本向量操作

```java
// 创建向量
final static VectorSpecies<Float> SPECIES = FloatVector.SPECIES_256;

float[] a = new float[8];
float[] b = new float[8];
// ... 填充数组

FloatVector va = FloatVector.fromArray(SPECIES, a, 0);
FloatVector vb = FloatVector.fromArray(SPECIES, b, 0);

// 向量加法
FloatVector vc = va.add(vb);

// 存储结果
float[] c = new float[8];
vc.intoArray(c, 0);
```

### UMIN/UMAX 示例

```java
// 无符号比较
IntVector a = IntVector.fromArray(IntVector.SPECIES_256, array1, 0);
IntVector b = IntVector.fromArray(IntVector.SPECIES_256, array2, 0);

// 无符号最小值
IntVector min = a.lanewise(VectorOperators.UMIN, b);

// 无符号最大值
IntVector max = a.lanewise(VectorOperators.UMAX, b);
```

### 掩码操作

```java
// 创建掩码
VectorMask<Float> mask = va.compare(VectorOperators.GT, 0.0f);

// 条件选择
FloatVector result = va.mul(vb, mask);  // 只在 mask 为 true 的车道执行乘法

// 混合
FloatVector blended = va.blend(vb, mask);
```

---

## 8. 性能考虑

### SIMD 加速

| 操作 | 标量 | SIMD (AVX2) | 加速比 |
|------|------|------------|--------|
| 加法 | 8 次 | 1 次 | 8x |
| 乘法 | 8 次 | 1 次 | 8x |
| 平方根 | 8 次 | 1 次 | 8x |

### 内存带宽

```
标量加载: 8 次缓存访问
向量加载: 1 次缓存访问
```

---

## 9. 总结

JDK 26 的 VectorAPI 改进：

1. **命名规范**：统一的 API 命名
2. **新操作**：UMIN/UMAX 无符号操作
3. **Float16**：半精度浮点支持
4. **编译器优化**：改进的 SuperWord 向量化

---

## 10. 相关链接

- [VectorAPI 文档](https://openjdk.org/jeps/338)
- [Commit: 8376186](https://github.com/openjdk/jdk/commit/8376186)
- [Commit: 8377447](https://github.com/openjdk/jdk/commit/8377447)
