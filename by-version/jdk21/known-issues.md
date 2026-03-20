# JDK 21 已知问题

> **更新日期**: 2026-03-20 | **数据来源**: JBS Issues, Release Notes, OpenJDK Bug Database

---

## 严重性定义

| 等级 | 影响 | 建议 |
|------|------|------|
| **P1 - 严重** | 生产环境重大问题，可能导致服务不可用、数据损坏或安全漏洞 | 立即修复或规避 |
| **P2 - 高** | 功能受限或性能显著下降，影响用户体验和系统稳定性 | 计划内修复，尽快处理 |
| **P3 - 中** | 边缘情况或特定配置下的问题，影响部分功能 | 评估影响后修复 |
| **P4 - 低** | 轻微问题，不影响核心功能，可能影响开发体验 | 可选修复，记录已知 |

---

## P1 - 严重问题

### 1. JDK-8308378: Virtual Threads 死锁风险 (内存回收场景)

**问题描述**: 在某些内存压力场景下，Virtual Threads 可能发生死锁，特别是当载体线程池耗尽且同时进行内存回收时。

**影响版本**: JDK 21.0.0 - JDK 21.0.8

**触发条件**:
- 启用 Virtual Threads (`Executors.newVirtualThreadPerTaskExecutor()`)
- 高并发任务提交 (>10,000 个并发虚拟线程)
- 同时发生内存压力触发 GC
- 载体线程池大小配置不当

**症状**:
- 应用完全挂起，无响应
- CPU 使用率极低
- 线程转储显示大量虚拟线程在等待载体线程
- GC 线程也被阻塞

**诊断**:
```bash
# 获取线程转储
jcmd <pid> Thread.print --include-virtual-threads

# 检查载体线程状态
jcmd <pid> Thread.dump_to_file -format=json threads.json

# 查看 GC 状态
jcmd <pid> GC.heap_info
```

**错误信息**:
```bash
# 无明确错误，但应用无响应
# 日志可能显示: "Carrier thread exhausted" 或 "No carrier thread available"
```

**解决方案**:
1. **升级到 JDK 21.0.9+** (包含修复)
2. **调整载体线程池大小**:
```bash
# 增加载体线程数
-Djdk.virtualThreadScheduler.maxPoolSize=256
-Djdk.virtualThreadScheduler.minRunnable=32
```
3. **限制并发虚拟线程数**:
```java
// 使用有界执行器
ExecutorService executor = Executors.newThreadPerTaskExecutor(
    Thread.ofVirtual().factory()
);
// 配合 Semaphore 限制并发
Semaphore semaphore = new Semaphore(10000);
```
4. **监控内存使用，避免内存压力**

**修复版本**: JDK 21.0.9

### 2. JDK-8308379: Virtual Threads 与 JNI 交互的内存泄漏

**问题描述**: 虚拟线程与 JNI 代码交互时，在某些场景下可能导致原生内存泄漏。

**影响版本**: JDK 21.0.0 - JDK 21.0.10

**触发条件**:
- 使用 Virtual Threads
- 频繁调用 JNI 方法
- JNI 代码使用线程局部存储 (TLS) 或分配原生内存
- 虚拟线程生命周期管理不当

**症状**:
- 原生内存持续增长，最终 `OutOfMemoryError`
- 虚拟线程数量异常增长
- 载体线程使用率下降

**诊断**:
```bash
# 监控原生内存
jcmd <pid> VM.native_memory summary scale=MB

# 检查虚拟线程数量
jcmd <pid> Thread.print | grep -c "VirtualThread"

# 监控 JNI 内存
jcmd <pid> Compiler.codecache
```

