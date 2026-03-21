# Mandy Chung

> **Organization**: Oracle (Java Platform Group)
> **Role**: Core Libraries Engineer, Module System Runtime Expert
> **GitHub**: [@mlchung](https://github.com/mlchung)
> **OpenJDK**: [@mchung](https://openjdk.org/census#mchung)

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [职业时间线](#3-职业时间线)
4. [核心贡献](#4-核心贡献)
5. [主要 JEP 贡献](#5-主要-jep-贡献)
6. [技术专长](#6-技术专长)
7. [OpenJDK 角色与社区活动](#7-openjdk-角色与社区活动)
8. [合作关系](#8-合作关系)
9. [相关链接](#9-相关链接)

---


## 1. 概述

Mandy Chung 是 Oracle Java Platform Group 的**核心库资深工程师**，在 Java 平台上拥有超过 20 年的开发经验，从 Sun Microsystems 时代即参与 JDK 开发。她是 **Java 模块系统运行时支持**的核心实现者之一，也是 **jlink（Java 链接器）** 和 **jdeps（依赖分析工具）** 的主要开发者。她的工作涵盖 ServiceLoader 模块化改造、ClassLoader 层级重构、以及模块化运行时镜像等关键基础设施，是 Project Jigsaw 从设计到落地的核心工程力量。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Mandy Chung |
| **当前组织** | Oracle (Java Platform Group) |
| **职位** | Principal Member of Technical Staff |
| **前雇主** | Sun Microsystems |
| **GitHub** | [@mlchung](https://github.com/mlchung) |
| **OpenJDK** | [@mchung](https://openjdk.org/census#mchung) |
| **Email** | mandy.chung@oracle.com |
| **角色** | JDK Reviewer, Project Jigsaw 核心团队成员 |
| **专长** | Core Libraries, Module System Runtime, jlink, jdeps, ServiceLoader, ClassLoader |
| **活跃时间** | ~2000 - 至今 (20+ 年) |

---

## 3. 职业时间线

| 年份 | 事件 | 详情 |
|------|------|------|
| **~2000** | 加入 Sun Microsystems | Java 平台核心库开发 |
| **2000-2010** | Sun Microsystems 时期 | 参与 JDK 5/6/7 核心库开发，ServiceLoader、ClassLoader 维护 |
| **2010** | Oracle 收购 Sun | 继续在 Java Platform Group 从事核心库工作 |
| **2014-2017** | Project Jigsaw 核心团队 | 模块系统运行时支持实现，jdeps 工具开发 |
| **2017** | JDK 9 发布 | jlink、jdeps、模块化运行时镜像等核心成果交付 |
| **2017-至今** | 持续维护核心库 | 模块系统持续改进，jlink 增强，核心库维护 |

---

## 4. 核心贡献

### 1. jlink - Java 链接器 (JEP 282)

Mandy Chung 是 jlink 工具的核心开发者之一，jlink 是 JDK 9 引入的用于创建自定义运行时镜像的链接器：

- **自定义运行时**: 允许开发者将应用所需的模块组装成精简的运行时镜像
- **插件体系**: 设计并实现了 jlink 插件管道 (plugin pipeline)，支持压缩、优化等转换
- **模块化基础**: 与 JEP 220 (Modular Run-Time Images) 紧密配合

```bash
# jlink 创建自定义运行时示例
jlink --module-path $JAVA_HOME/jmods \
      --add-modules java.base,java.logging \
      --output custom-runtime
```

### 2. jdeps - 依赖分析工具

Mandy Chung 是 jdeps 工具的主要开发者，该工具用于分析 Java 类文件的依赖关系：

- **模块迁移辅助**: 帮助开发者将现有应用迁移到模块系统
- **内部 API 检测**: 识别对 JDK 内部 API 的依赖 (配合 JEP 260)
- **依赖图生成**: 生成包级和模块级依赖关系图
- **jlink 集成**: 分析模块依赖，生成适合 jlink 使用的模块列表

```bash
# jdeps 分析依赖示例
jdeps --module-path libs -s application.jar
jdeps --jdk-internals application.jar
```

### 3. 模块系统运行时支持 (Project Jigsaw)

作为 Project Jigsaw 核心团队成员，Mandy Chung 负责模块系统的运行时层面实现：

- **模块化运行时镜像 (JEP 220)**: 参与 JDK/JRE 运行时镜像的模块化重构
- **模块层 (Module Layers)**: ModuleLayer API 的实现，支持运行时模块配置
- **ServiceLoader 改造**: 将 ServiceLoader 适配到模块系统，支持 `provides...with` 声明
- **ClassLoader 重构**: 重构 JDK 内部的 ClassLoader 层级结构以适配模块系统

### 4. ServiceLoader 模块化

Mandy Chung 负责将传统的 ServiceLoader 机制改造为模块感知的服务发现框架：

- **module-info.java 集成**: 通过 `provides` 和 `uses` 指令声明服务
- **延迟加载**: 优化服务提供者的发现和加载性能
- **安全增强**: 模块系统提供的服务隔离和访问控制

```java
// module-info.java 中的服务声明
module my.module {
    uses java.sql.Driver;
    provides java.sql.Driver with my.module.MyDriver;
}
```

### 5. ClassLoader 架构改进

- **Application ClassLoader**: 重构为支持模块的类加载器
- **Platform ClassLoader**: 替代原有的 Extension ClassLoader
- **类加载委托模型**: 适配模块系统的类加载路径

---

## 5. 主要 JEP 贡献

| JEP | 标题 | JDK 版本 | 角色 |
|-----|------|----------|------|
| JEP 282 | jlink: The Java Linker | JDK 9 | 核心开发者 |
| JEP 220 | Modular Run-Time Images | JDK 9 | 贡献者 |
| JEP 260 | Encapsulate Most Internal APIs | JDK 9 | 贡献者 (jdeps 工具支持) |
| JEP 261 | Module System | JDK 9 | 核心团队成员 |
| JEP 275 | Modular Java Application Packaging | JDK 9 | 贡献者 |
| JEP 201 | Modular Source Code | JDK 9 | 贡献者 (源码重组) |

---

## 6. 技术专长

### 核心库

- **java.lang.module**: 模块系统运行时 API
- **java.util.ServiceLoader**: 服务提供者框架
- **java.lang.ClassLoader**: 类加载器体系
- **java.lang.instrument**: 检测和监控 API

### 工具

- **jlink**: Java 链接器，创建自定义运行时
- **jdeps**: Java 依赖分析工具
- **jmod**: JMOD 文件管理工具

### 模块系统

- **模块描述符**: module-info.java 编译和运行时处理
- **模块层**: ModuleLayer 和 Configuration API
- **模块路径**: 模块发现和解析机制
- **服务绑定**: 模块化服务提供者架构

---

## 7. OpenJDK 角色与社区活动

### OpenJDK 角色

- **JDK Reviewer**: JDK 项目评审者，参与核心库和模块系统变更评审
- **Project Jigsaw 核心团队**: 与 Alan Bateman、Mark Reinhold、Alex Buckley、Jonathan Gibbons 等共同构建模块系统

### 邮件列表活跃

- **jigsaw-dev**: Project Jigsaw 模块系统开发讨论
- **core-libs-dev**: 核心库开发讨论
- **build-dev**: 构建系统相关 (jlink 插件管道)

### 代码评审

Mandy Chung 在核心库和模块系统领域积极参与代码评审，确保 API 一致性和向后兼容性。

---

## 8. 合作关系

与以下 Java 平台核心工程师密切合作：

| 合作者 | 领域 |
|--------|------|
| **Mark Reinhold** | Project Jigsaw 总架构师 |
| **Alan Bateman** | 核心库、模块系统 |
| **Alex Buckley** | 模块系统语言规范 |
| **Jonathan Gibbons** | javac 模块系统编译器支持 |
| **Karen Kinnear** | HotSpot 模块系统 VM 支持 |
| **Stuart Marks** | 核心库 API 设计 |

---

## 9. 相关链接

### 官方资料
- [GitHub - mlchung](https://github.com/mlchung)
- [OpenJDK Census - mchung](https://openjdk.org/census#mchung)
- [OpenJDK Wiki - Mandy Chung](https://wiki.openjdk.org/display/~mchung)

### JEP 文档
- [JEP 282: jlink: The Java Linker](https://openjdk.org/jeps/282)
- [JEP 220: Modular Run-Time Images](https://openjdk.org/jeps/220)
- [JEP 260: Encapsulate Most Internal APIs](https://openjdk.org/jeps/260)
- [JEP 261: Module System](https://openjdk.org/jeps/261)
- [JEP 201: Modular Source Code](https://openjdk.org/jeps/201)

### 工具文档
- [jlink - Oracle Docs](https://docs.oracle.com/en/java/javase/21/docs/specs/man/jlink.html)
- [jdeps - Oracle Docs](https://docs.oracle.com/en/java/javase/21/docs/specs/man/jdeps.html)

---

**Sources**:
- [GitHub - mlchung](https://github.com/mlchung)
- [OpenJDK Wiki - mchung](https://wiki.openjdk.org/display/~mchung)
- [JEP 282: jlink](https://openjdk.org/jeps/282)
- [JEP 220: Modular Run-Time Images](https://openjdk.org/jeps/220)
- [JEP 261: Module System](https://openjdk.org/jeps/261)

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-22
