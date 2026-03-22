# 案例研究: Spring Boot 应用启动优化 — 从 12 秒到 1.5 秒

> **场景**: Spring Boot 3.x 微服务 | JDK 25 → JDK 26 | Kubernetes 部署
>
> **目标**: 将启动时间从 12 秒优化至 Pod 快速扩缩容可接受的范围 (< 3 秒)
>
> **注意**: 本文中所有性能数据均为 **示意数据**，用于展示优化趋势和方法论。
> 实际效果因应用规模、硬件配置、JDK 版本等因素而异，请以实测为准。

---

## 目录

1. [问题背景](#1-问题背景)
2. [基线测量](#2-基线测量)
3. [第一步 — Default CDS](#3-第一步--default-cds-jep-341)
4. [第二步 — AppCDS](#4-第二步--appcds-jep-310350)
5. [第三步 — AOT Cache](#5-第三步--aot-cache-jep-516-jdk-26)
6. [第四步 — 应用层优化](#6-第四步--应用层优化)
7. [与 GraalVM Native Image 对比](#7-与-graalvm-native-image-对比)
8. [优化效果总览](#8-优化效果总览)
9. [生产环境 Dockerfile 与 K8s 配置](#9-生产环境-dockerfile-与-k8s-配置)
10. [常见问题与注意事项](#10-常见问题与注意事项)

---

## 1. 问题背景

一个典型的 Spring Boot 3.x 微服务：Spring Boot 3.3 + Spring WebFlux + Spring Data JPA，约 180 个 JAR / ~15,000 个类，运行在 Kubernetes（1 CPU / 1 GB Memory）上。

```
Pod 启动流程 (示意数据):
  JVM 初始化      ~1.5s
  类加载/验证     ~4.0s     ← 最大瓶颈
  Spring 上下文   ~5.0s     ← 第二大瓶颈
  其他            ~1.5s
  ─────────────────────
  总计            ~12.0s
```

在 HPA 场景下，12 秒启动意味着流量突增时新 Pod 无法及时接流，Rolling update 期间服务容量下降，Liveness probe 超时被迫放宽。

---

## 2. 基线测量

### 2.1 类加载分析

```bash
# 记录所有类加载事件
java -Xlog:class+load=info:file=classload.log:time,level -jar app.jar

# 统计类数量
wc -l classload.log    # 14,837 (示意数据)
```

### 2.2 JFR 启动录制

```bash
java -XX:StartFlightRecording=filename=startup.jfr,duration=20s,settings=profile \
     -jar app.jar

jfr print --events jdk.ClassLoad --stack-depth 5 startup.jfr | head -100
```

### 2.3 基线结论

| 阶段 | 耗时 | 占比 |
|------|------|------|
| JVM bootstrap (类加载 + 验证) | ~5.5s | 46% |
| Spring context 初始化 | ~5.0s | 42% |
| 其他 (GC, JIT warmup 等) | ~1.5s | 12% |
| **总计** | **~12.0s** | **100%** |

> (示意数据)

---

## 3. 第一步 — Default CDS (JEP 341)

自 JDK 12 起，JDK 自带预生成的 CDS archive (`lib/server/classes.jsa`)，包含 ~1,200 个 JDK 核心类。JDK 25 中 **默认启用**，无需配置。

相关 JEP: [JEP 341: Default CDS Archives](../jeps/performance/jep-341.md)

```bash
# 验证 CDS 是否启用
java -Xlog:cds -version 2>&1 | grep "sharing"
# 预期: sharing is enabled
```

### 效果

| 指标 | 优化前 | Default CDS | 变化 |
|------|--------|-------------|------|
| 启动时间 | 12.0s | ~10.8s | -10% |
| 从 archive 加载 | 0 | ~1,200 | — |

> (示意数据)

**结论**: Default CDS 是免费的午餐，但仅覆盖 JDK 核心类，对大型应用效果有限。

---

## 4. 第二步 — AppCDS (JEP 310/350)

AppCDS 将 CDS 扩展到应用类和第三方库，通过 training run 记录实际加载的类，预处理到 shared archive 中。

相关 JEP:
- [JEP 310: Application Class-Data Sharing](../jeps/performance/jep-310.md) — JDK 10
- [JEP 350: Dynamic CDS Archives](../jeps/performance/jep-350.md) — JDK 13

### 4.1 方式一: 静态 AppCDS (三步法)

```bash
# Step 1: Training run — 记录加载的类
java -Xshare:off -XX:DumpLoadedClassList=app-classlist.txt -jar app.jar
# 应用 Ready 后 Ctrl+C 停止

# Step 2: 创建 shared archive
java -Xshare:dump \
     -XX:SharedClassListFile=app-classlist.txt \
     -XX:SharedArchiveFile=app-cds.jsa \
     -cp app.jar

# Step 3: 使用 archive 启动
java -Xshare:on -XX:SharedArchiveFile=app-cds.jsa -jar app.jar
```

### 4.2 方式二: Dynamic CDS (更简单)

```bash
# 一步生成 dynamic archive
java -XX:ArchiveClassesAtExit=app-dynamic.jsa -jar app.jar
# 应用 Ready 后停止，archive 自动生成

# 使用 archive 启动
java -XX:SharedArchiveFile=app-dynamic.jsa -jar app.jar
```

### 4.3 Dockerfile 集成

```dockerfile
FROM eclipse-temurin:25-jdk AS training
WORKDIR /app
COPY target/app.jar app.jar
RUN java -XX:ArchiveClassesAtExit=app-cds.jsa \
         -Dspring.profiles.active=cds-training \
         -jar app.jar &  \
    APP_PID=$! && \
    for i in $(seq 1 60); do \
      curl -sf http://localhost:8080/actuator/health > /dev/null 2>&1 && break; \
      sleep 1; \
    done && kill $APP_PID && wait $APP_PID 2>/dev/null || true

FROM eclipse-temurin:25-jre-alpine AS production
WORKDIR /app
COPY --from=training /app/app.jar app.jar
COPY --from=training /app/app-cds.jsa app-cds.jsa
ENTRYPOINT ["java", "-XX:SharedArchiveFile=app-cds.jsa", "-jar", "app.jar"]
```

### 4.4 效果

| 指标 | Default CDS | + AppCDS | 变化 |
|------|-------------|----------|------|
| 启动时间 | 10.8s | ~8.0s | -26% |
| 类加载耗时 | 4.9s | ~2.1s | -57% |
| 从 archive 加载 | ~1,200 | ~14,200 | +13,000 |

> (示意数据) **从基线 12s 降至 8s，累计优化 33%。**

---

## 5. 第三步 — AOT Cache (JEP 516, JDK 26)

JDK 26 引入的 AOT Cache 是 CDS 的全面升级，不仅缓存 class metadata，还缓存 **AOT compiled native code**、**archived heap objects** 和 **method profiling data**。

相关 JEP: [JEP 516: AOT Cache](../jeps/performance/jep-516.md)

### 5.1 单命令方式

```bash
# 自动 training + 生成 cache
java -XX:AOTCacheOutput=app.aot -jar app.jar
# 应用启动后停止，cache 自动生成

# 使用 cache 启动
java -XX:AOTCache=app.aot -jar app.jar
```

### 5.2 手动两步流程 (精细控制)

```bash
# Step 1: Training run
java -XX:AOTMode=record -XX:AOTConfiguration=app-training.aotconf -jar app.jar

# Step 2: 创建 cache
java -XX:AOTMode=create \
     -XX:AOTConfiguration=app-training.aotconf \
     -XX:AOTCache=app.aot -cp app.jar

# Step 3: 使用 cache
java -XX:AOTCache=app.aot -jar app.jar
```

### 5.3 Dockerfile 集成

```dockerfile
FROM eclipse-temurin:26-jdk AS training
WORKDIR /app
COPY target/app.jar app.jar
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
# Training run
RUN java -XX:AOTMode=record \
         -XX:AOTConfiguration=app-training.aotconf \
         -Dspring.profiles.active=aot-training -jar app.jar &  \
    APP_PID=$! && \
    for i in $(seq 1 60); do \
      curl -sf http://localhost:8080/actuator/health > /dev/null 2>&1 && break; \
      sleep 1; \
    done && sleep 2 && kill $APP_PID && wait $APP_PID 2>/dev/null || true
# 创建 AOT cache
RUN java -XX:AOTMode=create \
         -XX:AOTConfiguration=app-training.aotconf \
         -XX:AOTCache=app.aot -cp app.jar

FROM eclipse-temurin:26-jre-alpine AS production
RUN addgroup -S app && adduser -S app -G app
USER app
WORKDIR /app
COPY --from=training /app/app.jar app.jar
COPY --from=training /app/app.aot app.aot
ENTRYPOINT ["java", "-XX:AOTCache=app.aot", "-jar", "app.jar"]
```

### 5.4 效果

| 指标 | AppCDS (JDK 25) | + AOT Cache (JDK 26) | 变化 |
|------|-----------------|----------------------|------|
| 启动时间 | 8.0s | ~3.0s | -62% |
| 类加载耗时 | 2.1s | ~0.4s | -81% |
| JIT 编译时间 (启动阶段) | ~1.5s | ~0.1s | -93% |

> (示意数据) **从基线 12s 降至 3s，累计优化 75%。**

### 5.5 注意事项

- AOT cache 与 JDK 版本 **强绑定**，patch 更新后需要重新生成
- Training run 应覆盖应用的典型启动路径
- Cache 文件较大 (~150 MB)，会增加容器镜像体积

---

## 6. 第四步 — 应用层优化

JVM 层优化已将启动压到 3 秒，剩余时间主要在 Spring 上下文初始化。

### 6.1 Lazy Initialization

```properties
# application.properties — 全局延迟初始化
spring.main.lazy-initialization=true
```

```java
@Component
@Lazy(false)  // 关键组件仍立即初始化
public class CriticalHealthChecker { }
```

### 6.2 减少 Classpath Scanning

```java
@SpringBootApplication(scanBasePackages = {
    "com.example.myapp.controller",
    "com.example.myapp.service",
    "com.example.myapp.config"
})
public class Application { ... }
```

### 6.3 排除不需要的 AutoConfiguration

```java
@SpringBootApplication(exclude = {
    JmxAutoConfiguration.class,
    TaskExecutionAutoConfiguration.class
})
public class Application { ... }
```

### 6.4 Spring AOT Processing (Spring 6+)

```xml
<!-- pom.xml -->
<plugin>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-maven-plugin</artifactId>
    <executions>
        <execution>
            <id>process-aot</id>
            <goals><goal>process-aot</goal></goals>
        </execution>
    </executions>
</plugin>
```

### 6.5 效果

| 指标 | AOT Cache | + 应用层优化 | 变化 |
|------|-----------|-------------|------|
| 启动时间 | 3.0s | ~1.5s | -50% |
| Spring 上下文初始化 | ~1.8s | ~0.6s | -67% |

> (示意数据) **从基线 12s 降至 1.5s，累计优化 87.5%。**

---

## 7. 与 GraalVM Native Image 对比

| 维度 | JDK 26 + AOT Cache + 应用优化 | GraalVM Native Image |
|------|-------------------------------|---------------------|
| **启动时间** | ~1.5s | ~0.1s |
| **峰值吞吐量** | 100% (正常 JIT) | ~70-85% |
| **内存占用 (RSS)** | ~200 MB | ~80 MB |
| **构建时间** | ~30s (training) | ~3-5 min |
| **调试能力** | 完整 (JFR, JMX, debugger) | 有限 |
| **反射 / 动态代理** | 正常使用 | 需额外配置 (reflect-config.json) |
| **第三方库兼容** | 100% | ~90% |
| **镜像体积** | ~250 MB | ~80 MB |
| **CI/CD 复杂度** | 低 | 中-高 |

> (示意数据)

**选 AOT Cache**: 需要完整 JVM 诊断能力，使用大量反射/动态代理，1-3 秒启动可接受。

**选 Native Image**: Serverless/FaaS 需极致启动 (< 0.5s)，内存预算紧张，应用简单且库兼容性已验证。

---

## 8. 优化效果总览

```
基线 (JDK 25, 无优化)    ████████████████████████  12.0s
+ Default CDS             █████████████████████▌    10.8s  (-10%)
+ AppCDS                  ████████████████          8.0s   (-33%)
+ AOT Cache (JDK 26)      ██████                    3.0s   (-75%)
+ 应用层优化               ███                       1.5s   (-87.5%)
GraalVM Native Image      ▏                         0.1s   (-99.2%)
(示意数据)
```

| 优化阶段 | 启动时间 | 较上一步 | 较基线 | 额外工作量 |
|----------|---------|---------|--------|-----------|
| 基线 (无优化) | 12.0s | — | — | — |
| Default CDS (JEP 341) | 10.8s | -10% | -10% | 零 (默认启用) |
| AppCDS (JEP 310/350) | 8.0s | -26% | -33% | 低 (CI 加 training step) |
| AOT Cache (JEP 516) | 3.0s | -62% | -75% | 低 (升级 JDK + CI 调整) |
| 应用层优化 | 1.5s | -50% | -87.5% | 中 (代码改动) |
| GraalVM Native Image | 0.1s | -93% | -99.2% | 高 (兼容性适配) |

> (示意数据)

投入产出比排序: AOT Cache > AppCDS > Lazy Init > Default CDS > 排除 AutoConfig > Spring AOT > Native Image

---

## 9. 生产环境 Dockerfile 与 K8s 配置

对应的 Kubernetes Deployment (探针配置因优化后启动时间缩短而调整):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-spring-app
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: app
        image: my-registry/my-spring-app:latest
        resources:
          requests: { cpu: 500m, memory: 512Mi }
          limits:   { cpu: "1", memory: 1Gi }
        readinessProbe:
          httpGet: { path: /actuator/health/readiness, port: 8080 }
          initialDelaySeconds: 2    # 优化后可大幅缩短
          periodSeconds: 3
        livenessProbe:
          httpGet: { path: /actuator/health/liveness, port: 8080 }
          initialDelaySeconds: 5    # 无需 30s+
          periodSeconds: 10
        startupProbe:
          httpGet: { path: /actuator/health, port: 8080 }
          failureThreshold: 10
          periodSeconds: 1
```

---

## 10. 常见问题与注意事项

### 10.1 AOT Cache 失效与回退

AOT cache 在 JDK 版本变更、JAR 内容变更或 JVM 参数不兼容时会自动 fallback 到普通启动。建议 CI/CD 中每次构建时重新生成 cache。

```bash
# 显式禁用 (回退)
java -XX:AOTCache=none -jar app.jar
```

### 10.2 Training Run Profile

Training 环境应尽量接近生产配置，但可替换外部依赖:

```yaml
# application-aot-training.yml
spring:
  datasource:
    url: jdbc:h2:mem:training    # 内嵌 DB 替代真实数据库
  kafka:
    bootstrap-servers: ""
    listener:
      auto-startup: false
```

### 10.3 镜像体积优化

AOT cache (~100-200 MB) 增加镜像体积，可用 jlink 创建自定义 JRE 缓解:

```bash
jlink --add-modules java.base,java.sql,java.naming,java.management \
      --strip-debug --no-man-pages --compress=zip-6 --output /custom-jre
```

### 10.4 验证 AOT Cache 生效

```bash
java -XX:AOTCache=app.aot -Xlog:cds=info -jar app.jar 2>&1 | grep -i "aot\|sharing"
```

---

## 相关资源

- [JEP 310: Application Class-Data Sharing](../jeps/performance/jep-310.md)
- [JEP 350: Dynamic CDS Archives](../jeps/performance/jep-350.md)
- [JEP 516: AOT Cache](../jeps/performance/jep-516.md)
- [Project Leyden](https://openjdk.org/projects/leyden/) — OpenJDK 启动性能优化项目
