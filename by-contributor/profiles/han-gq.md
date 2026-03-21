# Han Guanqiang (han gq)

> JDK 26 编译器优化贡献者，麒麟软件 (KylinSoft)，2 个 commits

---
## 目录

1. [基本信息](#1-基本信息)
2. [贡献概览](#2-贡献概览)
3. [PR 列表](#3-pr-列表)
4. [关键贡献详解](#4-关键贡献详解)
5. [开发风格](#5-开发风格)
6. [相关链接](#6-相关链接)

---


## 1. 基本信息

| 属性 | 值 |
|------|-----|
| **姓名** | Han Guanqiang (韩冠强) |
| **当前组织** | 麒麟软件 (KylinSoft) |
| **GitHub** | [@hanguanqiang](https://github.com/hanguanqiang) |
| **OpenJDK** | Author |
| **主要领域** | 编译器优化 |
| **活跃时间** | 2024 - 至今 |

> **数据调查时间**: 2026-03-19

---

## 2. 贡献概览

### 按类别统计

| 类别 | 数量 | 占比 |
|------|------|------|
| 编译器优化 | 1 | 50% |
| 文档修复 | 1 | 50% |

### 关键成就

- 指针比较优化修复
- 代码缓存文档修复

---

## 3. PR 列表

### 编译器优化

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8361140 | Missing OptimizePtrCompare check in ConnectionGraph::reduce_phi_on_cmp | [JBS-8361140](https://bugs.openjdk.org/browse/JDK-8361140) |

### 文档修复

| Issue | 标题 | PR 链接 |
|-------|------|---------|
| 8344548 | Incorrect StartAggressiveSweepingAt doc for segmented code cache | [JBS-8344548](https://bugs.openjdk.org/browse/JDK-8344548) |

---

## 4. 关键贡献详解

### 1. 指针比较优化修复 (JDK-8361140)

**问题**: ConnectionGraph::reduce_phi_on_cmp 缺少 OptimizePtrCompare 检查。

**解决方案**: 添加缺失的检查。

```cpp
// 变更前: 缺少检查
Node* ConnectionGraph::reduce_phi_on_cmp(Node* phi, Node* cmp) {
  // 直接处理
  return process_phi(phi, cmp);
}

// 变更后: 添加检查
Node* ConnectionGraph::reduce_phi_on_cmp(Node* phi, Node* cmp) {
  if (!OptimizePtrCompare) {
    return NULL;  // 未启用优化，直接返回
  }
  return process_phi(phi, cmp);
}
```

**影响**: 修复了编译器优化问题。

### 2. 代码缓存文档修复 (JDK-8344548)

**问题**: StartAggressiveSweepingAt 参数文档不正确。

**解决方案**: 修正文档描述。

```
变更前:
StartAggressiveSweepingAt: 开始激进清扫的阈值

变更后:
StartAggressiveSweepingAt: 当分段代码缓存使用率达到此阈值时，
开始激进清扫。仅对分段代码缓存有效。
```

**影响**: 改进了参数文档准确性。

---

## 5. 开发风格

han gq 的贡献特点:

1. **麒麟软件**: 代表麒麟软件在 OpenJDK 的贡献
2. **编译器优化**: 关注编译器内部优化
3. **文档改进**: 同时改进文档

---

## 6. 相关链接

- [GitHub Commits](https://github.com/openjdk/jdk/commits?author=han%20gq)
- [JBS Issues](https://bugs.openjdk.org/issues/?jql=reporter%20%3D%20hanguanqiang)