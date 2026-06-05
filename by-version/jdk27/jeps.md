# JDK 27 JEP 汇总

> **数据截至**: 2026-06-06 | **来源**: [openjdk.org/projects/jdk/27](https://openjdk.org/projects/jdk/27/)（页面更新于 2026-06-04 Rampdown Phase One）

---

## 总览

| 指标 | 值 |
|------|-----|
| **已 Target JEP** | 9 |
| **Proposed to Target** | 0（特性集已冻结） |
| **预计 GA** | 2026-09-15 |
| **开发阶段** | Rampdown Phase One（2026-06-04 起） |

**按性质分类**:

| 性质 | JEP |
|------|-----|
| **正式特性 (Final)** | 527 (后量子 TLS)、536 (JFR 脱敏) |
| **行为变更 (默认值)** | 523 (G1 全环境默认)、534 (紧凑对象头默认) |
| **预览 (Preview)** | 531 (Lazy Constants)、532 (原始类型模式)、533 (结构化并发)、538 (PEM 编码) |
| **孵化 (Incubator)** | 537 (Vector API) |

---

## 已 Target 的 JEP

### JEP 523: Make G1 the Default Garbage Collector in All Environments

| 属性 | 值 |
|------|-----|
| **JEP** | [523](https://openjdk.org/jeps/523) |
| **类别** | GC |
| **性质** | 行为变更 |
| **组件** | hotspot/gc |

**概述**: 让 Garbage-First (G1) 在**所有环境**下成为默认垃圾收集器，而不仅是 server 类环境。此前，JVM 在资源受限环境（如单处理器、小内存容器）会经由 ergonomics 默认选择 Serial GC；JDK 27 起这些环境也将默认使用 G1。

**关键点**:
- 统一默认 GC，减少不同环境间的行为差异
- 资源受限环境仍可显式指定 `-XX:+UseSerialGC` 回退到 Serial GC
- 延续 OpenJDK 让 G1 适配小堆/容器场景的长期工作

**相关**: [GC 演进时间线](../../by-topic/core/gc/)

---

### JEP 527: Post-Quantum Hybrid Key Exchange for TLS 1.3

| 属性 | 值 |
|------|-----|
| **JEP** | [527](https://openjdk.org/jeps/527) |
| **类别** | 安全 (Security) |
| **性质** | 正式特性 |
| **组件** | security-libs/javax.net.ssl |

**概述**: 在 Java 的 TLS 1.3 实现中引入后量子混合密钥交换机制。使用经典密钥交换算法（如 X25519）与后量子密钥封装机制（如 ML-KEM）的混合方案，提供对量子计算威胁的前瞻性防护。

**关键点**:
- 混合方案确保即使后量子算法被攻破，仍有经典算法提供安全保障
- 基于 IETF 标准化的混合密钥交换机制
- 对现有 TLS 应用透明，无需代码修改
- 性能影响主要体现在握手阶段的数据量增加

**详细分析**: [JEP 527 分析](../../jeps/security/jep-527.md)

---

### JEP 531: Lazy Constants (Third Preview)

| 属性 | 值 |
|------|-----|
| **JEP** | [531](https://openjdk.org/jeps/531) |
| **类别** | 核心库 (Core Libs) |
| **性质** | 预览（第三轮） |
| **组件** | core-libs/java.lang |

**概述**: 引入 lazy constants（惰性常量）API——持有不可变数据的对象。Lazy constants 被 JVM 视为真正的常量，从而获得与 `final` 字段相同的性能优化（常量折叠等），同时比 `final` 字段提供更大的初始化时机灵活性（延迟到首次使用时才计算）。

**关键点**:
- 延续 [JEP 502 Stable Values](../../jeps/performance/jep-502.md) 的探索，现更名为 Lazy Constants
- 兼顾 `final` 的性能与延迟初始化的灵活性
- 适用于昂贵的、按需初始化的单例/缓存场景

**相关**: 前身 [JEP 502 Stable Values (Preview)](../../jeps/performance/jep-502.md)

---

### JEP 532: Primitive Types in Patterns, instanceof, and switch (Fifth Preview)

| 属性 | 值 |
|------|-----|
| **JEP** | [532](https://openjdk.org/jeps/532) |
| **类别** | 语言 (Language) |
| **性质** | 预览（第五轮） |
| **组件** | specification/language |

**概述**: 扩展模式匹配、`instanceof` 与 `switch`，使其支持**所有原始类型**（不限于引用类型）。允许在类型模式、`instanceof` 与 `switch` 中直接使用 `int`、`long`、`float` 等原始类型，并支持安全的精度判断。

**关键点**:
- 让模式匹配在原始类型与引用类型间保持一致
- 与 record 解构、`switch` 表达式协同
- 长期预览特性，自 [JEP 455](../../jeps/tools/jep-455.md) 起持续演进

**相关**: 前身 [JEP 455 Primitive Types in Patterns](../../jeps/tools/jep-455.md)

---

### JEP 533: Structured Concurrency (Seventh Preview)

| 属性 | 值 |
|------|-----|
| **JEP** | [533](https://openjdk.org/jeps/533) |
| **类别** | 并发 (Concurrency) |
| **性质** | 预览（第七轮） |
| **组件** | core-libs/java.util.concurrent |

**概述**: 通过 `StructuredTaskScope` 将一组相关并发任务视为单一工作单元，简化错误处理与任务取消，避免线程泄漏与取消遗漏。结构化并发与虚拟线程（JEP 444）配合，使高并发任务的生命周期管理更可靠。

**关键点**:
- 任务的层次结构与代码块结构一致，便于推理
- 子任务失败时自动取消其余子任务
- 长期预览特性，持续打磨 API

**相关**: 前身 [JEP 499 Structured Concurrency (Fourth Preview)](../../jeps/concurrency/jep-499.md)、[JEP 480](../../jeps/concurrency/jep-480.md)

---

### JEP 534: Compact Object Headers by Default

| 属性 | 值 |
|------|-----|
| **JEP** | [534](https://openjdk.org/jeps/534) |
| **类别** | 运行时 / 性能 |
| **性质** | 行为变更（默认） |
| **组件** | hotspot/runtime |

**概述**: 让紧凑对象头（Compact Object Headers）成为 HotSpot JVM 的**默认**对象头布局。紧凑对象头将 64 位架构上的对象头从 96 位压缩到 64 位，从而减小堆占用、提升部署密度并增强数据局部性。

**关键点**:
- 延续 [JEP 519 Compact Object Headers](../../jeps/gc/jep-519.md)（JDK 25 转为产品特性），JDK 27 起默认开启
- 对内存密集型、小对象众多的应用收益明显
- 可通过 `-XX:-UseCompactObjectHeaders` 关闭

**相关**: 前身 [JEP 519 Compact Object Headers](../../jeps/gc/jep-519.md)；[JEP 519 实现深入](../../deep-dive/jep-519-implementation.md)

---

### JEP 536: JFR In-Process Data Redaction

| 属性 | 值 |
|------|-----|
| **JEP** | [536](https://openjdk.org/jeps/536) |
| **类别** | 可观测性 (JFR) |
| **性质** | 正式特性 |
| **组件** | hotspot/jfr |

**概述**: 增强 JDK Flight Recorder (JFR)，在记录中对命令行参数、环境变量与系统属性的初始值进行脱敏。脱敏在数据离开进程之前完成，避免敏感信息（如密码、令牌）泄漏到 JFR 文件中。

**关键点**:
- 在进程内（in-process）脱敏，源头防止泄漏
- 覆盖命令行参数、环境变量、系统属性
- 提升 JFR 在生产环境采集时的安全合规性

**相关**: [JFR / 性能可观测性主题](../../by-topic/core/performance/)

---

### JEP 537: Vector API (Twelfth Incubator)

| 属性 | 值 |
|------|-----|
| **JEP** | [537](https://openjdk.org/jeps/537) |
| **类别** | 性能 / SIMD |
| **性质** | 孵化（第十二轮） |
| **组件** | core-libs/jdk.incubator.vector |

**概述**: 提供一套 API，以表达可在支持的 CPU 架构上可靠编译为最优 SIMD 指令的向量计算，从而获得超越等价标量计算的性能。Vector API 长期处于孵化阶段，等待 Project Valhalla 的值类型成熟后再考虑转正。

**关键点**:
- 平台无关地表达向量运算，运行时映射到 AVX/NEON/SVE 等 SIMD 指令
- 持续孵化，跟进 Valhalla 值类型进展
- 适用于机器学习、图像处理、科学计算等数据并行场景

**相关**: 前身 [JEP 508 Vector API (Tenth Incubator)](../../jeps/concurrency/jep-508.md)

---

### JEP 538: PEM Encodings of Cryptographic Objects (Third Preview)

| 属性 | 值 |
|------|-----|
| **JEP** | [538](https://openjdk.org/jeps/538) |
| **类别** | 安全 (Security) |
| **性质** | 预览（第三轮） |
| **组件** | security-libs/java.security |

**概述**: 提供一套 API，用于在 PEM 文本格式与加密对象（密钥、证书、证书吊销列表等）之间进行编码与解码。简化了密钥与证书的导入导出，避免开发者手工处理 Base64 与 PEM 头尾标记。

**关键点**:
- 标准化 PEM ↔ 加密对象的转换
- 覆盖 `PrivateKey`、`PublicKey`、`X509Certificate`、`X509CRL` 等
- 与现有 `KeyFactory` / `CertificateFactory` 协同

**相关**: [安全特性主题](../../by-topic/security/security/)

---

## 历史对比

| 版本 | JEP 数量 | GA 日期 | 类型 |
|------|---------|---------|------|
| JDK 24 | 24 | 2025-03-18 | Feature |
| JDK 25 | 18 | 2025-09-16 | **LTS** |
| JDK 26 | 10 | 2026-03-17 | Feature |
| JDK 27 | 9 | 2026-09-15 | Feature |

> 趋势：非 LTS 版本的 JEP 数量趋于平稳（9-10 个）。JDK 27 以两项默认行为变更（G1 全环境默认、紧凑对象头默认）为亮点，预览/孵化特性继续打磨。

---

## 相关链接

- [OpenJDK JDK 27 项目页](https://openjdk.org/projects/jdk/27/)
- [JEP 索引](https://openjdk.org/jeps/0)
- [JEP 分析总览](../../jeps/)
- [JDK 27 README](./README.md)
