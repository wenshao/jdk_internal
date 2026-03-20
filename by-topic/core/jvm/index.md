# JVM 调优与监控

> JVM 参数、调优工具和监控技术演进

---

## 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 6 ── JDK 7 ── JDK 8 ── JDK 11 ── JDK 21
   │         │        │        │        │        │        │
基础参数   JMX    jstat   G1 GC  元空间   ZGC     分代ZGC
-Xmx/-Xms  jconsole jmap   默认  Metaspace 低延迟   生产就绪
```

### 核心工具

| 工具 | 首发版本 | 用途 |
|------|----------|------|
| **jstat** | JDK 6 | GC 统计 |
| **jmap** | JDK 6 | 堆转储 |
| **jstack** | JDK 5 | 线程转储 |
| **jcmd** | JDK 7 | 统一诊断工具 |
| **jconsole** | JDK 5 | JMX 监控 |
| **JFR** | JDK 7 | Java Flight Recorder |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### JVM 运行时 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Coleen Phillimore | 317 | Oracle | 类加载, 运行时核心 |
| 2 | Ioi Lam | 215 | Oracle | CDS, AOT, 运行时 |
| 3 | David Holmes | 174 | Oracle | 并发, 线程, 规范 |
| 4 | Thomas Stuefe | 163 | Oracle | 内存, 跨平台 |
| 5 | Stefan Karlsson | 149 | Oracle | 并发 GC |
| 6 | Kim Barrett | 113 | Oracle | C++ 现代化 |
| 7 | Aleksey Shipilev | 112 | Oracle | 性能基准 |
| 8 | Daniel D. Daugherty | 87 | Oracle | JVMTI, 调试 |
| 9 | Robbin Ehn | 77 | Oracle | 并发, 锁 |
| 10 | Calvin Cheung | 77 | Oracle | 类加载 |

---

## 相关链接

- [JVM 时间线](timeline.md)
- [内存管理](../memory/)
- [性能优化](../performance/)
- [GC 演进](../gc/)
