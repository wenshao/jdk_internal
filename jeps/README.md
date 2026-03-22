# JEP 索引

> JDK Enhancement Proposals — 共收录 **197 篇** JEP 分析文档，覆盖 JDK 8 至 JDK 26

---

## 目录

1. [按主题浏览](#1-按主题浏览)
   - [语言特性](#11-语言特性)
   - [垃圾收集](#12-垃圾收集-gc)
   - [并发编程](#13-并发编程)
   - [性能优化](#14-性能优化)
   - [安全特性](#15-安全特性)
   - [工具改进](#16-工具改进)
   - [外部函数与内存](#17-外部函数与内存-ffi)
   - [平台移植](#18-平台移植)
   - [网络](#19-网络)
   - [监控诊断](#110-监控诊断-jfr)
   - [客户端与 API](#111-客户端与-api)
2. [按版本浏览](#2-按版本浏览)
3. [JEP 状态说明](#3-jep-状态说明)
4. [JSR 与 JEP](#4-jsr-与-jep)
5. [相关链接](#5-相关链接)

---

## 1. 按主题浏览

### 1.1 语言特性

#### Project Valhalla

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 401](language/jep-401.md) | Value Classes (Preview) | 26 | 🔍 预览 |
| [JEP 402](language/jep-402.md) | Unified Generics | - | 🔬 草案 |

#### 现代 Java 语法 (JDK 21-26)

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 513](language/jep-513.md) | Flexible Constructor Bodies | 25 | ✅ 正式 |
| [JEP 512](language/jep-512.md) | Compact Source Files | 25 | ✅ 正式 |
| [JEP 494](language/jep-494.md) | Module Import Declarations (2nd Preview) | 24 | 🔍 预览 |
| [JEP 492](language/jep-492.md) | Flexible Constructor Bodies (3rd Preview) | 24 | 🔍 预览 |
| [JEP 482](language/jep-482.md) | Flexible Constructor Bodies (2nd Preview) | 23 | 🔍 预览 |
| [JEP 477](language/jep-477.md) | Implicit Classes (3rd Preview) | 23 | 🔍 预览 |
| [JEP 476](language/jep-476.md) | Module Import Declarations (Preview) | 23 | 🔍 预览 |
| [JEP 473](language/jep-473.md) | Stream Gatherers (2nd Preview) | 23 | 🔍 预览 |
| [JEP 463](language/jep-463.md) | Implicit Classes (2nd Preview) | 22 | 🔍 预览 |
| [JEP 461](language/jep-461.md) | Stream Gatherers (Preview) | 22 | 🔍 预览 |
| [JEP 445](language/jep-445.md) | Unnamed Classes & Instance Main Methods | 21 | 🔍 预览 |
| [JEP 431](language/jep-431.md) | Sequenced Collections | 21 | ✅ 正式 |
| [JEP 430](language/jep-430.md) | String Templates | 21 | ⚠️ 撤回 |

#### Pattern Matching (JDK 14→26)

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 530](language/jep-530.md) | Primitive Types in Patterns (4th Preview) | 26 | 🔍 预览 |
| [JEP 507](language/jep-507.md) | Primitive Types in Patterns (3rd Preview) | 25 | 🔍 预览 |
| [JEP 488](language/jep-488.md) | Primitive Types in Patterns (2nd Preview) | 24 | 🔍 预览 |
| [JEP 456](language/jep-456.md) | Unnamed Variables and Patterns | 22 | ✅ 正式 |
| [JEP 443](language/jep-443.md) | Unnamed Patterns and Variables (Preview) | 21 | 🔍 预览 |
| [JEP 441](language/jep-441.md) | Pattern Matching for switch | 21 | ✅ 正式 |
| [JEP 440](language/jep-440.md) | Record Patterns | 21 | ✅ 正式 |
| [JEP 406](language/jep-406.md) | Pattern Matching for switch (Preview) | 17 | 🔍 预览 |
| [JEP 394](language/jep-394.md) | Pattern Matching for instanceof | 16 | ✅ 正式 |
| [JEP 375](language/jep-375.md) | Pattern Matching for instanceof (2nd Preview) | 15 | 🔍 预览 |
| [JEP 305](language/jep-305.md) | Pattern Matching for instanceof (Preview) | 14 | 🔍 预览 |

#### Sealed Classes (JDK 15→17)

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 409](language/jep-409.md) | Sealed Classes | 17 | ✅ 正式 |
| [JEP 397](language/jep-397.md) | Sealed Classes (2nd Preview) | 16 | 🔍 预览 |

#### Records (JDK 14→16)

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 395](language/jep-395.md) | Records | 16 | ✅ 正式 |
| [JEP 384](language/jep-384.md) | Records (2nd Preview) | 15 | 🔍 预览 |
| [JEP 359](language/jep-359.md) | Records (Preview) | 14 | 🔍 预览 |

#### Text Blocks (JDK 13→15)

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 378](language/jep-378.md) | Text Blocks | 15 | ✅ 正式 |
| [JEP 368](language/jep-368.md) | Text Blocks (2nd Preview) | 14 | 🔍 预览 |
| [JEP 355](language/jep-355.md) | Text Blocks (Preview) | 13 | 🔍 预览 |

#### Switch 表达式 (JDK 12→14)

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 361](language/jep-361.md) | Switch Expressions | 14 | ✅ 正式 |
| [JEP 354](language/jep-354.md) | Switch Expressions (2nd Preview) | 13 | 🔍 预览 |
| [JEP 325](language/jep-325.md) | Switch Expressions (Preview) | 12 | 🔍 预览 |

#### 模块系统与核心改进 (JDK 9-17)

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 403](language/jep-403.md) | Strongly Encapsulate JDK Internals | 17 | ✅ 正式 |
| [JEP 306](language/jep-306.md) | Restore Always-Strict Floating-Point Semantics | 17 | ✅ 正式 |
| [JEP 396](language/jep-396.md) | Strongly Encapsulate JDK Internals by Default | 16 | ✅ 正式 |
| [JEP 390](language/jep-390.md) | Warnings for Value-Based Classes | 16 | ✅ 正式 |
| [JEP 371](language/jep-371.md) | Hidden Classes | 15 | ✅ 正式 |
| [JEP 334](language/jep-334.md) | JVM Constants API | 12 | ✅ 正式 |
| [JEP 323](language/jep-323.md) | Local-Variable Syntax for Lambda Parameters | 11 | ✅ 正式 |
| [JEP 320](language/jep-320.md) | Remove Java EE and CORBA Modules | 11 | 🗑️ 移除 |
| [JEP 309](language/jep-309.md) | Dynamic Class-File Constants | 11 | ✅ 正式 |
| [JEP 286](language/jep-286.md) | Local-Variable Type Inference (var) | 10 | ✅ 正式 |
| [JEP 280](language/jep-280.md) | Indify String Concatenation | 9 | ✅ 正式 |
| [JEP 269](language/jep-269.md) | Convenience Factory Methods for Collections | 9 | ✅ 正式 |
| [JEP 261](language/jep-261.md) | Module System | 9 | ✅ 正式 |
| [JEP 260](language/jep-260.md) | Encapsulate Most Internal APIs | 9 | ✅ 正式 |
| [JEP 254](language/jep-254.md) | Compact Strings | 9 | ✅ 正式 |
| [JEP 201](language/jep-201.md) | Modular Source Code | 9 | ✅ 正式 |
| [JEP 200](language/jep-200.md) | The Modular JDK | 9 | ✅ 正式 |

#### JDK 8 基础

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 126](language/jep-126.md) | Lambda Expressions | 8 | ✅ 正式 |
| [JEP 150](language/jep-150.md) | Date & Time API (JSR 310) | 8 | ✅ 正式 |
| [JEP 107](language/jep-107.md) | Bulk Data Operations (Stream API) | 8 | ✅ 正式 |
| [JEP 109](language/jep-109.md) | Enhance Core Libraries with Lambda | 8 | ✅ 正式 |
| [JEP 104](language/jep-104.md) | Annotations on Java Types | 8 | ✅ 正式 |
| [JEP 120](language/jep-120.md) | Repeating Annotations | 8 | ✅ 正式 |
| [JEP 174](language/jep-174.md) | Nashorn JavaScript Engine | 8 | ✅ (JDK 15 移除) |
| [JEP 160](language/jep-160.md) | Lambda-Form Representation for Method Handles | 8 | ✅ 正式 |
| [JEP 176](language/jep-176.md) | Mechanical Checking of Caller-Sensitive Methods | 8 | ✅ 正式 |
| [JEP 192](language/jep-192.md) | String Deduplication in G1 | 8 | ✅ 正式 |

---

### 1.2 垃圾收集 (GC)

#### ZGC 演进

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 333](gc/jep-333.md) | ZGC (Experimental) | 11 | 🧪 实验 |
| [JEP 351](gc/jep-351.md) | ZGC: Uncommit Unused Memory | 13 | ✅ 正式 |
| [JEP 377](gc/jep-377.md) | ZGC (Production) | 15 | ✅ 正式 |
| [JEP 439](gc/jep-439.md) | Generational ZGC | 21 | ✅ 正式 |
| [JEP 474](gc/jep-474.md) | ZGC: Generational Mode by Default | 23 | ✅ 正式 |
| [JEP 490](gc/jep-490.md) | ZGC: Remove Non-Generational Mode | 24 | ✅ 正式 |

#### Shenandoah GC 演进

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 189](gc/jep-189.md) | Shenandoah GC (Experimental) | 12 | 🧪 实验 |
| [JEP 379](gc/jep-379.md) | Shenandoah GC (Production) | 15 | ✅ 正式 |
| [JEP 404](gc/jep-404.md) | Generational Shenandoah (Experimental) | 26 | 🧪 实验 |
| [JEP 521](gc/jep-521.md) | Generational Shenandoah | 26 | ✅ 正式 |

#### G1 GC 改进

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 344](gc/jep-344.md) | Abortable Mixed Collections for G1 | 12 | ✅ 正式 |
| [JEP 345](gc/jep-345.md) | NUMA-Aware Memory Allocation for G1 | 14 | ✅ 正式 |
| [JEP 346](gc/jep-346.md) | Promptly Return Unused Memory from G1 | 12 | ✅ 正式 |
| [JEP 423](gc/jep-423.md) | Region Pinning for G1 | 22 | ✅ 正式 |
| [JEP 475](gc/jep-475.md) | Late Barrier Expansion for G1 | 24 | ✅ 正式 |
| [JEP 522](gc/jep-522.md) | G1: Improve Throughput | 26 | ✅ 正式 |

#### 其他 GC

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 318](gc/jep-318.md) | Epsilon: A No-Op GC | 11 | ✅ 正式 |
| [JEP 363](gc/jep-363.md) | Remove CMS GC | 14 | 🗑️ 移除 |
| [JEP 519](gc/jep-519.md) | Compact Object Headers | 25 | ✅ 正式 |

---

### 1.3 并发编程

#### Virtual Threads

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 425](concurrency/jep-425.md) | Virtual Threads (Preview) | 19 | 🔍 预览 |
| [JEP 436](concurrency/jep-436.md) | Virtual Threads (2nd Preview) | 20 | 🔍 预览 |
| [JEP 444](concurrency/jep-444.md) | Virtual Threads | 21 | ✅ 正式 |
| [JEP 491](concurrency/jep-491.md) | Synchronize Virtual Threads without Pinning | 24 | ✅ 正式 |

#### Structured Concurrency

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 453](concurrency/jep-453.md) | Structured Concurrency (Preview) | 21 | 🔍 预览 |
| [JEP 462](concurrency/jep-462.md) | Structured Concurrency (2nd Preview) | 22 | 🔍 预览 |
| [JEP 480](concurrency/jep-480.md) | Structured Concurrency (3rd Preview) | 23 | 🔍 预览 |
| [JEP 499](concurrency/jep-499.md) | Structured Concurrency (4th Preview) | 24 | 🔍 预览 |
| [JEP 505](concurrency/jep-505.md) | Structured Concurrency (5th Preview) | 25 | 🔍 预览 |
| [JEP 525](concurrency/jep-525.md) | Structured Concurrency (6th Preview) | 26 | 🔍 预览 |

#### Scoped Values

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 446](concurrency/jep-446.md) | Scoped Values (Preview) | 21 | 🔍 预览 |
| [JEP 464](concurrency/jep-464.md) | Scoped Values (2nd Preview) | 22 | 🔍 预览 |
| [JEP 481](concurrency/jep-481.md) | Scoped Values (3rd Preview) | 23 | 🔍 预览 |
| [JEP 487](concurrency/jep-487.md) | Scoped Values (4th Preview) | 24 | 🔍 预览 |
| [JEP 506](concurrency/jep-506.md) | Scoped Values | 25 | ✅ 正式 |

