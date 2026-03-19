# 模块/组件源码分析

> 本目录包含 JDK 核心模块和组件的源码分析文档

---

## 概述

JDK 26 包含约 70 个模块，本目录分析最重要的核心模块。

---

## 模块索引

### 核心模块

| 模块 | 描述 | 分析文档 |
|------|------|----------|
| java.base | Java 核心 API | [详细分析](java.base.md) |
| java.logging | 日志 API (JUL) | [详细分析](java.logging.md) |
| java.management | JMX 管理 | [详细分析](java.management.md) |
| java.sql | JDBC 数据库连接 | [详细分析](java.sql.md) |
| java.xml | XML 处理 (JAXP) | [详细分析](java.xml.md) |

### 并发模块

| 模块 | 描述 | 分析文档 |
|------|------|----------|
| java.util.concurrent | 并发工具 (JUC) | [详细分析](concurrent.md) |

### 网络模块

| 模块 | 描述 | 分析文档 |
|------|------|----------|
| java.net.http | HTTP Client (HTTP/3) | [详细分析](java.net.http.md) |

### 安全模块

| 模块 | 描述 | 分析文档 |
|------|------|----------|
| java.crypto / java.security | 加密与安全 | [详细分析](java.crypto.md) |

### JVM 组件

| 组件 | 描述 | 分析文档 |
|------|------|----------|
| hotspot | HotSpot VM 架构 | [详细分析](hotspot.md) |
| hotspot-gc | 垃圾回收器 | [详细分析](hotspot-gc.md) |
| hotspot-c2 | C2 JIT 编译器 | [详细分析](hotspot-c2.md) |

### 编译工具

| 模块 | 描述 | 分析文档 |
|------|------|----------|
| jdk.compiler | javac 编译器 API | [详细分析](jdk.compiler.md) |

---

## 模块依赖图

```
                    ┌─────────────┐
                    │  java.se    │
                    └──────┬──────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐
    │java.sql.rowset│ │java.naming │ │java.desktop │
    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
           │               │               │
           └───────────────┼───────────────┘
                           │
                    ┌──────┴──────┐
                    │  java.base  │
                    └─────────────┘
```

---

## 源码结构

```
jdk/
├── src/
│   ├── java.base/              # 核心模块
│   │   ├── share/
│   │   │   ├── classes/        # Java 类
│   │   │   │   ├── java/
│   │   │   │   │   ├── lang/   # java.lang
│   │   │   │   │   ├── util/   # java.util
│   │   │   │   │   ├── io/     # java.io
│   │   │   │   │   └── net/    # java.net
│   │   │   │   └── jdk/
│   │   │   │       └── internal/  # 内部 API
│   │   │   ├── native/         # 本地代码
│   │   │   └── conf/           # 配置文件
│   │   └── <platform>/         # 平台特定代码
│   │
│   ├── java.net.http/          # HTTP Client 模块
│   │   └── share/classes/
│   │       └── java.net.http/
│   │
│   └── hotspot/                # HotSpot VM
│       └── share/
│           ├── classfile/      # 类文件处理
│           ├── code/           # 代码生成
│           ├── compiler/       # 编译器接口
│           ├── gc/             # 垃圾回收
│           ├── memory/         # 内存管理
│           ├── oops/           # 对象模型
│           ├── runtime/        # 运行时
│           └── services/       # JVM TI
│
└── test/                       # 测试代码
    ├── jdk/
    │   ├── java/
    │   │   ├── lang/           # java.lang 测试
    │   │   └── util/           # java.util 测试
    │   └── sun/
    └── hotspot/                # HotSpot 测试
```

---

## 分析文档模板

每个模块分析文档包含：

1. **模块概述**: 功能描述、依赖关系
2. **包结构**: 主要包和类
3. **核心类分析**: 关键类的源码解读
4. **JDK 26 变更**: 该模块在 JDK 26 中的变更
5. **性能特性**: 性能相关的设计和优化
6. **使用示例**: API 使用示例

---

## 相关链接

- [JDK 26 模块文档](https://openjdk.org/projects/jdk/26/spec/)
- [API 文档](https://download.java.net/java/early_access/jdk26/docs/api/)
- [源码浏览](https://github.com/openjdk/jdk)