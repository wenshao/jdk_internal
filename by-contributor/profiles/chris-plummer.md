# Chris Plummer

> **GitHub**: [@plummercj](https://github.com/plummercj)
> **Organization**: Oracle
> **OpenJDK Contributions**: 437 to openjdk/jdk (277 integrated PRs on GitHub)

---
## 目录

1. [概述](#1-概述)
2. [Basic Information](#2-basic-information)
3. [Contribution Overview](#3-contribution-overview)
4. [Key Contributions](#4-key-contributions)
5. [Recent Activity](#5-recent-activity)
6. [Development Style](#7-development-style)
7. [Related Links](#8-related-links)

---

## 1. 概述

Chris Plummer is a long-standing Oracle engineer based in San Martin, California, and one of the most prolific contributors to JDK serviceability infrastructure. With 437 contributions to openjdk/jdk, he is the primary maintainer and developer for the Java debugging stack: JDWP (Java Debug Wire Protocol), JDI (Java Debug Interface), JVMTI (JVM Tool Interface), and SA (Serviceability Agent). His work ensures that debuggers, profilers, and diagnostic tools function correctly across all JDK releases, including adapting the entire debugging subsystem for Project Loom's virtual threads. He is a JDK Reviewer/Committer in the OpenJDK Census.

---

## 2. Basic Information

| Attribute | Value |
|-----------|-------|
| **Name** | Chris Plummer |
| **Current Organization** | Oracle |
| **Location** | San Martin, California, USA |
| **GitHub** | [@plummercj](https://github.com/plummercj) |
| **OpenJDK** | [@plummercj](https://openjdk.org/census#plummercj) |
| **Email** | cjplummer@openjdk.org |
| **PRs** | [277 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Aplummercj+is%3Aclosed+label%3Aintegrated) |
| **Total Contributions** | 437 (including pre-GitHub commits) |
| **主要领域** | JDWP, JDI, JVMTI, SA, Debugging, Serviceability |

---

## 3. Contribution Overview

### By Category

| Category | Approx. Count | Description |
|----------|---------------|-------------|
| JDI (Java Debug Interface) | 80+ | Test fixes, spec clarifications, virtual thread support |
| JDWP (Debug Wire Protocol) | 40+ | Debug agent fixes, thread management, protocol correctness |
| SA (Serviceability Agent) | 50+ | Core file support, jhsdb, pointer analysis, thread types |
| JVMTI | 20+ | Event handling, stress tests, problem listing |
| Test Infrastructure | 40+ | Problem listing, test reliability, diagnostics |
| Spec / Javadoc | 15+ | JDI/JDWP specification fixes and clarifications |

### Key Areas of Expertise

- **JDWP / Debug Agent**: The native debug agent (libjdwp) that implements the wire protocol between debuggers and the JVM. Thread lifecycle management, connection handling, deadlock prevention.
- **JDI**: The Java-level debugging API. Thread references, event requests, frame inspection, virtual thread support for nsk test suites.
- **SA (Serviceability Agent)**: Post-mortem and live-attach analysis tool (jhsdb). Core file handling, CodeBlob support, pointer location analysis, GC-specific adaptations.
- **JVMTI**: JVM-level tool interface. Event callbacks, thread state management, stress testing modes.
- **Virtual Thread Debugging**: Adapting the entire debugging stack for Project Loom virtual threads, including ThreadNode management in JDWP and `includevirtualthreads` support in JDI tests.

---

## 4. Key Contributions

### 4.1 Virtual Thread Support in Debug Agent (JDK-8282441)

One of Plummer's most significant contributions: making the JDWP debug agent properly manage virtual thread ThreadNodes. Before this fix, vthread ThreadNodes accumulated indefinitely, causing memory leaks. The fix ensures the debug agent frees vthread ThreadNodes when they are no longer needed.

### 4.2 Single Stepping Fix (JDK-8229012)

Fixed a long-standing issue where the debug agent could cause a thread to remain in interpreter mode after single stepping completes. This affected performance of debugged applications, as threads would not return to compiled code after stepping operations finished.

### 4.3 Debug Agent Deadlock Prevention (JDK-8332738)

Resolved a deadlock in the debug agent's `callbackLock` when using `StackFrame.PopFrames`. This was a critical fix for debugger reliability, as the deadlock would hang both the debugger and the target VM.

### 4.4 SA CodeBlob and Thread Cleanup (JDK-8350287, JDK-8348347, JDK-8349571)

A series of cleanups to the Serviceability Agent removing obsolete CodeBlob subclass support, JavaThread subclass handling, and the JavaThreadFactory interface. These simplifications made SA more maintainable and aligned it with current HotSpot internals.

### 4.5 JDWP Spec Clarifications (JDK-8362304, JDK-8309400)

Fixed the JDWP specification regarding OPAQUE_FRAME and INVALID_SLOT errors, and clarified JDI spec behavior for OpaqueFrameException and NativeMethodException. These spec fixes are essential for debugger implementors building against the JPDA specification.

### 4.6 JDI ThreadReference.threadGroups() Lockup Fix (JDK-8352088)

Fixed a case where calling `ThreadReference.threadGroups()` could lock up the target VM. This affected real-world debugger usage in IDEs where thread group enumeration is a common operation.

### 4.7 JVMTI DataDumpRequest for Debug Agent (JDK-8332488)

Added JVMTI DataDumpRequest support to the debug agent, along with useful debugging APIs (JDK-8341295). These enhancements improve the diagnostic capability of the debug agent itself when troubleshooting debugger issues.

### 4.8 SA PointerFinder G1 Support (JDK-8323681)

Extended the SA PointerFinder code to support the G1 garbage collector, improving SA's ability to identify what a given memory address points to during post-mortem analysis.

---

## 5. Recent Activity

| Date | PR | Title |
|------|-----|-------|
| 2026-03 | [#29959](https://github.com/openjdk/jdk/pull/29959) | Disable SA tests when ZGC is being used |
| 2026-02 | [#29849](https://github.com/openjdk/jdk/pull/29849) | Step Over doesn't stop after receiving MethodExitEvent |
| 2026-02 | [#29624](https://github.com/openjdk/jdk/pull/29624) | Problem list serviceability/sa/TestJhsdbJstackMixedCore.java |
| 2026-01 | [#29284](https://github.com/openjdk/jdk/pull/29284) | CoreUtils support for SA tests: locate and unzip core files |
| 2025-12 | [#28907](https://github.com/openjdk/jdk/pull/28907) | JDI EventRequestManager javadoc link tag fix |
| 2025-12 | [#28653](https://github.com/openjdk/jdk/pull/28653) | JDWP WRONG_PHASE error during VirtualMachine dispose |
| 2025-12 | [#28616](https://github.com/openjdk/jdk/pull/28616) | JDWP invalid FrameIDs after vthread ThreadNode changes |
| 2025-11 | [#28211](https://github.com/openjdk/jdk/pull/28211) | Debug agent vthread ThreadNode lifecycle management |

---

## 6. Development Style

### Patterns

- **Deep domain ownership**: Plummer owns the full debugging stack end-to-end, from the native JDWP agent through JDI to the SA. Changes often span multiple layers.
- **Test reliability focus**: A large portion of contributions are stabilizing flaky JDI and SA tests, adding proper timeouts, fixing race conditions, and problem-listing intermittent failures with tracking bugs.
- **Incremental multi-part refactoring**: Large changes are broken into numbered parts (e.g., "fetch ThreadReference from static field: part 1/2/3/4"), making reviews manageable.
- **Spec-conscious**: Regularly fixes JDI/JDWP specification text alongside code changes, ensuring spec and implementation stay aligned.
- **Virtual thread adaptation**: Systematic work adapting the nsk/jdi test suite for virtual threads, ensuring `includevirtualthreads=y` works correctly across hundreds of tests.

### Commit Style

Commits follow the standard OpenJDK format: `JDK-NNNNNNN: <description>`. Plummer's commit messages are concise and issue-focused, typically matching the JBS bug title directly.

---

## 7. Related Links

- [GitHub Profile](https://github.com/plummercj)
- [GitHub Commits to openjdk/jdk](https://github.com/openjdk/jdk/commits?author=plummercj)
- [Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Aplummercj+is%3Aclosed+label%3Aintegrated)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=assignee%20%3D%20cjplummer)
- [OpenJDK Census](https://openjdk.org/census#plummercj)


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 741 |
| **活跃仓库数** | 4 |
