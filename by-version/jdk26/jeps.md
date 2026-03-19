# JDK 26 JEP 汇总

> JDK 26 包含的所有 JEP (JDK Enhancement Proposal)

---

## JEP 分类

### 语言特性

| JEP | 标题 | 状态 | 文档 |
|-----|------|------|------|
| JEP 530 | Primitive Types in Patterns | 预览 | [详情](/jeps/concurrency/jep-530.md) |
| JEP 526 | Lazy Constants | 预览 | [详情](/jeps/concurrency/jep-526.md) |
| JEP 512 | Compact Source Files | 正式 | [详情](/jeps/language/jep-512.md) |
| JEP 511 | Module Import Declarations | 正式 | [详情](/jeps/language/jep-511.md) |

### 性能

| JEP | 标题 | 影响 | 文档 |
|-----|------|------|------|
| JEP 522 | G1 GC Throughput | +10-20% | [详情](/jeps/gc/jep-522.md) |
| JEP 521 | Generational Shenandoah | -30% pause | [详情](/jeps/gc/jep-521.md) |
| JEP 519 | Compact Object Headers | -16% heap | [详情](/jeps/gc/jep-519.md) |
| JEP 514 | AOT Ergonomics | 更快启动 | [详情](/jeps/performance/jep-514.md) |
| JEP 515 | AOT Method Profiling | 更好性能 | [详情](/jeps/performance/jep-515.md) |

### 网络

| JEP | 标题 | 状态 | 文档 |
|-----|------|------|------|
| JEP 517 | HTTP/3 | 正式 | [详情](/jeps/network/jep-517.md) |

### 并发

| JEP | 标题 | 状态 | 文档 |
|-----|------|------|------|
| JEP 525 | Structured Concurrency | 预览 | [详情](/jeps/concurrency/jep-525.md) |
| JEP 506 | Scoped Values | 预览 | [详情](/jeps/concurrency/jep-506.md) |
| JEP 502 | Stable Values | 正式 | [详情](/jeps/performance/jep-502.md) |

### 安全

| JEP | 标题 | 文档 |
|-----|------|------|
| JEP 510 | KDF API | [详情](/jeps/security/jep-510.md) |
| JEP 500 | Make Final Mean Final | [详情](/jeps/removed/jep-500.md) |
| JEP 470 | PEM Encodings | [详情](/jeps/security/jep-470.md) |

---

## 状态说明

| 状态 | 说明 |
|------|------|
| 正式 | 包含在 JDK 26 中，可生产使用 |
| 预览 | 包含在 JDK 26 中，需要 `--enable-preview` |
| 提议 | 计划包含，可能延后 |

---

## 相关链接

- [OpenJDK JEP 首页](https://openjdk.org/jeps/0)
- [JDK 26 发布计划](https://openjdk.org/projects/jdk/26/)
