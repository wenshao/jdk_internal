# SAP

> PPC 移植和 HotSpot 调试支持的重要贡献者

---

## 概览

SAP 是 OpenJDK 的长期贡献者，专注于 PowerPC (PPC) 移植、AIX 平台支持和 HotSpot 调试能力。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 700+ |
| **贡献者数** | 30+ |
| **主要领域** | PPC 移植, AIX, HotSpot |

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。OpenJDK Committer 使用 `@openjdk.org` 邮箱提交代码，因此 git commits 按邮箱统计不准确。

---

## Top 贡献者

| 排名 | 贡献者 | GitHub | PRs | 领域 |
|------|--------|--------|-----|------|
| 1 | Matthias Baesken | [@MBaesken](https://github.com/MBaesken) | 515 | 构建系统 |
| 2 | Erik Joelsson | [@eirbjo](https://github.com/eirbjo) | 103 | 构建系统 |
| 3 | Martin Haessig | [@mhaessig](https://github.com/mhaessig) | 57 | 测试 |
| 4 | Anatoly Zelenin | [@toxaart](https://github.com/toxaart) | 29 | PPC |

**小计**: 704 PRs (以上 4 人)

---

## 影响的模块

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

## 主要领域

### PowerPC (PPC) 移植

SAP 主导 PowerPC 架构的 OpenJDK 移植：

- **PPC64**: 64 位 PowerPC 支持
- **PPC64LE**: 小端模式支持
- **JIT 支持**: C2 编译器 PPC 后端

### AIX 平台

- AIX 操作系统支持
- AIX 特定的构建配置
- AIX 线程和内存管理

### HotSpot 调试

- JVM 初始化、调试支持
- HotSpot 服务性

### 构建系统

- 跨平台构建
- Windows 构建

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

## 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-19

---

## 相关链接

- [SAP SapMachine](https://sap.github.io/SapMachine/)
- [SAP GitHub](https://github.com/SAP/SapMachine)
- [SAP OpenJDK](https://openjdk.org/groups/hotspot/)