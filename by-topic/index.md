# 按主题浏览

跨版本追踪某个技术领域的演进历程。

---

## 主题列表

### [GC 演进](gc/)

垃圾收集器的发展历程，从 Serial 到分代 ZGC。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 8 | G1 成为主流，CMS 标记废弃 | - |
| JDK 11 | ZGC 引入 (实验性) | JEP 333 |
| JDK 15 | ZGC 生产可用 | JEP 378 |
| JDK 17 | 并发线程栈扫描 | - |
| JDK 21 | **分代 ZGC** (JEP 439)、分代 Shenandoah (JEP 429) | JEP 439, JEP 429 |
| JDK 23 | ZGC 分代改进 | JEP 474 |
| JDK 26 | G1 吞吐量提升 (JEP 522)、ZGC NUMA | JEP 522 |

→ [GC 时间线](gc/timeline.md)

### [并发编程](concurrency/)

从 Thread 到 Virtual Thread 的演进。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 5 | Executor 框架 | JSR-166 |
| JDK 7 | Fork/Join 框架 | JSR-166y |
| JDK 8 | Lambda、Parallel Stream | JEP 126 |
| JDK 8 | CompletableFuture | JEP 107 |
| JDK 9 | CompletableFuture 改进、Reactive Streams | JEP 266 |
| JDK 19 | **Virtual Threads** (预览) | JEP 425 |
| JDK 20 | Virtual Threads (第二次预览) | JEP 436 |
| JDK 21 | **Virtual Threads** (正式)、**Structured Concurrency** (预览)、**Scoped Values** (预览) | JEP 444, JEP 453, JEP 446 |
| JDK 22 | Structured Concurrency (第二次预览) | JEP 462 |
| JDK 23 | Structured Concurrency (第三次预览) | JEP 477 |
| JDK 24 | Structured Concurrency (第四次预览) | JEP 483 |
| JDK 25 | Structured Concurrency (第五次预览) | JEP 491 |
| JDK 26 | Structured Concurrency (第六次预览) | JEP 493 |

→ [并发时间线](concurrency/timeline.md)

### [字符串处理](string/)

字符串相关优化和新特性。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 8 | StringJoiner | - |
| JDK 9 | **Compact Strings** (JEP 254)、invokedynamic 拼接 (JEP 280) | JEP 254, JEP 280 |
| JDK 11 | repeat()、strip()、isBlank()、lines() | JEP 378 (Text Blocks) |
| JDK 15 | **Text Blocks** (正式) | JEP 378 |
| JDK 21 | String Templates (预览) | JEP 430 |
| JDK 24 | 隐藏类拼接策略 (+40% 启动性能) | JDK-8336856 |
| JDK 25 | String Templates (第二次预览) | JEP 459 |
| JDK 26 | Integer/Long.toString 优化 | JDK-8370503 |

→ [字符串优化时间线](string/timeline.md)

### [HTTP 客户端](http/)

从 HttpURLConnection 到 HTTP/3。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 1.0 | HttpURLConnection | - |
| JDK 9 | HTTP Client (孵化器) | JEP 110 |
| JDK 10 | HTTP Client (孵化器) | - |
| JDK 11 | **HTTP Client** (标准) | JEP 321 |
| JDK 16 | HTTP/2 支持 | - |
| JDK 22 | HTTP Client 多项改进 | - |
| JDK 23 | HTTP/2 连接复用优化 | - |
| JDK 26 | **HTTP/3** (预览) | JEP 517 |

→ [HTTP 演进时间线](http/timeline.md)

### [安全特性](security/)

加密、TLS、后量子密码。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 8 | TLS 1.2 (默认) | - |
| JDK 11 | **TLS 1.3** (默认)、ChaCha20-Poly1305 | JEP 332, JEP 329 |
| JDK 15 | 禁用弱签名算法 | - |
| JDK 17 | KMAC、SHA-3 家族 | JEP 370 |
| JDK 21 | 增强密码套件、HSS/LMS 签名 | - |
| JDK 22 | KDF API (预览) | JEP 495 |
| JDK 23 | KDF API (第二次预览) | JEP 508 |
| JDK 24 | 12 KDF 算法支持 | - |
| JDK 26 | **ML-DSA** 后量子签名、**KDF API** (正式)、**PEM 格式** | JEP 518, JEP 510, JEP 470 |

→ [安全特性时间线](security/timeline.md)

---

## 特性首发版本速查

### 语言特性

