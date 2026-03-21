# JDK 17

> **状态**: LTS (长期支持) | **GA 发布**: 2021-09-14 | **类型**: Long Term Support

[![OpenJDK](https://img.shields.io/badge/OpenJDK-17-orange)](https://openjdk.org/projects/jdk/17/)
[![LTS](https://img.shields.io/badge/LTS-2029--purple.svg)](https://www.oracle.com/java/technologies/java-se-support.html)

---

## 版本概览

JDK 17 是继 JDK 11 之后的 LTS 版本，包含多项重要新特性：

| 特性 | 状态 | 说明 |
|------|------|------|
| **Sealed Classes** | 正式 (JEP 409) | 密封类 |
| **Records** | 正式 (JEP 395) | 记录类 |
| **Text Blocks** | 正式 (JEP 378) | 文本块 |
| **Pattern Matching for instanceof** | 预览 (JEP 394) | instanceof 模式匹配 |
| **Foreign Function & Memory API** | 孵化 (JEP 412) | Java 原生互连 |
| **Vector API** | 孵化 (JEP 417) | 向量 API |
| **Context-Specific Deserialization Filters** | 正式 (JEP 415) | 反序列化过滤 |

---

## GC 状态

| GC | 状态 | 说明 |
|----|------|------|
| **G1 GC** | 默认 | 持续优化 |
| **ZGC** | 实验 (JEP 333) | 低延迟 GC，JDK 15 正式 |
| **Shenandoah** | 实验 | 低延迟 GC |

---

## 迁移指南

### 从 JDK 11 升级

**重要变更**:
- **Sealed Classes 正式版**：限制继承的类
- **Records 正式版**：不可变数据类
- **Text Blocks 正式版**：多行字符串
- **强封装**：JDK 内部 API 默认不可访问
- `Security Manager` 部分功能弃用
- `rmiregistry` 工具移除

**推荐配置**:
```bash
-XX:+UseZGC             # 尝试 ZGC (实验)
-XX:+ZGenerational      # 需要 JDK 21+
```

---

## 相关链接

- [JDK 17 发布说明](https://openjdk.org/projects/jdk/17/)
- [JDK 17 新特性](https://openjdk.org/projects/jdk/17/features)
- [Sealed Classes 指南](https://openjdk.org/jeps/409)
