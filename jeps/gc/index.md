# GC (垃圾收集) JEPs

> JDK 21-26 垃圾收集器相关 JEP 汇总

---

## 概览

```
JDK 21 ───── JDK 22 ───── JDK 23 ───── JDK 24 ───── JDK 25 ───── JDK 26
   │            │            │            │            │            │
Gen ZGC     Region      Gen ZGC     移除非Gen    Gen Sheno.   G1 吞吐
(正式)      Pinning      默认Gen      ZGC模式     (正式)       优化
```

---

## ZGC (Z Garbage Collector)

### 演进历程

| 版本 | JEP | 状态 | 说明 |
|------|-----|------|------|
| JDK 15 | 377 | ✅ 正式 | ZGC 首次正式发布 |
| JDK 21 | 439 | ✅ 正式 | 分代 ZGC |
| JDK 23 | 474 | ✅ 正式 | 分代模式成为默认 |
| JDK 24 | 490 | ✅ 正式 | 移除非分代模式 |

### 分代 ZGC (Generational ZGC)

**JEP 439** (JDK 21) 引入分代收集：

```bash
# 启用分代 ZGC
-XX:+UseZGC -XX:+ZGenerational

# JDK 23+ 默认即为分代模式
-XX:+UseZGC
```

**核心改进**：
- **分代收集**：年轻代 + 老年代分离
- **更低延迟**：减少 STW 停顿时间
- **更高吞吐**：适合大内存应用

**详见**：[ZGC 分代模式分析](zgc-generational.md) | [JEP 439](jep-439.md) | [JEP 474](jep-474.md) | [JEP 490](jep-490.md)

---

## G1 GC

### 演进历程

| 版本 | JEP | 状态 | 说明 |
|------|-----|------|------|
| JDK 22 | 423 | ✅ 正式 | Region Pinning |
| JDK 24 | 475 | ✅ 正式 | Late Barrier Expansion |
| JDK 26 | 522 | ✅ 正式 | 吞吐量优化 |

### 关键优化

**Region Pinning (JDK 22)**：
- 解决 JNI Critical 区域导致的内存钉扎问题
- 允许 G1 在有钉扎对象时仍能收集

**Late Barrier Expansion (JDK 24)**：
- 延迟屏障扩展，减少编译开销
- 提升 G1 编译性能

**详见**：[G1 GC 优化分析](g1-improvements.md) | [JEP 423](jep-423.md) | [JEP 475](jep-475.md) | [JEP 522](jep-522.md)

---

## Shenandoah GC

### 演进历程

| 版本 | JEP | 状态 | 说明 |
|------|-----|------|------|
| JDK 12 | 189 | ✅ 正式 | Shenandoah 首次发布 |
| JDK 25 | 521 | ✅ 正式 | 分代 Shenandoah |

### 分代 Shenandoah (JDK 25)

```bash
# 启用分代 Shenandoah
-XX:+UseShenandoahGC -XX:+ShenandoahGenerational
```

**核心改进**：
- 年轻代 + 老年代分离
- 更好的短期对象处理
- 更低的 GC 停顿

**详见**：[Shenandoah 分析](shenandoah.md) | [JEP 521](jep-521.md)

---

## 性能对比

### 延迟对比 (99th percentile)

| GC | 小堆 (1GB) | 中堆 (16GB) | 大堆 (64GB) |
|----|-----------|-------------|-------------|
| G1 | ~50ms | ~100ms | ~200ms |
| ZGC | ~1ms | ~1ms | ~1ms |
| Shenandoah | ~5ms | ~10ms | ~20ms |

### 吞吐量对比

| GC | 相对吞吐量 |
|----|-----------|
| G1 | 100% (基准) |
| ZGC | ~95% |
| ZGC (分代) | ~98% |
| Shenandoah | ~97% |
| Shenandoah (分代) | ~99% |

---

## 选择指南

| 场景 | 推荐 GC | 原因 |
|------|---------|------|
| 通用应用 | G1 | 平衡延迟和吞吐 |
| 低延迟要求 | ZGC | 亚毫秒级停顿 |
| 大堆内存 | ZGC | 停顿时间与堆大小无关 |
| 高吞吐量 | Parallel | 最大化 CPU 利用 |
| 容器环境 | G1/ZGC | 资源感知 |

---

## VM 参数参考

### G1 GC
```bash
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
-XX:G1HeapRegionSize=16m
```

### ZGC
```bash
-XX:+UseZGC
-XX:+ZGenerational          # JDK 21-22
-XX:SoftMaxHeapSize=4g
-XX:ZCollectionInterval=5
```

### Shenandoah
```bash
-XX:+UseShenandoahGC
-XX:+ShenandoahGenerational  # JDK 25+
```

---

## 相关链接

- [OpenJDK: ZGC](https://wiki.openjdk.org/display/zgc)
- [OpenJDK: Shenandoah](https://wiki.openjdk.org/display/shenandoah/Main)
- [GC 主题时间线](/by-topic/gc/)
