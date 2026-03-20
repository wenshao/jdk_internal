# JIT 编译

> C1、C2、分层编译、Graal 演进历程

[← 返回核心平台](../)

---

## 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 6 ── JDK 9 ── JDK 17 ── JDK 21 ── JDK 26
   │         │        │        │        │        │        │
解释器    C1/C2   分层    Graal   JIT    虚拟线程  SuperWord
纯解释   分离    编译     JIT     优化     支持    成本模型
                  Tiered           性能
```

### 核心演进

| 版本 | 特性 | 说明 | 深度分析 |
|------|------|------|----------|
| **JDK 1.0** | 解释器 | 纯解释执行 | - |
| **JDK 1.3** | C2 (Server Compiler) | 高性能编译器 | [C2 优化阶段](c2-phases.md) |
| **JDK 1.4** | C1 (Client Compiler) | 快速启动编译器 | [C1 编译器详解](c1-compiler.md) |
| **JDK 5** | C1/C2 分离 | -client/-server | [编译器对比](#编译器对比) |
| **JDK 6** | 分层编译 | C1 + C2 组合 | [分层编译详解](tiered-compilation.md) |
| **JDK 9** | Graal JIT | 实验性高性能 JIT | [Graal JIT](graal-jit.md) |
| **JDK 17** | JIT 优化 | 编译器改进 | [近期改进](recent-changes.md) |
| **JDK 21** | String Templates, Record Patterns | 模式匹配优化 | [近期改进](recent-changes.md) |
| **JDK 23** | JIT 性能 | 编译吞吐量提升 | [近期改进](recent-changes.md) |
| **JDK 26** | SuperWord 成本模型 | 智能向量化 | [SuperWord 向量化](superword.md) |

---

## 编译器对比

### 快速对比

| 编译器 | 全称 | 特点 | 适用场景 |
|--------|------|------|----------|
| **解释器** | Interpreter | 启动快，执行慢 | 应用启动、冷代码 |
| **C1** | Client Compiler | 编译快，优化少 | 桌面应用、短时运行 |
| **C2** | Server Compiler | 编译慢，深度优化 | 长期运行的服务器应用 |
| **Graal** | Graal JIT | 基于 Java，可扩展 | 实验性，特定场景 |

### C1 vs C2 详细对比

| 维度 | C1 (Client Compiler) | C2 (Server Compiler) |
|------|----------------------|----------------------|
| **设计目标** | 快速编译，低延迟 | 深度优化，高吞吐量 |
| **编译速度** | 快 (毫秒级) | 慢 (秒级) |
| **优化时间** | < 100ms | 1-5 秒 |
| **代码质量** | 中等 | 优秀 |
| **启动影响** | 小 | 大 |
| **稳态性能** | 中等 | 最佳 |
| **内存占用** | 低 | 高 (编译期间) |

### 优化能力对比

| 优化技术 | C1 | C2 |
|----------|----|----|
| **内联** | ✅ 保守内联 | ✅ 激进内联 |
| **常量折叠** | ✅ 局部 | ✅ 全局 |
| **死代码消除** | ✅ 基本 | ✅ 激进 |
| **循环优化** | ❌ 无 | ✅ 完整 (展开/剥离/外提) |
| **逃逸分析** | ❌ 无 | ✅ 有 |
| **标量替换** | ❌ 无 | ✅ 有 |
| **向量化** | ❌ 无 | ✅ SuperWord SIMD |
| **寄存器分配** | 线性扫描 | 图着色算法 |
| **全局值编号** | ❌ 无 | ✅ 有 |

### 内联策略对比

| 方面 | C1 | C2 |
|------|----|----|
| **内联阈值** | ~35 字节码 | ~325 字节码 |
| **最大内联深度** | 2-3 层 | 9+ 层 |
| **虚方法内联** | 保守 (需类型统计) | 激进 (基于 profiling) |
| **内联失败** | 放弃 | 记录供后续优化 |

### 性能特征对比

```
启动性能:
解释器 > C1 > C2

稳态性能 (长时间运行):
C2 > C1 > 解释器

内存占用:
解释器 < C1 < C2 (编译期间)

