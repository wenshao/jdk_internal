# JIT 与 GC 协作

> JIT 编译器如何与垃圾收集器协作优化性能

[← 返回 JIT 编译](../)

---

## 结论先行

| 协作机制 | 优化效果 | 影响范围 |
|----------|----------|----------|
| **逃逸分析** | 栈上分配 | 减少 GC 压力 |
| **标量替换** | 消除对象 | 无 GC 开销 |
| **Safepoint 插入** | 安全点定位 | GC 准确性 |
| **Barrier 优化** | 减少 barrier 开销 | 写屏障优化 |
| **Card Mark 优化** | 减少卡片标记 | 跨代 GC |

---

## 一眼看懂

### JIT 与 GC 的关系

```
JIT 编译器生成代码时:
├── 插入 GC Safepoint
├── 生成 Read/Write Barrier
├── 标记对象引用位置
├── 优化逃逸对象 (栈上分配)
└── 标量替换 (消除对象)

GC 执行时:
├── 查找 Safepoint 停止线程
├── 使用 JIT 生成的元数据
├── 扫描栈上的对象
└── 更新引用关系
```

### 关键协作点

```
编译时协作:
├── 逃逸分析 → 减少对象分配
├── 标量替换 → 消除对象
├── Barrier 优化 → 减少 GC 开销
└── Safepoint 放置 → 平衡 GC 与性能

运行时协作:
├── 对象分配 → 选择合适 GC
├── 代码去优化 → GC 后类型假设失效
├── 编译排队 → GC 暂停时降低编译
└── 代码缓存清理 → 内存压力
```

---

## 1. 逃逸分析与 GC

### 逃逸分析对 GC 的影响

```
逃逸分析结果:
├── 不逃逸 → 栈上分配 (无 GC)
├── 部分逃逸 → 条件优化
├── 全局逃逸 → 堆分配 (有 GC)
└── 方法逃逸 → 可能标量替换
```

### 栈上分配

```java
// 示例: 临时对象不逃逸
public int calculate() {
    Point p = new Point(10, 20);  // 不逃逸
    return p.x + p.y;
}

// JIT 优化:
// 1. 逃逸分析发现 p 不逃逸
// 2. 标量替换为 int p$x = 10, p$y = 20
// 3. 完全消除对象分配
// 4. GC 无需处理此对象
```

### GC 压力减少

| 场景 | 无逃逸分析 | 有逃逸分析 | GC 减少 |
|------|-----------|-----------|---------|
| **局部临时对象** | 堆分配 | 栈分配/消除 | 100% |
| **方法返回对象** | 堆分配 | 可能优化 | 50-80% |
| **容器临时对象** | 堆分配 | 部分优化 | 30-50% |

---

## 2. 标量替换

### 标量替换原理

```
对象分解:
├── 字段 → 局部变量
├── 数组 → 多个标量
├── 嵌套对象 → 递归分解
└── 限制: 对象结构简单
```

### 示例

```java
// 原始代码
class Point {
    int x, y;
}

public int sum() {
    Point p = new Point();
    p.x = 10;
    p.y = 20;
    return p.x + p.y;
}

// JIT 标量替换后:
public int sum() {
    int p$x = 10;  // 标量
    int p$y = 20;  // 标量
    return p$x + p$y;
}

// 结果: 无对象分配，GC 无压力
```

### 对 GC 的好处

```
标量替换效果:
├── 减少对象分配 → 降低 GC 频率
├── 减少堆内存 → 降低 GC 时间
├── 减少引用关系 → 简化 GC 图
└── 提高缓存局部性 → 间接提升 GC
```

---

## 3. Safepoint 插入

### Safepoint 的作用

```
GC Safepoint:
├── 停止所有应用线程
├── 查找对象引用
├── 更新引用关系
└── 恢复线程执行
```

### JIT 如何插入 Safepoint

```java
// 原始代码
public void process() {
    for (int i = 0; i < 1000; i++) {
        doWork(i);
    }
}

// JIT 插入 Safepoint 后:
public void process() {
    for (int i = 0; i < 1000; i++) {
        // Safepoint poll (检查 GC 请求)
        if (ThreadLocalPoll.poll()) {
            safepoint();
        }
        doWork(i);
    }
}
```

### Safepoint 放置策略

