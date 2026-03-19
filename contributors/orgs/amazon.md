# Amazon

> AArch64 优化和 Shenandoah GC 的重要贡献者

---

## 概览

Amazon 通过 Corretto 团队参与 OpenJDK 开发，专注于 AArch64 优化、Shenandoah GC 和 C2 编译器改进。

| 指标 | 值 |
|------|-----|
| **总 Commits** | 300+ |
| **贡献者数** | 30+ |
| **占比** | ~1% |
| **主要领域** | AArch64, Shenandoah, C2 编译器 |

---

## 影响的模块分布

基于 git 修改文件统计：

| 模块 | 文件数 | 说明 |
|------|--------|------|
| AArch64 移植 | 69 | 64 位 ARM 架构 |
| C2 编译器 | 55 | 服务端编译器 |
| Shenandoah GC | 55 | Shenandoah 垃圾收集器 |
| Shenandoah 启发式 | 26 | GC 启发式算法 |
| 代码缓存 | 24 | 代码缓存管理 |
| x86 移植 | 20 | x86 架构支持 |
| G1 GC | 15 | G1 垃圾收集器 |
| 编译器共享 | 11 | 编译器共享代码 |

---

## Top 贡献者

| 排名 | 贡献者 | Commits | 领域 |
|------|--------|---------|------|
| 1 | Xiaolong Peng | 269 | C2 编译器 |
| 2 | William Kemper | 231 | Shenandoah GC |
| 3 | Kelvin Nilsen | 186 | AArch64 |
| 4 | Evgeny Astigeevich | 58 | C2 编译器 |
| 5 | Joshua Cao | 24 | 编译器 |
| 6 | Chad Rakoczy | 18 | 编译器 |
| 7 | Yi-Fan Tsai | 15 | - |
| 8 | Rui Li | 12 | - |

---

## 主要领域

### AArch64 优化

Amazon 在 AArch64 架构上有重要贡献：

- **Kelvin Nilsen**: AArch64 向量化优化
- **AArch64 后端**: C2 编译器 AArch64 支持

**关键贡献**:
- 向量指令优化
- NEON 指令集支持
- 性能基准测试

### Shenandoah GC

- **William Kemper**: Shenandoah 维护者 (原 Red Hat)
- GC 启发式算法改进
- 性能优化

### C2 编译器

- **Xiaolong Peng**: C2 优化专家
- **Evgeny Astigeevich**: C2 向量化
- 编译器中间表示优化

---

## Amazon Corretto

Amazon 维护自己的 JDK 发行版 Corretto：

| 特性 | 说明 |
|------|------|
| 基于 | OpenJDK |
| 支持 | 长期支持 (LTS) |
| 许可 | GPLv2 |
| 平台 | Linux, Windows, macOS, Docker |

**特点**:
- 免费生产就绪
- 长期支持
- AWS 优化
- 安全补丁

---

## 技术特点

### 云原生优化

- AWS Graviton (ARM) 处理器优化
- 容器化部署支持
- 低延迟配置

### 性能优化

- 向量化优化
- GC 调优
- 启动时间优化

---

## 数据来源

- **统计方法**: `git log upstream_master --author="amazon"`
- **模块分析**: 基于修改文件路径统计

---

## 相关链接

- [Amazon Corretto](https://aws.amazon.com/corretto/)
- [Corretto GitHub](https://github.com/corretto)
- [AWS Java](https://aws.amazon.com/java/)