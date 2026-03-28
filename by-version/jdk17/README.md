# JDK 17

> **状态**: LTS (长期支持) | **GA 发布**: 2021-09-14 | **类型**: Long Term Support

[![OpenJDK](https://img.shields.io/badge/OpenJDK-17-orange)](https://openjdk.org/projects/jdk/17/)
[![LTS](https://img.shields.io/badge/LTS-2029--purple.svg)](https://www.oracle.com/java/technologies/java-se-support.html)

---
## 目录

1. [版本概览](#1-版本概览)
2. [GC 状态](#2-gc-状态)
3. [迁移指南](#3-迁移指南)
4. [关键 JEP（自 JDK 11 以来集成）](#4-关键-jep自-jdk-11-以来集成)
5. [相关链接](#5-相关链接)

---


## 1. 版本概览

JDK 17 是继 JDK 11 之后的 LTS 版本，包含多项重要新特性：

| 特性 | 状态 | 说明 |
|------|------|------|
| **Sealed Classes** | 正式 (JEP 409) | 密封类 |
| **Records** | 正式 (JEP 395) | 记录类 |
| **Text Blocks** | 正式 (JEP 378) | 文本块 |
| **Pattern Matching for instanceof** | 正式 (JEP 394，JDK 16) | instanceof 模式匹配 |
| **Pattern Matching for switch** | 预览 (JEP 406) | switch 模式匹配 |
| **Foreign Function & Memory API** | 孵化 (JEP 412) | Java 原生互连 |
| **Vector API** | 孵化 (JEP 414，第2次) | 向量 API |
| **Context-Specific Deserialization Filters** | 正式 (JEP 415) | 反序列化过滤 |

---

## 2. GC 状态

| GC | 状态 | 说明 |
|----|------|------|
| **G1 GC** | 默认 | 持续优化 |
| **ZGC** | 正式 (JEP 377) | 低延迟 GC，JDK 15 正式 |
| **Shenandoah** | 正式 (JEP 379) | 低延迟 GC |

---

## 3. 迁移指南

### 从 JDK 11 升级

**重要变更**:
- **Sealed Classes 正式版**：限制继承的类
- **Records 正式版**：不可变数据类
- **Text Blocks 正式版**：多行字符串
- **强封装**：JDK 内部 API 默认不可访问
- `Security Manager` 部分功能弃用
- `rmid` 工具移除（JEP 407，RMI Activation）

**推荐配置**:
```bash
-XX:+UseZGC             # 使用 ZGC (正式)
```

---

## 4. 关键 JEP（自 JDK 11 以来集成）

### 语言特性

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 394](/jeps/language/jep-394.md) | Pattern Matching for instanceof | instanceof 模式匹配 | 16 |
| [JEP 395](/jeps/language/jep-395.md) | Records | 记录类 | 16 |
| [JEP 306](/jeps/language/jep-306.md) | Restore Always-Strict Floating-Point Semantics | 严格浮点语义 | 17 |
| [JEP 409](/jeps/language/jep-409.md) | Sealed Classes | 密封类 | 17 |
| [JEP 361](/jeps/language/jep-361.md) | Switch Expressions | Switch 表达式 | 14 |
| [JEP 378](/jeps/language/jep-378.md) | Text Blocks | 文本块 | 15 |
| [JEP 406](/jeps/language/jep-406.md) | Pattern Matching for switch (Preview) | switch 模式匹配（预览） | 17 |

### 核心库

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 356](/jeps/math/jep-356.md) | Enhanced Pseudo-Random Number Generators | 增强随机数生成器 | 17 |
| [JEP 371](/jeps/language/jep-371.md) | Hidden Classes | 隐藏类 | 15 |
| [JEP 334](/jeps/language/jep-334.md) | JVM Constants API | JVM 常量 API | 12 |
| [JEP 415](/jeps/security/jep-415.md) | Context-Specific Deserialization Filters | 反序列化过滤器 | 17 |

### HotSpot VM

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 341](/jeps/performance/jep-341.md) | Default CDS Archives | 默认 CDS 存档 | 12 |
| [JEP 350](/jeps/performance/jep-350.md) | Dynamic CDS Archives | 动态 CDS 存档 | 13 |
| [JEP 387](/jeps/performance/jep-387.md) | Elastic Metaspace | 弹性元空间 | 16 |
| [JEP 358](/jeps/platform/jep-358.md) | Helpful NullPointerExceptions | Helpful NPE | 14 |
| [JEP 390](/jeps/language/jep-390.md) | Warnings for Value-Based Classes | 值类警告 | 16 |
| [JEP 403](/jeps/language/jep-403.md) | Strongly Encapsulate JDK Internals | 强封装 JDK 内部 | 17 |

### 垃圾收集器

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 377](/jeps/gc/jep-377.md) | ZGC: A Scalable Low-Latency Garbage Collector | ZGC 正式版 | 15 |
| [JEP 376](https://openjdk.org/jeps/376) | ZGC: Concurrent Thread-Stack Processing | ZGC 并发栈处理 | 16 |
| [JEP 379](/jeps/gc/jep-379.md) | Shenandoah: A Low-Pause-Time Garbage Collector | Shenandoah 正式版 | 15 |
| [JEP 344](/jeps/gc/jep-344.md) | Abortable Mixed Collections for G1 | G1 可中断 Mixed GC | 12 |
| [JEP 345](/jeps/gc/jep-345.md) | NUMA-Aware Memory Allocation for G1 | G1 NUMA 感知 | 14 |
| [JEP 346](/jeps/gc/jep-346.md) | Promptly Return Unused Committed Memory from G1 | G1 及时归还内存 | 12 |

### 端口支持

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 386](/jeps/platform/jep-386.md) | Alpine Linux Port | Alpine Linux 端口 | 16 |
| [JEP 391](/jeps/platform/jep-391.md) | macOS/AArch64 Port | macOS AArch64 端口 | 17 |
| [JEP 340](/jeps/platform/jep-340.md) | One AArch64 Port, Not Two | 统一 AArch64 端口 | 12 |
| [JEP 388](/jeps/platform/jep-388.md) | Windows/AArch64 Port | Windows AArch64 端口 | 16 |

### I/O 和网络

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 353](/jeps/api/jep-353.md) | Reimplement the Legacy Socket API | 重新实现 Socket API | 13 |
| [JEP 373](/jeps/concurrency/jep-373.md) | Reimplement the Legacy DatagramSocket API | 重新实现 DatagramSocket API | 15 |
| [JEP 380](/jeps/network/jep-380.md) | Unix-Domain Socket Channels | Unix 域套接字 | 16 |
| [JEP 352](https://openjdk.org/jeps/352) | Non-Volatile Mapped Byte Buffers | 非易失性映射字节缓冲区 | 14 |

### 图形和加密

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 382](/jeps/client/jep-382.md) | New macOS Rendering Pipeline | 新 macOS 渲染管线 | 17 |
| [JEP 339](https://openjdk.org/jeps/339) | Edwards-Curve Digital Signature Algorithm (EdDSA) | EdDSA 签名算法 | 15 |

### 工具

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 392](/jeps/tools/jep-392.md) | Packaging Tool | 打包工具 | 16 |

### 监控

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 349](https://openjdk.org/jeps/349) | JFR Event Streaming | JFR 事件流 | 14 |

### 预览和孵化

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 406](/jeps/language/jep-406.md) | Pattern Matching for switch (Preview) | switch 模式匹配（预览） | 17 |
| [JEP 412](/jeps/ffi/jep-412.md) | Foreign Function & Memory API (Incubator) | FFM API（孵化器） | 17 |
| [JEP 414](/jeps/tools/jep-414.md) | Vector API (Second Incubator) | Vector API（第2次孵化） | 17 |

### 废弃

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 398](/jeps/tools/jep-398.md) | Deprecate the Applet API for Removal | 废弃 Applet API | 17 |
| [JEP 411](/jeps/security/jep-411.md) | Deprecate the Security Manager for Removal | 废弃 Security Manager | 17 |
| [JEP 374](/jeps/performance/jep-374.md) | Deprecate and Disable Biased Locking | 废弃偏向锁 | 15 |
| [JEP 366](https://openjdk.org/jeps/366) | Deprecate the ParallelScavenge + SerialOld GC Combination | 废弃 PS+SerialOld | 14 |

### 移除

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 410](/jeps/tools/jep-410.md) | Remove the Experimental AOT and JIT Compiler | 移除实验性 AOT/JIT | 17 |
| [JEP 407](/jeps/tools/jep-407.md) | Remove RMI Activation | 移除 RMI Activation | 17 |
| [JEP 381](/jeps/platform/jep-381.md) | Remove the Solaris and SPARC Ports | 移除 Solaris/SPARC | 15 |
| [JEP 372](/jeps/tools/jep-372.md) | Remove the Nashorn JavaScript Engine | 移除 Nashorn | 15 |
| [JEP 367](https://openjdk.org/jeps/367) | Remove the Pack200 Tools and API | 移除 Pack200 | 14 |
| [JEP 363](/jeps/gc/jep-363.md) | Remove the Concurrent Mark Sweep (CMS) Garbage Collector | 移除 CMS GC | 14 |

---

## 5. 按主题深入

| 主题 | JDK 17 引入/改进 | 链接 |
|------|------------------|------|
| **Record 类型** | Record 正式版 (JEP 395) | [→](/by-topic/core/records/) |
| **模式匹配** | instanceof 模式匹配 (JEP 394)、switch 预览 (JEP 406) | [→](/by-topic/core/patterns/) |
| **GC 演进** | ZGC/Shenandoah 正式版 | [→](/by-topic/core/gc/) |
| **安全特性** | Security Manager 废弃 (JEP 411) | [→](/by-topic/security/security/) |
| **内存管理** | 弹性 Metaspace (JEP 387) | [→](/by-topic/core/memory/) |
| **JIT 编译** | 移除实验性 AOT/JIT (JEP 410) | [→](/by-topic/core/jit/) |

---

## 6. 相关链接

- [JDK 17 发布说明](https://openjdk.org/projects/jdk/17/)
- [JDK 17 新特性](https://openjdk.org/projects/jdk/17/features)
- [Sealed Classes 指南](https://openjdk.org/jeps/409)

### 相关主题

| 主题 | 链接 |
|------|------|
| Records | [Records 主题](/by-topic/core/records/) |
| Sealed Classes | [Sealed Classes](/by-topic/language/syntax/) |
| Pattern Matching | [模式匹配](/by-topic/core/patterns/) |
| GC 演进 | [GC 时间线](/by-topic/core/gc/) |
| ZGC/Shenandoah | [GC 详解](/jeps/gc/jep-377.md) |
| 安全特性 | [安全主题](/by-topic/security/security/) |
| Foreign Function | [FFM API](/by-topic/core/panama/) |
| 内存管理 | [内存主题](/by-topic/core/memory/) |
| JIT 编译 | [JIT 主题](/by-topic/core/jit/) |

### 实战案例

| 案例 | 关键词 | 链接 |
|------|-------|------|
| GC 调优实战 | G1→ZGC | [→](/cases/gc-tuning-case.md) |
| Full GC 抖动 | G1 Full GC | [→](/cases/gc-fullgc-jitter.md) |
| ZGC 调优 | Gen ZGC | [→](/cases/zgc-tuning.md) |
| 死锁诊断 | synchronized/ReentrantLock | [→](/cases/deadlock-diagnosis.md) |
| JIT 编译回退 | C2 编译 | [→](/cases/jit-compilation-fallback.md) |
| Metaspace OOM | 类加载泄漏 | [→](/cases/metaspace-oom.md) |

### 迁移指南

| 来源 | 链接 |
|------|------|
| 从 JDK 11 迁移 | [→](migration/from-11.md) |
| 迁移到 JDK 21 | [→](migration/to-21.md) |

### 相关 JEP 深度分析

| JEP | 链接 |
|-----|------|
| JEP 395: Records | [→](/jeps/language/jep-395.md) |
| JEP 409: Sealed Classes | [→](/jeps/language/jep-409.md) |
| JEP 394: Pattern Matching instanceof | [→](/jeps/language/jep-394.md) |
| JEP 377: ZGC Production | [→](/jeps/gc/jep-377.md) |
| JEP 387: Elastic Metaspace | [→](/jeps/performance/jep-387.md) |
| JEP 412: FFM API (Incubator) | [→](/jeps/ffi/jep-412.md) |
| JEP 378: Text Blocks | [→](/jeps/language/jep-378.md) |