| 位置 | 策略 | 影响 |
|------|------|------|
| **循环回边** | 总是插入 | GC 响应及时 |
| **方法返回** | 总是插入 | 确保安全退出 |
| **长时间运行** | 定期插入 | 避免 GC 等待 |
| **热点代码** | 最小化插入 | 减少开销 |

### Safepoint 开销

```
Safepoint Poll 开销:
├── 单次检查: ~1-2 条指令
├── 循环内: 每次 1-3 ns
├── 总体影响: < 1% 性能
└── GC 收益: 远大于开销
```

---

## 4. Barrier 优化

### GC Barrier 的作用

```
GC Barrier:
├── Read Barrier: 读引用时检查
├── Write Barrier: 写引用时记录
├── Card Mark: 记录跨代引用
└── SATB: Snapshot-at-the-beginning
```

### JIT 优化 Barrier

#### 写屏障优化

```java
// 原始代码
obj.field = value;  // 写引用

// JIT 生成的代码 (G1 GC):
StoreBarrier(obj, value);
obj.field = value;
if (G1GC) {
    card_mark = value >> card_shift;
    card_table[card_mark] = dirty;
}
```

#### Barrier 消除

```java
// JIT 可以证明不需要 barrier 的情况:
final Object obj = new Object();
obj.field = value;  // final 字段初始化

// JIT 可能优化为:
obj.field = value;  // 无 barrier
// 因为 obj 是新对象，不可能是跨代引用
```

### 不同 GC 的 Barrier 开销

| GC 类型 | Barrier 类型 | 开销 |
|---------|-------------|------|
| **Serial** | 简单写屏障 | 低 |
| **Parallel** | 写屏障 | 低 |
| **G1** | Card Mark + SATB | 中 |
| **ZGC** | 读屏障 | 中高 |
| **Shenandoah** | 读屏障 | 中高 |

---

## 5. 对象分配优化

### TLAB (Thread-Local Allocation Buffer)

```
TLAB 机制:
├── 每个线程私有缓冲区
├── 无锁快速分配
├── JIT 优化分配路径
└── 减少竞争
```

### JIT 生成的分配代码

```java
// Java 代码
Object obj = new Object();

// JIT 生成的汇编 (快速路径):
mov    rax, [rsi + tlab_top]     // 读取 TLAB 顶部
lea    rcx, [rax + size]         // 计算新顶部
cmp    rcx, [rsi + tlab_end]     // 检查是否有空间
ja     slow_path                 // 慢速路径
mov    [rsi + tlab_top], rcx     // 更新顶部
mov    [rax], header             // 写对象头
// 分配完成
```

### 分配优化技术

| 技术 | 说明 | 效果 |
|------|------|------|
| **标量替换** | 消除分配 | 100% 减少 |
| **TLAB** | 线程本地分配 | 无竞争 |
| **批量分配** | 数组创建优化 | 减少 barrier |
| **逃逸分析** | 栈上分配 | 无 GC |

---

## 6. 去优化与 GC

### Deoptimization 触发

```
GC 导致去优化:
├── 类型假设失效
├── 类层次结构变化
├── 方法重新定义
└── 对象布局变化
```

### 示例

```java
// 假设 JIT 优化:
List<String> list = new ArrayList<>();
list.add("item");  // 去虚拟化为直接调用

// GC 后如果类层次变化:
// (例如通过 JVMTI 重新定义类)
// → 去优化触发
// → 回到解释执行
```

### 去优化开销

| 场景 | 触发频率 | 开销 |
|------|---------|------|
| **类型转换失效** | 罕见 | 高 |
| **类层次变化** | 极罕见 | 高 |
| **方法重定义** | 开发环境 | 中 |
| **正常情况** | 几乎不 | 无 |

---

## 7. 代码缓存与 GC

### 代码缓存管理

```
代码缓存:
├── 存储编译后的本地代码
├── 内存压力时可能清理
├── GC 与代码缓存协调
└── 频繁重编译影响性能
```

### 代码缓存清理

```bash
# 代码缓存配置
-XX:ReservedCodeCacheSize=256m     # 预留大小
-XX:InitialCodeCacheSize=8m        # 初始大小
-XX:+PrintCodeCache                # 打印信息

# 代码缓存满时的行为:
# 1. 停止编译 (不推荐)
-XX:-UseCodeCacheFlushing

# 2. 清理不热代码 (推荐)
-XX:+UseCodeCacheFlushing
-XX:MinCodeCacheFlushingInterval=300  # 5 分钟
```