编译时间:
C1 < C2
```

### 使用场景

| 场景 | 推荐编译器 | 原因 |
|------|------------|------|
| **GUI 应用** | C1 | 快速响应用户操作 |
| **批处理任务** | C2 | 长时间运行，最大化吞吐量 |
| **微服务** | C1 + C2 (分层) | 快速启动 + 高性能 |
| **大数据处理** | C2 | 计算密集型 |
| **桌面应用** | C1 | 交互式应用 |
| **服务器应用** | C2 | 7x24 长期运行 |

### 分层编译 (Tiered Compilation)

```
Level 0: 解释执行 (Interpreter)
Level 1: C1 (纯解释 profiling)
Level 2: C1 (有限 profiling)
Level 3: C1 (完全 profiling)
Level 4: C2 (深度优化)
```

**编译策略:**
- 方法从 Level 0 开始
- 达到阈值后升级到下一层
- C1 收集 profiling 信息供 C2 使用
- C2 可以基于 profiling 做更激进的优化

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### JIT 编译器 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | 72 | Oracle | C1/C2 编译器 |
| 2 | [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | 68 | Oracle | JIT 编译器 |
| 3 | [Ioi Lam](/by-contributor/profiles/ioi-lam.md) | 62 | Oracle | 编译器, 运行时 |
| 4 | Stefan Karlsson | 31 | Oracle | 编译器, GC |
| 5 | [Doug Simon](/by-contributor/profiles/doug-simon.md) | 29 | Oracle | JIT 编译器 |
| 6 | [David Holmes](/by-contributor/profiles/david-holmes.md) | 24 | Oracle | 并发, 编译器 |
| 7 | [Claes Redestad](/by-contributor/profiles/claes-redestad.md) | 24 | Oracle | 编译器优化 |
| 8 | [Thomas Stuefe](/by-contributor/profiles/thomas-stuefe.md) | 22 | Oracle | 编译器 |
| 9 | [Vladimir Kozlov](/by-contributor/profiles/vladimir-kozlov.md) | 20 | Oracle | JIT 编译器 |
| 10 | [Igor Veresov](/by-contributor/profiles/igor-veresov.md) | 17 | Oracle | JIT 编译器 |

### C2 专项贡献者

| 排名 | 贡献者 | 主要贡献 | 组织 |
|------|--------|----------|------|
| 1 | [Vladimir Kozlov](/by-contributor/profiles/vladimir-kozlov.md) | C2 架构师 | Oracle |
| 2 | [Roland Westrelin](/by-contributor/profiles/rooland-westrelin.md) | C2 优化 (JDK-8325495) | Oracle |
| 3 | [John Rose](/by-contributor/profiles/john-rose.md) | invokedynamic, JIT | Oracle |
| 4 | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | SuperWord 向量化, C2 博客作者 | Oracle |
| 5 | [Christian Hagedorn](/by-contributor/profiles/christian-hagedorn.md) | C2 优化, GVN | Oracle |
| 6 | [Johannes Graham](/by-contributor/profiles/johannes-graham.md) | C2 常量折叠优化 | Oracle |

---

## 文档导航

### 核心概念

#### 编译器架构

- [C1 编译器详解](c1-compiler.md) - Client Compiler 完整分析
  - HIR/LIR 中间表示
  - 线性扫描寄存器分配
  - 7 个编译阶段详解
- [C2 优化阶段](c2-phases.md) - 15 个编译阶段详解
  - PhaseIterGVN、PhaseIdealLoop、PhaseCCP
  - 逃逸分析、标量替换、向量化
- [Ideal Graph 详解](ideal-graph.md) - C2 中间表示
  - SSA 形式、节点类型、图变换
  - IGV 可视化工具使用

#### 编译策略

- [分层编译详解](tiered-compilation.md) - C1 + C2 组合策略
  - Level 0-4 编译层级
  - Profiling 数据收集
  - 启动性能与稳态性能平衡
- [Graal JIT](graal-jit.md) - 基于 Java 的 JIT 编译器
  - JVMCI 架构
  - Truffle 框架
  - SubstrateVM Native Image

#### 优化技术深度分析

- [内联优化](inlining.md) - JIT 内联策略和启发式算法
  - C1/C2 内联对比
  - 内联阈值和决策流程
  - 内联友好设计模式
- [循环优化详解](loop-optimizations.md) - C2 循环优化技术
  - 循环展开、剥离、外提
  - 循环融合、交换
  - PhaseIdealLoop 流程
- [SuperWord 向量化](superword.md) - 自动 SIMD 优化
  - SIMD 指令集
  - 成本模型 (JDK-8340093)
  - VTransform 架构
- [逃逸分析详解](escape-analysis.md) - 对象分配优化
  - 标量替换、栈上分配、锁消除
  - 连接图算法
  - 编程建议
- [寄存器分配详解](register-allocation.md) - 线性扫描 vs 图着色
  - 活跃分析、溢出处理
  - C1/C2 算法对比
- [MergeStore 优化](mergestore.md) - 内存写入合并优化
  - 多次字节存储合并为单次宽写入
  - StringBuilder 优化案例
  - JMH 基准测试

### 配置参考

- [VM 参数](vm-parameters.md) - 完整参数参考
  - 编译器选择、阈值、代码缓存
  - 内联控制、C2 特定参数

### 调试诊断

- [诊断工具](diagnostics.md) - 调试和性能分析
  - 编译日志、JFR、jhsdb
  - Ideal Graph 可视化

### 历史演进

- [版本时间线](timeline.md) - JDK 1.0 到 JDK 26
- [近期改进](recent-changes.md) - 2024-2025 更新
- [C2 迭代速度分析](c2-pace-analysis.md) - C2是否"迭代慢"？事实核查
- [C2 活跃度时间线](c2-activity-timeline.md) - 按月度展示PR、新功能、活跃度
- [分层编译历史](tiered-compilation.md#分层编译的历史) - JDK 6 引入
- [Graal JIT 演进](graal-jit.md#近期发展) - JDK 9+ 支持

---

## 快速参考

### 常用 VM 参数

```bash
# 启用分层编译 (默认)
-XX:+TieredCompilation

