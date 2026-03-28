# 性能基准 (Benchmarks)

Performance benchmarking methodology, results, and guidelines for the JDK ecosystem.

> **Important**: All performance claims in this repository should reference benchmarks documented here. Every result must include the source, workload conditions, and reproducibility information.

---

## Table of Contents

1. [Benchmarking Methodology](#1-benchmarking-methodology)
2. [Key Results](#2-key-results)
3. [Tools](#3-tools)
4. [Guidelines](#4-guidelines)

---

## 1. Benchmarking Methodology

### 1.1 Principles

Every benchmark result in this repository must satisfy the following criteria:

| Criterion | Requirement |
|-----------|-------------|
| **Source** | JBS issue, PR description, or mailing list post |
| **Workload** | Specific scenario (e.g., "high-allocation microservice", "batch processing") |
| **Environment** | JDK version, OS, CPU, memory, GC configuration |
| **Reproducibility** | Command or harness to reproduce the result |
| **Statistical Rigor** | Number of iterations, confidence interval, warm-up period |

### 1.2 Common Pitfalls

1. **Micro-benchmarks without JMH**: Hand-written loops are unreliable due to JIT elimination, dead code elimination, and on-stack replacement.
2. **Insufficient warm-up**: JIT compilation stabilizes after several thousand iterations. Report steady-state numbers.
3. **Single-run results**: Always report the median of multiple runs with confidence intervals.
4. **Ignoring GC pauses**: A single GC pause can skew throughput results. Use `-XX:+PrintGCDetails` or JFR to correlate.
5. **Unrealistic workloads**: Synthetic benchmarks that do not represent production patterns lead to misleading conclusions.

### 1.3 Benchmark Categories

| Category | Scope | Typical Tool | Example |
|----------|-------|-------------|---------|
| **Micro** | Single method / operation | JMH | `String.hashCode()` throughput |
| **Meso** | Component / subsystem | JMH / custom | G1 remembered set scan time |
| **Macro** | Full application | Renaissance, SPECjbb2015 | Web server request latency |
| **Startup** | Time-to-first-response | Custom harness | JDK startup time with `CDS` |

---

## 2. Key Results

> **Note**: Benchmark results are populated as verified data becomes available. See Section 4 for the template to contribute results. Results must reference a verifiable source (JBS issue, PR, mailing list post).

### Contributing Results

To add benchmark results, create a subdirectory (e.g., `benchmarks/gc/`) with detailed Markdown files following the template in Section 4.

---

## 3. Tools

### 3.1 JMH (Java Microbenchmark Harness)

The standard tool for Java micro-benchmarks, maintained as part of the OpenJDK project.

```bash
# Install via Maven
mvn install:install-file \
  -Dfile=jmh-core.jar -DgroupId=org.openjdk.jmh -DartifactId=jmh-core

# Run a benchmark with GC logging
java -jar benchmarks.jar \
  -jvmArgs "-XX:+UseZGC -XX:+PrintGCDetails" \
  -wi 5 -i 10 -t 4
```

**Key options**:

| Option | Purpose |
|--------|---------|
| `-wi N` | Warm-up iterations |
| `-i N` | Measurement iterations |
| `-t N` | Number of threads |
| `-f N` | Fork count (isolate JIT state) |
| `-jvmArgs` | Pass JVM flags |

### 3.2 Renaissance Suite

A modern macro-benchmark suite covering diverse real-world workloads.

```bash
# Download and run
java -jar renaissance.jar \
  --csv results.csv \
  --policy fixed-count --iterations 5 \
  all
```

**Notable benchmarks**: `scala-kmeans`, `finagle-http`, `akka-uct`, `rx-json`, `jdk-concurrent-scramble`.

### 3.3 SPECjbb2015

Industry-standard Java server benchmark. Measures throughput and response time under controlled load.

```bash
# Run with custom GC
java -XX:+UseG1GC -Xmx4g \
  -jar specjbb2015.jar \
  -m COMPOSITE
```

### 3.4 DaCapo Benchmarks

Open-source macro-benchmarks for Java runtime research.

```bash
java -jar dacapo.jar -s large -n 5 lusearch
```

### 3.5 Tool Selection Guide

| Tool | Best For | License |
|------|----------|---------|
| **JMH** | Micro-benchmarks, JIT behavior | GPL v2 |
| **Renaissance** | Macro workloads, library performance | MIT |
| **SPECjbb2015** | Enterprise throughput, compliance | Commercial |
| **DaCapo** | Academic research, GC evaluation | Apache-like |

---

## 4. Guidelines

### 4.1 Documenting a Benchmark

When adding benchmark results, use the following template:

```markdown
## [Benchmark Name]

**Date**: YYYY-MM-DD
**JDK Version**: JDK XX (build ...)
**Platform**: Linux x86_64, 8-core, 32GB RAM
**GC**: ZGC (-Xmx8g)
**Tool**: JMH 1.37

### Configuration
[Detailed flags and setup]

### Results
| Metric | Value | Unit | Confidence |
|--------|-------|------|-----------|
| Throughput | 12.5 | ops/ms | +/- 0.3 |

### Comparison
| JDK | Throughput (ops/ms) | Delta |
|-----|---------------------|-------|
| JDK 21 | 10.0 | baseline |
| JDK 26 | 12.5 | +25% |
```

### 4.2 Environment Checklist

Before running benchmarks, verify:

- [ ] OS: Disable frequency scaling (`cpupower frequency-set -g performance`)
- [ ] OS: Disable transparent huge pages if testing default behavior
- [ ] JDK: Record exact build string (`java -version`)
- [ ] JDK: Disable background compilation for warm-up tests (`-Xbatch`)
- [ ] System: No other CPU-intensive processes running
- [ ] System: Sufficient free memory to avoid OS-level swapping
- [ ] Reproducibility: Save the full command line and configuration

### 4.3 Reporting Rules for This Repository

1. **Always qualify performance claims**: Write "up to 25% improvement under high-allocation workloads" not "25% faster".
2. **Cite the source**: Link to the JBS issue, PR, or mailing list thread.
3. **Provide context**: State the workload, JDK version, and GC configuration.
4. **Avoid cherry-picking**: Report best, worst, and median results when possible.
5. **Update on new versions**: When a new JDK version changes results, update or annotate older data.

---

## Related

- [Performance topic](/by-topic/performance/) - JDK performance analysis
- [GC timeline](/by-topic/gc/) - Garbage collector evolution
- [Cases](/cases/) - Real-world performance case studies
