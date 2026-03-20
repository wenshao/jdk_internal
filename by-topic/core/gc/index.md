# GC 垃圾收集器

> 从 Serial 到分代 ZGC 的完整演进历程

[← 返回核心平台](../)

---

## TL;DR 快速概览

> 💡 **30 秒选择合适的 GC**

### 快速选择决策树

```
开始
  │
  ├─ 内存 < 100MB ───────────────────→ Serial GC
  │
  ├─ 单核 CPU ──────────────────────→ Serial GC
  │
  ├─ 停顿时间 < 10ms (低延迟)
  │    ├─ 内存 < 4GB ──────────────→ ZGC
  │    └─ 内存 ≥ 4GB ──────────────→ ZGC / Shenandoah
  │
  ├─ 吞吐量优先 (后台任务)
  │    └──────────────────────────→ Parallel GC
  │
  └─ 通用服务器 (默认)
       └──────────────────────────→ G1 GC
```

### GC 选择速查表

| 场景 | 推荐 GC | JVM 参数 |
|------|---------|----------|
| **桌面应用** | G1 | `-XX:+UseG1GC` |
| **微服务/容器** | G1 | `-XX:+UseG1GC -XX:MaxGCPauseMillis=200` |
| **大数据批处理** | Parallel | `-XX:+UseParallelGC` |
| **低延迟交易** | ZGC | `-XX:+UseZGC` |
| **大内存 (8GB+)** | ZGC | `-XX:+UseZGC` |
| **内存受限 (<256MB)** | Serial | `-XX:+UseSerialGC` |

### 性能特征对比

| GC | 停顿时间 | 吞吐量 | 内存开销 | 适用堆大小 |
|----|----------|--------|----------|------------|
| Serial | 长 | 低 | 最小 | < 100MB |
| Parallel | 中 | 高 | 小 | 任意 |
| G1 | 可预测 | 中高 | 中 | 任意 |
| ZGC | < 10ms | 中高 | 中 | 8MB - 16TB |
| Shenandoah | < 10ms | 中 | 中 | 任意 |

### 版本建议

| JDK 版本 | 推荐 GC | 备注 |
|----------|---------|------|
| **JDK 8** | G1 / Parallel | G1 需显式指定 |
| **JDK 11+** | G1 (默认) / ZGC | ZGC 生产就绪 |
| **JDK 21+** | G1 / 分代 ZGC | ZGC 分代提升吞吐量 |

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

### JDK 默认 GC 变化

| 版本 | 默认 GC | 说明 |
|------|---------|------|
| JDK 1.0-1.3 | Serial GC | 单核时代 |
| JDK 6-14 | Parallel GC | 多核时代，吞吐优先 |
| JDK 9-20 | G1 GC | 停顿时间可控 |
| JDK 21+ | G1 GC | 继续作为默认 |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### GC 团队 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Albert Mingkun Yang | 681 | Oracle | G1 GC, 内存管理 |
| 2 | Thomas Schatzl | 674 | Oracle | G1 GC 维护者 |
| 3 | Aleksey Shipilev | 324 | Oracle | Shenandoah GC |
| 4 | Zhengyu Gu | 252 | Oracle | Shenandoah 核心开发者 |
| 5 | Kim Barrett | 235 | Oracle | C++ 现代化 |
| 6 | Stefan Karlsson | 229 | Oracle | 分代 ZGC (JEP 439) |
| 7 | Per Lidén | 198 | Oracle | ZGC 创始人 |
| 8 | Roman Kennke | 163 | Red Hat | Shenandoah 架构 |
| 9 | William Kemper | 112 | Red Hat | 分代 Shenandoah (JEP 429) |
| 10 | Erik Österlund | 96 | Oracle | ZGC 核心开发者 |

### G1 GC 专项

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Thomas Schatzl | 600 | Oracle | G1 GC 维护者 |
| 2 | Albert Mingkun Yang | 202 | Oracle | G1 GC, 内存管理 |
| 3 | Kim Barrett | 129 | Oracle | C++ 现代化 |
| 4 | Ivan Walulya | 83 | Oracle | G1 GC |
| 5 | Stefan Karlsson | 75 | Oracle | 并发 GC |
| 6 | Stefan Johansson | 56 | Oracle | G1 GC |

### ZGC 专项

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Per Lidén | 157 | Oracle | ZGC 创始人 |
| 2 | Stefan Karlsson | 116 | Oracle | 分代 ZGC (JEP 439) |
| 3 | Erik Österlund | 56 | Oracle | ZGC 核心开发者 |
| 4 | Per Liden | 45 | Oracle | ZGC (别名) |
| 5 | Axel Boldt-Christmas | 44 | Oracle | ZGC |
| 6 | Joel Sikström | 31 | Oracle | ZGC |

