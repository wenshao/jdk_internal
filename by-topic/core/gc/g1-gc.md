# G1 GC 详解

> Garbage-First GC 架构、原理与 JDK 26 (JEP 522) 深度优化

[← 返回 GC](../)

---

## 1. 架构原理

### 1.1 G1 Heap Layout (区域化布局)

G1 取代了传统的物理连续的分代布局，将堆内存划分为多个大小相等的独立 **Region**。

```
┌─────────────────────────────────────────────────────────┐
│                    G1 Heap Layout                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐  │
│  │ E  │ S  │ O  │ E  │ H  │ O  │ E  │ S  │ H  │... │  │
│  └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘  │
│                                                         │
│  Region 大小: 1MB ~ 32MB (必须是 2 的幂)                 │
│  堆内存最大支持: 2048 个 Region                          │
│                                                         │
│  角色标识:                                              │
│  - E (Eden): 新对象分配区                               │
│  - S (Survivor): 存活对象晋升区                         │
│  - O (Old): 老年代区域                                  │
│  - H (Humongous): 巨大对象区 (> 50% Region Size)        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**设计优势**:
- **增量回收**: 每次只回收价值最高（垃圾最多）的 Region 集合（CSet），从而实现可预测的停顿时间。
- **避免碎片**: 采用标记-复制算法，通过 Region 间的移动实现内存紧缩。

---

## 2. 核心技术组件

### 2.1 Remembered Set (RSet) & Card Table

G1 使用 RSet 来解决**跨 Region 引用**的扫描问题，避免为了回收一个 Region 而扫描整个堆。

- **Card Table (卡表)**: 堆内存的字节数组，每 512 字节对应一个 Card。若该区域有引用变更，对应 Card 标记为 "Dirty"。
- **RSet (记忆集)**: 记录“谁引用了我”。每个 Region 维护一个 RSet，内部存储了指向该 Region 的 Dirty Cards 列表。

### 2.2 写屏障 (Write Barrier) 与 SATB

G1 属于 **并发标记 (Concurrent Marking)** 收集器，为了保证并发标记的正确性，使用了 **SATB (Snapshot-At-The-Beginning)** 算法：

- **写前屏障 (Pre-Write Barrier)**: 拦截引用的修改，将被覆盖的旧对象压入 SATB 队列，确保标记开始时的存活对象“快照”不丢失。
- **写后屏障 (Post-Write Barrier)**: 记录新引用的产生，更新卡表并通知 Refine 线程处理 RSet。

---

## 3. JDK 26 重大突破: JEP 522 (G1 吞吐量优化)

JEP 522 是 G1 近年来最核心的性能改进，通过引入 **Claim Table (认领表)** 机制大幅减少了写屏障的同步开销。

### 3.1 传统瓶颈: 卡表原子竞争
在 JDK 26 之前，多线程应用在更新同一卡表区域时，会产生激烈的原子操作（CAS）竞争，导致 CPU 指令周期浪费。

### 3.2 创新机制: Claim Table (认领表)
JEP 522 在卡表之上增加了一个轻量级的 **Claim Table**。

```
┌─────────────────────────────────────────────────────────┐
│ Claim Table 机制示意图                                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 1. 认领 (Claiming): 每个应用线程尝试“认领”一段卡表范围。    │
│ 2. 独占路径 (Fast Path): 线程在自己认领的区域内更新卡表，  │
│    无需任何原子指令或内存屏障。                          │
│ 3. 协作路径 (Slow Path): 若区域已被其他线程认领，则通过    │
│    Dirty Card Queue 异步处理。                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 3.3 汇编级对比 (x86-64)

| 指标 | JDK 26 (传统) | JDK 26 (JEP 522) |
|------|--------------|------------------|
| **核心指令** | `lock cmpxchg` (高昂原子操作) | `cmp` + `mov` (普通加载/存储) |
| **指令数** | ~50 条 | **~12 条** |
| **同步开销** | 线程间竞争激烈 | **近乎零竞争** |

### 3.4 源码路径 (HotSpot)
- `src/hotspot/share/gc/g1/g1CardTableClaimTable.cpp`: Claim Table 的核心实现。
- `src/hotspot/cpu/x86/gc/g1/g1BarrierSetAssembler_x86.cpp`: 优化后的汇编写屏障生成逻辑。

---

## 4. GC 运行周期深度解析

### 4.1 Young GC (STW)
Eden 满时触发，采用多线程并行复制存活对象。
- **根扫描**: 扫描栈、静态变量。
- **RSet 扫描**: 快速定位老年代对年轻代的引用。

### 4.2 Concurrent Marking (并发标记)
当堆占用达到 `InitiatingHeapOccupancyPercent` (IHOP) 阈值时触发。
1. **Initial Mark (STW)**: 标记 GC Roots 能直接关联的对象。
2. **Concurrent Mark**: 遍历对象图，与应用线程并发运行。
3. **Remark (STW)**: 处理 SATB 队列中的剩余变更。
4. **Cleanup (STW)**: 回收完全空的 Region，为下阶段做准备。

### 4.3 Mixed GC (增量回收)
核心特色。不仅回收年轻代，还根据停顿时间目标，挑选部分收益最高的老年代 Region 进行回收。
- **Refine 优化 (JDK 26)**: Refine 线程现在利用 Claim Table 信息进行**批量处理**，显著降低了 RSet 更新的平均延迟。

---

## 5. 性能表现与实战数据

根据 SPECjbb2015 行业标准测试，开启 JEP 522 后的 G1 表现：

| 指标 | 提升幅度 | 说明 |
|------|----------|------|
| **max-jOPS** | **+15.6%** | 峰值吞吐量大幅提升 |
| **critical-jOPS** | **+16.7%** | 低延迟下的有效吞吐量提升 |
| **GC 暂停时间** | **-20.8%** | 总体平均暂停时间缩短 |
| **写屏障 CPU 占比** | **从 8% 降至 3%** | 极大释放了计算资源 |

---

## 6. VM 核心参数调优

### 6.1 基础配置
```bash
-XX:+UseG1GC                    # 启用 G1 (JDK 9+ 默认)
-XX:MaxGCPauseMillis=200         # 核心目标：最大停顿时间 (默认 200ms)
-XX:G1HeapRegionSize=16m         # Region 大小 (1-32MB，必须是 2 的幂)
```

### 6.2 JEP 522 相关 (JDK 26+)

JEP 522 优化默认启用，无需 JVM 参数。

### 6.3 进阶调优
- **解决晋升失败**: 若 Full GC 频繁，尝试调低 `-XX:InitiatingHeapOccupancyPercent=40` 以更早启动并发标记。
- **处理巨型对象**: 若日志中频繁出现 `Humongous Allocation`，尝试增大 `-XX:G1HeapRegionSize=32m`。

---

## 7. 诊断与监控

### 7.1 统一日志 (Xlog)
```bash
# 查看详细的 GC 步骤耗时
-Xlog:gc+phases=debug

# 查看 RSet 更新和扫描详情
-Xlog:gc+remset=trace
```

### 7.2 HSDB 实战建议
使用 `jhsdb hsdb` 连接进程后，通过 `G1HeapRegion` 工具可以实时观察每个 Region 的角色（Eden/Old/Humongous）及其 RSet 的占用情况。

---

## 相关链接
- [GC 演进时间线](timeline.md)
- [VM 参数完整参考](vm-parameters.md)
- [JEP 522](/jeps/gc/jep-522.md)
- [G1 GC 源码 (GitHub)](https://github.com/openjdk/jdk/tree/master/src/hotspot/share/gc/g1)
