# Joe Wang

> **Organization**: Oracle (Java Platform Group)
> **Role**: JDK Reviewer, XML (JAXP) Lead Engineer
> **GitHub**: [JoeWang-Java](https://github.com/JoeWang-Java)
> **OpenJDK**: [@joehw](https://openjdk.org/census#joehw)

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [核心技术贡献](#3-核心技术贡献)
4. [技术专长](#4-技术专长)
5. [职业经历](#5-职业经历)
6. [相关链接](#6-相关链接)

---


## 1. 概述

Joe Wang 是 Oracle Java 平台工程师，是 JDK **XML 处理（JAXP）** 模块的核心维护者和主要贡献者。他在 openjdk/jdk 仓库有 **371 次贡献**，几乎全部集中在 `java.xml` 模块。他负责维护 JAXP 的所有子系统：**StAX、SAX、DOM、XPath、XSLT、XML Schema 验证、Catalog API** 以及 XML 安全属性管理。他还负责上游组件（Xerces、Xalan、BCEL）的同步更新。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Joe Wang |
| **当前组织** | Oracle (Java Platform Group) |
| **OpenJDK** | [@joehw](https://openjdk.org/census#joehw) |
| **GitHub** | [JoeWang-Java](https://github.com/JoeWang-Java) |
| **角色** | JDK Reviewer, java.xml Module Lead |
| **专长** | JAXP, StAX, SAX, DOM, XPath, XSLT, XML Schema, Catalog API |
| **openjdk/jdk 贡献数** | 371 |
| **GitHub 集成 PR** | 62+ (通过 GitHub PR 工作流) |

---

## 3. 核心技术贡献

### 1. JAXP 配置与安全属性

Joe Wang 主导了 JAXP 安全模型的现代化工作：
- **JAXP 配置文件重定义** (8303530): 重新设计 JAXP 配置文件机制，使 XML 处理限制和安全属性可以通过配置文件统一管理
- **严格 JAXP 配置模板** (8330542): 提供严格安全配置文件模板
- **JAXP 限制调整** (8343004): 调整 XML 处理限制的默认值
- **XMLSecurityPropertyManager 重构** (8353234): 重构 XML 安全属性管理器
- **标准化 XML 组件配置** (8353232): 统一和标准化 XML 组件配置方式
- **DTD 支持属性** (8306632): 添加 JDK 属性用于指定 DTD 支持策略
- **扩展函数控制** (8343001, 8354084): 调整 XSLT 和 XPath 扩展函数属性，精简 XPath API 的扩展函数控制

### 2. JDK 内置 Catalog

Joe Wang 设计并实现了 JDK 内置 XML Catalog 系统：
- **内置 Catalog** (8306055): 为 JDK XML 模块添加内置 Catalog，减少外部 DTD/XSD 访问
- **W3C DTD/XSD** (8344800): 将 W3C DTD 和 XSD 添加到内置 Catalog
- **公共标识符** (8351969): 向内置 Catalog 添加公共标识符
- **Catalog API 增强** (8316996): 添加工厂方法
- **Catalog 错误修复** (8320918, 8290740, 8253569): 修复 Catalog 实现中的多个问题

### 3. XPath

Joe Wang 维护并改进 JDK 的 XPath 实现：
- **XPathFactory 属性方法** (8276141): 添加 set/getProperty 方法
- **操作符计数准确性** (8285081): 改进 XPath 操作符计数
- **异常处理** (8284400): 改进 XPath 异常处理
- **Bug 修复** (8284548, 8284920, 8266559): 修复 token 解析、结果类型映射等问题

### 4. StAX 与 SAX

- **XMLStreamReader 修复** (8327378): XMLStreamReader 错误地抛出 EOFException 而非 XMLStreamException
- **CDATA 处理** (8349516): StAXStream2SAX.handleCharacters() 在空 CDATA 上失败
- **XML 名称限制** (8294858): XMLStreamReader 不尊重命名长度限制
- **SAXParser 修复** (8316383): AbstractSAXParser 空指针修复

### 5. XSLT

- **UTF-8 边界处理** (8349699): XSL 转换在 1024 字节边界上的 UTF-8 字符处理失败
- **translet-name 处理** (8344925): 当 package-name 同时设置时 translet-name 被忽略
- **空类名** (8276657): XSLT 编译器尝试定义空名称的类
- **isStandalone 属性** (8260858, 8261209): 为 XSLTC 序列化器添加 isStandalone 属性

### 6. 上游组件更新

Joe Wang 负责同步 JDK 使用的第三方 XML 组件：
- **Xerces 更新** (8282280): 更新到 Xerces 2.12.2
- **Xalan 更新** (8305814): 更新到 Xalan Java 2.7.3
- **BCEL 更新** (8336695, 8301269, 8255035): 多次更新 Commons BCEL（6.5.0 → 6.7.0 → 6.10.0）

---

## 4. 技术专长

### XML 处理 (java.xml)

- **JAXP**: Java API for XML Processing 全栈
- **StAX**: Streaming API for XML（XMLStreamReader/Writer）
- **SAX**: Simple API for XML（事件驱动解析）
- **DOM**: Document Object Model（树形解析）
- **XPath**: XML 路径语言查询
- **XSLT**: XML 样式转换
- **XML Schema**: 验证框架
- **Catalog API**: XML 资源解析 Catalog

### 安全与配置

- **XML 安全属性**: 处理限制、扩展函数控制、DTD 策略
- **JAXP 配置文件**: 统一配置管理

---

## 5. 职业经历

### Oracle (现职)

在 Oracle Java Platform Group 担任 java.xml 模块的核心工程师：
- **java.xml 模块维护**: JAXP 全栈的开发、维护和安全加固
- **安全增强**: 持续改进 XML 处理的安全模型和默认限制
- **内置 Catalog**: 设计并实现 JDK 内置 Catalog 系统
- **上游同步**: 管理 Xerces、Xalan、BCEL 等上游组件的更新
- **长期贡献**: 自 openjdk/jdk 仓库创建以来持续贡献，从 2020 年至今通过 GitHub PR 提交了 62+ 个集成补丁

---

## 6. 相关链接

### 官方资料
- [OpenJDK Census - joehw](https://openjdk.org/census#joehw)
- [GitHub: JoeWang-Java](https://github.com/JoeWang-Java)

### 关键提交
- [8306055: Add a built-in Catalog to JDK XML module](https://github.com/openjdk/jdk/pull/16719)
- [8303530: Redefine JAXP Configuration File](https://github.com/openjdk/jdk/pull/12985)
- [8306632: Add a JDK Property for specifying DTD support](https://github.com/openjdk/jdk/pull/15075)
- [8353232: Standardizing and Unifying XML Component Configurations](https://github.com/openjdk/jdk/pull/25102)

### 模块资料
- [java.xml Module Summary](https://docs.oracle.com/en/java/javase/21/docs/api/java.xml/module-summary.html)
- [JAXP Tutorial](https://docs.oracle.com/javase/tutorial/jaxp/)

---

**Sources**:
- [GitHub: JoeWang-Java](https://github.com/JoeWang-Java)
- [OpenJDK Core Libraries Group](https://openjdk.org/groups/core-libs/)
