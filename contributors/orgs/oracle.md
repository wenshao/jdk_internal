# Oracle

> OpenJDK 主要贡献者

---

## 概览

Oracle 是 OpenJDK 的主要维护者和最大贡献者，自 2010 年收购 Sun Microsystems 以来，一直主导 JDK 的开发。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 4,000+ |
| **贡献者数** | 500+ |
| **主要领域** | 全领域 |

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。OpenJDK Committer 使用 `@openjdk.org` 邮箱提交代码，因此 git commits 按邮箱统计不准确。

---

## Top 贡献者

| 排名 | 贡献者 | GitHub | PRs | 领域 |
|------|--------|--------|-----|------|
| 1 | Aleksey Shipilev | [@shipilev](https://github.com/shipilev) | 803 | Shenandoah GC |
| 2 | Albert Mingkun Yang | [@albertnetymk](https://github.com/albertnetymk) | 744 | GC |
| 3 | Thomas Schatzl | [@tschatzl](https://github.com/tschatzl) | 546 | G1 GC |
| 4 | Ioi Lam | [@iklam](https://github.com/iklam) | 431 | CDS/AOT |
| 5 | Coleen Phillimore | [@coleenp](https://github.com/coleenp) | 400 | HotSpot |
| 6 | Naoto Sato | [@naotoj](https://github.com/naotoj) | 273 | 国际化 |
| 7 | Sergey Bylokhov | [@mrserb](https://github.com/mrserb) | 273 | AWT/2D |
| 8 | Chen Liang | [@liach](https://github.com/liach) | 237 | ClassFile API |
| 9 | Alexey Semenyuk | [@alexeysemenyukoracle](https://github.com/alexeysemenyukoracle) | 233 | AOT |
| 10 | Jan Lahoda | [@lahodaj](https://github.com/lahodaj) | 324 | javac |
| 11 | Jaikiran Pai | [@jaikiran](https://github.com/jaikiran) | 322 | 构建 |
| 12 | Sendao Yan | [@sendaoYan](https://github.com/sendaoYan) | 202 | 测试稳定性 |
| 13 | Daniel Fuchs | [@dfuch](https://github.com/dfuch) | 192 | JMX |
| 14 | Yasumasa Suenaga | [@YaSuenag](https://github.com/YaSuenag) | 113 | HotSpot |
| 15 | Hamlin Li | [@merykitty](https://github.com/merykitty) | 74 | RISC-V |

**小计**: 4,865 PRs (以上 15 人)

---

## Oracle 中国团队

| 贡献者 | GitHub | PRs | 主要领域 |
|--------|--------|-----|----------|
| Albert Mingkun Yang | [@albertnetymk](https://github.com/albertnetymk) | 744 | GC |
| Naoto Sato | [@naotoj](https://github.com/naotoj) | 273 | 国际化 |
| Chen Liang | [@liach](https://github.com/liach) | 237 | ClassFile API |
| Sendao Yan | [@sendaoYan](https://github.com/sendaoYan) | 202 | 测试稳定性 |
| Yasumasa Suenaga | [@YaSuenag](https://github.com/YaSuenag) | 113 | HotSpot |
| Hamlin Li | [@merykitty](https://github.com/merykitty) | 74 | RISC-V |

**小计**: 1,643 PRs

---

## 影响的模块

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

---

## 主要领域

### GC (垃圾收集)

- **G1 GC**: Thomas Schatzl, Albert Mingkun Yang, Zhengyu Gu
- **ZGC**: Stefan Karlsson
- **Shenandoah**: Aleksey Shipilev
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

## 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-19

---

## 相关链接

- [Oracle Java](https://www.oracle.com/java/)
- [Oracle OpenJDK](https://openjdk.org/groups/hotspot/)
- [Oracle GitHub](https://github.com/oracle)