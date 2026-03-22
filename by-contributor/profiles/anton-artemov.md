# Anton Artemov

> 数学库 (fdlibm) Java 移植开发者，AArch64 帧处理修复专家，ObjectMonitor 代码重构贡献者

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
| **姓名** | Anton Artemov |
| **当前组织** | [Oracle](/contributors/orgs/oracle.md) |
| **职位** | Software Engineer (HotSpot JVM) |
| **位置** | 斯德哥尔摩, 瑞典 |
| **GitHub** | [@toxaart](https://github.com/toxaart) |
| **OpenJDK** | [@toxaart](https://openjdk.org/census#toxaart) |
| **角色** | JDK Committer |
| **主要领域** | 数学库 (fdlibm), AArch64 帧处理, ObjectMonitor |
| **PRs (integrated)** | 29 |
| **活跃时间** | 2024 - 至今 (OpenJDK GitHub 时代) |

> **数据来源**: [GitHub](https://github.com/toxaart), [OpenJDK Census](https://openjdk.org/census#toxaart)

---

## 2. 职业时间线

| 年份 | 事件 | 详情 |
|------|------|------|
| **2024** | 加入 Oracle HotSpot 团队 | 开始 JDK 核心库和运行时贡献 |
| **2025** | fdlibm 数学函数 Java 移植 | acosh, atanh 等反双曲函数 |
| **2026** | AArch64 帧修复和 ObjectMonitor 重构 | 跨领域贡献 |

---

## 3. 技术影响力

| 指标 | 值 |
|------|-----|
| **PRs (integrated)** | 29 |
| **影响模块** | java.lang.Math, AArch64 后端, ObjectMonitor |

### 影响的主要目录

| 目录 | 说明 |
|------|------|
| `src/java.base/share/classes/java/lang/` | Math/StrictMath 类 |
| `src/java.base/share/classes/jdk/internal/math/` | fdlibm Java 实现 |
| `src/hotspot/cpu/aarch64/` | AArch64 平台代码 |
| `src/hotspot/share/runtime/objectMonitor.cpp` | ObjectMonitor 同步原语 |
| `test/jdk/java/lang/Math/` | 数学函数测试 |

---

## 4. 贡献时间线

```
2024:      ██████████████ (约10) 初始贡献, 基础修复
2025:      ██████████████████ (约12) fdlibm 移植 (acosh, atanh), ObjectMonitor
2026:      ██████████ (约7) AArch64 帧修复, 反双曲测试 (截至3月)
```

---

## 5. 技术特长

`fdlibm` `反双曲函数` `acosh` `atanh` `AArch64` `帧处理` `ObjectMonitor` `数学库` `IEEE 754` `栈帧`

---

## 6. 代表性工作

### 1. fdlibm atanh Java 移植
**PR**: [#29782](https://github.com/openjdk/jdk/pull/29782) | **Bug**: [JDK-8377223](https://bugs.openjdk.org/browse/JDK-8377223)

将 fdlibm 的 atanh (反双曲正切) 函数从 C 移植到 Java，作为 JDK 数学库纯 Java 化的一部分，消除对本地代码的依赖。

### 2. AArch64 解释器帧 id 和 is_older 修复
**PR**: [#30020](https://github.com/openjdk/jdk/pull/30020) | **Bug**: [JDK-8294152](https://bugs.openjdk.org/browse/JDK-8294152)

修复 AArch64 平台上解释器帧在 max_stack 较大时 `frame::id()` 和 `frame::is_older()` 返回错误结果的问题，确保栈遍历正确性。

### 3. fdlibm acosh Java 移植
**PR**: [#29488](https://github.com/openjdk/jdk/pull/29488) | **Bug**: [JDK-8376665](https://bugs.openjdk.org/browse/JDK-8376665)

将 fdlibm 的 acosh (反双曲余弦) 函数从 C 移植到 Java，保持 IEEE 754 精度要求。

### 4. ObjectMonitor enter/reenter 代码统一
**PR**: [#29759](https://github.com/openjdk/jdk/pull/29759) | **Bug**: [JDK-8362239](https://bugs.openjdk.org/browse/JDK-8362239)

统一 ObjectMonitor 中 `enter_internal` 和 `reenter_internal` 的实现，消除重复代码，降低同步原语的维护负担。

---

## 7. 技术深度

### 跨领域 JVM 开发者

Anton Artemov 在数学库移植、平台后端和运行时同步等多个 JVM 子领域做出贡献。

**关键技术领域**:
- fdlibm 数学函数：IEEE 754 精度的反双曲函数 Java 实现
- AArch64 帧处理：解释器帧布局、栈遍历、frame id 计算
- ObjectMonitor：Java 同步原语的内部实现
- 最坏情况测试：反双曲函数的边界值测试

### 代码风格

- 精确的数学实现，严格遵循 IEEE 754 标准
- 跨平台意识，关注 AArch64 特定行为
- 代码重构和统一，减少重复逻辑

---

## 8. 协作网络

### 常见审查者

| 审查者 | 领域 |
|--------|------|
| Joe Darcy | 数学库 (fdlibm) |
| Andrew Haley | AArch64 后端 |
| Daniel D. Daugherty | ObjectMonitor |
| Richard Reingruber | 帧处理 |

---

## 9. 历史贡献

### JDK 版本贡献

| JDK 版本 | 主要贡献 |
|----------|----------|
| JDK 23-24 | 初始贡献, 基础修复 |
| JDK 25 | fdlibm acosh/atanh 移植, ObjectMonitor 重构 |
| JDK 26 | AArch64 帧修复, 反双曲函数测试 (截至3月) |

### 长期影响

- **数学库纯 Java 化**：消除 fdlibm 本地代码依赖，提升可移植性和可维护性
- **AArch64 正确性**：帧处理修复确保 ARM64 平台栈遍历可靠
- **同步原语简化**：ObjectMonitor 代码统一降低维护复杂度
- **数学精度保证**：最坏情况测试确保反双曲函数满足精度规范

---

## 10. 外部资源

| 类型 | 链接 |
|------|------|
| **GitHub** | [@toxaart](https://github.com/toxaart) |
| **OpenJDK Census** | [toxaart](https://openjdk.org/census#toxaart) |
| **公司** | [Oracle](https://www.oracle.com/) |

### 相关链接

- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=toxaart)
- [GitHub PRs](https://github.com/openjdk/jdk/pulls?q=author%3Atoxaart+is%3Amerged)

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-22
> **更新内容**:
> - 初始版本创建
> - 基于 GitHub API 数据: 29 integrated PRs
> - fdlibm 数学函数移植为最高频贡献领域
> - AArch64 帧处理修复为最具技术深度的工作
