# JEP 索引

> JDK Enhancement Proposals - JDK 增强提案索引

---

## 概述

JEP (JDK Enhancement Proposals) 是 Java 平台新特性的设计和规范文档。本目录包含 JDK 21-26 相关的重要 JEP 分析文档。

---

## JEP 分类索引

### 语言特性

| JEP | 标题 | JDK | 状态 | 文档 |
|-----|------|-----|------|------|
| [JEP 445](jep-445.md) | Unnamed Classes & Instance Main Methods | 21 | 🔍 预览 | [→](jep-445.md) |
| [JEP 444](jep-444.md) | Virtual Threads | 21 | ✅ 正式 | [→](jep-444.md) |
| [JEP 430](jep-430.md) | String Templates (已撤回) | 21 | ⚠️ 撤回 | [→](jep-430.md) |
| [JEP 454](jep-454.md) | Foreign Function & Memory API | 22 | ✅ 正式 | [→](jep-454.md) |
| [JEP 456](jep-456.md) | Unnamed Variables & Patterns | 22 | ✅ 正式 | [→](jep-456.md) |
| [JEP 463](jep-463.md) | Implicit Classes & Instance Main (2nd) | 22 | 🔍 预览 | [→](jep-463.md) |
| [JEP 462](jep-462.md) | Structured Concurrency (2nd) | 22 | 🔍 预览 | [→](jep-462.md) |
| [JEP 477](jep-477.md) | Implicit Classes & Instance Main (3rd) | 23 | ✅ 正式 | [→](jep-477.md) |
| [JEP 467](jep-467.md) | Markdown Documentation Comments | 23 | ✅ 正式 | [→](jep-467.md) |
| [JEP 466](jep-466.md) | Class-File API (2nd) | 23 | 🔍 预览 | [→](jep-466.md) |
| [JEP 484](jep-484.md) | Class-File API | 24 | ✅ 正式 | [→](jep-484.md) |
| [JEP 505](jep-505.md) | Structured Concurrency (5th) | 25 | 🔍 预览 | [→](jep-505.md) |
| [JEP 507](jep-507.md) | Primitive Types in Patterns (3rd) | 25 | 🔍 预览 | [→](jep-507.md) |
| [JEP 502](jep-502.md) | Stable Values | 25 | 🔍 预览 | [→](jep-502.md) |
| [JEP 506](jep-506.md) | Scoped Values | 25 | ✅ 正式 | [→](jep-506.md) |
| [JEP 508](jep-508.md) | Vector API (10th) | 25 | 🔧 孵化 | [→](jep-508.md) |
| [JEP 511](jep-511.md) | Module Import Declarations | 25 | ✅ 正式 | [→](jep-511.md) |
| [JEP 512](jep-512.md) | Compact Source Files & Instance Main | 25 | ✅ 正式 | [→](jep-512.md) |
| [JEP 513](jep-513.md) | Flexible Constructor Bodies | 25 | ✅ 正式 | [→](jep-513.md) |
| [JEP 500](jep-500.md) | Prepare to Make Final Mean Final | 26 | 🗑️ 移除 | [→](jep-500.md) |
| [JEP 503](jep-503.md) | Remove 32-bit x86 Port | 25 | 🗑️ 移除 | [→](jep-503.md) |
| [JEP 504](jep-504.md) | Remove Applet API | 26 | 🗑️ 移除 | [→](jep-504.md) |
| [JEP 525](jep-525.md) | Structured Concurrency (6th) | 26 | 🔍 预览 | [→](jep-525.md) |
| [JEP 526](jep-526.md) | Lazy Constants (2nd) | 26 | 🔍 预览 | [→](jep-526.md) |
| [JEP 530](jep-530.md) | Primitive Types in Patterns (4th) | 26 | 🔍 预览 | [→](jep-530.md) |

### 性能

| JEP | 标题 | JDK | 状态 | 文档 |
|-----|------|-----|------|------|
| [JEP 439](jep-439.md) | Generational ZGC | 21 | ✅ 正式 | [→](jep-439.md) |
| [JEP 474](jep-474.md) | ZGC Generational by Default | 23 | ✅ 正式 | [→](jep-474.md) |
| [JEP 490](jep-490.md) | ZGC Remove Non-Generational Mode | 24 | ✅ 正式 | [→](jep-490.md) |
| [JEP 475](jep-475.md) | Late Barrier Expansion for G1 | 24 | ✅ 正式 | [→](jep-475.md) |
| [JEP 519](jep-519.md) | Compact Object Headers | 25 | ✅ 正式 | [→](jep-519.md) |
| [JEP 521](jep-521.md) | Generational Shenandoah | 25 | ✅ 正式 | [→](jep-521.md) |
| [JEP 514](jep-514.md) | AOT Command-Line Ergonomics | 25 | ✅ 正式 | [→](jep-514.md) |
| [JEP 515](jep-515.md) | AOT Method Profiling | 25 | ✅ 正式 | [→](jep-515.md) |
| [JEP 522](jep-522.md) | G1 GC Throughput Improvement | 26 | ✅ 正式 | [→](jep-522.md) |

