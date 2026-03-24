# Ian Graves

> **GitHub**: [@igraves](https://github.com/igraves)
> **Organization**: Oracle (Java Platform Group)
> **Role**: Vector API Owner (JEP 508), SIMD/向量化专家

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [主要 JEP 贡献](#3-主要-jep-贡献)
4. [核心技术贡献](#4-核心技术贡献)
5. [社区活动](#5-社区活动)
6. [技术专长](#6-技术专长)
7. [相关链接](#7-相关链接)

---


## 1. 概述

Ian Graves 是 Oracle Java Platform Group 的工程师，也是 **Java Vector API** 的核心贡献者和 **JEP 508 (Vector API, Tenth Incubator)** 的 Owner。他长期致力于在 Java 平台上实现高效的 **SIMD (Single Instruction Multiple Data)** 向量化计算能力，使 Java 程序能够利用现代 CPU 的向量扩展指令集 (SSE、AVX、NEON 等)。他早在 2016 年的 JVM Language Summit 上就展示了 Vector API 的设计理念。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Ian Graves |
| **当前组织** | Oracle (Java Platform Group) |
| **GitHub** | [@igraves](https://github.com/igraves) (58 followers, 52 repos) |
| **OpenJDK** | Member of @openjdk |
| **位置** | Kansas City 地区 |
| **专长** | Vector API, SIMD, Data-Parallel Computation, Vectorization, JVM Performance |

> **数据来源**: [GitHub](https://github.com/igraves), [JEP 508](https://openjdk.org/jeps/508), [JVMLS 2016 Presentation](https://www.oracle.com/technetwork/java/jvmls2016-graves-3125549.pptx)

---

## 3. 主要 JEP 贡献

### JEP 508: Vector API (Tenth Incubator) - JDK 25

| 属性 | 值 |
|------|-----|
| **角色** | Owner |
| **Reviewers** | Jatin Bhateja, Sandhya Viswanathan, Vladimir Ivanov |
| **Endorsed by** | Paul Sandoz |
| **状态** | Delivered |
| **发布版本** | JDK 25 |

**影响**: 作为 Vector API 的第十轮孵化迭代的 Owner，Ian Graves 负责推进 API 的持续改进和稳定化。

### Vector API 系列 JEP (参与贡献)

Vector API 从 JEP 338 (JDK 16) 开始，经历了多轮孵化迭代：

| JEP | 版本 | 状态 | 角色 |
|-----|------|------|------|
| JEP 338 | JDK 16 | Delivered | 贡献者 |
| JEP 414 | JDK 17 | Delivered | 贡献者 |
| JEP 417 | JDK 18 | Delivered | 贡献者 |
| JEP 426 | JDK 19 | Delivered | 贡献者 |
| JEP 438 | JDK 20 | Delivered | 贡献者 |
| JEP 448 | JDK 21 | Delivered | 贡献者 |
| JEP 460 | JDK 22 | Delivered | 贡献者 |
| JEP 469 | JDK 23 | Delivered | 贡献者 |
| JEP 489 | JDK 24 | Delivered | 贡献者 |
| **JEP 508** | **JDK 25** | **Delivered** | **Owner** |
| JEP 529 | JDK 26 | Incubator | 贡献者 |

---

## 4. 核心技术贡献

### 1. Java Vector API 设计与实现

Ian Graves 是 Java Vector API 的关键贡献者：
- **平台无关的向量化 API**: 设计了统一的向量计算接口，抽象底层硬件差异
- **SIMD 指令映射**: 将 Java 向量操作映射到 CPU 原生向量指令
- **数据并行计算**: 支持高效的批量数据处理

```java
// Vector API 示例
import jdk.incubator.vector.*;

static final VectorSpecies<Float> SPECIES = FloatVector.SPECIES_PREFERRED;

void vectorAdd(float[] a, float[] b, float[] c) {
    int i = 0;
    int upperBound = SPECIES.loopBound(a.length);
    for (; i < upperBound; i += SPECIES.length()) {
        var va = FloatVector.fromArray(SPECIES, a, i);
        var vb = FloatVector.fromArray(SPECIES, b, i);
        var vc = va.add(vb);
        vc.intoArray(c, i);
    }
    // 处理尾部元素
    for (; i < a.length; i++) {
        c[i] = a[i] + b[i];
    }
}
```

### 2. HotSpot C2 向量化

Vector API 依赖 HotSpot C2 编译器将向量操作编译为高效的硬件指令：
- **x64 架构**: SSE (Streaming SIMD Extensions) 和 AVX (Advanced Vector Extensions)
- **AArch64 架构**: NEON 和 SVE 向量指令
- **运行时编译**: 可靠的向量操作 JIT 编译优化

### 3. Project Panama 集成

Vector API 与 Project Panama 的 FFM API 集成：
- **超越函数**: 对于三角函数等运算，Vector API 通过 FFM API 链接到本地数学函数库
- **跨平台优化**: 利用本地代码实现平台特定的向量化优化

### 4. JVMLS 2016 早期设计

Ian Graves 在 2016 年 JVM Language Summit 上展示了 Vector API 的早期设计：
- **设计理念**: 为 Java 提供平台无关的数据并行计算能力
- **性能目标**: 接近手写向量化代码的性能

---

## 5. 社区活动

### 会议演讲

- **JVMLS 2016**: "Vector APIs for Java" — 展示了 Vector API 的设计理念和早期原型

### 邮件列表

在 OpenJDK 邮件列表中活跃：
- **panama-dev**: Vector API 和 Panama 项目讨论
- **hotspot-compiler-dev**: C2 编译器向量化支持讨论

### Inside.java

- **JVMLS 2025**: "Beyond the Vector API - A Quest for a Lower Level API" — 探索向量 API 的未来方向

---

## 6. 技术专长

### 向量化与 SIMD

- **Vector API**: Java 平台向量化 API 设计与实现
- **SIMD**: SSE, AVX, AVX-512, NEON, SVE 指令集
- **数据并行**: 批量数据处理优化

### JVM 性能

- **HotSpot C2**: JIT 编译器向量化支持
- **自动向量化**: 编译器自动向量化优化
- **性能基准**: 向量化操作性能评估

### 其他编程语言

- **Haskell**: 函数式编程 (GitHub 上有多个 Haskell 项目)
- **系统编程**: PE 格式解析、密码学实现

---

## 7. 相关链接

### 官方资料
- [GitHub - igraves](https://github.com/igraves)
- [JVMLS 2016: Vector APIs for Java](https://www.oracle.com/technetwork/java/jvmls2016-graves-3125549.pptx)

### JEP 文档
- [JEP 508: Vector API (Tenth Incubator)](https://openjdk.org/jeps/508)
- [JEP 529: Vector API (Eleventh Incubator)](https://openjdk.org/jeps/529)
- [JEP 489: Vector API (Ninth Incubator)](https://openjdk.org/jeps/489)
- [JEP 338: Vector API (Incubator)](https://openjdk.org/jeps/338)

### 技术资料
- [Inside.java: Beyond the Vector API](https://inside.java/2025/11/16/jvmls-vector-api/)
- [Vector API Javadoc (JDK 16)](https://docs.oracle.com/en/java/javase/16/docs/api/jdk.incubator.vector/jdk/incubator/vector/package-summary.html)

---

**Sources**:
- [GitHub - igraves](https://github.com/igraves)
- [JEP 508: Vector API (Tenth Incubator)](https://openjdk.org/jeps/508)
- [JEP 529: Vector API (Eleventh Incubator)](https://openjdk.org/jeps/529)
- [JEP 338: Vector API (Incubator)](https://openjdk.org/jeps/338)
- [JVMLS 2016: Vector APIs for Java](https://www.oracle.com/technetwork/java/jvmls2016-graves-3125549.pptx)
- [Inside.java: Beyond the Vector API](https://inside.java/2025/11/16/jvmls-vector-api/)

## 角色晋升 (CFV)

| 日期 | 角色 | 提名者 | 投票数 | 链接 |
|------|------|--------|--------|------|
| 2021-04-23 | Committer | Stuart Marks | 35 | [CFV](https://mail.openjdk.org/pipermail/jdk-dev/2021-April/005385.html) |


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 22 |
| **活跃仓库数** | 1 |
