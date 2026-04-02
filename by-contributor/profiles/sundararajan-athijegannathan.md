# Sundararajan Athijegannathan

> **GitHub**: [@sundararajana](https://github.com/sundararajana)
> **OpenJDK**: [@sundar](https://wiki.openjdk.org/display/~sundar)
> **Organization**: Oracle
> **Location**: Chennai, India

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [关键指标](#3-关键指标)
4. [主要贡献](#4-主要贡献)
5. [代表性 PR](#5-代表性-pr)
6. [相关 JEP](#6-相关-jep)
7. [相关文档](#7-相关文档)

---

## 1. 概述

Sundararajan Athijegannathan (通常简称 "Sundar") 是 Oracle 的资深工程师，对 OpenJDK 有 688 次贡献。他最广为人知的工作是 Nashorn JavaScript 引擎 (JEP 174)，这是 JDK 8 引入的高性能 JavaScript 运行时，用于替代旧的 Rhino 引擎。他也深度参与了 jdk.dynalink 动态链接库、jlink/jmod 工具链以及 jrt 文件系统的开发和维护。

Sundar 在 OpenJDK Census 中担任多个角色：**Detroit 项目负责人 (Project Lead)**、JDK 项目 Reviewer/Committer、JDK Updates Reviewer、Code Tools Committer，以及 HotSpot Group 成员。他也是 Serviceability Group 成员。2026 年 2 月，他提议重建 Detroit 项目，目标是基于 Chrome V8 引擎和 CPython 提供 javax.script API 的实现，将 JavaScript 和 Python 作为 Java 的扩展语言。

> **数据来源**: [GitHub](https://github.com/sundararajana), [OpenJDK](https://openjdk.org/)

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Sundararajan Athijegannathan |
| **当前组织** | Oracle |
| **位置** | Chennai, India |
| **GitHub** | [@sundararajana](https://github.com/sundararajana) |
| **OpenJDK** | [@sundar](https://wiki.openjdk.org/display/~sundar) |
| **专长** | Nashorn JavaScript 引擎, jdk.dynalink, jlink/jmod, jrt 文件系统, javax.script API |
| **OpenJDK 角色** | Detroit Project Lead, JDK Reviewer/Committer, JDK Updates Reviewer, HotSpot Group Member |

---

## 3. 关键指标

| 指标 | 值 |
|------|-----|
| **OpenJDK 贡献数** | 688 |
| **GitHub 集成 PR 数** | 11 (openjdk/jdk 仓库，GitHub 迁移后) |
| **活跃时期** | JDK 8 至今 |
| **主要关注领域** | Nashorn, 脚本引擎, jlink 工具, 内部 API |

> **注**: 688 次贡献中大部分发生在 OpenJDK 迁移到 GitHub 之前 (2020 年以前)，因此 GitHub PR 数量仅反映迁移后的活动。

---

## 4. 主要贡献

### Nashorn JavaScript 引擎

Sundar 是 Nashorn JavaScript 引擎的核心开发者之一。Nashorn 在 JDK 8 中引入 (JEP 174)，是一个基于 `invokedynamic` 的高性能 JavaScript 运行时，用于替代 JDK 6 引入的 Rhino 引擎。Nashorn 实现了 ECMAScript 5.1 规范，并通过 `javax.script` (JSR 223) API 和 `jjs` 命令行工具提供 JavaScript 脚本能力。

Nashorn 在 JDK 11 中被标记为弃用 (JEP 335)，并在 JDK 15 中正式移除 (JEP 372)。

### jdk.dynalink 动态链接库

`jdk.dynalink` 是从 Nashorn 中抽取的通用动态链接框架，提供了在 JVM 上实现动态语言的基础设施。Sundar 负责维护该模块，包括补充 `@since` 标签等文档改进工作。

### jlink / jmod 工具链

在 Nashorn 移除后，Sundar 将工作重心转向 jlink 和 jmod 工具链的维护与改进：

- 修复 jlink 在失败时残留部分输出目录的问题
- 改进 jlink 插件的调试模式
- 清理 jlink 帮助信息中的未文档化选项
- 修复 jmod 处理符号链接的问题
- 修正 jlink 文档中的格式问题

### jrt 文件系统 (jrtfs)

Sundar 维护了 JDK 的 jrt 文件系统实现，修复了多个关键问题：

- `ThreadLocal` 内存泄漏 (`ImageBufferCache`)
- `Path::toUri` 对异常输入抛出 `AssertionError`
- `Files.exists` 调用破坏 JRT 文件系统

---

## 5. 代表性 PR

| PR | 标题 | 合并时间 |
|----|------|----------|
| [#20292](https://github.com/openjdk/jdk/pull/20292) | 8204582: Extra spaces in jlink documentation | 2024-07 |
| [#17305](https://github.com/openjdk/jdk/pull/17305) | 8310995: missing @since tags in 36 jdk.dynalink classes | 2024-01 |
| [#6696](https://github.com/openjdk/jdk/pull/6696) | 8278205: jlink plugins should dump .class file in debug mode | 2021-12 |
| [#4386](https://github.com/openjdk/jdk/pull/4386) | 8240349: jlink should not leave partial image on failure | 2021-06 |
| [#4202](https://github.com/openjdk/jdk/pull/4202) | 8267583: jmod fails on symlink to class file | 2021-05 |
| [#4022](https://github.com/openjdk/jdk/pull/4022) | 8266291: (jrtfs) Files.exists may break JRT filesystem | 2021-05 |
| [#3849](https://github.com/openjdk/jdk/pull/3849) | 8260621: (jrtfs) ThreadLocal memory leak in ImageBufferCache | 2021-05 |
| [#1669](https://github.com/openjdk/jdk/pull/1669) | 8242258: (jrtfs) Path::toUri throws AssertionError | 2020-12 |

---

## 6. 相关 JEP

| JEP | 标题 | 状态 | 关系 |
|-----|------|------|------|
| [JEP 174](https://openjdk.org/jeps/174) | Nashorn JavaScript Engine | JDK 8 正式 | 核心开发者 |
| [JEP 335](https://openjdk.org/jeps/335) | Deprecate the Nashorn JavaScript Engine | JDK 11 弃用 | 相关 |
| [JEP 372](https://openjdk.org/jeps/372) | Remove the Nashorn JavaScript Engine | JDK 15 移除 | 相关 |

---

## 7. 相关文档

### 相关主题

- [jlink 工具](/guides/learning-path.md) - 模块化运行时镜像工具
- [Nashorn](/by-topic/language/lambda/nashorn/) - JavaScript 引擎历史

### 外部资源

- [NashornExamples](https://github.com/sundararajana/NashornExamples) - Sundar 的 Nashorn 示例代码库
- [nashorn (standalone)](https://github.com/sundararajana/nashorn) - 独立 Nashorn 仓库
- [Oracle Blog](https://blogs.oracle.com/sundararajan/) - Sundar 的 Oracle 技术博客，涵盖 Nashorn 脚本相关主题
- [Detroit Project](https://openjdk.org/projects/detroit/) - Sundar 领导的 javax.script API 实现项目 (V8 + CPython)

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-22
> **数据来源**: GitHub API, OpenJDK PR 记录


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 171 |
| **活跃仓库数** | 2 |
