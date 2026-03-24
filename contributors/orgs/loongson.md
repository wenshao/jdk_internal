# 龙芯

> LoongArch 架构移植

[← 返回组织索引](README.md)

---
## 目录

1. [概览](#1-概览)
2. [贡献者](#2-贡献者)
3. [主要领域](#3-主要领域)
4. [关键贡献](#4-关键贡献)
5. [Loongson JDK](#5-loongson-jdk)
6. [技术特点](#6-技术特点)
7. [数据来源](#7-数据来源)
8. [相关链接](#8-相关链接)

---


## 1. 概览

龙芯中科参与 OpenJDK 开发，专注于 LoongArch 架构的 JVM 移植和优化。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 36+ |
| **贡献者数** | 3 |
| **活跃时间** | 2021 - 至今 |
| **主要领域** | LoongArch Zero VM, 编译器, 网络 |
| **Loongson JDK** | [龙芯 JDK](https://github.com/loongson/jdk) |

> **统计说明**: 使用 GitHub Integrated PRs 统计。

---

## 2. 贡献者

| 排名 | 贡献者 | GitHub | PRs | 角色 | 主要领域 |
|------|--------|--------|-----|------|----------|
| 1 | SUN Guoyun | [@sunny868](https://github.com/sunny868) | 15 | Author | LoongArch, 网络 |
| 2 | Ao Qi | [@theaoqi](https://github.com/theaoqi) | 14 | Committer | LoongArch Zero VM, 编译器 |
| 3 | Haomin Wang | [@haominw](https://github.com/haominw) | 7 | Author | LoongArch, Vector |

**总计**: 36+ PRs (1 Committer + 2 Author)

> **重要更正**: 之前文档中的 "Zhang Xiaofeng (@xfeng)" 和 "Liu Xinyu (@liuxinyu)" 经核实在上游 OpenJDK (openjdk/jdk) 没有 Integrated PRs，已替换为实际贡献者。
> 发现方法: 通过搜索 `LoongArch` 关键词的 Integrated PRs 反查作者。
>
> **Ao Qi** (@theaoqi): GitHub company=**Loongson**, 北京。代表工作: [JDK-8270517: Add Zero support for LoongArch](https://github.com/openjdk/jdk/pull/)。
>
> **注**: [Fei Yang](../../by-contributor/profiles/fei-yang.md) (@RealFYang) 是 **[华为](huawei.md)** 员工 (RISC-V Port Lead)，不属于龙芯。

---

## 3. 主要领域

### LoongArch 移植

- LoongArch 架构支持
- Zero VM 移植
- JIT 后端开发

### 编译器

- C2 编译器 LoongArch 后端
- 正确性修复

---

## 4. 关键贡献

### LoongArch 架构支持

龙芯贡献了 LoongArch 架构的 OpenJDK 移植，包括：

| 领域 | 说明 |
|------|------|
| Zero VM | 解释器模式移植 |
| 模板解释器 | LoongArch 模板解释器 |
| C1 编译器 | 客户端编译器后端 |
| C2 编译器 | 服务端编译器后端 |

---

## 5. 贡献时间线

```
2021: ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 5 PRs
2022: ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 8 PRs
2023: ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 10 PRs
2024: ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 10 PRs
```

> **总计**: 33 PRs (2021-2024)

---

## 6. Loongson JDK

龙芯维护自己的 JDK 发行版：

| 特性 | 说明 |
|------|------|
| 基于 | OpenJDK |
| 支持 | 长期支持版本 |
| 特点 | LoongArch 原生支持 |
| 许可 | GPLv2 |

**版本**: Loongson JDK 8 / 11 / 17 / 21

---

## 7. 技术特点

### LoongArch 指令集

龙芯的贡献完全聚焦于 LoongArch 架构：

- **LoongArch**: 龙芯自主指令集架构
- **LASX**: 256 位向量扩展
- **LSX**: 128 位向量扩展

---



## 审查者网络

> Loongson 的 PR 被以下审查者审查最多 (共 99 次审查)

| 审查者 | 组织 | 审查次数 |
|--------|------|----------|
| TobiHartmann | Oracle | 8 |
| sunny868 | Loongson | 7 |
| DamonFool | Tencent | 7 |
| vnkozlov | Oracle | 6 |
| erikj79 | Oracle | 4 |
| shipilev | Amazon | 4 |
| theaoqi | Loongson | 4 |
| AlanBateman | Oracle | 4 |

### 审查组织分布

| 审查者组织 | 次数 | 占比 |
|-----------|------|------|
| Oracle | 54 | 55% |
| Loongson | 14 | 14% |
| Tencent | 7 | 7% |
| Amazon | 4 | 4% |
| Red Hat | 4 | 4% |

---

## 8. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-21

---

## 9. 相关链接

- [龙芯 JDK](https://github.com/loongson/jdk)
- [龙芯中科](https://www.loongson.cn/)
- [LoongArch 指令集](https://loongson.github.io/LoongArch-Documentation/README-CN.html)

---

**文档版本**: 1.1
**最后更新**: 2026-03-21
**更新内容**:
- 新增贡献时间线章节

[→ 返回组织索引](README.md)
