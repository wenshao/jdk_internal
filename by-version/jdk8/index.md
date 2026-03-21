# JDK 8

> **状态**: LTS (长期支持) | **GA 发布**: 2014-03-18 | **类型**: Long Term Support

[![OpenJDK](https://img.shields.io/badge/OpenJDK-8-blue)](https://openjdk.org/projects/jdk8/)
[![LTS](https://img.shields.io/badge/LTS-Extended--purple.svg)](https://www.oracle.com/java/technologies/java-se-support.html)

---

## 版本概览

JDK 8 是一个具有里程碑意义的版本，引入了 Lambda 表达式、Stream API 等重大特性：

| 特性 | 说明 |
|------|------|
| **Lambda 表达式** | 函数式编程基础 |
| **Stream API** | 集合操作新方式 |
| **日期时间 API** | 全新的 java.time 包 |
| **默认方法** | 接口默认实现 |
| **类型注解** | 更强的类型检查 |
| **重复注解** | 同一注解多次使用 |
| **方法引用** | Lambda 简化语法 |
| **Optional** | 空值处理 |
| **CompletableFuture** | 异步编程 |
| **Base64 编码** | 内置 Base64 支持 |
| **PermGen 移除** | 替换为 Metaspace |

---

## GC 状态

| GC | 状态 | 说明 |
|----|------|------|
| **ParallelGC** | 默认 | 高吞吐量 |
| **G1 GC** | 可选 | 低延迟，JDK 9 成为默认 |
| **CMS** | 已废弃 | JDK 9 标记废弃，JDK 14 移除 |

---

## 迁移指南

### 从 JDK 7 升级

**破坏性变更**:
- `PermGen` 移除，替换为 `Metaspace`
- `URLClassLoader` 不再搜索 `sun.*` 包

**推荐配置**:
```bash
-XX:+UseG1GC           # 使用 G1 GC
-XX:MaxMetaspaceSize=256m  # 元空间大小
```

---

## 相关链接

- [JDK 8 发布说明](https://openjdk.org/projects/jdk8/)
- [JDK 8 文档](https://docs.oracle.com/javase/8/)
- [Lambda 指南](https://docs.oracle.com/javase/tutorial/java/javaOO/lambdaexpressions.html)
