# C1 编译器详解

> Client Compiler - 快速编译、平衡优化的 JIT 编译器
> 分层编译的基石，为 C2 提供 profiling 数据

[← 返回 JIT 编译](../)

---

## 一眼看懂

| 维度 | 内容 |
|------|------|
| **设计目标** | 快速编译 > 代码质量 |
| **编译速度** | < 100ms (vs C2: 1-5 秒) |
| **代码质量** | 中等 (解释器 2-5x, C2 的 50-70%) |
| **IR 类型** | HIR (High-level IR) + LIR (Low-level IR) |
| **寄存器分配** | 线性扫描算法 |
| **主要优化** | 内联、常量折叠、局部值编号 |
| **适用场景** | 桌面应用、短时运行、快速启动 |

---

## C1 在分层编译中的角色

### 编译层级

```
Level 0: 解释器
   │  启动快，性能低 (~5-50x slower than C2)
   │  收集基础 profiling 信息
   ▼
Level 1: C1 (纯解释 profiling)
   │  快速编译，低优化
   │  收集 profiling 数据
   ▼
Level 2: C1 (有限 profiling)
   │  中等优化
   │  继续收集 profiling
   ▼
Level 3: C1 (完全 profiling)
   │  激进 profiling 收集
   │  为 C2 准备数据
   ▼
Level 4: C2 (深度优化)
   │  基于 C1 profiling 的深度优化
   ▼
峰值性能
```

### C1 的职责

| 职责 | 说明 |
|------|------|
| **快速启动** | 应用启动后立即提供优化的代码 |
| **Profiling 收集** | 为 C2 收集类型、分支、调用频率信息 |
| **中等性能** | 提供比解释器好 2-5 倍的性能 |
| **编译队列缓冲** | 减少 C2 的编译压力 |

---

## C1 编译流程

### 完整流程图

```
字节码
   │
   ▼
┌─────────────────────────────────────────┐
│ Phase 1: GraphBuilder                   │
│   构建 HIR (High-level Intermediate IR) │
│   - 字节码 → HIR 节点                    │
│   - 基础内联优化                        │
│   - 局部优化                            │
└─────────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────────┐
│ Phase 2: Canonicalizer                  │
│   HIR 规范化                            │
│   - 表达式简化                          │
│   - 常量折叠                            │
│   - 死代码消除                          │
└─────────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────────┐
│ Phase 3: ValueNumbering                 │
│   局部值编号                            │
│   - 冗余消除                            │
│   - 公共子表达式消除                    │
└─────────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────────┐
│ Phase 4: Optimizer                      │
│   C1 优化器                             │
│   - 块内联                              │
│   - 常量传播                            │
│   - 空值检查消除                        │
└─────────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────────┐
│ Phase 5: LIR Generator                  │
│   HIR → LIR 转换                        │
│   - 指令选择                            │
│   - 寄存器需求分析                      │
└─────────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────────┐
│ Phase 6: LinearScan                     │
│   寄存器分配 (线性扫描)                 │
│   - 快速分配算法                        │
│   - 最小化 spilling                     │
└─────────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────────┐
│ Phase 7: CodeGenerator                  │
│   代码生成                              │
│   - LIR → 机器码                        │
│   - 生成 nmethod                        │
└─────────────────────────────────────────┘
   │
   ▼
本地代码
```

---

## HIR (High-level IR)

### HIR 节点类型

C1 使用类型化的 HIR 表示：

