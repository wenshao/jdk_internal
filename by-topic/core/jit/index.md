# JIT 编译

> C1、C2、分层编译、Graal 演进历程

[← 返回核心平台](../)

---

## 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 6 ── JDK 9 ── JDK 17 ── JDK 23
   │         │        │        │        │        │
解释器    C1/C2   分层    Graal   JIT    Graal
纯解释   分离    编译     JIT     优化   (实验)
                  Tiered
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 1.0** | 解释器 | 纯解释执行 |
| **JDK 1.3** | C2 (Server Compiler) | 高性能编译器 |
| **JDK 1.4** | C1 (Client Compiler) | 快速启动编译器 |
| **JDK 5** | C1/C2 分离 | -client/-server |
| **JDK 6** | 分层编译 | C1 + C2 组合 |
| **JDK 9** | Graal JIT | 实验性高性能 JIT |
| **JDK 17** | JIT 优化 | 编译器改进 |
| **JDK 23** | Graal 优化 | 性能提升 |

---

## 编译器对比

| 编译器 | 全称 | 特点 | 适用场景 |
|--------|------|------|----------|
| **解释器** | Interpreter | 启动快，执行慢 | 应用启动、冷代码 |
| **C1** | Client Compiler | 编译快，优化少 | 桌面应用、短时运行 |
| **C2** | Server Compiler | 编译慢，深度优化 | 长期运行的服务器应用 |
| **Graal** | Graal JIT | 基于 Java，可扩展 | 实验性，特定场景 |

### 分层编译 (Tiered Compilation)

```
Level 0: 解释器
Level 1: C1 (纯解释 profiling)
Level 2: C1 (有限 profiling)
Level 3: C1 (完全 profiling)
Level 4: C2 (深度优化)
```

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### JIT 编译器 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Coleen Phillimore | 72 | Oracle | C1/C2 编译器 |
| 2 | Aleksey Shipilev | 68 | Oracle | JIT 编译器 |
| 3 | Ioi Lam | 62 | Oracle | 编译器, 运行时 |
| 4 | Stefan Karlsson | 31 | Oracle | 编译器, GC |
| 5 | Doug Simon | 29 | Oracle | JIT 编译器 |
| 6 | David Holmes | 24 | Oracle | 并发, 编译器 |
| 7 | Claes Redestad | 24 | Oracle | 编译器优化 |
| 8 | Thomas Stuefe | 22 | Oracle | 编译器 |
| 9 | Vladimir Kozlov | 20 | Oracle | JIT 编译器 |
| 10 | Igor Veresov | 17 | Oracle | JIT 编译器 |

### C2 专项 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Vladimir Kozlov | 50+ | Oracle | C2 架构师 |
| 2 | Roland Westrelin | 30+ | Oracle | C2 优化 |
| 3 | John Rose | 25+ | Oracle | invokedynamic, JIT |

---

## 内部结构

### HotSpot 编译器源码

```
src/hotspot/share/compiler/
├── c1/                          # C1 (Client Compiler)
│   ├── c1_Compilation.cpp       # C1 编译入口
│   ├── c1_GraphBuilder.cpp      # IR 构建
│   ├── c1_IR.cpp                # 中间表示
│   ├── c1_Instruction.cpp        # 指令定义
│   └── c1_LIR.cpp               # 线性 IR
├── c2/                          # C2 (Server Compiler)
│   ├── compile.cpp              # C2 编译入口
│   ├── compilerOracle.cpp       # 编译决策
│   ├── idealGraphPrinter.cpp    # IR 可视化
│   ├── loopnode.cpp             # 循环优化
│   ├── matcher.cpp              # 指令匹配
│   ├── output.cpp               # 代码生成
│   └── phase.cpp                # 优化阶段
├── graal/                       # Graal JIT (可选)
│   └── ...
└── lib/                         # 编译器共享代码
    ├── compile.cpp              # 编译任务队列
    ├── compilation.cpp          # 编译策略
    └── compilerDefinitions.cpp  # 编译器定义
```

### 关键内部类

| 类 | 作用 | 访问级别 |
|---|------|----------|
| `jdk.vm.ci.meta.Runtime` | JVMCI 接口 | `@JVMCI` |
| `jdk.vm.ci.code.CodeCache` | 代码缓存管理 | `@JVMCI` |
| `jdk.vm.ci.hotspot.HotSpotJVMCIRuntime` | JVMCI 实现 | `@JVMCI` |
| `jdk.internal.misc.CompoundMapping` | 代码映射 | 内部 |

---

## VM 参数

### 编译器选择

```bash
# 选择编译器
-client                         # 使用 C1
-server                        # 使用 C2 (默认 JDK 9+)
-XX:+TieredCompilation          # 启用分层编译 (默认)
-XX:-TieredCompilation         # 禁用分层编译

# Graal JIT (JDK 9+)
-XX:+UnlockExperimentalVMOptions
-XX:+UseJVMCICompiler
-XX:+EnableJVMCI
-XX:+UseGraalJIT               # 使用 Graal 替代 C2
```

### 编译阈值

```bash
# 分层编译阈值
-XX:Tier0InvokeNotifyFreqLog=7     # Level 0 调用频率
-XX:Tier3InvokeNotifyFreqLog=10    # Level 3 (C1) 调用频率
-XX:Tier4CompileThreshold=5000     # Level 4 (C2) 调用阈值
-XX:CompileThreshold=10000         # 传统 C2 阈值

# 回边阈值 (循环)
-XX:OnStackReplacePercentage=140   # OSR 比例
-XX:InterpreterProfilePercentage=33
```

