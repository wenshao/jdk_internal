# Red Hat

> Shenandoah GC 和 Zero VM 的主要贡献者

---

## 概览

Red Hat 是 OpenJDK 的重要贡献者，尤其在 Shenandoah GC、Zero VM 和 AArch64 移植方面有深厚积累。

| 指标 | 值 |
|------|-----|
| **总 Commits** | 400+ |
| **贡献者数** | 50+ |
| **占比** | ~5% |
| **主要领域** | GC, 编译器, 架构移植 |

---

## 影响的模块分布

基于 git 修改文件统计：

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

## Commit 类型分析

| 类型 | 数量 | 说明 |
|------|------|------|
| Fix | 35 | 修复问题 |
| Add | 8 | 新增功能 |
| Shenandoah | 6 | Shenandoah 相关 |
| Remove | 4 | 删除代码 |
| Implement | 3 | 实现功能 |
| AArch64 | 1 | AArch64 相关 |

---

## Top 贡献者

| 排名 | 贡献者 | Commits | 领域 |
|------|--------|---------|------|
| 1 | Gary Benson | 35 | Zero VM, 构建 |
| 2 | Andrew Haley | 22 | AArch64 |
| 3 | Ashutosh Mehra | 19 | AArch64 |
| 4 | Robert Toyonaga | 14 | - |
| 5 | David M. Lloyd | 14 | - |
| 6 | Zdenek Zambersky | 9 | - |
| 7 | Severin Gehwolf | 8 | - |
| 8 | Florian Weimer | 8 | - |
| 9 | Michal Vala | 8 | - |
| 10 | Roman Kennke | 6 | Shenandoah |

> 注：Aleksey Shipilev (1,320 commits) 使用 @openjdk.org 邮箱，统计在 Oracle 中

---

## 主要领域

### Shenandoah GC

Red Hat 主导 Shenandoah GC 的开发：

- **Aleksey Shipilev**: Shenandoah GC 创始人，JEP 189
- **Roman Kennke**: Shenandoah 核心开发者
- **William Kemper**: Shenandoah 维护者 (现 Amazon)

**关键贡献**:
- 低延迟垃圾收集器
- 并发整理算法
- 区域化内存管理

### Zero VM

- **Gary Benson**: Zero VM 维护者
- 零汇编解释器，支持无 JIT 的平台
- 基于 C++ 实现

### Shark VM

- 基于 LLVM 的 JIT 编译器
- 用于不支持 HotSpot JIT 的平台

### AArch64

- **Andrew Haley**: AArch64 移植负责人
- **Ashutosh Mehra**: AArch64 优化

---

## JEP 贡献

| JEP | 标题 | 主导者 | 状态 |
|-----|------|--------|------|
| JEP 189 | Shenandoah GC (Incubator) | Aleksey Shipilev | JDK 12 |
| JEP 379 | Shenandoah GC (Standard) | Aleksey Shipilev | JDK 15 |
| JEP 418 | Internet-Address Resolution SPI | Andrew Dinn | JDK 18 |

---

## 技术特点

### 低延迟 GC

Shenandoah GC 是 Red Hat 的核心贡献：
- 目标暂停时间 < 10ms
- 并发整理，不依赖 STW
- 适用于大堆内存场景

### 多架构支持

- Zero VM: 支持任何 POSIX 平台
- AArch64: 64 位 ARM 架构优化

---

## 数据来源

- **统计方法**: `git log upstream_master --author="redhat"`
- **模块分析**: 基于修改文件路径统计
- **关键词分析**: 基于 commit message 提取

---

## 相关链接

- [Red Hat OpenJDK](https://developers.redhat.com/products/openjdk)
- [Shenandoah GC](https://openjdk.org/projects/shenandoah/)
- [Red Hat GitHub](https://github.com/redhat-openjdk)