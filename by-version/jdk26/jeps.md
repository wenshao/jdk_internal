# JDK 26 JEP 汇总

> JDK 26 包含的所有 JEP (JDK Enhancement Proposal)
> **官方来源**: [OpenJDK JDK 26](https://openjdk.org/projects/jdk/26/)
> **GA 日期**: 2026-03-17

---

## JEP 分类

### 语言特性

| JEP | 标题 | 状态 | 文档 |
|-----|------|------|------|
| JEP 530 | Primitive Types in Patterns, instanceof, and switch | 预览 (第4次) | [详情](https://openjdk.org/jeps/530) |
| JEP 526 | Lazy Constants | 预览 (第2次) | [详情](https://openjdk.org/jeps/526) |
| JEP 500 | Prepare to Make Final Mean Final | 正式 | [详情](https://openjdk.org/jeps/500) |

### 性能

| JEP | 标题 | 影响 | 文档 |
|-----|------|------|------|
| JEP 522 | G1 GC: Improve Throughput by Reducing Synchronization | +10-20% | [详情](https://openjdk.org/jeps/522) |
| JEP 516 | Ahead-of-Time Object Caching with Any GC | 更快启动 | [详情](https://openjdk.org/jeps/516) |
| JEP 529 | Vector API (Eleventh Incubator) | 孵化 (第11次) | [详情](https://openjdk.org/jeps/529) |

### 网络

| JEP | 标题 | 状态 | 文档 |
|-----|------|------|------|
| JEP 517 | HTTP/3 for the HTTP Client API | 正式 | [详情](https://openjdk.org/jeps/517) |

### 并发

| JEP | 标题 | 状态 | 文档 |
|-----|------|------|------|
| JEP 525 | Structured Concurrency (Sixth Preview) | 预览 (第6次) | [详情](https://openjdk.org/jeps/525) |
| **Scoped Values (Final)** | 正式 | 作用域值 | [详情](https://openjdk.org/jeps/506) |

### 安全

| JEP | 标题 | 状态 | 文档 |
|-----|------|------|------|
| JEP 524 | PEM Encodings of Cryptographic Objects (Second Preview) | 预览 (第2次) | [详情](https://openjdk.org/jeps/524) |

### 移除功能

| JEP | 标题 | 状态 | 文档 |
|-----|------|------|------|
| JEP 504 | Remove the Applet API | 正式 | [详情](https://openjdk.org/jeps/504) |

---

## 状态说明

| 状态 | 说明 |
|------|------|
| 正式 | 包含在 JDK 26 中，可生产使用 |
| 预览 | 包含在 JDK 26 中，需要 `--enable-preview` |
| 孵化 | 包含在 JDK 26 中，API 可能变化 |

---

## 与 JDK 25 的 JEP 差异

以下 JEP 在 JDK 25 中，**不在** JDK 26 中：

| JEP | 标题 | 目标版本 |
|-----|------|----------|
| JEP 503 | Remove the 32-bit x86 Port | JDK 25 |
| JEP 505 | Structured Concurrency (Fifth Preview) | JDK 25 |
| JEP 506 | Scoped Values | JDK 25 |
| JEP 507 | Primitive Types in Patterns (Third Preview) | JDK 25 |
| JEP 510 | Key Derivation Function API | JDK 25 |
| JEP 511 | Module Import Declarations | JDK 25 |
| JEP 512 | Compact Source Files and Instance Main Methods | JDK 25 |
| JEP 513 | Flexible Constructor Bodies | JDK 25 |
| JEP 519 | Compact Object Headers | JDK 25 |
| JEP 520 | JFR Method Timing & Tracing | JDK 25 |
| JEP 521 | Generational Shenandoah | JDK 25 |

---

## 相关链接

- [OpenJDK JEP 首页](https://openjdk.org/jeps/0)
- [JDK 26 发布计划](https://openjdk.org/projects/jdk/26/)