| 节点类型 | 说明 | 示例 |
|----------|------|------|
| **Instruction** | 所有指令的基类 | - |
| **Constant** | 常量值 | `IntConstant: 42` |
| **LoadField** | 字段加载 | `LoadField: obj.field` |
| **StoreField** | 字段存储 | `StoreField: obj.field = value` |
| **ArrayLoad** | 数组元素加载 | `ArrayLoad: array[i]` |
| **ArrayStore** | 数组元素存储 | `ArrayStore: array[i] = value` |
| **ArithmeticOp** | 算术运算 | `Add: a + b` |
| **LogicOp** | 逻辑运算 | `And: a & b` |
| **CompareOp** | 比较运算 | `If: a < b` |
| **If** | 条件分支 | `if (condition) {...}` |
| **Goto** | 无条件跳转 | `goto label` |
| **Return** | 返回指令 | `return value` |
| **Call** | 方法调用 | `call method` |
| **BlockBegin** | 基本块开始 | - |
| **BlockEnd** | 基本块结束 | - |

### HIR 示例

```java
// Java 代码
public int add(int a, int b) {
    int result = a + b;
    return result;
}

// C1 HIR 表示 (简化)
BlockBegin:
    b1: (HIR)

    // 参数加载
    i1:  LoadParam: a (int)
    i2:  LoadParam: b (int)

    // 算术运算
    i3:  ArithmeticOp: Add(i1, i2) → result

    // 返回
    i4:  Return: i3

BlockEnd:
```

---

## LIR (Low-level IR)

### LIR 指令类型

LIR 更接近机器码，包含具体的操作：

| 指令类型 | 说明 | 示例 |
|----------|------|------|
| **li_op1** | 单操作数指令 | `neg r0` |
| **li_op2** | 双操作数指令 | `add r0, r1` |
| **li_add** | 加法 | `add r0, r1, r2` |
| **li_sub** | 减法 | `sub r0, r1, r2` |
| **li_mul** | 乘法 | `mul r0, r1, r2` |
| **li_div** | 除法 | `div r0, r1, r2` |
| **li_move** | 数据移动 | `move r0, r1` |
| **li_load** | 内存加载 | `load [r0 + 8], r1` |
| **li_store** | 内存存储 | `store r0, [r1 + 8]` |
| **li_branch** | 分支指令 | `branch eq, r0, label` |
| **li_cmp** | 比较指令 | `cmp r0, r1` |
| **li_call** | 方法调用 | `call method` |
| **li_return** | 返回 | `return r0` |

### LIR 示例

```java
// Java 代码
public int add(int a, int b) {
    return a + b;
}

// C1 LIR 表示 (x86-64, 简化)
# 参数位置
r0 := [rsp + 8]    # load a
r1 := [rsp + 16]   # load b

# 加法
r2 := add r0, r1

# 返回
return r2

# 对应汇编
mov eax, [rsp + 8]
add eax, [rsp + 16]
ret
```

---

## 寄存器分配：线性扫描算法

### 算法原理

C1 使用线性扫描算法进行寄存器分配，相比 C2 的图着色算法更快但质量略低。

```
线性扫描流程:
1. 计算每个值的活跃区间 [start, end)
2. 按起点排序
3. 线性扫描，分配可用寄存器
4. 无可用寄存器时，溢出到栈
```

### 活跃区间

```java
// Java 代码
public int calculate(int x, int y) {
    int a = x + 1;    // 活跃: [0, 3)
    int b = y * 2;    // 活跃: [1, 3)
    int c = a - b;    // 活跃: [2, 3)
    return c;         // 使用 c
}

// 活跃区间分析
// a: [0, 3) - 从定义到 c 计算
// b: [1, 3) - 从定义到 c 计算
// c: [2, 3) - 从定义到返回
```

### 线性扫描分配

```
时间线: 0    1    2    3
         │    │    │    │
a: ──────┼────┼────┼────
              ┌────┘
b:       ─────┼────┼────
              ┌────┘
c:            ─────┼────
         │    │    │    │
寄存器:  r0   r1   r0

0-1: a → r0
1-2: b → r1 (r0 被占用)
2-3: c → r0 (a 已过期，可复用)
```

### 线性扫描 vs 图着色

