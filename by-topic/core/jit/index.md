# JIT 编译

> C1、C2、分层编译、Graal 演进历程

[← 返回核心平台](../)

---

## 快速概览

```
JDK 1.0 ── JDK 5 ── JDK 6 ── JDK 9 ── JDK 17 ── JDK 21 ── JDK 26
   │         │        │        │        │        │        │
解释器    C1/C2   分层    Graal   JIT    虚拟线程  SuperWord
纯解释   分离    编译     JIT     优化     支持    成本模型
                  Tiered           性能
```

### 核心演进

| 版本 | 特性 | 说明 |
|------|------|------|
| **JDK 1.0** | 解释器 | 纯解释执行 |
| **JDK 1.3** | C2 (Server Compiler) | 高性能编译器 |
| **JDK 1.4** | C1 (Client Compiler) | 快速启动编译器 |
| **JDK 5** | C1/C2 分离 | -client/-server |
| **JDK 6** | 分层编译 | C1 + C2 组合 |
| **JDK 9** | Graal JIT | 实验性高性能 JIT |
| **JDK 17** | JIT 优化 | 编译器改进 |
| **JDK 21** | Record 支持 | 编译器优化 |
| **JDK 23** | JIT 性能 | 编译吞吐量提升 |
| **JDK 26** | SuperWord 成本模型 | 智能向量化 |

---

## 编译器对比

| 编译器 | 全称 | 特点 | 适用场景 |
|--------|------|------|----------|
| **解释器** | Interpreter | 启动快，执行慢 | 应用启动、冷代码 |
| **C1** | Client Compiler | 编译快，优化少 | 桌面应用、短时运行 |
| **C2** | Server Compiler | 编译慢，深度优化 | 长期运行的服务器应用 |
| **Graal** | Graal JIT | 基于 Java，可扩展 | 实验性，特定场景 |

### 分层编译 (Tiered Compilation)

```
Level 0: 解释执行 (Interpreter)
Level 1: C1 (纯解释 profiling)
Level 2: C1 (有限 profiling)
Level 3: C1 (完全 profiling)
Level 4: C2 (深度优化)
```

**编译策略:**
- 方法从 Level 0 开始
- 达到阈值后升级到下一层
- C1 收集 profiling 信息供 C2 使用
- C2 可以基于 profiling 做更激进的优化

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### JIT 编译器 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Coleen Phillimore | 72 | Oracle | C1/C2 编译器 |
| 2 | Aleksey Shipilev | 68 | Oracle | JIT 编译器 |
| 3 | Ioi Lam | 62 | Oracle | 编译器, 运行时 |
| 4 | Stefan Karlsson | 31 | Oracle | 编译器, GC |
| 5 | Doug Simon | 29 | Oracle | JIT 编译器 |
| 6 | David Holmes | 24 | Oracle | 并发, 编译器 |
| 7 | Claes Redestad | 24 | Oracle | 编译器优化 |
| 8 | Thomas Stuefe | 22 | Oracle | 编译器 |
| 9 | Vladimir Kozlov | 20 | Oracle | JIT 编译器 |
| 10 | Igor Veresov | 17 | Oracle | JIT 编译器 |

### C2 专项贡献者

