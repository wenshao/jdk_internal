# synchronized 内部实现

> 从 Mark Word 到 ObjectMonitor 的锁演进

[← 返回并发编程](index.md)

---

## 1. 对象头与锁状态 (Object Header / Mark Word)

HotSpot 中每个 Java 对象的对象头 (object header) 包含一个 mark word，用于存储锁状态。在 64 位 JVM 中，mark word 为 64 bit：

```
64-bit Mark Word 布局 (低 2 bit 为 tag):

  Unlocked (无锁):   [unused:25 | hashcode:31 | age:4 | 0 | 01]
  Thin Lock (轻量级): [Lock Record 指针 (62 bit)             | 00]
  Fat Lock (重量级):  [ObjectMonitor 指针 (62 bit)            | 10]
  GC Marked:         [Forwarding 指针 (62 bit)               | 11]
```

锁状态转换的整体流程：

```
Unlocked (无锁, tag=01)
    │
    ├── CAS 成功 ──► Thin Lock (轻量级锁, tag=00)
    │                    │
    │                    ├── CAS 竞争失败 + 自旋超限
    │                    │         │
    │                    │         ▼
    │                    └──► Fat Lock (重量级锁, tag=10)
    │                              │
    │                              └── 无竞争 + deflation ──► Unlocked
    │
    └── (JDK 6-14) 偏向锁路径 → 已废弃
```

---

## 2. Biased Locking（偏向锁，已废弃）

Biased Locking（偏向锁）在 JDK 6 引入，JDK 15 通过 **JEP 374** 默认禁用，JDK 18 彻底移除代码。

**原理**：当一个对象只被单线程访问时，将线程 ID 写入 mark word，后续同一线程进入 synchronized 无需任何 CAS 操作。

**废弃原因**：
- 现代硬件上 CAS 操作已非常快（几纳秒），Biased Locking 的收益不明显
- 偏向撤销 (bias revocation) 需要 STW safepoint，代价高
- 代码复杂度高，与 Compact Object Headers (JEP 450) 不兼容
- HotSpot 中维护 Biased Locking 的代码超过 1500 行

---

## 3. Thin Lock（轻量级锁）

当存在轻度竞争 (light contention) 时，HotSpot 使用 Thin Lock（基于 CAS 的轻量级锁）。

### 获取过程

1. 在当前线程栈帧中分配 **Lock Record**
2. 将对象 mark word 复制到 Lock Record（**Displaced Mark Word**）
3. CAS 将对象 mark word 替换为 Lock Record 指针（tag 位设为 `00`）

```
Thread Stack          Object Header
┌─────────────┐       ┌──────────────────┐
│ Lock Record │◄──────│ LR ptr │ tag: 00 │
│ [Displaced  │       └──────────────────┘
│  Mark Word] │  ← 保存原始 mark word
└─────────────┘

CAS 成功 → 获取锁
CAS 失败 → 已被自己持有则重入计数，否则膨胀为 Fat Lock
```

### 重入处理 (Reentrant)

同一线程再次进入 synchronized 时，CAS 会失败，但 JVM 检测到 Lock Record 指针属于当前线程栈帧范围，则直接压入一个新的 Displaced Mark Word 为 `null` 的 Lock Record 作为重入计数。

### 释放过程

CAS 将对象 mark word 恢复为 Displaced Mark Word。如果 CAS 失败（说明已膨胀为 Fat Lock），则走 Fat Lock 的释放路径。

---

## 4. Fat Lock（重量级锁）与 ObjectMonitor

当 Thin Lock CAS 竞争失败（自旋一定次数后仍未获得锁），发生 **Lock Inflation（锁膨胀）**。

### ObjectMonitor 结构

