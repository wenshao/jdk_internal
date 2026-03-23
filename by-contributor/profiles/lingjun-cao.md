# Lingjun Cao

> **DecimalFormat 性能优化贡献者**

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
| **姓名** | Lingjun Cao (曹令军) |
| **GitHub** | [@lingjun-cg](https://github.com/lingjun-cg) |
| **邮箱** | lingjun.cg@alibaba-inc.com |
| **当前组织** | [Alibaba](/contributors/orgs/alibaba.md) |
| **位置** | 杭州 |
| **OpenJDK** | Author |
| **PRs** | [2 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Alingjun-cg+is%3Aclosed+label%3Aintegrated) |
| **社区参与** | [OpenJDK i18n-dev 邮件列表](https://www.mail-archive.com/i18n-dev@openjdk.org/msg03682.html) (DecimalFormat 性能讨论) |
| **Dragonwell** | [Dragonwell8 Extended Edition Release Notes](https://github.com/dragonwell-project/dragonwell8/wiki/Alibaba-Dragonwell8-Extended-Edition-Release-Notes) (PR #635) |
| **主要领域** | DecimalFormat, 性能优化, java.text |
| **活跃时间** | 2024 |
| **其他贡献** | Alibaba Dragonwell (内部 OpenJDK 发行版) |

> **数据来源**: Git commits in openjdk/jdk

---

## 2. 技术影响力

| 指标 | 值 |
|------|-----|
| **Commits** | 2 |
| **主要贡献** | DecimalFormat 性能优化 |

### 影响的主要领域

| 领域 | 贡献数 | 说明 |
|------|--------|------|
| DecimalFormat | 2 | 格式化性能优化 |
| java.text | 2 | Format 类改进 |

---

## 3. 代表性工作

### 1. java.text.Format 内部使用 StringBuilder
**Issue**: [JDK-8333396](https://bugs.openjdk.org/browse/JDK-8333396)

**日期**: 2024-07-22

**问题**: java.text.Format.* 格式化方法内部使用 StringBuffer，由于 StringBuffer 包含大量 synchronized 方法，在 JDK 15+ 移除偏向锁 (biased locking) 后，原子指令出现在热点区域，导致与 JDK 11 相比性能显著下降。

**解决方案**: 内部改用 StringBuilder 替代 StringBuffer，避免不必要的同步开销。该 PR 经历了 20+ 轮 review 迭代，最终集成。

```
最终标题: Use StringBuilder internally for java.text.Format.* formatting
影响: 格式化性能提升，消除热点区域中的原子指令开销
```

### 2. DecimalFormat 构造函数性能回归
**Issue**: [JDK-8333462](https://bugs.openjdk.org/browse/JDK-8333462)

**日期**: 2024-06-05

**问题**: new DecimalFormat() 与 JDK 11 相比性能下降。

**解决方案**: 优化 DecimalFormat 构造函数。

```
影响: DecimalFormat 实例化性能
```

---

## 4. 相关链接

| 类型 | 链接 |
|------|------|
| **JBS Issues** | [lingjun](https://bugs.openjdk.org/issues/?jql=assignee%20%3D%20lingjun) |

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-21
> **更新内容**: 初始创建
