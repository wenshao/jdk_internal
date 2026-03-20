# GC 调优指南

> GC 选择与性能优化策略

[← 返回 GC](../)

---

## 调优原则

### 明确目标

1. **延迟优先**: 最低暂停时间
2. **吞吐优先**: 最小 GC 开销
3. **内存优先**: 最小堆占用
4. **平衡**: 综合优化

### 调优流程

```
1. 监控分析
   ├── 收集 GC 日志
   ├── 分析暂停时间
   └── 识别瓶颈

2. 选择 GC
   ├── 根据目标选择
   ├── 根据堆大小选择
   └── 根据平台选择

3. 参数调优
   ├── 堆大小
   ├── GC 触发阈值
   └── 线程数

4. 验证优化
   ├── 压测验证
   ├── 监控指标
   └── 迭代优化
```

---

## 选择 GC

### 决策树

```
堆大小
  │
  ├─ < 2GB
  │   └─ Serial GC 或 Parallel GC
  │
  ├─ 2-16GB
  │   ├─ 延迟敏感 → G1 GC
  │   └─ 吞吐优先 → Parallel GC
  │
  └─ > 16GB
      ├─ x86_64/aarch64
      │   ├─ 极低延迟 (<10ms) → ZGC
      │   └─ 通用 → G1 GC
      │
      └─ 其他平台
          ├─ 低延迟 → Shenandoah
          └─ 通用 → G1 GC
```

### GC 对比

| 场景 | 推荐 GC | 理由 |
|------|---------|------|
| 微服务 (REST API) | ZGC | 低延迟，快速响应 |
| 批处理 | Parallel GC | 高吞吐量 |
| 流处理 | ZGC/Shenandoah | 稳定延迟 |
| 大内存分析 | ZGC | TB 级堆支持 |
| 嵌入式 | Serial GC | 低内存占用 |

---

## G1 GC 调优

### 延迟优先

```bash
-XX:+UseG1GC
-XX:MaxGCPauseMillis=50        # 目标暂停 50ms
-XX:G1HeapRegionSize=8m        # 更小的 Region
-XX:G1MixedGCCountTarget=16    # 更频繁的 Mixed GC
-XX:InitiatingHeapOccupancyPercent=35  # 更早触发并发
```

### 吞吐优先

```bash
-XX:+UseG1GC
-XX:MaxGCPauseMillis=500       # 放宽暂停时间
-XX:G1HeapRegionSize=32m       # 更大的 Region
-XX:G1MixedGCCountTarget=4     # 减少 Mixed GC 频率
-XX:G1ReservePercent=5         # 减少保留堆
```

### Full GC 优化

```bash
# 避免 Full GC
-XX:G1ReservePercent=10        # 增加保留堆
-XX:InitiatingHeapOccupancyPercent=40  # 更早触发
-XX:G1MixedGCCountTarget=8     # 优化 Mixed GC

# String 去重
-XX:+UseStringDeduplication
-XX:StringDeduplicationAgeThreshold=3
```

---

## ZGC 调优

### 基础配置

```bash
-XX:+UseZGC
-XX:+ZGenerational            # 分代模式 (JDK 21+)
-Xmx4g                        # 设置最大堆
```

### 低延迟优化

```bash
-XX:+UseZGC
-XX:+ZGenerational
-XX:ZCollectionInterval=5     # 自动 GC 间隔
-XX:ParallelGCThreads=8       # 增加 GC 线程
-XX:ConcGCThreads=4           # 并发标记线程
```

### NUMA 优化 (JDK 21+)

```bash
-XX:+UseNUMA                  # 启用 NUMA 感知
-XX:+UseNUMAInterleaving      # 交错分配
```

### 碎片控制

```bash
-XX:ZFragmentationLimit=25    # 碎片率阈值
-XX:ZAllocationSpikeTolerance=2.0  # 分配尖刺容忍
```

---

## Shenandoah GC 调优

### 基础配置

```bash
-XX:+UseShenandoahGC
-XX:ShenandoahGCHeuristics=adaptive  # 自适应启发式
```

### 延迟优先

