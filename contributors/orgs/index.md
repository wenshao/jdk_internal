# OpenJDK 贡献组织

[← 返回贡献者索引](../../by-contributor/index.md)

---

## 概览

OpenJDK 是一个由多个组织共同维护的开源项目。本文档汇总了各主要贡献组织的工作领域、版本贡献和专业方向。

| 组织 | Integrated PRs | 主要领域 | JDK 发行版 |
|------|----------------|----------|------------|
| [Oracle](oracle.md) | 4,000+ | 全领域 | Oracle JDK |
| [SAP](sap.md) | 700+ | PPC, AIX, 构建 | SapMachine |
| [Alibaba](alibaba.md) | 121 | 核心库, C2, GC | Dragonwell |
| [Amazon](amazon.md) | 160+ | Shenandoah GC, AArch64 | Corretto |
| [Red Hat](redhat.md) | 200+ | Shenandoah GC, AArch64 | Red Hat OpenJDK |
| [IBM](ibm.md) | 120+ | s390x, JVM | Semeru |
| [ISCAS PLCT](iscas-plct.md) | 100+ | RISC-V | - |
| [ByteDance](bytedance.md) | 25 | RISC-V 向量 | - |
| [Tencent](tencent.md) | 10+ | G1 GC, 容器 | Kona |
| [Loongson](loongson.md) | 30+ | LoongArch | Loongson JDK |

> **统计时间**: 2026-03-21 | **统计方法**: GitHub Integrated PRs

---

## 按专业领域

### 垃圾收集 (GC)

| 组织 | G1 GC | ZGC | Shenandoah | 代表贡献者 |
|------|-------|-----|------------|------------|
| **Oracle** | ✅ 核心 | ✅ 核心 | - | Thomas Schatzl, Stefan Karlsson |
| **Red Hat** | - | - | ✅ 创始 | Roman Kennke, Andrew Dinn |
| **Amazon** | - | - | ✅ 维护 | William Kemper |
| **Alibaba** | ✅ | ✅ | - | Yude Lin, Xiaowei Lu |
| **Tencent** | ✅ | - | - | Tongbao Zhang |

### 编译器 (JIT)

| 组织 | C2 编译器 | C1 编译器 | Graal | 代表贡献者 |
|------|-----------|-----------|-------|------------|
| **Oracle** | ✅ 核心 | ✅ 核心 | ✅ | Emanuel Peter, Vladimir Kozlov |
| **Alibaba** | ✅ | - | - | Kuai Wei |
| **IBM** | ✅ (s390x) | - | - | Amit Kumar |

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
| **Oracle** | ✅ | ✅ | ✅ | ✅ | Claes Redestad, Naoto Sato |
| **Alibaba** | ✅ 核心 | ✅ | ✅ | ✅ | Shaojin Wen |

---

## 按 JDK 版本贡献

### JDK 26 (GA 2026-03-17)

| 组织 | 主要贡献 | 关键 PR | JEP |
|------|----------|---------|-----|
| **Oracle** | GC 优化, 编译器改进 | 多个 | JEP 519, JEP 521 |
| **Alibaba** | 核心库优化 | 8370503, 8370013 | - |
| **Amazon** | Generational Shenandoah | 8354078 | JEP 521 |
| **ISCAS PLCT** | RISC-V 向量指令 | 8355667 | - |
| **ByteDance** | RISC-V Zvbb/Zfa | 8329887 | - |

### JDK 25 (2024-2025)

| 组织 | 主要贡献 | 关键 PR |
|------|----------|---------|
| **Oracle** | Compact Object Headers, Valhalla | 多个 |
| **Alibaba** | ClassFile API 优化 | 8342336, 8341906 |
| **Amazon** | Shenandoah 改进 | 多个 |
| **Red Hat** | Leyden 贡献 | 多个 |

### JDK 21 (LTS, 2023-09)

| 组织 | 主要贡献 | 关键 PR |
|------|----------|---------|
| **Oracle** | Virtual Threads, Pattern Matching | 多个 |
| **Alibaba** | Integer/Long toString 优化 | 8310929, 8310502 |
| **Red Hat** | Scoped Values | JEP 446 |

### JDK 17 (LTS, 2021-09)

| 组织 | 主要贡献 | 关键 PR |
|------|----------|---------|
| **Oracle** | Sealed Classes, ZGC 改进 | 多个 |
| **Alibaba** | ZGC, Shenandoah 早期贡献 | 8272138 |
| **SAP** | PPC 移植完善 | 多个 |

### JDK 11 (LTS, 2018-09)

| 组织 | 主要贡献 | 关键 PR |
|------|----------|---------|
| **Oracle** | HTTP Client, Epsilon GC | 多个 |
| **Red Hat** | Shenandoah (Incubator) | JEP 189 |
| **SAP** | PPC64LE 移植 | 多个 |

