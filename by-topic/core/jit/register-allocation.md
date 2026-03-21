# 寄存器分配详解

> 从线性扫描到图着色：JIT 编译器的寄存器分配算法
> C1 和 C2 的不同策略

[← 返回 JIT 编译](../)

---
## 目录

1. [一眼看懂](#1-一眼看懂)
2. [为什么需要寄存器分配？](#2-为什么需要寄存器分配)
3. [活跃分析](#3-活跃分析)
4. [线性扫描算法 (C1)](#4-线性扫描算法-c1)
5. [图着色算法 (C2)](#5-图着色算法-c2)
6. [C1 vs C2 寄存器分配对比](#6-c1-vs-c2-寄存器分配对比)
7. [寄存器分配与代码生成](#7-寄存器分配与代码生成)
8. [平台特定考虑](#8-平台特定考虑)
9. [诊断和调优](#9-诊断和调优)
10. [实际案例](#10-实际案例)
11. [相关链接](#11-相关链接)

---


## 1. 一眼看懂

| 维度 | 内容 |
|------|------|
| **问题** | 无限的临时变量 vs 有限的寄存器 |
| **C1 算法** | 线性扫描 - 快速但次优 |
| **C2 算法** | 图着色 (Chaitin-Briggs) - 慢但接近最优 |
| **溢出** | 临时变量存储到栈上 |
| **Spilling** | 寄存器不足时的溢出策略 |
| **寄存器压力** | 同时活跃的变量数量 |

---

## 2. 为什么需要寄存器分配？

### 问题定义

```
代码:
    int a = x + y;  // 需要存储 a
    int b = a * 2;  // 需要存储 a, b
    int c = b - 1;  // 需要存储 b, c
    return c;

问题:
    - a, b, c 放在哪里？
    - 寄存器数量有限 (x86-64: 16 个通用寄存器)
    - 选择不当可能导致频繁的内存访问
```

### 寄存器 vs 内存

| 特性 | 寄存器 | 内存 (栈) |
|------|--------|----------|
| **访问速度** | ~1 周期 | ~100-200 周期 |
| **延迟** | 0 | 3-10 周期 |
| **容量** | 极小 (16-32) | 大 (GB 级) |
| **指令** | 直接操作 | 需要 load/store |

---

## 3. 活跃分析

### 活跃区间

```java
// 示例代码
public int calculate(int x, int y) {
    int a = x + 1;    // 行 2: a 定义
    int b = y * 2;    // 行 3: b 定义
    int c = a + b;    // 行 4: c 定义, a 最后使用
    int d = b - c;    // 行 5: d 定义, b 最后使用
    return d;         // 行 6: c, d 最后使用
}

// 活跃区间分析
// 变量 | 定义点 | 最后使用 | 活跃区间
//   x   |  行 1  |   行 2   |  [1, 3)
//   y   |  行 1  |   行 3   |  [1, 4)
//   a   |  行 2  |   行 4   |  [2, 5)
//   b   |  行 3  |   行 5   |  [3, 6)
//   c   |  行 4  |   行 6   |  [4, 7)
//   d   |  行 5  |   行 6   |  [5, 7)
```

### 活跃区间图示

```
时间线: 1    2    3    4    5    6    7
         │    │    │    │    │    │    │
x: ──────┼────┼────┼────┼────┼────┼────
              ┌────┘
y: ──────┼────┼────┼────┼────┼────┼────
                   ┌────┴────┐
a:       ─────┼────┼────┼────┼────┼────┼────
                        ┌────┴────┐
b:             ─────┼────┼────┼────┼────┼────┼────
                              ┌────┴────┐
c:                   ─────┼────┼────┼────┼────┼────┼────
                                   ┌────┘
d:                         ─────┼────┼────┼────┼────┼────┼────
                              │    │    │    │    │    │    │

最大活跃数: 3 (在时间 3-5 之间)
```

---

## 4. 线性扫描算法 (C1)

### 算法原理

```
1. 计算每个值的活跃区间 [start, end)
2. 按起点排序所有值
3. 维护活跃值集合 (按 end 排序)
4. 线性扫描:
   a. 移除已过期的值
   b. 尝试分配可用寄存器
   c. 无可用寄存器时:
      - 溢出最晚使用的活跃值
      - 分配其寄存器给当前值
```

### 算法示例

```java
// 代码
public int calculate() {
    int a = 1;     // 活跃: [0, 4)
    int b = 2;     // 活跃: [1, 5)
    int c = 3;     // 活跃: [2, 3)
    int d = a + b; // 活跃: [3, 6)
    int e = b + d; // 活跃: [4, 7)
    return e;
}

// 假设只有 3 个寄存器: r0, r1, r2
```

```
时间线扫描:

t=0: a 定义
    活跃: {}
    分配: a → r0
    活跃: {a:[0,4)}

t=1: b 定义
    活跃: {a:[0,4)}
    分配: b → r1
    活跃: {a:[0,4), b:[1,5)}

t=2: c 定义
    活跃: {a:[0,4), b:[1,5)}
    分配: c → r2
    活跃: {a:[0,4), b:[1,5), c:[2,3)}

t=3: d 定义, c 过期
    活跃: {a:[0,4), b:[1,5), c:[2,3)}
    移除: c (已过期)
    活跃: {a:[0,4), b:[1,5)}
    分配: d → r2 (复用 c 的寄存器)
    活跃: {a:[0,4), b:[1,5), d:[3,6)}

t=4: e 定义, a 过期
    活跃: {a:[0,4), b:[1,5), d:[3,6)}
    移除: a (已过期)
    活跃: {b:[1,5), d:[3,6)}
    分配: e → r0 (复用 a 的寄存器)
    活跃: {b:[1,5), d:[3,6), e:[4,7)}

最终分配:
    a → r0  [0, 4)
    b → r1  [1, 5)
    c → r2  [2, 3)
    d → r2  [3, 6)
    e → r0  [4, 7)
```

### 线性扫描复杂度

| 阶段 | 时间复杂度 |
|------|-----------|
| **活跃分析** | O(n) |
| **排序** | O(n log n) |
| **扫描分配** | O(n log n) |
| **总计** | O(n log n) |

### 线性扫描优缺点

| 优点 | 缺点 |
|------|------|
| 实现简单 | 分配质量一般 |
| 速度快 | 容易产生不必要的溢出 |
| 适合快速编译 | 不考虑全局优化 |

---

## 5. 图着色算法 (C2)

### 算法原理 (Chaitin-Briggs)

```
1. 构建干涉图 (Interference Graph)
   - 节点: 每个值
   - 边: 两个值同时活跃 (不能共享寄存器)

2. 简化 (Simplification)
   - 移除度数 < K 的节点 (K = 寄存器数量)
   - 将节点压栈

3. 溢出 (Spilling)
   - 如果剩余节点度数 ≥ K
   - 选择溢出代价最小的节点
   - 标记为溢出到栈

4. 选择 (Select)
   - 从栈中弹出节点
   - 尝试分配寄存器
   - 已溢出的节点分配栈位置

5. 重启 (Restart)
   - 如果有溢出，重新计算活跃区间
   - 重复步骤 1-4
```

### 干涉图示例

```java
// 代码
public int calculate() {
    int a = 1;     // 活跃: [0, 4)
    int b = 2;     // 活跃: [1, 5)
    int c = a + b; // 活跃: [2, 3)
    int d = b + c; // 活跃: [3, 4)
    return d;
}
```

```
干涉图:

    a ─────┬──── b
           │
           │
    c ─────┴──── d

边 (同时活跃):
    (a, b): 时间 [1, 4) 重叠
    (a, c): 时间 [2, 4) 重叠
    (b, c): 时间 [2, 3) 重叠
    (b, d): 时间 [3, 4) 重叠
    (c, d): 时间 [3, 4) 重叠

度数:
    a: 2 (连接 b, c)
    b: 3 (连接 a, c, d)
    c: 3 (连接 a, b, d)
    d: 2 (连接 b, c)
```

### 图着色示例

```
假设 K = 2 (只有 2 个寄存器)

简化阶段:
    度数: a:2, b:3, c:3, d:2
    移除度数 < 2 的节点? 无

溢出阶段:
    需要溢出一个节点
    计算溢出代价:
        a: (4-0) / 2 = 2
        b: (5-1) / 3 = 1.33
        c: (3-2) / 3 = 0.33 ← 最小, 溢出 c
        d: (4-3) / 2 = 0.5

    溢出 c, 移除 c 及其边

简化阶段 (第 2 轮):
    度数: a:1, b:1, d:1
    移除 a (度数 < 2)
    移除 b (度数 < 2)
    移除 d (度数 < 2)

选择阶段:
    弹出 d → r0
    弹出 b → r1
    弹出 a → r0 (与 d 不冲突)
    c 溢出到栈

最终分配:
    a → r0
    b → r1
    c → [stack]
    d → r0
```

### 溢出代价计算

```
代价 = (区间长度) × (使用频率) / (度数)

区间长度: end - start
使用频率: 循环中的使用次数
度数: 干涉图中的连接数
```

### 图着色复杂度

| 阶段 | 时间复杂度 |
|------|-----------|
| **干涉图构建** | O(n²) |
| **简化** | O(n²) |
| **选择** | O(n) |
| **重启** | 最多 2-3 轮 |
| **总计** | O(n²) |

### 图着色优缺点

| 优点 | 缺点 |
|------|------|
| 接近最优分配 | 实现复杂 |
| 全局优化 | 编译时间长 |
| 更少的溢出 | 需要多轮迭代 |

---

## 6. C1 vs C2 寄存器分配对比

### 算法对比

| 维度 | C1 (线性扫描) | C2 (图着色) |
|------|--------------|------------|
| **算法** | Linear Scan | Chaitin-Briggs |
| **时间复杂度** | O(n log n) | O(n²) |
| **分配质量** | 中等 | 优秀 |
| **溢出次数** | 较多 | 较少 |
| **编译时间** | 快 | 慢 |
| **适用场景** | 快速编译 | 最优性能 |

### 性能对比

```
示例: 大量临时变量的函数

线性扫描分配:
    r0, r1, r2 被使用
    t3 → [spill]
    t4 → [spill]
    t5 → [spill]
    额外的 load/store 指令

图着色分配:
    r0-r15 全部利用
    更少的溢出
    更少的内存访问
```

### 寄存器利用率

| 场景 | 线性扫描 | 图着色 |
|------|----------|--------|
| **简单函数** | 80-90% | 85-95% |
| **复杂函数** | 50-70% | 70-90% |
| **循环密集** | 40-60% | 60-80% |

---

## 7. 寄存器分配与代码生成

### 分配后的指令选择

```java
// Java 代码
public int add(int a, int b) {
    return a + b;
}

// 线性扫描后 (x86-64)
// 假设 a → rdi, b → rsi

mov eax, edi    // a → eax
add eax, esi    // eax += b
ret             // return eax

// 对应汇编
0x00: mov eax, edi
0x02: add eax, esi
0x04: ret
```

### 溢出代码示例

```java
// Java 代码
public int calculate(int a, int b, int c, int d, int e) {
    return (a + b) + (c + d) + e;
}

// 寄存器不足时的分配
// r0 = a, r1 = b, r2 = c, [rsp+8] = d, [rsp+16] = e

mov eax, [rdi]     // load a
add eax, [rsi]     // add b
mov [rsp-8], eax   // spill (a+b)

mov eax, [rdx]     // load c
add eax, [rsp+8]   // add d (load from stack)
add eax, [rsp-8]   // add (a+b) (load from stack)
add eax, [rsp+16]  // add e (load from stack)
ret
```

---

## 8. 平台特定考虑

### x86-64

| 特性 | 说明 |
|------|------|
| **通用寄存器** | 16 个 (RAX, RBX, RCX, RDX, RSI, RDI, R8-R15) |
| **调用约定** | 参数: RDI, RSI, RDX, RCX, R8, R9 |
| ** callee 保存** | RBX, RBP, R12-R15 |
| ** caller 保存** | RAX, RCX, RDX, RSI, RDI, R8-R11 |

### AArch64

| 特性 | 说明 |
|------|------|
| **通用寄存器** | 31 个 (X0-X30) |
| **调用约定** | 参数: X0-X7 |
| ** callee 保存** | X19-X29 |
| ** caller 保存** | X0-X18 |

### RISC-V

| 特性 | 说明 |
|------|------|
| **通用寄存器** | 31 个 (x0-x30, x0 固定为 0) |
| **调用约定** | 参数: x10-x17 |
| ** callee 保存** | x8, x9, x18-x27 |
| ** caller 保存** | x1, x5-x7, x10-x17 |

---

## 9. 诊断和调优

### 查看寄存器分配

```bash
# 打印汇编输出
-XX:+PrintAssembly
-XX:CompileCommand=print,*MyClass.myMethod

# 需要 hsdis 库
# 下载: https://github.com/AdoptOpenJDK/jdk11-openjdk-source-code/blob/master/src/utils/hsdis/

# 输出示例
{method} 'add/II' in 'MyClass'
# parm 0:    rdi:rdi   = int
# parm 1:    rsi:rsi   = int
#           [sp+0x20]  (sp of caller)
0x0000000001f4c000: mov    eax, edi
0x0000000001f4c002: add    eax, esi
0x0000000001f4c004: vpxor  xmm0,xmm0,xmm0
0x0000000001f4c008: ret
```

### 寄存器分配统计

```bash
# JFR 事件
jcmd <pid> JFR.start name=jit
jcmd <pid> JFR.dump name=jit filename=jit.jfr

# 分析寄存器分配事件
jfr print --events jdk.CPUInformation jit.jfr
```

### 调优参数

```bash
# 寄存器分配相关
-XX:+PrintRegisterAllocation              # 打印分配信息
-XX:ReservedCodeCacheSize=256m            # 代码缓存大小
-XX:CompileThreshold=10000                # 编译阈值

# 诊断
-XX:+PrintCompilation                     # 编译日志
-XX:+LogCompilation                       # 详细日志
```

---

## 10. 实际案例

### 案例 1: 过多局部变量

```java
// 不推荐: 大量同时活跃的变量
public int calculate() {
    int a = 1, b = 2, c = 3, d = 4, e = 5;
    int f = 6, g = 7, h = 8, i = 9, j = 10;
    // ... 20 个变量同时活跃
    return a + b + c + d + e + f + g + h + i + j;
}

// 推荐: 复用变量
public int calculate() {
    int sum = 0;
    sum += 1;
    sum += 2;
    sum += 3;
    // ...
    return sum;
}
```

### 案例 2: 循环中的变量

```java
// 不推荐: 每次循环创建新变量
for (int i = 0; i < n; i++) {
    int temp1 = array1[i];
    int temp2 = array2[i];
    int temp3 = array3[i];
    // 3 个变量在循环中始终活跃
}

// 推荐: 减少活跃变量
for (int i = 0; i < n; i++) {
    process(array1[i], array2[i], array3[i]);
    // 变量在调用后不再活跃
}
```

---

## 11. 相关链接

### 本地文档

- [C1 编译器](c1-compiler.md) - 线性扫描实现
- [C2 优化阶段](c2-phases.md) - PhaseChaitin
- [诊断工具](diagnostics.md) - 查看汇编输出

### 外部资源

- [Chaitin's Register Allocation Algorithm](https://en.wikipedia.org/wiki/Register_allocation#Chaitin.27s_algorithm)
- [Linear Scan Register Allocation](https://dl.acm.org/doi/10.1145/330249.330250) - Poletto & Sarkar
- [SSA-based Register Allocation](https://www.cs.ucla.edu/~palsberg/course/cs132/lectures/ssa-based-regalloc.pdf)

### 贡献者

| 贡献者 | 领域 | 组织 |
|--------|------|------|
| [Vladimir Kozlov](/by-contributor/profiles/vladimir-kozlov.md) | C2 编译器架构 | Oracle |
| [Roland Westrelin](/by-contributor/profiles/rooland-westrelin.md) | C2 优化 | Red Hat |
| [John Rose](/by-contributor/profiles/john-rose.md) | JIT 编译器 | Oracle |

---

**最后更新**: 2026-03-20
