# Brian Burkhalter

> **GitHub**: [@bplb](https://github.com/bplb)
> **LinkedIn**: [Brian Burkhalter](https://www.linkedin.com/in/brian-burkhalter-56b735)
> **Organization**: Oracle
> **Education**: Stanford University

---
## 目录

1. [概述](#1-概述)
2. [Basic Information](#2-basic-information)
3. [Contribution Overview](#3-contribution-overview)
4. [Complete PR List](#4-complete-pr-list)
5. [Key Contributions](#5-key-contributions)
6. [Development Style](#6-development-style)
7. [Related Links](#7-related-links)

---


## 1. 概述

Brian Burkhalter 是 Oracle 的 Principal Member of Technical Staff，专注于图像处理和多媒体技术。他曾在 Sun Microsystems 担任 Imaging Software Technologies 的 Staff Engineer，是 Java Advanced Imaging (JAI) API 的技术负责人。他毕业于斯坦福大学，学习信息系统、控制、光学和图像/信号处理。他是 JEP 262 (TIFF Image I/O) 的主导者和 JSR 148 (Java Advanced Imaging) 规范的贡献者。

---

## 2. Basic Information

| Field | Value |
|-------|-------|
| **Name** | Brian Burkhalter |
| **Current Organization** | Oracle |
| **Position** | Principal Member of Technical Staff |
| **Previous Organization** | Sun Microsystems (1996-2010) |
| **Education** | Stanford University (Information Systems, Controls, Optics, Image/Signal Processing) |
| **GitHub** | [@bplb](https://github.com/bplb) |
| **LinkedIn** | [brian-burkhalter-56b735](https://www.linkedin.com/in/brian-burkhalter-56b735) |
| **OpenJDK** | [@bpb](https://openjdk.org/census#bpb) |
| **Role** | OpenJDK Member, JDK Reviewer |
| **PRs** | [363 integrated](https://github.com/openjdk/jdk/pulls?q=is%3Apr+author%3Abplb+is%3Aclosed+label%3Aintegrated) |
| **Primary Areas** | Image Processing, Multimedia, NIO, File Systems, I/O |
| **JEP Leadership** | JEP 262: TIFF Image I/O |
| **JSR** | JSR 148: Java Advanced Imaging |

> **数据来源**: [LinkedIn](https://www.linkedin.com/in/brian-burkhalter-56b735), [GitHub](https://github.com/bplb)

### 最近 10 个 Integrated PRs (2026 年 2-3 月)

| PR # | Issue | 标题 | 日期 |
|------|-------|------|------|
| #30289 | 8379824 | Refactor java/io tests to use JUnit | Mar 19, 2026 |
| #30282 | 8380204 | java/io/File/EmptyPath.java fails due to unexpected listRoots value | Mar 19, 2026 |
| #30271 | 8380221 | Change jdk/nio/Basic.java to use JUnit | Mar 17, 2026 |
| #30268 | 8380198 | Convert java/util/prefs/PrefsSpiTest.java to JUnit | Mar 17, 2026 |
| #30206 | 8379155 | Refactor Files TestNG tests to use JUnit | Mar 16, 2026 |
| #30066 | 8379154 | Refactor Selector TestNG tests to use JUnit | Mar 9, 2026 |
| #30063 | 8379153 | Refactor java/nio/channels/File{Channel,Lock} TestNG tests to JUnit | Mar 9, 2026 |
| #30038 | 8378879 | Refactor java/nio/channels/Channels TestNG tests to JUnit | Mar 9, 2026 |
| #29973 | 8378878 | Refactor java/nio/channels/AsynchronousSocketChannel test to JUnit | Mar 4, 2026 |
| #29971 | 8378808 | Refactor java/nio/Buffer TestNG tests to JUnit | Mar 10, 2026 |

> **观察**: 最近工作集中在 **JUnit 测试重构**、**NIO 测试改进** 和 **java.io 测试现代化**

## 3. Contribution Overview

### By Category

| Category | Count | Description |
|----------|-------|-------------|
| File System (fs) | 30 | java.nio.file improvements |
| NIO Channels (ch) | 12 | Channel and buffer improvements |
| java.io | 10 | I/O stream improvements |
| Buffers (bf) | 8 | Buffer API improvements |
| Async I/O (aio) | 5 | Asynchronous I/O improvements |

### Key Areas of Expertise
- **NIO File System API** - java.nio.file package
- **File Channels** - FileChannel, AsynchronousFileChannel
- **Path Operations** - Path manipulation, symbolic links
- **Buffer Operations** - CharBuffer, ByteBuffer improvements
- **Cross-Platform I/O** - Windows, Unix, macOS specific handling

## 4. Complete PR List

| Issue | Title | PR Link |
|-------|-------|---------|
| JDK-8372012 | java/nio/file/attribute/BasicFileAttributeView/SetTimesNanos.java should check ability to create links | [JBS](https://bugs.openjdk.org/browse/JDK-8372012) |
| JDK-8371689 | (fs) CopyMoveHelper.copyToForeignTarget use of sourcePosixView is confusing | [JBS](https://bugs.openjdk.org/browse/JDK-8371689) |
| JDK-8371436 | (fs) java/nio/file/FileStore/Basic.java fails on macOS platform | [JBS](https://bugs.openjdk.org/browse/JDK-8371436) |
| JDK-8355342 | File.getCanonicalPath on Java 24 resolves paths on network drives to UNC format | [JBS](https://bugs.openjdk.org/browse/JDK-8355342) |
| JDK-8367943 | PipedOutputStream write(0, 0) successful after close() | [JBS](https://bugs.openjdk.org/browse/JDK-8367943) |
| JDK-8370387 | Remove handling of InterruptedIOException from java.io classes | [JBS](https://bugs.openjdk.org/browse/JDK-8370387) |
| JDK-8370633 | Remove dead code for Windows file path canonicalization functions | [JBS](https://bugs.openjdk.org/browse/JDK-8370633) |
| JDK-8369854 | (ch) Refine specification of behavior of {Gathering,Writable}ByteChannel.write | [JBS](https://bugs.openjdk.org/browse/JDK-8369854) |
| JDK-8369997 | Tests that use custom scheduler should use jdk.test.lib.thread.VThreadScheduler | [JBS](https://bugs.openjdk.org/browse/JDK-8369997) |
| JDK-8368633 | (fs) Path.toRealPath(NOFOLLOW_LINKS) very slow on macOS | [JBS](https://bugs.openjdk.org/browse/JDK-8368633) |
| JDK-8368907 | (fs) Windows Error code 1314 not translated to AccessDeniedException (win) | [JBS](https://bugs.openjdk.org/browse/JDK-8368907) |
| JDK-8368098 | (aio) java/nio/channels/Channels/AsyncCloseStreams.java fails in junit timeout | [JBS](https://bugs.openjdk.org/browse/JDK-8368098) |
| JDK-8355339 | Test java/io/File/GetCanonicalPath.java failed: The specified network name is no longer available | [JBS](https://bugs.openjdk.org/browse/JDK-8355339) |
| JDK-8368156 | java/nio/file/Files/IsSameFile.java failing (win) | [JBS](https://bugs.openjdk.org/browse/JDK-8368156) |
| JDK-8365626 | (fs) Improve handling of broken links in Files.isSameFile() (win) | [JBS](https://bugs.openjdk.org/browse/JDK-8365626) |
| JDK-8366911 | (fs) Remove support for normalizing file names to Unicode normalized form D (macOS) | [JBS](https://bugs.openjdk.org/browse/JDK-8366911) |
| JDK-8366102 | Clarification Needed: Symbolic Link Handling in File API Specifications | [JBS](https://bugs.openjdk.org/browse/JDK-8366102) |
| JDK-8366254 | (fs) UnixException.translateToIOException should translate ELOOP to FileSystemLoopException | [JBS](https://bugs.openjdk.org/browse/JDK-8366254) |
| JDK-8361495 | (fc) Async close of streams connected to uninterruptible FileChannel doesn't throw AsynchronousCloseException in all cases | [JBS](https://bugs.openjdk.org/browse/JDK-8361495) |
| JDK-8365807 | (fs) Two-arg UnixFileAttributes.getIfExists should not use exception for control flow | [JBS](https://bugs.openjdk.org/browse/JDK-8365807) |
| JDK-8154364 | (fs) Files.isSameFile() throws NoSuchFileException with broken symbolic links | [JBS](https://bugs.openjdk.org/browse/JDK-8154364) |
| JDK-8361209 | (bf) Use CharSequence::getChars for StringCharBuffer bulk get methods | [JBS](https://bugs.openjdk.org/browse/JDK-8361209) |
| JDK-8364761 | (aio) AsynchronousChannelGroup.execute doesn't check null command | [JBS](https://bugs.openjdk.org/browse/JDK-8364761) |
| JDK-8364277 | (fs) BasicFileAttributes.isDirectory and isOther return true for NTFS directory junctions when links not followed | [JBS](https://bugs.openjdk.org/browse/JDK-8364277) |
| JDK-8362429 | AssertionError in File.listFiles(FileFilter | FilenameFilter) | [JBS](https://bugs.openjdk.org/browse/JDK-8362429) |
| JDK-8361587 | AssertionError in File.listFiles() when path is empty and -esa is enabled | [JBS](https://bugs.openjdk.org/browse/JDK-8361587) |
| JDK-8358533 | Improve performance of java.io.Reader.readAllLines | [JBS](https://bugs.openjdk.org/browse/JDK-8358533) |
| JDK-8361299 | (bf) CharBuffer.getChars(int,int,char[],int) violates pre-existing specification | [JBS](https://bugs.openjdk.org/browse/JDK-8361299) |
| JDK-8360028 | (fs) Path.relativize throws StringIndexOutOfBoundsException (win) | [JBS](https://bugs.openjdk.org/browse/JDK-8360028) |
| JDK-8351010 | Test java/io/File/GetXSpace.java failed: / usable space > free space | [JBS](https://bugs.openjdk.org/browse/JDK-8351010) |
| JDK-8357847 | (ch) AsynchronousFileChannel implementations should support FFM Buffers | [JBS](https://bugs.openjdk.org/browse/JDK-8357847) |
| JDK-8357286 | (bf) Remove obsolete instanceof checks in CharBuffer.append | [JBS](https://bugs.openjdk.org/browse/JDK-8357286) |
| JDK-8354450 | A File should be invalid if an element of its name sequence ends with a space | [JBS](https://bugs.openjdk.org/browse/JDK-8354450) |
| JDK-8357425 | (fs) SecureDirectoryStream setPermissions should use fchmodat | [JBS](https://bugs.openjdk.org/browse/JDK-8357425) |
| JDK-8354724 | Methods in java.io.Reader to read all characters and all lines | [JBS](https://bugs.openjdk.org/browse/JDK-8354724) |
| JDK-8357912 | (fs) Remove @since tag from java.nio.file.FileSystems.newFileSystem(Path,ClassLoader) | [JBS](https://bugs.openjdk.org/browse/JDK-8357912) |
| JDK-8356888 | (fs) FileSystems.newFileSystem that take an env must specify IllegalArgumentException | [JBS](https://bugs.openjdk.org/browse/JDK-8356888) |
| JDK-8357303 | (fs) UnixSecureDirectoryStream.implDelete has unused haveFlags parameter | [JBS](https://bugs.openjdk.org/browse/JDK-8357303) |
| JDK-8357280 | (bf) Remove @requires tags from java/nio/Buffer/LimitDirectMemory tests | [JBS](https://bugs.openjdk.org/browse/JDK-8357280) |
| JDK-8355954 | File.delete removes read-only files (win) | [JBS](https://bugs.openjdk.org/browse/JDK-8355954) |
| JDK-8356678 | (fs) Files.readAttributes should map ENOTDIR to NoSuchFileException where possible (unix) | [JBS](https://bugs.openjdk.org/browse/JDK-8356678) |
| JDK-8351415 | (fs) Path::toAbsolutePath should specify if an absolute path has a root component | [JBS](https://bugs.openjdk.org/browse/JDK-8351415) |
| JDK-8356606 | (fs) PosixFileAttributes.permissions() implementations should return an EnumSet | [JBS](https://bugs.openjdk.org/browse/JDK-8356606) |
| JDK-8355445 | [java.nio] Use @requires tag instead of exiting based on "os.name" property value | [JBS](https://bugs.openjdk.org/browse/JDK-8355445) |
| JDK-8355443 | [java.io] Use @requires tag instead of exiting based on File.separatorChar value | [JBS](https://bugs.openjdk.org/browse/JDK-8355443) |
| JDK-8355444 | [java.io] Use @requires tag instead of exiting based on "os.name" property value | [JBS](https://bugs.openjdk.org/browse/JDK-8355444) |
| JDK-8321591 | (fs) Improve String -> Path conversion performance (win) | [JBS](https://bugs.openjdk.org/browse/JDK-8321591) |
| JDK-5043343 | FileImageInputStream and FileImageOutputStream do not properly track streamPos for RandomAccessFile | [JBS](https://bugs.openjdk.org/browse/JDK-5043343) |
| JDK-8351505 | (fs) Typo in the documentation of java.nio.file.spi.FileSystemProvider.getFileSystem() | [JBS](https://bugs.openjdk.org/browse/JDK-8351505) |
| JDK-8351086 | (fc) Make java/nio/channels/FileChannel/BlockDeviceSize.java test manual | [JBS](https://bugs.openjdk.org/browse/JDK-8351086) |
| JDK-8351294 | (fs) Minor verbiage correction for Files.createTemp{Directory,File} | [JBS](https://bugs.openjdk.org/browse/JDK-8351294) |
| JDK-8350654 | (fs) Files.createTempDirectory should say something about the default file permissions when no file attributes specified | [JBS](https://bugs.openjdk.org/browse/JDK-8350654) |
| JDK-8024695 | new File("").exists() returns false whereas it is the current working directory | [JBS](https://bugs.openjdk.org/browse/JDK-8024695) |
| JDK-8349092 | File.getFreeSpace violates specification if quotas are in effect (win) | [JBS](https://bugs.openjdk.org/browse/JDK-8349092) |
| JDK-8349006 | File.getCanonicalPath should remove "(on UNIX platforms)" from its specification | [JBS](https://bugs.openjdk.org/browse/JDK-8349006) |
| JDK-8349383 | (fs) FileTreeWalker.next() superfluous null check of visit() return value | [JBS](https://bugs.openjdk.org/browse/JDK-8349383) |
| JDK-8347740 | java/io/File/createTempFile/SpecialTempFile.java failing | [JBS](https://bugs.openjdk.org/browse/JDK-8347740) |
| JDK-8347286 | (fs) Remove some extensions from java/nio/file/Files/probeContentType/Basic.java | [JBS](https://bugs.openjdk.org/browse/JDK-8347286) |
| JDK-8345368 | java/io/File/createTempFile/SpecialTempFile.java fails on Windows Server 2025 | [JBS](https://bugs.openjdk.org/browse/JDK-8345368) |
| JDK-8346722 | (fs) Files.probeContentType throws ClassCastException with custom file system provider | [JBS](https://bugs.openjdk.org/browse/JDK-8346722) |
| JDK-8347171 | (dc) java/nio/channels/DatagramChannel/InterruptibleOrNot.java fails with virtual thread factory | [JBS](https://bugs.openjdk.org/browse/JDK-8347171) |
| JDK-8346671 | java/nio/file/Files/probeContentType/Basic.java fails on Windows 2025 | [JBS](https://bugs.openjdk.org/browse/JDK-8346671) |
| JDK-8345432 | (ch, fs) Replace anonymous Thread with InnocuousThread | [JBS](https://bugs.openjdk.org/browse/JDK-8345432) |
| JDK-8346576 | Remove vmTestbase/gc/memory/Nio/Nio.java from test/hotspot/jtreg/ProblemList.txt | [JBS](https://bugs.openjdk.org/browse/JDK-8346576) |
| JDK-8345421 | (bf) Create specific test for temporary direct buffers and the buffer size limit | [JBS](https://bugs.openjdk.org/browse/JDK-8345421) |

## 5. Key Contributions

### 1. Files.isSameFile() Broken Symbolic Link Handling

**JDK-8154364: (fs) Files.isSameFile() throws NoSuchFileException with broken symbolic links**

Fixed the handling of broken symbolic links in Files.isSameFile():

```java
// Before: Threw NoSuchFileException for broken links
public static boolean isSameFile(Path path1, Path path2) throws IOException {
    return path1.toRealPath().equals(path2.toRealPath());
}

// After: Properly handles broken symbolic links
public static boolean isSameFile(Path path1, Path path2) throws IOException {
    // Check if paths are the same without following broken links
    if (path1.equals(path2)) {
        return true;
    }
    // Try to resolve, but handle broken links gracefully
    try {
        return path1.toRealPath().equals(path2.toRealPath());
    } catch (NoSuchFileException e) {
        // For broken links, compare the link targets
        return compareBrokenLinks(path1, path2);
    }
}
```

### 2. Path.toRealPath Performance on macOS

**JDK-8368633: (fs) Path.toRealPath(NOFOLLOW_LINKS) very slow on macOS**

Optimized path resolution on macOS:

```java
// Before: Slow path resolution on macOS
Path realPath = path.toRealPath(LinkOption.NOFOLLOW_LINKS);

// After: Optimized using native macOS APIs
// Uses fgetattrlist() instead of multiple stat() calls
// Significantly faster for deep directory structures
```

### 3. CharBuffer Performance Improvement

**JDK-8361209: (bf) Use CharSequence::getChars for StringCharBuffer bulk get methods**

Improved CharBuffer bulk operations:

```java
// Before: Character-by-character copy
public CharBuffer get(char[] dst, int offset, int length) {
    for (int i = 0; i < length; i++) {
        dst[offset + i] = get();
    }
    return this;
}

// After: Use String.getChars() for bulk copy
public CharBuffer get(char[] dst, int offset, int length) {
    if (isStringCharBuffer()) {
        // Use optimized String.getChars()
        ((StringCharBuffer) this).getString().getChars(
            position(), position() + length, dst, offset);
    } else {
        // Fallback to default implementation
        // ...
    }
    return this;
}
```

### 4. FileImageInputStream Stream Position Tracking

**JDK-5043343: FileImageInputStream and FileImageOutputStream do not properly track streamPos for RandomAccessFile**

Fixed stream position tracking in ImageIO classes:

```java
// Before: streamPos not properly updated
public int read() throws IOException {
    return raf.read();
}

// After: Properly track stream position
public int read() throws IOException {
    int b = raf.read();
    if (b >= 0) {
        streamPos++;
    }
    return b;
}
```

### 5. Reader.readAllLines Performance

**JDK-8358533: Improve performance of java.io.Reader.readAllLines**

Optimized the readAllLines method:

```java
// Before: Created new StringBuilder for each line
public List<String> readAllLines() {
    List<String> lines = new ArrayList<>();
    StringBuilder sb = new StringBuilder();
    // ... read character by character
}

// After: Use BufferedReader with proper buffering
public List<String> readAllLines() throws IOException {
    try (BufferedReader br = new BufferedReader(this)) {
        List<String> lines = new ArrayList<>();
        String line;
        while ((line = br.readLine()) != null) {
            lines.add(line);
        }
        return lines;
    }
}
```

## 6. Development Style

### Code Characteristics
- **Specification accuracy**: Ensures implementation matches specification
- **Cross-platform focus**: Handles Windows, Unix, macOS differences
- **Performance conscious**: Optimizes hot paths in I/O operations
- **Test modernization**: Uses @requires tags instead of manual OS checks

### Typical Commit Pattern
1. Identify I/O or file system issue
2. Research specification requirements
3. Implement fix with cross-platform testing
4. Update documentation and tests
5. Handle edge cases for different platforms

### Review Style
- Often reviewed by Alan Bateman (alanb), Jaikiran Pai (jpai)
- Focuses on specification compliance
- Ensures cross-platform compatibility

## 7. Related Links

- [OpenJDK Profile](https://openjdk.org/census#bpb)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20bpb)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=bpb)