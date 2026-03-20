# JDK 发行版对比

> 主流 JDK 发行版的特点、支持策略和选择建议

---

## 概述

OpenJDK 是 Java 的官方参考实现，各大厂商和组织基于 OpenJDK 构建了自己的 JDK 发行版，提供不同的特性和支持策略。

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
└─────────────────────────────────────────────────────────────┘
```

---

## 发行版对比

### 快速对比表

| 发行版 | 组织 | 商业支持 | 特点 | 推荐场景 |
|--------|------|----------|------|----------|
| **OpenJDK** | Oracle 社区 | ❌ | 官方参考实现 | 开发、测试 |
| **Oracle JDK** | Oracle | ✅ | 商业支持，安全更新 | 企业生产 |
| **GraalVM** | Oracle Labs | ✅ | Native Image, Truffle | 云原生、多语言 |
| **Zulu** | Azul | ✅ | 优化的 GC，多平台 | 企业生产 |
| **Prime** | Azul | ✅ | C4 GC，低延迟 | 低延迟场景 |
| **Corretto** | Amazon | ❌ | AWS 优化，免费 | AWS 环境 |
| **Dragonwell** | 阿里巴巴 | ✅ | 阿里云优化 | 阿里云环境 |
| **Kona** | 腾讯 | ❌ | 容器优化 | 腾讯云环境 |
| **Temurin** | Eclipse | ❌ | 社区支持，免费 | 通用场景 |
| **Liberica** | BellSoft | ✅ | 多平台，轻量级 | 嵌入式、云 |
| **Semeru** | IBM | ✅ | OpenJ9，低内存 | 内存敏感 |
| **SAPMachine** | SAP | ✅ | SAP 优化 | SAP 环境 |
| **Microsoft Build** | Microsoft | ✅ | Azure 优化 | Azure 环境 |

---

## 详细介绍

### Oracle JDK

Oracle 官方 JDK 发行版。

| 属性 | 值 |
|------|-----|
| **组织** | Oracle |
| **官网** | https://www.oracle.com/java/ |
| **许可证** | OTNLA (商业) / GPLv2 (个人) |
| **商业支持** | ✅ |
| **特性** | 官方支持，安全更新，性能优化 |

**许可证**:
- 个人使用：免费
- 商业使用：需要订阅 Oracle Java SE Subscription

**适用场景**:
- 需要官方商业支持的企业
- Oracle 技术栈环境

---

### GraalVM

Oracle Labs 开发的高性能 JDK。

| 属性 | 值 |
|------|-----|
| **组织** | Oracle Labs |
| **官网** | https://www.graalvm.org/ |
| **许可证** | GPLv2 + CE / GFTC (企业) |
| **商业支持** | ✅ |
| **特性** | Native Image, Truffle, Polyglot |

**核心特性**:
- **Graal JIT**: 用 Java 编写的高性能 JIT
- **Native Image**: AOT 编译，毫秒级启动
- **Truffle**: 多语言运行时框架
- **Polyglot**: JavaScript/Python/Ruby/R 支持

**适用场景**:
- 云原生 / Serverless
- 微服务（Quarkus, Spring Native）
- 多语言应用

**安装**:
```bash
# SDKMAN
sdk install java 21-graal
sdk use java 21-graal
```

→ [详细文档](/by-topic/core/graalvm/)

---

### Azul Zulu

Azul Systems 提供的商业 JDK 发行版。

| 属性 | 值 |
|------|-----|
| **组织** | Azul Systems |
| **官网** | https://www.azul.com/downloads/ |
| **许可证** | GPLv2 + CPEx (社区) / 商业 |
| **商业支持** | ✅ |
| **特性** | 优化的 GC，多平台支持，长期支持 |

**版本**:
- **Zulu Community**: 免费社区版
- **Zulu Enterprise**: 商业版，技术支持
- **Zulu Platform Prime**: 高性能版，包含 C4 GC

**C4 GC (Continuously Concurrent Compacting Collector)**:
- 低延迟 GC，pause 时间 < 1ms
- 适用于大堆内存场景
- 仅 Prime 版本可用

**安装**:
```bash
# SDKMAN
sdk install java 21-zulu
sdk use java 21-zulu

