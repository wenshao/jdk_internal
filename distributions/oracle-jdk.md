# Oracle JDK

> Oracle 官方 JDK 发行版，基于 OpenJDK 构建，提供商业支持

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
| **许可证** | NFTC (JDK 17+) / OTNLA (JDK 8, 11) |
| **商业支持** | ✅ (Java SE Subscription) |
| **源码** | 基于 OpenJDK |
| **Docker** | `container-registry.oracle.com/java/jdk:21` |

---

## 2. 许可证

### NFTC (No-Fee Terms and Conditions) - JDK 17+

自 JDK 17 起，Oracle JDK 使用 **NFTC** 许可证：
- **个人使用**: ✅ 免费
- **商业使用**: ✅ 免费
- **生产使用**: ✅ 免费
- **分发**: ✅ 允许
- **更新**: 免费获取安全更新

> ✅ **JDK 17, 21, 23, 25+ 均可免费用于生产环境**

### OTNLA (Oracle Technology Network License Agreement) - JDK 8, 11

⚠️ **需要 Java SE Subscription 的场景**:
- 商业生产环境使用
- 嵌入硬件或软件产品分发
- 需要 Oracle 官方技术支持

### Oracle Java SE Subscription

| 计划 | 价格 (每员工/年) | 适用场景 |
|------|-----------------|----------|
| **Java SE** | $150 | 标准版，包含 JDK 8, 11, 17, 21 |
| **Java SE Desktop** | $50 | 仅桌面应用 |
| **Java SE Advanced** | $300 | 包含 JRockit Mission Control |
| **Java SE Advanced Desktop** | $100 | 桌面高级版 |

**订阅包含**:
- ✅ 安全更新 (JDK 8, 11 _extended support_)
- ✅ 性能优化
- ✅ Bug 修复
- ✅ 24/7 技术支持
- ✅ 合规性保障

---

## 3. 版本支持

### LTS 支持周期

| 版本 | 发布 | 免费支持 (NFTC) | 付费支持 (Subscription) |
|------|------|-----------------|------------------------|
| JDK 8 | 2014-03 | ❌ (OTNLA) | 2030-12 |
| JDK 11 | 2018-09 | ❌ (OTNLA) | 2026-01 |
| JDK 17 | 2021-09 | ✅ 2029-10 | 2029-10 |
| JDK 21 | 2023-09 | ✅ 2031-10 | 2031-10 |
| JDK 23 | 2024-09 | ✅ 2025-03 | - |
| JDK 24 | 2025-03 | ✅ 2025-09 | - |
| JDK 25 | 2025-09 | ✅ 2026-03 | 2032-10 (Extended) |
| JDK 26 | 2026-03 | ✅ 2026-09 | 2029-10 (Extended) |

> **说明**: 
> - JDK 17+ 使用 NFTC 许可，免费获得安全更新直至下一个 LTS 发布后 6 个月
> - JDK 8, 11 使用 OTNLA 许可，商业使用需要 Java SE Subscription

### 特性版本支持策略

| 版本类型 | 支持周期 | 示例 |
|----------|----------|------|
| 特性版本 | 6 个月 | JDK 23, 24, 25, 26 |
| LTS 版本 | 8+ 年 | JDK 17, 21, 25 |

---

## 4. 特性

### 与 OpenJDK 的关系

```
┌─────────────────────────────────────────────────────────┐
│                    OpenJDK (上游)                        │
│                        │                                 │
│                        ▼                                 │
│              Oracle JDK (下游发行版)                      │
│                        │                                 │
│         ┌──────────────┴──────────────┐                 │
│         │                             │                 │
│         ▼                             ▼                 │
│   相同核心代码                   额外功能                 │
│   - HotSpot JVM                  - 商业支持               │
│   - 标准类库                     - 长期安全更新           │
│   - 标准工具                     - 技术支持               │
└─────────────────────────────────────────────────────────┘
```

### 与 OpenJDK 的区别

