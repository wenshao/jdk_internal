# JDK 26 开发者贡献分析

> 本文档分析 JDK 26 中做出重要贡献的开发者，基于 git commit 统计。

---

## 概览

JDK 26 包含 **4,913 个 commit**，由 **300+ 位开发者** 贡献。以下是贡献最突出的开发者分析。

---

## 贡献者排行榜

### Top 20 贡献者

| 排名 | 开发者 | Commits | 主要领域 |
|------|--------|---------|----------|
| 1 | Albert Mingkun Yang | 124 | GC (G1/Parallel) |
| 2 | Aleksey Shipilev | 120 | 编译器、性能优化 |
| 3 | Matthias Baesken | 117 | 构建系统、跨平台 |
| 4 | Ioi Lam | 109 | AOT/CDS |
| 5 | Magnus Ihse Bursie | 106 | 构建系统 |
| 6 | Thomas Schatzl | 95 | G1 GC |
| 7 | Alexey Semenyuk | 93 | 安装程序、打包 |
| 8 | SendaoYan | 88 | 测试、Bug 修复 |
| 9 | Chen Liang | 85 | 核心库、反射 |
| 10 | Erik Gahlin | 74 | JFR |
| 11 | Phil Race | 69 | 安全、图形 |
| 12 | Coleen Phillimore | 68 | JVM 核心 |
| 13 | Kim Barrett | 65 | 并发、原子操作 |
| 14 | Hamlin Li | 65 | C2 编译器、RISC-V |
| 15 | David Holmes | 65 | 并发、线程 |
| 16 | Brian Burkhalter | 65 | 网络 |
| 17 | Jaikiran Pai | 64 | HttpClient |
| 18 | Prasanta Sadhukhan | 62 | Swing、AWT |
| 19 | Jan Lahoda | 62 | javac、JShell |
| 20 | William Kemper | 60 | Shenandoah GC |

---

## JEP 主要贡献者

> 以下开发者主导了 JDK 26 的 JEP 实现

### 语言与编译器

| JEP | 开发者 | 组织 |
|-----|--------|------|
| **JEP 511**: Module Import Declarations | Jan Lahoda | Oracle |
| **JEP 512**: Compact Source Files | Jan Lahoda | Oracle |
| **JEP 530**: Primitive Types in Patterns | Aggelos Biboudis | Oracle |

### 并发编程

| JEP | 开发者 | 组织 |
|-----|--------|------|
| **JEP 525**: Structured Concurrency | Alan Bateman | Oracle |
| **JEP 506**: Scoped Values | Andrew Haley | Red Hat |
| **JEP 502**: Stable Values | Per Minborg | Oracle |
| **JEP 526**: Lazy Constants | Per Minborg | Oracle |

### 网络

| JEP | 开发者 | 组织 |
|-----|--------|------|
| **JEP 517**: HTTP/3 | Daniel Fuchs | Oracle |

### GC 与性能

| JEP | 开发者 | 组织 |
|-----|--------|------|
| **JEP 522**: G1 GC Throughput | Thomas Schatzl | Oracle |
| **JEP 521**: Generational Shenandoah | William Kemper | Red Hat |
| **JEP 519**: Compact Object Headers | Roman Kennke | Red Hat |
| **JEP 514**: AOT Ergonomics | Ioi Lam | Oracle |
| **JEP 515**: AOT Profiling | Igor Veresov | Oracle |

### 监控诊断

| JEP | 开发者 | 组织 |
|-----|--------|------|
| **JEP 509**: JFR CPU-Time Profiling | Johannes Bechberger | SAP |
| **JEP 518**: JFR Cooperative Sampling | Markus Grönlund | Oracle |
| **JEP 520**: JFR Method Timing | Erik Gahlin | Oracle |

### 安全

| JEP | 开发者 | 组织 |
|-----|--------|------|
| **JEP 500**: Make Final Mean Final | Alan Bateman | Oracle |
| **JEP 510**: KDF API | Weijun Wang | Oracle |
| **JEP 470**: PEM Encodings | Anthony Scarpino | Oracle |

### 移除与清理

| JEP | 开发者 | 组织 |
|-----|--------|------|
| **JEP 503**: Remove 32-bit x86 | Aleksey Shipilev | Oracle |
| **JEP 504**: Remove Applet API | Phil Race | Oracle |

---

## 领域专家

### GC 专家

