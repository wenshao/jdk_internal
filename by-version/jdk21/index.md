# JDK 21

> **状态**: LTS (长期支持) | **GA 发布**: 2023-09-19 | **类型**: Long Term Support

[![OpenJDK](https://img.shields.io/badge/OpenJDK-21-orange)](https://openjdk.org/projects/jdk/21/)
[![LTS](https://img.shields.io/badge/LTS-2031--purple.svg)](https://www.oracle.com/java/technologies/java-se-support.html)

---
## 目录

1. [版本概览](#1-版本概览)
2. [关键 JEP](#2-关键-jep)
3. [GC 状态](#3-gc-状态)
4. [迁移指南](#4-迁移指南)
5. [虚拟线程快速开始](#5-虚拟线程快速开始)
6. [相关链接](#6-相关链接)

---


## 1. 版本概览

JDK 21 是继 JDK 17 之后的 LTS 版本，引入了虚拟线程等重要特性：

| 特性 | 状态 | 说明 |
|------|------|------|
| **Virtual Threads** | 正式 (JEP 444) | 虚拟线程，支持大规模并发 |
| **Pattern Matching for switch** | 正式 (JEP 441) | switch 模式匹配 |
| **Generational ZGC** | 正式 (JEP 439) | 分代 ZGC，可减少内存开销 |
| **Record Patterns** | 正式 (JEP 440) | 记录模式 |
| **String Templates** | 预览 (JEP 430，后撤销) | 字符串模板 |
| **Scoped Values** | 预览 (JEP 446) | 作用域值 |
| **Structured Concurrency** | 预览 (JEP 453) | 结构化并发 |
| **Sequenced Collections** | 正式 (JEP 431) | 有序集合 |
| **Unnamed Patterns and Variables** | 预览 (JEP 443) | 未命名模式和变量 |
| **Unnamed Classes** | 预览 (JEP 445) | 未命名类 |
| **Vector API** | 孵化 (JEP 448) | 向量 API（第6次孵化） |
| **Foreign Function & Memory API** | 预览 (JEP 442) | FFM API（第3次预览） |
| **KEM API** | 正式 (JEP 452) | 密钥封装机制 API |

---

## 2. 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 430](https://openjdk.org/jeps/430) | String Templates (Preview) | 字符串模板（后撤销） |
| [JEP 431](https://openjdk.org/jeps/431) | Sequenced Collections | 有序集合 |
| [JEP 439](https://openjdk.org/jeps/439) | Generational ZGC | 分代 ZGC |
| [JEP 440](https://openjdk.org/jeps/440) | Record Patterns | 记录模式 |
| [JEP 441](https://openjdk.org/jeps/441) | Pattern Matching for switch | switch 模式匹配 |
| [JEP 442](https://openjdk.org/jeps/442) | Foreign Function & Memory API (Third Preview) | FFM API（第3次预览） |
| [JEP 443](https://openjdk.org/jeps/443) | Unnamed Patterns and Variables (Preview) | 未命名模式和变量 |
| [JEP 444](https://openjdk.org/jeps/444) | Virtual Threads | 虚拟线程 |
| [JEP 445](https://openjdk.org/jeps/445) | Unnamed Classes and Instance Main Methods (Preview) | 未命名类 |
| [JEP 446](https://openjdk.org/jeps/446) | Scoped Values (Preview) | 作用域值 |
| [JEP 448](https://openjdk.org/jeps/448) | Vector API (Sixth Incubator) | Vector API（第6次孵化） |
| [JEP 449](https://openjdk.org/jeps/449) | Deprecate the Windows 32-bit x86 Port for Removal | 废弃 32 位 Windows |
| [JEP 451](https://openjdk.org/jeps/451) | Prepare to Disallow the Dynamic Loading of Agents | 准备禁止动态加载代理 |
| [JEP 452](https://openjdk.org/jeps/452) | Key Encapsulation Mechanism API | KEM API |
| [JEP 453](https://openjdk.org/jeps/453) | Structured Concurrency (Preview) | 结构化并发 |

---

## 3. GC 状态

| GC | 状态 | 说明 |
|----|------|------|
| **G1 GC** | 默认 | 持续优化 |
| **ZGC** | 正式 (JEP 439) | 支持分代收集，需使用 -XX:+ZGenerational 启用分代模式（JDK 21 起才为默认） |
| **Shenandoah** | 正式 | 低延迟 GC |

---

## 4. 迁移指南

### 从 JDK 17 升级

**重要变更**:
- **Virtual Threads 正式版**：可以使用虚拟线程作为传统线程池的轻量级替代方案（线程池仍适用于 CPU 密集型场景）
- **Pattern Matching for switch 正式版**：更简洁的 switch 语法
- **Generational ZGC 正式版**：ZGC 支持分代模式（需使用 -XX:+ZGenerational 启用）
- 动态代理 `Proxy` 行为变更
- `Thread.stop()` 改为抛出 `UnsupportedOperationException`

**推荐配置**:
```bash
-XX:+UseZGC -XX:+ZGenerational  # 使用 ZGC（需显式启用分代模式，JDK 23 起才为默认）
# 虚拟线程调度器并行度默认为 Runtime.availableProcessors()，通常无需调整
```

---

## 5. 虚拟线程快速开始

```java
// 传统方式 (平台线程)
try (var executor = Executors.newFixedThreadPool(100)) {
    executor.submit(() -> task());
}

// 虚拟线程 (JDK 21+)
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> task());
}
```

---

## 6. 相关链接

- [JDK 21 发布说明](https://openjdk.org/projects/jdk/21/)
- [虚拟线程指南](https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html)
- [从 JDK 17 迁移](https://docs.oracle.com/en/java/javase/21/migrate/)
