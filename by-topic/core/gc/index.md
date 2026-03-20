# GC 垃圾收集器

> 从 Serial 到分代 ZGC 的完整演进历程

---

## 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 6 ── JDK 7 ── JDK 9 ── JDK 11 ── JDK 15 ── JDK 21 ── JDK 26
   │         │        │        │        │        │         │         │         │
Serial    Parallel CMS    G1    G1默认   ZGC      ZGC     分代ZGC  G1优化
GC        GC      (废弃)  (默认)  (实验)  (生产)  (生产)   (正式)
```

### GC 算法对比

| GC 算法 | 首发版本 | 设计目标 | 适用场景 |
|---------|----------|----------|----------|
| **Serial** | JDK 1.0 | 单线程，内存占用小 | 单核、小内存 |
| **Parallel** | JDK 6 | 多线程，吞吐量优先 | 多核、后台批处理 |
| **CMS** | JDK 6 | 低延迟 | 交互式应用 (已废弃) |
| **G1** | JDK 6 | 可预测停顿 | 通用服务器应用 (默认) |
| **ZGC** | JDK 11 | 低延迟 (<10ms) | 大内存、低延迟 |
| **Shenandoah** | JDK 12 | 低延迟 (<10ms) | 大内存、低延迟 |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### G1 GC (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Thomas Schatzl | 600 | Oracle | G1 GC 维护者 |
| 2 | Albert Mingkun Yang | 202 | Oracle | G1 GC, 内存管理 |
| 3 | Kim Barrett | 129 | Oracle | C++ 现代化 |
| 4 | Ivan Walulya | 83 | Oracle | G1 GC |
| 5 | Stefan Karlsson | 75 | Oracle | 并发 GC |
| 6 | Stefan Johansson | 56 | Oracle | G1 GC |

### ZGC (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Per Lidén | 157 | Oracle | ZGC 创始人 |
| 2 | Stefan Karlsson | 116 | Oracle | 分代 ZGC (JEP 439) |
| 3 | Erik Österlund | 56 | Oracle | ZGC 核心开发者 |
| 4 | Per Liden | 45 | Oracle | ZGC (别名) |
| 5 | Axel Boldt-Christmas | 44 | Oracle | ZGC |
| 6 | Joel Sikström | 31 | Oracle | ZGC |

### Shenandoah GC (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Aleksey Shipilev | 272 | Oracle | Shenandoah 维护者 |
| 2 | Zhengyu Gu | 217 | Oracle | Shenandoah 核心开发者 |
| 3 | William Kemper | 109 | Red Hat | 分代 Shenandoah (JEP 429) |
| 4 | Roman Kennke | 107 | Red Hat | Shenandoah 架构 |
| 5 | Stefan Karlsson | 44 | Oracle | 并发支持 |

---

## 相关链接

- [GC 时间线](timeline.md)
- [核心平台](../)
- [性能优化](../performance/)