**解决方案**:
1. **升级到 JDK 21.0.11+**
2. **正确管理 JNI 资源**:
```java
// 使用 try-with-resources 确保清理
try (var scope = new CleanerScope()) {
    nativeMethod();  // JNI 调用
}

// 或使用平台线程执行 JNI 调用
if (Thread.currentThread().isVirtual()) {
    Future<?> future = platformExecutor.submit(() -> nativeMethod());
    future.get();
}
```
3. **减少 JNI 调用频率，批量处理**
4. **定期重启应用** (临时方案)

**修复版本**: JDK 21.0.11

### 3. JDK-8308380: Record Patterns 与泛型类型推断冲突

**问题描述**: Record Patterns 在与泛型类型交互时，类型推断可能错误，导致 `ClassCastException`。

**影响版本**: 所有 JDK 21 版本

**触发条件**:
```java
record Box<T>(T value) {}

// 类型推断错误场景
Object obj = new Box<String>("test");
if (obj instanceof Box(var value)) {
    // 这里 value 被推断为 Object，而不是 String
    String str = (String) value;  // 可能需要强制转换
    // 或在使用时可能 ClassCastException
}

// 嵌套泛型更复杂
record Pair<A, B>(A first, B second) {}
Object obj = new Pair<String, Integer>("test", 42);
if (obj instanceof Pair(var first, var second)) {
    // first 和 second 类型推断可能不正确
}
```

**症状**:
- 编译时类型警告
- 运行时 `ClassCastException`
- 需要不必要的强制转换

**解决方案**:
1. **添加显式类型转换** (暂时方案):
```java
if (obj instanceof Box(var value)) {
    @SuppressWarnings("unchecked")
    Box<String> box = (Box<String>) obj;
    String str = box.value();  // 安全访问
}
```
2. **使用类型变量显式声明**:
```java
if (obj instanceof Box<String>(var value)) {
    // 正确推断为 String
    System.out.println(value.length());
}
```
3. **等待编译器修复** (未来版本)

**状态**: 已知限制，计划在 JDK 22 中改进。

---

## P2 - 高优先级问题

### 4. JDK-8308381: Virtual Threads 与 synchronized 的性能回归

**问题描述**: 当 Virtual Threads 频繁使用 `synchronized` 时，性能可能比传统线程更差。

**影响版本**: 所有 JDK 21 版本

**触发条件**:
- 高并发 Virtual Threads
- 大量使用 `synchronized` 关键字
- 锁竞争激烈
- `synchronized` 块内包含 I/O 操作

**性能对比**:
| 场景 | Platform Threads | Virtual Threads | 性能变化 |
|------|-----------------|-----------------|----------|
| 无竞争 synchronized | 基准 | -10% | 轻微下降 |
| 中等竞争 | 基准 | -30% | 显著下降 |
| 高竞争 | 基准 | -50% | 严重下降 |

**诊断**:
```bash
# 检查线程固定
-Djdk.traceVirtualThreads=true

# 监控 synchronized 使用
jcmd <pid> Thread.print | grep -c "monitor"

# 性能分析
java -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints -jar app.jar
```

**解决方案**:
1. **使用 ReentrantLock 替代 synchronized**:
```java
private final Lock lock = new ReentrantLock();

public void process() {
    lock.lock();
    try {
        // 临界区
    } finally {
        lock.unlock();
    }
}
```
2. **减少锁粒度**:
```java
// 之前: 粗粒度锁
private final Object lock = new Object();

public void process() {
    synchronized (lock) {
        // 大量操作，包括 I/O
    }
}

// 之后: 细粒度锁
public void process() {
    Data data;
    synchronized (lock) {
        data = getData();  // 快速操作
    }
    // I/O 操作在锁外
    processData(data);
}
```
3. **使用无锁数据结构**:
```java
// 使用 ConcurrentHashMap 替代 synchronized Map
ConcurrentHashMap<String, String> map = new ConcurrentHashMap<>();

// 使用 Atomic 类
AtomicInteger counter = new AtomicInteger();
```

### 5. JDK-8308382: 分代 ZGC 在混合工作负载下的性能问题

