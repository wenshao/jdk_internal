# HTTP 客户端

> 从 HttpURLConnection 到 HTTP/3 的完整演进历程

---

## 快速概览

```
JDK 1.0 ── JDK 9 ── JDK 11 ── JDK 16 ── JDK 22 ── JDK 26
   │         │        │        │        │        │
HttpURL   HTTP    HTTP    HTTP/2  多项    HTTP/3
Connection Client  Client  支持   优化    (预览)
(旧API)   (孵化)  (标准)         (预览)  JEP 517
```

### 协议演进

| 版本 | 协议 | 特性 |
|------|------|------|
| **JDK 1.0** | HTTP/1.0 | 基础支持 |
| **JDK 11** | HTTP/2 | 多路复用 |
| **JDK 26** | HTTP/3 | 基于 QUIC |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### HTTP Client (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Daniel Fuchs | 95 | Oracle | HTTP Client, HTTP/3 |
| 2 | Michael McMahon | 19 | Oracle | HTTP Client (JEP 321) |
| 3 | Jaikiran Pai | 18 | Red Hat/Oracle | HTTP/2, 连接池 |
| 4 | Volkan Yazıcı | 17 | Oracle | HTTP/3, WebSocket |
| 5 | Chris Hegarty | 17 | Oracle | HTTP Client 基础 |
| 6 | Daniel Jeliński | 16 | Oracle | HTTP/2, 连接池 |
| 7 | Conor Cleary | 14 | Oracle | HTTP/3 (QUIC) |

---

## 相关链接

- [HTTP 时间线](timeline.md)
- [并发编程](../concurrency/)
- [网络编程](../network/)
