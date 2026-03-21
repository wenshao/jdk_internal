# Alibaba Dragonwell JDK Team

> **Alibaba's OpenJDK Distribution** | **Shanghai/Hangzhou** | **JVM Team**

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **GitHub Org** | [@dragonwell-project](https://github.com/dragonwell-project) |
| **公司账号** | [@alijvm](../../by-contributor/profiles/alijvm.md) |
| **主要仓库** | [dragonwell8](https://github.com/dragonwell-project/dragonwell8), [dragonwell11](https://github.com/dragonwell-project/dragonwell11), [dragonwell21](https://github.com/dragonwell-project/dragonwell21) |
| **官网** | https://dragonwell-jdk.io/ |
| **主要领域** | JVM, JDK 发行版，性能优化 |

---

## 多层网络分析

### 协作网络 (Co-authorship Network)

基于 Dragonwell 团队的协作关系分析：

```
                          Dragonwell 协作网络图
                          
                    ┌─────────────────────────────┐
                    │    Alibaba Dragonwell        │
                    │   Shanghai/Hangzhou JVM      │
                    └─────────────┬───────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
          ▼                       ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │ 核心团队  │           │ 技术社区  │           │ 行业合作  │
    │  (内部)   │           │  (外部)   │           │  (外部)   │
    └────┬─────┘           └────┬─────┘           └────┬─────┘
         │                      │                      │
    ┌────┴────┐           ┌────┴────┐           ┌────┴────┐
    │Kuai     │           │Jonathan │           │Leslie   │
    │Wei      │           │Lu       │           │Zhai     │
    │(13 PRs) │           │(上海)   │           │(龙芯)   │
    │         │           │         │           │         │
    │Sendaoyan│           │Hao Tang │           │         │
    │Yan      │           │(ByteD.) │           │         │
    │(测试)   │           │(杭州)   │           │         │
    └─────────┘           └─────────┘           └─────────┘
```

#### 核心团队 (Alibaba 内部)

| 贡献者 | 组织 | PRs | 主要领域 | 角色 |
|--------|------|-----|----------|------|
| [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) | Alibaba | 13 | C2 编译器，RISC-V | C2 编译器专家 |
| [Sendaoyan Yan](../../by-contributor/profiles/sendaoyan.md) | Alibaba | - | 编译器测试 | Compiler Tester |
| [Long Yang](../../by-contributor/profiles/yanglong1010.md) | Alibaba | - | JVM, GC | JVM 团队 |

#### 技术社区 (外部合作)

| 贡献者 | 组织 | 位置 | 关系类型 |
|--------|------|------|----------|
| [Jonathan Lu](../../by-contributor/profiles/luchsh.md) | JVM 社区 | 上海 | 技术同行 |
| [Hao Tang](../../by-contributor/profiles/tanghaoth90.md) | ByteDance | 杭州 | 技术同行 |
| [shako](../../by-contributor/profiles/xhao.md) | JVM 社区 | 上海 | 技术同行 |
| [WenjunMin](../../by-contributor/profiles/aitozi.md) | JVM 社区 | - | 技术同行 |

#### 行业合作 (外部合作)

| 贡献者 | 组织 | 位置 | 合作领域 |
|--------|------|------|----------|
| [Leslie Zhai](../../by-contributor/profiles/xiangzhai.md) | Loongson | 北京 | RISC-V/LoongArch |

### 技术影响力网络

```
                    Dragonwell 技术影响力辐射图
                    
                         C2 编译器
                              │
                    ┌─────────┼─────────┐
                    │         │         │
                    ▼         ▼         ▼
               IR 框架   内存屏障   RISC-V
                    │         │         │
                    └─────────┼─────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
              电商优化           金融优化
              (Dragonwell 8)    (Dragonwell 11)
                    │                   │
                    └─────────┬─────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
                    ▼         ▼         ▼
                性能优化   GC 调优    测试框架
```

#### 技术影响力指标

| 领域 | 直接影响 | 间接影响 | 影响范围 |
|------|----------|----------|----------|
| **C2 编译器** | 13 PRs | 电商/金融用户 | 性能优化 |
| **RISC-V 支持** | 5+ PRs | RISC-V 服务器 | 架构移植 |
| **内存屏障** | 3+ PRs | 所有 Dragonwell 用户 | 正确性 |
| **编译器测试** | 测试框架 | JDK 测试 | 质量保证 |

### 组织关系网络

```
                    Dragonwell 组织关系图
                    
                    ┌──────────────────┐
                    │   Alibaba        │
                    │ (Shanghai/       │
                    │  Hangzhou)       │
                    └────────┬─────────┘
                             │ Dragonwell 团队
                    ┌────────┴─────────┐
                    │                  │
                    ▼                  ▼
            ┌──────────────┐   ┌──────────────┐
            │  JVM 团队     │   │  技术社区    │
            │              │   │              │
            └──────┬───────┘   └──────┬───────┘
                   │                  │
              ┌────┴────┐        ┌────┴────┐
              │         │        │         │
              ▼         ▼        ▼         ▼
         Kuai     Sendaoyan  Jonathan  Hao Tang
         Wei      Yan        Lu        (ByteDance)
         (C2)     (测试)     (上海)    
```

### 协作深度分析

#### C2 编译器优化协作网络

这是 Kuai Wei 主导的 C2 编译器优化项目：

```
        C2 编译器优化协作网络
        
              Kuai Wei
              (Author)
                   │
              ┌────┴────┐
              │         │
              ▼         ▼
        Sendaoyan  Long Yang
        Yan        (Alibaba)
        (测试)     (GC)
              │
              └────┬────┘
                   │
                   ▼
         Dragonwell 8/11/21
```

| 指标 | 数值 | 说明 |
|------|------|------|
| 开发周期 | 2018-2026 | 持续优化 |
| PR 数量 | 13 个 | C2 编译器 |
| 影响范围 | Dragonwell 用户 | 电商/金融场景 |

#### 与 Sendaoyan Yan 的协作

| 指标 | 数值 | 说明 |
|------|------|------|
| 合作领域 | 编译器测试 | 质量保证 |
| Kuai 角色 | C2 编译器专家 | 优化实现 |
| Sendaoyan 角色 | Compiler Tester | 测试框架 |
| 协作模式 | 实现 + 测试 | 内部协作 |

**Sendaoyan Yan 背景**:
- Alibaba Compiler Tester
- 上海
- 专注于编译器测试框架

### 技术社区参与

Dragonwell 团队积极参与技术社区活动：

- **C2 编译器优化**: Kuai Wei 主导的持续优化项目
- **学术论文**: ASE 2021 "Towards a Serverless Java Runtime"
- **邮件列表**: 在 compiler-dev、hotspot-dev 邮件列表活跃
- **开源贡献**: Dragonwell JDK 发行版维护

### 知识传承网络

```
                    Dragonwell 知识传承

        前辈层                    同辈层                    后辈层
    ┌─────────────┐          ┌─────────────┐          ┌─────────────┐
    │ Kuai        │          │ Sendaoyan   │          │ 新贡献者    │
    │ Wei         │◄────────►│ Yan         │          │ (通过 PR    │
    │ (C2 专家)   │  协作    │ (测试)      │──协作──►│  学习)      │
    └─────────────┘          └─────────────┘          └──────┬──────┘
                                                              │
                                                              │
                                                              ▼
                    ┌─────────────────────────────────────────────────┐
                    │         Dragonwell 团队                          │
                    │         (知识枢纽)                               │
                    │         - C2 编译器                             │
                    │         - RISC-V                                │
                    │         - 电商/金融优化                         │
                    └─────────────────────────────────────────────────┘
                                                              │
                    ┌─────────────┐          ┌─────────────┐  │
                    │ Jonathan    │          │ Long        │  │
                    │ Lu          │◄────────►│ Yang        │◄─┘
                    │ (上海)      │  协作    │ (GC)        │   协作
                    └─────────────┘          └─────────────┘
```

---


## Dragonwell JDK 版本

| 版本 | 基础 JDK | Stars | Forks | 说明 |
|------|----------|-------|-------|------|
| **Dragonwell 8** | OpenJDK 8 | 4,318 | 501 | LTS，电商优化 |
| **Dragonwell 11** | OpenJDK 11 | 584 | 118 | LTS，金融优化 |
| **Dragonwell 17** | OpenJDK 17 | 337 | 49 | LTS |
| **Dragonwell 21** | OpenJDK 21 | 134 | 28 | LTS |
| **Dragonwell 25** | OpenJDK 25 | 13 | 3 | 最新版本 |

---

## 核心团队成员

### JVM 团队核心

| 成员 | GitHub | 位置 | 角色 |
|------|--------|------|------|
| **Sanhong Li** | [sanhong](../../by-contributor/profiles/sanhong.md), [alijvm](../../by-contributor/profiles/alijvm.md) | - | ASE 2021 论文作者，JVM 团队 |
| **Kuai Wei** | [kuaiwei](../../by-contributor/profiles/kuai-wei.md) | 上海/杭州 | C2 编译器专家 |
| **Long Yang** | [yanglong1010](../../by-contributor/profiles/yanglong1010.md) | 杭州 | JVM 团队 |
| **Sendaoyan Yan** | [sendaoyan](../../by-contributor/profiles/sendaoyan.md) | 上海 | Compiler Tester |
| **Joshua Zhu** | [joshua-zhu](../../by-contributor/profiles/joshua-zhu.md) | 上海 | JVM 团队 |

### 技术社区联系

| 成员 | GitHub | 位置 | 组织 |
|------|--------|------|------|
| **Jonathan Lu** | [luchsh](../../by-contributor/profiles/luchsh.md) | 上海 | JVM 社区 |
| **Hao Tang** | [tanghaoth90](../../by-contributor/profiles/tanghaoth90.md) | 杭州 | ByteDance |
| **shako** | [xhao](../../by-contributor/profiles/xhao.md) | 上海 | JVM 社区 |
| **WenjunMin** | [aitozi](../../by-contributor/profiles/aitozi.md) | - | JVM 社区 |

### 行业合作

| 成员 | GitHub | 位置 | 组织 |
|------|--------|------|------|
| **Leslie Zhai** | [xiangzhai](../../by-contributor/profiles/xiangzhai.md) | 北京 | 龙芯 (Loongson) |

---

## 技术方向

### 核心优化领域

| 领域 | 说明 | 代表贡献者 |
|------|------|------------|
| **C2 编译器** | JIT 编译器优化 | [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) |
| **GC 优化** | G1, ZGC 调优 | [Long Yang](../../by-contributor/profiles/yanglong1010.md) |
| **性能优化** | 电商场景优化 | JVM 团队 |
| **编译器测试** | 测试框架 | [Sendaoyan Yan](../../by-contributor/profiles/sendaoyan.md) |
| **RISC-V/LoongArch** | 架构移植 | [Leslie Zhai](../../by-contributor/profiles/xiangzhai.md) |

### 学术论文

**ASE 2021**: "Towards a Serverless Java Runtime"
- **作者**: Yifei Zhang, Tianxiao Gu, Xiaolin Zheng, Lei Yu, **Wei Kuai**, **Sanhong Li**
- **单位**: Alibaba Group
- **DBLP**: [记录](https://dblp.org/rec/conf/kbse/0001GZYKL21)

---

## 社交网络分析

### 地理位置分布

| 城市 | 人数 | 组织 |
|------|------|------|
| **上海** | 4 | Alibaba (2), JVM 社区 (2) |
| **杭州** | 2 | Alibaba (1), ByteDance (1) |
| **北京** | 1 | Loongson (1) |

### 行业联系

| 类型 | 组织 | 联系人 |
|------|------|--------|
| **龙芯** | Loongson | [Leslie Zhai](../../by-contributor/profiles/xiangzhai.md) |
| **字节跳动** | ByteDance | [Hao Tang](../../by-contributor/profiles/tanghaoth90.md) |
| **JDK 社区** | JRuby | [Charles Nutter](../../by-contributor/profiles/headius.md) |

---

## OpenJDK 贡献

### Integrated PRs 统计

| 贡献者 | PRs | 主要领域 |
|--------|-----|----------|
| [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) | 13 | C2 IR, RISC-V, 内存屏障 |
| [Long Yang](../../by-contributor/profiles/yanglong1010.md) | - | JVM, 核心库 |
| [Sendaoyan Yan](../../by-contributor/profiles/sendaoyan.md) | - | 编译器测试 |

### 贡献时间线

| 年份 | 贡献者 | 主要工作 |
|------|--------|----------|
| 2018 | Kuai Wei | C2 后屏障优化 |
| 2020 | Kuai Wei | AArch64 r27 分配 |
| 2021 | Kuai Wei | RISC-V OpenJDK, handle split_USE |
| 2024 | Kuai Wei | C2 IR 优化，release barrier |
| 2025 | Kuai Wei | C2 IR, Windows devkit |
| 2026 | Kuai Wei | Jeandle JIT 编译器 |

---

## 外部链接

| 类型 | 链接 |
|------|------|
| **Dragonwell 官网** | https://dragonwell-jdk.io/ |
| **GitHub Org** | https://github.com/dragonwell-project |
| **Dragonwell 8** | https://github.com/dragonwell-project/dragonwell8 |
| **Dragonwell 11** | https://github.com/dragonwell-project/dragonwell11 |
| **Dragonwell 21** | https://github.com/dragonwell-project/dragonwell21 |

---

## 相关文档

### 团队成员
- [Sanhong Li](../../by-contributor/profiles/sanhong.md) - ASE 2021 论文作者
- [Kuai Wei](../../by-contributor/profiles/kuai-wei.md) - C2 编译器专家
- [Long Yang](../../by-contributor/profiles/yanglong1010.md) - JVM 团队，杭州
- [Sendaoyan Yan](../../by-contributor/profiles/sendaoyan.md) - 编译器测试工程师
- [Joshua Zhu](../../by-contributor/profiles/joshua-zhu.md) - 上海团队

### 技术社区
- [Jonathan Lu](../../by-contributor/profiles/luchsh.md) - 上海 JVM 社区
- [Hao Tang](../../by-contributor/profiles/tanghaoth90.md) - ByteDance，杭州
- [shako](../../by-contributor/profiles/xhao.md) - 上海 JVM 社区
- [WenjunMin](../../by-contributor/profiles/aitozi.md) - JVM 社区
- [Leslie Zhai](../../by-contributor/profiles/xiangzhai.md) - 龙芯，北京
- [Charles Nutter](../../by-contributor/profiles/headius.md) - JRuby 创始人

### 组织
- [Alibaba](alibaba.md) - 阿里巴巴贡献者
- [中国贡献者](../../by-contributor/profiles/chinese-contributors.md) - 中国 OpenJDK 贡献者

---

**文档版本**: 1.0
**最后更新**: 2026-03-21
**更新内容**:
- 新增多层网络分析章节 (6 个小节)
- 添加协作网络可视化图表
- 补充技术影响力网络分析 (4 大领域)
- 新增组织关系网络图 (Dragonwell 团队结构)
- 添加协作深度分析 (C2 编译器优化案例)
- 新增知识传承网络分析
