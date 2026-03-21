# 中国贡献者

> OpenJDK 历史上的中国开发者贡献 (JDK 8 - JDK 26)

---
## 目录

1. [概览](#1-概览)
2. [Oracle 中国团队](#2-oracle-中国团队)
3. [中国企业](#3-中国企业)
4. [按领域统计](#4-按领域统计)
5. [统计汇总](#5-统计汇总)
6. [其他知名华人 JVM 专家](#6-其他知名华人-jvm-专家)
7. [相关链接](#7-相关链接)

---


## 1. 概览

中国开发者在 OpenJDK 社区中做出了重要贡献，涵盖 GC、编译器、RISC-V、LoongArch、核心库、国际化等多个领域。

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。查询方式：`repo:openjdk/jdk author:xxx type:pr label:integrated`

---

## 2. Oracle 中国团队

> 统计在 [Oracle](../../contributors/orgs/oracle.md) 组织中

| 排名 | 贡献者 | GitHub | PRs | 主要领域 |
|------|--------|--------|-----|----------|
| 1 | Albert Mingkun Yang | [@albertnetymk](https://github.com/albertnetymk) | 744 | GC |
| 2 | Naoto Sato | [@naotoj](https://github.com/naotoj) | 273 | 国际化 |
| 3 | [Chen Liang](chen-liang.md) | [@liach](https://github.com/liach) | 237 | ClassFile API |
| 4 | Sendao Yan | [@sendaoYan](https://github.com/sendaoYan) | 202 | 测试稳定性 |
| 5 | Yasumasa Suenaga | [@YaSuenag](https://github.com/YaSuenag) | 113 | HotSpot |
| 6 | [Hamlin Li](hamlin-li.md) | [@merykitty](https://github.com/merykitty) | 74 | RISC-V |

**小计**: 1,643 PRs

---

## 3. 中国企业

### 阿里巴巴

👉 [查看完整详情](../../contributors/orgs/alibaba.md)
👉 [Dragonwell 团队](../../contributors/orgs/dragonwell.md)

| 贡献者 | GitHub | PRs | 主要领域 |
|--------|--------|-----|----------|
| [Shaojin Wen](shaojin-wen.md) | [@wenshao](https://github.com/wenshao) | 97 | 核心库优化 |
| [Kuai Wei](kuai-wei.md) | [@kuaiwei](https://github.com/kuaiwei) | 13 | C2 编译器 |
| [Yude Lin](yude-lin.md) | [@linade](https://github.com/linade) | 8 | G1 GC, AArch64 |
| [Xiaowei Lu](xiaowei-lu.md) | [@weixlu](https://github.com/weixlu) | 3 | ZGC |

**小计**: 121 PRs

**关键贡献**:
- 字符串拼接优化 (+10%)
- DateTime toString 优化 (+10%)
- G1 GC 监控增强
- ZGC 性能优化

**Dragonwell 团队成员**:
- [Sanhong Li](../../by-contributor/profiles/sanhong.md) - ASE 2021 论文作者
- [Long Yang](../../by-contributor/profiles/yanglong1010.md) - JVM 团队，杭州
- [Sendaoyan Yan](../../by-contributor/profiles/sendaoyan.md) - 编译器测试工程师
- [Joshua Zhu](../../by-contributor/profiles/joshua-zhu.md) - 上海团队

---

### 字节跳动

👉 [查看完整详情](../../contributors/orgs/bytedance.md)

| 贡献者 | GitHub | PRs | 主要领域 |
|--------|--------|-----|----------|
| [Anjian Wen](anjian-wen.md) | [@Anjian-Wen](https://github.com/Anjian-Wen) | 25 | RISC-V 向量指令 |

**小计**: 25 PRs

**关键贡献**:
- RISC-V Zvbb 向量指令
- RISC-V Zfa 浮点指令
- 数组填充优化

---

### 龙芯

👉 [查看完整详情](../../contributors/orgs/loongson.md)

**关键贡献**:
- LoongArch Zero VM 支持
- 编译器正确性修复

---

### 腾讯

👉 [查看完整详情](../../contributors/orgs/tencent.md)

**关键贡献**:
- G1 压缩指针边界修复
- 容器资源检测修复

---

### ISCAS (中科院软件所)

| 贡献者 | GitHub | PRs | 主要领域 |
|--------|--------|-----|----------|
| Dingli Zhang | [@DingliZhang](https://github.com/DingliZhang) | 53 | RISC-V |

---

## 4. 按领域统计

### GC (垃圾收集)

| 贡献者 | PRs | 组织 | 领域 |
|--------|-----|------|------|
| Albert Mingkun Yang | 744 | Oracle | G1/Parallel GC |
| Yude Lin | 8 | 阿里巴巴 | G1 GC |
| Xiaowei Lu | 3 | 阿里巴巴 | ZGC |

### 编译器

| 贡献者 | PRs | 组织 | 领域 |
|--------|-----|------|------|
| Kuai Wei | 13 | 阿里巴巴 | C2 编译器 |
| Anjian Wen | 25 | 字节跳动 | RISC-V 后端 |

### RISC-V

| 贡献者 | PRs | 组织 |
|--------|-----|------|
| Hamlin Li | 74 | Oracle |
| Anjian Wen | 25 | 字节跳动 |
| Dingli Zhang | 53 | ISCAS |

### 核心库

| 贡献者 | PRs | 组织 |
|--------|-----|------|
| Shaojin Wen | 97 | 阿里巴巴 |
| Naoto Sato | 273 | Oracle |

---

## 5. 统计汇总

| 组织 | PRs | 详情 |
|------|-----|------|
| Oracle 中国团队 | 1,643 | [详情](../../contributors/orgs/oracle.md) |
| 阿里巴巴 | 121 | [详情](../../contributors/orgs/alibaba.md) |
| ISCAS | 53 | - |
| 字节跳动 | 25 | [详情](../../contributors/orgs/bytedance.md) |
| 龙芯 | 50+ | [详情](../../contributors/orgs/loongson.md) |
| 腾讯 | 40+ | [详情](../../contributors/orgs/tencent.md) |

---

## 6. 其他知名华人 JVM 专家

> 以下专家在 JVM 领域有重要影响力，但未在 `openjdk/jdk` 仓库有大量 Integrated PRs（可能通过其他渠道贡献或专注于商业 JVM）

| 专家 | 领域 | 现任组织 | 简介 |
|------|------|----------|------|
| **Kris Mok** (RednaxelaFX) | HotSpot、编译器、JVM 优化 | Databricks | JVM 深度专家，曾任职 Azul Systems (Zing JVM)，专注于编译器和运行时优化。GitHub: [@RednaxelaFX](https://github.com/RednaxelaFX)，博客: [rednaxelafx.iteye.com](http://rednaxelafx.iteye.com) |
| **Alex Blewitt** | JVM、Eclipse | Instagram | JVM 和 Eclipse 专家，著有 JVM 相关书籍。GitHub: [@AlBlue](https://github.com/AlBlue) |

### Kris Mok (RednaxelaFX)

Kris Mok 是华人 JVM 社区中最知名的技术专家之一：

- **当前**: Databricks，专注于 Apache Spark 性能优化
- **曾任**: Azul Systems，参与 Zing JVM 开发
- **专长**: HotSpot JVM 内部机制、JIT 编译器、GC 优化
- **开源项目**:
  - [hotspot_evil](https://github.com/RednaxelaFX/hotspot_evil) - HotSpot JVM 工具集
  - [ajvm](https://github.com/RednaxelaFX/ajvm) - 个人 JVM 实现
  - [jvm.go](https://github.com/RednaxelaFX/jvm.go) - Go 语言实现的 JVM
- **技术博客**: [rednaxelafx.iteye.com](http://rednaxelafx.iteye.com) - 大量 JVM 深度技术文章

> **说明**: 以上专家的贡献主要通过商业 JVM (如 Azul Zing) 或其他开源项目，而非直接通过 OpenJDK 官方仓库。按照项目规范，仅统计 `openjdk/jdk` 的 Integrated PRs。

---

## 7. 相关链接

- [OpenJDK 中国社区](https://openjdk.org/groups/china/)
- [阿里巴巴 Dragonwell](https://github.com/alibaba/dragonwell8)
- [龙芯 JDK](https://github.com/loongson/jdk)
- [腾讯 Kona](https://github.com/Tencent/TencentKona-8)
- [Azul Zing](https://www.azul.com/products/zing/) (商业 JVM)