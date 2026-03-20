# 异常处理

> Throwable、Exception、Error、异常链演进历程

---

## 快速概览

```
JDK 1.0 ── JDK 1.4 ── JDK 7 ── JDK 9 ── JDK 21
   │         │        │        │        │
异常    异常链   try-with   StackWalker  异常层次
体系    getCause   resources  (JEP 259)   优化
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 1.0** | Throwable/Error/Exception | 异常体系 |
| **JDK 1.4** | 异常链 | getCause() |
| **JDK 7** | try-with-resources | 自动资源管理 |
| **JDK 7** | multi-catch | 多异常捕获 |
| **JDK 9** | StackWalker | 栈遍历 API |
| **JDK 21** | 异常优化 | 性能改进 |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 异常处理 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Joe Darcy | 7 | Oracle | 异常体系 |
| 2 | Pavel Rappo | 4 | Oracle | API 设计 |
| 3 | Erik Gahlin | 3 | Oracle | JFR |
| 4 | Roger Riggs | 1 | Oracle | 核心库 |
| 5 | Mikael Vidstedt | 1 | Oracle | 运行时 |

---

## 相关链接

- [异常时间线](timeline.md)
- [核心 API](../)
