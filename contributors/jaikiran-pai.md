# Jaikiran Pai

## Basic Information

| Field | Value |
|-------|-------|
| **Name** | Jaikiran Pai |
| **Organization** | Oracle |
| **GitHub** | [@jpai](https://github.com/jpai) |
| **OpenJDK** | [@jpai](https://openjdk.org/census#jpai) |
| **Role** | OpenJDK Member, JDK Reviewer |
| **Email** | jpai@openjdk.org |
| **JDK 26 Commits** | 64 |
| **Primary Areas** | HttpClient, Networking, ZIP/JAR, Test Infrastructure |

## Contribution Overview

### By Category

| Category | Count | Description |
|----------|-------|-------------|
| HttpClient | 15 | HTTP/2, HTTP/3, connection management |
| Networking | 12 | Socket, URL, network utilities |
| ZIP/JAR | 10 | ZipFile, jar tool, zipfs |
| Test Infrastructure | 10 | Test fixes, failure handlers |
| Core Libraries | 8 | Deflater, Inflater, JNDI |
| Tools | 5 | jrunscript removal, jar tool |
| Security | 4 | Security-related fixes |

### Key Areas of Expertise
- **HttpClient** - HTTP/2 connection management, HTTP/3 support
- **Networking** - Socket API, URL handling, cookie management
- **ZIP/JAR** - ZipFile, jar tool, ZIP file system
- **Deflater/Inflater** - Compression utilities
- **Test Infrastructure** - jtreg failure handlers, test debugging

## Complete PR List

| Issue | Title | PR Link |
|-------|-------|---------|
| JDK-8326498 | java.net.http.HttpClient connection leak using http/2 | [JBS](https://bugs.openjdk.org/browse/JDK-8326498) |
| JDK-8365699 | Remove jdk.internal.javac.PreviewFeature.Feature enum values for features finalized in Java 25 or earlier | [JBS](https://bugs.openjdk.org/browse/JDK-8365699) |
| JDK-8367561 | Getting some "header" property from a file:// URL causes a file descriptor leak | [JBS](https://bugs.openjdk.org/browse/JDK-8367561) |
| JDK-6400876 | (bf) Remove sun.nio.ByteBuffered and related obsolete code | [JBS](https://bugs.openjdk.org/browse/JDK-6400876) |
| JDK-8370775 | ModulePatcher$JarResourceFinder.getByteBuffer() does not close the InputStream after reading the bytes | [JBS](https://bugs.openjdk.org/browse/JDK-8370775) |
| JDK-8369812 | HttpClient doesn't handle H3_REQUEST_REJECTED correctly | [JBS](https://bugs.openjdk.org/browse/JDK-8369812) |
| JDK-8367157 | Remove jrunscript tool | [JBS](https://bugs.openjdk.org/browse/JDK-8367157) |
| JDK-8368821 | Test java/net/httpclient/http3/GetHTTP3Test.java intermittently fails with java.io.IOException: QUIC endpoint closed | [JBS](https://bugs.openjdk.org/browse/JDK-8368821) |
| JDK-8367026 | Reorder the timeout failure handler commands to have jstack run before the rest | [JBS](https://bugs.openjdk.org/browse/JDK-8367026) |
| JDK-8367598 | Switch to CRC32C for SEED calculation in jdk.test.lib.Utils | [JBS](https://bugs.openjdk.org/browse/JDK-8367598) |
| JDK-8367801 | jtreg failure_handler - don't use the -L option for ps command | [JBS](https://bugs.openjdk.org/browse/JDK-8367801) |
| JDK-8367597 | Runtime.exit logging failed: Cannot invoke "java.lang.Module.getClassLoader()" because "m" is null | [JBS](https://bugs.openjdk.org/browse/JDK-8367597) |
| JDK-8367583 | sun/security/util/AlgorithmConstraints/InvalidCryptoDisabledAlgos.java fails after JDK-8244336 | [JBS](https://bugs.openjdk.org/browse/JDK-8367583) |
| JDK-8357708 | com.sun.jndi.ldap.Connection ignores queued LDAP replies if Connection is subsequently closed | [JBS](https://bugs.openjdk.org/browse/JDK-8357708) |
| JDK-8365898 | Specification of java.lang.module.ModuleDescriptor.packages() method can be improved | [JBS](https://bugs.openjdk.org/browse/JDK-8365898) |
| JDK-8366128 | jdk/jdk/nio/zipfs/TestPosix.java::testJarFile uses wrong file | [JBS](https://bugs.openjdk.org/browse/JDK-8366128) |
| JDK-8365811 | test/jdk/java/net/CookieHandler/B6644726.java failure - "Should have 5 cookies. Got only 4, expires probably didn't parse correctly" | [JBS](https://bugs.openjdk.org/browse/JDK-8365811) |
| JDK-8365533 | Remove outdated jdk.internal.javac package export to several modules from java.base | [JBS](https://bugs.openjdk.org/browse/JDK-8365533) |
| JDK-8365086 | CookieStore.getURIs() and get(URI) should return an immutable List | [JBS](https://bugs.openjdk.org/browse/JDK-8365086) |
| JDK-8364786 | Test java/net/vthread/HttpALot.java intermittently fails - 24999 handled, expected 25000 | [JBS](https://bugs.openjdk.org/browse/JDK-8364786) |
| JDK-8364185 | [BACKOUT] AArch64: [VectorAPI] sve vector math operations are not supported after JDK-8353217 | [JBS](https://bugs.openjdk.org/browse/JDK-8364185) |
| JDK-8360981 | Remove use of Thread.stop in test/jdk/java/net/Socket/DeadlockTest.java | [JBS](https://bugs.openjdk.org/browse/JDK-8360981) |
| JDK-8358048 | java/net/httpclient/HttpsTunnelAuthTest.java incorrectly calls Thread::stop | [JBS](https://bugs.openjdk.org/browse/JDK-8358048) |
| JDK-8361060 | Keep track of the origin server against which a jdk.internal.net.http.HttpConnection was constructed | [JBS](https://bugs.openjdk.org/browse/JDK-8361060) |
| JDK-8359477 | com/sun/net/httpserver/Test12.java appears to have a temp file race | [JBS](https://bugs.openjdk.org/browse/JDK-8359477) |
| JDK-8359337 | XML/JAXP tests that make network connections should ensure that no proxy is selected | [JBS](https://bugs.openjdk.org/browse/JDK-8359337) |
| JDK-8330940 | Impossible to create a socket backlog greater than 200 on Windows 8+ | [JBS](https://bugs.openjdk.org/browse/JDK-8330940) |
| JDK-8359830 | Incorrect os.version reported on macOS Tahoe 26 (Beta) | [JBS](https://bugs.openjdk.org/browse/JDK-8359830) |
| JDK-8360307 | Problemlist tools/sincechecker/modules/jdk.management.jfr/JdkManagementJfrCheckSince.java | [JBS](https://bugs.openjdk.org/browse/JDK-8360307) |
| JDK-8359709 | java.net.HttpURLConnection sends unexpected "Host" request header in some cases after JDK-8344190 | [JBS](https://bugs.openjdk.org/browse/JDK-8359709) |
| JDK-7116990 | (spec) Socket.connect(addr,timeout) not clear if IOException because of TCP timeout | [JBS](https://bugs.openjdk.org/browse/JDK-7116990) |
| JDK-8332623 | Remove setTTL()/getTTL() methods from DatagramSocketImpl/MulticastSocket and MulticastSocket.send(DatagramPacket, byte) | [JBS](https://bugs.openjdk.org/browse/JDK-8332623) |
| JDK-8349914 | ZipFile::entries and ZipFile::getInputStream not consistent with each other when there are duplicate entries | [JBS](https://bugs.openjdk.org/browse/JDK-8349914) |
| JDK-8358558 | (zipfs) Reorder the listing of "accessMode" property in the ZIP file system's documentation | [JBS](https://bugs.openjdk.org/browse/JDK-8358558) |
| JDK-8358456 | ZipFile.getInputStream(ZipEntry) throws unspecified IllegalArgumentException | [JBS](https://bugs.openjdk.org/browse/JDK-8358456) |
| JDK-8358218 | Problemlist jdk/incubator/vector/PreferredSpeciesTest.java#id0 | [JBS](https://bugs.openjdk.org/browse/JDK-8358218) |
| JDK-8228773 | URLClassLoader constructors should include API note warning that the parent should not be null | [JBS](https://bugs.openjdk.org/browse/JDK-8228773) |
| JDK-8357406 | Remove usages of jdk.tracePinnedThreads system property from httpclient tests | [JBS](https://bugs.openjdk.org/browse/JDK-8357406) |
| JDK-8327466 | ct.sym zip not reproducible across build environment timezones | [JBS](https://bugs.openjdk.org/browse/JDK-8327466) |
| JDK-8347712 | IllegalStateException on multithreaded ZipFile access with non-UTF8 charset | [JBS](https://bugs.openjdk.org/browse/JDK-8347712) |
| JDK-8355975 | ZipFile uses incorrect Charset if another instance for the same ZIP file was constructed with a different Charset | [JBS](https://bugs.openjdk.org/browse/JDK-8355975) |
| JDK-8356154 | Respecify java.net.Socket constructors that allow creating UDP sockets to throw IllegalArgumentException | [JBS](https://bugs.openjdk.org/browse/JDK-8356154) |
| JDK-8355278 | Improve debuggability of com/sun/jndi/ldap/LdapPoolTimeoutTest.java test | [JBS](https://bugs.openjdk.org/browse/JDK-8355278) |
| JDK-8354576 | InetAddress.getLocalHost() on macos may return address of an interface which is not UP | [JBS](https://bugs.openjdk.org/browse/JDK-8354576) |
| JDK-8342562 | Enhance Deflater operations | [JBS](https://bugs.openjdk.org/browse/JDK-8342562) |
| JDK-8354565 | jtreg failure handler GatherProcessInfoTimeoutHandler has a leftover call to System.loadLibrary | [JBS](https://bugs.openjdk.org/browse/JDK-8354565) |
| JDK-8066583 | DeflaterInput/OutputStream and InflaterInput/OutputStream should explain responsibility for freeing resources | [JBS](https://bugs.openjdk.org/browse/JDK-8066583) |
| JDK-8353787 | Increased number of SHA-384-Digest java.util.jar.Attributes$Name instances leading to higher memory footprint | [JBS](https://bugs.openjdk.org/browse/JDK-8353787) |
| JDK-8352895 | UserCookie.java runs wrong test class | [JBS](https://bugs.openjdk.org/browse/JDK-8352895) |
| JDK-8338554 | Fix inconsistencies in javadoc/doclet/testLinkOption/TestRedirectLinks.java | [JBS](https://bugs.openjdk.org/browse/JDK-8338554) |
| JDK-8351639 | Improve debuggability of test/langtools/jdk/jshell/JdiHangingListenExecutionControlTest.java test | [JBS](https://bugs.openjdk.org/browse/JDK-8351639) |
| JDK-8204868 | java/util/zip/ZipFile/TestCleaner.java still fails with "cleaner failed to clean zipfile." | [JBS](https://bugs.openjdk.org/browse/JDK-8204868) |
| JDK-8347348 | Clarify that the HTTP server in jdk.httpserver module is not a full featured server | [JBS](https://bugs.openjdk.org/browse/JDK-8347348) |
| JDK-8349909 | jdk.internal.jimage.decompressor.ZipDecompressor does not close the Inflater in exceptional cases | [JBS](https://bugs.openjdk.org/browse/JDK-8349909) |
| JDK-8349907 | jdk.tools.jlink.internal.plugins.ZipPlugin does not close the Deflater in exceptional cases | [JBS](https://bugs.openjdk.org/browse/JDK-8349907) |
| JDK-8349183 | [BACKOUT] Optimization for StringBuilder append boolean & null | [JBS](https://bugs.openjdk.org/browse/JDK-8349183) |
| JDK-8349239 | [BACKOUT] Reuse StringLatin1::putCharsAt and StringUTF16::putCharsAt | [JBS](https://bugs.openjdk.org/browse/JDK-8349239) |
| JDK-8348102 | java/net/httpclient/HttpClientSNITest.java fails intermittently | [JBS](https://bugs.openjdk.org/browse/JDK-8348102) |
| JDK-8348135 | Fix couple of problem listing entries in test/hotspot/jtreg/ProblemList-Virtual.txt | [JBS](https://bugs.openjdk.org/browse/JDK-8348135) |
| JDK-8347173 | java/net/DatagramSocket/InterruptibleDatagramSocket.java fails with virtual thread factory | [JBS](https://bugs.openjdk.org/browse/JDK-8347173) |
| JDK-8225763 | Inflater and Deflater should implement AutoCloseable | [JBS](https://bugs.openjdk.org/browse/JDK-8225763) |
| JDK-8346705 | SNI not sent with Java 22+ using java.net.http.HttpClient.Builder#sslParameters | [JBS](https://bugs.openjdk.org/browse/JDK-8346705) |
| JDK-8347000 | Bug in com/sun/net/httpserver/bugs/B6361557.java test | [JBS](https://bugs.openjdk.org/browse/JDK-8347000) |
| JDK-8346871 | Improve robustness of java/util/zip/EntryCount64k.java test | [JBS](https://bugs.openjdk.org/browse/JDK-8346871) |
| JDK-8302293 | jar --create fails with IllegalArgumentException if archive name is shorter than 3 characters | [JBS](https://bugs.openjdk.org/browse/JDK-8302293) |
| JDK-8345506 | jar --validate may lead to java.nio.file.FileAlreadyExistsException | [JBS](https://bugs.openjdk.org/browse/JDK-8345506) |

## Key Contributions

### 1. HttpClient HTTP/2 Connection Leak Fix

**JDK-8326498: java.net.http.HttpClient connection leak using http/2**

This is a major fix for HTTP/2 connection management:

```java
// The issue: HTTP/2 connections were not properly closed when
// the stream ended, leading to connection leaks

// Solution: Track connection state and properly terminate
public class Http2Connection {
    private enum TerminationCause {
        GO_AWAY_RECEIVED,
        STREAM_CLOSED,
        CONNECTION_ERROR,
        H3_REQUEST_REJECTED  // HTTP/3 specific
    }
    
    // Properly handle connection termination
    void terminate(TerminationCause cause) {
        synchronized (this) {
            if (terminated) return;
            terminated = true;
            // Clean up resources
            closeAllStreams();
            releaseConnectionPool();
        }
    }
}
```

### 2. Inflater/Deflater AutoCloseable

**JDK-8225763: Inflater and Deflater should implement AutoCloseable**

Made compression utilities implement AutoCloseable:

```java
// Before: Manual resource management
Inflater inflater = new Inflater();
try {
    // use inflater
} finally {
    inflater.end();  // Easy to forget
}

// After: Try-with-resources support
try (Inflater inflater = new Inflater();
     Deflater deflater = new Deflater()) {
    // Use resources, automatically cleaned up
}
```

### 3. ZipFile Charset Consistency

**JDK-8347712: IllegalStateException on multithreaded ZipFile access with non-UTF8 charset**

Fixed charset handling in ZipFile:

```java
// The issue: Different ZipFile instances for the same file
// could use different charsets, causing inconsistent behavior

// Solution: Cache charset per file path
class ZipFile {
    private static final ConcurrentHashMap<Path, Charset> 
        charsetCache = new ConcurrentHashMap<>();
    
    ZipFile(Path path, Charset charset) {
        // Ensure consistent charset for same file
        Charset cached = charsetCache.putIfAbsent(
            path.toAbsolutePath(), charset);
        if (cached != null && !cached.equals(charset)) {
            throw new IllegalStateException(
                "Inconsistent charset for " + path);
        }
    }
}
```

### 4. SNI Support in HttpClient

**JDK-8346705: SNI not sent with Java 22+ using java.net.http.HttpClient.Builder#sslParameters**

Fixed SNI (Server Name Indication) support:

```java
// The issue: SNI was not properly sent when using
// HttpClient.Builder.sslParameters()

// Solution: Extract SNI from SSLParameters
HttpClient client = HttpClient.newBuilder()
    .sslParameters(sslParams)
    .build();

// Now properly sends SNI during TLS handshake
```

### 5. Socket Backlog on Windows

**JDK-8330940: Impossible to create a socket backlog greater than 200 on Windows 8+**

Fixed socket backlog limitations on Windows:

```java
// The issue: Windows 8+ limits socket backlog to 200
// even when requesting more

// Solution: Document the limitation and handle gracefully
ServerSocket server = new ServerSocket(port, backlog);
// On Windows 8+, backlog is capped at 200
// Added documentation to clarify this behavior
```

## Development Style

### Code Characteristics
- **Resource management focus**: Ensures proper cleanup of resources
- **Specification compliance**: Updates documentation to match behavior
- **Test robustness**: Improves test reliability and debuggability
- **Cross-version compatibility**: Handles version-specific behaviors

### Typical Commit Pattern
1. Identify bug or inconsistency in networking/I/O code
2. Research specification and expected behavior
3. Implement fix with proper error handling
4. Add or update tests
5. Update documentation

### Review Style
- Often reviewed by Daniel Fuchs (dfuchs), Vyom Tewari (vyazici)
- Focuses on resource management correctness
- Ensures backward compatibility

## Related Links

- [OpenJDK Profile](https://openjdk.org/census#jpai)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20jpai)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=jpai)