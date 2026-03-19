# 分代 ZGC 深度分析

> JDK 25 正式特性 - JEP 468

---

## 概述

Generational ZGC（分代 ZGC）将 Java 堆分为年轻代和老年代，大幅降低 GC 开销，提升大内存场景性能。

---

## 背景与动机

### ZGC 演进

| 版本 | 特性 | GC 开销 |
|------|------|---------|
| JDK 11 | 初始版本 | ~10% |
| JDK 15 | 并发类卸载 | ~8% |
| JDK 21 | 分代 ZGC (预览) | ~5% |
| JDK 25 | 分代 ZGC (正式) | ~4% |

### 非分代 vs 分代

```
非分代 ZGC:
┌─────────────────────────────────────┐
│         整个堆                        │
│  [新对象 + 存活对象混合]               │
│  → 需要频繁扫描整个堆                 │
└─────────────────────────────────────┘

分代 ZGC:
┌──────────────┬──────────────────────┐
│   年轻代      │      老年代            │
│  [新对象]     │   [存活对象]          │
│  → 只扫描年轻代  │  → 很少全堆扫描       │
└──────────────┴──────────────────────┘
```

---

## 核心设计

### 分代假设

```
弱分代假说:
- 大多数对象朝生夕死
- 老对象很少引用年轻对象
```

### ZGC 分代实现

```cpp
// HotSpot 源码结构
src/hotspot/share/gc/z/
├── zCollectedHeap.cpp      // 堆管理
├── zGeneration.cpp          // 分代实现 (新增)
├── zYoungGeneration.cpp     // 年轻代 (新增)
├── zOldGeneration.cpp       // 老年代 (新增)
├── zCollector.cpp           // 收集器
└── zRemembered.cpp          // 记忆集 (新增)
```

---

## GC 周期

### 年轻代 GC

```
1. 标记年轻代存活对象
2. 复制到幸存区或老年代
3. 并发执行，暂停时间 < 1ms
```

### 老年代 GC

```
1. 标记老年代存活对象
2. 处理跨代引用
3. 并发压缩
```

### 混合 GC

```
1. 年轻代 + 老年代一起收集
2. 处理记忆集
3. 比单独收集更高效
```

---

## 记忆集 (Remembered Set)

### 跨代引用跟踪

```java
// 老年代引用年轻代
class Old {
    Young youngRef;  // 需要记录
}

// 记忆集结构
struct RememberedSet {
    // 卡表标记
    CardTable* card_table;

    // 跨代引用
    HashSet<oop*> cross_gen_refs;
};
```

### 写屏障

```cpp
// 写屏障拦截跨代引用
void oop_store(oop* field, oop value) {
    if (is_old_gen(field) && is_young_gen(value)) {
        remembered_set->add(field);
    }
    *field = value;
}
```

---

## 性能数据

### GC 开销对比

| 场景 | 非分代 ZGC | 分代 ZGC | 改进 |
|------|-----------|----------|------|
| 大内存 (16GB) | 8% | 4% | -50% |
| 超大内存 (64GB) | 12% | 6% | -50% |
| 低延迟要求 | 5% pause | 3% pause | -40% |

### 吞吐量提升

```
Benchmark: SpecJBB
- 非分代 ZGC: 85,000 ops/min
- 分代 ZGC:   98,000 ops/min (+15%)
```

---

## 使用指南

### 启用分代 ZGC

```bash
# JDK 25 默认启用
java -XX:+UseZGC -XX:+ZGenerational MyApp

# 禁用分代（不推荐）
java -XX:+UseZGC -XX:-ZGenerational MyApp
```

### 调优参数

```bash
# 年轻代大小
-XX:ZYoungGenerationSize=512m

# 老年代大小
-XX:ZOldGenerationSize=4g

# 记忆集大小
-XX:ZRememberedSetSize=256m
```

---

## 监控与诊断

### GC 日志

```bash
# 启用 GC 日志
java -Xlog:gc*:gc.log -XX:+UseZGC -XX:+ZGenerational MyApp

# 日志示例
[0.234s][info][gc] GC(1) Young Generation Pause (G1 Evacuation Pause)...
[0.235s][info][gc] GC(1) Young: 512M->64M(512M) Pause: 1.23ms
[1.456s][info][gc] GC(2) Old Generation Pause...
[1.458s][info][gc] GC(2) Old: 4096M->4000M(4096M) Pause: 2.45ms
```

### JMX 监控

```java
// 获取 ZGC 统计
GarbageCollectorMXBean gc = ManagementFactory.getGarbageCollectorMXBeans()
    .stream()
    .filter(b -> b.getName().contains("ZGC"))
    .findFirst()
    .orElseThrow();

System.out.println("Collections: " + gc.getCollectionCount());
System.out.println("Time: " + gc.getCollectionTime() + "ms");
```

---

## 最佳实践

### 适用场景

```
✓ 推荐:
- 大内存应用 (>8GB)
- 长运行服务
- 对 GC 开销敏感的应用

✗ 不推荐:
- 小内存应用 (<2GB)
- 短运行任务
```

### 参数建议

```bash
# 通用推荐
java -XX:+UseZGC -XX:+ZGenerational -Xmx16g MyApp

# 低延迟场景
java -XX:+UseZGC -XX:+ZGenerational -Xmx32g \
     -XX:MaxGCPauseMillis=10 MyApp

# 高吞吐场景
java -XX:+UseZGC -XX:+ZGenerational -Xmx64g \
     -XX:GCTimeRatio=99 MyApp
```

---

## 相关链接

- [JEP 468: Generational ZGC](https://openjdk.org/jeps/468)
- [ZGC 官方文档](https://openjdk.org/projects/jdk/25/docs/specs/man/gc-zgc.html)
- [源码](https://github.com/openjdk/jdk/tree/master/src/hotspot/share/gc/z)
