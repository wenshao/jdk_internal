# Volkan Yazici

## Basic Information

| Field | Value |
|-------|-------|
| **Name** | Volkan Yazici |
| **Organization** | Oracle |
| **GitHub** | [@vyazici](https://github.com/vyazici) |
| **OpenJDK** | [@vyazici](https://openjdk.org/census#vyazici) |
| **Role** | JDK Reviewer |
| **Email** | vyazici@openjdk.org |
| **Primary Areas** | HttpClient API, Networking, Core Libraries |

## Contribution Overview

Volkan Yazici is a key contributor to the Java HttpClient API and networking infrastructure. His work in JDK 26 focuses on enhancing HttpClient functionality, improving API usability, and cleaning up legacy code.

### Contribution Categories

| Category | Count | Description |
|----------|-------|-------------|
| HttpClient | 20 | HTTP client API improvements |
| Networking | 12 | Socket and network infrastructure |
| Core Libraries | 8 | String, encoding, and utility improvements |
| Testing | 5 | Test improvements and fixes |
| Documentation | 4 | Documentation enhancements |

## Complete PR List

| Issue | Title | PR Link |
|-------|-------|---------|
| JDK-8328919 | Add BodyHandlers / BodySubscribers methods to handle excessive server input | [JBS](https://bugs.openjdk.org/browse/JDK-8328919) |
| JDK-8329829 | HttpClient: Add a BodyPublishers.ofFileChannel method | [JBS](https://bugs.openjdk.org/browse/JDK-8329829) |
| JDK-8343074 | test/jdk/com/sun/net/httpserver/docs/test1/largefile.txt could be generated | [JBS](https://bugs.openjdk.org/browse/JDK-8343074) |
| JDK-8345625 | Better HTTP connections | [JBS](https://bugs.openjdk.org/browse/JDK-8345625) |
| JDK-8349135 | Add tests for HttpRequest.Builder.copy() | [JBS](https://bugs.openjdk.org/browse/JDK-8349135) |
| JDK-8349551 | Failures in tests after JDK-8345625 | [JBS](https://bugs.openjdk.org/browse/JDK-8349551) |
| JDK-8349702 | jdk.internal.net.http.Http2Connection::putStream needs to provide cause while cancelling stream | [JBS](https://bugs.openjdk.org/browse/JDK-8349702) |
| JDK-8349813 | Test behavior of limiting() on RS operators throwing exceptions | [JBS](https://bugs.openjdk.org/browse/JDK-8349813) |
| JDK-8350019 | HttpClient: DelegatingExecutor should resort to the fallback executor only on RejectedExecutionException | [JBS](https://bugs.openjdk.org/browse/JDK-8350019) |
| JDK-8350279 | HttpClient: Add a new HttpResponse method to identify connections | [JBS](https://bugs.openjdk.org/browse/JDK-8350279) |
| JDK-8350915 | [JMH] test SocketChannelConnectionSetup failed for 2 threads config | [JBS](https://bugs.openjdk.org/browse/JDK-8350915) |
| JDK-8351339 | WebSocket::sendBinary assume that user supplied buffers are BIG_ENDIAN | [JBS](https://bugs.openjdk.org/browse/JDK-8351339) |
| JDK-8351347 | HttpClient Improve logging of response headers | [JBS](https://bugs.openjdk.org/browse/JDK-8351347) |
| JDK-8351601 | [JMH] test UnixSocketChannelReadWrite failed for 2 threads config | [JBS](https://bugs.openjdk.org/browse/JDK-8351601) |
| JDK-8352431 | java/net/httpclient/EmptyAuthenticate.java uses "localhost" | [JBS](https://bugs.openjdk.org/browse/JDK-8352431) |
| JDK-8353197 | Document preconditions for JavaLangAccess methods | [JBS](https://bugs.openjdk.org/browse/JDK-8353197) |
| JDK-8353949 | HttpHeaders.firstValueAsLong unnecessarily boxes to Long | [JBS](https://bugs.openjdk.org/browse/JDK-8353949) |
| JDK-8354024 | [JMH] Create ephemeral UnixDomainSocketAddress provider with thread-safe close semantics | [JBS](https://bugs.openjdk.org/browse/JDK-8354024) |
| JDK-8355360 | -d option of jwebserver command should accept relative paths | [JBS](https://bugs.openjdk.org/browse/JDK-8355360) |
| JDK-8355370 | Include server name in HTTP test server thread names to improve diagnostics | [JBS](https://bugs.openjdk.org/browse/JDK-8355370) |
| JDK-8355391 | Use Long::hashCode in java.time | [JBS](https://bugs.openjdk.org/browse/JDK-8355391) |
| JDK-8355578 | [java.net] Use @requires tag instead of exiting based on "os.name" property value | [JBS](https://bugs.openjdk.org/browse/JDK-8355578) |
| JDK-8356439 | Rename JavaLangAccess::*NoRepl methods | [JBS](https://bugs.openjdk.org/browse/JDK-8356439) |
| JDK-8357821 | Revert incorrectly named JavaLangAccess::unchecked* methods | [JBS](https://bugs.openjdk.org/browse/JDK-8357821) |
| JDK-8357993 | Use "stdin.encoding" for reading System.in with InputStreamReader/Scanner [hotspot] | [JBS](https://bugs.openjdk.org/browse/JDK-8357993) |
| JDK-8357995 | Use "stdin.encoding" for reading System.in with InputStreamReader/Scanner [core] | [JBS](https://bugs.openjdk.org/browse/JDK-8357995) |
| JDK-8358688 | HttpClient: Simplify file streaming in RequestPublishers.FilePublisher | [JBS](https://bugs.openjdk.org/browse/JDK-8358688) |
| JDK-8359168 | Revert stdin.encoding usage in test/hotspot/jtreg/vmTestbase/nsk/jvmti/AttachOnDemand/attach010/attach010Agent00.java | [JBS](https://bugs.openjdk.org/browse/JDK-8359168) |
| JDK-8359223 | HttpClient: Remove leftovers from the SecurityManager cleanup | [JBS](https://bugs.openjdk.org/browse/JDK-8359223) |
| JDK-8359225 | Remove unused test/jdk/javax/script/MyContext.java | [JBS](https://bugs.openjdk.org/browse/JDK-8359225) |
| JDK-8361842 | Move input validation checks to Java for java.lang.StringCoding intrinsics | [JBS](https://bugs.openjdk.org/browse/JDK-8361842) |
| JDK-8362243 | Devkit creation for Fedora base OS is broken | [JBS](https://bugs.openjdk.org/browse/JDK-8362243) |
| JDK-8362244 | Devkit's Oracle Linux base OS keyword is incorrectly documented | [JBS](https://bugs.openjdk.org/browse/JDK-8362244) |
| JDK-8362884 | [GCC static analyzer] unix NetworkInterface.c addif leak on early returns | [JBS](https://bugs.openjdk.org/browse/JDK-8362884) |
| JDK-8363925 | Remove unused sun.nio.cs.ArrayEncoder::encode | [JBS](https://bugs.openjdk.org/browse/JDK-8363925) |
| JDK-8364263 | HttpClient: Improve encapsulation of ProxyServer | [JBS](https://bugs.openjdk.org/browse/JDK-8364263) |
| JDK-8364365 | HKSCS encoder does not properly set the replacement character | [JBS](https://bugs.openjdk.org/browse/JDK-8364365) |
| JDK-8365244 | Some test control variables are undocumented in doc/testing.md | [JBS](https://bugs.openjdk.org/browse/JDK-8365244) |
| JDK-8366040 | Change URL.lookupViaProviders to use ScopedValue to detect recursive lookup | [JBS](https://bugs.openjdk.org/browse/JDK-8366040) |
| JDK-8366575 | Remove SDP support | [JBS](https://bugs.openjdk.org/browse/JDK-8366575) |
| JDK-8366577 | Deprecate java.net.Socket::setPerformancePreferences | [JBS](https://bugs.openjdk.org/browse/JDK-8366577) |
| JDK-8366693 | Backout recent JavaLangAccess changes breaking the build | [JBS](https://bugs.openjdk.org/browse/JDK-8366693) |
| JDK-8366765 | [REDO] Rename JavaLangAccess::*NoRepl methods | [JBS](https://bugs.openjdk.org/browse/JDK-8366765) |
| JDK-8367067 | Improve exception handling in HttpRequest.BodyPublishers | [JBS](https://bugs.openjdk.org/browse/JDK-8367067) |
| JDK-8367068 | Remove redundant HttpRequest.BodyPublisher tests | [JBS](https://bugs.openjdk.org/browse/JDK-8367068) |
| JDK-8367976 | Validate and clamp jdk.httpclient.bufsize | [JBS](https://bugs.openjdk.org/browse/JDK-8367976) |
| JDK-8368249 | HttpClient: Translate exceptions thrown by sendAsync | [JBS](https://bugs.openjdk.org/browse/JDK-8368249) |
| JDK-8368528 | HttpClient.Builder.connectTimeout should accept arbitrarily large values | [JBS](https://bugs.openjdk.org/browse/JDK-8368528) |
| JDK-8371133 | Clarify the purpose of "src/jdk.compiler/share/classes/com/sun/tools/javac/resources/ct.properties" | [JBS](https://bugs.openjdk.org/browse/JDK-8371133) |

## Key Contributions

### 1. BodyPublishers.ofFileChannel (JDK-8329829)

Added a new method to create a BodyPublisher from a FileChannel with offset and length parameters, enabling efficient file streaming for HTTP requests.

**API Addition:**

```java
/**
 * Returns a {@code BodyPublisher} that reads data from a {@link FileChannel}
 * starting at the specified offset and continuing for the specified length.
 *
 * <p> This method is useful when you need to upload a portion of a file
 * without reading the entire file into memory.
 *
 * @param channel a file channel
 * @param offset the offset of the first byte
 * @param length the number of bytes to read from the file channel
 *
 * @throws IndexOutOfBoundsException if the specified byte range is
 * found to be {@linkplain Objects#checkFromIndexSize(long, long, long)
 * out of bounds} compared with the size of the file referred by the
 * channel
 *
 * @throws IOException if the {@linkplain FileChannel#size() channel's
 * size} cannot be determined or the {@code channel} is closed
 *
 * @since 26
 */
public static BodyPublisher ofFileChannel(FileChannel channel, 
                                          long offset, 
                                          long length) throws IOException {
    Objects.requireNonNull(channel, "channel");
    return new RequestPublishers.FileChannelPublisher(channel, offset, length);
}
```

**Impact:** 4 files changed, 849 insertions(+), 5 deletions(-)

### 2. Better HTTP Connections (JDK-8345625)

A comprehensive improvement to HTTP connection handling, introducing better proxy utilities and connection management.

**Key Changes:**
- Added `ProxyUtil` class for centralized proxy handling
- Improved connection reuse and management
- Enhanced error handling across HTTP/HTTPS/FTP protocols

**Impact:** 10 files changed, 109 insertions(+), 47 deletions(-)

### 3. BodyHandlers for Excessive Server Input (JDK-8328919)

Added methods to handle situations where servers send more data than expected.

### 4. Connection Identification (JDK-8350279)

Added a new method to identify HTTP connections, useful for debugging and connection pooling.

### 5. Security Manager Cleanup (JDK-8359223)

Removed leftover code from the SecurityManager deprecation, modernizing the HttpClient codebase.

### 6. SDP Support Removal (JDK-8366575)

Removed Solaris-specific SDP (Sockets Direct Protocol) support as part of platform modernization.

### 7. Socket.setPerformancePreferences Deprecation (JDK-8366577)

Deprecated the `setPerformancePreferences` method which was rarely used and had implementation limitations.

## Development Style

### API Design Philosophy

Volkan Yazici's development approach emphasizes:

1. **Backward Compatibility**: Careful consideration of API changes
2. **Clear Documentation**: Comprehensive Javadoc with examples
3. **Defensive Programming**: Input validation and null checks
4. **Test Coverage**: Extensive test suites for new features

### Code Review Pattern

```
Typical commit structure:
- Clear JBS issue reference
- Detailed API design rationale
- Reviewed-by: typically dfuchs, jpai, michaelm
- Comprehensive test cases included
```

### Key Technical Areas

1. **HTTP/2 Protocol**: Deep understanding of HTTP/2 semantics
2. **Reactive Streams**: BodyPublisher/BodySubscriber patterns
3. **Async Programming**: CompletableFuture-based APIs
4. **Security**: Connection security and validation

## Related Links

- [OpenJDK Profile](https://openjdk.org/census#vyazici)
- [JBS Issues by Volkan Yazici](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20vyazici)
- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=vyazici@openjdk.org)

## Technical Notes

### HttpClient Architecture

The HttpClient API follows a reactive, non-blocking design:

```
HttpRequest -> HttpClient -> HttpResponse
     |              |              |
     v              v              v
BodyPublisher  send/sendAsync  BodyHandler
     |                              |
     v                              v
Flow.Publisher               BodySubscriber
```

### Key API Additions in JDK 26

| Method | Purpose |
|--------|---------|
| `BodyPublishers.ofFileChannel()` | Efficient file streaming |
| `HttpResponse.connectionId()` | Connection identification |
| `BodyHandlers.ofExcessiveInput()` | Handle oversized responses |

### Testing Philosophy

Volkan's tests typically include:
- Positive test cases for normal operation
- Negative test cases for error conditions
- Edge cases (empty input, large input, concurrent access)
- JMH benchmarks for performance-critical code