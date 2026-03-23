# 阿里巴巴

> 核心库性能优化、编译器改进和 HotSpot Runtime 增强

[← 返回组织索引](README.md)

---
## 目录

1. [概览](#1-概览)
2. [贡献者](#2-贡献者)
3. [技术领域](#3-技术领域)
4. [按版本贡献](#4-按版本贡献)
5. [版本贡献统计](#5-版本贡献统计)
6. [贡献时间线](#6-贡献时间线)
7. [影响的模块](#7-影响的模块)
8. [关键贡献](#8-关键贡献)
9. [相关 PR 分析文档](#9-相关-pr-分析文档)
10. [技术深度分析](#10-技术深度分析)
11. [相关主题文档](#11-相关主题文档)
12. [技术特点](#12-技术特点)
13. [Alibaba Dragonwell](#13-alibaba-dragonwell)
14. [影响评估](#14-影响评估)
15. [数据来源](#15-数据来源)
16. [相关链接](#16-相关链接)

---


## 1. 概览

阿里巴巴通过 Dragonwell/JVM 团队参与 OpenJDK 开发，主要贡献集中在核心库性能优化、C2/C1 编译器改进、HotSpot Runtime 增强和 AArch64/RISC-V 架构支持。

| 指标 | 值 |
|------|------|
| **Authored PRs** | 246 (当前) + 202 (前员工测试) = **448** |
| **参与贡献 (含 Review/Sponsor)** | **600+** (来自内部仪表盘统计) |
| **贡献者数** | 13 上游贡献者 (6 Committer + 7 Author) + 1 团队负责人 |
| **活跃时间** | 2020 - 至今 |
| **主要领域** | 核心库、C2 编译器、AArch64、ZGC、RISC-V、HotSpot Runtime |
| **Dragonwell** | [Alibaba Dragonwell](https://github.com/dragonwell-project/dragonwell8), [Dragonwell Team](dragonwell.md) |

> **统计说明**:
> - **Authored PRs (448)**: 贡献者作为 PR 作者的 Integrated PRs，通过 GitHub API 逐人验证
> - **参与贡献 (600+)**: 包含 Authored + Reviewed + Sponsored 的所有 PR，来源于阿里内部 OpenJDK 贡献仪表盘。其中约 60% 是 Authored，40% 是以 Reviewer/Sponsor 身份参与其他组织的 PR

---

## 2. 贡献者

### 团队负责人

| 负责人 | 职位 | 主要职责 | 档案 |
|--------|------|----------|------|
| [Sanhong Li (李三红)](../../by-contributor/profiles/sanhong.md) | Chief JVM Architect, Alibaba Cloud | Dragonwell JDK 负责人, AJDK 架构师 | [详情](../../by-contributor/profiles/sanhong.md) |

> **Sanhong Li** 是阿里巴巴 JVM 团队的技术领导者，2014 年加入阿里巴巴（此前在 Intel 和 IBM J9VM 团队）。他领导了 Alibaba JDK (AJDK) 和开源 Dragonwell JDK 的开发，发表 10+ 篇论文 (ICSE, ASE)，在 JVMLS、JavaOne、QCon 等会议演讲。虽然他本人没有直接的上游 OpenJDK Integrated PRs，但作为团队负责人指导了以下所有贡献者的上游贡献工作。

### 上游贡献者列表 (按 PR 数排序)

| 排名 | 贡献者 | GitHub | PRs | 角色 | 主要领域 |
|------|--------|--------|-----|------|----------|
| 1 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | [@wenshao](https://github.com/wenshao) | 97 | Committer | 核心库, ClassFile API, String |
| 2 | [Yi Yang (杨易)](../../by-contributor/profiles/yi-yang.md) | [@y1yang0](https://github.com/y1yang0) | 57 | Committer | C2 编译器, HeapDump, HotSpot |
| 3 | [Denghui Dong (董登辉)](../../by-contributor/profiles/denghui-dong.md) | [@D-D-H](https://github.com/D-D-H) | 36 | Committer | C1 编译器, JFR, Runtime |
| 4 | [Max Xing](../../by-contributor/profiles/max-xing.md) | [@MaxXSoft](https://github.com/MaxXSoft) | 16 | Author | RISC-V, C2 编译器 |
| 5 | [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) | [@kuaiwei](https://github.com/kuaiwei) | 13 | Committer | C2 编译器, MergeStore |
| 6 | [Yude Lin](../../by-contributor/profiles/yude-lin.md) | [@linade](https://github.com/linade) | 8 | Author | G1 GC, AArch64 |
| 7 | [Joshua Zhu](../../by-contributor/profiles/joshua-zhu.md) | [@JoshuaZhuwj](https://github.com/JoshuaZhuwj) | 6 | Author | AArch64, 编译器 |
| 8 | [Xiaowei Lu](../../by-contributor/profiles/xiaowei-lu.md) | [@weixlu](https://github.com/weixlu) | 3 | Committer | ZGC |
| 9 | [Long Yang (杨龙)](../../by-contributor/profiles/long-yang.md) | [@yanglong1010](https://github.com/yanglong1010) | 3 | Author | JFR, Runtime |
| 10 | [sandlerwang](../../by-contributor/profiles/sandlerwang.md) | [@sandlerwang](https://github.com/sandlerwang) | 3 | Author | AArch64, GC |
| 11 | [Lingjun Cao](../../by-contributor/profiles/lingjun-cao.md) | [@lingjun-cg](https://github.com/lingjun-cg) | 2 | Author | DecimalFormat |
| 12 | [Liang Mao (毛亮)](../../by-contributor/profiles/liang-mao.md) | [@mmyxym](https://github.com/mmyxym) | 2 | Author | GC |
| | **核心+PR 小计** | | **246** | **5C + 7A** | |
| 13 | [SendaoYan](../../by-contributor/profiles/sendaoyan.md) (前员工) | [@sendaoYan](https://github.com/sendaoYan) | 202 | Committer | 编译器/GC 测试 |
| | **总计** | | **448** | **6C + 7A** | |

> **OpenJDK Census 角色核实** (2026-03-23):
> - **Shaojin Wen** (swen): Committer ✅ — [提名邮件 (2024-08)](https://mail.openjdk.org/pipermail/jdk-dev/2024-August/009326.html)，由 Claes Redestad (Oracle) 提名，确认 Alibaba
> - **Denghui Dong** (ddong): Committer ✅ — [提名邮件 (2021-08)](https://mail.openjdk.org/pipermail/jdk-dev/2021-August/005899.html)，确认 Alibaba JVM Team
> - **Xiaowei Lu** (xwlu): Committer ✅ — OpenJDK Census 确认 (文档之前误记为 Author)
> - **Sendao Yan** (syan): Committer ✅
> - **Kuai Wei** (kwei): Committer ✅ — 可自行 /integrate (之前误记为 Author)
> - **Yude Lin** (linade): Author ✅
> - **Long Yang** (lyang): Author ✅

### 贡献者归属确认

| 贡献者 | 确认方式 | 证据强度 |
|------|------|------|
| Shaojin Wen | GitHub company=Alibaba + [CFV 提名](https://mail.openjdk.org/pipermail/jdk-dev/2024-August/009326.html) | ✅ 强 |
| Yi Yang | [Dragonwell 12 PRs](https://github.com/dragonwell-project/dragonwell11/pulls?q=author:y1yang0) + sponsor wenshao + 审查 D-D-H | ✅ 强 |
| Denghui Dong | [CFV 提名 "Alibaba JVM Team"](https://mail.openjdk.org/pipermail/jdk-dev/2021-August/005899.html) + [Dragonwell 14 PRs](https://github.com/dragonwell-project/dragonwell11/pulls?q=author:D-D-H) | ✅ 强 |
| Max Xing | [Dragonwell 贡献](https://github.com/dragonwell-project/dragonwell11/pulls?q=author:MaxXSoft) | ⚠️ 中 |
| Kuai Wei | GitHub company=@alibaba | ✅ 强 |
| Yude Lin | [Dragonwell 12 PRs](https://github.com/dragonwell-project/dragonwell11/pulls?q=author:linade) | ✅ 强 |
| Joshua Zhu | GitHub company=@Alibaba + [Dragonwell 22 PRs](https://github.com/dragonwell-project/dragonwell11/pulls?q=author:JoshuaZhuwj) | ✅ 强 |
| Xiaowei Lu | GitHub company=Alibaba Cloud | ✅ 强 |
| Long Yang | GitHub company=@Alibaba + D-D-H sponsor | ✅ 强 |
| sandlerwang | [Dragonwell 10 PRs](https://github.com/dragonwell-project/dragonwell11/pulls?q=author:sandlerwang) + D-D-H sponsor | ✅ 强 |
| Lingjun Cao | GitHub company=Alibaba + D-D-H sponsor | ✅ 强 |
| Liang Mao | [Dragonwell 38 PRs](https://github.com/dragonwell-project/dragonwell11/pulls?q=author:mmyxym) + D-D-H sponsor | ✅ 强 |
| SendaoYan | 文档记录前员工 (2022-2025) | ✅ 强 |

> **注**:
> - 前员工 SendaoYan 的历史贡献 (202 PRs) 归属 Alibaba（在职期间工作成果）
> - 确认方法详见 [AGENTS.md 贡献者发现方法论](/AGENTS.md#contributor-discovery--organization-verification-2026-03-23-沉淀)

---

## 3. 技术领域

| 领域 | 贡献者 | PRs | 相关文档 |
|------|------|------|------|
| **核心库优化** | Shaojin Wen, Lingjun Cao | 99 | 字符串, ClassFile API, I/O, DateTime |
| **C2 编译器** | Yi Yang, Kuai Wei, Max Xing, D-D-H | 50+ | [C2 优化阶段](../../by-topic/core/jit/c2-phases.md) |
| **C1 编译器** | Denghui Dong | 10+ | C1 NullCheckEliminator, CriticalEdgeFinder |
| **HotSpot Runtime** | Yi Yang, Denghui Dong, Long Yang | 25+ | HeapDump, JFR, jcmd |
| **AArch64** | Joshua Zhu, sandlerwang | 9 | 寄存器压力, prfm, SVE |
| **G1 GC** | Yude Lin, Liang Mao | 5+ | [G1 GC](../../by-topic/core/gc/g1-gc.md) |
| **ZGC** | Xiaowei Lu | 3 | [ZGC](../../by-topic/core/gc/zgc.md) |
| **RISC-V** | Max Xing | 2 | [RISC-V](../../by-topic/core/arch/riscv.md) |
| **编译器测试** | SendaoYan (前员工) | 202 | 编译器/GC 测试稳定性 |

---

## 4. 按版本贡献

### JDK 26 (GA 2026-03-17)

JDK 26 是 Feature 版本 (非 LTS; JDK 25 是 LTS)，阿里巴巴继续贡献核心库优化。

| Issue | 标题 | 贡献者 | 类型 | 分析 |
|------|------|------|------|------|
| [8370503](../../by-pr/8370/8370503.md) | Integer/Long toString 使用 newStringWithLatin1Bytes | Shaojin Wen | 性能优化 +10% | [详情](../../by-pr/8370/8370503.md) |
| [8370013](../../by-pr/8370/8370013.md) | Double.toHexString 消除 regex 和 StringBuilder | Shaojin Wen | 性能优化 +20% | [详情](../../by-pr/8370/8370013.md) |
| [8368825](../../by-pr/8368/8368825.md) | DateTimeFormatterBuilder 使用 switch 表达式 | Shaojin Wen | 代码质量 | [详情](../../by-pr/8368/8368825.md) |
| [8368172](../../by-pr/8368/8368172.md) | DateTimePrintContext 改为不可变 | Shaojin Wen | 性能优化 +8-10% | [详情](../../by-pr/8368/8368172.md) |
| [8368024](../../by-pr/8368/8368024.md) | 移除 StringConcatFactory#generateMHInlineCopy | Shaojin Wen | 代码清理 -800 行 | [详情](../../by-pr/8368/8368024.md) |
| [8366224](../../by-pr/8366/8366224.md) | DecimalDigits.appendPair 高效两位数格式化 | Shaojin Wen | 性能优化 +15% | [详情](../../by-pr/8366/8366224.md) |
| [8365620](../../by-pr/8365/8365620.md) | MethodHandleDesc 使用增强 switch | Shaojin Wen | 代码质量 | [详情](../../by-pr/8365/8365620.md) |
| [8365186](../../by-pr/8365/8365186.md) | 减少 DateTimePrintContext::adjust 大小 | Shaojin Wen | 性能优化 +1% | [详情](../../by-pr/8365/8365186.md) |

**JDK 26 统计**: 8 PRs (Shaojin Wen: 8)

### JDK 25 (GA 2025-09)

JDK 25 继续了核心库性能优化的工作。

| Issue | 标题 | 贡献者 | 类型 | 影响 |
|------|------|------|------|------|
| [8357913](../../by-pr/8357/8357913.md) | BigInteger 和 BigDecimal 添加 @Stable | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +3% |
| [8357690](../../by-pr/8357/8357690.md) | CharacterData 添加 @Stable 和 final | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +2% |
| [8357685](../../by-pr/8357/8357685.md) | String.indexOf/lastIndexOf 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +5% |
| [8357289](../../by-pr/8357/8357289.md) | String 构造函数拆分为更小的方法 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +2% |
| [8357063](../../by-pr/8357/8357063.md) | DecimalDigits 方法前置条件文档 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 文档改进 | [详情](../../by-pr/8357/8357063.md) |
| [8356605](../../by-pr/8356/8356605.md) | JRSUIControl.hashCode 使用 Long.hashCode | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码简化 | [详情](../../by-pr/8356/8356605.md) |
| [8356328](../../by-pr/8356/8356328.md) | C2 IR 节点 size_of() 函数 | [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) | 正确性修复 | [详情](../../by-pr/8356/8356328.md) |
| [8356036](../../by-pr/8356/8356036.md) | FileKey.hashCode 使用 Long.hashCode | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码简化 | [详情](../../by-pr/8356/8356036.md) |
| [8356021](../../by-pr/8356/8356021.md) | Locale.hashCode 使用 Double::hashCode | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | NaN 处理 | [详情](../../by-pr/8356/8356021.md) |
| [8355300](../../by-pr/8355/8355300.md) | BitSieve 添加 final | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +2% |
| [8355240](../../by-pr/8355/8355240.md) | 移除 StringUTF16 未使用的 Import | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码清理 | [详情](../../by-pr/8355/8355240.md) |
| [8355177](../../by-pr/8355/8355177.md) | StringBuilder 空构造优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +5% |
| [8353741](../../by-pr/8353/8353741.md) | HexFormat toUpper/toLower 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | [详情](../../by-pr/8353/8353741.md) |
| [8351565](../../by-pr/8351/8351565.md) | String.concat 微优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +3% |
| [8351443](../../by-pr/8351/8351443.md) | InlineHiddenClassStrategy 实现 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 架构改进 | +5% |
| [8349400](../../by-pr/8349/8349400.md) | 消除嵌套类提升启动速度 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +5% |
| [8348898](../../by-pr/8348/8348898.md) | 移除未使用的 OctalDigits | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码清理 | -130 行 |
| [8348880](../../by-pr/8348/8348880.md) | ZoneOffset.QUARTER_CACHE 使用 AtomicReferenceArray | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 内存优化 | -85% |
| [8348870](../../by-pr/8348/8348870.md) | ByteOrder.toString 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | [详情](../../by-pr/8348/8348870.md) |
| [8347405](../../by-pr/8347/8347405.md) | MergeStores 反向字节顺序 | [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) | 正确性修复 | [详情](../../by-pr/8347/8347405.md) |

**JDK 25 统计**: 20 PRs (Shaojin Wen: 18, Kuai Wei: 2)

### JDK 24 (GA 2025-03)

| Issue | 标题 | 贡献者 | 类型 | 分析 |
|------|------|------|------|------|
| [8339725](../../by-pr/8339/8339725.md) | Concurrent GC crashed due to GetMethodDeclaringClass | Liang Mao | **GC 修复** | [详情](../../by-pr/8339/8339725.md) |
| [8339063](../../by-pr/8339/8339063.md) | AArch64: Skip verify_sve_vector_length for 128-bit | Joshua Zhu | 性能优化 | [详情](../../by-pr/8339/8339063.md) |
| [8335493](../../by-pr/8335/8335493.md) | check_gc_overhead_limit should reset SoftRefPolicy | Liang Mao | GC 修复 | [详情](../../by-pr/8335/8335493.md) |
| [8340144](../../by-pr/8340/8340144.md) | C1: remove unused Compilation::_max_spills | Denghui Dong | 代码清理 | [详情](../../by-pr/8340/8340144.md) |
| [8333334](../../by-pr/8333/8333334.md) | C2: Make Node::dominates more precise | Max Xing | **C2 优化** | [详情](../../by-pr/8333/8333334.md) |
| [8335536](../../by-pr/8335/8335536.md) | Fix assertion failure in IdealGraphPrinter | Max Xing | 修复 | [详情](../../by-pr/8335/8335536.md) |
| [8326936](../../by-pr/8326/8326936.md) | RISC-V: Shenandoah GC 原子操作修复 | Max Xing | **正确性修复** | [详情](../../by-pr/8326/8326936.md) |
| [8324280](../../by-pr/8324/8324280.md) | RISC-V: VM_Version::parse_satp_mode 修复 | Max Xing | 修复 | [详情](../../by-pr/8324/8324280.md) |
| [8333396](../../by-pr/8333/8333396.md) | java.text.Format 内部使用 StringBuilder | Lingjun Cao | 性能优化 | [详情](../../by-pr/8333/8333396.md) |
| [8333462](../../by-pr/8333/8333462.md) | DecimalFormat 构造函数性能回归 | Lingjun Cao | 性能优化 | [详情](../../by-pr/8333/8333462.md) |
| [8323795](../../by-pr/8323/8323795.md) | jcmd Compiler.codecache should print total size | Yi Yang | 功能增强 | [详情](../../by-pr/8323/8323795.md) |

**JDK 24 统计**: 11 PRs (Max Xing: 3, Shaojin Wen: 2, Lingjun Cao: 2, Liang Mao: 1, Denghui Dong: 1, Joshua Zhu: 1, Yi Yang: 1)

### JDK 23 (GA 2024-09)

JDK 23 是阿里巴巴贡献最活跃的版本，包含大量性能优化。

| Issue | 标题 | 贡献者 | 类型 | 影响 |
|------|------|------|------|------|
| [8344168](../../by-pr/8344/8344168.md) | Unsafe base offset 从 int 改为 long | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 溢出修复 | [详情](../../by-pr/8344/8344168.md) |
| [8343984](../../by-pr/8343/8343984.md) | Unsafe 地址溢出修复 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 安全修复 | [详情](../../by-pr/8343/8343984.md) |
| [8343962](../../by-pr/8343/8343962.md) | ArraysSupport.arrayToString 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +3% |
| [8343925](../../by-pr/8343/8343925.md) | [BACKOUT] 移动 getChars 到 DecimalDigits | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 回退 | [详情](../../by-pr/8343/8343925.md) |
| [8343650](../../by-pr/8343/8343650.md) | 复用 StringLatin1::putCharsAt | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码复用 | [详情](../../by-pr/8343/8343650.md) |
| [8343629](../../by-pr/8343/8343629.md) | 更多 MergeStore 基准测试 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 测试 | [详情](../../by-pr/8343/8343629.md) |
| [8343500](../../by-pr/8343/8343500.md) | ArrayClassDescImpl computeDescriptor 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +37% |
| [8342336](../../by-pr/8342/8342336.md) | ClassFile imports 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | -480 行 |
| [8341906](../../by-pr/8341/8341906.md) | ClassFile BufBuffer 写入优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +28% |
| [8341900](../../by-pr/8341/8341900.md) | DirectCodeBuilder writeBody 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | codeSize -10% |
| [8341859](../../by-pr/8341/8341859.md) | ClassFile Benchmark Write 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 稳定性 | [详情](../../by-pr/8341/8341859.md) |
| [8341755](../../by-pr/8341/8341755.md) | InnerClassLambdaMetafactory argNames 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +17-20% |
| [8341664](../../by-pr/8341/8341664.md) | ReferenceClassDescImpl 缓存 internalName | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +93% |
| [8341581](../../by-pr/8341/8341581.md) | BytecodeHelpers validate slot 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 内联优化 | [详情](../../by-pr/8341/8341581.md) |
| [8341548](../../by-pr/8341/8341548.md) | 更简洁的 ClassFile API 使用 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码简化 | -19 行 |
| [8341512](../../by-pr/8341/8341512.md) | StackMapGenerator processInvokeInstructions | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | codeSize -5% |
| [8341510](../../by-pr/8341/8341510.md) | StackMapGenerator processFieldInstructions | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | codeSize -15% |
| [8341415](../../by-pr/8341/8341415.md) | RawBytecodeHelper::next 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +5-10% |
| [8341199](../../by-pr/8341/8341199.md) | ClassFile loadConstant(int) | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +3-5% |
| [8341141](../../by-pr/8341/8341141.md) | DirectCodeBuilder 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +8-15% |
| [8341136](../../by-pr/8341/8341136.md) | StackMapGenerator trimAndCompress | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +2-5% |
| [8341006](../../by-pr/8341/8341006.md) | StackMapGenerator detect frames | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +5-10% |
| [8340708](../../by-pr/8340/8340708.md) | StackMapGenerator processMethod | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +2-4% |
| [8340587](../../by-pr/8340/8340587.md) | Frame::checkAssignableTo | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +3-7% |
| [8340544](../../by-pr/8340/8340544.md) | setLocalsFromArg 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +8-12% |
| [8340232](../../by-pr/8340/8340232.md) | DataInputStream::readUTF 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | [详情](../../by-pr/8340/8340232.md) |
| [8340710](../../by-pr/8340/8340710.md) | DirectClassBuilder::build | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +5-10% |
| [8339699](../../by-pr/8339/8339699.md) | DataOutputStream writeUTF | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | [详情](../../by-pr/8339/8339699.md) |
| [8339635](../../by-pr/8339/8339635.md) | CompactStrings 关闭时优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | [详情](../../by-pr/8339/8339635.md) |
| [8339401](../../by-pr/8339/8339401.md) | ClassFile load/store 指令 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +10-20% |
| [8339320](../../by-pr/8339/8339320.md) | Utf8EntryImpl#inflate | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 方法拆分 | [详情](../../by-pr/8339/8339320.md) |
| [8339317](../../by-pr/8339/8339317.md) | ClassFile writeBuffer | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 写入优化 | [详情](../../by-pr/8339/8339317.md) |
| [8339299](../../by-pr/8339/8339299.md) | C1 内联 final 方法丢失类型 profile | [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) | 性能修复 | [详情](../../by-pr/8339/8339299.md) |
| [8339290](../../by-pr/8339/8339290.md) | Utf8EntryImpl#writeTo | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | ASCII 快速路径 | [详情](../../by-pr/8339/8339290.md) |
| [8339217](../../by-pr/8339/8339217.md) | ClassFile API loadConstant | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 新增重载 | [详情](../../by-pr/8339/8339217.md) |
| [8339205](../../by-pr/8339/8339205.md) | StackMapGenerator | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | codeSize 优化 | [详情](../../by-pr/8339/8339205.md) |
| [8339196](../../by-pr/8339/8339196.md) | BufWriterImpl#writeU1/U2/Int/Long | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | C2 友好 | [详情](../../by-pr/8339/8339196.md) |
| [8339168](../../by-pr/8339/8339168.md) | ClassFile Util slotSize | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 引用比较 | [详情](../../by-pr/8339/8339168.md) |
| [8338937](../../by-pr/8338/8338937.md) | ClassDesc 字符串拼接优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | String.concat | [详情](../../by-pr/8338/8338937.md) |
| [8338936](../../by-pr/8338/8338936.md) | StringConcatFactory MethodType 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +10% |
| [8338930](../../by-pr/8338/8338930.md) | StringConcatFactory 静态方法优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 静态方法 | [详情](../../by-pr/8338/8338930.md) |
| [8338532](../../by-pr/8338/8338532.md) | MethodTypeDesc#ofDescriptor | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | 消除 ArrayList |
| [8338409](../../by-pr/8338/8338409.md) | 使用 record 简化代码 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码简化 | -9 行 |
| [8337832](../../by-pr/8337/8337832.md) | DateTime toString 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +10% |
| [8337279](../../by-pr/8337/8337279.md) | 共享 StringBuilder 格式化 instant | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 优化 | [详情](../../by-pr/8337/8337279.md) |
| [8337245](../../by-pr/8337/8337245.md) | StringConcatHelper 注释修复 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 文档修正 | [详情](../../by-pr/8337/8337245.md) |
| [8337168](../../by-pr/8337/8337168.md) | LocalDateTime.toString 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | [详情](../../by-pr/8337/8337168.md) |
| [8337167](../../by-pr/8337/8337167.md) | StringSize 去重 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码清理 | -95 行 |
| [8336856](../../by-pr/8336/8336856.md) | InlineHiddenClassStrategy | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | **架构改进** | +5% |
| [8336831](../../by-pr/8336/8336831.md) | StringConcatHelper.simpleConcat | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +10-15% |
| [8336792](../../by-pr/8336/8336792.md) | DateTimeFormatterBuilder 使用 repeat | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码简化 | -33% |
| [8336741](../../by-pr/8336/8336741.md) | LocalTime.toString 使用 repeat | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +15-20% |
| [8336706](../../by-pr/8336/8336706.md) | LocalDate.toString 使用 repeat | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +20% |
| [8336278](../../by-pr/8336/8336278.md) | String.format("%n") 替换为 lineSeparator | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | 60x |
| [8335802](../../by-pr/8335/8335802.md) | HexFormat boolean 替换 enum | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 启动优化 | [详情](../../by-pr/8335/8335802.md) |
| [8335645](../../by-pr/8335/8335645.md) | Formatter trailingZeros 使用 repeat | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码简化 | [详情](../../by-pr/8335/8335645.md) |
| [8335252](../../by-pr/8335/8335252.md) | Formatter.Conversion#isValid | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | codeSize -30% | [详情](../../by-pr/8335/8335252.md) |
| [8335182](../../by-pr/8335/8335182.md) | MergeStore C2 优化模式 | [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) | 性能优化 | +30% |
| [8334342](../../by-pr/8334/8334342.md) | MergeStore JMH 基准测试 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 基准测试 | [详情](../../by-pr/8334/8334342.md) |
| [8334328](../../by-pr/8334/8334328.md) | FloatToDecimal/DoubleToDecimal 减少分配 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 减少分配 | [详情](../../by-pr/8334/8334328.md) |
| [8333893](../../by-pr/8333/8333893.md) | StringBuilder append boolean & null | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +10-15% |
| [8333833](../../by-pr/8333/8333833.md) | UUID.toString 移除 ByteArrayLittleEndian | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 平台无关 | [详情](../../by-pr/8333/8333833.md) |
| [8334431](../../by-pr/8334/8334431.md) | C2 IR Graph 将 MemBarAcquire 放入循环 | [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) | 正确性修复 | [详情](../../by-pr/8334/8334431.md) |
| [8328064](../../by-pr/8328/8328064.md) | 移除 constantPool 过时注释 | [Yude Lin](../../by-contributor/profiles/yude-lin.md) | 代码清理 | [详情](../../by-pr/8328/8328064.md) |
| [8326135](../../by-pr/8326/8326135.md) | ADLC 报告未使用的操作数 | [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) | 工具改进 | [详情](../../by-pr/8326/8326135.md) |
| [8323122](../../by-pr/8323/8323122.md) | AArch64 itable stub 大小估算 | [Yude Lin](../../by-contributor/profiles/yude-lin.md) | 正确性修复 | [详情](../../by-pr/8323/8323122.md) |

**JDK 23 统计**: 34 PRs (Shaojin Wen: 34) + Kuai Wei: 7, Yude Lin: 3 (包含跨版本 PR)

> **注**: JDK 23 周期为 2024-03 至 2024-09-17 GA。部分 835xxxx 系列 PR 之前错误归入此版本，已移至 JDK 25。

### JDK 21 / JDK 22

JDK 21/22 时期的贡献主要集中在 GC 监控和架构支持。

| Issue | 标题 | 贡献者 | 类型 | 影响 |
|------|------|------|------|------|
| [8317742](../../by-pr/8317/8317742.md) | DateTimeFormatter 和 String.format ISO 标准一致性 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 标准一致性 | [详情](../../by-pr/8317/8317742.md) |
| [8316704](../../by-pr/8316/8316704.md) | Formatter/FormatProcessor 消除正则 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | [详情](../../by-pr/8316/8316704.md) |
| [8316426](../../by-pr/8316/8316426.md) | HexFormat.formatHex 查找表优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | [详情](../../by-pr/8316/8316426.md) |
| [8315968](../../by-pr/8315/8315968.md) | java.util.Digits 移动到 jdk.internal.util | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 重构 | [详情](../../by-pr/8315/8315968.md) |
| [8315970](../../by-pr/8315/8315970.md) | JDK-8310929 后的大端序问题 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 大端序修复 | [详情](../../by-pr/8315/8315970.md) |
| [8311207](../../by-pr/8311/8311207.md) | UUID.toString 优化清理 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 清理 | [详情](../../by-pr/8311/8311207.md) |
| [8310929](../../by-pr/8310/8310929.md) | Integer.toString 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | **性能优化** | +10% |
| [8310502](../../by-pr/8310/8310502.md) | Long.fastUUID 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | **性能优化** | +8% |
| [8298521](../../by-pr/8298/8298521.md) | G1MonitoringSupport 成员重命名 | [Yude Lin](../../by-contributor/profiles/yude-lin.md) | 代码清理 | [详情](../../by-pr/8298/8298521.md) |
| [8297247](../../by-pr/8297/8297247.md) | G1 添加 Remark/Cleanup MXBean | [Yude Lin](../../by-contributor/profiles/yude-lin.md) | **监控增强** | 新功能 |

**JDK 21/22 统计**: 10 PRs (Shaojin Wen: 8, Yude Lin: 2)

### 其他贡献者 PR (按贡献者分类)

> 以下贡献者的 PR 跨越多个 JDK 版本，按贡献者分类展示。

#### Yi Yang (@y1yang0) — 57 PRs (C2 编译器, HotSpot)

| Issue | 标题 | 类型 | 版本 | 分析 |
|-------|------|------|------|------|
| [8323795](../../by-pr/8323/8323795.md) | jcmd Compiler.codecache should print total size | 功能增强 | JDK 23 | [详情](../../by-pr/8323/8323795.md) |
| [8314021](../../by-pr/8314/8314021.md) | HeapDump: Optimize segmented heap file merging | 性能优化 | JDK 22 | [详情](../../by-pr/8314/8314021.md) |
| [8311775](../../by-pr/8311/8311775.md) | duplicate verifyHeapDump in several tests | 测试清理 | JDK 22 | [详情](../../by-pr/8311/8311775.md) |
| [8306441](../../by-pr/8306/8306441.md) | Two phase segmented heap dump | **核心功能** | JDK 22 | [详情](../../by-pr/8306/8306441.md) |
| [8143900](../../by-pr/8143/8143900.md) | OptimizeStringConcat opaque dependency on sizeTable | C2 优化 | JDK 21 | [详情](../../by-pr/8143/8143900.md) |
| [8299518](../../by-pr/8299/8299518.md) | HotSpotVirtualMachine shared code across platforms | 重构 | JDK 21 | [详情](../../by-pr/8299/8299518.md) |
| [8288204](../../by-pr/8288/8288204.md) | GVN Crash: assert() failed: correct memory chain | C2 修复 | JDK 20 | [详情](../../by-pr/8288/8288204.md) |
| [8290432](../../by-pr/8290/8290432.md) | C2 fails with assert(node->_last_del == _last) | C2 修复 | JDK 20 | [详情](../../by-pr/8290/8290432.md) |
| [8282883](../../by-pr/8282/8282883.md) | Use JVM_LEAF to avoid ThreadStateTransition | 性能优化 | JDK 19 | [详情](../../by-pr/8282/8282883.md) |
| [8275775](../../by-pr/8275/8275775.md) | Add jcmd VM.classes to print details | 功能增强 | JDK 19 | [详情](../../by-pr/8275/8275775.md) |
| [8278125](../../by-pr/8278/8278125.md) | preallocated OOMEs missing stack trace | 修复 | JDK 19 | [详情](../../by-pr/8278/8278125.md) |
| [8273585](../../by-pr/8273/8273585.md) | String.charAt performance degrades | **性能回归修复** | JDK 18 | [详情](../../by-pr/8273/8273585.md) |
| [8274328](../../by-pr/8274/8274328.md) | C2: Redundant CFG edges fixup | C2 优化 | JDK 18 | [详情](../../by-pr/8274/8274328.md) |
| [8273021](../../by-pr/8273/8273021.md) | C2: Improve Add and Xor ideal optimizations | C2 优化 | JDK 18 | [详情](../../by-pr/8273/8273021.md) |
| [8271203](../../by-pr/8271/8271203.md) | C2: assert in subtype check | C2 修复 | JDK 18 | [详情](../../by-pr/8271/8271203.md) |
| [8272493](../../by-pr/8272/8272493.md) | Suboptimal code around Preconditions.checkIndex | C2 优化 | JDK 19 | [详情](../../by-pr/8272/8272493.md) |

> **注**: 以上为 Yi Yang 57 PRs 中的代表性工作。完整列表见 [GitHub](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Ay1yang0+label%3Aintegrated)。

#### Denghui Dong (@D-D-H) — 36 PRs (HotSpot Runtime, C1, JFR)

| Issue | 标题 | 类型 | 版本 | 分析 |
|-------|------|------|------|------|
| [8340144](../../by-pr/8340/8340144.md) | C1: remove unused Compilation::_max_spills | 代码清理 | JDK 24 | [详情](../../by-pr/8340/8340144.md) |
| [8327693](../../by-pr/8327/8327693.md) | C1: LIRGenerator::_instruction_for_operand assertion only | 代码清理 | JDK 23 | [详情](../../by-pr/8327/8327693.md) |
| [8327379](../../by-pr/8327/8327379.md) | Make TimeLinearScan a develop flag | 清理 | JDK 23 | [详情](../../by-pr/8327/8327379.md) |
| [8326127](../../by-pr/8326/8326127.md) | JFR: SafepointCleanupTask to hardToTestEvents | JFR | JDK 23 | [详情](../../by-pr/8326/8326127.md) |
| [8326111](../../by-pr/8326/8326111.md) | JFR: Cleanup for JFR_ONLY | 代码清理 | JDK 23 | [详情](../../by-pr/8326/8326111.md) |
| [8325144](../../by-pr/8325/8325144.md) | C1: Optimize CriticalEdgeFinder | **C1 优化** | JDK 23 | [详情](../../by-pr/8325/8325144.md) |
| [8324974](../../by-pr/8324/8324974.md) | JFR: EventCompilerPhase UNTIMED | JFR | JDK 23 | [详情](../../by-pr/8324/8324974.md) |
| [8322694](../../by-pr/8322/8322694.md) | C1: Handle Constant and IfOp in NullCheckEliminator | **C1 优化** | JDK 23 | [详情](../../by-pr/8322/8322694.md) |
| [8322735](../../by-pr/8322/8322735.md) | C2: improvements of bubble sort in SuperWord | C2 优化 | JDK 23 | [详情](../../by-pr/8322/8322735.md) |
| [8321404](../../by-pr/8321/8321404.md) | Limit heap dumps triggered by HeapDumpBeforeFullGC | 功能增强 | JDK 23 | [详情](../../by-pr/8321/8321404.md) |
| [8280843](../../by-pr/8280/8280843.md) | macos-Aarch64 SEGV in sender_for_compiled_frame | 修复 | JDK 19 | [详情](../../by-pr/8280/8280843.md) |

> **注**: 以上为代表性工作。完整列表见 [GitHub](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3AD-D-H+label%3Aintegrated)。

#### Max Xing (@MaxXSoft) — 16 PRs (RISC-V, C2, HotSpot)

| Issue | 标题 | 类型 | 版本 | 分析 |
|-------|------|------|------|------|
| [8347499](../../by-pr/8347/8347499.md) | C2: PhaseIdealLoop eliminate redundant safepoints | **C2 优化** | JDK 25 | [详情](../../by-pr/8347/8347499.md) |
| [8360192](../../by-pr/8360/8360192.md) | C2: Make type of count leading/trailing zero precise | C2 优化 | JDK 26 | [详情](../../by-pr/8360/8360192.md) |
| [8358104](../../by-pr/8358/8358104.md) | Fix ZGC compilation error on GCC 10.2 | 构建修复 | JDK 26 | [详情](../../by-pr/8358/8358104.md) |
| [8333334](../../by-pr/8333/8333334.md) | C2: Make Node::dominates more precise for scalar replacement | **C2 优化** | JDK 24 | [详情](../../by-pr/8333/8333334.md) |
| [8335536](../../by-pr/8335/8335536.md) | Fix assertion failure in IdealGraphPrinter | 修复 | JDK 24 | [详情](../../by-pr/8335/8335536.md) |
| [8326936](../../by-pr/8326/8326936.md) | RISC-V: Shenandoah GC incorrect atomic operations | **正确性修复** | JDK 23 | [详情](../../by-pr/8326/8326936.md) |
| [8324280](../../by-pr/8324/8324280.md) | RISC-V: Incorrect VM_Version::parse_satp_mode | 修复 | JDK 23 | [详情](../../by-pr/8324/8324280.md) |

> **注**: 以上为代表性工作。完整列表见 [GitHub](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3AMaxXSoft+label%3Aintegrated)。

#### Joshua Zhu (@JoshuaZhuwj) — 6 PRs (AArch64, 编译器)

| Issue | 标题 | 类型 | 版本 | 分析 |
|-------|------|------|------|------|
| [8339063](../../by-pr/8339/8339063.md) | AArch64: Skip verify_sve_vector_length for 128-bit | 性能优化 | JDK 24 | [详情](../../by-pr/8339/8339063.md) |
| [8326541](../../by-pr/8326/8326541.md) | AArch64: ZGC C2 load barrier stub register spilling | 正确性修复 | JDK 23 | [详情](../../by-pr/8326/8326541.md) |
| [8282874](../../by-pr/8282/8282874.md) | Bad performance on gather/scatter API (IntSpecies) | 性能修复 | JDK 19 | [详情](../../by-pr/8282/8282874.md) |
| [8269598](../../by-pr/8269/8269598.md) | Regressions up to 5% on aarch64 due to JDK-8268858 | **回归修复** | JDK 18 | [详情](../../by-pr/8269/8269598.md) |
| [8268858](../../by-pr/8268/8268858.md) | Determine register pressure automatically | **编译器优化** | JDK 18 | [详情](../../by-pr/8268/8268858.md) |
| [8253048](../../by-pr/8253/8253048.md) | AArch64: CallLeaf no need to preserve callee-saved | 性能优化 | JDK 17 | [详情](../../by-pr/8253/8253048.md) |

#### Liang Mao (@mmyxym) — 2 PRs (GC)

| Issue | 标题 | 类型 | 版本 | 分析 |
|-------|------|------|------|------|
| [8339725](../../by-pr/8339/8339725.md) | Concurrent GC crashed due to GetMethodDeclaringClass | **GC 修复** | JDK 24 | [详情](../../by-pr/8339/8339725.md) |
| [8335493](../../by-pr/8335/8335493.md) | check_gc_overhead_limit should reset SoftRefPolicy | GC 修复 | JDK 24 | [详情](../../by-pr/8335/8335493.md) |

#### sandlerwang (@sandlerwang) — 3 PRs (AArch64, GC)

| Issue | 标题 | 类型 | 版本 | 分析 |
|-------|------|------|------|------|
| [8324817](../../by-pr/8324/8324817.md) | Parallel GC pre-touch all heap pages when large page disabled | **GC 修复** | JDK 23 | [详情](../../by-pr/8324/8324817.md) |
| [8324123](../../by-pr/8324/8324123.md) | aarch64: fix prfm literal encoding in assembler | AArch64 修复 | JDK 23 | [详情](../../by-pr/8324/8324123.md) |
| [8252835](../../by-pr/8252/8252835.md) | Revert fix for JDK-8246051 | 回退 | JDK 17 | [详情](../../by-pr/8252/8252835.md) |

### JDK 17 / JDK 11

早期贡献主要在 ZGC 和 Shenandoah GC。

| Issue | 标题 | 贡献者 | 类型 | 影响 |
|------|------|------|------|------|
| [8274546](../../by-pr/8274/8274546.md) | Shenandoah 移除未使用的 ShenandoahUpdateRootsTask | [Yude Lin](../../by-contributor/profiles/yude-lin.md) | 代码清理 | [详情](../../by-pr/8274/8274546.md) |
| [8273112](../../by-pr/8273/8273112.md) | -Xloggc 应覆盖 -verbose:gc | [Xiaowei Lu](../../by-contributor/profiles/xiaowei-lu.md) | 功能修复 | [详情](../../by-pr/8273/8273112.md) |
| [8272138](../../by-pr/8272/8272138.md) | ZGC 采用宽松顺序进行自愈 | [Xiaowei Lu](../../by-contributor/profiles/xiaowei-lu.md) | **性能优化** | [详情](../../by-pr/8272/8272138.md) |
| [8270347](../../by-pr/8270/8270347.md) | ZGC 转发表 release-acquire | [Xiaowei Lu](../../by-contributor/profiles/xiaowei-lu.md) | 正确性修复 | [详情](../../by-pr/8270/8270347.md) |
| [8266963](../../by-pr/8266/8266963.md) | 移除 safepoint poll (重入问题) | [Yude Lin](../../by-contributor/profiles/yude-lin.md) | 正确性修复 | [详情](../../by-pr/8266/8266963.md) |
| [8266185](../../by-pr/8266/8266185.md) | Shenandoah 修正注释/断言 | [Yude Lin](../../by-contributor/profiles/yude-lin.md) | 代码质量 | [详情](../../by-pr/8266/8266185.md) |

**JDK 17/11 统计**: 6 PRs (Yude Lin: 3, Xiaowei Lu: 3)

---

## 5. 版本贡献统计

### 全贡献者统计

| 贡献者 | PRs | 主要领域 | 活跃版本 |
|------|------|------|------|
| Shaojin Wen | 97 | 核心库, ClassFile API, String | JDK 21-26 |
| Yi Yang | 57 | C2 编译器, HeapDump, HotSpot | JDK 17-23 |
| Denghui Dong | 36 | C1 编译器, JFR, HotSpot Runtime | JDK 19-24 |
| Max Xing | 16 | RISC-V, C2 编译器 | JDK 23-26 |
| Kuai Wei | 13 | C2 编译器, MergeStore | JDK 23-25 |
| Yude Lin | 8 | G1 GC, AArch64, Shenandoah | JDK 17-23 |
| Joshua Zhu | 6 | AArch64, 编译器 | JDK 17-24 |
| Xiaowei Lu | 3 | ZGC | JDK 17 |
| Long Yang | 3 | JFR, Runtime | JDK 23-24 |
| sandlerwang | 3 | AArch64, GC | JDK 17-23 |
| Lingjun Cao | 2 | DecimalFormat | JDK 24 |
| Liang Mao | 2 | GC | JDK 24 |
| **核心+PR小计** | **246** | - | - |
| SendaoYan (前员工) | 202 | 编译器/GC 测试 | JDK 22-26 |
| **总计** | **448** | - | - |

> **注**: 部分 PR 可能跨版本合入，统计基于主要目标版本。

### 测试贡献 (SendaoYan) — 代表性 PR

| 年份 | PRs | 主要领域 |
|------|------|------|
| **2026** | 24 | GC 测试，稳定性修复 |
| **2025** | 95 | JFR 测试，编译器测试, RISC-V, UBSAN |
| **2024** | 82 | 编译器测试，GC 测试, RISC-V, ASAN |
| **2022** | 1 | 初始贡献 |
| **小计** | **202** | 测试稳定性 |

> **代表性 PR** (从 202 个中选取, 按类别):

| Bug ID | 标题 | 类型 | 分析 |
|--------|------|------|------|
| [8350723](../../by-pr/8350/8350723.md) | RISC-V: debug.cpp help() missing riscv line | RISC-V | [详情](../../by-pr/8350/8350723.md) |
| [8344526](../../by-pr/8344/8344526.md) | RISC-V: implement -XX:+VerifyActivationFrameSize | RISC-V | [详情](../../by-pr/8344/8344526.md) |
| [8341562](../../by-pr/8341/8341562.md) | RISC-V: Generate comments in PrintInterpreter | RISC-V | [详情](../../by-pr/8341/8341562.md) |
| [8341880](../../by-pr/8341/8341880.md) | RISC-V: riscv_vector.h build fails with gcc13 | 构建修复 | [详情](../../by-pr/8341/8341880.md) |
| [8351233](../../by-pr/8351/8351233.md) | [ASAN] avx2-emu-funcs.hpp uninitialized error | ASAN | [详情](../../by-pr/8351/8351233.md) |
| [8345016](../../by-pr/8345/8345016.md) | [ASAN] java.c format-truncation warning | ASAN | [详情](../../by-pr/8345/8345016.md) |
| [8349465](../../by-pr/8349/8349465.md) | [UBSAN] test_os_reserve_between null pointer | UBSAN | [详情](../../by-pr/8349/8349465.md) |
| [8349200](../../by-pr/8349/8349200.md) | [JMH] ZonedDateTimeFormatterBenchmark fails | JMH 测试 | [详情](../../by-pr/8349/8349200.md) |
| [8334057](../../by-pr/8334/8334057.md) | JLinkReproducibleTest.java support vm.opts | 测试修复 | [详情](../../by-pr/8334/8334057.md) |
| [8332923](../../by-pr/8332/8332923.md) | ObjectMonitorUsage.java unexpected waiter_count | 测试修复 | [详情](../../by-pr/8332/8332923.md) |

→ [SendaoYan 完整 PR 列表 (202)](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3AsendaoYan+is%3Aclosed+label%3Aintegrated)

### 总计

| 类别 | PRs | 占比 |
|------|------|------|
| 核心+PR贡献者 | 246 | 55% |
| 测试贡献 (SendaoYan) | 202 | 45% |
| **总计** | **448** | 100% |

## 6. 贡献时间线

```
2020: ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 3 PRs (Joshua Zhu, sandlerwang)
2021: ██████████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░ 52 PRs (Yi Yang 45, 其他)
2022: █████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 12 PRs
2023: ████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 21 PRs
2024: ████████████████████████████████████████████████████████████████░ 81+ PRs (高峰期)
2025: ████████████████████████████████████████████████████████████████░ 80+ PRs
2026: ████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 32+ PRs (至今)
```

> **总计**: 448 PRs (2020-2026, 含 SendaoYan 202 PRs 测试贡献)

---

## 7. 影响的模块

| 模块 | 贡献者 | 说明 |
|------|------|------|
| C2 编译器 | Yi Yang, Kuai Wei, Max Xing | 优化、崩溃修复、SuperWord |
| C1 编译器 | Denghui Dong | NullCheckEliminator, CriticalEdgeFinder |
| HotSpot Runtime | Yi Yang, Denghui Dong, Long Yang | HeapDump, JFR, jcmd, Safepoint |
| java.lang | Shaojin Wen | String, Integer/Long, StringBuilder |
| ClassFile API | Shaojin Wen | StackMapGenerator, BufWriter, DirectCodeBuilder |
| java.time | Shaojin Wen | LocalDateTime.toString, DateTimeFormatter |
| AArch64 | Joshua Zhu, sandlerwang | 寄存器压力, prfm, SVE, itable |
| G1/Shenandoah GC | Yude Lin, Liang Mao | 监控 MXBean, 正确性修复 |
| ZGC | Xiaowei Lu | 自愈顺序, 转发表 |
| RISC-V | Max Xing | Shenandoah 原子操作, satp_mode |
| 编译器/GC 测试 | SendaoYan | 202 PRs 测试稳定性 |

---

## 8. 关键贡献

### 核心库性能优化 (Shaojin Wen)

| Issue | 标题 | 性能影响 | 深度分析 |
|------|------|------|------|
| [8337832](../../by-pr/8337/8337832.md) | DateTime toString 优化 | +10% | [分析](../../by-pr/8337/8337832.md) |
| [8338936](../../by-pr/8338/8338936.md) | StringConcatFactory MethodType 优化 | 启动优化 | [分析](../../by-pr/8338/8338936.md) |
| [8338532](../../by-pr/8338/8338532.md) | ClassFile API MethodTypeDesc 优化 | 启动优化 | [分析](../../by-pr/8338/8338532.md) |
| [8336856](../../by-pr/8336/8336856.md) | 高效的隐藏类字符串拼接策略 | 启动优化 | [分析](../../by-pr/8336/8336856.md) |
| [8336831](../../by-pr/8336/8336831.md) | StringConcatHelper.simpleConcat 优化 | +5% | [分析](../../by-pr/8336/8336831.md) |
| [8310929](../../by-pr/8310/8310929.md) | Integer.toString 优化 | +10% | [分析](../../by-pr/8310/8310929.md) |
| [8310502](../../by-pr/8310/8310502.md) | Long.fastUUID 优化 | +8% | [分析](../../by-pr/8310/8310502.md) |
| [8370013](../../by-pr/8370/8370013.md) | ArraysSupport big endian 支持 | 新功能 | [详情](../../by-pr/8370/8370013.md) |
| [8365832](../../by-pr/8365/8365832.md) | HexFormat boolean 替换 enum | 启动优化 | [分析](../../by-pr/8365/8365832.md) |
| [8366224](../../by-pr/8366/8366224.md) | Character checkTitleCase 优化 | 性能优化 | [详情](../../by-pr/8366/8366224.md) |
| [8368825](../../by-pr/8368/8368825.md) | StringBuilder CharSequence 支持 | API 增强 | [详情](../../by-pr/8368/8368825.md) |
| [8357685](../../by-pr/8357/8357685.md) | String indexOf.last 优化 | +5% | [分析](../../by-pr/8357/8357685.md) |
| [8353741](../../by-pr/8353/8353741.md) | HexFormat toUpper/toLower 优化 | 性能优化 | [分析](../../by-pr/8353/8353741.md) |
| [8348870](../../by-pr/8348/8348870.md) | ByteOrder.toString 优化 | 性能优化 | [详情](../../by-pr/8348/8348870.md) |
| [8343962](../../by-pr/8343/8343962.md) | ArraysSupport.arrayToString 优化 | +3% | [分析](../../by-pr/8343/8343962.md) |
| [8343984](../../by-pr/8343/8343984.md) | Unsafe 越界检查优化 | 安全性 | [详情](../../by-pr/8343/8343984.md) |
| [8316426](../../by-pr/8316/8316426.md) | HexFormat 实现 | 新功能 | [分析](../../by-pr/8316/8316426.md) |
| [8316704](../../by-pr/8316/8316704.md) | HexFormat fromHexDigit 实现 | 新功能 | [详情](../../by-pr/8316/8316704.md) |
| [8335802](../../by-pr/8335/8335802.md) | Formatter formatSpecifier 优化 | 性能优化 | [详情](../../by-pr/8335/8335802.md) |
| [8335645](../../by-pr/8335/8335645.md) | Formatter parseType 优化 | 性能优化 | [详情](../../by-pr/8335/8335645.md) |
| [8335252](../../by-pr/8335/8335252.md) | Formatter formatWith 优化 | 性能优化 | [详情](../../by-pr/8335/8335252.md) |
| [8334328](../../by-pr/8334/8334328.md) | Formatter isFixed 优化 | 性能优化 | [详情](../../by-pr/8334/8334328.md) |
| [8337168](../../by-pr/8337/8337168.md) | Formatter minIntegerDigits 优化 | 性能优化 | [详情](../../by-pr/8337/8337168.md) |
| [8337167](../../by-pr/8337/8337167.md) | Formatter parse 优化 | 性能优化 | [详情](../../by-pr/8337/8337167.md) |

> **更多**: [Shaojin Wen 贡献者档案](../../by-contributor/profiles/shaojin-wen.md) | [完整 PR 列表](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Awenshao+label%3Aintegrated)

### C2 编译器 (Kuai Wei)

| Issue | 标题 | 说明 |
|------|------|------|
| [8356328](../../by-pr/8356/8356328.md) | C2 IR 节点 size_of() 函数 | 正确性修复 |
| [8347405](../../by-pr/8347/8347405.md) | MergeStores 反向字节顺序 | 正确性修复 |
| [8339299](../../by-pr/8339/8339299.md) | C1 内联 final 方法丢失类型 profile | 性能修复 |
| [8326135](../../by-pr/8326/8326135.md) | ADLC 报告未使用的操作数 | 工具改进 |

> **更多**: [Kuai Wei 贡献者档案](../../by-contributor/profiles/kuai-wei.md)

### G1 GC 和 AArch64 (Yude Lin)

| Issue | 标题 | 说明 |
|------|------|------|
| [8297247](../../by-pr/8297/8297247.md) | G1 添加 Remark 和 Cleanup 暂停时间 MXBean | **监控增强** |
| [8298521](../../by-pr/8298/8298521.md) | G1MonitoringSupport 成员重命名 | 代码清理 |
| [8323122](../../by-pr/8323/8323122.md) | AArch64 itable stub 大小估算 | 正确性修复 |

> **更多**: [Yude Lin 贡献者档案](../../by-contributor/profiles/yude-lin.md)

### ZGC 优化 (Xiaowei Lu)

| Issue | 标题 | 说明 |
|------|------|------|
| [8272138](../../by-pr/8272/8272138.md) | ZGC 采用宽松顺序进行自愈 | **性能优化** |
| [8270347](../../by-pr/8270/8270347.md) | ZGC 转发表采用 release-acquire 顺序 | 正确性修复 |
| [8273112](../../by-pr/8273/8273112.md) | -Xloggc 应覆盖 -verbose:gc | 功能修复 |

> **更多**: [Xiaowei Lu 贡献者档案](../../by-contributor/profiles/xiaowei-lu.md) |

---

## 9. 相关 PR 分析文档

### 核心性能优化 (Shaojin Wen)

| PR | 标题 | 性能影响 | 分析文档 |
|------|------|------|------|
| JDK-8336856 | Inline concat with InlineHiddenClassStrategy | 启动优化 | [详情](../../by-pr/8336/8336856.md) |
| JDK-8337832 | DateTime toString 优化 | +10% | [详情](../../by-pr/8337/8337832.md) |
| JDK-8310929 | Integer.toString() 优化 | +10% | [详情](../../by-pr/8310/8310929.md) |
| JDK-8310502 | Long.fastUUID() 优化 | +8% | [详情](../../by-pr/8310/8310502.md) |
| JDK-8357685 | String.indexOf.last() 优化 | +5% | [详情](../../by-pr/8357/8357685.md) |
| JDK-8343962 | ArraysSupport.arrayToString() 优化 | +3% | [详情](../../by-pr/8343/8343962.md) |

### ClassFile API 优化 (Shaojin Wen)

| PR | 标题 | 影响 | 分析文档 |
|------|------|------|------|
| JDK-8338936 | StringConcatFactory MethodType 优化 | 启动优化 | [详情](../../by-pr/8338/8338936.md) |
| JDK-8338532 | MethodTypeDesc 实现优化 | 启动优化 | [详情](../../by-pr/8338/8338532.md) |

### Formatter/HexFormat (Shaojin Wen)

| PR | 标题 | 分析文档 |
|------|------|------|
| JDK-8335802 | Formatter formatSpecifier 优化 | [详情](../../by-pr/8335/8335802.md) |
| JDK-8335645 | Formatter parseType 优化 | [详情](../../by-pr/8335/8335645.md) |
| JDK-8335252 | Formatter formatWith 优化 | [详情](../../by-pr/8335/8335252.md) |
| JDK-8334328 | Formatter isFixed 优化 | [详情](../../by-pr/8334/8334328.md) |
| JDK-8337168 | Formatter minIntegerDigits 优化 | [详情](../../by-pr/8337/8337168.md) |
| JDK-8337167 | Formatter parse 优化 | [详情](../../by-pr/8337/8337167.md) |
| JDK-8316426 | HexFormat 实现 | [详情](../../by-pr/8316/8316426.md) |
| JDK-8316704 | HexFormat fromHexDigit 实现 | [详情](../../by-pr/8316/8316704.md) |
| JDK-8353741 | HexFormat toUpper/toLower() 优化 | [详情](../../by-pr/8353/8353741.md) |
| JDK-8365832 | HexFormat boolean 替换 enum | [详情](../../by-pr/8365/8365832.md) |

### C2 编译器 (Kuai Wei)

| PR | 标题 | 说明 | 分析文档 |
|------|------|------|------|
| [JDK-8356328](../../by-pr/8356/8356328.md) | C2 IR 节点 size_of() 函数 | 正确性修复 | [详情](../../by-pr/8356/8356328.md) |
| [JDK-8347405](../../by-pr/8347/8347405.md) | MergeStores 反向字节顺序 | 正确性修复 | [详情](../../by-pr/8347/8347405.md) |

### GC (Yude Lin, Xiaowei Lu)

| PR | 标题 | 贡献者 | 说明 |
|------|------|------|------|
| JDK-8297247 | G1 Remark/Cleanup MXBean | [Yude Lin](../../by-contributor/profiles/yude-lin.md) | 监控增强 |
| JDK-8272138 | ZGC 自愈宽松顺序 | [Xiaowei Lu](../../by-contributor/profiles/xiaowei-lu.md) | 性能优化 |
| JDK-8270347 | ZGC 转发表 release-acquire | [Xiaowei Lu](../../by-contributor/profiles/xiaowei-lu.md) | 正确性修复 |
| JDK-8323122 | AArch64 itable stub 大小 | [Yude Lin](../../by-contributor/profiles/yude-lin.md) | 正确性修复 |

---

## 10. 技术深度分析

### 字符串拼接优化 (JDK-8336856)

**问题**: Java 9 的 `invokedynamic` 字符串拼接在高参数场景存在扩展性问题

**解决方案**: 引入 `InlineHiddenClassStrategy`，消除大量嵌套类生成

**技术细节**:
- 减少类加载开销
- 提升 C2 编译器内存效率
- 保持向后兼容性

→ [完整分析](../../by-pr/8336/8336856.md) | String "+" 运算符

### DateTime 格式化优化 (JDK-8337832)

**优化点**: `DateTimeFormatter.toString()` 性能提升 10%

**技术手段**:
- 减少方法调用开销
- 优化格式化逻辑
- 缓存常用格式

→ [完整分析](../../by-pr/8337/8337832.md) | 日期时间 API

### C2 IR 节点修复 (JDK-8356328)

**问题**: 部分 C2 IR 节点缺少 `size_of()` 函数实现

**影响**: 导致编译器断言失败

**解决方案**: 为缺失节点添加正确的 `size_of()` 实现

→ [C2 编译器](../../by-topic/core/jit/c2-phases.md) | [Kuai Wei 贡献者档案](../../by-contributor/profiles/kuai-wei.md)

### Jade GC (EuroSys 2024)

**论文**: [Jade: A High-throughput Concurrent Copying Garbage Collector](https://dl.acm.org/doi/10.1145/3627703.3650087) (EuroSys 2024, Athens)

**阿里巴巴共同作者**: [Liang Mao](../../by-contributor/profiles/liang-mao.md), [Yude Lin](../../by-contributor/profiles/yude-lin.md), [Xiaowei Lu](../../by-contributor/profiles/xiaowei-lu.md), [Denghui Dong](../../by-contributor/profiles/denghui-dong.md)

**合作机构**: 上海交通大学 IPADS 实验室 (Mingyu Wu, Haibo Chen, Binyu Zang)

**技术贡献**:
- Group-wise collection 缩短预回收周期
- 分代堆布局 + 单阶段算法最大化 Young GC 吞吐量
- 兼顾短暂停和高 GC 效率

→ [PDF](https://ipads.se.sjtu.edu.cn/_media/publications/wu-eurosys24.pdf) | [ACM DL](https://dl.acm.org/doi/10.1145/3627703.3650087)

---

## 11. 相关主题文档

### 核心库

| 主题 | 描述 | 链接 |
|------|------|------|
| 字符串处理 | String, StringBuilder 优化 | 字符串优化 |
| 数字格式化 | Integer/Long toString 优化 | 数字格式化 |
| ClassFile API | 字节码操作 API | ClassFile API |

### 编译器

| 主题 | 描述 | 链接 |
|------|------|------|
| C2 编译器 | 服务端编译器优化阶段 | [C2 阶段](../../by-topic/core/jit/c2-phases.md) |
| JIT 编译 | 即时编译器概述 | [JIT 编译](../../by-topic/core/jit/README.md) |
| IR 节点 | 中间表示节点 | C2 IR |

### 垃圾收集

| 主题 | 描述 | 链接 |
|------|------|------|
| G1 GC | Garbage First 收集器 | [G1 GC](../../by-topic/core/gc/g1-gc.md) |
| ZGC | Z Garbage Collector | [ZGC](../../by-topic/core/gc/zgc.md) |
| Shenandoah | 低暂停 GC | [Shenandoah](../../by-topic/core/gc/shenandoah.md) |

### 架构

| 主题 | 描述 | 链接 |
|------|------|------|
| AArch64 | ARM 64 位架构 | [AArch64](../../by-topic/core/arch/aarch64.md) |
| x86/x64 | Intel/AMD 架构 | [x86/x64](../../by-topic/core/arch/x86.md) |

---

[← 返回组织索引](README.md)

---

## 12. 技术特点

### 性能优化导向

- **字符串处理**: StringBuilder.repeat、减少分配
- **数字格式化**: Integer/Long.toString、UUID.toString
- **启动优化**: 消除嵌套类、@Stable 注解

### 实际场景驱动

- Dragonwell 在阿里巴巴大规模部署
- 针对电商、支付等场景优化
- 性能数据来自真实业务

### 多领域覆盖

- **核心库**: java.lang, java.util, java.time, ClassFile API (Shaojin Wen 97 PRs)
- **编译器**: C2 优化 (Yi Yang 57 PRs), C1 优化 (Denghui Dong), MergeStore (Kuai Wei)
- **HotSpot Runtime**: HeapDump, JFR, jcmd (Yi Yang, Denghui Dong)
- **架构**: AArch64 寄存器压力优化 (Joshua Zhu), RISC-V (Max Xing)
- **GC**: G1 监控 MXBean (Yude Lin), ZGC 自愈 (Xiaowei Lu)

---

## 13. Alibaba Dragonwell

阿里巴巴维护自己的 JDK 发行版 Dragonwell：

| 特性 | 说明 |
|------|------|
| 基于 | OpenJDK |
| 支持 | 长期支持 (LTS) |
| 许可 | GPLv2 |
| 平台 | Linux, Windows, macOS |

**版本**: Dragonwell 8 / 11 / 17 / 21

**团队链接**:
- [Dragonwell 团队](dragonwell.md) - 核心团队成员
- [Sanhong Li (李三红)](../../by-contributor/profiles/sanhong.md) - Chief JVM Architect, Java Champion
- [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) - C2 编译器专家
- [Joshua Zhu](../../by-contributor/profiles/joshua-zhu.md) - 上海团队

**社区链接**:
- [GreenTeaJUG](http://greenteajug.cn/) - 中国最大 Java 用户组, 由 Sanhong Li 和[莫简豪 (Mo Jianhao)](https://github.com/mojianhao) 共同领导
  - 莫简豪: 前阿里巴巴, 现任[简算科技 (JianSuan)](https://jiansuan.tech/) Executive Director, GreenTeaJUG Leader
  - 组织 OpenJDK 技术分享活动 (邀请 Alibaba, Huawei, Azul, ByteDance 等技术专家)

**外部链接**:
- [Dragonwell 官网](https://dragonwell-jdk.io/)
- [GitHub Org](https://github.com/dragonwell-project)
- [Dragonwell 8](https://github.com/dragonwell-project/dragonwell8)
- [Dragonwell 11](https://github.com/dragonwell-project/dragonwell11)
- [Dragonwell 21](https://github.com/dragonwell-project/dragonwell21)

---

## 14. 影响评估

| 场景 | 受益优化 | 预期提升 | 相关 PR |
|------|------|------|------|
| JSON 序列化 | 字符串拼接优化 | +10% | [8336856](../../by-pr/8336/8336856.md) |
| 日志格式化 | DateTime toString | +10% | [8337832](../../by-pr/8337/8337832.md) |
| UUID 处理 | UUID.toString | +8% | [8310502](../../by-pr/8310/8310502.md) |
| 应用启动 | 启动优化 | +5% | [8338936](../../by-pr/8338/8338936.md) |
| 数字转换 | Integer/Long.toString | +10% | [8310929](../../by-pr/8310/8310929.md) |
| 数组操作 | ArraysSupport 优化 | +3% | [8343962](../../by-pr/8343/8343962.md) |

> **了解更多**: [JDK 性能优化](../../by-topic/core/performance/README.md)

---

## 15. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-23
- **分析工具**: PR Analysis Tool

---

## 16. 相关链接

### 外部资源

- [Alibaba Dragonwell](https://github.com/dragonwell-project/dragonwell8)
- [Dragonwell 文档](https://dragonwell-jdk.io/)
- [阿里云 Java](https://www.aliyun.com/product/dragonwell)
- [OpenJDK Census - swen](https://openjdk.org/census#swen)

### 内部文档

- [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) — 核心库优化 (97 PRs)
- [Yi Yang (杨易)](../../by-contributor/profiles/yi-yang.md) — C2 编译器, HeapDump (57 PRs)
- [Denghui Dong (董登辉)](../../by-contributor/profiles/denghui-dong.md) — C1 编译器, JFR (36 PRs)
- [Max Xing](../../by-contributor/profiles/max-xing.md) — RISC-V, C2 编译器 (16 PRs)
- [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) — C2 编译器, MergeStore (13 PRs)
- [Yude Lin](../../by-contributor/profiles/yude-lin.md) — G1 GC, AArch64 (8 PRs)
- [Joshua Zhu](../../by-contributor/profiles/joshua-zhu.md) — AArch64, 编译器 (6 PRs)
- [Xiaowei Lu](../../by-contributor/profiles/xiaowei-lu.md) — ZGC (3 PRs)
- [Long Yang (杨龙)](../../by-contributor/profiles/long-yang.md) — JFR, Runtime (3 PRs)
- [sandlerwang](../../by-contributor/profiles/sandlerwang.md) — AArch64, GC (3 PRs)
- [Liang Mao (毛亮)](../../by-contributor/profiles/liang-mao.md) — GC (2 PRs)
- [Lingjun Cao](../../by-contributor/profiles/lingjun-cao.md) — DecimalFormat (2 PRs)
- [SendaoYan](../../by-contributor/profiles/sendaoyan.md) — 编译器/GC 测试 (202 PRs, 前员工)
- [中国贡献者索引](../../by-contributor/profiles/chinese-contributors.md)

---

> **文档版本**: 5.0
> **最后更新**: 2026-03-23
> **本次更新 (v5.0) — 多轮核实与完善**:
> - **角色修正**: Kuai Wei: Author → Committer (可自行 /integrate)
> - **tagline 修正**: 新增 "HotSpot Runtime 增强"
> - **技术领域表**: 全面重写，按贡献者和具体工作分列
> - **影响模块表**: 更新为按模块-贡献者矩阵
> - **贡献时间线**: 修正为包含所有 14 位贡献者的年度数据 (含 2020 年)
> - **版本统计**: 修正旧表残留的 341/139 数据为 448/246
> - **导航链接**: 修正指向 README.md
> - **内部文档链接**: 补充所有 14 位贡献者
> - **技术特点**: 更新多领域覆盖描述
> - **数据来源时间**: 更新为 2026-03-23
>
> **v4.2**: 新增 Yi Yang (57), Joshua Zhu (6), Liang Mao (2), sandlerwang (3) 通过 /sponsor 网络发现
> **v4.1**: 移除 hgqxjj (归属证据不足), 角色修正 (Xiaowei Lu: Author→Committer)
> **v4.0**: 新增 D-D-H (36), Long Yang (3) 通过源码版权反查
> **v3.1**: 修正 Max Xing 和 SendaoYan PR 数
> **v3.0**: 初始版本