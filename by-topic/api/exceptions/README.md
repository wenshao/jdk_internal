# 异常处理

> Throwable、Exception、Error、异常链、try-with-resources、Helpful NPE、StackWalker 演进历程

[← 返回 API 框架](../)

---

## 1. 快速概览

```
JDK 1.0 ── JDK 1.4 ── JDK 7 ── JDK 9 ── JDK 14 ── JDK 19+ ── JDK 21
   │         │        │        │        │         │          │
异常体系   异常链   try-with  StackWalker Helpful  switch    Virtual
Throwable  getCause  resources (JEP 259)  NPE     exhaust.  Thread
Error/Exc  initCause 多捕获               (JEP 358)         异常传播
```

### 核心演进

| 版本 | 特性 | JEP | 说明 |
|------|------|-----|------|
| **JDK 1.0** | Throwable/Error/Exception | - | 异常体系基础 |
| **JDK 1.4** | 异常链 (chained exceptions) | - | getCause(), initCause() |
| **JDK 7** | try-with-resources | - | 自动资源管理, suppressed exceptions |
| **JDK 7** | multi-catch | - | catch (A \| B e) |
| **JDK 7** | 精确异常重抛 (precise rethrow) | - | final 重抛类型推断 |
| **JDK 9** | StackWalker | JEP 259 | 惰性栈遍历 API |
| **JDK 14** | Helpful NullPointerException | JEP 358 | 详细空指针消息 |
| **JDK 21** | StructuredTaskScope | JEP 453 | 结构化并发异常传播 |

---

## 目录

