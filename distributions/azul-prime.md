# Azul Platform Prime

> Azul Systems 提供的高性能 JDK 发行版 (C4 GC)

[← 返回发行版](../distributions/)

---

## 概述

Azul Platform Prime (前身为 Azul Zing) 是 Azul Systems 提供的高性能 JDK 发行版，以 C4 低延迟垃圾回收器著称。

| 属性 | 值 |
|------|-----|
| **组织** | Azul Systems |
| **官网** | https://www.azul.com/products/azul-platform-prime/ |
| **许可证** | 商业 |
| **商业支持** | ✅ |
| **核心特性** | C4 GC |

---

## C4 GC

### 特性

C4 (Continuously Concurrent Compacting Collector) 是 Azul 独有的垃圾回收器：

| 特性 | 说明 |
|------|------|
| **低延迟** | Pause 时间 < 1ms |
| **无 Stop-The-World** | 完全并发执行 |
| **大堆内存** | 支持 TB 级堆 |
| **压缩** | 持续压缩，无碎片 |

### 对比

| 特性 | G1 GC | ZGC | Shenandoah | C4 GC |
|------|-------|-----|------------|-------|
| Pause 时间 | 10-200ms | < 1ms | < 10ms | < 1ms |
| 最大堆 | 32GB | 16TB | 16TB | TB+ |
| 压缩 | 有限 | 是 | 是 | 是 |
| 商业 | ❌ | ❌ | ❌ | ✅ |

---

## 性能

### 基准测试

| 指标 | Prime | OpenJDK |
|------|-------|---------|
| 吞吐量 | 110-130% | 100% |
| GC Pause | < 1ms | 10-200ms |
| 堆内存 | TB+ | 32GB (推荐) |

### 适用场景

- **金融交易**: 低延迟要求
- **游戏服务器**: 大内存，低 GC
- **大数据处理**: TB 级堆内存
- **实时系统**: 可预测延迟

---

## 安装

Azul Platform Prime 需要商业订阅。

```bash
# 下载 (需要订阅)
# 访问 https://www.azul.com/downloads/

# 安装
tar -xzf zprime21-jdk21-linux_x64.tar.gz
export JAVA_HOME=$PWD/zulu21-prime
export PATH=$JAVA_HOME/bin:$PATH

# 验证
java -version
# openjdk version "21.0.1" 2023-10-17 LTS
# OpenJDK Runtime Environment Azul Platform Prime Builds (build 21.0.1+12-LTS)
# OpenJDK 64-Bit Server VM Azul Platform Prime Builds (build 21.0.1+12-LTS, mixed mode)
```

---

## 定价

### Azul Platform Prime

| 版本 | 年度订阅 (每处理器) |
|------|---------------------|
| Prime | $2,500+ |

**包含**:
- C4 GC
- 24/7 技术支持
- Mission Control
- 性能分析工具

---

## 相关链接

- [Azul Platform Prime](https://www.azul.com/products/azul-platform-prime/)
- [C4 GC 白皮书](https://www.azul.com/products/azul-platform-prime/c4-garbage-collector/)

---

**最后更新**: 2026-03-20
