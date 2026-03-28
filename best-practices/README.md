# 最佳实践 (Best Practices)

Curated best practices for JDK development, deployment, and operations, organized by topic.

---

## Table of Contents

1. [GC Best Practices](#1-gc-best-practices)
2. [Virtual Thread Best Practices](#2-virtual-thread-best-practices)
3. [Memory Management](#3-memory-management)
4. [Security](#4-security)
5. [Performance](#5-performance)
6. [JDK Migration](#6-jdk-migration)

---

## 1. GC Best Practices

### 1.1 GC Selection Guide

| Workload | Recommended GC | Rationale |
|----------|---------------|-----------|
| General-purpose / balanced | **G1GC** (default) | Good balance of throughput and latency |
| Low-latency (< 10ms pauses) | **ZGC** | Sub-millisecond pauses regardless of heap size |
| Large heap (> 32GB) | **ZGC** or **Shenandoah** | Concurrent compaction avoids Full GC stalls |
| Batch / throughput-critical | **ParallelGC** | Maximum throughput, pauses acceptable |
| Small heap (< 512MB) | **SerialGC** | Minimal overhead for small workloads |

### 1.2 Do's and Don'ts

| Do | Don't |
|----|-------|
| Use `-Xlog:gc*:gc.log` to enable GC logging from day one | Blindly tune GC flags without measuring first |
| Size the heap to leave 25-50% headroom | Set `-Xms` and `-Xmx` to the same value without testing |
| Monitor GC metrics with JFR in production | Ignore `GC overhead limit exceeded` warnings |
| Test with production-like data volumes | Assume GC behavior on small heaps predicts production |
| Use `-XX:MaxGCPauseMillis` as a hint for G1 | Set `-XX:MaxGCPauseMillis` to an unreasonably low value |
| Consider ZGC for latency-sensitive services | Use CMS (deprecated in JDK 9 via JEP 291, removed in JDK 14 via JEP 363) |

### 1.3 Key Flags Reference

```bash
# G1 - General tuning
-XX:+UseG1GC -Xmx4g -XX:MaxGCPauseMillis=200

# ZGC - Low latency
-XX:+UseZGC -Xmx16g -XX:+ZGenerational (JDK 21+, generational mode)

# Shenandoah - Low latency alternative
-XX:+UseShenandoahGC -Xmx16g
```

---

## 2. Virtual Thread Best Practices

### 2.1 Do's and Don'ts

| Do | Don't |
|----|-------|
| Use `Executors.newVirtualThreadPerTaskExecutor()` for concurrent I/O tasks | Pool virtual threads (they are not meant to be pooled) |
| Replace `synchronized` with `ReentrantLock` in hot paths that may block | Use `synchronized` around blocking I/O operations (causes pinning) |
| Use virtual threads for I/O-bound workloads | Use virtual threads for CPU-bound compute tasks |
| Set `-Djdk.tracePinnedThreads=short` during development | Ignore pinning warnings in production |
| Use `StructuredTaskScope` for structured concurrency | Create unbounded virtual threads without back-pressure |
| Handle `InterruptedException` properly | Swallow `InterruptedException` in virtual thread code |

### 2.2 Migration from Platform Threads

| Pattern | Platform Thread (Before) | Virtual Thread (After) |
|---------|------------------------|----------------------|
| Thread-per-request | `new Thread(task).start()` | `Thread.ofVirtual().start(task)` |
| Thread pool | `Executors.newFixedThreadPool(N)` | `Executors.newVirtualThreadPerTaskExecutor()` |
| Synchronized block | `synchronized (lock) { ... }` | `lock.lock(); try { ... } finally { lock.unlock(); }` |
| ThreadLocal | `ThreadLocal.withInitial(...)` | Use sparingly; prefer method parameters |

### 2.3 Pinning Detection

```bash
# Detect pinned virtual threads (development)
java -Djdk.tracePinnedThreads=full -jar app.jar

# Typical pinning warning:
# Thread[#123] pinned at com.example.MyService.process() line 42
```

---

## 3. Memory Management

### 3.1 Do's and Don'ts

| Do | Don't |
|----|-------|
| Use try-with-resources for `InputStream`, `Connection`, etc. | Rely on `finalize()` (deprecated since JDK 9, for removal) |
| Prefer primitive arrays over boxed types for large data | Use `ArrayList<Integer>` for millions of elements |
| Set `-XX:MaxDirectMemorySize` when using NIO heavily | Allocate direct ByteBuffers without tracking |
| Use `WeakReference` / `SoftReference` intentionally | Use `SoftReference` as a caching strategy without understanding GC impact |
| Profile with JFR `jdk.ObjectAllocationInNewTLAB` event | Guess where allocations happen |
| Use `ByteBuffer` pooling for high-throughput NIO | Allocate a new ByteBuffer per operation in hot loops |

### 3.2 Memory Configuration Guide

| Scenario | Recommended Settings |
|----------|---------------------|
| Microservice (container) | `-Xms512m -Xmx512m` with container awareness (`-XX:+UseContainerSupport`) |
| Data processing | `-Xmx` based on data size + 50% headroom |
| Cache-heavy | Consider off-heap storage or `ByteBuffer.allocateDirect()` |
| Many classloaders | `-XX:MaxMetaspaceSize=256m` to prevent unbounded growth |

---

## 4. Security

### 4.1 Do's and Don'ts

| Do | Don't |
|----|-------|
| Use `MessageDigest` with SHA-256 or stronger | Use MD5 or SHA-1 for security purposes |
| Validate all external input (deserialization, XML, etc.) | Use `ObjectInputStream` on untrusted data without filtering |
| Enable `-Djava.security.properties=strong.properties` for strong cryptography | Use default JCE limits when high-security is required |
| Keep JDK updated for security patches | Run end-of-life JDK versions in production |
| Use `SecurityManager` filters or migration paths (JDK 17+) | Rely on `SecurityManager` as sole security boundary (deprecated for removal) |
| Configure `serialFilter` for RMI and JMX | Expose JMX/RMI ports without authentication |
| Use TLS 1.3 (`-Djdk.tls.client.protocols=TLSv1.3`) | Allow TLS 1.0/1.1 in production |

### 4.2 Common Security Flags

```bash
# Force TLS 1.3
-Djdk.tls.client.protocols=TLSv1.3

# Disable dangerous serialization
-Djdk.serialFilter=!com.dangerous.**

# Enable security audit logging
-Djava.security.debug=access,failure
```

---

## 5. Performance

### 5.1 Do's and Don'ts

| Do | Don't |
|------|-------|
| Profile before optimizing ("measure, don't guess") | Optimize based on intuition alone |
| Use JMH for micro-benchmarks | Write hand-rolled micro-benchmarks without JMH |
| Enable CDS for faster startup (`-Xshare:on`) | Ignore startup time for CLI tools and serverless |
| Use `StringBuilder` for string concatenation **in loops** (applies to all JDK versions; `StringConcatFactory` in JDK 9+ only optimizes single-expression concatenation, not loop accumulation) | Use `+=` for string concatenation in loops expecting high throughput |
| Prefer `ArrayList` over `LinkedList` in most cases | Use `LinkedList` for indexed access patterns |
| Warm up JIT before measuring performance | Benchmark in the first few seconds of JVM execution |
| Use `ConcurrentHashMap` over `Collections.synchronizedMap` | Use `Hashtable` (legacy, fully synchronized) |
| Check for lock contention with JFR `jdk.JavaMonitorWait` | Assume synchronized is always the bottleneck |

### 5.2 Quick Performance Tuning Checklist

```bash
# 1. Enable GC logging
-Xlog:gc*:gc.log

# 2. Enable JFR (low overhead, < 2%)
-XX:StartFlightRecording=duration=60s,filename=app.jfr

# 3. Enable CDS for startup
-Xshare:on

# 4. Use appropriate GC
-XX:+UseZGC  # for low latency
-XX:+UseG1GC # for balanced (default)
```

---

## 6. JDK Migration

### 6.1 Migration Do's and Don'ts

| Do | Don't |
|----|-------|
| Use `jdeps` to analyze dependencies before migration | Migrate to a new JDK without testing |
| Test with `--illegal-access=deny` (JDK 17) early | Ignore deprecation warnings |
| Use Maven/Gradle toolchains to manage multiple JDK versions | Hard-code JDK paths in build scripts |
| Read the [JDK Migration Guide](https://docs.oracle.com/en/java/javase/17/migrate/) for each major version | Assume code compiled on JDK 8 runs on JDK 21 without changes |
| Replace removed APIs (`javax.xml.bind` -> `jakarta.xml.bind`) | Wait until the last minute to address removed modules |
| Use `jlink` to create minimal custom runtimes | Ship the full JDK for microservices |
| Test with `-Xcheck:jni` to catch JNI issues | Assume JNI code is forward-compatible without testing |

### 6.2 Migration Path by Version

| From -> To | Key Changes | Effort |
|------------|-------------|--------|
| JDK 8 -> 11 | Modules, removed APIs, javax -> jakarta | High |
| JDK 11 -> 17 | Sealed classes, pattern matching preview, SecurityManager deprecation | Medium |
| JDK 17 -> 21 | Virtual Threads, pattern matching final, Generational ZGC | Low-Medium |
| JDK 21 -> 25 | Scoped Values final (JEP 506), Primitive Types in Patterns (JEP 455), Flexible Constructor Bodies (JEP 482) | Low |
| JDK 25 -> 26 | HTTP/3 (JEP 517, final), Value Classes (JEP 401, preview) | Low |

### 6.3 Essential Migration Tools

| Tool | Purpose | Command |
|------|---------|---------|
| **jdeps** | Dependency analysis | `jdeps --jdk-internals myapp.jar` |
| **jlink** | Custom runtime creation | `jlink --add-modules java.se --output custom-jre` |
| **jdeprscan** | Find deprecated API usage | `jdeprscan --release 21 myapp.jar` |
| **jtreg** | Regression testing | See [jtreg guide](/guides/) |

---

## Related Resources

- [Benchmarks](/benchmarks/) - Performance benchmark results and methodology
- [Troubleshooting](/troubleshooting/) - Diagnosing runtime issues
- [Guides](/guides/) - In-depth JDK guides
- [Cases](/cases/) - Real-world case studies
- [By-Topic](/by-topic/) - Topic-specific deep dives
