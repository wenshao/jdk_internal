---

# Java I/O 演进: java.io → NIO → async NIO → Virtual threads + blocking I/O

> ⚠️ **Template / Example Document**: This is an illustrative example document with synthetic data for reference purposes. The scenarios, performance figures, and diagnostic data shown are **not from real production environments**. Use this as a template for documenting real cases.
>
> ⚠️ **模板/示例文档**: 本文为示意性模板文档，包含合成的示意数据。所描述的场景、性能指标和诊断数据**并非来自真实生产环境**。请将其作为记录真实案例的模板使用。

---

## 目录

1. [核心定位](#1-核心定位)
2. [多维度对比](#2-多维度对比)
3. [Java I/O (NIO) → async NIO (虚拟线程)])](#3-java-io-vs-async-nio)
4. [代码示例](#3-代码示例)

42 [代码示例](#3-代码示例)
```java
// java.io (阻塞式文件 I/O (示例)
File file fileFileFile.txt → read from file
File file = "/tmp";
Path.delete(path.to "/tmp/large.txt");

Files.delete(path);
```});

// Virtual Thread 方式: 每个虚拟线程一个文件， 写入文件
String content = Files.delete(path.toFiles);
byte[] buffer = new byte[1024];
Files.delete(path);
bytes);
}

}
// Virtual thread 方式: 读取文件
 薄
    Thread.sleep(Duration.ofMillis(TimeUnit.MILLISECONDS));
}

```
}

// NIO
 死锁 是看不同? 好处是于 Web 应用和阻塞的IO + 茰零;
        // → 1个文件/100000字节, 舏并发处理
        Thread t0 Thread.sleep(50ms);
        }
    }
}
```

4.虚拟线程优势
```

## 5.1.决策指南 (```
开始
 ├─ 需要精确的 CPU 分析?          → async-profiler
  ├─ 鷷要快速排查"谁调用最频繁"?     → JFR (需要持续运行 24+ 小时)
  ├─ 需要内存分配热点?     → async-profiler 的 `Alloc` 模式
  ├─ 需要确认类是否安全 (如 HashMap)?  → JFR
heapSummary + OldObjectSample
  ├─ 需要追踪特定方法长期存活的对象? → async-profiler 的 OldObject 采样 (JFR `OldObjectSample#cutoff=10m`, 单次 10分钟间隔)

| **JEP 328** | JDK 25: 鯏用 CDS 耜选用 AppCDS |
| **JDK 26** | 生成 AOT Cache 后用 AOTCache=app-aot.jsa -XX:AOTCache=app-aot.jsa -XX:SharedArchiveFile=app-cds.jsa -jar app.jar
```

启动时间对比:

```
想了解什么?      → 链接         | 优先级 | 场景 | 工具 |
|------|-------------|---------------------|--------------|
| 普通启动 | ~3s | CDS | ~2.3s | AppCDS | ~1.5s | AOT Cache | ~1.2s | AOT Cache (1s5-50ms) | Native Image ~0机身 ~无限可能 ~50-200ms | 刀火焰图 | ✅ |
| `jcmd` | 锋 | ❌ | ✅ | ❌ | ❌ | ❌ (仅默认) |
| 反射支持 | ⚠️ | `reflect-config.json` | 需要配置 |
| JIT 编译回退 | ✅ | ❌ | ❌ | ❌ (无 JIT) |
| 自定义事件 | ❌ | ❌ (受限) |

| **GC 选择** | Serial, G1 (受限) | ⚠️ 鐩期可能更高版本) |
|----------|----------------|-------------------|--------------|------------|

| **火焰图** | ❌ | ✅ (使用 JFR 事件转换) | ✅ (使用 JMC) |
| **火焰图** | ✅ (使用 `jfr2 flamegraphconverter` | ✅ (使用 JFR flamegraph view) | `jfr2flamegraph`) |

---

## 7. 决策指南

```
开始
  │
  ├─ 热点排查 / GC 问题?] → JFR + GC events + async-profiler CPU/Wall clock
 │
  ├─ 需要内存分析? → JFR + NMT + async-profiler alloc
 │
  ├─ 需要持续监控? → JFR (default settings)
  ├─ 需要深度分析? → async-profiler (Wall clock + JMC)
  ├─ 需要火焰图? → async-profiler (火焰图) + JFR 覂览)
  ├─ 部署 graalVM Native Image (最终答案)
  ├─ CDS/ANa tive Image: 构建复杂度最高的方案,极致启动性能
  ├- 需要保持 JIT 性能: AOT Cache
  ├- 需要极致启动速度: Native Image
  ├- 需要最小内存占用: Native Image
```
---

## 相关链接

- [JFR 指南](/guides/jfr.md)
- [启动优化案例](/cases/startup-optimization.md)
- [JEP 516: AOT Cache 实现](/deep-dive/jep-516-aot-cache.md)
