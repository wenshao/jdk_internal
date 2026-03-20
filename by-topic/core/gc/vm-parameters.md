# GC VM 参数参考

> 垃圾收集器参数完整指南

[← 返回 GC](../)

---

## 选择 GC

### GC 选择器

```bash
# Serial GC
-XX:+UseSerialGC

# Parallel GC
-XX:+UseParallelGC

# G1 GC (JDK 9+ 默认)
-XX:+UseG1GC

# ZGC
-XX:+UseZGC

# Shenandoah GC
-XX:+UseShenandoahGC
```

### 查看当前 GC

```bash
# 打印所有 VM 标志
java -XX:+PrintCommandLineFlags -version

# 只看 GC
java -XX:+PrintCommandLineFlags -version | grep -E 'Use.*GC'
```

---

## 通用 GC 参数

### 堆大小

```bash
# 初始堆大小
-Xms2g
-XX:InitialHeapSize=2g

# 最大堆大小
-Xmx4g
-XX:MaxHeapSize=4g

# 新生代大小
-Xmn1g
-XX:MaxNewSize=1g
-XX:NewSize=256m
-XX:MaxNewSize=512m

# 幸存区比例
-XX:SurvivorRatio=8               # Eden:S0:S1 = 8:1:1
-XX:TargetSurvivorRatio=50        # 幸存区目标使用率
```

### GC 线程

```bash
# 并行 GC 线程
-XX:ParallelGCThreads=8           # STW 阶段线程数
-XX:ConcGCThreads=4               # 并发阶段线程数

# 自适应 (通常不需要设置)
-XX:+UseDynamicNumberOfGCThreads  # 动态调整线程数
-XX:ParallelGCThreads=0           # 自动选择
```

### GC 日志

```bash
# JDK 9+ 统一日志
-Xlog:gc                          # 基本 GC 日志
-Xlog:gc*:file=gc.log:level,tags  # 详细 GC 日志

# 包含时间戳
-Xlog:gc*:file=gc.log:time,level,tags

# 包含 uptime
-Xlog:gc*:file=gc.log:uptime,time,level,tags

# 按标签过滤
-Xlog:gc+heap=debug               # 堆相关
-Xlog:gc+ref=debug                # 引用处理
-Xlog:gc+ergo=debug               # 启发式决策
```

### 代码缓存

```bash
# 代码缓存大小
-XX:ReservedCodeCacheSize=256m    # 预留代码缓存
-XX:InitialCodeCacheSize=32m      # 初始代码缓存

# 代码缓存刷新
-XX:+UseCodeCacheFlushing         # 启用代码缓存刷新
-XX:MinCodeCacheFlushingInterval=100  # 刷新间隔 (ms)
```

---

## Serial GC 参数

```bash
# 基础
-XX:+UseSerialGC

# 线程
-XX:ParallelGCThreads=1           # 单线程

# 新生代
-XX:SurvivorRatio=8
-XX:TargetSurvivorRatio=50
```

---

## Parallel GC 参数

### 基础配置

```bash
# 启用
-XX:+UseParallelGC

# 吞吐量目标
-XX:GCTimeRatio=99                # GC 时间占比 1/(1+99) = 1%
-XX:MaxGCPauseMillis=200          # 最大暂停时间
```

### 新生代

```bash
# 新生代大小
-XX:NewSize=256m
-XX:MaxNewSize=512m
-XX:SurvivorRatio=8

# 年龄阈值
-XX:MaxTenuringThreshold=15       # 晋升阈值
-XX:+PrintTenuringDistribution    # 打印年龄分布
```

### 老年代

```bash
# 老年代配置
-XX:OldSize=512m
-XX:MaxOldSize=2g

# 触发阈值
-XX:MaxHeapFreeRatio=70           # 老年代最大空闲比例
-XX:MinHeapFreeRatio=40           # 老年代最小空闲比例
```

---

## G1 GC 参数

### 基础配置

```bash
# 启用
-XX:+UseG1GC

# 目标暂停时间
-XX:MaxGCPauseMillis=200          # 目标最大暂停 (ms)
-XX:GCPauseIntervalMillis=5000    # 期望暂停间隔 (ms)

# Region 大小
-XX:G1HeapRegionSize=16m          # 1MB-32MB, 2 的幂
```

### 调优参数

```bash
# 并发标记
-XX:InitiatingHeapOccupancyPercent=45  # 并发标记触发阈值
-XX:ConcGCThreads=4                     # 并发标记线程数

# Mixed GC
-XX:G1MixedGCCountTarget=8              # Mixed GC 目标次数
-XX:G1OldCSetRegionThreshold=2          # Old Region 回收阈值

# 保留堆
-XX:G1ReservePercent=10                 # 保留堆比例
```

### 特殊场景

```bash
# Humongous 对象
-XX:G1HumongousObjectThreshold=8m       # 大对象阈值

# String 去重 (JDK 8u20+)
-XX:+UseStringDeduplication             # 启用 String 去重
-XX:StringDeduplicationAgeThreshold=3   # 去重年龄阈值
```

