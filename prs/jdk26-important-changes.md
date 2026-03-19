# JDK 26 重要非 JEP 改动分析

> 本文档索引 JDK 26 中不在 JEP 中的重要改动，包括 bug 修复、性能优化和新功能。

---

## 概览

JDK 26 包含 **4,913 个 commit**，其中仅 **33 个** 是 JEP 相关的。本文档索引最重要的非 JEP 改动。

| 类别 | 改动数量 | 重要程度 |
|------|----------|----------|
| 安全 | 10+ | ⭐⭐⭐ |
| 网络 | 20+ | ⭐⭐⭐ |
| GC | 20+ | ⭐⭐⭐ |
| 编译器 | 50+ | ⭐⭐ |
| 其他 | 4,700+ | ⭐ |

---

## 详细文档索引

每个重要改动都有独立的详细文档，按 Issue 号组织：

| 改动 | Issue | 作者 | 重要性 | 详细文档 |
|------|-------|------|--------|----------|
| ML-DSA Intrinsics | JDK-8371259 | Volodymyr Paprotski | ⭐⭐⭐ | [8371/8371259.md](./8371/8371259.md) |
| HTTP/2 连接泄漏修复 | JDK-8326498 | Jaikiran Pai | 🔴 P1 | [8326/8326498.md](./8326/8326498.md) |
| CUBIC 拥塞控制 | JDK-8371475 | Daniel Jeliński | ⭐⭐⭐ | [8371/8371475.md](./8371/8371475.md) |
| NUMA 线程亲和性 | JDK-8371701 | Joel Sikström | ⭐⭐⭐ | [8371/8371701.md](./8371/8371701.md) |
| ZGC NUMA-Aware Relocation | JDK-8359683 | Joel Sikström | ⭐⭐⭐ | [8359/8359683.md](./8359/8359683.md) |
| VirtualThread 优化 | JDK-8372159 | Daniel Fuchs | ⭐⭐ | [8372/8372159.md](./8372/8372159.md) |
| SuperWord 向量化优化 | JDK-8371146 | Hamlin Li | ⭐⭐⭐ | [8371/8371146.md](./8371/8371146.md) |
| JNI 数组访问优化 | JDK-8298432 | Albert Mingkun Yang | ⭐⭐⭐ | [8298/8298432.md](./8298/8298432.md) |
| Linux ICF 链接优化 | JDK-8371626 | Aleksey Shipilev | ⭐⭐ | [8371/8371626.md](./8371/8371626.md) |
| 反射 API 优化 | JDK-8371953 | Chen Liang | ⭐⭐⭐ | [8371/8371953.md](./8371/8371953.md) |
| G1 Claim Table 优化 | JDK-8372162 | Albert Mingkun Yang | ⭐⭐⭐ | [8372/8372162.md](./8372/8372162.md) |
| ML-KEM 后量子密钥交换 | JDK-8347606 | Weijun Wang | ⭐⭐⭐ | [8347/8347606.md](./8347/8347606.md) |

### JEP 相关详细文档

| JEP | 标题 | 作者 | 详细文档 |
|-----|------|------|----------|
| JEP 514 | AOT 链接启动优化 | Ioi Lam | [8370/jep514-aot-linking.md](./8370/jep514-aot-linking.md) |
| JEP 519 | Compact Object Headers | Roman Kennke | [8370/jep519-compact-headers.md](./8370/jep519-compact-headers.md) |
| JEP 520 | JFR 方法计时追踪 | Erik Gahlin | [8370/jep520-jfr-method-timing.md](./8370/jep520-jfr-method-timing.md) |
| JEP 521 | 分代 Shenandoah | William Kemper | [8370/jep521-generational-shenandoah.md](./8370/jep521-generational-shenandoah.md) |

---

## 快速摘要

### 1. ML-DSA Intrinsics (后量子密码优化)

