# 中国贡献者

> JDK 26 中来自中国开发者的贡献

---

## 概览

JDK 26 中有多位中国开发者做出了重要贡献，涵盖 GC、编译器、RISC-V、核心库等领域。

> **数据来源**: JDK git 仓库 `upstream_master` 分支 (2025-09-01 至 2026-03-20)  
> **统计时间**: 2026-03-19  
> **注意**: 仅统计已合并到 master 分支的 commits

---

## 贡献者列表 (已合并 master)

| 贡献者 | 组织 | Commits | 主要领域 | 详情 |
|--------|------|---------|----------|------|
| [SendaoYan](sendaoyan.md) | 海光 | 56 | 测试稳定性 | [查看详情](sendaoyan.md) |
| [Chen Liang](chen-liang.md) | Oracle | 36 | ClassFile API | [查看详情](chen-liang.md) |

---

## 贡献者列表 (PR 待合并)

> 以下贡献者有活跃的 PR，但尚未合并到 master 分支

| 贡献者 | 组织 | PR 数量 | 主要领域 |
|--------|------|---------|----------|
| [Shaojin Wen](shaojin-wen.md) | 阿里巴巴 | 97 | 核心库优化 |
| Anjian-Wen | 字节跳动 | 43 | RISC-V 向量指令 |
| Hamlin Li | Rivos | 49 | RISC-V |
| Dingli Zhang | ISCAS | 11 | RISC-V |
| Fei Yang | ISCAS | 6 | RISC-V |
| [Kuai Wei](kuai-wei.md) | 阿里巴巴 | 13 | C2 编译器 |

---

## 详细贡献

### SendaoYan (海光)

| 属性 | 值 |
|------|-----|
| **Commits** | 56 |
| **主要领域** | 测试稳定性 |
| **GitHub** | [@sendaoYan](https://github.com/sendaoYan) |

**关键 PR**:

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8354894 | java/lang/Thread/virtual/Starvation.java timeout on server with high CPUs | [JBS-8354894](https://bugs.openjdk.org/browse/JDK-8354894) |
| 8343340 | Swapping checking do not work for MetricsMemoryTester failcount | [JBS-8343340](https://bugs.openjdk.org/browse/JDK-8343340) |
| 8368677 | acvp test should throw SkippedException when no ACVP-Server available | [JBS-8368677](https://bugs.openjdk.org/browse/JDK-8368677) |

👉 [查看完整 PR 列表](sendaoyan.md)

---

### Chen Liang (Oracle)

| 属性 | 值 |
|------|-----|
| **Commits** | 36 |
| **主要领域** | ClassFile API、反射 |
| **GitHub** | [@liach](https://github.com/liach) |

**关键 PR**:

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8352748 | Remove com.sun.tools.classfile from the JDK | [JBS-8352748](https://bugs.openjdk.org/browse/JDK-8352748) |
| 8297271 | AccessFlag.maskToAccessFlags should be specific to class file version | [JBS-8297271](https://bugs.openjdk.org/browse/JDK-8297271) |

👉 [查看完整 PR 列表](chen-liang.md)

---

### Shaojin Wen (阿里巴巴) - PR 待合并

| 属性 | 值 |
|------|-----|
| **PRs** | 97 integrated |
| **主要领域** | 核心库性能优化 |
| **GitHub** | [@wenshao](https://github.com/wenshao) |

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

### Anjian-Wen (字节跳动) - PR 待合并

| 属性 | 值 |
|------|-----|
| **组织** | 字节跳动 (ByteDance) |
| **PRs** | 43 |
| **主要领域** | RISC-V 向量指令 |

**关键 PR**:

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8329887 | RISC-V: C2: Support Zvbb Vector And-Not instruction | [JBS-8329887](https://bugs.openjdk.org/browse/JDK-8329887) |
| 8349632 | RISC-V: Add Zfa fminm/fmaxm | [JBS-8349632](https://bugs.openjdk.org/browse/JDK-8349632) |
| 8351140 | RISC-V: Intrinsify Unsafe::setMemory | [JBS-8351140](https://bugs.openjdk.org/browse/JDK-8351140) |

---

### Kuai Wei (阿里巴巴) - PR 待合并

| 属性 | 值 |
|------|-----|
| **组织** | 阿里巴巴 (Alibaba) |
| **PRs** | 13 integrated |
| **主要领域** | C2 编译器 |

**关键 PR**:

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8356328 | Some C2 IR nodes miss size_of() function | [JBS-8356328](https://bugs.openjdk.org/browse/JDK-8356328) |
| 8347405 | MergeStores with reverse bytes order value | [JBS-8347405](https://bugs.openjdk.org/browse/JDK-8347405) |

👉 [查看完整 PR 列表](kuai-wei.md)

---

## 统计

### 按领域

| 领域 | Commits/PRs | 主要贡献者 |
|------|-------------|-----------|
| 测试稳定性 | 56 | SendaoYan |
| ClassFile API | 36 | Chen Liang |
| 核心库优化 | 97 PRs | Shaojin Wen |
| RISC-V | 100+ PRs | Anjian-Wen, Hamlin Li, Dingli Zhang, Fei Yang |
| C2 编译器 | 13 PRs | Kuai Wei |

---

## 相关链接

- [OpenJDK 中国社区](https://openjdk.org/groups/china/)
- [Loongson JDK](https://github.com/loongson/jdk)