### 监控与诊断 (JFR)

| JEP | 标题 | JDK | 状态 | 文档 |
|-----|------|-----|------|------|
| [JEP 509](jep-509.md) | JFR CPU-Time Profiling | 25 | 🔧 实验 | [→](jep-509.md) |
| [JEP 518](jep-518.md) | JFR Cooperative Sampling | 25 | ✅ 正式 | [→](jep-518.md) |
| [JEP 520](jep-520.md) | JFR Method Timing & Tracing | 25 | ✅ 正式 | [→](jep-520.md) |

### 安全与加密

| JEP | 标题 | JDK | 状态 | 文档 |
|-----|------|-----|------|------|
| [JEP 451](jep-451.md) | Prepare to Restrict Dynamic Loading | 21 | ⚠️ 废弃 | [→](jep-451.md) |
| [JEP 452](jep-452.md) | Key Encapsulation Mechanism API | 21 | ✅ 正式 | [→](jep-452.md) |
| [JEP 470](jep-470.md) | PEM Encodings | 25 | 🔍 预览 | [→](jep-470.md) |
| [JEP 510](jep-510.md) | Key Derivation Function API | 25 | ✅ 正式 | [→](jep-510.md) |
| [JEP 472](jep-472.md) | Prepare to Restrict JNI | 24 | ⚠️ 废弃 | [→](jep-472.md) |

### 库与工具

| JEP | 标题 | JDK | 状态 | 文档 |
|-----|------|-----|------|------|
| [JEP 458](jep-458.md) | Launch Multi-File Source-Code | 22 | ✅ 正式 | [→](jep-458.md) |
| [JEP 485](jep-485.md) | Stream Gatherers | 24 | ✅ 正式 | [→](jep-485.md) |
| [JEP 483](jep-483.md) | AOT Class Loading & Linking | 24 | ✅ 正式 | [→](jep-483.md) |
| [JEP 491](jep-491.md) | Synchronize Virtual Threads | 24 | ✅ 正式 | [→](jep-491.md) |
| [JEP 493](jep-493.md) | Linking Run-Time Images | 24 | ✅ 正式 | [→](jep-493.md) |

### 网络

| JEP | 标题 | JDK | 状态 | 文档 |
|-----|------|-----|------|------|
| [JEP 517](jep-517.md) | HTTP/3 for HTTP Client | 26 | 🔍 预览 | [→](jep-517.md) |

> 图例: ✅ 正式发布 | 🔍 预览特性 | 🔧 孵化器 | ⚠️ 废弃 | 🗑️ 移除

---

## 按版本索引

### JDK 21 LTS

#### 语言特性
- JEP 430: String Templates (第1次预览，已撤回)
- JEP 444: Virtual Threads (正式版)
- JEP 445: Unnamed Classes & Instance Main Methods (第1次预览)
- JEP 446: Scoped Values (预览)
- JEP 452: Key Encapsulation Mechanism API
- JEP 453: Structured Concurrency (第1次预览)

#### 性能
- JEP 439: Generational ZGC

### JDK 22 Feature

#### 语言特性
- JEP 454: Foreign Function & Memory API (正式版)
- JEP 456: Unnamed Variables & Patterns (正式版)
- JEP 457: Implicit Classes & Instance Main (预览) → JEP 463
- JEP 458: Launch Multi-File Source-Code (正式版)
- JEP 459: String Templates (第2次预览)
- JEP 462: Structured Concurrency (第2次预览)
- JEP 463: Implicit Classes & Instance Main (第2次预览)

#### 性能
- JEP 423: Region Pinning for G1

### JDK 23 Feature

#### 语言特性
- JEP 466: Class-File API (第2次预览)
- JEP 467: Markdown Documentation Comments (正式版)
- JEP 477: Implicit Classes & Instance Main (正式版)

#### 性能
- JEP 474: ZGC: Generational Mode by Default

### JDK 24 Feature

#### 语言特性
- JEP 484: Class-File API (正式版)
- JEP 485: Stream Gatherers (正式版)

#### 性能
- JEP 475: Late Barrier Expansion for G1
- JEP 483: AOT Class Loading & Linking
- JEP 490: ZGC Remove Non-Generational Mode
- JEP 491: Synchronize Virtual Threads without Pinning

#### 工具
- JEP 493: Linking Run-Time Images without JMODs

### JDK 25 LTS

#### 语言特性
- JEP 502: Stable Values (预览)
- JEP 505: Structured Concurrency (第5次预览)
- JEP 506: Scoped Values (正式版)
- JEP 507: Primitive Types in Patterns (第3次预览)
- JEP 508: Vector API (第10次孵化)
- JEP 511: Module Import Declarations (正式版)
- JEP 512: Compact Source Files & Instance Main (正式版)
- JEP 513: Flexible Constructor Bodies (正式版)

#### 性能
- JEP 514: AOT Command-Line Ergonomics
- JEP 515: AOT Method Profiling
- JEP 519: Compact Object Headers
- JEP 521: Generational Shenandoah

