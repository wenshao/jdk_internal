# VM 参数参考

> HotSpot JIT 编译器完整参数手册

[← 返回 JIT 编译](../)

---

## 编译器选择

### 基础选择

```bash
-client                         # 使用 C1 (Client Compiler)
-server                        # 使用 C2 (Server Compiler, 默认 JDK 9+)
-XX:+TieredCompilation          # 启用分层编译 (默认)
-XX:-TieredCompilation         # 禁用分层编译
```

### Graal JIT

```bash
# 启用 Graal JIT (JDK 9+)
-XX:+UnlockExperimentalVMOptions
-XX:+UseJVMCICompiler
-XX:+EnableJVMCI
-XX:+UseGraalJIT               # 使用 Graal 替代 C2
-XX:-UseJVMCICompiler          # 禁用 JVMCI
```

---

## 编译阈值

### 分层编译阈值

```bash
# 各层编译阈值
-XX:Tier0InvokeNotifyFreqLog=7     # Level 0 调用频率对数
-XX:Tier1InvokeNotifyFreqLog=7     # Level 1 调用频率对数
-XX:Tier2InvokeNotifyFreqLog=14    # Level 2 调用频率对数
-XX:Tier3InvokeNotifyFreqLog=10    # Level 3 调用频率对数
-XX:Tier4CompileThreshold=5000     # Level 4 (C2) 调用阈值
-XX:CompileThreshold=10000         # 传统 C2 阈值 (非分层)
```

### 回边阈值 (循环)

```bash
-XX:OnStackReplacePercentage=140   # OSR (On-Stack Replacement) 比例
-XX:InterpreterProfilePercentage=33 # 解释器 profiling 比例
-XX:FreqInlineSize=325             # 热方法内联阈值 (字节码)
-XX:MaxInlineSize=35               # 最大内联方法大小 (字节码)
```

### 阈值说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `CompileThreshold` | 10000 | C2 编译需要的调用次数 |
| `Tier4CompileThreshold` | 5000 | 分层编译 C2 阈值 |
| `FreqInlineSize` | 325 | 热方法内联阈值 |
| `MaxInlineSize` | 35 | 最大可内联方法大小 |

---

## 代码缓存

### 缓存大小

```bash
# 代码缓存配置
-XX:InitialCodeCacheSize=256k      # 初始代码缓存
-XX:ReservedCodeCacheSize=240m     # 最大代码缓存 (默认)
-XX:CodeCacheExpansionSize=64k     # 扩展增量
-XX:MinCodeCacheSize=512k          # 最小代码缓存
```

### 分段代码缓存 (JDK 9+)

```bash
# 启用分段代码缓存 (默认)
-XX:+SegmentedCodeCache

# 各段大小
-XX:NonMethodCodeHeapSize=56m      # 非方法代码 (adapter, stubs)
-XX:ProfiledCodeHeapSize=41m       # Profiled 代码 (C1 编译)
-XX:NonProfiledCodeHeapSize=161m   # 非 Profiled 代码 (C2 编译)

# 查看代码缓存
-XX:+PrintCodeCache                # 打印代码缓存信息
-XX:+PrintCodeCacheOnCompilation   # 编译时打印代码缓存
```

### 代码缓存清理

```bash
-XX:+UseCodeCacheFlushing          # 启用代码缓存清理
-XX:MinCodeCacheFlushRatio=11      # 最小清理比例
-XX:CodeCacheFlushingMinimumFreeSpace=16m
```

---

## 内联控制

### 内联阈值

```bash
# 内联大小限制
-XX:MaxInlineSize=35               # 最大内联方法大小 (字节码)
-XX:FreqInlineSize=325             # 热方法内联阈值
-XX:MaxTrivialSize=6               # 平凡方法内联阈值 (getter/setter)
-XX:MaxRecursiveInlineSize=35      # 递归内联阈值
```

### 内联策略

```bash
-XX:InlineSmallCode=1000           # 小代码内联 (字节码)
-XX:+Inline                       # 启用内联 (默认)
-XX:-Inline                       # 禁用内联
-XX:CompileThreshold=10000         # 内联调用阈值
```

### 内联排除

```bash
# 排除特定方法内联
-XX:CompileCommand=exclude,java/lang/String.*
-XX:CompileCommand=exclude,*String.indexOf

# 只内联特定方法
-XX:CompileCommand=inline,java/lang/Math.*
-XX:CompileCommand=option,java/lang/Math.*,InlineLimit,100
```

---

## C2 特定参数

### 循环优化

```bash
# 循环优化控制
-XX:LoopUnrollLimit=60             # 循环展开限制
-XX:LoopOptsCount=30               # 循环优化迭代次数
-XX:LoopUnrollMin=2                # 最小展开次数
-XX:+UseLoopPredicate             # 循环谓词 (默认)
-XX:-UseLoopPredicate             # 禁用循环谓词

# 循环剥离
-XX:LoopMaxUnroll=16               # 最大循环展开次数
-XX:PeelIterations=0               # 循环剥离迭代次数
```