#### Thomas Schatzl (Oracle)
- **Commits**: 95
- **主要贡献**: JEP 522 (G1 GC Throughput Improvement)
- **关键工作**:
  - G1 IHOP 优化
  - G1 收集集选择改进
  - GC 暂停时间优化

```
代表性 commits:
- 8342382: Implement JEP 522: G1 GC: Improve Throughput
- 8371791: G1: Improve accuracy of non_young_occupancy_after_allocation
- 8274178: G1: Occupancy value in IHOP logging is inaccurate
```

#### Albert Mingkun Yang (Oracle)
- **Commits**: 124 (最多)
- **主要贡献**: G1 和 Parallel GC 优化
- **关键工作**:
  - G1 代码清理和重构
  - Parallel GC 改进
  - TLAB 优化

```
代表性 commits:
- 8372162: G1: Merge subclasses of G1IHOPControl
- 8371985: Parallel: Move should_attempt_scavenge
- 8371465: Parallel: Revise asserts around heap expansion
```

#### William Kemper (Red Hat)
- **Commits**: 60
- **主要贡献**: JEP 521 (Generational Shenandoah)
- **关键工作**:
  - 分代 Shenandoah 实现
  - Shenandoah 性能优化

### 编译器专家

#### Aleksey Shipilev (Oracle)
- **Commits**: 120
- **主要贡献**: JEP 503, C2 优化
- **关键工作**:
  - 移除 32位 x86 支持
  - C2 编译器优化
  - 性能基准测试

```
代表性 commits:
- 8345169: Implement JEP 503: Remove the 32-bit x86 Port
- 8371581: C2: PhaseCCP should reach fixpoint
- 8370318: AES-GCM vector intrinsic may read out of bounds
```

#### Hamlin Li (Oracle)
- **Commits**: 65
- **主要贡献**: C2 SuperWord, RISC-V
- **关键工作**:
  - SuperWord 向量化修复
  - RISC-V 后端优化

```
代表性 commits:
- 8370794: C2 SuperWord: Long/Integer.compareUnsigned return wrong value
- 8369685: RISC-V: refactor code related to RVFeatureValue
```

### 网络专家

#### Daniel Fuchs (Oracle)
- **Commits**: 49
- **主要贡献**: JEP 517 (HTTP/3)
- **关键工作**:
  - HTTP/3 客户端实现
  - QUIC 协议栈
  - HttpClient 虚拟线程支持

```
代表性 commits:
- 8349910: Implement JEP 517: HTTP/3 for the HTTP Client API
- 8372159: HttpClient SelectorManager thread could be a VirtualThread
- 8371471: HttpClient: Log HTTP/3 handshake failures
```

#### Daniel Jeliński (Oracle)
- **Commits**: 42
- **主要贡献**: HTTP/3 拥塞控制
- **关键工作**:
  - CUBIC 拥塞控制实现
  - QUIC pacing 实现

```
代表性 commits:
- 8371475: HttpClient: Implement CUBIC congestion controller
- 8370024: HttpClient: QUIC congestion controller doesn't implement pacing
```

#### Jaikiran Pai (Oracle)
- **Commits**: 64
- **主要贡献**: HttpClient bug 修复
- **关键工作**:
  - HTTP/2 连接泄漏修复 (严重 bug)
  - HTTP/3 错误处理

```
代表性 commits:
- 8326498: java.net.http.HttpClient connection leak using http/2
- 8369812: HttpClient doesn't handle H3_REQUEST_REJECTED correctly
```

### JFR 专家

#### Erik Gahlin (Oracle)
- **Commits**: 74
- **主要贡献**: JEP 520 (JFR Method Timing)
- **关键工作**:
  - JFR 事件优化
  - JFR 流式 API 改进

```
代表性 commits:
- 8352738: Implement JEP 520: JFR Method Timing and Tracing
- 8365972: JFR: ThreadDump and ClassLoaderStatistics events
- 8247776: JFR: TestThreadContextSwitches.java failed
```

#### Johannes Bechberger (SAP)
- **Commits**: 40
- **主要贡献**: JEP 509 (JFR CPU-Time Profiling)
- **关键工作**:
  - CPU 时间采样实现
  - JFR 性能优化

```
代表性 commits:
- 8358666: [REDO] Implement JEP 509: JFR CPU-Time Profiling
```

### AOT/CDS 专家

#### Ioi Lam (Oracle)
- **Commits**: 109
- **主要贡献**: JEP 514 (AOT Ergonomics)
- **关键工作**:
  - AOT 链接优化
  - CDS 改进
  - 启动性能优化

