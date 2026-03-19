# Oracle

> OpenJDK 主要贡献者，贡献超过 60,000 commits

---

## 概览

Oracle 是 OpenJDK 的主要维护者和最大贡献者，自 2010 年收购 Sun Microsystems 以来，一直主导 JDK 的开发。

| 指标 | 值 |
|------|-----|
| **总 Commits** | 60,000+ |
| **贡献者数** | 500+ |
| **占比** | 70%+ |
| **主要领域** | 全领域 |

---

## 影响的模块分布

基于 git 修改文件统计：

| 模块 | 文件数 | 说明 |
|------|--------|------|
| CLDR 数据 | 9,340 | 国际化数据更新 |
| HotSpot Runtime | 7,379 | JVM 运行时 |
| G1 GC | 6,862 | G1 垃圾收集器 |
| C2 编译器 | 6,532 | 服务端编译器 |
| Shenandoah GC | 3,982 | Shenandoah 垃圾收集器 |
| Class File | 3,781 | 类文件处理 |
| x86 移植 | 3,755 | x86 架构支持 |
| GC 共享 | 3,587 | GC 共享代码 |
| OOPs | 3,359 | 对象模型 |
| AArch64 移植 | 2,975 | AArch64 架构支持 |
| ZGC | 2,958 | Z 垃圾收集器 |
| JVM Primitives | 2,791 | JVM 原语 |

---

## Commit 类型分析

| 类型 | 数量 | 说明 |
|------|------|------|
| Merge | 14,585 | 合并提交 |
| Add | 7,008 | 新增功能 |
| Remove | 3,343 | 删除代码 |
| Fix | 2,525 | 修复问题 |
| Update | 1,335 | 更新代码 |
| Clean | 872 | 代码清理 |
| Refactor | 516 | 重构 |
| Implement | 378 | 实现功能 |
| Optimize | 240 | 性能优化 |

---

## Top 30 贡献者

| 排名 | 贡献者 | Commits | 领域 |
|------|--------|---------|------|
| 1 | David Katleman | 1,487 | 构建/发布 |
| 2 | Jonathan Gibbons | 1,320 | javac |
| 3 | Phil Race | 1,313 | 图形/打印 |
| 4 | Coleen Phillimore | 1,209 | HotSpot |
| 5 | Joe Darcy | 1,194 | 核心库 |
| 6 | Thomas Schatzl | 1,113 | G1 GC |
| 7 | Alejandro Murillo | 998 | HotSpot |
| 8 | Erik Joelsson | 956 | 构建系统 |
| 9 | Weijun Wang | 954 | 安全/工具 |
| 10 | Sergey Bylokhov | 953 | AWT/2D |
| 11 | Vladimir Kozlov | 942 | C2 编译器 |
| 12 | Magnus Ihse Bursie | 925 | 构建系统 |
| 13 | Jesper Wilhelmsson | 912 | GC |
| 14 | Daniel D. Daugherty | 867 | HotSpot |
| 15 | Alan Bateman | 867 | 核心库 |
| 16 | Chris Hegarty | 812 | 网络 |
| 17 | Jan Lahoda | 785 | javac |
| 18 | Brian Burkhalter | 779 | NIO |
| 19 | Prasanta Sadhukhan | 772 | Swing |
| 20 | Albert Mingkun Yang | 747 | GC |
| 21 | David Holmes | 720 | 线程 |
| 22 | Stefan Karlsson | 692 | ZGC |
| 23 | Sundararajan Athijegannathan | 689 | Nashorn |
| 24 | Claes Redestad | 688 | 核心库 |
| 25 | Mandy Chung | 687 | 模块系统 |
| 26 | Kim Barrett | 680 | GC |
| 27 | Igor Ignatyev | 673 | 测试 |
| 28 | Maurizio Cimadamore | 670 | 语言特性 |
| 29 | Ioi Lam | 661 | CDS/AOT |
| 30 | Zhengyu Gu | 582 | GC |

---

## 主要领域

### GC (垃圾收集)

- **G1 GC**: Thomas Schatzl, Albert Mingkun Yang, Zhengyu Gu
- **ZGC**: Stefan Karlsson
- **Shenandoah**: (部分贡献，主要来自 Red Hat)
- **并发 GC**: Kim Barrett

### 编译器

- **C2**: Vladimir Kozlov, Tobias Hartmann
- **Graal**: Tom Rodriguez, Vladimir Ivanov

### 核心库

- **java.lang/java.util**: Joe Darcy, Claes Redestad
- **模块系统**: Alan Bateman, Mandy Chung
- **反射**: Roger Riggs

### 语言特性

- **javac**: Jonathan Gibbons, Jan Lahoda, Maurizio Cimadamore
- **Lambda**: Brian Goetz

### 构建系统

- **构建**: David Katleman, Erik Joelsson, Magnus Ihse Bursie

### 桌面

- **图形/打印**: Phil Race
- **AWT/2D**: Sergey Bylokhov, Prasanta Sadhukhan

---

## Oracle 中国团队

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| Weijun Wang | 954 | 安全/工具 |
| Albert Mingkun Yang | 747 | GC |
| Sundararajan Athijegannathan | 689 | Nashorn |
| Zhengyu Gu | 582 | GC |
| Naoto Sato | 569 | 国际化 |
| Xue-Lei Andrew Fan | 412 | 安全 |
| Hamlin Li | 301 | RISC-V |
| Jiangli Zhou | 251 | CDS |

---

## 数据来源

- **统计方法**: `git log upstream_master --author="@openjdk.org"`
- **模块分析**: 基于修改文件路径统计
- **关键词分析**: 基于 commit message 提取

---

## 相关链接

- [Oracle Java](https://www.oracle.com/java/)
- [Oracle OpenJDK](https://openjdk.org/groups/hotspot/)
- [Oracle GitHub](https://github.com/oracle)