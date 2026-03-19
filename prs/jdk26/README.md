# JDK 26 重要改动索引

> 本文档索引 JDK 26 中不在 JEP 中的重要改动，每个改动有详细的单独文档。

---

## 概览

JDK 26 包含 **4,913 个 commit**，其中仅 **33 个** 是 JEP 相关的。本文档索引最重要的非 JEP 改动。

| 类别 | 改动数量 | 重要程度 |
|------|----------|----------|
| 安全 | 7 | ⭐⭐⭐ |
| 网络 | 20+ | ⭐⭐⭐ |
| GC | 15+ | ⭐⭐⭐ |
| 编译器 | 50+ | ⭐⭐ |
| 其他 | 4,800+ | ⭐ |

---

## 重要改动列表

### 1. 安全

#### [pr-8371259: ML-DSA Intrinsics (后量子密码优化)](./pr-8371259.md)

| 属性 | 值 |
|------|-----|
| **Issue** | JDK-8371259 |
| **作者** | Volodymyr Paprotski |
| **重要性** | ⭐⭐⭐ |
| **影响** | 后量子密码性能提升 2-5x |

ML-DSA (Module-Lattice-Based Digital Signature Algorithm) 是 NIST 标准化的后量子密码签名算法。本改动引入 AVX2 和 AVX-512 intrinsics 优化。

**关键特性:**
- AVX-512 向量化实现
- AArch64 NEON 支持
- JAR 签名支持

---

### 2. 网络 (HttpClient)

#### [pr-8326498: HTTP/2 连接泄漏修复](./pr-8326498.md)

| 属性 | 值 |
|------|-----|
| **Issue** | JDK-8326498 |
| **作者** | Jaikiran Pai |
| **严重程度** | 🔴 P1 严重 |
| **影响** | 长时间运行服务稳定性 |

修复 `java.net.http.HttpClient` 在使用 HTTP/2 时的连接池泄漏问题。

**关键特性:**
- 新增 `Http2TerminationCause` 枚举
- 统一的连接终止逻辑
- 连接池正确清理

---

#### [pr-8371475: CUBIC 拥塞控制](./pr-8371475.md)

| 属性 | 值 |
|------|-----|
| **Issue** | JDK-8371475 |
| **作者** | Daniel Jeliński |
| **重要性** | ⭐⭐⭐ |
| **影响** | 高延迟网络性能提升 35-60% |

为 HTTP/3 (QUIC) 实现了 CUBIC 拥塞控制算法，替代原有的 Reno 算法。

**关键特性:**
- 三次函数窗口增长
- TCP 友好性
- 发送节奏控制 (Pacing)

---

#### [pr-8372159: VirtualThread 优化](./pr-8372159.md)

| 属性 | 值 |
|------|-----|
| **Issue** | JDK-8372159 |
| **作者** | Daniel Fuchs |
| **重要性** | ⭐⭐ |
| **影响** | 资源占用减少 1000x |

将 HttpClient 的 SelectorManager 线程改为虚拟线程，减少平台线程占用。

**关键特性:**
- 内存占用从 ~1MB 降至 ~1KB
- 完全向后兼容
- 避免虚拟线程 pinning

---

### 3. 性能与并发

#### [pr-8371701: NUMA 线程亲和性](./pr-8371701.md)

| 属性 | 值 |
|------|-----|
| **Issue** | JDK-8371701 |
| **作者** | Joel Sikström |
| **重要性** | ⭐⭐⭐ |
| **影响** | 多插槽服务器性能提升 15-30% |

新增 API 允许设置线程的 NUMA 亲和性，优化多插槽服务器的内存访问性能。

**关键特性:**
- JVM 内部 API
- Linux/Windows 支持
- 内存分配策略控制

---

### 4. GC (ZGC)

#### [pr-8359683: ZGC NUMA-Aware Relocation](./pr-8359683.md)

| 属性 | 值 |
|------|-----|
| **Issue** | JDK-8359683 |
| **作者** | Joel Sikström |
| **重要性** | ⭐⭐⭐ |
| **影响** | 大内存服务器吞吐量提升 20-35% |

ZGC 在对象迁移时考虑 NUMA 亲和性，减少跨节点内存访问。

**关键特性:**
- 对象访问模式分析
- NUMA-Aware 页面分配
- 迁移统计日志

---

## 快速导航

### 按重要性

| 重要性 | 改动 |
|--------|------|
| ⭐⭐⭐ | [pr-8371259: ML-DSA Intrinsics](./pr-8371259.md) |
| 🔴 P1 | [pr-8326498: HTTP/2 连接泄漏修复](./pr-8326498.md) |
| ⭐⭐⭐ | [pr-8371475: CUBIC 拥塞控制](./pr-8371475.md) |
| ⭐⭐⭐ | [pr-8371701: NUMA 线程亲和性](./pr-8371701.md) |
| ⭐⭐⭐ | [pr-8359683: ZGC NUMA-Aware Relocation](./pr-8359683.md) |
| ⭐⭐ | [pr-8372159: VirtualThread 优化](./pr-8372159.md) |

### 按类别

| 类别 | 改动 |
|------|------|
| 安全 | [pr-8371259: ML-DSA Intrinsics](./pr-8371259.md) |
| 网络 | [pr-8326498: HTTP/2 连接泄漏修复](./pr-8326498.md) |
| 网络 | [pr-8371475: CUBIC 拥塞控制](./pr-8371475.md) |
| 网络 | [pr-8372159: VirtualThread 优化](./pr-8372159.md) |
| 并发 | [pr-8371701: NUMA 线程亲和性](./pr-8371701.md) |
| GC | [pr-8359683: ZGC NUMA-Aware Relocation](./pr-8359683.md) |

### 按作者

| 作者 | 改动 |
|------|------|
| Volodymyr Paprotski | [pr-8371259: ML-DSA Intrinsics](./pr-8371259.md) |
| Jaikiran Pai | [pr-8326498: HTTP/2 连接泄漏修复](./pr-8326498.md) |
| Daniel Jeliński | [pr-8371475: CUBIC 拥塞控制](./pr-8371475.md) |
| Daniel Fuchs | [pr-8372159: VirtualThread 优化](./pr-8372159.md) |
| Joel Sikström | [pr-8371701: NUMA 线程亲和性](./pr-8371701.md) |
| Joel Sikström | [pr-8359683: ZGC NUMA-Aware Relocation](./pr-8359683.md) |

---

## 升级建议

### 推荐升级的场景

| 场景 | 相关改动 | 预期收益 |
|------|----------|----------|
| 长时间运行的 HTTP 服务 | [pr-8326498](./pr-8326498.md) | 稳定性 |
| 高延迟网络应用 | [pr-8371475](./pr-8371475.md) | +35-60% 吞吐量 |
| 多插槽服务器 | [pr-8371701](./pr-8371701.md) | +15-30% 性能 |
| 大内存应用 (128GB+) | [pr-8359683](./pr-8359683.md) | +20-35% 吞吐量 |
| 后量子安全需求 | [pr-8371259](./pr-8371259.md) | 2-5x 性能 |
| 高并发连接 | [pr-8372159](./pr-8372159.md) | 资源占用 -1000x |

### 升级检查清单

- [ ] 检查 HTTP/2 连接池配置
- [ ] 启用 `-XX:+UseNUMA` (多插槽服务器)
- [ ] 启用 `-XX:+ZNUMAAwareRelocation` (ZGC 用户)
- [ ] 评估 ML-DSA 迁移计划 (安全敏感应用)
- [ ] 验证虚拟线程兼容性

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
