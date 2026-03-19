# Emanuel Peter

## Basic Information

| Field | Value |
|-------|-------|
| **Name** | Emanuel Peter |
| **Email** | epeter@openjdk.org |
| **Organization** | Oracle |
| **JDK 26 Commits** | 52 |
| **Primary Areas** | C2 Compiler, SuperWord Auto-Vectorization, Template Testing Framework |

## Contribution Overview

Emanuel Peter is a core contributor to the HotSpot C2 compiler, specializing in SuperWord auto-vectorization. His work in JDK 26 represents a major evolution of the vectorization infrastructure, introducing a new cost model, aliasing analysis, and the innovative Template-Based Testing Framework.

### Contribution Categories

| Category | Count | Description |
|----------|-------|-------------|
| C2 SuperWord | 35 | Auto-vectorization improvements |
| Template Framework | 6 | New testing infrastructure |
| C2 Core | 8 | Compiler infrastructure fixes |
| Test Fixes | 3 | Test stability improvements |

## Complete PR List

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

## Key Contributions

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

## Development Style

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

## Related Links

- [OpenJDK Profile](https://openjdk.org/census#epeter)
- [JBS Issues by Emanuel Peter](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20epeter)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=epeter@openjdk.org)
- [JVMLS 2025 NormalMapping Demo](https://openjdk.org/projects/jvmls)

## Technical Notes

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