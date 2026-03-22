# JFR (监控诊断) JEPs

> JDK Flight Recorder 相关 JEP 汇总

---
## 目录

1. [概览](#1-概览)
2. [JFR CPU-Time Profiling (JEP 509)](#2-jfr-cpu-time-profiling-jep-509)
3. [JFR Cooperative Sampling (JEP 518)](#3-jfr-cooperative-sampling-jep-518)
4. [JFR Method Timing & Tracing (JEP 520)](#4-jfr-method-timing--tracing-jep-520)
5. [相关链接](#5-相关链接)

---


## 1. 概览

| JEP | 标题 | JDK | 状态 | 说明 |
|-----|------|-----|------|------|
| [JEP 509](jep-509.md) | JFR CPU-Time Profiling | 25 | 🔧 实验 | CPU 时间分析 |
| [JEP 518](jep-518.md) | JFR Cooperative Sampling | 25 | ✅ 正式 | 协作采样 |
| [JEP 520](jep-520.md) | JFR Method Timing & Tracing | 25 | ✅ 正式 | 方法计时 |

---

## 2. JFR CPU-Time Profiling (JEP 509)

### 核心特性

- **低开销 CPU 分析**：基于 async-profiler 技术
- **火焰图支持**：生成火焰图数据
- **协作采样**：减少采样偏差

```bash
# 启用 CPU 时间分析
jcmd <pid> JFR.start \
  settings=profile \
  jfc+cpu-time-profiling=true
```

**详见**：[JEP 509](jep-509.md)

---

## 3. JFR Cooperative Sampling (JEP 518)

### 核心改进

- **协作式采样**：减少采样偏差
- **更准确的数据**：避免安全点偏差
- **更低开销**：减少性能影响

**详见**：[JEP 518](jep-518.md)

---

## 4. JFR Method Timing & Tracing (JEP 520)

### 核心功能

- **方法计时**：精确测量方法执行时间
- **追踪支持**：支持分布式追踪集成
- **低开销**：适合生产环境

**详见**：[JEP 520](jep-520.md)

---

## 5. 相关链接

- JFR 指南 
- [JDK Mission Control](https://www.oracle.com/java/technologies/jdk-mission-control.html)
