# 集合框架

> Collection、List、Set、Map、Stream 演进历程

[← 返回 API 框架](../)

---

## 快速概览

```
JDK 1.0 ── JDK 1.2 ── JDK 5 ── JDK 8 ── JDK 17
   │         │        │        │        │
Vector   Collection  泛型   Stream  不可变
HashTable  List/Set   增强循环 Optional 集合
          Map        for
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 1.0** | Vector/Hashtable | 原始集合 |
| **JDK 1.2** | 集合框架 | Collection/List/Set/Map |
| **JDK 5** | 泛型 | 类型安全 |
| **JDK 5** | 增强循环 | for-each |
| **JDK 8** | Stream | 函数式操作 |
| **JDK 9** | 不可变集合 | List.of/Set.of/Map.of |
| **JDK 17** | 增强伪随机数发生器 |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 集合框架 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Stuart Marks | 30+ | Oracle | 集合 API 设计 |
| 2 | Martin Buchholz | 20+ | Oracle | Collections 实现 |
| 3 | Brian Goetz | 15+ | Oracle | Stream API |
| 4 | Henry Jen | 12 | Oracle | 集合增强 |
| 5 | Paul Sandoz | 10 | Oracle | Stream/Optional |

---

## 相关链接

- [集合时间线](timeline.md)
- [核心 API](../)
- [并发编程](../../concurrency/)
