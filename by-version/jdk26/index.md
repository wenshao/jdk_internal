# JDK 26

> **状态**: 开发中 | **发布**: 2025-09 | **类型**: Feature Release

---

## 版本概览

JDK 26 是继 JDK 21 之后的首个功能版本，包含多项重要改进：

- **HTTP/3** 支持
- **分代 ZGC** 和 **分代 Shenandoah**
- **G1 GC** 吞吐量提升
- **后量子密码** (ML-DSA)
- **Compact Object Headers**
- **AOT 编译**改进

---

## JEP 汇总

### 语言特性

| JEP | 标题 | 状态 |
|-----|------|------|
| [JEP 530](../../jeps/jep-530.md) | Primitive Types in Patterns | 预览 |
| [JEP 526](../../jeps/jep-526.md) | Lazy Constants | 预览 |
| [JEP 512](../../jeps/jep-512.md) | Compact Source Files | 正式 |
| [JEP 511](../../jeps/jep-511.md) | Module Import Declarations | 正式 |

### 性能

| JEP | 标题 | 影响 |
|-----|------|------|
| [JEP 522](../../jeps/jep-522.md) | G1 GC Throughput | +10-20% |
| [JEP 521](../../jeps/jep-521.md) | Generational Shenandoah | -30% pause |
| [JEP 519](../../jeps/jep-519.md) | Compact Object Headers | -16% heap |
| [JEP 514](../../jeps/jep-514.md) | AOT Ergonomics | 更快启动 |
| [JEP 515](../../jeps/jep-515.md) | AOT Method Profiling | 更好性能 |

### 网络

| JEP | 标题 | 状态 |
|-----|------|------|
| [JEP 517](../../jeps/jep-517.md) | HTTP/3 | 正式 |

### 并发

| JEP | 标题 | 状态 |
|-----|------|------|
| [JEP 525](../../jeps/jep-525.md) | Structured Concurrency | 预览 |
| [JEP 506](../../jeps/jep-506.md) | Scoped Values | 预览 |
| [JEP 502](../../jeps/jep-502.md) | Stable Values | 正式 |

### 安全

| JEP | 标题 | 影响 |
|-----|------|------|
| [JEP 510](../../jeps/jep-510.md) | KDF API | 新 API |
| [JEP 470](../../jeps/jep-470.md) | PEM Encodings | 格式支持 |

---

## 相比 JDK 21 的新特性

### 网络

- **HTTP/3** (JEP 517)：基于 QUIC 协议，提升 UDP 场景性能
- **CUBIC 拥塞控制**：改进高延迟网络

### GC

- **G1 吞吐量提升** (JEP 522)：可达 10-20%
- **分代 Shenandoah** (JEP 521)：降低 pause 时间
- **ZGC NUMA-aware**：多插槽服务器优化

### 安全

- **ML-DSA Intrinsics**：后量子密码算法硬件加速
- **KDF API**：标准化的密钥派生接口

### 其他

- **Compact Object Headers**：减少 16% heap 开销
- **AOT 改进**：更好的启动性能和运行时性能

---

## 重要非 JEP 改动

详见 [JDK 26 重要非 JEP 改动分析](../../prs/jdk26-important-changes.md)

| 改动 | Issue | 影响 |
|------|-------|------|
| ML-DSA Intrinsics | 8371259 | 后量子密码性能 2-5x |
| HttpClient 连接泄漏修复 | 8326498 | 严重 bug 修复 |
| CUBIC 拥塞控制 | 8371475 | HTTP/3 性能优化 |
| NUMA 线程亲和性 | 8371701 | 多插槽服务器优化 |
| ZGC NUMA-Aware Relocation | 8359683 | 大内存应用优化 |
| HttpClient VirtualThread 优化 | 8372159 | 内存占用优化 |

---

## 迁移指南

### 从 JDK 21 升级

1. **破坏性变更**
   - 暂无重大破坏性变更

2. **推荐使用的新特性**
   - HTTP/3 用于网络应用
   - 虚拟线程用于 I/O 密集应用
   - 分代 ZGC 用于大内存应用

3. **性能调优**
   - 尝试启用分代 ZGC
   - 检查 G1 吞吐量提升
   - AOT 编译优化启动时间

→ [迁移指南详情](migration/from-21.md)

---

## 相关链接

- [JDK 26 发布计划](https://openjdk.org/projects/jdk/26/)
- [JDK 26 JEP 列表](https://openjdk.org/jeps/0)
- [升级到 JDK 26](migration/from-21.md)
