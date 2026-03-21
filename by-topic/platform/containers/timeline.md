# 容器环境时间线

JDK 容器支持的完整演进历史。

[← 返回容器环境](./)

---
## 目录

1. [JDK 8: 无容器感知](#1-jdk-8-无容器感知)
2. [JDK 10: 容器感知 (JEP 307)](#2-jdk-10-容器感知-jep-307)
3. [JDK 11: 改进容器检测](#3-jdk-11-改进容器检测)
4. [JDK 14: cgroup v2 初步支持](#4-jdk-14-cgroup-v2-初步支持)
5. [JDK 17: cgroup v2 改进](#5-jdk-17-cgroup-v2-改进)
6. [JDK 21: cgroup v2 完整支持](#6-jdk-21-cgroup-v2-完整支持)
7. [JDK 26: 容器优化增强](#7-jdk-26-容器优化增强)
8. [容器技术时间线](#8-容器技术时间线)
9. [JVM 参数演进](#9-jvm-参数演进)
10. [基础镜像演进](#10-基础镜像演进)
11. [核心贡献者](#11-核心贡献者)
12. [参考资料](#12-参考资料)

---


## 1. JDK 8: 无容器感知

### 问题背景

```bash
# JDK 8 不感知容器限制
docker run -m 512m openjdk:8 java -Xmx4g
# 结果: JVM 尝试分配 4GB，超出容器限制
# 容器被 OOM Killer 终止
```

### 问题

| 问题 | 描述 |
|------|------|
| **内存检测** | 读取主机内存，非容器限制 |
| **CPU 检测** | 读取主机 CPU，非容器配额 |
| **GC 线程数** | 基于主机 CPU，过多线程 |

---

## 2. JDK 10: 容器感知 (JEP 307)

### JEP 307: Container Awareness

| 日期 | 版本 | 变化 |
|------|------|------|
| 2018-03 | JDK 10 | 首次容器感知支持 |

**核心特性**:
```bash
-XX:+UseContainerSupport  # 默认启用
-XX:ActiveProcessorCount=auto
-XX:MaxRAMPercentage=75.0
```

**支持的功能**:
- ✅ 内存限制检测
- ✅ CPU 配额检测
- ❌ cgroup v2 (未支持)

---

## 3. JDK 11: 改进容器检测

### 修复和改进

| 日期 | 版本 | 变化 |
|------|------|------|
| 2018-09 | JDK 11 | 改进容器检测 |

**修复的问题**:
- 更准确的内存检测
- CPU 配额计算修复
- 限制检测边界情况

---

## 4. JDK 14: cgroup v2 初步支持

### cgroup v2 引入

```
2016 ─── Linux 内核 4.5: cgroup v2 合并
   │
2018 ─── RHEL 8: 默认使用 cgroup v2
   │
2020 ─── JDK 14: cgroup v2 初步支持
```

**支持状态**:
- ✅ 内存检测 (部分)
- ✅ CPU 检测 (部分)
- ⚠️  完整性待改进

---

## 5. JDK 17: cgroup v2 改进

### JEP Draft: 改进支持

| 日期 | 版本 | 变化 |
|------|------|------|
| 2021-09 | JDK 17 | cgroup v2 改进 |

**改进**:
- 更准确的内存检测
- CPU 配额检测优化
- 错误处理改进

---

## 6. JDK 21: cgroup v2 完整支持

### 完整支持

| 日期 | 版本 | 变化 |
|------|------|------|
| 2023-09 | JDK 21 | cgroup v2 完整支持 |

**完整功能**:
- ✅ 内存限制检测
- ✅ CPU 配额检测
- ✅ 内存和 CPU 使用统计
- ✅ cgroup v2 统一接口

**验证**:
```bash
# 检查容器支持
jcmd <pid> VM.flags | grep -i container

# 输出
bool UseContainerSupport = true
```

---

## 7. JDK 26: 容器优化增强

### 性能优化

| 日期 | 版本 | 变化 |
|------|------|------|
| 2025 | JDK 26 | 容器优化增强 |

**改进**:
- 更精确的资源检测
- 减少系统调用开销
- 性能优化

---

## 8. 容器技术时间线

### Docker

```
2013 ─── Docker 发布
   │
2014 ─── Docker 1.0
   │
2017 ─── Docker 企业版
   │
2020 ─── Docker 集成到 Kubernetes
```

### Kubernetes

```
2014 ─── Kubernetes 发布
   │
2015 ─── Kubernetes 1.0
   │
2018 ─── Kubernetes 1.10 (大规模采用)
   │
2020 ─── Kubernetes 1.19 (cgroup v2 默认)
```

### cgroup

```
2006 ─── cgroup v1 引入 (Linux 2.6.24)
   │
2016 ─── cgroup v2 合并 (Linux 4.5)
   │
2018 ─── RHEL 8 默认 cgroup v2
   │
2020 ─── Ubuntu 21.04 默认 cgroup v2
```

---

## 9. JVM 参数演进

### 内存参数

```
JDK 8 ─── -Xmx, -Xms (固定值)
   │
JDK 10 ─── -XX:MaxRAMPercentage (百分比)
   │
JDK 11 ─── -XX:InitialRAMPercentage
   │
JDK 21 ─── -XX:MinRAMPercentage
```

### CPU 参数

```
JDK 8 ─── 自动检测主机 CPU
   │
JDK 10 ─── -XX:ActiveProcessorCount=auto
   │
JDK 17 ─── 改进 CPU 检测
```

---

## 10. 基础镜像演进

### OpenJDK 镜像

| 镜像 | 发布时间 | 大小 | 说明 |
|------|----------|------|------|
| openjdk:8-jre-alpine | 2017 | ~100MB | 精简镜像 |
| eclipse-temurin | 2021 | ~100MB | AdoptOpenJDk 后继 |
| eclipse-temurin:21-jre-alpine | 2023 | ~100MB | JDK 21 精简版 |
| gcr.io/distroless/java21 | 2022 | ~150MB | Distroless 镜像 |

---

## 11. 核心贡献者

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| [Ioi Lam](/by-contributor/profiles/ioi-lam.md) | Oracle | CDS, 容器支持 |
| [Bob Vandette](/by-contributor/profiles/bob-vandette.md) | Oracle | 容器感知实现 |
| [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | Oracle | 类加载, CDS |

---

## 12. 参考资料

- [JEP 307](/jeps/platform/jep-307.md)
- [Docker 文档](https://docs.docker.com/)
- [Kubernetes 文档](https://kubernetes.io/docs/)

→ [返回容器环境](./)
