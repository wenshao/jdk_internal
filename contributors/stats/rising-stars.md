# 新星贡献者

> 近年加入并快速成长的 OpenJDK 贡献者 (2023-2026)

---
## 目录

1. [新星榜单](#1-新星榜单)
2. [按领域新星](#2-按领域新星)
3. [中国新星 (2023-2026)](#3-中国新星-2023-2026)
4. [新星成长路径](#4-新星成长路径)
5. [新贡献者指南](#5-新贡献者指南)
6. [企业新星计划](#6-企业新星计划)
7. [新星影响力](#7-新星影响力)
8. [数据说明](#8-数据说明)
9. [相关页面](#9-相关页面)

---


## 1. 新星榜单

### 2025 新星

| 贡献者 | 首次贡献 | Commits | 领域 | 组织 | 亮点 |
|--------|----------|---------|------|------|------|
| [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | 2024-05 | 27 | 核心库/性能 | 阿里巴巴 | 字符串拼接优化 (+40% 启动) |

### 2024 新星

| 贡献者 | 首次贡献 | Commits | 领域 | 组织 | 亮点 |
|--------|----------|---------|------|------|------|
| [Chen Liang](/by-contributor/profiles/chen-liang.md) | 2023 | 36 | 反射/ClassFile | Oracle | ClassFile API |
| [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | 2023 | 42 | C2 编译器 | Oracle | 编译器优化 |
| Anjian-Wen | 2024 | 12 | RISC-V | 字节跳动 | 架构移植 |

### 2023 新星

| 贡献者 | 首次贡献 | Commits | 领域 | 组织 | 亮点 |
|--------|----------|---------|------|------|------|
| [William Kemper](/by-contributor/profiles/william-kemper.md) | 2022 | 34 | Shenandoah GC | Amazon | GC 优化 |
| Felix Nensemba | 2023 | 25 | GC | Amazon | 性能优化 |
| Dingli Zhang | 2023 | 11 | RISC-V | ISCAS | 架构移植 |

---

## 2. 按领域新星

### GC 领域

| 贡献者 | 首次贡献 | Commits | GC 类型 | 组织 |
|--------|----------|---------|---------|------|
| [William Kemper](/by-contributor/profiles/william-kemper.md) | 2022 | 34 | Shenandoah | Amazon |
| Felix Nensemba | 2023 | 25 | Shenandoah | Amazon |
| Y. S. K. Nilsen | 2023 | 20 | 各类 GC | Amazon |

### 编译器领域

| 贡献者 | 首次贡献 | Commits | 编译器 | 组织 |
|--------|----------|---------|--------|------|
| [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | 2023 | 42 | C2 | Oracle |

### 核心库领域

| 贡献者 | 首次贡献 | Commits | 主要工作 | 组织 |
|--------|----------|---------|----------|------|
| [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | 2024 | 27 | 字符串优化 | 阿里巴巴 |

### 架构移植

| 贡献者 | 首次贡献 | Commits | 架构 | 组织 |
|--------|----------|---------|------|------|
| Anjian-Wen | 2024 | 12 | RISC-V | 字节跳动 |
| Dingli Zhang | 2023 | 11 | RISC-V | ISCAS |
| sunguoyun | 2024 | 14 | LoongArch | 龙芯 |

---

## 3. 中国新星 (2023-2026)

### 阿里巴巴

| 贡献者 | 首次贡献 | PRs | 主要贡献 |
|--------|----------|-----|----------|
| [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | 2024-05 | 27 | 字符串拼接优化 (JDK-8336856) |
| Denghui Dong | 2024 | 15 | GC 优化 |

### 字节跳动

| 贡献者 | 首次贡献 | Commits | 主要贡献 |
|--------|----------|---------|----------|
| Anjian-Wen | 2024 | 12 | RISC-V 移植 |

### 龙芯

| 贡献者 | 首次贡献 | Commits | 主要贡献 |
|--------|----------|---------|----------|
| sunguoyun | 2024 | 14 | LoongArch 移植 |
| Ao Qi | 2024 | 11 | LoongArch 移植 |

---

## 4. 新星成长路径

### 从首次贡献到核心贡献者

```
典型成长路径:

第1阶段: 首次贡献 (1-3 个月)
├── 选择合适的 issue (good first issue)
├── 熟悉代码规范和提交流程
└── 获得第一个 commit

第2阶段: 持续贡献 (3-12 个月)
├── 深入特定领域
├── 参与代码审查
└── 建立信任关系

第3阶段: 核心贡献者 (1-2 年)
├── 独立负责功能开发
├── 成为 Reviewer
└── 指导新贡献者
```

### Shaojin Wen 的成长案例

| 时间 | 里程碑 | PR |
|------|--------|-----|
| 2024-05 | 首次贡献 | 小型优化 |
| 2024-07 | 第一个重要 PR | JDK-8336856 (字符串拼接) |
| 2024-08 | PR 集成 | +40% 启动性能 |
| 2025-06 | 后续优化 | JDK-8355177 (StringBuilder) |
| 2025-12 | 持续贡献 | 累计 27+ PRs |

---

## 5. 新贡献者指南

### 如何开始

1. **选择领域**
   - [good first issue](https://bugs.openjdk.org/) 标签
   - 自己感兴趣的模块
   - 日常工作中遇到的问题

2. **准备工作**
   - 订阅 [mailing lists](https://mail.openjdk.org/)
   - 阅读贡献指南
   - 设置开发环境

3. **首次贡献**
   - 从小改动开始 (文档、测试)
   - 遵循代码规范
   - 写好 commit message

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| 不熟悉代码库 | 先阅读相关模块的测试用例 |
| 害怕被拒绝 | Review 意见是学习机会 |
| 不确定方向 | 在邮件列表提问 |
| 时间不够 | 小步前进，持续贡献 |

---

## 6. 企业新星计划

### Oracle 新星

- **Entry Level**: 1-2 年培养
- **领域专注**: GC, 编译器, 核心库
- **Mentor 制度**: 资深工程师指导

### Red Hat 新星

- **开源文化**: 社区优先
- **远程工作**: 全球分布
- **快速反馈**: 社区驱动

### 中国企业新星

- **阿里**: 性能优化方向
- **腾讯**: GC 优化方向
- **华为**: JIT/AOT 方向

---

## 7. 新星影响力

### 2024-2025 年度影响

| 贡献者 | 影响力 | 说明 |
|--------|--------|------|
| [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | ⭐⭐⭐⭐⭐ | JDK 24 启动性能 +40% |
| [Chen Liang](/by-contributor/profiles/chen-liang.md) | ⭐⭐⭐⭐ | ClassFile API 改进 |
| [Emanuel Peter](/by-contributor/profiles/emanuel-peter.md) | ⭐⭐⭐⭐ | C2 编译器优化 |

### 技术博客和分享

| 贡献者 | 分享内容 |
|--------|----------|
| [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | 字符串优化系列文章 |
| [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | GC 性能分析 |

---

## 8. 数据说明

- **统计时间**: 2023-2026
- **入选标准**: 首次贡献在 2023 年后，且有持续贡献
- **影响力**: 基于 commits 数量和功能重要性

---

## 9. 相关页面

- [Top 50 贡献者](top50.md)
- [按组织分类](by-org.md)
- [按领域分类](by-domain.md)
- [地区分布](by-region.md)
- [Shaojin Wen 贡献者页面](/by-contributor/profiles/shaojin-wen.md)
