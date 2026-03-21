# Alibaba Dragonwell JDK

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

## OpenJDK 上游贡献

> **注**: 详细的 OpenJDK 贡献统计请查看 [Alibaba 组织页面](alibaba.md)

### 主要贡献者

| 贡献者 | OpenJDK PRs | 主要领域 |
|--------|-------------|----------|
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
- [Alibaba OpenJDK 贡献](alibaba.md) - 阿里巴巴 OpenJDK 上游贡献统计
- [中国贡献者](../../by-contributor/profiles/chinese-contributors.md) - 中国 OpenJDK 贡献者

---

**文档版本**: 2.0
**最后更新**: 2026-03-21
**更新内容**:
- 删除重复的社交网络分析图表
- 简化为团队介绍和 Dragonwell 发行版信息
- 添加指向 Alibaba OpenJDK 贡献页面的链接
- 聚焦 Dragonwell 发行版本身