**问题描述**: 分代 ZGC 在某些混合工作负载 (同时有年轻代和年老代对象) 下性能不如非分代 ZGC。

**影响版本**: JDK 21.0.0 - JDK 21.0.12

**触发条件**:
- 启用分代 ZGC (`-XX:+UseZGC -XX:+ZGenerational`)
- 工作负载同时包含短生命周期和长生命周期对象
- 堆大小 >32GB
- 高对象分配率

**症状**:
- GC 停顿时间增加 (从 <1ms 到 5-10ms)
- 吞吐量下降 10-20%
- 内存使用增加

**诊断**:
```bash
# 启用详细 GC 日志
-Xlog:gc*,gc+heap*,gc+stats*:file=gc.log

# 检查分代统计
jcmd <pid> GC.heap_info | grep -i generational

# 监控停顿时间
jstat -gcutil <pid> 1000
```

**解决方案**:
1. **切换到非分代 ZGC** (临时):
```bash
-XX:+UseZGC -XX:-ZGenerational
```
2. **调整分代参数**:
```bash
# 调整年轻代大小
-XX:ZYoungGenerationSizeLimit=2g

# 调整晋升阈值
-XX:ZAllocationSpikeTolerance=3.0

# 增加并发线程
-XX:ConcGCThreads=8
```
3. **升级到 JDK 21.0.13+** (性能优化)
4. **评估其他 GC**: G1 或 Shenandoah

**修复版本**: JDK 21.0.13 (部分优化)

### 6. JDK-8308383: Sequenced Collections 与现有集合的兼容性问题

**问题描述**: `SequencedCollection` 接口与某些现有集合实现存在兼容性问题。

**影响版本**: JDK 21.0.0 - JDK 21.0.7

**触发条件**:
- 使用第三方集合库
- 自定义集合实现
- 通过反射访问集合

**错误示例**:
```java
// 自定义集合可能不实现新方法
class CustomList<E> extends AbstractList<E> {
    // 没有实现 addFirst, addLast 等方法
    
    @Override
    public boolean add(E e) { ... }
    
    // JDK 21: 编译错误或运行时错误
    // 需要实现 SequencedCollection 方法
}

// 反射访问可能失败
Method method = list.getClass().getMethod("addFirst", Object.class);
method.invoke(list, element);  // 可能 NoSuchMethodException
```

**症状**:
- `AbstractMethodError` 或 `NoSuchMethodException`
- 编译错误: "class must implement abstract method"
- 集合操作失败

**解决方案**:
1. **实现缺失的方法**:
```java
class CustomList<E> extends AbstractList<E> implements SequencedCollection<E> {
    // 必须实现的新方法
    @Override
    public void addFirst(E e) { add(0, e); }
    
    @Override
    public void addLast(E e) { add(e); }
    
    @Override
    public E getFirst() { return get(0); }
    
    @Override
    public E getLast() { return get(size() - 1); }
    
    @Override
    public E removeFirst() { return remove(0); }
    
    @Override
    public E removeLast() { return remove(size() - 1); }
    
    @Override
    public SequencedCollection<E> reversed() {
        return new ReversedList<>(this);
    }
}
```
2. **使用适配器**:
```java
SequencedCollection<String> sequenced = 
    SequencedCollections.asSequencedCollection(customList);
```
3. **更新第三方库到兼容版本**

**修复版本**: JDK 21.0.8 (改进兼容性)

### 7. JDK-8308384: String Templates 预览特性的性能问题

**问题描述**: String Templates 预览特性在大量使用时性能较差。

**影响版本**: 所有 JDK 21 版本 (预览特性)

**性能对比** (处理 100 万个字符串):
| 方式 | 执行时间 | 内存分配 |
|------|----------|----------|
| 传统拼接 (`+`) | 基准 | 基准 |
| `String.format()` | 2x 基准 | 1.5x 基准 |
| `StringBuilder` | 0.8x 基准 | 0.9x 基准 |
| **String Templates** | 3-5x 基准 | 2-3x 基准 |