#### 其他

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 373](concurrency/jep-373.md) | Reimplement DatagramSocket | 15 | ✅ 正式 |
| [JEP 508](concurrency/jep-508.md) | Vector API (10th Incubator) | 25 | 🥚 孵化 |

---

### 1.4 性能优化

#### CDS / AOT 演进

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 310](performance/jep-310.md) | Application Class-Data Sharing | 10 | ✅ 正式 |
| [JEP 341](performance/jep-341.md) | Default CDS Archives | 12 | ✅ 正式 |
| [JEP 350](performance/jep-350.md) | Dynamic CDS Archives | 13 | ✅ 正式 |
| [JEP 514](performance/jep-514.md) | AOT Command-Line Ergonomics | 25 | ✅ 正式 |
| [JEP 515](performance/jep-515.md) | AOT Method Profiling | 25 | ✅ 正式 |
| [JEP 516](performance/jep-516.md) | AOT Cache | 26 | ✅ 正式 |

#### 运行时优化

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 243](performance/jep-243.md) | JVMCI | 9 | ✅ 正式 |
| [JEP 374](performance/jep-374.md) | Disable and Deprecate Biased Locking | 15 | ✅ 正式 |
| [JEP 387](performance/jep-387.md) | Elastic Metaspace | 16 | ✅ 正式 |
| [JEP 502](performance/jep-502.md) | Stable Values (Preview) | 25 | 🔍 预览 |
| [JEP 528](performance/jep-528.md) | Stable Values (2nd Preview) | 26 | 🔍 预览 |
| [JEP 503](performance/jep-503.md) | Remove 32-bit x86 Port | 25 | 🗑️ 移除 |

