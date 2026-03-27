---

# 死锁诊断：支付系统分布式锁死锁排查

> **声明**：本文中所有监控数据、线程转储、性能指标均为 **示意数据（illustrative data）**，实际结果取决于工作负载、硬件环境和应用架构。

---

## 目录

1. [背景与问题描述](#1-背景与问题描述)
2. [环境信息](#2-环境信息)
3. [第一阶段：问题发现](#3-第一阶段问题发现)
4. [第二阶段：线程转储分析](#4-第二阶段线程转储分析)
5. [第三阶段：根因定位](#5-第三阶段根因定位)
6. [第四阶段：修复方案](#6-第四阶段修复方案)
7. [最终效果对比](#7-最终效果对比)
8. [经验总结与 Checklist](#8-经验总结与-checklist)

---

## 1. 背景与问题描述

### 1.1 业务场景

**跨境支付系统**，涉及多币种、多账户的转账操作。每笔转账需要同时锁定双方账户，确保余额一致性。

### 1.2 问题现象

- **接口超时**：约每 2-3 天出现一批转账请求超时（30s timeout）
- **线程耗尽**：Tomcat 线程池被占满，新请求无法处理
- **自动恢复**：超时后部分请求释放锁，系统恢复正常
- **无报错日志**：日志中只有 timeout 异常，无明显 error

---

## 2. 环境信息

```
应用架构:    Spring Boot 3.1 + MyBatis + Redis (分布式锁)
JDK 版本:    JDK 21.0.2
容器:        4C8G × 3 副本
数据库:      MySQL 8.0 (RDS)
分布式锁:    Redisson 3.24 (Redis 分布式锁)
线程模型:    Tomcat 默认线程池 (200 线程)
```

---

## 3. 第一阶段：问题发现

### 3.1 监控告警

```
告警时间:    2026-02-14 14:32:18
告警内容:    接口 /api/transfer 平均响应时间 > 10s (阈值 5s)
持续时间:    约 8 分钟
影响范围:    3 个副本中的 2 个
```

### 3.2 快速诊断

```bash
# 查看线程池状态
jcmd <pid> Thread.print -l > thread_dump.txt

# 查看 Tomcat 线程使用
curl http://localhost:8080/actuator/metrics/tomcat.threads.busy
# 结果: 198/200 线程忙碌（几乎耗尽）
```

---

## 4. 第二阶段：线程转储分析

### 4.1 线程转储关键片段

```
Found one Java-level deadlock:
=============================
"tomcat-thread-47":
  waiting to lock monitor 0x00007f8b3c02a890 (object 0x0000000701a2b5c0, a com.example.service.AccountLock),
  which is held by "tomcat-thread-123"

"tomcat-thread-123":
  waiting to lock monitor 0x00007f8b3c02a860 (object 0x0000000701a2b5f0, a com.example.service.AccountLock),
  which is held by "tomcat-thread-47"
```

### 4.2 死锁链分析

```
┌──────────────────────────────────────────────────────────┐
│                      Deadlock Cycle                       │
│                                                          │
│  Thread-47: transfer(A→B)                                │
│    ├─ lock(Account A) ✅ 已获取                          │
│    └─ lock(Account B) ⏳ 等待 Thread-123                 │
│                                                          │
│  Thread-123: transfer(B→A)                               │
│    ├─ lock(Account B) ✅ 已获取                          │
│    └─ lock(Account A) ⏳ 等待 Thread-47                  │
│                                                          │
│  结果: 两个线程互相等待 → 死锁                            │
└──────────────────────────────────────────────────────────┘
```

---

## 5. 第三阶段：根因定位

### 5.1 问题代码

```java
// 问题代码: 锁获取顺序不一致
public class TransferService {

    public void transfer(String fromAccount, String toAccount, BigDecimal amount) {
        // 问题: 按参数顺序获取锁
        // A→B 转账: 先锁 A，再锁 B
        // B→A 转账: 先锁 B，再锁 A
        // 如果两个请求同时发生 → 死锁
        synchronized (getLock(fromAccount)) {
            synchronized (getLock(toAccount)) {
                debit(fromAccount, amount);
                credit(toAccount, amount);
            }
        }
    }
}
```

### 5.2 根因

1. **锁排序不一致**: 按参数顺序获取锁，而非按固定顺序（如账户 ID 的字典序）
2. **锁粒度过粗**: 使用 `synchronized` 锁住整个转账流程，持有时间长
3. **无超时机制**: `synchronized` 无超时，死锁后无法自动恢复

---

## 6. 第四阶段：修复方案

### 方案一：固定锁顺序（推荐）

```java
// 修复: 始终按固定顺序获取锁
public void transfer(String fromAccount, String toAccount, BigDecimal amount) {
    // 按账户 ID 排序，确保所有线程按相同顺序获取锁
    String first = fromAccount.compareTo(toAccount) < 0 ? fromAccount : toAccount;
    String second = fromAccount.compareTo(toAccount) < 0 ? toAccount : fromAccount;

    synchronized (getLock(first)) {
        synchronized (getLock(second)) {
            if (first.equals(fromAccount)) {
                debit(fromAccount, amount);
                credit(toAccount, amount);
            } else {
                credit(toAccount, amount);
                debit(fromAccount, amount);
            }
        }
    }
}
```

### 方案二：使用 ReentrantLock + tryLock（带超时）

```java
// 更优: 使用 tryLock 带超时，避免永久阻塞
private final ConcurrentHashMap<String, ReentrantLock> locks = new ConcurrentHashMap<>();

public void transfer(String fromAccount, String toAccount, BigDecimal amount)
        throws InterruptedException {
    ReentrantLock lock1 = locks.computeIfAbsent(
        min(fromAccount, toAccount), k -> new ReentrantLock());
    ReentrantLock lock2 = locks.computeIfAbsent(
        max(fromAccount, toAccount), k -> new ReentrantLock());

    if (lock1.tryLock(5, TimeUnit.SECONDS)) {
        try {
            if (lock2.tryLock(5, TimeUnit.SECONDS)) {
                try {
                    debit(fromAccount, amount);
                    credit(toAccount, amount);
                } finally {
                    lock2.unlock();
                }
            } else {
                throw new TransferException("Cannot acquire lock, please retry");
            }
        } finally {
            lock1.unlock();
        }
    } else {
        throw new TransferException("Cannot acquire lock, please retry");
    }
}
```

### 方案三：分布式锁全局排序

```java
// 分布式环境: 使用 Redisson 的公平锁 + 固定顺序
public void transfer(String fromAccount, String toAccount, BigDecimal amount) {
    String first = min(fromAccount, toAccount);
    String second = max(fromAccount, toAccount);

    RLock lock1 = redisson.getFairLock("account:" + first);
    RLock lock2 = redisson.getFairLock("account:" + second);

    lock1.lock(10, TimeUnit.SECONDS);
    try {
        lock2.lock(10, TimeUnit.SECONDS);
        try {
            debit(fromAccount, amount);
            credit(toAccount, amount);
        } finally {
            lock2.unlock();
        }
    } finally {
        lock1.unlock();
    }
}
```

---

## 7. 最终效果对比

| 指标 | 修复前 | 方案一 | 方案二 |
|------|--------|--------|--------|
| 死锁发生 | 每 2-3 天 | 0 | 0 |
| 超时率 | 0.5% | 0 | <0.01% (可重试) |
| P99 延迟 | 不稳定 | 35ms | 40ms |
| 代码复杂度 | 低 | 低 | 中 |

---

## 8. 经验总结与 Checklist

### 死锁排查 Checklist

- [ ] 获取线程转储（`jcmd <pid> Thread.print -l`）
- [ ] 查找 "Found one Java-level deadlock" 关键字
- [ ] 分析死锁环（哪个线程持有哪个锁，等待哪个锁）
- [ ] 检查锁获取顺序是否一致
- [ ] 检查是否有嵌套锁获取
- [ ] 检查是否有 `synchronized` 嵌套或 `ReentrantLock` 嵌套
- [ ] 确认是否有锁超时机制

### 死锁预防原则

1. **固定锁顺序**: 所有线程按相同顺序获取多把锁（最有效）
2. **使用 tryLock + 超时**: 避免无限等待，提供优雅降级
3. **减小锁粒度**: 缩小临界区范围，减少持有时间
4. **避免嵌套锁**: 尽量一次只持有一把锁
5. **使用 JFR 持续监控**: `JavaMonitorWait` 和 `JavaMonitorBlocked` 事件

### 相关资源

- [内存泄漏诊断](memory-leak-diagnosis.md)
- [虚拟线程迁移](virtual-threads-migration.md)
- [并发编程主题](/by-topic/concurrency/concurrency/)
