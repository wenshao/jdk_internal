# Linux 平台时间线

JDK 在 Linux 平台上的演进历史。

[← 返回 Linux 平台](./)

---
## 目录

1. [JDK 1.0 - 1.4: 基础支持](#1-jdk-10---14-基础支持)
2. [JDK 5-6: 性能改进](#2-jdk-5-6-性能改进)
3. [JDK 7-8: 现代 Linux 支持](#3-jdk-7-8-现代-linux-支持)
4. [JDK 10: 容器感知](#4-jdk-10-容器感知)
5. [JDK 14-17: cgroup v2 支持](#5-jdk-14-17-cgroup-v2-支持)
6. [JDK 17: AArch64 成熟](#6-jdk-17-aarch64-成熟)
7. [JDK 21: io_uring 支持](#7-jdk-21-io_uring-支持)
8. [架构支持时间线](#8-架构支持时间线)
9. [发行版支持](#9-发行版支持)
10. [核心贡献者](#10-核心贡献者)
11. [参考资料](#11-参考资料)

---


## 1. JDK 1.0 - 1.4: 基础支持

### JDK 1.0 (1996)
- Linux 作为支持的平台之一
- 基于 Sun JDK 1.0
- 需要手工编译

### JDK 1.2 (1998)
- JIT 编译器引入
- 性能显著提升

### JDK 1.3 - 1.4
- HotSpot VM 成为默认
- NIO 引入 (epoll 支持)

---

## 2. JDK 5-6: 性能改进

### JDK 5 (2004)
- 分层编译
- JMX 监控

### JDK 6 (2006)
- 性能工具: jstat, jmap, jstack
- 动态编译优化

---

## 3. JDK 7-8: 现代 Linux 支持

### JDK 7 (2011)
- NIO.2 (异步 I/O)
- G1 GC 引入

### JDK 8 (2014)
- Lambda 表达式
- Stream API
- 永久代移除

---

## 4. JDK 10: 容器感知

### JEP 307: 容器感知 (2018)

| 版本 | 日期 | 变化 |
|------|------|------|
| JDK 10 | 2018-03 | 首次容器感知支持 |
| JDK 11 | 2018-09 | 改进容器检测 |
| JDK 14 | 2020-03 | cgroup v2 初步支持 |
| JDK 17 | 2021-09 | cgroup v2 改进 |
| JDK 21 | 2023-09 | cgroup v2 完整支持 |
| JDK 26 | 2025 | 容器优化增强 |

**关键参数**:
```bash
-XX:+UseContainerSupport  # JDK 10+
-XX:ActiveProcessorCount=auto
-XX:MaxRAMPercentage=75.0
```

---

## 5. JDK 14-17: cgroup v2 支持

### cgroup v2 时间线

```
2016 ─── Linux 内核 4.5: cgroup v2 合并
   │
2018 ─── RHEL 8: 默认使用 cgroup v2
   │
2020 ─── Ubuntu 21.04: 默认使用 cgroup v2
   │
2020 ─── JDK 14: cgroup v2 初步支持
   │
2021 ─── JDK 17: cgroup v2 改进
   │
2023 ─── JDK 21: cgroup v2 完整支持
```

### 支持对比

| 特性 | cgroup v1 | cgroup v2 |
|------|-----------|-----------|
| **JDK 支持** | JDK 8+ | JDK 21+ 完整 |
| **内存检测** | ✅ | ✅ |
| **CPU 检测** | ✅ | ✅ |
| **IO 检测** | ❌ | ✅ (JDK 26+) |

---

## 6. JDK 17: AArch64 成熟

### AArch64 支持

| 版本 | 日期 | 状态 |
|------|------|------|
| JDK 9 | 2017 | AArch64 引入 |
| JDK 16 | 2021 | AArch64 成熟 |
| JDK 17 | 2021 | AArch64 生产就绪 |

### ARM 服务器支持

- AWS Graviton
- AWS Graviton2
- Azure ARM 系列
- 阿里云 Yitian 710

---

## 7. JDK 21: io_uring 支持

### JEP Draft: io_uring (2023)

**io_uring 时间线**:
```
2019 ─── Linux 内核 5.1: io_uring 引入
   │
2020 ─── Linux 内核 5.7: 稳定 API
   │
2023 ─── JDK 21: io_uring 实验性支持
   │
2025 ─── JDK 26+: io_uring 正式支持
```

**启用 io_uring**:
```bash
-Djdk.io.useIOUring=true
```

---

## 8. 架构支持时间线

```
JDK 1.0 ─── x86 (32位)
   │
JDK 5  ─── x86_64 (64位)
   │
JDK 9  ─── AArch64 (ARM64)
   │       ├── ppc64le (PowerPC)
   │       └── s390x (IBM z)
   │
JDK 19 ─── RISC-V (实验性)
   │
JDK 21 ─── LoongArch (龙芯)
```

---

## 9. 发行版支持

### RHEL/CentOS

| 版本 | 支持 | EOL |
|------|------|-----|
| RHEL 7 | ✅ | 2024-06 |
| RHEL 8 | ✅ | 2029-05 |
| RHEL 9 | ✅ | 2032-05 |

### Ubuntu

| 版本 | 支持 | EOL |
|------|------|-----|
| 18.04 LTS | ✅ | 2028-04 |
| 20.04 LTS | ✅ | 2030-04 |
| 22.04 LTS | ✅ | 2032-04 |
| 24.04 LTS | ✅ | 2034-04 |

### Debian

| 版本 | 支持 | EOL |
|------|------|-----|
| Debian 10 | ✅ | 2024-06 |
| Debian 11 | ✅ | 2026 |
| Debian 12 | ✅ | 2028 |

---

## 10. 核心贡献者

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| [Ioi Lam](/by-contributor/profiles/ioi-lam.md) | Oracle | CDS, 容器支持 |
| [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | Oracle | 类加载 |
| [David Holmes](/by-contributor/profiles/david-holmes.md) | Oracle | 并发, 线程 |

---

## 11. 参考资料

- [JEP 307: Container Awareness](https://openjdk.org/jeps/307)
- [JEP 358: Apple Silicon Support](https://openjdk.org/jeps/358)
- [Linux cgroup v2 文档](https://docs.kernel.org/admin-guide/cgroup-v2.html)

→ [返回 Linux 平台](./)
