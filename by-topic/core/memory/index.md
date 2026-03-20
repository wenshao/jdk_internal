# 内存管理

> 堆、栈、Metaspace、Compressed Oops 演进历程

---

## 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 6 ── JDK 8 ── JDK 17 ── JDK 21
   │         │        │        │        │        │
堆/栈    Compressed  永久代  元空间  ZGC    分代ZGC
 PermGen   Oops    移除   字符串  低延迟  吞吐量优化
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 5** | Compressed Oops | 压缩普通对象指针 |
| **JDK 6** | Compressed Oops | 默认启用 (64位) |
| **JDK 8** | 元空间 | 移除永久代 |
| **JDK 8u20** | String Deduplication | 字符串去重 |
| **JDK 11** | ZGC | 低延迟 GC |
| **JDK 15** | ZGC 生产可用 | 正式版 |
| **JDK 21** | 分代 ZGC | 降低 GC 频率 |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 内存管理 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Coleen Phillimore | 317 | Oracle | 类加载, 运行时 |
| 2 | Ioi Lam | 215 | Oracle | CDS, AOT, 内存 |
| 3 | David Holmes | 174 | Oracle | 并发, 线程 |
| 4 | Thomas Stuefe | 163 | Oracle | 内存, 跨平台 |
| 5 | Stefan Karlsson | 149 | Oracle | 并发 GC |
| 6 | Kim Barrett | 113 | Oracle | C++ 现代化 |
| 7 | Aleksey Shipilev | 112 | Oracle | 性能基准 |
| 8 | Robbin Ehn | 77 | Oracle | 并发, 锁 |
| 9 | Calvin Cheung | 77 | Oracle | 类加载 |
| 10 | Patricio Chilano Mateo | 76 | Oracle | 运行时 |

---

## 相关链接

- [内存时间线](timeline.md)
- [GC 演进](../gc/)
- [JVM 调优](../jvm/)
- [性能优化](../performance/)
