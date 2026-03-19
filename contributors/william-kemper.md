# William Kemper

## Basic Information

| Attribute | Value |
|-----------|-------|
| **Name** | William Kemper |
| **Current Organization** | Amazon |
| **GitHub** | [@wkemper](https://github.com/wkemper), [@earthling-amzn](https://github.com/earthling-amzn) |
| **OpenJDK** | [@wkemper](https://openjdk.org/census#wkemper) |
| **Role** | JDK Reviewer |
| **PRs** | [123 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Aearthling-amzn+is%3Aclosed+label%3Aintegrated) |
| **Primary Areas** | Shenandoah GC, Generational Shenandoah (JEP 521) |

### Organization History

| Period | Organization | Email |
|--------|--------------|-------|
| Prior | Red Hat | - |
| Present | Amazon | kemperw@amazon.com |

> **Data as of**: 2026-03-19

## Contribution Overview

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

## Complete PR List

| Issue | Title | PR Link |
|-------|-------|---------|
| 8370039 | GenShen: array copy SATB barrier improvements | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8370041 | GenShen: Filter young pointers from thread local SATB buffers when only marking old | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8370521 | GenShen: Various code cleanup related to promotion | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8370667 | GenShen: Only make assertions about region pinning for collected generation | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8370726 | GenShen: Misplaced assertion that old referent is marked during young collection | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8370520 | GenShen: Track and report on promotion failures | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8369068 | GenShen: Generations still aren't reconciled assertion failure | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8369447 | GenShen: Regulator thread may observe inconsistent states | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8241066 | Shenandoah: fix or cleanup SH::do_full_collection | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8370050 | Shenandoah: Obsolete ShenandoahPacing option | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8367709 | GenShen: Dirty cards for objects that get promoted by safepoint | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8367646 | [GenShen] Control thread may overwrite gc cancellation cause set by mutator | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8368501 | Shenandoah: GC progress evaluation does not use generation | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8264851 | Shenandoah: Rework control loop mechanics to use timed waits | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8368499 | GenShen: Do not collect age census during evac when adaptive tenuring is disabled | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8368152 | Shenandoah: Incorrect behavior at end of degenerated cycle | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8365792 | GenShen: assertion "Generations aren't reconciled" | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8367473 | Shenandoah: Make the detailed evacuation metrics a runtime diagnostic option | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8367450 | Shenandoah: Log the composition of the collection set | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8367451 | GenShen: Remove the option to compute age census during evacuation | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8367378 | GenShen: Missing timing stats when old mark buffers are flushed during final update refs | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8365956 | GenShen: Adaptive tenuring threshold algorithm may raise threshold prematurely | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8365622 | Shenandoah: Fix Shenandoah simple bit map test | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8365571 | GenShen: PLAB promotions may remain disabled for evacuation threads | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8365572 | Shenandoah: Remove unused thread local _paced_time field | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8361726 | Shenandoah: More detailed evacuation instrumentation | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8360288 | Shenandoah crash at size_given_klass in op_degenerated | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8357550 | GenShen crashes during freeze: assert(!chunk->requires_barriers()) failed | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8359394 | GC cause cleanup | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8357976 | GenShen crash in swap_card_tables: Should be clean | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8358102 | GenShen: Age tables could be seeded with cumulative values | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8354078 | Implement JEP 521: Generational Shenandoah | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8355372 | GenShen: Test gc/shenandoah/generational/TestOldGrowthTriggers.java fails | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8355789 | GenShen: assert(_degen_point == ShenandoahGC::_degenerated_unset) failed | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8353596 | GenShen: Test TestClone.java#generational-no-coops intermittent timed out | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8354452 | Shenandoah: Enforce range checks on parameters controlling heuristic sleep times | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8353218 | Shenandoah: Out of date comment references Brooks pointers | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8352918 | Shenandoah: Verifier does not deactivate barriers as intended | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8348400 | GenShen: assert(ShenandoahHeap::heap()->is_full_gc_in_progress() || ...) failed | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8352299 | GenShen: Young cycles that interrupt old cycles cannot be cancelled | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8352091 | GenShen: assert(!(request.generation->is_old() && ...)) failed | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8350898 | Shenandoah: Eliminate final roots safepoint | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8351464 | Shenandoah: Hang on ShenandoahController::handle_alloc_failure | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8350905 | Shenandoah: Releasing a WeakHandle's referent may extend its lifetime | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8351444 | Shenandoah: Class Unloading may encounter recycled oops | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8350605 | assert(!heap->is_uncommit_in_progress()) failed | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8349094 | GenShen: Race between control and regulator threads may violate assertions | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8348092 | Shenandoah: assert(nk >= _lowest_valid_narrow_klass_id ...) failed | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8348268 | Test gc/shenandoah/TestResizeTLAB.java#compact: fatal error | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8349002 | GenShen: Deadlock during shutdown | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8348420 | Shenandoah: Check is_reserved before using ReservedSpace instances | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8345750 | Shenandoah: Test TestJcmdHeapDump.java#aggressive intermittent assert | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8347617 | Shenandoah: Use consistent name for update references phase | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8344049 | Shenandoah: Eliminate init-update-refs safepoint | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8347620 | Shenandoah: Use 'free' tag for free set related logging | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8346737 | GenShen: Generational memory pools should not report zero for maximum capacity | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8346688 | GenShen: Missing metadata trigger log message | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8346690 | Shenandoah: Fix log message for end of GC usage report | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8346051 | MemoryTest fails when Shenandoah's generational mode is enabled | [PR](https://github.com/openjdk/jdk/pull/XXXX) |
| 8345970 | pthread_getcpuclockid related crashes in shenandoah tests | [PR](https://github.com/openjdk/jdk/pull/XXXX) |

> **JBS Link**: https://bugs.openjdk.org/browse/JDK-[Issue Number]

## Key Contributions

### 1. JEP 521: Generational Shenandoah (JDK-8354078)

The flagship contribution for JDK 26 - implementing generational garbage collection for Shenandoah.

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

## Development Style

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

## Related Links

- [OpenJDK Profile](https://openjdk.org/people/wkemper)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=wkemper)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20wkemper)
- [JEP 521: Generational Shenandoah](https://openjdk.org/jeps/521)