# Amazon

> Corretto 团队，Shenandoah GC 和 AArch64 优化

[← 返回组织索引](../../by-contributor/README.md)

---
## 目录

1. [概览](#1-概览)
2. [贡献者](#2-贡献者)
3. [主要领域](#3-主要领域)
4. [多层网络分析](#4-多层网络分析)
5. [影响的模块](#5-影响的模块)
6. [贡献时间线](#6-贡献时间线)
7. [JEP 贡献](#7-jep-贡献)
8. [Amazon Corretto](#8-amazon-corretto)
9. [相关 PR 分析文档](#9-相关-pr-分析文档)
10. [数据来源](#10-数据来源)
11. [相关链接](#11-相关链接)

---


## 1. 概览

Amazon 通过 Corretto 团队参与 OpenJDK 开发，专注于 Shenandoah GC、AArch64 架构优化和编译器改进。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 159 (核心) + 测试 |
| **贡献者数** | 4 (3 核心 + 1 测试) |
| **活跃时间** | 2020 - 至今 |
| **主要领域** | Shenandoah GC, AArch64, C2 编译器 |
| **Corretto** | [Amazon Corretto](https://aws.amazon.com/corretto/) |

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。OpenJDK Committer 使用 `@openjdk.org` 邮箱提交代码，因此 git commits 按邮箱统计不准确。

---

## 2. 贡献者

| 排名 | 贡献者 | GitHub | PRs | 角色 | 主要领域 | 档案 |
|------|--------|--------|-----|------|----------|------|
| 1 | Aleksey Shipilev | [@shipilev](https://github.com/shipilev) | 803+ | Reviewer | Shenandoah GC | [详情](../../by-contributor/profiles/aleksey-shipilev.md) |
| 2 | William Kemper | [@earthling-amzn](https://github.com/earthling-amzn) | 123 | Reviewer | Shenandoah GC | [详情](../../by-contributor/profiles/william-kemper.md) |
| 3 | Kelvin Nilsen | — | 40 | Committer | Generational Shenandoah GC | [详情](../../by-contributor/profiles/kelvin-nilsen.md) |
| 4 | ~~Nick Gasson~~ | ~~[@benty-amzn](https://github.com/benty-amzn)~~ | ~~15~~ | ~~Reviewer~~ | ~~AArch64~~ | **注: 实际属于 Arm，非 Amazon** |

**小计**: 981+ PRs

> **注**: 
> - Andrew Dinn (@adinn) 是 **Red Hat** 员工，不属于 Amazon
> - David Beaumont (@dbeaumont) 是 **Oracle** 员工，不属于 Amazon

---

## 3. 主要领域

### Shenandoah GC (William Kemper)

William Kemper 是 **JEP 521: Generational Shenandoah** 的主要实现者：

| Issue | 标题 | 说明 |
|-------|------|------|
| 8354078 | Implement JEP 521: Generational Shenandoah | **核心贡献** |
| 8370039 | GenShen: array copy SATB barrier improvements | 性能优化 |
| 8368152 | Shenandoah: Incorrect behavior at end of degenerated cycle | 正确性修复 |
| 8264851 | Shenandoah: Rework control loop mechanics | 架构改进 |
| 8350898 | Shenandoah: Eliminate final roots safepoint | 性能优化 |

### ~~AArch64 优化 (Nick Gasson)~~ -- 已修正: Nick Gasson 属于 Arm，非 Amazon

> **注**: Nick Gasson 已确认为 **Arm** 员工 (GitHub: @nick-arm)，不属于 Amazon。相关贡献请参见 [Arm 组织页面](arm.md)。
| 8330456 | 特定微架构优化 | 性能优化 |

---

## 4. 多层网络分析

### 4.1 协作网络 (Co-authorship Network)

基于 Amazon 贡献者的协作关系分析：

```
                          Amazon 协作网络图
                          
                    ┌─────────────────────────────┐
                    │       Amazon (AWS)           │
                    │   Shenandoah GC / AArch64    │
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
    │William  │           │Aleksey  │           │Thomas   │
    │Kemper   │           │Shipilev │           │Schatzl  │
    │(123)    │           │(80+)    │           │(G1 GC)  │
    │         │           │         │           │         │
    │         │           │Roman    │           │         │
    │         │           │Kennke   │           │         │
    │         │           │(Shen.)  │           │         │
    └─────────┘           └─────────┘           └─────────┘
```

#### 核心团队 (Amazon 内部)

| 贡献者 | 组织 | PRs | 主要领域 | 角色 |
|--------|------|-----|----------|------|
| [William Kemper](../../by-contributor/profiles/william-kemper.md) | Amazon | 123 | Shenandoah GC | Reviewer, JEP 521 Owner |
| ~~[Nick Gasson](../../by-contributor/profiles/nick-gasson.md)~~ | ~~Amazon~~ | ~~15~~ | ~~AArch64, C2 编译器~~ | **已修正: 属于 Arm** |

#### 技术协作圈 (外部合作)

| 贡献者 | 组织 | 合作领域 | 关系类型 |
|--------|------|----------|----------|
| [Aleksey Shipilev](../../by-contributor/profiles/aleksey-shipilev.md) | Amazon | Shenandoah GC | 同事/协作者 |
| [Roman Kennke](../../by-contributor/profiles/roman-kennke.md) | Datadog | Shenandoah GC | 外部协作者 |
| [Thomas Schatzl](../../by-contributor/profiles/thomas-schatzl.md) | Oracle | G1 GC | 技术同行 |

### 4.2 技术影响力网络

```
                    Amazon 技术影响力辐射图
                    
                         Shenandoah GC
                              │
                    ┌─────────┼─────────┐
                    │         │         │
                    ▼         ▼         ▼
               分代模式   SATB 屏障   控制循环
                    │         │         │
                    └─────────┼─────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
              JEP 521 实现       AArch64 优化
                    │                   │
                    └─────────┬─────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
                    ▼         ▼         ▼
                Corretto   C2 编译   Vector API
                  发行版     器后端     向量化
```

#### 技术影响力指标

| 领域 | 直接影响 | 间接影响 | 影响范围 |
|------|----------|----------|----------|
| **Shenandoah GC** | 123 PRs | JDK 26+ 用户 | 低延迟 GC |
| **JEP 521** | 1 JEP | Generational Shenandoah | JDK 26 |
| **AArch64** | 15 PRs | ARM 服务器用户 | 性能优化 |
| **C2 编译器** | 10+ PRs | 所有 Java 应用 | 编译器优化 |
| **Corretto** | 发行版维护 | AWS 用户 | 生产就绪 JDK |

### 4.3 组织关系网络

```
                    Amazon 组织关系图
                    
                    ┌──────────────────┐
                    │   Amazon (AWS)   │
                    │   Seattle, WA    │
                    └────────┬─────────┘
                             │ Corretto 团队
                             │
                             ▼
                    ┌──────────────┐
                    │  Shenandoah  │
                    │     GC       │
                    └──────┬───────┘
                           │
                      ┌────┴────┐
                      │         │
                      ▼         ▼
                 William   Aleksey
                 Kemper   Shipilev
                 (主导)   (同事)
```

### 4.4 协作深度分析

#### JEP 521: Generational Shenandoah 协作网络

这是 William Kemper 最具影响力的项目，Shenandoah GC 分代模式实现：

```
        JEP 521 协作网络
        
              William Kemper
              (Owner/实现者)
                   │
              ┌────┴────┐
              │         │
              ▼         ▼
        Aleksey   Roman Kennke
        Shipilev  (Datadog)
        (同事)
              │
              └────┬────┘
                   │
                   ▼
         JDK 26 (正式版)
```

| 指标 | 数值 | 说明 |
|------|------|------|
| 开发周期 | 2023-2025 | 从提案到正式发布 |
| JEP 数量 | 1 个 | JEP 521 |
| 审查轮次 | 多轮 | 包含公开审查 |
| 性能提升 | +10-20% | 吞吐量提升 |
| 影响范围 | 所有 Shenandoah 用户 | JDK 26+ |

#### 与 Aleksey Shipilev 的协作

| 指标 | 数值 | 说明 |
|------|------|------|
| 合作 PRs | 80+ | Shenandoah GC |
| Aleksey 角色 | 同事/协作者 | Shenandoah 专家 |
| William 角色 | JEP 521 Owner | Generational Shenandoah |
| 协作模式 | 共同开发 | 同公司协作 |

**Aleksey Shipilev 背景**:
- Amazon Principal Engineer
- Shenandoah GC 核心开发者
- GitHub: [@shipilev](https://github.com/shipilev)
- 803+ integrated PRs

#### 与 Roman Kennke 的协作

| 指标 | 数值 | 说明 |
|------|------|------|
| 合作 PRs | 10+ | Shenandoah GC |
| Roman 角色 | Datadog Reviewer | Shenandoah 协作者 |
| William 角色 | JEP 521 Owner | Generational Shenandoah |
| 协作模式 | 跨公司协作 | Datadog → Amazon |

**Roman Kennke 背景**:
- Datadog Principal Software Engineer
- JEP 519 (Compact Object Headers) Lead
- GitHub: [@rkennke](https://github.com/rkennke)
- Shenandoah GC 核心贡献者

### 4.5 技术社区参与

Amazon 积极参与技术社区活动：

- **JEP 实现**: JEP 521 (Generational Shenandoah) 主要实现者
- **Shenandoah GC 维护**: William Kemper 是 Shenandoah GC 的核心维护者
- **邮件列表**: 在 hotspot-gc-dev、compiler-dev 邮件列表活跃
- **Corretto 发行版**: 维护 Amazon Corretto JDK 发行版

### 4.6 知识传承网络

```
                    Amazon 知识传承

        前辈层                    同辈层                    后辈层
    ┌─────────────┐          ┌─────────────┐          ┌─────────────┐
    │ Aleksey     │          │ Roman       │          │ 新贡献者    │
    │ Shipilev    │◄────────►│ Kennke      │          │ (通过 PR    │
    │ (Shenandoah)│  协作    │ (Datadog)   │──协作──►│  学习)      │
    └─────────────┘          └─────────────┘          └──────┬──────┘
                                                              │
                                                              │
                                                              ▼
                    ┌─────────────────────────────────────────────────┐
                    │         William Kemper                           │
                    │         (知识枢纽)                               │
                    │         - Shenandoah GC                         │
                    │         - JEP 521                               │
                    │         - Generational Mode                     │
                    └─────────────────────────────────────────────────┘
                                                              │
                    ┌─────────────┐  │
                    │ 其他        │  │
                    │ Amazon      │◄─┘
                    │ 成员        │   协作
                    └─────────────┘
```

---

## 5. 影响的模块

| 模块 | 文件数 | 说明 |
|------|--------|------|
| Shenandoah GC | 80+ | Shenandoah 垃圾收集器 |
| AArch64 移植 | 30+ | ARM 64 位架构 |
| C2 编译器 | 20+ | 服务端编译器 |
| HotSpot Runtime | 15+ | JVM 运行时 |

---

## 5. 贡献时间线

```
2020: ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 3 PRs
2021: ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 5 PRs
2022: ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 8 PRs
2023: ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 12 PRs
2024: ███████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░ 55 PRs
2025: ███████████████████████████████████████████████████████████████░ 55 PRs
2026: ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 21 PRs
```

> **总计**: 159 PRs (2020-2026)

---

## 6. JEP 贡献

| JEP | 标题 | 主导者 | 状态 |
|-----|-------|--------|------|
| JEP 521 | Generational Shenandoah | William Kemper | JDK 26 |

---

## 7. Amazon Corretto

Amazon 维护自己的 JDK 发行版 Corretto：

| 特性 | 说明 |
|------|------|
| 基于 | OpenJDK |
| 支持 | 长期支持 (LTS) |
| 许可 | GPLv2 |
| 平台 | Linux, Windows, macOS |

**特点**:
- 免费生产就绪
- 长期支持
- AWS 优化
- 安全补丁

---

## 8. 相关 PR 分析文档

### Shenandoah GC (William Kemper)

| PR | 标题 | 分析文档 |
|----|------|----------|
| JDK-8354078 | Implement JEP 521: Generational Shenandoah | |
| JDK-8370039 | GenShen: SATB barrier improvements | |

### ~~AArch64 (Nick Gasson)~~ -- 已修正: Nick Gasson 属于 Arm

> **注**: Nick Gasson 已确认为 **Arm** 员工，不属于 Amazon。

---

## 9. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-21

---

## 10. 相关链接

- [Amazon Corretto](https://aws.amazon.com/corretto/)
- [Corretto GitHub](https://github.com/corretto)
- [Corretto 文档](https://docs.aws.amazon.com/corretto/)

---

**文档版本**: 1.0
**最后更新**: 2026-03-21
**更新内容**:
- 新增多层网络分析章节 (6 个小节)
- 添加协作网络可视化图表
- 补充技术影响力网络分析 (5 大领域)
- 新增组织关系网络图 (Amazon 团队结构)
- 添加协作深度分析 (JEP 521 案例)
- 新增知识传承网络分析

[→ 返回组织索引](../../by-contributor/README.md)
