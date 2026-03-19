# Magnus Ihse Bursie

## Basic Information

| Field | Value |
|-------|-------|
| **Name** | Magnus Ihse Bursie |
| **Current Organization** | Oracle |
| **GitHub** | [@magicus](https://github.com/magicus) |
| **OpenJDK** | [@ihse](https://openjdk.org/census#ihse) |
| **Role** | OpenJDK Member, JDK Reviewer |
| **PRs** | [351 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Amagicus+is%3Aclosed+label%3Aintegrated) |
| **Primary Areas** | Build System, Makefiles, Configure Scripts |

> **Data as of**: 2026-03-19

## Contribution Overview

Magnus Ihse Bursie is the primary maintainer of the JDK build system. His work in JDK 26 represents a massive effort to modernize the build infrastructure, improve UTF-8 support, enable static builds, and enhance developer experience.

### Contribution Categories

| Category | Count | Description |
|----------|-------|-------------|
| Build Infrastructure | 45 | Core build system improvements |
| UTF-8/Encoding | 12 | Source code encoding modernization |
| Static Builds | 8 | Windows static build support |
| Configure | 15 | Configure script improvements |
| Testing | 8 | Test infrastructure enhancements |
| Cleanup | 18 | Code cleanup and maintenance |

## Complete PR List

| Issue | Title | PR Link |
|-------|-------|---------|
| JDK-8187520 | Add --disable-java-warnings-as-errors configure option | [JBS](https://bugs.openjdk.org/browse/JDK-8187520) |
| JDK-8196896 | Use SYSROOT_CFLAGS in dtrace gensrc | [JBS](https://bugs.openjdk.org/browse/JDK-8196896) |
| JDK-8233115 | Protect ExecuteWithLog from running with redirection without a subshell | [JBS](https://bugs.openjdk.org/browse/JDK-8233115) |
| JDK-8244533 | Configure should abort on missing short names in Windows | [JBS](https://bugs.openjdk.org/browse/JDK-8244533) |
| JDK-8246325 | Add DRYRUN facility to SetupExecute | [JBS](https://bugs.openjdk.org/browse/JDK-8246325) |
| JDK-8282493 | Add --with-jcov-modules convenience option | [JBS](https://bugs.openjdk.org/browse/JDK-8282493) |
| JDK-8285692 | Enable _FORTIFY_SOURCE=2 when building with Clang | [JBS](https://bugs.openjdk.org/browse/JDK-8285692) |
| JDK-8287122 | Use gcc12 -ftrivial-auto-var-init=pattern in debug builds | [JBS](https://bugs.openjdk.org/browse/JDK-8287122) |
| JDK-8292944 | Noisy output when running make help the first time | [JBS](https://bugs.openjdk.org/browse/JDK-8292944) |
| JDK-8300339 | Run jtreg in the work dir | [JBS](https://bugs.openjdk.org/browse/JDK-8300339) |
| JDK-8301197 | Make sure use of printf is correct and actually needed | [JBS](https://bugs.openjdk.org/browse/JDK-8301197) |
| JDK-8301971 | Make JDK source code UTF-8 | [JBS](https://bugs.openjdk.org/browse/JDK-8301971) |
| JDK-8311227 | Add .editorconfig | [JBS](https://bugs.openjdk.org/browse/JDK-8311227) |
| JDK-8315844 | $LSB_RELEASE is not defined before use | [JBS](https://bugs.openjdk.org/browse/JDK-8315844) |
| JDK-8317012 | Explicitly check for 32-bit word size for using libatomic with zero | [JBS](https://bugs.openjdk.org/browse/JDK-8317012) |
| JDK-8329173 | LCMS_CFLAGS from configure are lost | [JBS](https://bugs.openjdk.org/browse/JDK-8329173) |
| JDK-8330341 | Wrap call to MT in ExecuteWithLog | [JBS](https://bugs.openjdk.org/browse/JDK-8330341) |
| JDK-8332872 | SetupExecute should cd to temp directory | [JBS](https://bugs.openjdk.org/browse/JDK-8332872) |
| JDK-8334391 | JDK build should exclude *-files directories for Java source | [JBS](https://bugs.openjdk.org/browse/JDK-8334391) |
| JDK-8338973 | Document need to have UTF-8 locale available to build the JDK | [JBS](https://bugs.openjdk.org/browse/JDK-8338973) |
| JDK-8339622 | Regression in make open-hotspot-xcode-project | [JBS](https://bugs.openjdk.org/browse/JDK-8339622) |
| JDK-8340185 | Use make -k on GHA to catch more build errors | [JBS](https://bugs.openjdk.org/browse/JDK-8340185) |
| JDK-8340341 | Abort in configure when using Xcode 16.0 or 16.1 | [JBS](https://bugs.openjdk.org/browse/JDK-8340341) |
| JDK-8344030 | Improved handling of TOOLCHAIN_PATH | [JBS](https://bugs.openjdk.org/browse/JDK-8344030) |
| JDK-8344559 | Log is spammed by missing pandoc warnings when building man pages | [JBS](https://bugs.openjdk.org/browse/JDK-8344559) |
| JDK-8345424 | Move FindDebuginfoFiles out of FileUtils.gmk | [JBS](https://bugs.openjdk.org/browse/JDK-8345424) |
| JDK-8345627 | [REDO] Use gcc12 -ftrivial-auto-var-init=pattern in debug builds | [JBS](https://bugs.openjdk.org/browse/JDK-8345627) |
| JDK-8345683 | Remove special flags for files compiled for static libraries | [JBS](https://bugs.openjdk.org/browse/JDK-8345683) |
| JDK-8345793 | Update copyright year to 2024 for the build system in files where it was missed | [JBS](https://bugs.openjdk.org/browse/JDK-8345793) |
| JDK-8345795 | Update copyright year to 2024 for hotspot in files where it was missed | [JBS](https://bugs.openjdk.org/browse/JDK-8345795) |
| JDK-8345797 | Update copyright year to 2024 for client-libs in files where it was missed | [JBS](https://bugs.openjdk.org/browse/JDK-8345797) |
| JDK-8345799 | Update copyright year to 2024 for core-libs in files where it was missed | [JBS](https://bugs.openjdk.org/browse/JDK-8345799) |
| JDK-8345800 | Update copyright year to 2024 for serviceability in files where it was missed | [JBS](https://bugs.openjdk.org/browse/JDK-8345800) |
| JDK-8345803 | Update copyright year to 2024 for security in files where it was missed | [JBS](https://bugs.openjdk.org/browse/JDK-8345803) |
| JDK-8345804 | Update copyright year to 2024 for langtools in files where it was missed | [JBS](https://bugs.openjdk.org/browse/JDK-8345804) |
| JDK-8345805 | Update copyright year to 2024 for other files where it was missed | [JBS](https://bugs.openjdk.org/browse/JDK-8345805) |
| JDK-8346195 | Fix static initialization problem in GDIHashtable | [JBS](https://bugs.openjdk.org/browse/JDK-8346195) |
| JDK-8346278 | Clean up some flag handing in flags-cflags.m4 | [JBS](https://bugs.openjdk.org/browse/JDK-8346278) |
| JDK-8346377 | Properly support static builds for Windows | [JBS](https://bugs.openjdk.org/browse/JDK-8346377) |
| JDK-8346378 | Cannot use DllMain in libnet for static builds | [JBS](https://bugs.openjdk.org/browse/JDK-8346378) |
| JDK-8346383 | Cannot use DllMain in libdt_socket for static builds | [JBS](https://bugs.openjdk.org/browse/JDK-8346383) |
| JDK-8346388 | Cannot use DllMain in libawt for static builds | [JBS](https://bugs.openjdk.org/browse/JDK-8346388) |
| JDK-8346394 | Bundled freetype library needs to have JNI_OnLoad for static builds | [JBS](https://bugs.openjdk.org/browse/JDK-8346394) |
| JDK-8346433 | Cannot use DllMain in hotspot for static builds | [JBS](https://bugs.openjdk.org/browse/JDK-8346433) |
| JDK-8346669 | Increase abstraction in SetupBuildLauncher and remove extra args | [JBS](https://bugs.openjdk.org/browse/JDK-8346669) |
| JDK-8346719 | Add relaunchers to the static JDK image for missing executables | [JBS](https://bugs.openjdk.org/browse/JDK-8346719) |
| JDK-8347501 | Make static-launcher fails after JDK-8346669 | [JBS](https://bugs.openjdk.org/browse/JDK-8347501) |
| JDK-8347570 | Configure fails on macOS if directory name do not have correct case | [JBS](https://bugs.openjdk.org/browse/JDK-8347570) |
| JDK-8347825 | Make IDEA ide support use proper build system mechanisms | [JBS](https://bugs.openjdk.org/browse/JDK-8347825) |
| JDK-8347996 | JavaCompilation.gmk should not include ZipArchive.gmk | [JBS](https://bugs.openjdk.org/browse/JDK-8347996) |
| JDK-8348039 | testmake fails at IDEA after JDK-8347825 | [JBS](https://bugs.openjdk.org/browse/JDK-8348039) |
| JDK-8348190 | Framework for tracing makefile inclusion and parsing | [JBS](https://bugs.openjdk.org/browse/JDK-8348190) |
| JDK-8348324 | The failure handler cannot be build by JDK 24 due to restricted warning | [JBS](https://bugs.openjdk.org/browse/JDK-8348324) |
| JDK-8348387 | Add fixpath if needed for user-supplied tools | [JBS](https://bugs.openjdk.org/browse/JDK-8348387) |
| JDK-8348391 | Keep case if possible for TOPDIR | [JBS](https://bugs.openjdk.org/browse/JDK-8348391) |
| JDK-8348392 | Make claims "other matches are possible" even when that is not true | [JBS](https://bugs.openjdk.org/browse/JDK-8348392) |
| JDK-8348429 | Update cross-compilation devkits to Fedora 41/gcc 13.2 | [JBS](https://bugs.openjdk.org/browse/JDK-8348429) |
| JDK-8348586 | Optionally silence make warnings about non-control variables | [JBS](https://bugs.openjdk.org/browse/JDK-8348586) |
| JDK-8348998 | Split out PreInit.gmk from Init.gmk | [JBS](https://bugs.openjdk.org/browse/JDK-8348998) |
| JDK-8349075 | Once again allow -compilejdk in JAVA_OPTIONS | [JBS](https://bugs.openjdk.org/browse/JDK-8349075) |
| JDK-8349143 | All make control variables need special propagation | [JBS](https://bugs.openjdk.org/browse/JDK-8349143) |
| JDK-8349467 | INIT_TARGETS tab completions on "make" lost with JDK-8348998 | [JBS](https://bugs.openjdk.org/browse/JDK-8349467) |
| JDK-8349515 | [REDO] Framework for tracing makefile inclusion and parsing | [JBS](https://bugs.openjdk.org/browse/JDK-8349515) |
| JDK-8349665 | Make clean removes module-deps.gmk | [JBS](https://bugs.openjdk.org/browse/JDK-8349665) |
| JDK-8350774 | Generated test-<testname> targets broken after JDK-8348998 | [JBS](https://bugs.openjdk.org/browse/JDK-8350774) |
| JDK-8351029 | IncludeCustomExtension does not work on cygwin with source code below /home | [JBS](https://bugs.openjdk.org/browse/JDK-8351029) |
| JDK-8351154 | Use -ftrivial-auto-var-init=pattern for clang too | [JBS](https://bugs.openjdk.org/browse/JDK-8351154) |
| JDK-8352506 | Simplify make/test/JtregNativeHotspot.gmk | [JBS](https://bugs.openjdk.org/browse/JDK-8352506) |
| JDK-8352618 | Remove old deprecated functionality in the build system | [JBS](https://bugs.openjdk.org/browse/JDK-8352618) |
| JDK-8353066 | Properly detect Windows/aarch64 as build platform | [JBS](https://bugs.openjdk.org/browse/JDK-8353066) |
| JDK-8353458 | Don't pass -Wno-format-nonliteral to CFLAGS | [JBS](https://bugs.openjdk.org/browse/JDK-8353458) |
| JDK-8354213 | Restore pointless unicode characters to ASCII | [JBS](https://bugs.openjdk.org/browse/JDK-8354213) |
| JDK-8354266 | Fix non-UTF-8 text encoding | [JBS](https://bugs.openjdk.org/browse/JDK-8354266) |
| JDK-8354273 | Replace even more Unicode characters with ASCII | [JBS](https://bugs.openjdk.org/browse/JDK-8354273) |
| JDK-8354278 | Revert use of non-POSIX echo -n introduced in JDK-8301197 | [JBS](https://bugs.openjdk.org/browse/JDK-8354278) |
| JDK-8354968 | Replace unicode sequences in comment text with UTF-8 characters | [JBS](https://bugs.openjdk.org/browse/JDK-8354968) |
| JDK-8355725 | SPEC_FILTER stopped working | [JBS](https://bugs.openjdk.org/browse/JDK-8355725) |
| JDK-8356335 | Remove linux-x86 from jib profiles | [JBS](https://bugs.openjdk.org/browse/JDK-8356335) |
| JDK-8356379 | Need a proper way to test existence of binary from configure | [JBS](https://bugs.openjdk.org/browse/JDK-8356379) |
| JDK-8356644 | Update encoding declaration to UTF-8 | [JBS](https://bugs.openjdk.org/browse/JDK-8356644) |
| JDK-8356977 | UTF-8 cleanups | [JBS](https://bugs.openjdk.org/browse/JDK-8356977) |
| JDK-8356978 | Convert unicode sequences in Java source code to UTF-8 | [JBS](https://bugs.openjdk.org/browse/JDK-8356978) |
| JDK-8357048 | RunTest variables should always be assigned | [JBS](https://bugs.openjdk.org/browse/JDK-8357048) |
| JDK-8357510 | [REDO] RunTest variables should always be assigned | [JBS](https://bugs.openjdk.org/browse/JDK-8357510) |
| JDK-8357842 | PandocFilter misses copyright header | [JBS](https://bugs.openjdk.org/browse/JDK-8357842) |
| JDK-8357920 | Add .rej and .orig to .gitignore | [JBS](https://bugs.openjdk.org/browse/JDK-8357920) |
| JDK-8357979 | Compile jdk.internal.vm.ci targeting the Boot JDK version | [JBS](https://bugs.openjdk.org/browse/JDK-8357979) |
| JDK-8357991 | make bootcycle-images is broken after JDK-8349665 | [JBS](https://bugs.openjdk.org/browse/JDK-8357991) |
| JDK-8358337 | JDK-8357991 was committed with incorrect indentation | [JBS](https://bugs.openjdk.org/browse/JDK-8358337) |
| JDK-8358515 | make cmp-baseline is broken after JDK-8349665 | [JBS](https://bugs.openjdk.org/browse/JDK-8358515) |
| JDK-8358538 | Update GHA Windows runner to 2025 | [JBS](https://bugs.openjdk.org/browse/JDK-8358538) |
| JDK-8358543 | Remove CommentChecker.java and DirDiff.java | [JBS](https://bugs.openjdk.org/browse/JDK-8358543) |
| JDK-8361142 | Improve custom hooks for makefiles | [JBS](https://bugs.openjdk.org/browse/JDK-8361142) |
| JDK-8361306 | jdk.compiler-gendata needs to depend on java.base-launchers | [JBS](https://bugs.openjdk.org/browse/JDK-8361306) |
| JDK-8365231 | Don't build gtest with /EHsc | [JBS](https://bugs.openjdk.org/browse/JDK-8365231) |
| JDK-8366836 | Don't execute post-IncludeCustomExtension if file was not included | [JBS](https://bugs.openjdk.org/browse/JDK-8366836) |
| JDK-8366837 | Clean up gensrc by spp.Spp | [JBS](https://bugs.openjdk.org/browse/JDK-8366837) |
| JDK-8366899 | SetupExecute should add the command line to vardeps | [JBS](https://bugs.openjdk.org/browse/JDK-8366899) |
| JDK-8367034 | [REDO] Protect ExecuteWithLog from running with redirection without a subshell | [JBS](https://bugs.openjdk.org/browse/JDK-8367034) |
| JDK-8367259 | Clean up make/scripts and bin directory | [JBS](https://bugs.openjdk.org/browse/JDK-8367259) |
| JDK-8367859 | Remove nio exception gensrc | [JBS](https://bugs.openjdk.org/browse/JDK-8367859) |
| JDK-8368094 | Fix problem list errors | [JBS](https://bugs.openjdk.org/browse/JDK-8368094) |
| JDK-8368102 | Don't store macros in spec.gmk | [JBS](https://bugs.openjdk.org/browse/JDK-8368102) |
| JDK-8368312 | Move CC_OUT_OPTION out of spec.gmk | [JBS](https://bugs.openjdk.org/browse/JDK-8368312) |
| JDK-8368326 | Don't export unresolved make variables from configure | [JBS](https://bugs.openjdk.org/browse/JDK-8368326) |
| JDK-8368468 | Split out everything but configure results from spec.gmk | [JBS](https://bugs.openjdk.org/browse/JDK-8368468) |
| JDK-8368674 | Incremental builds keep rebuilding interim jmod | [JBS](https://bugs.openjdk.org/browse/JDK-8368674) |

## Key Contributions

### 1. UTF-8 Source Code Migration (JDK-8301971, JDK-8338973)

A landmark change that makes the JDK source code UTF-8 by default, modernizing the codebase and improving internationalization support.

**Key Changes in make/autoconf/basic.m4:**

```m4
# Check if we actually have C.UTF-8; if so, use it
if $LOCALE -a | $GREP -q -E "^C\.(utf8|UTF-8)$"; then
  LOCALE_USED=C.UTF-8
  AC_MSG_RESULT([C.UTF-8 (recommended)])
elif $LOCALE -a | $GREP -q -E "^en_US\.(utf8|UTF-8)$"; then
  LOCALE_USED=en_US.UTF-8
  AC_MSG_RESULT([en_US.UTF-8 (acceptable fallback)])
else
  # As a fallback, check if users locale is UTF-8
  if $ECHO $USER_LOCALE | $GREP -q -E "\.(utf8|UTF-8)$"; then
    LOCALE_USED=$USER_LOCALE
    AC_MSG_RESULT([$USER_LOCALE (untested fallback)])
    AC_MSG_WARN([Could not find C.UTF-8 or en_US.UTF-8 locale.])
  else
    AC_MSG_RESULT([no UTF-8 locale found])
    LOCALE_USED=C
  fi
fi
```

**Impact:** 13 files changed, 72 insertions(+), 128 deletions(-)

### 2. Windows Static Build Support (JDK-8346377)

Comprehensive support for static builds on Windows, enabling new deployment scenarios.

**Key Changes:**
- Modified `make/StaticLibs.gmk` for Windows-specific handling
- Updated `make/autoconf/flags-ldflags.m4` for static linking flags
- Fixed DllMain issues in multiple libraries (libnet, libdt_socket, libawt, hotspot)
- Added JNI_OnLoad for bundled freetype library

**Impact:** 5 files changed, 55 insertions(+), 21 deletions(-)

### 3. Makefile Infrastructure Improvements

A series of improvements to the build system infrastructure:

| Issue | Description |
|-------|-------------|
| JDK-8348998 | Split out PreInit.gmk from Init.gmk |
| JDK-8348190 | Framework for tracing makefile inclusion and parsing |
| JDK-8348586 | Optionally silence make warnings about non-control variables |
| JDK-8368102 | Don't store macros in spec.gmk |
| JDK-8368468 | Split out everything but configure results from spec.gmk |

### 4. DevKit Updates (JDK-8348429)

Updated cross-compilation devkits to Fedora 41 with GCC 13.2, ensuring modern compiler support.

### 5. Security Hardening

Enabled additional security features in debug builds:

| Issue | Description |
|-------|-------------|
| JDK-8287122 | Use gcc12 -ftrivial-auto-var-init=pattern in debug builds |
| JDK-8285692 | Enable _FORTIFY_SOURCE=2 when building with Clang |
| JDK-8351154 | Use -ftrivial-auto-var-init=pattern for clang too |

### 6. IDE Support Improvements

| Issue | Description |
|-------|-------------|
| JDK-8347825 | Make IDEA ide support use proper build system mechanisms |
| JDK-8311227 | Add .editorconfig |

## Development Style

### Build System Philosophy

Magnus Ihse Bursie's approach to build system development emphasizes:

1. **Incremental Improvements**: Large changes broken into reviewable chunks
2. **Cross-Platform Consistency**: Ensuring builds work on Linux, macOS, and Windows
3. **Developer Experience**: Clear error messages and helpful warnings
4. **Maintainability**: Clean, well-documented makefiles and configure scripts

### Commit Pattern Analysis

```
Typical commit structure:
- Clear JBS issue reference
- Detailed explanation of the problem
- Step-by-step solution description
- Reviewed-by: typically erikj, mbaesken, naoto
- Focus on one logical change per commit
```

### Key Technical Areas

1. **GNU Make**: Deep expertise in makefile patterns and best practices
2. **Autoconf**: Configure script development and maintenance
3. **Cross-Compilation**: DevKit creation and toolchain management
4. **Platform-Specific Code**: Windows, macOS, Linux build differences

## Related Links

- [OpenJDK Profile](https://openjdk.org/census#ihse)
- [JBS Issues by Magnus Ihse Bursie](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20ihse)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=ihse@openjdk.org)

## Technical Notes

### Build System Architecture

The JDK build system follows a layered architecture:

```
configure (autoconf)
    |
    v
spec.gmk (configuration output)
    |
    v
Main.gmk -> Init.gmk -> PreInit.gmk
    |
    v
Makefiles (module-specific)
    |
    v
Native/Java compilation rules
```

### Key Makefile Patterns

```makefile
# Typical SetupExecute pattern
$(eval $(call SetupExecute, $1, \
    INFO := $$(info Running $1), \
    COMMAND := $(COMMAND), \
    OUTPUT_FILE := $(OUTPUT_FILE), \
))
```

### Static Build Considerations

Windows static builds require special handling:
- No DllMain entry points
- JNI_OnLoad for library initialization
- Proper relauncher executables
- Static library linking order