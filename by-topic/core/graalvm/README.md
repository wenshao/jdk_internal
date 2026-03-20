# GraalVM 文档导航

> GraalVM 主题文档完整索引

[← 返回核心平台](../)

---

## 文档结构

```
graalvm/
├── 📘 index.md              # 主页面 - 快速概览
├── 📊 benchmarks.md         # 性能基准测试
├── ⚙️ performance.md        # 性能优化技术
├── 🏗️ architecture.md       # 架构详解
├── 🔧 native-image-guide.md # Native Image 指南
├── ⚔️ graal-vs-c2.md        # Graal vs C2 对比
├── ❓ faq.md                # 常见问题
├── 📖 glossary.md           # 术语表
├── 📚 case-studies.md       # 案例研究
└── 🔍 deep-dive.md          # 深度分析
```

---

## 文档索引

### 入门文档

| 文档 | 说明 | 适合人群 |
|------|------|----------|
| [index.md](index.md) | 📘 GraalVM 主页面，快速概览 | 所有人 |
| [faq.md](faq.md) | ❓ 常见问题解答 | 初学者 |
| [glossary.md](glossary.md) | 📖 术语和缩略语解释 | 所有人 |

### 性能相关

| 文档 | 说明 | 适合人群 |
|------|------|----------|
| [benchmarks.md](benchmarks.md) | 📊 官方和第三方性能基准测试 | 性能工程师 |
| [performance.md](performance.md) | ⚙️ Graal JIT、Native Image、Truffle 优化技术 | 高级开发者 |
| [case-studies.md](case-studies.md) | 📚 真实世界性能优化案例 | 架构师 |

### 技术深入

| 文档 | 说明 | 适合人群 |
|------|------|----------|
| [architecture.md](architecture.md) | 🏗️ GraalVM 内部架构详解 | 编译器开发者 |
| [graal-vs-c2.md](graal-vs-c2.md) | ⚔️ Graal 与 C2 编译器技术对比 | JIT 开发者 |
| [native-image-guide.md](native-image-guide.md) | 🔧 Native Image 配置最佳实践 | 云原生开发者 |

### 背景分析

| 文档 | 说明 | 适合人群 |
|------|------|----------|
| [deep-dive.md](deep-dive.md) | 🔍 Oracle 内部冲突和技术决策分析 | 技术管理者 |
| [index.md#graalvm-发展史](index.md#graalvm-发展史) | 📜 GraalVM 发展历史 | 所有人 |

---

## 学习路径

### 初学者路径

```
1. index.md          → 了解 GraalVM 是什么
       ↓
2. faq.md            → 解答常见问题
       ↓
3. glossary.md       → 学习术语
       ↓
4. benchmarks.md     → 查看性能数据
```

### 开发者路径

```
1. index.md          → 快速概览
       ↓
2. performance.md    → 学习优化技术
       ↓
3. native-image-guide.md → 实践 Native Image
       ↓
4. graal-vs-c2.md    → 深入理解编译器
```

### 架构师路径

```
1. index.md          → 整体了解
       ↓
2. architecture.md   → 理解架构
       ↓
3. case-studies.md   → 学习最佳实践
       ↓
4. deep-dive.md      → 理解技术决策
```

### 研究者路径

```
1. deep-dive.md      → 了解历史背景
       ↓
2. architecture.md   → 研究技术实现
       ↓
3. graal-vs-c2.md    → 对比分析
       ↓
4. performance.md    → 性能分析
```

---

## 快速查找

### 我想了解...

| 问题 | 查看文档 |
|------|----------|
| GraalVM 是什么？ | [index.md](index.md) |
| 性能提升多少？ | [benchmarks.md](benchmarks.md) |
| 如何构建 Native Image？ | [native-image-guide.md](native-image-guide.md) |
| 为什么 Graal 更快？ | [performance.md](performance.md) |
| Graal 和 C2 有什么区别？ | [graal-vs-c2.md](graal-vs-c2.md) |
| 如何配置反射？ | [native-image-guide.md](native-image-guide.md#反射配置) |
| 遇到错误怎么办？ | [faq.md](faq.md#故障排查) |
| 术语不懂怎么办？ | [glossary.md](glossary.md) |
| 有成功案例吗？ | [case-studies.md](case-studies.md) |
| Oracle 内部有什么冲突？ | [deep-dive.md](deep-dive.md) |

### 我想...

| 目标 | 查看文档 |
|------|----------|
| 快速上手 GraalVM | [index.md](index.md#快速开始) |
| 优化应用性能 | [performance.md](performance.md) |
| 迁移到 Native Image | [native-image-guide.md](native-image-guide.md) |
| 了解架构原理 | [architecture.md](architecture.md) |
| 对比编译器 | [graal-vs-c2.md](graal-vs-c2.md) |
| 查看性能数据 | [benchmarks.md](benchmarks.md) |
| 学习最佳实践 | [case-studies.md](case-studies.md) |
| 解决常见问题 | [faq.md](faq.md) |

---

## 文档统计

| 指标 | 数值 |
|------|------|
| **文档总数** | 10 篇 |
| **总字数** | ~50,000 字 |
| **代码示例** | 100+ |
| **性能数据** | 50+ 组 |
| **案例研究** | 8 个 |

---

## 贡献指南

### 发现错误？

1. 检查 [GitHub Issues](https://github.com/oracle/graal/issues)
2. 在邮件列表讨论：graalvm-dev@openjdk.org

### 想贡献内容？

1. Fork 仓库
2. 创建分支
3. 提交 PR
4. 等待审核

---

## 相关资源

### 官方资源
- [GraalVM 官网](https://www.graalvm.org/)
- [GraalVM GitHub](https://github.com/oracle/graal)
- [官方文档](https://www.graalvm.org/latest/docs/)

### 社区资源
- [Stack Overflow](https://stackoverflow.com/questions/tagged/graalvm)
- [GraalVM Slack](https://graalvm.slack.com/)
- [Mailing List](mailto:graalvm-dev@openjdk.org)

### 相关主题
- [JIT 编译](../jit/)
- [性能优化](../performance/)
- [JEP 243: JVMCI](../../../jeps/compiler/jep-243.md)

---

**最后更新**: 2026-03-21

**维护者**: JDK Internal Documentation Project
