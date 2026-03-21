# BellSoft Liberica

> BellSoft 提供的多平台 OpenJDK 发行版

[← 返回发行版](../distributions/)

---
## 目录

1. [概述](#1-概述)
2. [版本类型](#2-版本类型)
3. [特点](#3-特点)
4. [安装](#4-安装)
5. [适用场景](#5-适用场景)
6. [相关链接](#6-相关链接)

---


## 1. 概述

Liberica 是 BellSoft 提供的 OpenJDK 发行版，以多平台支持和轻量级著称。

| 属性 | 值 |
|------|-----|
| **组织** | BellSoft |
| **官网** | https://bell-sw.com/ |
| **下载** | https://bell-sw.com/pages/downloads/ |
| **许可证** | GPLv2 + CPEx (社区) / 商业 |
| **商业支持** | ✅ |
| **特性** | 多平台，Native Image |

---

## 2. 版本类型

| 版本 | 说明 |
|------|------|
| **Liberica JDK** | 标准版 |
| **Liberica Lite** | 轻量版，小体积 |
| **Liberica NIK** | Native Image Kit |

---

## 3. 特点

- ✅ **多平台**: Linux, Windows, macOS, ARM, RISC-V, Alpine
- ✅ **Lite 版本**: 更小的体积
- ✅ **Native Image**: 包含 GraalVM Native Image

---

## 4. 安装

### SDKMAN

```bash
sdk install java 21-librca
sdk use java 21-librca
```

### Docker

```bash
docker pull bellsoft/liberica-runtime-container:jdk-21
docker pull bellsoft/liberica-runtime-container:jre-21-alpine
```

---

## 5. 适用场景

| 场景 | 理由 |
|------|------|
| 嵌入式设备 | Lite 版本 |
| Alpine Linux | musl 支持 |
| RISC-V | 架构支持 |
| Native Image | NIK 版本 |

---

## 6. 相关链接

- [BellSoft 官网](https://bell-sw.com/)
- [Liberica 下载](https://bell-sw.com/pages/downloads/)

---

**最后更新**: 2026-03-20
