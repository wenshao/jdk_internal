# GraalVM 调试和诊断工具

> GraalVM 性能分析、调试和故障排查的完整指南

[← 返回 GraalVM 首页](./) | [← 返回源码解读](source-code.md)

---
## 目录

1. [调试工具总览](#1-调试工具总览)
2. [IGV (Ideal Graph Visualizer)](#2-igv-ideal-graph-visualizer)
3. [Graal 编译器日志](#3-graal-编译器日志)
4. [Async Profiler](#4-async-profiler)
5. [JFR (Java Flight Recorder)](#5-jfr-java-flight-recorder)
6. [Native Image 调试](#6-native-image-调试)
7. [jcmd 诊断命令](#7-jcmd-诊断命令)
8. [故障排查流程](#8-故障排查流程)
9. [调试配置模板](#9-调试配置模板)
10. [相关链接](#10-相关链接)

---


## 1. 调试工具总览

```
┌─────────────────────────────────────────────────────────────────┐
│                  GraalVM 调试工具矩阵                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  编译器调试                                                     │
│  ├── IGV (Ideal Graph Visualizer)      ← 图可视化              │
│  ├── Graal Compiler Log                ← 编译日志              │
│  └── Debug Context                     ← 调试上下文            │
│                                                                 │
│  性能分析                                                       │
│  ├── Async Profiler                    ← CPU/内存分析          │
│  ├── JFR (Java Flight Recorder)        ← 飞行记录器            │
│  └── JMH (Java Microbenchmark Harness) ← 微基准测试            │
│                                                                 │
│  Native Image 调试                                             │
│  ├── Native Image Agent                  ← 配置生成            │
│  ├── Build Output Analysis               ← 构建分析            │
│  └── Runtime Debugging                   ← 运行时调试          │
│                                                                 │
│  通用工具                                                       │
│  ├── jcmd                              ← JVM 诊断命令           │
│  ├── jstack                            ← 线程堆栈              │
│  └── jmap                              ← 内存映射              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. IGV (Ideal Graph Visualizer)

### 什么是 IGV?

IGV 是 GraalVM 的**图可视化调试工具**，可以查看 Graal 编译器的中间表示 (IR)。

```
┌─────────────────────────────────────────────────────────────────┐
│                      IGV 界面示意                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Methods                    Graph View                          │
│  ────────                   ──────────                          │
│  ├─ Main.main()             ┌──────────────┐                   │
│  ├─ Calculator.compute()    │  StartNode   │                   │
│  └─ ...                     └──────┬───────┘                   │
│                                    │                            │
│  Compilation Phases           ┌────┴────┐                      │
│  ──────────────────           │         │                       │
│  ├─ Before Inlining         ┌─▼─┐   ┌─▼─┐                     │
│  ├─ After Inlining         │ A │   │ B │                      │
│  ├─ After Optimization     └─┬─┘   └─┬─┘                      │
│  └─ Final Graph              │         │                       │
│                              └────┬────┘                      │
│                                   │                            │
│                              ┌────▼────┐                      │
│                              │ Return  │                       │
│                              └─────────┘                       │
│                                                                 │
│  Properties Panel                                               │
│  ─────────────────                                              │
│  Node Type: AddNode                                             │
│  Inputs: [x, y]                                                 │
│  Usages: [z]                                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 安装 IGV

```bash
# 方法 1: GraalVM 自带 (推荐)
$GRAALVM_HOME/bin/igv

# 方法 2: 独立下载
wget https://github.com/graalvm/igv/releases/latest/download/igv.zip
unzip igv.zip
./igv/bin/igv

# 方法 3: SDKMAN
sdk install visualvm
```

### 使用 IGV

```bash
# 启用图转储
java \
  -Dgraal.Dump=:2 \
  -Dgraal.PrintGraph=Network \
  -jar app.jar

# 查看特定方法的图
java \
  -Dgraal.Dump=MyClass.myMethod:2 \
  -jar app.jar

# 查看特定优化阶段的图
java \
  -Dgraal.Dump=Inlining:2 \
  -Dgraal.DumpPath=/tmp/graal-dumps \
  -jar app.jar
```

### IGV 视图解读

```
节点颜色说明:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  🟦 蓝色 = Fixed Node (控制流节点)                              │
│     • MethodStart, Return, If, Loop                             │
│                                                                 │
│  🟩 绿色 = Floating Node (数据流节点)                           │
│     • Add, Multiply, Load, Store                                │
│                                                                 │
│  🟥 红色 = Deoptimize Node (去优化节点)                         │
│     • UncommonTrap, Deoptimize                                  │
│                                                                 │
│  🟨 黄色 = Constant Node (常量节点)                             │
│     • Constant, Null, True, False                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

边的类型:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ─────→ = Control Edge (控制流边)                               │
│                                                                 │
│  ······> = Data Edge (数据流边)                                 │
│                                                                 │
│  - - - -> = Exception Edge (异常边)                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Graal 编译器日志

### 启用编译日志

```bash
# 基础日志
java \
  -Dgraal.LogFile=graal.log \
  -Dgraal.LogLevel=INFO \
  -jar app.jar

# 详细日志
java \
  -Dgraal.LogFile=graal.log \
  -Dgraal.LogLevel=FINE \
  -Dgraal.TraceInlining=true \
  -Dgraal.TraceEscapeAnalysis=true \
  -jar app.jar

# 诊断日志
java \
  -Dgraal.LogFile=graal.log \
  -Dgraal.LogLevel=FINEST \
  -Dgraal.Dump=:2 \
  -Dgraal.PrintCompilation=true \
  -jar app.jar
```

### 日志级别

| 级别 | 说明 | 输出量 |
|------|------|--------|
| **OFF** | 禁用日志 | 无 |
| **SEVERE** | 严重错误 | 极少 |
| **WARNING** | 警告 | 少 |
| **INFO** | 一般信息 | 中等 |
| **FINE** | 详细调试 | 多 |
| **FINER** | 更详细 | 很多 |
| **FINEST** | 最详细 | 极多 |

### 日志分析

```
示例日志输出:
┌─────────────────────────────────────────────────────────────────┤
│ graal.log                                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ [INFO] Compiling method: com.example.Calculator.compute()      │
│ [INFO]   Bytecodes: 45                                         │
│ [INFO]   Inlining depth: 5                                     │
│ [FINE] Inlined: com.example.Utils.add() @ bci 12               │
│ [FINE] Inlined: com.example.Utils.multiply() @ bci 28          │
│ [INFO] Optimization phases: 15                                  │
│ [FINE] Escape analysis: 3 objects scalar replaced              │
│ [INFO] Generated code: 512 bytes                               │
│ [INFO] Compilation time: 25ms                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Async Profiler

### 安装 Async Profiler

```bash
# GitHub 下载
wget https://github.com/jvm-profiling-tools/async-profiler/releases/latest/download/async-profiler-2.9-linux-x64.tar.gz
tar xzf async-profiler-2.9-linux-x64.tar.gz

# 或使用 SDKMAN
sdk install async-profiler
```

### CPU 性能分析

```bash
# 开始 profiling
./profiler.sh start <pid>

# 运行 30 秒后停止
./profiler.sh stop -d 30 -f profile.html <pid>

# 生成火焰图
./profiler.sh start --event cpu --interval 1ms <pid>
./profiler.sh stop --format flamegraph --file cpu-flame.html <pid>
```

### 内存分配分析

```bash
# 分析对象分配
./profiler.sh start --event alloc --interval 512k <pid>
./profiler.sh stop --format flamegraph --file alloc-flame.html <pid>

# 查看 GC 根源
./profiler.sh start --event itimer <pid>
./profiler.sh stop --format tree --file gc-tree.txt <pid>
```

### Graal 特定分析

```bash
# 分析 Graal 编译时间
./profiler.sh start --event cpu --filter java.*graal.* <pid>
./profiler.sh stop -f graal-profile.html <pid>

# 分析 JIT 编译
./profiler.sh start --event jit-compile <pid>
./profiler.sh stop -f jit-profile.html <pid>
```

---

## 5. JFR (Java Flight Recorder)

### 启用 JFR

```bash
# 基础 JFR 录制
java \
  -XX:StartFlightRecording=filename=recording.jfr,duration=60s \
  -jar app.jar

# 详细 JFR 录制
java \
  -XX:StartFlightRecording=filename=recording.jfr,\
    duration=60s,\
    settings=profile \
  -jar app.jar

# 持续录制 (用于生产环境)
java \
  -XX:StartFlightRecording=filename=recording.jfr,\
    duration=continuous,\
    disk=true,\
    maxsize=1GB \
  -jar app.jar
```

### JFR 事件

| 事件类别 | 事件示例 | 用途 |
|----------|----------|------|
| **Code** | CodeSweeperStats | 代码扫描统计 |
| **JVM** | JVMStatistics | JVM 统计 |
| **GC** | GCHeapSummary | GC 堆摘要 |
| **JIT** | Compilation | 编译事件 |
| **Execution** | ExecutionSample | 执行采样 |

### 分析 JFR 录制

```bash
# 使用 JMC (Java Mission Control) 分析
jmc recording.jfr

# 使用 jfr 命令行工具
jfr print recording.jfr

# 使用 async-profiler 转换
./profiler.sh convert recording.jfr -f jfr-flame.html
```

---

## 6. Native Image 调试

### 构建时调试

```bash
# 详细构建日志
native-image \
  --verbose \
  -jar app.jar

# 输出分析树
native-image \
  -H:PrintAnalysisCallTree=calltree.txt \
  -jar app.jar

# 查看包含的类
native-image \
  -H:PrintClassInitialization=classes.txt \
  -jar app.jar

# 查看资源文件
native-image \
  -H:PrintRuntimeInitialization=runtime-init.txt \
  -jar app.jar
```

### Native Image Agent

```bash
# 1. 使用 agent 运行应用
java \
  -agentlib:native-image-agent=config-output-dir=config/ \
  -jar app.jar

# 执行所有功能，触发反射调用
# 访问所有 API 端点
# 运行所有测试

# 2. 查看生成的配置
ls config/
# ├── jni-config.json
# ├── proxy-config.json
# ├── reflection-config.json
# └── resource-config.json

# 3. 使用配置编译
native-image \
  -H:ConfigurationFileDirectories=config/ \
  -jar app.jar
```

### 运行时调试

```bash
# 启用详细日志
./app \
  -Dpolyglot.log.level=FINE \
  -Dgraal.LogFile=graal.log

# 使用 GDB 调试
gdb ./app
(gdb) run
(gdb) bt  # 崩溃时查看堆栈

# 启用核心转储
ulimit -c unlimited
# 崩溃后生成 core 文件
gdb ./app core
```

---

## 7. jcmd 诊断命令

### 查看 Graal 编译统计

```bash
# 查看编译统计
jcmd <pid> VM.compiler -stat

# 查看编译队列
jcmd <pid> VM.compiler -queue

# 查看代码缓存
jcmd <pid> VM.code_cache
```

### 查看 JVMCI 状态

```bash
# 查看 JVMCI 编译器状态
jcmd <pid> VM.jvmci -stat

# 查看 JVMCI 编译统计
jcmd <pid> VM.jvmci -compiler
```

### 生成线程转储

```bash
# 生成线程转储
jcmd <pid> Thread.print

# 包含锁信息
jcmd <pid> Thread.print -l

# 生成 JSON 格式
jcmd <pid> Thread.print -j
```

---

## 8. 故障排查流程

### 性能问题排查

```
┌─────────────────────────────────────────────────────────────────┐
│                  性能问题排查流程                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 确认问题                                                    │
│     • 启动慢？峰值性能低？内存占用高？                          │
│                                                                 │
│  2. 收集数据                                                    │
│     • JFR 录制 60 秒                                              │
│     • Async Profiler CPU 分析                                    │
│     • GC 日志分析                                                 │
│                                                                 │
│  3. 分析瓶颈                                                    │
│     • 热点方法识别                                              │
│     • GC 频率分析                                                 │
│     • 编译时间分析                                              │
│                                                                 │
│  4. 应用优化                                                    │
│     • 调整编译参数                                              │
│     • 优化 GC 配置                                                │
│     • 使用 Native Image                                         │
│                                                                 │
│  5. 验证效果                                                    │
│     • 基准测试对比                                              │
│     • 性能回归检测                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 内存问题排查

```bash
# 1. 启用 GC 日志
java -Xlog:gc*:file=gc.log -jar app.jar

# 2. 查看堆使用
jcmd <pid> GC.heap_info

# 3. 生成堆转储
jcmd <pid> GC.heap_dump /tmp/heap.hprof

# 4. 分析堆转储
jhat /tmp/heap.hprof
# 或使用 Eclipse MAT
mat heap.hprof
```

### 编译问题排查

```bash
# 1. 启用编译日志
java -Dgraal.LogLevel=FINE -jar app.jar

# 2. 查看编译失败
grep -i "fail" graal.log

# 3. 查看去优化
grep -i "deopt" graal.log

# 4. 使用 IGV 查看问题图
java -Dgraal.Dump=:2 -jar app.jar
```

---

## 9. 调试配置模板

### 开发环境

```bash
java \
  # Graal 调试
  -Dgraal.LogFile=graal.log \
  -Dgraal.LogLevel=FINE \
  -Dgraal.PrintCompilation=true \
  \
  # JFR
  -XX:StartFlightRecording=filename=recording.jfr,\
    duration=continuous,\
    settings=profile \
  \
  # GC 日志
  -Xlog:gc*:file=gc.log \
  \
  -jar app.jar
```

### 生产环境

```bash
java \
  # JFR (低开销)
  -XX:StartFlightRecording=filename=recording.jfr,\
    duration=1h,\
    disk=true,\
    maxsize=500MB \
  \
  # GC 日志
  -Xlog:gc*:file=gc.log:time,uptime,level,tags \
  \
  # 错误日志
  -XX:+HeapDumpOnOutOfMemoryError \
  -XX:HeapDumpPath=/var/log/heapdumps/ \
  \
  -jar app.jar
```

---

## 10. 相关链接

### 工具下载
- [IGV](https://github.com/graalvm/igv)
- [Async Profiler](https://github.com/jvm-profiling-tools/async-profiler)
- [JMC](https://jdk.java.net/jmc/)

### 文档
- [GraalVM Debugging](https://www.graalvm.org/latest/docs/developers-guide/debugging/)
- [Async Profiler 使用指南](https://github.com/jvm-profiling-tools/async-profiler/wiki)
- [JFR 官方文档](https://docs.oracle.com/en/java/javase/21/jfapi/java-flight-recorder.html)

---

**最后更新**: 2026-03-21
