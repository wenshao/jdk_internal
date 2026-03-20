# 编译阈值机制

> 为什么方法要执行 10000 次才被 C2 编译？

[← 返回 JIT 编译](../)

---

## 结论先行

| 问题 | 答案 |
|------|------|
| **为什么需要阈值？** | 编译有成本，只编译"热点"代码才划算 |
| **默认阈值是多少？** | C2: 10000 次，C1 Level 3: 约 3000 次 |
| **如何调整？** | `-XX:CompileThreshold` |
| **阈值越低越好？** | ❌ 编译太多代码反而降低性能 |

---

## 一眼看懂

### 编译阈值的作用

```
JIT 编译成本:
├── 编译时间: 10-100ms (取决于方法大小)
├── 内存占用: 编译后的代码需要空间
└── 优化时间: 深度优化需要更多时间

只有执行足够多次的方法才值得编译:
├── 执行 1 次 → 解释执行最快
├── 执行 100 次 → 解释还是更快
├── 执行 1000 次 → C1 编译值得
└── 执行 10000 次 → C2 深度优化值得
```

### 分层编译阈值

```
Level 0: 解释执行
    ↓
Level 1: C1 (简单编译) - ~100 次调用
    ↓
Level 2: C1 (有限 profiling) - ~500 次调用
    ↓
Level 3: C1 (完全 profiling) - ~3000 次调用
    ↓
Level 4: C2 (深度优化) - ~10000 次调用
```

---

## 阈值详解

### 默认阈值

| 层级 | 名称 | 默认阈值 | 说明 |
|------|------|----------|------|
| **Level 1** | C1 简单 | 100 | 快速编译，启动优化 |
| **Level 2** | C1 有限 | 500 | 开始 profiling |
| **Level 3** | C1 完全 | 3000 | 收集完整 profiling |
| **Level 4** | C2 | 10000 | 深度优化 |

### 相关参数

```bash
# 主阈值
-XX:CompileThreshold=10000         # C2 编译阈值
-XX:FreqInlineSize=325             # 热方法内联阈值

# 分层编译特定
-XX:Tier0InvokeNotifyFreq=100      # Level 0 → 1
-XX:Tier3InvokeNotifyFreq=3000     # Level 3 → 4
-XX:Tier23InlineeNotifyFreq=50     # 内联后触发
-XX:Tier0BackedgeNotifyFreq=1242   # 循环回边频率

# 调整阈值
-XX:CompileThreshold=5000          # 更早编译 C2
-XX:CompileThreshold=20000         # 更晚编译 C2
```

---

## 为什么是 10000？

### 经验值

```
10000 次的由来:
├── 经验: 大多数应用的热点方法会调用这么多次
├── 平衡: 编译成本 vs 运行收益
├── 启动: 避免启动时编译太多代码
└── 内存: 限制代码缓存大小

历史:
├── 早期 JDK: 固定 1500 次 (不分层)
├── JDK 6+: 引入分层编译
├── JDK 7+: 默认启用分层
└── 现在: 10000 是经过验证的默认值
```

### 成本收益分析

```java
// 假设:
// 编译成本: 10ms
// 解释执行: 100ns/次
// 编译后执行: 10ns/次

// 不编译 (10000 次解释):
// 总时间 = 10000 × 100ns = 1,000,000ns = 1ms

// 编译后执行:
// 编译 = 10ms + 10000 × 10ns = 10ms + 0.1ms = 10.1ms

// 结论: 如果只执行 10000 次，不值得编译！

// 但如果执行 100000 次:
// 不编译 = 100000 × 100ns = 10ms
// 编译后 = 10ms + 100000 × 10ns = 10ms + 1ms = 11ms

// 开始划算的临界点: 约 11000 次
```

---

## 分层切换条件

### 层级提升

```
Level 0 → Level 1:
├── 方法调用 ≥ Tier0InvokeNotifyFreq (100)
└── 循环回边 ≥ Tier0BackedgeNotifyFreq (1242)

Level 1 → Level 2:
├── 解释器 profiling 满足条件
└── 方法调用 ≥ Tier0InvokeNotifyFreq × 2

Level 2 → Level 3:
├── C1 编译完成
└── 收集足够的 profiling

Level 3 → Level 4 (C2):
├── 方法调用 ≥ Tier3InvokeNotifyFreq (3000)
└── profiling 数据足够
```

### 层级降级

```
去优化触发:
├── Level 4 → Level 3: 假设失效
├── Level 3 → Level 0: 重新收集数据
└── 完全重新开始: 严重问题
```

---

## 阈值调优

### 何时调整阈值

| 场景 | 建议 |
|------|------|
| **短时应用** | 降低阈值，快速编译 |
| **长时应用** | 保持默认 |
| **内存受限** | 提高阈值，减少编译 |
| **预热敏感** | 降低阈值 |

### 调优示例

```bash
# 快速启动 (牺牲峰值性能)
-XX:CompileThreshold=1000
-XX:TieredStopAtLevel=1

# 长时运行 (优化峰值性能)
-XX:CompileThreshold=10000
-XX:TieredStopAtLevel=4

# 内存受限 (减少编译)
-XX:CompileThreshold=20000
-XX:ReservedCodeCacheSize=128m

# 微基准测试 (立即编译)
-XX:CompileThreshold=100
-Dgraal.CompileThreshold=100
```

### 调优风险

```
阈值过低:
├── 编译太多冷方法
├── 代码缓存溢出
├── 编译时间增加
└── 可能降低性能

阈值过高:
├── 热点延迟编译
├── 错过优化机会
└── 性能无法达到峰值
```

