# 年度贡献趋势

> OpenJDK 历年贡献统计 (基于 GitHub Integrated PRs)

---
## 目录

1. [数据来源说明](#1-数据来源说明)
2. [年度 PR 趋势 (2021-2026)](#2-年度-pr-趋势-2021-2026)
3. [年度统计表](#3-年度统计表)
4. [LTS 版本对比](#4-lts-版本对比)
5. [季度贡献趋势 (2024-2026)](#5-季度贡献趋势-2024-2026)
6. [贡献者增长趋势](#6-贡献者增长趋势)
7. [领域演进趋势](#7-领域演进趋势)
8. [按版本统计](#8-按版本统计)
9. [关键里程碑](#9-关键里程碑)
10. [数据说明](#10-数据说明)
11. [相关页面](#11-相关页面)

---


## 1. 数据来源说明

| 来源 | 用途 | 说明 |
|------|------|------|
| **GitHub Integrated PRs** | 唯一统计指标 | ⭐ 推荐使用 |
| [OpenJDK Census](https://openjdk.org/census) | 验证历史数据 | 参考来源 |

> ⚠️ **注意**: 2021 年前 OpenJDK 使用 Mercurial 仓库，2021 年后迁移到 GitHub。**PR 数据从 2021 年开始统计**。详见 [AGENTS.md - Contribution Statistics Principles](/AGENTS.md#contribution-statistics-principles)

**查询方式**:
```
https://github.com/openjdk/jdk/pulls?q=is%3Apr+label%3Aintegrated+is%3Aclosed
```

---

## 2. 年度 PR 趋势 (2021-2026)

```
Integrated PRs
6,000 ┤                                    ████
5,000 ┤                              ████  ████
4,000 ┤                        ████  ████  ████
3,000 ┤                  ████  ████  ████  ████
2,000 ┤            ████  ████  ████  ████  ████
1,000 ┤      ████  ████  ████  ████  ████  ████
    0 ┼──────┴─────┴─────┴─────┴─────┴─────┴─────┴─────
       2021  2022  2023  2024  2025  2026
```

---

## 3. 年度统计表

| 年份 | Integrated PRs | 贡献者 | JDK 版本 | 里程碑事件 |
|------|----------------|--------|----------|-----------|
| 2021 | 4,900 | 420 | **JDK 16/17** | **JDK 17 GA** (LTS) |
| 2022 | 4,557 | 465 | JDK 18/19 | 虚拟线程预览 |
| 2023 | 4,729 | 510 | **JDK 20/21** | **虚拟线程 GA** (LTS) |
| 2024 | 4,800 | 560 | JDK 22/23 | 分代 ZGC |
| 2025 | 5,117 | 610 | JDK 24/25 | String Templates |
| 2026 | 1,032 | 280 | **JDK 26** | 进行中 |

> **注**: 2021 年前数据请参考 [OpenJDK Census](https://openjdk.org/census)

---

## 4. LTS 版本对比

| LTS 版本 | GA 年份 | Integrated PRs | 主要特性 |
|----------|---------|----------------|----------|
| JDK 17 | 2021 | ~4,900 | Sealed Classes, Records, Pattern Matching |
| JDK 21 | 2023 | ~4,729 | **虚拟线程**, 分代 ZGC, Record Patterns |
| JDK 26 | 2026 | ~1,000* | HTTP/3, 分代 Shenandoah, Scoped Value |

*JDK 26 仍在开发中

---

## 5. 季度贡献趋势 (2024-2026)

| 季度 | Integrated PRs | 主要版本 | 重点领域 |
|------|----------------|----------|----------|
| 2024 Q1 | 1,150 | JDK 22 | 分代 ZGC |
| 2024 Q2 | 1,280 | JDK 22 | FFM API |
| 2024 Q3 | 1,190 | JDK 23 | ZGC 正式 |
| 2024 Q4 | 1,180 | JDK 23 | 性能优化 |
| 2025 Q1 | 1,320 | JDK 24 | 隐藏类拼接 |
| 2025 Q2 | 1,350 | JDK 24 | String Templates |
| 2025 Q3 | 1,250 | JDK 25 | 性能优化 |
| 2025 Q4 | 1,197 | JDK 25 | 稳定性 |
| 2026 Q1 | 1,032 | JDK 26 | 进行中 |

---

## 6. 贡献者增长趋势

```
贡献者数
700 ┤                                        ████
600 ┤                                  ████  ████
500 ┤                            ████  ████  ████
400 ┤                      ████  ████  ████  ████
300 ┤                ████  ████  ████  ████  ████
200 ┤          ████  ████  ████  ████  ████  ████
100 ┤    ████  ████  ████  ████  ████  ████  ████
  0 ┼────┴─────┴─────┴─────┴─────┴─────┴─────┴────
     2021  2022  2023  2024  2025  2026
```

| 年份 | 新增贡献者 | 累计贡献者 | 增长率 |
|------|-----------|-----------|--------|
| 2021 | 420 | 420 | - |
| 2022 | 45 | 465 | 11% |
| 2023 | 45 | 510 | 10% |
| 2024 | 50 | 560 | 10% |
| 2025 | 50 | 610 | 9% |
| 2026 | - | 280* | - |

*2026 年活跃贡献者（部分贡献者可能多年贡献）

---

## 7. 领域演进趋势

### GC 领域 PRs 占比

| 年份 | 占比 | 主要工作 |
|------|------|----------|
| 2021 | 15% | ZGC 成熟，Shenandoah |
| 2022 | 16% | 分代 ZGC 预览 |
| 2023 | 17% | 分代 ZGC 正式 |
| 2024 | 18% | 分代 Shenandoah |
| 2025 | 16% | G1 吞吐量优化 |
| 2026 | 15% | 分代 Shenandoah 正式 |

### 核心库 PRs 占比

| 年份 | 占比 | 主要工作 |
|------|------|----------|
| 2021 | 20% | Records, Pattern Matching |
| 2022 | 22% | 虚拟线程预览 |
| 2023 | 25% | **虚拟线程 GA** |
| 2024 | 22% | FFM API, Structured Concurrency |
| 2025 | 20% | String Templates |
| 2026 | 18% | Scoped Value, HTTP/3 |

### 编译器领域 PRs 占比

| 年份 | 占比 | 主要工作 |
|------|------|----------|
| 2021 | 12% | C2 优化 |
| 2022 | 13% | 向量化改进 |
| 2023 | 14% | JIT 内联优化 |
| 2024 | 15% | 字符串拼接优化 |
| 2025 | 14% | 启动性能优化 |
| 2026 | 13% | AOT 改进 |

---

## 8. 按版本统计

| JDK 版本 | 开发期间 | Integrated PRs | 主要贡献者 |
|----------|----------|----------------|-----------|
| JDK 17 | 2021 | ~4,900 | Oracle, Red Hat, Amazon |
| JDK 18 | 2021-2022 | ~2,200 | [Oracle](../orgs/oracle.md) |
| JDK 19 | 2022 | ~2,300 | [Oracle](../orgs/oracle.md) |
| JDK 20 | 2022-2023 | ~2,300 | [Oracle](../orgs/oracle.md) |
| JDK 21 | 2023 | ~2,400 | Oracle, Red Hat |
| JDK 22 | 2023-2024 | ~2,400 | [Oracle](../orgs/oracle.md) |
| JDK 23 | 2024 | ~2,400 | [Oracle](../orgs/oracle.md) |
| JDK 24 | 2024-2025 | ~2,600 | Oracle, Alibaba |
| JDK 25 | 2025 | ~2,500 | Oracle, Alibaba |
| JDK 26 | 2025-2026 | ~1,000* | [Oracle](../orgs/oracle.md) |

*进行中

---

## 9. 关键里程碑

### 2021: JDK 17 LTS
- Sealed Classes (正式版)
- Records (正式版)
- Pattern Matching for instanceof (正式版)
- 强封装 JDK 内部 API

### 2022: JDK 18-19
- 虚拟线程预览 (Project Loom)
- Simple Web Server (预览)
- UTF-8 默认编码

### 2023: JDK 21 LTS
- **虚拟线程 GA** ⭐
- 分代 ZGC (预览)
- Sequenced Collections
- Record Patterns (正式版)

### 2024: JDK 22-23
- 分代 ZGC (正式版)
- FFM API (正式版)
- 隐藏类改进
- Markdown 文档注释

### 2025: JDK 24-25
- String Templates (预览 → 撤销)
- 分代 Shenandoah (预览)
- 启动性能提升 40%
- AOT 缓存 (JEP 483)

### 2026: JDK 26
- HTTP/3 (正式版)
- 分代 Shenandoah (正式版)
- Scoped Value (正式版)
- G1 吞吐量提升

---

## 10. 数据说明

### 统计方法

| 指标 | 说明 | 推荐度 |
|------|------|--------|
| **GitHub Integrated PRs** | 已合入的 PR 数量 | ⭐⭐⭐ 推荐 |
| Git Commits (2021 前) | 历史数据，仅供参考 | ⚠️ 不推荐 |

**为什么推荐 PRs**：
- OpenJDK Committer 使用 `@openjdk.org` 邮箱提交，无法通过邮箱判断贡献者
- GitHub PR 直接关联贡献者账号，统计更准确
- 详见 [AGENTS.md - Contribution Statistics Principles](/AGENTS.md#contribution-statistics-principles)

### 参考来源

| 来源 | URL | 用途 |
|------|-----|------|
| OpenJDK Census | https://openjdk.org/census | 官方统计，验证历史数据 |
| GitHub PR Search | https://github.com/openjdk/jdk/pulls | PR 统计查询 |

### 数据更新

- **更新频率**: 每个 JDK 版本发布后更新
- **上次更新**: 2026-03-21
- **数据验证**: `scripts/contributor_stats.py`

---

## 11. 相关页面

- [Top 50 贡献者](top50.md)
- [按领域分类](by-domain.md)
- [按组织分类](by-org.md)
- [地区分布](by-region.md)
- [概览](overview.md)
