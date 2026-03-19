# Thomas Schatzl

> G1 GC 核心开发者，JEP 522 主导者

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Thomas Schatzl |
| **组织** | Oracle |
| **GitHub** | [@tschatzl](https://github.com/tschatzl) |
| **OpenJDK** | [@tschatzl](https://openjdk.org/census#tschatzl) |
| **角色** | OpenJDK Member, JDK Reviewer |
| **PRs** | [545 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Atschatzl+is%3Aclosed+label%3Aintegrated) |
| **主要领域** | G1 GC |
| **主导 JEP** | JEP 522: G1 GC Throughput Improvement |
| **活跃时间** | 2013 - 至今 |

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

- [OpenJDK Changesets](https://hg.openjdk.org/jdk/jdk/user?user=tschatzl)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=Thomas%20Schatzl)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=assignee%20%3D%20tschatzl)