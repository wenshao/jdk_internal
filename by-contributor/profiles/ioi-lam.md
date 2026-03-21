# Ioi Lam

> AOT/CDS 核心开发者，JEP 514 主导者，Project Leyden 演讲者

---
## 目录

1. [基本信息](#1-基本信息)
2. [职业时间线](#2-职业时间线)
3. [语言能力](#3-语言能力)
4. [技术影响力](#4-技术影响力)
5. [技术特长](#5-技术特长)
6. [代表性工作](#6-代表性工作)
7. [外部资源](#7-外部资源)
8. [贡献概览](#8-贡献概览)
9. [PR 列表](#9-pr-列表)
10. [关键贡献详解](#10-关键贡献详解)
11. [开发风格](#11-开发风格)
12. [相关链接](#12-相关链接)

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
| **角色** | OpenJDK Member, JDK Reviewer, HSX Committer (2013-04) |
| **PRs** | [431+ integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Aiklam+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | AOT, CDS, 启动优化, Project Leyden |
| **主导 JEP** | JEP 514: Ahead-of-Time Command Line Ergonomics |
| **活跃时间** | 2013 - 至今 |

> **数据来源**: [LinkedIn](https://www.linkedin.com/in/ioi-lam-3b07731), [CFV HSX Committer](https://mail.openjdk.org/pipermail/hotspot-dev/2013-April/009124.html), [JVMLS Leyden](https://inside.java/2024/08/25/jvmls-leyden/)

### 最近 10 个 Integrated PRs (2026 年 2-3 月)

| PR # | Issue | 标题 | 日期 |
|------|-------|------|------|
| #29947 | 8378211 | Test ChangedJarFile.java failed: missing "timestamp has changed" | Mar 17, 2026 |
| #29869 | 8376822 | UseCompactObjectHeaders: fill Klass alignment gaps in AOT cache | Mar 17, 2026 |
| #29834 | 8378298 | Remove obsolete CDS string tests | Feb 21, 2026 |
| #29825 | 8377512 | AOT cache creation fails with invalid native pointer | Mar 17, 2026 |
| #29778 | 8378152 | Upstream AOT heap object improvements from Leyden repo | Mar 17, 2026 |
| #29728 | 8377932 | AOT cache is not rejected when JAR file has changed | Feb 16, 2026 |
| #29678 | 8377712 | ConstantPool of WeakReferenceKey is not deterministic in CDS archive | Feb 19, 2026 |
| #29590 | 8377307 | Refactor code for AOT cache pointer compression | Feb 11, 2026 |
| #29549 | 8377096 | Refactor AOTMapLogger::OopDataIterator implementations | Feb 10, 2026 |
| #29472 | 8375569 | Store Java mirrors in AOT configuration file | Jan 29, 2026 |

> **观察**: 最近工作集中在 **AOT 缓存优化**、**CDS 改进** 和 **Project Leyden 上游合并**

---

## 2. 职业时间线

| 年份 | 事件 | 详情 |
|------|------|------|
| **2013-04** | HSX Committer | 被 Volker Simonis 提名为 HSX Committer |
| **2013-至今** | Oracle HotSpot Engineer | Java Platform Group |
| **2018-至今** | AppCDS 主要贡献者 | Application Class Data Sharing 核心开发 |
| **2024** | Project Leyden 演讲 | JVM Language Summit 2024 与 Dan Heidinga 一起展示 |
| **2024-2025** | JEP 514 | AOT 命令行人体工程学主导者 |

---

## 3. 语言能力

| 语言 | 熟练度 |
|------|--------|
| **英语** | Native/Bilingual |
| **中文** | Native/Bilingual |
| **日语** | Professional Working Proficiency |

---

## 4. 技术影响力

| 指标 | 值 |
|------|-----|
| **代码行数** | +109,076 / -76,495 (净 +32,581) |
| **影响模块** | hotspot (CDS, classfile) |
| **主要贡献** | AOT 优化、CDS 改进、启动优化 |

### 影响的主要目录

| 目录 | 文件数 | 说明 |
|------|--------|------|
| cds | 1,139 | CDS (Class Data Sharing) |
| classfile | 783 | 类文件加载 |
| oops | 444 | 对象模型 |

---

## 5. 技术特长

`AOT` `CDS` `启动优化` `类加载` `内存映射` `确定性归档`

---

## 6. 代表性工作

### 1. JEP 514: Ahead-of-Time Command Line Ergonomics
**Issue**: [JDK-8345169](https://bugs.openjdk.org/browse/JDK-8345169)

简化 AOT 配置，提供更好的命令行人体工程学。

### 2. CDS (Class Data Sharing) 核心贡献者
CDS 功能的主要开发者，显著提升应用启动速度。

### 3. 确定性归档地址
实现 CDS 归档的确定性地址分配，提升可重现性。

### 4. AOT 类预加载
AOT 编译类的预加载优化，减少启动时间。

### 5. Leyden 项目贡献
为 Leyden 项目 (提前编译) 做出重要贡献。

---

## 7. 外部资源

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
| **Patents** | [Justia Patents](https://patents.justia.com/inventor/ioi-lam) |

---

## 8. 贡献概览

### 按类别统计

| 类别 | 数量 | 占比 |
|------|------|------|
| AOT 优化 | 60 | 55% |
| CDS 改进 | 30 | 28% |
| 测试修复 | 15 | 14% |
| 其他 | 4 | 3% |

### 关键成就

- **JEP 514**: AOT 命令行人体工程学
- **CDS 改进**: 确定性归档地址
- **启动优化**: AOT 类预加载

---

## 9. PR 列表

### JEP 514: AOT Command Line Ergonomics

| Issue | 标题 | 描述 |
|-------|------|------|
| 8355798 | Implement JEP 514: Ahead-of-Time Command Line Ergonomics | **核心实现** |

### AOT 类链接

| Issue | 标题 | 描述 |
|-------|------|------|
| 8369742 | Link AOT-linked classes at JVM bootstrap | JVM 启动时链接 AOT 类 |
| 8369856 | AOT map does not include unregistered classes | 未注册类处理 |
| 8317269 | Store old classes in linked state in AOT cache | 旧类链接状态存储 |
| 8368174 | Proactive initialization of @AOTSafeClassInitializer classes | 主动初始化安全类 |
| 8350550 | Preload classes from AOT cache during VM bootstrap | VM 启动时预加载 |

### CDS 改进

| Issue | 标题 | 描述 |
|-------|------|------|
| 8363986 | Heap region in CDS archive is not at deterministic address | **确定性地址** |

---

## 10. 关键贡献详解

### 1. JEP 514: AOT Command Line Ergonomics

**背景**: AOT 缓存使用复杂，需要手动指定许多参数。

**解决方案**: 简化命令行，自动检测和配置。

```bash
# 变更前: 复杂的命令
java -XX:ArchiveClassesAtExit=app.aot \
     -XX:SharedArchiveFile=base.aot \
     -cp myapp.jar MyApp

# 变更后: 简化的命令
java -XX:ArchiveClassesAtExit=app.aot -cp myapp.jar MyApp
java -XX:SharedArchiveFile=app.aot -cp myapp.jar MyApp
```

**影响**: 启动时间减少 30-50%。

---

## 11. 开发风格

Ioi 的贡献特点:

1. **性能导向**: 专注于启动时间和内存占用
2. **系统级理解**: 深入理解 JVM 内部机制
3. **渐进式改进**: 大改动拆分为多个小 commit
4. **测试覆盖**: 每个改动都有充分的测试

---

## 12. 相关链接

- [OpenJDK Changesets](https://hg.openjdk.org/jdk/jdk/user?user=iklam)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=Ioi%20Lam)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=assignee%20%3D%20iklam)
- [Blog: AOT & CDS](https://medium.com/@ioilam)

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-21
> **更新内容**: 初始创建
