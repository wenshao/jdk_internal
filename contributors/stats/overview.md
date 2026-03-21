# 贡献者统计概览

> OpenJDK 历史贡献数据 (JDK 8 - JDK 26)

---

## 数据来源与统计方法

### 主要指标：GitHub Integrated PRs

**推荐使用 GitHub Integrated PRs 作为统计指标**，原因：

| 问题 | Git Commits | GitHub PRs |
|------|-------------|------------|
| 邮箱归属 | OpenJDK Committer 使用 `@openjdk.org` 邮箱，无法反映实际公司 | GitHub 账号关联真实组织 |
| 合并提交 | 大量合并提交干扰统计 | PR 粒度更清晰 |
| 贡献遗漏 | 过滤公司邮箱会遗漏大量贡献 | 准确反映实际贡献 |

**查询方式**：
```
https://github.com/openjdk/jdk/pulls?q=is%3Apr+author:{username}+label%3Aintegrated+is%3Aclosed
```

### 参考来源：OpenJDK Census

[OpenJDK Census](https://openjdk.org/census) 是官方统计页面，包含：

| 数据 | 说明 | 用途 |
|------|------|------|
| Groups | 项目组成员 | 验证领域归属 |
| People | 贡献者 commit 排名 | 参考对比 |
| Organizations | 按邮箱域名归类 | 验证组织归属 |

> ⚠️ **注意**: Census 使用 commit 统计，存在邮箱归属问题。建议作为参考而非主要指标。

---

## 总体统计

| 指标 | 数值 |
|------|------|
| 总贡献者 | 2,155 |
| 总 Commits | 85,000+ |
| 500+ commits 贡献者 | 40 |
| 100+ commits 贡献者 | 172 |
| 时间跨度 | 2007 - 2026 |

---

## 年度贡献趋势

| 年份 | Commits | JDK 版本 | 里程碑 |
|------|---------|----------|--------|
| 2007 | 21 | - | OpenJDK 开源 |
| 2008 | 1,643 | - | |
| 2009 | 2,489 | - | |
| 2010 | 2,837 | - | |
| 2011 | 3,274 | JDK 7 | JDK 7 发布 |
| 2012 | 3,228 | - | |
| 2013 | 6,897 | JDK 8 | Lambda, Stream |
| 2014 | 5,593 | JDK 8 | JDK 8 GA |
| 2015 | 6,268 | - | |
| 2016 | 7,463 | JDK 9 | 模块系统 |
| 2017 | 8,798 | JDK 9/10 | JDK 9 GA |
| 2018 | 4,655 | JDK 11 | LTS |
| 2019 | 4,436 | JDK 12/13 | |
| 2020 | 4,874 | JDK 14/15 | |
| 2021 | 4,900 | JDK 16/17 | LTS |
| 2022 | 4,557 | JDK 18/19 | |
| 2023 | 4,729 | JDK 20/21 | LTS, 虚拟线程 |
| 2024 | 4,800 | JDK 22/23 | |
| 2025 | 5,117 | JDK 24/25 | |
| 2026 | 1,032 | JDK 26 | 进行中 |

---

## 组织贡献分布

| 组织 | Commits | 占比 | 主要贡献者 |
|------|---------|------|-----------|
| Oracle | 60,000+ | 70%+ | Katleman, Gibbons, Race... |
| Red Hat | 4,000+ | 5% | Shipilev, Westrelin... |
| SAP | 2,000+ | 2% | Baesken, Stuefe... |
| IBM | 1,500+ | 2% | Stoodley... |
| Amazon | 1,000+ | 1% | Peng, Kemper, Nilsen... |
| Google | 800+ | 1% | Miller-Cushon... |
| 中国企业 | 500+ | <1% | Wen, Zhang... |

---

## 领域贡献分布

| 领域 | 主要贡献者数 | 代表性贡献者 |
|------|-------------|--------------|
| GC | 50+ | Shipilev, Schatzl, Yang |
| 编译器 (C2/Graal) | 40+ | Kozlov, Westrelin, Ivanov |
| 核心库 | 60+ | Darcy, Bateman, Redestad |
| 构建系统 | 20+ | Katleman, Joelsson, Ihse Bursie |
| 桌面 (AWT/Swing) | 30+ | Race, Bylokhov, Sadhukhan |
| 网络 (NIO/HTTP) | 25+ | Hegarty, Burkhalter, Fuchs |
| 国际化 | 10+ | Sato |
| 安全 | 15+ | Wang, Fan, Mullan |

---

## 数据说明

### 统计方法

| 指标 | 说明 | 推荐度 |
|------|------|--------|
| **GitHub Integrated PRs** | 已合入的 PR 数量 | ⭐⭐⭐ 推荐 |
| Git Commits | 历史数据，仅供参考 | ⚠️ 有偏差 |

**为什么推荐 PRs**：
- OpenJDK Committer 使用 `@openjdk.org` 邮箱提交，无法通过邮箱判断公司
- GitHub PR 直接关联贡献者账号，组织归属更准确
- 详见 [AGENTS.md - Contribution Statistics Principles](/AGENTS.md#contribution-statistics-principles)

### 参考来源

| 来源 | URL | 用途 |
|------|-----|------|
| OpenJDK Census | https://openjdk.org/census | 官方统计，验证组织归属 |
| GitHub PR Search | https://github.com/openjdk/jdk/pulls | PR 统计查询 |

### 数据更新

- **更新频率**: 每个 JDK 版本发布后更新
- **上次更新**: 2026-03-21
- **数据验证**: `scripts/contributor_stats.py`

---

## 相关页面

- [Top 50 贡献者](top50.md)
- [中国贡献者](/by-contributor/profiles/chinese-contributors.md)
- [按领域分类](by-domain.md)
- [按组织分类](by-org.md)
- [年度趋势](by-year.md)
- [地区分布](by-region.md)
- [新星贡献者](rising-stars.md)