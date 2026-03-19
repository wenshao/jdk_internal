# JDK PR 分析索引

> 本仓库索引 JDK 重要的 PR 和 Issue 分析文档

---

## 文件组织

```
prs/
├── {前4位Issue号}/     # 如 8371/ 代表 8371000-8371999
│   ├── {完整Issue号}.md   # 如 8371259.md
│   └── jep{JEP号}-{名称}.md  # JEP 相关文档
├── index.md            # 本文件
├── jdk-history.md      # JDK 历史概览
├── jdk26-contributors.md
└── jdk26-important-changes.md
```

**URL 规则**: `prs/{前4位}/{Issue号}.md`
- 例如: `prs/8371/8371259.md`

---

## JDK 26 重要改动 (已分析)

### 🔴 严重问题

| Issue | 标题 | 作者 | 文档 |
|-------|------|------|------|
| 8326498 | HTTP/2 连接泄漏修复 | Jaikiran Pai | [8326/8326498.md](./8326/8326498.md) |

### ⭐⭐⭐ 安全

| Issue | 标题 | 作者 | 文档 |
|-------|------|------|------|
| 8371259 | ML-DSA Intrinsics | Volodymyr Paprotski | [8371/8371259.md](./8371/8371259.md) |
| 8347606 | ML-KEM 后量子密钥交换 | Weijun Wang | [8347/8347606.md](./8347/8347606.md) |

### ⭐⭐⭐ 网络 (HttpClient)

| Issue | 标题 | 作者 | 文档 |
|-------|------|------|------|
| 8371475 | CUBIC 拥塞控制 | Daniel Jeliński | [8371/8371475.md](./8371/8371475.md) |
| 8372159 | VirtualThread 优化 | Daniel Fuchs | [8372/8372159.md](./8372/8372159.md) |

### ⭐⭐⭐ GC

| Issue | 标题 | 作者 | 文档 |
|-------|------|------|------|
| 8372162 | G1 Claim Table 优化 | Albert Mingkun Yang | [8372/8372162.md](./8372/8372162.md) |
| 8359683 | ZGC NUMA-Aware Relocation | Joel Sikström | [8359/8359683.md](./8359/8359683.md) |
| JEP 521 | 分代 Shenandoah | William Kemper | [8370/jep521-generational-shenandoah.md](./8370/jep521-generational-shenandoah.md) |

### ⭐⭐⭐ 编译器 (C2)

| Issue | 标题 | 作者 | 文档 |
|-------|------|------|------|
| 8371146 | SuperWord 向量化优化 | Hamlin Li | [8371/8371146.md](./8371/8371146.md) |

### ⭐⭐⭐ 性能与并发

| Issue | 标题 | 作者 | 文档 |
|-------|------|------|------|
| 8371701 | NUMA 线程亲和性 | Joel Sikström | [8371/8371701.md](./8371/8371701.md) |

### ⭐⭐⭐ JNI

| Issue | 标题 | 作者 | 文档 |
|-------|------|------|------|
| 8298432 | GetPrimitiveArrayCritical 优化 | Albert Mingkun Yang | [8298/8298432.md](./8298/8298432.md) |

### ⭐⭐⭐ 核心库

| Issue | 标题 | 作者 | 文档 |
|-------|------|------|------|
| 8371953 | 反射 API 优化 | Chen Liang | [8371/8371953.md](./8371/8371953.md) |

### ⭐⭐⭐ 启动优化

| Issue | 标题 | 作者 | 文档 |
|-------|------|------|------|
| JEP 514 | AOT 链接启动优化 | Ioi Lam | [8370/jep514-aot-linking.md](./8370/jep514-aot-linking.md) |
| JEP 519 | Compact Object Headers | Roman Kennke | [8370/jep519-compact-headers.md](./8370/jep519-compact-headers.md) |

### ⭐⭐⭐ 监控诊断

| Issue | 标题 | 作者 | 文档 |
|-------|------|------|------|
| JEP 520 | JFR 方法计时追踪 | Erik Gahlin | [8370/jep520-jfr-method-timing.md](./8370/jep520-jfr-method-timing.md) |

### ⭐⭐ 构建

| Issue | 标题 | 作者 | 文档 |
|-------|------|------|------|
| 8371626 | Linux ICF 链接优化 | Aleksey Shipilev | [8371/8371626.md](./8371/8371626.md) |

---

## 按类别浏览

### GC 优化
- [G1 Claim Table](./8372/8372162.md) - 吞吐量 +10-15%
- [ZGC NUMA-Aware](./8359/8359683.md) - 吞吐量 +20-35%
- [分代 Shenandoah](./8370/jep521-generational-shenandoah.md) - 吞吐量 +20-40%

### 网络优化
- [HTTP/2 连接泄漏](./8326/8326498.md) - 🔴 严重
- [CUBIC 拥塞控制](./8371/8371475.md) - 高延迟网络 +35-60%
- [VirtualThread 优化](./8372/8372159.md) - 资源 -1000x

### 后量子安全
- [ML-DSA Intrinsics](./8371/8371259.md) - 签名性能 +2-5x
- [ML-KEM 实现](./8347/8347606.md) - 密钥交换

### 启动与内存
- [AOT 链接](./8370/jep514-aot-linking.md) - 启动 -30-50%
- [Compact Headers](./8370/jep519-compact-headers.md) - 内存 -12-25%

---

## 按作者浏览

### 顶级贡献者

| 作者 | 贡献数 | 主要领域 | 详细分析 |
|------|--------|----------|----------|
| Albert Mingkun Yang | 2 | GC, JNI | [contributors/albert-mingkun-yang.md](../contributors/albert-mingkun-yang.md) |
| Joel Sikström | 2 | NUMA, ZGC | [contributors/joel-sikstrom.md](../contributors/joel-sikstrom.md) |
| Daniel Fuchs | 1 | HttpClient | [contributors/daniel-fuchs.md](../contributors/daniel-fuchs.md) |
| Chen Liang | 1 | 核心库 | [contributors/chen-liang.md](../contributors/chen-liang.md) |
| Ioi Lam | 1 | AOT/CDS | [contributors/ioi-lam.md](../contributors/ioi-lam.md) |
| Roman Kennke | 1 | 对象布局 | [contributors/roman-kennke.md](../contributors/roman-kennke.md) |

---

## 统计

| 指标 | 值 |
|------|-----|
| 已分析 PR 数量 | 16 |
| 覆盖 JDK 版本 | 26 |
| 覆盖类别 | 10 |

---

## 相关链接

- [JDK 26 JEP 列表](https://openjdk.org/projects/jdk/26/)
- [OpenJDK Bug System](https://bugs.openjdk.org/)
- [JDK Commit History](https://github.com/openjdk/jdk/commits/)

---

## 如何添加新的 PR 分析

1. 确定目录: `prs/{Issue号前4位}/`
2. 创建文件: `{完整Issue号}.md`
3. 更新索引: 添加到本文件相应类别
4. 提交 PR

文件命名规则:
- Issue: `{Issue号}.md` (如 `8371259.md`)
- JEP: `jep{JEP号}-{简短名称}.md` (如 `jep521-generational-shenandoah.md`)
