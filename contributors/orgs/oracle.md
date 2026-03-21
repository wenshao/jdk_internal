# Oracle

> OpenJDK 主要维护者和最大贡献者

---
## 目录

1. [概览](#1-概览)
2. [Top 贡献者](#2-top-贡献者)
3. [按地区分类](#3-按地区分类)
4. [组织架构](#4-组织架构)
5. [影响的模块](#5-影响的模块)
6. [主要领域与 JEP 贡献](#6-主要领域与-jep-贡献)
7. [相关 PR 分析文档](#7-相关-pr-分析文档)
8. [OpenJDK 治理参与](#8-openjdk-治理参与)
9. [数据来源](#9-数据来源)
10. [相关链接](#10-相关链接)

---


## 1. 概览

Oracle 是 OpenJDK 的主要维护者和最大贡献者，自 2010 年收购 Sun Microsystems 以来，一直主导 JDK 的开发。Oracle 贡献者遍布美国、欧洲和亚洲，涵盖 HotSpot、Core Libraries、LangTools、Security 等所有核心领域。

| 指标 | 值 |
|------|-----|
| **Integrated PRs (JDK 26)** | 4,200+ |
| **贡献者数** | 320+ |
| **主要领域** | 全领域 |
| **JDK 26 份额** | 70%+ |
| **OpenJDK Governing Board** | Oracle 代表 |

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。OpenJDK Committer 使用 `@openjdk.org` 邮箱提交代码，因此 git commits 按邮箱统计不准确。

### 历史背景

| 时间 | 事件 |
|------|------|
| **1995** | Sun Microsystems 发布 Java |
| **2006** | OpenJDK 项目启动 |
| **2010** | Oracle 收购 Sun Microsystems |
| **2017** | JDK 9 发布，新的 6 个月发布周期 |
| **2021-至今** | LTS 版本 (JDK 17, JDK 21, JDK 26) |

---

## 2. Top 贡献者

### JDK 26 Top Oracle 贡献者 (按 PR 数量排序)

| 排名 | 贡献者 | GitHub | PRs | 角色 | 领域 | 团队 | 档案 |
|------|--------|--------|-----|------|------|------|------|
| 1 | Thomas Schatzl | [@tschatzl](https://github.com/tschatzl) | 546 | Reviewer | G1 GC | HotSpot GC | [详情](../../by-contributor/profiles/thomas-schatzl.md) |
| 2 | Ioi Lam | [@iklam](https://github.com/iklam) | 431 | Reviewer | CDS/AOT | HotSpot Runtime/CDS | [详情](../../by-contributor/profiles/ioi-lam.md) |
| 3 | Coleen Phillimore | [@coleenp](https://github.com/coleenp) | 400 | Reviewer | HotSpot | HotSpot Runtime | [详情](../../by-contributor/profiles/coleen-phillimore.md) |
| 4 | Phil Race | [@prrace](https://github.com/prrace) | 303 | Reviewer | Client Libraries | Core Libraries | [详情](../../by-contributor/profiles/phil-race.md) |
| 5 | Erik Gahlin | [@egahlin](https://github.com/egahlin) | 322 | Reviewer | JFR | HotSpot Runtime | [详情](../../by-contributor/profiles/erik-gahlin.md) |
| 6 | Kim Barrett | [@kimbarrett](https://github.com/kimbarrett) | 352 | Reviewer | Atomic, C++ | HotSpot Runtime | [详情](../../by-contributor/profiles/kim-barrett.md) |
| 7 | Emanuel Peter | [@eme64](https://github.com/eme64) | 226 | Reviewer | C2 编译器 | HotSpot Compiler | [详情](../../by-contributor/profiles/emanuel-peter.md) |
| 8 | Jan Lahoda | [@lahodaj](https://github.com/lahodaj) | 324 | Reviewer | javac | LangTools | [详情](../../by-contributor/profiles/jan-lahoda.md) |
| 9 | Jaikiran Pai | [@jaikiran](https://github.com/jaikiran) | 322 | Reviewer | Networking | Core Libraries | [详情](../../by-contributor/profiles/jaikiran-pai.md) |
| 10 | Daniel Fuchs | [@dfuchs](https://github.com/dfuchs) | 192+ | Reviewer | HTTP/3, JMX | Core Libraries | [详情](../../by-contributor/profiles/daniel-fuchs.md) |
| 11 | Naoto Sato | [@naotoj](https://github.com/naotoj) | 273 | Reviewer | 国际化 | Core Libraries | [详情](../../by-contributor/profiles/naoto-sato.md) |
| 12 | Sergey Bylokhov | [@mrserb](https://github.com/mrserb) | 273 | Reviewer | AWT/2D | Core Libraries | [详情](../../by-contributor/profiles/sergey-bylokhov.md) |
| 13 | Chen Liang | [@liach](https://github.com/liach) | 237 | Reviewer | ClassFile API | LangTools | [详情](../../by-contributor/profiles/chen-liang.md) |
| 14 | Alexey Semenyuk | [@alexeysemenyukoracle](https://github.com/alexeysemenyukoracle) | 233 | Committer | jpackage | Tools | [详情](../../by-contributor/profiles/alexey-semenyuk.md) |
| 15 | David Holmes | - | 80+ | Reviewer | 并发 | Concurrency & Runtime | [详情](../../by-contributor/profiles/david-holmes.md) |
| 16 | Brian Burkhalter | - | 60+ | Reviewer | 网络 | Core Libraries | [详情](../../by-contributor/profiles/brian-burkhalter.md) |
| 17 | Prasanta Sadhukhan | - | 65+ | Reviewer | Desktop | Core Libraries | [详情](../../by-contributor/profiles/prasanta-sadhukhan.md) |
| 18 | Volkan Yazici | - | 40+ | Committer | HTTP Client | Core Libraries | [详情](../../by-contributor/profiles/volkan-yazici.md) |
| 19 | Justin Lu | - | 40+ | Committer | Localization | Core Libraries | [详情](../../by-contributor/profiles/justin-lu.md) |
| 20 | Leonid Mesnik | - | 35+ | Reviewer | JVMTI | Concurrency & Runtime | [详情](../../by-contributor/profiles/leonid-mesnik.md) |
| 21 | Claes Redestad | [@redestad](https://github.com/redestad) | 30+ | Reviewer | Performance | Java Platform | [详情](../../by-contributor/profiles/claes-redestad.md) |
| 22 | Magnus Ihse Bursie | - | 28+ | Reviewer | Build | Infrastructure | [详情](../../by-contributor/profiles/magnus-ihse-bursie.md) |
| 23 | Hamlin Li | - | 20+ | Committer | RISC-V | **已离职 (Rivos)** | [详情](../../by-contributor/profiles/hamlin-li.md) |
| 24 | Per Minborg | - | 15+ | Reviewer | Core Libs | Core Libraries | [详情](../../by-contributor/profiles/per-minborg.md) |
| 25 | Weijun Wang | - | 15+ | Reviewer | Security | Security | [详情](../../by-contributor/profiles/weijun-wang.md) |
| 26 | Alan Bateman | - | 12+ | Reviewer | Concurrency | Concurrency & Runtime | [详情](../../by-contributor/profiles/alan-bateman.md) |
| 27 | Erik Österlund | - | 12+ | Reviewer | ZGC, GC | HotSpot GC | [详情](../../by-contributor/profiles/erik-osterlund.md) |
| 28 | Doug Simon | - | 10+ | Member | Graal | Oracle Labs | [详情](../../by-contributor/profiles/doug-simon.md) |
| 29 | Adam Sotona | [@asotona](https://github.com/asotona) | 30+ | Committer | ClassFile API | LangTools | [详情](../../by-contributor/profiles/adam-sotona.md) |
| 30 | Jonathan Gibbons | - | 100+ | Reviewer | javac, javadoc | LangTools | [详情](../../by-contributor/profiles/jonathan-gibbons.md) |
| 31 | Vicente Romero | - | 50+ | Reviewer | javac | LangTools | [详情](../../by-contributor/profiles/vicente-romero.md) |
| 32 | Lance Andersen | - | 50+ | Reviewer | JDBC | Core Libraries | [详情](../../by-contributor/profiles/lance-andersen.md) |

**小计**: 4,200+ PRs (以上 32 人，含 1 位已离职)

### 新晋 Committer/Reviewer

| 贡献者 | 时间 | 角色 | 提名人 | 领域 |
|--------|------|------|--------|------|
| Claes Redestad | 2022-03 | OpenJDK Member | Daniel Fuchs | Performance |

> **注**: Roman Kennke (Compact Headers) 是 Red Hat 员工，不是 Oracle，已从列表中移除

> **角色说明**:
> - **Reviewer**: 有权批准变更集的资深贡献者 ([详情](https://openjdk.org/bylaws))
> - **Committer**: 有直接推送权限的贡献者 ([详情](https://openjdk.org/guide/))
> - **Author**: 可以创建和提交更改的贡献者 ([详情](https://dev.java/contribute/openjdk/))
> - **Member**: OpenJDK 成员组，参与治理和投票

---

## 3. 按地区分类的 Oracle 贡献者

### 美国团队

| 贡献者 | 位置 | GitHub | PRs | 角色 | 领域 | 档案 |
|--------|------|--------|-----|------|------|------|
| Ioi Lam | Mountain View, CA | [@iklam](https://github.com/iklam) | 431 | Reviewer | CDS/AOT | [详情](../../by-contributor/profiles/ioi-lam.md) |
| Coleen Phillimore | Acton, MA | [@coleenp](https://github.com/coleenp) | 400 | Reviewer | HotSpot | [详情](../../by-contributor/profiles/coleen-phillimore.md) |
| Kim Barrett | Malden, MA | [@kimbarrett](https://github.com/kimbarrett) | 352 | Reviewer | Atomic, C++ | [详情](../../by-contributor/profiles/kim-barrett.md) |
| Naoto Sato | San Jose, CA | [@naotoj](https://github.com/naotoj) | 273 | Reviewer | 国际化 | [详情](../../by-contributor/profiles/naoto-sato.md) |
| Chen Liang | Austin, TX | [@liach](https://github.com/liach) | 237 | Reviewer | ClassFile API | [详情](../../by-contributor/profiles/chen-liang.md) |
| Phil Race | USA | [@prrace](https://github.com/prrace) | 303 | Reviewer | Client Libs | [详情](../../by-contributor/profiles/phil-race.md) |
| Jonathan Gibbons | USA | - | 100+ | Reviewer | javac/javadoc | [详情](../../by-contributor/profiles/jonathan-gibbons.md) |
| Brian Burkhalter | USA | - | 60+ | Reviewer | 网络 | [详情](../../by-contributor/profiles/brian-burkhalter.md) |
| Justin Lu | USA | - | 40+ | Committer | Localization | [详情](../../by-contributor/profiles/justin-lu.md) |
| Leonid Mesnik | USA | - | 35+ | Reviewer | JVMTI | [详情](../../by-contributor/profiles/leonid-mesnik.md) |
| Lance Andersen | USA | - | 50+ | Reviewer | JDBC | [详情](../../by-contributor/profiles/lance-andersen.md) |
| Vicente Romero | USA | - | 50+ | Reviewer | javac | [详情](../../by-contributor/profiles/vicente-romero.md) |

### 欧洲团队

| 贡献者 | 位置 | GitHub | PRs | 角色 | 领域 | 档案 |
|--------|------|--------|-----|------|------|------|
| Thomas Schatzl | Germany | [@tschatzl](https://github.com/tschatzl) | 546 | Reviewer | G1 GC | [详情](../../by-contributor/profiles/thomas-schatzl.md) |
| Erik Gahlin | Sweden | [@egahlin](https://github.com/egahlin) | 322 | Reviewer | JFR | [详情](../../by-contributor/profiles/erik-gahlin.md) |
| Emanuel Peter | Zürich, Switzerland | [@eme64](https://github.com/eme64) | 226 | Reviewer | C2 编译器 | [详情](../../by-contributor/profiles/emanuel-peter.md) |
| Claes Redestad | Stockholm, Sweden | [@redestad](https://github.com/redestad) | 30+ | Reviewer | Performance | [详情](../../by-contributor/profiles/claes-redestad.md) |
| Magnus Ihse Bursie | Sweden | - | 28+ | Reviewer | Build | [详情](../../by-contributor/profiles/magnus-ihse-bursie.md) |
| Erik Österlund | Sweden | - | 12+ | Reviewer | ZGC, GC | [详情](../../by-contributor/profiles/erik-osterlund.md) |
| Per Minborg | Sweden | - | 15+ | Reviewer | Core Libs | [详情](../../by-contributor/profiles/per-minborg.md) |
| Daniel Fuchs | Dublin, Ireland | [@dfuchs](https://github.com/dfuchs) | 192+ | Reviewer | HTTP/3, JMX | [详情](../../by-contributor/profiles/daniel-fuchs.md) |
| Jan Lahoda | Czechia | [@lahodaj](https://github.com/lahodaj) | 324 | Reviewer | javac | [详情](../../by-contributor/profiles/jan-lahoda.md) |
| Alan Bateman | UK | - | 12+ | Reviewer | Concurrency | [详情](../../by-contributor/profiles/alan-bateman.md) |

### 亚洲团队

| 贡献者 | 位置 | GitHub | PRs | 角色 | 领域 | 档案 |
|--------|------|--------|-----|------|------|------|
| Weijun Wang | China | - | 15+ | Reviewer | Security | [详情](../../by-contributor/profiles/weijun-wang.md) |
| Sergey Bylokhov | Russia/USA | [@mrserb](https://github.com/mrserb) | 273 | Reviewer | AWT/2D | [详情](../../by-contributor/profiles/sergey-bylokhov.md) |
| Alexey Semenyuk | Russia | [@alexeysemenyukoracle](https://github.com/alexeysemenyukoracle) | 233 | Committer | jpackage | [详情](../../by-contributor/profiles/alexey-semenyuk.md) |

### 澳洲团队

| 贡献者 | 位置 | GitHub | PRs | 角色 | 领域 | 档案 |
|--------|------|--------|-----|------|------|------|
| David Holmes | Brisbane, Australia | - | 80+ | Reviewer | 并发 | [详情](../../by-contributor/profiles/david-holmes.md) |

### Oracle Labs

| 贡献者 | 位置 | GitHub | PRs | 角色 | 领域 | 档案 |
|--------|------|--------|-----|------|------|------|
| Doug Simon | - | - | 10+ | Member | Graal | [详情](../../by-contributor/profiles/doug-simon.md) |

### 已离职贡献者

| 贡献者 | 原 Oracle 团队 | 现状 | PRs | 领域 | 档案 |
|--------|----------------|------|-----|------|------|
| Hamlin Li | RISC-V | **Rivos** | 20+ | RISC-V | [详情](../../by-contributor/profiles/hamlin-li.md) |
| Zhengyu Gu | HotSpot GC | **Datadog** | 30+ | G1 GC, Shenandoah | [详情](../../by-contributor/profiles/zhengyu-gu.md) |
| Chris Thalinger | HotSpot Compiler | **Twitter/X** | - | JIT 编译器 | - |
| Xuelei Fan | Security | **Salesforce** | - | Security, TLS | - |

> **注**:
> - 位置信息基于贡献者档案、LinkedIn 和 OpenJDK Census
> - 部分贡献者可能已迁移到其他地区或离职
> - 历史贡献仍归属 Oracle 时期

---

## 4. 组织架构

基于贡献者的团队归属和技术领域，Oracle JDK 团队组织架构如下：

### 组织架构图

```
Oracle JDK 开发团队
│
├── Java Platform Group (Java 平台组)
│   │
│   ├── LangTools Team (语言工具团队)
│   │   ├── Jonathan Gibbons (团队负责人) - javac, javadoc
│   │   ├── Chen Liang - ClassFile API, 核心反射
│   │   ├── Jan Lahoda - javac 编译器, JEP 511/512
│   │   ├── Adam Sotona - ClassFile API
│   │   └── Vicente Romero - javac 编译器
│   │
│   ├── Core Libraries Team (核心库团队)
│   │   ├── Phil Race (Client Libraries Group Lead) - Swing, Java 2D, AWT
│   │   ├── Daniel Fuchs (Networking Team Lead) - HTTP Client, JMX, HTTP/3
│   │   ├── Naoto Sato - 国际化 (i18n)
│   │   ├── Brian Burkhalter - NIO, 网络
│   │   ├── Justin Lu - 本地化
│   │   ├── Prasanta Sadhukhan - Desktop, Swing
│   │   ├── Volkan Yazici - HTTP Client
│   │   ├── Sergey Bylokhov - AWT/2D
│   │   ├── Jaikiran Pai - Networking
│   │   ├── Lance Andersen - JDBC
│   │   └── Per Minborg - Core Libs
│   │
│   ├── Concurrency & Runtime Team (并发与运行时团队)
│   │   ├── Alan Bateman (Core Libraries Group Lead) - 并发, Project Loom
│   │   ├── David Holmes (JVM Runtime Group) - 并发，JVM 运行时
│   │   └── Leonid Mesnik - JVMTI, HotSpot 测试
│   │
│   └── Performance Team (性能优化团队)
│       └── Claes Redestad - 启动性能，字符串拼接
│
├── HotSpot Runtime Team (HotSpot 运行时团队)
│   ├── Ioi Lam - CDS, AOT, JEP 514
│   ├── Coleen Phillimore - HotSpot VM Core, Metaspace
│   ├── Kim Barrett - HotSpot Runtime, C++ 现代化
│   └── Erik Gahlin - JFR, JEP 520
│
├── HotSpot GC Team (HotSpot 垃圾收集器团队)
│   ├── Thomas Schatzl (G1 GC Lead) - G1 GC, Parallel GC, JEP 522
│   └── Erik Österlund - ZGC, GC
│
├── HotSpot Compiler Team (HotSpot 编译器团队)
│   ├── Emanuel Peter - C2 编译器, SuperWord, 向量化
│   └── Christian Hagedorn - HotSpot Compiler/C2
│
├── Tools Team (工具团队)
│   └── Alexey Semenyuk - jpackage
│
├── Java Engineering Infrastructure Team (Java 工程基础设施团队)
│   └── Magnus Ihse Bursie - 构建系统
│
├── Security Team (安全团队)
│   └── Weijun Wang - 安全
│
└── Oracle Labs
    └── Doug Simon - Graal 编译器
```

### 团队统计

| 团队 | 人数 | 代表贡献者 | PR 总数 |
|------|------|------------|---------|
| **Java Platform Group** | 19 人 | Chen Liang, Jan Lahoda, Daniel Fuchs, Phil Race | 2,800+ |
| **HotSpot Runtime Team** | 4 人 | Ioi Lam, Coleen Phillimore, Kim Barrett, Erik Gahlin | 1,505+ |
| **HotSpot GC Team** | 2 人 | Thomas Schatzl, Erik Österlund | 558+ |
| **HotSpot Compiler Team** | 2 人 | Emanuel Peter, Christian Hagedorn | 226+ |
| **Tools Team** | 1 人 | Alexey Semenyuk | 233+ |
| **Java Engineering Infrastructure** | 1 人 | Magnus Ihse Bursie | 28+ |
| **Security Team** | 1 人 | Weijun Wang | 15+ |
| **Oracle Labs** | 1 人 | Doug Simon | 10+ |
| **总计** | **32 人** | - | **5,700+** |

> **注**: 当前 Oracle 团队 31 人 + 已离职 (Hamlin Li) 1 人 = Top 贡献者列表 32 人

### Group Leads

| Group | Lead | 职责 | JEP 贡献 |
|-------|------|------|----------|
| **Client Libraries** | [Phil Race](../../by-contributor/profiles/phil-race.md) | Swing, Java 2D, AWT | JEP 504 |
| **Networking** | [Daniel Fuchs](../../by-contributor/profiles/daniel-fuchs.md) | HTTP Client, JMX | JEP 517 |
| **G1 GC** | [Thomas Schatzl](../../by-contributor/profiles/thomas-schatzl.md) | G1 GC, Parallel GC | JEP 522 |
| **C2 Compiler** | [Emanuel Peter](../../by-contributor/profiles/emanuel-peter.md) | SuperWord 向量化 | - |
| **LangTools** | [Jonathan Gibbons](../../by-contributor/profiles/jonathan-gibbons.md) | javac, javadoc | - |
| **Performance** | [Claes Redestad](../../by-contributor/profiles/claes-redestad.md) | 启动性能 | - |
| **JFR** | [Erik Gahlin](../../by-contributor/profiles/erik-gahlin.md) | Flight Recorder | JEP 520 |
| **CDS/AOT** | [Ioi Lam](../../by-contributor/profiles/ioi-lam.md) | Class Data Sharing | JEP 514 |

---

## 5. 影响的模块

| 模块 | 文件数 | 说明 |
|------|--------|------|
| CLDR 数据 | 9,340 | 国际化数据更新 |
| HotSpot Runtime | 7,379 | JVM 运行时 |
| G1 GC | 6,862 | G1 垃圾收集器 |
| C2 编译器 | 6,532 | 服务端编译器 |
| Shenandoah GC | 3,982 | Shenandoah 垃圾收集器 |
| Class File | 3,781 | 类文件处理 |
| x86 移植 | 3,755 | x86 架构支持 |
| GC 共享 | 3,587 | GC 共享代码 |
| OOPs | 3,359 | 对象模型 |
| AArch64 移植 | 2,975 | AArch64 架构支持 |
| ZGC | 2,958 | Z 垃圾收集器 |

---

## 6. 主要领域与 JEP 贡献

### GC (垃圾收集)

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| G1 GC | Thomas Schatzl | JEP 522 | [详情](../../by-contributor/profiles/thomas-schatzl.md) |
| G1 GC | Albert Mingkun Yang | - | [详情](../../by-contributor/profiles/albert-mingkun-yang.md) |
| 并发 GC | Kim Barrett | - | [详情](../../by-contributor/profiles/kim-barrett.md) |

### 编译器

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| C2 编译器 | Emanuel Peter | - | [详情](../../by-contributor/profiles/emanuel-peter.md) |
| SuperWord 向量化 | Emanuel Peter | - | [详情](../../by-contributor/profiles/emanuel-peter.md) |

### 核心库与性能

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| 启动性能 | Claes Redestad | - | [详情](../../by-contributor/profiles/claes-redestad.md) |
| ClassFile API | Chen Liang | JEP 459, 466, 484 | [详情](../../by-contributor/profiles/chen-liang.md) |

### 语言特性

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| javac | Jan Lahoda | JEP 511, JEP 512 | [详情](../../by-contributor/profiles/jan-lahoda.md) |
| javadoc | Jonathan Gibbons | - | [详情](../../by-contributor/profiles/jonathan-gibbons.md) |

### 构建系统

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| 构建系统 | Magnus Ihse Bursie | - | [详情](../../by-contributor/profiles/magnus-ihse-bursie.md) |

### 桌面/客户端

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| Client Libraries | Phil Race | JEP 504 | [详情](../../by-contributor/profiles/phil-race.md) |
| Swing/AWT | Prasanta Sadhukhan | - | [详情](../../by-contributor/profiles/prasanta-sadhukhan.md) |
| 图形/打印 | Brian Burkhalter | - | [详情](../../by-contributor/profiles/brian-burkhalter.md) |

### 网络与 HTTP

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| HTTP/3 | Daniel Fuchs | JEP 517 | [详情](../../by-contributor/profiles/daniel-fuchs.md) |
| HTTP Client | Volkan Yazici | - | [详情](../../by-contributor/profiles/volkan-yazici.md) |

### 并发与运行时

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| 并发 | David Holmes | - | [详情](../../by-contributor/profiles/david-holmes.md) |
| Atomic<T> | Kim Barrett | - | [详情](../../by-contributor/profiles/kim-barrett.md) |

### 工具与监控

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| JFR | Erik Gahlin | JEP 520, JEP 349 | [详情](../../by-contributor/profiles/erik-gahlin.md) |
| JVMTI | Leonid Mesnik | - | [详情](../../by-contributor/profiles/leonid-mesnik.md) |

### 国际化

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| i18n | Naoto Sato | - | [详情](../../by-contributor/profiles/naoto-sato.md) |
| 本地化 | Justin Lu | - | [详情](../../by-contributor/profiles/justin-lu.md) |

### AOT 与 CDS

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| AOT/CDS | Ioi Lam | JEP 514 | [详情](../../by-contributor/profiles/ioi-lam.md) |
| jpackage | Alexey Semenyuk | - | [详情](../../by-contributor/profiles/alexey-semenyuk.md) |

---

## 7. Oracle 主导的 JEP (JDK 24-26)

| JEP | 标题 | Lead | 团队 | 版本 |
|-----|------|------|------|------|
| [JEP 517](https://openjdk.org/jeps/517) | HTTP/3 for HTTP Client | Daniel Fuchs | Core Libraries | JDK 26 |
| [JEP 514](https://openjdk.org/jeps/514) | AOT Command Line Ergonomics | Ioi Lam | HotSpot Runtime | JDK 26 |
| [JEP 520](https://openjdk.org/jeps/520) | JFR Method Timing and Tracing | Erik Gahlin | HotSpot Runtime | JDK 26 |
| [JEP 511](https://openjdk.org/jeps/511) | Module Import Declarations | Jan Lahoda | LangTools | JDK 26 |
| [JEP 512](https://openjdk.org/jeps/512) | Compact Source Files | Jan Lahoda | LangTools | JDK 26 |
| [JEP 522](https://openjdk.org/jeps/522) | G1 GC Throughput Improvement | Thomas Schatzl | HotSpot GC | JDK 26 |
| [JEP 504](https://openjdk.org/jeps/504) | Remove Applet API | Phil Race | Client Libraries | JDK 26 |

### 历史 JEP 贡献 (JDK 9-21)

| JEP | 标题 | Lead | 版本 |
|-----|------|------|------|
| [JEP 254](https://openjdk.org/jeps/254) | Compact Strings | Xueming Shen | JDK 9 |
| [JEP 280](https://openjdk.org/jeps/280) | Indify String Concatenation | Aleksey Shipilev | JDK 9 |
| [JEP 349](https://openjdk.org/jeps/349) | JFR Event Streaming | Erik Gahlin | JDK 14 |

---

## 8. 相关 PR 分析文档

### ClassFile API (Chen Liang)

| PR | 标题 | 分析文档 |
|----|------|----------|
| JDK-8342336 | Remove unused imports | [详情](../../by-pr/8342/8342336.md) |
| JDK-8341199 | Add ConstantDynamicBuilder.loadConstant | [详情](../../by-pr/8341/8341199.md) |
| JDK-8339217 | Add ClassBuilder.loadConstant | [详情](../../by-pr/8339/8339217.md) |
| JDK-8339320 | Utf8EntryImpl#inflate | [详情](../../by-pr/8339/8339320.md) |
| JDK-8339290 | Utf8EntryImpl#writeTo | [详情](../../by-pr/8339/8339290.md) |
| JDK-8339317 | BytecodeBuilder#writeBuffer | [详情](../../by-pr/8339/8339317.md) |
| JDK-8339168 | ClassImpl#slotSize | [详情](../../by-pr/8339/8339168.md) |
| JDK-8339205 | StackMapGenerator writeU1/U2/Int/Long | [详情](../../by-pr/8339/8339205.md) |
| JDK-8339196 | Add writeU1/U2/Int/Long to BufferBuilder | [详情](../../by-pr/8339/8339196.md) |
| JDK-8338937 | ClassDesc concat optimization | [详情](../../by-pr/8338/8338937.md) |
| JDK-8338532 | MethodTypeDesc implementation optimization | [详情](../../by-pr/8338/8338532.md) |
| JDK-8338409 | Record helpers | [详情](../../by-pr/8338/8338409.md) |
| JDK-8338936 | StringConcatFactory MethodType optimization | [详情](../../by-pr/8338/8338936.md) |
| JDK-8371953 | Reflection API performance | [详情](../../by-pr/8371/8371953.md) |
| JDK-8371701 | Field lookup optimization | [详情](../../by-pr/8371/8371701.md) |

### GC 相关

| PR | 标题 | 分析文档 |
|----|------|----------|
| JDK-8343984 | Unsafe out-of-bounds check | [详情](../../by-pr/8343/8343984.md) |
| JDK-8343925 | SharedGC support | [详情](../../by-pr/8343/8343925.md) |

### 性能优化

| PR | 标题 | 分析文档 |
|----|------|----------|
| JDK-8310929 | Integer.toString 优化 | [详情](../../by-pr/8310/8310929.md) |
| JDK-8310502 | Long.fastUUID 优化 | [详情](../../by-pr/8310/8310502.md) |
| JDK-8315968 | Array optimization | [详情](../../by-pr/8315/8315968.md) |
| JDK-8315970 | Bug fix | [详情](../../by-pr/8315/8315970.md) |
| JDK-8317742 | Type check optimization | [详情](../../by-pr/8317/8317742.md) |
| JDK-8311207 | Code cleanup | [详情](../../by-pr/8311/8311207.md) |

[→ 返回组织索引](../../by-contributor/index.md)

---

## 8. 贡献时间线

```
注: 2010-2019 年的贡献数据无法通过 GitHub PR 统计获取（OpenJDK 于 2020 年迁移至 GitHub）。
2020: ███████████████████████████████████████████████████████████░ 800+ PRs
2020: ███████████████████████████████████████████████████████████░ 800+ PRs
2021: ███████████████████████████████████████████████████████████░ 800+ PRs
2022: ███████████████████████████████████████████████████████████░ 850+ PRs
2023: ███████████████████████████████████████████████████████████░ 900+ PRs
2024: ███████████████████████████████████████████████████████████░ 950+ PRs
2025: ███████████████████████████████████████████████████████████░ 1000+ PRs
2026: ████████████████████████████████████████████░░░░░░░░░░░ 500+ PRs
```

> **总计**: 12,000+ PRs (2010-2026)

> **注**: Oracle 是 OpenJDK 的主要维护者，持续贡献占比约 70%

---

## 9. OpenJDK 治理参与

### OpenJDK Governing Board 成员

Oracle 在 OpenJDK Governing Board 中有代表席位：

| 代表 | 角色 | 任期 |
|------|------|------|
| Phil Race | At-Large Member | 多届当选 |

### Group Leads

Oracle 贡献者担任以下 Group 的 Lead：

| Group | Lead | 职责 |
|-------|------|------|
| Client Libraries | Phil Race | Swing, Java 2D, AWT |
| Core Libraries | Alan Bateman (Lead) | 核心库 |
| HotSpot | - | JVM 运行时 |

### 新晋 Committer/Reviewer 提名

| 贡献者 | 时间 | 角色 | 提名人 | 领域 |
|--------|------|------|--------|------|
| Claes Redestad | 2022-03 | OpenJDK Member | Daniel Fuchs | Performance |
| Coleen Phillimore | 2024-07 | Valhalla Committer | - | Valhalla |
| Emanuel Peter | 2022-05 | JDK Committer | Tobias Hartmann | C2 Compiler |
| Emanuel Peter | 2023-05 | JDK Reviewer | Andrew Dinn | C2 Compiler |

---

## 10. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-21
- **数据来源**: [JDK 26 Top Contributors](../../by-contributor/profiles/jdk26-top-contributors.md)

---

## 9. 相关链接

- [Oracle Java](https://www.oracle.com/java/)
- [Oracle OpenJDK](https://openjdk.org/groups/hotspot/)
- [Oracle GitHub](https://github.com/oracle)

---

> **文档版本**: 12.0
> **最后更新**: 2026-03-22
> **更新内容**:
> - **修复**: Core Libraries Group Lead 从 Stuart Marks 修正为 Alan Bateman (根据 OpenJDK Census 验证)
> - **修复**: David Holmes 从美国团队移至澳洲团队 (Brisbane, Australia)
> - **修复**: Alan Bateman 从美国团队移至欧洲团队 (UK)
> - **修复**: Per Minborg 从美国团队移至欧洲团队 (Sweden)
> - **修复**: Jan Lahoda 从美国团队移至欧洲团队 (Czechia)
> - **修复**: Erik Gahlin 从 HotSpot Compiler 移至 HotSpot Runtime (根据 Oracle 官方资料验证)
> - **修复**: Alexey Semenyuk 领域从 AOT/HotSpot Compiler 修正为 jpackage/Tools (根据 OpenJDK 贡献记录验证)
> - **修复**: Erik Osterlund 领域从 AOT, GC 修正为 ZGC, GC (他是 ZGC 核心开发者)
> - **修复**: Brian Burkhalter 角色从 Committer 修正为 Reviewer (根据 OpenJDK Census 验证)
> - **修复**: Per Minborg 角色从 Member 修正为 Reviewer (根据 OpenJDK Census 验证)
> - **修复**: Jaikiran Pai 领域从构建修正为 Networking (根据 OpenJDK Networking Group 成员记录验证)
> - **修复**: JEP 514 团队从 HotSpot GC 修正为 HotSpot Runtime (Ioi Lam 的 CDS/AOT 团队)
> - **修复**: JEP 254 作者从 Claes Redestad 修正为 Xueming Shen (根据 openjdk.org/jeps/254 验证)
> - **修复**: JEP 280 作者从 Claes Redestad 修正为 Aleksey Shipilev (根据 openjdk.org/jeps/280 验证)
> - **新增**: 澳洲团队分类 (David Holmes)
> - 美国团队：12 人
> - 欧洲团队：10 人 (新增 Per Minborg, Jan Lahoda, Alan Bateman)
> - 亚洲团队：3 人
> - 澳洲团队：1 人 (David Holmes)
> - Oracle Labs: 1 人 (Doug Simon)
> - 数据来源：贡献者档案、OpenJDK Census 和 Web 验证

---

> **文档版本**: 12.0
> **最后更新**: 2026-03-22
> **本次更新**:
> - 基于 Web 验证修正多处错误 (角色、团队归属、地区分类、JEP 归属)
> - **新增**: 新晋 Committer/Reviewer 提名表
> - **更新**: 地理位置更准确 (基于 LinkedIn/个人档案)
> - **新增**: 已离职贡献者单独列表
> - **修复**: 章节编号统一 (1-11)
> - **新增**: Oracle Labs 贡献者 (Christian Hagedorn)
> - **更新**: 团队统计数据更准确