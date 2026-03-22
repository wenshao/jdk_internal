# JDK PR Analysis Index

> Last updated: 2026-03-19

---

## JDK 26 Overview

JDK 26 is the current non-LTS release. This document provides an index to all JDK 26 PR and commit analysis.

### Quick Stats

| Metric | Value |
|--------|-------|
| Total Commits | 3,936 |
| Development Period | 2025-06 to 2026-03 |
| Top Contributors | Thomas Schatzl (140), Albert Mingkun Yang (136), Phil Race (110) |

### Component Distribution

| Component | Commits | Percentage |
|-----------|---------|------------|
| GC | 745 | 18.9% |
| Compiler | 725 | 18.4% |
| Core | 694 | 17.6% |
| Test | 491 | 12.5% |
| Other | 423 | 10.7% |
| Security | 234 | 5.9% |
| Network | 208 | 5.3% |
| Concurrency | 177 | 4.5% |
| Build | 153 | 3.9% |
| JFR | 86 | 2.2% |

---

## JEPs in JDK 26

> 详细分析: [JEP 深度分析](./jeps/jdk26-jeps.md)

| JEP | Title | Issue | Status |
|-----|-------|-------|--------|
| 516 | Ahead-of-Time Object Caching | 8365932 | ✅ |
| 517 | HTTP/3 for the HTTP Client | 8349910 | ✅ |
| 519 | Compact Object Headers | 8373845 | ✅ |
| 521 | Generational Shenandoah | 8350562 | ✅ |
| 522 | G1 GC Throughput Improvements | 8342382 | ✅ |
| 524 | PEM Encodings | 8360564 | ✅ |
| 525 | Structured Concurrency (6th Preview) | 8367857 | ✅ |
| 526 | Lazy Constants (2nd Preview) | 8366178 | ✅ |
| 500 | Prepare to Make Final Mean Final | 8353835 | ✅ |
| 504 | Remove Applet API | 8359053 | ✅ |
| 509 | JFR CPU-Time Profiling | 8342818 | ✅ |
| 527 | TLS 1.3 Hybrid Key Exchange | 8314323 | ✅ |

---

## Key Documents

- **[Full Commit Report](./jdk26-commits.md)** - Complete analysis of all 3,936 commits
- **[Top 50 PRs](./jdk26-top-prs.md)** - Most impactful commits by code changes
- **[JEP Analysis](./jeps/jdk26-jeps.md)** - Detailed JEP analysis
- **[Analysis Strategy](./ANALYSIS_STRATEGY.md)** - Methodology and approach

---

## Component Reports

| Component | Commits | Report |
|-----------|---------|--------|
| GC | 745 | [gc.md](./components/gc.md) |
| Compiler | 725 | [compiler.md](./components/compiler.md) |
| Network | 208 | [network.md](./components/network.md) |
| Security | 234 | [security.md](./components/security.md) |

---

## Top 30 Contributors

| Rank | Contributor | Commits | Focus Areas |
|------|-------------|---------|-------------|
| 1 | Thomas Schatzl | 140 | G1 GC |
| 2 | Albert Mingkun Yang | 136 | GC, Parallel GC |
| 3 | Phil Race | 110 | Printing, Desktop |
| 4 | Matthias Baesken | 105 | Build, Ports |
| 5 | Alexey Semenyuk | 85 | jpackage |
| 6 | Aleksey Shipilev | 80 | Shenandoah, Performance |
| 7 | Ioi Lam | 76 | CDS, AOT |
| 8 | Kim Barrett | 76 | GC, HotSpot |
| 9 | SendaoYan | 71 | Testing |
| 10 | Jaikiran Pai | 67 | Networking |
| 11 | Francesco Andreuzzi | 60 | Testing |
| 12 | Prasanta Sadhukhan | 59 | Desktop |
| 13 | Chen Liang | 59 | ClassFile API, Core |
| 14 | Sergey Bylokhov | 57 | Desktop |
| 15 | Erik Gahlin | 57 | JFR |
| 16 | Brian Burkhalter | 53 | Networking |
| 17 | Axel Boldt-Christmas | 52 | ZGC |
| 18 | David Holmes | 50 | Threading |
| 19 | Emanuel Peter | 49 | C2 Compiler |
| 20 | Jan Lahoda | 48 | javac |
| 21 | Daniel Fuchs | 47 | HTTP Client |
| 22 | Volkan Yazici | 45 | HTTP Client |
| 23 | Joel Sikström | 44 | ZGC |
| 24 | Justin Lu | 43 | Localization |
| 25 | William Kemper | 43 | Shenandoah |
| 26 | Manuel Hässig | 39 | Testing |
| 27 | Naoto Sato | 36 | i18n |
| 28 | Leonid Mesnik | 33 | JVMTI |
| 29 | Coleen Phillimore | 32 | HotSpot |
| 30 | Yasumasa Suenaga | 32 | Serviceability |

---

## Major Changes by Area

### GC (Garbage Collection)

- **G1**: Throughput improvements (JEP 522), heap resizing optimizations
- **Shenandoah**: Generational mode (JEP 521), improved allocation
- **ZGC**: Allocator cleanup, uncommit logic improvements
- **Parallel**: Improved heap resizing heuristics

### Compiler (C1/C2)

- Template-based testing framework
- SuperWord vectorization improvements
- Known bits analysis for TypeInt/Long
- RISC-V backend improvements
- AVX10/AVX512 intrinsics

### Network

- **HTTP/3** (JEP 517): Full implementation with QUIC
- **TLS 1.3**: Hybrid key exchange (JEP 527)
- HttpClient improvements: CUBIC congestion control
- PEM encodings (JEP 524)

### Security

- Post-quantum cryptography: ML-KEM, ML-DSA improvements
- Hybrid Public Key Encryption (HPKE)
- Certificate validation enhancements
- PKCS#12 improvements

### Core Libraries

- **Structured Concurrency** (JEP 525): 6th preview
- **Lazy Constants** (JEP 526): 2nd preview
- CLDR 48.0 update
- Unicode 17.0.0 support
- JDBC 4.5 MR support

---

## Detailed PR Analysis

Individual PR analysis documents:

| Directory | Description | Files |
|-----------|-------------|-------|
| [8298/](./8298/) | Early JDK 26 backports | 1 |
| [8326/](./8326/) | Core library changes | 1 |
| [8347/](./8347/) | Security changes | 1 |
| [8359/](./8359/) | Mid-development changes | 1 |
| [8370/](./8370/) | JEP implementations | 4 |
| [8371/](./8371/) | Compiler/GC changes | 6 |
| [8372/](./8372/) | Late-stage changes | 2 |

---

## Related Resources

- [Contributors](/by-contributor/) - Contributor profiles and statistics
- [Guides](/guides/) - JDK development guides
- [Issues](/issues/) - Issue analysis
- [Deep Dive](/deep-dive/) - In-depth technical analysis

---

## Change Log

| Date | Change |
|------|--------|
| 2026-03-19 | Initial JDK 26 analysis with 3,936 commits |
| 2026-03-19 | Added JEP deep analysis, component reports |
