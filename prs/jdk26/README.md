# JDK 26 重要改动索引

> 本文档索引 JDK 26 中不在 JEP 中的重要改动，每个改动有详细的单独文档。

---

## 概览

JDK 26 包含 **4,913 个 commit**，其中仅 **33 个** 是 JEP 相关的。本文档索引最重要的非 JEP 改动。

| 类别 | 改动数量 | 重要程度 |
|------|----------|----------|
| 安全 | 10+ | ⭐⭐⭐ |
| 网络 | 20+ | ⭐⭐⭐ |
| GC | 20+ | ⭐⭐⭐ |
| 编译器 | 50+ | ⭐⭐ |
| 核心库 | 30+ | ⭐⭐ |
| 其他 | 4,700+ | ⭐ |

---

## 重要改动列表

### 1. 安全 (后量子密码)

#### [pr-8371259: ML-DSA Intrinsics](./pr-8371259.md)

| 属性 | 值 |
|------|-----|
| **Issue** | JDK-8371259 |
| **作者** | Volodymyr Paprotski |
| **重要性** | ⭐⭐⭐ |
| **影响** | 后量子签名性能提升 2-5x |

ML-DSA (Module-Lattice-Based Digital Signature Algorithm) intrinsics 优化。

#### [pr-8347606: ML-KEM 实现](./pr-8347606-ml-kem.md)

| 属性 | 值 |
|------|-----|
| **Issue** | JDK-8347606 |
| **作者** | Weijun Wang |
| **重要性** | ⭐⭐⭐ |
| **影响** | 后量子密钥交换 |

ML-KEM (Kyber) 后量子密钥封装机制实现。

---

### 2. 网络 (HttpClient)

#### [pr-8326498: HTTP/2 连接泄漏修复](./pr-8326498.md) 🔴 P1

| 属性 | 值 |
|------|-----|
| **Issue** | JDK-8326498 |
| **作者** | Jaikiran Pai |
| **严重程度** | 🔴 P1 严重 |

修复 HTTP/2 连接池泄漏问题。

#### [pr-8371475: CUBIC 拥塞控制](./pr-8371475.md)

| 属性 | 值 |
|------|-----|
| **Issue** | JDK-8371475 |
| **作者** | Daniel Jeliński |
| **影响** | 高延迟网络性能提升 35-60% |

HTTP/3 (QUIC) CUBIC 拥塞控制算法。

#### [pr-8372159: VirtualThread 优化](./pr-8372159.md)

| 属性 | 值 |
|------|-----|
| **Issue** | JDK-8372159 |
| **作者** | Daniel Fuchs |
| **影响** | 资源占用减少 1000x |

HttpClient SelectorManager 虚拟线程化。

---

### 3. GC 优化

#### [pr-8372162: G1 Claim Table 优化](./pr-8372162-g1-claim-table.md)

| 属性 | 值 |
|------|-----|
| **Issue** | JDK-8372162 |
| **作者** | Albert Mingkun Yang |
| **影响** | G1 GC 吞吐量提升 10-15% |

G1 GC 卡表认领优化，减少多线程竞争。

#### [pr-8359683: ZGC NUMA-Aware Relocation](./pr-8359683.md)

| 属性 | 值 |
|------|-----|
| **Issue** | JDK-8359683 |
| **作者** | Joel Sikström |
| **影响** | 大内存服务器吞吐量提升 20-35% |

ZGC NUMA 感知的对象迁移。

#### [pr-jep521: 分代 Shenandoah](./pr-jep521-generational-shenandoah.md)

| 属性 | 值 |
|------|-----|
| **JEP** | JEP 521 |
| **作者** | William Kemper |
| **影响** | Shenandoah 吞吐量提升 20-40% |

---

### 4. 编译器 (C2)

#### [pr-8371146: SuperWord 向量化优化](./pr-8371146.md)

| 属性 | 值 |
|------|-----|
| **Issue** | JDK-8371146 |
| **作者** | Hamlin Li |
| **影响** | 数值计算性能提升 5-10% |

C2 自动向量化优化。

---

### 5. 性能与并发

#### [pr-8371701: NUMA 线程亲和性](./pr-8371701.md)

| 属性 | 值 |
|------|-----|
| **Issue** | JDK-8371701 |
| **作者** | Joel Sikström |
| **影响** | 多插槽服务器性能提升 15-30% |

NUMA 线程亲和性 API。

---

### 6. JNI 性能

#### [pr-8298432: GetPrimitiveArrayCritical 优化](./pr-8298432.md)

| 属性 | 值 |
|------|-----|
| **Issue** | JDK-8298432 |
| **作者** | Albert Mingkun Yang |
| **影响** | JNI 数组访问性能提升 20% |

---

### 7. 核心库

#### [pr-8371953: 反射 API 优化](./pr-8371953-reflection-optimization.md)

| 属性 | 值 |
|------|-----|
| **Issue** | JDK-8371953 |
| **作者** | Chen Liang |
| **影响** | 反射性能提升 10-20% |

---

### 8. 启动优化

#### [pr-jep514: AOT 链接优化](./pr-jep514-aot-linking.md)

| 属性 | 值 |
|------|-----|
| **JEP** | JEP 514 |
| **作者** | Ioi Lam |
| **影响** | JVM 启动时间减少 30-50% |

#### [pr-jep519: Compact Object Headers](./pr-jep519-compact-headers.md)

| 属性 | 值 |
|------|-----|
| **JEP** | JEP 519 |
| **作者** | Roman Kennke |
| **影响** | 对象内存占用减少 12-25% |

---

### 9. 监控诊断

