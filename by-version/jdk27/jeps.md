# JDK 27 JEP 汇总

> **数据截至**: 2026-04-12 | **来源**: [openjdk.org/projects/jdk/27](https://openjdk.org/projects/jdk/27/)

---

## 总览

| 指标 | 值 |
|------|-----|
| **已 Target JEP** | 1 |
| **Proposed to Target** | 0 |
| **预计 GA** | 2026-09-16 |
| **开发阶段** | 早期开发 |

---

## 已 Target 的 JEP

### JEP 527: Post-Quantum Hybrid Key Exchange for TLS 1.3

| 属性 | 值 |
|------|-----|
| **JEP** | [527](https://openjdk.org/jeps/527) |
| **状态** | Completed / Targeted to JDK 27 |
| **类别** | 安全 (Security) |
| **组件** | security-libs/javax.net.ssl |

**概述**: 引入后量子混合密钥交换机制到 Java 的 TLS 1.3 实现中。使用经典密钥交换算法（如 X25519）与后量子密钥封装机制（如 ML-KEM）的混合方案，提供对量子计算威胁的前瞻性防护。

**关键点**:
- 混合方案确保即使后量子算法被攻破，仍有经典算法提供安全保障
- 基于 IETF 标准化的混合密钥交换机制
- 对现有 TLS 应用透明，无需代码修改
- 性能影响最小，主要增加握手阶段的数据量

**详细分析**: [JEP 527 分析](../../jeps/security/jep-527.md)

---

## Proposed to Target

暂无。JDK 27 处于早期开发阶段（GA 预计 2026-09-16），更多 JEP 将在 Rampdown Phase One（2026-06-04）之前陆续确定。

---

## 历史对比

| 版本 | JEP 数量 | GA 日期 |
|------|---------|---------|
| JDK 24 | 24 | 2025-03-18 |
| JDK 25 | 18 | 2025-09-16 |
| JDK 26 | 10 | 2026-03-17 |
| JDK 27 | 1+ (开发中) | 2026-09-16 |

---

## 相关链接

- [OpenJDK JDK 27 项目页](https://openjdk.org/projects/jdk/27/)
- [JEP 索引](https://openjdk.org/jeps/0)
- [JEP 分析总览](../../jeps/)
- [JDK 27 README](./README.md)
