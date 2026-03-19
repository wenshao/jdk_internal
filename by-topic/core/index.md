# 核心平台

JVM、内存、性能、模块系统等底层技术。

---

## 主题列表

### [GC 演进](gc/)

垃圾收集器的发展历程，从 Serial 到分代 ZGC。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 8 | G1 成为主流，CMS 标记废弃 | - |
| JDK 11 | ZGC 引入 (实验性) | JEP 333 |
| JDK 15 | ZGC 生产可用 | JEP 378 |
| JDK 17 | 并发线程栈扫描 | JEP 379 |
| JDK 21 | **分代 ZGC** (JEP 439)、分代 Shenandoah (JEP 429) | JEP 439, JEP 429 |
| JDK 23 | ZGC 分代改进 | JEP 474 |
| JDK 26 | G1 吞吐量提升 (JEP 522)、ZGC NUMA | JEP 522 |

→ [GC 时间线](gc/timeline.md)

### [内存管理](memory/)

Java 内存管理从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 5 | WeakReference 等 | 引用类型 |
| JDK 6 | Compressed Oops | 压缩指针 |
| JDK 8 | 元空间、String Dedup | 永久代移除 |
| JDK 11 | ZGC | 低延迟 GC |
| JDK 15 | ZGC 生产可用 | 正式版 |
| JDK 21 | 分代 ZGC | 降低 GC 频率 |
| JDK 22 | Foreign Memory Access | 堆外内存 |

→ [内存管理时间线](memory/timeline.md)

### [性能优化](performance/)

Java 性能优化从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 1.0 | 解释器执行 | 纯解释 |
| JDK 5 | JIT 编译器 (HotSpot) | 分层编译 |
| JDK 6 | 性能统计工具 | jstat/jmap |
| JDK 7 | G1 GC、Compressed Oops | 内存优化 |
| JDK 8 | Lambda/String Dedup | 编译优化 |
| JDK 17 | Record/Pattern Matching | 编译器优化 |
| JDK 21 | 虚拟线程 | I/O 性能提升 |

→ [性能优化时间线](performance/timeline.md)

### [类加载器](classloading/)

Java 类加载器从 JDK 1.0 到 JDK 26 的完整演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 1.0 | Bootstrap/Extension/Application | 三层类加载 |
| JDK 1.2 | 自定义 ClassLoader | 用户类加载 |
| JDK 5 | ContextClassLoader | SPI 支持 |
| JDK 6 | Instrumentation | Java Agent |
| JDK 6 | ServiceLoader | SPI 标准化 |
| JDK 9 | Platform ClassLoader | 模块化 |
| JDK 17 | 强封装 | 内部 API 限制 |

→ [类加载器时间线](classloading/timeline.md)

### [模块系统](modules/)

Java 模块系统 (JPMS) 从 JDK 9 到现在的完整演进。

| 版本 | 主要变化 | JEP |
|------|----------|-----|
| JDK 9 | **JPMS** (JEP 261) | 模块化系统 |
| JDK 11 | jlink 定制运行时 | - |
| JDK 16 | 强封装 | - |
| JDK 17 | 遗留封装 | - |
| JDK 21 | 动态模块加载 | - |

→ [模块系统时间线](modules/timeline.md)

### [JVM 调优与监控](jvm/)

JVM 参数、调优工具和监控技术从 JDK 1.0 到 JDK 26 的演进。

| 版本 | 主要变化 | 说明 |
|------|----------|------|
| JDK 1.0 | 基础参数 (-Xmx, -Xms) | 内存配置 |
| JDK 5 | JMX, jconsole | 监控工具 |
| JDK 6 | jstat, jmap, jstack | 诊断工具 |
| JDK 7 | G1 GC | 新 GC 算法 |
| JDK 8 | Metaspace | 永久代移除 |
| JDK 9 | G1 成为默认 | GC 默认值 |
| JDK 11 | ZGC, JFR | 低延迟 GC |
| JDK 21 | 分代 ZGC | 生产就绪 |

→ [JVM 调优时间线](jvm/timeline.md)

---

## 学习路径

1. **入门**: [性能优化](performance/) → 了解 JVM 执行模型
2. **进阶**: [内存管理](memory/) → [GC 演进](gc/) → 理解内存和 GC
3. **深入**: [类加载器](classloading/) → [模块系统](modules/) → 理解类加载机制
4. **专家**: [JVM 调优](jvm/) → 掌握生产调优
