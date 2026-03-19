# hotspot-c2 模块分析

> C2 编译器，HotSpot 的服务端即时编译器

---

## 1. 概述

C2 (Server Compiler) 是 HotSpot VM 的高级即时编译器，专注于生成高度优化的机器码。它是 Java 应用生产环境性能的关键。

### 编译器对比

| 特性 | C1 (Client) | C2 (Server) |
|------|-------------|-------------|
| 编译速度 | 快 | 慢 |
| 优化程度 | 中 | 高 |
| 代码大小 | 小 | 大 |
| 启动时间 | 快 | 慢 |
| 峰值性能 | 中 | 高 |
| JDK 26 状态 | ✓ | ✓ |

### 分层编译策略

```
Level 0: 解释执行
    ↓ (调用次数 > 1000)
Level 1: C1 编译 (简单优化)
    ↓ (调用次数 > 5000)
Level 2: C1 编译 (带 profiling)
    ↓ (调用次数 > 10000 或 profiling 数据充足)
Level 3: C2 编译 (完全优化)
```

---

## 2. 源码结构

**目录**: `src/hotspot/share/compiler/` 和 `src/hotspot/cpu/*/`

```
compiler/
├── c2/
│   ├── compiler.cpp          # C2 编译器主入口
│   ├── compile.cpp           # 编译任务
│   ├── compileLog.cpp        # 编译日志
│   ├── escape.cpp            # 逃逸分析
│   ├── ideal.cpp             # Ideal 图节点
│   ├── loopnode.cpp          # 循环优化
│   ├── machnode.cpp          # 机器相关节点
│   ├── matcher.cpp           # 指令匹配
│   ├── node.cpp              # 节点基类
│   ├── output.cpp            # 代码生成
│   ├── phase.cpp             # 优化阶段基类
│   ├── regalloc.cpp          # 寄存器分配
│   └── stringopts.cpp        # 字符串优化
├── abstractCompiler.hpp      # 编译器抽象
├── compilationPolicy.cpp     # 编译策略
└── compileBroker.cpp         # 编译调度
```

---

## 3. 编译流程

### 3.1 总体流程

```
字节码
    ↓
解析 (Parse)
    ↓
构建 Ideal 图
    ↓
优化阶段 (Optimization Phases)
    ├─ 全局值编号 (GVN)
    ├─ 逃逸分析 (Escape Analysis)
    ├─ 循环优化 (Loop Optimization)
    ├─ 内联 (Inlining)
    ├─ 常量折叠 (Constant Folding)
    ├─ 死代码消除 (DCE)
    └─ ...
    ↓
匹配到机器指令 (Matcher)
    ↓
寄存器分配 (Register Allocation)
    ↓
代码生成 (Code Generation)
    ↓
机器码 (Native Code)
```

### 3.2 关键源码

**入口**: `src/hotspot/share/compiler/c2/compiler.cpp`

```cpp
void Compiler::compile() {
    // 1. 解析字节码
    Parse parse;

    // 2. 构建 Ideal 图
    PhaseGVN gvn;

    // 3. 优化
    PhaseIdealLoop ideal_loop;
    PhaseEscapeAnalysis escape;

    // 4. 匹配机器指令
    PhaseCFG cfg;
    Matcher matcher;

    // 5. 寄存器分配
    PhaseChaitin chaitin;

    // 6. 代码生成
    PhaseOutput output;
}
```

---

## 4. 中间表示 (IR)

### 4.1 Ideal 图

**源码**: `src/hotspot/share/compiler/c2/node.cpp`

C2 使用图结构的中间表示，称为 Ideal 图。

**节点类型**:

```cpp
// 节点基类
class Node {
 private:
  Node* _in[Max];     // 输入边
  Node* _out[Max];    // 输出边
  uint _cnt;          // 输入数量
};

// 常见节点类型
class ConNode : public Node {        // 常量
class TypeNode : public Node {        // 类型节点
class PhiNode : public Node {         // Phi 函数 (SSA)
class IfNode : public Node {          // 条件分支
class LoopNode : public Node {        // 循环头
class CallNode : public Node {        // 方法调用
class AddNode : public Node {         // 加法
class LoadNode : public Node {        // 内存加载
class StoreNode : public Node {       // 内存存储
```

### 4.2 SSA 形式

```java
// 原始代码
int x = a + b;
if (condition) {
    x = x + 1;
}
return x;

// SSA 形式 (C2 内部)
int x1 = a + b;
if (condition) {
    x2 = x1 + 1;
} else {
    x2 = x1;
}
int x3 = Phi(x2, condition);
return x3;
```

---

## 5. 关键优化

### 5.1 逃逸分析

**源码**: `src/hotspot/share/compiler/c2/escape.cpp`

**目的**: 判断对象是否逃逸出方法/线程

```cpp
class ConnectionGraph {
    // 分析对象逃逸状态
    void analyze_escape_state();
};

enum EscapeState {
    NoEscape,        // 不逃逸 → 可标量替换
    ArgEscape,       // 参数逃逸 → 可去除锁
    GlobalEscape     // 全局逃逸 → 堆分配
};
```

**优化效果**:
- **标量替换**: 对象字段拆分为局部变量
- **栈上分配**: 不逃逸对象分配在栈上
- **锁消除**: 不逃逸对象无需同步

### 5.2 循环优化

**源码**: `src/hotspot/share/compiler/c2/loopnode.cpp`

```cpp
class PhaseIdealLoop {
    // 循环不变代码外提
    void hoist_invariant();

    // 循环展开
    void do_unroll();

    // 向量化
    void do_vectorization();
};
```

### 5.3 内联

