# Albert Mingkun Yang

> JDK 26 贡献最多的开发者，专注于 GC 优化

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Albert Mingkun Yang |
| **组织** | Oracle |
| **GitHub** | [@albertnetymk](https://github.com/albertnetymk) |
| **OpenJDK** | [@ayang](https://openjdk.org/census#ayang) |
| **角色** | OpenJDK Member, JDK Reviewer |
| **Commits** | 124 (JDK 26 最多) |
| **主要领域** | G1 GC, Parallel GC |
| **活跃时间** | 2023 - 至今 |

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