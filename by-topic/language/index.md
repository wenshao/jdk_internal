# 语言特性

语法、类型、反射等语言层面演进。

[← 返回主题索引](../)

---

## 演进概览

```
JDK 1.0 ─── JDK 5 ─── JDK 8 ─── JDK 14-17 ─── JDK 21-26
   │           │           │            │              │
 基础语法    泛型/注解    Lambda      Records       模式匹配
 反射        变参        invokedynamic  Sealed        String Templates
             枚举        Stream        隐式类         分代 ZGC
```

### 版本里程碑

| 版本 | 主题 | 关键特性 |
|------|------|----------|
| **JDK 5** | 语法革命 | 泛型、枚举、注解、变参、增强 for |
| **JDK 8** | 函数式 | Lambda、Stream、invokedynamic |
| **JDK 11 LTS** | 模块化成熟 | Compact Strings、var、HttpClient |
| **JDK 17 LTS** | 模式匹配 | Records、Sealed Classes、switch 表达式 |
| **JDK 21 LTS** | 并发增强 | 虚拟线程、分代 ZGC、String Templates |
| **JDK 26** | 性能优化 | G1 +10-20%、ZGC NUMA、Primitive Patterns |

---

## 主题列表

### [字符串处理](string/)

字符串相关优化和新特性。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 8 | StringJoiner | - |
| JDK 9 | **Compact Strings** (JEP 254)、invokedynamic 拼接 (JEP 280) | JEP 254, JEP 280 |
| JDK 11 | repeat()、strip()、isBlank()、lines() | - |
| JDK 15 | **Text Blocks** (正式) | JEP 378 |
| JDK 21 | String Templates (预览，后撤回) | JEP 430 |
| JDK 23 | String Templates 移除 | - |
| JDK 24 | 隐藏类拼接策略 (+40% 启动性能) | JDK-8336856 |
| JDK 26 | Integer/Long.toString 优化 | JDK-8370503 |

→ [字符串优化时间线](string/timeline.md)

### [反射与元数据](reflection/)

反射、注解和字节码操作的演进。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 1.0 | 反射 API | - |
| JDK 5 | Annotations (JSR 175) | JSR 175 |
| JDK 6 | Pluggable Annotation Processing | JSR 269 |
| JDK 7 | MethodHandle (JSR 292) | JSR 292 |
| JDK 8 | Lambda invokedynamic, Parameter 反射 | - |
| JDK 11 | Constable/ConstantDesc | - |
| JDK 16 | ClassFile API | JEP 395 |
| JDK 22 | Class-File API (预览) | JEP 459 |
| JDK 24 | Class-File API (正式) | JEP 484 |
| JDK 26 | Mirror API | - |

→ [反射时间线](reflection/timeline.md)

### [Class File API](classfile/)

标准 class 文件读写 API，替代 ASM。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 22 | Class-File API (预览) | JEP 459 |
| JDK 23 | Class-File API (第二次预览) | JEP 466 |
| JDK 24 | Class-File API (正式) | JEP 484 |

→ [Class File API 时间线](classfile/timeline.md)

### [语法演进](syntax/)

语言语法从 JDK 1.0 到 JDK 26 的完整演进。

| 特性 | 引入版本 | 说明 |
|------|----------|------|
| 内部类 | JDK 1.1 | 匿名类、成员类 |
| 断言 | JDK 1.4 | assert |
| 泛型 | JDK 5 | 类型参数化 |
| 枚举 | JDK 5 | enum |
| 变参 | JDK 5 | T... |
| 注解 | JDK 5 | @interface |
| 增强 for | JDK 5 | for (T : collection) |
| Lambda | JDK 8 | → 表达式 |
| 方法引用 | JDK 8 | Object::method |
| var | JDK 10 | 局部变量类型推断 |
| Records | JDK 16 | 不可变数据类 |
| instanceof 模式 | JDK 16 | obj instanceof Type t |
| Sealed Classes | JDK 17 | 密封类 |
| switch 模式 | JDK 21 | case Type t → ... |
| String Templates | JDK 21+ | STR."\{value}" |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 语言/编译器 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | [Jan Lahoda](/by-contributor/profiles/jan-lahoda.md) | 98 | Oracle | javac, 模式匹配 |
| 2 | Vicente Romero | 52 | Oracle | javac, Records |
| 3 | Jonathan Gibbons | 43 | Oracle | javadoc, 注解 |
| 4 | Liam Miller-Cushon | 31 | Oracle | javac, Lambda |

