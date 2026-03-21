# Loongson JDK

> 龙芯提供的 OpenJDK 发行版 (LoongArch 架构)

[← 返回发行版](../distributions/)

---
## 目录

1. [概述](#1-概述)
2. [特点](#2-特点)
3. [版本支持](#3-版本支持)
4. [安装](#4-安装)
5. [性能](#5-性能)
6. [适用场景](#6-适用场景)
7. [贡献](#7-贡献)
8. [相关链接](#8-相关链接)

---


## 1. 概述

Loongson JDK 是龙芯中科针对 LoongArch (龙芯) 架构优化的 OpenJDK 发行版，支持信创国产化环境。

| 属性 | 值 |
|------|-----|
| **组织** | 龙芯中科 |
| **官网** | https://www.loongnix.cn/ |
| **下载** | https://www.loongnix.cn/zh/api/java/ |
| **许可证** | GPLv2 + Classpath Exception |
| **商业支持** | ❌ (社区支持) |
| **源码** | 基于 OpenJDK |
| **架构** | LoongArch64, MIPS64 |

---

## 2. 特点

### 核心特性

- ✅ **LoongArch 原生**: 针对龙芯 CPU 架构优化
- ✅ **信创支持**: 符合信创国产化要求
- ✅ **JCK 认证**: 通过 Java 兼容性测试
- ✅ **长期支持**: LTS 版本长期支持
- ✅ **完全免费**: 个人和商业使用免费

### 架构支持

| 架构 | 说明 | 状态 |
|------|------|------|
| **LoongArch64** | 龙芯新架构 (LA464, LA664) | ✅ 推荐 |
| **MIPS64** | 旧架构 | ⚠️ 维护模式 |

---

## 3. 版本支持

### 支持周期

| 版本 | 发布 | 支持截止 | 状态 |
|------|------|----------|------|
| Loongson JDK 8 | - | 2026-05 | ✅ |
| Loongson JDK 11 | 2022-01 | 2027-10 | ✅ |
| Loongson JDK 17 | 2023 | 2029-10 | ✅ |
| Loongson JDK 21 | 2024 | 2031-10 | ✅ |

### 版本历史

| 版本 | OpenJDK 版本 | 发布日期 |
|------|-------------|----------|
| JDK 11.0.13+8 | OpenJDK 11.0.13 | 2022-01-27 |
| JDK 17.0.8+7 | OpenJDK 17.0.8 | 2023-08 |
| JDK 21.0.1+12 | OpenJDK 21.0.1 | 2024 |

---

## 4. 安装

### 下载

访问 [Loongson JDK 下载页](https://www.loongnix.cn/zh/api/java/downloads-jdk11/)

### 包管理器

```bash
# 龙芯 Linux (Loongnix)
sudo apt install loongson-jdk-11

# 验证
java -version
# openjdk version "11.0.13" 2021-10-19
# OpenJDK Runtime Environment (build 11.0.13+8-loongson)
# OpenJDK 64-Bit Server VM (build 11.0.13+8-loongson, mixed mode)
```

### 手动安装

```bash
# 下载
wget https://github.com/loongson/jdk11u/releases/download/jdk-11.0.13%2B8-loongson/openjdk-11.0.13_8-loongson-loongarch64.tar.gz

# 解压
tar -xzf openjdk-11.0.13_8-loongson-loongarch64.tar.gz

# 配置
export JAVA_HOME=$PWD/jdk-11.0.13-loongson
export PATH=$JAVA_HOME/bin:$PATH

# 验证
java -version
```

### Docker

```dockerfile
# 基于龙芯 Linux
FROM loongarch64/debian:latest

# 安装 Loongson JDK
RUN apt update && apt install -y loongson-jdk-11

# 验证
RUN java -version
```

---

## 5. 性能

### 基准测试

| CPU | 吞吐量 | 启动时间 |
|-----|--------|----------|
| LA464 @ 2.0GHz | ~85% | ~120ms |
| LA664 @ 2.5GHz | ~95% | ~110ms |

### 优化

- **SIMD 指令**: 使用 LoongArch SIMD 优化
- **分支预测**: 针对龙芯 CPU 优化
- **缓存优化**: 针对 LoongArch 缓存结构优化

---

## 6. 适用场景

### 推荐使用

| 场景 | 理由 |
|------|------|
| 信创环境 | 国产化要求 |
| 龙芯平台 | LoongArch 原生支持 |
| 政府项目 | 国产化要求 |
| 国产服务器 | 龙芯服务器 |
| kkFileView | 龙芯平台文件预览 |

### 不推荐使用

| 场景 | 替代方案 |
|------|----------|
| x86 平台 | Eclipse Temurin |
| ARM 平台 | Azul Zulu |

---

## 7. 贡献

### OpenJDK 贡献

龙芯在 OpenJDK 社区活跃贡献：

- **OpenJDK 13**: 全球贡献排名 **第 5** (中国厂商最高)
- **OpenJDK 17**: LoongArch 移植
- **OpenJDK 21**: LoongArch 优化

### 代码仓库

| 仓库 | 地址 |
|------|------|
| JDK 11u | https://gitee.com/loongson3/jdk11u |
| JDK 17u | https://gitee.com/loongson3/jdk17u |
| JDK | https://github.com/loongson/jdk |

---

## 8. 相关链接

### 官方资源

- [Loongson JDK 下载](https://www.loongnix.cn/zh/api/java/)
- [Loongnix 文档](https://docs.loongnix.cn/java/)
- [龙芯中科官网](https://www.loongson.cn/)

### 社区

- [龙芯开源社区](https://www.loongnix.cn/)
- [Loongson Gitee](https://gitee.com/loongson)

### 安装文档

- [Loongson JDK 安装指南](https://docs.loongnix.cn/java/install.html)

---

**最后更新**: 2026-03-20
