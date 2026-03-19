# JDK 8 Top Contributors

> JDK 8 (LTS) - OpenJDK 8u Updates Contributors

---

## Overview

JDK 8 was released in March 2014 and remains one of the most widely used Java versions. The OpenJDK 8u project continues to receive updates through the **Adoptium** (formerly AdoptOpenJDK), **Amazon Corretto**, **Azul Zulu**, **Oracle JDK**, and other distributions.

---

## Project Leadership

| Role | Name | Organization |
|------|------|--------------|
| **Project Lead** | Andrew Haley | Red Hat |
| **Release Manager** | Volker Simonis | SAP |
| **Build Lead** | Magnus Ihse Bursie | Oracle |

---

## Historical Top Contributors (2014-2024)

JDK 8 has been maintained by a dedicated community over its 10+ year lifespan.

### Original JDK 8 Team (2014 Release)

| Contributor | Role | Focus |
|-------------|------|-------|
| Brian Goetz | Language Architect | Lambda, Streams |
| Paul Sandoz | Spec Lead | Lambda, Streams API |
| Aleksey Shipilev | Performance | Arrays, String |
| John Rose | JVM Architect | InvokeDynamic |
| Viktor Klang | Library | Concurrency |
| Doug Lea | Library | Concurrency (JSR-166) |

### Long-Term Maintainers (2014-2024)

| Contributor | Organization | Focus | Since |
|-------------|--------------|-------|-------|
| [Volker Simonis](./matthias-baesken.md) | SAP | Build, x86_64 | 2010 |
| [Magnus Ihse Bursie](./magnus-ihse-bursie.md) | Oracle | Build System | 2012 |
| [David Holmes](./david-holmes.md) | Oracle | Threading, Runtime | 2000 |
| [Coleen Phillimore](./coleen-phillimore.md) | Oracle | HotSpot | 2005 |
| [Kim Barrett](./kim-barrett.md) | Oracle/Red Hat | GC, HotSpot | 2005 |
| Andrew Haley | Red Hat | AArch64, Zero | 1999 |
| [Ioi Lam](./ioi-lam.md) | Oracle | CDS, AOT | 2010 |
| [Thomas Schatzl](./thomas-schatzl.md) | Oracle | G1 GC | 2012 |
| [Erik Gahlin](./erik-gahlin.md) | Oracle | JFR | 2013 |

---

## By Organization

### Oracle

JDK 8 was primarily developed by Sun Microsystems (acquired by Oracle in 2010).

| Contributor | Focus | Notes |
|-------------|-------|-------|
| Brian Goetz | Lambda Project Lead | JSR-335 Spec Lead |
| Paul Sandoz | Streams API | JSR-335 Expert |
| [David Holmes](./david-holmes.md) | Threading | JSR-166 |
| [Mike Duigou](./magnus-ihse-bursie.md) | Collections | Lambda integration |
| [Henry Jen](./magnus-ihse-bursie.md) | Core Libraries | I18n |

### Red Hat

Contributed AArch64 port and ongoing maintenance.

| Contributor | Focus |
|-------------|-------|
| Andrew Haley | AArch64 Port Lead |
| Andrew Dinn | AArch64 |
| Nick Gasson | AArch64 |
| [Aleksey Shipilev](./aleksey-shipilev.md) | Performance (later) |

### SAP

Long-term contributors to JDK 8 updates.

| Contributor | Focus | 档案 |
|-------------|-------|------|
| Volker Simonis | Build, x86_64 | - |
| [Matthias Baesken](./matthias-baesken.md) | Build, Ports | [详情](./matthias-baesken.md) |
| Goetz Lindenmaier | HotSpot | - |

### Amazon (Corretto)

Maintains Amazon Corretto 8 distribution.

| Contributor | Focus | 档案 |
|-------------|-------|------|
| Andrew Dinn | AArch64 | [详情](./andrew-dinn.md) |
| Nick Gasson | AArch64 | [详情](./nick-gasson.md) |
| David Beaumont | Compiler | [详情](./david-beaumont.md) |

### Alibaba (Dragonwell)

Maintains Dragonwell 8 distribution for China market.

| Contributor | Focus | 档案 |
|-------------|-------|------|
| [Shaojin Wen](./shaojin-wen.md) | Core Libraries | [详情](./shaojin-wen.md) |
| [Liang Chen](./chen-liang.md) | ClassFile | [详情](./chen-liang.md) |

### Azul Systems (Zulu)

Long-term OpenJDK contributor with Zulu distribution.

| Contributor | Focus |
|-------------|-------|
| Gil Tene | Latency, GC |
| Dinko Srkoc | HotSpot |

