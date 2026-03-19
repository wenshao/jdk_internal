# JDK 26 Network Component Summary

> Commits: 208 (5.3% of total)
> Key Contributors: Daniel Fuchs, Volkan Yazici, Jaikiran Pai, Brian Burkhalter

---

## Overview

JDK 26 brings one of the most significant networking changes in recent years: **HTTP/3 support** (JEP 517). This release also includes TLS improvements, HTTP client enhancements, and test framework migrations.

---

## JEPs

### JEP 517: HTTP/3 for the HTTP Client

The headline feature for networking in JDK 26 is full HTTP/3 support with QUIC.

**JDK-8349910**: Implement JEP 517: HTTP/3 for the HTTP Client

| Metric | Value |
|--------|-------|
| Additions | 104,307 |
| Deletions | 2,639 |
| Author | Daniel Fuchs |
| Impact | ⭐⭐⭐⭐⭐ |

**Key Features**:
- QUIC protocol implementation
- HTTP/3 frame handling
- QPACK header compression
- Connection management for HTTP/3
- CUBIC congestion controller

**Related Issues**:
- 8371475: CUBIC congestion controller
- 8370024: QUIC pacing implementation
- 8371802: QUIC idle timeout handling
- 8372198: Connection closing fix

### JEP 527: TLS 1.3 Hybrid Key Exchange

**JDK-8314323**: Implement hybrid key exchange for TLS 1.3

| Metric | Value |
|--------|-------|
| Additions | 1,839 |
| Deletions | 120 |
| Author | Hai-May Chao |

**Key Features**:
- Post-quantum key exchange
- ML-KEM integration
- Hybrid classical/post-quantum handshakes

### JEP 524: PEM Encodings

**JDK-8360564**: PEM Encodings of Cryptographic Objects

| Metric | Value |
|--------|-------|
| Additions | 1,382 |
| Deletions | 813 |
| Author | Anthony Scarpino |

**Key Features**:
- Standardized PEM output format
- Better interoperability with OpenSSL
- Test refactoring to use PEM API

---

## HTTP Client Improvements

### Connection Management

| Issue | Description | Author |
|-------|-------------|--------|
| 8326498 | Connection leak fix (HTTP/2) | Jaikiran Pai |
| 8208693 | Request timeout scope extension | Volkan Yazici |
| 8372198 | Avoid closing connection while holding lock | Daniel Fuchs |
| 8361060 | Track origin server for connections | Jaikiran Pai |

### API Enhancements

| Issue | Description | Author |
|-------|-------------|--------|
| 8367067 | Improve exception handling in BodyPublishers | Volkan Yazici |
| 8368528 | Accept arbitrarily long connectTimeout | Volkan Yazici |
| 8369595 | firstValueAsLong failure handling | Volkan Yazici |
| 8329829 | Add BodyPublishers.ofFileChannel | Volkan Yazici |

### Cleanup

| Issue | Description | Author |
|-------|-------------|--------|
| 8366575 | Remove SDP support | Volkan Yazici |
| 8359223 | Remove SecurityManager leftovers | Volkan Yazici |

---

## HTTP Server

| Issue | Description | Author |
|-------|-------------|--------|
| 8377302 | Stop uses full timeout if handler throws | Daniel Fuchs |
| 8376031 | getServerCertificates() fix | Daniel Fuchs |
| 8372746 | Formatting cleanup | Daisuke Yamazaki |
| 8272758 | Avoid partial file name matches | Volkan Yazici |

---

## TLS & SSL

### Certificate Handling

| Issue | Description | Author |
|-------|-------------|--------|
| 8359956 | Algorithm constraints in SunX509 | Artur Barashev |
| 8367104 | RSASSA-PSS parameter validation | Artur Barashev |
| 8365820 | Certificate scope constraints | Artur Barashev |
| 8365953 | Handshake session certificate fix | Artur Barashev |
| 8368032 | Enhance certificate checking | Jamil Nimeh |

