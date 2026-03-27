# 故障排查指南 (Troubleshooting Guide)

A structured approach to diagnosing and resolving common JDK runtime issues.

---

## Table of Contents

1. [Quick Diagnosis Flowchart](#1-quick-diagnosis-flowchart)
2. [Common Problems](#2-common-problems)
3. [Tool Matrix](#3-tool-matrix)
4. [Emergency Checklist](#4-emergency-checklist)

---

## 1. Quick Diagnosis Flowchart

```
Application Problem?
│
├── OutOfMemoryError ──────────────────────┐
│   ├── Java heap space ................... │──► [2.1 Memory Issues]
│   ├── Metaspace .......................... │
│   ├── GC overhead limit exceeded ......... │
│   └── Direct buffer memory ............... │
│
├── Slow / High Latency ───────────────────┐
│   ├── Long GC pauses ..................... │──► [2.2 GC Issues]
│   ├── Thread contention .................. │──► [2.3 Thread Issues]
│   ├── JIT deoptimization ................. │──► [2.5 JIT Issues]
│   └── I/O bottleneck ..................... │
│
├── High CPU Usage ─────────────────────────┐
│   ├── GC spinning ........................ │──► [2.2 GC Issues]
│   ├── Thread loops / deadlock ............ │──► [2.3 Thread Issues]
│   ├── JIT compilation storms ............. │──► [2.5 JIT Issues]
│   └── Infinite regex / regex catastroph.. │
│
├── Startup Slow ──────────────────────────┐
│   ├── Class loading ...................... │──► [2.4 Startup Issues]
│   ├── JIT warm-up ........................ │
│   ├── Large classpath .................... │
│   └── No CDS / AOT ....................... │
│
├── Crash / SIGSEGV / SIGBUS ──────────────┐
│   ├── JNI issue .......................... │──► Check hs_err_pid*.log
│   ├── JVM bug ............................ │
│   ├── Native library ..................... │
│   └── OS / hardware ...................... │
│
└── Hang / Unresponsive ───────────────────┐
    ├── Deadlock ........................... │──► [2.3 Thread Issues]
    ├── Waiting on external resource ....... │
    ├── GC Full GC stall ................... │──► [2.2 GC Issues]
    └── Virtual thread pinned .............. │──► [2.3 Thread Issues]
```

---

## 2. Common Problems

### 2.1 Memory Issues

| Symptom | Likely Cause | Diagnostic Command | Fix |
|---------|-------------|-------------------|-----|
| `OOM: Java heap space` | Memory leak or undersized heap | `jmap -histo <pid>` | Increase `-Xmx`, analyze heap dump |
| `OOM: Metaspace` | Class loader leak, dynamic proxy generation | `jstat -gcmetacapacity <pid>` | Increase `-XX:MaxMetaspaceSize`, check for classloader leaks |
| `OOM: GC overhead` | Heap too small, excessive allocation rate | `-Xlog:gc*:gc.log` | Increase heap, tune GC, reduce allocation |
| `OOM: Direct buffer` | NIO ByteBuffer leak | `jcmd <pid> VM.native_memory` | Ensure `release()` or use try-with-resources |
| Heap grows indefinitely | Memory leak in application or library | `jcmd <pid> GC.heap_info` | Take periodic heap dumps, compare with `jhat` or MAT |

### 2.2 GC Issues

| Symptom | Likely Cause | Diagnostic Command | Fix |
|---------|-------------|-------------------|-----|
| Long STW pauses (>500ms) | Full GC, humongous allocation in G1 | `-Xlog:gc*:gc.log` | Switch to ZGC, tune G1 region size |
| High GC frequency | Small heap, high allocation rate | `jstat -gcutil <pid> 1000` | Increase heap, reduce allocation, tune young gen |
| GC takes >10% CPU | Metaspace or heap pressure | `-Xlog:gc,gc+cpu=debug` | Review allocation patterns, increase heap |
| Promotion failure | Fragmented old gen | `-Xlog:gc+ergo*=debug` | Increase `-XX:G1ReservePercent`, tune mixed GC |
| Concurrent mode failure | CMS/old gen full during concurrent cycle | N/A (legacy) | Migrate to G1 or ZGC |

### 2.3 Thread Issues

| Symptom | Likely Cause | Diagnostic Command | Fix |
|---------|-------------|-------------------|-----|
| Deadlock | Circular lock acquisition | `jstack <pid>` or `jcmd <pid> Thread.print` | Reorder lock acquisition, use `tryLock` with timeout |
| Thread leak | Unbounded thread creation | `jcmd <pid> Thread.dump_to_file` | Use virtual threads or bounded thread pools |
| Virtual thread pinned | Synchronized block during blocking I/O | `-Djdk.tracePinnedThreads=full` | Replace `synchronized` with `ReentrantLock` |
| High context switching | Too many platform threads | `pidstat -t -p <pid> 1` | Reduce thread count, use virtual threads |
| `InterruptedException` swallowed | Catch blocks ignoring interrupts | Code review | Always restore interrupt status: `Thread.currentThread().interrupt()` |

### 2.4 Startup Issues

| Symptom | Likely Cause | Diagnostic Command | Fix |
|---------|-------------|-------------------|-----|
| Slow cold start | No CDS, large classpath | `-Xlog:class+load:cds.log` | Enable CDS: `java -Xshare:dump` then `-Xshare:on` |
| Slow warm start | No AppCDS, no AOT | `-XX:+PrintCompilation` | Use AppCDS, explore Leyden/AOT |
| Large classpath scan | Many JARs, SpringBoot | `-verbose:class` | Use classpath optimization, Spring thin launcher |
| Agent overhead | Too many -javaagent flags | Benchmark without agents | Reduce agents, use JFR instead of multiple agents |
| Initial JIT cost | C1/C2 compilation queue | `-XX:+CITime` | Consider `-XX:TieredStopAtLevel=1` for CLI tools |

### 2.5 JIT Issues

| Symptom | Likely Cause | Diagnostic Command | Fix |
|---------|-------------|-------------------|-----|
| Deoptimization storms | Unstable type profiles | `-XX:+PrintDeoptimization` | Fix polymorphic call sites, warm up with representative data |
| Code cache full | Large methods, many compiled methods | `jcmd <pid> Compiler.CodeHeap_Analytics` | Increase `-XX:ReservedCodeCacheSize` |
| Inlining failure | Large methods, complex branches | `-XX:+PrintInlining` | Refactor to smaller methods, use `-XX:MaxInlineSize` |
| C2 crash | Compiler bug (rare) | `hs_err_pid*.log` | File JBS issue, use `-XX:CompileCommand=exclude` as workaround |
| Intermittent slow | Tiered promotion not complete | `-XX:+PrintCompilation` | Ensure warm-up is sufficient before measurement |

---

## 3. Tool Matrix

### 3.1 JDK Built-in Tools

| Tool | Purpose | When to Use | Example |
|------|---------|-------------|---------|
| **jcmd** | Swiss-army knife for JVM diagnostics | First tool to reach for | `jcmd <pid> help` |
| **jstack** | Thread dump | Deadlocks, hangs | `jstack -l <pid>` |
| **jmap** | Heap histogram and dump | Memory leaks | `jmap -histo:live <pid>` |
| **jstat** | GC and compilation statistics | Monitoring GC behavior | `jstat -gcutil <pid> 1000` |
| **jinfo** | View/modify JVM flags | Checking runtime config | `jinfo -flags <pid>` |
| **jfr** | Flight Recording (event-based profiling) | Production profiling, low overhead | `jcmd <pid> JFR.start duration=60s filename=rec.jfr` |
| **jhsdb** | HotSpot Serviceability Agent | Deep debugging, CLHSDB | `jhsdb clhsdb --pid <pid>` |

### 3.2 GC-Specific Diagnostics

| GC | Key Flags for Diagnosis | |
|----|------------------------|---|
| **G1** | `-Xlog:gc*=info:gc.log` `-XX:+PrintGCDetails` (pre-JDK 9) | |
| **ZGC** | `-Xlog:gc*:gc.log` `-XX:+ZStatisticsForceTrace` | |
| **Shenandoah** | `-Xlog:gc*=info:gc.log` | |

### 3.3 OS-Level Tools

| Tool | Purpose | Example |
|------|---------|---------|
| **top / htop** | CPU and memory overview | `top -H -p <pid>` |
| **pidstat** | Per-thread CPU, I/O | `pidstat -t -p <pid> 1` |
| **strace** | System call tracing | `strace -f -e trace=read,write -p <tid>` |
| **perf** | CPU profiling (native + Java) | `perf record -g -p <pid>` |
| **vmstat** | Memory and swap activity | `vmstat 1` |

---

## 4. Emergency Checklist

When a production JVM is in trouble, follow this checklist in order:

### Step 1: Collect Data Before Restarting

```bash
# Thread dump (3 times, 5 seconds apart)
jcmd <pid> Thread.print -l > threaddump_1.txt
sleep 5
jcmd <pid> Thread.print -l > threaddump_2.txt
sleep 5
jcmd <pid> Thread.print -l > threaddump_3.txt

# Heap histogram (lightweight, does not stop the app)
jcmd <pid> GC.class_histogram > class_histogram.txt

# GC log (if not already enabled)
jcmd <pid> VM.log output=gc_emergency.log what=gc*

# JFR recording (30 seconds)
jcmd <pid> JFR.start duration=30s filename=emergency_recording.jfr

# System info
jcmd <pid> VM.info > vminfo.txt
jcmd <pid> VM.flags > vmflags.txt
```

### Step 2: Quick Assessment

| Check | Command | What to Look For |
|-------|---------|-----------------|
| Is it alive? | `jcmd <pid> VM.version` | Command responds |
| Heap usage? | `jcmd <pid> GC.heap_info` | Used > 90% indicates pressure |
| Thread count? | `jcmd <pid> Thread.dump_to_file -format=json threads.json` | Unusually high count |
| GC activity? | Check gc.log | Full GC, long pauses |
| CPU usage? | `top -H -p <pid>` | Which thread is consuming CPU |

### Step 3: Escalation

- **JVM crash**: Check `hs_err_pid*.log`, search [JBS](https://bugs.openjdk.org) for the `siginfo` and `Exception` in the stack trace
- **Memory leak**: Analyze heap dump with Eclipse MAT or VisualVM
- **Performance regression**: Compare JFR recordings before and after the regression
- **GC issue**: Consider switching GC (`-XX:+UseZGC` for low latency, `-XX:+UseG1GC` for balanced throughput)

---

## Related Resources

- [Cases](/cases/) - Real-world troubleshooting case studies
- [Best Practices](/best-practices/) - Preventive measures and recommended configurations
- [Guides](/guides/) - In-depth JDK guides
- [By-Topic](/by-topic/) - Topic-specific deep dives
