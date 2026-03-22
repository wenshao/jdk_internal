# Java / JDK 常见问题 (FAQ)

> 覆盖版本选择、发行版选择、性能调优、迁移排错、安全演进、容器部署与未来路线图。

---
## 目录

1. [版本选择 (Which Version)](#1-版本选择-which-version)
2. [发行版选择 (Which Distribution)](#2-发行版选择-which-distribution)
3. [性能 (Performance)](#3-性能-performance)
4. [迁移 (Migration)](#4-迁移-migration)
5. [安全 (Security)](#5-安全-security)
6. [容器 (Containers)](#6-容器-containers)
7. [未来路线 (Future Roadmap)](#7-未来路线-future-roadmap)
8. [语言特性 (Language Features)](#8-语言特性-language-features)
9. [工具与 IDE (Tooling)](#9-工具与-ide-tooling)
10. [更多资源](#10-更多资源)

---


## 1. 版本选择 (Which Version)

### Q: LTS 和 Feature Release 有什么区别？

Java 从 2017 年 (JDK 9) 起采用 **6 个月固定发布节奏**。

| 类型 | 含义 | 例子 |
|------|------|------|
| **LTS (Long-Term Support)** | 主要发行版商提供 **4-8 年** 补丁更新 | JDK 8, 11, 17, 21, 25 |
| **Feature Release** | 仅获得 **6 个月** 更新，到下一版就停止 | JDK 22, 23, 24, 26 |

- LTS 间隔：从 JDK 17 起，每 **2 年** 一个 LTS（即每 4 个 Feature Release 出一个 LTS）。
- Oracle 从 JDK 25 开始将 LTS 节奏改为 **每 2 年**。

### Q: 我应该用哪个 JDK 版本？

```
生产环境
  ├─ 保守策略 → JDK 21 LTS（2023-09 GA，主流支持到 2028+）
  ├─ 追新策略 → JDK 25 LTS（2025-09 GA，最新 LTS）
  └─ 特性驱动 → JDK 26（需要 HTTP/3, Scoped Values 等最新 API）

开发 / 测试
  └─ 直接用最新版 (JDK 26)，体验新特性并提前发现兼容性问题

新项目
  └─ JDK 25 LTS（兼顾新特性与长期支持）
```

### Q: 还在用 JDK 8 / JDK 11，应该升级到哪个版本？

**推荐直接升级到 JDK 21 或 JDK 25**，跳过中间版本。理由：

1. JDK 8 → JDK 21 的迁移路径已经非常成熟，大量框架 (Spring Boot 3.x, Quarkus 3.x) 已要求 JDK 17+。
2. JDK 11 → JDK 21 相对平滑，主要注意模块系统封装收紧和 `SecurityManager` 废弃。
3. JDK 21 → JDK 25 几乎无 breaking change。

| 源版本 | 目标版本 | 难度 | 关键障碍 |
|--------|----------|------|----------|
| JDK 8 | JDK 21 | 中高 | JPMS 封装、javax → jakarta、Nashorn 移除 |
| JDK 8 | JDK 25 | 中高 | 同上 + SecurityManager 废弃 |
| JDK 11 | JDK 21 | 中 | 内部 API 封装、CMS GC 移除 |
| JDK 11 | JDK 25 | 中 | 同上 + final 字段修改限制 |
| JDK 17 | JDK 21 | 低 | 几乎无障碍 |
| JDK 21 | JDK 25 | 低 | SecurityManager 移除、32-bit x86 移除 |

### Q: JDK 版本号 (version string) 怎么读？

```
java -version
openjdk version "25.0.1" 2026-01-21
```

- `25` = feature release number (主版本)
- `0` = interim (保留，目前始终为 0)
- `1` = update (季度安全更新计数)

### Q: Preview Features 可以在生产环境使用吗？

**不建议**。Preview features 可能在下一版本发生 breaking change。它们的目的是收集社区反馈。如果必须使用，需要明确：
- 编译时加 `--enable-preview`
- 运行时加 `--enable-preview`
- 升级 JDK 时可能需要修改代码

---

## 2. 发行版选择 (Which Distribution)

### Q: Oracle JDK 和 OpenJDK 有什么区别？

从 JDK 11 起，Oracle JDK 和 OpenJDK 的**源代码基本相同**。区别在于：

| 维度 | Oracle JDK | OpenJDK (上游) |
|------|-----------|----------------|
| 许可证 | NFTC (免费) 或 OTN (付费订阅) | GPLv2 + Classpath Exception |
| 商业支持 | 付费获得 Oracle 支持 | 无官方支持 |
| 更新频率 | 季度 CPU (Critical Patch Update) | 同步 |
| 特有功能 | 极少 (Java Management Service 等) | 无 |

> **结论**: 如果不需要 Oracle 官方支持，免费的 OpenJDK 发行版 (如 Eclipse Temurin) 功能完全相同。

### Q: 这么多发行版，怎么选？

快速决策：

```
├─ 不想多想 → Eclipse Temurin（社区标准，Adoptium 品牌）
├─ 部署在 AWS → Amazon Corretto（免费，AWS 优化）
├─ 部署在 Azure → Microsoft Build of OpenJDK
├─ 部署在阿里云 → Alibaba Dragonwell
├─ 需要商业支持 → Oracle JDK 或 Azul Zulu Enterprise
├─ 需要超低延迟 GC → Azul Platform Prime (C4 GC)
├─ 需要最小 Docker 镜像 → BellSoft Liberica (Alpine/musl)
├─ 需要 ARM 嵌入式 → BellSoft Liberica Lite
└─ 信创 / 龙芯 → Loongson JDK / Dragonwell
```

详细对比请参考 [发行版对比指南](jdk-distributions.md)。

### Q: 换发行版会影响现有应用吗？

所有基于 HotSpot 的发行版**二进制兼容** (binary compatible)。替换 JDK 不需要重新编译。唯一例外：
- IBM Semeru 使用 **OpenJ9** 引擎，JVM 参数不完全兼容 HotSpot。
- GraalVM Native Image 是 AOT 编译，需要单独构建。

---

## 3. 性能 (Performance)

### Q: 虚拟线程 (Virtual Threads) vs 响应式 (Reactive)，该选哪个？

| 维度 | Virtual Threads | Reactive (WebFlux / Mutiny) |
|------|----------------|---------------------------|
| 编程模型 | 同步阻塞（熟悉的 try-catch） | 异步非阻塞（Publisher/Subscriber） |
| 学习曲线 | 低 | 高 |
| 调试 | 友好（正常栈帧） | 困难（异步回调链） |
| 背压 (backpressure) | 无内建 | 内建 |
| 生态成熟度 | JDK 21 起正式支持，Spring Boot 3.2+ 支持 | 成熟 (Project Reactor, RxJava) |
| 性能上限 | 极高 (百万级线程) | 极高 |
| 适用场景 | I/O 密集型，大量并发连接 | 流式处理、背压需求 |

**建议**:
- **新项目**: 优先考虑 Virtual Threads，代码更简洁可维护。
- **已有 Reactive 代码**: 无需迁移，两者性能上限相近。
- **需要背压**: 目前 Reactive 仍有优势。
- **CPU 密集型**: 两者都不适合，用平台线程 + ForkJoinPool。

### Q: GC 怎么选？

```
默认选择 → G1 GC（JDK 9+ 默认，JDK 26 有 Claim Table 优化）

低延迟需求
  ├─ 开源 → ZGC (亚毫秒暂停，JDK 21 分代 ZGC 正式版)
  ├─ 开源 → Shenandoah (亚毫秒暂停，JDK 26 分代模式)
  └─ 商业 → Azul C4 GC (Azul Platform Prime)

高吞吐需求 → G1 (大堆) 或 Parallel GC (批处理)

小堆 / 短命进程 → Serial GC 或 Epsilon GC
```

| GC | 暂停目标 | 堆大小 | 适用场景 |
|----|----------|--------|----------|
| G1 | 10-200ms 可配 | 4GB-TB | 通用 Web 服务 |
| ZGC | < 1ms | 8MB-16TB | 低延迟在线服务 |
| Shenandoah | < 10ms | 中大堆 | 低延迟 + 吞吐兼顾 |
| Parallel | 较长但吞吐高 | 中大堆 | 批处理、离线计算 |
| Serial | 较长 | 小堆 | 容器小实例、CLI 工具 |
| Epsilon | 不回收 | - | 性能测试基准、极短命进程 |

### Q: 启动时间太慢怎么优化？

按效果从小到大：

```
1. 类数据共享 CDS (默认已开启)
   → 启动快 10-15%

2. AOT 缓存 (JDK 26 JEP 514)
   $ java -XX:AOTCacheOutput=app.aot -cp app.jar MyApp  # 训练
   $ java -XX:AOTCache=app.aot -cp app.jar MyApp        # 使用
   → 启动快 30-50%

3. GraalVM Native Image
   $ native-image -jar app.jar
   → 启动快 50-100x，但编译慢、峰值吞吐可能下降

4. CRaC (Coordinated Restore at Checkpoint)
   → 毫秒级启动，需要框架支持 (Spring Boot 3.2+, Quarkus)
```

### Q: 紧凑对象头 (Compact Object Headers) 能省多少内存？

JEP 519 在 JDK 26 正式启用（默认开启）：

```
对象类型          传统 (12-16 bytes)  紧凑 (8 bytes)   节省
───────────────────────────────────────────────────────────
空对象            16 bytes           8-12 bytes       25-50%
Point (2 int)     24 bytes           16 bytes         33%
小 String         40 bytes           32 bytes         20%
```

对拥有大量小对象的应用 (如缓存、图数据结构)，整体堆内存可减少 **10-20%**。

### Q: JFR (Java Flight Recorder) 在生产环境开销大吗？

JFR 设计目标是 **< 1% 开销**。JDK 26 新增：
- JEP 509: CPU-Time Profiling（精准 CPU 时间剖析）
- JEP 518: Cooperative Sampling（协作式采样，进一步降低开销）
- JEP 520: Method Timing and Tracing（方法级耗时追踪）

推荐生产环境始终开启：
```bash
-XX:StartFlightRecording=settings=default,maxsize=250m,disk=true
```

---

## 4. 迁移 (Migration)

### Q: 最常见的迁移报错有哪些？

#### 1. `IllegalAccessError` / `InaccessibleObjectException`

**原因**: JDK 16+ 默认强封装内部 API (JEP 396/403)。

```
java.lang.reflect.InaccessibleObjectException:
  Unable to make field private final byte[] java.lang.String.value accessible:
  module java.base does not "opens java.lang" to unnamed module
```

**解法**:
```bash
# 临时: 运行时加 --add-opens
java --add-opens java.base/java.lang=ALL-UNNAMED -jar app.jar

# 长期: 替换内部 API 调用
# sun.misc.Unsafe → VarHandle / MethodHandle
# sun.reflect.*   → java.lang.invoke.*
```

#### 2. `ClassNotFoundException: javax.xml.bind.*`

**原因**: JDK 11 移除了 Java EE 模块 (JAXB, JAX-WS, CORBA)。

**解法**: 添加独立依赖
```xml
<!-- Maven -->
<dependency>
    <groupId>jakarta.xml.bind</groupId>
    <artifactId>jakarta.xml.bind-api</artifactId>
    <version>4.0.2</version>
</dependency>
<dependency>
    <groupId>org.glassfish.jaxb</groupId>
    <artifactId>jaxb-runtime</artifactId>
    <version>4.0.5</version>
</dependency>
```

#### 3. `NoSuchMethodError` / `IncompatibleClassChangeError`

**原因**: 依赖的三方库编译于旧 JDK，内部使用了被移除或变更的 API。

**解法**: 升级依赖到最新版本。常见需要升级的库：
```
ASM          → 9.7+
Byte Buddy   → 1.15+
Lombok       → 1.18.34+
Mockito      → 5.14+
Jackson      → 2.18+
Spring Boot  → 3.3+ (需要 JDK 17+)
```

#### 4. `java.lang.UnsupportedOperationException` (final 字段修改)

**原因**: JDK 25 预备，JDK 26+ `final` 字段反射修改受限 (JEP 500)。

**解法**:
```bash
# 临时: 运行时参数（未来版本将移除此选项）
java --add-opens java.base/java.lang.reflect=ALL-UNNAMED -jar app.jar

# 长期: 重构代码，避免反射修改 final 字段
# 使用 Builder 模式或可变中间对象
```

### Q: 如何批量检查代码兼容性？

```bash
# 1. 检查内部 API 使用
jdeps --jdk-internals -cp 'libs/*.jar' app.jar

# 2. 检查多版本兼容性
jdeps --multi-release 25 app.jar

# 3. 检查模块依赖
jdeps --module-path libs -s app.jar

# 4. 第三方工具
# OpenRewrite: 自动化代码迁移
mvn org.openrewrite.maven:rewrite-maven-plugin:run \
  -Drewrite.activeRecipes=org.openrewrite.java.migrate.UpgradeToJava21

# EMT4J (阿里巴巴): 迁移检查
java -jar emt4j.jar -f 8 -t 21 -o report.html app.jar
```

### Q: Spring Boot 应用升级到新 JDK 要注意什么？

| Spring Boot 版本 | 最低 JDK | 最高 JDK | 状态 |
|-----------------|----------|----------|------|
| 2.7.x | 8 | 21 | EOL (2023-11) |
| 3.0.x - 3.2.x | 17 | 23 | 维护中 |
| 3.3.x - 3.4.x | 17 | 25 | 维护中 |
| 3.5.x+ | 17 | 26+ | 最新 |

关键步骤：
1. 先升级 Spring Boot 到 3.x (需要 javax → jakarta 命名空间迁移)
2. 再升级 JDK
3. 用 `spring-boot-properties-migrator` 检查配置变化

---

## 5. 安全 (Security)

### Q: Security Manager 废弃后怎么办？

`SecurityManager` 在 JDK 17 被标记 `@Deprecated(forRemoval=true)`，JDK 24 正式移除。

**替代方案**:

| 原 Security Manager 用途 | 替代方案 |
|--------------------------|----------|
| 限制文件 I/O | OS 级别沙箱 (容器, SELinux, AppArmor) |
| 限制网络访问 | 网络策略 (iptables, Kubernetes NetworkPolicy) |
| 限制反射 | JPMS `exports` / `opens` 控制 |
| 限制类加载 | 自定义 ClassLoader + JPMS |
| 限制 native 代码 | 容器隔离 |
| 代码签名验证 | jarsigner + 部署管道校验 |

**迁移建议**: 安全边界从 JVM 内部转移到 **基础设施层** (容器 + 网络策略 + RBAC)。

### Q: 后量子密码 (Post-Quantum Cryptography) 什么时候该用？

JDK 的 PQC 支持时间线：

| JDK 版本 | PQC 进展 |
|----------|----------|
| JDK 24 | ML-KEM (密钥封装) 实现 |
| JDK 25 | ML-DSA (数字签名) 实现 |
| JDK 26+ | 持续完善，集成到 TLS 握手 |

**何时开始使用**:
- **现在**: 如果你的数据有 **10+ 年保密需求** (政府、金融、医疗)，应开始规划"先收集后解密" (harvest-now-decrypt-later) 防护。
- **2026-2027**: 对 TLS 连接启用混合模式 (经典 + PQC)。
- **2030+**: 全面迁移到 PQC 算法。

```java
// JDK 24+ ML-KEM 示例
KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-KEM");
kpg.initialize(NamedParameterSpec.ML_KEM_768);
KeyPair kp = kpg.generateKeyPair();
```

### Q: JDK 26 的 KDF (Key Derivation Function) API 怎么用？

JEP 510 提供标准化 KDF API：

```java
// HKDF 密钥派生
KDF hkdf = KDF.getInstance("HKDF-SHA256");
SecretKey derived = hkdf.deriveKey("AES",
    HKDFParameterSpec.expandOnly(
        inputKey, info, 32));
```

内置算法：HKDF-SHA256, HKDF-SHA384, HKDF-SHA512。
第三方 Provider 可扩展支持 PBKDF2, Argon2, Scrypt。

### Q: TLS 1.3 和之前版本有什么区别？

| 特性 | TLS 1.2 | TLS 1.3 |
|------|---------|---------|
| 握手延迟 | 2 RTT | 1 RTT (0-RTT 可选) |
| 加密套件 | 可选不安全套件 | 仅安全套件 |
| 前向保密 | 可选 | 强制 |
| 支持 JDK 版本 | JDK 6+ | JDK 11+ |

JDK 11+ 默认启用 TLS 1.3。建议禁用 TLS 1.0/1.1：
```properties
# java.security 配置
jdk.tls.disabledAlgorithms=SSLv3, TLSv1, TLSv1.1
```

### Q: 序列化过滤 (Serialization Filter) 怎么配置？

JDK 17+ 支持全局序列化过滤器，防止反序列化攻击：

```properties
# JVM 参数
-Djdk.serialFilter=maxdepth=5;maxrefs=1000;maxbytes=500000;!*

# 或在 java.security 中配置
jdk.serialFilter=com.myapp.**;!*
```

```java
// 编程方式
ObjectInputFilter filter = ObjectInputFilter.Config
    .createFilter("com.myapp.**;java.base/*;!*");
ObjectInputFilter.Config.setSerialFilter(filter);
```

---

## 6. 容器 (Containers)

### Q: Docker 中运行 JDK 需要注意什么？

#### 基础镜像选择

```dockerfile
# 推荐: Eclipse Temurin (多架构, 维护活跃)
FROM eclipse-temurin:25-jre-alpine

# 也可选: Amazon Corretto (AWS 部署)
FROM amazoncorretto:25-alpine

# 最小镜像: BellSoft Liberica (Alpine musl)
FROM bellsoft/liberica-openjdk-alpine:25
```

#### 内存配置

```bash
# JDK 10+ 自动识别容器内存限制，但建议显式配置:

# 容器限制 512MB 时:
docker run -m 512m myapp \
  java -XX:MaxRAMPercentage=75.0 \  # 堆占容器内存 75%
       -XX:InitialRAMPercentage=50.0 \
       -jar app.jar

# 不要同时用 -Xmx 和 -XX:MaxRAMPercentage
# 不要设置 -Xms = -Xmx（除非明确需要，否则浪费内存）
```

#### CPU 配置

```bash
# JDK 自动识别 CPU 限制 (--cpus)
docker run --cpus=2 myapp java -jar app.jar
# JVM 会自动设置 ActiveProcessorCount=2

# 如需手动覆盖:
java -XX:ActiveProcessorCount=4 -jar app.jar
```

### Q: Kubernetes 中的 JVM 最佳实践？

```yaml
# Pod 资源配置
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "512Mi"   # 建议 request = limit (避免 OOMKilled)
    cpu: "2000m"      # CPU limit 可以高于 request

# 健康检查 (考虑 JVM 启动时间)
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30   # JVM 启动需要时间
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 15
```

JVM 参数建议：
```bash
java -XX:MaxRAMPercentage=75.0 \
     -XX:+UseG1GC \
     -XX:+ExitOnOutOfMemoryError \     # OOM 时退出，让 K8s 重启
     -jar app.jar
```

### Q: 如何减小 Docker 镜像体积？

```
策略                            镜像大小约
─────────────────────────────────────────
eclipse-temurin:25-jdk          ~350MB
eclipse-temurin:25-jre          ~200MB
eclipse-temurin:25-jre-alpine   ~100MB
jlink 自定义运行时 + Alpine     ~50-80MB
GraalVM native-image + distroless  ~30-50MB
```

```dockerfile
# jlink 自定义运行时示例
FROM eclipse-temurin:25-jdk-alpine AS build
COPY . /app
WORKDIR /app
RUN javac -d out src/*.java && \
    jlink --add-modules java.base,java.sql,java.logging \
          --strip-debug --compress zip-9 \
          --output /custom-jre

FROM alpine:3.20
COPY --from=build /custom-jre /opt/java
COPY --from=build /app/out /app
ENTRYPOINT ["/opt/java/bin/java", "-cp", "/app", "Main"]
```

### Q: 容器中 JFR 录制怎么导出？

```bash
# 方法 1: 挂载卷
docker run -v /host/jfr:/jfr myapp \
  java -XX:StartFlightRecording=filename=/jfr/app.jfr -jar app.jar

# 方法 2: jcmd 远程导出
docker exec <container> jcmd 1 JFR.dump filename=/tmp/app.jfr
docker cp <container>:/tmp/app.jfr ./app.jfr

# 方法 3: JMX 远程连接 (需要配置端口映射)
```

---

## 7. 未来路线 (Future Roadmap)

### Q: Project Valhalla (值类型 / Value Classes) 什么时候 final？

**状态**: Preview 中 (JDK 25 预览，JDK 26 第二次预览)。

**预计正式发布**: JDK 27 或 JDK 28 (2027-2028)。

**影响**:
- `int`, `long` 等基本类型可以作为泛型参数: `List<int>`
- 用户定义值类型 (value class): 无身份、可内联、减少内存分配
- 可能改变集合框架性能特征

```java
// 值类型示例 (Preview 语法可能变化)
value class Point {
    int x;
    int y;
}
// 无对象头，栈上分配，无 GC 开销
```

### Q: Project Leyden (静态运行时镜像) 什么时候 final？

**状态**: JDK 24-26 通过多个 JEP 逐步交付。

- JEP 483: AOT Class Loading & Linking (JDK 24)
- JEP 514: AOT Command Line Ergonomics (JDK 26)
- JEP 515: AOT Method Profiling (JDK 26)

**目标**: 在 "解释执行 → JIT → AOT → Native Image" 的光谱上提供渐进式选择。
**预计路线**: 后续版本将继续添加更多 AOT 优化层次，最终提供接近 native-image 的启动速度同时保留 HotSpot 峰值性能。

### Q: Project Loom (虚拟线程 / 结构化并发) 什么时候全部 final？

| 组件 | 状态 | 正式版本 |
|------|------|---------|
| Virtual Threads | **Final** | JDK 21 |
| Scoped Values | **Final** | JDK 25 |
| Structured Concurrency | Preview (第六次) | 预计 JDK 27 |

Structured Concurrency 多次预览主要因为 API 设计在持续调整 (如 `Joiner` API 变化)。

### Q: 其他值得关注的 OpenJDK 项目？

| 项目 | 目标 | 状态 |
|------|------|------|
| **Panama** (Foreign Function & Memory) | 替代 JNI，直接调用本地代码 | JDK 22 Final |
| **Amber** (语言特性) | Pattern Matching, Records, Sealed Classes | 大部分已 Final |
| **Lilliput** (对象头压缩) | 压缩对象头到 4 bytes | JDK 26 紧凑头 Final (8 bytes) |
| **Galahad** (GraalVM 合并) | 将 Graal JIT 合入 OpenJDK | 进行中 |
| **Babylon** (代码反射) | GPU/FPGA 编程支持 | 早期阶段 |

---

## 8. 语言特性 (Language Features)

### Q: `import module` 和普通 import 有什么区别？

```java
// 普通 import - 导入单个类或包
import java.util.List;
import java.util.ArrayList;

// 模块 import (JDK 26 final) - 导入模块的所有导出包
import module java.base;  // 自动导入 java.util.*, java.io.*, java.lang.* 等
```

- 模块导入更简洁，适合脚本和快速原型
- 可能导致命名冲突 (如 `java.util.List` vs `java.awt.List`)
- 编译后字节码相同，无运行时开销

### Q: Scoped Values vs ThreadLocal？

| 维度 | ScopedValue | ThreadLocal |
|------|-------------|-------------|
| 可变性 | 不可变 (绑定后不可修改) | 可变 |
| 继承 | 自动对虚拟线程子任务可见 | InheritableThreadLocal 有性能问题 |
| 生命周期 | 绑定作用域结束自动清理 | 需要手动 remove() |
| 内存泄漏风险 | 无 | 高 (忘记 remove) |
| 性能 (虚拟线程) | 优 | 差 (每个虚拟线程复制一份) |

```java
// 推荐: ScopedValue (JDK 25+ final)
private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();

ScopedValue.where(CURRENT_USER, user).run(() -> {
    // 在这个作用域内可以读取 CURRENT_USER
    handleRequest();
});
```

### Q: StableValue 和其他懒加载方式有什么区别？

| 方式 | 线程安全 | JVM 优化 | 代码量 |
|------|----------|----------|--------|
| `StableValue.of()` | 是 | 常量折叠 | 1 行 |
| Double-checked locking | 需要 volatile | 无 | 10+ 行 |
| `Lazy<T>` (Kotlin) | 是 | 无 | N/A |
| `AtomicReference` | 是 | 无 | 5 行 |

```java
// StableValue - 一次写入，JVM 视为常量优化
StableValue<Logger> logger = StableValue.of();
logger.orElseSet(() -> Logger.getLogger("app"));
```

---

## 9. 工具与 IDE (Tooling)

### Q: 各 IDE 对 JDK 26 的支持情况？

| IDE | 最低版本 | 预览特性支持 |
|-----|---------|-------------|
| IntelliJ IDEA | 2025.1+ | 是 |
| Eclipse | 2025-06+ | 部分 |
| VS Code (Extension Pack for Java) | 持续更新 | 是 |
| NetBeans | 25+ | 部分 |

### Q: Maven / Gradle 如何配置 JDK 26？

**Maven**:
```xml
<properties>
    <maven.compiler.release>26</maven.compiler.release>
</properties>

<!-- 如需预览特性 -->
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.14.0</version>
    <configuration>
        <release>26</release>
        <compilerArgs>
            <arg>--enable-preview</arg>
        </compilerArgs>
    </configuration>
</plugin>
```

**Gradle**:
```groovy
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(26)
    }
}

tasks.withType(JavaCompile).configureEach {
    options.compilerArgs += '--enable-preview'
}

tasks.withType(JavaExec).configureEach {
    jvmArgs += '--enable-preview'
}
```

### Q: SDKMAN 怎么管理多个 JDK 版本？

```bash
# 安装
curl -s "https://get.sdkman.io" | bash

# 列出可用版本
sdk list java

# 安装指定发行版
sdk install java 25-tem       # Eclipse Temurin 25
sdk install java 26.ea-open   # OpenJDK 26 Early Access

# 切换版本
sdk use java 25-tem           # 当前终端
sdk default java 25-tem       # 全局默认

# 项目级别: 在项目根目录创建 .sdkmanrc
echo "java=25-tem" > .sdkmanrc
sdk env                       # 自动切换
```

---

## 10. 更多资源

- [学习路径](learning-path.md) — 按角色推荐的学习路线
- [迁移指南](migration-guide.md) — JDK 版本升级详细步骤
- [速查表](cheat-sheet.md) — JVM 参数与 API 快速参考
- [发行版对比](jdk-distributions.md) — 主流发行版详细对比
- [模块系统指南](modules.md) — JPMS 实用指南
- [OpenJDK 官网](https://openjdk.org/) — 官方文档与 JEP 列表
