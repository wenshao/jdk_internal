# 中国企业

> 阿里巴巴、腾讯、字节跳动、龙芯等中国企业的 OpenJDK 贡献

---

## 概览

中国企业在 OpenJDK 社区的贡献日益增长，涵盖核心库优化、RISC-V、LoongArch 等领域。

| 组织 | Commits | 主要领域 | 详情 |
|------|---------|----------|------|
| [阿里巴巴](alibaba.md) | 72 | 核心库优化 | [查看详情](alibaba.md) |
| [腾讯](tencent.md) | 44 | G1 GC, 容器 | [查看详情](tencent.md) |
| [龙芯](loongson.md) | 52 | LoongArch | [查看详情](loongson.md) |
| [字节跳动](bytedance.md) | 12 | RISC-V | [查看详情](bytedance.md) |
| [海光](#海光-hygon) | 60+ | 测试稳定性 | - |
| [华为](#华为-huawei) | 10+ | 测试 | - |
| [ISCAS](#iscas-中科院软件所) | 17+ | RISC-V | - |

---

## 影响的模块分布

基于 git 修改文件统计：

| 模块 | 文件数 | 主要贡献者 |
|------|--------|-----------|
| AArch64 移植 | 39 | 龙芯、华为 |
| RISC-V 移植 | 32 | 字节跳动、ISCAS |
| C2 编译器 | 31 | 阿里巴巴、字节跳动 |
| java.lang | 23 | 阿里巴巴 |
| G1 GC | 18 | 腾讯、阿里巴巴 |
| java.util | 14 | 阿里巴巴 |
| java.text | 14 | 阿里巴巴 |

---

## 阿里巴巴

> 核心库性能优化

👉 [查看完整详情](alibaba.md)

| 指标 | 值 |
|------|-----|
| **Commits** | 72 |
| **贡献者** | 16 |
| **主要领域** | 核心库、C2 编译器 |

### Top 贡献者

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| [Shaojin Wen](../shaojin-wen.md) | 28 | 核心库优化 |
| [Kuai Wei](../kuai-wei.md) | 13 | C2 编译器 |
| Yude Lin | 8 | 测试 |

### 关键贡献

- 字符串拼接优化 (+15%)
- DateTime toString 优化 (+10%)
- C2 IR 节点修复

---

## 腾讯

> G1 GC 优化和容器支持

👉 [查看完整详情](tencent.md)

| 指标 | 值 |
|------|-----|
| **Commits** | 44 |
| **贡献者** | 13 |
| **主要领域** | G1 GC、容器 |

### Top 贡献者

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| Bob Peng Xie | 15 | 测试、构建 |
| Caspar Wang | 7 | 测试 |
| [Tongbao Zhang](../tongbao-zhang.md) | 5 | G1 GC |

### 关键贡献

- G1 压缩指针边界修复
- 容器资源检测修复
- 编译器崩溃修复

---

## 字节跳动

> RISC-V 向量指令支持

👉 [查看完整详情](bytedance.md)

| 指标 | 值 |
|------|-----|
| **Commits** | 12 |
| **贡献者** | 1 |
| **主要领域** | RISC-V |

### 贡献者

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| [Anjian Wen](../anjian-wen.md) | 12 | RISC-V 向量指令 |

### 关键贡献

- RISC-V Zvbb 向量指令
- RISC-V Zfa 浮点指令
- 数组填充优化

---

## 龙芯 (Loongson)

> LoongArch 架构支持和测试修复

👉 [查看完整详情](loongson.md)

| 指标 | 值 |
|------|-----|
| **Commits** | 52 |
| **贡献者** | 9 |
| **主要领域** | LoongArch、测试 |

### Top 贡献者

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| Guoyun Sun | 14 | 测试、文档 |
| Qi Ao | 11 | 测试、编译器 |
| Jie Fu | 8 | 测试 |

### 关键贡献

- LoongArch Zero VM 支持
- 编译器正确性修复
- 测试稳定性改进

---

## 海光 (Hygon)

> 测试稳定性

| 指标 | 值 |
|------|-----|
| **Commits** | 60+ |
| **贡献者** | 2+ |
| **主要领域** | 测试稳定性 |

### Top 贡献者

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| SendaoYan | 56 | 测试稳定性 |

### 关键贡献

- 虚拟线程测试修复
- 测试超时问题解决
- 测试环境兼容性

---

## 华为 (Huawei)

> 测试和兼容性

### Top 贡献者

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| Dong Bo | 6 | 测试 |
| Huang Wang | 3 | 测试 |

---

## ISCAS (中科院软件所)

> RISC-V 移植

### Top 贡献者

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| Dingli Zhang | 11 | RISC-V |
| Fei Yang | 6 | RISC-V |

---

## 数据来源

- **统计方法**: `git log upstream_master --author="alibaba|tencent|loongson|bytedance|hygon|iscas|huawei"`
- **模块分析**: 基于修改文件路径统计

---

## 相关链接

- [阿里巴巴 Dragonwell](https://github.com/alibaba/dragonwell8)
- [龙芯 JDK](https://github.com/loongson/jdk)
- [腾讯 Kona](https://github.com/Tencent/TencentKona-8)
- [OpenJDK 中国社区](https://openjdk.org/groups/china/)