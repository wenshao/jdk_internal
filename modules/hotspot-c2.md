# hotspot-c2 模块分析

> C2 Server 编译器 — HotSpot 的高级即时编译器 (Advanced JIT Compiler)

---

## 1. 概述

C2 (又称 Server Compiler 或 Opto) 是 HotSpot VM 的高级 JIT 编译器，负责生成高度优化的机器码。C2 在分层编译 (Tiered Compilation) 中处于最高层级 (Level 4)，是 Java 应用峰值性能的关键。

### 1.1 编译器对比

| 特性 | C1 (Client) | C2 (Server/Opto) |
|------|-------------|-------------------|
| 源码目录 | `share/c1/` (44 files) | `share/opto/` (158 files) |
| 编译速度 | 快 (数百微秒) | 慢 (数毫秒到数十毫秒) |
| IR 类型 | HIR/LIR (线性) | Ideal Graph (Sea of Nodes) |
| 优化深度 | 基本优化 | 激进优化 (逃逸分析、循环变换等) |
| 峰值性能 | 中 | 高 |

### 1.2 分层编译中的位置

```
Level 0: 解释执行 (Interpreter)
    ↓ (方法调用/回边计数达到阈值)
Level 1: C1 编译, 无 profiling
Level 2: C1 编译, 有限 profiling
Level 3: C1 编译, 完整 profiling (收集类型信息、分支概率)
    ↓ (profiling 数据充足)
Level 4: C2 编译, 完全优化 (使用 Level 3 收集的 profile 数据)
```

---

## 2. 源码结构

### 2.1 opto/ 目录 (C2 核心)

**路径**: `src/hotspot/share/opto/`
**规模**: **85 个 .cpp 文件** + **73 个 .hpp 文件** = 158 文件