| 排名 | 贡献者 | 主要贡献 |
|------|--------|----------|
| 1 | [Vladimir Kozlov](https://github.com/vklang) | C2 架构师 |
| 2 | [Roland Westrelin](https://github.com/rwestrel) | C2 优化 (JDK-8325495 Add 优化) |
| 3 | [John Rose](https://github.com/jrose) | invokedynamic, JIT |
| 4 | [Emanuel Peter](https://eme64.github.io/blog/) | C2 博客作者, 编译器工程师 |
| 5 | [Christian Hagedorn](https://github.com/chhagedorn) | C2 优化, GVN |

---

## 文档导航

### 核心概念

- [C2 优化阶段](c2-phases.md) - 15 个编译阶段详解
  - PhaseIterGVN、PhaseIdealLoop、PhaseCCP
  - 逃逸分析、标量替换、向量化

### 配置参考

- [VM 参数](vm-parameters.md) - 完整参数参考
  - 编译器选择、阈值、代码缓存
  - 内联控制、C2 特定参数

### 调试诊断

- [诊断工具](diagnostics.md) - 调试和性能分析
  - 编译日志、JFR、jhsdb
  - Ideal Graph 可视化

### 历史演进

- [版本时间线](timeline.md) - JDK 1.0 到 JDK 26
- [近期改进](recent-changes.md) - 2024-2025 更新

---

## 快速参考

### 常用 VM 参数

```bash
# 启用分层编译 (默认)
-XX:+TieredCompilation

# 调整编译阈值
-XX:CompileThreshold=10000         # C2 阈值
-XX:FreqInlineSize=325             # 热方法内联阈值

# 代码缓存
-XX:ReservedCodeCacheSize=256m

# 诊断
-XX:+PrintCompilation             # 打印编译活动
-XX:+PrintInlining                 # 打印内联决策
-XX:+CITime                       # 编译时间统计
```

### 诊断命令

```bash
# 查看编译活动
jcmd <pid> Compiler.compile

# JFR 记录
jcmd <pid> JFR.start name=jit
jcmd <pid> JFR.dump name=jit filename=jit.jfr

# jhsdb 诊断
jhsdb clhsdb --pid <pid>
> printcodecache
```

---

## 内部结构

### HotSpot 编译器源码

```
src/hotspot/share/
├── compiler/
│   ├── compileBroker.cpp          # 编译任务调度
│   ├── compilation.cpp            # 编译策略
│   └── compilerOracle.cpp         # 编译规则
├── c1/                            # C1 (Client Compiler)
│   ├── c1_Compilation.cpp         # C1 编译入口
│   ├── c1_GraphBuilder.cpp        # IR 构建
│   └── c1_LinearScan.cpp          # 寄存器分配
├── opto/                          # C2 (Server Compiler)
│   ├── compile.cpp                # C2 编译入口, Optimize()
│   ├── gvn.cpp                    # Global Value Numbering
│   ├── loopopts.cpp               # 循环优化
│   ├── escape.cpp                 # 逃逸分析
│   ├── superword.cpp              # 向量化
│   ├── matcher.cpp                # 指令匹配
│   ├── chaitin.cpp                # 寄存器分配
│   └── output.cpp                 # 代码生成
└── jvmci/                         # JVMCI (Graal 接口)
```

---

## C2 编译流程概览

```
字节码
   │
   ▼
Parse Phase ────────► 解析字节码 → Ideal Graph
   │                      内联优化
   ▼                      初始 GVN
PhaseIterGVN ◄────────── 全局值编号
   │                      常量折叠
   ▼                      公共子表达式消除
PhaseIdealLoop ────────► 循环优化 (多轮迭代)
   │                      Peeling/Unswitching/Unrolling
   ▼
PhaseCCP ───────────────► 条件常量传播
   │                      死代码消除
   ▼
PhaseEscapeAnalysis ───► 逃逸分析
   │                      标量替换
   ▼                      栈上分配
PhaseMacroExpand ──────► 宏扩展
   │                      锁优化
   ▼
PhaseSuperWord ────────► SIMD 向量化
   │
   ▼
代码生成 ───────────────► 寄存器分配 → 机器码
```

---

## 相关链接

### 本地文档

- [C2 优化阶段](c2-phases.md) - 15 个编译阶段详解
- [VM 参数](vm-parameters.md) - 完整参数参考
- [诊断工具](diagnostics.md) - 调试和性能分析
- [近期改进](recent-changes.md) - 2024-2025 更新
- [版本时间线](timeline.md) - JDK 1.0 到 JDK 26

### 相关主题

- [性能优化](../performance/) - 编译器优化
- [GC 演进](../gc/) - GC 与 JIT 协作
- [JVM 调优](../jvm/) - VM 参数

### 外部参考

**官方文档:**
- [Tuning Java HotSpot VM](https://docs.oracle.com/javase/8/docs/technotes/guides/vm/performance.html)
- [HotSpot Internals Wiki](https://wiki.openjdk.org/display/HotSpot)

**技术博客:**
- [Emanuel's HotSpot C2 Blog](https://eme64.github.io/blog/) - C2 编译器深入解析
  - [Part 2: GVN](https://eme64.github.io/blog/2024/12/24/Intro-to-C2-Part02.html)
  - [Part 3: 优化阶段](https://eme64.github.io/blog/2025/01/23/Intro-to-C2-Part03.html)
  - [Part 4: 循环优化](https://eme64.github.io/blog/2025/01/23/Intro-to-C2-Part04.html)

**Bug 跟踪:**
- [JDK-8325497: C2 性能调查](https://bugs.openjdk.org/browse/JDK-8325497)
- [JDK-8340093: SuperWord 成本模型](https://bugs.openjdk.org/browse/JDK-8340093)
