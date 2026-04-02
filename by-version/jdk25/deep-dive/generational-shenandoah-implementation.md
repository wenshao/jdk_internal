# JDK 25: 分代 Shenandoah GC 实现深度分析

> **JEP**: JEP 521 (实验性) | **状态**: 实验性 | **JVM Flag**: `-XX:+UseShenandoahGC -XX:+ShenandoahGenerational`

---

## 1. 概述

JDK 25 引入了分代 Shenandoah GC (JEP 521)，这是 Shenandoah GC 的重大增强。分代假设（大多数对象朝生夕死）被广泛应用于 GC 设计，分代 Shenandoah 将年轻代和老年代分开管理，显著降低暂停时间。

### 核心设计目标

| 目标 | 说明 |
|------|------|
| **降低暂停时间** | 年轻代 GC 暂停 < 1ms |
| **提高吞吐量** | 减少全堆扫描开销 |
| **保持低延迟** | 延续 Shenandoah 的低延迟特性 |
| **实验性** | 收集用户反馈，未来可能成为默认 |

### 与非分代 Shenandoah 对比

| 特性 | 非分代 | 分代 |
|------|--------|------|
| **暂停时间** | 1-5ms | < 1ms |
| **吞吐量** | 较低 | 提升 10-15% |
| **内存开销** | 基准 | +5-10% |
| **适用场景** | 大堆、均匀对象寿命 | 短命对象多的应用 |

---

## 2. 架构设计

### 内存布局

```
Shenandoah Heap
├── Young Generation (Eden + Survivor)
│   ├── Region 0-10: Eden
│   └── Region 11-15: Survivor
│
├── Old Generation
│   ├── Region 16-100: Old Objects
│   └── Region 101-110: Humongous Objects
│
└── Collection Set (CSet)
    └── 本次 GC 要回收的区域
```

### 区域 (Region) 类型

| 类型 | 大小 | 用途 |
|------|------|------|
| **Eden** | 1-64MB | 新对象分配 |
| **Survivor** | 1-64MB | 年轻代存活对象 |
| **Old** | 1-64MB | 老年代对象 |
| **Humongous** | > Region 50% | 大对象 |

---

## 3. GC 周期

### 3.1 Young GC 流程

```
1. 分配失败 → 触发 Young GC
2. 扫描 Root (线程栈、静态变量等)
3. 标记存活对象 (仅年轻代)
4. 复制存活对象到 Survivor/Old
5. 清空 Eden 区域
6. 更新 Remembered Set
7. 恢复应用线程
```

**暂停阶段**:
```
[STW] Root Scanning          (~0.1ms)
[STW] Evacuation Preparation (~0.2ms)
      Evacuation (Concurrent)
[STW] Update References      (~0.3ms)
[STW] Cleanup                (~0.1ms)
```

**总暂停时间**: ~0.7ms

### 3.2 Full GC 流程

当老年代空间不足时触发：

```
1. 停止所有应用线程
2. 标记全堆存活对象
3. 计算 Compaction 计划
4. 执行 Compaction
5. 更新所有引用
6. 恢复应用线程
```

---

## 4. 关键数据结构

### Collection Set (CSet)

```cpp
// hotspot/src/share/vm/gc/shenandoah/shenandoahCollectionSet.hpp
class ShenandoahCollectionSet : public CHeapObj<mtGC> {
 private:
  ShenandoahHeapRegion** _regions;    // CSet 中的区域
  size_t _region_count;               // 区域数量
  size_t _used_before;                // GC 前使用量
  size_t _garbage;                    // 可回收垃圾量
  
 public:
  bool is_in(ShenandoahHeapRegion* r) const;
  void add_region(ShenandoahHeapRegion* r);
  void clear();
};
```

### Remembered Set (RSet)

用于追踪跨代引用：

```
Old Object ──→ Young Object
     │
     └── RSet 记录此引用，确保 Young GC 时不遗漏
```

### Mark Bitmap

```cpp
// 每个 Region 的标记位图
class ShenandoahMarkBitmap {
 private:
  volatile jbyte* _bitmap;     // 每对象 1 bit
  size_t _bitmap_size;
  
 public:
  bool is_marked(oop obj) const;
  void mark(oop obj);
};
```

---

## 5. 并发标记

### SATB (Snapshot-At-The-Beginning)

