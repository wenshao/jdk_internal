# JDK 11 Top Contributors

> JDK 11 (LTS) - Released September 2018

---
## 目录

1. [Overview](#1-overview)
2. [Project Leadership](#2-project-leadership)
3. [Top Contributors](#3-top-contributors)
4. [By Organization](#4-by-organization)
5. [Key Features in JDK 11](#5-key-features-in-jdk-11)
6. [JDK 11u Update Project](#6-jdk-11u-update-project)
7. [Distributions Based on JDK 11](#7-distributions-based-on-jdk-11)
8. [Migration Notes](#8-migration-notes)
9. [References](#9-references)

---

## 1. Overview

JDK 11 was the first Long-Term Support (LTS) release after the new six-month release cadence was adopted. It was released in September 2018 and remains widely used in enterprise environments.

**Key Statistics:**
- **Release Date**: September 25, 2018
- **LTS Support**: Until September 2026 (Oracle) / 2032 (OpenJDK)
- **JEPs Delivered**: 17 JEPs
- **Notable**: First LTS under new release model

---

## 2. Project Leadership

| Role | Name | Organization |
|------|------|--------------|
| **Release Manager** | Alan Bateman | Oracle |
| **Build Lead** | Magnus Ihse Bursie | Oracle |
| **Quality Lead** | Joe Darcy | Oracle |

---

## 3. Top Contributors

### Core Development Team

| Contributor | Organization | Focus |
|-------------|--------------|-------|
| [Alan Bateman](./alan-bateman.md) | Oracle | Module System, Release Management |
| [Mandy Chung](./mandy-chung.md) | Oracle | Module System |
| [Alex Buckley](./alex-buckley.md) | Oracle | Language Specification |
| [Brian Goetz](./brian-goetz.md) | Oracle | Language Design |
| [Mark Reinhold](./mark-reinhold.md) | Oracle | Chief Architect |
| [Stuart Marks](./stuart-marks.md) | Oracle | Core Libraries |

### Performance & GC

| Contributor | Organization | Focus |
|-------------|--------------|-------|
| [Aleksey Shipilev](./aleksey-shipilev.md) | Amazon | Performance, Epsilon GC |
| [Roman Kennke](./roman-kennke.md) | Red Hat | Shenandoah GC |
| [Per Liden](./per-liden.md) | Oracle | ZGC |
| [Stefan Karlsson](./stefan-karlsson.md) | Oracle | ZGC |

### Security & Crypto

| Contributor | Organization | Focus |
|-------------|--------------|-------|
| [Sean Mullan](./sean-mullan.md) | Oracle | Security |
| [Valerie Peng](./valerie-peng.md) | Oracle | Crypto |
| [Xuelei Fan](./xuelei-fan.md) | Oracle | TLS, Crypto |

### Compiler & Runtime

| Contributor | Organization | Focus |
|-------------|--------------|-------|
| [Vladimir Kozlov](./vladimir-kozlov.md) | Oracle | C2 Compiler |
| [Tobias Hartmann](./tobias-hartmann.md) | Oracle | JIT Compiler |
| [Coleen Phillimore](./coleen-phillimore.md) | Oracle | HotSpot |
| [David Holmes](./david-holmes.md) | Oracle | Threading |

---

## 4. By Organization

### Oracle

Primary developer of JDK 11 features.

| Contributor | Focus |
|-------------|-------|
| [Alan Bateman](./alan-bateman.md) | Module System |
| [Mandy Chung](./mandy-chung.md) | Module System |
| [Per Liden](./per-liden.md) | ZGC |
| [Sean Mullan](./sean-mullan.md) | Security |

### Red Hat

Major contributor to GC and runtime.

| Contributor | Focus |
|-------------|-------|
| [Roman Kennke](./roman-kennke.md) | Shenandoah GC |
| [Andrew Dinn](./andrew-dinn.md) | AArch64 |
| Andrew Haley | Zero VM |

### Amazon (Corretto)

| Contributor | Focus |
|-------------|-------|
| [Aleksey Shipilev](./aleksey-shipilev.md) | Performance |

### SAP

| Contributor | Focus |
|-------------|-------|
| Volker Simonis | Build, Ports |
| [Matthias Baesken](./matthias-baesken.md) | Build |

### Alibaba (Dragonwell)

| Contributor | Focus |
|-------------|-------|
| [Shaojin Wen](./shaojin-wen.md) | Core Libraries |

---

## 5. Key Features in JDK 11

### JEPs Delivered

| JEP | Title | Lead(s) |
|-----|-------|---------|
| JEP 181 | Nest-Based Access Control |  |
| JEP 309 | Dynamic Class-File Constants | John Rose |
| JEP 315 | Improve AArch64 Intrinsics |  |
| JEP 318 | Epsilon: A No-Op Garbage Collector | Aleksey Shipilev |
| JEP 320 | Remove the Java EE and CORBA Modules |  |
| JEP 321 | HTTP Client (Standard) |  |
| JEP 323 | Local-Variable Syntax for Lambda Parameters | Alex Buckley |
| JEP 324 | Key Agreement with Curve25519 and Curve448 |  |
| JEP 327 | Unicode 10 |  |
| JEP 328 | Flight Recorder | Erik Gahlin |
| JEP 329 | ChaCha20 and Poly1305 Cryptographic Algorithms |  |
| JEP 330 | Launch Single-File Source-Code Programs |  |
| JEP 331 | Low-Overhead Heap Profiling |  |
| JEP 332 | Transport Layer Security (TLS) 1.3 | Xuelei Fan |
| JEP 333 | ZGC: A Scalable Low-Latency Garbage Collector (Experimental) | Per Liden |
| JEP 335 | Deprecate Nashorn JavaScript Engine |  |
| JEP 336 | Deprecate Pack200 Tools and API |  |

### Key Highlights

- **ZGC** - New scalable low-latency garbage collector
- **Epsilon GC** - No-op GC for performance testing
- **HTTP Client** - Modern HTTP client (incubating since JDK 9)
- **Flight Recorder** - Low-overhead profiling framework
- **TLS 1.3** - Modern encryption support
- **Single-File Source Programs** - `java HelloWorld.java`

---

## 6. JDK 11u Update Project

The **jdk11u** project maintains OpenJDK 11 with security updates and bug fixes.

### Current Maintainers

| Role | Name | Organization |
|------|------|--------------|
| Project Lead |  |  |
| Build Lead | [Magnus Ihse Bursie](./magnus-ihse-bursie.md) | Oracle |

### Update Cadence

- **Security Updates**: Quarterly (CPU)
- **Bug Fixes**: Ongoing
- **Ports**: AArch64, ARM, x86-64, PPC64, s390x

---

## 7. Distributions Based on JDK 11

| Distribution | Organization | Status |
|--------------|--------------|--------|
| Oracle JDK 11 | Oracle | LTS until 2026 |
| OpenJDK 11u | OpenJDK Community | Active |
| Amazon Corretto 11 | Amazon | LTS until 2027+ |
| Azul Zulu 11 | Azul Systems | Active |
| Eclipse Temurin 11 | Eclipse Foundation | Active |
| Alibaba Dragonwell 11 | Alibaba | China-focused |
| SAP SapMachine 11 | SAP | Enterprise |
| Microsoft Build of OpenJDK 11 | Microsoft | Active |
| IBM Semeru 11 | IBM | Active |

---

## 8. Migration Notes

### From JDK 8 to JDK 11

1. **Java EE Modules Removed**: JAXB, JAX-WS need separate dependencies
2. **Security Manager**: Deprecation warnings
3. **Performance**: Significant improvements in G1 GC
4. **Container Awareness**: Better Docker support

### Migration Resources

- [JDK 11 Migration Guide](https://docs.oracle.com/en/java/javase/11/migrate/)
- [Oracle JDK 11 Documentation](https://docs.oracle.com/en/java/javase/11/)

---

## 9. References

- [JDK 11 Release Notes](https://openjdk.org/projects/jdk/11/)
- [JDK 11 JEPs](https://openjdk.org/projects/jdk/11/specifications)
- [OpenJDK 11u Project](https://openjdk.org/projects/jdk11u/)

---

*Last updated: 2026-03-21*
