# Goetz Lindenmaier (Götz Lindenmaier)

> SAP OpenJDK Lead Maintainer, **OpenJDK 最大的 LTS 维护贡献者**

---

## 目录

1. [基本信息](#1-基本信息)
2. [职业时间线](#2-职业时间线)
3. [贡献统计](#3-贡献统计)
4. [LTS 维护贡献](#4-lts-维护贡献)
5. [技术特长](#5-技术特长)
6. [协作网络](#6-协作网络)
7. [数据来源](#7-数据来源)
8. [相关链接](#8-相关链接)

---

## 1. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Götz Lindenmaier (Goetz Lindenmaier) |
| **当前组织** | [SAP](../../contributors/orgs/sap.md) |
| **职位** | Lead Maintainer, OpenJDK at SAP |
| **位置** | 德国 |
| **GitHub** | [@GoeLin](https://github.com/GoeLin) |
| **OpenJDK** | [@goetz](https://openjdk.org/census#goetz) |
| **角色** | JDK Reviewer (JDK 9) |
| **Integrated PRs (主线)** | [6](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3AGoeLin+is%3Aclosed+label%3Aintegrated) |
| **LTS 维护 PRs** | **3,915** (jdk17u + jdk21u + jdk11u + jdk25u + jdk8u) |
| **总计 PRs** | **3,921** |
| **主要领域** | LTS Backport 维护, HotSpot Runtime, PowerPC/AIX Port |
| **活跃时间** | 2010+ - 至今 |

> **核心角色**: Goetz Lindenmaier 是 OpenJDK 历史上最大的 LTS 维护贡献者。他的工作确保了 JDK 17/21/11 等 LTS 版本持续获得安全补丁和 bug 修复的 backport。他个人完成的维护分支 PR 占所有 SAP 维护贡献的 74%，占全部维护分支 PR 的 ~32%。

---

## 2. 职业时间线

| 年份 | 事件 | 详情 |
|------|------|------|
| **~2000s** | 加入 SAP | SAP Java Virtual Machine Team |
| **~2005-2010** | IA64 Port | 实现和调优 SAP JVM 的 IA64 移植 |
| **2014-2017** | JDK 9 Reviewer | [CFV](https://mail.openjdk.org/archives/list/jdk9-dev@openjdk.org/message/FCO5VSP5HGYANFJ6KFCIFEQBJFUHMRR5/) |
| **2019** | SapMachine | 编辑 SapMachine 与 OpenJDK 差异文档 |
| **2024** | Lead Maintainer | [SAP Open Source Report 2024](https://community.sap.com/t5/technology-blog-posts-by-sap/a-year-of-collaboration-and-innovation-sap-open-source-report-2024/ba-p/13978967) |

---

## 3. 贡献统计

### 年度分布 (LTS 维护分支, 基于 created 日期)

```
2021: ████████████████████████████████░░░░░░░░░  jdk17u 开始, jdk11u 活跃
2022: ████████████████████████████████████████░░  多版本维护高峰
2023: ████████████████████████████████████████░░  持续高产
2024: ████████████████████████████████████████░░  jdk21u 活跃
2025: ██████████████████████████████████████░░░░  jdk17u/21u/25u
2026: ██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  截至 3 月
```

### 仓库分布

| 仓库 | PRs | 占比 | 时间段 |
|------|-----|------|--------|
| **openjdk/jdk17u-dev** | 1,951 | 49.8% | 2021-至今 |
| **openjdk/jdk21u-dev** | 1,114 | 28.4% | 2023-至今 |
| **openjdk/jdk11u-dev** | 785 | 20.0% | 2021-2024 |
| **openjdk/jdk25u-dev** | 65 | 1.7% | 2025-至今 |
| **openjdk/jdk (主线)** | 6 | 0.2% | — |
| **总计** | **3,921** | 100% | |

---

## 4. LTS 维护贡献

### 角色定位

Goetz Lindenmaier 的核心工作是将 openjdk/jdk 主线的修复 **backport** 到各 LTS 维护分支。这是一项关键但低调的工作：

- 每个 backport 需要评估适用性、解决冲突、验证兼容性
- 涉及安全补丁、性能修复、平台支持、测试改进等各类变更
- 确保企业用户使用的 LTS 版本持续获得关键修复

### SAP 维护团队对比

| 贡献者 | 维护 PRs | 主线 PRs | 总计 | 维护占比 |
|--------|----------|----------|------|----------|
| **GoeLin** | 3,915 | 6 | 3,921 | 99.8% |
| [MBaesken](matthias-baesken.md) | 499 | 492 | 991 | 50.4% |
| [TheRealMDoerr](martin-doerr.md) | 429 | 141 | 570 | 75.3% |
| [RealCLanger](christoph-langer.md) | 277 | 78 | 355 | 78.0% |
| **SAP 总计** | **5,264** | **999** | **6,263** | 84.1% |

---

## 5. 技术特长

`LTS Backport` `HotSpot Runtime` `GC` `PowerPC/AIX Port` `SapMachine` `跨平台维护`

---

## 6. 协作网络

### SAP 团队协作者

| 协作者 | 关系 | 主要领域 |
|--------|------|----------|
| [Matthias Baesken](matthias-baesken.md) | SAP 同事 | 构建系统, AIX |
| [Martin Doerr](martin-doerr.md) | SAP 同事 | PPC64/s390x, JIT |
| [Christoph Langer](christoph-langer.md) | SAP 同事 | SapMachine lead |
| [Richard Reingruber](richard-reingruber.md) | SAP 同事 | C2 编译器 |

---

## 7. 数据来源

- **主线**: GitHub PR search `repo:openjdk/jdk author:GoeLin label:integrated` (6 PRs)
- **jdk17u-dev**: `repo:openjdk/jdk17u-dev author:GoeLin label:integrated` (1,951 PRs)
- **jdk21u-dev**: `repo:openjdk/jdk21u-dev author:GoeLin label:integrated` (1,114 PRs)
- **jdk11u-dev**: `repo:openjdk/jdk11u-dev author:GoeLin label:integrated` (785 PRs)
- **jdk25u-dev**: `repo:openjdk/jdk25u-dev author:GoeLin label:integrated` (65 PRs)
- **统计时间**: 2026-03-24
- **CFV**: [jdk9 Reviewer](https://mail.openjdk.org/archives/list/jdk9-dev@openjdk.org/message/FCO5VSP5HGYANFJ6KFCIFEQBJFUHMRR5/)
- **SAP Report**: [SAP Open Source 2024](https://community.sap.com/t5/technology-blog-posts-by-sap/a-year-of-collaboration-and-innovation-sap-open-source-report-2024/ba-p/13978967)

---

## 8. 相关链接

- [GitHub Profile](https://github.com/GoeLin)
- [OpenJDK Census](https://openjdk.org/census#goetz)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20goetz)
- [FOSDEM 2013: Power to the People](https://archive.fosdem.org/2013/schedule/speaker/goetz_lindenmaier/)
- [FOSDEM 2014: PowerPC/AIX Port Endgame](https://archive.fosdem.org/2014/schedule/speaker/goetz_lindenmaier/)
- [SapMachine Wiki](https://github.com/SAP/SapMachine/wiki/Differences-between-SapMachine-and-OpenJDK)

---

> **文档版本**: 2.0
> **最后更新**: 2026-03-24
> **更新内容**: 基于 6 仓库 CSV 数据全面重写，补充 LTS 维护分支贡献统计


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 141 |
| **活跃仓库数** | 4 |
