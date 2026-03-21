# Ioi Lam

> **AOT/CDS 核心开发者，JEP 514 主导者，Project Leyden 演讲者**

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
| **姓名** | Ioi Lam |
| **当前组织** | [Oracle](../../contributors/orgs/oracle.md) (Java Platform Group) |
| **职位** | HotSpot JVM Engineer |
| **位置** | Mountain View, California, 美国 |
| **GitHub** | [@iklam](https://github.com/iklam) |
| **LinkedIn** | [ioi-lam-3b07731](https://www.linkedin.com/in/ioi-lam-3b07731) |
| **OpenJDK** | [@iklam](https://openjdk.org/census#iklam) |
| **角色** | OpenJDK Member, JDK Reviewer, HSX Committer |
| **PRs** | [431+ integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Aiklam+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | AOT, CDS, 启动优化, Project Leyden |
| **主导 JEP** | JEP 514: Ahead-of-Time Command Line Ergonomics |
| **活跃时间** | 2013 - 至今 |
| **代表仓库** | [github.com/iklam](https://github.com/iklam) (jdk, valhalla, tools) |

> **数据来源**: [LinkedIn](https://www.linkedin.com/in/ioi-lam-3b07731), [CFV HSX Committer](https://mail.openjdk.org/pipermail/hotspot-dev/2013-April/009124.html), [JVMLS Leyden](https://inside.java/2024/08/25/jvmls-leyden/)

---

## 2. 职业历程

| 时间 | 事件 | 详情 |
|------|------|------|
| **2013-04** | HSX Committer | 被 Volker Simonis 提名为 HSX Committer |
| **2013-至今** | Oracle HotSpot Engineer | Java Platform Group, Mountain View |
| **2018-至今** | AppCDS 主要贡献者 | Application Class Data Sharing 核心开发 |
| **2024** | Project Leyden 演讲 | JVM Language Summit 2024 与 Dan Heidinga 一起展示 |
| **2024-2025** | JEP 514 | AOT 命令行人体工程学主导者 |
| **JDK 26** | 76 commits | AOT/CDS 领域排名第 1 |

---

## 3. 技术影响力

| 指标 | 值 |
|------|-----|
| **代码行数** | +109,076 / -76,495 (净 +32,581) |
| **影响模块** | hotspot (CDS, classfile) |
| **JDK 26 排名** | #7 (76 commits) |
| **主要贡献** | AOT 优化、CDS 改进、启动优化 |

### 影响的主要目录

| 目录 | 文件数 | 说明 |
|------|--------|------|
| cds | 1,139 | CDS (Class Data Sharing) |
| classfile | 783 | 类文件加载 |
| oops | 444 | 对象模型 |

---

## 4. 代表性工作

### 1. JEP 514: Ahead-of-Time Command Line Ergonomics
**Issue**: [JDK-8345169](https://bugs.openjdk.org/browse/JDK-8345169)

简化 AOT 配置，提供更好的命令行人体工程学，实现 **JVM 启动时间 -30~50%**。

```bash
# 变更前: 复杂的命令
java -XX:ArchiveClassesAtExit=app.aot \
     -XX:SharedArchiveFile=base.aot \
     -cp myapp.jar MyApp

# 变更后: 简化的命令
java -XX:ArchiveClassesAtExit=app.aot -cp myapp.jar MyApp
```

### 2. CDS (Class Data Sharing) 核心贡献者
CDS 功能的主要开发者，显著提升应用启动速度。

### 3. 确定性归档地址
实现 CDS 归档的确定性地址分配，提升可重现性。

### 4. AOT 类预加载
AOT 编译类的预加载优化，减少启动时间。

### 5. Leyden 项目贡献
为 Leyden 项目 (提前编译) 做出重要贡献。

---

## 5. PR 列表

### JDK 26 Top PRs

| Issue | 标题 | 变更行数 | 描述 |
|-------|------|----------|------|
| 8362566 | AOT map logging | 1,776 | AOT 映射日志输出 |
| 8374549 | MetaspaceClosure extend | 1,373 | 扩展 MetaspaceClosure |
| 8350550 | Preload classes from AOT | 1,110 | VM 启动时预加载 AOT 类 |
| 8317269 | Store old classes in linked state | 1,569 | 旧类链接状态存储 |
| 8373392 | Replace CDS object subgraphs | 692 | 替换 CDS 对象子图 |

### JEP 514: AOT Command Line Ergonomics

| Issue | 标题 | 描述 |
|-------|------|------|
| 8355798 | Implement JEP 514 | **核心实现** |
| 8369742 | Link AOT-linked classes at bootstrap | JVM 启动时链接 AOT 类 |
| 8363986 | Heap region deterministic address | **确定性地址** |

---

## 6. 开发风格

Ioi 的贡献特点:

1. **性能导向**: 专注于启动时间和内存占用
2. **系统级理解**: 深入理解 JVM 内部机制
3. **渐进式改进**: 大改动拆分为多个小 commit
4. **测试覆盖**: 每个改动都有充分的测试
5. **文档完善**: 详细的代码注释和设计文档

---

## 7. 相关链接

| 类型 | 链接 |
|------|------|
| **GitHub** | [@iklam](https://github.com/iklam) |
| **LinkedIn** | [ioi-lam-3b07731](https://www.linkedin.com/in/ioi-lam-3b07731) |
| **OpenJDK Census** | [iklam](https://openjdk.org/census#iklam) |
| **YouTube** | [AppCDS Presentation](https://www.youtube.com/watch?v=nniYSR4GAH4) |
| **Project Leyden JVMLS** | [Inside.java](https://inside.java/2024/08/25/jvmls-leyden/) |
| **AppCDS Wiki** | [OpenJDK Wiki](https://wiki.openjdk.org/spaces/HotSpot/pages/49250346/Application+Class+Data+Sharing+-+AppCDS) |
| **HSX CFV** | [hotspot-dev](https://mail.openjdk.org/pipermail/hotspot-dev/2013-April/009124.html) |
| **Blog** | [Medium @ioilam](https://medium.com/@ioilam) |

---

> **文档版本**: 2.0
> **最后更新**: 2026-03-21
> **更新内容**: 添加 JDK 26 PRs、JEP 514 详情、开发风格
