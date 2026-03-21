# 腾讯

> G1 GC 和容器化优化

[← 返回组织索引](../../by-contributor/index.md)

---
## 目录

1. [概览](#1-概览)
2. [贡献者](#2-贡献者)
3. [主要领域](#3-主要领域)
4. [关键贡献](#4-关键贡献)
5. [影响的模块](#5-影响的模块)
6. [Tencent Kona](#6-tencent-kona)
7. [数据来源](#7-数据来源)
8. [相关链接](#8-相关链接)

---


## 1. 概览

腾讯通过 Kona 团队参与 OpenJDK 开发，专注于 G1 GC 优化和容器化场景支持。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 10+ |
| **贡献者数** | 2 |
| **活跃时间** | 2021 - 至今 |
| **主要领域** | G1 GC, 容器 |
| **Kona** | [Tencent Kona](https://github.com/Tencent/TencentKona-8) |

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。OpenJDK Committer 使用 `@openjdk.org` 邮箱提交代码，因此 git commits 按邮箱统计不准确。

---

## 2. 贡献者

| 贡献者 | GitHub | PRs | 角色 | 主要领域 | 档案 |
|--------|--------|-----|------|----------|------|
| Tongbao Zhang | [@tbzhang](https://github.com/tbzhang) | 5 | Author | G1 GC | [详情](../../by-contributor/profiles/tongbao-zhang.md) |
| Luo Chunyi | [@luochunyi](https://github.com/luochunyi) | 5+ | Author | G1 GC | - |

**小计**: 10+ PRs

> **注**: 
> - Sendao Yan (202 PRs) 是 **Hygon** 员工（前阿里巴巴），不属于腾讯
> - Wang Dingwei (@dw-virtual) 需要进一步核实组织归属

---

## 3. 主要领域

### G1 GC

- G1 垃圾收集器优化
- 压缩指针边界修复
- 对齐检查修复

### 容器化

- 容器资源检测
- Cgroup 支持

---

## 4. 关键贡献

| Issue | 标题 | 贡献者 | 说明 |
|-------|------|--------|------|
| 8354145 | G1 压缩指针边界计算修复 | [Tongbao Zhang](../../by-contributor/profiles/tongbao-zhang.md) | 正确性修复 |
| 8293782 | Shenandoah 锁排名检查修复 | [Tongbao Zhang](../../by-contributor/profiles/tongbao-zhang.md) | 测试修复 |
| 8274259 | G1 对齐检查修复 | [Tongbao Zhang](../../by-contributor/profiles/tongbao-zhang.md) | 正确性修复 |

---

## 5. 影响的模块

| 模块 | 文件数 | 说明 |
|------|--------|------|
| G1 GC | 5+ | G1 垃圾收集器 |
| Shenandoah GC | 2+ | Shenandoah 测试 |
| 容器检测 | 2+ | Cgroup 支持 |

---

## 6. Tencent Kona

腾讯维护自己的 JDK 发行版 Kona：

| 特性 | 说明 |
|------|------|
| 基于 | OpenJDK |
| 支持 | 长期支持版本 |
| 特点 | 云原生优化 |
| 许可 | GPLv2 |

**版本**: Kona 8 / 11 / 17 / 21

---

## 7. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-21

---

## 8. 相关链接

- [Tencent Kona](https://github.com/Tencent/TencentKona-8)
- [腾讯云 Java](https://cloud.tencent.com/product/tke)

[→ 返回组织索引](../../by-contributor/index.md)
