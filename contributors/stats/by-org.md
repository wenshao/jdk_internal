# 按组织分类

> OpenJDK 贡献者按所属组织统计

---

## 组织贡献总览

| 排名 | 组织 | Commits | 占比 | 贡献者数 | 主要领域 |
|------|------|---------|------|----------|----------|
| 1 | **Oracle** | 60,000+ | 70%+ | 800+ | 全领域 |
| 2 | **Red Hat** | 4,500+ | 5% | 50+ | GC, 编译器 |
| 3 | **SAP** | 2,500+ | 3% | 30+ | HotSpot, 构建系统 |
| 4 | **IBM** | 1,800+ | 2% | 25+ | JVM, AOT |
| 5 | **Amazon** | 1,200+ | 1.5% | 20+ | GC, 性能 |
| 6 | **Google** | 900+ | 1% | 15+ | 核心库 |
| 7 | **Alibaba** | 150+ | <1% | 10+ | 核心库, 性能 |
| 8 | **腾讯** | 80+ | <1% | 5+ | GC |
| 9 | **华为** | 60+ | <1% | 8+ | JIT, AOT |
| 10 | **字节跳动** | 40+ | <1% | 5+ | RISC-V |

---

## Oracle

**最大贡献者，主导 OpenJDK 开发**

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| David Katleman | 1,487 | 构建/发布 |
| Jonathan Gibbons | 1,320 | javac/工具 |
| [Phil Race](/by-contributor/profiles/phil-race.md) | 1,313 | 图形/打印 |
| [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | 1,209 | HotSpot VM |
| Joe Darcy | 1,194 | 核心库 |
| [Thomas Schatzl](/by-contributor/profiles/thomas-schatzl.md) | 1,113 | G1 GC |
| Sergey Bylokhov | 953 | AWT/2D |
| Vladimir Kozlov | 942 | C2 编译器 |
| [Magnus Ihse Bursie](/by-contributor/profiles/magnus-ihse-bursie.md) | 925 | 构建系统 |
| Erik Joelsson | 956 | 构建系统 |
| Alan Bateman | 867 | 核心库/模块 |
| [David Holmes](/by-contributor/profiles/david-holmes.md) | 720 | 线程/并发 |
| Stefan Karlsson | 692 | ZGC |
| Claes Redestad | 688 | 核心库/性能 |
| Mandy Chung | 687 | 模块系统 |
| Weijun Wang | 954 | 安全/工具 |
| Naoto Sato | 569 | 国际化 |

**主要贡献领域**：
- GC: G1, ZGC, Serial, Parallel
- 编译器: C1, C2, Graal
- 核心库: java.lang, java.util, java.io
- 桌面: AWT, Swing, JavaFX
- 工具: javac, jlink, jpackage
- 安全: TLS, 加密, 认证

---

## Red Hat

**GC 和编译器专家**

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | 1,320 | Shenandoah GC |
| Roland Westrelin | 676 | C2 编译器 |
| [William Kemper](/by-contributor/profiles/william-kemper.md) | 34 | Shenandoah GC |
| Andrew Dinn | 200+ | JFR |
| Andrew Hughes | 150+ | 安全 |

**主要贡献领域**：
- Shenandoah GC (主要开发者)
- C2 编译器优化
- JFR 改进
- 安全补丁

---

## SAP

**企业级 JVM 优化**

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| [Matthias Baesken](/by-contributor/profiles/matthias-baesken.md) | 742 | 构建系统 |
| Thomas Stuefe | 548 | HotSpot |
| Goetz Lindenmaier | 300+ | HotSpot |

**主要贡献领域**：
- HotSpot VM 移植
- 构建系统 (AIX, Windows)
- 企业级特性

---

## IBM

**J9/OpenJ9 贡献**

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| Mark Stoodley | 200+ | AOT |
| Babneet Singh | 100+ | 测试 |
| Jielong Zhou | 80+ | GC |

**主要贡献领域**：
- AOT 编译
- GC 优化
- s390x 架构移植

---

## Amazon

**性能和 GC 优化**

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| [Aleksey Shipilev](/by-contributor/profiles/aleksey-shipilev.md) | - | Corretto |
| [William Kemper](/by-contributor/profiles/william-kemper.md) | 34 | Shenandoah |
| Felix Nensemba | 25 | GC |
| Y. S. K. Nilsen | 20 | 性能 |

**主要贡献领域**：
- Shenandoah GC (Corretto)
- 启动性能优化
- 云原生优化

---

## Google

**核心库贡献**

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| Michael Miller-Cushon | 100+ | 核心库 |
| Paul Sandoz | 80+ | 核心库 |

**主要贡献领域**：
- java.util.concurrent
- 性能优化
- API 改进

---

## 中国企业

### 阿里巴巴

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md) | 27 | 核心库/性能 |
| Denghui Dong | 15 | GC |

**主要贡献**：
- 字符串拼接优化 (JDK-8336856)
- StringBuilder 优化 (JDK-8355177)
- 启动性能改进

### 腾讯

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| Jie Fu | 20+ | GC |

### 华为

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| Feilong Jiang | 30+ | JIT/AOT |

### 字节跳动

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| Anjian-Wen | 12 | RISC-V |

---

## 学术机构

### ISCAS (中科院软件所)

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| Dingli Zhang | 11 | RISC-V |
| Fei Yang | 6 | RISC-V |

### 龙芯

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| sunguoyun | 14 | LoongArch |
| Ao Qi | 11 | LoongArch |

---

## 组织演进历史

| 时期 | 主要组织 | 事件 |
|------|----------|------|
| 2007-2010 | Sun, Oracle | OpenJDK 开源 |
| 2011-2014 | Oracle, Red Hat | JDK 7/8 发布 |
| 2015-2018 | Oracle, Red Hat, SAP | JDK 9-11 |
| 2019-2021 | +IBM, Amazon | JDK 12-17 |
| 2022-2024 | +中国企业 | JDK 18-23 |
| 2025-2026 | 全球化加速 | JDK 24-26 |

---

## 数据说明

- **统计依据**: Git commits (非 PRs)
- **邮箱域名**: 按提交邮箱域名归属组织
- **多组织**: 部分贡献者可能跨组织
- **数据时间**: 2007-2026

---

## 相关页面

- [Top 50 贡献者](top50.md)
- [按领域分类](by-domain.md)
- [年度趋势](by-year.md)
- [地区分布](by-region.md)
