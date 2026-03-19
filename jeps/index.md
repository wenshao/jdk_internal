# JEP 索引

> JDK Enhancement Proposals - JDK 增强提案索引

---

## 概述

JEP (JDK Enhancement Proposals) 是 Java 平台新特性的设计和规范文档。本目录包含 JDK 21-26 相关的重要 JEP 分析文档，**按主题分类组织**。

---

## 按主题浏览

### 并发编程

| JEP | 标题 | JDK | 状态 | 文档 |
|-----|------|-----|------|------|
| [JEP 444](concurrency/jep-444.md) | Virtual Threads | 21 | ✅ 正式 | [→](concurrency/jep-444.md) |
| [JEP 462](concurrency/jep-462.md) | Structured Concurrency (2nd) | 22 | 🔍 预览 | [→](concurrency/jep-462.md) |
| [JEP 505](concurrency/jep-505.md) | Structured Concurrency (5th) | 25 | 🔍 鐄览 | [→](concurrency/jep-505.md) |
| [JEP 525](concurrency/jep-525.md) | Structured Concurrency (6th) | 26 | 🔍 预览 | [→](concurrency/jep-525.md) |
| [JEP 446](concurrency/jep-446.md) | Scoped Values | 25 | ✅ 正式 | [→](concurrency/jep-446.md) |
| [JEP 506](concurrency/jep-506.md) | Scoped Values | 25 | ✅ 正式 | [→](concurrency/jep-506.md) |
| [JEP 526](tools/jep-526.md) | Lazy Constants | 26 | 🔍 预览 | [→](tools/jep-526.md) |
| [JEP 491](concurrency/jep-491.md) | Synchronization without Blocking | 25 | ✅ 正式 | [→](concurrency/jep-491.md) |

### 垃圾收集 (GC)

| JEP | 标题 | JDK | 状态 | 文档 |
|-----|------|-----|------|------|
| [JEP 439](gc/jep-439.md) | Generational ZGC | 21 | ✅ 正式 | [→](gc/jep-439.md) |
| [JEP 474](gc/jep-474.md) | ZGC Generational by Default | 23 | ✅ 正式 | [→](gc/jep-474.md) |
| [JEP 490](gc/jep-490.md) | ZGC Remove Non-Generational Mode | 24 | ✅ 正式 | [→](gc/jep-490.md) |
| [JEP 423](gc/jep-423.md) | Region Pinning for G1 | 22 | ✅ 正式 | [→](gc/jep-423.md) |
| [JEP 475](gc/jep-475.md) | Late Barrier Expansion for G1 | 24 | ✅ 正式 | [→](gc/jep-475.md) |
| [JEP 522](gc/jep-522.md) | G1 GC Throughput Improvement | 26 | ✅ 正式 | [→](gc/jep-522.md) |
| [JEP 521](gc/jep-521.md) | Generational Shenandoah | 25 | ✅ 正式 | [→](gc/jep-521.md) |
| [JEP 519](gc/jep-519.md) | Compact Object Headers | 25 | ✅ 正式 | [→](gc/jep-519.md) |

### 语言特性

| JEP | 标题 | JDK | 状态 | 文档 |
|-----|------|-----|------|------|
| [JEP 445](language/jep-445.md) | Unnamed Classes & Instance Main Methods | 21 | 🔍 预览 | [→](language/jep-445.md) |
| [JEP 456](language/jep-456.md) | Unnamed Variables & Patterns | 22 | ✅ 正式 | [→](language/jep-456.md) |
| [JEP 463](language/jep-463.md) | Implicit Classes & Instance Main (2nd) | 22 | 🔍 预览 | [→](language/jep-463.md) |
| [JEP 477](language/jep-477.md) | Implicit Classes & Instance Main (3rd) | 23 | ✅ 正式 | [→](language/jep-477.md) |
| [JEP 430](language/jep-430.md) | String Templates | 21 | ⚠️ 撤回 | [→](language/jep-430.md) |
| [JEP 507](language/jep-507.md) | Primitive Types in Patterns (3rd) | 25 | 🔍 预览 | [→](language/jep-507.md) |
| [JEP 530](language/jep-530.md) | Primitive Types in Patterns (4th) | 26 | 🔍 预览 | [→](language/jep-530.md) |
| [JEP 458](language/jep-458.md) | Vector API (1st) | 23 | 🔍 预览 | [→](language/jep-458.md) |
| [JEP 449](language/jep-449.md) | Snippet Tagging | 23 | 🔍 预览 | [→](language/jep-449.md) |

### 外部函数 (FFI)

| JEP | 标题 | JDK | 状态 | 文档 |
|-----|------|-----|------|------|
| [JEP 454](ffi/jep-454.md) | Foreign Function & Memory API | 22 | ✅ 正式 | [→](ffi/jep-454.md) |
| [JEP 472](ffi/jep-472.md) | Prepare to Restrict JNI | 24 | ⚠️ 废弃警告 | [→](ffi/jep-472.md) |

### 安全特性

