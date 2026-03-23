# 华为

> RISC-V Port 主导者，毕昇 JDK 维护者

[← 返回组织索引](README.md)

---
## 目录

1. [概览](#1-概览)
2. [贡献者](#2-贡献者)
3. [主要领域](#3-主要领域)
4. [JEP 贡献](#4-jep-贡献)
5. [毕昇 JDK](#5-毕昇-jdk)
6. [数据来源](#6-数据来源)
7. [相关链接](#7-相关链接)

---

## 1. 概览

华为通过毕昇 JDK (BiSheng JDK) 团队参与 OpenJDK 开发，**主导了 RISC-V Port (JEP 422) 的开发并正式合入 OpenJDK 主线**（JDK 19）。这是 OpenJDK 历史上首个由中国团队主导合入的架构移植。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 167+ |
| **上游贡献者** | 3 (1 Reviewer + 2 Committer) |
| **活跃时间** | 2015 - 至今 |
| **主要领域** | RISC-V Port, AArch64, HotSpot JIT |
| **毕昇 JDK** | [BiSheng JDK](https://www.openeuler.org/en/other/projects/bishengjdk/) |
| **里程碑** | [JEP 422: Linux/RISC-V Port](https://openjdk.org/jeps/422) (JDK 19, 2022) |

> **统计说明**: 使用 GitHub Integrated PRs 统计。

---

## 2. 贡献者

### 上游贡献者

| 排名 | 贡献者 | GitHub | PRs | 角色 | 主要领域 | 档案 |
|------|--------|--------|-----|------|----------|------|
| 1 | [Fei Yang (杨飞)](../../by-contributor/profiles/fei-yang.md) | [@RealFYang](https://github.com/RealFYang) | 100 | Reviewer | RISC-V, AArch64, C1/C2 JIT | [详情](../../by-contributor/profiles/fei-yang.md) |
| 2 | Feilong Jiang | [@feilongjiang](https://github.com/feilongjiang) | 55 | Committer | RISC-V | - |
| 3 | Yadong Wang | [@yadongw](https://github.com/yadongw) | 12 | Committer | RISC-V | - |

**总计**: 167+ PRs (1 Reviewer + 2 Committer)

### Fei Yang (杨飞) — RISC-V Port Project Lead

Fei Yang 是华为 JVM 团队成员，[OpenJDK RISC-V Port](https://openjdk.org/projects/riscv-port/) 的 **Project Lead**。他自 2015 年起参与 OpenJDK AArch64 移植工作，同时也是 GCC Committer (2013+)。

**主要成就**:
- 主导 JEP 422 (Linux/RISC-V Port) 开发并合入 OpenJDK 主线
- 实现 RISC-V 平台的 Template Interpreter, C1/C2 JIT, 全部主线 GC
- [CFV: New JDK Reviewer: Fei Yang](https://mail.openjdk.org/pipermail/jdk-dev/2022-March/006470.html) (2022-03)

### Feilong Jiang — RISC-V 贡献者

Feilong Jiang 是华为杭州的 RISC-V 贡献者，也经常审查其他 RISC-V 贡献者（如 ByteDance Anjian-Wen）的 PR。

- [CFV: New JDK Committer: Feilong Jiang](https://mail.openjdk.org/pipermail/jdk-dev/2023-June/) (2023-06, 确认 "Huawei JVM Team")
- 位置: 杭州
- GitHub company: Huawei

### Yadong Wang — RISC-V 贡献者

Yadong Wang 是华为上海的 RISC-V 贡献者，参与了 RISC-V Port 的早期开发。

- [CFV: New JDK Committer: Yadong Wang](https://mail.openjdk.org/pipermail/jdk-dev/2023-June/007923.html) (2023-06, 确认 "Huawei JDK team")
- 位置: 上海
- 代表工作: [8299844: RISC-V: Implement _onSpinWait intrinsic](https://github.com/openjdk/jdk/pull/11921)

> **OpenJDK Census 角色核实** (2026-03-23):
> - **Fei Yang** (fyang): Reviewer ✅ — [CFV 2022-03](https://mail.openjdk.org/pipermail/jdk-dev/2022-March/006470.html), 确认 "JVM team at Huawei"
> - **Feilong Jiang** (fjiang): Committer ✅ — [CFV 2023-06](https://mail.openjdk.org/pipermail/jdk-dev/2023-June/)
> - **Yadong Wang** (yadongw): Committer ✅ — [CFV 2023-06](https://mail.openjdk.org/pipermail/jdk-dev/2023-June/), 确认 "Huawei JDK team"

---

## 3. 主要领域

### RISC-V 移植

| 贡献 | 说明 |
|------|------|
| **JEP 422** | Linux/RISC-V Port — 首个由中国团队主导的 OpenJDK 架构移植 |
| **Template Interpreter** | RISC-V 模板解释器实现 |
| **C1/C2 JIT** | RISC-V C1/C2 编译器后端 |
| **GC 支持** | 所有主线 GC 的 RISC-V 支持 |
| **Vector 扩展** | RISC-V Vector (RVV) 指令支持 |

### AArch64

Fei Yang 自 2015 年起也参与 AArch64 移植和优化工作。

---

## 4. JEP 贡献

| JEP | 标题 | Lead | 版本 |
|-----|------|------|------|
| [JEP 422](https://openjdk.org/jeps/422) | Linux/RISC-V Port | [Fei Yang](../../by-contributor/profiles/fei-yang.md) | JDK 19 |

> JEP 422 于 2022 年 3 月正式合入 OpenJDK 主线，使 RISC-V 成为 OpenJDK 官方支持的架构之一。

---

## 5. 毕昇 JDK

华为维护自己的 JDK 发行版 BiSheng JDK：

| 特性 | 说明 |
|------|------|
| **基于** | OpenJDK |
| **支持版本** | BiSheng JDK 8 / 11 / 17 |
| **特点** | ARM (鲲鹏) 架构优化, 性能和稳定性修复 |
| **规模** | 运行在华为内部 500+ 产品上 |
| **许可** | GPLv2 |
| **社区** | openEuler 生态 |

| 版本 | 仓库 |
|------|------|
| BiSheng JDK 8 | [openeuler-mirror/bishengjdk-8](https://github.com/openeuler-mirror/bishengjdk-8) |
| BiSheng JDK 11 | [openeuler-mirror/bishengjdk-11](https://github.com/openeuler-mirror/bishengjdk-11) |
| BiSheng JDK 17 | [openeuler-mirror/bishengjdk-17](https://github.com/openeuler-mirror/bishengjdk-17) |

---

## 6. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-23
- **CFV 来源**: [jdk-dev 邮件列表](https://mail.openjdk.org/pipermail/jdk-dev/)

---

## 7. 相关链接

- [BiSheng JDK (openEuler)](https://www.openeuler.org/en/other/projects/bishengjdk/)
- [OpenJDK RISC-V Port](https://openjdk.org/projects/riscv-port/)
- [JEP 422: Linux/RISC-V Port](https://openjdk.org/jeps/422)
- [RISC-V Port Wiki](https://wiki.openjdk.org/spaces/RISCVPort/overview)
- [Fei Yang Profile](../../by-contributor/profiles/fei-yang.md)

[← 返回组织索引](README.md)

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-23
> **创建说明**: 基于 OpenJDK 源码版权分析、CFV 提名邮件、GitHub API 核实创建