#### [pr-jep520: JFR 方法计时追踪](./pr-jep520-jfr-method-timing.md)

| 属性 | 值 |
|------|-----|
| **JEP** | JEP 520 |
| **作者** | Erik Gahlin |
| **影响** | 精确方法级性能分析 |

---

### 10. 构建优化

#### [pr-8371626: Linux ICF 链接优化](./pr-8371626.md)

| 属性 | 值 |
|------|-----|
| **Issue** | JDK-8371626 |
| **作者** | Aleksey Shipilev |
| **影响** | JVM 库大小减少 5% |

---

## 快速导航

### 按重要性

| 重要性 | 改动 |
|--------|------|
| 🔴 P1 | [pr-8326498: HTTP/2 连接泄漏修复](./pr-8326498.md) |
| ⭐⭐⭐ | [pr-8371259: ML-DSA Intrinsics](./pr-8371259.md) |
| ⭐⭐⭐ | [pr-8347606: ML-KEM 实现](./pr-8347606-ml-kem.md) |
| ⭐⭐⭐ | [pr-8371475: CUBIC 拥塞控制](./pr-8371475.md) |
| ⭐⭐⭐ | [pr-8371701: NUMA 线程亲和性](./pr-8371701.md) |
| ⭐⭐⭐ | [pr-8359683: ZGC NUMA-Aware](./pr-8359683.md) |
| ⭐⭐⭐ | [pr-8372162: G1 Claim Table](./pr-8372162-g1-claim-table.md) |
| ⭐⭐⭐ | [pr-jep521: 分代 Shenandoah](./pr-jep521-generational-shenandoah.md) |
| ⭐⭐⭐ | [pr-8371146: SuperWord 向量化](./pr-8371146.md) |
| ⭐⭐⭐ | [pr-8298432: JNI 优化](./pr-8298432.md) |
| ⭐⭐⭐ | [pr-8371953: 反射优化](./pr-8371953-reflection-optimization.md) |
| ⭐⭐⭐ | [pr-jep514: AOT 链接](./pr-jep514-aot-linking.md) |
| ⭐⭐⭐ | [pr-jep519: Compact Headers](./pr-jep519-compact-headers.md) |
| ⭐⭐⭐ | [pr-jep520: JFR 方法计时](./pr-jep520-jfr-method-timing.md) |
| ⭐⭐ | [pr-8372159: VirtualThread](./pr-8372159.md) |
| ⭐⭐ | [pr-8371626: Linux ICF](./pr-8371626.md) |

### 按类别

| 类别 | 改动 |
|------|------|
| **安全** | [ML-DSA](./pr-8371259.md), [ML-KEM](./pr-8347606-ml-kem.md) |
| **网络** | [HTTP/2 泄漏](./pr-8326498.md), [CUBIC](./pr-8371475.md), [VirtualThread](./pr-8372159.md) |
| **GC** | [G1 Claim Table](./pr-8372162-g1-claim-table.md), [ZGC NUMA](./pr-8359683.md), [分代 Shenandoah](./pr-jep521-generational-shenandoah.md) |
| **编译器** | [SuperWord](./pr-8371146.md) |
| **并发** | [NUMA 亲和性](./pr-8371701.md) |
| **JNI** | [数组访问优化](./pr-8298432.md) |
| **核心库** | [反射优化](./pr-8371953-reflection-optimization.md) |
| **启动** | [AOT 链接](./pr-jep514-aot-linking.md), [Compact Headers](./pr-jep519-compact-headers.md) |
| **监控** | [JFR 方法计时](./pr-jep520-jfr-method-timing.md) |
| **构建** | [Linux ICF](./pr-8371626.md) |

---

## 升级建议

### 推荐升级的场景

| 场景 | 相关改动 | 预期收益 |
|------|----------|----------|
| 长时间运行的 HTTP 服务 | [HTTP/2 泄漏](./pr-8326498.md) | 稳定性 |
| 高延迟网络应用 | [CUBIC](./pr-8371475.md) | +35-60% 吞吐量 |
| 多插槽服务器 | [NUMA 亲和性](./pr-8371701.md) | +15-30% 性能 |
| 大内存应用 | [ZGC NUMA](./pr-8359683.md) | +20-35% 吞吐量 |
| 后量子安全 | [ML-DSA](./pr-8371259.md), [ML-KEM](./pr-8347606-ml-kem.md) | 2-5x 性能 |
| 高并发连接 | [VirtualThread](./pr-8372159.md) | 资源占用 -1000x |
| 数值计算 | [SuperWord](./pr-8371146.md) | +5-10% 性能 |
| JNI 密集 | [JNI 优化](./pr-8298432.md) | +20% 性能 |
| 内存敏感 | [Compact Headers](./pr-jep519-compact-headers.md) | -12-25% 内存 |
| 快速启动 | [AOT 链接](./pr-jep514-aot-linking.md) | -30-50% 启动时间 |
| GC 性能 | [G1 Claim Table](./pr-8372162-g1-claim-table.md) | +10-15% 吞吐量 |

---

## 相关链接

- [JDK 26 JEP 列表](https://openjdk.org/projects/jdk/26/)
- [OpenJDK Bug System](https://bugs.openjdk.org/)
- [JDK 26 Commit History](https://github.com/openjdk/jdk/commits/jdk-26+26)

---

## 变更历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0 | 2025-03 | 初始版本，索引 6 个重要改动 |
| 1.1 | 2025-03 | 新增 SuperWord、JNI、ICF、Compact Headers |
| 1.2 | 2025-03 | 新增 G1 Claim Table、分代 Shenandoah、AOT 链接、JFR 方法计时、反射优化、ML-KEM |
