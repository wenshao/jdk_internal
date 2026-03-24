# LTS 维护分支贡献分析

> 基于 openjdk/jdk17u-dev, jdk21u-dev, jdk11u-dev, jdk25u-dev, jdk8u-dev 五个仓库的 12,281 个 Integrated PRs

---

## 1. 概览

| 仓库 | PRs | 时间段 | 活跃贡献者 |
|------|-----|--------|-----------|
| **jdk17u-dev** | 4,000 | 2021-至今 | 100+ |
| **jdk21u-dev** | 2,486 | 2023-至今 | 80+ |
| **jdk11u-dev** | 2,771 | 2021-2026 | 90+ |
| **jdk25u-dev** | 341 | 2025-至今 | 30+ |
| **jdk8u-dev** | 601 | 2022-2026 | 40+ |
| **总计** | **12,281** | | |

---

## 2. Top 贡献者

### 跨仓库综合排名

| 排名 | 贡献者 | 组织 | jdk17u | jdk21u | jdk11u | jdk25u | jdk8u | 总计 | 主线 PRs |
|------|--------|------|--------|--------|--------|--------|-------|------|---------|
| 1 | [GoeLin](../../by-contributor/profiles/goetz-lindenmaier.md) | [SAP](../orgs/sap.md) | 1,951 | 1,114 | 785 | 65 | 0 | **3,915** | 6 |
| 2 | [luchenlin](https://github.com/luchenlin) | [Red Hat](../orgs/redhat.md) | 140 | 109 | 250 | 0 | 0 | **499** | 0 |
| 3 | [MBaesken](../../by-contributor/profiles/matthias-baesken.md) | [SAP](../orgs/sap.md) | 212 | 165 | 95 | 27 | 0 | **499** | 492 |
| 4 | [shipilev](../../by-contributor/profiles/aleksey-shipilev.md) | [Amazon](../orgs/amazon.md) | 239 | 149 | 157 | 21 | 0 | **566** | 775 |
| 5 | [TheRealMDoerr](../../by-contributor/profiles/martin-doerr.md) | [SAP](../orgs/sap.md) | 187 | 89 | 149 | 4 | 0 | **429** | 141 |
| 6 | [sendaoYan](../../by-contributor/profiles/sendaoyan.md) | [Alibaba](../orgs/alibaba.md) | 81 | 109 | 38 | 17 | 31 | **276** | 181 |
| 7 | [RealCLanger](../../by-contributor/profiles/christoph-langer.md) | [SAP](../orgs/sap.md) | 65 | 21 | 190 | 1 | 0 | **277** | 78 |
| 8 | [amosshi](https://github.com/amosshi) | [Alibaba](../orgs/alibaba.md) | 79 | 33 | 156 | 0 | 0 | **268** | 0 |
| 9 | [satyenme](https://github.com/satyenme) | Oracle | 98 | 138 | 0 | 0 | 0 | **236** | — |
| 10 | [mrserb](https://github.com/mrserb) | Oracle | 82 | 45 | 79 | 4 | 76 | **286** | — |
| 11 | [gnu-andrew](https://github.com/gnu-andrew) | [Red Hat](../orgs/redhat.md) | 18 | 4 | 42 | 2 | 85 | **151** | 0 |
| 12 | [jerboaa](https://github.com/jerboaa) | [Red Hat](../orgs/redhat.md) | 25 | 11 | 49 | 3 | 32 | **120** | 0 |
| 13 | [rm-gh-8](https://github.com/rm-gh-8) | Oracle | 0 | 26 | 0 | 144 | 0 | **170** | — |
| 14 | [zhengyu123](https://github.com/zhengyu123) | [Red Hat](../orgs/redhat.md) | 21 | 2 | 63 | 0 | 3 | **89** | 0 |

---

## 3. 组织贡献对比

### LTS 维护 PRs by 组织

| 组织 | jdk17u | jdk21u | jdk11u | jdk25u | jdk8u | 总计 | 主线 PRs | 维护/主线比 |
|------|--------|--------|--------|--------|-------|------|---------|------------|
| **[SAP](../orgs/sap.md)** | 2,493 | 1,412 | 1,248 | 105 | 6 | **5,264** | 999 | 5.3:1 |
| **[Red Hat](../orgs/redhat.md)** | 183 | 124 | 341 | 5 | 117 | **770** | 584 | 1.3:1 |
| **[Alibaba](../orgs/alibaba.md)** | 160 | 142 | 195 | 17 | 45 | **559** | 388 | 1.4:1 |
| **[Amazon](../orgs/amazon.md)** | 239+ | 149+ | 157+ | 21+ | 0 | **566+** | 1,172 | 0.5:1 |

> SAP 的维护/主线比为 **5.3:1**，显示其战略重心在 LTS 维护。相比之下 Amazon 的比率为 0.5:1，更偏向主线创新。

### 角色分工模式

```
主线创新为主:  Oracle (17,088) → Amazon (1,172) → SAP (999) → Red Hat (584)
LTS 维护为主:  SAP (5,264) → Red Hat (770) → Amazon (713) → Alibaba (559)
```

---

## 4. LTS 版本维护趋势

### jdk17u-dev (4,000 PRs)

```
2021: ██░░░░░░░░░░░░░░░░░░   45 PRs (10月开始)
2022: ████████████████████  899 PRs (活跃)
2023: ████████████████████ 1000 PRs (峰值)
2024: ████████████████████ 1006 PRs (稳定)
2025: ████████████████████  975 PRs (持续)
2026: ██░░░░░░░░░░░░░░░░░░   75 PRs (截至3月)
```

### jdk21u-dev (2,486 PRs)

```
2023: ██░░░░░░░░░░░░░░░░░░  100 PRs (10月开始)
2024: ████████████████████ 1129 PRs (快速增长)
2025: ████████████████████ 1106 PRs (稳定)
2026: ███░░░░░░░░░░░░░░░░░  151 PRs (截至3月)
```

### jdk11u-dev (2,771 PRs)

```
2021: ████████████░░░░░░░░  651 PRs (迁移至GitHub)
2022: ████████████████░░░░  796 PRs (峰值)
2023: ██████████████░░░░░░  723 PRs
2024: ████████░░░░░░░░░░░░  457 PRs (下降)
2025: ██░░░░░░░░░░░░░░░░░░  121 PRs (大幅下降)
2026: █░░░░░░░░░░░░░░░░░░░   23 PRs (接近EOL)
```

---

## 5. 数据来源

- **数据文件**: `{repo}/all-integrated-prs.csv` (6 仓库)
- **采集方法**: GitHub Issues Search API, 按季度分段
- **采集时间**: 2026-03-24
- **总计**: 12,281 个 Integrated PRs

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-24