| 特性 | Oracle JDK | OpenJDK | 说明 |
|------|------------|---------|------|
| 核心代码 | 相同 | 相同 | 基于同一源码 |
| HotSpot JVM | 相同 | 相同 | 同一 JVM 实现 |
| 标准类库 | 相同 | 相同 | Java SE API |
| 商业支持 | ✅ | ❌ | Oracle Java SE Subscription |
| 安全更新 | ✅ (NFTC) | ✅ (社区) | Oracle 提供官方更新 |
| JFR | ✅ | ✅ | JDK 11+ 已完全开源 |
| JMC | ✅ | ✅ | 开源版本可用 |

### Oracle JDK 优势

1. **官方商业支持**: 24/7 技术支持，SLA 保障
2. **长期安全更新**: JDK 8, 11 Extended Support
3. **合规性保障**: 适合金融、政府等受监管行业
4. **Oracle 产品集成**: 与 Oracle Database, WebLogic 等深度集成
5. **性能优化**: 针对 Oracle 硬件和云环境优化

### 注意事项

> ⚠️ **JFR 和 JMC 已在 OpenJDK 中完全开源**
> - JFR: JDK 11+ 完全可用
> - JMC: 可从 adoptium.net 免费下载

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

Oracle 提供官方容器镜像：

```dockerfile
# Oracle JDK 21 (基于 Oracle Linux 9)
FROM container-registry.oracle.com/java/jdk:21

# 或者使用 Oracle Linux + JDK
FROM oraclelinux:9
RUN dnf install -y oracle-java21
```

**官方镜像仓库**:
- `container-registry.oracle.com/java/jdk:21`
- `container-registry.oracle.com/java/jdk:17`
- `container-registry.oracle.com/java/jdk:11`

### SDKMAN (Linux/macOS)

```bash
# 安装 SDKMAN
curl -s "https://get.sdkman.io" | bash

# 安装 Oracle JDK (需要接受许可证)
sdk install java 21-oracle
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
| 企业生产环境 | 官方商业支持，SLA 保障 |
| 需要合规认证 | Oracle 认证，审计支持 |
| Oracle 技术栈 | 与 Oracle Database, WebLogic 深度集成 |
| 金融/医疗行业 | 需要商业保障和长期支持 |
| 政府/公共部门 | 需要供应商支持和合规性 |
| JDK 8, 11 商业使用 | Extended Support 安全更新 |

### 替代方案考虑

| 场景 | 替代方案 | 理由 |
|------|----------|------|
| 成本敏感项目 | Eclipse Temurin / Corretto | 完全免费，无许可顾虑 |
| CI/CD 环境 | Eclipse Temurin | 社区支持，易于自动化 |
| AWS 云环境 | Amazon Corretto | AWS 优化，免费 |
| 阿里云环境 | Alibaba Dragonwell | 阿里云优化 |
| 云原生部署 | GraalVM Native Image | 快速启动，低内存 |
| 低延迟交易 | Azul Platform Prime | C4 GC，pause < 1ms |
| 大内存堆 (>1TB) | Azul Prime / IBM Semeru | 专门优化 |

> **注意**: JDK 17+ 使用 NFTC 许可，生产环境免费，可根据需求选择

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
- [Oracle Java SE Subscription](https://www.oracle.com/java/technologies/javase-subscription.html)
- [Oracle Java Documentation](https://docs.oracle.com/en/java/javase/)
- [Oracle Container Registry](https://container-registry.oracle.com/)

### 许可证

- [NFTC License (JDK 17+)](https://www.oracle.com/downloads/licenses/no-fee-license.html)
- [OTNLA License (JDK 8, 11)](https://www.oracle.com/downloads/licenses/javase-license1.html)
- [Java SE Pricing](https://www.oracle.com/java/technologies/pricing.html)

### 技术资源

- [Java Mission Control](https://jdk.java.net/jmc/)
- [Oracle Java Tutorials](https://docs.oracle.com/javase/tutorial/)
- [Oracle Java Best Practices](https://www.oracle.com/java/technologies/javase-support.html)

### 社区资源

- [WhichJDK](https://whichjdk.com/) - JDK 选择建议
- [JDK Comparison](https://jdkcomparison.com/) - JDK 对比工具

---

**最后更新**: 2026-03-21
