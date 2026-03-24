# Azul Zulu

> Azul Systems 提供的商业 OpenJDK 发行版

[← 返回发行版](../distributions/)

---
## 目录

1. [概述](#1-概述)
2. [版本类型](#2-版本类型)
3. [版本支持](#3-版本支持)
4. [安装](#4-安装)
5. [适用场景](#5-适用场景)
6. [相关链接](#6-相关链接)

---


## 1. 概述

Azul Zulu 是 Azul Systems 提供的免费和企业级 OpenJDK 发行版，以稳定性和多平台支持著称。

| 属性 | 值 |
|------|-----|
| **组织** | Azul Systems |
| **官网** | https://www.azul.com/downloads/ |
| **下载** | https://www.azul.com/downloads/zulu/ |
| **许可证** | GPLv2 + CPEx (社区) / 商业 |
| **商业支持** | ✅ |
| **源码** | 基于 OpenJDK |

---

## 2. 版本类型

### Zulu Community

- ✅ **完全免费**: 个人和商业使用免费
- ✅ **多平台**: Linux, Windows, macOS, ARM
- ✅ **TCK 认证**: 通过 Java 兼容性测试
- ❌ **无商业支持**: 仅社区支持

### Zulu Enterprise

- ✅ **商业支持**: 24/7 技术支持
- ✅ **长期支持**: 延长支持周期
- ✅ **安全更新**: 优先安全补丁
- ✅ **合规认证**: 符合行业合规要求

### Azul Platform Prime

- ✅ **C4 GC**: 低延迟垃圾回收
- ✅ **高性能**: 吞吐量优化
- ✅ **大堆内存**: 支持 TB 级堆
- ✅ **高级监控**: Azul Platform Cloud

---

## 3. 版本支持

### 支持周期

| 版本 | Community | Enterprise |
|------|-----------|------------|
| Zulu 8 | 2030-12 | 2030-12+ |
| Zulu 11 | 2027-10 | 2030+ |
| Zulu 17 | 2029-10 | 2032+ |
| Zulu 21 | 2031-10 | 2034+ |

---

## 4. 安装

### SDKMAN

```bash
# 安装 Zulu
sdk install java 21-zulu
sdk use java 21-zulu

# 验证
java -version
# openjdk version "21.0.1" 2023-10-17 LTS
# OpenJDK Runtime Environment Azul Zulu Builds (build 21.0.1+12-LTS)
# OpenJDK 64-Bit Server VM Azul Zulu Builds (build 21.0.1+12-LTS, mixed mode)
```

### Docker

```bash
# 社区版
docker pull azul/zulu-openjdk:21
docker pull azul/zulu-openjdk:21-alpine
docker pull azul/zulu-openjdk:21-jre

# 运行
docker run -it --rm azul/zulu-openjdk:21 java -version
```

### 包管理器

```bash
# Homebrew (macOS)
brew install --cask zulu
brew install --cask zulu@17
brew install --cask zulu@11

# apt (通过 Azul APT 仓库)
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0xB1998361219BD9C9
apt install software-properties-common
apt-add-repository 'deb https://repos.azul.com/zing-only stable main'
apt update
apt install zulu-21-jdk
```

---

## 5. 适用场景

### 推荐使用

| 场景 | 版本 | 理由 |
|------|------|------|
| 开发环境 | Community | 免费，多平台 |
| 企业生产 | Enterprise | 商业支持 |
| 低延迟交易 | Prime | C4 GC |
| 大内存应用 | Prime | TB 级堆支持 |
| Windows 服务 | Enterprise | Windows 优化 |
| ARM 平台 | Community | ARM64 支持 |

### 不推荐使用

| 场景 | 替代方案 |
|------|----------|
| 成本敏感 | Eclipse Temurin |

---

## 6. 上游维护团队

Azul 的上游贡献主要集中在 **CRaC (Coordinated Restore at Checkpoint)** 实验性项目，主线直接贡献较少。

| 维度 | PRs | 说明 |
|------|-----|------|
| **CRaC 项目** | **251** (81%) | Azul 主导的检查点恢复项目 |
| **主线** | 18 | Anton Kozlov (CRaC Runtime) |
| **LTS 维护** | 4 | jdk17u/11u 少量 |
| **总计** | **273** | |

核心贡献者:
- **TimPushkin** — 75 CRaC PRs
- **[AntonKozlov](../by-contributor/profiles/anton-kozlov.md)** — 18 主线 PRs + CRaC 核心
- **rvansa** — 63 CRaC PRs
- **jankratochvil** — 36 CRaC PRs

> 详情: [Azul 组织页面](../contributors/orgs/azul.md)

---

## 7. 相关链接

### 官方资源

- [Azul 官网](https://www.azul.com/)
- [Zulu 下载](https://www.azul.com/downloads/zulu/)
- [Azul 文档](https://docs.azul.com/)

---

**最后更新**: 2026-03-20
