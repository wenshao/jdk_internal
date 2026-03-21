# JDK 25

> **状态**: 已发布 (GA) | **发布日期**: 2025-09-16 | **类型**: LTS

[![OpenJDK](https://img.shields.io/badge/OpenJDK-25-orange)](https://openjdk.org/projects/jdk/25/)
[![License](https://img.shields.io/badge/License-GPLv2--with--Classpath--Exception-blue)](https://openjdk.org/projects/jdk/25/)

---
## 目录

1. [快速导航](#1-快速导航)
2. [版本概览](#2-版本概览)
3. [发布时间线](#3-发布时间线)
4. [代码示例速览](#4-代码示例速览)
5. [JEP 汇总](#5-jep-汇总)
6. [性能改进总览](#6-性能改进总览)
7. [快速开始](#7-快速开始)
8. [相比 JDK 21 的新特性](#8-相比-jdk-21-的新特性)
9. [迁移指南](#9-迁移指南)
10. [深度分析文档](#10-深度分析文档)
11. [相关资源](#11-相关资源)
12. [更多阅读](#12-更多阅读)

---


## 1. 快速导航

| 我想了解 | 链接 |
|---------|------|
| 所有 JEP 详细列表 | [JEP 汇总](./jeps.md) |
| 深度技术分析 | [深度分析文档](./deep-dive/) |
| 如何试用 | [快速开始](#快速开始) |
| 从 JDK 21 升级 | [迁移指南](./migration/from-21.md) |
| 按主题浏览 | [GC](/by-topic/core/gc/timeline.md) · [并发](/by-topic/concurrency/concurrency/timeline.md) |
| 按模块学习 | [模块分析](/modules/) |

---

## 2. 版本概览

JDK 25 是继 JDK 21 (LTS) 之后的下一个长期支持版本，包含多项重要改进：

| 特性 | 影响 | 详情 |
|------|------|------|
| **Scoped Values** | ⭐⭐⭐⭐⭐ | 正式版，虚拟线程场景下 ThreadLocal 的轻量替代方案 |
| **Flexible Constructor Bodies** | ⭐⭐⭐⭐ | 正式版，构造器更灵活 |
| **Compact Object Headers** | ⭐⭐⭐⭐⭐ | 实验性，减少对象头开销 |
| **JFR Method Timing** | ⭐⭐⭐⭐ | 方法级性能追踪 |
| **JFR CPU Profiling** | ⭐⭐⭐ | CPU 时间采样 (实验) |
| **JFR Cooperative Sampling** | ⭐⭐⭐ | 协作采样 |
| **KDF API** | ⭐⭐⭐⭐ | 密钥派生 API |
| **PEM Encodings** | ⭐⭐⭐⭐ | 加密对象 PEM 编码 |
| **结构化并发** | ⭐⭐⭐⭐⭐ | 第五次预览，API 趋于稳定 |
| **Module Import Declarations** | ⭐⭐⭐⭐ | 正式版，简化模块导入 |
| **原始类型模式匹配** | ⭐⭐⭐⭐ | 第三次预览 |
| **Stable Values** | ⭐⭐⭐⭐ | 预览，稳定值 |
| **Compact Source Files** | ⭐⭐⭐ | 正式版，简化源文件 |
| **Vector API** | ⭐⭐⭐ | 第十次孵化 |
| **Generational Shenandoah** | ⭐⭐⭐⭐ | 分代 Shenandoah GC |
| **AOT Ergonomics** | ⭐⭐⭐ | AOT 命令行优化 |
| **AOT Method Profiling** | ⭐⭐⭐ | AOT 方法分析 |
| **String Templates** | ❌ | 已撤销，重新设计中 |

> **注意**: String Templates (JEP 430) 在 JDK 21-22 预览后已被撤销，不在 JDK 25 中。该特性正在重新设计。

---

## 3. 发布时间线

```
2025-06-12    Rampdown Phase 1 (特性冻结)
2025-07-17    Rampdown Phase 2 (代码冻结)
2025-08-14    Initial Release Candidate
2025-09-04    Final Release Candidate
2025-09-16    GA 发布 (LTS)
```

---

## 4. 代码示例速览

### Scoped Values (正式版)

```java
// 声明 ScopedValue
static final ScopedValue<String> USER = ScopedValue.newInstance();

// 在作用域内绑定值
ScopedValue.where(USER, "alice")
    .run(() -> {
        System.out.println(USER.get()); // "alice"
    });
```

### Flexible Constructor Bodies (正式版)

```java
class MyClass {
    private final int value;

    MyClass(int value) {
        this.value = value;
    }

    MyClass() {
        // 可以在 this() 之前执行语句
        int computed = computeValue();
        this(computed);
    }

    private static int computeValue() {
        return 42;
    }
}
```

### 结构化并发 (第五次预览)

```java
try (var scope = StructuredTaskScope.open()) {
    Subtask<String> user = scope.fork(() -> fetchUser(id));
    Subtask<List<Order>> orders = scope.fork(() -> fetchOrders(id));

    scope.join();  // 等待所有子任务完成

    return new Response(user.get(), orders.get());
}
```

### 虚拟线程 (正式版)

```java
// 创建虚拟线程
Thread vthread = Thread.ofVirtual().start(() -> {
    System.out.println("Hello from virtual thread");
});

// 使用 ExecutorService
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 10000; i++) {
        executor.submit(() -> {
            // 处理任务
        });
    }
}
```

### 原始类型模式匹配 (第三次预览)

```java
// switch 中原始类型的精确匹配与范围检查
int code = 200;
String label = switch (code) {
    case 0 -> "zero";
    case int i when i > 0 -> "positive";
    default -> "negative";
};

// instanceof 支持原始类型窄化转换
Object obj = 42;
if (obj instanceof int i) {
    System.out.println("Integer value: " + i);
}
```

### 简化源文件 (正式版)

```java
// 单文件程序无需类声明
void main() {
    System.out.println("Hello, World!");
}

// 带参数的 main
void main(String[] args) {
    for (String arg : args) {
        System.out.println(arg);
    }
}
```

---

## 5. JEP 汇总

### 语言特性

| JEP | 标题 | 状态 | 描述 | 深度分析 |
|-----|------|------|------|----------|
| JEP 507 | Primitive Types in Patterns | 🔍 预览 | 原始类型模式匹配 (第3次) | → |
| JEP 511 | Module Import Declarations | ✅ 正式 | 模块导入声明 | → |
| JEP 502 | Stable Values | 🔍 预览 | 稳定值 | → |
| JEP 512 | Compact Source Files and Instance Main Methods | ✅ 正式 | 简化源文件 | → |
| [JEP 513](/jeps/language/jep-513.md) | Flexible Constructor Bodies | ✅ 正式 | 灵活构造器 | → |
| [JEP 503](/jeps/removed/jep-503.md) | Remove 32-bit x86 Port | ✅ 正式 | 移除 32 位 x86 | → |

### 性能

| JEP | 标题 | 影响 | 描述 | 深度分析 |
|-----|------|------|------|----------|
| [JEP 519](/jeps/gc/jep-519.md) | Compact Object Headers (Experimental) | 🚀 内存优化 | 紧凑对象头 (实验性) | → |
| [JEP 520](/jeps/jfr/jep-520.md) | JFR Method Timing | 🚀 性能追踪 | JFR 方法计时 | → |
| JEP 508 | Vector API (Tenth Incubator) | 🚀 SIMD | 向量 API（第10次孵化） | → |
| JEP 514 | Ahead-of-Time Command-Line Ergonomics | 🚀 启动 | AOT 命令行优化 | → |
| JEP 515 | Ahead-of-Time Method Profiling | 🚀 启动 | AOT 方法分析 | → |

### 并发

| JEP | 标题 | 状态 | 描述 | 深度分析 |
|-----|------|------|------|----------|
| [JEP 505](/jeps/concurrency/jep-505.md) | Structured Concurrency | 🔍 预览 | 结构化并发 (第5次) | → |
| [JEP 506](/jeps/concurrency/jep-506.md) | Scoped Values | ✅ 正式 | 作用域值 | [→](/deep-dive/jep-506-implementation.md) |

### 安全

| JEP | 标题 | 状态 | 描述 | 深度分析 |
|-----|------|------|------|----------|
| [JEP 510](/jeps/security/jep-510.md) | Key Derivation Function API | ✅ 正式 | KDF API | → |
| [JEP 470](/jeps/security/jep-470.md) | PEM Encodings | 🔍 预览 | PEM 编码 | → |

### JFR / 监控

| JEP | 标题 | 状态 | 描述 | 深度分析 |
|-----|------|------|------|----------|
| JEP 509 | JFR CPU-Time Profiling | ⚠️ 实验 | CPU 时间采样 | → |
| JEP 518 | JFR Cooperative Sampling | ✅ 正式 | 协作采样 | → |

### GC

| JEP | 标题 | 状态 | 描述 | 深度分析 |
|-----|------|------|------|----------|
| JEP 521 | Generational Shenandoah | ✅ 正式 | 分代 Shenandoah | → |

> 图例: ✅ 正式发布 | 🔍 预览特性 (需要 `--enable-preview`) | 🚀 性能提升 | ⚠️ 废弃/移除 | ⚠️ 实验性

---

[查看所有 JEP 详情 →](./jeps.md)

---

## 6. 性能改进总览

| 领域 | 改进 | 数据 | 深度分析 |
|------|------|------|----------|
| **内存** | 紧凑对象头 (实验性) | 对象头从 12-16 字节压缩至 8 字节 | [→](/jeps/gc/jep-519.md) |
| **启动时间** | AOT 命令行优化 | AOT 缓存简化启动流程 | → |
| **并发** | Scoped Values | 虚拟线程场景下 ThreadLocal 的轻量替代 | [→](/deep-dive/jep-506-implementation.md) |
| **追踪** | JFR 方法计时 | 低开销方法级追踪 | [→](/jeps/jfr/jep-520.md) |

---

## 7. 快速开始

### 下载安装

```bash
# 使用 SDKMAN
sdk install java 25

# 使用 Homebrew (macOS)
brew install openjdk@25

# 从源码构建
git clone https://github.com/openjdk/jdk.git
cd jdk
sh configure
make images
```

### 启用预览特性

```bash
# 编译时启用预览特性
javac --release 25 --enable-preview MyClass.java

# 运行时启用预览特性
java --enable-preview MyClass
```

### Scoped Values 快速体验

```java
public class ScopedValueDemo {
    public static final ScopedValue<String> USER = ScopedValue.newInstance();

    public static void main(String[] args) {
        // 在作用域内设置值
        ScopedValue.where(USER, "alice")
            .run(() -> {
                System.out.println("User: " + USER.get()); // "User: alice"
            });

        // 虚拟线程中需要在 ScopedValue.where 作用域内使用
        ScopedValue.where(USER, "bob")
            .run(() -> Thread.ofVirtual().start(() -> {
                System.out.println("Virtual thread user: " + USER.get()); // "bob"
            }));
    }
}
```

### JVM 参数建议

```bash
# ZGC (推荐用于大内存应用，默认分代模式)
java -XX:+UseZGC MyApp

# 虚拟线程 (高并发 I/O)
java -Djdk.virtualThreadScheduler.parallelism=4 MyApp

# 结构化并发 (需要预览)
java --enable-preview MyApp
```

---

## 8. 相比 JDK 21 的新特性

### 语言

- **Scoped Values** (JEP 506)：正式版，虚拟线程场景下 ThreadLocal 的轻量替代方案
- **Flexible Constructor Bodies** (JEP 513)：正式版，构造器更灵活
- **Module Import Declarations** (JEP 511)：正式版，简化模块导入
- **Primitive Types in Patterns** (JEP 507)：第3次预览

### 性能

- **Compact Object Headers** (JEP 519)：实验性，减少对象头开销
- **JFR Method Timing** (JEP 520)：方法级性能追踪

### 并发

- **结构化并发** (JEP 505)：第五次预览，API 更稳定

### 安全

- **KDF API** (JEP 510)：密钥派生函数 API
- **PEM Encodings** (JEP 470)：PEM 格式支持

### 移除

- **32-bit x86 Port** (JEP 503)：移除 32 位 x86 支持

### 注意事项

- **String Templates** 已从 JDK 25 中撤销，正在重新设计
- **Virtual Threads** 在 JDK 21 已是正式版，无变化

---

## 9. 迁移指南

### 从 JDK 21 升级

#### ✅ 兼容性

JDK 25 与 JDK 21 具有良好的二进制兼容性，大部分应用可以直接运行。

#### ⚠️ 破坏性变更

| 变更 | 影响 | 建议 |
|------|------|------|
| 32-bit x86 移除 | 32 位 x86 平台用户 | 迁移到 64 位 |
| String Templates 撤销 | 使用了 JDK 21-22 预览版 String Templates 的代码 | 改用传统字符串拼接或 String.format |
| Security Manager 进一步限制 | 依赖 Security Manager 的应用 | 迁移至其他安全机制 |

#### 🚀 推荐使用的新特性

| 场景 | 推荐特性 | 深度分析 |
|------|----------|----------|
| ThreadLocal 替代方案 (虚拟线程场景) | Scoped Values | [→](/deep-dive/jep-506-implementation.md) |
| 大内存应用 | ZGC (默认分代模式) | → |
| 高并发 I/O | 虚拟线程 | → |
| 并发任务 | 结构化并发 | → |
| 构造器逻辑复杂 | Flexible Constructor Bodies | [→](/jeps/language/jep-513.md) |

#### 🔧 性能调优建议

参见 [快速开始](#7-快速开始) 中的 JVM 参数建议。

---

## 10. 深度分析文档

| 主题 | 描述 | 链接 |
|------|------|------|
| Scoped Values | 作用域值实现 | [→](/deep-dive/jep-506-implementation.md) |
| Flexible Constructor Bodies | 灵活构造器 | [→](/jeps/language/jep-513.md) |
| Compact Object Headers | 紧凑对象头 | [→](/jeps/gc/jep-519.md) |
| JFR Method Timing | JFR 方法计时 | [→](/jeps/jfr/jep-520.md) |
| Module Import Declarations | 模块导入声明 | [→](/deep-dive/jep-511-implementation.md) |
| DateTime toString 优化 | 日期时间格式化性能 | [→](./deep-dive/datetime-tostring-optimization.md) |
| I/O 优化 | DataInput/Output UTF 处理 | [→](./deep-dive/io-optimization.md) |

---

## 11. 相关资源

### 本地文档

| 资源 | 链接 |
|------|------|
| **按主题浏览** | [GC](/by-topic/core/gc/timeline.md) · [并发](/by-topic/concurrency/concurrency/timeline.md) · [HTTP](/by-topic/concurrency/http/timeline.md) |
| **模块分析** | [java.base](/modules/java.base.md) · [concurrent](/modules/concurrent.md) · [hotspot](/modules/hotspot.md) |
| **JEP 分析** | [JEP 468](/jeps/tools/jep-468.md) · [JEP 462](/jeps/concurrency/jep-462.md) · [JEP 444](/jeps/concurrency/jep-444.md) |
| **深度分析** | [JEP 506](/deep-dive/jep-506-implementation.md) · [JEP 517](/deep-dive/jep-517-implementation.md) |
| **指南** | [速查表](/guides/cheat-sheet.md) · [FAQ](/guides/faq.md) · [学习路径](/guides/learning-path.md) |

### 官方资源

| 资源 | 链接 |
|------|------|
| **官方发布计划** | [openjdk.org/projects/jdk/25](https://openjdk.org/projects/jdk/25/) |
| **JEP 完整列表** | [openjdk.org/jeps/0](https://openjdk.org/jeps/0) |
| **官方下载** | [openjdk.org](https://openjdk.org/projects/jdk/25/) |
| **发布公告** | [openjdk.org/blog](https://openjdk.org/blog/) |

---

## 12. 更多阅读

### 相关版本

- [JDK 21](/by-version/jdk21/) - 上一个 LTS 版本
- [JDK 24](/by-version/jdk24/) - 前一个功能版本
- [JDK 26](/by-version/jdk26/) - 下一个功能版本

### 按主题浏览

- [GC 演进](/by-topic/core/gc/timeline.md) - G1/ZGC/Shenandoah 时间线
- [并发编程](/by-topic/concurrency/concurrency/timeline.md) - Virtual Threads, Structured Concurrency
- [字符串处理](/by-topic/language/string/timeline.md) - 字符串 API 演进
- [HTTP 客户端](/by-topic/concurrency/http/timeline.md) - HTTP Client, HTTP/3

### 按贡献者浏览

- [贡献者索引](/by-contributor/) - 了解贡献者和他们的工作
- [JDK 26 Top 100](/by-contributor/profiles/jdk26-top-contributors.md) - JDK 26 贡献者排名
- [中国贡献者](/by-contributor/profiles/chinese-contributors.md) - 中国开发者贡献
