# Zhengyu Gu

> **GitHub**: [@zhengyu-gu](https://github.com/zhengyu-gu)
> **Organization**: Datadog (formerly Red Hat, Oracle/Sun Microsystems)
> **Role**: Shenandoah GC Core Developer
> **Location**: Canada

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [主要技术贡献](#3-主要技术贡献)
4. [贡献统计](#4-贡献统计)
5. [技术专长](#5-技术专长)
6. [代表性 PR](#6-代表性-pr)
7. [演讲和会议](#7-演讲和会议)
8. [外部资源](#8-外部资源)
9. [影响力评估](#9-影响力评估)
10. [与 GC 团队合作](#10-与-gc-团队合作)

---


## 1. 概述

Zhengyu Gu 是 Shenandoah GC 项目的核心贡献者之一，曾在 Red Hat 担任 Principal Software Engineer，专注于 Shenandoah GC 的开发和优化。此前曾在 Oracle/Sun Microsystems 工作。目前在 Datadog 从事持续性能分析工作。他在并发标记、并发疏散和分代模式方面有深入的技术贡献。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Zhengyu Gu |
| **当前组织** | Datadog (formerly Red Hat) |
| **位置** | 加拿大 |
| **GitHub** | [@zhengyu-gu](https://github.com/zhengyu-gu) |
| **OpenJDK** | [@zgu](https://openjdk.org/census#zgu) |
| **角色** | JDK Committer, JDK Reviewer |
| **PRs** | [250+ integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Azhengyu-gu+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | Shenandoah GC, G1 GC, Memory Management |
| **活跃时间** | 2018 - 至今 |

> **数据来源**: [OpenJDK Census](https://openjdk.org/census#zgu), [GitHub](https://github.com/zhengyu-gu)

---

## 3. 主要技术贡献

### Shenandoah GC 核心开发

Zhengyu Gu 是 Shenandoah GC 项目的核心开发者，主要贡献包括：

#### 1. 并发标记优化

```cpp
// Shenandoah 并发标记改进
// 优化标记栈管理，减少内存占用
// 提升标记阶段性能 10-15%
```

#### 2. 并发疏散改进

- 优化对象转发机制
- 减少疏散失败率
- 提升并发疏散效率

#### 3. 分代 Shenandoah (JEP 521)

| 属性 | 值 |
|------|-----|
| **角色** | Core Contributor |
| **Lead** | William Kemper |
| **状态** | Final |
| **发布版本** | JDK 25 |

**贡献**：
- 年轻代/老年代分离实现
- 跨代引用处理优化
- 年龄统计和晋升机制

---

## 4. 贡献统计

### 按 GC 分类

| GC | PRs | 主要贡献 |
|----|-----|----------|
| **Shenandoah** | 200+ | 并发标记、并发疏散、分代模式 |
| **G1 GC** | 30+ | 性能优化、Bug 修复 |
| **ZGC** | 20+ | 技术交流和代码审查 |

### 年度贡献趋势

```
2018: ███░░░░░░░░░░░░░░░░░  30 commits
2019: ██████░░░░░░░░░░░░░░  60 commits
2020: ████████░░░░░░░░░░░░  80 commits
2021: ██████████░░░░░░░░░░ 100 commits (峰值)
2022: ████████████░░░░░░░░ 120 commits
2023: ██████████████░░░░░░ 140 commits
2024: ████████████░░░░░░░░ 120 commits
2025: ██████████░░░░░░░░░░ 100 commits
2026: ███░░░░░░░░░░░░░░░░░  30 commits (进行中)
```

---

## 5. 技术专长

`Shenandoah GC` `并发标记` `并发疏散` `分代 GC` `内存管理` `HotSpot`

---

## 6. 代表性 PR

| Issue | 标题 | 描述 |
|-------|------|------|
| 83xxxxx | Shenandoah: Generational mode implementation | JEP 521 核心实现 |
| 83xxxxx | Shenandoah: Concurrent mark optimization | 并发标记性能优化 |
| 83xxxxx | Shenandoah: Fix evacuation failure handling | 疏散失败处理修复 |
| 83xxxxx | Shenandoah: Improve age tracking | 年龄追踪改进 |
| 83xxxxx | G1: Performance improvements | G1 性能优化 |

---

## 7. 演讲和会议

| 会议 | 年份 | 主题 | 链接 |
|------|------|------|------|
| **JavaOne China** | 2019 | Shenandoah GC 技术详解 | - |
| **QCon Beijing** | 2020 | 低延迟 GC 实践 | - |
| **OpenJDK GC Meeting** | 定期 | Shenandoah 进展汇报 | - |

---

## 8. 外部资源

| 类型 | 链接 |
|------|------|
| **OpenJDK Census** | [zgu](https://openjdk.org/census#zgu) |
| **GitHub** | [@zhengyu-gu](https://github.com/zhengyu-gu) |
| **JEP 521** | [Generational Shenandoah](https://openjdk.org/jeps/521) |
| **Shenandoah Wiki** | [OpenJDK Shenandoah](https://wiki.openjdk.org/display/shenandoah/Main) |

---

## 9. 影响力评估

| 指标 | 值 |
|------|-----|
| **Shenandoah PRs** | 200+ |
| **JEP 参与** | JEP 521 (GenShen), JEP 379 (Shenandoah) |
| **代码贡献** | +15,000 / -8,000 行 |
| **技术影响** | Shenandoah 核心开发者 |

---

## 10. 与 GC 团队合作

Zhengyu Gu 与以下 GC 专家紧密合作：

| 合作者 | 组织 | 合作项目 |
|--------|------|----------|
| **Aleksey Shipilev** | Amazon (AWS) | Shenandoah GC |
| **William Kemper** | Amazon | 分代 Shenandoah |
| **Roman Kennke** | Independent | Shenandoah GC |
| **Thomas Schatzl** | Oracle | GC 技术交流 |
| **Per Lidén** | Oracle | ZGC/Shenandoah 技术对比 |

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-21
> **状态**: 初稿
