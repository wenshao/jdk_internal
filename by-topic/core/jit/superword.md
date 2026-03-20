# SuperWord 向量化详解

> C2 JIT 编译器的自动 SIMD 优化
> 从标量代码到向量化指令的自动转换

[← 返回 JIT 编译](../)

---

## 一眼看懂

| 维度 | 内容 |
|------|------|
| **全称** | SuperWord Auto-Vectorization |
| **SIMD** | Single Instruction, Multiple Data |
| **原理** | 一次操作多个数据元素 |
| **性能提升** | 2-16x (取决于向量和硬件) |
| **JDK 26** | 引入成本模型，智能决策 |
| **主要作者** | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) (Oracle) |

---

## SIMD 概述

### 什么是 SIMD？

```
标量处理 (Scalar):
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│   a[0]  │ + │   a[1]  │ + │   a[2]  │ + │   a[3]  │
└─────────┘   └─────────┘   └─────────┘   └─────────┘
     │             │             │             │
     ▼             ▼             ▼             ▼
   4 次加法操作

SIMD 处理:
┌─────────────────────────────────────┐
│  [a[0] | a[1] | a[2] | a[3]]  │  向量加载
└─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│  [a[0]+b[0] | a[1]+b[1] | ...]   │  1 次向量加法
└─────────────────────────────────────┘
```

### SIMD 指令集

| 指令集 | 向量宽度 | 浮点数 | 整数 |
|--------|----------|--------|------|
| **SSE** | 128-bit | 4 × float | 2 × double |
| **AVX** | 256-bit | 8 × float | 4 × double |
| **AVX-512** | 512-bit | 16 × float | 8 × double |
| **NEON** | 128-bit | 4 × float | 2 × double |
| **SVE** | 可变 | 128-2048-bit | - |

---

## SuperWord 架构

### 编译流程

```
Java 代码
   │
   ▼
for (int i = 0; i < 1024; i++) {
    c[i] = a[i] + b[i];
}
   │
   ▼
Parse Phase (构建 Ideal Graph)
   │
   ▼
PhaseIdealLoop (识别循环)
   │
   ▼
SuperWord Phase
   │
   ├─► 1. 循环分析 (VLoopAnalyzer)
   │   └─ 识别可向量化的循环
   │
   ├─► 2. 对齐分析 (Alignment)
   │   └─ 检查内存访问对齐
   │
   ├─► 3. 依赖分析 (Memory Graph)
   │   └─ 构建内存依赖图
   │
   ├─► 4. PackSet 构建
   │   └─ 将操作打包为向量
   │
   ├─► 5. 成本模型 (Cost Model)
   │   └─ 评估向量化收益
   │
   └─► 6. 向量化应用
       └─ 生成向量指令
   │
   ▼
汇编输出
   │
   ▼
vaddps %ymm0, %ymm1, %ymm2  # AVX 加法
```

---

## 向量化条件

### 可向量化模式

| 模式 | 示例 | 可向量化 |
|------|------|----------|
| **简单算术** | `a[i] = b[i] + c[i]` | ✅ |
| **常数乘法** | `a[i] = b[i] * 2` | ✅ |
| **归约** | `sum += a[i]` | ✅ |
| **标量-向量** | `a[i] = b[i] + c` | ✅ |

### 不可向量化模式

| 模式 | 原因 |
|------|------|
| **跨迭代依赖** | `a[i] = a[i-1] + 1` |
| **条件分支** | `if (condition) a[i]++` |
| **函数调用** | `a[i] = method(b[i])` |
| **不规则访问** | `a[index[i]]++` |

### 内存依赖

```java
// 可向量化: 无依赖
for (int i = 0; i < n; i++) {
    c[i] = a[i] + b[i];
}

// 不可向量化: 有依赖
for (int i = 0; i < n; i++) {
    a[i] = a[i+1] + 1;  // 读写重叠
}
```

---

## 成本模型 (JDK-8340093)

### 为什么需要成本模型？

```
问题: 盲目向量化可能降低性能

示例: 小循环
for (int i = 0; i < 4; i++) {
    a[i] = b[i] + c[i];
}

向量化后:
- 需要 shuffle/pack/unpack
- 对齐检查开销
- 可能比标量更慢
```

