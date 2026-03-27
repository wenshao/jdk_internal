---

# Java 锁机制对比: synchronized vs ReentrantLock vs StampedLock

---

## 目录

1. [核心设计哲学](#1-核心设计哲学)
2. [多维度对比](#2-多维度对比)
3. [synchronized 详解](#3-synchronized-详解)
4. [ReentrantLock 详解](#4-reentrantlock-详解)
5. [StampedLock 详解](#5-stampedlock-详解)
6. [虚拟线程影响](#6-虚拟线程影响)
7. [决策指南](#7-决策指南)
8. [常见误区](#8-常见误区)

---

## 1. 核心设计哲学

| 锁 | 一句话描述 |
|---|---|
| **synchronized** | JVM 内置关键字，简单安全，无显式释放 |
| **ReentrantLock** | java.util.concurrent 显式锁，功能丰富 |
| **StampedLock** | 乐观读锁，读多写少场景极致性能 |

---

## 2. 多维度对比

| 特性 | synchronized | ReentrantLock | StampedLock |
|------|-------------|---------------|-------------|
| **类型** | 关键字 | 类 | 类 |
| **锁释放** | 自动 (代码块退出) | 手动 (finally unlock) | 手动 (finally unlock) |
| **可中断** | ❌ | ✅ `lockInterruptibly()` | ✅ |
| **超时获取** | ❌ | ✅ `tryLock(timeout)` | ✅ |
| **公平锁** | ❌ (非公平) | ✅ (可选) | ❌ (非公平) |
| **条件变量** | ❌ (wait/notify) | ✅ `Condition` | ❌ |
| **乐观读** | ❌ | ❌ | ✅ `tryOptimisticRead` |
| **可重入** | ✅ | ✅ | ❌ (不可重入) |
| **虚拟线程安全** | ❌ (Pinning!) | ✅ | ✅ |
| **JDK 版本** | 1.0 | 5.0 | 8.0 |

---

## 3. synchronized 详解

### 3.1 使用方式

```java
// 1. 方法级
public synchronized void method() { /* ... */ }

// 2. 代码块级
public void method() {
    synchronized (lock) {
        /* ... */
    }
}

// 3. 静态方法 (类级锁)
public static synchronized void staticMethod() { /* ... */ }
```

### 3.2 JVM 实现

```
字节码:
  monitorenter      // 获取锁
  // 临界区
  monitorexit       // 释放锁

JDK 15 之前: 偏向锁 (Biased Locking) → 轻量级锁 → 重量级锁
JDK 15+:    偏向锁默认禁用 (JEP 374)
            轻量级锁 (自旋) → 重量级锁 (OS mutex)
```

### 3.3 适用场景

- 简单的临界区保护
- 不需要超时/中断/Condition
- 不在虚拟线程中使用（Pinning 问题）

---

## 4. ReentrantLock 详解

### 4.1 基本用法

```java
private final ReentrantLock lock = new ReentrantLock();

public void method() {
    lock.lock();
    try {
        // 临界区
    } finally {
        lock.unlock();  // 必须在 finally 中释放!
    }
}
```

### 4.2 高级功能

```java
// 1. 可中断获取
lock.lockInterruptibly();

// 2. 超时获取
if (lock.tryLock(5, TimeUnit.SECONDS)) {
    try { /* ... */ } finally { lock.unlock(); }
}

// 3. 非阻塞获取
if (lock.tryLock()) {
    try { /* ... */ } finally { lock.unlock(); }
} else {
    // 获取失败，走备选方案
}

// 4. 公平锁
ReentrantLock fairLock = new ReentrantLock(true); // FIFO 顺序

// 5. Condition 变量
Condition notEmpty = lock.newCondition();
Condition notFull = lock.newCondition();
```

### 4.3 适用场景

- 需要超时/中断/Condition
- 虚拟线程环境（不会 Pinning）
- 复杂的锁协作模式
- 生产者-消费者模型

---

## 5. StampedLock 详解

### 5.1 三种模式

```
┌─────────────────────────────────────────────────┐
│              StampedLock 模式                    │
│                                                  │
│  Writing (排他写锁)                              │
│    └── writeLock() → stamp                      │
│        完全排他，阻塞所有读和写                  │
│                                                  │
│  Reading (悲观读锁)                              │
│    └── readLock() → stamp                       │
│        允许并发读，阻塞写                        │
│                                                  │
│  Optimistic Reading (乐观读)                     │
│    └── tryOptimisticRead() → stamp              │
│        无锁! 不阻塞写，之后验证是否被修改       │
└─────────────────────────────────────────────────┘
```

### 5.2 乐观读示例

```java
private final StampedLock sl = new StampedLock();
private double x, y;

// 乐观读: 无锁，高性能
double distanceFromOrigin() {
    long stamp = sl.tryOptimisticRead();    // 获取乐观读 stamp
    double currentX = x, currentY = y;      // 读取数据
    if (!sl.validate(stamp)) {              // 验证期间是否有写操作
        // 乐观读失败，升级为悲观读
        stamp = sl.readLock();
        try {
            currentX = x;
            currentY = y;
        } finally {
            sl.unlockRead(stamp);
        }
    }
    return Math.sqrt(currentX * currentX + currentY * currentY);
}

// 写操作
void move(double deltaX, double deltaY) {
    long stamp = sl.writeLock();
    try {
        x += deltaX;
        y += deltaY;
    } finally {
        sl.unlockWrite(stamp);
    }
}
```

### 5.3 适用场景

- 读多写少（99% 读 / 1% 写）
- 高并发读取坐标、配置等
- 性能敏感场景

---

## 6. 虚拟线程影响

| 锁 | 虚拟线程行为 | 问题 | 建议 |
|----|------------|------|------|
| **synchronized** | ⚠️ **Pinning** | carrier thread 被钉住 | 替换为 ReentrantLock |
| **ReentrantLock** | ✅ 可卸载 | 无 | 推荐 |
| **StampedLock** | ✅ 可卸载 | 无 | 读多写少推荐 |
| **Object.wait()** | ⚠️ JDK 21 Pinning | JDK 24+ 修复 | 使用 Condition.await() |

### 迁移示例

```java
// ❌ 虚拟线程不安全
synchronized (lock) {
    blockingOperation();
}

// ✅ 虚拟线程安全
reentrantLock.lock();
try {
    blockingOperation();
} finally {
    reentrantLock.unlock();
}
```

---

## 7. 决策指南

```
开始
  │
  ├─ 虚拟线程环境?
  │    └── 是 → 使用 ReentrantLock (避免 synchronized)
  │
  ├─ 读多写少 (读 > 90%)?
  │    └── 是 → 使用 StampedLock 乐观读
  │
  ├─ 需要超时/中断/Condition?
  │    └── 是 → 使用 ReentrantLock
  │
  ├─ 简单临界区 + 无虚拟线程?
  │    └── 是 → 使用 synchronized (最简单)
  │
  └─ 默认 → ReentrantLock (最通用)
```

---

## 8. 常见误区

| 误区 | 正确理解 |
|------|---------|
| "synchronized 最慢" | JDK 15+ 无偏向锁后差距缩小，简单场景差异 < 5% |
| "StampedLock 总是更快" | 写多场景反而更慢（乐观读验证开销） |
| "ReentrantLock 总是更好" | synchronized 更安全（自动释放，不会忘记 unlock） |
| "公平锁更好" | 公平锁吞吐量降低 30-50%，大多数场景不需要 |
| "synchronized 不能用于虚拟线程" | JDK 25+ 改善了部分场景，但 ReentrantLock 仍推荐 |

---

## 相关链接

- [Virtual Thread 迁移案例](/cases/virtual-threads-migration.md)
- [Virtual Thread Pinning 排查](/cases/virtual-thread-pinning.md)
- [并发编程主题](/by-topic/concurrency/concurrency/)
- [JUC 深度分析](/modules/concurrent.md)
