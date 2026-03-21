# Erik Gahlin

> **GitHub**: [@egahlin](https://github.com/egahlin)
> **Twitter**: [@ErikGahlin](https://x.com/ErikGahlin)
> **Blog**: [egahlin.github.io](https://egahlin.github.io/)
> **Organization**: Oracle

---
## 目录

1. [概述](#1-概述)
2. [基本信息](#2-基本信息)
3. [技术影响力](#3-技术影响力)
4. [技术特长](#4-技术特长)
5. [代表性工作](#5-代表性工作)
6. [外部资源](#6-外部资源)
7. [贡献概览](#7-贡献概览)
8. [PR 列表](#8-pr-列表)
9. [关键贡献详解](#9-关键贡献详解)
10. [开发风格](#10-开发风格)
11. [相关链接](#11-相关链接)

---


## 1. 概述

Erik Gahlin 是 Oracle HotSpot Runtime 团队核心成员，JDK Flight Recorder (JFR) 的主要作者和设计者。他负责 `jdk.jfr` 和 `jdk.management.jfr` 模块的 API 设计和实现。在加入 JVM 团队之前，曾在 Java Mission Control (JMC) 团队工作。他是 JEP 349 (JFR Event Streaming) 的共同作者，并定期撰写关于 JDK 新版本中 JFR 更新的技术文章。

---

## 2. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Erik Gahlin |
| **当前组织** | Oracle |
| **团队** | HotSpot Runtime Team |
| **GitHub** | [@egahlin](https://github.com/egahlin) |
| **Twitter/X** | [@ErikGahlin](https://x.com/ErikGahlin) |
| **Blog** | [egahlin.github.io](https://egahlin.github.io/) |
| **OpenJDK** | [@egahlin](https://openjdk.org/census#egahlin) |
| **角色** | JDK Reviewer |
| **PRs** | [322 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Aegahlin+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | JFR (Java Flight Recorder), JMX, 性能监控 |
| **主导 JEP** | JEP 520: JFR Method Timing and Tracing, JEP 349: JFR Event Streaming |
| **活跃时间** | 2013 - 至今 |

> **数据来源**: [Inside.java](https://inside.java/u/ErikGahlin/), [个人博客](https://egahlin.github.io/), [Twitter](https://x.com/ErikGahlin)

### 最近 10 个 Integrated PRs (2026 年 2-3 月)

| PR # | Issue | 标题 | 日期 |
|------|-------|------|------|
| #30243 | 8380037 | JFR: Don't format identifiers as numbers | Mar 16, 2026 |
| #30228 | 8379917 | JFR: Method timing event can have incorrect minimum value | Mar 13, 2026 |
| #29791 | 8378171 | JFR: Copy of a closed recording should not be available | Feb 19, 2026 |
| #29191 | 8372321 | TestBackToBackSensitive fails intermittently after JDK-8365972 backport | Jan 14, 2026 |
| #29117 | 8372321 | TestBackToBackSensitive fails intermittently after JDK-8365972 | Jan 12, 2026 |
| #28947 | 8367949 | JFR: MethodTrace double-counts methods that catch their own exceptions | Jan 8, 2026 |
| #28636 | 8373024 | JFR: CPU throttle rate can't handle incorrect values | Dec 4, 2025 |
| #28481 | 8372441 | JFR: Improve logging of TestBackToBackSensitive | Nov 25, 2025 |
| #28153 | 8365972 | JFR: ThreadDump and ClassLoaderStatistics events may cause back to back rotations | Nov 10, 2025 |
| #28135 | 8370884 | JFR: Overflow in aggregators | Nov 6, 2025 |

> **观察**: 最近工作集中在 **JFR 方法跟踪**、**事件准确性修复** 和 **测试稳定性**

---

## 3. 技术影响力

| 指标 | 值 |
|------|-----|
| **代码行数** | +190,055 / -33,295 (净 +156,760) |
| **影响模块** | jdk.jfr |
| **主要贡献** | JFR 核心开发、事件流、查询工具 |

> 💡 **JFR 核心开发者**: 净添加 156,760 行代码，是 JFR 模块的主要贡献者

### 影响的主要目录

| 目录 | 文件数 | 说明 |
|------|--------|------|
| jdk/jfr/internal | 490 | JFR 内部实现 |
| jdk/jfr/internal/consumer | 161 | JFR 消费者 API |
| jdk/jfr | 160 | JFR 公共 API |

---

## 4. 技术特长

`JFR` `Java Flight Recorder` `性能监控` `事件流` `诊断工具` `JEP 520`

---

## 5. 代表性工作

### 1. JEP 520: JFR Method Timing and Tracing
**Issue**: [JDK-8370037](https://bugs.openjdk.org/browse/JDK-8370037)

JFR 方法计时和追踪，提供详细的方法执行性能数据。

### 2. JFR 核心开发者
Java Flight Recorder 的主要开发者，JFR 是 JDK 内置的低开销性能监控工具。

### 3. JFR 流式 API
改进 JFR 事件流处理，支持实时事件消费。

### 4. JFR 查询工具
改进 jfr query 命令行工具，提供更强大的查询能力。

### 5. JFR 事件扩展
添加新的 JFR 事件类型，扩展监控能力。

---

## 6. 外部资源

### 个人博客

Erik 在 [egahlin.github.io](https://egahlin.github.io/) 撰写关于 JDK Flight Recorder、OpenJDK 和 Java 的技术文章：

| 标题 | 主题 | 链接 |
|------|------|------|
| "What's new for JFR in JDK 25" | JDK 25 JFR 新功能 | [博客](https://egahlin.github.io/) |
| "JDK 21 JFR view command" | JDK 21 JFR 视图命令 | [博客](https://egahlin.github.io/) |

### 链接

| 类型 | 链接 |
|------|------|
| **GitHub** | [@egahlin](https://github.com/egahlin) |
| **Twitter/X** | [@ErikGahlin](https://x.com/ErikGahlin) |
| **Blog** | [egahlin.github.io](https://egahlin.github.io/) |
| **OpenJDK Census** | [@egahlin](https://openjdk.org/census#egahlin) |
| **Inside.java** | [ErikGahlin](https://inside.java/u/ErikGahlin/) |

### JEP 贡献

| JEP | 标题 | 角色 |
|-----|------|------|
| [JEP 349](https://openjdk.org/jeps/349) | JFR Event Streaming | Co-author |
| [JEP 520](https://openjdk.org/jeps/520) | JFR Method Timing and Tracing | Lead |

---

## 7. 贡献概览

### 按类别统计

| 类别 | 数量 | 占比 |
|------|------|------|
| JFR 改进 | 55 | 74% |
| JEP 实现 | 5 | 7% |
| Bug 修复 | 10 | 14% |
| 测试 | 4 | 5% |

### 关键成就

- **JEP 520**: JFR Method Timing and Tracing
- **JFR 流式 API**: 改进事件流处理
- **JFR 查询**: 改进 jfr query 工具

---

## 8. PR 列表

### JEP 520: JFR Method Timing and Tracing

| Issue | 标题 | 描述 |
|-------|------|------|
| 8352738 | Implement JEP 520: JFR Method Timing and Tracing | **核心实现** |

### JFR 核心改进

| Issue | 标题 | 描述 |
|-------|------|------|
| 8372441 | JFR: Improve logging of TestBackToBackSensitive | 日志改进 |
| 8365972 | JFR: ThreadDump and ClassLoaderStatistics events may cause back to back rotations | 旋转问题修复 |
| 8370884 | JFR: Overflow in aggregators | 聚合器溢出修复 |
| 8370242 | JFR: Clear event reference eagerly when using EventStream | 事件流引用清理 |
| 8369510 | JFR: Remove flush handler from Dispatcher lookup | 分发器优化 |
| 8368670 | Deadlock in JFR on event register + class load | 死锁修复 |
| 8368809 | JFR: Remove events from testSettingConfiguration in TestActiveSettingEvent | 测试清理 |
| 8368563 | JFR: Improve jfr query help text | 帮助文本改进 |
| 8366896 | JFR: Use GarbageCollection.name in gc view | GC 视图改进 |
| 8366809 | JFR: Use factory for aggregator functions | 聚合器工厂 |
| 8367948 | JFR: MethodTrace threshold setting has no effect | 阈值设置修复 |
| 8367107 | JFR: Refactor policy tests out of TestRemoteDump | 测试重构 |
| 8365815 | JFR: Update metadata.xml with 'jfr query' examples | 元数据更新 |
| 8365614 | JFR: Improve PrettyWriter::printValue | 打印改进 |
| 8365636 | JFR: Minor cleanup | 清理 |
| 8365550 | JFR: The active-settings view should not use LAST_BATCH | 视图修复 |
| 8365638 | JFR: Add --exact for debugging out-of-order events | 调试选项 |
| 8364556 | JFR: Disable SymbolTableStatistics and StringTableStatistics in default.jfc | 默认配置优化 |
| 8364756 | JFR: Improve slow tests | 测试优化 |
| 8364993 | JFR: Disable jdk.ModuleExport in default.jfc | 默认配置优化 |
| 8364667 | JFR: Throttle doesn't work with dynamic events | 节流修复 |
| 8364316 | JFR: Incorrect validation of mirror fields | 验证修复 |
| 8364190 | JFR: RemoteRecordingStream withers don't work | 远程流修复 |
| 8364461 | JFR: Default constructor may not be first in setting control | 构造函数顺序修复 |
| 8364427 | JFR: Possible resource leak in Recording::getStream | 资源泄漏修复 |
| 8364257 | JFR: User-defined events and settings with a one-letter name cannot be configured | 配置修复 |

### JFR 测试修复

| Issue | 标题 | 描述 |
|-------|------|------|
| 8369982 | ProblemList jdk/jfr/jvm/TestWaste.java | 测试问题列表 |
| 8282427 | jdk/jfr/jvm/TestWaste.java is failing with "exit code 139" | 测试失败修复 |
| 8247776 | JFR: TestThreadContextSwitches.java failed "RuntimeException: No events" | 测试修复 |
| 8365630 | jdk/jfr/tool/TestPrintContextual.java fails with wrong spanId | 测试修复 |

---

## 9. 关键贡献详解

### 1. JEP 520: JFR Method Timing and Tracing

**背景**: 需要更精确的方法执行时间测量。

**解决方案**: 新增方法计时和追踪事件。

```java
// 新增事件类型
@Label("Method Timing")
class MethodTimingEvent extends Event {
    @Label("Method")
    Method method;
    
    @Label("Duration")
    long duration;
    
    @Label("Count")
    long count;
}

// 使用示例
try (var event = new MethodTimingEvent()) {
    event.method = MyClass.class.getMethod("myMethod");
    // 方法执行
    myMethod();
    event.duration = ...;
}
```

**配置**:

```bash
# 启用方法计时
-XX:StartFlightRecording=settings=profile,method-timing=true

# 使用 jfr query 分析
jfr print --json recording.jfr | jfr query "SELECT method, avg(duration) FROM MethodTiming"
```

**影响**: 提供了更精确的性能分析能力。

### 2. JFR 事件流优化 (JDK-8370242)

**问题**: EventStream 使用时事件引用未及时清理。

**解决方案**: 及时清理事件引用。

```java
// 变更前
public void onEvent(Consumer<RecordedEvent> action) {
    events.add(event);  // 引用未清理
    action.accept(event);
}

// 变更后
public void onEvent(Consumer<RecordedEvent> action) {
    try {
        action.accept(event);
    } finally {
        event = null;  // 及时清理
    }
}
```

**影响**: 减少了内存占用。

### 3. JFR 死锁修复 (JDK-8368670)

**问题**: 事件注册和类加载可能发生死锁。

**解决方案**: 改进锁顺序。

```java
// 变更前: 可能死锁
synchronized (eventRegistry) {
    Class<?> cls = Class.forName(eventName);  // 可能触发类加载
}

// 变更后: 避免死锁
Class<?> cls = Class.forName(eventName);  // 类加载在外部
synchronized (eventRegistry) {
    registerEvent(cls);
}
```

**影响**: 消除了潜在的死锁问题。

---

## 10. 开发风格

Erik 的贡献特点:

1. **JFR 专家**: 深入理解 JFR 架构
2. **性能导向**: 专注于低开销监控
3. **API 设计**: 注重 API 的易用性
4. **测试驱动**: 每个改动都有充分的测试

---

## 11. 相关链接

- [OpenJDK Changesets](https://hg.openjdk.org/jdk/jdk/user?user=egahlin)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=Erik%20Gahlin)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=assignee%20%3D%20egahlin)
- [JFR Documentation](https://docs.oracle.com/en/java/javase/26/jfapi/)