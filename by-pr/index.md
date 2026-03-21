# JDK PR Analysis Index

> Last updated: 2026-03-22

---

## JDK 26 Overview

JDK 26 is the current non-LTS release. This document provides an index to all JDK 26 PR and commit analysis.

### Quick Stats

| Metric | Value |
|--------|-------|
| Total Commits | 3,439 |
| Development Period | 2025-06 to 2026-03 |
| Top Contributors | Thomas Schatzl (130), Albert Mingkun Yang (120), Matthias Baesken (90) |

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
| 500 | Prepare to Make Final Mean Final | 8353835 | ✅ |
| 504 | Remove Applet API | 8359053 | ✅ |
| 516 | Ahead-of-Time Object Caching | 8365932 | ✅ |
| 517 | HTTP/3 for the HTTP Client | 8349910 | ✅ |
| 522 | G1 GC Throughput Improvements | 8342382 | ✅ |
| 524 | PEM Encodings | 8360564 | ✅ |
| 525 | Structured Concurrency (6th Preview) | 8367857 | ✅ |
| 526 | Lazy Constants (2nd Preview) | 8366178 | ✅ |
| 529 | Vector API (11th Incubator) | 8369012 | ✅ |
| 530 | Primitive Types in Patterns (4th Preview) | 8359136 | ✅ |

> **Note**: JEP 519, 521, 509, 527 were delivered in JDK 25 or later, not JDK 26.

---

## Key Documents

- **[Full Commit Report](./jdk26-commits.md)** - Complete analysis of all 3,439 commits
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
| 1 | Thomas Schatzl | 130 | G1 GC |
| 2 | Albert Mingkun Yang | 120 | GC, Parallel GC |
| 3 | Matthias Baesken | 90 | Build, Ports |
| 4 | Phil Race | 79 | Printing, Desktop |
| 5 | Aleksey Shipilev | 76 | Shenandoah, Performance |
| 6 | Kim Barrett | 69 | GC, HotSpot |
| 7 | Ioi Lam | 68 | CDS, AOT |
| 8 | Alexey Semenyuk | 67 | jpackage |
| 9 | SendaoYan | 61 | Testing |
| 10 | Francesco Andreuzzi | 60 | Testing |
| 11 | Prasanta Sadhukhan | 55 | Desktop |
| 12 | Jaikiran Pai | 54 | Networking |
| 13 | Erik Gahlin | 54 | JFR |
| 14 | Chen Liang | 54 | ClassFile API, Core |
| 15 | Sergey Bylokhov | 46 | Desktop |
| 16 | David Holmes | 46 | Threading |
| 17 | Emanuel Peter | 46 | C2 Compiler |
| 18 | Axel Boldt-Christmas | 46 | ZGC |
| 19 | Brian Burkhalter | 43 | Networking |
| 20 | Volkan Yazici | 41 | HTTP Client |
| 21 | Jan Lahoda | 41 | javac |
| 22 | Justin Lu | 40 | Localization |
| 23 | Joel Sikström | 40 | ZGC |
| 24 | William Kemper | 39 | Shenandoah |
| 25 | Manuel Hässig | 33 | Testing |
| 26 | Leonid Mesnik | 32 | JVMTI |
| 27 | Naoto Sato | 31 | i18n |
| 28 | Daniel Fuchs | 30 | HTTP Client |
| 29 | Mikhail Yankelevich | 29 | Build |
| 30 | Magnus Ihse Bursie | 29 | Build |

---

## Major Changes by Area

### GC (Garbage Collection)

- **G1**: Throughput improvements (JEP 522), heap resizing optimizations
- **Shenandoah**: Improved allocation, concurrent refinement
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
- **Vector API** (JEP 529): 11th incubator
- **Primitive Types in Patterns** (JEP 530): 4th preview
- CLDR 48.0 update
- Unicode 17.0.0 support
- JDBC 4.5 MR support

---

## Detailed PR Analysis

Individual PR analysis documents organized by issue prefix:

| Directory | Description | Files |
|-----------|-------------|-------|
| [8298/](./8298/) | Early JDK 26 backports | 1 |
| [8310/](./8310/) | Core library changes | 3 |
| [8311/](./8311/) | HotSpot changes | 4 |
| [8315/](./8315/) | Build changes | 2 |
| [8316/](./8316/) | Compiler changes | 2 |
| [8317/](./8317/) | Security changes | 1 |
| [8324/](./8324/) | Core changes | 1 |
| [8326/](./8326/) | Core library changes | 1 |
| [8327/](./8327/) | Network changes | 1 |
| [8328/](./8328/) | Core changes | 1 |
| [8331/](./8331/) | Core changes | 1 |
| [8332/](./8332/) | Core changes | 1 |
| [8333/](./8333/) | Compiler changes | 4 |
| [8334/](./8334/) | Core changes | 2 |
| [8335/](./8335/) | GC changes | 4 |
| [8336/](./8336/) | Compiler changes | 6 |
| [8337/](./8337/) | HotSpot changes | 5 |
| [8338/](./8338/) | Compiler changes | 7 |
| [8339/](./8339/) | Core changes | 12 |
| [8340/](./8340/) | Compiler changes | 6 |
| [8341/](./8341/) | Core changes | 14 |
| [8342/](./8342/) | Core changes | 2 |
| [8343/](./8343/) | Core changes | 7 |
| [8344/](./8344/) | Core changes | 2 |
| [8346/](./8346/) | ClassFile API changes | 1 |
| [8347/](./8347/) | Security changes | 4 |
| [8348/](./8348/) | Core changes | 3 |
| [8349/](./8349/) | Network changes | 6 |
| [8351/](./8351/) | Core changes | 2 |
| [8353/](./8353/) | Core changes | 1 |
| [8355/](./8355/) | GC changes | 12 |
| [8356/](./8356/) | GC changes | 4 |
| [8357/](./8357/) | GC changes | 7 |
| [8359/](./8359/) | Mid-development changes | 1 |
| [8362/](./8362/) | Core changes | 1 |
| [8364/](./8364/) | Core changes | 1 |
| [8365/](./8365/) | JEP implementations | 4 |
| [8366/](./8366/) | Core changes | 2 |
| [8368/](./8368/) | Core changes | 3 |
| [8370/](./8370/) | JEP implementations | 7 |
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
| 2026-03-22 | Added 8346 directory, updated file counts, fixed contributor ranking |
| 2026-03-21 | Updated commit count (3,439), contributor stats, JEP list |
| 2026-03-19 | Initial JDK 26 analysis with 3,936 commits |
| 2026-03-19 | Added JEP deep analysis, component reports |