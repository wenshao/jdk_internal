# Coleen Phillimore

> HotSpot VM 核心架构师，JVM 运行时专家

---

## Basic Information

| Field | Value |
|-------|-------|
| **Name** | Coleen Phillimore |
| **Current Organization** | Oracle |
| **GitHub** | [@coleenp](https://github.com/coleenp) |
| **OpenJDK** | [@coleenp](https://openjdk.org/census#coleenp) |
| **Role** | OpenJDK Member, JDK Reviewer |
| **PRs** | [400 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Acoleenp+is%3Aclosed+label%3Aintegrated) |
| **Primary Areas** | JVM Core, HotSpot, Metaspace, Class Loading |

> **Data as of**: 2026-03-19

---

## Technical Impact

| Metric | Value |
|--------|-------|
| **Lines of Code** | +158,019 / -148,467 (net +9,552) |
| **Affected Modules** | hotspot (runtime, classfile) |
| **Main Contributions** | JVM core, metaspace, class loading |

### Most Affected Directories

| Directory | Files | Description |
|-----------|-------|-------------|
| runtime | 951 | JVM runtime |
| classfile | 764 | Class file loading |
| oops | 672 | Object model |

---

## Technical Expertise

`HotSpot VM` `Metaspace` `Class Loading` `Object Monitor` `JVM TI` `Runtime`

---

## Representative Work

### 1. HotSpot VM Core Architect
Long-time HotSpot VM contributor and architect, shaping JVM internals.

### 2. Metaspace Improvements
Major contributions to metaspace memory management for class metadata.

### 3. Class Loading Modernization
Class file loading and verification improvements.

### 4. Object Monitor Optimization
Synchronization primitives and object monitor optimizations.

### 5. Code Cleanup and Modernization
Extensive code cleanup, removing deprecated code and modernizing codebase.

---

## External Resources

| Type | Link |
|------|------|
| **GitHub** | [@coleenp](https://github.com/coleenp) |
| **OpenJDK Census** | [coleenp](https://openjdk.org/census#coleenp) |

---

## Contribution Overview

### By Category

| Category | Count | Description |
|----------|-------|-------------|
| JVM Core | 25 | HotSpot VM internals |
| Metaspace | 15 | Memory management for classes |
| Class Loading | 10 | Class loading and verification |
| Code Cleanup | 10 | Removing deprecated code |
| Format Macros | 8 | SIZE_FORMAT replacement |

### Key Areas of Expertise
- **HotSpot VM** - JVM internals and runtime
- **Metaspace** - Class metadata storage
- **Class Loading** - Class file loading and verification
- **Object Monitor** - Synchronization primitives
- **JVM TI** - JVM Tool Interface

## Complete PR List

| Issue | Title | PR Link |
|-------|-------|---------|
| JDK-8371860 | Make non-public methods in java_lang_Class private | [Link]([需要补充 PR 链接]) |
| JDK-8364360 | Defining hidden class with no room in constant pool crashes the VM | [Link]([需要补充 PR 链接]) |
| JDK-8369622 | GlobalChunkPoolMutex is recursively locked during error handling | [Link]([需要补充 PR 链接]) |
| JDK-8361451 | Test vmTestbase/metaspace/stressHierarchy/stressHierarchy012 fails | [Link]([需要补充 PR 链接]) |
| JDK-8367989 | Remove InstanceKlass::allocate_objArray and ArrayKlass::allocate_arrayArray | [Link]([需要补充 PR 链接]) |
| JDK-8365823 | Revert storing abstract and interface Klasses to non-class metaspace | [Link]([需要补充 PR 链接]) |
| JDK-8367368 | Add message for verify_legal_class_modifiers for inner classes | [Link]([需要补充 PR 链接]) |
| JDK-8366908 | Use a different class for testing JDK-8351654 | [Link]([需要补充 PR 链接]) |
| JDK-8364750 | Remove unused declaration in jvm.h | [Link]([需要补充 PR 链接]) |
| JDK-8343218 | Add option to disable allocating interface and abstract classes in non-class metaspace | [Link]([需要补充 PR 链接]) |
| JDK-8364187 | Make getClassAccessFlagsRaw non-native | [Link]([需要补充 PR 链接]) |
| JDK-8363816 | Refactor array name creation | [Link]([需要补充 PR 链接]) |
| JDK-8359707 | Add classfile modification code to RedefineClassHelper | [Link]([需要补充 PR 链接]) |
| JDK-8295851 | Do not use ttyLock in BytecodeTracer::trace | [Link]([需要补充 PR 链接]) |
| JDK-8268406 | Deallocate jmethodID native memory | [Link]([需要补充 PR 链接]) |
| JDK-8359920 | Use names for frame types in stackmaps | [Link]([需要补充 PR 链接]) |
| JDK-8358326 | Use oopFactory array allocation | [Link]([需要补充 PR 链接]) |
| JDK-8358205 | Remove unused JFR array allocation code | [Link]([需要补充 PR 链接]) |
| JDK-8356173 | Remove ThreadCritical | [Link]([需要补充 PR 链接]) |
| JDK-8330022 | Failure test/hotspot/jtreg/vmTestbase/nsk/sysdict/share/BTreeTest.java | [Link]([需要补充 PR 链接]) |
| JDK-8356172 | IdealGraphPrinter doesn't need ThreadCritical | [Link]([需要补充 PR 链接]) |
| JDK-8355353 | File Leak in os::read_image_release_file | [Link]([需要补充 PR 链接]) |
| JDK-8355627 | Don't use ThreadCritical for EventLog list | [Link]([需要补充 PR 链接]) |
| JDK-8349405 | Redundant and confusing null checks on data from CP::resolved_klasses | [Link]([需要补充 PR 链接]) |
| JDK-8354448 | [REDO] Remove friends for ObjectMonitor | [Link]([需要补充 PR 链接]) |
| JDK-8354446 | [BACKOUT] Remove friends for ObjectMonitor | [Link]([需要补充 PR 链接]) |
| JDK-8354180 | Clean up uses of ObjectMonitor caches | [Link]([需要补充 PR 链接]) |
| JDK-8354234 | Remove friends for ObjectMonitor | [Link]([需要补充 PR 链接]) |
| JDK-8349007 | The jtreg test ResolvedMethodTableHash takes excessive time | [Link]([需要补充 PR 链接]) |
| JDK-8351654 | Agent transformer bytecodes should be verified | [Link]([需要补充 PR 链接]) |
| JDK-8353584 | [BACKOUT] DaCapo xalan performance with -XX:+UseObjectMonitorTable | [Link]([需要补充 PR 链接]) |
| JDK-8351673 | Clean up a case of if (LockingMode == LM_LIGHTWEIGHT) | [Link]([需要补充 PR 链接]) |
| JDK-8351046 | Rename ObjectMonitor functions | [Link]([需要补充 PR 链接]) |
| JDK-8351165 | Remove unused includes from vmStructs | [Link]([需要补充 PR 链接]) |
| JDK-8350974 | The os_cpu VM_STRUCTS, VM_TYPES, etc have no declarations | [Link]([需要补充 PR 链接]) |
| JDK-8315488 | Remove outdated and unused ciReplay support from SA | [Link]([需要补充 PR 链接]) |
| JDK-8328473 | StringTable and SymbolTable statistics delay time to safepoint | [Link]([需要补充 PR 链接]) |
| JDK-8349860 | Make Class.isArray(), Class.isInterface() and Class.isPrimitive() non-native | [Link]([需要补充 PR 链接]) |
| JDK-8349145 | Make Class.getProtectionDomain() non-native | [Link]([需要补充 PR 链接]) |
| JDK-8346567 | Make Class.getModifiers() non-native | [Link]([需要补充 PR 链接]) |
| JDK-8349559 | Compiler interface doesn't need to store protection domain | [Link]([需要补充 PR 链接]) |
| JDK-8334320 | Replace vmTestbase/metaspace/share/TriggerUnloadingWithWhiteBox.java | [Link]([需要补充 PR 链接]) |
| JDK-8337548 | Parallel class loading can pass is_superclass true for interfaces | [Link]([需要补充 PR 链接]) |
| JDK-8337458 | Remove debugging code print_cpool_bytes | [Link]([需要补充 PR 链接]) |
| JDK-8347990 | Remove SIZE_FORMAT macros and replace remaining uses | [Link]([需要补充 PR 链接]) |
| JDK-8347733 | Replace SIZE_FORMAT in runtime code | [Link]([需要补充 PR 链接]) |
| JDK-8347924 | Replace SIZE_FORMAT in memory and metaspace | [Link]([需要补充 PR 链接]) |
| JDK-8347609 | Replace SIZE_FORMAT in os/os_cpu/cpu directories | [Link]([需要补充 PR 链接]) |
| JDK-8347730 | Replace SIZE_FORMAT in g1 | [Link]([需要补充 PR 链接]) |
| JDK-8347731 | Replace SIZE_FORMAT in zgc | [Link]([需要补充 PR 链接]) |
| JDK-8347732 | Replace SIZE_FORMAT in shenandoah | [Link]([需要补充 PR 链接]) |
| JDK-8347431 | Update ObjectMonitor comments | [Link]([需要补充 PR 链接]) |
| JDK-8347727 | Replace SIZE_FORMAT in shared gc | [Link]([需要补充 PR 链接]) |
| JDK-8347729 | Replace SIZE_FORMAT in parallel and serial gc | [Link]([需要补充 PR 链接]) |
| JDK-8347721 | Replace SIZE_FORMAT in compiler directories | [Link]([需要补充 PR 链接]) |
| JDK-8347724 | Replace SIZE_FORMAT in jfr directory | [Link]([需要补充 PR 链接]) |
| JDK-8347566 | Replace SSIZE_FORMAT with 'z' length modifier | [Link]([需要补充 PR 链接]) |
| JDK-8346990 | Remove INTX_FORMAT and UINTX_FORMAT macros | [Link]([需要补充 PR 链接]) |
| JDK-8293123 | Fix various include file ordering | [Link]([需要补充 PR 链接]) |
| JDK-8346929 | runtime/ClassUnload/DictionaryDependsTest.java fails | [Link]([需要补充 PR 链接]) |
| JDK-8347147 | [REDO] AccessFlags can be u2 in metadata | [Link]([需要补充 PR 链接]) |
| JDK-8329549 | Remove FORMAT64_MODIFIER | [Link]([需要补充 PR 链接]) |
| JDK-8339113 | AccessFlags can be u2 in metadata | [Link]([需要补充 PR 链接]) |
| JDK-8337016 | serviceability/jvmti/RedefineClasses/RedefineLeakThrowable.java gets Metaspace OOM | [Link]([需要补充 PR 链接]) |
| JDK-8346304 | SA doesn't need a copy of getModifierFlags | [Link]([需要补充 PR 链接]) |
| JDK-8345678 | compute_modifiers should not be in create_mirror | [Link]([需要补充 PR 链接]) |
| JDK-8346040 | Zero interpreter build on Linux Aarch64 is broken | [Link]([需要补充 PR 链接]) |
| JDK-8340212 | -Xshare:off -XX:CompressedClassSpaceBaseAddress=... crashes on macos-aarch64 | [Link]([需要补充 PR 链接]) |

## Key Contributions

### 1. Making Class Methods Non-Native

**JDK-8349860: Make Class.isArray(), Class.isInterface() and Class.isPrimitive() non-native**

Moved native methods to Java, improving maintainability:

```java
// Before: Native method
public native boolean isArray();

// After: Java implementation using stored flags
public boolean isArray() {
    return (getModifiers() & Modifier.ARRAY) != 0;
}

// In java_lang_Class.cpp - store flags in Java object
void java_lang_Class::set_modifiers(oop java_class, int value) {
    java_class->int_field_put(_modifiers_offset, value);
}
```

### 2. SIZE_FORMAT Macro Replacement

**JDK-8346990: Remove INTX_FORMAT and UINTX_FORMAT macros**

Modernized printf-style formatting:

```cpp
// Before: Custom macros
printf("Size: " SIZE_FORMAT " bytes\n", size);
printf("Value: " INTX_FORMAT "\n", value);

// After: Standard C format specifiers
printf("Size: %zu bytes\n", size);
printf("Value: %" PRIdPTR "\n", value);
```

### 3. ObjectMonitor Refactoring

**JDK-8354234: Remove friends for ObjectMonitor**

Improved encapsulation by removing friend declarations:

```cpp
// Before: Friend class with full access
class ObjectMonitor : public CHeapObj<mtObjectMonitor> {
  friend class ObjectSynchronizer;
  // ... private members
};

// After: Proper accessors
class ObjectMonitor : public CHeapObj<mtObjectMonitor> {
public:
  int contentions() const { return _contentions; }
  void set_contentions(int value) { _contentions = value; }
private:
  int _contentions;
};
```

### 4. ThreadCritical Removal

**JDK-8356173: Remove ThreadCritical**

Replaced deprecated ThreadCritical with modern synchronization:

```cpp
// Before: ThreadCritical
void add_to_list(Node* node) {
    ThreadCritical tc;
    _list->append(node);
}

// After: Mutex or Atomic operations
void add_to_list(Node* node) {
    MutexLocker ml(_list_mutex, Mutex::_no_safepoint_check_flag);
    _list->append(node);
}
```

### 5. Hidden Class Constant Pool Fix

**JDK-8364360: Defining hidden class with no room in constant pool crashes the VM**

Fixed crash when constant pool is full:

```cpp
// Before: Crash on OOM
ConstantPool* cp = ConstantPool::allocate(loader_data, length, CHECK_NULL);

// After: Proper error handling
ConstantPool* cp = ConstantPool::allocate(loader_data, length, THREAD);
if (HAS_PENDING_EXCEPTION) {
    // Handle out of memory gracefully
    return nullptr;
}
```

## Development Style

### Code Characteristics
- **Encapsulation advocate**: Removes friend classes, adds proper accessors
- **Modernization focus**: Replaces legacy code with modern patterns
- **Memory safety**: Fixes memory leaks and crashes
- **Code cleanup**: Removes unused code and deprecated patterns

### Typical Commit Pattern
1. Identify legacy or problematic code
2. Research impact on dependent code
3. Implement modern replacement
4. Update all call sites
5. Add/update tests

### Review Style
- Often reviewed by David Long (dlong), Roger Riggs (rriggs), Vladimir Ivanov (vlivanov)
- Focuses on correctness and maintainability
- Ensures proper error handling

## Related Links

- [OpenJDK Profile](https://openjdk.org/census#coleenp)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20coleenp)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=coleenp)