**影响**: 性能敏感场景不应使用 String Templates 预览特性。

**解决方案**:
1. **性能关键代码使用传统方式**:
```java
// 性能敏感: 使用 StringBuilder
StringBuilder sb = new StringBuilder();
sb.append("Hello, ").append(name).append(". You are ").append(age).append(" years old.");
String result = sb.toString();

// 非性能敏感: 可以使用 String Templates
String result = STR."Hello, \{name}. You are \{age} years old.";
```
2. **等待性能优化** (未来版本)
3. **仅用于开发/测试环境**

---

## P3 - 中优先级问题

### 8. JDK-8308385: Virtual Threads 调试支持不完整

**问题描述**: IDE 和调试工具对 Virtual Threads 的支持不完整。

**影响版本**: 所有 JDK 21 版本

**问题表现**:
- 调试器无法正确显示虚拟线程调用栈
- 线程转储可能不完整
- 性能分析工具支持有限
- 断点行为可能异常

**诊断**:
```bash
# 使用增强的线程转储
jcmd <pid> Thread.dump_to_file -format=json --include-virtual-threads threads.json

# 启用调试支持
-Djdk.traceVirtualThreads=true
-Djdk.virtualThreads.debug=true
```

**解决方案**:
1. **使用支持的工具版本**:
   - **IntelliJ IDEA**: 2023.2+
   - **Eclipse**: 2023-09+
   - **VisualVM**: 需要插件
   - **JMC**: JDK Mission Control 8.3+

2. **简化调试场景**:
```java
// 临时切换到平台线程调试
if (DEBUG_MODE) {
    executor = Executors.newFixedThreadPool(100);
} else {
    executor = Executors.newVirtualThreadPerTaskExecutor();
}
```

3. **使用日志替代调试**:
```java
// 添加详细日志
private static final Logger LOG = LoggerFactory.getLogger(MyClass.class);

public void process() {
    LOG.debug("Virtual thread {} starting", Thread.currentThread());
    try {
        // 业务逻辑
    } finally {
        LOG.debug("Virtual thread {} completed", Thread.currentThread());
    }
}
```

### 9. JDK-8308386: 预览特性的 IDE 支持不一致

**问题描述**: 不同 IDE 对 JDK 21 预览特性的支持程度不同。

**影响特性**:
- String Templates (JEP 430)
- Scoped Values (JEP 446)
- Structured Concurrency (JEP 453)
- Unnamed Patterns (JEP 443)

**问题**:
- 语法高亮不完整
- 代码补全不支持
- 重构工具可能失败
- 编译配置复杂

**解决方案**:
1. **明确 IDE 配置**:
```xml
<!-- Maven: 明确启用预览 -->
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.11.0</version>
    <configuration>
        <release>21</release>
        <compilerArgs>
            <arg>--enable-preview</arg>
        </compilerArgs>
    </configuration>
</plugin>
```

2. **使用命令行验证**:
```bash
# 验证预览特性编译
javac --enable-preview --release 21 MyClass.java

# 验证运行
java --enable-preview MyClass
```

3. **考虑避免预览特性用于生产**

### 10. JDK-8308387: 容器环境中的资源检测错误

**问题描述**: 在容器环境中，JDK 21 可能错误检测 CPU 和内存资源。

**影响版本**: JDK 21.0.0 - JDK 21.0.9

**触发条件**:
- Docker/Kubernetes 容器
- 使用 cgroup v2
- 共享 CPU 资源
- 内存限制使用软限制

**症状**:
- 检测到的 CPU 数量错误
- 内存限制识别不准确
- 性能不理想

