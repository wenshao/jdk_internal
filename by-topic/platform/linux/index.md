# Linux 平台

Linux 是 JDK 开发和部署的主要平台，拥有最完善的支持和最佳性能。

---
## 目录

1. [概述](#1-概述)
2. [容器支持](#2-容器支持)
3. [cgroup 支持](#3-cgroup-支持)
4. [性能调优](#4-性能调优)
5. [系统调用优化](#5-系统调用优化)
6. [监控和诊断](#6-监控和诊断)
7. [常见问题解决](#7-常见问题解决)
8. [相关链接](#8-相关链接)

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

---

## 2. 容器支持

### 演进时间线

```
JDK 8  ──── 无容器感知
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
          │
JDK 26 ──── 容器优化增强
              - 更精确的资源检测
              - 性能优化
```

### 容器感知配置

```bash
# 默认启用 (JDK 10+)
-XX:+UseContainerSupport

# CPU 配置
-XX:ActiveProcessorCount=4       # 手动指定 (整数值)

# 内存配置
-XX:MaxRAMPercentage=75.0        # 使用容器内存的 75%
-XX:InitialRAMPercentage=50.0    # 初始使用 50%
-XX:MinRAMPercentage=25.0        # 最小 25%

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
| **JDK 支持** | JDK 8+ | JDK 21+ 完整 |
| **内存检测** | ✅ | ✅ (JDK 21+) |
| **CPU 检测** | ✅ | ✅ (JDK 21+) |
| **推荐版本** | 兼容性 | 新部署 |

### cgroup v1 配置

**检测 cgroup 版本**:
```bash
# 检查是否使用 cgroup v1
mount | grep cgroup

# 或检查 cgroup v2
mount | grep cgroup2
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
/sys/fs/cgroup/cpu.max
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
# 症状: 容器被 OOM Killer 终止
# 原因: 原生内存超出限制

# 解决方案
-XX:MaxRAMPercentage=70.0  # 留出更多空间给原生内存
-XX:MaxDirectMemorySize=128m  # 限制直接内存
```

---

## 4. 性能调优

### 内存优化

**大页内存**:
```bash
# 启用透明大页
echo always > /sys/kernel/mm/transparent_hugepage/enabled

# JVM 配置
-XX:+UseLargePages
-XX:+UseTransparentHugePages

# 或使用显式大页
# 首先配置系统大页
echo 8192 > /proc/sys/vm/nr_hugepages

# JVM 配置
-XX:+UseLargePages
-XX:LargePageSizeInBytes=2m
```

**内存对齐**:
```bash
# 对齐内存分配
-XX:+UseTransparentHugePages
-XX:LargePageSizeInBytes=2m
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
echo noop > /sys/block/sda/queue/scheduler  # SSD
echo deadline > /sys/block/sda/queue/scheduler  # 数据库
```

### 网络优化

**TCP 调优**:
```bash
# 系统参数
sysctl -w net.core.somaxconn=65535
sysctl -w net.ipv4.tcp_max_syn_backlog=65535
sysctl -w net.ipv4.tcp_tw_reuse=1
sysctl -w net.ipv4.tcp_fin_timeout=30

# JVM 配置
-Djava.net.preferIPv4Stack=true
```

---

## 5. 系统调用优化

### 关键系统调用

| 系统调用 | 用途 | 优化建议 |
|----------|------|----------|
| **epoll** | 事件通知 | 默认使用，性能优秀 |
| **io_uring** | 异步 I/O | 实验性，尚未正式支持 |
| **futex** | 线程同步 | 默认使用 |
| **mmap** | 内存映射 | 大文件场景 |

### io_uring 支持

**io_uring (实验性，尚未正式支持)**:
```bash
# 启用 io_uring (实验性)
-Djdk.io.useIOUring=true

# 检查内核支持
uname -r  # 需要 5.1+
```

---

## 6. 监控和诊断

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
netstat -s
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

## 7. 常见问题解决

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

## 8. 相关链接

- [容器支持](containers/)
- [性能优化](/by-topic/core/performance/)
- [GC 调优](/by-topic/core/gc/)
- [JDK 版本文档](/by-version/)