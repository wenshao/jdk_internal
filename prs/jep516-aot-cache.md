# AOT 对象缓存与任意 GC 支持

> JEP 516 | Erik Osterlund | JDK 26

---

## 概述

JEP 516 增强了 HotSpot JVM 的 **AOT (Ahead-of-Time) 对象缓存**机制，使其能够与任意垃圾收集器配合工作，包括低延迟的 Z Garbage Collector (ZGC)。核心方法是将缓存对象以 **GC 无关的中性格式** 存储，而非 GC 特定的内存格式，从而解除 AOT 缓存与特定 GC 实现之间的耦合。

| 属性 | 值 |
|------|-----|
| **JEP** | [JEP 516](https://openjdk.org/jeps/516) |
| **作者** | Erik Osterlund |
| **目标版本** | JDK 26 |
| **类型** | Feature |
| **组件** | hotspot / gc |
| **状态** | Closed / Delivered |
| **Issue** | [JDK-8365932](https://bugs.openjdk.org/browse/JDK-8365932) |
| **重要性** | 启动性能 + GC 兼容性关键 |

---

## 问题背景

### 为什么需要 JEP 516？

JEP 483 (JDK 24) 引入了 AOT 类加载与链接，使 Spring PetClinic 等应用的启动时间缩短约 41%（通过缓存约 21,000 个类）。然而，**先前的 AOT 对象缓存方式与 ZGC 不兼容**，用户被迫在两种延迟之间做出选择：

```
┌────────────────────────────────────────────────────────────────────┐
│                         用户面临的困境                              │
├────────────────────────────┬───────────────────────────────────────┤
│   选择 ZGC                 │   选择 G1/Parallel + AOT 缓存         │
├────────────────────────────┼───────────────────────────────────────┤
│ ✅ GC 暂停 < 1ms           │ ✅ 启动速度快 (-41%)                  │
│ ✅ 支持大堆 (≤16TB)        │ ✅ 类预加载、对象缓存                  │
│ ❌ 无法使用 AOT 对象缓存    │ ❌ GC 暂停时间较长                    │
│ ❌ 启动延迟高               │ ❌ 大堆场景受限                       │
└────────────────────────────┴───────────────────────────────────────┘

JEP 516 的目标: 同时获得两者的优势
```

### 不同 GC 引用格式不兼容的根因

各 GC 使用完全不同的对象引用格式，这是 AOT 对象缓存无法跨 GC 共享的根本原因：

```
不同 GC 的引用格式:

Serial / Parallel / G1:
  ┌─────────────────────────────────────────────────┐
  │ 64 位直接地址 或 32 位压缩地址                     │
  │ 多种压缩方案 (取决于堆大小)                        │
  │ G1 额外: 高位编码 Region 信息, 大对象独占 Region   │
  └─────────────────────────────────────────────────┘

ZGC:
  ┌─────────────────────────────────────────────────┐
  │ 区分小/中/大对象, 各有专用引用格式                  │
  │ 引用中编码元数据位 (用于并发收集)                   │
  │ 与其他 GC 的引用格式完全不兼容                      │
  └─────────────────────────────────────────────────┘
```

---

## 解决方案

### 核心创新: 逻辑索引替代内存地址

JEP 516 的关键创新是在缓存中使用 **逻辑索引 (logical indices)** 替代直接内存地址。这使得缓存数据与特定 GC 的内存布局解耦。

```
以 String 对象为例:

传统方式 (GC 特定格式 - 直接内存地址):
┌─────────┬───────────────────┬─────────┬──────┬────────────┐
│ header  │ value: 0x40020452 │ coder   │ hash │ hashIsZero │
│   ...   │   78              │   ...   │ ...  │    ...     │
└─────────┴───────────────────┴─────────┴──────┴────────────┘
                  ↑
           直接指向 byte[] 的内存地址
           (与 GC 的内存布局绑定)


JEP 516 方式 (GC 无关格式 - 逻辑索引):
┌─────────┬───────────────────┬─────────┬──────┬────────────┐
│ header  │ value: 5          │ coder   │   hash │ hashIsZero │
│   ...   │                   │   ...   │ ...  │    ...     │
└─────────┴───────────────────┴─────────┴──────┴────────────┘
                  ↑
           逻辑索引 5 → 通过查找表映射到实际地址
           (与任何 GC 兼容)
```

### Streaming vs Mapping: 两种加载策略

```
┌─────────────────────────────────────────────────────────────────┐
│                    两种对象加载策略对比                           │
├─────────────────────────┬───────────────────────────────────────┤
│  Mapping (GC 特定格式)   │  Streaming (GC 无关格式)              │
├─────────────────────────┼───────────────────────────────────────┤
│ 内存映射, 即时可用        │ 后台线程逐个物化对象                   │
│ 要求 GC 引用格式匹配     │ 通过 Access API 让 GC 自行布局        │
│ 适合单核 + 热启动         │ 适合多核 + 冷启动                     │
│ 零额外 CPU 开销          │ 需要一个空闲 CPU 核心                  │
│ 无法跨 GC 使用           │ 任何 GC 均可使用                      │
└─────────────────────────┴───────────────────────────────────────┘
```

### 对象物化 (Materialization) 流程

后台线程在 JVM 启动时执行以下步骤：

```
Streaming 物化流程:

┌─────────────────────────────────────────────────────────┐
│ 后台线程                        │  主线程 (应用启动)     │
├─────────────────────────────────┼───────────────────────┤
│ 1. 打开 AOT 缓存文件            │                       │
│ 2. 读取对象数据                  │  初始化 JVM           │
│ 3. 为每个对象:                   │                       │
│    a) 分配堆内存                 │  加载 bootstrap 类    │
│    b) 用缓存数据初始化字段        │                       │
│    c) 逻辑索引 → 实际地址        │  加载应用类           │
│       (通过查找表)               │                       │
│ 4. 所有对象就绪                  │  ← 同步点 (若需要)    │
│                                 │  main() 执行          │
└─────────────────────────────────┴───────────────────────┘

Spring PetClinic 实测:
  - AOT 缓存对象大小: ~2 MB
  - 主线程因等待阻塞: ~2 ms
  - 后台线程物化耗时: ~6 ms (与 JVM 启动并行)
```

---

## 基线 AOT 缓存

JDK 26 随发行版内置了 **两个基线 AOT 缓存**，即使应用程序不提供自定义缓存，JVM 也能自动选择最优策略：

```
JDK 26 基线缓存:

┌───────────────────────────────────────────────────────────┐
│  JVM 启动                                                 │
│    ↓                                                      │
│  检测运行环境                                              │
│    ↓                                                      │
│  ┌─────────────────────┐    ┌──────────────────────────┐  │
│  │ 使用 ZGC?           │ 是 │ 选择 GC 无关基线缓存      │  │
│  │ -XX:-CompressedOops?│───→│ (Streaming 方式加载)      │  │
│  │ 堆 > 32GB?          │    └──────────────────────────┘  │
│  └────────┬────────────┘                                  │
│           │ 否                                            │
│           ↓                                               │
│  ┌──────────────────────────┐                             │
│  │ 选择 GC 特定基线缓存      │                             │
│  │ (Mapping 方式加载)        │                             │
│  └──────────────────────────┘                             │
└───────────────────────────────────────────────────────────┘
```

### 自动选择策略

| 训练条件 | 选择的缓存格式 | 加载方式 |
|----------|----------------|----------|
| 使用 ZGC | GC 无关格式 | Streaming |
| `-XX:-CompressedOops` | GC 无关格式 | Streaming |
| 堆 > 32 GB | GC 无关格式 | Streaming |
| `-XX:+UseCompressedOops` (堆 < 32GB, 非 ZGC) | GC 特定格式 | Mapping |

---

## 使用方法

### 1. 使用默认基线 AOT 缓存 (零配置)

```bash
# JDK 26 默认启用基线 AOT 缓存, 无需额外配置
# 以下命令自动受益于基线缓存:

# 使用 G1 GC (默认) - 自动选择 GC 特定缓存
java -jar myapp.jar

# 使用 ZGC - 自动选择 GC 无关缓存
java -XX:+UseZGC -jar myapp.jar
```

### 2. 创建自定义 AOT 缓存

```bash
# 步骤 1: 训练运行 - 记录应用行为并生成 AOT 缓存
java -XX:AOTCacheOutput=myapp.aot -jar myapp.jar

# 步骤 2: 使用自定义 AOT 缓存运行
java -XX:AOTCache=myapp.aot -jar myapp.jar
```

### 3. 强制使用 GC 无关格式 (Streaming)

```bash
# 使用诊断选项强制生成 streamable 格式的缓存
java -XX:+UnlockDiagnosticVMOptions \
     -XX:AOTCacheOutput=streamable-cache.aot \
     -XX:+AOTStreamableObjects \
     -jar myapp.jar

# 使用该缓存运行
java -XX:AOTCache=streamable-cache.aot -jar myapp.jar
```

### 4. Spring PetClinic 完整示例

```bash
# 训练运行 - 生成 streamable AOT 缓存
java -XX:+UnlockDiagnosticVMOptions \
     -XX:AOTCacheOutput=petclinic.aot \
     -XX:+AOTStreamableObjects \
     -jar spring-petclinic-4.0.0-SNAPSHOT.jar

# 生产运行 - 使用 ZGC + AOT 缓存
java -XX:+UseZGC \
     -XX:AOTCache=petclinic.aot \
     -jar spring-petclinic-4.0.0-SNAPSHOT.jar
```

---

## JVM 参数

### AOT 缓存配置

```bash
# 生成 AOT 缓存 (训练运行)
-XX:AOTCacheOutput=<path>

# 使用 AOT 缓存 (生产运行)
-XX:AOTCache=<path>

# 强制使用 GC 无关的 streamable 格式 (诊断选项)
-XX:+UnlockDiagnosticVMOptions
-XX:+AOTStreamableObjects

# 选择 GC
-XX:+UseZGC              # Z Garbage Collector
-XX:+UseG1GC             # G1 (默认)
-XX:+UseParallelGC       # Parallel GC
-XX:+UseSerialGC         # Serial GC
```

---

## 性能数据

### Spring PetClinic 启动性能

```
Spring PetClinic (缓存约 21,000 个类):

                        无 AOT 缓存      有 AOT 缓存       提升
───────────────────────────────────────────────────────────────────
启动时间               ~2,400 ms        ~1,400 ms         -41%
类加载                 ~1,000 ms        ~200 ms           -80%
───────────────────────────────────────────────────────────────────
```

### Streaming 加载开销 (Spring PetClinic)

```
GC 无关格式 Streaming 加载:

AOT 缓存对象大小:     ~2 MB
后台物化线程耗时:     ~6 ms   (与 JVM 启动并行执行)
主线程阻塞时间:       ~2 ms   (等待同步)
额外 CPU 需求:        1 个空闲核心

结论: Streaming 加载的额外开销可以忽略不计
```

### 冷启动 vs 热启动

```
┌────────────────────────────────────────────────────────────────┐
│                冷启动 vs 热启动性能对比                          │
├─────────────────┬─────────────────────┬────────────────────────┤
│                 │ 冷启动              │ 热启动                  │
│                 │ (首次,无文件缓存)    │ (重复启动,有文件缓存)   │
├─────────────────┼─────────────────────┼────────────────────────┤
│ Streaming       │ ✅ 可掩盖磁盘 I/O   │ 正常                   │
│ (GC 无关)       │    延迟              │                        │
├─────────────────┼─────────────────────┼────────────────────────┤
│ Mapping         │ 受磁盘 I/O 影响     │ ✅ 即时加载, 零开销     │
│ (GC 特定)       │                     │    适合单核环境         │
└─────────────────┴─────────────────────┴────────────────────────┘
```

### 云原生场景

```
容器启动 (Kubernetes + ZGC):

JEP 516 之前:
  - ZGC 无法使用 AOT 对象缓存
  - 启动时间: 完整冷启动延迟
  - 扩容时 p99 延迟受启动影响

JEP 516 之后:
  - ZGC 可完整使用 AOT 缓存
  - 启动时间: 与 G1 AOT 缓存接近
  - 扩容时保持低 GC 暂停 (< 1ms)
```

---

## 技术实现

### 文件变更

```
src/hotspot/
├── share/
│   ├── gc/
│   │   ├── shared/
│   │   │   ├── aotObjectCache.cpp       (新增: GC 无关对象缓存)
│   │   │   ├── aotObjectCache.hpp
│   │   │   ├── aotStreamableObjects.cpp (新增: Streaming 加载逻辑)
│   │   │   └── aotStreamableObjects.hpp
│   │   ├── z/
│   │   │   └── zAOTSupport.cpp          (新增: ZGC AOT 集成)
│   │   └── g1/
│   │       └── g1AOTSupport.cpp         (修改: G1 AOT 适配)
│   └── cds/
│       ├── heapShared.cpp               (修改: 堆共享扩展)
│       └── archiveBuilder.cpp           (修改: 缓存构建)
```

### 逻辑索引映射表

```cpp
// 概念示意: 逻辑索引 → 实际对象地址映射

class AOTObjectCache {
private:
    // 查找表: 索引 → 实际堆地址
    GrowableArray<oop> _index_to_object;

public:
    /**
     * 物化缓存对象 (后台线程执行)
     *
     * 1. 从缓存读取对象元数据
     * 2. 通过 GC Access API 分配内存
     * 3. 初始化字段, 将逻辑索引转换为实际地址
     * 4. 注册到查找表
     */
    void materialize_objects() {
        for (int i = 0; i < _cached_count; i++) {
            // 通过 Access API 分配 — GC 决定内存布局
            oop obj = allocate_via_access_api(_cached_metadata[i]);

            // 初始化字段
            for (auto& field : _cached_metadata[i].fields) {
                if (field.is_reference()) {
                    // 逻辑索引 → 实际对象引用
                    oop target = _index_to_object.at(field.logical_index());
                    obj->obj_field_put(field.offset(), target);
                } else {
                    obj->field_put(field.offset(), field.value());
                }
            }

            // 注册到查找表
            _index_to_object.at_put(i, obj);
        }
    }

    /**
     * 解析逻辑索引为实际对象引用
     */
    oop resolve(int logical_index) {
        return _index_to_object.at(logical_index);
    }
};
```

---

## 与 GraalVM Native Image 对比

```
AOT 对象缓存 (JEP 516) vs GraalVM Native Image:

┌─────────────────────┬──────────────────────────┬────────────────┐
│                     │ JEP 516 AOT 缓存         │ Native Image   │
├─────────────────────┼──────────────────────────┼────────────────┤
│ 启动时间            │ ~50-100ms               │ ~5ms            │
│ GC 选择             │ ✅ 任意 GC (含 ZGC)      │ ⚠️ Serial/G1   │
│ 动态特性            │ ✅ 完全支持              │ ⚠️ 有限支持     │
│ 反射                │ ✅ 完全支持              │ ⚠️ 需配置       │
│ JIT 编译            │ ✅ 支持 (峰值性能更高)    │ ❌ 不支持       │
│ 兼容性              │ ✅ 100%                  │ ⚠️ 部分限制     │
│ 构建复杂度          │ 低 (一条命令)             │ 高             │
│ 大堆支持 (>32GB)    │ ✅ 支持                  │ ⚠️ 受限         │
│ 调试体验            │ ✅ 标准                  │ ⚠️ 受限         │
└─────────────────────┴──────────────────────────┴────────────────┘
```

---

## 相关 JEP 演进路线

```
Project Leyden 演进路线:

┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  JEP 483 (JDK 24)          JEP 514 (JDK 25)                     │
│  AOT 类加载与链接           AOT 命令行增强                        │
│  ├─ 启动提升 ~41%           ├─ 3 步简化为 1 步                    │
│  ├─ 类预加载/预链接         ├─ java -XX:AOTCacheOutput=...        │
│  └─ 首次引入 AOT 缓存       └─ 降低使用门槛                      │
│       ↓                          ↓                               │
│  JEP 515 (JDK 25)          JEP 516 (JDK 26)                     │
│  AOT 方法性能分析           AOT 对象缓存 + 任意 GC                │
│  ├─ 解决 warmup 问题        ├─ GC 无关格式 (逻辑索引)             │
│  ├─ 训练运行记录热点方法     ├─ ZGC 支持                          │
│  └─ AOT 缓存中存储分析数据   ├─ 内置基线 AOT 缓存                 │
│                              └─ Streaming 加载机制                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

| JEP | 版本 | 名称 | 解决的问题 |
|-----|------|------|-----------|
| [JEP 483](https://openjdk.org/jeps/483) | JDK 24 | AOT 类加载与链接 | 启动时间 (类加载) |
| [JEP 514](https://openjdk.org/jeps/514) | JDK 25 | AOT 命令行增强 | 使用复杂度 (3 步→1 步) |
| [JEP 515](https://openjdk.org/jeps/515) | JDK 25 | AOT 方法性能分析 | 预热时间 (warmup) |
| [JEP 516](https://openjdk.org/jeps/516) | JDK 26 | AOT 对象缓存 + 任意 GC | GC 兼容性 (ZGC) |

---

## 被否决的替代方案

| 替代方案 | 描述 | 否决原因 |
|---------|------|---------|
| ZGC 专用缓存 | 创建 ZGC 专用的缓存格式 | 性能优势仅在单核环境体现, ZGC 通常运行在多核环境 |
| 修改 ZGC 解释多种引用格式 | 类似 Serial/Parallel 的适配方式 | 会将所有 GC 实现耦合在一起, 阻碍各 GC 独立演进 |

---

## 参考资料

- [JEP 516: Ahead-of-Time Object Caching with Any GC](https://openjdk.org/jeps/516)
- [JEP 483: Ahead-of-Time Class Loading & Linking](https://openjdk.org/jeps/483)
- [JEP 514: Ahead-of-Time Command-Line Ergonomics](https://openjdk.org/jeps/514)
- [JEP 515: Ahead-of-Time Method Profiling](https://openjdk.org/jeps/515)
- [Project Leyden](https://openjdk.org/projects/leyden/)
- [Inside.java - JEP 516 Target JDK 26](https://inside.java/2025/11/13/jep516-target-jdk26/)
- [Project Leyden & JDK 26: Bringing AOT Caching to ZGC](https://softwaremill.com/project-leyden-and-jdk-26-bringing-aot-caching-to-zgc/)

---

## 变更历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0 | 2025-10 | JEP 516 proposed to target JDK 26 |
| 1.1 | 2025-11 | JEP 516 targeted to JDK 26 |
| 1.2 | 2026-03 | JDK 26 GA, JEP 516 delivered |
