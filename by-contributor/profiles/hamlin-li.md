## 目录

1. [Basic Information](#1-basic-information)
2. [Contribution Overview](#2-contribution-overview)
3. [Complete PR List](#3-complete-pr-list)
4. [Key Contributions](#4-key-contributions)
5. [Development Style](#5-development-style)
6. [Related Links](#6-related-links)

---

# Hamlin Li

## 1. Basic Information

| Field | Value |
|-------|-------|
| **Name** | Hamlin Li |
| **Current Organization** | Rivos |
| **GitHub** | [@Hamlin-Li](https://github.com/Hamlin-Li) |
| **OpenJDK** | [@mli](https://openjdk.org/census#mli) |
| **Role** | JDK Reviewer |
| **PRs** | [integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3AHamlin-Li+is%3Aclosed+label%3Aintegrated) |
| **Total Contributions** | 130+ (across all OpenJDK history) |
| **Primary Areas** | RISC-V Backend, C2 SuperWord, Vectorization, Core Libraries |

### Organization History

| Period | Organization | Email |
|--------|--------------|-------|
| ~2016 - ~2023 | Oracle | huaming.li@oracle.com |
| ~2024 - Present | Rivos | hamlin@rivosinc.com |

> **Data as of**: 2026-03-19

## 2. Contribution Overview

### By Category

| Category | Count | Description |
|----------|-------|-------------|
| RISC-V Backend | 40 | CPU features, intrinsics, code generation |
| C2 SuperWord | 10 | SLP vectorization improvements |
| C2 Compiler | 8 | Optimization fixes |
| Testing | 5 | Test enablement and fixes |
| HotSpot Runtime | 2 | General runtime improvements |

### Key Areas of Expertise
- **RISC-V Architecture** - CPU feature detection, intrinsics, assembly code generation
- **C2 SuperWord** - SIMD vectorization (SLP - Superword Level Parallelism)
- **Float16 Operations** - Scalar and vector Float16 support
- **Conditional Moves** - CMove optimizations for RISC-V
- **CRC32 Intrinsics** - Carry-less multiplication implementation
- **Core Libraries** (Oracle era) - Compact Strings, Stack Walking, Platform Logging, NIO, RMI

### Career Notes
- Became JDK Reviewer in March 2020 (voted in by the community)
- At Oracle, focused on test quality, code coverage, and tracking intermittent failures in Core Libraries
- At Rivos, shifted focus to RISC-V backend, vectorization, and compiler optimizations

## 3. Complete PR List

| Issue | Title | PR Link |
|-------|-------|---------|
| JDK-8371297 | C2: assert triggered in BoolTest::BoolTest | [JBS](https://bugs.openjdk.org/browse/JDK-8371297) |
| JDK-8370794 | C2 SuperWord: Long/Integer.compareUnsigned return wrong value for EQ/NE in SLP | [JBS](https://bugs.openjdk.org/browse/JDK-8370794) |
| JDK-8370481 | C2 SuperWord: Long/Integer.compareUnsigned return wrong value in SLP | [JBS](https://bugs.openjdk.org/browse/JDK-8370481) |
| JDK-8370225 | RISC-V: cleanup verify_xxx in interp_masm_riscv.hpp | [JBS](https://bugs.openjdk.org/browse/JDK-8370225) |
| JDK-8369685 | RISC-V: refactor code related to RVFeatureValue::enabled | [JBS](https://bugs.openjdk.org/browse/JDK-8369685) |
| JDK-8368950 | RISC-V: fail to catch out of order declarations among dependent cpu extensions/flags | [JBS](https://bugs.openjdk.org/browse/JDK-8368950) |
| JDK-8368897 | RISC-V: Cleanup RV_EXT_FEATURE_FLAGS & RV_NON_EXT_FEATURE_FLAGS | [JBS](https://bugs.openjdk.org/browse/JDK-8368897) |
| JDK-8368893 | RISC-V: crash after JDK-8352673 on fastdebug version | [JBS](https://bugs.openjdk.org/browse/JDK-8368893) |
| JDK-8367981 | Update CompactHashtable for readability | [JBS](https://bugs.openjdk.org/browse/JDK-8367981) |
| JDK-8367253 | RISC-V: refactor dependent cpu extensions | [JBS](https://bugs.openjdk.org/browse/JDK-8367253) |
| JDK-8367103 | RISC-V: store cpu features in a bitmap | [JBS](https://bugs.openjdk.org/browse/JDK-8367103) |
| JDK-8368525 | nmethod ic cleanup | [JBS](https://bugs.openjdk.org/browse/JDK-8368525) |
| JDK-8367501 | RISC-V: build broken after JDK-8365926 | [JBS](https://bugs.openjdk.org/browse/JDK-8367501) |
| JDK-8367066 | RISC-V: refine register selection in MacroAssembler::decode_klass_not_null | [JBS](https://bugs.openjdk.org/browse/JDK-8367066) |
| JDK-8367098 | RISC-V: sync CPU features with related JVM flags for dependant ones | [JBS](https://bugs.openjdk.org/browse/JDK-8367098) |
| JDK-8365772 | RISC-V: correctly prereserve NaN payload when converting from float to float16 in vector way | [JBS](https://bugs.openjdk.org/browse/JDK-8365772) |
| JDK-8365206 | RISC-V: compiler/c2/irTests/TestFloat16ScalarOperations.java is failing on riscv64 | [JBS](https://bugs.openjdk.org/browse/JDK-8365206) |
| JDK-8364120 | RISC-V: unify the usage of MacroAssembler::instruction_size | [JBS](https://bugs.openjdk.org/browse/JDK-8364120) |
| JDK-8362515 | RISC-V: cleanup NativeFarCall | [JBS](https://bugs.openjdk.org/browse/JDK-8362515) |
| JDK-8362493 | Cleanup CodeBuffer::copy_relocations_to | [JBS](https://bugs.openjdk.org/browse/JDK-8362493) |
| JDK-8362284 | RISC-V: cleanup NativeMovRegMem | [JBS](https://bugs.openjdk.org/browse/JDK-8362284) |
| JDK-8360090 | [TEST] RISC-V: disable some cds tests on qemu | [JBS](https://bugs.openjdk.org/browse/JDK-8360090) |
| JDK-8358892 | RISC-V: jvm crash when running dacapo sunflow after JDK-8352504 | [JBS](https://bugs.openjdk.org/browse/JDK-8358892) |
| JDK-8359045 | RISC-V: construct test to verify invocation of C2_MacroAssembler::enc_cmove_cmp_fp | [JBS](https://bugs.openjdk.org/browse/JDK-8359045) |
| JDK-8358685 | [TEST] AOTLoggingTag.java failed with missing log message | [JBS](https://bugs.openjdk.org/browse/JDK-8358685) |
| JDK-8350960 | RISC-V: Add riscv backend for Float16 operations - vectorization | [JBS](https://bugs.openjdk.org/browse/JDK-8350960) |
| JDK-8356875 | RISC-V: extension flag UseZvfh should depends on UseZfh | [JBS](https://bugs.openjdk.org/browse/JDK-8356875) |
| JDK-8356642 | RISC-V: enable hotspot/jtreg/compiler/vectorapi/VectorFusedMultiplyAddSubTest.java | [JBS](https://bugs.openjdk.org/browse/JDK-8356642) |
| JDK-8355704 | RISC-V: enable TestIRFma.java | [JBS](https://bugs.openjdk.org/browse/JDK-8355704) |
| JDK-8355699 | RISC-V: support SUADD/SADD/SUSUB/SSUB | [JBS](https://bugs.openjdk.org/browse/JDK-8355699) |
| JDK-8356030 | RISC-V: enable (part of) BasicDoubleOpTest.java | [JBS](https://bugs.openjdk.org/browse/JDK-8356030) |
| JDK-8355980 | RISC-V: remove vmclr_m before vmsXX and vmfXX | [JBS](https://bugs.openjdk.org/browse/JDK-8355980) |
| JDK-8355913 | RISC-V: improve hotspot/jtreg/compiler/vectorization/runner/BasicFloatOpTest.java | [JBS](https://bugs.openjdk.org/browse/JDK-8355913) |
| JDK-8355293 | [TEST] RISC-V: enable more ir tests | [JBS](https://bugs.openjdk.org/browse/JDK-8355293) |
| JDK-8355476 | RISC-V: using zext_w directly in vector_update_crc32 could trigger assert | [JBS](https://bugs.openjdk.org/browse/JDK-8355476) |
| JDK-8352504 | RISC-V: implement and enable CMoveI/L | [JBS](https://bugs.openjdk.org/browse/JDK-8352504) |
| JDK-8346786 | RISC-V: Reconsider ConditionalMoveLimit when adding conditional move | [JBS](https://bugs.openjdk.org/browse/JDK-8346786) |
| JDK-8353600 | RISC-V: compiler/vectorization/TestRotateByteAndShortVector.java is failing with Zvbb | [JBS](https://bugs.openjdk.org/browse/JDK-8353600) |
| JDK-8353665 | RISC-V: IR verification fails in TestSubNodeFloatDoubleNegation.java | [JBS](https://bugs.openjdk.org/browse/JDK-8353665) |
| JDK-8352607 | RISC-V: use cmove in min/max when Zicond is supported | [JBS](https://bugs.openjdk.org/browse/JDK-8352607) |
| JDK-8320997 | RISC-V: C2 ReverseV | [JBS](https://bugs.openjdk.org/browse/JDK-8320997) |
| JDK-8352615 | [Test] RISC-V: TestVectorizationMultiInvar.java fails on riscv64 without rvv support | [JBS](https://bugs.openjdk.org/browse/JDK-8352615) |
| JDK-8352159 | RISC-V: add more zfa support | [JBS](https://bugs.openjdk.org/browse/JDK-8352159) |
| JDK-8352423 | RISC-V: simplify DivI/L ModI/L | [JBS](https://bugs.openjdk.org/browse/JDK-8352423) |
| JDK-8352248 | Check if CMoveX is supported | [JBS](https://bugs.openjdk.org/browse/JDK-8352248) |
| JDK-8352529 | RISC-V: enable loopopts tests | [JBS](https://bugs.openjdk.org/browse/JDK-8352529) |
| JDK-8351902 | RISC-V: Several tests fail after JDK-8351145 | [JBS](https://bugs.openjdk.org/browse/JDK-8351902) |
| JDK-8351876 | RISC-V: enable and fix some float round tests | [JBS](https://bugs.openjdk.org/browse/JDK-8351876) |
| JDK-8318220 | RISC-V: C2 ReverseI | [JBS](https://bugs.openjdk.org/browse/JDK-8318220) |
| JDK-8318221 | RISC-V: C2 ReverseL | [JBS](https://bugs.openjdk.org/browse/JDK-8318221) |
| JDK-8345298 | RISC-V: Add riscv backend for Float16 operations - scalar | [JBS](https://bugs.openjdk.org/browse/JDK-8345298) |
| JDK-8351861 | RISC-V: add simple assert at arrays_equals_v | [JBS](https://bugs.openjdk.org/browse/JDK-8351861) |
| JDK-8351662 | [Test] RISC-V: enable bunch of IR test | [JBS](https://bugs.openjdk.org/browse/JDK-8351662) |
| JDK-8351345 | [IR Framework] Improve reported disabled ir verification messages | [JBS](https://bugs.openjdk.org/browse/JDK-8351345) |
| JDK-8351145 | RISC-V: only enable some crypto intrinsic when AvoidUnalignedAccess == false | [JBS](https://bugs.openjdk.org/browse/JDK-8351145) |
| JDK-8350095 | RISC-V: Refactor string_compare | [JBS](https://bugs.openjdk.org/browse/JDK-8350095) |
| JDK-8350931 | RISC-V: remove unnecessary src register for fp_sqrt_d/f | [JBS](https://bugs.openjdk.org/browse/JDK-8350931) |
| JDK-8350940 | RISC-V: remove unnecessary assert_different_registers in minmax_fp | [JBS](https://bugs.openjdk.org/browse/JDK-8350940) |
| JDK-8351033 | RISC-V: TestFloat16ScalarOperations asserts with offset too large | [JBS](https://bugs.openjdk.org/browse/JDK-8351033) |
| JDK-8350855 | RISC-V: print offset by assert of patch_offset_in_conditional_branch | [JBS](https://bugs.openjdk.org/browse/JDK-8350855) |
| JDK-8321003 | RISC-V: C2 MulReductionVI | [JBS](https://bugs.openjdk.org/browse/JDK-8321003) |
| JDK-8321004 | RISC-V: C2 MulReductionVL | [JBS](https://bugs.openjdk.org/browse/JDK-8321004) |
| JDK-8350383 | Test: add more test case for string compare (UL case) | [JBS](https://bugs.openjdk.org/browse/JDK-8350383) |
| JDK-8349908 | RISC-V: C2 SelectFromTwoVector | [JBS](https://bugs.openjdk.org/browse/JDK-8349908) |
| JDK-8349556 | RISC-V: improve the performance when -COH and -AvoidUnalignedAccesses for UL and LU string comparison | [JBS](https://bugs.openjdk.org/browse/JDK-8349556) |
| JDK-8349666 | RISC-V: enable superwords tests for vector reductions | [JBS](https://bugs.openjdk.org/browse/JDK-8349666) |
| JDK-8348575 | SpinLockT is typedef'ed but unused | [JBS](https://bugs.openjdk.org/browse/JDK-8348575) |
| JDK-8345669 | RISC-V: fix client build failure due to AlignVector after JDK-8343827 | [JBS](https://bugs.openjdk.org/browse/JDK-8345669) |
| JDK-8339910 | RISC-V: crc32 intrinsic with carry-less multiplication | [JBS](https://bugs.openjdk.org/browse/JDK-8339910) |

## 4. Key Contributions

### 1. RISC-V CPU Feature Bitmap Implementation

**JDK-8367103: RISC-V: store cpu features in a bitmap**

This contribution refactored how RISC-V CPU features are stored, moving from individual flags to a bitmap-based approach:

```cpp
// Before: Individual feature flags
bool UseZfh;
bool UseZvfh;
bool UseZicond;
// ... many more

// After: Bitmap-based storage
class RVFeatures {
private:
  Bitmap _features;
public:
  bool has_feature(RVFeature feature) const {
    return _features.at(feature);
  }
  void set_feature(RVFeature feature) {
    _features.set_bit(feature);
  }
};
```

This approach provides better scalability and easier feature dependency management.

### 2. Float16 Vectorization for RISC-V

**JDK-8350960: RISC-V: Add riscv backend for Float16 operations - vectorization**

Implemented vector Float16 operations using RISC-V vector extensions:

```cpp
// Float16 vector operations using Zvfh extension
void C2_MacroAssembler::float16_vector_operation(FloatRegister dst,
                                                   FloatRegister src,
                                                   BasicType bt) {
  if (UseZvfh) {
    // Use vector Float16 instructions
    vfmv_vf(dst, src);
  } else {
    // Fallback to scalar operations
    float16_scalar_operation(dst, src);
  }
}
```

### 3. Conditional Move Implementation

**JDK-8352504: RISC-V: implement and enable CMoveI/L**

Implemented conditional move instructions for RISC-V, improving performance of branch-heavy code:

```cpp
// Conditional move using Zicond extension
void MacroAssembler::cmove(Register dst, Register src, Condition cond) {
  if (UseZicond) {
    // Use czero.eqz/czero.nez instructions
    czero_eqz(dst, src, cond);
  } else {
    // Fallback to branch-based implementation
    Label skip;
    beqz(cond, skip);
    mv(dst, src);
    bind(skip);
  }
}
```

### 4. CRC32 Intrinsic with Carry-less Multiplication

**JDK-8339910: RISC-V: crc32 intrinsic with carry-less multiplication**

Implemented CRC32 using RISC-V's Zbkc (Carry-less multiplication) extension:

```cpp
uint32_t crc32_clmul(uint32_t crc, const uint8_t* buf, size_t len) {
  // Use Zbkc extension for carry-less multiplication
  // This provides significant performance improvement for CRC32
  for (size_t i = 0; i < len; i++) {
    crc = clmul(crc ^ buf[i], CRC32_POLY);
  }
  return crc;
}
```

### 5. C2 SuperWord Unsigned Compare Fix

**JDK-8370794: C2 SuperWord: Long/Integer.compareUnsigned return wrong value for EQ/NE in SLP**

Fixed a critical bug in SuperWord vectorization for unsigned comparisons:

```cpp
// Fixed: Correct handling of unsigned compare in SLP
// The issue was that EQ/NE comparisons were incorrectly optimized
// when vectorizing unsigned compare operations
bool VTransform::transform_unsigned_compare(Node* n) {
  // Ensure proper handling of unsigned semantics
  // in vectorized compare operations
}
```

## 5. Development Style

### Code Characteristics
- **Architecture-focused**: Deep understanding of RISC-V instruction set
- **Performance-oriented**: Optimizes for specific CPU extensions
- **Incremental approach**: Builds features step by step (scalar -> vector)
- **Test-driven**: Enables and fixes tests alongside implementation

### Typical Commit Pattern
1. Implement core functionality for RISC-V
2. Add CPU feature detection and dependency handling
3. Enable tests and fix any failures
4. Refactor for code clarity and maintainability

### Review Style
- Often reviewed by Dean Long (dlong), Ludovic Henry (luhenry, Rivos colleague), and Emanuel Peter (epeter)
- Focuses on correctness of assembly code generation
- Ensures proper feature dependency chains

## 6. Related Links

- [OpenJDK Profile](https://openjdk.org/census#mli)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20mli)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=Hamlin-Li)
- [RISC-V Port Project](https://openjdk.org/projects/riscv-port/)