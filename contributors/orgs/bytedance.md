# 字节跳动

> RISC-V 向量指令支持

---

## 概览

字节跳动参与 OpenJDK 开发，专注于 RISC-V 架构的向量指令支持和性能优化。

| 指标 | 值 |
|------|-----|
| **总 Commits** | 12 |
| **贡献者数** | 1 |
| **主要领域** | RISC-V 向量指令 |

---

## 影响的模块分布

基于 git 修改文件统计：

| 模块 | 文件数 | 说明 |
|------|--------|------|
| RISC-V 移植 | 23 | RISC-V 架构代码 |
| RISC-V GC 共享 | 1 | GC 共享代码 |
| 向量 API 测试 | 2 | Vector API 测试 |
| IR 框架测试 | 2 | 编译器 IR 测试 |

---

## 贡献者

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| [Anjian Wen](../anjian-wen.md) | 12 | RISC-V 向量指令 |

---

## 关键贡献

### RISC-V 向量指令 (Zvbb)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8329887 | RISC-V: C2 支持 Zvbb Vector And-Not 指令 | 向量 And-Not 指令 |
| 8355074 | RISC-V: C2 支持向量标量版 Zvbb Vector And-Not | 向量标量版本 |

**Zvbb 指令集**:
- Vector Bit-manipulation used in Cryptography
- 包含向量 And-Not (vandn) 指令
- 用于密码学和位操作优化

### RISC-V 浮点指令 (Zfa)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8349632 | RISC-V: 添加 Zfa fminm/fmaxm | 浮点最小/最大指令 |
| 8352022 | RISC-V: 支持 Zfa fminm_h/fmaxm_h | float16 支持 |

**Zfa 指令集**:
- Additional Floating-Point instructions
- 包含 fminm/fmaxm 指令
- 不设置异常标志的最小/最大操作

### RISC-V 内存操作

| Issue | 标题 | 说明 |
|-------|------|------|
| 8351140 | RISC-V: Intrinsify Unsafe::setMemory | 内存填充 intrinsic |

### RISC-V 数组填充优化

| Issue | 标题 | 说明 |
|-------|------|------|
| 8356593 | RISC-V: 数组填充 stub 小改进 | 性能优化 |
| 8356700 | RISC-V: fill_words/zero_memory 声明不可压缩范围 | 正确性 |
| 8356869 | RISC-V: 改进数组填充 stub 尾部处理 | 性能优化 |

### RISC-V 编译器输出改进

| Issue | 标题 | 说明 |
|-------|------|------|
| 8355562 | RISC-V: 清理向量标量指令名称 | 代码清理 |
| 8355657 | RISC-V: 改进向量标量指令 PrintOptoAssembly 输出 | 调试支持 |
| 8355796 | RISC-V: 修复 AllBitsSetVectorMatchRuleTest 测试 | 测试修复 |
| 8354815 | RISC-V: 改变位旋转移位类型 | 正确性修复 |

---

## 技术特点

### RISC-V 专注

字节跳动的贡献完全聚焦于 RISC-V：
- 向量指令支持
- 浮点指令支持
- 内存操作优化

### 指令集扩展

支持的 RISC-V 扩展：
- **Zvbb**: 向量位操作 (密码学相关)
- **Zfa**: 附加浮点指令
- **V**: 向量扩展

### 性能优化

- 数组填充优化
- 内存操作 intrinsic
- 向量化支持

---

## RISC-V 背景

RISC-V 是开源指令集架构，字节跳动在以下方面有贡献：

| 领域 | 贡献 |
|------|------|
| 向量计算 | Zvbb 指令支持 |
| 浮点运算 | Zfa 指令支持 |
| 内存操作 | setMemory intrinsic |
| 编译器 | C2 后端优化 |

---

## 数据来源

- **统计方法**: `git log upstream_master --author="bytedance"`
- **模块分析**: 基于修改文件路径统计
- **贡献者**: Anjian Wen

---

## 相关链接

- [RISC-V International](https://riscv.org/)
- [RISC-V 指令集规范](https://github.com/riscv/riscv-isa-manual)
- [OpenJDK RISC-V Port (JEP 422)](https://openjdk.org/jeps/422)