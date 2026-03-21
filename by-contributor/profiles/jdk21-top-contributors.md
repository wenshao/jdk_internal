# JDK 21 Top Contributors

> Based on GitHub Integrated PRs (2022-2023)

---
## 目录

1. [Overview](#1-overview)
2. [Top 50 by PR Count](#2-top-50-by-pr-count)
3. [By Organization](#3-by-organization)
4. [By Component](#4-by-component)
5. [Key Features in JDK 21](#5-key-features-in-jdk-21)
6. [Data Sources](#6-data-sources)

---


## 1. Overview

JDK 21 LTS (GA: 2023-09) had **~380 unique contributors** making Integrated PRs during its development cycle.

**Key Statistics**:
- **Total Integrated PRs**: ~4,729
- **Top Contributor**: Thomas Schatzl (120+ PRs)
- **Dominant Organization**: Oracle (70%+)
- **Key Features**: Virtual Threads, Pattern Matching, Generational ZGC

---

## 2. Top 50 by PR Count

| Rank | Contributor | Organization | PRs | Primary Focus | Profile |
|------|-------------|--------------|-----|---------------|---------|
| 1 | [Thomas Schatzl](thomas-schatzl.md) | Oracle | 120+ | G1 GC | [详情](thomas-schatzl.md) |
| 2 | [Albert Mingkun Yang](albert-mingkun-yang.md) | Oracle | 100+ | GC | [详情](albert-mingkun-yang.md) |
| 3 | [Phil Race](phil-race.md) | Oracle | 90+ | Printing, Desktop | [详情](phil-race.md) |
| 4 | [Matthias Baesken](matthias-baesken.md) | SAP | 85+ | Build, Ports | [详情](matthias-baesken.md) |
| 5 | [Aleksey Shipilev](aleksey-shipilev.md) | Amazon | 80+ | Shenandoah, JMH | [详情](aleksey-shipilev.md) |
| 6 | [Kim Barrett](kim-barrett.md) | Oracle | 75+ | GC | [详情](kim-barrett.md) |
| 7 | [Ioi Lam](ioi-lam.md) | Oracle | 70+ | CDS | [详情](ioi-lam.md) |
| 8 | [Sendaoyan](sendaoyan.md) | Independent | 65+ | Testing | [详情](sendaoyan.md) |
| 9 | [Jaikiran Pai](jaikiran-pai.md) | Oracle | 60+ | Networking | [详情](jaikiran-pai.md) |
| 10 | [Prasanta Sadhukhan](prasanta-sadhukhan.md) | Oracle | 55+ | Desktop | [详情](prasanta-sadhukhan.md) |
| 11 | Sergey Bylokhov | Oracle | 50+ | Desktop | - |
| 12 | [Brian Burkhalter](brian-burkhalter.md) | Oracle | 50+ | NIO | [详情](brian-burkhalter.md) |
| 13 | [David Holmes](david-holmes.md) | Oracle | 48+ | Threading | [详情](david-holmes.md) |
| 14 | [Erik Gahlin](erik-gahlin.md) | Oracle | 45+ | JFR | [详情](erik-gahlin.md) |
| 15 | [Jan Lahoda](jan-lahoda.md) | Oracle | 42+ | javac | [详情](jan-lahoda.md) |
| 16 | [Emanuel Peter](emanuel-peter.md) | Oracle | 40+ | C2 Compiler | [详情](emanuel-peter.md) |
| 17 | [Daniel Fuchs](daniel-fuchs.md) | Oracle | 40+ | HTTP Client | [详情](daniel-fuchs.md) |
| 18 | [Justin Lu](justin-lu.md) | Oracle | 38+ | Localization | [详情](justin-lu.md) |
| 19 | [Naoto Sato](naoto-sato.md) | Oracle | 35+ | i18n | [详情](naoto-sato.md) |
| 20 | [Leonid Mesnik](leonid-mesnik.md) | Oracle | 32+ | JVMTI | [详情](leonid-mesnik.md) |
| 21 | [Coleen Phillimore](coleen-phillimore.md) | Oracle | 30+ | HotSpot | [详情](coleen-phillimore.md) |
| 22 | [Claes Redestad](claes-redestad.md) | Oracle | 28+ | Performance | [详情](claes-redestad.md) |
| 23 | [Magnus Ihse Bursie](magnus-ihse-bursie.md) | Oracle | 25+ | Build | [详情](magnus-ihse-bursie.md) |
| 24 | [William Kemper](william-kemper.md) | Amazon | 25+ | Shenandoah | [详情](william-kemper.md) |
| 25 | [Chen Liang](chen-liang.md) | Oracle | 25+ | ClassFile API | [详情](chen-liang.md) |
| 26 | [Volkan Yazici](volkan-yazici.md) | Oracle | 22+ | HTTP Client | [详情](volkan-yazici.md) |
| 27 | [Fei Yang](fei-yang.md) | Huawei | 20+ | RISC-V | [详情](fei-yang.md) |
| 28 | Yasumasa Suenaga | NTT DATA | 18+ | Serviceability | - |
| 29 | [Hamlin Li](hamlin-li.md) | Oracle | 18+ | RISC-V | [详情](hamlin-li.md) |
| 30 | [Shaojin Wen](shaojin-wen.md) | Alibaba | 15+ | Core Libs | [详情](shaojin-wen.md) |
| 31 | [Anjian Wen](anjian-wen.md) | ByteDance | 12+ | RISC-V | [详情](anjian-wen.md) |
| 32 | [Roman Kennke](roman-kennke.md) | Datadog | 12+ | Shenandoah | [详情](roman-kennke.md) |
| 33 | [Johannes Bechberger](johannes-bechberger.md) | SAP | 12+ | JFR | [详情](johannes-bechberger.md) |
| 34 | [Per Minborg](per-minborg.md) | Oracle | 10+ | Core Libs | [详情](per-minborg.md) |
| 35 | [Jatin Bhateja](jatin-bhateja.md) | Intel | 10+ | Vector API | [详情](jatin-bhateja.md) |
| 36 | [Roland Westrelin](roland-westrelin.md) | Red Hat | 10+ | C2 Compiler | [详情](roland-westrelin.md) |
| 37 | [Weijun Wang](weijun-wang.md) | Oracle | 10+ | Security | [详情](weijun-wang.md) |
| 38 | [Alexey Semenyuk](alexey-semenyuk.md) | Oracle | 8+ | jpackage | [详情](alexey-semenyuk.md) |
| 39 | [Alan Bateman](alan-bateman.md) | Oracle | 8+ | Concurrency | [详情](alan-bateman.md) |
| 40 | [Andrew Haley](andrew-haley.md) | Red Hat | 8+ | RISC-V | [详情](andrew-haley.md) |
| 41 | [Doug Simon](doug-simon.md) | Oracle Labs | 8+ | Graal | [详情](doug-simon.md) |
| 42 | [Christian Hagedorn](christian-hagedorn.md) | Oracle Labs | 8+ | Graal | [详情](christian-hagedorn.md) |
| 43 | [Yude Lin](yude-lin.md) | Alibaba | 6+ | Compiler | [详情](yude-lin.md) |
| 44 | [Xiaowei Lu](xiaowei-lu.md) | Alibaba | 6+ | ZGC | [详情](xiaowei-lu.md) |
| 45 | [Kuai Wei](kuai-wei.md) | Alibaba | 5+ | Compiler | [详情](kuai-wei.md) |
| 46 | [Tongbao Zhang](tongbao-zhang.md) | Alibaba | 5+ | Testing | [详情](tongbao-zhang.md) |
| 47 | [Han GQ](han-gq.md) | Alibaba | 4+ | Core | [详情](han-gq.md) |
| 48 | [Francesco Andreuzzi](francesco-andreuzzi.md) | Oracle | 4+ | Testing | [详情](francesco-andreuzzi.md) |
| 49 | [Stefan Karlsson](stefan-karlsson.md) | Oracle | 4+ | ZGC | [详情](stefan-karlsson.md) |
| 50 | [Vladimir Kozlov](vladimir-kozlov.md) | Oracle | 4+ | C2 Compiler | [详情](vladimir-kozlov.md) |

> **Note**: PR counts are approximate. Data based on GitHub Integrated PRs with `label:integrated`.

---

## 3. By Organization

| Organization | Contributors | PRs | Share |
|--------------|--------------|-----|-------|
| **Oracle** | 280+ | 3,300+ | 70%+ |
| **Red Hat** | 40+ | 450+ | 10% |
| **SAP** | 25+ | 220+ | 5% |
| **Amazon** | 20+ | 180+ | 4% |
| **Alibaba** | 10+ | 80+ | 2% |
| **IBM** | 15+ | 140+ | 3% |
| **Others** | 50+ | 350+ | 6% |

---

## 4. By Component

| Component | Top Contributors | PRs |
|-----------|------------------|-----|
| **GC** | Thomas Schatzl, Albert Yang, William Kemper | 700+ |
| **Compiler** | Emanuel Peter, Roland Westrelin, Jatin Bhateja | 380+ |
| **Core Libs** | Claes Redestad, Brian Burkhalter | 550+ |
| **Build** | Matthias Baesken, Magnus Ihse Bursie | 280+ |
| **JFR** | Erik Gahlin | 120+ |
| **Desktop** | Phil Race, Prasanta Sadhukhan | 240+ |
| **Network** | Daniel Fuchs, Volkan Yazici | 180+ |
| **Security** | Weijun Wang, Sean Mullan | 140+ |

---

## 5. Key Features in JDK 21

| JEP | Feature | Lead Contributors |
|-----|---------|-------------------|
| JEP 444 | Virtual Threads | Ron Pressler, Alan Bateman |
| JEP 440 | Pattern Matching for switch | Gavin Bierman, Brian Goetz |
| JEP 439 | Generational ZGC | Stefan Karlsson, Albert Yang |
| JEP 445 | Unnamed Classes (Preview) | Gavin Bierman |
| JEP 446 | Unnamed Variables (Preview) | Gavin Bierman |
| JEP 442 | Foreign Function & Memory (Preview) | Maurizio Cimadamore |

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
- [JDK 25 Top Contributors](jdk25-top-contributors.md)
- [JDK 17 Top Contributors](jdk17-top-contributors.md)
- [All Contributors](/by-contributor/)
- [By Organization](/contributors/stats/by-org.md)
