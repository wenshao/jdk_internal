# 逃逸分析详解

> Java 对象分配优化的核心技术
> 栈上分配、标量替换、锁消除

[← 返回 JIT 编译](../)

---

## 一眼看懂

| 维度 | 内容 |
|------|------|
| **什么是逃逸** | 对象的作用域是否超出方法 |
| **不逃逸** | 对象只在方法内使用 |
| **逃逸分析** | 分析对象是否逃逸的编译器优化 |
| **标量替换** | 将对象字段拆分为独立变量 |
| **栈上分配** | 不逃逸对象分配在栈而非堆 |
| **锁消除** | 不逃逸对象的锁可消除 |

---

## 逃逸分析概述

### 问题的本质

```java
// 每次调用都创建新对象
public int calculate() {
    Point p = new Point(1, 2);
    return p.x + p.y;
}

// 问题:
// 1. 堆分配开销
// 2. GC 压力
// 3. 缓存不友好

// 逃逸分析优化后:
public int calculate() {
    int p_x = 1;  // 标量替换
    int p_y = 2;
    return p_x + p_y;  // 无对象分配
}
```

### 逃逸状态分类

| 逃逸状态 | 定义 | 优化潜力 |
|----------|------|----------|
| **No Escape** | 对象不逃出方法 | ✅ 标量替换、栈上分配、锁消除 |
| **Arg Escape** | 作为参数传递 | ⚠️ 部分优化 |
| **Global Escape** | 赋值给静态字段/返回 | ❌ 无法优化 |

---

## 逃逸分析算法

### 连接图 (Connection Graph)

```
逃逸分析使用连接图跟踪对象:

节点类型:
├── ObjectNode: 对象抽象节点
├── FieldNode: 对象字段
├── LocalNode: 局部变量
└── UnknownNode: 未知节点 (可能逃逸)

边类型:
├── PointsToEdge: 指向关系
└── DeferredEdge: 延迟边 (复杂分析)
```

### 分析流程

```
Phase 1: 构建连接图
    └── 为每个对象分配创建节点
    └── 为每个字段分配创建 FieldNode
    └── 添加指向关系

Phase 2: 逃逸状态分析
    └── 从方法返回点反向追踪
    └── 从静态字段写入点追踪
    └── 从方法参数传递点追踪

Phase 3: 标量替换
    └── No Escape 对象字段拆分为标量
    └── 消除对象分配

Phase 4: 锁消除
    └── No Escape 对象的同步操作可消除
```

---

## 标量替换

### 原理

```java
// 原始代码
class Point {
    int x, y;
}

public int calculate() {
    Point p = new Point();
    p.x = 1;
    p.y = 2;
    return p.x + p.y;
}

// 标量替换后 (无对象分配)
public int calculate() {
    int p$x = 1;  // p.x 的标量表示
    int p$y = 2;  // p.y 的标量表示
    return p$x + p$y;
}
```

### 标量替换条件

| 条件 | 说明 |
|------|------|
| **No Escape** | 对象不逃逸方法 |
| **无同步** | 对象无 synchronized 操作 |
| **无安全依赖** | 无 finalize/安全相关 |
| **大小合理** | 对象字段不太多 |

### 标量替换示例

```java
// 复杂对象
class Rectangle {
    int x, y, width, height;
    int area() { return width * height; }
}

public int calculate() {
    Rectangle r = new Rectangle();
    r.x = 0;
    r.y = 0;
    r.width = 10;
    r.height = 20;
    return r.area();
}

// 标量替换后
public int calculate() {
    int r$x = 0;
    int r$y = 0;
    int r$width = 10;
    int r$height = 20;
    return r$width * r$height;  // area() 被内联
}
```

### 性能影响

```
标量替换带来的优化:
├── 消除堆分配       (- 几十到几百周期)
├── 消除 GC 压力      (- GC 暂停时间)
├── 改善缓存局部性    (+ 10-20%)
└── 启用更多优化      (+ 常量折叠、死代码消除)
```

---

## 栈上分配

### 原理

```java
// 不逃逸对象可以分配在栈上
public int calculate() {
    Point p = new Point(1, 2);
    return p.x + p.y;
}

// 栈上分配伪代码
public int calculate() {
    Point p = allocate_on_stack(sizeof(Point));
    p.x = 1;
    p.y = 2;
    int result = p.x + p.y;
    // 方法返回时自动释放
    return result;
}
```

### 栈上分配 vs 堆分配

| 特性 | 栈上分配 | 堆分配 |
|------|----------|--------|
| **分配速度** | ~5 ns | ~50-500 ns |
| **释放方式** | 自动 (出栈) | GC |
| **缓存局部性** | 优秀 | 一般 |
| **碎片化** | 无 | 有 |
| **适用场景** | 短生命周期对象 | 长生命周期对象 |

