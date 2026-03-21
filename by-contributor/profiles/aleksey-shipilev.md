# Aleksey Shipilev

> 性能优化专家，JMH 主要贡献者，JEP 503 主导者

---

## 目录

1. [基本信息](#1-基本信息)
2. [技术影响力](#2-技术影响力)
3. [贡献时间线](#3-贡献时间线)
4. [技术特长](#4-技术特长)
5. [代表性工作](#5-代表性工作)
6. [外部资源](#6-外部资源)
7. [PR 列表](#7-pr-列表)
8. [关键贡献详解](#8-关键贡献详解)
9. [开发风格](#9-开发风格)
10. [历史贡献 (JDK 8+)](#10-历史贡献-jdk-8)
11. [相关链接](#11-相关链接)

---

## 1. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Aleksey Shipilëv |
| **当前组织** | Amazon Web Services (Principal Engineer) |
| **位置** | 波茨坦, 德国 |
| **GitHub** | [@shipilev](https://github.com/shipilev) |
| **Twitter** | [@shipilev](https://twitter.com/shipilev) |
| **Blog** | [shipilev.net](https://shipilev.net/) |
| **OpenJDK** | [@shade](https://openjdk.org/census#shade) |
| **角色** | OpenJDK Member, JDK Reviewer (JDK 9+) |
| **PRs** | [803+ integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Ashipilev+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | C2 编译器、Shenandoah GC、性能优化、JMH、基准测试 |
| **活跃时间** | 2012 - 至今 |
| **教育背景** | ITMO University (MSc Computer Science, 2003-2009, With Honors) |

### 组织历史

| 时间段 | 组织 | 角色 | 邮箱 |
|--------|------|------|------|
| 2023 - 至今 | Amazon Web Services | Principal Engineer | shade@amazon.de |
| 2016 - 2023 | Red Hat | Principal Software Engineer | shade@redhat.com |
| 2012 - 2016 | Oracle | Java Performance Engineer | aleksey.shipilev@oracle.com |
| ~2009 - 2012 | Intel | Software Engineer | - |

> **数据来源**: [CV](https://shipilev.net/Aleksey_Shipilev_CV.pdf), [LinkedIn](https://de.linkedin.com/in/alekseyshipilev), [OpenJDK Census](https://openjdk.org/census#shade), [JDK 9 Reviewer CFV](https://mail.openjdk.org/pipermail/jdk9-dev/2016-April/004138.html)

### 最近 10 个 Integrated PRs (2026 年 2-3 月)

| PR # | Issue | 标题 | 日期 |
|------|-------|------|------|
| #29843 | 8378338 | Shenandoah: Heap-used generic verification error after update-refs | Mar 11, 2026 |
| #29754 | 8378080 | Zero: JNIEnv argument is corrupted in native calls | Feb 20, 2026 |
| #29743 | 8377990 | Zero: Replace Java math ops with UB-safe implementations | Feb 20, 2026 |
| #29528 | 8376761 | ARM32: Constant base assert after JDK-8373266 | Feb 4, 2026 |
| #29527 | 8376970 | Shenandoah: Verifier should do basic verification before touching oops | Feb 3, 2026 |
| #29526 | 8376969 | Shenandoah: GC state getters should be inlineable | Feb 3, 2026 |
| #29468 | 8376604 | C2: EA should assert is_oop_field for AddP with oop outs | Jan 30, 2026 |
| #29462 | 8376570 | GrowableArray::remove_{till,range} should work on empty list | Feb 2, 2026 |
| #29444 | 8376472 | Shenandoah: Assembler store barriers read destination memory despite the decorators | Feb 2, 2026 |
| #29254 | 8375359 | Improve GC serviceability init staging | Feb 23, 2026 |

> **观察**: 最近工作集中在 **Shenandoah GC 验证**、**Zero 端口维护** 和 **C2 编译器优化**

---

## 2. 技术影响力

| 指标 | 值 |
|------|-----|
| **代码行数** | +90,897 / -82,925 (净 +7,972) |
| **影响模块** | hotspot (GC, 编译器) |
| **主要贡献** | Shenandoah GC, C2 优化, JMH |

### 影响的主要目录

| 目录 | 文件数 | 说明 |
|------|--------|------|
| gc/shenandoah | 933 | Shenandoah GC |
| cpu/x86 | 291 | x86 后端 |
| opto | 196 | C2 编译器 |
| runtime | 194 | 运行时 |
| compiler | 120 | 编译器接口 |

---

## 3. 贡献时间线

```
2012: ░░░░░░░░░░░░░░░░░░░░   4 commits
2013: ░░░░░░░░░░░░░░░░░░░░  20 commits
2014: ░░░░░░░░░░░░░░░░░░░░  17 commits
2015: ░░░░░░░░░░░░░░░░░░░░  22 commits
2016: ████░░░░░░░░░░░░░░░░  53 commits
2017: ░░░░░░░░░░░░░░░░░░░░   5 commits
2018: █████░░░░░░░░░░░░░░░  66 commits
2019: ███████████░░░░░░░░░ 150 commits
2020: ████████████████████ 285 commits (峰值)
2021: ████████████████░░░░ 204 commits
2022: ████████████░░░░░░░░ 160 commits
2023: █████████░░░░░░░░░░░ 124 commits
2024: ████████████░░░░░░░░ 163 commits
2025: █████████████████░░░ 227 commits
2026: ███░░░░░░░░░░░░░░░░░  38 commits (进行中)
```

---

## 4. 技术特长

`Shenandoah GC` `C2 编译器` `性能优化` `JMH` `x86 后端` `基准测试`

---

## 5. 代表性工作

### 主导 JEP

| JEP | 标题 | 状态 | 说明 |
|-----|------|------|------|
| [JEP 503](https://openjdk.org/jeps/503) | Remove the 32-bit x86 Port | JDK 23 | 移除 32 位 x86 支持 |
| [JEP 501](https://openjdk.org/jeps/501) | Deprecate the 32-bit x86 Port for Removal | JDK 22 | 弃用 32 位 x86 |
| [JEP 379](https://openjdk.org/jeps/379) | Shenandoah: Low-Pause-Time Garbage Collector (Production) | JDK 15 | Shenandoah GC 正式版 |
| [JEP 318](https://openjdk.org/jeps/318) | Epsilon: A No-Op Garbage Collector (Experimental) | JDK 11 | 无操作 GC，性能测试专用 |
| [JEP 280](https://openjdk.org/jeps/280) | Indify String Concatenation | JDK 9 | 字符串拼接优化 |

### 1. JMH (Java Microbenchmark Harness)
**主要贡献者/创建者**

Java 微基准测试框架的创始人和主要维护者，为 Java 性能测试提供标准工具。

- **项目地址**: [openjdk/jmh](https://github.com/openjdk/jmh)
- **集成**: JDK 9+ 集成到 OpenJDK
- **功能**: 方法级性能测试，提供 OPS、TP99 等指标

### 2. Shenandoah GC 核心贡献者
主导 Shenandoah GC 的开发和优化，使其成为低延迟 GC 的首选。

- **超低暂停时间**: 亚毫秒级 GC 暂停
- **并发处理**: 与 Java 线程并发执行 GC
- **生产可用**: JDK 15+ 正式版本

### 3. 其他工具开发

| 工具 | 全称 | 用途 | 链接 |
|------|------|------|------|
| **JOL** | Java Object Layout | 对象内存布局分析 | [openjdk.org/jol](https://openjdk.org/projects/code-tools/jol/) |
| **JCStress** | Java Concurrency Stress | 并发压力测试 | [openjdk.org/jcstress](https://openjdk.org/projects/code-tools/jcstress/) |

#### JOL (Java Object Layout)

分析 Java 对象在 JVM 中的内存布局的工具。

- **功能**: 分析对象内存布局、内存占用、类结构
- **技术**: 使用 Unsafe、JVMTI、Serviceability Agent
- **用途**: JVM 内部分析、对象内存优化
- **代码示例**: JOLSample_01_Basic.java, JOLSample_19_Promotion.java

#### JCStress (Java Concurrency Stress)

实验性的并发正确性测试框架。

- **功能**: 测试低级 JVM 并发问题、硬件级并发
- **目标**: 破坏 Java 实现的并发行为以发现问题
- **资源**: [YouTube 播放列表](https://www.youtube.com/playlist?list=PLC5OGTO4dWxYC9Eh9RJYRSP85GKROho3S)
- **工作坊**: [HydraConf 2021 JCStress Workshop](https://shipilev.net/talks/hydraconf-June2021-jcstress-workshop.pdf)

### 4. C2 编译器优化
多项 C2 编译器优化，包括逃逸分析、内联优化等。

### 5. 性能分析和调优
大量性能问题分析和修复，涵盖 GC、编译器、运行时等多个领域。

---

## 6. 外部资源

| 类型 | 链接 |
|------|------|
| **个人主页** | [shipilev.net](https://shipilev.net/) |
| **CV** | [Aleksey_Shipilev_CV.pdf](https://shipilev.net/Aleksey_Shipilev_CV.pdf) |
| **Twitter** | [@shipilev](https://twitter.com/shipilev) |
| **GitHub** | [@shipilev](https://github.com/shipilev) |
| **OpenJDK Census** | [shade](https://openjdk.org/census#shade) |
| **演讲集合** | [shipilev.net/talks](https://shipilev.net/talks/) |
| **构建服务** | [builds.shipilev.net](https://builds.shipilev.net/) |

### JVM Anatomy Quarks

个人博客上的 JVM 知识系列文章：
- [JVM Anatomy Quarks](https://shipilev.net/jvm/anatomy-quarks/)
- 描述 JVM 的基础知识点
- 持续更新的迷你文章系列

### 演讲和会议

Aleksey 经常在各大 Java 会议发表演讲：

#### Devoxx

| 年份 | 主题 | 链接 |
|------|------|------|
| 2012 | Performance Methodology | [PDF](https://shipilev.net/talks/devoxx-Nov2012-perfMethodology.pdf) |
| 2013 | JMH: The Lesser of Two Evils | [PDF](https://shipilev.net/talks/devoxx-Nov2013-benchmarking.pdf) |
| 2017 | Shenandoah: The GC That Could | [PDF](https://shipilev.net/talks/devoxx-Nov2017-shenandoah.pdf) [Video](https://www.youtube.com/watch?v=VCeHkcwfF9Q) |

#### JavaZone

| 年份 | 主题 | 链接 |
|------|------|------|
| 2018 | Shenandoah GC - Part I | [PDF](https://shipilev.net/talks/javazone-Sep2018-shenandoah.pdf) |
| - | JVM Benchmarking | [Video](https://www.youtube.com/watch?v=x3Vlze1mUj4) |

#### GeeCON

| 年份 | 主题 | 链接 |
|------|------|------|
| 2018 | Java Memory Model Unlearning Experience | [PDF](https://shipilev.net/talks/geecon-May2018-jmm.pdf) [Video](https://www.youtube.com/watch?v=TK-7GCCDF_I) |
| - | JCStress Workshop | [Video Playlist](https://www.youtube.com/playlist?list=PLC5OGTO4dWxYC9Eh9RJYRSP85GKROho3S) |

#### 其他会议

- **Joker Conference**: Performance, Java Memory Model
- **Øredev**: The Art of Java Benchmarking (2013)
- **Jfokus**: Speaker (2018)
- **Froscon**: Java Memory Model for Beginners
- **HydraConf**: JCStress Workshop (2021)
| HydraConf | JCStress Workshop |

### 开源工具

| 项目 | 链接 | 说明 |
|------|------|------|
| **builds.shipilev.net** | [builds.shipilev.net](https://builds.shipilev.net/) | OpenJDK 每日构建 |
| **backports-monitor** | [GitHub](https://github.com/shipilev/jdk-backports-monitor) | JDK 回迁监控 |

**builds.shipilev.net** 提供：
- OpenJDK 8u, 11u, 17u 每日构建
- Fastdebug/Slowdebug 调试版本
- JDK 回迁监控报告
- 多架构构建支持

---

### 按类别统计

| 类别 | 数量 | 占比 |
|------|------|------|
| C2 编译器优化 | 50 | 42% |
| 性能基准测试 | 30 | 25% |
| JEP 实现 | 5 | 4% |
| Bug 修复 | 35 | 29% |

### 关键成就

- **JEP 503**: 移除 32位 x86 支持
- **C2 优化**: 多项编译器优化
- **JMH**: Java 微基准测试框架主要贡献者

---

## 7. PR 列表

### JEP 503: Remove the 32-bit x86 Port

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8345169 | Implement JEP 503: Remove the 32-bit x86 Port | [JBS-8345169](https://bugs.openjdk.org/browse/JDK-8345169) |

### C2 编译器优化

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8371581 | C2: PhaseCCP should reach fixpoint by revisiting deeply-Value-d nodes | [JBS-8371581](https://bugs.openjdk.org/browse/JDK-8371581) |
| 8371804 | C2: Tighten up LoadNode::Value comments after JDK-8346184 | [JBS-8371804](https://bugs.openjdk.org/browse/JDK-8371804) |
| 8372154 | AArch64: Match rule failure with some CompareAndSwap operand shapes | [JBS-8372154](https://bugs.openjdk.org/browse/JDK-8372154) |
| 8370318 | AES-GCM vector intrinsic may read out of bounds (x86_64, AVX-512) | [JBS-8370318](https://bugs.openjdk.org/browse/JDK-8370318) |
| 8348278 | Trim InitialRAMPercentage to improve startup in default modes | [JBS-8348278](https://bugs.openjdk.org/browse/JDK-8348278) |

### 性能基准测试

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8371709 | Add CTW to hotspot_compiler testing | [JBS-8371709](https://bugs.openjdk.org/browse/JDK-8371709) |
| 8372319 | com/sun/crypto/provider/Cipher/HPKE/KAT9180 test has external dependencies | [JBS-8372319](https://bugs.openjdk.org/browse/JDK-8372319) |
| 8369226 | GHA: Switch to MacOS 15 | [JBS-8369226](https://bugs.openjdk.org/browse/JDK-8369226) |
| 8369283 | Improve trace logs in safepoint machinery | [JBS-8369283](https://bugs.openjdk.org/browse/JDK-8369283) |

### GC 优化

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8370572 | Cgroups hierarchical memory limit is not honored after JDK-8322420 | [JBS-8370572](https://bugs.openjdk.org/browse/JDK-8370572) |

---

## 8. 关键贡献详解

### 1. JEP 503: Remove the 32-bit x86 Port

**背景**: 32位 x86 平台使用率持续下降，维护成本高。

**解决方案**: 移除 32位 x86 端口支持。

```cpp
// 移除的文件
src/hotspot/cpu/x86/vm_version_x86_32.cpp
src/hotspot/cpu/x86/interpreterRT_x86_32.cpp
src/hotspot/cpu/x86/c1_MacroAssembler_x86_32.cpp
// ... 等多个文件

// 构建系统更新
// 移除 linux-x86, windows-x86 等配置
```

**影响**: 简化了代码库，减少了维护负担。

### 2. C2 PhaseCCP 修复 (JDK-8371581)

**问题**: PhaseCCP 在某些情况下无法达到不动点。

**解决方案**: 改进 Value 节点的重访逻辑。

```cpp
// 变更前: 可能遗漏某些节点
void PhaseCCP::analyze() {
  while (!_worklist.is_empty()) {
    Node* n = _worklist.pop();
    // 处理节点
  }
}

// 变更后: 确保所有节点都被处理
void PhaseCCP::analyze() {
  while (!_worklist.is_empty()) {
    Node* n = _worklist.pop();
    // 处理节点
    // 如果值发生变化，重新添加依赖节点
    if (value_changed) {
      for (DUIterator i = n->outs(); n->has_out(i); i++) {
        _worklist.push(n->out(i));
      }
    }
  }
}
```

**影响**: 修复了编译器优化问题。

---

## 9. 开发风格

Aleksey Shipilev 的贡献特点:

1. **性能专家**: 深入理解 JVM 性能优化
2. **JMH 作者**: Java 微基准测试框架主要开发者
3. **数据驱动**: 每个优化都有详细的基准测试
4. **跨领域**: 涵盖编译器、GC、基准测试

---

## 10. 历史贡献 (JDK 8+)

Aleksey Shipilev 从 JDK 8 开始就有重要贡献：

| JDK 版本 | 主要贡献 |
|----------|----------|
| JDK 8 | JMH 框架初始版本 |
| JDK 9 | JMH 集成到 OpenJDK |
| JDK 11 | Shenandoah GC 优化 |
| JDK 17 | 分代 ZGC 贡献 |
| JDK 21 | 虚拟线程性能优化 |
| JDK 26 | JEP 503, C2 优化 |

---

## 11. 相关链接

- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=Aleksey%20Shipilev)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=assignee%20%3D%20shade)
- [JMH 项目](https://openjdk.org/projects/code-tools/jmh/)
- [个人博客](https://shipilev.net/)

---

> **文档版本**: 2.0
> **最后更新**: 2026-03-20
> **更新内容**:
> - 修正教育背景 (ITMO University MSc, 2003-2009)
> - 补充职业历史 (Intel 时期)
> - 添加主导的 JEP 列表 (JEP 280, 318, 379, 501, 503)
> - 添加 JOL, JCStress 工具信息
> - 添加 JVM Anatomy Quarks 系列
> - 添加演讲和会议信息
> - 添加构建服务链接