# AOT 编译演进

> JEP 295 → GraalVM Native Image → Project Leyden (JEP 483/514/515/516)

[← 返回 JIT 编译概览](README.md)

---

## 目录

1. [演进概览](#1-演进概览)
2. [JEP 295: jaotc (已移除)](#2-jep-295-jaotc-已移除)
3. [GraalVM Native Image](#3-graalvm-native-image)
4. [Project Leyden (JDK 24+)](#4-project-leyden-jdk-24)
5. [Graal 编译器简史](#5-graal-编译器简史)

---

## 1. 演进概览

Java AOT (Ahead-of-Time) 编译经历了多个阶段的演进:

| 阶段 | JEP/项目 | JDK 版本 | 状态 | 说明 |
|------|----------|----------|------|------|
| **第一代** | JEP 295 (jaotc) | JDK 9-15 | 已移除 (JDK 16) | 基于 Graal 的实验性 AOT；使用复杂、收益有限 |
| **GraalVM** | Native Image | 外部项目 | 活跃 | 闭合世界 (closed-world) AOT；不支持完整 Java 动态特性 |
| **第二代** | Project Leyden | JDK 24+ | 进行中 | 渐进式 AOT，保持 Java 完整语义 |

```
JDK 9 ──── JDK 16 ──── JDK 24 ──── JDK 25 ──── JDK 26+
  │           │           │           │           │
JEP 295   JEP 410      JEP 483    JEP 515    持续增强
jaotc     移除 jaotc   Leyden     AOT Method  Leyden
引入      + Graal JIT  首批 JEP    Profiling   扩展
```

---

## 2. JEP 295: jaotc (已移除)

**JDK 9 引入, JDK 16 移除 (JEP 410)**

- 使用 Graal 编译器将字节码 AOT 编译为共享库 (.so)
- 需要手动指定要编译的类/方法
- 不支持完整的 Java 动态特性 (反射、动态类加载受限)
- 维护成本高，使用者少

**移除原因:**
- 使用复杂，几乎没有生产用户
- 收益有限 (启动时间改善不显著)
- 维护与 Graal 版本同步的成本过高

---

## 3. GraalVM Native Image

**独立于 OpenJDK 主线的外部项目**

SubstrateVM 提供的闭合世界 (closed-world) AOT 编译:

| 特性 | 说明 |
|------|------|
| **编译方式** | 编译时确定所有可达代码 (points-to analysis) |
| **启动时间** | 可达毫秒级 |
| **内存占用** | 显著降低 (无 JIT 编译器运行时开销) |
| **动态特性** | 不支持运行时动态类加载；反射、JNI、代理需额外配置 |
| **生态兼容** | 需要框架适配 (Quarkus、Micronaut、Spring Native) |

**与 Leyden 的关键区别:**
- GraalVM Native Image 要求闭合世界假设 (closed-world assumption)
- Leyden 保持 Java 的完整动态性

> 详见: [GraalVM 技术内幕专题](../graalvm/)

---

## 4. Project Leyden (JDK 24+)

Project Leyden 采用与 jaotc 和 Native Image 不同的策略——**渐进式约束 (gradual constraints)**，在保持 Java 完整语义的前提下逐步引入 AOT 能力。

### 核心 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| **JEP 483** | Ahead-of-Time Class Loading & Linking | AOT 类加载和链接缓存；训练运行 (training run) 记录类加载顺序，后续启动直接使用 |
| **JEP 514** | Ahead-of-Time Cache for Code | AOT 代码缓存；缓存 JIT 编译结果，后续启动直接加载已编译代码 |
| **JEP 515** | Ahead-of-Time Method Profiling | AOT 方法 Profiling；缓存训练运行的 profiling 数据，让 C2 在启动时就能做高质量编译 |
| **JEP 516** | Ahead-of-Time Compilation (Preview) | AOT 编译 (预览)；将编译结果持久化存储 |

### Leyden 的设计原则

| 原则 | 说明 |
|------|------|
| **保持完整动态性** | 反射、动态加载等完全支持 (no closed-world assumption) |
| **基于训练运行** | 收集运行时数据，不要求静态分析确定所有可达代码 |
| **渐进式改进** | 每个 JEP 独立提供收益，可组合使用 |
| **透明优化** | 应用代码无需修改 |

### 使用方式 (JDK 25+)

```bash
# 步骤 1: 训练运行 (收集数据)
java -XX:AOTMode=record -XX:AOTConfiguration=app.aotconf \
     -cp app.jar com.example.Main

# 步骤 2: 创建 AOT 缓存
java -XX:AOTMode=create -XX:AOTConfiguration=app.aotconf \
     -XX:AOTCache=app.aot -cp app.jar

# 步骤 3: 使用 AOT 缓存启动
java -XX:AOTCache=app.aot -cp app.jar com.example.Main
```

### 性能数据

据早期测试报告，启动时间改善可达 15-25% (具体数字因应用而异):
- JEP 483 (类加载缓存): 减少类加载和链接时间
- JEP 515 (方法 Profiling): C2 编译在启动时即可获得高质量 profiling 数据

---

## 5. Graal 编译器简史

### JVMCI: JIT 编译器接口

**JEP 243: Java-Level JVM Compiler Interface (JDK 9)**
- 定义了 JVM 与外部 JIT 编译器之间的标准接口 (standard interface)
- 允许用 Java 编写的编译器替代 C2
- 源码位于 `src/hotspot/share/jvmci/`
- Graal 编译器是 JVMCI 的主要消费者

### Graal JIT 在 OpenJDK 中的历程

| 版本 | 事件 | 说明 |
|------|------|------|
| JDK 9 | JEP 243 (JVMCI) | 引入编译器接口，为 Graal 提供插入点 |
| JDK 10 | JEP 317 (Experimental Graal) | Graal JIT 作为实验性特性加入 OpenJDK |
| JDK 17 | JEP 410 (Remove Experimental Graal) | 从 OpenJDK 中移除实验性 Graal JIT 编译器 |

**JEP 410 移除的原因:**
- OpenJDK 中的 Graal 副本与 GraalVM 的 Graal 版本逐渐分歧
- 很少有用户通过 OpenJDK 使用 Graal JIT
- JVMCI 接口保留，用户仍可通过 GraalVM 或自行集成使用 Graal

### GraalVM 外部发展

Graal 编译器在 GraalVM 项目中继续独立发展:

| 特性 | 说明 |
|------|------|
| **GraalVM CE/EE** | 提供 Graal JIT (替代 C2) + Native Image (AOT) |
| **Truffle 框架** | 基于 Graal 的多语言运行时 (JavaScript、Python、Ruby 等) |
| **部分转义分析** (PEA) | GraalVM 独有的高级优化，比 C2 的逃逸分析更精细 |
| **推测性优化** | 更激进的推测性去虚化和内联 |
| **版本跟踪** | GraalVM 从 JDK 21 开始跟踪 OpenJDK 版本发布节奏 |

> 详见: [Graal JIT](graal-jit.md) | [Graal vs C2 性能对比](graal-vs-c2-performance.md) | [GraalVM 独有技术](graal-unique-features.md)

---

## 相关文档

- [Graal JIT](graal-jit.md) - JVMCI 架构、Truffle 框架
- [Graal vs C2 性能对比](graal-vs-c2-performance.md) - 基准测试数据
- [GraalVM 独有技术](graal-unique-features.md) - PEA、推测性优化
- [GraalVM 技术内幕专题](../graalvm/) - 完整的 GraalVM 文档
- [近期改进](recent-changes.md) - JDK 25/26 AOT 相关更新

---

**最后更新**: 2026-03-22
