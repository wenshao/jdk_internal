# 代码缓存管理

> JIT 编译的代码存在哪里？满了会怎样？

[← 返回 JIT 编译](../)

---

## 结论先行

| 问题 | 答案 |
|------|------|
| **代码缓存是什么？** | 存储 JIT 编译后本地代码的内存区域 |
| **默认大小？** | 240MB (分段管理) |
| **满了会怎样？** | 停止编译或清理冷代码 |
| **如何监控？** | `-XX:+PrintCodeCache` 或 JFR |

---

## 一眼看懂

### 代码缓存的作用

```
JIT 编译流程:
├── 字节码 → 编译器 → 本地代码
└── 本地代码 → 代码缓存 → CPU 执行

代码缓存特点:
├── 存储编译后的机器码
├── 分段管理 (不同代码类型)
├── 有限大小 (需管理)
└── 可清理 (回收冷代码)
```

### 代码缓存结构

```
CodeCache (总内存区域)
├── CodeHeap 'non-profiled nmethods' (非 profiling 方法)
│   ├── C1 编译的代码
│   └── C2 编译的代码 (大部分)
├── CodeHeap 'profiled nmethods' (profiling 方法)
│   └── C1 Level 3 编译的代码
├── CodeHeap 'non-nmethods' (非方法代码)
│   ├── Adapter blobs
│   ├── Handler blobs
│   └── 其他运行时 stub
└── CodeHeap 'inline cache' (内联缓存)
    └── 虚方法调用缓存
```

---

## 代码缓存详解

### CodeBlob 结构

```
CodeBlob (编译代码块):
├── Header (元数据)
│   ├── 类型信息
│   ├── 大小
│   ├── 编译级别
│   └── 起始地址
├── Relocation (重定位信息)
├── Exception Handler (异常处理)
├── Frame Size (栈帧大小)
└── Code (机器码)
    ├── 入口序列
    ├── 主体代码
    └── 退出序列
```

### CodeHeap 分段

| CodeHeap | 默认大小 | 内容 |
|----------|----------|------|
| **non-profiled** | ~120MB | C1/C2 编译的方法 |
| **profiled** | ~50MB | C1 profiling 方法 |
| **non-nmethods** | ~5MB | Adapter/Handler |
| **inline cache** | ~5MB | 内联缓存 |

### 查看代码缓存

```bash
# 查看代码缓存信息
-XX:+PrintCodeCache
-XX:+PrintCodeCacheOnCompilation

# 输出示例:
# CodeHeap 'non-profiled nmethods': size=122880Kb used=12345Kb max=122880Kb
# CodeHeap 'profiled nmethods': size=51200Kb used=5678Kb max=51200Kb
# CodeHeap 'non-nmethods': size=5120Kb used=890Kb max=5120Kb
```

---

## 代码缓存满时的行为

### 策略选择

```
代码缓存满时的行为取决于配置:

1. 不清理 (默认行为):
   └── -XX:-UseCodeCacheFlushing
   └── 停止编译，性能受影响

2. 清理冷代码:
   └── -XX:+UseCodeCacheFlushing (默认 JDK 8+)
   └── 清理最少使用的代码
   └── 继续编译新方法
```

### 清理策略

```java
// 清理条件 (当使用率 > 阈值):
-XX:CodeCacheFlushingMinimumFreeSpace=10M  // 最小保留空间

// 清理算法:
1. 扫描代码缓存
2. 找到最少使用的 CodeBlob
3. 检查是否在调用栈上
4. 如果不在 → 标记为僵尸 (zombie)
5. 下次 GC 时回收内存
```

### 警告和错误

```
使用率 > 80%:
└── "CodeCache is full. Compiler has been disabled."

使用率 > 95%:
└── "CodeHeap 'non-profiled nmethods' is full."

使用率 = 100%:
└── 编译器停止工作
└── 性能显著下降
```

---

## 代码缓存配置

### 大小设置

```bash
# 预留总大小
-XX:ReservedCodeCacheSize=256m

# 各 CodeHeap 大小
-XX:InitialCodeCacheSize=16m           # 初始大小
-XX:CodeCacheMinimumUseSpace=200k      # 最小保留

# 分段配置
-XX:NonProfiledCodeHeapSize=122m       # 非 profiling
-XX:ProfiledCodeHeapSize=51m           # profiling
-XX:NonNMethodCodeHeapSize=5m          # 非方法
-XX:SegmentedCodeCache                 # 启用分段 (JDK 9+)
```

### 清理配置

```bash
# 启用清理 (JDK 8+ 默认启用)
-XX:+UseCodeCacheFlushing

# 清理阈值
-XX:CodeCacheFlushingMinimumFreeSpace=10M

# 清理间隔
-XX:MinCodeCacheFlushingInterval=300   # 秒

# 禁用清理 (不推荐)
-XX:-UseCodeCacheFlushing
```

### 调优建议

| 场景 | 大小 | 清理 |
|------|------|------|
| **大型应用** | 512m | 启用 |
| **微服务** | 128m | 启用 |
| **容器** | 64m | 启用 |
| **长时运行** | 256m | 可选 |

---

## 监控代码缓存

### 1. JVM 参数

