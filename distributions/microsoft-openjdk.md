# Microsoft Build of OpenJDK

> 微软提供的 OpenJDK 发行版

[← 返回发行版](../distributions/)

---

## 概述

Microsoft Build of OpenJDK 是微软提供的 OpenJDK 发行版，针对 Azure 和 Windows 优化。

| 属性 | 值 |
|------|-----|
| **组织** | Microsoft |
| **官网** | https://learn.microsoft.com/java/openjdk/ |
| **下载** | https://learn.microsoft.com/java/openjdk/download |
| **许可证** | GPLv2 + CPEx |
| **商业支持** | ✅ (Azure 支持) |
| **源码** | https://github.com/microsoft/openjdk-build |

---

## 特点

### 核心特性

- ✅ **Azure 优化**: 针对云服务优化
- ✅ **Windows 优化**: Windows 平台优化
- ✅ **安全补丁**: 微软安全补丁
- ✅ **开源**: 开源构建过程

### 微软集成

- **Azure**: Azure Functions, App Service
- **Visual Studio**: VS Code 支持
- **GitHub**: GitHub Codespaces
- **Windows**: Windows 原生支持

---

## 版本支持

| 版本 | 支持截止 |
|------|----------|
| Microsoft 17 | 2029-10 |
| Microsoft 21 | 2031-10 |

---

## 安装

### winget (Windows)

```bash
# 安装
winget install Microsoft.OpenJDK.21
winget install Microsoft.OpenJDK.17

# 验证
java -version
# openjdk version "21.0.1" 2023-10-17 LTS
# OpenJDK Runtime Environment Microsoft-21.0.1 (build 21.0.1+12)
# OpenJDK 64-Bit Server VM Microsoft-21.0.1 (build 21.0.1+12, mixed mode)
```

### Docker

```bash
# 官方镜像
docker pull mcr.microsoft.com/openjdk/jdk:21
docker pull mcr.microsoft.com/openjdk/jre:21
docker pull mcr.microsoft.com/openjdk/jdk:21-windowsservercore-ltsc2022

# 运行
docker run -it --rm mcr.microsoft.com/openjdk/jdk:21 java -version
```

### MSI 安装 (Windows)

```powershell
# 下载并安装 MSI
# https://learn.microsoft.com/java/openjdk/download#download-openjdk-for-windows

# 验证
java -version
```

---

## Azure 集成

### Azure Functions

```bash
# 使用 Microsoft OpenJDK 创建 Azure Functions
func init --java
```

### Azure App Service

```bash
# Azure App Service 支持 Microsoft OpenJDK
# 配置 Java 版本
az webapp config set --java-version 21 --java-container mcr.microsoft.com/openjdk/jdk:21
```

### Azure DevOps

```yaml
# Azure Pipeline 示例
pool:
  vmImage: 'windows-latest'

steps:
- task: JavaToolInstaller@1
  inputs:
    versionSpec: '21'
    jdkArchitectureOption: 'x64'
    jdkSourceOption: 'PreInstalled'
```

---

## 性能

### 基准测试

| 指标 | Microsoft OpenJDK |
|------|-------------------|
| 启动时间 | ~100ms |
| 内存占用 | ~35MB |
| 吞吐量 | 100% (基准) |

---

## 适用场景

### 推荐使用

| 场景 | 理由 |
|------|------|
| Azure 环境 | Azure 优化 |
| Windows Server | Windows 优化 |
| 微软技术栈 | 与微软产品集成 |
| GitHub Actions | GitHub 支持 |
| VS Code | VS Code 集成 |

### 不推荐使用

| 场景 | 替代方案 |
|------|----------|
| 非微软环境 | Eclipse Temurin |

---

## 相关链接

### 官方资源

- [Microsoft OpenJDK 文档](https://learn.microsoft.com/java/openjdk/)
- [Microsoft OpenJDK 下载](https://learn.microsoft.com/java/openjdk/download)
- [Microsoft OpenJDK GitHub](https://github.com/microsoft/openjdk-build)
- [Azure Java 文档](https://learn.microsoft.com/azure/developer/java/)

### 容器镜像

- [Microsoft Container Registry](https://mcr.microsoft.com/openjdk/jdk)

---

**最后更新**: 2026-03-20
