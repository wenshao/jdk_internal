# Ben Perez

> **GitHub**: [@bperez](https://github.com/bperez)
> **Organization**: Trail of Bits
> **Location**: New York, USA

---
## 目录

1. [概述](#1-概述)
2. [主要贡献](#2-主要贡献)
3. [分析的 PR](#3-分析的-pr)
4. [外部资源](#4-外部资源)

---


## 1. 概述

Ben Perez 是 Trail of Bits 的安全研究员和密码学工程师，专注于后量子密码学实现和审计。他对 JDK 的主要贡献是 ML-KEM 和 ML-DSA 后量子密码学算法的性能优化。

---

## 2. 主要贡献

### JDK 26 (2025-2026)

| PR/Issue | 标题 | 角色 |
|----------|------|------|
| [JDK-8347608](../../by-pr/8347/8347608.md) | 优化 ML-KEM Java 实现 | Author |
| [JDK-8347606](https://bugs.openjdk.org/browse/JDK-8347606) | 优化 ML-DSA 实现 | Author |

### 核心优化领域

| 领域 | 说明 |
|------|------|
| **后量子密码学** | ML-KEM, ML-DSA 算法优化 |
| **密码学性能** | 数组操作优化、循环展开 |
| **安全审计** | 密码学实现安全审查 |

---

## 3. 分析的 PR

### JDK-8347608: 优化 ML-KEM Java 实现

优化了 ML-KEM (Module-Lattice-Based Key Encapsulation Mechanism) 的实现，通过循环展开和行缓存实现 1-2% 的性能提升。

**关键改进**:
- 矩阵向量乘法循环展开（8 次迭代为一组）
- 行缓存减少数组访问开销
- 边界检查减少

**技术细节**:
- 优化矩阵向量乘法热点路径
- 使用 `while (j + 8 <= N)` 模式减少边界检查
- 预先缓存 `matrix[i]` 行引用

**文档**: [详细分析](../../by-pr/8347/8347608.md)

---

## 4. 外部资源

### 链接

- **GitHub**: [https://github.com/bperez](https://github.com/bperez)
- **Blog**: [Trail of Bits Blog](https://blog.trailofbits.com/authors/ben-perez/)
- **Company**: [Trail of Bits](https://www.trailofbits.com/)

### 相关阅读

- [FIPS 203: ML-KEM Standard](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- [Post-Quantum Cryptography in JDK](https://openjdk.org/jeps/)

---

> **文档版本**: 1.0
> **最后更新**: 2026-03-20
> **创建原因**: JDK-8347608 PR 分析

## 角色晋升 (CFV)

| 日期 | 角色 | 提名者 | 投票数 | 链接 |
|------|------|--------|--------|------|
| 2024-08-01 | Committer | Valerie Peng | 6 | [CFV](https://mail.openjdk.org/pipermail/jdk-dev/2024-August/009282.html) |

**提名时统计**: 16 fixes
**贡献领域**: From: jdk-dev <jdk-dev-retn at openjdk.org> On Behalf Of Sean Mullan