```
opto/
├── 编译器入口与调度 (Compiler entry)
│   ├── c2compiler.cpp/hpp         # C2Compiler 类: compile_method() 入口
│   ├── compile.cpp/hpp            # Compile 类: 单次编译的上下文
│   └── phase.cpp/hpp              # Phase 基类: 所有优化阶段的父类
│
├── IR 节点定义 (Node types)
│   ├── node.cpp/hpp               # Node 基类: 所有 IR 节点的根
│   ├── cfgnode.cpp/hpp            # 控制流节点: RegionNode, IfNode, PhiNode
│   ├── callnode.cpp/hpp           # 调用节点: CallNode, SafePointNode
│   ├── memnode.cpp/hpp            # 内存节点: LoadNode, StoreNode
│   ├── addnode.cpp/hpp            # 加法节点: AddINode, AddLNode, AddPNode
│   ├── subnode.cpp/hpp            # 减法/比较: SubNode, CmpNode, BoolNode
│   ├── mulnode.cpp/hpp            # 乘法/位移: MulNode, LShiftNode
│   ├── divnode.cpp/hpp            # 除法: DivINode, DivLNode, ModNode
│   ├── connode.cpp/hpp            # 常量节点: ConINode, ConLNode
│   ├── castnode.cpp/hpp           # 类型转换: CastIINode, CheckCastPPNode
│   ├── convertnode.cpp/hpp        # 数值转换: ConvI2LNode
│   ├── loopnode.cpp/hpp           # 循环节点: LoopNode, CountedLoopNode
│   ├── locknode.cpp/hpp           # 锁节点: LockNode, UnlockNode
│   ├── rootnode.cpp/hpp           # 根节点: RootNode
│   ├── machnode.cpp/hpp           # 机器节点: MachNode (指令选择后)
│   ├── multnode.cpp/hpp           # 多输出节点: MultiNode, ProjNode
│   ├── opaquenode.cpp/hpp         # 不透明节点 (防止优化穿透)
│   ├── intrinsicnode.cpp/hpp      # 内建函数节点
│   ├── vectornode.cpp/hpp         # 向量化节点
│   └── movenode.cpp/hpp           # 条件移动节点
│
├── 解析与内联 (Parsing & Inlining)
│   ├── parse1.cpp                 # 字节码解析: 控制流
│   ├── parse2.cpp                 # 字节码解析: 数据流
│   ├── parse3.cpp                 # 字节码解析: 调用与字段
│   ├── parseHelper.cpp            # 解析辅助
│   ├── parse.hpp                  # Parse 类定义
│   ├── doCall.cpp                 # 方法调用处理
│   ├── callGenerator.cpp/hpp      # CallGenerator: 内联/虚调用决策
│   ├── bytecodeInfo.cpp           # 内联信息: InlineTree
│   └── graphKit.cpp/hpp           # GraphKit: 构建 IR 的工具类
│
├── 优化阶段 (Optimization phases)
│   ├── phaseX.cpp/hpp             # PhaseGVN / PhaseIterGVN: 全局值编号
│   ├── escape.cpp/hpp             # 逃逸分析: ConnectionGraph
│   ├── loopopts.cpp               # 循环优化: 不变代码外提、展开
│   ├── loopTransform.cpp          # 循环变换: 预剥离、展开、向量化
│   ├── loopPredicate.cpp          # 循环谓词: Range Check Elimination
│   ├── loopUnswitch.cpp           # 循环开关: Loop Unswitching
│   ├── macro.cpp/hpp              # 宏展开: 分配、锁
│   ├── stringopts.cpp/hpp         # 字符串优化: StringBuilder 折叠
│   ├── split_if.cpp               # If 分裂优化
│   ├── predicates.cpp/hpp         # 谓词优化
│   └── superword.cpp/hpp          # 超字向量化 (SLP vectorization)
│
├── 代码生成 (Code generation)
│   ├── matcher.cpp/hpp            # 指令选择: Ideal → MachNode (BURS)
│   ├── chaitin.cpp/hpp            # Chaitin-Briggs 图着色寄存器分配
│   ├── regalloc.cpp/hpp           # 寄存器分配基类
│   ├── regmask.cpp/hpp            # 寄存器掩码
│   ├── ifg.cpp                    # 干扰图 (Interference Graph) 构建
│   ├── coalesce.cpp/hpp           # 寄存器合并 (Coalescing)
│   ├── postaloc.cpp               # 分配后优化
│   ├── reg_split.cpp              # 寄存器溢出拆分
│   ├── live.cpp/hpp               # 活跃性分析 (Liveness Analysis)
│   ├── output.cpp/hpp             # PhaseOutput: 机器码发射
│   ├── block.cpp/hpp              # 基本块 (BasicBlock)
│   ├── gcm.cpp                    # Global Code Motion: 指令调度
│   ├── lcm.cpp                    # Local Code Motion
│   ├── buildOopMap.cpp            # OopMap 构建 (GC 根扫描)
│   └── constantTable.cpp/hpp      # 常量表
│
├── 类型系统 (Type system)
│   ├── type.cpp/hpp               # Type 层次: TypeInt, TypePtr, TypeOop 等
│   ├── rangeinference.cpp/hpp     # 范围推断 (值域分析)
│   └── mempointer.cpp/hpp        # 内存指针分析
│
├── 向量化 (Vectorization)
│   ├── vector.cpp/hpp             # 向量操作
│   ├── vectorIntrinsics.cpp       # 向量内建函数
│   ├── vectorization.cpp/hpp      # 自动向量化框架
│   ├── vtransform.cpp/hpp         # 向量变换
│   └── superwordVTransformBuilder.cpp/hpp # 超字向量变换
│
└── 其他 (Miscellaneous)
    ├── idealKit.cpp/hpp           # IdealKit: 手动构建 IR 片段
    ├── idealGraphPrinter.cpp/hpp  # IGV 输出 (Ideal Graph Visualizer)
    ├── classes.cpp/hpp            # 节点类注册
    ├── opcodes.cpp/hpp            # 操作码定义
    ├── indexSet.cpp/hpp           # 高效位集
    ├── runtime.cpp/hpp            # 运行时桩调用
    ├── library_call.cpp/hpp       # 库函数内联 (Math, System.arraycopy 等)
    ├── phasetype.cpp/hpp          # 阶段类型枚举
    ├── printinlining.cpp/hpp      # 内联决策打印
    └── replacednodes.cpp/hpp      # 被替换节点追踪
```

---

## 3. 编译总流程

### 3.1 入口

