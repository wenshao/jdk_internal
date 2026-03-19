# 贡献者索引

> 从贡献者维度了解 JDK 26 的开发贡献

---

## Top 贡献者

| 贡献者 | Commits | 主要领域 | 详情 |
|--------|---------|----------|------|
| [Albert Mingkun Yang](albert-mingkun-yang.md) | 124 | GC (G1/Parallel) | [查看详情](albert-mingkun-yang.md) |
| [Aleksey Shipilev](aleksey-shipilev.md) | 120 | 编译器、性能 | [查看详情](aleksey-shipilev.md) |
| [Thomas Schatzl](thomas-schatzl.md) | 95 | G1 GC | [查看详情](thomas-schatzl.md) |
| [Ioi Lam](ioi-lam.md) | 109 | AOT/CDS | [查看详情](ioi-lam.md) |
| [Daniel Fuchs](daniel-fuchs.md) | 49 | HttpClient/HTTP/3 | [查看详情](daniel-fuchs.md) |
| [Jan Lahoda](jan-lahoda.md) | 62 | javac/JShell | [查看详情](jan-lahoda.md) |
| [Erik Gahlin](erik-gahlin.md) | 74 | JFR | [查看详情](erik-gahlin.md) |
| [Jaikiran Pai](jaikiran-pai.md) | 64 | HttpClient | [查看详情](jaikiran-pai.md) |
| [Chen Liang](chen-liang.md) | 85 | 核心库/反射 | [查看详情](chen-liang.md) |
| [Kim Barrett](kim-barrett.md) | 65 | 并发/原子操作 | [查看详情](kim-barrett.md) |

---

## 按领域分类

### GC 专家

| 贡献者 | Commits | 专长 |
|--------|---------|------|
| [Albert Mingkun Yang](albert-mingkun-yang.md) | 124 | G1, Parallel GC |
| [Thomas Schatzl](thomas-schatzl.md) | 95 | G1 GC |
| [William Kemper](william-kemper.md) | 60 | Shenandoah |
| [Kim Barrett](kim-barrett.md) | 65 | 并发 GC |

### 编译器专家

| 贡献者 | Commits | 专长 |
|--------|---------|------|
| [Aleksey Shipilev](aleksey-shipilev.md) | 120 | C2 优化 |
| [Hamlin Li](hamlin-li.md) | 65 | SuperWord, RISC-V |
| [Emanuel Peter](emanuel-peter.md) | 52 | C2 向量化 |

### 网络专家

| 贡献者 | Commits | 专长 |
|--------|---------|------|
| [Daniel Fuchs](daniel-fuchs.md) | 49 | HTTP/3, QUIC |
| [Daniel Jeliński](daniel-jelinski.md) | 42 | HTTP/3 拥塞控制 |
| [Jaikiran Pai](jaikiran-pai.md) | 64 | HttpClient bug 修复 |
| [Brian Burkhalter](brian-burkhalter.md) | 65 | 网络 API |

### 语言/编译器专家

| 贡献者 | Commits | 专长 |
|--------|---------|------|
| [Jan Lahoda](jan-lahoda.md) | 62 | javac, JShell |
| [Maurizio Cimadamore](maurizio-cimadamore.md) | 25 | 语言特性 |

### JFR 专家

| 贡献者 | Commits | 专长 |
|--------|---------|------|
| [Erik Gahlin](erik-gahlin.md) | 74 | JFR 核心 |
| [Johannes Bechberger](johannes-bechberger.md) | 40 | JFR CPU-Time |
| [Markus Grönlund](markus-gronlund.md) | 33 | JFR 采样 |

### AOT/CDS 专家

| 贡献者 | Commits | 专长 |
|--------|---------|------|
| [Ioi Lam](ioi-lam.md) | 109 | AOT, CDS |
| [Calvin Cheung](calvin-cheung.md) | 35 | CDS |
| [Jiangli Zhou](jiangli-zhou.md) | 38 | CDS |

### 安全专家

