# Marc Chevalier

> C2 JIT 编译器开发者，IR Framework 核心维护者，内联优化和编译器测试基础设施专家

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
| **姓名** | Marc Chevalier |
| **当前组织** | [Oracle](../../contributors/orgs/oracle.md) |
| **职位** | Software Engineer (HotSpot JVM Compiler) |
| **位置** | 苏黎世, 瑞士 |
| **GitHub** | [@marc-chevalier](https://github.com/marc-chevalier) |
| **OpenJDK** | [@marc-chevalier](https://openjdk.org/census#marc-chevalier) |
| **角色** | JDK Committer |
| **主要领域** | C2 JIT 编译器, IR Framework, 内联优化, 编译器测试 |
| **PRs (integrated)** | 45 |
| **活跃时间** | 2024 - 至今 (OpenJDK GitHub 时代) |

> **数据来源**: [GitHub](https://github.com/marc-chevalier), [OpenJDK Census](https://openjdk.org/census#marc-chevalier)

---

## 2. 职业时间线

| 年份 | 事件 | 详情 |
|------|------|------|
| **2014** | BSc in Computer Science | ENS Lyon |
| **2016** | MSc in Computer Science | ENS Lyon / EPFL |
| **2017-2020** | PhD in Computer Science | ENS Paris (Antique team), 导师: Jérôme Feret |
| **2020** | 博士论文答辩 | "Proving the Security of Software-Intensive Embedded Systems by Abstract Interpretation" |
| **~2021-2023** | 静态分析研究 / 工业合作 | Astrée 静态分析器改进 (与 AbsInt GmbH / Airbus 合作) |
| **2024** | 加入 Oracle HotSpot 编译器团队 | 开始 C2 编译器贡献 |
| **2025** | IR Framework 核心改进 | 方法命名、重载检测、规则验证 |
| **2026** | 内联优化和编译策略改进 | StressIncrementalInlining 随机化 |

---

## 3. 技术影响力

| 指标 | 值 |
|------|-----|
| **PRs (integrated)** | 45 |
| **影响模块** | C2 编译器, IR Framework, 编译器测试 |

### 影响的主要目录

| 目录 | 说明 |
|------|------|
| `src/hotspot/share/opto/` | C2 JIT 编译器核心代码 |
| `test/hotspot/jtreg/compiler/lib/ir_framework/` | IR Framework 测试框架 |
| `src/hotspot/share/opto/compile.cpp` | C2 编译流程控制 |
| `test/hotspot/jtreg/compiler/` | 编译器回归测试 |

---

## 4. 贡献时间线

```
2024:      ████████████████████ (约20) C2 修复, 编译器基础工作
2025:      ██████████████████ (约18) IR Framework 改进, 内联优化
2026:      ██████████ (约7) RepeatCompilation, 方法命名 (截至3月)
```

---

## 5. 技术特长

`C2 编译器` `IR Framework` `内联优化` `Phi 节点` `编译策略` `CompileCommand` `投机类型` `编译器测试` `RepeatCompilation` `形式化方法`

---

## 6. 代表性工作

### 1. IR Framework 方法命名改进
**PR**: [#29520](https://github.com/openjdk/jdk/pull/29520) | **Bug**: [JDK-8376324](https://bugs.openjdk.org/browse/JDK-8376324)

使 IR Framework 中的方法命名方式兼容 CompileCommand，确保编译器测试可以精确匹配目标方法，避免方法名冲突导致的测试失败。

### 2. IR Framework 重载检测与报告
**PR**: [#29483](https://github.com/openjdk/jdk/pull/29483) | **Bug**: [JDK-8376325](https://bugs.openjdk.org/browse/JDK-8376325)

在 IR Framework 中添加方法重载的自动检测和报告机制，帮助开发者在编写编译器测试时避免因方法重载导致的歧义。

### 3. StressIncrementalInlining 随机化处理顺序
**PR**: [#29110](https://github.com/openjdk/jdk/pull/29110) | **Bug**: [JDK-8374622](https://bugs.openjdk.org/browse/JDK-8374622)

扩展 StressIncrementalInlining 功能，使其不仅延迟内联操作，还能随机化处理顺序，从而更有效地暴露内联相关的编译器缺陷。

### 4. Phi 节点投机类型冲突修复
**PR**: [#28331](https://github.com/openjdk/jdk/pull/28331) | **Bug**: [JDK-8371716](https://bugs.openjdk.org/browse/JDK-8371716)

修复 C2 编译器中 Phi 节点在投机类型 (speculative types) 冲突时 Value() 验证失败的问题，提升编译器稳定性。

---

## 7. 技术深度

### C2 编译器和测试基础设施专家

Marc Chevalier 拥有静态分析和形式化方法的学术背景，将这些经验应用于 C2 编译器的内联优化和测试框架改进。

**关键技术领域**:
- IR Framework：编译器中间表示的验证和测试框架
- 内联优化：增量内联、内联策略随机化
- Phi 节点和类型系统：投机类型传播、Value() 验证
- CompileCommand 集成：编译器指令与测试框架的配合
- RepeatCompilation：编译重复策略和 bailout 处理

### 学术背景

Marc Chevalier 于 2020 年在巴黎高等师范学院 (ENS Paris) 获得计算机科学博士学位，研究方向为抽象解释 (Abstract Interpretation)。博士期间致力于改进 Astrée 静态分析器，用于验证嵌入式操作系统的安全属性，解决 C 和汇编混合代码的内存模型统一问题。他曾担任 SAS 2022 和 SAS 2023 Artifact Evaluation Committee 主席。

### 代码风格

- 注重测试基础设施的可靠性和易用性
- 形式化验证思维，确保编译器内部一致性 (源自抽象解释研究背景)
- 对编译器 stress 测试模式的深入理解

---

## 8. 协作网络

### 常见审查者

| 审查者 | 领域 |
|--------|------|
| Christian Hagedorn | C2 编译器, IR Framework |
| Tobias Hartmann | C2 编译器 |
| Vladimir Kozlov | C2 编译器 |
| Emanuel Peter | C2 编译器 |

---

## 9. 历史贡献

### JDK 版本贡献

| JDK 版本 | 主要贡献 |
|----------|----------|
| JDK 23-24 | C2 编译器修复和改进 |
| JDK 25 | IR Framework 增强, 内联策略 |
| JDK 26 | RepeatCompilation 修复, 方法命名 (截至3月) |

### 长期影响

- **IR Framework 改进**：提升编译器测试框架的准确性和可用性
- **内联优化测试**：StressIncrementalInlining 随机化帮助发现潜在内联缺陷
- **编译器正确性**：Phi 节点投机类型修复防止编译崩溃
- **测试可靠性**：CompileCommand 兼容性改进减少测试误报

---

## 10. 外部资源

| 类型 | 链接 |
|------|------|
| **GitHub** | [@marc-chevalier](https://github.com/marc-chevalier) |
| **OpenJDK Census** | [marc-chevalier](https://openjdk.org/census#marc-chevalier) |
| **公司** | [Oracle](https://www.oracle.com/) |
| **个人主页** | [marc-chevalier.com](https://marc-chevalier.com/) |
| **研究主页** | [research.marc-chevalier.com](https://research.marc-chevalier.com/) |
| **Google Scholar** | [Marc Chevalier](https://scholar.google.com/citations?user=LbfW-roAAAAJ) |

### 相关链接

- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=marc-chevalier)
- [GitHub PRs](https://github.com/openjdk/jdk/pulls?q=author%3Amarc-chevalier+is%3Amerged)
- [博士论文: Proving the Security of Software-Intensive Embedded Systems by Abstract Interpretation](https://hal-ens.archives-ouvertes.fr/THESES-ENS/tel-03127921v2)

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-22
> **更新内容**:
> - 初始版本创建
> - 基于 GitHub API 数据: 45 integrated PRs
> - C2 编译器和 IR Framework 为最高频贡献领域
> - 内联优化随机化为最具创新性的改进

## 角色晋升 (CFV)

| 日期 | 角色 | 提名者 | 投票数 | 链接 |
|------|------|--------|--------|------|
| 2025-04-22 | Committer | Tobias Hartmann | 20 | [CFV](https://mail.openjdk.org/pipermail/jdk-dev/2025-April/009978.html) |


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 84 |
| **活跃仓库数** | 2 |
