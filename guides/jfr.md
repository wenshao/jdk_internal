# JFR (Java Flight Recorder) 指南

> Java Flight Recorder 是 JDK 内置的低开销性能分析工具

---
## 目录

1. [概述](#1-概述)
2. [快速开始](#2-快速开始)
3. [常用配置](#3-常用配置)
4. [关键事件类型](#4-关键事件类型)
5. [JDK 25+ 新特性](#5-jdk-25-新特性)
6. [相关资源](#6-相关资源)

---


## 1. 概述

JFR 是 Java 平台的诊断和性能分析工具，具有以下特点：

- **低开销**: 生产环境可用，开销通常 < 1%
- **内置集成**: JDK 内置，无需额外安装
- **丰富事件**: 数百种内置事件类型
- **持续监控**: 支持持续录制和事件流

---

## 2. 快速开始

### 启动 JFR 录制

```bash
# 方式 1: JVM 启动参数
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr MyApp

# 方式 2: jcmd 动态启动
jcmd <pid> JFR.start name=profiling duration=60s filename=recording.jfr
```

### 分析录制文件

```bash
# 使用 jfr 工具
jfr print recording.jfr

# 使用 JDK Mission Control (JMC)
jmc recording.jfr
```

---

## 3. 常用配置

### 预设配置

| 配置 | 描述 | 开销 |
|------|------|------|
| `default` | 默认配置，低开销 | < 1% |
| `profile` | 性能分析配置 | 1-2% |
| `continuous` | 持续监控配置 | < 1% |

### 自定义事件

```java
@Label("Custom Event")
@Description("自定义业务事件")
public class CustomEvent extends Event {
    @Label("User ID")
    public String userId;

    @Label("Operation")
    public String operation;
}

// 使用
CustomEvent event = new CustomEvent();
event.userId = "user123";
event.operation = "login";
event.commit();
```

---

## 4. 关键事件类型

### 内存事件

- `jdk.GCPhasePause` - GC 暂停
- `jdk.GCHeapSummary` - 堆内存摘要
- `jdk.JavaMonitorWait` - 监视器等待

### CPU 事件

- `jdk.ExecutionSample` - 执行采样
- `jdk.CPUTime` - CPU 时间 (JDK 25+)
- `jdk.ThreadAllocationStatistics` - 线程分配统计

### IO 事件

- `jdk.FileRead` - 文件读取
- `jdk.FileWrite` - 文件写入
- `jdk.SocketRead` - Socket 读取
- `jdk.SocketWrite` - Socket 写入

---

## 5. JDK 25+ 新特性

### JEP 509: CPU-Time Profiling

JDK 25 引入了 CPU 时间分析功能：

```bash
# 启用 CPU 时间分析
jcmd <pid> JFR.start settings=cpu-profiling
```

---

## 6. 相关资源

- [JDK Mission Control](https://www.oracle.com/java/technologies/jdk-mission-control.html)
- [JFR 配置参考](https://docs.oracle.com/en/java/javase/21/jfapi/)
- [性能分析最佳实践](/guides/performance.md)