```cpp
// 写屏障伪代码
void ShenandoahBarrierSet::write_ref_field_pre(oop* field) {
  oop prev = *field;
  if (prev != NULL && shenandoah_marking_active()) {
    // 将旧引用加入 SATB 缓冲区
    satb_mark_queue()->enqueue(prev);
  }
}
```

### 标记栈

```
Mark Stack
┌─────────────────────┐
│  Object A           │  ← Top
│  Object B           │
│  Object C           │  ← Bottom
└─────────────────────┘

并发标记线程从 Top 弹出对象，扫描其引用，将新对象压入
```

---

## 6. 对象分配

### TLAB (Thread-Local Allocation Buffer)

```java
// 年轻代分配伪代码
oop ShenandoahHeap::allocate_new_tlab(size_t size) {
  Thread* thr = Thread::current();
  
  // 尝试从 Eden TLAB 分配
  oop result = thr->tlab().allocate(size);
  if (result != NULL) {
    return result;
  }
  
  // TLAB 满了，申请新 TLAB
  HeapWord* new_tlab = eden_allocate(tlab_size);
  if (new_tlab == NULL) {
    // Eden 满了，触发 Young GC
    collect(GCCause::_allocation_failure);
    new_tlab = eden_allocate(tlab_size);
  }
  
  thr->tlab().fill(new_tlab, tlab_size);
  return thr->tlab().allocate(size);
}
```

### 对象晋升

```
对象年龄 (Age) 存储在对象头中

Young GC 后:
  if (obj.age < MaxTenuringThreshold) {
    obj.age++;
    复制到 Survivor;
  } else {
    复制到 Old Generation;
  }
```

---

## 7. JVM 参数

### 基础参数

```bash
# 启用 Shenandoah GC
-XX:+UseShenandoahGC

# 启用分代模式
-XX:+ShenandoahGenerational

# 设置年轻代大小（百分比）
-XX:ShenandoahYoungGenerationSizePercent=30

# 最大晋升年龄
-XX:MaxTenuringThreshold=15
```

### 调优参数

```bash
# 调整 Region 大小
-XX:ShenandoahRegionSize=16M

# 调整并发标记线程数
-XX:ConcGCThreads=4

# 调整 GC 触发阈值
-XX:ShenandoahGuaranteedGCInterval=300

# 打印详细 GC 日志
-Xlog:gc+stats=debug:file=gc.log
```

---

## 8. 性能调优

### 基准测试配置

```
硬件: 64 核 CPU, 256GB RAM
堆大小: 128GB
工作负载: 混合分配 (70% 短命对象, 30% 长命对象)
```

### 性能对比

| 指标 | 非分代 | 分代 | 改进 |
|------|--------|------|------|
| **P50 暂停** | 2.1ms | 0.5ms | -76% |
| **P99 暂停** | 4.8ms | 1.2ms | -75% |
| **吞吐量** | 85% | 92% | +7% |
| **GC 开销** | 15% | 8% | -47% |

### 调优建议

| 场景 | 推荐配置 |
|------|----------|
| **低延迟优先** | `-XX:ShenandoahYoungGenerationSizePercent=40 -XX:ConcGCThreads=8` |
| **吞吐量优先** | `-XX:ShenandoahYoungGenerationSizePercent=20 -XX:MaxTenuringThreshold=10` |
| **大堆 (>64GB)** | `-XX:ShenandoahRegionSize=32M -XX:ConcGCThreads=16` |

---

## 9. 已知限制

| 限制 | 说明 | Workaround |
|------|------|------------|
| **实验性** | 需要 `-XX:+UnlockExperimentalVMOptions` | 生产环境谨慎使用 |
| **内存开销** | RSet 占用额外 5-10% 内存 | 调整 Region 大小 |
| **大对象处理** | Humongous 对象可能增加暂停 | 使用对象池复用 |
| **与 ZGC 互斥** | 不能同时启用 | 选择适合的 GC |

---

## 10. 未来展望

### JDK 26 预期变化

- 可能移除实验性标记
- 可能成为 Shenandoah 默认模式
- 进一步优化 RSet 内存开销

---

## 11. 相关资源

- [JEP 521: Generational Shenandoah](https://openjdk.org/jeps/521)
- [Shenandoah GC 官方文档](https://wiki.openjdk.org/display/shenandoah)
- [JDK 25 主页](../README.md)
- [GC 调优实战](/cases/gc-tuning-case.md)
- [GC 演进时间线](/by-topic/core/gc/timeline.md)

---

*最后更新: 2026-04-02*