# Docker
docker pull azul/zulu-openjdk:21
```

**适用场景**:
- 企业生产环境
- 需要商业支持
- 大堆内存应用 (Prime + C4 GC)

---

### Amazon Corretto

Amazon 提供的免费 JDK 发行版。

| 属性 | 值 |
|------|-----|
| **组织** | Amazon Web Services |
| **官网** | https://aws.amazon.com/corretto/ |
| **许可证** | GPLv2 + CPEx |
| **商业支持** | ❌ (AWS 支持计划) |
| **特性** | AWS 优化，免费，长期支持 |

**特点**:
- 完全免费，无需订阅
- AWS 环境优化
- 包含 Amazon 安全补丁
- 长期支持 (LTS 版本 8 年)

**版本**:
- Corretto 8 (支持至 2026)
- Corretto 11 (支持至 2027)
- Corretto 17 (支持至 2029)
- Corretto 21 (支持至 2032)

**安装**:
```bash
# SDKMAN
sdk install java 21-amzn
sdk use java 21-amzn

# Docker
docker pull amazoncorretto:21

# Amazon Linux
sudo yum install java-21-amazon-corretto
```

**适用场景**:
- AWS 环境
- 成本敏感的企业
- 需要长期支持的 LTS 版本

---

### Alibaba Dragonwell

阿里巴巴提供的 JDK 发行版。

| 属性 | 值 |
|------|-----|
| **组织** | 阿里巴巴 |
| **官网** | https://dragonwell-jdk.io/ |
| **GitHub** | https://github.com/alibaba/dragonwell8 |
| **许可证** | GPLv2 + CPEx |
| **商业支持** | ✅ (阿里云) |
| **特性** | 阿里云优化，JWarmUp，Elastic Heap |

**核心特性**:
- **JWarmUp**: 预热优化，减少冷启动
- **Elastic Heap**: 弹性堆内存
- **Wisp**: 协程支持 (类似虚拟线程)
- **JFR 增强**: 更丰富的监控

**版本**:
- Dragonwell 8 (基于 JDK 8)
- Dragonwell 11 (基于 JDK 11)
- Dragonwell 17 (基于 JDK 17)
- Dragonwell 21 (基于 JDK 21)

**安装**:
```bash
# 阿里云
yum install dragonwell

# Docker
docker pull dragonwell-registry.cn-hangzhou.cr.aliyuncs.com/dragonwell/dragonwell:21
```

**适用场景**:
- 阿里云环境
- 中国市场
- 需要阿里云技术支持

→ [阿里巴巴贡献者](/contributors/orgs/alibaba.md)

---

### Tencent Kona

腾讯提供的 JDK 发行版。

| 属性 | 值 |
|------|-----|
| **组织** | 腾讯 |
| **GitHub** | https://github.com/Tencent/TencentKona-8 |
| **许可证** | GPLv2 + CPEx |
| **商业支持** | ❌ (腾讯云支持) |
| **特性** | 容器优化，G1 GC 增强 |

**核心特性**:
- 容器资源感知优化
- G1 GC 性能增强
- 腾讯云环境优化

**版本**:
- Kona 8 (基于 JDK 8)
- Kona 11 (基于 JDK 11)
- Kona 17 (基于 JDK 17)

**安装**:
```bash
# 腾讯云
yum install tencent-kona

# Docker
docker pull ccr.ccs.tencentyun.com/qcloud/tencentkona8:latest
```

**适用场景**:
- 腾讯云环境
- 容器化部署

→ [腾讯贡献者](/contributors/orgs/tencent.md)

---

### Eclipse Temurin

Eclipse Adoptium 项目提供的免费 JDK 发行版。

| 属性 | 值 |
|------|-----|
| **组织** | Eclipse Foundation |
| **官网** | https://adoptium.net/ |
| **许可证** | GPLv2 + CPEx |
| **商业支持** | ❌ (社区支持) |
| **特性** | 完全免费，社区驱动，多平台 |

**特点**:
- 完全免费，无商业限制
- 社区驱动 (原 AdoptOpenJDK)
- 多平台支持 (Linux/Windows/macOS/AIX)
- TCK 认证

**版本**:
- Temurin 8 / 11 / 17 / 21 / 24

**安装**:
```bash
# SDKMAN
sdk install java 21-tem
sdk use java 21-tem

# Docker
docker pull eclipse-temurin:21

