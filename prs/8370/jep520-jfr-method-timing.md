# JFR 方法计时追踪

> JEP 520 | Erik Gahlin | JDK 26

---

## 概述

JEP 520 为 JFR (Java Flight Recorder) 实现了**方法级计时追踪**功能，允许开发者精确测量方法的执行时间，无需修改代码。

| 属性 | 值 |
|------|-----|
| **JEP** | [JEP 520](https://openjdk.org/jeps/520) |
| **作者** | Erik Gahlin |
| **目标版本** | JDK 26 |
| **重要性** | ⭐⭐⭐ 性能分析关键 |
| **影响** | 精确方法级性能分析 |

---

## 背景

### 传统性能分析

```
传统 JFR 事件:

┌─────────────────────────────────────────────────────────────┐
│  事件: MethodInvocation                                     │
│  时间戳: 12:34:56.789                                       │
│  方法: com.example.MyClass.processData()                    │
│  线程: main                                                 │
└─────────────────────────────────────────────────────────────┘

问题:
1. 只有方法调用事件，没有执行时间
2. 需要手动计算时间差
3. 开销大，影响生产性能
```

### JEP 520 解决方案

```
JFR 方法计时:

┌─────────────────────────────────────────────────────────────┐
│  事件: MethodTiming                                         │
│  开始时间: 12:34:56.789.123                                 │
│  结束时间: 12:34:56.789.456                                 │
│  执行时间: 333 μs                                           │
│  方法: com.example.MyClass.processData()                    │
│  线程: main                                                 │
│  调用栈: [method1, method2, processData]                    │
└─────────────────────────────────────────────────────────────┘

优势:
1. 精确的方法执行时间
2. 低开销 (<1%)
3. 支持选择性追踪
```

---

## 技术实现

### 文件变更

```
src/hotspot/share/jfr/
├── methodTracing/
│   ├── jfrMethodTracing.cpp        (新增: 核心实现)
│   ├── jfrMethodTracing.hpp
│   ├── jfrMethodTimer.cpp          (新增: 计时器)
│   └── jfrMethodTimer.hpp
├── metadata.xml                    (修改: 事件定义)
└── jfrEvents.cpp                   (修改: 事件生成)

src/java.base/share/classes/jdk/jfr/
├── MethodTiming.java               (新增: 配置类)
├── MethodTimingEvent.java          (新增: 事件类)
└── events/
    └── MethodTimingEvent.java      (新增: 内置事件)
```

### 事件定义

```java
// 文件: src/java.base/share/classes/jdk/jfr/events/MethodTimingEvent.java

package jdk.jfr.events;

import jdk.jfr.*;

/**
 * 方法计时事件
 * 记录方法的执行时间
 */
@Label("Method Timing")
@Category("Java Method")
@Description("Execution timing for a method")
@StackTrace(true)
@Timestamp(Timestamp.TICKS)
public final class MethodTimingEvent extends Event {

    /**
     * 执行的类
     */
    @Label("Class")
    public Class<?> eventClass;

    /**
     * 执行的方法名
     */
    @Label("Method Name")
    public String methodName;

    /**
     * 方法描述符
     */
    @Label("Method Descriptor")
    public String methodDescriptor;

    /**
     * 执行时间 (纳秒)
     */
    @Label("Execution Time")
    @Timespan(Timespan.NANOSECONDS)
    public long executionTime;

    /**
     * 分配的字节数
     */
    @Label("Allocation Size")
    @DataAmount(DataAmount.BYTES)
    public long allocationSize;

    /**
     * 是否抛出异常
     */
    @Label("Exception Thrown")
    public boolean exceptionThrown;

    /**
     * 调用深度
     */
    @Label("Call Depth")
    public int callDepth;
}
```

### 配置 API

```java
// 文件: src/java.base/share/classes/jdk/jfr/MethodTiming.java

package jdk.jfr;

import java.util.*;
import java.util.regex.Pattern;

/**
 * 方法计时配置
 * 
 * 用于配置哪些方法需要计时追踪
 */
public final class MethodTiming {

    /**
     * 创建配置构建器
     */
    public static Builder newBuilder() {
        return new Builder();
    }

    /**
     * 配置构建器
     */
    public static final class Builder {
        private final List<Pattern> includePatterns = new ArrayList<>();
        private final List<Pattern> excludePatterns = new ArrayList<>();
        private long thresholdNanos = 0;
        private boolean trackAllocations = true;
        private boolean trackExceptions = true;
        private int maxCallDepth = 64;

        /**
         * 包含指定的类/方法
         * @param pattern 类/方法名模式 (支持通配符)
         */
        public Builder include(String pattern) {
            includePatterns.add(Pattern.compile(wildcardToRegex(pattern)));
            return this;
        }

        /**
         * 排除指定的类/方法
         */
        public Builder exclude(String pattern) {
            excludePatterns.add(Pattern.compile(wildcardToRegex(pattern)));
            return this;
        }

        /**
         * 设置计时阈值 (低于此时间不记录)
         */
        public Builder threshold(long nanos) {
            this.thresholdNanos = nanos;
            return this;
        }

        /**
         * 是否追踪内存分配
         */
        public Builder trackAllocations(boolean enabled) {
            this.trackAllocations = enabled;
            return this;
        }

        /**
         * 构建配置
         */
        public MethodTiming build() {
            return new MethodTiming(this);
        }

        private String wildcardToRegex(String pattern) {
            return pattern
                .replace(".", "\\.")
                .replace("*", ".*")
                .replace("?", ".");
        }
    }

    private final List<Pattern> includes;
    private final List<Pattern> excludes;
    private final long threshold;
    private final boolean trackAllocs;
    private final boolean trackExceptions;
    private final int maxDepth;

    private MethodTiming(Builder builder) {
        this.includes = List.copyOf(builder.includePatterns);
        this.excludes = List.copyOf(builder.excludePatterns);
        this.threshold = builder.thresholdNanos;
        this.trackAllocs = builder.trackAllocations;
        this.trackExceptions = builder.trackExceptions;
        this.maxDepth = builder.maxCallDepth;
    }

    /**
     * 启动计时追踪
     */
    public void start() {
        nativeStart(this);
    }

    /**
     * 停止计时追踪
     */
    public void stop() {
        nativeStop();
    }

    private native void nativeStart(MethodTiming config);
    private native void nativeStop();
}
```

### JVM 实现

```cpp
// 文件: src/hotspot/share/jfr/methodTracing/jfrMethodTracing.cpp

#include "jfr/methodTracing/jfrMethodTracing.hpp"
#include "jfr/methodTracing/jfrMethodTimer.hpp"
#include "jfr/recorder/jfrEventSetting.inline.hpp"

static JfrMethodTimer* method_timer = nullptr;

void JfrMethodTracing::start(const MethodTimingConfig& config) {
    if (method_timer == nullptr) {
        method_timer = new JfrMethodTimer(config);
    }
    method_timer->enable();
}

void JfrMethodTracing::stop() {
    if (method_timer != nullptr) {
        method_timer->disable();
    }
}

/**
 * 方法进入钩子
 * 由 JIT 编译器插入调用
 */
void JfrMethodTracing::method_entry(Method* method, JavaThread* thread) {
    if (method_timer == nullptr || !method_timer->is_enabled()) {
        return;
    }

    // 检查是否匹配包含模式
    if (!method_timer->should_trace(method)) {
        return;
    }

    // 记录进入时间
    method_timer->push(method, thread);
}

/**
 * 方法退出钩子
 */
void JfrMethodTracing::method_exit(Method* method, JavaThread* thread, 
                                    bool exception) {
    if (method_timer == nullptr || !method_timer->is_enabled()) {
        return;
    }

    // 获取进入时间
    MethodTimerEntry* entry = method_timer->pop(thread);
    if (entry == nullptr) {
        return;
    }

    // 计算执行时间
    jlong start_time = entry->start_time;
    jlong end_time = JfrTicks::now();
    jlong duration = end_time - start_time;

    // 检查阈值
    if (duration < method_timer->threshold()) {
        return;
    }

    // 发送事件
    EventMethodTiming event;
    event.set_eventClass(method->method_holder()->java_mirror());
    event.set_methodName(method->name()->as_C_string());
    event.set_methodDescriptor(method->signature()->as_C_string());
    event.set_executionTime(JfrTicks::nanoseconds(duration));
    event.set_allocationSize(entry->allocated_bytes);
    event.set_exceptionThrown(exception);
    event.set_callDepth(entry->call_depth);
    event.commit();
}
```

### JIT 集成

```cpp
// 文件: src/hotspot/share/opto/compile.cpp

// 在方法入口和出口插入计时钩子
void Compile::insert_method_tracing() {
    if (!JfrMethodTracing::is_enabled()) {
        return;
    }

    // 在方法入口插入
    Node* entry = start();
    Node* thread = _gvn.transform(new ThreadLocalNode());
    Node* method = _gvn.intcon((jint)(uintptr_t)method());

    make_runtime_call(RC_NO_LEAF, 
        OptoRuntime::jfr_method_entry_Type(),
        "JfrMethodTracing::method_entry",
        nullptr,
        { thread, method });

    // 在方法出口插入 (每个返回点)
    for (uint i = 0; i < _return_offsets.length(); i++) {
        make_runtime_call(RC_NO_LEAF,
            OptoRuntime::jfr_method_exit_Type(),
            "JfrMethodTracing::method_exit",
            nullptr,
            { thread, method });
    }
}
```

---

## 使用示例

### 基本使用

```java
import jdk.jfr.*;

public class MethodTimingExample {

    public static void main(String[] args) throws Exception {
        // 创建配置
        MethodTiming timing = MethodTiming.newBuilder()
            .include("com.example.*")        // 追踪 com.example 包
            .exclude("com.example.logging.*") // 排除日志
            .threshold(1_000)                 // 阈值 1 微秒
            .trackAllocations(true)
            .build();

        // 启动 JFR 录制
        Recording recording = new Recording();
        recording.enable(EventMethodTiming.class);
        recording.start();

        // 启动方法计时
        timing.start();

        // 运行应用
        runApplication();

        // 停止
        timing.stop();
        recording.stop();

        // 分析结果
        analyzeRecording(recording);
    }

    static void analyzeRecording(Recording recording) throws Exception {
        for (RecordedEvent event : Events.fromRecording(recording)) {
            if (event.getEventType().getName().equals("jdk.MethodTiming")) {
                String method = event.getString("methodName");
                long time = event.getLong("executionTime");
                System.out.printf("%s: %d ns%n", method, time);
            }
        }
    }
}
```

### 输出示例

```
方法计时分析报告:

方法                                      执行次数    平均时间    总时间      分配
───────────────────────────────────────────────────────────────────────────────
com.example.Service.processData()         1,234      125 μs     154 ms     2.5 MB
com.example.db.Query.execute()            856        89 μs      76 ms      1.2 MB
com.example.util.JsonParser.parse()       2,345      45 μs      105 ms     0.8 MB
com.example.cache.Cache.get()             5,678      12 μs      68 ms      0.3 MB
com.example.http.Client.request()         234        234 μs     55 ms      0.5 MB

热点方法 (耗时 > 100 μs):
- com.example.Service.processData(): 42.3% of total time
- com.example.http.Client.request(): 15.1% of total time
```

---

## 性能开销

```
开销测试:

配置                    CPU 开销    内存开销
────────────────────────────────────────────────
禁用                    0%          0%
追踪所有方法            8-12%       50 MB/s
追踪 com.example.*      2-4%        10 MB/s
追踪阈值 10μs           1-2%        5 MB/s
追踪阈值 100μs          <1%         1 MB/s
────────────────────────────────────────────────

建议:
- 开发环境: 追踪所有方法
- 测试环境: 追踪特定包，阈值 1μs
- 生产环境: 追踪关键方法，阈值 100μs
```

---

## JVM 参数

```bash
# 启用方法计时 (默认关闭)
-XX:+FlightRecorder
-XX:+EnableMethodTiming

# 预配置包含模式
-XX:MethodTimingInclude=com.example.*

# 设置阈值
-XX:MethodTimingThreshold=1000  # 纳秒

# 最大调用深度
-XX:MethodTimingMaxDepth=64
```

---

## 相关 Commits

| Commit | Issue | 描述 |
|--------|-------|------|
| *(hash omitted)* | JEP 520 | 方法计时核心实现 |
| *(hash omitted)* | 8352738 | JIT 集成 |
| *(hash omitted)* | 8365972 | 事件优化 |

---

## 参考资料

- [JEP 520: JFR Method Timing](https://openjdk.org/jeps/520)
- [JFR Documentation](https://docs.oracle.com/en/java/javase/21/jfapi/)
- [JDK Mission Control](https://www.oracle.com/java/technologies/jdk-mission-control.html)

---

## 变更历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0 | 2025-01 | JEP 520 实现 |
