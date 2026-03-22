# JDK 发行版对比指南

> 10 大主流 JDK 发行版详细对比，帮助你做出明智的选择。

---
## 目录

1. [概览对比表](#1-概览对比表)
2. [各发行版详情](#2-各发行版详情)
3. [选择决策树](#3-选择决策树)
4. [LTS 支持周期对比](#4-lts-支持周期对比)
5. [平台覆盖对比](#5-平台覆盖对比)
6. [许可证详解](#6-许可证详解)
7. [安装方式](#7-安装方式)
8. [常见问题](#8-常见问题)

---


## 1. 概览对比表

### 核心对比

| 发行版 | 维护方 | 免费商用 | 商业支持 | VM 引擎 | 特色功能 |
|--------|--------|---------|---------|---------|---------|
| **Oracle JDK** | Oracle | 有条件 | 付费 | HotSpot | Java SE 参考实现 |
| **OpenJDK** (上游) | OpenJDK 社区 | 是 | 无 | HotSpot | 源代码基准 |
| **Eclipse Temurin** | Eclipse Adoptium | 是 | 可选 (第三方) | HotSpot | 社区标准，AQAvit 测试 |
| **Amazon Corretto** | Amazon | 是 | AWS 内含 | HotSpot | AWS 优化，长 LTS |
| **Azul Zulu** | Azul Systems | 社区版免费 | Enterprise 付费 | HotSpot | 最广泛 LTS 支持 |
| **BellSoft Liberica** | BellSoft | 是 | 付费 | HotSpot | Alpine/musl, 嵌入式 |
| **SAP SapMachine** | SAP | 是 | SAP 客户 | HotSpot | SAP 平台优化 |
| **Red Hat build** | Red Hat | RHEL 订阅含 | RHEL 含 | HotSpot | RHEL/OpenShift 集成 |
| **Microsoft Build** | Microsoft | 是 | Azure 内含 | HotSpot | Windows/Azure 优化 |
| **Alibaba Dragonwell** | 阿里巴巴 | 是 | 阿里云内含 | HotSpot | JWarmUp, Wisp 协程 |

### 许可证一览

| 发行版 | 许可证 | 含义 |
|--------|--------|------|
| Oracle JDK | **OTN** (商业) / **NFTC** (免费) | NFTC: 个人和开发免费，生产可用但无支持；OTN: 需要付费订阅 |
| OpenJDK | **GPLv2 + CE** | 完全自由使用，含 Classpath Exception |
| Temurin | **GPLv2 + CE** | 同 OpenJDK |
| Corretto | **GPLv2 + CE** | 同 OpenJDK |
| Zulu | **GPLv2 + CE** (社区版) | 企业版另有商业协议 |
| Liberica | **GPLv2 + CE** | 同 OpenJDK |
| SapMachine | **GPLv2 + CE** | 同 OpenJDK |
| Red Hat build | **GPLv2 + CE** | 二进制通过 RHEL 订阅分发 |
| Microsoft Build | **GPLv2 + CE** | 同 OpenJDK |
| Dragonwell | **GPLv2 + CE** | 同 OpenJDK |

---

## 2. 各发行版详情

### Oracle JDK

```
维护方:    Oracle
官网:      https://www.oracle.com/java/
许可证:    OTN License (付费) / NFTC License (免费)
VM 引擎:   HotSpot
```

**定位**: Java SE 参考实现 (Reference Implementation)，Oracle 官方支持。

**特点**:
- 与 OpenJDK **源代码基本相同** (JDK 11 起)
- Oracle 独有: Java Management Service (JMS)、GraalVM Enterprise 集成
- 季度 CPU (Critical Patch Update) 安全更新
- 商业支持需要 Java SE Subscription ($25/处理器/月 起)

**适用场景**: 需要 Oracle 官方支持和 SLA 的企业客户。

**许可证变迁**:
| 时期 | 许可证 | 免费情况 |
|------|--------|---------|
| JDK 8 (8u211 前) | BCL | 免费商用 |
| JDK 8 (8u211 后) | OTN | 商用需付费 |
| JDK 17-24 | NFTC | 免费 (含生产) |
| JDK 25+ | NFTC + OTN | NFTC 免费，OTN 付费 |

---

### OpenJDK (上游源码)

```
维护方:    OpenJDK 社区 (Oracle 主导)
官网:      https://openjdk.org/
下载:      https://jdk.java.net/
许可证:    GPLv2 + Classpath Exception
VM 引擎:   HotSpot
```

**定位**: 所有发行版的**源代码基准**。

**特点**:
- Oracle 工程师贡献约 80% 的代码
- jdk.java.net 提供二进制下载，但**仅当前版本**有更新
- 非 LTS 版本在下一版本发布后停止更新
- 不提供官方商业支持

**适用场景**: 开发测试、体验最新版本。生产环境建议使用下游发行版 (如 Temurin)。

---

### Eclipse Temurin (Adoptium)

```
维护方:    Eclipse Adoptium 工作组
官网:      https://adoptium.net/
许可证:    GPLv2 + Classpath Exception
VM 引擎:   HotSpot
```

**定位**: 社区标准 OpenJDK 发行版，**最推荐的通用选择**。

**特点**:
- 前身是 AdoptOpenJDK (2021 年迁入 Eclipse 基金会)
- **AQAvit** 质量保证套件: 超过 OpenJDK 官方测试范围
- 多平台: Linux (x64/aarch64/s390x/ppc64le), macOS (x64/aarch64), Windows (x64), Alpine (musl)
- LTS 版本更新跟随 Oracle CPU 节奏
- 工作组成员: Microsoft, Red Hat, IBM, Azul, Alibaba 等

**适用场景**: 大多数场景的**默认选择**。无需特殊理由时，选 Temurin。

---

### Amazon Corretto

```
维护方:    Amazon
官网:      https://aws.amazon.com/corretto/
许可证:    GPLv2 + Classpath Exception
VM 引擎:   HotSpot
```

**定位**: AWS 优化的 OpenJDK 发行版。

**特点**:
- Amazon 内部大规模生产使用 (AWS 服务本身运行在 Corretto 上)
- **超长 LTS**: JDK 8 支持到 2026+, JDK 11 到 2027+, JDK 17 到 2029+, JDK 21 到 2032+
- 包含 Amazon 自研补丁 (已上游化或计划上游化)
- AWS Lambda, ECS, EKS 原生支持
- Alpine Linux 支持

**适用场景**: AWS 用户的首选。即使不在 AWS 上也是优质选择 (因为超长 LTS)。

---

### Azul Zulu / Azul Platform Prime

```
维护方:    Azul Systems
官网:      https://www.azul.com/
许可证:    GPLv2 + CE (Zulu 社区版) / 商业 (Prime)
VM 引擎:   HotSpot (Zulu) / Zing (Prime)
```

**Zulu (社区版)**:
- 免费，覆盖最多的 JDK 版本 (JDK 6-25+)
- 支持 JDK 7, 8, 11, 13, 15, 17, 21 的 LTS (商业版)
- 多平台: 包括 ARM 32-bit, Solaris

**Platform Prime (商业版)**:
- 使用 **C4 GC** (Continuously Concurrent Compacting Collector)
- 暂停时间 < 1ms，与堆大小无关
- **ReadyNow**: AOT 编译 + 即时预热
- 最强无暂停 GC 方案

**适用场景**: Zulu 适合通用生产；Prime 适合低延迟交易系统、金融系统。

---

### BellSoft Liberica

```
维护方:    BellSoft
官网:      https://bell-sw.com/
许可证:    GPLv2 + Classpath Exception
VM 引擎:   HotSpot
```

**特点**:
- **最广泛的平台支持**: 包括 Alpine Linux (musl), ARM 32/64, RISC-V, Solaris
- **Liberica Lite**: 精简版，适合嵌入式和 IoT
- **Liberica Native Image Kit (NIK)**: 基于 GraalVM 的 Native Image
- Spring Boot 官方推荐的构建包 (Buildpacks) 使用 Liberica
- Docker 镜像体积小 (Alpine 基础)

**适用场景**: 需要 Alpine/musl 支持、嵌入式设备、或 Spring Boot 云部署。

---

### SAP SapMachine

```
维护方:    SAP
官网:      https://sapmachine.io/
许可证:    GPLv2 + Classpath Exception
VM 引擎:   HotSpot
```

**特点**:
- SAP 内部生产使用
- SAP HANA, S/4HANA, Business Technology Platform 优化
- 包含 SAP 自研的诊断和性能补丁
- 与 OpenJDK 上游保持紧密同步

**适用场景**: SAP 生态系统用户。

---

### Red Hat build of OpenJDK

```
维护方:    Red Hat (IBM)
官网:      https://developers.redhat.com/products/openjdk/
许可证:    GPLv2 + Classpath Exception
VM 引擎:   HotSpot
```

**特点**:
- 通过 **RHEL / CentOS Stream** 订阅分发
- OpenShift 容器平台原生集成
- Red Hat 是 OpenJDK 社区的**第二大代码贡献者** (仅次于 Oracle)
- Shenandoah GC 的主要开发者和维护者
- Windows 版本也可免费下载

**适用场景**: RHEL 用户、OpenShift 用户。

---

### Microsoft Build of OpenJDK

```
维护方:    Microsoft
官网:      https://www.microsoft.com/openjdk
许可证:    GPLv2 + Classpath Exception
VM 引擎:   HotSpot
```

**特点**:
- Azure 服务 (App Service, Functions, Spring Apps) 原生支持
- Windows ARM64 优化
- macOS aarch64 支持
- Microsoft 是 OpenJDK 和 Adoptium 的活跃贡献者

**适用场景**: Azure 用户、Windows 开发者。

---

### Alibaba Dragonwell

```
维护方:    阿里巴巴
官网:      https://dragonwell-jdk.io/
GitHub:    https://github.com/dragonwell-project
许可证:    GPLv2 + Classpath Exception
VM 引擎:   HotSpot
```

**特点**:
- **JWarmUp**: 记录 JIT 编译数据，下次启动时直接使用，启动预热加速
- **Wisp**: 协程实现 (类似虚拟线程的先行探索)
- **ElasticHeap**: 动态调整堆大小，适合容器化部署
- **多租户 GC**: 隔离不同租户的 GC 影响
- 阿里巴巴双十一核心系统大规模验证
- 阿里云 ECS/ACK 原生支持

**适用场景**: 阿里云用户、需要 JWarmUp 等特性的场景、信创需求。

---

## 3. 选择决策树

```
开始: 你的部署环境是什么？
│
├─ AWS (EC2, ECS, Lambda, EKS)
│   └─ → Amazon Corretto
│
├─ Azure (App Service, AKS, Functions)
│   └─ → Microsoft Build of OpenJDK
│
├─ 阿里云 (ECS, ACK, 函数计算)
│   └─ → Alibaba Dragonwell
│
├─ RHEL / OpenShift
│   └─ → Red Hat build of OpenJDK
│
├─ SAP 平台
│   └─ → SapMachine
│
├─ 不绑定云厂商
│   │
│   ├─ 需要商业支持？
│   │   ├─ 是 + 需要超低延迟 GC → Azul Platform Prime
│   │   ├─ 是 + Oracle 品牌 → Oracle JDK
│   │   └─ 是 + 灵活选择 → Azul Zulu Enterprise
│   │
│   ├─ 需要最小镜像 / Alpine？
│   │   └─ → BellSoft Liberica
│   │
│   ├─ 需要嵌入式 / IoT？
│   │   └─ → BellSoft Liberica Lite
│   │
│   └─ 通用需求
│       └─ → Eclipse Temurin (推荐默认选择)
│
├─ 信创 / 龙芯
│   └─ → Loongson JDK / Alibaba Dragonwell
│
└─ 特殊场景
    ├─ 需要 Native Image → GraalVM Community / Liberica NIK
    └─ 需要低内存 (OpenJ9) → IBM Semeru
```

---

## 4. LTS 支持周期对比

### JDK 8

| 发行版 | 免费更新截止 | 商业支持截止 |
|--------|-------------|-------------|
| Oracle JDK | 已结束 (2019-03) | 2030-12 (Extended) |
| Corretto | 2026-06 | - |
| Zulu | 2030-12 (Enterprise) | 2030-12 |
| Temurin | 2026-11 | - |
| Dragonwell | 2029-06 | - |

### JDK 11

| 发行版 | 免费更新截止 | 商业支持截止 |
|--------|-------------|-------------|
| Oracle JDK | 已结束 (2023-09) | 2032-01 (Extended) |
| Corretto | 2027-09 | - |
| Zulu | 2032-01 (Enterprise) | 2032-01 |
| Temurin | 2027-10 | - |
| Dragonwell | 2029-10 | - |

### JDK 17

| 发行版 | 免费更新截止 | 商业支持截止 |
|--------|-------------|-------------|
| Oracle JDK | 2029-09 (NFTC) | 2029-09 (Premier) |
| Corretto | 2029-10 | - |
| Zulu | 2029-10 | 2030+ (Enterprise) |
| Temurin | 2029-10 | - |
| Dragonwell | 2029-10 | - |
| Liberica | 2029-10 | 2030+ |

### JDK 21

| 发行版 | 免费更新截止 | 商业支持截止 |
|--------|-------------|-------------|
| Oracle JDK | 2031-09 (NFTC) | 2031-09 (Premier) |
| Corretto | 2032-04 | - |
| Zulu | 2031-10 | 2032+ (Enterprise) |
| Temurin | 2031-10 | - |
| Dragonwell | 2031-10 | - |
| Liberica | 2031-10 | 2032+ |

### JDK 25 (最新 LTS)

| 发行版 | 免费更新截止 (预计) |
|--------|-------------------|
| Oracle JDK | 2033-09 |
| Corretto | 2034+ |
| Zulu | 2033-10 |
| Temurin | 2033-10 |
| Dragonwell | 2033-10 |

---

## 5. 平台覆盖对比

### 操作系统 + 架构

| 平台 | Oracle | Temurin | Corretto | Zulu | Liberica | Dragonwell | Microsoft |
|------|--------|---------|----------|------|----------|------------|-----------|
| Linux x86_64 | Y | Y | Y | Y | Y | Y | Y |
| Linux aarch64 | Y | Y | Y | Y | Y | Y | Y |
| Linux ARM 32 | - | - | - | Y | Y | - | - |
| Linux s390x | - | Y | - | Y | Y | - | - |
| Linux ppc64le | - | Y | - | Y | Y | - | - |
| Linux riscv64 | Y | - | - | - | Y | - | - |
| Alpine (musl) | - | Y | Y | Y | Y | Y | Y |
| macOS x86_64 | Y | Y | Y | Y | Y | - | Y |
| macOS aarch64 | Y | Y | Y | Y | Y | - | Y |
| Windows x86_64 | Y | Y | Y | Y | Y | Y | Y |
| Windows aarch64 | Y | - | - | Y | Y | - | Y |

### 容器镜像大小对比 (JDK 21, 近似值)

| 镜像 | 大小 |
|------|------|
| `eclipse-temurin:21-jdk` (Ubuntu) | ~340MB |
| `eclipse-temurin:21-jre` (Ubuntu) | ~200MB |
| `eclipse-temurin:21-jre-alpine` | ~100MB |
| `amazoncorretto:21-alpine` | ~110MB |
| `bellsoft/liberica-openjdk-alpine:21` | ~95MB |
| `azul/zulu-openjdk-alpine:21` | ~100MB |

---

## 6. 许可证详解

### GPLv2 + Classpath Exception (GPLv2+CE)

绝大多数 OpenJDK 发行版使用此许可证。

**含义**:
- JDK 本身是 GPL 许可
- **Classpath Exception**: 你的应用链接 JDK 标准库时**不需要 GPL 传染**
- 可以自由地在商业闭源软件中使用
- 可以重新分发 (需保留许可证声明)

**简单说**: 像用 GCC 编译你的代码一样，你的代码不受 GPL 约束。

### Oracle 许可证

**NFTC (No-Fee Terms and Conditions)**:
- JDK 17+ 可用
- 免费用于开发、测试、生产
- 无商业支持
- Oracle 可以在新版本发布后停止旧版本更新

**OTN (Oracle Technology Network)**:
- 需要 Java SE Subscription
- 包含 Oracle 商业支持
- 定价: ~$25/处理器/月 (企业) 或 ~$15/用户/月 (桌面)

### 重要提醒

> **Oracle JDK 8** (8u211+) 商业使用需要付费许可证。如果你还在生产环境免费使用 Oracle JDK 8，请尽快迁移到 Temurin/Corretto 等免费发行版，或购买 Oracle 订阅。

---

## 7. 安装方式

### SDKMAN (推荐, Linux/macOS)

```bash
# 安装 SDKMAN
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"

# 查看所有可用发行版
sdk list java

# 安装
sdk install java 25-tem        # Eclipse Temurin
sdk install java 25-amzn       # Amazon Corretto
sdk install java 25-zulu       # Azul Zulu
sdk install java 25-librca     # BellSoft Liberica
sdk install java 25-sapmchn    # SapMachine
sdk install java 25-ms         # Microsoft
sdk install java 25-oracle     # Oracle JDK

# 版本切换
sdk use java 25-tem            # 当前 shell
sdk default java 25-tem        # 全局默认

# 项目级别
echo "java=25-tem" > .sdkmanrc
sdk env                        # 自动切换
```

### Docker

```bash
# Eclipse Temurin
docker pull eclipse-temurin:25-jdk
docker pull eclipse-temurin:25-jre-alpine

# Amazon Corretto
docker pull amazoncorretto:25
docker pull amazoncorretto:25-alpine

# Azul Zulu
docker pull azul/zulu-openjdk:25
docker pull azul/zulu-openjdk-alpine:25

# BellSoft Liberica
docker pull bellsoft/liberica-openjdk-alpine:25

# Microsoft
docker pull mcr.microsoft.com/openjdk/jdk:25-ubuntu

# SapMachine
docker pull sapmachine/jdk:25
```

### 包管理器

```bash
# macOS (Homebrew)
brew install --cask temurin         # Temurin (推荐)
brew install --cask corretto        # Corretto
brew install --cask zulu            # Zulu

# Ubuntu / Debian
sudo apt install openjdk-25-jdk    # Ubuntu 默认 OpenJDK

# 或添加 Adoptium 仓库
wget -qO - https://packages.adoptium.net/artifactory/api/gpg/key/public | sudo apt-key add -
sudo add-apt-repository "deb https://packages.adoptium.net/artifactory/deb $(lsb_release -cs) main"
sudo apt install temurin-25-jdk

# RHEL / Fedora
sudo dnf install java-25-openjdk-devel

# Windows (winget)
winget install EclipseAdoptium.Temurin.25.JDK
winget install Amazon.Corretto.25
winget install Azul.Zulu.25.JDK
```

---

## 8. 常见问题

### Q: 切换发行版需要重新编译应用吗？

**不需要** (同一 JDK 大版本内)。所有基于 HotSpot 的发行版生成和运行相同的字节码。唯一例外是 IBM Semeru (OpenJ9)，其 JVM 参数不完全兼容。

### Q: 不同发行版性能有差异吗？

基于 HotSpot 的发行版**性能几乎相同**，因为核心 JIT 编译器和 GC 代码相同。差异来自：
- 各发行版的自研补丁 (通常影响 < 5%)
- Azul Platform Prime 的 C4 GC 在低延迟场景有显著优势
- IBM Semeru (OpenJ9) 在内存占用上有优势，但吞吐量可能较低

### Q: 发行版会"跑路"吗？

开源发行版基于 GPLv2+CE，即使维护方停止维护：
- 源代码永远可用
- 社区可以 fork 继续维护
- 你可以自行构建

降低风险的策略：选择由大型组织 (Eclipse, Amazon, Microsoft, Alibaba) 维护、并且有 Adoptium 工作组成员身份的发行版。

### Q: GraalVM 和普通 JDK 是什么关系？

GraalVM 有两种使用方式：

| 方式 | 说明 | 场景 |
|------|------|------|
| GraalVM JDK | 带 Graal JIT 的 HotSpot JDK | 替代普通 JDK |
| Native Image | AOT 编译为原生二进制 | Serverless/CLI |

GraalVM Community 基于 OpenJDK，Oracle GraalVM 包含额外优化。

### Q: 中国企业应该选哪个发行版？

```
├─ 阿里云 → Alibaba Dragonwell (首选)
├─ 腾讯云 → Tencent Kona
├─ 华为云 → 毕昇 JDK (BiSheng JDK)
├─ 信创 / 龙芯 → Loongson JDK + Dragonwell
├─ 无特定云 → Eclipse Temurin (国际标准) 或 Dragonwell (中文社区)
└─ 需要商业支持 → Oracle JDK 或 Azul Zulu Enterprise
```

---

**最后更新**: 2026-03-22

**相关资源**:
- [FAQ](faq.md) — 常见问题
- [学习路径](learning-path.md) — 按角色推荐的学习路线
- [迁移指南](migration-guide.md) — JDK 版本升级详细步骤
- [SDKMAN](https://sdkman.io/) — Java 版本管理器
- [WhichJDK](https://whichjdk.com/) — JDK 选择建议
- [Adoptium](https://adoptium.net/) — Eclipse Temurin 官网
