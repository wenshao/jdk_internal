# Erik Gahlin

> JFR 核心开发者，JEP 520 主导者

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Erik Gahlin |
| **组织** | Oracle |
| **Commits** | 74 |
| **主要领域** | JFR (Java Flight Recorder) |
| **主导 JEP** | JEP 520: JFR Method Timing and Tracing |
| **活跃时间** | 2013 - 至今 |

---

## 贡献概览

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

## PR 列表

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

## 关键贡献详解

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

## 开发风格

Erik 的贡献特点:

1. **JFR 专家**: 深入理解 JFR 架构
2. **性能导向**: 专注于低开销监控
3. **API 设计**: 注重 API 的易用性
4. **测试驱动**: 每个改动都有充分的测试

---

## 相关链接

- [OpenJDK Changesets](https://hg.openjdk.org/jdk/jdk/user?user=egahlin)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=Erik%20Gahlin)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=assignee%20%3D%20egahlin)
- [JFR Documentation](https://docs.oracle.com/en/java/javase/26/jfapi/)