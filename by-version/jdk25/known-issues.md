# JDK 25 已知问题

> **版本**: JDK 25 (LTS) | **发布日期**: 2025-09-16 | **最后更新**: 2026-03-23

---
## 目录

1. [概述](#1-概述)
2. [预览特性限制](#2-预览特性限制)
3. [实验性特性注意事项](#3-实验性特性注意事项)
4. [兼容性问题](#4-兼容性问题)
5. [平台特定问题](#5-平台特定问题)
6. [框架兼容性](#6-框架兼容性)
7. [相关链接](#7-相关链接)

---


## 1. 概述

JDK 25 作为 LTS 版本整体稳定性良好。以下问题主要影响特定使用场景或预览/实验性特性。

| 类别 | 问题数 | 严重程度 |
|------|--------|----------|
| 预览特性限制 | 3 | 🟡 中 |
| 实验性特性 | 2 | 🟡 中 |
| 兼容性 | 2 | 🟢 低 |
| 平台特定 | 2 | 🟢 低 |

---

## 2. 预览特性限制

### 结构化并发（第五次预览）

**状态**: 预览特性，API 可能在后续版本变化

**注意事项**:
- 需要 `--enable-preview` 编译和运行
- `StructuredTaskScope` 的 API 自 JDK 21 以来有多次变更
- 不建议在生产代码中使用，除非做好跟随版本升级的准备

```bash
# 必须启用预览
javac --release 25 --enable-preview MyApp.java
java --enable-preview MyApp
```

### 原始类型模式匹配（第三次预览）

**注意事项**:
- `instanceof` 和 `switch` 对原始类型的模式匹配仍在调整
- 与现有 autoboxing 规则可能存在边界情况

### Stable Values（预览）

**注意事项**:
- `StableValue` API 是新引入的预览特性
- 与 `final` 字段和 `volatile` 字段的语义区别需注意

---

## 3. 实验性特性注意事项

### Compact Object Headers (JEP 519)

**状态**: 实验性，默认关闭

**已知限制**:
- 需要显式启用：`-XX:+UnlockExperimentalVMOptions -XX:+UseCompactObjectHeaders`
- 可能影响某些依赖对象头布局的 native 代码
- 与部分序列化框架的兼容性需要验证

```bash
# 启用紧凑对象头
java -XX:+UnlockExperimentalVMOptions -XX:+UseCompactObjectHeaders MyApp

# 验证是否生效
java -XX:+UnlockExperimentalVMOptions -XX:+UseCompactObjectHeaders \
     -XX:+PrintFieldLayout MyApp
```

**不兼容的场景**:
- JNI 代码直接操作对象头
- 使用 `Unsafe.objectFieldOffset()` 的遗留代码
- 部分 APM 工具的字节码注入

### JFR CPU-Time Profiling (JEP 509)

**状态**: 实验性

**已知限制**:
- Linux 平台需要 `perf_event` 支持
- 容器环境中可能需要额外权限：`--privileged` 或 `SYS_ADMIN` capability
- 采样精度受操作系统调度影响

---

## 4. 兼容性问题

### 反射访问限制加强

JDK 25 继续收紧 `--illegal-access` 限制：

```bash
# 如果应用依赖内部 API，需要显式开放
java --add-opens java.base/java.lang=ALL-UNNAMED MyApp
```

**常见受影响的库**:
| 库 | 最低兼容版本 | 说明 |
|----|-------------|------|
| Lombok | 1.18.30+ | 需要更新 |
| Byte Buddy | 1.14.10+ | Agent 模式需要参数 |
| Mockito | 5.8.0+ | 依赖 Byte Buddy |
| Jackson | 2.16.0+ | 反射序列化 |

### ThreadLocal 与虚拟线程

虚拟线程中使用 `ThreadLocal` 不会报错，但存在性能隐患：

```java
// ⚠️ 虚拟线程中应避免
static final ThreadLocal<Connection> conn = new ThreadLocal<>();

// ✅ 推荐使用 Scoped Values (JDK 25 正式版)
static final ScopedValue<Connection> CONN = ScopedValue.newInstance();
```

---

## 5. 平台特定问题

### macOS

- **Apple Silicon**: 完全支持，无已知问题
- **macOS 渲染**: Metal 渲染管线在某些旧版 macOS (< 13) 上可能有兼容问题

### Linux 容器

- **cgroup v2**: 完全支持
- **Alpine Linux / musl libc**: 支持，但 JFR CPU Profiling 功能受限
- **容器内存检测**: 正确识别容器内存限制

```bash
# 验证容器内存检测
java -XshowSettings:system 2>&1 | grep "Memory"
```

### Windows

- **32-bit**: 不再支持 (JEP 503)
- **Windows 11**: 完全支持
- **Windows Server 2022**: 完全支持

---

## 6. 框架兼容性

| 框架 | 最低兼容版本 | 虚拟线程支持 | 说明 |
|------|-------------|-------------|------|
| Spring Boot | 3.2+ | ✅ | 需 3.2+ 获得虚拟线程集成 |
| Quarkus | 3.6+ | ✅ | 原生虚拟线程支持 |
| Micronaut | 4.2+ | ✅ | 支持虚拟线程 |
| Netty | 4.1.100+ | ⚠️ 部分 | Event Loop 仍用平台线程 |
| Tomcat | 10.1.16+ | ✅ | Connector 支持虚拟线程 |
| Hibernate | 6.4+ | ✅ | Session 在虚拟线程中安全 |

---

## 7. 相关链接

- [JDK 25 主页](../index.md)
- [JDK 25 破坏性变更](../breaking-changes.md)
- [JDK 25 性能调优](../performance.md)
- [JDK 25 迁移指南](../migration/from-21.md)
- [Oracle JDK 25 Release Notes](https://www.oracle.com/java/technologies/javase/25-relnote-issues.html)

---

[← 返回 JDK 25](../index.md)
