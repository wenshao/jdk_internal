# Kuai Wei

> **Alibaba C2 Compiler Expert** | **Dragonwell JDK Contributor** | **RISC-V, ZGC**

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Kuai Wei |
| **GitHub** | [@kuaiwei](https://github.com/kuaiwei) |
| **组织** | [Alibaba](../../contributors/orgs/alibaba.md) |
| **邮箱** | kuaiwei.kw@alibaba-inc.com, wei.kuai@gmail.com |
| **OpenJDK Census** | ✅ [Committer, JDK Project](https://openjdk.org/census#kwei) (username: `kwei`) |
| **Integrated PRs** | 13 |
| **Dragonwell Commits** | 15+ |
| **GitHub 统计** | 19 public repos, 15 followers, 8 following |
| **主要领域** | C2 Compiler, IR Optimization, RISC-V, ZGC |
| **活跃时间** | 2018 - 至今 (2018 年加入阿里云, 首个 Integrated PR: 2021) |
| **教育背景** | Carnegie Mellon University (高级计算机科学), University of Auckland (博士研究) |
| **工作经历** | HPE (HotSpot JIT, 2007-2018) → 阿里云 (JVM 架构师, 2018-至今), 新西兰 3E Software CEO |
| **演讲** | "Speed JVM Performance with JWarmUp" (合作), "Java on RISC-V: OpenJDK Porting" (RISC-V Forum 2021, 与 Sanhong Li 合作) |

> **统计来源**: [GitHub Integrated PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Akuaiwei+label%3Aintegrated+is%3Aclosed), [OpenJDK Census](https://openjdk.org/census#kwei)

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

**会议演讲**:
- **JWarmUp**: 与 Xiaoming Gu 合作演讲 "Speed JVM Performance with JWarmUp"，展示了使用 JWarmUp 加速大型 Java 应用及 AppAOT 加速小型应用的统一方案

**OpenJDK 邮件列表活动** (2021 年 3 月):
- 参与 hotspot-compiler-dev 邮件列表讨论
- 邮件地址：github.com+1981974+kuaiwei at openjdk.java.net
- 讨论主题：C2 编译器优化，assert 修复

---

## 数据核实

**多渠道交叉印证**：

| 来源 | 显示名称 | 邮箱 | 组织 | 状态 |
|------|----------|------|------|------|
| **GitHub** | kuaiwei | - | @alibaba | ✅ 已验证 (19 repos, 15 followers) |
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

**GitHub 成就徽章**:
- Pair Extraordinaire (x2)
- Pull Shark (x2)
- Quickdraw
- Arctic Code Vault Contributor

**GitHub Gists** (技术笔记):
- [JMH alloc with final field](https://gist.github.com/kuaiwei/f71fba40df29991c93325a8600e34c13) - 性能测试
- [Java ArrayList.toArray](https://gist.github.com/kuaiwei/7109343) - Java 问题记录
- [X Window client access](https://gist.github.com/kuaiwei/5001706) - Linux 系统笔记

**社交网络分析** (基于 GitHub 关注关系):

| 关联类型 | 用户 | 真实姓名 | 位置 | 组织 | 推断 |
|----------|------|----------|------|------|------|
| **论文合著者** | [sanhong](sanhong.md) | Sanhong Li | - | - | ASE 2021 论文合著者，互相关注 |
| **阿里巴巴同事** | [JoshuaZhuwj](joshua-zhu.md) | Joshua Zhu | 上海 | [Alibaba](../../contributors/orgs/alibaba.md) | 互相关注 |
| **阿里巴巴同事** | [sendaoYan](sendaoyan.md) | Sendaoyan Yan | 上海 | - | Kuai Wei 的 follower, compiler tester |
| **阿里巴巴同事** | [yanglong1010](yanglong1010.md) | Long Yang | 杭州 | [Alibaba](../../contributors/orgs/alibaba.md) | 互相关注 |
| **社区联系** | [luchsh](luchsh.md) | Jonathan Lu | 上海 | - | 互相关注 |
| **社区联系** | [tanghaoth90](tanghaoth90.md) | Hao Tang | 杭州 | [ByteDance](../../contributors/orgs/bytedance.md) | 互相关注 |
| **社区联系** | [XHao](xhao.md) | shako | 上海 | - | 互相关注 |
| **龙芯联系** | [xiangzhai](xiangzhai.md) | Leslie Zhai | 北京 | [Loongson](../../contributors/orgs/loongson.md) | Kuai Wei 的 follower |
| **JDK 社区** | [alijvm](alijvm.md) | Sanhong Li | - | - | 阿里巴巴 JVM 团队账号 |
| **JDK 社区** | [Aitozi](aitozi.md) | WenjunMin | - | - | 互相关注 |
| **JDK 社区** | [headius](headius.md) | Charles Nutter | - | - | Kuai Wei 关注 (JRuby 创始人) |

**地理位置推断**：
- 多个互相关注者位于**上海**（Joshua Zhu, Jonathan Lu, Sendaoyan Yan, shako）
- 多个互相关注者位于**杭州**（Long Yang, Hao Tang）
- 阿里巴巴在上海和杭州都有大型研发团队
- **推断**: Kuai Wei 可能工作于**阿里巴巴上海/杭州团队**（JVM 方向）

**技术社区关联**：
- 与阿里巴巴 JVM 团队（alijvm）有紧密联系
- 与龙芯（xiangzhai）有联系，可能参与 RISC-V/LoongArch 相关工作
- 与 ByteDance（tanghaoth90）有联系，可能是行业交流

**Jeandle JDK 项目关联**：
- Kuai Wei 是 [Jeandle JDK](https://github.com/jeandle/jeandle-jdk) 项目的核心贡献者
- Jeandle 是基于 LLVM 的 Java JIT 编译器项目 (422 stars, 57 forks)
- 项目创建：2025-06-25
- Kuai Wei 的贡献：
  - PR #393 (2026-03-11, merged 2026-03-16): 修复 TestStackBangRbp.java 测试失败
    - 修改文件：jeandleAbstractInterpreter.cpp, jeandleCompiledCode.cpp 等
    - Additions: 32, Deletions: 8
  - Commit db2d2aa (2025-12-08): Create ScopeValue for jeandle compiled code
  - Commit 3ad757f (2025-11-17): Track java basic type in JeandleVMState
  - Commit 038bf18 (2025-10-27): Support create new java instance
  - Commit 19bec1d (2025-09-19): Support intrinsic implemented by native function
  - Commit 4681197 (2025-09-11): Support inline intrinsic functions
- 项目与 OpenJDK 顶级贡献者有关联（jonathan-gibbons, shipilev, prrace 等）

**OpenJDK 贡献时间线**：
| 日期 | Issue | 说明 | Reviewer |
|------|-------|------|----------|
| 2026-03 | JDK-8379502 | 移除未使用的 PhaseOutput 方法 | chagedorn |
| 2025-05 | JDK-8356328 | C2 IR 节点 size_of() 函数 | thartmann, chagedorn |
| 2025-04 | JDK-8355697 | Windows devkit on WSL/MSYS2 | ihse, erikj |
| 2025-03 | JDK-8347405 | MergeStores 反向字节顺序 | Richard Reingruber |
| 2025-02 | JDK-8350858 | IR Framework 测试失败 (Cascade Lake) | chagedorn |
| 2024-09 | JDK-8339299 | C1 内联 final 方法丢失类型 profile | lmesnik |
| 2024-06 | JDK-8325821 | [REDO] release barrier (dmb.ishst+dmb.ishld) | shade |
| 2024-06 | JDK-8333410 | [AArch64] 清理未使用的类 | - |
| 2024-03 | JDK-8326983 | 未使用的操作数报告 | kvn, vlivanov |
| 2024-02 | JDK-8326135 | 增强 adlc 报告未使用操作数 | kvn, vlivanov |
| 2024-01 | JDK-8324186 | release barrier (dmb.ishst+dmb.ishld) 原始版本 | RealFYang, aph |
| 2022-03 | JEP 422 | Linux/RISC-V Port (co-author) | ihse, dholmes, rriggs, kvn, shade |
| 2021-03 | JDK-8262837 | handle split_USE correctly | - |
| 2020-04 | JDK-8242449 | AArch64: r27 分配 (CompressedOops 模式) | aph |
| 2018-10 | JDK-8210853 | JIT: C2 新分配对象后屏障优化 | - |

**JEP 422: Linux/RISC-V Port (Co-author)**:
- 作为 JEP 422 实现的 [co-author](https://github.com/openjdk/jdk/commit/5905b02c0e2643ae8d097562f181953f6c88fc89)（commit 5905b02, 2022-03-24）
- 与 Huawei (Fei Yang 等)、Alibaba (Xiaolin Zheng)、Aleksey Shipilev (formerly Red Hat, now Amazon)、Oracle (Magnus Ihse Bursie) 共同完成
- 为 riscv-port-jdk11u 提交 backport PR

**早期 OpenJDK 贡献 (Bug Database)**：
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
| [#30138](https://github.com/openjdk/jdk/pull/30138) | JDK-8379502 | Remove unused PhaseOutput::need_register_stack_bang() | 2026-03 |
| [#25081](https://github.com/openjdk/jdk/pull/25081) | JDK-8356328 | Some C2 IR nodes miss size_of() function | 2025-05 |
| [#24916](https://github.com/openjdk/jdk/pull/24916) | JDK-8355697 | Create windows devkit on wsl and msys2 | 2025-04 |
| [#23824](https://github.com/openjdk/jdk/pull/23824) | JDK-8350858 | [IR Framework] Some tests failed on Cascade Lake | 2025-02 |
| [#23030](https://github.com/openjdk/jdk/pull/23030) | JDK-8347405 | MergeStores with reverse bytes order value | 2025-03 |
| [#20786](https://github.com/openjdk/jdk/pull/20786) | JDK-8339299 | C1 will miss type profile when inline final method | 2024-09 |
| [#20090](https://github.com/openjdk/jdk/pull/20090) | JDK-8335946 | DTrace code snippets should be generated | 2024-07 |
| [#19518](https://github.com/openjdk/jdk/pull/19518) | JDK-8333410 | [AArch64] Clean unused classes | 2024-06 |
| [#19278](https://github.com/openjdk/jdk/pull/19278) | JDK-8325821 | [REDO] use "dmb.ishst+dmb.ishld" for release barrier | 2024-06 |
| [#18075](https://github.com/openjdk/jdk/pull/18075) | JDK-8326983 | Unused operands reported after JDK-8326135 | 2024-03 |
| [#17910](https://github.com/openjdk/jdk/pull/17910) | JDK-8326135 | Enhance adlc to report unused operands | 2024-02 |
| [#17511](https://github.com/openjdk/jdk/pull/17511) | JDK-8324186 | Use "dmb.ishst+dmb.ishld" for release barrier | 2024-01 |
| [#2791](https://github.com/openjdk/jdk/pull/2791) | JDK-8262837 | handle split_USE correctly | 2021-03 |

### 年度趋势

| 年份 | PRs | 主要工作 |
|------|-----|----------|
| 2021 | 1 | C2 编译器基础 (split_USE) |
| 2024 | 7 | 内存屏障 (dmb)，adlc 增强，DTrace，AArch64 清理，C1 类型分析 |
| 2025 | 4 | MergeStores 优化，IR Framework 测试，WSL devkit，C2 IR size_of |
| 2026 | 1 | 编译器代码清理 (PhaseOutput) |

---

## 主要贡献领域

### 1. C2 编译器 IR 优化

**JDK-8379502**: 移除未使用的 PhaseOutput 方法
- PR: [#30138](https://github.com/openjdk/jdk/pull/30138) (2026-03 集成)
- Reviewed by Christian Hagedorn (@chhagedorn), sponsored by D-D-H
- 移除 IA64 遗留代码 `need_register_stack_bang()`
- 清理编译器代码，提高可维护性

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
- PR: [#17511](https://github.com/openjdk/jdk/pull/17511) (原始, 2024-01 集成, reviewed by Fei Yang, sponsored by Andrew Haley)
- 原始 PR 集成后发现性能回归 (JDK-8325449, JDK-8325269)
- PR: [#19278](https://github.com/openjdk/jdk/pull/19278) (REDO, 2024-06 集成, 修复回归问题)
- 改进 ARM 架构内存屏障性能，使用更精确的屏障指令

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

**JWarmUp 模块**:
- Dragonwell 8u JWarmUp 功能移植与修复
- 与 Xiaoming Gu 合作演讲 "Speed JVM Performance with JWarmUp"

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
| **RISC-V** | JEP 422 co-author，MacroAssembler，架构移植 |
| **ZGC** | 垃圾回收器优化和移植 |
| **JWarmUp** | Dragonwell JWarmUp 模块移植与优化 |
| **Dragonwell** | JIT backport, 构建系统，aarch64 优化 |

---

## 外部链接

| 类型 | 链接 |
|------|------|
| **GitHub** | https://github.com/kuaiwei |
| **GitHub PRs** | https://github.com/openjdk/jdk/pulls?q=author%3Akuaiwei |
| **OpenJDK Census** | https://openjdk.org/census#kwei |

**JEP 贡献**:
- [JEP 422: Linux/RISC-V Port](https://openjdk.org/jeps/422) - Co-author ([commit 5905b02](https://github.com/openjdk/jdk/commit/5905b02c0e2643ae8d097562f181953f6c88fc89))

**Dragonwell 相关**:
- [Dragonwell 团队](../../contributors/orgs/dragonwell.md) - 核心团队成员和社交网络
- [Dragonwell 8](https://github.com/dragonwell-project/dragonwell8)
- [Dragonwell 11](https://github.com/dragonwell-project/dragonwell11)
- [Dragonwell 21](https://github.com/dragonwell-project/dragonwell21)
- [Dragonwell 官网](https://dragonwell-jdk.io/)

---

## 相关文档

### 阿里巴巴 JVM 团队
- [Sanhong Li](sanhong.md) - ASE 2021 论文作者，阿里巴巴 JVM 团队
- [Long Yang](yanglong1010.md) - 阿里巴巴 JVM 团队，杭州
- [Sendaoyan Yan](sendaoyan.md) - 编译器测试工程师，上海
- [Joshua Zhu](joshua-zhu.md) - 阿里巴巴上海团队
- [alijvm](alijvm.md) - 阿里巴巴 JVM 团队账号

### 技术社区
- [Jonathan Lu](luchsh.md) - 上海 JVM 社区
- [Hao Tang](tanghaoth90.md) - ByteDance，杭州
- [shako](xhao.md) - 上海 JVM 社区
- [WenjunMin](aitozi.md) - JVM 社区
- [Leslie Zhai](xiangzhai.md) - 龙芯，北京
- [Charles Nutter](headius.md) - JRuby 创始人

### 技术主题
- [C2 编译器](/by-topic/core/jit/) - JIT 编译优化
- [RISC-V](/by-topic/platform/) - RISC-V 架构支持
- 内存屏障 - 并发内存模型
- [Alibaba](../../contributors/orgs/alibaba.md) - 阿里巴巴贡献者
- [中国贡献者](chinese-contributors.md) - 中国 OpenJDK 贡献者

---

**最后更新**: 2026-03-22