```java
// HotSpot 内部 ObjectMonitor 结构（C++ 实现，简化版）
// src/hotspot/share/runtime/objectMonitor.hpp
class ObjectMonitor {
    volatile markWord _header;      // displaced mark word
    volatile intptr_t _owner;       // 持有锁的线程
    volatile int _recursions;       // 重入次数
    ObjectWaiter* _EntryList;       // 等待获取锁的线程（竞争队列）
    ObjectWaiter* _cxq;             // 最近到达的竞争者（Contention Queue）
    ObjectWaiter* _WaitSet;         // 调用 wait() 的线程
    volatile int _waiters;          // wait() 的线程数
    volatile int _contentions;      // 竞争计数
};
```

### 锁膨胀过程 (Lock Inflation)

1. 分配 ObjectMonitor 对象
2. 将对象原始 mark word 保存到 ObjectMonitor 的 `_header` 字段
3. 用 CAS 将对象 mark word 替换为 ObjectMonitor 指针（tag 位设为 `10`）
4. 竞争线程进入 `_cxq` 或 `_EntryList`，通过 `pthread_mutex` + `pthread_cond`（Linux）或等价 OS 原语阻塞

```
竞争线程的流转:

  新到达 ──► _cxq (Contention Queue, 后进先出)
                │
                ▼
         _EntryList (等待队列, 先进先出)
                │
                ├── owner 释放锁 → 从 _EntryList 或 _cxq 选取下一个
                │
                ▼
           _owner = 当前线程

  wait() 调用:
    _owner ──► _WaitSet (等待 notify)
                   │
                   ├── notify() → 移回 _EntryList 或 _cxq
                   │
                   ▼
              重新竞争锁
```

### 锁降级 (Lock Deflation)

JDK 21+ 默认使用异步锁降级（通过 `DeflateIdleMonitors` 在 safepoint 或异步执行）。当 ObjectMonitor 无竞争者且无 owner 时，可回收 ObjectMonitor，将对象 mark word 恢复为无锁状态。

JVM 参数 `-XX:+UseObjectMonitorTable`（JDK 21+）将 monitor 从对象头移至全局表，支持更高效的 deflation。

---

## 5. synchronized 与虚拟线程 (Virtual Threads)

### Pinning 问题

虚拟线程在 `synchronized` 块/方法内执行阻塞操作时，会被 **pin（固定）** 到载体线程 (carrier thread)，导致载体线程无法服务其他虚拟线程：

```java
// ❌ Pinning 场景: synchronized + 阻塞 I/O
synchronized (sharedLock) {
    socket.read(buffer);  // 载体线程被 pin，无法复用
}

// 检测 Pinning:
// -Djdk.tracePinnedThreads=full   打印完整堆栈
// -Djdk.tracePinnedThreads=short  打印摘要
```

### JDK 24 改进: JEP 491

**JEP 491** (Synchronize Virtual Threads without Pinning) 使虚拟线程在 `synchronized` 块中阻塞时可以 unmount，消除了大部分 pinning 问题。但 JNI 关键区和 `monitorenter` 在 native 代码中仍会导致 pinning。

### 迁移建议

```java
// JDK 24 之前的推荐做法：使用 ReentrantLock 替代 synchronized
// ❌ synchronized + 阻塞 I/O
synchronized (lock) {
    Thread.sleep(1000);  // Pinning!
}

// ✅ ReentrantLock 天然支持虚拟线程 unmount
ReentrantLock lock = new ReentrantLock();
lock.lock();
try {
    Thread.sleep(1000);  // 虚拟线程 unmount，载体线程释放
} finally {
    lock.unlock();
}

// JDK 24+ 后 synchronized 不再导致 pinning（大部分情况）
```

---

## 6. 相关 JEP

| JEP | 版本 | 说明 |
|-----|------|------|
| **JEP 374** | JDK 15 | 废弃 Biased Locking（偏向锁） |
| **JEP 450** | JDK 23 (预览) | Compact Object Headers，与 Biased Locking 不兼容 |
| **JEP 491** | JDK 24 | 虚拟线程 synchronized 不再 pin |

---

**最后更新**: 2026-03-20

[← 返回并发编程](index.md)