### HotSpot 实现

```
HotSpot 中的栈上分配:
├── 实际上是"标量替换"
│   └── 对象字段变为局部变量
│   └── 局部变量自然在栈上
│
└── 真正的栈上分配 (Scalar Replacement 无法处理时)
    └── 不常见，主要用于特殊场景
```

---

## 锁消除

### 原理

```java
// 不逃逸对象的锁是多余的
public int calculate() {
    Point p = new Point();
    synchronized (p) {  // 锁可消除
        p.x = 1;
        p.y = 2;
    }
    return p.x + p.y;
}

// 锁消除后
public int calculate() {
    int p$x = 1;
    int p$y = 2;
    return p$x + p$y;
}
```

### 锁消除条件

| 条件 | 说明 |
|------|------|
| **No Escape** | 对象不逃逸 |
| **单线程访问** | 无其他线程可见 |
| **锁对象确定** | 编译时可知 |

### 锁消除示例

```java
// StringBuffer 的锁消除
public String concat(String a, String b) {
    StringBuffer sb = new StringBuffer();
    sb.append(a);
    sb.append(b);
    return sb.toString();
}

// 优化前: 每次 append 都加锁
// 优化后: sb 不逃逸，所有锁被消除

// 实际生成的代码类似:
public String concat(String a, String b) {
    char[] chars = new char[a.length() + b.length()];
    // 直接复制字符，无锁
    return new String(chars);
}
```

---

## C2 逃逸分析实现

### PhaseEscapeAnalysis

```
C2 编译流程中的逃逸分析:

Parse Phase
   │
   ▼
PhaseIterGVN (第一次)
   │
   ▼
PhaseIdealLoop
   │
   ▼
PhaseCCP
   │
   ▼
PhaseStringOpts
   │
   ▼
PhaseEliminateNullChecks
   │
   ▼
PhaseEscapeAnalysis ◄───────┐
   │                        │
   ├─ 连接图构建             │
   ├─ 逃逸状态计算           │
   ├─ 标量替换候选选择        │
   └─ 锁消除分析             │
   │                        │
   ▼                        │
PhaseScalarReplace ─────────┘
   │
   ▼
PhaseMacroExpand
   │
   ▼
...
```

### 源码位置

```
src/hotspot/share/opto/
├── escape.hpp/cpp          # 逃逸分析主逻辑
├── escape.cpp              # 连接图实现
├── macroArrayCopy.cpp      # 数组复制优化
└── callnode.cpp            # 方法调用节点
```

### 关键类

| 类 | 职责 |
|----|------|
| `ConnectionGraph` | 连接图管理 |
| `PointsToNode` | 指向分析节点 |
| `EscapeAnalyzer` | 逃逸分析器 |
| `ScalarReplaceNode` | 标量替换 |

---

## 逃逸分析效果

### 微基准测试

```java
// 不逃逸对象
@Benchmark
public int noEscape() {
    Point p = new Point(1, 2);
    return p.x + p.y;
}

// 逃逸对象
@Benchmark
public int escape() {
    Point p = new Point(1, 2);
    return consume(p);  // 逃逸
}

private int consume(Point p) {
    return p.x + p.y;
}
```

| 场景 | 无逃逸分析 | 有逃逸分析 | 提升 |
|------|-----------|-----------|------|
| **noEscape** | 50 ns/op | 5 ns/op | **10x** |
| **escape** | 50 ns/op | 50 ns/op | 无变化 |

### 实际应用场景

| 场景 | 逃逸分析效果 |
|------|-------------|
| **StringBuilder** | ⭐⭐⭐⭐⭐ 90%+ 情况可优化 |
| **临时对象** | ⭐⭐⭐⭐⭐ 常见模式 |
| **数学计算** | ⭐⭐⭐⭐ Point/Rectangle 等 |
| **集合临时使用** | ⭐⭐⭐ 取决于使用方式 |

---

## 逃逸分析限制

### 无法优化的情况

| 情况 | 原因 |
|------|------|
| **返回对象** | Global Escape |
| **存储到静态字段** | Global Escape |
| **传递给线程** | 可能被其他线程访问 |
| **JNI 调用** | 本地代码可能存储引用 |
| **反射访问** | 行为难以预测 |

### 部分优化的情况

```java
// Arg Escape: 作为参数传递但不被存储
public int calculate(Point p) {
    // p 可能逃逸，但需要更复杂的分析
    return process(p);
}

// 优化: 可能部分标量替换
// 如果 process() 可以内联，p 的字段可以标量化
```

---

## 编程建议

### 逃逸分析友好设计

#### 1. 使用短生命周期对象