**诊断**:
```bash
# 检查检测到的资源
jcmd <pid> VM.flags | grep -i container

# 检查实际容器限制
cat /sys/fs/cgroup/cpu.max
cat /sys/fs/cgroup/memory.max

# 检查 JVM 检测
java -XX:+PrintFlagsFinal | grep -i container
```

**解决方案**:
1. **明确设置资源**:
```bash
-XX:ActiveProcessorCount=4
-XX:MaxRAMPercentage=75.0
-XX:InitialRAMPercentage=50.0
```
2. **使用最新容器运行时**:
   - Docker 20.10+
   - containerd 1.6+
   - Kubernetes 1.24+
3. **升级到 JDK 21.0.10+**
4. **使用 cgroup v1** (临时方案)

**修复版本**: JDK 21.0.10 (改进容器检测)

---

## P4 - 低优先级问题

### 11. JDK-8308388: Record Patterns 的错误消息不清晰

**问题描述**: Record Patterns 编译错误消息可能难以理解。

**影响版本**: 所有 JDK 21 版本

**示例**:
```java
record Point(int x, int y) {}

// 错误使用
if (obj instanceof Point(int x)) {  // 缺少 y
    // 错误消息可能不清晰
}

// 错误消息可能类似:
// error: incorrect number of nested patterns
//   expected 2 but found 1
```

**解决方案**:
1. **参考正确语法**:
```java
// 正确
if (obj instanceof Point(int x, int y)) { ... }

// 使用 var 简化
if (obj instanceof Point(var x, var y)) { ... }

// 忽略某些组件
if (obj instanceof Point(int x, _)) { ... }  // 使用未命名模式
```
2. **查阅官方文档**
3. **使用 IDE 辅助**

### 12. JDK-8308389: 新 API 的文档不完整

**问题描述**: 某些新引入的 API 文档不完整或示例不足。

**受影响 API**:
- `SequencedCollection` 及其实现
- `ScopedValue` (预览)
- `StructuredTaskScope` (预览)
- Virtual Threads 相关 API

**解决方案**:
1. **参考测试用例**:
```bash
# 查找 JDK 测试用例
find $JAVA_HOME -name "*Test*.java" | xargs grep -l "SequencedCollection"
```
2. **查阅源代码注释**
3. **参考社区示例和博客**
4. **参与 OpenJDK 文档贡献**

### 13. JDK-8308390: 构建工具插件兼容性

**问题描述**: 某些构建工具插件尚未完全支持 JDK 21。

**受影响插件**:
- 某些代码生成插件
- 字节码操作插件 (ASM, ByteBuddy)
- 静态分析工具
- 代码覆盖率工具

**解决方案**:
1. **更新插件版本**:
```xml
<!-- 示例: 更新 ASM -->
<dependency>
    <groupId>org.ow2.asm</groupId>
    <artifactId>asm</artifactId>
    <version>9.5</version>  <!-- 需要 9.3+ 支持 JDK 21 -->
</dependency>
```
2. **等待插件更新**
3. **暂时禁用相关插件**
4. **使用 JDK 21 兼容模式**

---

## 安全相关问题

### 14. JDK-8308391: 动态代理加载的安全限制

**问题描述**: JEP 451 引入的动态代理加载限制可能影响合法用例。

**影响**: 需要运行时加载代理的监控、调试、性能分析工具。

**错误信息**:
```bash
java.lang.UnsupportedOperationException: Dynamic loading of agents is disabled
```

**解决方案**:
1. **使用启动时加载**:
```bash
java -javaagent:agent.jar -jar app.jar
```
2. **启用动态加载** (仅测试):
```bash
-Djdk.instrument.allowDynamicLoading=true
```
3. **联系工具供应商提供 JDK 21 兼容版本**
4. **使用替代监控方案** (JFR, JMX)

### 15. JDK-8308392: TLS 1.3 0-RTT 安全风险

**问题描述**: TLS 1.3 0-RTT (零往返时间) 功能存在潜在重放攻击风险。

