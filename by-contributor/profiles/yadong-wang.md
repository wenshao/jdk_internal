# Yadong Wang (王亚东)

> 华为毕昇 JDK 团队，OpenJDK RISC-V 移植核心实现者，JEP 422 联合作者

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
| **姓名** | Yadong Wang (王亚东) |
| **当前组织** | [华为 (Huawei)](../../contributors/orgs/index.md) - 毕昇 JDK 团队 |
| **位置** | 中国 |
| **邮箱** | yadong.wang [at] huawei.com |
| **OpenJDK** | OpenJDK Committer |
| **角色** | RISC-V 移植核心实现者 |
| **主要领域** | RISC-V 后端, Template Interpreter, C1/C2 JIT, 平台移植 |
| **代表性贡献** | JEP 422 (Linux/RISC-V Port) 联合实现者 |

> **数据来源**: [JEP 422](https://openjdk.org/jeps/422), [CFD: RISC-V Port](https://mail.openjdk.org/pipermail/discuss/2021-September/005957.html), [JDK-8276799](https://github.com/openjdk/jdk/commit/5905b02c0e2643ae8d097562f181953f6c88fc89)

---

## 2. 技术专长

`RISC-V` `Template Interpreter` `C1 JIT` `C2 JIT` `Platform Porting` `BiSheng JDK`

Yadong Wang 是华为毕昇 JDK 团队的核心成员，是 OpenJDK RISC-V 移植的早期推动者和核心实现者之一。他从 2019 年开始基于 OpenJDK 11 进行 RISC-V 移植工作，编写了大量的移植代码，最终推动该移植在 OpenJDK 19 中正式集成。

---

## 3. 贡献概览

### 关键成就

| 项目 | 贡献 | 影响 |
|------|------|------|
| **JEP 422** | Linux/RISC-V Port 核心实现者 | OpenJDK 19 正式集成 |
| **BiSheng JDK** | RISC-V 移植先驱 | 首个 OpenJDK RISC-V 完整移植 |
| **Template Interpreter** | RISC-V 模板解释器 | JVM 基础执行引擎 |
| **C1/C2 JIT** | RISC-V JIT 后端 | 编译器代码生成 |
| **OpenJDK 11u** | RISC-V 后向移植 | 旧版 JDK 的 RISC-V 支持 |

### RISC-V 移植时间线

| 时间 | 里程碑 |
|------|--------|
| **2019** | 华为开始基于 OpenJDK 11 的 RISC-V 移植工作 |
| **2020** | 在 openEuler 社区开源毕昇 JDK RISC-V 移植 |
| **2020-12** | 向 OpenJDK 社区发起 RISC-V 移植讨论 |
| **2021-09** | Call for Discussion: 新项目 RISC-V Port |
| **2021-11** | 初始 RV64GV 支持提交 |
| **2022-03** | JEP 422 正式进入 JDK 19 |
| **2022-09** | JDK 19 发布，RISC-V Port 正式集成 |

---

## 4. 关键贡献详解

### 1. JEP 422: Linux/RISC-V Port

**背景**: RISC-V 作为开源指令集架构快速发展，Java 生态需要原生支持。

**贡献**: Yadong Wang 是 RISC-V 移植的核心实现者之一:
- 领导华为毕昇 JDK 团队完成初始 RISC-V 移植
- 实现 RV64G (IMAFD) 指令集支持
- 包括 Template Interpreter、C1 和 C2 JIT 后端
- 通过大部分 jtreg 测试和 SpecJVM2008 基准测试
- 在 QEMU RISC-V64 和 HiFive Unleashed 硬件上验证

**影响**: 这是首个由华为团队主导的 OpenJDK 社区项目，标志着华为在 OpenJDK 社区影响力的里程碑。

### 2. BiSheng JDK RISC-V 移植

**背景**: 毕昇 JDK (BiSheng JDK) 是华为的 OpenJDK 下游发行版，运行在华为 500+ 产品中。

**贡献**:
- 2019 年开始基于 OpenJDK 11 的 RISC-V 移植
- 2020 年在 openEuler 社区开源
- 移植成果最终上游化到 OpenJDK 主线

### 3. OpenJDK Committer

Yadong Wang 被提名为 OpenJDK Committer，提名由 Fei Yang (RISC-V Port Project Lead) 发起，体现了他在 RISC-V 移植中的突出贡献。

---

## 5. 开发风格

Yadong Wang 的贡献特点:

1. **移植先驱**: 从零开始实现 OpenJDK 的 RISC-V 移植
2. **全栈实现**: 覆盖解释器、JIT 编译器、运行时等全栈组件
3. **硬件验证**: 在真实 RISC-V 硬件和模拟器上全面测试
4. **上游化推动**: 成功将内部移植工作推向 OpenJDK 上游

---

## 6. 相关链接

| 类型 | 链接 |
|------|------|
| **JEP 422** | [Linux/RISC-V Port](https://openjdk.org/jeps/422) |
| **CFD 邮件** | [New Project: RISC-V Port](https://mail.openjdk.org/pipermail/discuss/2021-September/005957.html) |
| **JDK Commit** | [8276799: Implementation of JEP 422](https://github.com/openjdk/jdk/commit/5905b02c0e2643ae8d097562f181953f6c88fc89) |
| **RISC-V Port Wiki** | [OpenJDK RISC-V Port](https://wiki.openjdk.org/spaces/RISCVPort/overview) |
| **BiSheng JDK** | [openEuler BiSheng JDK](https://www.openeuler.org/en/other/projects/bishengjdk/) |
| **BiSheng JDK 11** | [GitHub](https://github.com/openeuler-mirror/bishengjdk-11) |

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-22
> **状态**: 初稿
