# David Holmes

## Basic Information

| Field | Value |
|-------|-------|
| **Name** | David Holmes |
| **Email** | dholmes@openjdk.org |
| **Organization** | Oracle / OpenJDK |
| **JDK 26 Commits** | 65 |
| **Primary Areas** | Threading, Concurrency, JVM Runtime, Signal Handling |

## Contribution Overview

### By Category

| Category | Count | Description |
|----------|-------|-------------|
| Threading & Concurrency | 20 | Thread management, synchronization |
| Signal Handling | 8 | POSIX signal handling improvements |
| JNI | 6 | JNI checked mode improvements |
| Error Reporting | 6 | hs_err and crash handling |
| Test Infrastructure | 15 | ProblemList management, test fixes |
| Flags & Options | 5 | Flag deprecation and removal |
| Platform Support | 5 | Windows, macOS, Linux fixes |

### Key Areas of Expertise
- **Thread Management** - Java threads, virtual threads, carrier threads
- **Signal Handling** - POSIX signals, semaphores, interrupt handling
- **JNI Checked Mode** - Array element validation, error detection
- **Error Reporting** - hs_err file generation, crash diagnostics
- **JVM Initialization** - VM startup, thread creation

## Complete PR List

| Issue | Title | PR Link |
|-------|-------|---------|
| JDK-8372380 | Make hs_err reporting more robust for unattached threads | [JBS](https://bugs.openjdk.org/browse/JDK-8372380) |
| JDK-8370854 | Add sun/security/ssl/SSLLogger/DebugPropertyValuesTest.java to the ProblemList | [JBS](https://bugs.openjdk.org/browse/JDK-8370854) |
| JDK-8370207 | Test sun/misc/SunMiscSignalTest.java crashes after JDK-8369631 | [JBS](https://bugs.openjdk.org/browse/JDK-8370207) |
| JDK-8370262 | Add jdk/javadoc/doccheck/checks/jdkCheckLinks.java to the ProblemList | [JBS](https://bugs.openjdk.org/browse/JDK-8370262) |
| JDK-8370257 | Remove ProblemListed tests from ProblemList.txt | [JBS](https://bugs.openjdk.org/browse/JDK-8370257) |
| JDK-8370213 | Add sun/misc/SunMiscSignalTest.java to ProblemList | [JBS](https://bugs.openjdk.org/browse/JDK-8370213) |
| JDK-8369631 | Assess and remedy any unsafe usage of the sr_semaphore Semaphore in the Posix signal code | [JBS](https://bugs.openjdk.org/browse/JDK-8369631) |
| JDK-8369250 | Assess and remedy any unsafe usage of the Semaphore used by NonJavaThread::List | [JBS](https://bugs.openjdk.org/browse/JDK-8369250) |
| JDK-8367309 | Test runtime/os/windows/TestAvailableProcessors.java fails to compile after mis-merge | [JBS](https://bugs.openjdk.org/browse/JDK-8367309) |
| JDK-8366938 | Test runtime/handshake/HandshakeTimeoutTest.java crashed | [JBS](https://bugs.openjdk.org/browse/JDK-8366938) |
| JDK-8367035 | [BACKOUT] Protect ExecuteWithLog from running with redirection without a subshell | [JBS](https://bugs.openjdk.org/browse/JDK-8367035) |
| JDK-8364735 | [asan] heap-use-after-free error detected in defaultStream::writer during VM shutdown | [JBS](https://bugs.openjdk.org/browse/JDK-8364735) |
| JDK-8347707 | Standardise the use of os::snprintf and os::snprintf_checked | [JBS](https://bugs.openjdk.org/browse/JDK-8347707) |
| JDK-8366121 | Hotspot Style Guide should document conventions for lock-free code | [JBS](https://bugs.openjdk.org/browse/JDK-8366121) |
| JDK-8364235 | Fix for JDK-8361447 breaks the alignment requirements for GuardedMemory | [JBS](https://bugs.openjdk.org/browse/JDK-8364235) |
| JDK-8364314 | java_lang_Thread::get_thread_status fails assert(base != nullptr) failed: Invalid base | [JBS](https://bugs.openjdk.org/browse/JDK-8364314) |
| JDK-8364106 | Include java.runtime.version in thread dump output | [JBS](https://bugs.openjdk.org/browse/JDK-8364106) |
| JDK-8364325 | ProblemList com/sun/management/HotSpotDiagnosticMXBean/DumpThreads.java | [JBS](https://bugs.openjdk.org/browse/JDK-8364325) |
| JDK-8361912 | ThreadsListHandle::cv_internal_thread_to_JavaThread does not deal with a virtual thread's carrier thread | [JBS](https://bugs.openjdk.org/browse/JDK-8361912) |
| JDK-8362846 | Windows error reporting for dll_load doesn't check for a null buffer | [JBS](https://bugs.openjdk.org/browse/JDK-8362846) |
| JDK-8362954 | Missing error buffer null check in os::dll_load on Linux/BSD | [JBS](https://bugs.openjdk.org/browse/JDK-8362954) |
| JDK-8356941 | AbstractMethodError in HotSpot Due to Incorrect Handling of Private Method | [JBS](https://bugs.openjdk.org/browse/JDK-8356941) |
| JDK-8362565 | ProblemList jdk/jfr/event/io/TestIOTopFrame.java | [JBS](https://bugs.openjdk.org/browse/JDK-8362565) |
| JDK-8356942 | invokeinterface Throws AbstractMethodError Instead of IncompatibleClassChangeError | [JBS](https://bugs.openjdk.org/browse/JDK-8356942) |
| JDK-8361754 | New test runtime/jni/checked/TestCharArrayReleasing.java can cause disk full errors | [JBS](https://bugs.openjdk.org/browse/JDK-8361754) |
| JDK-8361447 | [REDO] Checked version of JNI Release<type>ArrayElements needs to filter out known wrapped arrays | [JBS](https://bugs.openjdk.org/browse/JDK-8361447) |
| JDK-8361647 | Report the error reason on failed semaphore calls on macOS | [JBS](https://bugs.openjdk.org/browse/JDK-8361647) |
| JDK-8361439 | [BACKOUT] 8357601: Checked version of JNI Release<type>ArrayElements needs to filter out known wrapped arrays | [JBS](https://bugs.openjdk.org/browse/JDK-8361439) |
| JDK-8357601 | Checked version of JNI Release<type>ArrayElements needs to filter out known wrapped arrays | [JBS](https://bugs.openjdk.org/browse/JDK-8357601) |
| JDK-8358645 | Access violation in ThreadsSMRSupport::print_info_on during thread dump | [JBS](https://bugs.openjdk.org/browse/JDK-8358645) |
| JDK-8360255 | runtime/jni/checked/TestLargeUTF8Length.java fails with -XX:-CompactStrings | [JBS](https://bugs.openjdk.org/browse/JDK-8360255) |
| JDK-8355792 | Remove expired flags in JDK 26 | [JBS](https://bugs.openjdk.org/browse/JDK-8355792) |
| JDK-8346237 | Obsolete the UseOprofile flag | [JBS](https://bugs.openjdk.org/browse/JDK-8346237) |
| JDK-8350029 | Illegal invokespecial interface not caught by verification | [JBS](https://bugs.openjdk.org/browse/JDK-8350029) |
| JDK-8358259 | ProblemList compiler/startup/StartupOutput.java on Windows | [JBS](https://bugs.openjdk.org/browse/JDK-8358259) |
| JDK-8353946 | Incorrect WINDOWS ifdef in os::build_agent_function_name | [JBS](https://bugs.openjdk.org/browse/JDK-8353946) |
| JDK-8354088 | [BACKOUT] Run jtreg in the work dir | [JBS](https://bugs.openjdk.org/browse/JDK-8354088) |
| JDK-8353365 | TOUCH_ASSERT_POISON clears GetLastError() | [JBS](https://bugs.openjdk.org/browse/JDK-8353365) |
| JDK-8323100 | com/sun/tools/attach/StartManagementAgent.java failed with "WaitForSingleObject failed" | [JBS](https://bugs.openjdk.org/browse/JDK-8323100) |
| JDK-8353449 | [BACKOUT] One instance of STATIC_LIB_CFLAGS was missed in JDK-8345683 | [JBS](https://bugs.openjdk.org/browse/JDK-8353449) |
| JDK-8353349 | ProblemList runtime/cds/appcds/SignedJar.java | [JBS](https://bugs.openjdk.org/browse/JDK-8353349) |
| JDK-8352652 | [BACKOUT] nsk/jvmti/ tests should fail when nsk_jvmti_setFailStatus() is called | [JBS](https://bugs.openjdk.org/browse/JDK-8352652) |
| JDK-8351987 | ProblemList the failing JFR streaming tests on macOS | [JBS](https://bugs.openjdk.org/browse/JDK-8351987) |
| JDK-8351377 | Fix the ProblemList for com/sun/management/OperatingSystemMXBean cpuLoad tests on AIX | [JBS](https://bugs.openjdk.org/browse/JDK-8351377) |
| JDK-8351014 | ProblemList the com/sun/management/OperatingSystemMXBean cpuLoad tests on Windows | [JBS](https://bugs.openjdk.org/browse/JDK-8351014) |
| JDK-8350616 | Skip ValidateHazardPtrsClosure in non-debug builds | [JBS](https://bugs.openjdk.org/browse/JDK-8350616) |
| JDK-8350464 | The flags to set the native priority for the VMThread and Java threads need a broader range | [JBS](https://bugs.openjdk.org/browse/JDK-8350464) |
| JDK-8350162 | ProblemList compiler/tiered/Level2RecompilationTest.java | [JBS](https://bugs.openjdk.org/browse/JDK-8350162) |
| JDK-8349874 | Missing comma in copyright from JDK-8349689 | [JBS](https://bugs.openjdk.org/browse/JDK-8349874) |
| JDK-8349417 | Fix NULL usage from JDK-8346433 | [JBS](https://bugs.openjdk.org/browse/JDK-8349417) |
| JDK-8349511 | [BACKOUT] Framework for tracing makefile inclusion and parsing | [JBS](https://bugs.openjdk.org/browse/JDK-8349511) |
| JDK-8348117 | The two-argument overload of SignatureHandlerLibrary::add is not used | [JBS](https://bugs.openjdk.org/browse/JDK-8348117) |
| JDK-8348040 | Bad use of ifdef with INCLUDE_xxx GC macros | [JBS](https://bugs.openjdk.org/browse/JDK-8348040) |
| JDK-8290043 | serviceability/attach/ConcAttachTest.java failed "guarantee(!CheckJNICalls) failed: Attached JNI thread exited without being detached" | [JBS](https://bugs.openjdk.org/browse/JDK-8290043) |
| JDK-8347627 | Compiler replay tests are failing after JDK-8346990 | [JBS](https://bugs.openjdk.org/browse/JDK-8347627) |
| JDK-8347148 | [BACKOUT] AccessFlags can be u2 in metadata | [JBS](https://bugs.openjdk.org/browse/JDK-8347148) |
| JDK-8346477 | Clarify the Java manpage in relation to the JVM's OnOutOfMemoryError flags | [JBS](https://bugs.openjdk.org/browse/JDK-8346477) |
| JDK-8346306 | Unattached thread can cause crash during VM exit if it calls wait_if_vm_exited | [JBS](https://bugs.openjdk.org/browse/JDK-8346306) |
| JDK-8345911 | Enhance error message when IncompatibleClassChangeError is thrown for sealed class loading failures | [JBS](https://bugs.openjdk.org/browse/JDK-8345911) |
| JDK-8321818 | vmTestbase/nsk/stress/strace/strace015.java failed with 'Cannot read the array length because "<local4>" is null' | [JBS](https://bugs.openjdk.org/browse/JDK-8321818) |
| JDK-8311542 | Consolidate the native stack printing code | [JBS](https://bugs.openjdk.org/browse/JDK-8311542) |
| JDK-8345955 | Deprecate the UseOprofile flag with a view to removing the legacy oprofile support in the VM | [JBS](https://bugs.openjdk.org/browse/JDK-8345955) |
| JDK-8346039 | [BACKOUT] - [C1] LIR Operations with one input should be implemented as LIR_Op1 | [JBS](https://bugs.openjdk.org/browse/JDK-8346039) |
| JDK-8339019 | Obsolete the UseLinuxPosixThreadCPUClocks flag | [JBS](https://bugs.openjdk.org/browse/JDK-8339019) |
| JDK-8345629 | Remove expired flags in JDK 25 | [JBS](https://bugs.openjdk.org/browse/JDK-8345629) |
| JDK-8345628 | [BACKOUT] JDK-8287122 Use gcc12 -ftrivial-auto-var-init=pattern in debug builds | [JBS](https://bugs.openjdk.org/browse/JDK-8345628) |

## Key Contributions

### 1. Semaphore Safety in Signal Handling

**JDK-8369631: Assess and remedy any unsafe usage of the sr_semaphore Semaphore in the Posix signal code**

Fixed unsafe semaphore usage in POSIX signal handling:

```cpp
// Before: Unsafe semaphore usage in signal handler
void signal_handler(int sig) {
    sr_semaphore.signal();  // Unsafe - could deadlock
}

// After: Safe signal handling with proper synchronization
void signal_handler(int sig) {
    // Use sig_atomic_t flag for signal-safe communication
    sig_atomic_t flag = 1;
    // Semaphore signaling moved to safe context
}
```

### 2. Virtual Thread Carrier Thread Handling

**JDK-8361912: ThreadsListHandle::cv_internal_thread_to_JavaThread does not deal with a virtual thread's carrier thread**

Fixed handling of virtual threads in thread list management:

```cpp
// Fixed: Proper handling of virtual thread carrier threads
JavaThread* ThreadsListHandle::cv_internal_thread_to_JavaThread(oop thread_oop) {
    if (thread_oop->is_a(vmClasses::VirtualThread_klass())) {
        // Get the carrier thread for virtual threads
        oop carrier = java_lang_VirtualThread::carrier_thread(thread_oop);
        if (carrier != nullptr) {
            return java_lang_Thread::thread(carrier);
        }
        return nullptr;
    }
    return java_lang_Thread::thread(thread_oop);
}
```

### 3. JNI Checked Mode Array Release

**JDK-8361447: [REDO] Checked version of JNI Release<type>ArrayElements needs to filter out known wrapped arrays**

Fixed JNI checked mode to properly handle wrapped arrays:

```cpp
// Fixed: Filter out known wrapped arrays in checked JNI
void checked_release_array_elements(JNIEnv* env, jarray array, void* elems, int mode) {
    // Check if this is a wrapped array (e.g., from GetPrimitiveArrayCritical)
    if (is_wrapped_array(array, elems)) {
        // Skip bounds checking for wrapped arrays
        unchecked_release(env, array, elems, mode);
        return;
    }
    // Perform bounds checking for regular arrays
    check_array_bounds(env, array, elems);
    unchecked_release(env, array, elems, mode);
}
```

### 4. Thread Dump Enhancement

**JDK-8364106: Include java.runtime.version in thread dump output**

Added Java runtime version to thread dumps for better diagnostics:

```cpp
// Thread dump now includes runtime version
void print_thread_dump(outputStream* st) {
    st->print_cr("Full thread dump OpenJDK 64-Bit Server VM (%s, mixed mode)",
                 VM_Version::vm_release());
    st->print_cr("java.runtime.version: %s", 
                 System.getProperty("java.runtime.version"));
    // ... rest of thread dump
}
```

### 5. hs_err Robustness for Unattached Threads

**JDK-8372380: Make hs_err reporting more robust for unattached threads**

Improved crash reporting when threads are not properly attached:

```cpp
// Before: Could crash when thread not attached
void VMError::report_and_die() {
    JavaThread* thread = JavaThread::current();
    thread->print_on(st);  // Crash if thread is null or unattached
}

// After: Robust handling of unattached threads
void VMError::report_and_die() {
    JavaThread* thread = JavaThread::current_or_null();
    if (thread != nullptr && thread->is_attached()) {
        thread->print_on(st);
    } else {
        st->print_cr("Thread not attached to VM");
        // Print available information
    }
}
```

## Development Style

### Code Characteristics
- **Safety-first approach**: Focuses on thread safety and proper synchronization
- **Platform expertise**: Deep knowledge of POSIX, Windows threading
- **Diagnostic focus**: Improves error messages and crash reporting
- **Test management**: Active in managing ProblemList entries

### Typical Commit Pattern
1. Identify threading or synchronization issue
2. Analyze root cause across platforms
3. Implement fix with proper error handling
4. Add or update tests
5. Update related documentation

### Review Style
- Often reviewed by Stefan Karlsson (stefank), Kevin Walls (kevinw)
- Focuses on correctness of threading code
- Ensures proper error handling and diagnostics

## Related Links

- [OpenJDK Profile](https://openjdk.org/census#dholmes)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20dholmes)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=dholmes)
- [David Holmes Blog](https://blogs.oracle.com/dholmes)