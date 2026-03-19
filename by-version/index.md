# 按版本浏览

选择你使用的 JDK 版本，查看该版本的特性、问题和迁移指南。

---

## 版本概览

### LTS 版本（长期支持）

| 版本 | 发布时间 | 支持截止 | 状态 |
|------|----------|----------|------|
| **JDK 8** | 2014-03 | 2030-12 (付费) | 稳定 |
| **JDK 11** | 2018-09 | 2032-01 | 稳定 |
| **JDK 17** | 2021-09 | 2029-10 | 稳定 |
| **JDK 21** | 2023-09 | 2031-10 | 稳定 |
| **JDK 25** | 2025-09 | 2032+ | 当前 LTS |

### Feature 版本（短期支持，6个月）

| 版本 | 发布时间 | 主要特性 |
|------|----------|----------|
| **JDK 9** | 2017-09 | 模块系统 (JPMS) |
| **JDK 10** | 2018-03 | var 类型推断 |
| **JDK 12** | 2019-03 | Switch 表达式 (预览) |
| **JDK 13** | 2019-09 | 文本块 (预览) |
| **JDK 14** | 2020-03 | Records (预览)、Helpful NPE |
| **JDK 15** | 2020-09 | Text Blocks、ZGC 正式版 |
| **JDK 16** | 2021-03 | Records 正式版、instanceof 模式匹配 |
| **JDK 18** | 2022-03 | UTF-8 默认、Simple Web Server |
| **JDK 19** | 2022-09 | Virtual Threads (预览) |
| **JDK 20** | 2023-03 | Virtual Threads (第2次预览) |
| **JDK 22** | 2024-03 | String Templates (预览) |
| **JDK 23** | 2024-09 | Markdown 文档注释 |
| **JDK 24** | 2025-03 | String Templates (第3次预览) |
| **JDK 26** | 2025-09 | HTTP/3、G1 吞吐量提升 |

---

## 快速对比

### GC 默认选择

| 版本 | 默认 GC | 可选 GC |
|------|---------|---------|
| JDK 8 | ParallelGC | G1, CMS |
| JDK 9-10 | G1 | ZGC(实验) |
| JDK 11-16 | G1 | ZGC(11+), Shenandoah(15+) |
| JDK 17-20 | G1 | 分代 ZGC(21+), 分代 Shenandoah |
| JDK 21-24 | G1 | 分代 ZGC, 分代 Shenandoah |
| JDK 25-26 | G1 | 分代 ZGC(默认), 分代 Shenandoah |

### 主要特性演进

| 特性 | JDK 8 | 9 | 10 | 11 | 12 | 14 | 15 | 16 | 19 | 21 | 25 | 26 |
|------|-------|---|----|----|----|----|----|-----|-----|-----|-----|-----|
| Lambda | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 模块系统 | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| var | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Records | ❌ | ❌ | ❌ | ❌ | ❌ | 🔍 | 🔍 | ✅ | ✅ | ✅ | ✅ | ✅ |
| Text Blocks | ❌ | ❌ | ❌ | ❌ | 🔍 | 🔍 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| instanceof 模式匹配 | ❌ | ❌ | ❌ | ❌ | ❌ | 🔍 | 🔍 | ✅ | ✅ | ✅ | ✅ | ✅ |
| Virtual Threads | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🔍 | ✅ | ✅ | ✅ |
| String Templates | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Structured Concurrency | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 |
| HTTP/3 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

> ✅ 正式版 | 🔍 预览版

---

## 各版本文档

### LTS 版本

#### [JDK 8](jdk8/) - LTS 2014
- 核心特性：Lambda、Stream、Date/Time API
- GC：ParallelGC (默认)、G1、CMS
- [版本详情](jdk8/index.md)

#### [JDK 11](jdk11/) - LTS 2018
- 新特性：var、HTTP Client、Flight Recorder
- GC：G1 (默认)、ZGC (实验)
- [版本详情](jdk11/index.md)

#### [JDK 17](jdk17/) - LTS 2021
- 新特性：Records、Pattern Matching、Sealed Classes
- 强封装：JDK 内部 API 默认不可访问
- [版本详情](jdk17/index.md)

#### [JDK 21](jdk21/) - LTS 2023
- 新特性：Virtual Threads、Scoped Values、Structured Concurrency
- Pattern Matching 最终版
- [版本详情](jdk21/index.md)

