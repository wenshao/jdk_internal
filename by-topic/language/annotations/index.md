# 注解

> 注解声明、注解处理器、类型注解演进历程

[← 返回语言特性](../)

---

## 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 6 ── JDK 7 ── JDK 8 ── JDK 21
   │         │        │        │        │        │
Javadoc   注解    注解    可重复    类型    注解模式
标签    JSR 175  处理器   注解     注解     匹配
         @Override  JSR   @Repeatable  Type
         @Deprecated  269               Use
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 1.0** | Javadoc | 文档注释 |
| **JDK 5** | 注解 (JSR 175) | @Override, @Deprecated |
| **JDK 6** | 注解处理器 (JSR 269) | 编译期处理 |
| **JDK 8** | 类型注解 (JSR 308) | Type Use |
| **JDK 8** | 可重复注解 | @Repeatable |
| **JDK 21** | 注解模式匹配 | for instanceof |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 注解/处理器 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Joe Darcy | 30 | Oracle | 注解, 类型系统 |
| 2 | Jan Lahoda | 18 | Oracle | 注解处理器 |
| 3 | Pavel Rappo | 10 | Oracle | API 设计 |
| 4 | Jonathan Gibbons | 10 | Oracle | Javadoc, 注解 |
| 5 | Vicente Romero | 6 | Oracle | javac 编译器 |
| 6 | Jim Laskey | 4 | Oracle | 字符串模板 |
| 7 | Aggelos Biboudis | 3 | Oracle | 模式匹配 |

---

## 相关链接

- [注解时间线](timeline.md)
- [反射与元数据](../reflection/)
- [语法演进](../syntax/)
