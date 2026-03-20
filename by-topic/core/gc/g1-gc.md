# G1 GC 详解

> Garbage-First GC 架构、原理与调优

[← 返回 GC](../)

---

## 架构原理

### G1 Heap Layout

```
┌─────────────────────────────────────────────────────────┐
│                    G1 Heap Layout                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐  │
│  │ R1 │ R2 │ R3 │ R4 │ R5 │ R6 │ R7 │ R8 │... │ RN │  │
│  └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘  │
│                                                         │
│  Region = 1MB~32MB (必须是 2 的幂)                      │
│                                                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────────────────┐    │
│  │  Eden   │  │ Survivor│  │        Old          │    │
│  │ Regions │  │ Regions │  │      Regions        │    │
│  └─────────┘  └─────────┘  └─────────────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**关键概念**:
- **Region**: 堆被划分为固定大小的区域
- **Eden**: 新对象分配区域
- **Survivor**: 存活对象经过多次 GC 后晋升
- **Old**: 长存活对象

### G1 GC 工作流程

```
1. Young GC (Minor GC)
   ├── 标记 Eden Region
   ├── 复制存活对象到 Survivor Region
   ├── 维护年龄阈值
   └── 空的 Region 加入回收列表

2. Concurrent Mark (并发标记)
   ├── Initial Mark (STW, 与 Young GC 并行)
   ├── Root Region Scan
   ├── Concurrent Mark
   ├── Remark (STW, 处理 SATB)
   └── Cleanup (STW)

3. Mixed GC
   ├── Young Region + Old Region
   ├── 复制存活对象到空 Region
   ├── 处理跨代引用
   └── 空的 Region 回收

4. Full GC (退化时)
   └── 单线程 Mark-Sweep-Compact
```

---

## 关键技术

### Region 分配

**Humongous Region**: 超大对象 (>8MB)
- 单独占用一个或多个连续 Region
- 不参与 Mixed GC
- 在 Full GC 时回收

### Remembered Set (RSet)

**作用**: 记录跨 Region 引用

**实现**:
```cpp
// RSet 记录: Region A 引用了 Region B 的对象
Region A -> RSet -> Region B
```

**SATB vs Incremental Update**:
- **SATB (Snapshot-At-The-Beginning)**: 并发标记开始时的快照
- **Incremental Update**: 增量更新记录

### Card Table

**作用**: 记录跨代引用

**结构**:
- 每个 512 字节对应一个 Card
- Card 标记对应 Region 的脏页信息

---

## 性能优化

### JDK 26: JEP 522

**改进**: 减少 G1 GC 同步开销

**效果**:
- 吞吐量提升 10-20%
- 写屏障从 ~50 指令减少到 ~12 指令
- 减少 card table 同步频率

**相关链接**: [JEP 522](https://openjdk.org/jeps/522)

### Region Pinning

**作用**: 防止 GC 移动正在被读取的 Region

**场景**:
- JNI GetPrimitiveArrayCritical
- Unsafe 内存访问
- 减少 GC 竞争

**相关链接**: [Understanding Region Pinning in G1 GC](https://www.kosmadunikowski.com/posts/understanding-region-pinning-in-g1-gc/)

---

## VM 参数

### 基础参数

```bash
# 选择 G1 GC (JDK 9+ 默认)
-XX:+UseG1GC

# 目标暂停时间
-XX:MaxGCPauseMillis=200       # 最大 GC 暂停时间 (默认 200ms)
-XX:GCPauseIntervalMillis=200  # 期望暂停间隔

# Region 大小
-XX:G1HeapRegionSize=16m       # Region 大小 (1-32MB, 2 的幂)
```

### 调优参数

```bash
# 保留堆
-XX:G1ReservePercent=10        # 保留堆比例 (默认 10)

# 并发标记
-XX:ConcGCThreads=4             # 并发标记线程数
-XX:ParallelGCThreads=8         # 并发 GC 线程数

# Mixed GC
-XX:G1MixedGCCountTarget=8     # Mixed GC 触发次数
-XX:G1OldCSetRegionThreshold=2  # Old Region 回收阈值
```

### 诊断参数

```bash
# 详细日志
-XX:+PrintGCDetails            # 详细 GC 信息
-XX:+PrintGCTimeStamps        # GC 时间戳
-XX:+PrintGCApplicationStoppedTime  # 应用暂停时间

# 统计信息
-XX:+G1SummarizeConcMark       # 并发标记统计
-XX:+G1TraceConcMark         # 并发标记跟踪
```

---

## 性能调优

### 延迟优先

```bash
-XX:MaxGCPauseMillis=50        # 目标暂停 50ms
-XX:G1HeapRegionSize=8m        # 更小的 Region
-XX:G1MixedGCCountTarget=16    # 更频繁的 Mixed GC
```

### 吞吐量优先

```bash
-XX:MaxGCPauseMillis=500       # 放宽暂停时间
-XX:G1HeapRegionSize=32m       # 更大的 Region
-XX:G1MixedGCCountTarget=4     # 减少 Mixed GC 频率
-XX:G1ReservePercent=5         # 减少保留堆
```

### 大内存 (>16GB)

```bash
-XX:G1HeapRegionSize=32m       # 更大的 Region
-XX:ConcGCThreads=8            # 增加并发标记线程
-XX:G1MixedGCCountTarget=8     # 优化 Mixed GC
```

---

## 常见问题

### Full GC 过多

**原因**:
- Old Region 回收不及时
- 分配速度 > 回收速度
- 并发标记失败

**解决**:
```bash
-XX:G1MixedGCCountTarget=8     # 降低 Mixed GC 触发阈值
-XX:G1ReservePercent=10        # 增加保留堆
-XX:InitiatingHeapOccupancyPercent=45  # 降低并发触发阈值
```

### GC 停顿过长

**原因**:
- Region 碎片过多
- Mixed GC 处理过多 Region
- 保留堆过小

**解决**:
```bash
-XX:MaxGCPauseMillis=200       # 明确目标暂停时间
-XX:G1HeapRegionSize=16m       # 调整 Region 大小
-XX:G1MixedGCCountTarget=8     # 优化 Mixed GC
```

---

## 相关链接

- [VM 参数](../vm-parameters.md) - GC 参数完整参考
- [调优指南](../tuning.md) - GC 选择与调优策略
- [近期改进](../recent-changes.md) - JDK 21-26 GC 改进
- [G1 GC 文档](https://docs.oracle.com/en/java/javase/21/gctuning/garbage-first-garbage-collector1.html)
