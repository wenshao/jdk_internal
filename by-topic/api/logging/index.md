# 日志

> java.util.logging、System.Logger、日志桥接演进历程

---

## 快速概览

```
JDK 1.0 ── JDK 1.4 ── JDK 9 ── JDK 11
   │         │        │        │
System.out  JUL    System.Logger  日志增强
PrintStream  java.util.  桥接
          logging    JUL桥接
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 1.0** | System.out | 控制台输出 |
| **JDK 1.4** | java.util.logging (JUL) | 内置日志框架 |
| **JDK 9** | System.Logger | 平台日志 API |
| **JDK 11** | 日志桥接 | SLF4J 桥接支持 |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 日志 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Daniel Fuchs | 15 | Oracle | 日志框架 |
| 2 | Roger Riggs | 3 | Oracle | 核心库 |
| 3 | Pavel Rappo | 3 | Oracle | API 设计 |
| 4 | Mandy Chung | 3 | Oracle | 模块系统 |
| 5 | Joe Darcy | 3 | Oracle | API 设计 |

---

## 相关链接

- [日志时间线](timeline.md)
- [核心 API](../)
