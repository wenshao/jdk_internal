# Xingqi Zheng (MaxXSoft)

> **RISC-V 架构专家，Shenandoah GC 贡献者**

---
## 目录

1. [基本信息](#1-基本信息)
2. [技术影响力](#2-技术影响力)
3. [代表性工作](#3-代表性工作)
4. [相关链接](#4-相关链接)

---


## 1. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Xingqi Zheng (郑兴琪) |
| **GitHub** | [@MaxXSoft](https://github.com/MaxXSoft) |
| **邮箱** | xingqizheng.xqz@alibaba-inc.com |
| **当前组织** | [Alibaba](../../contributors/orgs/alibaba.md) |
| **角色** | Author |
| **Commits** | 2 |
| **主要领域** | RISC-V, Shenandoah GC, 原子操作 |
| **活跃时间** | 2024 |

> **数据来源**: [GitHub](https://github.com/MaxXSoft), Git commits in openjdk/jdk

---

## 2. 技术影响力

| 指标 | 值 |
|------|-----|
| **Commits** | 2 |
| **主要贡献** | RISC-V 架构修复 |

### 影响的主要领域

| 领域 | 贡献数 | 说明 |
|------|--------|------|
| RISC-V | 2 | 架构相关修复 |
| Shenandoah GC | 1 | GC 原子操作修复 |

---

## 3. 代表性工作

### 1. RISC-V Shenandoah GC 原子操作修复
**Issue**: [JDK-8326936](https://bugs.openjdk.org/browse/JDK-8326936)

**日期**: 2024-03-05

**问题**: Shenandoah GC 在 RISC-V 上由于错误的原子内存操作导致崩溃。

**解决方案**: 修复 RISC-V 架构上的原子操作实现。

```
文件: src/hotspot/cpu/riscv/atomic_riscv.hpp
影响: Shenandoah GC 稳定性
```

### 2. RISC-V VM_Version::parse_satp_mode 修复
**Issue**: [JDK-8324280](https://bugs.openjdk.org/browse/JDK-8324280)

**日期**: 2024-01-25

**问题**: RISC-V 上 `VM_Version::parse_satp_mode` 实现不正确。

**解决方案**: 修正 SATP 模式解析逻辑。

```
文件: src/hotspot/cpu/riscv/vm_version_riscv.cpp
影响: RISC-V 平台检测
```

---

## 4. 相关链接

| 类型 | 链接 |
|------|------|
| **GitHub** | [@MaxXSoft](https://github.com/MaxXSoft) |
| **JBS Issues** | [xingqizheng](https://bugs.openjdk.org/issues/?jql=assignee%20%3D%20xingqizheng) |
| **协作者** | Kuai Wei, Yude Lin |

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-21
> **更新内容**: 初始创建