- [异常层次结构](#2-异常层次结构)
- [Helpful NullPointerException](#3-helpful-nullpointerexception-jdk-14)
- [try-with-resources 与 Suppressed Exceptions](#4-try-with-resources-与-suppressed-exceptions)
- [异常链](#5-异常链)
- [StackWalker API](#6-stackwalker-api-jdk-9)
- [异常性能](#7-异常性能)
- [常见陷阱](#8-常见陷阱)
- [Pattern Matching 与异常](#9-pattern-matching-与异常)
- [Virtual Thread 异常传播](#10-virtual-thread-异常传播)
- [最佳实践](#11-最佳实践)
- [核心贡献者](#12-核心贡献者)
- [相关链接](#13-相关链接)

---

## 2. 异常层次结构

### Throwable 继承树 (Exception Hierarchy)

```
                    ┌─────────────────┐
                    │   Throwable     │
                    ├─────────────────┤
                    │ - message       │
                    │ - cause         │
                    │ - stackTrace    │
                    │ - suppressed[]  │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
     ┌────────▼────────┐          ┌────────▼────────┐
     │     Error       │          │    Exception    │
     │  (unchecked)    │          │                 │
     │  系统级/不可恢复 │          │                 │
     └────────┬────────┘          └────────┬────────┘
              │                             │
     ┌────────┼────────┐        ┌──────────┼──────────┐
     │        │        │        │                     │
 OutOfMemory Stack   VM     ┌───▼──────────┐   ┌─────▼──────┐
 Error     Overflow Error   │RuntimeException│  │ Checked    │
           Error            │ (unchecked)   │  │ Exceptions │
                            └───────┬───────┘  └─────┬──────┘
                                    │                 │
                          ┌─────────┼──────┐    ┌─────┼──────┐
                          │         │      │    │     │      │
                        NPE    Illegal  Class  IO  SQL  Reflective
                              Argument  Cast   Exc  Exc  OperationExc
                              Exc       Exc
```

### 三大类异常

| 类别 | 继承 | checked? | 说明 | 示例 |
|------|------|----------|------|------|
| **Error** | Throwable → Error | unchecked | JVM 级别错误，通常不可恢复 | OutOfMemoryError, StackOverflowError |
| **Checked Exception** | Throwable → Exception | checked | 编译器强制处理，可预见的外部错误 | IOException, SQLException |
| **Unchecked Exception** | Throwable → Exception → RuntimeException | unchecked | 编程错误，可以不声明 | NullPointerException, IllegalArgumentException |

### checked vs unchecked 设计哲学

```java
// Checked exception: 调用者必须处理或声明
public void readFile(String path) throws IOException {
    // IOException 是 checked — 文件可能不存在是可预见的
    FileReader fr = new FileReader(path);
}

// Unchecked exception: 编程错误，不强制处理
public void setAge(int age) {
    if (age < 0) {
        // IllegalArgumentException 是 unchecked — 调用者的 bug
        throw new IllegalArgumentException("age must be >= 0, got: " + age);
    }
}

// 自定义异常选择原则:
// - 调用者能合理恢复 → checked (extends Exception)
// - 编程错误/不变量违反 → unchecked (extends RuntimeException)
```

---

## 3. Helpful NullPointerException (JDK 14)

### JEP 358: 详细消息生成原理

JDK 14 之前 NPE 消息只有 `null`，无法定位是哪个变量为空。JEP 358 让 JVM 在抛出 NPE 时分析字节码，生成精确的 null 定位消息。

```java
// JDK 14 之前的 NPE 消息
// Exception in thread "main" java.lang.NullPointerException

// JDK 14+ Helpful NPE 消息
String city = person.getAddress().getCity().toUpperCase();
// Exception in thread "main" java.lang.NullPointerException:
//   Cannot invoke "Address.getCity()" because the return value of
//   "Person.getAddress()" is null

// 数组访问
int[] arr = null;
int v = arr[0];
// Cannot load from int array because "arr" is null

// 字段访问
String s = obj.field.toString();
// Cannot invoke "String.toString()" because "obj.field" is null
```

### 工作原理 (How It Works)

1. JVM 抛出 NPE 时，检查抛出位置的字节码 (bytecode)
2. 分析导致 NPE 的指令 (如 invokevirtual, getfield, aaload)
3. 回溯操作数栈 (operand stack) 确定哪个引用为 null
4. 生成人类可读的消息描述

### JVM 参数控制

```bash
# JDK 14: 默认关闭，需手动启用
java -XX:+ShowCodeDetailsInExceptionMessages MyApp

# JDK 15+: 默认启用
# 关闭 (极端性能敏感场景):
java -XX:-ShowCodeDetailsInExceptionMessages MyApp
```

### 安全考虑

Helpful NPE 消息可能泄露变量名和代码结构。在安全敏感的环境中，序列化异常消息前应考虑脱敏 (sanitization)。

---

## 4. try-with-resources 与 Suppressed Exceptions

### AutoCloseable 与 Closeable

```java
// AutoCloseable (JDK 7): close() throws Exception
// Closeable (JDK 1.5): close() throws IOException — 是 AutoCloseable 的子接口

public class MyResource implements AutoCloseable {
    public void doWork() { /* ... */ }

    @Override
    public void close() throws Exception {
        // 释放资源
    }
}

// try-with-resources: 保证 close() 被调用
try (MyResource r = new MyResource()) {
    r.doWork();
}  // 自动调用 r.close()，即使 doWork() 抛出异常
```

### 多资源与关闭顺序

```java
// 多个资源按声明的逆序关闭 (LIFO)
try (FileReader fr = new FileReader("input.txt");       // 第二个关闭
     BufferedReader br = new BufferedReader(fr)) {      // 第一个关闭
    String line = br.readLine();
}

// JDK 9+: 简化语法 — 可引用已有的 effectively final 变量
FileReader fr = new FileReader("input.txt");
BufferedReader br = new BufferedReader(fr);
try (fr; br) {
    String line = br.readLine();
}
```

### Suppressed Exceptions 机制

当 try 块和 close() 都抛出异常时，close() 的异常被抑制 (suppressed)，附加到主异常上。

```java
public class FlakyResource implements AutoCloseable {
    public void doWork() {
        throw new RuntimeException("work failed");
    }

    @Override
    public void close() {
        throw new RuntimeException("close failed");
    }
}

try (FlakyResource r = new FlakyResource()) {
    r.doWork();
} catch (RuntimeException e) {
    System.out.println("Primary: " + e.getMessage());
    // "Primary: work failed"

    Throwable[] suppressed = e.getSuppressed();
    for (Throwable t : suppressed) {
        System.out.println("Suppressed: " + t.getMessage());
        // "Suppressed: close failed"
    }
}
```

### Suppressed vs Cause

```java
// cause (异常链): 上层异常包装下层异常
//   e.getCause() → 因果关系
// suppressed (抑制异常): 主异常发生后，清理阶段产生的附加异常
//   e.getSuppressed() → 并发/附带关系

// 手动添加 suppressed exception
Exception primary = new Exception("primary");
primary.addSuppressed(new Exception("secondary"));
primary.addSuppressed(new Exception("tertiary"));
```

---

## 5. 异常链

### 异常包装 (Exception Wrapping, JDK 1.4+)

```java
try {
    // 底层操作
    FileReader file = new FileReader("config.txt");
} catch (FileNotFoundException e) {
    // 包装为更高层异常，保留原因
    throw new ConfigException("配置文件未找到", e);
}

// 遍历异常链 (walking the cause chain)
try {
    // ...
} catch (ServiceException e) {
    Throwable cause = e;
    while (cause != null) {
        System.err.println(cause.getClass().getName() + ": " + cause.getMessage());
        cause = cause.getCause();
    }
}
```

### initCause() — 延迟设置原因

```java
// 某些遗留异常没有接受 cause 的构造函数
// 可以用 initCause() 补设 (只能调用一次)
Exception ex = new LegacyException("high level");
ex.initCause(new IOException("low level"));
throw ex;
```

---

## 6. StackWalker API (JDK 9)

### 替代 Thread.getStackTrace()

`StackWalker` (JEP 259) 提供惰性 (lazy) 栈帧遍历，按需读取，性能远优于旧 API。

```java
import java.lang.StackWalker;
import java.lang.StackWalker.StackFrame;

// 旧方式 — 立即捕获整个栈，分配 StackTraceElement[]
StackTraceElement[] stack = Thread.currentThread().getStackTrace();
// 或 new Throwable().getStackTrace()

// 新方式 — 惰性遍历，可提前终止
StackWalker walker = StackWalker.getInstance();

// 遍历所有帧
walker.forEach(frame ->
    System.out.println(frame.getClassName() + "." +
                       frame.getMethodName() + ":" +
                       frame.getLineNumber())
);

// 只取前 N 帧 (短路)
List<StackFrame> top5 = walker.walk(s ->
    s.limit(5).collect(Collectors.toList())
);
```

### 获取调用者类

```java
// 需要 RETAIN_CLASS_REFERENCE 选项
StackWalker walker = StackWalker.getInstance(
    StackWalker.Option.RETAIN_CLASS_REFERENCE
);

// 获取直接调用者的 Class 对象
Class<?> caller = walker.getCallerClass();

// 用途: 日志框架确定调用者、安全检查、SPI 加载
```

### 高级配置

```java
StackWalker walker = StackWalker.getInstance(
    Set.of(
        StackWalker.Option.RETAIN_CLASS_REFERENCE,  // 保留 Class 引用
        StackWalker.Option.SHOW_HIDDEN_FRAMES,      // 显示 lambda/method-handle 帧
        StackWalker.Option.SHOW_REFLECT_FRAMES       // 显示反射帧
    )
);

// 过滤查找特定帧
Optional<StackFrame> frame = walker.walk(s ->
    s.filter(f -> f.getClassName().startsWith("com.myapp"))
     .findFirst()
);

// 统计栈深度
long depth = walker.walk(s -> s.count());
```

### 性能对比

| 方法 | 行为 | 性能 |
|------|------|------|
| `Thread.currentThread().getStackTrace()` | 立即捕获全部帧 | 慢，分配数组 |
| `new Throwable().getStackTrace()` | 同上 | 慢 |
| `StackWalker.walk(s -> s.limit(5).collect(...))` | 惰性遍历，只读 5 帧 | 快，按需分配 |
| `StackWalker.getCallerClass()` | 只获取调用者 | 最快 |

---

## 7. 异常性能

### 栈追踪开销 (Stack Trace Cost)

异常创建的主要开销在于 `fillInStackTrace()`，需要遍历当前线程栈并分配 `StackTraceElement[]`。

```java
// 异常创建成本测试
long start = System.nanoTime();
for (int i = 0; i < 100_000; i++) {
    new RuntimeException("test");  // 大部分时间在 fillInStackTrace()
}
// 典型: 数百毫秒 (取决于栈深度)

// 对比: 不填充栈追踪
for (int i = 0; i < 100_000; i++) {
    new RuntimeException("test") {
        @Override
        public synchronized Throwable fillInStackTrace() {
            return this;  // 跳过栈追踪填充
        }
    };
}
// 典型: 几毫秒
```

### -XX:-OmitStackTraceInFastThrow

HotSpot 默认启用 `-XX:+OmitStackTraceInFastThrow`。当同一位置重复抛出同一类型异常时，JIT 会优化为抛出一个预分配的、**没有栈追踪** 的异常实例。

```bash
# 关闭此优化 (调试时有用)
java -XX:-OmitStackTraceInFastThrow MyApp

# 现象: 日志中 NPE/ClassCastException 等丢失栈追踪
# java.lang.NullPointerException   ← 没有 stack trace!
# 原因: HotSpot 在热路径上复用预分配异常对象
```

### 性能优化策略

```java
// 1. 避免用异常做流程控制
// 差: 异常驱动的循环
try {
    while (true) {
        Object item = iterator.next();  // 依赖 NoSuchElementException 退出
    }
} catch (NoSuchElementException e) { }

// 好: 条件检查
while (iterator.hasNext()) {
    Object item = iterator.next();
}

// 2. 预分配异常 (高频场景)
private static final RuntimeException SENTINEL =
    new RuntimeException("sentinel") {
        @Override
        public synchronized Throwable fillInStackTrace() {
            return this;  // 无栈追踪
        }
    };

// 3. 自定义异常可覆盖 fillInStackTrace() 降低开销
public class LightweightException extends RuntimeException {
    @Override
    public synchronized Throwable fillInStackTrace() {
        return this;
    }
}
```

---

## 8. 常见陷阱

### catch Exception vs catch Throwable

```java
// catch (Exception e): 捕获所有 Exception (包括 RuntimeException)
// 不捕获 Error (OutOfMemoryError, StackOverflowError 等)
// 通常正确的选择

// catch (Throwable t): 捕获一切，包括 Error
// 几乎总是错误的! Error 代表 JVM 级故障，捕获后状态可能已损坏
try {
    // ...
} catch (Throwable t) {
    // 危险: OutOfMemoryError 被捕获后，JVM 状态不确定
}

// 例外: 框架级代码 (如线程池) 可能需要捕获 Throwable 以保护线程存活
```

### 空 catch 块 (Empty Catch Block)

```java
// 吞掉异常是常见 bug 来源
try {
    riskyOperation();
} catch (Exception e) {
    // 空! 异常被静默忽略
}

// 至少记录日志
try {
    riskyOperation();
} catch (Exception e) {
    log.warn("Operation failed, continuing", e);
}

// 明确表示有意忽略
try {
    Thread.sleep(1000);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();  // 恢复中断状态
}
```

### 异常做流程控制 (Exceptions as Control Flow)

```java
// 反模式: 用异常代替条件判断
public int parseOrDefault(String s, int defaultVal) {
    try {
        return Integer.parseInt(s);       // 非数字时抛异常
    } catch (NumberFormatException e) {
        return defaultVal;                // 用异常做流程控制
    }
}
// 当大量输入无效时，性能极差

// 如果高频调用且无效输入常见，考虑预检查或返回 Optional
```

### InterruptedException 处理

```java
// 错误: 吞掉中断
try {
    Thread.sleep(5000);
} catch (InterruptedException e) {
    // 什么都不做 → 线程中断状态丢失
}

// 正确方案 1: 恢复中断状态
try {
    Thread.sleep(5000);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}

// 正确方案 2: 重新抛出
try {
    Thread.sleep(5000);
} catch (InterruptedException e) {
    throw new RuntimeException("Interrupted", e);
}
```

### finally 中的 return

```java
// 危险: finally 中的 return 会覆盖 try/catch 中的返回值和异常
try {
    throw new RuntimeException("error");
} finally {
    return 42;  // 异常被吞掉! 方法返回 42
}
// 编译器可能发出警告，但代码可编译
```

---

## 9. Pattern Matching 与异常

### instanceof 模式匹配 (JDK 16+, JEP 394)

```java
// 在 catch 块中简化异常类型判断
try {
    // ...
} catch (Exception e) {
    if (e instanceof IOException ioe) {
        handleIO(ioe);
    } else if (e instanceof SQLException sqle) {
        handleSQL(sqle);
    }
}
```

### switch exhaustiveness 与异常

JDK 21+ 的 switch 表达式要求穷尽性 (exhaustiveness)。对于 sealed 类型，编译器保证覆盖所有可能。在运行时，如果 sealed 层次被非法扩展 (如不同 jar 版本)，JVM 会抛出 `MatchException`。

```java
// JDK 21+: sealed 类型的 switch 必须穷尽
sealed interface Shape permits Circle, Rectangle, Triangle {}
record Circle(double r) implements Shape {}
record Rectangle(double w, double h) implements Shape {}
record Triangle(double a, double b, double c) implements Shape {}

double area(Shape shape) {
    return switch (shape) {
        case Circle c -> Math.PI * c.r() * c.r();
        case Rectangle r -> r.w() * r.h();
        case Triangle t -> {
            double s = (t.a() + t.b() + t.c()) / 2;
            yield Math.sqrt(s * (s - t.a()) * (s - t.b()) * (s - t.c()));
        }
        // 不需要 default — 编译器知道所有子类型已覆盖
    };
}

// MatchException (JDK 21+)
// 当 switch 表达式在运行时无法匹配任何分支时抛出
// 常见于 sealed 类层次在编译后被修改的场景
```

### switch 表达式中的异常

```java
// switch 表达式中的 guard 和异常
String classify(Object obj) {
    return switch (obj) {
        case Integer i when i > 0 -> "positive int";
        case Integer i -> "non-positive int";
        case String s -> s.isEmpty() ? "empty string" : "string: " + s;
        case null -> "null";
        default -> "other: " + obj.getClass().getName();
    };
}
// null case (JDK 21+): switch 可以显式匹配 null，避免 NPE
```

---

## 10. Virtual Thread 异常传播

### StructuredTaskScope (JDK 21 预览, JEP 453)

结构化并发 (Structured Concurrency) 中，子任务的异常传播遵循结构化原则。

```java
import java.util.concurrent.StructuredTaskScope;

// ShutdownOnFailure: 任一子任务失败则关闭全部
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    StructuredTaskScope.Subtask<String> user = scope.fork(() -> fetchUser());
    StructuredTaskScope.Subtask<List<Order>> orders = scope.fork(() -> fetchOrders());

    scope.join();           // 等待所有子任务
    scope.throwIfFailed();  // 如果有失败，抛出异常

    // 两个都成功才到这里
    process(user.get(), orders.get());
} catch (Exception e) {
    // e 是第一个失败子任务的异常
    // 其余子任务被取消 (cancel)
}

// ShutdownOnSuccess: 任一子任务成功则关闭全部
try (var scope = new StructuredTaskScope.ShutdownOnSuccess<String>()) {
    scope.fork(() -> fetchFromPrimary());
    scope.fork(() -> fetchFromBackup());

    scope.join();
    String result = scope.result();  // 第一个成功的结果
} catch (Exception e) {
    // 所有子任务都失败时抛出
}
```

### Virtual Thread 异常特点

```java
// Virtual thread 的异常行为与 platform thread 基本相同
Thread vt = Thread.ofVirtual().start(() -> {
    throw new RuntimeException("virtual thread error");
});
// 未捕获异常由 UncaughtExceptionHandler 处理

// 设置异常处理器
Thread.ofVirtual()
    .uncaughtExceptionHandler((t, e) -> {
        System.err.println("Virtual thread " + t.getName() + " failed: " + e);
    })
    .start(() -> { throw new RuntimeException("error"); });

// 注意: virtual thread 中的 InterruptedException
// virtual thread 的 sleep/wait/blocking IO 在取消时抛出 InterruptedException
// StructuredTaskScope 取消子任务时通过 interrupt 机制通知
```

### 异常传播 vs 传统线程池

| 特性 | ExecutorService | StructuredTaskScope |
|------|----------------|---------------------|
| 异常获取 | `Future.get()` 包装为 `ExecutionException` | `throwIfFailed()` 直接抛原始异常 |
| 取消传播 | 手动取消其余任务 | 自动取消 (ShutdownOnFailure) |
| 异常聚合 | 需手动收集 | scope 管理 |
| 生命周期 | 任务可能泄漏 | 结构化保证 (structured guarantee) |

---

## 11. 最佳实践

### 异常设计原则

```java
// 1. 选择合适的异常类型
// Error: 系统级错误，不应捕获
// RuntimeException: 编程错误，可以不声明
// Checked Exception: 可恢复错误，必须声明

// 2. 提供有用的错误信息 (包含上下文)
throw new IllegalArgumentException(
    "pageSize must be >= 1, got: " + pageSize
);

// 3. 保留原因链
throw new ServiceException("保存用户失败", originalException);

// 4. 保持异常不可变
public final class OrderException extends RuntimeException {
    private final String orderId;
    public OrderException(String orderId, String message, Throwable cause) {
        super(message, cause);
        this.orderId = orderId;
    }
    public String getOrderId() { return orderId; }
}

// 5. 提供恢复信息
public class RetryableException extends RuntimeException {
    private final Duration retryAfter;
    public Duration getRetryAfter() { return retryAfter; }
}
```

### 异常处理模式

```java
// 1. 转换异常 (translate): 底层异常 → 业务异常
try {
    dao.save(entity);
} catch (SQLException e) {
    throw new PersistenceException("Failed to save entity", e);
}

// 2. 链式处理 (chain): 按类型分别处理
try {
    operation();
} catch (TransientException e) {
    retry(operation);
} catch (Exception e) {
    log.error("Permanent failure", e);
    throw new ServiceException("服务不可用", e);
}

// 3. 后备操作 (fallback)
try {
    return primaryService.fetch(id);
} catch (ServiceException e) {
    log.warn("Primary failed, falling back", e);
    return fallbackService.fetch(id);
}

// 4. 异常聚合 (aggregation): 收集多个异常
List<Exception> errors = new ArrayList<>();
for (Task task : tasks) {
    try {
        task.execute();
    } catch (Exception e) {
        errors.add(e);
    }
}
if (!errors.isEmpty()) {
    RuntimeException aggregate = new RuntimeException("Multiple failures");
    errors.forEach(aggregate::addSuppressed);
    throw aggregate;
}
```

### 多异常捕获 (Multi-catch, JDK 7+)

```java
// 多异常捕获 — 用 | 分隔
try {
    // ...
} catch (IOException | SQLException e) {
    // e 的类型是两者的共同父类
    log.error("Operation failed: " + e.getMessage(), e);
}

// 注意: 不能有继承关系
// catch (IOException | FileNotFoundException e)  ← 编译错误
// FileNotFoundException 是 IOException 的子类，直接 catch (IOException e) 即可

// 精确异常重抛 (Precise Rethrow, JDK 7+)
public void process() throws IOException, SQLException {
    try {
        // 可能抛出 IOException 或 SQLException
    } catch (final Exception e) {
        log.error("Failed", e);
        throw e;  // 编译器知道实际类型，throws 声明精确
    }
}
```

### 自定义异常设计

```java
// 好的自定义异常: 携带上下文信息
public class OrderNotFoundException extends RuntimeException {
    private final String orderId;
    private final String customerId;

    public OrderNotFoundException(String orderId, String customerId) {
        super("Order " + orderId + " not found for customer " + customerId);
        this.orderId = orderId;
        this.customerId = customerId;
    }

    public String getOrderId() { return orderId; }
    public String getCustomerId() { return customerId; }
}

// 异常层次设计: 业务异常基类 + 具体子类
public abstract class BusinessException extends RuntimeException {
    private final String errorCode;
    protected BusinessException(String errorCode, String message, Throwable cause) {
        super(message, cause);
        this.errorCode = errorCode;
    }
    public String getErrorCode() { return errorCode; }
}

public class InsufficientBalanceException extends BusinessException {
    public InsufficientBalanceException(BigDecimal required, BigDecimal available) {
        super("INSUFFICIENT_BALANCE",
              "Required " + required + " but only " + available + " available",
              null);
    }
}
```

---

## 12. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 异常处理 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Joe Darcy | 7 | Oracle | 异常体系设计 |
| 2 | Pavel Rappo | 4 | Oracle | API 设计 |
| 3 | Erik Gahlin | 3 | Oracle | JFR 异常事件 |
| 4 | Roger Riggs | 1 | Oracle | 核心库 |
| 5 | Mikael Vidstedt | 1 | Oracle | 运行时 |

### 历史贡献者

| 贡献者 | 公司/机构 | 主要贡献 |
|--------|----------|----------|
| **Joshua Bloch** | Sun/Google | 异常设计原则 (Effective Java) |
| **Neal Gafter** | Sun | 异常链实现, multi-catch |
| **Mandy Chung** | Oracle | StackWalker API (JEP 259) |
| **Goetz Lindenmaier** | SAP | Helpful NullPointerException (JEP 358) |
| **Alan Bateman** | Oracle | StructuredTaskScope 异常传播 |

---

## 13. 相关链接

### 内部文档

- [异常时间线](timeline.md) - 详细的历史演进
- [核心 API](../)

### 外部资源

- [JEP 259: StackWalker](https://openjdk.org/jeps/259)
- [JEP 358: Helpful NullPointerExceptions](https://openjdk.org/jeps/358)
- [JEP 394: Pattern Matching for instanceof](https://openjdk.org/jeps/394)
- [JEP 453: Structured Concurrency](https://openjdk.org/jeps/453)
- [Java 异常处理指南 (Oracle)](https://docs.oracle.com/javase/tutorial/essential/exceptions/)
- [Effective Java - 异常章节](https://www.oreilly.com/library/view/effective-java/9780134686097/)

---

**最后更新**: 2026-03-22
