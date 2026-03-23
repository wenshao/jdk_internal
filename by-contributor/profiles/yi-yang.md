# Yi Yang (杨易)

> C2/C1 编译器优化、HeapDump 分段、HotSpot Runtime 改进

---
## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Yi Yang (杨易) |
| **当前组织** | [阿里巴巴 (Alibaba) - 云基础设施部](/contributors/orgs/alibaba.md) |
| **GitHub** | [@y1yang0](https://github.com/y1yang0) (2.3k followers) |
| **OpenJDK** | Committer (yyang) — [CFV 2021-05](https://mail.openjdk.org/pipermail/jdk-dev/2021-May/) |
| **PRs** | [57 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Ay1yang0+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | C2 编译器, C1 编译器, HeapDump, HotSpot Runtime, CDS, JFR |
| **活跃时间** | 2021 - 2024 (高峰期 2021: 45 PRs) |
| **著作** | 《深入解析Java虚拟机HotSpot》(机械工业出版社, 2020) |
| **个人项目** | [YVM](https://github.com/y1yang0/YVM) (C++ 实现的 JVM), [Yarrow](https://github.com/y1yang0/Yarrow) (JVMCI 优化编译器) |
| **归属确认** | [Dragonwell 12 PRs](https://github.com/dragonwell-project/dragonwell11/pulls?q=author:y1yang0) + sponsor wenshao/sendaoYan + 审查 D-D-H |

> **数据调查时间**: 2026-03-23

---

## 贡献概览

| 年份 | PRs | 主要工作 |
|------|-----|----------|
| **2021** | 45 | C1/C2 编译器优化, CDS, JFR, 代码清理 |
| **2022** | 5 | C2 崩溃修复, JVM_LEAF 优化, Preconditions.checkIndex |
| **2023** | 5 | HeapDump 分段优化, OptimizeStringConcat, HotSpotVM 重构 |
| **2024** | 2 | jcmd Compiler.codecache, HeapDump 优化 |
| **总计** | **57** | |

---

## 代表性工作

### 核心贡献

| PR | Bug ID | 标题 | 类型 | 分析 |
|----|--------|------|------|------|
| [#13667](https://github.com/openjdk/jdk/pull/13667) | 8306441 | Two phase segmented heap dump | **核心功能** | [详情](/by-pr/8306/8306441.md) |
| [#15245](https://github.com/openjdk/jdk/pull/15245) | 8314021 | Optimize segmented heap file merging | 性能优化 | [详情](/by-pr/8314/8314021.md) |
| [#6096](https://github.com/openjdk/jdk/pull/6096) | 8273585 | String.charAt performance degrades | **回归修复** | [详情](/by-pr/8273/8273585.md) |
| [#12680](https://github.com/openjdk/jdk/pull/12680) | 8143900 | OptimizeStringConcat opaque dependency | C2 优化 | [详情](/by-pr/8143/8143900.md) |
| [#7105](https://github.com/openjdk/jdk/pull/7105) | 8275775 | Add jcmd VM.classes | 功能增强 | [详情](/by-pr/8275/8275775.md) |
| [#7760](https://github.com/openjdk/jdk/pull/7760) | 8282883 | Use JVM_LEAF to avoid ThreadStateTransition | 性能优化 | [详情](/by-pr/8282/8282883.md) |

### C2 编译器优化

| PR | Bug ID | 标题 | 分析 |
|----|--------|------|------|
| [#5266](https://github.com/openjdk/jdk/pull/5266) | 8273021 | Improve Add and Xor ideal optimizations | [详情](/by-pr/8273/8273021.md) |
| [#4920](https://github.com/openjdk/jdk/pull/4920) | 8271203 | assert failed in subtype check | [详情](/by-pr/8271/8271203.md) |
| [#5705](https://github.com/openjdk/jdk/pull/5705) | 8274328 | Redundant CFG edges fixup | [详情](/by-pr/8274/8274328.md) |
| [#9695](https://github.com/openjdk/jdk/pull/9695) | 8290432 | assert(node->_last_del == _last) | [详情](/by-pr/8290/8290432.md) |
| [#9777](https://github.com/openjdk/jdk/pull/9777) | 8288204 | GVN Crash: correct memory chain | [详情](/by-pr/8288/8288204.md) |
| [#7770](https://github.com/openjdk/jdk/pull/7770) | 8272493 | Suboptimal code around Preconditions.checkIndex | [详情](/by-pr/8272/8272493.md) |

### C1 编译器优化

| PR | Bug ID | 标题 |
|----|--------|------|
| [#3615](https://github.com/openjdk/jdk/pull/3615) | 8265518 | C1: Intrinsic support for Preconditions.checkIndex |
| [#3616](https://github.com/openjdk/jdk/pull/3616) | 8265711 | C1: Intrinsify Class.getModifier method |
| [#3965](https://github.com/openjdk/jdk/pull/3965) | 8266798 | C1: More types for LoopInvariantCodeMotion |
| [#3966](https://github.com/openjdk/jdk/pull/3966) | 8266874 | Clean up C1 canonicalizer for TableSwitch/LookupSwitch |
| [#4083](https://github.com/openjdk/jdk/pull/4083) | 8267239 | C1: RangeCheckElimination for % operator |
| [#3935](https://github.com/openjdk/jdk/pull/3935) | 8266189 | Remove C1 "IfInstanceOf" instruction |

### HotSpot Runtime / CDS / JFR

| PR | Bug ID | 标题 |
|----|--------|------|
| [#1904](https://github.com/openjdk/jdk/pull/1904) | 8256156 | JFR: Allow 'jfr' tool to show metadata without recording |
| [#3244](https://github.com/openjdk/jdk/pull/3244) | 8264337 | VM crashed when -XX:+VerifySharedSpaces |
| [#3323](https://github.com/openjdk/jdk/pull/3323) | 8264644 | Add PrintClassLoaderDataGraphAtExit |
| [#3320](https://github.com/openjdk/jdk/pull/3320) | 8264634 | CollectCLDClosure collects duplicated CLDs |
| [#6672](https://github.com/openjdk/jdk/pull/6672) | 8278125 | Some preallocated OOMEs missing stack trace |
| [#11823](https://github.com/openjdk/jdk/pull/11823) | 8299518 | HotSpotVirtualMachine shared code across platforms |
| [#17445](https://github.com/openjdk/jdk/pull/17445) | 8323795 | jcmd Compiler.codecache should print total size |

→ [完整 PR 列表 (57)](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Ay1yang0+is%3Aclosed+label%3Aintegrated)

---

## 协作网络

| 关系 | 贡献者 | 说明 |
|------|--------|------|
| /sponsor | [Shaojin Wen](shaojin-wen.md) | 为 wenshao 的核心库 PR sponsor |
| /sponsor | [SendaoYan](sendaoyan.md) | 为 sendaoYan 的测试 PR sponsor |
| /sponsor | [Lingjun Cao](lingjun-cao.md) | 为 lingjun-cg 的 DecimalFormat PR sponsor |
| 审查 | [Denghui Dong](denghui-dong.md) | 审查 D-D-H 的 HotSpot PR |
| 被审查 | Vladimir Kozlov (Oracle) | C2 编译器 PR 审查者 |

---

> **文档等级**: L2
> **创建时间**: 2026-03-23