```java
// 推荐: 不逃逸的临时对象
public int calculate() {
    int[] temp = new int[100];
    // 使用 temp
    return temp[0] + temp[1];
}
// 可以完全优化掉
```

#### 2. 避免不必要的对象逃逸

```java
// 不推荐
class Calculator {
    private Point temp = new Point();

    public int calculate(int x, int y) {
        temp.x = x;
        temp.y = y;
        return temp.x + temp.y;
    }
}

// 推荐
public int calculate(int x, int y) {
    return x + y;  // 无需对象
}
```

#### 3. 使用基本类型

```java
// 不推荐
public Integer add(Integer a, Integer b) {
    return Integer.valueOf(a.intValue() + b.intValue());
}

// 推荐
public int add(int a, int b) {
    return a + b;
}
```

---

## 诊断和调优

### 查看逃逸分析结果

```bash
# 打印逃逸分析
-XX:+PrintEscapeAnalysis

# 打印标量替换
-XX:+PrintEliminateAllocations
-XX:+DoEscapeAnalysis

# 打印锁消除
-XX:+PrintEliminateLocks
-XX:+EliminateLocks

# 禁用逃逸分析 (对比性能)
-XX:-DoEscapeAnalysis
-XX:-EliminateAllocations
-XX:-EliminateLocks
```

### 输出示例

```
# 逃逸分析日志
Escape analysis:
  Object Point@123 allocated in method calculate
  - NoEscape: true
  - ScalarReplace: true
  - Fields: x, y

# 标量替换日志
Scalar replacement:
  - Point@123 replaced with {int x, int y}
  - Allocation eliminated
```

### JFR 事件

```bash
# 记录分配事件
jcmd <pid> JFR.start name=alloc
jcmd <pid> JFR.dump name=alloc filename=alloc.jfr

# 分析
jfr print --events jdk.ObjectAllocationInNewTLAB alloc.jfr
```

---

## 相关 PR 和改进

### 直接相关的 PR 分析

| Issue | 标题 | 作者 | 说明 |
|-------|------|------|------|
| [JDK-8370405](/by-pr/8370/8370405.md) | MergeStores 在分配消除中被错误标量替换 | [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | 逃逸分析 + MergeStore 交互 bug 修复 |
| [JDK-8357690](/by-pr/8357/8357690.md) | CharacterDataLatin1 添加 @Stable 注解 | [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | 启用标量替换优化 |
| [JDK-8357913](/by-pr/8357/8357913.md) | StringCoding 添加 @Stable 注解 | [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | 启用标量替换和循环展开 |
| [JDK-8368172](/by-pr/8368/8368172.md) | DateTimePrintContext 不可变对象优化 | [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | JIT 逃逸分析优化 (+6-10%) |
| [JDK-8366224](/by-pr/8366/8366224.md) | DecimalDigits 数组优化 | [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | 逃逸分析受益 |

### 近期改进

| Issue | 标题 | 影响 |
|-------|------|------|
| JDK-8339799 | 减少 java.lang.invoke 字节码生成 | 改善逃逸分析效果 |
| JDK-8327247 | 复杂字符串拼接内存爆炸 | 限制复杂度以支持逃逸分析 |
| JDK-8356761 | IGV dump escape analysis information | 逃逸分析诊断改进 |

### 相关文档

- [MergeStore 优化](mergestore.md) - 标量替换后的优化
- [C2 优化阶段](c2-phases.md) - PhaseEscapeAnalysis 位置
- [String 构造函数优化](/by-pr/8355/8357289.md) - 方法拆分以支持内联和逃逸分析

---

## 相关链接

### 本地文档

- [C2 优化阶段](c2-phases.md) - 逃逸分析在编译流程中的位置
- [JIT 编译概览](../) - 编译器优化总览

### 外部资源

- [HotSpot Escape Analysis Status](https://cr.openjdk.org/~cslucas/escape-analysis/EscapeAnalysis.html)
- [JDConf 2024: Improving HotSpot Scalar Replacement](https://jdconf.com/2024/downloads/JDConf%20202024-Improving%20HotSpot%20Scalar%20Replacement-Soares.pdf)
- [Escape Analysis in Java](https://www.ibm.com/developerworks/java/library/j-jtp09296/)

### 贡献者

| 贡献者 | 领域 | 组织 |
|--------|------|------|
| [Vladimir Kozlov](/by-contributor/profiles/vladimir-kozlov.md) | C2 编译器架构 | Oracle |
| [John Rose](/by-contributor/profiles/john-rose.md) | invokedynamic, JIT | Oracle |
| [Tobias Hartmann](/by-contributor/profiles/tobias-hartmann.md) | JIT 编译器 | Oracle |

---

**最后更新**: 2026-03-20
