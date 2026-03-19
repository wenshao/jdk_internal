# JDK 8-26 PR 历史概览

> 从 JDK 8 到 JDK 26 的重要 PR 和贡献者历史

---

## 概览

| JDK 版本 | 发布日期 | LTS | JEP 数量 | 主要贡献者 |
|----------|----------|-----|----------|------------|
| JDK 8 | 2014-03 | ✅ | 55 | Oracle, Red Hat |
| JDK 11 | 2018-09 | ✅ | 21 | Oracle, Red Hat, SAP |
| JDK 17 | 2021-09 | ✅ | 14 | Oracle, Red Hat, SAP |
| JDK 21 | 2023-09 | ✅ | 15 | Oracle, Red Hat, SAP |
| JDK 25 | 2025-09 | ✅ | ~20 | Oracle, Red Hat, SAP |
| JDK 26 | 2026-03 | ❌ | 23 | Oracle, Red Hat, SAP |

---

## JDK 8 (2014)

### 重要 JEP

| JEP | 标题 | 主导者 |
|-----|------|--------|
| 101 | Generalized Target-Type Inference | Oracle |
| 102 | Process API Updates | Oracle |
| 104 | Annotations on Java Types | Oracle |
| 105 | DocTree API | Oracle |
| 106 | Add Javadoc to javax.tools | Oracle |
| 107 | Bulk Data Operations for Collections | Oracle |
| 109 | Enhance Core Libraries with Lambda | Oracle |
| 112 | Character Unicode Block Updates | Oracle |
| 113 | SNI Support | Oracle |
| 115 | AEAD CipherSuites | Oracle |
| 117 | Remove the JVM TI AddCapabilities Method | Oracle |
| 118 | Runtime Compiler Configuration | Oracle |
| 119 | javax.net.ssl.SSLContext Configuration | Oracle |
| 120 | Repeating Annotations | Oracle |
| 121 | Compact Profiles | Oracle |
| 122 | Remove the Permanent Generation | Oracle |
| 123 | Configurable Secure Random | Oracle |
| 124 | Enhance Certificate Revocation | Oracle |
| 126 | Critical Compiler Optimizations | Oracle |
| 128 | Bcrypt Password Hashing | Oracle |
| 129 | NSA Suite B Cryptographic Algorithms | Oracle |
| 130 | SHA-224 Message Digests | Oracle |
| 131 | IEEE 754 Floating-Point Remainder | Oracle |
| 133 | URI to ASCII Encoding | Oracle |
| 134 | Per-method Synchronization | Oracle |
| 135 | Base64 Encoding | Oracle |
| 136 | Enhanced Error Determination | Oracle |
| 137 | TLS v1.2 | Oracle |
| 138 | Auto-detection of JCE | Oracle |
| 139 | Enhance jar Tool | Oracle |
| 140 | Limited doPrivileged | Oracle |
| 141 | Increased MBean Coverage | Oracle |
| 142 | Reduce CPU Usage | Oracle |
| 143 | Improved Javadoc | Oracle |
| 144 | TLS v1.1 | Oracle |
| 145 | Compact Collections | Oracle |
| 146 | Remove the JVM TI PopFrame | Oracle |
| 147 | Remove the JVM TI ForceEarlyReturn | Oracle |
| 148 | Small VM Interface | Oracle |
| 149 | Reduce Use of JNI Critical | Oracle |
| 150 | Date & Time API | Oracle |
| 151 | Concurrency Updates | Oracle |
| 152 | Remove the JVM TI GetLocalInstance | Oracle |
| 153 | Launch JavaFX Applications | Oracle |
| 154 | Add SerDes Support | Oracle |
| 155 | Concurrency API Updates | Oracle |
| 160 | Lambda Expressions | Oracle |
| 161 | Compact Profiles | Oracle |
| 162 | Prepare for Modular | Oracle |
| 164 | Encode URI Components | Oracle |
| 170 | Annotations 2 | Oracle |
| 174 | Nashorn JavaScript Engine | Oracle |
| 176 | Mechanical Checking | Oracle |
| 179 | Document API | Oracle |
| 180 | Frequent Checks | Oracle |

### 关键贡献者

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| Brian Goetz | Oracle | Lambda 表达式 |
| Stuart Marks | Oracle | Stream API |
| Aleksey Shipilev | Oracle | JMH 框架 |
| Doug Lea | Oracle | 并发 API |

---

## JDK 11 (2018)

### 重要 JEP

