# Joe Darcy

> **OpenJDK**: [@darcy](https://openjdk.org/census#darcy)
> **Organization**: Oracle

---

## 概述

Joe Darcy 是 Oracle 的杰出工程师，长期担任 JDK 核心库的技术负责人。他对 JDK 的贡献涵盖数学库、常量折叠、注解处理等多个领域。

---

## 主要贡献

### JDK 26 (2025-2026)

| PR/Issue | 标题 | 角色 |
|----------|------|------|
| [JDK-8362376](/by-pr/8362/8362376.md) | 在 Java FDLIBM 实现中使用 @Stable 注解 | Author |

### 核心优化领域

| 领域 | 说明 |
|------|------|
| **数学库** | FDLIBM、Math 库优化 |
| **常量折叠** | 编译时常量表达式求值 |
| **JVM 注解** | @Stable、@Contended 等内部注解 |

---

## 分析的 PR

### JDK-8362376: 在 Java FDLIBM 实现中使用 @Stable 注解

在 FDLIBM (Freely Distributable LIBM) 实现中应用 @Stable 注解，启用 JIT 优化，实现 5-15% 的性能提升。

**关键改进**:
- 在查找表数组上添加 `@Stable` 注解
- 启用边界检查消除
- 启用常量折叠
- 改善循环向量化

**技术细节**:
- `__libm_sincos_table` 数组添加 @Stable
- `__libm_exp_table` 数组添加 @Stable
- JIT 可以将数组元素视为常量

**性能影响**:
- 三角函数: +5-10%
- 指数/对数: +3-8%
- 密集计算: +10-15%

**文档**: [详细分析](/by-pr/8362/8362376.md)

---

## 外部资源

### 链接

- **OpenJDK Census**: [darcy](https://openjdk.org/census#darcy)
- **JDK-8362376 Thread**: [Mail Archive](https://mail.openjdk.org/archives/list/jdk-changes@openjdk.org/thread/6W4JAMJLVD4AVRUTCOWAYDLBI5I5PTFH/)

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-20
> **创建原因**: JDK-8362376 PR 分析
