# GC 垃圾收集器

> 从 Serial 到分代 ZGC 的完整演进历程

[← 返回核心平台](../)

---

## 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 6 ── JDK 7 ── JDK 9 ── JDK 11 ── JDK 15 ── JDK 21 ── JDK 25 ── JDK 26
   │         │        │        │        │        │         │         │         │         │
Serial    Parallel CMS    G1    G1默认   ZGC      ZGC     分代ZGC  分代    G1优化   紧凑
GC        GC      (废弃)  (默认)  (实验)  (生产)  (生产)  Shenandoah 吞吐量   对象头
                                                        (生产)
```

### GC 算法对比

| GC 算法 | 首发版本 | 设计目标 | 适用场景 | 停顿时间 | 吞吐量 |
|---------|----------|----------|----------|----------|--------|
| **Serial** | JDK 1.0 | 单线程，内存占用小 | 单核、小内存 (<100MB) | 长 | 低 |
| **Parallel** | JDK 6 | 多线程，吞吐量优先 | 多核、后台批处理 | 中 | 高 |
| **CMS** | JDK 6 | 低延迟 | 交互式应用 (已废弃) | 短 | 中 |
| **G1** | JDK 6 | 可预测停顿 | 通用服务器应用 (默认) | 可预测 | 中高 |
| **ZGC** | JDK 11 | 低延迟 (<10ms) | 大内存、低延迟 | <10ms | 中高 |
| **Shenandoah** | JDK 12 | 低延迟 (<10ms) | 大内存、低延迟 | <10ms | 中高 |

---

## 目录

- [GC 基础](#gc-基础)
- [GC 算法详解](#gc-算法详解)
- [最新增强](#最新增强)
- [GC 选择指南](#gc-选择指南)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## GC 基础

### GC 算法分类

```
┌─────────────────────────────────────────────────────────┐
│                    GC 算法分类                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  按线程数分类:                                          │
│  ├── Serial GC      (单线程)                           │
│  └── Parallel GC    (多线程)                           │
│                                                         │
│  按工作方式分类:                                        │
│  ├── 串行 GC        (Stop-the-world)                   │
│  ├── 并发 GC        (部分并发)                         │
│  └── 增量 GC        (分片执行)                         │
│                                                         │
│  按内存布局分类:                                        │
│  ├── 分代 GC        (年轻代/老年代)                    │
│  └── 区域 GC        (G1, ZGC, Shenandoah)              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 分代假说

```
┌─────────────────────────────────────────────────────────┐
│                    分代假说                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 弱分代假说:                                         │
│     大多数对象都是朝生夕灭的                             │
│                                                         │
│  2. 强分代假说:                                         │
│     越老的对象越难消亡                                   │
│                                                         │
│  3. 跨代引用假说:                                       │
│     跨代引用相对较少                                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 堆内存结构

```
┌─────────────────────────────────────────────────────────┐
│                      Java 堆                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────┐       │
│  │            年轻代 (Young Gen)               │       │
│  │  ├── Eden 区                                 │       │
│  │  └── Survivor 区 (S0, S1)                   │       │
│  └─────────────────────────────────────────────┘       │
│                                                         │
│  ┌─────────────────────────────────────────────┐       │
│  │            老年代 (Old Gen)                 │       │
│  │  ├── 存活期长的对象                          │       │
│  │  └── 大对象直接分配                          │       │
│  └─────────────────────────────────────────────┘       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## GC 算法详解

### Serial GC

**特点**: 单线程，Stop-the-world

```bash
# 启用 Serial GC
-XX:+UseSerialGC

# 适用场景
# - 单核 CPU
# - 小内存 (< 100MB)
# - 客户端应用
```

**工作原理**:
1. 新对象分配在 Eden 区
2. Eden 满后，触发 Minor GC
3. 存活对象复制到 Survivor 区
4. 多次 GC 后存活对象晋升老年代
5. 老年代满后，触发 Full GC

### Parallel GC

**特点**: 多线程，吞吐量优先

```bash
# 启用 Parallel GC (JDK 8 默认)
-XX:+UseParallelGC

# 配置参数
-XX:ParallelGCThreads=8            # GC 线程数
-XX:MaxGCPauseMillis=200           # 最大停顿时间
-XX:GCTimeRatio=99                 # GC 时间比例 (1/(1+n))
```

**工作原理**:
- 与 Serial GC 类似，但使用多线程
- 适合多核 CPU 和后台批处理

### G1 GC

**特点**: 区域化、可预测停顿

```bash
# 启用 G1 GC (JDK 9+ 默认)
-XX:+UseG1GC

# 配置参数
-XX:MaxGCPauseMillis=200           # 目标最大停顿时间
-XX:G1HeapRegionSize=16m           # Region 大小
-XX:G1ReservePercent=10            # 保留堆空间百分比
-XX:G1MixedGCCountTarget=8         # 混合 GC 目标次数
```

**工作原理**:

