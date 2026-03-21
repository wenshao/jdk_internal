# JDK 21 Top Contributors

> JDK 21 (LTS) - Released September 2023

---
## 目录

1. [Overview](#1-overview)
2. [Project Leadership](#2-project-leadership)
3. [Top Contributors](#3-top-contributors)
4. [By Organization](#4-by-organization)
5. [Key Features in JDK 21](#5-key-features-in-jdk-21)
6. [JDK 21u Update Project](#6-jdk-21u-update-project)
7. [Distributions Based on JDK 21](#7-distributions-based-on-jdk-21)
8. [Migration Notes](#8-migration-notes)
9. [References](#9-references)

---

## 1. Overview

JDK 21 is the third Long-Term Support (LTS) release under the six-month release cadence. Released in September 2023, it introduces Virtual Threads (Project Loom), Pattern Matching for switch, and Record Patterns.

**Key Statistics:**
- **Release Date**: September 19, 2023
- **LTS Support**: Until September 2031 (Oracle) / 2033 (OpenJDK)
- **JEPs Delivered**: 15 JEPs
- **Notable**: Virtual Threads, Pattern Matching, Sequenced Collections

---

## 2. Project Leadership

| Role | Name | Organization |
|------|------|--------------|
| **Release Manager** | [Alan Bateman](./alan-bateman.md) | Oracle |
| **Build Lead** | [Magnus Ihse Bursie](./magnus-ihse-bursie.md) | Oracle |
| **Quality Lead** | [Joe Darcy](./joe-darcy.md) | Oracle |

---

## 3. Top Contributors

### Virtual Threads (Project Loom)

| Contributor | Organization | Focus |
|-------------|--------------|-------|
| [Brian Goetz](./brian-goetz.md) | Oracle | Architecture, Design |
| [Ron Pressler](./ron-pressler.md) | Oracle | Virtual Threads Lead |
| [Alan Bateman](./alan-bateman.md) | Oracle | Runtime Integration |
| [David Holmes](./david-holmes.md) | Oracle | Threading |

### Pattern Matching

| Contributor | Organization | Focus |
|-------------|--------------|-------|
| [Brian Goetz](./brian-goetz.md) | Oracle | Design |
| [Vicente Romero](./vicente-romero.md) | Oracle | javac Implementation |
| [Jan Lahoda](./jan-lahoda.md) | Oracle | Pattern Matching |

### Sequenced Collections

| Contributor | Organization | Focus |
|-------------|--------------|-------|
| [Stuart Marks](./stuart-marks.md) | Oracle | Collections |

### GC & Performance

| Contributor | Organization | Focus |
|-------------|--------------|-------|
| [Per Liden](./per-liden.md) | Oracle | ZGC Lead |
| [Stefan Karlsson](./stefan-karlsson.md) | Oracle | ZGC |
| [Roman Kennke](./roman-kennke.md) | Red Hat | Shenandoah GC |
| [Aleksey Shipilev](./aleksey-shipilev.md) | Amazon | Performance |

### Foreign Function & Memory API

| Contributor | Organization | Focus |
|-------------|--------------|-------|
| [Maurizio Cimadamore](./maurizio-cimadamore.md) | Oracle | Foreign API Lead |
| [Jorn Vernee](./jorn-vernee.md) | Oracle | Foreign API |

### Compiler & Runtime

| Contributor | Organization | Focus |
|-------------|--------------|-------|
| [Vladimir Kozlov](./vladimir-kozlov.md) | Oracle | C2 Compiler |
| [Tobias Hartmann](./tobias-hartmann.md) | Oracle | JIT Compiler |
| [Coleen Phillimore](./coleen-phillimore.md) | Oracle | HotSpot |
| [Ioi Lam](./ioi-lam.md) | Oracle | CDS, AOT |

### Security

| Contributor | Organization | Focus |
|-------------|--------------|-------|
| [Sean Mullan](./sean-mullan.md) | Oracle | Security |
| [Weijun Wang](./weijun-wang.md) | Oracle | Security |
| [Xuelei Fan](./xuelei-fan.md) | Oracle | TLS |

### RISC-V Port

| Contributor | Organization | Focus |
|-------------|--------------|-------|
| [Fei Yang](./fei-yang.md) | ISCAS | RISC-V Port Lead |
| [Hamlin Li](./hamlin-li.md) | Rivos | RISC-V Vectors |

---

## 4. By Organization

### Oracle

Primary developer of JDK 21 features.

| Contributor | Focus |
|-------------|-------|
| [Brian Goetz](./brian-goetz.md) | Virtual Threads Architecture |
| [Ron Pressler](./ron-pressler.md) | Virtual Threads Lead |
| [Maurizio Cimadamore](./maurizio-cimadamore.md) | Foreign API |
| [Per Liden](./per-liden.md) | ZGC |

### Red Hat

GC, runtime, and platform contributions.

| Contributor | Focus |
|-------------|-------|
| [Roman Kennke](./roman-kennke.md) | Shenandoah GC |
| [Andrew Dinn](./andrew-dinn.md) | AArch64 |

### Amazon (Corretto)

Performance and Shenandoah GC.

| Contributor | Focus |
|-------------|-------|
| [Aleksey Shipilev](./aleksey-shipilev.md) | Shenandoah, Performance |

### ISCAS / PLCT Lab

RISC-V platform support.

| Contributor | Focus |
|-------------|-------|
| [Fei Yang](./fei-yang.md) | RISC-V Port Lead |
| Dingli Zhang | RISC-V Testing |

### Rivos

RISC-V vector support.

| Contributor | Focus |
|-------------|-------|
| [Hamlin Li](./hamlin-li.md) | RISC-V Vectors |

### Alibaba (Dragonwell)

China market distribution.

| Contributor | Focus |
|-------------|-------|
| [Shaojin Wen](./shaojin-wen.md) | Core Libraries |

### ByteDance

RISC-V contributions.

| Contributor | Focus |
|-------------|-------|
| [Anjian Wen](./anjian-wen.md) | RISC-V Zvbb/Zfa |

---

## 5. Key Features in JDK 21

### JEPs Delivered

| JEP | Title | Status | Lead(s) |
|-----|-------|--------|---------|
| JEP 430 | String Templates (Preview) | Preview | Jim Laskey |
| JEP 431 | Sequenced Collections | Final | Stuart Marks |
| JEP 439 | Generational ZGC | Final | Per Liden |
| JEP 440 | Record Patterns | Final | Vicente Romero |
| JEP 441 | Pattern Matching for switch | Final | Brian Goetz |
| JEP 442 | Foreign Function & Memory API (Third Preview) | Preview | Maurizio Cimadamore |
| JEP 443 | Unnamed Patterns and Variables (Preview) | Preview | Brian Goetz |
| JEP 444 | Virtual Threads | Final | Ron Pressler |
| JEP 445 | Unnamed Classes and Instance Main Methods (Preview) | Preview |  |
| JEP 446 | Scoped Values (Preview) | Preview | Ron Pressler |
| JEP 448 | Vector API (Sixth Incubator) | Incubator |  |
| JEP 449 | Deprecate the Windows 32-bit x86 Port for Removal | Deprecate |  |
| JEP 451 | Prepare to Disallow the Dynamic Loading of Agents |  |  |
| JEP 452 | Key Encapsulation Mechanism API | Final |  |
| JEP 453 | Structured Concurrency (Preview) | Preview | Ron Pressler |

### Key Highlights

- **Virtual Threads** - Lightweight threads for high-throughput applications
- **Sequenced Collections** - New collection interfaces with defined order
- **Record Patterns** - Deconstruction patterns for records
- **Pattern Matching for switch** - Final feature
- **Generational ZGC** - Generational mode for ZGC
- **Foreign Function & Memory API** - Modern native interop

---

## 6. JDK 21u Update Project

The **jdk21u** project maintains OpenJDK 21 with security updates and bug fixes.

### Current Maintainers

| Role | Name | Organization |
|------|------|--------------|
| Project Lead |  |  |
| Build Lead | [Magnus Ihse Bursie](./magnus-ihse-bursie.md) | Oracle |

### Update Cadence

- **Security Updates**: Quarterly (CPU)
- **Bug Fixes**: Ongoing
- **Ports**: AArch64, ARM, x86-64, PPC64, s390x, RISC-V, LoongArch

---

## 7. Distributions Based on JDK 21

| Distribution | Organization | Status |
|--------------|--------------|--------|
| Oracle JDK 21 | Oracle | LTS until 2031 |
| OpenJDK 21u | OpenJDK Community | Active |
| Amazon Corretto 21 | Amazon | LTS until 2032+ |
| Azul Zulu 21 | Azul Systems | Active |
| Eclipse Temurin 21 | Eclipse Foundation | Active |
| Alibaba Dragonwell 21 | Alibaba | China-focused |
| SAP SapMachine 21 | SAP | Enterprise |
| Microsoft Build of OpenJDK 21 | Microsoft | Active |
| IBM Semeru 21 | IBM | Active |
| Azul Prime 21 | Azul Systems | Enterprise |

---

## 8. Migration Notes

### From JDK 17 to JDK 21

1. **Virtual Threads**: Evaluate for I/O-bound workloads
2. **Sequenced Collections**: Update collection usage patterns
3. **Pattern Matching**: Simplify switch statements
4. **Generational ZGC**: Enable for better GC performance

### From JDK 11 to JDK 21

Major upgrade with significant benefits:
1. **Virtual Threads**: Revolutionary for concurrent applications
2. **Foreign Function API**: Modern native interop
3. **Pattern Matching**: Cleaner code patterns
4. **Performance**: Major improvements across all components

### From JDK 8 to JDK 21

Complete platform modernization:
1. **Module System**: Ensure proper module configuration
2. **Virtual Threads**: Massive improvement for concurrent code
3. **Security Manager**: Removed/Deprecated
4. **Performance**: 2-3x improvement in many workloads

### Migration Resources

- [JDK 21 Migration Guide](https://docs.oracle.com/en/java/javase/21/migrate/)
- [Virtual Threads Guide](https://openjdk.org/jeps/444)
- [Oracle JDK 21 Documentation](https://docs.oracle.com/en/java/javase/21/)

---

## 9. References

- [JDK 21 Release Notes](https://openjdk.org/projects/jdk/21/)
- [JDK 21 JEPs](https://openjdk.org/projects/jdk/21/specifications)
- [OpenJDK 21u Project](https://openjdk.org/projects/jdk21u/)
- [Project Loom](https://openjdk.org/projects/loom/)

---

*Last updated: 2026-03-21*
