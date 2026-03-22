# C2 编译器优化概览

> JIT 编译器优化的核心技术和实现

---
## 目录

1. [优化分类](#1-优化分类)
2. [优化级别](#2-优化级别)
3. [相关资源](#3-相关资源)

---


## 1. 优化分类

### 1. 方法内联 (Inlining)

将方法调用替换为方法体本身，消除调用开销。

**详细文档**: [inlining.md](./inlining.md)

**关键优化**:
- 虚方法内联
- 多态调用优化
- 内联深度控制

### 2. 逃逸分析 (Escape Analysis)

分析对象是否逃逸出方法或线程，支持标量替换和栈上分配。

**详细文档**: [escape-analysis.md](./escape-analysis.md)

**关键优化**:
- 标量替换
- 栈上分配
- 锁消除

### 3. 循环优化 (Loop Optimizations)

针对循环结构的各种优化技术。

**详细文档**: [loop-optimizations.md](./loop-optimizations.md)

**关键优化**:
- 循环展开
- 循环不变量外提
- 循环向量化 (SuperWord)

### 4. 向量化优化 (SuperWord)

利用 SIMD 指令并行处理数据。

**详细文档**: [superword.md](./superword.md)

**关键优化**:
- 数据依赖分析
- 向量指令生成
- 循环向量化

### 5. 全局优化

跨方法的全局优化技术。

**相关文档**:
- [ideal-graph.md](./ideal-graph.md) - 理想图表示
- [c2-phases.md](./c2-phases.md) - C2 编译阶段

---

## 2. 优化级别

| 级别 | 编译器 | 特点 |
|------|--------|------|
| 0 | 解释器 | 无优化 |
| 1-3 | C1 | 快速编译，基本优化 |
| 4 | C2 | 深度优化，激进优化 |

**详细文档**: [tiered-compilation.md](./tiered-compilation.md)

---

## 3. 相关资源

- [JIT 索引](./README.md) - JIT 编译器完整文档
- [C2 编译阶段](./c2-phases.md) - C2 编译流程
- [IGV 教程](./igv-tutorial.md) - 理想图可视化工具