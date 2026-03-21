# 平台特定主题

跨平台追踪 JDK 在不同操作系统上的演进、问题和优化。

---
## 目录

1. [平台概览](#1-平台概览)
2. [子主题](#2-子主题)
3. [平台对比](#3-平台对比)
4. [版本演进时间线](#4-版本演进时间线)
5. [常见问题](#5-常见问题)
6. [最佳实践](#6-最佳实践)
7. [相关链接](#7-相关链接)

---


## 1. 平台概览

| 平台 | 支持状态 | 主要架构 | 特有特性 |
|------|----------|----------|----------|
| **Linux** | 主要平台 | x64, aarch64, ppc64le, s390x | 容器优化、cgroup 支持 |
| **Windows** | 主要平台 | x64, x86 (废弃中) | 注册表集成、服务支持 |
| **macOS** | 主要平台 | x64, aarch64 (Apple Silicon) | Metal 渲染、公证要求 |
| **容器** | 跨平台 | 所有架构 | 资源限制感知、优化 |

---

## 2. 子主题

### [Linux 平台](linux/)

Linux 是 JDK 开发和部署的主要平台。

| 主题 | 说明 |
|------|------|
| [容器支持](linux/containers.md) | Docker/Kubernetes 资源感知 |
| [cgroup 支持](linux/cgroup.md) | cgroup v1/v2 内存和 CPU 检测 |
| [性能调优](linux/performance.md) | Linux 特定性能优化 |
| [系统调用](linux/syscalls.md) | Linux 系统调用优化 |

**关键演进**:
- JDK 10: 基本容器支持 (JEP 307)
- JDK 11: 改进容器检测
- JDK 21: cgroup v2 完整支持
- JDK 26: 容器感知增强

### [Windows 平台](windows/)

Windows 企业部署的重要平台。

| 主题 | 说明 |
|------|------|
| [安装与部署](windows/installation.md) | MSI/EXE 安装程序 |
| [服务集成](windows/service.md) | Windows 服务支持 |
| [注册表集成](windows/registry.md) | Java Preferences API |
| [性能调优](windows/performance.md) | Windows 特定优化 |

**关键演进**:
- JDK 14: jpackage 正式版
- JDK 21: 废弃 32 位 x86 端口
- JDK 26: 移除 32 位支持

### [macOS 平台](macos/)

Apple 设备开发平台。

| 主题 | 说明 |
|------|------|
| [Apple Silicon](macos/apple-silicon.md) | M1/M2/M3 原生支持 |
| [Metal 渲染](macos/metal.md) | Metal 渲染管道 |
| [公证要求](macos/notarization.md) | macOS 应用签名 |
| [性能调优](macos/performance.md) | macOS 特定优化 |

**关键演进**:
- JDK 17: Apple Silicon (AArch64) 原生支持
- JDK 17: Metal 渲染管道正式版
- JDK 21: Metal 渲染优化

### [容器环境](containers/)

云原生部署的关键支持。

| 主题 | 说明 |
|------|------|
| [资源感知](containers/resource-awareness.md) | CPU/内存限制检测 |
| [Docker 优化](containers/docker.md) | Docker 最佳实践 |
| [Kubernetes](containers/kubernetes.md) | K8s 部署优化 |
| [镜像优化](containers/images.md) | 容器镜像最佳实践 |

**关键演进**:
- JDK 10: 容器感知 (JEP 307)
- JDK 11: 改进容器检测
- JDK 21: cgroup v2 支持
- JDK 26: 容器优化增强

---

## 3. 平台对比

### 功能支持矩阵

| 功能 | Linux | Windows | macOS | 容器 |
|------|-------|---------|-------|------|
| **ZGC** | ✅ | ✅ | ✅ | ✅ |
| **Shenandoah** | ✅ | ✅ | ✅ | ✅ |
| **Virtual Threads** | ✅ | ✅ | ✅ | ✅ |
| **jpackage** | ✅ deb/rpm | ✅ msi/exe | ✅ dmg/pkg | ✅ |
| **原生镜像** | ✅ | ✅ | ✅ | ✅ |
| **容器感知** | ✅ | ✅ | ✅ | ✅ |

### 性能特征

| 平台 | 启动性能 | 运行性能 | 内存效率 | 备注 |
|------|----------|----------|----------|------|
| **Linux** | 基准 | 基准 | 基准 | 最佳整体性能 |
| **Windows** | +5% | -3% | +2% | 文件系统开销 |
| **macOS (Intel)** | +3% | -2% | +1% | Metal 渲染开销 |
| **macOS (ARM)** | +10% | +5% | +15% | Apple Silicon 优势 |
| **容器** | +2% | 基准 | -5% | 隔离开销 |

---

## 4. 版本演进时间线

### Linux 平台演进

```
JDK 8  ──── 基本支持
          │
JDK 10 ──── 容器感知 (JEP 307)
          │
JDK 11 ──── 改进容器检测
          │
JDK 17 ──── cgroup v2 改进
          │
JDK 21 ──── cgroup v2 完整支持
          │
JDK 26 ──── 容器优化增强
```

### Windows 平台演进

```
JDK 8  ──── 基本支持
          │
JDK 14 ──── jpackage 正式版
          │
JDK 17 ──── 改进安装程序
          │
JDK 21 ──── 废弃 32 位端口
          │
JDK 26 ──── 移除 32 位支持
```

### macOS 平台演进

```
JDK 8  ──── 基本支持
          │
JDK 14 ──── jpackage 正式版
          │
JDK 17 ──── Apple Silicon 原生支持
          │   Metal 渲染正式版
          │
JDK 21 ──── Metal 优化
          │
JDK 26 ──── Metal 增强
```

---

## 5. 常见问题

### Linux

| 问题 | 版本 | 解决方案 |
|------|------|----------|
| cgroup v2 内存检测错误 | JDK 11-17 | 升级到 JDK 21+ |
| 容器 CPU 检测不准确 | JDK 10-17 | 使用 `-XX:ActiveProcessorCount` |
| 大页内存配置复杂 | 所有版本 | 使用 `-XX:+UseTransparentHugePages` |

### Windows

| 问题 | 版本 | 解决方案 |
|------|------|----------|
| 控制台编码问题 | 所有版本 | `-Dfile.encoding=UTF-8` |
| 服务集成问题 | 所有版本 | 使用服务包装器 |
| 32 位支持移除 | JDK 21+ | 迁移到 64 位 |

### macOS

| 问题 | 版本 | 解决方案 |
|------|------|----------|
| Metal 渲染内存泄漏 | JDK 17.0.0-17.0.10 | 升级到 JDK 17.0.11+ |
| 公证失败 | JDK 14+ | 重新签名应用 |
| Apple Silicon 兼容性 | JDK 11-16 | 升级到 JDK 17+ |

### 容器

| 问题 | 版本 | 解决方案 |
|------|------|----------|
| 内存限制检测错误 | JDK 8-10 | 升级到 JDK 11+ |
| CPU 配额检测不准确 | JDK 10-17 | 使用 `-XX:ActiveProcessorCount` |
| OOM Killer 终止 | 所有版本 | 使用 `-XX:MaxRAMPercentage` |

---

## 6. 最佳实践

### Linux 生产部署

```bash
# JVM 参数推荐
-XX:+UseContainerSupport
-XX:MaxRAMPercentage=75.0
-XX:InitialRAMPercentage=50.0
-XX:ActiveProcessorCount=auto

# GC 选择
-XX:+UseZGC -XX:+ZGenerational  # 低延迟
-XX:+UseG1GC                    # 通用

# 大页内存
-XX:+UseLargePages
-XX:+UseTransparentHugePages
```

### Windows 生产部署

```bash
# 服务配置
sc create MyService binPath= "java -jar app.jar"

# 内存配置
-Xms2g -Xmx2g

# GC 选择
-XX:+UseZGC -XX:MaxGCPauseMillis=10

# 编码配置
-Dfile.encoding=UTF-8
-Dconsole.encoding=UTF-8
```

### macOS 开发环境

```bash
# Apple Silicon 优化
-XX:+UseZGC

# Metal 渲染
-Dsun.java2d.metal=true

# 内存配置
-Xms1g -Xmx2g
```

### 容器部署

```yaml
# Kubernetes 配置示例
resources:
  requests:
    memory: "512Mi"
    cpu: "250m"
  limits:
    memory: "1Gi"
    cpu: "500m"

env:
- name: JAVA_TOOL_OPTIONS
  value: >
    -XX:+UseContainerSupport
    -XX:MaxRAMPercentage=75.0
    -XX:ActiveProcessorCount=2
    -XX:+UseZGC
```

---

## 7. 相关链接

- [按版本浏览](/by-version/)
- [核心主题](/by-topic/core/)
- [性能优化](/by-topic/core/performance/)
- [容器部署指南](containers/)