#### 监控诊断
- JEP 509: JFR CPU-Time Profiling (实验)
- JEP 518: JFR Cooperative Sampling
- JEP 520: JFR Method Timing & Tracing

#### 安全
- JEP 470: PEM Encodings (预览)
- JEP 510: Key Derivation Function API

#### 移除
- JEP 503: Remove the 32-bit x86 Port

### JDK 26 Feature

#### 语言特性
- JEP 500: Prepare to Make Final Mean Final
- JEP 504: Remove Applet API
- JEP 525: Structured Concurrency (第6次预览)
- JEP 526: Lazy Constants (第2次预览)
- JEP 530: Primitive Types in Patterns (第4次预览)

#### 性能
- JEP 522: G1 GC Throughput Improvement

#### 网络
- JEP 517: HTTP/3 for HTTP Client

---

## 按功能分类索引

### 并发编程
- [JEP 444](jep-444.md) - Virtual Threads (JDK 21)
- [JEP 446](jep-446.md) - Scoped Values (JDK 21 预览)
- [JEP 453](jep-453.md) - Structured Concurrency (JDK 21 第1次预览)
- [JEP 462](jep-462.md) - Structured Concurrency (JDK 22 第2次预览)
- [JEP 506](jep-506.md) - Scoped Values (JDK 25 正式)
- [JEP 505](jep-505.md) - Structured Concurrency (JDK 25 第5次预览)
- [JEP 525](jep-525.md) - Structured Concurrency (JDK 26 第6次预览)

### 模块系统
- [JEP 511](jep-511.md) - Module Import Declarations (JDK 25)
- [JEP 484](jep-484.md) - Class-File API (JDK 24)

### 文档工具
- [JEP 467](jep-467.md) - Markdown Documentation Comments (JDK 23)

### 内存管理
- [JEP 439](jep-439.md) - Generational ZGC (JDK 21)
- [JEP 474](jep-474.md) - ZGC: Generational Mode by Default (JDK 23)
- [JEP 490](jep-490.md) - ZGC Remove Non-Generational Mode (JDK 24)
- [JEP 519](jep-519.md) - Compact Object Headers (JDK 25)
- [JEP 521](jep-521.md) - Generational Shenandoah (JDK 25)

### GC 收集器
- [JEP 423](jep-423.md) - Region Pinning for G1 (JDK 22)
- [JEP 475](jep-475.md) - Late Barrier Expansion for G1 (JDK 24)
- [JEP 522](jep-522.md) - G1 GC Throughput Improvement (JDK 26)

### FFI (外部函数接口)
- [JEP 454](jep-454.md) - Foreign Function & Memory API (JDK 22)
- [JEP 472](jep-472.md) - Prepare to Restrict JNI (JDK 24)

### 加密与安全
- [JEP 452](jep-452.md) - Key Encapsulation Mechanism API (JDK 21)
- [JEP 470](jep-470.md) - PEM Encodings (JDK 25 预览)
- [JEP 510](jep-510.md) - Key Derivation Function API (JDK 25)

### 字符串处理
- [JEP 430](jep-430.md) - String Templates (JDK 21 预览，已撤回)
- [JEP 459](jep-459.md) - String Templates (JDK 22 第2次预览)

### 简化语法
- [JEP 445](jep-445.md) - Unnamed Classes & Instance Main (JDK 21)
- [JEP 463](jep-463.md) - Implicit Classes & Instance Main (JDK 22)
- [JEP 477](jep-477.md) - Implicit Classes & Instance Main (JDK 23 正式)
- [JEP 512](jep-512.md) - Compact Source Files & Instance Main (JDK 25)

### 模式匹配
- [JEP 456](jep-456.md) - Unnamed Variables & Patterns (JDK 22)
- [JEP 507](jep-507.md) - Primitive Types in Patterns (JDK 25 第3次预览)
- [JEP 530](jep-530.md) - Primitive Types in Patterns (JDK 26 第4次预览)

### 流处理
- [JEP 485](jep-485.md) - Stream Gatherers (JDK 24)

### 监控诊断 (JFR)
- [JEP 509](jep-509.md) - JFR CPU-Time Profiling (JDK 25 实验)
- [JEP 518](jep-518.md) - JFR Cooperative Sampling (JDK 25)
- [JEP 520](jep-520.md) - JFR Method Timing & Tracing (JDK 25)

### 网络
- [JEP 517](jep-517.md) - HTTP/3 for HTTP Client (JDK 26)

---

## 相关链接

- [OpenJDK JEP 官方页面](https://openjdk.org/jeps/0)
- [JDK 21 JEPs](https://openjdk.org/projects/jdk/21/)
- [JDK 22 JEPs](https://openjdk.org/projects/jdk/22/)
- [JDK 23 JEPs](https://openjdk.org/projects/jdk/23/)
- [JDK 24 JEPs](https://openjdk.org/projects/jdk/24/)
- [JDK 25 JEPs](https://openjdk.org/projects/jdk/25/)
- [JDK 26 JEPs](https://openjdk.org/projects/jdk/26/)
