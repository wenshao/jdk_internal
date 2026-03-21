# OpenJDK 贡献组织

[← 返回贡献者索引](../../by-contributor/index.md)

---

## 概览

OpenJDK 是一个由多个组织共同维护的开源项目。本文档汇总了各主要贡献组织的工作领域、版本贡献和专业方向。

| 组织 | Integrated PRs | 主要领域 | JDK 发行版 |
|------|----------------|----------|------------|
| [Oracle](oracle.md) | 4,000+ | 全领域 | Oracle JDK |
| [SAP](sap.md) | 734+ | PPC, AIX, 构建 | SapMachine |
| [Alibaba](alibaba.md) | 121 | 核心库, C2, GC | Dragonwell |
| [Amazon](amazon.md) | 138+ | Shenandoah GC, AArch64 | Corretto |
| [Red Hat](redhat.md) | 200+ | Shenandoah GC, AArch64, Leyden | Red Hat OpenJDK |
| [IBM](ibm.md) | 113+ | s390x, JVM | Semeru |
| [ISCAS PLCT](iscas-plct.md) | 100+ | RISC-V | - |
| [ByteDance](bytedance.md) | 25 | RISC-V 向量 | - |
| [Tencent](tencent.md) | 10+ | G1 GC, 容器 | Kona |
| [Loongson](loongson.md) | 30+ | LoongArch | Loongson JDK |
| [Google](google.md) | 需核实 | - | - |

> **统计时间**: 2026-03-21 | **统计方法**: GitHub Integrated PRs

---

## 按专业领域

### 垃圾收集 (GC)

| 组织 | G1 GC | ZGC | Shenandoah | 代表贡献者 |
|------|-------|-----|------------|------------|
| **Oracle** | ✅ 核心 | ✅ 核心 | - | [Thomas Schatzl](../../by-contributor/profiles/thomas-schatzl.md), [Stefan Karlsson](../../by-contributor/profiles/stefan-karlsson.md) |
| **Red Hat** | - | - | ✅ 创始 | [Roman Kennke](../../by-contributor/profiles/roman-kennke.md) |
| **Amazon** | - | - | ✅ 维护 | [William Kemper](../../by-contributor/profiles/william-kemper.md), [Aleksey Shipilev](../../by-contributor/profiles/aleksey-shipilev.md) |
| **Alibaba** | ✅ | ✅ | - | [Yude Lin](../../by-contributor/profiles/yude-lin.md), [Xiaowei Lu](../../by-contributor/profiles/xiaowei-lu.md) |
| **Tencent** | ✅ | - | - | [Tongbao Zhang](../../by-contributor/profiles/tongbao-zhang.md) |

### 编译器 (JIT)

| 组织 | C2 编译器 | C1 编译器 | Graal | 代表贡献者 |
|------|-----------|-----------|-------|------------|
| **Oracle** | ✅ 核心 | ✅ 核心 | ✅ | [Emanuel Peter](../../by-contributor/profiles/emanuel-peter.md), [Vladimir Kozlov](../../by-contributor/profiles/vladimir-kozlov.md) |
| **Alibaba** | ✅ | - | - | [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) |
| **IBM** | ✅ (s390x) | - | - | [Amit Kumar](../../by-contributor/profiles/amit-kumar.md) |
| **Amazon** | ✅ | - | - | [Aleksey Shipilev](../../by-contributor/profiles/aleksey-shipilev.md) |

### 架构移植

| 组织 | x86/x64 | AArch64 | RISC-V | s390x | PPC | LoongArch |
|------|---------|---------|--------|-------|-----|-----------|
| **Oracle** | ✅ | ✅ | ✅ | - | - | - |
| **Red Hat** | - | ✅ 核心 | - | - | - | - |
| **Amazon** | - | ✅ | - | - | - | - |
| **IBM** | - | - | - | ✅ 核心 | - | - |
| **SAP** | - | - | - | - | ✅ 核心 | - |
| **ISCAS PLCT** | - | - | ✅ 核心 | - | - | - |
| **ByteDance** | - | - | ✅ 向量 | - | - | - |
| **Loongson** | - | - | - | - | - | ✅ 核心 |

