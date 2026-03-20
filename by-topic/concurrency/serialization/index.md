# 序列化

> Serializable、Externalizable、序列化过滤器演进历程

[← 返回并发网络](../)

---

## 快速概览

```
JDK 1.0 ── JDK 1.2 ── JDK 6 ── JDK 9 ── JDK 17 ── JDK 21
   │         │        │        │        │        │
序列化   Externalizable  过滤器  Records  模式匹配  模式匹配
接口      优化          JEP     不可序列   for       for
                              默认      instance   instanceof
                              序列化
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 1.0** | Serializable | 基础序列化接口 |
| **JDK 1.2** | Externalizable | 自定义序列化 |
| **JDK 6** | readResolve/writeReplace | 序列化代理模式 |
| **JDK 9** | 过滤器 (JEP 290) | 序列化安全过滤 |
| **JDK 17** | Record 序列化 | 不可变对象序列化 |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 序列化 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Kim Barrett | 12 | Oracle | 序列化运行时 |
| 2 | Stefan Karlsson | 8 | Oracle | 对象布局, 序列化 |
| 3 | Mandy Chung | 8 | Oracle | 序列化核心 |
| 4 | Joe Darcy | 5 | Oracle | Record 序列化 |
| 5 | Ioi Lam | 5 | Oracle | 序列化优化 |
| 6 | Roman Kennke | 4 | Red Hat | Shenandoah GC |
| 7 | Pavel Rappo | 4 | Oracle | API 设计 |

---

## 相关链接

- [序列化时间线](timeline.md)
- [并发编程](../)
- [网络编程](../network/)