---

### 1.5 安全特性

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 510](security/jep-510.md) | Key Derivation Function API | 25 | ✅ 正式 |
| [JEP 470](security/jep-470.md) | PEM Encodings (Preview) | 25 | 🔍 预览 |
| [JEP 498](security/jep-498.md) | Warn upon Use of sun.misc.Unsafe Memory Access | 24 | ✅ 正式 |
| [JEP 497](security/jep-497.md) | Quantum-Resistant ML-DSA (FIPS 204) | 24 | ✅ 正式 |
| [JEP 496](security/jep-496.md) | Quantum-Resistant ML-KEM (FIPS 203) | 24 | ✅ 正式 |
| [JEP 486](security/jep-486.md) | Permanently Disable the Security Manager | 24 | ✅ 正式 |
| [JEP 452](security/jep-452.md) | Key Encapsulation Mechanism API | 21 | ✅ 正式 |
| [JEP 451](security/jep-451.md) | Prepare to Restrict Dynamic Agent Loading | 21 | ⚠️ 警告 |
| [JEP 415](security/jep-415.md) | Context-Specific Deserialization Filters | 17 | ✅ 正式 |
| [JEP 411](security/jep-411.md) | Deprecate the Security Manager for Removal | 17 | 🗑️ 废弃 |
| [JEP 332](security/jep-332.md) | TLS 1.3 | 11 | ✅ 正式 |
| [JEP 329](security/jep-329.md) | ChaCha20-Poly1305 | 11 | ✅ 正式 |
| [JEP 290](security/jep-290.md) | Filter Incoming Serialization Data | 9 | ✅ 正式 |

