# 字节跳动

> RISC-V 向量指令支持

[← 返回组织索引](../../by-contributor/README.md)

---
## 目录

1. [概览](#1-概览)
2. [贡献者](#2-贡献者)
3. [多层网络分析](#3-多层网络分析)
4. [贡献时间线](#4-贡献时间线)
5. [影响的模块](#5-影响的模块)
6. [关键贡献](#6-关键贡献)
7. [技术特点](#7-技术特点)
8. [数据来源](#8-数据来源)
9. [相关链接](#9-相关链接)

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
---

## 3. 多层网络分析

### 3.1 协作网络 (Co-authorship Network)

基于字节跳动 RISC-V 贡献的协作关系分析：

```
                          字节跳动协作网络图
                          
                    ┌─────────────────────────────┐
                    │      ByteDance (字节跳动)     │
                    │   RISC-V Vector Instructions │
                    └─────────────┬───────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
          ▼                       ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │ 核心团队  │           │ 技术协作圈 │           │ 审查协作圈 │
    │  (内部)   │           │  (外部)   │           │  (外部)   │
    └────┬─────┘           └────┬─────┘           └────┬─────┘
         │                      │                      │
    ┌────┴────┐           ┌────┴────┐           ┌────┴────┐
    │Anjian   │           │Fei      │           │Andrew   │
    │Wen      │           │Yang     │           │Haley    │
    │(25)     │           │(RISC-V) │           │(RISC-V) │
    │         │           │         │           │         │
    │         │           │Shaojin  │           │         │
    │         │           │Wen      │           │         │
    │         │           │(Alibaba)│           │         │
    └─────────┘           └─────────┘           └─────────┘
```

#### 核心团队 (字节跳动内部)

| 贡献者 | 组织 | PRs | 主要领域 | 角色 |
|--------|------|-----|----------|------|
| [Anjian Wen](../../by-contributor/profiles/anjian-wen.md) | ByteDance | 25 | RISC-V 向量指令 | Author |

#### 技术协作圈 (外部合作)

| 贡献者 | 组织 | 合作领域 | 关系类型 |
|--------|------|----------|----------|
| [Fei Yang](../../by-contributor/profiles/fei-yang.md) | Huawei | RISC-V | 技术同行 |
| [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | Alibaba | 性能优化 | 技术同行 |
| [Andrew Haley](../../by-contributor/profiles/andrew-haley.md) | Red Hat | RISC-V | 审查者 |

### 3.2 技术影响力网络

```
                    字节跳动技术影响力辐射图
                    
                         RISC-V 支持
                              │
                    ┌─────────┼─────────┐
                    │         │         │
                    ▼         ▼         ▼
               向量指令   浮点指令   内存操作
                    │         │         │
                    └─────────┼─────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
              Zvbb 指令集         Zfa 指令集
              (向量位操作)        (附加浮点)
                    │                   │
                    └─────────┬─────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
                    ▼         ▼         ▼
                密码学    数组填充   内存填充
                相关优化   stub 优化   intrinsic
```

#### 技术影响力指标

| 领域 | 直接影响 | 间接影响 | 影响范围 |
|------|----------|----------|----------|
| **RISC-V 向量指令** | 25 PRs | RISC-V 服务器用户 | 性能优化 |
| **Zvbb 指令集** | 2 PRs | 密码学应用 | 向量位操作 |
| **Zfa 指令集** | 2 PRs | 科学计算 | 浮点运算 |
| **内存操作优化** | 4 PRs | 所有 RISC-V 应用 | 性能提升 |

### 3.3 组织关系网络

```
                    字节跳动组织关系图
                    
                    ┌──────────────────┐
                    │   ByteDance      │
                    │   (字节跳动)      │
                    │   Beijing, CN    │
                    └────────┬─────────┘
                             │ RISC-V 团队
                    ┌────────┴─────────┐
                    │                  │
                    ▼                  ▼
            ┌──────────────┐   ┌──────────────┐
            │  RISC-V      │   │  其他方向    │
            │  向量指令    │   │  (未参与)    │
            └──────┬───────┘   └──────────────┘
                   │
              ┌────┴────┐
              │         │
              ▼         ▼
         Anjian    其他成员
         Wen       (未参与)
         (主导)
```

### 3.4 协作深度分析

#### RISC-V 向量指令支持协作网络

这是 Anjian Wen 主导的 RISC-V 向量指令支持项目：

```
        RISC-V 向量指令协作网络
        
              Anjian Wen
              (Author)
                   │
              ┌────┴────┐
              │         │
              ▼         ▼
        Fei Yang   Andrew Haley
        (Huawei)      (Red Hat)
        (技术同行)  (审查者)
              │
              └────┬────┘
                   │
                   ▼
         JDK 26 (正式版)
```

| 指标 | 数值 | 说明 |
|------|------|------|
| 开发周期 | 2025-2026 | 从提案到正式发布 |
| PR 数量 | 25 个 | RISC-V 向量指令 |
| 审查轮次 | 多轮 | 包含公开审查 |
| 影响范围 | RISC-V 用户 | JDK 26+ |

#### 与 Fei Yang 的协作

| 指标 | 数值 | 说明 |
|------|------|------|
| 合作领域 | RISC-V | 向量指令支持 |
| Fei 角色 | Huawei RISC-V 专家 | 技术同行 |
| Anjian 角色 | ByteDance RISC-V 开发者 | 向量指令实现 |
| 协作模式 | 技术同行交流 | 跨公司协作 |

**Fei Yang 背景**:
- Huawei RISC-V 专家
- OpenJDK Committer
- GitHub: [@RealFeiYang](https://github.com/RealFeiYang)
- 100+ integrated PRs

#### 与 Andrew Haley 的协作

| 指标 | 数值 | 说明 |
|------|------|------|
| 合作领域 | RISC-V | 向量指令审查 |
| Andrew 角色 | Red Hat Reviewer | RISC-V 审查者 |
| Anjian 角色 | Author | 向量指令实现 |
| 协作模式 | 审查指导 | Red Hat → ByteDance |

**Andrew Haley 背景**:
- Red Hat Principal Software Engineer
- OpenJDK Committer
- RISC-V 端口主要贡献者
- GitHub: [@aph](https://github.com/aph)

### 3.5 技术社区参与

字节跳动积极参与技术社区活动：

- **RISC-V 支持**: RISC-V 向量指令主要实现者
- **邮件列表**: 在 riscv-port-dev、compiler-dev 邮件列表活跃
- **开源贡献**: 25 个 integrated PRs

### 3.6 知识传承网络

```
                    字节跳动知识传承

        前辈层                    同辈层                    后辈层
    ┌─────────────┐          ┌─────────────┐          ┌─────────────┐
    │ Andrew      │          │ Fei Yang    │          │ 新贡献者    │
    │ Haley       │◄────────►│ (Huawei)       │          │ (通过 PR    │
    │ (Red Hat)   │  审查    │             │──交流──►│  学习)      │
    └─────────────┘          └─────────────┘          └──────┬──────┘
                                                              │
                                                              │
                                                              ▼
                    ┌─────────────────────────────────────────────────┐
                    │         Anjian Wen                               │
                    │         (知识枢纽)                               │
                    │         - RISC-V                                │
                    │         - Vector Instructions                   │
                    │         - Zvbb/Zfa                              │
                    └─────────────────────────────────────────────────┘
                                                              │
                    ┌─────────────┐          ┌─────────────┐  │
                    │ 其他字节    │          │ 新贡献者    │  │
                    │ 跳动成员    │◄────────►│             │◄─┘
                    │             │  协作    │             │   指导
                    └─────────────┘          └─────────────┘
```

---


## 4. 贡献时间线

```
2025: █████████████████████████████████████████████████████████████████░ 24 PRs
2026: ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1 PR
```

> **总计**: 25 PRs (2025-2026)

---

## 5. 影响的模块

| 目录 | 修改次数 | 说明 |
|------|----------|------|
| RISC-V 移植 | 23 | RISC-V 架构代码 |
| 向量 API 测试 | 2 | Vector API 测试 |
| IR 框架测试 | 2 | 编译器 IR 测试 |

---

## 6. 关键贡献

### RISC-V 密码学 Intrinsics (AES/GHASH)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8371968 | RISC-V: implement AES CBC intrinsics | AES CBC 模式加解密 |
| 8365732 | RISC-V: implement AES CTR intrinsics | AES CTR 模式加解密 |
| 8373069 | RISC-V: implement GHASH intrinsic | GHASH 认证哈希 |
| 8374351 | RISC-V: Small refactoring for crypto macro-assembler routines | 密码学汇编重构 |

### RISC-V 向量指令 (Zvbb)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8329887 | RISC-V: C2 支持 Zvbb Vector And-Not 指令 | 向量 And-Not 指令 |
| 8355074 | RISC-V: C2 支持向量标量版 Zvbb Vector And-Not | 向量标量版本 |
| 8355657 | RISC-V: Improve PrintOptoAssembly output of vector-scalar instructions | 向量标量输出改进 |
| 8355562 | RISC-V: Cleanup names of vector-scalar instructions | 命名清理 |
| 8355796 | RISC-V: AllBitsSetVectorMatchRuleTest.java fix | 测试修复 |

**Zvbb 指令集**: Vector Bit-manipulation used in Cryptography

### RISC-V 浮点指令 (Zfa)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8349632 | RISC-V: 添加 Zfa fminm/fmaxm | 浮点最小/最大指令 |
| 8352022 | RISC-V: 支持 Zfa fminm_h/fmaxm_h | float16 支持 |

**Zfa 指令集**: Additional Floating-Point instructions

### RISC-V 解释器优化

| Issue | 标题 | 说明 |
|-------|------|------|
| 8358105 | RISC-V: Optimize interpreter profile updates | 解释器性能优化 |
| 8357626 | RISC-V: Tighten up template interpreter method entry code | 方法入口优化 |
| 8359801 | RISC-V: Simplify Interpreter::profile_taken_branch | 分支 profiling 简化 |
| 8359105 | RISC-V: No need for acquire fence in safepoint poll during JNI calls | JNI 优化 |
| 8377225 | RISC-V: Improve receiver type profiling reliability | 类型 profiling 改进 |

### RISC-V 内存操作与数组填充

| Issue | 标题 | 说明 |
|-------|------|------|
| 8351140 | RISC-V: Intrinsify Unsafe::setMemory | 内存填充 intrinsic |
| 8356593 | RISC-V: 数组填充 stub 小改进 | 性能优化 |
| 8356700 | RISC-V: fill_words/zero_memory 声明不可压缩范围 | 正确性 |
| 8356869 | RISC-V: 改进数组填充 stub 尾部处理 | 性能优化 |

### 其他

| Issue | 标题 | 说明 |
|-------|------|------|
| 8354815 | RISC-V: Change type of bitwise rotation shift to iRegIorL2I | 类型修正 |
| 8360179 | RISC-V: Only enable BigInteger intrinsics when AvoidUnalignedAccess == false | 正确性修复 |
| 8359218 | RISC-V: Only enable CRC32 intrinsic when AvoidUnalignedAccess == false | 正确性修复 |
| 8366747 | RISC-V: Improve VerifyMethodHandles for method handle linkers | 验证改进 |
| 8371966 | RISC-V: Incorrect pointer dereference in TemplateInterpreterGenerator | Bug 修复 |

---

## 7. 技术特点

### RISC-V 全栈贡献

字节跳动的贡献覆盖 RISC-V 多个层面：

| 层面 | PRs | 说明 |
|------|-----|------|
| **密码学 Intrinsics** | 4 | AES CBC/CTR, GHASH 原生实现 |
| **向量指令** | 5 | Zvbb 位操作，向量标量指令 |
| **解释器优化** | 5 | Profile, 方法入口, JNI |
| **内存/数组操作** | 4 | setMemory, 数组填充 |
| **浮点指令** | 2 | Zfa fminm/fmaxm |
| **其他修复** | 5 | 正确性修复, 验证改进 |

### 支持的 RISC-V 扩展

| 扩展 | 说明 |
|------|------|
| **Zvbb** | 向量位操作 (密码学相关) |
| **Zfa** | 附加浮点指令 |
| **V** | 向量扩展 |

> **注**: 通过源码版权声明搜索 (`Copyright ... ByteDance`)、PR 描述搜索和 commit 邮箱搜索均未发现其他字节跳动贡献者。当前确认仅 Anjian-Wen 一人贡献上游 OpenJDK。

---

## 8. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:Anjian-Wen type:pr label:integrated`
- **统计时间**: 2026-03-19

---

## 9. 相关链接

- [RISC-V International](https://riscv.org/)
- [RISC-V 指令集规范](https://github.com/riscv/riscv-isa-manual)
- [OpenJDK RISC-V Port (JEP 422)](https://openjdk.org/jeps/422)


---

**文档版本**: 2.0
**最后更新**: 2026-03-23
**本次更新**:
- **完善**: 关键贡献列表从 7 个扩展为全部 25 个 PR 的完整记录
- **新增**: 密码学 Intrinsics 分类 (AES CBC/CTR, GHASH) — 4 PRs
- **新增**: 解释器优化分类 (profile, 方法入口, JNI) — 5 PRs
- **更新**: 技术特点从 3 个领域扩展为 6 个层面的全栈分析
- **验证**: 通过源码版权、PR 搜索、commit 邮箱三种方式确认无遗漏贡献者

[→ 返回组织索引](../../by-contributor/README.md)