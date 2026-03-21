# JDK 21 相比 JDK 17 的新特性

> **对比版本**: JDK 17u (LTS 2021) → JDK 21u (LTS 2023) | **时间跨度**: 2 年 | **变革性版本**: ⭐⭐⭐

---
## 目录

1. [革命性特性: Virtual Threads (JEP 444) ⭐⭐⭐](#1-革命性特性-virtual-threads-jep-444-)
2. [语言特性增强](#2-语言特性增强)
3. [预览特性](#3-预览特性)
4. [性能与垃圾收集](#4-性能与垃圾收集)
5. [API 增强](#5-api-增强)
6. [弃用和移除](#6-弃用和移除)
7. [性能基准测试](#7-性能基准测试)
8. [迁移建议](#8-迁移建议)
9. [工具和生态系统](#9-工具和生态系统)
10. [资源](#10-资源)
11. [总结](#11-总结)

---


## 1. 革命性特性: Virtual Threads (JEP 444) ⭐⭐⭐

### 什么是 Virtual Threads？

**传统线程 (Platform Threads) 的限制**:
- 1:1 映射到操作系统线程
- 创建成本高 (~1MB 栈内存)
- 上下文切换由操作系统管理
- 数量受限 (通常几百到几千)

**Virtual Threads 的优势**:
- JVM 管理的轻量级线程
- 创建成本极低 (~几百字节)
- 挂起/恢复由 JVM 管理
- 数量可达数百万

### 性能对比

| 指标 | Platform Threads | Virtual Threads | 改进倍数 |
|------|-----------------|-----------------|----------|
| **线程创建时间** | ~1ms | ~1μs | **1000x** |
| **内存占用** | ~1MB/线程 | ~200-300字节/线程 | **3000x** |
| **最大并发数** | 1000-5000 | 1,000,000+ | **200x** |
| **上下文切换** | 操作系统成本高 | JVM 管理成本低 | **10x** |

### 使用示例

```java
// 1. 基本创建
Thread virtualThread = Thread.ofVirtual()
    .name("virtual-thread-", 1)
    .start(() -> {
        System.out.println("Running in virtual thread");
    });

// 2. 虚拟线程执行器 (推荐)
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    Future<String> future = executor.submit(() -> {
        Thread.sleep(Duration.ofSeconds(1));  // 不会阻塞载体线程
        return "Result";
    });
    
    String result = future.get();
}

// 3. 结构化并发 (预览, JEP 453)
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> user = scope.fork(() -> fetchUser());
    Future<String> profile = scope.fork(() -> fetchProfile());
    
    scope.join();           // 等待所有任务
    scope.throwIfFailed();  // 如果有失败则抛出异常
    
    return new Response(user.resultNow(), profile.resultNow());
}
```

### 迁移指南

**适用场景**:
- ✅ **高并发 I/O 操作**: HTTP 请求, 数据库查询, 文件读写
- ✅ **网络服务**: Web 服务器, API 网关, 微服务
- ✅ **异步任务处理**: 消息队列消费者, 批处理任务
- ⚠️ **计算密集型任务**: 无性能优势，可能略差
- ❌ **本地代码调用 (JNI)**: 需要兼容性检查

**代码迁移示例**:
```java
// JDK 17: 传统线程池
ExecutorService executor = Executors.newFixedThreadPool(200);

// JDK 21: 虚拟线程执行器
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();

// 或兼容性迁移
ExecutorService executor = ThreadPoolBuilder
    .virtualThreadExecutor()
    .setThreadFactory(Thread.ofVirtual().factory())
    .setCorePoolSize(10)  // 载体线程数
    .setMaximumPoolSize(200)
    .build();
```

### 常见问题解决

1. **线程被固定 (Pinned Threads)**:
```bash
# 诊断固定问题
-Djdk.traceVirtualThreads=true
-Djdk.traceVirtualThreadLocals=true

# 日志中会显示 "Pinned" 警告
```

**解决方案**:
- 避免在 `synchronized` 块内进行 I/O
- 使用 `ReentrantLock` 替代 `synchronized`
- 减少 `ThreadLocal` 使用，考虑 `ScopedValue`

2. **内存泄漏**:
```java
// 确保正确关闭执行器
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    // 使用 executor
}  // 自动关闭，释放所有线程
```

---

## 2. 语言特性增强

### 1. Record Patterns 正式版 (JEP 440) ⭐

**功能**: Record 的解构模式匹配

```java
record Point(int x, int y) {}
record Rectangle(Point topLeft, Point bottomRight) {}

// 基本解构
static void printPoint(Object obj) {
    if (obj instanceof Point(int x, int y)) {
        System.out.printf("Point at (%d, %d)%n", x, y);
    }
}

// 嵌套解构
static void printRectangle(Object obj) {
    if (obj instanceof Rectangle(Point(var x1, var y1), Point(var x2, var y2))) {
        System.out.printf("Rectangle from (%d,%d) to (%d,%d)%n", x1, y1, x2, y2);
    }
}

// switch 表达式
static String describe(Object obj) {
    return switch (obj) {
        case Point(int x, int y) -> String.format("Point(%d, %d)", x, y);
        case Rectangle(Point tl, Point br) -> "Rectangle";
        case null -> "null";
        default -> "Unknown";
    };
}
```

**性能优势**: 编译时优化，减少运行时类型检查。

### 2. Pattern Matching for switch 正式版 (JEP 441) ⭐

**状态变化**: JDK 17 预览 → JDK 21 正式

```java
// 正式使用，无需预览标志
static String formatter(Object obj) {
    return switch (obj) {
        case Integer i -> String.format("int %d", i);
        case Long l    -> String.format("long %d", l);
        case Double d  -> String.format("double %f", d);
        case String s  -> String.format("String %s", s);
        case null      -> "null";
        default        -> obj.toString();
    };
}

// 守卫表达式
static void checkString(Object obj) {
    switch (obj) {
        case String s when s.length() > 100 -> 
            System.out.println("Very long string");
        case String s when s.length() > 10 -> 
            System.out.println("Long string");
        case String s -> 
            System.out.println("Short string");
        default -> 
            System.out.println("Not a string");
    }
}

// 穷尽性检查 (与密封类结合)
sealed interface Shape permits Circle, Rectangle, Triangle {
    double area();
}

static String describeShape(Shape shape) {
    return switch (shape) {
        case Circle c    -> "Circle with radius " + c.radius();
        case Rectangle r -> "Rectangle " + r.width() + "x" + r.height();
        case Triangle t  -> "Triangle";
        // 不需要 default，编译器知道所有情况已覆盖
    };
}
```

### 3. Sequenced Collections (JEP 431) ⭐

**新接口层次**:
```
Collection
    ↓
SequencedCollection (新增)
    ↓
List, Deque, SequencedSet (新增)
    ↓
ArrayList, LinkedList, LinkedHashSet
```

**新增方法**:
```java
interface SequencedCollection<E> extends Collection<E> {
    // 新增方法
    SequencedCollection<E> reversed();
    void addFirst(E e);
    void addLast(E e);
    E getFirst();
    E getLast();
    E removeFirst();
    E removeLast();
}

interface SequencedSet<E> extends Set<E>, SequencedCollection<E> {
    SequencedSet<E> reversed();  // 协变返回类型
}

interface SequencedMap<K, V> extends Map<K, V> {
    SequencedMap<K, V> reversed();
    void putFirst(K key, V value);
    void putLast(K key, V value);
    Entry<K, V> firstEntry();
    Entry<K, V> lastEntry();
    Entry<K, V> pollFirstEntry();
    Entry<K, V> pollLastEntry();
}
```

**使用示例**:
```java
// List 示例
SequencedCollection<String> list = new ArrayList<>();
list.add("b");
list.addFirst("a");    // ["a", "b"]
list.addLast("c");     // ["a", "b", "c"]
String first = list.getFirst();  // "a"
String last = list.getLast();    // "c"

// 反向视图 (不复制)
SequencedCollection<String> reversed = list.reversed();  // ["c", "b", "a"]

// Map 示例
SequencedMap<String, Integer> map = new LinkedHashMap<>();
map.put("b", 2);
map.putFirst("a", 1);    // {a=1, b=2}
map.putLast("c", 3);     // {a=1, b=2, c=3}
Map.Entry<String, Integer> firstEntry = map.firstEntry();  // a=1
```

**迁移收益**: 统一的首尾元素访问API，减少特定集合类的依赖。

---

## 3. 预览特性

### 4. String Templates (JEP 430) 🔍

**目标**: 类型安全的字符串插值

```java
// STR 模板处理器 (内置)
String name = "Alice";
int age = 30;
String message = STR."Hello, \{name}. You are \{age} years old.";
// 结果: "Hello, Alice. You are 30 years old."

// FMT 模板处理器 (格式化)
String formatted = FMT."Value: %05d\{42}";  // "Value: 00042"

// RAW 模板处理器 (原始模板)
StringTemplate st = RAW."Hello, \{name}";
String result = STR.process(st);  // 显式处理

// 自定义模板处理器
StringTemplate.Processor<String, RuntimeException> JSON = 
    StringTemplate.Processor.of(
        (StringTemplate template) -> {
            List<Object> values = template.values();
            // 生成 JSON
            return "{\"name\": \"" + values.get(0) + "\"}";
        }
    );

String json = JSON."""
    {
        "name": "\{name}",
        "age": \{age}
    }
    """;
```

**安全优势**: 避免注入攻击，编译时检查。

### 5. Scoped Values (JEP 446) 🔍

**目标**: 替代 `ThreadLocal` 在 Virtual Threads 场景的使用

```java
private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();

// 设置作用域值
ScopedValue.where(CURRENT_USER, user).run(() -> {
    // 在此作用域内可访问 CURRENT_USER
    processRequest();
});

// 嵌套作用域
ScopedValue.where(CURRENT_USER, user1).run(() -> {
    // user1 可见
    ScopedValue.where(CURRENT_USER, user2).run(() -> {
        // user2 可见 (遮蔽 user1)
    });
    // user1 再次可见
});

// 多个作用域值
ScopedValue.where(CURRENT_USER, user)
           .where(REQUEST_ID, requestId)
           .run(() -> {
               // 两个值都可见
           });
```

**与 ThreadLocal 对比**:
| 特性 | ThreadLocal | ScopedValue |
|------|-------------|-------------|
| 继承性 | 可继承 | 不可继承 |
| Virtual Threads 支持 | 性能差 | 优化支持 |
| 内存泄漏风险 | 高 | 低 |
| 作用域控制 | 弱 | 强 |

### 6. Structured Concurrency (JEP 453) 🔍

**目标**: 简化并发任务的生命周期管理

```java
// 结构化任务域
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> userFuture = scope.fork(() -> fetchUser());
    Future<List<Order>> ordersFuture = scope.fork(() -> fetchOrders());
    
    scope.join();           // 等待所有任务完成
    scope.throwIfFailed();  // 如果有失败则抛出异常
    
    // 所有任务成功完成
    return new Response(userFuture.resultNow(), ordersFuture.resultNow());
}  // 自动关闭，取消未完成的任务

// 处理失败
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> future1 = scope.fork(() -> task1());
    Future<String> future2 = scope.fork(() -> task2());
    
    scope.join();
    
    if (future1.state() == Future.State.SUCCESS) {
        return future1.resultNow();
    } else if (future2.state() == Future.State.SUCCESS) {
        return future2.resultNow();
    } else {
        throw new RuntimeException("All tasks failed");
    }
}
```

**优势**: 避免任务泄漏，简化错误处理，改进可观测性。

### 7. Unnamed Patterns and Variables (JEP 443) 🔍

**目标**: 使用 `_` 表示不需要的变量

```java
// 未命名变量
var _ = computeValue();  // 忽略返回值
try {
    // 忽略异常
} catch (IOException _) {
    System.out.println("IO error occurred");
}

// 未命名模式
if (obj instanceof Point(int x, _)) {
    System.out.println("x = " + x);  // 只关心 x
}

// 增强 for 循环
int count = 0;
for (var _ : items) {
    count++;  // 只计数，不关心元素
}

// try-with-resources
try (var _ = acquireResource()) {
    // 使用资源，但不需要引用
}
```

**优势**: 提高代码可读性，明确表示忽略意图。

### 8. Unnamed Classes and Instance Main Methods (JEP 445) 🔍

**目标**: 简化 Java 入门体验

```java
// Hello.java - 最简形式
void main() {
    println("Hello, World!");
}

// 等同于传统写法
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}

// 带参数
void main(String[] args) {
    println("Hello, " + args[0]);
}

// 使用静态导入
import static java.lang.System.*;
void main() {
    out.println("Hello");  // 可以直接使用 out
}
```

**教育价值**: 降低 Java 学习曲线。

---

## 4. 性能与垃圾收集

### 9. Generational ZGC (JEP 439) ⭐⭐

**重大改进**: ZGC 引入分代收集

**性能数据**:
| 场景 | 非分代 ZGC | 分代 ZGC | 改进 |
|------|------------|----------|------|
| **吞吐量下降** | 5-10% | < 5% | **+50%** |
| **GC 频率** | 基准 | -50% | **-50%** |
| **内存占用** | 基准 | -20% | **-20%** |
| **最大停顿时间** | < 1ms | < 1ms | 持平 |

**启用配置**:
```bash
# 启用分代 ZGC
-XX:+UseZGC -XX:+ZGenerational

# 调优参数
-XX:ZAllocationSpikeTolerance=2.0
-XX:ZCollectionInterval=5
-XX:ZUncommitDelay=300

# 监控
-Xlog:gc*,gc+heap*,gc+stats*:file=gc.log:time,level,tags
```

**适用场景推荐**:
- ✅ **大堆应用** (>32GB): 显著收益
- ✅ **高分配率应用**: 减少GC频率
- ✅ **低延迟要求**: 保持亚毫秒停顿
- ⚠️ **小堆应用** (<4GB): 收益有限

### 10. Shenandoah GC 更新

**分代 Shenandoah** (实验性):
```bash
# 启用分代 Shenandoah
-XX:+UseShenandoahGC -XX:+ShenandoahGenerational
```

**性能对比**:
| GC | 平均停顿时间 | 吞吐量影响 | 内存开销 |
|----|--------------|------------|----------|
| G1 | 100-200ms | 基准 | 基准 |
| ZGC (非分代) | 1-2ms | -5% | 低 |
| ZGC (分代) | 1-2ms | -3% | 更低 |
| Shenandoah | 10-50ms | -10% | 中 |

---

## 5. API 增强

### 11. Key Encapsulation Mechanism API (JEP 452)

**新安全 API**: 标准的密钥封装机制

```java
// 发送方
KEM kemS = KEM.getInstance("DHKEM");
KEM.Encapsulator encS = kemS.newEncapsulator(senderPrivateKey);
KEM.Encapsulated encapsulated = encS.encapsulate();
byte[] ciphertext = encapsulated.encapsulation();
byte[] key = encapsulated.key();

// 接收方  
KEM kemR = KEM.getInstance("DHKEM");
KEM.Decapsulator decR = kemR.newDecapsulator(receiverPrivateKey);
byte[] decryptedKey = decR.decapsulate(ciphertext);
```

**支持的算法**: DHKEM, RSA-KEM, ECIES-KEM。

### 12. 准备禁止动态加载代理 (JEP 451)

**安全增强**: 默认禁止动态加载 Java 代理

**影响**:
- `-javaagent` 命令行参数仍然可用
- 运行时动态加载 (`VirtualMachine.loadAgent`) 默认禁止
- 可通过系统属性启用: `-Djdk.instrument.traceUsage`

**迁移**:
```bash
# JDK 21 之前: 允许动态加载
# JDK 21 默认: 禁止动态加载

# 如果需要动态加载
-Djdk.instrument.traceUsage
# 或明确允许
-Djdk.instrument.allowDynamicLoading=true
```

---

## 6. 弃用和移除

### 13. 废弃 Windows 32位 x86 端口 (JEP 449)

**影响**: Windows 32位版本标记为废弃，计划未来移除

**建议**:
- 32位应用迁移到 64位
- 更新本地库 (JNI) 到 64位
- 测试 64位环境兼容性

### 14. Vector API 第六轮孵化 (JEP 448)

**状态**: 继续孵化，API 可能变化

```java
// SIMD 向量计算
static final VectorSpecies<Float> SPECIES = FloatVector.SPECIES_PREFERRED;

void vectorComputation(float[] a, float[] b, float[] c) {
    int i = 0;
    int upperBound = SPECIES.loopBound(a.length);
    for (; i < upperBound; i += SPECIES.length()) {
        FloatVector va = FloatVector.fromArray(SPECIES, a, i);
        FloatVector vb = FloatVector.fromArray(SPECIES, b, i);
        FloatVector vc = va.mul(va).add(vb.mul(vb)).neg();
        vc.intoArray(c, i);
    }
    // 标量处理剩余元素
    for (; i < a.length; i++) {
        c[i] = (a[i] * a[i] + b[i] * b[i]) * -1.0f;
    }
}
```

**性能提升**: 特定场景下 4-8 倍加速。

---

## 7. 性能基准测试

### 宏观性能对比

| 工作负载类型 | JDK 17 基准 | JDK 21 性能 | 提升幅度 | 主要贡献 |
|--------------|-------------|-------------|----------|----------|
| **I/O 密集型** | 100% | 200-500% | 2-5x | Virtual Threads |
| **微服务吞吐量** | 100% | 150-300% | 1.5-3x | Virtual Threads + 分代 ZGC |
| **启动时间** | 100% | 95-105% | 基本持平 | 优化抵消 |
| **内存使用** | 基准 | -10-20% | 减少 | 分代 ZGC |
| **延迟 (P99)** | 基准 | -30-50% | 显著改善 | Virtual Threads + 分代 ZGC |

### 微基准测试 (JMH)

**Virtual Threads 性能**:
```java
@State(Scope.Benchmark)
public class VirtualThreadsBenchmark {
    
    @Benchmark
    @BenchmarkMode(Mode.Throughput)
    public void platformThreads() throws Exception {
        try (var executor = Executors.newFixedThreadPool(200)) {
            List<Future<?>> futures = new ArrayList<>();
            for (int i = 0; i < 10_000; i++) {
                futures.add(executor.submit(() -> {
                    LockSupport.parkNanos(1_000_000);  // 1ms 模拟 I/O
                }));
            }
            for (Future<?> future : futures) {
                future.get();
            }
        }
    }
    
    @Benchmark
    @BenchmarkMode(Mode.Throughput) 
    public void virtualThreads() throws Exception {
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            List<Future<?>> futures = new ArrayList<>();
            for (int i = 0; i < 10_000; i++) {
                futures.add(executor.submit(() -> {
                    LockSupport.parkNanos(1_000_000);  // 1ms 模拟 I/O
                }));
            }
            for (Future<?> future : futures) {
                future.get();
            }
        }
    }
}
```

**预期结果**: Virtual Threads 吞吐量高 3-10 倍，内存使用少 90%+。

---

## 8. 迁移建议

### 优先级矩阵

| 特性 | 采用优先级 | 影响范围 | 建议时间 |
|------|------------|----------|----------|
| **Virtual Threads** | 最高 | 高 (架构级) | 立即评估，2-4 周试点 |
| **分代 ZGC** | 高 | 中 (性能) | 下个发布周期 |
| **Record Patterns** | 中 | 低 (代码质量) | 逐步采用 |
| **Sequenced Collections** | 中 | 低 (API 改进) | 代码审查时更新 |
| **预览特性** | 低 | 低 (实验性) | 评估，不用于生产 |

### 分阶段迁移策略

**阶段 1: 评估和试点** (1-2 个月)
- Virtual Threads 适用性分析
- 性能基准测试
- 小规模试点项目

**阶段 2: 基础设施升级** (1 个月)
- 构建环境更新
- CI/CD 流水线升级
- 监控系统增强

**阶段 3: 应用迁移** (2-4 个月)
- 非关键路径应用先行
- 逐步启用 Virtual Threads
- 性能监控和调优

**阶段 4: 全面采用** (持续)
- 新项目直接使用 JDK 21
- 旧项目逐步迁移
- 最佳实践总结和推广

### 风险控制

**技术风险**:
- Virtual Threads 兼容性问题
- 第三方库支持程度
- 性能回归风险

**缓解措施**:
- 充分测试，特别是并发测试
- 建立回滚计划
- 分阶段灰度发布

**组织风险**:
- 团队技能更新需求
- 工具链适配
- 运维监控变更

**缓解措施**:
- 培训和技术分享
- 文档和工具支持
- 监控告警体系建设

---

## 9. 工具和生态系统

### 构建工具支持

| 工具 | 最小版本 | 关键特性 |
|------|----------|----------|
| **Maven** | 3.6.3+ | `maven.compiler.release=21` |
| **Gradle** | 8.0+ | JavaToolchain 支持 JDK 21 |
| **Spring Boot** | 3.2.0+ | Virtual Threads 自动配置 |
| **Micronaut** | 4.0.0+ | 原生支持 Virtual Threads |
| **Quarkus** | 3.0.0+ | 预览特性支持 |

### IDE 支持

| IDE | 最小版本 | Virtual Threads 调试 |
|-----|----------|---------------------|
| **IntelliJ IDEA** | 2023.2+ | 完整支持 |
| **Eclipse** | 2023-09+ | 基本支持 |
| **VS Code** | 1.80+ | 通过扩展支持 |
| **NetBeans** | 19+ | 有限支持 |

### 监控和诊断

**新增 JFR 事件**:
- `jdk.VirtualThreadStart`
- `jdk.VirtualThreadEnd`
- `jdk.VirtualThreadPinned`
- `jdk.VirtualThreadSubmitFailed`

**监控命令**:
```bash
# 查看 Virtual Threads 统计
jcmd <pid> Thread.dump_to_file -format=json threads.json

# 监控线程状态
jcmd <pid> VM.native_memory summary | grep -A5 "Virtual Thread"

# JFR 记录
jcmd <pid> JFR.start duration=60s filename=recording.jfr settings=profile
```

---

## 10. 资源

### 学习资源
- [Virtual Threads 深度指南](https://openjdk.org/jeps/444)
- [JDK 21 新特性教程](https://docs.oracle.com/en/java/javase/21/)
- [迁移案例研究](https://inside.java/tag/jdk21/)

### 工具资源
- [Virtual Threads 性能分析工具](https://github.com/openjdk/jmc)
- [迁移检查工具](https://github.com/openjdk/jdk/tree/master/src/jdk.jdeps)
- [兼容性测试套件](https://github.com/openjdk/jdk/tree/master/test)

### 社区支持
- [OpenJDK loom-dev 邮件列表](https://mail.openjdk.org/mailman/listinfo/loom-dev)
- [Stack Overflow: virtual-threads](https://stackoverflow.com/questions/tagged/virtual-threads)
- [Java User Groups](https://community.oracle.com/community/developer/)

---

## 11. 总结

JDK 21 是 Java 历史上最具变革性的版本之一，**Virtual Threads** 重新定义了 Java 并发编程模型，为高并发应用带来数量级的性能提升。结合**分代 ZGC**、**Record Patterns** 等特性，JDK 21 为现代云原生应用提供了强大的基础。

**立即行动建议**:
1. **评估 Virtual Threads 对现有架构的影响**
2. **建立 JDK 21 测试环境**
3. **从非关键应用开始试点**
4. **培训团队掌握新特性和最佳实践**
5. **规划全面的迁移路线图**

JDK 21 不仅是技术升级，更是架构演进的机会，值得投入资源充分评估和采用。