| 特性 | 首发版本 | 预览次数 | 正式版本 | JEP |
|------|----------|----------|----------|-----|
| Lambda | JDK 8 | - | JDK 8 | JEP 126 |
| Stream API | JDK 8 | - | JDK 8 | JEP 107 |
| Optional | JDK 8 | - | JDK 8 | JEP 150 |
| Module System | JDK 9 | - | JDK 9 | JEP 261 |
| Local Variable Type Inference | JDK 10 | - | JDK 10 | JEP 286 |
| Var Handles | JDK 9 | - | JDK 9 | JEP 193 |
| Records | JDK 14 | 2 | JDK 16 | JEP 395, JEP 384 |
| Pattern Matching for instanceof | JDK 14 | 2 | JDK 16 | JEP 375, JEP 305 |
| Sealed Classes | JDK 15 | 2 | JDK 17 | JEP 409, JEP 360 |
| Pattern Matching for switch | JDK 17 | 2 | JDK 21 | JEP 406, JEP 420, JEP 441 |
| Record Patterns | JDK 19 | 2 | JDK 21 | JEP 405, JEP 432, JEP 440 |
| String Templates (Preview) | JDK 21 | 2+ | JDK 26+ | JEP 430, JEP 459 |
| Flexible Constructor Bodies | JDK 21 | 3 | JDK 25 | JEP 447, JEP 482, JEP 513 |
| Primitive Types in Patterns | JDK 23 | - | JDK 26 | JEP 455 |
| Implicit Classes | JDK 21 | 3 | JDK 23 | JEP 443, JEP 463, JEP 469 |

### 并发特性

| 特性 | 首发版本 | 预览次数 | 正式版本 | JEP |
|------|----------|----------|----------|-----|
| Virtual Threads | JDK 19 | 2 | JDK 21 | JEP 425, JEP 436, JEP 444 |
| Scoped Values | JDK 20 | 3+ | JDK 23+ | JEP 429, JEP 446, JEP 467 |
| Structured Concurrency | JDK 21 | 6+ | JDK 27+ | JEP 453, JEP 462, JEP 477, JEP 483, JEP 491, JEP 493 |

### GC 特性

| 特性 | 首发版本 | 状态 | JEP |
|------|----------|------|-----|
| G1 GC | JDK 6 | 生产 | - |
| ZGC | JDK 11 | 生产 | JEP 333 |
| Shenandoah | JDK 12 | 生产 | JEP 379 |
| Generational ZGC | JDK 21 | 生产 | JEP 439 |
| Generational Shenandoah | JDK 21 | 生产 | JEP 429 |
| G1 Throughput Improvement | JDK 26 | 生产 | JEP 522 |

### 安全特性

| 特性 | 首发版本 | 状态 | JEP |
|------|----------|------|-----|
| TLS 1.3 | JDK 11 | 生产 | JEP 332 |
| ChaCha20-Poly1305 | JDK 11 | 生产 | JEP 329 |
| KMAC | JDK 17 | 生产 | JEP 370 |
| ML-DSA (后量子) | JDK 26 | 生产 | JEP 518 |
| KDF API | JDK 22 | 预览→正式JDK26 | JEP 495, JEP 508, JEP 510 |
| PEM Encodings | JDK 26 | 生产 | JEP 470 |

---

## 版本选择指南

### LTS 版本推荐

| 版本 | 发布时间 | 支持状态 | 推荐场景 |
|------|----------|----------|----------|
| JDK 8 | 2014-03 | LTS (至 2030) | 遗留系统维护 |
| JDK 11 | 2018-09 | LTS (至 2032) | 稳定生产环境 |
| JDK 17 | 2021-09 | LTS (至 2029) | 现代应用首选 |
| JDK 21 | 2023-09 | LTS (至 2031) | 虚拟线程生产 |
| JDK 25 | 2025-09 | LTS | 下一个 LTS |

### 选择决策树

```
需要虚拟线程?
├── 是 → JDK 21+ (推荐 JDK 25 LTS)
└── 否 → 继续

    需要低延迟 GC?
    ├── 是 → JDK 21+ (分代 ZGC/Shenandoah)
    └── 否 → 继续

        需要 HTTP/3?
        ├── 是 → JDK 26+
        └── 否 → 继续

            需要 String Templates?
            ├── 是 → JDK 26+
            └── 否 → JDK 17/21 LTS
```

---

## 相关链接

- [按版本浏览](../by-version/)
- [JEP 索引](../jeps/)
- [PR 分析](../by-pr/)
