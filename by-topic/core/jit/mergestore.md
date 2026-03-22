# MergeStore 优化

> C2 JIT 编译器的内存写入合并优化技术

[← 返回 JIT 编译](./)

---

## 1. 快速概览

**MergeStore** 是 HotSpot C2 JIT 编译器的一项优化技术，能够将**多次连续的内存写入**合并为**单次宽写入**。

```java
// 原始代码
buf[0] = 'a';
buf[1] = 'b';
buf[2] = 'c';
buf[3] = 'd';

// JIT 优化后 (MergeStore)
Unsafe.putInt(buf, 0, 0x64636261);  // 单次 32 位写入
```

| 优势 | 说明 |
|------|------|
| **减少内存访问** | 4 次字节写入 → 1 次整型写入 |
| **提高缓存利用率** | 更少的内存总线占用 |
| **利用 CPU 宽写入** | 64 位 CPU 可一次写入 8 字节 |

---

## 目录

- [核心原理](#核心原理)
- [演进历史](#演进历史)
- [相关 PR](#相关-pr)
- [最佳实践](#最佳实践)
- [性能对比](#性能对比)

---

## 2. 核心原理

### C2 优化过程

```
原始字节码:
├── aload_2 (加载数组引用)
├── iconst_0
├── bipush 'a'
├── bastore (存储 'a')
├── iconst_1
├── bipush 'b'
├── bastore (存储 'b')
├── iconst_2
├── bipush 'c'
├── bastore (存储 'c')
├── iconst_3
├── bipush 'd'
└── bastore (存储 'd')

        ↓ C2 优化 (MergeStore)

优化后机器码:
├── mov eax, 0x64636261  ("abcd")
└── mov [buf], eax       (单次 32 位写入)
```

### 触发条件

| 条件 | 说明 |
|------|------|
| **连续存储** | 多次存储到连续地址 |
| **相同类型** | 字节/字符/整数 |
| **常量或可预测值** | JIT 可分析 |
| **安全边界** | 数组边界可验证 |

### 不触发的情况

```java
// ❌ 不连续的存储
buf[0] = 'a';
buf[5] = 'b';

// ❌ 不同类型的存储
buf[0] = (byte) x;
buf[1] = (char) y;

// ❌ 边界无法验证
for (int i = 0; i < unknown; i++) {
    buf[i] = value;  // unknown 可能导致越界
}
```

---

## 3. 演进历史

### JDK 23 (2024)

- **JDK-8318446**: 初始 MergeStore 优化
  - 支持基本类型数组
  - Big-Endian 和 Little-Endian
  - Unsafe 和 VarHandle 写入
- **JDK-8334342**: 添加 JMH 基准测试

### JDK 24 (2024-2025)

- **JDK-8333893**: StringBuilder append(boolean/null) 优化
- **JDK-8343629**: 扩展基准测试覆盖（新增 MergeLoadBench）
- **JDK-8349142**: 修复 MergeLoadBench 测试（VarHandle 偏移量错误）

### JDK 25 (2025)

- **JDK-8347405**: 支持反向字节序

### JDK 26 (2025-2026)

- **PR #28228**: 合并两个 append(char) 调用
- **PR #29688**: 优化连续 Latin1 字符追加
- **PR #29699**: StringBuilder char append 优化
- **JDK-8370405**: 修复标量替换错误

---

## 4. 贡献者

> **统计来源**: OpenJDK HotSpot 编译器团队 git 历史分析
> **统计时间**: 2026-03-20

### MergeStore 核心贡献者

| 贡献者 | 公司 | 主要贡献 |
|--------|------|----------|
| [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | Oracle | MergeStore 初始实现 (JDK-8318446) |
| [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) (温绍锦) | Alibaba | StringBuilder 优化, 性能测试 |
| [Vladimir Kozlov](/by-contributor/profiles/vladimir-kozlov.md) | Oracle | C2 编译器团队负责人, 技术指导 |
| [Roland Westrelin](/by-contributor/profiles/roland-westrelin.md) | Red Hat | C2 编译器团队, 循环优化 |

### Emanuel Peter

> **博客**: [Emanuel's HotSpot JVM C2 Blog](https://eme64.github.io/blog/)
> **档案**: [贡献者档案](/by-contributor/profiles/emanuel-peter.md)

- **职位**: OpenJDK Compiler Engineer, Oracle
- **团队**: HotSpot Compiler Team
- **经验**: 75+ JDK 贡献
- **身份**: JDK Committer (2023年5月获得)
- **专长**: C2 JIT 编译器优化
- **主要贡献**:
  - JDK-8318446: MergeStore 初始实现
  - JDK-8331311: Big-Endian 移植
  - C2 编译器博客系列作者

> "MergeStore combines multiple consecutive store operations into a single larger store operation."
> — Emanuel Peter, RFR: 8318446

### Vladimir Kozlov

- **职位**: HotSpot Compiler Team Lead, Oracle
- **经验**: 20+ 年 JVM 开发经验
- **主要贡献**:
  - C2 编译器架构设计
  - 循环优化文档 ([Loop optimizations in C2](https://wiki.openjdk.org/spaces/HotSpot/pages/20415918))
  - JDK-8371385: 非对齐访问修复 (Reviewer; 作者为 Fei Yang)

### Roland Westrelin

- **职位**: HotSpot Compiler Engineer, Red Hat
- **经验**: JDK Committer (2017年加入)
- **主要贡献**:
  - Loop Strip Mining in C2
  - C2 编译器优化和 Bug 修复
  - Code Cache 优化

### Shaojin Wen (温绍锦)

> **档案**: [贡献者档案](/by-contributor/profiles/shaojin-wen.md)

- **职位**: Alibaba, fastjson 负责人
- **主要贡献**:
  - JDK-8333893: StringBuilder boolean/null 优化
  - PR #28228: 合并两个 append(char)
  - PR #29688: Latin1 字符优化
  - MergeStore 基准测试完善

---

## 5. 邮件列表讨论

### RFR: JDK-8318446 (v12)

**主题**: [RFR: 8318446: C2: optimize stores into primitive arrays by combining values into larger store](https://mail.openjdk.org/pipermail/hotspot-compiler-dev/2024-February/073213.html)

> "This optimizes stores into primitive arrays by combining values into larger stores when possible."
> — Emanuel Peter, hotspot-compiler-dev@openjdk.org

**关键讨论点**:
- Big-Endian 平台支持 (s390x, PPC64)
- 与逃逸分析的交互
- 基准测试验证方法

### MergeStore 设计原则

> "The key insight is that the JIT can recognize patterns of consecutive stores to the same array and combine them into a single wider store."
> — HotSpot compiler-dev mailing list, 2024

---

## 6. 相关 PR

### 核心 JIT 优化

#### JDK-8318446: MergeStore 初始实现

> **状态**: 已集成 (JDK 23)
> **影响**: ⭐⭐⭐⭐⭐ 基础优化

**改进内容**:
- 基本类型数组存储合并
- Big-Endian/Little-Endian 支持
- Unsafe 和 VarHandle 优化路径

```java
// 优化前 (4 次字节存储)
array[offset] = (byte) (value >> 24);
array[offset + 1] = (byte) (value >> 16);
array[offset + 2] = (byte) (value >> 8);
array[offset + 3] = (byte) value;

// 优化后 (1 次整型存储)
UNSAFE.putInt(array, offset, value);
```

→ [基准测试分析](/by-pr/8334/8334342.md)

#### JDK-8347405: Reverse Bytes Order

> **状态**: 已集成 (JDK 25)
> **影响**: ⭐⭐⭐ 字节序优化

**改进内容**:
- 支持反向字节序的存储合并
- `Unsafe.putInt(array, offset, Integer.reverseBytes(value))`

### StringBuilder 优化

#### JDK-8333893: append(boolean) & append(null)

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ +5-15% 性能提升

**问题**: 原始实现无法触发 MergeStore

**解决方案**:
```java
// 优化前 - 无法触发 MergeStore
public AbstractStringBuilder append(boolean b) {
    writeInt(b ? 1 : 0);  // 间接调用
    return this;
}

// 优化后 - 可触发 MergeStore
public AbstractStringBuilder append(boolean b) {
    if (b) {
        putStringAt("true");   // 4 个连续字符
    } else {
        putStringAt("false");  // 5 个连续字符
    }
    return this;
}
```

**效果**:
- append(boolean): **+14.7%**
- append(null): **+9.2%**

→ [详细分析](/by-pr/8333/8333893.md)

#### PR #28228: 合并两个 append(char)

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ char append 优化

**改进**: 将两个连续的 `append(char)` 合并为 `append(char, char)`

```java
// 优化前
sb.append('a');
sb.append('b');

// 优化后 (新增方法)
sb.append('a', 'b');  // 可触发 MergeStore
```

#### PR #29688: 连续 Latin1 字符优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ Latin1 字符串优化

**改进**: 优化 `StringLatin1.putCharsAt` 以触发 MergeStore

```java
// 优化后 - 连续的 putByte 可被合并
static void putCharsAt(byte[] val, int index, int c1, int c2, int c3, int c4) {
    UNSAFE.putByte(val, address, (byte)(c1));
    UNSAFE.putByte(val, address + 1, (byte)(c2));
    UNSAFE.putByte(val, address + 2, (byte)(c3));
    UNSAFE.putByte(val, address + 3, (byte)(c4));
}
// JIT 优化为: UNSAFE.putInt(val, address, packedValue)
```

### Bug 修复

#### JDK-8349142: MergeLoadBench 测试修复

> **状态**: 已修复 (2025-02-02)
> **影响**: ⭐⭐⭐ 测试稳定性

**问题**: MergeLoadBench 中 VarHandle 使用错误的多余偏移量

**根因**: 在创建测试时复制了 Unsafe 代码模式，误加了 `Unsafe.ARRAY_BYTE_BASE_OFFSET`

**修复**: 移除 VarHandle 调用中的多余偏移量

→ [详细分析](/by-pr/8349/8349142.md)

#### JDK-8370405: 标量替换错误

> **状态**: 已修复
> **影响**: ⭐⭐⭐⭐ 重要修复

**问题**: MergeStores 在分配消除中被错误标量替换

**修复**: 改进逃逸分析和标量替换的交互

#### JDK-8371385: TestRematerializeObjects 失败

> **状态**: 已修复
> **平台**: s390x, 非 x86

**问题**: `-XX:-UseUnalignedAccesses` 下测试失败

**修复**: 改进非对齐访问的处理

---

## 7. 最佳实践

### 触发 MergeStore 的代码模式

#### ✅ 推荐模式

```java
// 1. 连续常量字符
static void putNull(byte[] buf, int offset) {
    buf[offset] = 'n';
    buf[offset + 1] = 'u';
    buf[offset + 2] = 'l';
    buf[offset + 3] = 'l';
}

// 2. 使用 Unsafe.putByte
static void putChars(byte[] buf, int offset) {
    UNSAFE.putByte(buf, base + offset, 'a');
    UNSAFE.putByte(buf, base + offset + 1, 'b');
    UNSAFE.putByte(buf, base + offset + 2, 'c');
    UNSAFE.putByte(buf, base + offset + 3, 'd');
}

// 3. Big-Endian 手动写入
static void putIntBE(byte[] buf, int offset, int value) {
    buf[offset] = (byte) (value >> 24);
    buf[offset + 1] = (byte) (value >> 16);
    buf[offset + 2] = (byte) (value >> 8);
    buf[offset + 3] = (byte) value;
}
```

#### ❌ 避免的模式

```java
// 1. 不连续的存储
buf[0] = 'a';
buf[5] = 'b';  // 跳过了索引 1-4

// 2. 动态索引
for (int i = 0; i < count; i++) {
    buf[getIndex(i)] = value;  // 索引不可预测
}

// 3. 条件存储
if (condition) {
    buf[0] = 'a';
}
buf[1] = 'b';  // 可能不连续
```

### StringBuilder 使用建议

```java
// ✅ 推荐: 直接 append 常量
sb.append("null");  // 可触发 MergeStore

// ✅ 推荐: 使用专门的 append 方法
sb.append(true);    // JDK-8333893 优化后

// ⚠️ 避免条件拼接
sb.append(x ? "yes" : "no");  // 三元运算符可能阻碍优化
```

---

## 8. 性能对比

### JMH 基准测试结果

| 方法 | 平均时间 (ns) | 相对性能 | MergeStore |
|------|---------------|----------|------------|
| **setIntB (手动)** | ~12000 | 基准 | ❌ |
| **setIntBU (Unsafe)** | ~8000 | +50% | N/A |
| **setIntBV (VarHandle)** | ~8500 | +41% | N/A |
| **setIntB (JIT 优化)** | ~8200 | +46% | ✅ |

### StringBuilder 优化效果

| 操作 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| append(boolean) | 45.2 ns | 38.5 ns | **+14.7%** |
| append(null) | 38.6 ns | 35.1 ns | **+9.2%** |
| append(char, char) | 28.4 ns | 24.2 ns | **+17.4%** |

### 真实场景影响

| 场景 | 预期提升 |
|------|----------|
| JSON 序列化 | +3-8% (预估值，无具体 benchmark 来源) |
| 日志格式化 | +2-5% (预估值，无具体 benchmark 来源) |
| 字符串拼接 | +5-15% (预估值，无具体 benchmark 来源) |

---

## 9. 诊断和验证

### 查看 JIT 编译输出

```bash
# 启用 JIT 编译日志
java -XX:+PrintCompilation -XX:+PrintInlining \
     -XX:+UnlockDiagnosticVMOptions \
     -XX:+PrintAssembly \
     YourClass

# 查看汇编输出
# 查找 "mov" 指令，确认是否使用宽写入
```

### JMH 基准测试

```bash
# 运行 MergeStore 基准测试
cd jdk
make test TEST="micro:java.lang.invoke.MergeStoreBench"

# 或直接运行
java -jar build/benchmarks/jars/micro-benchmarks.jar \
     MergeStoreBench
```

### 确认 MergeStore 生效

```java
// 测试代码
@Benchmark
public void putChars4(byte[] buf) {
    buf[0] = 't';
    buf[1] = 'e';
    buf[2] = 's';
    buf[3] = 't';
}

// 使用 -XX:+PrintAssembly 查看
// 优化后应该看到单次 mov 指令
```

---

## 10. 跨编译器对比

存储合并是一种通用的编译器优化技术，不同编译器在实现方式、触发时机和优化深度上有显著差异。本节将 HotSpot C2 的 MergeStore 与 GCC、LLVM、GraalVM 的对应实现进行对比分析。

### 10.1 GCC: -fstore-merging

GCC 的 [GIMPLE Store Merging Pass](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html) 是在 GCC 7 (2016) 中引入的优化，通过 `-fstore-merging` 标志控制。

**核心特性**:

- **默认在 `-O2` 及以上优化级别启用**（包括 `-Os`）
- 合并连续的窄标量存储为更宽的存储指令，减少指令数量
- 支持结构体成员的合并写入（例如连续初始化结构体字段）
- 支持死存储消除（多次写入同一位置时，只保留最后一次）

**典型优化示例**:

```c
// 优化前: 4 次 byte 存储
buf[0] = 'H';
buf[1] = 'e';
buf[2] = 'l';
buf[3] = 'l';

// GCC -O2 优化后: 1 次 int 存储
*(int*)buf = 0x6c6c6548;  // "Hell" (Little-Endian)
```

**与 HotSpot C2 的差异**:

- GCC 是 **AOT 编译器**，有充足的编译时间进行分析，可以做更激进的优化
- 在 GIMPLE 中间表示级别操作，拥有完整的程序信息
- 不需要考虑 Java 对象模型（数组边界检查、对象头等）
- 可以处理非对齐访问的架构限制（通过 `-fno-store-merging` 禁用）

**禁用选项**: 在某些架构上（如不支持非对齐访问的 ARM 变体），合并后的宽存储可能导致数据对齐错误，此时可通过 `-fno-store-merging` 关闭。

### 10.2 LLVM: MergeConsecutiveStores

LLVM 的存储合并优化分布在**多个编译阶段**，形成了一套多层次的优化策略。

**DAGCombiner 级别 (SelectionDAG)**:

[MergeConsecutiveStores](https://llvm.org/doxygen/DAGCombiner_8cpp_source.html) 是 DAGCombiner 中的核心存储合并函数：

- 扫描存储链，找到内存地址连续的存储候选
- 通过 `getStoreMergeCandidates` 识别合并候选，仅沿链分析
- `checkMergeStoreCandidatesForDependencies` 确保无环依赖
- `tryStoreMergeOfConstants` 专门处理常量值的存储链合并
- 支持从向量元素提取的连续存储合并
- 最近优化了缓存机制：缓存 `getMergeStoreCandidates` 的否定结果以节省编译时间

**InstCombine 级别 (IR)**:

- 在 LLVM IR 级别识别可合并的存储指令
- 支持等价指针操作数的存储合并（通过 bitcast 匹配类型）
- 当两个存储值都是 `ConstantInt` 时，可以移位合并为更大的常量存储
- 支持 memset 模式识别：将相同值的连续存储转化为 `memset` 调用

**向量化支持**:

- 多个标量 int 存储 → 单个 SIMD 向量写入
- 通过 `storeOfVectorConstantIsCheap()` 目标钩子判断向量存储是否有利
- GlobalISel 也有对应的常量值连续存储合并 Pass

**启用方式**: Clang `-O2` 自动启用，无需额外标志。

### 10.3 GraalVM

GraalVM 的 Graal 编译器采用了与 C2 不同的中间表示和优化架构。

**Graal JIT 编译器 (libgraal)**:

- 基于 **StructuredGraph**（Sea of Nodes 变体）进行优化
- 通过多个 Phase（优化阶段）实现各类优化
- 具备类似的存储优化能力，但实现策略与 C2 MergeStore 不同
- Graal 的 IR 更适合做高层语义优化，底层存储合并依赖后端代码生成

**Native Image (SubstrateVM)**:

- AOT 编译时有更多时间做激进优化
- 可以结合封闭世界假设（Closed-World Assumption），获得更完整的存储模式信息
- Profile-Guided Optimization (PGO) 可以指导存储合并决策
- 由于是静态编译，可以跨方法边界分析连续存储模式

**与 C2 MergeStore 的架构差异**:

- C2 使用经典 Sea of Nodes IR；Graal 使用 StructuredGraph（增强的 Sea of Nodes）
- C2 的 MergeStore 在 Ideal Graph 级别操作；Graal 的优化分散在多个 Phase 中
- Graal 通过 JVMCI 接口与 HotSpot 集成，可以替代 C2 作为 JIT 编译器
- Graal 的 Phase 机制更模块化，便于添加新的存储优化

### 10.4 对比表

| 特性 | HotSpot C2 | GCC | LLVM | GraalVM |
|------|-----------|-----|------|---------|
| **优化名称** | MergeStore | `-fstore-merging` | MergeConsecutiveStores | Phase-based 优化 |
| **编译时机** | JIT (运行时) | AOT | AOT | JIT / AOT |
| **默认启用** | JDK 23+ | `-O2`+ | `-O2`+ | 是 |
| **IR 级别** | Ideal Graph | GIMPLE | SelectionDAG + LLVM IR | StructuredGraph |
| **向量化合并** | 否 | 有限 | 是 (SIMD) | 有限 |
| **memset 识别** | 否 | 是 | 是 | 有限 |
| **Big-Endian** | 是 | 是 | 是 | 是 |
| **Profile-Guided** | 是 (JIT PGO) | 可选 (`-fprofile-use`) | 可选 (`-fprofile-use`) | 是 (JIT + AOT PGO) |
| **结构体合并** | N/A (Java 无结构体) | 是 | 是 | N/A |
| **引入时间** | 2024 (JDK 23) | 2016 (GCC 7) | 早期版本 | - |

### 10.5 HotSpot C2 的独特挑战

HotSpot C2 作为 JIT 编译器，在实现存储合并时面临若干 AOT 编译器不需要处理的约束：

**编译时间预算限制**:

- JIT 编译发生在运行时，必须在**毫秒级**时间内完成
- AOT 编译器（GCC、LLVM）没有时间限制，可以做更深层的分析
- C2 必须在优化收益和编译开销之间权衡

**Java 语义约束**:

- **数组边界检查**: 合并存储前必须确保所有访问在数组边界内
- **对象头**: Java 对象有头部信息（Mark Word、Klass Pointer），存储偏移量计算更复杂
- **空指针检查**: 需要确保目标引用非 null
- **类型安全**: Java 的强类型系统限制了跨类型存储合并的可能性

**逃逸分析交互**:

- 标量替换后的对象字段写入可能产生新的连续存储机会
- JDK-8370405 修复的 Bug 正是 MergeStore 与标量替换交互的问题
- 逃逸分析的结果直接影响 MergeStore 的触发条件

**GC 安全点约束**:

- 合并后的存储指令不能跨越 GC 安全点（Safepoint）
- 写屏障（Write Barrier）的存在限制了引用类型存储的合并
- 不同 GC（G1、ZGC、Shenandoah）的屏障实现影响合并策略

**虚方法内联依赖**:

- 连续存储可能来自不同的方法调用（如连续 `append` 调用）
- 只有在虚方法被内联后，JIT 才能看到完整的连续存储模式
- 内联决策直接影响 MergeStore 的优化效果

### 10.6 未来方向

**C2 AutoVectorization 与 MergeStore 的协同**:

- 当前 MergeStore 仅做标量宽化（byte→int→long），未利用 SIMD 指令
- LLVM 已支持将多个标量存储合并为向量存储（如 4 个 int → 1 个 128-bit SIMD）
- 未来 C2 可以结合 Vector API 和 AutoVectorization 实现类似优化

**支持更复杂的模式**:

- 条件存储合并：当分支两侧都有连续存储时的合并
- 循环内存储合并：识别循环展开后的连续存储模式
- 跨基本块的存储合并：当前仅在同一基本块内分析

**memset 模式识别**:

- GCC 和 LLVM 都能将相同值的连续存储转化为 `memset` 调用
- C2 目前缺少此优化，可以借鉴 LLVM 的 InstCombine 实现

**与 Graal JVMCI 的竞争**:

- Graal 通过 JVMCI 可以替代 C2，两者在存储优化上的竞争推动双方进步
- Leyden 项目（AOT 编译）可能为 HotSpot 带来类似 AOT 编译器的优化机会
- 未来 C2 和 Graal 可能在存储优化上趋于功能对等

---

## 11. 相关链接

### 内部文档

- [JIT 编译索引](index.md)
- [C2 编译阶段](c2-phases.md)
- [JIT 诊断工具](diagnostics.md)
- [Graal 高级优化](graal-advanced-optimizations.md) - MergeStore 对比
- [性能优化](../performance/)

### PR 分析

- [JDK-8334342: MergeStore JMH 基准测试](/by-pr/8334/8334342.md)
- [JDK-8333893: StringBuilder boolean/null 优化](/by-pr/8333/8333893.md)
- [JDK-8343629: 更多 MergeStore 基准测试](/by-pr/8343/8343629.md)
- [JDK-8349142: MergeLoadBench 测试修复](/by-pr/8349/8349142.md)

### 外部资源

- [JDK-8318446: MergeStore 初始实现](https://bugs.openjdk.org/browse/JDK-8318446)
- [JDK-8347405: Reverse Bytes Order](https://bugs.openjdk.org/browse/JDK-8347405)
- [JMH 文档](https://openjdk.org/projects/code-tools/jmh/)

### 邮件列表讨论

- [hotspot-compiler-dev](https://mail.openjdk.org/pipermail/hotspot-compiler-dev/)
- MergeStore 优化设计讨论

---

**最后更新**: 2026-03-20

**Sources**:
- [OpenJDK MergeStore PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+MergeStore+is%3Aclosed)
- [JDK-8318446 Bug Report](https://bugs.openjdk.org/browse/JDK-8318446)
