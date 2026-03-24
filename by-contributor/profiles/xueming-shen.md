# Xueming Shen (沈学明)

> **OpenJDK**: [@sherman](https://openjdk.org/census#sherman)
> **LinkedIn**: [xueming-shen-8091388](https://www.linkedin.com/in/xueming-shen-8091388/)
> **Organization**: Oracle
> **Role**: Core Libraries Engineer, String/Charset/Zip Expert

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [职业历程](#3-职业历程)
4. [主要 JEP 贡献](#4-主要-jep-贡献)
5. [核心技术贡献](#5-核心技术贡献)
6. [技术专长](#6-技术专长)
7. [协作网络](#7-协作网络)
8. [相关链接](#8-相关链接)

---


## 1. 概述

Xueming Shen (沈学明，OpenJDK 用户名: **sherman**) 是 Oracle 的 **Core Libraries 工程师**，在 String、Charset、NIO、Zip/Jar 处理和正则表达式等多个基础库领域拥有深厚的技术积累。他是 **JEP 254 (Compact Strings)** 的 Owner，该 JEP 是 JDK 9 中最具影响力的性能优化之一，将 String 对象在仅包含 Latin-1 字符时的内存占用减少了 50%。他毕业于上海交通大学，长期在 Oracle (原 Sun Microsystems) 从事 Java 核心库开发。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Xueming Shen (沈学明) |
| **当前组织** | Oracle Corporation |
| **职位** | Core Libraries Engineer |
| **位置** | San Francisco Bay Area |
| **LinkedIn** | [xueming-shen-8091388](https://www.linkedin.com/in/xueming-shen-8091388/) |
| **OpenJDK** | [@sherman](https://openjdk.org/census#sherman) |
| **角色** | OpenJDK Reviewer, Committer |
| **专长** | String, Charset, Jar/Zip, Regular Expression, Font Rendering, Unicode, NIO |
| **教育背景** | 上海交通大学 (Shanghai Jiao Tong University) |

> **数据来源**: [LinkedIn](https://www.linkedin.com/in/xueming-shen-8091388/), [OpenJDK Census](https://openjdk.org/census), [JEP 254](https://openjdk.org/jeps/254)

---

## 3. 职业历程

| 时间 | 事件 | 详情 |
|------|------|------|
| **早期** | 上海交通大学毕业 | 计算机科学相关专业 |
| **~2000s** | 加入 Sun Microsystems / Oracle | Java Core Libraries 团队 |
| **持续** | Charset 子系统重构 | JDK-6653797: 重新实现 JDK charset 仓库 charsets.jar |
| **JDK 9 (2017)** | JEP 254 交付 | Compact Strings 优化正式发布 |
| **持续** | Zip/Jar 处理 | ZipFileSystem 的核心开发和维护 |
| **持续** | 正则表达式与 Unicode | 推动 java.util.regex 符合 Unicode 技术标准 |

---

## 4. 主要 JEP 贡献

### JEP 254: Compact Strings

| 属性 | 值 |
|------|-----|
| **角色** | Owner |
| **JBS** | [JDK-8054307](https://bugs.openjdk.org/browse/JDK-8054307) |
| **状态** | Delivered |
| **发布版本** | JDK 9 |

**问题**: String 类使用 `char[]` 存储字符，每个字符占用 2 字节 (UTF-16)。然而数据表明 String 是堆内存的主要组成部分，且大多数 String 对象仅包含 Latin-1 字符 (仅需 1 字节)。

**解决方案**: 将 String 的内部表示从 UTF-16 `char[]` 改为 `byte[]` 加编码标志位。对于仅包含 Latin-1 字符的字符串，每个字符仅占用 1 字节 (ISO-8859-1/Latin-1 编码)；包含非 Latin-1 字符时仍使用 UTF-16 (2 字节)。

**影响**:
- String 对象内存占用减少高达 **50%** (对 Latin-1 字符串)
- `StringBuilder` 和 `StringBuffer` 同步更新
- 完全保持 API 兼容性和语义不变
- 广泛改善了几乎所有 Java 应用的内存效率

---

## 5. 核心技术贡献

### 1. Charset 子系统

Xueming 是 JDK 字符集编解码子系统的核心维护者：

- **JDK-6653797: 重新实现 charsets.jar**: 将大部分字符集实现改为在 JDK 构建时从文本映射表自动生成，charsets.jar 大小减少约 50%，大幅降低维护成本，同时提升 NIO 编解码性能
- **sun.nio.cs 包**: 标准字符集的底层实现维护
- **字符集注册与发现**: `java.nio.charset.Charset` 的 provider 机制

### 2. Zip/Jar 文件处理

- **ZipFileSystem**: `jdk.nio.zipfs.ZipFileSystem` 的核心作者，实现基于 NIO FileSystem API 的 Zip 文件系统
- **JDK-8142508**: 将 `java.util.zip.ZipFile` 的原生 C 实现改为纯 Java 实现，消除昂贵的 JNI 调用开销和 mmap 崩溃风险
- **Zip/Jar 核心类**: `ZipFile`、`ZipInputStream`、`JarFile` 等核心类的维护

### 3. 正则表达式与 Unicode

- **Unicode 合规性**: 推动 `java.util.regex` 符合 Unicode Technical Standard #18 (Unicode Regular Expressions) Level 1
- **Unicode Case-Folding**: 实现 Unicode 大小写折叠支持 (JDK-8365675)，为大小写无关匹配提供语言中立的折叠操作
- **RL1.5 合规**: 确保正则表达式引擎对字面量和字符类应用简单大小写折叠

### 4. String 内部实现

- **Compact Strings (JEP 254)**: String 内部表示从 `char[]` 到 `byte[]` 的核心重构
- **编码检测**: 自动检测字符串是否可以使用 Latin-1 紧凑编码
- **性能兼容**: 确保紧凑编码不引入性能回归

---

## 6. 技术专长

### 字符串与编码

- **String 内部架构**: Java String 的内存布局和编码策略
- **字符集编解码**: `java.nio.charset` 的编码器/解码器体系
- **Unicode 标准**: Unicode 字符属性、大小写映射、规范化

### 文件与归档

- **Zip/Jar 格式**: ZIP 文件格式的解析和生成
- **NIO FileSystem**: FileSystem Provider SPI 实现
- **压缩算法**: zlib 集成和性能优化

### 正则表达式

- **java.util.regex**: 正则表达式引擎的实现和优化
- **Unicode 正则**: Unicode 属性匹配和大小写折叠

---

## 7. 协作网络

| 协作者 | 合作领域 |
|--------|----------|
| [Martin Buchholz](martin-buchholz.md) | Core Libraries, 集合框架 |
| [Stuart Marks](stuart-marks.md) | Core Libraries API |
| [Roger Riggs](roger-riggs.md) | Core Libraries |
| [Aleksey Shipilev](aleksey-shipilev.md) | Compact Strings 性能分析 |
| [Claes Redestad](claes-redestad.md) | String 性能优化 |
| Naoto Sato | i18n, Unicode, Charset |

---

## 8. 相关链接

### 官方资料
- [OpenJDK Census - sherman](https://openjdk.org/census#sherman)
- [LinkedIn - Xueming Shen](https://www.linkedin.com/in/xueming-shen-8091388/)

### JEP 文档
- [JEP 254: Compact Strings](https://openjdk.org/jeps/254) - JDK 9

### JBS Issues
- [JDK-8054307: JEP 254: Compact Strings](https://bugs.openjdk.org/browse/JDK-8054307)
- [JDK-6653797: Reimplement JDK charset repository charsets.jar](https://bugs.openjdk.org/browse/JDK-6653797)
- [JDK-8142508: Bring ZipFile native implementation to Java](https://bugs.openjdk.org/browse/JDK-8142508)

### 技术参考
- [Strings in Java 9 (Oracle Blog)](https://blogs.oracle.com/java/post/strings-in-java-9)
- [Q&A: Compact Strings Optimization in OpenJDK 9 (InfoQ)](https://www.infoq.com/news/2016/02/compact-strings-Java-JDK9/)

---

**Sources**:
- [LinkedIn - Xueming Shen](https://www.linkedin.com/in/xueming-shen-8091388/)
- [OpenJDK Census](https://openjdk.org/census)
- [JEP 254: Compact Strings](https://openjdk.org/jeps/254)
- [JDK-8054307](https://bugs.openjdk.org/browse/JDK-8054307)
- [JDK-6653797](https://bugs.openjdk.org/browse/JDK-6653797)
- [Strings in Java 9](https://blogs.oracle.com/java/post/strings-in-java-9)