#### [JDK 25](jdk25/) - LTS 2025
- 新特性：String Templates、Generational ZGC、Virtual Threads (正式版)
- Structured Concurrency (第5次预览)
- [版本详情](jdk25/index.md) | [JEP 汇总](jdk25/jeps.md) | [迁移指南](jdk25/migration/from-21.md)

##### JDK 25 深度分析
| 主题 | 链接 |
|------|------|
| String Templates | [深度分析](jdk25/deep-dive/string-templates.md) |
| 分代 ZGC | [深度分析](jdk25/deep-dive/generational-zgc.md) |

### Feature 版本

#### [JDK 9](jdk9/) - 2017
- 核心特性：模块系统 (JPMS)、接口私有方法
- [版本详情](jdk9/index.md)

#### [JDK 10](jdk10/) - 2018
- 核心特性：局部变量类型推断 (var)
- [版本详情](jdk10/index.md)

#### [JDK 12](jdk12/) - 2019
- 核心特性：Switch 表达式 (预览)、Shenandoah GC
- [版本详情](jdk12/index.md)

#### [JDK 13](jdk13/) - 2019
- 核心特性：文本块 (预览)、动态 CDS 存档
- [版本详情](jdk13/index.md)

#### [JDK 14](jdk14/) - 2020
- 核心特性：Records (预览)、instanceof 模式匹配 (预览)、Helpful NPE
- [版本详情](jdk14/index.md)

#### [JDK 15](jdk15/) - 2020
- 核心特性：Text Blocks (正式版)、Records (第2次预览)、Sealed Classes (预览)
- ZGC、Shenandoah 正式版
- [版本详情](jdk15/index.md)

#### [JDK 16](jdk16/) - 2021
- 核心特性：Records (正式版)、instanceof 模式匹配 (正式版)
- Vector API (孵化器)
- [版本详情](jdk16/index.md)

#### [JDK 18](jdk18/) - 2022
- 核心特性：UTF-8 默认字符集、Simple Web Server
- [版本详情](jdk18/index.md)

#### [JDK 19](jdk19/) - 2022
- 核心特性：Virtual Threads (预览)、Structured Concurrency (预览)
- [版本详情](jdk19/index.md)

#### [JDK 20](jdk20/) - 2023
- 核心特性：Virtual Threads (第2次预览)、Structured Concurrency (第2次预览)
- Scoped Values (预览)
- [版本详情](jdk20/index.md)

#### [JDK 22](jdk22/) - 2024
- 核心特性：String Templates (预览)、Implicit Classes (预览)
- Stream Gatherers (预览)
- [版本详情](jdk22/index.md)

#### [JDK 23](jdk23/) - 2024
- 核心特性：Module Import Declarations (预览)、Markdown 文档注释
- Flexible Constructors
- [版本详情](jdk23/index.md)

#### [JDK 24](jdk24/) - 2025
- 核心特性：String Templates (第3次预览)、Implicit Classes (第4次预览)
- Structured Concurrency (第4次预览)
- [版本详情](jdk24/index.md)

#### [JDK 26](jdk26/) - 2025
- 新特性：HTTP/3、G1 吞吐量提升、分代 Shenandoah、Compact Object Headers
- [版本详情](jdk26/index.md) | [JEP 汇总](jdk26/jeps.md) | [迁移指南](jdk26/migration/from-21.md)

##### JDK 26 深度分析
| 主题 | 链接 |
|------|------|
| HTTP/3 实现 | [深度分析](jdk26/deep-dive/http3-implementation.md) |
| 结构化并发 | 深度分析 |
| 原始类型模式匹配 | [深度分析](jdk26/deep-dive/primitive-pattern-matching.md) |
| Vector API 改进 | [深度分析](jdk26/deep-dive/vectorapi-improvements.md) |
| G1 GC 吞吐量优化 | [深度分析](jdk26/deep-dive/g1-gc-throughput.md) |
| AOT 改进 | [深度分析](jdk26/deep-dive/aot-improvements.md) |

---

## 迁移路径

```
JDK 8 ───────► JDK 11 ───────► JDK 17 ───────► JDK 21 ───────► JDK 25 ───────► JDK 26+
 │              │               │               │               │               │
 │              │               │               │               │               │
 ├─ 2017 EOL     ├─ 2026 EOL     ├─ 2029 EOL     ├─ 2031 EOL     ├─ LTS          └─ Feature
 └─ 付费延长    └─ 8年LTS       └─ 5年LTS       └─ 8年LTS       └─ 2032+ EOL
```

