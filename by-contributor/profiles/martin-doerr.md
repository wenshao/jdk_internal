# Martin Doerr

> HotSpot 后端专家，PPC64/s390x 平台移植负责人，JIT 编译器和 CPU 架构支持核心贡献者，SAP JVM 团队成员

---
## 目录

1. [基本信息](#1-基本信息)
2. [职业时间线](#2-职业时间线)
3. [技术影响力](#3-技术影响力)
4. [贡献时间线](#4-贡献时间线)
5. [技术特长](#5-技术特长)
6. [代表性工作](#6-代表性工作)
7. [平台移植工作](#7-平台移植工作)
8. [技术深度](#8-技术深度)
9. [协作网络](#9-协作网络)
10. [历史贡献](#10-历史贡献)
11. [外部资源](#11-外部资源)
12. [相关链接](#12-相关链接)

---


## 1. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Martin Doerr |
| **当前组织** | [SAP](/contributors/orgs/sap.md) |
| **职位** | JVM Developer |
| **位置** | 德国 |
| **GitHub** | [@TheRealMDoerr](https://github.com/TheRealMDoerr) |
| **OpenJDK** | [@mdoerr](https://openjdk.org/census#mdoerr) |
| **角色** | JDK Committer, Reviewer, PowerPC/AIX Port Project Lead |
| **主要领域** | HotSpot 后端, JIT 编译器, PPC64, s390x, AIX, CPU 架构支持 |
| **Contributions (openjdk/jdk)** | 293 |
| **PRs (integrated)** | 147 |
| **活跃时间** | 2020 - 至今 (OpenJDK GitHub 时代) |

> **数据来源**: [GitHub](https://github.com/TheRealMDoerr), [OpenJDK Census](https://openjdk.org/census#mdoerr)

---

## 2. 职业时间线

| 年份 | 事件 | 详情 |
|------|------|------|
| **早期** | 加入 SAP | SAP JVM 团队，专注 HotSpot 后端开发 |
| **~2015** | PowerPC/AIX Port 项目 | 成为 OpenJDK PowerPC/AIX Port Project Lead |
| **2020** | GitHub 时代贡献开始 | 首批 PR 涉及 PPC64 清理、s390x 修复 |
| **2023-2024** | ZGC PPC64 支持 | 为 PPC64 平台实现 ZGC 支持 |
| **2025** | Vector API PPC64 | PPC64 向量寄存器分配和 VSX 性能优化 |
| **至今** | 持续贡献 | HotSpot 后端、JIT 编译器、多平台维护 |

---

## 3. 技术影响力

| 指标 | 值 |
|------|-----|
| **Contributions (openjdk/jdk)** | 293 |
| **PRs (integrated)** | 147 |
| **影响平台** | PPC64, s390x, AIX, x86_64 |
| **影响模块** | HotSpot C1/C2 编译器, 解释器, GC 屏障, 汇编器 |

### 影响的主要目录

| 目录 | 说明 |
|------|------|
| `src/hotspot/cpu/ppc/` | PPC64 平台 HotSpot 后端代码 |
| `src/hotspot/cpu/s390/` | s390x 平台 HotSpot 后端代码 |
| `src/hotspot/os_cpu/aix_ppc/` | AIX/PPC64 平台特定代码 |
| `src/hotspot/share/opto/` | C2 编译器共享代码 |
| `src/hotspot/share/c1/` | C1 编译器共享代码 |

---

## 4. 贡献时间线

```
2020: ████████████████████████ (22) PPC64/s390x 清理和修复
2021: ██████████████████████ (19) 解释器和编译器改进
2022: ████████████████████ (17) 平台维护和 GC 支持
2023: ████████████████████████████ (25) ZGC PPC64, C2 修复
2024: ██████████████████████████████ (29) 寄存器分配, 性能优化
2025: ██████████████████████████████ (29) Vector API, AES 性能
2026: ██████ (6) 持续 PPC64 维护 (截至3月)
```

---

## 5. 技术特长

`PPC64` `s390x` `AIX` `HotSpot 后端` `C1 编译器` `C2 编译器` `JIT` `汇编器` `寄存器分配` `ZGC` `Vector API` `AES 加密` `CPU 架构移植`

---

## 6. 代表性工作

### 1. PPC64 Vector 寄存器支持和 VSX 性能优化
**PR**: [#23987](https://github.com/openjdk/jdk/pull/23987) | **Bug**: [JDK-8351666](https://bugs.openjdk.org/browse/JDK-8351666)

将非易失性 VectorRegister 提供给 C2 寄存器分配器，改善 PPC64 平台上的向量化性能。后续通过 [#25514](https://github.com/openjdk/jdk/pull/25514) 解决 Power8 上 VSX 性能问题。

### 2. ZGC PPC64 支持
**PR**: [#16835](https://github.com/openjdk/jdk/pull/16835) | **Bug**: [JDK-8320807](https://bugs.openjdk.org/browse/JDK-8320807)

修复 PPC64 平台上 C1 编译器生成 ZGC 原子操作的错误代码，确保 ZGC 在 PPC64 上正确运行。多个后续 PR 完善了 ZGC 在 PPC64 上的完整支持。

### 3. AES 性能优化
**PR**: [#28299](https://github.com/openjdk/jdk/pull/28299) | **Bug**: [JDK-8371820](https://bugs.openjdk.org/browse/JDK-8371820)

进一步优化 AES 密钥调度生成的性能，跨平台的加密性能改进。

### 4. x86_64 寄存器打印增强
**PR**: [#21615](https://github.com/openjdk/jdk/pull/21615) | **Bug**: [JDK-8342607](https://bugs.openjdk.org/browse/JDK-8342607)

增强 x86_64 平台上的寄存器打印功能，展示了 Martin 不仅限于 PPC64 的跨平台贡献能力。

---

## 7. 平台移植工作

Martin Doerr 是 OpenJDK **PowerPC/AIX Port** 项目的负责人，承担着确保 HotSpot JVM 在非主流 CPU 架构上正确运行的关键职责。

### 维护平台

| 平台 | 角色 | 说明 |
|------|------|------|
| **PPC64 (Linux)** | Project Lead | 主要维护者，负责编译器后端和运行时 |
| **s390x** | 核心贡献者 | IBM System z 平台支持 |
| **AIX** | 核心贡献者 | IBM AIX 操作系统支持 |

### PR 标题中平台出现频率

| 平台/组件 | PR 数量 |
|-----------|---------|
| PPC64 | 75+ |
| C2 编译器 | 15+ |
| AIX | 13+ |
| C1 编译器 | 8+ |
| ZGC | 6+ |

### 关键职责

- 当共享代码变更破坏 PPC64/s390x 构建时快速修复
- 为新 JVM 特性 (ZGC, Vector API, Loom 等) 提供 PPC64 实现
- 维护 PPC64 特定的内联函数和汇编代码
- 确保 JIT 编译器在非 x86 架构上的正确性

---

## 8. 技术深度

### HotSpot 后端和 JIT 编译器专家

Martin Doerr 的工作集中在 JVM 最底层：CPU 指令生成、寄存器分配、汇编器和运行时支持代码。

**关键技术领域**:
- C1/C2 编译器后端：PPC64 指令选择和寄存器分配
- 汇编器：PPC64 和 s390x 汇编指令实现
- GC 屏障：ZGC、Shenandoah 在 PPC64 上的屏障实现
- 内联函数：AES 加密、字符串操作等 PPC64 特定优化
- Safepoint 机制：平台特定的安全点实现

### 代码风格

- 精确的底层代码，直接操作 CPU 寄存器和指令
- 快速响应共享代码变更对平台构建的破坏
- 注重不同 CPU 代际 (Power8/9/10) 的兼容性
- 跨平台视角，理解 x86_64 和 PPC64 架构差异

---

## 9. 协作网络

### 常见审查者

| 审查者 | 领域 |
|--------|------|
| Goetz Lindenmaier | HotSpot PPC64, SAP 同事 |
| Richard Reingruber | HotSpot 后端, SAP 同事 |
| Vladimir Kozlov | C2 编译器 |
| Roberto Castaneda Lozano | C2 编译器 |

### 常见协作者

| 协作者 | 合作领域 |
|--------|----------|
| Thomas Stuefe | SAP JVM 团队, HotSpot Runtime |
| Amit Kumar | PPC64 平台测试 |
| Lutz Schmidt | SAP JVM 团队, s390x |

---

## 10. 历史贡献

### JDK 版本贡献

| JDK 版本 | 主要贡献 |
|----------|----------|
| JDK 9+ | PowerPC/AIX Port 项目 Lead |
| JDK 16 | PPC64 平台 C1/C2 编译器修复 |
| JDK 21 | ZGC PPC64 支持 |
| JDK 23 | Vector API PPC64 支持 |
| JDK 24 | AES 性能优化, 寄存器分配改进 |
| JDK 25+ | 持续 PPC64 维护和优化 |

### 长期影响

- **PPC64 平台持续可用性**：作为 Project Lead 确保每个 JDK 版本在 PPC64 上正确构建和运行
- **非 x86 架构支持**：为 s390x 和 AIX 提供持续维护
- **新特性平台覆盖**：确保 ZGC、Vector API 等新特性在非主流平台上可用
- **构建稳定性**：快速修复跨平台构建破坏，维护 CI 稳定

---

## 11. 外部资源

| 类型 | 链接 |
|------|------|
| **GitHub** | [@TheRealMDoerr](https://github.com/TheRealMDoerr) |
| **OpenJDK Census** | [mdoerr](https://openjdk.org/census#mdoerr) |
| **公司** | [SAP](https://www.sap.com/) |

---

## 12. 相关链接

- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20mdoerr)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=TheRealMDoerr)
- [GitHub PRs](https://github.com/openjdk/jdk/pulls?q=author%3ATheRealMDoerr+is%3Amerged)
- [OpenJDK PowerPC/AIX Port Project](https://openjdk.org/projects/ppc-aix-port/)

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-22
> **更新内容**:
> - 初始版本创建
> - 基于 GitHub API 数据: 147 integrated PRs, 293 contributions
> - PPC64 为最高频贡献平台 (75+ PRs)
> - SAP JVM 团队成员, PowerPC/AIX Port Project Lead
