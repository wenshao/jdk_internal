# JDK 发行版对比

> 主流 JDK 发行版的特点、支持策略和选择建议

[← 返回指南](../guides/)

**详细的发行版文档请访问**: [distributions/](../distributions/)

---

## 快速概览

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

## 快速对比

### 核心发行版对比

| 发行版 | 组织 | 商业支持 | 完全免费 | 特点 |
|--------|------|----------|----------|------|
| **[Oracle JDK](oracle-jdk.md)** | Oracle | ✅ | ❌ | 官方支持 |
| **[GraalVM](graalvm.md)** | Oracle Labs | ✅ | ✅ | Native Image |
| **[Zulu](azul-zulu.md)** | Azul | ✅ | ✅ | 企业级 |
| **[Prime](azul-prime.md)** | Azul | ✅ | ❌ | C4 GC 低延迟 |
| **[Temurin](eclipse-temurin.md)** | Eclipse | ❌ | ✅ | 社区标准 |
| **[Corretto](amazon-corretto.md)** | Amazon | ❌ | ✅ | AWS 优化 |
| **[Dragonwell](alibaba-dragonwell.md)** | 阿里巴巴 | ✅ | ✅ | 阿里云优化 |
| **[Kona](tencent-kona.md)** | 腾讯 | ❌ | ✅ | 腾讯云优化 |
| **[Liberica](bellsoft-liberica.md)** | BellSoft | ✅ | ✅ | 多平台 |
| **[Semeru](ibm-semeru.md)** | IBM | ✅ | ✅ | OpenJ9 低内存 |
| **[SAPMachine](sap-sapmachine.md)** | SAP | ✅ | ✅ | SAP 优化 |
| **[Microsoft Build](microsoft-openjdk.md)** | Microsoft | ✅ | ✅ | Azure 优化 |
| **[Loongson](loongson-jdk.md)** | 龙芯 | ❌ | ✅ | LoongArch 信创 |

---

## 按场景选择

### 开发环境
| 推荐发行版 | 理由 |
|------------|------|
| **Eclipse Temurin** | 完全免费，社区支持 |
| **Azul Zulu** | 免费社区版，稳定可靠 |
| **Amazon Corretto** | 免费，长期支持 |

### 云服务环境
| 云服务商 | 推荐发行版 |
|----------|------------|
| **AWS** | Amazon Corretto |
| **阿里云** | Alibaba Dragonwell |
| **腾讯云** | Tencent Kona |
| **Azure** | Microsoft Build |

### 特殊场景
| 场景 | 推荐发行版 | 理由 |
|------|------------|------|
| **云原生/Serverless** | GraalVM | Native Image |
| **低延迟交易** | Azul Platform Prime | C4 GC |
| **内存敏感** | IBM Semeru | OpenJ9 |
| **信创国产化** | Loongson JDK | LoongArch |

---

## 安装方式

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

# Microsoft Build
docker pull mcr.microsoft.com/openjdk/jdk:21
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
| **Kona** | 2025 | 2027 | 2029 | 2031 |
| **Liberica** | 2026 | 2027 | 2029 | 2031 |
| **Semeru** | 2026 | 2027 | 2029 | 2031 |
| **SAPMachine** | 2030 | 2027 | 2029 | 2031 |
| **Microsoft Build** | 2026 | 2027 | 2029 | 2031 |
| **Loongson** | 2026 | 2027 | 2029 | 2031 |

---

## 性能对比

### 启动时间 (Hello World)

| 发行版 | JVM | 启动时间 |
|--------|-----|----------|
| HotSpot (标准) | HotSpot | ~100ms |
| GraalVM | Graal JIT | ~120ms |
| GraalVM Native | - | ~5ms |
| OpenJ9 | OpenJ9 | ~60ms |

### 内存占用 (空闲应用)

| 发行版 | JVM | 内存占用 |
|--------|-----|----------|
| HotSpot (标准) | HotSpot | ~35MB |
| GraalVM | Graal JIT | ~45MB |
| GraalVM Native | - | ~5MB |
| OpenJ9 | OpenJ9 | ~20MB |

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
| Temurin | https://adoptium.net/ | https://github.com/adoptium |
| Liberica | https://bell-sw.com/ | https://github.com/bell-sw |
| Semeru | https://developer.ibm.com/java/ | https://github.com/ibmruntimes/semeru |
| Microsoft Build | https://learn.microsoft.com/java/openjdk/ | https://github.com/microsoft/openjdk-build |
| Loongson | https://www.loongnix.cn/ | https://github.com/loongson/jdk |

### 工具

| 工具 | 说明 |
|------|------|
| [SDKMAN](https://sdkman.io/) | Java 版本管理器 |
| [JDK Mission Control](https://jdk.java.net/jmc/) | JVM 监控工具 |
| [WhichJDK](https://whichjdk.com/) | JDK 选择建议 |
| [JDK Comparison](https://jdkcomparison.com/) | JDK 对比工具 |

---

## 详细文档

每个发行版的详细文档请访问:

- [Oracle JDK](../distributions/oracle-jdk.md) - Oracle 官方 JDK
- [GraalVM](../distributions/graalvm.md) - Native Image 和多语言
- [Azul Zulu](../distributions/azul-zulu.md) - Azul 社区版
- [Azul Prime](../distributions/azul-prime.md) - C4 GC 低延迟版
- [Eclipse Temurin](../distributions/eclipse-temurin.md) - Eclipse 社区版
- [Amazon Corretto](../distributions/amazon-corretto.md) - AWS 优化版
- [Alibaba Dragonwell](../distributions/alibaba-dragonwell.md) - 阿里云优化版
- [Tencent Kona](../distributions/tencent-kona.md) - 腾讯云优化版
- [BellSoft Liberica](../distributions/bellsoft-liberica.md) - 多平台版
- [IBM Semeru](../distributions/ibm-semeru.md) - OpenJ9 低内存版
- [SAPMachine](../distributions/sap-sapmachine.md) - SAP 优化版
- [Microsoft Build](../distributions/microsoft-openjdk.md) - Azure 优化版
- [Loongson JDK](../distributions/loongson-jdk.md) - 龙芯信创版

---

## 相关主题

- [JDK 版本迁移](migration-guide.md) - 版本迁移指南
- [GraalVM](../by-topic/core/graalvm/) - GraalVM 详细文档
- [性能优化](../by-topic/core/performance/) - JVM 性能调优

---

**最后更新**: 2026-03-20

**Sources**:
- [WhichJDK.com](https://whichjdk.com/)
- [JDKComparison.com](https://jdkcomparison.com/)
- [2024 State of Java Ecosystem](https://newrelic.com/resources/report/2024-state-of-the-java-ecosystem)
