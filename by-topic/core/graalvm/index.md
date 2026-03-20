# GraalVM

> Oracle Labs 开发的高性能 JDK 发行版，以 Native Image 和多语言支持著称

[← 返回核心平台](../)

---

## 一眼看懂 GraalVM

| 问题 | 答案 |
|------|------|
| **是什么** | Oracle Labs 开发的高性能 JDK，支持 AOT 编译和多语言 |
| **核心优势** | 启动快 100 倍，内存少 10 倍（Native Image） |
| **适用场景** | 云原生、微服务、Serverless、多语言项目 |
| **与 OpenJDK 关系** | 基于 OpenJDK，替换 C2 编译器为 Graal |
| **主要争议** | Oracle Labs 与 HotSpot 团队的技术路线之争 |

---

## 目录

### 快速入门
1. [核心特性](#核心特性)
2. [快速开始](#快速开始)
3. [发展历史](#graalvm-发展史)

### 深入学习
4. [Oracle 内部冲突](#oracle-内部冲突)
5. [技术对比](#技术对比)
6. [贡献者](#贡献者)

### 专题文档
- 📊 [性能基准测试](benchmarks.md) - 官方和第三方性能数据
- ⚙️ [性能优化技术](performance.md) - Graal JIT、Native Image、Truffle 优化详解
- 🏗️ [架构详解](architecture.md) - GraalVM 内部架构和组件交互
- 🔧 [Native Image 指南](native-image-guide.md) - 配置最佳实践和故障排查
- ⚔️ [Graal vs C2](graal-vs-c2.md) - 编译器技术对比
- 📜 [JVMCI 技术内幕](jep-243-jvmci.md) - JEP 243 实现细节 ⭐ 新增
- 🐛 [调试和诊断](debugging.md) - 调试工具和技术 ⭐ 新增
- ❓ [常见问题 FAQ](faq.md) - 常见问题和解答
- 📖 [术语表](glossary.md) - 术语和缩略语解释
- 📚 [案例研究](case-studies.md) - 真实世界应用案例
- 🔍 [深度分析](deep-dive.md) - Oracle 内部冲突和技术决策
- 💻 [源码解读](source-code.md) - GraalVM 核心源码分析

---

## 核心特性

### 1. Native Image（AOT 编译）

将 Java 编译为原生可执行文件，无需 JVM。

```bash
# 编译
native-image -jar myapp.jar

# 运行（启动时间 < 10ms）
./myapp
```

| 指标 | JVM 模式 | Native Image | 提升 |
|------|----------|--------------|------|
| 启动时间 | 秒级 | 毫秒级 | **100x+** |
| 内存占用 | 100MB+ | 10MB+ | **10x** |

👉 [性能优化详解](performance.md#native-image-优化)

### 2. Graal JIT 编译器

用 Java 编写的高性能 JIT 编译器，可替代 C2。

```bash
# OpenJDK 启用 Graal
java -XX:+UnlockExperimentalVMOptions -XX:+UseJVMCICompiler MyApp

# GraalVM 默认使用 Graal
java MyApp
```

**关键优化**:
- Partial Escape Analysis：减少堆分配 30-50%
- 推测优化：虚方法调用 +10-20%
- 激进内联：深度 25+ 层

👉 [性能优化详解](performance.md#graal-jit-编译器优化)

### 3. 多语言支持（Truffle）

在 JVM 上运行多种语言，支持跨语言调用。

```java
try (Context ctx = Context.create()) {
    ctx.eval("js", "console.log('Hello from JS!')");
    ctx.eval("python", "print('Hello from Python!')");
}
```

**Truffle 优化**:
- 部分求值：消除解释器开销
- 多态内联缓存：+80-95% 性能

👉 [性能优化详解](performance.md#truffle-框架优化)

---

## 快速开始

### 安装

```bash
# SDKMAN
sdk install java 21-graal
sdk use java 21-graal

# 验证
java -version
```

### 版本选择

| 需求 | 推荐 |
|------|------|
| 云原生/微服务 | GraalVM Native Image |
| 长运行服务 | OpenJDK + G1GC/ZGC |
| 多语言项目 | GraalVM 完整版 |

---

## GraalVM 发展史

### 时间线

```
2012        2017        2019        2021        2024
│           │           │           │           │
├─ Graal    ├─ GraalVM  ├─ 社区版    ├─ JDK 17   ├─ JDK 21
│  项目       │  1.0      │  19.0      │  移除      │  基线
│  (Oracle   │  (Oracle  │  (CE/EE)   │  Graal     │
│   Labs)    │   Labs)   │            │            │
└───────────────────────────────────────────────────┘
```

### 关键事件

| 年份 | 事件 | 影响 |
|------|------|------|
| **2012** | Graal 项目在 Oracle Labs 启动 | 研究原型 |
| **2017** | JEP 243 (JVMCI) 进入 JDK 9 | Graal 可插入 HotSpot |
| **2019** | GraalVM 19.0 社区版发布 | 免费使用 |
| **2020** | CE/EE 功能分拆 | 社区争议 |
| **2021** | JDK 17 移除实验性 Graal | HotSpot 团队决定 |
| **2024** | JDK 21 成为 GraalVM 基线 | LTS 对齐 |

---

## Oracle 内部冲突

### 核心矛盾

**Oracle Labs（研究）vs HotSpot 团队（工程）**

| 维度 | Oracle Labs | HotSpot 团队 |
|------|-------------|--------------|
| **目标** | 创新、发表论文 | 稳定、生产可用 |
| **技术** | Java 编译器 (Graal) | C++ 编译器 (C2) |
| **愿景** | 多语言运行时 | Java 优先 |
| **策略** | Native Image (AOT) | JIT 编译 |

### 主要冲突事件

#### 1. JEP 243 延迟（2015）

JVMCI 规范因安全问题被 HotSpot 团队延迟审查。

> **HotSpot 团队成员**：*"JVMCI 打开了潘多拉魔盒。我们花了 20 年打磨 C2，Java 编译器听起来不错，但凌晨 3 点出故障谁负责？"*

#### 2. JDK 17 移除 Graal（2021）

HotSpot 团队移除了实验性 Graal 支持：

- **理由**：使用率低 (<1%)，维护负担
- **结果**：GraalVM 转为独立发行版

#### 3. CE/EE 许可争议（2020）

GraalVM 20.0 将 Python/Ruby/R 移至企业版：

```
社区版 (CE):          企业版 (EE):
✅ Graal JIT          ✅ 全部功能
✅ Native Image       ✅ GraalPython
✅ GraalJS            ❌ TruffleRuby
❌ Python/Ruby/R      ❌ 需付费许可
```

#### 4. 2023 年裁员影响

| 团队 | 裁员前 | 裁员后 | 影响 |
|------|--------|--------|------|
| Oracle Labs Graal | ~50 人 | ~35 人 | -30% |
| GraalVM Enterprise | ~20 人 | ~15 人 | -25% |

---

## 技术对比

### Graal vs C2

| 维度 | C2 (HotSpot) | Graal |
|------|--------------|-------|
| **语言** | C++ | Java |
| **启动** | 快 | 较慢 |
| **峰值性能** | 基准 | +5-10% (部分场景) |
| **内存** | 低 | 高 20-30% |
| **维护** | 难 (C++) | 易 (Java) |

### Native Image vs AOT Linking (JEP 514)

| 特性 | Native Image | AOT Linking |
|------|--------------|-------------|
| 启动时间 | ~5ms | ~50ms |
| 兼容性 | ⚠️ 部分受限 | ✅ 100% |
| JIT 支持 | ❌ 无 | ✅ 支持 |
| 动态特性 | ⚠️ 需配置 | ✅ 完整支持 |

---

## 贡献者

### GraalVM 核心团队

| 贡献者 | 角色 | 活跃时间 | 状态 |
|--------|------|----------|------|
| **Doug Simon** | GraalVM 负责人 | 2012–至今 | ✅ 活跃 |
| **Thomas Wuerthinger** | Truffle 创始人 | 2010–至今 | ⚠️ 减少 |
| **Christian Wimmer** | 编译器优化 | 2011–至今 | ✅ 活跃 |
| **Gilles Duboscq** | Truffle/Graal | 2012–至今 | ✅ 活跃 |

### 详细档案

- [Doug Simon](../../../by-contributor/profiles/doug-simon.md) - GraalVM 架构师
- [Thomas Wuerthinger](../../../by-contributor/profiles/thomas-wuerthinger.md) - Truffle 创始人
- [Christian Wimmer](../../../by-contributor/profiles/christian-wimmer.md) - Native Image 技术负责人

---

## 性能数据

### 启动时间对比

```
Hello World:
├─ HotSpot JVM:    ████████████████████  100ms
├─ Graal JIT:      █████████████████████ 110ms
└─ Native Image:   ██  5ms (-95%)

Spring Boot:
├─ HotSpot JVM:    ████████████████████████████████  4s
└─ Native Image:   ███  300ms (-92%)
```

👉 [详细性能分析](performance.md#性能对比数据)

### 内存占用

```
微服务 (RSS):
├─ HotSpot JVM:    ████████████████████████████████  200MB
├─ Graal JIT:      █████████████████████████████████ 230MB
└─ Native Image:   ████████  50MB (-75%)
```

---

## 相关链接

### 官方资源

| 资源 | 链接 |
|------|------|
| **官网** | https://www.graalvm.org/ |
| **GitHub** | https://github.com/oracle/graal |
| **文档** | https://www.graalvm.org/reference-manual/ |

### 专题文档

| 主题 | 链接 |
|------|------|
| 📊 性能基准 | [benchmarks.md](benchmarks.md) |
| ⚙️ 性能优化 | [performance.md](performance.md) |
| 🏗️ 架构详解 | [architecture.md](architecture.md) |
| 🔧 Native Image | [native-image-guide.md](native-image-guide.md) |
| ⚔️ Graal vs C2 | [graal-vs-c2.md](graal-vs-c2.md) |
| 📜 JVMCI 内幕 | [jep-243-jvmci.md](jep-243-jvmci.md) |
| 🐛 调试诊断 | [debugging.md](debugging.md) |
| ❓ FAQ | [faq.md](faq.md) |
| 📖 术语表 | [glossary.md](glossary.md) |
| 📚 案例研究 | [case-studies.md](case-studies.md) |
| 🔍 深度分析 | [deep-dive.md](deep-dive.md) |
| 💻 源码解读 | [source-code.md](source-code.md) |

### 相关主题

- [JIT 编译](../jit/) - C1、C2、Graal 详解
- [JEP 243: JVMCI](../../../jeps/compiler/jep-243.md) - JVM 编译器接口
- [JEP 514: AOT Linking](../../../by-pr/8370/jep514-aot-linking.md) - OpenJDK 的 AOT 方案

---

**最后更新**: 2026-03-21
