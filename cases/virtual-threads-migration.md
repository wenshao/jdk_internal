# Virtual Threads 迁移实战: Spring Boot 微服务从 JDK 21 到 25

> **声明**: 本文中所有性能数据均为**示意数据**, 用于说明迁移前后的趋势变化, 不代表任何特定硬件环境下的实测结果。

## 目录

- [项目背景](#项目背景)
- [迁移评估](#迁移评估)
- [第一步: 启用虚拟线程](#第一步-启用虚拟线程)
- [踩坑 1: HikariCP 连接池耗尽](#踩坑-1-hikaricp-连接池耗尽)
- [踩坑 2: synchronized 导致载体线程 Pinning](#踩坑-2-synchronized-导致载体线程-pinning)
- [踩坑 3: ThreadLocal 内存膨胀](#踩坑-3-threadlocal-内存膨胀)
- [踩坑 4: Logback MDC 上下文丢失](#踩坑-4-logback-mdc-上下文丢失)
- [最终配置与调优](#最终配置与调优)
- [迁移效果总结](#迁移效果总结)
- [决策指南: 哪些场景不适合虚拟线程](#决策指南-哪些场景不适合虚拟线程)
- [迁移检查清单](#迁移检查清单)

---

## 项目背景

### 系统架构

一个典型的 Spring Boot 3.2 微服务, 负责订单查询与处理:

```
客户端 → Nginx → Spring Boot 服务 → PostgreSQL (主存储)
                                   → Redis (缓存层)
                                   → 下游微服务 (REST 调用)
```

### 技术栈

| 组件             | 版本              |
|-----------------|-------------------|
| JDK             | 21 → 25 (分阶段)  |
| Spring Boot     | 3.2.x → 3.4.x    |
| HikariCP        | 5.x               |
| Lettuce (Redis) | 6.x               |
| Logback         | 1.4.x             |
| Tomcat          | 10.1.x            |

### 迁移前的线程模型

```
# 迁移前 application.yml (示意数据)
server:
  tomcat:
    threads:
      max: 200
      min-spare: 20
    accept-count: 100

spring:
  datasource:
    hikari:
      maximum-pool-size: 50
      minimum-idle: 10
      connection-timeout: 30000

# 自定义业务线程池
app:
  async:
    core-pool-size: 20
    max-pool-size: 50
    queue-capacity: 500
```

迁移前, 系统在高峰期的线程快照 (示意数据):

```
"http-nio-8080-exec-1" through "http-nio-8080-exec-200"   # Tomcat 工作线程
"HikariPool-1 housekeeper"                                 # 连接池维护
"async-executor-1" through "async-executor-50"             # 自定义异步线程池
"lettuce-nioEventLoop-1" through "lettuce-nioEventLoop-4"  # Redis 客户端
```

总线程数: ~270 个平台线程, 每个占用约 1MB 栈空间。

### 关键业务方法 (迁移前)

```java
@Service
public class OrderService {

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private RedisTemplate<String, Order> redisTemplate;

    @Autowired
    private InventoryClient inventoryClient;

    // 典型的 I/O 密集型方法: 缓存查询 + 数据库 + 远程调用
    public OrderDetailDTO getOrderDetail(String orderId) {
        // 1. 查 Redis 缓存
        Order cached = redisTemplate.opsForValue().get("order:" + orderId);
        if (cached != null) {
            return toDTO(cached);
        }

        // 2. 查数据库
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new OrderNotFoundException(orderId));

        // 3. 查库存 (远程 HTTP 调用)
        InventoryInfo inventory = inventoryClient.getInventory(order.getSkuId());

        // 4. 写回缓存
        redisTemplate.opsForValue().set("order:" + orderId, order,
                Duration.ofMinutes(30));

        return toDTO(order, inventory);
    }
}
```

每次请求至少包含 3 次 I/O 阻塞操作, 这正是虚拟线程的理想应用场景。

---

## 迁移评估

### 步骤 1: 识别 I/O 密集的 Service 层

通过以下脚本统计阻塞调用点:

```bash
# 粗略统计各 Service 中的 I/O 调用点
grep -rn "repository\.\|redisTemplate\.\|restTemplate\.\|webClient\." \
  src/main/java/com/example/service/ | wc -l
# 结果: 147 处阻塞调用 (示意数据)
```

### 步骤 2: 审计现有线程池配置

```bash
# 查找所有线程池定义
grep -rn "ThreadPoolTaskExecutor\|ExecutorService\|newFixedThreadPool\|newCachedThreadPool" \
  src/main/java/ | wc -l
# 结果: 8 处自定义线程池 (示意数据)
```

### 步骤 3: 检查不兼容项

重点排查三类问题:

```bash
# 1. synchronized 块内的 I/O 调用 (潜在 pinning)
grep -rn "synchronized" src/main/java/ | wc -l
# 结果: 23 处 (示意数据)

# 2. ThreadLocal 使用情况
grep -rn "ThreadLocal\|InheritableThreadLocal" src/main/java/ | wc -l
# 结果: 12 处 (示意数据)

# 3. 依赖 Thread.currentThread() 身份的代码
grep -rn "Thread.currentThread()" src/main/java/ | wc -l
# 结果: 5 处 (示意数据)
```

### 评估结论

| 评估项               | 结果     | 风险等级 |
|---------------------|---------|---------|
| I/O 密集型方法占比    | 85%     | 适合迁移 |
| synchronized + I/O  | 3 处    | 中等     |
| ThreadLocal 使用     | 12 处   | 中等     |
| 自定义线程池          | 8 处    | 低      |
| 第三方库兼容性        | 良好    | 低      |

决策: **适合迁移**, 预期收益显著。

---

## 第一步: 启用虚拟线程

### 最小改动

Spring Boot 3.2+ 提供了一键开关:

```yaml
# application.yml — 仅需添加一行
spring:
  threads:
    virtual:
      enabled: true
```

这一行配置触发以下变化:

1. Tomcat 的工作线程从平台线程池切换为每请求一个虚拟线程
2. Spring 的 `@Async` 默认执行器改为虚拟线程执行器
3. Spring 管理的 `TaskExecutor` bean 自动使用虚拟线程工厂

### 对应的自动配置源码逻辑

```java
// Spring Boot 自动配置的核心逻辑 (简化示意)
@ConditionalOnProperty(prefix = "spring.threads.virtual",
                       name = "enabled", havingValue = "true")
public class VirtualThreadAutoConfiguration {

    @Bean
    public TomcatProtocolHandlerCustomizer<?> virtualThreadCustomizer() {
        return protocolHandler -> {
            // 关键: 用虚拟线程工厂替换平台线程池
            protocolHandler.setExecutor(
                Executors.newVirtualThreadPerTaskExecutor()
            );
        };
    }
}
```

### 移除冗余配置

启用虚拟线程后, 以下 Tomcat 线程池参数不再生效, 可以移除:

```yaml
# 删除 — 虚拟线程模式下这些配置无意义
server:
  tomcat:
    threads:
      max: 200        # 删除
      min-spare: 20   # 删除
```

### 初步测试

```bash
# 启动应用后观察线程
jcmd <pid> Thread.dump_to_file -format=json threads.json

# 确认虚拟线程在工作
cat threads.json | python3 -m json.tool | grep -c "virtual"
# 预期输出: 大量虚拟线程
```

启动后看起来一切正常——直到压力测试开始。

---

## 踩坑 1: HikariCP 连接池耗尽

### 问题现象

启用虚拟线程后, 压测 5 分钟内出现大量异常:

```
java.sql.SQLTransientConnectionException:
  HikariPool-1 - Connection is not available,
  request timed out after 30000ms.
```

同时观察到 (示意数据):

```
# 监控指标快照
hikari_connections_active:     50/50 (100% 占满)
hikari_connections_pending:    1,847 (大量等待)
tomcat_threads_current:        不适用 (虚拟线程无上限)
http_server_requests_active:   2,100+ (同时处理的请求)
```

### 根因分析

**迁移前**: Tomcat 最多 200 个线程, 即使所有线程同时查数据库, 50 个连接池也能在
合理时间内轮转服务完毕。线程池大小天然起到了限流的作用。

**迁移后**: 虚拟线程没有上限, 高峰期瞬间涌入 2000+ 并发请求, 全部尝试获取数据库
连接。50 个连接池被瞬间占满, 剩余 1950 个虚拟线程全部阻塞在等待连接上。

```
迁移前:  200 线程 → 50 连接 → 比例 4:1, 可控
迁移后: 2000+ 虚拟线程 → 50 连接 → 比例 40:1, 连接池成为瓶颈
```

这是虚拟线程迁移中最常见的问题: **虚拟线程移除了线程数的天花板,
暴露了下游资源的真实容量限制**。

### 解决方案: 使用 Semaphore 限流

```java
/**
 * 通过 Semaphore 限制同时访问数据库的虚拟线程数量。
 * permits 应略小于连接池大小, 为连接池维护任务预留余量。
 */
@Configuration
public class DatabaseThrottleConfig {

    // 连接池 50, Semaphore 设为 40, 预留 10 个连接给后台任务
    // (示意数据, 实际值需根据业务调优)
    private static final int DB_ACCESS_PERMITS = 40;

    @Bean
    public Semaphore databaseAccessSemaphore() {
        return new Semaphore(DB_ACCESS_PERMITS, true); // fair=true 防止饥饿
    }
}
```

封装为可复用的切面:

```java
@Aspect
@Component
public class DatabaseThrottleAspect {

    @Autowired
    private Semaphore databaseAccessSemaphore;

    /**
     * 拦截所有 Repository 方法, 在进入前获取许可。
     * 这确保同时执行数据库操作的虚拟线程数不超过 Semaphore 的 permits。
     */
    @Around("execution(* com.example..repository.*.*(..))")
    public Object throttle(ProceedingJoinPoint joinPoint) throws Throwable {
        boolean acquired = databaseAccessSemaphore.tryAcquire(5, TimeUnit.SECONDS);
        if (!acquired) {
            throw new ServiceUnavailableException(
                "Database access throttled — too many concurrent requests");
        }
        try {
            return joinPoint.proceed();
        } finally {
            databaseAccessSemaphore.release();
        }
    }
}
```

或者, 如果不想用 AOP, 可以在 Service 层显式控制:

```java
// Before: 无限流, 虚拟线程直接打满连接池
public Order findOrder(String id) {
    return orderRepository.findById(id)
            .orElseThrow(() -> new OrderNotFoundException(id));
}

// After: Semaphore 限流
private final Semaphore dbSemaphore = new Semaphore(40, true);

public Order findOrder(String id) throws InterruptedException {
    dbSemaphore.acquire();
    try {
        return orderRepository.findById(id)
                .orElseThrow(() -> new OrderNotFoundException(id));
    } finally {
        dbSemaphore.release();
    }
}
```

### 修复后的监控指标 (示意数据)

```
# 修复后的监控指标快照
hikari_connections_active:     35/50 (70%, 健康水位)
hikari_connections_pending:    5 (极少等待)
db_semaphore_available:        5/40 (高峰期仍有余量)
http_server_requests_active:   2,100+ (并发不受影响)
```

### 补充: 也可以调大连接池吗?

可以, 但需要综合考虑:

```yaml
spring:
  datasource:
    hikari:
      # 不建议盲目增大 — 数据库端也有连接上限
      # PostgreSQL 默认 max_connections=100, 需要协调
      maximum-pool-size: 50  # 保持不变, 用 Semaphore 限流更灵活
```

数据库连接是昂贵的服务端资源, Semaphore 允许在应用层做精细控制,
而不依赖数据库端的配置调整。

---

## 踩坑 2: synchronized 导致载体线程 Pinning

### 问题现象

在 JDK 21 环境下, 应用运行一段时间后出现周期性延迟抖动:

```
# JFR 事件中出现大量 jdk.VirtualThreadPinned 事件 (示意数据)
jdk.VirtualThreadPinned {
  startTime = 2025-01-15T10:23:45.123
  duration = 245 ms
  carrierThread = "ForkJoinPool-1-worker-3"
}
```

JVM 日志中出现 pinning 警告:

```bash
# 启用 pinning 检测
java -Djdk.tracePinnedThreads=short ...

# 输出:
Thread[#38,ForkJoinPool-1-worker-3] pinned while holding monitor
    at com.example.service.CacheService.getOrLoad(CacheService.java:42)
    at com.example.service.OrderService.getOrderDetail(OrderService.java:28)
```

### 根因分析

问题代码:

```java
public class CacheService {

    private final Map<String, Object> localCache = new HashMap<>();

    /**
     * 问题: synchronized 块内执行了数据库查询。
     * 在 JDK 21-23 中, 虚拟线程在 synchronized 块内无法从载体线程卸载 (unmount),
     * 导致载体线程被 "钉住" (pinned)。
     * 如果数据库查询耗时 200ms, 载体线程就被白白占用 200ms。
     */
    public synchronized Object getOrLoad(String key) {
        Object value = localCache.get(key);
        if (value == null) {
            // 这里触发数据库 I/O — 在 synchronized 块内!
            value = repository.findByKey(key);      // <-- pinning 点
            localCache.put(key, value);
        }
        return value;
    }
}
```

Pinning 的机制:

```
正常情况 (无 synchronized):
  虚拟线程 → 阻塞 I/O → 从载体线程卸载 → 载体线程服务其他虚拟线程

Pinning 情况 (synchronized + I/O):
  虚拟线程 → 进入 synchronized → 阻塞 I/O → 无法卸载 → 载体线程被占用
  其他虚拟线程无法使用该载体线程, ForkJoinPool 吞吐量下降
```

### 解决方案 A: 替换为 ReentrantLock (JDK 21-23)

```java
// Before: synchronized 导致 pinning
public class CacheService {

    private final Map<String, Object> localCache = new HashMap<>();

    public synchronized Object getOrLoad(String key) {
        Object value = localCache.get(key);
        if (value == null) {
            value = repository.findByKey(key);  // pinning!
            localCache.put(key, value);
        }
        return value;
    }
}

// After: ReentrantLock 允许虚拟线程正常卸载
public class CacheService {

    private final Map<String, Object> localCache = new HashMap<>();
    private final ReentrantLock lock = new ReentrantLock();

    public Object getOrLoad(String key) {
        lock.lock();
        try {
            Object value = localCache.get(key);
            if (value == null) {
                value = repository.findByKey(key);  // 虚拟线程可正常卸载
                localCache.put(key, value);
            }
            return value;
        } finally {
            lock.unlock();
        }
    }
}
```

### 解决方案 B: 升级到 JDK 24+ (根本解决)

从 JDK 24 开始 (JEP 491), `synchronized` 不再导致虚拟线程 pinning。
JVM 内部重新实现了 monitor 机制, 允许虚拟线程在持有 monitor 时从载体线程卸载。

```yaml
# 如果能升级到 JDK 24+, pinning 问题自动消失
# 无需修改任何 synchronized 代码
```

### 解决方案 C: 缩小 synchronized 范围

如果暂时无法替换锁或升级 JDK, 将 I/O 操作移出 synchronized 块:

```java
public Object getOrLoad(String key) {
    // 先在 synchronized 块内检查缓存 (纯内存操作, 极快)
    synchronized (this) {
        Object value = localCache.get(key);
        if (value != null) {
            return value;
        }
    }

    // I/O 操作放在 synchronized 块外
    Object loaded = repository.findByKey(key);

    // 再进入 synchronized 块写缓存 (纯内存操作)
    synchronized (this) {
        localCache.putIfAbsent(key, loaded);
        return localCache.get(key);
    }
}
```

注意: 方案 C 可能导致同一个 key 的并发查询重复加载, 需根据业务容忍度决定。

### 批量排查 synchronized + I/O 的脚本

```bash
#!/bin/bash
# 查找 synchronized 方法或块, 手动检查其中是否包含 I/O
grep -rn "synchronized" src/main/java/ \
  --include="*.java" \
  -l | while read file; do
    echo "=== $file ==="
    grep -n "synchronized\|repository\.\|template\.\|Client\." "$file"
    echo ""
done
```

### 不同 JDK 版本的 Pinning 行为对比

| JDK 版本 | synchronized + I/O | ReentrantLock + I/O | 建议                   |
|---------|--------------------|---------------------|------------------------|
| 21      | Pinning            | 正常卸载             | 替换为 ReentrantLock    |
| 22      | Pinning            | 正常卸载             | 替换为 ReentrantLock    |
| 23      | Pinning            | 正常卸载             | 替换为 ReentrantLock    |
| 24      | 正常卸载           | 正常卸载             | 无需改动               |
| 25      | 正常卸载           | 正常卸载             | 无需改动               |

---

## 踩坑 3: ThreadLocal 内存膨胀

### 问题现象

启用虚拟线程数天后, 应用内存持续增长, 最终触发 OOM:

```
java.lang.OutOfMemoryError: Java heap space

# GC 日志中观察到 (示意数据)
[GC (Allocation Failure) -- old generation occupancy:
  ThreadLocal entries: ~850MB (占堆的 65%)]
```

Heap dump 分析显示大量 `ThreadLocal.ThreadLocalMap.Entry` 对象。

### 根因分析

问题代码:

```java
public class RequestContextHolder {

    // 每个线程独立的请求上下文
    private static final ThreadLocal<RequestContext> CONTEXT =
        new ThreadLocal<>();

    public static void set(RequestContext ctx) {
        CONTEXT.set(ctx);
    }

    public static RequestContext get() {
        return CONTEXT.get();
    }

    public static void clear() {
        CONTEXT.remove();
    }
}
```

```java
public class AuditLogger {

    // 另一个 ThreadLocal: 审计上下文
    private static final ThreadLocal<AuditContext> AUDIT =
        ThreadLocal.withInitial(AuditContext::new);
    // ...
}
```

**迁移前**: 200 个平台线程 × 每线程几个 ThreadLocal 对象 = 内存可控。
平台线程会被复用, ThreadLocal 跟随线程生命周期。

**迁移后**: 虚拟线程按请求创建, 百万级请求 = 百万级虚拟线程,
每个虚拟线程携带独立的 ThreadLocal 副本。虽然虚拟线程结束后会被 GC 回收,
但如果创建速度大于回收速度, 内存就会膨胀。

```
迁移前: 200 线程 × 3 个 ThreadLocal × 1KB = ~600KB
迁移后: 高峰期 50,000 并发虚拟线程 × 3 个 ThreadLocal × 1KB = ~150MB
       (示意数据, 实际取决于 ThreadLocal 中存储的对象大小)
```

更严重的是, 如果某些 ThreadLocal 没有正确调用 `remove()`, 就会一直
持有引用直到虚拟线程被 GC 回收。

### 解决方案: 迁移到 ScopedValue (JDK 21+ preview, JDK 25 正式)

`ScopedValue` 是为虚拟线程设计的 `ThreadLocal` 替代品:

- 不可变 (immutable) — 一旦绑定就不能修改, 避免了意外的共享状态
- 自动清理 — 作用域结束后值自动失效, 无需手动 `remove()`
- 内存高效 — 不在每个线程中存储副本, 而是通过作用域链查找

```java
// Before: ThreadLocal — 需要手动管理生命周期
public class RequestContextHolder {

    private static final ThreadLocal<RequestContext> CONTEXT =
        new ThreadLocal<>();

    public static void set(RequestContext ctx) {
        CONTEXT.set(ctx);
    }

    public static RequestContext get() {
        return CONTEXT.get();
    }

    public static void clear() {
        CONTEXT.remove();  // 容易忘记调用
    }
}

// 使用方式
public void handleRequest(HttpServletRequest request) {
    RequestContext ctx = buildContext(request);
    RequestContextHolder.set(ctx);
    try {
        processOrder(ctx.getOrderId());
    } finally {
        RequestContextHolder.clear();  // 必须手动清理
    }
}
```

```java
// After: ScopedValue — 自动管理生命周期
public class RequestContextHolder {

    // ScopedValue 声明为 static final
    public static final ScopedValue<RequestContext> CONTEXT =
        ScopedValue.newInstance();

    // 不再需要 set/get/clear 方法
}

// 使用方式
public void handleRequest(HttpServletRequest request) {
    RequestContext ctx = buildContext(request);

    // ScopedValue.where() 定义作用域, .run() 在作用域内执行
    ScopedValue.where(RequestContextHolder.CONTEXT, ctx)
        .run(() -> processOrder(ctx.getOrderId()));
    // 作用域结束, ctx 自动失效, 无需手动清理
}

// 在调用链的任意深度读取
public void processOrder(String orderId) {
    // 通过 .get() 读取当前作用域的值
    RequestContext ctx = RequestContextHolder.CONTEXT.get();
    auditLog(ctx.getUserId(), orderId);
}
```

带返回值的用法:

```java
// ScopedValue.where().call() — 用于有返回值的场景
public OrderResult handleRequest(HttpServletRequest request) {
    RequestContext ctx = buildContext(request);

    return ScopedValue.where(RequestContextHolder.CONTEXT, ctx)
        .call(() -> {
            Order order = findOrder(ctx.getOrderId());
            return processOrder(order);
        });
}
```

### 对于无法立即迁移到 ScopedValue 的代码

确保 ThreadLocal 被正确清理, 可以用 Filter 或 Interceptor 做兜底:

```java
@Component
public class ThreadLocalCleanupFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request,
                         ServletResponse response,
                         FilterChain chain) throws IOException, ServletException {
        try {
            chain.doFilter(request, response);
        } finally {
            // 兜底清理所有已知的 ThreadLocal
            RequestContextHolder.clear();
            AuditContext.clear();
            MDC.clear();
        }
    }
}
```

---

## 踩坑 4: Logback MDC 上下文丢失

### 问题现象

启用虚拟线程后, 日志中的 traceId 和 userId 间歇性丢失:

```
# 正常日志 (有 traceId)
2025-01-20 10:15:23 [traceId=abc123] [userId=user42] INFO  OrderService - 查询订单 ORD-001

# 异常日志 (MDC 丢失)
2025-01-20 10:15:24 [traceId=] [userId=] INFO  OrderService - 查询订单 ORD-002
```

### 根因分析

Logback 的 MDC (Mapped Diagnostic Context) 底层使用 `InheritableThreadLocal`。
在平台线程模型下, 子线程会继承父线程的 MDC 上下文, 而线程池复用的线程会保持
之前设置的 MDC 值。

虚拟线程的问题:

1. **不继承**: 虚拟线程默认不继承 `InheritableThreadLocal` 的值
   (通过 `Thread.Builder` 创建时可选, 但 `Executors.newVirtualThreadPerTaskExecutor()`
   默认不继承)。
2. **生命周期短**: 虚拟线程是一次性的, 无法依赖线程池复用来保持 MDC。

```java
// MDC 底层实现 (Logback)
public class LogbackMDCAdapter implements MDCAdapter {
    // 使用 InheritableThreadLocal 存储上下文
    final InheritableThreadLocal<Map<String, String>> copyOnInheritThreadLocal =
        new InheritableThreadLocal<>();
    // ...
}
```

### 解决方案 A: 使用 Filter 在每个请求入口设置 MDC

既然无法依赖线程继承, 就在每个请求的入口显式设置 MDC:

```java
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class MdcFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request,
                         ServletResponse response,
                         FilterChain chain) throws IOException, ServletException {
        HttpServletRequest httpRequest = (HttpServletRequest) request;

        try {
            // 从 Header 中提取 traceId, 或生成新的
            String traceId = httpRequest.getHeader("X-Trace-Id");
            if (traceId == null || traceId.isBlank()) {
                traceId = UUID.randomUUID().toString().substring(0, 8);
            }

            MDC.put("traceId", traceId);
            MDC.put("userId", extractUserId(httpRequest));

            chain.doFilter(request, response);
        } finally {
            MDC.clear();
        }
    }
}
```

但这只解决了请求入口的问题。如果 Service 层又创建新的虚拟线程做并行处理,
新线程中的 MDC 仍然是空的。

### 解决方案 B: 用 ScopedValue 替代 MDC (推荐)

```java
// 定义 ScopedValue 版的 TraceContext
public class TraceContext {

    public static final ScopedValue<TraceInfo> TRACE =
        ScopedValue.newInstance();

    public record TraceInfo(String traceId, String userId) {}
}
```

```java
// Filter 中绑定 ScopedValue
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class TraceFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request,
                         ServletResponse response,
                         FilterChain chain) throws IOException, ServletException {
        HttpServletRequest httpRequest = (HttpServletRequest) request;

        String traceId = resolveTraceId(httpRequest);
        String userId = extractUserId(httpRequest);
        TraceInfo info = new TraceInfo(traceId, userId);

        // 整个请求处理链都能通过 TraceContext.TRACE.get() 获取
        ScopedValue.where(TraceContext.TRACE, info)
            .run(() -> {
                try {
                    chain.doFilter(request, response);
                } catch (IOException | ServletException e) {
                    throw new RuntimeException(e);
                }
            });
    }
}
```

```java
// 自定义 Logback Layout, 从 ScopedValue 读取 traceId
public class ScopedValuePatternLayout extends PatternLayout {

    @Override
    public String doLayout(ILoggingEvent event) {
        // 在格式化日志时从 ScopedValue 取值
        String traceId = TraceContext.TRACE.isBound()
            ? TraceContext.TRACE.get().traceId()
            : "N/A";
        // 注入到 MDC 中供 pattern 使用
        event.getMDCPropertyMap().put("traceId", traceId);
        return super.doLayout(event);
    }
}
```

### 解决方案 C: 使用 StructuredTaskScope 自动传播

当在 Service 层创建并行子任务时, 使用 `StructuredTaskScope` 可以让子任务
自动继承父任务的 ScopedValue:

```java
// ScopedValue 在 StructuredTaskScope 中自动传播
public OrderDetailDTO getOrderDetail(String orderId) {
    // 父任务中 TraceContext.TRACE 已绑定
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {

        // 子任务自动继承 ScopedValue — 无需手动传递
        Subtask<Order> orderTask = scope.fork(() -> {
            // TraceContext.TRACE.get() 在这里可用!
            return orderRepository.findById(orderId).orElseThrow();
        });

        Subtask<InventoryInfo> inventoryTask = scope.fork(() -> {
            // 这里也可用!
            return inventoryClient.getInventory(orderId);
        });

        scope.join().throwIfFailed();
        return toDTO(orderTask.get(), inventoryTask.get());
    }
}
```

---

## 最终配置与调优

### application.yml (迁移后)

```yaml
# application.yml — 虚拟线程模式 (示意配置)
spring:
  threads:
    virtual:
      enabled: true

  datasource:
    hikari:
      maximum-pool-size: 50           # 保持不变
      minimum-idle: 10
      connection-timeout: 5000        # 缩短超时, 配合 Semaphore 使用
      leak-detection-threshold: 10000 # 开启连接泄漏检测

  data:
    redis:
      lettuce:
        pool:
          max-active: 50              # Redis 连接池也需要关注
          max-idle: 20
          min-idle: 5

# Tomcat 线程池配置已移除 — 虚拟线程模式下不需要
server:
  tomcat:
    accept-count: 200
    max-connections: 10000            # 可适当调大, 虚拟线程能处理更多并发
```

### JVM 启动参数

```bash
# 最终 JVM 参数 (示意配置)
java \
  # 基础内存配置
  -Xms1g -Xmx4g \
  -XX:+UseZGC \
  -XX:+ZGenerational \
  \
  # 虚拟线程相关诊断
  -Djdk.tracePinnedThreads=short \
  \
  # JFR 持续监控
  -XX:StartFlightRecording=name=continuous,settings=default,maxsize=256m,dumponexit=true \
  \
  # 如果使用 JDK 21-23 且有 preview 特性
  # --enable-preview \
  \
  -jar app.jar
```

### 关于 ZGC 的选择

虚拟线程场景下推荐使用 ZGC (Generational):

- 虚拟线程频繁创建和销毁, 产生大量短生命周期对象
- ZGC 的低延迟特性与虚拟线程的高并发模型互补
- Generational 模式 (JDK 21+) 对短生命周期对象回收更高效

```bash
# 不推荐 G1 的原因 (示意数据):
# G1:  P99 GC pause ~15ms, 偶尔 ~50ms — 在 2000 并发下会被放大
# ZGC: P99 GC pause ~1ms,  最差 ~3ms — 对高并发场景更友好
```

### 自定义线程池的处理

迁移前的自定义线程池应逐步替换:

```java
// Before: 自定义平台线程池
@Configuration
public class AsyncConfig {

    @Bean("taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(20);
        executor.setMaxPoolSize(50);
        executor.setQueueCapacity(500);
        executor.setThreadNamePrefix("async-");
        executor.initialize();
        return executor;
    }
}

// After: 替换为虚拟线程执行器
@Configuration
public class AsyncConfig {

    @Bean("taskExecutor")
    public Executor taskExecutor() {
        // 每个任务一个虚拟线程, 无需配置池大小
        return Executors.newVirtualThreadPerTaskExecutor();
    }
}
```

---

## 迁移效果总结

### 性能指标对比 (示意数据)

| 指标                    | 迁移前 (平台线程) | 迁移后 (虚拟线程) | 变化        |
|------------------------|--------------------|--------------------|-----------:|
| 最大并发处理数           | 200                | 5,000+             | 25x        |
| 吞吐量 (req/s)         | 1,200              | 2,500              | **+108%**  |
| P50 延迟 (ms)           | 45                 | 42                 | -7%        |
| P99 延迟 (ms)           | 320                | 128                | **-60%**   |
| P999 延迟 (ms)          | 1,200              | 350                | -71%       |
| 平台线程数               | ~270               | ~20 (载体线程)     | -93%       |
| 线程栈内存占用           | ~270MB             | ~20MB + 虚拟线程栈  | 大幅降低   |
| 排队等待时间 (avg, ms)   | 85                 | 3                  | -96%       |

### 延迟分布变化 (示意数据)

```
迁移前 P99 延迟分布:
  0-50ms   ████████████████████ 52%
  50-100ms ████████             20%
  100-200ms ██████              15%
  200-500ms ████                10%
  500ms+    █                    3%

迁移后 P99 延迟分布:
  0-50ms   ██████████████████████████ 65%
  50-100ms ██████████                 25%
  100-200ms ███                        8%
  200-500ms █                          2%
  500ms+                              <1%
```

### 为什么 P50 延迟几乎不变?

P50 (中位数) 反映的是正常负载下单次请求的处理时间。虚拟线程不会让
数据库查询本身变快, 它改善的是**排队等待时间**。

- P50 不变: 请求本身的 I/O 时间不变
- P99 大幅改善: 高并发时不再因线程池满而排队
- 吞吐量翻倍: 同样的硬件能同时处理更多请求

### 资源使用变化 (示意数据)

```
迁移前:
  CPU 使用率: 平均 35%, 峰值 70% (大量时间在等线程调度)
  内存使用:   2.8GB (线程栈占 270MB)
  GC 频率:   Young GC 12次/分钟, Full GC 偶发

迁移后:
  CPU 使用率: 平均 45%, 峰值 65% (CPU 利用更充分)
  内存使用:   2.1GB (线程栈内存大幅减少)
  GC 频率:   ZGC pause <1ms, 持续低延迟
```

---

## 决策指南: 哪些场景不适合虚拟线程

虚拟线程不是万能的。以下场景应继续使用平台线程:

### 1. CPU 密集型计算

```java
// 不适合: 纯 CPU 计算, 没有 I/O 阻塞点
// 虚拟线程无法提升 CPU 密集型任务的性能, 反而增加调度开销
public BigDecimal calculateRiskScore(Portfolio portfolio) {
    // 大量数学计算, 没有 I/O
    return portfolio.getPositions().stream()
        .map(this::computeVaR)       // 纯计算
        .reduce(BigDecimal.ZERO, BigDecimal::add);
}

// 建议: 继续使用 ForkJoinPool 或固定大小的平台线程池
ExecutorService cpuPool = Executors.newFixedThreadPool(
    Runtime.getRuntime().availableProcessors()
);
```

### 2. 需要精确控制并发度的场景

```java
// 不适合: 需要严格限制并发的任务 (如批量导入)
// 虚拟线程没有内置的队列和拒绝策略
// 如果使用虚拟线程, 必须额外加 Semaphore 控制

// 建议: 继续使用 ThreadPoolTaskExecutor, 利用其队列和拒绝策略
ThreadPoolTaskExecutor batchExecutor = new ThreadPoolTaskExecutor();
batchExecutor.setCorePoolSize(4);
batchExecutor.setMaxPoolSize(4);  // 严格限制
batchExecutor.setQueueCapacity(1000);
batchExecutor.setRejectedExecutionHandler(new CallerRunsPolicy());
```

### 3. 依赖线程身份的场景

```java
// 不适合: 代码依赖 Thread 对象的身份或优先级
// 虚拟线程不支持 setPriority(), 也不应该用 Thread 身份做业务逻辑

// 例如: 使用 ThreadGroup 做隔离
// 例如: 使用 Thread.getId() 做分片
```

### 4. 使用了不兼容的本地库 (JNI/FFM)

```java
// 不适合: 通过 JNI 调用的本地代码可能假设平台线程
// 某些 native 库使用 thread-local storage (TLS), 与虚拟线程不兼容
```

### 5. 使用了大量 synchronized 且无法修改的第三方库 (JDK < 24)

```java
// 不适合 (JDK 21-23): 如果核心依赖库大量使用 synchronized + I/O
// 例如某些旧版 JDBC 驱动, 旧版 HTTP 客户端
// JDK 24+ 后此限制解除
```

### 决策流程图

```
你的工作负载是什么类型?
│
├── I/O 密集型 (数据库/HTTP/文件)
│   ├── 使用 JDK 24+? → 直接启用虚拟线程
│   └── 使用 JDK 21-23?
│       ├── 有 synchronized + I/O? → 先替换为 ReentrantLock, 再启用
│       └── 无 synchronized 问题? → 直接启用
│
├── CPU 密集型 → 继续使用平台线程池
│
├── 混合型
│   ├── I/O 部分 → 虚拟线程
│   └── CPU 部分 → 平台线程池
│
└── 不确定 → 先用 JFR 分析线程阻塞情况
```

---

## 迁移检查清单

以下是虚拟线程迁移的完整检查清单:

### 迁移前

- [ ] 使用 JFR 或 `jstack` 分析当前线程阻塞模式, 确认以 I/O 阻塞为主
- [ ] 统计所有 `synchronized` 块/方法, 标记其中包含 I/O 调用的位置
- [ ] 统计所有 `ThreadLocal` / `InheritableThreadLocal` 使用点
- [ ] 检查第三方库的虚拟线程兼容性 (特别是 JDBC 驱动, HTTP 客户端)
- [ ] 确认数据库连接池大小和数据库端 `max_connections` 的配比
- [ ] 确认 Redis 连接池配置

### 迁移中

- [ ] 设置 `spring.threads.virtual.enabled=true`
- [ ] 移除 Tomcat 线程池大小配置 (`server.tomcat.threads.*`)
- [ ] 为数据库访问层添加 Semaphore 限流
- [ ] 将 `synchronized` + I/O 替换为 `ReentrantLock` (JDK < 24)
- [ ] 将 `ThreadLocal` 迁移到 `ScopedValue` 或确保正确清理
- [ ] 处理 MDC 上下文传播
- [ ] 替换自定义平台线程池为虚拟线程执行器 (仅 I/O 密集型任务)

### 迁移后

- [ ] 使用 `-Djdk.tracePinnedThreads=short` 验证无 pinning (JDK < 24)
- [ ] 使用 JFR 监控 `jdk.VirtualThreadPinned` 事件
- [ ] 压测验证吞吐量和延迟改善
- [ ] 监控连接池使用率 (HikariCP, Redis)
- [ ] 监控内存使用, 排查 ThreadLocal 泄漏
- [ ] 验证日志中的 traceId 等上下文信息完整
- [ ] 验证 GC 行为, 考虑切换到 ZGC

---

> **总结**: 虚拟线程迁移的核心不是"开启开关"本身, 而是识别和处理虚拟线程暴露出来的
> 下游资源瓶颈 (连接池)、锁兼容性 (pinning)、和线程局部状态管理 (ThreadLocal/MDC)。
> 做好这三方面的准备, 迁移过程就是顺畅的。
