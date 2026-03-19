# Issue 分析文档

> 本目录包含 JDK 重要 issue 的详细分析

---

## 概述

JDK 26 包含 4,913 个 commit，对应数千个 issue。本目录选取最重要的 issue 进行深入分析。

---

## 分类索引

### 🔴 严重 Bug 修复

| Issue | 标题 | 影响 | 分析 |
|-------|------|------|------|
| [JDK-8326498](jdk-8326498.md) | HttpClient HTTP/2 连接泄漏 | 连接池耗尽 | [详细分析](jdk-8326498.md) |
| [JDK-8354894](jdk-8354894.md) | Virtual Thread Starvation | 高 CPU 服务器超时 | [详细分析](jdk-8354894.md) |

### 🟡 性能优化

| Issue | 标题 | 提升 | 分析 |
|-------|------|------|------|
| [JDK-8371259](jdk-8371259.md) | ML-DSA Intrinsics | 后量子密码 2-5x | [详细分析](jdk-8371259.md) |
| [JDK-8355177](jdk-8355177.md) | StringBuilder.append 优化 | +15% | [详细分析](jdk-8355177.md) |
| [JDK-8371475](jdk-8371475.md) | CUBIC 拥塞控制 | HTTP/3 性能 | [详细分析](jdk-8371475.md) |

### 🟢 功能增强

| Issue | 标题 | 功能 | 分析 |
|-------|------|------|------|
| [JDK-8371701](jdk-8371701.md) | NUMA 线程亲和性 | 多插槽优化 | [详细分析](jdk-8371701.md) |
| [JDK-8359683](jdk-8359683.md) | ZGC NUMA-Aware | 大内存优化 | [详细分析](jdk-8359683.md) |
| [JDK-8372159](jdk-8372159.md) | HttpClient 虚拟线程 | 内存优化 | [详细分析](jdk-8372159.md) |

---

## Issue 分析模板

每个 issue 分析文档包含以下部分：

1. **概述**: Issue 基本信息
2. **问题描述**: 问题背景和影响
3. **根因分析**: 问题根本原因
4. **解决方案**: 修复方案详解
5. **代码变更**: 关键代码变更
6. **测试验证**: 测试用例和验证方法
7. **影响评估**: 对用户的影响

---

## 按组件分类

### java.net.http

- [JDK-8326498](jdk-8326498.md) - HTTP/2 连接泄漏
- [JDK-8371475](jdk-8371475.md) - CUBIC 拥塞控制
- [JDK-8372159](jdk-8372159.md) - 虚拟线程优化

### hotspot/gc

- [JDK-8359683](jdk-8359683.md) - ZGC NUMA-Aware

### hotspot/runtime

- [JDK-8371701](jdk-8371701.md) - NUMA 线程亲和性

### java.lang

- [JDK-8355177](jdk-8355177.md) - StringBuilder 优化

### security

- [JDK-8371259](jdk-8371259.md) - ML-DSA Intrinsics

---

## 相关链接

- [OpenJDK Bug System (JBS)](https://bugs.openjdk.org/)
- [JDK 26 Issue 列表](https://bugs.openjdk.org/issues/?jql=project%20%3D%20JDK%20AND%20fixVersion%20%3D%2026)