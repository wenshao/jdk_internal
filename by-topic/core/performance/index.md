# 性能优化

> JIT、分层编译、逃逸分析、JFR 演进历程

[← 返回核心平台](../)

---

## 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 7 ── JDK 8 ── JDK 17 ── JDK 21
   │         │        │        │        │        │
解释器    分层   G1 GC  Lambda  Graal  虚拟线程
(纯解释)  编译   默认   Stream  (实验)  (正式)
```

### 核心技术

| 技术 | 首发版本 | 说明 |
|------|----------|------|
| **解释器** | JDK 1.0 | 纯解释执行 |
| **JIT 编译** | JDK 1.0 | C1/C2 编译器 |
| **分层编译** | JDK 6 | C1 + C2 组合 |
| **逃逸分析** | JDK 6 | 标量替换、栈上分配 |
| **Graal JIT** | JDK 9 | 实验性高性能 JIT |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 性能优化 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Coleen Phillimore | 72 | Oracle | C1/C2 编译器 |
| 2 | Aleksey Shipilev | 68 | Oracle | JIT 编译器 |
| 3 | Ioi Lam | 62 | Oracle | 编译器, 运行时 |
| 4 | Stefan Karlsson | 31 | Oracle | 编译器, GC |
| 5 | Doug Simon | 29 | Oracle | JIT 编译器 |
| 6 | David Holmes | 24 | Oracle | 并发, 编译器 |
| 7 | Claes Redestad | 24 | Oracle | 启动性能 |
| 8 | Thomas Stuefe | 22 | Oracle | 编译器 |
| 9 | Vladimir Kozlov | 20 | Oracle | JIT 编译器 |
| 10 | Igor Veresov | 17 | Oracle | JIT 编译器 |

### 启动性能 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Ioi Lam | 167 | Oracle | CDS, AOT |
| 2 | Albert Mingkun Yang | 75 | Oracle | G1 GC, 内存 |
| 3 | Claes Redestad | 70 | Oracle | 字符串, 启动优化 |
| 4 | Thomas Stuefe | 37 | Oracle | CDS, 归档 |
| 5 | Stefan Karlsson | 35 | Oracle | 并发 GC |

---

## 相关链接

- [性能时间线](timeline.md)
- [JVM 调优](../jvm/)
- [内存管理](../memory/)
- [GC 演进](../gc/)