| 贡献者 | Commits | 专长 |
|--------|---------|------|
| [Anthony Scarpino](anthony-scarpino.md) | 35 | PEM, 加密 |
| [Weijun Wang](weijun-wang.md) | 29 | KDF, 安全 API |
| [Sean Mullan](sean-mullan.md) | 22 | 安全框架 |

---

## JEP 主导者

| JEP | 主导者 | 协作者 |
|-----|--------|--------|
| JEP 511: Module Import | [Jan Lahoda](jan-lahoda.md) | Maurizio Cimadamore |
| JEP 512: Compact Source Files | [Jan Lahoda](jan-lahoda.md) | - |
| JEP 517: HTTP/3 | [Daniel Fuchs](daniel-fuchs.md) | Daniel Jeliński, Volkan Yazici |
| JEP 522: G1 GC Throughput | [Thomas Schatzl](thomas-schatzl.md) | - |
| JEP 521: Gen Shenandoah | [William Kemper](william-kemper.md) | - |
| JEP 519: Compact Headers | Roman Kennke | - |
| JEP 514: AOT Ergonomics | [Ioi Lam](ioi-lam.md) | - |
| JEP 515: AOT Profiling | Igor Veresov | - |
| JEP 509: JFR CPU-Time | Johannes Bechberger | - |
| JEP 520: JFR Method Timing | [Erik Gahlin](erik-gahlin.md) | - |
| JEP 518: JFR Sampling | Markus Grönlund | - |
| JEP 500: Make Final Mean Final | Alan Bateman | - |
| JEP 510: KDF API | Weijun Wang | - |
| JEP 506: Scoped Values | Andrew Haley | - |
| JEP 502: Stable Values | Per Minborg | - |
| JEP 526: Lazy Constants | Per Minborg | - |
| JEP 503: Remove 32-bit x86 | [Aleksey Shipilev](aleksey-shipilev.md) | - |
| JEP 504: Remove Applet API | Phil Race | - |
| JEP 470: PEM Encodings | Anthony Scarpino | - |
| JEP 530: Primitive Patterns | Aggelos Biboudis | - |
| JEP 525: Structured Concurrency | Alan Bateman | - |

---

## 组织贡献

### Oracle (80%+)

主要贡献者: Albert Mingkun Yang, Thomas Schatzl, Daniel Fuchs, Jan Lahoda, Ioi Lam, Erik Gahlin...

### Red Hat (~5%)

主要贡献者: William Kemper, Roman Kennke, Andrew Haley, Kim Barrett...

### SAP (~2%)

主要贡献者: Johannes Bechberger...

---

## 中国贡献者

> 详见 [中国贡献者专题](chinese-contributors.md)

| 贡献者 | 组织 | Commits | 主要领域 |
|--------|------|---------|----------|
| [SendaoYan](chinese-contributors.md#sendaoyan) | Oracle | 88 | 测试稳定性 |
| [Shaojin Wen](chinese-contributors.md#shaojin-wen) | Oracle | 31 | 核心库优化 |
| [Fei Yang](chinese-contributors.md#fei-yang) | Oracle | 30 | RISC-V |
| [Anjian-Wen](chinese-contributors.md#anjian-wen-字节跳动) | 字节跳动 | 12 | RISC-V |
| [Kuai Wei](chinese-contributors.md#kuai-wei-阿里巴巴) | 阿里巴巴 | 4 | C2 编译器 |
| [han gq](chinese-contributors.md#han-gq-麒麟) | 麒麟 | 2 | 编译器 |
| [Tongbao Zhang](chinese-contributors.md#tongbao-zhang-腾讯) | 腾讯 | 1 | G1 GC |

---

## 如何阅读贡献者页面

每个贡献者页面包含:

1. **基本信息**: 姓名、组织、专注领域
2. **贡献统计**: Commits 数量、JEP 参与
3. **PR 列表**: 按类别组织的详细 PR 列表
4. **关键贡献**: 最重要的几个贡献详解
5. **代码示例**: 相关代码变更示例
6. **相关链接**: OpenJDK 页面、邮件列表等