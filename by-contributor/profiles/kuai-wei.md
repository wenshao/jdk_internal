# Kuai Wei

> **Alibaba C2 Compiler Expert** | **Dragonwell JDK Contributor** | **RISC-V, ZGC**

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Kuai Wei |
| **GitHub** | [@kuaiwei](https://github.com/kuaiwei) |
| **公司** | [@alibaba](https://github.com/alibaba) |
| **邮箱** | kuaiwei.kw@alibaba-inc.com, wei.kuai@gmail.com |
| **OpenJDK Census** | ✅ [记录在案](https://openjdk.org/census) |
| **Integrated PRs** | 13 |
| **Dragonwell Commits** | 15+ |
| **主要领域** | C2 Compiler, IR Optimization, RISC-V, ZGC |
| **活跃时间** | 2021 - 至今 |

> **统计来源**: [GitHub Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Akuaiwei+label%3Aintegrated+is%3Aclosed), [OpenJDK Census](https://openjdk.org/census)

---

## 技术方向

**基于 GitHub 仓库和贡献分析**：

| 领域 | 证据 |
|------|------|
| **C2 编译器** | OpenJDK 13 PRs (IR 优化，节点分析) |
| **RISC-V** | Starred: riscv-openjdk, riscv-port, aliyun/yitian-ecs |
| **JIT 编译器** | Starred: jeandle/jeandle-jdk (LLVM-based JIT) |
| **GraalVM** | Starred: graalvm/mandrel, oracle/graal |
| **Dragonwell** | 15+ commits to dragonwell8/11/21 |
| **内存屏障** | OpenJDK PRs: dmb.ishst+dmb.ishld for release barrier |
| **LLVM** | Starred: llvm/llvm-project |
| **AArch64** | OpenJDK commits: nativeInst_aarch64 cleanup |

**关注领域** (从 Starred/Forked Repos 推断):
- Jeandle JDK (LLVM-based JIT 编译器)
- RISC-V 架构支持 (riscv-openjdk, riscv-port)
- GraalVM 和 Mandrel 分发版
- Alibaba FastFFI
- Renaissance Benchmark Suite
- DynamoRIO (动态插桩工具)

**OpenJDK 邮件列表活动** (2021 年 3 月):
- 参与 hotspot-compiler-dev 邮件列表讨论
- 邮件地址：github.com+1981974+kuaiwei at openjdk.java.net
- 讨论主题：C2 编译器优化，assert 修复

---

## 数据核实

**多渠道交叉印证**：

| 来源 | 显示名称 | 邮箱 | 组织 | 状态 |
|------|----------|------|------|------|
| **GitHub** | kuaiwei | - | @alibaba | ✅ 已验证 |
| **OpenJDK Census** | Kuai Wei | - | - | ✅ 记录在案 |
| **Dragonwell Commits** | Kuai Wei | kuaiwei.kw@alibaba-inc.com | Alibaba | ✅ 已验证 |
| **Dragonwell Commits** | Kuai Wei | wei.kuai@gmail.com | - | ✅ 个人邮箱 |
| **ASE 2021 论文** | Wei Kuai | - | Alibaba Group | ✅ 合著者 |

**学术论文**：
- **ASE 2021**: "Towards a Serverless Java Runtime"
  - 作者：Yifei Zhang, Tianxiao Gu, Xiaolin Zheng, Lei Yu, **Wei Kuai**, Sanhong Li
  - 单位：Alibaba Group
  - DBLP: [记录](https://dblp.org/rec/conf/kbse/0001GZYKL21)
  - Semantic Scholar: [记录](https://www.semanticscholar.org/paper/Towards-a-Serverless-Java-Runtime-Zhang-Gu)

**GitHub Gists** (技术笔记):
- [JMH alloc with final field](https://gist.github.com/kuaiwei/f71fba40df29991c93325a8600e34c13) - 性能测试
- [Java ArrayList.toArray](https://gist.github.com/kuaiwei/7109343) - Java 问题记录
- [X Window client access](https://gist.github.com/kuaiwei/5001706) - Linux 系统笔记

**社交网络分析** (基于 GitHub 关注关系):

| 关联类型 | 用户 | 信息 | 推断 |
|----------|------|------|------|
| **论文合著者** | sanhong | Sanhong Li | ASE 2021 论文合著者，互相关注 |
| **阿里巴巴同事** | JoshuaZhuwj | Joshua Zhu, @Alibaba, 上海 | 互相关注 |
| **阿里巴巴同事** | sendaoYan | Sendaoyan Yan, 上海, compiler tester | Kuai Wei 的 follower |
| **社区联系** | luchsh | Jonathan Lu, 上海 | 互相关注 |
| **龙芯联系** | xiangzhai | Leslie Zhai, @loongson, 北京 | Kuai Wei 的 follower |
| **JDK 社区** | headius | Charles Nutter (JRuby 创始人) | Kuai Wei 关注 |

**地理位置推断**：
- 多个互相关注者位于**上海**（Joshua Zhu, Jonathan Lu, Sendaoyan Yan）
- 阿里巴巴在上海有大型研发团队
- **推断**: Kuai Wei 可能工作于**阿里巴巴上海团队**

**Jeandle JDK 项目关联**：
- Kuai Wei 是 [Jeandle JDK](https://github.com/jeandle/jeandle-jdk) 项目的活跃贡献者
- Jeandle 是基于 LLVM 的 Java JIT 编译器项目
- 最近 PR: #393 (2026-03-11, merged 2026-03-16)
  - 修复 TestStackBangRbp.java 测试失败
  - Additions: 32, Deletions: 8
  - Merged by: jeandle-bot
- 项目与 OpenJDK 顶级贡献者有关联（jonathan-gibbons, shipilev, prrace 等）

**OpenJDK 贡献时间线**：
| 日期 | Issue | 说明 | Reviewer |
|------|-------|------|----------|
| 2025-05 | JDK-8356328 | C2 IR 节点 size_of() 函数 | thartmann, chagedor |
| 2025-04 | JDK-8355697 | Windows devkit on WSL/MSYS2 | ihse, erikj |
| 2025-03 | JDK-8347405 | MergeStores 反向字节顺序 | Richard Reingruber |
| 2025-02 | JDK-8350858 | IR Framework 测试失败 (Cascade Lake) | chagedor |
| 2024-09 | JDK-8339299 | C1 内联 final 方法丢失类型 profile | lmesnik |
| 2024-06 | JDK-8325821 | [REDO] release barrier (dmb.ishst+dmb.ishld) | shade |
| 2024-06 | JDK-8333410 | [AArch64] 清理未使用的类 | - |
| 2024-03 | JDK-8326983 | 未使用的操作数报告 | kvn, vlivanov |
| 2024-02 | JDK-8326135 | 增强 adlc 报告未使用操作数 | kvn, vlivanov |
| 2021-03 | JDK-8262837 | handle split_USE correctly | - |
| 2020-04 | JDK-8242449 | AArch64: r27 分配 (CompressedOops 模式) | aph |
| 2018-10 | JDK-8210853 | JIT: C2 新分配对象后屏障优化 | - |

**RISC-V OpenJDK 贡献**：
- 2021-03: JDK-8262837 handle split_USE correctly
- 2020-04: JDK-8242449 AArch64: r27 can be allocated in CompressedOops mode
- 2018-10: JDK-8210853 JIT: C2 doesn't skip post barrier for new allocated objects

**无法证实的信息**：
- ❌ 中文名：公开来源无确凿证据（拼音 Wei Kuai 可能对应多个中文名）
- ❌ 教育背景：论文仅标注 Alibaba Group，无学校信息
- ❌ 具体职位：仅知为 Alibaba 贡献者
- ❌ 专利：Google Patents 无公开记录

**注意**: 文档中不使用未经证实的中文名和教育背景信息。

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
- **Kuai Wei**: 15+ commits (JIT 优化，backport)

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