```cpp
// src/hotspot/share/opto/c2compiler.cpp
C2Compiler::compile_method()
  → Compile::Compile()             // 创建编译上下文
    → Parse (字节码 → Ideal Graph) // 阶段 1: 解析
    → Compile::Optimize()          // 阶段 2: 优化
    → Compile::Code_Gen()          // 阶段 3: 代码生成
```

### 3.2 Compile::Optimize() — 优化阶段详解

以下是 `Compile::Optimize()` 的实际执行顺序 (来自 `compile.cpp:2293`):

```
Compile::Optimize() {
    // === 第一轮 IGVN (Iterative Global Value Numbering) ===
    PhaseIterGVN igvn;
    igvn.optimize();                       // 初始值编号 + Ideal 变换

    // === 增量内联 (Incremental Inlining) ===
    inline_incrementally(igvn);            // 逐步内联更多方法
    inline_boxing_calls(igvn);             // 内联 valueOf() 等装箱方法

    // === 类型清理 ===
    remove_speculative_types(igvn);        // 移除推测类型
    cleanup_expensive_nodes(igvn);         // 清理代价高的节点

    // === Vector API 支持 ===
    if (has_vbox_nodes()) {
        PhaseVector pv(igvn);
        pv.optimize_vector_boxes();        // 优化 VectorAPI box 操作
    }

    // === 逃逸分析 (Escape Analysis) ===
    if (do_escape_analysis()) {
        ConnectionGraph::do_analysis();    // 构建连接图, 判断逃逸状态
        igvn.optimize();                   // 基于逃逸分析结果再优化
        PhaseMacroExpand mexp(igvn);
        mexp.eliminate_macro_nodes();      // 消除标量替换的分配
    }

    // === 循环优化 (Loop Optimizations) — 多轮 ===
    PhaseIdealLoop::optimize(igvn, LoopOptsDefault);      // 第 1 轮
    PhaseIdealLoop::optimize(igvn, LoopOptsSkipSplitIf);  // 第 2 轮 (partial peeling)
    PhaseIdealLoop::optimize(igvn, LoopOptsSkipSplitIf);  // 第 3 轮 (pre-CCP)

    // === 条件常量传播 (Conditional Constant Propagation) ===
    PhaseCCP ccp(&igvn);
    ccp.do_transform();                    // 基于控制流的常量传播

    // === 第二轮 IGVN ===
    igvn.reset_from_igvn(&ccp);
    igvn.optimize();                       // CCP 后再做值编号

    // === 第二轮循环优化 ===
    optimize_loops(igvn, LoopOptsDefault); // 更多循环变换

    // === 后处理 ===
    process_for_post_loop_opts_igvn(igvn);
    process_for_merge_stores_igvn(igvn);   // 合并存储优化

    // === 宏展开 (Macro Expansion) ===
    PhaseMacroExpand mex(igvn);
    mex.eliminate_macro_nodes();            // 消除剩余宏节点
    mex.expand_macro_nodes();              // 展开分配、锁等为低级操作

    // === 屏障展开 (Barrier Expansion) ===
    bs->expand_barriers(this, igvn);       // GC 屏障展开

    // === 向量逻辑优化 ===
    optimize_logic_cones(igvn);            // 向量逻辑锥优化

    // === 最终图重塑 ===
    final_graph_reshaping();               // 最终清理和规范化
}
```

### 3.3 Compile::Code_Gen() — 代码生成阶段

来自 `compile.cpp:3009`:

```
Compile::Code_Gen() {
    // 1. 指令选择 (Instruction Selection)
    Matcher matcher;
    matcher.match();                // Ideal Graph → MachNode Graph (BURS 算法)

    // 2. 构建控制流图 (CFG Construction)
    PhaseCFG cfg(node_arena(), root(), matcher);
    cfg.do_global_code_motion();    // 全局代码移动: 调度指令

    // 3. 寄存器分配 (Register Allocation)
    PhaseChaitin regalloc(unique(), cfg, matcher, false);
    regalloc.Register_Allocate();   // Chaitin-Briggs 图着色

    // 4. 基本块优化 (Block Optimization)
    cfg.remove_empty_blocks();
    PhaseBlockLayout layout(cfg);   // 基于频率的块布局
    cfg.fixup_flow();
    cfg.remove_unreachable_blocks();

    // 5. 窥孔优化 (Peephole Optimization)
    PhasePeephole peep(_regalloc, cfg);
    peep.do_transform();

    // 6. 分配后展开 (Post-Alloc Expand, 某些 CPU)
    cfg.postalloc_expand(_regalloc);

    // 7. 代码发射 (Code Emission)
    PhaseOutput output;
    output.Output();                // 将 MachNode 编码为机器码
    output.install();               // 安装到 CodeCache
}
```

