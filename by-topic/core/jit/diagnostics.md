# 诊断工具

> JIT 编译调试、性能分析和问题排查

[← 返回 JIT 编译](../)

---
## 目录

1. [编译日志](#1-编译日志)
2. [Ideal Graph Visualizer (IGV)](#2-ideal-graph-visualizer-igv)
3. [jcmd 诊断](#3-jcmd-诊断)
4. [jhsdb (JDK 9+)](#4-jhsdb-jdk-9)
5. [JFR (Java Flight Recorder)](#5-jfr-java-flight-recorder)
6. [Perf / perf-map (Linux)](#6-perf--perf-map-linux)
7. [常见诊断场景](#7-常见诊断场景)
8. [调试技巧](#8-调试技巧)
9. [性能分析](#9-性能分析)
10. [相关链接](#10-相关链接)

---


## 1. 编译日志

### PrintCompilation

**基础编译日志**:
```bash
-XX:+PrintCompilation
```

**输出示例**:
```
     199   35   java.lang.String::charAt (8 bytes)
     200   36   java.lang.String::indexOf (14 bytes)
```
格式: `序号 编译级别 方法名 (字节码大小)`

### PrintInlining

**内联决策日志**:
```bash
-XX:+PrintInlining
```

**输出示例**:
```
@ 36 java.lang.String::indexOf (14 bytes)
  inline (hot)
  @ 35 java.lang.String::charAt (8 bytes)
    inline (hot)
```

### 详细日志组合

```bash
# 完整编译诊断
-XX:+PrintCompilation
-XX:+PrintInlining
-XX:+UnlockDiagnosticVMOptions
-XX:+CITime
-XX:+CITimeVerbose
```

---

## 2. Ideal Graph Visualizer (IGV)

### 导出 IR

```bash
# 导出 Ideal Graph 到 XML
-XX:PrintIdealGraphLevel=2
-XX:PrintIdealGraphFile=ideal.xml

# 特定方法
-XX:CompileCommand=print,java/lang/String.indexOf
-XX:PrintIdealGraphAtLineNumber=123
```

### IGV 使用

1. 下载 [Ideal Graph Visualizer](https://github.com/JetBrains/ideal-graph-viewer)
2. 打开 XML 文件
3. 查看优化阶段的 IR 变化

**快捷键**:
- `Ctrl + +`: 放大
- `Ctrl + -`: 缩小
- `F`: 自动布局
- `Ctrl + F`: 查找节点

---

## 3. jcmd 诊断

### 编译队列

```bash
# 查看编译队列
jcmd <pid> Compiler.queue

# 查看编译器统计
jcmd <pid> Compiler.codecache

# 查看编译器配置
jcmd <pid> Compiler.config

# 强制编译方法
jcmd <pid> Compiler.compile <class> <method>
```

### 方法数据

```bash
# 查看 MethodData (profiling 信息)
jcmd <pid> VM.methodMetadata <class> <method>
jcmd <pid> VM.print_metaspace

# 查看编译任务
jcmd <pid> Compiler.directives_add
```

---

## 4. jhsdb (JDK 9+)

### 基本使用

```bash
# 启动 clhsdb
jhsdb clhsdb --pid <pid>

# 或 attach 到进程
jhsdb attach <pid>
```

### clhsdb 命令

```bash
# 代码缓存
> printcodecache                   # 打印代码缓存
> printcodememory                  # 打印代码内存

# 方法相关
> printmdo <MethodData address>    # 打印 MethodData
> printmethod <Method address>      # 打印 Method
> printcodecache                   # 代码缓存信息

# JIT 相关
> printcompiledcode                # 打印已编译代码
> printaot                         # 打印 AOT 代码
> printmetadata                     # 打印元数据

# 内存转储
> memdump <file>                   # 内存转储
> heapdump <file>                  # 堆转储

# 其他
> help                             # 帮助
> quit                             # 退出
```

### 示例会话

```bash
$ jhsdb clhsdb --pid 12345
hsdb> printcodecache
Code Cache:
  [...]
  [0x00007f8b40000000-0x00007f8b40008000, 32768 bytes, 1 chunks, 100% used
  [...]
hsdb> quit
```

---

## 5. JFR (Java Flight Recorder)

### JIT 相关事件

```bash
# 开始 JFR 记录
jcmd <pid> JFR.start name=jit dumponexit=true

# 指定 JIT 事件
jcmd <pid> JFR.start name=jit \
  jdk.CITime=true \
  jdk.CICompiler=true \
  jdk.CodeCache=true \
  jdk.Inlining=true

# 导出记录
jcmd <pid> JFR.dump name=jit filename=jit.jfr

# 停止记录
jcmd <pid> JFR.stop name=jit
```

### 关键事件

| 事件 | 说明 |
|------|------|
| `jdk.CITime` | 各阶段编译时间 |
| `jdk.CICompiler` | 编译器活动 |
| `jdk.CodeCache` | 代码缓存状态 |
| `jdk.CodeSweeper` | 代码清理活动 |
| `jdk.Inlining` | 内联决策 |

### 分析 JFR

使用 JDK Mission Control 或 `jfr` 命令行工具:

```bash
# 查看事件
jfr print --events jdk.CITime jit.jfr
jfr summary jit.jfr
```

---

## 6. Perf / perf-map (Linux)

### 火焰图

```bash
# 记录 perf
perf record -F 99 -a -g -- sleep 60

# 生成火焰图
perf script | FlameGraph/stackcollapse-perf.pl | \
  FlameGraph/flamegraph.pl > flame.svg
```

### JIT 编译代码映射

```bash
# 生成 perf-map 文件
jcmd <pid> VM.perfmap_print > /tmp/perf-<pid>.map
```

---

## 7. 常见诊断场景

### 场景 1: 方法未编译

**症状**: 方法执行慢，未达到编译阈值

**诊断**:
```bash
-XX:+PrintCompilation
-XX:+PrintInlining
-XX:CompileThreshold=1000  # 降低阈值测试
```

**解决方案**:
```bash
# 降低编译阈值
-XX:CompileThreshold=1000

# 预热
-XX:CompileThreshold=500
-XX:FreqInlineSize=100
```

### 场景 2: 内联失败

**症状**: 小方法调用开销大

**诊断**:
```bash
-XX:+PrintInlining
-XX:MaxInlineSize=100  # 增加内联阈值测试
```

**解决方案**:
```bash
# 强制内联
-XX:CompileCommand=inline,<class>.<method>
-XX:MaxInlineSize=100
```

### 场景 3: 代码缓存满

**症状**: 日志显示 "CodeCache is full"

**诊断**:
```bash
-XX:+PrintCodeCache
-XX:ReservedCodeCacheSize=512m  # 增大测试
```

**解决方案**:
```bash
-XX:ReservedCodeCacheSize=512m
-XX:+UseCodeCacheFlushing
```

### 场景 4: 编译时间长

**症状**: 某些方法编译卡住

**诊断**:
```bash
-XX:+CITime
-XX:+PrintCompilation
```

**解决方案**:
```bash
# 排除大方法编译
-XX:DontCompileHugeMethods=true
-XX:FreqInlineSize=200
-XX:MaxInlineSize=50
```

### 场景 5: C2 崩溃

**症状**: hs_err_pid.log 显示 C2 崩溃

**诊断**:
```bash
# 检查错误日志
cat hs_err_pid.log | grep "Current CompileTask"

# 复现编译
-XX:CompileCommand=exclude,<class>.<method>
```

**解决方案**:
```bash
# 排除问题方法
-XX:CompileCommand=exclude,<class>.<method>

# 降级到 C1
-XX:TieredStopAtLevel=3
```

---

## 8. 调试技巧

### 条件编译

```bash
# 只编译特定方法
-XX:CompileCommand=option,java/lang/String.*,CompileOnly,true
-XX:CompileCommand=exclude,*

# 打印特定方法
-XX:CompileCommand=print,*String.*
```

### 重复编译

```bash
# 重复编译 (测试编译器稳定性)
-XX:+RepeatCompilation
-XX:RepeatCompilationCount=3
```

### JIT 编译验证

```bash
# 编译器验证 (调试用)
-XX:+VerifyCompileOnly            # 只验证不优化
-XX:+CompileTheWorld              # 编译所有方法
-XX:+CompileTheWorldSafely         # 安全模式
```

---

## 9. 性能分析

### 编译时间分析

```bash
# 打印各阶段编译时间
-XX:+CITime
-XX:+CITimeVerbose
```

**输出示例**:
```
     _    total time    compiled method name
     2      0.023       35   java.lang.String::charAt
     3      0.045       36   java.lang.String::indexOf
```

### 内联分析

```bash
# 详细内联日志
-XX:+PrintInlining -XX:+PrintCompilation
```

### 代码缓存分析

```bash
# 代码缓存统计
-XX:+PrintCodeCache
-XX:+PrintCodeCacheOnCompilation
```

---

## 10. 相关链接

- [VM 参数](vm-parameters.md) - 诊断参数配置
- [C2 优化阶段](c2-phases.md) - 诊断特定阶段
- [性能调优](../performance/) - 更多诊断工具

---

**最后更新**: 2026-03-21

### 贡献者

| 贡献者 | 领域 | 组织 |
|--------|------|------|
| [Igor Veresov](/by-contributor/profiles/igor-veresov.md) | 编译器诊断 | Oracle |
| [David Holmes](/by-contributor/profiles/david-holmes.md) | JVM 工具 | Oracle |
