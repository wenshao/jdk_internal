# JFR Method Timing 深度分析

> JDK 25 正式特性 - JEP 520

---
## 目录

1. [概述](#1-概述)
2. [背景与动机](#2-背景与动机)
3. [核心机制](#3-核心机制)
4. [使用方式](#4-使用方式)
5. [与现有工具对比](#5-与现有工具对比)
6. [性能开销](#6-性能开销)
7. [实战示例](#7-实战示例)
8. [相关链接](#8-相关链接)

---


## 1. 概述

JEP 520 为 JFR (Java Flight Recorder) 新增方法级计时事件，允许开发者以极低开销追踪特定方法的执行时间，无需修改代码或使用外部 Agent。

---

## 2. 背景与动机

### 现有方案的问题

| 方案 | 问题 |
|------|------|
| 手动计时 (`System.nanoTime()`) | 侵入代码、难以全面覆盖 |
| Java Agent (ByteBuddy) | 部署复杂、启动时注入有延迟 |
| Async Profiler | 采样式、可能错过短方法 |
| JFR Method Sampling | 采样不精确、无法追踪特定方法 |

### JFR Method Timing 的优势

- **零代码侵入**: 通过 JFR 配置即可启用
- **低开销**: JIT 编译器层面插桩，开销 < 1%
- **精确计时**: 非采样式，记录每次调用的精确耗时
- **灵活过滤**: 可指定类、方法、包级别的过滤

---

## 3. 核心机制

### 实现原理

```
JFR Method Timing 工作流:

1. 配置阶段
   ┌──────────────┐
   │ .jfc 配置文件  │ ← 指定要追踪的方法
   └──────┬───────┘
          ↓
2. JIT 编译阶段
   ┌──────────────┐
   │ C2 编译器     │ ← 在目标方法入口/出口插入计时代码
   └──────┬───────┘
          ↓
3. 运行时阶段
   ┌──────────────┐
   │ 方法执行      │ ← 记录 (方法, 开始时间, 结束时间, 线程)
   └──────┬───────┘
          ↓
4. 输出阶段
   ┌──────────────┐
   │ JFR 缓冲区   │ → .jfr 文件
   └──────────────┘
```

### JFR 事件定义

```java
// JFR 内部事件类型
@Name("jdk.MethodTiming")
@Label("Method Timing")
@Category("Java Application")
class MethodTimingEvent extends jdk.jfr.Event {
    @Label("Method")
    Method method;

    @Label("Duration")
    @Timespan
    long duration;

    @Label("Invocation Count")
    long invocationCount;
}
```

---

## 4. 使用方式

### 基本用法

```bash
# 启用方法计时录制
java -XX:StartFlightRecording=settings=profile,filename=app.jfr MyApp
```

### 自定义 .jfc 配置

```xml
<!-- method-timing.jfc -->
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <event name="jdk.MethodTiming">
        <setting name="enabled">true</setting>
        <setting name="threshold">1 ms</setting>
        <setting name="filter">
            com.myapp.service.*
        </setting>
    </event>
</configuration>
```

```bash
# 使用自定义配置
java -XX:StartFlightRecording=settings=method-timing.jfc,filename=timing.jfr MyApp
```

### jcmd 运行时控制

```bash
# 动态开始方法计时
jcmd <pid> JFR.start name=timing settings=profile

# 指定录制时长
jcmd <pid> JFR.start name=timing duration=60s settings=profile

# 导出数据
jcmd <pid> JFR.dump name=timing filename=timing.jfr

# 停止
jcmd <pid> JFR.stop name=timing
```

### 分析结果

```bash
# 查看方法计时事件
jfr print --events "jdk.MethodTiming" timing.jfr

# 按耗时排序
jfr print --events "jdk.MethodTiming" --stack-depth 5 timing.jfr

# JSON 格式输出
jfr print --json --events "jdk.MethodTiming" timing.jfr
```

---

## 5. 与现有工具对比

| 特性 | JFR Method Timing | Async Profiler | Java Agent | 手动计时 |
|------|-------------------|----------------|------------|----------|
| 精确度 | 精确 (每次调用) | 采样 | 精确 | 精确 |
| 开销 | <1% | <2% | 1-5% | ~0% |
| 代码侵入 | 无 | 无 | 无 | 有 |
| 部署复杂度 | 低 (JVM 内置) | 中 | 中 | 低 |
| 过滤粒度 | 方法/类/包 | 方法 | 自定义 | 手动 |
| 生产可用 | ✅ | ✅ | ⚠️ | ✅ |
| 与 JFR 集成 | 原生 | 可导出 | 需编写 | 不集成 |

---

## 6. 性能开销

### 开销来源

1. **方法入口**: 读取时钟 (`rdtsc` 指令，~20ns)
2. **方法出口**: 读取时钟 + 写入 JFR 缓冲区 (~50ns)
3. **总开销**: 每次调用约 70ns

### 开销控制

```xml
<!-- 使用 threshold 过滤短方法，降低开销 -->
<event name="jdk.MethodTiming">
    <setting name="threshold">10 ms</setting>  <!-- 只记录 >10ms 的调用 -->
</event>
```

### 开销评估

| 方法调用频率 | 无 JFR | 方法计时 (无过滤) | 方法计时 (10ms 过滤) |
|------------|--------|-----------------|-------------------|
| 1K/sec | 基准 | +0.007% | ~0% |
| 100K/sec | 基准 | +0.7% | ~0% |
| 10M/sec | 基准 | +70% ⚠️ | ~0% |

**建议**: 高频方法使用 threshold 过滤，避免追踪每秒调用百万次以上的热点方法。

---

## 7. 实战示例

### 定位慢 SQL 调用

```xml
<!-- 追踪数据库操作 -->
<event name="jdk.MethodTiming">
    <setting name="enabled">true</setting>
    <setting name="threshold">100 ms</setting>
    <setting name="filter">
        java.sql.Statement.execute*
        java.sql.PreparedStatement.execute*
    </setting>
</event>
```

### 追踪 HTTP 请求处理

```xml
<!-- 追踪 Servlet 处理 -->
<event name="jdk.MethodTiming">
    <setting name="enabled">true</setting>
    <setting name="threshold">50 ms</setting>
    <setting name="filter">
        jakarta.servlet.http.HttpServlet.service
        org.springframework.web.servlet.DispatcherServlet.*
    </setting>
</event>
```

---

## 8. 相关链接

- [JEP 520: JFR Method Timing](https://openjdk.org/jeps/520)
- [JFR 完整指南](/guides/jfr.md)
- [JDK 25 性能调优](../performance.md)
- [JDK 25 主页](../README.md)

---

[← 返回 JDK 25 深度分析](../)
