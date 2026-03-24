# Tencent Kona

> 腾讯提供的 OpenJDK 发行版

[← 返回发行版](../distributions/)

---
## 目录

1. [概述](#1-概述)
2. [特点](#2-特点)
3. [版本支持](#3-版本支持)
4. [安装](#4-安装)
5. [相关链接](#5-相关链接)

---


## 1. 概述

Tencent Kona (腾讯 JDK) 是腾讯基于 OpenJDK 构建的 JDK 发行版，针对腾讯云环境和容器化场景优化。

| 属性 | 值 |
|------|-----|
| **组织** | 腾讯 |
| **GitHub** | https://github.com/Tencent/TencentKona-8 |
| **许可证** | GPLv2 + Classpath Exception |
| **商业支持** | ❌ (腾讯云支持) |
| **源码** | 基于 OpenJDK |

---

## 2. 特点

### 核心特性

- ✅ **腾讯云优化**: 针对腾讯云环境优化
- ✅ **容器优化**: 容器资源感知
- ✅ **G1 GC 增强**: 性能优化
- ✅ **完全免费**: 个人和商业使用免费
- ✅ **大规模验证**: 微信等大规模使用

---

## 3. 版本支持

| 版本 | 发布 | 支持截止 | 状态 |
|------|------|----------|------|
| Kona 8 | 2019 | 2026-05 | ⚠️ 即将终止 |
| Kona 11 | 2020 | 2027-10 | ✅ |
| Kona 17 | 2022 | 2029-10 | ✅ |
| Kona 21 | 2024 | 2031-10 | ✅ |

> ⚠️ **注意**: Kona 8 支持即将终止，建议迁移到 Kona 11 或更高版本

---

## 4. 安装

```bash
# 腾讯云
yum install tencent-kona

# Docker
docker pull ccr.ccs.tencentyun.com/qcloud/tencentkona8:latest
```

---

## 5. 上游维护团队

### 团队负责人

**杨晓峰 (Yang Xiaofeng)** — 腾讯 JDK 团队技术领导，前 Oracle Java 核心工程师。

### 维护分支贡献统计

| 贡献者 | jdk17u | jdk21u | jdk11u | jdk8u | 总计 |
|--------|--------|--------|--------|-------|------|
| [DamonFool](https://github.com/DamonFool) (Jie Fu) | 5 | 0 | 20 | 0 | **25** |
| johnshajiang | 1 | 1 | 2 | 1 | **5** |
| **合计** | **6** | **1** | **22** | **1** | **30** |

### 主线贡献

Tencent 在 openjdk/jdk 主线有 **223+ PRs**，核心贡献者:
- **[Jie Fu (傅杰)](https://github.com/DamonFool)** — 187 PRs, 编译器测试/修复, GC
- **[John Jiang](https://github.com/johnshajiang)** — 30+ PRs, 安全/密码学

> 详情: [Tencent 组织页面](../contributors/orgs/tencent.md)

---

## 6. 相关链接

- [Tencent Kona GitHub](https://github.com/Tencent/TencentKona-8)

---

**最后更新**: 2026-03-20
