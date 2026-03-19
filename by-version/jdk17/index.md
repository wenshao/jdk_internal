# JDK 17

> **状态**: LTS (长期支持) | **GA 发布**: 2021-09-14 | **类型**: Long Term Support

[![OpenJDK](https://img.shields.io/badge/OpenJDK-17-orange)](https://openjdk.org/projects/jdk/17/)
[![LTS](https://img.shields.io/badge/LTS-2029--purple.svg)](https://www.oracle.com/java/technologies/java-se-support.html)

---

## 版本概览

JDK 17 是最新的 LTS 版本，包含多项重要新特性：

| 特性 | 状态 | 说明 |
|------|------|------|
| **Sealed Classes** | 正式 | 密封类 |
| **Pattern Matching** | 预览 | instanceof 模式匹配 |
| **Records** | 正式 | 记录类 |
| **Text Blocks** | 正式 | 文本块 |
| **Foreign Function Interface** | 正式 | Java 原生互连 |
| **Virtual Threads** | 实验性 | 虚拟线程（孵化） |

---

## GC 状态

| GC | 状态 | 说明 |
|----|------|------|
| **G1 GC** | 默认 | 持续优化 |
| **ZGC** | 正式 | 生产可用 |
| **Shenandoah** | 正式 | 生产可用 |

---

## 迁移指南

### 从 JDK 11 升级

**破坏性变更**:
- `Security Manager` 部分功能弃用
- `rmiregistry` 工具移除

**推荐配置**:
```bash
-XX:+UseZGC             # 尝试 ZGC
-XX:+ZGenerational      # JDK 21+ 特性
```

---

## 相关链接

- [JDK 17 发布说明](https://openjdk.org/projects/jdk/17/)
- [JDK 17 新特性](https://openjdk.org/projects/jdk/17/features)
- [Sealed Classes 指南](https://openjdk.org/jeps/409)
