# 腾讯

> G1 GC 和容器化优化

[← 返回组织索引](../../by-contributor/index.md)

---
## 目录

1. [概览](#1-概览)
2. [贡献者](#2-贡献者)
3. [多层网络分析](#3-多层网络分析)
4. [主要领域](#4-主要领域)
5. [关键贡献](#5-关键贡献)
6. [影响的模块](#6-影响的模块)
7. [Tencent Kona](#7-tencent-kona)
8. [数据来源](#8-数据来源)
9. [相关链接](#9-相关链接)

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

## 3. 多层网络分析

### 3.1 协作网络 (Co-authorship Network)

基于腾讯 Kona 团队的协作关系分析：

```
                          腾讯协作网络图
                          
                    ┌─────────────────────────────┐
                    │      Tencent (腾讯)          │
                    │   G1 GC / Container          │
                    └─────────────┬───────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
          ▼                       ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │ 核心团队  │           │ 技术协作圈 │           │ 审查协作圈 │
    │  (内部)   │           │  (外部)   │           │  (外部)   │
    └────┬─────┘           └────┬─────┘           └────┬─────┘
         │                      │                      │
    ┌────┴────┐           ┌────┴────┐           ┌────┴────┐
    │Tongbao  │           │Thomas   │           │Albert   │
    │Zhang    │           │Schatzl  │           │Mingkun  │
    │(5)      │           │(G1 GC)  │           │Yang     │
    │         │           │         │           │(G1 GC)  │
    │Luo      │           │Shaojin  │           │         │
    │Chunyi   │           │Wen      │           │         │
    │(5+)     │           │(Alibaba)│           │         │
    └─────────┘           └─────────┘           └─────────┘
```

#### 核心团队 (腾讯内部)

| 贡献者 | 组织 | PRs | 主要领域 | 角色 |
|--------|------|-----|----------|------|
| [Tongbao Zhang](../../by-contributor/profiles/tongbao-zhang.md) | Tencent | 5 | G1 GC | Author |
| Luo Chunyi | Tencent | 5+ | G1 GC | Author |

#### 技术协作圈 (外部合作)

| 贡献者 | 组织 | 合作领域 | 关系类型 |
|--------|------|----------|----------|
| [Thomas Schatzl](../../by-contributor/profiles/thomas-schatzl.md) | Oracle | G1 GC | 技术同行 |
| [Albert Mingkun Yang](../../by-contributor/profiles/albert-mingkun-yang.md) | Oracle | G1 GC | 技术同行 |
| [Shaojin Wen](../../by-contributor/profiles/shaojin-wen.md) | Alibaba | 性能优化 | 技术同行 |

### 3.2 技术影响力网络

```
                    腾讯技术影响力辐射图
                    
                         G1 GC 优化
                              │
                    ┌─────────┼─────────┐
                    │         │         │
                    ▼         ▼         ▼
               压缩指针   对齐检查   容器检测
                    │         │         │
                    └─────────┼─────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
              正确性修复         Cgroup 支持
                    │                   │
                    └─────────┬─────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
                    ▼         ▼         ▼
                Kona 8   Kona 11   Kona 17
                发行版    发行版     发行版
```

#### 技术影响力指标

| 领域 | 直接影响 | 间接影响 | 影响范围 |
|------|----------|----------|----------|
| **G1 GC 优化** | 10+ PRs | 云原生用户 | 正确性修复 |
| **压缩指针** | 2 PRs | 64 位 JVM 用户 | 内存优化 |
| **容器检测** | 2+ PRs | 容器化部署 | 资源感知 |
| **Kona 发行版** | 4 版本 | 腾讯云服务 | 生产就绪 |

### 3.3 组织关系网络

```
                    腾讯组织关系图
                    
                    ┌──────────────────┐
                    │   Tencent        │
                    │   Shenzhen, CN   │
                    └────────┬─────────┘
                             │ Kona 团队
                    ┌────────┴─────────┐
                    │                  │
                    ▼                  ▼
            ┌──────────────┐   ┌──────────────┐
            │  G1 GC       │   │  容器化      │
            │  优化团队     │   │  支持团队    │
            └──────┬───────┘   └──────┬───────┘
                   │                  │
              ┌────┴────┐        ┌────┴────┐
              │         │        │         │
              ▼         ▼        ▼         ▼
         Tongbao   Luo      (其他)    (其他)
         Zhang    Chunyi    成员      成员
         (主导)   (主导)
```

### 3.4 协作深度分析

#### G1 GC 压缩指针边界修复协作网络

这是 Tongbao Zhang 主导的 G1 GC 正确性修复项目：

```
        G1 GC 压缩指针修复协作网络
        
              Tongbao Zhang
              (Author)
                   │
              ┌────┴────┐
              │         │
              ▼         ▼
        Thomas    Albert Mingkun
        Schatzl   Yang
        (G1 GC)   (G1 GC)
              │
              └────┬────┘
                   │
                   ▼
         JDK 21+ (正式版)
```

| 指标 | 数值 | 说明 |
|------|------|------|
| 开发周期 | 2021-2024 | 从提案到正式发布 |
| PR 数量 | 5 个 | G1 GC 修复 |
| 审查轮次 | 多轮 | 包含公开审查 |
| 影响范围 | G1 GC 用户 | JDK 21+ |

#### 与 Thomas Schatzl 的协作

| 指标 | 数值 | 说明 |
|------|------|------|
| 合作领域 | G1 GC | 垃圾收集器优化 |
| Thomas 角色 | Oracle G1 GC 专家 | 技术审查 |
| Tongbao 角色 | Tencent Kona 开发者 | G1 GC 修复 |
| 协作模式 | 审查指导 | Oracle → Tencent |

**Thomas Schatzl 背景**:
- Oracle Principal Engineer
- G1 GC 主要维护者
- GitHub: [@tschatzl](https://github.com/tschatzl)
- 546+ integrated PRs

### 3.5 技术社区参与

腾讯积极参与技术社区活动：

- **G1 GC 优化**: G1 GC 正确性修复主要贡献者
- **邮件列表**: 在 hotspot-gc-dev、hotspot-dev 邮件列表活跃
- **Kona 发行版**: 维护 Tencent Kona JDK 发行版 (8/11/17/21)

### 3.6 知识传承网络

```
                    腾讯知识传承

        前辈层                    同辈层                    后辈层
    ┌─────────────┐          ┌─────────────┐          ┌─────────────┐
    │ Thomas      │          │ Shaojin     │          │ 新贡献者    │
    │ Schatzl     │◄────────►│ Wen         │          │ (通过 PR    │
    │ (Oracle)    │  审查    │ (Alibaba)   │──交流──►│  学习)      │
    └─────────────┘          └─────────────┘          └──────┬──────┘
                                                              │
                                                              │
                                                              ▼
                    ┌─────────────────────────────────────────────────┐
                    │         Tongbao Zhang                            │
                    │         (知识枢纽)                               │
                    │         - G1 GC                                 │
                    │         - 压缩指针                              │
                    │         - 容器检测                              │
                    └─────────────────────────────────────────────────┘
                                                              │
                    ┌─────────────┐          ┌─────────────┐  │
                    │ Luo         │          │ 其他腾讯    │  │
                    │ Chunyi      │◄────────►│ 成员        │◄─┘
                    │ (G1 GC)     │  协作    │             │   协作
                    └─────────────┘          └─────────────┘
```

---

## 4. 主要领域

### G1 GC

- G1 垃圾收集器优化
- 压缩指针边界修复
- 对齐检查修复

### 容器化

- 容器资源检测
- Cgroup 支持

---

## 5. 关键贡献

| Issue | 标题 | 贡献者 | 说明 |
|-------|------|--------|------|
| 8354145 | G1 压缩指针边界计算修复 | [Tongbao Zhang](../../by-contributor/profiles/tongbao-zhang.md) | 正确性修复 |
| 8293782 | Shenandoah 锁排名检查修复 | [Tongbao Zhang](../../by-contributor/profiles/tongbao-zhang.md) | 测试修复 |
| 8274259 | G1 对齐检查修复 | [Tongbao Zhang](../../by-contributor/profiles/tongbao-zhang.md) | 正确性修复 |

---

## 6. 影响的模块

| 模块 | 文件数 | 说明 |
|------|--------|------|
| G1 GC | 5+ | G1 垃圾收集器 |
| Shenandoah GC | 2+ | Shenandoah 测试 |
| 容器检测 | 2+ | Cgroup 支持 |

---

## 7. Tencent Kona

腾讯维护自己的 JDK 发行版 Kona：

| 特性 | 说明 |
|------|------|
| 基于 | OpenJDK |
| 支持 | 长期支持版本 |
| 特点 | 云原生优化 |
| 许可 | GPLv2 |

**版本**: Kona 8 / 11 / 17 / 21

---

## 8. 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-21

---

## 9. 相关链接

- [Tencent Kona](https://github.com/Tencent/TencentKona-8)
- [腾讯云 Java](https://cloud.tencent.com/product/tke)

---

**文档版本**: 1.0
**最后更新**: 2026-03-21
**更新内容**:
- 新增多层网络分析章节 (6 个小节)
- 添加协作网络可视化图表
- 补充技术影响力网络分析 (4 大领域)
- 新增组织关系网络图 (腾讯 Kona 团队结构)
- 添加协作深度分析 (G1 GC 压缩指针修复案例)
- 新增知识传承网络分析

[→ 返回组织索引](../../by-contributor/index.md)
