# JVM 调优与监控时间线

JVM 参数、调优工具和监控技术从 JDK 1.0 到 JDK 26 的演进。

---

## 时间线概览

```
JDK 1.0 ──── JDK 5 ──── JDK 6 ──── JDK 7 ──── JDK 8 ──── JDK 11 ──── JDK 17 ──── JDK 21 ──── JDK 26
 │            │           │           │           │           │           │           │           │
-verbose      JMX         jstat       G1 GC      Metaspace   JFR         ZGC         分代ZGC     智能调优
-Xmx         jconsole    jmap        Compressed String      JMC         Shenandoah   JFR增强     AI诊断
-Xms         JUC         jinfo       Oops       Dedup
```

---

## JVM 参数分类

### 标准参数 (-)

```bash
# 所有 JDK 版本支持
java -version
java -help
java -showversion
java -cp <classpath>
java -classpath <classpath>
java -D<property>=<value>
java -XshowSettings:properties
```

### 非标准参数 (-X)

```bash
# 可能随版本变化
java -Xms<size>          # 初始堆大小
java -Xmx<size>          # 最大堆大小
java -Xss<size>          # 线程栈大小
java -XshowSettings      # 显示设置
java -Xmixed             # 混合模式 (默认)
java -Xint               # 仅解释模式
java -Xnoclassgc         # 禁用类 GC
```

### 高级选项 (-XX)

```bash
# 不推荐生产使用，可能随时变化
java -XX:+PrintGCDetails
java -XX:+UseG1GC
java -XX:MaxHeapFreeRatio=75
```

---

## JDK 版本演进

### JDK 1.0-1.4 - 基础参数

```bash
# 基础内存参数
java -Xms128m -Xmx512m MyApp

# 垃圾回收 (串行 GC 是默认)
java -XX:+UseSerialGC MyApp

# 类路径
java -cp /lib/myapp.jar MyApp

# 系统属性
java -Duser.timezone=Asia/Shanghai MyApp

# 调试输出
-verbose:class           # 类加载
-verbose:gc              # GC
-verbose:jni             # JNI 调用
```

### JDK 5 (2004) - JMX 与监控

#### JMX (Java Management Extensions)

```java
// 启用 JMX
java -Dcom.sun.management.jmxremote \
     -Dcom.sun.management.jmxremote.port=9010 \
     -Dcom.sun.management.jmxremote.authenticate=false \
     -Dcom.sun.management.jmxremote.ssl=false \
     MyApp

// 代码中使用
MBeanServer mbs = ManagementFactory.getPlatformMBeanServer();
ObjectName name = new ObjectName("com.example:type=MyMBean");
mbs.registerMBean(myMBean, name);
```

#### jconsole (JDK 5+)

```bash
# 启动 JConsole
jconsole localhost:9010
jconsole <pid>

# 监控内容:
# - 内存使用
# - 线程状态
# - 类加载
# - CPU 使用
# - MBeans
```

#### JDK 5 新增参数

```bash
# GC 算法选择
-XX:+UseSerialGC         # 串行 GC (默认)
-XX:+UseParallelGC       # 并行 GC
-XX:+UseConcMarkSweepGC  # CMS GC

# 线程配置
-XX:ParallelGCThreads=n  # GC 线程数
-XX:SurvivorRatio=8      # Eden/Survivor 比例

# 堆配置
-XX:NewRatio=2           # 新生代/老年代比例
-XX:MaxPermSize=256m     # 永久代最大值
```

### JDK 6 (2006) - 监控工具集

#### jstat - JVM 统计

```bash
# 类加载统计
jstat -class <pid> 1000 10

# 编译统计
jstat -compiler <pid>

# GC 统计
jstat -gc <pid> 1000 10

# GC 容量统计
jstat -gccapacity <pid>

# GC 新生代统计
jstat -gcnew <pid> 1000 10

# 输出格式
#  S0C    S1C    S0U    S1U      EC       EU       OC         OU       MC     MU    CCSC   CCSU   YGC     YGCT    FGC    FGCT     GCT
#  512.0  512.0    0.0   496.0   5120.0   4096.0   10240.0     5120.0  20480.0 19456.0 2560.0 2400.0     4    0.123   0      0.000    0.123
```

#### jmap - 内存映射