```
代表性 commits:
- 8355798: Implement JEP 514: Ahead-of-Time Command Line Ergonomics
- 8369742: Link AOT-linked classes at JVM bootstrap
- 8363986: Heap region in CDS archive is not at deterministic address
```

### 安全专家

#### Anthony Scarpino (Oracle)
- **Commits**: 35
- **主要贡献**: JEP 470 (PEM Encodings)
- **关键工作**:
  - PEM 编解码实现
  - 加密 API 改进

```
代表性 commits:
- 8360564: Implement JEP 524: PEM Encodings (Second Preview)
- 8298420: Implement JEP 470: PEM Encodings (Preview)
```

#### Weijun Wang (Oracle)
- **Commits**: 29
- **主要贡献**: JEP 510 (KDF API)
- **关键工作**:
  - 密钥派生函数 API
  - 安全 API 改进

```
代表性 commits:
- 8353888: Implement JEP 510: Key Derivation Function API
```

### 核心库专家

#### Chen Liang (Oracle)
- **Commits**: 85
- **主要贡献**: 核心反射 API
- **关键工作**:
  - 反射 API 改进
  - Class-File API 改进

```
代表性 commits:
- 8371953: Document null handling in core reflection APIs
- 8370976: Review the behavioral changes of core reflection
- 8367585: Prevent creation of unrepresentable Utf8Entry
```

#### Alan Bateman (Oracle)
- **Commits**: 28
- **主要贡献**: JEP 500, JEP 525
- **关键工作**:
  - final 字段安全限制
  - 结构化并发

```
代表性 commits:
- 8353835: Implement JEP 500: Prepare to Make Final Mean Final
- 8367857: Implement JEP 525: Structured Concurrency (Sixth Preview)
```

---

## 组织贡献

### Oracle
- **贡献者**: 200+
- **Commits**: ~4,000 (80%+)
- **主导 JEP**: 18/21

### Red Hat
- **主要贡献者**: William Kemper, Roman Kennke, Andrew Haley
- **主导 JEP**: JEP 506, JEP 519, JEP 521

### SAP
- **主要贡献者**: Johannes Bechberger
- **主导 JEP**: JEP 509

### 独立贡献者
- **Per Minborg**: JEP 502, JEP 526

---

## 新星贡献者

### Joel Sikström
- **Commits**: 42
- **主要贡献**: NUMA 优化
- **关键工作**:
  - NUMA 线程亲和性
  - ZGC NUMA-Aware Relocation

```
代表性 commits:
- 8371701: Add ability to set NUMA-affinity for threads
- 8359683: ZGC: NUMA-Aware Relocation
```

### Volkan Yazici
- **Commits**: 49
- **主要贡献**: HttpClient 改进
- **关键工作**:
  - HttpClient API 清理
  - 废弃 API 移除

```
代表性 commits:
- 8366577: Deprecate java.net.Socket::setPerformancePreferences
- 8366575: Remove SDP support
```

---

## 贡献类型分布

| 类型 | 开发者 | 说明 |
|------|--------|------|
| JEP 实现 | 20+ | 主导新特性开发 |
| 性能优化 | 50+ | GC、编译器、核心库优化 |
| Bug 修复 | 100+ | 各种 bug 修复 |
| 测试 | 80+ | 测试用例编写和维护 |
| 构建/基础设施 | 30+ | 构建系统、CI/CD |
| 文档 | 40+ | API 文档、规范 |

---

## 总结

JDK 26 的开发由 **Oracle 主导**，贡献了 80%+ 的代码。**Red Hat** 在 GC (Shenandoah) 和并发领域有重要贡献，**SAP** 贡献了 JFR CPU-Time Profiling。

关键贡献者：
- **Albert Mingkun Yang**: 最多 commits，GC 优化
- **Thomas Schatzl**: G1 GC 核心优化
- **Daniel Fuchs**: HTTP/3 实现
- **Jan Lahoda**: 语言特性 (模块导入、紧凑源文件)
- **Ioi Lam**: AOT/CDS 优化
- **Erik Gahlin**: JFR 改进

---

## 相关链接

- [OpenJDK Contributors](https://openjdk.org/census)
- [JDK 26 Commits](https://github.com/openjdk/jdk/commits/jdk-26+26)
- [OpenJDK Groups](https://openjdk.org/groups)