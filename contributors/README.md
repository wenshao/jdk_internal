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

| 排名 | 贡献者 | Commits | 领域 |
|------|--------|---------|------|
| 1 | David Katleman | 1,487 | 构建/发布 |
| 2 | Jonathan Gibbons | 1,320 | javac |
| 3 | [Aleksey Shipilev](aleksey-shipilev.md) | 1,320 | Shenandoah GC |
| 4 | [Phil Race](phil-race.md) | 1,313 | 图形 |
| 5 | [Coleen Phillimore](coleen-phillimore.md) | 1,209 | HotSpot |
| 6 | Joe Darcy | 1,194 | 核心库 |
| 7 | [Thomas Schatzl](thomas-schatl.md) | 1,113 | G1 GC |
| 8 | Alejandro Murillo | 998 | HotSpot |
| 9 | Erik Joelsson | 956 | 构建系统 |
| 10 | Weijun Wang | 954 | 安全/工具 |

👉 [查看完整 Top 50](stats/top50.md)

---

## 按领域

| 领域 | 代表性贡献者 |
|------|-------------|
| **GC** | Shipilev, Schatzl, Yang, Karlsson, Barrett |
| **编译器** | Kozlov, Westrelin, Hartmann, Ivanov |
| **核心库** | Darcy, Bateman, Redestad, Chung |
| **构建系统** | Katleman, Joelsson, Ihse Bursie |
| **桌面** | Race, Bylokhov, Sadhukhan |
| **网络** | Hegarty, Burkhalter, Fuchs |

👉 [查看完整分类](stats/by-domain.md)

---

## 按组织

| 组织 | Commits | 占比 | 主要领域 | 详情 |
|------|---------|------|----------|------|
| [Oracle](orgs/oracle.md) | 60,000+ | 70%+ | 全领域 | [查看详情](orgs/oracle.md) |
| [Red Hat](orgs/redhat.md) | 4,000+ | ~5% | GC, 编译器 | [查看详情](orgs/redhat.md) |
| [SAP](orgs/sap.md) | 2,000+ | ~2% | HotSpot, 调试 | [查看详情](orgs/sap.md) |
| [IBM](orgs/ibm.md) | 1,500+ | ~2% | JVM, 测试 | [查看详情](orgs/ibm.md) |
| [Amazon](orgs/amazon.md) | 1,000+ | ~1% | AArch64, 编译器 | [查看详情](orgs/amazon.md) |
| [Google](orgs/google.md) | 800+ | ~1% | 核心库, 编译器 | [查看详情](orgs/google.md) |
| [阿里巴巴](orgs/alibaba.md) | 72 | <1% | 核心库优化 | [查看详情](orgs/alibaba.md) |
| [龙芯](orgs/loongson.md) | 52 | <1% | LoongArch | [查看详情](orgs/loongson.md) |
| [腾讯](orgs/tencent.md) | 44 | <1% | G1 GC, 容器 | [查看详情](orgs/tencent.md) |
| [字节跳动](orgs/bytedance.md) | 12 | <1% | RISC-V | [查看详情](orgs/bytedance.md) |

---

## 数据来源

- **仓库**: OpenJDK git `upstream_master` 分支
- **指标**: Git commits
- **时间**: 2007-2026
- **验证**: `scripts/contributor_stats.py`

---

## 相关链接

- [OpenJDK](https://openjdk.org/)
- [OpenJDK Census](https://openjdk.org/census)
- [JBS Issue Tracker](https://bugs.openjdk.org/)