### 反射/元数据 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | 333 | Oracle | 类加载, 运行时 |
| 2 | David Holmes | 201 | Oracle | 并发, 线程 |
| 3 | [Ioi Lam](/by-contributor/profiles/ioi-lam.md) | 167 | Oracle | 反射, CDS |
| 4 | Serguei Spitsyn | 107 | Oracle | JVMTI, 反射 |
| 隐式类 | JDK 25 | void main() {} |

→ [语法演进时间线](syntax/timeline.md)

### [注解与元编程](annotations/)

注解处理器、编译期元编程。

| 版本 | 主要变化 | JSR |
|------|----------|-----|
| JDK 5 | 注解引入 | JSR 175 |
| JDK 6 | Pluggable Annotation Processing API | JSR 269 |
| JDK 7 | 类型注解 | JSR 308 |
| JDK 8 | 重复注解 @Repeatable | - |
| JDK 17 | Sealed Classes 支持 | - |

→ [注解时间线](annotations/timeline.md)

### [Class File API](classfile/)

标准 class 文件读写 API。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 22 | Class-File API (预览) | JEP 459 |
| JDK 23 | Class-File API (第二次预览) | JEP 466 |
| JDK 24 | Class-File API (正式) | JEP 484 |

→ [Class File API 时间线](classfile/timeline.md)

| 版本 | 主要变化 | JSR |
|------|----------|-----|
| JDK 5 | 注解引入 | JSR 175 |
| JDK 6 | Pluggable Annotation Processing API | JSR 269 |
| JDK 7 | 类型注解 | JSR 308 |
| JDK 8 | 重复注解 @Repeatable | - |
| JDK 17 | Sealed Classes 支持 | - |

→ [注解时间线](annotations/timeline.md)

---

## 核心贡献者

### 语法与类型

| 贡献者 | 公司 | 主要贡献 |
|--------|------|----------|
| **[Brian Goetz](/by-contributor/profiles/brian-goetz.md)** | Oracle | Java Language Architect, JSR-335 (Lambda) |
| **Gavin Bierman** | Oracle | Records, Sealed Classes, Pattern Matching |
| **Jim Laskey** | Oracle | String Templates, Text Blocks |
| **Alex Buckley** | Oracle | JLS 维护者, JSR-308 |

### 字符串与性能

| 贡献者 | 公司 | 主要贡献 |
|--------|------|----------|
| **Aleksey Shipilev** | [Red Hat](/contributors/orgs/redhat.md) | JEP 254 (Compact Strings) |
| **Shaojin Wen** (温绍锦) | [Alibaba](/contributors/orgs/alibaba.md) | JDK-8336856 (+40% 启动), 25+ PR |
| **Claes Redestad** | [Oracle](/contributors/orgs/oracle.md) | String 压缩、字节码优化 |

### 反射与注解

| 贡献者 | 公司/机构 | 主要贡献 |
|--------|----------|----------|
| **Joshua Bloch** | Google/Sun | JSR 175 (注解), 《Effective Java》 |
| **Joseph Darcy** | Oracle | JSR 269 (注解处理器), Project Coin |
| **Michael Ernst** | UW | JSR 308 (类型注解), Checker Framework |

---

## 按 JDK 版本索引

### JDK 5 (2004) - 语法革命

- **泛型** (JSR 14)
- **枚举** (enum)
- **注解** (JSR 175)
- **变参** (T...)
- **增强 for 循环**
- **静态导入**
- **自动装箱/拆箱**

### JDK 6 (2006)

- **注解处理器 API** (JSR 269)
- **Compiler API** (javax.tools)

### JDK 7 (2011)

- **Diamond 操作符** (`<>`)
- **Try-with-resources**
- **多异常捕获**
- **二进制字面量**
- **字面串下划线**
- **switch 字符串**
- **MethodHandle** (JSR 292)

### JDK 8 (2014) - 函数式编程