---

## ZGC 参数

### 基础配置

```bash
# 启用
-XX:+UseZGC

# 分代 ZGC (JDK 21+)
-XX:+ZGenerational                     # 启用分代 (JDK 23+ 默认)
```

### 调优参数

```bash
# GC 触发
-XX:ZCollectionInterval=5               # 自动 GC 间隔 (秒)
-XX:ZAllocationSpikeTolerance=2.0       # 分配尖刺容忍度

# 碎片控制
-XX:ZFragmentationLimit=25              # 碎片率阈值 (%)
```

### NUMA (JDK 21+)

```bash
# NUMA 支持
-XX:+UseNUMA                            # 启用 NUMA
-XX:+UseNUMAInterleaving                # NUMA 交错分配
```

### 线程

```bash
# GC 线程
-XX:ParallelGCThreads=8                 # GC 工作线程
-XX:ConcGCThreads=4                     # 并发标记线程
```

---

## Shenandoah GC 参数

### 基础配置

```bash
# 启用
-XX:+UseShenandoahGC
```

### 启发式算法

```bash
# 自适应 (默认)
-XX:ShenandoahGCHeuristics=adaptive

# 静态
-XX:ShenandoahGCHeuristics=static

# 紧凑
-XX:ShenandoahGCHeuristics=compact

# 激进
-XX:ShenandoahGCHeuristics=aggressive

# 分代 (JDK 21+)
-XX:ShenandoahGCHeuristics=generational
```

### 调优参数

```bash
# Region 大小
-XX:ShenandoahMinRegionSize=256k
-XX:ShenandoahMaxRegionSize=32m

# GC 触发
-XX:ShenandoahGCThreshold=0             # GC 触发阈值
-XX:ShenandoahFreeThreshold=10          # 空闲阈值 (%)

# 引用更新
-XX:ShenandoahUpdateRefsEarly=true      # 提前更新引用
```

---

## 诊断参数

### GC 日志

```bash
# 基础日志
-XX:+PrintGC                            # 打印 GC 日志
-XX:+PrintGCDetails                     # 详细 GC 信息
-XX:+PrintGCTimeStamps                  # GC 时间戳
-XX:+PrintGCApplicationStoppedTime      # 应用暂停时间

# 堆信息
-XX:+PrintHeapAtGC                      # GC 时打印堆
-XX:+PrintStringDeduplicationStatistics # String 去重统计
```

### 统计信息

```bash
# 编译时间
-XX:+CITime                             # 打印编译时间
-XX:+CITimeVerbose                      # 详细编译时间

# GC 统计
-XX:+PrintGCStatistics                  # GC 统计信息
-XX:+PrintGCTaskTimeStamps              # GC 任务时间戳
```

###OOM 处理

```bash
# OOM 时转储
-XX:+HeapDumpOnOutOfMemoryError         # OOM 时转储堆
-XX:HeapDumpPath=/tmp/heap.hprof        # 转储路径
-XX:+ExitOnOutOfMemoryError             # OOM 时退出
-XX:+CrashOnOutOfMemoryError            # OOM 时崩溃
-XX:OnOutOfMemoryError="<cmd>"          # OOM 时执行命令
```

---

## 实验性参数

### 启用诊断选项

```bash
-XX:+UnlockDiagnosticVMOptions          # 解锁诊断选项
-XX:+PrintSafepointStatistics           # Safepoint 统计
-XX:+LogCompilation                     # 日志编译
-XX:+PrintAssembly                      # 打印汇编 (需要 hsdis)
```

### 调试选项

```bash
# GC 调试
-XX:+VerifyBeforeGC                    # GC 前验证
-XX:+VerifyAfterGC                     # GC 后验证
-XX:+VerifyDuringGC                    # GC 中验证

# 栈跟踪
-XX:+TraceSafepoint                     # 追踪 Safepoint
-XX:+TraceGC                            # 追踪 GC
```

---

## 快速参考

### 选择 GC 决策树

```
大堆 (>16GB) + 低延迟 (<10ms)
  ├── ZGC (x86_64, aarch64)
  └── Shenandoah (多平台)

通用服务器应用
  └── G1 GC (默认)

单核/小内存
  └── Serial GC

吞吐优先/批处理
  └── Parallel GC
```

### 常用组合

```bash
# 低延迟 (ZGC)
-XX:+UseZGC -XX:+ZGenerational

# 平衡 (G1)
-XX:+UseG1GC -XX:MaxGCPauseMillis=200

# 吞吐优先 (Parallel)
-XX:+UseParallelGC -XX:GCTimeRatio=99

# 小内存 (Serial)
-XX:+UseSerialGC -Xms128m -Xmx256m
```

---

## 相关链接

- [G1 GC 详解](g1-gc.md) - G1 专用参数
- [ZGC 详解](zgc.md) - ZGC 专用参数
- [Shenandoah 详解](shenandoah.md) - Shenandoah 专用参数
- [调优指南](tuning.md) - GC 调优策略
