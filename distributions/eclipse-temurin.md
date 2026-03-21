# Eclipse Temurin

> Eclipse Adoptium 项目提供的免费 OpenJDK 发行版

[← 返回发行版](../distributions/)

---
## 目录

1. [概述](#1-概述)
2. [特点](#2-特点)
3. [版本支持](#3-版本支持)
4. [安装](#4-安装)
5. [性能](#5-性能)
6. [适用场景](#6-适用场景)
7. [相关链接](#7-相关链接)

---


## 1. 概述

Eclipse Temurin (原 AdoptOpenJDK) 是 Eclipse Foundation 旗下的 Adoptium 项目提供的免费 OpenJDK 发行版。

| 属性 | 值 |
|------|-----|
| **组织** | Eclipse Foundation (Adoptium) |
| **官网** | https://adoptium.net/ |
| **下载** | https://adoptium.net/temurin/releases/ |
| **许可证** | GPLv2 + Classpath Exception |
| **商业支持** | ❌ (社区支持) |
| **源码** | 基于 OpenJDK |
| **TCK 认证** | ✅ |

---

## 2. 特点

### 核心特性

- ✅ **完全免费**: 个人和商业使用免费
- ✅ **TCK 认证**: 通过 Java 技术兼容性套件
- ✅ **多平台**: Linux, Windows, macOS, AIX
- ✅ **长期支持**: LTS 版本支持 5-8 年
- ✅ **社区驱动**: 开源社区维护
- ✅ **高质量**: 严格的 QA 流程

### 历史背景

| 时间 | 事件 |
|------|------|
| 2017 | AdoptOpenJDK 成立 |
| 2021 | 迁移到 Eclipse Foundation，更名为 Adoptium |
| 2023 | 发布 Temurin 21 |

---

## 3. 版本支持

### 支持周期

| 版本 | 发布 | 支持截止 | 状态 |
|------|------|----------|------|
| Temurin 8 | - | 2026-05 | ✅ |
| Temurin 11 | - | 2027-10 | ✅ |
| Temurin 17 | - | 2029-10 | ✅ |
| Temurin 21 | 2023-09 | 2031-10 | ✅ |
| Temurin 24 | 2025-03 | 2025-09 | ✅ |

### 支持策略

- **LTS 版本**: 至少 5 年支持
- **非 LTS 版本**: 仅支持到下一版本发布
- **安全更新**: 定期发布
- **季度更新**: 每季度一次功能更新

---

## 4. 安装

### SDKMAN

```bash
# 安装 Temurin
sdk install java 21-tem
sdk use java 21-tem

# 验证
java -version
# openjdk version "21.0.1" 2023-10-17 LTS
# OpenJDK Runtime Environment Temurin-21.0.1+12 (build 21.0.1+12)
# OpenJDK 64-Bit Server VM Temurin-21.0.1+12 (build 21.0.1+12, mixed mode)
```

### Docker

```bash
# 官方镜像
docker pull eclipse-temurin:21-jdk
docker pull eclipse-temurin:21-jre
docker pull eclipse-temurin:21-alpine

# 运行
docker run -it --rm eclipse-temurin:21-jdk java -version
```

### 包管理器

```bash
# Homebrew (macOS)
brew install --cask temurin
brew install --cask temurin@8
brew install --cask temurin@11
brew install --cask temurin@17
brew install --cask temurin@21

# apt (Ubuntu - 通过 Adoptium PPA)
apt install -y wget
wget -O - https://apt.adoptium.net/adoptium.key | apt-key add -
echo "deb https://apt.adoptium.net/ all main" | tee /etc/apt/sources.list.d/adoptium.list
apt update
apt install temurin-21-jdk

# winget (Windows)
winget install EclipseAdoptium.Temurin.21.JDK
winget install EclipseAdoptium.Temurin.17.JDK
```

### 手动安装

```bash
# 下载
wget https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.1+12/OpenJDK21U-jdk_x64_linux_hotspot_21.0.1_12.tar.gz

# 解压
tar -xzf OpenJDK21U-jdk_x64_linux_hotspot_21.0.1_12.tar.gz

# 配置
export JAVA_HOME=$PWD/jdk-21.0.1+12
export PATH=$JAVA_HOME/bin:$PATH

# 验证
java -version
```

---

## 5. 性能

### 基准测试

| 指标 | Temurin 21 |
|------|------------|
| 启动时间 | ~100ms |
| 内存占用 | ~35MB |
| 吞吐量 | 100% (基准) |

### 与其他发行版对比

| 指标 | Temurin | Corretto | Zulu |
|------|---------|----------|------|
| 吞吐量 | 100% | 100% | 100% |
| 启动时间 | ~100ms | ~100ms | ~100ms |
| 内存占用 | ~35MB | ~35MB | ~35MB |

> 性能与其他基于 HotSpot 的发行版基本相同

---

## 6. 适用场景

### 推荐使用

| 场景 | 理由 |
|------|------|
| 开发环境 | 完全免费，社区支持 |
| CI/CD 环境 | 官方 Docker 镜像 |
| 开源项目 | 无商业限制 |
| 成本敏感项目 | 零成本 |
| 通用生产环境 | 稳定可靠 |

### 不推荐使用

| 场景 | 替代方案 |
|------|----------|
| 需要商业支持 | Azul Zulu Enterprise |
| 云原生部署 | GraalVM |
| 低延迟交易 | Azul Platform Prime |

---

## 7. 相关链接

### 官方资源

- [Adoptium 官网](https://adoptium.net/)
- [Temurin 发布页](https://adoptium.net/temurin/releases/)
- [Adoptium GitHub](https://github.com/adoptium)
- [Adoptium 文档](https://adoptium.net/docs/)

### 社区

- [Adoptium Discord](https://discord.gg/adoptium)
- [Adoptium Slack](https://adoptium.net/slack)

### Docker Hub

- [eclipse-temurin](https://hub.docker.com/_/eclipse-temurin)

---

**最后更新**: 2026-03-20
