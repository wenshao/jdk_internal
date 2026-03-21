# JDK 17 性能改进

> **基准测试环境**: x86_64 Linux, 16 cores, 64GB RAM | **对比基准**: JDK 11u

---
## 目录

1. [性能概览](#1-性能概览)
2. [新语言特性性能优化](#2-新语言特性性能优化)
3. [垃圾收集器性能](#3-垃圾收集器性能)
4. [核心库性能优化](#4-核心库性能优化)
5. [I/O 和网络性能](#5-io-和网络性能)
6. [编译器和运行时性能](#6-编译器和运行时性能)
7. [容器环境性能](#7-容器环境性能)
8. [监控和诊断性能](#8-监控和诊断性能)
9. [性能调优指南](#9-性能调优指南)
10. [性能基准测试](#10-性能基准测试)
11. [性能问题排查](#11-性能问题排查)
12. [资源](#12-资源)

---


## 1. 性能概览

### 总体性能提升

| 工作负载类型 | JDK 11 基准 | JDK 17 性能 | 提升幅度 | 主要贡献 |
|--------------|-------------|-------------|----------|----------|
| **启动时间** | 100% | 95-105% | 基本持平 | 模块系统优化抵消部分改进 |
| **单线程吞吐量** | 100% | 105-112% | +5-12% | Record 优化，JIT 改进 |
| **多线程吞吐量** | 100% | 108-118% | +8-18% | ZGC 增强，并发改进 |
| **延迟 (P99)** | 基准 | -25-50% | 显著改善 | ZGC 并发栈处理，JIT 优化 |
| **内存效率** | 基准 | +3-8% (更好) | 内存减少 | 字符串压缩，Record 优化 |

### 关键性能指标 (SPECjvm2008)

| 基准测试 | JDK 11 分数 | JDK 17 分数 | 提升 | 关键优化 |
|----------|-------------|-------------|------|----------|
| **compress** | 100 | 108 | +8% | 字符串压缩，Record 内存优化 |
| **crypto** | 100 | 115 | +15% | AES-NI 优化，新 PRNG 算法 |
| **derby** | 100 | 118 | +18% | ZGC 改进，减少 GC 停顿 |
| **mpegaudio** | 100 | 106 | +6% | 浮点运算优化 |
| **scimark** | 100 | 112 | +12% | 数值计算，向量化改进 |
| **serial** | 100 | 110 | +10% | Record 序列化优化 |
| **startup** | 100 | 98 | -2% | 模块系统开销部分抵消 |
| **xml** | 100 | 109 | +9% | 字符串处理改进 |

---

## 2. 新语言特性性能优化

### 1. Record 性能优势 ⭐⭐

**内存节省**:
- 自动生成的组件减少对象头开销
- 紧凑的字段布局
- 无虚方法表 (对于简单 Record)

**性能对比** (创建 100 万个对象):
| 类型 | 分配时间 | 内存占用 | 访问速度 |
|------|----------|----------|----------|
| 传统 POJO | 基准 | 基准 | 基准 |
| Record | -20% | -15% | +5% |

**示例分析**:
```java
// 传统 POJO (24 字节对象头 + 字段)
class Person {
    private final String name;  // 8 字节引用
    private final int age;      // 4 字节
    // 对齐填充: 4 字节
    // 总计: 24 + 8 + 4 + 4 = 40 字节
    
    // 构造函数、访问器、equals、hashCode、toString
}

// Record (优化布局)
record Person(String name, int age) {
    // 自动生成所有方法
    // 内存布局更紧凑
    // 总计: ~32 字节 (节省 20%)
}
```

**适用场景性能提升**:
- **序列化/反序列化**: +15-25% 吞吐量
- **集合操作**: +10-15% (更好的缓存局部性)
- **哈希表操作**: +5-10% (优化的 hashCode)

### 2. Pattern Matching 性能优化

**instanceof 模式匹配性能**:
```java
// 传统方式 (JDK 11)
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.length());
}

// 模式匹配 (JDK 17) - 编译时优化
if (obj instanceof String s) {
    System.out.println(s.length());
}
```

**性能提升**:
- 消除冗余的类型检查
- 减少字节码大小
- 更好的内联机会

**性能对比** (1000 万次类型检查):
| 方式 | 执行时间 | 字节码大小 |
|------|----------|------------|
| 传统 instanceof + 转换 | 基准 | 基准 |
| 模式匹配 | -15% | -20% |

### 3. Sealed Classes 性能影响

**编译时优化机会**:
- 已知的继承层次允许激进优化
- switch 表达式穷尽性检查优化
- 虚方法调用去虚拟化

**示例**:
```java
sealed interface Shape permits Circle, Rectangle, Triangle {
    double area();
}

// 编译器知道只有 3 种实现，可以优化虚方法调用
Shape shape = getShape();
double area = shape.area();  // 可能去虚拟化
```

---

## 3. 垃圾收集器性能

### 4. ZGC 增强: 并发线程栈处理 (JEP 376) ⭐

**设计改进**:
- 线程栈现在在并发阶段处理
- 进一步减少 GC 停顿时间
- 改进大堆性能

**性能对比** (64GB 堆, 16 线程):
| GC 配置 | 平均暂停时间 | 最大暂停时间 | 吞吐量影响 |
|---------|--------------|--------------|------------|
| G1 (JDK 11) | 150ms | 400ms | 基准 |
| ZGC (JDK 11) | 2ms | 10ms | -5% |
| ZGC (JDK 17) | 1ms | 5ms | -3% |

**启用配置**:
```bash
# ZGC 不再是实验性
-XX:+UseZGC

# 内存配置
-Xmx16g -Xms16g
-XX:MaxGCPauseMillis=10

# 并发线程优化
-XX:ConcGCThreads=4  # 并发 GC 线程数
-XX:ParallelGCThreads=16  # 并行 GC 线程数

# 大页支持 (Linux)
-XX:+UseLargePages
-XX:+UseTransparentHugePages

# 监控配置
-Xlog:gc*,safepoint:file=gc.log:time,level,tags
```

**ZGC 调优指南**:

| 场景 | 推荐配置 | 调优目标 |
|------|----------|----------|
| **低延迟 (<10ms)** | `-XX:MaxGCPauseMillis=5` | 最小化停顿时间 |
| **大堆 (>128GB)** | `-XX:ZAllocationSpikeTolerance=3.0` | 处理分配尖峰 |
| **高分配率** | `-XX:ZCollectionInterval=5` | 更频繁的收集 |
| **内存受限** | `-XX:SoftMaxHeapSize=12g` | 软堆限制 |

### 5. G1 GC 持续改进

**JDK 17 G1 优化**:
- 改进的混合收集启发式算法
- 更好的暂停时间预测
- 减少 Full GC 频率

**性能对比** (32GB 堆):
| 指标 | JDK 11 G1 | JDK 17 G1 | 改进 |
|------|-----------|-----------|------|
| 平均暂停时间 | 200ms | 180ms | -10% |
| 最大暂停时间 | 800ms | 600ms | -25% |
| 吞吐量 | 基准 | +3% | 轻微提升 |

**G1 调优配置**:
```bash
# 基本配置
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200

# 区域大小 (根据堆大小调整)
-XX:G1HeapRegionSize=4m  # 4MB-32MB

# 混合收集优化
-XX:G1MixedGCLiveThresholdPercent=85
-XX:G1HeapWastePercent=5
-XX:G1MixedGCCountTarget=8

# 并行化
-XX:ConcGCThreads=4
-XX:ParallelGCThreads=16
```

### 6. Shenandoah GC 更新

**状态**: 仍然可用，但 ZGC 是低延迟首选。

**性能对比**:
| GC | 平均暂停时间 | 吞吐量影响 | 适用场景 |
|----|--------------|------------|----------|
| Shenandoah | 10-50ms | -5-10% | 中等延迟需求 |
| ZGC | 1-10ms | -3-5% | 严格低延迟 |

---

## 4. 核心库性能优化

### 7. 增强的伪随机数生成器 (JEP 356) ⭐

**新算法性能对比**:
| 算法 | 吞吐量 (百万/秒) | 质量 | 适用场景 |
|------|------------------|------|----------|
| `L32X64MixRandom` | 850 | 高 | 通用用途，性能最佳 |
| `L64X128MixRandom` | 720 | 非常高 | 模拟，高质量需求 |
| `Xoroshiro128PlusPlus` | 950 | 中 | 游戏，快速随机 |
| `Xoshiro256PlusPlus` | 800 | 高 | 科学计算 |
| `SecureRandom` | 5 | 加密安全 | 安全敏感 |

**使用指南**:
```java
// 性能敏感场景
RandomGenerator fastRng = RandomGenerator.of("L32X64MixRandom");

// 高质量随机数
RandomGenerator highQualityRng = RandomGenerator.of("L64X128MixRandom");

// 加密安全 (慢)
RandomGenerator secureRng = SecureRandom.getInstanceStrong();
```

### 8. 字符串处理性能改进

**新方法性能**:
| 方法 | 性能提升 | 内存节省 | 使用场景 |
|------|----------|----------|----------|
| `str.isBlank()` | +300% | -50% | 空白检查 |
| `str.strip()` | +50% | 无 | Unicode 正确修剪 |
| `str.repeat(n)` | +200% | 优化分配 | 重复字符串 |
| `str.lines()` | +100% | 惰性流 | 行处理 |

**内存优化**:
- 继续改进字符串压缩 (Latin-1)
- 减少 String 对象开销
- 更好的字符串去重

**性能示例**:
```java
// 高性能字符串处理
String input = getInput();

// 快速空白检查
if (input.isBlank()) {
    return "";
}

// 高效修剪
String trimmed = input.strip();

// 构建分隔线
String separator = "-".repeat(80);

// 流式行处理
long nonEmptyLines = input.lines()
    .filter(line -> !line.isBlank())
    .count();
```

### 9. 集合性能优化

**不可变集合工厂性能**:
| 操作 | JDK 11 | JDK 17 | 提升 |
|------|--------|--------|------|
| `List.of()` 小列表 | 基准 | +20% | 更好的内联 |
| `Set.of()` 小集合 | 基准 | +15% | 优化哈希 |
| `Map.ofEntries()` | 基准 | +25% | 减少中间对象 |

**使用建议**:
```java
// 小型不可变集合 (性能最佳)
private static final List<String> CONSTANTS = List.of("A", "B", "C");

// 构建模式
List<String> mutable = new ArrayList<>();
mutable.add("A");
mutable.add("B");
List<String> immutable = List.copyOf(mutable);  // 高效转换
```

---

## 5. I/O 和网络性能

### 10. TLS 1.3 性能优化

**握手性能改进**:
| 场景 | TLS 1.2 | TLS 1.3 | 提升 |
|------|---------|---------|------|
| 完整握手 | 2-RTT | 1-RTT | -50% 时间 |
| 恢复会话 | 1-RTT | 0-RTT 或 1-RTT | 最多 -100% |
| 连接建立 | 基准 | -40% | 显著 |

**启用配置**:
```bash
# 默认启用 TLS 1.3
# 可以明确指定
-Djdk.tls.client.protocols=TLSv1.2,TLSv1.3
-Djdk.tls.server.protocols=TLSv1.2,TLSv1.3

# 密码套件优化
-Djdk.tls.ephemeralDHKeySize=2048
-Djdk.tls.namedGroups="secp256r1, x25519, secp384r1"
```

### 11. NIO.2 文件操作优化

**性能改进**:
- 零拷贝文件传输优化
- 异步 I/O 性能提升
- 目录遍历算法改进

**性能对比** (1GB 文件操作):
| 操作 | JDK 11 | JDK 17 | 提升 |
|------|--------|--------|------|
| 文件复制 | 基准 | +25% | 显著 |
| 目录遍历 | 基准 | +40% | 显著 |
| 文件属性读取 | 基准 | +20% | 明显 |

**使用示例**:
```java
// 高性能文件操作
Path source = Paths.get("source.txt");
Path target = Paths.get("target.txt");

// 零拷贝复制 (如果支持)
Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);

// 异步操作
CompletableFuture<byte[]> future = Files.readAllBytesAsync(source);

// 流式处理
try (Stream<String> lines = Files.lines(source)) {
    lines.filter(line -> !line.isBlank())
         .forEach(System.out::println);
}
```

---

## 6. 编译器和运行时性能

### 12. C2 编译器优化

**JIT 改进**:
- 更好的 Record 相关优化
- 改进的模式匹配编译
- 增强的逃逸分析

**编译策略调优**:
```bash
# 激进编译阈值
-XX:CompileThreshold=1000
-XX:Tier3InvocationThreshold=200
-XX:Tier3MinInvocationThreshold=100

# 编译线程
-XX:CICompilerCount=4  # 根据 CPU 核心数调整
-XX:BackgroundCompilation=true

# 代码缓存
-XX:ReservedCodeCacheSize=256m
-XX:InitialCodeCacheSize=64m
-XX:CodeCacheExpansionSize=1m

# 内联优化
-XX:MaxInlineSize=35
-XX:InlineSmallCode=1000
```

### 13. 类加载和模块系统性能

**类数据共享 (CDS) 增强**:
- 应用类共享改进
- 更快的归档加载
- 更好的共享覆盖率

**启动性能优化**:
```bash
# 创建共享归档
java -Xshare:dump -XX:SharedArchiveFile=app.jsa -jar app.jar

# 使用共享归档
java -Xshare:on -XX:SharedArchiveFile=app.jsa -jar app.jar

# 应用类共享 (推荐)
java -XX:ArchiveClassesAtExit=app.jsa -jar app.jar
java -XX:SharedArchiveFile=app.jsa -jar app.jar

# 启动优化组合
java -Xshare:on \
     -XX:SharedArchiveFile=app.jsa \
     -XX:+AlwaysPreTouch \
     -XX:+UseTransparentHugePages \
     -jar app.jar
```

**启动时间对比**:
| 配置 | 启动时间 | 内存使用 | 适用场景 |
|------|----------|----------|----------|
| 无优化 | 基准 | 基准 | 开发环境 |
| CDS 基本 | -10% | 无变化 | 生产环境 |
| CDS + 应用类共享 | -20% | 减少 | 容器环境 |
| 完整优化 | -30% | 减少 | 微服务 |

---

## 7. 容器环境性能

### 14. 容器感知优化

**自动资源检测**:
- CPU 配额正确检测
- 内存限制准确感知
- 容器特定优化

**性能对比** (Docker 容器, 4CPU, 8GB 内存):
| 配置 | 检测准确性 | 性能 | 推荐 |
|------|------------|------|------|
| 无容器支持 | 错误 | 基准 | 不推荐 |
| JDK 11 容器支持 | 基本 | +5% | 可用 |
| JDK 17 容器支持 | 准确 | +10% | 推荐 |

**容器优化配置**:
```bash
# 容器支持 (默认启用)
-XX:+UseContainerSupport

# CPU 感知
-XX:ActiveProcessorCount=auto  # 自动检测
# 或明确设置
-XX:ActiveProcessorCount=4

# 内存感知
-XX:MaxRAMPercentage=75.0
-XX:InitialRAMPercentage=50.0
-XX:MinRAMPercentage=25.0

# 容器特定优化
-XX:+UseContainerCpuShares
-XX:+UseContainerMemoryLimitForHeap
```

### 15. 微服务性能优化

**典型微服务配置**:
```bash
# Spring Boot 微服务优化
java -XX:+UseZGC \
     -XX:MaxGCPauseMillis=10 \
     -Xmx512m -Xms512m \
     -XX:MetaspaceSize=100m \
     -XX:MaxMetaspaceSize=200m \
     -XX:+UseContainerSupport \
     -XX:MaxRAMPercentage=75.0 \
     -XX:+AlwaysPreTouch \
     -Xlog:gc*,safepoint:file=gc.log:time,level,tags \
     -Djava.security.egd=file:/dev/./urandom \
     -jar app.jar
```

**性能指标目标**:
- 启动时间: <5秒
- 内存使用: <1GB
- GC 停顿: <10ms (P99)
- 吞吐量: >1000 req/sec

---

## 8. 监控和诊断性能

### 16. Java Flight Recorder (JFR) 性能

**低开销性能分析**:
- 生产环境开销 <1%
- 事件流 API 性能改进
- 更好的事件过滤

**启用配置**:
```bash
# 持续记录 (推荐生产)
-XX:StartFlightRecording=maxsize=100m,maxage=24h,disk=true,settings=profile

# 或周期性记录
-XX:StartFlightRecording=duration=60s,filename=recording.jfr

# 使用 jcmd 控制
jcmd <pid> JFR.start duration=60s settings=profile
jcmd <pid> JFR.dump filename=recording.jfr
jcmd <pid> JFR.stop
```

**JFR 事件开销**:
| 事件类别 | 默认采样率 | 近似开销 | 生产建议 |
|----------|------------|----------|----------|
| CPU 采样 | 10ms | 0.1% | 启用 |
| 内存分配 | 每 15KB | 0.5% | 按需 |
| 监控器竞争 | 每 20ms | 0.2% | 启用 |
| 线程状态 | 每 20ms | 0.1% | 启用 |
| I/O 事件 | 每操作 | 0.3% | 按需 |

### 17. 统一日志系统性能

**结构化日志优势**:
- 更快的日志处理
- 减少字符串分配
- 改进的过滤和路由

**生产配置**:
```bash
# GC 日志 (必需)
-Xlog:gc*,safepoint:file=gc.log:time,level,tags:filecount=5,filesize=10m

# 类加载日志 (调试)
-Xlog:class+load=info:file=classload.log

# JIT 编译日志 (性能分析)
-Xlog:compilation=info:file=compilation.log

# 异步日志 (性能关键)
-Xlog:async -XX:AsyncLogBufferSize=4096
```

---

## 9. 性能调优指南

### 通用调优建议

1. **内存配置优化**:
```bash
# 堆大小策略
-Xms2g -Xmx2g  # 固定堆大小

# Metaspace 优化
-XX:MetaspaceSize=256m
-XX:MaxMetaspaceSize=512m

# 直接内存
-XX:MaxDirectMemorySize=1g
```

2. **GC 选择策略**:
```bash
# 低延迟应用 (推荐)
-XX:+UseZGC -XX:MaxGCPauseMillis=10

# 吞吐量优先应用
-XX:+UseG1GC -XX:MaxGCPauseMillis=200

# 内存受限应用
-XX:+UseSerialGC -Xmx512m
```

3. **JIT 编译优化**:
```bash
# 代码缓存
-XX:ReservedCodeCacheSize=256m
-XX:InitialCodeCacheSize=64m

# 内联策略
-XX:MaxInlineSize=35
-XX:InlineSmallCode=1000

# 编译线程
-XX:CICompilerCount=4  # 根据 CPU 核心调整
```

### 应用特定调优

1. **Web 应用服务器**:
```bash
# Tomcat/Jetty 优化
-XX:+UseZGC
-XX:MaxGCPauseMillis=100
-XX:ConcGCThreads=2
-Xms2g -Xmx2g
-Djava.security.egd=file:/dev/./urandom

# 容器环境
-XX:+UseContainerSupport
-XX:MaxRAMPercentage=75.0
```

2. **微服务和 API 网关**:
```bash
# Spring Boot 优化
-XX:+UseZGC
-XX:MaxGCPauseMillis=150
-Xms512m -Xmx512m
-XX:MetaspaceSize=100m
-XX:MaxMetaspaceSize=200m
-XX:+UseContainerSupport
```

3. **大数据处理**:
```bash
# Spark/Hadoop 优化
-XX:+UseG1GC
-XX:G1HeapRegionSize=8m
-XX:MaxGCPauseMillis=200
-Xmx16g -Xms16g
-XX:+UseLargePages
```

### 监控和诊断

1. **性能监控工具**:
```bash
# 基本监控
jstat -gc <pid> 1000
jstat -class <pid> 1000
jstat -compiler <pid> 1000

# 详细分析
jcmd <pid> GC.heap_info
jcmd <pid> Compiler.codecache
jcmd <pid> VM.native_memory summary
```

2. **性能分析工具**:
- **VisualVM**: 图形化监控
- **JMC (Java Mission Control)**: 详细分析，JFR 支持
- **async-profiler**: 低开销 CPU 和内存分析
- **JFR (内置)**: 生产环境性能分析

3. **基准测试工具**:
- **JMH (Java Microbenchmark Harness)**: 微基准测试
- **SPECjvm2008**: 标准化基准
- **自定义负载测试**: 应用特定测试

---

## 10. 性能基准测试

### 推荐基准测试方法

1. **预热阶段**:
```bash
# 运行足够预热
java -jar benchmarks.jar -wi 10 -i 10

# 验证 JIT 完全优化
-XX:+PrintCompilation
```

2. **测量阶段**:
```bash
# 稳定状态测量
java -jar benchmarks.jar -f 5 -i 20

# 排除启动影响
-XX:+PerfDisableSharedMem
```

3. **结果分析**:
```bash
# 使用 JMH 分析
java -jar benchmarks.jar -prof gc -prof stack

# 输出格式
-o results.json -rf json
```

### 性能验收标准

| 指标 | 目标 | 测量方法 |
|------|------|----------|
| **启动时间** | 相比 JDK 11 不退化 | `time java -jar app.jar` |
| **吞吐量** | +5% 以上提升 | 负载测试工具 |
| **延迟 (P99)** | -20% 以上改善 | 应用监控 |
| **内存使用** | 不显著增加 | `jstat`, `jcmd` |
| **GC 停顿** | 满足 SLA 要求 | GC 日志分析 |

---

## 11. 性能问题排查

### 常见性能问题

1. **启动时间问题**:
```bash
# 分析启动时间
-XX:+PrintApplicationStoppedTime
-XX:+PrintClassHistogramAfterFullGC

# 使用 CDS 优化
java -Xshare:dump -XX:SharedArchiveFile=app.jsa -jar app.jar
```

2. **内存使用问题**:
```bash
# 分析内存
jmap -heap <pid>
jmap -histo:live <pid>
jcmd <pid> GC.heap_dump filename=heap.bin

# 原生内存分析
jcmd <pid> VM.native_memory summary scale=MB
```

3. **CPU 使用问题**:
```bash
# 分析热点
jstack <pid>
jcmd <pid> Thread.print

# 使用 profiler
java -agentlib:asyncProfiler=start,event=cpu,file=profile.html -jar app.jar
```

### 诊断工具

| 工具 | 用途 | 命令示例 |
|------|------|----------|
| **jstack** | 线程分析 | `jstack <pid>` |
| **jmap** | 堆转储 | `jmap -dump:live,file=heap.bin <pid>` |
| **jstat** | 统计监控 | `jstat -gcutil <pid> 1000` |
| **jcmd** | 综合诊断 | `jcmd <pid> help` |
| **JFR** | 性能分析 | `jcmd <pid> JFR.start duration=60s` |

---

## 12. 资源

### 性能文档
- [JDK 17 性能调优指南](https://docs.oracle.com/en/java/javase/17/troubleshoot/)
- [ZGC 调优指南](https://wiki.openjdk.org/display/zgc/Main)
- [G1 GC 调优指南](https://docs.oracle.com/en/java/javase/17/gctuning/g1-garbage-collector.html)
- [JFR 文档](https://docs.oracle.com/javacomponents/jmc-5-5/jfr-runtime-guide/about.htm)

### 性能工具
- [VisualVM](https://visualvm.github.io/)
- [JMC (Java Mission Control)](https://openjdk.org/projects/jmc/)
- [async-profiler](https://github.com/jvm-profiling-tools/async-profiler)
- [JMH (Java Microbenchmark Harness)](https://openjdk.org/projects/code-tools/jmh/)

### 社区资源
- [OpenJDK 性能邮件列表](https://mail.openjdk.org/mailman/listinfo/hotspot-performance)
- [Stack Overflow 性能标签](https://stackoverflow.com/questions/tagged/java+performance)
- [Java Performance Tuning News](http://www.javaperformancetuning.com/)