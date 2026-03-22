# JVM 调优与监控

> JVM 参数、调优工具和监控技术演进

[← 返回核心平台](../)

---
## 目录

1. [快速概览](#1-快速概览)
2. [核心贡献者](#2-核心贡献者)
3. [JVM 参数](#3-jvm-参数)
4. [诊断工具](#4-诊断工具)
5. [JFR (Java Flight Recorder)](#5-jfr-java-flight-recorder)
6. [JMX 监控](#6-jmx-监控)
7. [常见问题诊断](#7-常见问题诊断)
8. [性能调优](#8-性能调优)
9. [hsdb (HotSpot Debugger)](#9-hsdb-hotspot-debugger)
10. [相关链接](#10-相关链接)

---


## 1. 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 6 ── JDK 7 ── JDK 8 ── JDK 11 ── JDK 17 ── JDK 21 ── JDK 26
   │         │        │        │        │        │        │        │        │
基础参数   JMX    jstat   G1 GC  元空间   ZGC     外部    分代    CDS
-Xmx/-Xms  jconsole jmap   默认  Metaspace 低延迟   函数    ZGC     简化
          jstack  jinfo   JFR   字符串   生产就绪  (FFM)  生产     (JEP 467)
```

### 核心工具

| 工具 | 首发版本 | 用途 | 类型 |
|------|----------|------|------|
| **jstat** | JDK 6 | GC 统计 | 命令行 |
| **jmap** | JDK 6 | 堆转储 | 命令行 |
| **jstack** | JDK 5 | 线程转储 | 命令行 |
| **jinfo** | JDK 5 | JVM 配置 | 命令行 |
| **jcmd** | JDK 7 | 统一诊断 | 命令行 |
| **jconsole** | JDK 5 | JMX 监控 | GUI |
| **jvisualvm** | JDK 6 | 综合分析 | GUI |
| **JFR** | JDK 11 (商业), JDK 11 (开源, JEP 328) | 飞行记录 | 生产级 |
| **JMC** | JDK 7 | Mission Control | GUI |

---

## 2. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### JVM 运行时团队 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | 317 | Oracle | 类加载, 运行时核心 |
| 2 | [Ioi Lam](/by-contributor/profiles/ioi-lam.md) | 215 | Oracle | CDS, AOT, 运行时 |
| 3 | [David Holmes](/by-contributor/profiles/david-holmes.md) | 174 | Oracle | 并发, 线程, 规范 |
| 4 | Thomas Stuefe | 163 | Red Hat | 内存, 跨平台 |
| 5 | Stefan Karlsson | 149 | Oracle | 并发 GC |
| 6 | Kim Barrett | 113 | Oracle | C++ 现代化 |
| 7 | [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | 112 | Amazon | 性能基准 |
| 8 | Daniel D. Daugherty | 87 | Oracle | JVMTI, 调试 |
| 9 | Robbin Ehn | 77 | Oracle | 并发, 锁 |
| 10 | Calvin Cheung | 77 | Oracle | 类加载 |

---

## 3. JVM 参数

### 内存参数

```bash
# 堆内存
-Xms2g                    # 初始堆大小
-Xmx4g                    # 最大堆大小
-XX:NewSize=512m          # 新生代大小
-XX:MaxNewSize=1g         # 最大新生代
-XX:MetaspaceSize=256m    # 元空间初始大小
-XX:MaxMetaspaceSize=512m # 元空间最大大小

# 线程栈
-Xss1m                    # 线程栈大小

# 本地内存
-XX:MaxDirectMemorySize=1g # 直接内存最大值
```

### GC 参数

```bash
# GC 选择
-XX:+UseG1GC              # G1 GC (JDK 9+ 默认)
-XX:+UseZGC               # ZGC
-XX:+UseShenandoahGC      # Shenandoah GC
-XX:+UseSerialGC          # Serial GC
-XX:+UseParallelGC        # Parallel GC

# G1 调优
-XX:MaxGCPauseMillis=200  # 目标暂停时间
-XX:G1HeapRegionSize=16m  # Region 大小
-XX:G1ReservePercent=10   # 保留堆比例

# ZGC 调优
-XX:+ZGenerational        # 分代 ZGC (JDK 21+)
-XX:ZCollectionInterval=5 # GC 间隔
```

### JIT 参数

```bash
# 编译器
-XX:+UseTieredCompilation # 分层编译 (默认)
-XX:TieredStopAtLevel=4   # 最高编译级别

# 代码缓存
-XX:ReservedCodeCacheSize=256m # 代码缓存大小
-XX:InitialCodeCacheSize=32m   # 初始代码缓存

# 编译阈值
-XX:CompileThreshold=10000     # C2 编译阈值
-XX:OnStackReplacePercentage=140  # OSR 百分比
```

### 性能参数

```bash
# 字符串去重 (JDK 8u20+)
-XX:+UseStringDeduplication

# 压缩普通对象指针
-XX:+UseCompressedOops       # 自动启用 (<32GB)
-XX:+UseCompressedClassPointers  # 压缩类指针

# 紧凑对象头 (JDK 26)
-XX:+UseCompactObjectHeaders

# 偏向锁 (已废弃: JDK 15 废弃, JDK 18 移除)
# 注意: 以下参数在 JDK 18+ 中不再可用
# -XX:+UseBiasedLocking
# -XX:BiasedLockingStartupDelay=0
```

### 日志参数

```bash
# JDK 9+ 统一日志
-Xlog:gc                    # GC 日志
-Xlog:gc*:file=gc.log:time,level,tags  # 详细 GC 日志

# 类加载日志
-Xlog:class+load=info

# JIT 编译日志
-Xlog:compilation

# Safepoint 日志
-Xlog:safepoint

# 错误日志
-XX:ErrorFile=/var/log/java/hs_err_pid%p.log
```

---

## 4. 诊断工具

### jstat

```bash
# GC 统计 (每秒更新, 10 次)
jstat -gc <pid> 1000 10

# 类加载统计
jstat -class <pid> 1000

# 编译统计
jstat -compiler <pid>

# 容量统计
jstat -gccapacity <pid>

# 新生代统计
jstat -gcnew <pid>
```

### jmap

```bash
# 堆转储
jmap -dump:format=b,file=heap.hprof <pid>

# 查看堆配置
jmap -heap <pid>

# 查看类加载器统计
jmap -clstats <pid>

# 查看最终队列 (GC 回收队列)
jmap -finalizerinfo <pid>
```

### jstack

```bash
# 线程转储
jstack <pid>

# 死锁检测
jstack -l <pid>

# 输出到文件
jstack <pid> > thread_dump.txt
```

### jinfo

```bash
# 查看 JVM 参数
jinfo -flags <pid>

# 查看特定参数
jinfo -flag UseG1GC <pid>

# 动态修改可写参数
jinfo -flag +PrintGCDetails <pid>
```

### jcmd

```bash
# 查看所有可用命令
jcmd <pid> help

# GC 堆转储
jcmd <pid> GC.heap_dump /tmp/heap.hprof

# GC 概览
jcmd <pid> GC.heap_info

# GC 运行
jcmd <pid> GC.run

# 类加载统计
jcmd <pid> VM.classloader_stats

# 线程打印
jcmd <pid> Thread.print

# VM 信息
jcmd <pid> VM.info

# VM 版本
jcmd <pid> VM.version

# VM 命令行
jcmd <pid> VM.command_line

# VM 系统属性
jcmd <pid> VM.system_properties

# VM flags
jcmd <pid> VM.flags

# 设置标志
jcmd <pid> VM.set_flag PrintGCDetails true
```

---

## 5. JFR (Java Flight Recorder)

### 启用 JFR

```bash
# 启动时启用
java -XX:StartFlightRecording=filename=recording.jfr,duration=60s ...

# 运行时启用
jcmd <pid> JFR.start name=myrecording dumponexit=true

# 停止并导出
jcmd <pid> JFR.stop name=myrecording
jcmd <pid> JFR.dump name=myrecording filename=recording.jfr
```

### JFR 配置

```bash
# 低开销配置 (<1%)
java -XX:FlightRecorderOptions=samplethreads=true \
     -XX:StartFlightRecording=filename=recording.jfr \
     -XX:StartFlightRecording=settings=profile ...

# 自定义配置
java -XX:StartFlightRecording=filename=recording.jfr,\
    dumponexit=true,\
    settings=profile.jfc \
    ...
```

### JFR 分析

```bash
# 使用 JDK Mission Control
jmc

# 命令行打印
jfr print recording.jfr

# 打印特定事件
jfr print --events jdk.GarbageCollection recording.jfr

# 汇总
jfr summary recording.jfr
```

---

## 6. JMX 监控

### 启用 JMX

```bash
# 本地监控
java -Dcom.sun.management.jmxremote ...

# 远程监控 (不安全)
java -Dcom.sun.management.jmxremote.port=9010 \
     -Dcom.sun.management.jmxremote.authenticate=false \
     -Dcom.sun.management.jmxremote.ssl=false ...

# 远程监控 (安全)
java -Dcom.sun.management.jmxremote.port=9010 \
     -Dcom.sun.management.jmxremote.authenticate=true \
     -Dcom.sun.management.jmxremote.password.file=jmxremote.password \
     -Dcom.sun.management.jmxremote.access.file=jmxremote.access \
     -Dcom.sun.management.jmxremote.ssl=true \
     ...
```

### JConsole 连接

```bash
# 本地连接
jconsole

# 远程连接
jconsole <host>:9010

# 使用 JMX 服务 URL
jconsole service:jmx:rmi:///jndi/rmi://<host>:9010/jmxrmi
```

---

## 7. 常见问题诊断

### 内存泄漏

**症状**: OOM: Java heap space

**诊断**:
```bash
# 1. 堆转储
jmap -dump:format=b,file=heap.hprof <pid>

# 2. 使用 MAT/Eclipse 分析
# 3. 查找 Dominator Tree
# 4. 查找 Leak Suspects
```

### CPU 高

**症状**: CPU 使用率高

**诊断**:
```bash
# 1. 线程转储
jstack <pid> > thread_dump.txt

# 2. 多次采样 (间隔 5 秒)
for i in {1..5}; do
    jstack <pid> > thread_$i.txt
    sleep 5
done

# 3. 找到 RUNNABLE 状态线程
# 4. 分析热点方法
```

### 死锁

**症状**: 应用无响应

**诊断**:
```bash
# 1. 死锁检测
jstack -l <pid>

# 2. 查找 "Found one Java-level deadlock"
# 3. 分析锁持有关系
```

### GC 频繁

**症状**: GC 日志频繁

**诊断**:
```bash
# 1. GC 日志
-Xlog:gc*:file=gc.log:time,level,tags

# 2. 分析 GC 日志
# 3. 调整堆大小
-Xmx4g -Xms4g

# 4. 调整 GC 策略
-XX:MaxGCPauseMillis=200
```

---

## 8. 性能调优

### 启动优化

```bash
# AppCDS (应用类数据共享)
java -XX:DumpLoadedClassList=classes.lst -cp app.jar Main
java -Xshare:dump -XX:SharedClassListFile=classes.lst \
    -XX:SharedArchiveFile=app.jsa -cp app.jar
java -Xshare:on -XX:SharedArchiveFile=app.jsa -cp app.jar Main

# AOT 编译 (JDK 26+)
java -XX:AOTMode=create -jar app.jar
java -XX:AOTMode=use -jar app.jar
```

### 吞吐量优化

```bash
# 堆大小
-Xms4g -Xmx4g              # 避免动态调整

# GC
-XX:+UseParallelGC         # 吞吐优先
-XX:GCTimeRatio=99         # GC 时间 <1%

# JIT
-XX:CompileThreshold=8000  # 提前编译
```

### 延迟优化

```bash
# GC
-XX:+UseZGC                # 低延迟 GC
-XX:MaxGCPauseMillis=50    # 目标暂停

# JIT
-XX:CompileThreshold=10000 # 延迟编译
```

---

## 9. hsdb (HotSpot Debugger)

### 启动 hsdb

```bash
# JDK 9+
jhsdb clhsdb --pid <pid>

# 或使用 core 文件
jhsdb clhsdb --pid <pid> --exe <java> --core <core>
```

### hsdb 命令

```bash
# 代码缓存
> printcodecache

# 方法数据
> printmdo <MethodData address>

# 堆
> heapdump /tmp/heap.hprof

# 线程栈
> threads

# 帮助
> help

# 退出
> quit
```

---

## 10. 相关链接

### 本地文档

- [GC 演进](../gc/) - GC 调优
- [内存管理](../memory/) - 堆、Metaspace
- [性能优化](../performance/) - 性能分析

### 外部参考

**工具文档:**
- [JFR Documentation](https://docs.oracle.com/javacomponents/jmc-5-4/jfr-runtime-guide/about.htm)
- [Mission Control](https://docs.oracle.com/javacomponents/jmc-5-4/jmc-user-guide/about.htm)

**调优指南:**
- [Java Tuning Guide](https://docs.oracle.com/en/java/javase/21/gctuning/)
- [Tool Documentation](https://docs.oracle.com/en/java/javase/21/docs/specs/man/tools.html)
