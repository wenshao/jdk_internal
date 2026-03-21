# 从 JDK 17 迁移到 JDK 21

> **迁移复杂度**: 中高 | **建议时间**: 4-8 周 | **关键变革**: Virtual Threads 革命性并发模型

---
## 目录

1. [迁移概览](#1-迁移概览)
2. [Virtual Threads 迁移评估](#2-virtual-threads-迁移评估)
3. [代码迁移步骤](#3-代码迁移步骤)
4. [配置迁移](#4-配置迁移)
5. [测试策略](#5-测试策略)
6. [部署策略](#6-部署策略)
7. [常见问题解决](#7-常见问题解决)
8. [迁移后优化](#8-迁移后优化)
9. [工具和资源](#9-工具和资源)
10. [总结检查清单](#10-总结检查清单)

---


## 1. 迁移概览

### 为什么迁移到 JDK 21？

1. **Virtual Threads 革命**: 重新定义 Java 并发编程，数量级性能提升
2. **最新 LTS**: JDK 21 (LTS 2023) 支持至 2031 年
3. **语言特性成熟**: Record Patterns、Pattern Matching for switch 正式版
4. **性能飞跃**: 分代 ZGC、Sequenced Collections 性能优化
5. **现代开发体验**: 预览特性提供未来方向

### 迁移路径
```
JDK 17 (当前)
    ↓
兼容性评估 (1-2 周)
    ↓    
Virtual Threads 评估 (1-2 周)
    ↓
代码迁移 (2-3 周)
    ↓
性能测试 (1-2 周)
    ↓
生产部署
```

### 关键差异
| 方面 | JDK 17 | JDK 21 | 影响等级 |
|------|--------|--------|----------|
| **并发模型** | Platform Threads | Virtual Threads (JEP 444) | ⭐⭐⭐ (革命性) |
| **语言特性** | 预览阶段 | Record Patterns、switch 正式版 | ⭐⭐ (重要) |
| **GC 特性** | ZGC 单代 | 分代 ZGC (JEP 439) | ⭐ (改进) |
| **集合 API** | 传统集合 | Sequenced Collections (JEP 431) | ⭐ (增强) |
| **预览特性** | 有限 | String Templates、Scoped Values 等 | ⭐ (探索性) |

---

## 2. Virtual Threads 迁移评估

### 理解变革

**传统线程 (JDK 17 及之前)**:
```java
// 平台线程: 1:1 映射到操作系统线程
ExecutorService executor = Executors.newFixedThreadPool(200);  // 通常 <1000 线程
```

**虚拟线程 (JDK 21)**:
```java
// 虚拟线程: JVM 管理的轻量级线程
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    // 可创建数百万个虚拟线程
    Future<?> future = executor.submit(() -> {
        Thread.sleep(1000);  // 不会阻塞操作系统线程
        return "result";
    });
}
```

### 适用性评估矩阵

| 应用类型 | Virtual Threads 适用性 | 预期收益 | 风险 |
|----------|------------------------|----------|------|
| **微服务/REST API** | ⭐⭐⭐ (极高) | 吞吐量 2-5x，延迟降低 50-80% | 低 |
| **数据库密集型** | ⭐⭐⭐ (极高) | 连接池需求减少，吞吐量提升 | 中 |
| **消息队列消费者** | ⭐⭐ (高) | 并发消费者数量大幅增加 | 低 |
| **计算密集型** | ⭐ (低) | 无收益，可能略差 | 低 |
| **GUI 应用** | ⭐ (低) | UI 线程仍应用平台线程 | 中 |

### 快速评估工具

```java
public class VirtualThreadsAssessment {
    
    public static AssessmentResult assessApplication() {
        AssessmentResult result = new AssessmentResult();
        
        // 1. 检查线程使用模式
        Map<Thread, StackTraceElement[]> allThreads = Thread.getAllStackTraces();
        long platformThreads = allThreads.keySet().stream()
            .filter(t -> !t.isDaemon())
            .count();
        
        result.setPlatformThreadCount(platformThreads);
        result.setRecommendVirtualThreads(platformThreads > 50);
        
        // 2. 检查 I/O 操作比例
        // 通过代码分析或监控数据
        
        // 3. 检查 synchronized 使用
        // 使用静态分析工具
        
        return result;
    }
    
    static class AssessmentResult {
        private long platformThreadCount;
        private boolean recommendVirtualThreads;
        private String riskLevel;
        // getters/setters
    }
}
```

---

## 3. 代码迁移步骤

### 步骤 1: 构建环境更新

**Maven 配置**:
```xml
<properties>
    <maven.compiler.source>21</maven.compiler.source>
    <maven.compiler.target>21</maven.compiler.target>
    <maven.compiler.release>21</maven.compiler.release>
    <!-- 启用预览特性 (如果需要) -->
    <maven.compiler.enablePreview>true</maven.compiler.enablePreview>
</properties>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.11.0</version>
            <configuration>
                <release>21</release>
                <parameters>true</parameters>
                <compilerArgs>
                    <arg>--enable-preview</arg>
                </compilerArgs>
            </configuration>
        </plugin>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.0.0</version>
            <configuration>
                <argLine>--enable-preview</argLine>
            </configuration>
        </plugin>
    </plugins>
</build>
```

**Gradle 配置**:
```groovy
plugins {
    id 'java'
}

java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
    modularity.inferModulePath = true
}

tasks.withType(JavaCompile) {
    options.compilerArgs += ['--release', '21', '--enable-preview']
}

tasks.withType(Test) {
    jvmArgs += '--enable-preview'
}

tasks.withType(JavaExec) {
    jvmArgs += '--enable-preview'
}
```

### 步骤 2: Virtual Threads 迁移

#### 2.1 线程池迁移

```java
// JDK 17: 传统线程池
ExecutorService executor = Executors.newFixedThreadPool(200);
// 或
ExecutorService executor = Executors.newCachedThreadPool();

// JDK 21: 虚拟线程执行器 (推荐)
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();

// 或兼容性迁移 (逐步过渡)
ExecutorService executor = createExecutor();
// 根据配置选择
private ExecutorService createExecutor() {
    if (useVirtualThreads()) {
        return Executors.newVirtualThreadPerTaskExecutor();
    } else {
        return Executors.newFixedThreadPool(getThreadPoolSize());
    }
}
```

#### 2.2 处理 synchronized 问题

```java
// 问题: synchronized 会阻塞载体线程
public class Counter {
    private int count;
    
    public synchronized void increment() {
        count++;
        Thread.sleep(10);  // I/O 操作 → 阻塞载体线程!
    }
}

// 解决方案 A: 使用 ReentrantLock
public class Counter {
    private int count;
    private final Lock lock = new ReentrantLock();
    
    public void increment() {
        lock.lock();
        try {
            count++;
            Thread.sleep(10);  // 不会阻塞载体线程
        } finally {
            lock.unlock();
        }
    }
}

// 解决方案 B: 分离 I/O 操作
public void process() {
    Data data;
    synchronized (this) {
        data = getData();  // 快速操作
    }
    // I/O 在同步块外
    processIO(data);
}
```

#### 2.3 ThreadLocal 迁移

```java
// JDK 17: 正常使用 ThreadLocal
private static final ThreadLocal<Context> contextHolder = new ThreadLocal<>();

public void process() {
    contextHolder.set(new Context());
    try {
        // 业务逻辑
    } finally {
        contextHolder.remove();
    }
}

// JDK 21: 减少使用或迁移到 ScopedValue (预览)
// 方案 A: 减少使用频率
public void processBatch(List<Item> items) {
    Context context = createContext();
    for (Item item : items) {
        processItem(item, context);  // 传递参数而非 ThreadLocal
    }
}

// 方案 B: 使用 ScopedValue (预览特性)
private static final ScopedValue<Context> CURRENT_CONTEXT = ScopedValue.newInstance();

public void process() {
    ScopedValue.where(CURRENT_CONTEXT, new Context()).run(() -> {
        // 在此作用域内可访问
        businessLogic();
    });
}
```

### 步骤 3: 采用新语言特性

#### 3.1 Record Patterns 正式版

```java
// 从传统方式迁移
record Point(int x, int y) {}

// JDK 17: 传统 instanceof + 转换
if (obj instanceof Point) {
    Point p = (Point) obj;
    System.out.println("x=" + p.x() + ", y=" + p.y());
}

// JDK 21: Record Patterns
if (obj instanceof Point(int x, int y)) {
    System.out.println("x=" + x + ", y=" + y);
}

// 嵌套解构
record Rectangle(Point topLeft, Point bottomRight) {}

if (obj instanceof Rectangle(Point(var x1, var y1), Point(var x2, var y2))) {
    System.out.printf("Rectangle from (%d,%d) to (%d,%d)%n", x1, y1, x2, y2);
}
```

#### 3.2 Pattern Matching for switch 正式版

```java
// 移除预览标志，正式使用
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

// 与密封类结合 (编译时穷尽性检查)
sealed interface Shape permits Circle, Rectangle, Triangle {
    double area();
}

static String describe(Shape shape) {
    return switch (shape) {
        case Circle c    -> "Circle: radius=" + c.radius();
        case Rectangle r -> "Rectangle: " + r.width() + "x" + r.height();
        case Triangle t  -> "Triangle";
        // 不需要 default，编译器确保所有情况覆盖
    };
}
```

#### 3.3 Sequenced Collections

```java
// 迁移集合操作
// 之前: 多种方式访问首尾元素
List<String> list = new ArrayList<>();
if (!list.isEmpty()) {
    String first = list.get(0);           // ArrayList
    // 或
    String first = list.getFirst();       // LinkedList
}

// 之后: 统一 API
SequencedCollection<String> seq = new ArrayList<>();
seq.addFirst("first");    // 添加到开头
seq.addLast("last");      // 添加到结尾
String first = seq.getFirst();
String last = seq.getLast();

// 反向视图 (不复制)
SequencedCollection<String> reversed = seq.reversed();

// Map 操作统一
SequencedMap<String, Integer> map = new LinkedHashMap<>();
map.putFirst("a", 1);
map.putLast("z", 26);
Map.Entry<String, Integer> firstEntry = map.firstEntry();
```

### 步骤 4: 使用预览特性 (可选)

#### 4.1 String Templates (预览)

```java
// 传统方式
String name = "Alice";
int age = 30;
String message = String.format("Hello, %s. You are %d years old.", name, age);

// String Templates (预览)
String message = STR."Hello, \{name}. You are \{age} years old.";

// 多行模板
String json = STR."""
    {
        "name": "\{name}",
        "age": \{age}
    }
    """;

// 自定义模板处理器
StringTemplate.Processor<String, RuntimeException> JSON = 
    StringTemplate.Processor.of(
        template -> {
            // 自定义处理逻辑
            return new ObjectMapper().writeValueAsString(template.values());
        }
    );
```

#### 4.2 Scoped Values (预览)

```java
// 替代 ThreadLocal 在 Virtual Threads 场景
private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();

// 设置作用域值
ScopedValue.where(CURRENT_USER, user).run(() -> {
    // 在此作用域内可访问
    processRequest();
});

// 嵌套作用域
ScopedValue.where(CURRENT_USER, user1).run(() -> {
    // user1 可见
    ScopedValue.where(CURRENT_USER, user2).run(() -> {
        // user2 可见 (遮蔽 user1)
    });
    // 恢复 user1
});
```

#### 4.3 Structured Concurrency (预览)

```java
// 简化并发任务管理
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> user = scope.fork(() -> fetchUser(userId));
    Future<List<Order>> orders = scope.fork(() -> fetchOrders(userId));
    
    scope.join();           // 等待所有任务
    scope.throwIfFailed();  // 如果有失败则抛出
    
    return new Response(user.resultNow(), orders.resultNow());
}  // 自动关闭，取消未完成的任务
```

---

## 4. 配置迁移

### JVM 参数更新

#### Virtual Threads 配置

```bash
# 基本启用
-Djdk.virtualThreadScheduler.maxPoolSize=256
-Djdk.virtualThreadScheduler.minRunnable=32
-Djdk.virtualThreadScheduler.keepAliveTime=60000

# 诊断配置
-Djdk.traceVirtualThreads=true
-Djdk.traceVirtualThreadLocals=true
-Djdk.virtualThreads.debug=true

# 平台线程回退 (兼容性)
-Djdk.virtualThreads.enabled=true  # 默认 true
```

#### 分代 ZGC 配置

```bash
# 启用分代 ZGC (推荐)
-XX:+UseZGC -XX:+ZGenerational

# 调优参数
-Xmx16g -Xms16g
-XX:MaxGCPauseMillis=10
-XX:ConcGCThreads=4
-XX:ZYoungGenerationSizeLimit=2g
-XX:ZAllocationSpikeTolerance=3.0

# 监控
-Xlog:gc*,gc+heap*,gc+stats*:file=gc.log:time,level,tags
```

#### 模块系统增强

```bash
# Virtual Threads 需要额外的包开放
--add-opens java.base/jdk.internal.vm=ALL-UNNAMED
--add-opens java.base/java.lang=ALL-UNNAMED
--add-opens java.base/java.util.concurrent=ALL-UNNAMED

# 兼容性包开放 (如果遇到访问错误)
--add-opens java.base/jdk.internal.misc=ALL-UNNAMED
--add-opens java.base/sun.nio.ch=ALL-UNNAMED
```

#### 安全配置更新

```bash
# 动态代理加载限制 (JEP 451)
# 默认禁止动态加载，需要代理的应用使用:
java -javaagent:agent.jar -jar app.jar

# 或启用动态加载 (不推荐生产)
-Djdk.instrument.allowDynamicLoading=true

# TLS 配置 (保持兼容性)
-Djdk.tls.client.protocols=TLSv1.2,TLSv1.3
-Djdk.tls.server.protocols=TLSv1.2,TLSv1.3
```

### 应用框架配置

#### Spring Boot 3 迁移

**重要**: Spring Boot 3.x 需要 JDK 17+，并迁移到 Jakarta EE 10。

```yaml
# application.yml
spring:
  threads:
    virtual:
      enabled: true  # 启用 Virtual Threads
  
server:
  tomcat:
    # 传统线程用于连接处理
    threads:
      max: 200
      min-spare: 10
    # Virtual Threads 用于请求处理
    
# Jakarta EE 10 (包名从 javax 改为 jakarta)
# 自动处理，但需要更新导入
```

**依赖更新**:
```xml
<!-- Spring Boot 3.x -->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>  <!-- 需要 JDK 17+ -->
</parent>

<!-- Jakarta EE 10 -->
<dependency>
    <groupId>jakarta.servlet</groupId>
    <artifactId>jakarta.servlet-api</artifactId>
    <version>6.0.0</version>
</dependency>
```

#### 数据库连接池优化

```properties
# 使用 Virtual Threads 可减少连接池大小
# HikariCP 配置
spring.datasource.hikari.maximum-pool-size=20  # 之前可能 50-100
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.connection-timeout=30000

# 连接验证
spring.datasource.hikari.connection-test-query=SELECT 1
```

---

## 5. 测试策略

### Virtual Threads 测试

#### 1. 功能正确性测试

```java
@Test
void testVirtualThreadsBasic() {
    try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
        Future<String> future = executor.submit(() -> {
            return "Hello from virtual thread";
        });
        
        assertEquals("Hello from virtual thread", future.get());
    }
}

@Test
void testVirtualThreadsWithIO() throws Exception {
    try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
        List<Future<Integer>> futures = new ArrayList<>();
        
        for (int i = 0; i < 1000; i++) {
            int taskId = i;
            futures.add(executor.submit(() -> {
                Thread.sleep(10);  // 模拟 I/O
                return taskId;
            }));
        }
        
        for (int i = 0; i < 1000; i++) {
            assertEquals(i, futures.get(i).get());
        }
    }
}
```

#### 2. 并发测试

```java
@Test
void testVirtualThreadsConcurrency() {
    AtomicInteger counter = new AtomicInteger();
    int threadCount = 10_000;
    
    try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
        List<Future<?>> futures = new ArrayList<>();
        
        for (int i = 0; i < threadCount; i++) {
            futures.add(executor.submit(() -> {
                counter.incrementAndGet();
            }));
        }
        
        for (Future<?> future : futures) {
            future.get();
        }
        
        assertEquals(threadCount, counter.get());
    }
}
```

#### 3. 线程固定测试

```java
@Test
void testThreadPinningDetection() {
    // 测试 synchronized 是否导致线程固定
    Object lock = new Object();
    
    try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
        Future<?> future = executor.submit(() -> {
            synchronized (lock) {
                Thread.sleep(100);  // 会固定线程
                return "done";
            }
        });
        
        future.get();
    }
    
    // 检查日志中是否有 "Pinned" 警告
    // 需要启用: -Djdk.traceVirtualThreads=true
}
```

### 性能基准测试

#### JMH 基准测试

```java
@State(Scope.Benchmark)
@BenchmarkMode(Mode.Throughput)
@OutputTimeUnit(TimeUnit.SECONDS)
public class VirtualThreadsBenchmark {
    
    @Param({"100", "1000", "10000"})
    private int taskCount;
    
    @Benchmark
    public void platformThreads() throws Exception {
        try (var executor = Executors.newFixedThreadPool(200)) {
            executeTasks(executor);
        }
    }
    
    @Benchmark
    public void virtualThreads() throws Exception {
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            executeTasks(executor);
        }
    }
    
    private void executeTasks(ExecutorService executor) throws Exception {
        List<Future<?>> futures = new ArrayList<>();
        for (int i = 0; i < taskCount; i++) {
            futures.add(executor.submit(() -> {
                LockSupport.parkNanos(1_000_000);  // 1ms 延迟
            }));
        }
        for (Future<?> future : futures) {
            future.get();
        }
    }
}
```

#### 真实应用性能测试

**测试场景**:
1. **基线测试**: JDK 17 + Platform Threads
2. **迁移测试**: JDK 21 + Platform Threads (兼容性)
3. **优化测试**: JDK 21 + Virtual Threads

**关键指标**:
- 吞吐量 (请求/秒)
- 延迟 (P50, P95, P99)
- 内存使用
- CPU 使用率
- GC 停顿时间

### 兼容性测试

#### 第三方库兼容性验证

| 库/框架 | 测试要点 | 预期结果 |
|---------|----------|----------|
| **Netty** | Virtual Threads 兼容性 | 应支持，检查版本 (4.1.90+) |
| **gRPC** | 客户端/服务器交互 | 应正常工作 |
| **数据库驱动** | 连接池行为 | 连接池需求可能减少 |
| **缓存客户端** | 连接管理 | 应正常工作 |
| **消息队列** | 消费者并发度 | 可大幅增加消费者数量 |

#### JNI 兼容性测试

```java
@Test
void testJNIWithVirtualThreads() {
    // 测试本地方法调用
    try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
        Future<?> future = executor.submit(() -> {
            nativeMethod();  // JNI 调用
        });
        future.get();  // 应正常完成
    }
}

private native void nativeMethod();
```

---

## 6. 部署策略

### 分阶段部署计划

#### 阶段 1: 兼容性验证 (1-2 周)
```yaml
# Kubernetes 部署 - 阶段 1
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-jdk21-compat
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: app
        image: app:jdk21-compat
        env:
        - name: JAVA_TOOL_OPTIONS
          value: >
            -Djdk.virtualThreads.enabled=false  # 禁用 Virtual Threads
            -XX:+UseZGC -XX:-ZGenerational     # 使用非分代 ZGC
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
```

**验证目标**:
- ✅ 应用启动正常
- ✅ 基本功能测试通过
- ✅ 性能基线测试

#### 阶段 2: Virtual Threads 试点 (2-3 周)
```yaml
# 阶段 2: 启用 Virtual Threads
env:
- name: JAVA_TOOL_OPTIONS
  value: >
    -Djdk.virtualThreads.enabled=true
    -Djdk.virtualThreadScheduler.maxPoolSize=64
    -XX:+UseZGC -XX:+ZGenerational
```

**试点应用选择标准**:
1. 无状态服务
2. I/O 密集型工作负载
3. 有完善的监控
4. 可快速回滚

#### 阶段 3: 全面推广 (3-4 周)
**推广策略**:
- 按业务线逐步推广
- 监控关键指标
- 建立回滚机制

### 监控和告警

#### 新增监控指标

```promql
# Virtual Threads 监控
jvm_threads_virtual_live
rate(jvm_threads_virtual_created_total[5m])
rate(jvm_threads_virtual_pinned_total[5m])

# 载体线程监控
jvm_threads_carrier_active
jvm_threads_carrier_idle
jvm_threads_carrier_utilization

# 分代 ZGC 监控
jvm_gc_collection_seconds_count{gc="ZGC Young Generation"}
jvm_gc_collection_seconds_count{gc="ZGC Old Generation"}
jvm_gc_collection_seconds_sum{gc="ZGC Young Generation"}
```

#### 关键告警规则

```yaml
- alert: VirtualThreadsPinnedHigh
  expr: rate(jvm_threads_virtual_pinned_total[5m]) > 100
  for: 5m
  labels:
    severity: warning
  annotations:
    description: Virtual Threads 被固定频率过高，可能影响性能

- alert: VirtualThreadsCreationRateHigh
  expr: rate(jvm_threads_virtual_created_total[5m]) > 1000
  for: 2m
  labels:
    severity: warning
  annotations:
    description: Virtual Threads 创建率过高，检查是否有泄漏

- alert: ZGCYoungGenFrequent
  expr: rate(jvm_gc_collection_seconds_count{gc="ZGC Young Generation"}[5m]) > 10
  for: 5m
  labels:
    severity: warning
  annotations:
    description: 年轻代 GC 过于频繁，考虑调整年轻代大小
```

### 回滚计划

#### 快速回滚触发器
- Virtual Threads 内存泄漏
- 性能下降超过 20%
- 并发问题 (死锁、竞争条件)
- 兼容性问题

#### 回滚步骤
```bash
# 1. 停止 JDK 21 实例
kubectl scale deployment app-jdk21 --replicas=0

# 2. 启动 JDK 17 实例
kubectl scale deployment app-jdk17 --replicas=3

# 3. 验证回滚
kubectl rollout status deployment/app-jdk17
curl -f http://app/health
kubectl logs deployment/app-jdk17 --tail=100

# 4. 验证功能
./scripts/run_smoke_tests.sh
```

---

## 7. 常见问题解决

### Virtual Threads 相关问题

#### 问题 1: 线程被过度固定

**症状**: 性能提升不如预期，日志显示 "Pinned" 警告。

**诊断**:
```bash
# 启用诊断
-Djdk.traceVirtualThreads=true
-Djdk.traceVirtualThreadLocals=true

# 检查日志
grep "Pinned" application.log
```

**解决方案**:
1. 减少 `synchronized` 使用，改用 `ReentrantLock`
2. 避免在同步块内进行 I/O
3. 减少 `ThreadLocal` 使用
4. 批量处理减少锁竞争

#### 问题 2: 内存泄漏

**症状**: 原生内存持续增长。

**诊断**:
```bash
# 监控原生内存
jcmd <pid> VM.native_memory summary scale=MB

# 检查虚拟线程数量
jcmd <pid> Thread.print | grep -c "VirtualThread"
```

**解决方案**:
1. 确保正确关闭执行器 (`try-with-resources`)
2. 限制并发虚拟线程数
3. 定期重启应用 (临时方案)
4. 升级到最新 JDK 21 更新版本

### 兼容性问题

#### 问题 3: 第三方库不兼容

**症状**: 库功能异常或性能问题。

**解决方案**:
1. 检查库版本兼容性
2. 联系供应商获取 JDK 21 兼容版本
3. 使用兼容性配置
4. 考虑替代库

#### 问题 4: JNI 代码问题

**症状**: 本地方法调用失败或性能问题。

**解决方案**:
1. 在平台线程中执行 JNI 调用
```java
if (Thread.currentThread().isVirtual()) {
    Future<?> future = platformExecutor.submit(() -> nativeMethod());
    future.get();
} else {
    nativeMethod();
}
```
2. 重新审查 JNI 代码，避免阻塞操作
3. 更新本地库到最新版本

### 性能问题

#### 问题 5: 分代 ZGC 性能不如预期

**症状**: GC 停顿时间增加或吞吐量下降。

**解决方案**:
1. 切换到非分代模式测试
```bash
-XX:+UseZGC -XX:-ZGenerational
```
2. 调整年轻代大小
```bash
-XX:ZYoungGenerationSizeLimit=1g
```
3. 监控 GC 日志，分析模式
4. 考虑其他 GC (G1, Shenandoah)

---

## 8. 迁移后优化

### 架构优化机会

#### 1. 简化异步代码

```java
// 之前: 复杂的异步回调
CompletableFuture.supplyAsync(() -> fetchData(), executor)
    .thenApply(data -> transform(data))
    .thenAccept(result -> process(result))
    .exceptionally(ex -> handleError(ex));

// 之后: 同步风格的 Virtual Threads
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    Future<Data> future = executor.submit(() -> fetchData());
    Data data = future.get();
    Result result = transform(data);
    process(result);
}
```

#### 2. 连接池优化

- 减少数据库连接池大小 (因 Virtual Threads 高效)
- 简化连接管理逻辑
- 改进资源利用率

#### 3. 批处理优化

```java
// 利用 Virtual Threads 高并发特性
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<Result>> futures = items.stream()
        .map(item -> executor.submit(() -> processItem(item)))
        .toList();
    
    List<Result> results = futures.stream()
        .map(Future::get)
        .toList();
}
```

### 持续性能优化

#### 监控和调优循环

1. **监控**: 建立全面的性能监控
2. **分析**: 定期分析性能数据
3. **调优**: 基于数据调整配置
4. **验证**: 测试调优效果
5. **文档**: 记录最佳实践

#### 定期性能评估

- 每月性能审查会议
- 季度性能基准测试
- 年度架构性能评审

---

## 9. 工具和资源

### 迁移工具

1. **OpenJDK 工具**:
   - `jdeps`: 依赖分析
   - `jdeprscan`: 废弃 API 扫描
   - `jcmd`: Virtual Threads 诊断
   - `jfr`: 性能分析

2. **第三方工具**:
   - [Virtual Threads Profiler](https://github.com/openjdk/jmc)
   - [Async Profiler](https://github.com/jvm-profiling-tools/async-profiler)
   - [JProfiler](https://www.ej-technologies.com/products/jprofiler/overview.html)

### 学习资源

1. **官方文档**:
   - [JEP 444: Virtual Threads](https://openjdk.org/jeps/444)
   - [JDK 21 迁移指南](https://docs.oracle.com/en/java/javase/21/migrate/)
   - [Virtual Threads 教程](https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html)

2. **社区资源**:
   - [Inside Java: Virtual Threads](https://inside.java/tag/virtual-threads/)
   - [Java Almanac: JDK 21](https://javaalmanac.io/jdk/21/)
   - [迁移案例研究](https://github.com/foo/bar)

### 支持渠道

1. **商业支持**:
   - Oracle Java SE Subscription
   - Red Hat OpenJDK Support
   - Azul Prime Support

2. **社区支持**:
   - [OpenJDK loom-dev 邮件列表](https://mail.openjdk.org/mailman/listinfo/loom-dev)
   - [Stack Overflow: virtual-threads](https://stackoverflow.com/questions/tagged/virtual-threads)
   - [GitHub Discussions](https://github.com/openjdk/jdk/discussions)

---

## 10. 总结检查清单

### 迁移前准备
- [ ] 环境兼容性验证完成
- [ ] Virtual Threads 适用性评估完成
- [ ] 第三方库兼容性检查完成
- [ ] 风险评估矩阵完成
- [ ] 迁移计划制定和批准

### 代码迁移
- [ ] 构建环境更新完成
- [ ] Virtual Threads 迁移策略制定
- [ ] synchronized 代码审查完成
- [ ] ThreadLocal 使用优化完成
- [ ] 新语言特性采用评估完成

### 测试验证
- [ ] 单元测试适配完成
- [ ] Virtual Threads 功能测试完成
- [ ] 性能基准测试达标
- [ ] 兼容性测试通过
- [ ] 回归测试完成

### 部署上线
- [ ] 分阶段部署计划制定
- [ ] 监控告警配置完成
- [ ] 回滚计划测试通过
- [ ] 团队培训完成
- [ ] 文档更新完成

### 长期优化
- [ ] 性能监控持续优化
- [ ] 架构简化路线图制定
- [ ] 最佳实践总结和分享
- [ ] 知识库持续更新