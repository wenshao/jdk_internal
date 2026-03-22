# AOT 命令行优化与方法分析 深度分析

> JDK 25 正式特性 - JEP 514 (AOT Ergonomics) + JEP 515 (AOT Method Profiling)

---
## 目录

1. [概述](#1-概述)
2. [AOT 演进历程](#2-aot-演进历程)
3. [JEP 514: 命令行优化](#3-jep-514-命令行优化)
4. [JEP 515: 方法分析](#4-jep-515-方法分析)
5. [工作原理](#5-工作原理)
6. [实战配置](#6-实战配置)
7. [与其他启动优化对比](#7-与其他启动优化对比)
8. [相关链接](#8-相关链接)

---


## 1. 概述

JDK 25 对 AOT (Ahead-of-Time) 缓存机制进行了两项改进：

| JEP | 改进 | 效果 |
|-----|------|------|
| JEP 514 | 简化 AOT 命令行参数 | 更容易启用 AOT |
| JEP 515 | AOT 方法分析数据 | 更好的编译质量 |

---

## 2. AOT 演进历程

```
JDK 9-17:  实验性 AOT 编译器 (jaotc) → JDK 17 移除 (JEP 410)
JDK 13:    动态 CDS 归档 (JEP 350)
JDK 21-24: CDS + AOT Cache 逐步改进
JDK 25:    AOT 命令行优化 + 方法分析 ← 当前
JDK 26:    AOT 对象缓存，支持任意 GC (JEP 516)
```

### CDS 与 AOT 的关系

```
CDS (Class Data Sharing):
  共享类元数据 → 减少类加载时间

AOT Cache:
  预编译 + 缓存方法 profiling 数据 → 减少 JIT 编译时间

两者结合:
  CDS + AOT → 类加载快 + JIT 预热快 = 最优启动时间
```

---

## 3. JEP 514: 命令行优化

### 之前的配置方式 (JDK 24)

```bash
# 步骤 1: 创建类列表
java -Xshare:off -XX:DumpLoadedClassList=classes.lst -jar myapp.jar

# 步骤 2: 创建 CDS 归档
java -Xshare:dump -XX:SharedClassListFile=classes.lst \
     -XX:SharedArchiveFile=myapp.jsa

# 步骤 3: 使用归档
java -Xshare:on -XX:SharedArchiveFile=myapp.jsa -jar myapp.jar
```

### JDK 25 简化方式

```bash
# 一步录制
java -XX:AOTConfiguration=app.aotconf -jar myapp.jar

# 一步生成缓存
java -XX:AOTCache=app.aot -XX:AOTConfiguration=app.aotconf -jar myapp.jar

# 使用缓存
java -XX:AOTCache=app.aot -jar myapp.jar
```

### 动态 CDS 归档（更简单）

```bash
# 自动归档
java -XX:ArchiveClassesAtExit=app.jsa -jar myapp.jar

# 使用归档
java -XX:SharedArchiveFile=app.jsa -jar myapp.jar
```

---

## 4. JEP 515: 方法分析

### 问题背景

JIT 编译器的分层编译策略在应用启动阶段效率不高：

```
传统启动流程:
1. 解释执行 (慢)
2. C1 编译 (tier 1-3, 有 profiling)
3. C2 编译 (tier 4, 优化, 依赖 profiling 数据)

问题: 步骤 2-3 需要运行时收集 profiling，启动阶段来不及收集
```

### AOT Method Profiling 解决方案

```
首次运行 (录制 profiling):
1. 正常运行应用
2. JVM 收集方法调用频率、分支概率、类型信息
3. 保存到 AOT 配置文件

后续运行 (使用 profiling):
1. 加载缓存的 profiling 数据
2. JIT 直接使用高质量 profiling → 跳过 C1 收集阶段
3. C2 更快产出优化代码
```

### 启用方式

```bash
# 录制含 profiling 的配置
java -XX:AOTConfiguration=app.aotconf \
     -XX:+AOTMethodProfiling \
     -jar myapp.jar

# 生成带 profiling 的缓存
java -XX:AOTCache=app.aot \
     -XX:AOTConfiguration=app.aotconf \
     -jar myapp.jar

# 启动时自动利用缓存的 profiling
java -XX:AOTCache=app.aot -jar myapp.jar
```

---

## 5. 工作原理

### AOT 缓存内容

```
app.aot 文件内容:
├── 共享类元数据 (CDS)
│   ├── 系统类 (java.lang.*, java.util.*, ...)
│   └── 应用类 (com.myapp.*, ...)
├── 方法 Profiling 数据 (JEP 515)
│   ├── 调用计数
│   ├── 分支概率
│   ├── 类型 profile (receiver type)
│   └── 内联决策提示
└── 预编译代码 (可选)
    └── 热点方法的 native code
```

### C2 编译器利用 profiling 数据

```
无 AOT profiling:
  方法调用 1000 次 → 收集 profiling → C2 编译 → 优化代码
  [------- 慢 (解释/C1) -------][-- C2 --][----- 快 -----]

有 AOT profiling:
  启动 → 加载缓存 profiling → C2 立即编译 → 优化代码
  [- C2 -][--------------- 快 ----------------]
```

---

## 6. 实战配置

### Spring Boot 应用

```bash
# 1. 录制 (运行一段时间后停止)
java -XX:AOTConfiguration=spring.aotconf \
     -XX:+AOTMethodProfiling \
     -jar myapp.jar
# 接收几个请求后 Ctrl+C

# 2. 生成缓存
java -XX:AOTCache=spring.aot \
     -XX:AOTConfiguration=spring.aotconf \
     -jar myapp.jar

# 3. 生产使用
java -XX:AOTCache=spring.aot \
     -Xmx2g \
     -jar myapp.jar
```

### Docker 集成

```dockerfile
FROM eclipse-temurin:25-jdk AS builder

COPY myapp.jar /app/myapp.jar
WORKDIR /app

# 构建阶段生成 AOT 缓存
RUN java -XX:AOTConfiguration=app.aotconf -jar myapp.jar &  \
    sleep 10 && kill %1
RUN java -XX:AOTCache=app.aot -XX:AOTConfiguration=app.aotconf -jar myapp.jar & \
    sleep 5 && kill %1

FROM eclipse-temurin:25-jre
COPY --from=builder /app/myapp.jar /app/
COPY --from=builder /app/app.aot /app/

ENTRYPOINT ["java", "-XX:AOTCache=/app/app.aot", "-jar", "/app/myapp.jar"]
```

### CI/CD 集成

```bash
#!/bin/bash
# ci-build-aot.sh - 在 CI 中生成 AOT 缓存

APP_JAR="target/myapp.jar"
AOT_CONF="target/app.aotconf"
AOT_CACHE="target/app.aot"

echo "Step 1: Recording AOT configuration..."
timeout 30 java -XX:AOTConfiguration=$AOT_CONF -jar $APP_JAR || true

echo "Step 2: Building AOT cache..."
timeout 30 java -XX:AOTCache=$AOT_CACHE \
     -XX:AOTConfiguration=$AOT_CONF -jar $APP_JAR || true

echo "AOT cache generated: $AOT_CACHE"
ls -la $AOT_CACHE
```

---

## 7. 与其他启动优化对比

| 方案 | 启动提升 | 复杂度 | 维护成本 | 兼容性 |
|------|----------|--------|----------|--------|
| 默认 CDS | 10-20% | 低 | 零 | 极好 |
| 动态 CDS | 20-30% | 低 | 低 | 好 |
| AOT Cache | 40-60% | 中 | 中 | 好 |
| AOT + Profiling | 50-70% | 中 | 中 | 好 |
| GraalVM Native | 90-95% | 高 | 高 | 有限 |

**选择建议**:
- 通用应用: 动态 CDS（零成本收益）
- 微服务: AOT Cache + Profiling
- Serverless/CLI 工具: 考虑 GraalVM Native Image
- 大型应用: AOT Cache（Native Image 可能受限）

---

## 8. 相关链接

- [JEP 514: AOT Command-Line Ergonomics](https://openjdk.org/jeps/514)
- [JEP 515: AOT Method Profiling](https://openjdk.org/jeps/515)
- [启动优化案例](/cases/startup-optimization.md)
- [JDK 25 性能调优](../performance.md)
- [JDK 26 AOT 对象缓存](/by-version/jdk26/deep-dive/aot-improvements.md)

---

[← 返回 JDK 25 深度分析](../)