### 代码缓存

```bash
# 代码缓存大小
-XX:InitialCodeCacheSize=256k      # 初始代码缓存
-XX:ReservedCodeCacheSize=256m     # 最大代码缓存
-XX:CodeCacheExpansionSize=64k     # 扩展增量

# 代码缓存分层
-XX:SegmentedCodeCache             # 分段代码缓存 (JDK 9+)
-XX:NonMethodCodeHeapSize=56m      # 非方法代码
-XX:ProfiledCodeHeapSize=41m       # Profiled 代码
-XX:NonProfiledCodeHeapSize=161m   # 非 Profiled 代码
```

### 内联控制

```bash
# 内联阈值
-XX:MaxInlineSize=35               # 最大内联方法大小 (字节码)
-XX:FreqInlineSize=325             # 热方法内联阈值
-XX:MaxTrivialSize=6               # 平凡方法内联阈值

# 内联策略
-XX:InlineSmallCode=1000           # 小代码内联
-XX:+Inline                       # 启用内联 (默认)
-XX:-Inline                       # 禁用内联
```

### C2 特定参数

```bash
# C2 优化级别
-XX:LoopUnrollLimit=60             # 循环展开限制
-XX:LoopOptsCount=30               # 循环优化迭代次数
-XX:+UseLoopPredicate             # 循环谓词

# Escape Analysis
-XX:+DoEscapeAnalysis             # 启用逃逸分析 (默认)
-XX:+EliminateAllocations          # 消除分配
-XX:+PrintEliminateAllocations     # 打印分配消除

# Vectorization
-XX:+UseVectorStubs               # 向量化桩
-XX:MaxVectorSize=32               # 最大向量大小
```

---

## 诊断工具

### 编译日志

```bash
# 打印编译信息
-XX:+PrintCompilation             # 打印编译活动
-XX:+PrintInlining                 # 打印内联决策
-XX:+UnlockDiagnosticVMOptions     # 解锁诊断选项
-XX:+PrintCompilation             # 详细编译日志
-XX:LogFile=compilation.log        # 日志文件

# C2 IR 输出
-XX:+PrintIdealGraphLevel          # 打印 IR
-XX:PrintIdealGraphLevel=2         # IR 详细级别
-XX:PrintIdealGraphFile=ideal.xml  # IR 输出文件

# 热点方法
-XX:CompileCommand=print,*String.* # 打印 String 类的编译
-XX:CompileCommand=exclude,*.*     # 排除编译
```

### jhsdb (JDK 9+)

```bash
# 查看 JIT 编译
jhsdb jstack --pid <pid> --mixed
jhsdb jmap --pid <pid> --heap --binary
jhsdb clhsdb

# 在 clhsdb 中
> printcodecache                   # 打印代码缓存
> printmdo <address>               # 打印 MethodData
> printmethod <address>            # 打印 Method
```

### JFR (JDK 11+)

```bash
# JIT 编译事件
jcmd <pid> JFR.start name=jit
jcmd <pid> JFR.dump name=jit filename=jit.jfr
jcmd <pid> JFR.stop name=jit

# 关键事件
- jdk.CITime
- jdk.CICompiler
- jdk.CodeCache
- jdk.CodeSweeper
- jdk.Inlining
```

---

## 编译优化技术

### C2 优化阶段

```
1. Parse Phase           # 解析字节码 → 控制流图
2. PhaseIdealLoop        # 循环优化
3. PhaseIdealLoop1       # 循环优化第二遍
4. PhaseCCP              # 常量传播
5. PhaseStringOpts       # 字符串优化
6. PhaseEliminateNullChecks  # 空值检查消除
7. PhaseScalarReplace    # 标量替换
8. PhaseEscapeAnalysis   # 逃逸分析
9. PhaseLoopUnswitching  # 循环开关
10. PhaseSuperWord       # 向量化
11. PhaseMatcher         # 指令匹配
12. PhaseScheduling      # 指令调度
13. PhaseRegAlloc        # 寄存器分配
14. PhaseBlockLayout     # 基本块布局
15. PhaseCodeGen         # 代码生成
```

### 优化技术

| 技术 | 说明 | 效果 |
|------|------|------|
| **内联** | 方法调用替换为方法体 | 消除调用开销 |
| **逃逸分析** | 分析对象作用域 | 栈上分配 |
| **标量替换** | 对象拆分为字段 | 消除对象分配 |
| **循环展开** | 复制循环体 | 减少分支 |
| **向量化** | SIMD 指令 | 并行计算 |
| **常量折叠** | 编译期计算 | 消除运行时计算 |
| **死代码消除** | 移除不可达代码 | 减少代码大小 |

---

## 相关链接

### 本地文档

- [性能时间线](../performance/timeline.md) - JIT 编译演进
- [JVM 调优](../jvm/) - 编译器参数
- [内存管理](../memory/) - 代码缓存

### 相关主题

- [性能优化](../performance/) - 编译器优化
- [GC 演进](../gc/) - GC 与 JIT 协作
- [JVM 调优](../jvm/) - VM 参数

### 外部参考

- [Tuning Java HotSpot VM](https://docs.oracle.com/javase/8/docs/technotes/guides/vm/performance.html)
- [HotSpot Internals](https://wiki.openjdk.org/display/HotSpot)
- [Graal VM](https://www.graalvm.org/)
