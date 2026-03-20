# GraalVM

> Oracle Labs 开发的高性能 JDK 发行版

[← 返回核心平台](../)

---

## 概述

GraalVM 是 Oracle Labs 开发的高性能 JDK 发行版，基于 OpenJDK，核心特性包括：

| 特性 | 说明 |
|------|------|
| **Graal JIT** | 用 Java 编写的高性能 JIT 编译器 |
| **Native Image** | AOT 编译，生成原生可执行文件 |
| **Truffle** | 多语言运行时框架 |
| **Polyglot** | 在 JVM 上运行多种语言 |

```
┌─────────────────────────────────────────────────────────────┐
│                       GraalVM 架构                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Polyglot Languages                      │   │
│  │  JavaScript │ Ruby │ Python │ R │ LLVM │ WebAssembly │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│                          ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Truffle Framework                       │   │
│  │        AST 解释器框架 + Self-Optimizing              │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│                          ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Graal Compiler                          │   │
│  │         JIT / AOT / Polyglot 优化                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│                          ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              JVMCI Interface                         │   │
│  │        JVM Compiler Interface (JEP 243)              │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│                          ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              HotSpot VM (OpenJDK)                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 版本历史

### GraalVM 版本演进

| 版本 | 发布时间 | JDK 基线 | 主要特性 |
|------|----------|----------|----------|
| **GraalVM 19** | 2019-05 | JDK 11 | 首个社区版本 |
| **GraalVM 20** | 2020-01 | JDK 11 | Native Image 改进 |
| **GraalVM 21** | 2021-01 | JDK 11 | Truffle 优化 |
| **GraalVM 22** | 2022-01 | JDK 17 | Native Image 性能提升 |
| **GraalVM 23** | 2023-06 | JDK 17/20 | 多版本支持 |
| **GraalVM 24** | 2024-03 | JDK 21 | JDK 21 基线 |
| **GraalVM 25** | 2025-03 | JDK 21/24 | 最新特性 |

---

## 核心特性

### 1. Graal JIT 编译器

用 Java 编写的高性能 JIT 编译器，可替代 HotSpot C2 编译器。

```bash
# 启用 Graal JIT (OpenJDK)
java -XX:+UnlockExperimentalVMOptions -XX:+UseJVMCICompiler MyApp

# GraalVM 默认使用 Graal JIT
java MyApp
```

**优势**:
- 代码更易维护（Java vs C++）
- 更好的内联和逃逸分析
- 支持 Truffle 语言优化

**劣势**:
- 启动时间略长
- 内存占用较高
- 部分场景性能不如 C2

---

### 2. Native Image (AOT 编译)

将 Java 应用编译为原生可执行文件。

```bash
# 安装 native-image 组件
gu install native-image

# 编译为原生可执行文件
native-image -jar myapp.jar

# 运行原生可执行文件
./myapp
```

**性能对比**:

| 指标 | JVM 模式 | Native Image | 提升 |
|------|----------|--------------|------|
| 启动时间 | 秒级 | 毫秒级 | **100x+** |
| 内存占用 | 100MB+ | 10MB+ | **10x** |
| 首次响应 | JIT 预热 | 即时 | **即时** |

**限制**:
- 动态类加载受限
- 反射需要配置
- JNI 需要特殊处理

---

### 3. Truffle Framework

多语言运行时框架，支持在 JVM 上运行多种语言。

**支持的语言**:

| 语言 | 状态 | 说明 |
|------|------|------|
| **JavaScript** | ✅ 生产 | GraalJS, Node.js 兼容 |
| **Python** | ✅ 生产 | GraalPython, 兼容 CPython |
| **Ruby** | ✅ 生产 | TruffleRuby, 兼容 MRI |
| **R** | ✅ 生产 | FastR, 兼容 GNU R |
| **LLVM** | ✅ 生产 | Sulong, 运行 C/C++/Rust |
| **WebAssembly** | ✅ 生产 | WASM 支持 |

**Polyglot 示例**:
```java
import org.graalvm.polyglot.*;