# 调整编译阈值
-XX:CompileThreshold=10000         # C2 阈值
-XX:FreqInlineSize=325             # 热方法内联阈值

# 代码缓存
-XX:ReservedCodeCacheSize=256m

# 诊断
-XX:+PrintCompilation             # 打印编译活动
-XX:+PrintInlining                 # 打印内联决策
-XX:+CITime                       # 编译时间统计
```

### 诊断命令

```bash
# 查看编译活动
jcmd <pid> Compiler.compile

# JFR 记录
jcmd <pid> JFR.start name=jit
jcmd <pid> JFR.dump name=jit filename=jit.jfr

# jhsdb 诊断
jhsdb clhsdb --pid <pid>
> printcodecache
```

---

## 内部结构

### HotSpot 编译器源码

```
src/hotspot/share/
├── compiler/
│   ├── compileBroker.cpp          # 编译任务调度
│   ├── compilation.cpp            # 编译策略
│   └── compilerOracle.cpp         # 编译规则
├── c1/                            # C1 (Client Compiler)
│   ├── c1_Compilation.cpp         # C1 编译入口
│   ├── c1_GraphBuilder.cpp        # IR 构建
│   ├── c1_Optimizer.cpp           # C1 优化器
│   ├── c1_LinearScan.cpp          # 寄存器分配 (线性扫描)
│   ├── c1_Canonicalizer.cpp       # 规范化
│   ├── c1_ValueMap.cpp            # 值编号
│   └── c1_CodeGenerator.cpp        # 代码生成
├── opto/                          # C2 (Server Compiler)
│   ├── compile.cpp                # C2 编译入口, Optimize()
│   ├── gvn.cpp                    # Global Value Numbering
│   ├── loopopts.cpp               # 循环优化
│   ├── escape.cpp                 # 逃逸分析
│   ├── superword.cpp              # SuperWord 向量化
│   ├── vtransform.cpp             # VTransform 架构 (JDK 26+)
│   ├── matcher.cpp                # 指令匹配
│   ├── chaitin.cpp                # 寄存器分配 (图着色)
│   └── output.cpp                 # 代码生成
└── jvmci/                         # JVMCI (Graal 接口)
```

### C1 vs C2 源码结构对比

| 组件 | C1 | C2 |
|------|----|----|
| **IR 构建** | `c1_GraphBuilder.cpp` | `parse.cpp` (在 opto/) |
| **优化器** | `c1_Optimizer.cpp` | `compile.cpp::Optimize()` |
| **值编号** | `c1_ValueMap.cpp` | `gvn.cpp` (全局值编号) |
| **寄存器分配** | `c1_LinearScan.cpp` (线性扫描) | `chaitin.cpp` (图着色) |
| **代码生成** | `c1_CodeGenerator.cpp` | `output.cpp` (LIR → 机器码) |
| **循环优化** | ❌ 无 | `loopopts.cpp` (完整) |
| **逃逸分析** | ❌ 无 | `escape.cpp` |
| **向量化** | ❌ 无 | `superword.cpp` |

---

## C2 编译流程概览

```
字节码
   │
   ▼
