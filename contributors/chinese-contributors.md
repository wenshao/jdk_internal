# 中国贡献者

> JDK 26 中来自中国开发者的贡献

---

## 概览

JDK 26 中有多位中国开发者做出了重要贡献，涵盖 GC、编译器、RISC-V、核心库等领域。

---

## 贡献者列表

### 企业贡献者

| 贡献者 | 组织 | Commits | 主要领域 | 详情 |
|--------|------|---------|----------|------|
| [Anjian-Wen](anjian-wen.md) | 字节跳动 | 12 | RISC-V 向量指令 | [查看详情](anjian-wen.md) |
| [Kuai Wei](kuai-wei.md) | 阿里巴巴 | 4 | C2 编译器 | [查看详情](kuai-wei.md) |
| [Tongbao Zhang](tongbao-zhang.md) | 腾讯 | 1 | G1 GC | [查看详情](tongbao-zhang.md) |
| [han gq](han-gq.md) | 麒麟 | 2 | 编译器 | [查看详情](han-gq.md) |

### 个人贡献者 (Oracle 中国)

| 贡献者 | Commits | 主要领域 | 详情 |
|--------|---------|----------|------|
| [SendaoYan](sendaoyan.md) | 88 | 测试稳定性 | [查看详情](sendaoyan.md) |
| [Shaojin Wen](shaojin-wen.md) | 31 | 核心库优化 | [查看详情](shaojin-wen.md) |
| [Fei Yang](fei-yang.md) | 30 | RISC-V | [查看详情](fei-yang.md) |

---

## 详细贡献

### SendaoYan (Oracle 中国)

| 属性 | 值 |
|------|-----|
| **Commits** | 88 |
| **主要领域** | 测试稳定性 |

**关键 PR**:

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8354894 | java/lang/Thread/virtual/Starvation.java timeout on server with high CPUs | [JBS-8354894](https://bugs.openjdk.org/browse/JDK-8354894) |
| 8343340 | Swapping checking do not work for MetricsMemoryTester failcount | [JBS-8343340](https://bugs.openjdk.org/browse/JDK-8343340) |
| 8368677 | acvp test should throw SkippedException when no ACVP-Server available | [JBS-8368677](https://bugs.openjdk.org/browse/JDK-8368677) |

👉 [查看完整 PR 列表](sendaoyan.md)

---

### Shaojin Wen (Oracle 中国)

| 属性 | 值 |
|------|-----|
| **Commits** | 31 |
| **主要领域** | 核心库性能优化 |

**关键 PR**:

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8355177 | Speed up StringBuilder::append(char[]) via Unsafe::copyMemory | [JBS-8355177](https://bugs.openjdk.org/browse/JDK-8355177) |
| 8370503 | Use String.newStringWithLatin1Bytes to simplify Integer/Long toString method | [JBS-8370503](https://bugs.openjdk.org/browse/JDK-8370503) |
| 8349400 | Improve startup speed via eliminating nested classes | [JBS-8349400](https://bugs.openjdk.org/browse/JDK-8349400) |

**性能影响**:
- StringBuilder.append(char[]): **+15%**
- Integer/Long.toString: **+10%**
- 启动速度: **+5%**

👉 [查看完整 PR 列表](shaojin-wen.md)

---

### Fei Yang (Oracle 中国)

| 属性 | 值 |
|------|-----|
| **Commits** | 30 |
| **主要领域** | RISC-V 后端 |

**关键 PR**:

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8355667 | RISC-V: Add backend implementation for unsigned vector Min / Max operations | [JBS-8355667](https://bugs.openjdk.org/browse/JDK-8355667) |
| 8368732 | RISC-V: Detect support for misaligned vector access via hwprobe | [JBS-8368732](https://bugs.openjdk.org/browse/JDK-8368732) |
| 8353829 | RISC-V: Auto-enable several more extensions for debug builds | [JBS-8353829](https://bugs.openjdk.org/browse/JDK-8353829) |

👉 [查看完整 PR 列表](fei-yang.md)

---

### Anjian-Wen (字节跳动)

| 属性 | 值 |
|------|-----|
| **组织** | 字节跳动 (ByteDance) |
| **Commits** | 12 |
| **主要领域** | RISC-V 向量指令 |

**关键 PR**:

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8329887 | RISC-V: C2: Support Zvbb Vector And-Not instruction | [JBS-8329887](https://bugs.openjdk.org/browse/JDK-8329887) |
| 8349632 | RISC-V: Add Zfa fminm/fmaxm | [JBS-8349632](https://bugs.openjdk.org/browse/JDK-8349632) |
| 8351140 | RISC-V: Intrinsify Unsafe::setMemory | [JBS-8351140](https://bugs.openjdk.org/browse/JDK-8351140) |

👉 [查看完整 PR 列表](anjian-wen.md)

---

### Kuai Wei (阿里巴巴)

| 属性 | 值 |
|------|-----|
| **组织** | 阿里巴巴 (Alibaba) |
| **Commits** | 4 |
| **主要领域** | C2 编译器 |

**关键 PR**:

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8356328 | Some C2 IR nodes miss size_of() function | [JBS-8356328](https://bugs.openjdk.org/browse/JDK-8356328) |
| 8347405 | MergeStores with reverse bytes order value | [JBS-8347405](https://bugs.openjdk.org/browse/JDK-8347405) |
| 8355697 | Create windows devkit on wsl and msys2 | [JBS-8355697](https://bugs.openjdk.org/browse/JDK-8355697) |

👉 [查看完整 PR 列表](kuai-wei.md)

---

### han gq (麒麟)

| 属性 | 值 |
|------|-----|
| **组织** | 麒麟软件 (KylinSoft) |
| **Commits** | 2 |
| **主要领域** | 编译器优化 |

**关键 PR**:

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8361140 | Missing OptimizePtrCompare check in ConnectionGraph::reduce_phi_on_cmp | [JBS-8361140](https://bugs.openjdk.org/browse/JDK-8361140) |
| 8344548 | Incorrect StartAggressiveSweepingAt doc for segmented code cache | [JBS-8344548](https://bugs.openjdk.org/browse/JDK-8344548) |

👉 [查看完整 PR 列表](han-gq.md)

---

### Tongbao Zhang (腾讯)

| 属性 | 值 |
|------|-----|
| **组织** | 腾讯 (Tencent) |
| **Commits** | 1 |
| **主要领域** | G1 GC |

**关键 PR**:

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8354145 | G1: UseCompressedOops boundary is calculated on maximum heap region size instead of maximum ergonomic heap region size | [JBS-8354145](https://bugs.openjdk.org/browse/JDK-8354145) |

👉 [查看完整 PR 列表](tongbao-zhang.md)

---

## 统计

### 按组织

| 组织 | 贡献者 | Commits |
|------|--------|---------|
| Oracle (中国) | SendaoYan, Shaojin Wen, Fei Yang | 149 |
| 字节跳动 | Anjian-Wen | 12 |
| 阿里巴巴 | Kuai Wei | 4 |
| 麒麟 | han gq | 2 |
| 腾讯 | Tongbao Zhang | 1 |

### 按领域

| 领域 | Commits | 主要贡献者 |
|------|---------|-----------|
| 测试稳定性 | 88 | SendaoYan |
| RISC-V | 42 | Anjian-Wen, Fei Yang |
| 核心库优化 | 31 | Shaojin Wen |
| C2 编译器 | 6 | Kuai Wei, han gq |
| G1 GC | 1 | Tongbao Zhang |

---

## 相关链接

- [OpenJDK 中国社区](https://openjdk.org/groups/china/)
- [Loongson JDK](https://github.com/loongson/jdk)