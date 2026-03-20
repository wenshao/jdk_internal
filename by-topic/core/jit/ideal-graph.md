# Ideal Graph 详解

> C2 编译器的中间表示 (IR)
> 从字节码到机器码的核心数据结构

[← 返回 JIT 编译](../)

---

## 一眼看懂

| 维度 | 内容 |
|------|------|
| **什么是 Ideal Graph** | C2 编译器的 SSA (静态单赋值) 形式中间表示 |
| **设计目标** | 平台无关、优化友好的图结构 |
| **节点类型** | 200+ 节点类型 (AddNode, LoadNode, IfNode 等) |
| **图变换** | 通过优化 Phase 逐步变换图结构 |
| **可视化工具** | IGV (Ideal Graph Visualizer) |
| **SSA 形式** | 每个变量只定义一次 |

---

## Ideal Graph 概述

### 为什么需要 Ideal Graph？

```
编译流程中的 IR 转换:

字节码 → Parse → Ideal Graph → 优化阶段 → MachNodes → 机器码
         (解析)  (平台无关)   (15+ Phase)  (平台相关)
```

| IR 类型 | 位置 | 特点 |
|---------|------|------|
| **字节码** | 输入 | 平台无关，高层抽象 |
| **Ideal Graph** | 中间 | 平台无关，优化友好 |
| **MachNodes** | 输出前 | 平台相关，接近机器码 |
| **机器码** | 输出 | 具体架构的机器码 |

### Ideal Graph 的特点

| 特点 | 说明 |
|------|------|
| **SSA 形式** | 每个值只定义一次，简化数据流分析 |
| **双向图** | 节点有输入和输出边 |
| **类型化** | 每个节点有明确的类型 |
| **副作用标注** | 区分纯计算和副作用操作 |
| **控制流+数据流** | 统一表示控制流和数据流 |

---

## 图结构

### 节点 (Node) 结构

```cpp
// 简化的 Node 结构
class Node {
    uint8_t _id;              // 节点 ID
    uint8_t _flags;           // 标志位
    Type* _type;              // 类型信息
    Node* _in[MAX];           // 输入边
    Node* _out[MAX];          // 输出边 (通过 _in 反向)

    // 关键操作
    virtual int Opcode();     // 操作码
    virtual const char* Name(); // 节点名称
    virtual uint hash();      // 哈希值 (用于 GVN)
    virtual uint cmp(Node*);  // 比较 (用于 GVN)
};
```

### 边类型

| 边类型 | 说明 | 示例 |
|--------|------|------|
| **输入边 (in)** | 数据依赖和控制依赖 | `AddNode` 的两个操作数 |
| **输出边 (out)** | 反向边，通过输入边维护 | 谁使用了这个节点 |
| **控制边** | 控制流依赖 | `IfNode` 的两个分支 |

### 图示例

```java
// Java 代码
public int add(int a, int b) {
    int result = a + b;
    if (result > 10) {
        return result;
    }
    return 0;
}

// Ideal Graph (简化表示)
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  StartNode                                              │
│     │                                                   │
│     ├─→ ParmNode: a                                     │
│     ├─→ ParmNode: b                                     │
│     │                                                   │
│     ▼                                                   │
│  AddNode(a, b) ────────┐                                │
│     │                  │                                │
│     ▼                  │                                │
│  CmpINode(>10)         │                                │
│     │                  │                                │
│     ▼                  │                                │
│  BoolNode (true/false) │                                │
│     │                  │                                │
│     ├────┬─────────────┘                                │
│     │    │                                              │
│     ▼    ▼                                              │
│  IfNode                                                 │
│   │    │                                                │
│   │    └─→ [False] → ReturnNode(0)                     │
│   │                                                     │
│   └─→ [True] → ReturnNode(result)                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 核心节点类型

### 数据节点

| 节点 | 操作 | 示例 |
|------|------|------|
| **Conv2BNode** | int → byte 转换 | `(byte)x` |
| **ConvI2LNode** | int → long 转换 | `(long)x` |
| **AddINode** | 整数加法 | `a + b` |
| **SubINode** | 整数减法 | `a - b` |
| **MulINode** | 整数乘法 | `a * b` |
| **DivINode** | 整数除法 | `a / b` |
| **AndINode** | 按位与 | `a & b` |
| **OrINode** | 按位或 | `a \| b` |
| **XorINode** | 按位异或 | `a ^ b` |
| **LShiftINode** | 左移 | `a << b` |
| **RShiftINode** | 右移 | `a >> b` |

### 控制流节点

| 节点 | 操作 | 示例 |
|------|------|------|
| **IfNode** | 条件分支 | `if (condition)` |
| **RegionNode** | 多路合并 | 多个前驱的合并点 |
| **LoopNode** | 循环头 | `for/while` 循环 |
| **CountedLoopNode** | 计数循环 | 标准的 `for (i=0;i<n;i++)` |
| **StartNode** | 方法入口 | 方法开始 |
| **ReturnNode** | 方法返回 | `return value` |

### 内存节点

| 节点 | 操作 | 示例 |
|------|------|------|
| **LoadNode** | 内存加载 | 读取字段/数组 |
| **StoreNode** | 内存存储 | 写入字段/数组 |
| **AllocateNode** | 对象分配 | `new Object()` |
| **ProjNode** | 投影节点 | 提取元组的特定部分 |
| **LoadKlassNode** | 加载类指针 | 读取对象类型 |
| **LoadRangeNode** | 加载数组长度 | `array.length` |

### 类型节点

| 节点 | 操作 | 说明 |
|------|------|------|
| **CheckCastPPNode** | 类型检查 | `(Type)obj` |
| **InstanceOfNode** | instanceof 检查 | `obj instanceof Type` |
| **GetClassNode** | 获取类对象 | `obj.getClass()` |

### Phi 节点 (SSA)

```java
// Java 代码
int x;
if (condition) {
    x = 1;
} else {
    x = 2;
}
return x;

