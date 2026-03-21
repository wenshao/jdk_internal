# 地区分布

> OpenJDK 贡献者按地理区域分布 (基于 GitHub Integrated PRs)

---
## 目录

1. [数据来源说明](#1-数据来源说明)
2. [全球分布概览](#2-全球分布概览)
3. [北美 (USA/Canada)](#3-北美-usacanada)
4. [欧洲](#4-欧洲)
5. [中国](#5-中国)
6. [印度](#6-印度)
7. [日本](#7-日本)
8. [架构移植贡献](#8-架构移植贡献)
9. [数据说明](#9-数据说明)
10. [相关页面](#10-相关页面)

---


## 1. 数据来源说明

| 来源 | 用途 | 说明 |
|------|------|------|
| **GitHub Integrated PRs** | 唯一统计指标 | ⭐ 推荐使用 |
| [OpenJDK Census](https://openjdk.org/census) | 验证地区归属 | 参考来源 |

> ⚠️ **注意**: 不使用 Git commits 统计，因为 OpenJDK Committer 使用 `@openjdk.org` 邮箱提交，无法准确反映地区归属。详见 [AGENTS.md - Contribution Statistics Principles](/AGENTS.md#contribution-statistics-principles)

**查询方式**:
```
https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3A{username}+label%3Aintegrated+is%3Aclosed
```

---

## 2. 全球分布概览

> **统计来源**: [GitHub Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+label%3Aintegrated+is%3Aclosed)
> **数据更新**: 2026-03-21

| 地区 | 贡献者数 | Integrated PRs | 占比 | 主要组织 |
|------|----------|----------------|------|----------|
| 🇺🇸 **北美** | 800+ | 12,000+ | 60%+ | Oracle, Red Hat, Amazon, Google |
| 🇪🇺 **欧洲** | 300+ | 4,000+ | 20% | Red Hat, SAP, Oracle 欧洲 |
| 🇨🇳 **中国** | 50+ | 1,000+ | 5% | Oracle 中国，阿里，腾讯 |
| 🇮🇳 **印度** | 80+ | 800+ | 4% | Oracle 印度，Amazon |
| 🇦🇺 **澳大利亚** | 20+ | 200+ | 1% | 独立贡献者 |
| 🇯🇵 **日本** | 15+ | 150+ | <1% | NTT DATA |
| **其他** | 100+ | 1,000+ | 5% | 全球各地 |

---

## 3. 北美 (USA/Canada)

### 主要贡献者

| 贡献者 | Integrated PRs | 组织 | 领域 |
|--------|----------------|------|------|
| [Phil Race](/by-contributor/profiles/phil-race.md) | 200+ | Oracle | 图形 |
| [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | 90+ | Oracle | HotSpot |
| [Thomas Schatzl](/by-contributor/profiles/thomas-schatzl.md) | 150+ | Oracle | G1 GC |
| [Vladimir Kozlov](/by-contributor/profiles/vladimir-kozlov.md) | 100+ | Oracle | C2 编译器 |
| [Magnus Ihse Bursie](/by-contributor/profiles/magnus-ihse-bursie.md) | 100+ | Oracle | 构建系统 |
| [Brian Burkhalter](/by-contributor/profiles/brian-burkhalter.md) | 100+ | Oracle | NIO |
| [David Holmes](/by-contributor/profiles/david-holmes.md) | 80+ | Oracle | 并发 |
| [Daniel Fuchs](/by-contributor/profiles/daniel-fuchs.md) | 50+ | Oracle | HTTP/JMX |
| [Erik Gahlin](/by-contributor/profiles/erik-gahlin.md) | 50+ | Oracle | JFR |

### 城市/地区分布

| 地区 | 贡献者数 | 主要组织 |
|------|----------|----------|
| 加州硅谷 | 300+ | Oracle HQ, Google |
| 华盛顿州 | 40+ | Amazon |
| 马萨诸塞州 | 60+ | Oracle, Red Hat |
| 德克萨斯州 | 30+ | Oracle |
| 加拿大 | 20+ | 独立贡献者 |

---

## 4. 欧洲

### 主要贡献者

| 贡献者 | Integrated PRs | 组织 | 国家 |
|--------|----------------|------|------|
| [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | 803+ | Amazon | 俄罗斯/荷兰 |
| [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | 200+ | Oracle | 瑞士 |
| [Tobias Hartmann](/by-contributor/profiles/tobias-hartmann.md) | 150+ | Oracle | 瑞典 |
| [Matthias Baesken](/by-contributor/profiles/matthias-baesken.md) | 100+ | SAP | 德国 |
| [Thomas Stuefe](/by-contributor/profiles/thomas-stuefe.md) | 50+ | Red Hat | 德国 |
| [Stefan Karlsson](/by-contributor/profiles/stefan-karlsson.md) | 50+ | Oracle | 瑞典 |
| [Jaroslav Bachorik](/by-contributor/profiles/jaroslav-bachorik.md) | 6 | DataDog | 捷克 |

### 国家分布

| 国家 | 贡献者数 | Integrated PRs | 主要组织 |
|------|----------|----------------|----------|
| 德国 | 60+ | 500+ | SAP, Oracle |
| 瑞典 | 40+ | 400+ | Oracle |
| 英国 | 35+ | 300+ | Oracle, Red Hat |
| 法国 | 30+ | 250+ | Red Hat, Oracle |
| 瑞士 | 25+ | 300+ | Oracle |
| 捷克 | 10+ | 50+ | Oracle, DataDog |
| 荷兰 | 20+ | 200+ | 独立贡献者 |

---

## 5. 中国

### 主要贡献者

| 贡献者 | Integrated PRs | 组织 | 领域 |
|--------|----------------|------|------|
| [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | 97 | 阿里巴巴 | 核心库/性能 |
| [Albert Mingkun Yang](/by-contributor/profiles/albert-mingkun-yang.md) | 70+ | Oracle 中国 | G1 GC |
| [Fei Yang](/by-contributor/profiles/fei-yang.md) | 20+ | Huawei | RISC-V |
| Weijun Wang | 50+ | Oracle 中国 | 安全/工具 |
| Zhengyu Gu | 30+ | Oracle 中国 | G1 GC |
| Naoto Sato | 20+ | Oracle 中国 | 国际化 |
| Xue-Lei Andrew Fan | 20+ | Oracle 中国 | 安全 |

### 组织分布

| 组织 | 贡献者数 | Integrated PRs | 主要贡献 |
|------|----------|----------------|----------|
| Oracle 中国 | 15+ | 200+ | GC, 安全，国际化 |
| 阿里巴巴 | 5+ | 100+ | 性能优化 |
| ISCAS | 3+ | 10+ | RISC-V |
| 腾讯 | 3+ | 20+ | GC |
| 华为 | 5+ | 15+ | JIT/AOT |
| 字节跳动 | 3+ | 10+ | RISC-V |
| 龙芯 | 5+ | 15+ | LoongArch |

### 城市/地区分布

| 城市 | 贡献者数 | 主要组织 |
|------|----------|----------|
| 北京 | 30+ | Oracle 中国，阿里，腾讯 |
| 杭州 | 10+ | 阿里巴巴 |
| 上海 | 8+ | 独立贡献者 |
| 深圳 | 6+ | 腾讯，华为 |
| 成都 | 4+ | 腾讯 |

### 中国贡献者增长趋势

| 年份 | 新增 PRs | 累计 PRs | 主要贡献 |
|------|----------|----------|----------|
| 2021 | 50 | 50 | Oracle 中国 |
| 2022 | 100 | 150 | Oracle 中国 + 独立 |
| 2023 | 200 | 350 | 阿里加入 |
| 2024 | 300 | 650 | 多家企业 |
| 2025 | 350 | 1,000+ | 持续增长 |

---

## 6. 印度

### 主要贡献者

| 贡献者 | Integrated PRs | 组织 | 领域 |
|--------|----------------|------|------|
| (Oracle 印度团队) | 100+ | Oracle | 测试，QA |
| (Amazon 印度团队) | 50+ | Amazon | GC |

### 组织分布

| 组织 | 贡献者数 | Integrated PRs | 主要贡献 |
|------|----------|----------------|----------|
| Oracle 印度 | 40+ | 300+ | 测试，QA |
| Amazon 印度 | 15+ | 100+ | GC 优化 |
| 独立贡献者 | 25+ | 200+ | 各领域 |

---

## 7. 日本

### 主要贡献者

| 贡献者 | Integrated PRs | 组织 | 领域 |
|--------|----------------|------|------|
| [Yasumasa Suenaga](/by-contributor/profiles/yasumasa-suenaga.md) | 20+ | NTT DATA | JFR 工具 |

### 组织分布

| 组织 | 贡献者数 | Integrated PRs | 主要贡献 |
|------|----------|----------------|----------|
| NTT DATA | 5+ | 30+ | JFR 工具 |
| 独立贡献者 | 10+ | 100+ | 各领域 |

---

## 8. 架构移植贡献

### RISC-V

| 贡献者 | Integrated PRs | 组织 | 地区 |
|--------|----------------|------|------|
| [Fei Yang](/by-contributor/profiles/fei-yang.md) | 20+ | Huawei | 中国 |
| Anjian-Wen | 10+ | 字节跳动 | 中国 |
| Dingli Zhang | 10+ | ISCAS | 中国 |

### LoongArch

| 贡献者 | Integrated PRs | 组织 | 地区 |
|--------|----------------|------|------|
| Zhang Xiaofeng | 10+ | 龙芯 | 中国 |
| Ao Qi | 5+ | 龙芯 | 中国 |

### ARM64 (AArch64)

| 贡献者 | Integrated PRs | 组织 | 地区 |
|--------|----------------|------|------|
| [Andrew Dinn](/by-contributor/profiles/andrew-dinn.md) | 50+ | Red Hat | 英国 |
| [Nick Gasson](/by-contributor/profiles/nick-gasson.md) | 30+ | Arm | 欧洲 |

---

## 9. 数据说明

### 统计方法

| 指标 | 说明 | 推荐度 |
|------|------|--------|
| **GitHub Integrated PRs** | 已合入的 PR 数量 | ⭐⭐⭐ 推荐 |
| Git Commits | 历史数据，仅供参考 | ⚠️ 不推荐 |

**为什么推荐 PRs**：
- OpenJDK Committer 使用 `@openjdk.org` 邮箱提交，无法通过邮箱判断地区
- GitHub PR 直接关联贡献者账号，地区归属更准确
- 详见 [AGENTS.md - Contribution Statistics Principles](/AGENTS.md#contribution-statistics-principles)

### 参考来源

| 来源 | URL | 用途 |
|------|-----|------|
| OpenJDK Census | https://openjdk.org/census | 官方统计，验证地区归属 |
| GitHub PR Search | https://github.com/openjdk/jdk/pulls | PR 统计查询 |
| LinkedIn | https://linkedin.com | 验证贡献者所在地 |

### 数据更新

- **更新频率**: 每个 JDK 版本发布后更新
- **上次更新**: 2026-03-21
- **数据验证**: `scripts/contributor_stats.py`

---

## 10. 相关页面

- [Top 50 贡献者](top50.md)
- [按组织分类](by-org.md)
- [年度趋势](by-year.md)
- [中国贡献者](/by-contributor/profiles/chinese-contributors.md)