---

## 4. 中间表示 (Intermediate Representation)

### 4.1 Sea of Nodes — Ideal Graph

C2 使用 "Sea of Nodes" IR (由 Cliff Click 发明)，其特点:
- **数据流和控制流统一表示** — 节点通过边连接，无显式基本块
- **SSA 形式** — 每个值只有一个定义
- **图变换即优化** — 通过模式匹配和重写规则优化

### 4.2 Node 基类

**源码**: `src/hotspot/share/opto/node.hpp`

```cpp
class Node {
 protected:
  Node** _in;       // 输入边数组 (input edges)
  Node** _out;      // 输出边数组 (use-def chains)
  uint   _cnt;      // 输入边数量
  uint   _outcnt;   // 输出边数量
  uint   _idx;      // 唯一节点编号

 public:
  // 每个节点实现 Ideal() 进行局部优化 (pattern → simplified form)
  virtual Node* Ideal(PhaseGVN* phase, bool can_reshape);
  // 每个节点实现 Value() 进行值分析
  virtual const Type* Value(PhaseGVN* phase) const;
  // 每个节点实现 Identity() 发现恒等变换
  virtual Node* Identity(PhaseGVN* phase);
};
```

### 4.3 Node 类层次 (主要分支)

```
Node (node.hpp)
├── TypeNode                    # 带类型信息的节点
├── RegionNode (cfgnode.hpp)    # 控制流合并 (merge point)
│   └── LoopNode (loopnode.hpp) # 循环头
│       └── CountedLoopNode     # 计数循环
├── IfNode (cfgnode.hpp)        # 条件分支
│   └── RangeCheckNode          # 范围检查
├── GotoNode (cfgnode.hpp)      # 无条件跳转
├── PhiNode (cfgnode.hpp)       # SSA Phi 函数 (值合并)
├── AddNode (addnode.hpp)       # 加法
│   ├── AddINode                # int 加法
│   ├── AddLNode                # long 加法
│   └── AddPNode                # 指针加法 (base + offset)
├── SubNode (subnode.hpp)       # 减法
│   ├── CmpINode                # int 比较
│   ├── CmpLNode                # long 比较
│   └── CmpPNode                # 指针比较
├── MulNode (mulnode.hpp)       # 乘法
│   └── LShiftNode              # 左移
├── MemNode (memnode.hpp)       # 内存操作
│   ├── LoadNode                # 内存加载
│   │   ├── LoadINode            # load int
│   │   ├── LoadLNode            # load long
│   │   └── LoadPNode            # load pointer
│   └── StoreNode               # 内存存储
│       ├── StoreINode           # store int
│       └── StorePNode           # store pointer
├── CallNode (callnode.hpp)     # 方法调用
│   ├── CallStaticJavaNode      # 静态/确定性调用
│   └── CallDynamicJavaNode     # 虚方法调用
├── SafePointNode (callnode.hpp)# 安全点
├── ReturnNode (callnode.hpp)   # 返回
├── BoolNode (subnode.hpp)      # 布尔结果
├── AbsNode (subnode.hpp)       # 绝对值
├── NegNode (subnode.hpp)       # 取反
├── ConNode (connode.hpp)       # 常量
├── MachNode (machnode.hpp)     # 指令选择后的机器节点
│   ├── MachReturnNode          # 机器返回
│   ├── MachCallNode            # 机器调用
│   └── MachSpillCopyNode       # 溢出/恢复
├── LockNode (locknode.hpp)     # monitorenter
├── UnlockNode (locknode.hpp)   # monitorexit
├── RootNode (rootnode.hpp)     # 图的根节点
├── VectorNode (vectornode.hpp) # SIMD 向量操作
└── MultiNode (multnode.hpp)    # 多输出节点
    └── ProjNode                # 投影 (选择某个输出)
```

