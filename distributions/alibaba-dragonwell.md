# Alibaba Dragonwell

> 阿里巴巴提供的 OpenJDK 发行版

[← 返回发行版](../distributions/)

---
## 目录

1. [概述](#1-概述)
2. [特点](#2-特点)
3. [版本支持](#3-版本支持)
4. [独有功能详解](#4-独有功能详解)
5. [安装](#5-安装)
6. [阿里云集成](#6-阿里云集成)
7. [性能](#7-性能)
8. [适用场景](#8-适用场景)
9. [贡献者](#9-贡献者)
10. [相关链接](#10-相关链接)

---


## 1. 概述

Alibaba Dragonwell (龙井) 是阿里巴巴基于 OpenJDK 构建的 JDK 发行版，针对阿里云环境和大规模电商场景优化。

| 属性 | 值 |
|------|-----|
| **组织** | 阿里巴巴 |
| **官网** | https://dragonwell-jdk.io/ |
| **下载** | https://dragonwell-jdk.io/download/ |
| **许可证** | GPLv2 + Classpath Exception |
| **商业支持** | ✅ (阿里云) |
| **源码** | 基于 OpenJDK |
| **GitHub** | https://github.com/alibaba/dragonwell8 |

---

## 2. 特点

### 核心特性

- ✅ **阿里云优化**: 针对阿里云环境深度优化
- ✅ **大规模验证**: 双11等大规模场景验证
- ✅ **长期支持**: LTS 版本长期支持
- ✅ **商业支持**: 阿里云技术支持
- ✅ **国内优化**: 针对中国市场优化

### 独有功能

| 功能 | 说明 |
|------|------|
| **JWarmUp** | 预热优化，减少冷启动影响 |
| **Elastic Heap** | 弹性堆内存，自动扩缩容 |
| **Wisp** | 协程支持 (类似虚拟线程) |
| **JFR 增强** | 更丰富的监控数据 |
| **JDK 8 增强** | 在 JDK 8 上实现部分新特性 |

---

## 3. 版本支持

### 支持周期

| 版本 | 发布 | 支持截止 | 状态 |
|------|------|----------|------|
| Dragonwell 8 | 2019 | 2029-07 | ✅ |
| Dragonwell 11 | 2020 | 2027-10 | ✅ |
| Dragonwell 17 | 2022 | 2029-10 | ✅ |
| Dragonwell 21 | 2023 | 2031-10 | ✅ |

### 版本类型

- **Standard**: 标准版，基于 OpenJDK
- **Extended**: 扩展版，包含额外优化

---

## 4. 独有功能详解

### JWarmUp

```java
// JWarmUp - 预热优化
// 在应用启动时预先编译热点代码

// 启用参数
-XX:+UseJWarmUp
-XX:JWarmUpMinRestartCount=2
-XX:JWarmUpMinStartCount=1
```

### Elastic Heap

```java
// Elastic Heap - 弹性堆内存
// 根据负载自动调整堆内存大小

// 启用参数
-XX:+UseElasticHeap
-XX:ElasticHeapMaxGCSkipMargin=20
```

### Wisp 协程

```java
// Wisp - 协程支持 (JDK 8)
// 在 JDK 8 上实现类似虚拟线程的功能

// 启用参数
-XX:+UseWisp
```

---

## 5. 安装

### 下载

访问 [Dragonwell 下载页](https://dragonwell-jdk.io/download/)

### 包管理器

```bash
# 阿里云 Linux
sudo yum install dragonwell

# 验证
java -version
# openjdk version "21.0.1" 2023-10-17 LTS
# OpenJDK Runtime Environment Dragonwell-21.0.1+12 (build 21.0.1+12-LTS)
# OpenJDK 64-Bit Server VM Dragonwell-21.0.1+12 (build 21.0.1+12-LTS, mixed mode)
```

### Docker

```bash
# 官方镜像 (阿里云容器镜像)
docker pull dragonwell-registry.cn-hangzhou.cr.aliyuncs.com/dragonwell/dragonwell:21

# 运行
docker run -it --rm dragonwell-registry.cn-hangzhou.cr.aliyuncs.com/dragonwell/dragonwell:21 java -version
```

### 手动安装

```bash
# 下载
wget https://github.com/alibaba/dragonwell21/releases/download/jdk-21.0.1.0.1+12/dragonwell-21.0.1.0.1+12-linux-x64.tar.gz

# 解压
tar -xzf dragonwell-21.0.1.0.1+12-linux-x64.tar.gz

# 配置
export JAVA_HOME=$PWD/jdk-21.0.1.0.1+12
export PATH=$JAVA_HOME/bin:$PATH

# 验证
java -version
```

---

## 6. 阿里云集成

### 阿里云 ECS

```bash
# 阿里云 ECS 提供预装 Dragonwell 的镜像
# 选择镜像时选择 "Alibaba Cloud Linux" 包含 Dragonwell

# 或手动安装
sudo yum install dragonwell -y
```

### 阿里云 ACK

```dockerfile
# Dockerfile 示例
FROM dragonwell-registry.cn-hangzhou.cr.aliyuncs.com/dragonwell/dragonwell:21

WORKDIR /app
COPY target/myapp.jar .
EXPOSE 8080

ENTRYPOINT ["java", "-jar", "myapp.jar"]
```

---

## 7. 性能

### 基准测试

| 指标 | Dragonwell 21 | OpenJDK 21 |
|------|---------------|------------|
| 吞吐量 | 100-105% | 100% |
| 启动时间 | ~95ms | ~100ms |
| 内存占用 | ~33MB | ~35MB |
| GC pause | 优化 | 标准 |

### 阿里云环境

| 指标 | Dragonwell | OpenJDK |
|------|------------|---------|
| ECS 性能 | 105% | 100% |
| ACK 启动 | 优化 | 标准 |
| 监控数据 | 丰富 | 标准 |

---

## 8. 适用场景

### 推荐使用

| 场景 | 理由 |
|------|------|
| 阿里云 ECS | 阿里云优化 |
| 阿里云 ACK | 容器优化 |
| 阿里云函数计算 | 冷启动优化 |
| 大规模电商 | 双11验证 |
| JDK 8 升级 | JWarmUp 减少升级影响 |
| 中国市场 | 本地化支持 |

### 不推荐使用

| 场景 | 替代方案 |
|------|----------|
| 非阿里云 | Eclipse Temurin |
| 国外部署 | Eclipse Temurin |

---

## 9. 贡献者

Dragonwell 由阿里巴巴 JDK 团队维护：

- **Wei Wu (吴一)** - JDK 8 维护者
- **Luo Chun (罗秦)** - GC 优化
- **Shaojin Wen (温少进)** - 性能优化
- **Fei Yang** - 核心库

[阿里巴巴贡献者](../../contributors/orgs/alibaba.md)

---

## 10. 相关链接

### 官方资源

- [Dragonwell 官网](https://dragonwell-jdk.io/)
- [Dragonwell 下载](https://dragonwell-jdk.io/download/)
- [Dragonwell GitHub](https://github.com/alibaba/dragonwell8)
- [Dragonwell 文档](https://dragonwell-jdk.io/doc/)

### 社区

- [阿里云开发者社区](https://developer.aliyun.com/)
- [Dragonwell Gitee](https://gitee.com/dragonwell/dragonwell8)

---

**最后更新**: 2026-03-20
