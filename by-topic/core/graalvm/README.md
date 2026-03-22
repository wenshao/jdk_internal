# GraalVM 技术内幕

> Oracle Labs 的高性能 JVM 实现，Graal 编译器、Native Image 与多语言运行时

[← 返回核心平台](../)

---
## 目录

1. [概述](#1-概述)
2. [GraalVM 架构](#2-graalvm-架构)
3. [JVMCI (JEP 243) 接口](#3-jvmci-jep-243-接口)
4. [Native Image 深度解析](#4-native-image-深度解析)
5. [与 Project Leyden 的关系](#5-与-project-leyden-的关系)
6. [Truffle 语言生态](#6-truffle-语言生态)
7. [性能优化技术](#7-性能优化技术)
8. [GraalVM 版本演进](#8-graalvm-版本演进)
9. [实际使用与框架集成](#9-实际使用与框架集成)
10. [调试和诊断](#10-调试和诊断)
11. [源码结构](#11-源码结构)
12. [专题文档](#12-专题文档)
13. [贡献者](#13-贡献者)
14. [相关链接](#14-相关链接)

---


## 1. 概述

GraalVM 是 Oracle Labs 开发的**高性能 JVM 实现**，核心创新包括：

1. **Graal 编译器** - 用 Java 编写的高性能 JIT 编译器，基于 Sea of Nodes IR
2. **Native Image** - AOT 编译技术，将 Java 字节码编译为原生机器码
3. **Truffle 框架** - 语言实现框架，支持多语言运行时和跨语言调用

```
┌─────────────────────────────────────────────────────────────────┐
│                       GraalVM 技术架构                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  应用层                                  │   │
│  │     Java │ JavaScript │ Python │ Ruby │ R │ LLVM        │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Truffle 框架                            │   │
│  │        AST 解释器 + 部分求值 + 多态内联缓存               │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Graal 编译器                            │   │
│  │        Sea of Nodes IR + 逃逸分析 + 推测优化             │   │
│  │        JIT (运行时) │ Native Image (构建时)              │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  JVMCI 接口 (JEP 243)                    │   │
│  │        Java 编译器与 HotSpot VM 的桥梁                    │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  HotSpot VM                              │   │
│  │        C1 │ C2 │ GC │ 运行时服务                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. GraalVM 架构

GraalVM 由三大核心组件构成：**Graal 编译器**、**Truffle 框架**、**SubstrateVM**。它们各自独立又紧密协作，构成了一个完整的多语言高性能运行时平台。

### 2.1 Graal 编译器 (JIT/AOT 双模式)

Graal 是用 **Java 编写**的编译器，同时支持 JIT (Just-In-Time) 和 AOT (Ahead-Of-Time) 两种模式。

**JIT 模式** — 替代 C2 作为 HotSpot 的顶层编译器 (top-tier compiler)：
- 通过 JVMCI 插入 HotSpot，接收 C1 profiling 数据后触发编译
- 编译后的机器码通过 `CodeInstallationProvider` 安装到 CodeCache
- 支持 deoptimization（去优化）：优化假设失效时回退到解释执行

**AOT 模式** — 作为 Native Image 的编译后端：
- 构建时接收静态分析的结果，将可达方法编译为机器码
- 不依赖 profiling 数据，使用 PGO (Profile-Guided Optimization) 弥补
- 生成的代码链接到 SubstrateVM 运行时

**编译流水线 (compilation pipeline)**:
```
字节码 → BytecodeParser → StructuredGraph (HIR)
    → HighTier Phases (内联、逃逸分析、常量折叠)
    → MidTier Phases (循环优化、null check消除)
    → LowTier Phases (寄存器分配、指令选择)
    → LIR → 机器码
```

**Sea of Nodes IR** — Graal 的核心中间表示：
- **FixedNode**: 有固定执行顺序的节点（控制流节点，如 If、Merge、Return）
- **FloatingNode**: 可自由调度的节点（纯计算，如 Add、Mul、Constant）
- 统一数据流和控制流于一张图中，比 C2 的 Ideal Graph 更加规范化
- 图结构由 `StructuredGraph` 类管理，每个方法对应一张图

**与 C2 的区别**:

| 维度 | C2 | Graal |
|------|-----|-------|
| **实现语言** | C++ (~15 万行) | Java (~30 万行) |
| **IR 结构** | Sea of Nodes (Ideal) | Sea of Nodes (统一，类型更严格) |
| **逃逸分析** | 方法级 (connection graph) | 控制流敏感 (Partial Escape Analysis) |
| **内联深度** | 15 层 (MaxInlineLevel) | 激进内联 (25+ 层) |
| **编译速度** | 快 (~ms 级) | 较慢 (~2-5x C2) |
| **峰值性能** | 基准 | +5-10% (特定负载更高) |
| **可维护性** | 低 (C++ 复杂度) | 高 (Java 生态工具链) |
| **扩展性** | 添加新 pass 困难 | Phase 系统，易插拔 |

### 2.2 Truffle 框架

Truffle 是**自优化 AST 解释器框架** (self-optimizing AST interpreter framework)，用于实现高性能语言运行时：

```
┌─────────────────────────────────────────────────────┐
│                   Truffle 框架                        │
│                                                       │
│  语言实现者编写 AST 解释器:                              │
│  ┌─────────────────────────────────────────────┐     │
│  │  RootNode                                     │     │
│  │  ├─ AddNode (自特化: int → long → double)      │     │
│  │  ├─ ReadLocalNode                              │     │
│  │  └─ IfNode                                     │     │
│  └─────────────────────────────────────────────┘     │
│                    │                                   │
│                    ▼ Partial Evaluation (部分求值)      │
│  ┌─────────────────────────────────────────────┐     │
│  │  Graal IR (StructuredGraph)                    │     │
│  │  解释器循环被展开，特化路径被编译                     │     │
│  └─────────────────────────────────────────────┘     │
│                    │                                   │
│                    ▼ Graal 编译器                       │
│  ┌─────────────────────────────────────────────┐     │
│  │  优化后的机器码                                  │     │
│  └─────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────┘
```

核心原理：**First Futamura Projection** — 通过对解释器做部分求值（partial evaluation），将 `interpreter(program, input)` 自动转换为 `compiled_program(input)`。

### 2.3 SubstrateVM

SubstrateVM 是 Native Image 的**运行时组件** (runtime substrate)，用 Java 编写：

- **内存管理**: 内置 GC（Serial GC 默认，G1 GC 可选 since GraalVM 21），不依赖 HotSpot GC
- **线程管理**: 基于 OS 线程 (pthread)，支持 Virtual Threads (JDK 21+)
- **异常处理**: 编译时生成异常表，运行时通过 unwinding 机制处理
- **Isolates**: 同一进程中的独立堆空间，不同 isolate 之间零共享，适用于多租户场景
- **信号处理**: 替代 HotSpot 的 signal chaining，直接注册 POSIX 信号处理器

---

## 3. JVMCI (JEP 243) 接口

JVMCI (JVM Compiler Interface) 是 JDK 9 引入的**编译器插件接口**，定义了 Java 编写的编译器如何与 HotSpot VM 交互。它是 Graal 能够替代 C2 的技术基础。

### 3.1 核心接口层次

```java
// 1. 编译器接口 — 编译请求入口
public interface JVMCICompiler {
    CompilationRequestResult compileMethod(CompilationRequest request);
}

// 2. 元数据访问 — 读取类/方法/字段信息
public interface MetaAccessProvider {
    ResolvedJavaType lookupJavaType(Class<?> clazz);
    ResolvedJavaMethod lookupJavaMethod(Executable method);
    ResolvedJavaField lookupJavaField(Field field);
}

// 3. 代码安装 — 将编译结果安装到 CodeCache
public interface CodeCacheProvider {
    InstalledCode installCode(
        ResolvedJavaMethod method,
        CompiledCode compiledCode,
        InstalledCode installedCode,
        SpeculationLog log,
        boolean isDefault
    );
}

// 4. Profiling 数据 — 获取解释器/C1 收集的运行时信息
public interface ProfilingInfo {
    TriState getExceptionSeen(int bci);
    TriState getNullSeen(int bci);
    double getBranchTakenProbability(int bci);
    JavaTypeProfile getTypeProfile(int bci);  // 虚调用的接收者类型分布
}
```

### 3.2 Graal 如何替换 C2

```
HotSpot 的编译请求流程:

1. 方法被解释执行，触发 invocation counter / backedge counter 阈值
2. 编译线程 (CompilerThread) 从编译队列取出请求
3. 调用 JVMCI → JVMCICompiler.compileMethod()
4. Graal 接收到 CompilationRequest:
   - 通过 MetaAccessProvider 读取方法字节码
   - 通过 ProfilingInfo 读取 profiling 数据
   - 构建 StructuredGraph → 优化 → 生成机器码
5. 通过 CodeCacheProvider.installCode() 安装到 CodeCache
6. 后续调用直接跳转到编译后的机器码

启用方式:
  -XX:+EnableJVMCI -XX:+UseJVMCICompiler
  -Djvmci.Compiler=graal
```

### 3.3 安全模型与模块隔离

- **模块系统隔离** (JEP 261): `jdk.internal.vm.ci` 模块，默认不可访问
- **权限检查**: 需要 `RuntimePermission("jvmci")` 权限
- **实验性标志**: `-XX:+UnlockExperimentalVMOptions -XX:+EnableJVMCI`
- **信任边界**: 编译器代码必须位于 Boot ClassPath 或 module path 上的受信模块
- **JDK 17 后**: JEP 410 移除了 JDK 内置的 Graal，但 JVMCI 接口保留，第三方编译器仍可插入

### 3.4 JVMCI 的性能开销

| 操作 | 开销 | 说明 |
|------|------|------|
| 编译请求传递 | ~微秒级 | JNI downcall，一次性 |
| 元数据访问 | ~纳秒级 | 直接读取 HotSpot 内存 |
| 代码安装 | ~微秒级 | 写入 CodeCache + ICache flush |
| Profiling 读取 | ~纳秒级 | 读取 MethodData 结构 |
| **总体编译延迟** | ~2-5x C2 | Java 编译器本身也需要 JIT 编译 |

JVMCI 引入了 **libgraal** 优化：将 Graal 编译器预编译为 native shared library，消除编译器自身的 JIT 预热开销，编译延迟降至接近 C2 水平。

---

## 4. Native Image 深度解析

### 4.1 构建过程详解

Native Image 的构建分为四个主要阶段：

```
┌──────────────────────────────────────────────────────────────────┐
│                   Native Image 构建流程                            │
│                                                                    │
│  阶段1: Points-to Analysis (静态分析)                               │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │ 从 main() 入口出发，分析所有可达的:                          │    │
│  │ - 类 (reachable types)                                     │    │
│  │ - 方法 (reachable methods)                                 │    │
│  │ - 字段 (reachable fields)                                   │    │
│  │ 使用 flow-sensitive points-to analysis 追踪对象引用          │    │
│  └──────────────────────────────────────────────────────────┘    │
│                          ↓                                        │
│  阶段2: Heap Snapshotting (堆快照)                                 │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │ 执行类初始化器 (static initializers)                        │    │
│  │ 将 build-time 初始化的对象图序列化到 image heap               │    │
│  │ 运行时直接映射，无需重新初始化                                 │    │
│  └──────────────────────────────────────────────────────────┘    │
│                          ↓                                        │
│  阶段3: AOT Compilation (编译)                                     │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │ 使用 Graal 编译器将所有可达方法编译为机器码                     │    │
│  │ 应用全程序优化 (WP-SCCP, devirtualization, 常量折叠)          │    │
│  └──────────────────────────────────────────────────────────┘    │
│                          ↓                                        │
│  阶段4: Linking (链接)                                             │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │ 将编译后的机器码 + image heap + SubstrateVM 运行时            │    │
│  │ 链接为 ELF/Mach-O/PE 原生可执行文件                          │    │
│  └──────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

### 4.2 Closed-World Assumption (闭世界假设)

闭世界假设是 Native Image 的核心约束：**构建时必须已知所有代码**。

**具体限制**:
- **无运行时类加载** (no dynamic class loading): 不能使用 `Class.forName()` 动态加载
- **无运行时字节码生成** (no bytecode generation): CGLIB、ByteBuddy 动态代理需替换
- **无 InvokeDynamic bootstrap** (受限): Lambda 在构建时解析，但通用 invokedynamic 受限
- **反射须显式声明**: 运行时反射调用的类/方法/字段必须在配置中声明

**对比 JVM 的开放世界模型**:
| 特性 | JVM (开放世界) | Native Image (闭世界) |
|------|---------------|---------------------|
| 类加载 | 运行时按需加载 | 构建时全部确定 |
| 反射 | 无限制 | 须配置或 agent 采集 |
| 动态代理 | 运行时生成字节码 | 构建时生成 |
| 序列化 | 自动发现类 | 须配置可序列化类型 |
| ServiceLoader | 运行时扫描 | 构建时解析 |

### 4.3 反射配置 (Reflection Configuration)

三种配置方式：

**方式1: JSON 配置文件** (`reflect-config.json`):
```json
[
  {
    "name": "com.example.MyClass",
    "allDeclaredConstructors": true,
    "allPublicMethods": true,
    "fields": [
      { "name": "myField", "allowWrite": true }
    ]
  }
]
```

**方式2: Tracing Agent 自动采集**:
```bash
# 运行应用时自动记录反射/资源/代理/序列化/JNI 的使用
java -agentlib:native-image-agent=config-output-dir=./config \
     -jar myapp.jar

# 生成的配置文件:
# config/reflect-config.json
# config/resource-config.json
# config/proxy-config.json
# config/serialization-config.json
# config/jni-config.json
```

**方式3: 代码中注解/API 标记** (GraalVM Reachability Metadata):
```java
// 使用 @RegisterForReflection (Quarkus) 或 @ReflectiveAccess (Spring)
@RegisterForReflection
public class MyDTO { ... }
```

### 4.4 性能特征

| 指标 | JVM (HotSpot) | Native Image | 差异 |
|------|--------------|--------------|------|
| 启动时间 | 秒级 (1-5s) | 毫秒级 (10-50ms) | **100x 提升** |
| 内存占用 (RSS) | 100MB+ | 10-30MB | **5-10x 减少** |
| 峰值吞吐量 | 100% | 80-95% (无 PGO) | -5~-20% 降低 |
| 峰值吞吐量 (PGO) | 100% | 90-100% | 接近持平 |
| 构建时间 | N/A | 1-10 分钟 | 额外开销 |
| 可执行文件大小 | JRE ~300MB | 10-80MB | 显著减少 |

**GraalVM 25 Native Image 新增优化** (2025-09):
- **WP-SCCP** (Whole-Program Sparse Conditional Constant Propagation) 默认启用，分析全调用图传播常量，消除死代码分支
- **XGBoost 静态剖析器**: 基于机器学习推断方法调用频率，自动分类热/冷代码，减少二进制体积
- **高级混淆** (实验性, Oracle GraalVM): 重命名原生镜像中的符号，增强逆向工程防护

---

## 5. 与 Project Leyden 的关系

Project Leyden (JDK 内置 AOT) 和 GraalVM Native Image 是两种不同路线的 AOT 方案，目标和约束截然不同。

### 5.1 架构对比

```
GraalVM Native Image:                    Project Leyden:
┌────────────────────┐                  ┌────────────────────┐
│  Closed-World       │                  │  Condensed JVM     │
│  全静态编译          │                  │  渐进式约束          │
│  SubstrateVM 运行时  │                  │  HotSpot 运行时     │
│  无 JIT、无类加载    │                  │  保留 JIT + 类加载  │
│  100x 启动加速      │                  │  10-20x 启动加速    │
└────────────────────┘                  └────────────────────┘
```

### 5.2 详细对比

| 维度 | GraalVM Native Image | Project Leyden (JDK AOT) |
|------|---------------------|--------------------------|
| **归属** | Oracle Labs (GraalVM 项目) | OpenJDK 社区 (HotSpot 团队) |
| **世界模型** | 闭世界 (Closed-World) | 约束世界 (Constrained, 渐进) |
| **运行时** | SubstrateVM (Java 编写) | HotSpot VM (C++ 编写) |
| **类加载** | 构建时完成，运行时不可加载 | 保留运行时类加载能力 |
| **JIT 编译** | 无（纯 AOT） | 保留 JIT (C2/Graal) |
| **反射支持** | 须显式配置 | 更宽松，逐步限制 |
| **启动优化** | 100x (毫秒级) | 10-20x (CDS + AOT cache) |
| **峰值性能** | 80-95% (无 PGO) | 100% (JIT 仍可优化) |
| **兼容性** | 需适配 (闭世界约束) | 高兼容 (渐进式) |
| **目标 JDK** | 独立分发 (GraalVM) | JDK 内置 (JEP 483 等) |
| **核心 JEP** | JEP 295 (已移除), N/A | JEP 483 (AOT Cache, JDK 24) |

### 5.3 互补而非替代

两个项目的定位不同：
- **Native Image**: 适用于**无服务器 (serverless)、CLI 工具、微服务**等对启动时间和内存极度敏感的场景，愿意接受闭世界约束
- **Leyden AOT**: 适用于**传统企业应用**，需要保持完整的 Java 兼容性，同时获得启动加速，是 HotSpot 团队的长期方向
- Oracle 同时推动两个项目：GraalVM 团队负责 Native Image，HotSpot 团队负责 Leyden

---

## 6. Truffle 语言生态

Truffle 框架使得在 GraalVM 上实现高性能语言运行时成为可能。语言实现者只需编写 AST 解释器，Graal 编译器通过部分求值自动将其优化为高性能编译代码。

### 6.1 支持的语言

| 语言 | 项目名 | 成熟度 | 相对性能 | 说明 |
|------|--------|--------|----------|------|
| **JavaScript** | GraalJS | 生产就绪 | V8 的 60-80% | ECMAScript 2024 兼容，可替代 Nashorn |
| **Python** | GraalPython | 实验性→稳定 | CPython 的 50-150% | Python 3.11+ 兼容，C extension 部分支持 |
| **Ruby** | TruffleRuby | 生产就绪 | MRI 的 5-10x | CRuby 兼容，Rails 可运行 |
| **R** | FastR | 实验性 | GNU R 的 2-40x | 数值计算场景显著加速 |
| **WebAssembly** | GraalWasm | 生产就绪 | 原生的 50-80% | Wasm MVP + 扩展支持 |
| **LLVM** | Sulong | 生产就绪 | 原生的 50-80% | 运行 C/C++/Rust 的 LLVM bitcode |
| **Java** | Espresso | 实验性 | HotSpot 的 70-90% | Java-on-Java 元循环解释器 |

### 6.2 跨语言互操作 (Polyglot API)

Truffle 语言之间可以**零开销互调用** (zero-overhead interop)：

```java
// Java 调用 JavaScript
try (Context context = Context.create()) {
    Value jsFunction = context.eval("js", "(x) => x * 2");
    int result = jsFunction.execute(21).asInt();  // 42
}

// Java 调用 Python
try (Context context = Context.create()) {
    context.eval("python", "import numpy as np");
    Value npArray = context.eval("python", "np.array([1,2,3])");
}

// JavaScript 调用 Ruby
// 同一 Context 中不同语言共享对象，类型自动映射
```

跨语言调用在 Graal 编译后可被**内联** (inlined across language boundaries)，消除调用开销。

### 6.3 GraalJS 替代 Nashorn

JDK 11 移除 Nashorn (JEP 335) 后，GraalJS 成为推荐替代方案：
- 完整的 ECMAScript 2024 支持
- 兼容 `javax.script.ScriptEngine` API
- 支持 Node.js 兼容模式
- 通过 GraalVM Polyglot API 或 ScriptEngine API 使用

---

## 7. 性能优化技术

### 7.1 Partial Escape Analysis (部分逃逸分析)

Graal 的核心优化之一，比 C2 的逃逸分析更精确：

```java
// C2 的逃逸分析: Point 在 if-else 某些路径逃逸 → 整体堆分配
// Graal 的 PEA: 仅在逃逸路径上分配，非逃逸路径标量替换
public int compute(boolean flag) {
    Point p = new Point(x, y);  // Graal: 虚拟分配 (virtual allocation)
    if (flag) {
        return p.x + p.y;      // 非逃逸路径: 标量替换，无堆分配
    } else {
        list.add(p);            // 逃逸路径: 此处才实际分配
        return 0;
    }
}
// PEA 将分配延迟到逃逸点 (materialization point)
// 效果: 堆分配减少 30-50%，GC 压力降低
```

### 7.2 Speculative Optimizations (推测优化)

基于运行时 profiling 数据的**激进优化**，配合 deoptimization 保证正确性：

- **Type speculation**: profiling 显示虚调用只看到一种接收者类型 → 内联 + 类型守卫
- **Branch speculation**: profiling 显示分支总是走同一方向 → 消除另一方向的代码
- **Null speculation**: profiling 显示引用从不为 null → 消除 null 检查
- **Deoptimization**: 当守卫失败时，通过 uncommon trap 回退到解释器重新 profiling

### 7.3 Graal JIT 优化总览

| 优化技术 | 说明 | 性能提升 |
|----------|------|----------|
| **Partial Escape Analysis** | 控制流敏感的逃逸分析 | 堆分配 -30-50% |
| **Speculative Optimizations** | 基于 profiling 的推测 | 虚调用 +10-20% |
| **Aggressive Inlining** | 激进内联 (25+ 层) | 方法调用 +5-15% |
| **Loop Optimizations** | 循环向量化、边界检查消除 | 数值计算 +20-40% |
| **Read/Write Elimination** | 冗余内存操作消除 | 内存访问 +5-10% |
| **Conditional Elimination** | 冗余条件检查消除 | 分支 +5-10% |

### 7.4 Native Image 优化

| 优化技术 | 说明 | 效果 |
|----------|------|------|
| **静态分析** | 构建时分析调用图 | 启动时无需类加载 |
| **堆快照** | 构建时初始化对象 | 启动时间 -100-300ms |
| **闭世界假设** | 已知所有代码 | 激进 devirtualization |
| **PGO** | Profile-Guided Optimization | 性能 +10-15% |
| **WP-SCCP** | 全程序稀疏条件常量传播 (GraalVM 25 默认启用) | 二进制体积减少，死代码消除 |
| **ML 静态剖析** | XGBoost 推断方法调用频率，分类热/冷代码 | 二进制体积减少，运行时性能保持 |

### 7.5 Truffle 优化

| 优化技术 | 说明 | 性能提升 |
|----------|------|----------|
| **Partial Evaluation** | AST 折叠，消除解释器开销 | +50-100% |
| **Polymorphic Inline Cache** | 多态内联缓存 | +80-95% |
| **Assumptions** | 自动去优化机制 | 保证正确性 |
| **OSR** (On-Stack Replacement) | 长循环运行中编译替换 | 避免热循环停滞 |

---

## 8. GraalVM 版本演进

### 8.1 CE/EE 合并历程

```
2019-2022:  双版本时代
┌─────────────────────────────────────────────────────────┐
│  Community Edition (CE)     │  Enterprise Edition (EE)    │
│  - GPLv2 + CE               │  - 商业许可                  │
│  - 基础 Graal 编译器         │  - 增强 PEA、G1 for NI      │
│  - Serial GC for NI         │  - 压缩指针 for NI           │
│  - 无 PGO                   │  - PGO 支持                  │
│  - 无压缩指针 (NI)          │  - 企业级支持                │
└─────────────────────────────────────────────────────────┘

2023:  合并为统一发行版
┌─────────────────────────────────────────────────────────┐
│  Oracle GraalVM             │  GraalVM CE (社区构建)       │
│  - GFTC 免费许可             │  - GPLv2 + CE               │
│  - 含原 EE 全部优化          │  - 与 Oracle 版本同源码      │
│  - Oracle 官方支持           │  - 社区支持                  │
│  - 生产环境免费使用          │  - 完全开源                   │
└─────────────────────────────────────────────────────────┘
```

**合并后的变化**:
- 原 EE-only 优化（增强 PEA、G1 for Native Image、PGO、压缩指针）全部免费可用
- Oracle GraalVM 采用 **GFTC** (GraalVM Free Terms and Conditions) 许可，生产环境免费
- 社区版仍以 GPLv2 + Classpath Exception 提供

### 8.2 发展时间线

| 年份 | 事件 | 影响 |
|------|------|------|
| **2012** | Graal 项目在 Oracle Labs 启动 | 研究原型 |
| **2017** | JEP 243 (JVMCI) 进入 JDK 9 | Graal 可插入 HotSpot |
| **2018** | Graal JIT 进入 JDK 10 (JEP 317) | 实验性 Java 编写的 JIT 编译器 |
| **2019** | GraalVM 19.0 社区版发布 | 免费使用 |
| **2020** | CE/EE 功能差异化 | EE 含额外优化，CE 仍可安装 Python/Ruby/R |
| **2021** | JDK 17 移除实验性 Graal (JEP 410) | JVMCI 保留，Graal 需独立安装 |
| **2023** | CE/EE 合并为 Oracle GraalVM | GFTC 免费许可，原 EE 优化免费可用 |
| **2023** | Oracle 裁员 | Graal 团队受影响 (未经证实的报道) |
| **2023** | JDK 21 成为 GraalVM 基线 | LTS 对齐 |
| **2025** | GraalVM 25 发布 (2025-09-16) | 对齐 JDK 25 LTS；WP-SCCP 默认启用；XGBoost 静态剖析器；高级混淆 (实验性) |
| **2025** | GraalVM for JDK 24 为最后 Java SE 捆绑版 | 后续通过 GraalVM Free Terms 和 CE 提供 |

### 8.3 版本号与 JDK 对齐

GraalVM 从 2023 年开始采用 "GraalVM for JDK N" 命名：
- **GraalVM for JDK 17** — 长期支持 (LTS)
- **GraalVM for JDK 21** — LTS，CE/EE 合并后首个 LTS
- **GraalVM for JDK 22/23/24** — 短期支持 (non-LTS)
- **GraalVM 25** — 基于 JDK 25 LTS 的新命名方式

---

## 9. 实际使用与框架集成

### 9.1 Spring Native / Spring Boot AOT

Spring 从 **Spring Boot 3.0** 开始内置 GraalVM Native Image 支持：

```bash
# 构建 Native Image (使用 Maven)
mvn -Pnative native:compile

# 构建 Native Image (使用 Gradle)
gradle nativeCompile
```

**Spring AOT 引擎**:
- 构建时执行 Bean 定义处理（替代运行时 `BeanFactory` 的反射扫描）
- 自动生成反射/代理/资源配置（`reflect-config.json` 等）
- `@Conditional` 在构建时求值，不可达的 Bean 被消除
- Spring 6.x 引入 `RuntimeHints` API，框架和库可声明运行时所需的反射/资源

**性能数据** (Spring Boot 3.x + GraalVM):
| 指标 | JVM | Native Image |
|------|-----|--------------|
| 启动时间 | 2-5s | 30-80ms |
| 内存 (RSS) | 200-400MB | 40-80MB |
| 构建时间 | 10-30s | 2-8min |
| 峰值吞吐量 | 100% | 85-95% |

### 9.2 Quarkus Native

Quarkus 是**原生云优先** (cloud-native first) 的框架，从设计之初就针对 GraalVM Native Image 优化：

- **构建时元数据处理**: CDI bean 发现、配置解析在构建时完成
- **扩展系统**: 每个 Quarkus 扩展提供 `BuildStep`，在构建时生成必要的 Native Image 配置
- **Dev Mode**: 开发时使用 JVM 模式，部署时切换为 Native Image
- 大部分 Quarkus 扩展**开箱即用** (out of the box) 支持 Native Image

```bash
# 构建 Quarkus Native
./mvnw package -Dnative

# 容器化构建 (无需本地安装 GraalVM)
./mvnw package -Dnative -Dquarkus.native.container-build=true
```

### 9.3 Micronaut

Micronaut 使用**编译时依赖注入** (compile-time DI)，天然适合 Native Image：

- **编译时注解处理**: 使用 Java Annotation Processor 在编译时解析 `@Inject`、`@Singleton`
- **无运行时反射**: 不依赖反射做 DI，与闭世界假设高度兼容
- **GraalVM 元数据自动生成**: Micronaut 编译器插件自动生成 `reflect-config.json`

### 9.4 Helidon

Oracle 的轻量级微服务框架，两种编程模型均支持 Native Image：

- **Helidon SE**: 响应式 API，无 CDI，极轻量，Native Image 友好
- **Helidon MP**: MicroProfile 兼容，CDI 支持，通过构建插件支持 Native Image
- Oracle 官方维护 GraalVM 兼容性

### 9.5 框架 Native Image 支持对比

| 框架 | Native Image 支持 | 启动时间 (NI) | 额外配置 | 生态兼容性 |
|------|-------------------|--------------|----------|-----------|
| **Spring Boot 3** | 内置 | 30-80ms | 较少 (AOT 引擎) | 大部分 starter 支持 |
| **Quarkus** | 一等公民 | 10-30ms | 极少 (扩展系统) | 扩展生态完善 |
| **Micronaut** | 一等公民 | 10-30ms | 极少 (编译时 DI) | 核心模块全支持 |
| **Helidon SE** | 一等公民 | 10-20ms | 无 | Oracle 官方维护 |

---

## 10. 调试和诊断

### IGV (Ideal Graph Visualizer)

```bash
# 启用图转储
java -Dgraal.Dump=:2 -Dgraal.PrintGraph=Network -jar app.jar

# 查看特定方法
java -Dgraal.Dump=MyClass.myMethod:2 -jar app.jar
```

### 编译日志

```bash
# 启用编译日志
java -Dgraal.LogFile=graal.log -Dgraal.LogLevel=INFO -jar app.jar

# 详细日志
java -Dgraal.LogLevel=FINE -Dgraal.TraceInlining=true -jar app.jar
```

### Async Profiler

```bash
# CPU 分析
./profiler.sh start --event cpu <pid>
./profiler.sh stop --format flamegraph --file cpu-flame.html <pid>

# 内存分配分析
./profiler.sh start --event alloc <pid>
./profiler.sh stop --format flamegraph --file alloc-flame.html <pid>
```

---

## 11. 源码结构

### Graal 编译器

```
graal/
├── compiler/
│   ├── src/
│   │   ├── org.graalvm.compiler.core/
│   │   │   ├── BytecodeParser.java      # 字节码解析
│   │   │   ├── GraalCompiler.java       # 编译器入口
│   │   ├── org.graalvm.compiler.nodes/  # IR 节点
│   │   │   ├── FixedNode.java           # 固定节点
│   │   │   ├── FloatingNode.java        # 浮动节点
│   │   │   └── StructuredGraph.java     # 图结构
│   │   ├── org.graalvm.compiler.phases/ # 优化阶段
│   │   └── org.graalvm.compiler.lir/    # 低级 IR
│   └── test/
└── docs/
```

### JVMCI

```
jdk.vm.ci/
├── src/
│   ├── jdk.vm.ci.code/      # 编译代码接口
│   ├── jdk.vm.ci.meta/      # 元数据接口
│   └── jdk.vm.ci.runtime/   # 运行时接口
└── test/
```

---

## 12. 专题文档

| 文档 | 说明 |
|------|------|
| **[架构详解](architecture.md)** | GraalVM 内部架构、Sea of Nodes IR、JVMCI、Native Image 流程 |
| **[性能优化](performance.md)** | Graal JIT、Native Image、Truffle 优化技术详解 |
| **[基准测试](benchmarks.md)** | SPEC、DaCapo、Renaissance、TechEmpower、AWS Lambda 数据 |
| **[Native Image 指南](native-image-guide.md)** | 配置参数、反射/代理/JNI 配置、PGO、故障排查 |
| **[Graal vs C2](graal-vs-c2.md)** | 编译器架构对比、优化策略、性能数据 |
| **[JVMCI 内幕](jep-243-jvmci.md)** | JEP 243 接口、安全模型、性能开销 |
| **[调试工具](debugging.md)** | IGV、Async Profiler、JFR、故障排查流程 |
| **[源码解读](source-code.md)** | GraalCompiler、StructuredGraph、逃逸分析实现 |
| **[案例研究](case-studies.md)** | Spring Boot、Quarkus、AWS Lambda 迁移案例 |
| **[深度分析](deep-dive.md)** | Oracle Labs vs HotSpot 团队冲突、技术决策历史 |
| **[FAQ](faq.md)** | 64 个常见问题解答 |
| **[术语表](glossary.md)** | 40+ 术语和缩略语解释 |

---

## 13. 贡献者

### GraalVM 核心团队

| 贡献者 | 角色 | 活跃时间 | 状态 |
|--------|------|----------|------|
| **Doug Simon** | Director, Oracle Labs (Graal 编译器) | 2006-至今 | 活跃 |
| **Thomas Wuerthinger** | GraalVM 创始人, Senior Research Director | 2010-至今 | 减少日常参与 |
| **Christian Wimmer** | 编译器优化 (PhD ~2008, JKU Linz) | 2011-至今 | 活跃 |
| **Gilles Duboscq** | Truffle/Graal | 2012-至今 | 活跃 |

---

## 14. 相关链接

### 官方资源
- [GraalVM 官网](https://www.graalvm.org/)
- [Graal GitHub](https://github.com/oracle/graal)
- [JEP 243](/jeps/performance/jep-243.md)

### 技术文档
- [架构详解](architecture.md)
- [性能优化](performance.md)
- [源码解读](source-code.md)
- [JVMCI 内幕](jep-243-jvmci.md)

---

**最后更新**: 2026-03-22

**维护者**: JDK Internal Documentation Project