```bash
-XX:+UseShenandoahGC
-XX:ShenandoahGCHeuristics=compact
-XX:ShenandoahGCThreshold=0
-XX:ShenandoahFreeThreshold=10
```

### 分代模式 (JDK 21+)

```bash
-XX:+UseShenandoahGC
-XX:ShenandoahGCHeuristics=generational
```

---

## Parallel GC 调优

### 吞吐优先

```bash
-XX:+UseParallelGC
-XX:GCTimeRatio=99            # GC 时间 < 1%
-XX:ParallelGCThreads=8        # STW 线程数
-XX:MaxGCPauseMillis=200       # (可选) 最大暂停
```

### 新生代优化

```bash
-XX:NewSize=512m
-XX:MaxNewSize=1g
-XX:SurvivorRatio=8
-XX:MaxTenuringThreshold=15
```

---

## 常见问题

### Full GC 过多

**G1 GC**:
```bash
-XX:InitiatingHeapOccupancyPercent=35  # 更早触发
-XX:G1MixedGCCountTarget=8
-XX:G1ReservePercent=10
```

**Parallel GC**:
```bash
-XX:MaxHeapFreeRatio=70        # 降低空闲阈值
-XX:MinHeapFreeRatio=40
```

### GC 停顿过长

**G1 GC**:
```bash
-XX:MaxGCPauseMillis=200       # 明确目标
-XX:G1HeapRegionSize=16m       # 调整 Region
-XX:G1MixedGCCountTarget=8
```

**ZGC**:
```bash
-XX:ZCollectionInterval=3      # 更频繁 GC
-XX:ParallelGCThreads=12       # 增加线程
```

### 内存碎片

**G1 GC**:
```bash
-XX:G1MixedGCCountTarget=12    # 更频繁 Mixed GC
```

**Parallel GC**:
```bash
-XX:+UseParallelGC
-XX:-UseParallelOldGC          # 禁用并行老年代 GC
```

---

## 监控工具

### GC 日志分析

```bash
# JDK 9+ 统一日志
-Xlog:gc*:file=gc.log:time,level,tags

# 分析工具
- GCViewer
- GCLogAnalyzer
- JITWatch
```

### JFR

```bash
# 记录 GC 事件
jcmd <pid> JFR.start name=gc \
  jdk.GCConfiguration=true \
  jdk.GCHeapSummary=true \
  jdk.GCHeapMemoryPool=true
```

### jstat

```bash
# GC 统计
jstat -gc <pid> 1000 10

# 容量统计
jstat -gccapacity <pid>

# 新生代统计
jstat -gcnew <pid>
```

---

## 性能指标

### 关键指标

| 指标 | 目标 | 说明 |
|------|------|------|
| GC 暂停时间 | <100ms | G1 目标 |
| GC 暂停时间 | <10ms | ZGC/Shenandoah 目标 |
| GC 频率 | <1次/秒 | 避免 GC 风暴 |
| 堆使用率 | 70-80% | 留有缓冲 |
| 吞吐量 | >98% | Parallel GC 目标 |

### 基准测试

```bash
# SPECjbb
java -jar specjbb.jar -m composite

# GC 测试
java -XX:+PrintGC -XX:+PrintGCDetails YourApp

# 压力测试
java -Xmx4g -Xms4g -XX:+UseG1GC YourApp
```

---

## JDK 版本建议

| JDK 版本 | 推荐 GC | 说明 |
|----------|---------|------|
| JDK 8 | G1 GC | 首个稳定版本 |
| JDK 11 | ZGC | 首个生产可用 ZGC |
| JDK 17 | ZGC/Shenandoah | 性能改进 |
| JDK 21+ | 分代 ZGC | 最佳性能 |
| JDK 23+ | 分代 ZGC (默认) | 默认启用分代 |

---

## 相关链接

- [G1 GC 详解](g1-gc.md) - G1 架构与调优
- [ZGC 详解](zgc.md) - ZGC 原理与配置
- [Shenandoah 详解](shenandoah.md) - Shenandoah 配置
- [VM 参数](vm-parameters.md) - 参数完整参考
