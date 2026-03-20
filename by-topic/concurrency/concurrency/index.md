# 并发编程

> 从 Thread 到 Virtual Thread 的完整演进历程

[← 返回并发网络](../)

---

## 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 7 ── JDK 8 ── JDK 19 ── JDK 21 ── JDK 26
   │         │        │        │        │        │        │
Thread    Executor ForkJoin Stream Virtual Structured Scoped
Runnable  Future   Pool    Parallel Thread  Concurrency Values
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 1.0** | Thread, Runnable | 基础线程 |
| **JDK 5** | Executor 框架 | 线程池、并发集合 |
| **JDK 7** | Fork/Join 框架 | 工作窃取算法 |
| **JDK 8** | CompletableFuture | 异步编程 |
| **JDK 19** | Virtual Threads (预览) | 轻量级线程 |
| **JDK 21** | Virtual Threads (正式) | 生产就绪 |
| **JDK 26** | Structured Concurrency | 结构化并发 |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 并发基础 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Doug Lea | 65 | SUNY Oswego | JSR-166, ConcurrentHashMap |
| 2 | Alan Bateman | 43 | Oracle | NIO, Thread |
| 3 | Viktor Klang | 29 | Lightbend/Oracle | CompletableFuture |
| 4 | Martin Buchholz | 13 | Google | 并发工具, 算法 |
| 5 | Stuart Marks | 8 | Oracle | 集合, 并发 |

### Thread/Virtual Thread (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Alan Bateman | 43 | Oracle | Virtual Threads 实现 |
| 2 | Serguei Spitsyn | 6 | Oracle | JVMTI, 线程 |
| 3 | Patricio Chilano Mateo | 5 | Oracle | JVM 运行时 |
| 4 | David Holmes | 4 | Oracle | 并发规范 |
| 5 | Mandy Chung | 2 | Oracle | 监控, JFR |

---

## 相关链接

- [并发时间线](timeline.md)
- [HTTP 客户端](../http/)
- [网络编程](../network/)
- [并发网络](../)
