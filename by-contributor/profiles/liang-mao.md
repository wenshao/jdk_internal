# Liang Mao (毛亮)

> GC 正确性修复, Compact Object Headers, Jade GC 研究

---
## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Liang Mao (毛亮) |
| **当前组织** | [阿里巴巴 (Alibaba)](/contributors/orgs/alibaba.md) |
| **GitHub** | [@mmyxym](https://github.com/mmyxym) (Arctic Code Vault Contributor) |
| **OpenJDK** | Author |
| **PRs** | [2 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Ammyxym+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | GC (G1, Parallel, Compact Object Headers) |
| **活跃时间** | 2024 |
| **论文** | [Jade: A High-throughput Concurrent Copying GC](https://dl.acm.org/doi/10.1145/3627703.3650087) (EuroSys 2024, 第 2 作者, 与 SJTU IPADS 合作) |
| **技术博客** | [Compact Object Headers in Dragonwell JDK](https://www.alibabacloud.com/blog/compact-object-headers-in-dragonwell-jdk-reducing-costs-and-increasing-efficiency-for-java-applications_601065) (Alibaba Cloud, 2024) |
| **归属确认** | [Dragonwell 38 PRs](https://github.com/dragonwell-project/dragonwell11/pulls?q=author:mmyxym) + D-D-H sponsor + Jade 论文 Alibaba 署名 |

> **数据调查时间**: 2026-03-23

---

## 全部 PR

| PR | Bug ID | 标题 | 类型 |
|----|--------|------|------|
| [#19982](https://github.com/openjdk/jdk/pull/19982) | 8335493 | check_gc_overhead_limit should reset SoftRefPolicy | GC 修复 |
| [#20907](https://github.com/openjdk/jdk/pull/20907) | 8339725 | Concurrent GC crashed due to GetMethodDeclaringClass | GC 崩溃修复 |

---

## 其他贡献

- **Dragonwell**: [38 PRs](https://github.com/dragonwell-project/dragonwell11/pulls?q=author:mmyxym), 主要工作在 GC 和 HotSpot Runtime
- **Compact Object Headers**: 在 Dragonwell JDK 中实现 `UseCompactObjectHeaders`, SPECjbb2015 上内存降低 5-10%
- **Jade GC 研究**: EuroSys 2024 论文第 2 作者, 与上海交通大学 IPADS 实验室合作

---

> **文档等级**: L2
> **创建时间**: 2026-03-23