### GC 与代码缓存交互

```
内存压力场景:
├── 堆内存高 → GC 更频繁
├── 代码缓存大 → 总内存压力
├── GC 可能触发代码缓存清理
└── 清理后需要重新编译
```

---

## 8. 编译排队与 GC

### 编译器调度

```
编译策略:
├── 高优先级: 热方法
├── 低优先级: 冷方法
├── GC 暂停时: 降低编译优先级
└── 内存充足: 提高编译率
```

### CI (Compiler Interface) 与 GC

```java
// GC 运行时:
// 1. CI 检测到 GC 活动
// 2. 降低编译线程优先级
// 3. 减少 CPU 竞争
// 4. GC 完成后恢复正常
```

---

## 9. 实战优化

### 优化 1: 减少临时对象

```java
// 优化前: 每次循环创建对象
for (int i = 0; i < 1000; i++) {
    String result = String.format("Item %d", i);
    process(result);
}

// 优化后: 重用对象
StringBuilder sb = new StringBuilder(32);
for (int i = 0; i < 1000; i++) {
    sb.setLength(0);
    sb.append("Item ").append(i);
    process(sb.toString());
}

// GC 减少: ~80%
```

### 优化 2: 避免逃逸

```java
// 优化前: 对象逃逸
public List<Point> getPoints() {
    List<Point> points = new ArrayList<>();
    for (int i = 0; i < 1000; i++) {
        points.add(new Point(i, i * 2));  // 必须分配
    }
    return points;
}

// 优化后: 原始类型数组
public int[] getPoints() {
    int[] points = new int[2000];
    for (int i = 0; i < 1000; i++) {
        points[i * 2] = i;
        points[i * 2 + 1] = i * 2;
    }
    return points;
}

// GC 减少: ~50%
```

### 优化 3: 标量替换友好

```java
// 优化前: 复杂对象难以标量替换
class ComplexCalc {
    int a, b, c, d, e;
    // ... 很多字段
}

// 优化后: 简单结构
class Point {
    final int x, y;  // final 更易优化
}

// GC 减少: ~30%
```

---

## 10. 诊断与监控

### 检查逃逸分析

```bash
# 查看逃逸分析结果
-XX:+PrintEscapeAnalysis
-XX:+PrintEliminateAllocations

# 输出示例:
# EA: allocating scalar-replaced object Point
# EA: allocated object is not escaping
```

### 检查 Safepoint

```bash
# Safepoint 统计
-XX:+PrintSafepointStatistics
-XX:PrintSafepointStatisticsCount=100

# JFR 事件
jfr record --name=jit gc
```

### 检查 Barrier 开销

```bash
# JFR GC 事件
jfr print --events jdk.GCPhaseParallel

# 查看屏障时间
```

---

## 总结

### JIT 与 GC 协作要点

| 协作点 | JIT 责任 | GC 责任 |
|--------|---------|---------|
| **对象分配** | 优化分配路径 | 快速回收 |
| **Safepoint** | 插入安全点 | 检测点位置 |
| **Barrier** | 优化 barrier | 使用 barrier |
| **元数据** | 记录引用 | 扫描引用 |
| **去优化** | 响应变化 | 通知变化 |

### 最佳实践

```
1. 利用逃逸分析减少对象分配
2. 保持对象结构简单 (便于标量替换)
3. 使用 final 字段 (便于优化)
4. 避免频繁的跨代引用
5. 合理设置代码缓存大小
6. 监控 safepoint 开销
7. 选择合适的 GC (与 JIT 配合)
8. 避免不必要的对象创建
9. 重用对象而不是创建新对象
10. 让 JIT 做它擅长的事
```

---

## 相关链接

### 本地文档

- [逃逸分析详解](escape-analysis.md) - 逃逸分析原理
- [最佳实践](best-practices.md) - JIT 友好代码模式
- [C2 优化阶段](c2-phases.md) - PhaseEscapeAnalysis

### 外部资源

- [GC 与 JIT 协作](https://openjdk.org/groups/hotspot/docs/HotSpotGlossary.html)
- [Safepoint 机制](https://blogs.oracle.com/dave/entry/safepoints_and_the_vms)

---

**最后更新**: 2026-03-21