---

### 1.6 工具改进

#### Source Launcher 演进

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 330](tools/jep-330.md) | Launch Single-File Source-Code Programs | 11 | ✅ 正式 |
| [JEP 458](tools/jep-458.md) | Launch Multi-File Source-Code Programs | 22 | ✅ 正式 |
| [JEP 495](tools/jep-495.md) | Simple Source Files (4th Preview) | 24 | 🔍 预览 |

#### Class-File API 演进

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 457](tools/jep-457.md) | Class-File API (Preview) | 22 | 🔍 预览 |
| [JEP 466](tools/jep-466.md) | Class-File API (2nd Preview) | 23 | 🔍 预览 |
| [JEP 484](tools/jep-484.md) | Class-File API | 24 | ✅ 正式 |

#### Vector API

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 338](language/jep-338.md) | Vector API (Incubator) | 16 | 🥚 孵化 |
| [JEP 414](tools/jep-414.md) | Vector API (2nd Incubator) | 17 | 🥚 孵化 |
| [JEP 448](tools/jep-448.md) | Vector API (6th Incubator) | 21 | 🥚 孵化 |
| [JEP 460](tools/jep-460.md) | Vector API (7th Incubator) | 22 | 🥚 孵化 |
| [JEP 469](tools/jep-469.md) | Vector API (8th Incubator) | 23 | 🥚 孵化 |
| [JEP 529](language/jep-529.md) | Vector API (11th Incubator) | 26 | 🥚 孵化 |

