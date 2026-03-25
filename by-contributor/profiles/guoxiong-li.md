# Guoxiong Li

> GC 和 HotSpot Runtime 代码清理贡献者，javac 编译器改进者，多个 GC 实现的重构参与者

---
## 目录

1. [基本信息](#1-基本信息)
2. [职业时间线](#2-职业时间线)
3. [技术影响力](#3-技术影响力)
4. [贡献时间线](#4-贡献时间线)
5. [技术特长](#5-技术特长)
6. [代表性工作](#6-代表性工作)
7. [技术深度](#7-技术深度)
8. [协作网络](#8-协作网络)
9. [历史贡献](#9-历史贡献)
10. [外部资源](#10-外部资源)

---

## 1. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Guoxiong Li |
| **位置** | 中国 |
| **所属机构** | 独立贡献者 |
| **学历** | 暨南大学 (Jinan University), 2013 届 |
| **GitHub** | [@lgxbslgx](https://github.com/lgxbslgx) |
| **OpenJDK** | [@lgxbslgx](https://openjdk.org/census#lgxbslgx) |
| **角色** | JDK Reviewer, Committer |
| **主要领域** | GC 重构, Serial/G1/ZGC 清理, HotSpot Runtime, javac |
| **Contributions (openjdk/jdk)** | 107 |
| **PRs (integrated)** | 102 |
| **活跃时间** | 2023 - 至今 (OpenJDK GitHub 时代) |

> **数据来源**: [GitHub](https://github.com/lgxbslgx), [OpenJDK Census](https://openjdk.org/census#lgxbslgx)

---

## 2. 职业时间线

| 年份 | 事件 | 详情 |
|------|------|------|
| **2013** | 暨南大学毕业 | 广东, 中国 |
| **~2021** | OpenJDK 社区早期贡献 | javac 编译器修复 (如重复命令行选项处理) |
| **~2023** | OpenJDK 大规模贡献开始 | 从 GC 代码清理和重构开始, 获得 Committer 身份 |
| **2024** | 大量 GC 重构 | Serial GC、G1、ZGC 的系统性代码清理, 年度约 70 PRs |
| **2025** | JDK Reviewer | 持续 HotSpot Runtime 修复、GC 改进 |

### OpenJDK 角色

- **JDK Reviewer** — 具备代码审查权限
- **JDK Committer** — 可直接提交代码
- 活跃于 OpenJDK Skara 基础设施项目 (贡献了邮件域名修复等)
- 贡献范围扩展至 openjdk/jmh 等子项目

---

## 3. 技术影响力

| 指标 | 值 |
|------|-----|
| **Contributions (openjdk/jdk)** | 107 |
| **PRs (integrated)** | 102 |
| **影响模块** | Serial GC, G1 GC, ZGC, HotSpot Runtime, javac |

### 影响的主要目录

| 目录 | 说明 |
|------|------|
| `src/hotspot/share/gc/serial/` | Serial GC 重构 |
| `src/hotspot/share/gc/g1/` | G1 GC BlockOffsetTable 重构 |
| `src/hotspot/share/gc/z/` | ZGC 代码清理 |
| `src/hotspot/share/gc/parallel/` | Parallel GC 修复 |
| `src/jdk.compiler/` | javac 编译器 |

---

## 4. 贡献时间线

```
2024: ████████████████████████████████████████████████████ (约70) Serial/G1/ZGC 大规模重构
2025: ██████████████████████████ (约28) GC 清理, Runtime 修复
2026: ████ (约4) 持续维护 (截至3月)
```

---

## 5. 技术特长

`Serial GC` `G1 GC` `ZGC` `Parallel GC` `BlockOffsetTable` `GC 重构` `javac` `HotSpot Runtime` `代码清理`

---

## 6. 代表性工作

### 1. Serial GC 大规模重构
**PR 系列**: [#23218](https://github.com/openjdk/jdk/pull/23218), [#23334](https://github.com/openjdk/jdk/pull/23334) 等

系统性重构 Serial GC 代码：重命名 MarkSweep 为 SerialFullGC，移除 TenuredSpace，内联 Generation 方法，清理 ContiguousSpace。总计 20+ PRs 涉及 Serial GC 现代化。

### 2. G1 BlockOffsetTable 重构
**PR 系列**: [#22176](https://github.com/openjdk/jdk/pull/22176) 等

将 G1BlockOffsetTablePart 合并到 G1BlockOffsetTable，重构偏移表验证逻辑，移动方法到适当的类中，内联访问器方法。

### 3. Generational ZGC 清理
**PR 系列**: 多个相关 PR

移除 ZGC 中的未使用方法和冗余友元类声明，简化 ZAddress 和 ZBarrier 逻辑，提升代码可读性。

### 4. MemAllocator 清理
**PR**: [#27020](https://github.com/openjdk/jdk/pull/27020) | **Bug**: [JDK-8357188](https://bugs.openjdk.org/browse/JDK-8357188)

移除 MemAllocator::Allocation 中未使用的 `_overhead_limit_exceeded` 字段及相关代码。

---

## 7. 技术深度

### GC 代码清理和重构专家

Guoxiong Li 的贡献主要体现在对 HotSpot GC 子系统的系统性清理和现代化改进。

**关键技术领域**:
- Serial GC 现代化：重命名、移除死代码、简化类层次结构
- G1 GC 重构：BlockOffsetTable 合并、方法移动、API 清理
- ZGC 清理：移除未使用代码、简化地址和屏障逻辑
- javac 编译器：类型系统和模式匹配相关改进
- HotSpot Runtime：内存分配器清理、测试修复

### 代码风格

- 大量小而精确的重构 PR，每个聚焦单一改进
- 系统性地遍历代码库，移除死代码和简化 API
- 注重代码命名一致性和逻辑组织
- 高产出，2024 年贡献约 70 个集成 PR

---

## 8. 协作网络

### 常见审查者

| 审查者 | 领域 |
|--------|------|
| Albert Mingkun Yang | GC |
| Thomas Schatzl | G1 GC |
| Stefan Karlsson | GC, ZGC |
| Kim Barrett | HotSpot Runtime, GC |

### 常见协作者

| 协作者 | 合作领域 |
|--------|----------|
| Albert Mingkun Yang | Serial/G1 GC 重构 |
| William Kemper | ZGC |
| Jan Lahoda | javac 编译器 |

---

## 9. 历史贡献

### JDK 版本贡献

| JDK 版本 | 主要贡献 |
|----------|----------|
| JDK 23 | G1 BlockOffsetTable 重构, ZGC 清理 |
| JDK 24 | Serial GC 大规模重命名和重构 |
| JDK 25 | GC 持续清理, Runtime 修复 |

### 长期影响

- **Serial GC 现代化**：通过系统性重命名和重构，使 Serial GC 代码更易理解和维护
- **G1 GC 简化**：合并和清理 BlockOffsetTable 相关类，减少代码复杂度
- **ZGC 代码质量**：移除冗余代码，提升 Generational ZGC 可读性
- **中国 OpenJDK 社区贡献者典范**：展示了独立贡献者对大型开源项目的持续影响

---

## 10. 外部资源

| 类型 | 链接 |
|------|------|
| **GitHub** | [@lgxbslgx](https://github.com/lgxbslgx) |
| **个人主页/博客** | [lgxbslgx.github.io](https://lgxbslgx.github.io/) |
| **OpenJDK Census** | [lgxbslgx](https://openjdk.org/census#lgxbslgx) |

### 兴趣与技术方向

根据个人主页，除 OpenJDK 贡献外，Guoxiong Li 的技术兴趣还包括 Spring Framework 和 JVM 内部机制，并在博客中撰写编译器设计、JVM 架构相关的技术文章和 OpenJDK 贡献指南。

### 相关链接

- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=lgxbslgx)
- [GitHub PRs](https://github.com/openjdk/jdk/pulls?q=author%3Algxbslgx+is%3Amerged)

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-22
> **更新内容**:
> - 初始版本创建
> - 基于 GitHub API 数据: 102 integrated PRs, 107 contributions
> - Serial GC 重构和 G1 BlockOffsetTable 改进为最高频贡献领域

## 角色晋升 (CFV)

| 日期 | 角色 | 提名者 | 投票数 | 链接 |
|------|------|--------|--------|------|
| 2021-06-02 | Committer | Vicente Romero | 10 | [CFV](https://mail.openjdk.org/pipermail/jdk-dev/2021-June/005641.html) |

**提名时统计**: 101 commits
**贡献领域**: javac; GC
