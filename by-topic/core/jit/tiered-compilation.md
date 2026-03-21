# 分层编译 (Tiered Compilation)

> C1 + C2 组合的最佳实践
> 平衡启动性能和稳态性能的编译策略

[← 返回 JIT 编译](../)

---
## 目录

1. [一眼看懂](#1-一眼看懂)
2. [分层编译概述](#2-分层编译概述)
3. [编译层级详解](#3-编译层级详解)
4. [Profiling 数据收集](#4-profiling-数据收集)
5. [分层编译流程](#5-分层编译流程)
6. [分层编译 vs 传统模式](#6-分层编译-vs-传统模式)
7. [分层编译的历史](#7-分层编译的历史)
8. [诊断和调优](#8-诊断和调优)
9. [实际应用场景](#9-实际应用场景)
10. [分层编译的限制](#10-分层编译的限制)
11. [相关链接](#11-相关链接)
12. [贡献者](#12-贡献者)

---


## 1. 一眼看懂

| 维度 | 内容 |
|------|------|
| **核心思想** | 解释器 → C1 → C2，逐步优化 |
| **编译层级** | Level 0 (解释器) → Level 4 (C2) |
| **Profiling** | C1 收集运行时信息供 C2 使用 |
| **启动性能** | 解释器 + C1 提供快速启动 |
| **稳态性能** | C2 提供峰值性能 |
| **默认启用** | JDK 8+ 默认开启 |

---

## 2. 分层编译概述

### 为什么需要分层编译？

```
传统方案的问题:

只使用解释器:
  └─ 启动快，但性能极差 (50-100x slower than C2)

只使用 C1:
  └─ 编译快，但性能一般 (2-5x slower than C2)

只使用 C2:
  └─ 性能最好，但编译慢，启动延迟高

分层编译:
  ├─ 解释器: 快速启动
  ├─ C1: 快速提供优化代码，收集 profiling
  └─ C2: 基于 profiling 深度优化
```

### 性能对比

| 场景 | 解释器 | C1 | C2 | 分层编译 |
|------|--------|----|----|----------|
| **启动时间** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **预热时间** | - | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **稳态性能** | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **内存占用** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

---

## 3. 编译层级详解

### 5 个编译层级

```
Level 0: 解释执行 (Interpreter)
   │
   │  - 字节码逐条解释执行
   │  - 零编译延迟
   │  - 收集基础 profiling
   │
   ▼
Level 1: C1 (简单优化)
   │
   │  - 快速编译 (< 50ms)
   │  - 基础优化 (内联、常量折叠)
   │  - 开始 profiling
   │
   ▼
Level 2: C1 (有限 profiling)
   │
   │  - 中等优化
   │  - 收集更多 profiling 信息
   │
   ▼
Level 3: C1 (完全 profiling)
   │
   │  - 激进 profiling 收集
   │  - 为 C2 准备完整信息
   │
   ▼
Level 4: C2 (深度优化)
   │
   │  - 基于 profiling 的深度优化
   │  - 循环优化、逃逸分析、向量化
   │
   ▼
峰值性能
```

### 各层级详细参数

| Level | 编译器 | 特点 | 编译阈值 | 用途 |
|-------|--------|------|----------|------|
| **0** | 解释器 | 纯解释执行 | - | 应用启动、冷代码 |
| **1** | C1 | 简单优化，无 profiling | 1,500 次调用 | 快速提供优化代码 |
| **2** | C1 | 有限 profiling | 数千次调用 | 收集运行时信息 |
| **3** | C1 | 完全 profiling | 数千次调用 | 为 C2 准备数据 |
| **4** | C2 | 深度优化 | 10,000 次调用 | 峰值性能 |

---

## 4. Profiling 数据收集

### C1 收集的信息

| 数据类型 | 用途 | 示例 |
|----------|------|------|
| **方法调用频率** | 识别热点方法 | 方法 A 被调用 100,000 次 |
| **类型反馈** | 虚方法内联 | ArrayList.iterator() 总是返回 ArrayList$Itr |
| **分支概率** | 优化分支预测 | 90% 的情况走 if 分支 |
| **循环计数** | 循环展开决策 | 循环执行 10,000 次 |
| **逃逸信息** | 逃逸分析 | 对象不逃出方法 |

### Profiling 传递

```
C1 收集的 profiling 信息 → C2 使用

示例:
C1 发现:
  - method() 总是被同一个类调用
  - 循环执行 > 10,000 次
  - 分支总是走 true 路径

C2 基于 C1 的信息:
  - 激进内联 method()
  - 完全展开循环
  - 删除死分支 (false 路径)
```

---

## 5. 分层编译流程

### 方法升级路径

```
方法首次调用
   │
   ▼
Level 0: 解释执行
   │  收集调用次数
   │
   ▼ (达到阈值)
Level 1: C1 编译
   │  快速优化
   │  开始 profiling
   │
   ▼ (继续热点)
Level 2: C1 重编译
   │  更多 profiling
   │
   ▼ (持续热点)
Level 3: C1 重编译
   │  完整 profiling
   │  准备 C2 编译
   │
   ▼ (达到 C2 阈值)
Level 4: C2 编译
   │  深度优化
   │  峰值性能
   ▼
稳态运行
```

### 阈值参数

```bash
# 编译阈值 (方法调用次数)
-XX:CompileThreshold=10000              # C2 默认阈值
-XX:CompileThreshold=1500               # C1 默认阈值 (非分层)

# 分层编译特定阈值
-XX:Tier0InvokeNotifyFreqLog=7          # Level 0 → 1: 2^7 = 128 次
-XX:Tier0BackedgeNotifyFreqLog=10       # Level 0 循环回边: 2^10 = 1024 次
-XX:Tier3InvokeNotifyFreqLog=10         # Level 3 → 4: 2^10 = 1024 次
-XX:Tier3BackedgeNotifyFreqLog=13       # Level 3 循环回边: 2^13 = 8192 次

# 调整阈值示例
-XX:CompileThreshold=5000               # 更早触发 C2
-XX:CompileThreshold=20000              # 更晚触发 C2
```

---

## 6. 分层编译 vs 传统模式

### 传统模式

```
-server 模式 (仅 C2):
解释器 ──► 等待 10,000 次调用 ──► C2 编译 ──► 高性能
   │                                    ↑
   └──────── 启动慢，预热慢 ──────────────┘

-client 模式 (仅 C1):
解释器 ──► 等待 1,500 次调用 ──► C1 编译 ──► 中等性能
   │                                    ↑
   └──────── 启动快，但性能上限低 ────────┘
```

### 分层模式

```
分层编译:
解释器 ──► C1 (1500 次) ──► C2 (10000 次) ──► 高性能
   │          │                  │
   │          └─ 快速提供优化代码 ─┘
   │
   └─ 启动快，逐步达到峰值性能
```

### 性能对比

| 应用类型 | -client | -server | 分层编译 |
|----------|---------|---------|----------|
| **短时运行** | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **长时间运行** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **微服务** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **批处理** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **桌面应用** | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |

---

## 7. 分层编译的历史

### JDK 版本演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 1.3** | -client/-server | 手动选择编译器 |
| **JDK 6** | 分层编译引入 | 实验性功能 (-XX:+TieredCompilation) |
| **JDK 7** | 分层编译改进 | Server JVM 默认开启 |
| **JDK 8** | 分层编译成熟 | 所有平台默认开启 |

### 启用方式

```bash
# JDK 6-7: 需要显式启用
java -XX:+TieredCompilation MyApp

# JDK 8+: 默认启用
java MyApp

# 禁用分层编译 (仅 C2)
java -XX:-TieredCompilation MyApp

# 仅使用 C1
java -XX:+TieredCompilation -XX:TieredStopAtLevel=1 MyApp
```

---

## 8. 诊断和调优

### 查看编译层级

```bash
# 查看编译日志
java -XX:+PrintCompilation MyApp

# 输出示例
     71   10       3       java.util.String::charAt (26 bytes)
     72   11       4       java.util.String::hashCode (16 bytes)
              ^   ^        ^
              │   │        └─ 编译层级 (4 = C2)
              │   └─ 编译 ID
              └─ 方法序号

# 查看分层编译详情
java -XX:+PrintCompilation -XX:+UnlockDiagnosticVMOptions \
     -XX:+PrintTieredEvents MyApp
```

### 分层编译事件

```
tiered events 输出示例:

# 方法从 Level 0 升级到 Level 1
tiered-upgrade level=1 method=MyClass.myMethod

# 方法从 Level 1 升级到 Level 2
tiered-upgrade level=2 method=MyClass.myMethod

# 方法从 Level 3 升级到 Level 4 (C2)
tiered-upgrade level=4 method=MyClass.myMethod
```

### 调优参数

```bash
# 控制分层编译行为
-XX:+TieredCompilation                 # 启用分层编译
-XX:-TieredCompilation                 # 禁用分层编译
-XX:TieredStopAtLevel=1                # 只使用 C1
-XX:TieredStopAtLevel=3                # 不使用 C2

# 调整编译阈值
-XX:CompileThreshold=10000             # C2 阈值
-XX:FreqInlineSize=325                 # 热方法内联阈值

# Profiling 控制
-XX:ProfileInterpreter=1               # 解释器 profiling
-XX:TieredCompileTaskTimeout=50        # 编译任务超时 (秒)
```

---

## 9. 实际应用场景

### 场景 1: 微服务

```
特点:
- 频繁启动/停止
- 需要快速响应请求

分层编译优势:
- Level 0-1: 快速启动，处理早期请求
- Level 4: 稳定后提供峰值性能
```

### 场景 2: 批处理

```
特点:
- 长时间运行
- 追求吞吐量

分层编译优势:
- 快速度过启动阶段
- C2 提供最优吞吐量
```

### 场景 3: 桌面应用

```
特点:
- 交互式操作
- 响应时间敏感

分层编译优势:
- C1 提供快速响应
- 避免长时间 GC 暂停
```

---

## 10. 分层编译的限制

### 已知限制

| 限制 | 说明 | 影响 |
|------|------|------|
| **代码缓存** | 需要存储多个版本 | 增加 Code Cache 压力 |
| **编译时间** | 多次编译 | 增加总编译时间 |
| **Profiling 开销** | 收集信息有成本 | 略微降低早期性能 |
| **去优化** | profiling 变化需回退 | 可能导致性能波动 |

### 去优化 (Deoptimization)

```
当 C2 基于错误的 profiling 优化时:

1. 检测到假设失效
2. 去优化 (Deopt)
3. 回退到解释器或 C1
4. 重新收集 profiling
5. 重新编译

示例:
C2 假设: 方法总是接收 ArrayList
运行时: 收到了 LinkedList
结果: 去优化，重新编译
```

---

## 11. 相关链接

### 本地文档

- [C1 编译器详解](c1-compiler.md) - Level 1-3 的编译器
- [C2 优化阶段](c2-phases.md) - Level 4 的编译器
- [内联优化](inlining.md) - 各层级的内联策略
- [VM 参数](vm-parameters.md) - 分层编译参数

### 外部资源

- [JEP 193](/jeps/language/jep-193.md) - 涉及分层编译
- [Tiered Compilation in HotSpot JVM](https://blog.joda.org/2010/06/tiered-compilation-in-hotspot-jvm.html)
- [Understanding JIT Compilation](https://www.oracle.com/java/technologies/javase/whitepapers.html)

---

## 12. 贡献者

| 贡献者 | 领域 | 组织 |
|--------|------|------|
| [John Rose](/by-contributor/profiles/john-rose.md) | JIT 编译器 | Oracle |
| [Vladimir Kozlov](/by-contributor/profiles/vladimir-kozlov.md) | C2 编译器 | Oracle |
| [Tom Rodriguez](/by-contributor/profiles/tom-rodriguez.md) | JIT 编译器 | Oracle |

---

**最后更新**: 2026-03-20
