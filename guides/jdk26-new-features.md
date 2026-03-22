# JDK 26 新特性实战

JDK 26 于 2026-03-17 正式 GA，这是继 JDK 25 (LTS) 之后的第一个功能版本 (feature release)。本指南覆盖所有重要特性，每个特性均附带可运行的代码或命令。

---
## 目录

1. [AOT Cache (JEP 516)](#1-aot-cache-jep-516--最大亮点)
2. [HTTP/3 (JEP 517)](#2-http3-jep-517--网络升级)
3. [Value Classes (JEP 401, Preview)](#3-value-classes-jep-401-preview--valhalla-首次亮相)
4. [G1 吞吐量提升 (JEP 522)](#4-g1-吞吐量提升-jep-522--默认受益)
5. [Stable Values (JEP 528, 2nd Preview)](#5-stable-values-jep-528-2nd-preview--延迟初始化)
6. [Generational Shenandoah (JEP 404/521)](#6-generational-shenandoah-jep-404521--新-gc-选项)
7. [其他变更速查](#7-其他变更速查)
8. [升级检查清单](#8-升级检查清单--从-jdk-25-升级)

---

## 1. AOT Cache (JEP 516) — 最大亮点

Ahead-of-Time Class Loading & Linking Cache 是 JDK 26 最具生产力影响的特性。它将应用程序的类加载、链接和部分初始化结果缓存到文件中，后续启动时跳过这些重复工作。

### 1.1 核心概念

- **Training Run**: 第一次启动应用，JVM 记录加载了哪些类
- **Cache Creation**: 基于 training run 的记录，构建 AOT 缓存文件
- **Production Run**: 使用缓存启动，跳过类加载/链接步骤

### 1.2 一键模式 (最简用法)

```bash
# JDK 26 支持单命令模式 — 自动完成 training + 缓存创建
java -XX:AOTCache=app.aot -jar app.jar
```

首次运行时 JVM 发现 `app.aot` 不存在，自动进入 training 模式并生成缓存。
后续运行直接使用缓存。

### 1.3 三步分离模式 (生产推荐)

生产环境推荐分步执行，便于 CI/CD 集成:

```bash
# 步骤 1: Training Run — 记录类加载信息
# 启动应用并执行典型工作负载 (如跑一轮集成测试)，然后正常退出
java -XX:AOTConfiguration=app.aotconf -jar app.jar

# 步骤 2: Cache Creation — 基于记录生成缓存文件
# 此步骤不需要真正运行应用，JVM 在缓存创建完成后自动退出
java -XX:AOTCache=app.aot -XX:AOTConfiguration=app.aotconf -jar app.jar

# 步骤 3: Production Run — 使用缓存启动
java -XX:AOTCache=app.aot -jar app.jar
```

### 1.4 验证缓存是否生效

```bash
# 使用 -Xlog 确认缓存加载情况
java -XX:AOTCache=app.aot -Xlog:cds -jar app.jar 2>&1 | head -20

# 预期输出包含类似行:
# [0.002s][info][cds] Opened AOT cache app.aot
# [0.003s][info][cds] Mapped AOT cache app.aot
```

### 1.5 Spring Boot 集成: 多阶段 Dockerfile

```dockerfile
# === 构建阶段 ===
FROM eclipse-temurin:26-jdk AS builder
WORKDIR /app
COPY target/myapp.jar app.jar

# Training run: 启动应用后自动退出 (使用 actuator 健康检查 + 自动关闭)
# 确保 training 覆盖主要代码路径
RUN java -XX:AOTConfiguration=app.aotconf \
    -Dspring.context.exit=onRefresh \
    -jar app.jar || true

# 生成 AOT 缓存
RUN java -XX:AOTCache=app.aot \
    -XX:AOTConfiguration=app.aotconf \
    -jar app.jar

# === 运行阶段 ===
FROM eclipse-temurin:26-jre
WORKDIR /app
COPY --from=builder /app/app.jar .
COPY --from=builder /app/app.aot .

EXPOSE 8080
ENTRYPOINT ["java", "-XX:AOTCache=app.aot", "-jar", "app.jar"]
```

### 1.6 效果估算

> **注意**: 以下数据为估算值，实际效果因应用而异。

| 指标 | 无 AOT Cache | 有 AOT Cache | 改进幅度 (估算) |
|------|-------------|-------------|----------------|
| Spring Boot 启动时间 | ~3.5s | ~1.5-2.0s | 40-55% |
| 首次请求延迟 | ~200ms | ~80-120ms | 40-60% |
| RSS 内存占用 | ~250MB | ~220-230MB | 8-12% |
| 类加载时间 | ~800ms | ~100-200ms | 75-85% |

### 1.7 注意事项

```text
⚠ AOT Cache 在以下情况需要重新生成:
  - 更新了 JAR 文件 (依赖版本变化、代码变更)
  - 更新了 JDK 版本
  - 修改了 JVM 参数中影响类加载的选项

⚠ AOT Cache 不支持:
  - 跨平台使用 (Linux 生成的缓存不能在 macOS 使用)
  - 不同 JDK 发行版之间共享 (Temurin 的缓存不能用于 Corretto)
```

---

## 2. HTTP/3 (JEP 517) — 网络升级

JDK 11 引入的 `java.net.http.HttpClient` 现在支持 HTTP/3 (基于 QUIC 协议)。HTTP/3 使用 UDP 而非 TCP，在高丢包网络环境下性能显著提升。

### 2.1 基本用法 — 自动升级

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Http3Demo {
    public static void main(String[] args) throws Exception {
        // HttpClient 默认启用 HTTP/3 升级 (upgrade)
        // 首次请求使用 HTTP/2，如果服务器通告支持 HTTP/3，
        // 后续请求自动升级到 HTTP/3
        try (var client = HttpClient.newBuilder()
                .version(HttpClient.Version.HTTP_2) // 初始版本
                .build()) {

            var request = HttpRequest.newBuilder()
                    .uri(URI.create("https://www.cloudflare.com"))
                    .GET()
                    .build();

            // 第一次请求: 可能使用 HTTP/2，同时发现 HTTP/3 支持
            var response = client.send(request,
                    HttpResponse.BodyHandlers.ofString());

            System.out.println("Status: " + response.statusCode());
            System.out.println("HTTP Version: " + response.version());

            // 第二次请求: 如果服务器支持，自动使用 HTTP/3
            var response2 = client.send(request,
                    HttpResponse.BodyHandlers.ofString());

            System.out.println("HTTP Version (2nd): " + response2.version());
        }
    }
}
```

### 2.2 显式请求 HTTP/3

```java
// 显式指定 HTTP/3 — 如果服务器不支持则自动降级
try (var client = HttpClient.newBuilder()
        .version(HttpClient.Version.HTTP_3)
        .build()) {

    var request = HttpRequest.newBuilder()
            .uri(URI.create("https://www.cloudflare.com"))
            .GET()
            .build();

    var response = client.send(request,
            HttpResponse.BodyHandlers.ofString());
    System.out.println("Version: " + response.version());
}
```

### 2.3 HTTP/3 vs HTTP/2 行为差异

| 特性 | HTTP/2 | HTTP/3 |
|------|--------|--------|
| 传输层协议 | TCP + TLS 1.2/1.3 | UDP + QUIC (内置 TLS 1.3) |
| 连接建立 | 2-3 RTT (TCP + TLS) | 1 RTT (0-RTT 恢复时) |
| 队头阻塞 (Head-of-Line) | 有 (TCP 层) | 无 (流级别独立) |
| 连接迁移 | 不支持 | 支持 (网络切换不断连) |
| Java 降级行为 | 可降级到 HTTP/1.1 | 可降级到 HTTP/2 或 HTTP/1.1 |

### 2.4 验证 HTTP/3 是否生效

```bash
# 方法 1: 通过 Java 代码检查 response.version()
# HttpClient.Version.HTTP_3 表示使用了 HTTP/3

# 方法 2: 使用系统属性启用调试日志
java -Djdk.httpclient.HttpClient.log=all Http3Demo 2>&1 | grep -i quic

# 方法 3: 使用 JFR 事件
java -XX:StartFlightRecording=filename=http3.jfr,duration=30s Http3Demo
jfr print --events jdk.HttpClient http3.jfr
```

### 2.5 注意事项

```text
⚠ HTTP/3 要求:
  - 服务器必须支持 HTTP/3 (通过 Alt-Svc header 通告)
  - 网络环境必须允许 UDP 443 端口
  - 部分企业防火墙可能阻止 QUIC/UDP 流量

⚠ 生产建议:
  - 不需要修改代码即可受益 (自动升级机制)
  - 如果需要强制禁用: HttpClient.Version.HTTP_2
  - 监控初期建议记录 response.version() 以观察升级比例
```

---

## 3. Value Classes (JEP 401, Preview) — Valhalla 首次亮相

Project Valhalla 历经多年终于在 JDK 26 首次以 Preview 形式发布。Value Classes 是没有对象标识 (identity) 的类，JVM 可以将其内联存储，减少堆分配和指针追踪。

### 3.1 语法与关键规则

// 编译: javac --enable-preview --release 26 Money.java
// 运行: java --enable-preview Money

public value class Money {   // 使用 value 修饰符
    private final long amountInCents;
    private final String currency;

    public Money(long amountInCents, String currency) {
        this.amountInCents = amountInCents;
        this.currency = currency;
    }

    public Money add(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new IllegalArgumentException("Currency mismatch");
        }
        return new Money(this.amountInCents + other.amountInCents, this.currency);
    }

    public static void main(String[] args) {
        var a = new Money(1000, "CNY");
        var b = new Money(1000, "CNY");

        // value class 没有对象标识 — == 按值比较
        System.out.println(a == b);        // true
        System.out.println(a.equals(b));   // true

        var c = a.add(new Money(500, "CNY"));
        System.out.println(c); // Money[amountInCents=1500, currency=CNY]
    }
}
```

### 3.2 Value Class vs Record vs 普通 Class

| 特性 | `class` | `record` | `value class` | `value record` |
|------|---------|----------|---------------|----------------|
| 对象标识 (identity) | 有 | 有 | **无** | **无** |
| 可变性 (mutable) | 可以 | 不可变 | 不可变 | 不可变 |
| 自定义字段 | 任意 | 组件即字段 | 任意 | 组件即字段 |
| 继承 | 可以 | 不可以 | 受限 | 不可以 |
| synchronized | 可以 | 可以 (不推荐) | **不可以** | **不可以** |
| == 语义 | 引用比较 | 引用比较 | **值比较** | **值比较** |
| JVM 内联优化 | 不会 | 不会 | **可能** | **可能** |

### 3.3 Value Record 语法

```java
// value 也可以结合 record — 最简洁的 value 类型
public value record Complex(double real, double imag) {
    public Complex add(Complex other) {
        return new Complex(real + other.real, imag + other.imag);
    }
}
```

### 3.4 当前限制 (Preview 阶段)

```text
⚠ Value Class 在 Preview 阶段的限制:
  1. 不能对 value class 的实例使用 synchronized — 编译错误
  2. 所有字段必须是 final (隐式)
  3. 不能声明 finalize() 方法
  4. 身份敏感的操作会产生警告或错误:
     - System.identityHashCode() 行为不同
     - WeakReference/SoftReference 不能引用 value 对象
  5. 第三方库 (如序列化框架) 可能尚未适配
  6. 作为 Preview 特性，不建议在生产环境使用
```

---

## 4. G1 吞吐量提升 (JEP 522) — 默认受益

JEP 522 通过引入晚期屏障扩展 (Late Barrier Expansion) 优化 G1 的写屏障 (write barrier) 实现，减少应用线程在 GC 记账上的开销。

### 4.1 无需配置

```bash
# G1 是 JDK 的默认 GC，升级到 JDK 26 后自动受益
java -jar app.jar

# 确认使用的是 G1 (通常不需要显式指定)
java -XX:+PrintFlagsFinal -version 2>&1 | grep UseG1GC
# bool UseG1GC = true
```

### 4.2 双卡表 (Dual Card Table) 原理简述

G1 使用"卡表" (card table) 追踪跨 Region 的对象引用。传统实现中，每次对象字段写入都需要执行屏障代码来标记卡表，这在应用线程中产生开销。

JEP 522 的优化策略:

```text
传统方式:
  应用线程写入对象字段 → 立即执行完整的写屏障 → 标记卡表
  (每次写入都有完整开销)

JDK 26 优化:
  应用线程写入对象字段 → 执行最小化的快速路径屏障
  GC 线程定期处理 → 完成完整的卡表标记
  (应用线程开销大幅减少)
```

### 4.3 性能验证

```bash
# 使用 JFR 收集 GC 相关事件进行前后对比
java -XX:StartFlightRecording=filename=gc-jdk26.jfr,duration=60s,\
settings=profile -jar app.jar

# 分析 GC 暂停时间
jfr print --events jdk.GCPhasePause gc-jdk26.jfr

# 使用 GC 日志对比
java -Xlog:gc*:file=gc-jdk26.log:time,level,tags -jar app.jar

# 关键指标: 关注 Mutator Utilization (应用线程占比)
# JDK 26 预期比 JDK 25 的 Mutator Utilization 更高
```

### 4.4 预期改进

> **注意**: 以下为估算值，实际效果取决于工作负载特征。

| 工作负载类型 | 吞吐量改进 (估算) | 说明 |
|-------------|------------------|------|
| 写密集型 (如大量对象引用更新) | 10-20% | 受益最大 |
| 读密集型 (如缓存查询) | 2-5% | 写屏障开销本来就小 |
| 混合型 Web 应用 | 5-10% | 典型的中等受益 |
| 大堆 (>32GB) 应用 | 10-15% | 跨 Region 引用更多 |

---

## 5. Stable Values (JEP 528, 2nd Preview) — 延迟初始化

`StableValue` 提供了一种线程安全、JVM 可优化的延迟初始化 (lazy initialization) 机制。它是 `static final` 常量和手写双重检查锁定 (double-checked locking) 的更好替代方案。

### 5.1 基本用法: StableValue.of()

```java
// javac --enable-preview --release 26 StableValueDemo.java
// java --enable-preview StableValueDemo

import java.lang.StableValue;
import java.util.logging.Logger;

public class StableValueDemo {

    // 延迟初始化的 Logger — 只在首次调用 get() 时创建
    private static final StableValue<Logger> LOGGER =
            StableValue.of(() -> {
                System.out.println("Logger initializing...");
                return Logger.getLogger(StableValueDemo.class.getName());
            });

    public static void main(String[] args) {
        System.out.println("Before first access");

        // 首次调用 — 触发初始化
        LOGGER.get().info("Hello from StableValue!");

        // 后续调用 — 直接返回缓存值，无锁开销
        LOGGER.get().info("Second call, no re-init");
    }
}
```

### 5.2 替代传统延迟初始化模式

```java
import java.lang.StableValue;
import java.sql.Connection;
import java.sql.DriverManager;

public class DatabaseService {

    // ❌ 传统方式: Double-Checked Locking (容易写错)
    private static volatile Connection legacyConnection;
    private static Connection getLegacyConnection() {
        if (legacyConnection == null) {
            synchronized (DatabaseService.class) {
                if (legacyConnection == null) {
                    try {
                        legacyConnection = DriverManager.getConnection(
                            "jdbc:postgresql://localhost/mydb");
                    } catch (Exception e) {
                        throw new RuntimeException(e);
                    }
                }
            }
        }
        return legacyConnection;
    }

    // ✅ JDK 26 方式: StableValue — 简洁、正确、JVM 可优化
    private static final StableValue<Connection> connection =
            StableValue.of(() -> {
                try {
                    return DriverManager.getConnection(
                        "jdbc:postgresql://localhost/mydb");
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }
            });

    public static Connection getConnection() {
        return connection.get();
    }
}
```

### 5.3 StableValue vs 其他方案对比

| 方案 | 线程安全 | 延迟初始化 | JVM 可优化为常量 | 代码复杂度 |
|------|---------|-----------|----------------|-----------|
| `static final` 字段 | 是 | 否 (类加载即初始化) | 是 | 低 |
| `volatile` + DCL | 是 (写对了的话) | 是 | 否 | 高 |
| Holder 类模式 | 是 | 是 | 是 | 中 |
| `StableValue.of()` | **是** | **是** | **是** | **低** |

### 5.4 注意事项

```text
⚠ StableValue 仍是 2nd Preview，使用需要 --enable-preview
⚠ Supplier 只会被调用一次；如果抛出异常，后续调用会重新抛出相同异常
⚠ StableValue 不适合需要重新赋值的场景 — 一旦初始化就不可变
⚠ StableValue.of() 的 Supplier 不应有副作用 (side effects)
```

---

## 6. Generational Shenandoah (JEP 404/521) — 新 GC 选项

Shenandoah GC 现在支持分代模式 (generational mode)，将堆划分为年轻代和老年代，利用分代假设 (generational hypothesis) 提升 GC 效率。

### 6.1 启用分代 Shenandoah

```bash
# 启用 Shenandoah + 分代模式
java -XX:+UseShenandoahGC \
     -XX:ShenandoahGCMode=generational \
     -jar app.jar

# 完整的生产配置示例
java -XX:+UseShenandoahGC \
     -XX:ShenandoahGCMode=generational \
     -Xms4g -Xmx4g \
     -Xlog:gc*:file=shenandoah-gc.log:time,level,tags \
     -jar app.jar
```

### 6.2 验证 GC 配置

```bash
# 确认 GC 类型和模式
java -XX:+UseShenandoahGC -XX:ShenandoahGCMode=generational \
     -Xlog:gc+init -version

# 预期输出:
# Shenandoah GC mode: Generational
# Shenandoah heuristics: Adaptive (Generational)
```

### 6.3 适用场景

| 场景 | 推荐 GC | 原因 |
|------|---------|------|
| 超低延迟 (<1ms 暂停) | ZGC | 暂停时间最短 |
| 低延迟 + 吞吐量平衡 | **Shenandoah (分代)** | 分代后吞吐量更好 |
| 大堆 (>16GB) + 低延迟 | ZGC 或 Shenandoah (分代) | 都能处理大堆 |
| 最大吞吐量 | G1 (JDK 26 优化后) | 吞吐量最高 |
| 小堆 (<2GB) | Serial 或 G1 | 开销最小 |

### 6.4 JDK 26 GC 选项速查

```bash
# G1 — 默认 GC (JDK 26 自动受益于 JEP 522)
java -XX:+UseG1GC -jar app.jar

# ZGC — 分代模式 (自 JDK 23 起默认分代)
java -XX:+UseZGC -jar app.jar

# Shenandoah — 分代模式 (JDK 26 新增)
java -XX:+UseShenandoahGC -XX:ShenandoahGCMode=generational -jar app.jar

# Shenandoah — 传统非分代模式
java -XX:+UseShenandoahGC -jar app.jar
```

---

## 7. 其他变更速查

### 7.1 正式化和移除的特性

| JEP | 特性 | 状态 | 影响 |
|-----|------|------|------|
| JEP 404 | Generational Shenandoah | 正式化 | 新 GC 选项 |
| JEP 521 | Generational Shenandoah 默认 | 正式化 | Shenandoah 默认使用分代模式 |
| JEP 516 | AOT Cache | 正式化 | 启动加速 |
| JEP 517 | HTTP/3 | 正式化 | 网络升级 |
| JEP 522 | G1 Late Barrier Expansion | 正式化 | 吞吐量提升 |

### 7.2 Preview 和 Incubator 特性

| JEP | 特性 | Preview 轮次 | 要点 |
|-----|------|-------------|------|
| JEP 401 | Value Classes | 1st Preview | Valhalla 核心特性 |
| JEP 528 | Stable Values | 2nd Preview | 延迟初始化 API |

### 7.3 兼容性检查

```bash
# 检查你的代码是否使用了被废弃的 API
jdeprscan --release 26 --class-path lib/*.jar myapp.jar

# 检查对 JDK 内部 API 的非法访问
jdeps --jdk-internals myapp.jar
```

### 7.4 工具链更新

| 工具 | JDK 26 兼容版本 (建议最低) | 备注 |
|------|--------------------------|------|
| Maven | 3.9.x + compiler-plugin 3.13+ | 需设置 `<release>26</release>` |
| Gradle | 8.12+ | 需在 toolchain 中指定 JDK 26 |
| IntelliJ IDEA | 2026.1+ | 通常在 GA 前已支持 |
| Eclipse | 2026-03+ | 通过 Marketplace 安装 Java 26 支持 |
| Spring Boot | 3.5.x+ | 验证兼容性 |
| Quarkus | 3.18+ | 通常快速跟进 |

---

## 8. 升级检查清单 — 从 JDK 25 升级

### 8.1 升级前准备

```bash
# 1. 确认当前版本
java -version
# openjdk version "25.0.x" ...

# 2. 下载 JDK 26
# Eclipse Temurin
curl -LO https://api.adoptium.net/v3/binary/latest/26/ga/linux/x64/jdk/hotspot/normal/eclipse

# 或使用 SDKMAN
sdk install java 26-tem
sdk use java 26-tem

# 3. 验证安装
java -version
# openjdk version "26" 2026-03-17
```

### 8.2 编译检查

```bash
# 1. 使用 JDK 26 编译项目
# Maven
mvn clean compile -Dmaven.compiler.release=26

# Gradle
./gradlew compileJava  # 确保 build.gradle 中 toolchain 指向 JDK 26

# 2. 检查编译警告 — 特别关注 deprecation 警告
mvn clean compile -Dmaven.compiler.showWarnings=true \
    -Dmaven.compiler.showDeprecation=true

# 3. 检查内部 API 依赖
jdeps --jdk-internals --multi-release 26 target/*.jar
```

### 8.3 Maven 配置更新

```xml
<!-- pom.xml -->
<properties>
    <maven.compiler.release>26</maven.compiler.release>
    <java.version>26</java.version>
</properties>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.13.0</version>
            <configuration>
                <release>26</release>
                <!-- 如果使用 Preview 特性 -->
                <!-- <compilerArgs>
                    <arg>--enable-preview</arg>
                </compilerArgs> -->
            </configuration>
        </plugin>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.5.2</version>
            <configuration>
                <!-- 如果使用 Preview 特性 -->
                <!-- <argLine>--enable-preview</argLine> -->
            </configuration>
        </plugin>
    </plugins>
</build>
```

### 8.4 Gradle 配置更新

```kotlin
// build.gradle.kts
java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(26))
    }
}

// 如果使用 Preview 特性
tasks.withType<JavaCompile> {
    options.compilerArgs.add("--enable-preview")
}

tasks.withType<Test> {
    jvmArgs("--enable-preview")
}

tasks.withType<JavaExec> {
    jvmArgs("--enable-preview")
}
```

### 8.5 测试验证

```bash
# 1. 运行完整测试套件
mvn clean verify

# 2. 特别关注的测试场景:
#    - 反射相关代码 (可能受模块访问限制影响)
#    - 序列化/反序列化 (Jackson, Gson 等)
#    - 字节码操作 (ASM, ByteBuddy, Javassist)
#    - GC 敏感的测试 (如 WeakReference 测试)
#    - 网络相关测试 (HTTP/3 行为变化)

# 3. 运行性能基准测试 (对比 JDK 25)
java -jar benchmarks.jar -jvm /path/to/jdk25/bin/java
java -jar benchmarks.jar -jvm /path/to/jdk26/bin/java
```

### 8.6 生产部署检查

```bash
# 1. 启用 AOT Cache (推荐)
java -XX:AOTConfiguration=app.aotconf -jar app.jar  # training
java -XX:AOTCache=app.aot -XX:AOTConfiguration=app.aotconf -jar app.jar  # build
java -XX:AOTCache=app.aot -jar app.jar  # production

# 2. GC 监控 — G1 自动受益于 JEP 522
java -Xlog:gc*:file=gc.log:time,level,tags:filecount=5,filesize=100M \
     -XX:AOTCache=app.aot \
     -jar app.jar

# 3. JFR 持续监控
java -XX:StartFlightRecording=disk=true,maxage=24h,maxsize=1g,\
dumponexit=true,filename=app.jfr \
     -jar app.jar

# 4. 验证 HTTP/3 (如果使用 HttpClient)
# 检查日志确认连接协议版本
```

### 8.7 升级决策树

```text
JDK 25 (LTS) → JDK 26 升级决策:

Q1: 是否需要 AOT Cache 加速启动?
    → Yes: 升级收益明显 (特别是 Serverless/容器环境)
    → No: 继续评估

Q2: 是否需要 HTTP/3 支持?
    → Yes: 升级 (无需修改代码)
    → No: 继续评估

Q3: 是否在意 G1 吞吐量提升?
    → Yes: 升级后自动受益
    → No: 继续评估

Q4: 是否想试用 Value Classes?
    → Yes: 升级 (Preview, 仅开发环境)
    → No: 可以等待 JDK 27

建议:
  - 开发/测试环境: 推荐升级，提前验证兼容性
  - 生产环境: 如果 JDK 25 运行稳定且无迫切需求，
    可以在 JDK 26.0.1 (预计 2026-07) 后升级
  - 注意: JDK 26 不是 LTS，下一个 LTS 预计是 JDK 29
```

### 8.8 回滚方案

```bash
# 如果升级后遇到问题，快速回滚到 JDK 25

# 1. 容器环境: 修改 Dockerfile 基础镜像
# FROM eclipse-temurin:26-jre  →  FROM eclipse-temurin:25-jre

# 2. SDKMAN 环境
sdk use java 25-tem

# 3. 删除 AOT Cache (不影响回滚)
rm -f app.aot app.aotconf

# 4. 确保 CI/CD 中保留了 JDK 25 的构建产物
# 以便快速回滚部署
```

---

## 附录: JDK 26 关键 JVM 参数速查

```bash
# AOT Cache
-XX:AOTCache=<file>              # 指定 AOT 缓存文件路径
-XX:AOTConfiguration=<file>      # 指定 AOT 训练配置文件路径

# GC 相关
-XX:+UseG1GC                     # G1 (默认, 自动受益于 JEP 522)
-XX:+UseZGC                      # ZGC (分代模式默认)
-XX:+UseShenandoahGC             # Shenandoah
-XX:ShenandoahGCMode=generational  # Shenandoah 分代模式

# Preview 特性
--enable-preview                 # 启用 Preview 特性 (Value Classes, Stable Values)

# 诊断和监控
-Xlog:cds                       # AOT/CDS 相关日志
-Xlog:gc*                       # GC 详细日志
-XX:StartFlightRecording=...     # JFR 录制
```
