# IO 与 NIO

> File、Stream、Channel、Buffer 演进历程

[← 返回 API 框架](../)

---

## 快速概览

```
JDK 1.0 ── JDK 1.4 ── JDK 7 ── JDK 11
   │         │        │        │
File     NIO     NIO.2   增强
Stream   Channel Path   File
         Selector  Files
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 1.0** | Stream IO | InputStream/OutputStream |
| **JDK 1.0** | File API | java.io.File |
| **JDK 1.4** | NIO (JSR 51) | Buffer, Channel, Selector |
| **JDK 7** | NIO.2 (JSR 203) | Path, Files, WatchService |
| **JDK 11** | 增强 | 文件操作优化 |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### IO/NIO (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Alan Bateman | 43 | Oracle | NIO, NIO.2 (JSR 51, JSR 203) |
| 2 | Chris Hegarty | 17 | Oracle | 网络基础 |
| 3 | Brian Goetz | 12 | Oracle | API 设计 |
| 4 | Henry Jen | 10 | Oracle | NIO.2 增强 |
| 5 | Paul Sandoz | 8 | Oracle | IO 增强 |

---

## 相关链接

- [IO 时间线](timeline.md)
- [核心 API](../)
- [网络编程](../../concurrency/network/)
