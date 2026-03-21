# 从 JDK 11 迁移到 JDK 17

> **迁移复杂度**: 中 | **建议时间**: 2-4 周 | **测试要求**: 全面回归测试和性能基准测试

---
## 目录

1. [迁移概览](#1-迁移概览)
2. [准备工作](#2-准备工作)
3. [代码迁移步骤](#3-代码迁移步骤)
4. [配置迁移](#4-配置迁移)
5. [测试策略](#5-测试策略)
6. [部署策略](#6-部署策略)
7. [常见问题解决](#7-常见问题解决)
8. [迁移后优化](#8-迁移后优化)
9. [工具和资源](#9-工具和资源)
10. [总结检查清单](#10-总结检查清单)

---


## 1. 迁移概览

### 为什么迁移到 JDK 17？

1. **LTS 支持**: JDK 17 是长期支持版本 (支持至 2029 年)
2. **现代语言特性**: Records, Sealed Classes, Pattern Matching
3. **性能提升**: ZGC 增强，启动时间优化
4. **安全增强**: 更强的加密，改进的 TLS
5. **容器优化**: 更好的容器资源管理
6. **生产就绪工具**: jpackage 正式版，JFR 改进

### 迁移路径
```
JDK 11u (当前)
    ↓
兼容性评估 (1 周)
    ↓    
代码迁移 (1-2 周)
    ↓
特性采用 (可选)
    ↓
测试验证 (1 周)
    ↓
性能优化 (可选)
    ↓
生产部署
```

### 关键差异
| 方面 | JDK 11 | JDK 17 | 影响等级 |
|------|--------|--------|----------|
| **语言特性** | var, HTTP Client | Records, Sealed Classes, Pattern Matching | 低 (新特性) |
| **GC 选项** | ZGC 实验性 | ZGC 生产就绪，并发栈处理 | 低 |
| **安全变更** | Security Manager 正常 | Security Manager 废弃 | 中 |
| **移除功能** | 基本完整 | RMI Activation, Applet API 移除 | 低 |
| **工具支持** | 基本工具 | jpackage 正式版，macOS Metal | 低 |

---

## 2. 准备工作

### 环境评估

1. **系统要求检查**:
```bash
# JDK 17 最低要求:
# - Linux: glibc 2.17+, kernel 3.10+
# - Windows: Windows 10+
# - macOS: 10.14+ (Mojave)

# 检查兼容性
uname -a
ldd --version  # Linux glibc 版本

# 验证架构支持
# JDK 17 新增: macOS AArch64 (Apple Silicon) 原生支持
```

2. **磁盘空间需求**:
| 组件 | JDK 11 大小 | JDK 17 大小 | 变化 |
|------|------------|-------------|------|
| JRE | ~150MB | ~160MB | +7% |
| JDK | ~300MB | ~320MB | +7% |

### 依赖分析

1. **使用 jdeps 分析**:
```bash
# 分析依赖关系
jdeps --multi-release 17 --ignore-missing-deps your-application.jar

# 检查已移除 API
jdeps -jdkinternals your-application.jar | grep -E "(removed|deprecated)"

# 生成迁移报告
jdeps --generate-module-info . your-application.jar
```

2. **使用 jdeprscan 扫描废弃 API**:
```bash
# 扫描标记为移除的 API
jdeprscan --release 17 --for-removal your-application.jar

# 扫描所有废弃 API
jdeprscan --release 17 your-application.jar
```

3. **第三方库兼容性**:
| 库/框架 | JDK 11 兼容版本 | JDK 17 最小版本 | 操作 |
|---------|----------------|-----------------|------|
| Spring Framework | 5.1+ | 5.3+ | 推荐 Spring 6.x |
| Hibernate | 5.4+ | 5.6+ | 升级 |
| Jackson | 2.10+ | 2.13+ | 升级 |
| Log4j 2 | 2.11+ | 2.17+ | 必须升级 (安全) |
| JUnit | 5.4+ | 5.8+ | 升级 |

### 风险评估矩阵

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| **Security Manager 依赖** | 低 | 高 | 检查使用，开始迁移 |
| **RMI Activation 使用** | 低 | 中 | 检查并迁移到现代 RPC |
| **内部 API 访问失败** | 中 | 中 | 使用 --add-opens 或迁移 |
| **模块化冲突** | 低 | 低 | 使用类路径模式兼容 |
| **性能回归** | 低 | 低 | 性能基准测试 |

---

## 3. 代码迁移步骤

### 步骤 1: 更新构建环境

1. **更新构建配置**:
```xml
<!-- Maven pom.xml -->
<properties>
    <maven.compiler.source>17</maven.compiler.source>
    <maven.compiler.target>17</maven.compiler.target>
    <maven.compiler.release>17</maven.compiler.release>
</properties>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.10.0</version>
            <configuration>
                <release>17</release>
                <parameters>true</parameters>
                <!-- 启用预览特性 (如果需要) -->
                <compilerArgs>
                    <arg>--enable-preview</arg>
                </compilerArgs>
            </configuration>
        </plugin>
    </plugins>
</build>
```

```groovy
// Gradle build.gradle
plugins {
    id 'java'
}

java {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
    modularity.inferModulePath = true
}

tasks.withType(JavaCompile) {
    options.compilerArgs += ['--release', '17']
    // 启用预览特性
    options.compilerArgs += ['--enable-preview']
}

tasks.withType(Test) {
    jvmArgs += '--enable-preview'
}

tasks.withType(JavaExec) {
    jvmArgs += '--enable-preview'
}
```

2. **IDE 配置**:
- **IntelliJ IDEA**: Project Structure → SDK → 添加 JDK 17
- **Eclipse**: Window → Preferences → Java → Installed JREs → 添加 JDK 17
- **VS Code**: 设置 `java.home` 或使用 Java Extension Pack

### 步骤 2: 处理废弃和移除的 API

1. **Security Manager 迁移**:
```java
// JDK 11: 正常使用
SecurityManager sm = new CustomSecurityManager();
System.setSecurityManager(sm);

// JDK 17: 标记为废弃，需要迁移
// 选项 1: 使用模块系统 (推荐)
module com.example.app {
    // 使用模块访问控制替代权限检查
}

// 选项 2: 使用容器技术
// Docker/容器提供隔离

// 选项 3: 暂时忽略警告 (不推荐长期)
@SuppressWarnings("removal")
public class CustomSecurityManager extends SecurityManager {
    // ...
}
```

2. **RMI Activation 迁移**:
```java
// 如果使用 RMI Activation，需要迁移到:
// 1. 现代 RPC 框架: gRPC, Apache Thrift
// 2. RESTful 服务: Spring Boot, Micronaut
// 3. 消息队列: Kafka, RabbitMQ
// 4. 传统 RMI (无激活): 仍然可用
```

3. **Applet API 迁移**:
```html
<!-- 从 Applet 迁移到现代 Web 技术 -->
<!-- 之前 -->
<applet code="MyApplet.class" width="300" height="200"></applet>

<!-- 之后 -->
<canvas id="myCanvas" width="300" height="200"></canvas>
<script src="myapp.js"></script>
```

### 步骤 3: 采用新语言特性 (可选但推荐)

1. **Records - 简化数据类**:
```java
// JDK 11 之前
public class Person {
    private final String name;
    private final int age;
    
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public String name() { return name; }
    public int age() { return age; }
    
    @Override
    public boolean equals(Object o) { ... }
    @Override
    public int hashCode() { ... }
    @Override
    public String toString() { ... }
}

// JDK 17: Record
public record Person(String name, int age) {
    // 自动生成所有样板代码
    
    // 可以添加验证逻辑
    public Person {
        if (age < 0) {
            throw new IllegalArgumentException("Age cannot be negative");
        }
    }
    
    // 可以添加额外方法
    public boolean isAdult() {
        return age >= 18;
    }
}
```

**迁移策略**:
1. 从简单的数据传输对象开始
2. 逐步替换不可变值对象
3. 注意序列化兼容性

2. **Sealed Classes - 受控继承**:
```java
// 定义密封接口/类
public sealed interface Shape 
    permits Circle, Rectangle, Triangle { }

// 允许的子类必须声明继承状态
public final class Circle implements Shape { ... }
public final class Rectangle implements Shape { ... }
public non-sealed class Triangle implements Shape { ... }

// 编译器确保穷尽性检查
double area = switch (shape) {
    case Circle c -> Math.PI * c.radius() * c.radius();
    case Rectangle r -> r.length() * r.width();
    case Triangle t -> 0.5 * t.base() * t.height();
    // 不需要 default，因为所有情况已覆盖
};
```

**适用场景**:
- 代数数据类型
- 状态机实现
- API 设计中的类型安全

3. **Pattern Matching for instanceof**:
```java
// JDK 11
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.length());
}

// JDK 17
if (obj instanceof String s) {
    System.out.println(s.length());
}

// 带条件
if (obj instanceof String s && s.length() > 5) {
    System.out.println("Long string: " + s);
}
```

**迁移建议**: 逐步替换现有的 instanceof 检查。

### 步骤 4: 使用新的核心库特性

1. **增强的随机数生成器**:
```java
// JDK 11: 有限的随机数算法
Random random = new Random();

// JDK 17: 增强的 PRNG 框架
import java.util.random.*;

// 获取特定算法的生成器
RandomGenerator generator = RandomGenerator.of("L32X64MixRandom");

// 算法选择指南:
// - L32X64MixRandom: 通用用途，性能最佳
// - L64X128MixRandom: 高质量，适用于模拟
// - Xoroshiro128PlusPlus: 快速，非加密用途

// 列出所有可用算法
RandomGeneratorFactory.all()
    .map(RandomGeneratorFactory::name)
    .sorted()
    .forEach(System.out::println);
```

2. **上下文特定的反序列化过滤器**:
```java
// 增强的反序列化安全性
ObjectInputFilter filter = ObjectInputFilter.allowFilter(
    cl -> cl != null && cl.getName().startsWith("com.example."),
    ObjectInputFilter.Status.REJECTED
);

// 设置全局过滤器
ObjectInputFilter.Config.setSerialFilter(filter);

// 或为特定流设置
ObjectInputStream ois = new ObjectInputStream(input);
ois.setObjectInputFilter(filter);
```

### 步骤 5: 外部函数和内存 API (孵化器)

```java
// 注意: 这是孵化器 API，可能变化
import jdk.incubator.foreign.*;

// 分配本地内存
try (ResourceScope scope = ResourceScope.newConfinedScope()) {
    MemorySegment segment = MemorySegment.allocateNative(100, scope);
    
    // 访问内存
    MemoryAccess.setIntAtOffset(segment, 0, 42);
    int value = MemoryAccess.getIntAtOffset(segment, 0);
}

// 编译时需要特殊参数
// javac --add-modules jdk.incubator.foreign ...
// java --add-modules jdk.incubator.foreign ...
```

**使用场景**: 替代 JNI，高性能本地互操作。

---

## 4. 配置迁移

### JVM 参数迁移

1. **GC 参数更新**:
```bash
# ZGC 不再是实验性
-XX:+UseZGC  # 不再需要 -XX:+UnlockExperimentalVMOptions

# ZGC 增强参数
-XX:ZAllocationSpikeTolerance=2.0
-XX:+ZProactive  # 主动回收

# G1 优化参数 (如果使用 G1)
-XX:G1ConcRefinementThreads=4
```

2. **模块系统参数**:
```bash
# 兼容性参数 (如果需要)
--add-opens java.base/jdk.internal.misc=ALL-UNNAMED
--add-opens java.base/sun.nio.ch=ALL-UNNAMED
--add-opens java.base/java.lang=ALL-UNNAMED

# 模块化运行
--module-path app.jar:lib
--module com.example.app/com.example.Main

# 类路径模式 (兼容性)
--class-path app.jar:lib/*
```

3. **容器优化参数**:
```bash
# 容器支持增强
-XX:+UseContainerSupport  # 默认启用
-XX:MaxRAMPercentage=75.0
-XX:InitialRAMPercentage=50.0
-XX:ActiveProcessorCount=auto
```

4. **废弃参数处理**:
```bash
# 已废弃参数
-XX:+UseConcMarkSweepGC    # 使用 G1 或 ZGC
-XX:+UseParNewGC          # 使用 G1 或 ZGC
-XX:+AggressiveOpts       # 已默认优化
-XX:+UseBiasedLocking     # 默认已优化
```

### 应用服务器配置

1. **Tomcat 优化**:
```xml
<!-- conf/server.xml -->
<Connector port="8080" protocol="org.apache.coyote.http11.Http11NioProtocol"
           maxThreads="200"
           minSpareThreads="10"
           acceptCount="100"
           connectionTimeout="20000"
           redirectPort="8443"
           
           <!-- JDK 17 优化 -->
           useAsyncIO="true"
           maxConnections="10000"
           
           <!-- TLS 优化 -->
           sslEnabledProtocols="TLSv1.2,TLSv1.3"
           ciphers="TLS_AES_256_GCM_SHA384,TLS_CHACHA20_POLY1305_SHA256,..." />
```

2. **Spring Boot 配置**:
```yaml
# application.yml
spring:
  main:
    banner-mode: off
  jackson:
    default-property-inclusion: non_null

server:
  tomcat:
    threads:
      max: 200
      min-spare: 10
    connection-timeout: 20000
    
# JDK 17 特定
    keep-alive-timeout: 30000
    max-connections: 10000
```

### 安全配置更新

1. **TLS 配置**:
```bash
# 启用 TLS 1.3 (默认)
# 可以明确指定
-Djdk.tls.client.protocols=TLSv1.2,TLSv1.3
-Djdk.tls.server.protocols=TLSv1.2,TLSv1.3

# 禁用弱算法
-Djdk.tls.disabledAlgorithms=SSLv3, TLSv1, TLSv1.1, RC4, DES, \
    MD5withRSA, DH keySize < 1024, EC keySize < 224
```

2. **加密算法**:
```bash
# 使用现代算法
-Djdk.tls.namedGroups="secp256r1, x25519, secp384r1"
-Djdk.tls.ephemeralDHKeySize=2048
```

### 监控配置

1. **统一日志系统**:
```bash
# GC 日志
-Xlog:gc*,safepoint:file=gc.log:time,level,tags:filecount=5,filesize=10m

# 类加载日志 (调试)
-Xlog:class+load=info:file=classload.log

# JFR 配置
-XX:StartFlightRecording=maxsize=100m,maxage=24h,disk=true,settings=profile
```

---

## 5. 测试策略

### 兼容性测试

1. **API 兼容性测试**:
```bash
# 使用 jdeps 验证
jdeps --check your-application.jar

# 运行所有单元测试
mvn test  # 或 gradle test
```

2. **模块化测试**:
```bash
# 测试模块路径运行
java --module-path out:lib -m com.example.app/com.example.Main

# 测试类路径运行 (兼容模式)
java --class-path app.jar:lib/* com.example.Main
```

### 性能基准测试

1. **关键指标对比**:
| 指标 | JDK 11 基准 | JDK 17 目标 | 测量工具 |
|------|------------|-------------|----------|
| 启动时间 | 100% | 95-105% | `time` 命令 |
| 吞吐量 | 100% | 105-115% | JMH, wrk |
| 内存使用 | 100% | 95-105% | `jstat`, `jcmd` |
| GC 暂停 | 基准 | -20-50% | GC 日志 |
| 延迟 (P99) | 基准 | -10-30% | 应用监控 |

2. **使用 JMH 基准测试**:
```java
@BenchmarkMode(Mode.Throughput)
@OutputTimeUnit(TimeUnit.SECONDS)
@State(Scope.Benchmark)
public class JDK17MigrationBenchmark {
    
    private List<Person> persons;
    
    @Setup
    public void setup() {
        // 创建测试数据
        persons = IntStream.range(0, 1000)
            .mapToObj(i -> new Person("Name" + i, i % 100))
            .collect(Collectors.toList());
    }
    
    @Benchmark
    public void testRecordPerformance() {
        // 测试 Record 性能
    }
    
    @Benchmark 
    public void testPatternMatching() {
        // 测试模式匹配性能
    }
}
```

### 安全测试

1. **TLS 连接测试**:
```bash
# 测试 TLS 1.3 连接
openssl s_client -connect localhost:8443 -tls1_3

# 测试 TLS 1.2 兼容性
openssl s_client -connect localhost:8443 -tls1_2
```

2. **反序列化安全测试**:
- 测试自定义过滤器
- 验证安全异常处理
- 渗透测试

### 回归测试

1. **功能测试覆盖**:
- 所有业务功能测试
- 边界条件测试
- 错误处理测试
- 集成测试

2. **生产环境模拟**:
- 真实流量重放
- 压力测试
- 故障恢复测试

---

## 6. 部署策略

### 分阶段部署

1. **金丝雀部署**:
```yaml
# Kubernetes 部署示例
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-jdk17
spec:
  replicas: 1  # 初始 1 个副本
  selector:
    matchLabels:
      app: myapp
      version: jdk17
  template:
    metadata:
      labels:
        app: myapp
        version: jdk17
    spec:
      containers:
      - name: app
        image: myapp:jdk17
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        env:
        - name: JAVA_TOOL_OPTIONS
          value: "-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0"
```

2. **流量切分策略**:
- **阶段 1**: 1% 流量 (开发验证)
- **阶段 2**: 10% 流量 (内部测试)
- **阶段 3**: 50% 流量 (生产验证)
- **阶段 4**: 100% 流量 (完全迁移)

### 监控和告警

1. **新增监控指标**:
```promql
# Record 使用监控
jvm_classes_loaded{type="record"}

# 密封类监控
jvm_classes_loaded{type="sealed"}

# ZGC 增强监控
jvm_gc_collector_seconds_count{collector="ZGC Cycles"}

# 模块系统监控
jvm_classes_loaded{context="module"}
```

2. **关键告警规则**:
```yaml
- alert: SecurityManagerUsageDetected
  expr: increase(jvm_security_manager_checks_total[5m]) > 0
  for: 5m
  labels:
    severity: warning
  annotations:
    description: 检测到 Security Manager 使用，需要迁移

- alert: RecordSerializationFailure
  expr: rate(jvm_record_serialization_errors_total[5m]) > 0.1
  for: 2m
  labels:
    severity: warning
  annotations:
    description: Record 序列化失败率超过阈值
```

### 回滚计划

1. **快速回滚条件**:
- 模块解析失败导致应用无法启动
- 性能下降超过 15%
- 关键功能故障
- 安全漏洞暴露

2. **回滚步骤**:
```bash
# 停止 JDK 17 实例
kubectl scale deployment app-jdk17 --replicas=0

# 启动 JDK 11 实例
kubectl scale deployment app-jdk11 --replicas=3

# 验证回滚
curl -f http://app/health
kubectl logs deployment/app-jdk11 --tail=100

# 验证功能
run_smoke_tests.sh
```

---

## 7. 常见问题解决

### 模块访问错误

```bash
# 错误信息
java.lang.IllegalAccessError: class tried to access private method

# 解决方案
java --add-opens java.base/jdk.internal.misc=ALL-UNNAMED \
     --add-opens java.base/sun.nio.ch=ALL-UNNAMED \
     --add-opens java.base/java.lang=ALL-UNNAMED \
     -jar app.jar
```

### Record 序列化问题

```java
// 错误: Record 有自定义 readObject/writeObject
public record Person(String name, int age) {
    private void writeObject(ObjectOutputStream out) throws IOException {
        // 与 Record 自动生成冲突
    }
}

// 解决方案: 移除自定义序列化方法
// Record 自动处理序列化
// 或使用 Externalizable 如果需要完全控制
```

### 预览特性编译错误

```bash
# 错误信息
error: pattern matching in switch is a preview feature and is disabled by default

# 解决方案
# 编译时启用预览
javac --enable-preview --release 17 Main.java

# 运行时启用预览
java --enable-preview Main
```

### TLS 连接失败

```bash
# 临时启用旧协议 (仅测试)
java -Djdk.tls.client.protocols=TLSv1,TLSv1.1,TLSv1.2,TLSv1.3 \
     -jar app.jar
```

---

## 8. 迁移后优化

### 代码优化机会

1. **采用 Records**:
   - 替换简单的数据传输对象
   - 替换不可变值对象
   - 注意保持序列化兼容性

2. **采用 Sealed Classes**:
   - 类型安全的 API 设计
   - 改进的模式匹配
   - 编译时检查

3. **性能优化**:
   - 启用 ZGC (如果未使用)
   - 使用新的随机数生成器
   - 优化反序列化过滤器

### 架构优化

1. **模块化设计** (如果适用):
   - 明确模块边界
   - 减少循环依赖
   - 使用服务提供者

2. **安全架构**:
   - 迁移 Security Manager 到模块系统
   - 实现严格的反序列化过滤器
   - 使用现代 TLS 配置

### 运维优化

1. **监控增强**:
   - 启用 JFR 生产使用
   - 配置统一日志系统
   - 监控新特性使用情况

2. **部署优化**:
   - 使用 jpackage 创建安装包
   - 优化容器配置
   - 改进启动性能

---

## 9. 工具和资源

### 迁移工具

1. **OpenJDK 工具**:
   - `jdeps`: 依赖分析
   - `jdeprscan`: 废弃 API 扫描
   - `jlink`: 创建自定义运行时
   - `jpackage`: 应用打包

2. **第三方工具**:
   - [Java Migration Guide](https://github.com/openjdk/jmh)
   - [Moditect](https://github.com/moditect/moditect): 模块化工具
   - [OpenRewrite](https://github.com/openrewrite/rewrite): 代码迁移工具

### 文档资源

1. **官方指南**:
   - [JDK 17 迁移指南](https://docs.oracle.com/en/java/javase/17/migrate/)
   - [Records 教程](https://docs.oracle.com/en/java/javase/17/language/records.html)
   - [Sealed Classes 教程](https://docs.oracle.com/en/java/javase/17/language/sealed-classes-and-interfaces.html)

2. **社区资源**:
   - [Java Champions 博客](https://inside.java/)
   - [Stack Overflow: java-17-migration](https://stackoverflow.com/questions/tagged/java-17+migration)
   - [Reddit r/java](https://www.reddit.com/r/java/)

### 支持渠道

1. **商业支持**:
   - Oracle Java SE Subscription
   - Red Hat OpenJDK Support
   - Azul Prime Support

2. **社区支持**:
   - [OpenJDK 邮件列表](https://mail.openjdk.org/)
   - [Java User Groups](https://community.oracle.com/community/developer/)
   - [GitHub Discussions](https://github.com/openjdk/jdk/discussions)

---

## 10. 总结检查清单

### 迁移前准备
- [ ] 环境兼容性验证完成
- [ ] 依赖库兼容性分析完成
- [ ] 废弃 API 扫描完成
- [ ] 迁移计划制定和批准

### 代码迁移
- [ ] 构建环境更新完成
- [ ] 废弃 API 处理完成
- [ ] Security Manager 迁移计划制定
- [ ] 新特性采用评估完成

### 测试验证
- [ ] 单元测试全部通过
- [ ] 集成测试完成
- [ ] 性能基准测试达标
- [ ] 安全测试通过
- [ ] 回归测试完成

### 部署上线
- [ ] 生产环境部署验证
- [ ] 监控告警配置完成
- [ ] 回滚计划测试通过
- [ ] 团队培训完成

### 长期优化
- [ ] Records 采用计划制定
- [ ] Sealed Classes 采用评估
- [ ] 性能监控持续优化
- [ ] 安全架构改进计划