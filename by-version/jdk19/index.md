# JDK 19

> **发布日期**: 2022-09-20 | **类型**: Feature Release

---

## 核心特性

JDK 19 引入了 Virtual Threads（首次预览）、Structured Concurrency（首次预览）和 Foreign Function & Memory API（预览）。

| 特性 | 影响 | 详情 |
|------|------|------|
| **Virtual Threads（第1次预览）** | ⭐⭐⭐⭐⭐ | JEP 425/444，虚拟线程 |
| **Structured Concurrency（第1次预览）** | ⭐⭐⭐⭐⭐ | JEP 428，结构化并发 |
| **Foreign Function & Memory API（第2次预览）** | ⭐⭐⭐⭐ | JEP 424，预览 |
| **Record Patterns（第1次预览）** | ⭐⭐⭐⭐ | JEP 405，预览 |
| **Pattern Matching for switch（第3次预览）** | ⭐⭐⭐⭐ | JEP 420/427 |
| **Linux/RISC-V 端口** | ⭐⭐⭐ | JEP 422 |
| **Foreign Function & Memory API（第2次预览）** | ⭐⭐⭐⭐ | JEP 424 |

---

## 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 425](https://openjdk.org/jeps/425) | Virtual Threads (First Preview) | 虚拟线程（第1次预览） |
| [JEP 428](https://openjdk.org/jeps/428) | Structured Concurrency (Preview) | 结构化并发（第1次预览） |
| [JEP 424](https://openjdk.org/jeps/424) | Foreign Function & Memory API (Second Preview) | FFM API（第2次预览） |
| [JEP 405](https://openjdk.org/jeps/405) | Record Patterns (Preview) | Record 模式匹配（第1次预览） |
| [JEP 427](https://openjdk.org/jeps/427) | Pattern Matching for switch (Third Preview) | switch 模式匹配（第3次预览） |
| [JEP 422](https://openjdk.org/jeps/422) | Linux/RISC-V Port | Linux RISC-V |
| [JEP 426](https://openjdk.org/jeps/426) | Vector API (Fourth Incubator) | Vector API（第4次孵化） |
| [JEP 429](https://openjdk.org/jeps/429) | Scoped Values (Incubator) | 作用域值（孵化器） |

---

## 代码示例

### Virtual Threads（第1次预览）

```java
// 创建虚拟线程
Thread vthread = Thread.ofVirtual().start(() -> {
    System.out.println("Hello from virtual thread");
});

// 使用 ExecutorService
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 10000; i++) {
        executor.submit(() -> {
            // 处理任务
        });
    }
}
```

### Structured Concurrency（第1次预览）

```java
try (var scope = new StructuredTaskScope<Object>()) {
    Future<String> user = scope.fork(() -> fetchUser());
    Future<List<Order>> orders = scope.fork(() -> fetchOrders());

    scope.join();
    scope.throwIfFailed();

    return new Response(user.resultNow(), orders.resultNow());
}
```

### Record Patterns（第1次预览）

```java
record Point(int x, int y) { }

// JDK 19 (第1次预览)
if (obj instanceof Point(int x, int y)) {
    System.out.println("x=" + x + ", y=" + y);
}
```

---

## 相关链接

- [发布说明](https://openjdk.org/projects/jdk/19/)
