# XML 与 JSON

> DOM、SAX、StAX、JSON 处理演进历程

[← 返回 API 框架](../)

---

## 快速概览

```
JDK 1.0 ── JDK 1.4 ── JDK 6 ── JDK 11 ── JDK 23
   │         │        │        │        │
DOM      SAX     StAX    JSON-P  JSON.B
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 1.4** | DOM/SAX | XML 解析 |
| **JDK 6** | StAX (JSR 173) | 流式 XML 解析 |
| **JDK 11** | JSON-P (JEP 353) | JSON 处理 API |
| **JDK 23** | JSON.B (JEP 471) | JSON 绑定 |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### XML/JSON (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Joe Wang | 42 | Oracle | XML, JSON API |
| 2 | Roger Riggs | 2 | Oracle | 核心库 |
| 3 | Pavel Rappo | 2 | Oracle | API 设计 |
| 4 | Justin Lu | 2 | Oracle | JSON 处理 |
| 5 | Joe Darcy | 2 | Oracle | API 设计 |

---

## 相关链接

- [XML/JSON 时间线](timeline.md)
- [核心 API](../)
