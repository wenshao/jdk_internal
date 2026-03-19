# JDK 26 Top 50 Most Impactful Commits

> Generated: 2026-03-19
> Selection criteria: Code changes (additions + deletions)

---

## JEP Implementations

These commits implement major JEPs and have the highest impact on JDK 26.

### 1. JDK-8349910: HTTP/3 for the HTTP Client (JEP 517)

| Metric | Value |
|--------|-------|
| Additions | 104,307 |
| Deletions | 2,639 |
| Author | Daniel Fuchs |
| Impact | ⭐⭐⭐⭐⭐ |

**Summary**: Full HTTP/3 and QUIC implementation for the Java HTTP Client.

**Key Changes**:
- New QUIC protocol implementation
- HTTP/3 frame handling
- QPACK header compression
- Connection management for HTTP/3

**Analysis Status**: [JBS Issue →](https://bugs.openjdk.org/browse/JDK-8349910)

---

### 2. JDK-8342382: G1 GC Throughput Improvements (JEP 522)

| Metric | Value |
|--------|-------|
| Additions | 3,572 |
| Deletions | 4,628 |
| Author | Thomas Schatzl |
| Impact | ⭐⭐⭐⭐⭐ |

**Summary**: Reduce synchronization overhead in G1 to improve throughput.

**Key Changes**:
- Reduced synchronization in marking
- Improved reference processing
- Better NUMA awareness

**Analysis Status**: [JBS Issue →](https://bugs.openjdk.org/browse/JDK-8342382)

---

### 3. JDK-8365932: Ahead-of-Time Object Caching (JEP 516)

| Metric | Value |
|--------|-------|
| Additions | 5,269 |
| Deletions | 1,645 |
| Author | Erik Österlund |
| Impact | ⭐⭐⭐⭐⭐ |

**Summary**: AOT caching for faster startup.

**Key Changes**:
- AOT cache infrastructure
- Class metadata caching
- Heap object caching

**Analysis Status**: [JBS Issue →](https://bugs.openjdk.org/browse/JDK-8365932)

---

### 4. JDK-8366178: Lazy Constants (JEP 526)

| Metric | Value |
|--------|-------|
| Additions | 2,784 |
| Deletions | 3,536 |
| Author | Per Minborg |
| Impact | ⭐⭐⭐⭐⭐ |

**Summary**: Second preview of lazy constant initialization.

**Analysis Status**: [JBS Issue →](https://bugs.openjdk.org/browse/JDK-8366178)

---

### 5. JDK-8353835: Prepare to Make Final Mean Final (JEP 500)

| Metric | Value |
|--------|-------|
| Additions | 5,310 |
| Deletions | 195 |
| Author | Alan Bateman |
| Impact | ⭐⭐⭐⭐⭐ |

**Summary**: Prepare for stricter final field semantics.

**Analysis Status**: [JBS Issue →](https://bugs.openjdk.org/browse/JDK-8353835)

---

### 6. JDK-8359053: Remove the Applet API (JEP 504)

| Metric | Value |
|--------|-------|
| Additions | 295 |
| Deletions | 3,137 |
| Author | Phil Race |
| Impact | ⭐⭐⭐⭐ |

**Summary**: Remove deprecated Applet API.

**Analysis Status**: [JBS Issue →](https://bugs.openjdk.org/browse/JDK-8359053)

---

## Major Library Updates

### 7. JDK-8354548: Update CLDR to Version 48.0

| Metric | Value |
|--------|-------|
| Additions | 120,372 |
| Deletions | 41,544 |
| Author | Naoto Sato |
| Impact | ⭐⭐⭐⭐⭐ |

**Summary**: Localization data update with new locales and data fixes.

---

### 8. JDK-8375057: Update HarfBuzz to 12.3.2

| Metric | Value |
|--------|-------|
| Additions | 11,830 |
| Deletions | 9,727 |
| Author | Damon Nguyen |
| Impact | ⭐⭐⭐⭐ |

**Summary**: Text shaping library update.

---

### 9. JDK-8373290: Update FreeType to 2.14.1

| Metric | Value |
|--------|-------|
| Additions | 7,332 |
| Deletions | 4,950 |
| Author | Jayathirth D V |
| Impact | ⭐⭐⭐⭐ |

**Summary**: Font rendering library update.

---

### 10. JDK-8346944: Update Unicode to 17.0.0

| Metric | Value |
|--------|-------|
| Additions | 2,327 |
| Deletions | 1,632 |
| Author | Naoto Sato |
| Impact | ⭐⭐⭐⭐ |

**Summary**: Unicode 17.0.0 support.

---

## Compiler & Vector API

### 11. JDK-8376186: VectorAPI Nomenclature Change

| Metric | Value |
|--------|-------|
| Additions | 17,809 |
| Deletions | 17,810 |
| Author | Jatin Bhateja |
| Impact | ⭐⭐⭐⭐ |

**Summary**: Rename vector classes for consistency.

---

### 12. JDK-8344942: Template-Based Testing Framework

| Metric | Value |
|--------|-------|
| Additions | 6,722 |
| Deletions | 0 |
| Author | Emanuel Peter |
| Impact | ⭐⭐⭐⭐⭐ |

**Summary**: New template-based testing framework for C2 compiler.

---

### 13. JDK-8324751: C2 SuperWord Aliasing Analysis

| Metric | Value |
|--------|-------|
| Additions | 5,810 |
| Deletions | 249 |
| Author | Emanuel Peter |
| Impact | ⭐⭐⭐⭐⭐ |

**Summary**: Runtime aliasing checks for better vectorization.

---

### 14. JDK-8351159: 32-bit x86 Removal Cleanup

| Metric | Value |
|--------|-------|
| Additions | 16,353 |
| Deletions | 17,326 |
| Author | Anton Seoane Ampudia |
| Impact | ⭐⭐⭐⭐ |

**Summary**: Remove 32-bit x86 support remnants.

---

## Garbage Collection

### 15. JDK-8338977: Parallel GC Heap Resizing

| Metric | Value |
|--------|-------|
| Additions | 892 |
| Deletions | 3,855 |
| Author | Albert Mingkun Yang |
| Impact | ⭐⭐⭐⭐ |

**Summary**: Improved heap resizing heuristics for Parallel GC.

---

### 16. JDK-8365880: Shenandoah Memory Accounting

| Metric | Value |
|--------|-------|
| Additions | 2,455 |
| Deletions | 1,351 |
| Author | Kelvin Nilsen |
| Impact | ⭐⭐⭐⭐ |

**Summary**: Unified memory usage accounting in Shenandoah.

---

## Build & Packaging

### 17. JDK-8333727: jpackage JOpt Command Line

| Metric | Value |
|--------|-------|
| Additions | 18,471 |
| Deletions | 6,636 |
| Author | Alexey Semenyuk |
| Impact | ⭐⭐⭐⭐⭐ |

**Summary**: Improve jpackage command line parsing.

---

### 18. JDK-8374219: jpackage Executor Fixes

| Metric | Value |
|--------|-------|
| Additions | 8,888 |
| Deletions | 1,907 |
| Author | Alexey Semenyuk |
| Impact | ⭐⭐⭐⭐ |

**Summary**: Fix issues in jpackage's Executor class.

---

## Test Migration

### 19. JDK-8373830: java/time Tests JUnit Migration

| Metric | Value |
|--------|-------|
| Additions | 13,033 |
| Deletions | 11,460 |
| Author | Justin Lu |
| Impact | ⭐⭐⭐ |

**Summary**: Migrate java/time tests from TestNG to JUnit.

---

### 20. JDK-8378344: HTTP Client Tests JUnit Migration

| Metric | Value |
|--------|-------|
| Additions | 2,814 |
| Deletions | 2,627 |
| Author | Daniel Fuchs |
| Impact | ⭐⭐⭐ |

**Summary**: Migrate HTTP client tests from TestNG to JUnit.

---

## Complete Top 50 List

| Rank | Issue | Description | +/- | Author |
|------|-------|-------------|-----|--------|
| 1 | 8354548 | Update CLDR to 48.0 | 161,916 | Naoto Sato |
| 2 | 8349910 | HTTP/3 (JEP 517) | 106,946 | Daniel Fuchs |
| 3 | 8376186 | VectorAPI nomenclature | 35,619 | Jatin Bhateja |
| 4 | 8351159 | 32-bit x86 cleanup | 33,679 | Anton Seoane Ampudia |
| 5 | 8333727 | jpackage JOpt | 25,107 | Alexey Semenyuk |
| 6 | 8373830 | java/time JUnit | 24,493 | Justin Lu |
| 7 | 8375057 | HarfBuzz 12.3.2 | 21,557 | Damon Nguyen |
| 8 | 8372978 | VectorAPI UMIN/UMAX | 16,747 | Eric Fang |
| 9 | 8377447 | VectorAPI float16 | 16,323 | Jatin Bhateja |
| 10 | 8373290 | FreeType 2.14.1 | 12,282 | Jayathirth D V |
| 11 | 8374219 | jpackage Executor | 10,795 | Alexey Semenyuk |
| 12 | 8373935 | java/lang/invoke JUnit | 10,747 | Chen Liang |
| 13 | 8371446 | VectorAPI mask tests | 10,380 | Xueming Shen |
| 14 | 8378758 | VectorAPI scalar wrappers | 10,325 | Jatin Bhateja |
| 15 | 8342382 | G1 throughput (JEP 522) | 8,200 | Thomas Schatzl |
| 16 | 8365932 | AOT caching (JEP 516) | 6,914 | Erik Österlund |
| 17 | 8344942 | Template testing | 6,722 | Emanuel Peter |
| 18 | 8366178 | Lazy constants (JEP 526) | 6,320 | Per Minborg |
| 19 | 8324751 | SuperWord aliasing | 6,059 | Emanuel Peter |
| 20 | 8360707 | Enumerate blobs/stubs | 5,992 | Andrew Dinn |
| 21 | 8353835 | Final mean final (JEP 500) | 5,505 | Alan Bateman |
| 22 | 8354348 | EVEX/REX demotion | 5,483 | Srinivas Vamsi Parasa |
| 23 | 8378344 | HTTP client JUnit | 5,441 | Daniel Fuchs |
| 24 | 8367014 | Atomic to AtomicAccess | 5,106 | Kim Barrett |
| 25 | 8367531 | Template framework | 4,979 | Emanuel Peter |
| 26 | 8338977 | Parallel GC resizing | 4,747 | Albert Mingkun Yang |
| 27 | 8376038 | java/sql JUnit | 4,648 | Justin Lu |
| 28 | 8357551 | RISC-V vectorization | 4,093 | Hamlin Li |
| 29 | 8346944 | Unicode 17.0.0 | 3,959 | Naoto Sato |
| 30 | 8368030 | Package bundlers stateless | 3,912 | Alexey Semenyuk |
| 31 | 8365880 | Shenandoah accounting | 3,806 | Kelvin Nilsen |
| 32 | 8366017 | FloatingDecimal fast paths | 3,788 | Raffaello Giulietti |
| 33 | 8379626 | jaxp JUnit | 3,734 | David Beaumont |
| 34 | 8353738 | TLS test cleanup | 3,603 | Matthew Donovan |
| 35 | 8336695 | BCEL 6.10.0 | 3,589 | Joe Wang |
| 36 | 8376187 | VectorAPI lane types | 3,508 | Jatin Bhateja |
| 37 | 8359053 | Remove Applet API (JEP 504) | 3,432 | Phil Race |
| 38 | 8325467 | C2 many arguments | 3,165 | Daniel Lundén |
| 39 | 8358768 | VectorAPI SUADD associative | 3,159 | Ian Graves |
| 40 | 8369238 | Virtual thread preemption | 2,693 | Patricio Chilano Mateo |
| 41 | 8362279 | VectorAPI SUADD reduction | 2,171 | Ian Graves |
| 42 | 8370774 | Merge ModRefBarrierSet | 2,131 | Albert Mingkun Yang |
| 43 | 8357471 | GenShen reserves | 1,956 | Kelvin Nilsen |
| 44 | 8362566 | AOT map logging | 1,776 | Ioi Lam |
| 45 | 8342692 | C2 long counted loop | 1,744 | Roland Westrelin |
| 46 | 8260555 | Timeout factor change | 1,660 | Leo Korinth |
| 47 | 8316694 | CodeCache relocation | 1,655 | Chad Rakoczy |
| 48 | 8373595 | ObjectMonitorTable | 1,447 | Fredrik Bredberg |
| 49 | 8365190 | Remove LockingMode code | 1,409 | Fredrik Bredberg |
| 50 | 8374549 | MetaspaceClosure extend | 1,373 | Ioi Lam |

---

## Analysis Priority

### Priority 1: JEP Implementations

These require detailed analysis due to their broad impact:
1. JDK-8349910 (HTTP/3)
2. JDK-8342382 (G1 throughput)
3. JDK-8365932 (AOT caching)
4. JDK-8366178 (Lazy constants)
5. JDK-8353835 (Final semantics)

### Priority 2: Compiler Optimizations

Important for performance:
1. JDK-8324751 (SuperWord aliasing)
2. JDK-8344942 (Template testing)
3. JDK-8357551 (RISC-V vectorization)

### Priority 3: Infrastructure

Build and test improvements:
1. JDK-8333727 (jpackage)
2. JDK-8351159 (x86 cleanup)

---

*For complete commit list, see [jdk26-commits.md](./jdk26-commits.md)*
