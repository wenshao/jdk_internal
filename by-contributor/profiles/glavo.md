# Glavo

> PLCT Lab (ISCAS) | OpenJDK Author | HMCL 维护者 | Java 性能优化贡献者

---

## 目录

1. [基本信息](#1-基本信息)
2. [职业里程碑](#2-职业里程碑)
3. [OpenJDK 贡献](#3-openjdk-贡献)
4. [开源项目](#4-开源项目)
5. [技术特长](#5-技术特长)
6. [PR 深度分析](#6-pr-深度分析)
7. [相关链接](#7-相关链接)

---

## 1. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Glavo |
| **当前组织** | [PLCT Lab](https://plctlab.org/) (中科院软件所 ISCAS) |
| **位置** | 内蒙古，中国 |
| **GitHub** | [@Glavo](https://github.com/Glavo) (820 followers, 188 repos) |
| **OpenJDK 角色** | Author (JDK Project) |
| **Integrated PRs** | [10](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3AGlavo+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | 核心库性能优化、字符编码、JImage、国际化 (i18n/Locale) |
| **活跃时间** | 2022 - 至今 |
| **知名开源项目** | HMCL (9k⭐)、ClassViewer (278⭐)、Kala Common (63⭐)、JApp (95⭐) |

> **PLCT Lab** (程序语言与编译技术实验室) 是中科院软件所 (ISCAS) 下属团队，专注于 RISC-V 生态的编译器、运行时和模拟器开发。

---

## 2. 职业里程碑

| 日期 | 事件 | 详情 |
|------|------|------|
| **早期** | HMCL 维护者 | 参与维护 Hello Minecraft! Launcher（9k⭐），跨平台 Minecraft 启动器，支持 x86/ARM/MIPS/LoongArch |
| **2022-04** | OpenJDK 首次贡献 | JDK-8284702: 为 `LocalDate.EPOCH` 添加 `@since` 标注 |
| **2023** | 核心库优化高峰 | 贡献 8 个 Integrated PR，涵盖 URLEncoder、String 解码、字符集、Locale |
| **2024-01** | JImage 优化 | JDK-8321620: JImage 解压缩优化 (速度 +21%, 内存 -70%) |
| **至今** | PLCT Lab 成员 | 持续为 Java 在 RISC-V/LoongArch 平台上的适配做贡献 |

---

## 3. OpenJDK 贡献

### 贡献概览

```
2022: █░░░░░░░░░░░░░░░░░░░  1 PR
2023: ████████░░░░░░░░░░░░  8 PRs
2024: █░░░░░░░░░░░░░░░░░░░  1 PR
```

> **总计**: 10 Integrated PRs (2022-2024)

### PR 完整列表

| PR # | Issue | 标题 | 日期 | 影响 |
|------|-------|------|------|------|
| #17405 | JDK-8321620 | Optimize JImage decompressors | 2024-01-15 | 速度 +21%, GC -70% |
| #15354 | JDK-8314774 | Optimize URLEncoder | 2023-09-19 | 吞吐量 +34%, 内存 -76% |
| #15353 | JDK-8317246 | Cleanup URLEncoder/URLDecoder file.encoding usage | 2023-10-03 | 代码清理 |
| #14763 | JDK-8311943 | Cleanup toLowerCase/toUpperCase in java.base | 2023-08-16 | Locale 安全修复 |
| #12697 | JDK-8303024 | WindowsFileSystem.supportedFileAttributeViews use Set.of | 2023-02-22 | 代码清理 |
| #12570 | JDK-8302603 | Use Set.of in java.nio.charset.Charset | 2023-02-21 | 代码清理 |
| #12281 | JDK-8301569 | jmod list/jimage list Turkish locale bug | 2023-06-29 | i18n 修复 |
| #12238 | JDK-8301190 | Vector API LaneType Turkish locale bug | 2023-01-27 | i18n 修复 |
| #12119 | JDK-8299807 | newStringNoRepl avoid copying for ASCII charsets | 2023-03-03 | UTF-8 文件读取 +55% |
| #8192 | JDK-8284702 | Add @since for LocalDate.EPOCH | 2022-04-13 | 文档 |

### 贡献分类

| 类别 | PR 数 | 代表性工作 |
|------|--------|----------|
| **性能优化** | 3 | JImage 解压缩、URLEncoder、String 解码 |
| **i18n/Locale 修复** | 3 | Turkish locale 导致的 toLowerCase 问题 |
| **代码清理** | 3 | Set.of 替换、file.encoding 清理 |
| **文档** | 1 | @since 标注 |

---

## 4. 开源项目

### HMCL (Hello Minecraft! Launcher)

| 属性 | 值 |
|------|-----|
| **GitHub** | [HMCL-dev/HMCL](https://github.com/HMCL-dev/HMCL) |
| **Stars** | 9,000+ |
| **语言** | Java |
| **特点** | 跨平台 (Windows/macOS/Linux)，支持 x86/ARM/MIPS/LoongArch |
| **功能** | Mod 管理、自动安装 Forge/Fabric/Quilt、整合包创建、UI 自定义 |

### 其他项目

| 项目 | Stars | 说明 |
|------|-------|------|
| [ClassViewer](https://github.com/ClassViewer/ClassViewer) | 278 | 轻量级 Java 类文件查看器 |
| [JApp](https://github.com/janex-dev/japp) | 95 | Java 程序新型打包格式 |
| [kala-common](https://github.com/Glavo/kala-common) | 63 | 现代 Java 核心库 |
| [classfile](https://github.com/Glavo/classfile) | - | JDK ClassFile API 的 Java 17 回移版本 |
| [module-info-compiler](https://github.com/Glavo/module-info-compiler) | 17 | module-info.java 编译器 |
| [JetBrains-IDE-Multiarch](https://github.com/Glavo/JetBrains-IDE-Multiarch) | - | JetBrains IDE 的 RISC-V/LoongArch 构建 |
| [java-ffi-benchmark](https://github.com/Glavo/java-ffi-benchmark) | - | Java FFI 性能基准测试 |

---

## 5. 技术特长

| 领域 | 说明 |
|------|------|
| **性能优化** | JImage 解压缩、URLEncoder、String 解码等核心库优化 |
| **国际化 (i18n)** | Turkish locale 问题专家，修复 toLowerCase/toUpperCase 的 Locale 敏感问题 |
| **字节码/ClassFile** | ClassViewer 作者，JDK ClassFile API 回移版本维护者 |
| **跨架构支持** | RISC-V、LoongArch 平台 Java 应用适配 (HMCL, JetBrains IDE) |
| **Java 打包** | JApp 打包格式设计者，熟悉 jmod/jlink/jpackage |
| **Minecraft 生态** | HMCL 维护者，深入理解 Java 桌面应用开发 |

---

## 6. PR 深度分析

### JDK-8321620: JImage 解压缩优化

> **影响**: ⭐⭐⭐⭐⭐ 启动性能优化

优化 `jlink` 创建的 JImage 文件的解压缩过程：

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| **解压缩速度** | 194,237 ns/op | 152,855 ns/op | **+21%** |
| **内存分配** | 243,953 B/op | 74,376 B/op | **-70%** |
| **GC 次数** | 2 次/迭代 | 1 次/迭代 | **-50%** |

**Reviewers**: Mandy Chung, Claes Redestad

### JDK-8314774: URLEncoder 优化

> **影响**: ⭐⭐⭐⭐⭐ Web 框架性能

优化 Java 的 URLEncoder 类，减少不必要的对象分配：

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| **吞吐量** | 5.582 ms/op | 3.681 ms/op | **+34%** |
| **内存分配** | 8,429,374 B/op | 2,000,689 B/op | **-76%** |

**关键优化**:
- 无需编码时直接返回原字符串（fast path）
- BitSet 替换为 boolean 数组（+7-10% 吞吐量）
- 提取 UTF-8 编码逻辑为工具类

**Reviewers**: Claes Redestad, Daniel Fuchs, Roger Riggs

### JDK-8299807: ASCII 字符集 String 解码优化

> **影响**: ⭐⭐⭐⭐ 文件 I/O 性能

避免 `newStringNoRepl` 对 ASCII 兼容字符集（如 UTF-8）不必要的数组复制：

| 场景 | 提升 |
|------|------|
| 1 MiB ASCII 文件 (UTF-8) | **+55%** |
| 小文件 (0-32 KiB) | 无显著变化 |
| 非 ASCII 内容 | 在 4% 以内 |

**Reviewer**: Roger Riggs

---

## 7. 相关链接

### 官方资源

| 资源 | 链接 |
|------|------|
| **GitHub** | [github.com/Glavo](https://github.com/Glavo) |
| **OpenJDK PRs** | [Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3AGlavo+is%3Aclosed+label%3Aintegrated) |
| **PLCT Lab** | [plctlab.org](https://plctlab.org/) |
| **HMCL** | [github.com/HMCL-dev/HMCL](https://github.com/HMCL-dev/HMCL) |
| **ClassViewer** | [github.com/ClassViewer/ClassViewer](https://github.com/ClassViewer/ClassViewer) |

### 代表性 PR

| PR | 说明 |
|----|------|
| [#17405](https://github.com/openjdk/jdk/pull/17405) | JImage 解压缩优化 (+21% 速度, -70% 内存) |
| [#15354](https://github.com/openjdk/jdk/pull/15354) | URLEncoder 优化 (+34% 吞吐量, -76% 内存) |
| [#12119](https://github.com/openjdk/jdk/pull/12119) | ASCII String 解码优化 (+55%) |
| [#12238](https://github.com/openjdk/jdk/pull/12238) | Vector API Turkish locale 修复 |

---

> **数据来源**: [GitHub Profile](https://github.com/Glavo), [OpenJDK PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3AGlavo+label%3Aintegrated), [PLCT Lab](https://plctlab.org/)
>
> **最后更新**: 2026-03-22
