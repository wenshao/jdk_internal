# GraalVM 术语表

> GraalVM 相关术语和缩略语解释

[← 返回 GraalVM 首页](./)

---
## 目录

1. [A](#1-a)
2. [B](#2-b)
3. [C](#3-c)
4. [D](#4-d)
5. [E](#5-e)
6. [F](#6-f)
7. [G](#7-g)
8. [H](#8-h)
9. [I](#9-i)
10. [J](#10-j)
11. [L](#11-l)
12. [N](#12-n)
13. [O](#13-o)
14. [P](#14-p)
15. [S](#15-s)
16. [T](#16-t)
17. [V](#17-v)
18. [缩略语速查](#18-缩略语速查)
19. [相关资源](#19-相关资源)

---


## 1. A

### AOT (Ahead-Of-Time Compilation)
**提前编译**。在程序运行之前将字节码编译为机器码。与 JIT 相对。

**优势**: 启动快，无需 JIT 预热
**劣势**: 无法进行运行时优化

参见：[Native Image](#native-image)

### AST (Abstract Syntax Tree)
**抽象语法树**。编程语言代码的树状表示形式。

```
示例：表达式 "1 + 2" 的 AST
     +
    / \
   1   2
```

---

## 2. B

### Bytecode
**字节码**。Java 编译器生成的中间代码格式 (.class 文件)。

---

## 3. C

### C1 Compiler
HotSpot 的**客户端编译器**，优化编译速度，适合启动敏感场景。

### C2 Compiler
HotSpot 的**服务端编译器**，优化峰值性能，适合长运行服务。

### CE (Community Edition)
GraalVM **社区版**，免费开源版本。

### Closed World Assumption
**闭世界假设**。假设构建时已知所有代码，运行时不会加载新类。Native Image 基于此假设。

对比：[Open World](#open-world)

---

## 4. D

### Deoptimization
**去优化**。当优化假设失效时，从优化的代码回退到未优化版本的过程。

**触发场景**:
- 类型假设错误
- 内联失效
- 边界检查失效

---

## 5. E

### EE (Enterprise Edition)
GraalVM **企业版** (已于 2023 年 6 月停产)。原 EE 功能已合并到免费的 Oracle GraalVM (GFTC 许可) 中。

### Escape Analysis
**逃逸分析**。分析对象的作用范围，判断是否可以标量替换。

**逃逸级别**:
- NoEscape: 对象未逃逸
- ArgEscape: 对象作为参数传递
- GlobalEscape: 对象逃逸到全局

---

## 6. F

### Fixed Node
Graal IR 中的**固定节点**，有控制流依赖的节点（如方法调用、返回）。

对比：[Floating Node](#floating-node)

### Floating Node
Graal IR 中的**浮动节点**，仅数据流依赖的节点（如加法、加载）。

---

## 7. G

### GC (Garbage Collection)
**垃圾回收**。自动内存管理机制。

Native Image 支持的 GC:
- Serial GC
- G1 GC
- Epsilon (无 GC)

### Graal JIT
用 Java 编写的高性能**JIT 编译器**，可替代 HotSpot C2。

### GraalVM
Oracle Labs 开发的高性能 JDK 发行版。

**核心特性**:
- Graal JIT 编译器
- Native Image (AOT)
- Truffle 框架

### GFTC (GraalVM Free Terms and Conditions)
Oracle GraalVM 的许可协议。自 2023 年 6 月起，原 Enterprise Edition 合并为 Oracle GraalVM，在 GFTC 下免费使用 (包括生产环境)。

---

## 8. H

### HotSpot VM
Oracle JDK 和 OpenJDK 的默认 JVM 实现。

**组件**:
- C1 编译器
- C2 编译器 (使用 Sea of Nodes "Ideal" IR)
- GC (G1, ZGC, Shenandoah)

---

## 9. I

### Inlining
**内联**。将被调用方法的代码直接插入到调用处，消除调用开销。

### IR (Intermediate Representation)
**中间表示**。编译器内部使用的代码表示形式。

---

## 10. J

### JIT (Just-In-Time Compilation)
**即时编译**。在程序运行时将字节码编译为机器码。

对比：[AOT](#aot)

### JNI (Java Native Interface)
**Java 本地接口**。Java 与其他语言（如 C/C++）交互的接口。

### JVMCI (JVM Compiler Interface)
**JVM 编译器接口** (JEP 243)。允许 Java 编写的编译器（如 Graal）集成到 HotSpot。

---

## 11. L

### LIR (Low Level IR)
**低级中间表示**。接近机器码的中间表示。

### LLVM (Low Level Virtual Machine)
编译器基础设施项目。GraalVM 通过 Sulong 支持 LLVM bitcode。

---

## 12. N

### Native Image
GraalVM 的**AOT 编译技术**，将 Java 应用编译为原生可执行文件。

**特点**:
- 启动快 (毫秒级)
- 内存少 (70-80% 减少)
- 无需 JVM

### Nashorn
JDK 8 引入的 JavaScript 引擎，JDK 15 移除。

**替代方案**: GraalJS

---

## 13. O

### Open World
**开世界假设**。假设运行时可能加载任何类。传统 JVM 采用此假设。

对比：[Closed World](#closed-world-assumption)

### OSR (On-Stack Replacement)
**栈上替换**。在方法执行过程中从解释器切换到编译代码的技术。

---

## 14. P

### Partial Escape Analysis
**部分转逸分析**。Graal 的逃逸分析技术，比 C2 更精确。

**优势**: 更多标量替换机会，减少堆分配

### PGO (Profile-Guided Optimization)
**剖面引导优化**。基于运行时 profile 信息进行优化。

**流程**:
1. 插桩编译
2. 运行工作负载
3. 使用 profile 重新编译

**效果**: 性能提升 10-15%

### Polyglot
**多语言**。GraalVM 支持在同一个运行时上运行多种语言。

**支持的语言**:
- Java
- JavaScript (GraalJS)
- Python (GraalPython)
- Ruby (TruffleRuby)
- R (FastR)
- LLVM

---

## 15. S

### Sea of Nodes
Graal 编译器的**中间表示**，统一数据流和控制流的图结构。

**特点**:
- 数据流和控制流统一
- 优化更精确
- 支持激进内联

### Scalar Replacement
**标量替换**。将对象替换为其字段，消除堆分配。

```java
// 优化前
Point p = new Point(1, 2);
return p.x + p.y;

// 优化后 (标量替换)
int x = 1;
int y = 2;
return x + y;
```

### Speculative Optimization
**推测优化**。基于运行时 profiling 做激进优化假设。

**示例**:
- 类型推测
- 内联推测
- 空值推测

---

## 16. T

### Truffle
语言实现框架，简化 JVM 语言的实现。

**特点**:
- AST 解释器
- 自动优化
- 多语言支持

### TruffleRuby
基于 Truffle 的 Ruby 实现。

**性能**: 比 MRI 快 5-10 倍

---

## 17. V

### Virtual Threads
**虚拟线程**。JDK 21 引入的轻量级线程。

**注意**: Native Image 对虚拟线程的支持有限。

---

## 18. 缩略语速查

| 缩略语 | 全称 | 中文 |
|--------|------|------|
| **AOT** | Ahead-Of-Time | 提前编译 |
| **AST** | Abstract Syntax Tree | 抽象语法树 |
| **CE** | Community Edition | 社区版 |
| **EE** | Enterprise Edition | 企业版 (2023 年后合并为 Oracle GraalVM) |
| **GC** | Garbage Collection | 垃圾回收 |
| **GFTC** | GraalVM Free Terms and Conditions | GraalVM 免费许可条款 |
| **IR** | Intermediate Representation | 中间表示 |
| **JIT** | Just-In-Time | 即时编译 |
| **JNI** | Java Native Interface | Java 本地接口 |
| **JVMCI** | JVM Compiler Interface | JVM 编译器接口 |
| **LIR** | Low Level IR | 低级 IR |
| **LLVM** | Low Level Virtual Machine | 低级虚拟机 |
| **OSR** | On-Stack Replacement | 栈上替换 |
| **PGO** | Profile-Guided Optimization | 剖面引导优化 |
| **RSS** | Resident Set Size | 常驻内存集 |

---

## 19. 相关资源

### 术语学习
- [GraalVM 官方词汇表](https://www.graalvm.org/latest/docs/)
- [JVM 术语表](https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-1.html)

### 技术文档
- [Graal 编译器架构](architecture.md)
- [性能优化技术](performance.md)
- [Native Image 指南](native-image-guide.md)

---

**最后更新**: 2026-03-21

**贡献**: 欢迎添加缺失的术语