// Ideal Graph 中的 Phi 节点
RegionNode     // 控制流合并点
   ├─ True branch
   └─ False branch

PhiNode(RegionNode)  // 数据流合并
   ├─ Value from True branch (1)
   └─ Value from False branch (2)
```

---

## 图变换过程

### Phase 对图的影响

```
初始 Ideal Graph
   │
   ▼
Parse Phase                    ──► 构建基础图
   │
   ▼
PhaseIterGVN (第一次)          ──► GVN 优化，消除冗余
   │
   ▼
PhaseIdealLoop                 ──► 循环优化，插入循环节点
   │
   ▼
PhaseCCP                       ──► 条件常量传播
   │
   ▼
PhaseEscapeAnalysis            ──► 标量替换，添加 Phi
   │
   ▼
PhaseIterGVN (最终)            ──► 最终优化
   │
   ▼
PhaseVector                    ──► 向量化节点
   │
   ▼
Matcher                        ──► Ideal → MachNodes
```

### GVN 变换示例

```java
// 原始代码
public int calculate(int x, int y) {
    int a = x + y;
    int b = x + y;  // 冗余计算
    return a + b;
}

// GVN 优化前
AddNode(x, y) ──► a
AddNode(x, y) ──► b  // 冗余节点
AddNode(a, b)

// GVN 优化后
AddNode(x, y) ──► a
a ────────────► b  // 复用 a
AddNode(a, a)  // 2 * a
```

---

## IGV (Ideal Graph Visualizer)

### 启动 IGV

```bash
# 1. 生成编译日志
java -XX:+UnlockDiagnosticVMOptions \
     -XX:+PrintIdealGraphFile \
     -XX:PrintIdealGraphFile=ideal_graph_ \
     MyApp

# 2. 启动 IGV
# 下载: https://github.com/JetBrains/jdk8u_hotspot/tree/master/ideaproject/IdealGraphVisualizer
# 或使用: bin/igv.sh (在 JDK 渠道版本中)

# 3. 打开生成的 .xml 文件
```

### IGV 界面

| 面板 | 功能 |
|------|------|
| **Graph 视图** | 可视化 Ideal Graph |
| **控制流图** | CFG 视图 |
| **字节码视图** | 对应字节码 |
| **节点属性** | 查看节点详细信息 |
| **时间轴** | 查看每个 Phase 后的图变化 |

### IGV 使用技巧

```
常用操作:
1. 双击节点: 查看详细信息
2. Ctrl + 滚轮: 缩放
3. 拖拽: 移动视图
4. 搜索: Ctrl+F 查找节点类型
5. 颜色编码: 不同节点类型有不同颜色

节点颜色含义:
- 蓝色: 控制流节点
- 绿色: 算术运算
- 橙色: 内存操作
- 红色: 特殊节点
```

---

## Ideal Graph 优化示例

### 常量折叠

```java
// 原始代码
public int calculate() {
    return 2 + 3;
}

// Ideal Graph 优化前
ConI(2)
ConI(3)
  │
  └─→ AddINode
        └─→ ReturnNode

// GVN 优化后
ConI(5)                      // 常量折叠
  └─→ ReturnNode
```

### 死代码消除

```java
// 原始代码
public int calculate(boolean flag) {
    if (flag) {
        return 1;
    } else {
        return 2;
    }
}

// 当 flag = true 时优化后
ConI(1)
  └─→ ReturnNode        // 整个 if 结构被消除
```

### 循环优化

```java
// 原始代码
public int sum(int[] arr) {
    int sum = 0;
    for (int i = 0; i < arr.length; i++) {
        sum += arr[i];
    }
    return sum;
}

