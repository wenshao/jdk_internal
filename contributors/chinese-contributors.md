# 中国贡献者

> OpenJDK 历史上的中国开发者贡献 (JDK 8 - JDK 26)

---

## 概览

中国开发者在 OpenJDK 社区中做出了重要贡献，涵盖 GC、编译器、RISC-V、LoongArch、核心库、国际化等多个领域。

```
中国贡献者统计 (2007-2026)
├── Oracle: 4,500+ commits (中国团队成员)
├── 阿里巴巴: 72 commits
├── 龙芯: 52 commits
├── 腾讯: 44 commits
├── 海光: 60+ commits
├── 字节跳动: 12 commits
└── 总贡献者: 50+
```

> **数据来源**: OpenJDK git 仓库 `upstream_master` 分支
> **统计时间**: 2026-03-19

---

## 快速导航

| 页面 | 说明 |
|------|------|
| [阿里巴巴](orgs/alibaba.md) | 核心库优化 (72 commits) |
| [龙芯](orgs/loongson.md) | LoongArch (52 commits) |
| [腾讯](orgs/tencent.md) | G1 GC、容器 (44 commits) |
| [字节跳动](orgs/bytedance.md) | RISC-V (12 commits) |

---

## Oracle 中国团队成员

> 统计在 [Oracle](orgs/oracle.md) 组织中

| 排名 | 贡献者 | Commits | 主要领域 | 详情 |
|------|--------|---------|----------|------|
| 1 | Weijun Wang | 953 | 安全、工具、keytool | - |
| 2 | [Albert Mingkun Yang](albert-mingkun-yang.md) | 747 | GC (G1/Parallel) | [详情](albert-mingkun-yang.md) |
| 3 | Sundararajan Athijegannathan | 688 | Nashorn、脚本引擎 | - |
| 4 | Zhengyu Gu | 582 | G1 GC | - |
| 5 | [Naoto Sato](naoto-sato.md) | 569 | 国际化、Unicode | [详情](naoto-sato.md) |
| 6 | Xue-Lei Andrew Fan | 412 | 安全、加密 | - |
| 7 | [Hamlin Li](hamlin-li.md) | 301 | RISC-V | [详情](hamlin-li.md) |
| 8 | Jiangli Zhou | 251 | CDS、类共享 | - |
| 9 | Yasumasa Suenaga | 243 | HotSpot、JFR | - |
| 10 | [Chen Liang](chen-liang.md) | 211 | ClassFile API | [详情](chen-liang.md) |
| 11 | [SendaoYan](sendaoyan.md) | 182 | 测试稳定性 | [详情](sendaoyan.md) |
| 12 | Michael Fang | 155 | 国际化 | - |
| 13 | Suchen Chien | 148 | 安全 | - |
| 14 | [Fei Yang](fei-yang.md) | 116 | RISC-V | [详情](fei-yang.md) |

---

## 企业贡献者

### 阿里巴巴

👉 [查看完整详情](orgs/alibaba.md)

| 贡献者 | Commits | 主要领域 |
|--------|---------|----------|
| [Shaojin Wen](shaojin-wen.md) | 28 | 核心库优化、字符串处理 |
| [Kuai Wei](kuai-wei.md) | 13 | C2 编译器 |
| Yude Lin | 8 | 测试 |

**关键贡献**:
- 字符串拼接优化 (+15%)
- DateTime toString 优化 (+10%)
- C2 编译器 IR 修复

---

### 龙芯 (Loongson)

👉 [查看完整详情](orgs/loongson.md)

| 贡献者 | Commits | 主要领域 |
|--------|---------|----------|
| Guoyun Sun | 14 | 测试、文档 |
| Qi Ao | 11 | 测试、编译器 |
| Jie Fu | 6 | 测试 |

**关键贡献**:
- LoongArch Zero VM 支持
- 编译器正确性修复
- 测试稳定性改进

---

### 腾讯

👉 [查看完整详情](orgs/tencent.md)

| 贡献者 | Commits | 主要领域 |
|--------|---------|----------|
| Bob Peng Xie | 15 | 测试、构建 |
| Caspar Wang | 7 | 测试 |
| [Tongbao Zhang](tongbao-zhang.md) | 5 | G1 GC |

**关键贡献**:
- G1 压缩指针边界修复
- 容器资源检测修复
- 编译器崩溃修复

---

### 字节跳动 (ByteDance)

👉 [查看完整详情](orgs/bytedance.md)

| 贡献者 | Commits | 主要领域 |
|--------|---------|----------|
| [Anjian Wen](anjian-wen.md) | 12 | RISC-V 向量指令 |

**关键贡献**:
- RISC-V Zvbb 向量指令
- RISC-V Zfa 浮点指令
- 数组填充优化

