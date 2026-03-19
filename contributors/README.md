# 贡献者索引

> OpenJDK 历史贡献者全景 (JDK 8 - JDK 26)

---

## 快速导航

| 页面 | 说明 |
|------|------|
| [统计概览](stats/overview.md) | 总体数据、年度趋势、组织分布 |
| [Top 50 贡献者](stats/top50.md) | 历史贡献排名 |
| [按领域分类](stats/by-domain.md) | GC、编译器、核心库等 |
| [按组织分类](#按组织) | Oracle、Red Hat、SAP 等 |
| [中国贡献者](chinese-contributors.md) | 中国开发者专题 |

---

## 统计说明

> **使用 GitHub Integrated PRs 作为主要贡献指标**

**为什么不用 git commits?**
- OpenJDK Committer 使用 `@openjdk.org` 邮箱提交代码
- 按公司邮箱统计 commits 会遗漏大量贡献
- GitHub PR 更准确反映实际贡献

**查询方式**: `repo:openjdk/jdk author:xxx type:pr label:integrated`

---

## Top 10 贡献者

| 排名 | 贡献者 | PRs | 组织 | 领域 |
|------|--------|-----|------|------|
| 1 | Aleksey Shipilev | 803 | Oracle | Shenandoah GC |
| 2 | Albert Mingkun Yang | 744 | Oracle | GC |
| 3 | Thomas Schatzl | 546 | Oracle | G1 GC |
| 4 | Ioi Lam | 431 | Oracle | CDS/AOT |
| 5 | Coleen Phillimore | 400 | Oracle | HotSpot |
| 6 | Naoto Sato | 273 | Oracle | 国际化 |
| 7 | Sergey Bylokhov | 273 | Oracle | AWT/2D |
| 8 | Chen Liang | 237 | Oracle | ClassFile API |
| 9 | Alexey Semenyuk | 233 | Oracle | AOT |
| 10 | Jan Lahoda | 324 | Oracle | javac |

👉 [查看完整 Top 50](stats/top50.md)

---

## 按领域

| 领域 | 代表性贡献者 |
|------|-------------|
| **GC** | Shipilev, Yang, Schatzl, Barrett |
| **编译器** | Kozlov, Westrelin, Hartmann, Ivanov |
| **核心库** | Darcy, Bateman, Redestad, Chung |
| **构建系统** | Katleman, Joelsson, Ihse Bursie |
| **桌面** | Race, Bylokhov, Sadhukhan |
| **网络** | Hegarty, Burkhalter, Fuchs |

👉 [查看完整分类](stats/by-domain.md)

---

## 按组织

| 组织 | Integrated PRs | 主要领域 | 详情 |
|------|----------------|----------|------|
| [Oracle](orgs/oracle.md) | 4,000+ | 全领域 | [查看详情](orgs/oracle.md) |
| [SAP](orgs/sap.md) | 700+ | PPC, AIX | [查看详情](orgs/sap.md) |
| [Google](orgs/google.md) | 170+ | 核心库, 编译器 | [查看详情](orgs/google.md) |
| [Amazon](orgs/amazon.md) | 165+ | AArch64, 编译器 | [查看详情](orgs/amazon.md) |
| [Red Hat](orgs/redhat.md) | 75+ | GC, 编译器 | [查看详情](orgs/redhat.md) |
| [阿里巴巴](orgs/alibaba.md) | 110 | 核心库优化 | [查看详情](orgs/alibaba.md) |
| [字节跳动](orgs/bytedance.md) | 25 | RISC-V | [查看详情](orgs/bytedance.md) |
| [龙芯](orgs/loongson.md) | 50+ | LoongArch | [查看详情](orgs/loongson.md) |
| [腾讯](orgs/tencent.md) | 40+ | G1 GC, 容器 | [查看详情](orgs/tencent.md) |
| [IBM](orgs/ibm.md) | 50+ | JVM, 测试 | [查看详情](orgs/ibm.md) |

---

## 数据来源

- **仓库**: OpenJDK git `upstream_master` 分支
- **指标**: GitHub Integrated PRs (`repo:openjdk/jdk type:pr label:integrated`)
- **时间**: 2007-2026
- **验证**: `scripts/count_prs.py`