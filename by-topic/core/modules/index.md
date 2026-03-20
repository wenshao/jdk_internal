# 模块系统

> JEP 200、JPMS、jlink 演进历程

[← 返回核心平台](../)

---

## 快速概览

```
JDK 1.0 ── JDK 8 ── JDK 9 ── JDK 11 ── JDK 18
   │         │        │        │        │
单一下载  RT.jar   JPMS    jlink   增强
          Monolith  JEP 200  JEP 282  模块化
          Jar      module-info.java
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 8** | ClassPath | 传统类路径 |
| **JDK 9** | JPMS (JEP 200/261) | Java 平台模块系统 |
| **JDK 9** | module-info | 模块描述符 |
| **JDK 9** | jlink (JEP 282) | 自定义运行时 |
| **JDK 11** | 模块化增强 | 稳定化 |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 模块系统 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Claes Redestad | 18 | Oracle | 模块系统 |
| 2 | Alan Bateman | 17 | Oracle | JPMS 设计 |
| 3 | Severin Gehwolf | 13 | Red Hat | 模块系统 |
| 4 | Athijegannathan Sundararajan | 13 | Oracle | jlink |
| 5 | Mandy Chung | 9 | Oracle | 模块层 |

---

## 相关链接

- [模块系统时间线](timeline.md)
- [JVM 调优](../jvm/)