### Debugging

| Issue | Description | Author |
|-------|-------------|--------|
| 8372004 | SSLLogger implements System.Logger | Sean Coffey |
| 8044609 | javax.net.debug options fix | Sean Coffey |
| 8368493 | Disable test JSSE debug by default | Bradford Wetmore |

### Root Certificates

| Issue | Description | Author |
|-------|-------------|--------|
| 8361212 | Remove AffirmTrust root CAs | Rajan Halade |
| 8359170 | Add 2 TLS and 2 CS Sectigo roots | Rajan Halade |
| 8369282 | Distrust Chunghwa ePKI Root | Mark Powers |

---

## Test Migration

A major effort to migrate networking tests from TestNG to JUnit:

| Issue | Description | Files Changed |
|-------|-------------|---------------|
| 8378344 | HTTP client tests to JUnit | 5,441 |
| 8378163 | HTTP client I/O tests | 1,991 |
| 8378276 | QUIC tests to JUnit | 1,402 |
| 8378565 | HTTP/3 tests to JUnit | 995 |
| 8378598 | WebSocket tests | 643 |
| 8378599 | Whitebox tests | 626 |
| 8378164 | HTTP/3 additional tests | 459 |
| 8373893 | HTTP server tests | 1,839 |
| 8378879 | Channels tests | 424 |
| 8373808 | QPACK/HPACK tests | 825 |
| 8378111 | java/util/jar tests | 1,797 |
| 8379154 | Selector tests | 340 |
| 8379153 | FileChannel tests | 186 |
| 8378398 | URLClassLoader tests | 443 |

---

## Other Networking

### Socket & Datagram

| Issue | Description | Author |
|-------|-------------|--------|
| 8332623 | Remove setTTL/getTTL methods | Jaikiran Pai |
| 8358958 | AsynchronousByteChannel validation | Alan Bateman |

### I/O Poller

| Issue | Description | Author |
|-------|-------------|--------|
| 8374170 | I/O Poller updates | Alan Bateman |

### URL Handling

| Issue | Description | Author |
|-------|-------------|--------|
| 8367561 | File URL header property | Jaikiran Pai |

---

## Key Commits by Impact

| Issue | Description | +/- | Author |
|-------|-------------|-----|--------|
| 8349910 | HTTP/3 (JEP 517) | 106,946 | Daniel Fuchs |
| 8353738 | TLS test cleanup | 3,603 | Matthew Donovan |
| 8378344 | HTTP client JUnit | 5,441 | Daniel Fuchs |
| 8360564 | PEM encodings (JEP 524) | 2,195 | Anthony Scarpino |
| 8314323 | TLS hybrid key exchange | 1,959 | Hai-May Chao |

---

## Top Contributors

| Rank | Contributor | Commits | Focus |
|------|-------------|---------|-------|
| 1 | Daniel Fuchs | 47 | HTTP/3, HTTP Client |
| 2 | Volkan Yazici | 45 | HTTP Client API |
| 3 | Brian Burkhalter | 53 | NIO, Networking |
| 4 | Jaikiran Pai | 67 | Connections, Sockets |
| 5 | Sean Coffey | 11 | TLS debugging |

---

## Migration Notes

### For HTTP Client Users
- HTTP/3 is now available - test with HTTP/3 servers
- Connection leak fixes may change behavior of long-lived connections
- CUBIC congestion controller improves performance on high-latency links

### For TLS Users
- Hybrid key exchange enabled by default for TLS 1.3
- Some root CAs removed - verify certificate chains
- PEM output format standardized

### For Server Developers
- HTTP Server timeout behavior changed if handlers throw
- Consider testing with new timeout semantics

---

## Performance Notes

- **HTTP/3**: Significant performance improvement for high-latency connections
- **CUBIC**: Better throughput on long-fat networks
- **Connection pooling**: Fixes may reduce connection creation overhead

---

*Last updated: 2026-03-19*
