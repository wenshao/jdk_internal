# GraalVM vs C2 高级优化特性对比

> 类似 MergeStore 的内存优化及其他高级特性深度对比

[← 返回 JIT 编译](../)

---

## 结论先行

| 优化特性 | C2 | Graal | 胜者 |
|----------|----|-------|------|
| **MergeStore/MergeLoad** | ✅ JDK 21+ 显著改进 | ✅ 更激进 | **相当** |
| **部分转逃分析** | ❌ 无 | ✅ 有 | **Graal** |
| **条件消除** | ✅ CCP | ✅ 更激进 | **Graal** |
| **死存储消除** | ✅ 基础 DSE | ✅ 更完善 | **Graal** |
| **数组消除** | ✅ 标量替换 | ✅ 数组内联 | **Graal** |
| **循环展开** | ✅ 保守 | ✅ 激进 | **Graal** |

> **重要说明**: C2 在 JDK 21-26 期间有显著改进 (尤其是 MergeStore 和 SuperWord)，两者差距在缩小。

---

## 一眼看懂

### C2 vs Graal 优化能力对比

```
C2 能做的，Graal 都能做
Graal 能做的，C2 不一定能做

根本原因:
├── Graal IR 更灵活 (Sea of Nodes)
├── Graal 优化更激进 (不惜编译时间)
├── Graal 分析更深入 (部分转逃)
└── Graal 可扩展性强 (Java 实现)
```

### 关键差异

| 特性 | C2 | Graal |
|------|----|-------|
| **MergeStore** | 4-8字节 (JDK 21+) | 16+字节 |
| **部分转逃** | 无 | 有 |
| **迭代 PEA** | 无 | 可选 (Truffle) |
| **数组内联** | 标量替换 | 寄存器嵌入 |

---

## MergeStore/MergeLoad 对比

### C2 MergeStore (JDK 21+)

> **完整文档**: [MergeStore 优化](mergestore.md)

```java
// C2 JDK 21+ 可以合并连续存储
buf[0] = 'a';
buf[1] = 'b';
buf[2] = 'c';
buf[3] = 'd';

// C2 优化后:
Unsafe.putInt(buf, 0, 0x64636261);  // 4字节合并

// JDK 21+ 新增 (JDK-8318446):
// - 支持 4-8 字节合并
// - StringBuilder append 优化
// - Big-Endian/Little-Endian 支持
```

**C2 MergeStore 限制**:
- 主要针对 4-8 字节合并
- 需要连续、相同类型的存储
- 边界必须可验证

### Graal MergeStore

```java
// Graal 可以合并更大的连续存储
buf[0] = 'a';
// ... 16次写入
buf[15] = 'p';

// Graal 优化为:
Unsafe.putLong(buf, 0, 0x...);   // 前8字节
Unsafe.putLong(buf, 8, 0x...);   // 后8字节

// Graal Native 可能优化为 SIMD:
movdqu xmm0, [constant]
movdqu [buf], xmm0
```

### 性能对比

| 场景 | C2 (JDK 21+) | Graal JIT | 差异 |
|------|-------------|-----------|------|
| **4字节合并** | ✅ | ✅ | 相当 |
| **8字节合并** | ✅ | ✅ | 相当 |
| **16字节合并** | ⚠️ | ✅ | Graal 略优 |
| **32字节合并** | ❌ | ✅ (SIMD) | Graal 胜 |

**结论**: 对于常见场景 (4-8字节)，两者相当。Graal 在更大合并时占优。

### C2 MergeStore 贡献者