Parse Phase ────────► 解析字节码 → Ideal Graph
   │                      内联优化
   ▼                      初始 GVN
PhaseIterGVN ◄────────── 全局值编号
   │                      常量折叠
   ▼                      公共子表达式消除
PhaseIdealLoop ────────► 循环优化 (多轮迭代)
   │                      Peeling/Unswitching/Unrolling
   ▼
PhaseCCP ───────────────► 条件常量传播
   │                      死代码消除
   ▼
PhaseEscapeAnalysis ───► 逃逸分析
   │                      标量替换
   ▼                      栈上分配
PhaseMacroExpand ──────► 宏扩展
   │                      锁优化
   ▼
PhaseSuperWord ────────► SIMD 向量化
   │
   ▼
代码生成 ───────────────► 寄存器分配 → 机器码
```

---

## C1 编译流程概览

```
字节码
   │
   ▼
GraphBuilder ───────► 构建 HIR (High-level IR)
   │                      基础优化
   ▼
Canonicalizer ───────► IR 规范化
   │                      简化表达式
   ▼
ValueNumbering ───────► 局部值编号
   │                      冗余消除
   ▼
Optimizer ────────────► C1 优化器
   │                      内联、常量折叠
   ▼
LinearScan ───────────► 寄存器分配
   │                      线性扫描算法
   ▼
CodeGenerator ────────► 代码生成
   │                      LIR → 机器码
