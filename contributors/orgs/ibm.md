# IBM

> JVM、s390x 和多平台支持的重要贡献者

[← 返回组织索引](README.md)

---
## 目录

1. [概览](#1-概览)
2. [贡献者](#2-贡献者)
3. [主要领域](#3-主要领域)
4. [关键贡献](#4-关键贡献)
5. [影响的模块](#5-影响的模块)
6. [IBM Semeru](#6-ibm-semeru)
7. [贡献时间线](#7-贡献时间线)
8. [数据来源](#8-数据来源)
9. [相关链接](#9-相关链接)

---


## 1. 概览

IBM 是 OpenJDK 的长期贡献者，专注于 JVM 开发、s390x 架构移植、测试框架和多平台支持。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 239+ |
| **贡献者数** | 4 |
| **活跃时间** | 2020 - 至今 |
| **主要领域** | s390x, 容器/cgroup, AArch64, JVM |
| **Semeru** | [IBM Semeru](https://developer.ibm.com/languages/java/semeru-runtimes/) |

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。

---

## 2. 贡献者

| 排名 | 贡献者 | GitHub | PRs | 角色 | 主要领域 | 档案 |
|------|--------|--------|-----|------|----------|------|
| 1 | Amit Kumar | [@offamitkumar](https://github.com/offamitkumar) | 93 | Committer | s390x, Compiler | [详情](../../by-contributor/profiles/amit-kumar.md) |
| 2 | Severin Gehwolf | [@jerboaa](https://github.com/jerboaa) | 75 | Reviewer | 容器/cgroup, jlink | [详情](../../by-contributor/profiles/severin-gehwolf.md) |
| 3 | [Ashutosh Mehra](../../by-contributor/profiles/ashutosh-mehra.md) | [@ashu-mehra](https://github.com/ashu-mehra) | 46 | Committer | AOT, CDS, Runtime | [详情](../../by-contributor/profiles/ashutosh-mehra.md) |
| 4 | Andrew Dinn | [@adinn](https://github.com/adinn) | 25 | Reviewer | AArch64, Byteman | [详情](../../by-contributor/profiles/andrew-dinn.md) |

**小计**: 239+ PRs

> **新增贡献者说明**:
> - **Severin Gehwolf** (75 PRs): 从 Red Hat 转至 IBM。GitHub 公司标注 IBM。专注容器/cgroup 支持和 jlink。
> - **Ashutosh Mehra** (46 PRs): GitHub 公司标注 IBM, 位于 Canada。[CFV: New JDK Committer (2023-08)](https://mail.openjdk.org/pipermail/jdk-dev/2023-August/)。专注 AOT/CDS/Runtime。
> - **Andrew Dinn** (25 PRs): 从 Red Hat 转至 IBM。GitHub bio 写明 "Red Hat Distinguished Engineer, IBM OpenJDK Java Platform Team"。
>
> **注**:
> - Goetz Lindenmaier (@GoeLin) 是 **SAP** 员工，不属于 IBM
> - Thomas Stuefe 属于 **Red Hat**，不属于 IBM

---

## 3. 主要领域

### s390x (IBM System z) - Amit Kumar

- s390x 架构移植
- JIT 编译器后端
- 向量指令支持
- 性能优化

---

## 4. 关键贡献

### s390x 架构 (Amit Kumar)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8275275 | s390x 向量指令扩展支持 | 性能优化 |
| 8293100 | s390x C2 编译器后端重构 | 架构改进 |
| 8319254 | 跨平台性能一致性优化 | 性能优化 |

---

## 5. 影响的模块

| 模块 | 文件数 | 说明 |
|------|--------|------|
| s390x 移植 | 60+ | s390x 架构代码 |
| C2 编译器 | 40+ | 服务端编译器 |
| HotSpot Runtime | 10+ | JVM 运行时 |
| 测试框架 | 10+ | 测试工具 |

---

## 6. IBM Semeru

IBM 维护自己的 JVM 发行版 Semeru：

| 特性 | 说明 |
|------|------|
| 基于 | OpenJDK |
| 支持 | 长期支持版本 |
| 特点 | 多平台优化 |
| 许可 | GPLv2 |

**支持平台**:
- Linux x64
- Linux s390x (IBM Z)
- Linux ppc64le (PowerPC)
- AIX

---

## 7. 贡献时间线

```
2022: ████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 22 PRs
2023: ████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 30 PRs
2024: ███████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░ 45 PRs
2025: ██████████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░ 50 PRs
2026: ████████████████████████████████████████████░░░░░░░░░░░░░░░░░░░ 55 PRs
```

> **注**: 2015-2020 年无 GitHub PR 数据 (OpenJDK 于 2020 年迁移至 GitHub)。
>
> **总计**: 82 GitHub PRs (Amit Kumar, 截至 2026-03-24); 时间线中的年度数据为估算

---



## 审查者网络

> IBM 的 PR 被以下审查者审查最多 (共 784 次审查)

| 审查者 | 组织 | 审查次数 |
|--------|------|----------|
| RealLucy | — | 59 |
| jerboaa | Red Hat | 58 |
| TheRealMDoerr | SAP | 53 |
| vnkozlov | Oracle | 47 |
| offamitkumar | IBM | 39 |
| thegreystone | Datadog | 39 |
| tstuefe | Red Hat | 37 |
| ashu-mehra | IBM | 27 |

### 审查组织分布

| 审查者组织 | 次数 | 占比 |
|-----------|------|------|
| Oracle | 265 | 34% |
| Red Hat | 133 | 17% |
| IBM | 124 | 16% |
| SAP | 91 | 12% |
| Datadog | 39 | 5% |

---

## 8. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-21

---

## 9. 相关链接

- [IBM Semeru](https://developer.ibm.com/languages/java/semeru-runtimes/)
- [IBM GitHub](https://github.com/ibmruntimes)
- [IBM Research Labs](https://research.ibm.com/)
- [IBM Z](https://www.ibm.com/it-infrastructure/z)

[→ 返回组织索引](README.md)