---

## Key Features in JDK 8

### JEPs Delivered

| JEP | Title | Lead(s) |
|-----|-------|---------|
| JEP 126 | Lambda Expressions | Brian Goetz |
| JEP 104 | Nashorn JavaScript Engine | Sundararajan Athijegannathan |
| JEP 150 | Date-Time API | Stephen Colebourne |
| JEP 122 | Remove Permanent Generation | Jon Masamitsu |
| JEP 160 | Lambda Form | John Rose |
| JEP 161 | Compact Strings | Aleksey Shipilev |
| JEP 178 | Statically-Linked JNI | - |
| JEP 180 | Treat Lazy Fields As Final | Alex Buckley |

### JSR Specifications

| JSR | Title | Spec Lead |
|-----|-------|-----------|
| JSR-335 | Lambda Expressions | Brian Goetz |
| JSR-310 | Date-Time API | Stephen Colebourne |
| JSR-337 | Java SE 8 | Alex Buckley |

---

## JDK 8u Update Project

The **jdk8u** project maintains OpenJDK 8 with security updates and bug fixes.

### Current Maintainers (2024+)

| Role | Name | Organization |
|------|------|--------------|
| Project Lead | Andrew Haley | Red Hat |
| Reviewers | 15+ | Multiple |
| Committers | 50+ | Multiple |

### Update Cadence

- **Security Updates**: Quarterly (CPU)
- **Bug Fixes**: Ongoing
- **Ports**: AArch64, ARM, RISC-V, x86-64

---

## Legacy Contributors

Many contributors who worked on JDK 8 have since moved to other projects or retired:

| Contributor | Contribution | Era |
|-------------|--------------|-----|
| Alex Buckley | JLS, JVMS | 2010-2020 |
| Joe Darcy | javac | 2005-2020 |
| Jonathan Gibbons | javadoc, javac | 2000-2023 |
| Karen Kinnear | JVM | 1998-2018 |
| Mandy Chung | Monitoring, Management | 2000-2020 |
| Shirley Chkel | Client Libraries | 2005-2020 |

---

## Distributions Based on JDK 8

| Distribution | Organization | Status |
|--------------|--------------|--------|
| Oracle JDK | Oracle | LTS until 2030 |
| OpenJDK 8u | OpenJDK Community | Active |
| Amazon Corretto 8 | Amazon | LTS until 2026+ |
| Azul Zulu 8 | Azul Systems | Active |
| Eclipse Temurin 8 | Eclipse Foundation | Active |
| Alibaba Dragonwell 8 | Alibaba | China-focused |
| SAP SapMachine 8 | SAP | Enterprise |
| Microsoft Build of OpenJDK 8 | Microsoft | Active |
| IBM Semeru 8 | IBM | Active |

---

## Migration Notes

### From JDK 8 to JDK 11/17/21

Organizations still on JDK 8 should consider:

1. **Security Updates**: Oracle JDK 8 public updates ended in 2019
2. **Performance**: Newer JDKs have significant improvements
3. **Features**: Lambda adoption enables newer features
4. **Support**: Consider OpenJDK distributions for continued updates

### Migration Resources

- [JDK 8 Migration Guide](https://docs.oracle.com/en/java/javase/11/migrate/)
- [OpenJDK Migration Guide](https://openjdk.org/projects/migration)

---

## Detailed Profiles

For detailed contributor profiles, see:

### JDK 8 Original Authors
- Brian Goetz - Lambda Project Lead
- Paul Sandoz - Streams API Spec Lead
- Aleksey Shipilev - Arrays, String, Performance

### Long-Term Maintainers
- [David Holmes](./david-holmes.md) - Threading
- [Coleen Phillimore](./coleen-phillimore.md) - HotSpot
- [Kim Barrett](./kim-barrett.md) - GC
- [Ioi Lam](./ioi-lam.md) - CDS/AOT
- [Thomas Schatzl](./thomas-schatzl.md) - G1 GC

### Current Maintainers
- [Andrew Haley](./andrew-dinn.md) - AArch64
- [Matthias Baesken](./matthias-baesken.md) - Build System
- [Magnus Ihse Bursie](./magnus-ihse-bursie.md) - Build System

[→ All contributor profiles](./README.md)

---

## References

- [JDK 8 Release Notes](https://openjdk.org/projects/jdk8/)
- [OpenJDK 8u Project](https://openjdk.org/projects/jdk8u/)
- [Lambda Project](https://openjdk.org/projects/lambda/)
- [JSR-335](https://jcp.org/en/jsr/detail?id=335)

---

*Last updated: 2026-03-20*
