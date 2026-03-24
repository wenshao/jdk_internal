# Jiangli Zhou

> **CDS/AppCDS 先驱，Static JDK 核心推动者，JVM 静态链接与启动优化专家**

---
## 目录

1. [基本信息](#1-基本信息)
2. [职业历程](#2-职业历程)
3. [技术影响力](#3-技术影响力)
4. [代表性工作](#4-代表性工作)
5. [PR 列表](#5-pr-列表)
6. [开发风格](#6-开发风格)
7. [相关链接](#7-相关链接)

---


## 1. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Jiangli Zhou |
| **当前组织** | [Oracle](../../contributors/orgs/oracle.md) (Java Platform Group) |
| **职位** | HotSpot JVM Engineer |
| **GitHub** | [@jianglizhou](https://github.com/jianglizhou) |
| **OpenJDK** | [@jiangli](https://openjdk.org/census#jiangli) |
| **角色** | OpenJDK Member, JDK Reviewer |
| **PRs** | [66+ integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Ajianglizhou+is%3Aclosed+label%3Aintegrated) |
| **贡献数** | 251 contributions to openjdk/jdk |
| **主要领域** | CDS, AppCDS, Static JDK, 静态链接, 启动优化 |
| **活跃时间** | 2021 - 至今 |

---

## 2. 职业历程

| 时间 | 事件 | 详情 |
|------|------|------|
| **2021** | 开始在 openjdk/jdk 提交 PR | 早期贡献涉及 CDS 子图归档和 G1 Open Archive 区域修复 |
| **2021-06** | G1 Open Archive 关键修复 | PR #4265: 修复 Open Archive 区域 BOT 缺失导致的长暂停 |
| **2023** | 启动 Static JDK 项目 | 开始系统性解决 JDK 原生库静态链接的多重定义问题 |
| **2023-05** | 静态库构建目标 | PR #13768/PR #14064: 添加构建完整 JDK 和 HotSpot 静态库的 make 目标 |
| **2025** | Static JDK 全面推进 | 大量 PR 实现 static JDK 的测试支持、CI 集成和功能兼容 |

---

## 3. 技术影响力

| 指标 | 值 |
|------|-----|
| **总 PR 数** | 66+ integrated |
| **总贡献数** | 251 contributions |
| **2024-2025 PR** | 46 |
| **主要贡献** | Static JDK、静态链接、CDS 归档、启动优化 |

### 影响的主要目录

| 目录 | 说明 |
|------|------|
| make / StaticLibs.gmk | 静态库构建基础设施 |
| cds / runtime | CDS 归档与运行时支持 |
| test / jtreg | 大量 static JDK 测试适配 |
| src/java.base/native | 原生库静态链接兼容 |

---

## 4. 代表性工作

### 1. G1 Open Archive 区域 BOT 修复
**PR**: [#4265](https://github.com/openjdk/jdk/pull/4265) — JDK-8267562: G1: Missing BOT in Open Archive regions causes long pauses

修复 G1 垃圾收集器中 Open Archive 区域缺失 Block Offset Table 条目的问题，该问题会导致 GC 暂停时间异常增长。这是 CDS 堆归档与 GC 交互的关键修复。

### 2. JDK 原生库静态链接基础
**PR**: [#13397](https://github.com/openjdk/jdk/pull/13397) — 8305761: Resolve multiple definition of 'jvm' when statically linking with JDK native libraries
**PR**: [#13438](https://github.com/openjdk/jdk/pull/13438) — 8305858: Resolve multiple definition of 'handleSocketError'
**PR**: [#13497](https://github.com/openjdk/jdk/pull/13497) — 8306033: Resolve multiple definition of 'throwIOException' and friends

系统性解决将 JDK 原生库静态链接时遇到的多重符号定义问题，为 Static JDK 奠定了基础。

### 3. 静态库构建目标
**PR**: [#14064](https://github.com/openjdk/jdk/pull/14064) — 8307858: [REDO] Add make target for optionally building a complete set of all JDK and hotspot libjvm static libraries

添加构建完整 JDK 和 HotSpot 静态库的 make 目标，使开发者能够构建包含所有原生代码的静态库集合，是 Static JDK 的关键构建基础设施。

### 4. Static JDK CI 与测试基础设施
**PR**: [#23471](https://github.com/openjdk/jdk/pull/23471) — 8349399: GHA: Add static-jdk build on linux-x64
**PR**: [#23528](https://github.com/openjdk/jdk/pull/23528) — 8349620: Add VMProps for static JDK
**PR**: [#24992](https://github.com/openjdk/jdk/pull/24992) — 8355452: GHA: Test jtreg tier1 on linux-x64 static-jdk

在 GitHub Actions 中添加 static JDK 的构建和 tier1 测试，并引入 VMProps 属性以便测试框架识别 static JDK 环境，确保持续集成覆盖。

### 5. Static JDK 功能兼容性
**PR**: [#24086](https://github.com/openjdk/jdk/pull/24086) — 8352098: -Xrunjdwp fails on static JDK
**PR**: [#24801](https://github.com/openjdk/jdk/pull/24801) — 8355080: java.base/jdk.internal.foreign.SystemLookup.find() doesn't work on static JDK
**PR**: [#23881](https://github.com/openjdk/jdk/pull/23881) — 8350982: -server|-client causes fatal exception on static JDK

修复 static JDK 中调试器代理、Foreign Function API、VM 模式选择等功能的兼容性问题，逐步使 static JDK 达到与标准 JDK 相当的功能覆盖。

### 6. SymbolTable 挂起修复
**PR**: [#14938](https://github.com/openjdk/jdk/pull/14938) — 8312401: SymbolTable::do_add_if_needed hangs when called with requesting length exceeds max_symbol_length

修复 SymbolTable 在符号长度超限时的挂起问题，属于 JVM 运行时核心的关键稳定性修复。

---

## 5. PR 列表

### 近期代表性 PRs (2025)

| PR | 标题 | 日期 |
|----|------|------|
| [#28363](https://github.com/openjdk/jdk/pull/28363) | 8371864: AES-GCM encryption failure for certain payload sizes | 2025-12 |
| [#26565](https://github.com/openjdk/jdk/pull/26565) | 8362564: TestLWLockingCodeGen fails on static JDK with AVX | 2025-07 |
| [#25516](https://github.com/openjdk/jdk/pull/25516) | 8357632: CDS test failures on static JDK | 2025-06 |
| [#24992](https://github.com/openjdk/jdk/pull/24992) | 8355452: GHA: Test jtreg tier1 on linux-x64 static-jdk | 2025-05 |
| [#24934](https://github.com/openjdk/jdk/pull/24934) | 8355669: Add static-jdk-bundles make target | 2025-04 |
| [#24801](https://github.com/openjdk/jdk/pull/24801) | 8355080: SystemLookup.find() on static JDK | 2025-04 |
| [#24086](https://github.com/openjdk/jdk/pull/24086) | 8352098: -Xrunjdwp fails on static JDK | 2025-03 |
| [#23881](https://github.com/openjdk/jdk/pull/23881) | 8350982: -server\|-client fatal exception on static JDK | 2025-03 |
| [#23528](https://github.com/openjdk/jdk/pull/23528) | 8349620: Add VMProps for static JDK | 2025-02 |
| [#23471](https://github.com/openjdk/jdk/pull/23471) | 8349399: GHA: Add static-jdk build on linux-x64 | 2025-02 |

---

## 6. 开发风格

Jiangli 的贡献特点:

1. **Static JDK 主导者**: 几乎独力推动了 JDK 静态链接项目，从底层符号冲突解决到构建系统再到 CI 集成，覆盖完整栈
2. **系统性工程方法**: 面对静态链接兼容性问题时，采用逐模块解决策略，methodically 消除每个原生库的冲突
3. **CDS 先驱**: 早期工作涵盖 CDS 归档堆对象与 GC 交互，为 AppCDS 功能奠定基础
4. **测试驱动**: 大量 PR 专注于让现有测试在 static JDK 上正确运行，确保功能回归覆盖
5. **协作紧密**: 与 [Ioi Lam](./ioi-lam.md) 和 [Calvin Cheung](./calvin-cheung.md) 共同推进 CDS 生态

---

## 7. 相关链接

| 类型 | 链接 |
|------|------|
| **GitHub** | [@jianglizhou](https://github.com/jianglizhou) |
| **OpenJDK Census** | [jiangli](https://openjdk.org/census#jiangli) |
| **PR 列表** | [openjdk/jdk PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Ajianglizhou+is%3Aclosed+label%3Aintegrated) |
| **协作者** | [Ioi Lam](./ioi-lam.md) — CDS 核心搭档 |
| **协作者** | [Calvin Cheung](./calvin-cheung.md) — CDS/AppCDS 搭档 |

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-22
> **更新内容**: 初始版本创建


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 49 |
| **活跃仓库数** | 3 |
