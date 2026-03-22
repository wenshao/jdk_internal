# 容器环境

容器是现代云原生应用部署的核心方式，JDK 提供了完善的容器支持。

---
## 目录

1. [概述](#1-概述)
2. [cgroup 检测机制](#2-cgroup-检测机制)
3. [CPU 资源感知](#3-cpu-资源感知)
4. [内存资源感知](#4-内存资源感知)
5. [Docker 最佳实践](#5-docker-最佳实践)
6. [Kubernetes 部署](#6-kubernetes-部署)
7. [镜像优化](#7-镜像优化)
8. [GraalVM Native Image](#8-graalvm-native-image)
9. [JFR 容器内分析](#9-jfr-容器内分析)
10. [监控和诊断](#10-监控和诊断)
11. [常见问题](#11-常见问题)
12. [最佳实践清单](#12-最佳实践清单)
13. [相关链接](#13-相关链接)

---


## 1. 概述

### 支持的容器技术

| 技术 | 支持状态 | 说明 |
|------|----------|------|
| **Docker** | ✅ 完全支持 | 主要容器平台 |
| **Kubernetes** | ✅ 完全支持 | 容器编排平台 |
| **containerd** | ✅ 完全支持 | 容器运行时 |
| **Podman** | ✅ 完全支持 | 无守护进程容器 |

### 容器感知演进

```
JDK 8  ──── 无容器感知
          │   需要手动配置资源
          │
JDK 10 ──── 容器感知 (JDK-8146115)
          │   - 自动检测 CPU/内存限制
          │   - -XX:+UseContainerSupport
          │
JDK 11 ──── 改进容器检测
          │   - 更准确的资源检测
          │   - 修复多个检测问题
          │
JDK 14 ──── cgroup v2 初步支持
          │
JDK 17 ──── cgroup v2 改进
          │   - 更好的内存检测
          │   - CPU 配额检测优化
          │
JDK 21 ──── cgroup v2 完整支持
          │   - 完整的 cgroup v2 支持
          │   - 改进的容器检测
          │
JDK 25 ──── 容器密度提升 (LTS)
          │   - Compact Object Headers (JEP 519)
          │   - 对象头 12→8 字节，堆使用减少 ~22%
          │   - 更高容器部署密度
          │   - AOT 命令行增强 (JEP 514)
          │   - Generational Shenandoah (JEP 521)
          │
JDK 26 ──── 容器优化增强
              - G1 GC 减少同步提高吞吐 (JEP 522)
              - AOT 对象缓存支持 ZGC (JEP 516)
              - HTTP/3 客户端 API (JEP 517)
              - 更精确的资源检测
```

---

## 2. cgroup 检测机制

### cgroup v1 vs v2 对比

| 特性 | cgroup v1 | cgroup v2 |
|------|-----------|-----------|
| **内核支持** | Linux 2.6.24+ | Linux 4.5+ (推荐 5.8+) |
| **JDK 支持** | JDK 8u191+ / JDK 10+ | JDK 15+ (部分), JDK 21+ (完整) |
| **层级结构** | 多层级 (Multi-hierarchy) | 统一层级 (Unified hierarchy) |
| **内存控制** | `memory.limit_in_bytes` | `memory.max` |
| **CPU 控制** | `cpu.cfs_quota_us` / `cpu.shares` | `cpu.max` / `cpu.weight` |
| **Docker 默认** | Docker 20.10 以下 | Docker 20.10+ (可选) |
| **K8s 默认** | K8s 1.24 以下 | K8s 1.25+ (默认) |

### JVM 检测链 (Detection Chain)

JVM 启动时按以下顺序检测容器环境：

```
1. 检查 UseContainerSupport 是否启用 (默认 true)
      ↓
2. 读取 /proc/self/mountinfo 和 /proc/self/cgroup
      ↓
3. 判断 cgroup 版本
   ├── cgroup v1: 检查 /sys/fs/cgroup/memory/, /sys/fs/cgroup/cpu/
   └── cgroup v2: 检查 /sys/fs/cgroup/ (统一层级)
      ↓
4. 读取内存限制
   ├── v1: memory.limit_in_bytes
   └── v2: memory.max
      ↓
5. 读取 CPU 限制
   ├── v1: cpu.cfs_quota_us / cpu.cfs_period_us, cpu.shares
   └── v2: cpu.max (格式: "$MAX $PERIOD"), cpu.weight
      ↓
6. 计算有效 CPU 数和可用内存
      ↓
7. 基于检测结果设置 JVM 默认参数
   - 堆大小 (Heap Size)
   - GC 线程数 (GC Threads)
   - 编译线程数 (Compiler Threads)
   - ForkJoinPool 并行度
```

### cgroup v1 文件路径

```bash
# 内存相关
/sys/fs/cgroup/memory/memory.limit_in_bytes     # 内存限制 (Memory Limit)
/sys/fs/cgroup/memory/memory.usage_in_bytes      # 当前内存使用
/sys/fs/cgroup/memory/memory.max_usage_in_bytes  # 历史最高内存使用
/sys/fs/cgroup/memory/memory.stat                # 内存统计 (RSS, Cache 等)
/sys/fs/cgroup/memory/memory.failcnt             # OOM 次数

# CPU 相关
/sys/fs/cgroup/cpu/cpu.cfs_quota_us              # CPU 配额 (微秒)
/sys/fs/cgroup/cpu/cpu.cfs_period_us             # CPU 周期 (微秒, 默认 100000)
/sys/fs/cgroup/cpu/cpu.shares                    # CPU 共享权重 (默认 1024)
/sys/fs/cgroup/cpuset/cpuset.cpus                # 绑定的 CPU 核心
```

### cgroup v2 文件路径

```bash
# 内存相关
/sys/fs/cgroup/memory.max                        # 内存硬限制 ("max" 表示无限制)
/sys/fs/cgroup/memory.current                    # 当前内存使用
/sys/fs/cgroup/memory.high                       # 内存软限制 (触发回收)
/sys/fs/cgroup/memory.stat                       # 内存统计

# CPU 相关
/sys/fs/cgroup/cpu.max                           # "quota period" 格式, 如 "200000 100000"
/sys/fs/cgroup/cpu.weight                        # 权重 (1-10000, 默认 100)
/sys/fs/cgroup/cpuset.cpus.effective             # 有效 CPU 核心
```

### 如何判断当前 cgroup 版本

```bash
# 在容器内检查
stat -fc %T /sys/fs/cgroup/
# "cgroup2fs" = cgroup v2
# "tmpfs"     = cgroup v1

# 或检查挂载
mount | grep cgroup
# cgroup2 on /sys/fs/cgroup type cgroup2  → v2
# cgroup on /sys/fs/cgroup/memory type cgroup → v1

# JVM 日志: 打印容器检测信息
-Xlog:os+container=trace
```

---

## 3. CPU 资源感知

### cpu.shares vs cpu.cfs_quota

**cpu.shares (相对权重, Relative Weight)**:
```bash
# cpu.shares 不是硬限制，而是竞争时的相对比例
# 容器 A: cpu.shares=1024, 容器 B: cpu.shares=512
# 竞争时 A 获得 2/3 CPU, B 获得 1/3
# 但如果只有 A 在运行，A 可以使用所有 CPU

docker run --cpu-shares 1024 myapp    # 默认值
docker run --cpu-shares 2048 myapp    # 2 倍权重
```

**cpu.cfs_quota (硬限制, Hard Limit)**:
```bash
# cpu.cfs_quota_us / cpu.cfs_period_us = 有效 CPU 数
# 例: 200000 / 100000 = 2 个 CPU

docker run --cpus="2" myapp           # 等于 quota=200000, period=100000
docker run --cpu-quota=200000 --cpu-period=100000 myapp  # 等效
```

**JVM 如何计算有效 CPU 数 (Effective Processors)**:

```
有效 CPU = min(
    cpu.cfs_quota_us / cpu.cfs_period_us,   # 配额限制
    cpuset.cpus 中的 CPU 数,                # 绑定核心数
    物理 CPU 数                             # 主机 CPU 数
)

向上取整 (ceil)，最小为 1

例: quota=150000, period=100000
→ 150000/100000 = 1.5 → ceil(1.5) = 2 个有效 CPU

JDK 21+: 使用更精确的非整数计算影响线程池大小
```

### ActiveProcessorCount

```bash
# 自动检测 (默认)
-XX:ActiveProcessorCount=0    # 0 = 自动

# 手动覆盖 (推荐在 CPU shares 场景下)
-XX:ActiveProcessorCount=4

# 验证 JVM 检测到的 CPU 数
jcmd <pid> VM.info | grep "active_processor_count"

# 或通过 Java 代码
Runtime.getRuntime().availableProcessors();
```

**ActiveProcessorCount 影响的 JVM 子系统**:

| 子系统 | 影响 | 公式 |
|--------|------|------|
| **GC 线程 (ParallelGCThreads)** | GC 并行度 | ~CPU * 5/8 (CPU>8 时递减) |
| **GC 并发线程 (ConcGCThreads)** | 并发 GC 线程数 | ParallelGCThreads / 4 |
| **JIT 编译线程 (CICompilerCount)** | 编译速度 | log2(CPU) (大约) |
| **ForkJoinPool.commonPool()** | 并行流默认并行度 | CPU - 1 |

> **注意**: 当使用 `cpu.shares` 而非 `--cpus` 时，JVM 无法计算硬性 CPU 限制，会使用主机的全部 CPU 数。此时建议手动设置 `ActiveProcessorCount`。

---

## 4. 内存资源感知

### UseContainerSupport 检测链

```bash
# 默认启用 (JDK 10+)
-XX:+UseContainerSupport

# 禁用容器检测 (使用主机资源视图)
-XX:-UseContainerSupport
```

**检测链详情**:
```
UseContainerSupport=true
    ↓
读取容器内存限制 (Container Memory Limit)
├── cgroup v1: /sys/fs/cgroup/memory/memory.limit_in_bytes
│   如果值 ≥ 主机物理内存，视为无限制
└── cgroup v2: /sys/fs/cgroup/memory.max
    如果值为 "max"，视为无限制
    ↓
计算 JVM 可用内存 = min(容器限制, 物理内存)
    ↓
应用堆大小参数
├── 如果指定了 -Xmx: 直接使用
├── 如果指定了 MaxRAMPercentage: 可用内存 * 百分比
└── 如果都未指定: 使用默认人机工程学
    ├── 可用内存 ≤ 256MB: 堆 = 50% (MinRAMPercentage 生效)
    └── 可用内存 > 256MB: 堆 = 25% (MaxRAMPercentage 生效)
```

### MaxRAMPercentage 计算公式

```bash
# MaxRAMPercentage: 当物理/容器内存 > 256MB 时使用 (默认 25.0)
# MinRAMPercentage: 当物理/容器内存 ≤ 256MB 时使用 (默认 50.0)
# InitialRAMPercentage: 初始堆大小占比 (默认 1.5625)

# 注意: MinRAMPercentage 名字有误导性，它用于小内存环境
# "Min" 指的是"最小内存环境下的百分比"，不是"最小百分比"

-XX:MaxRAMPercentage=75.0
-XX:InitialRAMPercentage=50.0
-XX:MinRAMPercentage=50.0
```

**计算示例**:

| 容器内存限制 | MaxRAMPercentage | 计算的最大堆 | 非堆预留 |
|-------------|-----------------|-------------|---------|
| 256MB | 50.0% (MinRAM) | 128MB | 128MB |
| 512MB | 75.0% | 384MB | 128MB |
| 1GB | 75.0% | 768MB | 256MB |
| 2GB | 75.0% | 1536MB | 512MB |
| 4GB | 75.0% | 3072MB | 1024MB |

**内存预算 (Memory Budget)**:
```
容器内存限制 = JVM 堆 + 元空间 + 线程栈 + 直接内存 + JIT 代码缓存 + GC 开销 + 本地库
              │         │        │          │           │              │         │
              Xmx     ~100MB   每线程1MB  MaxDirect  ~240MB       ~5-10%堆   变化
```

**典型配置推荐**:
```bash
# 小容器 (256MB-512MB): 保守配置
-XX:MaxRAMPercentage=50.0 -XX:MaxDirectMemorySize=32m -Xss256k

# 中容器 (1GB-2GB): 标准配置
-XX:MaxRAMPercentage=70.0 -XX:MaxDirectMemorySize=128m

# 大容器 (4GB+): 激进配置
-XX:MaxRAMPercentage=75.0 -XX:MaxDirectMemorySize=256m

# 固定堆大小 (推荐生产环境, 行为可预测)
-Xms512m -Xmx512m -XX:MaxDirectMemorySize=128m -XX:MaxMetaspaceSize=128m
```

### OOM Killer 防范

容器 OOM 常见原因: 堆+非堆超限、本地内存泄漏、线程过多 (每线程 ~1MB 栈)。

```bash
# 防范措施: 限制所有内存区域
-XX:MaxRAMPercentage=70.0 -XX:MaxDirectMemorySize=128m -XX:MaxMetaspaceSize=256m
-XX:ReservedCodeCacheSize=128m -Xss512k

# 诊断: 本地内存追踪 (Native Memory Tracking)
-XX:NativeMemoryTracking=summary
jcmd <pid> VM.native_memory summary
```

---

## 5. Docker 最佳实践

### Dockerfile 优化

**基础镜像选择**:
```dockerfile
# 推荐: 使用精简 JRE 镜像
FROM eclipse-temurin:21-jre-alpine

# 或 Ubuntu 基础镜像
FROM eclipse-temurin:21-jre

# 或使用 distroless (最小攻击面)
FROM gcr.io/distroless/java21-debian12
```

### Alpine + musl 注意事项

Alpine Linux 使用 musl libc 而非 glibc，这对 JVM 有特殊影响：

```dockerfile
# Alpine 镜像 (基于 musl)
FROM eclipse-temurin:21-jre-alpine
# 镜像大小 ~100MB vs Ubuntu 的 ~250MB

# musl 的已知差异:
# 1. DNS 解析: musl 不支持 glibc 的 nsswitch.conf
# 2. 线程栈: musl 默认栈大小较小 (128KB vs glibc 8MB)
# 3. 内存分配: musl 的 malloc 实现与 glibc 不同
# 4. 本地库: 依赖 glibc 的 JNI 库无法在 Alpine 上使用

# 解决 DNS 问题 (Kubernetes 中常见)
RUN echo "hosts: files dns" > /etc/nsswitch.conf

# 如果需要 glibc 兼容
FROM eclipse-temurin:21-jre-alpine
RUN apk add --no-cache gcompat    # glibc 兼容层
```

**musl vs glibc 性能差异**:

| 场景 | glibc (Ubuntu) | musl (Alpine) | 说明 |
|------|---------------|--------------|------|
| **启动时间** | 基准 | +5-10% | musl 略慢 |
| **吞吐量** | 基准 | -3-5% | musl malloc 差异 |
| **内存占用** | 基准 | -10-20% | musl 更紧凑 |
| **镜像大小** | ~250MB | ~100MB | 显著优势 |

### 多阶段构建

```dockerfile
# 构建阶段
FROM eclipse-temurin:21-jdk AS builder
WORKDIR /app
COPY . .
RUN ./gradlew build -x test

# 运行阶段
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /app/build/libs/*.jar app.jar

ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0"

EXPOSE 8080
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

### jlink 瘦身 (Custom Runtime Image)

```dockerfile
# 阶段 1: 构建应用
FROM eclipse-temurin:21-jdk AS builder
WORKDIR /app
COPY . .
RUN ./gradlew build -x test

# 阶段 2: 分析依赖模块
FROM eclipse-temurin:21-jdk AS jlink
COPY --from=builder /app/build/libs/*.jar /app/app.jar
RUN jdeps --ignore-missing-deps --multi-release 21 \
    --print-module-deps /app/app.jar > /app/modules.txt
RUN jlink --module-path $JAVA_HOME/jmods \
    --add-modules $(cat /app/modules.txt) \
    --output /opt/custom-jre \
    --strip-debug \
    --compress zip-6 \
    --no-header-files \
    --no-man-pages

# 阶段 3: 最终镜像 (仅 OS + 自定义 JRE + 应用)
FROM alpine:3.20
RUN apk add --no-cache libc6-compat
COPY --from=jlink /opt/custom-jre /opt/java
COPY --from=builder /app/build/libs/*.jar /app/app.jar

ENV PATH="/opt/java/bin:$PATH"
RUN addgroup -S app && adduser -S app -G app
USER app

ENTRYPOINT ["java", "-XX:+UseContainerSupport", "-XX:MaxRAMPercentage=75.0", "-jar", "/app/app.jar"]
# 最终镜像可缩减到 ~50-80MB
```

### 运行配置

**资源限制**:
```bash
# 运行容器
docker run -d \
  --name myapp \
  --memory="1g" \
  --memory-swap="1g" \
  --cpus="2" \
  --cpu-shares=1024 \
  -p 8080:8080 \
  -e JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0" \
  myapp:latest

# 注意: --memory-swap 等于 --memory 表示禁用 swap
# 如果不设置 --memory-swap，默认为 memory 的 2 倍
```

**健康检查**:
```dockerfile
# Dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1
```

**日志配置**:
```bash
# JSON 日志驱动
docker run -d \
  --log-driver json-file \
  --log-opt max-size="10m" \
  --log-opt max-file="3" \
  myapp:latest
```

### Docker 安全最佳实践

- 使用非 root 用户运行 (`adduser` + `USER`)
- 使用只读文件系统 (`--read-only --tmpfs /tmp`)
- 使用特定版本标签，避免 `latest`
- 合并 RUN 指令减少镜像层数
- 清理包管理器缓存 (`rm -rf /var/lib/apt/lists/*`)

---

## 6. Kubernetes 部署

### 资源限制与 JVM 参数协调

**核心原则**: Kubernetes 的 `resources.limits.memory` 就是容器的 cgroup 内存限制，JVM 的 `MaxRAMPercentage` 基于此值计算。

```yaml
resources:
  requests:
    memory: "512Mi"    # 调度依据 (Scheduling)
    cpu: "250m"        # 250 毫核 = 0.25 CPU
  limits:
    memory: "1Gi"      # cgroup 硬限制 → JVM 以此计算堆大小
    cpu: "500m"        # 500 毫核 = 0.5 CPU → JVM 检测为 1 个 CPU
```

**CPU 毫核 (millicores) 与 JVM CPU 数映射**:

| K8s CPU Limit | CFS Quota | JVM availableProcessors() |
|---------------|-----------|--------------------------|
| 250m | 25000/100000 | 1 |
| 500m | 50000/100000 | 1 |
| 1000m (1 CPU) | 100000/100000 | 1 |
| 1500m | 150000/100000 | 2 |
| 2000m (2 CPU) | 200000/100000 | 2 |
| 4000m (4 CPU) | 400000/100000 | 4 |

### Deployment 配置

**基本配置**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: java-app
  labels:
    app: java-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: java-app
  template:
    metadata:
      labels:
        app: java-app
    spec:
      containers:
      - name: app
        image: myapp:21
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        env:
        - name: JAVA_TOOL_OPTIONS
          value: >
            -XX:+UseContainerSupport
            -XX:MaxRAMPercentage=75.0
            -XX:InitialRAMPercentage=50.0
            -XX:ActiveProcessorCount=2
            -XX:+UseZGC
            -XX:MaxGCPauseMillis=10
```

### 存活/就绪/启动探针 (Liveness/Readiness/Startup Probes)

Java 应用启动通常较慢，探针配置不当会导致 Pod 被反复杀死。

**推荐配置**:
```yaml
# startupProbe: 等待应用完全启动
# 在 startupProbe 成功之前，liveness 和 readiness 不会运行
startupProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8081
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 30
  # 最大等待: 10 + 30*5 = 160 秒

# livenessProbe: 检测应用是否存活 (死锁、无响应)
# 失败时 kubelet 会重启容器
livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8081
  periodSeconds: 10
  timeoutSeconds: 3
  failureThreshold: 3
  # 注意: 不要在 livenessProbe 中检查外部依赖
  # 否则数据库宕机会导致所有 Pod 重启 (级联故障)

# readinessProbe: 检测应用是否可以接收流量
# 失败时 Service 会移除该 Pod 的 endpoint
readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8081
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
  # 可以在 readinessProbe 中检查外部依赖
```

### ConfigMap 和 Secret

- **ConfigMap**: 存放 `application.yaml`、JVM 参数等非敏感配置，挂载到容器内
- **Secret**: 存放数据库连接、密码等敏感信息，通过环境变量或卷挂载注入
- 建议使用 `JAVA_TOOL_OPTIONS` 环境变量传递 JVM 参数 (JVM 自动读取)

### HorizontalPodAutoscaler

配置 HPA 时注意 Java 应用的特性:
- CPU 目标利用率建议 70% (JIT 编译期间 CPU 会冲高)
- 内存目标利用率建议 80% (JVM 堆使用有天花板)
- scaleDown 稳定窗口建议 300 秒 (避免 GC 峰值触发缩容)
- scaleUp 可以更激进 (60 秒窗口)

---

## 7. 镜像优化

### 镜像大小优化

| 基础镜像 | 大小 | 说明 |
|----------|------|------|
| `eclipse-temurin:25-jdk` | ~450MB | 完整 JDK (LTS) |
| `eclipse-temurin:25-jre` | ~250MB | JRE (LTS) |
| `eclipse-temurin:25-jre-alpine` | ~100MB | Alpine JRE (LTS) |
| `eclipse-temurin:21-jre-alpine` | ~100MB | Alpine JRE (上一 LTS) |
| `gcr.io/distroless/java21` | ~150MB | Distroless |
| **jlink 自定义 JRE + Alpine** | **~50-80MB** | **最小化** |

> **注意**: Oracle 提供基于 Oracle Linux 的容器镜像，覆盖 JDK 26、25、21、17、11、8 版本。JDK 25 为当前 LTS，推荐新项目使用。

### 启动优化

**CDS / AppCDS**: 在 Dockerfile 中预生成类共享归档 (Class Data Sharing archive)，减少启动时间:

```dockerfile
# 方式 1: 默认 CDS
RUN java -Xshare:dump -XX:SharedArchiveFile=/opt/java/.cache/app.jsa
ENTRYPOINT ["java", "-Xshare:on", "-XX:SharedArchiveFile=/opt/java/.cache/app.jsa", "-jar", "app.jar"]

# 方式 2: AppCDS (包含应用类)
RUN java -XX:ArchiveClassesAtExit=/opt/java/.cache/app.jsa -jar app.jar
ENTRYPOINT ["java", "-XX:SharedArchiveFile=/opt/java/.cache/app.jsa", "-jar", "app.jar"]
```

---

## 8. GraalVM Native Image

### 容器中的 Native Image 优势

GraalVM Native Image 将 Java 应用 AOT 编译为原生可执行文件，在容器环境中有显著优势：

| 指标 | JVM (JIT) | Native Image | 改进 |
|------|-----------|-------------|------|
| **启动时间 (Startup Time)** | 2-10 秒 | 10-100 毫秒 | 10-100x |
| **内存占用 (RSS)** | 200-500MB | 30-100MB | 3-5x |
| **镜像大小** | 100-250MB | 20-80MB | 3-5x |
| **峰值吞吐量 (Peak Throughput)** | 基准 | -10-30% | JIT 更优 |
| **预热时间 (Warmup)** | 需要预热 | 无需预热 | 显著 |

### Dockerfile 示例

```dockerfile
# 阶段 1: 使用 GraalVM 构建 Native Image
FROM ghcr.io/graalvm/native-image:21 AS builder
WORKDIR /app
COPY . .
RUN ./gradlew nativeCompile

# 阶段 2: 最小运行镜像 (无需 JVM)
FROM gcr.io/distroless/base-debian12
COPY --from=builder /app/build/native/nativeCompile/myapp /app/myapp
EXPOSE 8080
ENTRYPOINT ["/app/myapp"]
# 最终镜像 ~20-50MB，启动时间 <100ms
```

### 容器资源检测

```bash
# Native Image 也支持容器资源检测
# 启动参数通过构建时或运行时 flag 传递

# 构建时指定 (编译进二进制)
native-image -H:+UseContainerSupport ...

# 运行时 flag
./myapp -XX:MaxRAMPercentage=75.0

# Native Image 的 GC 选项
# Serial GC (默认, 适合小内存容器)
# G1 GC (需要 GraalVM Enterprise / Oracle GraalVM)
native-image --gc=serial ...   # 低内存占用
native-image --gc=G1 ...       # 高吞吐
```

### 适用场景

| 场景 | 推荐方式 | 原因 |
|------|----------|------|
| **Serverless / FaaS** | Native Image | 冷启动 (Cold Start) 性能关键 |
| **Sidecar 容器** | Native Image | 资源占用要求极低 |
| **高密度微服务** | Native Image | 每容器内存最小化 |
| **高吞吐量服务** | JVM (JIT) | JIT 优化后峰值性能更高 |
| **长时间运行服务** | JVM (JIT) | JIT Profile-Guided 优化更好 |
| **动态反射密集** | JVM (JIT) | Native Image 需要额外配置 |

---

## 9. JFR 容器内分析

### 容器内 JFR 配置

JFR (Java Flight Recorder) 在容器内的使用需要特别注意存储和提取。

**启动时开启 JFR**:
```bash
# 持续记录 (Continuous Recording)
-XX:StartFlightRecording=maxsize=100m,maxage=24h,disk=true,\
    filename=/logs/recording.jfr,\
    settings=profile

# 轻量记录 (Low Overhead, 生产推荐)
-XX:StartFlightRecording=maxsize=50m,maxage=12h,disk=true,\
    filename=/logs/recording.jfr,\
    settings=default
# default 设置 ~1% 性能开销
# profile 设置 ~2-3% 性能开销
```

**运行时控制 JFR**:
```bash
# 在容器内使用 jcmd
kubectl exec -it <pod-name> -- jcmd 1 JFR.start \
    duration=60s filename=/logs/diagnostic.jfr settings=profile

# 检查 JFR 状态
kubectl exec -it <pod-name> -- jcmd 1 JFR.check

# 导出正在运行的记录
kubectl exec -it <pod-name> -- jcmd 1 JFR.dump filename=/logs/dump.jfr

# 停止记录
kubectl exec -it <pod-name> -- jcmd 1 JFR.stop name=1
```

### 从容器中提取 JFR 文件

```bash
# 从 Kubernetes Pod 拷贝 JFR 文件
kubectl cp <pod-name>:/logs/recording.jfr ./recording.jfr

# 从 Docker 容器拷贝
docker cp <container-id>:/logs/recording.jfr ./recording.jfr

# 使用 JDK Mission Control (JMC) 分析
jmc ./recording.jfr
```

### 容器特定的 JFR 事件

JFR 自动记录容器相关事件: `jdk.ContainerConfiguration` (容器配置)、`jdk.ContainerCPUUsage` (CPU 使用率)、`jdk.ContainerMemoryUsage` (内存使用)、`jdk.ContainerCPUThrottling` (CPU 节流)。使用 `jfr print --events jdk.ContainerCPUThrottling recording.jfr` 查看。

### Kubernetes 中的 JFR 存储方案

- **emptyDir**: 临时存储，Pod 重启丢失，适合临时诊断
- **PersistentVolume**: 持久存储，适合长期记录
- **Sidecar 上传**: Sidecar 容器监控 JFR 文件并上传到 S3/MinIO

---

## 10. 监控和诊断

### Prometheus 指标

- **JMX Exporter**: 使用 `-javaagent` 方式部署，在 `JAVA_TOOL_OPTIONS` 中添加 `-javaagent:/opt/jmx-exporter/jmx_prometheus_javaagent.jar=8081:config.yaml`
- **Micrometer (Spring Boot)**: 在 `management.endpoints.web.exposure.include` 中添加 `prometheus` endpoint

### 日志收集

常用方案: Fluentd / Fluent Bit 作为 DaemonSet 收集 `/var/log/containers/*.log`，发送到 Elasticsearch 或其他日志存储。GC 日志和 JFR 文件建议输出到 emptyDir 卷，由 sidecar 或定时任务上传。

---

## 11. 常见问题

### 问题 1: 内存检测不准确 (OOM Killed)

**症状**:
- JVM 分配内存超出容器限制
- 容器被 OOM Killer 终止 (`Exit Code 137`)

**解决方案**:
```bash
# 使用百分比 (留出空间给非堆内存)
-XX:MaxRAMPercentage=70.0

# 或明确指定 (更可预测)
-Xmx512m

# 限制直接内存和元空间
-XX:MaxDirectMemorySize=128m
-XX:MaxMetaspaceSize=256m

# 诊断: 查看被 kill 的原因
kubectl describe pod <pod-name> | grep -A5 "Last State"
# 如果 reason 为 OOMKilled，增加 memory limit 或减少堆大小

# 诊断: 查看容器内存使用详情
kubectl exec -it <pod-name> -- jcmd 1 VM.native_memory summary
```

### 问题 2: CPU 检测错误

**症状**:
- 线程数过多或过少
- CPU Throttling (CFS 节流) 严重

**解决方案**:
```bash
# 明确指定 CPU 数
-XX:ActiveProcessorCount=4

# 验证检测结果
jcmd <pid> VM.flags | grep -i container
jcmd <pid> VM.info | grep "active_processor_count"

# 检查 CPU Throttling
cat /sys/fs/cgroup/cpu/cpu.stat
# nr_throttled: 节流次数
# throttled_time: 累计节流时间 (纳秒)
# 如果频繁节流，考虑增加 CPU limit 或减少并行线程
```

### 问题 3: 启动时间慢 (Slow Startup)

**症状**:
- 容器启动时间长
- 就绪探针超时

**解决方案**:
```bash
# 使用 CDS / AppCDS
-XX:SharedArchiveFile=app.jsa

# 使用 startupProbe (而非增加 livenessProbe 的 initialDelaySeconds)
startupProbe:
  failureThreshold: 30
  periodSeconds: 5

# 考虑 GraalVM Native Image (启动时间 <100ms)
# 考虑 AOT 缓存 (JDK 25+)
```

### 问题 4: cgroup v2 不兼容

**症状**: 升级到 cgroup v2 宿主机后，JVM 不识别容器限制，使用主机全部资源。

**解决方案**: 升级 JDK 到 21+ (完整 cgroup v2 支持)。JDK 15-20 有部分支持但存在 bug。使用 `-Xlog:os+container=trace` 查看检测日志。临时方案: 手动指定 `-Xmx512m -XX:ActiveProcessorCount=2`。

---

## 12. 最佳实践清单

### Docker

- [ ] 使用精简基础镜像 (Alpine 或 Distroless)
- [ ] 多阶段构建 (Multi-stage Build)
- [ ] 考虑 jlink 创建自定义 JRE 瘦身
- [ ] 非 root 用户运行
- [ ] 健康检查配置
- [ ] 资源限制设置 (`--memory`, `--cpus`)
- [ ] 日志配置 (大小限制)
- [ ] Alpine + musl 兼容性测试

### Kubernetes

- [ ] 资源请求和限制 (requests/limits)
- [ ] 三种探针配置 (startup/liveness/readiness)
- [ ] livenessProbe 不检查外部依赖
- [ ] ConfigMap 和 Secret 管理配置
- [ ] HPA 配置 (水平自动伸缩)
- [ ] Pod 反亲和性 (高可用)
- [ ] 优雅终止 (preStop + terminationGracePeriod)

### JVM

- [ ] 确认 UseContainerSupport 已启用 (默认)
- [ ] 配置 MaxRAMPercentage (70-75%)
- [ ] 限制非堆内存 (MaxDirectMemorySize, MaxMetaspaceSize)
- [ ] 在 cpu.shares 场景下手动设置 ActiveProcessorCount
- [ ] 选择合适的 GC (ZGC/G1/Shenandoah)
- [ ] 开启 JFR 持续记录
- [ ] 配置 GC 日志
- [ ] 开启 NativeMemoryTracking (诊断用)

---

## 13. 相关链接

- [Docker 最佳实践](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Kubernetes 文档](https://kubernetes.io/docs/)
- [JDK 容器支持](/jeps/platform/jep-307.md)
- [性能优化](/by-topic/core/performance/)