### Shenandoah GC 专项

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Aleksey Shipilev | 272 | Oracle | Shenandoah 维护者 |
| 2 | Zhengyu Gu | 217 | Oracle | Shenandoah 核心开发者 |
| 3 | William Kemper | 109 | Red Hat | 分代 Shenandoah (JEP 429) |
| 4 | Roman Kennke | 107 | Red Hat | Shenandoah 架构 |
| 5 | Stefan Karlsson | 44 | Oracle | 并发支持 |

---

## 重要 PR 分析

### 内存优化

#### JDK-8349400: 消除匿名内部类减少元空间

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ 元空间占用减少 82%

将 `KnownOIDs` 枚举中的匿名内部类转换为构造函数参数：

**核心改进**:
- 消除 10 个匿名内部类
- 减少类加载开销
- 元空间占用减少 82%

```java
// 优化前：10 个匿名内部类
enum KnownOIDs {
    KP_TimeStamping("...") {
        @Override boolean registerNames() { return false; }
    },
    // ... 9 more anonymous classes
}

// 优化后：无匿名类
enum KnownOIDs {
    KP_TimeStamping("...", "...", false),
    // ...
}
```

**GC 影响**:
- 减少元空间压力
- 更快的类加载
- 降低 GC 频率

→ [详细分析](/by-pr/8349/8349400.md)

### GC 性能优化

#### 对象头压缩 (JEP 519: JDK 26)

**紧凑对象头特性**:
- 每个对象节省 8-16 字节
- GC 压力降低
- 缓存效率提升

```bash
# 启用紧凑对象头 (默认)
-XX:+UseCompactObjectHeaders

# 内存节省示例:
# 100 万个对象 × 12 字节 = 12 MB 节省
```

**GC 优化效果**:
- 堆内存占用减少 5-10%
- GC 停顿时间减少 5-15%
- 吞吐量提升 3-8%

---

## GC 性能最佳实践

### 选择合适的 GC

```java
// ✅ 小内存应用 (<100MB)
// Serial GC
java -XX:+UseSerialGC -jar app.jar

// ✅ 通用服务器 (默认)
// G1 GC
java -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -jar app.jar

// ✅ 低延迟要求
// ZGC
java -XX:+UseZGC -jar app.jar

// ✅ 大内存 + 低延迟
// 分代 ZGC (JDK 21+)
java -XX:+UseZGC -XX:ZCollectionInterval=5 -jar app.jar
```

### GC 调优参数

```bash
# G1 GC 调优
-XX:+UseG1GC                    # 使用 G1
-XX:MaxGCPauseMillis=200         # 目标停顿时间
-XX:G1HeapRegionSize=16m         # Region 大小
-XX:G1ReservePercent=10          # 保留空间比例

# ZGC 调优
-XX:+UseZGC                      # 使用 ZGC
-XX:ZCollectionInterval=5        # GC 间隔 (秒)
-XX:ZAllocationSpikeTolerance=2.0  # 分配峰值容忍度

# 通用调优
-Xlog:gc*:file=gc.log:time,uptime,level,tags  # GC 日志
-XX:+PrintGCDetails              # 详细 GC 信息
-XX:+PrintGCDateStamps           # 时间戳
```

### 避免常见的 GC 问题

```java
// ❌ 避免：创建大量临时对象
for (int i = 0; i < 1000000; i++) {
    String s = new String("temp");  // 每次创建新对象
}

// ✅ 推荐：使用字面量或常量
String TEMP = "temp";
for (int i = 0; i < 1000000; i++) {
    process(TEMP);  // 复用常量
}

// ❌ 避免：大对象频繁分配
byte[] buffer = new byte[10 * 1024 * 1024];  // 10 MB
for (int i = 0; i < 1000; i++) {
    buffer = new byte[10 * 1024 * 1024];  // 频繁分配大对象
}

// ✅ 推荐：重用缓冲区
byte[] buffer = new byte[10 * 1024 * 1024];
for (int i = 0; i < 1000; i++) {
    process(buffer);  // 重用
    Arrays.fill(buffer, (byte) 0);  // 清空
}
```

### 监控 GC

```bash
# GC 日志
-Xlog:gc*:file=gc.log:time,uptime,level,tags

# JFR 监控
-XX:StartFlightRecording=filename=gc.jfr,duration=60s

# jstat 监控
jstat -gc <pid> 1000 10  # 每秒输出，共 10 次

# jcmd 诊断
jcmd <pid> GC.heap_info
jcmd <pid> GC.run
jcmd <pid> GC.run_finalization
```

