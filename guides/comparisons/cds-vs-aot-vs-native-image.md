---

# 启动优化方案对比: CDS vs AOT Cache vs GraalVM Native Image

---

## 目录

1. [核心设计哲学](#1-核心设计哲学)
2. [多维度对比](#2-多维度对比)
3. [Class Data Sharing (CDS)](#3-class-data-sharing-cds)
4. [AOT Cache (JEP 483/516)](#4-aot-cache-jep-483516)
5. [GraalVM Native Image](#5-graalvm-native-image)
6. [性能对比](#6-性能对比)
7. [决策指南](#7-决策指南)

---

## 1. 核心设计哲学

| 方案 | 一句话描述 |
|---|---|
| **CDS** | 将类元数据归档到文件，启动时直接映射到内存 |
| **AOT Cache** | 在 CDS 基础上缓存 AOT 编译代码和堆对象 |
| **Native Image** | 编译为独立原生可执行文件，无需 JVM |

---

## 2. 多维度对比

| 维度 | CDS (AppCDS) | AOT Cache (JDK 24+) | Native Image |
|------|-------------|---------------------|-------------|
| **原理** | 类元数据归档 | 类元数据 + AOT 代码 + 堆对象 | 提前编译为原生代码 |
| **启动加速** | 10-20% | 30-50% | 10-100x |
| **峰值性能** | 不影响 | 略低 (AOT < C2) | 低 10-30% |
| **GC 选择** | 任意 | 任意 (JDK 26+) | Serial/G1 (有限) |
| **反射支持** | ✅ 完全 | ✅ 完全 | ⚠️ 需配置 |
| **动态代理** | ✅ 完全 | ✅ 完全 | ⚠️ 需配置 |
| **JNI** | ✅ 完全 | ✅ 完全 | ⚠️ 需配置 |
| **构建复杂度** | 低 (1 步) | 中 (2 步) | 高 (专用工具链) |
| **调试难度** | 简单 | 简单 | 困难 |
| **运行时兼容** | 100% | 99% | 部分不兼容 |
| **JDK 版本** | 5+ | 24+ | GraalVM |

---

## 3. Class Data Sharing (CDS)

### 3.1 工作原理

```
CDS 流程:
┌──────────────────────────────────────────────────┐
│ 第一步: 训练运行 (生成归档)                      │
│   java -XX:ArchiveClassesAtExit=app.jsa -jar app.jar │
│   → 记录加载的类元数据到 app.jsa 文件            │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│ 第二步: 使用归档启动                             │
│   java -XX:SharedArchiveFile=app.jsa -jar app.jar │
│   → 直接 mmap 归档文件到内存，跳过类加载和解析   │
└──────────────────────────────────────────────────┘
```

### 3.2 CDS 类型

| 类型 | JDK 版本 | 说明 |
|------|---------|------|
| Default CDS | 12+ | JVM 自带的默认归档 (仅 java.base) |
| AppCDS | 13+ | 应用类归档 (需要训练) |
| Dynamic CDS | 13+ | 运行时自动生成归档 |

### 3.3 配置

```bash
# 1. 生成归档
java -XX:ArchiveClassesAtExit=app-cds.jsa \
     -cp app.jar \
     com.example.Main

# 2. 使用归档启动
java -XX:SharedArchiveFile=app-cds.jsa \
     -cp app.jar \
     com.example.Main
```

---

## 4. AOT Cache (JEP 483/516)

### 4.1 工作原理

```
AOT Cache 架构:
┌──────────────────────────────────────────────────┐
│ AOT 归档内容:                                    │
│  ├── 类元数据 (CDS)                              │
│  ├── AOT 编译的机器码 (LW1/LW2 等)              │
│  ├── 常量池解析结果                               │
│  └── 堆对象 (JDK 26, JEP 516)                   │
│                                                  │
│ 启动时:                                          │
│  1. mmap AOT 归档 → 内存映射                     │
│  2. 类元数据直接可用 (跳过解析)                  │
│  3. AOT 代码直接执行 (跳过解释和 JIT 编译)       │
│  4. 堆对象直接映射 (跳过初始化)                  │
└──────────────────────────────────────────────────┘
```

### 4.2 JDK 版本对比

| 版本 | AOT 能力 | 说明 |
|------|---------|------|
| JDK 24 | JEP 483 | AOT 类加载和链接 (约 -40% 启动时间) |
| JDK 26 | JEP 516 | AOT 对象缓存 + 任意 GC 支持 |

### 4.3 配置 (JDK 26)

```bash
# 1. 训练运行
java -XX:AOTCache=app-aot.jsa \
     -cp app.jar \
     com.example.Main

# 2. 使用 AOT 缓存启动
java -XX:AOTCache=app-aot.jsa \
     -cp app.jar \
     com.example.Main
```

---

## 5. GraalVM Native Image

### 5.1 工作原理

```
Native Image 编译:
┌──────────────────────────────────────────────────┐
│ 源代码 (.java)                                    │
│    │                                              │
│    ▼                                              │
│ 编译 → .class                                     │
│    │                                              │
│    ▼                                              │
│ Native Image: 静态分析 → 只包含可达代码           │
│    │                                              │
│    ├── 类初始化在编译期执行 (build-time init)     │
│    ├── 反射/代理/JNI 需要显式配置                 │
│    └── GC: Serial 或 G1 (非 ZGC/Shenandoah)      │
│    │                                              │
│    ▼                                              │
│ 原生可执行文件 (无 JVM)                           │
│ 启动时间: 毫秒级                                  │
│ 内存占用: 10-50MB (vs JVM 200MB+)               │
└──────────────────────────────────────────────────┘
```

### 5.2 配置

```bash
# 构建原生镜像
native-image -jar app.jar -o app-native

# 直接运行
./app-native

# 需要反射配置 (reflect-config.json)
[
  {"name": "com.example.MyClass", "allDeclaredConstructors": true}
]
```

---

## 6. 性能对比

### Spring PetClinic 示例（示意数据）

| 指标 | 普通启动 | +CDS | +AOT Cache | Native Image |
|------|---------|------|-----------|-------------|
| **启动时间** | 2.8s | 2.3s (-18%) | 1.2s (-57%) | 0.05s (-98%) |
| **首次请求延迟** | 3.5s | 2.8s | 1.5s | 0.08s |
| **峰值吞吐量** | 5,000 rps | 5,000 rps | 4,800 rps | 3,500 rps |
| **内存占用** | 320MB | 300MB | 280MB | 80MB |
| **GC 停顿** | 正常 | 正常 | 正常 | 较大 (Serial) |

> **说明**: 数据为示意数据，实际结果因应用和硬件而异。Native Image 的峰值吞吐量通常比 JIT 低 10-30%。

---

## 7. 决策指南

```
开始
  │
  ├─ 需要极致启动速度 (<100ms)?
  │    └── 是 → GraalVM Native Image
  │         (接受峰值性能损失和兼容性限制)
  │
  ├─ 需要保持峰值性能?
  │    └── 是 → CDS 或 AOT Cache
  │         (保持 JIT 编译优势)
  │
  ├─ JDK 24+ 且 GC 灵活?
  │    └── 是 → AOT Cache
  │         (最佳启动/性能平衡)
  │
  ├─ 任何 JDK 版本?
  │    └── 是 → CDS (AppCDS)
  │         (零风险，简单)
  │
  └─ 云原生 / Serverless?
       └── Native Image (最小镜像 + 最快冷启动)
```

---

## 相关链接

- [启动优化案例](/cases/startup-optimization.md)
- [JEP 516: AOT Cache 实现](/deep-dive/jep-516-aot-cache.md)
- [性能优化主题](/by-topic/core/performance/)
- [GraalVM 文档](/distributions/graalvm.md)
