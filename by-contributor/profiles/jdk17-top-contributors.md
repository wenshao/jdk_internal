# JDK 17 Top Contributors

> JDK 17 (LTS) - Released September 2021

---
## 目录

1. [Overview](#1-overview)
2. [Project Leadership](#2-project-leadership)
3. [Top Contributors](#3-top-contributors)
4. [By Organization](#4-by-organization)
5. [Key Features in JDK 17](#5-key-features-in-jdk-17)
6. [JDK 17u Update Project](#6-jdk-17u-update-project)
7. [Distributions Based on JDK 17](#7-distributions-based-on-jdk-17)
8. [Migration Notes](#8-migration-notes)
9. [References](#9-references)

---

## 1. Overview

JDK 17 is the second Long-Term Support (LTS) release under the new six-month release cadence. Released in September 2021, it introduces significant language enhancements including Sealed Classes and Pattern Matching.

**Key Statistics:**
- **Release Date**: September 14, 2021
- **LTS Support**: Until September 2029 (Oracle) / 2031 (OpenJDK)
- **JEPs Delivered**: 14 JEPs
- **Notable**: Sealed Classes, macOS/AArch64, ZGC Improvements

---

## 2. Project Leadership

| Role | Name | Organization |
|------|------|--------------|
| **Release Manager** | [Alan Bateman](./alan-bateman.md) | Oracle |
| **Build Lead** | [Magnus Ihse Bursie](./magnus-ihse-bursie.md) | Oracle |
| **Quality Lead** | [Joe Darcy](./joe-darcy.md) | Oracle |

---

## 3. Top Contributors

### Language Features

| Contributor | Organization | Focus |
|-------------|--------------|-------|
| [Brian Goetz](./brian-goetz.md) | Oracle | Sealed Classes, Pattern Matching |
| [Alex Buckley](./alex-buckley.md) | Oracle | Language Specification |
| [Vicente Romero](./vicente-romero.md) | Oracle | Sealed Classes, Records |
| [Jan Lahoda](./jan-lahoda.md) | Oracle | Pattern Matching, javac |

### GC & Performance

| Contributor | Organization | Focus |
|-------------|--------------|-------|
| [Per Liden](./per-liden.md) | Oracle | ZGC Lead |
| [Stefan Karlsson](./stefan-karlsson.md) | Oracle | ZGC |
| [Roman Kennke](./roman-kennke.md) | Red Hat (当时) | Shenandoah GC |
| [Aleksey Shipilev](./aleksey-shipilev.md) | Amazon | Shenandoah, Performance |

### macOS/AArch64 Port

| Contributor | Organization | Focus |
|-------------|--------------|-------|
| [Nick Gasson](./nick-gasson.md) | - | macOS/AArch64 Port |
| Andrew Dinn | Red Hat | AArch64 |

### Compiler & Runtime

| Contributor | Organization | Focus |
|-------------|--------------|-------|
| [Vladimir Kozlov](./vladimir-kozlov.md) | Oracle | C2 Compiler |
| [Tobias Hartmann](./tobias-hartmann.md) | Oracle | JIT Compiler |
| [Coleen Phillimore](./coleen-phillimore.md) | Oracle | HotSpot |
| [David Holmes](./david-holmes.md) | Oracle | Threading |

### Security

| Contributor | Organization | Focus |
|-------------|--------------|-------|
| [Sean Mullan](./sean-mullan.md) | Oracle | Security |
| [Valerie Peng](./valerie-peng.md) | Oracle | Crypto |
| [Weijun Wang](./weijun-wang.md) | Oracle | Security |

---

## 4. By Organization

### Oracle

Primary developer of JDK 17 features.

| Contributor | Focus |
|-------------|-------|
| [Brian Goetz](./brian-goetz.md) | Language Architecture |
| [Per Liden](./per-liden.md) | ZGC |
| [Vicente Romero](./vicente-romero.md) | Sealed Classes |
| [Nick Gasson](./nick-gasson.md) | macOS/AArch64 |

### Red Hat

Major contributor to Shenandoah GC and Linux ports.

| Contributor | Focus |
|-------------|-------|
| [Roman Kennke](./roman-kennke.md) | Shenandoah GC |
| Andrew Dinn | AArch64 |

### Amazon (Corretto)

Shenandoah GC maintenance and optimization.

| Contributor | Focus |
|-------------|-------|
| [Aleksey Shipilev](./aleksey-shipilev.md) | Shenandoah, Performance |

### SAP

Enterprise Java contributions.

| Contributor | Focus |
|-------------|-------|
| [Volker Simonis](./matthias-baesken.md) | Build, x86_64 |
| [Matthias Baesken](./matthias-baesken.md) | Build, Ports |

### Alibaba (Dragonwell)

China market distribution.

| Contributor | Focus |
|-------------|-------|
| [Shaojin Wen](./shaojin-wen.md) | Core Libraries |

---

## 5. Key Features in JDK 17

### JEPs Delivered

| JEP | Title | Lead(s) |
|-----|-------|---------|
| JEP 306 | Restore Always-Strict Floating-Point Semantics | Joe Darcy |
| JEP 356 | Enhanced Pseudo-Random Number Generators |  |
| JEP 382 | New macOS Rendering Pipeline |  |
| JEP 391 | macOS/AArch64 Port | Nick Gasson |
| JEP 398 | Deprecate the Applet API for Removal |  |
| JEP 403 | Strongly Encapsulate JDK Internals | Alan Bateman |
| JEP 406 | Pattern Matching for switch (Preview) | Brian Goetz |
| JEP 407 | Remove RMI Activation |  |
| JEP 409 | Sealed Classes | Vicente Romero |
| JEP 410 | Remove the Experimental AOT and JIT Compiler |  |
| JEP 411 | Deprecate the Security Manager for Removal |  |
| JEP 412 | Foreign Function & Memory API (Incubator) |  |
| JEP 414 | Vector API (Second Incubator) |  |
| JEP 415 | Context-Specific Deserialization Filters |  |

### Key Highlights

- **Sealed Classes** - Finalization of sealed classes feature
- **macOS/AArch64** - Native Apple Silicon support
- **ZGC Improvements** - Improved performance and scalability
- **Strong Encapsulation** - JDK internals strongly encapsulated
- **Security Manager Deprecation** - Marked for removal

---

## 6. JDK 17u Update Project

The **jdk17u** project maintains OpenJDK 17 with security updates and bug fixes.

### Current Maintainers

| Role | Name | Organization |
|------|------|--------------|
| Project Lead |  |  |
| Build Lead | [Magnus Ihse Bursie](./magnus-ihse-bursie.md) | Oracle |

### Update Cadence

- **Security Updates**: Quarterly (CPU)
- **Bug Fixes**: Ongoing
- **Ports**: AArch64, ARM, x86-64, PPC64, s390x, macOS/AArch64

---

## 7. Distributions Based on JDK 17

| Distribution | Organization | Status |
|--------------|--------------|--------|
| Oracle JDK 17 | Oracle | LTS until 2029 |
| OpenJDK 17u | OpenJDK Community | Active |
| Amazon Corretto 17 | Amazon | LTS until 2030+ |
| Azul Zulu 17 | Azul Systems | Active |
| Eclipse Temurin 17 | Eclipse Foundation | Active |
| Alibaba Dragonwell 17 | Alibaba | China-focused |
| SAP SapMachine 17 | SAP | Enterprise |
| Microsoft Build of OpenJDK 17 | Microsoft | Active |
| IBM Semeru 17 | IBM | Active |
| Azul Prime 17 | Azul Systems | Enterprise |

---

## 8. Migration Notes

### From JDK 11 to JDK 17

1. **Strong Encapsulation**: `--add-opens` may be needed for legacy code
2. **Security Manager**: Deprecated, plan for removal
3. **Applet API**: Deprecated for removal
4. **Performance**: ZGC significantly improved

### From JDK 8 to JDK 17

Major upgrade requiring significant testing:
1. **Java EE Modules**: Use standalone versions
2. **Security Manager**: Deprecated
3. **Nashorn**: Removed
4. **Performance**: Significant improvements across all GCs

### Migration Resources

- [JDK 17 Migration Guide](https://docs.oracle.com/en/java/javase/17/migrate/)
- [Oracle JDK 17 Documentation](https://docs.oracle.com/en/java/javase/17/)

---

## 9. References

- [JDK 17 Release Notes](https://openjdk.org/projects/jdk/17/)
- [JDK 17 JEPs](https://openjdk.org/projects/jdk/17/specifications)
- [OpenJDK 17u Project](https://openjdk.org/projects/jdk17u/)

---

*Last updated: 2026-03-21*
