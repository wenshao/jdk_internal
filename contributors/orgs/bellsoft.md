# BellSoft

> Liberica JDK 维护者, ARM32/AArch64 和 RISC-V 贡献

[← 返回组织索引](README.md)

---

## 代表性 PR

> 以下为各贡献者的代表性工作（最新 5 个）。完整列表见 GitHub 链接。

### Boris Ulasevich (@bulasevich) — 39 PRs

| Bug ID | 标题 | 分析 |
|--------|------|------|
| [8374343](../../by-pr/8374/8374343.md) | 8374343: Fix SIGSEGV when lib/modules is unreadable | [详情](../../by-pr/8374/8374343.md) |
| [8371459](../../by-pr/8371/8371459.md) | 8371459: [REDO] AArch64: Use SHA3 GPR intrinsic where it's faster | [详情](../../by-pr/8371/8371459.md) |
| [8359256](../../by-pr/8359/8359256.md) | 8359256: AArch64: Use SHA3 GPR intrinsic where it's faster | [详情](../../by-pr/8359/8359256.md) |
| [8338197](../../by-pr/8338/8338197.md) | 8338197: [ubsan] ad_x86.hpp:6417:11: runtime error: shift exponent 100 | [详情](../../by-pr/8338/8338197.md) |
| [8365071](../../by-pr/8365/8365071.md) | 8365071: ARM32: JFR intrinsic jvm_commit triggers C2 regalloc assert | [详情](../../by-pr/8365/8365071.md) |

→ [完整 PR 列表](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Abulasevich+is%3Aclosed+label%3Aintegrated)

---

## 目录

1. [概览](#1-概览)
2. [贡献者](#2-贡献者)
3. [Liberica JDK](#3-liberica-jdk)
4. [数据来源](#4-数据来源)
5. [相关链接](#5-相关链接)

---

## 1. 概览

BellSoft 是 [Liberica JDK](https://bell-sw.com/libericajdk/) 的维护者，通过上游 OpenJDK 贡献参与开发，专注于 ARM32/AArch64 架构支持和 RISC-V。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 40+ |
| **贡献者数** | 1 |
| **活跃时间** | 2022 - 至今 |
| **主要领域** | ARM32, AArch64, RISC-V, JVMCI |
| **发行版** | [Liberica JDK](https://bell-sw.com/libericajdk/) |
| **源码版权** | 47 个文件含 BellSoft 版权 |

> **统计说明**: 使用 GitHub Integrated PRs 统计。

---

## 2. 贡献者

| 贡献者 | GitHub | PRs | 角色 | 主要领域 |
|--------|--------|-----|------|----------|
| Boris Ulasevich | [@bulasevich](https://github.com/bulasevich) | 40 | Committer | ARM32, AArch64, RISC-V |

**总计**: 40+ PRs

> Boris Ulasevich 位于阿根廷布宜诺斯艾利斯，是 BellSoft 的核心 OpenJDK 贡献者。他的工作涵盖 ARM32 维护、AArch64 SHA3 intrinsics、RISC-V 支持和 JVMCI 修复。

---

## 3. Liberica JDK

| 特性 | 说明 |
|------|------|
| **基于** | OpenJDK |
| **特点** | 多平台支持 (x86, ARM, RISC-V), 容器优化, JavaFX 捆绑 |
| **支持版本** | 8 / 11 / 17 / 21 |
| **许可** | GPLv2 |

---



## 审查者网络

> BellSoft 的 PR 被以下审查者审查最多 (共 100 次审查)

| 审查者 | 组织 | 审查次数 |
|--------|------|----------|
| phohensee | Oracle | 14 |
| shipilev | Amazon | 13 |
| vnkozlov | Oracle | 11 |
| bulasevich | BellSoft | 10 |
| theRealAph | Red Hat | 9 |
| eastig | Amazon | 8 |
| dean-long | Oracle | 6 |
| adinn | IBM | 4 |

### 审查组织分布

| 审查者组织 | 次数 | 占比 |
|-----------|------|------|
| Oracle | 46 | 46% |
| Amazon | 23 | 23% |
| Red Hat | 10 | 10% |
| BellSoft | 10 | 10% |
| IBM | 4 | 4% |

---

## 4. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:bulasevich type:pr label:integrated`
- **统计时间**: 2026-03-23

---

## 5. 相关链接

- [Liberica JDK](https://bell-sw.com/libericajdk/)
- [BellSoft 官网](https://bell-sw.com/)
- [Boris Ulasevich GitHub](https://github.com/bulasevich)

[← 返回组织索引](README.md)

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-23
