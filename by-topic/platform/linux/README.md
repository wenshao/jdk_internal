# Linux 平台

Linux 是 JDK 开发和部署的主要平台，拥有最完善的支持和最佳性能。

---
## 目录

1. [概述](#1-概述)
2. [容器支持](#2-容器支持)
3. [cgroup 支持](#3-cgroup-支持)
4. [信号处理](#4-信号处理)
5. [内存管理](#5-内存管理)
6. [线程模型](#6-线程模型)
7. [文件系统与 /proc 接口](#7-文件系统与-proc-接口)
8. [Alpine/musl 支持](#8-alpinemusl-支持)
9. [性能调优](#9-性能调优)
10. [系统调用优化](#10-系统调用优化)
11. [监控和诊断](#11-监控和诊断)
12. [常见问题解决](#12-常见问题解决)
13. [相关链接](#13-相关链接)

---


## 1. 概述

### 支持的架构

| 架构 | 状态 | 说明 |
|------|------|------|
| **x64 (AMD64)** | ✅ 主要平台 | 最广泛支持 |
| **aarch64 (ARM64)** | ✅ 主要平台 | 云服务器常用 |
| **ppc64le (PowerPC)** | ✅ 支持 | IBM Power 系统 |
| **s390x (z Systems)** | ✅ 支持 | IBM 大型机 |
| **arm32** | ⚠️ 有限支持 | 嵌入式设备 |
| **riscv64** | ✅ GA (JDK 19+) | 新兴架构 |

### 支持的发行版

| 发行版 | 最低版本 | 推荐 |
|--------|----------|------|
| **RHEL/CentOS** | 7.x | 8.x/9.x |
| **Ubuntu** | 18.04 LTS | 22.04 LTS/24.04 LTS |
| **Debian** | 10 | 12 |
| **SLES** | 12 | 15 |
| **Amazon Linux** | 2 | 2023 |
| **Alpine Linux** | 3.14 | 3.19+ (musl libc) |

---

## 2. 容器支持

### 演进时间线

```
JDK 8  ──── 无容器感知 (Container-Unaware)
          │   - Runtime.availableProcessors() 返回宿主机核心数
          │   - 堆大小基于宿主机物理内存计算
          │
JDK 10 ──── 容器感知 (JEP 307 / JDK-8146115)
          │   - 自动检测 cgroup v1 的 CPU/内存限制
          │   - -XX:+UseContainerSupport (默认启用)
          │   - Runtime.availableProcessors() 尊重 CPU 配额
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
          │
JDK 26 ──── 容器优化增强
              - 更精确的资源检测
              - 性能优化
```

### UseContainerSupport 机制详解

JVM 在启动时通过读取 cgroup 文件系统来检测容器环境。检测链路:

```
JVM 启动
  └─ os::Linux::is_containerized()
       ├─ 检查 /proc/self/cgroup 是否存在非根 cgroup
       ├─ 检查 /proc/1/sched 中的 PID 是否为 1
       └─ 读取 cgroup 文件获取限制值
            ├─ CPU:  cpu.cfs_quota_us / cpu.cfs_period_us  (v1)
            │        cpu.max                                (v2)
            ├─ 内存: memory.limit_in_bytes                  (v1)
            │        memory.max                             (v2)
            └─ 影响: -Xmx 默认值, GC 线程数, ForkJoinPool 并行度
```

### 容器感知配置

```bash
# 默认启用 (JDK 10+)
-XX:+UseContainerSupport

# CPU 配置
-XX:ActiveProcessorCount=4       # 手动指定 (整数值，覆盖自动检测)

# 内存配置
-XX:MaxRAMPercentage=75.0        # 使用容器内存的 75%
-XX:InitialRAMPercentage=50.0    # 初始使用 50%
-XX:MinRAMPercentage=25.0        # 小堆场景的最大百分比阈值

# 禁用容器支持 (不推荐)
-XX:-UseContainerSupport
```

### Docker 最佳实践

**Dockerfile 示例**:
```dockerfile
# 使用精简基础镜像
FROM eclipse-temurin:21-jre-alpine

# 或使用 Ubuntu 基础镜像
FROM ubuntu:22.04

# 设置工作目录
WORKDIR /app

# 复制应用
COPY app.jar /app/

# 暴露端口
EXPOSE 8080

# JVM 参数
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0"

# 启动命令
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

**运行命令**:
```bash
# 运行容器
docker run -d \
  --name myapp \
  --memory="1g" \
  --cpus="2" \
  -p 8080:8080 \
  myapp:latest

# 验证资源检测
docker exec myapp jcmd 1 VM.flags | grep -i container
```

### Kubernetes 部署

**Deployment 配置**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: java-app
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
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

---

## 3. cgroup 支持

### cgroup v1 vs v2

| 特性 | cgroup v1 | cgroup v2 |
|------|-----------|-----------|
| **JDK 支持** | JDK 8u191+ | JDK 15+ 部分, JDK 21+ 完整 |
| **内存检测** | ✅ memory.limit_in_bytes | ✅ memory.max |
| **CPU 检测** | ✅ cpu.cfs_quota_us | ✅ cpu.max |
| **层级结构** | 每个控制器独立层级 | 统一层级 (unified hierarchy) |
| **默认发行版** | RHEL 7/8, Ubuntu <21.10 | RHEL 9, Ubuntu 21.10+, Fedora 31+ |

### cgroup v1 配置

**检测 cgroup 版本**:
```bash
# 检查是否使用 cgroup v1
mount | grep cgroup

# 或检查 cgroup v2 (unified hierarchy)
mount | grep cgroup2

# 确认容器内 cgroup 版本
stat -fc %T /sys/fs/cgroup/
# "tmpfs" → cgroup v1,  "cgroup2fs" → cgroup v2
```

**cgroup v1 路径**:
```
/sys/fs/cgroup/memory/memory.limit_in_bytes
/sys/fs/cgroup/memory/memory.usage_in_bytes
/sys/fs/cgroup/cpu/cpu.cfs_quota_us
/sys/fs/cgroup/cpu/cpu.cfs_period_us
```

### cgroup v2 配置

**cgroup v2 路径**:
```
/sys/fs/cgroup/memory.max
/sys/fs/cgroup/memory.current
/sys/fs/cgroup/cpu.max          # 格式: "quota period" 如 "200000 100000"
/sys/fs/cgroup/cpu.stat
```

**JDK 21+ cgroup v2 支持**:
```bash
# JDK 21+ 自动检测 cgroup v2
# 无需额外配置

# 验证检测
jcmd <pid> VM.flags | grep -i container

# 输出示例
bool UseContainerSupport = true
```

### 常见问题

**问题 1: 内存检测不准确**
```bash
# 症状: JVM 分配内存超出容器限制
# 原因: cgroup v2 支持不完整 (JDK < 21)

# 解决方案
-XX:MaxRAMPercentage=75.0  # 使用百分比
-Xmx512m                    # 或明确指定
```

**问题 2: CPU 检测错误**
```bash
# 症状: 线程数过多或过少
# 原因: CPU 配额检测不准确

# 解决方案
-XX:ActiveProcessorCount=4  # 明确指定
```

**问题 3: OOM Killer 终止容器**
```bash
# 症状: 容器被 OOM Killer 终止 (dmesg 中出现 "oom-kill")
# 原因: JVM 原生内存 (native memory) + 堆内存超出 cgroup 限制

# 解决方案
-XX:MaxRAMPercentage=70.0  # 留出更多空间给原生内存
-XX:MaxDirectMemorySize=128m  # 限制直接内存
-XX:NativeMemoryTracking=summary  # 启用 NMT 追踪原生内存
```

---

## 4. 信号处理

### JVM 信号映射

Linux 信号是 JVM 异常处理和进程管理的底层机制:

| 信号 | 编号 | JVM 用途 | 说明 |
|------|------|----------|------|
| **SIGSEGV** | 11 | NullPointerException, 安全点轮询 (safepoint polling) | JVM 截获段错误，区分空指针与真正的崩溃 |
| **SIGBUS** | 7 | 内存映射错误 | 访问已截断文件的 mmap 区域时触发 |
| **SIGFPE** | 8 | ArithmeticException (除零) | 整数除以零时触发 |
| **SIGILL** | 4 | 非法指令 | 执行不支持的 CPU 指令时触发 |
| **SIGQUIT** | 3 | 线程转储 (Thread Dump) | `kill -3 <pid>` 输出所有线程栈 |
| **SIGHUP** | 1 | 日志轮转 | 部分应用用于重新加载配置 |
| **SIGTERM** | 15 | 正常关闭 | 触发 shutdown hook |
| **SIGKILL** | 9 | 强制终止 | 无法捕获，不执行 shutdown hook |

### 信号链 (Signal Chaining) — libjsig

当 JVM 与使用信号的本地库 (如 GPGPU 框架) 共存时，需要使用信号链避免冲突:

```bash
# 使用 libjsig 启用信号链
export LD_PRELOAD=$JAVA_HOME/lib/libjsig.so
java -jar app.jar

# 工作原理:
# 1. libjsig 拦截 sigaction() 调用
# 2. 本地库注册的信号处理器被记录
# 3. JVM 收到信号时，先调用本地库的处理器
# 4. 如果本地库不处理，JVM 自行处理
```

### SIGSEGV 与 NullPointerException 的关系

```
Java 代码: obj.method()  (obj == null)
     │
     ▼
CPU 访问地址 0x0 (或附近)
     │
     ▼
MMU 产生页错误 → 内核发送 SIGSEGV
     │
     ▼
JVM 信号处理器检查故障地址:
  ├─ 地址在低地址区域 → 转换为 NullPointerException
  ├─ 地址在安全点轮询页 → 触发 safepoint
  └─ 其他地址 → 真正的崩溃，生成 hs_err_pid.log
```

### 诊断信号相关崩溃

```bash
# 查看 JVM 崩溃日志中的信号信息
# hs_err_pid<pid>.log 中会包含:
#   siginfo: si_signo: 11 (SIGSEGV), si_code: 1 (SEGV_MAPERR), si_addr: 0x0000000000000000

# 检查进程收到的信号
strace -e signal -p <pid>

# 查看 JVM 已注册的信号处理器
jcmd <pid> VM.info | grep -A 20 "Signal Handlers"
```

---

## 5. 内存管理

### mmap / madvise

JVM 堆、Code Cache、Metaspace 等均通过 `mmap` 分配:

```bash
# JVM 堆分配的典型 mmap 调用
mmap(NULL, heap_size, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_NORESERVE, -1, 0)

# JVM 使用 madvise 提示内核优化内存行为
madvise(addr, len, MADV_DONTNEED)   # ZGC/Shenandoah 回收时释放物理页
madvise(addr, len, MADV_HUGEPAGE)   # 请求透明大页
```

### 大页支持 (Large Pages / Huge Pages)

大页减少 TLB (Translation Lookaside Buffer) 缺失，对大堆 JVM 有显著性能提升:

| 类型 | 页大小 | 配置方式 | 特点 |
|------|--------|----------|------|
| **HugeTLB (显式大页)** | 2MB / 1GB | 预先分配，需 root | 内存预留，不可被回收 |
| **THP (透明大页)** | 2MB | 内核自动管理 | 按需合并，可能有延迟抖动 |

```bash
# === HugeTLB 显式大页 ===
# 1. 系统配置: 预留大页 (需要 root)
echo 4096 > /proc/sys/vm/nr_hugepages       # 预留 4096 个 2MB 大页 = 8GB
# 或在启动参数中:
# kernel: hugepages=4096

# 2. 验证预留
grep Huge /proc/meminfo
# HugePages_Total:    4096
# HugePages_Free:     4096
# Hugepagesize:       2048 kB

# 3. JVM 配置
-XX:+UseLargePages -XX:LargePageSizeInBytes=2m

# === THP 透明大页 ===
# 系统启用
echo always > /sys/kernel/mm/transparent_hugepage/enabled

# JVM 配置 (JDK 14+)
-XX:+UseTransparentHugePages
```

### NUMA 感知 (Non-Uniform Memory Access)

多插槽服务器上，NUMA 感知可避免跨节点内存访问 (remote access) 的延迟惩罚:

```bash
# 查看 NUMA 拓扑
numactl --hardware
# available: 2 nodes (0-1)
# node 0 cpus: 0-15
# node 1 cpus: 16-31

# JVM NUMA 感知 (Parallel GC 和 G1 支持)
-XX:+UseNUMA                   # 启用 NUMA 感知堆分配
-XX:+UseParallelGC             # Parallel GC 的 NUMA 支持最完善

# 操作系统级别绑定
numactl --cpunodebind=0 --membind=0 java -jar app.jar
```

---

## 6. 线程模型

### pthread 与 JVM 线程

JVM 平台线程 (platform thread) 与 Linux pthread 1:1 映射:

```
Java Thread                     Linux 内核
├─ Thread.start()          →    pthread_create()
├─ synchronized            →    futex()
├─ Object.wait()           →    futex() + FUTEX_WAIT
├─ Thread.sleep()          →    clock_nanosleep()
└─ Thread 终止             →    pthread_exit()
```

```bash
# 默认线程栈大小
-Xss1m                        # 平台线程默认 1MB 栈 (可调整)
-XX:ThreadStackSize=1024       # 同上 (以 KB 为单位)

# 查看 JVM 创建的 pthread 数量
ls /proc/<pid>/task/ | wc -l

# 查看线程栈使用
pmap -x <pid> | grep -c "\[stack\]"
```

### 虚拟线程 (Virtual Threads) 与 epoll/io_uring

虚拟线程 (JDK 21+, JEP 444) 使用少量载体线程 (carrier thread) 支撑大量虚拟线程:

```
虚拟线程模型:
  Virtual Thread (数百万级)
       │ 挂载 (mount) / 卸载 (unmount)
       ▼
  Carrier Thread (= CPU 核心数)    ← ForkJoinPool
       │ 1:1 映射
       ▼
  OS pthread

I/O 多路复用:
  虚拟线程执行阻塞 I/O
       │
       ▼
  JVM 将 I/O 注册到 Poller
       │
       ▼
  Linux epoll_wait() 等待就绪        ← 目前 JDK 使用 epoll
       │
       ▼
  I/O 就绪 → 虚拟线程重新调度
```

```bash
# 虚拟线程相关调优
-Djdk.virtualThreadScheduler.parallelism=8     # 载体线程数
-Djdk.virtualThreadScheduler.maxPoolSize=256   # 载体线程池上限

# 监控虚拟线程 (JFR 事件)
-XX:StartFlightRecording=settings=profile
# 查看 jdk.VirtualThreadPinned 事件以诊断钉住 (pinning) 问题
```

---

## 7. 文件系统与 /proc 接口

### JVM 使用的关键 /proc 文件

| 路径 | JVM 用途 | 说明 |
|------|----------|------|
| `/proc/self/maps` | NMT (Native Memory Tracking) | 内存映射区域，验证 mmap 分配 |
| `/proc/self/status` | 内存统计 | VmRSS, VmSize 等与 NMT 对照 |
| `/proc/self/cgroup` | 容器检测 | 确定 cgroup 路径与层级 |
| `/proc/cpuinfo` | CPU 特性检测 | 指令集、核心数 |
| `/proc/meminfo` | 物理内存 | 总内存、可用内存 |
| `/proc/sys/vm/*` | 内核参数 | 大页、swappiness 等 |

### NMT 验证: /proc/self/maps 与 /proc/self/status

```bash
# 启用 NMT (Native Memory Tracking)
-XX:NativeMemoryTracking=summary   # 或 detail

# 查看 NMT 报告
jcmd <pid> VM.native_memory summary

# 与 /proc 数据对照验证
cat /proc/<pid>/status | grep -E "VmRSS|VmSize|VmPeak"
# VmPeak:  5234567 kB    ← 进程峰值虚拟内存
# VmSize:  4987654 kB    ← 当前虚拟内存
# VmRSS:   1234567 kB    ← 驻留集大小 (实际物理内存)

# /proc/self/maps 显示详细内存映射 (NMT detail 模式可与之对照)
cat /proc/<pid>/maps | head -20
# 地址范围        权限  偏移   设备  inode  路径
# 00400000-00401000 r-xp 00000000 fd:01 12345 /usr/lib/jvm/.../java
```

### tmpfs 与 JVM

```bash
# tmpfs 用于高性能临时文件 (基于内存)
# JVM 可将 CodeCache dump、JFR 录制等放在 tmpfs 上
mount -t tmpfs -o size=512m tmpfs /mnt/jvm-tmp
-XX:StartFlightRecording=filename=/mnt/jvm-tmp/recording.jfr
```

---

## 8. Alpine/musl 支持

### JEP 386: Alpine Linux Port (musl libc)

JDK 16 通过 JEP 386 正式提供 Alpine Linux (musl libc) 移植版本:

| 对比项 | glibc | musl libc |
|--------|-------|-----------|
| **镜像大小** | ~200MB+ (基础镜像) | ~5MB (Alpine 基础镜像) |
| **JRE 镜像大小** | ~250-350MB | ~100-150MB |
| **内存占用** | 标准 | 稍低 (malloc 实现差异) |
| **线程栈默认大小** | 8MB (系统默认) | 80KB (系统默认) |
| **DNS 解析** | nsswitch.conf | 不支持 nsswitch，使用 musl 内置 |
| **locale 支持** | 完整 ICU/glibc locale | 有限 (无 glibc locale) |
| **性能** | 通常更好 (更优化的 malloc) | 接近，某些场景略低 |

### glibc vs musl 的关键差异

```bash
# 1. 线程栈大小 — musl 默认 80KB，可能导致 StackOverflowError
#    解决方案: 显式指定
-Xss512k

# 2. DNS 解析差异 — musl 不使用 nsswitch.conf
#    Alpine 中 /etc/nsswitch.conf 不生效
#    如需自定义 DNS 行为，编辑 /etc/resolv.conf

# 3. 时区数据 — Alpine 需要单独安装
apk add tzdata

# 4. 字体渲染 — 需要单独安装字体库
apk add fontconfig ttf-dejavu
```

### 容器镜像大小优化

```dockerfile
# === 最小化 Alpine + JRE 镜像 ===
FROM eclipse-temurin:21-jre-alpine
# 最终镜像 ~100MB

# === 使用 jlink 自定义运行时 ===
FROM eclipse-temurin:21-jdk-alpine AS builder
RUN jlink --add-modules java.base,java.logging,java.net.http \
          --strip-debug --no-man-pages --no-header-files \
          --output /opt/jre-minimal

FROM alpine:3.19
COPY --from=builder /opt/jre-minimal /opt/jre
COPY app.jar /app/
ENTRYPOINT ["/opt/jre/bin/java", "-jar", "/app/app.jar"]
# 最终镜像 ~50MB

# === 使用 Distroless (glibc) 作为替代 ===
FROM gcr.io/distroless/java21-debian12
COPY app.jar /app/app.jar
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
# 安全性高 (无 shell, 无包管理器)，~200MB
```

---

## 9. 性能调优

### Kernel 参数调优

```bash
# === 内存相关 ===
# vm.swappiness: 控制换页倾向 (0-100)
# 对于 JVM，低值减少换页停顿
sysctl -w vm.swappiness=10                  # 生产推荐 (默认 60)

# transparent_hugepage: 透明大页策略
echo madvise > /sys/kernel/mm/transparent_hugepage/enabled
# "always" → 所有进程启用 (可能导致延迟抖动)
# "madvise" → 仅对 madvise(MADV_HUGEPAGE) 区域启用 (JVM 推荐)
# "never"  → 禁用

# THP defrag 策略
echo defer+madvise > /sys/kernel/mm/transparent_hugepage/defrag
# 避免同步碎片整理导致的延迟尖峰

# === 文件系统 / I/O ===
sysctl -w vm.dirty_ratio=10                 # 脏页比例阈值
sysctl -w vm.dirty_background_ratio=5       # 后台写回阈值

# === 网络 ===
sysctl -w net.core.somaxconn=65535
sysctl -w net.ipv4.tcp_max_syn_backlog=65535
sysctl -w net.ipv4.tcp_tw_reuse=1
sysctl -w net.ipv4.tcp_fin_timeout=30
```

### CPU 优化

**CPU 亲和性**:
```bash
# 绑定到特定 CPU 核心
taskset -c 0-3 java -jar app.jar

# 或使用 numactl
numactl --cpunodebind=0 --membind=0 java -jar app.jar
```

**调度器优化**:
```bash
# 设置调度器策略
chrt -f 50 java -jar app.jar  # FIFO 实时调度
```

### I/O 优化

**文件系统选择**:
| 文件系统 | 性能 | 特性 | 推荐 |
|----------|------|------|------|
| **ext4** | 良好 | 稳定、广泛支持 | ✅ 通用 |
| **XFS** | 优秀 | 大文件、高并发 | ✅ 数据密集 |
| **Btrfs** | 良好 | 快照、压缩 | ⚠️ 特定场景 |

**I/O 调度器**:
```bash
# 查看当前调度器
cat /sys/block/sda/queue/scheduler

# 设置调度器
echo none > /sys/block/sda/queue/scheduler     # NVMe SSD (noop)
echo mq-deadline > /sys/block/sda/queue/scheduler  # 数据库负载
```

### perf / bpftrace 集成

```bash
# === perf: CPU 性能分析 ===
# 需要 -XX:+PreserveFramePointer 以获取准确的 Java 栈帧
java -XX:+PreserveFramePointer -jar app.jar &

# 采样 CPU 火焰图
perf record -g -p <pid> -- sleep 30
perf script | stackcollapse-perf.pl | flamegraph.pl > flamegraph.svg

# JDK 17+ 支持 perf map 文件 (自动生成)
-XX:+DumpPerfMapAtExit          # 退出时生成 /tmp/perf-<pid>.map
-XX:+PreserveFramePointer       # 保留帧指针以便 perf 解析

# === bpftrace: 动态追踪 ===
# 追踪 JVM 的 mmap 调用
bpftrace -e 'tracepoint:syscalls:sys_enter_mmap /pid == <pid>/ {
  printf("mmap: len=%lu, prot=%d\n", args->len, args->prot);
}'

# 追踪 GC STW (Stop-The-World) 暂停
# 利用 JVM USDT 探针 (需要编译时启用 --enable-dtrace)
bpftrace -e 'usdt:/path/to/libjvm.so:gc__begin { printf("GC begin\n"); }
             usdt:/path/to/libjvm.so:gc__end   { printf("GC end\n"); }'
```

---

## 10. 系统调用优化

### 关键系统调用

| 系统调用 | 用途 | 优化建议 |
|----------|------|----------|
| **epoll** | 事件通知 (NIO, 虚拟线程 I/O) | 默认使用，性能优秀 |
| **io_uring** | 异步 I/O | 实验性，尚未正式支持 |
| **futex** | 线程同步 (synchronized, ReentrantLock) | 默认使用 |
| **mmap** | 内存映射 (堆、Code Cache) | 大文件场景 |
| **clone3** | 线程创建 | JDK 内部使用 pthread_create |

### io_uring 支持

**io_uring (尚未正式支持)**:

OpenJDK 目前没有内置 io_uring 支持。社区有第三方库（如 JUring）通过 Panama FFM API 提供 io_uring 绑定，但 JDK 本身尚无官方 io_uring 集成。

```bash
# 检查内核是否支持 io_uring (Linux 5.1+)
uname -r  # 需要 5.1+
```

---

## 11. 监控和诊断

### 系统监控

**进程监控**:
```bash
# CPU 使用
top -p <pid>

# 内存使用
pmap -x <pid>

# 线程状态
ps -eLf | grep java

# 打开文件
lsof -p <pid>
```

**系统指标**:
```bash
# CPU
cat /proc/cpuinfo
mpstat 1

# 内存
free -h
cat /proc/meminfo

# I/O
iostat -x 1

# 网络
ss -s
```

### JVM 监控

**JFR 配置**:
```bash
# 启动 JFR
-XX:StartFlightRecording=duration=60s,filename=recording.jfr

# 使用 jcmd
jcmd <pid> JFR.start duration=60s filename=recording.jfr
jcmd <pid> JFR.dump filename=recording.jfr
```

**GC 日志**:
```bash
# 统一日志格式
-Xlog:gc*,safepoint:file=gc.log:time,level,tags:filecount=5,filesize=10m
```

### 性能分析

**async-profiler**:
```bash
# CPU 分析
./profiler.sh -d 60 -f cpu.html <pid>

# 内存分析
./profiler.sh -d 60 -e alloc -f alloc.html <pid>

# 锁分析
./profiler.sh -d 60 -e lock -f lock.html <pid>
```

---

## 12. 常见问题解决

### 问题 1: 启动时间慢

**诊断**:
```bash
# 检查启动时间
time java -jar app.jar

# 分析启动
-XX:+PrintCompilation
-Xlog:class+load=info
```

**解决方案**:
```bash
# 使用 CDS
java -Xshare:dump -XX:SharedArchiveFile=app.jsa -jar app.jar
java -Xshare:on -XX:SharedArchiveFile=app.jsa -jar app.jar

# 减少验证
-Xverify:none  # 不推荐生产
```

### 问题 2: 内存使用高

**诊断**:
```bash
# 堆内存
jcmd <pid> GC.heap_info

# 原生内存
jcmd <pid> VM.native_memory summary

# 内存映射
pmap -x <pid>
```

**解决方案**:
```bash
# 调整堆大小
-Xms2g -Xmx2g

# 限制原生内存
-XX:MaxDirectMemorySize=256m
-XX:MetaspaceSize=256m
-XX:MaxMetaspaceSize=512m

# 使用 ZGC
-XX:+UseZGC -XX:MaxGCPauseMillis=10
```

### 问题 3: CPU 使用高

**诊断**:
```bash
# 线程转储
jcmd <pid> Thread.print

# CPU 分析
./profiler.sh -d 30 -f cpu.html <pid>
```

**解决方案**:
- 优化热点代码
- 减少锁竞争
- 使用更高效的算法

---

## 13. 相关链接

- [容器支持](/by-topic/platform/containers/)
- [性能优化](/by-topic/core/performance/)
- [GC 调优](/by-topic/core/gc/)
- [JDK 版本文档](/by-version/)
