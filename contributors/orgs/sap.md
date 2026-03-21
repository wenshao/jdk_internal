# SAP

> PPC 移植、AIX 平台和 HotSpot 调试支持的重要贡献者

[← 返回组织索引](../../by-contributor/index.md)

---
## 目录

1. [概览](#1-概览)
2. [Top 贡献者](#2-top-贡献者)
3. [影响的模块](#3-影响的模块)
4. [主要领域](#4-主要领域)
5. [关键贡献](#5-关键贡献)
6. [SAP JVM (SapMachine)](#6-sap-jvm-sapmachine)
7. [贡献时间线](#7-贡献时间线)
8. [数据来源](#8-数据来源)
9. [相关链接](#9-相关链接)

---


## 1. 概览

SAP 是 OpenJDK 的长期贡献者，专注于 PowerPC (PPC) 移植、AIX 平台支持和 HotSpot 调试能力。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 700+ |
| **贡献者数** | 5+ |
| **活跃时间** | 2010+ - 至今 |
| **主要领域** | PPC 移植, AIX, HotSpot |
| **SapMachine** | [SAP SapMachine](https://sap.github.io/SapMachine/) |

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。OpenJDK Committer 使用 `@openjdk.org` 邮箱提交代码，因此 git commits 按邮箱统计不准确。

---

## 2. Top 贡献者

| 排名 | 贡献者 | GitHub | PRs | 角色 | 领域 | 档案 |
|------|--------|--------|-----|------|------|------|
| 1 | Matthias Baesken | [@MBaesken](https://github.com/MBaesken) | 515 | Reviewer | 构建系统 | [详情](../../by-contributor/profiles/matthias-baesken.md) |
| 2 | Goetz Lindenmaier | [@goetzk](https://github.com/goetzk) | 30+ | Reviewer | HotSpot Runtime | [详情](../../by-contributor/profiles/goetz-lindenmaier.md) |
| 3 | Erik Joelsson | [@eirbjo](https://github.com/eirbjo) | 103 | Committer | 构建系统 | [详情](../../by-contributor/profiles/erik-joelsson.md) |
| 4 | Martin Haessig | [@mhaessig](https://github.com/mhaessig) | 57 | Committer | 测试 | [详情](../../by-contributor/profiles/martin-haessig.md) |
| 5 | Anatoly Zelenin | [@toxaart](https://github.com/toxaart) | 29 | Committer | PPC | [详情](../../by-contributor/profiles/anatoly-zelenin.md) |

**小计**: 734+ PRs

---

## 3. 影响的模块

| 模块 | 文件数 | 说明 |
|------|--------|------|
| PPC 移植 (旧) | 42 | PowerPC 架构支持 (旧路径) |
| PPC 移植 (新) | 30 | PowerPC 架构支持 (新路径) |
| C2 编译器 | 22 | 服务端编译器 |
| HotSpot Runtime | 15 | JVM 运行时 |
| AIX 平台 | 14 | AIX 操作系统支持 |
| ADLC | 12 | 架构描述语言编译器 |
| 构建系统 | 10 | Autoconf 构建配置 |

---

## 4. 主要领域

### PowerPC (PPC) 移植

SAP 主导 PowerPC 架构的 OpenJDK 移植：

- **PPC64**: 64 位 PowerPC 支持
- **PPC64LE**: 小端模式支持
- **JIT 支持**: C2 编译器 PPC 后端

### AIX 平台

- AIX 操作系统支持
- AIX 特定的构建配置
- AIX 线程和内存管理

### HotSpot Runtime

- HotSpot 运行时改进
- GC 和内存管理
- 诊断和监控工具

### 构建系统

- 跨平台构建
- Windows 构建
- AIX 构建

---

## 5. 关键贡献

### 构建系统 (Matthias Baesken, Erik Joelsson)

| Issue | 标题 | 说明 |
|-------|------|------|
| 多个 | 构建系统改进 | 跨平台支持 |
| 多个 | Windows 构建修复 | 平台支持 |

### PPC 移植 (Anatoly Zelenin)

| Issue | 标题 | 说明 |
|-------|------|------|
| 多个 | PPC64 架构支持 | 平台移植 |
| 多个 | C2 编译器后端 | 性能优化 |

### HotSpot Runtime (Goetz Lindenmaier)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8237354 | HotSpot Runtime 服务层重构 | 架构改进 |
| 8278945 | TLAB 优化 | 性能优化 |

---

## 6. SAP JVM (SapMachine)

SAP 维护自己的 JVM 发行版 SapMachine：

| 特性 | 说明 |
|------|------|
| 基于 | OpenJDK |
| 支持 | 长期支持版本 |
| 特点 | 企业级服务性增强 |
| 许可 | GPLv2 |

**额外特性**:
- 增强的诊断能力
- 更好的错误报告
- 企业级监控
- SapMachine Vitals (OS 和 JVM 统计)

**创始人**: Thomas Stuefe (现为 IBM 员工)

---

## 7. 贡献时间线

```
2010: ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 10 PRs
2015: ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 25 PRs
2018: ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 50 PRs
2020: ████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 100 PRs
2022: ████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 150 PRs
2023: ████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 200 PRs
2024: ███████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░ 199 PRs
```

> **总计**: 734+ PRs (2010-2024)

---

## 8. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-21

---

## 9. 相关链接

- [SAP SapMachine](https://sap.github.io/SapMachine/)
- [SAP GitHub](https://github.com/SAP/SapMachine)
- [SapMachine Wiki](https://github.com/SAP/SapMachine/wiki)
- [SAP OpenJDK](https://openjdk.org/groups/hotspot/)

[→ 返回组织索引](../../by-contributor/index.md)
