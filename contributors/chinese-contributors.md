# 中国贡献者

> OpenJDK 历史上的中国开发者贡献 (JDK 8 - JDK 26)

---

## 概览

中国开发者在 OpenJDK 社区中做出了重要贡献，涵盖 GC、编译器、RISC-V、LoongArch、核心库、国际化等多个领域。

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。查询方式：`repo:openjdk/jdk author:xxx type:pr label:integrated`

---

## Oracle 中国团队

> 统计在 [Oracle](orgs/oracle.md) 组织中

| 排名 | 贡献者 | GitHub | PRs | 主要领域 |
|------|--------|--------|-----|----------|
| 1 | Albert Mingkun Yang | [@albertnetymk](https://github.com/albertnetymk) | 744 | GC |
| 2 | Naoto Sato | [@naotoj](https://github.com/naotoj) | 273 | 国际化 |
| 3 | [Chen Liang](chen-liang.md) | [@liach](https://github.com/liach) | 237 | ClassFile API |
| 4 | Sendao Yan | [@sendaoYan](https://github.com/sendaoYan) | 202 | 测试稳定性 |
| 5 | Yasumasa Suenaga | [@YaSuenag](https://github.com/YaSuenag) | 113 | HotSpot |
| 6 | [Hamlin Li](hamlin-li.md) | [@merykitty](https://github.com/merykitty) | 74 | RISC-V |

**小计**: 1,643 PRs

---

## 中国企业

### 阿里巴巴

👉 [查看完整详情](orgs/alibaba.md)

| 贡献者 | GitHub | PRs | 主要领域 |
|--------|--------|-----|----------|
| [Shaojin Wen](shaojin-wen.md) | [@wenshao](https://github.com/wenshao) | 97 | 核心库优化 |
| [Kuai Wei](kuai-wei.md) | [@kuaiwei](https://github.com/kuaiwei) | 13 | C2 编译器 |
| [Yude Lin](yude-lin.md) | [@linade](https://github.com/linade) | 8 | G1 GC, AArch64 |
| [Xiaowei Lu](xiaowei-lu.md) | [@weixlu](https://github.com/weixlu) | 3 | ZGC |

**小计**: 121 PRs

**关键贡献**:
- 字符串拼接优化 (+10%)
- DateTime toString 优化 (+10%)
- G1 GC 监控增强
- ZGC 性能优化

---

### 字节跳动

👉 [查看完整详情](orgs/bytedance.md)

| 贡献者 | GitHub | PRs | 主要领域 |
|--------|--------|-----|----------|
| [Anjian Wen](anjian-wen.md) | [@Anjian-Wen](https://github.com/Anjian-Wen) | 25 | RISC-V 向量指令 |

**小计**: 25 PRs

**关键贡献**:
- RISC-V Zvbb 向量指令
- RISC-V Zfa 浮点指令
- 数组填充优化

---

### 龙芯

👉 [查看完整详情](orgs/loongson.md)

**关键贡献**:
- LoongArch Zero VM 支持
- 编译器正确性修复

---

### 腾讯

👉 [查看完整详情](orgs/tencent.md)

**关键贡献**:
- G1 压缩指针边界修复
- 容器资源检测修复

---

### ISCAS (中科院软件所)

| 贡献者 | GitHub | PRs | 主要领域 |
|--------|--------|-----|----------|
| Dingli Zhang | [@DingliZhang](https://github.com/DingliZhang) | 53 | RISC-V |

---

## 按领域统计

### GC (垃圾收集)

| 贡献者 | PRs | 组织 | 领域 |
|--------|-----|------|------|
| Albert Mingkun Yang | 744 | Oracle | G1/Parallel GC |
| Yude Lin | 8 | 阿里巴巴 | G1 GC |
| Xiaowei Lu | 3 | 阿里巴巴 | ZGC |

### 编译器

| 贡献者 | PRs | 组织 | 领域 |
|--------|-----|------|------|
| Kuai Wei | 13 | 阿里巴巴 | C2 编译器 |
| Anjian Wen | 25 | 字节跳动 | RISC-V 后端 |

### RISC-V

| 贡献者 | PRs | 组织 |
|--------|-----|------|
| Hamlin Li | 74 | Oracle |
| Anjian Wen | 25 | 字节跳动 |
| Dingli Zhang | 53 | ISCAS |

### 核心库

| 贡献者 | PRs | 组织 |
|--------|-----|------|
| Shaojin Wen | 97 | 阿里巴巴 |
| Naoto Sato | 273 | Oracle |

---

## 统计汇总

| 组织 | PRs | 详情 |
|------|-----|------|
| Oracle 中国团队 | 1,643 | [详情](orgs/oracle.md) |
| 阿里巴巴 | 121 | [详情](orgs/alibaba.md) |
| ISCAS | 53 | - |
| 字节跳动 | 25 | [详情](orgs/bytedance.md) |
| 龙芯 | 50+ | [详情](orgs/loongson.md) |
| 腾讯 | 40+ | [详情](orgs/tencent.md) |

---

## 相关链接

- [OpenJDK 中国社区](https://openjdk.org/groups/china/)
- [阿里巴巴 Dragonwell](https://github.com/alibaba/dragonwell8)
- [龙芯 JDK](https://github.com/loongson/jdk)
- [腾讯 Kona](https://github.com/Tencent/TencentKona-8)