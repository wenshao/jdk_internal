# Red Hat

> Shenandoah GC 和 AArch64 的主要贡献者

[← 返回组织索引](../../by-contributor/index.md)

---
## 目录

1. [概览](#1-概览)
2. [Top 贡献者](#2-top-贡献者)
3. [主要领域](#3-主要领域)
4. [JEP 贡献](#4-jep-贡献)
5. [关键贡献](#5-关键贡献)
6. [影响的模块](#6-影响的模块)
7. [Red Hat OpenJDK](#7-red-hat-openjdk)
8. [数据来源](#8-数据来源)
9. [相关链接](#9-相关链接)

---


## 1. 概览

Red Hat 是 OpenJDK 的重要贡献者，尤其在 Shenandoah GC、AArch64 移植和 Project Leyden 方面有深厚积累。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 200+ |
| **贡献者数** | 5+ |
| **活跃时间** | 2010+ - 至今 |
| **主要领域** | GC, AArch64, Leyden |
| **OpenJDK** | [Red Hat OpenJDK](https://developers.redhat.com/products/openjdk) |

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。

---

## 2. Top 贡献者

| 排名 | 贡献者 | GitHub | PRs | 角色 | 主要领域 | 档案 |
|------|--------|--------|-----|------|----------|------|
| 1 | Roman Kennke | [@rkennke](https://github.com/rkennke) | 50+ | Reviewer | Shenandoah GC | [详情](../../by-contributor/profiles/roman-kennke.md) |
| 2 | Andrew Dinn | [@adinn](https://github.com/adinn) | 40+ | Reviewer | AArch64 | [详情](../../by-contributor/profiles/andrew-dinn.md) |
| 3 | Aleksey Shipilev | [@shipilev](https://github.com/shipilev) | - | Reviewer | Shenandoah GC (前员工) | [详情](../../by-contributor/profiles/aleksey-shipilev.md) |

**小计**: 90+ PRs

> **注**: 
> - Aleksey Shipilev (Shenandoah GC 创始人) 曾在 Red Hat 工作，现已离职
> - Andrew Dinn (@adinn) 是 Red Hat Distinguished Engineer，专注于 AArch64

---

## 3. 主要领域

### Shenandoah GC

Red Hat 主导 Shenandoah GC 的开发：

- **Roman Kennke**: Shenandoah 核心开发者
- **低暂停时间**: 亚毫秒级 GC 暂停
- **分代 Shenandoah**: JEP 521 贡献

### AArch64 架构

- **Andrew Dinn**: AArch64 移植核心维护者
- **ARM 优化**: SVE 向量指令支持
- **JBoss Byteman**: Project Lead

### Project Leyden

Red Hat 参与 Project Leyden (改善 Java 启动时间):

- 静态 Java 支持
- GraalVM Native 集成
- AOT 编译

---

## 4. JEP 贡献

| JEP | 标题 | 主导者 | 状态 |
|-----|-------|--------|------|
| JEP 189 | Shenandoah GC (Incubator) | Aleksey Shipilev | JDK 12 |
| JEP 379 | Shenandoah GC (Standard) | Aleksey Shipilev | JDK 15 |
| JEP 418 | Internet-Address Resolution SPI | Andrew Dinn | JDK 18 |
| JEP 464 | Scoped Values (Second Preview) | - | JDK 21 |
| JEP 519 | Compact Object Headers | Roman Kennke | JDK 24 |
| JEP 521 | Generational Shenandoah | William Kemper (Amazon) | JDK 25 |

---

## 5. 关键贡献

### Shenandoah GC (Roman Kennke)

| Issue | 标题 | 说明 |
|-------|------|------|
| JEP 519 | Compact Object Headers | 架构改进 |
| 多个 | Shenandoah 优化 | 性能改进 |

### AArch64 (Andrew Dinn)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8275275 | AArch64 SVE 向量指令支持 | 性能优化 |
| 8316971 | AArch64 栈溢出保护优化 | 正确性修复 |

---

## 6. 影响的模块

| 模块 | 文件数 | 说明 |
|------|--------|------|
| Shenandoah GC | 500+ | Shenandoah 垃圾收集器 |
| AArch64 移植 | 100+ | ARM 64 位架构 |
| HotSpot Runtime | 50+ | JVM 运行时 |

---

## 7. Red Hat OpenJDK

Red Hat 维护 OpenJDK 发行版：

| 特性 | 说明 |
|------|------|
| 基于 | OpenJDK |
| 支持 | 长期支持版本 |
| 平台 | RHEL, Fedora, CentOS |
| 许可 | GPLv2 |

---

## 8. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-21

---

## 9. 相关链接

- [Red Hat OpenJDK](https://developers.redhat.com/products/openjdk)
- [Shenandoah GC](https://openjdk.org/projects/shenandoah/)
- [Andrew Dinn @ Red Hat](https://developers.redhat.com/author/andrew-dinn)
- [Roman Kennke @ Red Hat](https://developers.redhat.com/author/roman-kennke)

[→ 返回组织索引](../../by-contributor/index.md)