### 4.4 SSA 与 Phi 节点示例

```java
// Java 源码
int result;
if (x > 0) {
    result = a + b;
} else {
    result = a - b;
}
return result;
```

```
// C2 Ideal Graph (简化)
        [CmpI x, 0]
             |
         [Bool GT]
             |
         [If]──────────────┐
         /                  \
    [IfTrue]            [IfFalse]
        |                    |
    [AddI a, b]          [SubI a, b]
        \                   /
         ──── [Region] ────
               |
         [Phi result]      ← SSA Phi: 合并两个分支的值
               |
          [Return]
```

---

## 5. 关键优化详解

### 5.1 全局值编号 (GVN — Global Value Numbering)

**源码**: `src/hotspot/share/opto/phaseX.cpp`

```cpp
class PhaseIterGVN : public PhaseGVN {
    // 迭代式全局值编号
    // 核心: 将计算相同值的节点合并为一个
    void optimize();                       // 主循环: 工作列表驱动

    // 每个节点的 Ideal() 方法实现局部变换:
    // (a + 0) → a                         // 恒等消除
    // (a + K1) + K2 → a + (K1+K2)         // 常量折叠
    // (a - a) → 0                         // 代数简化
};
```

### 5.2 逃逸分析 (Escape Analysis)

**源码**: `src/hotspot/share/opto/escape.cpp/hpp`

```cpp
// escape.hpp:157
// 三级逃逸状态
enum EscapeState {
    NoEscape     = 1,  // 不逃逸: 可标量替换/栈分配 (scalar replacement/stack allocation)
    ArgEscape    = 2,  // 参数逃逸: 可消除锁 (lock elimination)
    GlobalEscape = 3   // 全局逃逸: 必须堆分配 (heap allocation required)
};

// escape.hpp:323
class ConnectionGraph: public ArenaObj {
    // 构建"连接图": 追踪对象引用关系
    static void do_analysis(Compile* C, PhaseIterGVN* igvn);
    // 分析结果用于:
    // 1. 标量替换 (Scalar Replacement): 将对象字段拆为局部变量
    // 2. 锁消除 (Lock Elimination): 移除不逃逸对象的锁
    // 3. 栈分配 (Stack Allocation): 在栈上分配不逃逸对象
};
```

**优化示例**:
```java
// 源码
synchronized (new Object()) {  // NoEscape → 锁消除
    Point p = new Point(x, y); // NoEscape → 标量替换
    return p.x + p.y;          // → 直接 return x + y
}
```

### 5.3 循环优化 (Loop Optimizations)

**源码**: `loopnode.cpp`, `loopopts.cpp`, `loopTransform.cpp`, `loopPredicate.cpp`, `loopUnswitch.cpp`

`PhaseIdealLoop` 执行以下变换:

| 优化 | 源文件 | 说明 |
|------|--------|------|
| 循环不变代码外提 (LICM) | `loopopts.cpp` | 将循环内不变计算移到循环外 |
| 循环展开 (Unrolling) | `loopTransform.cpp` | 减少循环开销 |
| 循环预剥离 (Pre-peeling) | `loopTransform.cpp` | 剥离首次迭代 |
| 范围检查消除 (RCE) | `loopPredicate.cpp` | 消除数组越界检查 |
| 循环开关 (Loop Unswitching) | `loopUnswitch.cpp` | 将循环内条件移到循环外 |
| 循环向量化 (Vectorization) | `superword.cpp` | SLP (Superword Level Parallelism) |
| 循环条带挖掘 (Strip Mining) | `loopTransform.cpp` | 限制循环体以配合安全点 |

### 5.4 内联 (Inlining)

**源码**: `doCall.cpp`, `callGenerator.cpp`, `bytecodeInfo.cpp`

内联决策因素:
- 方法大小 (`-XX:MaxInlineSize=35`, 字节码字节数)
- 调用频率 (`-XX:FreqInlineSize=325`, 热方法阈值)
- 调用深度 (`-XX:MaxInlineLevel=15`)
- 是否是虚方法 (需 CHA 类层次分析去虚化)
- 内建函数 (`library_call.cpp` 中的 intrinsic 方法)

