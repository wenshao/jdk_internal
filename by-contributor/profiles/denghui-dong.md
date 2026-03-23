# Denghui Dong (董登辉)

> C1 编译器优化、JFR 改进、HotSpot Runtime 增强

---
## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Denghui Dong (董登辉) |
| **当前组织** | [阿里巴巴 (Alibaba) - JVM Team](/contributors/orgs/alibaba.md) |
| **GitHub** | [@D-D-H](https://github.com/D-D-H) |
| **OpenJDK** | Committer (ddong) — [CFV 2021-08 "Alibaba JVM Team"](https://mail.openjdk.org/pipermail/jdk-dev/2021-August/005899.html) |
| **PRs** | [36 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3AD-D-H+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | C1 编译器, JFR, HeapDump, HotSpot Runtime, String Dedup |
| **活跃时间** | 2021 - 2024 |
| **归属确认** | [CFV 提名 "Alibaba JVM Team"](https://mail.openjdk.org/pipermail/jdk-dev/2021-August/005899.html) + [Dragonwell 14 PRs](https://github.com/dragonwell-project/dragonwell11/pulls?q=author:D-D-H) |

> **数据调查时间**: 2026-03-23

---

## 贡献概览

| 年份 | PRs | 主要工作 |
|------|-----|----------|
| **2021** | 18 | JFR 文件名扩展, String Dedup for Serial GC, 代码清理 |
| **2022** | 2 | AArch64 崩溃修复, -Xlog:help 输出修复 |
| **2023-2024** | 16 | C1 编译器优化, JFR 清理, HeapDump 限制 |
| **总计** | **36** | |

---

## 代表性工作

### 核心贡献

| PR | Bug ID | 标题 | 类型 | 分析 |
|----|--------|------|------|------|
| [#5153](https://github.com/openjdk/jdk/pull/5153) | 8272609 | Add string deduplication support to SerialGC | **核心功能** | - |
| [#4550](https://github.com/openjdk/jdk/pull/4550) | 8261441 | JFR: Filename expansion | **JFR 增强** | - |
| [#16976](https://github.com/openjdk/jdk/pull/16976) | 8321404 | Limit heap dumps triggered by HeapDumpBeforeFullGC | 功能增强 | [详情](/by-pr/8321/8321404.md) |
| [#17674](https://github.com/openjdk/jdk/pull/17674) | 8325144 | C1: Optimize CriticalEdgeFinder | **C1 优化** | [详情](/by-pr/8325/8325144.md) |
| [#17191](https://github.com/openjdk/jdk/pull/17191) | 8322694 | C1: Handle Constant and IfOp in NullCheckEliminator | **C1 优化** | [详情](/by-pr/8322/8322694.md) |
| [#3470](https://github.com/openjdk/jdk/pull/3470) | 8265129 | Add intrinsic support for JVM.getClassId | JFR 性能 | - |

### C1 编译器优化 (2023-2024)

| PR | Bug ID | 标题 | 分析 |
|----|--------|------|------|
| [#17191](https://github.com/openjdk/jdk/pull/17191) | 8322694 | C1: Handle Constant and IfOp in NullCheckEliminator | [详情](/by-pr/8322/8322694.md) |
| [#17674](https://github.com/openjdk/jdk/pull/17674) | 8325144 | C1: Optimize CriticalEdgeFinder | [详情](/by-pr/8325/8325144.md) |
| [#17499](https://github.com/openjdk/jdk/pull/17499) | 8324213 | C1: Canonicalizer doesn't need to handle IfOp | - |
| [#17553](https://github.com/openjdk/jdk/pull/17553) | 8324630 | C1: Canonicalizer::do_LookupSwitch optimization | - |
| [#17204](https://github.com/openjdk/jdk/pull/17204) | 8322779 | C1: Remove unused counter 'totalInstructionNodes' | - |
| [#17205](https://github.com/openjdk/jdk/pull/17205) | 8322781 | C1: Debug build crash in GraphBuilder::vmap() | - |
| [#18125](https://github.com/openjdk/jdk/pull/18125) | 8327379 | Make TimeLinearScan a develop flag | [详情](/by-pr/8327/8327379.md) |
| [#18170](https://github.com/openjdk/jdk/pull/18170) | 8327693 | C1: LIRGenerator assertion only | [详情](/by-pr/8327/8327693.md) |
| [#21007](https://github.com/openjdk/jdk/pull/21007) | 8340144 | C1: remove unused Compilation::_max_spills | [详情](/by-pr/8340/8340144.md) |

### JFR 贡献

| PR | Bug ID | 标题 |
|----|--------|------|
| [#4550](https://github.com/openjdk/jdk/pull/4550) | 8261441 | JFR: Filename expansion |
| [#4573](https://github.com/openjdk/jdk/pull/4573) | 8269225 | JFR.stop misses written info |
| [#4631](https://github.com/openjdk/jdk/pull/4631) | 8268298 | jdk/jfr/api/consumer/log/TestVerbosity.java fix |
| [#2088](https://github.com/openjdk/jdk/pull/2088) | 8259808 | Add JFR event to detect GC locker stall |
| [#2138](https://github.com/openjdk/jdk/pull/2138) | 8259956 | ChunkInputStream#available fix |
| [#17632](https://github.com/openjdk/jdk/pull/17632) | 8324974 | JFR: EventCompilerPhase should be UNTIMED |
| [#17903](https://github.com/openjdk/jdk/pull/17903) | 8326111 | JFR: Cleanup for JFR_ONLY |
| [#17907](https://github.com/openjdk/jdk/pull/17907) | 8326127 | JFR: Add SafepointCleanupTask to hardToTestEvents |
| [#17307](https://github.com/openjdk/jdk/pull/17307) | 8323188 | JFR: Needless RESOURCE_ARRAY |

→ [完整 PR 列表 (36)](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3AD-D-H+is%3Aclosed+label%3Aintegrated)

---

## 协作网络 (Sponsor)

D-D-H 作为 Committer 为以下 Alibaba Author 的 PR 提供 /sponsor:

| 贡献者 | 被 sponsor 的 PR |
|--------|-----------------|
| [Long Yang](long-yang.md) (@yanglong1010) | JFR/Runtime PRs |
| [Liang Mao](liang-mao.md) (@mmyxym) | GC PRs |
| [sandlerwang](sandlerwang.md) | AArch64/GC PRs |
| [Lingjun Cao](lingjun-cao.md) (@lingjun-cg) | DecimalFormat PRs |

---

> **文档等级**: L2
> **创建时间**: 2026-03-23