```bash
# 堆转储
jmap -dump:live,format=b,file=heap.hprof <pid>

# 类直方图
jmap -histo:live <pid>

# 输出格式
#  num     #instances         #bytes  class name
#    1:          12345        9876543  [C
#    2:           6789        543210  [B
#    3:          34567        456789  java.lang.String
```

#### jinfo - 配置信息

```bash
# 查看 JVM 参数
jinfo -flags <pid>

# 查看系统属性
jinfo -sysprops <pid>

# 设置特定参数
jinfo -flag +PrintGCDetails <pid>
```

#### jstack - 线程堆栈

```bash
# 打印线程堆栈
jstack <pid>

# 打印锁信息
jstack -l <pid>

# 多次采样
jstack <pid> > thread_dump_1.txt
sleep 10
jstack <pid> > thread_dump_2.txt
diff thread_dump_1.txt thread_dump_2.txt
```

### JDK 7 (2011) - G1 GC

#### G1 参数

```bash
# 启用 G1 (JDK 7u4+)
-XX:+UseG1GC

# G1 特定参数
-XX:MaxGCPauseMillis=200        # 最大 GC 暂停时间
-XX:G1HeapRegionSize=16m        # Region 大小
-XX:G1ReservePercent=10         # 保留堆百分比
-XX:G1MixedGCCountTarget=8      # 混合 GC 目标次数
```

#### Compressed Oops

```bash
# 压缩普通对象指针 (默认启用 < 32GB)
-XX:+UseCompressedOops          # 启用
-XX:-UseCompressedOops          # 禁用

# 对象对齐
-XX:ObjectAlignmentInBytes=8    # 默认 8 字节
```

#### JDK 7 新增参数

```bash
# 字符串去重 (实验性)
-XX:+G1StringDeduplication

# 类卸载
-XX:+ClassUnloading
-XX:+ClassUnloadingWithConcurrentMark

# OOM 时自动转储
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/path/to/dump
```

### JDK 8 (2014) - Metaspace

#### Metaspace 替代永久代

```bash
# Metaspace 大小
-XX:MetaspaceSize=256m          # 初始 Metaspace 大小
-XX:MaxMetaspaceSize=512m       # 最大 Metaspace 大小

# 比较永久代
# JDK 7:
-XX:PermSize=256m
-XX:MaxPermSize=512m

# JDK 8+:
-XX:MetaspaceSize=256m
-XX:MaxMetaspaceSize=512m
```

#### Lambda 相关

```bash
# Lambda 序列化缓存
-XX:LambdaFormInlining

# invokedynamic
-XX:+UnlockDiagnosticVMOptions
-XX:+PrintLambdaForm
```

#### G1 改进

```bash
# G1 字符串去重 (JDK 8u20+)
-XX:+UseStringDeduplication
-XX:StringDeduplicationAgeThreshold=3

# G1 混合 GC
-XX:G1MixedGCCountTarget=8
-XX:G1OldCSetRegionThreshold=10
```

### JDK 9 (2017) - 模块化与 G1 默认

#### 模块相关

```bash
# 模块路径
--module-path <path>
--add-modules <module>(,<module>)*
--limit-modules <module>(,<module>)*

# 打印模块依赖
--print-module-deps

# 启动时验证
--validate-modules

# 冲突日志
--illegal-access=deny|permit|warn|debug
```

#### G1 成为默认 GC

```bash
# JDK 9+ G1 是默认
# 显式启用
-XX:+UseG1GC

# 切换其他 GC
-XX:+UseParallelGC
-XX:+UseSerialGC
-XX:+UseZGC              # JDK 11+ (实验)
```

#### CDS (Class Data Sharing)

```bash
# 类数据共享
java -Xshare:dump                     # 生成共享归档
java -Xshare:on -cp myapp.jar Main    # 使用共享
java -Xshare:off                      # 禁用共享

# AppCDS (应用类数据共享)
java -XX:DumpLoadedClassList=classes.lst -cp myapp.jar Main
java -Xshare:dump -XX:SharedClassListFile=classes.lst -XX:SharedArchiveFile=app.jsa
java -Xshare:on -XX:SharedArchiveFile=app.jsa -cp myapp.jar Main
```

### JDK 11 (2018) - ZGC 与 JFR

#### ZGC (实验性)