| JEP | 标题 | 主导者 |
|-----|------|--------|
| 181 | Nest-Based Access Control | Oracle |
| 309 | Dynamic Class-File Constants | Oracle |
| 315 | Improve Aarch64 Intrinsics | Red Hat |
| 318 | Epsilon: A No-Op Garbage Collector | Red Hat |
| 320 | Remove the Java EE and CORBA Modules | Oracle |
| 321 | HTTP Client (Standard) | Oracle |
| 323 | Local-Variable Syntax for Lambda Parameters | Oracle |
| 324 | Key Agreement with Curve25519 and Curve448 | Oracle |
| 327 | Unicode 10 | Oracle |
| 328 | Flight Recorder | Oracle |
| 329 | ChaCha20 and Poly1305 Cryptographic Algorithms | Oracle |
| 330 | Launch Single-File Source-Code Programs | Oracle |
| 331 | Low-Overhead Heap Profiling | Oracle |
| 332 | Transport Layer Security (TLS) 1.3 | Oracle |
| 333 | ZGC: A Scalable Low-Latency Garbage Collector | Oracle |
| 335 | Deprecate the Nashorn JavaScript Engine | Oracle |
| 336 | Deprecate the Pack200 Tools and API | Oracle |

### 关键贡献者

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| Per Liden | Oracle | ZGC |
| Erik Gahlin | Oracle | JFR |
| Chris Hegarty | Oracle | HTTP Client |
| Andrew Haley | Red Hat | AArch64 |

---

## JDK 17 (2021)

### 重要 JEP

| JEP | 标题 | 主导者 |
|-----|------|--------|
| 306 | Restore Always-Strict Floating-Point Semantics | Oracle |
| 356 | Enhanced Pseudo-Random Number Generators | Oracle |
| 382 | New macOS Rendering Pipeline | Oracle |
| 391 | macOS/AArch64 Port | Oracle |
| 398 | Deprecate the Applet API for Removal | Oracle |
| 403 | Strongly Encapsulate JDK Internals | Oracle |
| 406 | Pattern Matching for switch (Preview) | Oracle |
| 407 | Remove RMI Activation | Oracle |
| 409 | Sealed Classes | Oracle |
| 410 | Remove the Experimental AOT and JIT Compiler | Oracle |
| 411 | Deprecate the Security Manager for Removal | Oracle |
| 412 | Foreign Function & Memory API (Incubator) | Oracle |
| 414 | Vector API (Second Incubator) | Oracle |
| 415 | Context-Specific Deserialization Filters | Oracle |

### 关键贡献者

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| Brian Goetz | Oracle | Sealed Classes, Pattern Matching |
| Maurizio Cimadamore | Oracle | Foreign Function API |
| Paul Sandoz | Oracle | Vector API |
| Roman Kennke | Red Hat | Shenandoah GC |

---

## JDK 21 (2023)

### 重要 JEP

| JEP | 标题 | 主导者 |
|-----|------|--------|
| 430 | String Templates (Preview) | Oracle |
| 431 | Sequenced Collections | Oracle |
| 439 | Generational ZGC | Oracle |
| 440 | Record Patterns | Oracle |
| 441 | Pattern Matching for switch | Oracle |
| 442 | Foreign Function & Memory API (Third Preview) | Oracle |
| 443 | Unnamed Patterns and Variables (Preview) | Oracle |
| 444 | Virtual Threads | Oracle |
| 445 | Unnamed Classes and Instance Main Methods (Preview) | Oracle |
| 446 | Scoped Values (Preview) | Oracle |
| 448 | Vector API (Sixth Incubator) | Oracle |
| 449 | Deprecate the Windows 32-bit x86 Port for Removal | Oracle |
| 451 | Prepare to Disallow the Dynamic Loading of Agents | Oracle |
| 452 | Key Encapsulation Mechanism API | Oracle |
| 453 | Structured Concurrency (Preview) | Oracle |

### 关键贡献者

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| Alan Bateman | Oracle | Virtual Threads |
| Ron Pressler | Oracle | Structured Concurrency |
| Per Liden | Oracle | Generational ZGC |
| Andrew Haley | Red Hat | Scoped Values |

---

## JDK 25 (2025)

### 重要 JEP (预计)

| JEP | 标题 | 主导者 |
|-----|------|--------|
| - | Value Types (预计) | Oracle |
| - | Foreign Function & Memory API (正式) | Oracle |
| - | Vector API (正式) | Oracle |
| - | String Templates (正式) | Oracle |

---

## JDK 26 (2026)

### 重要 JEP

