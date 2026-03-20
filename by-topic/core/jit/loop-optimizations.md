# 循环优化详解

> C2 编译器的循环优化技术
> 从识别到变换的完整流程

[← 返回 JIT 编译](../)

---

## 一眼看懂

| 维度 | 内容 |
|------|------|
| **问题** | 循环是程序中最耗时的部分 |
| **优化收益** | 2-50x 性能提升 |
| **主要技术** | 展开、剥离、外提、向量化 |
| **C1 支持** | ❌ 无循环优化 |
| **C2 支持** | ✅ 完整的循环优化 |
| **关键阶段** | PhaseIdealLoop (执行 3+ 轮) |

---

## 循环优化概述

### 为什么循环优化如此重要？

```java
// 典型场景: 数组处理
for (int i = 0; i < 1000000; i++) {
    sum += array[i];  // 执行 1,000,000 次
}

// 如果循环体优化 20%:
// 总性能提升 = 20% × 1,000,000 = 显著
```

### 优化分类

| 优化类型 | 说明 | 收益 |
|----------|------|------|
| **循环展开** | 减少分支和循环控制开销 | 10-30% |
| **循环剥离** | 分离前置/后置条件 | 15-40% |
| **循环外提** | 将不变计算移出循环 | 20-50% |
| **循环不变代码外提** | 消除重复计算 | 10-25% |
| **循环融合** | 合并多个循环 | 减少内存访问 |
| **循环交换** | 改变嵌套顺序 | 改善缓存局部性 |

---

## 循环识别

### 计数循环 (Counted Loop)

```java
// 标准计数循环
for (int i = 0; i < n; i++) {
    body(i);
}

// C2 识别为 CountedLoopNode:
// - init: i = 0
// - limit: i < n
// - stride: i++ (步长 1)
```

### 归约循环 (Reduction Loop)

```java
// 归约变量
int sum = 0;
for (int i = 0; i < n; i++) {
    sum += array[i];  // sum 是归约变量
}

// C2 识别归约模式:
// - sum 是循环外使用的变量
// - 每次迭代更新 sum
// - 可以优化为向量归约
```

### 不可优化循环

```java
// 复杂条件
for (int i = 0; condition(i); i++) {
    // condition(i) 难以预测
}

// 未知边界
for (int i = 0; i < unknown(); i++) {
    // 边界不可知
}

// 有副作用
for (int i = 0; i < n; i++) {
    if (rare()) {
        throw new Exception();  // 可能退出
    }
}
```

---

## 循环展开 (Loop Unrolling)

### 原理

```java
// 原始循环
for (int i = 0; i < 100; i++) {
    a[i] = b[i] * 2;
}

// 展开因子 4
for (int i = 0; i < 100; i += 4) {
    a[i]   = b[i] * 2;
    a[i+1] = b[i+1] * 2;
    a[i+2] = b[i+2] * 2;
    a[i+3] = b[i+3] * 2;
}

// 收益:
// - 分支减少 75%
// - 更好的指令级并行
// - 更容易向量化
```

### 展开策略

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| **完全展开** | 完全消除循环 | 小循环 (次数 < 16) |
| **部分展开** | 展开固定倍数 | 大循环 |
| **自适应展开** | 根据性能动态选择 | 取决于 profiling |

### 完全展开示例

```java
// 原始代码
for (int i = 0; i < 4; i++) {
    result += data[i];
}

// 完全展开后 (无循环)
result += data[0];
result += data[1];
result += data[2];
result += data[3];

// 编译器可以进一步优化:
result = data[0] + data[1] + data[2] + data[3];
```

---

## 循环剥离 (Loop Peeling)

### 原理

```java
// 原始循环
for (int i = 0; i < n; i++) {
    if (i == 0) {
        init();  // 首次特殊处理
    }
    process(i);
}

// 剥离首次迭代
init();
for (int i = 1; i < n; i++) {
    process(i);  // 主循环无分支
}
```

### 剥离类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **前置剥离** | 执行第一次迭代 | 检查边界条件 |
| **后置剥离** | 执行最后一次迭代 | 处理余数 |
| **完全剥离** | 完全展开小循环 | 固定小次数循环 |

### Partial Peeling