- **Lambda 表达式**
- **方法引用**
- **Stream API**
- **CompletableFuture**
- **invokedynamic 字符串拼接**
- **重复注解** (@Repeatable)
- **类型注解** (JSR 308)
- **参数反射** (Parameter)

### JDK 9 (2017)

- **Compact Strings** (JEP 254)
- **私有接口方法**
- **模块化** (JPMS)

### JDK 10 (2018)

- **局部变量类型推断** (var)

### JDK 11 (2018) LTS

- **字符串新方法**: repeat(), strip(), isBlank(), lines()
- **HTTP Client**
- **Constable/ConstantDesc**

### JDK 14-16 (2020-2021)

- **Records** (JEP 395, JDK 16 正式)
- **instanceof 模式匹配** (JEP 394, JDK 16 正式)
- **Text Blocks** (JEP 378, JDK 15 正式)
- **switch 表达式** (JEP 361, JDK 14 正式)

### JDK 17 (2021) LTS

- **Sealed Classes** (JEP 409)
- **Pattern Matching for switch** (预览)
- **Record Patterns** (预览)

### JDK 21 (2023) LTS

- **String Templates** (JEP 430, 预览)
- **Record Patterns** (正式)
- **Pattern Matching for switch** (正式)
- **未命名模式和变量** (JEP 443)
- **隐式类** (JEP 469)

### JDK 24-26 (2025-2026)

- **隐藏类拼接策略** (JDK-8336856, +40% 启动)
- **分代 ZGC** (JDK 21+, JDK 23 默认)
- **Primitive Patterns** (JEP 455)
- **G1 吞吐量提升** (JEP 522, +10-20%)

---

## 内部开发者资源

### 源码结构

```
src/java.base/share/classes/java/lang/
├── String.java              # 字符串核心
├── StringBuilder.java       # 可变字符串
├── Record.java              # 记录类注解
├── Enum.java                # 枚举基类
├── invoke/                  # invokedynamic 相关
│   ├── StringConcatFactory.java
│   └── MethodHandle.java
└── reflect/                 # 反射 API

src/java.base/share/classes/java/lang/compiler/
├── SyntaxException.java     # 语法异常
└── └── 相关编译器 API

src/java.compiler/share/classes/javax/annotation/processing/
├── Processor.java           # 注解处理器接口
└── └── 相关工具类
```

### 关键内部类

| 类 | 作用 | 访问级别 |
|---|------|----------|
| `StringLatin1` | LATIN1 编码操作 | 包级私有 |
| `StringUTF16` | UTF16 编码操作 | 包级私有 |
| `StringConcatHelper` | 拼接辅助方法 | `@ForceInline` |
| `LambdaMetafactory` | Lambda 元工厂 | 内部 API |
| `ConstantBootstraps` | invokedynamic 引导 | 内部 API |

### VM 参数速查

```bash
# 字符串相关
-XX:+CompactStrings           # 启用压缩字符串 (默认)
-XX:+UseStringDeduplication    # 启用字符串去重
-XX:StringDeduplicationAgeThreshold=3

# Lambda/invokedynamic
-Djdk.invoke.LambdaMetafactory.dumpProxyClassFiles=true

# 注解处理器
-processor <类名>             # 指定注解处理器
-proc:only                    # 仅处理注解，不编译

# 泛型/类型
-XX:+TypeProfileGCLevel       # 类型 profiling 级别
```

### 常用调试工具

```bash
# javac 详细输出
javac -Xprint:Round           # 打印注解处理轮次
javac -Xlint:unchecked        # 未检查转换警告

# jdk.internal.misc.VM
VM.getFinalRefCount()         # Finalizer 引用计数
VM.latestUserDefinedLoader()  # 最新类加载器
```

---

## 统计数据

| 指标 | 数值 |
|------|------|
| 语言特性 JEP (JDK 5-26) | 45+ |
| JSR 规范 | 10+ |
| 新增关键字 | 3 (enum, assert, var) |
| 新增运算符 | 2 (::, ->) |
| 新增注解 | 8+ |

---

## 学习路径

1. **入门**: [字符串处理](string/) → 日常开发必备
2. **进阶**: [语法演进](syntax/) → 掌握现代 Java 语法
3. **深入**: [反射与元数据](reflection/) → [注解与元编程](annotations/) → 元编程能力
