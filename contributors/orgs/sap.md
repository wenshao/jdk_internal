# SAP

> PPC 移植和 HotSpot 调试支持的重要贡献者

---

## 概览

SAP 是 OpenJDK 的长期贡献者，专注于 PowerPC (PPC) 移植、AIX 平台支持和 HotSpot 调试能力。

| 指标 | 值 |
|------|-----|
| **总 Commits** | 200+ |
| **贡献者数** | 30+ |
| **占比** | ~2% |
| **主要领域** | PPC 移植, AIX, HotSpot |

---

## 影响的模块分布

基于 git 修改文件统计：

| 模块 | 文件数 | 说明 |
|------|--------|------|
| PPC 移植 (旧) | 42 | PowerPC 架构支持 (旧路径) |
| PPC 移植 (新) | 30 | PowerPC 架构支持 (新路径) |
| C2 编译器 | 22 | 服务端编译器 |
| HotSpot Runtime | 15 | JVM 运行时 |
| AIX 平台 | 14 | AIX 操作系统支持 |
| ADLC | 12 | 架构描述语言编译器 |
| 构建系统 | 10 | Autoconf 构建配置 |

---

## Commit 类型分析

| 类型 | 数量 | 说明 |
|------|------|------|
| AIX | 12 | AIX 平台相关 |
| Fix | 10 | 修复问题 |
| PPC | 12 | PowerPC 相关 |
| Add | 4 | 新增功能 |
| Optimize | 3 | 性能优化 |
| Clean | 3 | 代码清理 |

---

## Top 贡献者

| 排名 | 贡献者 | Commits | 领域 |
|------|--------|---------|------|
| 1 | Johannes Bechberger | 9 | 测试 |
| 2 | Goetz Lindenmaier | 9 | HotSpot |
| 3 | Richard Reingruber | 8 | - |
| 4 | David Briemann | 8 | - |
| 5 | [Matthias Baesken](../matthias-baesken.md) | 7 | 构建系统 |
| 6 | Axel Siebenborn | 7 | - |
| 7 | Joachim Kern | 7 | - |
| 8 | Thomas Stuefe | 6 | HotSpot |
| 9 | Christoph Langer | 6 | 构建 |
| 10 | Arno Zeller | 6 | - |

> 注：Matthias Baesken (742 commits) 主要使用 @openjdk.org 邮箱

---

## 主要领域

### PowerPC (PPC) 移植

SAP 主导 PowerPC 架构的 OpenJDK 移植：

- **PPC64**: 64 位 PowerPC 支持
- **PPC64LE**: 小端模式支持
- **JIT 支持**: C2 编译器 PPC 后端

**关键文件**:
- `src/hotspot/cpu/ppc/` - PPC 架构代码
- `src/hotspot/cpu/ppc/gc/shared/` - GC 共享代码

### AIX 平台

- AIX 操作系统支持
- AIX 特定的构建配置
- AIX 线程和内存管理

### HotSpot 调试

- **Thomas Stuefe**: JVM 初始化、调试支持
- **Goetz Lindenmaier**: HotSpot 服务性

### 构建系统

- **Matthias Baesken**: 跨平台构建
- **Christoph Langer**: Windows 构建

---

## SAP JVM (SapMachine)

SAP 维护自己的 JVM 发行版 SapMachine：

| 特性 | 说明 |
|------|------|
| 基于 | OpenJDK |
| 支持 | 长期支持版本 |
| 特点 | 企业级服务性增强 |
| 许可 | GPLv2 |

**额外特性**:
- 增强的诊断能力
- 更好的错误报告
- 企业级监控

---

## 技术特点

### 多平台支持

- **Linux PPC64/PPC64LE**: 主要服务器平台
- **AIX**: IBM Unix 系统
- **Windows**: 企业环境

### 服务性

SAP 特别关注 JVM 的服务性：
- 崩溃诊断
- 内存泄漏检测
- 性能分析工具

---

## 数据来源

- **统计方法**: `git log upstream_master --author="sap.com"`
- **模块分析**: 基于修改文件路径统计
- **关键词分析**: 基于 commit message 提取

---

## 相关链接

- [SAP SapMachine](https://sap.github.io/SapMachine/)
- [SAP GitHub](https://github.com/SAP/SapMachine)
- [SAP OpenJDK](https://openjdk.org/groups/hotspot/)