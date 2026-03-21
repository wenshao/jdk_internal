# Oracle JDK

> Oracle 官方 JDK 发行版

[← 返回发行版](../distributions/)

---
## 目录

1. [概述](#1-概述)
2. [许可证](#2-许可证)
3. [版本支持](#3-版本支持)
4. [特性](#4-特性)
5. [安装](#5-安装)
6. [性能](#6-性能)
7. [适用场景](#7-适用场景)
8. [迁移](#8-迁移)
9. [相关链接](#9-相关链接)

---


## 1. 概述

Oracle JDK 是 Oracle 公司官方维护的 Java Development Kit，基于 OpenJDK 构建，提供商业支持和额外功能。

| 属性 | 值 |
|------|-----|
| **组织** | Oracle |
| **官网** | https://www.oracle.com/java/ |
| **下载** | https://www.oracle.com/java/technologies/downloads/ |
| **许可证** | OTNLA (商业) / GPLv2 (个人) |
| **商业支持** | ✅ |
| **源码** | 基于 OpenJDK |

---

## 2. 许可证

### NFTC (No-Fee Terms and Conditions) - JDK 17+

自 JDK 17 起，Oracle JDK 使用 NFTC 许可证：
- **个人使用**: 免费
- **商业使用**: 免费
- **生产使用**: 免费
- **分发**: 允许

### OTNLA (Oracle Technology Network License Agreement) - JDK 8, 11

- **个人使用**: 免费
- **商业使用**: 需要 Oracle Java SE Subscription
- **生产使用**: 需要 Subscription

### Oracle Java SE Subscription

| 版本 | 年度订阅 (每处理器) | 年度订阅 (每用户) |
|------|---------------------|-------------------|
| Java SE | $300 | $150 |
| Java SE Desktop | $100 | $50 |

**订阅包含**:
- 安全更新
- 性能优化
- Bug 修复
- 技术支持
- 遵循特定合规性要求

---

## 3. 版本支持

### LTS 支持周期

| 版本 | 发布 | 免费支持截止 | 付费支持截止 |
|------|------|-------------|-------------|
| JDK 8 | 2014-03 | 已终止 | 2030-12 |
| JDK 11 | 2018-09 | 已终止 | 2026-01 |
| JDK 17 | 2021-09 | 2029-10 | 2029-10 |
| JDK 21 | 2023-09 | 2031-10 | 2031-10 |
| JDK 25 | 2025-09 | 2032+ | 2032+ |

### 特性版本

| 版本 | 支持截止 |
|------|----------|
| JDK 23 | 2025-09 |
| JDK 24 | 2026-03 |

---

## 4. 特性

### 与 OpenJDK 的区别

| 特性 | Oracle JDK | OpenJDK |
|------|------------|---------|
| 核心代码 | 相同 | 相同 |
| 商业支持 | ✅ | ❌ |
| 安全更新 | 付费 | 免费社区 |
| 额外功能 | ✅ | ❌ |
| JFR | ✅ 全部 | ✅ 全部 |
| Flight Recorder | ✅ | ✅ |

### Oracle JDK 独有功能

1. **Java Mission Control (JMC)**: 性能监控工具
2. **Java Flight Recorder (JFR)**: 生产环境 profiling
3. **Advanced Management**: 企业级管理功能

---

## 5. 安装

### 下载

访问 [Oracle JDK Downloads](https://www.oracle.com/java/technologies/downloads/)

### 安装

```bash
# Linux (tar.gz)
tar -xzf jdk-21_linux-x64_bin.tar.gz
export JAVA_HOME=$PWD/jdk-21
export PATH=$JAVA_HOME/bin:$PATH

# 验证
java -version
# java version "21.0.1" 2023-10-17 LTS
# Java(TM) SE Runtime Environment (build 21.0.1+12-29)
# Java HotSpot(TM) 64-Bit Server VM (build 21.0.1+12-29, mixed mode)

# Windows (MSI)
# 运行下载的 MSI 安装程序

# macOS (PKG)
# 运行下载的 PKG 安装程序
```

### Docker

```dockerfile
# Oracle JDK 不提供官方 Docker 镜像
# 推荐使用 Oracle Linux + Oracle JDK

FROM oraclelinux:9
RUN dnf install -y java-21-openjdk-devel
```

---

## 6. 性能

### 与其他发行版对比

| 指标 | Oracle JDK | Eclipse Temurin | Amazon Corretto |
|------|------------|-----------------|-----------------|
| 吞吐量 | 100% (基准) | 100% | 100% |
| 启动时间 | ~100ms | ~100ms | ~100ms |
| 内存占用 | ~35MB | ~35MB | ~35MB |
| GC 性能 | G1/ZGC | G1/ZGC | G1/ZGC |

> Oracle JDK 与其他基于 HotSpot 的发行版性能基本相同

---

## 7. 适用场景

### 推荐使用

| 场景 | 理由 |
|------|------|
| 企业生产环境 | 官方商业支持 |
| 需要合规认证 | Oracle 认证 |
| Oracle 技术栈 | 与 Oracle 产品集成 |
| 金融行业 | 需要商业保障 |
| 政府/公共部门 | 需要长期支持承诺 |

### 不推荐使用

| 场景 | 替代方案 |
|------|----------|
| 个人开发 | Eclipse Temurin |
| 成本敏感项目 | Amazon Corretto |
| CI/CD 环境 | Eclipse Temurin |
| 云原生部署 | GraalVM |

---

## 8. 迁移

### 从 Oracle JDK 迁移到其他发行版

```bash
# 1. 选择目标发行版 (如 Temurin)
sdk install java 21-tem

# 2. 验证兼容性
java -version
javac -version

# 3. 运行测试
./mvnw test

# 4. 性能验证
# 使用 JMC 或 JFR 对比性能
```

### 从其他发行版迁移到 Oracle JDK

```bash
# 1. 下载 Oracle JDK
# 访问 https://www.oracle.com/java/technologies/downloads/

# 2. 安装
tar -xzf jdk-21_linux-x64_bin.tar.gz

# 3. 配置环境
export JAVA_HOME=$PWD/jdk-21
export PATH=$JAVA_HOME/bin:$PATH

# 4. 验证
java -version
```

---

## 9. 相关链接

### 官方资源

- [Oracle Java SE Downloads](https://www.oracle.com/java/technologies/downloads/)
- [Oracle Java SE Subscription](https://www.oracle.com/java/technologies/javase-pricing.html)
- [Oracle Java Documentation](https://docs.oracle.com/en/java/javase/21/)
- [Oracle Java Magazine](https://www.oracle.com/java/)

### 技术资源

- [Java Mission Control](https://jdk.java.net/jmc/)
- [Oracle Java Learning](https://learn.oracle.com/en-us/javase/)

---

**最后更新**: 2026-03-20
