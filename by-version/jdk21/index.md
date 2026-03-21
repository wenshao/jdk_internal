# JDK 21

> **状态**: LTS (长期支持) | **GA 发布**: 2023-09-19 | **类型**: Long Term Support

[![OpenJDK](https://img.shields.io/badge/OpenJDK-21-orange)](https://openjdk.org/projects/jdk/21/)
[![LTS](https://img.shields.io/badge/LTS-2031--purple.svg)](https://www.oracle.com/java/technologies/java-se-support.html)

---

## 版本概览

JDK 21 是当前最新的 LTS 版本，引入了虚拟线程等革命性特性：

| 特性 | 状态 | 说明 |
|------|------|------|
| **Virtual Threads** | 正式 (JEP 444) | 虚拟线程，百万级并发 |
| **Pattern Matching for switch** | 正式 (JEP 441) | switch 模式匹配 |
| **Generational ZGC** | 正式 (JEP 439) | 分代 ZGC，降低 GC 频率 |
| **Generational Shenandoah** | 正式 | 分代 Shenandoah |
| **Record Patterns** | 预览 (JEP 440) | 记录模式 |
| **String Templates** | 预览 (JEP 430，后撤销) | 字符串模板 |
| **Scoped Values** | 预览 (JEP 446) | 作用域值 |
| **Structured Concurrency** | 预览 (JEP 453) | 结构化并发 |

---

## GC 状态

| GC | 状态 | 说明 |
|----|------|------|
| **G1 GC** | 默认 | 持续优化 |
| **ZGC** | 正式 (JEP 439) | 支持分代收集，默认分代模式 |
| **Shenandoah** | 正式 | 支持分代收集 |

---

## 迁移指南

### 从 JDK 17 升级

**重要变更**:
- **Virtual Threads 正式版**：可以使用虚拟线程替代传统线程池
- **Pattern Matching for switch 正式版**：更简洁的 switch 语法
- **Generational ZGC 正式版**：ZGC 默认启用分代模式
- 动态代理 `Proxy` 行为变更
- `Thread.stop()` 已被移除

**推荐配置**:
```bash
-XX:+UseZGC                   # 使用 ZGC (默认分代模式)
-Djdk.virtualThreadScheduler.parallelism=256  # 虚拟线程并行度
```

---

## 虚拟线程快速开始

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

## 相关链接

- [JDK 21 发布说明](https://openjdk.org/projects/jdk/21/)
- [虚拟线程指南](https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html)
- [从 JDK 17 迁移](https://docs.oracle.com/en/java/javase/21/migrate/)