**源码**: `src/hotspot/share/compiler/c2/compile.cpp`

```cpp
// 内联策略
bool InlineTree::is_not_reached() {
    // 热点方法优先内联
    // 小方法优先内联
    // 非虚方法优先内联
}

// 内联阈值
-XX:MaxInlineSize=35        // 默认最大内联字节码大小
-XX:FreqInlineSize=325       // 频繁调用的方法
```

### 5.4 全局值编号 (GVN)

**源码**: `src/hotspot/share/compiler/c2/phaseX.cpp`

```cpp
class PhaseGVN {
    // 消除冗余计算
    Node* transform(Node* node) {
        // 查找已存在的相同节点
        Node* existing = find_existing(node);
        if (existing != NULL) {
            return existing;  // 复用已有节点
        }
        return node;
    }
};
```

---

## 6. 代码生成

### 6.1 指令匹配

**源码**: `src/hotspot/share/compiler/c2/matcher.cpp`

```cpp
class Matcher {
    // 将 Ideal 节点匹配到机器指令
    MachNode* match(Node* node) {
        // 为每个节点选择合适的机器指令
        // x86: ADD -> ADD_rm_r32
        // ARM: ADD -> ADD_rr
    }
};
```

### 6.2 寄存器分配

**源码**: `src/hotspot/share/compiler/c2/regalloc.cpp`

```cpp
class PhaseChaitin {
    // 图着色寄存器分配
    void Register_Allocate() {
        // 1. 构建干扰图
        // 2. 图着色
        // 3. 溢出处理
    }
};
```

### 6.3 平台相关代码

**目录**: `src/hotspot/cpu/*/`

| 架构 | 目录 |
|------|------|
| x86 | `src/hotspot/cpu/x86/` |
| ARM | `src/hotspot/cpu/arm/` |
| AArch64 | `src/hotspot/cpu/aarch64/` |
| RISC-V | `src/hotspot/cpu/riscv/` |
| s390 | `src/hotspot/cpu/s390/` |

```cpp
// x86 代码生成示例 (src/hotspot/cpu/x86/assembler_x86.cpp)
void Assembler::addl(Register dst, int32_t imm32) {
    // emit: 01 /r     ADD r/m32, r32
    //       or: 81 /0 id ADD r/m32, imm32
    emit_int8(0x81);
    emit_int8(0xC0 | dst.encoding());
    emit_int32(imm32);
}
```

---

## 7. JDK 26 变更

### 7.1 性能改进

- **Vector API 集成**: 更好的 SIMD 向量化支持
- **字符串优化**: 改进字符串操作的内联和优化
- **模式匹配**: 支持模式匹配的编译优化

### 7.2 新增优化

```cpp
// JDK 26 新增/改进的优化
- Record 类优化
- Switch 表达式优化
- Sealed 类优化
- 虚拟线程友好优化
```

### 7.3 编译日志增强

```bash
# 查看编译日志
java -XX:+UnlockDiagnosticVMOptions \
     -XX:+LogCompilation \
     -XX:LogFile=compilation.log \
     -jar app.jar

# 查看编译后的汇编
java -XX:+UnlockDiagnosticVMOptions \
     -XX:+PrintAssembly \
     -jar app.jar
```

---

## 8. 调优选项

### 8.1 编译阈值

```bash
# 调整分层编译阈值
-XX:Tier0InvokeNotifyFreqLog=7     # Level 0 → 1
-XX:Tier3InvokeNotifyFreqLog=10    # Level 2 → 3 (C2)

# 禁用分层编译 (不推荐)
-XX:-TieredCompilation
```

### 8.2 内联控制

```bash
# 内联大小限制
-XX:MaxInlineSize=35               # 最大内联字节码大小
-XX:FreqInlineSize=325             # 频繁调用方法
-XX:MaxTrivialSize=6               # 无条件内联

# 内联深度
-XX:MaxInlineLevel=9               # 最大内联深度
```

### 8.3 优化控制

```bash
# 启用/禁用特定优化
-XX:+EliminateAllocations          # 逃逸分析
-XX:+LoopUnswitching               # 循环开关
-XX:+UseVectorizedMismatchedIntrinsic  # 向量化不匹配比较

# 循环优化
-XX:LoopUnrollLimit=60             # 循环展开限制
-XX:LoopPercentProfileLimit=10     # 循环 profiling 限制
```

---

## 9. 性能分析

### 9.1 编译日志分析

使用 JITWatch 分析编译日志:

```bash
# 1. 生成编译日志
java -XX:+UnlockDiagnosticVMOptions -XX:+LogCompilation -jar app.jar

# 2. 使用 JITWatch 打开
java -jar jitwatch.jar hotspot.log
```

### 9.2 查看热点方法

```java
// 使用 JMX 获取编译信息
CompilationMXBean compiler = ManagementFactory.getCompilationMXBean();
System.out.println("Compilation time: " + compiler.getTotalCompilationTime());

// 使用 HotSpotMXBean
com.sun.management.HotSpotDiagnosticMXBean diag =
    ManagementFactory.newPlatformMXBeanProxy(
        mbs,
        "com.sun.management:type=HotSpotDiagnostic",
        com.sun.management.HotSpotDiagnosticMXBean.class
    );
```

---

## 10. 相关链接

- [HotSpot 编译器接口文档](https://openjdk.org/groups/hotspot/docs/CompilerInterface.html)
- [GraalVM (替代 C2)](https://www.graalvm.org/)
- [JMH 基准测试](https://openjdk.org/projects/code-tools/jmh/)
- [源码](https://github.com/openjdk/jdk/tree/master/src/hotspot/share/compiler/c2)