// 循环优化后的 Ideal Graph
CountedLoopNode               // 计数循环节点
   ├─ Init: ConI(0)
   ├─ Limit: LoadRange(arr)
   ├─ Stride: ConI(1)
   └─ Body:
        ├─ LoadNode(arr[i])
        └─ PhiNode(sum)       // 归约变量的 Phi
```

### 标量替换

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

// 逃逸分析 + 标量替换后
AllocateNode 被消除
p.x → ConI(1)  // 直接使用常量
p.y → ConI(2)
return → AddINode(ConI(1), ConI(2)) → ConI(3)
```

---

## 节点哈希和比较

### GVN 中的节点相等性

```cpp
// 节点哈希 (简化)
uint Node::hash() {
    uint h = Opcode();
    for (uint i = 0; i < req(); i++) {
        h = h * 31 + _in[i]->_id;
    }
    return h;
}

// 节点比较 (简化)
bool Node::cmp(Node* n) {
    if (Opcode() != n->Opcode()) return false;
    if (req() != n->req()) return false;
    for (uint i = 0; i < req(); i++) {
        if (_in[i] != n->_in[i]) return false;
    }
    return true;
}
```

### Type IGVN (Iterative GVN)

```
工作队列处理:
1. 初始化: 所有节点加入工作列表
2. 迭代:
   a. 取出节点 n
   b. 检查 n 是否已有等价节点 m
   c. 如果有，用 m 替换 n
   d. 更新 n 的所有使用者
   e. 如果图有变化，继续迭代
3. 收敛: 当工作列表为空时停止
```

---

## 常见 Ideal Graph 模式

### 模式 1: 冗余加载消除

```java
// 原始代码
public int process(Object obj) {
    int x = obj.field;  // 第一次加载
    int y = obj.field;  // 冗余加载
    return x + y;
}

// 优化后
LoadNode(obj.field) ──► x
x ────────────────────► y  // 复用第一次加载
AddINode(x, x)
```

### 模式 2: 循环不变代码外提

```java
// 原始代码
public int calculate(int[] arr, int factor) {
    int sum = 0;
    for (int i = 0; i < arr.length; i++) {
        sum += arr[i] * factor;  // factor 是循环不变
    }
    return sum;
}

// 循环外提后
LoadNode(factor) ──► 循环外
    │
    ▼
CountedLoopNode
    └─ MulINode(arr[i], factor_outside)
```

### 模式 3: 公共子表达式消除

```java
// 原始代码
public int calculate(int x, int y) {
    int a = (x + y) * 2;
    int b = (x + y) + 1;
    return a + b;
}

// 优化后
AddINode(x, y) ──► temp
MulINode(temp, 2) ──► a
AddINode(temp, 1) ──► b
```

---

## 调试和诊断

### 打印 Ideal Graph

```bash
# 打印每个 Phase 后的图
-XX:+PrintIdeal
-XX:+PrintIdealPhase

# 打印到文件
-XX:+PrintIdealGraphFile
-XX:PrintIdealGraphFile=ideal_graph_

# 打印特定方法
-XX:CompileCommand=print,*MyClass.myMethod
```

### IGV 远程连接

```bash
# 启动 JVM 时启用 IGV 连接
-XX:+PrintIdealGraphLevel
-XX:PrintIdealGraphFile=ideal_graph_
-Djdk.internal.module.BootLayer=ALL-UNNAMED

# 在 IGV 中选择 "Connect to JVM"
```

---

## 相关链接

### 本地文档

- [C2 优化阶段](c2-phases.md) - Ideal Graph 在各阶段的变换
- [诊断工具](diagnostics.md) - IGV 使用指南
- [GVN 优化](../) - 全局值编号详解

### 外部资源

- [Ideal Graph Visualizer](https://github.com/JetBrains/jdk8u_hotspot/tree/master/ideaproject/IdealGraphVisualizer)
- [SSA Form](https://en.wikipedia.org/wiki/Static_single_assignment_form)
- [Introduction to C2 - Part 2: GVN](https://eme64.github.io/blog/2024/12/24/Intro-to-C2-Part02.html) - [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) 的深入分析

### 贡献者

| 贡献者 | 领域 | 组织 |
|--------|------|------|
| [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | C2 SuperWord 向量化、C2 博客作者 | Oracle |
| [Johannes Graham](/by-contributor/profiles/johannes-graham.md) | C2 编译器优化、常量折叠 | Oracle |
| [Vladimir Kozlov](/by-contributor/profiles/vladimir-kozlov.md) | C2 编译器创始人 | Oracle |
| [Christian Hagedorn](/by-contributor/profiles/christian-hagedorn.md) | C2 优化、GVN | Oracle |

---

**最后更新**: 2026-03-20
