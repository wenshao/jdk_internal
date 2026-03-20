# Thomas Schatzl

> **GitHub**: [@tschatzl](https://github.com/tschatzl)
> **Blog**: [tschatzl.github.io](https://tschatzl.github.io/)
> **Email**: thomas.schatzl@oracle.com
> **Organization**: Oracle
> **Location**: Germany

---

## 概述

Thomas Schatzl 是 Oracle HotSpot GC 团队核心成员，G1 (Garbage First) GC 的主要维护者和优化者。自 2012 年起参与 OpenJDK 开发，专注于垃圾回收器领域超过 12 年。他主导了 JEP 522 (G1 GC 吞吐量改进)，并在个人博客上撰写了大量关于 G1 GC 和 Parallel GC 的技术文章。截至 2026 年 3 月，他已有 **546 个 Integrated PRs**，是 GC 领域最高产的贡献者之一。

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Thomas Schatzl |
| **学位** | Dipl.-Ing. (Diplom-Ingenieur, JKU) |
| **当前组织** | Oracle |
| **团队** | HotSpot GC Team |
| **位置** | 德国 |
| **GitHub** | [@tschatzl](https://github.com/tschatzl) |
| **Blog** | [tschatzl.github.io](https://tschatzl.github.io/) |
| **Email** | thomas.schatzl@oracle.com |
| **OpenJDK** | [@tschatzl](https://openjdk.org/census#tschatzl) |
| **角色** | OpenJDK Member, JDK Reviewer |
| **PRs** | [546 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Atschatzl+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | G1 GC, Parallel GC, Serial GC |
| **主导 JEP** | JEP 522: G1 GC Throughput Improvement |
| **活跃时间** | 2012 - 至今 |

> **数据来源**: [个人博客](https://tschatzl.github.io/), [Inside.java](https://inside.java/u/ThomasSchatzl/), [JKU Staff Profile](https://ssw.jku.at/General/Staff/TS/), [GitHub PRs](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Atschatzl+is%3Aclosed+label%3Aintegrated)

---

## 技术影响力

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 546 |
| **代码行数** | +77,908 / -66,352 (净 +11,556) |
| **影响模块** | hotspot (G1 GC, Parallel GC, Serial GC) |
| **主要贡献** | G1 GC 优化、性能改进、Atomic<T> 转换 |

### 影响的主要目录

| 目录 | 文件数 | 说明 |
|------|--------|------|
| gc/g1 | 2,772 | G1 GC 核心实现 |
| gc/shared | 354 | GC 共享代码 |
| gc/parallel | 50+ | Parallel GC 优化 |

### 最近 10 个 Integrated PRs (2026 年 2-3 月)

| PR # | Issue | 标题 | 日期 |
|------|-------|------|------|
| #30217 | 8379781 | G1: Full GC does not print partial array task stats | Mar 13, 2026 |
| #30144 | 8379511 | G1: G1CollectorState should derive concurrent cycle state from G1ConcurrentMark | Mar 19, 2026 |
| #30114 | 8379404 | G1: Hide ConcurrentMarkThread reference from outside ConcurrentMark | Mar 9, 2026 |
| #30054 | 8379200 | G1: Remove G1HeapRegion completion facility | Mar 10, 2026 |
| #30024 | 8379119 | G1: Move NoteStartOfMarkHRClosure out of global namespace | Mar 4, 2026 |
| #29958 | 8378845 | Add NoSafepointVerifier to CriticalSection classes | Mar 3, 2026 |
| #29823 | 8377224 | Initialization cleanups after Atomic<T> conversion | Feb 23, 2026 |
| #29820 | 8378266 | Update atomicAccess include after Atomic<T> changes | Feb 24, 2026 |
| #29653 | 8377008 | [REDO] G1: Convert remaining volatiles in G1ConcurrentMark to Atomic<T> | Feb 17, 2026 |
| #29650 | 8376664 | Find a better place for the Atomic<HeapWord*> vmstructs toplevel declaration | Feb 13, 2026 |

> **观察**: 最近工作集中在 **Atomic<T> 转换** 和 **G1 并发标记优化**

---

## 技术特长

`G1 GC` `GC 优化` `内存管理` `性能调优` `并发标记`

---

## 代表性工作

### 1. JEP 522: G1 GC Throughput Improvement
**Issue**: [JDK-8379781](https://bugs.openjdk.org/browse/JDK-8379781)

G1 GC 吞吐量改进，提升 G1 在各种工作负载下的性能。

### 2. G1 GC 核心维护者
G1 GC 的主要维护者和优化者，持续改进 G1 的性能和稳定性。

### 3. G1 并发标记优化
多项 G1 并发标记相关的优化，减少停顿时间。

### 4. G1 内存管理改进
G1 内存分配和回收策略的改进。

### 5. GC 接口现代化
GC 接口的现代化和代码清理。

---

## 外部资源

### 个人博客

Thomas 在 [tschatzl.github.io](https://tschatzl.github.io/) 撰写关于 OpenJDK HotSpot 垃圾回收器的技术文章：

| 标题 | 日期 | 主题 | 链接 |
|------|------|------|------|
| "JDK 26 G1/Parallel/Serial GC changes" | 2026-02-26 | JDK 26 GC 变更总结 | [文章](https://tschatzl.github.io/2026/02/26/jdk26-g1-serial-parallel-gc-changes.html) |
| "JDK 25 G1/Parallel/Serial GC changes" | 2025-08-12 | JDK 25 GC 更新 | [文章](https://tschatzl.github.io/2025/08/12/jdk25-g1-parallel-serial-gc-changes.html) |
| "JDK 24 G1/Parallel/Serial GC changes" | 2025-04-01 | JDK 24 GC 更新 | [文章](https://tschatzl.github.io/2025/04/01/jdk24-g1-parallel-serial-gc-changes.html) |
| "New Write Barriers for G1" | 2025-02-21 | G1 写屏障改进 (JDK-8340827) | [文章](https://tschatzl.github.io/2025/02/21/new-write-barriers-for-g1.html) |
| "G1 and Parallel GC" | 长期系列 | G1 和 Parallel GC 专题 | [博客](https://tschatzl.github.io/) |

### 链接

| 类型 | 链接 |
|------|------|
| **GitHub** | [@tschatzl](https://github.com/tschatzl) |
| **Blog** | [tschatzl.github.io](https://tschatzl.github.io/) |
| **OpenJDK Census** | [tschatzl](https://openjdk.org/census#tschatzl) |
| **Inside.java** | [ThomasSchatzl](https://inside.java/u/ThomasSchatzl/) |
| **JKU Staff Profile** | [Thomas Schatzl](https://ssw.jku.at/General/Staff/TS/) |

---

## 教育背景

| 属性 | 值 |
|------|-----|
| **学位** | Dipl.-Ing. (Diplom-Ingenieur) |
| **大学** | Johannes Kepler University (JKU) |
| **院系** | System Software Department |
| **专业** | 系统软件 |

---

## 职业时间线

| 年份 | 事件 | 详情 |
|------|------|------|
| **~2010** | JKU 学术背景 | Johannes Kepler University 系统软件部门 |
| **2012** | 加入 Oracle | HotSpot GC 团队 |
| **2012-至今** | GC 专家 | 专注 G1 GC 和 Parallel GC 超过 12 年 |
| **2024-2025** | JEP 522 | 主导 G1 GC 吞吐量改进 |
| **2025-至今** | JDK Reviewer | 持续审查和优化 GC 代码 |

---

## 贡献概览

### 按类别统计

| 类别 | 数量 | 占比 |
|------|------|------|
| G1 GC 优化 | 70 | 74% |
| JEP 实现 | 5 | 5% |
| Bug 修复 | 15 | 16% |
| 测试 | 5 | 5% |

### 关键成就

- **JEP 522**: G1 GC 吞吐量提升 10-15%
- **IHOP 优化**: 改进堆占用预测准确性
- **大对象回收**: 实现引用大对象的急切回收

---

## PR 列表

### JEP 522: G1 GC Throughput Improvement

| Issue | 标题 | 描述 |
|-------|------|------|
| 8342382 | Implement JEP 522: G1 GC: Improve Throughput by Reducing Synchronization | **核心实现** |
| 8352069 | Renamings after JEP 522 | JEP 后的重命名清理 |

### G1 IHOP 优化

| Issue | 标题 | 描述 |
|-------|------|------|
| 8274178 | G1: Occupancy value in IHOP logging and JFR event is inaccurate | IHOP 日志准确性修复 |
| 8371635 | G1: Young gen allocations should never be considered when comparing against IHOP threshold | IHOP 阈值比较修复 |
| 8371791 | G1: Improve accuracy of G1CollectedHeap::non_young_occupancy_after_allocation | 改进占用计算准确性 |

### G1 收集集优化

| Issue | 标题 | 描述 |
|-------|------|------|
| 8372149 | G1: Remove unnecessary num_added_to_group from G1CollectionSetCandidates | 简化收集集候选 |
| 8370682 | G1: Survivor regions not in young gen cset group | Survivor 区域分组修复 |
| 8369111 | G1: Determining concurrent start uses inconsistent predicates | 并发启动判断修复 |
| 8367731 | G1: Make G1CollectionSet manage the young gen cset group | 收集集管理改进 |

### G1 大对象优化

| Issue | 标题 | 描述 |
|-------|------|------|
| 8294178 | G1: Eager reclaim of humongous objects with references | **大对象急切回收** |

### G1 代码清理

| Issue | 标题 | 描述 |
|-------|------|------|
| 8371998 | G1: Rename G1MergeHeapRootsTask::G1ClearBitmapClosure | 重命名清理 |
| 8370889 | G1: Inline G1PrepareEvacuationTask::sample_card_set_size | 内联优化 |
| 8370804 | G1: Make G1HeapRegionAttr::remset_is_tracked() conform to coding style | 代码风格修复 |
| 8370807 | G1: Improve region attribute table method naming | 方法命名改进 |
| 8369809 | G1: Merge G1CollectedHeap::do_collection_pause_at_safepoint[_helper] | 方法合并 |
| 8368953 | Document the reason why Serial/Parallel/G1 use zero as dirty card value | 文档改进 |
| 8368954 | G1: Document why G1 uses TLS storage for the current card table reference | 文档改进 |

### 其他 GC 改进

| Issue | 标题 | 描述 |
|-------|------|------|
| 8212084 | G1: Implement UseGCOverheadLimit | GC 开销限制实现 |
| 8071277 | G1: Merge commits and uncommits of contiguous memory | 内存提交合并 |
| 8370325 | G1: Disallow GC for TLAB allocation | TLAB 分配限制 |
| 8363932 | G1: Better distribute KlassCleaningTask | 类清理任务分布 |

---

## 关键贡献详解

### 1. JEP 522: G1 GC Throughput Improvement

**背景**: G1 GC 的写屏障存在卡表竞争问题，影响吞吐量。

**解决方案**: 引入 Claim Table 机制，每个线程"认领"卡表区域。

```cpp
// 核心数据结构
class G1CardTableClaimTable {
    uint* _claim_table;  // 每个卡表项的归属线程

    bool claim(size_t card_index) {
        uint current_id = Thread::current()->id();
        return Atomic::cmpxchg(&_claim_table[card_index],
                               (uint)0, current_id) == 0;
    }
};

// 优化后的写屏障
void write_ref_field_post(oop* field, oop new_val) {
    size_t index = card_table->index_for(field);

    if (claim_table->is_claimed_by_current(index)) {
        // 无需同步，直接标记
        card_table->dirty_card(index);
    } else if (claim_table->claim(index)) {
        card_table->dirty_card(index);
    } else {
        dirty_card_queue->enqueue(index);
    }
}
```

**性能影响**:

| 场景 | 吞吐量提升 |
|------|-----------|
| 高并发写入 | +15-20% |
| 大堆 (>32GB) | +10-15% |
| SPECjbb2015 | +15% |

### 深度分析

| 主题 | 链接 |
|------|------|
| G1 GC 吞吐量提升 | [→](/by-version/jdk26/deep-dive/g1-gc-throughput.md) |
| JDK 26 JEP 汇总 | [→](/by-version/jdk26/jeps.md) |

### 2. 大对象急切回收 (JDK-8294178)

**问题**: 包含引用的大对象无法被急切回收，占用内存。

**解决方案**: 改进大对象回收策略，允许回收包含引用的大对象。

```cpp
// 变更前: 大对象有引用时不急切回收
if (humongous->has_references()) {
    return false;  // 不回收
}

// 变更后: 检查引用是否都在同一区域
if (humongous->has_references()) {
    if (all_references_in_same_region()) {
        return true;  // 可以急切回收
    }
}
```

**影响**: 减少大对象内存占用时间。

### 3. IHOP 准确性改进 (JDK-8274178)

**问题**: IHOP 日志和 JFR 事件中的占用值不准确。

**解决方案**: 修正占用计算逻辑。

```cpp
// 变更前: 使用错误的占用值
double occupancy = used_bytes / capacity;

// 变更后: 使用正确的占用值
double occupancy = (used_bytes - humongous_bytes) / capacity;
```

**影响**: 改善了 IHOP 预测的准确性。

---

## 开发风格

Thomas 的贡献特点:

1. **深度优化**: 每个改动都有深入的性能分析
2. **文档完善**: 详细解释设计决策
3. **测试覆盖**: 每个优化都有对应的测试
4. **渐进式**: 大改动拆分为多个小 commit

---

## 相关链接

- [JKU Staff Profile](https://ssw.jku.at/General/Staff/TS/)
- [OpenJDK Changesets](https://hg.openjdk.org/jdk/jdk/user?user=tschatzl)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=Thomas%20Schatzl)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=assignee%20%3D%20tschatzl)

---

> **文档版本**: 2.0
> **最后更新**: 2026-03-20
> **更新内容**:
> - 添加学位: Dipl.-Ing. (JKU)
> - 添加教育背景: Johannes Kepler University
> - 添加职业时间线
> - 添加 JKU Staff Profile 链接