### Escape Analysis

```bash
# 逃逸分析
-XX:+DoEscapeAnalysis             # 启用逃逸分析 (默认)
-XX:+EliminateAllocations          # 消除分配 (默认)
-XX:+PrintEliminateAllocations     # 打印分配消除
-XX:+EliminateLocks               # 锁消除
-XX:+EliminateNullChecks           # 空值检查消除
```

### 向量化 (SuperWord)

```bash
# SuperWord 向量化
-XX:+UseSuperWord                 # 启用向量化 (默认)
-XX:MaxVectorSize=32               # 最大向量大小
-XX:+UseVectorStubs               # 向量化桩
-XX:VectorizeDebugOptions=0        # 向量化调试选项
-XX:+TraceSuperWord               # 跟踪向量化决策
```

### 类型特化

```bash
# 类型 profiling
-XX:+UseTypeSpeculation           # 类型推测 (默认)
-XX:+IgnoreUnrecognizedVMOptions   # 忽略未知选项
-XX:TypeProfileLevel=111           # 类型 profiling 级别
```

---

## 诊断参数

### 编译时间统计

```bash
# 编译时间
-XX:+CITime                       # 打印编译时间
-XX:+CITimeVerbose                # 详细编译时间
-XX:+PrintCompilation             # 打印编译活动 (简洁)
-XX:+PrintInlining                 # 打印内联决策
-XX:+UnlockDiagnosticVMOptions     # 解锁诊断选项
```

### 编译日志

```bash
# 日志输出
-XX:LogFile=compilation.log        # 日志文件
-XX:+PrintCompilation             # 打印编译活动
-XX:+PrintInlining                 # 打印内联决策
-XX:+PrintCodeCache                # 打印代码缓存
```

### IR 输出

```bash
# Ideal Graph 可视化
-XX:+PrintIdealGraphLevel          # 打印 IR 级别
-XX:PrintIdealGraphLevel=2         # IR 详细级别 (0-4)
-XX:PrintIdealGraphFile=ideal.xml  # IR 输出文件
-XX:PrintIdealGraphAddress=0x1234   # 打印特定地址的 IR

# IGV (Ideal Graph Visualizer)
-XX:+PrintIdealGraphAtLineNumber=123
-XX:+PrintIdealGraphFile           # 生成 IGV 文件
```

### 编译命令

```bash
# 编译规则
-XX:CompileCommand=print,*String.*     # 打印 String 类的编译
-XX:CompileCommand=exclude,*.*         # 排除所有编译
-XX:CompileCommand=inline,java/lang/Math.*  # 强制内联
-XX:CompileCommand=dontinline,java/lang/String.indexOf

# 打印汇编
-XX:+PrintAssembly                  # 需要 hsdis 库
-XX:+PrintOptoAssembly              # 打印优化后的汇编
-XX:PrintAssemblyOptions=intel      # 汇编语法 (intel/att)
```

---

## Stress 模式

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
```

---

## 性能调优建议

### 启动优先

```bash
# 快速启动 (减少编译)
-XX:TieredStopAtLevel=1            # 只用 C1
-XX:CompileThreshold=15000         # 提高 C2 阈值
-XX:ReservedCodeCacheSize=32m       # 减小代码缓存
```

### 吞吐量优先

```bash
# 最大吞吐量
-XX:+TieredCompilation             # 启用分层编译
-XX:CompileThreshold=5000          # 降低 C2 阈值
-XX:FreqInlineSize=300             # 降低热方法内联阈值
-XX:ReservedCodeCacheSize=512m      # 增大代码缓存
```

### 低延迟

```bash
# 低延迟 (减少 GC 暂停)
-XX:+UseG1GC
-XX:MaxGCPauseMillis=50
-XX:+UseStringDeduplication        # 字符串去重
-XX:+OptimizeStringConcat          # 字符串拼接优化
```

---

## 参数速查表

| 场景 | 参数 |
|------|------|
| **查看编译活动** | `-XX:+PrintCompilation` |
| **查看内联决策** | `-XX:+PrintInlining` |
| **查看编译时间** | `-XX:+CITime` |
| **禁用 C2** | `-XX:TieredStopAtLevel=3` |
| **只解释** | `-Xint` |
| **增大代码缓存** | `-XX:ReservedCodeCacheSize=512m` |
| **调整内联阈值** | `-XX:FreqInlineSize=300` |
| **导出 IR** | `-XX:PrintIdealGraphLevel=2` |
| **打印汇编** | `-XX:+PrintAssembly` |

---

## 相关链接

- [诊断工具](../diagnostics.md) - 如何使用这些参数
- [C2 优化阶段](../c2-phases.md) - 参数影响哪些阶段
- [JVM 调优](../../jvm/) - 更多 JVM 参数