### 成本因素

| 因素 | 影响 | 权重 |
|------|------|------|
| **向量宽度** | 越宽越快 | 高 |
| **循环次数** | 次数少不值得 | 高 |
| **内存访问** | 连续访问最佳 | 高 |
| **对齐状态** | 对齐更快 | 中 |
| **Shuffle 开销** | 数据重排成本 | 中 |
| **归约复杂度** | 复杂归约慢 | 低 |

### 成本计算

```cpp
// 简化的成本模型公式
scalar_cost = iterations * operations_per_iteration;
vector_cost = setup_cost + (iterations / vector_width) * vector_operations;

if (vector_cost < scalar_cost) {
    // 向量化有利
} else {
    // 保持标量
}
```

---

## SuperWord 优化类型

### 1. 算术向量化

```java
// 原始代码
for (int i = 0; i < 1024; i++) {
    c[i] = a[i] + b[i];
}

// 向量化后 (AVX2, 256-bit)
for (int i = 0; i < 1024; i += 8) {
    // 加载 8 个 int
    __m256i va = _mm256_loadu_ps(&a[i]);
    __m256i vb = _mm256_loadu_ps(&b[i]);
    // 一次加法
    __m256i vc = _mm256_add_ps(va, vb);
    // 存储 8 个 int
    _mm256_storeu_ps(&c[i], vc);
}
```

### 2. 归约向量化

```java
// 原始代码
int sum = 0;
for (int i = 0; i < 1024; i++) {
    sum += array[i];
}

// 向量化归约
int sum = 0;
for (int i = 0; i < 1024; i += 8) {
    __m256i v = _mm256_loadu_ps(&array[i]);
    // 水平求和
    sum += horizontal_sum(v);
}
```

### 3. 比较向量化

```java
// 原始代码
for (int i = 0; i < 1024; i++) {
    if (a[i] > threshold) {
        count++;
    }
}

// 向量化比较
for (int i = 0; i < 1024; i += 8) {
    __m256i va = _mm256_loadu_ps(&a[i]);
    __m256i cmp = _mm256_cmpgt_ps(va, threshold);
    count += popcount(cmp);
}
```

---

## VTransform 架构 (JDK 26+)

### 新架构

```cpp
// VTransform: SuperWord 的新架构

class VTransform {
    // 变换图
    VTransformGraph* _graph;

    // 变换节点
    GrowableArray<VTransformNode*> _nodes;

    // 成本模型
    CostModel* _cost_model;

    // 应用变换
    void apply(IdealLoopTree* loop);
};
```

### 改进点

| 改进 | 说明 |
|------|------|
| **更精确的成本模型** | 基于 profiling 的决策 |
| **更好的别名分析** | 运行时检查 |
| **支持更多操作** | Compare, Min, Max 等 |
| **更好的调试支持** | IR 规则验证 |

---

## JVM 参数

### 控制参数

```bash
# 启用/禁用向量化
-XX:+UseSuperWord                 # 启用 (默认)
-XX:-UseSuperWord                 # 禁用

# 向量宽度
-XX:MaxVectorSize=32              # 最大向量大小 (字节)
-XX:MaxVectorSize=16              # SSE (128-bit)
-XX:MaxVectorSize=32              # AVX (256-bit)
-XX:MaxVectorSize=64              # AVX-512 (512-bit)

# 调试
-XX:+TraceSuperWord               # 跟踪向量化决策
-XX:+PrintIdealGraphLevel         # 打印 IR 图
-XX:CompileCommand=print,*SuperWord*

# 成本模型控制
-XX:AutoVectorizationOverrideProfitability=true  # 强制向量化
```

### 诊断输出

```bash
# 查看向量化决策
java -XX:+TraceSuperWord MyApp

# 输出示例
SuperWord::superword_loop caught a vectorizable loop
SuperWord::construct_vloop_nodes
SuperWord::apply_packset: PackSet with 4 packs
SuperWord::do_vector_loop: SUCCESS
```

---

## 性能影响

