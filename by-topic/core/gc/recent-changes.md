# GC 近期改进

> JDK 21-26 垃圾收集器改进汇总

[← 返回 GC](../)

---
## 目录

1. [JDK 26 (2025)](#1-jdk-26-2025)
2. [JDK 23 (2024)](#2-jdk-23-2024)
3. [JDK 22 (2024)](#3-jdk-22-2024)
4. [JDK 21 (2023 LTS)](#4-jdk-21-2023-lts)
5. [ZGC 时间线](#5-zgc-时间线)
6. [Shenandoah 时间线](#6-shenandoah-时间线)
7. [G1 GC 时间线](#7-g1-gc-时间线)
8. [版本对比](#8-版本对比)
9. [邮件列表讨论](#9-邮件列表讨论)
10. [相关链接](#10-相关链接)
11. [参与贡献](#11-参与贡献)

---


## 1. JDK 26 (2025)

### JEP 522: G1 GC 吞吐量优化

**状态**: 已集成

**改进内容**:
- 减少 G1 GC 同步开销
- 写屏障从 ~50 指令减少到 ~12 指令
- 减少 card table 同步频率
- 吞吐量提升 10-20%

**相关链接**:
- [JEP 522](https://openjdk.org/jeps/522)
- [PR #21373](https://github.com/openjdk/jdk/pull/21373)

### JDK-8340592: ZGC NUMA 支持

**状态**: 已集成

**改进内容**:
- NUMA 感知内存分配
- 跨 NUMA 节点访问优化
- 多插槽服务器性能提升

---

## 2. JDK 23 (2024)

### JEP 474: 分代 ZGC 成为默认

**状态**: 正式

**改进内容**:
- 分代 ZGC 成为 ZGC 默认模式
- 无需显式 `-XX:+ZGenerational`
- 性能自动优化

### JDK-8318585: ZGC 压缩指针优化

**作者**: Per Lidén

**改进内容**:
- 优化压缩指针布局
- 减少内存开销
- 改进大堆性能

---

## 3. JDK 22 (2024)

### JDK-8321847: Shenandoah 并发改进

**作者**: Roman Kennke

**改进内容**:
- 减少并发阶段同步
- 优化 Brooks Barrier
- 降低延迟

### JDK-8314234: G1 Region Pinning

**作者**: Thomas Schatzl

**改进内容**:
- Region Pinning 机制优化
- JNI Critical 支持改进
- 减少 GC 竞争

---

## 4. JDK 21 (2023 LTS)

### JEP 439: 分代 ZGC

**状态**: 正式

**改进内容**:
- 年轻代/老年代分离
- 年轻代独立 GC
- 吞吐量提升 ~10%
- 堆占用降低 ~20%

**配置**:
```bash
-XX:+ZGenerational  # JDK 21+
# JDK 23+ 默认启用
```

**相关链接**:
- [JEP 439](https://openjdk.org/jeps/439)
- [Inside Java: Generational ZGC](https://inside.java/2023/11/28/gen-zgc-explainer/)

### JEP 521: 分代 Shenandoah

**状态**: 正式 (JDK 25)

**改进内容**:
- 年轻代/老年代分离
- 吞吐量提升 ~15%
- 降低暂停时间

**配置**:
```bash
-XX:+UseShenandoahGC -XX:ShenandoahGCMode=generational
```

**相关链接**:
- [JEP 521](https://openjdk.org/jeps/521)

### JDK-8307390: ZGC 并发线程栈扫描

**改进内容**:
- 线程栈扫描并发化
- 消除栈扫描 STW
- 进一步降低暂停时间

---

## 5. ZGC 时间线

### JDK 15 (2020)
- ZGC 成为正式特性

### JDK 11 (2018)
- ZGC 首次发布 (实验性)
- 支持 x86_64

### JDK 14
- 支持 Windows 和 macOS

### JDK 15+
- 支持 macOS ARM64 (Apple Silicon)
- 支持 multi-mapping

---

## 6. Shenandoah 时间线

### JDK 15 (2020)
- Shenandoah 成为正式特性

### JDK 12 (2019)
- Shenandoah 首次发布

### JDK 25+
- 分代 Shenandoah (JEP 521)

---

## 7. G1 GC 时间线

### JDK 9 (2017)
- G1 成为默认 GC

### JDK 6u45 (2012)
- G1 首次发布

### JDK 26
- JEP 522: 吞吐量优化

---

## 8. 版本对比

| 版本 | 主要 GC 改进 |
|------|--------------|
| **JDK 21** | 分代 ZGC |
| **JDK 22** | G1 Region Pinning, Shenandoah 并发优化 |
| **JDK 23** | 分代 ZGC 默认, 压缩指针优化 |
| **JDK 24** | 稳定性修复, 性能调优 |
| **JDK 25** | 分代 Shenandoah, NUMA 优化 |
| **JDK 26** | JEP 522: G1 吞吐量优化 |

---

## 9. 邮件列表讨论

### hotspot-gc-dev (2024-2025)

**关键讨论**:
1. 分代 ZGC 默认化 (JEP 474)
2. G1 GC 吞吐量优化 (JEP 522)
3. NUMA 支持设计
4. Region Pinning 语义

**存档**: [mail.openjdk.org/pipermail/hotspot-gc-dev/](https://mail.openjdk.org/pipermail/hotspot-gc-dev/)

---

## 10. 相关链接

### JEP 文档

- [JEP 439: Generational ZGC](https://openjdk.org/jeps/439)
- [JEP 521: Generational Shenandoah](https://openjdk.org/jeps/521)
- [JEP 522: G1 GC Throughput](https://openjdk.org/jeps/522)
- [JEP 474: ZGC Defaults to Generational](https://openjdk.org/jeps/474)

### 技术博客

- [Understanding Generational ZGC](https://inside.java/2023/11/28/gen-zgc-explainer/)
- [Understanding Generational Shenandoah](https://inside.java/2024/05/07/generational-shenandoah/)
- [G1 GC Improvements](https://inside.java/2025/01/15/g1-improvements/)

---

## 11. 参与贡献

### 如何报告 GC 问题

1. 收集 GC 日志:
   ```bash
   -Xlog:gc*:file=gc.log:time,level,tags
   ```

2. 收集堆转储 (如果 OOM):
   ```bash
   -XX:+HeapDumpOnOutOfMemoryError
   ```

3. 在 [bugs.openjdk.org](https://bugs.openjdk.org) 提交

4. 邮件发送到 hotspot-gc-dev

### 贡献者指南

- [OpenJDK Contributing Guide](https://openjdk.org/contribute/)
- [HotSpot GC Project Page](https://openjdk.org/projects/hotspot/)
