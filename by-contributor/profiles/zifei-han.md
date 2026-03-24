# Zifei Han

> **GitHub**: [@zifeihan](https://github.com/zifeihan)
> **Organization**: Independent / Community Contributor
> **OpenJDK Contributions**: 66 to openjdk/jdk (66 integrated PRs on GitHub)

---
## 目录

1. [概述](#1-概述)
2. [Basic Information](#2-basic-information)
3. [Contribution Overview](#3-contribution-overview)
4. [Key Contributions](#4-key-contributions)
5. [Recent Activity](#5-recent-activity)
6. [Development Style](#6-development-style)
7. [Related Links](#7-related-links)

---

## 1. 概述

Zifei Han is a community contributor and one of the most active RISC-V platform engineers working on OpenJDK. With 66 contributions to openjdk/jdk, he focuses on RISC-V architecture support, including the RISC-V Vector Extension (RVV) implementation, C1/C2 compiler backends for RISC-V, and low-level assembler improvements. His work helps ensure that the JDK runs efficiently on the emerging RISC-V hardware ecosystem, covering vector API support, compiler intrinsics, and platform-specific bug fixes.

Zifei 也是 **Apache** 开源社区的贡献者 (GitHub profile 显示 Apache 组织成员)，曾参与 **Apache SkyWalking** (APM 监控系统) 的开发。在 RISC-V 领域，他维护了 [vector-api-test-rvv](https://github.com/zifeihan/vector-api-test-rvv) 测试项目，用于在 RISC-V 硬件上对 JDK Vector API 进行性能基准测试。他的测试结果显示，启用 `-XX:+UseRVV` 后 C2 汇编指令数可减少约 50%。他还参与了 JDK 17u 和 JDK 11u 的 RISC-V 移植工作。

---

## 2. Basic Information

| Attribute | Value |
|-----------|-------|
| **Name** | Zifei Han (韩子飞) |
| **GitHub** | [@zifeihan](https://github.com/zifeihan) |
| **Organization** | Apache Member; Community Contributor |
| **PRs** | [66 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Azifeihan+is%3Aclosed+label%3Aintegrated) |
| **Total Contributions** | 66 |
| **主要领域** | RISC-V, Vector Extension (RVV), C1/C2 Compiler Backends, MacroAssembler |

---

## 3. Contribution Overview

### By Category

| Category | Approx. Count | Description |
|----------|---------------|-------------|
| RISC-V Vector (RVV) | 15+ | Vector API tests, register constraints, vector gather/scatter |
| RISC-V C1/C2 Backend | 15+ | Compiler intrinsics, code generation, optimizations |
| RISC-V MacroAssembler | 10+ | Assembler routines, alignment fixes, cleanup |
| RISC-V Platform Fixes | 10+ | Build fixes, secondary super cache, problem listing |
| General HotSpot | 5+ | Removing unused code, fixing warnings |

### Key Areas of Expertise

- **RISC-V Vector Extension (RVV)**: Implementing and fixing JDK Vector API support on RISC-V hardware, including register constraint relaxation and vector instruction correctness.
- **RISC-V Compiler Backends**: C1 and C2 compiler code generation for RISC-V, including intrinsics like `Class.isInstance` and secondary super cache lookups.
- **RISC-V MacroAssembler**: Low-level assembler routines for RISC-V, including sub/subw cleanup, reserved stack checks, and alignment handling.
- **Object Monitor Implementation**: Contributed the RISC-V implementation of the new Object-to-ObjectMonitor mapping (JDK-8338539).

---

## 4. Key Contributions

### 4.1 RISC-V Object-to-ObjectMonitor Mapping (JDK-8338539)

Implemented the RISC-V 64-bit version of the new Object-to-ObjectMonitor mapping ([PR #20621](https://github.com/openjdk/jdk/pull/20621)). This was a platform-specific implementation of a cross-cutting JVM change that affects synchronization performance on RISC-V hardware.

### 4.2 RISC-V Secondary Super Cache (JDK-8342881)

Implemented the C1 and interpreter support for the secondary super cache on RISC-V ([PR #21922](https://github.com/openjdk/jdk/pull/21922)), part of the effort to improve `instanceof` and type-check performance on this architecture.

### 4.3 RISC-V Vector API Fixes (JDK-8355878, JDK-8355668)

Fixed multiple Vector API test failures when using the RISC-V Vector Extension, including DoubleMaxVectorTests ([PR #24943](https://github.com/openjdk/jdk/pull/24943)) and Int256VectorTests ([PR #24910](https://github.com/openjdk/jdk/pull/24910)). These fixes ensure the JDK Vector API works correctly on RVV-capable hardware.

### 4.4 RISC-V Vector Register Constraint Relaxation (JDK-8355654)

Relaxed register constraints for some vector-scalar instructions on RISC-V ([PR #24905](https://github.com/openjdk/jdk/pull/24905)), allowing the register allocator more freedom and potentially improving generated code quality.

### 4.5 C1 Class.isInstance Intrinsic for RISC-V (JDK-8349764)

Improved the C1 compiler's `Class.isInstance` intrinsic on RISC-V ([PR #23551](https://github.com/openjdk/jdk/pull/23551)), reducing the overhead of this commonly-used reflection operation.

### 4.6 Alignment Fix After JDK-8347489 (JDK-8349428)

Fixed a "bad alignment" error on RISC-V when running with `-XX:-AvoidUnalignedAccesses` ([PR #23459](https://github.com/openjdk/jdk/pull/23459)), a platform-specific regression that could cause crashes on real RISC-V hardware.

---

## 5. Recent Activity

| Date | PR | Title |
|------|-----|-------|
| 2025-04 | [#24943](https://github.com/openjdk/jdk/pull/24943) | RISC-V: DoubleMaxVectorTests fails when using RVV |
| 2025-04 | [#24910](https://github.com/openjdk/jdk/pull/24910) | RISC-V: Int256VectorTests fails when using RVV |
| 2025-04 | [#24905](https://github.com/openjdk/jdk/pull/24905) | RISC-V: Relax register constraint for vector-scalar instructions |
| 2025-02 | [#23551](https://github.com/openjdk/jdk/pull/23551) | RISC-V: C1: Improve Class.isInstance intrinsic |
| 2025-02 | [#23459](https://github.com/openjdk/jdk/pull/23459) | RISC-V: bad alignment with -XX:-AvoidUnalignedAccesses |
| 2025-01 | [#22902](https://github.com/openjdk/jdk/pull/22902) | TestVectorizationNegativeScale.java fails without rvv extension |
| 2025-01 | [#22901](https://github.com/openjdk/jdk/pull/22901) | TestVectorReinterpret.java fails without rvv extension |
| 2025-01 | [#21922](https://github.com/openjdk/jdk/pull/21922) | RISC-V: secondary_super_cache: C1 and interpreter |

---

## 6. Development Style

### Patterns

- **Platform specialist**: Nearly all contributions are RISC-V-specific, demonstrating deep knowledge of the RISC-V ISA, vector extensions, and how HotSpot maps to this architecture.
- **Test-driven fixes**: Many contributions fix test failures on RISC-V hardware, indicating access to real RISC-V hardware for testing rather than just emulation.
- **Cross-subsystem platform work**: Contributions span the C1 compiler, C2 compiler, interpreter, MacroAssembler, and runtime, covering all the layers that need platform-specific code.
- **Responsive to regressions**: Quick to fix build failures and test regressions caused by cross-platform changes that break RISC-V (e.g., JDK-8339237 fixing builds after JDK-8339120).

### Commit Style

Commits follow the standard OpenJDK format: `JDK-NNNNNNN: <description>`. Most commit descriptions are prefixed with "RISC-V:" for clear identification of the target platform.

---

## 7. Related Links

- [GitHub Profile](https://github.com/zifeihan)
- [GitHub Commits to openjdk/jdk](https://github.com/openjdk/jdk/commits?author=zifeihan)
- [Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Azifeihan+is%3Aclosed+label%3Aintegrated)
- [vector-api-test-rvv](https://github.com/zifeihan/vector-api-test-rvv) - RISC-V Vector API performance benchmarks
- [State of OpenJDK on RISC-V (JCP, April 2024)](https://jcp.org/aboutJava/communityprocess/ec-public/materials/2024-04-24/JCP-State_of_OpenJDK_on_RISC-V.pdf)


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 38 |
| **活跃仓库数** | 1 |
