# JIT 编译

> C1、C2、分层编译、Graal 演进历程

[← 返回核心平台](../)

---

## 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 6 ── JDK 9 ── JDK 17 ── JDK 21 ── JDK 26
   │         │        │        │        │        │        │
解释器    C1/C2   分层    Graal   JIT    虚拟线程  SuperWord
纯解释   分离    编译     JIT     优化     支持    成本模型
                  Tiered           性能
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
| **JDK 21** | Record 支持 | 编译器优化 |
| **JDK 23** | JIT 性能 | 编译吞吐量提升 |
| **JDK 26** | SuperWord 成本模型 | 智能向量化 |

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
Level 0: 解释执行 (Interpreter)
Level 1: C1 (纯解释 profiling)
Level 2: C1 (有限 profiling)
Level 3: C1 (完全 profiling)
Level 4: C2 (深度优化)
```

**编译策略:**
- 方法从 Level 0 开始
- 达到阈值后升级到下一层
- C1 收集 profiling 信息供 C2 使用
- C2 可以基于 profiling 做更激进的优化

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

### C2 专项贡献者

| 排名 | 贡献者 | 主要贡献 |
|------|--------|----------|
| 1 | [Vladimir Kozlov](https://github.com/vklang) | C2 架构师 |
| 2 | [Roland Westrelin](https://github.com/rwestrel) | C2 优化 (JDK-8325495 Add 优化) |
| 3 | [John Rose](https://github.com/jrose) | invokedynamic, JIT |
| 4 | [Emanuel Peter](https://eme64.github.io/blog/) | C2 博客作者, 编译器工程师 |
| 5 | [Christian Hagedorn](https://github.com/chhagedorn) | C2 优化, GVN |

---

## 内部结构

### HotSpot 编译器源码

```
src/hotspot/share/
├── compiler/
│   ├── compileBroker.cpp          # 编译任务调度
│   ├── compilation.cpp            # 编译策略
│   ├── compilerOracle.cpp         # 编译规则
│   └── compilerDefinitions.cpp    # 编译器定义
├── c1/                            # C1 (Client Compiler)
│   ├── c1_Compilation.cpp         # C1 编译入口
│   ├── c1_GraphBuilder.cpp        # IR 构建
│   ├── c1_IR.cpp                  # 中间表示
│   ├── c1_Instruction.cpp          # 指令定义
│   ├── c1_LinearScan.cpp          # 寄存器分配
│   └── c1_LIR.cpp                 # 线性 IR
├── opto/                          # C2 (Server Compiler)
│   ├── compile.cpp                # C2 编译入口, Optimize()
│   ├── callnode.cpp               # 方法调用节点
│   ├── cfgnode.cpp                # 控制流节点
│   ├── loopnode.cpp               # 循环节点
│   ├── memnode.cpp                # 内存节点
│   ├── castnode.cpp               # 类型转换
│   ├── mulnode.cpp                # 乘法节点
│   ├── addnode.cpp                # 加法节点
│   ├── subnode.cpp                # 减法节点
│   ├── divnode.cpp                # 除法节点
│   ├── connode.cpp                # 常量节点
│   ├── type.cpp                   # 类型系统
│   ├── gvn.cpp                    # Global Value Numbering
│   ├── phase.cpp                  # 优化阶段
│   ├── phaseX.cpp                 # 各优化阶段
│   ├── matcher.cpp                # 指令匹配
│   ├── output.cpp                 # 代码生成
│   ├── chaitin.cpp                # 寄存器分配 (图着色)
│   ├── block.cpp                  # 基本块
│   ├── classes.cpp                # 类继承图
│   ├── coalesce.cpp               # 寄存器合并
│   ├── loopopts.cpp               # 循环优化
│   ├── lock.cpp                   # 锁优化
│   ├── escape.cpp                 # 逃逸分析
│   ├── macro.cpp                  # 宏扩展
│   ├── node.cpp                   # Ideal 节点基类
│   ├── phase.cpp                  # Phase 基类
│   ├── regmask.cpp                # 寄存器掩码
│   ├── relocInfo.cpp              # 重定位信息
│   └── superword.cpp              # 向量化
├── jvmci/                         # JVMCI (Graal 接口)
│   └── ...
└── lib/                           # 编译器共享代码
    ├── compile.cpp                # 编译队列
    └── compilation.cpp            # 编译策略
```

### 关键内部类

| 类 | 作用 | 访问级别 |
|---|------|----------|
| `jdk.vm.ci.meta.Runtime` | JVMCI 接口 | `@JVMCI` |
| `jdk.vm.ci.code.CodeCache` | 代码缓存管理 | `@JVMCI` |
| `jdk.vm.ci.hotspot.HotSpotJVMCIRuntime` | JVMCI 实现 | `@JVMCI` |
| `jdk.internal.misc.CompoundMapping` | 代码映射 | 内部 |

---

## C2 编译流程详解

### 完整编译流程

```
1. Parse Phase (解析)
   ├── 字节码 → Ideal Graph
   ├── 内联优化
   └── 初始 GVN