#### 其他工具

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 526](tools/jep-526.md) | Lazy Constants (Preview) | 26 | 🔍 预览 |
| [JEP 511](tools/jep-511.md) | Module Import Declarations | 25 | ✅ 正式 |
| [JEP 493](tools/jep-493.md) | Linking Run-Time Images without JMOD Files | 24 | ✅ 正式 |
| [JEP 485](tools/jep-485.md) | Stream Gatherers | 24 | ✅ 正式 |
| [JEP 483](tools/jep-483.md) | Ahead-of-Time Class Loading & Linking | 24 | ✅ 正式 |
| [JEP 467](tools/jep-467.md) | Markdown Documentation Comments | 23 | ✅ 正式 |
| [JEP 416](tools/jep-416.md) | Code Snippets in Java API Documentation | 18 | ✅ 正式 |
| [JEP 408](tools/jep-408.md) | Simple Web Server | 18 | ✅ 正式 |
| [JEP 392](tools/jep-392.md) | Packaging Tool | 16 | ✅ 正式 |
| [JEP 343](tools/jep-343.md) | Packaging Tool (Incubator) | 14 | 🥚 孵化 |
| [JEP 282](tools/jep-282.md) | jlink | 9 | ✅ 正式 |
| [JEP 238](tools/jep-238.md) | Multi-Release JAR Files | 9 | ✅ 正式 |
| [JEP 222](tools/jep-222.md) | jshell (REPL) | 9 | ✅ 正式 |