---

## 文档导航

### GC 算法详解

- [G1 GC](g1-gc.md) - G1 架构、Region、Mixed GC
- [ZGC](zgc.md) - 读屏障、染色指针、NUMA
- [Shenandoah](shenandoah.md) - Brooks Pointer、 Brooks Forwarding

### 配置调优

- [VM 参数](vm-parameters.md) - GC 参数完整参考
- [调优指南](tuning.md) - GC 选择与调优策略

### 演进历史

- [版本时间线](timeline.md) - JDK 1.0 到 JDK 26
- [近期改进](recent-changes.md) - 2024-2025 更新

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

## 快速参考

### 选择 GC

```bash
# 查看当前 GC
java -XX:+PrintCommandLineFlags -version | grep GC

# 指定 GC
-XX:+UseSerialGC              # Serial GC
-XX:+UseParallelGC            # Parallel GC
-XX:+UseG1GC                  # G1 GC (默认)
-XX:+UseZGC                   # ZGC
-XX:+UseShenandoahGC          # Shenandoah GC
```

### 常用参数

```bash
# G1 GC
-XX:MaxGCPauseMillis=200       # 目标暂停时间
-XX:G1HeapRegionSize=16m       # Region 大小
-XX:G1ReservePercent=10        # 保留堆比例

# ZGC
-XX:ZCollectionInterval       # GC 间隔
-XX:ZFragmentationLimit       # 碎片率阈值

# 通用
-XX:+PrintGC                  # 打印 GC 日志
-XX:+PrintGCDetails            # 详细 GC 信息
-XX:+PrintGCTimeStamps        # GC 时间戳
```

### GC 日志

```bash
# JDK 9+ 统一日志
-Xlog:gc*:file=gc.log:level,tags

# 包含详情
-Xlog:gc*:file=gc.log:level,tags,uptime,time,level,tags

# 包含 GC 堆转储
-Xlog:gc+heap=info:file=gc.log:level,tags
```

---

## 内部结构

### HotSpot GC 源码

```
src/hotspot/share/gc/
├── serial/                       # Serial GC
│   └── serialMemoryManager.cpp
├── parallel/                    # Parallel GC
│   ├── parallelScavenge.cpp
│   └── psMarkSweep.cpp
├── g1/                          # G1 GC
│   ├── g1CollectedHeap.cpp      # G1 堆管理
│   ├── g1Allocator.cpp          # Region 分配器
│   ├── g1AllocRegion.cpp        # Region 分配
│   ├── g1Analytics.cpp          # 分析统计
│   ├── g1RemSet.cpp             # Remembered Set
│   ├── g1BarrierSet.cpp         # 屏障集
│   └── g1SATBBufferQueue.cpp    # SATB 队列
├── z/                           # ZGC
│   ├── zAddress.cpp             # 地址管理
│   ├── zArray.cpp                # 数组支持
│   ├── zCollectedHeap.cpp        # 堆管理
│   ├── zGeneration.cpp           # 分代支持
│   ├── zPage.cpp                 # 页管理
│   ├── zRemembered.cpp           # Remembered Set
│   └── zThread.cpp               # 线程管理
├── shenandoah/                   # Shenandoah GC
│   ├── shenandoahHeap.cpp        # 堆管理
│   ├── shenandoahMark.cpp        # 标记
│   ├── shenandoahEvacuation.cpp  # 转发
│   ├── shenandoahAgeCensus.cpp   # 年龄普查
│   ├── shenandoahBarrierSet.cpp  # 屏障集
│   ├── shenandoahUtils.cpp       # 工具类
│   └── mode/                     # 并发模式
└── shared/                       # 共享代码
    ├── barrierSet.cpp            # 屏障集抽象
    ├── collector.cpp             # 收集器抽象
    ├── workerThreads.cpp         # 工作线程
    └── workerDataArray.cpp       # 线程数据
```

---

## 相关链接

### 内部文档

- [GC 时间线](timeline.md) - 详细的历史演进
- [G1 GC 详解](g1-gc.md) - G1 架构与配置
- [ZGC 详解](zgc.md) - ZGC 原理与调优
- [Shenandoah 详解](shenandoah.md) - Shenandoah GC 实现细节
- [VM 参数](vm-parameters.md) - GC 参数参考
- [调优指南](tuning.md) - GC 选择策略
- [近期改进](recent-changes.md) - JDK 21-26 改进

### 相关主题

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