### 核心库与性能

| 组织 | java.lang | java.util | java.time | 启动优化 | 代表贡献者 |
|------|-----------|-----------|-----------|----------|------------|
| **Oracle** | ✅ | ✅ | ✅ | ✅ | [Claes Redestad](../../by-contributor/profiles/claes-redestad.md), [Naoto Sato](../../by-contributor/profiles/naoto-sato.md) |
| **Alibaba** | ✅ 核心 | ✅ | ✅ | ✅ | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) |

---

## 按 JDK 版本贡献

### JDK 26 (GA 2026-03-17)

| 组织 | 主要贡献 | 关键 PR/JEP |
|------|----------|-------------|
| **Oracle** | GC 优化, 编译器改进 | 多个 |
| **Alibaba** | 核心库优化 | 8370503, 8370013 |
| **Amazon** | Generational Shenandoah | [JEP 521](https://openjdk.org/jeps/521) |
| **Red Hat** | Compact Object Headers | [JEP 519](https://openjdk.org/jeps/519) |
| **ISCAS PLCT** | RISC-V 向量指令 | 8355667 |
| **ByteDance** | RISC-V Zvbb/Zfa | 8329887, 8349632 |

### JDK 25 (2024-2025)

| 组织 | 主要贡献 | 关键 PR |
|------|----------|---------|
| **Oracle** | Valhalla 预览, GC 改进 | 多个 |
| **Alibaba** | ClassFile API 优化 | 8342336, 8341906 |
| **Amazon** | Shenandoah 改进 | 多个 |
| **Red Hat** | Leyden 贡献 | 多个 |

### JDK 21 (LTS, 2023-09)

| 组织 | 主要贡献 | 关键 PR/JEP |
|------|----------|-------------|
| **Oracle** | Virtual Threads, Pattern Matching | [JEP 444](https://openjdk.org/jeps/444) |
| **Alibaba** | Integer/Long toString 优化 | 8310929, 8310502 |
| **Red Hat** | Scoped Values | [JEP 446](https://openjdk.org/jeps/446) |
| **SAP** | 构建系统改进 | 多个 |

### JDK 19 (2022-09)

| 组织 | 主要贡献 | 关键 JEP |
|------|----------|----------|
| **Oracle** | Virtual Threads (Preview) | [JEP 425](https://openjdk.org/jeps/425) |
| **ISCAS PLCT** | Linux/RISC-V Port | [JEP 422](https://openjdk.org/jeps/422) |

### JDK 17 (LTS, 2021-09)

| 组织 | 主要贡献 | 关键 PR |
|------|----------|---------|
| **Oracle** | Sealed Classes, ZGC 改进 | 多个 |
| **Alibaba** | ZGC, Shenandoah 早期贡献 | 8272138 |
| **SAP** | PPC 移植完善 | 多个 |

### JDK 15 (2020-09)

| 组织 | 主要贡献 | 关键 JEP |
|------|----------|----------|
| **Oracle** | Text Blocks, ZGC | 多个 |
| **Red Hat** | Shenandoah GC (Standard) | [JEP 379](https://openjdk.org/jeps/379) |

### JDK 12 (2019-03)

| 组织 | 主要贡献 | 关键 JEP |
|------|----------|----------|
| **Oracle** | Switch Expressions | [JEP 325](https://openjdk.org/jeps/325) |
| **Red Hat** | Shenandoah GC (Incubator) | [JEP 189](https://openjdk.org/jeps/189) |

### JDK 11 (LTS, 2018-09)

| 组织 | 主要贡献 | 关键 JEP |
|------|----------|----------|
| **Oracle** | HTTP Client, Epsilon GC | [JEP 321](https://openjdk.org/jeps/321) |
| **SAP** | PPC64LE 移植 | - |

### JDK 9 (2017-09)

| 组织 | 主要贡献 | 关键 JEP |
|------|----------|----------|
| **Oracle** | Module System, JShell | [JEP 261](https://openjdk.org/jeps/261) |
| **Red Hat** | AArch64 Port | [JEP 237](https://openjdk.org/jeps/237) |

### JDK 8 (LTS, 2014-03)

| 组织 | 主要贡献 |
|------|----------|
| **Oracle** | Lambdas, Streams, Date/Time API |
| **Red Hat** | AArch64 移植早期工作 |
| **IBM** | s390x 移植 |

---

## 贡献趋势

### 年度 PR 统计 (2021-2025)

```
         2021    2022    2023    2024    2025
Oracle   800+    850+    900+    950+   1000+
SAP      150+    180+    200+    250+    280+
Alibaba    7      2       8      68      35
Amazon    30      40      50      60      90
Red Hat   30      35      40      45      50
IBM       15      20      30      40      45
```

### 中国企业贡献增长

| 组织 | 2023 | 2024 | 2025 | 增长趋势 |
|------|------|------|------|----------|
| **Alibaba** | 8 | 68 | 35 | ↑ 高峰后稳定 |
| **ByteDance** | 0 | 0 | 24 | ↑ 新兴 |
| **ISCAS PLCT** | 15 | 50 | 35 | ↑ 持续贡献 |
| **Tencent** | 2 | 4 | 4 | → 稳定 |
| **Loongson** | 5 | 10 | 15 | ↑ 增长 |

---

## 组织发行版

| 组织 | 发行版 | 基于 | 特点 | 链接 |
|------|--------|------|------|------|
| **Oracle** | Oracle JDK | OpenJDK | 商业支持 | [oracle.com/java](https://www.oracle.com/java/) |
| **Amazon** | Corretto | OpenJDK | AWS 优化 | [aws.amazon.com/corretto](https://aws.amazon.com/corretto/) |
| **Alibaba** | Dragonwell | OpenJDK | 电商优化 | [dragonwell-jdk.io](https://dragonwell-jdk.io/) |
| **SAP** | SapMachine | OpenJDK | 企业诊断 | [sap.github.io/SapMachine](https://sap.github.io/SapMachine/) |
| **IBM** | Semeru | OpenJDK | 多平台 | [ibm.com/semeru-runtimes](https://developer.ibm.com/languages/java/semeru-runtimes/) |
| **Red Hat** | OpenJDK | OpenJDK | RHEL 集成 | [redhat.com/openjdk](https://developers.redhat.com/products/openjdk) |
| **Tencent** | Kona | OpenJDK | 云原生 | [TencentKona-8](https://github.com/Tencent/TencentKona-8) |
| **Loongson** | Loongson JDK | OpenJDK | LoongArch | [loongson/jdk](https://github.com/loongson/jdk) |

---

## JEP 主导组织

### GC 相关 JEP

| JEP | 标题 | 主导组织 | Lead | 版本 |
|-----|------|----------|------|------|
| [JEP 189](https://openjdk.org/jeps/189) | Shenandoah GC (Incubator) | Red Hat | [Aleksey Shipilev](../../by-contributor/profiles/aleksey-shipilev.md) | JDK 12 |
| [JEP 379](https://openjdk.org/jeps/379) | Shenandoah GC (Standard) | Red Hat | [Aleksey Shipilev](../../by-contributor/profiles/aleksey-shipilev.md) | JDK 15 |
| [JEP 519](https://openjdk.org/jeps/519) | Compact Object Headers | Red Hat | [Roman Kennke](../../by-contributor/profiles/roman-kennke.md) | JDK 25 |
| [JEP 521](https://openjdk.org/jeps/521) | Generational Shenandoah | Amazon | [William Kemper](../../by-contributor/profiles/william-kemper.md) | JDK 26 |
| [JEP 439](https://openjdk.org/jeps/439) | Generational ZGC | Oracle | - | JDK 21 |

### 架构移植 JEP

| JEP | 标题 | 主导组织 | Lead | 版本 |
|-----|------|----------|------|------|
| [JEP 237](https://openjdk.org/jeps/237) | AArch64 Port | Red Hat | [Andrew Dinn](../../by-contributor/profiles/andrew-dinn.md) | JDK 9 |
| [JEP 422](https://openjdk.org/jeps/422) | Linux/RISC-V Port | ISCAS PLCT | [Fei Yang](../../by-contributor/profiles/fei-yang.md) | JDK 19 |

### 语言与运行时 JEP

| JEP | 标题 | 主导组织 | 版本 |
|-----|------|----------|------|
| [JEP 444](https://openjdk.org/jeps/444) | Virtual Threads | Oracle | JDK 21 |
| [JEP 446](https://openjdk.org/jeps/446) | Scoped Values | Red Hat | JDK 21 |
| [JEP 455](https://openjdk.org/jeps/455) | Primitive Types in Patterns | Oracle | JDK 23 |

---

## 组织特点

### Oracle

> OpenJDK 主要维护者

| 属性 | 值 |
|------|-----|
| **覆盖范围** | 全领域 |
| **PR 占比** | ~70% |
| **核心项目** | GC, 编译器, 核心库, 语言特性 |
| **特点** | 拥有最多 Reviewer 和 Committer |
| **代表贡献者** | [Thomas Schatzl](../../by-contributor/profiles/thomas-schatzl.md), [Claes Redestad](../../by-contributor/profiles/claes-redestad.md), [Emanuel Peter](../../by-contributor/profiles/emanuel-peter.md) |

### Alibaba

> 核心库性能优化专家

| 属性 | 值 |
|------|-----|
| **专注领域** | java.lang, java.util, java.time |
| **贡献特点** | 性能优化导向，实际场景驱动 |
| **代表工作** | Integer/Long toString, ClassFile API, 字符串拼接 |
| **Dragonwell** | 电商场景优化 |
| **代表贡献者** | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md), [Kuai Wei](../../by-contributor/profiles/kuai-wei.md), [Yude Lin](../../by-contributor/profiles/yude-lin.md) |

### Amazon

> Shenandoah GC 维护者

| 属性 | 值 |
|------|-----|
| **专注领域** | Shenandoah GC, AArch64 |
| **贡献特点** | GC 深度优化 |
| **代表工作** | JEP 521 Generational Shenandoah |
| **Corretto** | AWS 云优化 |
| **代表贡献者** | [William Kemper](../../by-contributor/profiles/william-kemper.md), [Aleksey Shipilev](../../by-contributor/profiles/aleksey-shipilev.md), [Nick Gasson](../../by-contributor/profiles/nick-gasson.md) |

### Red Hat

> AArch64 和 Leyden 贡献者

| 属性 | 值 |
|------|-----|
| **专注领域** | Shenandoah GC, AArch64, Project Leyden |
| **贡献特点** | 架构优化，启动性能 |
| **代表工作** | AArch64 移植, JEP 519 Compact Object Headers |
| **特点** | JBoss Byteman 项目 |
| **代表贡献者** | [Roman Kennke](../../by-contributor/profiles/roman-kennke.md), [Andrew Dinn](../../by-contributor/profiles/andrew-dinn.md) |

### SAP

> PPC 和企业诊断专家

| 属性 | 值 |
|------|-----|
| **专注领域** | PPC 移植, AIX 平台, 构建系统 |
| **贡献特点** | 跨平台构建，企业级诊断 |
| **代表工作** | PPC64LE 移植, SapMachine Vitals |
| **特点** | 最多构建系统贡献 |
| **代表贡献者** | [Matthias Baesken](../../by-contributor/profiles/matthias-baesken.md), [Goetz Lindenmaier](../../by-contributor/profiles/goetz-lindenmaier.md), [Erik Joelsson](../../by-contributor/profiles/erik-joelsson.md) |

### IBM

> s390x 和企业级 JVM

| 属性 | 值 |
|------|-----|
| **专注领域** | s390x 架构, HotSpot |
| **贡献特点** | 企业级平台支持 |
| **代表工作** | s390x 向量指令 |
| **Semeru** | IBM Z 优化 |
| **代表贡献者** | [Amit Kumar](../../by-contributor/profiles/amit-kumar.md), [Thomas Stuefe](../../by-contributor/profiles/thomas-stuefe.md) |

### ISCAS PLCT

> RISC-V 核心贡献者

| 属性 | 值 |
|------|-----|
| **专注领域** | RISC-V 架构移植 |
| **贡献特点** | 向量指令支持 |
| **代表工作** | JEP 422 RISC-V Port, RISC-V 向量指令 |
| **特点** | 中国科学院软件所 |
| **代表贡献者** | [Fei Yang](../../by-contributor/profiles/fei-yang.md) |

### ByteDance

> RISC-V 向量指令专家

| 属性 | 值 |
|------|-----|
| **专注领域** | RISC-V 向量扩展 (Zvbb, Zfa) |
| **贡献特点** | 新指令支持 |
| **代表工作** | Zvbb Vector And-Not, Zfa 浮点指令 |
| **代表贡献者** | [Anjian Wen](../../by-contributor/profiles/anjian-wen.md) |

---

## 贡献者流动

### 跨组织流动

| 贡献者 | 原组织 | 现组织 | 说明 |
|--------|--------|--------|------|
| [Thomas Stuefe](../../by-contributor/profiles/thomas-stuefe.md) | SAP → Amazon → IBM | IBM | SapMachine 创始人 |
| [Aleksey Shipilev](../../by-contributor/profiles/aleksey-shipilev.md) | Oracle → Red Hat → AWS | Amazon | Shenandoah 创始人 |
| [William Kemper](../../by-contributor/profiles/william-kemper.md) | Red Hat | Amazon | Shenandoah 维护者 |

---

## 地区分布

### 中国企业

| 组织 | PRs | 主要领域 | 发行版 |
|------|-----|----------|--------|
| [Alibaba](alibaba.md) | 121 | 核心库, GC | Dragonwell |
| [ISCAS PLCT](iscas-plct.md) | 100+ | RISC-V | - |
| [Loongson](loongson.md) | 30+ | LoongArch | Loongson JDK |
| [ByteDance](bytedance.md) | 25 | RISC-V 向量 | - |
| [Tencent](tencent.md) | 10+ | G1 GC, 容器 | Kona |

### 欧洲企业

| 组织 | PRs | 主要领域 | 发行版 |
|------|-----|----------|--------|
| [SAP](sap.md) | 734+ | PPC, 构建 | SapMachine |
| [Red Hat](redhat.md) | 200+ | GC, AArch64 | Red Hat OpenJDK |
| Oracle (欧洲团队) | - | - | - |

### 美国企业

| 组织 | PRs | 主要领域 | 发行版 |
|------|-----|----------|--------|
| [Oracle](oracle.md) | 4000+ | 全领域 | Oracle JDK |
| [Amazon](amazon.md) | 138+ | GC | Corretto |
| [IBM](ibm.md) | 113+ | s390x | Semeru |

---

## 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-21
- **验证方式**: [GitHub Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+is%3Aclosed+label%3Aintegrated)

---

## 相关链接

- [OpenJDK Census](https://openjdk.org/census)
- [OpenJDK Groups](https://openjdk.org/groups/)
- [OpenJDK JEPs](https://openjdk.org/jeps/)
- [GitHub openjdk/jdk](https://github.com/openjdk/jdk)

[→ 返回贡献者索引](../../by-contributor/index.md)
