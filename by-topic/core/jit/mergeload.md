# MergeLoad 优化

> C2 JIT 编译器的内存读取合并优化技术

[← 返回 JIT 编译](./)

---

## 1. 快速概览

**MergeLoad** 是 HotSpot C2 JIT 编译器的一项优化技术（开发中），能够将**多次连续的窄内存读取**合并为**单次宽读取**，然后通过移位/掩码提取各字段值。

```java
// 原始代码: 4 次字节读取
int v = (a[0] & 0xff)
      | ((a[1] & 0xff) << 8)
      | ((a[2] & 0xff) << 16)
      | ((a[3] & 0xff) << 24);

// JIT 优化后 (MergeLoad): 单次 32 位读取
int v = Unsafe.getInt(a, ARRAY_BYTE_BASE_OFFSET);  // 1 次 LoadI
```

| 优势 | 说明 |
|------|------|
| **减少内存访问** | 4 次字节读取 → 1 次整型读取 (75% reduction) |
| **降低指令数** | 消除移位 (shift) 和按位或 (OR) 指令 |
| **提高缓存利用率** | 更少的内存总线占用，单次缓存行访问 |
| **利用 CPU 宽读取** | 64 位 CPU 可一次读取 8 字节 |

> **当前状态**: MergeLoad 尚未集成到 JDK 主线。核心 PR ([JDK-8345485](https://bugs.openjdk.org/browse/JDK-8345485))
> 正在 Review 中，预计在 JDK 26 或更高版本集成。

---

## 目录

- [核心原理](#2-核心原理)
- [与 MergeStore 的关系](#3-与-mergestore-的关系)
- [演进历史](#4-演进历史)
- [贡献者](#5-贡献者)
- [相关 PR 详解](#6-相关-pr-详解)
- [实际应用场景](#7-实际应用场景)
- [触发条件与限制](#8-触发条件与限制)
- [性能对比](#9-性能对比)
- [跨编译器对比](#10-跨编译器对比)
- [诊断和验证](#11-诊断和验证)

---

## 2. 核心原理

### 2.1 MergeLoad 的变换过程

MergeLoad 是 MergeStore 的对称 (symmetric) 优化。MergeStore 将多次窄写入合并为一次宽写入，而 MergeLoad 将多次窄读取合并为一次宽读取。

```
原始 IR (Ideal Graph):

  LoadB[0]   LoadB[1]   LoadB[2]   LoadB[3]
     |          |          |          |
  And 0xff  And 0xff   And 0xff   And 0xff
     |          |          |          |
     |       LShift 8   LShift 16  LShift 24
     |          |          |          |
     +--- Or ---+--- Or ---+--- Or --+
                                     |
                                   result

        ↓ C2 MergeLoad 优化

优化后 IR:

  LoadI[0]  (单次 32 位读取)
     |
   result
```

### 2.2 支持的合并类型

| 合并模式 | 源操作 | 目标操作 | 指令减少 |
|----------|--------|----------|----------|
| 2 bytes → short | 2 × LoadB | 1 × LoadUS | 50% |
| 4 bytes → int | 4 × LoadB | 1 × LoadI | 75% |
| 8 bytes → long | 8 × LoadB | 1 × LoadL | 87.5% |
| 2 shorts → int | 2 × LoadUS | 1 × LoadI | 50% |
| 2 ints → long | 2 × LoadI | 1 × LoadL | 50% |

### 2.3 C2 优化过程 (IGVN Phase)

MergeLoad 在 C2 的 IGVN (Iterative Global Value Numbering) 阶段执行。与 MergeStore 在 `StoreNode::Ideal` 中实现不同，MergeLoad 的实现位于 `OrINode::Ideal` / `OrLNode::Ideal` (以及 `AddINode::Ideal` / `AddLNode::Ideal`)，从表达式树的底部 (combine operator) 向上匹配读取模式。

```
匹配方向:

  MergeStore: 从 StoreNode (内存链底部) 向上查找可合并的前驱 Store
                    ↑ 匹配方向

  MergeLoad:  从 OrNode / AddNode (表达式树底部) 向上查找 Load+Shift 模式
                    ↑ 匹配方向
```

Emanuel Peter 在 [PR #24023 Review](https://github.com/openjdk/jdk/pull/24023) 中指出:

> "I think your implementation should go into `OrINode`, and match the expression up from there.
> Because we want to replace the old `OrI` with the new `LoadL`."

### 2.4 支持的 Combine 操作符

| 操作符 | 节点类型 | 支持状态 | 约束 |
|--------|----------|----------|------|
| `\|` (OR) | OrINode / OrLNode | 已实现 | 无额外约束 |
| `+` (ADD) | AddINode / AddLNode | PR #29980 | 仅支持无符号读取 (LoadUB/LoadUS) |
| `^` (XOR) | XorINode / XorLNode | 未实现 | - |
| `&` (AND) | AndINode / AndLNode | 未实现 | - |

> **为什么 ADD 仅支持无符号读取?**
> 有符号字节读取 (LoadB) 在高位可能为 1 (负数)，移位后与 ADD 组合会产生进位传播 (carry propagation)，
> 导致结果与使用 OR 时不同。无符号读取 (LoadUB) 的 `& 0xFF` 掩码确保高位为 0，ADD 和 OR 等价。

---

## 3. 与 MergeStore 的关系

MergeLoad 和 MergeStore 是一对**互补优化** (complementary optimizations)，分别处理内存读写的合并：

### 3.1 对称性

```java
// === MergeStore (写入合并) ===
// 多次窄写入 → 单次宽写入
buf[0] = (byte)(value >> 24);
buf[1] = (byte)(value >> 16);
buf[2] = (byte)(value >> 8);
buf[3] = (byte)(value);
// → UNSAFE.putInt(buf, offset, value)

// === MergeLoad (读取合并) ===
// 多次窄读取 → 单次宽读取
int v = ((buf[0] & 0xff) << 24)
      | ((buf[1] & 0xff) << 16)
      | ((buf[2] & 0xff) << 8)
      | ((buf[3] & 0xff));
// → UNSAFE.getInt(buf, offset)
```

### 3.2 功能对比

| 特性 | MergeStore | MergeLoad |
|------|-----------|-----------|
| **方向** | 写入合并 | 读取合并 |
| **状态** | 已集成 (JDK 23+) | 开发中 (目标 JDK 26+) |
| **实现位置** | `StoreNode::Ideal` (memnode.cpp) | `OrINode::Ideal` / `AddINode::Ideal` (addnode.cpp) |
| **匹配模式** | 连续 Store 链 | Load+Shift+Or/Add 表达式树 |
| **JBS Issue** | JDK-8318446 | JDK-8345485 |
| **主要作者** | Emanuel Peter | Kuai Wei, Shaojin Wen |
| **字节序支持** | Big-Endian / Little-Endian | Big-Endian / Little-Endian |
| **反向字节序** | JDK-8347405 (已关闭，未集成) | 已包含在核心 PR |

### 3.3 互补应用场景

在二进制数据处理中，MergeStore 和 MergeLoad 经常成对出现：

```java
// 序列化: MergeStore 优化写入
static void serialize(byte[] buf, int offset, int value) {
    buf[offset    ] = (byte)(value >> 24);  // ┐
    buf[offset + 1] = (byte)(value >> 16);  // │ MergeStore → 1 次 putInt
    buf[offset + 2] = (byte)(value >>  8);  // │
    buf[offset + 3] = (byte)(value      );  // ┘
}

// 反序列化: MergeLoad 优化读取
static int deserialize(byte[] buf, int offset) {
    return ((buf[offset    ] & 0xff) << 24)  // ┐
         | ((buf[offset + 1] & 0xff) << 16)  // │ MergeLoad → 1 次 getInt
         | ((buf[offset + 2] & 0xff) <<  8)  // │
         | ((buf[offset + 3] & 0xff)      ); // ┘
}
```

### 3.4 架构讨论: 统一 MergeMemory Phase

Emanuel Peter 在 PR review 中转述了 Quan Anh Mai (@merykitty) 的想法：

> "Once proposed the idea of not doing MergeStores / MergeLoads as IGVN optimizations,
> but rather to just have a separate and dedicated phase. That would allow you to take a
> global view, collect all loads (and stores), put them in a big list, and then make groups
> that belong together."
> — Emanuel Peter, [PR #24023](https://github.com/openjdk/jdk/pull/24023) review, 2025-06-17

这种方法的潜在优势：
- 全局视图，可以同时分析所有 Load/Store 节点
- 避免 IGVN 中的重复匹配和标志位开销
- 可以扩展到 copy pattern (如 `a[i] = b[i]` 的连续拷贝)
- 更容易处理多组合并候选的冲突

Kuai Wei 在 2025-07-18 关闭了 PR #24023，计划按此方向重构：

> "It need rework to combine merge loads and merge stores in separate optimize phase."

---

## 4. 演进历史

### JDK 24 (2025) — 基准测试准备

- **JDK-8343629** ([PR #21659](https://github.com/openjdk/jdk/pull/21659)): 新增 MergeStore 基准测试 (MergeStoreBench)，同时包含 MergeLoadBench
  - 作者: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
  - 集成时间: 2025-01-08
  - 为未来 MergeLoad 优化建立性能基线

- **JDK-8349142** ([PR #23393](https://github.com/openjdk/jdk/pull/23393)): 修复 MergeLoadBench 测试
  - 作者: sendaoYan
  - 集成时间: 2025-02-02
  - 修复 VarHandle 调用中多余的 `Unsafe.ARRAY_BYTE_BASE_OFFSET` 偏移量

### JDK 25 (2025) — 初始实现

- **JDK-8345485** ([PR #24023](https://github.com/openjdk/jdk/pull/24023)): 核心 MergeLoad 实现 (v1)
  - 作者: [Kuai Wei](/by-contributor/profiles/kuai-wei.md)
  - 状态: 已关闭 (2025-07-18)，计划重构为独立 Phase
  - 支持 Or 操作符的 2/4/8 字节读取合并
  - 经过 Emanuel Peter 深度 Review (16+ 轮修订)

### JDK 26 (2026) — 继续开发

- **JDK-8345485** ([PR #29955](https://github.com/openjdk/jdk/pull/29955)): MergeLoad 实现 (v2) by Shaojin Wen
  - 状态: 已关闭 (2026-02-28)
  - 基于 Kuai Wei 原始实现，添加 2 字节合并和 Bug 修复

- **JDK-8345485** ([PR #29980](https://github.com/openjdk/jdk/pull/29980)): MergeLoad + Add 操作符 (v3)
  - 作者: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
  - 状态: **进行中** (Open)
  - 新增 Add 操作符 (AddI/AddL) 支持
  - 包含 `TestMergeLoadsAdd.java` 测试 (324 行)
  - 支持 x86-64, AArch64, PPC64, s390x, RISC-V (with Zbb)

---

## 5. 贡献者

> **统计来源**: OpenJDK GitHub PR 历史分析
> **统计时间**: 2026-03-22

### MergeLoad 核心贡献者

| 贡献者 | 公司 | 主要贡献 |
|--------|------|----------|
| [Kuai Wei](/by-contributor/profiles/kuai-wei.md) | - | MergeLoad 初始实现 (PR #24023), MergeStore 反向字节序 |
| [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) (温绍锦) | Alibaba | MergeLoadBench, MergeLoad v2/v3, Add 操作符支持 |
| [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | Oracle | MergeStore 作者, MergeLoad 技术审查和架构指导 |
| [Roberto Castaneda Lozano](https://github.com/robcasloz) | Oracle | C2 编译器 Review |
| sendaoYan | - | MergeLoadBench VarHandle 修复 (JDK-8349142) |

### [Kuai Wei](/by-contributor/profiles/kuai-wei.md)

- **GitHub**: [kuaiwei](https://github.com/kuaiwei)
- **主要贡献**:
  - PR #24023: MergeLoad 初始实现 (16+ 轮修订)
  - PR #23030: MergeStore 反向字节序支持 (JDK-8347405)
  - 将 MergeStore 扩展为 MergeLoad 的第一人
- **设计决策**:
  - 最初在 `LoadNode::Ideal` 中实现，后按 Emanuel Peter 建议迁移到 `addnode.cpp`
  - 最终决定重构为独立 Phase，关闭了 PR #24023

### Shaojin Wen (温绍锦)

> **档案**: [贡献者档案](/by-contributor/profiles/shaojin-wen.md)

- **职位**: Alibaba, fastjson 负责人
- **MergeLoad 贡献**:
  - JDK-8343629: MergeLoadBench 基准测试
  - PR #29955: MergeLoad v2 (rebased + 2-byte merge)
  - PR #29980: MergeLoad + Add 操作符 (当前进行中)
  - 详细的应用场景分析 (密码学、网络、字符串处理)

### Emanuel Peter

> **博客**: [Emanuel's HotSpot JVM C2 Blog](https://eme64.github.io/blog/)
> **档案**: [贡献者档案](/by-contributor/profiles/emanuel-peter.md)

- **职位**: OpenJDK Compiler Engineer, Oracle
- **角色**: MergeLoad 的核心 Reviewer 和架构指导
- **关键反馈**:
  - 建议将实现从 `LoadNode::Ideal` 迁移到 `OrINode::Ideal`
  - 要求添加 "nodes with other uses" 测试
  - 提出统一 MergeMemory Phase 的架构方向

---

## 6. 相关 PR 详解

### 6.1 PR #24023: MergeLoad 初始实现 (Kuai Wei)

> **Issue**: [JDK-8345485](https://bugs.openjdk.org/browse/JDK-8345485)
> **状态**: 已关闭 (2025-07-18, 计划重构)
> **修订**: 16+ 轮
> **影响**: 基础架构

**核心改动**:
- 在 `addnode.cpp` 中实现 `OrINode::Ideal` / `OrLNode::Ideal` 的读取合并
- 新增 `MergePrimitiveLoads` 类（类似 `MergePrimitiveStores`）
- 支持 Or 操作符的 2/4/8 字节合并
- 包含 `TestMergeLoads.java` 测试

**基准测试结果** (AMD EPYC 9T24, ns/op):

| 测试用例 | 无 MergeLoad | 有 MergeLoad | 加速比 |
|----------|-------------|-------------|--------|
| getIntBU (4-byte Unsafe BE) | 6854 | 2764 | **2.48x** |
| getIntLU (4-byte Unsafe LE) | 6741 | 2603 | **2.59x** |
| getIntRL (4-byte Reverse LE) | 16323 | 7787 | **2.10x** |
| getLongBU (8-byte Unsafe BE) | 14042 | 2513 | **5.59x** |
| getLongLU (8-byte Unsafe LE) | 14113 | 2238 | **6.31x** |
| getLongRBU (8-byte Reverse BE) | 14031 | 2520 | **5.57x** |
| getLongRLU (8-byte Reverse LE) | 14125 | 2240 | **6.31x** |

> 注意: `getIntB` / `getLongB` (数组直接访问模式) 加速较小，因为 C2 已有部分优化。
> Unsafe 访问模式 (`*U` 后缀) 获益最大。

(AArch64 数据见 PR #24023 原始 benchmark，此处略)

**Review 关键讨论**:

1. **实现位置**: Emanuel Peter 建议从 `LoadNode::Ideal` 迁移到 `OrINode::Ideal`
2. **其他用途测试**: 要求验证 Load/Or 节点有其他使用者时的正确性
3. **标志位问题**: 讨论是否使用 `_merge_memops_checked` 标志位 vs 模式匹配
4. **统一 Phase**: 最终讨论导向将 MergeLoad/MergeStore 统一为独立 Phase

### 6.2 PR #29980: MergeLoad + Add 操作符 (Shaojin Wen)

> **Issue**: [JDK-8345485](https://bugs.openjdk.org/browse/JDK-8345485)
> **状态**: **进行中** (Open)
> **影响**: 扩展优化范围

**核心改动**:
- 在 Or 操作符基础上新增 Add (AddI/AddL) 支持
- 新增辅助函数:
  - `is_unsigned_load_opcode()` — 检查 LoadUB/LoadUS
  - `is_add_combine_opcode()` — 识别 AddI/AddL
  - `is_same_combine_type()` — 确保同一链中不混合 Or/Add
- 新增 `_merge_memops_checked` 成员到 AddINode 和 AddLNode
- 新增 `TestMergeLoadsAdd.java` (324 行)

**Add 操作符约束**:
```java
// Or 操作符: 有符号和无符号读取都支持
int v1 = (a[0] & 0xff) | ((a[1] & 0xff) << 8);       // LoadUB + Or
int v2 = (a[0])        | ((a[1])        << 8);        // LoadB  + Or (也支持)

// Add 操作符: 仅支持无符号读取 (防止进位传播)
int v3 = (a[0] & 0xff) + ((a[1] & 0xff) << 8);        // LoadUB + Add (支持)
int v4 = (a[0])        + ((a[1])        << 8);        // LoadB  + Add (不支持!)
```

**受益的核心库代码** (来自 PR #29980 分析):

| 模块 | 文件 | 操作符 | 影响 |
|------|------|--------|------|
| 后量子密码学 | ML_DSA.java, ML_KEM.java | ADD | NIST 标准量子安全算法加速 |
| 网络安全 | OutputRecord.java (SSL/TLS) | ADD | TLS 记录处理优化 |
| 经典密码学 | BlowfishCrypt.java, RC2Crypt.java | OR/ADD | 加解密性能提升 |
| 字符串处理 | UTF_32Coder.java, CharacterName.java | OR | UTF-32 解码加速 |
| 二进制格式 | ImageLocation.java (JIMAGE) | OR | 模块镜像加载加速 |
| 认证 | NTLM.java | ADD | NTLM 认证性能提升 |

**平台支持**:

| 平台 | 支持状态 | 关键指令 |
|------|----------|----------|
| x86-64 | 完整支持 | BSWAP |
| AArch64 | 完整支持 | REV |
| PPC64 | 完整支持 | LWBRX/STWBRX |
| s390x | 完整支持 | LRV |
| RISC-V | 有条件支持 | 需要 Zbb 扩展 |
| ARM32 | 不支持 | 不支持非对齐访问 |

### 6.3 JDK-8343629: MergeLoadBench 基准测试

> **PR**: [#21659](https://github.com/openjdk/jdk/pull/21659)
> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **集成**: 2025-01-08
> **影响**: 测试基础设施

为 MergeLoad 优化建立 JMH 基准测试基线。测试文件位于:
`test/micro/org/openjdk/bench/vm/compiler/MergeLoadBench.java`

覆盖的测试场景:
- `getIntB` / `getIntL`: Big-Endian / Little-Endian 数组字节读取
- `getIntBU` / `getIntLU`: Unsafe 字节读取
- `getIntBV` / `getIntLV`: VarHandle 读取 (基线参照)
- `getIntRB` / `getIntRL`: 带 `Integer.reverseBytes()` 的读取
- `getLong*`: 64 位 Long 型的对应测试
- `getChar*`: 16 位 Char 型的对应测试

### 6.4 JDK-8349142: MergeLoadBench VarHandle 修复

> **PR**: [#23393](https://github.com/openjdk/jdk/pull/23393)
> **作者**: sendaoYan
> **集成**: 2025-02-02
> **影响**: 测试正确性

**问题**: MergeLoadBench 中 `getCharBV` 等 VarHandle 基准测试失败。

**根因**: 在创建 MergeLoadBench 时，从 Unsafe 代码模式复制而来，VarHandle 调用中误加了 `Unsafe.ARRAY_BYTE_BASE_OFFSET`。VarHandle 已经内部处理了数组偏移量，多余的偏移量导致越界访问。

**修复**: 移除 VarHandle 调用中的多余偏移量。

→ [详细分析](/by-pr/8349/8349142.md)

---

## 7. 实际应用场景

### 7.1 二进制协议解析

网络协议处理是 MergeLoad 最典型的应用场景。许多网络协议使用 Big-Endian 字节序，需要从字节数组中读取多字节整数。

```java
// HTTP/2 帧头解析: 3 字节长度字段
public static int readFrameLength(byte[] header, int offset) {
    return ((header[offset    ] & 0xff) << 16)
         | ((header[offset + 1] & 0xff) <<  8)
         | ((header[offset + 2] & 0xff)      );
    // MergeLoad: 3 × LoadB → 优化的内存访问
}

// TCP 头部解析: 16 位端口号
public static int readPort(byte[] packet, int offset) {
    return ((packet[offset] & 0xff) << 8)
         | ((packet[offset + 1] & 0xff));
    // MergeLoad: 2 × LoadB → 1 × LoadUS
}

// DNS 查询: 32 位 IP 地址
public static int readIPv4(byte[] data, int offset) {
    return ((data[offset    ] & 0xff) << 24)
         | ((data[offset + 1] & 0xff) << 16)
         | ((data[offset + 2] & 0xff) <<  8)
         | ((data[offset + 3] & 0xff)      );
    // MergeLoad: 4 × LoadB → 1 × LoadI
}
```

### 7.2 反序列化

JSON、Protobuf、Avro 等序列化框架需要从字节流中读取多字节数值。

```java
// fastjson2 风格的 VarInt 读取
public static long readVarLong(byte[] buf, int offset) {
    return  ((long)(buf[offset    ] & 0xff)      )
          | ((long)(buf[offset + 1] & 0xff) <<  8)
          | ((long)(buf[offset + 2] & 0xff) << 16)
          | ((long)(buf[offset + 3] & 0xff) << 24)
          | ((long)(buf[offset + 4] & 0xff) << 32)
          | ((long)(buf[offset + 5] & 0xff) << 40)
          | ((long)(buf[offset + 6] & 0xff) << 48)
          | ((long)(buf[offset + 7] & 0xff) << 56);
    // MergeLoad: 8 × LoadB → 1 × LoadL (87.5% 指令减少)
}
```

### 7.3 密码学算法

后量子密码学 (Post-Quantum Cryptography) 和经典密码学算法大量使用字节拼装模式。

```java
// ML-DSA (FIPS 204) 后量子数字签名 — 使用 ADD 操作符
// java.base: sun.security.provider.ML_DSA (lines 875-885)
// 注意: 下方为简化示意，实际代码中的索引为非连续访问 (vIndex+1, +3, +5, +7, +8)，
// 不会直接触发 MergeLoad 合并。MergeLoad 仅对连续地址的读取生效。
// 实际优化收益来自其中连续部分的合并。
int coeff = ((v[vIndex + 1] & 0xff) << 8)
          + ((v[vIndex + 3] & 0xff) << 6)
          + ((v[vIndex + 5] & 0xff) << 4)
          + ((v[vIndex + 7] & 0xff) << 2)
          + ((v[vIndex + 8] & 0xff) << 10);
// 需要 ADD 操作符支持 (PR #29980)

// Blowfish 加密 — 使用 OR 操作符
// java.base: com.sun.crypto.provider.BlowfishCrypt (lines 197-203)
int temp = ((in[offset    ]       ) << 24)
         | ((in[offset + 1] & 0xff) << 16)
         | ((in[offset + 2] & 0xff) <<  8)
         | ((in[offset + 3] & 0xff)      );
// MergeLoad: 4 × LoadB → 1 × LoadI
```

### 7.4 字符串与文本处理

```java
// UTF-32 解码: 4 字节码点
// java.base: sun.nio.cs.UTF_32Coder (lines 43-51)
int cp = ((src.get() & 0xff) << 24)
       | ((src.get() & 0xff) << 16)
       | ((src.get() & 0xff) <<  8)
       | ((src.get() & 0xff)      );
// MergeLoad: 4 × get() → 优化的宽读取

// UTF-16 字符读取
// 手动从 byte[] 读取 char (Latin1 → UTF-16 转换等场景)
char c = (char)(((val[index] & 0xff))
              | ((val[index + 1] & 0xff) << 8));
// MergeLoad: 2 × LoadB → 1 × LoadUS
```

### 7.5 图像/像素处理

```java
// RGBA 像素读取
int pixel = (pixels[offset    ] & 0xFF)         // R
          | ((pixels[offset + 1] & 0xFF) <<  8)  // G
          | ((pixels[offset + 2] & 0xFF) << 16)  // B
          | ((pixels[offset + 3] & 0xFF) << 24); // A
// MergeLoad: 4 × LoadB → 1 × LoadI
```

### 7.6 SSL/TLS 记录处理

```java
// TLS 记录头长度读取 — 使用 ADD 操作符
// java.base: sun.security.ssl.OutputRecord (lines 564-565)
int v3CSLen = ((fragment[v3CSLenOffset    ] & 0xff) << 8)
            + ((fragment[v3CSLenOffset + 1] & 0xff));
// 需要 ADD 操作符支持 → 2 × LoadB → 1 × LoadUS
```

---

## 8. 触发条件与限制

### 8.1 触发条件

| 条件 | 说明 |
|------|------|
| **连续地址** | 多次读取的内存地址必须连续相邻 |
| **同一数组/内存** | 所有读取必须来自同一基地址 (base pointer) |
| **Combine 操作符** | 读取结果通过 Or 或 Add 组合 |
| **位移模式** | 每个读取值的左移量构成连续的 8/16/32 位偏移 |
| **无符号掩码** | 通常需要 `& 0xff` / `& 0xffff` 掩码 (Or 操作符对有符号读取也支持) |
| **平台支持** | 目标平台支持非对齐访问 (unaligned access) |

### 8.2 可触发的代码模式

```java
// Pattern 1: Little-Endian 4 字节读取 (最常见)
int v = (a[off] & 0xff)
      | ((a[off + 1] & 0xff) << 8)
      | ((a[off + 2] & 0xff) << 16)
      | ((a[off + 3] & 0xff) << 24);

// Pattern 2: Big-Endian 4 字节读取
int v = ((a[off] & 0xff) << 24)
      | ((a[off + 1] & 0xff) << 16)
      | ((a[off + 2] & 0xff) << 8)
      | ((a[off + 3] & 0xff));

// Pattern 3: Unsafe 字节读取
int v = ((UNSAFE.getByte(a, base) & 0xff))
      | ((UNSAFE.getByte(a, base + 1) & 0xff) << 8)
      | ((UNSAFE.getByte(a, base + 2) & 0xff) << 16)
      | ((UNSAFE.getByte(a, base + 3) & 0xff) << 24);

// Pattern 4: 2-byte char 读取
char c = (char)(((val[i] & 0xff))
              | ((val[i + 1] & 0xff) << 8));

// Pattern 5: 使用 ADD 操作符 (仅无符号)
int v = (a[off] & 0xff)
      + ((a[off + 1] & 0xff) << 8)
      + ((a[off + 2] & 0xff) << 16)
      + ((a[off + 3] & 0xff) << 24);
```

### 8.3 不触发的情况

```java
// 1. 不连续的读取
int v = (a[0] & 0xff) | ((a[5] & 0xff) << 8);  // 跳过了索引 1-4

// 2. 不同数组的读取
int v = (a[0] & 0xff) | ((b[1] & 0xff) << 8);  // 来自不同数组

// 3. 混合 Or 和 Add
int v = (a[0] & 0xff) | ((a[1] & 0xff) << 8)
      + ((a[2] & 0xff) << 16);                  // Or 和 Add 混合

// 4. 有符号读取 + Add (进位传播风险)
int v = a[0] + (a[1] << 8);                     // 无 & 0xff, 有符号 + Add

// 5. 移位量不匹配
int v = (a[0] & 0xff) | ((a[1] & 0xff) << 7);   // 应该是 << 8

// 6. 中间有副作用
int v = (a[0] & 0xff) | ((sideEffect(a, 1) & 0xff) << 8);

// 7. Load/Or 节点有其他使用者 (其他代码也引用了中间 Or 结果)
int mid = (a[0] & 0xff) | ((a[1] & 0xff) << 8);
int v = mid | ((a[2] & 0xff) << 16) | ((a[3] & 0xff) << 24);
use(mid);  // mid 有其他使用者，阻止合并

// 8. 平台不支持非对齐访问 (ARM32 等)
// 在这些平台上 MergeLoad 被禁用
```

---

## 9. 性能对比

### 9.1 MergeLoadBench 基准测试 (AMD EPYC 9T24)

以下数据来自 [PR #24023](https://github.com/openjdk/jdk/pull/24023) 的基准测试结果 (单位: ns/op):

#### Int (32-bit) 读取

| 测试用例 | 描述 | 无 MergeLoad | 有 MergeLoad | 加速 |
|----------|------|-------------|-------------|------|
| getIntB | 数组 Big-Endian | 11200 | 6869 | **38.7%** |
| getIntBU | Unsafe Big-Endian | 6854 | 2764 | **59.7%** |
| getIntL | 数组 Little-Endian | 10427 | 6524 | **37.4%** |
| getIntLU | Unsafe Little-Endian | 6741 | 2603 | **61.4%** |
| getIntRB | Reverse Big-Endian | 11336 | 8981 | **20.8%** |
| getIntRBU | Reverse Unsafe BE | 7440 | 3190 | **57.1%** |
| getIntRL | Reverse Little-Endian | 16323 | 7787 | **52.3%** |
| getIntRLU | Reverse Unsafe LE | 7458 | 3364 | **54.9%** |
| getIntU | Unsafe 直接 (基线) | 2501 | 2501 | 0% |

#### Long (64-bit) 读取

| 测试用例 | 描述 | 无 MergeLoad | 有 MergeLoad | 加速 |
|----------|------|-------------|-------------|------|
| getLongBU | Unsafe Big-Endian | 14042 | 2513 | **82.1%** |
| getLongLU | Unsafe Little-Endian | 14113 | 2238 | **84.1%** |
| getLongRBU | Reverse Unsafe BE | 14031 | 2520 | **82.0%** |
| getLongRLU | Reverse Unsafe LE | 14125 | 2240 | **84.1%** |
| getLongU | Unsafe 直接 (基线) | 3060 | 3058 | 0% |

> **关键发现**: Unsafe 字节读取模式 (`*U` 后缀) 获益最大，因为 C2 对这些模式
> 此前没有类似优化。8 字节 Long 读取的加速比最高可达 **6.3x**。

### 9.2 已有 Unsafe/VarHandle 为什么不够?

| 方式 | 优点 | 缺点 |
|------|------|------|
| `Unsafe.getInt()` | 最快，单次读取 | 非标准 API，不安全 |
| `VarHandle.get()` | 标准 API，类型安全 | 需要额外代码，不适用于已有代码 |
| 手动 OR/ADD | 可移植，无依赖 | 性能差 (多次读取+移位+OR) |
| **MergeLoad** | **自动优化手动模式** | **编译器级别，零代码改动** |

MergeLoad 的价值在于: 大量已有的 Java 代码使用手动 OR/ADD 模式读取多字节值，
这些代码无需修改即可自动获得性能提升。

### 9.3 预期真实场景影响

| 场景 | 预期提升 | 说明 |
|------|----------|------|
| 二进制协议解析 | +20-60% | 频繁的字节拼装操作 |
| JSON/Protobuf 反序列化 | +5-15% | VarInt 和定长字段读取 |
| 密码学运算 | +10-30% | Blowfish, RC2, ML-DSA 等 |
| 字符串解码 (UTF-32) | +15-40% | 4 字节码点读取 |
| 图像像素处理 | +20-50% | RGBA 像素读取 |

---

## 10. 跨编译器对比

### 10.1 GCC: 加载合并优化

GCC 的加载合并能力主要体现在以下方面:

- **GIMPLE 级别**: `tree-ssa-forwprop.c` 中的前向传播可以识别连续字节加载+移位+OR 模式
- **RTL 级别**: combine pass 可以将多个窄加载合并为宽加载
- 在 `-O2` 及以上级别自动启用
- 支持结构体成员的连续读取合并

```c
// GCC 可以优化此模式:
unsigned int read_le32(const unsigned char *p) {
    return p[0] | (p[1] << 8) | (p[2] << 16) | (p[3] << 24);
}
// → 生成单次 32 位加载指令 (x86: mov eax, [rdi])
```

### 10.2 LLVM: InstCombine + DAGCombiner

LLVM 在多个层级实现加载合并:

- **InstCombine**: IR 级别识别 load+shift+or 模式，转化为宽加载
- **DAGCombiner**: SelectionDAG 级别的 `MergeConsecutiveStores` 也处理加载方向
- **SLP Vectorizer**: 可以将多个标量加载合并为向量加载

LLVM 的加载合并是 C/C++ 编译器中最成熟的实现之一。

### 10.3 GraalVM

根据 [PR #29980 的分析](https://github.com/openjdk/jdk/pull/29980):

| 操作符 | HotSpot C2 (PR) | GraalVM |
|--------|-----------------|---------|
| OR | 支持 | 支持 (`FloatingReadPhase`) |
| ADD | 支持 (PR #29980) | 支持 (`CanonicalizerPhase`) |
| XOR | 不支持 | 有条件支持 (`XorNode`) |
| AND | 不支持 | 有条件支持 (`AndNode`) |

GraalVM 在 XOR 和 AND 操作符上有优势，对 AES 加密 (XOR 模式) 和位掩码操作 (AND 模式) 有额外的优化能力。(来源: PR 评论，未经 GraalVM 源码验证)

### 10.4 对比表

| 特性 | HotSpot C2 | GCC | LLVM | GraalVM |
|------|-----------|-----|------|---------|
| **加载合并** | 开发中 (JDK 26+) | 成熟 (`-O2`+) | 成熟 (`-O2`+) | 部分支持 |
| **编译时机** | JIT (运行时) | AOT | AOT | JIT / AOT |
| **Or 合并** | 是 | 是 | 是 | 是 |
| **Add 合并** | 是 (PR) | 有限 | 有限 | 是 |
| **XOR 合并** | 否 | 否 | 是 | 有条件 |
| **Big-Endian** | 是 | 是 | 是 | 是 |
| **BSWAP 识别** | 是 | 是 | 是 | 是 |
| **引入时间** | 开发中 | 早期版本 | 早期版本 | - |

### 10.5 HotSpot C2 的独特挑战

作为 JIT 编译器，C2 在实现 MergeLoad 时面临额外挑战:

**编译时间预算**:
- JIT 必须在毫秒级完成编译
- MergeLoad 的模式匹配需要遍历表达式树，IGVN 中可能被多次触发
- 需要权衡匹配深度和编译时间

**表达式树排列**:
- Or/Add 操作符的输入可能有多种排列方式
- `(((a Or b) Or c) Or d)` vs `((a Or b) Or (c Or d))`
- 必须处理各种合法的 C2 IR 形态

**与现有优化的交互**:
- 数组边界检查消除 (RangeCheck elimination)
- 公共子表达式消除 (CSE) 可能共享中间节点
- 内联决策影响可见的连续读取模式

---

## 11. 诊断和验证

### 11.1 运行 MergeLoadBench 基准测试

```bash
# 构建 JDK 微基准测试
cd /path/to/jdk
make test TEST="micro:java.lang.invoke.MergeLoadBench"

# 或直接运行
java -jar build/benchmarks/jars/micro-benchmarks.jar \
     "MergeLoadBench"
```

### 11.2 查看 JIT 编译输出

```bash
# 启用 JIT 编译日志，查找 MergeLoad 优化效果
java -XX:+PrintCompilation \
     -XX:+UnlockDiagnosticVMOptions \
     -XX:+PrintAssembly \
     -XX:CompileCommand=compileonly,*YourClass::getIntL \
     YourClass

# 在汇编输出中查找:
# 优化前: 多个 movzbl (字节加载) + shl + or 指令
# 优化后: 单个 mov (32/64 位加载) 指令
```

### 11.3 验证代码模式

```java
// 测试代码: 验证 MergeLoad 是否触发
@Benchmark
public int readIntLE(byte[] buf) {
    return (buf[0] & 0xff)
         | ((buf[1] & 0xff) << 8)
         | ((buf[2] & 0xff) << 16)
         | ((buf[3] & 0xff) << 24);
}

// 使用 -XX:+PrintAssembly 查看
// 优化前: movzbl + shl + or (4 组)
// 优化后: mov eax, [rsi+0x10]  (单次 32 位加载)
```

### 11.4 IR 可视化 (Ideal Graph Visualizer)

```bash
# 使用 IGV 可视化 C2 IR，观察 MergeLoad 前后的节点变化
java -XX:+UnlockDiagnosticVMOptions \
     -XX:+PrintIdeal \
     -XX:+PrintIdealGraphLevel=4 \
     -XX:+PrintIdealGraphFile=mergeload.xml \
     YourClass

# 在 IGV 中查找:
# 优化前: LoadB → AndI → LShiftI → OrI (多层嵌套)
# 优化后: LoadI (单个节点)
```

### 11.5 确认平台支持

```bash
# 检查当前 JDK 是否支持非对齐访问
java -XX:+PrintFlagsFinal 2>&1 | grep -i unaligned
# UseUnalignedAccesses = true  → 支持 MergeLoad
# UseUnalignedAccesses = false → MergeLoad 被禁用
```

---

## 12. 相关链接

### 内部文档

- [JIT 编译索引](README.md)
- [MergeStore 优化](mergestore.md) — 对称的写入合并优化
- [C2 编译阶段](c2-phases.md)
- [JIT 诊断工具](diagnostics.md)
- [Graal 高级优化](graal-advanced-optimizations.md)

### PR 分析

- [JDK-8349142: MergeLoadBench 测试修复](/by-pr/8349/8349142.md)
- [JDK-8343629: MergeLoadBench 基准测试](/by-pr/8343/8343629.md)

### 外部资源

- [JDK-8345485: MergeLoads 增强](https://bugs.openjdk.org/browse/JDK-8345485)
- [PR #24023: MergeLoad 初始实现](https://github.com/openjdk/jdk/pull/24023) (Kuai Wei)
- [PR #29980: MergeLoad + Add 操作符](https://github.com/openjdk/jdk/pull/29980) (Shaojin Wen, 进行中)
- [PR #29955: MergeLoad v2](https://github.com/openjdk/jdk/pull/29955) (Shaojin Wen, 已关闭)
- [MergeLoadBench 源码](https://github.com/openjdk/jdk/blob/master/test/micro/org/openjdk/bench/vm/compiler/MergeLoadBench.java)
- [Emanuel Peter 的 C2 博客](https://eme64.github.io/blog/)
- [Performance Improvements in JDK 25 - Inside.java](https://inside.java/2025/10/20/jdk-25-performance-improvements/)

### 邮件列表

- [hotspot-compiler-dev](https://mail.openjdk.org/pipermail/hotspot-compiler-dev/)

---

**最后更新**: 2026-03-22

**Sources**:
- [PR #24023: MergeLoad 初始实现](https://github.com/openjdk/jdk/pull/24023)
- [PR #29980: MergeLoad + Add 操作符](https://github.com/openjdk/jdk/pull/29980)
- [PR #29955: MergeLoad v2](https://github.com/openjdk/jdk/pull/29955)
- [JDK-8345485 Bug Report](https://bugs.openjdk.org/browse/JDK-8345485)
- [MergeLoadBench.java](https://github.com/openjdk/jdk/blob/master/test/micro/org/openjdk/bench/vm/compiler/MergeLoadBench.java)
- [Emanuel's HotSpot JVM C2 Blog](https://eme64.github.io/blog/)
- [Performance Improvements in JDK 25 - Inside.java](https://inside.java/2025/10/20/jdk-25-performance-improvements/)
