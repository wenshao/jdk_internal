---

# ZGC 调优实战：从 G1 迁移到 Generational ZGC

> ⚠️ **Template / Example Document**: This is an illustrative example document with synthetic data for reference purposes. The scenarios, performance figures, and diagnostic data shown are **not from real production environments**. Use this as a template for documenting real cases.
>
> ⚠️ **模板/示例文档**: 本文为示意性模板文档，包含合成的示意数据。所描述的场景、性能指标和诊断数据**并非来自真实生产环境**。请将其作为记录真实案例的模板使用。

---

## 目录

1. [背景与问题描述](#1-背景与问题描述)
2. [环境信息](#2-环境信息)
3. [第一阶段：G1 基线测量](#3-第一阶段g1-基线测量)
4. [第二阶段：迁移到 ZGC](#4-第二阶段迁移到-zgc)
5. [第三阶段：Non-Generational ZGC 调优](#5-第三阶段non-generational-zgc-调优)
6. [第四阶段：迁移到 Generational ZGC](#6-第四阶段迁移到-generational-zgc)
7. [第五阶段：最终精调](#7-第五阶段最终精调)
8. [最终效果对比](#8-最终效果对比)
9. [经验总结与 Checklist](#9-经验总结与-checklist)

---

## 1. 背景与问题描述

### 1.1 业务场景

**实时风控引擎**，需要对每笔交易在 50ms 内完成风险评估：

| 指标 | SLA 要求 |
|------|----------|
| 单笔评估延迟 | < 50ms |
| P99 延迟 | < 100ms |
| 吞吐量 | 5,000 TPS |
| 机器学习模型 | 多个 ONNX 模型，内存占用约 2GB |

### 1.2 问题现象

- G1 GC 的 Mixed GC 暂停时间在 50-150ms 范围，已逼近 SLA 上限
- 模型推理产生的短期大对象导致 G1 humongous 分配
- 大促流量下 GC 暂停导致交易超时

---

## 2. 环境信息

```
硬件:        8C16G (Kubernetes Pod)
JDK 版本:    JDK 21.0.2 (升级路径: 17 → 21 → 25)
框架:        Spring Boot 3.2
堆大小:      10GB
ML 模型:     ONNX Runtime (Java)
```

---

## 3. 第一阶段：G1 基线测量

### 3.1 G1 GC 指标（示意）

```
GC 类型             平均暂停    最大暂停    频率
Young GC            22ms        48ms        每 3-5s
Mixed GC            65ms        180ms       每小时 20-30 次
Concurrent Mark     0ms (并发)  -           每小时 6 次
Full GC             -           -           未发生

问题: Mixed GC 最大暂停 180ms 已超过 SLA (100ms)
```

### 3.2 G1 已调优参数

```bash
-XX:+UseG1GC
-XX:MaxGCPauseMillis=50
-XX:G1HeapRegionSize=8m
-XX:InitiatingHeapOccupancyPercent=45
-XX:+ParallelRefProcEnabled
```

> G1 的 STW 暂停受堆大小和存活对象数量影响，在 10GB 堆下很难保证 <100ms。

---

## 4. 第二阶段：迁移到 ZGC

### 4.1 迁移步骤

```bash
# 第一步：仅替换 GC，其他参数不变
java \
  -Xms10g -Xmx10g \
  -XX:+UseZGC \
  -jar risk-engine.jar
```

### 4.2 初步结果

| 指标 | G1 | ZGC (Non-Gen) |
|------|-----|---------------|
| 最大 GC 暂停 | 180ms | 2ms |
| P99 延迟 | 120ms | 55ms |
| 吞吐量 | 5,000 TPS | 4,200 TPS (-16%) |

> **问题**: Non-Generational ZGC 延迟极佳，但吞吐量下降 16%。原因：所有对象（包括朝生夕灭的短期对象）都需要并发标记和重定位。

---

## 5. 第三阶段：Non-Generational ZGC 调优

### 5.1 调优参数

```bash
-XX:+UseZGC
-XX:ZCollectionInterval=0        # 不定时触发
-XX:ZAllocationSpikeTolerance=2  # 分配尖峰容忍度
-XX:+UnlockDiagnosticVMOptions
-XX:+ZStatisticsForceTrace        # 启用统计跟踪
-XX:+UseLargePages                # 使用大页面
```

### 5.2 调优后结果

| 指标 | ZGC 默认 | ZGC 调优后 |
|------|----------|-----------|
| 最大 GC 暂停 | 2ms | 1.5ms |
| 吞吐量 | 4,200 TPS | 4,500 TPS |
| 内存占用 | 10GB | 10.5GB (+大页面开销) |

> 吞吐量改善有限。根本原因是 Non-Gen ZGC 需要处理所有对象。

---

## 6. 第四阶段：迁移到 Generational ZGC

### 6.1 JDK 21 Generational ZGC

```bash
# JDK 21: 需显式启用分代模式
java \
  -Xms10g -Xmx10g \
  -XX:+UseZGC \
  -XX:+ZGenerational \
  -jar risk-engine.jar
```

```bash
# JDK 23+: 分代模式为默认
java \
  -Xms10g -Xmx10g \
  -XX:+UseZGC \
  -jar risk-engine.jar
```

### 6.2 Generational ZGC 结果

| 指标 | G1 | ZGC (Non-Gen) | ZGC (Gen) |
|------|-----|---------------|-----------|
| 最大 GC 暂停 | 180ms | 2ms | 1.5ms |
| P99 延迟 | 120ms | 55ms | 25ms |
| 吞吐量 | 5,000 TPS | 4,200 TPS | 4,950 TPS |
| 内存开销 | 10GB | 11GB | 11.5GB |

> **关键发现**: Generational ZGC 的吞吐量接近 G1，同时保持了 <2ms 的暂停时间。

---

## 7. 第五阶段：最终精调

### 7.1 最终参数

```bash
java \
  -Xms10g -Xmx10g \
  -XX:+UseZGC \
  -XX:+ZGenerational \
  -XX:+UseLargePages \
  -XX:+UseNUMA \
  -XX:ZAllocationSpikeTolerance=3 \
  -XX:ConcGCThreads=4 \
  -Xlog:gc*:file=/logs/gc.log:time,level,tags:filecount=5,filesize=100m
```

### 7.2 监控配置

```bash
# 持续 JFR 监控
-XX:StartFlightRecording=duration=24h,filename=/logs/recording.jfr,settings=profile
```

---

## 8. 最终效果对比

| 指标 | G1 (初始) | Gen ZGC (最终) | 改善 |
|------|----------|---------------|------|
| P50 延迟 | 8ms | 3ms | -63% |
| P99 延迟 | 120ms | 25ms | -79% |
| P999 延迟 | 350ms | 45ms | -87% |
| 最大 GC 暂停 | 180ms | 1.5ms | -99% |
| 吞吐量 | 5,000 TPS | 4,950 TPS | -1% |
| 内存占用 | 10GB | 11.5GB | +15% |

> **说明**: 上述数据为示意数据。Gen ZGC 的代价是额外的内存开销（约 15%），换来的是极致的延迟稳定性。

---

## 9. 经验总结与 Checklist

### G1 → ZGC 迁移 Checklist

- [ ] 确认 JDK 版本 ≥ 21（推荐 JDK 25+ 以获得最新 Gen ZGC 改进）
- [ ] 评估堆大小是否充足（ZGC 需要约 15-20% 额外内存开销）
- [ ] 评估吞吐量需求（ZGC 吞吐量通常低于 G1 约 0-5%）
- [ ] 确认没有依赖 GC 行为的代码（如 `System.gc()` 调用、Finalizer）
- [ ] 使用 `-XX:+ZGenerational` 启用分代模式（JDK 21 必须，JDK 23+ 默认）
- [ ] 在 staging 环境做充分的压力测试
- [ ] 配置 GC 日志以便回溯分析
- [ ] 考虑使用大页面（`-XX:+UseLargePages`）降低 TLB miss

### 关键经验

1. **Non-Gen ZGC 延迟极佳但吞吐量有损失**——对于吞吐量敏感场景，优先使用 Generational ZGC
2. **内存开销不可忽视**——10GB 堆的 ZGC 实际可能需要 11.5GB 物理内存
3. **大页面效果显著**——在 Linux 上启用 transparent huge pages 可降低 5-10% 的 GC 开销
4. **NUMA 感知**——多插槽服务器务必启用 `-XX:+UseNUMA`

### 相关资源

- [GC 调优实战：电商订单服务](gc-tuning-case.md)
- [G1 vs ZGC vs Shenandoah 对比](/guides/comparisons/g1-vs-zgc-vs-shenandoah.md)
- [JEP 439: Generational ZGC](/jeps/gc/jep-439.md)
- [GC 演进时间线](/by-topic/core/gc/)
