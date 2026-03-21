# Michael McMahon

> **Inside.java**: [MichaelMcMahon](https://inside.java/u/MichaelMcMahon/)
> **OpenJDK**: [@mmcmahon](https://openjdk.org/census#mmcmahon)
> **Organization**: Oracle
> **Role**: OpenJDK Networking Group Lead, Core Libraries Networking Team

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [职业历程](#3-职业历程)
4. [主要 JEP 贡献](#4-主要-jep-贡献)
5. [核心技术贡献](#5-核心技术贡献)
6. [技术演讲与媒体](#6-技术演讲与媒体)
7. [技术专长](#7-技术专长)
8. [协作网络](#8-协作网络)
9. [相关链接](#9-相关链接)

---


## 1. 概述

Michael McMahon 是 Oracle Java Platform Group Core Libraries 团队的工程师，同时也是 **OpenJDK Networking Group 的负责人**。他主导了 Java 平台多项关键网络功能的开发，包括 **JEP 110/321 (HTTP Client API)**、**JEP 380 (Unix-Domain Socket Channels)** 以及 **JEP 517 (HTTP/3)** 的协作推进。他是 Java 现代网络栈从 HTTP/1.1 到 HTTP/3 演进的核心推动者，负责将传统的 `HttpURLConnection` 替换为现代化的 `java.net.http` API。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Michael McMahon |
| **当前组织** | Oracle Corporation |
| **职位** | Engineer, Core Libraries Team, Java Platform Group |
| **OpenJDK** | [@mmcmahon](https://openjdk.org/census#mmcmahon) |
| **角色** | OpenJDK Networking Group Lead, JDK Reviewer |
| **Inside.java** | [MichaelMcMahon](https://inside.java/u/MichaelMcMahon/) |
| **主要领域** | HTTP Client API, Unix Domain Sockets, HTTP/3, Java Networking |
| **主导 JEP** | JEP 110, JEP 321, JEP 380 |

> **数据来源**: [Inside.java](https://inside.java/u/MichaelMcMahon/), [OpenJDK Census](https://openjdk.org/census), [JEP 110](https://openjdk.org/jeps/110), [JEP 380](https://openjdk.org/jeps/380)

---

## 3. 职业历程

| 时间 | 事件 | 详情 |
|------|------|------|
| **早期** | 加入 Oracle Java Platform Group | Core Libraries Networking 团队 |
| **2011** | JEP 110 创建 | 提出新的 HTTP Client API 以替代 HttpURLConnection |
| **JDK 9 (2017)** | HTTP/2 Client 孵化 | JEP 110: HTTP/2 Client 作为孵化模块交付 |
| **JDK 10 (2018)** | HTTP Client 更新 | 孵化 API 持续改进 |
| **JDK 11 (2018)** | HTTP Client 标准化 | JEP 321: HTTP Client API 正式成为标准 API |
| **JDK 16 (2021)** | Unix Domain Sockets | JEP 380: Unix-Domain Socket Channels 交付 |
| **2021-04** | Inside.java Podcast | Episode 16: 与 Daniel Fuchs 讨论 JDK 网络功能 |
| **JDK 26 (2025-2026)** | HTTP/3 协作 | 支持 Daniel Fuchs 实现 JEP 517: HTTP/3 |

---

## 4. 主要 JEP 贡献

### JEP 110: HTTP/2 Client (Incubator)

| 属性 | 值 |
|------|-----|
| **角色** | Owner |
| **状态** | Delivered |
| **发布版本** | JDK 9 |

**影响**: 定义了全新的 HTTP 客户端 API，实现 HTTP/2 和 WebSocket 支持，旨在替代遗留的 `HttpURLConnection` API。作为孵化模块首次在 JDK 9 中交付，为 Java 平台引入了现代化的异步 HTTP 客户端。

### JEP 321: HTTP Client (Standard)

| 属性 | 值 |
|------|-----|
| **角色** | Owner / Key Contributor |
| **状态** | Delivered |
| **发布版本** | JDK 11 |

**影响**: 将孵化中的 HTTP Client API 标准化，成为 `java.net.http` 模块的正式部分。API 提供基于 `CompletableFuture` 的非阻塞请求/响应语义，通过 `java.util.concurrent.Flow` API 实现请求和响应体的背压和流控。

### JEP 380: Unix-Domain Socket Channels

| 属性 | 值 |
|------|-----|
| **角色** | Owner |
| **状态** | Delivered |
| **发布版本** | JDK 16 |

**影响**: 为 `java.nio.channels` 中的 SocketChannel 和 ServerSocketChannel 添加 Unix 域套接字 (AF_UNIX) 支持。Unix 域套接字用于同一主机上的进程间通信 (IPC)，比 TCP/IP 回环连接更安全、更高效，并在 Unix 和 Windows 10+ 平台上均可使用。

### JEP 517: HTTP/3 for the HTTP Client API

| 属性 | 值 |
|------|-----|
| **角色** | Co-author / Networking Group Lead |
| **主要实现者** | Daniel Fuchs |
| **状态** | Delivered |
| **发布版本** | JDK 26 |

**影响**: 作为 Networking Group 负责人，Michael 参与了 HTTP/3 在 Java HTTP Client 中的引入。JEP 517 基于 QUIC 传输协议实现 HTTP/3，为 Java 应用在高延迟和丢包网络环境中提供更好的性能。

---

## 5. 核心技术贡献

### 1. Java HTTP Client 架构

Michael 主导了从 JDK 9 到 JDK 11 的 HTTP Client API 完整演进：

- **API 设计**: `HttpClient`、`HttpRequest`、`HttpResponse` 核心 API 的架构设计
- **HTTP/2 支持**: 多路复用、头部压缩 (HPACK)、服务器推送
- **异步模型**: 基于 `CompletableFuture` 的非阻塞 I/O
- **WebSocket 支持**: 集成 WebSocket 协议支持
- **背压机制**: 通过 Reactive Streams (`java.util.concurrent.Flow`) 实现流控

### 2. Unix 域套接字

- **SocketChannel 扩展**: 扩展 NIO SocketChannel 支持 AF_UNIX 地址族
- **ServerSocketChannel 扩展**: 支持 Unix 域套接字的服务端监听
- **UnixDomainSocketAddress**: 新增 `java.net.UnixDomainSocketAddress` 类型
- **跨平台支持**: 在 Unix (Linux, macOS) 和 Windows 10+ 上统一支持

### 3. Java 网络栈维护

- **java.net 核心类**: Socket、ServerSocket、URL 等核心网络类的维护
- **TLS/SSL 集成**: 与安全团队协作确保网络层安全
- **性能优化**: 网络 I/O 性能调优和连接池管理
- **API 废弃管理**: 推动过时 API 的废弃 (如 `URL::getPermission`)

---

## 6. 技术演讲与媒体

| 标题 | 日期 | 类型 | 说明 |
|------|------|------|------|
| **Episode 16: Let's Discuss JDK and Networking** | 2021-04-12 | Inside.java Podcast | 与 Daniel Fuchs 讨论 JDK 16/17 网络功能，HTTP/2 Client 更新，Unix Domain Sockets |
| **JEP-380: Unix domain socket channels** | 2021-02-03 | Inside.java 文章 | Unix 域套接字功能的技术介绍 |
| **Java Networking Enhancements since JDK 11** | 2022-12-28 | Inside.java 文章 | JDK 11 以来的 Java 网络增强汇总 |

---

## 7. 技术专长

### 网络协议

- **HTTP/1.1, HTTP/2, HTTP/3**: 完整的 HTTP 协议栈专家
- **WebSocket**: 双向实时通信协议
- **QUIC**: 基于 UDP 的传输层协议
- **Unix Domain Sockets**: 进程间通信机制

### Java 网络 API

- **java.net.http**: 现代 HTTP Client API
- **java.nio.channels**: NIO 通道和选择器
- **java.net**: 传统网络 API 维护
- **响应式编程**: Flow API 集成

### 系统级网络

- **TCP/IP 栈**: 底层网络协议理解
- **TLS/SSL**: 安全传输层
- **连接池与复用**: 高性能网络连接管理

---

## 8. 协作网络

| 协作者 | 合作领域 |
|--------|----------|
| [Daniel Fuchs](/by-contributor/profiles/daniel-fuchs.md) | HTTP/3 实现, HttpClient 维护, JEP 517 |
| [Chris Hegarty](/by-contributor/profiles/chris-hegarty.md) | 网络栈, Core Libraries |
| [Alan Bateman](/by-contributor/profiles/alan-bateman.md) | NIO, 虚拟线程与网络集成 |
| Daniel Jelinski | HTTP/3 CUBIC 拥塞控制 |

---

## 9. 相关链接

### 官方资料
- [Inside.java - MichaelMcMahon](https://inside.java/u/MichaelMcMahon/)
- [OpenJDK Census - mmcmahon](https://openjdk.org/census#mmcmahon)
- [OpenJDK Networking Group](https://openjdk.org/groups/net/)

### JEP 文档
- [JEP 110: HTTP/2 Client (Incubator)](https://openjdk.org/jeps/110) - JDK 9
- [JEP 321: HTTP Client (Standard)](https://openjdk.org/jeps/321) - JDK 11
- [JEP 380: Unix-Domain Socket Channels](https://openjdk.org/jeps/380) - JDK 16
- [JEP 517: HTTP/3 for the HTTP Client API](https://openjdk.org/jeps/517) - JDK 26

### 技术文档
- [Introduction to the Java HTTP Client](https://openjdk.org/groups/net/httpclient/intro.html)
- [Java 11 HTTP Client](https://openjdk.org/groups/net/httpclient/)
- [JEP-380: Unix domain socket channels (Inside.java)](https://inside.java/2021/02/03/jep380-unix-domain-sockets-channels/)
- [Java Networking Enhancements since JDK 11](https://inside.java/2022/12/28/jdk-networking-enhancements/)

### 媒体
- [Inside.java Podcast Episode 16](https://inside.java/2021/04/12/podcast-016/) - 与 Daniel Fuchs 讨论 JDK 网络功能

---

**Sources**:
- [Inside.java - MichaelMcMahon](https://inside.java/u/MichaelMcMahon/)
- [OpenJDK Census](https://openjdk.org/census)
- [JEP 110: HTTP/2 Client](https://openjdk.org/jeps/110)
- [JEP 321: HTTP Client (Standard)](https://openjdk.org/jeps/321)
- [JEP 380: Unix-Domain Socket Channels](https://openjdk.org/jeps/380)
- [JEP 517: HTTP/3 for the HTTP Client API](https://openjdk.org/jeps/517)
- [Inside.java Podcast Episode 16](https://inside.java/2021/04/12/podcast-016/)
