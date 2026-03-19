# 腾讯

> G1 GC 和容器化优化

---

## 概览

腾讯通过 Kona 团队参与 OpenJDK 开发，专注于 G1 GC 优化和容器化场景支持。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 40+ |
| **贡献者数** | 10+ |
| **主要领域** | G1 GC, 容器 |

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。OpenJDK Committer 使用 `@openjdk.org` 邮箱提交代码，因此 git commits 按邮箱统计不准确。

---

## 主要领域

### G1 GC

- G1 垃圾收集器优化
- 压缩指针边界修复

### 容器化

- 容器资源检测
- Cgroup 支持

### 测试

- 测试稳定性改进
- 问题修复

---

## Tencent Kona

腾讯维护自己的 JDK 发行版 Kona：

| 特性 | 说明 |
|------|------|
| 基于 | OpenJDK |
| 支持 | 长期支持版本 |
| 特点 | 云原生优化 |
| 许可 | GPLv2 |

---

## 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-19

---

## 相关链接

- [Tencent Kona](https://github.com/Tencent/TencentKona-8)
- [腾讯云 Java](https://cloud.tencent.com/product/tke)