| 维度 | 线性扫描 (C1) | 图着色 (C2) |
|------|--------------|------------|
| **时间复杂度** | O(n log n) | O(n²) 或更高 |
| **分配质量** | 中等 | 优秀 |
| **实现复杂度** | 简单 | 复杂 |
| **溢出处理** | 贪心策略 | 全局优化 |
| **适用场景** | 快速编译 | 最优分配 |

---

## C1 优化详解

### 1. 内联优化

| 特性 | C1 |
|------|----|
| **内联阈值** | 35 字节 |
| **最大深度** | 2-3 层 |
| **虚方法内联** | 保守，需要类型统计 |
| **失败处理** | 放弃内联 |

```java
// C1 内联示例
public int process(int x) {
    return add(x, 1);  // 如果 add 方法 < 35 字节，可能内联
}

private static int add(int a, int b) {
    return a + b;  // 6 字节，容易被内联
}
```

### 2. 常量折叠

```java
// 优化前
public int calculate() {
    int a = 2 + 3;
    int b = a * 4;
    return b;
}

// C1 常量折叠后
public int calculate() {
    return 20;  // 直接返回常量
}
```

### 3. 死代码消除

```java
// 优化前
public int calculate(int x) {
    int a = x * 2;
    if (false) {  // 永假条件
        a = a + 100;
    }
    return a;
}

// C1 死代码消除后
public int calculate(int x) {
    return x * 2;
}
```

### 4. 局部值编号

```java
// 优化前
public int calculate(int x, int y) {
    int a = x + y;
    int b = x + y;  // 重复计算
    return a + b;
}

// C1 值编号后
public int calculate(int x, int y) {
    int a = x + y;
    int b = a;      // 复用 a
    return a + b;
}
```

### 5. 空值检查消除

```java
// 优化前
public int getValue(Object obj) {
    if (obj != null) {
        return obj.hashCode();
    }
    return 0;
}

// C1 优化后 (使用隐式空检查)
public int getValue(Object obj) {
    // 在访问对象字段时触发硬件异常
    return obj != null ? obj.hashCode() : 0;
}
```

---

## C1 的限制

### 不支持的优化

| 优化 | C1 | C2 |
|------|----|----|
| **循环展开** | ❌ | ✅ |
| **循环剥离** | ❌ | ✅ |
| **循环外提** | ❌ | ✅ |
| **逃逸分析** | ❌ | ✅ |
| **标量替换** | ❌ | ✅ |
| **向量化** | ❌ | ✅ |
| **全局值编号** | ❌ | ✅ |
| **激进内联** | ❌ | ✅ |

### 性能差距

| 场景 | C1 vs C2 性能比 |
|------|----------------|
| **简单计算** | 70-80% |
| **小循环** | 50-70% |
| **大循环** | 30-50% |
| **对象密集** | 40-60% |
| **虚方法调用** | 60-80% |

---

## C1 源码结构

### 关键文件

```
src/hotspot/share/c1/
├── c1_Compilation.hpp/cpp           # C1 编译入口
├── c1_GraphBuilder.hpp/cpp          # HIR 构建器
├── c1_Optimizer.hpp/cpp             # C1 优化器
├── c1_Canonicalizer.hpp/cpp         # 规范化
├── c1_ValueMap.hpp/cpp              # 值编号
├── c1_ValueSet.hpp/cpp              # 值集合
├── c1_IR.hpp                        # HIR 定义
├── c1_Instruction.hpp               # 指令定义
├── c1_LIR.hpp                       # LIR 定义
├── c1_LIRGenerator.hpp/cpp          # LIR 生成器
├── c1_LinearScan.hpp/cpp            # 寄存器分配
├── c1_CodeGenerator.hpp/cpp         # 代码生成
├── c1_FpuStackSim.hpp/cpp           # FPU 栈模拟
├── c1_FrameMap.hpp/cpp              # 栈帧布局
├── c1_MacroAssembler.hpp/cpp        # 宏汇编器
└── c1_RInfo.hpp/cpp                 # 寄存器信息
```

