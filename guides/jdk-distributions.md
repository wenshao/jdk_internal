# JDK 发行版快速选择指南

> 30 秒选择最适合你的 JDK 发行版

[← 返回指南](../guides/)
[→ 详细对比](../distributions/)

---
## 目录

1. [快速决策树](#1-快速决策树)
2. [场景化推荐](#2-场景化推荐)
3. [一行安装命令](#3-一行安装命令)
4. [支持周期速查](#4-支持周期速查)
5. [许可证速查](#5-许可证速查)
6. [相关链接](#6-相关链接)
7. [常见问题](#7-常见问题)

---


## 1. 快速决策树

```
开始
  │
  ├─ 生产环境 (商业支持)
  │    ├─ AWS 部署       → Amazon Corretto
  │    ├─ 阿里云部署     → Alibaba Dragonwell
  │    ├─ 腾讯云部署     → Tencent Kona
  │    ├─ Azure 部署     → Microsoft Build of OpenJDK
  │    ├─ 低延迟交易     → Azul Platform Prime
  │    ├─ 内存敏感       → IBM Semeru (OpenJ9)
  │    └─ 通用企业       → Oracle JDK / Azul Zulu Enterprise
  │
  ├─ 开发/测试 (免费优先)
  │    ├─ 社区标准       → Eclipse Temurin
  │    ├─ 个人项目       → Azul Zulu (免费)
  │    └─ 学习探索       → 任意免费发行版
  │
  ├─ 云原生/Serverless
  │    └─ 快速启动       → GraalVM Native Image
  │
  └─ 特殊需求
       ├─ 信创国产化     → Loongson JDK / Dragonwell
       ├─ 嵌入式设备     → BellSoft Liberica Lite
       └─ 多语言运行     → GraalVM Polyglot
```

---

## 2. 场景化推荐

### 🏢 企业生产环境

| 场景 | 推荐发行版 | 核心理由 |
|------|-----------|---------|
| 通用生产 | **Eclipse Temurin** | 免费社区标准，多平台支持 |
| AWS 云 | **Amazon Corretto** | AWS 优化，免费长期支持 |
| 阿里云 | **Alibaba Dragonwell** | 阿里云优化，JWarmUp |
| 腾讯云 | **Tencent Kona** | 腾讯云优化，容器优化 |
| Azure | **Microsoft Build** | Windows 优化，Azure 集成 |
| 低延迟交易 | **Azul Platform Prime** | C4 GC，pause < 1ms |
| 内存受限 | **IBM Semeru** | OpenJ9，内存占用 -40% |

### 💻 开发环境

| 需求 | 推荐发行版 |
|------|-----------|
| 默认选择 | **Eclipse Temurin** |
| macOS 开发 | **Azul Zulu** |
| Windows 开发 | **Microsoft Build of OpenJDK** |
| 多版本管理 | 使用 SDKMAN |

### 🚀 云原生/微服务

| 需求 | 推荐发行版 |
|------|-----------|
| 快速启动 | **GraalVM Native Image** |
| 小镜像 | **Amazon Corretto** / **Eclipse Temurin** (Alpine) |
| 低内存 | **IBM Semeru** |

### 🇨🇳 信创国产化

| 需求 | 推荐发行版 |
|------|-----------|
| 龙芯 CPU | **Loongson JDK** |
| 国产通用 | **Dragonwell** / **Kona** |

---

## 3. 一行安装命令

### SDKMAN (推荐 Linux/macOS)

```bash
# 安装 SDKMAN
curl -s "https://get.sdkman.io" | bash && source "$HOME/.sdkman/bin/sdkman-init.sh"

# 根据场景安装
sdk install java 21-tem      # 社区标准
sdk install java 21-amzn     # AWS 优化
sdk install java 21-graal    # Native Image
```

### Docker

```bash
# 通用
docker pull eclipse-temurin:21-jdk

# AWS
docker pull amazoncorretto:21

# Azure
docker pull mcr.microsoft.com/openjdk/jdk:21

# GraalVM
docker pull ghcr.io/graalvm/native-image-community:21
```

### 包管理器

```bash
# macOS
brew install --cask temurin

# Ubuntu/Debian
apt install openjdk-21-jdk

# Windows
winget install EclipseAdoptium.Temurin.21.JDK
```

---

## 4. 支持周期速查

### LTS 版本 (2026 年后仍受支持)

| 发行版 | JDK 17 | JDK 21 |
|--------|--------|--------|
| Temurin | 2029-10 | 2031-10 |
| Corretto | 2029-09 | 2032-04 |
| Zulu | 2029-10 | 2031-10 |
| Dragonwell | 2029-10 | 2031-10 |
| Kona | 2029-10 | 2031-10 |

> 💡 **建议**: 新项目使用 JDK 21 LTS

---

## 5. 许可证速查

| 许可证 | 含义 | 代表发行版 |
|--------|------|-----------|
| **GPLv2 + CPEx** | 完全免费 (含商业) | Temurin, Corretto, Zulu, Kona, Liberica |
| **OTNLA** | 个人免费，商业付费 | Oracle JDK |
| **GFTC** | 生产免费 (不含支持) | GraalVM Community |

---

## 6. 相关链接

### 详细文档

- [完整发行版对比](../distributions/) - 所有发行版详细对比
- [Oracle JDK](../distributions/oracle-jdk.md) - Oracle 官方 JDK
- [GraalVM](../distributions/graalvm.md) - Native Image 详解
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

### 工具

- [SDKMAN](https://sdkman.io/) - Java 版本管理器
- [WhichJDK](https://whichjdk.com/) - JDK 选择建议
- [JDK Comparison](https://jdkcomparison.com/) - JDK 对比工具

---

## 7. 常见问题

**Q: Oracle JDK 和 OpenJDK 有什么区别？**

A: Oracle JDK 基于 OpenJDK，增加了商业支持。对于大多数场景，免费的 OpenJDK 发行版（如 Temurin）完全够用。

**Q: 哪个发行版最快？**

A: 所有基于 HotSpot 的发行版性能相近。特殊场景：
- 低延迟 → Azul Platform Prime (C4 GC)
- 低内存 → IBM Semeru (OpenJ9)
- 快速启动 → GraalVM Native Image

**Q: 可以在生产环境免费使用吗？**

A: Temurin、Corretto、Zulu 社区版等都可以免费商用。Oracle JDK 商业使用需要付费订阅。

---

**最后更新**: 2026-03-20

**相关主题**:
- [JDK 版本迁移](migration-guide.md)
- [性能优化](../by-topic/core/performance/)
- [GraalVM](../by-topic/core/graalvm/)
