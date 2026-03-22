# JIT 编译

> C1、C2、分层编译、Graal 演进历程

[← 返回核心平台](../)

---
## 目录

1. [快速概览](#1-快速概览)
2. [编译器对比](#2-编译器对比)
3. [核心贡献者](#3-核心贡献者)
4. [文档导航](#4-文档导航)
5. [快速参考](#5-快速参考)
6. [内部结构](#6-内部结构)
7. [C2 编译流程概览](#7-c2-编译流程概览)
8. [C1 编译流程概览](#8-c1-编译流程概览)
9. [C2 优化技术摘要](#9-c2-优化技术摘要)
10. [JIT 编译与虚拟线程](#10-jit-编译与虚拟线程)
11. [AOT 编译与 Graal 摘要](#11-aot-编译与-graal-摘要)
12. [诊断工具](#12-诊断工具)
13. [重要 PR 分析](#13-重要-pr-分析)
14. [JIT 内联优化最佳实践](#14-jit-内联优化最佳实践)
15. [相关链接](#15-相关链接)

---


## 1. 快速概览

```
JDK 1.0 ── JDK 1.3 ── JDK 7 ── JDK 9 ── JDK 10 ── JDK 17 ── JDK 21 ── JDK 26
   │         │        │        │        │        │        │        │
解释器    C1/C2   分层    JVMCI  Graal   JIT    虚拟线程  SuperWord
纯解释   引入    编译     接口    JIT     优化     支持    成本模型
                  Tiered                  性能
```

### 核心演进

| 版本 | 特性 | 说明 | 深度分析 |
|------|------|------|----------|
| **JDK 1.0** | 解释器 | 纯解释执行 | - |
| **JDK 1.3** | C1 (Client Compiler) | 快速启动编译器 | [C1 编译器详解](c1-compiler.md) |
| **JDK 1.3** | C2 (Server Compiler) | 高性能编译器 | [C2 优化阶段](c2-phases.md) |
| **JDK 5** | C1/C2 分离 | -client/-server | [编译器对比](#编译器对比) |
| **JDK 6** | 分层编译 (实验), JDK 8 默认启用 | C1 + C2 组合 | [分层编译详解](tiered-compilation.md) |
| **JDK 9** | JVMCI (JEP 243) | JVM 编译器接口 | [Graal JIT](graal-jit.md) |
| **JDK 10** | Graal JIT (JEP 317) | 实验性高性能 JIT | [Graal JIT](graal-jit.md) |
| **JDK 17** | JIT 优化 | 编译器改进 | [近期改进](recent-changes.md) |
| **JDK 21** | String Templates, Record Patterns | 模式匹配优化 | [近期改进](recent-changes.md) |
| **JDK 23** | JIT 性能 | 编译吞吐量提升 | [近期改进](recent-changes.md) |
| **JDK 25** | AOT Method Profiling, C2 常量折叠修复 | JEP 515 AOT 方法 Profiling (启动加速 15-25%), 表达式优化回归修复, MergeStores 独立 pass, String::hashCode 常量折叠 | [近期改进](recent-changes.md) |
| **JDK 26** | C2 扩展编译, Lazy Constants | 支持大参数方法编译, Lazy Constants (Second Preview, JIT 常量折叠), 自动向量化扩展 | [SuperWord 向量化](superword.md) |

---

## 2. 编译器对比

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
| **内联** (inlining) | 保守内联 | 激进内联 |
| **常量折叠** (constant folding) | 局部 | 全局 |
| **死代码消除** (dead code elimination) | 基本 | 激进 |
| **循环优化** (loop optimization) | 基础 (null check 消除/循环不变量外提) | 完整 (展开/剥离/外提) |
| **逃逸分析** (escape analysis) | 无 | 有 |
| **标量替换** (scalar replacement) | 无 | 有 |
| **向量化** (vectorization) | 无 | SuperWord SIMD |
| **寄存器分配** (register allocation) | 线性扫描 | 图着色算法 |
| **全局值编号** (GVN) | 无 | 有 |

### 内联策略对比

| 方面 | C1 | C2 |
|------|----|----|
| **内联阈值** | ~35 字节码 (MaxInlineSize) | ~35 字节码 (冷方法) / ~325 字节码 (热方法, FreqInlineSize) |
| **最大内联深度** | 9 层 (C1MaxInlineLevel=9) | 15 层 (MaxInlineLevel=15, JDK 14 起从 9 提升) |
| **虚方法内联** | 保守 (需类型统计) | 激进 (基于 profiling) |
| **内联失败** | 放弃 | 记录供后续优化 |

> 内联策略详解: [内联优化深入](inlining.md) — CHA、多态内联缓存 (Polymorphic Inline Cache)、内联决策流程

### 使用场景

| 场景 | 推荐编译器 | 原因 |
|------|------------|------|
| **GUI 应用** | C1 | 快速响应用户操作 |
| **批处理任务** | C2 | 长时间运行，最大化吞吐量 |
| **微服务** | C1 + C2 (分层) | 快速启动 + 高性能 |
| **大数据处理** | C2 | 计算密集型 |

### 分层编译 (Tiered Compilation)

```
Level 0: 解释执行 (Interpreter)
Level 1: C1 (编译，无 profiling)
Level 2: C1 (有限 profiling)
Level 3: C1 (完全 profiling)
Level 4: C2 (深度优化)
```

**各层级详细说明:**

| 层级 | 编译器 | Profiling | 说明 |
|------|--------|-----------|------|
| **Tier 0** | 解释器 | 基本计数 | 解释执行，收集方法调用次数和回边计数 |
| **Tier 1** | C1 | 无 | C1 编译但不插入 profiling 代码；用于已知不需要进一步优化的方法 (如 trivial 方法) |
| **Tier 2** | C1 | 有限 | C1 编译 + 调用计数和回边计数；较少使用，主要在 C2 队列积压时作为过渡 |
| **Tier 3** | C1 | 完全 | C1 编译 + 完整 profiling (MethodDataObject)：分支概率、类型统计、调用目标等；这是最常见的 C1 编译层级 |
| **Tier 4** | C2 | 使用已收集数据 | C2 利用 Tier 3 收集的 profiling 数据做深度优化；不再插入 profiling 代码 |

**编译阈值 (源码实际默认值):**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `Tier3InvocationThreshold` | 200 | 方法调用次数达到此值触发 Tier 3 编译 |
| `Tier3MinInvocationThreshold` | 100 | Tier 3 最低调用次数门槛 |
| `Tier3CompileThreshold` | 2000 | Tier 3 综合阈值 (调用次数 + 回边次数) |
| `Tier3BackEdgeThreshold` | 60000 | Tier 3 回边次数触发 OSR 编译 |
| `Tier4InvocationThreshold` | 5000 | 方法调用次数达到此值触发 Tier 4 编译 |
| `Tier4MinInvocationThreshold` | 600 | Tier 4 最低调用次数门槛 |
| `Tier4CompileThreshold` | 15000 | Tier 4 综合阈值 (调用次数 + 回边次数) |
| `Tier4BackEdgeThreshold` | 40000 | Tier 4 回边次数触发 OSR 编译 |

> 数据来源: `src/hotspot/share/compiler/compiler_globals.hpp`

**编译决策公式** (简化描述，源码在 `compilationPolicy.cpp`):
- Tier 3 触发: `invocations >= Tier3InvocationThreshold` 或 `(invocations >= Tier3MinInvocationThreshold && invocations + back_edges >= Tier3CompileThreshold)`
- Tier 4 触发: `invocations >= Tier4InvocationThreshold` 或 `(invocations >= Tier4MinInvocationThreshold && invocations + back_edges >= Tier4CompileThreshold)`

**典型编译路径:**

```
常规方法:   Tier 0 → Tier 3 → Tier 4
简单方法:   Tier 0 → Tier 1 (不再升级)
C2 队列满:  Tier 0 → Tier 2 → Tier 3 → Tier 4
OSR 编译:   Tier 0 (循环中) → Tier 3 OSR → Tier 4 OSR
```

---

## 3. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### JIT 编译器 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | 72 | Oracle | HotSpot 运行时 (涉及编译器源文件) † |
| 2 | [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | 68 | Amazon | JIT 编译器 |
| 3 | [Ioi Lam](/by-contributor/profiles/ioi-lam.md) | 62 | Oracle | CDS/AOT (涉及编译器源文件) † |
| 4 | Stefan Karlsson | 31 | Oracle | GC/运行时 (涉及编译器源文件) † |
| 5 | [Doug Simon](/by-contributor/profiles/doug-simon.md) | 29 | Oracle | JVMCI/Graal JIT |
| 6 | [David Holmes](/by-contributor/profiles/david-holmes.md) | 24 | Oracle | HotSpot 运行时/并发 (涉及编译器源文件) † |
| 7 | [Claes Redestad](/by-contributor/profiles/claes-redestad.md) | 24 | Oracle | 启动性能/编译器优化 |
| 8 | [Thomas Stuefe](/by-contributor/profiles/thomas-stuefe.md) | 22 | Red Hat | Metaspace/运行时 (涉及编译器源文件) † |
| 9 | [Vladimir Kozlov](/by-contributor/profiles/vladimir-kozlov.md) | 20 | Oracle | C2 架构师, JIT 编译器 |
| 10 | [Igor Veresov](/by-contributor/profiles/igor-veresov.md) | 17 | Oracle | JIT 编译器 |

> † 标注的贡献者主要工作领域并非 JIT 编译器本身，但因跨模块重构、共享代码维护等原因在编译器源文件中有较多提交。

### C2 专项贡献者

| 排名 | 贡献者 | 主要贡献 | 组织 |
|------|--------|----------|------|
| 1 | [Vladimir Kozlov](/by-contributor/profiles/vladimir-kozlov.md) | C2 架构师 | Oracle |
| 2 | [Roland Westrelin](/by-contributor/profiles/rooland-westrelin.md) | C2 优化 (JDK-8325495) | Red Hat |
| 3 | [John Rose](/by-contributor/profiles/john-rose.md) | invokedynamic, JIT | Oracle |
| 4 | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | SuperWord 向量化, C2 博客作者 | Oracle |
| 5 | [Christian Hagedorn](/by-contributor/profiles/christian-hagedorn.md) | C2 优化, GVN | Oracle |
| 6 | [Johannes Graham](/by-contributor/profiles/johannes-graham.md) | C2 常量折叠优化 | Oracle |

---

## 4. 文档导航

| 分类 | 文档 |
|------|------|
| **编译器架构** | [C1 编译器](c1-compiler.md) &#124; [C2 优化阶段](c2-phases.md) &#124; [C2 优化与 Ideal Graph 深入](c2-optimizations.md) &#124; [Ideal Graph 详解](ideal-graph.md) |
| **编译策略** | [分层编译](tiered-compilation.md) &#124; [Graal JIT](graal-jit.md) &#124; [Graal vs C2 性能](graal-vs-c2-performance.md) &#124; [GraalVM 独有技术](graal-unique-features.md) |
| **优化技术** | [内联优化](inlining.md) &#124; [逃逸分析](escape-analysis.md) &#124; [循环优化](loop-optimizations.md) &#124; [SuperWord 向量化](superword.md) &#124; [MergeStore](mergestore.md) &#124; [寄存器分配](register-allocation.md) |
| **AOT / Graal** | [AOT 编译演进](aot-evolution.md) (JEP 295 → Leyden) &#124; [Graal 高级优化](graal-advanced-optimizations.md) |
| **调试诊断** | [诊断工具](diagnostics.md) &#124; [IGV 教程](igv-tutorial.md) &#124; [去优化](deoptimization.md) &#124; [汇编输出](assembly-output.md) |
| **实战指南** | [JIT 友好代码](best-practices.md) &#124; [JIT 与 GC 协作](jit-gc-collaboration.md) &#124; [编译阈值](compilation-thresholds.md) &#124; [代码缓存](code-cache.md) |
| **配置/历史** | [VM 参数](vm-parameters.md) &#124; [版本时间线](timeline.md) &#124; [近期改进](recent-changes.md) &#124; [C2 活跃度](c2-activity-timeline.md) |

> 另见 [GraalVM 技术内幕专题](../graalvm/) 目录。

---

## 5. 快速参考

### 常用 VM 参数

```bash
# 启用分层编译 (默认)
-XX:+TieredCompilation

# 调整编译阈值
-XX:CompileThreshold=10000         # C2 阈值
-XX:FreqInlineSize=325             # 热方法内联阈值 (仅频繁执行的方法)
-XX:MaxInlineSize=35               # 冷方法内联阈值 (不论调用频率)

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

## 6. 内部结构

### HotSpot 编译器源码概要

```
src/hotspot/share/
├── compiler/     # 编译调度: compileBroker.cpp, compilationPolicy.cpp
├── c1/           # C1: GraphBuilder → Optimizer → LinearScan → LIRAssembler
├── opto/         # C2: Parse → IGVN → IdealLoop → CCP → Escape → Matcher → Chaitin
└── jvmci/        # JVMCI (Graal 接口)
```

### C1 vs C2 源码结构对比

| 组件 | C1 | C2 |
|------|----|----|
| **IR 构建** | `c1_GraphBuilder.cpp` | `parse1.cpp`, `parse2.cpp` |
| **优化器** | `c1_Optimizer.cpp` | `compile.cpp::Optimize()` |
| **值编号** | `c1_ValueMap.cpp` (局部) | `phaseX.cpp`, `gvn.cpp` (全局) |
| **寄存器分配** | `c1_LinearScan.cpp` (线性扫描) | `chaitin.cpp` (图着色) |
| **逃逸分析** | 无 | `escape.cpp` |
| **向量化** | 无 | `superword.cpp` |

> 完整源码文件清单: [C2 优化与 Ideal Graph 深入](c2-optimizations.md) | [C1 编译器详解](c1-compiler.md)

---

## 7. C2 编译流程概览

```
字节码 → Parse (Ideal Graph + 内联 + 初始 GVN)
       → PhaseIterGVN (全局值编号/常量折叠/CSE)
       → PhaseIdealLoop (循环展开/剥离/外提, 多轮)
       → PhaseCCP (条件常量传播/死代码消除)
       → EscapeAnalysis (逃逸分析/标量替换)
       → MacroExpand (锁消除/宏扩展)
       → SuperWord (SIMD 向量化)
       → Matcher → PhaseCFG → Chaitin → Output (机器码)
```

> 完整 20 步执行顺序、Sea of Nodes IR、IGVN 工作原理、节点类型: [C2 优化与 Ideal Graph 深入](c2-optimizations.md)

---

## 8. C1 编译流程概览

```
字节码 → GraphBuilder (HIR) → Canonicalizer → ValueNumbering
       → NullCheckEliminator → RangeCheckEliminator
       → LIRGenerator (LIR) → LinearScan → LIRAssembler (机器码)
```

| 对比维度 | C1 | C2 |
|----------|----|----|
| **IR 类型** | HIR + LIR | Ideal Graph + MachNodes |
| **IR 构建** | GraphBuilder (单遍) | Parse (多遍，内联) |
| **优化深度** | Optimizer (基础, ~7 阶段) | 多个 Phase (激进, 20+ 阶段) |
| **寄存器分配** | LinearScan (快速) | Chaitin (图着色) |
| **设计原则** | 快速编译 > 代码质量 | 深度优化 > 编译速度 |

> 完整 C1 编译管线详解: [C1 编译器详解](c1-compiler.md)

---

## 9. C2 优化技术摘要

以下是 C2 三大核心优化技术的摘要，详细内容请参见各专题文件。

### Ideal Graph 与 IGVN

C2 使用 **Sea of Nodes** 中间表示 (Ideal Graph)，同时表达数据流和控制流。IGVN (Iterative Global Value Numbering) 是其核心优化框架，通过 worklist 驱动的迭代变换达到不动点 (fixed point)。典型优化包括常量折叠、代数简化、公共子表达式消除、死代码消除、强度削减。

> 完整内容: [C2 优化与 Ideal Graph 深入](c2-optimizations.md) — 节点类型、IGVN 工作原理、循环优化、Optimize() 20 步执行顺序

### 逃逸分析

C2 使用 Connection Graph 算法将对象分为三种逃逸状态: `NoEscape` (可标量替换/锁消除)、`ArgEscape` (部分锁消除)、`GlobalEscape` (无优化)。标量替换将 `NoEscape` 对象的字段拆解为独立变量，完全消除堆分配。

> 完整内容: [逃逸分析深入](escape-analysis.md) — 标量替换限制、锁消除条件、迭代分析、编程建议

### 内联优化

C2 的内联基于字节码大小阈值 (`MaxInlineSize`=35 / `FreqInlineSize`~325)、内联深度 (`MaxInlineLevel`=15)、以及 profiling 数据。多态内联通过 CHA (Class Hierarchy Analysis) 和 inline cache (单态/多态/超多态) 实现。内联是后续优化 (逃逸分析、常量折叠等) 的前提。

> 完整内容: [内联优化深入](inlining.md) — 内联决策流程、CHA、多态内联缓存、内联友好设计模式

---

## 10. JIT 编译与虚拟线程

JDK 21 虚拟线程 (Virtual Threads) 基于 Continuation 实现，挂起时冻结栈帧到堆 (freeze)，恢复时解冻 (thaw)。

**对 JIT 的影响:**
- 编译代码的 OopMap 必须在 yield 点处准确，栈帧布局需与 Continuation 兼容
- JIT 可照常进行大部分优化 (内联、逃逸分析等)，热路径性能与平台线程一致
- `Continuation.yield` / `Continuation.run` 是 intrinsic 方法，JIT 有特殊处理
- 性能开销主要在 freeze/thaw 操作本身 (栈帧拷贝)

---

## 11. AOT 编译与 Graal 摘要

Java AOT 编译经历三个阶段: JEP 295 jaotc (JDK 9, 已移除) → GraalVM Native Image (外部项目, 闭合世界) → Project Leyden (JDK 24+, 渐进式 AOT)。

**Project Leyden 核心 JEP:**
- **JEP 483**: AOT 类加载和链接缓存
- **JEP 514**: AOT 代码缓存
- **JEP 515**: AOT 方法 Profiling (启动加速 15-25%)
- **JEP 516**: AOT 编译 (预览)

Graal JIT 通过 JVMCI (JEP 243) 接入 JVM，在 JDK 10 作为实验特性加入 OpenJDK，JDK 17 移除 (JEP 410)，现在 GraalVM 项目中独立发展。

> 完整内容: [AOT 编译演进](aot-evolution.md) — JEP 295 历史、GraalVM Native Image、Leyden 使用方式、Graal 编译器简史

---

## 12. 诊断工具

### 编译日志

```bash
-XX:+PrintCompilation             # 编译事件 (时间/编译ID/层级/方法名/大小)
-XX:+UnlockDiagnosticVMOptions -XX:+PrintInlining  # 内联决策树
-XX:+CITime                       # 编译时间统计
-XX:+TraceDeoptimization           # 去优化信息
```

**PrintCompilation 常见标记:** `%`=OSR, `s`=同步, `!`=异常处理, `made not entrant`=去优化

**PrintInlining 常见失败原因:** `too big` (超过 FreqInlineSize/MaxInlineSize), `too deep` (超过 MaxInlineLevel), `no static binding`

### JFR 编译事件

| 事件 | 说明 |
|------|------|
| `jdk.Compilation` | 编译完成 (方法名、时长、层级、代码大小) |
| `jdk.CompilerInlining` | 内联决策 (成功/失败及原因) |
| `jdk.Deoptimization` | 去优化 (原因、方法) |
| `jdk.CompilerPhase` | 编译阶段耗时 |

> 详细教程: [IGV 实战教程](igv-tutorial.md) | [诊断工具](diagnostics.md) | [汇编输出分析](assembly-output.md) | [去优化详解](deoptimization.md)

---

## 13. 重要 PR 分析

### SuperWord 向量化优化系列

> **主要贡献者**: [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | **详见**: [SuperWord 向量化](superword.md)

| PR | 说明 | 影响 |
|----|------|------|
| JDK-8340093 | SuperWord 成本模型 (向量宽度/迭代次数/内存模式) | 智能向量化决策 |
| JDK-8334431 | 修复 Store-to-Load 转发回归 ([分析](/by-pr/8333/8334431.md)) | 性能回归修复 |
| JDK-8324890 | VLoop 分析器重构 ([分析](/by-pr/8324/8324890.md)) | 架构改进 |

### MergeStore 优化系列

> **完整专题**: [MergeStore 优化](mergestore.md)

#### JDK-8333893: StringBuilder append(boolean/null) 优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | **效果**: append(boolean) +14.7%, append(null) +9.2%

→ [详细分析](/by-pr/8333/8333893.md)

### JDK-8365186: Reduce size of DateTimePrintContext::adjust

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | **影响**: +3-12% 日期格式化性能提升

将 382 字节方法拆分为三个方法 (27 + 123 + 232 字节)，使热路径可被 C2 内联。

→ [详细分析](/by-pr/8365/8365186.md)

### JDK-8349400: 消除嵌套类优化启动

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | **影响**: 启动类加载数量 -90%

→ [详细分析](/by-pr/8349/8349400.md)

### JDK-8355177: StringBuilder::append(char[]) 加速

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | **影响**: +15% 性能提升

→ [详细分析](/by-pr/8355/8355177.md)

### JDK-8341906: ClassFile 写入 BufBuffer 优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | **影响**: +28% 字节码写入性能提升

→ [详细分析](/by-pr/8341/8341906.md)

---

## 14. JIT 内联优化最佳实践

### 方法大小控制

| 方法类型 | 推荐大小 | 说明 |
|----------|----------|------|
| **热路径方法** (hot path) | < 50 字节 | 确保 C1/C2 都能内联 |
| **常规方法** | < 200 字节 | C2 可内联 |
| **复杂方法** | 拆分为多个方法 | 冷热分离 (hot/cold splitting) |

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
2. **早期返回** (early return) - 常见情况优先处理
3. **避免大 switch** - 使用策略模式
4. **静态方法** (static method) - 比虚方法更容易内联
5. **final 方法** - 消除多态调用

> 更多内联技巧: [内联优化深入](inlining.md) | [JIT 友好代码模式](best-practices.md)

---

## 15. 相关链接

### 相关主题

- [性能优化](../performance/) | [GC 演进](../gc/) | [JVM 调优](../jvm/)

### 外部参考

- [Emanuel's HotSpot C2 Blog](https://eme64.github.io/blog/) - C2 编译器深入解析 ([Part 1: Overview](https://eme64.github.io/blog/2024/12/06/Intro-to-C2-Part01.html), [Part 2: GVN](https://eme64.github.io/blog/2024/12/24/Intro-to-C2-Part02.html), [Part 3: Inlining](https://eme64.github.io/blog/2024/12/31/Intro-to-C2-Part03.html), [Part 4: Loop Optimizations](https://eme64.github.io/blog/2025/01/23/Intro-to-C2-Part04.html))

---

**最后更新**: 2026-03-22
