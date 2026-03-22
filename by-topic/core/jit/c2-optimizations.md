# C2 优化与 Ideal Graph 深入

> Sea of Nodes IR、IGVN、循环优化、Compile::Optimize() 执行顺序

[← 返回 JIT 编译概览](README.md)

---

## 目录

1. [C2 编译流程概览](#1-c2-编译流程概览)
2. [Compile::Optimize() 实际执行顺序](#2-compileoptimize-实际执行顺序)
3. [Sea of Nodes IR](#3-sea-of-nodes-ir)
4. [主要节点类型](#4-主要节点类型)
5. [IGVN (Iterative Global Value Numbering)](#5-igvn-iterative-global-value-numbering)
6. [循环优化 (PhaseIdealLoop)](#6-循环优化-phaseidealloop)

---

## 1. C2 编译流程概览

```
字节码
   │
   ▼
Parse Phase ────────► 解析字节码 → Ideal Graph
   │                      内联优化 (inlining)
   ▼                      初始 GVN (全局值编号, Global Value Numbering)
PhaseIterGVN ◄────────── 全局值编号
   │                      常量折叠 (constant folding)
   ▼                      公共子表达式消除 (CSE)
PhaseIdealLoop ────────► 循环优化 (多轮迭代)
   │                      Peeling/Unswitching/Unrolling
   ▼
PhaseCCP ───────────────► 条件常量传播 (Conditional Constant Propagation)
   │                      死代码消除 (dead code elimination)
   ▼
PhaseEscapeAnalysis ───► 逃逸分析 (escape analysis)
   │                      标量替换 (scalar replacement)
   ▼                      栈上分配
PhaseMacroExpand ──────► 宏扩展 (macro expansion)
   │                      锁优化 (lock elimination)
   ▼
PhaseSuperWord ────────► SIMD 向量化 (auto-vectorization)
   │
   ▼
代码生成 ───────────────► 寄存器分配 (register allocation) → 机器码
```

---

## 2. Compile::Optimize() 实际执行顺序

以下为 `Compile::Optimize()` 方法的实际调用顺序 (源码: `src/hotspot/share/opto/compile.cpp`):

```
1.  PhaseIterGVN              ← 第 1 轮 IGVN (全局值编号)
2.  inline_incrementally       ← 增量内联 (分批内联 + IGVN)
3.  inline_boxing_calls        ← 自动装箱内联 (valueOf() 等)
4.  remove_speculative_types   ← 移除推测类型
5.  cleanup_expensive_nodes    ← 清理高开销节点
6.  PhaseVector                ← 向量 box 优化 (如有)
7.  PhaseRenumberLive          ← 重新编号存活节点 (如需)
8.  ConnectionGraph::do_analysis ← 逃逸分析 (可迭代多轮)
9.  PhaseMacroExpand::eliminate  ← 标量替换/锁消除
10. PhaseIdealLoop (1-3 轮)    ← 循环优化 (范围检查消除/展开/剥离)
11. PhaseCCP                   ← 条件常量传播
12. PhaseIterGVN               ← 第 2 轮 IGVN (CCP 后清理)
13. PhaseIdealLoop (后续轮)    ← 更多循环优化
14. process_for_merge_stores   ← MergeStore 优化 (内存写入合并)
15. PhaseMacroExpand::expand   ← 宏节点扩展
16. BarrierExpansion           ← GC 屏障扩展 (barrier expansion)
17. Matcher                    ← Ideal → MachNode 指令选择
18. PhaseCFG                   ← 基本块调度 (basic block scheduling)
19. PhaseChaitin               ← 寄存器分配 (图着色, graph coloring)
20. Output                     ← 生成机器码 (machine code emission)
```

**关键观察:**
- IGVN 运行两次: 第一次在解析后，第二次在 CCP 后
- 逃逸分析 (步骤 8) 在循环优化 (步骤 10) 之前执行
- MergeStore (步骤 14) 是 JDK 25 起独立出来的 pass
- 循环优化可迭代多轮 (步骤 10 + 13)

---

## 3. Sea of Nodes IR

C2 使用 **Sea of Nodes** 中间表示 (Ideal Graph)，这是一种同时表达数据流 (data flow) 和控制流 (control flow) 的图结构。与传统 CFG+SSA 不同，Sea of Nodes 中的节点不严格属于某个基本块——调度 (scheduling) 是后期决定的。

**核心设计:**
- 数据依赖 (data edges): 从使用者指向定义者 (`in(n)`)
- 控制依赖 (control edges): 节点的 `in(0)` 通常指向控制输入
- 没有显式的基本块结构 (直到后期调度)
- 全局优化可以自由移动节点 (node motion)

**与传统 IR 对比:**

| 特性 | 传统 CFG+SSA | Sea of Nodes |
|------|-------------|--------------|
| 基本块 | 显式结构 | 隐式 (后期调度) |
| 节点归属 | 属于特定基本块 | 浮动 (floating) |
| 调度灵活性 | 受限 | 完全自由 |
| 优化便利性 | 需维护 CFG 一致性 | 图变换更直接 |

---

## 4. 主要节点类型

源码中，节点类型定义分布在多个头文件中 (均在 `src/hotspot/share/opto/`):

| 节点类 | 头文件 | 说明 |
|--------|--------|------|
| `Node` | `node.hpp` | 所有节点的基类 (base class) |
| **控制流节点 (Control Flow)** | | |
| `RegionNode` | `cfgnode.hpp` | 控制流合并点 (类似 Phi 的控制流版本) |
| `IfNode` | `cfgnode.hpp` | 条件分支 (产出 IfTrue/IfFalse 两个投影) |
| `GotoNode` | `cfgnode.hpp` | 无条件跳转 |
| `PhiNode` | `cfgnode.hpp` | SSA Phi 函数 (合并不同路径的值) |
| **算术节点 (Arithmetic)** | | |
| `AddNode` / `AddINode` / `AddLNode` | `addnode.hpp` | 加法 (通用/int/long) |
| `SubNode` / `SubINode` | `subnode.hpp` | 减法 |
| `MulNode` / `MulINode` | `mulnode.hpp` | 乘法 |
| `DivNode` | `divnode.hpp` | 除法 |
| **内存节点 (Memory)** | | |
| `LoadNode` | `memnode.hpp` | 内存读取 |
| `StoreNode` | `memnode.hpp` | 内存写入 |
| `MergeMemNode` | `memnode.hpp` | 合并多个内存状态 |
| `MemNode` | `memnode.hpp` | 内存操作基类 |
| **调用节点 (Call)** | | |
| `CallNode` | `callnode.hpp` | 方法调用 |
| `CallStaticJavaNode` | `callnode.hpp` | 静态 Java 调用 |
| `CallDynamicJavaNode` | `callnode.hpp` | 虚调用 (virtual dispatch) |
| **常量节点 (Constant)** | | |
| `ConNode` / `ConINode` / `ConLNode` | `connode.hpp` | 常量值 |
| **类型转换 (Type Conversion)** | | |
| `CastNode` | `castnode.hpp` | 类型转换/断言 |
| `ConvertNode` | `convertnode.hpp` | 数值类型转换 |
| **锁节点 (Lock)** | | |
| `LockNode` / `UnlockNode` | `locknode.hpp` | 锁操作 (可被逃逸分析消除) |

### 节点的核心方法

每个节点类都可以定义自己的优化规则:

| 方法 | 作用 | 返回值 |
|------|------|--------|
| `Ideal()` | 图变换 (graph transformation) | 返回替代节点，或 `nullptr` 表示无变换 |
| `Value()` | 类型推断 (type inference) | 计算节点输出的类型 |
| `Identity()` | 消除冗余 (redundancy elimination) | 返回等价的已有节点 |

---

## 5. IGVN (Iterative Global Value Numbering)

IGVN 是 C2 最核心的优化框架，实现在 `phaseX.cpp` 中。它通过迭代地对图中的节点应用 `Ideal()` 变换来优化代码。

### 工作原理

```
1. 维护一个 worklist (待处理节点集合)
2. 从 worklist 取出节点，调用其 Ideal() 方法尝试变换
3. 如果节点被变换，将受影响的邻居节点加入 worklist
4. 重复直到 worklist 为空 (达到不动点, fixed point)
```

### IGVN 执行的典型优化

| 优化 | 示例 | 说明 |
|------|------|------|
| **常量折叠** (constant folding) | `3 + 5` → `8` | 编译时计算常量表达式 |
| **代数简化** (algebraic simplification) | `x + 0` → `x`, `x * 1` → `x` | 利用代数恒等式 |
| **公共子表达式消除** (CSE) | 相同计算只做一次 | 消除重复计算 |
| **死代码消除** (dead code elimination) | 移除无用节点 | 减少代码体积 |
| **强度削减** (strength reduction) | `x * 2` → `x << 1` | 用低成本操作替代 |

### IGVN 与其他 Phase 的交互

IGVN 在 `Compile::Optimize()` 中运行两次:
1. **第 1 轮** (步骤 1): 在解析和初始内联后，进行第一遍全局优化
2. **第 2 轮** (步骤 12): 在 CCP (条件常量传播) 后，CCP 可能暴露新的常量和死代码，IGVN 进一步清理

---

## 6. 循环优化 (PhaseIdealLoop)

循环优化是 C2 中最复杂的优化阶段之一，实现分布在多个文件中:

### 源码文件分布

| 文件 | 优化技术 |
|------|----------|
| `loopopts.cpp` | 循环不变量外提 (LICM, Loop Invariant Code Motion)、split-if |
| `loopTransform.cpp` | 循环展开 (unrolling)、循环剥离 (peeling) |
| `loopUnswitch.cpp` | 循环分支外提 (unswitching) |
| `loopPredicate.cpp` | 循环谓词 (predication) |
| `superword.cpp` | 向量化 (在循环优化之后) |

### 主要循环变换

| 变换 | 说明 | 典型收益 |
|------|------|----------|
| **循环展开 (Unrolling)** | 复制循环体多次，减少分支开销 | 减少循环控制开销，暴露更多优化机会 |
| **循环剥离 (Peeling)** | 提取第一/最后几次迭代 | 消除首次迭代的特殊检查 |
| **循环不变量外提 (LICM)** | 将不依赖循环变量的计算移出循环 | 减少重复计算 |
| **循环分支外提 (Unswitching)** | 将循环内条件判断移到循环外 | 消除循环内分支 |
| **范围检查消除 (RCE)** | 证明数组访问总在范围内，消除边界检查 | 减少运行时检查 |
| **循环谓词 (Predication)** | 在循环前插入一次性检查 | 将循环内检查提前到循环外 |

### 循环优化的迭代

PhaseIdealLoop 在 `Compile::Optimize()` 中可以运行多轮:
- **步骤 10** (1-3 轮): 范围检查消除、循环展开、循环剥离
- **步骤 13** (后续轮): 进一步的循环变换

多轮迭代的原因: 一轮循环优化可能暴露出新的优化机会 (例如展开后的循环体可以进一步做 LICM)。

### 相关参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `LoopUnrollLimit` | 60 | 循环展开的最大展开因子 |
| `LoopMaxUnroll` | 16 | 单次展开的最大倍数 |
| `LoopUnswitching` | true | 是否启用循环分支外提 |

---

## 相关文档

- [C2 优化阶段](c2-phases.md) - 15 个编译阶段详解
- [逃逸分析深入](escape-analysis.md) - 标量替换、锁消除
- [内联优化深入](inlining.md) - 内联决策、CHA、多态内联
- [SuperWord 向量化](superword.md) - 自动 SIMD 优化
- [MergeStore 优化](mergestore.md) - 内存写入合并
- [IGV 实战教程](igv-tutorial.md) - Ideal Graph Visualizer 使用指南

---

**最后更新**: 2026-03-22