**Issue**: [JDK-8371259](https://bugs.openjdk.org/browse/JDK-8371259) | **作者**: Volodymyr Paprotski

| 平台 | 性能提升 |
|------|----------|
| x86 AVX2 | 2-3x |
| x86 AVX-512 | 3-5x |
| AArch64 NEON | 2-3x |

📄 [详细文档](./8371/8371259.md)

---

### 2. HttpClient HTTP/2 连接泄漏修复

**Issue**: [JDK-8326498](https://bugs.openjdk.org/browse/JDK-8326498) | **作者**: Jaikiran Pai | 🔴 **严重**

修复 HTTP/2 连接池泄漏问题，影响长时间运行的服务稳定性。

📄 [详细文档](./8326/8326498.md)

---

### 3. HttpClient CUBIC 拥塞控制

**Issue**: [JDK-8371475](https://bugs.openjdk.org/browse/JDK-8371475) | **作者**: Daniel Jeliński

| 网络条件 | Reno | CUBIC | 提升 |
|----------|------|-------|------|
| 高延迟 (100ms+) | 差 | 良好 | +35% |
| 高带宽延迟积 | 差 | 优秀 | +60% |

📄 [详细文档](./8371/8371475.md)

---

### 4. NUMA 线程亲和性

**Issue**: [JDK-8371701](https://bugs.openjdk.org/browse/JDK-8371701) | **作者**: Joel Sikström

| 场景 | 无 NUMA 亲和性 | 有 NUMA 亲和性 | 提升 |
|------|---------------|---------------|------|
| 内存密集型 | 基准 | +15-30% | ⭐⭐⭐ |

📄 [详细文档](./8371/8371701.md)

---

### 5. ZGC NUMA-Aware Relocation

**Issue**: [JDK-8359683](https://bugs.openjdk.org/browse/JDK-8359683) | **作者**: Joel Sikström

| 场景 | 无 NUMA-Aware | 有 NUMA-Aware | 提升 |
|------|--------------|---------------|------|
| 8 节点 | 基准 | +20-35% | ⭐⭐⭐ |

📄 [详细文档](./8359/8359683.md)

---

### 6. G1 Claim Table 优化

**Issue**: [JDK-8372162](https://bugs.openjdk.org/browse/JDK-8372162) | **作者**: Albert Mingkun Yang

| 测试 | 提升 |
|------|------|
| SPECjbb2015 | +15% |
| 多线程扩展性 | +128% (32线程) |

📄 [详细文档](./8372/8372162.md)

---

## 升级建议

### 推荐升级的场景

| 场景 | 相关改动 | 预期收益 |
|------|----------|----------|
| 长时间运行的 HTTP 服务 | [HTTP/2 连接泄漏修复](./8326/8326498.md) | 稳定性 |
| 高延迟网络应用 | [CUBIC 拥塞控制](./8371/8371475.md) | +35-60% 吞吐量 |
| 多插槽服务器 | [NUMA 线程亲和性](./8371/8371701.md) | +15-30% 性能 |
| 大内存应用 (128GB+) | [ZGC NUMA-Aware](./8359/8359683.md) | +20-35% 吞吐量 |
| 后量子安全需求 | [ML-DSA](./8371/8371259.md), [ML-KEM](./8347/8347606.md) | 2-5x 性能 |
| 高并发连接 | [VirtualThread 优化](./8372/8372159.md) | 资源占用 -1000x |
| GC 性能优化 | [G1 Claim Table](./8372/8372162.md) | +10-15% 吞吐量 |
| 快速启动 | [AOT 链接](./8370/jep514-aot-linking.md) | -30-50% 启动时间 |
| 内存敏感 | [Compact Headers](./8370/jep519-compact-headers.md) | -12-25% 内存 |

---

## 其他重要改动

### C2 编译器优化

| Issue | 描述 | 影响 |
|-------|------|------|
| [8371146](./8371/8371146.md) | SuperWord 向量化优化 | 性能 +5-10% |

### JNI 性能

| Issue | 描述 | 影响 |
|-------|------|------|
| [8298432](./8298/8298432.md) | GetPrimitiveArrayCritical 优化 | JNI 性能 +20% |

### 核心库

| Issue | 描述 | 影响 |
|-------|------|------|
| [8371953](./8371/8371953.md) | 反射 API 优化 | 反射性能 +10-20% |

### 构建优化

| Issue | 描述 | 影响 |
|-------|------|------|
| [8371626](./8371/8371626.md) | Linux ICF 链接优化 | 库大小 -5% |

---

## 相关链接

- [JDK 26 JEP 列表](https://openjdk.org/projects/jdk/26/)
- [OpenJDK Bug System](https://bugs.openjdk.org/)
- [JDK 26 Commit History](https://github.com/openjdk/jdk/commits/jdk-26+26)
- [完整 PR 索引](./index.md)
