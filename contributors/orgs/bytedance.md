# 字节跳动

> RISC-V 向量指令支持

---
## 目录

1. [概览](#1-概览)
2. [贡献者](#2-贡献者)
3. [贡献时间线](#3-贡献时间线)
4. [影响的模块](#4-影响的模块)
5. [关键贡献](#5-关键贡献)
6. [技术特点](#6-技术特点)
7. [数据来源](#7-数据来源)
8. [相关链接](#8-相关链接)

---


## 1. 概览

字节跳动参与 OpenJDK 开发，专注于 RISC-V 架构的向量指令支持和性能优化。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 25 |
| **贡献者数** | 1 |
| **活跃时间** | 2025 - 至今 |
| **主要领域** | RISC-V 向量指令 |

---

## 2. 贡献者

| 贡献者 | GitHub | PRs | 角色 | 主要领域 |
|--------|--------|-----|------|----------|
| [Anjian Wen](../../by-contributor/profiles/anjian-wen.md) | [@Anjian-Wen](https://github.com/Anjian-Wen) | 25 | Author | RISC-V 向量指令 |

---

## 3. 贡献时间线

```
2025: █████████████████████████████████████████████████████████████████░ 24 PRs
2026: ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1 PR
```

> **总计**: 25 PRs (2025-2026)

---

## 4. 影响的模块

| 目录 | 修改次数 | 说明 |
|------|----------|------|
| RISC-V 移植 | 23 | RISC-V 架构代码 |
| 向量 API 测试 | 2 | Vector API 测试 |
| IR 框架测试 | 2 | 编译器 IR 测试 |

---

## 5. 关键贡献

### RISC-V 向量指令 (Zvbb)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8329887 | RISC-V: C2 支持 Zvbb Vector And-Not 指令 | 向量 And-Not 指令 |
| 8355074 | RISC-V: C2 支持向量标量版 Zvbb Vector And-Not | 向量标量版本 |

**Zvbb 指令集**: Vector Bit-manipulation used in Cryptography

### RISC-V 浮点指令 (Zfa)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8349632 | RISC-V: 添加 Zfa fminm/fmaxm | 浮点最小/最大指令 |
| 8352022 | RISC-V: 支持 Zfa fminm_h/fmaxm_h | float16 支持 |

**Zfa 指令集**: Additional Floating-Point instructions

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

---

## 6. 技术特点

### RISC-V 专注

字节跳动的贡献完全聚焦于 RISC-V：
- 向量指令支持
- 浮点指令支持
- 内存操作优化

### 支持的 RISC-V 扩展

| 扩展 | 说明 |
|------|------|
| **Zvbb** | 向量位操作 (密码学相关) |
| **Zfa** | 附加浮点指令 |
| **V** | 向量扩展 |

---

## 7. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:Anjian-Wen type:pr label:integrated`
- **统计时间**: 2026-03-19

---

## 8. 相关链接

- [RISC-V International](https://riscv.org/)
- [RISC-V 指令集规范](https://github.com/riscv/riscv-isa-manual)
- [OpenJDK RISC-V Port (JEP 422)](https://openjdk.org/jeps/422)

[→ 返回组织索引](../../by-contributor/index.md)