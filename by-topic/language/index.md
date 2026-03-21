# 语言特性

语法、类型系统、反射、字节码等语言层面演进。

[← 返回主题索引](../)

---
## 目录

1. [演进概览](#1-演进概览)
2. [完整语言特性演进表 (JDK 5-26)](#2-完整语言特性演进表-jdk-5-26)
3. [OpenJDK 项目](#3-openjdk-项目)
4. [主题列表](#4-主题列表)
5. [核心贡献者](#5-核心贡献者)
6. [按 JDK 版本索引](#6-按-jdk-版本索引)
7. [内部开发者资源](#7-内部开发者资源)
8. [统计数据](#8-统计数据)
9. [学习路径](#9-学习路径)

---

## 1. 演进概览

```
JDK 1.0 ── JDK 5 ── JDK 7 ── JDK 8 ── JDK 9 ── JDK 10 ── JDK 14-17 ── JDK 21 ── JDK 25-26
   │          │        │        │        │         │           │            │           │
 基础语法   泛型    Diamond  Lambda   模块化     var        Records      模式匹配    紧凑源文件
 反射      枚举    try-with  Stream   Compact    类型推断    Sealed       switch模式   模块导入
 类/接口   注解    resources 方法引用  Strings               switch表达式  Record模式  原始类型模式
           变参    多异常捕获         invokedynamic                       未命名变量   灵活构造体
                                      字符串拼接
```

### 版本里程碑

| 版本 | 年份 | 主题 | 关键特性 |
|------|------|------|----------|
| **JDK 5** | 2004 | 语法革命 | 泛型、枚举、注解、变参、增强 for、自动装箱 |
| **JDK 7** | 2011 | 语法简化 | Diamond、try-with-resources、多异常捕获、MethodHandle (JSR 292) |
| **JDK 8** | 2014 | 函数式编程 | Lambda (JSR 335)、Stream API、方法引用、默认方法 |
| **JDK 9** | 2017 | 模块化与字符串 | JPMS、Compact Strings (JEP 254)、invokedynamic 字符串拼接 (JEP 280) |
| **JDK 10** | 2018 | 类型推断 | 局部变量类型推断 var (JEP 286) |
| **JDK 11 LTS** | 2018 | API 增强 | 字符串新方法 (repeat/strip/isBlank)、HTTP Client |
| **JDK 14** | 2020 | 表达式增强 | switch 表达式 (JEP 361) |
| **JDK 15** | 2020 | 文本处理 | Text Blocks (JEP 378) |
| **JDK 16** | 2021 | 数据建模 | Records (JEP 395)、instanceof 模式匹配 (JEP 394) |
| **JDK 17 LTS** | 2021 | 继承控制 | Sealed Classes (JEP 409) |
| **JDK 21 LTS** | 2023 | 模式匹配成熟 | switch 模式匹配 (JEP 441)、Record Patterns (JEP 440) |
| **JDK 22** | 2024 | 未命名模式 | 未命名变量与模式 (JEP 456)、ClassFile API 预览 (JEP 457) |
| **JDK 24** | 2025 | 字节码 API | ClassFile API 正式版 (JEP 484) |
| **JDK 25 LTS** | 2025 | 语法最终化 | 紧凑源文件 (JEP 512)、模块导入 (JEP 511)、灵活构造体 (JEP 513) |
| **JDK 26** | 2026 | 持续演进 | 原始类型模式第四预览 (JEP 530)、Lazy Constants 第二预览 (JEP 526) |

---

## 2. 完整语言特性演进表 (JDK 5-26)

### 语法与类型系统

| 版本 | 特性 | JEP/JSR | 状态 | 说明 |
|------|------|---------|------|------|
| **JDK 5** | 泛型 | JSR 14 | 正式 | 类型参数化，编译期类型安全 |
| **JDK 5** | 枚举 | - | 正式 | enum 关键字 |
| **JDK 5** | 注解 | JSR 175 | 正式 | @interface 元数据 |
| **JDK 5** | 变参 | - | 正式 | T... 可变长参数 |
| **JDK 5** | 增强 for | - | 正式 | for (T x : collection) |
| **JDK 5** | 自动装箱/拆箱 | - | 正式 | int <-> Integer |
| **JDK 5** | 静态导入 | - | 正式 | import static |
| **JDK 7** | Diamond 操作符 | - | 正式 | `new ArrayList<>()` |
| **JDK 7** | try-with-resources | - | 正式 | 自动资源管理 |
| **JDK 7** | 多异常捕获 | - | 正式 | `catch (A \| B e)` |
| **JDK 7** | switch 字符串 | - | 正式 | switch 支持 String |
| **JDK 7** | 二进制字面量 | - | 正式 | 0b1010 |
| **JDK 7** | 数字下划线 | - | 正式 | 1_000_000 |
| **JDK 8** | Lambda 表达式 | JSR 335 | 正式 | `(x) -> x + 1` |
| **JDK 8** | 方法引用 | JSR 335 | 正式 | `Object::method` |
| **JDK 8** | 默认方法 | JSR 335 | 正式 | 接口 default 方法 |
| **JDK 8** | 重复注解 | - | 正式 | @Repeatable |
| **JDK 8** | 类型注解 | JSR 308 | 正式 | 注解可用于类型位置 |
| **JDK 9** | 私有接口方法 | - | 正式 | 接口 private 方法 |
| **JDK 10** | var 局部变量 | JEP 286 | 正式 | 局部变量类型推断 |
| **JDK 12** | switch 表达式 | JEP 325 | 预览 | 首次预览 |
| **JDK 13** | switch 表达式 | JEP 354 | 预览 | 第二次预览，引入 yield |
| **JDK 14** | switch 表达式 | JEP 361 | **正式** | `int r = switch(x) { ... };` |
| **JDK 14** | instanceof 模式 | JEP 305 | 预览 | 首次预览 |
| **JDK 15** | instanceof 模式 | JEP 375 | 预览 | 第二次预览 |
| **JDK 14** | Records | JEP 359 | 预览 | 首次预览 |
| **JDK 15** | Records | JEP 384 | 预览 | 第二次预览 |
| **JDK 15** | Sealed Classes | JEP 360 | 预览 | 首次预览 |
| **JDK 16** | Records | JEP 395 | **正式** | 不可变数据类 |
| **JDK 16** | instanceof 模式 | JEP 394 | **正式** | `obj instanceof String s` |
| **JDK 16** | Sealed Classes | JEP 397 | 预览 | 第二次预览 |
| **JDK 17** | Sealed Classes | JEP 409 | **正式** | 密封类/接口 |
| **JDK 17** | switch 模式匹配 | JEP 406 | 预览 | 首次预览 |
| **JDK 18** | switch 模式匹配 | JEP 420 | 预览 | 第二次预览 |
| **JDK 19** | switch 模式匹配 | JEP 427 | 预览 | 第三次预览 |
| **JDK 20** | switch 模式匹配 | JEP 433 | 预览 | 第四次预览 |
| **JDK 20** | Record Patterns | JEP 432 | 预览 | 第二次预览 |
| **JDK 21** | switch 模式匹配 | JEP 441 | **正式** | `case Type t -> ...` |
| **JDK 21** | Record Patterns | JEP 440 | **正式** | 记录解构 |
| **JDK 21** | 未命名模式和变量 | JEP 443 | 预览 | 首次预览 |
| **JDK 22** | 未命名变量与模式 | JEP 456 | **正式** | `_` 占位符 |
| **JDK 23** | 原始类型模式 | JEP 455 | 预览 | 首次预览 |
| **JDK 24** | 原始类型模式 | JEP 488 | 预览 | 第二次预览 |
| **JDK 25** | 原始类型模式 | JEP 507 | 预览 | 第三次预览 |
| **JDK 25** | 灵活构造体 | JEP 513 | **正式** | 构造方法前可执行语句 |
| **JDK 25** | 紧凑源文件 | JEP 512 | **正式** | 简化入门 `void main() {}` |
| **JDK 25** | 模块导入声明 | JEP 511 | **正式** | `import module java.base;` |
| **JDK 26** | 原始类型模式 | JEP 530 | 预览 | 第四次预览 |
| **JDK 26** | Lazy Constants | JEP 526 | 预览 | 第二次预览 |

### 字符串处理演进

| 版本 | 特性 | JEP/JSR | 状态 | 说明 |
|------|------|---------|------|------|
| **JDK 8** | StringJoiner | - | 正式 | 字符串连接器 |
| **JDK 9** | Compact Strings | JEP 254 | **正式** | byte[] 存储，LATIN1/UTF16 编码标志 |
| **JDK 9** | invokedynamic 字符串拼接 | JEP 280 | **正式** | 替代 StringBuilder 字节码 |
| **JDK 11** | 字符串新方法 | - | 正式 | repeat()、strip()、isBlank()、lines() |
| **JDK 12** | indent()、transform() | - | 正式 | 字符串转换方法 |
| **JDK 13** | Text Blocks | JEP 355 | 预览 | 首次预览 |
| **JDK 14** | Text Blocks | JEP 368 | 预览 | 第二次预览 |
| **JDK 15** | Text Blocks | JEP 378 | **正式** | `"""..."""` 多行字符串 |
| **JDK 21** | String Templates | JEP 430 | 预览 | 首次预览 |
| **JDK 22** | String Templates | JEP 459 | 预览 | 第二次预览 |
| **JDK 23** | String Templates | - | **撤回** | 设计问题，从 JDK 23 移除 |
| **JDK 24** | 隐藏类拼接策略 | JDK-8336856 | 正式 | +40% 启动性能 |
| **JDK 26** | Integer/Long.toString | JDK-8370503 | 正式 | toString 优化 |

> **String Templates 注**: 该特性经 JEP 430 (JDK 21) 和 JEP 459 (JDK 22) 两轮预览后，因处理器设计
> (processor-centric) 方案存在可组合性问题，Brian Goetz 在 amber-spec-experts 邮件列表发文讨论后决定撤回。
> 这是 Java 历史上首个经预览后被撤回的特性。

### 反射与元数据演进

| 版本 | 特性 | JEP/JSR | 说明 |
|------|------|---------|------|
| **JDK 1.0** | 反射 API | - | java.lang.reflect |
| **JDK 5** | 注解 | JSR 175 | @interface 元数据 |
| **JDK 6** | 注解处理器 API | JSR 269 | Pluggable Annotation Processing |
| **JDK 7** | MethodHandle | JSR 292 | invokedynamic 基础设施 |
| **JDK 7** | 类型注解 | JSR 308 | 注解可用于类型位置 |
| **JDK 8** | Lambda invokedynamic | - | LambdaMetafactory |
| **JDK 8** | 参数反射 | - | Parameter 类 |
| **JDK 11** | Constable/ConstantDesc | - | 常量描述 API |
| **JDK 16** | Records | JEP 395 | 不可变数据类 |
| **JDK 22** | ClassFile API | JEP 457 | 预览版 |
| **JDK 23** | ClassFile API | JEP 466 | 第二次预览 |
| **JDK 24** | ClassFile API | JEP 484 | **正式版** |

### ClassFile API 演进

ClassFile API 是 JDK 标准 class 文件读写 API，旨在替代第三方 ASM 库。

| 版本 | JEP | 状态 | 说明 |
|------|-----|------|------|
| **JDK 22** | JEP 457 | 预览 | 首次预览，引入不可变模型 |
| **JDK 23** | JEP 466 | 预览 | 第二次预览，API 细化 |
| **JDK 24** | JEP 484 | **正式** | 正式发布，替代内部 ASM 依赖 |
| **JDK 26** | - | 持续优化 | 移除 ASM，统一使用 ClassFile API |

> **注**: ClassFile API 的首次预览 JEP 编号为 **457**（非 459）。JEP 459 为 String Templates 第二次预览。

---

## 3. OpenJDK 项目

### [Project Amber](../core/amber/)

Java 语言特性演进项目，由 Brian Goetz 领导。目标是通过较小的、面向生产力的语言特性增强 Java。

| 特性 | 预览版本 | 正式版本 | JEP |
|------|----------|----------|-----|
| var 关键字 | - | JDK 10 | JEP 286 |
| switch 表达式 | JDK 12 (JEP 325) | JDK 14 | JEP 361 |
| Text Blocks | JDK 13 (JEP 355) | JDK 15 | JEP 378 |
| Records | JDK 14 (JEP 359) | JDK 16 | JEP 395 |
| instanceof 模式 | JDK 14 (JEP 305) | JDK 16 | JEP 394 |
| Sealed Classes | JDK 15 (JEP 360) | JDK 17 | JEP 409 |
| switch 模式匹配 | JDK 17 (JEP 406) | JDK 21 | JEP 441 |
| Record Patterns | JDK 19 (JEP 405) | JDK 21 | JEP 440 |
| 未命名变量与模式 | JDK 21 (JEP 443) | JDK 22 | JEP 456 |
| 紧凑源文件 | JDK 21 (JEP 463) | JDK 25 | JEP 512 |
| 模块导入声明 | JDK 23 (JEP 476) | JDK 25 | JEP 511 |
| 灵活构造体 | JDK 22 (JEP 447) | JDK 25 | JEP 513 |
| 原始类型模式 | JDK 23 (JEP 455) | 预览中 | JEP 530 (JDK 26 第四预览) |
| String Templates | JDK 21 (JEP 430) | **已撤回** | JDK 23 移除 |

> [Amber 时间线](../core/amber/timeline.md)

---

## 4. 主题列表

### [Lambda 与 Stream](lambda/)

JDK 8 引入的函数式编程特性。

| 版本 | 主要变化 | JEP/JSR |
|------|----------|---------|
| JDK 8 | **Lambda 表达式** (JSR 335) | JSR 335 |
| JDK 8 | **Stream API** | - |
| JDK 8 | **方法引用** `Object::method` | JSR 335 |
| JDK 8 | **默认方法** 接口 default | JSR 335 |
| JDK 8 | **CompletableFuture** | - |
| JDK 9 | Stream 增强: takeWhile/dropWhile/ofNullable | - |
| JDK 10 | Collectors.toUnmodifiableList/Set/Map | - |
| JDK 16 | Stream.toList() | - |
| JDK 22 | Stream Gatherers (预览) | JEP 461 |
| JDK 24 | Stream Gatherers (正式) | JEP 485 |

> [Lambda 详情](lambda/) | [Stream 详情](streams/)

### [字符串处理](string/)

字符串相关优化和新特性。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 8 | StringJoiner | - |
| JDK 9 | **Compact Strings** (byte[] 存储) | JEP 254 |
| JDK 9 | **invokedynamic 字符串拼接** | JEP 280 |
| JDK 11 | repeat()、strip()、isBlank()、lines() | - |
| JDK 12 | indent()、transform() | - |
| JDK 15 | **Text Blocks** (正式) | JEP 378 |
| JDK 21 | String Templates (预览，后撤回) | JEP 430 |
| JDK 23 | String Templates 移除 | - |
| JDK 24 | 隐藏类拼接策略 (+40% 启动性能) | JDK-8336856 |
| JDK 26 | Integer/Long.toString 优化 | JDK-8370503 |

> [字符串优化时间线](string/timeline.md)

### [反射与元数据](reflection/)

反射、注解和字节码操作的演进。

| 版本 | 主要变化 | JEP/JSR |
|------|----------|---------|
| JDK 1.0 | 反射 API | - |
| JDK 5 | Annotations (JSR 175) | JSR 175 |
| JDK 6 | Pluggable Annotation Processing | JSR 269 |
| JDK 7 | MethodHandle (JSR 292) | JSR 292 |
| JDK 8 | Lambda invokedynamic, Parameter 反射 | - |
| JDK 11 | Constable/ConstantDesc | - |
| JDK 16 | Records | JEP 395 |
| JDK 22 | ClassFile API (预览) | JEP 457 |
| JDK 24 | ClassFile API (正式) | JEP 484 |

> [反射时间线](reflection/timeline.md)

### [ClassFile API](classfile/)

标准 class 文件读写 API，替代 ASM。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 22 | ClassFile API (预览) | JEP 457 |
| JDK 23 | ClassFile API (第二次预览) | JEP 466 |
| JDK 24 | ClassFile API (正式) | JEP 484 |

> [ClassFile API 时间线](classfile/timeline.md)

### [语法演进](syntax/)

语言语法从 JDK 1.0 到 JDK 26 的完整演进。

| 特性 | 引入版本 | 正式版本 | 说明 |
|------|----------|----------|------|
| 内部类 | JDK 1.1 | JDK 1.1 | 匿名类、成员类 |
| 断言 | JDK 1.4 | JDK 1.4 | assert 关键字 |
| 泛型 | JDK 5 | JDK 5 | 类型参数化 (JSR 14) |
| 枚举 | JDK 5 | JDK 5 | enum 关键字 |
| 变参 | JDK 5 | JDK 5 | T... |
| 注解 | JDK 5 | JDK 5 | @interface (JSR 175) |
| 增强 for | JDK 5 | JDK 5 | for (T : collection) |
| Diamond | JDK 7 | JDK 7 | `new ArrayList<>()` |
| try-with-resources | JDK 7 | JDK 7 | 自动资源管理 |
| Lambda | JDK 8 | JDK 8 | `(x) -> x + 1` (JSR 335) |
| 方法引用 | JDK 8 | JDK 8 | `Object::method` |
| 默认方法 | JDK 8 | JDK 8 | 接口 default 方法 |
| var | JDK 10 | JDK 10 | 局部变量类型推断 (JEP 286) |
| switch 表达式 | JDK 12 | JDK 14 | JEP 325 -> 354 -> 361 |
| Text Blocks | JDK 13 | JDK 15 | JEP 355 -> 368 -> 378 |
| Records | JDK 14 | JDK 16 | JEP 359 -> 384 -> 395 |
| instanceof 模式 | JDK 14 | JDK 16 | JEP 305 -> 375 -> 394 |
| Sealed Classes | JDK 15 | JDK 17 | JEP 360 -> 397 -> 409 |
| switch 模式匹配 | JDK 17 | JDK 21 | JEP 406 -> ... -> 441 |
| Record Patterns | JDK 19 | JDK 21 | JEP 405 -> 432 -> 440 |
| 未命名变量与模式 | JDK 21 | JDK 22 | JEP 443 -> 456 |
| 紧凑源文件 | JDK 21 | JDK 25 | JEP 463 -> ... -> 512 |
| 模块导入声明 | JDK 23 | JDK 25 | JEP 476 -> ... -> 511 |
| 灵活构造体 | JDK 22 | JDK 25 | JEP 447 -> ... -> 513 |
| 原始类型模式 | JDK 23 | 预览中 | JEP 455 -> 488 -> 507 -> 530 |

> [语法演进时间线](syntax/timeline.md)

### [注解与元编程](annotations/)

注解处理器、编译期元编程。

| 版本 | 主要变化 | JSR |
|------|----------|-----|
| JDK 5 | 注解引入 | JSR 175 |
| JDK 6 | Pluggable Annotation Processing API | JSR 269 |
| JDK 7 | 类型注解 | JSR 308 |
| JDK 8 | 重复注解 @Repeatable | - |
| JDK 17 | Sealed Classes 支持 | - |

> [注解时间线](annotations/timeline.md)

---

## 5. 核心贡献者

### 语言架构与设计

| 贡献者 | 公司 | 主要贡献 |
|--------|------|----------|
| **[Brian Goetz](/by-contributor/profiles/brian-goetz.md)** | Oracle | Java Language Architect, JSR-335 (Lambda), Project Amber 领导者 |
| **Gavin Bierman** | Oracle | Records, Sealed Classes, Pattern Matching 规范设计 |
| **Jim Laskey** | Oracle | String Templates, Text Blocks |
| **Alex Buckley** | Oracle | JLS 维护者, JSR-308 |

### 编译器 (按 Git 提交数)

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析 | **统计时间**: 2026-03-20

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | [Jan Lahoda](/by-contributor/profiles/jan-lahoda.md) | 98 | Oracle | javac, 模式匹配 |
| 2 | Vicente Romero | 52 | Oracle | javac, Records |
| 3 | Jonathan Gibbons | 43 | Oracle | javadoc, 注解 |
| 4 | Liam Miller-Cushon | 31 | Oracle | javac, Lambda |

### 字符串与性能

| 贡献者 | 公司 | 主要贡献 |
|--------|------|----------|
| **Aleksey Shipilev** | Oracle (JEP 254 时期) | JEP 254 (Compact Strings) |
| **Shaojin Wen** (温绍锦) | [Alibaba](/contributors/orgs/alibaba.md) | JDK-8336856 (+40% 启动), 25+ PR |
| **Claes Redestad** | [Oracle](/contributors/orgs/oracle.md) | String 压缩、字节码优化 |

### 反射与注解

| 贡献者 | 公司/机构 | 主要贡献 |
|--------|----------|----------|
| **Joshua Bloch** | Google/Sun | JSR 175 (注解), Effective Java |
| **Joseph Darcy** | Oracle | JSR 269 (注解处理器), Project Coin |
| **Michael Ernst** | UW | JSR 308 (类型注解), Checker Framework |

### 反射/元数据 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | 333 | Oracle | 类加载, 运行时 |
| 2 | David Holmes | 201 | Oracle | 并发, 线程 |
| 3 | [Ioi Lam](/by-contributor/profiles/ioi-lam.md) | 167 | Oracle | 反射, CDS |
| 4 | Serguei Spitsyn | 107 | Oracle | JVMTI, 反射 |

---

## 6. 按 JDK 版本索引

### JDK 5 (2004) - 语法革命

- **泛型** (JSR 14) -- 类型安全，消除强制转换
- **枚举** (enum) -- 类型安全的常量
- **注解** (JSR 175) -- 元数据机制
- **变参** (T...) -- 可变长参数
- **增强 for 循环** -- for-each 简化迭代
- **静态导入** -- import static
- **自动装箱/拆箱** -- int <-> Integer

### JDK 6 (2006)

- **注解处理器 API** (JSR 269) -- Pluggable Annotation Processing
- **Compiler API** (javax.tools) -- 编程式编译

### JDK 7 (2011) - Project Coin

- **Diamond 操作符** (`<>`) -- 类型推断简化
- **try-with-resources** -- 自动资源管理
- **多异常捕获** -- `catch (A | B e)`
- **二进制字面量** -- 0b1010
- **数字下划线** -- 1_000_000
- **switch 字符串** -- switch 支持 String
- **MethodHandle** (JSR 292) -- invokedynamic 基础设施

### JDK 8 (2014) - 函数式编程

- **Lambda 表达式** (JSR 335) -- `(x) -> x + 1`
- **方法引用** -- `Object::method`、`Class::new`
- **Stream API** -- 声明式数据处理管道
- **默认方法** -- 接口 default 方法
- **CompletableFuture** -- 异步编程
- **重复注解** (@Repeatable)
- **类型注解** (JSR 308)
- **参数反射** (Parameter 类)
- **StringJoiner** -- 字符串连接工具

### JDK 9 (2017) - 模块化与字符串

- **模块化** (JPMS, JSR 376) -- module-info.java
- **Compact Strings** (JEP 254) -- byte[] 存储，内存减少约 30-40%
- **invokedynamic 字符串拼接** (JEP 280) -- 替代 StringBuilder 字节码
- **私有接口方法** -- 接口 private 方法
- **Stream 增强** -- takeWhile, dropWhile, ofNullable
- **List/Set/Map.of()** -- 不可变集合工厂方法

### JDK 10 (2018)

- **局部变量类型推断** (var, JEP 286) -- `var name = "Alice";`

### JDK 11 (2018) LTS

- **字符串新方法**: repeat(), strip(), isBlank(), lines()
- **HTTP Client** (JEP 321) -- 标准化
- **Constable/ConstantDesc** -- 常量描述 API

### JDK 12-13 (2019)

- **switch 表达式** (JEP 325/354, 预览)
- **Text Blocks** (JEP 355, 预览)
- **字符串方法**: indent(), transform()

### JDK 14 (2020) - 表达式增强

- **switch 表达式** (JEP 361, **正式**)
- **Records** (JEP 359, 预览)
- **instanceof 模式匹配** (JEP 305, 预览)

### JDK 15 (2020) - 文本处理

- **Text Blocks** (JEP 378, **正式**) -- `"""..."""`
- **Sealed Classes** (JEP 360, 预览)
- **Records** (JEP 384, 第二次预览)

### JDK 16 (2021) - 数据建模

- **Records** (JEP 395, **正式**) -- 不可变数据类
- **instanceof 模式匹配** (JEP 394, **正式**) -- `obj instanceof String s`
- **Sealed Classes** (JEP 397, 第二次预览)
- **Stream.toList()** -- 简化收集

### JDK 17 (2021) LTS - 继承控制

- **Sealed Classes** (JEP 409, **正式**) -- 密封类/接口
- **Pattern Matching for switch** (JEP 406, 预览)

### JDK 18-20 (2022-2023)

- **switch 模式匹配** (JEP 420/427/433, 持续预览)
- **Record Patterns** (JEP 405/432, 预览)

### JDK 21 (2023) LTS - 模式匹配成熟

- **switch 模式匹配** (JEP 441, **正式**)
- **Record Patterns** (JEP 440, **正式**)
- **未命名模式和变量** (JEP 443, 预览)
- **String Templates** (JEP 430, 预览 -- 后撤回)

### JDK 22 (2024) - 未命名模式

- **未命名变量与模式** (JEP 456, **正式**) -- `_` 占位符
- **ClassFile API** (JEP 457, 预览)
- **String Templates** (JEP 459, 第二次预览 -- 后撤回)
- **Stream Gatherers** (JEP 461, 预览)

### JDK 23 (2024)

- **ClassFile API** (JEP 466, 第二次预览)
- **原始类型模式** (JEP 455, 预览)
- **String Templates 移除** -- 因设计问题被撤回

### JDK 24 (2025)

- **ClassFile API** (JEP 484, **正式**) -- 替代内部 ASM
- **原始类型模式** (JEP 488, 第二次预览)
- **Stream Gatherers** (JEP 485, **正式**)
- **隐藏类拼接策略** (JDK-8336856) -- +40% 启动性能

### JDK 25 (2025) LTS - 语法最终化

- **紧凑源文件** (JEP 512, **正式**) -- `void main() {}`
- **模块导入声明** (JEP 511, **正式**) -- `import module java.base;`
- **灵活构造体** (JEP 513, **正式**) -- 构造方法前可执行语句
- **原始类型模式** (JEP 507, 第三次预览)

### JDK 26 (2026-03-17) - 持续演进

- **原始类型模式** (JEP 530, 第四次预览) -- primitive patterns
- **Lazy Constants** (JEP 526, 第二次预览) -- 延迟初始化常量
- **G1 同步优化** (JEP 521) -- 减少同步开销，吞吐量提升
- **HTTP/3** (JEP 517) -- HTTP Client API 支持 HTTP/3
- **AOT 对象缓存** (JEP 516) -- 跨 GC 实现的 AOT 缓存
- **Prepare to Make Final Mean Final** (JEP 500)
- **移除 Applet API** (JEP 504)
- **Integer/Long.toString 优化** (JDK-8370503)

---

## 7. 内部开发者资源

### 源码结构

```
src/java.base/share/classes/java/lang/
├── String.java              # 字符串核心 (Compact Strings, JEP 254)
├── StringBuilder.java       # 可变字符串
├── Record.java              # 记录类基类 (JDK 16+)
├── Enum.java                # 枚举基类
├── invoke/                  # invokedynamic 相关
│   ├── StringConcatFactory.java   # JEP 280 字符串拼接
│   ├── LambdaMetafactory.java     # Lambda 元工厂
│   └── MethodHandle.java
└── reflect/                 # 反射 API

src/java.base/share/classes/java/lang/classfile/
└── ClassFile.java           # ClassFile API (JEP 484)

src/jdk.compiler/share/classes/com/sun/tools/javac/
├── comp/                    # 编译器核心
├── parser/                  # 语法解析
└── tree/                    # AST 节点

src/java.compiler/share/classes/javax/annotation/processing/
└── Processor.java           # 注解处理器接口 (JSR 269)
```

### 关键内部类

| 类 | 作用 | 访问级别 |
|---|------|----------|
| `StringLatin1` | LATIN1 编码操作 (JEP 254) | 包级私有 |
| `StringUTF16` | UTF16 编码操作 (JEP 254) | 包级私有 |
| `StringConcatHelper` | 拼接辅助方法 (JEP 280) | `@ForceInline` |
| `LambdaMetafactory` | Lambda 元工厂 (JSR 335) | 内部 API |
| `ConstantBootstraps` | invokedynamic 引导方法 | 内部 API |
| `InnerClassLambdaMetafactory` | Lambda 内部实现 | 内部 API |

### VM 参数速查

```bash
# 字符串相关
-XX:+CompactStrings           # 启用压缩字符串 (JEP 254, 默认开启)
-XX:+UseStringDeduplication    # 启用字符串去重 (G1/ZGC)
-XX:StringDeduplicationAgeThreshold=3

# Lambda/invokedynamic
-Djdk.invoke.LambdaMetafactory.dumpProxyClassFiles=true

# 注解处理器
-processor <类名>             # 指定注解处理器
-proc:only                    # 仅处理注解，不编译

# ClassFile API (JDK 22-23 预览阶段)
--enable-preview              # 启用预览特性
```

### 常用调试工具

```bash
# javac 详细输出
javac -Xprint:Round           # 打印注解处理轮次
javac -Xlint:unchecked        # 未检查转换警告
javac -XDshouldStopPolicy=FLOW  # 显示编译流程

# 字符串拼接策略
-Djava.lang.invoke.stringConcat=MH_INLINE_SIZED_EXACT  # JEP 280 策略

# 查看生成的 Lambda 类
-Djdk.internal.lambda.dumpProxyClasses=<目录>
```

---

## 8. 统计数据

| 指标 | 数值 |
|------|------|
| 语言特性 JEP (JDK 8-26) | 60+ |
| JSR 规范 (语言相关) | 10+ (JSR 14/175/269/292/308/335/376 等) |
| 新增关键字 | enum (JDK 5), assert (JDK 1.4); var/record/sealed/yield 为受限标识符 |
| 新增运算符 | `::` (方法引用), `->` (Lambda/switch) |
| 经预览后正式化的特性 | 15+ (Records, Sealed, switch 模式等) |
| 经预览后撤回的特性 | 1 (String Templates) |
| Project Amber 已交付正式特性 | 12+ |

---

## 9. 学习路径

1. **入门**: [字符串处理](string/) -- 日常开发必备 (Compact Strings, Text Blocks)
2. **函数式**: [Lambda 与 Stream](lambda/) -- JDK 8 函数式编程基础
3. **现代语法**: [语法演进](syntax/) -- Records, Sealed, 模式匹配
4. **深入**: [反射与元数据](reflection/) -- [注解与元编程](annotations/) -- 元编程能力
5. **字节码**: [ClassFile API](classfile/) -- JDK 24 正式版，替代 ASM

---

**最后更新**: 2026-03-22