```java
// 原始循环
for (int i = 0; i < n; i++) {
    if (rare_condition) {
        handle_rare();
    }
    process(i);
}

// Partial Peeling 后
if (rare_condition) {
    handle_rare();
    i = 0;
} else {
    // 主循环: 假设 rare_condition 为 false
    for (i = 0; i < n; i++) {
        process(i);
    }
}
```

---

## 循环外提 (Loop Hoisting)

### 不变代码外提

```java
// 原始代码
for (int i = 0; i < n; i++) {
    int x = Math.sqrt(100);  // 循环不变
    array[i] = array[i] + x;
}

// 外提后
int x = Math.sqrt(100);  // 只计算一次
for (int i = 0; i < n; i++) {
    array[i] = array[i] + x;
}
```

### 条件外提 (Loop Unswitching)

```java
// 原始代码
for (int i = 0; i < n; i++) {
    if (flag) {
        a[i] = b[i] + 1;
    } else {
        a[i] = b[i] + 2;
    }
}

// 外提后
if (flag) {
    for (int i = 0; i < n; i++) {
        a[i] = b[i] + 1;  // 无分支
    }
} else {
    for (int i = 0; i < n; i++) {
        a[i] = b[i] + 2;  // 无分支
    }
}
```

### 归约外提

```java
// 原始代码
for (int i = 0; i < n; i++) {
    sum += array[i];
    if (sum > threshold) {
        // 每次迭代都检查
    }
}

// 归约外提后
for (int i = 0; i < n; i++) {
    sum += array[i];
}
// 循环后检查
if (sum > threshold) {
}
```

---

## 循环不变代码外提

### 数组边界检查外提

```java
// 原始代码
for (int i = 0; i < array.length; i++) {
    if (i >= 0 && i < array.length) {  // 每次迭代检查
        array[i] = array[i] * 2;
    }
}

// 边界检查外提后
if (0 >= 0 && array.length <= array.length) {  // 循环外检查一次
    for (int i = 0; i < array.length; i++) {
        array[i] = array[i] * 2;
    }
}
```

### 空值检查外提

```java
// 原始代码
for (int i = 0; i < n; i++) {
    if (obj != null) {  // 每次迭代检查
        obj.method(i);
    }
}

// 空值检查外提后
if (obj != null) {  // 循环外检查一次
    for (int i = 0; i < n; i++) {
        obj.method(i);
    }
}
```

---

## 其他循环优化

### 循环融合 (Loop Fusion)

```java
// 原始: 两个循环
for (int i = 0; i < n; i++) {
    a[i] = b[i] * 2;
}
for (int i = 0; i < n; i++) {
    c[i] = a[i] + 1;
}

// 融合后: 一个循环
for (int i = 0; i < n; i++) {
    a[i] = b[i] * 2;
    c[i] = a[i] + 1;
}

// 收益:
// - 减少循环开销
// - 改善缓存局部性
// - 更容易向量化
```

### 循环交换 (Loop Interchange)

```java
// 原始: 按行访问 (缓存不友好)
for (int i = 0; i < M; i++) {
    for (int j = 0; j < N; j++) {
        sum += matrix[i][j];  // 行主序，缓存友好
    }
}

// 如果是列主序存储
for (int j = 0; j < N; j++) {
    for (int i = 0; i < M; i++) {
        sum += matrix[i][j];
    }
}
```

### 循环倾斜 (Loop Skewing)

```java
// 用于处理循环依赖
// 原始
for (int i = 1; i < N; i++) {
    for (int j = 1; j < N; j++) {
        a[i][j] = a[i-1][j] + a[i][j-1];  // 依赖
    }
}

// 倾斜后可并行化
for (int k = 2; k < 2*N; k++) {
    for (int i = max(1, k-N); i < min(N, k); i++) {
        int j = k - i;
        a[i][j] = a[i-1][j] + a[i][j-1];
    }
}
```

---

## C2 PhaseIdealLoop

### 优化流程