# Homebrew
brew install --cask temurin
```

**适用场景**:
- 开发环境
- CI/CD 环境
- 成本敏感项目
- 开源项目

---

### BellSoft Liberica

BellSoft 提供的 JDK 发行版。

| 属性 | 值 |
|------|-----|
| **组织** | BellSoft |
| **官网** | https://bell-sw.com/ |
| **许可证** | GPLv2 + CPEx (社区) / 商业 |
| **商业支持** | ✅ |
| **特性** | 轻量级，多平台，Native Image |

**版本**:
- **Liberica JDK**: 标准版
- **Liberica Lite**: 轻量版，更小体积
- **Liberica Native Image Kit**: 包含 Native Image

**特点**:
- 支持更多平台 (ARM, RISC-V, Alpine)
- Liberica Lite 体积更小
- 包含 GraalVM Native Image 功能

**安装**:
```bash
# SDKMAN
sdk install java 21-librca
sdk use java 21-librca

# Docker
docker pull bellsoft/liberica-runtime-container:jdk-21
```

**适用场景**:
- 嵌入式设备
- 容器环境
- 需要 Native Image 但不想用 GraalVM

---

### IBM Semeru

IBM 提供的 JDK 发行版，使用 OpenJ9 VM。

| 属性 | 值 |
|------|-----|
| **组织** | IBM |
| **官网** | https://developer.ibm.com/languages/java/semeru-runtimes/ |
| **许可证** | GPLv2 + CPEx (社区) / 商业 |
| **商业支持** | ✅ |
| **特性** | OpenJ9 VM，低内存占用 |

**OpenJ9 vs HotSpot**:

| 特性 | HotSpot | OpenJ9 |
|------|---------|--------|
| 内存占用 | 标准 | 低 30-50% |
| 启动时间 | 标准 | 更快 |
| 成熟度 | 高 | 中等 |
| 工具兼容 | 完全 | 大部分 |

**安装**:
```bash
# SDKMAN
sdk install java 21-sem
sdk use java 21-sem

# Docker
docker pull ibm-semeru-runtimes:open-21-jdk
```

**适用场景**:
- 内存敏感应用
- 云原生环境
- IBM Cloud 环境

---

### Microsoft Build of OpenJDK

微软提供的 JDK 发行版。

| 属性 | 值 |
|------|-----|
| **组织** | Microsoft |
| **官网** | https://learn.microsoft.com/java/openjdk/ |
| **许可证** | GPLv2 + CPEx |
| **商业支持** | ✅ (Azure 支持) |
| **特性** | Azure 优化，Windows 优化 |

**特点**:
- Azure 环境优化
- Windows 平台优化
- 包含微软安全补丁

**安装**:
```bash
# Docker
docker pull mcr.microsoft.com/openjdk/jdk:21

# Windows (winget)
winget install Microsoft.OpenJDK.21
```

**适用场景**:
- Azure 环境
- Windows 服务器
- Microsoft 技术栈

---

## 选择建议

### 按场景选择

| 场景 | 推荐发行版 | 理由 |
|------|------------|------|
| **开发环境** | Temurin, Zulu | 免费，社区支持 |
| **AWS 生产** | Corretto | AWS 优化，免费 |
| **阿里云生产** | Dragonwell | 阿里云优化 |
| **腾讯云生产** | Kona | 腾讯云优化 |
| **Azure 生产** | Microsoft Build | Azure 优化 |
| **通用生产** | Zulu, Temurin | 稳定，免费 |
| **需要商业支持** | Oracle JDK, Zulu Enterprise | 官方支持 |
| **云原生/Serverless** | GraalVM | Native Image |
| **内存敏感** | Semeru (OpenJ9) | 低内存占用 |
| **低延迟** | Zulu Prime (C4 GC) | 低延迟 GC |
| **嵌入式** | Liberica Lite | 小体积 |

### 按许可证选择

| 需求 | 推荐发行版 |
|------|------------|
| 完全免费 | Temurin, Corretto, Dragonwell, Kona |
| 免费但需商业支持 | Zulu Enterprise, Liberica |
| 可接受付费 | Oracle JDK, GraalVM Enterprise |

### 按平台选择

| 平台 | 推荐发行版 |
|------|------------|
| Linux x64 | 任意 |
| Linux ARM | Zulu, Liberica, Temurin |
| Windows | Zulu, Liberica, Microsoft Build |
| macOS | Zulu, Liberica, Temurin |
| Alpine Linux | Liberica, Zulu (musl) |
| AIX | Temurin, IBM Semeru |
| RISC-V | Liberica |

---

## 安装方式对比

### SDKMAN

```bash
# 安装 SDKMAN
curl -s "https://get.sdkman.io" | bash

