# Amazon Corretto

> Amazon 提供的免费 OpenJDK 发行版

[← 返回发行版](../distributions/)

---

## 概述

Amazon Corretto 是 Amazon Web Services 提供的免费、多平台、生产就绪的 OpenJDK 发行版。

| 属性 | 值 |
|------|-----|
| **组织** | Amazon Web Services |
| **官网** | https://aws.amazon.com/corretto/ |
| **下载** | https://corretto.aws/downloads/ |
| **许可证** | GPLv2 + Classpath Exception |
| **商业支持** | ❌ (AWS 支持计划) |
| **源码** | 基于 OpenJDK |
| **GitHub** | https://github.com/corretto |

---

## 特点

### 核心特性

- ✅ **完全免费**: 无需订阅，个人和商业使用免费
- ✅ **长期支持**: LTS 版本支持 8 年
- ✅ **AWS 优化**: 针对 AWS 环境优化
- ✅ **安全补丁**: Amazon 独立的安全补丁
- ✅ **多平台**: Linux, Windows, macOS, Docker
- ✅ **生产就绪**: AWS 内部大规模使用

### Amazon 内部使用

Corretto 在 AWS 内部广泛使用：
- Amazon EC2
- Amazon S3
- Amazon Lambda
- AWS 服务

---

## 版本支持

### 支持周期

| 版本 | 发布 | 支持截止 | 支持时长 |
|------|------|----------|----------|
| Corretto 8 | 2018 | 2026-05 | 8 年 |
| Corretto 11 | 2019 | 2027-09 | 8 年 |
| Corretto 17 | 2021 | 2029-09 | 8 年 |
| Corretto 21 | 2023 | 2032-04 | 8 年 |
| Corretto 23 | 2024 | 2025-10 | 1 年 |
| Corretto 24 | 2025 | 2026-03 | 1 年 |

### 更新策略

- **LTS 版本**: 季度更新
- **特性版本**: 每月更新
- **安全补丁**: 及时发布
- **长期支持**: 至少 8 年

---

## 安装

### SDKMAN

```bash
# 安装 Corretto
sdk install java 21-amzn
sdk use java 21-amzn

# 验证
java -version
# openjdk version "21.0.1" 2023-10-17 LTS
# OpenJDK Runtime Environment Corretto-21.0.1.12.1 (build 21.0.1+12-LTS)
# OpenJDK 64-Bit Server VM Corretto-21.0.1.12.1 (build 21.0.1+12-LTS, mixed mode)
```

### Docker

```bash
# 官方镜像
docker pull amazoncorretto:21
docker pull amazoncorretto:21-alpine
docker pull amazoncorretto:21-alpine3.19

# 运行
docker run -it --rm amazoncorretto:21 java -version
```

### 包管理器

```bash
# Amazon Linux 2023
sudo dnf install java-21-amazon-corretto -y

# Amazon Linux 2
sudo amazon-linux-extras install java-openjdk11
sudo yum install java-21-amazon-corretto -y

# Ubuntu/Debian
wget -O- https://apt.corretto.aws/corretto.key | sudo apt-key add -
sudo add-apt-repository 'deb https://apt.corretto.aws/ main'
sudo apt-get update
sudo apt-get install -y java-21-amazon-corretto

# macOS (Homebrew)
brew install --cask corretto
brew install --cask corretto@17
brew install --cask corretto@11
brew install --cask corretto@8

# Windows (winget)
winget install Amazon.Corretto.21
winget install Amazon.Corretto.17
```

### 手动安装

```bash
# 下载
wget https://corretto.aws/downloads/latest/amazon-corretto-21-x64-linux-jdk.tar.gz

# 解压
tar -xzf amazon-corretto-21-x64-linux-jdk.tar.gz

# 配置
export JAVA_HOME=$PWD/amazon-corretto-21.0.1.12.1-linux-x64
export PATH=$JAVA_HOME/bin:$PATH

# 验证
java -version
```

---

## AWS 集成

### Amazon EC2

```bash
# Amazon Linux 2023 AMI 预装 Corretto
# 启动实例后即可使用

# 安装特定版本
sudo dnf install java-21-amazon-corretto -y
```

### Amazon ECR

```dockerfile
# Dockerfile 示例
FROM amazoncorretto:21

WORKDIR /app
COPY target/myapp.jar .
EXPOSE 8080

ENTRYPOINT ["java", "-jar", "myapp.jar"]
```

### AWS Lambda

```yaml
# SAM Template 示例
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: java21
      CodeUri: ./target/myapp.jar
      Handler: com.example.Handler::handleRequest
```

---

## 性能

### 基准测试

| 指标 | Corretto 21 |
|------|-------------|
| 启动时间 | ~100ms |
| 内存占用 | ~35MB |
| 吞吐量 | 100% (基准) |

### AWS 环境优化

- **EC2**: 针对 EC2 实例优化
- **Graviton**: ARM64 架构优化
- **Lambda**: 冷启动优化
- **Fargate**: 容器优化

---

## 适用场景

### 推荐使用

| 场景 | 理由 |
|------|------|
| AWS 云环境 | AWS 优化，免费 |
| 成本敏感项目 | 完全免费 |
| 长期支持 | 8 年支持周期 |
| Lambda 函数 | AWS 原生支持 |
| EC2 实例 | 预装或易于安装 |

### 不推荐使用

| 场景 | 替代方案 |
|------|----------|
| 非云环境 | Eclipse Temurin |
| 需要商业支持 | Azul Zulu Enterprise |

---

## 相关链接

### 官方资源

- [Amazon Corretto 官网](https://aws.amazon.com/corretto/)
- [Corretto 下载页](https://corretto.aws/downloads/)
- [Corretto GitHub](https://github.com/corretto)
- [Corretto 博客](https://aws.amazon.com/blogs/opensource/)

### 文档

- [Corretto 文档](https://docs.aws.amazon.com/corretto/)
- [Corretto 发行说明](https://github.com/corretto/corretto-21/releases)

### Docker Hub

- [amazoncorretto](https://hub.docker.com/_/amazoncorretto)

---

**最后更新**: 2026-03-20