### 5.5 条件常量传播 (CCP)

**源码**: `phaseX.cpp` 中的 `PhaseCCP`

CCP 基于控制流进行常量传播，比普通常量传播更强:
```java
// 源码
if (x == 5) {
    y = x + 1;  // CCP 知道此处 x==5, 直接折叠为 y=6
}
```

### 5.6 内建函数 (Intrinsics)

**源码**: `src/hotspot/share/opto/library_call.cpp`

C2 直接为常用库方法生成优化机器码，绕过正常编译:
- `Math.sqrt()`, `Math.abs()`, `Math.min/max()`
- `System.arraycopy()`
- `String.equals()`, `String.compareTo()`
- `Integer.numberOfLeadingZeros()`, `Long.reverseBytes()`
- `Unsafe.compareAndSwap*()`
- `Thread.currentThread()`

### 5.7 字符串优化 (String Optimization)

**源码**: `src/hotspot/share/opto/stringopts.cpp`

- StringBuilder 链式调用折叠 (将多次 append 合并)
- 字符串拼接优化 (避免中间对象)

---

## 6. 指令选择 (Instruction Selection)

### 6.1 Matcher — BURS 算法

**源码**: `src/hotspot/share/opto/matcher.cpp`

C2 使用 BURS (Bottom-Up Rewrite System) 进行指令选择:
1. Ideal Graph 的子树与 `.ad` 文件中的规则匹配
2. 选择代价最低的覆盖方案
3. 生成 MachNode (平台特定的机器节点)

**ADL 文件** (Architecture Description Language):
- `src/hotspot/cpu/x86/x86_64.ad` — x86-64 指令定义
- `src/hotspot/cpu/aarch64/aarch64.ad` — AArch64 指令定义
- 由 `adlc/` (ADL Compiler) 编译为 C++ 代码

### 6.2 匹配示例

```
// Ideal Graph 中的 AddI 节点
AddI(LoadI(mem, off), ConI(42))

// 匹配为 x86 指令
addl reg, [mem + off]    // 合并了 Load + Add
// 或
addl reg, $42            // 如果值已在寄存器中
```

---

## 7. 寄存器分配 (Register Allocation)

### 7.1 PhaseChaitin — Chaitin-Briggs 图着色

**源码**: `src/hotspot/share/opto/chaitin.cpp/hpp`

```cpp
// chaitin.hpp:424
class PhaseChaitin : public PhaseRegAlloc {
 public:
  void Register_Allocate();  // 主入口 (chaitin.cpp)
  // 算法步骤:
  // 1. 活跃性分析 (Liveness Analysis) — live.cpp
  // 2. 构建干扰图 (Interference Graph) — ifg.cpp
  // 3. 合并 (Coalescing) — coalesce.cpp: 消除不必要的复制
  // 4. 简化 (Simplification): 从图中移除度 < K 的节点
  // 5. 选择 (Select): 为节点分配颜色 (寄存器)
  // 6. 溢出 (Spill): 无法着色的节点溢出到栈 — reg_split.cpp
  // 7. 迭代直到成功
};
```

### 7.2 相关文件

| 文件 | 职责 |
|------|------|
| `chaitin.cpp` | 主算法: simplify-select-spill 循环 |
| `ifg.cpp` | 构建干扰图 (两个同时活跃的值不能分配同一寄存器) |
| `coalesce.cpp` | 寄存器合并: 消除 Phi 和 Copy 节点的复制 |
| `live.cpp` | 活跃性分析: 确定每个值的活跃区间 |
| `reg_split.cpp` | 溢出拆分: 将长活跃区间拆成短片段 |
| `postaloc.cpp` | 分配后优化: 利用寄存器值重用机会 |
| `regmask.cpp` | 寄存器掩码: 表示允许分配的寄存器集合 |

---

## 8. 代码发射 (Code Emission)

### 8.1 PhaseOutput

**源码**: `src/hotspot/share/opto/output.cpp`

PhaseOutput 将 MachNode 图编码为二进制机器码:

