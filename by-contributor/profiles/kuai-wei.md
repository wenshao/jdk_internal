# Kuai Wei (魏快)

> **Alibaba C2 Compiler Expert** | **Dragonwell JDK Contributor** | **RISC-V, ZGC**

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Kuai Wei (魏快) |
| **GitHub** | [@kuaiwei](https://github.com/kuaiwei) |
| **公司** | [@alibaba](https://github.com/alibaba) |
| **邮箱** | kuaiwei.kw@alibaba-inc.com |
| **OpenJDK Role** | Author, Committer |
| **Integrated PRs** | 13 |
| **主要领域** | C2 Compiler, IR Optimization, RISC-V, ZGC |
| **活跃时间** | 2021 - 至今 |

> **统计来源**: [GitHub Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Akuaiwei+label%3Aintegrated+is%3Aclosed)

---

## 关键指标

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 13 |
| **代码变更** | +2,000 / -1,500 (估计) |
| **主要领域** | C2 IR, RISC-V, 内存屏障 |
| **平均合入时间** | 7-14 天 |

---

## Integrated PRs 统计

### 按组件分布

| 组件 | PR 数量 | 说明 |
|------|--------|------|
| **C2 IR** | 5 | 编译器中间表示优化 |
| **内存屏障** | 2 | Release barrier 实现 |
| **开发工具** | 1 | Windows/WSL 开发环境 |
| **测试修复** | 2 | IR Framework 测试 |
| **C1 编译器** | 1 | 类型分析优化 |
| **DTrace** | 1 | 代码生成 |
| **AArch64** | 1 | 代码清理 |

### 全部 Integrated PRs

| PR | Issue | 标题 | 日期 |
|----|-------|------|------|
| [#30138](https://github.com/openjdk/jdk/pull/30138) | JDK-8379502 | Remove unused PhaseOutput::need_register_stack_bang() | 2025-04 |
| [#25081](https://github.com/openjdk/jdk/pull/25081) | JDK-8356328 | Some C2 IR nodes miss size_of() function | 2025-02 |
| [#24916](https://github.com/openjdk/jdk/pull/24916) | JDK-8355697 | Create windows devkit on wsl and msys2 | 2025-01 |
| [#23824](https://github.com/openjdk/jdk/pull/23824) | JDK-8350858 | [IR Framework] Some tests failed on Cascade Lake | 2024-12 |
| [#23030](https://github.com/openjdk/jdk/pull/23030) | JDK-8347405 | MergeStores with reverse bytes order value | 2024-11 |
| [#20786](https://github.com/openjdk/jdk/pull/20786) | JDK-8339299 | C1 will miss type profile when inline final method | 2024-08 |
| [#20090](https://github.com/openjdk/jdk/pull/20090) | JDK-8335946 | DTrace code snippets should be generated | 2024-07 |
| [#19518](https://github.com/openjdk/jdk/pull/19518) | JDK-8333410 | [AArch64] Clean unused classes | 2024-06 |
| [#19278](https://github.com/openjdk/jdk/pull/19278) | JDK-8325821 | [REDO] use "dmb.ishst+dmb.ishld" for release barrier | 2024-06 |
| [#18075](https://github.com/openjdk/jdk/pull/18075) | JDK-8326983 | Unused operands reported after JDK-8326135 | 2024-04 |
| [#17910](https://github.com/openjdk/jdk/pull/17910) | JDK-8326135 | Enhance adlc to report unused operands | 2024-04 |
| [#17511](https://github.com/openjdk/jdk/pull/17511) | JDK-8324186 | Use "dmb.ishst+dmb.ishld" for release barrier | 2024-03 |
| [#2791](https://github.com/openjdk/jdk/pull/2791) | JDK-8262837 | handle split_USE correctly | 2021-03 |

### 年度趋势

| 年份 | PRs | 主要工作 |
|------|-----|----------|
| 2021 | 1 | C2 编译器基础 |
| 2024 | 10 | 内存屏障，IR 优化，开发工具 |
| 2025 | 2 | C2 IR 完善 |

---

## 主要贡献领域

### 1. C2 编译器 IR 优化

**JDK-8379502**: 移除未使用的 PhaseOutput 方法
- PR: [#30138](https://github.com/openjdk/jdk/pull/30138)
- 清理编译器代码
- 提高可维护性

**JDK-8356328**: C2 IR 节点缺少 size_of() 函数
- PR: [#25081](https://github.com/openjdk/jdk/pull/25081)
- 修复 IR 节点序列化问题
- 确保所有节点类型一致性

**JDK-8326135**: 增强 adlc 报告未使用操作数
- PR: [#17910](https://github.com/openjdk/jdk/pull/17910)
- 改进编译器诊断能力
- 帮助发现潜在问题

### 2. 内存屏障实现

**JDK-8325821**: 使用 "dmb.ishst+dmb.ishld" 作为 release barrier
- PR: [#19278](https://github.com/openjdk/jdk/pull/19278) (REDO)
- PR: [#17511](https://github.com/openjdk/jdk/pull/17511) (原始)
- 改进 ARM 架构内存屏障性能
- 使用更精确的屏障指令

**技术背景**:
```cpp
// 变更前
void release_barrier() {
  dmb.ish();  // 完整的内存屏障
}

// 变更后
void release_barrier() {
  dmb.ishst + dmb.ishld;  // 分离的存储/加载屏障
}
```

### 3. 开发工具改进

**JDK-8355697**: 在 WSL 和 MSYS2 上创建 Windows devkit
- PR: [#24916](https://github.com/openjdk/jdk/pull/24916)
- 简化 Windows 开发环境配置
- 支持 WSL 和 MSYS2 两种环境

### 4. 测试修复

**JDK-8350858**: IR Framework 测试在 Cascade Lake 上失败
- PR: [#23824](https://github.com/openjdk/jdk/pull/23824)
- 修复特定 CPU 微架构的测试问题
- 提高测试稳定性

### 5. C1 编译器优化

**JDK-8339299**: C1 内联 final 方法时丢失类型分析
- PR: [#20786](https://github.com/openjdk/jdk/pull/20786)
- 修复 C1 编译器类型分析 bug
- 提高内联决策准确性

---

## 职业背景

### 阿里巴巴 Dragonwell JDK

Kuai Wei 是阿里巴巴 **Dragonwell JDK** 的核心贡献者之一。Dragonwell 是阿里巴巴基于 OpenJDK 的发行版，针对电商、金融、物流等场景优化。

| 版本 | Stars | Forks | Commits | Kuai Wei 贡献 |
|------|-------|-------|---------|--------------|
| Dragonwell 8 | 4,318 | 501 | 91,553 | 5+ commits |
| Dragonwell 11 | 584 | 118 | 112,268 | 5+ commits |
| Dragonwell 21 | 134 | 28 | - | 5+ commits |

**Dragonwell 主要维护者**:
- **GoeLin** (林珑): 1,200+ commits (Dragonwell 11/21)
- **wangweij** (王卫建): 600+ commits
- **Kuai Wei** (魏快): 15+ commits (JIT 优化，backport)

### Dragonwell 贡献详情

**JIT 编译器 Backport**:
- [JIT] Backport 8318446: C2 optimize stores into primitive arrays
- [JIT] Backport 8255120: C2 assert fix for MemNode
- [JIT] Compress method entries for aarch64

**构建系统改进**:
- Support build with gcc 10
- Make UseAIExtension experimental options

**Bug 修复**:
- [Backport] 6563994: assert(wf.check_method_context) fix
- [Backport] 8239429: AbsPathsInImage.java Windows 失败修复

### 技术专长

| 领域 | 技能 |
|------|------|
| **C2 编译器** | IR 优化，节点分析，诊断改进 |
| **内存屏障** | ARM/AArch64 内存模型，并发优化 |
| **RISC-V** | MacroAssembler，架构移植 |
| **ZGC** | 垃圾回收器优化和移植 |
| **Dragonwell** | JIT backport, 构建系统，aarch64 优化 |

---

## 外部链接

| 类型 | 链接 |
|------|------|
| **GitHub** | https://github.com/kuaiwei |
| **GitHub PRs** | https://github.com/openjdk/jdk/pulls?q=author%3Akuaiwei |
| **OpenJDK Census** | https://openjdk.org/census#kuaiwei |
| **Dragonwell 8** | https://github.com/dragonwell-project/dragonwell8 |
| **Dragonwell 11** | https://github.com/dragonwell-project/dragonwell11 |
| **Dragonwell 21** | https://github.com/dragonwell-project/dragonwell21 |
| **Dragonwell 官网** | https://dragonwell-jdk.io/ |

---

## 相关文档

- [C2 编译器](/by-topic/core/jit/) - JIT 编译优化
- [RISC-V](/by-topic/arch/riscv/) - RISC-V 架构支持
- [内存屏障](/by-topic/concurrency/memory-barriers/) - 并发内存模型
- [Alibaba](/contributors/orgs/alibaba.md) - 阿里巴巴贡献者

---

**最后更新**: 2026-03-21
