# JIT 编译演进时间线

> 从解释器到分层编译、Graal JIT 的完整演进历程

[← 返回 JIT 编译](../)

---
## 目录

1. [时间线概览](#1-时间线概览)
2. [JIT 编译基础概念](#2-jit-编译基础概念)
3. [JDK 1.0 - JDK 1.2: 纯解释时代](#3-jdk-10---jdk-12-纯解释时代)
4. [JDK 1.2 - JDK 1.3: JIT 萌芽](#4-jdk-12---jdk-13-jit-萌芽)
5. [JDK 5 - JDK 6: 编译器分离与优化](#5-jdk-5---jdk-6-编译器分离与优化)
6. [JDK 7 - JDK 8: 编译器增强](#6-jdk-7---jdk-8-编译器增强)
7. [JDK 9 - JDK 10: 模块化与 Graal](#7-jdk-9---jdk-10-模块化与-graal)
8. [JDK 11 - JDK 16: Graal JIT 与优化](#8-jdk-11---jdk-16-graal-jit-与优化)
9. [JDK 17 - JDK 20: 长期支持版本优化](#9-jdk-17---jdk-20-长期支持版本优化)
10. [JDK 21 - JDK 26: 现代编译器](#10-jdk-21---jdk-26-现代编译器)
11. [编译器对比](#11-编译器对比)
12. [相关链接](#12-相关链接)

---


## 1. 时间线概览

```
JDK 1.0 ─── JDK 1.3 ─── JDK 5 ─── JDK 6 ─── JDK 9 ─── JDK 17 ─── JDK 21 ─── JDK 23 ─── JDK 26
   │          │        │        │        │        │        │        │        │
纯解释    C2       C1/C2   分层    Graal   JIT    模式     SuperWord  成本
(慢启动)   Server   分离    编译    JIT     优化    匹配     向量化    模型
          (高性能)  编译    Tiered  (实验)  性能   优化     (正式)   (集成)
```

---

## 2. JIT 编译基础概念

### 编译器分层

```
┌─────────────────────────────────────────────────────────┐
│                    JIT 编译器分层                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Level 0: 解释器 (Interpreter)                          │
│           ├── 字节码直接执行                              │
│           ├── 启动快，执行慢                              │
│           └── 收集 profiling 信息                           │
│                                                         │
│  Level 1-3: C1 (Client Compiler)                          │
│           ├── 快速编译，优化少                             │
│           ├── 生成优化代码                                │
│           └── 收集 profiling 信息                           │
│                                                         │
│  Level 4: C2 (Server Compiler)                           │
│           ├── 编译慢，深度优化                             │
│           ├── 内联、逃逸分析、循环优化                      │
│           └── 基于激进优化                                 │
│                                                         │
│  Graal JIT (可选)                                        │
│           ├── 基于 Java 的编译器                           │
│           ├── 更激进的优化                                │
│           └── 支持 Truffle 语言                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 编译性能指标

| 指标 | 说明 | 目标值 |
|------|------|--------|
| **启动时间** | 首次执行预热时间 | < 1s |
| **峰值性能** | 长期运行吞吐量 | 最大化 |
| **内存占用** | 代码缓存大小 | < 240MB |
| **编译暂停** | 编译造成的 GC 暂停 | 最小化 |

---

## 3. JDK 1.0 - JDK 1.2: 纯解释时代

### JDK 1.0 (1996)

```
特点: 纯解释执行
优势: 快速启动，跨平台
劣势: 执行效率低
```

- 字节码解释器
- 无 JIT 编译
- 适合 Applet 小程序

### JDK 1.1 (1997)

- JDBC 内省支持
- 反射 API
- 仍然纯解释执行

---

## 4. JDK 1.2 - JDK 1.3: JIT 萌芽

### JDK 1.2 (1998)

- Classic VM 引入
- 内存布局改进
- 性能提升约 2-3x

### JDK 1.3 (2000)

**HotSpot VM 首次引入 JIT**

```
┌─────────────────────────────────────────────────────────┐
│                    HotSpot 1.0                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Client Compiler (C1)                                  │
│  ├── 针对客户端应用                                     │
│  ├── 快速编译，简单优化                                 │
│  └── -client 参数选择                                   │
│                                                         │
│  Server Compiler (C2)                                  │
│  ├── 针对服务器应用                                     │
│  ├── 深度优化，自适应编译                               │
│  └── -server 参数选择 (默认)                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**C2 关键优化**:
- 方法内联
- 循环优化
- 逃逸分析
- 全局值编号

---

## 5. JDK 5 - JDK 6: 编译器分离与优化

### JDK 5 (2004) - Tiger

**Server 2.0 架构**

- C1/C2 完全分离
- -client/-server 参数
- 自适应优化 (On Stack Replacement, OSR)

```bash
# 客户端模式
java -client MyApp

# 服务器模式 (默认)
java -server MyApp
```

**JIT 优化改进**:
- 类型 profiling 改进
- 分支预测优化
- 寄存器分配优化

### JDK 6 (2006) - Mustang

**分层编译 (Tiered Compilation) 引入**

```
Level 0 → Level 1 → Level 2 → Level 3 → Level 4
  ↑          ↑         ↑         ↑         ↑
解释器    C1      C1      C1       C2
        (profiling) (profiling) (profiling) (优化)
```

**优势**:
- 快速启动 (C1 快速编译)
- 高峰值性能 (C2 深度优化)
- 自动平衡编译成本

---

## 6. JDK 7 - JDK 8: 编译器增强

### JDK 7 (2011)

**InvokeDynamic 支持**

```java
// invokedynamic 字节码指令
// 动态语言支持基础
// 为 Lambda 表达式做准备
```

### JDK 8 (2014) - Lambda 时代

**Lambda 编译优化**

```java
// Lambda 表达式编译
// 使用 invokedynamic + LambdaMetafactory
List<String> list = Arrays.asList("a", "b", "c");
list.forEach(s -> System.out.println(s));
```

**编译改进**:
- Lambda 表达式优化
- 默认方法支持
- 类型注解支持

---

## 7. JDK 9 - JDK 10: 模块化与 Graal

### JDK 9 (2017)

**JVMCI (JVM Compiler Interface)**

- JEP 243: JVM Compiler Interface
- 允许第三方 JIT 编译器
- Graal JIT 实验性引入

### JDK 10 (2018)

**G1GC 成为默认**

- 为 JIT 提供更好的 GC 支持
- 降低 GC 暂停对编译的影响

---

## 8. JDK 11 - JDK 16: Graal JIT 与优化

### JDK 11 (2018)

**Graal JIT 实验性**

```
启用 Graal JIT:
-XX:+UnlockExperimentalVMOptions
-XX:+UseJVMCICompiler
```

**特性**:
- 基于 Java 编写
- 更激进的优化
- 支持 Truffle 语言实现

### JDK 14-16 (2020-2021)

**编译器改进**

- **JDK 14**: NullPointerException 增强 (JEP 358) - 更好的错误消息
- **JDK 15**: 文本字符串 (JEP 378) - 编译时字符串优化
- **JDK 16**: Pattern Matching for instanceof (JEP 394) - 编译器优化模式匹配

**注意**: Record (JDK 14) 是语言特性，主要在 javac 编译器处理，不属于 JIT 运行时优化

---

## 9. JDK 17 - JDK 20: 长期支持版本优化

### JDK 17 (2021) - LTS

**Pattern Matching for instanceof (JEP 394)**

```java
// 编译器优化模式匹配
if (obj instanceof String s) {
    System.out.println(s.toUpperCase());
}
```

**Sealed Classes (JEP 409)**

- 编译器类型检查
- 优化继承层次

### JDK 18-20 (2022-2023)

**Vector API (JEP 338, 417, 426)**

- SIMD 向量化支持
- 编译器自动向量化优化
- 性能提升 2-8x (特定场景)

---

## 10. JDK 21 - JDK 26: 现代编译器

### JDK 21 (2023) - LTS

**Record Patterns (JEP 440)**

```java
// 模式匹配优化
if (obj instanceof Point(int x, int y)) {
    System.out.println("x=" + x + ", y=" + y);
}
```

**String Templates (JEP 430)**

- 编译时字符串模板优化
- 后续版本中撤回

### JDK 22-23 (2024)

**编译器稳定性**

- C2 性能修复
- 编译吞吐量提升
- 内存占用优化

### JDK 24-26 (2025-2026)

**SuperWord 成本模型 (JEP 455, JDK-8340093)**

- 智能向量化决策
- 小循环向量化优化
- 性能提升 10-30%

**StringBuilder 优化**

```java
// JDK 24: 隐藏类拼接
// JDK 25: StringBuilder.append(char) 优化
// 性能提升 15-40%
```

**其他改进**

- G1 GC Claim Table 优化 (+10-20% 吞吐量)
- JIT 编译队列改进
- 代码缓存管理优化

---

## 11. 编译器对比

| 编译器 | 版本 | 启动时间 | 峰值性能 | 适用场景 |
|--------|------|----------|----------|----------|
| **解释器** | 1.0+ | 快 | 低 | 应用启动、冷代码 |
| **C1** | 1.3+ | 中 | 中 | 桌面应用、短时运行 |
| **C2** | 1.3+ | 慢 | 高 | 长期运行的服务器应用 |
| **Graal** | 11+ | 慢 | 高 | 特定优化场景 |

---

## 12. 相关链接

### 本地文档

- [C2 优化阶段](c2-phases.md) - 15 个编译阶段详解
- [VM 参数](vm-parameters.md) - JIT 参数配置
- [诊断工具](diagnostics.md) - 编译器调试
- [近期改进](recent-changes.md) - 2024-2025 更新
- [StringBuilder 优化 PR](/by-pr/8355/8355177.md) - Unsafe.copyMemory 优化
- [String 构造函数优化](/by-version/jdk26/deep-dive/string-constructor-optimization.md) - JIT 内联优化

### 外部参考

**JEP 文档:**
- [JEP 243](/jeps/performance/jep-243.md)
- [JEP 244](/jeps/performance/jep-244.md)

**技术博客:**
- [HotSpot JIT Compiler](https://wiki.openjdk.org/display/HotSpot/)
- [Tiered Compilation in HotSpot](https://blogs.oracle.com/jonthecryptist/entry/tiered_compilation_in_hotspot)

---

**最后更新**: 2026-03-21
