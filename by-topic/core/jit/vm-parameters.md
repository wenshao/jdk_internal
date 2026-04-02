# VM 参数参考

> HotSpot JIT 编译器完整参数手册

[← 返回 JIT 编译](../)

---
## 目录

1. [快速索引](#1-快速索引)
2. [编译器选择](#2-编译器选择)
3. [编译阈值](#3-编译阈值)
4. [代码缓存](#4-代码缓存)
5. [内联控制](#5-内联控制)
6. [C2 优化参数](#6-c2-优化参数)
7. [平台特定参数](#7-平台特定参数)
8. [版本相关参数](#8-版本相关参数)
9. [诊断参数](#9-诊断参数)
10. [Stress 模式](#10-stress-模式)
11. [性能调优建议](#11-性能调优建议)
12. [参数速查表](#12-参数速查表)
13. [相关链接](#13-相关链接)
14. [贡献者](#14-贡献者)

---


## 1. 快速索引

| 类别 | 描述 |
|------|------|
| [编译器选择](#编译器选择) | C1, C2, Graal, 分层编译 |
| [编译阈值](#编译阈值) | 调用/回边阈值, OSR |
| [代码缓存](#代码缓存) | 分段缓存, 清理策略 |
| [内联控制](#内联控制) | 内联阈值, 策略, 排除 |
| [C2 优化](#c2-优化参数) | 循环, 逃逸分析, 向量化 |
| [平台特定](#平台特定参数) | x86, ARM, RISC-V |
| [诊断参数](#诊断参数) | 日志, IR, 汇编输出 |
| [性能调优](#性能调优建议) | 启动/吞吐量/延迟配置 |
| [版本相关](#版本相关参数) | JDK 17/21/23+ 新增参数 |

---

## 2. 编译器选择

### 基础选择

```bash
-client                         # 使用 C1 (Client Compiler)
-server                        # 使用 C2 (Server Compiler, 默认 JDK 9+)
-XX:+TieredCompilation          # 启用分层编译 (默认)
-XX:-TieredCompilation         # 禁用分层编译
```

### 分层编译级别

```bash
# 分层编译级别控制 (JDK 8+)
-XX:TieredStopAtLevel=0         # 只解释执行
-XX:TieredStopAtLevel=1         # C1 简单编译
-XX:TieredStopAtLevel=2         # C1 有限 profiling
-XX:TieredStopAtLevel=3         # C1 完整 profiling
-XX:TieredStopAtLevel=4         # C2 (默认)

# 常用配置
-XX:TieredStopAtLevel=1         # 快速启动 (只 C1)
-XX:-TieredCompilation -Xcomp   # 强制编译所有代码
-Xint                           # 纯解释模式
-Xmixed                         # 混合模式 (默认)
```

### 编译器特性

| 特性 | C1 | C2 |
|------|-----|-----|
| 编译速度 | 快 | 慊 |
| 优化程度 | 基础 | 高级 |
| Profiling | 有 | 有 (来自 C1) |
| 适用场景 | 启动阶段 | 长期运行服务 |

### Graal JIT

```bash
# 启用 Graal JIT (JDK 9+)
-XX:+UnlockExperimentalVMOptions
-XX:+UseJVMCICompiler
-XX:+EnableJVMCI
-XX:+UseGraalJIT               # 使用 Graal 替代 C2
-XX:-UseJVMCICompiler          # 禁用 JVMCI
-XX:jvmciCompiler=graal        # 指定 Graal 编译器

# Graal 特定参数
-XX:+UseGraalJITAsServer       # Graal 作为服务编译器
-XX:+PrintCompilation          # 查看实际使用的编译器
```

---

## 3. 编译阈值

### 分层编译阈值

```bash
# 各层编译阈值
-XX:Tier0InvokeNotifyFreqLog=7     # Level 0 调用频率对数
-XX:Tier1InvokeNotifyFreqLog=7     # Level 1 调用频率对数
-XX:Tier2InvokeNotifyFreqLog=14    # Level 2 调用频率对数
-XX:Tier3InvokeNotifyFreqLog=10    # Level 3 调用频率对数
-XX:Tier4CompileThreshold=5000     # Level 4 (C2) 调用阈值
-XX:CompileThreshold=10000         # 传统 C2 阈值 (非分层)

# 回边阈值 (循环)
-XX:Tier0BackedgeNotifyFreqLog=10  # Level 0 回边频率
-XX:Tier3BackEdgeNotifyFreqLog=13  # Level 3 回边频率
-XX:OnStackReplacePercentage=140   # OSR 比例
```

### OSR (On-Stack Replacement)

```bash
# OSR 配置
-XX:OnStackReplacePercentage=140   # OSR 触发百分比
-XX:InterpreterProfilePercentage=33 # 解释器 profiling 比例
-XX:CompileThreshold=10000         # 基础编译阈值

# OSR 调整
-XX:MinInlinelogRatio=20           # 最小内联比率
-XX:FreqInlineSize=325             # 热方法内联阈值
```

### 阈值说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `CompileThreshold` | 10000 | C2 编译需要的调用次数 |
| `Tier4CompileThreshold` | 5000 | 分层编译 C2 阈值 |
| `Tier3CompileThreshold` | 2000 | C1 完整 profiling 阈值 |
| `FreqInlineSize` | 325 | 热方法内联阈值 (字节码) |
| `MaxInlineSize` | 35 | 最大内联方法大小 (字节码) |

### 阈值调优示例

```bash
# 快速启动 - 提高阈值
-XX:CompileThreshold=15000
-XX:Tier4CompileThreshold=10000

# 快速优化 - 降低阈值
-XX:CompileThreshold=1000
-XX:Tier4CompileThreshold=500

# 禁用 OSR
-XX:OnStackReplacePercentage=0
```

---

## 4. 代码缓存

### 缓存大小

```bash
# 代码缓存配置
-XX:InitialCodeCacheSize=256k      # 初始代码缓存
-XX:ReservedCodeCacheSize=240m     # 最大代码缓存 (默认)
-XX:CodeCacheExpansionSize=64k     # 扩展增量
-XX:MinCodeCacheSize=512k          # 最小代码缓存

# 分段代码缓存 (JDK 9+)
-XX:+SegmentedCodeCache            # 启用分段 (默认)
-XX:-SegmentedCodeCache            # 禁用分段

# 各段配置 (JDK 17+ 默认值)
-XX:NonNMethodCodeHeapSize=5m      # 非方法代码 (blob, stubs)
-XX:ProfiledCodeHeapSize=122m      # Profiled 代码 (C1 编译)
-XX:NonProfiledCodeHeapSize=122m   # 非 Profiled 代码 (C2 编译)
```

### 代码缓存结构

```
┌─────────────────────────────────────────────────────┐
│                  Code Cache                         │
├─────────────────┬───────────────┬───────────────────┤
│  Non-NMethod     │  Profiled     │  NonProfiled      │
│  (5 MB)         │  (122 MB)     │  (122 MB)         │
├─────────────────┼───────────────┼───────────────────┤
│ • Buffers       │ • C1 编译     │ • C2 编译         │
│ • Runtime stubs │ • 有 profiling│ • 无 profiling    │
│ • Adapters      │ • 可能反优化  │ • 稳定代码        │
│ • Deopt         │               │                   │
└─────────────────┴───────────────┴───────────────────┘
```

### 代码缓存监控

```bash
# 打印代码缓存信息
-XX:+PrintCodeCache                # 打印代码缓存信息
-XX:+PrintCodeCacheOnCompilation   # 编译时打印代码缓存
-XX:PrintCodeCacheOnCompilation=2  # 详细级别

# 代码缓存统计
-XX:+PrintCodeCacheStatistics      # 打印统计信息
```

### 代码缓存清理

```bash
# 清理策略
-XX:+UseCodeCacheFlushing          # 启用代码缓存清理 (默认)
-XX:-UseCodeCacheFlushing          # 禁用清理
-XX:MinCodeCacheFlushRatio=11      # 最小清理比例
-XX:CodeCacheFlushingMinimumFreeSpace=16m

# 清理触发条件
-XX:CodeCacheFullCount=0           # 缓存满后清理次数
```

---

## 5. 内联控制

### 内联阈值

```bash
# 内联大小限制
-XX:MaxInlineSize=35               # 最大内联方法大小 (字节码)
-XX:FreqInlineSize=325             # 热方法内联阈值
-XX:MaxTrivialSize=6               # 平凡方法内联阈值 (getter/setter)
-XX:MaxRecursiveInlineSize=35      # 递归内联阈值
-XX:InlineSmallCode=1000           # 小代码内联 (字节码)
```

### 内联策略

```bash
# 启用/禁用
-XX:+Inline                       # 启用内联 (默认)
-XX:-Inline                       # 禁用内联

# 内联层次
-XX:MaxInlineLevel=9               # 最大内联深度
-XX:InlineFrequencyRatio=10        # 频率比率

# 特殊情况
-XX:InlinePrimitivesOnly           # 只内联原始类型方法
-XX:InlineUnsafeOps                # 内联 Unsafe 操作
```

### 编译命令 (CompileCommand)

```bash
# 基本语法
-XX:CompileCommand=<command>,<class>.<method>

# 常用命令
-XX:CompileCommand=exclude,java/lang/String.*      # 排除 String 类
-XX:CompileCommand=exclude,*String.indexOf         # 排除特定方法
-XX:CompileCommand=inline,java/lang/Math.*         # 强制内联
-XX:CompileCommand=dontinline,java/lang/String.*   # 禁止内联
-XX:CompileCommand=print,*String.*                 # 打印编译信息
-XX:CompileCommand=log,*String.*                   # 日志记录
-XX:CompileCommand=option,java/lang/Math.*,InlineLimit,100  # 设置选项

# 多个命令
-XX:CompileCommandFile=commands.txt                # 从文件读取
```

### 内联决策日志

```bash
# 查看内联决策
-XX:+PrintInlining                 # 打印内联决策
-XX:+PrintCompilation             # 包含内联信息
-XX:FrequencyInlineSize=100        # 频率内联大小

# 日志输出示例
# @ 12   java.lang.String::indexOf (70 bytes)
#   @ 3   java.lang.String::isLatin1 (6 bytes)   inline (hot)
#   @ 5   java.lang.StringCoding::hasNegatives   inline (hot)
```

---

## 6. C2 优化参数

### 循环优化

```bash
# 循环展开
-XX:LoopUnrollLimit=60             # 循环展开限制
-XX:LoopUnrollMin=2                # 最小展开次数
-XX:LoopMaxUnroll=16               # 最大循环展开次数
-XX:LoopOptsCount=30               # 循环优化迭代次数

# 循环剥离
-XX:PeelIterations=0               # 循环剥离迭代次数
-XX:PeelOuterLoops                 # 剥离外层循环

# 循环谓词
-XX:+UseLoopPredicate              # 循环谓词 (默认)
-XX:-UseLoopPredicate              # 禁用循环谓词
-XX:LoopPredicatePercent=20        # 谓词百分比
```

### 逃逸分析 (Escape Analysis)

```bash
# 逃逸分析控制
-XX:+DoEscapeAnalysis              # 启用逃逸分析 (默认)
-XX:-DoEscapeAnalysis              # 禁用逃逸分析
-XX:+EliminateAllocations           # 消除分配 (默认)
-XX:-EliminateAllocations           # 保留分配
-XX:+PrintEliminateAllocations     # 打印分配消除
-XX:EscapeAnalysisTimeout=20       # 分析超时 (秒)

# 相关优化
-XX:+EliminateLocks                # 锁消除 (默认)
-XX:+EliminateNullChecks           # 空值检查消除 (默认)
-XX:+EliminateAutoBox              # 自动装箱消除
-XX:EliminateAllocationsMaxLoop=10 # 最大循环消除次数
```

### 向量化 (SuperWord)

```bash
# SuperWord 向量化
-XX:+UseSuperWord                  # 启用向量化 (默认)
-XX:-UseSuperWord                  # 禁用向量化
-XX:MaxVectorSize=32               # 最大向量大小 (字节)
-XX:+UseVectorStubs                # 向量化桩
-XX:VectorizeDebugOptions=0        # 向量化调试选项
-XX:+TraceSuperWord                # 跟踪向量化决策
-XX:SuperWordLoopUnrollLimit=60    # 向量化循环展开限制

# 向量化特性
-XX:+UseVectorizedMismatchIntrinsic # 向量化不匹配操作
-XX:MaxVectorSize=64               # AVX-512 支持
```

### 类型特化与 Speculation

```bash
# 类型 profiling
-XX:+UseTypeSpeculation            # 类型推测 (默认)
-XX:-UseTypeSpeculation            # 禁用类型推测
-XX:TypeProfileLevel=111           # 类型 profiling 级别
-XX:+UseSpeculativePredictions     # 投机预测

# 去虚拟化
-XX:+UseInlineCaches               # 内联缓存 (默认)
-XX:InlineType=3                   # 内联类型级别
```

### 数组优化

```bash
# 数组边界检查消除
-XX:+EliminateArrayChecks          # 数组检查消除 (默认)
-XX:MaxBcotypeSize=30              # 字节码大小限制

# 数组克隆优化
-XX:+OptimizeArrayClone            # 数组克隆优化

# 数组拷贝优化
-XX:+UseFastAccessorMethods        # 快速访问方法
```

---

## 7. 平台特定参数

### x86/x64

```bash
# x86 特定优化
-XX:+UseXMMForArrayOps             # 使用 XMM 寄存器数组操作
-XX:+UseXMMForObjInit              # 使用 XMM 对象初始化
-XX:UseSSE=4                       # SSE 级别 (0-4)
-XX:UseAVX=3                       # AVX 级别 (0-3)
-XX:UseAVX512=2                    # AVX-512 级别
-XX:+UseUnalignedLoadStores        # 非对齐加载/存储

# 指令选择
-XX:+UseAddressNop                 # 使用 NOP 指令
-XX:+UseIncDec                     # 使用 INC/DEC 指令
-XX:UseCountLeadingZerosInstruction=1  # LZCNT 指令
-XX:UseCountTrailingZerosInstruction=1 # TZCNT 指令
```

### ARM / AArch64

```bash
# ARM 特定优化
-XX:+UseSIMDForMemoryOps           # SIMD 内存操作
-XX:+UseNeon                       # 使用 NEON 指令
-XX:+UseAESIntrinsics              # AES 硬件加速
-XX:+UseSHA1Intrinsics             # SHA-1 硬件加速
-XX:+UseSHA256Intrinsics           # SHA-256 硬件加速
-XX:+UseSHA512Intrinsics           # SHA-512 硬件加速

# SVE (Scalable Vector Extension)
-XX:+UseSVE                        # 启用 SVE
-XX:UseSVE=2                       # SVE 版本
```

### RISC-V

```bash
# RISC-V 特定优化
-XX:+UseRVC                        # 使用 RVC 压缩指令
-XX:+UseZba                        # 位操作扩展
-XX:+UseZbb                        # 基本位操作
-XX:+UseZbs                        # 单位设置位
-XX:+UseZihintpause                # 暂停提示
```

### LoongArch

```bash
# LoongArch 特定优化
-XX:+UseLASX                       # 使用 LSX (128-bit SIMD)
-XX:+UseLZX                        # 使用 LASX (256-bit SIMD)
-XX:+UseLoongArchIntrinsics        # 龙芯 intrinsic
```

---

## 8. 版本相关参数

### JDK 17+

```bash
# 新增优化参数
-XX:+UseCompactObjectHeaders       # 紧凑对象头 (默认)
-XX:-UseCompactObjectHeaders       # 禁用紧凑对象头

# 记录类 (JDK 14+)
-XX:+UnlockExperimentalVMOptions
-XX:+UseEpsilonGC                  # No-op GC (测试)
```

### JDK 21+

```bash
# 虚拟线程 (Project Loom)
-XX:+VirtualThreads                # 启用虚拟线程支持
-XX:VirtualThreadTaskMaxParallelism=1 # 虚拟线程并行度

# Generational ZGC
-XX:+ZGenerational                 # 启用分代 ZGC
```

### JDK 23+

```bash
# Region-based VM
-XX:+UseRegionBasedVM              # 基于区域的 VM

# 新的 GC
-XX:+UseZGC                        # ZGC 正式版
-XX:+UseShenandoahGC               # Shenandoah (某些平台)
```

---

## 9. 诊断参数

### 统一日志 (JDK 9+)

```bash
# JIT 编译日志
-Xlog:compilation=info:file=comp.log              # 编译日志
-Xlog:compilation=debug                           # 详细编译日志
-Xlog:compilation=info:stdout                     # 输出到控制台
-Xlog:compilation*=debug                          # 所有编译相关日志

# 内联日志
-Xlog:inlining=info                               # 内联决策
-Xlog:inlining=debug                              # 详细内联

# 代码缓存日志
-Xlog:codecache=info                              # 代码缓存
-Xlog:codecache=debug                             # 详细代码缓存

# 组合日志
-Xlog:compilation+inlining=info:file=compile.log  # 编译+内联
-Xlog:gc+compilation=info                         # GC+编译
```

### 传统日志选项

```bash
# 编译时间统计
-XX:+CITime                       # 打印编译时间
-XX:+CITimeVerbose                # 详细编译时间
-XX:+PrintCompilation             # 打印编译活动 (简洁)
-XX:+PrintInlining                 # 打印内联决策
-XX:+UnlockDiagnosticVMOptions     # 解锁诊断选项
```

### IR 输出

```bash
# Ideal Graph 可视化
-XX:+PrintIdealGraphLevel          # 打印 IR 级别
-XX:PrintIdealGraphLevel=2         # IR 详细级别 (0-4)
-XX:PrintIdealGraphFile=ideal.xml  # IR 输出文件
-XX:PrintIdealGraphAddress=0x1234  # 打印特定地址的 IR

# IGV (Ideal Graph Visualizer)
-XX:+PrintIdealGraphAtLineNumber=123
-XX:+PrintIdealGraphFile           # 生成 IGV 文件

# PrintIdeal 选项
-XX:+PrintIdeal                    # 打印 IR
-XX:PrintIdealPhase=xxx            # 特定阶段
```

### 汇编输出

```bash
# 打印汇编 (需要 hsdis 库)
-XX:+PrintAssembly                  # 打印生成汇编
-XX:+PrintOptoAssembly              # 打印优化后的汇编
-XX:PrintAssemblyOptions=intel      # 汇编语法 (intel/att)
-XX:PrintAssemblyOptions=syntax     # 指定语法

# 指定方法
-XX:CompileCommand=print,*MyClass.myMethod
-XX:CompileCommand=print,*MyClass.* -XX:+PrintAssembly
```

### 编译队列监控

```bash
# 编译队列
-XX:+PrintCompilation              # 查看编译活动
-XX:+PrintCompilerOracle           # 打印编译预测
-XX:+LogCompilation                # 日志编译
-XX:CompileCommand=print,*.*       # 打印所有编译
```

---

## 10. Stress 模式

```bash
# 压力测试模式 (用于测试 JVM)
-XX:+StressIGVN                     # GVN 压力测试
-XX:+StressLCM                       # 循环移动压力测试
-XX:+StressGCM                       # 全局代码移动压力测试
-XX:+StressCCP                       # CCP 压力测试
-XX:+StressIncrementalInlining       # 增量内联压力测试
-XX:+StressMacroExpansion            # 宏扩展压力测试
-XX:+StressMacroElimination          # 宏消除压力测试
-XX:+StressUnstableIfTraps           # 不稳定 if 陷阱压力测试
-XX:+StressBailout                   # Bailout 压力测试
-XX:+StressLoopPeeling               # 循环剥离压力测试
-XX:+StressLoopOpts                  # 循环优化压力测试
-XX:+StressSeed=0                    # 随机种子
```

---

## 11. 性能调优建议

### 启动优先配置

```bash
# 快速启动 - 减少编译开销
-XX:TieredStopAtLevel=1            # 只用 C1
-XX:CompileThreshold=15000         # 提高 C2 阈值
-XX:ReservedCodeCacheSize=32m       # 减小代码缓存
-XX:InitialCodeCacheSize=8m         # 减小初始缓存

# 极速启动 (短生命周期应用)
-XX:-TieredCompilation -Xcomp      # 预编译所有代码
-XX:CompileThreshold=1             # 立即编译
```

### 吞吐量优先配置

```bash
# 最大吞吐量 - 激进优化
-XX:+TieredCompilation             # 启用分层编译
-XX:CompileThreshold=5000          # 降低 C2 阈值
-XX:FreqInlineSize=300             # 降低热方法内联阈值
-XX:MaxInlineSize=50               # 增大内联限制
-XX:ReservedCodeCacheSize=512m      # 增大代码缓存
-XX:+UseSuperWord                  # 启用向量化
-XX:LoopUnrollLimit=80             # 增大循环展开
```

### 低延迟配置

```bash
# 低延迟 - 稳定性能
-XX:+UseG1GC                       # 使用 G1 GC
-XX:MaxGCPauseMillis=50            # 最大 GC 暂停
-XX:+UseStringDeduplication        # 字符串去重
-XX:+OptimizeStringConcat          # 字符串拼接优化
-XX:CompileThreshold=10000         # 标准编译阈值
-XX:+TieredCompilation             # 分层编译
```

### 内存受限配置

```bash
# 低内存环境
-XX:ReservedCodeCacheSize=64m      # 减小代码缓存
-XX:InitialCodeCacheSize=16m       # 减小初始缓存
-XX:TieredStopAtLevel=3            # 不使用 C2
-XX:MaxInlineSize=25               # 减小内联限制
```

### 容器环境配置

```bash
# 容器化环境 (Docker/Kubernetes)
-XX:+UseContainerSupport           # 容器感知 (默认)
-XX:MaxRAMPercentage=75.0          # 使用容器内存限制
-XX:InitialRAMPercentage=50.0      # 初始堆内存
-XX:MinRAMPercentage=50.0          # 最小堆内存
-XX:ActiveProcessorCount=2         # 限制 CPU 数

# 结合代码缓存
-XX:ReservedCodeCacheSize=128m     # 适中代码缓存
```

---

## 12. 参数速查表

### 常用场景

| 场景 | 参数 |
|------|------|
| **查看编译活动** | `-XX:+PrintCompilation` 或 `-Xlog:compilation=info` |
| **查看内联决策** | `-XX:+PrintInlining` 或 `-Xlog:inlining=info` |
| **查看编译时间** | `-XX:+CITime` |
| **禁用 C2** | `-XX:TieredStopAtLevel=3` |
| **只解释** | `-Xint` |
| **增大代码缓存** | `-XX:ReservedCodeCacheSize=512m` |
| **调整内联阈值** | `-XX:FreqInlineSize=300` |
| **导出 IR** | `-XX:PrintIdealGraphLevel=2` |
| **打印汇编** | `-XX:+PrintAssembly` |
| **快速启动** | `-XX:TieredStopAtLevel=1` |

### 参数类别速查

| 类别 | 关键参数 |
|------|----------|
| **编译器选择** | `-client`, `-server`, `-XX:+TieredCompilation` |
| **编译阈值** | `-XX:CompileThreshold`, `-XX:Tier4CompileThreshold` |
| **代码缓存** | `-XX:ReservedCodeCacheSize`, `-XX:+SegmentedCodeCache` |
| **内联控制** | `-XX:MaxInlineSize`, `-XX:FreqInlineSize` |
| **循环优化** | `-XX:LoopUnrollLimit`, `-XX:LoopMaxUnroll` |
| **逃逸分析** | `-XX:+DoEscapeAnalysis`, `-XX:+EliminateAllocations` |
| **向量化** | `-XX:+UseSuperWord`, `-XX:MaxVectorSize` |
| **诊断** | `-XX:+PrintCompilation`, `-Xlog:compilation=info` |

---

## 13. 相关链接

- [诊断工具](./diagnostics.md) - 如何使用这些参数
- [C2 优化阶段](./c2-phases.md) - 参数影响哪些阶段
- [性能调优](../performance/) - 更多 JVM 参数
- [分层编译](./tiered-compilation.md) - 分层编译详解
- [内联优化](./inlining.md) - 内联策略详解

---

## 14. 贡献者

本文档由社区维护，主要贡献者包括：
- [Vladimir Kozlov](/by-contributor/profiles/vladimir-kozlov.md) - C2 编译器架构
- [Tobias Hartmann](/by-contributor/profiles/tobias-hartmann.md) - JIT 编译器优化
- [Christian Hagedorn](/by-contributor/profiles/christian-hagedorn.md) - C2 编译器
- [Roman Kennke](/by-contributor/profiles/roman-kennke.md) - JIT 编译、Shenandoah

---

**最后更新**: 2026-03-21
