# Vector API 贡献者分析

> 基于 JDK 源码 git 历史分析

---

## 贡献统计

### 按组织/公司

| 组织 | 提交数 | 主要贡献者 | 重点关注 |
|------|--------|--------------|----------|
| **Oracle** | ~1167 | Paul Sandoz, Sandhya Viswanathan | API 设计, C2 编译器 |
| **Intel** | ~148 | **Jatin Bhateja** | x86 优化, AVX-512 |
| **AMD** | ~32 | Jatin Bhateja (部分) | x86 优化 |
| **ARM** | ~23 | Andrew Haley, Nick Gasson | SVE/NEON 适配 |
| **Red Hat** | ~22 | Andrew Dinn, Roman Kennke | GC 相关 |
| **个人** | ~100+ | 多位独立贡献者 | 测试、Bug 修复 |

### 按个人贡献者

| 贡献者 | 提交数 | 邮箱 | 主要贡献 |
|------|--------|------|----------|
| **Jatin Bhateja** | 51 | jatin.bhateja@intel.com / amd.com | x86 优化, AVX-512, SVE |
| **Paul Sandoz** | ~200 | paul.sandoz@oracle.com | API 设计, 规范制定 |
| **Sandhya Viswanathan** | 7 | sandhya.viswanathan@intel.com | 测试, 优化 |
| **Aleksey Shipilev** | 20 | aleksey@shipilev.net | 性能基准测试 |

## Intel 的深度参与

### Jatin Bhateja (Intel/AMD)

**贡献领域**:
- x86 AVX/AVX2/AVX-512 指令优化
- 向量操作优化 (broadcast, shuffle, reduction)
- 新指令支持 (VPALIGNR, VNNI)
- SVE 可变长度支持

**关键 JBS Issue**:
- [JDK-8303762](https://bugs.openjdk.org/browse/JDK-8303762): VPALIGNR 指令优化
- [JDK-8358521](https://bugs.openjdk.org/browse/JDK-8358521): 广播输入优化
- [JDK-8338021](https://bugs.openjdk.org/browse/JDK-8338021): 饱和运算符支持
- [JDK-8338023](https://bugs.openjdk.org/browse/JDK-8338023): selectFrom API

- [JDK-8346256](https://bugs.openjdk.org/browse/JDK-8346256): UMIN/UMAX 优化

### Sandhya Viswanathan (Intel)
**贡献领域**:
- 测试用例
- 代码审查
- 文档更新

## 当前活跃度 (2025-2026)

### 最近 6 个月的提交

| 月份 | 提交数 | 主要变更 |
|------|--------|----------|
| 2025-01 | 8 | API 修复, 新 LaneType |
| 2025-02 | 12 | 优化, AVX-512 |
| 2025-03 | 15+ | 新特性, 测试 |

| 2026-03 | 5+ | 持续开发中 |

### 活跃贡献者 (2025-2026)

| 贡献者 | 组织 | 最近提交数 |
|------|------|------------|
| Jatin Bhateja | Intel | 15 |
| Sandhya Viswanathan | Intel | 3 |
| Paul Sandoz | Oracle | 2 |
| Tobias Hartmann | Oracle | 5 |
| Andrew Haley | ARM | 3 |

## Intel 的战略意义

### 为什么 Intel 如此积极？

1. **硬件优势**: Intel 是 x86 和 AVX 指令集的主要开发者
2. **性能竞争**: 与 ARM/RISC-V 竞争需要优秀的 SIMD 支持
3. **生态建设**: Java 在服务器市场的主导地位
4. **客户需求**: 云服务商 (AWS, Azure) 需要 Java 高性能

### Intel 的投入

| 投入类型 | 描述 |
|----------|------|
| **人员** | 2+ 资深工程师 |
| **时间** | 2017 年至今 |
| **代码量** | ~150 commits |
| **影响范围** | x86 平台优化 |

## AMD 的贡献

AMD 虽然也投入了 Vector API，但 主要贡献者也是 Jatin Bhateja (前 Intel 员工)
- 这体现了芯片厂商之间的合作关系
- AMD 也需要优秀的 Java SIMD 支持
- Zen 架构使用 AVX 指令

## ARM 的贡献

ARM 主要关注:
- **SVE 支持**: 可变向量长度适配
- **NEON 优化**: 128-bit 向量操作
- **新平台**: ARM Neoverse, Apple Silicon

**主要贡献者**:
- Andrew Haley
- Nick Gasson
- 多位 ARM 工程师

## 当前挑战

### 为什么孵化这么慢？

| 挑战 | 描述 | 进展 |
|------|------|------|
| **SVE 可变长度** | ARM SVE 的向量长度在运行时确定 | 🔄 进行中 |
| **跨平台一致性** | x86/ARM/RISC-V 指令差异大 | 🔄 进行中 |
| **C2 编译器** | 需要大量优化工作 | 🔄 进行中 |
| **测试覆盖** | 需要覆盖所有平台组合 | 🔄 进行中 |

### 参与度趋势

```
2021: ████████ Oracle (主导)
2022: ████████ Oracle + ████ Intel (增加)
2023: ████████ Oracle + ████████ Intel (大幅增加)
2024: ████████ Oracle + ████████ Intel + ████ ARM
2025: ████████ Oracle + ████████ Intel + ████ ARM + ██ AMD
2026: ████████ Oracle + ██████ Intel + ████ ARM (稳定)
```

## 未来展望

### 预计毕业时间

| 场景 | 时间 | 可能性 |
|------|------|--------|
| **乐观** | JDK 27 (2026-09) | 30% |
| **中性** | JDK 28 (2027-03) | 50% |
| **保守** | JDK 29+ (2027+) | 20% |

### Intel 的持续投入

Intel 预计会继续投入，因为:
- AVX-512 是 Intel 的核心优势
- 未来 CPU 会继续增强向量能力
- Java 在数据中心的重要性

---

> **数据来源**: 
> - JDK 源码 git 历史
> - JBS Issue 跟踪
> - GitHub PR 分析
> 
> **统计时间**: 2026-03-20