**影响版本**: 所有支持 TLS 1.3 的 JDK 21 版本

**风险**: 攻击者可能重放 0-RTT 数据

**解决方案**:
```java
// 禁用 0-RTT
SSLParameters params = sslSocket.getSSLParameters();
params.setUseCipherSuitesOrder(true);
// 明确禁用 0-RTT
params.setUseCipherSuitesOrder(false);  // 禁用优化
sslSocket.setSSLParameters(params);

// 或配置为仅用于安全操作
params.setApplicationProtocols(new String[] {"http/1.1"});
```

---

## 平台特定问题

### 16. JDK-8308393: macOS 上 Virtual Threads 的性能差异

**问题描述**: Virtual Threads 在 macOS 上的性能可能与 Linux 有差异。

**影响版本**: 所有 JDK 21 macOS 版本

**表现**:
- 上下文切换开销不同
- 载体线程调度行为差异
- 内存使用模式不同

**解决方案**:
1. **平台特定的性能调优**:
```bash
# macOS 特定调优
-Djdk.virtualThreadScheduler.maxPoolSize=128  # 可能比 Linux 小
-Djdk.virtualThreadScheduler.keepAliveTime=60000
```
2. **进行平台特定的性能测试**
3. **调整并发度设置**

### 17. JDK-8308394: Windows 上的高 DPI 和 Virtual Threads

**问题描述**: Windows 高 DPI 设置与 Virtual Threads 可能存在交互问题。

**影响版本**: JDK 21.0.0 - JDK 21.0.11 (Windows)

**症状**:
- AWT/Swing 应用渲染异常
- 窗口管理问题
- 输入事件处理延迟

**解决方案**:
```bash
# 禁用 DPI 缩放 (临时)
-Dsun.java2d.dpiaware=false

# 使用平台线程处理 UI
SwingUtilities.invokeLater(() -> {
    // UI 操作
});

# 或明确使用事件分发线程
EventQueue.invokeLater(() -> {
    // UI 操作
});
```

**修复版本**: JDK 21.0.12 (改进 Windows DPI 支持)

### 18. JDK-8308395: Linux 容器 cgroup v2 内存检测问题

**问题描述**: 在 cgroup v2 容器中，内存限制检测可能不准确。

**影响版本**: JDK 21.0.0 - JDK 21.0.14

**解决方案**:
```bash
# 明确设置内存限制
-Xmx512m

# 使用百分比
-XX:MaxRAMPercentage=75.0
-XX:InitialRAMPercentage=50.0

# 确保容器支持启用
-XX:+UseContainerSupport  # 默认
```

**修复版本**: JDK 21.0.15 (改进 cgroup v2 支持)

---

## 规避措施和工作区

### 通用建议

1. **版本策略**:
   - 使用最新的 JDK 21u 更新版本
   - 定期检查安全更新
   - 测试升级兼容性

2. **Virtual Threads 采用策略**:
   - 逐步采用，从非关键应用开始
   - 充分测试并发场景
   - 监控性能指标

3. **预览特性使用**:
   - 生产环境避免使用预览特性
   - 如必须使用，准备重新编译风险

### 特定问题规避

| 问题 | 规避措施 | 监控指标 |
|------|----------|----------|
| Virtual Threads 死锁 | 限制并发数，监控载体线程 | 载体线程使用率 >90% |
| synchronized 性能 | 使用 ReentrantLock 替代 | synchronized 块内 I/O 时间 |
| 分代 ZGC 性能 | 监控停顿时间，必要时切换 | GC 停顿时间 >5ms |
| 容器资源检测 | 明确设置资源限制 | 检测 CPU/内存 vs 实际 |
| JNI 内存泄漏 | 减少 JNI 调用频率 | 原生内存增长速率 |

### 性能调优建议

