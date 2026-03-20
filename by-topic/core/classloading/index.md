# 类加载

> ClassLoader、双亲委派、模块化类加载演进历程

[← 返回核心平台](../)

---

## 快速概览

```
JDK 1.0 ── JDK 2 ── JDK 6 ── JDK 8 ── JDK 9 ── JDK 17
   │         │        │        │        │        │
类加载   双亲    线程上下   元空间   模块化   层层初始化
机制    委派    类加载器   类加载   类加载   (Layinit)
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 1.0** | ClassLoader | 基础类加载 |
| **JDK 2** | 双亲委派 | 安全性保证 |
| **JDK 6** | 线程上下文类加载器 | JavaEE 支持 |
| **JDK 8** | 元空间 | 取代永久代 |
| **JDK 9** | 模块化类加载 | JPMS |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 类加载 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Coleen Phillimore | 341 | Oracle | SystemDictionary |
| 2 | Ioi Lam | 254 | Oracle | CDS, AOT |
| 3 | Calvin Cheung | 103 | Oracle | 类加载器 |
| 4 | Harold Seigel | 89 | Oracle | JVM 运行时 |
| 5 | Stefan Karlsson | 87 | Oracle | 并发 GC |

---

## 相关链接

- [类加载时间线](timeline.md)
- [JVM 调优](../jvm/)
- [内存管理](../memory/)
