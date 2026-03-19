# GC 演进时间线

跨版本追踪垃圾收集器的发展历程。

---

## 时间线概览

```
JDK 8 ───── JDK 11 ───── JDK 15 ───── JDK 17 ───── JDK 21 ───── JDK 26
 │              │              │              │              │              │
 │              │              │              │              │              │
G1 默认        ZGC 引入       ZGC 生产      并发扫描      分代 ZGC      G1 +10-20%
Parallel 默认   (实验)                       Shenandoah    分代 Shen     ZGC NUMA
CMS 废弃        Shenandoah     Windows       JEP 379       JEP 439       JEP 522
               (实验)
```

---

## G1 GC

| 版本 | 变更 | 说明 |
|------|------|------|
| JDK 6 | G1 引入 | 替代 CMS 的低延迟 GC |
| JDK 7 | G1 完善 | 成为可选 GC |
| JDK 8 | G1 主流 | 大堆内存首选 |
| JDK 9 | **G1 默认** | 替代 ParallelGC |
| JDK 11 | 并发标记改进 | 降低 pause 时间 |
| JDK 17 | G1 Full GC 改进 | 降低 worst-case pause |
| JDK 21 | Region 固定 | 降低延迟 |
| JDK 26 | **吞吐量提升** (JEP 522) | +10-20% 吞吐量 |

→ [JDK 26 G1 优化](/by-version/jdk26/index.md#g1-吞吐量提升)

---

## ZGC (低延迟 GC)

| 版本 | 变更 | 状态 |
|------|------|------|
| JDK 11 | ZGC 引入 | 实验性，支持 Linux/macOS |
| JDK 14 | ZGC 生产可用 | 脱离实验标签 |
| JDK 15 | Windows 支持 | 跨平台完整支持 |
| JDK 17 | 并发线程栈扫描 | 降低 pause 时间 |
| JDK 21 | **分代 ZGC** (JEP 439) | 显著降低 GC 频率 |
| JDK 26 | NUMA-aware Relocation | 多插槽服务器优化 |

### ZGC 适用场景

- **大堆内存**：> 10GB
- **低延迟要求**：< 10ms pause
- **多线程应用**：并发标记优势明显

→ [ZGC 详细分析](zgc.md)

---

## Shenandoah

| 版本 | 变更 | 说明 |
|------|------|------|
| JDK 12 | Shenandoah 引入 | 实验性 |
| JDK 15 | Shenandoah 生产可用 | 脱离实验标签 |
| JDK 17 | 并发线程栈扫描 | 降低 pause 时间 |
| JDK 21 | **分代 Shenandoah** (JEP 439) | 降低 GC 频率 |
| JDK 26 | 进一步优化 | 持续改进 |

### Shenandoah vs ZGC

| 特性 | Shenandoah | ZGC |
|------|------------|-----|
| 设计理念 | 全并发 | 尽量并发 |
| Pause 目标 | < 10ms | < 10ms |
| 平台支持 | Linux/Windows/macOS | Linux/Windows/macOS |
| JDK 26 | 分代 | 分代 + NUMA |

---

## ParallelGC

| 版本 | 状态 | 说明 |
|------|------|------|
| JDK 8 | **默认 GC** | 吞吐量优先 |
| JDK 9 | 默认改为 G1 | 仍可通过参数使用 |
| JDK 11+ | 可选 | 吞吐量场景仍适用 |

---

## 历史版本

### CMS (Concurrent Mark Sweep)

- **JDK 5**: 引入
- **JDK 9**: 标记废弃
- **JDK 14**: **移除**

### Serial GC

- 保留用于单线程、小内存场景

---

## 选择建议

| 场景 | 推荐版本 | 推荐 GC |
|------|----------|---------|
| 小内存 (< 2GB) | 任何 | SerialGC |
| 通用场景 | 任何 | G1 |
| 大堆内存 (10GB+) | JDK 17+ | ZGC |
| 超低延迟 (< 10ms) | JDK 21+ | 分代 ZGC |
| 多插槽服务器 | JDK 26 | ZGC (NUMA-aware) |
| 吞吐量优先 | 任何 | ParallelGC |

---

## 相关链接

- [JEP 522: G1 GC Throughput](https://openjdk.org/jeps/522)
- [JEP 439: Generational ZGC](https://openjdk.org/jeps/439)
- [JEP 379: Shenandoah](https://openjdk.org/jeps/379)