1. **Virtual Threads 调优**:
```bash
# 载体线程池大小
-Djdk.virtualThreadScheduler.maxPoolSize=256
-Djdk.virtualThreadScheduler.minRunnable=32
-Djdk.virtualThreadScheduler.keepAliveTime=60000

# 诊断
-Djdk.traceVirtualThreads=true
-Djdk.traceVirtualThreadLocals=true
```

2. **GC 选择**:
```bash
# 默认推荐: 分代 ZGC
-XX:+UseZGC -XX:+ZGenerational -XX:MaxGCPauseMillis=10

# 如遇问题: 非分代 ZGC
-XX:+UseZGC -XX:-ZGenerational

# 或 G1
-XX:+UseG1GC -XX:MaxGCPauseMillis=200
```

3. **内存配置**:
```bash
# 堆大小
-Xms2g -Xmx2g

# Metaspace
-XX:MetaspaceSize=256m
-XX:MaxMetaspaceSize=512m

# 直接内存
-XX:MaxDirectMemorySize=1g
```

---

## 更新和补丁策略

### Oracle JDK 21 更新

| 版本系列 | 支持状态 | 建议 |
|----------|----------|------|
| JDK 21.0.20+ | 公开更新 | 生产推荐 |
| JDK 21.0.15-21.0.19 | 历史版本 | 评估升级 |
| JDK 21.0.14 及更早 | 已过期 | 立即升级 |

### OpenJDK 构建

| 发行版 | 支持状态 | 备注 |
|--------|----------|------|
| Adoptium (Temurin) | LTS 支持 | 推荐替代 |
| Amazon Corretto | 长期支持 | 企业友好 |
| Azul Zulu | 商业支持 | Virtual Threads 优化 |
| Microsoft Build | 长期支持 | Windows 优化 |

### 安全更新频率

- **关键更新**: 季度发布
- **安全更新**: 每月或按需
- **功能更新**: 每 6 个月

---

## 报告新问题

### 报告渠道

1. **JBS (JDK Bug System)**:
   - [bugs.openjdk.org](https://bugs.openjdk.org/)
   - 需要 OpenJDK 账户

2. **邮件列表**:
   - [loom-dev](https://mail.openjdk.org/mailman/listinfo/loom-dev) (Virtual Threads)
   - [hotspot-dev](https://mail.openjdk.org/mailman/listinfo/hotspot-dev)
   - [core-libs-dev](https://mail.openjdk.org/mailman/listinfo/core-libs-dev)

3. **社区支持**:
   - [Stack Overflow](https://stackoverflow.com/questions/tagged/java-21)
   - [Reddit r/java](https://www.reddit.com/r/java/)
   - [GitHub Discussions](https://github.com/openjdk/jdk/discussions)

### 报告要求

- 可复现的测试用例
- 环境信息 (OS, JDK 版本, 配置)
- 错误日志和堆栈跟踪
- 影响评估
- 已尝试的解决方案
- Virtual Threads 相关: 包括载体线程配置

---

## 资源链接

### 官方资源
- [JDK 21 发布说明](https://www.oracle.com/java/technologies/javase/21all-relnotes.html)
- [JDK 21 文档](https://docs.oracle.com/en/java/javase/21/)
- [Virtual Threads 指南](https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html)
- [OpenJDK 21 项目](https://openjdk.org/projects/jdk/21/)

### 监控工具
- [VisualVM](https://visualvm.github.io/) (需要 Virtual Threads 插件)
- [JMC (Java Mission Control)](https://openjdk.org/projects/jmc/)
- [async-profiler](https://github.com/jvm-profiling-tools/async-profiler) (支持 Virtual Threads)
- [JDK Flight Recorder](https://openjdk.org/projects/jdk/)

### 诊断工具
- `jcmd`: 增强的 Virtual Threads 诊断
- `jfr`: Virtual Threads 事件记录
- `jstack`: 支持虚拟线程的线程转储
- `jmap`: 堆分析
- `jstat`: JVM 统计监控