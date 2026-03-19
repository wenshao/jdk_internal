# JDK 26 发布说明

> 基于 openjdk/jdk 仓库标签 `jdk-26+26` 分析

## 概述

JDK 26 包含 **23 个 JEP**（JDK Enhancement Proposals），涵盖语言特性、API、性能优化、垃圾回收等多个领域。

## JEP 列表

### 语言特性

| JEP | 标题 | 状态 |
|-----|------|------|
| [JEP 511](https://openjdk.org/jeps/511) | Module Import Declarations | 新增 |
| [JEP 512](https://openjdk.org/jeps/512) | Compact Source Files and Instance Main Methods | 新增 |
| [JEP 530](https://openjdk.org/jeps/530) | Primitive Types in Patterns, instanceof, and switch (Fourth Preview) | 预览 |
| [JEP 526](https://openjdk.org/jeps/526) | Lazy Constants (Second Preview) | 预览 |

### 核心库

| JEP | 标题 | 状态 |
|-----|------|------|
| [JEP 502](https://openjdk.org/jeps/502) | Stable Values (Preview) | 预览 |
| [JEP 506](https://openjdk.org/jeps/506) | Scoped Values | 正式 |
| [JEP 510](https://openjdk.org/jeps/510) | Key Derivation Function API | 新增 |

### 并发与多线程

| JEP | 标题 | 状态 |
|-----|------|------|
| [JEP 505](https://openjdk.org/jeps/505) | Structured Concurrency (Fifth Preview) | 预览 |
| [JEP 525](https://openjdk.org/jeps/525) | Structured Concurrency (Sixth Preview) | 预览 |

### 性能与监控

| JEP | 标题 | 状态 |
|-----|------|------|
| [JEP 509](https://openjdk.org/jeps/509) | JFR CPU-Time Profiling | 新增 |
| [JEP 514](https://openjdk.org/jeps/514) | Ahead-of-Time Command Line Ergonomics | 新增 |
| [JEP 515](https://openjdk.org/jeps/515) | Ahead-of-Time Method Profiling | 新增 |
| [JEP 518](https://openjdk.org/jeps/518) | JFR Cooperative Sampling | 新增 |
| [JEP 519](https://openjdk.org/jeps/519) | Compact Object Headers | 新增 |
| [JEP 520](https://openjdk.org/jeps/520) | JFR Method Timing and Tracing | 新增 |

### 垃圾回收

| JEP | 标题 | 状态 |
|-----|------|------|
| [JEP 521](https://openjdk.org/jeps/521) | Generational Shenandoah | 新增 |
| [JEP 522](https://openjdk.org/jeps/522) | G1 GC: Improve Throughput by Reducing Synchronization | 新增 |

### 网络

| JEP | 标题 | 状态 |
|-----|------|------|
| [JEP 517](https://openjdk.org/jeps/517) | HTTP/3 for the HTTP Client API | 新增 |

### 安全

| JEP | 标题 | 状态 |
|-----|------|------|
| [JEP 470](https://openjdk.org/jeps/470) | PEM Encodings of Cryptographic Objects (Preview) | 预览 |
| [JEP 524](https://openjdk.org/jeps/524) | PEM Encodings of Cryptographic Objects (Second Preview) | 预览 |

### 移除与清理

| JEP | 标题 | 状态 |
|-----|------|------|
| [JEP 500](https://openjdk.org/jeps/500) | Prepare to Make Final Mean Final | 新增 |
| [JEP 503](https://openjdk.org/jeps/503) | Remove the 32-bit x86 Port | 移除 |
| [JEP 504](https://openjdk.org/jeps/504) | Remove the Applet API | 移除 |

## 亮点特性

### 1. 模块导入声明 (JEP 511)
简化模块化开发，允许直接导入整个模块。

### 2. 紧凑源文件 (JEP 512)
进一步简化 Java 入门体验，无需显式类声明。

### 3. HTTP/3 支持 (JEP 517)
HTTP Client API 正式支持 HTTP/3 协议。

### 4. 分代 Shenandoah (JEP 521)
Shenandoah GC 支持分代模式，提升性能。

### 5. 紧凑对象头 (JEP 519)
减少对象内存占用，提升内存效率。

### 6. 移除 32位 x86 端口 (JEP 503)
正式移除 32位 x86 平台支持。

## 相关链接

- [OpenJDK JDK 26 项目页面](https://openjdk.org/projects/jdk/26/)
- [JDK 26 JEP 列表](https://openjdk.org/projects/jdk/26/spec/)