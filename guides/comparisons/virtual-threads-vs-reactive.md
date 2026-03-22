# Virtual Threads vs Reactive: 并发编程模型全面对比

> **一句话总结**: Virtual Threads 让你用简单的同步代码获得异步的扩展性;
> Reactive 提供强大的流处理能力但代码复杂度高. 对于大多数新项目, Virtual Threads 是更好的选择.

---

## 目录

1. [编程模型对比](#编程模型对比)
2. [代码复杂度对比](#代码复杂度对比)
3. [性能对比](#性能对比)
4. [调试与可观测性](#调试与可观测性)
5. [生态系统对比](#生态系统对比)
6. [何时仍需 Reactive](#何时仍需-reactive)
7. [迁移路径: WebFlux → Virtual Threads](#迁移路径)
8. [结论与推荐](#结论与推荐)

---

## 编程模型对比

### Virtual Threads: 同步阻塞 (Synchronous Blocking)

Virtual Threads (虚拟线程, JEP 444, JDK 21) 是轻量级线程, 由 JVM 调度而非 OS.
代码风格与传统线程相同 — **同步、阻塞、顺序执行** — 但可以创建数百万个.

```
Platform Thread (OS 线程):         Virtual Thread (虚拟线程):
┌──────────────────────┐          ┌──────────────────────┐
│ OS Thread (1:1)      │          │ Virtual Thread (M:N) │
│ Stack: 1MB           │          │ Stack: ~几 KB (按需)  │
│ 创建成本: 高          │          │ 创建成本: 极低        │
│ 数量上限: ~数千       │          │ 数量上限: 数百万      │
└──────────────────────┘          └──────────────────────┘
                                    ↓ mounted on
                                  ┌──────────────────────┐
                                  │ Carrier Thread (载体) │
                                  │ (ForkJoinPool)        │
                                  └──────────────────────┘
```

### Reactive: 异步非阻塞 (Asynchronous Non-Blocking)

Reactive (响应式) 基于事件循环和回调链. Project Reactor / RxJava 使用 `Mono`/`Flux`
包装异步操作, 通过 operator chaining 组合.

```
Event Loop Model:
┌─────────────────────────────────────┐
│ Event Loop Thread (少量, 如 4 个)    │
│                                     │
│  ┌──► handle request               │
│  │    ├── non-blocking DB call ──►  │──► callback when ready
│  │    ├── non-blocking HTTP call ►  │──► callback when ready
│  │    └── compose results           │
│  └── next event                     │
└─────────────────────────────────────┘
  ⚠️ 绝不能阻塞 Event Loop 线程!
```

### 核心差异总结

| 方面                  | Virtual Threads              | Reactive (WebFlux/Reactor)     |
|----------------------|------------------------------|--------------------------------|
| **代码风格**          | 同步阻塞 (synchronous)       | 异步链式 (operator chaining)    |
| **心智模型**          | 一个请求一个线程             | 事件驱动, 回调/信号             |
| **阻塞操作**          | 安全阻塞 (VT 自动 unmount)   | 绝不允许阻塞                   |
| **学习曲线**          | 低 (与传统 Java 相同)        | 高 (需掌握 Reactive 范式)       |
| **错误处理**          | try-catch                    | onErrorResume / onErrorMap     |
| **栈跟踪**            | 完整, 可读                   | 碎片化, 难以追踪               |
| **底层机制**          | JVM 级调度 (continuation)    | 库级别 (Reactor/RxJava)        |

---

## 代码复杂度对比

### 场景: 查询用户 → 获取订单 → 获取支付信息 → 组装响应

#### Virtual Threads (Spring MVC + VT)

```java
// 简洁、直观、可读性强
@GetMapping("/users/{id}/summary")
public UserSummary getUserSummary(@PathVariable Long id) {
    // 顺序执行, 每步阻塞 — 但 Virtual Thread 使其高效
    User user = userService.findById(id);                    // blocking I/O
    List<Order> orders = orderService.findByUserId(id);      // blocking I/O
    PaymentInfo payment = paymentService.getInfo(id);        // blocking I/O

    return new UserSummary(user, orders, payment);
}

// 需要并发? 用 StructuredTaskScope (JEP 480, JDK 23 preview)
@GetMapping("/users/{id}/summary")
public UserSummary getUserSummaryConcurrent(@PathVariable Long id) {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        Subtask<User> userTask = scope.fork(() -> userService.findById(id));
        Subtask<List<Order>> ordersTask = scope.fork(() -> orderService.findByUserId(id));
        Subtask<PaymentInfo> paymentTask = scope.fork(() -> paymentService.getInfo(id));

        scope.join().throwIfFailed();

        return new UserSummary(userTask.get(), ordersTask.get(), paymentTask.get());
    }
}
```

#### Reactive (Spring WebFlux + Reactor)

```java
// 链式操作, 需要理解 Mono/Flux 语义
@GetMapping("/users/{id}/summary")
public Mono<UserSummary> getUserSummary(@PathVariable Long id) {
    return userService.findById(id)                          // returns Mono<User>
        .flatMap(user ->
            Mono.zip(
                orderService.findByUserId(id),               // returns Mono<List<Order>>
                paymentService.getInfo(id)                   // returns Mono<PaymentInfo>
            ).map(tuple -> new UserSummary(user, tuple.getT1(), tuple.getT2()))
        );
}

// 错误处理更复杂
@GetMapping("/users/{id}/summary")
public Mono<UserSummary> getUserSummaryWithErrorHandling(@PathVariable Long id) {
    return userService.findById(id)
        .switchIfEmpty(Mono.error(new UserNotFoundException(id)))
        .flatMap(user ->
            Mono.zip(
                orderService.findByUserId(id)
                    .onErrorResume(e -> Mono.just(Collections.emptyList())),
                paymentService.getInfo(id)
                    .onErrorResume(e -> Mono.just(PaymentInfo.UNKNOWN))
            ).map(tuple -> new UserSummary(user, tuple.getT1(), tuple.getT2()))
        )
        .timeout(Duration.ofSeconds(5))
        .onErrorMap(TimeoutException.class, e -> new ServiceUnavailableException());
}
```

### 代码行数对比 (Lines of Code)

```
相同业务逻辑的代码量:

Virtual Threads:  [████████████]           ~12 行
Reactive:         [████████████████████████] ~24 行 (2x)

含错误处理:
Virtual Threads:  [████████████████]        ~16 行 (try-catch)
Reactive:         [████████████████████████████████] ~32 行 (2x)
```

---

## 性能对比

### 吞吐量 (Throughput)

在 I/O 密集型场景 (如 HTTP 服务调用数据库):

```
并发连接数 vs 吞吐量 (requests/sec):

连接数:    100      1,000    10,000   100,000
           │        │        │        │
Platform   ████████ ████████ ████     (线程耗尽)
Threads    8,000    8,000    4,000    OOM

Virtual    ████████ ████████ ████████ ████████
Threads    8,000    8,000    8,000    7,500

Reactive   ████████ ████████ ████████ ████████
(WebFlux)  7,800    7,800    7,800    7,500
```

> **关键发现**: Virtual Threads 和 Reactive 在高并发下吞吐量接近.
> Virtual Threads 的优势在于达到相同性能的代码复杂度远低于 Reactive.

### 延迟 (Latency)

```
p99 延迟 (ms), 10,000 并发连接:

Virtual Threads:  [████████████]        p99 = 12ms
Reactive:         [███████████]         p99 = 11ms
Platform Threads: [████████████████████████████████] p99 = 很高或直接 reject
```

两者延迟特性相近. Reactive 在极高并发下可能有微小优势 (fewer context switches).

### 内存占用 (Memory)

```
10,000 并发任务的内存占用:

Platform Threads: [████████████████████████████████] ~10 GB (1MB stack × 10K)
Virtual Threads:  [████]                             ~400 MB (动态栈)
Reactive:         [██]                               ~200 MB (无栈, 仅对象)
```

> Reactive 内存最低, 因为不需要为每个任务维护栈. Virtual Threads 的栈按需增长,
> 通常每个只有几 KB, 但仍比无栈的 Reactive 模型多.

### CPU 开销 (CPU Overhead)

| 场景           | Virtual Threads       | Reactive               |
|---------------|----------------------|------------------------|
| I/O 密集      | 低 (阻塞时自动 unmount) | 低 (event-driven)      |
| CPU 密集      | 中 (与平台线程相同)    | 需注意不阻塞 event loop |
| 混合型        | 低                    | 需手动 publishOn 切换   |

---

## 调试与可观测性

### 栈跟踪对比

#### Virtual Threads — 清晰完整

```
java.lang.RuntimeException: Payment service unavailable
    at com.example.PaymentService.getInfo(PaymentService.java:42)
    at com.example.UserController.getUserSummary(UserController.java:25)
    at java.base/java.lang.VirtualThread.run(VirtualThread.java:309)
```

#### Reactive — 碎片化, 难以定位

```
java.lang.RuntimeException: Payment service unavailable
    at com.example.PaymentService.lambda$getInfo$0(PaymentService.java:42)
    at reactor.core.publisher.MonoFlatMap$FlatMapMain.onNext(MonoFlatMap.java:125)
    at reactor.core.publisher.FluxMap$MapSubscriber.onNext(FluxMap.java:122)
    at reactor.core.publisher.MonoZip$ZipCoordinator.signal(MonoZip.java:251)
    ... 30 more lines of Reactor internals ...
```

> **调试难度**: Reactive 的栈跟踪充满框架内部调用, 需要 Reactor Debug Agent (`ReactorDebugAgent.init()`)
> 或 `Hooks.onOperatorDebug()` 来增强, 且这些工具有显著性能开销.

### 调试工具支持

| 工具               | Virtual Threads           | Reactive                    |
|-------------------|--------------------------|----------------------------|
| **IDE 断点**       | 正常工作                  | 需特殊配置, 断点位置不直观   |
| **jstack**         | 完整显示所有 VT            | 只能看到少量 event loop 线程 |
| **JFR**            | 完整支持                  | 部分支持                    |
| **分布式追踪**      | 自动 context propagation  | 需手动处理 Reactor Context   |
| **Profiler**       | 标准 profiler 支持        | 需要异步 profiler            |

### Thread Dump 对比

```bash
# Virtual Threads — jcmd 显示所有虚拟线程
jcmd <pid> Thread.dump_to_file -format=json threads.json
# 可以看到每个 VT 的状态和栈

# Reactive — 只能看到少量载体线程
# reactor-http-nio-1, reactor-http-nio-2, ...
# 看不到"请求级别"的上下文
```

---

## 生态系统对比

### Spring MVC + Virtual Threads vs Spring WebFlux

| 方面               | Spring MVC + VT              | Spring WebFlux                |
|-------------------|------------------------------|-------------------------------|
| **配置**           | `spring.threads.virtual.enabled=true` | 默认使用 Netty             |
| **Servlet 兼容**   | 完全兼容                     | 不兼容 Servlet API            |
| **JDBC**           | 直接使用                     | 需要 R2DBC (异步驱动)         |
| **JPA/Hibernate**  | 直接使用                     | 不支持 (需 Spring Data R2DBC) |
| **Redis**          | Jedis/Lettuce                | Lettuce (reactive)            |
| **HTTP Client**    | RestClient / RestTemplate    | WebClient                     |
| **Filter/拦截器**  | 标准 Servlet Filter          | WebFilter                     |
| **模板引擎**       | Thymeleaf 等                 | Thymeleaf Reactive            |
| **社区规模**       | 非常大                       | 较小                          |
| **文档/教程**      | 丰富                         | 相对较少                      |

### 数据库驱动对比

```
                    阻塞 (Virtual Threads)     非阻塞 (Reactive)
PostgreSQL:         JDBC (pgjdbc)              R2DBC (r2dbc-postgresql)
MySQL:              JDBC (Connector/J)         R2DBC (r2dbc-mysql)
MongoDB:            MongoDB Driver             MongoDB Reactive Streams
Redis:              Jedis / Lettuce            Lettuce Reactive
```

> **关键点**: JDBC 是阻塞 API, 但在 Virtual Threads 上运行完全没问题.
> R2DBC 为 Reactive 设计, 但驱动成熟度和功能不如 JDBC.

### Spring Boot 配置

```yaml
# Spring MVC + Virtual Threads (Spring Boot 3.2+)
spring:
  threads:
    virtual:
      enabled: true     # 一行搞定!

# 等效于:
# Tomcat 会为每个请求创建一个 Virtual Thread
# 无需额外配置 thread pool
```

```yaml
# Spring WebFlux — 需要完全不同的依赖和编程模型
# build.gradle:
# implementation 'org.springframework.boot:spring-boot-starter-webflux'
# (替换 spring-boot-starter-web)
```

---

## 何时仍需 Reactive

Virtual Threads 并非万能. 以下场景 Reactive 仍有优势:

### 1. 背压 (Backpressure)

当生产者速度 > 消费者速度时, Reactive Streams 提供标准化的背压机制:

```java
// Reactive — 内置背压
Flux.fromIterable(hugeDataset)
    .flatMap(item -> processAsync(item), 10)  // 并发度限制为 10
    .onBackpressureBuffer(1000)               // 缓冲 1000 个
    .subscribe();

// Virtual Threads — 需要手动实现流控
// 可以用 Semaphore, BlockingQueue 等实现, 但不如 Reactive 优雅
var semaphore = new Semaphore(10);
for (var item : hugeDataset) {
    semaphore.acquire();
    Thread.startVirtualThread(() -> {
        try {
            process(item);
        } finally {
            semaphore.release();
        }
    });
}
```

### 2. Server-Sent Events (SSE)

```java
// Reactive — 天然适合流式响应
@GetMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<ServerSentEvent<String>> stream() {
    return Flux.interval(Duration.ofSeconds(1))
        .map(i -> ServerSentEvent.builder("event-" + i).build());
}

// Virtual Threads — 也可以, 但需要手动管理
@GetMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public SseEmitter stream() {
    var emitter = new SseEmitter();
    Thread.startVirtualThread(() -> {
        try {
            for (int i = 0; ; i++) {
                emitter.send("event-" + i);
                Thread.sleep(Duration.ofSeconds(1));
            }
        } catch (Exception e) {
            emitter.completeWithError(e);
        }
    });
    return emitter;
}
```

### 3. 复杂的流处理 (Stream Processing)

```java
// Reactive — 丰富的操作符
Flux.from(kafkaConsumer)
    .bufferTimeout(100, Duration.ofMillis(500))
    .flatMap(batch -> processBatch(batch))
    .retry(3)
    .onErrorContinue((e, o) -> log.warn("Skipping: {}", o, e))
    .subscribe();
```

### 4. WebSocket

Reactive 对 WebSocket 的双向流支持更自然, 因为 WebSocket 本质是双向流.

### 适用场景总结

```
                    Virtual Threads 更好        Reactive 更好
                    ────────────────────        ─────────────
CRUD API:           ████████████████████
微服务间调用:        ████████████████████
批处理:             ████████████████████
数据流处理:                                     ████████████████████
背压场景:                                       ████████████████████
SSE/WebSocket:                                  ██████████████
既有 Servlet 应用:   ████████████████████
新项目 (一般):       ████████████████████
```

---

## 迁移路径

### WebFlux → Virtual Threads 迁移步骤

#### Step 1: 评估可行性

```
检查清单:
☐ 不依赖 Reactive 特有功能 (背压/SSE)?
☐ 可以切换到 JDBC (从 R2DBC)?
☐ 使用 JDK 21+?
☐ Spring Boot 3.2+?
```

#### Step 2: 依赖替换

```xml
<!-- 移除 -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webflux</artifactId>
</dependency>
<dependency>
    <groupId>io.r2dbc</groupId>
    <artifactId>r2dbc-postgresql</artifactId>
</dependency>

<!-- 添加 -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
</dependency>
```

#### Step 3: 启用 Virtual Threads

```yaml
spring:
  threads:
    virtual:
      enabled: true
```

#### Step 4: 代码迁移

```java
// BEFORE: Reactive
@GetMapping("/users/{id}")
public Mono<User> getUser(@PathVariable Long id) {
    return userRepository.findById(id)                    // R2DBC
        .switchIfEmpty(Mono.error(new NotFoundException()))
        .flatMap(user ->
            enrichmentService.enrich(user)                // Reactive call
                .onErrorResume(e -> Mono.just(user))
        );
}

// AFTER: Virtual Threads
@GetMapping("/users/{id}")
public User getUser(@PathVariable Long id) {
    User user = userRepository.findById(id)               // JPA/JDBC
        .orElseThrow(NotFoundException::new);
    try {
        return enrichmentService.enrich(user);            // Blocking call
    } catch (Exception e) {
        return user;                                      // Fallback
    }
}
```

#### Step 5: WebClient → RestClient

```java
// BEFORE: WebClient (Reactive)
Mono<Order> order = webClient.get()
    .uri("/orders/{id}", orderId)
    .retrieve()
    .bodyToMono(Order.class);

// AFTER: RestClient (Synchronous, Spring 6.1+)
Order order = restClient.get()
    .uri("/orders/{id}", orderId)
    .retrieve()
    .body(Order.class);
```

#### 迁移注意事项

1. **pinning 问题**: `synchronized` 块会 pin Virtual Thread 到 carrier thread.
   改用 `ReentrantLock`:
   ```java
   // 避免 — 会导致 pinning
   synchronized (lock) {
       jdbcCall();
   }

   // 推荐 — VT-friendly
   private final ReentrantLock lock = new ReentrantLock();
   lock.lock();
   try {
       jdbcCall();
   } finally {
       lock.unlock();
   }
   ```

2. **ThreadLocal 注意**: Virtual Threads 数量巨大, 过多 ThreadLocal 会消耗大量内存.
   考虑使用 Scoped Values (JEP 487):
   ```java
   // 避免 — 百万 VT 各自持有 ThreadLocal 副本
   private static final ThreadLocal<User> CURRENT_USER = new ThreadLocal<>();

   // 推荐 — Scoped Value (JDK 23+ preview)
   private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();
   ScopedValue.where(CURRENT_USER, user).run(() -> handleRequest());
   ```

3. **连接池仍然需要**: Virtual Threads 不消除对连接池的需求. 数据库连接是有限资源:
   ```yaml
   spring:
     datasource:
       hikari:
         maximum-pool-size: 50   # 仍然需要限制!
   ```

---

## 结论与推荐

### 决策矩阵

| 场景                              | 推荐                      | 原因                                    |
|----------------------------------|--------------------------|----------------------------------------|
| **新项目, 一般 Web 应用**          | **Virtual Threads**      | 简单、高效、生态成熟                     |
| **新项目, 数据流处理**             | **Reactive**             | 背压、流操作符是核心需求                  |
| **既有 Spring MVC 应用**           | **+ Virtual Threads**    | 一行配置, 立即获益                       |
| **既有 WebFlux 应用, 运行良好**     | **保持 Reactive**        | 没坏别修 (if it ain't broke...)         |
| **既有 WebFlux 应用, 维护困难**     | **迁移到 VT**            | 降低代码复杂度, 改善调试体验              |
| **超高并发 + 极限内存优化**         | **Reactive**             | 无栈模型内存占用最低                     |

### 最终建议

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   对于 大多数新 Java 项目:                                   │
│                                                             │
│       选择 Spring MVC + Virtual Threads                     │
│       (Spring Boot 3.2+, JDK 21+)                          │
│                                                             │
│   原因:                                                     │
│   1. 代码简单 — 同步阻塞, 人人都会                            │
│   2. 性能相当 — 吞吐量与 Reactive 持平                       │
│   3. 调试容易 — 完整栈跟踪, 标准工具                          │
│   4. 生态成熟 — JDBC, JPA, 所有库直接可用                     │
│   5. 迁移成本低 — 既有代码几乎不用改                          │
│                                                             │
│   Reactive 保留用于: 流处理 / 背压 / SSE / WebSocket          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> **行业趋势**: Spring 团队自身也在推荐 Virtual Threads 作为大多数场景的首选.
> Spring Framework 6.1 和 Spring Boot 3.2 的 Virtual Threads 支持标志着
> Java 并发编程从 "Reactive 是未来" 转向 "简单同步 + VT 是更好的默认选择".
