# 中国贡献者

> OpenJDK 历史上的中国开发者贡献 (JDK 8 - JDK 26)

---

## 概览

中国开发者在 OpenJDK 社区中做出了重要贡献，涵盖 GC、编译器、RISC-V、核心库、国际化等多个领域。

> **数据来源**: OpenJDK git 仓库 `upstream_master` 分支  
> **统计时间**: 2026-03-19

---

## Oracle 中国团队

> Oracle 中国研发中心的贡献者，是 OpenJDK 中国贡献的主力军

| 贡献者 | Commits | 主要领域 | 详情 |
|--------|---------|----------|------|
| Weijun Wang | 954 | 安全、工具、keytool | - |
| [Albert Mingkun Yang](albert-mingkun-yang.md) | 747 | GC (G1/Parallel) | [查看详情](albert-mingkun-yang.md) |
| Sundararajan Athijegannathan | 689 | Nashorn、脚本引擎 | - |
| Zhengyu Gu | 582 | G1 GC | - |
| Naoto Sato | 569 | 国际化、Unicode | - |
| Xue-Lei Andrew Fan | 412 | 安全、加密 | - |
| Hamlin Li | 301 | RISC-V | - |
| Jiangli Zhou | 251 | CDS、类共享 | - |
| Yasumasa Suenaga | 243 | HotSpot、JFR | - |
| [SendaoYan](sendaoyan.md) | 56 | 测试稳定性 | [查看详情](sendaoyan.md) |
| [Chen Liang](chen-liang.md) | 36 | ClassFile API | [查看详情](chen-liang.md) |

---

## 企业贡献者

### 阿里巴巴

| 贡献者 | Commits | 主要领域 |
|--------|---------|----------|
| Shaojin Wen | 27 | 核心库优化、字符串处理 |
| Kuai Wei | 13 | C2 编译器 |
| Yude Lin | 8 | 测试 |
| Xiaowei Lu | 3 | 测试 |
| Zhuo Wang | 3 | 测试 |

**关键贡献**:
- StringBuilder 性能优化 (+15%)
- Integer/Long.toString 优化 (+10%)
- C2 编译器 IR 优化

### 龙芯 (Loongson)

| 贡献者 | Commits | 主要领域 |
|--------|---------|----------|
| sunguoyun | 14 | LoongArch 移植 |
| Ao Qi | 11 | LoongArch 移植 |
| Jie Fu | 6 | LoongArch 移植 |
| sunyaqi | 4 | LoongArch 移植 |
| Jia Huang | 3 | LoongArch 移植 |
| Wang Haomin | 3 | LoongArch 移植 |

**关键贡献**:
- LoongArch 架构移植
- LoongArch 指令集支持

### 腾讯

| 贡献者 | Commits | 主要领域 |
|--------|---------|----------|
| bobpengxie | 15 | 测试、构建 |
| casparcwang | 7 | 测试 |
| Tongbao Zhang | 5 | G1 GC |
| miao zheng | 4 | 测试 |
| Junji Wang | 2 | 测试 |

**关键贡献**:
- G1 GC 压缩指针边界修复
- 测试稳定性改进

### 字节跳动 (ByteDance)

| 贡献者 | Commits | 主要领域 |
|--------|---------|----------|
| Anjian-Wen | 12 | RISC-V 向量指令 |

**关键贡献**:
- RISC-V Zvbb 向量指令支持
- RISC-V Zfa 浮点指令

### 华为

| 贡献者 | Commits | 主要领域 |
|--------|---------|----------|
| Dong Bo | 6 | 测试 |
| Huang Wang | 3 | 测试 |

### ISCAS (中科院软件所)

| 贡献者 | Commits | 主要领域 |
|--------|---------|----------|
| Dingli Zhang | 11 | RISC-V |
| Fei Yang | 6 | RISC-V |

---

## 个人贡献者

### Yasumasa Suenaga

| 属性 | 值 |
|------|-----|
| **Commits** | 243 |
| **主要领域** | HotSpot、JFR、AArch64 |
| **组织** | 个人贡献者 |

**关键贡献**:
- JFR 事件改进
- AArch64 移植
- HotSpot 调试支持

---

## 按领域统计

### GC

| 贡献者 | Commits | 组织 |
|--------|---------|------|
| [Albert Mingkun Yang](albert-mingkun-yang.md) | 747 | Oracle |
| Zhengyu Gu | 582 | Oracle |
| Tongbao Zhang | 5 | 腾讯 |

### 编译器

| 贡献者 | Commits | 组织 |
|--------|---------|------|
| Kuai Wei | 13 | 阿里巴巴 |
| Anjian-Wen | 12 | 字节跳动 |

### RISC-V

| 贡献者 | Commits | 组织 |
|--------|---------|------|
| Hamlin Li | 301 | Oracle |
| Dingli Zhang | 11 | ISCAS |
| Anjian-Wen | 12 | 字节跳动 |
| Fei Yang | 6 | ISCAS |

### LoongArch

| 贡献者 | Commits | 组织 |
|--------|---------|------|
| sunguoyun | 14 | 龙芯 |
| Ao Qi | 11 | 龙芯 |
| Jie Fu | 6 | 龙芯 |

### 核心库

| 贡献者 | Commits | 组织 |
|--------|---------|------|
| Shaojin Wen | 27 | 阿里巴巴 |
| Weijun Wang | 954 | Oracle |
| Naoto Sato | 569 | Oracle |

### 国际化

| 贡献者 | Commits | 组织 |
|--------|---------|------|
| Naoto Sato | 569 | Oracle |

### 安全

| 贡献者 | Commits | 组织 |
|--------|---------|------|
| Weijun Wang | 954 | Oracle |
| Xue-Lei Andrew Fan | 412 | Oracle |

---

## 统计汇总

### 按组织

| 组织 | 贡献者数 | Commits |
|------|----------|---------|
| Oracle 中国 | 11+ | 4,000+ |
| 阿里巴巴 | 5+ | 50+ |
| 龙芯 | 6+ | 40+ |
| 腾讯 | 5+ | 30+ |
| 字节跳动 | 1 | 12 |
| 华为 | 2 | 9 |
| ISCAS | 2 | 17 |

### 按领域

| 领域 | Commits | 主要贡献者 |
|------|---------|-----------|
| 安全/工具 | 1,366 | Weijun Wang, Xue-Lei Andrew Fan |
| GC | 1,334 | Albert Mingkun Yang, Zhengyu Gu |
| 国际化 | 569 | Naoto Sato |
| Nashorn | 689 | Sundararajan Athijegannathan |
| RISC-V | 330+ | Hamlin Li, Anjian-Wen, Dingli Zhang |
| CDS | 251 | Jiangli Zhou |
| HotSpot | 243 | Yasumasa Suenaga |
| 核心库优化 | 27 | Shaojin Wen |
| LoongArch | 40+ | 龙芯团队 |

---

## 相关链接

- [OpenJDK 中国社区](https://openjdk.org/groups/china/)
- [Loongson JDK](https://github.com/loongson/jdk)
- [Alibaba Dragonwell](https://github.com/alibaba/dragonwell8)