```bash
# 持续打印代码缓存状态
-XX:+PrintCodeCache
-XX:+PrintCodeCacheOnCompilation

# 示例输出:
# CodeCache 'Size': 245760Kb used=45678Kb used=45678Kb free=200082Kb
# bounds [0x00007f1234000000, 0x00007f1234000000, 0x00007f1240000000]
# total_blobs=1234 nmethods=890 adapters=234
```

### 2. JFR

```bash
# 记录代码缓存事件
jfr record --name=codecache \
    --jdk.CodeCache*=true \
    duration=60s \
    filename=codecache.jfr

# 分析
jfr print --events jdk.CodeCache* codecache.jfr

# 事件类型:
# - CodeCacheFull
# - CodeCacheConfiguration
# - CodeCacheStatistics
```

### 3. JMX

```java
// 监控代码缓存
import java.lang.management.*;

MemoryPoolMXBean codeCacheMB =
    ManagementFactory.getMemoryPoolMXBeans().stream()
        .filter(p -> p.getName().equals("CodeHeap 'non-profiled nmethods'"))
        .findFirst()
        .orElse(null);

if (codeCacheMB != null) {
    MemoryUsage usage = codeCacheMB.getUsage();
    System.out.println("Used: " + usage.getUsed() + " bytes");
    System.out.println("Max: " + usage.getMax() + " bytes");
    System.out.println("Usage%: " + (usage.getUsed() * 100 / usage.getMax()));
}
```

### 4. jstat

```bash
# 查看编译器统计
jstat -compiler <pid>

# 输出:
# CompileTime : 累计编译时间
# LastCompile : 最后编译时间
# LastType : 最后编译类型
# CodeCacheUsed : 代码缓存使用量
# CodeCacheCapacity : 代码缓存总容量
```

---

## 实战案例分析

### 案例 1: 代码缓存满

```
症状:
├── 应用性能突然下降
├── 日志显示 "CodeCache is full"
└── 新方法不再被编译

诊断:
-XX:+PrintCodeCache
# 显示 CodeCache 使用率 100%

解决方案:
1. 增加代码缓存大小
   -XX:ReservedCodeCacheSize=512m

2. 启用清理
   -XX:+UseCodeCacheFlushing

3. 重启应用 (临时方案)
```

### 案例 2: 容器环境优化

```bash
# Docker 容器内存限制
docker run -m 2g ...

# JVM 参数
java -XX:ReservedCodeCacheSize=128m \
     -XX:+UseCodeCacheFlushing \
     -XX:CodeCacheFlushingMinimumFreeSpace=5m \
     MyApp

# 原因:
├── 容器内存有限
├── 代码缓存需要适配
└── 清理策略更激进
```

### 案例 3: 监控告警

```java
// 代码缓存使用率告警
public class CodeCacheMonitor {
    private static final double ALERT_THRESHOLD = 0.9;

    public static void checkCodeCache() {
        for (MemoryPoolMXBean pool :
                ManagementFactory.getMemoryPoolMXBeans()) {
            if (pool.getName().contains("CodeCache")) {
                MemoryUsage usage = pool.getUsage();
                double usageRatio =
                    (double) usage.getUsed() / usage.getMax();

                if (usageRatio > ALERT_THRESHOLD) {
                    System.err.println(
                        "WARNING: CodeCache usage " +
                        (int)(usageRatio * 100) + "%");
                }
            }
        }
    }
}
```

---

## 代码缓存与性能

### 大小影响

```
代码缓存太小:
├── 频繁清理
├── 重新编译开销
└── 性能波动

代码缓存太大:
├── 内存浪费
├── GC 压力
└── 可能不必要

最佳实践:
├── 监控实际使用
├── 留 20-30% 余量
└── 根据应用调整
```

### 清理影响

```
清理冷代码:
├── 释放内存
├── 允许新编译
├── 重新编译开销 (如果再次调用)
└── 总体: 正面影响 > 负面影响

不清理:
├── 无重新编译
├── 但代码缓存满
└── 新代码无法编译
```

---

## 常见问题

### Q1: 如何知道代码缓存大小？

```bash
# 方法 1: JVM 日志
-XX:+PrintCodeCache

# 方法 2: jstat
jstat -compiler <pid>

# 方法 3: JMX
MemoryPoolMXBean pool = ...;
pool.getUsage().getMax();
```

### Q2: 代码缓存碎片化？

```
问题:
├── CodeBlob 分配/释放导致碎片
├── 无法分配大块连续内存
└── 浪费空间

解决:
├── 定期清理 (UseCodeCacheFlushing)
├── 合并空闲空间
└── 重启应用 (彻底解决)
```

### Q3: Native Library 代码？

```
JNI 代码不在代码缓存:
├── JNI native 方法
├── 系统库
└── 不占用代码缓存

但:
├── JNI stubs 在代码缓存
├── adapter 代码在代码缓存
└── 这些通常很小
```

---

## 相关链接

### 本地文档

- [C2 优化阶段](c2-phases.md) - 代码生成阶段
- [VM 参数](vm-parameters.md) - 代码缓存参数
- [诊断工具](diagnostics.md) - 监控方法
- [JIT 与 GC 协作](jit-gc-collaboration.md) - 代码缓存清理

### 外部资源

- [Code Cache Management in HotSpot](https://docs.oracle.com/en/java/javase/17/vm/code-cache-management.html)
- [Tuning Code Cache](https://blogs.oracle.com/sundararajan/entry/understanding_code_cache_flushing)

---

**最后更新**: 2026-03-21
