# 龙芯

> LoongArch 架构移植

[← 返回组织索引](../../by-contributor/README.md)

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
| **Integrated PRs** | 30+ |
| **贡献者数** | 3+ |
| **活跃时间** | 2021 - 至今 |
| **主要领域** | LoongArch |
| **Loongson JDK** | [龙芯 JDK](https://github.com/loongson/jdk) |

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。

---

## 2. 贡献者

| 贡献者 | GitHub | PRs | 角色 | 主要领域 |
|--------|--------|-----|------|----------|
| Zhang Xiaofeng | [@xfeng](https://github.com/xfeng) | 20+ | Author | LoongArch |
| Liu Xinyu | [@liuxinyu](https://github.com/liuxinyu) | 10+ | Author | C2 编译器 |

**小计**: 30+ PRs

> **注**: Fei Yang (@RealFYang) 是 **华为 (Huawei)** 贡献者，专注于 RISC-V，不属于龙芯。@merykitty 是 Quan Anh Mai (独立贡献者)，不是 Fei Yang 的别名。

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

[→ 返回组织索引](../../by-contributor/README.md)
