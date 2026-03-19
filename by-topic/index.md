# 按主题浏览

跨版本追踪某个技术领域的演进历程。

---

## 主题列表

### [GC 演进](gc/)

垃圾收集器的发展历程，从 Serial 到分代 ZGC。

| 版本 | 主要变化 |
|------|----------|
| JDK 8 | G1 成为主流，CMS 标记废弃 |
| JDK 11 | ZGC 引入 (实验性) |
| JDK 15 | ZGC 生产可用 |
| JDK 17 | 并发线程栈扫描 |
| JDK 21 | 分代 ZGC、分代 Shenandoah |
| JDK 26 | G1 吞吐量提升、ZGC NUMA |

→ [GC 时间线](gc/timeline.md)

### [并发编程](concurrency/)

从 Thread 到 Virtual Thread 的演进。

| 版本 | 主要变化 |
|------|----------|
| JDK 8 | Lambda、Parallel Stream |
| JDK 9 | CompletableFuture 改进 |
| JDK 21 | **Virtual Threads** (正式版) |
| JDK 21 | **Scoped Values** (预览) |
| JDK 26 | Structured Concurrency (预览) |

→ [并发时间线](concurrency/timeline.md)

### [字符串处理](string/)

字符串相关优化和新特性。

| 版本 | 主要变化 |
|------|----------|
| JDK 8 | StringJoiner |
| JDK 11 | Compact Strings |
| JDK 21 | String Templates (预览) |
| JDK 26 | 多项性能优化 |

→ [字符串优化时间线](string/timeline.md)

### [HTTP 客户端](http/)

从 HttpURLConnection 到 HTTP/3。

| 版本 | 主要变化 |
|------|----------|
| JDK 8 | HttpURLConnection、HttpURLConnection |
| JDK 11 | **HTTP Client** (新 API) |
| JDK 16 | HTTP/2 支持 |
| JDK 21 | HTTP Client 正式版 |
| JDK 26 | **HTTP/3** |

→ [HTTP 演进时间线](http/timeline.md)

### [安全特性](security/)

加密、TLS、后量子密码。

| 版本 | 主要变化 |
|------|----------|
| JDK 8 | TLS 1.2 |
| JDK 11 | TLS 1.3 |
| JDK 21 | ChaCha20-Poly1305 |
| JDK 26 | **ML-DSA 后量子密码** |

→ [安全特性时间线](security/timeline.md)

---

## 特性首发版本

| 特性 | 首发版本 | 稳定版本 |
|------|----------|----------|
| Lambda | JDK 8 | JDK 8 |
| HTTP Client | JDK 11 | JDK 11 |
| ZGC | JDK 11 (实验) | JDK 15 |
| Records | JDK 14 (预览) | JDK 16 |
| Pattern Matching | JDK 14 (预览) | JDK 21 |
| Virtual Threads | JDK 19 (预览) | JDK 21 |
| Scoped Values | JDK 20 (预览) | - |
| Structured Concurrency | JDK 21 (预览) | - |
| HTTP/3 | JDK 26 | - |
