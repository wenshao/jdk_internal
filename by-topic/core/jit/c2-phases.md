# C2 优化阶段详解

> HotSpot C2 编译器的 15 个优化阶段完整解析

[← 返回 JIT 编译](../)

---
## 目录

1. [TL;DR 快速概览](#1-tldr-快速概览)
2. [完整编译流程](#2-完整编译流程)
3. [Phase 1: Parse Phase](#3-phase-1-parse-phase)
4. [Phase 2: PhaseIterGVN (Iterative GVN)](#4-phase-2-phaseitergvn-iterative-gvn)
5. [Phase 3: PhaseIdealLoop (循环优化)](#5-phase-3-phaseidealloop-循环优化)
6. [Phase 4: PhaseCCP (Conditional Constant Propagation)](#6-phase-4-phaseccp-conditional-constant-propagation)
7. [Phase 5: PhaseStringOpts](#7-phase-5-phasestringopts)
8. [Phase 6: PhaseEliminateNullChecks](#8-phase-6-phaseeliminatenullchecks)
9. [Phase 7 & 8: PhaseEscapeAnalysis & ScalarReplace](#9-phase-7--8-phaseescapeanalysis--scalarreplace)
10. [Phase 9: PhaseMacroExpand](#10-phase-9-phasemacroexpand)
11. [Phase 10: PhaseIterGVN (最终)](#11-phase-10-phaseitergvn-最终)
12. [Phase 11: PhaseVector (SuperWord)](#12-phase-11-phasevector-superword)
13. [Phase 12-15: 代码生成阶段](#13-phase-12-15-代码生成阶段)
14. [优化阶段顺序图](#14-优化阶段顺序图)
15. [相关链接](#15-相关链接)

---


## 1. TL;DR 快速概览

> 💡 **1 分钟了解 C2 编译阶段**

### 编译流程速览

```
字节码 → 控制流图 → 优化 → 代码生成
  ↓        ↓         ↓        ↓
Parse  PhaseIterGVN  Loop  Peephole
```

### 15 个阶段分类

| 类别 | 阶段 | 数量 |
|------|------|------|
| **分析** | Parse, CCP, Escape Analysis | 3 |
| **优化** | IterGVN, Loop, StringOpts, Vector 等 | 8 |
| **后端** | CFG, Chaitin, BlockLayout, Output | 4 |

### 关键阶段影响

| 阶段 | 优化效果 | 性能提升 |
|------|----------|----------|
| PhaseIterGVN | 消除冗余计算 | 10-30% |
| PhaseIdealLoop | 循环优化 | 20-50% |
| PhaseEscapeAnalysis | 栈上分配 | 减少 GC |
| PhaseVector | SIMD 向量化 | 2-8x |

### 快速参考

```
热点代码 → 解释器 → C1 → C2 (15 阶段) → 本地代码
                    ↑                    ↓
                  性能                  峰值性能
```

---

## 2. 完整编译流程

```
1. Parse Phase              解析字节码 → 控制流图
2. PhaseIterGVN (第一次)     全局值编号
3. PhaseIdealLoop (多轮)     循环优化
4. PhaseCCP                 条件常量传播
5. PhaseStringOpts           字符串优化
6. PhaseEliminateNullChecks  空值检查消除
7. PhaseEscapeAnalysis       逃逸分析
8. PhaseScalarReplace        标量替换
9. PhaseMacroExpand          宏扩展
10. PhaseIterGVN (最终)      最终优化
11. PhaseVector              向量化
12. PhaseCFG                 控制流图构建
13. PhaseChaitin             寄存器分配
14. PhaseBlockLayout         基本块布局
15. PhasePeephole/Output     窥孔优化/代码生成
```

---

## 3. Phase 1: Parse Phase

**作用**: 将字节码解析为 Ideal Graph

**关键操作**:
- 字节码 → Ideal 节点图
- 基础内联优化
- 初始 GVN (Global Value Numbering)

**源码位置**: `src/hotspot/share/opto/compile.cpp`

**相关类**:
- `GraphKit` - 图构建工具
- `Parse` - 字节码解析器

---

## 4. Phase 2: PhaseIterGVN (Iterative GVN)

**作用**: 全局值编号，识别和消除冗余计算

**关键优化**:
- **常量折叠**: `2 + 3` → `5`
- **公共子表达式消除**: `x + y` 复用
- **类型特化**: 基于 profiling 的类型优化

**工作原理**:
```
原始:          优化后:
a = x + y      a = x + y
b = x + y  →   b = a (复用)
c = a * 2      c = a * 2
```

**相关 Bug 修复**:
- [JDK-8347645](/by-pr/8347/8347645.md) - XOR 有界值处理阻止常量折叠 ([Johannes Graham](/by-contributor/profiles/johannes-graham.md))
- [JDK-8360035](https://bugs.openjdk.org/browse/JDK-8360035) - PhaseIterGVN 无限循环优化崩溃 (JDK 11)

**参考资料**:
- [Introduction to C2 - Part 2: GVN](https://eme64.github.io/blog/2024/12/24/Intro-to-C2-Part02.html) - [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md)

---

## 5. Phase 3: PhaseIdealLoop (循环优化)

**作用**: 循环结构分析和优化 (执行 3+ 轮)

**子优化阶段**:

### 3.1 循环识别
- 构建循环树
- 识别归纳变量
- 分析循环依赖

### 3.2 Partial Peeling (部分剥离)
```
原始:                  剥离后:
for (int i = 0;) {      if (rare) {
  if (rare) check();      check();
  body();                }
}                       for (int i = 0;) {
                          body();
                        }
```

### 3.3 Full Peeling (完全剥离)
- 完全展开循环体
- 消除循环条件判断
- 适用于小迭代次数

### 3.4 Unswitching (条件外提)
```
原始:                  外提后:
for (int i = 0;) {      if (cond) {
  if (cond) {             for (int i = 0;) { a(); }
    a();                } else {
  } else {                for (int i = 0;) { b(); }
    b();                }
  }
}
```

### 3.5 Unrolling (循环展开)
```
原始:          展开:
for (i=0;i<4;)  a[0]; a[1];
  a[i++]        a[2]; a[3];
```

### 3.6 Range Check Elimination
- 数组边界检查消除
- 基于循环分析的优化

**源码位置**: `src/hotspot/share/opto/loopnode.cpp`, `loopopts.cpp`

**参考资料**:
- [OpenJDK Wiki: Loop optimizations](https://wiki.openjdk.org/spaces/HotSpot/pages/20415918/Loop+optimizations+in+Hotspot+Server+VM+Compiler+C2)
- [Introduction to C2 - Part 4: Loop Optimizations](https://eme64.github.io/blog/2025/01/23/Intro-to-C2-Part04.html)

---

## 6. Phase 4: PhaseCCP (Conditional Constant Propagation)

**作用**: 条件常量传播

**关键优化**:
- 基于条件的常量传播
- 死分支消除
- 不可达代码移除

**示例**:
```
原始:                  优化后:
if (x > 5 && x < 10) {  if (false) {
  ...                   ...  (死代码, 移除)
}                      }
```

---

## 7. Phase 5: PhaseStringOpts

**作用**: 字符串操作优化

**关键优化**:
- 字符串拼接优化
- StringBuilder 转换
- String.substring 优化 (JDK 7u6+)

---

## 8. Phase 6: PhaseEliminateNullChecks

**作用**: 空值检查消除

**技术**:
- 基于类型的空值检查消除
- 基于控制流的空值检查消除
- 隐式空值检查 (利用硬件异常)

---

## 9. Phase 7 & 8: PhaseEscapeAnalysis & ScalarReplace

**作用**: 逃逸分析和标量替换

**逃逸分析**: 分析对象作用域
- **No Escape**: 不逃逸，可完全优化
- **Argument Escape**: 作为参数传递
- **Global Escape**: 全局逃逸，无法优化

**标量替换**: 对象字段拆分为独立变量
```java
// 原始
class Point { int x, y; }
Point p = new Point();
p.x = 1; p.y = 2;

// 标量替换后
int p_x = 1;
int p_y = 2;
// (无对象分配)
```

**栈上分配**: 不逃逸对象分配在栈上
- 自动回收 (无 GC)
- 更好的缓存局部性

**相关 PR 分析**:
| Issue | 标题 | 作者 | 说明 |
|-------|------|------|------|
| [JDK-8370405](/by-pr/8370/8370405.md) | MergeStores 在分配消除中被错误标量替换 | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | 逃逸分析 + MergeStore 交互 bug |
| [JDK-8357913](/by-pr/8357/8357913.md) | StringCoding 添加 @Stable 注解 | [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | 启用标量替换和循环展开 |
| [JDK-8357690](/by-pr/8357/8357690.md) | CharacterDataLatin1 添加 @Stable 注解 | [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | 启用标量替换优化 |
| [JDK-8368172](/by-pr/8368/8368172.md) | DateTimePrintContext 不可变对象优化 | [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | JIT 逃逸分析优化 (+6-10%) |

**参考资料**:
- [HotSpot Escape Analysis Status](https://cr.openjdk.org/~cslucas/escape-analysis/EscapeAnalysis.html)
- [JDConf 2024: Improving HotSpot Scalar Replacement](https://jdconf.com/2024/downloads/JDConf%20202024-Improving%20HotSpot%20Scalar%20Replacement-Soares.pdf)

---

## 10. Phase 9: PhaseMacroExpand

**作用**: 宏节点扩展

**关键操作**:
- 锁消除 (Lock Elision)
- 锁粗化 (Lock Coarsening)
- 原子操作优化
- Unsafe 操作内联

---

## 11. Phase 10: PhaseIterGVN (最终)

**作用**: 最终优化遍历

**与第一次 IGVN 的区别**:
- 基于前面优化的结果
- 更激进的优化
- 准备代码生成

---

## 12. Phase 11: PhaseVector (SuperWord)

**作用**: SIMD 向量化优化

**向量化转换**:
```java
// 原始标量代码
for (int i = 0; i < 1024; i++) {
  a[i] = b[i] + c[i];
}

// 向量化后 (伪代码)
for (int i = 0; i < 1024; i += 16) {
  vector a = load(&b[i]);      // SIMD 加载 16 个元素
  vector b = load(&c[i]);
  vector result = a + b;        // SIMD 加法
  store(&a[i], result);         // SIMD 存储
}
```

**相关 PR 分析**:
| Issue | 标题 | 作者 | 说明 |
|-------|------|------|------|
| [JDK-8340093](/by-pr/8340/8340093.md) | SuperWord 成本模型实现 | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | 智能判断向量化收益 |
| [JDK-8332163](/by-pr/8332/8332163.md) | SuperWord VTransformGraph 重构 | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | 架构重构，为成本模型奠定基础 |
| [JDK-8371146](/by-pr/8371/8371146.md) | C2 SuperWord 向量化优化 | [Hamlin Li](/by-contributor/profiles/hamlin-li.md) | 修复多个关键 bug |
| [JDK-8334431](/by-pr/8333/8334431.md) | 修复 SuperWord Store-to-Load 转发失败 | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | 性能回归修复 |
| [JDK-8344085](/by-pr/8344/8344085.md) | 改进小循环迭代计数的 SuperWord 向量化 | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | 小循环优化 |
| [JDK-8328938](https://bugs.openjdk.org/browse/JDK-8328938) | SuperWord 大步长禁用 | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | 算法边界修复 |
| [JDK-8324890](/by-pr/8324/8324890.md) | SuperWord VLoop 分析器重构 | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | 架构改进 |
| [JDK-8333713](/by-pr/8333/8333713.md) | SuperWord 清理重命名 | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | 代码质量 |

**相关参数**:
```bash
-XX:+UseSuperWord                 # 启用向量化
-XX:MaxVectorSize=32               # 最大向量大小
-XX:+TraceSuperWord               # 跟踪向量化决策
```

---

## 13. Phase 12-15: 代码生成阶段

### Phase 12: PhaseCFG
**作用**: 构建控制流图

### Phase 13: PhaseChaitin
**作用**: 寄存器分配 (图着色算法)
- 构建干涉图
- 图着色分配寄存器
- Spilling (溢出到栈)

### Phase 14: PhaseBlockLayout
**作用**: 基本块布局优化
- 热路径连续
- 减少跳转

### Phase 15: PhasePeephole / PhaseOutput
**作用**: 窥孔优化和机器码生成
- 局部模式匹配优化
- 生成最终机器码

---

## 14. 优化阶段顺序图

```
Parse
   │
   ├─────────────────────────────────────────┐
   │                                         │
   ▼                                         ▼
Inline                                Initial GVN
   │                                         │
   ▼                                         │
PhaseIterGVN ◄──────────────────────────────┘
   │
   ▼
PhaseIdealLoop (多轮迭代)
   │
   ├─► Loop 1: Partial Peeling
   ├─► Loop 2: Full Peeling
   ├─► Loop 3: Unswitching
   └─► Loop 4+: Unrolling
   │
   ▼
PhaseCCP
   │
   ▼
PhaseStringOpts ──► PhaseEliminateNullChecks
   │
   ▼
PhaseEscapeAnalysis ──► PhaseScalarReplace
   │
   ▼
PhaseMacroExpand
   │
   ▼
PhaseIterGVN (最终)
   │
   ▼
PhaseVector (SuperWord)
   │
   ▼
PhaseCFG ──► PhaseChaitin ──► PhaseBlockLayout ──► Output
```

---

## 15. 相关链接

### 本地文档

- [VM 参数](vm-parameters.md) - 编译器参数配置
- [诊断工具](diagnostics.md) - 如何观察优化阶段
- [SuperWord 向量化](superword.md) - SuperWord 专题
- [Graal JIT](graal-jit.md) - Graal 编译器对比
- [Graal vs C2 性能对比](graal-vs-c2-performance.md) - 性能基准测试

### 贡献者

| 贡献者 | 领域 | 组织 |
|--------|------|------|
| [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | C2 SuperWord 向量化、C2 博客作者 | Oracle |
| [Johannes Graham](/by-contributor/profiles/johannes-graham.md) | C2 编译器优化、常量折叠 | Oracle |
| [Vladimir Kozlov](/by-contributor/profiles/vladimir-kozlov.md) | C2 编译器创始人 | Oracle |
| [Christian Hagedorn](/by-contributor/profiles/christian-hagedorn.md) | C2 优化、GVN | Oracle |
| [Roland Westrelin](/by-contributor/profiles/roland-westrelin.md) | C2 循环优化 | Red Hat |
| [John Rose](/by-contributor/profiles/john-rose.md) | invokedynamic、JIT | Oracle |

### 外部资源

- [Emanuel's C2 Blog](https://eme64.github.io/blog/) - [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) 的详细技术分析
  - [Introduction to C2 - Part 1: Overview](https://eme64.github.io/blog/2024/12/06/Intro-to-C2-Part01.html)

---

**最后更新**: 2026-03-21
  - [Introduction to C2 - Part 2: GVN](https://eme64.github.io/blog/2024/12/24/Intro-to-C2-Part02.html)
  - [Introduction to C2 - Part 3: Inlining](https://eme64.github.io/blog/2024/12/31/Intro-to-C2-Part03.html)
  - [Introduction to C2 - Part 4: Loop Optimizations](https://eme64.github.io/blog/2025/01/23/Intro-to-C2-Part04.html)
- [OpenJDK Wiki: Loop optimizations](https://wiki.openjdk.org/spaces/HotSpot/pages/20415918/Loop+optimizations+in+Hotspot+Server+VM+Compiler+C2)
- [HotSpot Escape Analysis Status](https://cr.openjdk.org/~cslucas/escape-analysis/EscapeAnalysis.html)