---

## 特殊情况

### 1. 循环热点

```java
// 方法只调用 1 次，但循环执行 10000 次
public void run() {
    for (int i = 0; i < 100000; i++) {
        process();  // 这个循环会被编译
    }
}

// 编译器使用 "回边计数器" (OSR)
// 循环达到阈值也会触发编译
```

### 2. OSR (On-Stack Replacement)

```bash
# OSR 相关参数
-XX:OnStackReplacePercentage=140    # OSR 阈值百分比
-XX:InterpreterProfilePercentage=33  # 解释器 profiling 比例

# OSR 只编译循环，不重新进入方法
```

### 3. 内联方法

```java
// 被内联的方法继承调用者的热度
// 不需要独立达到阈值

@HotSpotIntrinsicCandidate
public static int abs(int a) {
    return (a < 0) ? -a : a;  // 总是被内联
}
```

### 4. Trampoline 陷阱

```java
// 通过反射调用
Method m = clazz.getMethod("method");
m.invoke(obj);  // 热度不会累积到 method

// 解决: 使用 MethodHandle
MethodHandle mh = lookup.findVirtual(...);
mh.invokeExact(obj);  // 热度正常累积
```

---

## 监控阈值

### 查看编译活动

```bash
# 查看编译日志
-XX:+PrintCompilation

# 输出格式:
# 123   45   java.lang.String::charAt (8 bytes)
# │     │    │
# │     │    └─ 方法名
# │     └─ 编译 ID
# └─ 编译序号

# 查看达到阈值的方法
-XX:+PrintCompilation
-XX:+PrintPreciseCPUTime
```

### 使用 JFR

```bash
# 记录编译事件
jfr record --name=jit \
    --jdk.Compilation*=true \
    duration=60s \
    filename=jit.jfr

# 分析
jfr print --events jdk.Compilation jit.jfr
```

### 使用 JMX

```java
// 监控编译器
MBeanServer server = ManagementFactory.getPlatformMBeanServer();
HotSpotDiagnosticMXBean diagnostics =
    ManagementFactory.getPlatformMXBean(HotSpotDiagnosticMXBean.class);

// 查看编译阈值
String value = diagnostics.getVMOption("CompileThreshold").getValue();
System.out.println("CompileThreshold: " + value);
```

---

## 实战案例分析

### 案例 1: 微基准测试

```java
@Benchmark
public void test() {
    // JMH 会自动处理预热
    // 确保方法被编译
}
```

**手动测试问题**:
```java
// ❌ 错误: 没有预热
public static void main(String[] args) {
    long start = System.nanoTime();
    for (int i = 0; i < 1000; i++) {
        method();  // 可能还没编译！
    }
    long time = System.nanoTime() - start;
}

// ✅ 正确: 预热后再测试
public static void main(String[] args) {
    // 预热
    for (int i = 0; i < 20000; i++) {
        method();  // 确保达到 C2 阈值
    }

    // 测试
    long start = System.nanoTime();
    for (int i = 0; i < 1000; i++) {
        method();  // 现在用的是编译代码
    }
    long time = System.nanoTime() - start;
}
```

### 案例 2: 启动优化

```bash
# 服务器应用 (长时运行)
java -server MyApp
# 使用默认阈值

# CLI 工具 (短时运行)
java -XX:CompileThreshold=500 \
     -XX:TieredStopAtLevel=1 \
     MyApp
# 降低阈值，快速获得优化代码
```

### 案例 3: 内存受限

```bash
# 容器环境 (内存限制)
java -XX:CompileThreshold=15000 \
     -XX:ReservedCodeCacheSize=64m \
     -XX:+UseCodeCacheFlushing \
     MyApp
# 提高阈值，减少编译活动
```

---

## 常见问题

### Q1: 为什么我的方法没被编译？

```bash
# 检查:
1. 方法调用次数是否达到阈值
2. 方法是否太大 (超过内联阈值)
3. 代码缓存是否满
4. 是否有异常阻止编译

# 诊断:
-XX:+PrintCompilation
-XX:+PrintInlining
-XX:+LogCompilation
```

### Q2: 如何强制编译？

```bash
# 使用 CompileCommand
-XX:CompileCommand=compile,*MyClass.myMethod

# 降低阈值
-XX:CompileThreshold=100

# 使用白盒测试 API
import jdk.internal.vm.annotation.DontInline;
import jdk.internal.vm.compiler.WhiteBox;
// ...
WhiteBox wb = WhiteBox.getWhiteBox();
wb.enqueueMethodForCompilation(method, CompLevel.FULL_OPTIMIZATION);
```

### Q3: C1 和 C2 阈值不同？

```
是的:
├── C1: 更低阈值 (100-3000)
│   └── 快速编译，基础优化
└── C2: 更高阈值 (10000)
    └── 深度优化，需要更多 profiling

分层编译的好处:
├── C1 快速提供基本优化
├── 收集 profiling 数据
└── C2 基于数据做深度优化
```

---

## 相关链接

### 本地文档

- [C2 优化阶段](c2-phases.md) - 编译流程
- [分层编译](tiered-compilation.md) - 分层详解
- [诊断工具](diagnostics.md) - 监控编译
- [最佳实践](best-practices.md) - 预热建议

### 外部资源

- [Tuning Garbage Collection and CompileThreshold](https://docs.oracle.com/en/java/javase/17/vm/jvm-tuning.html)
- [Tiered Compilation in HotSpot JVM](https://blogs.oracle.com/jonthecryptist/entry/tiered_compilation_in_hotspot)

---

**最后更新**: 2026-03-21
