# 容器环境

容器是现代云原生应用部署的核心方式，JDK 提供了完善的容器支持。

---
## 目录

1. [概述](#1-概述)
2. [资源感知](#2-资源感知)
3. [Docker 最佳实践](#3-docker-最佳实践)
4. [Kubernetes 部署](#4-kubernetes-部署)
5. [镜像优化](#5-镜像优化)
6. [监控和诊断](#6-监控和诊断)
7. [常见问题](#7-常见问题)
8. [最佳实践清单](#8-最佳实践清单)
9. [相关链接](#9-相关链接)

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

## 2. 资源感知

### CPU 感知

**自动检测**:
```bash
# JDK 10+ 自动检测 CPU 限制
-XX:+UseContainerSupport  # 默认启用
-XX:ActiveProcessorCount=auto
```

**手动指定**:
```bash
# 明确指定 CPU 数量
-XX:ActiveProcessorCount=4

# 影响:
# - GC 线程数
# - JIT 编译线程数
# - ForkJoinPool 并行度
```

**检测逻辑**:
```
容器 CPU 配额 → JVM 检测 → 计算有效 CPU 数
     ↓              ↓              ↓
cpu.cfs_quota_us  读取 cgroup  min(配额, 实际)
cpu.cfs_period_us
```

### 内存感知

**自动检测**:
```bash
# JDK 10+ 自动检测内存限制
-XX:+UseContainerSupport  # 默认启用

# 使用百分比 (推荐)
-XX:MaxRAMPercentage=75.0
-XX:InitialRAMPercentage=50.0
-XX:MinRAMPercentage=25.0
```

**手动指定**:
```bash
# 明确指定堆大小
-Xmx512m -Xms512m

# 或使用百分比
-XX:MaxRAMPercentage=75.0
```

**检测逻辑**:
```
容器内存限制 → JVM 检测 → 计算堆大小
     ↓              ↓            ↓
memory.limit_in_bytes  读取 cgroup  限制 * 百分比
```

### cgroup 支持

**cgroup v1 vs v2**:

| 特性 | cgroup v1 | cgroup v2 |
|------|-----------|-----------|
| **JDK 支持** | JDK 8+ | JDK 21+ 完整 |
| **内存检测** | ✅ | ✅ |
| **CPU 检测** | ✅ | ✅ |
| **IO 检测** | ❌ | ❌ |

**cgroup v1 路径**:
```
/sys/fs/cgroup/memory/memory.limit_in_bytes
/sys/fs/cgroup/memory/memory.usage_in_bytes
/sys/fs/cgroup/cpu/cpu.cfs_quota_us
/sys/fs/cgroup/cpu/cpu.cfs_period_us
```

**cgroup v2 路径**:
```
/sys/fs/cgroup/memory.max
/sys/fs/cgroup/memory.current
/sys/fs/cgroup/cpu.max
/sys/fs/cgroup/cpu.stat
```

---

## 3. Docker 最佳实践

### Dockerfile 优化

**基础镜像选择**:
```dockerfile
# 推荐: 使用精简 JRE 镜像
FROM eclipse-temurin:21-jre-alpine

# 或 Ubuntu 基础镜像
FROM eclipse-temurin:21-jre

# 或使用 distroless
FROM gcr.io/distroless/java21-debian12
```

**多阶段构建**:
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

**优化技巧**:
```dockerfile
# 1. 使用 .dockerignore
# .dockerignore
.git
.gradle
build
target
*.md

# 2. 合并 RUN 指令
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 3. 使用特定版本标签
FROM eclipse-temurin:21.0.3_9-jre-alpine

# 4. 非 root 用户
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
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

# 或使用 journald
docker run -d \
  --log-driver journald \
  myapp:latest
```

---

## 4. Kubernetes 部署

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

**完整配置**:
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
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/actuator/prometheus"
    spec:
      serviceAccountName: java-app
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: app
        image: myapp:21
        imagePullPolicy: Always
        ports:
        - name: http
          containerPort: 8080
          protocol: TCP
        - name: management
          containerPort: 8081
          protocol: TCP
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
            -Xlog:gc*,safepoint:file=/logs/gc.log:time,level,tags:filecount=5,filesize=10m
            -XX:StartFlightRecording=maxsize=100m,maxage=24h,disk=true,filename=/logs/recording.jfr
        - name: SPRING_PROFILES_ACTIVE
          value: "kubernetes"
        volumeMounts:
        - name: logs
          mountPath: /logs
        - name: config
          mountPath: /config
          readOnly: true
        livenessProbe:
          httpGet:
            path: /actuator/health/liveness
            port: management
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /actuator/health/readiness
            port: management
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        startupProbe:
          httpGet:
            path: /actuator/health/liveness
            port: management
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 30
        lifecycle:
          preStop:
            exec:
              command: ["sh", "-c", "sleep 10"]
      volumes:
      - name: logs
        emptyDir: {}
      - name: config
        configMap:
          name: java-app-config
      terminationGracePeriodSeconds: 30
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchLabels:
                  app: java-app
              topologyKey: kubernetes.io/hostname
```

### ConfigMap 和 Secret

**ConfigMap**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: java-app-config
data:
  application.yaml: |
    server:
      port: 8080
    management:
      server:
        port: 8081
      endpoints:
        web:
          exposure:
            include: health,info,prometheus
    logging:
      level:
        root: INFO
```

**Secret**:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: java-app-secret
type: Opaque
stringData:
  database-url: "jdbc:postgresql://postgres:5432/mydb"
  database-user: "myuser"
  database-password: "mypassword"
```

### HorizontalPodAutoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: java-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: java-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
```

---

## 5. 镜像优化

### 镜像大小优化

| 基础镜像 | 大小 | 说明 |
|----------|------|------|
| `eclipse-temurin:25-jdk` | ~450MB | 完整 JDK (LTS) |
| `eclipse-temurin:25-jre` | ~250MB | JRE (LTS) |
| `eclipse-temurin:25-jre-alpine` | ~100MB | Alpine JRE (LTS) |
| `eclipse-temurin:21-jre-alpine` | ~100MB | Alpine JRE (上一 LTS) |
| `gcr.io/distroless/java21` | ~150MB | Distroless |

> **注意**: Oracle 提供基于 Oracle Linux 的容器镜像，覆盖 JDK 26、25、21、17、11、8 版本。JDK 25 为当前 LTS，推荐新项目使用。

**Alpine 优化**:
```dockerfile
FROM eclipse-temurin:21-jre-alpine

# 安装必要工具
RUN apk add --no-cache curl

# 设置时区
RUN apk add --no-cache tzdata
ENV TZ=Asia/Shanghai
```

**Distroless 优化**:
```dockerfile
# 构建阶段
FROM eclipse-temurin:21-jdk AS builder
WORKDIR /app
COPY . .
RUN ./gradlew build -x test

# 运行阶段
FROM gcr.io/distroless/java21-debian12
WORKDIR /app
COPY --from=builder /app/build/libs/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-XX:+UseContainerSupport", "-XX:MaxRAMPercentage=75.0", "-jar", "app.jar"]
```

### 启动优化

**CDS 优化**:
```dockerfile
# 生成 CDS 归档
RUN java -Xshare:dump -XX:SharedArchiveFile=/opt/java/.cache/app.jsa

# 使用 CDS 启动
ENTRYPOINT ["java", "-Xshare:on", "-XX:SharedArchiveFile=/opt/java/.cache/app.jsa", "-jar", "app.jar"]
```

**AppCDS 优化**:
```dockerfile
# 生成应用类共享归档
RUN java -XX:ArchiveClassesAtExit=/opt/java/.cache/app.jsa -jar app.jar

# 使用归档启动
ENTRYPOINT ["java", "-XX:SharedArchiveFile=/opt/java/.cache/app.jsa", "-jar", "app.jar"]
```

---

## 6. 监控和诊断

### Prometheus 指标

**JMX Exporter**:
```yaml
# 部署 JMX Exporter
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: app
        env:
        - name: JAVA_TOOL_OPTIONS
          value: >
            -javaagent:/opt/jmx-exporter/jmx_prometheus_javaagent.jar=8081:/opt/jmx-exporter/config.yaml
```

**Micrometer (Spring Boot)**:
```yaml
# application.yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
  metrics:
    tags:
      application: ${spring.application.name}
```

### 日志收集

**Fluentd 配置**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*.log
      pos_file /var/log/fluentd-containers.log.pos
      tag kubernetes.*
      read_from_head true
      <parse>
        @type json
        time_format %Y-%m-%dT%H:%M:%S.%NZ
      </parse>
    </source>
    
    <filter kubernetes.**>
      @type kubernetes_metadata
    </filter>
    
    <match kubernetes.**>
      @type elasticsearch
      host elasticsearch
      port 9200
      logstash_format true
    </match>
```

### JFR 在线分析

```bash
# 启动 JFR
jcmd <pid> JFR.start duration=60s filename=/logs/recording.jfr

# 下载并分析
kubectl cp pod-name:/logs/recording.jfr recording.jfr

# 使用 JMC 分析
jmc recording.jfr
```

---

## 7. 常见问题

### 问题 1: 内存检测不准确

**症状**:
- JVM 分配内存超出容器限制
- 容器被 OOM Killer 终止

**解决方案**:
```bash
# 使用百分比
-XX:MaxRAMPercentage=70.0  # 留出空间给原生内存

# 或明确指定
-Xmx512m

# 限制直接内存
-XX:MaxDirectMemorySize=128m
```

### 问题 2: CPU 检测错误

**症状**:
- 线程数过多或过少
- 性能不理想

**解决方案**:
```bash
# 明确指定 CPU 数
-XX:ActiveProcessorCount=4

# 验证检测
jcmd <pid> VM.flags | grep -i container
```

### 问题 3: 启动时间慢

**症状**:
- 容器启动时间长
- 就绪探针超时

**解决方案**:
```bash
# 使用 CDS
-XX:SharedArchiveFile=app.jsa

# 增加初始延迟
livenessProbe:
  initialDelaySeconds: 60

# 使用 startupProbe
startupProbe:
  failureThreshold: 30
  periodSeconds: 5
```

---

## 8. 最佳实践清单

### Docker

- [ ] 使用精简基础镜像
- [ ] 多阶段构建
- [ ] 非 root 用户运行
- [ ] 健康检查配置
- [ ] 资源限制设置
- [ ] 日志配置

### Kubernetes

- [ ] 资源请求和限制
- [ ] 健康探针配置
- [ ] ConfigMap 和 Secret
- [ ] HPA 配置
- [ ] Pod 反亲和性
- [ ] 优雅终止

### JVM

- [ ] 容器感知启用
- [ ] 内存百分比配置
- [ ] GC 选择和调优
- [ ] JFR 配置
- [ ] GC 日志配置

---

## 9. 相关链接

- [Docker 最佳实践](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Kubernetes 文档](https://kubernetes.io/docs/)
- [JDK 容器支持](/jeps/platform/jep-307.md)
- [性能优化](/by-topic/core/performance/)