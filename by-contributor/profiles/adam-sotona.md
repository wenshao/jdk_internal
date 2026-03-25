# Adam Sotona

> **Class File API 实现负责人** | Principal Member of Technical Staff, Oracle

---
## 目录

1. [基本信息](#1-基本信息)
2. [职业历程](#2-职业历程)
3. [技术影响力](#3-技术影响力)
4. [贡献时间线](#4-贡献时间线)
5. [技术特长](#5-技术特长)
6. [代表性工作](#6-代表性工作)
7. [其他重要 PR](#7-其他重要-pr)
8. [技术深度](#8-技术深度)
9. [协作网络](#9-协作网络)
10. [历史贡献](#10-历史贡献)
11. [外部资源](#11-外部资源)
12. [相关链接](#12-相关链接)
13. [相关文档](#13-相关文档)
14. [数据来源](#14-数据来源)

---


## 1. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Adam Sotona |
| **组织** | Oracle |
| **位置** | Prague, Czech Republic |
| **GitHub** | [@asotona](https://github.com/asotona) (40 followers, 15 repos) |
| **OpenJDK** | [@asotona](https://openjdk.org/census#asotona) |
| **LinkedIn** | [sotona](https://cz.linkedin.com/in/sotona) |
| **角色** | JDK Committer, Amber Committer |
| **主要领域** | Class File API, 字节码处理, javac, Project Babylon, Java ONNX |
| **经验** | 25+ years Java engineer |
| **活跃时间** | 2020 - 至今 |
| **Integrated PRs** | 30+ |
| **Git Commits (master)** | 59 (ClassFile API 相关) |

> **统计方法**:
> - GitHub PR search: `repo:openjdk/jdk author:asotona type:pr label:integrated`
> - Local git log (master only): `src/java.base/share/classes/java/lang/classfile/` + `jdk/internal/classfile/`

## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 226 |
| **活跃仓库数** | 3 |

> **统计时间**: 2026-03-20

---

## 2. 职业历程

| 时间 | 事件 | 详情 |
|------|------|------|
| **2000-2003** | Sun Microsystems | NetBeans 平台测试工具开发和质量工程 |
| **~2003-2011** | BlackBerry 等 | Senior Software Developer |
| **2011-2019** | Freelancer | Big Semantic Data Architect and Engineer (RDF, SPARQL, Linked Data) |
| **2020-01** | 加入 Oracle | Principal Member of Technical Staff (JDK LangTools 团队) |
| **2023-2024** | Class File API 实现 | 主导 JDK-8294982 实现 |
| **2024-2025** | Class File API 正式版 | JEP 484 完成 |

---

## 3. 技术影响力

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 30+ |
| **主要影响模块** | java.lang.classfile, jdk.internal.classfile.impl, javac |
| **关键 Issue** | JDK-8294982 (ClassFile API 实现) |

### 影响的主要目录

| 目录 | 说明 |
|------|------|
| `src/java.base/share/classes/java/lang/classfile/` | Class File API 公共接口 |
| `src/java.base/share/classes/jdk/internal/classfile/impl/` | 内部实现 |
| `src/jdk.javadoc/share/classes/jdk/javadoc/internal/doclets/formats/html/` | javadoc 集成 |
| `test/jdk/java/lang/classfile/` | 测试套件 |

---

## 4. 贡献时间线

```
2020: ░░░░░░░░░░░░░░░░░░░░  开始 Oracle 任职
2021: ░░░░░░░░░░░░░░░░░░░░  早期 PR
2022: ░░░░░░░░░░░░░░░░░░░░  ClassFile API 开发
2023: ████████████████████████  JDK-8294982 v6-v56 (峰值)
2024: ████████████████████░░░  20+ PRs, 预览到正式版
2025: ████████████████████░░░  持续优化, ASM 移除
2026: ██████░░░░░░░░░░░░░░░  维护和修复
```

---

## 5. 技术特长

`ClassFile API` `Bytecode` `javac` `ASM` `RDF` `SPARQL` `Semantic Web` `Linked Data`

---

## 6. 代表性工作

### 1. JDK-8294982: Implementation of Classfile API (主实现)

**Issue**: [JDK-8294982](https://bugs.openjdk.org/browse/JDK-8294982)
**状态**: 已集成 (JDK 22-24)
**版本迭代**: v6 → v56 (50+ 个版本)

这是 Class File API 的根 PR，包含完整的实现、测试和基准测试。API 从 `jdk.internal.classfile` 演进为 `java.lang.classfile` 标准公共 API。

**关键成果**:
- 完整的类文件解析 API
- 类文件生成和转换 API
- 流式函数式 API 设计
- 不可变模型架构
- 与 javac 的集成

> "This is the root PR for the Classfile API implementation, including comprehensive tests and benchmarks."
> — Adam Sotona, build-dev@openjdk.org

### 2. JDK-8308753: Class-File API transition to Preview

**Issue**: [JDK-8308753](https://bugs.openjdk.org/browse/JDK-8308753)
**状态**: 已集成 (JDK 22)
**版本**: v2

将 Class File API 从内部包迁移到公共预览 API。

**关键变更**:
- 包名: `jdk.internal.classfile` → `java.lang.classfile`
- 添加 `@PreviewFeature` 注解
- 所有 JDK 模块启用预览特性

### 3. JDK-8334714: Implement JEP 484: Class-File API (Final)

**Issue**: [JDK-8334714](https://bugs.openjdk.org/browse/JDK-8334714)
**状态**: 已集成 (JDK 24)
**版本**: v3

Class File API 正式版实现，移除预览标记，生产就绪。

### 4. JDK-8346986: Remove ASM from java.base

**Issue**: [JDK-8346986](https://bugs.openjdk.org/browse/JDK-8346986)
**状态**: 已集成 (JDK 26)

从 JDK 中完全移除 ASM 库，统一使用 Class File API 进行字节码处理。

**影响**:
- 移除 `com.sun.tools.classfile` 旧 API
- 移除 `jdk.internal.objectweb.asm` 包
- 统一为 `java.lang.classfile` API

### 5. JDK-8346983: Remove ASM-based benchmarks from Class-File API benchmarks

**Issue**: [JDK-8346983](https://bugs.openjdk.org/browse/JDK-8346983)
**状态**: 已集成 (JDK 26)

清理基于 ASM 的基准测试，统一使用 Class File API 进行性能对比。

---

## 7. 其他重要 PR

| PR # | Issue | 标题 | 集成时间 |
|------|-------|------|----------|
 | JDK-8366926 | Unexpected exception in JShell local environment | 2025-09 |
 | JDK-8357955 | Signature.ArrayTypeSig.of IAE validation | 2025-05 |
 | JDK-8350548 | NPE in getDeclarationAttributes | 2025-05 |
 | JDK-8348283 | PackageSnippets in java.base.jmod | 2025-01 |
 | JDK-8345773 | Class-File API debug printing capability | 2024-12 |
 | JDK-8344841 | ClassPrinter null value printing | 2024-11 |
 | JDK-8338981 | Attribute attributeName() returns Utf8Entry | 2024-11 |
 | JDK-8338661 | Remove obsolete AbstractNamedEntry::equals | 2024-08 |
 | JDK-8336833 | Endless loop in Javap ClassWriter | 2024-07 |
 | JDK-8333812 | ClassFile.verify() exception handling | 2024-07 |

---

## 8. 技术深度

### Class File API 专家

Adam Sotona 是 Class File API 的主要实现者，负责将这个 API 从内部工具发展为 JDK 标准公共 API。

**关键贡献**:
- 设计并实现了流式函数式 API (`ClassFile.of().parse()`)
- 创建不可变模型架构 (`ClassModel`, `MethodModel`, `FieldModel`)
- 实现类型安全的字节码生成 (`ClassBuilder`, `CodeBuilder`)
- 与 javac 团队紧密合作，实现编译器集成
- 从头替换 ASM 在 JDK 内部的使用

**代码风格**:
- 注重不可变性和线程安全
- 流式 API 设计，链式调用友好
- 完善的文档和 JavaDoc
- 全面的测试覆盖

---

## 9. 协作网络

### 常见审查者

| 审查者 | 领域 | 组织 |
|--------|------|------|
| [Chen Liang](chen-liang.md) | ClassFile API, javac | Oracle |
| [Jonathan Gibbons](jonathan-gibbons.md) | javac, 语言规范 | Oracle |
| [Claes Redestad](claes-redestad.md) | 核心库, 性能 | Oracle |
| [Brian Goetz](brian-goetz.md) | 语言架构, JEP 指导 | Oracle |

### 常见协作者

| 协作者 | 合作领域 | 组织 |
|--------|----------|------|
| Alan Bateman | javac, 语言集成 | Oracle |
| Lance Andersen | javac, 工具链 | Oracle |

---

## 10. 历史贡献

### JDK 版本贡献

| JDK 版本 | 主要贡献 |
|----------|----------|
| **JDK 21** | Class File API 内部实现 (`jdk.internal.classfile`) |
| **JDK 22** | Class File API 第一次预览 (JEP 459) |
| **JDK 23** | Class File API 第二次预览 (JEP 466) |
| **JDK 24** | Class File API 正式版 (JEP 484) |
| **JDK 26** | 移除 ASM，统一使用 ClassFile API |
| **进行中** | Project Babylon, Java ONNX 脚本库开发 |

### Project Babylon 贡献

Adam Sotona 目前还在积极参与 Project Babylon 开发，主导 Java ONNX 脚本库：
- 实现 ONNX 模型与 Java 类型系统的无缝集成
- 利用 code models 在 Java 与 ONNX 计算图之间架起桥梁
- 在 JavaOne Program Committee 中担任成员

### 长期影响

- **字节码处理标准化**: Class File API 成为处理 class 文件的标准方式
- **ASM 替代**: JDK 内部不再依赖外部 ASM 库
- **类型安全**: 编译时验证的字节码操作
- **开发者体验**: 简化的 API 设计，更易使用

---

## 11. 外部资源

| 类型 | 链接 |
|------|------|
| **GitHub** | [@asotona](https://github.com/asotona) |
| **OpenJDK Census** | [@asotona](https://openjdk.org/census#asotona) |
| **LinkedIn** | [sotona](https://cz.linkedin.com/in/sotona) |
| **CFV: Amber Committer** | [Nomination](https://mail.openjdk.org/archives/list/amber-dev@openjdk.org/thread/PV2DO5FLBYMLLLWBCPDF5EJYNNXS7X67/) |
| **Location** | Prague, Czech Republic |
| **Blog** | LinkedIn technical articles |

---

## 12. 相关链接

- [JDK-8294982: Classfile API Implementation](https://bugs.openjdk.org/browse/JDK-8294982)
- [JEP 484: Class-File API](https://openjdk.org/jeps/484)
- [JEP 466: Class-File API (Second Preview)](https://openjdk.org/jeps/466)
- [JEP 459: Class-File API (First Preview)](https://openjdk.org/jeps/459)
- [GitHub: openjdk/jdk (author:asotona)](https://github.com/openjdk/jdk/commits?author=asotona)
- [邮件列表: RFR 8294982 v31](https://mail.openjdk.org/archives/list/build-dev@openjdk.org/message/2UOJLVRSKPIPXYE44XT36SSGM2ZB74PX/)
- [邮件列表: RFR 8294982 v20](https://mail.openjdk.org/archives/list/build-dev@openjdk.org/message/ZQNNVJVXPE253ETYDCP4MRJM5HMXDFEO/)
- [JavaDoc: ClassFile API](https://cr.openjdk.org/~asotona/8312491/classfile-api/)

---

## 13. 相关文档

- [Class File API 主题概览](../../by-topic/language/classfile/)
- [Chen Liang (协作者)](chen-liang.md)
- [Claes Redestad (性能优化指导)](claes-redestad.md)
- [JDK-8336856: 字符串拼接优化](../../by-pr/8336/8336856.md)
- [JDK-8346986: 移除 ASM](../../by-pr/8346/8346986.md)

---

> **文档版本**: 1.1
> **最后更新**: 2026-03-22
> **审核状态**: ✅ 已完成

---

## 14. 数据来源

- GitHub PR search: `repo:openjdk/jdk author:asotona label:integrated`
- OpenJDK Bug System: JDK-8294982, JDK-8308753, JDK-8334714, JDK-8346986
- OpenJDK Mailing Lists: build-dev@openjdk.org, compiler-dev@openjdk.org
- LinkedIn: https://cz.linkedin.com/in/sotona
- GitHub Profile: https://github.com/asotona
