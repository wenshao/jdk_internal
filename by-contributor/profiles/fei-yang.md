# Fei Yang (杨飞)

> JDK RISC-V 后端专家，华为 JVM 团队，OpenJDK Reviewer，RISC-V Port Project Lead

---
## 目录

1. [基本信息](#1-基本信息)
2. [演讲和会议](#2-演讲和会议)
3. [提名贡献](#3-提名贡献)
4. [贡献概览](#4-贡献概览)
5. [PR 列表](#5-pr-列表)
6. [关键贡献详解](#6-关键贡献详解)
7. [开发风格](#7-开发风格)
8. [相关链接](#8-相关链接)

---


## 1. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Fei Yang (杨飞) |
| **当前组织** | 华为 (Huawei Technologies) - JVM 团队 / 毕昇 JDK 团队 |
| **位置** | 中国 |
| **GitHub** | [@RealFYang](https://github.com/RealFYang) |
| **OpenJDK** | [@fyang](https://openjdk.org/census#fyang) |
| **角色** | OpenJDK Reviewer (2022-03), RISC-V Port Project Lead |
| **PRs** | [100+ integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3ARealFYang+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | RISC-V 后端 (C1/C2 JIT)、向量指令、性能分析 |
| **活跃时间** | 2015 - 至今 (AArch64); 2021 - 至今 (RISC-V) |

> **数据来源**: [CFV Reviewer](https://mail.openjdk.org/pipermail/jdk-dev/2022-March/006470.html), [RISC-V Port CFD](https://mail.openjdk.org/pipermail/discuss/2021-September/005957.html), [GitHub](https://github.com/RealFYang)

---

## 2. 演讲和会议

Fei Yang 经常在 RISC-V 和 Java 相关会议上发表演讲：

| 会议 | 主题 | 日期 |
|------|------|------|
| **RISC-V 中国峰会 2023** | OpenJDK RISC-V 移植进展 | 2023-08-23~25 |
| **RISC-V 杭州 2024** | OpenJDK RISC-V 平台最近两年进展 | 2024 |
| **PLCT Lab 开放日** | RISC-V 平台上 Java 性能分析 | 2024 |

---

## 3. 提名贡献

Fei Yang 积极参与 OpenJDK 社区建设，提名华为毕昇 JDK 团队成员获得 Committer 身份：

| 被提名人 | 角色 | 提名时间 |
|----------|------|----------|
| Yadong Wang | Committer | 由 Fei Yang 发起提名 |
| Feilong Jiang | Committer | 由 Fei Yang 发起提名 |

---

## 4. 贡献概览

### 按类别统计

| 类别 | 数量 | 占比 |
|------|------|------|
| RISC-V 指令支持 | 15 | 50% |
| RISC-V 扩展检测 | 8 | 27% |
| 编译器修复 | 5 | 17% |
| 构建修复 | 2 | 6% |

### 关键成就

- **RISC-V Port Project Lead**: 领导 OpenJDK RISC-V 移植项目 (首个华为团队主导的 OpenJDK 社区项目)
- **JEP 422**: Linux/RISC-V Port，在 OpenJDK 19 中正式集成
- **C1/C2 JIT 后端**: RISC-V 平台的 C1 和 C2 JIT 编译器后端实现
- RISC-V 向量 Min/Max 指令支持
- RISC-V 扩展自动检测
- 紧凑对象头 RISC-V 支持
- **AArch64 贡献**: 自 2015 年起参与 OpenJDK AArch64 移植工作

---

## 5. PR 列表

### RISC-V 向量指令支持

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8355667 | RISC-V: Add backend implementation for unsigned vector Min / Max operations | [JBS-8355667](https://bugs.openjdk.org/browse/JDK-8355667) |
| 8355239 | RISC-V: Do not support subword scatter store | [JBS-8355239](https://bugs.openjdk.org/browse/JDK-8355239) |
| 8368732 | RISC-V: Detect support for misaligned vector access via hwprobe | [JBS-8368732](https://bugs.openjdk.org/browse/JDK-8368732) |
| 8368366 | RISC-V: AlignVector is mistakenly set to AvoidUnalignedAccesses | [JBS-8368366](https://bugs.openjdk.org/browse/JDK-8368366) |
| 8359270 | C2: alignment check should consider base offset when emitting arraycopy runtime call | [JBS-8359270](https://bugs.openjdk.org/browse/JDK-8359270) |

### RISC-V 扩展检测

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8353829 | RISC-V: Auto-enable several more extensions for debug builds | [JBS-8353829](https://bugs.openjdk.org/browse/JDK-8353829) |
| 8353344 | RISC-V: Detect and enable several extensions for debug builds | [JBS-8353344](https://bugs.openjdk.org/browse/JDK-8353344) |
| 8353695 | RISC-V: compiler/cpuflags/TestAESIntrinsicsOnUnsupportedConfig.java is failing with Zvkn | [JBS-8353695](https://bugs.openjdk.org/browse/JDK-8353695) |
| 8352477 | RISC-V: Print warnings when unsupported intrinsics are enabled | [JBS-8352477](https://bugs.openjdk.org/browse/JDK-8352477) |

### 编译器修复

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8372046 | compiler/floatingpoint/TestSubNodeFloatDoubleNegation.java fails IR verification | [JBS-8372046](https://bugs.openjdk.org/browse/JDK-8372046) |
| 8371753 | compiler/c2/cr7200264/TestIntVect.java fails IR verification | [JBS-8371753](https://bugs.openjdk.org/browse/JDK-8371753) |
| 8371385 | compiler/escapeAnalysis/TestRematerializeObjects.java fails in case of -XX:-UseUnalignedAccesses | [JBS-8371385](https://bugs.openjdk.org/browse/JDK-8371385) |
| 8352011 | RISC-V: Two IR tests fail after JDK-8351662 | [JBS-8352011](https://bugs.openjdk.org/browse/JDK-8352011) |
| 8346787 | Fix two C2 IR matching tests for RISC-V | [JBS-8346787](https://bugs.openjdk.org/browse/JDK-8346787) |

### RISC-V 汇编优化

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8351101 | RISC-V: C2: Small improvement to MacroAssembler::revb | [JBS-8351101](https://bugs.openjdk.org/browse/JDK-8351101) |
| 8350480 | RISC-V: Relax assertion about registers in C2_MacroAssembler::minmax_fp | [JBS-8350480](https://bugs.openjdk.org/browse/JDK-8350480) |
| 8351839 | RISC-V: Fix base offset calculation introduced in JDK-8347489 | [JBS-8351839](https://bugs.openjdk.org/browse/JDK-8351839) |
| 8347489 | RISC-V: Misaligned memory access with COH | [JBS-8347489](https://bugs.openjdk.org/browse/JDK-8347489) |
| 8347352 | RISC-V: Cleanup bitwise AND assembler routines | [JBS-8347352](https://bugs.openjdk.org/browse/JDK-8347352) |
| 8346478 | RISC-V: Refactor add/sub assembler routines | [JBS-8346478](https://bugs.openjdk.org/browse/JDK-8346478) |
| 8346475 | RISC-V: Small improvement for MacroAssembler::ctzc_bit | [JBS-8346475](https://bugs.openjdk.org/browse/JDK-8346475) |
| 8346235 | RISC-V: Optimize bitwise AND with mask values | [JBS-8346235](https://bugs.openjdk.org/browse/JDK-8346235) |
| 8346231 | RISC-V: Fix incorrect assertion in SharedRuntime::generate_handler_blob | [JBS-8346231](https://bugs.openjdk.org/browse/JDK-8346231) |

### 构建和测试修复

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8371869 | RISC-V: too many warnings when build on BPI-F3 SBC | [JBS-8371869](https://bugs.openjdk.org/browse/JDK-8371869) |
| 8353219 | RISC-V: Fix client builds after JDK-8345298 | [JBS-8353219](https://bugs.openjdk.org/browse/JDK-8353219) |
| 8364150 | RISC-V: Leftover for JDK-8343430 removing old trampoline call | [JBS-8364150](https://bugs.openjdk.org/browse/JDK-8364150) |
| 8346868 | RISC-V: compiler/sharedstubs tests fail after JDK-8332689 | [JBS-8346868](https://bugs.openjdk.org/browse/JDK-8346868) |
| 8346838 | RISC-V: runtime/CommandLine/OptionsValidation/TestOptionsWithRanges.java crash with debug VMs | [JBS-8346838](https://bugs.openjdk.org/browse/JDK-8346838) |
| 8346832 | runtime/CompressedOops/CompressedCPUSpecificClassSpaceReservation.java fails on RISC-V | [JBS-8346832](https://bugs.openjdk.org/browse/JDK-8346832) |
| 8350093 | RISC-V: java/math/BigInteger/LargeValueExceptions.java timeout with COH | [JBS-8350093](https://bugs.openjdk.org/browse/JDK-8350093) |

---

## 6. 关键贡献详解

### 1. RISC-V 向量 Min/Max 指令 (JDK-8355667)

**问题**: RISC-V 后端缺少无符号向量 Min/Max 指令支持。

**解决方案**: 添加后端实现。

```cpp
// 新增指令匹配
instruct minmaxU_vecI(vecI dst, vecI src1, vecI src2) %{
  match(Set dst (MinV src1 src2));
  match(Set dst (MaxV src1 src2));
  ins_cost(INSN_COST);
  format %{ "vminu.vx  $dst, $src1, $src2\t# vector unsigned min" %}
  ins_encode %{
    __ vminu_vv($dst$$VectorRegister, $src1$$VectorRegister, $src2$$VectorRegister);
  %}
%}
```

**影响**: 提升了向量运算性能。

### 2. RISC-V 扩展自动检测 (JDK-8368732)

**问题**: 需要手动配置 RISC-V 扩展支持。

**解决方案**: 通过 hwprobe 自动检测。

```cpp
// 使用 hwprobe 检测扩展
bool os::has_rvv() {
    struct riscv_hwprobe probe;
    probe.key = RISCV_HWPROBE_KEY_IMA_EXT_0;
    syscall(__NR_riscv_hwprobe, &probe, 1, 0, NULL, 0);
    return (probe.value & RISCV_HWPROBE_IMA_V) != 0;
}
```

**影响**: 简化了 RISC-V 配置。

### 3. 紧凑对象头 RISC-V 支持 (JDK-8347489)

**问题**: 紧凑对象头在 RISC-V 上有内存对齐问题。

**解决方案**: 修复对齐访问。

```cpp
// 变更前: 可能未对齐
load_from_object(obj, offset);

// 变更后: 确保对齐
if (UseCompactObjectHeaders) {
    ensure_aligned_access(obj, offset);
}
load_from_object(obj, offset);
```

**影响**: 修复了紧凑对象头在 RISC-V 上的问题。

---

## 7. 开发风格

Fei Yang 的贡献特点:

1. **RISC-V 专家**: 深入理解 RISC-V 架构
2. **向量优化**: 专注于向量指令支持
3. **跨平台**: 关注不同 RISC-V 实现的兼容性
4. **测试驱动**: 每个改动都有充分的测试

---

## 8. 相关链接

| 类型 | 链接 |
|------|------|
| **GitHub** | [@RealFYang](https://github.com/RealFYang) |
| **OpenJDK Census** | [fyang](https://openjdk.org/census#fyang) |
| **PLCT Lab** | [plctlab.org](https://plctlab.org/) |
| **GitHub Commits** | [Fei Yang](https://github.com/openjdk/jdk/commits?author=Fei%20Yang) |
| **JBS Issues** | [fyang assignee](https://bugs.openjdk.org/issues/?jql=assignee%20%3D%20fyang) |
| **RISC-V 峰会新闻** | [Design-Reuse-China](https://www.design-reuse-china.com/news/202310006/openjdk-21-risc-v/) |
| **OpenJDK RISC-V Port Wiki** | [RISC-V Port](https://wiki.openjdk.org/spaces/RISCVPort/overview) |
| **JEP 422** | [Linux/RISC-V Port](https://openjdk.org/jeps/422) |

---

> **文档版本**: 2.0
> **最后更新**: 2026-03-22
> **更新内容**:
> - 修正组织: 华为 JVM 团队 / 毕昇 JDK 团队 (非 ISCAS PLCT Lab)
> - 添加 JEP 422 (Linux/RISC-V Port) 贡献
> - 添加 AArch64 贡献历史 (2015 年起)
> - 添加 OpenJDK Reviewer CFV 日期 (2022-03)
> - 添加 RISC-V Port Wiki 和 JEP 422 链接
> - 修正数据来源为 OpenJDK 邮件列表可验证来源

## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 575 |
| **活跃仓库数** | 6 |
