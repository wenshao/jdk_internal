# JDK 11

> **状态**: LTS (长期支持) | **GA 发布**: 2018-09-25 | **类型**: Long Term Support

[![OpenJDK](https://img.shields.io/badge/OpenJDK-11-orange)](https://openjdk.org/projects/jdk/11/)
[![LTS](https://img.shields.io/badge/LTS-2028--purple.svg)](https://www.oracle.com/java/technologies/java-se-support.html)

---
## 目录

1. [版本概览](#1-版本概览)
2. [GC 状态](#2-gc-状态)
3. [迁移指南](#3-迁移指南)
4. [关键 JEP](#4-关键-jep)
5. [相关链接](#5-相关链接)

---


## 1. 版本概览

JDK 11 是继 JDK 8 之后的首个 LTS 版本，包含多项重要改进：

| 特性 | 说明 |
|------|------|
| **HTTP Client（正式版）** | JEP 321，新的 HTTP 客户端 API |
| **Flight Recorder（正式版）** | JEP 328，生产环境性能分析 |
| **ZGC（实验）** | JEP 333，低延迟 GC |
| **Nest-Based Access Control** | JEP 181，简化私有访问 |
| **Lambda 局部变量类型推断** | JEP 323，Lambda 参数可用 var (JEP 323) |
| **Epsilon GC** | JEP 318，被动 GC |
| **动态类文件常量** | [JEP 309](/jeps/language/jep-309.md) |
| **单文件源程序启动** | [JEP 330](/jeps/tools/jep-330.md) |
| **TLS 1.3** | [JEP 332](/jeps/security/jep-332.md) |
| **ChaCha20/Poly1305** | JEP 329，加密算法 |
| **Curve25519/Curve448** | JEP 324，密钥交换 |
| **Unicode 10** | JEP 327 |
| **低开销堆分析** | JEP 331 |
| **AArch64 内联优化** | JEP 315 |

---

## 2. GC 状态

| GC | 状态 | 说明 |
|----|------|------|
| **G1 GC** | 默认 | 均衡性能和延迟 |
| **ZGC** | 实验 (JEP 333) | Linux，低延迟 |
| **Shenandoah** | 实验 (非 mainline OpenJDK，JDK 12 起通过 JEP 189 进入主线) | 低延迟 GC |
| **Epsilon GC** | 实验 (JEP 318) | 被动 GC |

---

## 3. 迁移指南

### 从 JDK 8 升级

**重要变更**:
- **HTTP Client 正式版**：HttpURLConnection 的现代替代方案
- **Flight Recorder 正式版**：生产环境性能分析
- **var 关键字支持 Lambda**：局部变量类型推断扩展
- `JavaFX` 从 JDK 中分离
- `Pack200` 工具废弃（JEP 336，JDK 14 移除）

**推荐配置**:
```bash
# 方案一：G1 GC（默认）
-XX:+UseG1GC           # G1 仍然是默认
-XX:MaxGCPauseMillis=200  # 目标暂停时间

# 方案二：ZGC（实验，二选一，不可与 G1 同时使用）
-XX:+UnlockExperimentalVMOptions
-XX:+UseZGC            # 尝试 ZGC (实验)
```

---

## 4. 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 181](https://openjdk.org/jeps/181) | Nest-Based Access Control | 基于嵌套的访问控制 |
| [JEP 309](/jeps/language/jep-309.md) | Dynamic Class-File Constants | 动态类文件常量 |
| [JEP 315](https://openjdk.org/jeps/315) | Improve Aarch64 Intrinsics | 改进 AArch64 内联 |
| [JEP 318](/jeps/gc/jep-318.md) | Epsilon: A No-Op Garbage Collector | Epsilon GC |
| [JEP 320](/jeps/language/jep-320.md) | Remove the Java EE and CORBA Modules | 移除 Java EE 和 CORBA |
| [JEP 321](/jeps/network/jep-321.md) | HTTP Client (Standard) | HTTP 客户端 |
| [JEP 323](/jeps/language/jep-323.md) | Local-Variable Syntax for Lambda Parameters | Lambda var 语法 |
| [JEP 324](https://openjdk.org/jeps/324) | Key Agreement with Curve25519 and Curve448 | Curve25519/Curve448 |
| [JEP 327](https://openjdk.org/jeps/327) | Unicode 10 | Unicode 10 |
| [JEP 328](/jeps/jfr/jep-328.md) | Flight Recorder | 飞行记录器 |
| [JEP 329](/jeps/security/jep-329.md) | ChaCha20 and Poly1305 Cryptographic Algorithms | ChaCha20/Poly1305 |
| [JEP 330](/jeps/tools/jep-330.md) | Launch Single-File Source-Code Programs | 单文件程序 |
| [JEP 331](https://openjdk.org/jeps/331) | Low-Overhead Heap Profiling | 低开销堆分析 |
| [JEP 332](/jeps/security/jep-332.md) | Transport Layer Security (TLS) 1.3 | TLS 1.3 |
| [JEP 333](/jeps/gc/jep-333.md) | ZGC: A Scalable Low-Latency Garbage Collector | ZGC |
| [JEP 335](https://openjdk.org/jeps/335) | Deprecate the Nashorn JavaScript Engine | 废弃 Nashorn |
| [JEP 336](https://openjdk.org/jeps/336) | Deprecate the Pack200 Tools and API | 废弃 Pack200 |

---

## 5. 按主题深入

| 主题 | JDK 11 引入/改进 | 链接 |
|------|------------------|------|
| **HTTP 客户端** | HttpClient 正式版 (JEP 321) | [→](/by-topic/concurrency/http/) |
| **GC 演进** | ZGC 实验版、Epsilon GC | [→](/by-topic/core/gc/) |
| **安全特性** | TLS 1.3 (JEP 332) | [→](/by-topic/security/security/) |
| **字符串处理** | String.strip()、isBlank()、repeat() | [→](/by-topic/language/string/) |
| **模块系统** | JPMS 成熟 | [→](/by-topic/core/modules/) |

---

## 6. 相关链接

- [JDK 11 发布说明](https://openjdk.org/projects/jdk/11/)
- [从 JDK 8 迁移](https://docs.oracle.com/en/java/javase/11/migrate/)
- [ZGC 文档](https://openjdk.org/jeps/333)
