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
- `rmiregistry` 工具移除

**推荐配置**:
```bash
-XX:+UseZGC             # 使用 ZGC (正式)
-XX:+ZGenerational      # 需要 JDK 21+
```

---

## 4. 关键 JEP（自 JDK 11 以来集成）

### 语言特性

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 394](https://openjdk.org/jeps/394) | Pattern Matching for instanceof | instanceof 模式匹配 | 16 |
| [JEP 395](https://openjdk.org/jeps/395) | Records | 记录类 | 16 |
| [JEP 306](https://openjdk.org/jeps/306) | Restore Always-Strict Floating-Point Semantics | 严格浮点语义 | 17 |
| [JEP 409](https://openjdk.org/jeps/409) | Sealed Classes | 密封类 | 17 |
| [JEP 361](https://openjdk.org/jeps/361) | Switch Expressions | Switch 表达式 | 14 |
| [JEP 378](https://openjdk.org/jeps/378) | Text Blocks | 文本块 | 15 |
| [JEP 406](https://openjdk.org/jeps/406) | Pattern Matching for switch (Preview) | switch 模式匹配（预览） | 17 |

### 核心库

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 356](https://openjdk.org/jeps/356) | Enhanced Pseudo-Random Number Generators | 增强随机数生成器 | 17 |
| [JEP 371](https://openjdk.org/jeps/371) | Hidden Classes | 隐藏类 | 15 |
| [JEP 334](https://openjdk.org/jeps/334) | JVM Constants API | JVM 常量 API | 12 |
| [JEP 415](https://openjdk.org/jeps/415) | Context-Specific Deserialization Filters | 反序列化过滤器 | 17 |

### HotSpot VM

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 341](https://openjdk.org/jeps/341) | Default CDS Archives | 默认 CDS 存档 | 12 |
| [JEP 350](https://openjdk.org/jeps/350) | Dynamic CDS Archives | 动态 CDS 存档 | 13 |
| [JEP 387](https://openjdk.org/jeps/387) | Elastic Metaspace | 弹性元空间 | 16 |
| [JEP 358](https://openjdk.org/jeps/358) | Helpful NullPointerExceptions | Helpful NPE | 14 |
| [JEP 390](https://openjdk.org/jeps/390) | Warnings for Value-Based Classes | 值类警告 | 16 |
| [JEP 403](https://openjdk.org/jeps/403) | Strongly Encapsulate JDK Internals | 强封装 JDK 内部 | 17 |

### 垃圾收集器

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 377](https://openjdk.org/jeps/377) | ZGC: A Scalable Low-Latency Garbage Collector | ZGC 正式版 | 15 |
| [JEP 376](https://openjdk.org/jeps/376) | ZGC: Concurrent Thread-Stack Processing | ZGC 并发栈处理 | 16 |
| [JEP 379](https://openjdk.org/jeps/379) | Shenandoah: A Low-Pause-Time Garbage Collector | Shenandoah 正式版 | 15 |
| [JEP 344](https://openjdk.org/jeps/344) | Abortable Mixed Collections for G1 | G1 可中断 Mixed GC | 12 |
| [JEP 345](https://openjdk.org/jeps/345) | NUMA-Aware Memory Allocation for G1 | G1 NUMA 感知 | 14 |
| [JEP 346](https://openjdk.org/jeps/346) | Promptly Return Unused Committed Memory from G1 | G1 及时归还内存 | 12 |

### 端口支持

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 386](https://openjdk.org/jeps/386) | Alpine Linux Port | Alpine Linux 端口 | 16 |
| [JEP 391](https://openjdk.org/jeps/391) | macOS/AArch64 Port | macOS AArch64 端口 | 17 |
| [JEP 340](https://openjdk.org/jeps/340) | One AArch64 Port, Not Two | 统一 AArch64 端口 | 12 |
| [JEP 388](https://openjdk.org/jeps/388) | Windows/AArch64 Port | Windows AArch64 端口 | 16 |

### I/O 和网络

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 353](https://openjdk.org/jeps/353) | Reimplement the Legacy Socket API | 重新实现 Socket API | 13 |
| [JEP 373](https://openjdk.org/jeps/373) | Reimplement the Legacy DatagramSocket API | 重新实现 DatagramSocket API | 15 |
| [JEP 380](https://openjdk.org/jeps/380) | Unix-Domain Socket Channels | Unix 域套接字 | 16 |
| [JEP 352](https://openjdk.org/jeps/352) | Non-Volatile Mapped Byte Buffers | 非易失性映射字节缓冲区 | 14 |

### 图形和加密

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 382](https://openjdk.org/jeps/382) | New macOS Rendering Pipeline | 新 macOS 渲染管线 | 17 |
| [JEP 339](https://openjdk.org/jeps/339) | Edwards-Curve Digital Signature Algorithm (EdDSA) | EdDSA 签名算法 | 15 |

### 工具

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 392](https://openjdk.org/jeps/392) | Packaging Tool | 打包工具 | 16 |

### 监控

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 349](https://openjdk.org/jeps/349) | JFR Event Streaming | JFR 事件流 | 14 |

### 预览和孵化

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 406](https://openjdk.org/jeps/406) | Pattern Matching for switch (Preview) | switch 模式匹配（预览） | 17 |
| [JEP 412](https://openjdk.org/jeps/412) | Foreign Function & Memory API (Incubator) | FFM API（孵化器） | 17 |
| [JEP 414](https://openjdk.org/jeps/414) | Vector API (Second Incubator) | Vector API（第2次孵化） | 17 |

### 废弃

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 398](https://openjdk.org/jeps/398) | Deprecate the Applet API for Removal | 废弃 Applet API | 17 |
| [JEP 411](https://openjdk.org/jeps/411) | Deprecate the Security Manager for Removal | 废弃 Security Manager | 17 |
| [JEP 374](https://openjdk.org/jeps/374) | Deprecate and Disable Biased Locking | 废弃偏向锁 | 15 |
| [JEP 366](https://openjdk.org/jeps/366) | Deprecate the ParallelScavenge + SerialOld GC Combination | 废弃 PS+SerialOld | 14 |

### 移除

| JEP | 标题 | 说明 | 版本 |
|-----|------|------|------|
| [JEP 410](https://openjdk.org/jeps/410) | Remove the Experimental AOT and JIT Compiler | 移除实验性 AOT/JIT | 17 |
| [JEP 407](https://openjdk.org/jeps/407) | Remove RMI Activation | 移除 RMI Activation | 17 |
| [JEP 381](https://openjdk.org/jeps/381) | Remove the Solaris and SPARC Ports | 移除 Solaris/SPARC | 15 |
| [JEP 372](https://openjdk.org/jeps/372) | Remove the Nashorn JavaScript Engine | 移除 Nashorn | 15 |
| [JEP 367](https://openjdk.org/jeps/367) | Remove the Pack200 Tools and API | 移除 Pack200 | 14 |
| [JEP 363](https://openjdk.org/jeps/363) | Remove the Concurrent Mark Sweep (CMS) Garbage Collector | 移除 CMS GC | 14 |

---

## 5. 相关链接

- [JDK 17 发布说明](https://openjdk.org/projects/jdk/17/)
- [JDK 17 新特性](https://openjdk.org/projects/jdk/17/features)
- [Sealed Classes 指南](https://openjdk.org/jeps/409)
