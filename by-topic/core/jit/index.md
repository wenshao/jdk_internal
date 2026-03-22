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
9. [C2 Ideal Graph 深入](#9-c2-ideal-graph-深入)
10. [逃逸分析深入](#10-逃逸分析深入)
11. [内联优化深入](#11-内联优化深入)
12. [JIT 编译与虚拟线程](#12-jit-编译与虚拟线程)
13. [AOT 编译演进](#13-aot-编译演进)
14. [Graal 编译器简史](#14-graal-编译器简史)
15. [诊断工具](#15-诊断工具)
16. [重要 PR 分析](#16-重要-pr-分析)
17. [JIT 内联优化最佳实践](#17-jit-内联优化最佳实践)
18. [相关链接](#18-相关链接)

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
| **内联** | ✅ 保守内联 | ✅ 激进内联 |
| **常量折叠** | ✅ 局部 | ✅ 全局 |
| **死代码消除** | ✅ 基本 | ✅ 激进 |
| **循环优化** | ⚠️ 基础 (null check 消除/循环不变量外提) | ✅ 完整 (展开/剥离/外提) |
| **逃逸分析** | ❌ 无 | ✅ 有 |
| **标量替换** | ❌ 无 | ✅ 有 |
| **向量化** | ❌ 无 | ✅ SuperWord SIMD |
| **寄存器分配** | 线性扫描 | 图着色算法 |
| **全局值编号** | ❌ 无 | ✅ 有 |

### 内联策略对比

| 方面 | C1 | C2 |
|------|----|----|
| **内联阈值** | ~35 字节码 (MaxInlineSize) | ~35 字节码 (冷方法) / ~325 字节码 (热方法, FreqInlineSize) |
| **最大内联深度** | 9 层 (C1MaxInlineLevel=9, 独立参数) | 15 层 (MaxInlineLevel=15, JDK 14 起从 9 提升) |
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
- [Graal vs C2 性能对比](graal-vs-c2-performance.md) - 2024-2025 最新基准测试
  - 各场景性能数据
  - 启动/稳态性能对比
  - 实际应用建议
- [Graal 高级优化特性](graal-advanced-optimizations.md) - 类似 MergeStore 的优化对比
  - 部分转义分析
  - 数组消除优化
  - 死存储消除对比
- [GraalVM 独有技术](graal-unique-features.md) - C2没有而GraalVM有的完整清单
  - 帧状态分离
  - 推测性优化
  - LoopPredication
  - 虚拟对象材料化

> 💡 **提示**: 还有 [GraalVM 技术内幕专题](../graalvm/) 目录，包含更全面的 GraalVM 技术文档，包括架构、性能、Native Image 等。

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
- [IGV 实战教程](igv-tutorial.md) - Ideal Graph Visualizer 使用指南
  - 安装和配置
  - 导出和查看编译图
  - 分析优化阶段
  - 实战案例
- [去优化详解](deoptimization.md) - JIT 代码回退机制
  - 去优化的触发条件和类型
  - 如何查看和分析去优化
  - 避免频繁去优化的技巧
- [汇编输出分析](assembly-output.md) - 查看和分析 JIT 生成的机器码
  - hsdis 插件安装
  - 汇编指令解读
  - 优化模式识别
  - 实战案例分析

### 实战指南

- [JIT 友好代码模式](best-practices.md) - 编写高性能代码的最佳实践
  - 方法内联友好设计
  - 循环优化技巧
  - 避免对象逃逸
  - 常见陷阱与案例
- [JIT 与 GC 协作](jit-gc-collaboration.md) - 编译器与垃圾收集器的协作机制
  - 逃逸分析如何减少 GC 压力
  - Safepoint 插入策略
  - Barrier 优化
  - 标量替换效果
- [编译阈值机制](compilation-thresholds.md) - 为什么方法要执行 10000 次才编译
  - 各层级阈值详解
  - 分层编译切换条件
  - 阈值调优建议
- [代码缓存管理](code-cache.md) - JIT 代码存储机制
  - 代码缓存结构
  - 缓存满时的行为
  - 监控和调优

### 历史演进

- [版本时间线](timeline.md) - JDK 1.0 到 JDK 26
- [近期改进](recent-changes.md) - 2024-2026 更新
  - **JDK 25**: JEP 515 AOT 方法 Profiling (训练运行的 profile 数据缓存, 启动加速 15-25%); 修复 `(a | 3) | 6` 常量折叠回归 (特定场景 10,000x 提升); MergeStores 优化拆分为独立 pass (解决与 range check smearing 冲突); `String::hashCode` 可常量折叠 (常量键 Map 查找约 8x 提升); 无限循环块频率计算修复
  - **JDK 26**: C2 支持编译大参数方法 (此前回退至 C1/解释器); Lazy Constants (Second Preview, JIT 可对延迟初始化值做常量折叠); 更快 JVM 启动; 扩展 C2 编译覆盖范围; 自动向量化模式扩展
- [C2 迭代速度分析](c2-pace-analysis.md) - C2是否"迭代慢"？事实核查
- [C2 活跃度时间线](c2-activity-timeline.md) - 按月度展示PR、新功能、活跃度
- [分层编译历史](tiered-compilation.md#分层编译的历史) - JDK 6 引入
- [Graal JIT 演进](graal-jit.md#近期发展) - JDK 9+ 支持

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

### HotSpot 编译器源码

```
src/hotspot/share/
├── compiler/
│   ├── compileBroker.cpp          # 编译任务调度
│   ├── compilationPolicy.cpp      # 分层编译决策 (阈值判断)
│   ├── compilation.cpp            # 编译策略
│   └── compilerOracle.cpp         # 编译规则
├── c1/                            # C1 (Client Compiler)
│   ├── c1_Compilation.cpp         # C1 编译入口
│   ├── c1_GraphBuilder.cpp        # HIR 构建
│   ├── c1_IR.cpp                  # HIR 中间表示
│   ├── c1_Instruction.cpp         # HIR 指令节点定义
│   ├── c1_Optimizer.cpp           # C1 优化器 (null check/CE 消除)
│   ├── c1_LinearScan.cpp          # 寄存器分配 (线性扫描)
│   ├── c1_LIRGenerator.cpp        # HIR → LIR 转换
│   ├── c1_LIRAssembler.cpp        # LIR → 机器码
│   ├── c1_Canonicalizer.cpp       # 规范化
│   ├── c1_ValueMap.cpp            # 值编号
│   └── c1_RangeCheckElimination.cpp # 范围检查消除
├── opto/                          # C2 (Server Compiler)
│   ├── compile.cpp                # C2 编译入口, Optimize()
│   ├── parse1.cpp / parse2.cpp    # 字节码 → Ideal Graph
│   ├── gvn.cpp / phaseX.cpp       # Global Value Numbering (IGVN)
│   ├── loopopts.cpp               # 循环优化
│   ├── loopTransform.cpp          # 循环变换 (展开/剥离)
│   ├── loopUnswitch.cpp           # 循环分支外提
│   ├── escape.cpp                 # 逃逸分析 (ConnectionGraph)
│   ├── superword.cpp              # SuperWord 向量化
│   ├── vtransform.cpp             # VTransform 架构 (JDK 26+)
│   ├── macro.cpp                  # 宏扩展 (锁/分配消除)
│   ├── matcher.cpp                # Ideal → MachNode 指令选择
│   ├── chaitin.cpp                # 寄存器分配 (图着色)
│   ├── cfgnode.cpp                # 控制流节点 (RegionNode, IfNode, PhiNode)
│   ├── addnode.cpp                # 算术加法节点
│   ├── subnode.cpp                # 算术减法节点
│   ├── mulnode.cpp                # 算术乘法节点
│   ├── memnode.cpp                # 内存操作节点 (Load, Store, MergeMem)
│   ├── callnode.cpp               # 方法调用节点
│   ├── idealGraphPrinter.cpp      # IGV 输出支持
│   └── output.cpp                 # 代码生成
└── jvmci/                         # JVMCI (Graal 接口)
```

### C1 vs C2 源码结构对比

| 组件 | C1 | C2 |
|------|----|----|
| **IR 构建** | `c1_GraphBuilder.cpp` | `parse1.cpp`, `parse2.cpp` (在 opto/) |
| **优化器** | `c1_Optimizer.cpp` | `compile.cpp::Optimize()` |
| **值编号** | `c1_ValueMap.cpp` | `phaseX.cpp`, `gvn.cpp` (全局值编号) |
| **寄存器分配** | `c1_LinearScan.cpp` (线性扫描) | `chaitin.cpp` (图着色) |
| **代码生成** | `c1_LIRAssembler.cpp` | `output.cpp` |
| **循环优化** | ⚠️ 基础 (`c1_Optimizer.cpp`) | `loopopts.cpp`, `loopTransform.cpp` (完整) |
| **逃逸分析** | ❌ 无 | `escape.cpp` |
| **向量化** | ❌ 无 | `superword.cpp` |

---

## 7. C2 编译流程概览

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

### C2 Optimize() 实际执行顺序

以下为 `Compile::Optimize()` 方法的实际调用顺序 (源码: `src/hotspot/share/opto/compile.cpp`):

```
1. PhaseIterGVN          ← 第 1 轮 IGVN
2. inline_incrementally   ← 增量内联 (分批内联 + IGVN)
3. inline_boxing_calls    ← 自动装箱内联 (valueOf() 等)
4. remove_speculative_types ← 移除推测类型
5. cleanup_expensive_nodes  ← 清理高开销节点
6. PhaseVector            ← 向量 box 优化 (如有)
7. PhaseRenumberLive      ← 重新编号存活节点 (如需)
8. ConnectionGraph::do_analysis ← 逃逸分析 (可迭代多轮)
9. PhaseMacroExpand::eliminate ← 标量替换/锁消除
10. PhaseIdealLoop (1-3 轮)  ← 循环优化 (范围检查消除/展开/剥离)
11. PhaseCCP               ← 条件常量传播
12. PhaseIterGVN           ← 第 2 轮 IGVN (CCP 后)
13. PhaseIdealLoop (后续轮)  ← 更多循环优化
14. process_for_merge_stores ← MergeStore 优化
15. PhaseMacroExpand::expand ← 宏节点扩展
16. BarrierExpansion       ← GC 屏障扩展
17. Matcher                ← Ideal → MachNode 指令选择
18. PhaseCFG               ← 基本块调度
19. PhaseChaitin           ← 寄存器分配 (图着色)
20. Output                 ← 生成机器码
```

---

## 8. C1 编译流程概览

### C1 编译管线: HIR → LIR → 机器码

```
字节码
   │
   ▼
GraphBuilder ───────► 构建 HIR (High-level IR)
   │                      基于 SSA 形式
   │                      字节码到 HIR 指令映射
   ▼
Canonicalizer ───────► IR 规范化
   │                      简化表达式 (常量折叠)
   │                      规范化运算顺序
   ▼
ValueNumbering ───────► 局部值编号
   │                      消除冗余计算
   ▼
NullCheckEliminator ──► Null 检查消除
   │                      消除冗余 null 检查
   ▼
RangeCheckEliminator ─► 范围检查消除
   │                      (c1_RangeCheckElimination.cpp)
   ▼
LIRGenerator ─────────► HIR → LIR 转换
   │                      平台无关 → 平台相关
   │                      虚拟寄存器分配
   ▼
LinearScan ───────────► 寄存器分配
   │                      线性扫描算法
   │                      溢出处理
   ▼
LIRAssembler ─────────► LIR → 机器码
                          最终代码生成
```

**HIR (High-level IR) 特点:**
- 基于 SSA (Static Single Assignment) 形式
- 每条指令是 `c1_Instruction` 的子类
- 包含类型信息和控制流
- 源码: `c1_IR.cpp`, `c1_Instruction.cpp`

**LIR (Low-level IR) 特点:**
- 平台相关的低级操作
- 使用虚拟寄存器 (Virtual Registers)
- 接近最终机器码的形式
- 源码: `c1_LIR.cpp`, `c1_LIRGenerator.cpp`

**C1 vs C2 编译阶段对比**:

| 阶段 | C1 | C2 |
|------|----|----|
| **IR 类型** | HIR (High-level IR) + LIR | Ideal Graph + MachNodes |
| **IR 构建** | GraphBuilder (单遍) | Parse (多遍，内联) |
| **优化** | Optimizer (基础) | 多个 Phase (激进) |
| **值编号** | ValueNumbering (局部) | GVN (全局) |
| **寄存器分配** | LinearScan (快速) | Chaitin (图着色) |
| **代码生成** | LIR → 机器码 | MachNodes → 机器码 |
| **总阶段数** | ~7 | 20+ |

**C1 设计原则**:
- 快速编译 > 代码质量
- 简单算法 > 复杂优化
- 单遍处理 > 多遍迭代
- 牺牲性能换取编译速度

---

## 9. C2 Ideal Graph 深入

### Sea of Nodes IR

C2 使用 **Sea of Nodes** 中间表示 (Ideal Graph)，这是一种同时表达数据流和控制流的图结构。与传统 CFG+SSA 不同，Sea of Nodes 中的节点不严格属于某个基本块——调度是后期决定的。

**核心设计:**
- 数据依赖 (data edges): 从使用者指向定义者 (`in(n)`)
- 控制依赖 (control edges): 节点的 `in(0)` 通常指向控制输入
- 没有显式的基本块结构 (直到后期调度)
- 全局优化可以自由移动节点

### 主要节点类型

源码中，节点类型定义分布在多个头文件中 (均在 `src/hotspot/share/opto/`):

| 节点类 | 头文件 | 说明 |
|--------|--------|------|
| `Node` | `node.hpp` | 所有节点的基类 |
| **控制流节点** | | |
| `RegionNode` | `cfgnode.hpp` | 控制流合并点 (类似 Phi 的控制流版本) |
| `IfNode` | `cfgnode.hpp` | 条件分支 (产出 IfTrue/IfFalse 两个投影) |
| `GotoNode` | `cfgnode.hpp` | 无条件跳转 |
| `PhiNode` | `cfgnode.hpp` | SSA Phi 函数 (合并不同路径的值) |
| **算术节点** | | |
| `AddNode` / `AddINode` / `AddLNode` | `addnode.hpp` | 加法 (通用/int/long) |
| `SubNode` / `SubINode` | `subnode.hpp` | 减法 |
| `MulNode` / `MulINode` | `mulnode.hpp` | 乘法 |
| `DivNode` | `divnode.hpp` | 除法 |
| **内存节点** | | |
| `LoadNode` | `memnode.hpp` | 内存读取 |
| `StoreNode` | `memnode.hpp` | 内存写入 |
| `MergeMemNode` | `memnode.hpp` | 合并多个内存状态 |
| `MemNode` | `memnode.hpp` | 内存操作基类 |
| **调用节点** | | |
| `CallNode` | `callnode.hpp` | 方法调用 |
| `CallStaticJavaNode` | `callnode.hpp` | 静态 Java 调用 |
| `CallDynamicJavaNode` | `callnode.hpp` | 虚调用 |
| **常量节点** | | |
| `ConNode` / `ConINode` / `ConLNode` | `connode.hpp` | 常量值 |
| **类型转换** | | |
| `CastNode` | `castnode.hpp` | 类型转换/断言 |
| `ConvertNode` | `convertnode.hpp` | 数值类型转换 |
| **锁节点** | | |
| `LockNode` / `UnlockNode` | `locknode.hpp` | 锁操作 (可被逃逸分析消除) |

### IGVN (Iterative Global Value Numbering)

IGVN 是 C2 最核心的优化框架，实现在 `phaseX.cpp` 中。它通过迭代地对图中的节点应用 `Ideal()` 变换来优化代码:

**工作原理:**
1. 维护一个 worklist (待处理节点集合)
2. 从 worklist 取出节点，调用其 `Ideal()` 方法尝试变换
3. 如果节点被变换，将受影响的邻居节点加入 worklist
4. 重复直到 worklist 为空 (达到不动点)

**每个节点类都可以定义自己的优化规则:**
- `Ideal()`: 返回替代节点 (图变换)
- `Value()`: 计算节点的类型 (类型推断)
- `Identity()`: 返回等价的已有节点 (消除冗余)

**IGVN 执行的典型优化:**
- 常量折叠: `3 + 5` → `8`
- 代数简化: `x + 0` → `x`, `x * 1` → `x`
- 公共子表达式消除: 相同的计算只做一次
- 死代码消除: 移除无用节点
- 强度削减: `x * 2` → `x << 1`

### 循环优化 (PhaseIdealLoop)

循环优化是 C2 中最复杂的优化阶段之一，实现分布在多个文件中:

| 文件 | 优化技术 |
|------|----------|
| `loopopts.cpp` | 循环不变量外提 (LICM)、split-if |
| `loopTransform.cpp` | 循环展开 (unrolling)、循环剥离 (peeling) |
| `loopUnswitch.cpp` | 循环分支外提 (unswitching) |
| `loopPredicate.cpp` | 循环谓词 (predication) |
| `superword.cpp` | 向量化 (在循环优化之后) |

**主要循环变换:**

| 变换 | 说明 | 典型收益 |
|------|------|----------|
| **循环展开 (Unrolling)** | 复制循环体多次，减少分支开销 | 减少循环控制开销，暴露更多优化机会 |
| **循环剥离 (Peeling)** | 提取第一/最后几次迭代 | 消除首次迭代的特殊检查 |
| **循环不变量外提 (LICM)** | 将不依赖循环变量的计算移出循环 | 减少重复计算 |
| **循环分支外提 (Unswitching)** | 将循环内条件判断移到循环外 | 消除循环内分支 |
| **范围检查消除 (RCE)** | 证明数组访问总在范围内，消除边界检查 | 减少运行时检查 |
| **循环谓词 (Predication)** | 在循环前插入一次性检查 | 将循环内检查提前到循环外 |

---

## 10. 逃逸分析深入

### 逃逸状态分类

C2 的逃逸分析 (Escape Analysis) 使用 Connection Graph 算法，将对象分为三种逃逸状态 (定义在 `escape.hpp`):

| 逃逸状态 | 枚举值 | 说明 | 可执行优化 |
|----------|--------|------|------------|
| `NoEscape` | 1 | 对象不逃逸方法和线程 | 标量替换、栈上分配、锁消除 |
| `ArgEscape` | 2 | 对象作为参数传递但不逃逸线程 | 锁消除 (部分场景) |
| `GlobalEscape` | 3 | 对象逃逸方法或线程 | 无优化 |

### 标量替换 (Scalar Replacement)

当对象被判定为 `NoEscape` 时，C2 可以将对象的字段拆解为独立的标量变量，从而完全消除堆分配:

```java
// 原始代码
Point p = new Point(x, y);
double dist = Math.sqrt(p.x * p.x + p.y * p.y);

// 标量替换后 (概念等效)
double p_x = x;
double p_y = y;
double dist = Math.sqrt(p_x * p_x + p_y * p_y);
// Point 对象从未在堆上分配
```

**标量替换的限制:**
- 对象不能逃逸方法 (必须是 `NoEscape`)
- 对象类型必须在编译时已知 (不能是动态分派的)
- 对象的所有字段必须可追踪 (通常意味着对象不能存入数组)
- 对象大小受限 (受 `EliminateAllocationArraySizeLimit` 影响)
- `@IntrinsicCandidate` 方法内部分配的对象通常难以分析

**相关 VM 参数:**
- `-XX:+DoEscapeAnalysis` (默认开启): 启用逃逸分析
- `-XX:+EliminateAllocations` (默认开启): 启用标量替换
- `-XX:+EliminateLocks` (默认开启): 启用锁消除

### 锁消除 (Lock Elimination)

当逃逸分析确定对象不逃逸线程时，对该对象的同步操作可以被安全消除:

```java
// 原始代码
synchronized (new Object()) {  // 锁对象不逃逸
    doWork();
}

// 锁消除后 (概念等效)
doWork();  // synchronized 被完全消除
```

**锁消除条件:**
- 锁对象必须是 `NoEscape` 或在某些情况下 `ArgEscape`
- 逃逸分析必须成功完成
- 锁消除由 `PhaseMacroExpand::eliminate_macro_nodes()` 在宏扩展阶段执行

### 栈上分配

在 HotSpot 中，标量替换是主要的分配消除策略。严格意义上的"栈上分配"(在栈帧上分配完整对象) 在 HotSpot C2 中的实现方式主要就是通过标量替换来消除分配，而非在栈上保留完整的对象头和字段布局。GraalVM 的部分转义分析 (Partial Escape Analysis) 在这方面提供了更精细的优化。

### 逃逸分析的迭代

C2 的逃逸分析可以迭代执行 (源码中的 `do_iterative_escape_analysis()`)。当一轮逃逸分析成功消除了一些分配或锁后，可能暴露出新的 `NoEscape` 对象，因此再次运行逃逸分析可能发现更多优化机会。

---

## 11. 内联优化深入

### 内联决策参数

C2 的内联决策涉及多个 VM 参数 (定义在 `c2_globals.hpp`):

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `MaxInlineSize` | 35 | 方法字节码 <= 此值时，不论调用频率都尝试内联 |
| `FreqInlineSize` | 平台相关 (~325) | 热方法字节码 <= 此值时可内联 |
| `MaxInlineLevel` | 15 | 最大内联嵌套深度 |
| `InlineSmallCode` | 平台相关 | 已编译代码大小阈值 |

**内联决策流程** (简化，源码: `opto/bytecodeInfo.cpp`):

```
1. 方法字节码大小 <= MaxInlineSize?  → 直接内联
2. 方法是热方法 (基于 profiling)?
   2a. 字节码大小 <= FreqInlineSize? → 内联
   2b. 否则 → 不内联 (too big)
3. 内联深度 > MaxInlineLevel?       → 不内联 (too deep)
4. 编译后代码太大?                   → 不内联
5. 递归调用?                         → 通常不内联
```

### 多态内联

C2 支持对虚方法调用进行内联，采用以下策略:

**CHA (Class Hierarchy Analysis):**
- 在编译时分析类继承关系
- 如果某个虚方法只有一个实现 (或当前加载的类中只有一个实现)，可以直接内联
- 如果后续加载了新的子类覆盖了该方法，需要去优化 (deoptimization)

**基于 Profiling 的内联:**
- Tier 3 编译时，C1 收集调用点 (call site) 的类型统计
- C2 根据 profiling 数据判断最常见的接收者类型
- 对于单态调用点 (monomorphic): 直接内联目标方法 + 类型守卫 (type guard)
- 对于双态调用点 (bimorphic): 可能内联两个最常见的目标

**Inline Cache:**
- 解释器和 C1 编译代码使用 inline cache 记录最近一次的调用目标
- 单态 inline cache (monomorphic IC): 缓存一个类型 → 直接跳转
- 多态 inline cache (polymorphic IC): 缓存多个类型 → 查表跳转
- 超多态 (megamorphic): 退回 vtable dispatch

### 内联的级联效应

内联不仅减少方法调用开销，更重要的是将被调用方法的代码暴露给调用者的优化上下文。内联后，逃逸分析、常量折叠、循环优化等都可以跨越原来的方法边界进行优化。这就是为什么 `FreqInlineSize` 对性能影响巨大。

---

## 12. JIT 编译与虚拟线程

### Continuation 帧对 JIT 的影响

JDK 21 引入的虚拟线程 (Virtual Threads) 基于 Continuation 实现。当虚拟线程在阻塞操作处被挂起时，需要将当前线程栈帧保存到堆上 (freeze)；恢复时从堆上恢复栈帧 (thaw)。这对 JIT 编译器有以下影响:

**栈帧冻结/解冻 (Freeze/Thaw):**
- JIT 编译的栈帧需要能够被正确地序列化到堆上
- 编译代码中的 OopMap (对象指针映射) 必须在 yield 点处准确
- JIT 需要在 safepoint 处维护足够的元数据，以支持栈帧的冻结和恢复

**对优化的潜在约束:**
- 栈帧布局需要与 Continuation 机制兼容
- JIT 可以照常进行大部分优化 (内联、逃逸分析等)
- 虚拟线程的挂起/恢复路径本身 (`Continuation.yield`、`Continuation.run`) 是 intrinsic 方法，JIT 对其有特殊处理

**性能特点:**
- 虚拟线程不影响 JIT 编译的热路径性能——非阻塞代码的编译结果与平台线程一致
- 性能开销主要在 freeze/thaw 操作本身 (栈帧拷贝)
- JIT 对 `Continuation.yield` 的处理确保了 freeze/thaw 操作的正确性

---

## 13. AOT 编译演进

### 从 JEP 295 到 Project Leyden

Java AOT (Ahead-of-Time) 编译经历了多个阶段的演进:

| 阶段 | JEP/项目 | JDK 版本 | 状态 | 说明 |
|------|----------|----------|------|------|
| **第一代** | JEP 295 (jaotc) | JDK 9-15 | 已移除 (JDK 16) | 基于 Graal 的实验性 AOT；使用复杂、收益有限 |
| **GraalVM** | Native Image | 外部项目 | 活跃 | 闭合世界 (closed-world) AOT；不支持完整 Java 动态特性 |
| **第二代** | Project Leyden | JDK 24+ | 进行中 | 渐进式 AOT，保持 Java 完整语义 |

### JEP 295: jaotc (JDK 9, 已移除)

- 使用 Graal 编译器将字节码 AOT 编译为共享库 (.so)
- 需要手动指定要编译的类/方法
- 不支持完整的 Java 动态特性 (反射、动态类加载受限)
- 维护成本高，使用者少，在 JDK 16 中被 JEP 410 移除

### GraalVM Native Image

- SubstrateVM 提供的闭合世界 AOT 编译
- 编译时确定所有可达代码 (不支持运行时动态类加载)
- 启动时间可达毫秒级，内存占用显著降低
- 需要额外配置以支持反射、JNI、代理等动态特性
- 独立于 OpenJDK 主线发展

### Project Leyden (JDK 24+)

Project Leyden 采用与 jaotc 和 Native Image 不同的策略——**渐进式约束 (gradual constraints)**，在保持 Java 完整语义的前提下逐步引入 AOT 能力:

| JEP | 标题 | 说明 |
|-----|------|------|
| **JEP 483** | Ahead-of-Time Class Loading & Linking | AOT 类加载和链接缓存；训练运行记录类加载顺序，后续启动直接使用 |
| **JEP 514** | Ahead-of-Time Cache for Code | AOT 代码缓存；缓存 JIT 编译结果，后续启动直接加载已编译代码 |
| **JEP 515** | Ahead-of-Time Method Profiling | AOT 方法 Profiling；缓存训练运行的 profiling 数据，让 C2 在启动时就能做高质量编译 |
| **JEP 516** | Ahead-of-Time Compilation (Preview) | AOT 编译 (预览)；将编译结果持久化存储 |

**Leyden 的关键区别:**
- 保持 Java 的完整动态性 (反射、动态加载等完全支持)
- 基于训练运行 (training run) 收集数据，不要求闭合世界假设
- 渐进式改进: 每个 JEP 独立提供收益，可组合使用
- 据早期测试报告，启动时间改善可达 15-25% (具体数字因应用而异)

---

## 14. Graal 编译器简史

### JVMCI: JIT 编译器接口

**JEP 243: Java-Level JVM Compiler Interface (JDK 9)**
- 定义了 JVM 与外部 JIT 编译器之间的标准接口
- 允许用 Java 编写的编译器替代 C2
- 源码位于 `src/hotspot/share/jvmci/`
- Graal 编译器是 JVMCI 的主要消费者

### Graal JIT 在 OpenJDK 中的历程

| 版本 | 事件 | 说明 |
|------|------|------|
| JDK 9 | JEP 243 (JVMCI) | 引入编译器接口，为 Graal 提供插入点 |
| JDK 10 | JEP 317 (Experimental Graal) | Graal JIT 作为实验性特性加入 OpenJDK |
| JDK 17 | JEP 410 (Remove Experimental Graal) | 从 OpenJDK 中移除实验性 Graal JIT 编译器；原因: 维护成本高，使用者少，Graal 在 GraalVM 中独立发展更好 |

**JEP 410 移除的原因:**
- OpenJDK 中的 Graal 副本与 GraalVM 的 Graal 版本逐渐分歧
- 很少有用户通过 OpenJDK 使用 Graal JIT
- JVMCI 接口保留，用户仍可通过 GraalVM 或自行集成使用 Graal

### GraalVM 外部发展

Graal 编译器在 GraalVM 项目中继续独立发展:

- **GraalVM CE/EE**: 提供 Graal JIT (替代 C2) + Native Image (AOT)
- **Truffle 框架**: 基于 Graal 的多语言运行时 (JavaScript、Python、Ruby 等)
- **部分转义分析 (Partial Escape Analysis)**: GraalVM 独有的高级优化，比 C2 的逃逸分析更精细
- **推测性优化 (Speculative Optimizations)**: 更激进的推测性去虚化和内联
- GraalVM 从 JDK 21 开始跟踪 OpenJDK 版本发布节奏

---

## 15. 诊断工具

### -XX:+PrintCompilation

打印每个方法的编译事件:

```
  176   3       3       java.lang.String::hashCode (55 bytes)
  │     │       │       │                           │
  时间   编译ID  层级    方法名                      字节码大小
```

**层级说明:** 1=C1无profiling, 2=C1有限profiling, 3=C1完全profiling, 4=C2

**常见标记:**
- `%`: OSR (On-Stack Replacement) 编译
- `s`: 同步方法
- `!`: 方法包含异常处理
- `b`: 阻塞编译 (调用线程等待编译完成)
- `n`: native 方法包装
- `made not entrant`: 方法被去优化，不再接受新调用
- `made zombie`: 方法可被回收

### -XX:+PrintInlining

打印内联决策树 (需配合 `-XX:+UnlockDiagnosticVMOptions`):

```
@ 12   java.lang.String::length (5 bytes)   inline (hot)
@ 28   java.util.HashMap::get (23 bytes)   inline (hot)
  @ 9   java.util.HashMap::hash (20 bytes)   inline (hot)
  @ 15  java.util.HashMap::getNode (148 bytes)   inline (hot)
@ 45   com.example.Foo::bar (402 bytes)   too big
```

**常见内联失败原因:**
- `too big`: 方法字节码超过 `FreqInlineSize` (热方法) 或 `MaxInlineSize` (冷方法)
- `too deep`: 超过 `MaxInlineLevel`
- `not inlineable`: 方法不可内联 (如 native 方法)
- `no static binding`: 无法确定调用目标
- `callee is too large`: 被调方法编译后代码太大

### JFR 编译事件

JFR (Java Flight Recorder) 提供以下编译相关事件:

| 事件 | 说明 |
|------|------|
| `jdk.Compilation` | 编译完成事件 (方法名、编译时长、编译层级、代码大小) |
| `jdk.CompilerInlining` | 内联决策事件 (成功/失败及原因) |
| `jdk.CompilationFailure` | 编译失败事件 |
| `jdk.Deoptimization` | 去优化事件 (原因、方法) |
| `jdk.CompilerPhase` | 编译阶段耗时 (各优化 pass 的时间分解) |

```bash
# 启动时开启 JFR 编译事件记录
java -XX:StartFlightRecording=settings=profile,filename=compile.jfr ...

# 运行时开启
jcmd <pid> JFR.start settings=profile name=compile
jcmd <pid> JFR.dump name=compile filename=compile.jfr
```

### IdealGraphVisualizer (IGV)

IGV 是 C2 Ideal Graph 的可视化工具，用于分析 C2 编译器在各优化阶段的图变换:

**使用步骤:**

```bash
# 1. 启动 IGV (需要单独下载)
# 从 https://github.com/niclasvoss/igv 或 GraalVM 获取
idealgraphvisualizer &

# 2. 运行 Java 程序，输出 Ideal Graph 到 IGV
java -XX:+UnlockDiagnosticVMOptions \
     -XX:+PrintIdealGraph \
     -XX:PrintIdealGraphAddress=localhost \
     -XX:PrintIdealGraphPort=4444 \
     MyApp

# 3. 或者输出到文件后再用 IGV 打开
java -XX:+UnlockDiagnosticVMOptions \
     -XX:+PrintIdealGraph \
     -XX:PrintIdealGraphFile=graph.xml \
     MyApp
```

**IGV 分析要点:**
- 对比不同优化阶段的图变化 (如 "After Parsing" vs "After IGVN")
- 查看节点的类型信息和输入/输出边
- 追踪特定节点在各阶段的变换
- 识别未被优化掉的冗余节点

> 详细教程参见: [IGV 实战教程](igv-tutorial.md)

### 其他诊断参数

```bash
# 编译时间统计
-XX:+CITime

# 打印汇编 (需安装 hsdis 插件)
-XX:+UnlockDiagnosticVMOptions -XX:+PrintAssembly

# 指定方法编译/不编译
-XX:CompileOnly=java.lang.String::hashCode
-XX:CompileCommand=dontinline,com.example.Foo::bar

# 打印去优化信息
-XX:+TraceDeoptimization

# C2 SuperWord 向量化追踪
-XX:+TraceSuperWord
```

---

## 16. 重要 PR 分析

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

**问题**: `DateTimePrintContext.adjust` 方法字节码大小 382 > 325 字节 (FreqInlineSize，热方法阈值)，导致 C2 无法内联

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
- C2 热方法内联阈值约 325 字节 (FreqInlineSize; 冷方法阈值为 35 字节 MaxInlineSize)
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

## 17. JIT 内联优化最佳实践

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

## 18. 相关链接

### 本地文档

- [C2 优化阶段](c2-phases.md) - 15 个编译阶段详解
- [VM 参数](vm-parameters.md) - 完整参数参考
- [诊断工具](diagnostics.md) - 调试和性能分析
- [近期改进](recent-changes.md) - 2024-2026 更新
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

---

**最后更新**: 2026-03-22