public class PolyglotExample {
    public static void main(String[] args) {
        try (Context context = Context.create()) {
            // JavaScript
            context.eval("js", "console.log('Hello from JS!');");

            // Python
            context.eval("python", "print('Hello from Python!')");

            // 跨语言调用
            Value array = context.eval("js", "[1, 2, 3]");
            System.out.println(array.getArraySize()); // 3
        }
    }
}
```

---

## 与 OpenJDK 的关系

| 特性 | OpenJDK | GraalVM |
|------|---------|---------|
| JIT 编译器 | C1 + C2 | C1 + Graal |
| AOT 编译 | CDS (有限) | Native Image |
| 多语言 | 无 | Truffle |
| 启动时间 | 秒级 | 毫秒级 (Native) |
| 内存占用 | 标准 | 更低 (Native) |

---

## 使用场景

### 1. 云原生 / Serverless

毫秒级冷启动，低内存占用。

```bash
# 编译为原生可执行文件
native-image -jar myfunction.jar
./myfunction -Xmx64m
```

### 2. 微服务

**框架支持**:

| 框架 | Native Image 支持 |
|------|-------------------|
| **Quarkus** | ✅ 原生 |
| **Spring Native** | ✅ 原生 |
| **Micronaut** | ✅ 原生 |
| **Helidon** | ✅ 原生 |

### 3. 多语言应用

```java
// Java + Python 数据科学
try (Context ctx = Context.create()) {
    Value result = ctx.eval("python", 
        "import numpy as np; np.array([1,2,3])");
}
```

---

## 贡献者

### Graal 编译器

| 贡献者 | Commits | 组织 | 主要贡献 |
|--------|---------|------|----------|
| Doug Simon | 600+ | Oracle Labs | Graal 创始人 |
| Christian Wimmer | 400+ | Oracle Labs | Graal 优化 |
| Gilles Duboscq | 300+ | Oracle Labs | Graal IR |
| Peter Hofer | 250+ | Oracle Labs | Native Image |
| Tobias Hartmann | 563 | Oracle | Graal 集成 |
| Tom Rodriguez | 460 | Oracle | 基础设施 |
| Vladimir Ivanov | 448 | Oracle | Graal 优化 |

### Oracle Labs GraalVM 团队

| 成员 | 领域 |
|------|------|
| Doug Simon | 项目负责人 |
| Thomas Würthinger | Truffle 负责人 |
| Christian Wimmer | 编译器优化 |
| Peter Hofer | Native Image |

---

## 安装与使用

### 安装

```bash
# SDKMAN
sdk install java 21-graal
sdk use java 21-graal

# 验证安装
java -version
# OpenJDK Runtime Environment GraalVM ...
```

### 安装组件

```bash
# 安装 native-image
gu install native-image

# 安装 Python 支持
gu install python

# 列出可用组件
gu available
```

### Native Image 快速开始

```bash
# 编译
javac Hello.java

# 生成原生可执行文件
native-image Hello

# 运行
./hello  # 启动时间: < 10ms
```

---

## 性能对比

### 启动时间

| 应用 | JVM 模式 | Native Image | 提升 |
|------|----------|--------------|------|
| Hello World | 100ms | 5ms | 20x |
| Spring Boot | 2-5s | 100-300ms | 10-20x |
| Quarkus | 1-2s | 50-100ms | 10-20x |

### 内存占用

| 应用 | JVM 模式 | Native Image | 节省 |
|------|----------|--------------|------|
| Hello World | 30MB | 5MB | 83% |
| 微服务 | 200MB | 50MB | 75% |

---

## 限制与注意事项

| 限制 | 说明 | 解决方案 |
|------|------|----------|
| 动态类加载 | 运行时加载类受限 | 预配置反射 |
| 动态代理 | JDK 动态代理受限 | 预配置代理 |
| JNI | 需要特殊处理 | 配置 JNI 元数据 |
| 序列化 | 部分受限 | 配置序列化元数据 |

**生成反射配置**:
```bash
# 自动生成配置
java -agentlib:native-image-agent=config-output-dir=META-INF/native-image \
  -jar myapp.jar

# 使用配置编译
native-image -jar myapp.jar
```

---

## 相关链接

### 官方资源

| 资源 | 链接 |
|------|------|
| **官网** | https://www.graalvm.org/ |
| **文档** | https://www.graalvm.org/reference-manual/ |
| **GitHub** | https://github.com/oracle/graal |

### 社区

| 资源 | 链接 |
|------|------|
| **Slack** | https://graalvm.slack.com/ |
| **邮件列表** | graalvm-dev@openjdk.org |
| **Stack Overflow** | [graalvm 标签](https://stackoverflow.com/questions/tagged/graalvm) |

---

## 相关主题

- [JIT 编译](../jit/) - C1、C2、分层编译
- [性能优化](../performance/) - JVM 性能调优
- [HotSpot VM](../jvm/) - JVM 运行时