#### 已废弃/移除

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 410](tools/jep-410.md) | Remove Experimental AOT/JIT Compiler | 17 | 🗑️ 移除 |
| [JEP 407](tools/jep-407.md) | Remove RMI Activation | 17 | 🗑️ 移除 |
| [JEP 398](tools/jep-398.md) | Deprecate Applet API | 17 | 🗑️ 废弃 |
| [JEP 385](tools/jep-385.md) | Deprecate RMI Activation | 15 | 🗑️ 废弃 |
| [JEP 372](tools/jep-372.md) | Remove Nashorn | 15 | 🗑️ 移除 |

---

### 1.7 外部函数与内存 (FFI)

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 370](ffi/jep-370.md) | Foreign-Memory Access API (Incubator) | 14 | 🥚 孵化 |
| [JEP 383](ffi/jep-383.md) | Foreign-Memory Access API (2nd Incubator) | 15 | 🥚 孵化 |
| [JEP 389](ffi/jep-389.md) | Foreign Linker API (Incubator) | 16 | 🥚 孵化 |
| [JEP 393](ffi/jep-393.md) | Foreign-Memory Access API (3rd Incubator) | 16 | 🥚 孵化 |
| [JEP 412](ffi/jep-412.md) | Foreign Function & Memory API (Incubator) | 17 | 🥚 孵化 |
| [JEP 442](ffi/jep-442.md) | Foreign Function & Memory API (3rd Preview) | 21 | 🔍 预览 |
| [JEP 454](ffi/jep-454.md) | Foreign Function & Memory API | 22 | ✅ 正式 |
| [JEP 472](ffi/jep-472.md) | Prepare to Restrict JNI | 24 | ⚠️ 警告 |

---

### 1.8 平台移植

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 501](platform/jep-501.md) | Deprecate 32-bit x86 Port | 24 | 🗑️ 废弃 |
| [JEP 422](ffi/jep-422.md) | Linux/RISC-V Port | 19 | ✅ 正式 |
| [JEP 391](platform/jep-391.md) | macOS/AArch64 Port (Apple Silicon) | 17 | ✅ 正式 |
| [JEP 388](platform/jep-388.md) | Windows/AArch64 Port | 16 | ✅ 正式 |
| [JEP 386](platform/jep-386.md) | Alpine Linux Port (musl libc) | 16 | ✅ 正式 |
| [JEP 381](platform/jep-381.md) | Remove Solaris/SPARC | 15 | 🗑️ 移除 |
| [JEP 365](platform/jep-365.md) | ZGC on Windows | 14 | ✅ 正式 |
| [JEP 364](platform/jep-364.md) | ZGC on macOS | 14 | ✅ 正式 |
| [JEP 362](platform/jep-362.md) | Deprecate Solaris/SPARC | 14 | 🗑️ 废弃 |
| [JEP 358](platform/jep-358.md) | Apple Silicon Support | 14 | ✅ 正式 |
| [JEP 340](platform/jep-340.md) | One AArch64 Port, Not Two | 12 | ✅ 正式 |
| [JEP 307](platform/jep-307.md) | Container Awareness | 10 | ✅ 正式 |
| [JEP 237](ffi/jep-237.md) | AArch64 Port | 9 | ✅ 正式 |

---

### 1.9 网络

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 517](network/jep-517.md) | HTTP/3 for HTTP Client | 26 | ✅ 正式 |
| [JEP 380](network/jep-380.md) | Unix Domain Sockets | 16 | ✅ 正式 |
| [JEP 321](network/jep-321.md) | HTTP Client | 11 | ✅ 正式 |

---

### 1.10 监控诊断 (JFR)

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 520](jfr/jep-520.md) | JFR Method Timing and Tracing | 25 | ✅ 正式 |
| [JEP 518](jfr/jep-518.md) | JFR Cooperative Sampling | 25 | ✅ 正式 |
| [JEP 509](jfr/jep-509.md) | JFR CPU-Time Profiling | 25 | 🧪 实验 |
| [JEP 328](jfr/jep-328.md) | Java Flight Recorder | 11 | ✅ 正式 |

