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

## 一览

```
OpenJDK 贡献者生态 (2007-2026)
├── 总贡献者: 2,155
├── 总 Commits: 85,000+
├── 500+ commits: 40 人
└── 100+ commits: 172 人
```

---

## Top 10 贡献者

| 排名 | 贡献者 | PRs | 领域 |
|------|--------|-----|------|
| 1 | Aleksey Shipilev | 803 | Shenandoah GC |
| 2 | Albert Mingkun Yang | 744 | GC |
| 3 | Naoto Sato | 273 | 国际化 |
| 4 | Chen Liang | 237 | ClassFile API |
| 5 | Sendao Yan | 202 | 测试稳定性 |
| 6 | Yasumasa Suenaga | 113 | HotSpot |
| 7 | Shaojin Wen | 97 | 核心库优化 |
| 8 | Hamlin Li | 74 | RISC-V |
| 9 | Anjian Wen | 25 | RISC-V |
| 10 | Kuai Wei | 13 | C2 编译器 |

👉 [查看完整 Top 50](stats/top50.md)

---

## 按领域

| 领域 | 代表性贡献者 |
|------|-------------|
| **GC** | Shipilev, Yang, Karlsson, Barrett |
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
| [Oracle](orgs/oracle.md) | 2,400+ | 全领域 | [查看详情](orgs/oracle.md) |
| [Red Hat](orgs/redhat.md) | 800+ | GC, 编译器 | [查看详情](orgs/redhat.md) |
| [SAP](orgs/sap.md) | 200+ | HotSpot, 调试 | [查看详情](orgs/sap.md) |
| [IBM](orgs/ibm.md) | 150+ | JVM, 测试 | [查看详情](orgs/ibm.md) |
| [Amazon](orgs/amazon.md) | 100+ | AArch64, 编译器 | [查看详情](orgs/amazon.md) |
| [Google](orgs/google.md) | 80+ | 核心库, 编译器 | [查看详情](orgs/google.md) |
| [阿里巴巴](orgs/alibaba.md) | 110 | 核心库优化 | [查看详情](orgs/alibaba.md) |
| [字节跳动](orgs/bytedance.md) | 25 | RISC-V | [查看详情](orgs/bytedance.md) |
| [龙芯](orgs/loongson.md) | 50+ | LoongArch | [查看详情](orgs/loongson.md) |
| [腾讯](orgs/tencent.md) | 40+ | G1 GC, 容器 | [查看详情](orgs/tencent.md) |

---

## 数据来源

- **仓库**: OpenJDK git `upstream_master` 分支
- **指标**: GitHub Integrated PRs (`repo:openjdk/jdk type:pr label:integrated`)
- **时间**: 2007-2026
- **验证**: `scripts/count_prs.py`

> **统计说明**: 使用 GitHub Integrated PR 数量作为主要统计指标，比 git commits 更准确反映实际贡献。