### 微基准测试

```java
@Benchmark
public void vectorAdd() {
    for (int i = 0; i < 1024; i++) {
        c[i] = a[i] + b[i];
    }
}
```

| 硬件 | 标量 | SSE | AVX2 | AVX-512 |
|------|------|-----|------|---------|
| **Intel** | 1000 ns | 250 ns | 125 ns | 65 ns |
| **提升** | 1x | **4x** | **8x** | **16x** |

### 实际应用场景

| 场景 | 提升 | 说明 |
|------|------|------|
| **图像处理** | 8-12x | 像素操作 |
| **矩阵运算** | 6-10x | 科学计算 |
| **字符串处理** | 2-4x | 字符比较 |
| **数组复制** | 3-6x | System.arraycopy |

---

## 编程建议

### 向量化友好代码

#### 1. 简单循环

```java
// 推荐: 简单计数循环
for (int i = 0; i < n; i++) {
    c[i] = a[i] + b[i];
}

// 不推荐: 复杂索引
for (int i = 0; i < n; i += stride) {
    c[i] = a[i] + b[i];
}
```

#### 2. 连续内存

```java
// 推荐: 数组
int[] a = new int[1024];
int[] b = new int[1024];
for (int i = 0; i < 1024; i++) {
    a[i] += b[i];
}

// 不推荐: 链表
for (Node n = head; n != null; n = n.next) {
    n.value += 1;
}
```

#### 3. 避免条件

```java
// 推荐: 无条件操作
for (int i = 0; i < n; i++) {
    a[i] = b[i] + c[i];
}

// 不推荐: 循环内条件
for (int i = 0; i < n; i++) {
    if (valid[i]) {
        a[i] = b[i] + c[i];
    }
}
```

### 使用 Vector API

```java
// 显式向量化
static final VectorSpecies<Float> SPECIES = FloatVector.SPECIES_256;

void vectorAdd(float[] a, float[] b, float[] c) {
    int i = 0;
    int upper = SPECIES.loopBound(a.length);
    for (; i < upper; i += SPECIES.length()) {
        var va = FloatVector.fromArray(SPECIES, a, i);
        var vb = FloatVector.fromArray(SPECIES, b, i);
        var vc = va.add(vb);
        vc.intoArray(c, i);
    }
    // 处理余数
    for (; i < a.length; i++) {
        c[i] = a[i] + b[i];
    }
}
```

---

## 近期改进

### JDK 23-26

| Issue | 标题 | 作者 |
|-------|------|------|
| [JDK-8340093](/by-pr/8340/8340093.md) | SuperWord 成本模型 | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) |
| [JDK-8334431](/by-pr/8333/8334431.md) | 修复 Store-to-Load 转发 | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) |
| [JDK-8344085](/by-pr/8344/8344085.md) | 小循环向量化 | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) |
| [JDK-8324890](/by-pr/8324/8324890.md) | VLoop 分析器重构 | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) |

---

## 相关链接

### 本地文档

- [C2 优化阶段](c2-phases.md) - PhaseVector 详解
- [循环优化](loop-optimizations.md) - 循环优化总览
- [Vector API](/by-topic/core/vector-api/) - 显式向量化
- [Graal 高级优化](graal-advanced-optimizations.md) - 向量化对比

### 外部资源

- [Introduction to C2 - Part 4: Loop Optimizations](https://eme64.github.io/blog/2025/01/23/Intro-to-C2-Part04.html) - [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md)
- [SuperWord Status](https://eme64.github.io/blog/2025/01/01/SuperWord-Status.html)
- [Intel Intrinsics Guide](https://www.intel.com/content/www/us/en/docs/intrinsics-guide/)

---

## 贡献者

| 贡献者 | 领域 | 组织 |
|--------|------|------|
| [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | SuperWord 向量化、成本模型 | Oracle |
| [Vladimir Kozlov](/by-contributor/profiles/vladimir-kozlov.md) | C2 架构师 | Oracle |
| [Jatin Bhateja](/by-contributor/profiles/jatin-bhateja.md) | Vector API | Oracle |

---

**最后更新**: 2026-03-20
