# 从 JDK 17 迁移到 JDK 25

> JDK 17 (LTS 2021) → JDK 25 (LTS 2025)：跨越 4 年的 LTS 直升指南

---
## 目录

1. [概述](#1-概述)
2. [破坏性变更汇总](#2-破坏性变更汇总)
3. [新增正式特性](#3-新增正式特性)
4. [GC 演进](#4-gc-演进)
5. [安全与平台变更](#5-安全与平台变更)
6. [代码迁移示例](#6-代码迁移示例)
7. [迁移步骤](#7-迁移步骤)
8. [依赖兼容性](#8-依赖兼容性)
9. [JVM 参数变更](#9-jvm-参数变更)
10. [常见问题](#10-常见问题)
11. [相关资源](#11-相关资源)

---


## 1. 概述

从 JDK 17 到 JDK 25 跨越了 8 个版本（18-25），包含 JDK 21 这个中间 LTS。这是当前最常见的生产升级路径。

| 类别 | 新增正式特性 | 破坏性变更 | 整体兼容性 |
|------|-------------|-----------|-----------|
| 语言 | 10+ | 低 | ✅ 好 |
| 性能 | 6+ | 低 | ✅ 好 |
| 并发 | 2 | 低 | ✅ 好 |
| 安全 | 4+ | 中 | ⚠️ 需注意 |
| 移除 | 5+ | 中 | ⚠️ 需注意 |

**一句话总结**: 大部分应用可以直接从 JDK 17 切到 JDK 25 运行。需要关注的是：强封装进一步收紧、Security Manager 限制、32-bit x86 移除、以及部分 API 废弃/移除。

---

## 2. 破坏性变更汇总

### 必须处理

| 变更 | 引入版本 | 影响 | 检测方法 |
|------|----------|------|----------|
| 强封装 JDK 内部 API | JDK 17+ | `--add-opens` 不再默认生效 | `jdeps --jdk-internals app.jar` |
| Security Manager 限制 | JDK 18-25 | `setSecurityManager()` 抛异常 | `grep -rn 'SecurityManager' src/` |
| 32-bit x86 移除 | JDK 25 | 不支持 32 位平台 | `uname -m` |
| `Thread.stop()` 移除 | JDK 21 | 抛 `UnsupportedOperationException` | `grep -rn 'Thread.stop' src/` |
| 偏向锁完全移除 | JDK 25 | `-XX:+UseBiasedLocking` 被忽略 | `grep -rn 'BiasedLocking' scripts/` |

### 需要关注

| 变更 | 引入版本 | 影响 |
|------|----------|------|
| Finalization 废弃 | JDK 18 | `finalize()` 方法将来移除 |
| UTF-8 为默认编码 | JDK 18 | `Charset.defaultCharset()` 返回 UTF-8 |
| 动态代理 Agent 加载警告 | JDK 21 | `-XX:+EnableDynamicAgentLoading` 所需 |
| String Templates 撤销 | JDK 25 | 如果使用了 JDK 21-22 预览版 |

---

## 3. 新增正式特性

### JDK 17 → JDK 25 新增的正式语言特性

| 特性 | 正式版本 | 说明 | 案例 |
|------|----------|------|------|
| **Virtual Threads** | JDK 21 | 轻量级线程 | [虚拟线程迁移案例](/cases/virtual-threads-migration.md) |
| **Pattern Matching for switch** | JDK 21 | switch 模式匹配 | |
| **Record Patterns** | JDK 21 | Record 解构 | |
| **Sequenced Collections** | JDK 21 | 有序集合接口 | |
| **Scoped Values** | JDK 25 | ThreadLocal 替代 | |
| **Flexible Constructor Bodies** | JDK 25 | 构造器中 super() 前可执行代码 | |
| **Module Import Declarations** | JDK 25 | `import module java.base` | |
| **Compact Source Files** | JDK 25 | 无需类声明的 main 方法 | |
| **Foreign Function & Memory API** | JDK 22 | 替代 JNI 的原生调用 | |
| **Unnamed Variables** | JDK 22 | `_` 占位符 | |

### 性能改进

| 改进 | 版本 | 效果 | 案例 |
|------|------|------|------|
| **分代 ZGC** | JDK 21 正式 | GC 开销降低 50% | [GC 调优案例](/cases/gc-tuning-case.md) |
| **Compact Object Headers** | JDK 25 实验 | 对象头 12→8 字节 | |
| **AOT 命令行优化** | JDK 25 | 简化启动优化 | [启动优化案例](/cases/startup-optimization.md) |
| **JFR Method Timing** | JDK 25 | 方法级性能追踪 | |

---

## 4. GC 演进

### JDK 17 vs JDK 25 GC 状态

| GC | JDK 17 | JDK 25 | 建议 |
|----|--------|--------|------|
| **G1** | 默认 | 默认 | 无需变更 |
| **ZGC** | 正式（非分代） | 正式（分代默认） | 推荐大内存场景 |
| **Shenandoah** | 正式 | 正式 + 分代实验 | 低延迟替代 |
| **CMS** | 已移除 (JDK 14) | 已移除 | 不适用 |
| **Parallel** | 可用 | 可用 | 高吞吐批处理 |

### GC 参数迁移

```bash
# JDK 17 配置
java -XX:+UseZGC -Xmx8g MyApp

# JDK 25 配置（ZGC 默认分代，无需额外参数）
java -XX:+UseZGC -Xmx8g MyApp

# 如需禁用分代模式（不推荐）
java -XX:+UseZGC -XX:-ZGenerational -Xmx8g MyApp
```

---

## 5. 安全与平台变更

### 加密与 TLS

| 变更 | 版本 | 影响 |
|------|------|------|
| TLS 1.0/1.1 禁用 | JDK 20 | 旧客户端连接失败 |
| SHA-1 签名 JAR 限制 | JDK 18 | 旧签名 JAR 可能拒绝加载 |
| KDF API | JDK 25 | 新增密钥派生 API |
| PEM Encodings | JDK 25 预览 | PEM 格式标准化 |

### 平台支持变更

| 变更 | 版本 |
|------|------|
| 移除 32-bit x86 | JDK 25 |
| macOS 最低 11 (Big Sur) | JDK 21 |
| Linux glibc 最低 2.17 | JDK 21 |

---

## 6. 代码迁移示例

### 虚拟线程（最大收益）

```java
// JDK 17: 传统线程池
ExecutorService pool = Executors.newFixedThreadPool(200);
for (Request req : requests) {
    pool.submit(() -> handleRequest(req));
}

// JDK 25: 虚拟线程（I/O 密集型场景推荐）
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (Request req : requests) {
        executor.submit(() -> handleRequest(req));
    }
}
```

### Pattern Matching for switch

```java
// JDK 17: instanceof 链
if (shape instanceof Circle c) {
    return c.radius() * c.radius() * Math.PI;
} else if (shape instanceof Rectangle r) {
    return r.width() * r.height();
}

// JDK 25: switch 模式匹配
return switch (shape) {
    case Circle c    -> c.radius() * c.radius() * Math.PI;
    case Rectangle r -> r.width() * r.height();
    default          -> 0;
};
```

### Record Patterns

```java
// JDK 17: 手动解构
if (obj instanceof Point p) {
    int x = p.x();
    int y = p.y();
}

// JDK 25: Record Pattern 解构
if (obj instanceof Point(int x, int y)) {
    // 直接使用 x, y
}
```

### Scoped Values (替代 ThreadLocal)

```java
// JDK 17: ThreadLocal（虚拟线程中有性能问题）
static final ThreadLocal<User> CURRENT = new ThreadLocal<>();

// JDK 25: Scoped Values（虚拟线程友好）
static final ScopedValue<User> CURRENT = ScopedValue.newInstance();
ScopedValue.where(CURRENT, user).run(() -> handleRequest());
```

---

## 7. 迁移步骤

### 第 1 步：环境准备

```bash
# 安装 JDK 25
sdk install java 25

# 验证版本
java -version
```

### 第 2 步：编译检查

```bash
# 检查编译兼容性
javac --release 25 -Xlint:all src/**/*.java

# 检查内部 API 依赖
jdeps --jdk-internals -cp libs/*.jar app.jar

# 扫描废弃 API
jdeprscan --release 25 app.jar
```

### 第 3 步：运行测试

```bash
# 运行全量测试
mvn clean test -Dmaven.compiler.release=25

# 如有内部 API 依赖，临时添加
java --add-opens java.base/java.lang=ALL-UNNAMED -jar app.jar
```

### 第 4 步：性能验证

```bash
# JFR 录制对比
java -XX:StartFlightRecording=duration=60s,filename=jdk25.jfr -jar app.jar

# GC 日志对比
java -Xlog:gc*:gc-jdk25.log -jar app.jar
```

### 第 5 步：生产部署

```dockerfile
FROM eclipse-temurin:25-jdk
COPY app.jar /app/app.jar
ENTRYPOINT ["java", "-XX:+UseZGC", "-Xmx4g", "-jar", "/app/app.jar"]
```

---

## 8. 依赖兼容性

| 框架/库 | 最低兼容版本 | 说明 |
|---------|-------------|------|
| Spring Boot | 3.2+ | 3.2 支持虚拟线程集成 |
| Spring Framework | 6.1+ | |
| Quarkus | 3.6+ | 原生虚拟线程支持 |
| Micronaut | 4.2+ | |
| Hibernate | 6.4+ | |
| Netty | 4.1.100+ | Event Loop 仍用平台线程 |
| Tomcat | 10.1.16+ | Connector 支持虚拟线程 |
| Jackson | 2.16+ | |
| Lombok | 1.18.30+ | |
| Mockito | 5.8+ | |
| Byte Buddy | 1.14.10+ | Agent 模式需要参数 |
| Maven | 3.9+ | |
| Gradle | 8.5+ | |

---

## 9. JVM 参数变更

### 移除/忽略的参数

```bash
# 以下参数在 JDK 25 中被忽略或报错
-XX:+UseBiasedLocking          # 已移除，忽略
-XX:BiasedLockingStartupDelay  # 已移除，忽略
-Djava.security.manager        # 默认禁用
```

### 推荐的新参数

```bash
# ZGC 分代模式（默认启用）
-XX:+UseZGC

# 虚拟线程调度器
-Djdk.virtualThreadScheduler.parallelism=8

# AOT 缓存
-XX:AOTCache=app.aot

# 动态 Agent 加载（如需）
-XX:+EnableDynamicAgentLoading
```

---

## 10. 常见问题

### Q: 能直接从 JDK 17 跳到 25 吗？

A: 可以。JDK 25 与 JDK 17 保持二进制兼容，绝大部分应用无需修改代码即可运行。

### Q: 需要先升到 JDK 21 再升 25 吗？

A: 不需要。可以直接 17→25。但建议阅读 [JDK 21 变更](/by-version/jdk21/) 了解中间引入的重要特性。

### Q: 虚拟线程可以替代所有线程池吗？

A: 不是。虚拟线程适合 I/O 密集型任务。CPU 密集型场景仍建议使用平台线程 + ForkJoinPool。详见 [虚拟线程迁移案例](/cases/virtual-threads-migration.md)。

### Q: 升级后 GC 需要调整吗？

A: 如果当前用 G1，无需调整（自动获得优化）。如果想切换到 ZGC，只需 `-XX:+UseZGC`。详见 [GC 调优案例](/cases/gc-tuning-case.md)。

---

## 11. 相关资源

### 本项目文档

- [JDK 21→25 迁移指南](./from-21.md) — 如果你已经在 JDK 21 上
- [JDK 25 破坏性变更](/by-version/jdk25/breaking-changes.md)
- [JDK 25 性能调优](/by-version/jdk25/performance.md)
- [JDK 25 已知问题](/by-version/jdk25/known-issues.md)

### 实战案例

- [GC 调优：G1→ZGC 迁移](/cases/gc-tuning-case.md) — P99 200ms→5ms
- [虚拟线程迁移](/cases/virtual-threads-migration.md) — Spring Boot 线程池→虚拟线程
- [启动优化](/cases/startup-optimization.md) — 12s→1.5s
- [内存泄漏排查](/cases/memory-leak-diagnosis.md) — JFR+NMT+MAT

### 官方资源

- [Oracle JDK Migration Guide](https://docs.oracle.com/en/java/javase/25/migrate/)
- [OpenJDK JDK 25](https://openjdk.org/projects/jdk/25/)

---

[← 返回 JDK 25](../index.md) | [JDK 21→25 迁移 →](./from-21.md)
