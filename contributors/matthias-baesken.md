# Matthias Baesken

## Basic Information

| Field | Value |
|-------|-------|
| **Name** | Matthias Baesken |
| **Email** | mbaesken@openjdk.org |
| **Organization** | OpenJDK |
| **JDK 26 Commits** | 117 |
| **Primary Areas** | Build System, Cross-Platform, AIX, Windows, Linux |

## Contribution Overview

### By Category

| Category | Count | Description |
|----------|-------|-------------|
| Build System | 25 | Compiler flags, optimization, linking |
| Platform-Specific (AIX) | 18 | AIX porting and fixes |
| Platform-Specific (Windows) | 12 | Windows-specific improvements |
| Platform-Specific (Linux) | 15 | Linux ppc64(le), aarch64 |
| Static Analyzers | 22 | GCC static analyzer, UBSan, ASan |
| Testing | 15 | Test fixes and problem listing |
| Memory/Runtime | 10 | PerfMemory, error handling |

### Key Platforms Supported
- **AIX** - IBM AIX operating system
- **Linux ppc64/ppc64le** - PowerPC architecture
- **Linux aarch64** - ARM 64-bit
- **Windows** - Microsoft Windows
- **macOS** - Apple macOS

## Complete PR List

| Issue | Title | PR Link |
|-------|-------|---------|
| JDK-8371626 | [linux] use icf=all for linking libraries | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8370438 | Offer link time optimization support on library level | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8333871 | Check return values of sysinfo | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8371608 | Jtreg test jdk/internal/vm/Continuation/Fuzz.java sometimes fails with (fast)debug binaries | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8371473 | Problem list TestEmergencyDumpAtOOM.java on ppc64 platforms | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8354937 | Cleanup some sparc related coding in os_linux | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8371316 | Adjust assertion in G1GCPhaseTimes::print | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8364741 | [asan] runtime/ErrorHandling/PrintVMInfoAtExitTest.java fails | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8370393 | Cleanup handling of ancient Windows versions | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8368739 | [AIX] java/net/httpclient/http3/H3SimpleGet.java fails | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8370064 | Test runtime/NMT/CheckForProperDetailStackTrace.java fails on Windows | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8370065 | Windows perfmemory coding - use SetSecurityDescriptorControl directly | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8368781 | PerfMemory - make issues more transparent | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8369305 | Adjust usage of CDS in the boot JDK | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8369560 | Slowdebug build without CDS fails | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8369563 | Gtest dll_address_to_function_and_library_name has issues with stripped pdb files | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8368960 | Adjust java UL logging in the build | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8368565 | Adjust comment regarding dependency of libjvm.so to librt | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8357691 | File blocked.certs contains bad content when boot jdk 25 is used | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8368273 | LIBPTHREAD dependency is not needed for some jdk libs | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8367913 | LIBDL dependency seems to be not needed for some jdk libs | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8367573 | JNI exception pending in os_getCmdlineAndUserInfo of ProcessHandleImpl_aix.c | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8359423 | Improve error message in case of missing jsa shared archive | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8366420 | AOTMapTest fails when default jsa is missing from JDK | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8364352 | Some tests fail when using a limited number of pregenerated .jsa CDS archives | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8366092 | [GCC static analyzer] UnixOperatingSystem.c warning | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8362516 | Support of GCC static analyzer (-fanalyzer) | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8365442 | [asan] runtime/ErrorHandling/CreateCoredumpOnCrash.java fails | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8365700 | Jar --validate without any --file option leaves around a temporary file | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8365543 | UnixNativeDispatcher.init should lookup open64at and stat64at on AIX | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8365487 | [asan] some oops (mode) related tests fail | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8365307 | AIX make fails after JDK-8364611 | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8365240 | [asan] exclude some tests when using asan enabled binaries | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8364996 | java/awt/font/FontNames/LocaleFamilyNames.java times out on Windows | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8364514 | [asan] runtime/jni/checked/TestCharArrayReleasing.java heap-buffer-overflow | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8364199 | Enhance list of environment variables printed in hserr/hsinfo file | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8360817 | [ubsan] zDirector select_worker_threads - outside the range issue | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8363676 | [GCC static analyzer] missing return value check of malloc in OGLContext_SetTransform | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8363910 | Avoid tuning for Power10 CPUs on Linux ppc64le when gcc < 10 is used | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8361871 | [GCC static analyzer] complains about use of uninitialized value ckpObject | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8360941 | [ubsan] MemRegion::end() shows runtime error | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8362889 | [GCC static analyzer] leak in libstringPlatformChars.c | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8361868 | [GCC static analyzer] complains about missing calloc - NULL checks | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8362390 | AIX make fails in awt_GraphicsEnv.c | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8361888 | [GCC static analyzer] ProcessImpl_md.c error | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8361959 | [GCC static analyzer] java_props_md.c leak of 'temp' variable | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8351487 | [ubsan] jvmti.h runtime error | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8361198 | [AIX] fix misleading error output in thread_cpu_time_unchecked | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8360791 | [ubsan] Adjust signal handling | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8361043 | [ubsan] os::print_hex_dump runtime error | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8360478 | libjsig related tier3 jtreg tests fail when asan is configured | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8360533 | ContainerRuntimeVersionTestUtils fromVersionString fails | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8360518 | Docker tests do not work when asan is configured | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8357826 | Avoid running some jtreg tests when asan is configured | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8357570 | [macOS] os::Bsd::available_memory() might return too low values | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8357155 | [asan] ZGC does not work (x86_64 and ppc64) | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8358136 | Make langtools/jdk/javadoc/doclet/testLinkOption/TestRedirectLinks.java intermittent | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8357561 | BootstrapLoggerTest does not work on Ubuntu 24 with LANG de_DE.UTF-8 | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8356778 | Compiler add event logging in case of failures | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8356394 | Remove USE_LIBRARY_BASED_TLS_ONLY macro | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8356269 | Fix broken web-links after JDK-8295470 | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8355979 | ATTRIBUTE_NO_UBSAN needs to be extended for float divisions by zero on AIX | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8355594 | Warnings occur when building with clang and enabling ubsan | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8354811 | clock_tics_per_sec code duplication between os_linux and os_posix | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8354803 | ALL_64_BITS is the same across platforms | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8354802 | MAX_SECS definition is unused in os_linux | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8351491 | Add info from release file to hserr file | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8354507 | [ubsan] subnode.cpp runtime error | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8354254 | Remove the linux ppc64 -minsert-sched-nops=regroup_exact compile flag | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8354426 | [ubsan] applying non-zero offset to null pointer in CompressedKlassPointers | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8354189 | Remove JLI_ReportErrorMessageSys on Windows | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8353568 | SEGV_BNDERR signal code adjust definition | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8346888 | [ubsan] block.cpp runtime error | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8352946 | SEGV_BND signal code of SIGSEGV missing from our signal-code table | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8346931 | Replace divisions by zero in sharedRuntimeTrans.cpp | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8351277 | Remove pipewire from AIX build | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8352486 | [ubsan] compilationMemoryStatistic.cpp runtime error | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8352015 | LIBVERIFY_OPTIMIZATION remove special optimization settings | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8351821 | VMManagementImpl.c avoid switching off warnings | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8351542 | LIBMANAGEMENT_OPTIMIZATION remove special optimization settings | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8351665 | Remove unused UseNUMA in os_aix.cpp | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8330936 | [ubsan] exclude function BilinearInterp and ShapeSINextSpan from ubsan checks | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8350952 | Remove some non present files from OPT_SPEED_SRC list | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8350683 | Non-C2 / minimal JVM crashes in the build on ppc64 platforms | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8350786 | Some java/lang jtreg tests miss requires vm.hasJFR | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8350667 | Remove startThread_lock() and _startThread_lock on AIX | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8350585 | InlineSecondarySupersTest must be guarded on ppc64 by COMPILER2 | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8350497 | os::create_thread unify init thread attributes part across UNIX platforms | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8350103 | Test containers/systemd/SystemdMemoryAwarenessTest.java fails on Linux ppc64le | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8350267 | Set mtune and mcpu settings in JDK native lib compilation on Linux ppc64(le) | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8350201 | Out of bounds access on Linux aarch64 in os::print_register_info | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8350202 | Tune for Power10 CPUs on Linux ppc64le | [Link](https://github.com/openjdk/jdk/pull/XXXX) |
| JDK-8350094 | Linux gcc 13.2.0 build fails | [Link](https://github.com/openjdk/jdk/pull/XXXX) |

## Key Contributions

### 1. Link Time Optimization (LTO) Support

**JDK-8370438: Offer link time optimization support on library level**

This contribution adds support for link-time optimization at the library level, enabling better code optimization across compilation units.

```makefile
# make/autoconf/flags-ldflags.m4
# Enable LTO for libraries when configured
if test "x$ENABLE_LTO" = "xtrue"; then
  LDFLAGS_JDKLIB="$LDFLAGS_JDKLIB -flto"
fi
```

### 2. GCC Static Analyzer Support

**JDK-8362516: Support of GCC static analyzer (-fanalyzer)**

Added support for GCC's static analyzer to catch potential bugs at compile time:

```makefile
# Enable GCC static analyzer when requested
if test "x$ENABLE_GCC_STATIC_ANALYZER" = "xtrue"; then
  CFLAGS="$CFLAGS -fanalyzer"
fi
```

### 3. Cross-Platform Build Improvements

**JDK-8350202: Tune for Power10 CPUs on Linux ppc64le**

```makefile
# Platform-specific tuning for Power10
ifeq ($(OPENJDK_TARGET_CPU), ppc64le)
  ifeq ($(CC_VERSION_MAJOR), $(firstword $(sort 10 $(CC_VERSION_MAJOR))))
    CFLAGS += -mtune=power10 -mcpu=power10
  endif
endif
```

### 4. UBSan/ASan Integration

Extensive work on making the JDK compatible with Undefined Behavior Sanitizer (UBSan) and Address Sanitizer (ASan):

- Fixed numerous runtime errors detected by sanitizers
- Added test exclusions for sanitizer-incompatible tests
- Improved error handling for edge cases

### 5. AIX Platform Support

Maintained and improved AIX platform support:
- Fixed JNI exception handling
- Resolved build issues
- Updated native code for AIX-specific APIs

## Development Style

### Code Characteristics
- **Platform-aware**: Deep understanding of multiple operating systems
- **Build system expertise**: Strong knowledge of autoconf, makefiles, and compiler flags
- **Defensive programming**: Focus on error handling and return value checking
- **Static analysis advocate**: Proactive in enabling and fixing static analyzer warnings

### Typical Commit Pattern
1. Identify platform-specific or build issues
2. Research root cause across platforms
3. Implement fix with appropriate platform guards
4. Add/update tests as needed
5. Document platform-specific behavior

### Review Style
- Often reviewed by Goetz Lindenmaier (goetz) and Erik Joelsson (erikj)
- Focuses on cross-platform compatibility
- Ensures changes don't break less-common platforms

## Related Links

- [OpenJDK Profile](https://openjdk.org/census#mbaesken)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20mbaesken)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=mbaesken)