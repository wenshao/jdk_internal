# Tencent Kona

> 腾讯提供的 OpenJDK 发行版

[← 返回发行版](../distributions/)

---

## 概述

Tencent Kona (腾讯 JDK) 是腾讯基于 OpenJDK 构建的 JDK 发行版，针对腾讯云环境和容器化场景优化。

| 属性 | 值 |
|------|-----|
| **组织** | 腾讯 |
| **GitHub** | https://github.com/Tencent/TencentKona-8 |
| **许可证** | GPLv2 + Classpath Exception |
| **商业支持** | ❌ (腾讯云支持) |
| **源码** | 基于 OpenJDK |

---

## 特点

### 核心特性

- ✅ **腾讯云优化**: 针对腾讯云环境优化
- ✅ **容器优化**: 容器资源感知
- ✅ **G1 GC 增强**: 性能优化
- ✅ **完全免费**: 个人和商业使用免费
- ✅ **大规模验证**: 微信等大规模使用

---

## 版本支持

| 版本 | 发布 | 支持截止 |
|------|------|----------|
| Kona 8 | - | 2025-04 |
| Kona 11 | - | 2027-10 |
| Kona 17 | - | 2029-10 |

---

## 安装

```bash
# 腾讯云
yum install tencent-kona

# Docker
docker pull ccr.ccs.tencentyun.com/qcloud/tencentkona8:latest
```

---

## 相关链接

- [Tencent Kona GitHub](https://github.com/Tencent/TencentKona-8)

---

**最后更新**: 2026-03-20
