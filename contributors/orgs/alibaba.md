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

阿里巴巴通过 Dragonwell 团队参与 OpenJDK 开发，专注于核心库性能优化、字符串处理和 C2 编译器改进。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 246 (核心+PR贡献者) + 202 (测试) = 448 |
| **Git Commits (次要)** | 2 (1 位次要贡献者) |
| **贡献者数** | 14 (4 核心 + 8 PR贡献者 + 1 次要 + 1 测试) |
| **活跃时间** | 2021 - 至今 |
| **主要领域** | 核心库、C2 编译器、AArch64、ZGC、RISC-V、HotSpot Runtime |
| **Dragonwell** | [Alibaba Dragonwell](https://github.com/dragonwell-project/dragonwell8), [Dragonwell Team](dragonwell.md) |

> **统计说明**: 
> - 核心/测试贡献者使用 GitHub Integrated PRs 统计
> - 次要贡献者使用 git commit 邮箱 (`@alibaba-inc.com`) 统计

---

## 2. 贡献者

### 核心贡献者

| 贡献者 | Profile | PRs | 角色 | 主要领域 |
|--------|---------|-----|------|----------|
| [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | [@wenshao](https://github.com/wenshao) | 97 | Committer | 核心库优化 |
| [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) | [@kuaiwei](https://github.com/kuaiwei) | 13 | Committer | C2 编译器 |
| [Yude Lin](../../by-contributor/profiles/yude-lin.md) | [@linade](https://github.com/linade) | 8 | Author | G1 GC, AArch64 |
| [Xiaowei Lu](../../by-contributor/profiles/xiaowei-lu.md) | [@weixlu](https://github.com/weixlu) | 3 | Committer | ZGC |

> **OpenJDK Census 角色核实** (2026-03-23):
> - **Shaojin Wen** (swen): Committer ✅ — [提名邮件 (2024-08)](https://mail.openjdk.org/pipermail/jdk-dev/2024-August/009326.html)，由 Claes Redestad (Oracle) 提名，确认 Alibaba
> - **Denghui Dong** (ddong): Committer ✅ — [提名邮件 (2021-08)](https://mail.openjdk.org/pipermail/jdk-dev/2021-August/005899.html)，确认 Alibaba JVM Team
> - **Xiaowei Lu** (xwlu): Committer ✅ — OpenJDK Census 确认 (文档之前误记为 Author)
> - **Sendao Yan** (syan): Committer ✅
> - **Kuai Wei** (kwei): Committer ✅ — 可自行 /integrate (之前误记为 Author)
> - **Yude Lin** (linade): Author ✅
> - **Long Yang** (lyang): Author ✅

### 其他 PR 贡献者

| 贡献者 | Profile | PRs | 角色 | 主要领域 |
|--------|---------|-----|------|----------|
| Yi Yang (杨易) | [@y1yang0](https://github.com/y1yang0) | 57 | Committer | C2 编译器, HotSpot | - |
| Denghui Dong (董登辉) | [@D-D-H](https://github.com/D-D-H) | 36 | Committer | HotSpot Runtime, 编译器, GC | - |
| Max Xing | [@MaxXSoft](https://github.com/MaxXSoft) | 16 | Author | RISC-V, C2 编译器, HotSpot | - |
| Joshua Zhu (朱文杰) | [@JoshuaZhuwj](https://github.com/JoshuaZhuwj) | 6 | Author | AArch64, 编译器 | [详情](../../by-contributor/profiles/joshua-zhu.md) |
| Long Yang (杨龙) | [@yanglong1010](https://github.com/yanglong1010) | 3 | Author | JFR, Runtime | - |
| sandlerwang | [@sandlerwang](https://github.com/sandlerwang) | 3 | Author | AArch64, GC | - |
| Liang Mao (毛亮) | [@mmyxym](https://github.com/mmyxym) | 2 | Author | GC | - |
| [Lingjun Cao](../../by-contributor/profiles/lingjun-cao.md) | [@lingjun-cg](https://github.com/lingjun-cg) | 2 | Author | DecimalFormat 性能 | - |

> **贡献者归属确认**:
> - **Yi Yang** (57 PRs): 通过 [Dragonwell 项目 12 个 PR](https://github.com/dragonwell-project/dragonwell11/pulls?q=author:y1yang0) + 审查 D-D-H 的 PR + sponsor wenshao/sendaoYan 的 PR 确认为阿里巴巴。主要贡献 C2 编译器，活跃于 2021-2024。**(通过方法 5: PR 审查/Sponsor 关系网络发现)**
> - **Denghui Dong** (36 PRs): 通过 [Dragonwell 项目 14 个 PR](https://github.com/dragonwell-project/dragonwell11/pulls?q=author:D-D-H) + sponsor yanglong1010/mmyxym/sandlerwang 的 PR 确认。
> - **Joshua Zhu** (6 PRs): GitHub 公司标注 @Alibaba，位于上海。Dragonwell 项目 22 个 PR。
> - **Liang Mao** (2 PRs): [Dragonwell 项目 38 个 PR](https://github.com/dragonwell-project/dragonwell11/pulls?q=author:mmyxym)，D-D-H 为其 sponsor。
> - **sandlerwang** (3 PRs): [Dragonwell 项目 10 个 PR](https://github.com/dragonwell-project/dragonwell11/pulls?q=author:sandlerwang)，D-D-H 为其 sponsor。
> - **Max Xing** (16 PRs): [Dragonwell 项目贡献](https://github.com/dragonwell-project/dragonwell11/pulls?q=author:MaxXSoft) 确认关联。
> - **Long Yang** (3 PRs): GitHub 公司标注 @Alibaba，D-D-H 为其 sponsor。

### 次要贡献者

> **说明**: 以下贡献者通过 git commit (使用 @alibaba-inc.com 邮箱) 贡献，未通过 GitHub PR 提交。

| 贡献者 | Profile | Commits | 主要领域 |
|--------|---------|---------|----------|
| [Yibo Yan](../../by-contributor/profiles/yibo-yan.md) | - | 2 | CPU Load, 内存优化 |

### 前员工贡献

| 贡献者 | 时期 | PRs | 当前状态 | 主要领域 |
|--------|------|-----|----------|----------|
| [SendaoYan](../../by-contributor/profiles/sendaoyan.md) | 2022-2025 | 202 | Independent/Other | 编译器测试，GC 测试 |

> **注**:
> - 前员工的历史贡献 (202 PRs) 仍归属于 Alibaba，因为这是在职期间的工作成果
> - 次要贡献者通过 git commit 统计，邮箱为 `@alibaba-inc.com`

---

## 3. 技术领域

| 领域 | 贡献者 | PRs | 相关文档 |
|------|--------|-----|----------|
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

| Issue | 标题 | 贡献者 | 类型 | 影响 |
|-------|------|--------|------|------|
| 8370503 | Integer/Long toString 使用 String.newStringWithLatin1Bytes | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +10% |
| 8370013 | Double.toHexString 消除 regex 和 StringBuilder | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +20% |
| 8368825 | DateTimeFormatterBuilder 使用 switch 表达式 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码质量 | - |
| 8368172 | DateTimePrintContext 改为不可变 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +8-10% |
| 8368024 | 移除 StringConcatFactory#generateMHInlineCopy | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码清理 | -800 行 |
| 8366224 | DecimalDigits.appendPair 高效两位数格式化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +15% |
| 8365620 | MethodHandleDesc 使用增强 switch | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码质量 | - |
| 8365186 | 减少 DateTimePrintContext::adjust 大小 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +1% |

**JDK 26 统计**: 8 PRs (Shaojin Wen: 8)

### JDK 25 (GA 2025-09)

JDK 25 继续了核心库性能优化的工作。

| Issue | 标题 | 贡献者 | 类型 | 影响 |
|-------|------|--------|------|------|
| 8357913 | BigInteger 和 BigDecimal 添加 @Stable | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +3% |
| 8357690 | CharacterData 添加 @Stable 和 final | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +2% |
| 8357685 | String.indexOf/lastIndexOf 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +5% |
| 8357289 | String 构造函数拆分为更小的方法 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +2% |
| 8357063 | DecimalDigits 方法前置条件文档 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 文档改进 | - |
| 8356605 | JRSUIControl.hashCode 使用 Long.hashCode | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码简化 | - |
| 8356328 | C2 IR 节点 size_of() 函数 | [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) | 正确性修复 | - |
| 8356036 | FileKey.hashCode 使用 Long.hashCode | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码简化 | - |
| 8356021 | Locale.hashCode 使用 Double::hashCode | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | NaN 处理 | - |
| 8355300 | BitSieve 添加 final | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +2% |
| 8355240 | 移除 StringUTF16 未使用的 Import | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码清理 | - |
| 8355177 | StringBuilder 空构造优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +5% |
| 8353741 | HexFormat toUpper/toLower 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | - |
| 8351565 | String.concat 微优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +3% |
| 8351443 | InlineHiddenClassStrategy 实现 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 架构改进 | +5% |
| 8349400 | 消除嵌套类提升启动速度 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +5% |
| 8348898 | 移除未使用的 OctalDigits | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码清理 | -130 行 |
| 8348880 | ZoneOffset.QUARTER_CACHE 使用 AtomicReferenceArray | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 内存优化 | -85% |
| 8348870 | ByteOrder.toString 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | - |
| 8347405 | MergeStores 反向字节顺序 | [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) | 正确性修复 | - |

**JDK 25 统计**: 20 PRs (Shaojin Wen: 18, Kuai Wei: 2)

### JDK 24 (GA 2025-03)

JDK 24 是阿里巴巴开始活跃贡献的版本。

| Issue | 标题 | 贡献者 | 类型 | 影响 |
|-------|------|--------|------|------|
| 8343650 | 复用 StringLatin1::putCharsAt | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码复用 | - |
| 8342336 | ClassFile imports 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | -480 行 |
| 8341906 | ClassFile Buffer 写入优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +28% |
| 8339401 | ClassFile load/store 指令 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +10-20% |
| 8336856 | InlineHiddenClassStrategy | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | **架构改进** | +5% |
| 8336831 | StringConcatHelper.simpleConcat | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +10-15% |
| 8335182 | MergeStore C2 优化模式 | [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) | 性能优化 | +30% |
| 8334431 | C2 IR Graph 将 MemBarAcquire 放入循环 | [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) | 正确性修复 | - |

**JDK 24 统计**: 8 PRs (Shaojin Wen: 6, Kuai Wei: 2)

#### 次要贡献者 (Git Commits)

| Issue | 标题 | 贡献者 | 类型 | 日期 |
|-------|------|--------|------|------|
| 8326936 | RISC-V: Shenandoah GC 原子操作修复 | Max Xing | 正确性修复 | 2024-03-05 |
| 8324280 | RISC-V: VM_Version::parse_satp_mode 修复 | Max Xing | 正确性修复 | 2024-01-25 |
| 8326446 | Apple M1 CPU Load 修复 | [Yibo Yan](../../by-contributor/profiles/yibo-yan.md) | 正确性修复 | 2024-03-08 |
| 8319876 | VM_ThreadDump 内存优化 | [Yibo Yan](../../by-contributor/profiles/yibo-yan.md) | 内存优化 | 2023-11-17 |
| 8333396 | java.text.Format 内部使用 StringBuilder | [Lingjun Cao](../../by-contributor/profiles/lingjun-cao.md) | 性能优化 | 2024-07-22 |
| 8333462 | DecimalFormat 构造函数性能回归 | [Lingjun Cao](../../by-contributor/profiles/lingjun-cao.md) | 性能优化 | 2024-06-04 |

**JDK 24 次要贡献统计**: 6 commits/PRs (Max Xing: 2, Yibo Yan: 2, Lingjun Cao: 2)

### JDK 23 (GA 2024-09)

JDK 23 是阿里巴巴贡献最活跃的版本，包含大量性能优化。

| Issue | 标题 | 贡献者 | 类型 | 影响 |
|-------|------|--------|------|------|
| 8344168 | Unsafe base offset 从 int 改为 long | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 溢出修复 | - |
| 8343984 | Unsafe 地址溢出修复 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 安全修复 | - |
| 8343962 | ArraysSupport.arrayToString 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +3% |
| 8343925 | [BACKOUT] 移动 getChars 到 DecimalDigits | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 回退 | - |
| 8343650 | 复用 StringLatin1::putCharsAt | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码复用 | - |
| 8343629 | 更多 MergeStore 基准测试 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 测试 | - |
| 8343500 | ArrayClassDescImpl computeDescriptor 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +37% |
| 8342336 | ClassFile imports 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | -480 行 |
| 8341906 | ClassFile BufBuffer 写入优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +28% |
| 8341900 | DirectCodeBuilder writeBody 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | codeSize -10% |
| 8341859 | ClassFile Benchmark Write 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 稳定性 | - |
| 8341755 | InnerClassLambdaMetafactory argNames 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +17-20% |
| 8341664 | ReferenceClassDescImpl 缓存 internalName | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +93% |
| 8341581 | BytecodeHelpers validate slot 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 内联优化 | - |
| 8341548 | 更简洁的 ClassFile API 使用 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码简化 | -19 行 |
| 8341512 | StackMapGenerator processInvokeInstructions | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | codeSize -5% |
| 8341510 | StackMapGenerator processFieldInstructions | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | codeSize -15% |
| 8341415 | RawBytecodeHelper::next 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +5-10% |
| 8341199 | ClassFile loadConstant(int) | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +3-5% |
| 8341141 | DirectCodeBuilder 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +8-15% |
| 8341136 | StackMapGenerator trimAndCompress | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +2-5% |
| 8341006 | StackMapGenerator detect frames | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +5-10% |
| 8340708 | StackMapGenerator processMethod | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +2-4% |
| 8340587 | Frame::checkAssignableTo | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +3-7% |
| 8340544 | setLocalsFromArg 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +8-12% |
| 8340232 | DataInputStream::readUTF 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | - |
| 8340710 | DirectClassBuilder::build | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +5-10% |
| 8339699 | DataOutputStream writeUTF | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | - |
| 8339635 | CompactStrings 关闭时优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | - |
| 8339401 | ClassFile load/store 指令 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +10-20% |
| 8339320 | Utf8EntryImpl#inflate | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 方法拆分 | - |
| 8339317 | ClassFile writeBuffer | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 写入优化 | - |
| 8339299 | C1 内联 final 方法丢失类型 profile | [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) | 性能修复 | - |
| 8339290 | Utf8EntryImpl#writeTo | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | ASCII 快速路径 | - |
| 8339217 | ClassFile API loadConstant | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 新增重载 | - |
| 8339205 | StackMapGenerator | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | codeSize 优化 | - |
| 8339196 | BufWriterImpl#writeU1/U2/Int/Long | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | C2 友好 | - |
| 8339168 | ClassFile Util slotSize | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 引用比较 | - |
| 8338937 | ClassDesc 字符串拼接优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | String.concat | - |
| 8338936 | StringConcatFactory MethodType 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +10% |
| 8338930 | StringConcatFactory 静态方法优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 静态方法 | - |
| 8338532 | MethodTypeDesc#ofDescriptor | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | 消除 ArrayList |
| 8338409 | 使用 record 简化代码 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码简化 | -9 行 |
| 8337832 | DateTime toString 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +10% |
| 8337279 | 共享 StringBuilder 格式化 instant | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 优化 | - |
| 8337245 | StringConcatHelper 注释修复 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 文档修正 | - |
| 8337168 | LocalDateTime.toString 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | - |
| 8337167 | StringSize 去重 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码清理 | -95 行 |
| 8336856 | InlineHiddenClassStrategy | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | **架构改进** | +5% |
| 8336831 | StringConcatHelper.simpleConcat | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +10-15% |
| 8336792 | DateTimeFormatterBuilder 使用 repeat | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码简化 | -33% |
| 8336741 | LocalTime.toString 使用 repeat | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +15-20% |
| 8336706 | LocalDate.toString 使用 repeat | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +20% |
| 8336278 | String.format("%n") 替换为 lineSeparator | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | 60x |
| 8335802 | HexFormat boolean 替换 enum | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 启动优化 | - |
| 8335645 | Formatter trailingZeros 使用 repeat | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 代码简化 | - |
| 8335252 | Formatter.Conversion#isValid | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | codeSize -30% | - |
| 8335182 | MergeStore C2 优化模式 | [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) | 性能优化 | +30% |
| 8334342 | MergeStore JMH 基准测试 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 基准测试 | - |
| 8334328 | FloatToDecimal/DoubleToDecimal 减少分配 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 减少分配 | - |
| 8333893 | StringBuilder append boolean & null | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | +10-15% |
| 8333833 | UUID.toString 移除 ByteArrayLittleEndian | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 平台无关 | - |
| 8334431 | C2 IR Graph 将 MemBarAcquire 放入循环 | [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) | 正确性修复 | - |
| 8328064 | 移除 constantPool 过时注释 | [Yude Lin](../../by-contributor/profiles/yude-lin.md) | 代码清理 | - |
| 8326135 | ADLC 报告未使用的操作数 | [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) | 工具改进 | - |
| 8323122 | AArch64 itable stub 大小估算 | [Yude Lin](../../by-contributor/profiles/yude-lin.md) | 正确性修复 | - |

**JDK 23 统计**: 34 PRs (Shaojin Wen: 34) + Kuai Wei: 7, Yude Lin: 3 (包含跨版本 PR)

> **注**: JDK 23 周期为 2024-03 至 2024-09-17 GA。部分 835xxxx 系列 PR 之前错误归入此版本，已移至 JDK 25。

### JDK 21 / JDK 22

JDK 21/22 时期的贡献主要集中在 GC 监控和架构支持。

| Issue | 标题 | 贡献者 | 类型 | 影响 |
|-------|------|--------|------|------|
| 8317742 | DateTimeFormatter 和 String.format ISO 标准一致性 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 标准一致性 | - |
| 8316704 | Formatter/FormatProcessor 消除正则 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | - |
| 8316426 | HexFormat.formatHex 查找表优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 性能优化 | - |
| 8315968 | java.util.Digits 移动到 jdk.internal.util | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 重构 | - |
| 8315970 | JDK-8310929 后的大端序问题 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 大端序修复 | - |
| 8311207 | UUID.toString 优化清理 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | 清理 | - |
| 8310929 | Integer.toString 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | **性能优化** | +10% |
| 8310502 | Long.fastUUID 优化 | [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | **性能优化** | +8% |
| 8298521 | G1MonitoringSupport 成员重命名 | [Yude Lin](../../by-contributor/profiles/yude-lin.md) | 代码清理 | - |
| 8297247 | G1 添加 Remark/Cleanup MXBean | [Yude Lin](../../by-contributor/profiles/yude-lin.md) | **监控增强** | 新功能 |

**JDK 21/22 统计**: 10 PRs (Shaojin Wen: 8, Yude Lin: 2)

### 其他贡献者 PR (按贡献者分类)

> 以下贡献者的 PR 跨越多个 JDK 版本，按贡献者分类展示。

#### Yi Yang (@y1yang0) — 57 PRs (C2 编译器, HotSpot)

| Issue | 标题 | 类型 | 版本 |
|-------|------|------|------|
| 8323795 | jcmd Compiler.codecache should print total size | 功能增强 | JDK 23 |
| 8314021 | HeapDump: Optimize segmented heap file merging | 性能优化 | JDK 22 |
| 8311775 | duplicate verifyHeapDump in several tests | 测试清理 | JDK 22 |
| 8306441 | Two phase segmented heap dump | **核心功能** | JDK 22 |
| 8143900 | OptimizeStringConcat opaque dependency on sizeTable | C2 优化 | JDK 21 |
| 8299518 | HotSpotVirtualMachine shared code across platforms | 重构 | JDK 21 |
| 8288204 | GVN Crash: assert() failed: correct memory chain | C2 修复 | JDK 20 |
| 8290432 | C2 fails with assert(node->_last_del == _last) | C2 修复 | JDK 20 |
| 8282883 | Use JVM_LEAF to avoid ThreadStateTransition | 性能优化 | JDK 19 |
| 8275775 | Add jcmd VM.classes to print details | 功能增强 | JDK 19 |
| 8278125 | preallocated OOMEs missing stack trace | 修复 | JDK 19 |
| 8273585 | String.charAt performance degrades | **性能回归修复** | JDK 18 |
| 8274328 | C2: Redundant CFG edges fixup | C2 优化 | JDK 18 |
| 8273021 | C2: Improve Add and Xor ideal optimizations | C2 优化 | JDK 18 |
| 8271203 | C2: assert in subtype check | C2 修复 | JDK 18 |
| 8272493 | Suboptimal code around Preconditions.checkIndex | C2 优化 | JDK 19 |

> **注**: 以上为 Yi Yang 57 PRs 中的代表性工作。完整列表见 [GitHub](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Ay1yang0+label%3Aintegrated)。

#### Denghui Dong (@D-D-H) — 36 PRs (HotSpot Runtime, C1, JFR)

| Issue | 标题 | 类型 | 版本 |
|-------|------|------|------|
| 8340144 | C1: remove unused Compilation::_max_spills | 代码清理 | JDK 24 |
| 8327693 | C1: LIRGenerator::_instruction_for_operand assertion only | 代码清理 | JDK 23 |
| 8327379 | Make TimeLinearScan a develop flag | 清理 | JDK 23 |
| 8326127 | JFR: SafepointCleanupTask to hardToTestEvents | JFR | JDK 23 |
| 8326111 | JFR: Cleanup for JFR_ONLY | 代码清理 | JDK 23 |
| 8325144 | C1: Optimize CriticalEdgeFinder | **C1 优化** | JDK 23 |
| 8324974 | JFR: EventCompilerPhase UNTIMED | JFR | JDK 23 |
| 8322694 | C1: Handle Constant and IfOp in NullCheckEliminator | **C1 优化** | JDK 23 |
| 8322735 | C2: improvements of bubble sort in SuperWord | C2 优化 | JDK 23 |
| 8321404 | Limit heap dumps triggered by HeapDumpBeforeFullGC | 功能增强 | JDK 23 |
| 8280843 | macos-Aarch64 SEGV in sender_for_compiled_frame | 修复 | JDK 19 |

> **注**: 以上为代表性工作。完整列表见 [GitHub](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3AD-D-H+label%3Aintegrated)。

#### Max Xing (@MaxXSoft) — 16 PRs (RISC-V, C2, HotSpot)

| Issue | 标题 | 类型 | 版本 |
|-------|------|------|------|
| 8347499 | C2: PhaseIdealLoop eliminate redundant safepoints | **C2 优化** | JDK 25 |
| 8360192 | C2: Make type of count leading/trailing zero precise | C2 优化 | JDK 26 |
| 8358104 | Fix ZGC compilation error on GCC 10.2 | 构建修复 | JDK 26 |
| 8333334 | C2: Make Node::dominates more precise for scalar replacement | **C2 优化** | JDK 24 |
| 8335536 | Fix assertion failure in IdealGraphPrinter | 修复 | JDK 24 |
| 8326936 | RISC-V: Shenandoah GC incorrect atomic operations | **正确性修复** | JDK 23 |
| 8324280 | RISC-V: Incorrect VM_Version::parse_satp_mode | 修复 | JDK 23 |

> **注**: 以上为代表性工作。完整列表见 [GitHub](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3AMaxXSoft+label%3Aintegrated)。

#### Joshua Zhu (@JoshuaZhuwj) — 6 PRs (AArch64, 编译器)

| Issue | 标题 | 类型 | 版本 |
|-------|------|------|------|
| 8339063 | AArch64: Skip verify_sve_vector_length for 128-bit | 性能优化 | JDK 24 |
| 8326541 | AArch64: ZGC C2 load barrier stub register spilling | 正确性修复 | JDK 23 |
| 8282874 | Bad performance on gather/scatter API (IntSpecies) | 性能修复 | JDK 19 |
| 8269598 | Regressions up to 5% on aarch64 due to JDK-8268858 | **回归修复** | JDK 18 |
| 8268858 | Determine register pressure automatically | **编译器优化** | JDK 18 |
| 8253048 | AArch64: CallLeaf no need to preserve callee-saved | 性能优化 | JDK 17 |

#### Liang Mao (@mmyxym) — 2 PRs (GC)

| Issue | 标题 | 类型 | 版本 |
|-------|------|------|------|
| 8339725 | Concurrent GC crashed due to GetMethodDeclaringClass | **GC 修复** | JDK 24 |
| 8335493 | check_gc_overhead_limit should reset SoftRefPolicy | GC 修复 | JDK 24 |

#### sandlerwang (@sandlerwang) — 3 PRs (AArch64, GC)

| Issue | 标题 | 类型 | 版本 |
|-------|------|------|------|
| 8324817 | Parallel GC pre-touch all heap pages when large page disabled | **GC 修复** | JDK 23 |
| 8324123 | aarch64: fix prfm literal encoding in assembler | AArch64 修复 | JDK 23 |
| 8252835 | Revert fix for JDK-8246051 | 回退 | JDK 17 |

### JDK 17 / JDK 11

早期贡献主要在 ZGC 和 Shenandoah GC。

| Issue | 标题 | 贡献者 | 类型 | 影响 |
|-------|------|--------|------|------|
| 8274546 | Shenandoah 移除未使用的 ShenandoahUpdateRootsTask | [Yude Lin](../../by-contributor/profiles/yude-lin.md) | 代码清理 | - |
| 8273112 | -Xloggc 应覆盖 -verbose:gc | [Xiaowei Lu](../../by-contributor/profiles/xiaowei-lu.md) | 功能修复 | - |
| 8272138 | ZGC 采用宽松顺序进行自愈 | [Xiaowei Lu](../../by-contributor/profiles/xiaowei-lu.md) | **性能优化** | - |
| 8270347 | ZGC 转发表 release-acquire | [Xiaowei Lu](../../by-contributor/profiles/xiaowei-lu.md) | 正确性修复 | - |
| 8266963 | 移除 safepoint poll (重入问题) | [Yude Lin](../../by-contributor/profiles/yude-lin.md) | 正确性修复 | - |
| 8266185 | Shenandoah 修正注释/断言 | [Yude Lin](../../by-contributor/profiles/yude-lin.md) | 代码质量 | - |

**JDK 17/11 统计**: 6 PRs (Yude Lin: 3, Xiaowei Lu: 3)

---

## 5. 版本贡献统计

### 全贡献者统计

| 贡献者 | PRs | 主要领域 | 活跃版本 |
|--------|-----|----------|----------|
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

### 测试贡献 (SendaoYan)

| 年份 | PRs | 主要领域 |
|------|-----|----------|
| **2026** | 24 | GC 测试，稳定性修复 |
| **2025** | 95 | JFR 测试，编译器测试 |
| **2024** | 82 | 编译器测试，GC 测试 |
| **2022** | 1 | 初始贡献 |
| **小计** | **202** | 测试稳定性 |

### 总计

| 类别 | PRs | 占比 |
|------|-----|------|
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
|------|--------|------|
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
|-------|------|----------|----------|
| 8337832 | DateTime toString 优化 | +10% | [分析](../../by-pr/8337/8337832.md) |
| 8338936 | StringConcatFactory MethodType 优化 | 启动优化 | [分析](../../by-pr/8338/8338936.md) |
| 8338532 | ClassFile API MethodTypeDesc 优化 | 启动优化 | [分析](../../by-pr/8338/8338532.md) |
| 8336856 | 高效的隐藏类字符串拼接策略 | 启动优化 | [分析](../../by-pr/8336/8336856.md) |
| 8336831 | StringConcatHelper.simpleConcat 优化 | +5% | [分析](../../by-pr/8336/8336831.md) |
| 8310929 | Integer.toString 优化 | +10% | [分析](../../by-pr/8310/8310929.md) |
| 8310502 | Long.fastUUID 优化 | +8% | [分析](../../by-pr/8310/8310502.md) |
| 8370013 | ArraysSupport big endian 支持 | 新功能 | - |
| 8365832 | HexFormat boolean 替换 enum | 启动优化 | [分析](../../by-pr/8365/8365832.md) |
| 8366224 | Character checkTitleCase 优化 | 性能优化 | - |
| 8368825 | StringBuilder CharSequence 支持 | API 增强 | - |
| 8357685 | String indexOf.last 优化 | +5% | [分析](../../by-pr/8357/8357685.md) |
| 8353741 | HexFormat toUpper/toLower 优化 | 性能优化 | [分析](../../by-pr/8353/8353741.md) |
| 8348870 | ByteOrder.toString 优化 | 性能优化 | - |
| 8343962 | ArraysSupport.arrayToString 优化 | +3% | [分析](../../by-pr/8343/8343962.md) |
| 8343984 | Unsafe 越界检查优化 | 安全性 | - |
| 8316426 | HexFormat 实现 | 新功能 | [分析](../../by-pr/8316/8316426.md) |
| 8316704 | HexFormat fromHexDigit 实现 | 新功能 | - |
| 8335802 | Formatter formatSpecifier 优化 | 性能优化 | - |
| 8335645 | Formatter parseType 优化 | 性能优化 | - |
| 8335252 | Formatter formatWith 优化 | 性能优化 | - |
| 8334328 | Formatter isFixed 优化 | 性能优化 | - |
| 8337168 | Formatter minIntegerDigits 优化 | 性能优化 | - |
| 8337167 | Formatter parse 优化 | 性能优化 | - |

> **更多**: [Shaojin Wen 贡献者档案](../../by-contributor/profiles/shaojin-wen.md) | [完整 PR 列表](../../by-contributor/profiles/shaojin-wen.md#complete-pr-list)

### C2 编译器 (Kuai Wei)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8356328 | C2 IR 节点 size_of() 函数 | 正确性修复 |
| 8347405 | MergeStores 反向字节顺序 | 正确性修复 |
| 8339299 | C1 内联 final 方法丢失类型 profile | 性能修复 |
| 8326135 | ADLC 报告未使用的操作数 | 工具改进 |

> **更多**: [Kuai Wei 贡献者档案](../../by-contributor/profiles/kuai-wei.md)

### G1 GC 和 AArch64 (Yude Lin)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8297247 | G1 添加 Remark 和 Cleanup 暂停时间 MXBean | **监控增强** |
| 8298521 | G1MonitoringSupport 成员重命名 | 代码清理 |
| 8323122 | AArch64 itable stub 大小估算 | 正确性修复 |

> **更多**: [Yude Lin 贡献者档案](../../by-contributor/profiles/yude-lin.md)

### ZGC 优化 (Xiaowei Lu)

| Issue | 标题 | 说明 |
|-------|------|------|
| 8272138 | ZGC 采用宽松顺序进行自愈 | **性能优化** |
| 8270347 | ZGC 转发表采用 release-acquire 顺序 | 正确性修复 |
| 8273112 | -Xloggc 应覆盖 -verbose:gc | 功能修复 |

> **更多**: [Xiaowei Lu 贡献者档案](../../by-contributor/profiles/xiaowei-lu.md) |

---

## 9. 相关 PR 分析文档

### 核心性能优化 (Shaojin Wen)

| PR | 标题 | 性能影响 | 分析文档 |
|----|------|----------|----------|
| JDK-8336856 | Inline concat with InlineHiddenClassStrategy | 启动优化 | [详情](../../by-pr/8336/8336856.md) |
| JDK-8337832 | DateTime toString 优化 | +10% | [详情](../../by-pr/8337/8337832.md) |
| JDK-8310929 | Integer.toString() 优化 | +10% | [详情](../../by-pr/8310/8310929.md) |
| JDK-8310502 | Long.fastUUID() 优化 | +8% | [详情](../../by-pr/8310/8310502.md) |
| JDK-8357685 | String.indexOf.last() 优化 | +5% | [详情](../../by-pr/8357/8357685.md) |
| JDK-8343962 | ArraysSupport.arrayToString() 优化 | +3% | [详情](../../by-pr/8343/8343962.md) |

### ClassFile API 优化 (Shaojin Wen)

| PR | 标题 | 影响 | 分析文档 |
|----|------|------|----------|
| JDK-8338936 | StringConcatFactory MethodType 优化 | 启动优化 | [详情](../../by-pr/8338/8338936.md) |
| JDK-8338532 | MethodTypeDesc 实现优化 | 启动优化 | [详情](../../by-pr/8338/8338532.md) |

### Formatter/HexFormat (Shaojin Wen)

| PR | 标题 | 分析文档 |
|----|------|----------|
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
|----|------|------|----------|
| JDK-8356328 | C2 IR 节点 size_of() 函数 | 正确性修复 | - |
| JDK-8347405 | MergeStores 反向字节顺序 | 正确性修复 | - |

### GC (Yude Lin, Xiaowei Lu)

| PR | 标题 | 贡献者 | 说明 |
|----|------|--------|------|
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
- [Dragonwell 团队](dragonwell.md) - 核心团队成员和社交网络
- [Sanhong Li](../../by-contributor/profiles/sanhong.md) - ASE 2021 论文作者，JVM 团队
- [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) - C2 编译器专家
- [Long Yang](../../by-contributor/profiles/yanglong1010.md) - JVM 团队，杭州
- [SendaoYan](../../by-contributor/profiles/sendaoyan.md) - 编译器测试工程师
- [Joshua Zhu](../../by-contributor/profiles/joshua-zhu.md) - 上海团队

**外部链接**:
- [Dragonwell 官网](https://dragonwell-jdk.io/)
- [GitHub Org](https://github.com/dragonwell-project)
- [Dragonwell 8](https://github.com/dragonwell-project/dragonwell8)
- [Dragonwell 11](https://github.com/dragonwell-project/dragonwell11)
- [Dragonwell 21](https://github.com/dragonwell-project/dragonwell21)

---

## 14. 影响评估

| 场景 | 受益优化 | 预期提升 | 相关 PR |
|------|----------|----------|---------|
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
- [Yi Yang](https://github.com/y1yang0) — C2 编译器, HeapDump (57 PRs)
- [Denghui Dong](https://github.com/D-D-H) — C1 编译器, JFR (36 PRs)
- [Max Xing](https://github.com/MaxXSoft) — RISC-V, C2 编译器 (16 PRs)
- [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) — C2 编译器, MergeStore (13 PRs)
- [Yude Lin](../../by-contributor/profiles/yude-lin.md) — G1 GC, AArch64 (8 PRs)
- [Joshua Zhu](../../by-contributor/profiles/joshua-zhu.md) — AArch64, 编译器 (6 PRs)
- [Xiaowei Lu](../../by-contributor/profiles/xiaowei-lu.md) — ZGC (3 PRs)
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