# JDK 25

> **状态**: 已发布 (GA) | **发布日期**: 2025-09-16 | **类型**: LTS

[![OpenJDK](https://img.shields.io/badge/OpenJDK-25-orange)](https://openjdk.org/projects/jdk/25/)
[![License](https://img.shields.io/badge/License-GPLv2--with--Classpath--Exception-blue)](https://openjdk.org/projects/jdk/25/)

---

## 快速导航

| 我想了解 | 链接 |
|---------|------|
| 所有 JEP 详细列表 | [JEP 汇总](./jeps.md) |
| 重要 PR 分析 | [Top 50 Commits](/prs/jdk25-top-prs.md) |
| 深度技术分析 | [深度分析文档](./deep-dive/) |
| 如何试用 | [快速开始](#快速开始) |
| 从 JDK 21 升级 | [迁移指南](./migration/from-21.md) |

---

## 版本概览

JDK 25 是继 JDK 21 (LTS) 之后的下一个长期支持版本，包含多项重要改进：

| 特性 | 影响 | 详情 |
|------|------|------|
| **分代 ZGC** | ⭐⭐⭐⭐⭐ | 降低 GC 开销，提升大内存场景性能 |
| **结构化并发** | ⭐⭐⭐⭐⭐ | 第五次预览，API 趋于稳定 |
| **String Templates** | ⭐⭐⭐⭐⭐ | 正式版，字符串插值 |
| **原始类型模式匹配** | ⭐⭐⭐⭐ | 第三次预览 |
| **隐式类** | ⭐⭐⭐ | 第四次预览，简化单文件程序 |

---

## 发布时间线

```
2024-03-15    Rampdown Phase 1 (特性冻结)
2024-06-13    Rampdown Phase 2 (代码冻结)
2024-07-16    Initial Release Candidate
2025-07-18    Final Release Candidate
2025-09-16    GA 发布 (LTS)
```

---

## 代码示例速览

### String Templates

```java
// 之前：字符串拼接
String message = "Hello, " + name + "! Today is " + day + ".";

// 现在：字符串模板
String message = STR."Hello, \{name}! Today is \{day}.";

// 多行模板
String json = JSON."""
    {
        "name": "\{name}",
        "age": \{age},
        "active": \{active}
    }
    """;
```

### 结构化并发

```java
try (var scope = new StructuredTaskScope<Object>()) {
    Subtask<String> user = scope.fork(() -> fetchUser(id));
    Subtask<List<Order>> orders = scope.fork(() -> fetchOrders(id));

    scope.join();  // 等待所有子任务完成
    scope.throwIfFailed();  // 如果有失败则抛出异常

    return new Response(user.get(), orders.get());
}
```

### 原始类型模式匹配

```java
// switch 支持原始类型
String formatted = switch (value) {
    case int i -> String.format("int: %d", i);
    case long l -> String.format("long: %d", l);
    case double d -> String.format("double: %f", d);
    default -> "unknown";
};
```

### 隐式类

```java
// 单文件程序无需类声明
void main() {
    System.out.println("Hello, World!");
}

// 自动包装为隐式类
```

---

## JEP 汇总

### 语言特性

| JEP | 标题 | 状态 | 描述 |
|-----|------|------|------|
| [JEP 455](/jeps/jep-455.md) | Primitive Types in Patterns | 🔍 预览 | 模式匹配支持原始类型 |
| [JEP 469](/jeps/jep-469.md) | Implicit Classes and Instance Main Methods | 🔍 预览 | 隐式类 (第4次) |
| [JEP 466](/jeps/jep-466.md) | Class-File API (Second Preview) | 🔍 预览 | 类文件 API |
| [JEP 454](/jeps/jep-454.md) | Foreign Function & Memory API | ✅ 正式 | FFM API 正式版 |
| [JEP 444](/jeps/jep-444.md) | Virtual Threads | ✅ 正式 | 虚拟线程正式版 |
| [JEP 430](/jeps/jep-430.md) | String Templates | ✅ 正式 | 字符串模板 |

### 性能

| JEP | 标题 | 影响 | 描述 |
|-----|------|------|------|
| [JEP 468](/jeps/jep-468.md) | Generational ZGC | 🚀 大幅提升 | 分代 ZGC |
| [JEP 462](/jeps/jep-462.md) | Structured Concurrency | 🔍 预览 | 结构化并发 (第5次) |
| [JEP 448](/jeps/jep-448.md) | JVM Code Heap | 🚀 启动优化 | 代码堆分段 |
| [JEP 449](/jeps/jep-449.md) | Barrier-Based C2 | 🚀 吞吐量 | C2 编译器优化 |

### 并发

| JEP | 标题 | 状态 | 描述 |
|-----|------|------|------|
| [JEP 462](/jeps/jep-462.md) | Structured Concurrency | 🔍 预览 | 结构化并发 (第5次) |
| [JEP 467](/jeps/jep-467.md) | Scoped Values | 🔍 预览 | 作用域值 (第3次) |

### 安全

| JEP | 标题 | 状态 | 描述 |
|-----|------|------|------|
| [JEP 451](/jeps/jep-451.md) | Prepare to Restrict Dynamic Loading | ⚠️ 废弃 | 动态加载限制 |
| [JEP 452](/jeps/jep-452.md) | Key Encapsulation Mechanism API | ✅ 正式 | KEM API |

> 图例: ✅ 正式发布 | 🔍 预览特性 (需要 `--enable-preview`) | 🚀 性能提升 | ⚠️ 废弃/移除

---

[查看所有 JEP 详情 →](./jeps.md)

---

## 性能改进总览

| 领域 | 改进 | 数据 |
|------|------|------|
| **ZGC** | 分代收集 | -50% GC 开销 |
| **启动时间** | 代码堆优化 | ~5-10% |
| **吞吐量** | C2 barrier 优化 | ~3-5% |
| **内存** | 字符串模板优化 | 减少临时对象 |

---

## 快速开始

### 下载安装

```bash
# 使用 SDKMAN
sdk install java 25

# 或从 Oracle/OpenJDK 下载
https://openjdk.org/projects/jdk/25/
```

### 启用预览特性

```bash
# 编译时启用预览特性
javac --release 25 --enable-preview MyClass.java

# 运行时启用预览特性
java --enable-preview MyClass
```

### String Templates 快速体验

```java
import static java.util.Format.*;

public class TemplateDemo {
    public static void main(String[] args) {
        String name = "World";
        int count = 42;

        // STR 模板
        String message = STR."Hello, \{name}! Count: \{count}";
        System.out.println(message);

        // JSON 模板
        String json = JSON."""
            {
                "greeting": "\{name}",
                "value": \{count}
            }
            """;
        System.out.println(json);
    }
}
```

### JVM 参数建议

```bash
# 分代 ZGC (推荐用于大内存应用)
java -XX:+UseZGC -XX:+ZGenerational MyApp

# 虚拟线程 (高并发 I/O)
java -Djdk.virtualThreadScheduler.parallelism=4 MyApp

# 结构化并发
java --enable-preview MyApp
```

---

## 相比 JDK 21 的新特性

### 语言

- **String Templates** (JEP 430)：字符串插值，类似 Python f-string
- **原始类型模式匹配** (JEP 455)：switch 支持原始类型
- **隐式类** (JEP 469)：简化单文件程序

### 性能

- **分代 ZGC** (JEP 468)：大幅降低 GC 开销
- **JVM Code Heap** (JEP 448)：启动时间优化
- **C2 Barrier 优化** (JEP 449)：吞吐量提升

### 并发

- **结构化并发** (JEP 462)：第五次预览，API 稳定
- **Scoped Values** (JEP 467)：第三次预览
- **虚拟线程** (JEP 444)：正式版

### 安全

- **KEM API** (JEP 452)：密钥封装机制
- **动态加载限制** (JEP 451)：准备限制动态加载

---

## 迁移指南

### 从 JDK 21 升级

#### ✅ 兼容性

JDK 25 与 JDK 21 具有良好的二进制兼容性，大部分应用可以直接运行。

#### ⚠️ 破坏性变更

| 变更 | 影响 | 建议 |
|------|------|------|
| Security Manager 限制 | 使用自定义 Security Manager | 评估影响 |

#### 🚀 推荐使用的新特性

| 场景 | 推荐特性 |
|------|----------|
| 字符串处理 | String Templates |
| 大内存应用 | 分代 ZGC |
| 高并发 I/O | 虚拟线程 |
| 并发任务 | 结构化并发 |

#### 🔧 性能调优建议

```bash
# 1. 大内存应用使用分代 ZGC
java -XX:+UseZGC -XX:+ZGenerational MyApp

# 2. 高并发 I/O 使用虚拟线程
java -Djdk.virtualThreadScheduler.parallelism=4 MyApp

# 3. 启用字符串模板
java --enable-preview MyApp
```

---

## 相关链接

| 资源 | 链接 |
|------|------|
| **官方发布计划** | [openjdk.org/projects/jdk/25](https://openjdk.org/projects/jdk/25/) |
| **JEP 完整列表** | [openjdk.org/jeps/0](https://openjdk.org/jeps/0) |
| **官方下载** | [openjdk.org](https://openjdk.org/projects/jdk/25/) |
| **发布公告** | [openjdk.org/blog](https://openjdk.org/blog/) |

---

## 更多阅读

- [JDK 25 JEP 汇总](./jeps.md) - 所有 JEP 详细列表
- [Top 50 Commits](/prs/jdk25-top-prs.md) - 重要的代码变更
- [按主题浏览](/by-topic/) - 跨版本追踪技术演进
- [按贡献者浏览](/by-contributor/) - 了解贡献者和他们的工作