```bash
# 启用 ZGC (JDK 11+)
-XX:+UnlockExperimentalVMOptions -XX:+UseZGC

# ZGC 特定参数
-XX:ZCollectionInterval=5            # GC 间隔 (秒)
-XX:ZAllocationSpikeTolerance=5.0    # 分配峰值容忍度

# 线程数
-XX:ParallelGCThreads=12
-XX:ConcGCThreads=2
```

#### JFR (Java Flight Recorder)

```bash
# 启动 JFR
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr MyApp

# JFR 配置
java -XX:StartFlightRecording=filename=recording.jfr,dumponexit=true,settings=profile MyApp

# JFR 设置模板
# default.jfc    - 默认
# profile.jfc    - 性能分析
java -XX:StartFlightRecording=settings=profile ...

# 持续录制
java -XX:FlightRecorderOptions=disk=true,maxsize=1g,dumponexit=true ...
```

#### Epsilon GC

```bash
# 无操作 GC (JDK 11+)
-XX:+UseEpsilonGC

# 适用场景:
# - 短生命期应用
# - 性能测试
# - 超大堆 (>100GB)
```

### JDK 17 (2021) - ZGC 生产可用

#### ZGC (正式)

```bash
# JDK 15+ ZGC 不再是实验性
-XX:+UseZGC

# ZGC 线程配置
-XX:ParallelGCThreads=n
-XX:ConcGCThreads=n

# ZGC 内存配置
-XX:ZAllocationSpikeTolerance=2.0
```

#### Shenandoah GC

```bash
# 启用 Shenandoah (JDK 12+)
-XX:+UseShenandoahGC

# Shenandoah 模式
-XX:ShenandoahGCMode=normal         # 默认
-XX:ShenandoahGCMode=iuu            # Idle-Update-Updates
-XX:ShenandoahGCMode=passive        # 被动 GC
-XX:ShenandoahGCMode=aggressive     # 激进模式

# 并行线程
-XX:ParallelGCThreads=n
-XX:ConcGCThreads=n
```

### JDK 21 (2023) - 分代 ZGC

#### Generational ZGC

```bash
# 启用分代 ZGC (JDK 21+)
-XX:+UseZGC
-XX:+ZGenerational

# 性能提升
# - 降低 GC 频率 ~50%
# - 降低堆开销 ~30%
# - 保持低延迟 (<1ms)
```

#### JFR 增强

```bash
# JDK 21+ JFR 改进
-XX:StartFlightRecording=jdk.JVMInformation#jdk.GCHeapSummary

# 新事件
# - Virtual Thread 生命周期
# - Scoped Value 操作
# - Foreign Memory 访问
```

---

## 监控工具演进

### 命令行工具

| 工具 | 引入版本 | 功能 |
|------|----------|------|
| jps | JDK 1.2 | 列出 JVM 进程 |
| jstat | JDK 1.2 | JVM 统计 |
| jmap | JDK 1.2 | 内存映射 |
| jinfo | JDK 1.5 | 配置信息 |
| jstack | JDK 1.5 | 线程堆栈 |
| jcmd | JDK 7 | JVM 诊断命令 |

### GUI 工具

| 工具 | 引入版本 | 功能 |
|------|----------|------|
| jconsole | JDK 5 | JMX 控制台 |
| jvisualvm | JDK 6 | 综合监控 |
| JMC | JDK 7 | 任务控制 |
| Java Mission Control | JDK 11+ | JFR 分析 |

---

## 常用调优参数

### 堆内存配置

```bash
# 基础配置
-Xms2g                      # 初始堆 2GB
-Xmx4g                      # 最大堆 4GB

# 新生代配置
-Xmn1g                      # 新生代 1GB
-XX:NewRatio=2              # 新生代:老年代 = 1:2
-XX:SurvivorRatio=8         # Eden:Survivor = 8:1:1

# Metaspace 配置
-XX:MetaspaceSize=256m
-XX:MaxMetaspaceSize=512m

# 线程栈
-Xss1m                      # 每线程栈 1MB
```

### GC 选择

```bash
# 串行 GC (单核、小堆)
-XX:+UseSerialGC

# 并行 GC (多核、吞吐优先)
-XX:+UseParallelGC

# G1 GC (平衡吞吐和延迟，默认)
-XX:+UseG1GC

# ZGC (超低延迟，大堆)
-XX:+UseZGC

# Shenandoah GC (低延迟)
-XX:+UseShenandoahGC
```

