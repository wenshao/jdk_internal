# 中国企业

> 阿里巴巴、龙芯、腾讯、字节跳动等中国企业的 OpenJDK 贡献

---

## 概览

中国企业在 OpenJDK 社区的贡献日益增长，涵盖核心库优化、RISC-V、LoongArch 等领域。

| 组织 | Commits | 主要领域 |
|------|---------|----------|
| 阿里巴巴 | 50+ | 核心库优化 |
| 龙芯 | 40+ | LoongArch |
| 腾讯 | 30+ | 测试、GC |
| 字节跳动 | 12 | RISC-V |
| 华为 | 10+ | 测试 |
| 海光 | 60+ | 测试稳定性 |

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

### 概览

| 指标 | 值 |
|------|-----|
| **Commits** | 50+ |
| **贡献者** | 5+ |
| **主要领域** | 核心库、C2 编译器 |

### 影响的模块

| 模块 | 文件数 | 说明 |
|------|--------|------|
| java.lang | 23 | 核心类库 |
| C2 编译器 | 31 | 编译器优化 |
| java.util | 14 | 集合框架 |
| java.text | 14 | 文本处理 |

### Top 贡献者

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| Shaojin Wen | 27 | 核心库优化 |
| Kuai Wei | 13 | C2 编译器 |
| Yude Lin | 8 | 测试 |

### 关键贡献

| Issue | 标题 | 性能影响 |
|-------|------|----------|
| 8355177 | StringBuilder::append(char[]) 优化 | +15% |
| 8370503 | Integer/Long.toString 简化 | +10% |
| 8349400 | 消除嵌套类提升启动速度 | +5% |
| 8356328 | C2 IR 节点 size_of() | - |

### 相关项目

- [Alibaba Dragonwell](https://github.com/alibaba/dragonwell8) - 阿里巴巴 JDK 发行版

---

## 龙芯 (Loongson)

> LoongArch 架构移植

### 概览

| 指标 | 值 |
|------|-----|
| **Commits** | 40+ |
| **贡献者** | 6+ |
| **主要领域** | LoongArch 移植 |

### Top 贡献者

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| sunguoyun | 14 | LoongArch |
| Ao Qi | 11 | LoongArch |
| Jie Fu | 6 | LoongArch |
| sunyaqi | 4 | LoongArch |

### 关键贡献

- **LoongArch 架构移植**: 完整的 CPU 移植
- **LoongArch 指令集**: 汇编代码和 JIT 支持
- **构建系统**: LoongArch 平台构建配置

### 相关项目

- [Loongson JDK](https://github.com/loongson/jdk) - 龙芯 JDK 发行版

---

## 腾讯 (Tencent)

> 测试和 GC 优化

### 概览

| 指标 | 值 |
|------|-----|
| **Commits** | 30+ |
| **贡献者** | 5+ |
| **主要领域** | 测试、GC |

### Top 贡献者

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| bobpengxie | 15 | 测试、构建 |
| casparcwang | 7 | 测试 |
| Tongbao Zhang | 5 | G1 GC |
| miao zheng | 4 | 测试 |

### 关键贡献

| Issue | 标题 | 说明 |
|-------|------|------|
| 8354145 | G1 压缩指针边界计算修复 | G1 GC 正确性修复 |

---

## 字节跳动 (ByteDance)

> RISC-V 向量指令

### 概览

| 指标 | 值 |
|------|-----|
| **Commits** | 12 |
| **贡献者** | 1 |
| **主要领域** | RISC-V |

### 贡献者

| 贡献者 | Commits | 领域 |
|--------|---------|------|
| Anjian-Wen | 12 | RISC-V 向量指令 |

### 关键贡献

| Issue | 标题 | 说明 |
|-------|------|------|
| 8329887 | RISC-V Zvbb 向量指令 | 向量 And-Not 指令 |
| 8349632 | RISC-V Zfa 浮点指令 | fminm/fmaxm |
| 8351140 | RISC-V Unsafe::setMemory | 内存操作 intrinsic |

---

## 海光 (Hygon)

> 测试稳定性

### 概览

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

- [Alibaba Dragonwell](https://github.com/alibaba/dragonwell8)
- [Loongson JDK](https://github.com/loongson/jdk)
- [OpenJDK 中国社区](https://openjdk.org/groups/china/)