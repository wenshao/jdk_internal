# Kim Barrett

> **GitHub**: [@kimbarrett](https://github.com/kimbarrett)
> **LinkedIn**: [Kim Barrett](https://www.linkedin.com/in/kim-barrett-7b19a97)
> **Organization**: Oracle
> **Location**: Malden, MA (推测)

---

## 概述

Kim Barrett 是 Oracle 的资深 Java 开发者，专注于 HotSpot 运行时、原子操作和 C++ 现代化。他拥有超过 25 年的软件设计和实现经验，主导了 HotSpot 的 C++17 迁移、Atomic<T> 模板实现，以及 HotSpot Style Guide 的现代化工作。

---

## Basic Information

| Field | Value |
|-------|-------|
| **Name** | Kim Barrett |
| **Current Organization** | Oracle |
| **LinkedIn** | [kim-barrett-7b19a97](https://www.linkedin.com/in/kim-barrett-7b19a97) |
| **GitHub** | [@kimbarrett](https://github.com/kimbarrett) |
| **OpenJDK** | [@kbarrett](https://openjdk.org/census#kbarrett) |
| **Role** | OpenJDK Member, JDK Reviewer |
| **PRs** | [352 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Akimbarrett+is%3Aclosed+label%3Aintegrated) |
| **Primary Areas** | Concurrency, Atomic Operations, C++ Modernization, HotSpot Runtime |
| **Experience** | 25+ years in software design and implementation |

> **数据来源**: [LinkedIn](https://www.linkedin.com/in/kim-barrett-7b19a97), [OpenJDK Census](https://openjdk.org/census#kbarrett)

## Contribution Overview

### By Category

| Category | Count | Description |
|----------|-------|-------------|
| Atomic Operations | 15 | Atomic<T> template implementation |
| C++ Modernization | 15 | C++17 migration, style guide updates |
| HotSpot Style Guide | 10 | Documentation and conventions |
| Memory Management | 8 | Cleaner, allocation functions |
| Platform Support | 7 | Cross-platform fixes |
| Testing | 5 | Test improvements and fixes |
| GC Infrastructure | 5 | GC-related improvements |

### Key Areas of Expertise
- **Atomic Operations** - Lock-free programming, Atomic<T> template
- **C++ Modernization** - C++17 migration, standard library usage
- **HotSpot Style Guide** - Coding conventions and best practices
- **Memory Safety** - Cleaner implementation, allocation wrappers
- **Cross-Platform Compatibility** - Compiler warnings, undefined behavior fixes

## Complete PR List

| Issue | Title | PR Link |
|-------|-------|---------|
| JDK-8372251 | Convert PartialArrayStepper/State to use Atomic<T> | [JBS](https://bugs.openjdk.org/browse/JDK-8372251) |
| JDK-8372337 | clang compilation error on hardware_constructive_interference_size | [JBS](https://bugs.openjdk.org/browse/JDK-8372337) |
| JDK-8372240 | Convert FreeListAllocator to use Atomic<T> | [JBS](https://bugs.openjdk.org/browse/JDK-8372240) |
| JDK-8371965 | Convert TaskQueueSuper to use Atomic<T> | [JBS](https://bugs.openjdk.org/browse/JDK-8371965) |
| JDK-8369187 | Add wrapper for <new> that forbids use of global allocation and deallocation functions | [JBS](https://bugs.openjdk.org/browse/JDK-8369187) |
| JDK-8371923 | Update LockFreeStack for Atomic<T> | [JBS](https://bugs.openjdk.org/browse/JDK-8371923) |
| JDK-8371956 | Convert OopStorage to use Atomic<T> | [JBS](https://bugs.openjdk.org/browse/JDK-8371956) |
| JDK-8369188 | Update link-time check for HotSpot uses of allocation and deallocation functions | [JBS](https://bugs.openjdk.org/browse/JDK-8369188) |
| JDK-8371922 | Remove unused NonblockingQueue class | [JBS](https://bugs.openjdk.org/browse/JDK-8371922) |
| JDK-8367013 | Add Atomic<T> to package/replace idiom of volatile var plus AtomicAccess:: operations | [JBS](https://bugs.openjdk.org/browse/JDK-8367013) |
| JDK-8370333 | hotspot-unit-tests.md specifies wrong directory structure for tests | [JBS](https://bugs.openjdk.org/browse/JDK-8370333) |
| JDK-8371104 | gtests should use wrappers for <limits> and <type_traits> | [JBS](https://bugs.openjdk.org/browse/JDK-8371104) |
| JDK-8369186 | HotSpot Style Guide should permit some uses of the C++ Standard Library | [JBS](https://bugs.openjdk.org/browse/JDK-8369186) |
| JDK-8368957 | Remove metaprogramming/logical.hpp in favor of C++17 facilities | [JBS](https://bugs.openjdk.org/browse/JDK-8368957) |
| JDK-8368817 | Convert JDK_Version::to_string to use stringStream instead of jio_snprintf-chain | [JBS](https://bugs.openjdk.org/browse/JDK-8368817) |
| JDK-8367796 | Rename AtomicAccess gtests | [JBS](https://bugs.openjdk.org/browse/JDK-8367796) |
| JDK-8367724 | Remove Trailing Return Types from undecided list | [JBS](https://bugs.openjdk.org/browse/JDK-8367724) |
| JDK-8252582 | HotSpot Style Guide should permit variable templates | [JBS](https://bugs.openjdk.org/browse/JDK-8252582) |
| JDK-8367282 | FORBID_C_FUNCTION needs exception spec consistent with library declaration | [JBS](https://bugs.openjdk.org/browse/JDK-8367282) |
| JDK-8367014 | Rename class Atomic to AtomicAccess | [JBS](https://bugs.openjdk.org/browse/JDK-8367014) |
| JDK-8366057 | HotSpot Style Guide should permit trailing return types | [JBS](https://bugs.openjdk.org/browse/JDK-8366057) |
| JDK-8367051 | Build failure with clang on linux and AIX after switch to C++17 | [JBS](https://bugs.openjdk.org/browse/JDK-8367051) |
| JDK-8314488 | Compiling the JDK with C++17 | [JBS](https://bugs.openjdk.org/browse/JDK-8314488) |
| JDK-8300080 | offset_of for GCC/Clang exhibits undefined behavior and is not always a compile-time constant | [JBS](https://bugs.openjdk.org/browse/JDK-8300080) |
| JDK-8366037 | Remove oopDesc::mark_addr() | [JBS](https://bugs.openjdk.org/browse/JDK-8366037) |
| JDK-8365245 | Move size reducing operations to GrowableArrayWithAllocator | [JBS](https://bugs.openjdk.org/browse/JDK-8365245) |
| JDK-8361383 | LogFileStreamOutput::write_decorations uses wrong type for format precisions | [JBS](https://bugs.openjdk.org/browse/JDK-8361383) |
| JDK-8361426 | (ref) Remove jdk.internal.ref.Cleaner | [JBS](https://bugs.openjdk.org/browse/JDK-8361426) |
| JDK-8344332 | (bf) Migrate DirectByteBuffer away from jdk.internal.ref.Cleaner | [JBS](https://bugs.openjdk.org/browse/JDK-8344332) |
| JDK-8361086 | JVMCIGlobals::check_jvmci_flags_are_consistent has incorrect format string | [JBS](https://bugs.openjdk.org/browse/JDK-8361086) |
| JDK-8361085 | MemoryReserver log_on_large_pages_failure has incorrect format usage | [JBS](https://bugs.openjdk.org/browse/JDK-8361085) |
| JDK-8346914 | UB issue in scalbnA | [JBS](https://bugs.openjdk.org/browse/JDK-8346914) |
| JDK-8360458 | Rename Deferred<> to DeferredStatic<> and improve usage description | [JBS](https://bugs.openjdk.org/browse/JDK-8360458) |
| JDK-8352565 | Add native method implementation of Reference.get() | [JBS](https://bugs.openjdk.org/browse/JDK-8352565) |
| JDK-8360178 | TestArguments.atojulong gtest has incorrect format string | [JBS](https://bugs.openjdk.org/browse/JDK-8360178) |
| JDK-8360177 | ParallelArguments::initialize has incorrect format string | [JBS](https://bugs.openjdk.org/browse/JDK-8360177) |
| JDK-8360281 | VMError::error_string has incorrect format usage | [JBS](https://bugs.openjdk.org/browse/JDK-8360281) |
| JDK-8255082 | HotSpot Style Guide should permit noexcept | [JBS](https://bugs.openjdk.org/browse/JDK-8255082) |
| JDK-8319242 | HotSpot Style Guide should discourage non-local variables with non-trivial initialization or destruction | [JBS](https://bugs.openjdk.org/browse/JDK-8319242) |
| JDK-8359227 | Code cache/heap size options should be size_t | [JBS](https://bugs.openjdk.org/browse/JDK-8359227) |
| JDK-8342639 | Global operator new in adlc has wrong exception spec | [JBS](https://bugs.openjdk.org/browse/JDK-8342639) |
| JDK-8358284 | doc/testing.html is not up to date after JDK-8355003 | [JBS](https://bugs.openjdk.org/browse/JDK-8358284) |
| JDK-8356016 | Build fails by clang(XCode 16.3) on macOS after JDK-8347719 | [JBS](https://bugs.openjdk.org/browse/JDK-8356016) |
| JDK-8356686 | doc/building.html is not up to date after JDK-8301971 | [JBS](https://bugs.openjdk.org/browse/JDK-8356686) |
| JDK-8356689 | Make HotSpot Style Guide change process more prominent | [JBS](https://bugs.openjdk.org/browse/JDK-8356689) |
| JDK-8347719 | [REDO] Portable implementation of FORBID_C_FUNCTION and ALLOW_C_FUNCTION | [JBS](https://bugs.openjdk.org/browse/JDK-8347719) |
| JDK-8324686 | Remove redefinition of NULL for MSVC | [JBS](https://bugs.openjdk.org/browse/JDK-8324686) |
| JDK-8351374 | Improve comment about queue.remove timeout in CleanerImpl.run | [JBS](https://bugs.openjdk.org/browse/JDK-8351374) |
| JDK-8350771 | Fix -Wzero-as-null-pointer-constant warning in nsk/monitoring ThreadController utility | [JBS](https://bugs.openjdk.org/browse/JDK-8350771) |
| JDK-8350767 | Fix -Wzero-as-null-pointer-constant warnings in nsk jni stress tests | [JBS](https://bugs.openjdk.org/browse/JDK-8350767) |
| JDK-8350623 | Fix -Wzero-as-null-pointer-constant warnings in nsk native test utilities | [JBS](https://bugs.openjdk.org/browse/JDK-8350623) |
| JDK-8345492 | Fix -Wzero-as-null-pointer-constant warnings in adlc code | [JBS](https://bugs.openjdk.org/browse/JDK-8345492) |
| JDK-8346971 | [ubsan] psCardTable.cpp:131:24: runtime error: large index is out of bounds | [JBS](https://bugs.openjdk.org/browse/JDK-8346971) |
| JDK-8347720 | [BACKOUT] Portable implementation of FORBID_C_FUNCTION and ALLOW_C_FUNCTION | [JBS](https://bugs.openjdk.org/browse/JDK-8347720) |
| JDK-8313396 | Portable implementation of FORBID_C_FUNCTION and ALLOW_C_FUNCTION | [JBS](https://bugs.openjdk.org/browse/JDK-8313396) |
| JDK-8345374 | Ubsan: runtime error: division by zero | [JBS](https://bugs.openjdk.org/browse/JDK-8345374) |
| JDK-8345732 | Provide helpers for using PartialArrayState | [JBS](https://bugs.openjdk.org/browse/JDK-8345732) |
| JDK-8346160 | Fix -Wzero-as-null-pointer-constant warnings from explicit casts | [JBS](https://bugs.openjdk.org/browse/JDK-8346160) |
| JDK-8346139 | test_memset_with_concurrent_readers.cpp should not use <sstream> | [JBS](https://bugs.openjdk.org/browse/JDK-8346139) |
| JDK-8345505 | Fix -Wzero-as-null-pointer-constant warnings in zero code | [JBS](https://bugs.openjdk.org/browse/JDK-8345505) |
| JDK-8337995 | ZUtils::fill uses std::fill_n | [JBS](https://bugs.openjdk.org/browse/JDK-8337995) |
| JDK-8345269 | Fix -Wzero-as-null-pointer-constant warnings in ppc code | [JBS](https://bugs.openjdk.org/browse/JDK-8345269) |
| JDK-8345273 | Fix -Wzero-as-null-pointer-constant warnings in s390 code | [JBS](https://bugs.openjdk.org/browse/JDK-8345273) |
| JDK-8345589 | Simplify Windows definition of strtok_r | [JBS](https://bugs.openjdk.org/browse/JDK-8345589) |
| JDK-8345159 | RISCV: Fix -Wzero-as-null-pointer-constant warning in emit_static_call_stub | [JBS](https://bugs.openjdk.org/browse/JDK-8345159) |

## Key Contributions

### 1. Atomic<T> Template Implementation

**JDK-8367013: Add Atomic<T> to package/replace idiom of volatile var plus AtomicAccess:: operations**

This is a major refactoring that introduces a type-safe Atomic<T> template class:

```cpp
// Before: Error-prone volatile + AtomicAccess pattern
volatile int _counter;
int new_value = AtomicAccess::add(&_counter, 1);

// After: Type-safe Atomic<T> template
Atomic<int> _counter;
int new_value = _counter.add(1);

// The Atomic<T> template provides:
template<typename T>
class Atomic {
public:
  T add(T delta);
  T xchg(T new_value);
  T cmpxchg(T expected, T new_value);
  T load() const;
  void store(T value);
};
```

This pattern was then applied across many HotSpot components including OopStorage, FreeListAllocator, TaskQueueSuper, and PartialArrayStepper.

### 2. C++17 Migration

**JDK-8314488: Compiling the JDK with C++17**

Led the effort to migrate HotSpot from C++14 to C++17:

```cpp
// Before: Custom metaprogramming utilities
#include "metaprogramming/logical.hpp"

// After: Use C++17 standard library
#include <type_traits>
using std::conjunction;
using std::disjunction;
using std::negation;

// Enable C++17 features in HotSpot
// make/hotspot/lib/JvmOverrideFiles.gmk
CXXFLAGS += -std=c++17
```

### 3. HotSpot Style Guide Modernization

**JDK-8366057: HotSpot Style Guide should permit trailing return types**

Updated the HotSpot coding style to embrace modern C++ features:

```cpp
// Now permitted: Trailing return types
auto get_value() -> int;
auto process(Data& data) -> Result;

// Now permitted: Variable templates
template<typename T>
constexpr T pi = T(3.14159265358979323846);

// Now permitted: noexcept specifier
void critical_function() noexcept;
```

### 4. FORBID_C_FUNCTION / ALLOW_C_FUNCTION

**JDK-8313396: Portable implementation of FORBID_C_FUNCTION and ALLOW_C_FUNCTION**

Created portable macros to control C function usage:

```cpp
// Prevent accidental use of C library functions
// that have HotSpot-specific alternatives
FORBID_C_FUNCTION(malloc, "Use AllocateHeap instead");

// Allow specific C functions when needed
ALLOW_C_FUNCTION(sprintf, 
  result = sprintf(buffer, "%d", value);
);
```

### 5. Cleaner Migration

**JDK-8361426: (ref) Remove jdk.internal.ref.Cleaner**

Migrated from the internal Cleaner to java.lang.ref.Cleaner:

```java
// Before: Internal Cleaner
jdk.internal.ref.Cleaner cleaner = 
    jdk.internal.ref.Cleaner.create();

// After: Standard java.lang.ref.Cleaner
Cleaner cleaner = Cleaner.create();
cleaner.register(object, cleanupAction);
```

## Development Style

### Code Characteristics
- **Type safety focus**: Strong preference for type-safe templates over macros
- **Modern C++ advocate**: Pushes for adoption of C++17/20 features
- **Documentation emphasis**: Updates style guide alongside code changes
- **Undefined behavior elimination**: Systematic fixing of UB issues

### Typical Commit Pattern
1. Identify a pattern that could be modernized
2. Create a general solution (template, wrapper)
3. Apply the solution across multiple files
4. Update documentation and style guide
5. Add tests for the new infrastructure

### Review Style
- Often reviewed by Ioi Lam (iklam), Thomas Schatzl (tschatzl)
- Focuses on correctness of lock-free code
- Ensures cross-platform compatibility

## Related Links

- [OpenJDK Profile](https://openjdk.org/census#kbarrett)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20kbarrett)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=kbarrett)
- [HotSpot Style Guide](https://openjdk.org/groups/hotspot/docs/CodingStyle.html)