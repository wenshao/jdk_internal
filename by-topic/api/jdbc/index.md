# JDBC

> JDBC API、RowSet、连接池演进历程

---

## 快速概览

```
JDK 1.0 ── JDK 1.2 ── JDK 4 ── JDK 7 ── JDK 11
   │         │        │        │        │
JDBC 1.0  JDBC 2.0  JDBC 3.0  JDBC 4.1  JDBC 4.3
ODBC桥   RowSet    连接池    Try-with   模块化
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 1.1** | JDBC 1.0 | 基础数据库连接 |
| **JDK 1.2** | JDBC 2.0 | RowSet, 可滚动结果集 |
| **JDK 4** | JDBC 3.0 | 连接池, Savepoints |
| **JDK 6** | JDBC 4.0 | 自动驱动加载 |
| **JDK 7** | JDBC 4.1 | Try-with-resources |
| **JDK 11** | JDBC 4.3 | 模块化 |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### JDBC (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Lance Andersen | 7 | Oracle | JDBC 规范, 实现 |
| 2 | Joe Darcy | 5 | Oracle | API 设计 |
| 3 | Roger Riggs | 3 | Oracle | 核心库 |
| 4 | Hannes Wallnöfer | 2 | Oracle | JDBC 驱动 |

---

## 相关链接

- [JDBC 时间线](timeline.md)
- [核心 API](../)