| JEP | 标题 | JDK | 状态 | 文档 |
|-----|------|-----|------|------|
| [JEP 451](security/jep-451.md) | Prepare to Restrict Dynamic Loading | 21 | ⚠️ 废弃 | [→](security/jep-451.md) |
| [JEP 452](security/jep-452.md) | Key Encapsulation Mechanism API | 21 | ✅ 正式 | [→](security/jep-452.md) |
| [JEP 470](security/jep-470.md) | PEM Encodings | 25 | 🔍 预览 | [→](security/jep-470.md) |
| [JEP 510](security/jep-510.md) | Key Derivation Function API | 25 | ✅ 正式 | [→](security/jep-510.md) |

### 监控诊断 (JFR)

| JEP | 标题 | JDK | 状态 | 文档 |
|-----|------|-----|------|------|
| [JEP 509](jfr/jep-509.md) | JFR CPU-Time Profiling | 25 | 🔧 实验 | [→](jfr/jep-509.md) |
| [JEP 518](jfr/jep-518.md) | JFR Cooperative Sampling | 25 | ✅ 正式 | [→](jfr/jep-518.md) |
| [JEP 520](jfr/jep-520.md) | JFR Method Timing & Tracing | 25 | ✅ 正式 | [→](jfr/jep-520.md) |

### 工具改进

| JEP | 标题 | JDK | 状态 | 文档 |
|-----|------|-----|------|------|
| [JEP 467](tools/jep-467.md) | Markdown Documentation Comments | 23 | ✅ 正式 | [→](tools/jep-467.md) |
| [JEP 466](tools/jep-466.md) | Class-File API (2nd) | 23 | 🔍 预览 | [→](tools/jep-466.md) |
| [JEP 484](tools/jep-484.md) | Class-File API | 24 | ✅ 正式 | [→](tools/jep-484.md) |
| [JEP 511](tools/jep-511.md) | Module Import Declarations | 25 | ✅ 正式 | [→](tools/jep-511.md) |
| [JEP 512](tools/jep-512.md) | Compact Source Files | 25 | ✅ 正式 | [→](tools/jep-512.md) |

### 性能优化

| JEP | 标题 | JDK | 状态 | 文档 |
|-----|------|-----|------|------|
| [JEP 502](performance/jep-502.md) | Stable Values | 25 | 🔍 预览 | [→](performance/jep-502.md) |
| [JEP 503](performance/jep-503.md) | Remove 32-bit x86 Port | 25 | 🗑️ 移除 | [→](performance/jep-503.md) |
| [JEP 514](performance/jep-514.md) | AOT Command-Line Ergonomics | 25 | ✅ 正式 | [→](performance/jep-514.md) |
| [JEP 515](performance/jep-515.md) | AOT Method Profiling | 25 | ✅ 正式 | [→](performance/jep-515.md) |

### 网络改进

| JEP | 标题 | JDK | 状态 | 文档 |
|-----|------|-----|------|------|
| [JEP 517](network/jep-517.md) | HTTP/3 for HTTP Client | 26 | 🔍 预览 | [→](network/jep-517.md) |

### 已移除特性

| JEP | 标题 | JDK | 状态 | 文档 |
|-----|------|-----|------|------|
| [JEP 500](removed/jep-500.md) | Prepare to Make Final Mean Final | 26 | 🗑️ 移除 | [→](removed/jep-500.md) |
| [JEP 503](performance/jep-503.md) | Remove 32-bit x86 Port | 25 | 🗑️ 移除 | [→](performance/jep-503.md) |
| [JEP 504](removed/jep-504.md) | Remove Applet API | 26 | 🗑️ 移除 | [→](removed/jep-504.md) |

---

## JSR 与 JEP

许多重要特性同时有 JSR (规范) 和 JEP (实现)：

| 特性 | JSR | JEP | 说明 |
|------|-----|-----|------|
| Lambda | [JSR 335](/jsr/language/jsr-335.md) | JEP 126 | JSR 定义语法， JEP 实现编译 |
| Records | [JSR 395](/jsr/language/jsr-395.md) | JEP 395 | 同编号 |
| Sealed Classes | [JSR 397](/jsr/language/jsr-397.md) | JEP 409 | 不同编号 |
| 模块系统 | [JSR 376](/jsr/platform/jsr-376.md) | JEP 261 | JSR 定义规范， JEP 实现 |

> **详见**: [JSR 索引](/jsr/)

---

## 按版本浏览

- [JDK 21 JEPs](by-version/jdk21.md)
- [JDK 22 JEPs](by-version/jdk22.md)
- [JDK 23 JEPs](by-version/jdk23.md)
- [JDK 24 JEPs](by-version/jdk24.md)
- [JDK 25 JEPs](by-version/jdk25.md)
- [JDK 26 JEPs](by-version/jdk26.md)

---

## 相关链接

- [OpenJDK JEP Index](https://openjdk.org/jeps/)
- [JSR 索引](/jsr/)
- [JDK 21 Features](https://openjdk.org/projects/jdk/21/)
- [JDK 22 Features](https://openjdk.org/projects/jdk/22/)
- [JDK 23 Features](https://openjdk.org/projects/jdk/23/)
