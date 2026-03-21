# Shenandoah GC 详解

> 低延迟垃圾收集器，Red Hat 贡献

[← 返回 GC](../)

---
## 目录

1. [架构原理](#1-架构原理)
2. [工作流程](#2-工作流程)
3. [性能特性](#3-性能特性)
4. [VM 参数](#4-vm-参数)
5. [JDK 21+ 改进](#5-jdk-21-改进)
6. [性能对比](#6-性能对比)
7. [已知限制](#7-已知限制)
8. [相关链接](#8-相关链接)

---


## 1. 架构原理

### 核心设计

```
┌─────────────────────────────────────────────────────────┐
│              Shenandoah Architecture                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Application Thread                                     │
│       │                                                 │
│       ▼                                                 │
│  Brooks Barrier (读屏障)                               │
│       │                                                 │
│       ▼                                                 │
│  ┌─────────────────────────────────────────────────┐  │
│  │              Shenandoah Heap                     │  │
│  │  ┌────────────────────────────────────────────┐   │  │
│  │  │ Live Objects    │  Garbage            │   │  │
│  │  └────────────────────────────────────────────┘   │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  GC Thread                                              │
│       │                                                 │
│       ▼                                                 │
│  Concurrent Marking (并发标记)                         │
│       │                                                 │
│       ▼                                                 │
│  Concurrent Evacuation (并发回收)                      │
│       │                                                 │
│       └──────────────────────────────────────────┘     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 关键技术

#### 1. Brooks Pointer

**作用**: 对象头中存储转发指针

**实现**:
```java
// 对象头布局
object_header:
  [forwarding_address | mark_word | klass_ptr]

// 读取时通过 Brooks Barrier
Object obj = field.obj;
// 屏障检查 forwarding_address
// 如果已转发，返回新地址
```

**优势**:
- 无需染色指针 (与 ZGC 区别)
- 更好的平台兼容性
- 支持压缩 oops

#### 2. 读屏障 (Read Barrier)

**实现**:
```cpp
// 伪代码
Object* barrier(Object* obj) {
    if (obj != null) {
        // 检查转发指针
        Object* fwd = obj->forwarding_ptr();
        if (fwd != null) {
            return fwd;  // 返回新地址
        }
    }
    return obj;
}
```

#### 3. Region-Based Layout

**结构**:
```
Shenandoah Heap → Regions
Region: 256KB ~ 32MB (动态调整)

┌─────────────────────────────────────┐
│  Eden  │ Survivor │ Old │ Humongous │
└─────────────────────────────────────┘
```

---

## 2. 工作流程

### Shenandoah 周期

```
1. Concurrent Mark (并发标记)
   ├── Initial Mark (STW, 极短)
   ├── Concurrent Mark
   └── Final Mark (STW, 极短)

2. Concurrent Evacuation (并发回收)
   ├── 识别存活对象
   ├── 并发复制到新 Region
   └── 更新引用 (通过 Brooks Pointer)

3. Concurrent Update References (并发更新引用)
   ├── 栈扫描
   ├── 全局更新
   └── 最终清理

4. Concurrent Cleanup (并发清理)
   ├── 回收空 Region
   └── 重置 Region 状态
```

### 分代 Shenandoah (JDK 25+)

**JEP 521: Generational Shenandoah**

**改进**:
- 年轻代/老年代分离
- 年轻代独立 GC
- 老年代并发标记
- 吞吐量提升 ~15%

**配置**:
```bash
-XX:+UseShenandoahGC -XX:ShenandoahGCMode=generational  # 启用分代 (JDK 25+)
```

---

## 3. 性能特性

### 低延迟

| 场景 | 目标 |
|------|------|
| 小堆 (<8GB) | <1ms 暂停 |
| 中等堆 (8-32GB) | <3ms 暂停 |
| 大堆 (>32GB) | <5ms 暂停 |

### 高吞吐量

- 吞吐目标 > 95%
- GC 线程与应用线程高度并发
- STW 时间极短 (通常 <10ms)

### 平台兼容性

- 支持 x86_64, aarch64, riscv64, ppc64le, s390x
- 不依赖特殊硬件特性
- 支持压缩 oops

---

## 4. VM 参数

### 基础配置

```bash
# 启用 Shenandoah GC
-XX:+UseShenandoahGC

# 启发式算法
-XX:ShenandoahGCHeuristics=adaptive      # 自适应 (默认)
-XX:ShenandoahGCHeuristics=static       # 静态
-XX:ShenandoahGCHeuristics=compact      # 紧凑
-XX:ShenandoahGCHeuristics=aggressive   # 激进
-XX:ShenandoahGCHeuristics=generational # 分代 (JDK 21+)
```

### 调优参数

```bash
# GC 触发
-XX:ShenandoahGCCycleThreshold=0        # GC 循环阈值
-XX:ShenandoahFreeThreshold=10          # 空闲阈值 (%)

# 区域
-XX:ShenandoahMinRegionSize=256k        # 最小 Region
-XX:ShenandoahMaxRegionSize=32m         # 最大 Region

# 线程
-XX:ParallelGCThreads=8                 # 并发线程
-XX:ConcGCThreads=4                     # 并发标记线程
```

### 诊断参数

```bash
# 详细日志
-Xlog:gc*:file=shenandoah.log:level,tags
-Xlog:gc+heap=info:file=shenandoah.log
-Xlog:gc+ergo=debug:file=shenandoah.log

# 统计
-XX:+PrintGC                           # 打印 GC 日志
-XX:+PrintGCDetails                     # 详细 GC 信息
-XX:+ShenandoahGCHeuristics=verbose     # 启发式详细输出
```

---

## 5. JDK 25+ 改进

### JEP 521: Generational Shenandoah

**效果**:
- 吞吐量提升 15%
- 降低年轻代 GC 暂停
- 更好的内存利用率

### JDK 23+: 性能优化

**改进**:
- 减少屏障开销
- 优化转发指针更新
- 改进并发标记算法

---

## 6. 性能对比

| 堆大小 | G1 GC | ZGC | Shenandoah | 分代 Shenandoah |
|--------|-------|-----|------------|-----------------|
| 4GB | ~200ms | ~2ms | ~5ms | ~3ms |
| 8GB | ~300ms | ~3ms | ~8ms | ~5ms |
| 16GB | ~500ms | ~5ms | ~10ms | ~8ms |
| 32GB | ~800ms | ~10ms | ~15ms | ~12ms |

---

## 7. 已知限制

### 不支持的场景

- 需要大量原生内存的应用
- 超大对象分配 (>Region 大小)

### 注意事项

- 读屏障有一定开销 (约 5-10%)
- 需要足够的 CPU 资源支持并发
- 平台差异 (x86_64 最优)

---

## 8. 相关链接

- [JEP 521: Generational Shenandoah](https://openjdk.org/jeps/521) - 分代 Shenandoah 规范
- [Shenandoah GC Wiki](https://wiki.openjdk.org/spaces/shenandoah/) - 技术文档
- [Understanding Shenandoah](https://inside.java/2024/05/07/generational-shenandoah/) - 深入解析
- [VM 参数](vm-parameters.md) - GC 参数参考
