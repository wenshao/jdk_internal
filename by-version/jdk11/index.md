# JDK 11

> **状态**: LTS (长期支持) | **GA 发布**: 2018-09-25 | **类型**: Long Term Support

[![OpenJDK](https://img.shields.io/badge/OpenJDK-11-orange)](https://openjdk.org/projects/jdk/11/)
[![LTS](https://img.shields.io/badge/LTS-2028--purple.svg)](https://www.oracle.com/java/technologies/java-se-support.html)

---

## 版本概览

JDK 11 是继 JDK 8 之后的首个 LTS 版本，包含多项重要改进：

| 特性 | 说明 |
|------|------|
| **HTTP Client（正式版）** | 新的 HTTP 客户端 API |
| **ZGC（实验）** | 低延迟 GC |
| **Flight Recorder（正式版）** | 生产环境性能分析 |
| **Nest-Based Access Control** | 简化私有访问 |
| **Lambda 局部变量类型推断** | var 关键字 |
| **Epsilon GC** | 被动 GC，用于性能测试 |
| **动态类文件常量** | JEP 309 |

---

## GC 状态

| GC | 状态 | 说明 |
|----|------|------|
| **G1 GC** | 默认 | 均衡性能和延迟 |
| **ZGC** | 实验 (JEP 333) | Linux，低延迟 |
| **Shenandoah** | 实验 | 低延迟 GC |
| **Epsilon GC** | 正式 (JEP 318) | 被动 GC |

---

## 迁移指南

### 从 JDK 8 升级

**重要变更**:
- **HTTP Client 正式版**：替代 HttpURLConnection
- **Flight Recorder 正式版**：生产环境性能分析
- **var 关键字支持 Lambda**：局部变量类型推断扩展
- `java.util.logging` 从默认 JDK 中移除
- `JavaFX` 从 JDK 中分离
- `Pack200` 工具移除

**推荐配置**:
```bash
-XX:+UseG1GC           # G1 仍然是默认
-XX:MaxGCPauseMillis=200  # 目标暂停时间
-XX:+UseZGC            # 尝试 ZGC (实验)
```

---

## 相关链接

- [JDK 11 发布说明](https://openjdk.org/projects/jdk/11/)
- [从 JDK 8 迁移](https://docs.oracle.com/en/java/javase/11/migrate/)
- [ZGC 文档](https://openjdk.org/jeps/333)
