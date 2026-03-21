# 贡献者

了解 OpenJDK 贡献者和他们的工作。

> 💡 **提示**: 每个贡献者页面都包含活跃时间、职业时间线和贡献详情。
> 
> **角色说明**: 
> - **Reviewer** (评审者): 有权批准 PR 的资深贡献者，需经社区投票选举 ([OpenJDK Bylaws](https://openjdk.org/bylaws))
> - **Committer** (提交者): 有直接推送权限的贡献者 ([OpenJDK Guide](https://openjdk.org/guide/))
> - **Member** (成员): OpenJDK 社区成员
>
> **相关导航**: [按主题浏览](/by-topic/) · [按版本浏览](/by-version/) · [JEP 索引](/jeps/) · [OpenJDK Census](https://openjdk.org/census)

---
## 目录

1. [快速导航](#1-快速导航)
2. [浏览方式](#2-浏览方式)
3. [贡献者档案索引](#3-贡献者档案索引)
4. [顶级贡献者 (JDK 26)](#4-顶级贡献者-jdk-26)
5. [中国贡献者](#5-中国贡献者)
6. [相关 PR 分析文档](#6-相关-pr-分析文档)
7. [按 JDK 版本](#7-按-jdk-版本)
8. [贡献者统计](#8-贡献者统计)
9. [相关项目](#9-相关项目)

---


## 1. 快速导航

### 按活跃状态

| 状态 | 说明 | 代表贡献者 |
|------|------|------------|
| ✅ **活跃** | 2025-2026 有提交 | [Thomas Schatzl](/by-contributor/profiles/thomas-schatzl.md), [Phil Race](/by-contributor/profiles/phil-race.md), [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) |
| ⚠️ **减少参与** | 2022 年后减少 | [Thomas Wuerthinger](/by-contributor/profiles/thomas-wuerthinger.md) |

### 按主题领域

| 领域 | 代表贡献者 | Topic 页面 |
|------|------------|------------|
| [GC](/by-topic/core/gc/) | [Thomas Schatzl](/by-contributor/profiles/thomas-schatzl.md), [William Kemper](/by-contributor/profiles/william-kemper.md) | [GC 演进](/by-topic/core/gc/timeline.md) |
| [并发](/by-topic/concurrency/concurrency/) | [David Holmes](/by-contributor/profiles/david-holmes.md) | [并发编程](/by-topic/concurrency/concurrency/timeline.md) |
| [性能优化](/by-topic/core/performance/) | [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | [性能优化](/by-topic/core/performance/timeline.md) |
| [JFR](/by-topic/core/performance/) | [Erik Gahlin](/by-contributor/profiles/erik-gahlin.md) | [JFR 演进](/by-topic/core/performance/timeline.md) |
| [编译器](/by-topic/core/jit/) | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | [JIT 编译](/by-topic/core/jit/timeline.md) |
| [语言特性](/by-topic/language/) | [Jan Lahoda](/by-contributor/profiles/jan-lahoda.md), [Chen Liang](/by-contributor/profiles/chen-liang.md) | [语言演进](/by-topic/language/timeline.md) |
| [HTTP 客户端](/by-topic/concurrency/http/) | [Daniel Fuchs](/by-contributor/profiles/daniel-fuchs.md) | [HTTP 客户端](/by-topic/concurrency/http/timeline.md) |
| [国际化](/by-topic/security/i18n/) | [Naoto Sato](/by-contributor/profiles/naoto-sato.md) | [国际化](/by-topic/security/i18n/timeline.md) |

---

## 2. 浏览方式

### 按组织

#### Oracle

OpenJDK 的主要维护组织，涵盖全领域开发。

| 领域负责人 | 贡献者 | 查看 | Topic |
|-----------|--------|------|-------|
| Client Libraries Lead | [Phil Race](/by-contributor/profiles/phil-race.md) | [详情](/by-contributor/profiles/phil-race.md) | [→](/by-topic/api/) |
| Java Concurrency | [David Holmes](/by-contributor/profiles/david-holmes.md) | [详情](/by-contributor/profiles/david-holmes.md) | [→](/by-topic/concurrency/concurrency/) |
| C2 Compiler | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | [详情](/by-contributor/profiles/emanuel-peter.md) | [→](/by-topic/core/jit/) |
| JFR | [Erik Gahlin](/by-contributor/profiles/erik-gahlin.md) | [详情](/by-contributor/profiles/erik-gahlin.md) | [→](/by-topic/core/performance/) |
| javac | [Jan Lahoda](/by-contributor/profiles/jan-lahoda.md) | [详情](/by-contributor/profiles/jan-lahoda.md) | [→](/by-topic/language/syntax/) |
| i18n | [Naoto Sato](/by-contributor/profiles/naoto-sato.md) | [详情](/by-contributor/profiles/naoto-sato.md) | [→](/by-topic/security/i18n/) |
| 本地化 | [Justin Lu](/by-contributor/profiles/justin-lu.md) | [详情](/by-contributor/profiles/justin-lu.md) | [→](/by-topic/security/i18n/) |
| JVMTI | [Leonid Mesnik](/by-contributor/profiles/leonid-mesnik.md) | [详情](/by-contributor/profiles/leonid-mesnik.md) | [→](/by-topic/platform/) |
| ClassFile API | [Chen Liang](/by-contributor/profiles/chen-liang.md) | [详情](/by-contributor/profiles/chen-liang.md) | [→](/by-topic/language/classfile/) |
| C++ 现代化 | [Kim Barrett](/by-contributor/profiles/kim-barrett.md) | [详情](/by-contributor/profiles/kim-barrett.md) | [→](/by-topic/language/syntax/) |
| AOT/CDS | [Ioi Lam](/by-contributor/profiles/ioi-lam.md) | [详情](/by-contributor/profiles/ioi-lam.md) | [→](/by-topic/core/classloading/) |
| 构建系统 | [Magnus Ihse Bursie](/by-contributor/profiles/magnus-ihse-bursie.md) | [详情](/by-contributor/profiles/magnus-ihse-bursie.md) | [→](/by-topic/platform/) |
| Swing/AWT | [Prasanta Sadhukhan](/by-contributor/profiles/prasanta-sadhukhan.md) | [详情](/by-contributor/profiles/prasanta-sadhukhan.md) | [→](/by-topic/api/) |
| HTTP/3 | [Daniel Fuchs](/by-contributor/profiles/daniel-fuchs.md) | [详情](/by-contributor/profiles/daniel-fuchs.md) | [→](/by-topic/concurrency/http/) |

[→ Oracle 全部贡献者](/contributors/orgs/oracle.md)

#### Alibaba

| 贡献者 | 主要领域 | 查看 | Topic |
|--------|----------|------|-------|
| [Shaojin Wen (温绍锦)](/by-contributor/profiles/shaojin-wen.md) | 核心库优化 | [详情](/by-contributor/profiles/shaojin-wen.md) | [→](/by-topic/core/performance/) |
| [Fei Yang](/by-contributor/profiles/fei-yang.md) | RISC-V | [详情](/by-contributor/profiles/fei-yang.md) | [→](/by-topic/platform/) |
| [Albert Mingkun Yang](/by-contributor/profiles/albert-mingkun-yang.md) | GC | [详情](/by-contributor/profiles/albert-mingkun-yang.md) | [→](/by-topic/core/gc/) |

[→ Alibaba 全部贡献者](/contributors/orgs/alibaba.md)

#### Amazon

| 贡献者 | 主要领域 | 查看 | Topic |
|--------|----------|------|-------|
| [Andrew Dinn](/by-contributor/profiles/andrew-dinn.md) | AArch64 | [详情](/by-contributor/profiles/andrew-dinn.md) | [→](/by-topic/platform/) |
| [Nick Gasson](/by-contributor/profiles/nick-gasson.md) | AArch64 | [详情](/by-contributor/profiles/nick-gasson.md) | [→](/by-topic/platform/) |
| [David Beaumont](/by-contributor/profiles/david-beaumont.md) | 编译器 | [详情](/by-contributor/profiles/david-beaumont.md) | [→](/by-topic/core/jit/) |

[→ Amazon 全部贡献者](/contributors/orgs/amazon.md)

#### Red Hat

| 贡献者 | 主要领域 | 查看 | Topic |
|--------|----------|------|-------|
| Raffaello Giulietti | 核心库 | [OpenJDK Census](https://openjdk.org/census#rsgiulie) | - |
| [Roman Kennke](/by-contributor/profiles/roman-kennke.md) | Shenandoah GC | [详情](/by-contributor/profiles/roman-kennke.md) | [→](/by-topic/core/gc/) |
| [Andrew Dinn](/by-contributor/profiles/andrew-dinn.md) | AArch64 | [详情](/by-contributor/profiles/andrew-dinn.md) | [→](/by-topic/platform/) |

[→ Red Hat 全部贡献者](/contributors/orgs/redhat.md)

#### IBM

| 贡献者 | 主要领域 | 查看 | Topic |
|--------|----------|------|-------|
| [Goetz Lindenmaier](/by-contributor/profiles/goetz-lindenmaier.md) | HotSpot Runtime | [详情](/by-contributor/profiles/goetz-lindenmaier.md) | [→](/by-topic/core/) |
| [Thomas Stuefe](/by-contributor/profiles/thomas-stuefe.md) | HotSpot | [详情](/by-contributor/profiles/thomas-stuefe.md) | [→](/by-topic/core/) |
| [Amit Kumar](/by-contributor/profiles/amit-kumar.md) | s390x, Compiler | [详情](/by-contributor/profiles/amit-kumar.md) | [→](/by-topic/core/jit/) |

[→ IBM 全部贡献者](/contributors/orgs/ibm.md)

#### SAP

| 贡献者 | 主要领域 | 查看 | Topic |
|--------|----------|------|-------|
| [Matthias Baesken](/by-contributor/profiles/matthias-baesken.md) | 跨平台构建 | [详情](/by-contributor/profiles/matthias-baesken.md) | [→](/by-topic/platform/) |
| [Erik Joelsson](/by-contributor/profiles/erik-joelsson.md) | 构建系统 | [详情](/by-contributor/profiles/erik-joelsson.md) | [→](/by-topic/platform/) |

[→ SAP 全部贡献者](/contributors/orgs/sap.md)

#### Google

> ⚠️ Google 的 OpenJDK 贡献者信息需要核实。之前列出的贡献者实际在其他公司工作。

| 贡献者 | 实际组织 | 查看 |
|--------|----------|------|
| [Amit Kumar](/by-contributor/profiles/amit-kumar.md) | [IBM](/contributors/orgs/ibm.md) | [详情](/by-contributor/profiles/amit-kumar.md) |
| Christian Stein | Oracle | [OpenJDK Mail](https://mail.openjdk.org/pipermail/) |

[→ Google 全部贡献者](/contributors/orgs/google.md)

#### 其他组织

| 组织 | 贡献者 | 查看 |
|------|--------|------|
| [NTT DATA](/contributors/orgs/) | [Yasumasa Suenaga](/by-contributor/profiles/yasumasa-suenaga.md) | [详情](/by-contributor/profiles/yasumasa-suenaga.md) |
| [ByteDance](/contributors/orgs/bytedance.md) | [Anjian Wen](/by-contributor/profiles/anjian-wen.md) | [详情](/by-contributor/profiles/anjian-wen.md) |
| [DataDog](/contributors/orgs/) | [Jaroslav Bachorik](/by-contributor/profiles/jaroslav-bachorik.md) | [详情](/by-contributor/profiles/jaroslav-bachorik.md) |
| [Tencent](/contributors/orgs/tencent.md) | (无主要贡献者) | - |
| [ISCAS PLCT](/contributors/orgs/iscas-plct.md) | [Fei Yang](/by-contributor/profiles/fei-yang.md) | [详情](/by-contributor/profiles/fei-yang.md) |
| [龙芯](/contributors/orgs/loongson.md) | Zhang Xiaofeng, Liu Xinyu | [详情](/contributors/orgs/loongson.md) |

### 按地区

| 地区 | 贡献者 | 查看 |
|------|--------|------|
| 中国 | 20+ | [中国贡献者](/by-contributor/profiles/chinese-contributors.md) |
| 美国 | 50+ | [Oracle 贡献者](/contributors/orgs/oracle.md) |
| 欧洲 | 30+ | [Red Hat/SAP 贡献者](/contributors/orgs/redhat.md) |

### 按领域

> 💡 **提示**: 点击领域名称查看该技术主题的跨版本演进历程

#### 核心库与性能优化

| 领域 | 代表贡献者 | 查看 | Topic |
|------|------------|------|-------|
| 核心库优化 | Shaojin Wen | [详情](/by-contributor/profiles/shaojin-wen.md) | [→](/by-topic/core/performance/) |
| 启动性能 | Claes Redestad | [详情](/by-contributor/profiles/claes-redestad.md) | [→](/by-topic/core/performance/) |
| 性能优化 | Aleksey Shipilev | [详情](/by-contributor/profiles/aleksey-shipilev.md) | [→](/by-topic/core/performance/) |
| JIT 编译 | - | - | [→](/by-topic/core/jit/) |

#### 垃圾回收 (GC)

| 领域 | 代表贡献者 | 查看 | Topic |
|------|------------|------|-------|
| G1 GC | Thomas Schatzl | [详情](/by-contributor/profiles/thomas-schatzl.md) | [→](/by-topic/core/gc/) |
| Shenandoah GC | William Kemper | [详情](/by-contributor/profiles/william-kemper.md) | [→](/by-topic/core/gc/) |
| ZGC | Stefan Karlsson | [详情](/by-contributor/profiles/stefan-karlsson.md) | [→](/by-topic/core/gc/) |
| 内存管理 | - | - | [→](/by-topic/core/memory/) |

#### 网络与通信

| 领域 | 代表贡献者 | 查看 | Topic |
|------|------------|------|-------|
| HTTP/3 | Daniel Fuchs | [详情](/by-contributor/profiles/daniel-fuchs.md) | [→](/by-topic/concurrency/http/) |
| HttpClient | Volkan Yazıcı | [详情](/by-contributor/profiles/volkan-yazici.md) | [→](/by-topic/concurrency/http/) |
| 网络编程 | - | - | [→](/by-topic/concurrency/network/) |

#### 编译器与语言

| 领域 | 代表贡献者 | 查看 | Topic |
|------|------------|------|-------|
| ClassFile API | Chen Liang | [详情](/by-contributor/profiles/chen-liang.md) | [→](/by-topic/language/classfile/) |
| javac | Jan Lahoda | [详情](/by-contributor/profiles/jan-lahoda.md) | [→](/by-topic/language/syntax/) |
| C2 编译器 | Emanuel Peter | [详情](/by-contributor/profiles/emanuel-peter.md) | [→](/by-topic/core/jit/) |
| C++ 现代化 | Kim Barrett | [详情](/by-contributor/profiles/kim-barrett.md) | [→](/by-topic/language/syntax/) |
| 语言特性 | - | - | [→](/by-topic/language/) |

#### 工具与监控

| 领域 | 代表贡献者 | 查看 | Topic |
|------|------------|------|-------|
| JFR | Erik Gahlin | [详情](/by-contributor/profiles/erik-gahlin.md) | [→](/by-topic/core/performance/) |
| JFR 工具 | Jaroslav Bachorik | [详情](/by-contributor/profiles/jaroslav-bachorik.md) | [→](/by-topic/core/performance/) |
| JVMTI | Leonid Mesnik | [详情](/by-contributor/profiles/leonid-mesnik.md) | [→](/by-topic/platform/) |
| JMX | Claes Redestad | [详情](/by-contributor/profiles/claes-redestad.md) | [→](/by-topic/platform/) |

#### 国际化与客户端

| 领域 | 代表贡献者 | 查看 | Topic |
|------|------------|------|-------|
| i18n | Naoto Sato | [详情](/by-contributor/profiles/naoto-sato.md) | [→](/by-topic/security/i18n/) |
| 本地化 | Justin Lu | [详情](/by-contributor/profiles/justin-lu.md) | [→](/by-topic/security/i18n/) |
| Client Libraries | Phil Race | [详情](/by-contributor/profiles/phil-race.md) | [→](/by-topic/api/) |
| 图形/打印 | Brian Burkhalter | [详情](/by-contributor/profiles/brian-burkhalter.md) | [→](/by-topic/api/) |

#### 并发与运行时

| 领域 | 代表贡献者 | 查看 | Topic |
|------|------------|------|-------|
| 并发 | David Holmes | [详情](/by-contributor/profiles/david-holmes.md) | [→](/by-topic/concurrency/concurrency/) |
| 虚拟线程 | - | - | [→](/by-topic/concurrency/concurrency/) |
| AOT/CDS | Ioi Lam | [详情](/by-contributor/profiles/ioi-lam.md) | [→](/by-topic/core/classloading/) |
| 类加载器 | - | - | [→](/by-topic/core/classloading/) |

#### 构建系统

| 领域 | 代表贡献者 | 查看 | Topic |
|------|------------|------|-------|
| 构建系统 | Magnus Ihse Bursie | [详情](/by-contributor/profiles/magnus-ihse-bursie.md) | [→](/by-topic/platform/) |
| 跨平台 | Matthias Baesken | [详情](/by-contributor/profiles/matthias-baesken.md) | [→](/by-topic/platform/) |
| 容器支持 | - | - | [→](/by-topic/platform/containers/) |

#### UI 组件

| 领域 | 代表贡献者 | 查看 | Topic |
|------|------------|------|-------|
| Swing/AWT | Prasanta Sadhukhan | [详情](/by-contributor/profiles/prasanta-sadhukhan.md) | [→](/by-topic/api/) |

#### 安全与加密

| 领域 | 代表贡献者 | 查看 | Topic |
|------|------------|------|-------|
| 安全特性 | - | - | [→](/by-topic/security/security/) |
| TLS/SSL | - | - | [→](/by-topic/security/security/) |
| 后量子密码 | Ben Perez | [详情](/by-contributor/profiles/ben-perez.md) | [→](/by-topic/crypto/) |

#### 数学与计算

| 领域 | 代表贡献者 | 查看 | Topic |
|------|------------|------|-------|
| 数学库 | Joe Darcy | [详情](/by-contributor/profiles/joe-darcy.md) | [→](/by-topic/math/) |
| Vector API | - | - | [→](/by-topic/language/) |

#### 社区与生态

| 领域 | 代表贡献者 | 查看 | Topic |
|------|------------|------|-------|
| 日本社区 | Yasumasa Suenaga | [详情](/by-contributor/profiles/yasumasa-suenaga.md) | [→](/by-topic/security/i18n/) |
| 印度社区 | Jaikiran Pai | [详情](/by-contributor/profiles/jaikiran-pai.md) | [→](/by-topic/) |

---

## 3. 贡献者档案索引

### A-E

| 贡献者 | 组织 | 主要领域 | 档案 | Topic |
|--------|------|----------|------|-------|
| [Albert Mingkun Yang](/by-contributor/profiles/albert-mingkun-yang.md) | [Oracle](/contributors/orgs/oracle.md) | [GC](/by-topic/core/gc/) | [详情](/by-contributor/profiles/albert-mingkun-yang.md) | [→](/by-topic/core/gc/) |
| [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | [Amazon](/contributors/orgs/amazon.md) | [性能优化](/by-topic/core/performance/) | [详情](/by-contributor/profiles/aleksey-shipilev.md) | [→](/by-topic/core/performance/) |
| [Alexey Semenyuk](/by-contributor/profiles/alexey-semenyuk.md) | [Oracle](/contributors/orgs/oracle.md) | [编译器](/by-topic/core/jit/) | [详情](/by-contributor/profiles/alexey-semenyuk.md) | [→](/by-topic/core/jit/) |
| [Anjian Wen](/by-contributor/profiles/anjian-wen.md) | [ByteDance](/contributors/orgs/bytedance.md) | [RISC-V](/by-topic/platform/) | [详情](/by-contributor/profiles/anjian-wen.md) | [→](/by-topic/platform/) |
| [Ben Perez](/by-contributor/profiles/ben-perez.md) | Trail of Bits | [后量子密码学](/by-topic/crypto/) | [详情](/by-contributor/profiles/ben-perez.md) | [→](/by-topic/crypto/) |
| [Brian Burkhalter](/by-contributor/profiles/brian-burkhalter.md) | [Oracle](/contributors/orgs/oracle.md) | [图形/打印](/by-topic/api/) | [详情](/by-contributor/profiles/brian-burkhalter.md) | [→](/by-topic/api/) |
| [Chen Liang](/by-contributor/profiles/chen-liang.md) | [Oracle](/contributors/orgs/oracle.md) | [ClassFile API](/by-topic/language/classfile/) | [详情](/by-contributor/profiles/chen-liang.md) | [→](/by-topic/language/classfile/) |
| [Claes Redestad](/by-contributor/profiles/claes-redestad.md) | [Oracle](/contributors/orgs/oracle.md) | [性能优化](/by-topic/core/performance/) | [详情](/by-contributor/profiles/claes-redestad.md) | [→](/by-topic/core/performance/) |
| [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | [Oracle](/contributors/orgs/oracle.md) | [HotSpot](/by-topic/core/) | [详情](/by-contributor/profiles/coleen-phillimore.md) | [→](/by-topic/core/) |
| [Daniel Fuchs](/by-contributor/profiles/daniel-fuchs.md) | [Oracle](/contributors/orgs/oracle.md) | [HTTP/3](/by-topic/concurrency/http/) | [详情](/by-contributor/profiles/daniel-fuchs.md) | [→](/by-topic/concurrency/http/) |
| [David Holmes](/by-contributor/profiles/david-holmes.md) | [Oracle](/contributors/orgs/oracle.md) | [并发](/by-topic/concurrency/concurrency/) | [详情](/by-contributor/profiles/david-holmes.md) | [→](/by-topic/concurrency/concurrency/) |
| [Joe Darcy](/by-contributor/profiles/joe-darcy.md) | [Oracle](/contributors/orgs/oracle.md) | [数学库](/by-topic/math/) | [详情](/by-contributor/profiles/joe-darcy.md) | [→](/by-topic/math/) |

### F-J

| 贡献者 | 组织 | 主要领域 | 档案 | Topic |
|--------|------|----------|------|-------|
| [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | [Oracle](/contributors/orgs/oracle.md) | [C2 编译器](/by-topic/core/jit/) | [详情](/by-contributor/profiles/emanuel-peter.md) | [→](/by-topic/core/jit/) |
| [Erik Gahlin](/by-contributor/profiles/erik-gahlin.md) | [Oracle](/contributors/orgs/oracle.md) | [JFR](/by-topic/core/performance/) | [详情](/by-contributor/profiles/erik-gahlin.md) | [→](/by-topic/core/performance/) |
| [Fei Yang](/by-contributor/profiles/fei-yang.md) | [ISCAS PLCT](/contributors/orgs/iscas-plct.md) | [RISC-V](/by-topic/platform/) | [详情](/by-contributor/profiles/fei-yang.md) | [→](/by-topic/platform/) |
| Han Gq | - | - | [详情](/by-contributor/profiles/han-gq.md) | - |
| Hamlin Li | - | - | [详情](/by-contributor/profiles/hamlin-li.md) | - |
| [Ioi Lam](/by-contributor/profiles/ioi-lam.md) | [Oracle](/contributors/orgs/oracle.md) | [AOT/CDS](/by-topic/core/classloading/) | [详情](/by-contributor/profiles/ioi-lam.md) | [→](/by-topic/core/classloading/) |
| [Jaikiran Pai](/by-contributor/profiles/jaikiran-pai.md) | [Oracle](/contributors/orgs/oracle.md) | [JavaEE](/by-topic/api/) | [详情](/by-contributor/profiles/jaikiran-pai.md) | [→](/by-topic/api/) |
| [Jan Lahoda](/by-contributor/profiles/jan-lahoda.md) | [Oracle](/contributors/orgs/oracle.md) | [javac](/by-topic/language/syntax/) | [详情](/by-contributor/profiles/jan-lahoda.md) | [→](/by-topic/language/syntax/) |
| [Jaroslav Bachorik](/by-contributor/profiles/jaroslav-bachorik.md) | [DataDog](/contributors/orgs/) | [JFR 工具](/by-topic/core/performance/), BTrace | [详情](/by-contributor/profiles/jaroslav-bachorik.md) | [→](/by-topic/core/performance/) |
| [Jim Laskey](/by-contributor/profiles/jim-laskey.md) | [Oracle](/contributors/orgs/oracle.md) | [语言设计](/by-topic/language/) | [详情](/by-contributor/profiles/jim-laskey.md) | [→](/by-topic/language/) |
| [Johannes Graham](/by-contributor/profiles/johannes-graham.md) | [Oracle](/contributors/orgs/oracle.md) | [C2 编译器](/by-topic/core/jit/) | [详情](/by-contributor/profiles/johannes-graham.md) | [→](/by-topic/core/jit/) |
| [Justin Lu](/by-contributor/profiles/justin-lu.md) | [Oracle](/contributors/orgs/oracle.md) | [本地化](/by-topic/security/i18n/) | [详情](/by-contributor/profiles/justin-lu.md) | [→](/by-topic/security/i18n/) |

### K-O

| 贡献者 | 组织 | 主要领域 | 档案 | Topic |
|--------|------|----------|------|-------|
| [Kim Barrett](/by-contributor/profiles/kim-barrett.md) | [Oracle](/contributors/orgs/oracle.md) | [C++ 现代化](/by-topic/language/syntax/) | [详情](/by-contributor/profiles/kim-barrett.md) | [→](/by-topic/language/syntax/) |
| Kuai Wei | - | - | [详情](/by-contributor/profiles/kuai-wei.md) | - |
| [Leonid Mesnik](/by-contributor/profiles/leonid-mesnik.md) | [Oracle](/contributors/orgs/oracle.md) | [JVMTI](/by-topic/platform/) | [详情](/by-contributor/profiles/leonid-mesnik.md) | [→](/by-topic/platform/) |
| [Magnus Ihse Bursie](/by-contributor/profiles/magnus-ihse-bursie.md) | [Oracle](/contributors/orgs/oracle.md) | [构建系统](/by-topic/platform/) | [详情](/by-contributor/profiles/magnus-ihse-bursie.md) | [→](/by-topic/platform/) |
| [Matthias Baesken](/by-contributor/profiles/matthias-baesken.md) | [SAP](/contributors/orgs/sap.md) | [跨平台](/by-topic/platform/) | [详情](/by-contributor/profiles/matthias-baesken.md) | [→](/by-topic/platform/) |
| [Naoto Sato](/by-contributor/profiles/naoto-sato.md) | [Oracle](/contributors/orgs/oracle.md) | [i18n](/by-topic/security/i18n/) | [详情](/by-contributor/profiles/naoto-sato.md) | [→](/by-topic/security/i18n/) |

### P-Z

| 贡献者 | 组织 | 主要领域 | 档案 | Topic |
|--------|------|----------|------|-------|
| [Phil Race](/by-contributor/profiles/phil-race.md) | [Oracle](/contributors/orgs/oracle.md) | [Client Libraries](/by-topic/api/) | [详情](/by-contributor/profiles/phil-race.md) | [→](/by-topic/api/) |
| [Prasanta Sadhukhan](/by-contributor/profiles/prasanta-sadhukhan.md) | [Oracle](/contributors/orgs/oracle.md) | [Swing/AWT](/by-topic/api/) | [详情](/by-contributor/profiles/prasanta-sadhukhan.md) | [→](/by-topic/api/) |
| [Roger Riggs](/by-contributor/profiles/roger-riggs.md) | [Oracle](/contributors/orgs/oracle.md) | [核心库](/by-topic/core/) | [详情](/by-contributor/profiles/roger-riggs.md) | [→](/by-topic/core/) |
| [Sendaoyan](/by-contributor/profiles/sendaoyan.md) | Independent | [测试](/by-topic/) | [详情](/by-contributor/profiles/sendaoyan.md) | [→](/by-topic/) |
| [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | [Alibaba](/contributors/orgs/alibaba.md) | [核心库](/by-topic/core/) | [详情](/by-contributor/profiles/shaojin-wen.md) | [→](/by-topic/core/) |
| [Thomas Schatzl](/by-contributor/profiles/thomas-schatzl.md) | [Oracle](/contributors/orgs/oracle.md) | [G1 GC](/by-topic/core/gc/) | [详情](/by-contributor/profiles/thomas-schatzl.md) | [→](/by-topic/core/gc/) |
| Tongbao Zhang | - | - | [详情](/by-contributor/profiles/tongbao-zhang.md) | - |
| [Volkan Yazıcı](/by-contributor/profiles/volkan-yazici.md) | - | [HttpClient](/by-topic/concurrency/http/) | [详情](/by-contributor/profiles/volkan-yazici.md) | [→](/by-topic/concurrency/http/) |
| [William Kemper](/by-contributor/profiles/william-kemper.md) | [Amazon](/contributors/orgs/amazon.md) | [Shenandoah GC](/by-topic/core/gc/) | [详情](/by-contributor/profiles/william-kemper.md) | [→](/by-topic/core/gc/) |
| Xiaowei Lu | - | - | [详情](/by-contributor/profiles/xiaowei-lu.md) | - |
| [Yasumasa Suenaga](/by-contributor/profiles/yasumasa-suenaga.md) | [NTT DATA](/contributors/orgs/) | - | [详情](/by-contributor/profiles/yasumasa-suenaga.md) | - |
| Yude Lin | - | - | [详情](/by-contributor/profiles/yude-lin.md) | - |

---

## 4. 顶级贡献者

### OpenJDK Reviewer (评审者)

基于 [OpenJDK Census](https://openjdk.org/census) 的 Reviewer 名单，按领域分类。

#### GC (垃圾收集器)

| 贡献者 | 组织 | 领域 | Census | 档案 |
|--------|------|------|--------|------|
| [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | Amazon | Shenandoah GC, 性能优化 | [@shade](https://openjdk.org/census#shade) | [详情](/by-contributor/profiles/aleksey-shipilev.md) |
| [Thomas Schatzl](/by-contributor/profiles/thomas-schatzl.md) | Oracle | G1 GC | [@tschatzl](https://openjdk.org/census#tschatzl) | [详情](/by-contributor/profiles/thomas-schatzl.md) |
| [Albert Mingkun Yang](/by-contributor/profiles/albert-mingkun-yang.md) | Oracle | GC | [@ayoung](https://openjdk.org/census#ayoung) | [详情](/by-contributor/profiles/albert-mingkun-yang.md) |
| [William Kemper](/by-contributor/profiles/william-kemper.md) | Amazon | Shenandoah GC | [@wkemper](https://openjdk.org/census#wkemper) | [详情](/by-contributor/profiles/william-kemper.md) |
| [Roman Kennke](/by-contributor/profiles/roman-kennke.md) | Red Hat | Shenandoah GC, Compact Headers | [@rkennke](https://openjdk.org/census#rkennke) | [详情](/by-contributor/profiles/roman-kennke.md) |
| [Kim Barrett](/by-contributor/profiles/kim-barrett.md) | Oracle | GC, C++ 现代化 | [@kbarrett](https://openjdk.org/census#kbarrett) | [详情](/by-contributor/profiles/kim-barrett.md) |
| [Ioi Lam](/by-contributor/profiles/ioi-lam.md) | Oracle | CDS/AOT | [@iklam](https://openjdk.org/census#iklam) | [详情](/by-contributor/profiles/ioi-lam.md) |
| [Erik Gahlin](/by-contributor/profiles/erik-gahlin.md) | Oracle | JFR | [@egahlin](https://openjdk.org/census#egahlin) | [详情](/by-contributor/profiles/erik-gahlin.md) |

#### 编译器 (Compiler)

| 贡献者 | 组织 | 领域 | Census | 档案 |
|--------|------|------|--------|------|
| [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | Oracle | C2 编译器 | [@epeter](https://openjdk.org/census#epeter) | [详情](/by-contributor/profiles/emanuel-peter.md) |
| [Jan Lahoda](/by-contributor/profiles/jan-lahoda.md) | Oracle | javac | [@lahoda](https://openjdk.org/census#lahoda) | [详情](/by-contributor/profiles/jan-lahoda.md) |
| [Chen Liang](/by-contributor/profiles/chen-liang.md) | Oracle | ClassFile API | [@liach](https://openjdk.org/census#liach) | [详情](/by-contributor/profiles/chen-liang.md) |
| [Alexey Semenyuk](/by-contributor/profiles/alexey-semenyuk.md) | Oracle | AOT | [@ase menyuk](https://openjdk.org/census#asemenyuk) | [详情](/by-contributor/profiles/alexey-semenyuk.md) |
| [Roland Westrelin](/by-contributor/profiles/rooland-westrelin.md) | Oracle | C2 编译器 | [@roland](https://openjdk.org/census#roland) | [详情](/by-contributor/profiles/rooland-westrelin.md) |
| [Hamlin Li](/by-contributor/profiles/hamlin-li.md) | Oracle | C2 编译器 | [@hli](https://openjdk.org/census#hli) | [详情](/by-contributor/profiles/hamlin-li.md) |
| [Jatin Bhateja](/by-contributor/profiles/jatin-bhateja.md) | Oracle | Vector API | [@jbhateja](https://openjdk.org/census#jbhateja) | [详情](/by-contributor/profiles/jatin-bhateja.md) |

#### 并发与运行时 (Concurrency & Runtime)

| 贡献者 | 组织 | 领域 | Census | 档案 |
|--------|------|------|--------|------|
| [David Holmes](/by-contributor/profiles/david-holmes.md) | Oracle | 并发 | [@dholmes](https://openjdk.org/census#dholmes) | [详情](/by-contributor/profiles/david-holmes.md) |
| [Alan Bateman](/by-contributor/profiles/alan-bateman.md) | Oracle | 并发 | [@alanb](https://openjdk.org/census#alanb) | [详情](/by-contributor/profiles/alan-bateman.md) |
| [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | Oracle | HotSpot | [@coleenp](https://openjdk.org/census#coleenp) | [详情](/by-contributor/profiles/coleen-phillimore.md) |
| [Leonid Mesnik](/by-contributor/profiles/leonid-mesnik.md) | Oracle | JVMTI | [@lmesnik](https://openjdk.org/census#lmesnik) | [详情](/by-contributor/profiles/leonid-mesnik.md) |

#### 核心库 (Core Libraries)

| 贡献者 | 组织 | 领域 | Census | 档案 |
|--------|------|------|--------|------|
| [Phil Race](/by-contributor/profiles/phil-race.md) | Oracle | Client Libraries | [@prace](https://openjdk.org/census#prace) | [详情](/by-contributor/profiles/phil-race.md) |
| [Naoto Sato](/by-contributor/profiles/naoto-sato.md) | Oracle | 国际化 | [@naoto](https://openjdk.org/census#naoto) | [详情](/by-contributor/profiles/naoto-sato.md) |
| [Justin Lu](/by-contributor/profiles/justin-lu.md) | Oracle | 本地化 | [@jlu](https://openjdk.org/census#jlu) | [详情](/by-contributor/profiles/justin-lu.md) |
| [Brian Burkhalter](/by-contributor/profiles/brian-burkhalter.md) | Oracle | Networking | [@bpb](https://openjdk.org/census#bpb) | [详情](/by-contributor/profiles/brian-burkhalter.md) |
| [Daniel Fuchs](/by-contributor/profiles/daniel-fuchs.md) | Oracle | HTTP Client | [@dfuch](https://openjdk.org/census#dfuch) | [详情](/by-contributor/profiles/daniel-fuchs.md) |
| [Volkan Yazici](/by-contributor/profiles/volkan-yazici.md) | Oracle | HTTP Client | [@vyazici](https://openjdk.org/census#vyazici) | [详情](/by-contributor/profiles/volkan-yazici.md) |
| [Joe Darcy](/by-contributor/profiles/joe-darcy.md) | Oracle | 数学库 | [@darcy](https://openjdk.org/census#darcy) | [详情](/by-contributor/profiles/joe-darcy.md) |
| [Claes Redestad](/by-contributor/profiles/claes-redestad.md) | Oracle | 性能优化 | [@redestad](https://openjdk.org/census#redestad) | [详情](/by-contributor/profiles/claes-redestad.md) |
| [Stuart Marks](/by-contributor/profiles/stuart-marks.md) | Oracle | Core Libraries | [@smarks](https://openjdk.org/census#smarks) | [详情](/by-contributor/profiles/stuart-marks.md) |
| [Per Minborg](/by-contributor/profiles/per-minborg.md) | Oracle | Core Libraries | [@pminborg](https://openjdk.org/census#pminborg) | [详情](/by-contributor/profiles/per-minborg.md) |

#### 构建系统与工具 (Build & Tools)

| 贡献者 | 组织 | 领域 | Census | 档案 |
|--------|------|------|--------|------|
| [Magnus Ihse Bursie](/by-contributor/profiles/magnus-ihse-bursie.md) | Oracle | 构建系统 | [@ihse](https://openjdk.org/census#ihse) | [详情](/by-contributor/profiles/magnus-ihse-bursie.md) |
| [Matthias Baesken](/by-contributor/profiles/matthias-baesken.md) | Oracle | Build, Ports | [@mbaesken](https://openjdk.org/census#mbaesken) | [详情](/by-contributor/profiles/matthias-baesken.md) |
| [Jaikiran Pai](/by-contributor/profiles/jaikiran-pai.md) | Oracle | 构建系统 | [@jaikiran](https://openjdk.org/census#jaikiran) | [详情](/by-contributor/profiles/jaikiran-pai.md) |

#### 安全 (Security)

| 贡献者 | 组织 | 领域 | Census | 档案 |
|--------|------|------|--------|------|
| [Weijun Wang](/by-contributor/profiles/weijun-wang.md) | Oracle | 安全 | [@weijun](https://openjdk.org/census#weijun) | [详情](/by-contributor/profiles/weijun-wang.md) |
| [Anthony Scarpino](/by-contributor/profiles/anthony-scarpino.md) | Oracle | 安全 | [@ascarpino](https://openjdk.org/census#ascarpino) | [详情](/by-contributor/profiles/anthony-scarpino.md) |
| [Hai-May Chao](/by-contributor/profiles/hai-may-chao.md) | Oracle | 安全 | [@hmchao](https://openjdk.org/census#hmchao) | [详情](/by-contributor/profiles/hai-may-chao.md) |
| [Sean Mullan](/by-contributor/profiles/sean-mullan.md) | Oracle | 安全 | [@smullan](https://openjdk.org/census#smullan) | [详情](/by-contributor/profiles/sean-mullan.md) |
| [Xuelei Fan](/by-contributor/profiles/xuelei-fan.md) | Oracle | 安全 | [@xuelei](https://openjdk.org/census#xuelei) | [详情](/by-contributor/profiles/xuelei-fan.md) |

#### 桌面与 UI (Desktop & UI)

| 贡献者 | 组织 | 领域 | Census | 档案 |
|--------|------|------|--------|------|
| [Prasanta Sadhukhan](/by-contributor/profiles/prasanta-sadhukhan.md) | Oracle | Swing/AWT | [@psadhukhan](https://openjdk.org/census#psadhukhan) | [详情](/by-contributor/profiles/prasanta-sadhukhan.md) |
| [Sergey Bylokhov](/by-contributor/profiles/mrserb.md) | Oracle | AWT/2D | [@serb](https://openjdk.org/census#serb) | [详情](/by-contributor/profiles/mrserb.md) |

#### JFR (Java Flight Recorder)

| 贡献者 | 组织 | 领域 | Census | 档案 |
|--------|------|------|--------|------|
| [Markus Grönlund](/by-contributor/profiles/markus-gronlund.md) | Oracle | JFR | [@mgronlun](https://openjdk.org/census#mgronlun) | [详情](/by-contributor/profiles/markus-gronlund.md) |

#### AOT (Ahead-of-Time Compilation)

| 贡献者 | 组织 | 领域 | Census | 档案 |
|--------|------|------|--------|------|
| [Erik Österlund](/by-contributor/profiles/erik-osterlund.md) | Oracle | AOT | [@eosterlund](https://openjdk.org/census#eosterlund) | [详情](/by-contributor/profiles/erik-osterlund.md) |

---

### OpenJDK Committer (提交者)

基于 [OpenJDK Census](https://openjdk.org/census) 的 Committer 名单。

| 贡献者 | 组织 | 领域 | Census | 档案 |
|--------|------|------|--------|------|
| [Andrew Haley](/by-contributor/profiles/andrew-haley.md) | Red Hat | RISC-V | [@aph](https://openjdk.org/census#aph) | [详情](/by-contributor/profiles/andrew-haley.md) |
| [Fredrik Bredberg](/by-contributor/profiles/fredrik-bredberg.md) | Red Hat | Monitors | [@fredrik](https://openjdk.org/census#fredrik) | [详情](/by-contributor/profiles/fredrik-bredberg.md) |
| [Axel Boldt-Christmas](/by-contributor/profiles/axel-boldt-christmas.md) | SAP | ZGC | [@aboldtc](https://openjdk.org/census#aboldtc) | [详情](/by-contributor/profiles/axel-boldt-christmas.md) |
| [Johannes Bechberger](/by-contributor/profiles/johannes-bechberger.md) | SAP | JFR | [@jbechberger](https://openjdk.org/census#jbechberger) | [详情](/by-contributor/profiles/johannes-bechberger.md) |
| [Yasumasa Suenaga](/by-contributor/profiles/yasumasa-suenaga.md) | NTT DATA | Serviceability | [@suenaga](https://openjdk.org/census#suenaga) | [详情](/by-contributor/profiles/yasumasa-suenaga.md) |
| [Fei Yang](/by-contributor/profiles/fei-yang.md) | Alibaba | RISC-V | [@fyang](https://openjdk.org/census#fyang) | [详情](/by-contributor/profiles/fei-yang.md) |
| [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | Alibaba | 核心库 | [@swen](https://openjdk.org/census#swen) | [详情](/by-contributor/profiles/shaojin-wen.md) |
| [Anjian Wen](/by-contributor/profiles/anjian-wen.md) | ByteDance | RISC-V | [@awen](https://openjdk.org/census#awen) | [详情](/by-contributor/profiles/anjian-wen.md) |
| [Damon Nguyen](/by-contributor/profiles/damon-nguyen.md) | Oracle | Desktop | [@dnguyen](https://openjdk.org/census#dnguyen) | [详情](/by-contributor/profiles/damon-nguyen.md) |
| [Francesco Andreuzzi](/by-contributor/profiles/francesco-andreuzzi.md) | Oracle | 测试 | [@fandreuzzi](https://openjdk.org/census#fandreuzzi) | [详情](/by-contributor/profiles/francesco-andreuzzi.md) |
| [Manuel Hässig](/by-contributor/profiles/manuel-haessig.md) | Oracle | Testing | [@mhaessig](https://openjdk.org/census#mhaessig) | [详情](/by-contributor/profiles/manuel-haessig.md) |
| [SendaoYan](/by-contributor/profiles/sendaoyan.md) | Independent | 测试 | - | [详情](/by-contributor/profiles/sendaoyan.md) |

> **数据来源**: [OpenJDK Census](https://openjdk.org/census)
> 
> **说明**: 
> - Reviewer 和 Committer 需经社区投票选举产生
> - 完整名单请参考 [OpenJDK Census](https://openjdk.org/census)
> - 部分贡献者的 Census 账号待补充

---

### 历史累计 Top 50 (JDK 8-26)

基于 GitHub Integrated PRs 的历史累计贡献排名。

| 排名 | 贡献者 | 组织 | 累计 PRs | 领域 | 档案 |
|------|--------|------|----------|------|------|
| 1 | [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | [Amazon](/contributors/orgs/amazon.md) | 803 | Shenandoah GC, 性能优化 | [详情](/by-contributor/profiles/aleksey-shipilev.md) |
| 2 | [Albert Mingkun Yang](/by-contributor/profiles/albert-mingkun-yang.md) | [Oracle](/contributors/orgs/oracle.md) | 744 | GC | [详情](/by-contributor/profiles/albert-mingkun-yang.md) |
| 3 | [Thomas Schatzl](/by-contributor/profiles/thomas-schatzl.md) | [Oracle](/contributors/orgs/oracle.md) | 546 | G1 GC | [详情](/by-contributor/profiles/thomas-schatzl.md) |
| 4 | [Ioi Lam](/by-contributor/profiles/ioi-lam.md) | [Oracle](/contributors/orgs/oracle.md) | 431 | CDS/AOT | [详情](/by-contributor/profiles/ioi-lam.md) |
| 5 | [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | [Oracle](/contributors/orgs/oracle.md) | 400 | HotSpot | [详情](/by-contributor/profiles/coleen-phillimore.md) |
| 6 | [Jan Lahoda](/by-contributor/profiles/jan-lahoda.md) | [Oracle](/contributors/orgs/oracle.md) | 324 | javac | [详情](/by-contributor/profiles/jan-lahoda.md) |
| 7 | [Jaikiran Pai](/by-contributor/profiles/jaikiran-pai.md) | [Oracle](/contributors/orgs/oracle.md) | 322 | 构建系统 | [详情](/by-contributor/profiles/jaikiran-pai.md) |
| 8 | [Naoto Sato](/by-contributor/profiles/naoto-sato.md) | [Oracle](/contributors/orgs/oracle.md) | 273 | 国际化 | [详情](/by-contributor/profiles/naoto-sato.md) |
| 9 | [Sergey Bylokhov](/by-contributor/profiles/mrserb.md) | [Oracle](/contributors/orgs/oracle.md) | 273 | AWT/2D | [详情](/by-contributor/profiles/mrserb.md) |
| 10 | [Chen Liang](/by-contributor/profiles/chen-liang.md) | [Oracle](/contributors/orgs/oracle.md) | 237 | ClassFile API | [详情](/by-contributor/profiles/chen-liang.md) |
| 11 | [Alexey Semenyuk](/by-contributor/profiles/alexey-semenyuk.md) | [Oracle](/contributors/orgs/oracle.md) | 233 | AOT | [详情](/by-contributor/profiles/alexey-semenyuk.md) |
| 12 | [SendaoYan](/by-contributor/profiles/sendaoyan.md) | Independent | 202 | 测试 | [详情](/by-contributor/profiles/sendaoyan.md) |
| 13 | [Daniel Fuchs](/by-contributor/profiles/daniel-fuchs.md) | [Oracle](/contributors/orgs/oracle.md) | 192 | HTTP Client | [详情](/by-contributor/profiles/daniel-fuchs.md) |
| 14 | [Kim Barrett](/by-contributor/profiles/kim-barrett.md) | [Oracle](/contributors/orgs/oracle.md) | 180+ | GC, C++ 现代化 | [详情](/by-contributor/profiles/kim-barrett.md) |
| 15 | [Erik Gahlin](/by-contributor/profiles/erik-gahlin.md) | [Oracle](/contributors/orgs/oracle.md) | 170+ | JFR | [详情](/by-contributor/profiles/erik-gahlin.md) |
| 16 | [Phil Race](/by-contributor/profiles/phil-race.md) | [Oracle](/contributors/orgs/oracle.md) | 160+ | Client Libraries | [详情](/by-contributor/profiles/phil-race.md) |
| 17 | [Brian Burkhalter](/by-contributor/profiles/brian-burkhalter.md) | [Oracle](/contributors/orgs/oracle.md) | 150+ | Networking | [详情](/by-contributor/profiles/brian-burkhalter.md) |
| 18 | [David Holmes](/by-contributor/profiles/david-holmes.md) | [Oracle](/contributors/orgs/oracle.md) | 140+ | 并发 | [详情](/by-contributor/profiles/david-holmes.md) |
| 19 | [Matthias Baesken](/by-contributor/profiles/matthias-baesken.md) | [Oracle](/contributors/orgs/oracle.md) | 130+ | Build | [详情](/by-contributor/profiles/matthias-baesken.md) |
| 20 | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | [Oracle](/contributors/orgs/oracle.md) | 120+ | C2 编译器 | [详情](/by-contributor/profiles/emanuel-peter.md) |
| 21 | [William Kemper](/by-contributor/profiles/william-kemper.md) | [Amazon](/contributors/orgs/amazon.md) | 123 | Shenandoah GC | [详情](/by-contributor/profiles/william-kemper.md) |
| 22 | [Roman Kennke](/by-contributor/profiles/roman-kennke.md) | [Red Hat](/contributors/orgs/redhat.md) | 100+ | Compact Object Headers | [详情](/by-contributor/profiles/roman-kennke.md) |
| 23 | [Justin Lu](/by-contributor/profiles/justin-lu.md) | [Oracle](/contributors/orgs/oracle.md) | 100+ | 本地化 | [详情](/by-contributor/profiles/justin-lu.md) |
| 24 | [Fei Yang](/by-contributor/profiles/fei-yang.md) | [Alibaba](/contributors/orgs/alibaba.md) | 100 | RISC-V | [详情](/by-contributor/profiles/fei-yang.md) |
| 25 | [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | [Alibaba](/contributors/orgs/alibaba.md) | 97 | 核心库 | [详情](/by-contributor/profiles/shaojin-wen.md) |
| 26 | [Magnus Ihse Bursie](/by-contributor/profiles/magnus-ihse-bursie.md) | [Oracle](/contributors/orgs/oracle.md) | 90+ | Build | [详情](/by-contributor/profiles/magnus-ihse-bursie.md) |
| 27 | [Leonid Mesnik](/by-contributor/profiles/leonid-mesnik.md) | [Oracle](/contributors/orgs/oracle.md) | 80+ | JVMTI | [详情](/by-contributor/profiles/leonid-mesnik.md) |
| 28 | [Volkan Yazici](/by-contributor/profiles/volkan-yazici.md) | [Oracle](/contributors/orgs/oracle.md) | 80+ | HTTP Client | [详情](/by-contributor/profiles/volkan-yazici.md) |
| 29 | [Yasumasa Suenaga](/by-contributor/profiles/yasumasa-suenaga.md) | NTT DATA | 80+ | Serviceability | [详情](/by-contributor/profiles/yasumasa-suenaga.md) |
| 30 | [Prasanta Sadhukhan](/by-contributor/profiles/prasanta-sadhukhan.md) | [Oracle](/contributors/orgs/oracle.md) | 70+ | Swing/AWT | [详情](/by-contributor/profiles/prasanta-sadhukhan.md) |
| 31 | [Claes Redestad](/by-contributor/profiles/claes-redestad.md) | [Oracle](/contributors/orgs/oracle.md) | 70+ | 性能优化 | [详情](/by-contributor/profiles/claes-redestad.md) |
| 32 | [Joe Darcy](/by-contributor/profiles/joe-darcy.md) | [Oracle](/contributors/orgs/oracle.md) | 70+ | 数学库 | [详情](/by-contributor/profiles/joe-darcy.md) |
| 33 | [Andrew Haley](/by-contributor/profiles/andrew-haley.md) | [Red Hat](/contributors/orgs/redhat.md) | 60+ | RISC-V | [详情](/by-contributor/profiles/andrew-haley.md) |
| 34 | [Axel Boldt-Christmas](/by-contributor/profiles/axel-boldt-christmas.md) | [SAP](/contributors/orgs/sap.md) | 60+ | ZGC | [详情](/by-contributor/profiles/axel-boldt-christmas.md) |
| 35 | [Francesco Andreuzzi](/by-contributor/profiles/francesco-andreuzzi.md) | [Oracle](/contributors/orgs/oracle.md) | 60+ | 测试 | [详情](/by-contributor/profiles/francesco-andreuzzi.md) |
| 36 | [Johannes Bechberger](/by-contributor/profiles/johannes-bechberger.md) | [SAP](/contributors/orgs/sap.md) | 50+ | JFR | [详情](/by-contributor/profiles/johannes-bechberger.md) |
| 37 | [Weijun Wang](/by-contributor/profiles/weijun-wang.md) | [Oracle](/contributors/orgs/oracle.md) | 50+ | 安全 | [详情](/by-contributor/profiles/weijun-wang.md) |
| 38 | [Jatin Bhateja](/by-contributor/profiles/jatin-bhateja.md) | [Oracle](/contributors/orgs/oracle.md) | 50+ | Vector API | [详情](/by-contributor/profiles/jatin-bhateja.md) |
| 39 | [Hamlin Li](/by-contributor/profiles/hamlin-li.md) | [Oracle](/contributors/orgs/oracle.md) | 50+ | C2 编译器 | [详情](/by-contributor/profiles/hamlin-li.md) |
| 40 | [Anjian Wen](/by-contributor/profiles/anjian-wen.md) | [ByteDance](/contributors/orgs/bytedance.md) | 25 | RISC-V | [详情](/by-contributor/profiles/anjian-wen.md) |
| 41 | [Roland Westrelin](/by-contributor/profiles/rooland-westrelin.md) | [Oracle](/contributors/orgs/oracle.md) | 40+ | C2 编译器 | [详情](/by-contributor/profiles/rooland-westrelin.md) |
| 42 | [Alan Bateman](/by-contributor/profiles/alan-bateman.md) | [Oracle](/contributors/orgs/oracle.md) | 40+ | 并发 | [详情](/by-contributor/profiles/alan-bateman.md) |
| 43 | [Per Minborg](/by-contributor/profiles/per-minborg.md) | [Oracle](/contributors/orgs/oracle.md) | 40+ | Core Libraries | [详情](/by-contributor/profiles/per-minborg.md) |
| 44 | [Markus Grönlund](/by-contributor/profiles/markus-gronlund.md) | [Oracle](/contributors/orgs/oracle.md) | 40+ | JFR | [详情](/by-contributor/profiles/markus-gronlund.md) |
| 45 | [Damon Nguyen](/by-contributor/profiles/damon-nguyen.md) | [Oracle](/contributors/orgs/oracle.md) | 30+ | Desktop | [详情](/by-contributor/profiles/damon-nguyen.md) |
| 46 | [Anthony Scarpino](/by-contributor/profiles/anthony-scarpino.md) | [Oracle](/contributors/orgs/oracle.md) | 30+ | 安全 | [详情](/by-contributor/profiles/anthony-scarpino.md) |
| 47 | [Erik Österlund](/by-contributor/profiles/erik-osterlund.md) | [Oracle](/contributors/orgs/oracle.md) | 30+ | AOT | [详情](/by-contributor/profiles/erik-osterlund.md) |
| 48 | [Hai-May Chao](/by-contributor/profiles/hai-may-chao.md) | [Oracle](/contributors/orgs/oracle.md) | 30+ | 安全 | [详情](/by-contributor/profiles/hai-may-chao.md) |
| 49 | [Stuart Marks](/by-contributor/profiles/stuart-marks.md) | [Oracle](/contributors/orgs/oracle.md) | 30+ | Core Libraries | [详情](/by-contributor/profiles/stuart-marks.md) |
| 50 | [Yude Lin](/by-contributor/profiles/yude-lin.md) | [Alibaba](/contributors/orgs/alibaba.md) | 20+ | 编译器 | [详情](/by-contributor/profiles/yude-lin.md) |

> **数据来源**: [GitHub Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+is%3Aclosed+label%3Aintegrated)
> 
> **说明**: 
> - 统计周期：JDK 8 (2014) 至 JDK 26 (2026)
> - 仅统计标记为 `integrated` 的 PR
> - 部分资深贡献者的 PR 数基于 OpenJDK Census 估算

→ [查看完整历史贡献者列表](/contributors/orgs/index.md)

---

### JDK 26 周期 Top 50 (2025-06 to 2026-03)

JDK 26 开发周期内的贡献者排名。

| 排名 | 贡献者 | 组织 | PRs | 领域 | 档案 |
|------|--------|------|-----|------|------|
| 1 | [Thomas Schatzl](/by-contributor/profiles/thomas-schatzl.md) | [Oracle](/contributors/orgs/oracle.md) | 140 | G1 GC | [详情](/by-contributor/profiles/thomas-schatzl.md) |
| 2 | [Albert Mingkun Yang](/by-contributor/profiles/albert-mingkun-yang.md) | [Oracle](/contributors/orgs/oracle.md) | 136 | GC | [详情](/by-contributor/profiles/albert-mingkun-yang.md) |
| 3 | [Phil Race](/by-contributor/profiles/phil-race.md) | [Oracle](/contributors/orgs/oracle.md) | 110 | Printing, Desktop | [详情](/by-contributor/profiles/phil-race.md) |
| 4 | [Matthias Baesken](/by-contributor/profiles/matthias-baesken.md) | [Oracle](/contributors/orgs/oracle.md) | 105 | Build, Ports | [详情](/by-contributor/profiles/matthias-baesken.md) |
| 5 | [Alexey Semenyuk](/by-contributor/profiles/alexey-semenyuk.md) | [Oracle](/contributors/orgs/oracle.md) | 85 | jpackage | [详情](/by-contributor/profiles/alexey-semenyuk.md) |
| 6 | [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | [Amazon](/contributors/orgs/amazon.md) | 80 | Shenandoah, Performance | [详情](/by-contributor/profiles/aleksey-shipilev.md) |
| 7 | [Ioi Lam](/by-contributor/profiles/ioi-lam.md) | [Oracle](/contributors/orgs/oracle.md) | 76 | CDS, AOT | [详情](/by-contributor/profiles/ioi-lam.md) |
| 8 | [Kim Barrett](/by-contributor/profiles/kim-barrett.md) | [Oracle](/contributors/orgs/oracle.md) | 76 | GC, HotSpot | [详情](/by-contributor/profiles/kim-barrett.md) |
| 9 | [SendaoYan](/by-contributor/profiles/sendaoyan.md) | Independent | 71 | Testing | [详情](/by-contributor/profiles/sendaoyan.md) |
| 10 | [Jaikiran Pai](/by-contributor/profiles/jaikiran-pai.md) | [Oracle](/contributors/orgs/oracle.md) | 67 | Networking | [详情](/by-contributor/profiles/jaikiran-pai.md) |

> **数据来源**: [GitHub Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+is%3Aclosed+label%3Aintegrated)
> 
> **说明**: 
> - 统计周期：2025-06 至 2026-03 (JDK 26 开发周期)
> - 仅统计标记为 `integrated` 的 PR
> - [查看完整 JDK 26 Top 100 榜单](/by-contributor/profiles/jdk26-top-contributors.md)

→ [查看 JDK 26 完整 Top 100 榜单](/by-contributor/profiles/jdk26-top-contributors.md)

---

## 5. 中国贡献者

历史上对 OpenJDK 有重要贡献的中国开发者（累计 PRs）。

| 贡献者 | 组织 | 累计 PRs | 领域 | 档案 |
|--------|------|----------|------|------|
| [Shaojin Wen (温绍锦)](/by-contributor/profiles/shaojin-wen.md) | [Alibaba](/contributors/orgs/alibaba.md) | 97 | 核心库优化 | [详情](/by-contributor/profiles/shaojin-wen.md) |
| [Fei Yang](/by-contributor/profiles/fei-yang.md) | [ISCAS PLCT](/contributors/orgs/iscas-plct.md) | 30 | RISC-V | [详情](/by-contributor/profiles/fei-yang.md) |
| [Anjian Wen](/by-contributor/profiles/anjian-wen.md) | [ByteDance](/contributors/orgs/bytedance.md) | 25 | RISC-V | [详情](/by-contributor/profiles/anjian-wen.md) |
| [Sendaoyan](/by-contributor/profiles/sendaoyan.md) | Independent | 202 | 测试 | [详情](/by-contributor/profiles/sendaoyan.md) |

> **注意**: JDK 26 周期中国贡献者数据见上方 [中国贡献者 (JDK 26)](#4-顶级贡献者-jdk-26) 部分。
>
> → [查看完整中国贡献者专题](/by-contributor/profiles/chinese-contributors.md)

---

## 6. 相关 PR 分析文档

### 核心库优化

| 贡献者 | PR 分析文档 |
|--------|-----------|
| Shaojin Wen | [String "+" 优化](/by-pr/8336/8336856.md) |
| Claes Redestad | [字符串拼接优化](/by-pr/8335/8335182.md) |
| Claes Redestad | [C2 内存修复](/by-pr/8327/8327247.md) |
| Claes Redestad | [字节码生成优化](/by-pr/8339/8339799.md) |
| Claes Redestad | [HexFormat 优化](/by-pr/8335/8335802.md) |
| Chen Liang | [反射 API 性能优化](/by-pr/8371/8371953.md) |
| Roger Riggs | [StringBuilder 健壮性](/by-pr/8351/8351443.md) |
| [Raffaello Giulietti](/by-contributor/profiles/raffaello-giulietti.md) | [Independent](https://openjdk.org/census#rsgiulie) | [核心库，数学库](/by-topic/core/) | [详情](/by-contributor/profiles/raffaello-giulietti.md) | [→](/by-topic/core/) |

### 编译器优化

| 贡献者 | PR 分析文档 |
|--------|-----------|
| Emanuel Peter | [Store-to-Load 转发修复](/by-pr/8333/8334431.md) |
| Emanuel Peter | [小循环向量化](/by-pr/8344/8344085.md) |
| Emanuel Peter | SuperWord Cost Model (待补充) |
| Emanuel Peter | 模板测试框架 (待补充) |
| Johannes Graham | [XOR 常量折叠](/by-pr/8347/8347645.md) |

### 数学库与密码学

| 贡献者 | PR 分析文档 |
|--------|-----------|
| Joe Darcy | [FDLIBM @Stable](/by-pr/8362/8362376.md) |
| Ben Perez | [ML-KEM 优化](/by-pr/8347/8347608.md) |

### ClassFile API

| 贡献者 | PR 分析文档 |
|--------|-----------|
| Chen Liang | 移除 com.sun.tools.classfile (待补充) |
| Chen Liang | UTF-8 条目验证 (待补充) |

### JVM 运行时

| 贡献者 | PR 分析文档 |
|--------|-----------|
| Kim Barrett | Atomic<T> 模板 (待补充) |
| David Holmes | 信号处理安全 (待补充) |
| Leonid Mesnik | JVMTI 压力测试 (待补充) |
| William Kemper | 分代 Shenandoah (待补充) |

[→ 全部 PR 分析文档](/by-pr/)

---

## 7. 按 JDK 版本

### JDK 26 (2025-2026)

已发布版本 (GA 2026-03-17)。

| 查看 | 说明 |
|------|------|
| [Top 100 贡献者](/by-contributor/profiles/jdk26-top-contributors.md) | 完整贡献者列表 |
| **顶级贡献者** | Thomas Schatzl, Albert Mingkun Yang, Phil Race |
| **主要组织** | Oracle (75%), Red Hat (8%), Alibaba (3%) |

### JDK 25 (2024-2025)

JDK 26 的前身版本。

| 查看 | 说明 |
|------|------|
| [Top 50 贡献者](/by-contributor/profiles/jdk25-top-contributors.md) | 完整贡献者列表 |
| **顶级贡献者** | Thomas Schatzl, Albert Mingkun Yang, Phil Race |
| **关键特性** | Compact Object Headers, Generational Shenandoah |

### JDK 8 (LTS)

长期支持版本，2014 年发布，至今仍在广泛使用。

| 查看 | 说明 |
|------|------|
| [历史贡献者](/by-contributor/profiles/jdk8-top-contributors.md) | JDK 8 贡献者历史 |
| **原始作者** | Brian Goetz (Lambda), Paul Sandoz (Streams) |
| **长期维护者** | David Holmes, Coleen Phillimore, Kim Barrett |

### 其他版本

| 版本 | GA 时间 | 说明 | 贡献者页面 |
|------|---------|------|------------|
| JDK 21 (LTS) | 2023-09 | Virtual Threads, Pattern Matching, Sequenced Collections | [Top Contributors](/by-contributor/profiles/jdk21-top-contributors.md) |
| JDK 17 (LTS) | 2021-09 | Sealed Classes, macOS/AArch64, ZGC Improvements | [Top Contributors](/by-contributor/profiles/jdk17-top-contributors.md) |
| JDK 11 (LTS) | 2018-09 | HTTP Client, Local Variable Syntax, ZGC (Experimental) | [Top Contributors](/by-contributor/profiles/jdk11-top-contributors.md) |

---

## 8. 贡献者统计

**统计原则**: 使用 GitHub Integrated PRs 作为唯一指标

详见 [贡献者统计原则](/AGENTS.md#contribution-statistics-principles)

---

## 9. 相关项目

### GraalVM 团队

GraalVM 是一个独立的 JDK 发行版，与 OpenJDK 有密切关系但属于不同项目。

| 贡献者 | 活跃时间 | 状态 | 档案 |
|--------|----------|------|------|
| Doug Simon | 2012–至今 | ✅ | [详情](/by-contributor/profiles/doug-simon.md) |
| Thomas Wuerthinger | 2010–至今 | ⚠️ | [详情](/by-contributor/profiles/thomas-wuerthinger.md) |
| Christian Wimmer | 2011–至今 | ✅ | [详情](/by-contributor/profiles/christian-wimmer.md) |
| Gilles Duboscq | 2012–至今 | ✅ | [详情](/by-contributor/profiles/gilles-duboscq.md) |
| Tom Rodriguez | 2010–至今 | ✅ | [详情](/by-contributor/profiles/tom-rodriguez.md) |

> **注**: GraalVM 贡献者主要贡献到 GraalVM 项目，部分也会贡献到 OpenJDK 上游。