```
PhaseOutput::Output()
  → 遍历每个基本块 (BasicBlock)
    → 遍历每个 MachNode
      → MachNode::emit() — 发射指令字节
      → 生成重定位信息 (relocation info)
      → 生成 OopMap (GC 根信息)
      → 生成安全点信息 (safepoint debug info)
  → 安装到 CodeCache 成为 nmethod
```

### 8.2 OopMap — GC 安全点信息

**源码**: `buildOopMap.cpp`

在每个安全点 (safepoint)，生成 OopMap 记录:
- 哪些寄存器包含 oop (对象引用)
- 哪些栈位置包含 oop
- GC 可据此准确扫描根集

---

## 9. 平台相关代码

| 架构 | ADL 文件 | CPU 目录 |
|------|----------|----------|
| x86-64 | `cpu/x86/x86_64.ad` | `cpu/x86/` (137 files) |
| AArch64 | `cpu/aarch64/aarch64.ad` | `cpu/aarch64/` (112 files) |
| RISC-V | `cpu/riscv/riscv.ad` | `cpu/riscv/` (107 files) |
| PPC | `cpu/ppc/ppc.ad` | `cpu/ppc/` (105 files) |
| ARM32 | `cpu/arm/arm.ad` | `cpu/arm/` (94 files) |
| s390 | `cpu/s390/s390.ad` | `cpu/s390/` (93 files) |

---

## 10. 调优与诊断

### 10.1 编译控制

```bash
# 分层编译阈值
-XX:Tier3InvocationThreshold=200      # Level 3 触发
-XX:Tier4InvocationThreshold=5000     # Level 4 (C2) 触发

# 内联控制
-XX:MaxInlineSize=35                  # 字节码 ≤ 35 字节总是尝试内联
-XX:FreqInlineSize=325                # 热方法可内联更大方法
-XX:MaxInlineLevel=15                 # 最大内联嵌套深度
-XX:MaxRecursiveInlineLevel=1         # 递归内联层数

# 循环优化
-XX:LoopUnrollLimit=60                # 循环展开限制
-XX:+UseLoopPredicate                 # 启用循环谓词 (范围检查消除)

# 逃逸分析
-XX:+DoEscapeAnalysis                 # 启用逃逸分析 (默认开启)
-XX:+EliminateAllocations             # 标量替换 (默认开启)
-XX:+EliminateLocks                   # 锁消除 (默认开启)
```

### 10.2 诊断工具

```bash
# 编译日志 — 可用 JITWatch 分析
java -XX:+UnlockDiagnosticVMOptions \
     -XX:+LogCompilation \
     -XX:LogFile=compilation.log \
     -jar app.jar

# 打印编译事件 (轻量级)
java -XX:+PrintCompilation -jar app.jar

# 打印生成的汇编码 (需 hsdis 插件)
java -XX:+UnlockDiagnosticVMOptions \
     -XX:+PrintAssembly \
     -jar app.jar

# 输出 Ideal Graph 到 IGV (Ideal Graph Visualizer)
java -XX:+UnlockDiagnosticVMOptions \
     -XX:+PrintIdeal \
     -XX:PrintIdealGraphLevel=2 \
     -XX:PrintIdealGraphFile=ideal.xml \
     -jar app.jar

# 强制/排除编译特定方法
-XX:CompileCommand=compileonly,com.example.HotMethod::compute
-XX:CompileCommand=exclude,com.example.SlowMethod::*
-XX:CompileCommand=print,com.example.HotMethod::compute
```

### 10.3 编译日志格式 (PrintCompilation)

```
# 列: 时间戳 编译ID 属性 层级 方法名 (大小)
  67    1  b  3     java.lang.String::hashCode (55 bytes)
  ↑     ↑  ↑  ↑
  ms  task标志 level
         b = blocking, s = synchronized, % = OSR
         ! = has exception handler, n = native wrapper
```

---

## 11. 相关链接

- [HotSpot 模块总览](hotspot.md) — VM 整体架构
- [HotSpot GC 组件](hotspot-gc.md) — GC 实现 (C2 barrier 展开相关)
- [源码浏览](https://github.com/openjdk/jdk/tree/master/src/hotspot/share/opto)
