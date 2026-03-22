# JDK 25 Top Contributors

> Based on GitHub Integrated PRs (2024-2025)

---
## 目录

1. [Overview](#1-overview)
2. [Top 50 by PR Count](#2-top-50-by-pr-count)
3. [By Organization](#3-by-organization)
4. [By Component](#4-by-component)
5. [Key JEPs in JDK 25](#5-key-jeps-in-jdk-25)
6. [Data Sources](#6-data-sources)

---


## 1. Overview

JDK 25 had **~400 unique contributors** making Integrated PRs during its development cycle (March 2024 - March 2025).

**Key Statistics**:
- **Total Integrated PRs**: ~5,117
- **Top Contributor**: Thomas Schatzl (150+ PRs)
- **Dominant Organization**: Oracle (70%+)
- **Key Features**: Compact Object Headers, JFR Enhancements, AOT Cache

---

## 2. Top 50 by PR Count

| Rank | Contributor | Organization | PRs | Primary Focus | Profile |
|------|-------------|--------------|-----|---------------|---------|
| 1 | [Thomas Schatzl](thomas-schatzl.md) | Oracle | 150+ | G1 GC | [详情](thomas-schatzl.md) |
| 2 | [Albert Mingkun Yang](albert-mingkun-yang.md) | Oracle | 120+ | GC | [详情](albert-mingkun-yang.md) |
| 3 | [Phil Race](phil-race.md) | Oracle | 100+ | Printing, Desktop | [详情](phil-race.md) |
| 4 | [Matthias Baesken](matthias-baesken.md) | SAP | 90+ | Build, Ports | [详情](matthias-baesken.md) |
| 5 | [Aleksey Shipilev](aleksey-shipilev.md) | Amazon | 85+ | Shenandoah, JMH | [详情](aleksey-shipilev.md) |
| 6 | [Ioi Lam](ioi-lam.md) | Oracle | 80+ | CDS, AOT | [详情](ioi-lam.md) |
| 7 | [Kim Barrett](kim-barrett.md) | Oracle | 75+ | GC | [详情](kim-barrett.md) |
| 8 | [Sendaoyan](sendaoyan.md) | Independent | 70+ | Testing | [详情](sendaoyan.md) |
| 9 | [Jaikiran Pai](jaikiran-pai.md) | Oracle | 65+ | Networking | [详情](jaikiran-pai.md) |
| 10 | [Chen Liang](chen-liang.md) | Oracle | 60+ | ClassFile API | [详情](chen-liang.md) |
| 11 | [Prasanta Sadhukhan](prasanta-sadhukhan.md) | Oracle | 55+ | Desktop | [详情](prasanta-sadhukhan.md) |
| 12 | Sergey Bylokhov | Oracle | 50+ | Desktop | - |
| 13 | [Erik Gahlin](erik-gahlin.md) | Oracle | 50+ | JFR | [详情](erik-gahlin.md) |
| 14 | [Brian Burkhalter](brian-burkhalter.md) | Oracle | 50+ | NIO | [详情](brian-burkhalter.md) |
| 15 | [David Holmes](david-holmes.md) | Oracle | 45+ | Threading | [详情](david-holmes.md) |
| 16 | [Emanuel Peter](emanuel-peter.md) | Oracle | 45+ | C2 Compiler | [详情](emanuel-peter.md) |
| 17 | [Jan Lahoda](jan-lahoda.md) | Oracle | 40+ | javac | [详情](jan-lahoda.md) |
| 18 | [Daniel Fuchs](daniel-fuchs.md) | Oracle | 40+ | HTTP Client | [详情](daniel-fuchs.md) |
| 19 | [Volkan Yazici](volkan-yazici.md) | Oracle | 35+ | HTTP Client | [详情](volkan-yazici.md) |
| 20 | [Justin Lu](justin-lu.md) | Oracle | 35+ | Localization | [详情](justin-lu.md) |
| 21 | [William Kemper](william-kemper.md) | Amazon | 35+ | Shenandoah | [详情](william-kemper.md) |
| 22 | [Naoto Sato](naoto-sato.md) | Oracle | 30+ | i18n | [详情](naoto-sato.md) |
| 23 | [Leonid Mesnik](leonid-mesnik.md) | Oracle | 30+ | JVMTI | [详情](leonid-mesnik.md) |
| 24 | [Coleen Phillimore](coleen-phillimore.md) | Oracle | 28+ | HotSpot | [详情](coleen-phillimore.md) |
| 25 | [Claes Redestad](claes-redestad.md) | Oracle | 25+ | Performance | [详情](claes-redestad.md) |
| 26 | [Magnus Ihse Bursie](magnus-ihse-bursie.md) | Oracle | 25+ | Build | [详情](magnus-ihse-bursie.md) |
| 27 | [Shaojin Wen](shaojin-wen.md) | Alibaba | 25+ | Core Libs | [详情](shaojin-wen.md) |
| 28 | Yasumasa Suenaga | NTT DATA | 20+ | Serviceability | - |
| 29 | [Fei Yang](fei-yang.md) | Huawei | 20+ | RISC-V | [详情](fei-yang.md) |
| 30 | [Hamlin Li](hamlin-li.md) | Oracle | 18+ | RISC-V | [详情](hamlin-li.md) |
| 31 | [Anjian Wen](anjian-wen.md) | ByteDance | 15+ | RISC-V | [详情](anjian-wen.md) |
| 32 | [Roman Kennke](roman-kennke.md) | Datadog | 15+ | Compact Headers | [详情](roman-kennke.md) |
| 33 | [Johannes Bechberger](johannes-bechberger.md) | SAP | 15+ | JFR | [详情](johannes-bechberger.md) |
| 34 | [Per Minborg](per-minborg.md) | Oracle | 12+ | Core Libs | [详情](per-minborg.md) |
| 35 | [Jatin Bhateja](jatin-bhateja.md) | Intel | 12+ | Vector API | [详情](jatin-bhateja.md) |
| 36 | Roland Westrelin | Red Hat | 12+ | C2 Compiler | - |
| 37 | [Weijun Wang](weijun-wang.md) | Oracle | 12+ | Security | [详情](weijun-wang.md) |
| 38 | [Alexey Semenyuk](alexey-semenyuk.md) | Oracle | 10+ | jpackage | [详情](alexey-semenyuk.md) |
| 39 | [Alan Bateman](alan-bateman.md) | Oracle | 10+ | Concurrency | [详情](alan-bateman.md) |
| 40 | [Erik Österlund](erik-osterlund.md) | Oracle | 10+ | AOT, GC | [详情](erik-osterlund.md) |
| 41 | [Andrew Haley](andrew-haley.md) | Red Hat | 8+ | RISC-V | [详情](andrew-haley.md) |
| 42 | [Doug Simon](doug-simon.md) | Oracle Labs | 8+ | Graal | [详情](doug-simon.md) |
| 43 | [Christian Hagedorn](christian-hagedorn.md) | Oracle Labs | 8+ | Graal | [详情](christian-hagedorn.md) |
| 44 | [Yude Lin](yude-lin.md) | Alibaba | 8+ | Compiler | [详情](yude-lin.md) |
| 45 | [Xiaowei Lu](xiaowei-lu.md) | Alibaba | 8+ | ZGC | [详情](xiaowei-lu.md) |
| 46 | [Kuai Wei](kuai-wei.md) | Alibaba | 7+ | Compiler | [详情](kuai-wei.md) |
| 47 | [Tongbao Zhang](tongbao-zhang.md) | Alibaba | 6+ | Testing | [详情](tongbao-zhang.md) |
| 48 | [Han GQ](han-gq.md) | Alibaba | 5+ | Core | [详情](han-gq.md) |
| 49 | [Jaroslav Bachorik](jaroslav-bachorik.md) | DataDog | 5+ | JFR Tools | [详情](jaroslav-bachorik.md) |
| 50 | [Francesco Andreuzzi](francesco-andreuzzi.md) | Oracle | 5+ | Testing | [详情](francesco-andreuzzi.md) |

> **Note**: PR counts are approximate. Data based on GitHub Integrated PRs with `label:integrated`.

---

## 3. By Organization

| Organization | Contributors | PRs | Share |
|--------------|--------------|-----|-------|
| **Oracle** | 300+ | 3,500+ | 70%+ |
| **Red Hat** | 40+ | 500+ | 10% |
| **SAP** | 25+ | 250+ | 5% |
| **Amazon** | 20+ | 200+ | 4% |
| **Alibaba** | 10+ | 100+ | 2% |
| **IBM** | 15+ | 150+ | 3% |
| **Others** | 50+ | 300+ | 6% |

---

## 4. By Component

| Component | Top Contributors | PRs |
|-----------|------------------|-----|
| **GC** | Thomas Schatzl, Albert Yang, William Kemper | 800+ |
| **Compiler** | Emanuel Peter, Roland Westrelin, Jatin Bhateja | 400+ |
| **Core Libs** | Claes Redestad, Shaojin Wen, Brian Burkhalter | 600+ |
| **Build** | Matthias Baesken, Magnus Ihse Bursie | 300+ |
| **JFR** | Erik Gahlin, Jaroslav Bachorik | 150+ |
| **Desktop** | Phil Race, Prasanta Sadhukhan | 250+ |
| **Network** | Daniel Fuchs, Volkan Yazici | 200+ |
| **Security** | Weijun Wang, Sean Mullan | 150+ |

---

## 5. Key JEPs in JDK 25

| JEP | Title | Lead Contributors |
|-----|---------|-------------------|
| JEP 519 | Compact Object Headers | Roman Kennke, Stefan Karlsson |
| JEP 509 | JFR CPU-Time Profiling | Erik Gahlin, Markus Grönlund |
| JEP 518 | JFR Cooperative Sampling | Markus Grönlund |
| JEP 520 | JFR Method Timing | Erik Gahlin |
| JEP 483 | AOT Class Loading | Ioi Lam, Erik Österlund |
| JEP 514 | AOT Command-Line Ergonomics | John Rose |
| JEP 515 | AOT Method Analysis | Ioi Lam |

---

## 6. Data Sources

**Primary Source**: [GitHub Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+label%3Aintegrated+is%3Aclosed)

**Query Format**:
```
https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3A{username}+label%3Aintegrated+is%3Aclosed
```

**Why PRs NOT commits?**
- OpenJDK Committers use `@openjdk.org` email for commits
- Git commits by company email domain is inaccurate
- GitHub PRs accurately reflect actual contributions

**Last Updated**: 2026-03-21

---

## Related Pages

- [JDK 26 Top Contributors](jdk26-top-contributors.md)
- [JDK 21 Top Contributors](jdk21-top-contributors.md)
- [All Contributors](/by-contributor/)
- [By Organization](/contributors/stats/by-org.md)