### JDK 8 (LTS, 2014-03)

| 组织 | 主要贡献 | 关键 PR |
|------|----------|---------|
| **Oracle** | Lambdas, Streams | - |
| **Red Hat** | AArch64 移植早期工作 | - |
| **IBM** | s390x 移植 | - |

---

## 贡献趋势

### 年度 PR 统计 (2021-2025)

```
         2021    2022    2023    2024    2025
Oracle   800+    850+    900+    950+   1000+
SAP      100+    120+    150+    180+    200+
Alibaba    7      2       8      68      35
Amazon    10      15      20      40      75
Red Hat   30      35      40      45      50
IBM       15      20      30      40      45
```

### 中国企业贡献增长

| 组织 | 2023 | 2024 | 2025 | 增长率 |
|------|------|------|------|--------|
| **Alibaba** | 8 | 68 | 35 | +337% |
| **ByteDance** | 0 | 0 | 24 | - |
| **ISCAS PLCT** | 15 | 50 | 35 | +133% |
| **Tencent** | 2 | 4 | 4 | +100% |

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

| JEP | 标题 | 主导组织 | 版本 |
|-----|------|----------|------|
| JEP 189 | Shenandoah GC (Incubator) | Red Hat | JDK 12 |
| JEP 379 | Shenandoah GC (Standard) | Red Hat | JDK 15 |
| JEP 521 | Generational Shenandoah | Amazon | JDK 26 |
| JEP 519 | Compact Object Headers | Oracle/Red Hat | JDK 24 |

### 架构移植 JEP

| JEP | 标题 | 主导组织 | 版本 |
|-----|------|----------|------|
| JEP 237 | AArch64 Port | Red Hat | JDK 9 |
| JEP 422 | RISC-V Port | ISCAS PLCT | JDK 19 |
| JEP 386 | Alpine Linux Port | Oracle | JDK 16 |

### 语言特性 JEP

| JEP | 标题 | 主导组织 | 版本 |
|-----|------|----------|------|
| JEP 439 | Generational ZGC | Oracle | JDK 21 |
| JEP 444 | Virtual Threads | Oracle | JDK 21 |
| JEP 455 | Primitive Types in Patterns | Oracle | JDK 23 |

---

## 组织特点

### Oracle

> OpenJDK 主要维护者

- **覆盖范围**: 全领域
- **PR 占比**: ~70%
- **核心项目**: GC, 编译器, 核心库, 语言特性
- **特点**: 拥有最多 Reviewer 和 Committer

### Alibaba

> 核心库性能优化专家

- **专注领域**: java.lang, java.util, java.time
- **贡献特点**: 性能优化导向，实际场景驱动
- **代表工作**: Integer/Long toString, ClassFile API, 字符串拼接
- **Dragonwell**: 电商场景优化

### Amazon

> Shenandoah GC 维护者

- **专注领域**: Shenandoah GC, AArch64
- **贡献特点**: GC 深度优化
- **代表工作**: JEP 521 Generational Shenandoah
- **Corretto**: AWS 云优化

### Red Hat

> AArch64 和 Leyden 贡献者

- **专注领域**: Shenandoah GC, AArch64, Project Leyden
- **贡献特点**: 架构优化，启动性能
- **代表工作**: AArch64 移植，SVE 支持
- **特点**: JBoss Byteman 项目

### SAP

> PPC 和企业诊断专家

- **专注领域**: PPC 移植, AIX 平台, 构建系统
- **贡献特点**: 跨平台构建，企业级诊断
- **代表工作**: PPC64LE 移植, SapMachine Vitals
- **特点**: 最多构建系统贡献

### IBM

> s390x 和企业级 JVM

- **专注领域**: s390x 架构, HotSpot
- **贡献特点**: 企业级平台支持
- **代表工作**: s390x 向量指令
- **Semeru**: IBM Z 优化

### ISCAS PLCT

> RISC-V 核心贡献者

- **专注领域**: RISC-V 架构移植
- **贡献特点**: 向量指令支持
- **代表工作**: RISC-V 向量 Min/Max, 扩展检测
- **特点**: 中国科学院软件所

### ByteDance

> RISC-V 向量指令专家

- **专注领域**: RISC-V 向量扩展 (Zvbb, Zfa)
- **贡献特点**: 新指令支持
- **代表工作**: Zvbb Vector And-Not, Zfa 浮点指令

---

## 贡献者流动

### 跨组织流动

| 贡献者 | 原组织 | 现组织 | 说明 |
|--------|--------|--------|------|
| Thomas Stuefe | SAP → Amazon → IBM | IBM | SapMachine 创始人 |
| Aleksey Shipilev | Red Hat | AWS | Shenandoah 创始人 |
| William Kemper | Red Hat | Amazon | Shenandoah 维护 |

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
