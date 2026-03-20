# 网络编程

> Socket、NIO、Unix Domain Socket 演进历程

[← 返回并发网络](../)

---

## 快速概览

```
JDK 1.0 ── JDK 1.4 ── JDK 7 ── JDK 11 ── JDK 18 ── JDK 26
   │         │         │        │        │        │
Socket/   NIO      NIO.2   HTTP   Unix    HTTP/3
ServerSocket Channel  Path   Client Domain  预览
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 1.0** | Socket/ServerSocket | TCP/UDP 基础 |
| **JDK 1.4** | NIO | Buffer, Channel, Selector |
| **JDK 7** | NIO.2 | Path, Files, WatchService |
| **JDK 11** | HTTP Client | 新 API 标准化 |
| **JDK 18** | Unix Domain Socket | 本地 IPC |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 网络/并发 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Alan Bateman | 43 | Oracle | NIO, NIO.2 (JSR 51, JSR 203) |
| 2 | Viktor Klang | 44 | Lightbend/Oracle | CompletableFuture |
| 3 | Chris Hegarty | 17 | Oracle | HTTP Client 基础 |
| 4 | Daniel Jeliński | 16 | Oracle | HTTP/2, 连接池 |
| 5 | Jaikiran Pai | 34 | Red Hat/Oracle | HTTP/2, 网络层 |

---

## 相关链接

- [网络编程时间线](timeline.md)
- [HTTP 客户端](../http/)
- [并发编程](../concurrency/)
- [并发网络](../)
