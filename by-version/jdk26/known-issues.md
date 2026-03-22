# JDK 26 已知问题

> **版本**: JDK 26 (Feature Release) | **发布日期**: 2026-03-17 | **最后更新**: 2026-03-23

---
## 目录

1. [概述](#1-概述)
2. [预览特性限制](#2-预览特性限制)
3. [HTTP/3 注意事项](#3-http3-注意事项)
4. [兼容性问题](#4-兼容性问题)
5. [平台特定问题](#5-平台特定问题)
6. [相关链接](#6-相关链接)

---


## 1. 概述

JDK 26 作为 Feature Release，整体质量稳定。以下问题主要涉及新特性的使用限制。

| 类别 | 问题数 | 严重程度 |
|------|--------|----------|
| 预览特性 | 3 | 🟡 中 |
| HTTP/3 | 2 | 🟢 低 |
| 兼容性 | 1 | 🟢 低 |

---

## 2. 预览特性限制

### 结构化并发（第六次预览）

- API 自 JDK 21 以来持续调整，JDK 26 的 `Joiner` API 与 JDK 25 有差异
- 需要 `--enable-preview` 编译和运行

### 原始类型模式匹配（第四次预览）

- 部分复杂嵌套模式匹配场景的编译器行为仍在优化
- 与泛型类型擦除的交互存在边界情况

### Lazy Constants（第二次预览）

- `LazyConstant` API 为新引入，语义和使用模式仍在社区讨论
- 与 `static final` 和 `Stable Values` 的使用场景区分需要注意

---

## 3. HTTP/3 注意事项

### 网络环境要求

HTTP/3 基于 QUIC 协议（UDP），需要注意：

- **防火墙**: 确保 UDP 443 端口开放
- **负载均衡器**: 部分 L4 负载均衡器不支持 QUIC
- **企业网络**: 某些企业网络可能限制 UDP 流量

```java
// 如果 HTTP/3 不可用，HttpClient 自动回退到 HTTP/2
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_3)
    .build();
// 检查实际使用的协议版本
response.version();  // 可能返回 HTTP_2 而非 HTTP_3
```

### TLS 要求

HTTP/3 要求 TLS 1.3，不支持自签名证书的场景需要额外配置。

---

## 4. 兼容性问题

### Final 字段警告

JEP 500 在 JDK 26 中首先引入运行时警告。依赖反射修改 final 字段的框架需要关注：

| 框架 | 最低兼容版本 | 说明 |
|------|-------------|------|
| Spring Framework | 6.2+ | 避免 final 字段注入 |
| Gson | 2.11+ | 反序列化到 final 字段 |
| Jackson | 2.17+ | 构造器模式推荐 |

---

## 5. 平台特定问题

### Linux

- **QUIC 内核支持**: Linux 5.6+ 对 QUIC 有更好的 UDP 性能
- **JFR**: 完全支持，无已知问题

### macOS

- **HTTP/3**: 完全支持
- **AArch64 (Apple Silicon)**: 完全支持

### Windows

- **HTTP/3**: Windows 11 / Server 2022 完全支持
- **较旧版本**: Windows 10 的 UDP 性能可能影响 HTTP/3 表现

---

## 6. 相关链接

- [JDK 26 主页](../README.md)
- [JDK 26 破坏性变更](../breaking-changes.md)
- [HTTP/3 实现深度分析](../deep-dive/http3-implementation.md)
- [JDK 26 迁移指南](../migration/from-21.md)

---

[← 返回 JDK 26](../README.md)