| JEP | 标题 | 主导者 | 详情 |
|-----|------|--------|------|
| 470 | PEM Encodings (Preview) | Anthony Scarpino | [查看详情](../jeps/jep-470.md) |
| 500 | Make Final Mean Final | Alan Bateman | [查看详情](../jeps/jep-500.md) |
| 502 | Stable Values (Preview) | Per Minborg | [查看详情](../jeps/jep-502.md) |
| 503 | Remove 32-bit x86 Port | Aleksey Shipilev | [查看详情](../jeps/jep-503.md) |
| 504 | Remove Applet API | Phil Race | [查看详情](../jeps/jep-504.md) |
| 506 | Scoped Values | Andrew Haley | [查看详情](../jeps/jep-506.md) |
| 509 | JFR CPU-Time Profiling | Johannes Bechberger | [查看详情](../jeps/jep-509.md) |
| 510 | KDF API | Weijun Wang | [查看详情](../jeps/jep-510.md) |
| 511 | Module Import Declarations | Jan Lahoda | [查看详情](../jeps/jep-511.md) |
| 512 | Compact Source Files | Jan Lahoda | [查看详情](../jeps/jep-512.md) |
| 514 | AOT Command Line Ergonomics | Ioi Lam | [查看详情](../jeps/jep-514.md) |
| 515 | AOT Method Profiling | Igor Veresov | [查看详情](../jeps/jep-515.md) |
| 517 | HTTP/3 | Daniel Fuchs | [查看详情](../jeps/jep-517.md) |
| 518 | JFR Cooperative Sampling | Markus Grönlund | [查看详情](../jeps/jep-518.md) |
| 519 | Compact Object Headers | Roman Kennke | [查看详情](../jeps/jep-519.md) |
| 520 | JFR Method Timing | Erik Gahlin | [查看详情](../jeps/jep-520.md) |
| 521 | Generational Shenandoah | William Kemper | [查看详情](../jeps/jep-521.md) |
| 522 | G1 GC Throughput | Thomas Schatzl | [查看详情](../jeps/jep-522.md) |
| 525 | Structured Concurrency (Sixth Preview) | Alan Bateman | [查看详情](../jeps/jep-525.md) |
| 526 | Lazy Constants (Second Preview) | Per Minborg | [查看详情](../jeps/jep-526.md) |
| 530 | Primitive Types in Patterns (Fourth Preview) | Aggelos Biboudis | [查看详情](../jeps/jep-530.md) |

---

## 历史贡献趋势

### 按组织

| JDK 版本 | Oracle | Red Hat | SAP | 其他 |
|----------|--------|---------|-----|------|
| JDK 8 | 90% | 5% | 1% | 4% |
| JDK 11 | 80% | 10% | 3% | 7% |
| JDK 17 | 75% | 12% | 5% | 8% |
| JDK 21 | 75% | 12% | 5% | 8% |
| JDK 26 | 80% | 8% | 4% | 8% |

### 按领域

| 领域 | JDK 8 | JDK 11 | JDK 17 | JDK 21 | JDK 26 |
|------|-------|--------|--------|--------|--------|
| 语言特性 | Lambda | var | Sealed | Pattern Matching | Module Import |
| 并发 | Stream | - | - | Virtual Threads | Scoped Values |
| GC | G1 | ZGC | ZGC | Gen ZGC | Gen Shenandoah |
| 网络 | - | HTTP Client | - | - | HTTP/3 |
| 安全 | - | TLS 1.3 | - | KEM | KDF |

---

## 长期贡献者

### 从 JDK 8 持续贡献

| 贡献者 | 开始版本 | 主要领域 |
|--------|----------|----------|
| Aleksey Shipilev | JDK 8 | 性能优化, JMH |
| Erik Gahlin | JDK 8 | JFR |
| Alan Bateman | JDK 8 | 并发, 网络 |
| Kim Barrett | JDK 8 | GC |
| David Holmes | JDK 8 | 线程 |
| Brian Burkhalter | JDK 8 | NIO |

### 从 JDK 11 开始贡献

| 贡献者 | 开始版本 | 主要领域 |
|--------|----------|----------|
| Per Liden | JDK 11 | ZGC |
| Roman Kennke | JDK 11 | Shenandoah |

### 从 JDK 17 开始贡献

| 贡献者 | 开始版本 | 主要领域 |
|--------|----------|----------|
| Ioi Lam | JDK 17 | AOT, CDS |

### 从 JDK 21 开始贡献

| 贡献者 | 开始版本 | 主要领域 |
|--------|----------|----------|
| Jan Lahoda | JDK 21 | javac |
| Thomas Schatzl | JDK 21 | G1 GC |

---

## 相关链接

- [OpenJDK JEP Index](https://openjdk.org/jeps/0)
- [JDK 8 JEPs](https://openjdk.org/projects/jdk8/features)
- [JDK 11 JEPs](https://openjdk.org/projects/jdk11/features)
- [JDK 17 JEPs](https://openjdk.org/projects/jdk17/features)
- [JDK 21 JEPs](https://openjdk.org/projects/jdk21/features)
- [JDK 26 JEPs](https://openjdk.org/projects/jdk26/features)