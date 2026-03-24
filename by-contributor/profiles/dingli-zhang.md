# Dingli Zhang (张丁力)

> ISCAS PLCT Lab，RISC-V/LoongArch 平台 OpenJDK 贡献者，Vector API 后端实现

---
## 目录

1. [基本信息](#1-基本信息)
2. [技术专长](#2-技术专长)
3. [贡献概览](#3-贡献概览)
4. [关键贡献详解](#4-关键贡献详解)
5. [开发风格](#5-开发风格)
6. [相关链接](#6-相关链接)

---

## 1. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Dingli Zhang (张丁力) |
| **当前组织** | [ISCAS PLCT Lab](../../contributors/orgs/iscas-plct.md) (中国科学院软件研究所 PLCT 实验室) |
| **位置** | 中国南京 |
| **GitHub** | [@DingliZhang](https://github.com/DingliZhang) |
| **OpenJDK** | OpenJDK 组织成员 |
| **邮箱** | dingli [at] iscas.ac.cn |
| **主要领域** | RISC-V 后端, Vector API, LoongArch, Zero VM |
| **活跃时间** | 2022 - 至今 |

> **数据来源**: [GitHub](https://github.com/DingliZhang), [OpenJDK RISC-V Port](https://wiki.openjdk.org/spaces/RISCVPort/overview), [PLCT Lab](https://plctlab.org/)

---

## 2. 技术专长

`RISC-V` `LoongArch` `Vector API` `C2 JIT` `Zero VM` `JDK Backport` `汇编优化`

Dingli Zhang 是 ISCAS PLCT 实验室的 JDK 开发者，专注于 RISC-V 和 LoongArch 平台的 OpenJDK 后端支持。他在 Vector API 的 RISC-V 后端实现、Zero VM 的 RISC-V 适配以及 JDK 旧版本的后向移植方面做出了重要贡献。

---

## 3. 贡献概览

### 按类别统计

| 类别 | 数量 | 描述 |
|------|------|------|
| RISC-V Vector API | 4+ | 向量指令后端实现 |
| RISC-V 汇编优化 | 3+ | CMoveI/L、PrintOptoAssembly 改进 |
| Zero VM RISC-V | 2+ | JDK 8u Zero VM 的 RISC-V 支持 |
| JDK 后向移植 | 3+ | 从 mainline 向 JDK 11u/17u 移植补丁 |
| 编译器测试修复 | 2+ | RISC-V 相关的测试问题修复 |

### 关键成就

- **Vector API RISC-V 后端**: 实现 negVI/negVL 等向量指令支持
- **Masked Vector 指令**: 支持 RISC-V 上的掩码向量算术运算
- **Zero VM RISC-V 移植**: 将 Zero 解释器移植到 RISC-V，支持 JDK 8u
- **PLCT Lab 开放报告**: 定期分享 RISC-V JDK 开发进展

### 代表性 PR

| Issue | 标题 | 描述 |
|-------|------|------|
| JDK-8295967 | RISC-V: Support negVI/negVL instructions for Vector API | 添加向量取反指令后端实现 |
| JDK-8302908 | RISC-V: Support masked vector arithmetic instructions for Vector API | 支持掩码向量算术运算 |
| JDK-8299847 | RISC-V: Improve PrintOptoAssembly output of CMoveI/L nodes | 改进编译器汇编输出 |
| JDK-8199138 | Add RISC-V support to Zero | 为 Zero VM 添加 RISC-V 支持 |

---

## 4. 关键贡献详解

### 1. Vector API RISC-V 后端 (JDK-8295967)

**问题**: RISC-V 平台缺少 Vector API 中 negVI (向量整数取反) 和 negVL (向量长整数取反) 的后端实现。

**解决方案**: 参考 RISC-V V 扩展规范 v1.0，实现了相应的向量指令匹配和代码生成。

**影响**: 使 Vector API 在 RISC-V 平台上的功能更加完整。

### 2. 掩码向量算术指令 (JDK-8302908)

**问题**: RISC-V 上的 Vector API 不支持掩码向量算术运算。

**解决方案**: 实现了 RISC-V V 扩展的掩码向量指令支持，包括掩码加法、减法、乘法等运算。

**影响**: 提升了 RISC-V 上向量化计算的灵活性和性能。

### 3. Zero VM RISC-V 支持 (JDK-8199138)

**问题**: JDK 8u 的 Zero VM 不支持 RISC-V 架构，限制了旧版 JDK 在 RISC-V 硬件上的可用性。

**解决方案**: 为 Zero VM 添加 RISC-V 平台支持，在交叉编译和原生 RISC-V 硬件上测试通过。

**影响**: 使多个 Linux 发行版能够在 RISC-V 上提供 JDK 8 Zero 版本。

---

## 5. 开发风格

Dingli Zhang 的贡献特点:

1. **平台移植专家**: 专注于 RISC-V 和 LoongArch 平台的 JDK 移植工作
2. **后向移植**: 积极将新版本改进向旧版 JDK 移植
3. **社区开放**: 通过 PLCT Lab 开放报告定期分享工作进展
4. **硬件验证**: 在真实 RISC-V 硬件上进行测试验证

---

## 6. 相关链接

| 类型 | 链接 |
|------|------|
| **GitHub** | [@DingliZhang](https://github.com/DingliZhang) |
| **PLCT Lab** | [plctlab.org](https://plctlab.org/) |
| **PLCT 开放报告** | [PLCT-Open-Reports](https://github.com/plctlab/PLCT-Open-Reports) |
| **RISC-V Port Wiki** | [OpenJDK RISC-V Port](https://wiki.openjdk.org/spaces/RISCVPort/overview) |
| **ISCAS** | [中国科学院软件研究所](http://www.iscas.ac.cn/) |

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-22
> **状态**: 初稿


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 31 |
| **活跃仓库数** | 1 |
