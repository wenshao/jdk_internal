# OpenJDK 贡献组织

[← 返回贡献者索引](../../by-contributor/README.md)

---
## 目录

1. [概览](#1-概览)
2. [按专业领域](#2-按专业领域)
3. [按 JDK 版本贡献](#3-按-jdk-版本贡献)
4. [贡献趋势](#4-贡献趋势)
5. [组织发行版](#5-组织发行版)
6. [JEP 主导组织](#6-jep-主导组织)
7. [组织特点](#7-组织特点)
8. [贡献者流动](#8-贡献者流动)
9. [地区分布](#9-地区分布)
10. [数据来源](#10-数据来源)
11. [相关链接](#11-相关链接)

---


## 1. 概览

OpenJDK 是一个由多个组织共同维护的开源项目。本文档汇总了各主要贡献组织的工作领域、版本贡献和专业方向。

| 组织 | Integrated PRs | Reviewer | Committer | Author | 主要领域 | JDK 发行版 |
|------|----------------|----------|-----------|--------|----------|------------|
| [Oracle](oracle.md) | 4,200+ | 30+ | 20+ | - | 全领域 | Oracle JDK |
| [Amazon](amazon.md) | 1,048+ | 1 | 4 | 1 | Shenandoah GC, C2, Runtime | Corretto |
| [SAP](sap.md) | 851+ | 3 | 4 | - | PPC, AIX, 构建 | SapMachine |
| [Red Hat](redhat.md) | 649+ | 4 | - | - | C2 编译器, HotSpot Runtime | Red Hat OpenJDK |
| [Alibaba](alibaba.md) | 448 | - | 5 | 6 | 核心库, C2, GC, Runtime | Dragonwell |
| [IBM](ibm.md) | 239+ | 2 | 2 | - | s390x, 容器/cgroup, AArch64 | Semeru |
| [Tencent](tencent.md) | 228+ | 2 | - | 2 | 构建稳定性, 编译器, GC, 安全 | Kona |
| [Intel](intel.md) | 146+ | 1 | - | 1 | Vector API, x86_64, SuperWord | - |
| [ARM](arm.md) | 31+ | 1 | - | 1 | AArch64, Build | - |
| [Loongson](loongson.md) | 36+ | - | 1 | 2 | LoongArch | Loongson JDK |
| [ByteDance](bytedance.md) | 25 | - | 1 | - | RISC-V 向量 | - |
| [ISCAS PLCT](iscas-plct.md) | 64+ | - | 1 | 1 | RISC-V, 核心库 | - |
| [Huawei](huawei.md) | 167+ | 1 | 2 | - | RISC-V Port (JEP 422), AArch64 | BiSheng JDK |
| [BellSoft](bellsoft.md) | 40+ | - | 1 | - | ARM32, AArch64, RISC-V | Liberica JDK |
| [Azul](azul.md) | 18+ | - | 1 | - | CRaC, Runtime | Zulu JDK |
| [Google](google.md) | ~14 | - | - | ~3 | 构建系统, javac | - |
| [Microsoft](microsoft.md) | 少量 | - | - | ~3 | Azure 优化, Build | Microsoft Build of OpenJDK |

> **统计时间**: 2026-03-23 | **统计方法**: GitHub Integrated PRs
> **角色来源**: [OpenJDK Census](https://openjdk.org/census) JDK Project 部分
>
> **注**: PR 数据为各组织详情页面中记录的值，部分组织的统计范围仅限近几年活跃贡献者。完整历史数据参见 [按组织统计](../stats/by-org.md)。

---

## 2. 按专业领域

### 垃圾收集 (GC)

| 组织 | G1 GC | ZGC | Shenandoah | 代表贡献者 |
|------|-------|-----|------------|------------|
| **Oracle** | ✅ 核心 | ✅ 核心 | - | [Thomas Schatzl](../../by-contributor/profiles/thomas-schatzl.md), [Erik Österlund](../../by-contributor/profiles/erik-osterlund.md) |
| **Red Hat** | - | - | ✅ 创始 (历史) | [Andrew Dinn](../../by-contributor/profiles/andrew-dinn.md) |
| **Amazon** | - | - | ✅ 维护 | [William Kemper](../../by-contributor/profiles/william-kemper.md), [Aleksey Shipilev](../../by-contributor/profiles/aleksey-shipilev.md) |
| **Alibaba** | ✅ | ✅ | - | [Yude Lin](../../by-contributor/profiles/yude-lin.md), [Xiaowei Lu](../../by-contributor/profiles/xiaowei-lu.md) |
| **Tencent** | ✅ | ✅ (修复) | ✅ (修复) | [Jie Fu](https://github.com/DamonFool), [Tongbao Zhang](../../by-contributor/profiles/tongbao-zhang.md) |

### 编译器 (JIT)

| 组织 | C2 编译器 | C1 编译器 | Graal | 代表贡献者 |
|------|-----------|-----------|-------|------------|
| **Oracle** | ✅ 核心 | ✅ 核心 | ✅ | [Emanuel Peter](../../by-contributor/profiles/emanuel-peter.md), [Christian Hagedorn](../../by-contributor/profiles/christian-hagedorn.md) |
| **Red Hat** | ✅ 核心 | - | - | [Roland Westrelin](https://github.com/rwestrel) (225 PRs) |
| **Amazon** | ✅ | - | - | [Cesar Soares](https://github.com/JohnTortugo), [Aleksey Shipilev](../../by-contributor/profiles/aleksey-shipilev.md) |
| **Alibaba** | ✅ | - | - | [Kuai Wei](../../by-contributor/profiles/kuai-wei.md), [Denghui Dong](https://github.com/D-D-H) |
| **Intel** | ✅ (向量化) | - | - | [Jatin Bhateja](../../by-contributor/profiles/jatin-bhateja.md), [Swati Sharma](https://github.com/sviswa7) |
| **IBM** | ✅ (s390x) | - | - | [Amit Kumar](../../by-contributor/profiles/amit-kumar.md) |
| **Tencent** | ✅ (测试/修复) | ✅ (测试/修复) | - | [Jie Fu (傅杰)](https://github.com/DamonFool) (187 PRs) |

### 架构移植

| 组织 | x86/x64 | AArch64 | RISC-V | s390x | PPC | LoongArch |
|------|---------|---------|--------|-------|-----|-----------|
| **Oracle** | ✅ | ✅ | ✅ | - | - | - |
| **Red Hat** | - | ✅ 核心 | - | - | - | - |
| **ARM** | - | ✅ 核心 | - | - | - | - |
| **Amazon** | - | ✅ | - | - | - | - |
| **IBM** | - | - | - | ✅ 核心 | - | - |
| **SAP** | - | - | - | - | ✅ 核心 | - |
| **ISCAS PLCT** | - | - | ✅ 核心 | - | - | - |
| **ByteDance** | - | - | ✅ 向量 | - | - | - |
| **Loongson** | - | - | - | - | - | ✅ 核心 |
| **Intel** | ✅ 向量 | - | - | - | - | - |

### 核心库与性能

| 组织 | java.lang | java.util | java.time | 启动优化 | 代表贡献者 |
|------|-----------|-----------|-----------|----------|------------|
| **Oracle** | ✅ | ✅ | ✅ | ✅ | [Claes Redestad](../../by-contributor/profiles/claes-redestad.md), [Naoto Sato](../../by-contributor/profiles/naoto-sato.md) |
| **Alibaba** | ✅ 核心 | ✅ | ✅ | ✅ | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) |

### 安全

| 组织 | TLS/SSL | 加密 | 量子安全 | 代表贡献者 |
|------|---------|------|----------|------------|
| **Oracle** | ✅ 核心 | ✅ | ✅ | [Weijun Wang](../../by-contributor/profiles/weijun-wang.md), [Sean Coffey](../../by-contributor/profiles/sean-coffey.md) |

### 构建系统与基础设施

| 组织 | 构建系统 | 测试框架 | CI/CD | 代表贡献者 |
|------|----------|----------|-------|------------|
| **Oracle** | ✅ 核心 | ✅ | ✅ | [Magnus Ihse Bursie](../../by-contributor/profiles/magnus-ihse-bursie.md) |
| **Tencent** | ✅ (稳定性) | ✅ (修复) | - | [Jie Fu (傅杰)](https://github.com/DamonFool) — 构建稳定性守护者 (126+ PRs) |
| **SAP** | ✅ | ✅ | - | [Matthias Baesken](../../by-contributor/profiles/matthias-baesken.md) |
| **ARM** | ✅ | - | - | [Pankaj Bansal](../../by-contributor/profiles/pankaj-bansal.md) |

---

## 3. 按 JDK 版本贡献

### JDK 26 (GA 2026-03)

| 组织 | 主要贡献 | 关键 PR/JEP |
|------|----------|-------------|
| **Oracle** | JFR 增强, G1 GC 吞吐优化, AOT 对象缓存 | [JEP 520](https://openjdk.org/jeps/520), [JEP 522](https://openjdk.org/jeps/522), [JEP 516](https://openjdk.org/jeps/516) |
| **Alibaba** | 核心库优化 | [8370503](../../by-pr/8370/8370503.md), [8370013](../../by-pr/8370/8370013.md) |
| **Amazon** | Generational Shenandoah | [JEP 521](../../jeps/gc/jep-521.md) |
| **ISCAS PLCT** | RISC-V 向量指令 | 8355667 |
| **ByteDance** | RISC-V Zvbb/Zfa | 8329887, 8349632 |

### JDK 25 (GA 2025-09, LTS)

| 组织 | 主要贡献 | 关键 PR/JEP |
|------|----------|-------------|
| **Oracle** | HTTP/3, AOT 优化, Module Import, Compact Source Files | [JEP 517](https://openjdk.org/jeps/517), [JEP 514](https://openjdk.org/jeps/514), [JEP 511](https://openjdk.org/jeps/511), [JEP 512](https://openjdk.org/jeps/512) |
| **Alibaba** | ClassFile API 优化 | [8342336](../../by-pr/8342/8342336.md), [8341906](../../by-pr/8341/8341906.md) |
| **Amazon** | Shenandoah 改进 | 多个 |
| **Red Hat** | Compact Object Headers | [JEP 519](../../jeps/gc/jep-519.md) |

### JDK 24 (GA 2025-03)

| 组织 | 主要贡献 | 关键 PR/JEP |
|------|----------|-------------|
| **Oracle** | Class-File API, Stream Gatherers, AOT Class Loading, ZGC 精简 | [JEP 484](https://openjdk.org/jeps/484), [JEP 485](https://openjdk.org/jeps/485), [JEP 483](https://openjdk.org/jeps/483), [JEP 490](https://openjdk.org/jeps/490) |
| **Alibaba** | String "+" 运算符优化 | [JDK-8336856](../../by-pr/8336/8336856.md) |
| **Amazon** | Shenandoah 改进 | 多个 |

### JDK 23 (GA 2024-09)

| 组织 | 主要贡献 | 关键 PR/JEP |
|------|----------|-------------|
| **Oracle** | Primitive Types in Patterns | [JEP 455](../../jeps/tools/jep-455.md) |
| **Alibaba** | ClassFile API 全面优化 | [8341900](../../by-pr/8341/8341900.md), [8341906](../../by-pr/8341/8341906.md) |
| **Amazon** | Generational Shenandoah | [JEP 521](../../jeps/gc/jep-521.md) |
| **Red Hat** | Leyden 项目贡献 | 多个 |
| **ISCAS PLCT** | RISC-V 向量指令 | 多个 |

### JDK 22 (GA 2024-03)

| 组织 | 主要贡献 | 关键 JEP |
|------|----------|---------|
| **Oracle** | Class-File API, Unnamed Variables | [JEP 457](../../jeps/tools/jep-457.md), [JEP 462](https://openjdk.org/jeps/462) |
| **Alibaba** | 字符串拼接早期优化 | [8310929](../../by-pr/8310/8310929.md) |
| **Red Hat** | AArch64 改进 | 多个 |

### JDK 21 (GA 2023-09, LTS)

| 组织 | 主要贡献 | 关键 PR/JEP |
|------|----------|-------------|
| **Oracle** | Virtual Threads, Pattern Matching, Generational ZGC | [JEP 444](../../jeps/concurrency/jep-444.md), [JEP 439](../../jeps/gc/jep-439.md) |
| **Alibaba** | Integer/Long toString 优化 | [8310929](../../by-pr/8310/8310929.md), [8310502](../../by-pr/8310/8310502.md) |
| **Red Hat** | Scoped Values | [JEP 446](../../jeps/concurrency/jep-446.md) |
| **SAP** | 构建系统改进 | 多个 |

### JDK 19-20

| 版本 | 组织 | 主要贡献 | 关键 JEP |
|------|------|----------|----------|
| JDK 20 | **Oracle** | Record Patterns, Pattern Matching for switch | [JEP 440](../../jeps/language/jep-440.md), [JEP 441](../../jeps/language/jep-441.md) |
| JDK 20 | **Red Hat** | Scoped Value (Incubator) | [JEP 436](../../jeps/concurrency/jep-436.md) |
| JDK 20 | **ISCAS PLCT** | RISC-V 早期支持 | 多个 |
| JDK 19 | **Oracle** | Virtual Threads (Preview) | [JEP 425](../../jeps/concurrency/jep-425.md) |
| JDK 19 | **Huawei/ISCAS** | Linux/RISC-V Port | [JEP 422](../../jeps/ffi/jep-422.md) |

### JDK 17-18

| 版本 | 组织 | 主要贡献 | 关键 JEP |
|------|------|----------|----------|
| JDK 18 | **Oracle** | Simple Web Server, Code Snippets in API Docs | [JEP 408](../../jeps/tools/jep-408.md), [JEP 416](../../jeps/tools/jep-416.md) |
| JDK 18 | **SAP** | 构建系统优化 | 多个 |
| JDK 17 | **Oracle** | Sealed Classes, ZGC 改进 | 多个 |
| JDK 17 | **Alibaba** | ZGC, Shenandoah 早期贡献 | 8272138 |
| JDK 17 | **SAP** | PPC 移植完善 | 多个 |

### JDK 14-16

| 版本 | 组织 | 主要贡献 | 关键 JEP |
|------|------|----------|----------|
| JDK 16 | **Oracle** | Pattern Matching for instanceof, Records | [JEP 394](../../jeps/language/jep-394.md), [JEP 395](../../jeps/language/jep-395.md) |
| JDK 15 | **Oracle** | Text Blocks, ZGC | 多个 |
| JDK 15 | **Red Hat** | Shenandoah GC (Standard) | [JEP 379](../../jeps/gc/jep-379.md) |
| JDK 14 | **Oracle** | Switch Expressions, Records (Preview) | [JEP 361](../../jeps/language/jep-361.md), [JEP 359](https://openjdk.org/jeps/359) |

### JDK 9-13

| 版本 | 组织 | 主要贡献 | 关键 JEP |
|------|------|----------|----------|
| JDK 13 | **Oracle** | Text Blocks (Preview), Dynamic CDS Archives | [JEP 355](https://openjdk.org/jeps/355), [JEP 350](https://openjdk.org/jeps/350) |
| JDK 12 | **Oracle** | Switch Expressions | [JEP 325](../../jeps/language/jep-325.md) |
| JDK 12 | **Red Hat** | Shenandoah GC (Incubator) | [JEP 189](../../jeps/gc/jep-189.md) |
| JDK 11 | **Oracle** | HTTP Client, Epsilon GC | [JEP 321](https://openjdk.org/jeps/321) |
| JDK 10 | **Oracle** | Local-Variable Type Inference (var) | [JEP 286](../../jeps/language/jep-286.md) |
| JDK 9 | **Oracle** | Module System, JShell | [JEP 261](../../jeps/language/jep-261.md) |
| JDK 9 | **Red Hat** | AArch64 Port | [JEP 237](../../jeps/ffi/jep-237.md) |

### JDK 8 (LTS, 2014-03)

| 组织 | 主要贡献 |
|------|----------|
| **Oracle** | Lambdas, Streams, Date/Time API |
| **Red Hat** | AArch64 移植早期工作 |
| **IBM** | s390x 移植 |

---

## 4. 贡献趋势

### 年度 PR 统计 (2021-2025)

```
         2021    2022    2023    2024    2025
Oracle   800+    850+    900+    950+   1000+
SAP      150+    180+    200+    250+    280+
Amazon    30      40      50      60      90
Red Hat   30      35      40      45      50
IBM       15      20      30      40      45
Alibaba    7       2       8      68      35
```

### 中国企业贡献增长

| 组织 | 2023 | 2024 | 2025 | 增长趋势 |
|------|------|------|------|----------|
| **Alibaba** | 8 | 68 | 35 | ↑ 高峰后稳定 |
| **ISCAS PLCT** | 15 | 50 | 35 | ↑ 持续贡献 |
| **ByteDance** | 0 | 0 | 24 | ↑ 新兴 |
| **Loongson** | 5 | 10 | 15 | ↑ 增长 |
| **Tencent** | 19 | 7 | 3 | ↓ 高峰后回落 |

### 组织贡献份额 (JDK 26)

```
Oracle     ██████████████████████████████████████████████████████████ 70%
SAP        ████████                                                   10%
Red Hat    ████                                                        5%
Amazon     ███                                                         4%
IBM        ██                                                          3%
其他       █████                                                       8%
```

---

## 5. 组织发行版

| 组织 | 发行版 | 基于 | 特点 | 链接 |
|------|--------|------|------|------|
| **Oracle** | Oracle JDK | OpenJDK | 商业支持, 官方参考实现 | [oracle.com/java](https://www.oracle.com/java/) |
| **Amazon** | Corretto | OpenJDK | AWS 优化, 免费 LTS | [aws.amazon.com/corretto](https://aws.amazon.com/corretto/) |
| **Alibaba** | [Dragonwell](dragonwell.md) | OpenJDK | 电商场景优化 | [dragonwell-jdk.io](https://dragonwell-jdk.io/) |
| **SAP** | SapMachine | OpenJDK | 企业诊断, Vitals 工具 | [sap.github.io/SapMachine](https://sap.github.io/SapMachine/) |
| **IBM** | Semeru | OpenJDK | 多平台, IBM Z 优化 | [ibm.com/semeru-runtimes](https://developer.ibm.com/languages/java/semeru-runtimes/) |
| **Red Hat** | Red Hat OpenJDK | OpenJDK | RHEL 集成 | [redhat.com/openjdk](https://developers.redhat.com/products/openjdk) |
| **Microsoft** | Microsoft Build of OpenJDK | OpenJDK | Azure 优化, Windows ARM64 | [learn.microsoft.com/java/openjdk](https://learn.microsoft.com/java/openjdk/) |
| **Tencent** | Kona | OpenJDK | 云原生, 微服务 | [TencentKona-8](https://github.com/Tencent/TencentKona-8) |
| **Loongson** | Loongson JDK | OpenJDK | LoongArch 架构 | [loongson/jdk](https://github.com/loongson/jdk) |

---

## 6. JEP 主导组织

### GC 相关 JEP

| JEP | 标题 | 主导组织 | Lead | 版本 |
|-----|------|----------|------|------|
| [JEP 189](../../jeps/gc/jep-189.md) | Shenandoah GC (Incubator) | Red Hat | [Aleksey Shipilev](../../by-contributor/profiles/aleksey-shipilev.md) | JDK 12 |
| [JEP 379](../../jeps/gc/jep-379.md) | Shenandoah GC (Standard) | Red Hat | [Aleksey Shipilev](../../by-contributor/profiles/aleksey-shipilev.md) | JDK 15 |
| [JEP 439](../../jeps/gc/jep-439.md) | Generational ZGC | Oracle | - | JDK 21 |
| [JEP 490](https://openjdk.org/jeps/490) | ZGC: Remove Non-Generational Mode | Oracle | [Erik Österlund](../../by-contributor/profiles/erik-osterlund.md) | JDK 24 |
| [JEP 519](../../jeps/gc/jep-519.md) | Compact Object Headers | Red Hat→Datadog | [Roman Kennke](../../by-contributor/profiles/roman-kennke.md) | JDK 25 |
| [JEP 521](../../jeps/gc/jep-521.md) | Generational Shenandoah | Amazon | [William Kemper](../../by-contributor/profiles/william-kemper.md) | JDK 26 |
| [JEP 522](https://openjdk.org/jeps/522) | G1 GC Throughput Improvement | Oracle | [Thomas Schatzl](../../by-contributor/profiles/thomas-schatzl.md) | JDK 26 |

### 架构移植 JEP

| JEP | 标题 | 主导组织 | Lead | 版本 |
|-----|------|----------|------|------|
| [JEP 237](../../jeps/ffi/jep-237.md) | AArch64 Port | Red Hat | [Andrew Dinn](../../by-contributor/profiles/andrew-dinn.md) | JDK 9 |
| [JEP 422](../../jeps/ffi/jep-422.md) | Linux/RISC-V Port | Huawei | [Fei Yang](../../by-contributor/profiles/fei-yang.md) | JDK 19 |
| [JEP 501](https://openjdk.org/jeps/501) | Deprecate 32-bit x86 Port | Oracle | [Magnus Ihse Bursie](../../by-contributor/profiles/magnus-ihse-bursie.md) | JDK 24 |
| [JEP 503](https://openjdk.org/jeps/503) | Remove 32-bit x86 Port | Oracle | [Magnus Ihse Bursie](../../by-contributor/profiles/magnus-ihse-bursie.md) | JDK 25 |

### 语言与运行时 JEP

| JEP | 标题 | 主导组织 | Lead | 版本 |
|-----|------|----------|------|------|
| [JEP 444](../../jeps/concurrency/jep-444.md) | Virtual Threads | Oracle | Ron Pressler | JDK 21 |
| [JEP 446](../../jeps/concurrency/jep-446.md) | Scoped Values | Red Hat | Andrew Haley | JDK 21 |
| [JEP 455](../../jeps/tools/jep-455.md) | Primitive Types in Patterns | Oracle | [Aggelos Biboudis](../../by-contributor/profiles/aggelos-biboudis.md) | JDK 23 |
| [JEP 484](https://openjdk.org/jeps/484) | Class-File API | Oracle | [Chen Liang](../../by-contributor/profiles/chen-liang.md) | JDK 24 |
| [JEP 485](https://openjdk.org/jeps/485) | Stream Gatherers | Oracle | Viktor Klang | JDK 24 |
| [JEP 491](https://openjdk.org/jeps/491) | Synchronize Virtual Threads without Pinning | Oracle | - | JDK 24 |
| [JEP 511](https://openjdk.org/jeps/511) | Module Import Declarations | Oracle | [Jan Lahoda](../../by-contributor/profiles/jan-lahoda.md) | JDK 25 |
| [JEP 512](https://openjdk.org/jeps/512) | Compact Source Files | Oracle | [Jan Lahoda](../../by-contributor/profiles/jan-lahoda.md) | JDK 25 |
| [JEP 513](https://openjdk.org/jeps/513) | Flexible Constructor Bodies | Oracle | Gavin Bierman | JDK 25 |
| [JEP 517](https://openjdk.org/jeps/517) | HTTP/3 for HTTP Client | Oracle | [Daniel Fuchs](../../by-contributor/profiles/daniel-fuchs.md) | JDK 25 |

### AOT/CDS/性能 JEP

| JEP | 标题 | 主导组织 | Lead | 版本 |
|-----|------|----------|------|------|
| [JEP 483](https://openjdk.org/jeps/483) | Ahead-of-Time Class Loading & Linking | Oracle | [Ioi Lam](../../by-contributor/profiles/ioi-lam.md) | JDK 24 |
| [JEP 493](https://openjdk.org/jeps/493) | Linking Run-Time Images without JMODs | Oracle | [Henry Jen](../../by-contributor/profiles/henry-jen.md) | JDK 24 |
| [JEP 514](https://openjdk.org/jeps/514) | AOT Command Line Ergonomics | Oracle | [Ioi Lam](../../by-contributor/profiles/ioi-lam.md) | JDK 25 |
| [JEP 515](https://openjdk.org/jeps/515) | Ahead-of-Time Method Profiling | Oracle | Igor Veresov | JDK 25 |
| [JEP 516](https://openjdk.org/jeps/516) | AOT Object Caching | Oracle | [Erik Österlund](../../by-contributor/profiles/erik-osterlund.md) | JDK 26 |

### 监控与安全 JEP

| JEP | 标题 | 主导组织 | Lead | 版本 |
|-----|------|----------|------|------|
| [JEP 349](https://openjdk.org/jeps/349) | JFR Event Streaming | Oracle | [Erik Gahlin](../../by-contributor/profiles/erik-gahlin.md) | JDK 14 |
| [JEP 478](https://openjdk.org/jeps/478) | Key Derivation Function API (Preview) | Oracle | [Weijun Wang](../../by-contributor/profiles/weijun-wang.md) | JDK 24 |
| [JEP 496](https://openjdk.org/jeps/496) | Quantum-Resistant ML-KEM | Oracle | - | JDK 24 |
| [JEP 497](https://openjdk.org/jeps/497) | Quantum-Resistant ML-DSA | Oracle | - | JDK 24 |
| [JEP 518](https://openjdk.org/jeps/518) | JFR Cooperative Sampling | Oracle | Markus Grönlund | JDK 25 |
| [JEP 520](https://openjdk.org/jeps/520) | JFR Method Timing and Tracing | Oracle | [Erik Gahlin](../../by-contributor/profiles/erik-gahlin.md) | JDK 26 |

---

## 7. 组织特点

### Oracle

> OpenJDK 主要维护者，贡献占比约 70%

| 属性 | 值 |
|------|-----|
| **覆盖范围** | 全领域 |
| **PR 占比** | ~70% |
| **核心项目** | GC, 编译器, 核心库, 语言特性, 安全, 工具 |
| **OpenJDK 治理** | Governing Board Chair (Georges Saab), Chief Architect (Mark Reinhold) |
| **Project Leads** | Amber (Brian Goetz), Loom (Ron Pressler), Valhalla, Panama, Leyden |
| **代表贡献者** | [Thomas Schatzl](../../by-contributor/profiles/thomas-schatzl.md), [Ioi Lam](../../by-contributor/profiles/ioi-lam.md), [Emanuel Peter](../../by-contributor/profiles/emanuel-peter.md) |
| **详情** | [Oracle 组织页面](oracle.md) |

### Alibaba

> 核心库性能优化专家

| 属性 | 值 |
|------|-----|
| **专注领域** | java.lang, java.util, java.time |
| **贡献特点** | 性能优化导向，实际场景驱动 |
| **代表工作** | Integer/Long toString, ClassFile API, 字符串拼接 |
| **Dragonwell** | [电商场景优化](dragonwell.md) |
| **代表贡献者** | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md), [Kuai Wei](../../by-contributor/profiles/kuai-wei.md), [Yude Lin](../../by-contributor/profiles/yude-lin.md) |
| **详情** | [Alibaba 组织页面](alibaba.md) |

### Amazon

> Shenandoah GC 维护者，C2 编译器和 Runtime 贡献者

| 属性 | 值 |
|------|-----|
| **专注领域** | Shenandoah GC, C2 编译器, Runtime, 性能 |
| **贡献特点** | GC 深度优化，编译器改进，云原生场景 |
| **代表工作** | JEP 521 Generational Shenandoah, C2 编译器优化 |
| **Corretto** | AWS 云优化，免费 LTS 支持 |
| **代表贡献者** | [Aleksey Shipilev](../../by-contributor/profiles/aleksey-shipilev.md) (803+), [William Kemper](../../by-contributor/profiles/william-kemper.md) (123), [Cesar Soares](https://github.com/JohnTortugo) (46) |
| **详情** | [Amazon 组织页面](amazon.md) |

### Red Hat

> C2 编译器和 HotSpot Runtime 核心贡献者

| 属性 | 值 |
|------|-----|
| **专注领域** | C2 编译器, HotSpot Runtime, AArch64 |
| **贡献特点** | 编译器深度优化，运行时内存管理 |
| **代表工作** | C2 循环优化 (Roland Westrelin, 225 PRs), HotSpot Runtime/NMT (Thomas Stuefe, 347 PRs) |
| **特点** | 多位核心贡献者已流向 Amazon/Datadog |
| **代表贡献者** | [Thomas Stuefe](../../by-contributor/profiles/thomas-stuefe.md) (347), [Roland Westrelin](https://github.com/rwestrel) (225), [Andrew Haley](../../by-contributor/profiles/andrew-haley.md) (71) |
| **详情** | [Red Hat 组织页面](redhat.md) |

### SAP

> PPC 和企业诊断专家

| 属性 | 值 |
|------|-----|
| **专注领域** | PPC 移植, AIX 平台, 构建系统 |
| **贡献特点** | 跨平台构建，企业级诊断 |
| **代表工作** | PPC64LE 移植, SapMachine Vitals |
| **特点** | 构建系统贡献量第二 |
| **代表贡献者** | [Matthias Baesken](../../by-contributor/profiles/matthias-baesken.md), [Martin Doerr](../../by-contributor/profiles/martin-doerr.md) |
| **详情** | [SAP 组织页面](sap.md) |

### IBM

> s390x 和企业级 JVM

| 属性 | 值 |
|------|-----|
| **专注领域** | s390x 架构, HotSpot, 容器/cgroup |
| **贡献特点** | 企业级平台支持，大型机优化 |
| **代表工作** | s390x 向量指令 |
| **Semeru** | IBM Z 优化 |
| **代表贡献者** | [Amit Kumar](../../by-contributor/profiles/amit-kumar.md), [Severin Gehwolf](../../by-contributor/profiles/severin-gehwolf.md) |
| **详情** | [IBM 组织页面](ibm.md) |

### ARM

> AArch64 架构核心支持

| 属性 | 值 |
|------|-----|
| **专注领域** | AArch64 架构支持, 构建系统 |
| **贡献特点** | 架构级优化，指令集支持 |
| **代表工作** | AArch64 intrinsics, 构建改进 |
| **代表贡献者** | [Nick Gasson](../../by-contributor/profiles/nick-gasson.md) |
| **详情** | [ARM 组织页面](arm.md) |

### Intel

> Vector API 和 x86_64 向量化

| 属性 | 值 |
|------|-----|
| **专注领域** | Vector API, x86_64 架构优化, SuperWord |
| **贡献特点** | SIMD 向量指令支持，自动向量化 |
| **代表工作** | Vector API 向量化实现, SuperWord 优化 |
| **代表贡献者** | [Jatin Bhateja](../../by-contributor/profiles/jatin-bhateja.md) (109), [Swati Sharma](https://github.com/sviswa7) (37) |
| **详情** | [Intel 组织页面](intel.md) |

### ISCAS PLCT

> RISC-V 核心贡献者

| 属性 | 值 |
|------|-----|
| **专注领域** | RISC-V 架构移植 |
| **贡献特点** | 向量指令支持，新架构推广 |
| **代表工作** | JEP 422 RISC-V Port (与华为合作), RISC-V 向量指令 |
| **特点** | 中国科学院软件研究所 PLCT 实验室 |
| **代表贡献者** | Yadong Wang |
| **详情** | [ISCAS PLCT 组织页面](iscas-plct.md) |

### ByteDance

> RISC-V 向量指令专家

| 属性 | 值 |
|------|-----|
| **专注领域** | RISC-V 向量扩展 (Zvbb, Zfa) |
| **贡献特点** | 新指令集支持 |
| **代表工作** | Zvbb Vector And-Not, Zfa 浮点指令 |
| **代表贡献者** | [Anjian Wen](../../by-contributor/profiles/anjian-wen.md) |
| **详情** | [ByteDance 组织页面](bytedance.md) |

### Loongson

> LoongArch 架构支持

| 属性 | 值 |
|------|-----|
| **专注领域** | LoongArch 架构移植与优化 |
| **贡献特点** | 国产架构生态建设 |
| **代表工作** | LoongArch Port, 向量指令支持 |
| **详情** | [Loongson 组织页面](loongson.md) |

### Tencent

> 构建稳定性守护者，编译器测试和 GC 优化

| 属性 | 值 |
|------|-----|
| **专注领域** | 构建稳定性, 编译器测试, GC, Vector API |
| **贡献特点** | 广度最大的中国企业贡献者，OpenJDK 构建稳定性守护者 |
| **核心贡献者** | [Jie Fu (傅杰)](https://github.com/DamonFool) — 187 PRs，全球前列 |
| **Kona** | 腾讯云默认 JDK，4 个 LTS 版本 |
| **详情** | [Tencent 组织页面](tencent.md) |

### Microsoft

> Azure 平台优化

| 属性 | 值 |
|------|-----|
| **专注领域** | Azure 优化, Windows 平台 |
| **贡献特点** | 发行版维护为主，上游贡献较少 |
| **发行版** | Microsoft Build of OpenJDK |
| **详情** | [Microsoft 组织页面](microsoft.md) |

### Google

> 间接生态贡献

| 属性 | 值 |
|------|-----|
| **专注领域** | 构建系统, javac, 并发 |
| **贡献特点** | 直接代码贡献有限，主要通过 Android 生态影响 |
| **JDK 26 贡献** | ~14 提交, ~3 贡献者 |
| **详情** | [Google 组织页面](google.md) |

---

## 8. 贡献者流动

### 跨组织流动

OpenJDK 核心贡献者在组织间的流动对技术方向有深远影响：

| 贡献者 | 流动路径 | 影响领域 | 说明 |
|--------|----------|----------|------|
| [Aleksey Shipilev](../../by-contributor/profiles/aleksey-shipilev.md) | Oracle → Red Hat → **Amazon** | Shenandoah GC | Shenandoah 创始人，推动 GC 跨组织发展 |
| [Thomas Stuefe](../../by-contributor/profiles/thomas-stuefe.md) | **SAP** → **Red Hat** | HotSpot, 内存 | SapMachine 创始人，~2022 转至 Red Hat |
| [William Kemper](../../by-contributor/profiles/william-kemper.md) | Red Hat → **Amazon** | Shenandoah GC | 现 Shenandoah 主要维护者 |
| [Roman Kennke](../../by-contributor/profiles/roman-kennke.md) | Red Hat → **Datadog** | Shenandoah, Compact Headers | JEP 519 Lead |
| [Andrew Dinn](../../by-contributor/profiles/andrew-dinn.md) | Red Hat → **IBM** | AArch64, Byteman | Red Hat Distinguished Engineer 转至 IBM |
| [Severin Gehwolf](../../by-contributor/profiles/severin-gehwolf.md) | Red Hat → **IBM** | 容器/cgroup, jlink | 容器支持专家 |
| [Hamlin Li](../../by-contributor/profiles/hamlin-li.md) | Oracle → **Rivos** | RISC-V | RISC-V 架构贡献者 |
| [Tony Printezis](../../by-contributor/profiles/tony-printezis.md) | Oracle → **Rivos** | G1 GC | G1 GC 资深开发者 |
| [Xuelei Fan](../../by-contributor/profiles/xuelei-fan.md) | Oracle → **Salesforce** | Security, TLS | 安全领域专家 |

### 流动趋势

- **Oracle → 各组织**: 持续有核心开发者流出，但 Oracle 团队仍然最大
- **Red Hat → Amazon/Datadog**: Shenandoah GC 核心团队分散化
- **SAP → Red Hat**: 个别高级贡献者转移
- **整体趋势**: 人才流动促进了技术知识在组织间传播

---

## 9. 地区分布

### 按地区组织分布

| 地区 | 组织 | PRs | 发行版 |
|------|------|-----|--------|
| **北美** | | | |
| | [Oracle](oracle.md) (美国总部) | 4,200+ | Oracle JDK |
| | [Amazon](amazon.md) | 1,048+ | Corretto |
| | [IBM](ibm.md) | 113+ | Semeru |
| | [Intel](intel.md) | 146+ | - |
| | [Microsoft](microsoft.md) | 少量 | Microsoft Build of OpenJDK |
| **欧洲** | | | |
| | [SAP](sap.md) (德国) | 734+ | SapMachine |
| | [Red Hat](redhat.md) | 668+ | Red Hat OpenJDK |
| | [ARM](arm.md) (英国) | 50+ | - |
| | Oracle 欧洲团队 | - | - |
| **中国** | | | |
| | [Alibaba](alibaba.md) | 380 | Dragonwell |
| | [Loongson](loongson.md) | 30+ | Loongson JDK |
| | [ByteDance](bytedance.md) | 25 | - |
| | [ISCAS PLCT](iscas-plct.md) | 20+ | - |
| | [Tencent](tencent.md) | 228+ | Kona |

### 中国企业特点

| 特点 | 说明 |
|------|------|
| **增长迅速** | 2023-2025 年贡献增长显著，尤其是 Tencent、Alibaba 和 ISCAS PLCT |
| **领域聚焦** | 构建稳定性 (Tencent)、核心库性能 (Alibaba)、RISC-V (ISCAS/ByteDance)、LoongArch (Loongson) |
| **国产架构** | LoongArch 和 RISC-V 两大方向，推动国产芯片生态 |
| **发行版丰富** | Dragonwell、Kona、Loongson JDK 等针对不同场景 |

---

## 10. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-23
- **验证方式**: [GitHub Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+is%3Aclosed+label%3Aintegrated)
- **组织归属**: [OpenJDK Census](https://openjdk.org/census) 验证

> **注**: 各组织详情页面中的 PR 统计可能因统计范围不同 (仅活跃贡献者 vs. 历史全量) 而与 [按组织统计](../stats/by-org.md) 页面数据有差异。

---

## 11. 相关链接

- [OpenJDK Census](https://openjdk.org/census) - 官方贡献者组织归属
- [OpenJDK Groups](https://openjdk.org/groups/) - 技术工作组
- [OpenJDK Projects](https://openjdk.org/projects/) - 活跃项目列表
- [OpenJDK JEPs](https://openjdk.org/jeps/) - JEP 索引
- [GitHub openjdk/jdk](https://github.com/openjdk/jdk) - 源代码仓库
- [按组织统计](../stats/by-org.md) - 详细组织贡献统计
- [按地区分布](../stats/by-region.md) - 地区分布统计
- [Top 50 贡献者](../stats/top50.md) - 全球 Top 贡献者

[← 返回贡献者索引](../../by-contributor/README.md)
