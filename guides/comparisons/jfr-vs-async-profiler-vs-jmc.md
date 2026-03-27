---

# 性能分析工具对比: JFR vs async-profiler vs JMC

---

## 目录

1. [核心定位](#1-核心定位)
2. [多维度对比](#2-多维度对比)
3. [JFR (JDK Flight Recorder)](#3-jfr-jdk-flight-recorder)
4. [async-profiler](#4-async-profiler)
5. [JDK Mission Control (JMC)](#5-jdk-mission-control-jmc)
6. [协同使用](#6-协同使用)
7. [决策指南](#7-决策指南)

---

## 1. 核心定位

| 工具 | 一句话描述 |
|---|---|
| **JFR** | JDK 内置的事件记录框架，低开销持续监控 |
| **async-profiler** | 开源采样分析器，精确的 CPU/内存/Wall Clock 分析 |
| **JMC** | JFR 数据的可视化分析 IDE |

---

## 2. 多维度对比

| 维度 | JFR | async-profiler | JMC |
|------|-----|----------------|-----|
| **类型** | 事件记录 | 采样分析器 | 可视化分析工具 |
| **JDK 内置** | ✅ | ❌ (需下载) | ✅ (独立下载) |
| **CPU 开销** | <1% (default) | <5% | 0% (事后分析) |
| **CPU 分析** | ⚠️ 粗粒度 (ExecutionSample) | ✅ 精确 (perf_events) | N/A |
| **内存分析** | ✅ (HeapSummary, ObjectAllocation) | ✅ (Alloc 采样) | ✅ (可视化) |
| **Wall Clock** | ❌ | ✅ | N/A |
| **GC 事件** | ✅ 详细 | ❌ | ✅ 可视化 |
| **线程分析** | ✅ (锁等待/阻塞) | ✅ (Wall Clock) | ✅ 可视化 |
| **I/O 分析** | ✅ (File/Socket 事件) | ❌ | ✅ 可视化 |
| **自定义事件** | ✅ | ❌ | ✅ 显示 |
| **实时监控** | ✅ | ✅ | ✅ (JMX) |
| **火焰图** | ❌ (需转换) | ✅ 原生生成 | ✅ (内置) |
| **生产安全** | ✅ (<1% 开销) | ⚠️ (JNI agent) | ✅ (事后分析) |
| **需要的权限** | 无特殊 | 需加载 agent | 无 |

---

## 3. JFR (JDK Flight Recorder)

### 3.1 快速使用

```bash
# 启动时开启 JFR
java -XX:StartFlightRecording=duration=60s,filename=app.jfr,settings=profile -jar app.jar

# 动态开启
jcmd <pid> JFR.start name=profiling settings=profile duration=120s filename=recording.jfr

# 转储
jcmd <pid> JFR.dump name=profiling filename=dump.jfr
```

### 3.2 最佳实践

| 场景 | 配置 | 说明 |
|------|------|------|
| 生产持续监控 | `settings=default,disk=true,maxsize=100m` | <1% 开销 |
| 性能排查 | `settings=profile,duration=60s` | ~2% 开销 |
| GC 分析 | `+jdk.GCPhasePause#cutoff=0ms` | 捕获所有 GC 事件 |
| 内存泄漏 | `+OldObjectSample#cutoff=10m` | 捕获长寿命对象 |

### 3.3 优势

- 零依赖，JDK 内置
- 生产环境安全（<1% 开销）
- 丰富的事件类型（GC、JIT、线程、I/O、异常等）
- 自定义事件 API

---

## 4. async-profiler

### 4.1 安装与使用

```bash
# 下载
curl -L https://github.com/async-profiler/async-profiler/releases/download/v3.0/ap-3.0-linux-x64.tgz | tar xz

# CPU 分析
./asprof -d 30 -f cpu.html <pid>

# 内存分配分析
./asprof -d 30 -e alloc -f alloc.html <pid>

# Wall Clock 分析 (包含阻塞时间)
./asprof -d 30 -e wall -f wall.html <pid>

# 同时分析 CPU + 内存
./asprof -d 30 -e cpu,alloc -f combined.html <pid>
```

### 4.2 输出格式

| 格式 | 用途 |
|------|------|
| `.html` | 交互式火焰图 |
| `.jfr` | JFR 格式 (可在 JMC 中打开) |
| `.collapsed` | 折叠堆栈 (FlameGraph 工具) |
| `.tree` | 调用树文本视图 |

### 4.3 优势

- 精确的 CPU 分析（基于 perf_events，非 JFR 的 ExecutionSample）
- Wall Clock 分析（包含阻塞/等待时间）
- 原生火焰图生成
- 内存分配采样

---

## 5. JDK Mission Control (JMC)

### 5.1 核心功能

```
JMC 的分析能力:
┌──────────────────────────────────────────────────┐
│ 1. 概览仪表板                                    │
│    ├── CPU 使用率、内存使用、GC 暂停时间         │
│    └── 热点方法 Top N                            │
│                                                  │
│ 2. GC 分析                                       │
│    ├── GC 暂停时间分布图                         │
│    ├── 分代内存使用趋势                          │
│    └── GC 原因统计                               │
│                                                  │
│ 3. 线程分析                                      │
│    ├── 线程活动时间线                             │
│    ├── 锁等待/阻塞统计                           │
│    └── 线程分配排行                              │
│                                                  │
│ 4. 内存分析                                      │
│    ├── 堆使用趋势                                │
│    ├── 类实例数量/大小排行                        │
│    └── OldObjectSample 泄漏分析                  │
│                                                  │
│ 5. 代码分析                                      │
│    ├── JIT 编译统计                              │
│    ├── 方法热点排行                              │
│    └── 异常/错误统计                              │
│                                                  │
│ 6. I/O 分析                                      │
│    ├── 文件读写时间/大小                          │
│    └── Socket 读写时间/大小                      │
└──────────────────────────────────────────────────┘
```

### 5.2 使用方式

```bash
# 打开 JFR 文件
jmc recording.jfr

# 连接到运行中的 JVM (JMX)
jmc <pid>
```

---

## 6. 协同使用

### 6.1 推荐工作流

```
┌──────────────────────────────────────────────────┐
│                 性能分析工作流                    │
│                                                  │
│ Step 1: JFR (持续监控)                           │
│   └── 发现问题: GC 暂停过长 / CPU 飙升          │
│                                                  │
│ Step 2: JMC (可视化分析)                         │
│   └── 打开 JFR 录制 → 定位热点                  │
│                                                  │
│ Step 3: async-profiler (深入分析)                │
│   └── CPU/Wall/Alloc 火焰图 → 找到根因代码      │
│                                                  │
│ Step 4: JFR 自定义事件 (验证修复)                │
│   └── 添加业务指标 → 确认性能改善                │
└──────────────────────────────────────────────────┘
```

### 6.2 async-profiler 输出 JFR 格式

```bash
# 使用 async-profiler 生成 JFR 格式，然后在 JMC 中分析
./asprof -d 30 -e cpu,alloc -f profiling.jfr <pid>
jmc profiling.jfr
```

---

## 7. 决策指南

```
我想了解什么?
  │
  ├─ GC 性能 / 内存趋势?
  │    └── JFR + JMC (GC 事件最详细)
  │
  ├─ CPU 热点 / 哪个方法最慢?
  │    └── async-profiler (最精确的 CPU 分析)
  │
  ├─ 线程阻塞 / 锁竞争?
  │    └── async-profiler -e wall (Wall Clock 分析)
  │
  ├─ 内存分配热点?
  │    └── async-profiler -e alloc 或 JFR ObjectAllocation
  │
  ├─ 生产环境持续监控?
  │    └── JFR (最低开销, <1%)
  │
  ├─ 需要火焰图?
  │    └── async-profiler (原生火焰图)
  │
  └─ 综合 JFR 录制分析?
       └── JMC (最佳可视化工具)
```

---

## 相关链接

- [JFR 指南](/guides/jfr.md)
- [GC 调优案例](/cases/gc-tuning-case.md)
- [内存泄漏诊断](/cases/memory-leak-diagnosis.md)
- [JIT 编译回退排查](/cases/jit-compilation-fallback.md)
- [jdk.jfr 模块分析](/modules/jdk.jfr.md)
