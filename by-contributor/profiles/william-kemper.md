# William Kemper

> **GitHub**: [@earthling-amzn](https://github.com/earthling-amzn)
> **LinkedIn**: [William Kemper](https://www.getprog.ai/profile/71722661)
> **Organization**: Amazon
> **Location**: Redwood City
> **JEP Draft**: JEP draft: Make Shenandoah's generational mode the default

---
## 目录

1. [概述](#1-概述)
2. [Basic Information](#2-basic-information)
3. [Contribution Overview](#3-contribution-overview)
4. [Complete PR List](#4-complete-pr-list)
5. [Key Contributions](#5-key-contributions)
6. [Development Style](#6-development-style)
7. [Related Links](#7-related-links)
8. [外部资源](#8-外部资源)

---


## 1. 概述

William Kemper 是 Amazon (AWS) 的 SDE III（软件开发工程师 III），专注于 Shenandoah 垃圾回收器的分代模式开发。他是 JEP 404 (Generational Shenandoah, Experimental) 和 JEP 521 (Generational Shenandoah, Product) 的 owner 和主要实现者。2024年1月由 Aleksey Shipilev 提名成为 JDK Committer，当时已贡献 20+ mainline changes。他在 JEP draft 中提出了将 Shenandoah 的分代模式设为默认值。

---

## 2. Basic Information

| Attribute | Value |
|-----------|-------|
| **Name** | William Kemper |
| **Current Organization** | Amazon |
| **Position** | SDE III (Software Development Engineer III) |
| **Location** | Redwood City |
| **Previous Organization** | Red Hat |
| **GitHub** | [@earthling-amzn](https://github.com/earthling-amzn) (25 repositories) |
| **OpenJDK** | [@wkemper](https://openjdk.org/census#wkemper) |
| **Role** | JDK Committer (2024-01), Shenandoah Project Committer |
| **PRs** | [127 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Aearthling-amzn+is%3Aclosed+label%3Aintegrated) |
| **Primary Areas** | Shenandoah GC, Generational Shenandoah (JEP 404, JEP 521) |
| **JEP Work** | JEP 404 (Generational Shenandoah, Experimental), JEP 521 (Generational Shenandoah, Product) |
| **JEP Draft** | JEP draft: Make Shenandoah's generational mode the default |

> **数据来源**: [GitHub](https://github.com/earthling-amzn), [JEP 521](https://openjdk.org/jeps/521), [JEP draft](https://openjdk.org/jeps/8379682), [CFV Committer](https://mail.openjdk.org/pipermail/jdk-dev/2024-January/008688.html)

## 3. Contribution Overview

### By Category

| Category | Count | Description |
|----------|-------|-------------|
| Generational Shenandoah | 35 | Core GenShen implementation, JEP 521 |
| Shenandoah Bug Fixes | 18 | Stability and correctness fixes |
| Performance Improvements | 5 | SATB barriers, evacuation optimization |
| Test Infrastructure | 5 | Test fixes and improvements |

### Key Areas of Expertise

- **Generational Shenandoah (JEP 521)**: Lead implementer of generational GC
- **SATB Barriers**: Snapshot-at-the-beginning barrier optimization
- **GC Control Loop**: Control thread mechanics and timed waits
- **Memory Management**: Region pinning, promotion tracking
- **Concurrent Collection**: Degenerated cycle handling, evacuation

## 4. Complete PR List

| Issue | Title | PR Link |
|-------|-------|---------|
| 8370039 | GenShen: array copy SATB barrier improvements | [JBS](https://bugs.openjdk.org/browse/JDK-8370039) |
| 8370041 | GenShen: Filter young pointers from thread local SATB buffers when only marking old | [JBS](https://bugs.openjdk.org/browse/JDK-8370041) |
| 8370521 | GenShen: Various code cleanup related to promotion | [JBS](https://bugs.openjdk.org/browse/JDK-8370521) |
| 8370667 | GenShen: Only make assertions about region pinning for collected generation | [JBS](https://bugs.openjdk.org/browse/JDK-8370667) |
| 8370726 | GenShen: Misplaced assertion that old referent is marked during young collection | [JBS](https://bugs.openjdk.org/browse/JDK-8370726) |
| 8370520 | GenShen: Track and report on promotion failures | [JBS](https://bugs.openjdk.org/browse/JDK-8370520) |
| 8369068 | GenShen: Generations still aren't reconciled assertion failure | [JBS](https://bugs.openjdk.org/browse/JDK-8369068) |
| 8369447 | GenShen: Regulator thread may observe inconsistent states | [JBS](https://bugs.openjdk.org/browse/JDK-8369447) |
| 8241066 | Shenandoah: fix or cleanup SH::do_full_collection | [JBS](https://bugs.openjdk.org/browse/JDK-8241066) |
| 8370050 | Shenandoah: Obsolete ShenandoahPacing option | [JBS](https://bugs.openjdk.org/browse/JDK-8370050) |
| 8367709 | GenShen: Dirty cards for objects that get promoted by safepoint | [JBS](https://bugs.openjdk.org/browse/JDK-8367709) |
| 8367646 | [GenShen] Control thread may overwrite gc cancellation cause set by mutator | [JBS](https://bugs.openjdk.org/browse/JDK-8367646) |
| 8368501 | Shenandoah: GC progress evaluation does not use generation | [JBS](https://bugs.openjdk.org/browse/JDK-8368501) |
| 8264851 | Shenandoah: Rework control loop mechanics to use timed waits | [JBS](https://bugs.openjdk.org/browse/JDK-8264851) |
| 8368499 | GenShen: Do not collect age census during evac when adaptive tenuring is disabled | [JBS](https://bugs.openjdk.org/browse/JDK-8368499) |
| 8368152 | Shenandoah: Incorrect behavior at end of degenerated cycle | [JBS](https://bugs.openjdk.org/browse/JDK-8368152) |
| 8365792 | GenShen: assertion "Generations aren't reconciled" | [JBS](https://bugs.openjdk.org/browse/JDK-8365792) |
| 8367473 | Shenandoah: Make the detailed evacuation metrics a runtime diagnostic option | [JBS](https://bugs.openjdk.org/browse/JDK-8367473) |
| 8367450 | Shenandoah: Log the composition of the collection set | [JBS](https://bugs.openjdk.org/browse/JDK-8367450) |
| 8367451 | GenShen: Remove the option to compute age census during evacuation | [JBS](https://bugs.openjdk.org/browse/JDK-8367451) |
| 8367378 | GenShen: Missing timing stats when old mark buffers are flushed during final update refs | [JBS](https://bugs.openjdk.org/browse/JDK-8367378) |
| 8365956 | GenShen: Adaptive tenuring threshold algorithm may raise threshold prematurely | [JBS](https://bugs.openjdk.org/browse/JDK-8365956) |
| 8365622 | Shenandoah: Fix Shenandoah simple bit map test | [JBS](https://bugs.openjdk.org/browse/JDK-8365622) |
| 8365571 | GenShen: PLAB promotions may remain disabled for evacuation threads | [JBS](https://bugs.openjdk.org/browse/JDK-8365571) |
| 8365572 | Shenandoah: Remove unused thread local _paced_time field | [JBS](https://bugs.openjdk.org/browse/JDK-8365572) |
| 8361726 | Shenandoah: More detailed evacuation instrumentation | [JBS](https://bugs.openjdk.org/browse/JDK-8361726) |
| 8360288 | Shenandoah crash at size_given_klass in op_degenerated | [JBS](https://bugs.openjdk.org/browse/JDK-8360288) |
| 8357550 | GenShen crashes during freeze: assert(!chunk->requires_barriers()) failed | [JBS](https://bugs.openjdk.org/browse/JDK-8357550) |
| 8359394 | GC cause cleanup | [JBS](https://bugs.openjdk.org/browse/JDK-8359394) |
| 8357976 | GenShen crash in swap_card_tables: Should be clean | [JBS](https://bugs.openjdk.org/browse/JDK-8357976) |
| 8358102 | GenShen: Age tables could be seeded with cumulative values | [JBS](https://bugs.openjdk.org/browse/JDK-8358102) |
| 8354078 | Implement JEP 521: Generational Shenandoah | [JBS](https://bugs.openjdk.org/browse/JDK-8354078) |
| 8355372 | GenShen: Test gc/shenandoah/generational/TestOldGrowthTriggers.java fails | [JBS](https://bugs.openjdk.org/browse/JDK-8355372) |
| 8355789 | GenShen: assert(_degen_point == ShenandoahGC::_degenerated_unset) failed | [JBS](https://bugs.openjdk.org/browse/JDK-8355789) |
| 8353596 | GenShen: Test TestClone.java#generational-no-coops intermittent timed out | [JBS](https://bugs.openjdk.org/browse/JDK-8353596) |
| 8354452 | Shenandoah: Enforce range checks on parameters controlling heuristic sleep times | [JBS](https://bugs.openjdk.org/browse/JDK-8354452) |
| 8353218 | Shenandoah: Out of date comment references Brooks pointers | [JBS](https://bugs.openjdk.org/browse/JDK-8353218) |
| 8352918 | Shenandoah: Verifier does not deactivate barriers as intended | [JBS](https://bugs.openjdk.org/browse/JDK-8352918) |
| 8348400 | GenShen: assert(ShenandoahHeap::heap()->is_full_gc_in_progress() || ...) failed | [JBS](https://bugs.openjdk.org/browse/JDK-8348400) |
| 8352299 | GenShen: Young cycles that interrupt old cycles cannot be cancelled | [JBS](https://bugs.openjdk.org/browse/JDK-8352299) |
| 8352091 | GenShen: assert(!(request.generation->is_old() && ...)) failed | [JBS](https://bugs.openjdk.org/browse/JDK-8352091) |
| 8350898 | Shenandoah: Eliminate final roots safepoint | [JBS](https://bugs.openjdk.org/browse/JDK-8350898) |
| 8351464 | Shenandoah: Hang on ShenandoahController::handle_alloc_failure | [JBS](https://bugs.openjdk.org/browse/JDK-8351464) |
| 8350905 | Shenandoah: Releasing a WeakHandle's referent may extend its lifetime | [JBS](https://bugs.openjdk.org/browse/JDK-8350905) |
| 8351444 | Shenandoah: Class Unloading may encounter recycled oops | [JBS](https://bugs.openjdk.org/browse/JDK-8351444) |
| 8350605 | assert(!heap->is_uncommit_in_progress()) failed | [JBS](https://bugs.openjdk.org/browse/JDK-8350605) |
| 8349094 | GenShen: Race between control and regulator threads may violate assertions | [JBS](https://bugs.openjdk.org/browse/JDK-8349094) |
| 8348092 | Shenandoah: assert(nk >= _lowest_valid_narrow_klass_id ...) failed | [JBS](https://bugs.openjdk.org/browse/JDK-8348092) |
| 8348268 | Test gc/shenandoah/TestResizeTLAB.java#compact: fatal error | [JBS](https://bugs.openjdk.org/browse/JDK-8348268) |
| 8349002 | GenShen: Deadlock during shutdown | [JBS](https://bugs.openjdk.org/browse/JDK-8349002) |
| 8348420 | Shenandoah: Check is_reserved before using ReservedSpace instances | [JBS](https://bugs.openjdk.org/browse/JDK-8348420) |
| 8345750 | Shenandoah: Test TestJcmdHeapDump.java#aggressive intermittent assert | [JBS](https://bugs.openjdk.org/browse/JDK-8345750) |
| 8347617 | Shenandoah: Use consistent name for update references phase | [JBS](https://bugs.openjdk.org/browse/JDK-8347617) |
| 8344049 | Shenandoah: Eliminate init-update-refs safepoint | [JBS](https://bugs.openjdk.org/browse/JDK-8344049) |
| 8347620 | Shenandoah: Use 'free' tag for free set related logging | [JBS](https://bugs.openjdk.org/browse/JDK-8347620) |
| 8346737 | GenShen: Generational memory pools should not report zero for maximum capacity | [JBS](https://bugs.openjdk.org/browse/JDK-8346737) |
| 8346688 | GenShen: Missing metadata trigger log message | [JBS](https://bugs.openjdk.org/browse/JDK-8346688) |
| 8346690 | Shenandoah: Fix log message for end of GC usage report | [JBS](https://bugs.openjdk.org/browse/JDK-8346690) |
| 8346051 | MemoryTest fails when Shenandoah's generational mode is enabled | [JBS](https://bugs.openjdk.org/browse/JDK-8346051) |
| 8345970 | pthread_getcpuclockid related crashes in shenandoah tests | [JBS](https://bugs.openjdk.org/browse/JDK-8345970) |

> **JBS Link**: https://bugs.openjdk.org/browse/JDK-[Issue Number]

## 5. Key Contributions

### 1. JEP 404 / JEP 521: Generational Shenandoah (JDK-8354078)

The flagship contribution - implementing generational garbage collection for Shenandoah. JEP 404 integrated as experimental in JDK 26; JEP 521 drops experimental status, making it a product feature. Extensively tested with DaCapo, SPECjbb2015, SPECjvm2008, and Heapothesys benchmarks.

```cpp
// Core generational Shenandoah architecture
class ShenandoahGenerationalHeap : public ShenandoahHeap {
private:
  ShenandoahYoungGeneration* _young_generation;
  ShenandoahOldGeneration* _old_generation;
  
  // Age tracking for promotion decisions
  ShenandoahAgeCensus* _age_census;
  
public:
  // Generational collection set selection
  void select_generational_collection_set();
  
  // Card table management for cross-generational references
  ShenandoahCardTable* card_table() const;
  
  // Promotion tracking
  void track_promotion_failure();
};
```

### 2. SATB Barrier Improvements (JDK-8370039, JDK-8370041)

Optimized array copy SATB barriers for generational mode.

```cpp
// Improved SATB barrier for array copies
void ShenandoahBarrierSet::arraycopy_satb_barrier(oop* src, oop* dst, size_t length) {
  // Filter young pointers when only marking old generation
  if (_heap->is_concurrent_old_mark_in_progress() && 
      !_heap->is_concurrent_young_mark_in_progress()) {
    // Skip young generation pointers
    for (size_t i = 0; i < length; i++) {
      oop obj = src[i];
      if (obj != nullptr && _heap->is_in_old(obj)) {
        dst[i] = obj;
        ShenandoahBarrierSet::satb_enqueue(obj);
      }
    }
  } else {
    // Standard SATB barrier
    for (size_t i = 0; i < length; i++) {
      if (src[i] != nullptr) {
        ShenandoahBarrierSet::satb_enqueue(src[i]);
      }
    }
  }
}
```

### 3. Control Loop Rework (JDK-8264851)

Reworked control loop mechanics to use timed waits for better responsiveness.

```cpp
void ShenandoahController::run_service() {
  while (!should_terminate()) {
    // Use timed waits instead of indefinite blocking
    MonitorLocker ml(&_control_lock, Mutex::_no_safepoint_check_flag);
    
    if (_heap->check_allocation_failure()) {
      handle_alloc_failure();
    } else {
      // Timed wait for better responsiveness
      ml.wait(100); // 100ms timeout
    }
    
    // Check for GC triggers
    check_gc_triggers();
  }
}
```

### 4. Promotion Failure Tracking (JDK-8370520)

Added tracking and reporting for promotion failures.

```cpp
class ShenandoahPromotionStats {
private:
  size_t _promotion_attempts;
  size_t _promotion_failures;
  size_t _promotion_bytes;
  
public:
  void record_promotion(bool success, size_t size) {
    _promotion_attempts++;
    _promotion_bytes += size;
    if (!success) {
      _promotion_failures++;
    }
  }
  
  void print_on(outputStream* st) const {
    st->print_cr("Promotion attempts: " SIZE_FORMAT 
                 ", failures: " SIZE_FORMAT 
                 ", bytes: " SIZE_FORMAT,
                 _promotion_attempts, _promotion_failures, _promotion_bytes);
  }
};
```

### 5. Degenerated Cycle Handling (JDK-8368152)

Fixed incorrect behavior at end of degenerated cycle.

```cpp
void ShenandoahDegeneratedGC::finish() {
  // Ensure proper state transition
  if (_heap->is_concurrent_mark_in_progress()) {
    // Complete marking before finishing
    _heap->concurrent_mark()->finish_mark();
  }
  
  // Reconcile generations before final update refs
  if (_heap->mode()->is_generational()) {
    _heap->old_generation()->reconcile_generation();
  }
  
  // Final update references
  _heap->update_references();
}
```

## 6. Development Style

### Code Quality Focus

1. **Defensive Programming**: Extensive assertions for debugging
2. **Logging**: Detailed GC logging for diagnostics
3. **Test Coverage**: Comprehensive test infrastructure
4. **Documentation**: Clear comments explaining GC mechanics

### Commit Patterns

- Groups related fixes together (e.g., multiple GenShen fixes)
- Uses "GenShen:" prefix for generational Shenandoah changes
- Uses "Shenandoah:" prefix for general Shenandoah changes
- Often includes test fixes alongside core changes

### Testing Approach

- Stress testing with various heap configurations
- Concurrent test scenarios
- Memory pressure testing
- Platform-specific testing

## 7. Related Links

- **GitHub**: [earthling-amzn](https://github.com/earthling-amzn)
- **OpenJDK**: [wkemper](https://openjdk.org/people/wkemper)
- **JBS Issues**: [bugs.openjdk.org](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20wkemper)
- **GitHub Commits**: [openjdk/jdk](https://github.com/openjdk/jdk/commits?author=earthling-amzn)
- **CFV: Committer**: [JDK Committer nomination (Jan 2024)](https://mail.openjdk.org/pipermail/jdk-dev/2024-January/008688.html)
- **JEP 404**: [Generational Shenandoah (Experimental)](https://openjdk.org/jeps/404)
- **JEP 521**: [Generational Shenandoah (Product)](https://openjdk.org/jeps/521)
- **JEP Draft**: [Make Shenandoah's generational mode the default](https://openjdk.org/jeps/8379682)

---

## 8. 外部资源

### JEP Draft

| JEP | 标题 | 状态 |
|-----|------|------|
| JEP draft | Make Shenandoah's generational mode the default | Draft |

### Amazon Corretto

- 负责 Amazon Corretto 中 Shenandoah GC 的维护和改进
- 参与 JDK 8u backport 审查

---

> **文档版本**: 3.0
> **最后更新**: 2026-03-22
> **更新内容**:
> - 修正角色: JDK Committer (非 Reviewer)，2024-01 由 Aleksey Shipilev 提名
> - 添加 JEP 404 (Generational Shenandoah, Experimental) 信息
> - 更新 JEP 521 说明: 从 experimental 到 product feature
> - 更新 PRs 统计: 127 integrated
> - 添加 CFV 和 JEP 404 链接

## 审查统计

| 指标 | 值 |
|------|-----|
| **总审查次数** | 281 |
| **活跃仓库数** | 7 |
