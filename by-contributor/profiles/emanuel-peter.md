# Emanuel Peter

> **GitHub**: [@eme64](https://github.com/eme64)
> **OpenJDK**: [@epeter](https://openjdk.org/census#epeter)
> **Location**: Zürich / Thun, Switzerland
> **Organization**: Oracle (Java Platform Group)

---
## 目录

1. [概述](#1-概述)
2. [主要贡献](#2-主要贡献)
3. [Basic Information](#3-basic-information)
4. [Career Timeline](#4-career-timeline)
5. [Blog Posts](#5-blog-posts)
6. [Contribution Overview](#6-contribution-overview)
7. [Complete PR List](#7-complete-pr-list)
8. [Key Contributions](#8-key-contributions)
9. [Development Style](#9-development-style)
10. [Related Links](#10-related-links)
11. [Technical Notes](#11-technical-notes)

---


## 1. 概述

Emanuel Peter 是 Oracle 的 C2 编译器工程师，专注于 SuperWord 自动向量化优化。他在 JDK 26 中的工作代表了向量化基础设施的重大演进，引入了新的成本模型、别名分析系统和创新的基于模板的测试框架。

---

## 2. 主要贡献

### JDK 26 (2025-2026)

| PR/Issue | 标题 | 角色 |
|----------|------|------|
| [JDK-8334431](../../by-pr/8333/8334431.md) | 修复 SuperWord Store-to-Load 转发失败导致的性能回归 | Author |
| [JDK-8344085](../../by-pr/8344/8344085.md) | 改进小循环迭代计数的 SuperWord 向量化 | Author |

### 核心优化领域

| 领域 | 说明 |
|------|------|
| **SuperWord 向量化** | 自动向量化优化、成本模型、别名分析 |
| **C2 编译器** | IR 节点操作、循环优化 |
| **测试框架** | Template-Based Testing Framework |

---

## 3. Basic Information

| Field | Value |
|-------|-------|
| **Name** | Emanuel Peter |
| **Current Organization** | Oracle (Java Platform Group) |
| **Position** | Compiler Engineer, HotSpot JVM Compiler Team |
| **Location** | Zürich / Thun, Switzerland |
| **Education** | ETH Zürich |
| **GitHub** | [@eme64](https://github.com/eme64) |
| **LinkedIn** | [Emanuel Peter](https://ch.linkedin.com/in/emanuel-peter-4286a2207) |
| **Blog** | [Emanuel's Hotspot JVM C2 Blog](https://eme64.github.io/blog/) |
| **OpenJDK** | [@epeter](https://openjdk.org/census#epeter) |
| **Role** | JDK Committer (2022-05), JDK Reviewer (2023-05) |
| **PRs** | [226+ integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Aeme64+is%3Aclosed+label%3Aintegrated) |
| **Primary Areas** | C2 Compiler, SuperWord Auto-Vectorization, Template Testing Framework |

> **数据来源**: [LinkedIn](https://ch.linkedin.com/in/emanuel-peter-4286a2207), [GitHub](https://github.com/eme64), [个人博客](https://eme64.github.io/blog/), [CFV Committer](https://mail.openjdk.org/pipermail/jdk-dev/2022-May/007238.html), [CFV Reviewer](https://mail.openjdk.org/pipermail/jdk-dev/2023-May/008085.html)

---

## 4. Career Timeline

| Year | Event | Details |
|------|-------|---------|
| **Education** | ETH Zürich | Computer Science education at Swiss Federal Institute of Technology |
| **~2020** | Joined Oracle | HotSpot JVM Compiler Team |
| **2022-05** | JDK Committer | Nominated by Tobias Hartmann, CFV approved |
| **2023-02** | Blog Started | First SuperWord article published |
| **2023-05** | JDK Reviewer | Nominated by Andrew Dinn (Red Hat), CFV approved |
| **2023-2025** | Major Contributions | VTransform refactoring, Template Framework, Cost Model |
| **2024-2025** | Blog Series | Introduction to HotSpot JVM C2 JIT Compiler (Parts 0-4) |
| **2025-08** | JVMLS 2025 | SuperWord NormalMapping demo presentation |

---

## 5. Blog Posts

Emanuel Peter maintains an excellent technical blog about C2 compiler internals:

| Date | Title | Topic | Link |
|------|-------|-------|------|
| 2025-01-23 | Introduction to HotSpot JVM C2 JIT Compiler, Part 4 | C2 Compiler | [Blog](https://eme64.github.io/blog/2025/01/23/Intro-to-C2-Part-4.html) |
| 2025-01-23 | Introduction to HotSpot JVM C2 JIT Compiler, Part 3 | C2 Compiler | [Blog](https://eme64.github.io/blog/2025/01/23/Intro-to-C2-Part-3.html) |
| 2025-01-01 | AutoVectorization (SuperWord) Status | SuperWord | [Blog](https://eme64.github.io/blog/2025/01/01/SuperWord-Status.html) |
| 2024-12-24 | Introduction to HotSpot JVM C2 JIT Compiler, Part 2 | C2 Compiler | [Blog](https://eme64.github.io/blog/2024/12/24/Intro-to-C2-Part-2.html) |
| 2024-12-24 | Introduction to HotSpot JVM C2 JIT Compiler, Part 1 | C2 Compiler | [Blog](https://eme64.github.io/blog/2024/12/24/Intro-to-C2-Part-1.html) |
| 2024-12-24 | Introduction to HotSpot JVM C2 JIT Compiler, Part 0 | C2 Compiler | [Blog](https://eme64.github.io/blog/2024/12/24/Intro-to-C2-Part-0.html) |
| 2024-06-24 | Auto-Vectorization and Store-to-Load-Forwarding | SuperWord | [Blog](https://eme64.github.io/blog/2024/06/24/store-to-load-forwarding.html) |
| 2023-11-03 | C2 AutoVectorizer Improvement Ideas | SuperWord | [Blog](https://eme64.github.io/blog/2023/11/03/AutoVectorizer-Ideas.html) |
| 2023-05-16 | SuperWord (Auto-Vectorization) - Scheduling | SuperWord | [Blog](https://eme64.github.io/blog/2023/05/16/SuperWord-Scheduling.html) |
| 2023-02-23 | SuperWord (Auto-Vectorization) - An Introduction | SuperWord | [Blog](https://eme64.github.io/blog/2023/02/23/SuperWord-Introduction.html) |

### Blog Description
*"This blog focuses on my work I do in the C2 compiler of the HotSpot JVM. I currently work at Oracle as an OpenJDK compiler engineer. The views expressed on this blog are my own and do not necessarily reflect the views of my employer."*

---

## 6. Contribution Overview

Emanuel Peter is a core contributor to the HotSpot C2 compiler, specializing in SuperWord auto-vectorization. His work in JDK 26 represents a major evolution of the vectorization infrastructure, introducing a new cost model, aliasing analysis, and the innovative Template-Based Testing Framework.

### Contribution Categories

| Category | Count | Description |
|----------|-------|-------------|
| C2 SuperWord | 35 | Auto-vectorization improvements |
| Template Framework | 6 | New testing infrastructure |
| C2 Core | 8 | Compiler infrastructure fixes |
| Test Fixes | 3 | Test stability improvements |

## 7. Complete PR List

| Issue | Title | PR Link |
|-------|-------|---------|
| JDK-8323582 | C2 SuperWord AlignVector: misaligned vector memory access with unaligned native memory | [JBS](https://bugs.openjdk.org/browse/JDK-8323582) |
| JDK-8324751 | C2 SuperWord: Aliasing Analysis runtime check | [JBS](https://bugs.openjdk.org/browse/JDK-8324751) |
| JDK-8335747 | C2: fix overflow case for LoopLimit with constant inputs | [JBS](https://bugs.openjdk.org/browse/JDK-8335747) |
| JDK-8340093 | C2 SuperWord: implement cost model | [JBS](https://bugs.openjdk.org/browse/JDK-8340093) |
| JDK-8343685 | C2 SuperWord: refactor VPointer with MemPointer | [JBS](https://bugs.openjdk.org/browse/JDK-8343685) |
| JDK-8344942 | Template-Based Testing Framework | [JBS](https://bugs.openjdk.org/browse/JDK-8344942) |
| JDK-8346106 | Verify.checkEQ: testing utility for recursive value verification | [JBS](https://bugs.openjdk.org/browse/JDK-8346106) |
| JDK-8346993 | C2 SuperWord: refactor to make more vector nodes available in VectorNode::make | [JBS](https://bugs.openjdk.org/browse/JDK-8346993) |
| JDK-8347273 | C2: VerifyIterativeGVN for Ideal and Identity | [JBS](https://bugs.openjdk.org/browse/JDK-8347273) |
| JDK-8348263 | C2 SuperWord: TestMemorySegment.java has failing IR rules with AlignVector after JDK-8343685 | [JBS](https://bugs.openjdk.org/browse/JDK-8348263) |
| JDK-8348572 | C2 compilation asserts due to unexpected irreducible loop | [JBS](https://bugs.openjdk.org/browse/JDK-8348572) |
| JDK-8348657 | compiler/loopopts/superword/TestEquivalentInvariants.java timed out | [JBS](https://bugs.openjdk.org/browse/JDK-8348657) |
| JDK-8350756 | C2 SuperWord Multiversioning: remove useless slow loop when the fast loop disappears | [JBS](https://bugs.openjdk.org/browse/JDK-8350756) |
| JDK-8350841 | ProblemList jdk/incubator/vector/Long256VectorTests.java | [JBS](https://bugs.openjdk.org/browse/JDK-8350841) |
| JDK-8351392 | C2 crash: failed: Expected Bool, but got OpaqueMultiversioning | [JBS](https://bugs.openjdk.org/browse/JDK-8351392) |
| JDK-8351414 | C2: MergeStores must happen after RangeCheck smearing | [JBS](https://bugs.openjdk.org/browse/JDK-8351414) |
| JDK-8351952 | [IR Framework]: allow ignoring methods that are not compilable | [JBS](https://bugs.openjdk.org/browse/JDK-8351952) |
| JDK-8352020 | [CompileFramework] enable compilation for VectorAPI | [JBS](https://bugs.openjdk.org/browse/JDK-8352020) |
| JDK-8352587 | C2 SuperWord: we must avoid Multiversioning for PeelMainPost loops | [JBS](https://bugs.openjdk.org/browse/JDK-8352587) |
| JDK-8352597 | [IR Framework] test bug: TestNotCompilable.java fails on product build | [JBS](https://bugs.openjdk.org/browse/JDK-8352597) |
| JDK-8352869 | Verify.checkEQ: extension for NaN, VectorAPI and arbitrary Objects | [JBS](https://bugs.openjdk.org/browse/JDK-8352869) |
| JDK-8354477 | C2 SuperWord: make use of memory edges more explicit | [JBS](https://bugs.openjdk.org/browse/JDK-8354477) |
| JDK-8355094 | Performance drop in auto-vectorized kernel due to split store | [JBS](https://bugs.openjdk.org/browse/JDK-8355094) |
| JDK-8357530 | C2 SuperWord: Diagnostic flag AutoVectorizationOverrideProfitability | [JBS](https://bugs.openjdk.org/browse/JDK-8357530) |
| JDK-8358600 | Template-Framework Library: Template for TestFramework test class | [JBS](https://bugs.openjdk.org/browse/JDK-8358600) |
| JDK-8358772 | Template-Framework Library: Primitive Types | [JBS](https://bugs.openjdk.org/browse/JDK-8358772) |
| JDK-8359412 | Template-Framework Library: Operations and Expressions | [JBS](https://bugs.openjdk.org/browse/JDK-8359412) |
| JDK-8366357 | C2 SuperWord: refactor VTransformNode::apply with VTransformApplyState | [JBS](https://bugs.openjdk.org/browse/JDK-8366357) |
| JDK-8366361 | C2 SuperWord: rename VTransformNode::set_req -> init_req, analogue to Node::init_req | [JBS](https://bugs.openjdk.org/browse/JDK-8366361) |
| JDK-8366427 | C2 SuperWord: refactor VTransform scalar nodes | [JBS](https://bugs.openjdk.org/browse/JDK-8366427) |
| JDK-8366490 | C2 SuperWord: wrong result because CastP2X is missing ctrl and floats over SafePoint creating stale oops | [JBS](https://bugs.openjdk.org/browse/JDK-8366490) |
| JDK-8366702 | C2 SuperWord: refactor VTransform vector nodes | [JBS](https://bugs.openjdk.org/browse/JDK-8366702) |
| JDK-8366845 | C2 SuperWord: wrong VectorCast after VectorReinterpret with swapped src/dst type | [JBS](https://bugs.openjdk.org/browse/JDK-8366845) |
| JDK-8366940 | Test compiler/loopopts/superword/TestAliasingFuzzer.java timed out | [JBS](https://bugs.openjdk.org/browse/JDK-8366940) |
| JDK-8367243 | Format issues with dist dump debug output in PhaseGVN::dead_loop_check | [JBS](https://bugs.openjdk.org/browse/JDK-8367243) |
| JDK-8367389 | C2 SuperWord: refactor VTransform to model the whole loop instead of just the basic block | [JBS](https://bugs.openjdk.org/browse/JDK-8367389) |
| JDK-8367483 | C2 crash in PhaseValues::type: assert(t != nullptr) failed: must set before get | [JBS](https://bugs.openjdk.org/browse/JDK-8367483) |
| JDK-8367531 | Template Framework: use scopes and tokens instead of misbehaving immediate-return-queries | [JBS](https://bugs.openjdk.org/browse/JDK-8367531) |
| JDK-8367657 | C2 SuperWord: NormalMapping demo from JVMLS 2025 | [JBS](https://bugs.openjdk.org/browse/JDK-8367657) |
| JDK-8367969 | C2: compiler/vectorapi/TestVectorMathLib.java fails without UnlockDiagnosticVMOptions | [JBS](https://bugs.openjdk.org/browse/JDK-8367969) |
| JDK-8369448 | C2 SuperWord: refactor VTransform to do move_unordered_reduction_out_of_loop during VTransform::optimize | [JBS](https://bugs.openjdk.org/browse/JDK-8369448) |
| JDK-8369804 | TestGenerators.java fails with IllegalArgumentException: bound must be greater than origin | [JBS](https://bugs.openjdk.org/browse/JDK-8369804) |
| JDK-8369881 | C2: Unexpected node in SuperWord truncation: ReverseBytesS, ReverseBytesUS | [JBS](https://bugs.openjdk.org/browse/JDK-8369881) |
| JDK-8369898 | C2 SuperWord: assert(has_ctrl(i)) failed: should be control, not loop | [JBS](https://bugs.openjdk.org/browse/JDK-8369898) |
| JDK-8369902 | C2 SuperWord: wrong result because filtering NaN instead of zero in MemPointerParser::canonicalize_raw_summands | [JBS](https://bugs.openjdk.org/browse/JDK-8369902) |
| JDK-8370220 | C2: rename methods and improve documentation around get_ctrl and idom lazy updating/forwarding | [JBS](https://bugs.openjdk.org/browse/JDK-8370220) |
| JDK-8370332 | C2 SuperWord: SIGSEGV because PhaseIdealLoop::split_thru_phi left dead nodes in loop _body | [JBS](https://bugs.openjdk.org/browse/JDK-8370332) |
| JDK-8370405 | C2: mismatched store from MergeStores wrongly scalarized in allocation elimination | [JBS](https://bugs.openjdk.org/browse/JDK-8370405) |
| JDK-8370459 | C2: CompressBitsNode::Value produces wrong result on Windows (1UL vs 1ULL) | [JBS](https://bugs.openjdk.org/browse/JDK-8370459) |
| JDK-8371065 | C2 SuperWord: VTransformLoopPhiNode::apply setting type leads to assert/wrong result | [JBS](https://bugs.openjdk.org/browse/JDK-8371065) |
| JDK-8371146 | C2 SuperWord: VTransform::add_speculative_check uses pre_init that is pinned after Auto_Vectorization_Check | [JBS](https://bugs.openjdk.org/browse/JDK-8371146) |

## 8. Key Contributions

### 1. C2 SuperWord Cost Model (JDK-8340093)

This is a landmark contribution that implements a cost model for auto-vectorization decisions. The cost model helps determine whether vectorization is actually profitable for a given loop.

**Key Code Structure (vtransform.hpp):**

```cpp
// VTransform:
// - Models the transformation of the scalar loop to vectorized loop:
//   It is a "C2 subgraph" -> "C2 subgraph" mapping.
// - The VTransform contains a graph (VTransformGraph), which consists of
//   many vtnodes (VTransformNode).
// - Each vtnode models a part of the transformation, and is supposed
//   to represent the output C2 nodes after the vectorization as closely
//   as possible.
//
// This is the life-cycle of a VTransform:
// - Construction:
//   - From SuperWord PackSet, with the SuperWordVTransformBuilder.
//
// - Optimize:
//   - Move non-strict order reductions out of the loop.
//
// - Schedule:
//   - Compute linearization of the VTransformGraph.
//
// - Cost-Model:
//   - We use a cost-model as a heuristic to determine if vectorization 
//     is profitable. Compute the cost of the loop with and without 
//     vectorization.
//
// - Apply:
//   - Changes to the C2 IR are only made once the "apply" method is called.
```

**Impact:** 13 files changed, 2884 insertions(+), 94 deletions(-)

### 2. Aliasing Analysis Runtime Check (JDK-8324751)

Implemented a sophisticated aliasing analysis system with runtime checks for memory access patterns in vectorized loops.

**Key Files Modified:**
- `src/hotspot/share/opto/mempointer.cpp` - Memory pointer analysis
- `src/hotspot/share/opto/vectorization.cpp` - Vectorization infrastructure
- `src/hotspot/share/opto/vtransform.cpp` - Transform implementation

**Impact:** 22 files changed, 3000+ insertions

### 3. Template-Based Testing Framework (JDK-8344942)

Created a new testing infrastructure that enables more comprehensive and maintainable compiler tests.

**Key Components:**
- Template-Framework Library: Primitive Types (JDK-8358772)
- Template-Framework Library: Operations and Expressions (JDK-8359412)
- Template-Framework Library: Template for TestFramework test class (JDK-8358600)

### 4. VTransform Refactoring Series

A major refactoring effort to improve the VTransform infrastructure:

| Issue | Description |
|-------|-------------|
| JDK-8366357 | VTransformNode::apply with VTransformApplyState |
| JDK-8366427 | Refactor VTransform scalar nodes |
| JDK-8366702 | Refactor VTransform vector nodes |
| JDK-8367389 | Model the whole loop instead of just the basic block |
| JDK-8369448 | Move unordered reduction out of loop during optimize |

## 9. Development Style

### Code Quality Focus

Emanuel Peter's development style emphasizes:

1. **Incremental Refactoring**: Large features are broken into manageable, reviewable chunks
2. **Comprehensive Testing**: Each change includes extensive test coverage
3. **Documentation**: Clear comments explaining the "why" behind design decisions
4. **Defensive Programming**: Assertions and verification steps throughout

### Commit Pattern Analysis

```
Typical commit structure:
- Clear JBS issue reference in title
- Detailed description of the problem and solution
- Reviewed-by: typically kvn (Vladimir Kozlov), qamai, mhaessig
- Focus on one logical change per commit
```

### Key Technical Areas

1. **SuperWord Vectorization**: Core expertise in auto-vectorization algorithms
2. **C2 IR Manipulation**: Deep understanding of C2 intermediate representation
3. **Memory Alias Analysis**: Sophisticated memory access pattern analysis
4. **Testing Infrastructure**: Building maintainable test frameworks

## 10. Related Links

- [OpenJDK Profile](https://openjdk.org/census#epeter)
- [JBS Issues by Emanuel Peter](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20epeter)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=epeter@openjdk.org)
- [JVMLS 2025 NormalMapping Demo](https://openjdk.org/projects/jvmls)

## 11. Technical Notes

### VTransform Architecture

The VTransform system represents a significant architectural improvement in how SuperWord handles vectorization:

```
Scalar Loop -> VTransform Graph -> Cost Model -> Apply -> Vectorized Loop
                    |
                    v
              VTransformNode
              /    |    \
        Scalar  Vector  CFG
```

### Cost Model Heuristics

The cost model considers:
- Vector width and lane count
- Memory access patterns
- Operation types (load/store, arithmetic, reduction)
- Alignment requirements
- Loop trip count estimates

---

> **文档版本**: 2.0
> **最后更新**: 2026-03-22
> **更新内容**:
> - 修正位置为 Zürich / Thun (GitHub 验证)
> - 添加 JVMLS 2025 演讲 (NormalMapping demo)
> - 验证 Oracle 组织、ETH Zürich 教育背景、GitHub (@eme64) 信息

## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 445 |
| **活跃仓库数** | 3 |
