---

# Virtual Thread Pinning：虚拟线程钉住问题排查

> **声明**：本文中所有监控数据、线程转储、性能指标均为 **示意数据（illustrative data）**，实际结果取决于工作负载、硬件环境和 JVM 版本。

---

## 目录

1. [背景与问题描述](#1-背景与问题描述)
2. [环境信息](#2-环境信息)
3. [第一阶段：症状发现](#3-第一阶段症状发现)
4. [第二阶段：Pinning 检测](#4-第二阶段pinning-检测)
5. [第三阶段：代码定位](#5-第三阶段代码定位)
6. [第四阶段：修复方案](#6-第四阶段修复方案)
7. [最终效果对比](#7-最终效果对比)
8. [经验总结与 Checklist](#8-经验总结与-checklist)

---

## 1. 背景与问题描述

### 1.1 业务场景

**数据同步服务**，从外部系统批量拉取数据并写入数据库。迁移到虚拟线程后，期望提高并发处理能力。

| 指标 | 期望 |
|------|------|
| 并发任务数 | 5,000+ |
| 单任务延迟 | 200-500ms (含网络 I/O) |
| 吞吐量 | 10,000 tasks/s |

### 1.2 问题现象

- 迁移到虚拟线程后，吞吐量反而从平台线程的 8,000 tasks/s 降到 2,000 tasks/s
- CPU 利用率仅 30%（远低于预期的 80%+）
- 响应延迟从 500ms 飙升到 3-5s
- 监控显示 ForkJoinPool carrier thread 全部被占用

---

## 2. 环境信息

```
JDK 版本:    JDK 21.0.2
GC:          G1 (默认)
框架:        Spring Boot 3.2 + MyBatis
数据库:      PostgreSQL 16 (HikariCP 连接池)
并发模型:    Executors.newVirtualThreadPerTaskExecutor()
CPU:         8 核
```

---

## 3. 第一阶段：症状发现

### 3.1 性能对比

```
┌────────────────────────┬───────────────────┬───────────────────┐
│ 指标                   │ 平台线程 (200 池) │ 虚拟线程           │
├────────────────────────┼───────────────────┼───────────────────┤
│ 吞吐量                 │ 8,000 tasks/s     │ 2,000 tasks/s     │
│ CPU 利用率             │ 75%               │ 30%               │
│ P99 延迟               │ 800ms             │ 5,000ms           │
│ 活跃线程数             │ 200               │ ~5,000            │
│ Carrier thread 使用    │ N/A               │ 8/8 全部占用      │
└────────────────────────┴───────────────────┴───────────────────┘
```

> **异常**: 虚拟线程本应更高效，但性能反而下降 75%。CPU 低利用率 + carrier thread 全部占用 = Pinning 的典型症状。

---

## 4. 第二阶段：Pinning 检测

### 4.1 JFR 事件检测

```bash
# 启动时开启 VirtualThreadPinned 事件
java -XX:StartFlightRecording=+jdk.VirtualThreadPinned#threshold=10ms,filename=pinning.jfr ...
```

### 4.2 JFR 分析结果（JDK Mission Control）

```
jdk.VirtualThreadPinned 事件 (示意):
┌────────────────────────────────────────────────────────────┐
│ 事件数:     12,456 次 (1 小时内)                           │
│ 总钉住时间: 3,240 秒                                      │
│ 最大钉住:   850ms                                         │
│                                                            │
│ 热点调用栈 Top 3:                                          │
│ 1. DataSyncService.syncWithLock() → synchronized (6,200次)│
│ 2. HikariProxyConnection.prepareStatement() → native (3,800次)│
│ 3. Jackson ObjectMapper.writeValueAsString() → synchronized (2,456次)│
└────────────────────────────────────────────────────────────┘
```

### 4.3 JVM 诊断

```bash
# 查看虚拟线程调度器状态
jcmd <pid> Thread.vthread_scheduler

# 输出:
# Carrier thread count: 8
# Number of mounted virtual threads: 8  ← 全部被钉住
# Number of queued virtual threads: 4,982  ← 队列积压
```

---

## 5. 第三阶段：代码定位

### 5.1 热点 1: synchronized 同步方法

```java
// 问题代码: 使用 synchronized 保护共享状态
public class DataSyncService {
    private final Map<String, SyncStatus> syncStatusMap = new HashMap<>();

    // ❌ synchronized 导致虚拟线程 pinning
    public synchronized void syncWithLock(ExternalData data) {
        SyncStatus status = syncStatusMap.computeIfAbsent(
            data.getId(), k -> new SyncStatus());
        status.update(data);
        // ... 网络调用和数据库写入（阻塞操作）
        saveToDatabase(data);  // 阻塞 I/O
    }
}
```

### 5.2 热点 2: JDBC 连接的 synchronized

```java
// HikariCP 的 JDBC 连接代理内部使用 synchronized
// 当虚拟线程在 synchronized 块内阻塞时，carrier thread 被钉住
connection.prepareStatement(sql);  // 内部 synchronized
```

### 5.3 热点 3: Jackson ObjectMapper

```java
// Jackson ObjectMapper 内部有 synchronized 缓存
objectMapper.writeValueAsString(data);  // 内部 synchronized
```

---

## 6. 第四阶段：修复方案

### 6.1 修复热点 1: synchronized → ReentrantLock

```java
// ✅ 使用 ReentrantLock 替代 synchronized
public class DataSyncService {
    private final ConcurrentHashMap<String, SyncStatus> syncStatusMap = new ConcurrentHashMap<>();
    private final ReentrantLock lock = new ReentrantLock();

    public void syncWithLock(ExternalData data) {
        // 使用 ConcurrentHashMap 避免 synchronized
        SyncStatus status = syncStatusMap.computeIfAbsent(
            data.getId(), k -> new SyncStatus());
        status.update(data);

        // 使用 ReentrantLock (可卸载)
        lock.lock();
        try {
            saveToDatabase(data);
        } finally {
            lock.unlock();
        }
    }
}
```

### 6.2 修复热点 2: 虚拟线程安全的连接池

```java
// ✅ 使用虚拟线程适配的连接池配置
HikariConfig config = new HikariConfig();
config.setMaximumPoolSize(50);  // 限制连接数
config.setMinimumIdle(10);

// 关键: 不使用 synchronized 的连接代理
// JDK 21+ 的 JDBC 驱动已针对虚拟线程优化
```

### 6.3 修复热点 3: 线程安全的 JSON 序列化

```java
// ✅ 使用 ObjectMapper 的线程安全方式
private static final ObjectMapper MAPPER = new ObjectMapper();
// ObjectMapper 本身是线程安全的（内部 serializationConfig 不可变）
// 但避免在序列化过程中使用 synchronized 的自定义模块
```

### 6.4 JDK 版本升级

JDK 25+ 大幅减少了虚拟线程 pinning 的场景：
- `Object.wait()` 在 JDK 24+ 不再 pinning
- 许多 `synchronized` 用法在 JDK 25+ 可自动卸载

---

## 7. 最终效果对比

| 指标 | 修复前 | 修复后 |
|------|--------|--------|
| 吞吐量 | 2,000 tasks/s | 12,000 tasks/s |
| CPU 利用率 | 30% | 72% |
| P99 延迟 | 5,000ms | 350ms |
| Pinning 事件数 | 12,456/小时 | 120/小时 |
| Carrier thread 占用 | 8/8 全部 | 3-5/8 |

---

## 8. 经验总结与 Checklist

### Virtual Thread Pinning 排查 Checklist

- [ ] 启用 JFR `jdk.VirtualThreadPinned` 事件（阈值 10-20ms）
- [ ] 检查 `jcmd Thread.vthread_scheduler` 的 carrier 使用率
- [ ] 搜索代码中的 `synchronized` 关键字
- [ ] 搜索第三方库中的 synchronized（JDBC 驱动、Jackson 等）
- [ ] 使用 `ReentrantLock` 替换 `synchronized`
- [ ] 考虑使用 `ConcurrentHashMap` 等无锁替代方案
- [ ] 在 staging 环境做压测验证

### Pinning 场景速查

| 场景 | 是否 Pinning | 替代方案 |
|------|-------------|---------|
| `synchronized` 方法/块 | ✅ Pinning | `ReentrantLock` |
| `Object.wait()` | JDK 21 ✅ / JDK 24+ ❌ | `Condition.await()` |
| JNI 调用 | ✅ Pinning | Foreign Function API |
| `Thread.sleep()` | ❌ 不 pinning | - |
| `BlockingQueue.take()` | ❌ 不 pinning | - |
| `Socket I/O` | ❌ 不 pinning | - |
| `ReentrantLock.lock()` | ❌ 不 pinning | - |

### 相关资源

- [Virtual Thread 迁移案例](virtual-threads-migration.md)
- [Virtual Thread 实现分析](/deep-dive/virtual-thread-implementation.md)
- [JDK-8354894: Virtual Thread Starvation](/issues/jdk-8354894.md)
- [JEP 444: Virtual Threads](/jeps/concurrency/jep-444.md)
