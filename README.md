# JDK Docs

> 参考 [openjdk/jdk](https://github.com/openjdk/jdk) 仓库，分析 JDK issue、pull request 和源码，沉淀便于人类和 AI 阅读的文档。

## 目录结构

```
jdk_docs/
├── README.md          # 项目说明
├── releases/          # 版本发布分析
│   └── jdk26.md       # JDK 26 发布说明
├── jeps/              # JEP 详细分析
│   ├── jep-502.md     # Stable Values
│   ├── jep-503.md     # Remove 32-bit x86
│   ├── jep-504.md     # Remove Applet API
│   ├── jep-511.md     # Module Import Declarations
│   ├── jep-512.md     # Compact Source Files
│   ├── jep-517.md     # HTTP/3
│   └── jep-522.md     # G1 GC Throughput
├── issues/            # Issue 分析文档
├── prs/               # Pull Request 分析文档
└── modules/           # 模块/组件源码分析文档
```

## 文档规范

- **Issue 文档**：背景、问题分析、解决方案、相关代码
- **PR 文档**：改动概述、代码变更分析、测试验证、影响范围
- **模块文档**：架构概述、核心类解析、设计模式、使用示例

## 相关链接

- [OpenJDK 官网](https://openjdk.org/)
- [GitHub: openjdk/jdk](https://github.com/openjdk/jdk)
- [JDK Bug System (JBS)](https://bugs.openjdk.org/)