# Quan Anh Mai

> **Organization**: Shopee Pte. Ltd.
> **Role**: JDK Committer (since September 2022)
> **GitHub**: [@merykitty](https://github.com/merykitty)

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [主要贡献](#3-主要贡献)
4. [技术专长](#4-技术专长)
5. [相关链接](#5-相关链接)

---


## 1. 概述

Quan Anh Mai (GitHub: merykitty) 是 Shopee Pte. Ltd. 的软件工程师，专注于 **HotSpot C2 编译器**优化和性能改进。他于2022年9月被 Vladimir Kozlov 提名并成功当选为 JDK Committer，此前10个月内已贡献23项重要的 HotSpot 变更。他的工作涵盖 C2 编译器节点优化、寄存器分配、Vector API、Foreign Memory Access 以及类型系统约束等领域。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Quan Anh Mai (Quan Anh Mai Dang) |
| **GitHub** | [@merykitty](https://github.com/merykitty) |
| **当前组织** | Shopee Pte. Ltd. |
| **OpenJDK Role** | JDK Committer (since Sept 2022, nominated by Vladimir Kozlov) |
| **专长** | HotSpot C2 Compiler, Vector API, Foreign Memory Access |
| **JDK 26 贡献** | 26 commits |

---

## 3. 主要贡献

### 1. HotSpot C2 编译器优化

Quan Anh Mai 贡献于 HotSpot C2 编译器：
- **C2 Node Optimization**: 移除不必要的控制输入 (LoadKlassNode, LoadNKlassNode)
- **Register Allocation**: 紧密循环中的寄存器分配效率改进
- **ConstraintCastNode**: 运行时正确性验证机制
- **Store Merging**: C2 StoreNode::Ideal_merge_stores 实现
- **TypeInt/TypeLong**: 添加无符号边界和已知位约束

---

## 4. 技术专长

### HotSpot C2 Compiler

- **编译器节点**: Node graph optimization, control flow
- **寄存器分配**: Register allocation improvements
- **向量化**: Vector API, SIMD operations
- **Foreign Memory**: jdk.internal.foreign, SegmentFactories
- **类型系统约束**: TypeInt/TypeLong bounds, ConstraintCast verification

---

## 5. 相关链接

### OpenJDK
- **GitHub**: [merykitty](https://github.com/merykitty)
- **OpenJDK PRs**: [Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Amerykitty+label%3Aintegrated+is%3Aclosed)
- **JDK Committer CFV**: [CFV: New JDK Committer: Quan Anh Mai Dang](https://mail.openjdk.org/pipermail/jdk-dev/2022-September/007010.html)
- [OpenJDK Mailing Lists](https://mail.openjdk.org/) (hotspot-compiler-dev)

---

**Sources**:
- [JDK 26 Top Contributors](./jdk26-top-contributors.md)
- [CFV: New JDK Committer](https://mail.openjdk.org/pipermail/jdk-dev/2022-September/007010.html)


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 209 |
| **活跃仓库数** | 2 |
