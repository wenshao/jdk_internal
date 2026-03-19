# 按版本浏览

选择你使用的 JDK 版本，查看该版本的特性、问题和迁移指南。

---

## 版本概览

| 版本 | 类型 | 发布时间 | 支持截止 | 状态 |
|------|------|----------|----------|------|
| **JDK 8** | LTS | 2014-03 | 2030-12 (付费) | 稳定 |
| **JDK 11** | LTS | 2018-09 | 2032-01 | 稳定 |
| **JDK 17** | LTS | 2021-09 | 2029-10 | 稳定 |
| **JDK 21** | LTS | 2023-09 | 2031-10 | 当前 LTS |
| **JDK 26** | Feature | 2025-09 | - | 开发中 |

---

## 快速对比

### GC 默认选择

| 版本 | 默认 GC | 可选 GC |
|------|---------|---------|
| JDK 8 | ParallelGC | G1, CMS, ZGC(实验) |
| JDK 11 | G1 | ZGC(实验), Shenandoah |
| JDK 17 | G1 | ZGC, Shenandoah |
| JDK 21 | G1 | 分代 ZGC, 分代 Shenandoah |
| JDK 26 | G1 | ZGC(NUMA), Shenandoah |

### 主要特性

| 特性 | JDK 8 | JDK 11 | JDK 17 | JDK 21 | JDK 26 |
|------|-------|--------|--------|--------|--------|
| Lambda | ✅ | ✅ | ✅ | ✅ | ✅ |
| var | ❌ | ✅ | ✅ | ✅ | ✅ |
| Records | ❌ | ❌ | ✅ | ✅ | ✅ |
| Pattern Matching | ❌ | ❌ | 预览 | ✅ | ✅ |
| Virtual Threads | ❌ | ❌ | ❌ | ✅ | ✅ |
| Structured Concurrency | ❌ | ❌ | ❌ | 预览 | 预览 |
| HTTP/3 | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 各版本文档

### [JDK 8](jdk8/) - LTS 2014
- 核心特性：Lambda、Stream、Date/Time API
- GC：ParallelGC (默认)、G1、CMS
- [版本详情](jdk8/index.md)

### [JDK 11](jdk11/) - LTS 2018
- 新特性：var、HTTP Client、Flight Recorder
- GC：G1 (默认)、ZGC (实验)
- [版本详情](jdk11/index.md)

### [JDK 17](jdk17/) - LTS 2021
- 新特性：Records、Pattern Matching、Sealed Classes
- 强封装：JDK 内部 API 默认不可访问
- [版本详情](jdk17/index.md)

### [JDK 21](jdk21/) - LTS 2023
- 新特性：Virtual Threads、Scoped Values、Structured Concurrency
- Pattern Matching 最终版
- [版本详情](jdk21/index.md)

### [JDK 26](jdk26/) - GA 2025-09-16
- 新特性：HTTP/3、分代 ZGC、分代 Shenandoah、Compact Object Headers
- [版本详情](jdk26/index.md) | [JEP 汇总](jdk26/jeps.md) | [迁移指南](jdk26/migration/from-21.md)

#### JDK 26 深度分析
| 主题 | 链接 |
|------|------|
| HTTP/3 实现 | [深度分析](jdk26/deep-dive/http3-implementation.md) |
| 结构化并发 | [深度分析](jdk26/deep-dive/structured-concurrency.md) |
| 原始类型模式匹配 | [深度分析](jdk26/deep-dive/primitive-pattern-matching.md) |
| Vector API 改进 | [深度分析](jdk26/deep-dive/vectorapi-improvements.md) |
| G1 GC 吞吐量优化 | [深度分析](jdk26/deep-dive/g1-gc-throughput.md) |
| AOT 改进 | [深度分析](jdk26/deep-dive/aot-improvements.md) |

---

## 相关资源

### 按主题浏览

| 主题 | 链接 | 说明 |
|------|------|------|
| GC 演进 | [by-topic/gc/](../by-topic/gc/) | G1/ZGC/Shenandoah 时间线 |
| 并发编程 | [by-topic/concurrency/](../by-topic/concurrency/) | Virtual Threads, Structured Concurrency |
| 字符串处理 | [by-topic/string/](../by-topic/string/) | 字符串 API 演进 |
| HTTP 客户端 | [by-topic/http/](../by-topic/http/) | HTTP Client, HTTP/3 |
| 安全特性 | [by-topic/security/](../by-topic/security/) | 加密、认证、TLS |

### 按贡献者浏览

| 链接 | 说明 |
|------|------|
| [by-contributor/](../by-contributor/) | 贡献者索引 |
| [JDK 26 Top 100](../by-contributor/profiles/jdk26-top-contributors.md) | JDK 26 贡献者排名 |
| [中国贡献者](../by-contributor/profiles/chinese-contributors.md) | 中国开发者贡献 |

### JEP 详细分析

| JEP | 标题 | 链接 |
|-----|------|------|
| JEP 516 | Ahead-of-Time Object Caching | [分析](../jeps/jep-516.md) |
| JEP 517 | HTTP/3 for HTTP Client | [分析](../jeps/jep-517.md) |
| JEP 519 | Compact Object Headers | [分析](../jeps/jep-519.md) |
| JEP 521 | Generational Shenandoah | [分析](../jeps/jep-521.md) |
| JEP 522 | G1 GC Throughput | [分析](../jeps/jep-522.md) |
| JEP 525 | Structured Concurrency | [分析](../jeps/jep-525.md) |
| JEP 526 | Lazy Constants | [分析](../jeps/jep-526.md) |
| JEP 500 | Make Final Mean Final | [分析](../jeps/jep-500.md) |
| JEP 504 | Remove Applet API | [分析](../jeps/jep-504.md) |
| JEP 509 | JFR CPU-Time Profiling | [分析](../jeps/jep-509.md) |
| JEP 527 | TLS 1.3 Hybrid Key Exchange | [分析](../jeps/jep-527.md) |

### PR/Issue 深度分析

| 链接 | 说明 |
|------|------|
| [by-pr/](../by-pr/) | PR 索引 |
| [by-pr/8355/](../by-pr/8355/) | JDK-8355xxx 系列 (核心库优化) |
| [by-pr/8366/](../by-pr/8366/) | JDK-8366xxx 系列 (ClassFile API) |
| [by-pr/8370/](../by-pr/8370/) | JDK-8370xxx 系列 (字符串优化) |

---

## 迁移路径

```
JDK 8 ───────► JDK 11 ───────► JDK 17 ───────► JDK 21 ───────► JDK 26
 │              │               │               │               │
 │              │               │               │               │
 ├─ 3年免费     ├─ 8年LTS       ├─ 5年LTS       ├─ 8年LTS       └─ 开发中
 └─ 付费延长    └─ 2029 EOL     └─ 2026 EOL     └─ 2031 EOL
```

---

## 选择建议

| 当前版本 | 推荐升级 | 理由 |
|----------|----------|------|
| JDK 8 | → JDK 11 或 17 | 长期支持成本，性能提升 |
| JDK 11 | → JDK 17 或 21 | 新特性，更好的 GC |
| JDK 17 | → JDK 21 | 虚拟线程，结构化并发 |
| JDK 21 | 保持或 → JDK 26 | 当前 LTS，或体验新特性 |