### 关键类

| 类 | 职责 |
|----|------|
| `Compilation` | C1 编译上下文 |
| `GraphBuilder` | 字节码 → HIR |
| `IR` | HIR 表示 |
| `Instruction` | HIR 节点基类 |
| `LIRGenerator` | HIR → LIR |
| `LinearScan` | 寄存器分配 |
| `CodeGenerator` | LIR → 机器码 |

---

## C1 vs C2 对比总结

### 编译阶段对比

| 阶段 | C1 | C2 |
|------|----|----|
| **IR 构建** | GraphBuilder (单遍) | Parse (多遍，内联) |
| **优化** | Optimizer (基础) | 多个 Phase (激进) |
| **值编号** | ValueNumbering (局部) | GVN (全局) |
| **寄存器分配** | LinearScan (快速) | Chaitin (图着色) |
| **代码生成** | LIR → 机器码 | MachNodes → 机器码 |
| **总阶段数** | ~7 | 15+ |

### 适用场景

| 场景 | 推荐编译器 | 原因 |
|------|------------|------|
| **GUI 应用** | C1 | 快速响应用户操作 |
| **批处理任务** | C2 | 长时间运行，最大化吞吐量 |
| **微服务** | C1 → C2 | 快速启动 + 高性能 |
| **大数据处理** | C2 | 计算密集型 |
| **桌面应用** | C1 | 交互式应用 |
| **服务器应用** | C2 | 7x24 长期运行 |

---

## 诊断和调优

### 查看 C1 编译活动

```bash
# 查看编译日志
java -XX:+PrintCompilation -XX:+UnlockDiagnosticVMOptions \
     -XX:+PrintCompilation -XX:CompileThreshold=100 MyApp

# 输出示例
     71   10       3       java.util.String::charAt (26 bytes)
              ^   ^       ^
              │   │       └─ 编译层级 (3 = C1)
              │   └─ 编译 ID
              └─ 方法序号
```

### C1 特定参数

```bash
# C1 编译阈值
-XX:CompileThreshold=1000              # 默认 1500 (C2), C1 更低
-XX:Tier0InvokeNotifyFreqLog=7         # Level 0 频率
-XX:Tier0BackedgeNotifyFreqLog=10      # Level 0 回边频率
-XX:Tier3InvokeNotifyFreqLog=10        # Level 3 频率
-XX:Tier3BackedgeNotifyFreqLog=13      # Level 3 回边频率

# C1 优化控制
-XX:FreqInlineSize=325                 # 热方法内联阈值
-XX:MaxInlineSize=35                   # 最大内联大小

# 分层编译控制
-XX:+TieredCompilation                 # 启用分层编译 (默认)
-XX:-TieredCompilation                 # 禁用分层编译
-XX:TieredStopAtLevel=1                # 只使用 C1
```

---

## 相关链接

### 本地文档

- [JIT 编译概览](../) - C1 在分层编译中的角色
- [C2 优化阶段](c2-phases.md) - C2 的深度优化
- [寄存器分配](register-allocation.md) - 线性扫描 vs 图着色
- [内联优化](inlining.md) - C1 内联策略

### 外部资源

- [HotSpot Wiki: C1 Compiler](https://wiki.openjdk.org/display/HotSpot/Client+Compiler)
- [C1 Source Code](https://github.com/openjdk/jdk/tree/master/src/hotspot/share/c1)

### 贡献者

| 贡献者 | 领域 | 链接 |
|--------|------|------|
| [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | C1/C2 编译器 | Oracle |
| [Vladimir Kozlov](/by-contributor/profiles/vladimir-kozlov.md) | C2 架构师 | Oracle |
| [Tobias Hartmann](/by-contributor/profiles/tobias-hartmann.md) | JIT 编译器 | Oracle |

---

**最后更新**: 2026-03-20
