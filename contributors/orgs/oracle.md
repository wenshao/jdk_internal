# Oracle

> OpenJDK 主要贡献者

---
## 目录

1. [概览](#1-概览)
2. [Top 贡献者](#2-top-贡献者)
3. [Oracle 中国团队](#3-oracle-中国团队)
4. [影响的模块](#4-影响的模块)
5. [主要领域](#5-主要领域)
6. [相关 PR 分析文档](#6-相关-pr-分析文档)
7. [数据来源](#7-数据来源)
8. [相关链接](#8-相关链接)

---


## 1. 概览

Oracle 是 OpenJDK 的主要维护者和最大贡献者，自 2010 年收购 Sun Microsystems 以来，一直主导 JDK 的开发。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 4,000+ |
| **贡献者数** | 500+ |
| **主要领域** | 全领域 |

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。OpenJDK Committer 使用 `@openjdk.org` 邮箱提交代码，因此 git commits 按邮箱统计不准确。

---

## 2. Top 贡献者

| 排名 | 贡献者 | GitHub | PRs | 角色 | 领域 | 档案 |
|------|--------|--------|-----|------|------|------|
| 1 | Thomas Schatzl | [@tschatzl](https://github.com/tschatzl) | 546 | Reviewer | G1 GC | [详情](../../by-contributor/profiles/thomas-schatzl.md) |
| 2 | Ioi Lam | [@iklam](https://github.com/iklam) | 431 | Reviewer | CDS/AOT | [详情](../../by-contributor/profiles/ioi-lam.md) |
| 3 | Coleen Phillimore | [@coleenp](https://github.com/coleenp) | 400 | Reviewer | HotSpot | [详情](../../by-contributor/profiles/coleen-phillimore.md) |
| 4 | Naoto Sato | [@naotoj](https://github.com/naotoj) | 273 | Reviewer | 国际化 | [详情](../../by-contributor/profiles/naoto-sato.md) |
| 5 | Sergey Bylokhov | [@mrserb](https://github.com/mrserb) | 273 | Reviewer | AWT/2D | - |
| 6 | Chen Liang | [@liach](https://github.com/liach) | 237 | Committer | ClassFile API | [详情](../../by-contributor/profiles/chen-liang.md) |
| 7 | Alexey Semenyuk | [@alexeysemenyukoracle](https://github.com/alexeysemenyukoracle) | 233 | Committer | AOT | [详情](../../by-contributor/profiles/alexey-semenyuk.md) |
| 8 | Jan Lahoda | [@lahodaj](https://github.com/lahodaj) | 324 | Reviewer | javac | [详情](../../by-contributor/profiles/jan-lahoda.md) |
| 9 | Jaikiran Pai | [@jaikiran](https://github.com/jaikiran) | 322 | Reviewer | 构建 | [详情](../../by-contributor/profiles/jaikiran-pai.md) |
| 10 | Daniel Fuchs | [@dfuch](https://github.com/dfuch) | 192 | Committer | JMX | [详情](../../by-contributor/profiles/daniel-fuchs.md) |
| 11 | Kim Barrett | - | 100+ | Reviewer | GC, C++ | [详情](../../by-contributor/profiles/kim-barrett.md) |
| 12 | David Holmes | - | 80+ | Reviewer | 并发 | [详情](../../by-contributor/profiles/david-holmes.md) |
| 13 | Erik Gahlin | - | 70+ | Reviewer | JFR | [详情](../../by-contributor/profiles/erik-gahlin.md) |
| 14 | Brian Burkhalter | - | 60+ | Committer | 网络 | [详情](../../by-contributor/profiles/brian-burkhalter.md) |
| 15 | Emanuel Peter | - | 50+ | Reviewer | C2 编译器 | [详情](../../by-contributor/profiles/emanuel-peter.md) |

**小计**: 4,000+ PRs (以上 15 人)

> **角色说明**:
> - **Reviewer**: 有权批准变更集的资深贡献者 ([详情](https://openjdk.org/bylaws))
> - **Committer**: 有直接推送权限的贡献者 ([详情](https://openjdk.org/guide/))
> - **Author**: 可以创建和提交更改的贡献者 ([详情](https://dev.java/contribute/openjdk/))

---

## 3. Oracle 中国团队

| 贡献者 | GitHub | PRs | 角色 | 主要领域 | 档案 |
|--------|--------|-----|------|----------|------|
| Naoto Sato | [@naotoj](https://github.com/naotoj) | 273 | Reviewer | 国际化 | [详情](../../by-contributor/profiles/naoto-sato.md) |
| Chen Liang | [@liach](https://github.com/liach) | 237 | Committer | ClassFile API | [详情](../../by-contributor/profiles/chen-liang.md) |

**小计**: 510 PRs

---

## 4. 影响的模块

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

## 5. 主要领域

### GC (垃圾收集)

| 领域 | 贡献者 | 档案 |
|------|--------|------|
| G1 GC | Thomas Schatzl | [详情](../../by-contributor/profiles/thomas-schatzl.md) |
| G1 GC | Albert Mingkun Yang | [详情](../../by-contributor/profiles/albert-mingkun-yang.md) |
| Shenandoah GC | Aleksey Shipilev | [详情](../../by-contributor/profiles/aleksey-shipilev.md) |
| 并发 GC | Kim Barrett | [详情](../../by-contributor/profiles/kim-barrett.md) |

### 编译器

| 领域 | 贡献者 | 档案 |
|------|--------|------|
| C2 编译器 | Emanuel Peter | [详情](../../by-contributor/profiles/emanuel-peter.md) |

### 核心库与性能

| 领域 | 贡献者 | 档案 |
|------|--------|------|
| 启动性能 | Claes Redestad | [详情](../../by-contributor/profiles/claes-redestad.md) |

### 语言特性

| 领域 | 贡献者 | 档案 |
|------|--------|------|
| javac | Jan Lahoda | [详情](../../by-contributor/profiles/jan-lahoda.md) |

### 构建系统

| 领域 | 贡献者 | 档案 |
|------|--------|------|
| 构建系统 | Magnus Ihse Bursie | [详情](../../by-contributor/profiles/magnus-ihse-bursie.md) |

### 桌面/客户端

| 领域 | 贡献者 | 档案 |
|------|--------|------|
| Client Libraries | Phil Race | [详情](../../by-contributor/profiles/phil-race.md) |
| Swing/AWT | Prasanta Sadhukhan | [详情](../../by-contributor/profiles/prasanta-sadhukhan.md) |
| 图形/打印 | Brian Burkhalter | [详情](../../by-contributor/profiles/brian-burkhalter.md) |

### 并发与运行时

| 领域 | 贡献者 | 档案 |
|------|--------|------|
| 并发 | David Holmes | [详情](../../by-contributor/profiles/david-holmes.md) |

### 工具与监控

| 领域 | 贡献者 | 档案 |
|------|--------|------|
| JFR | Erik Gahlin | [详情](../../by-contributor/profiles/erik-gahlin.md) |
| JVMTI | Leonid Mesnik | [详情](../../by-contributor/profiles/leonid-mesnik.md) |

### 国际化

| 领域 | 贡献者 | 档案 |
|------|--------|------|
| i18n | Naoto Sato | [详情](../../by-contributor/profiles/naoto-sato.md) |
| 本地化 | Justin Lu | [详情](../../by-contributor/profiles/justin-lu.md) |

---

## 6. 相关 PR 分析文档

### ClassFile API (Chen Liang)

| PR | 标题 | 分析文档 |
|----|------|----------|
| JDK-8342336 | Remove unused imports | [详情](../../by-pr/8342/8342336.md) |
| JDK-8341199 | Add ConstantDynamicBuilder.loadConstant | [详情](../../by-pr/8341/8341199.md) |
| JDK-8339217 | Add ClassBuilder.loadConstant | [详情](../../by-pr/8339/8339217.md) |
| JDK-8339320 | Utf8EntryImpl#inflate | [详情](../../by-pr/8339/8339320.md) |
| JDK-8339290 | Utf8EntryImpl#writeTo | [详情](../../by-pr/8339/8339290.md) |
| JDK-8339317 | BytecodeBuilder#writeBuffer | [详情](../../by-pr/8339/8339317.md) |
| JDK-8339168 | ClassImpl#slotSize | [详情](../../by-pr/8339/8339168.md) |
| JDK-8339205 | StackMapGenerator writeU1/U2/Int/Long | [详情](../../by-pr/8339/8339205.md) |
| JDK-8339196 | Add writeU1/U2/Int/Long to BufferBuilder | [详情](../../by-pr/8339/8339196.md) |
| JDK-8338937 | ClassDesc concat optimization | [详情](../../by-pr/8338/8338937.md) |
| JDK-8338532 | MethodTypeDesc implementation optimization | [详情](../../by-pr/8338/8338532.md) |
| JDK-8338409 | Record helpers | [详情](../../by-pr/8338/8338409.md) |
| JDK-8338936 | StringConcatFactory MethodType optimization | [详情](../../by-pr/8338/8338936.md) |
| JDK-8371953 | Reflection API performance | [详情](../../by-pr/8371/8371953.md) |
| JDK-8371701 | Field lookup optimization | [详情](../../by-pr/8371/8371701.md) |

### GC 相关

| PR | 标题 | 分析文档 |
|----|------|----------|
| JDK-8343984 | Unsafe out-of-bounds check | [详情](../../by-pr/8343/8343984.md) |
| JDK-8343925 | SharedGC support | [详情](../../by-pr/8343/8343925.md) |

### 性能优化

| PR | 标题 | 分析文档 |
|----|------|----------|
| JDK-8310929 | Integer.toString 优化 | [详情](../../by-pr/8310/8310929.md) |
| JDK-8310502 | Long.fastUUID 优化 | [详情](../../by-pr/8310/8310502.md) |
| JDK-8315968 | Array optimization | [详情](../../by-pr/8315/8315968.md) |
| JDK-8315970 | Bug fix | [详情](../../by-pr/8315/8315970.md) |
| JDK-8317742 | Type check optimization | [详情](../../by-pr/8317/8317742.md) |
| JDK-8311207 | Code cleanup | [详情](../../by-pr/8311/8311207.md) |

[→ 返回组织索引](../../by-contributor/index.md)

---

## 7. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-19

---

## 8. 相关链接

- [Oracle Java](https://www.oracle.com/java/)
- [Oracle OpenJDK](https://openjdk.org/groups/hotspot/)
- [Oracle GitHub](https://github.com/oracle)