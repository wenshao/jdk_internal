# 核心平台

JVM、内存、性能、模块系统等底层技术。

[← 返回主题索引](../)

---

## 演进概览

```
JDK 1.0 ─── JDK 5 ─── JDK 8 ─── JDK 11 ─── JDK 17 ─── JDK 21 ─── JDK 26
   │           │           │            │            │            │           │
 解释器      分层编译    元空间      ZGC         强封装      虚拟线程    分代 ZGC
 Serial GC   G1 GC      Lambda      JFR         内部API     Project Loom G1优化
```

### 版本里程碑

| 版本 | 主题 | 关键特性 |
|------|------|----------|
| **JDK 5** | 性能革命 | 分层编译、JMX、并发工具 |
| **JDK 8** | 内存模型 | 元空间、Lambda、Compressed Oops |
| **JDK 11 LTS** | 低延迟 | ZGC (实验)、JFR、HTTP Client |
| **JDK 17 LTS** | 强封装 | 遗留封装限制、JDK 内部 API 封装 |
| **JDK 21 LTS** | 高并发 | 虚拟线程、分代 ZGC |
| **JDK 26** | 性能优化 | G1 +10-20%、ZGC NUMA |

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

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### GC 团队 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Albert Mingkun Yang | 681 | Oracle | G1 GC, 内存管理 |
| 2 | Thomas Schatzl | 674 | Oracle | G1 GC 维护者 |
| 3 | Aleksey Shipilev | 324 | Oracle | 性能基准, 内存 |
| 4 | Zhengyu Gu | 252 | Oracle | JVM 运行时 |
| 5 | Kim Barrett | 235 | Oracle | C++ 现代化 |
| 6 | Stefan Karlsson | 229 | Oracle | 分代 ZGC (JEP 439) |
| 7 | Per Lidén | 198 | Oracle | ZGC 创始人 |
| 8 | Roman Kennke | 163 | Red Hat | Shenandoah GC |
| 9 | William Kemper | 112 | Red Hat | 分代 Shenandoah (JEP 429) |

### JVM/性能团队 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Coleen Phillimore | 333 | Oracle | 类加载, 运行时 |
| 2 | David Holmes | 201 | Oracle | 并发, 线程 |
| 3 | Ioi Lam | 167 | Oracle | CDS, AOT |
| 4 | Aleksey Shipilev | 123 | Oracle | 性能基准 |
| 5 | Kim Barrett | 115 | Oracle | C++ 现代化 |
| 6 | Thomas Stuefe | 112 | Oracle | 内存, 跨平台 |
| 7 | Serguei Spitsyn | 107 | Oracle | JVMTI, JFR |

### 模块系统

| 贡献者 | 公司 | 主要贡献 |
|--------|------|----------|
| **Mark Reinhold** | Oracle | JPMS (JEP 261) 首席架构师 |
| **Alex Buckley** | Oracle | JLS/JVMS 规范维护 |

---

## 内部开发者资源

### HotSpot 源码结构

```
src/hotspot/share/
├── gc/                          # GC 实现
│   ├── g1/                      # G1 GC
│   ├── shenandoah/              # Shenandoah GC
│   ├── z/                       # ZGC
│   ├── parallel/                # Parallel GC
│   ├── serial/                  # Serial GC
│   └── shared/                  # GC 共享代码
├── interpreter/                 # 解释器
├── compiler/                    # JIT 编译器
│   ├── c1/                      # C1 (Client Compiler)
│   ├── c2/                      # C2 (Server Compiler)
│   └── graal/                   # Graal JIT (可选)
├── oops/                        # 对象模型
│   ├── instanceKlass.cpp        # 类元数据
│   ├── arrayKlass.cpp           # 数组类
│   └── symbol.cpp               # 符号表
├── memory/                      # 内存管理
│   ├── metaspace.cpp            # 元空间
│   ├── universe.cpp             # 堆初始化
│   └── virtualspace.cpp         # 虚拟内存
├── classfile/                   # 类文件处理
├── classloader/                 # 类加载器
├── prims/                       # JVM 内部原语
│   ├── jni.cpp                  # JNI 实现
│   ├── jvmti.cpp                # JVMTI 实现
│   └── jvm.cpp                  # JVM 接口
└── runtime/                     # 运行时
    ├── thread.cpp               # 线程实现
    ├── mutex.cpp                # 锁实现
    └── safepoint.cpp            # Safepoint
```

