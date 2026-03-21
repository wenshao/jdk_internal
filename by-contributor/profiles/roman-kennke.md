# Roman Kennke

> Datadog JVM Engineer | JEP 519 Lead | Shenandoah GC Project Lead | Project Lilliput Lead | Java Champion

---
## 目录

1. [Basic Information](#1-basic-information)
2. [JEP Leadership](#2-jep-leadership)
3. [Contribution Overview](#3-contribution-overview)
4. [Key Contributions](#4-key-contributions)
5. [External Resources](#5-external-resources)

---


## 1. Basic Information

| Attribute | Value |
|-----------|-------|
| **Name** | Roman Kennke |
| **Current Organization** | Datadog |
| **Previous Organizations** | Amazon (Principal Engineer) -> Red Hat (Principal Software Engineer) |
| **Location** | Zurich, Switzerland |
| **GitHub** | [@rkennke](https://github.com/rkennke) |
| **OpenJDK** | [@rkennke](https://openjdk.org/census#rkennke) |
| **Role** | JDK Committer, JDK Reviewer, Java Champion |
| **Primary Areas** | Shenandoah GC, Compact Object Headers, Project Lilliput, AArch64 |
| **Active Since** | 2004+ (GNU Classpath), OpenJDK since 2007+ |

> **数据来源**: [GitHub](https://github.com/rkennke), [OpenJDK Census](https://openjdk.org/census#rkennke), [JEP 519](https://openjdk.org/jeps/519), [Red Hat Developer](https://developers.redhat.com/author/roman-kennke)

---

## 2. JEP Leadership

| JEP | Title | Role | Status | Target |
|-----|------|------|--------|--------|
| [JEP 519](https://openjdk.org/jeps/519) | Compact Object Headers | Lead | Final | JDK 24 |
| [JEP 521](https://openjdk.org/jeps/521) | Generational Shenandoah | Co-contributor | Final | JDK 25 |

---

## 3. Contribution Overview

### JDK 26 Contributions

| Metric | Value |
|--------|-------|
| **Commits** | 30 |
| **Primary Focus** | Compact Object Headers |
| **JEP Lead** | JEP 519: Compact Object Headers |

### Key Areas of Expertise

- **Shenandoah GC**: Project lead of Shenandoah garbage collector
- **Project Lilliput**: Lead of OpenJDK's initiative to minimize object memory overhead
- **Compact Object Headers**: JEP 450 (Experimental, JDK 24) and JEP 519 (Final, JDK 25) lead
- **Memory Layout**: Object memory optimization
- **HotSpot**: JVM runtime improvements

## 4. Key Contributions

### JEP 450/519: Compact Object Headers (Project Lilliput)

Led the implementation of compact object headers, first as JEP 450 (Experimental) in JDK 24, then finalized as JEP 519 in JDK 25. This is the first integrated feature from Project Lilliput:

- Reduced object header size from 12 bytes to 8 bytes
- SPECjbb2015: 22% less heap space, 8% less CPU time
- Garbage collections reduced by 15% with G1 and Parallel collectors
- Highly parallel JSON parser benchmark runs 10% faster
- Coordinated with all GC teams (G1, ZGC, Shenandoah, Parallel)
- Amazon validated across hundreds of production services with backports to JDK 17 and 21

### Shenandoah GC

Project lead of Shenandoah garbage collector (with Christine Flood):

- Generational Shenandoah (JEP 521 co-author)
- Performance optimizations
- Cross-platform support improvements
- Memory management enhancements

### AArch64 Support

Contributions to AArch64 platform support:

- HotSpot runtime improvements
- Platform-specific optimizations
- Testing infrastructure

---

## 5. External Resources

| Type | Link |
|------|------|
| **GitHub** | [@rkennke](https://github.com/rkennke) |
| **OpenJDK Census** | [rkennke](https://openjdk.org/census#rkennke) |
| **Red Hat Developer** | [roman-kennke](https://developers.redhat.com/author/roman-kennke) |
| **JEP 450** | [Compact Object Headers (Experimental)](https://openjdk.org/jeps/450) |
| **JEP 519** | [Compact Object Headers (Final)](https://openjdk.org/jeps/519) |
| **JEP 521** | [Generational Shenandoah](https://openjdk.org/jeps/521) |
| **FOSDEM 2025** | [Speaker](https://archive.fosdem.org/2025/schedule/speaker/roman_kennke/) |

---

> **文档版本**: 3.0
> **最后更新**: 2026-03-22
> **更新内容**:
> - 修正组织: Red Hat -> Datadog (Zurich, Switzerland) (经 GitHub 确认)
> - 添加职业经历: Red Hat -> Amazon (Principal Engineer) -> Datadog
> - 添加 Java Champion 称号
> - 添加 Project Lilliput lead 角色
> - 添加 JEP 450 (Experimental) 参考
> - 添加性能基准数据 (SPECjbb2015)
> - 修正活跃时间: 2004+ (GNU Classpath 起)
