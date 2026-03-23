# ISCAS PLCT

> RISC-V 架构 JVM 移植和核心库优化

[← 返回组织索引](README.md)

---
## 目录

1. [概览](#1-概览)
2. [贡献者](#2-贡献者)
3. [主要领域](#3-主要领域)
4. [贡献时间线](#4-贡献时间线)
5. [技术特点](#5-技术特点)
6. [演讲和会议](#6-演讲和会议)
7. [数据来源](#7-数据来源)
8. [相关链接](#8-相关链接)

---


## 1. 概览

中科院软件所 PLCT 实验室（Programming Language & Compilation Technology Laboratory）参与 OpenJDK 开发，专注于 RISC-V 架构的 JVM 移植和性能优化。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 64+ |
| **贡献者数** | 2+ |
| **活跃时间** | 2023 - 至今 |
| **主要领域** | RISC-V, 核心库 |
| **位置** | 杭州 |
| **PLCT Lab** | [plctlab.org](https://plctlab.org/) |

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。

---

## 2. 贡献者

| 贡献者 | GitHub | PRs | 角色 | 主要领域 | 档案 |
|--------|--------|-----|------|----------|------|
| Dingli Zhang (张定立) | [@DingliZhang](https://github.com/DingliZhang) | 54 | Committer | RISC-V | - |
| Glavo | [@Glavo](https://github.com/Glavo) | 10 | Author | 核心库, 国际化, NIO, JavaFX | - |

**总计**: 64+ PRs

### Dingli Zhang (张定立) — RISC-V 核心贡献者

Dingli Zhang 是 ISCAS PLCT 实验室的 RISC-V 工程师 (dingli@iscas.ac.cn)，参与了 OpenJDK RISC-V Port 的早期开发。他与华为毕昇 JDK 团队合作，将 Template Interpreter 和 C1/C2 编译器后端带到 RISC-V 平台。他的上游贡献集中在 RISC-V 架构特定的 HotSpot 优化。

### Glavo — 核心库与多架构支持

Glavo 是 PLCT 实验室成员 (GitHub @plctlab)，位于内蒙古。除了 OpenJDK 核心库贡献外，他还维护 [JetBrains-IDE-Multiarch](https://github.com/Glavo/JetBrains-IDE-Multiarch)（为 RISC-V/LoongArch 构建 JetBrains IDE），也贡献了 OpenJFX 项目。

> **注**:
> - [Fei Yang (杨飞)](../../by-contributor/profiles/fei-yang.md) 是 **[华为 (Huawei)](huawei.md)** 员工 (RISC-V Port Project Lead)
> - [Anjian-Wen](../../by-contributor/profiles/anjian-wen.md) 是 **[字节跳动](bytedance.md)** 员工
> - PLCT 实验室参与了华为主导的 JEP 422 (RISC-V Port) 的早期协作开发

---

## 3. 主要领域

### RISC-V 优化

- RISC-V 向量指令支持 (RVV)
- RISC-V 扩展检测和自动启用
- 性能分析和优化
- 测试稳定性

### 关键贡献

| Issue | 标题 | 贡献者 | 说明 |
|-------|------|--------|------|
| 多个 | RISC-V 移植和优化 | Yadong Wang | 基础支持 |

---

## 4. 贡献时间线

```
2023: ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 5 PRs
2024: ████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░ 10 PRs
2025: ███████████████████████████████████████████████████████████░░░ 5+ PRs
```

> **总计**: 20+ PRs (2023-2026)

---

## 5. 技术特点

### RISC-V 扩展支持

| 扩展 | 说明 |
|------|------|
| **V** | 向量扩展 (RVV) |
| **Zvbb** | 向量位操作 |
| **Zfa** | 附加浮点指令 |
| **Zicsr** | CSR 指令 |

---

## 6. 演讲和会议

| 会议 | 主题 | 日期 |
|------|------|------|
| **RISC-V 中国峰会 2023** | OpenJDK RISC-V 移植进展 | 2023-08 |
| **RISC-V 杭州 2024** | OpenJDK RISC-V 平台进展 | 2024 |
| **PLCT Lab 开放日** | RISC-V 平台上 Java 性能分析 | 2024 |

---

## 7. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-21

---

## 8. 相关链接

- [PLCT Lab](https://plctlab.org/)
- [2024 RISC-V China Summit](https://plctlab.org/zh/news/050/)
- [OpenJDK RISC-V Port (JEP 422)](https://openjdk.org/jeps/422)

[→ 返回组织索引](../../by-contributor/README.md)
