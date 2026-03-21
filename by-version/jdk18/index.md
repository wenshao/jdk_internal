# JDK 18

> **发布日期**: 2022-03-22 | **类型**: Feature Release

---
## 目录

1. [核心特性](#1-核心特性)
2. [关键 JEP](#2-关键-jep)
3. [代码示例](#3-代码示例)
4. [相关链接](#4-相关链接)

---


## 1. 核心特性

JDK 18 引入了 UTF-8 作为默认字符集、Simple Web Server 和 Vector API（第2次孵化）。

| 特性 | 影响 | 详情 |
|------|------|------|
| **UTF-8 默认字符集** | ⭐⭐⭐⭐ | JEP 400 |
| **Simple Web Server** | ⭐⭐⭐ | JEP 408 |
| **Vector API（第2次孵化）** | ⭐⭐⭐ | JEP 414 |
| **代码片段** | ⭐⭐⭐ | JEP 413 |
| **Foreign Function & Memory API** | ⭐⭐⭐ | JEP 419，第2次孵化 |
| **@Snippets** | ⭐⭐⭐ | JEP 413 |

---

## 2. 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 400](https://openjdk.org/jeps/400) | UTF-8 by Default | UTF-8 默认字符集 |
| [JEP 408](https://openjdk.org/jeps/408) | Simple Web Server | 简单 Web 服务器 |
| [JEP 413](https://openjdk.org/jeps/413) | Code Snippets in Java API Documentation | 代码片段 |
| [JEP 416](https://openjdk.org/jeps/416) | Reimplement Core Reflection with Method Handles | 方法句柄重构反射 |
| [JEP 417](https://openjdk.org/jeps/417) | Vector API (Third Incubator) | Vector API（第3次孵化） |
| [JEP 421](https://openjdk.org/jeps/421) | Deprecate Finalization for Removal | 废弃 Finalization |

---

## 3. 代码示例

### UTF-8 默认字符集

```java
// JDK 18 之前依赖于系统
// JDK 18: UTF-8 是默认值
Charset default = Charset.defaultCharset(); // UTF-8

Files.writeString(Path.of("file.txt"), "Hello 世界");
// 自动使用 UTF-8
```

### Simple Web Server

```bash
# 启动简单 Web 服务器
java -m jdk.httpserver

# 指定端口和目录
java -m jdk.httpserver -p 8080 -d /path/to/files
```

---

## 4. 相关链接

- [发布说明](https://openjdk.org/projects/jdk/18/)
