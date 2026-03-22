# 实战案例 (Case Studies)

> 来自生产环境的 JVM/JDK 问题排查案例，包含完整的诊断过程、工具使用和修复方案。

> **注意**: 所有案例中的数据均为 **示意数据**，用于说明排查思路和工具用法，不代表真实生产环境数据。

---

## 案例索引

### 内存问题

| 案例 | 场景 | JDK 版本 | 关键工具 | 难度 |
|------|------|----------|----------|------|
| [内存泄漏诊断](memory-leak-diagnosis.md) | 长期运行服务 OOM | JDK 21 | JFR, NMT, MAT, jcmd, jmap | 中高 |

### GC 问题

| 案例 | 场景 | JDK 版本 | 关键工具 | 难度 |
|------|------|----------|----------|------|
| GC 停顿分析 *(计划中)* | Full GC 频繁导致延迟抖动 | JDK 17 | JFR, GC 日志, GCViewer | 中 |
| ZGC 调优 *(计划中)* | 从 G1 迁移到 ZGC 的调优过程 | JDK 21 | JFR, -Xlog:gc | 中 |

### 线程问题

| 案例 | 场景 | JDK 版本 | 关键工具 | 难度 |
|------|------|----------|----------|------|
| 死锁诊断 *(计划中)* | 多线程竞争导致服务挂起 | JDK 17 | jstack, JFR, ThreadMXBean | 中 |
| 虚拟线程 pinning *(计划中)* | Virtual Thread 阻塞平台线程 | JDK 21 | JFR, -Djdk.tracePinnedThreads | 中 |

### 性能问题

| 案例 | 场景 | JDK 版本 | 关键工具 | 难度 |
|------|------|----------|----------|------|
| 启动时间优化 *(计划中)* | 微服务冷启动慢 | JDK 21 | AppCDS, JFR, async-profiler | 中 |
| JIT 编译回退 *(计划中)* | C2 编译失败导致性能下降 | JDK 17 | JFR, -XX:+PrintCompilation | 高 |

### 类加载问题

| 案例 | 场景 | JDK 版本 | 关键工具 | 难度 |
|------|------|----------|----------|------|
| Metaspace OOM *(计划中)* | 动态类加载导致 Metaspace 溢出 | JDK 11 | NMT, jcmd, JFR | 中 |
| 模块化迁移 *(计划中)* | JPMS 迁移中的反射访问问题 | JDK 17 | --add-opens, jdeps | 中 |

---

## 案例结构说明

每个案例文件遵循统一结构：

1. **场景描述** - 问题背景、环境配置、业务特征
2. **症状表现** - 可观测的异常现象 (监控指标、日志、告警)
3. **排查过程** - 逐步使用工具定位问题的过程
4. **根因分析** - 多个可能的根因及其诊断方法
5. **修复方案** - 具体的代码/配置修改
6. **经验总结** - 可复用的排查思路和最佳实践

---

## 工具速查

案例中常用的诊断工具：

| 工具 | 用途 | 参考 |
|------|------|------|
| `jcmd` | JVM 诊断命令 (NMT, JFR, GC 等) | [JFR 指南](../guides/jfr.md) |
| `jmap` | Heap Dump 导出 | 案例内详述 |
| `jstack` | 线程转储 | 案例内详述 |
| JFR | 低开销持续诊断 | [JFR 指南](../guides/jfr.md) |
| MAT (Memory Analyzer) | Heap Dump 分析 | 案例内详述 |
| NMT | Native Memory Tracking | 案例内详述 |
| async-profiler | CPU/Alloc 采样 | 案例内详述 |

---

## 相关资源

- [JFR 实战指南](../guides/jfr.md) - JFR 详细使用方法
- [GC 演进](../by-topic/core/gc/) - 各版本 GC 特性对比
- [内存管理](../by-topic/core/memory/) - 堆/栈/Metaspace 详解
- [性能优化](../by-topic/core/performance/) - JFR/调优专题
