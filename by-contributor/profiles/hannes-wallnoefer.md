# Hannes Wallnoefer

> **GitHub**: [@hns](https://github.com/hns)
> **OpenJDK**: [@hannesw](https://wiki.openjdk.org/display/~hannesw)
> **Organization**: Oracle
> **Location**: Austria

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [主要贡献](#3-主要贡献)
4. [贡献统计](#4-贡献统计)
5. [近期活跃 PR](#5-近期活跃-pr)
6. [相关文档](#6-相关文档)

---


## 1. 概述

Hannes Wallnoefer 是 Oracle 的资深软件工程师，是 OpenJDK javadoc 工具的核心维护者和最活跃的贡献者之一。他在 openjdk/jdk 仓库拥有约 550 次贡献，GitHub 上可追踪到 201 个已集成的 PR，其中绝大多数 (93%+) 与 javadoc 工具相关。早期他是 Nashorn JavaScript 引擎的共同开发者，与 Jim Laskey 和 A. Sundararajan 一起负责 Nashorn 的 AST、解析器和运行时实现。

> **数据来源**: [GitHub](https://github.com/hns), [OpenJDK](https://openjdk.org/)

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Hannes Wallnoefer |
| **当前组织** | Oracle |
| **位置** | Austria |
| **GitHub** | [@hns](https://github.com/hns) |
| **OpenJDK** | [@hannesw](https://wiki.openjdk.org/display/~hannesw) |
| **专长** | Javadoc 工具、Nashorn JavaScript 引擎、API 文档生成 |
| **贡献数** | ~550 contributions to openjdk/jdk |

---

## 3. 主要贡献

### Javadoc 工具 (主要领域)

Hannes 是 javadoc 工具 (`jdk.javadoc` 模块) 的核心维护者，负责 API 文档生成工具的功能开发、样式改进和 bug 修复。他的 javadoc 工作涵盖以下几个方面：

#### 文档导航与可用性

| PR | 标题 | 版本周期 |
|----|------|----------|
| [#17062](https://github.com/openjdk/jdk/pull/17062) | 8320458: Improve structural navigation in API documentation | JDK 22 |
| [#23777](https://github.com/openjdk/jdk/pull/23777) | 8350638: Make keyboard navigation more usable in API docs | JDK 25 |
| [#26860](https://github.com/openjdk/jdk/pull/26860) | 8254622: Add the ability to right-click and open in new tab search results | JDK 26 |
| [#24137](https://github.com/openjdk/jdk/pull/24137) | 8352511: Show additional level of headings in table of contents | JDK 25 |
| [#23967](https://github.com/openjdk/jdk/pull/23967) | 8350920: Allow inherited member summaries to be viewed inline | JDK 25 |

#### 暗色主题 (Dark Mode)

| PR | 标题 | 版本周期 |
|----|------|----------|
| [#26185](https://github.com/openjdk/jdk/pull/26185) | 8342705: Add dark mode for docs | JDK 26 |
| [#27191](https://github.com/openjdk/jdk/pull/27191) | 8367321: Fix CSS bugs in dark theme | JDK 26 |
| [#28085](https://github.com/openjdk/jdk/pull/28085) | 8370612: Simplify implementation of dark theme | JDK 26 |
| [#29470](https://github.com/openjdk/jdk/pull/29470) | 8373679: Link color accessibility issue in dark theme | JDK 26 |

#### 代码片段与语法高亮

| PR | 标题 | 版本周期 |
|----|------|----------|
| [#24417](https://github.com/openjdk/jdk/pull/24417) | 8348282: Add option for syntax highlighting in javadoc snippets | JDK 25 |
| [#28354](https://github.com/openjdk/jdk/pull/28354) | 8371896: Links in snippets can not be highlighted | JDK 26 |
| [#27621](https://github.com/openjdk/jdk/pull/27621) | 8276966: Improve diagnostic output for mismatching parts of a hybrid snippet | JDK 26 |

#### 样式与前端改进

| PR | 标题 | 版本周期 |
|----|------|----------|
| [#17633](https://github.com/openjdk/jdk/pull/17633) | 8324774: Add DejaVu web fonts | JDK 23 |
| [#18756](https://github.com/openjdk/jdk/pull/18756) | 8330063: Upgrade jQuery to 3.7.1 | JDK 23 |
| [#23073](https://github.com/openjdk/jdk/pull/23073) | 8347381: Upgrade jQuery UI to version 1.14.1 | JDK 25 |
| [#24007](https://github.com/openjdk/jdk/pull/24007) | 8351626: Update remaining icons to SVG format | JDK 25 |
| [#15969](https://github.com/openjdk/jdk/pull/15969) | 8308659: Use CSS scroll-margin instead of flexbox layout | JDK 22 |

### Nashorn JavaScript 引擎

Hannes 是 Nashorn JavaScript 引擎 (JDK 8-14) 的共同开发者之一，与 Jim Laskey (项目负责人) 和 A. Sundararajan 组成核心开发团队。他主要负责：

- **AST (抽象语法树)**: Nashorn 解析器生成的语法树结构
- **Parser (解析器)**: JavaScript 源码到 AST 的转换
- **Runtime (运行时)**: Nashorn 运行时系统的核心组件

相关 JEP:

| JEP | 标题 | 状态 |
|-----|------|------|
| [JEP 174](https://openjdk.org/jeps/174) | Nashorn JavaScript Engine | JDK 8 正式引入 |
| [JEP 335](https://openjdk.org/jeps/335) | Deprecate the Nashorn JavaScript Engine | JDK 11 废弃 |
| [JEP 372](https://openjdk.org/jeps/372) | Remove the Nashorn JavaScript Engine | JDK 15 移除 |

### @serial 和 @spec 标签补全

Hannes 进行了多次大规模的文档标签修复工作：

| PR | 标题 |
|----|------|
| [#22978](https://github.com/openjdk/jdk/pull/22978) | 8347121: Add missing @serial tags to module java.base |
| [#22979](https://github.com/openjdk/jdk/pull/22979) | 8347122: Add missing @serial tags to module java.desktop |
| [#22980](https://github.com/openjdk/jdk/pull/22980) | 8347123: Add missing @serial tags to other modules |
| [#21326](https://github.com/openjdk/jdk/pull/21326) | 8305406: Add @spec tags in java.base/java.* (part 2) |

---

## 4. 贡献统计

| 指标 | 值 |
|------|-----|
| **总贡献数** | ~550 |
| **已集成 PR (GitHub 可查)** | 201 |
| **javadoc 相关 PR** | 187 (93%) |
| **compiler 相关 PR** | 15 |
| **build 相关 PR** | 12 |
| **core-libs 相关 PR** | 10 |

> 注: 550 次贡献包括 GitHub 迁移前的 Mercurial 提交，GitHub 上可追踪的 PR 为 201 个。

---

## 5. 近期活跃 PR

| PR | 标题 | 合并日期 |
|----|------|----------|
| [#29547](https://github.com/openjdk/jdk/pull/29547) | 8284315: DocTrees.getElement is inconsistent with Elements.getTypeElement | 2026-03-05 |
| [#29470](https://github.com/openjdk/jdk/pull/29470) | 8373679: Link color accessibility issue in dark theme | 2026-01-28 |
| [#28863](https://github.com/openjdk/jdk/pull/28863) | 8309748: Improve host selection in External Specifications page | 2026-02-26 |
| [#28603](https://github.com/openjdk/jdk/pull/28603) | 8372708: Javadoc ignores "-locale" and uses default locale | 2025-12-02 |
| [#28491](https://github.com/openjdk/jdk/pull/28491) | 8369531: Wrong tooltip used in external class links | 2025-11-26 |

---

## 6. 相关文档

### 相关贡献者

- [Jim Laskey](/by-contributor/profiles/jim-laskey.md) - Nashorn 项目负责人，String Templates 作者

### 相关主题

- [Javadoc 工具](/by-topic/tools/javadoc/) - javadoc 工具演进
- [Nashorn](/by-topic/nashorn/) - Nashorn JavaScript 引擎

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-22
> **数据来源**:
> - GitHub API (`gh api users/hns`)
> - GitHub PR 数据 (`gh pr list --repo openjdk/jdk --search "author:hns"`)
> - OpenJDK JEP 数据库
