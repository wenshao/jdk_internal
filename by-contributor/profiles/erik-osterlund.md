# Erik Österlund
> **ZGC 核心开发者, AOT 对象缓存, 《The Z Garbage Collector: In JDK 25》作者**

---
## 目录

1. [基本信息](#1-基本信息)
2. [职业背景](#2-职业背景)
3. [技术影响力](#3-技术影响力)
4. [代表性工作](#4-代表性工作)
5. [PR 列表](#5-pr-列表)
6. [相关链接](#6-相关链接)
---


## 1. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Erik Österlund |
| **当前组织** | [Oracle](../../contributors/orgs/oracle.md) |
| **职位** | Consulting Member of Technical Staff, Java Platform Group |
| **位置** | Sweden |
| **GitHub** | [@fisk](https://github.com/fisk) |
| **OpenJDK** | [@eosterlund](https://openjdk.org/census#eosterlund) |
| **Mastodon** | [@eosterlund_fisk](https://mastodon.social/@eosterlund_fisk) |
| **角色** | JDK Reviewer |
| **教育背景** | BSc, MSc, PhD - Linnaeus University, Sweden (PhD 2019, 垃圾收集方向) |
| **PRs** | 96+ (累计) |
| **JDK 26 Commits** | 12 |
| **主要领域** | ZGC, AOT, 并发, 内存管理 |
| **主导 JEP** | JEP 516: AOT Object Caching |
| **著作** | 《The Z Garbage Collector: In JDK 25》(CRC Press) |
| **活跃时间** | 2016 - 至今 |

> **数据来源**: [OpenJDK Census](https://openjdk.org/census#eosterlund), [Linnaeus University PhD Defence](https://lnu.se/en/meet-linnaeus-university/current/events/2019/public-defence-erik-osterlund-191018/), [Amazon Author Page](https://www.amazon.com/Garbage-Collector-JDK-25/dp/1032976926)

---

## 2. 职业背景

Erik Österlund 在 Linnaeus University 完成了 BSc、MSc 和 PhD 学位，研究方向均为垃圾收集。2012 年在北京的内存管理会议上结识了 Oracle 的 Jesper Wilhelmsson，随后获得研究实习机会。2016 年正式加入 Oracle，开始参与 ZGC 开发，成为 **ZGC (Z Garbage Collector)** 的核心开发者之一，与 Per Lidén 和 Stefan Karlsson 一起设计了 ZGC。2019 年完成博士答辩（论文: "Going beyond on-the-fly garbage collection and improving self-adaption with enhanced interfaces"）。后来专注于 AOT 和内存管理优化。2024 年出版专著《The Z Garbage Collector: In JDK 25》。

### 职业时间线
| 时间 | 事件 | 详情 |
|------|------|------|
| **2012** | 内存管理会议 (北京) | 结识 Oracle 的 Jesper Wilhelmsson |
| **2016** | 加入 Oracle | HotSpot GC 团队，开始参与 ZGC 开发 |
| **2018** | ZGC 引入 | JEP 333 实验性特性 (与 Per Lidén, Stefan Karlsson 合作) |
| **2019** | PhD 答辩 | Linnaeus University, 垃圾收集方向 |
| **2020** | PLDI 2020 论文 | "Improving Program Locality in the GC using Hotness" |
| **2024** | 出版专著 | 《The Z Garbage Collector: In JDK 25》(CRC Press) |
| **2024** | JEP 516 Lead | AOT Object Caching 主导者 |
| **JDK 26** | 12 commits | AOT 相关贡献 |

---

## 3. 技术影响力
| 指标 | 值 |
|------|-----|
| **累计 PRs** | 96+ |
| **JDK 26 Commits** | 12 |
| **排名** | #40 (JDK 26) |
| **主要贡献** | ZGC, AOT, 内存管理 |

### 影响的主要领域
| 领域 | 贡献数 | 说明 |
|------|--------|------|
| ZGC | 56+ | 核心开发者 |
| Aot | 40+ | 对象缓存 |

| 并发 | 20+ | 并发原语 |

---

## 4. 代表性工作
### 1. ZGC 标记屏障
ZGC 的并发屏障实现，显著降低 GC 嚪停时间。

### 2. AOT 对象缓存 (JEP 516)
**Issue**: [JDK-8365932](https://bugs.openjdk.org/browse/JDK-8365932)

实现 AOT 对象缓存
```
变更: +5,269/-1,645
影响: GC 嚴停时间优化
```

### 3. ZGC 性能优化
ZGC 性能持续提升，- 吞吐量改进
- 嚾停时间减少
- 勉停时间缩短

---

## 5. PR 列表
### JDK 26 Top PRs
| Issue | 标题 | 变更行数 | 描述 |
|-------|------|----------|------|
| 8365932 | AOT Object Caching | 6,914 | JEP 516 实现 |
### ZGC 相关
| Issue | 标题 | 描述 |
|-------|------|------|
| ZGC 栨 Barrier | 并发屏障 |
| ZGC 摘卡/Load | 勿删卡/Load 优化 |
| ZGC 标记 | 核心算法 |
| ZGC 性能 | 吞吐量提升 |

---
## 6. 相关链接
| 类型 | 链接 |
|------|------|
| **OpenJDK Census** | [eosterlund](https://openjdk.org/census#eosterlund) |
| **Inside.java** | [Erik Österlund](https://inside.java/u/ErikOsterlund/) |
| **Mastodon** | [@eosterlund_fisk](https://mastodon.social/@eosterlund_fisk) |
| **ZGC 文档** | [ZGC](https://wiki.openjdk.org/zgc) |
| **著作** | [The Z Garbage Collector: In JDK 25](https://www.amazon.com/Garbage-Collector-JDK-25/dp/1032976926) |
| **PLDI 2020 论文** | [Improving Program Locality in the GC using Hotness](https://pldi20.sigplan.org/details/pldi-2020-papers/17/Improving-Program-Locality-in-the-GC-using-Hotness) |
| **协作者** | Per Lidén, Stefan Karlsson, Ioi Lam |

---
> **文档版本**: 2.0
> **最后更新**: 2026-03-22
> **更新内容**: 添加教育背景 (Linnaeus University PhD 2019)、职位 (CMTS)、著作 (ZGC 书籍)、PLDI 2020 论文、Mastodon 链接、Inside.java 链接、完善职业时间线


## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 383 |
| **活跃仓库数** | 8 |