```

**C1 vs C2 编译阶段对比**:

| 阶段 | C1 | C2 |
|------|----|----|
| **IR 类型** | HIR (High-level IR) + LIR | Ideal Graph + MachNodes |
| **IR 构建** | GraphBuilder (单遍) | Parse (多遍，内联) |
| **优化** | Optimizer (基础) | 多个 Phase (激进) |
| **值编号** | ValueNumbering (局部) | GVN (全局) |
| **寄存器分配** | LinearScan (快速) | Chaitin (图着色) |
| **代码生成** | LIR → 机器码 | MachNodes → 机器码 |
| **总阶段数** | ~5 | 15+ |

**C1 设计原则**:
- 快速编译 > 代码质量
- 简单算法 > 复杂优化
- 单遍处理 > 多遍迭代
- 牺牲性能换取编译速度

---

## 重要 PR 分析

### SuperWord 向量化优化系列

> **主要贡献者**: [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md)

SuperWord 是 C2 JIT 编译器的 SIMD 向量化优化组件，在 JDK 23-26 中经历了重大架构改进。

#### JDK-8340093: SuperWord 成本模型

> **作者**: [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md)
> **影响**: ⭐⭐⭐⭐⭐ 智能向量化决策

引入了成本模型来智能判断向量化是否真的能带来性能提升：

**优化前**:
- 盲目向量化所有可向量化的循环
- 未考虑 shuffle/pack/unpack 开销
- 可能导致性能下降

**优化后**:
- 计算向量化的真实成本
- 考虑数据重排开销
- 评估归约操作的收益
- 只在真正有利可图时才向量化

**成本模型考虑因素**:
| 因素 | 说明 |
|------|------|
| 向量宽度 | 128-bit (SSE) vs 256-bit (AVX) vs 512-bit (AVX-512) |
| 循环迭代次数 | 少量迭代可能不值得向量化 |
| 内存访问模式 | 连续访问 vs 随机访问 |
| Shuffle 开销 | 数据重排操作的 CPU 周期 |
| 对齐状态 | 对齐访问更快，不对齐需要额外处理 |

#### JDK-8334431: 修复 SuperWord Store-to-Load 转发失败

> **作者**: [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md)
> **影响**: ⭐⭐⭐⭐⭐ 性能回归修复

修复了 JDK-8325155 引入的性能回归问题，恢复 Store-to-Load 转发优化。

→ [详细分析](/by-pr/8333/8334431.md)

#### JDK-8344085: 改进小循环迭代计数的 SuperWord 向量化

> **作者**: [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md)
> **影响**: ⭐⭐⭐⭐ 小循环优化

改进小循环（4-16 次迭代）的向量化决策，避免错误地向量化导致性能下降。

→ [详细分析](/by-pr/8344/8344085.md)

#### JDK-8328938: SuperWord 大步长禁用

> **作者**: [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md)
> **影响**: ⭐⭐⭐ 算法边界修复

禁用步长 > 1 的循环向量化，避免错误的优化。

#### JDK-8324890: SuperWord VLoop 分析器重构

> **作者**: [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md)
> **影响**: ⭐⭐⭐⭐ 架构改进

重构 VLoopAnalyzer 和 VTransformGraph 架构，为后续优化奠定基础。

→ [详细分析](/by-pr/8324/8324890.md)

#### JDK-8333713: SuperWord 清理重命名

> **作者**: [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md)
> **影响**: ⭐⭐ 代码质量

清理 SuperWord 代码，改进命名和可维护性。

→ [详细分析](/by-pr/8333/8333713.md)

**SuperWord VM 参数**:
```bash
-XX:+UseSuperWord                 # 启用向量化 (默认开启)
-XX:MaxVectorSize=32               # 最大向量大小 (字节)
-XX:+TraceSuperWord               # 跟踪向量化决策
-XX:CompileCommand=print,*SuperWord*  # 打印 SuperWord 信息
```

---

### MergeStore 优化系列

> **完整专题**: [MergeStore 优化](mergestore.md)

MergeStore 是 C2 JIT 编译器的一项优化技术，将多次连续的内存写入合并为单次宽写入。

#### JDK-8333893: StringBuilder append(boolean/null) 优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ +5-15% 性能提升

重写 `appendNull` 和 `append(boolean)` 方法，使其能被 C2 JIT 的 MergeStore 优化：

```java
// 优化后 - 可触发 MergeStore
static void putCharsAt(byte[] val, int index, int c1, int c2, int c3, int c4) {
    UNSAFE.putByte(val, address, (byte)(c1));
    UNSAFE.putByte(val, address + 1, (byte)(c2));
    UNSAFE.putByte(val, address + 2, (byte)(c3));
    UNSAFE.putByte(val, address + 3, (byte)(c4));
}
// JIT 优化为: UNSAFE.putInt(val, address, packedValue)
```

**效果**: append(boolean) +14.7%, append(null) +9.2%

→ [详细分析](/by-pr/8333/8333893.md) | [MergeStore 专题](mergestore.md)

#### JDK-8334342: MergeStore JMH 基准测试

> **作者**: Shaojin Wen
> **影响**: ⭐⭐⭐ 测试基础设施

为 MergeStore JIT 优化添加标准化 JMH 基准测试：

- Big-Endian / Little-Endian 写入
- VarHandle vs Unsafe vs 数组访问
- 性能回归测试

→ [详细分析](/by-pr/8334/8334342.md)

### JDK-8365186: Reduce size of DateTimePrintContext::adjust

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ +3-12% 日期格式化性能提升

这个 PR 展示了方法大小对 JIT 内联的影响：

**问题**: `DateTimePrintContext.adjust` 方法字节码大小 382 > 325 字节，导致 C2 无法内联

**解决方案**: 将 382 字节的单一方法拆分为三个方法

| 方法 | 大小 | 用途 |
|------|------|------|
| `adjust()` | 27 字节 | 热路径：快速返回（90%+ 场景） |
| `adjustWithOverride()` | 123 字节 | 中等路径：有覆盖的情况 |
| `adjustSlow()` | 232 字节 | 冷路径：复杂边界情况 |

**性能数据**:

| 平台 | Benchmark | 提升 |
|------|-----------|------|
| MacBook M1 Pro | formatInstants (HH:mm:ss) | +6.84% |
| Intel Xeon | formatInstants (HH:mm:ss) | +6.53% |
| Aliyun Yitian 710 | formatInstants (HH:mm:ss) | +9.89% |

**关键启示**:
- C2 热方法内联阈值约 325 字节
- 方法拆分可以让热路径被内联
- 冷热代码分离可以提升整体性能

→ [详细分析](/by-pr/8365/8365186.md)

### JDK-8349400: Improve startup speed via eliminating nested classes

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ 启动类加载数量 -90%

这个 PR 通过消除枚举中的匿名内部类来优化启动性能：

**问题**: `KnownOIDs` 枚举中有 10 个匿名内部类覆盖 `registerNames()` 方法

**解决方案**: 将方法覆盖转换为构造函数参数

```java
// 优化前：匿名内部类
KP_TimeStamping("1.3.6.1.5.5.7.3.8", "timeStamping") {
    @Override
    boolean registerNames() { return false; }
}

