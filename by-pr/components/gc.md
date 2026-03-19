# JDK 26 GC Component Summary

> Commits: 745 (18.9% of total)
> Key Contributors: Thomas Schatzl, Albert Mingkun Yang, Aleksey Shipilev, Kelvin Nilsen

---

## Overview

JDK 26 brings significant improvements across all garbage collectors, with a focus on throughput optimization, memory efficiency, and the introduction of Generational Shenandoah.

---

## JEPs

### JEP 521: Generational Shenandoah

The most significant GC change in JDK 26 is the introduction of **Generational Shenandoah** (GenShen), which separates young and old generations to improve pause times and throughput.

**Key Benefits**:
- Reduced pause times for young generation collections
- Better memory utilization
- Improved throughput for allocation-heavy workloads

**Related Issues**: 8357471, 8312116, 8358735, 8369068, 8377396

### JEP 522: G1 GC Throughput Improvements

Reduces synchronization overhead in G1 to improve throughput on multi-core systems.

**Key Changes**:
- Reduced synchronization in marking
- Improved reference processing
- Better NUMA awareness

**Related Issue**: 8342382

---

## GC-Specific Changes

### G1 (Garbage First)

| Issue | Description | Impact |
|-------|-------------|--------|
| 8342382 | Throughput improvements (JEP 522) | ⭐⭐⭐⭐⭐ |
| 8238687 | Memory uncommit during young collections | ⭐⭐⭐⭐ |
| 8373945 | Use WB.fullGC() for class unloading | ⭐⭐⭐ |

**Top Contributors**: Thomas Schatzl (140 commits)

### Shenandoah

| Issue | Description | Impact |
|-------|-------------|--------|
| 8357471 | GenShen: Share collector reserves | ⭐⭐⭐⭐ |
| 8312116 | GenShen: Allocation rate triggers | ⭐⭐⭐⭐ |
| 8358735 | GenShen: block_start() fix | ⭐⭐⭐ |
| 8369068 | GenShen: Generation reconciliation | ⭐⭐⭐ |
| 8377396 | GenShen: Region promotions | ⭐⭐⭐ |
| 8350050 | Disable allocation pacing | ⭐⭐⭐ |
| 8365880 | Memory usage accounting | ⭐⭐⭐⭐ |
| 8375568 | Thread name abbreviation | ⭐⭐ |

**Top Contributors**: Aleksey Shipilev, Kelvin Nilsen, William Kemper

### ZGC

| Issue | Description | Impact |
|-------|-------------|--------|
| 8358586 | Combine allocator classes | ⭐⭐⭐ |
| 8356716 | Cleanup uncommit logic | ⭐⭐⭐⭐ |
| 8371701 | NUMA-affinity for threads | ⭐⭐⭐ |

**Top Contributors**: Axel Boldt-Christmas, Joel Sikström

### Parallel GC

| Issue | Description | Impact |
|-------|-------------|--------|
| 8338977 | Improve heap resizing heuristics | ⭐⭐⭐⭐⭐ |

**Top Contributors**: Albert Mingkun Yang

---

## Key Commits by Impact

| Issue | Description | +/- | Author |
|-------|-------------|-----|--------|
| 8342382 | G1 throughput (JEP 522) | 8,200 | Thomas Schatzl |
| 8338977 | Parallel heap resizing | 4,747 | Albert Mingkun Yang |
| 8365880 | Shenandoah accounting | 3,806 | Kelvin Nilsen |
| 8357471 | GenShen reserves | 1,956 | Kelvin Nilsen |
| 8362566 | AOT map logging | 1,776 | Ioi Lam |

---

## Memory Management

### Object Monitor Improvements

- **JDK-8373595**: New ObjectMonitorTable implementation
- **JDK-8365190**: Remove LockingMode related code
- **JDK-8367982**: Unify ObjectSynchronizer and LightweightSynchronizer

### Metaspace

- **JDK-8374549**: Extend MetaspaceClosure for non-MetaspaceObj types
- **JDK-8366475**: Rename MetaspaceShared to AOTMetaspace

---

## AOT & CDS Integration

Several commits integrate GC with AOT caching:

| Issue | Description |
|-------|-------------|
| 8362566 | Use -Xlog:aot+map for cache contents |
| 8365932 | AOT caching implementation (JEP 516) |
| 8373392 | Replace CDS subgraphs with @AOTSafeClassInitializer |

---

## Top 10 Contributors

| Rank | Contributor | Commits |
|------|-------------|---------|
| 1 | Thomas Schatzl | 140 |
| 2 | Albert Mingkun Yang | 136 |
| 3 | Aleksey Shipilev | 80 |
| 4 | Kim Barrett | 76 |
| 5 | Ioi Lam | 76 |
| 6 | Kelvin Nilsen | ~20 |
| 7 | William Kemper | ~15 |
| 8 | Axel Boldt-Christmas | 52 |
| 9 | Joel Sikström | 44 |
| 10 | Fredrik Bredberg | ~10 |

---

## Testing

Key testing improvements:
- G1 humongous object tests cleanup
- GenShen stress testing additions
- Memory uncommit test coverage

---

## Migration Notes

### For G1 Users
- JEP 522 improvements are automatic
- No configuration changes required
- Expect ~5-10% throughput improvement on multi-core systems

### For Shenandoah Users
- GenShen is available but may require `-XX:+UnlockExperimentalVMOptions`
- Review allocation pacing changes if using custom pacing
- Monitor generation reconciliation in logs

### For Parallel GC Users
- Heap resizing improvements are automatic
- May see reduced GC frequency with same heap size

---

*Last updated: 2026-03-19*
