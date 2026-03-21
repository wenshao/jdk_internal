# IBM Semeru

> IBM 提供的 OpenJDK 发行版 (Eclipse OpenJ9 VM)

[← 返回发行版](../distributions/)

---
## 目录

1. [概述](#1-概述)
2. [Eclipse OpenJ9 vs HotSpot](#2-eclipse-openj9-vs-hotspot)
3. [版本支持](#3-版本支持)
4. [安装](#4-安装)
5. [适用场景](#5-适用场景)
6. [相关链接](#6-相关链接)

---


## 1. 概述

IBM Semeru (原 AdoptOpenJDK OpenJ9) 是 IBM 提供的 OpenJDK 发行版，使用 Eclipse OpenJ9 虚拟机。

| 属性 | 值 |
|------|-----|
| **组织** | IBM |
| **官网** | https://developer.ibm.com/languages/java/semeru-runtimes/ |
| **下载** | https://developer.ibm.com/languages/java/semeru-runtimes/downloads/ |
| **许可证** | GPLv2 + CPEx (社区) / 商业 |
| **商业支持** | ✅ |
| **VM** | Eclipse OpenJ9 (非 HotSpot) |

---

## 2. Eclipse OpenJ9 vs HotSpot

### 对比

| 特性 | HotSpot | Eclipse OpenJ9 |
|------|---------|----------------|
| 内存占用 | ~35MB | ~20MB (低 30-50%) |
| 启动时间 | ~100ms | ~60ms (更快) |
| 吞吐量 | 100% | 90-95% |
| 成熟度 | 高 | 中等 |
| 工具兼容 | 完全 | 大部分 |

### Eclipse OpenJ9 特性

- **共享缓存 (SCC)**: 跨 VM 共享类缓存
- **类数据共享 (CDS)**: 减少内存占用
- **AOT 编译**: 提前编译优化
- **Docker 优化**: 容器友好
- **类数据共享 (CDS)**: 减少内存占用
- **AOT 编译**: 提前编译优化
- **Docker 优化**: 容器友好

---

## 3. 版本支持

| 版本 | 支持截止 |
|------|----------|
| Semeru 8 | 2026-09 |
| Semeru 11 | 2027-10 |
| Semeru 17 | 2029-10 |
| Semeru 21 | 2031-10 |

---

## 4. 安装

### SDKMAN

```bash
sdk install java 21-sem
sdk use java 21-sem
```

### Docker

```bash
docker pull ibm-semeru-runtimes:open-21-jdk
docker pull ibm-semeru-runtimes:open-21-jre-alpine
```

---

## 5. 适用场景

| 场景 | 理由 |
|------|------|
| 内存敏感 | OpenJ9 低内存 |
| 云原生 | 快速启动 |
| 容器化 | 低内存占用 |
| IBM Cloud | IBM 优化 |

---

## 6. 相关链接

- [IBM Semeru](https://developer.ibm.com/languages/java/semeru-runtimes/)
- [OpenJ9 GitHub](https://github.com/eclipse-openj9/openj9)

---

**最后更新**: 2026-03-20
