# 并发 (Concurrency) JEPs

> JDK 21-26 并发编程相关 JEP 汇总

---
## 目录

1. [概览](#1-概览)
2. [虚拟线程 (Virtual Threads)](#2-虚拟线程-virtual-threads)
3. [结构化并发 (Structured Concurrency)](#3-结构化并发-structured-concurrency)
4. [隐式类和实例主方法 (Implicit Classes)](#4-隐式类和实例主方法-implicit-classes)
5. [作用域值 (Scoped Values)](#5-作用域值-scoped-values)
6. [相关链接](#6-相关链接)

---


## 1. 概览

```
JDK 21 ───── JDK 22 ───── JDK 23 ───── JDK 24 ───── JDK 25 ───── JDK 26
   │            │            │            │            │            │
Virtual    Structured   Implicit    Scoped     Structured   Scoped
Threads      Concurrency  Classes    Values     Concurrency  Values
(正式)       (预览)      (正式)      (正式)      (预览)        (正式)
```

---

## 2. 虚拟线程 (Virtual Threads)

### 演进历程

| 版本 | JEP | 状态 | 说明 |
|------|-----|------|------|
| JDK 19 | 425 | 🔍 预览 | 虚拟线程首次预览 |
| JDK 20 | 436 | 🔍 预览 | 第二次预览 |
| JDK 21 | 444 | ✅ 正式 | 虚拟线程正式发布 |

### 核心特性

**创建虚拟线程**：
```java
// 方式 1: Thread.startVirtualThread
Thread.startVirtualThread(() -> {
    // 虚拟线程任务
});

// 方式 2: Executors.newVirtualThreadPerTaskExecutor
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> task());
}

// 方式 3: Thread.ofVirtual
Thread.Builder.ofVirtual().name("my-vthread").task(() -> task());
```

**虚拟线程 vs 平台线程**：
| 特性 | 平台线程 | 虚拟线程 |
|------|---------|----------|
| 内存占用 | ~1MB/线程 | ~1KB/线程 |
| 创建数量 | 受限于物理资源 | 几乎无限 |
| 阻塞操作 | 阻塞OS线程 | 不阻塞OS线程 |
| 上下文切换 | 内核级别 | JVM级别 |

**详见**：[JEP 444](jep-444.md)

---

## 3. 结构化并发 (Structured Concurrency)

### 演进历程

| 版本 | JEP | 状态 | 说明 |
|------|-----|------|------|
| JDK 19 | 428 | 🔍 预览 | 预览版 |
| JDK 20 | 437 | 🔍 预览 | 第二次预览 |
| JDK 21 | 453 | 🔍 预览 | 第三次预览 |
| JDK 22 | 462 | 🔍 预览 | 第四次预览 |
| JDK 23 | 480 | 🔍 预览 | 第五次预览 |
| JDK 25 | 505 | 🔍 预览 | 第六次预览 |
| JDK 26 | 525 | 🔍 预览 | 第七次预览 |

### 核心API

```java
// StructuredTaskScope (JDK 21-25)
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Supplier<String> user = scope.fork(() -> findUser());
    Supplier<Integer> order = scope.fork(() -> findOrder());
    
    scope.join();  // 等待所有任务完成
    
    return new Response(user.get(), order.get());
}
```

**详见**：[JEP 462](jep-462.md) | [JEP 480](jep-480.md) | [JEP 505](jep-505.md) | [JEP 525](jep-525.md)

---

## 4. 隐式类和实例主方法 (Implicit Classes)

### 演进历程

| 版本 | JEP | 状态 | 说明 |
|------|-----|------|------|
| JDK 21 | 445 | 🔍 预览 | 无名类和实例主方法 |
| JDK 22 | 463 | 🔍 预览 | 隐式类和实例主方法 |
| JDK 23 | 477 | ✅ 正式 | 正式发布 |
| JDK 25 | 512 | ✅ 正式 | 紧凑源文件 |

### 简化 Hello World

```java
// 传统方式
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}

// JEP 445/463/477 (隐式类)
void main() {
    System.out.println("Hello, World!");
}

// JDK 25 紧凑源文件 (单一文件)
void main() {
    println("Hello, World!");  // 自动导入 System.out
}
```

**详见**：[JEP 445](../language/jep-445.md) | [JEP 463](../language/jep-463.md) | [JEP 477](../language/jep-477.md) | [JEP 512](../language/jep-512.md)

---

## 5. 作用域值 (Scoped Values)

### 演进历程

| 版本 | JEP | 状态 | 说明 |
|------|-----|------|------|
| JDK 20 | 429 | 🔍 预览 | 作用域值首次预览 |
| JDK 21 | 446 | ✅ 正式 | 正式发布 |
| JDK 25 | 506 | ✅ 正式 | 第二版 |
| JDK 26 | 530 | 🔍 预览 | 更多改进 |

### 核心用法

```java
// 声明作用域值
private static final ScopedValue<String> USER_ID = ScopedValue.create();

// 使用作用域值
USER_ID.where("user123", () -> {
    // 在此范围内， USER_ID.get() 返回 "user123"
    processUser(USER_ID.get());
});

// 跨线程共享
USER_ID.where("user123", () -> {
    Thread.startVirtualThread(() -> {
        // 子线程可以访问父线程的作用域值
        String id = USER_ID.get();  // "user123"
    });
});
```

**详见**：[JEP 446](jep-446.md) | [JEP 506](jep-506.md)

---

## 6. 相关链接

- [并发主题时间线](/by-topic/concurrency/)
- Virtual Threads 最佳实践 