---

## 选择建议

| 当前版本 | 推荐升级 | 理由 |
|----------|----------|------|
| JDK 8 | → JDK 11 或 17 | 长期支持成本，性能提升 |
| JDK 11 | → JDK 17 或 21 | 新特性，更好的 GC |
| JDK 17 | → JDK 21 或 25 | 虚拟线程，结构化并发 |
| JDK 21 | → JDK 25 | 最新 LTS |
| JDK 25 | 保持或 → JDK 26 | 当前 LTS，或体验新特性 |

---

## 相关资源

### 按主题浏览

| 主题 | 说明 | 链接 |
|------|------|------|
| GC 演进 | G1/ZGC/Shenandoah 时间线 | [→](/by-topic/gc/timeline.md) |
| 并发编程 | Virtual Threads, Structured Concurrency | [→](/by-topic/concurrency/timeline.md) |
| 字符串处理 | 字符串 API 演进 | [→](/by-topic/string/timeline.md) |
| HTTP 客户端 | HTTP Client, HTTP/3 | [→](/by-topic/http/timeline.md) |
| 安全特性 | 加密、认证、TLS | [→](/by-topic/security/timeline.md) |

### 按贡献者浏览

| 链接 | 说明 |
|------|------|
| [by-contributor/](/by-contributor/) | 贡献者索引 |
| [JDK 26 Top 100](/by-contributor/profiles/jdk26-top-contributors.md) | JDK 26 贡献者排名 |
| [中国贡献者](/by-contributor/profiles/chinese-contributors.md) | 中国开发者贡献 |
| [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | HotSpot 核心开发者 |
| [David Holmes](/by-contributor/profiles/david-holmes.md) | 并发和 HotSpot 专家 |
| [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | JIT 编译器专家 |
| [Claes Redestad](/by-contributor/profiles/claes-redestad.md) | 核心库开发者 |
| [Brian Burkhalter](/by-contributor/profiles/brian-burkhalter.md) | 核心库开发者 |
| [Daniel Fuchs](/by-contributor/profiles/daniel-fuchs.md) | 网络和安全专家 |
| [Erik Gahlin](/by-contributor/profiles/erik-gahlin.md) | JFR 专家 |
| [更多贡献者](/by-contributor/profiles/) | 完整列表 |

### JEP 详细分析

| JEP | 标题 | 链接 |
|-----|------|------|
| JEP 444 | Virtual Threads | [分析](/jeps/jep-444.md) |
| JEP 454 | Foreign Function & Memory API | [分析](/jeps/jep-454.md) |
| JEP 462 | Structured Concurrency | [分析](/jeps/jep-462.md) |
| JEP 467 | Scoped Values | [分析](/jeps/jep-467.md) |
| JEP 468 | Generational ZGC | [分析](/jeps/jep-468.md) |
| JEP 469 | Implicit Classes | 分析 |
| JEP 470 | PEM Encodings | [分析](/jeps/jep-470.md) |
| JEP 500 | Make Final Mean Final | [分析](/jeps/jep-500.md) |
| JEP 502 | Stable Values | [分析](/jeps/jep-502.md) |
| JEP 503 | Implicit Classes (Preview) | [分析](/jeps/jep-503.md) |
| JEP 504 | Remove Applet API | [分析](/jeps/jep-504.md) |
| JEP 506 | Scoped Values (Preview) | [分析](/jeps/jep-506.md) |
| JEP 509 | Vector API | [分析](/jeps/jep-509.md) |
| JEP 510 | KDF API | [分析](/jeps/jep-510.md) |
| JEP 511 | Module Import Declarations | [分析](/jeps/jep-511.md) |
| JEP 512 | Compact Source Files | [分析](/jeps/jep-512.md) |
| JEP 514 | AOT Command Line Ergonomics | [分析](/jeps/jep-514.md) |
| JEP 515 | AOT Method Profiling | [分析](/jeps/jep-515.md) |
| JEP 517 | HTTP/3 for HTTP Client | [分析](/jeps/jep-517.md) |
| JEP 518 | JFR Cooperative Sampling | [分析](/jeps/jep-518.md) |
| JEP 519 | Compact Object Headers | [分析](/jeps/jep-519.md) |
| JEP 520 | JFR Method Timing | [分析](/jeps/jep-520.md) |
| JEP 521 | Generational Shenandoah | [分析](/jeps/jep-521.md) |
| JEP 522 | G1 GC Throughput | [分析](/jeps/jep-522.md) |
| JEP 525 | Structured Concurrency (Preview) | [分析](/jeps/jep-525.md) |
| JEP 526 | Lazy Constants | [分析](/jeps/jep-526.md) |
| JEP 530 | Primitive Types in Patterns | [分析](/jeps/jep-530.md) |
| [更多 JEP](/jeps/) | 完整列表 | → |

### PR/Issue 深度分析

| 目录 | 说明 | 链接 |
|------|------|------|
| [by-pr/](/by-pr/) | PR 索引 | [→](/by-pr/index.md) |
| JDK 26 Top PRs | 重要 PR 列表 | [→](/by-pr/jdk26-top-prs.md) |
| JDK-8298xxx | 类加载器相关 | [→](/by-pr/8298/) |
| JDK-8310xxx | 核心库优化 | [→](/by-pr/8310/) |
| JDK-8311xxx | 核心库优化 | [→](/by-pr/8311/) |
| JDK-8315xxx | 工具链 | [→](/by-pr/8315/) |
| JDK-8316xxx | 热点修复 | [→](/by-pr/8316/) |
| JDK-8335xxx | 核心库优化 | [→](/by-pr/8335/) |
| JDK-8336xxx | ClassFile API | [→](/by-pr/8336/) |
| JDK-8337xxx | 字符串优化 | [→](/by-pr/8337/) |
| JDK-8338xxx | 集合框架 | [→](/by-pr/8338/) |
| JDK-8355xxx | 核心库优化 | [→](/by-pr/8355/) |
| JDK-8366xxx | ClassFile API | [→](/by-pr/8366/) |
| JDK-8370xxx | 字符串优化 | [→](/by-pr/8370/) |

### 模块分析

| 模块 | 说明 | 链接 |
|------|------|------|
| java.base | 核心 API | [分析](/modules/java.base.md) |
| java.util.concurrent | JUC 并发工具 | [分析](/modules/concurrent.md) |
| java.net.http | HTTP Client | [分析](/modules/java.net.http.md) |
| java.crypto | 加密与安全 | [分析](/modules/java.crypto.md) |
| java.logging | 日志框架 | [分析](/modules/java.logging.md) |
| java.management | JMX 监控 | [分析](/modules/java.management.md) |
| java.sql | JDBC 数据库 | [分析](/modules/java.sql.md) |
| java.xml | XML 处理 | [分析](/modules/java.xml.md) |
| jdk.compiler | javac API | [分析](/modules/jdk.compiler.md) |
| hotspot | HotSpot VM | [分析](/modules/hotspot.md) |
| hotspot-gc | 垃圾回收器 | [分析](/modules/hotspot-gc.md) |
| hotspot-c2 | C2 编译器 | [分析](/modules/hotspot-c2.md) |
| [完整列表](/modules/README.md) | 模块索引 | → |

---

### 深度分析文档

| JEP | 标题 | 链接 |
|-----|------|------|
| JEP 506 | Scoped Values 实现 | [→](/deep-dive/jep-506-implementation.md) |
| JEP 511 | Module Import 实现 | [→](/deep-dive/jep-511-implementation.md) |
| JEP 517 | HTTP/3 实现 | [→](/deep-dive/jep-517-implementation.md) |
| JEP 519 | Compact Object Headers 实现 | [→](/deep-dive/jep-519-implementation.md) |
| JEP 522 | G1 GC Throughput 实现 | [→](/deep-dive/jep-522-implementation.md) |

---

### 指南文档

| 文档 | 说明 | 链接 |
|------|------|------|
| 速查表 | JDK 特性快速参考 | [→](/guides/cheat-sheet.md) |
| 常见问题 | FAQ | [→](/guides/faq.md) |
| 学习路径 | 推荐学习顺序 | [→](/guides/learning-path.md) |
| 迁移指南 | 版本迁移建议 | [→](/guides/migration-guide.md) |

---

### Issue 深度分析

| Issue | 标题 | 链接 |
|-------|------|------|
| JDK-8326498 | 核心库优化 | [→](/issues/jdk-8326498.md) |
| JDK-8355177 | 字符串优化 | [→](/issues/jdk-8355177.md) |
| JDK-8371259 | 性能改进 | [→](/issues/jdk-8371259.md) |

---

### 发布文档

| 版本 | 说明 | 链接 |
|------|------|------|
| JDK 26 | GA 发布说明 | [→](/releases/jdk26.md) |