---

### 海光 (Hygon)

| 贡献者 | Commits | 主要领域 |
|--------|---------|----------|
| SendaoYan | 56 | 测试稳定性 |

**关键贡献**:
- 虚拟线程测试修复
- 测试超时问题解决

---

### 华为

| 贡献者 | Commits | 主要领域 |
|--------|---------|----------|
| Dong Bo | 3 | 测试 |
| Dongbo He | 3 | 测试 |
| Huang Wang | 3 | 测试 |

---

### ISCAS (中科院软件所)

| 贡献者 | Commits | 主要领域 |
|--------|---------|----------|
| Dingli Zhang | 11 | RISC-V |
| Fei Yang | 6 | RISC-V |

---

## 按领域统计

### GC (垃圾收集)

| 贡献者 | Commits | 组织 | 领域 |
|--------|---------|------|------|
| [Albert Mingkun Yang](albert-mingkun-yang.md) | 747 | Oracle | G1/Parallel GC |
| Zhengyu Gu | 582 | Oracle | G1 GC |
| [Tongbao Zhang](tongbao-zhang.md) | 5 | 腾讯 | G1 GC |

### 编译器

| 贡献者 | Commits | 组织 | 领域 |
|--------|---------|------|------|
| [Kuai Wei](kuai-wei.md) | 13 | 阿里巴巴 | C2 编译器 |
| [Anjian Wen](anjian-wen.md) | 12 | 字节跳动 | RISC-V 后端 |
| Qi Ao | 11 | 龙芯 | C1/C2 |

### RISC-V

| 贡献者 | Commits | 组织 |
|--------|---------|------|
| [Hamlin Li](hamlin-li.md) | 301 | Oracle |
| [Anjian Wen](anjian-wen.md) | 12 | 字节跳动 |
| Dingli Zhang | 11 | ISCAS |
| [Fei Yang](fei-yang.md) | 116 | Oracle |

### LoongArch

| 贡献者 | Commits | 组织 |
|--------|---------|------|
| Guoyun Sun | 14 | 龙芯 |
| Qi Ao | 11 | 龙芯 |
| Jie Fu | 6 | 龙芯 |

### 核心库

| 贡献者 | Commits | 组织 |
|--------|---------|------|
| Weijun Wang | 953 | Oracle |
| [Shaojin Wen](shaojin-wen.md) | 27 | 阿里巴巴 |
| [Naoto Sato](naoto-sato.md) | 569 | Oracle |

### 安全

| 贡献者 | Commits | 组织 |
|--------|---------|------|
| Weijun Wang | 953 | Oracle |
| Xue-Lei Andrew Fan | 412 | Oracle |
| Suchen Chien | 148 | Oracle |

### 国际化

| 贡献者 | Commits | 组织 |
|--------|---------|------|
| [Naoto Sato](naoto-sato.md) | 569 | Oracle |
| Michael Fang | 155 | Oracle |

---

## 统计汇总

### 按组织

| 组织 | 贡献者数 | Commits | 详情 |
|------|----------|---------|------|
| Oracle (中国团队) | 14+ | 4,500+ | [详情](orgs/oracle.md) |
| 阿里巴巴 | 16 | 72 | [详情](orgs/alibaba.md) |
| 龙芯 | 9 | 52 | [详情](orgs/loongson.md) |
| 腾讯 | 13 | 44 | [详情](orgs/tencent.md) |
| 海光 | 2 | 60+ | - |
| 字节跳动 | 1 | 12 | [详情](orgs/bytedance.md) |
| 华为 | 4 | 11 | - |
| ISCAS | 2 | 17 | - |

### 按领域

| 领域 | Commits | 主要贡献者 |
|------|---------|-----------|
| 安全/工具 | 1,365 | Weijun Wang, Xue-Lei Andrew Fan |
| GC | 1,334 | Albert Mingkun Yang, Zhengyu Gu |
| 国际化 | 724 | Naoto Sato, Michael Fang |
| Nashorn | 688 | Sundararajan Athijegannathan |
| RISC-V | 429 | Hamlin Li, Anjian Wen |
| CDS | 251 | Jiangli Zhou |
| HotSpot | 243 | Yasumasa Suenaga |
| ClassFile API | 211 | Chen Liang |
| 核心库优化 | 27 | Shaojin Wen |
| LoongArch | 52 | 龙芯团队 |

---

## 相关链接

- [OpenJDK 中国社区](https://openjdk.org/groups/china/)
- [阿里巴巴 Dragonwell](https://github.com/alibaba/dragonwell8)
- [龙芯 JDK](https://github.com/loongson/jdk)
- [腾讯 Kona](https://github.com/Tencent/TencentKona-8)