2. PhaseIterGVN (第一次)
   ├── Global Value Numbering
   ├── 常量折叠
   └── 公共子表达式消除

3. PhaseIdealLoop (多轮)
   ├── 循环识别
   ├── 循环优化 (迭代 3+ 次)
   │   ├── Partial Peeling (部分剥离)
   │   ├── Full Peeling (完全剥离)
   │   ├── Unswitching (条件外提)
   │   ├── Unrolling (循环展开)
   │   └── Range Check Elimination
   └── 归一化

4. PhaseCCP (条件常量传播)
   ├── 条件分支优化
   └── 死代码消除

5. PhaseStringOpts
   ├── 字符串拼接优化
   └── StringBuilder 转换

6. PhaseEliminateNullChecks
   └── 空值检查消除

7. PhaseEscapeAnalysis
   ├── 逃逸分析
   └── 标量替换

8. PhaseMacroExpand
   ├── 宏节点扩展
   ├── 锁消除/粗化
   └── 原子操作优化

9. PhaseIterGVN (最终)
   └── 最终优化

10. PhaseVector
    └── 向量化

11. PhaseCFG
    └── 控制流图构建

12. PhaseChaitin
    └── 寄存器分配 (图着色)

13. PhaseBlockLayout
    └── 基本块布局

14. PhasePeephole
    └── 窥孔优化

15. PhaseOutput
    └── 机器码生成
```

### C2 优化阶段详细说明

#### PhaseIterGVN (Iterative Global Value Numbering)

**作用**: 全局值编号，识别和消除冗余计算

**关键优化**:
- 常量折叠: `2 + 3` → `5`
- 公共子表达式消除: `x + y` 复用
- 类型特化: 基于 profiling 的类型优化

**相关 Bug**:
- [JDK-8360035](https://bugs.openjdk.org/browse/JDK-8360035) - PhaseIterGVN 无限循环优化崩溃

#### PhaseIdealLoop (循环优化)

**作用**: 循环结构分析和优化

**子优化**:
- **Partial Peeling**: 部分循环剥离，减少条件判断
- **Full Peeling**: 完全循环剥离，消除循环
- **Unswitching**: 循环条件外提
- **Unrolling**: 循环展开，减少迭代开销
- **Range Check Elimination**: 数组边界检查消除
- **Loop Invariant Code Motion**: 循环不变量外提

**参考资料**:
- [OpenJDK Wiki: Loop optimizations in Hotspot](https://wiki.openjdk.org/spaces/HotSpot/pages/20415918/Loop+optimizations+in+Hotspot+Server+VM+Compiler+C2)

#### PhaseCCP (Conditional Constant Propagation)

**作用**: 条件常量传播

**优化**:
- 基于条件的常量传播
- 死分支消除
- 不可达代码移除

#### PhaseEscapeAnalysis (逃逸分析)

**作用**: 分析对象作用域

**优化**:
- **标量替换**: 对象字段拆分为独立变量
- **栈上分配**: 不逃逸对象分配在栈上
- **锁消除**: 不逃逸对象的锁优化

**状态报告**:
- [HotSpot Escape Analysis Status](https://cr.openjdk.org/~cslucas/escape-analysis/EscapeAnalysis.html)

#### PhaseSuperWord (向量化)

**作用**: SIMD 向量化优化

**优化**:
- 自动向量化: 标量操作 → SIMD 指令
- Shuffle/Pack/Unpack 优化
- 归约 (reduction) 向量化

**近期改进**:
- **JDK-8340093** ([PR #20964](https://github.com/openjdk/jdk/pull/20964)): SuperWord 成本模型
  - 智能判断向量化是否收益
  - 处理 shuffle/pack/unpack 操作的开销
  - 优化归约向量化

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
-XX:CompileThreshold=10000         # 内联调用阈值
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

# Vectorization (SuperWord)
-XX:+UseSuperWord                 # 启用向量化 (默认)
-XX:MaxVectorSize=32               # 最大向量大小
-XX:+UseVectorStubs               # 向量化桩

# Stress 模式 (用于测试)
-XX:+StressIGVN                   # GVN 压力测试
-XX:+StressLCM                     # 循环移动压力测试
-XX:+StressCCP                     # CCP 压力测试
-XX:+StressIncrementalInlining     # 增量内联压力测试
```

### 诊断参数

```bash
# 编译时间统计
-XX:+CITime                       # 打印编译时间
-XX:+CITimeVerbose                # 详细编译时间

# 编译日志
-XX:+PrintCompilation             # 打印编译活动
-XX:+PrintInlining                 # 打印内联决策
-XX:+UnlockDiagnosticVMOptions     # 解锁诊断选项
-XX:LogFile=compilation.log        # 日志文件

# C2 IR 输出
-XX:+PrintIdealGraphLevel          # 打印 IR
-XX:PrintIdealGraphLevel=2         # IR 详细级别
-XX:PrintIdealGraphFile=ideal.xml  # IR 输出文件

# 热点方法
-XX:CompileCommand=print,*String.* # 打印 String 类的编译
-XX:CompileCommand=exclude,*.*     # 排除编译
-XX:CompileCommand=option,*String.*,PrintOptoAssembly
```

