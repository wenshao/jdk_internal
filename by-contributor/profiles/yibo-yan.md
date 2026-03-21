# Yibo Yan

> **CPU 监控和内存优化贡献者**

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
| **姓名** | Yibo Yan (颜一波) |
| **邮箱** | yibo.yl@alibaba-inc.com |
| **GitHub** | [@YiboYan](https://github.com/YiboYan) |
| **当前组织** | [Alibaba](../../contributors/orgs/alibaba.md) |
| **角色** | Author |
| **Commits** | 2 |
| **主要领域** | CPU 监控, 内存优化, macOS |
| **活跃时间** | 2023-2024 |

> **数据来源**: Git commits in openjdk/jdk

---

## 2. 技术影响力

| 指标 | 值 |
|------|-----|
| **Commits** | 2 |
| **主要贡献** | CPU Load 修复, 内存优化 |

### 影响的主要领域

| 领域 | 贡献数 | 说明 |
|------|--------|------|
| CPU 监控 | 1 | macOS M1 修复 |
| 内存优化 | 1 | ThreadDump 优化 |

---

## 3. 代表性工作

### 1. Apple M1 CPU Load 修复
**Issue**: [JDK-8326446](https://bugs.openjdk.org/browse/JDK-8326446)

**日期**: 2024-03-08

**问题**: jdk.CPULoad 在 Apple M1 上 User 和 System 值不准确。

**解决方案**: 修复 Apple Silicon 平台的 CPU 负载计算。

```
影响: macOS Apple Silicon 监控准确性
```

### 2. ThreadDump 内存优化
**Issue**: [JDK-8319876](https://bugs.openjdk.org/browse/JDK-8319876)

**日期**: 2023-11-17

**问题**: VM_ThreadDump::doit 内存消耗过高。

**解决方案**: 减少 ThreadDump 操作的内存分配。

```
影响: 大型应用线程转储性能
```

---

## 4. 相关链接

| 类型 | 链接 |
|------|------|
| **JBS Issues** | [yibo](https://bugs.openjdk.org/issues/?jql=assignee%20%3D%20yibo) |

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-21
> **更新内容**: 初始创建
