# GraalVM

> Oracle Labs 提供的高性能 JDK 发行版

[← 返回发行版](../distributions/)

---
## 目录

1. [概述](#1-概述)
2. [版本类型](#2-版本类型)
3. [核心特性](#3-核心特性)
4. [版本支持](#4-版本支持)
5. [安装](#5-安装)
6. [适用场景](#6-适用场景)
7. [相关链接](#7-相关链接)

---


## 1. 概述

GraalVM 是 Oracle Labs 开发的高性能 JDK，以 Native Image AOT 编译和多语言支持著称。

| 属性 | 值 |
|------|-----|
| **组织** | Oracle Labs |
| **官网** | https://www.graalvm.org/ |
| **下载** | https://www.graalvm.org/downloads/ |
| **许可证** | GFTC (自 2023 年中起统一为 Oracle GraalVM) |
| **商业支持** | ✅ |
| **核心特性** | Native Image, Truffle, Polyglot |

---

## 2. 版本类型

### Oracle GraalVM (2023 年中起)

自 2023 年中起，Oracle 将原 GraalVM CE 和 EE 合并为单一的 **Oracle GraalVM** 发行版，统一使用 GFTC 许可。

- ✅ **免费**: 生产环境免费使用 (GFTC 许可)
- ✅ **Native Image**: AOT 编译
- ✅ **Graal JIT**: 高性能 JIT 编译器 (原 EE 优化已包含)
- ✅ **Polyglot**: 多语言支持
- ✅ **商业支持**: 可通过 Oracle Java SE Subscription 获取

### 历史版本 (2023 年中之前)

> 以下 CE/EE 区分仅供历史参考，不再适用于当前版本。

- **GraalVM Community Edition (CE)**: 免费开源版本，仅社区支持
- **GraalVM Enterprise Edition (EE)**: 商业版本，包含额外性能优化和企业级工具

---

## 3. 核心特性

### Native Image

AOT (Ahead-Of-Time) 编译，将 Java 代码编译为本地可执行文件：

| 特性 | JVM | Native Image |
|------|-----|---------------|
| 启动时间 | ~100ms | ~5ms |
| 内存占用 | ~35MB | ~5MB |
| 编译时间 | - | ~30s-5min |
| 动态类加载 | ✅ | ❌ |

```bash
# 编译
native-image -jar myapp.jar

# 运行
./myapp
```

### Graal JIT

用 Java 编写的高性能 JIT 编译器：

- 更好的优化
- 更快的预热
- 更低的长期延迟

### Truffle & Polyglot

多语言运行时框架：

```java
// 多语言示例
import org.graalvm.polyglot.*;

Context context = Context.create();
Value result = context.eval("js", "10 + 20");
System.out.println(result.asInt());  // 30

// Python
context.eval("python", "print('Hello from Python')");

// Ruby
context.eval("ruby", "puts 'Hello from Ruby'");
```

---

## 4. 版本支持

### 支持周期

| 版本 | Oracle GraalVM 支持截止 |
|------|------------------------|
| GraalVM 21 (LTS) | 2031-10 |
| GraalVM 23 | 2025-09 |
| GraalVM 24 | 2026-03 |

---

## 5. 安装

### SDKMAN

```bash
# 安装 GraalVM
sdk install java 21-graal
sdk use java 21-graal

# 验证
java -version
# openjdk version "21.0.1" 2023-10-17 LTS
# OpenJDK Runtime Environment Oracle GraalVM 21.0.1+12.1 (build 21.0.1+12-LTS)
# OpenJDK 64-Bit Server VM Oracle GraalVM 21.0.1+12.1 (build 21.0.1+12-LTS, mixed mode)
```

### Docker

```bash
# 官方镜像
docker pull ghcr.io/graalvm/native-image-community:21
docker pull ghcr.io/graalvm/jdk:21

# Native Image
docker run -it --rm ghcr.io/graalvm/native-image-community:21 native-image --version
```

### 包管理器

```bash
# Homebrew (macOS)
brew install --cask graalvm/tap/graalvm-jdk21

# SDKMAN
sdk install java 21-graal
```

---

## 6. 适用场景

### 推荐使用

| 场景 | 理由 |
|------|------|
| 云原生 | Native Image 快速启动 |
| Serverless | Native Image 低内存 |
| 微服务 | Quarkus, Spring Native |
| 多语言 | Truffle Polyglot |

### 不推荐使用

| 场景 | 替代方案 |
|------|----------|
| 简单应用 | Eclipse Temurin |
| 动态类加载 | 普通 JDK |

---

## 7. 相关链接

### 官方资源

- [GraalVM 官网](https://www.graalvm.org/)
- [GraalVM 文档](https://www.graalvm.org/latest/docs/)
- [GraalVM GitHub](https://github.com/oracle/graal)

---

**最后更新**: 2026-03-20