---

### 1.11 客户端与 API

| JEP | 标题 | JDK | 状态 |
|-----|------|-----|------|
| [JEP 264](api/jep-264.md) | Platform Logging API | 9 | ✅ 正式 |
| [JEP 353](api/jep-353.md) | JSON Processing API | - | 🔬 草案 |
| [JEP 382](client/jep-382.md) | Metal Rendering Pipeline (macOS) | 17 | ✅ 正式 |
| [JEP 471](api/jep-471.md) | JSON Binding (JSON.B) | - | 🔬 草案 |
| [JEP 489](api/jep-489.md) | JSON Escaping | - | 🔬 草案 |

---

## 2. 按版本浏览

| 版本 | 类型 | GA 日期 | 链接 |
|------|------|---------|------|
| JDK 26 | Feature | 2026-03 | [→](../by-version/jdk26/) |
| JDK 25 | **LTS** | 2025-09 | [→](../by-version/jdk25/) |
| JDK 24 | Feature | 2025-03 | [→](../by-version/jdk24/) |
| JDK 23 | Feature | 2024-09 | [→](../by-version/jdk23/) |
| JDK 22 | Feature | 2024-03 | [→](../by-version/jdk22/) |
| JDK 21 | LTS | 2023-09 | [→](../by-version/jdk21/) |
| JDK 17 | LTS | 2021-09 | [→](../by-version/jdk17/) |
| JDK 11 | LTS | 2018-09 | [→](../by-version/jdk11/) |
| JDK 8 | LTS | 2014-03 | [→](../by-version/jdk8/) |

---

## 3. JEP 状态说明

| 图标 | 状态 | 含义 |
|------|------|------|
| ✅ | 正式 (Final) | 已交付的最终特性 |
| 🔍 | 预览 (Preview) | 需要 `--enable-preview` 启用 |
| 🥚 | 孵化 (Incubator) | jdk.incubator.* 模块 |
| 🧪 | 实验 (Experimental) | 需要 `-XX:+UnlockExperimentalVMOptions` |
| ⚠️ | 警告 (Warning) | 运行时发出废弃/迁移警告 |
| 🗑️ | 废弃/移除 | Deprecated for Removal / Removed |
| 🔬 | 草案 (Draft) | 尚未正式交付 |

---

## 4. JSR 与 JEP

许多重要特性同时有 JSR（规范）和 JEP（实现）：

| 特性 | JSR | JEP | 说明 |
|------|-----|-----|------|
| Lambda | [JSR 335](/jsr/language/jsr-335.md) | [JEP 126](language/jep-126.md) | JSR 定义语法，JEP 实现编译 |
| Date & Time | JSR 310 | [JEP 150](language/jep-150.md) | java.time 包 |
| Records | [JSR 395](/jsr/language/jsr-395.md) | [JEP 395](language/jep-395.md) | 同编号 |
| Sealed Classes | [JSR 397](/jsr/language/jsr-397.md) | [JEP 409](language/jep-409.md) | 不同编号 |
| 模块系统 | [JSR 376](/jsr/platform/jsr-376.md) | [JEP 261](language/jep-261.md) | JSR 定义规范，JEP 实现 |

> **详见**: [JSR 索引](/jsr/)

---

## 5. 相关链接

- [OpenJDK JEP Index](https://openjdk.org/jeps/)
- [JSR 索引](/jsr/)
- [JDK 21 Features](https://openjdk.org/projects/jdk/21/)
- [JDK 22 Features](https://openjdk.org/projects/jdk/22/)
- [JDK 23 Features](https://openjdk.org/projects/jdk/23/)
- [JDK 24 Features](https://openjdk.org/projects/jdk/24/)
- [JDK 25 Features](https://openjdk.org/projects/jdk/25/)
- [JDK 26 Features](https://openjdk.org/projects/jdk/26/)