# 查看可用版本
sdk list java

# 安装特定版本
sdk install java 21-tem      # Temurin
sdk install java 21-zulu     # Zulu
sdk install java 21-amzn     # Corretto
sdk install java 21-graal    # GraalVM
sdk install java 21-librca   # Liberica
sdk install java 21-sem      # Semeru (OpenJ9)
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

# Semeru (OpenJ9)
docker pull ibm-semeru-runtimes:open-21-jdk
```

### 包管理器

```bash
# Homebrew (macOS)
brew install --cask temurin    # Temurin
brew install --cask zulu       # Zulu

# apt (Ubuntu)
apt install openjdk-21-jdk     # OpenJDK

# yum (Amazon Linux)
yum install java-21-amazon-corretto  # Corretto

# winget (Windows)
winget install EclipseAdoptium.Temurin.21.JDK
winget install Microsoft.OpenJDK.21
```

---

## 版本支持周期

### LTS 版本支持

| 发行版 | JDK 8 | JDK 11 | JDK 17 | JDK 21 |
|--------|-------|--------|--------|--------|
| **Oracle JDK** | 2030 | 2026 | 2029 | 2031 |
| **Temurin** | 2026 | 2027 | 2029 | 2031 |
| **Corretto** | 2026 | 2027 | 2029 | 2032 |
| **Zulu** | 2030 | 2027 | 2029 | 2031 |
| **Dragonwell** | 2029 | 2027 | 2029 | 2031 |

---

## 性能对比

### 启动时间 (Hello World)

| 发行版 | 时间 |
|--------|------|
| OpenJDK (HotSpot) | ~100ms |
| GraalVM (JVM) | ~120ms |
| GraalVM (Native) | ~5ms |
| Semeru (OpenJ9) | ~60ms |

### 内存占用 (空闲)

| 发行版 | 内存 |
|--------|------|
| OpenJDK (HotSpot) | ~35MB |
| GraalVM (JVM) | ~45MB |
| GraalVM (Native) | ~5MB |
| Semeru (OpenJ9) | ~20MB |

---

## 迁移建议

### 从 Oracle JDK 迁移

```bash
# 1. 选择目标发行版
# 推荐: Temurin (免费) 或 Zulu (商业支持)

# 2. 安装新 JDK
sdk install java 21-tem

# 3. 验证兼容性
java -version
javac -version

# 4. 运行测试
./mvnw test

# 5. 更新 CI/CD
# 修改 Dockerfile 或构建脚本
```

### 从 JDK 8 迁移到 JDK 21

```bash
# 1. 安装 JDK 21
sdk install java 21-tem

# 2. 编译检查
javac --release 21 src/**/*.java

# 3. 处理废弃 API
# 使用 jdeprscan 检查废弃 API
jdeprscan --release 21 myapp.jar

# 4. 运行测试
./mvnw test

# 5. 性能测试
# 验证性能符合预期
```

---

## 相关链接

### 官方资源

| 发行版 | 官网 | GitHub |
|--------|------|--------|
| OpenJDK | https://openjdk.org/ | https://github.com/openjdk/jdk |
| Oracle JDK | https://www.oracle.com/java/ | - |
| GraalVM | https://www.graalvm.org/ | https://github.com/oracle/graal |
| Zulu | https://www.azul.com/ | https://github.com/azulsystems/zulu |
| Corretto | https://aws.amazon.com/corretto/ | https://github.com/corretto |
| Dragonwell | https://dragonwell-jdk.io/ | https://github.com/alibaba/dragonwell8 |
| Kona | - | https://github.com/Tencent/TencentKona-8 |
| Temurin | https://adoptium.net/ | https://github.com/adoptium |
| Liberica | https://bell-sw.com/ | https://github.com/bell-sw |
| Semeru | https://developer.ibm.com/java/ | https://github.com/ibmruntimes/semeru |

### 工具

| 工具 | 说明 |
|------|------|
| [SDKMAN](https://sdkman.io/) | Java 版本管理器 |
| [JDK Mission Control](https://jdk.java.net/jmc/) | JVM 监控工具 |
| [JProfiler](https://www.ej-technologies.com/products/jprofiler/overview.html) | 性能分析工具 |

---

## 相关主题

- [JDK 版本迁移](migration-guide.md) - 版本迁移指南
- [GraalVM](/by-topic/core/graalvm/) - GraalVM 详细文档
- [性能优化](/by-topic/core/performance/) - JVM 性能调优
