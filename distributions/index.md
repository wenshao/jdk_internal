# JDK 发行版

> 主流 JDK 发行版的特点、支持策略和选择建议

[← 返回指南](../guides/)

---
## 目录

1. [快速导航](#1-快速导航)
2. [概述](#2-概述)
3. [快速对比](#3-快速对比)
4. [按场景选择](#4-按场景选择)
5. [按平台选择](#5-按平台选择)
6. [许可证说明](#6-许可证说明)
7. [性能对比](#7-性能对比)
8. [版本支持周期](#8-版本支持周期)
9. [安装方式](#9-安装方式)
10. [迁移指南](#10-迁移指南)
11. [相关链接](#11-相关链接)
12. [相关主题](#12-相关主题)

---


## 1. 快速导航

| 页面 | 说明 |
|------|------|
| **[Java 平台变体](variants.md)** | Android、GraalVM Native Image、WebAssembly |
| **[发行版对比](#快速对比)** | Oracle、Temurin、Corretto、Dragonwell 等 |

---

## 2. 概述

OpenJDK 是 Java 的官方参考实现，各大厂商和组织基于 OpenJDK 构建了自己的 JDK 发行版。

```
┌─────────────────────────────────────────────────────────────┐
│                    JDK 发行版生态                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                     OpenJDK (上游)                           │
│                         │                                    │
│     ┌───────────┬───────┴───────┬───────────┐              │
│     │           │               │           │              │
│     ▼           ▼               ▼           ▼              │
│ Oracle JDK   GraalVM        Zulu        Temurin            │
│ (商业)      (Oracle Labs)   (Azul)      (Eclipse)          │
│                                                             │
│     ┌───────────┬───────┴───────┬───────────┐              │
│     │           │               │           │              │
│     ▼           ▼               ▼           ▼              │
│ Corretto    Dragonwell       Kona       Liberica           │
│ (Amazon)    (阿里巴巴)       (腾讯)      (BellSoft)         │
│                                                             │
│     ┌───────────┬───────┴───────┬───────────┐              │
│     │           │               │           │              │
│     ▼           ▼               ▼           ▼              │
│ Semeru     SAPMachine    Microsoft    Loongson             │
│ (IBM)      (SAP)         Build       (龙芯)                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. 快速对比

### 核心发行版对比

| 发行版 | 组织 | 商业支持 | 许可证 | 推荐场景 |
|--------|------|----------|--------|----------|
| **[Oracle JDK](oracle-jdk.md)** | Oracle | ✅ | NFTC (17+免费) | 企业生产，官方支持 |
| **[GraalVM](graalvm.md)** | Oracle Labs | ✅ | GFTC (社区免费) | 云原生，Native Image |
| **[Zulu](azul-zulu.md)** | Azul | ✅ | GPLv2+CPEx | 企业生产，低延迟 |
| **[Prime](azul-prime.md)** | Azul | ✅ | 商业 | 低延迟 (C4 GC) |
| **[Temurin](eclipse-temurin.md)** | Eclipse | ❌ | GPLv2+CPEx | 开发，CI/CD |
| **[Corretto](amazon-corretto.md)** | Amazon | ❌ | GPLv2+CPEx | AWS 环境 |
| **[Dragonwell](alibaba-dragonwell.md)** | 阿里巴巴 | ✅ | GPLv2+CPEx | 阿里云环境 |
| **[Kona](tencent-kona.md)** | 腾讯 | ❌ | GPLv2+CPEx | 腾讯云环境 |
| **[Liberica](bellsoft-liberica.md)** | BellSoft | ✅ | GPLv2+CPEx | 嵌入式，多平台 |
| **[Semeru](ibm-semeru.md)** | IBM | ✅ | GPLv2+CPEx | 内存敏感 (Eclipse OpenJ9) |
| **[SAPMachine](sap-sapmachine.md)** | SAP | ✅ | GPLv2+CPEx | SAP 环境 |
| **[Microsoft Build](microsoft-openjdk.md)** | Microsoft | ✅ (Azure) | GPLv2+CPEx | Azure/Windows 环境 |
| **[Loongson](loongson-jdk.md)** | 龙芯 | ❌ | GPLv2+CPEx | 信创环境 (LoongArch) |

### 按特性分类

#### 完全免费 (无商业限制)
- Eclipse Temurin
- Amazon Corretto
- Tencent Kona
- Loongson JDK
- Oracle JDK 17+ (NFTC 许可)
- GraalVM Community Edition
- Microsoft Build of OpenJDK
- Alibaba Dragonwell Standard Edition

#### 商业支持可用
- Oracle JDK (Java SE Subscription)
- Azul Zulu Enterprise
- Azul Platform Prime
- GraalVM Enterprise
- Alibaba Dragonwell Extended Edition
- BellSoft Liberica
- IBM Semeru
- SAPMachine
- Microsoft (Azure 支持)

#### 特殊功能
- **Native Image**: GraalVM, Liberica Native Image Kit
- **低延迟 GC**: Azul Platform Prime (C4 GC)
- **低内存**: IBM Semeru (OpenJ9)
- **多语言**: GraalVM (Polyglot)

---

## 4. 按场景选择

### 开发环境
| 推荐发行版 | 理由 |
|------------|------|
| **Eclipse Temurin** | 完全免费，社区支持，多平台 |
| **Azul Zulu** | 免费社区版，稳定可靠 |
| **Amazon Corretto** | 免费，长期支持 |

### 生产环境

#### AWS 云环境
| 推荐发行版 | 理由 |
|------------|------|
| **Amazon Corretto** | AWS 优化，免费，长期支持 |
| **Eclipse Temurin** | 通用选择，社区支持 |

#### 阿里云环境
| 推荐发行版 | 理由 |
|------------|------|
| **Alibaba Dragonwell** | 阿里云优化，JWarmUp，Elastic Heap |
| **Eclipse Temurin** | 通用选择 |

#### 腾讯云环境
| 推荐发行版 | 理由 |
|------------|------|
| **Tencent Kona** | 腾讯云优化，容器优化 |
| **Eclipse Temurin** | 通用选择 |

#### Azure 环境
| 推荐发行版 | 理由 |
|------------|------|
| **Microsoft Build** | Azure 优化，Windows 优化 |
| **Eclipse Temurin** | 通用选择 |

### 特殊场景

#### 云原生 / Serverless
| 推荐发行版 | 理由 |
|------------|------|
| **GraalVM** | Native Image，毫秒级启动 |
| **Liberica Native Image Kit** | 免费 Native Image |
| **IBM Semeru** | 低内存占用 |

#### 低延迟交易
| 推荐发行版 | 理由 |
|------------|------|
| **Azul Platform Prime** | C4 GC，pause < 1ms |
| **Oracle JDK** | 官方支持，性能优化 |

#### 大内存堆
| 推荐发行版 | 理由 |
|------------|------|
| **Azul Platform Prime** | C4 GC 支持大堆 |
| **Oracle JDK** | 经过大规模验证 |

#### 容器化部署
| 推荐发行版 | 理由 |
|------------|------|
| **Eclipse Temurin** | 官方 Docker 镜像 |
| **Amazon Corretto** | 小体积镜像 |
| **BellSoft Liberica** | Alpine Linux 支持 |

#### 嵌入式设备
| 推荐发行版 | 理由 |
|------------|------|
| **BellSoft Liberica Lite** | 小体积 |
| **Loongson JDK** | LoongArch 架构支持 |

#### 信创国产化
| 推荐发行版 | 理由 |
|------------|------|
| **Loongson JDK** | 龙芯 CPU，LoongArch |
| **Alibaba Dragonwell** | 国产发行版 |
| **Tencent Kona** | 国产发行版 |

---

## 5. 按平台选择

| 平台 | 推荐发行版 | 备注 |
|------|------------|------|
| **Linux x64** | 任意 | 所有发行版支持 |
| **Linux ARM64** | Zulu, Liberica, Temurin, Corretto, Dragonwell | AWS Graviton, Ampere |
| **Linux LoongArch64** | Loongson JDK | 国产龙芯 CPU |
| **Linux RISC-V64** | Temurin, Liberica | 实验性支持 |
| **Linux Alpine (musl)** | Liberica, Zulu | 静态链接 |
| **Windows x64** | Zulu, Liberica, Microsoft Build, Temurin | |
| **Windows ARM64** | Microsoft Build, Liberica | Snapdragon X Elite |
| **macOS x64** | Zulu, Liberica, Temurin | Intel Mac |
| **macOS ARM64** | Zulu, Liberica, Temurin | Apple Silicon |
| **AIX (ppc64)** | IBM Semeru, Temurin | IBM Power Systems |
| **Linux s390x** | IBM Semeru | IBM Z Mainframe |
| **Linux ppc64le** | IBM Semeru, Temurin | PowerPC LE |

---

## 6. 许可证说明

### GPLv2 + Classpath Exception (CPEx)
- **含义**: 可以自由使用，包括商业用途
- **义务**: 修改源码需要公开
- **适用**: 大多数开源发行版 (Temurin, Corretto, Zulu, Liberica, Kona, Dragonwell Standard, Microsoft Build)

### NFTC (No-Fee Terms and Conditions)
- **含义**: 免费用于生产环境
- **适用**: Oracle JDK 17+

### OTNLA (Oracle Technology Network License Agreement)
- **含义**: 个人免费，商业付费
- **义务**: 商业使用需要 Java SE Subscription
- **适用**: Oracle JDK 8, 11 (旧版本)

### GFTC (GraalVM Free Terms and Conditions)
- **含义**: 生产环境免费
- **限制**: 不包含商业支持
- **适用**: Oracle GraalVM (自 2023 年中起，Oracle 将原 CE 和 EE 合并为单一的 "Oracle GraalVM" 发行版，统一使用 GFTC 许可)

---

## 7. 性能对比

> ⚠️ **注意**: 以下数据为近似值，实际性能因应用场景而异

### 启动时间 (Hello World)

| 发行版 | JVM | 启动时间 |
|--------|-----|----------|
| OpenJDK (HotSpot) | HotSpot | ~100ms |
| Eclipse Temurin | HotSpot | ~100ms |
| Amazon Corretto | HotSpot | ~100ms |
| Azul Zulu | HotSpot | ~100ms |
| Alibaba Dragonwell | HotSpot | ~95ms |
| GraalVM | Graal JIT | ~120ms |
| GraalVM Native | AOT | ~5ms |
| IBM Semeru | Eclipse OpenJ9 | ~60ms |

### 内存占用 (空闲应用)

| 发行版 | JVM | 内存占用 |
|--------|-----|----------|
| OpenJDK (HotSpot) | HotSpot | ~35MB |
| Eclipse Temurin | HotSpot | ~35MB |
| Amazon Corretto | HotSpot | ~35MB |
| Azul Zulu | HotSpot | ~35MB |
| Alibaba Dragonwell | HotSpot | ~33MB |
| GraalVM | Graal JIT | ~45MB |
| GraalVM Native | AOT | ~5MB |
| IBM Semeru | Eclipse OpenJ9 | ~20MB |

### 吞吐量 (SPECjbb2015)

| 发行版 | 相对得分 |
|--------|----------|
| OpenJDK (HotSpot) | 100% (基准) |
| Eclipse Temurin | 100% |
| Amazon Corretto | 100% |
| Azul Zulu | 100% |
| Alibaba Dragonwell | 100-105% |
| Azul Platform Prime | 110-130% (C4 GC) |
| IBM Semeru | 90-95% (Eclipse OpenJ9) |

---

## 8. 版本支持周期

### LTS 版本支持截止

| 发行版 | JDK 8 | JDK 11 | JDK 17 | JDK 21 | JDK 26 |
|----------|-------|--------|--------|--------|--------|
| **Oracle JDK** | 2030-12 | 2026-01 | 2029-10 | 2031-10 | 2029-10 |
| **Temurin** | 2026-05 | 2027-10 | 2029-10 | 2031-10 | 2032-10 |
| **Corretto** | 2026-05 | 2027-09 | 2029-09 | 2032-04 | 2032-09 |
| **Zulu** | 2030-12 | 2027-10 | 2029-10 | 2031-10 | 2032-10 |
| **Dragonwell** | 2029-07 | 2027-10 | 2029-10 | 2031-10 | 2032-10 |
| **Kona** | 2026-05 | 2027-10 | 2029-10 | 2031-10 | 2032-10 |
| **Liberica** | 2026-05 | 2027-10 | 2029-10 | 2031-10 | 2032-10 |
| **Semeru** | 2026-09 | 2027-10 | 2029-10 | 2031-10 | 2032-10 |
| **SAPMachine** | 2030-12 | 2027-10 | 2029-10 | 2031-10 | 2032-10 |
| **Microsoft Build** | 2026-05 | 2027-10 | 2029-10 | 2031-10 | 2032-10 |
| **Loongson** | 2026-05 | 2027-10 | 2029-10 | 2031-10 | 2032-10 |

> ⚠️ **注意**: KDK 26 支持截止日期因厂商而异，需以厂商确认

---

## 9. 安装方式

### SDKMAN (推荐 Linux/macOS)

```bash
# 安装 SDKMAN
curl -s "https://get.sdkman.io" | bash

# 查看可用版本
sdk list java

# 安装
sdk install java 21-tem      # Temurin
sdk install java 21-zulu     # Zulu
sdk install java 21-amzn     # Corretto
sdk install java 21-graal    # GraalVM
sdk install java 21-librca   # Liberica
sdk install java 21-sem      # Semeru
```

### Docker

```bash
# Temurin
docker pull eclipse-temurin:21-jdk

# Corretto
docker pull amazoncorretto:21

# Zulu
docker pull azul/zulu-openjdk:21

# GraalVM
docker pull ghcr.io/graalvm/native-image-community:21

# Liberica
docker pull bellsoft/liberica-runtime-container:jdk-21

# Semeru
docker pull ibm-semeru-runtimes:open-21-jdk

# Microsoft Build
docker pull mcr.microsoft.com/openjdk/jdk:21
```

### 包管理器

```bash
# Homebrew (macOS)
brew install --cask temurin
brew install --cask zulu

# apt (Ubuntu)
apt install openjdk-21-jdk

# yum (Amazon Linux)
yum install java-21-amazon-corretto

# winget (Windows)
winget install EclipseAdoptium.Temurin.21.JDK
winget install Microsoft.OpenJDK.21
```

---

## 10. 迁移指南

### 从 Oracle JDK 迁移

大多数 OpenJDK 发行版与 Oracle JDK **100% 兼容**。

```bash
# 1. 选择目标发行版 (推荐 Temurin)
sdk install java 21-tem

# 2. 验证
java -version
javac -version

# 3. 运行测试
./mvnw test

# 4. 性能验证
# 使用 JMC 或其他工具验证性能
```

### 验证工具

```bash
# 检查 JDK 版本
java -version

# 检查编译器版本
javac -version

# 检查废弃 API
jdeprscan --release 21 myapp.jar

# 检查依赖
jdeps --jdk-intro myapp.jar
```

---

## 11. 相关链接

### 对比工具

| 工具 | 链接 |
|------|------|
| WhichJDK | https://whichjdk.com/ |
| JDK Comparison | https://jdkcomparison.com/ |
| BellSoft Comparison | [PDF](https://bell-sw.com/blog/oracle-java-alternatives-comparison-of-openjdk-distributions/) |

### 官方资源

| 资源 | 链接 |
|------|------|
| OpenJDK | https://openjdk.org/ |
| JDK Mission Control | https://jdk.java.net/jmc/ |
| Adoptium Working Group | https://adoptium.net/ |

### 社区讨论

- [Reddit: Best JDK Distribution](https://www.reddit.com/r/java/comments/1mfkcxv/the_best_generalpurpose_jdk_out_there_and_whats/)
- [2024三大免费JDK横向评测](https://blog.csdn.net/git9versioner/article/details/154422095)

---

## 12. 相关主题

- [JDK 版本迁移](../guides/migration-guide.md) - 版本迁移指南
- [GraalVM](../by-topic/core/graalvm/) - GraalVM 详细文档
- [性能优化](../by-topic/core/performance/) - JVM 性能调优

---

**最后更新**: 2026-03-20

**Sources**:
- [WhichJDK.com](https://whichjdk.com/)
- [JDKComparison.com](https://jdkcomparison.com/)
- [2024 State of Java Ecosystem](https://newrelic.com/resources/report/2024-state-of-the-java-ecosystem)
- [Loongson JDK](https://www.loongnix.cn/zh/api/java/)