### 关键内部类

| 类 | 作用 | 访问级别 |
|---|------|----------|
| `jdk.internal.misc.Unsafe` | 直接内存访问 | `@Restricted` |
| `jdk.internal.vm.VectorSupport` | Vector API 支持 | 内部 |
| `jdk.internal.access.JavaLangAccess` | 内部访问 | `@Restricted` |
| `jdk.internal.misc.Signal` | Unix 信号 | 内部 |

### VM 参数速查

```bash
# GC 选择
-XX:+UseG1GC                    # G1 (默认 JDK 9+)
-XX:+UseZGC                     # ZGC
-XX:+UseShenandoahGC            # Shenandoah
-XX:+UseParallelGC              # Parallel
-XX:+UseSerialGC                # Serial

# 内存配置
-Xms4g                          # 初始堆
-Xmx8g                          # 最大堆
-XX:MetaspaceSize=256m          # 元空间初始大小
-XX:MaxMetaspaceSize=512m       # 元空间最大值
-XX:CompressedClassSpaceSize=1g # 压缩类空间

# GC 调优
-XX:MaxGCPauseMillis=200        # G1 目标暂停时间
-XX:G1HeapRegionSize=16m        # G1 Region 大小
-XX:ConcGCThreads=4             # 并发 GC 线程
-XX:ParallelGCThreads=8         # 并行 GC 线程

# 性能诊断
-XX:+PrintGCDetails             # GC 详细日志
-XX:+PrintGCTimeStamps          # GC 时间戳
-Xlog:gc*:file=gc.log           # JDK 9+ 统一日志
-XX:+UseStringDeduplication     # 字符串去重

# JIT 编译
-XX:TieredStopAtLevel=3         # 分层编译级别
-XX:CompileThreshold=10000      # C2 编译阈值
-XX:+PrintCompilation           # 打印编译信息
-XX:+UnlockDiagnosticVMOptions  # 解锁诊断选项
-XX:+LogCompilation             # 记录编译日志
```

### 诊断工具

```bash
# jstat - GC 统计
jstat -gcutil <pid> 1000 10

# jmap - 堆转储
jmap -dump:live,format=b,file=heap.hprof <pid>

# jstack - 线程转储
jstack -l <pid>

# jinfo - VM 参数
jinfo -flags <pid>

# jcmd - JVM 诊断
jcmd <pid> GC.heap_info
jcmd <pid> VM.flags
jcmd <pid> Thread.print

# JFR (JDK 11+)
jcmd <pid> JFR.start name=myrecording
jcmd <pid> JFR.dump name=myrecording filename=recording.jfr
```

---

## 统计数据

| 指标 | 数值 |
|------|------|
| GC 算法 | 5 (Serial, Parallel, G1, ZGC, Shenandoah) |
| JIT 编译器 | 2 (C1, C2) + Graal |
| 类加载器层次 | 3 (Bootstrap, Platform, Application) |
| JFR 事件类型 | 200+ |

---

## 学习路径

1. **入门**: [性能优化](performance/) → 了解 JVM 执行模型
2. **进阶**: [内存管理](memory/) → [GC 演进](gc/) → 理解内存和 GC
3. **深入**: [类加载器](classloading/) → [模块系统](modules/) → 理解类加载机制
4. **专家**: [JVM 调优](jvm/) → 掌握生产调优
