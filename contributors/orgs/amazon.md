# Amazon

> Corretto 团队，AArch64 和编译器优化

---

## 概览

Amazon 通过 Corretto 团队参与 OpenJDK 开发，专注于 AArch64 架构优化、编译器改进和性能优化。

| 指标 | 值 |
|------|-----|
| **Integrated PRs** | 165+ |
| **贡献者数** | 3+ |
| **主要领域** | AArch64, 编译器 |

> **统计说明**: 使用 GitHub Integrated PRs 作为贡献指标。OpenJDK Committer 使用 `@openjdk.org` 邮箱提交代码，因此 git commits 按邮箱统计不准确。

---

## Top 贡献者

| 排名 | 贡献者 | GitHub | PRs | 领域 |
|------|--------|--------|-----|------|
| 1 | Andrew Dinn | [@earthling-amzn](https://github.com/earthling-amzn) | 123 | AArch64 |
| 2 | Nick Gasson | [@benty-amzn](https://github.com/benty-amzn) | 15 | AArch64 |
| 3 | David Beaumont | [@david-beaumont](https://github.com/david-beaumont) | 27 | 编译器 |

**小计**: 165 PRs (以上 3 人)

---

## 影响的模块

| 模块 | 文件数 | 说明 |
|------|--------|------|
| AArch64 移植 | 50+ | ARM 架构优化 |
| C2 编译器 | 30+ | 服务端编译器 |
| HotSpot Runtime | 20+ | JVM 运行时 |

---

## 主要领域

### AArch64 优化

- AArch64 架构优化
- 向量指令支持
- 性能调优

### 编译器

- C2 编译器改进
- JIT 优化

---

## Amazon Corretto

Amazon 维护自己的 JDK 发行版 Corretto：

| 特性 | 说明 |
|------|------|
| 基于 | OpenJDK |
| 支持 | 长期支持 (LTS) |
| 许可 | GPLv2 |
| 平台 | Linux, Windows, macOS |

**特点**:
- 免费生产就绪
- 长期支持
- AWS 优化
- 安全补丁

---

## 数据来源

- **统计方法**: GitHub PR search `repo:openjdk/jdk author:xxx type:pr label:integrated`
- **统计时间**: 2026-03-19

---

## 相关链接

- [Amazon Corretto](https://aws.amazon.com/corretto/)
- [Corretto GitHub](https://github.com/corretto)
- [Corretto 文档](https://docs.aws.amazon.com/corretto/)