| 贡献者 | 贡献 |
|--------|------|
| [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | JDK-8318446 初始实现 |
| [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | StringBuilder 优化 |
| [Vladimir Kozlov](/by-contributor/profiles/vladimir-kozlov.md) | 技术指导 |

---

## 部分转逃分析 (Partial Escape Analysis)

### C2 逃逸分析

> **完整文档**: [逃逸分析详解](escape-analysis.md)

```java
// C2: 全或无
public int calculate(int x) {
    Point p = new Point(x, 0);
    if (x > 100) {
        return p.x;  // p 不逃逸
    } else {
        return consume(p);  // p 逃逸
    }
}

// C2 分析:
// p 有逃逸路径 → 完全不优化
// 结果: 始终创建 Point 对象
```

**C2 逃逸分析能力**:
- ✅ 标量替换 (Scalar Replacement)
- ✅ 栈上分配
- ✅ 锁消除
- ❌ 无部分转逃分析

### Graal 部分转逃

> **完整文档**: [Graal 独有特性](graal-unique-features.md#部分转逃分析)

```java
// Graal: 部分优化
public int calculate(int x) {
    Point p = new Point(x, 0);
    if (x > 100) {
        return p.x;  // p 不逃逸
    } else {
        return consume(p);  // p 逃逸
    }
}

// Graal 分析:
// x > 100 路径: p 被标量替换
// x <= 100 路径: p 保持对象分配

// 优化后:
if (x > 100) {
    int p$x = x;      // 标量替换
    int p$y = 0;
    return p$x;
} else {
    Point p = new Point(x, 0);  // 创建对象
    return consume(p);
}
```

### 性能影响

| 场景 | C2 | Graal | 提升 |
|------|----|-------|------|
| **条件逃逸** | 不优化 | 部分优化 | +10-30% |
| **循环逃逸** | 不优化 | 部分优化 | +20-50% |
| **多路径逃逸** | 不优化 | 部分优化 | +15-40% |

### 相关研究

- [Partial Escape Analysis in Graal](https://chriswthomaspresentations.s3.amazonaws.com/PartialEscapeAnalysis.pdf) - [Lukas Stadler](/by-contributor/profiles/lukas-stadler.md)
- [Inlining-Benefit Prediction with Interprocedural Partial Escape Analysis](https://dl.acm.org/doi/10.1145/3563838.3567677) - 2023 论文

---

## 死存储消除 (Dead Store Elimination)

### C2 DSE

```java
// C2 基础 DSE
int x = 1;
x = 2;  // 死存储
x = 3;  // 死存储
return x;

// C2 优化后:
return 3;
```

**C2 DSE 能力**:
- ✅ 局部变量死存储消除
- ✅ 基本块内 DSE
- ⚠️ 跨基本块 DSE (有限)
- ⚠️ 数组 DSE (有限)

### Graal 高级 DSE

```java
// Graal 更激进的 DSE
// 1. 跨基本块 DSE
void method() {
    int x = 1;
    if (condition) {
        x = 2;
    }
    x = 3;  // 无论 condition，x=3 都是最后的值
    use(x);
}

// Graal 优化: 消除所有前面的 x 赋值

// 2. 数组死存储消除
char[] buf = new char[10];
buf[0] = 'a';  // 死存储
buf[0] = 'b';  // 覆盖
buf[0] = 'c';  // 最终值
// Graal: 只保留最后的写入
```

### 性能对比

| 场景 | C2 | Graal |
|------|----|-------|
| **局部 DSE** | ✅ | ✅ |
| **跨基本块 DSE** | ⚠️ 有限 | ✅ 完整 |
| **数组 DSE** | ⚠️ 有限 | ✅ 更完善 |
| **对象字段 DSE** | ⚠️ 有限 | ✅ 更完善 |

---

## 数组消除优化

### C2 标量替换

```java
// C2 可以标量替换小数组
public int sum() {
    int[] arr = new int[3];
    arr[0] = 1;
    arr[1] = 2;
    arr[2] = 3;
    return arr[0] + arr[1] + arr[2];
}

// C2 优化后 (如果数组不逃逸):
int arr$0 = 1;
int arr$1 = 2;
int arr$2 = 3;
return arr$0 + arr$1 + arr$2;
```

**C2 数组优化**:
- ✅ 小数组标量替换 (通常 ≤ 4 元素)
- ✅ 逃逸分析后消除分配
- ❌ 数组内联到寄存器

### Graal 数组内联

```java
// Graal 可以内联小数组到寄存器
public int process() {
    byte[] data = new byte[16];
    // ... 使用 data

    // Graal 优化为:
    // long data0, data1;  // 两个寄存器存储16字节
    // 所有操作直接在寄存器上进行
}

// Graal Native 可能优化为 SIMD:
// __m128i data;  // SSE/AVX 寄存器
```

### 对比

| 特性 | C2 | Graal |
|------|----|-------|
| **小数组标量替换** | ✅ | ✅ |
| **数组内联到寄存器** | ❌ | ✅ |
| **SIMD 向量化存储** | ⚠️ SuperWord | ✅ 更激进 |

---

## 条件消除 (Conditional Elimination)

### C2 条件消除

> **相关**: [C2 PhaseCCP](c2-phases.md#phase-6-phaseccp)

```java
// C2 CCP (Conditional Constant Propagation)
final int X = 5;
if (x > 10) {  // C2 可以消除
    doSomething();
}

// C2 优化后:
// 整个 if 块被移除
```

**C2 条件消除**:
- ✅ 常量条件消除 (CCP)
- ✅ 空检查消除
- ✅ 范围检查消除 (部分)
- ⚠️ 类型检查消除 (有限)

### Graal 条件消除

```java
// Graal 更激进的消除
// 1. 范围消除
void method(int x) {
    if (x >= 0 && x < 10) {
        if (x >= 0 && x < 5) {  // Graal 可以简化
            // ...
        }
    }
}

// 2. 类型检查消除
Object obj = getList();  // 返回 ArrayList
if (obj instanceof ArrayList) {
    ArrayList list = (ArrayList) obj;
    // Graal 可以消除后续的类型检查
    list.add(item);
}
```

### 对比

| 特性 | C2 | Graal |
|------|----|-------|
| **常量条件消除** | ✅ | ✅ |
| **范围条件消除** | ⚠️ 有限 | ✅ 更完整 |
| **类型检查消除** | ⚠️ 有限 | ✅ 更激进 |
| **空检查消除** | ✅ | ✅ 更完善 |

---

## 循环优化对比

### C2 循环优化

> **完整文档**: [循环优化详解](loop-optimizations.md)

```java
// C2 PhaseIdealLoop
for (int i = 0; i < 1000; i++) {
    sum += array[i];
}

// C2 优化:
// 1. 循环展开 (4x 或 8x)
// 2. SuperWord 向量化 (如果可能)
// 3. 强度削弱
```

**C2 循环优化**:
- ✅ 循环展开 (2-8x)
- ✅ 循环剥离
- ✅ 循环外提
- ✅ SuperWord 向量化 (JDK 26+ 改进)

### Graal 循环优化

```java
// Graal 更激进的优化
for (int i = 0; i < 16; i++) {
    result[i] = input[i] * 2;
}

// Graal 可能完全展开:
result[0] = input[0] * 2;
result[1] = input[1] * 2;
// ... 16次

// 然后进一步优化为 SIMD:
__m256i in = _mm256_loadu_ps(input);
__m256i out = _mm256_mul_ps(in, factor);
_mm256_storeu_ps(result, out);
```

### 对比

| 特性 | C2 | Graal |
|------|----|-------|
| **循环展开** | ✅ 保守 (2-8x) | ✅ 激进 (全展开) |
| **循环剥离** | ✅ | ✅ |
| **循环外提** | ✅ | ✅ |
| **循环不变代码外提** | ✅ | ✅ 更激进 |
| **完全展开小循环** | ⚠️ 很少 | ✅ 经常 |

### C2 SuperWord 改进 (JDK 26)

| PR | 贡献者 | 说明 |
|----|--------|------|
| [JDK-8340093](/by-pr/8340/8340093.md) | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | 成本模型 |
| [JDK-8344085](/by-pr/8344/8344085.md) | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | 小循环优化 |
| [JDK-8371146](/by-pr/8371/8371146.md) | [Hamlin Li](/by-contributor/profiles/hamlin-li.md) | Bug 修复 |

---

## GraalVM 独有优化

### 1. 迭代部分转逃分析

```bash
# 启用迭代 PEA
-H:+TruffleIterativePartialEscape

# 适用于 Truffle 语言实现
# 多轮分析提升优化效果
```

**效果**: 在多语言场景下额外提升 10-30%

**相关贡献者**:
- [Lukas Stadler](/by-contributor/profiles/lukas-stadler.md) - PEA 研究和实现
- [Thomas Wuerthinger](/by-contributor/profiles/thomas-wuerthinger.md) - Truffle 架构师

### 2. 数组边界检查消除

```java
// Graal 可以消除更多边界检查
for (int i = 0; i < array.length; i++) {
    // Graal 可以证明 i 始终在范围内
    // 消除所有边界检查
    array[i] *= 2;
}
```

### 3. 虚拟化优化

```java
// Graal 可以虚拟化对象
StringBuilder sb = new StringBuilder();
sb.append("a");
sb.append("b");
return sb.toString();

// Graal 可能完全消除 StringBuilder
// 直接返回 "ab"
```

**相关贡献者**:
- [Doug Simon](/by-contributor/profiles/doug-simon.md) - Graal 编译器架构

### 4. 帧状态分离

> **完整文档**: [Graal 独有特性](graal-unique-features.md#帧状态分离)

允许在优化过程中创建多个"帧状态"，实现更精确的优化。

---

## Native Image 特有优化

### AOT 优化优势

```
JIT (C2/Graal):
├── 运行时编译
├── 基于 profiling
└── 稳态性能好

Native Image (AOT):
├── 编译时优化
├── 全局分析
├── 激进优化
└── 启动快 + 稳态好
```

### Native Image 独有优化

| 优化 | 说明 |
|------|------|
| **全局分析** | 跨类边界优化 |
| **静态内联** | 所有调用都可内联 |
| **堆快照** | 编译时初始化堆 |
| **去除未用代码** | 更小的二进制 |

---

## 性能实测对比

### Renaissance Benchmark

> **详细数据**: [Graal vs C2 性能对比](graal-vs-c2-performance.md)

| Benchmark | C2 | Graal JIT | Graal Native |
|-----------|----|-----------|--------------|
| apache-spark | 100 | 95 | 85 |
| finagle-chirper | 100 | 98 | **110** |
| future-genetic | 100 | 105 | **120** |
| je-matrix | 100 | 110 | **115** |
| mnemonics | 100 | 108 | **125** |
| phoenix-polyglot | 100 | 145 | **180** |

**结论**:
- Graal JIT: 特定场景领先
- Graal Native: 多数场景领先
- C2: 仍是可靠的默认选择

### 微基准对比

```java
// 1. 连续内存写入 (MergeStore)
byte[] buf = new byte[16];
for (int i = 0; i < 16; i++) {
    buf[i] = (byte)i;
}
```

| 编译器 | 优化 | 时间 (ns) |
|--------|------|----------|
| C2 (JDK 21+) | 部分合并 | 40 |
| Graal JIT | 完全合并 | 35 |
| Graal Native | SIMD | 20 |

```java
// 2. 条件对象分配
public int process(int x) {
    Point p = new Point(x, 0);
    if (x > 100) return p.x;
    return p.y;
}
```

| 编译器 | 优化 | 时间 (ns) |
|--------|------|----------|
| C2 | 无优化 (对象分配) | 80 |
| Graal JIT | 部分转逃 | 25 |
| Graal Native | 完全优化 | 15 |

---

## 实际应用建议

### 何时利用 Graal 优势

| 场景 | 推荐技术 |
|------|---------|
| **多语言** | Graal + Truffle |
| **Serverless** | Graal Native Image |
| **内存敏感** | Graal (部分转逃) |
| **复杂对象** | Graal (虚拟化) |
| **计算密集** | C2 或 Graal JIT |
| **通用应用** | C2 (默认选择) |

### 代码优化建议

#### 1. 编写 Graal 友好代码

```java
// 推荐: 小数组、明确边界
public void process() {
    byte[] data = new byte[16];  // 小数组可内联
    for (int i = 0; i < data.length; i++) {
        data[i] = value;  // 边界明确
    }
}

// 不推荐: 大数组、未知边界
public void process(int size) {
    byte[] data = new byte[size];  // 无法优化
    for (int i = 0; i < size; i++) {
        data[i] = value;
    }
}
```

#### 2. 利用部分转逃

```java
// 推荐: 条件路径分离
public int calculate(int x) {
    if (x > 100) {
        return x * 2;  // 不创建对象
    } else {
        Point p = new Point(x, 0);  // 只在这里创建
        return p.x + p.y;
    }
}
```

#### 3. 启用 Graal 优化

```bash
# GraalVM JIT
java -Dgraal.EscapeAnalysis=true \
     -Dgraal.IterativePEA=true \
     MyApp

# Native Image
native-image -H:+TruffleIterativePartialEscape \
             -H:+DeleteLocalVariables \
             MyApp
```

---

## 总结

### Graal 优势领域

| 领域 | C2 | Graal | 胜者 |
|------|----|-------|------|
| **内存合并** | JDK 21+ 改进 | 激进 | **相当** |
| **逃逸分析** | 全或无 | 部分 | **Graal** |
| **循环展开** | 保守 | 激进 | **Graal** |
| **条件消除** | 标准 | 高级 | **Graal** |
| **跨语言** | 无 | Truffle | **Graal** |

### 最终建议

```
不是 "Graal 全面优于 C2"
而是 "Graal 在高级优化上更激进"

选择:
├── 默认应用: C2 足够 (JDK 21+ 显著改进)
├── 性能关键: 考虑 Graal JIT
├── 云原生: Graal Native Image
└── 多语言: Graal + Truffle (唯一选择)
```

---

## 相关链接

### 本地文档

- [MergeStore 优化](mergestore.md) - C2 内存合并详解
- [逃逸分析详解](escape-analysis.md) - C2 逃逸分析
- [循环优化详解](loop-optimizations.md) - C2 循环优化
- [C2 优化阶段](c2-phases.md) - C2 编译阶段
- [Graal JIT 详解](graal-jit.md) - Graal 架构
- [Graal vs C2 性能对比](graal-vs-c2-performance.md) - 综合性能
- [Graal 独有特性](graal-unique-features.md) - 完整特性列表
- [最佳实践](best-practices.md) - JIT 友好代码

### 外部资源

- [GraalVM Optimizations and Performance](https://www.graalvm.org/latest/reference-manual/native-image/optimizations-and-performance/)
- [Oracle GraalVM Enterprise Release Notes](https://docs.oracle.com/en/graalvm/enterprise/22/docs/release-notes/)
- [Partial Evaluation for GraalVM](https://arxiv.org/pdf/2411.10559)

### 关键贡献者

| 贡献者 | 领域 |
|--------|------|
| [Lukas Stadler](/by-contributor/profiles/lukas-stadler.md) | 部分转逃分析 |
| [Doug Simon](/by-contributor/profiles/doug-simon.md) | Graal 编译器架构 |
| [Thomas Wuerthinger](/by-contributor/profiles/thomas-wuerthinger.md) | Truffle 框架 |
| [Christian Wimmer](/by-contributor/profiles/christian-wimmer.md) | Graal 优化 |
| [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | C2 MergeStore |

---

**最后更新**: 2026-03-21

**Sources:**
- [GraalVM Optimizations and Performance](https://www.graalvm.org/latest/reference-manual/native-image/optimizations-and-performance/)
- [Oracle GraalVM Enterprise Release Notes](https://docs.oracle.com/en/graalvm/enterprise/22/docs/release-notes/)
- [Partial Escape Analysis in Graal](https://chriswthomaspresentations.s3.amazonaws.com/PartialEscapeAnalysis.pdf)
