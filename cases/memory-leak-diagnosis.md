# 内存泄漏诊断实战

> 长期运行的后台服务在 JDK 21 环境下运行约 3 天后发生 OOM，本文记录完整的排查过程。

> **注意**: 本案例中所有监控数据、内存数值、对象数量等均为 **示意数据**，用于说明排查思路和工具用法。

---

## 目录

1. [场景描述](#1-场景描述)
2. [症状表现](#2-症状表现)
3. [第一步：JFR 分析](#3-第一步jfr-分析)
4. [第二步：NMT 分析](#4-第二步nmt-分析)
5. [第三步：Heap Dump 分析](#5-第三步heap-dump-分析)
6. [根因分析](#6-根因分析)
7. [修复方案](#7-修复方案)
8. [验证与回归](#8-验证与回归)
9. [经验总结](#9-经验总结)

---

## 1. 场景描述

### 业务背景

一个后台数据处理服务，负责消费 Kafka 消息并进行业务规则匹配和结果持久化。服务使用 Netty 进行内部 RPC 通信，并在内存中维护业务规则缓存。

### 环境配置

| 项目 | 配置 |
|------|------|
| JDK 版本 | JDK 21.0.2 (LTS) |
| GC | G1GC (默认) |
| 堆配置 | -Xms4g -Xmx4g |
| Metaspace | -XX:MaxMetaspaceSize=512m |
| 容器 | Kubernetes Pod, 8C/8G |
| 框架 | Spring Boot 3.2 + Netty 4.1 |

### JVM 启动参数 (关键部分)

```bash
java -Xms4g -Xmx4g -XX:+UseG1GC -XX:MaxMetaspaceSize=512m \
     -XX:NativeMemoryTracking=detail \
     -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/data/dumps/ \
     -XX:StartFlightRecording=disk=true,maxsize=500m,maxage=3d,dumponexit=true \
     -jar app.jar
```

> **最佳实践**: 生产环境建议始终开启 NMT 和 JFR (NMT ~5-10% 内存开销，JFR < 1% CPU)，出问题时能提供关键数据。

---

## 2. 症状表现

### 监控指标异常 (示意数据)

服务运行约 72 小时后，Prometheus/Grafana 监控显示：

```
# 堆内存使用趋势 (示意数据)
时间点          Used Heap    Old Gen     Full GC 次数
启动后 1h       1.2 GB       0.8 GB      0
启动后 24h      2.5 GB       2.3 GB      2
启动后 48h      3.2 GB       3.0 GB      15
启动后 72h      OOM          -           200+
```

**关键特征**: Old Gen 每小时增长 ~30-40 MB，Full GC 后无法回收; Full GC 从每 12 小时一次加速到每 30 分钟一次，耗时从 500ms 增长到 3-5 秒。

### OOM 错误日志

```
java.lang.OutOfMemoryError: Java heap space
    at java.base/java.util.HashMap.resize(HashMap.java:699)
    at java.base/java.util.HashMap.putVal(HashMap.java:657)
    at java.base/java.util.concurrent.ConcurrentHashMap.putVal(ConcurrentHashMap.java:1011)
    at com.example.service.RuleCache.addRule(RuleCache.java:87)
    ...
```

---

## 3. 第一步：JFR 分析

因为启动时已开启 JFR，OOM 前的数据已记录在 .jfr 文件中。

### 3.1 导出 JFR 数据

```bash
# 如果服务还活着，可以动态导出
jcmd <pid> JFR.dump name=1 filename=/data/jfr/dump_before_oom.jfr

# 如果服务已崩溃，直接使用 dumponexit 生成的文件
ls -lh /data/jfr/app.jfr
```

### 3.2 OldObjectSample 事件分析

OldObjectSample 是 JFR 中用于检测内存泄漏的关键事件。它记录了在 Old Gen 中存活的对象的分配栈和引用链。

```bash
# 使用 jfr 命令行工具查看 OldObjectSample 事件
jfr print --events jdk.OldObjectSample /data/jfr/app.jfr
```

输出示意 (示意数据)：

```
jdk.OldObjectSample {
  startTime = 2024-01-15T10:23:45.123Z
  allocationTime = 2024-01-14T08:15:22.456Z
  objectAge = 26h 8m 22s
  lastKnownHeapUsage = 3.4 GB
  object = {
    type = java.util.concurrent.ConcurrentHashMap$Node (objectSize = 48 bytes)
    referrer = {
      type = java.util.concurrent.ConcurrentHashMap$Node[] (objectSize = 16.0 MB)
      referrer = {
        type = java.util.concurrent.ConcurrentHashMap (objectSize = 64 bytes)
        field = "table"
        referrer = {
          type = com.example.service.RuleCache (objectSize = 32 bytes)
          field = "ruleMap"
          referrer = {
            type = com.example.service.RuleEngine (objectSize = 48 bytes)
            field = "cache"
          }
        }
      }
    }
  }
  allocationStackTrace = [
    com.example.service.RuleCache.addRule(RuleCache.java:87)
    com.example.service.RuleEngine.processMessage(RuleEngine.java:134)
    com.example.consumer.KafkaHandler.onMessage(KafkaHandler.java:56)
    ...
  ]
}
```

### 3.3 分析要点

从 OldObjectSample 可以得到三个关键信息：

| 信息 | 含义 | 本例值 |
|------|------|--------|
| **objectAge** | 对象在 Old Gen 中存活的时间 | 26 小时 — 应该被回收但未回收 |
| **referrer 链** | 谁在持有这个对象 | RuleEngine → RuleCache → ConcurrentHashMap |
| **allocationStackTrace** | 对象在哪里分配的 | RuleCache.addRule() |

> 结论：RuleCache 中的 ConcurrentHashMap 持续增长，对象只进不出。

GC 事件中也可以看到 Full GC 后 Old Gen 回收极少：`Before: 3.4G → After: 3.38G (回收仅 20MB)`，进一步印证泄漏。

---

## 4. 第二步：NMT 分析

NMT (Native Memory Tracking) 用于分析 JVM 进程的完整内存使用情况，包括堆外内存。

### 4.1 建立基线

在服务启动初期 (例如启动后 10 分钟) 建立内存基线：

```bash
jcmd <pid> VM.native_memory baseline
```

### 4.2 对比差异

运行一段时间后 (例如 24 小时后)，查看内存变化：

```bash
jcmd <pid> VM.native_memory detail.diff
```

输出示意 (示意数据)：

```
Native Memory Tracking:
Total: reserved=7654MB +1245MB, committed=6234MB +1102MB

-          Java Heap (reserved=4096MB, committed=4096MB)
-              Class (reserved=1156MB +24MB, committed=132MB +24MB)
                     (classes #18562 +3200)                          # ← 异常
-             Thread (reserved=245MB +45MB, committed=245MB +45MB)
                     (thread #243 +45)
-               Code (reserved=256MB +12MB, committed=68MB +12MB)
-                 GC (reserved=210MB, committed=182MB)
-           Internal (reserved=423MB +112MB, committed=423MB +112MB) # ← 异常
-      Direct Buffer (reserved=256MB +180MB, committed=256MB +180MB) # ← 异常
```

### 4.3 NMT 输出解读

| 区域 | 增量 | 分析 |
|------|------|------|
| Java Heap | 0 (固定 4GB) | 堆大小固定，符合预期 |
| **Class** | **+24MB, classes +3200** | **异常：类数量持续增长，可能有 ClassLoader 泄漏** |
| Thread | +45MB, thread +45 | 线程数增长，需关注是否线程池泄漏 |
| **Internal** | **+112MB** | **异常：内部分配增长较大** |
| **Direct Buffer** | **+180MB** | **异常：堆外内存增长显著，可能是 DirectByteBuffer 泄漏** |

> 关键发现：除了 Java Heap 内的泄漏 (ConcurrentHashMap)，NMT 还揭示了 Class 区和 Direct Buffer 区的异常增长。这说明可能存在多个泄漏源。

---

## 5. 第三步：Heap Dump 分析

### 5.1 获取 Heap Dump

```bash
# 方式 1: 手动导出 (服务还活着时)
jmap -dump:live,format=b,file=/data/dumps/heap_72h.hprof <pid>

# 方式 2: 通过 jcmd (推荐，更安全)
jcmd <pid> GC.heap_dump /data/dumps/heap_72h.hprof

# 方式 3: 自动导出 (OOM 时自动触发，已通过启动参数配置)
# -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/data/dumps/
```

> **注意**: Heap Dump 会导致一次 Full GC 和短暂的 STW (Stop-The-World)，4GB 堆大约需要 10-30 秒。在生产环境中需要评估影响。

### 5.2 MAT (Eclipse Memory Analyzer) 分析

#### Dominator Tree 概览 (示意数据)

用 MAT 打开 .hprof 文件后，查看 Dominator Tree (支配树)：

```
Dominator Tree (按 Retained Heap 排序):

Rank  Class                                    Shallow Heap    Retained Heap    Percentage
----  -----                                    ------------    -------------    ----------
1     com.example.service.RuleCache            32 B            1,245 MB         31.1%
2     io.netty.buffer.PooledByteBufAllocator   128 B           623 MB           15.6%
3     com.example.loader.PluginClassLoader[]   512 B           412 MB           10.3%
4     java.lang.Thread[]                       1,024 B         234 MB           5.9%
5     java.util.concurrent.ConcurrentHashMap   64 B            198 MB           5.0%
...
```

#### Leak Suspects 报告 (示意数据)

MAT 的 Leak Suspects 自动报告识别出三个嫌疑：

| Suspect | 描述 | 占比 |
|---------|------|------|
| 1 | `RuleCache` 中 `ConcurrentHashMap` 占 1,245 MB | 31.1% |
| 2 | 38 个 `PluginClassLoader` 实例占 412 MB | 10.3% |
| 3 | `PooledByteBufAllocator` 持有 256 MB direct buffers | 6.4% |

---

## 6. 根因分析

综合 JFR、NMT、Heap Dump 的分析结果，本案例存在三个独立的泄漏源。

### Case A: ConcurrentHashMap 缓存无 eviction (主要泄漏源)

**现象**: RuleCache 中的 ConcurrentHashMap 持续增长，占堆内存 31%。

**根因代码** (示意)：

```java
public class RuleCache {
    // 问题：只有 put 没有 remove，没有 TTL/LRU 机制
    private final ConcurrentHashMap<String, RuleDefinition> ruleMap = new ConcurrentHashMap<>();

    public void addRule(String ruleId, RuleDefinition rule) {
        ruleMap.put(ruleId, rule);  // 每条消息都可能产生新规则
    }

    public RuleDefinition getRule(String ruleId) {
        return ruleMap.get(ruleId);
    }
    // 没有 removeRule, 没有 size 限制, 没有 TTL
}
```

**诊断要点**:
- OldObjectSample 中 objectAge 长达数十小时
- Dominator Tree 中 ConcurrentHashMap 的 Retained Heap 最大
- `ruleMap.size()` 从启动时数百增长到数十万

### Case B: ClassLoader 泄漏

**现象**: NMT 显示 Class 区域增长 +24MB，类数量增加 3200 个。

**根因代码** (示意)：

```java
public class PluginManager {
    private final List<PluginClassLoader> loaders = new ArrayList<>();

    public void loadPlugin(String jarPath) {
        // 问题：每次热加载创建新 ClassLoader，旧的不释放
        PluginClassLoader loader = new PluginClassLoader(new URL[]{new File(jarPath).toURL()});
        loaders.add(loader);  // 旧 loader 永远留在 list 中

        Class<?> pluginClass = loader.loadClass("com.example.Plugin");
        // ... 使用 plugin
    }
}
```

**诊断要点**:
- NMT 中 Class 区域持续增长
- MAT 中存在大量 PluginClassLoader 实例
- 每个 ClassLoader 持有的类无法被卸载 (因为 ClassLoader 本身未被 GC)

### Case C: DirectByteBuffer 泄漏 (Netty)

**现象**: NMT 显示 Direct Buffer 增长 +180MB。

**根因代码** (示意)：

```java
public class MessageHandler extends ChannelInboundHandlerAdapter {
    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) {
        ByteBuf buf = (ByteBuf) msg;
        try {
            // 处理消息
            processMessage(buf);
        } catch (Exception e) {
            log.error("处理失败", e);
            // 问题：异常路径未 release ByteBuf
            return;  // 缺少 buf.release()
        }
        buf.release();
    }
}
```

**诊断要点**:
- NMT 中 Direct Buffer 区域持续增长
- Netty 的 ResourceLeakDetector 日志 (需开启 `-Dio.netty.leakDetection.level=PARANOID`)
- MAT 中 PooledByteBufAllocator 的 Retained Heap 异常

---

## 7. 修复方案

### Case A 修复：引入 Caffeine 缓存替代裸 ConcurrentHashMap

```java
import com.github.benmanes.caffeine.cache.Cache;
import com.github.benmanes.caffeine.cache.Caffeine;

public class RuleCache {
    // 修复：使用 Caffeine 缓存，设置最大条目数和 TTL
    private final Cache<String, RuleDefinition> ruleMap = Caffeine.newBuilder()
            .maximumSize(10_000)                       // 最多缓存 1 万条规则
            .expireAfterAccess(Duration.ofHours(2))    // 2 小时未访问则过期
            .recordStats()                             // 开启统计，方便监控
            .removalListener((key, value, cause) ->
                log.info("Rule evicted: key={}, cause={}", key, cause))
            .build();

    public void addRule(String ruleId, RuleDefinition rule) {
        ruleMap.put(ruleId, rule);
    }

    public RuleDefinition getRule(String ruleId) {
        return ruleMap.getIfPresent(ruleId);
    }
}
```

### Case B 修复：ClassLoader 生命周期管理

```java
public class PluginManager {
    private volatile PluginClassLoader currentLoader;

    public void loadPlugin(String jarPath) throws Exception {
        // 修复：关闭并释放旧的 ClassLoader
        PluginClassLoader oldLoader = currentLoader;

        PluginClassLoader newLoader = new PluginClassLoader(
            new URL[]{new File(jarPath).toURL()});
        Class<?> pluginClass = newLoader.loadClass("com.example.Plugin");
        // ... 初始化 plugin

        currentLoader = newLoader;

        if (oldLoader != null) {
            oldLoader.close();  // 关闭旧 ClassLoader，允许 GC 回收
        }
    }
}
```

### Case C 修复：确保 ByteBuf 在所有路径释放

```java
public class MessageHandler extends ChannelInboundHandlerAdapter {
    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) {
        ByteBuf buf = (ByteBuf) msg;
        try {
            processMessage(buf);
        } catch (Exception e) {
            log.error("处理失败", e);
        } finally {
            // 修复：在 finally 中确保释放
            buf.release();
        }
    }
}
```

> 也可使用 `ReferenceCountUtil.release(msg)` 替代 `buf.release()`，语义更清晰。

---

## 8. 验证与回归

### 修复前后内存对比 (示意数据)

```
# 修复后堆内存使用趋势 (示意数据)
时间点          Used Heap    Old Gen     RuleCache Size    Direct Buffer
启动后 1h       1.1 GB       0.7 GB      2,345             64 MB
启动后 24h      1.2 GB       0.8 GB      10,000 (达到上限)  64 MB
启动后 72h      1.2 GB       0.8 GB      10,000            64 MB
启动后 7d       1.2 GB       0.8 GB      10,000            65 MB
```

### 验证要点

1. **堆内存稳定**: Old Gen 稳定在 ~0.8 GB，72 小时内 Full GC 次数为 0
2. **缓存命中率**: Caffeine 统计显示命中率 > 95%
3. **Class/Direct Buffer 稳定**: NMT diff 显示类数量和堆外内存不再增长

---

## 9. 经验总结

### 排查流程

```
OOM 发生
  │
  ├─→ 1. 检查 JFR (OldObjectSample)
  │      → 识别 Old Gen 中存活最久的对象
  │      → 查看引用链和分配栈
  │
  ├─→ 2. 检查 NMT (VM.native_memory diff)
  │      → 对比堆外内存各区域增长
  │      → 识别 Class/Direct Buffer/Thread 区域异常
  │
  ├─→ 3. 分析 Heap Dump (MAT)
  │      → Dominator Tree: 谁占内存最多
  │      → Leak Suspects: 自动分析泄漏嫌疑
  │      → OQL: 精确查询特定对象
  │
  └─→ 4. 定位根因 → 修复 → 验证
```

### 常见内存泄漏模式

| 模式 | 典型场景 | 检测方法 |
|------|----------|----------|
| **无界缓存** | Map 只 put 不 remove | JFR OldObjectSample + MAT Dominator Tree |
| **ClassLoader 泄漏** | 动态创建 ClassLoader 不关闭 | NMT Class 区域增长 + MAT ClassLoader 实例计数 |
| **堆外内存泄漏** | DirectByteBuffer / Netty ByteBuf 未释放 | NMT Direct Buffer 增长 + `-Dio.netty.leakDetection.level` |
| **监听器累积** | 注册事件监听器不移除 | MAT 查看 listener list size |
| **线程泄漏** | 创建线程不终止 | NMT Thread 区域增长 + jstack 线程数 |
| **ThreadLocal 泄漏** | 线程池中 ThreadLocal 未 remove | MAT 查看 Thread.threadLocals |

### 关键命令速查

```bash
# JFR 操作
jcmd <pid> JFR.start name=leak duration=60m filename=/tmp/leak.jfr
jcmd <pid> JFR.dump name=leak filename=/tmp/leak_dump.jfr
jcmd <pid> JFR.stop name=leak
jfr print --events jdk.OldObjectSample /tmp/leak.jfr

# NMT 操作
jcmd <pid> VM.native_memory baseline
jcmd <pid> VM.native_memory detail.diff
jcmd <pid> VM.native_memory summary.diff

# Heap Dump
jcmd <pid> GC.heap_dump /tmp/heap.hprof
jmap -dump:live,format=b,file=/tmp/heap.hprof <pid>

# 线程分析
jcmd <pid> Thread.print
jstack <pid> > /tmp/threads.txt
```

---

## 相关资源

- [JFR 实战指南](../guides/jfr.md) - JFR 详细使用方法和事件类型
- [GC 演进](../by-topic/core/gc/) - G1/ZGC/Shenandoah 各版本特性对比
- [内存管理](../by-topic/core/memory/) - 堆/栈/Metaspace/紧凑对象头
- [案例索引](README.md) - 更多实战案例
