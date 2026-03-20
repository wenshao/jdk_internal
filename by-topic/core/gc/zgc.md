# ZGC 详解

> Z Garbage Collector: 低延迟垃圾收集器

[← 返回 GC](../)

---

## 架构原理

### 核心设计

```
┌─────────────────────────────────────────────────────────┐
│                    ZGC Architecture                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Application Thread                                      │
│       │                                                 │
│       ▼                                                 │
│  Load Barrier (读屏障)                                  │
│       │                                                 │
│       ▼                                                 │
│  ┌─────────────────────────────────────────────────┐  │
│  │              ZGC Page (物理页)                     │  │
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
│  Concurrent Relocation (并发回收)                      │
│       │                                                 │
│       └──────────────────────────────────────────┘     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 关键技术

#### 1. 读屏障 (Load Barrier)

**作用**: 在对象引用读取时执行，维护 GC 相关信息

**实现**:
```java
// 伪代码
Object load(Object obj) {
    if (obj != null) {
        // 标记引用关系
        mark_color(obj);
        // 可能触发 GC
    }
    return obj;
}
```

#### 2. 染色指针 (Colored Pointers)

**作用**: 在对象指针中存储 GC 信息

**实现**:
```
64 位指针:
[63:0] 对象地址
[-1]    染色位 (GC 状态)
```

#### 3. Region-Based Page

**作用**: 页面按 Region 组织，便于并发回收

**结构**:
```
ZGC Page → Small/Medium/Large
Small: 512KB
Medium: 2MB
Large: 32MB+
```

---

## 工作流程

### ZGC 周期

```
1. GC Phase Start
   ├── 全局暂停 (通常 <1ms)
   └── 标记根集合

2. Concurrent Mark
   ├── 遍历对象图
   ├── 标记存活对象
   └── SATB (Snapshot-At-The-Beginning)

3. Concurrent Relocate
   ├── 识别存活对象
   ├── 重分配到新位置
   └── 更新引用

4. Concurrent Compact
   ├── 压缩内存
   ├── 更新引用
   └── 释放 Region
```

### 分代 ZGC (JDK 21+)

**JEP 439: Generational ZGC**

**改进**:
- 年轻代/老年代分离
- 年轻代频繁 GC
- 老年代较少 GC
- 吞吐量提升 ~10%

**配置**:
```bash
-XX:+ZGenerational              # 启用分代 ZGC (JDK 21+)
-XX:ZYoungGCFrequency=10        # 年轻代 GC 频率
```

---

## 性能特性

### 低延迟

| 场景 | 目标 |
|------|------|
| 小堆 (<8GB) | <1ms 暂停 |
| 中等堆 (8-32GB) | <2ms 暂停 |
| 大堆 (>32GB) | <5ms 暂停 |

### 高吞吐量

- 吞用目标 > 98%
- GC 线程与应用线程并发执行
- 最小化 STW 时间

### 可扩展性

- 支持 TB 级堆
- NUMA 友好 (JDK 21+)
- 动态调整 GC 线程数

---

## VM 参数

### 基础配置

```bash
# 启用 ZGC
-XX:+UseZGC

# 分代 ZGC (JDK 21+)
-XX:+ZGenerational

# NUMA 支持
-XX:+UseNUMA
-XX:+UseNUMAInterleaving
```

### 调优参数

```bash
# GC 间隔
-XX:ZCollectionInterval          # 自动 GC 间隔
-XX:ZAllocationSpikeTolerance     # 分配尖刺容忍度

# 碎片率
-XX:ZFragmentationLimit           # 碎片率阈值
-XX:ZCollectionIntervalMajor      # Major GC 间隔

# 线程数
-XX:ParallelGCThreads             # GC 工作线程
-XX:ConcGCThreads                 # 并发标记线程
```

### 诊断参数

```bash
# 详细日志
-Xlog:gc*:file=zgc.log:level,tags
-Xlog:gc+heap=info:file=zgc.log
-Xlog:gc+gc+start=debug:file=zgc.log

# 统计
-XX:+PrintGC                    # 打印 GC 日志
-XX:+PrintGCDetails              # 详细 GC 信息
-XX:+PrintGCTimeStamps          # GC 时间戳
```

---

## JDK 21+ 改进

### JEP 439: Generational ZGC

**效果**:
- 吞吐量提升 10%
- 降低 GC 频率
- 更好的内存利用率

### JEP 379: 并发线程栈扫描

**效果**:
- 消除栈扫描 STW
- 进一步降低暂停时间

### JDK 23+: 默认分代模式

**JEP 474**: 分代 ZGC 成为默认

---

## 性能对比

| 堆大小 | G1 GC | ZGC | 分代 ZGC |
|--------|-------|-----|---------|
| 4GB | ~200ms | ~2ms | ~2ms |
| 8GB | ~300ms | ~3ms | ~2ms |
| 16GB | ~500ms | ~5ms | ~3ms |
| 32GB | ~800ms | ~10ms | ~5ms |

---

## 已知限制

### 不支持的场景

- compressed oops 关闭 (JDK 16+ 已移除此选项)
- 非 x86_64/aarch64 架构 (部分支持)

### 注意事项

- 需要足够的物理内存 (建议至少 2GB)
- 频繁分配/释放大对象可能影响性能
- 与某些 JNI 操作可能有兼容性问题

---

## 相关链接

- [JEP 439: Generational ZGC](https://openjdk.org/jeps/439) - 分代 ZGC 规范
- [ZGC Wiki](https://wiki.openjdk.org/spaces/zgc/) - 技术文档
- [Understanding ZGC](https://inside.java/2023/11/28/gen-zgc-explainer/) - 深入解析
- [VM 参数](../vm-parameters.md) - GC 参数参考
