# JDK 26 Compiler Component Summary

> Commits: 725 (18.4% of total)
> Key Contributors: Emanuel Peter, Jatin Bhateja, Hamlin Li, Roland Westrelin

---

## Overview

JDK 26 brings significant improvements to the JIT compiler (C1/C2), with major work on vectorization (SuperWord), template-based testing, and platform-specific optimizations for RISC-V and x86 (AVX10/AVX512).

---

## Major Changes

### Template-Based Testing Framework

**JDK-8344942**: New template-based testing framework for C2 compiler

This is one of the most impactful compiler changes, adding a comprehensive testing infrastructure.

| Metric | Value |
|--------|-------|
| Additions | 6,722 |
| Deletions | 0 |
| Author | Emanuel Peter |

**Benefits**:
- More systematic compiler testing
- Easier to add new test cases
- Better coverage of compiler optimizations

**Related**: JDK-8367531 (scopes and tokens), JDK-8359412 (operations and expressions)

### SuperWord Improvements

SuperWord (auto-vectorization) received significant attention:

| Issue | Description | Impact |
|-------|-------------|--------|
| 8324751 | Aliasing Analysis runtime check | ⭐⭐⭐⭐⭐ |
| 8340093 | Implement cost model | ⭐⭐⭐⭐ |
| 8370794 | Long/Integer.compareUnsigned fix | ⭐⭐⭐⭐ |
| 8373026 | Vector algorithms test and bench | ⭐⭐⭐⭐ |

### Vector API

Extensive Vector API improvements and new intrinsics:

| Issue | Description | +/- |
|-------|-------------|-----|
| 8376186 | Nomenclature change for vector classes | 35,619 |
| 8372978 | Fix UMIN/UMAX reduction identity | 16,747 |
| 8377447 | Float16 conversion wrappers | 16,323 |
| 8371446 | Mask from long values tests | 10,380 |
| 8378758 | Scalar operation wrappers | 10,325 |
| 8376187 | New lane type constants | 3,508 |
| 8358768 | SUADD as associative | 3,159 |
| 8362279 | SUADD reduction support | 2,171 |
| 8354242 | Vector not with compare | 1,636 |
| 8372980 | AArch64 unsigned min/max | 1,776 |

---

## Platform-Specific Optimizations

### x86 (AVX10/AVX512)

| Issue | Description | Author |
|-------|-------------|--------|
| 8354348 | EVEX to REX2/REX demotion | Srinivas Vamsi Parasa |
| 8371955 | AVX10 floating point comparison | Mohamed Issa |
| 8359965 | Paired pushp/popp for APX | Srinivas Vamsi Parasa |
| 8371259 | ML-DSA AVX2/AVX512 intrinsics | Volodymyr Paprotski |

### RISC-V

| Issue | Description | Author |
|-------|-------------|--------|
| 8357551 | CMoveF/D vectorization | Hamlin Li |
| 8358892 | DAC crash fix | Hamlin Li |
| 8367137 | Zicboz block size detection | Dingli Zhang |
| 8372188 | Atomic match rules from M4 | Aleksey Shipilev |
| 8369211 | Devirtualize RelocActions | Andrew Haley |

### AArch64

| Issue | Description | Author |
|-------|-------------|--------|
| 8372980 | Unsigned min/max intrinsics | Eric Fang |
| 8348868 | SelectFromTwoVector backend | Bhavana Kilambi |

### 32-bit x86 Removal

**JDK-8351159**: Cleanup after 32-bit x86 support removal

| Metric | Value |
|--------|-------|
| Additions | 16,353 |
| Deletions | 17,326 |
| Author | Anton Seoane Ampudia |

---

## C2 Compiler Optimizations

### Loop Optimizations

| Issue | Description | Author |
|-------|-------------|--------|
| 8342692 | Long counted loop/range checks | Roland Westrelin |
| 8371685 | Flag to disable loop peeling | Ashay Rane |
| 8353290 | Refactor is_counted_loop() | Kangcheng Xu |

### Type System

| Issue | Description | Author |
|-------|-------------|--------|
| 8315066 | Unsigned bounds and known bits | Quan Anh Mai |
| 8367341 | KnownBits for And/Or operations | Quan Anh Mai |

### Memory Graph

| Issue | Description | Author |
|-------|-------------|--------|
| 8327963 | Initialize node memory graph | Roland Westrelin |

### Method Handle

| Issue | Description | Author |
|-------|-------------|--------|
| 8366461 | Remove obsolete invoke logic | Dean Long |
| 8325467 | Methods with many arguments | Daniel Lundén |

---

## C1 Compiler

Less activity than C2, but notable changes:

| Issue | Description |
|-------|-------------|
| 8365501 | Remove special AdapterHandlerEntry for abstract methods |

---

## Code Generation

### Register Allocation

| Issue | Description | Author |
|-------|-------------|--------|
| 8369569 | Regmask method naming | Daniel Lundén |

### Intrinsics

Major intrinsics added or improved:

| Issue | Description | Platform |
|-------|-------------|----------|
| 8371259 | ML-DSA | x86 AVX2/AVX512 |
| 8372980 | Unsigned min/max | AArch64 |
| 8371955 | FP comparison | x86 AVX10 |

---

## Top 10 Contributors

| Rank | Contributor | Focus Area |
|------|-------------|------------|
| 1 | Emanuel Peter | SuperWord, Testing |
| 2 | Jatin Bhateja | Vector API |
| 3 | Hamlin Li | RISC-V |
| 4 | Roland Westrelin | Loop optimizations |
| 5 | Kangcheng Xu | C2 refactoring |
| 6 | Quan Anh Mai | Type system |
| 7 | Srinivas Vamsi Parasa | x86 optimizations |
| 8 | Daniel Lundén | Register allocation |
| 9 | Eric Fang | Vector API AArch64 |
| 10 | Anton Seoane Ampudia | x86 cleanup |

---

## Testing Infrastructure

### New Tests

| Issue | Description |
|-------|-------------|
| 8344942 | Template-based testing framework |
| 8373026 | Vector algorithms benchmark |
| 8367158 | Fill and copy benchmarks |
| 8378166 | NBody / particle life demo |

### Test Migration

Several tests migrated from TestNG to JUnit:
- JDK-8373935: java/lang/invoke tests
- JDK-8365776: JShell tests

---

## Verification

### VerifyIterativeGVN

**JDK-8347273**: Add verification for Ideal and Identity transformations

This helps catch compiler bugs during development.

---

## Key Commits by Impact

| Issue | Description | +/- | Author |
|-------|-------------|-----|--------|
| 8376186 | VectorAPI nomenclature | 35,619 | Jatin Bhateja |
| 8351159 | 32-bit x86 cleanup | 33,679 | Anton Seoane Ampudia |
| 8372978 | VectorAPI UMIN/UMAX | 16,747 | Eric Fang |
| 8377447 | VectorAPI float16 | 16,323 | Jatin Bhateja |
| 8344942 | Template testing | 6,722 | Emanuel Peter |
| 8324751 | SuperWord aliasing | 6,059 | Emanuel Peter |
| 8367531 | Template scopes | 4,979 | Emanuel Peter |

---

## Migration Notes

### For Compiler Developers
- Template-based testing framework available for new tests
- SuperWord has new cost model - review if relying on auto-vectorization
- KnownBits analysis improved - may affect optimization assumptions

### For Performance Engineers
- AVX10 support maturing - test on newer Intel CPUs
- RISC-V vectorization improving - benchmark on RISC-V hardware
- Loop peeling can now be disabled for debugging

---

*Last updated: 2026-03-19*