```
┌─────────────────────────────────────────────────────────┐
│                    G1 GC 架构                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  堆被划分为多个大小相等的 Region:                       │
│                                                         │
│  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐           │
│  │ E │ E │ S │ O │ H │ E │ S │ O │ H │...│           │
│  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘           │
│                                                         │
│  E = Eden    S = Survivor                              │
│  O = Old     H = Humongous (大对象)                    │
│                                                         │
│  GC 过程:                                               │
│  1. Young GC: 回收 Eden + Survivor Region              │
│  2. Mixed GC: 回收 Young + 部分 Old Region             │
│  3. Full GC: 整个堆回收 (尽量避免)                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**G1 的优势**:
- 可预测停顿时间
- 无内存碎片
- 大堆性能好

### ZGC

**特点**: 低延迟、区域化、并发

```bash
# 启用 ZGC (JDK 15+)
-XX:+UseZGC

# 配置参数
-XX:ZCollectionInterval=5             # GC 间隔 (秒)
-XX:ZAllocationSpikeTolerance=2.0     # 分配峰值容忍度
```

**ZGC 演进**:

| 版本 | 特性 | 状态 |
|------|------|------|
| JDK 11 | ZGC 引入 | 实验性 |
| JDK 15 | ZGC 生产就绪 | 正式版 |
| JDK 21 | 分代 ZGC | 预览版 |
| JDK 23 | 分代 ZGC 改进 | 正式版 |

**分代 ZGC (JDK 21+)**:

```
┌─────────────────────────────────────────────────────────┐
│                 分代 ZGC 架构                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  年轻代 ZGC (Young Gen ZGC):                           │
│  ├── 频繁的小型 GC                                      │
│  ├── 大部分对象快速回收                                 │
│  └── 降低老年代压力                                     │
│                                                         │
│  老年代 ZGC (Old Gen ZGC):                             │
│  ├── 低频的大型 GC                                      │
│  ├── 并发标记重定位                                     │
│  └── 保持低延迟                                         │
│                                                         │
│  性能优势:                                             │
│  - GC 停顿时间减少 50%                                  │
│  - 吞吐量提升 20%                                       │
│  - 更低的对分配压力                                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Shenandoah GC

**特点**: 低延迟、区域化、并发

```bash
# 启用 Shenandoah GC
-XX:+UseShenandoahGC

# 配置参数
-XX:ShenandoahGCHeuristics=compact      # 启发式算法
-XX:ShenandoahGCCyclePause=200          # 目标停顿时间
```

**Shenandoah 演进**:

| 版本 | 特性 | 状态 |
|------|------|------|
| JDK 12 | Shenandoah 引入 | 实验性 |
| JDK 15 | 生产就绪 | 正式版 |
| JDK 21 | 分代 Shenandoah | 预览版 |
| JDK 25 | 分代 Shenandoah 改进 | 正式版 |

---

## 最新增强

### JDK 21: 分代 ZGC

**JEP 439: Generational ZGC**

分代 ZGC 将堆分为年轻代和老年代：

```java
// 性能改进
- GC 停顿时间减少 50%
- 吞吐量提升 20%
- 对分配压力更低
```

**技术细节**:
- 年轻代对象独立回收
- 老年代并发标记
- 跨代引用特殊处理

### JDK 25: 分代 Shenandoah

**JEP 429: Generational Shenandoah**

分代 Shenandoah 类似分代 ZGC：

```bash
# 启用分代模式
-XX:+UseShenandoahGC
-XX:ShenandoahGCMode=generational
```

**性能改进**:
- GC 停顿时间减少 40%
- 吞吐量提升 15%
- 更好的内存利用率

### JDK 26: G1 GC 吞吐量改进

**JEP 522: G1 GC: Improve Throughput by Reducing Synchronization**

```bash
# 自动启用，无需配置
# 写屏障从 50 条指令减少到 12 条指令 (x86-64)
```

**性能改进**:
- 应用吞吐量提升 10-15%
- 写屏障大幅减少
- 无需配置更改

### JDK 26: 紧凑对象头

**JEP 519: Compact Object Headers**

```bash
# 启用紧凑对象头 (默认)
-XX:+UseCompactObjectHeaders
```

**内存节省**:
- 每个对象节省 8-16 字节
- GC 压力降低
- 缓存效率提升

---

## GC 选择指南

### 按场景选择

| 场景 | 推荐 GC | 理由 |
|------|---------|------|
| 小内存应用 (<100MB) | Serial GC | 内存占用小 |
| 单核 CPU | Serial GC | 避免线程切换开销 |
| 多核批处理 | Parallel GC | 吞吐量优先 |
| 通用服务器 | G1 GC | 平衡停顿和吞吐量 |
| 低延迟要求 | ZGC/Shenandoah | 停顿 <10ms |
| 大内存 (>16GB) | ZGC/Shenandoah | 扩展性好 |
| 云原生/容器 | G1/ZGC | 内存限制友好 |

### GC 切换

