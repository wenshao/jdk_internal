# Richard Reingruber

> **GitHub**: [@reinrich](https://github.com/reinrich)
> **Organization**: SAP
> **OpenJDK Contributions**: 94 to openjdk/jdk (76 integrated PRs on GitHub)

---
## Table of Contents

1. [Overview](#1-overview)
2. [Basic Information](#2-basic-information)
3. [Contribution Overview](#3-contribution-overview)
4. [Key Contributions](#4-key-contributions)
5. [Recent Activity](#5-recent-activity)
6. [Development Style](#6-development-style)
7. [Related Links](#7-related-links)

---

## 1. Overview

Richard Reingruber is an engineer at SAP based in Germany and a significant contributor to the OpenJDK HotSpot runtime. With 94 contributions to openjdk/jdk, his work spans C2 compiler internals, PPC64 platform support, deoptimization, safepoints, and garbage collector barriers. He is one of the primary maintainers of the PPC64 backend for HotSpot and has contributed important fixes to escape analysis, JVMTI interactions, and Project Loom's continuation support on non-x86 platforms.

---

## 2. Basic Information

| Attribute | Value |
|-----------|-------|
| **Name** | Richard Reingruber |
| **Current Organization** | SAP |
| **GitHub** | [@reinrich](https://github.com/reinrich) |
| **Location** | Germany |
| **PRs** | [76 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Areinrich+is%3Aclosed+label%3Aintegrated) |
| **Total Contributions** | 94 (including pre-GitHub commits) |
| **Primary Areas** | C2 compiler, PPC64, deoptimization, safepoints, GC barriers |

---

## 3. Contribution Overview

### By Category

| Category | Approx. Count | Description |
|----------|---------------|-------------|
| PPC64 Platform | 25+ | Platform-specific fixes, continuations port, ABI handling |
| C2 Compiler | 15+ | Escape analysis, register allocation, store merging |
| Deoptimization / Safepoints | 10+ | Frame revocation, deopt fixes, safepoint checks |
| GC (G1/Parallel) | 8+ | SATB barriers, nmethod handling, work distribution |
| JVMTI / Debugging | 8+ | Escape analysis with JVMTI, JDWP deadlocks, EATests |
| Test Infrastructure | 10+ | Problem listing, test fixes, platform-specific test guards |

---

## 4. Key Contributions

### 4.1 Escape Analysis with JVMTI Agents (JDK-8227745)

One of Reingruber's most important contributions: enabling escape analysis optimizations to remain effective even in the presence of JVMTI agents. Previously, escape analysis was entirely disabled when agents were attached, significantly hurting debugged application performance. This change allows scalar replacement and lock elision to work alongside debugging tools.

### 4.2 Port of Virtual Threads (JEP 425) to PPC64 (JDK-8286302)

Ported Project Loom's virtual thread implementation to the PPC64 architecture, including continuation freeze/thaw support. This required adapting the continuation entry/exit stubs, thaw logic, and stack walking for the PPC64 ABI, enabling virtual threads on SAP's enterprise platforms.

### 4.3 G1 SATB Barrier Fix for Nmethods (JDK-8300915)

Fixed a critical bug where incomplete SATB (Snapshot-At-The-Beginning) marking could occur because nmethod entry barriers were not being armed correctly. This could lead to G1 garbage collector correctness issues, as live objects might not be marked during concurrent marking.

### 4.4 C2 Array Load Out-of-Bounds Fix (JDK-8262295)

Fixed a C2 compiler bug where an out-of-bounds array load could occur from a clone source object. This was a correctness issue in the compiler's handling of array cloning optimizations.

### 4.5 JDWP Deadlock Fix (JDK-8274687)

Resolved a deadlock in the JDWP debug agent that occurred when a Java thread reached a wait state inside `blockOnDebuggerSuspend`. This fix improved debugger reliability for production debugging scenarios.

### 4.6 C2 Independent Load Hoisting (JDK-8263781)

Enabled C2 to hoist independent loads above arraycopy operations, improving performance of code patterns where array copies are followed by loads from unrelated memory locations.

---

## 5. Recent Activity

| Date | PR | Title |
|------|-----|-------|
| 2026-03 | [#30245](https://github.com/openjdk/jdk/pull/30245) | PPC: remove POWER6 remnants |
| 2026-03 | [#30164](https://github.com/openjdk/jdk/pull/30164) | PPC: cleanup C2 OptoAssembly |
| 2026-01 | [#29133](https://github.com/openjdk/jdk/pull/29133) | PPC: MASM::pop_cont_fastpath() should reset _cont_fastpath |
| 2025-12 | [#27969](https://github.com/openjdk/jdk/pull/27969) | C2: Better Alignment of Vector Spill Slots |
| 2025-10 | [#27669](https://github.com/openjdk/jdk/pull/27669) | PPC: RelocateNMethodMultiplePaths.java fails with assertion |

---

## 6. Development Style

### Patterns

- **Platform steward**: Primary maintainer of the PPC64 backend in HotSpot, systematically porting new features (virtual threads, post-call NOPs, store merging) and fixing platform-specific issues.
- **Deep compiler expertise**: Contributions to C2 internals including register allocation, escape analysis, and code generation, often fixing subtle correctness bugs.
- **Cross-subsystem work**: Changes frequently span compiler, runtime, GC, and serviceability boundaries, reflecting a broad understanding of HotSpot internals.
- **Thorough test coverage**: Actively problem-lists failing tests on PPC64/AIX, fixes test assumptions about x86-specific behavior, and adds platform guards for IR-based tests.
- **Enterprise focus**: Work driven by SAP's need for reliable JDK support on enterprise hardware platforms including PPC64 and AIX.

### Commit Style

Commits follow the standard OpenJDK format: `JDK-NNNNNNN: <description>`. Platform-specific changes are consistently prefixed with `[PPC64]` or `PPC:` for easy identification.

---

## 7. Related Links

- [GitHub Profile](https://github.com/reinrich)
- [GitHub Commits to openjdk/jdk](https://github.com/openjdk/jdk/commits?author=reinrich)
- [Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Areinrich+is%3Aclosed+label%3Aintegrated)

## 角色晋升 (CFV)

| 日期 | 角色 | 提名者 | 投票数 | 链接 |
|------|------|--------|--------|------|
| 2020-11-09 | Reviewer | Lindenmaier, Goetz | 20 | [CFV](https://mail.openjdk.org/pipermail/jdk-dev/2020-November/004911.html) |

**提名时统计**: 30 changes
**贡献领域**: JVMTI; compiler; GC; s390/PPC ports
