# Johannes Graham

> **GitHub**: [@j3graham](https://github.com/j3graham)
> **OpenJDK**: [@j3graham](https://openjdk.org/census#j3graham)
> **Location**: United States
> **Organization**: Oracle

---
## 目录

1. [概述](#1-概述)
2. [主要贡献](#2-主要贡献)
3. [分析的 PR](#3-分析的-pr)
4. [外部资源](#4-外部资源)

---


## 1. 概述

Johannes Graham 是 Oracle 的 C2 编译器工程师，专注于 JIT 编译器优化。他的主要贡献集中在编译器中间表示（IR）和优化阶段的改进。

---

## 2. 主要贡献

### JDK 26 (2025-2026)

| PR/Issue | 标题 | 角色 |
|----------|------|------|
| [JDK-8347645](/by-pr/8347/8347645.md) | C2 XOR 有界值处理阻止常量折叠 | Author |

### 核心优化领域

| 领域 | 说明 |
|------|------|
| **C2 编译器** | JIT 编译器优化 |
| **常量折叠** | 编译时表达式求值 |
| **IR 节点优化** | XorINode, XorLNode 等节点优化 |

---

## 3. 分析的 PR

### JDK-8347645: C2 XOR 有界值处理阻止常量折叠

修复了 C2 编译器中 XOR 操作的有界值优化阻止常量折叠的问题。

**关键改进**:
- 调整优化优先级：常量折叠优先于有界值优化
- 恢复 XOR 操作的常量折叠能力
- 修复了 `x ^ 0` 类表达式的编译时求值

**技术细节**:
- 修改 `XorINode::Value()` 和 `XorLNode::Value()`
- 在返回有界值之前先尝试常量折叠
- 确保常见模式（如 `x ^ 0`, `x ^ -1`）被正确优化

**文档**: [详细分析](/by-pr/8347/8347645.md)

---

## 4. 外部资源

### 链接

- **GitHub**: [https://github.com/j3graham](https://github.com/j3graham)
- **OpenJDK Census**: [j3graham](https://openjdk.org/census#j3graham)
- **JDK-8347645 PR**: [#23089](https://github.com/openjdk/jdk/pull/23089)

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-20
> **创建原因**: JDK-8347645 PR 分析