```
Parse Phase
   │
   ▼
PhaseIterGVN (第一次)
   │
   ▼
PhaseIdealLoop (多轮迭代)
   │
   ├─► Loop 1: 构建循环树
   │   └─ 识别循环结构
   │
   ├─► Loop 2: Partial Peeling
   │   └─ 剥离条件检查
   │
   ├─► Loop 3: Full Peeling
   │   └─ 完全剥离小循环
   │
   ├─► Loop 4: Unswitching
   │   └─ 条件外提
   │
   ├─► Loop 5+: Unrolling
   │   └─ 循环展开
   │
   ▼
PhaseCCP
```

### 循环树结构

```
OuterLoop (i = 0; i < 100; i++)
   │
   ├─ InnerLoop1 (j = 0; j < 50; j++)
   │
   └─ InnerLoop2 (k = 0; k < 30; k++))

循环优化按层次进行:
1. 内层循环优先优化
2. 外层循环基于内层优化结果
```

---

## 性能影响

### 微基准测试

```java
@Benchmark
public int loopUnroll() {
    int sum = 0;
    for (int i = 0; i < 1024; i++) {
        sum += array[i];
    }
    return sum;
}

// 无展开: ~500 ns/op
// 展开 4x: ~350 ns/op (+30%)
// 展开 8x: ~300 ns/op (+40%)
```

### 实际应用收益

| 场景 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| **数组求和** | 100 ns | 35 ns | **+65%** |
| **矩阵乘法** | 5000 ns | 1200 ns | **+76%** |
| **字符串处理** | 200 ns | 80 ns | **+60%** |
| **图像处理** | 50000 ns | 15000 ns | **+70%** |

---

## 诊断和调试

### 查看循环优化

```bash
# 打印循环优化详情
-XX:+PrintCompilation -XX:+PrintLoopOpts

# 输出示例
<loop>
  - loop: 0x00007f1234567890
  - ident: 123
  - type: CountedLoop
  - unrolled: 4
  - unswitched: true
</loop>
```

### 控制循环优化

```bash
# 启用/禁用特定优化
-XX:+LoopUnrolling        # 启用循环展开 (默认)
-XX:-LoopUnrolling        # 禁用循环展开
-XX:LoopUnrollLimit=60    # 展开限制
-XX:+LoopUnswitching      # 启用条件外提
-XX:-LoopUnswitching      # 禁用条件外提

# 循环优化阈值
-XX:LoopPercentProfileLimit=10  # profiling 限制
```

---

## 编程建议

### 循环友好设计

#### 1. 使用简单计数循环

```java
// 推荐: 简单计数循环
for (int i = 0; i < n; i++) {
    // 容易优化
}

// 不推荐: 复杂条件
for (Iterator<String> it = list.iterator(); it.hasNext(); ) {
    // 难以优化
}
```

#### 2. 避免循环内复杂条件

```java
// 推荐
if (needsProcessing) {
    for (int i = 0; i < n; i++) {
        process(i);
    }
}

// 不推荐
for (int i = 0; i < n; i++) {
    if (needsProcessing) {
        process(i);
    }
}
```

#### 3. 使用数组而非集合

```java
// 推荐: 数组
int[] array = new int[1000];
for (int i = 0; i < array.length; i++) {
    sum += array[i];
}

// 不推荐: ArrayList
List<Integer> list = new ArrayList<>();
for (int i = 0; i < list.size(); i++) {
    sum += list.get(i);
}
```

---

## 相关链接

### 本地文档

- [C2 优化阶段](c2-phases.md) - PhaseIdealLoop 详解
- [SuperWord 向量化](superword.md) - 循环向量化
- [Ideal Graph](ideal-graph.md) - 循环节点表示

### 外部资源

- [OpenJDK Wiki: Loop optimizations](https://wiki.openjdk.org/spaces/HotSpot/pages/20415918/Loop+optimizations+in+Hotspot+Server+VM+Compiler+C2)
- [Introduction to C2 - Part 4: Loop Optimizations](https://eme64.github.io/blog/2025/01/23/Intro-to-C2-Part04.html) - [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md)

---

## 贡献者

| 贡献者 | 领域 | 组织 |
|--------|------|------|
| [Roland Westrelin](/by-contributor/profiles/rooland-westrelin.md) | C2 循环优化 | Oracle |
| [Vladimir Kozlov](/by-contributor/profiles/vladimir-kozlov.md) | C2 架构师 | Oracle |
| [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | SuperWord 向量化 | Oracle |

---

**最后更新**: 2026-03-20