---

## 诊断工具

### 编译日志

```bash
# 打印编译信息
-XX:+PrintCompilation             # 打印编译活动
-XX:+PrintInlining                 # 打印内联决策
-XX:+UnlockDiagnosticVMOptions     # 解锁诊断选项
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
> printcodecache                   # 代码缓存信息
> memdump <file>                   # 内存转储
```

### JFR (JDK 11+)

```bash
# JIT 编译事件
jcmd <pid> JFR.start name=jit
jcmd <pid> JFR.dump name=jit filename=jit.jfr
jcmd <pid> JFR.stop name=jit

# 关键事件
- jdk.CITime                       # 编译时间
- jdk.CICompiler                   # 编译器活动
- jdk.CodeCache                    # 代码缓存
- jdk.CodeSweeper                 # 代码清理
- jdk.Inlining                     # 内联决策
```

---

## 近期改进 (2024-2025)

### SuperWord 向量化改进

**JDK-8340093**: C2 SuperWord 成本模型 ([PR #20964](https://github.com/openjdk/jdk/pull/20964))
- 智能判断向量化收益
- 优化 shuffle/pack/unpack 操作
- 改进归约 (reduction) 向量化
- 集成时间: 2024年11月

**JDK-8344085**: 小循环向量化优化
- 扩展向量化到小迭代次数循环
- 改善边界情况处理

### C2 性能修复

**JDK-8325497**: C2 性能调查总纲 ([Issue](https://bugs.openjdk.org/browse/JDK-8325497))
- 追踪 JDK 21 C2 性能问题
- 包含多个子问题的修复

**JDK-8325495**: Add 系列优化 ([RFR v8](https://mail.openjdk.org/pipermail/hotspot-compiler-dev/2024-October/080608.html))
- 作者: Roland Westrelin
- 优化连续 Add 操作模式
- 8个版本迭代 (2024年)

### 编译器稳定性

**JDK-8360035**: PhaseIterGVN 崩溃修复
- 修复无限循环优化导致的崩溃
- 影响 JDK 11.0.27

**JDK-8317349**: 宏节点扩展随机化
- 随机化宏节点扩展顺序
- 改善编译确定性

### 编译吞吐量

**JDK-8366118**: 修复 DontCompileHugeMethods
- 确保分层编译下正确处理
- 修复大方法编译策略

**JDK-8368071**: 编译吞吐量回归修复
- 修复 2X-8X 编译性能下降

---

## 已知问题与限制

### C2 编译器已知问题

1. **内存峰值**: 字符串拼接编译时可能超过 1GB 内存 ([讨论](https://www.reddit.com/r/java/comments/1azwwcd/c2_compiler_memory_spike_on_string_concatenation/))
2. **CPU 卡死**: C2 编译器可能 100% CPU 卡死 ([JDK-8340238](https://bugs.openjdk.org/browse/JDK-8340238))
3. **编译时间**: 大方法编译时间可能很长

### SuperWord 局限性

- 向量化不总是有益的
- shuffle/pack/unpack 操作有开销
- 小循环可能不收益
- 某些架构支持有限

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

**官方文档:**
- [Tuning Java HotSpot VM](https://docs.oracle.com/javase/8/docs/technotes/guides/vm/performance.html)
- [HotSpot Internals Wiki](https://wiki.openjdk.org/display/HotSpot)

**技术博客:**
- [Emanuel's HotSpot C2 Blog](https://eme64.github.io/blog/) - C2 编译器深入解析
  - [Part 2: GVN](https://eme64.github.io/blog/2024/12/24/Intro-to-C2-Part02.html)
  - [Part 3: 优化阶段](https://eme64.github.io/blog/2025/01/23/Intro-to-C2-Part03.html)
  - [Part 4: 循环优化](https://eme64.github.io/blog/2025/01/23/Intro-to-C2-Part04.html)

**学术论文:**
- [Understanding and Finding JIT Compiler Performance Bugs](https://arxiv.org/html/2603.06551v1)
- [Translation Validation for HotSpot C2 Compiler](https://www.diva-portal.org/smash/get/diva2:1987997/FULLTEXT01.pdf)

**Bug 跟踪:**
- [JDK-8325497: C2 性能调查](https://bugs.openjdk.org/browse/JDK-8325497)
- [JDK-8340093: SuperWord 成本模型](https://bugs.openjdk.org/browse/JDK-8340093)

**邮件列表:**
- [hotspot-compiler-dev](https://mail.openjdk.org/pipermail/hotspot-compiler-dev/)