### GC 调优

```bash
# G1 GC
-XX:MaxGCPauseMillis=200    # 目标暂停时间
-XX:G1HeapRegionSize=16m    # Region 大小
-XX:G1MixedGCCountTarget=8  # 混合 GC 次数

# Parallel GC
-XX:ParallelGCThreads=8     # GC 线程数
-XX:MaxGCPauseMillis=200

# ZGC
-XX:ZCollectionInterval=5   # GC 间隔
-XX:ZAllocationSpikeTolerance=5.0
```

---

## 性能分析

### JFR 录制

```bash
# 启动时录制
java -XX:StartFlightRecording=duration=60s,filename=app.jfr MyApp

# 动态录制
jcmd <pid> JFR.start
jcmd <pid> JFR.dumpname=recording.jfr
jcmd <pid> JFR.stop

# 分析 JFR
jfr print recording.jfr
jfr summary recording.jfr
jfr metadata recording.jfr
```

### jstack 分析

```bash
# 线程死锁检测
jstack -l <pid> | grep -A 10 "Found one Java-level deadlock"

# 线程状态统计
jstack <pid> | grep "java.lang.Thread.State" | sort | uniq -c
```

### jmap 分析

```bash
# 类直方图
jmap -histo:live <pid> | head -20

# 堆转储
jmap -dump:live,format=b,file=heap.hprof <pid>

# 分析堆转储
jhat -port 7000 heap.hprof
# 或使用 MAT/Eclipse Memory Analyzer
```

---

## OOM 诊断

### 常见 OOM 类型

```bash
# java.lang.OutOfMemoryError: Java heap space
# 原因: 堆内存不足
# 解决: 增加 -Xmx

# java.lang.OutOfMemoryError: Metaspace
# 原因: Metaspace 满了
# 解决: 增加 -XX:MaxMetaspaceSize

# java.lang.OutOfMemoryError: GC overhead limit exceeded
# 原因: GC 时间过长
# 解决: 优化代码或调整 GC

# java.lang.OutOfMemoryError: Direct buffer memory
# 原因: 堆外内存不足
# 解决: 增加 -XX:MaxDirectMemorySize

# java.lang.StackOverflowError
# 原因: 栈溢出（通常递归过深）
# 解决: 增加 -Xss 或检查递归代码
```

### OOM 自动转储

```bash
# OOM 时自动转储
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/path/to/dumps
-XX:ErrorFile=/path/to/hs_err_pid%p.log
```

---

## 最佳实践

### 生产环境参数

```bash
# G1 GC 推荐配置
java -Xms4g -Xmx4g \
     -XX:+UseG1GC \
     -XX:MaxGCPauseMillis=200 \
     -XX:MetaspaceSize=256m \
     -XX:MaxMetaspaceSize=512m \
     -XX:+HeapDumpOnOutOfMemoryError \
     -XX:HeapDumpPath=/logs/ \
     -XX:+PrintGCDetails \
     -XX:+PrintGCDateStamps \
     -Xloggc:/logs/gc.log \
     MyApp

# ZGC 推荐配置 (JDK 21+)
java -Xms8g -Xmx8g \
     -XX:+UseZGC \
     -XX:+ZGenerational \
     -XX:MetaspaceSize=256m \
     -XX:MaxMetaspaceSize=512m \
     -XX:+HeapDumpOnOutOfMemoryError \
     MyApp
```

### JVM 版本选择

| 场景 | 推荐版本 | GC |
|------|----------|-----|
| 传统应用 | JDK 11/17 | G1 |
| 高并发 I/O | JDK 21+ | ZGC |
| 低延迟 | JDK 21+ | 分代 ZGC |
| 大数据 | JDK 17+ | G1/Shenandoah |

---

## 相关链接

- [HotSpot VM Options](https://docs.oracle.com/en/java/javase/21/vm/options/)
- [Java Mission Control](https://docs.oracle.com/en/java/javase/21/docs/specs/man/jmc.html)
- [JFR Documentation](https://docs.oracle.com/en/java/javase/21/docs/specs/man/jfr.html)
