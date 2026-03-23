# 腾讯

> 构建稳定性、编译器测试和 GC 优化

[← 返回组织索引](README.md)

---
## 目录

1. [概览](#1-概览)
2. [贡献者](#2-贡献者)
3. [主要领域](#3-主要领域)
4. [关键贡献](#4-关键贡献)
5. [贡献时间线](#5-贡献时间线)
6. [影响的模块](#6-影响的模块)
7. [Tencent Kona](#7-tencent-kona)
8. [协作网络](#8-协作网络)
9. [数据来源](#9-数据来源)
10. [相关链接](#10-相关链接)

---


## 1. 概览

腾讯是 OpenJDK 的重要贡献者，通过 Kona JDK 团队积极参与上游开发。腾讯最大的贡献者 **Jie Fu (傅杰)** 以 187 个 Integrated PRs 位居 OpenJDK 全球贡献者前列，主要专注于构建稳定性、编译器测试修复和跨平台兼容性。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 198+ |
| **贡献者数** | 3 |
| **活跃时间** | 2020 - 至今 |
| **主要领域** | 构建稳定性, 编译器, GC, 容器, Vector API |
| **Kona** | [Tencent Kona](https://github.com/Tencent/TencentKona-17) |

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。OpenJDK Committer 使用 `@openjdk.org` 邮箱提交代码，因此 git commits 按邮箱统计不准确。

---

## 2. 贡献者

| 排名 | 贡献者 | GitHub | PRs | 角色 | 主要领域 | 档案 |
|------|--------|--------|-----|------|----------|------|
| 1 | Jie Fu (傅杰) | [@DamonFool](https://github.com/DamonFool) | 187 | Committer | 构建稳定性, 编译器, GC | [详情](../../by-contributor/profiles/jie-fu.md) |
| 2 | Caspar Wang (王超) | [@casparcwang](https://github.com/casparcwang) | 6 | Author | C2 编译器, 容器, ZGC | - |
| 3 | Tongbao Zhang | [@tbzhang](https://github.com/tbzhang) | 5 | Author | G1 GC | [详情](../../by-contributor/profiles/tongbao-zhang.md) |

**总计**: 198+ PRs

### Jie Fu (傅杰) — 核心贡献者

Jie Fu 是腾讯 Kona JDK 团队的核心成员，也是 OpenJDK 全球最活跃的贡献者之一 (187 PRs)。他的贡献特点是：

- **构建稳定性守护者**: 126+ PRs 修复各种构建问题（GCC 版本兼容、跨平台编译、Minimal/Zero VM 构建等）
- **编译器测试修复**: 44+ PRs 修复 C2/C1 编译器相关测试
- **Vector API 质量保障**: 29+ PRs 修复 Vector API 测试和兼容性
- **GC 修复**: 30+ PRs 涉及 G1/ZGC/Shenandoah GC 修复
- **Zero VM 维护**: 12+ PRs 修复 Zero VM 构建和运行问题
- **容器支持**: 5+ PRs 改进 Docker/cgroup 支持

> **年度贡献**: 2020 (29) → 2021 (81) → 2022 (48) → 2023 (19) → 2024 (7) → 2025-26 (3)

### Caspar Wang (王超) — C2 编译器与容器

Caspar Wang 专注于 C2 编译器正确性修复和容器资源检测：

- C2 编译器崩溃修复 (PhaseIdealLoop, PhaseCFG)
- ZGC 并发标记修复
- 容器 cgroup 资源检测修复

### Tongbao Zhang — G1 GC

Tongbao Zhang 专注于 G1 GC 正确性修复：

- G1 压缩指针边界计算修复
- G1 对齐检查修复
- Shenandoah GC 测试修复

> **角色说明**:
> - **Committer**: 有直接推送权限的贡献者 ([详情](https://openjdk.org/guide/))
> - **Author**: 可以创建和提交更改的贡献者 ([详情](https://dev.java/contribute/openjdk/))

---

## 3. 主要领域

### 构建稳定性 (Build Stability)

腾讯最重要的贡献领域。Jie Fu 被社区认为是 OpenJDK 构建稳定性的守护者：

| 子领域 | PRs | 说明 |
|--------|-----|------|
| GCC 版本兼容 | 20+ | 修复 GCC8/GCC11 等版本的构建警告和错误 |
| Minimal/Zero VM | 15+ | 修复精简 VM 配置的构建问题 |
| 跨平台构建 | 15+ | 修复 x86_32, PPC, AArch64 等平台构建 |
| C2 禁用构建 | 10+ | 修复禁用 C2 编译器后的构建问题 |
| Clang 兼容 | 5+ | 修复 Clang 编译器的构建问题 |
| Release VM 测试 | 30+ | 修复仅在 Release VM 上失败的测试 |

### 编译器 (Compiler)

| 子领域 | 贡献者 | PRs | 说明 |
|--------|--------|-----|------|
| C2 测试修复 | Jie Fu | 30+ | IR Framework, 向量化测试等 |
| C2 崩溃修复 | Caspar Wang | 4 | PhaseIdealLoop, PhaseCFG 崩溃 |
| CompileCommand | Jie Fu | 2+ | 编译器命令解析修复 |

### GC (垃圾收集)

| 子领域 | 贡献者 | PRs | 说明 |
|--------|--------|-----|------|
| G1 GC 修复 | Tongbao Zhang | 3 | 压缩指针、对齐检查 |
| ZGC 修复 | Caspar Wang, Jie Fu | 5+ | 并发标记、构建修复 |
| Shenandoah 修复 | Caspar Wang, Jie Fu | 3+ | 锁排名、构建修复 |
| GC 构建修复 | Jie Fu | 15+ | 各 GC 的构建和测试修复 |

### Vector API

| 子领域 | 贡献者 | PRs | 说明 |
|--------|--------|-----|------|
| 测试修复 | Jie Fu | 20+ | VectorAPI 测试在各平台/配置的修复 |
| 正确性修复 | Jie Fu | 5+ | VectorReinterpret, MaskLoad 等修复 |
| 文档修复 | Jie Fu | 2+ | Vector API 文档错误修正 |
| x86_32 支持 | Jie Fu | 3+ | Vector API 在 32 位 x86 上的修复 |

### 容器化 (Container)

| 子领域 | 贡献者 | PRs | 说明 |
|--------|--------|-----|------|
| cgroup 检测 | Caspar Wang | 1 | 容器资源限制检测修复 |
| Docker 测试 | Jie Fu | 3+ | 容器测试修复 |
| Swap 检测 | Jie Fu | 1+ | 容器 Swap 空间检测 |

### 安全 (Security)

| 子领域 | 贡献者 | PRs | 说明 |
|--------|--------|-----|------|
| JGSS 清理 | (Tencent copyright) | 2 | GssName/GssContext Cleaner |
| SSL 异常 | (Tencent copyright) | 5+ | SSL 异常构造器增强 |
| PasswordCallback | (Tencent copyright) | 2 | 密码清理机制 |

> **注**: 部分安全领域的代码由 Tencent 贡献测试用例（Tencent 版权），实际 PR 作者可能是其他组织的贡献者。

---

## 4. 关键贡献

### Jie Fu (傅杰) 代表性 PR

| PR | Bug ID | 标题 | 领域 | 年份 |
|----|--------|------|------|------|
| #6933 | 8279258 | Auto-vectorization enhancement for 2D array | 向量化 | 2022 |
| #10262 | 8293774 | Improve TraceOptoParse to dump bytecode name | 编译器 | 2022 |
| #6142 | 8276066 | Reset LoopPercentProfileLimit for x86 | 性能 | 2021 |
| #7176 | 8280457 | Duplicate dprecision_rounding implementation | 代码清理 | 2022 |
| #7059 | 8279947 | Remove redundant gvn.transform calls | 编译器 | 2021 |
| #8291 | 8284992 | Fix misleading Vector API doc for LSHR operator | 文档 | 2022 |
| #6569 | 8277854 | GCCardSizeInBytes upper bound for 32-bit | GC | 2021 |
| #28956 | 8374200 | TestCgroupMetrics.java fails with common prefix | 容器 | 2025 |

### Caspar Wang (王超) 代表性 PR

| PR | Bug ID | 标题 | 领域 | 年份 |
|----|--------|------|------|------|
| #5140 | 8272570 | C2: crash in PhaseCFG::global_code_motion | 编译器 | 2021 |
| #5142 | 8272574 | C2: Bad graph detected in build_loop_late | 编译器 | 2021 |
| #6099 | 8275854 | C2: assert(stride_con != 0) failed | 编译器 | 2021 |
| #10329 | 8293978 | Duplicate simple loop back-edge crash | 编译器 | 2022 |
| #10193 | 8293472 | Incorrect container resource limit detection | 容器 | 2022 |
| #3011 | 8263579 | ZGC: Concurrent mark hangs with debug loglevel | GC | 2021 |

### Tongbao Zhang 代表性 PR

| PR | Bug ID | 标题 | 领域 | 年份 |
|----|--------|------|------|------|
| #24541 | 8354145 | G1: UseCompressedOops boundary calculation | G1 GC | 2025 |
| - | 8293782 | Shenandoah lock rank check fix | Shenandoah | 2022 |
| - | 8274259 | G1 alignment check fix | G1 GC | 2021 |

---

## 5. 贡献时间线

```
2020: ████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  29 PRs (Jie Fu 开始贡献)
2021: ████████████████████████████████████████████████████░░  87 PRs (峰值年, +Caspar Wang)
2022: ██████████████████████████████████░░░░░░░░░░░░░░░░░░░  54 PRs (+Tongbao Zhang)
2023: ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  20 PRs
2024: █████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   9 PRs
2025: ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   3 PRs
```

> **总计**: 198+ PRs (2020-2026)

---

## 6. 影响的模块

| 模块 | 文件数 | 说明 |
|------|--------|------|
| HotSpot 编译器 | 50+ | C2/C1 编译器修复和测试 |
| HotSpot GC | 30+ | G1/ZGC/Shenandoah 修复 |
| Vector API | 29+ | 向量化 API 测试和修复 |
| 构建系统 | 30+ | 跨平台构建修复 |
| 容器/cgroup | 5+ | Docker/cgroup 支持 |
| Zero VM | 12+ | Zero VM 构建和运行修复 |
| Runtime/CDS | 15+ | 运行时和 CDS 修复 |
| Security/SSL | 7+ | SSL 异常、JGSS、密码清理 |
| x86 数学库 | 3 | stubGenerator 数学内联函数 |

---

## 7. Tencent Kona

腾讯维护自己的 JDK 发行版 Kona：

| 特性 | 说明 |
|------|------|
| **基于** | OpenJDK |
| **支持版本** | Kona 8 / 11 / 17 / 21 |
| **特点** | 云原生优化，腾讯云内部默认 JDK |
| **许可** | GPLv2 |
| **认证** | Java SE 兼容性认证 |

| 版本 | GitHub 仓库 |
|------|-------------|
| Kona 8 | [Tencent/TencentKona-8](https://github.com/Tencent/TencentKona-8) |
| Kona 11 | [Tencent/TencentKona-11](https://github.com/Tencent/TencentKona-11) |
| Kona 17 | [Tencent/TencentKona-17](https://github.com/Tencent/TencentKona-17) |
| Kona 21 | [Tencent/TencentKona-21](https://github.com/Tencent/TencentKona-21) |

> Tencent Kona 是腾讯云计算和其他 Java 应用的默认 JDK，提供季度更新的长期支持。

---

## 8. 协作网络

### 核心团队与外部协作

```
                    ┌─────────────────────────────┐
                    │      Tencent (腾讯)          │
                    │   Build / Compiler / GC      │
                    └─────────────┬───────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
          ▼                       ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │ Jie Fu   │           │ Caspar   │           │ Tongbao  │
    │ (187 PRs)│           │ Wang     │           │ Zhang    │
    │ 构建/编译 │           │ (6 PRs)  │           │ (5 PRs)  │
    │ GC/Vector │           │ C2/容器   │           │ G1 GC   │
    └────┬─────┘           └────┬─────┘           └────┬─────┘
         │                      │                      │
         ▼                      ▼                      ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │ 审查协作   │           │ 审查协作   │           │ 审查协作   │
    │ Oracle    │           │ Oracle    │           │ Oracle    │
    │ 编译器团队 │           │ C2 团队   │           │ G1 GC    │
    │ Vladimir  │           │ Christian │           │ Thomas   │
    │ Kozlov    │           │ Hagedorn  │           │ Schatzl  │
    └──────────┘           └──────────┘           └──────────┘
```

### 与其他中国企业对比

| 组织 | PRs | 主要领域 | 特点 |
|------|-----|----------|------|
| **腾讯** | 198+ | 构建稳定性, 编译器, GC, Vector API | 广度最大，构建守护者 |
| **阿里巴巴** | 121 | 核心库性能, ClassFile API | 深度优化导向 |
| **字节跳动** | 25 | RISC-V 向量指令 | 新兴架构支持 |
| **ISCAS PLCT** | 20+ | RISC-V | 学术机构主导 |
| **龙芯** | 30+ | LoongArch | 国产架构支持 |

> **注**: 腾讯以 198+ PRs 位居中国企业 OpenJDK 上游贡献第一名。

---

## 9. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-23
- **验证方式**: OpenJDK 源码 `Copyright (C) [year], Tencent` 版权声明反查 PR 作者

---

## 10. 相关链接

- [Tencent Kona JDK](https://tencent.github.io/konajdk/)
- [TencentKona-17 GitHub](https://github.com/Tencent/TencentKona-17)
- [TencentKona-21 GitHub](https://github.com/Tencent/TencentKona-21)
- [Jie Fu GitHub](https://github.com/DamonFool)
- [腾讯云 Java](https://cloud.tencent.com/)

---

[← 返回组织索引](README.md)

---

> **文档版本**: 2.0
> **最后更新**: 2026-03-23
> **本次更新**:
> - **重大发现**: Jie Fu (傅杰, @DamonFool) 是腾讯核心贡献者，187 个 Integrated PRs，之前完全遗漏
> - **方法**: 通过 openjdk/jdk 源码中 `Copyright (C) [year], Tencent` 版权声明反查 git commit 和 PR 作者
> - **PR 总数更正**: 从 10+ 更正为 198+ (Jie Fu 187 + Caspar Wang 6 + Tongbao Zhang 5)
> - **新增**: Caspar Wang (王超, @casparcwang, 6 PRs) 贡献者
> - **新增**: 按子领域的详细贡献分析 (构建稳定性、编译器、GC、Vector API、容器)
> - **新增**: Jie Fu 年度 PR 统计 (2020:29 → 2021:81 → 2022:48 → 2023:19 → 2024:7)
> - **新增**: Tencent Kona 发行版详细信息 (4 个版本)
> - **更新**: 贡献时间线反映真实数据
> - **更新**: 影响模块范围大幅扩展
> - **更新**: 与其他中国企业贡献对比
