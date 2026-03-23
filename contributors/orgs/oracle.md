# Oracle

> OpenJDK 主要维护者和最大贡献者

[← 返回组织索引](README.md)

---
## 目录

1. [概览](#1-概览)
2. [Top 贡献者](#2-top-贡献者)
3. [按地区分类](#3-按地区分类的-oracle-贡献者)
4. [组织架构](#4-组织架构)
5. [影响的模块](#5-影响的模块)
6. [主要领域与 JEP 贡献](#6-主要领域与-jep-贡献)
7. [Oracle 主导的 JEP (JDK 24-26)](#7-oracle-主导的-jep-jdk-24-26)
8. [相关 PR 分析文档](#8-相关-pr-分析文档)
9. [贡献时间线](#9-贡献时间线)
10. [OpenJDK 治理参与](#10-openjdk-治理参与)
11. [数据来源](#11-数据来源)
12. [相关链接](#12-相关链接)

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
| **2021-至今** | LTS 版本 (JDK 17, JDK 21, JDK 25) |

---

## 2. Top 贡献者

### JDK 26 Top Oracle 贡献者 (按 PR 数量排序)

| 排名 | 贡献者 | GitHub | PRs | 角色 | 领域 | 团队 | 档案 |
|------|--------|--------|-----|------|------|------|------|
| 1 | Thomas Schatzl | [@tschatzl](https://github.com/tschatzl) | 546 | Reviewer | G1 GC | HotSpot GC | [详情](../../by-contributor/profiles/thomas-schatzl.md) |
| 2 | Ioi Lam | [@iklam](https://github.com/iklam) | 431 | Reviewer | CDS/AOT | HotSpot Runtime/CDS | [详情](../../by-contributor/profiles/ioi-lam.md) |
| 3 | Coleen Phillimore | [@coleenp](https://github.com/coleenp) | 400 | Reviewer | HotSpot | HotSpot Runtime | [详情](../../by-contributor/profiles/coleen-phillimore.md) |
| 4 | Kim Barrett | [@kimbarrett](https://github.com/kimbarrett) | 352 | Reviewer | Atomic, C++ | HotSpot Runtime | [详情](../../by-contributor/profiles/kim-barrett.md) |
| 5 | Jan Lahoda | [@lahodaj](https://github.com/lahodaj) | 324 | Reviewer | javac | LangTools | [详情](../../by-contributor/profiles/jan-lahoda.md) |
| 6 | Erik Gahlin | [@egahlin](https://github.com/egahlin) | 322 | Reviewer | JFR | HotSpot Runtime | [详情](../../by-contributor/profiles/erik-gahlin.md) |
| 7 | Jaikiran Pai | [@jaikiran](https://github.com/jaikiran) | 322 | Reviewer | Networking | Core Libraries | [详情](../../by-contributor/profiles/jaikiran-pai.md) |
| 8 | Phil Race | [@prrace](https://github.com/prrace) | 303 | Reviewer | Client Libraries | Core Libraries | [详情](../../by-contributor/profiles/phil-race.md) |
| 9 | Naoto Sato | [@naotoj](https://github.com/naotoj) | 273 | Reviewer | 国际化 | Core Libraries | [详情](../../by-contributor/profiles/naoto-sato.md) |
| 10 | Sergey Bylokhov | [@mrserb](https://github.com/mrserb) | 273 | Reviewer | AWT/2D | Core Libraries | [详情](../../by-contributor/profiles/sergey-bylokhov.md) |
| 11 | Chen Liang | [@liach](https://github.com/liach) | 237 | Reviewer | ClassFile API | LangTools | [详情](../../by-contributor/profiles/chen-liang.md) |
| 12 | Alexey Semenyuk | [@alexeysemenyukoracle](https://github.com/alexeysemenyukoracle) | 233 | Committer | jpackage | Tools | [详情](../../by-contributor/profiles/alexey-semenyuk.md) |
| 13 | Emanuel Peter | [@eme64](https://github.com/eme64) | 226 | Reviewer | C2 编译器 | HotSpot Compiler | [详情](../../by-contributor/profiles/emanuel-peter.md) |
| 14 | Daniel Fuchs | [@dfuchs](https://github.com/dfuchs) | 192+ | Reviewer | HTTP/3, JMX | Core Libraries | [详情](../../by-contributor/profiles/daniel-fuchs.md) |
| 15 | Jonathan Gibbons | [@jonathan-gibbons](https://github.com/jonathan-gibbons) | 100+ | Reviewer | javac, javadoc | LangTools | [详情](../../by-contributor/profiles/jonathan-gibbons.md) |
| 16 | David Holmes | [@dholmes-ora](https://github.com/dholmes-ora) | 80+ | Reviewer | 并发 | Concurrency & Runtime | [详情](../../by-contributor/profiles/david-holmes.md) |
| 17 | Prasanta Sadhukhan | [@prsadhuk](https://github.com/prsadhuk) | 65+ | Reviewer | Desktop | Core Libraries | [详情](../../by-contributor/profiles/prasanta-sadhukhan.md) |
| 18 | Brian Burkhalter | [@bplb](https://github.com/bplb) | 60+ | Reviewer | 网络 | Core Libraries | [详情](../../by-contributor/profiles/brian-burkhalter.md) |
| 19 | Vicente Romero | [@vicente-romero-oracle](https://github.com/vicente-romero-oracle) | 50+ | Reviewer | javac | LangTools | [详情](../../by-contributor/profiles/vicente-romero.md) |
| 20 | Lance Andersen | [@LanceAndersen](https://github.com/LanceAndersen) | 50+ | Reviewer | JDBC | Core Libraries | [详情](../../by-contributor/profiles/lance-andersen.md) |
| 21 | Volkan Yazici | [@vy](https://github.com/vy) | 40+ | Committer | HTTP Client | Core Libraries | [详情](../../by-contributor/profiles/volkan-yazici.md) |
| 22 | Justin Lu | [@justin-lu](https://github.com/justin-lu) | 40+ | Committer | Localization | Core Libraries | [详情](../../by-contributor/profiles/justin-lu.md) |
| 23 | Leonid Mesnik | [@lmesnik](https://github.com/lmesnik) | 35+ | Reviewer | JVMTI | Concurrency & Runtime | [详情](../../by-contributor/profiles/leonid-mesnik.md) |
| 24 | Christian Hagedorn | [@chhagedorn](https://github.com/chhagedorn) | 30+ | Reviewer | C2 编译器 | HotSpot Compiler | [详情](../../by-contributor/profiles/christian-hagedorn.md) |
| 25 | Claes Redestad | [@redestad](https://github.com/redestad) | 30+ | Reviewer | Performance | Java Platform | [详情](../../by-contributor/profiles/claes-redestad.md) |
| 26 | Adam Sotona | [@asotona](https://github.com/asotona) | 30+ | Committer | ClassFile API | LangTools | [详情](../../by-contributor/profiles/adam-sotona.md) |
| 27 | Magnus Ihse Bursie | [@magicus](https://github.com/magicus) | 28+ | Reviewer | Build | Infrastructure | [详情](../../by-contributor/profiles/magnus-ihse-bursie.md) |
| 28 | Hamlin Li | - | 20+ | Committer | RISC-V | **已离职 (Rivos)** | [详情](../../by-contributor/profiles/hamlin-li.md) |
| 29 | Weijun Wang | [@wangweij](https://github.com/wangweij) | 15+ | Reviewer | Security | Security | [详情](../../by-contributor/profiles/weijun-wang.md) |
| 30 | Per Minborg | [@pminborg](https://github.com/pminborg) | 15+ | Reviewer | Core Libs | Core Libraries | [详情](../../by-contributor/profiles/per-minborg.md) |
| 31 | Alan Bateman | [@AlanBateman](https://github.com/AlanBateman) | 12+ | Reviewer | Concurrency | Concurrency & Runtime | [详情](../../by-contributor/profiles/alan-bateman.md) |
| 32 | Erik Österlund | [@fisk](https://github.com/fisk) | 12+ | Reviewer | ZGC, GC | HotSpot GC | [详情](../../by-contributor/profiles/erik-osterlund.md) |
| 33 | Doug Simon | - | 10+ | Member | Graal | Oracle Labs | [详情](../../by-contributor/profiles/doug-simon.md) |
| 34 | Chris Plummer | [@plummercj](https://github.com/plummercj) | - | Reviewer | serviceability/debugging | HotSpot Runtime | [详情](../../by-contributor/profiles/chris-plummer.md) |
| 35 | Joe Wang | [@JoeWang-Java](https://github.com/JoeWang-Java) | - | Reviewer | XML/JAXP | Core Libraries | [详情](../../by-contributor/profiles/joe-wang.md) |
| 36 | Calvin Cheung | [@calvinccheung](https://github.com/calvinccheung) | - | Committer | CDS/AppCDS | HotSpot Runtime/CDS | [详情](../../by-contributor/profiles/calvin-cheung.md) |
| 37 | Sean Coffey | [@coffeys](https://github.com/coffeys) | - | Reviewer | security/TLS | Security | [详情](../../by-contributor/profiles/sean-coffey.md) |
| 38 | Yumin Qi | [@yminqi](https://github.com/yminqi) | - | Committer | CDS/AppCDS | HotSpot Runtime/CDS | [详情](../../by-contributor/profiles/yumin-qi.md) |
| 39 | Kevin Walls | [@kevinjwalls](https://github.com/kevinjwalls) | - | Committer | JMX/JFR | HotSpot Runtime | [详情](../../by-contributor/profiles/kevin-walls.md) |
| 40 | Alexander Ivanov | - | - | Committer | AWT/Swing | Core Libraries | [详情](../../by-contributor/profiles/alexander-ivanov.md) |
| 41 | Ivan Walulya | - | - | Committer | G1 GC | HotSpot GC | [详情](../../by-contributor/profiles/ivan-walulya.md) |
| 42 | Marc Chevalier | - | - | Committer | C2 compiler | HotSpot Compiler | [详情](../../by-contributor/profiles/marc-chevalier.md) |
| 43 | Casper Norrbin | - | - | Committer | Linux containers/runtime | HotSpot Runtime | [详情](../../by-contributor/profiles/casper-norrbin.md) |
| 44 | Anton Artemov | - | - | Committer | math/AArch64 | Core Libraries | [详情](../../by-contributor/profiles/anton-artemov.md) |
| 45 | Benoit Maillard | - | - | Committer | C2 compiler | HotSpot Compiler | [详情](../../by-contributor/profiles/benoit-maillard.md) |
| 46 | Aggelos Biboudis | - | - | Committer | javac/language features | LangTools | [详情](../../by-contributor/profiles/aggelos-biboudis.md) |
| 47 | Roberto Castaneda Lozano | - | - | Committer | C2 compiler/IGV | HotSpot Compiler | [详情](../../by-contributor/profiles/roberto-castaneda-lozano.md) |
| 48 | Tobias Holenstein | - | - | Committer | C2 compiler/IGV | HotSpot Compiler | [详情](../../by-contributor/profiles/tobias-holenstein.md) |
| 49 | Christian Stein | - | - | Committer | JEP 458/jtreg | Infrastructure | [详情](../../by-contributor/profiles/christian-stein.md) |
| 50 | Alexander Zuev | - | - | Committer | AWT/Swing | Core Libraries | [详情](../../by-contributor/profiles/alexander-zuev.md) |
| 51 | Nizar Ben Alla | - | - | Committer | javadoc/release eng | LangTools | [详情](../../by-contributor/profiles/nizar-ben-alla.md) |
| 52 | Patrick Concannon | - | - | Committer | networking | Core Libraries | [详情](../../by-contributor/profiles/patrick-concannon.md) |
| 53 | Dmitry Markov | - | - | Committer | AWT/Swing | Core Libraries | [详情](../../by-contributor/profiles/dmitry-markov.md) |
| 54 | Johan Sjolen | - | - | Committer | NMT/HotSpot diagnostics | HotSpot Runtime | [详情](../../by-contributor/profiles/johan-sjolen.md) |
| 55 | Henry Jen | [@slowhog](https://github.com/slowhog) | - | Committer | jlink/native code | Tools | [详情](../../by-contributor/profiles/henry-jen.md) |
| 56 | Sundararajan Athijegannathan | - | - | Committer | Nashorn/scripting | LangTools | [详情](../../by-contributor/profiles/sundararajan-athijegannathan.md) |
| 57 | Igor Ignatev | - | - | Committer | test infrastructure | Infrastructure | [详情](../../by-contributor/profiles/igor-ignatev.md) |
| 58 | Hannes Wallnoefer | - | - | Committer | javadoc/Nashorn | LangTools | [详情](../../by-contributor/profiles/hannes-wallnoefer.md) |
| 59 | Tim Bell | - | - | Committer | build infrastructure | Infrastructure | [详情](../../by-contributor/profiles/tim-bell.md) |

**小计**: 4,200+ PRs (以上 59 人，含 1 位已离职)

### 新晋 Committer/Reviewer

| 贡献者 | 时间 | 角色 | 提名人 | 领域 |
|--------|------|------|--------|------|
| Emanuel Peter | 2022-05 | JDK Committer | Tobias Hartmann | C2 Compiler |
| Claes Redestad | 2022-03 | OpenJDK Member | Daniel Fuchs | Performance |
| Emanuel Peter | 2023-05 | JDK Reviewer | Andrew Dinn | C2 Compiler |
| Coleen Phillimore | 2024-07 | Valhalla Committer | - | Valhalla |

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
| Phil Race | USA | [@prrace](https://github.com/prrace) | 303 | Reviewer | Client Libs | [详情](../../by-contributor/profiles/phil-race.md) |
| Naoto Sato | San Jose, CA | [@naotoj](https://github.com/naotoj) | 273 | Reviewer | 国际化 | [详情](../../by-contributor/profiles/naoto-sato.md) |
| Chen Liang | Austin, TX | [@liach](https://github.com/liach) | 237 | Reviewer | ClassFile API | [详情](../../by-contributor/profiles/chen-liang.md) |
| Jonathan Gibbons | USA | [@jonathan-gibbons](https://github.com/jonathan-gibbons) | 100+ | Reviewer | javac/javadoc | [详情](../../by-contributor/profiles/jonathan-gibbons.md) |
| Brian Burkhalter | USA | [@bplb](https://github.com/bplb) | 60+ | Reviewer | 网络 | [详情](../../by-contributor/profiles/brian-burkhalter.md) |
| Vicente Romero | USA | [@vicente-romero-oracle](https://github.com/vicente-romero-oracle) | 50+ | Reviewer | javac | [详情](../../by-contributor/profiles/vicente-romero.md) |
| Lance Andersen | USA | [@LanceAndersen](https://github.com/LanceAndersen) | 50+ | Reviewer | JDBC | [详情](../../by-contributor/profiles/lance-andersen.md) |
| Justin Lu | USA | [@justin-lu](https://github.com/justin-lu) | 40+ | Committer | Localization | [详情](../../by-contributor/profiles/justin-lu.md) |
| Leonid Mesnik | USA | [@lmesnik](https://github.com/lmesnik) | 35+ | Reviewer | JVMTI | [详情](../../by-contributor/profiles/leonid-mesnik.md) |
| Chris Plummer | USA | [@plummercj](https://github.com/plummercj) | - | Reviewer | serviceability/debugging | [详情](../../by-contributor/profiles/chris-plummer.md) |
| Joe Wang | USA | [@JoeWang-Java](https://github.com/JoeWang-Java) | - | Reviewer | XML/JAXP | [详情](../../by-contributor/profiles/joe-wang.md) |
| Calvin Cheung | USA | [@calvinccheung](https://github.com/calvinccheung) | - | Committer | CDS/AppCDS | [详情](../../by-contributor/profiles/calvin-cheung.md) |
| Yumin Qi | USA | [@yminqi](https://github.com/yminqi) | - | Committer | CDS/AppCDS | [详情](../../by-contributor/profiles/yumin-qi.md) |
| Henry Jen | USA | [@slowhog](https://github.com/slowhog) | - | Committer | jlink/native code | [详情](../../by-contributor/profiles/henry-jen.md) |
| Sundararajan Athijegannathan | USA | - | - | Committer | Nashorn/scripting | [详情](../../by-contributor/profiles/sundararajan-athijegannathan.md) |

### 欧洲团队

| 贡献者 | 位置 | GitHub | PRs | 角色 | 领域 | 档案 |
|--------|------|--------|-----|------|------|------|
| Thomas Schatzl | Germany | [@tschatzl](https://github.com/tschatzl) | 546 | Reviewer | G1 GC | [详情](../../by-contributor/profiles/thomas-schatzl.md) |
| Jan Lahoda | Czechia | [@lahodaj](https://github.com/lahodaj) | 324 | Reviewer | javac | [详情](../../by-contributor/profiles/jan-lahoda.md) |
| Erik Gahlin | Sweden | [@egahlin](https://github.com/egahlin) | 322 | Reviewer | JFR | [详情](../../by-contributor/profiles/erik-gahlin.md) |
| Emanuel Peter | Zürich, Switzerland | [@eme64](https://github.com/eme64) | 226 | Reviewer | C2 编译器 | [详情](../../by-contributor/profiles/emanuel-peter.md) |
| Daniel Fuchs | Dublin, Ireland | [@dfuchs](https://github.com/dfuchs) | 192+ | Reviewer | HTTP/3, JMX | [详情](../../by-contributor/profiles/daniel-fuchs.md) |
| Christian Hagedorn | Sweden | [@chhagedorn](https://github.com/chhagedorn) | 30+ | Reviewer | C2 编译器 | [详情](../../by-contributor/profiles/christian-hagedorn.md) |
| Claes Redestad | Stockholm, Sweden | [@redestad](https://github.com/redestad) | 30+ | Reviewer | Performance | [详情](../../by-contributor/profiles/claes-redestad.md) |
| Magnus Ihse Bursie | Sweden | [@magicus](https://github.com/magicus) | 28+ | Reviewer | Build | [详情](../../by-contributor/profiles/magnus-ihse-bursie.md) |
| Per Minborg | Sweden | [@pminborg](https://github.com/pminborg) | 15+ | Reviewer | Core Libs | [详情](../../by-contributor/profiles/per-minborg.md) |
| Alan Bateman | UK | [@AlanBateman](https://github.com/AlanBateman) | 12+ | Reviewer | Concurrency | [详情](../../by-contributor/profiles/alan-bateman.md) |
| Erik Österlund | Sweden | [@fisk](https://github.com/fisk) | 12+ | Reviewer | ZGC, GC | [详情](../../by-contributor/profiles/erik-osterlund.md) |
| Ivan Walulya | Sweden | - | - | Committer | G1 GC | [详情](../../by-contributor/profiles/ivan-walulya.md) |
| Marc Chevalier | Switzerland | - | - | Committer | C2 compiler | [详情](../../by-contributor/profiles/marc-chevalier.md) |
| Casper Norrbin | Sweden | - | - | Committer | Linux containers/runtime | [详情](../../by-contributor/profiles/casper-norrbin.md) |
| Benoit Maillard | Switzerland | - | - | Committer | C2 compiler | [详情](../../by-contributor/profiles/benoit-maillard.md) |
| Roberto Castaneda Lozano | Sweden | - | - | Committer | C2 compiler/IGV | [详情](../../by-contributor/profiles/roberto-castaneda-lozano.md) |
| Tobias Holenstein | Switzerland | - | - | Committer | C2 compiler/IGV | [详情](../../by-contributor/profiles/tobias-holenstein.md) |
| Christian Stein | Germany | - | - | Committer | JEP 458/jtreg | [详情](../../by-contributor/profiles/christian-stein.md) |
| Hannes Wallnoefer | Austria | - | - | Committer | javadoc/Nashorn | [详情](../../by-contributor/profiles/hannes-wallnoefer.md) |
| Sean Coffey | Ireland | [@coffeys](https://github.com/coffeys) | - | Reviewer | security/TLS | [详情](../../by-contributor/profiles/sean-coffey.md) |
| Patrick Concannon | Ireland | - | - | Committer | networking | [详情](../../by-contributor/profiles/patrick-concannon.md) |
| Aggelos Biboudis | Greece | - | - | Committer | javac/language features | [详情](../../by-contributor/profiles/aggelos-biboudis.md) |
| Johan Sjolen | Sweden | - | - | Committer | NMT/HotSpot diagnostics | [详情](../../by-contributor/profiles/johan-sjolen.md) |
| Nizar Ben Alla | Europe | - | - | Committer | javadoc/release eng | [详情](../../by-contributor/profiles/nizar-ben-alla.md) |
| Kevin Walls | UK | [@kevinjwalls](https://github.com/kevinjwalls) | - | Committer | JMX/JFR | [详情](../../by-contributor/profiles/kevin-walls.md) |
| Anton Artemov | Europe | - | - | Committer | math/AArch64 | [详情](../../by-contributor/profiles/anton-artemov.md) |

### 亚洲团队

| 贡献者 | 位置 | GitHub | PRs | 角色 | 领域 | 档案 |
|--------|------|--------|-----|------|------|------|
| Jaikiran Pai | India | [@jaikiran](https://github.com/jaikiran) | 322 | Reviewer | Networking | [详情](../../by-contributor/profiles/jaikiran-pai.md) |
| Sergey Bylokhov | Russia/USA | [@mrserb](https://github.com/mrserb) | 273 | Reviewer | AWT/2D | [详情](../../by-contributor/profiles/sergey-bylokhov.md) |
| Alexey Semenyuk | Russia | [@alexeysemenyukoracle](https://github.com/alexeysemenyukoracle) | 233 | Committer | jpackage | [详情](../../by-contributor/profiles/alexey-semenyuk.md) |
| Prasanta Sadhukhan | India | [@prsadhuk](https://github.com/prsadhuk) | 65+ | Reviewer | Desktop | [详情](../../by-contributor/profiles/prasanta-sadhukhan.md) |
| Weijun Wang | China | [@wangweij](https://github.com/wangweij) | 15+ | Reviewer | Security | [详情](../../by-contributor/profiles/weijun-wang.md) |
| Volkan Yazici | Turkey | [@vy](https://github.com/vy) | 40+ | Committer | HTTP Client | [详情](../../by-contributor/profiles/volkan-yazici.md) |
| Alexander Ivanov | Russia | - | - | Committer | AWT/Swing | [详情](../../by-contributor/profiles/alexander-ivanov.md) |
| Alexander Zuev | Russia | - | - | Committer | AWT/Swing | [详情](../../by-contributor/profiles/alexander-zuev.md) |
| Dmitry Markov | Russia | - | - | Committer | AWT/Swing | [详情](../../by-contributor/profiles/dmitry-markov.md) |
| Igor Ignatev | Russia | - | - | Committer | test infrastructure | [详情](../../by-contributor/profiles/igor-ignatev.md) |

### 澳洲团队

| 贡献者 | 位置 | GitHub | PRs | 角色 | 领域 | 档案 |
|--------|------|--------|-----|------|------|------|
| David Holmes | Brisbane, Australia | [@dholmes-ora](https://github.com/dholmes-ora) | 80+ | Reviewer | 并发 | [详情](../../by-contributor/profiles/david-holmes.md) |

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
| Tony Printezis | HotSpot GC | **Rivos** | - | G1 GC | [详情](../../by-contributor/profiles/tony-printezis.md) |

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
│   │   ├── Vicente Romero - javac 编译器
│   │   ├── Aggelos Biboudis - javac, 语言特性
│   │   ├── Sundararajan Athijegannathan - Nashorn/scripting
│   │   ├── Hannes Wallnoefer - javadoc/Nashorn
│   │   └── Nizar Ben Alla - javadoc/release eng
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
│   │   ├── Patrick Concannon - Networking
│   │   ├── Lance Andersen - JDBC
│   │   ├── Per Minborg - Core Libs, Stable Values
│   │   ├── Joe Wang - XML/JAXP
│   │   ├── Alexander Ivanov - AWT/Swing
│   │   ├── Alexander Zuev - AWT/Swing
│   │   ├── Dmitry Markov - AWT/Swing
│   │   └── Anton Artemov - math/AArch64
│   │
│   ├── Concurrency & Runtime Team (并发与运行时团队)
│   │   ├── Alan Bateman (Core Libraries Group Lead) - 并发, Project Loom
│   │   ├── David Holmes (JVM Runtime Group) - 并发，JVM 运行时
│   │   ├── Leonid Mesnik - JVMTI, HotSpot 测试
│   │   └── Kevin Walls - JMX/JFR
│   │
│   └── Performance Team (性能优化团队)
│       └── Claes Redestad - 启动性能，字符串拼接
│
├── HotSpot Runtime Team (HotSpot 运行时团队)
│   ├── Ioi Lam - CDS, AOT, JEP 514
│   ├── Coleen Phillimore - HotSpot VM Core, Metaspace
│   ├── Kim Barrett - HotSpot Runtime, C++ 现代化
│   ├── Erik Gahlin - JFR, JEP 520
│   ├── Chris Plummer - serviceability/debugging
│   ├── Calvin Cheung - CDS/AppCDS
│   ├── Yumin Qi - CDS/AppCDS
│   ├── Casper Norrbin - Linux containers/runtime
│   └── Johan Sjolen - NMT/HotSpot diagnostics
│
├── HotSpot GC Team (HotSpot 垃圾收集器团队)
│   ├── Thomas Schatzl (G1 GC Lead) - G1 GC, Parallel GC, JEP 522
│   ├── Erik Österlund - ZGC, GC
│   └── Ivan Walulya - G1 GC
│
├── HotSpot Compiler Team (HotSpot 编译器团队)
│   ├── Emanuel Peter - C2 编译器, SuperWord, 向量化
│   ├── Christian Hagedorn - HotSpot Compiler/C2
│   ├── Marc Chevalier - C2 compiler
│   ├── Benoit Maillard - C2 compiler
│   ├── Roberto Castaneda Lozano - C2 compiler/IGV
│   └── Tobias Holenstein - C2 compiler/IGV
│
├── Tools Team (工具团队)
│   ├── Alexey Semenyuk - jpackage
│   └── Henry Jen - jlink/native code
│
├── Java Engineering Infrastructure Team (Java 工程基础设施团队)
│   ├── Magnus Ihse Bursie - 构建系统
│   ├── Tim Bell - build infrastructure
│   ├── Igor Ignatev - test infrastructure
│   └── Christian Stein - JEP 458/jtreg
│
├── Security Team (安全团队)
│   ├── Weijun Wang - 安全, KDF API
│   └── Sean Coffey - security/TLS
│
└── Oracle Labs
    └── Doug Simon - Graal 编译器
```

### 团队统计

| 团队 | 人数 | 代表贡献者 | PR 总数 |
|------|------|------------|---------|
| **Java Platform Group** | 32 人 | Chen Liang, Jan Lahoda, Daniel Fuchs, Phil Race, Aggelos Biboudis | 2,800+ |
| **HotSpot Runtime Team** | 9 人 | Ioi Lam, Coleen Phillimore, Kim Barrett, Erik Gahlin, Chris Plummer | 1,505+ |
| **HotSpot GC Team** | 3 人 | Thomas Schatzl, Erik Österlund, Ivan Walulya | 558+ |
| **HotSpot Compiler Team** | 7 人 | Emanuel Peter, Christian Hagedorn, Marc Chevalier, Roberto Castaneda Lozano | 256+ |
| **Tools Team** | 2 人 | Alexey Semenyuk, Henry Jen | 233+ |
| **Java Engineering Infrastructure** | 4 人 | Magnus Ihse Bursie, Tim Bell, Igor Ignatev, Christian Stein | 28+ |
| **Security Team** | 2 人 | Weijun Wang, Sean Coffey | 15+ |
| **Oracle Labs** | 1 人 | Doug Simon | 10+ |
| **总计** | **59 人** | - | **5,700+** |

> **注**: 当前 Oracle 团队 58 人 + 已离职 (Hamlin Li) 1 人 = Top 贡献者列表 59 人

### Group Leads

| Group | Lead | 职责 | JEP 贡献 |
|-------|------|------|----------|
| **Client Libraries** | [Phil Race](../../by-contributor/profiles/phil-race.md) | Swing, Java 2D, AWT | JEP 504 |
| **Core Libraries** | [Alan Bateman](../../by-contributor/profiles/alan-bateman.md) | 核心库, Concurrency | JEP 499, 505, 525 |
| **Networking** | [Daniel Fuchs](../../by-contributor/profiles/daniel-fuchs.md) | HTTP Client, JMX | JEP 517 |
| **G1 GC** | [Thomas Schatzl](../../by-contributor/profiles/thomas-schatzl.md) | G1 GC, Parallel GC | JEP 522 |
| **C2 Compiler** | [Emanuel Peter](../../by-contributor/profiles/emanuel-peter.md) | SuperWord 向量化 | - |
| **LangTools** | [Jonathan Gibbons](../../by-contributor/profiles/jonathan-gibbons.md) | javac, javadoc | - |
| **Performance** | [Claes Redestad](../../by-contributor/profiles/claes-redestad.md) | 启动性能 | - |
| **JFR** | [Erik Gahlin](../../by-contributor/profiles/erik-gahlin.md) | Flight Recorder | JEP 520 |
| **CDS/AOT** | [Ioi Lam](../../by-contributor/profiles/ioi-lam.md) | Class Data Sharing | JEP 483, 514 |

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
| G1 GC | Ivan Walulya | - | [详情](../../by-contributor/profiles/ivan-walulya.md) |
| ZGC | Erik Österlund | JEP 490 | [详情](../../by-contributor/profiles/erik-osterlund.md) |

### 编译器

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| C2 编译器 | Emanuel Peter | - | [详情](../../by-contributor/profiles/emanuel-peter.md) |
| SuperWord 向量化 | Emanuel Peter | - | [详情](../../by-contributor/profiles/emanuel-peter.md) |
| C2 compiler | Christian Hagedorn | - | [详情](../../by-contributor/profiles/christian-hagedorn.md) |
| C2 compiler | Marc Chevalier | - | [详情](../../by-contributor/profiles/marc-chevalier.md) |
| C2 compiler | Benoit Maillard | - | [详情](../../by-contributor/profiles/benoit-maillard.md) |
| C2 compiler/IGV | Roberto Castaneda Lozano | - | [详情](../../by-contributor/profiles/roberto-castaneda-lozano.md) |
| C2 compiler/IGV | Tobias Holenstein | - | [详情](../../by-contributor/profiles/tobias-holenstein.md) |

### 核心库与性能

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| 启动性能 | Claes Redestad | - | [详情](../../by-contributor/profiles/claes-redestad.md) |
| ClassFile API | Chen Liang | JEP 484, 526 | [详情](../../by-contributor/profiles/chen-liang.md) |
| Stable Values | Per Minborg | JEP 502, 528 | [详情](../../by-contributor/profiles/per-minborg.md) |
| Stream Gatherers | Viktor Klang | JEP 485 | - |

### 语言特性

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| javac | Jan Lahoda | JEP 511, JEP 512 | [详情](../../by-contributor/profiles/jan-lahoda.md) |
| javadoc | Jonathan Gibbons | - | [详情](../../by-contributor/profiles/jonathan-gibbons.md) |
| javac/language features | Aggelos Biboudis | JEP 488, 507, 530 | [详情](../../by-contributor/profiles/aggelos-biboudis.md) |
| Flexible Constructor Bodies | Gavin Bierman | JEP 492, 513 | - |
| Nashorn/scripting | Sundararajan Athijegannathan | - | [详情](../../by-contributor/profiles/sundararajan-athijegannathan.md) |
| javadoc/Nashorn | Hannes Wallnoefer | - | [详情](../../by-contributor/profiles/hannes-wallnoefer.md) |
| javadoc/release eng | Nizar Ben Alla | - | [详情](../../by-contributor/profiles/nizar-ben-alla.md) |

### 构建系统

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| 构建系统 | Magnus Ihse Bursie | - | [详情](../../by-contributor/profiles/magnus-ihse-bursie.md) |
| build infrastructure | Tim Bell | - | [详情](../../by-contributor/profiles/tim-bell.md) |
| test infrastructure | Igor Ignatev | - | [详情](../../by-contributor/profiles/igor-ignatev.md) |
| JEP 458/jtreg | Christian Stein | - | [详情](../../by-contributor/profiles/christian-stein.md) |

### 桌面/客户端

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| Client Libraries | Phil Race | JEP 504 | [详情](../../by-contributor/profiles/phil-race.md) |
| Swing/AWT | Prasanta Sadhukhan | - | [详情](../../by-contributor/profiles/prasanta-sadhukhan.md) |
| 图形/打印 | Brian Burkhalter | - | [详情](../../by-contributor/profiles/brian-burkhalter.md) |
| AWT/Swing | Alexander Ivanov | - | [详情](../../by-contributor/profiles/alexander-ivanov.md) |
| AWT/Swing | Alexander Zuev | - | [详情](../../by-contributor/profiles/alexander-zuev.md) |
| AWT/Swing | Dmitry Markov | - | [详情](../../by-contributor/profiles/dmitry-markov.md) |

### 网络与 HTTP

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| HTTP/3 | Daniel Fuchs | JEP 517 | [详情](../../by-contributor/profiles/daniel-fuchs.md) |
| HTTP Client | Volkan Yazici | - | [详情](../../by-contributor/profiles/volkan-yazici.md) |
| networking | Patrick Concannon | - | [详情](../../by-contributor/profiles/patrick-concannon.md) |

### 并发与运行时

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| Structured Concurrency | Alan Bateman | JEP 499, 505, 525 | [详情](../../by-contributor/profiles/alan-bateman.md) |
| 并发 | David Holmes | - | [详情](../../by-contributor/profiles/david-holmes.md) |
| Atomic<T> | Kim Barrett | - | [详情](../../by-contributor/profiles/kim-barrett.md) |
| Virtual Threads | Ron Pressler | JEP 491 | - |

### 工具与监控

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| JFR | Erik Gahlin | JEP 520, JEP 349 | [详情](../../by-contributor/profiles/erik-gahlin.md) |
| JVMTI | Leonid Mesnik | - | [详情](../../by-contributor/profiles/leonid-mesnik.md) |
| JMX/JFR | Kevin Walls | - | [详情](../../by-contributor/profiles/kevin-walls.md) |
| serviceability/debugging | Chris Plummer | - | [详情](../../by-contributor/profiles/chris-plummer.md) |
| NMT/HotSpot diagnostics | Johan Sjolen | - | [详情](../../by-contributor/profiles/johan-sjolen.md) |
| Linux containers/runtime | Casper Norrbin | - | [详情](../../by-contributor/profiles/casper-norrbin.md) |

### 国际化

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| i18n | Naoto Sato | - | [详情](../../by-contributor/profiles/naoto-sato.md) |
| 本地化 | Justin Lu | - | [详情](../../by-contributor/profiles/justin-lu.md) |

### AOT 与 CDS

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| AOT/CDS | Ioi Lam | JEP 483, 514 | [详情](../../by-contributor/profiles/ioi-lam.md) |
| jpackage | Alexey Semenyuk | - | [详情](../../by-contributor/profiles/alexey-semenyuk.md) |
| CDS/AppCDS | Calvin Cheung | - | [详情](../../by-contributor/profiles/calvin-cheung.md) |
| CDS/AppCDS | Yumin Qi | - | [详情](../../by-contributor/profiles/yumin-qi.md) |
| jlink/native code | Henry Jen | JEP 493 | [详情](../../by-contributor/profiles/henry-jen.md) |
| XML/JAXP | Joe Wang | - | [详情](../../by-contributor/profiles/joe-wang.md) |
| math/AArch64 | Anton Artemov | - | [详情](../../by-contributor/profiles/anton-artemov.md) |

### 安全

| 领域 | 贡献者 | JEP | 档案 |
|------|--------|-----|------|
| Security, KDF | Weijun Wang | JEP 510 | [详情](../../by-contributor/profiles/weijun-wang.md) |
| security/TLS | Sean Coffey | - | [详情](../../by-contributor/profiles/sean-coffey.md) |
| Quantum-Resistant | - | JEP 496, 497 | - |

---

## 7. Oracle 主导的 JEP (JDK 24-26)

### JDK 26

| JEP | 标题 | Lead | 团队 | 状态 |
|-----|------|------|------|------|
| [JEP 520](https://openjdk.org/jeps/520) | JFR Method Timing and Tracing | Erik Gahlin | HotSpot Runtime | Targeted |
| [JEP 522](https://openjdk.org/jeps/522) | G1 GC Throughput Improvement | Thomas Schatzl | HotSpot GC | Targeted |
| [JEP 504](https://openjdk.org/jeps/504) | Remove Applet API | Phil Race | Client Libraries | Targeted |
| [JEP 525](https://openjdk.org/jeps/525) | Structured Concurrency (6th Preview) | Alan Bateman | Concurrency | Targeted |
| [JEP 526](https://openjdk.org/jeps/526) | Lazy Constants (2nd Preview) | Chen Liang | LangTools | Targeted |
| [JEP 528](https://openjdk.org/jeps/528) | Stable Values (2nd Preview) | Per Minborg | Core Libraries | Targeted |
| [JEP 529](https://openjdk.org/jeps/529) | Vector API (11th Incubator) | - | Core Libraries | Targeted |
| [JEP 530](https://openjdk.org/jeps/530) | Primitive Types in Patterns (4th Preview) | Aggelos Biboudis | LangTools | Targeted |
| [JEP 500](https://openjdk.org/jeps/500) | Prepare to Make Final Mean Final | Alan Bateman | Core Libraries | Targeted |
| [JEP 516](https://openjdk.org/jeps/516) | AOT Object Caching | Erik Österlund | HotSpot GC | Targeted |
| [JEP 524](https://openjdk.org/jeps/524) | PEM Encodings (2nd Preview) | Anthony Scarpino | Security | Targeted |

### JDK 25

| JEP | 标题 | Lead | 团队 | 状态 |
|-----|------|------|------|------|
| [JEP 517](https://openjdk.org/jeps/517) | HTTP/3 for HTTP Client | Daniel Fuchs | Core Libraries | Delivered |
| [JEP 514](https://openjdk.org/jeps/514) | AOT Command Line Ergonomics | Ioi Lam | HotSpot Runtime | Delivered |
| [JEP 511](https://openjdk.org/jeps/511) | Module Import Declarations | Jan Lahoda | LangTools | Delivered |
| [JEP 512](https://openjdk.org/jeps/512) | Compact Source Files and Instance Main Methods | Jan Lahoda | LangTools | Delivered |
| [JEP 513](https://openjdk.org/jeps/513) | Flexible Constructor Bodies | Gavin Bierman | LangTools | Delivered |
| [JEP 505](https://openjdk.org/jeps/505) | Structured Concurrency (5th Preview) | Alan Bateman | Concurrency | Delivered |
| [JEP 502](https://openjdk.org/jeps/502) | Stable Values (Preview) | Per Minborg | Core Libraries | Delivered |
| [JEP 507](https://openjdk.org/jeps/507) | Primitive Types in Patterns (3rd Preview) | Aggelos Biboudis | LangTools | Delivered |
| [JEP 508](https://openjdk.org/jeps/508) | Vector API (10th Incubator) | - | Core Libraries | Delivered |
| [JEP 510](https://openjdk.org/jeps/510) | Key Derivation Function API | Weijun Wang | Security | Delivered |
| [JEP 515](https://openjdk.org/jeps/515) | Ahead-of-Time Method Profiling | Igor Veresov | HotSpot Runtime | Delivered |
| [JEP 518](https://openjdk.org/jeps/518) | JFR Cooperative Sampling | Markus Grönlund | HotSpot Runtime | Delivered |
| [JEP 519](https://openjdk.org/jeps/519) | Compact Object Headers (Experimental) | Roman Kennke | HotSpot Runtime | Delivered |
| [JEP 470](https://openjdk.org/jeps/470) | PEM Encodings of Cryptographic Objects (Preview) | Anthony Scarpino | Security | Delivered |
| [JEP 503](https://openjdk.org/jeps/503) | Remove 32-bit x86 Port | Magnus Ihse Bursie | Infrastructure | Delivered |

### JDK 24

| JEP | 标题 | Lead | 团队 | 状态 |
|-----|------|------|------|------|
| [JEP 484](https://openjdk.org/jeps/484) | Class-File API | Chen Liang | LangTools | Delivered |
| [JEP 485](https://openjdk.org/jeps/485) | Stream Gatherers | Viktor Klang | Core Libraries | Delivered |
| [JEP 483](https://openjdk.org/jeps/483) | Ahead-of-Time Class Loading & Linking | Ioi Lam | HotSpot Runtime | Delivered |
| [JEP 486](https://openjdk.org/jeps/486) | Permanently Disable the Security Manager | Sean Mullan | Security | Delivered |
| [JEP 488](https://openjdk.org/jeps/488) | Primitive Types in Patterns (2nd Preview) | Aggelos Biboudis | LangTools | Delivered |
| [JEP 490](https://openjdk.org/jeps/490) | ZGC: Remove Non-Generational Mode | Erik Österlund | HotSpot GC | Delivered |
| [JEP 491](https://openjdk.org/jeps/491) | Synchronize Virtual Threads without Pinning | - | Concurrency | Delivered |
| [JEP 492](https://openjdk.org/jeps/492) | Flexible Constructor Bodies (3rd Preview) | Gavin Bierman | LangTools | Delivered |
| [JEP 493](https://openjdk.org/jeps/493) | Linking Run-Time Images without JMODs | Henry Jen | Tools | Delivered |
| [JEP 494](https://openjdk.org/jeps/494) | Module Import Declarations (2nd Preview) | Gavin Bierman | LangTools | Delivered |
| [JEP 495](https://openjdk.org/jeps/495) | Simple Source Files (4th Preview) | Gavin Bierman | LangTools | Delivered |
| [JEP 496](https://openjdk.org/jeps/496) | Quantum-Resistant Module-Lattice-Based KEM | - | Security | Delivered |
| [JEP 497](https://openjdk.org/jeps/497) | Quantum-Resistant Module-Lattice-Based DSA | - | Security | Delivered |
| [JEP 498](https://openjdk.org/jeps/498) | Warn upon Use of Memory-Access Methods in sun.misc.Unsafe | - | Core Libraries | Delivered |
| [JEP 499](https://openjdk.org/jeps/499) | Structured Concurrency (4th Preview) | Alan Bateman | Concurrency | Delivered |
| [JEP 501](https://openjdk.org/jeps/501) | Deprecate the 32-bit x86 Port for Removal | Magnus Ihse Bursie | Infrastructure | Delivered |
| [JEP 478](https://openjdk.org/jeps/478) | Key Derivation Function API (Preview) | Weijun Wang | Security | Delivered |

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

---

## 9. 贡献时间线

```
注: 2010-2019 年的贡献数据无法通过 GitHub PR 统计获取（OpenJDK 于 2020 年迁移至 GitHub）。
2020: ████████████████████████████████████████░░░░░░░░░░░░░░░░░░░░ 800+ PRs
2021: ████████████████████████████████████████░░░░░░░░░░░░░░░░░░░░ 800+ PRs
2022: █████████████████████████████████████████░░░░░░░░░░░░░░░░░░░ 850+ PRs
2023: ██████████████████████████████████████████░░░░░░░░░░░░░░░░░░ 900+ PRs
2024: ███████████████████████████████████████████░░░░░░░░░░░░░░░░░ 950+ PRs
2025: ████████████████████████████████████████████░░░░░░░░░░░░░░░░ 1000+ PRs
2026: ████████████████████████████████████████████░░░░░░░░░░░░░░░░ 500+ PRs (至今)
```

> **总计**: 12,000+ 贡献 (2010-2026, 其中 GitHub PR 始于 2020)

> **注**: Oracle 是 OpenJDK 的主要维护者，持续贡献占比约 70%

---

## 10. OpenJDK 治理参与

### OpenJDK Governing Board 成员

Oracle 在 OpenJDK Governing Board 中有代表席位：

| 代表 | 角色 | 任期 |
|------|------|------|
| Georges Saab | Chair | - |
| Phil Race | At-Large Member | 多届当选 |
| Mark Reinhold | Chief Architect | - |

### OpenJDK Project Leads

Oracle 贡献者担任多个关键 OpenJDK Project 的 Lead：

| Project | Lead | 说明 |
|---------|------|------|
| **JDK** | Mark Reinhold | JDK 主项目 |
| **Amber** | Brian Goetz | Java 语言演进 |
| **Loom** | Ron Pressler | 虚拟线程/结构化并发 |
| **Valhalla** | Brian Goetz | 值类型 |
| **Panama** | Maurizio Cimadamore | 外部函数与内存 API |
| **Leyden** | Mark Reinhold | 启动与预热优化 |
| **Lilliput** | Roman Kennke | 对象头压缩 |

### Group Leads

Oracle 贡献者担任以下 Group 的 Lead：

| Group | Lead | 职责 |
|-------|------|------|
| Client Libraries | Phil Race | Swing, Java 2D, AWT |
| Core Libraries | Alan Bateman (Lead) | 核心库 |
| HotSpot | - | JVM 运行时 |
| Security | Sean Mullan | 安全 |

### 新晋 Committer/Reviewer 提名

| 贡献者 | 时间 | 角色 | 提名人 | 领域 |
|--------|------|------|--------|------|
| Emanuel Peter | 2022-05 | JDK Committer | Tobias Hartmann | C2 Compiler |
| Claes Redestad | 2022-03 | OpenJDK Member | Daniel Fuchs | Performance |
| Emanuel Peter | 2023-05 | JDK Reviewer | Andrew Dinn | C2 Compiler |
| Coleen Phillimore | 2024-07 | Valhalla Committer | - | Valhalla |

---

## 11. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-23
- **数据来源**: [JDK 26 Top Contributors](../../by-contributor/profiles/jdk26-top-contributors.md)

---

## 12. 相关链接

- [Oracle Java](https://www.oracle.com/java/)
- [Oracle OpenJDK](https://openjdk.org/)
- [Oracle GitHub](https://github.com/oracle)
- [OpenJDK Census](https://openjdk.org/census)
- [OpenJDK Bylaws](https://openjdk.org/bylaws)
- [OpenJDK JEP Index](https://openjdk.org/jeps/0)
- [dev.java](https://dev.java/)

---

[← 返回组织索引](README.md)

---

> **文档版本**: 13.0
> **最后更新**: 2026-03-23
> **本次更新**:
> - **新增**: 22 位贡献者补充 GitHub handles (David Holmes, Brian Burkhalter, Volkan Yazici 等)
> - **新增**: Christian Hagedorn 加入 Top 贡献者表 (#24)
> - **新增**: Jaikiran Pai 加入亚洲团队 (India)
> - **修复**: 章节编号统一为 1-12，消除重复编号问题
> - **修复**: 目录与实际章节一一对应
> - **修复**: 贡献时间线中重复的 2020 年条目
> - **修复**: 合并底部重复的文档版本记录
> - **扩展**: JEP 章节从 7 个扩展至 40+ 个，覆盖 JDK 24/25/26 全部 Oracle 主导的 JEP
> - **新增**: OpenJDK Project Leads 表 (Amber, Loom, Valhalla, Panama, Leyden, Lilliput)
> - **新增**: OpenJDK Governing Board 补充 Georges Saab (Chair) 和 Mark Reinhold
> - **新增**: 顶部和底部导航链接
> - **新增**: 相关链接补充 OpenJDK Census, Bylaws, JEP Index, dev.java
> - **更新**: 按 PR 数量重新排序 Top 贡献者表
> - **更新**: 团队统计中 HotSpot Compiler 人数修正为 7 人 (加入 Christian Hagedorn)
