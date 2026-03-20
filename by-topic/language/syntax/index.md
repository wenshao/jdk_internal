# 语法演进

> 泛型、枚举、Lambda、模式匹配、记录类演进历程

---

## 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 8 ── JDK 14 ── JDK 17 ── JDK 21
   │         │        │        │        │        │
基础语法  泛型    Lambda   Records  Sealed   模式匹配
类/接口  枚举    Stream   Pattern  Classes  Switch
        变长    Optional  Matching          for
        参数    方法引用                     instance
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 5** | 泛型 (JSR 14) | 类型参数化 |
| **JDK 5** | 枚举 | enum 关键字 |
| **JDK 5** | 变长参数 | Method(...) |
| **JDK 8** | Lambda | 函数式编程 |
| **JDK 8** | 方法引用 | :: 操作符 |
| **JDK 10** | 局部变量类型推断 | var |
| **JDK 14** | Records (JEP 395) | 不可变类 |
| **JDK 15** | Sealed Classes | 密封类 |
| **JDK 21** | 模式匹配 | Pattern Matching |
| **JDK 21** | Switch 表达式 | 简化 switch |
| **JDK 21** | Record Patterns | 记录模式 |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 语法特性 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Joe Darcy | 11 | Oracle | 类型系统, 语法 |
| 2 | Vicente Romero | 7 | Oracle | javac 编译器 |
| 3 | Pavel Rappo | 2 | Oracle | API 设计 |
| 4 | Julia Boes | 2 | Oracle | Records |
| 5 | Jonathan Gibbons | 2 | Oracle | javac |

---

## 相关链接

- [语法时间线](timeline.md)
- [语言特性](../)
- [反射与元数据](../reflection/)
