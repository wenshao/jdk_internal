# JDK Docs

> 参考 [openjdk/jdk](https://github.com/openjdk/jdk) 仓库，分析 JDK issue、pull request 和源码，沉淀便于人类和 AI 阅读的文档。

---

## 快速开始

| 角色 | 推荐入口 |
|------|----------|
| 初学者 | [学习路径](guides/learning-path.md) |
| 开发者 | [速查表](guides/cheat-sheet.md) |
| 架构师 | [迁移指南](guides/migration-guide.md) |
| 所有人 | [FAQ](guides/faq.md) |

---

## 目录结构

```
jdk_docs/
├── README.md              # 项目说明 (本文件)
├── releases/              # 版本发布分析
│   └── jdk26.md           # JDK 26 发布说明
├── jeps/                  # JEP 详细分析 (21个)
│   ├── jep-470.md         # PEM Encodings
│   ├── jep-500.md         # Make Final Mean Final
│   ├── jep-502.md         # Stable Values
│   ├── jep-503.md         # Remove 32-bit x86
│   ├── jep-504.md         # Remove Applet API
│   ├── jep-506.md         # Scoped Values
│   ├── jep-509.md         # JFR CPU-Time Profiling
│   ├── jep-510.md         # KDF API
│   ├── jep-511.md         # Module Import Declarations
│   ├── jep-512.md         # Compact Source Files
│   ├── jep-514.md         # AOT Command Line Ergonomics
│   ├── jep-515.md         # AOT Method Profiling
│   ├── jep-517.md         # HTTP/3
│   ├── jep-518.md         # JFR Cooperative Sampling
│   ├── jep-519.md         # Compact Object Headers
│   ├── jep-520.md         # JFR Method Timing
│   ├── jep-521.md         # Generational Shenandoah
│   ├── jep-522.md         # G1 GC Throughput
│   ├── jep-525.md         # Structured Concurrency
│   ├── jep-526.md         # Lazy Constants
│   └── jep-530.md         # Primitive Types in Patterns
├── deep-dive/             # 深入源码分析
│   ├── jep-511-implementation.md  # 模块导入实现
│   ├── jep-517-implementation.md  # HTTP/3 实现
│   └── jep-522-implementation.md  # G1 GC 优化实现
├── guides/                # 指南文档
│   ├── learning-path.md   # 学习路径
│   ├── cheat-sheet.md     # 速查表
│   ├── migration-guide.md # 迁移指南
│   └── faq.md             # 常见问题
├── issues/                # Issue 分析文档
├── prs/                   # Pull Request 分析文档
└── modules/               # 模块/组件源码分析文档
```

---

## 文档规范

- **JEP 文档**: 背景、使用示例、实现分析、开发者影响、性能数据
- **深入分析**: 源码解读、设计决策、关键变更
- **指南文档**: 按角色分类、实用代码、配置建议

---

## 按主题浏览

### 🚀 性能优化
- [JEP 522: G1 GC Throughput](jeps/jep-522.md) | [深入分析](deep-dive/jep-522-implementation.md)
- [JEP 521: Generational Shenandoah](jeps/jep-521.md)
- [JEP 519: Compact Object Headers](jeps/jep-519.md)
- [JEP 514: AOT Ergonomics](jeps/jep-514.md)
- [JEP 515: AOT Profiling](jeps/jep-515.md)

### 📝 语言特性
- [JEP 511: Module Import](jeps/jep-511.md) | [深入分析](deep-dive/jep-511-implementation.md)
- [JEP 512: Compact Source Files](jeps/jep-512.md)
- [JEP 530: Primitive Patterns](jeps/jep-530.md)
- [JEP 526: Lazy Constants](jeps/jep-526.md)

### 🔄 并发编程
- [JEP 525: Structured Concurrency](jeps/jep-525.md)
- [JEP 506: Scoped Values](jeps/jep-506.md)
- [JEP 502: Stable Values](jeps/jep-502.md)

### 🌐 网络编程
- [JEP 517: HTTP/3](jeps/jep-517.md) | [深入分析](deep-dive/jep-517-implementation.md)

### 🔐 安全
- [JEP 500: Make Final Mean Final](jeps/jep-500.md)
- [JEP 510: KDF API](jeps/jep-510.md)
- [JEP 470: PEM Encodings](jeps/jep-470.md)

### 📊 监控诊断
- [JEP 509: JFR CPU-Time](jeps/jep-509.md)
- [JEP 518: JFR Cooperative Sampling](jeps/jep-518.md)
- [JEP 520: JFR Method Timing](jeps/jep-520.md)

---

## 相关链接

- [OpenJDK 官网](https://openjdk.org/)
- [GitHub: openjdk/jdk](https://github.com/openjdk/jdk)
- [JDK Bug System (JBS)](https://bugs.openjdk.org/)