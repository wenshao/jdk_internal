# Red Hat

> Shenandoah GC 和 Zero VM 的主要贡献者

---

## 概览

Red Hat 是 OpenJDK 的重要贡献者，尤其在 Shenandoah GC、Zero VM 和 AArch64 移植方面有深厚积累。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 75+ |
| **贡献者数** | 50+ |
| **主要领域** | GC, 编译器, 架构移植 |

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。OpenJDK Committer 使用 `@openjdk.org` 邮箱提交代码，因此 git commits 按邮箱统计不准确。Aleksey Shipilev (803 PRs) 统计在 Oracle 中。

---

## Top 贡献者

| 排名 | 贡献者 | GitHub | PRs | 领域 |
|------|--------|--------|-----|------|
| 1 | Raffaello Giulietti | [@rgiulietti](https://github.com/rgiulietti) | 75 | 核心库 |

**小计**: 75 PRs

> 注：Aleksey Shipilev (Shenandoah GC 创始人) 使用 @openjdk.org 邮箱，统计在 Oracle 中

---

## 影响的模块

| 模块 | 文件数 | 说明 |
|------|--------|------|
| Zero VM | 157 | 零汇编解释器 VM |
| Shark VM | 83 | 基于 LLVM 的 JIT |
| SSL/TLS | 65 | 安全通信 |
| JVMCI | 40 | JVM 编译器接口 |
| HotSpot Runtime | 31 | JVM 运行时 |
| Shenandoah GC | 15 | Shenandoah 垃圾收集器 |
| NMT | 19 | 原生内存追踪 |

---

## 主要领域

### Shenandoah GC

Red Hat 主导 Shenandoah GC 的开发：

- **Aleksey Shipilev**: Shenandoah GC 创始人，JEP 189
- **Roman Kennke**: Shenandoah 核心开发者

**关键贡献**:
- 低延迟垃圾收集器
- 并发整理算法
- 区域化内存管理

### Zero VM

- 零汇编解释器，支持无 JIT 的平台
- 基于 C++ 实现

### AArch64

- AArch64 移植
- AArch64 优化

---

## JEP 贡献

| JEP | 标题 | 主导者 | 状态 |
|-----|------|--------|------|
| JEP 189 | Shenandoah GC (Incubator) | Aleksey Shipilev | JDK 12 |
| JEP 379 | Shenandoah GC (Standard) | Aleksey Shipilev | JDK 15 |
| JEP 418 | Internet-Address Resolution SPI | Andrew Dinn | JDK 18 |

---

## 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-19

---

## 相关链接

- [Red Hat OpenJDK](https://developers.redhat.com/products/openjdk)
- [Shenandoah GC](https://openjdk.org/projects/shenandoah/)
- [Red Hat GitHub](https://github.com/redhat-openjdk)