// 优化后：构造函数参数
KP_TimeStamping("1.3.6.1.5.5.7.3.8", "timeStamping", false)
```

**效果**:
- 类加载数量：11 个 → 1 个（-90%）
- 元空间占用：约 22KB → 4KB
- 对 Java Agent 场景特别有益

→ [详细分析](/by-pr/8349/8349400.md)

### JDK-8355177: Speed up StringBuilder::append(char[])

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐⭐ +15% 性能提升

使用 `Unsafe.copyMemory` 替代 `System.arraycopy` 优化字符数组复制：

**优化点**:
- 消除 JNI 边界跨越
- 消除边界检查（容量已确保）
- 消除类型检查
- `Unsafe.copyMemory` 是 `@IntrinsicCandidate`，JIT 会内联

**性能提升**: +15.2% (微基准)

→ [详细分析](/by-pr/8355/8355177.md)

### JDK-8341906: Optimize ClassFile writing BufBuffer

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ +28% 字节码写入性能提升

通过写入合并优化 ClassFile API 性能：

**优化策略**: 将多次小写入合并为一次大写入

```java
// 优化前：3 次方法调用
buf.writeU1(u1Value);
buf.writeU2(u2Value);
buf.writeU4(u4Value);

// 优化后：1 次方法调用
buf.writeU1U2U4(u1Value, u2Value, u4Value);
```

**性能提升分解**:
- 减少方法调用：~15%
- 减少边界检查：~8%
- 更好的内联：~3%
- 局部性优化：~2%

→ [详细分析](/by-pr/8341/8341906.md)

---

## JIT 内联优化最佳实践

### 方法大小控制

| 方法类型 | 推荐大小 | 说明 |
|----------|----------|------|
| **热路径方法** | < 50 字节 | 确保 C1/C2 都能内联 |
| **常规方法** | < 200 字节 | C2 可内联 |
| **复杂方法** | 拆分为多个方法 | 冷热分离 |

### 方法拆分模式

```java
// 不推荐：大方法混合冷热代码
public void process() {
    // 200 行热路径代码
    // ...
    // 100 行边界情况处理
}

// 推荐：拆分为多个方法
public void process() {
    // 20 行热路径
    if (commonCase) {
        return;
    }
    processUncommon();
}

private void processUncommon() {
    // 边界情况处理
}
```

### 内联友好设计

1. **保持方法简短** - 热路径 < 50 字节
2. **早期返回** - 常见情况优先处理
3. **避免大 switch** - 使用策略模式
4. **静态方法** - 比虚方法更容易内联
5. **final 方法** - 消除多态调用

---

## 相关链接

### 本地文档

- [C2 优化阶段](c2-phases.md) - 15 个编译阶段详解
- [VM 参数](vm-parameters.md) - 完整参数参考
- [诊断工具](diagnostics.md) - 调试和性能分析
- [近期改进](recent-changes.md) - 2024-2025 更新
- [版本时间线](timeline.md) - JDK 1.0 到 JDK 26

### 相关主题

- [性能优化](../performance/) - 编译器优化
- [GC 演进](../gc/) - GC 与 JIT 协作
- [JVM 调优](../jvm/) - VM 参数

### 外部参考

**官方文档:**
- [Tuning Java HotSpot VM](https://docs.oracle.com/javase/8/docs/technotes/guides/vm/performance.html)
- [HotSpot Internals Wiki](https://wiki.openjdk.org/display/HotSpot)

**技术博客:**
- [Emanuel's HotSpot C2 Blog](https://eme64.github.io/blog/) - [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) 的 C2 编译器深入解析
  - [Part 1: C2 Overview](https://eme64.github.io/blog/2024/12/06/Intro-to-C2-Part01.html)
  - [Part 2: GVN](https://eme64.github.io/blog/2024/12/24/Intro-to-C2-Part02.html)
  - [Part 3: Inlining](https://eme64.github.io/blog/2024/12/31/Intro-to-C2-Part03.html)
  - [Part 4: Loop Optimizations](https://eme64.github.io/blog/2025/01/23/Intro-to-C2-Part04.html)

**Bug 跟踪:**
- [JDK-8325497: C2 性能调查](https://bugs.openjdk.org/browse/JDK-8325497)
- [JDK-8340093: SuperWord 成本模型](https://bugs.openjdk.org/browse/JDK-8340093) - [相关 PR](/by-pr/8340/8340093.md)
- [JDK-8347645: XOR 常量折叠修复](https://bugs.openjdk.org/browse/JDK-8347645) - [分析](/by-pr/8347/8347645.md)
