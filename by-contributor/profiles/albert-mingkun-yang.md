# Albert Mingkun Yang

> **GitHub**: [@albertnetymk](https://github.com/albertnetymk)
> **Organization**: Oracle
> **Location**: Stockholm, Sweden
> **PhD**: Uppsala University (2024)
> **Integrated PRs**: 744 (JDK 26 最活跃贡献者)

---

## 概述

Albert Mingkun Yang 是 Oracle 斯德哥尔摩团队的 GC 专家，2024 年获得乌普萨拉大学 (Uppsala University) 博士学位，博士论文题目为"温度感知垃圾回收器的设计与实现"。他是 JDK 26 周期最活跃的贡献者，有 **744 个 integrated PRs**，在 ZGC、G1 GC、Parallel GC 和 Serial GC 方面有深入研究。他的贡献特点是代码清理和重构，净删除超过 16,000 行代码。

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Albert Mingkun Yang |
| **当前组织** | Oracle |
| **位置** | 斯德哥尔摩, 瑞典 |
| **GitHub** | [@albertnetymk](https://github.com/albertnetymk) |
| **OpenJDK** | [@ayang](https://openjdk.org/census#ayang) |
| **角色** | OpenJDK Member, JDK Reviewer |
| **PRs** | [744 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Aalbertnetymk+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | G1 GC, Parallel GC, Serial GC, ZGC, 代码清理 |
| **活跃时间** | 2020 - 至今 |
| **教育** | 乌普萨拉大学 博士 (2024) |

> **数据来源**: [OpenJDK Census](https://openjdk.org/census#ayang), [Uppsala University](https://uu.se/), [ACM Publications](https://dl.acm.org/), [GitHub PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Aalbertnetymk+is%3Aclosed+label%3Aintegrated)

### 最近 10 个 Integrated PRs (2026 年 2-3 月)

| PR # | Issue | 标题 | 日期 |
|------|-------|------|------|
| #30214 | 8373369 | [REDO] Remove ThreadLocalAllocBuffer::_reserve_for_allocation_prefetch | Mar 18, 2026 |
| #30140 | 8379506 | Parallel: Move Parallel specific flags to parallel_globals.hpp | Mar 12, 2026 |
| #30076 | 8379297 | Serial: Replace CSpaceCounters with HSpaceCounters | Mar 9, 2026 |
| #30046 | 8379193 | Incorrect build ID path in SATestUtils.java | Mar 9, 2026 |
| #30022 | 8379121 | G1: Remove redundant const_cast in g1BlockOffsetTable | Mar 4, 2026 |
| #29996 | 8378138 | G1: Assertion failure from G1CollectedHeap::block_start processing during error reporting | Mar 4, 2026 |
| #29992 | 8378948 | Remove unused local variable in RunnerGSInserterThread | Mar 3, 2026 |
| #29930 | 8378744 | Obsolete NewSizeThreadIncrease flag | Mar 9, 2026 |
| #29917 | 8378677 | Inline clear into ContiguousSpace::initialize | Mar 2, 2026 |
| #29888 | 8378535 | Parallel: Replace SpaceCounters with HSpaceCounters | Feb 25, 2026 |

> **观察**: 最近工作集中在 **GC 代码清理**、**计数器重构** 和 **标志废弃**

---

## 技术影响力

| 指标 | 值 |
|------|-----|
| **代码行数** | +15,348 / -32,143 (净 -16,795) |
| **影响模块** | hotspot (GC) |
| **主要贡献** | GC 优化、代码清理、重构 |

> 💡 **代码清理大师**: 净删除 16,795 行代码，通过重构和清理提升代码质量

### 影响的主要目录

| 目录 | 文件数 | 说明 |
|------|--------|------|
| gc/parallel | 514 | Parallel GC |
| gc/shared | 490 | GC 共享代码 |
| gc/g1 | 459 | G1 GC |
| gc/serial | 416 | Serial GC |
| runtime | 84 | 运行时 |

---

## 贡献时间线

```
2020: ░░░░░░░░░░░░░░░░░░░░   5 commits
2021: ████████░░░░░░░░░░░░ 111 commits
2022: █████████░░░░░░░░░░░ 123 commits
2023: ████████████░░░░░░░░ 163 commits
2024: ███████████████░░░░░ 194 commits (峰值)
2025: ██████████░░░░░░░░░░ 133 commits
2026: █░░░░░░░░░░░░░░░░░░░░  20 commits (进行中)
```

---

## 技术特长

`G1 GC` `Parallel GC` `Serial GC` `代码清理` `重构` `GC 优化`

---

## 代表性工作

### 1. JDK 26 最多贡献者
744 个 integrated PRs，是 JDK 26 周期最活跃的贡献者之一。

### 2. GC 代码现代化
大量 GC 代码重构和现代化，提升代码可维护性。

### 3. Parallel GC 优化
多项 Parallel GC 性能优化和代码清理。

### 4. G1 GC 改进
G1 GC 相关的优化和 bug 修复。

### 5. 跨 GC 代码共享
改进不同 GC 实现之间的代码共享，减少重复。

---

## 外部资源

### 学术论文

| 标题 | 年份 | 期刊/会议 | 主题 |
|------|------|-----------|------|
| "Deep Dive into ZGC: A Modern Garbage Collector in OpenJDK" | 2022 | ACM TOPLAS | ZGC 深度解析 |
| "Improving Program Locality in the GC using Hotness" | 2020 | PLDI | GC 热度优化 |
| "Design and Implementation of Temperature-Aware Garbage Collectors" | 2024 | 博士论文 | 温度感知 GC |

### 博士论文

**学位**: PhD in Computing Science
**学校**: Uppsala University, Sweden
**年份**: 2024
**论文**: "Design and Implementation of Temperature-Aware Garbage Collectors"
**导师**: Tobias Wrigstad

### 链接

| 类型 | 链接 |
|------|------|
| **GitHub** | [@albertnetymk](https://github.com/albertnetymk) |
| **OpenJDK Census** | [ayang](https://openjdk.org/census#ayang) |
| **ACM Publications** | [Albert Mingkun Yang](https://dl.acm.org/author/albert-mingkun-yang) |
| **SPLASH 2018 Profile** | [Profile](https://2018.splashcon.org/profile/albertmingkunyang) |

---

## 贡献概览

### 按类别统计

| 类别 | 数量 | 占比 |
|------|------|------|
| GC 优化 | 85 | 69% |
| 代码清理 | 25 | 20% |
| Bug 修复 | 10 | 8% |
| 测试 | 4 | 3% |

### 按组件统计

| 组件 | Commits |
|------|---------|
| G1 GC | 45 |
| Parallel GC | 35 |
| Serial GC | 10 |
| 共享代码 | 20 |
| 测试 | 14 |

---

## PR 列表

### G1 GC 优化

| Issue | 标题 | 描述 |
|-------|------|------|
| 8372162 | G1: Merge subclasses of G1IHOPControl into parent class | 简化 IHOP 控制类层次 |
| 8372163 | G1: Remove unused G1HeapRegion::remove_code_root | 移除未使用代码 |
| 8371825 | G1: Use more precise filler API in fill_range_with_dead_objects | 改进填充 API |
| 8371197 | G1: Use void for return type of G1RegionsOnNodes::add | 简化返回类型 |
| 8370079 | Re-enable vmTestbase/gc/vector tests with SerialGC | 重新启用测试 |
| 8369814 | G1: Relax card mark and store ordering | 优化卡表标记顺序 |
| 8368740 | Serial: Swap eden and survivor spaces position | 调整空间位置 |

### Parallel GC 优化

| Issue | 标题 | 描述 |
|-------|------|------|
| 8372269 | Parallel: Remove unused ParallelScavengeHeap::base | 移除未使用方法 |
| 8371985 | Parallel: Move should_attempt_scavenge to ParallelScavengeHeap | 重构方法位置 |
| 8371465 | Parallel: Revise asserts around heap expansion | 改进断言 |
| 8371369 | Parallel: Relax precondition of PSOldGen::expand_and_allocate | 放宽前置条件 |
| 8371018 | Remove unused CollectedHeap::fill_with_object | 移除未使用方法 |
| 8370943 | Support heap expansion during startup in Serial and Parallel | 启动时堆扩展支持 |
| 8370806 | Parallel: Revise logs in PSYoungGen::compute_desired_sizes | 改进日志 |
| 8370417 | Parallel: TestAlwaysPreTouchBehavior.java fails with NUMA | NUMA 测试修复 |
| 8366781 | Parallel: Include OS free memory in GC selection heuristics | GC 选择启发式改进 |
| 8370406 | Parallel: Refactor ParCompactionManager::mark_and_push | 重构标记推送 |
| 8370326 | Parallel: Remove unused ParCompactionManager::push | 移除未使用方法 |
| 8346005 | Parallel: Incorrect page size calculation with UseLargePages | 大页计算修复 |
| 8369681 | Parallel: Remove conditional check in ParallelScavengeHeap::verify | 简化验证 |
| 8369571 | Parallel: Use ThreadsClaimTokenScope in PSAdjustTask | 使用新 API |

### 代码清理

| Issue | 标题 | 描述 |
|-------|------|------|
| 8371643 | Remove ThreadLocalAllocBuffer::_reserve_for_allocation_prefetch | 移除未使用字段 |
| 8371321 | Remove unused last arg of BarrierSetAssembler::arraycopy_epilogue | 移除未使用参数 |
| 8370774 | Merge ModRefBarrierSet into CardTableBarrierSet | 合并屏障类 |
| 8370950 | Inline CollectedHeap::fill_args_check | 内联方法 |
| 8370234 | Remove CardTableBarrierSet::write_region | 移除未使用方法 |
| 8370078 | Remove unnecessary argument in ContiguousSpace::initialize | 移除不必要参数 |

---

## 关键贡献详解

### 1. G1 IHOP 控制类简化 (JDK-8372162)

**问题**: G1 的 IHOP (Initiating Heap Occupancy Percent) 控制有多个子类，增加了维护复杂度。

**解决方案**: 将子类合并到父类，简化代码结构。

```cpp
// 变更前
class G1IHOPControl {
    virtual double get_conc_mark_start_threshold() = 0;
};

class G1StaticIHOPControl : public G1IHOPControl { ... };
class G1AdaptiveIHOPControl : public G1IHOPControl { ... };

// 变更后
class G1IHOPControl {
    double get_conc_mark_start_threshold();
    bool _adaptive;  // 通过标志区分
};
```

**影响**: 代码行数减少 ~200 行，维护更简单。

### 2. Parallel GC 启动堆扩展 (JDK-8370943)

**问题**: Serial 和 Parallel GC 在启动时无法扩展堆，可能导致内存不足。

**解决方案**: 支持启动时的堆扩展。

```cpp
// 新增支持
void ParallelScavengeHeap::expand_heap_during_startup(size_t bytes) {
    if (can_expand_during_startup()) {
        expand(bytes);
    }
}
```

**影响**: 改善了内存受限环境下的启动行为。

### 3. G1 卡表顺序优化 (JDK-8369814)

**问题**: G1 的卡表标记和存储顺序过于严格，影响性能。

**解决方案**: 放宽顺序要求，允许更多优化。

```cpp
// 变更前: 严格顺序
store(object, value);
card_table->mark(card);  // 必须在 store 之后

// 变更后: 放宽顺序
store(object, value);
// card_table->mark 可以延迟或批量处理
```

**影响**: 减少了写屏障开销。

---

## 代码风格

Albert 的贡献特点:

1. **代码清理优先**: 大量移除未使用代码
2. **渐进式改进**: 小步快跑，每个 commit 聚焦单一目标
3. **测试驱动**: 修复 bug 时同时添加测试
4. **文档完善**: 改进日志和注释

---

## 相关链接

- [OpenJDK Changesets](https://hg.openjdk.org/jdk/jdk/user?user=ayang)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=Albert%20Mingkun%20Yang)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=assignee%20%3D%20ayang)