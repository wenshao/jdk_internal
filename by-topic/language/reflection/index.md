# 反射与元数据

> 反射、注解和字节码操作的演进历程

---

## 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 6 ── JDK 7 ── JDK 8 ── JDK 16 ── JDK 24
   │         │        │        │        │        │        │
反射    注解    注解   MethodHandle Lambda   ClassFile  Mirror
API    (JSR   处理   (JSR   invokedynamic  (JEP 395)  API
        175)    JSR   JSR   292)      (JEP 484)
                269)           ClassFile
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 1.0** | 反射 API | Class, Method, Field |
| **JDK 5** | 注解 (JSR 175) | @interface, 元编程 |
| **JDK 6** | 注解处理器 (JSR 269) | 编译期处理 |
| **JDK 7** | MethodHandle (JSR 292) | 动态语言支持 |
| **JDK 8** | Lambda invokedynamic | 函数式编程 |
| **JDK 16** | ClassFile API (JEP 395) | Class 文件操作 |
| **JDK 24** | Class-File API (JEP 484) | 正式版 |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 类加载/反射 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Coleen Phillimore | 341 | Oracle | 类加载, 运行时 |
| 2 | Ioi Lam | 254 | Oracle | 反射, CDS, AOT |
| 3 | Calvin Cheung | 103 | Oracle | 类加载 |
| 4 | Harold Seigel | 89 | Oracle | JVM 运行时 |
| 5 | Stefan Karlsson | 87 | Oracle | 并发 GC |
| 6 | David Holmes | 63 | Oracle | 并发规范 |
| 7 | Aleksey Shipilev | 61 | Oracle | 性能基准 |
| 8 | Kim Barrett | 60 | Oracle | C++ 现代化 |
| 9 | Claes Redestad | 58 | Oracle | 性能优化 |
| 10 | Chen Liang | 47 | Oracle | ClassFile API |

### invokedynamic/lambda (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Claes Redestad | 89 | Oracle | invokedynamic, 字符串拼接 |
| 2 | Mandy Chung | 66 | Oracle | Lambda, invokedynamic |
| 3 | Joe Darcy | 54 | Oracle | Lambda, 类型推断 |
| 4 | Chen Liang | 47 | Oracle | ClassFile API, invokedynamic |
| 5 | Jorn Vernee | 19 | Oracle | Foreign Memory |
| 6 | Paul Sandoz | 17 | Oracle | 函数式 API |
| 7 | Maurizio Cimadamore | 15 | Oracle | javac, Lambda |
| 8 | Vladimir Ivanov | 11 | Oracle | JIT 编译器 |

---

## 相关链接

- [反射时间线](timeline.md)
- [Class File API](../classfile/)
- [语法演进](../syntax/)
- [语言特性](../)