```bash
# 切换到 G1 GC
java -XX:+UseG1GC -jar app.jar

# 切换到 ZGC (JDK 15+)
java -XX:+UseZGC -jar app.jar

# 切换到 Shenandoah GC
java -XX:+UseShenandoahGC -jar app.jar
```

### GC 监控

```bash
# GC 日志
-Xlog:gc*:file=gc.log:time,uptime,level,tags

# GC 详情
-XX:+PrintGCDetails -XX:+PrintGCTimeStamps

# JFR 监控
-XX:StartFlightRecording=filename=gc.jfr
```

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### G1 GC (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Thomas Schatzl | 600 | Oracle | G1 GC 维护者 |
| 2 | Albert Mingkun Yang | 202 | Oracle | G1 GC, 内存管理 |
| 3 | Kim Barrett | 129 | Oracle | C++ 现代化 |
| 4 | Ivan Walulya | 83 | Oracle | G1 GC |
| 5 | Stefan Karlsson | 75 | Oracle | 并发 GC |
| 6 | Stefan Johansson | 56 | Oracle | G1 GC |

### ZGC (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Per Lidén | 157 | Oracle | ZGC 创始人 |
| 2 | Stefan Karlsson | 116 | Oracle | 分代 ZGC (JEP 439) |
| 3 | Erik Österlund | 56 | Oracle | ZGC 核心开发者 |
| 4 | Per Liden | 45 | Oracle | ZGC (别名) |
| 5 | Axel Boldt-Christmas | 44 | Oracle | ZGC |
| 6 | Joel Sikström | 31 | Oracle | ZGC |

### Shenandoah GC (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Aleksey Shipilev | 272 | Oracle | Shenandoah 维护者 |
| 2 | Zhengyu Gu | 217 | Oracle | Shenandoah 核心开发者 |
| 3 | William Kemper | 109 | Red Hat | 分代 Shenandoah (JEP 429) |
| 4 | Roman Kennke | 107 | Red Hat | Shenandoah 架构 |
| 5 | Stefan Karlsson | 44 | Oracle | 并发支持 |

---

## Git 提交历史

> 基于 OpenJDK master 分支分析

### G1 GC 改进 (2024-2026)

```bash
# 最近的重要提交
a0c8fce 8379511: G1: G1CollectorState should derive concurrent cycle state
6e94119 8378176: Concurrent GC worker threads may suffer from priority inversion
1ea8ef92 8379781: G1: Full GC does not print partial array task stats
38e8a46 8378331: G1: WeakProcessor IsAlive and KeepAlive closures
272ca08 8378336: G1: j.l.ref.Reference processor always keeps alive humongous
```

### Shenandoah GC 改进 (2024-2026)

```bash
# 最近的重要提交
27a4ed5 8375568: Shenandoah: Abbreviate thread names in display
bcadf46 8377658: Fix bug in calculations of old-generation balance
c904a0e 8378338: Shenandoah: Heap-used generic verification error
3e06094 Merge simplify-aged-region-selection into promotions
dd2387f Skip regions scheduled for in place promotions
5bfa78c Proactively steal region from mutator view
```

### ZGC 改进 (2024-2026)

```bash
# 查看 ZGC 相关提交
cd /path/to/jdk
git log --oneline -- src/hotspot/share/gc/z/
```

---

## 相关链接

### 内部文档

- [GC 时间线](timeline.md) - 详细的历史演进
- [内存管理](../memory/) - 堆、栈、Metaspace
- [性能优化](../performance/) - JVM 调优

### 外部资源

- [Getting Started with G1 GC](https://openjdk.org/projects/jdk/features/g1)
- [The ZGC Garbage Collector](https://openjdk.org/projects/jdk/features/zgc)
- [Shenandoah GC](https://wiki.openjdk.org/display/shenandoah/Main)
- [JEP 439: Generational ZGC](https://openjdk.org/jeps/439)
- [JEP 429: Generational Shenandoah](https://openjdk.org/jeps/429)
- [JEP 522: G1 GC Throughput Improvement](https://openjdk.org/jeps/522)
- [JEP 519: Compact Object Headers](https://openjdk.org/jeps/519)

### Git 仓库

```bash
# 查看 G1 GC 相关提交
git log --oneline -- src/hotspot/share/gc/g1/

# 查看 ZGC 相关提交
git log --oneline -- src/hotspot/share/gc/z/

# 查看 Shenandoah GC 相关提交
git log --oneline -- src/hotspot/share/gc/shenandoah/
```

---

**最后更新**: 2026-03-20

**Sources**:
- [JEP 439: Generational ZGC](https://openjdk.org/jeps/439)
- [JEP 429: Generational Shenandoah](https://openjdk.org/jeps/429)
- [JEP 522: G1 GC Throughput Improvement](https://openjdk.org/jeps/522)
- [JEP 519: Compact Object Headers](https://openjdk.org/jeps/519)
- [ZGC Main - OpenJDK Wiki](https://wiki.openjdk.org/spaces/zgc/pages/34668579/Main)
