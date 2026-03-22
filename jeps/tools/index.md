# 工具 (Tools) JEPs

> JDK 21-26 工具相关 JEP 汇总

---
## 目录

1. [概览](#1-概览)
2. [Markdown Documentation Comments (JEP 467)](#2-markdown-documentation-comments-jep-467)
3. [Class-File API (JEP 466, 484)](#3-class-file-api-jep-466-484)
4. [Module Import Declarations (JEP 511)](#4-module-import-declarations-jep-511)
5. [Compact Source Files (JEP 512)](#5-compact-source-files-jep-512)
6. [Lazy Constants (JEP 526)](#6-lazy-constants-jep-526)
7. [相关链接](#7-相关链接)

---


## 1. 概览

| JEP | 标题 | JDK | 状态 | 说明 |
|-----|------|-----|------|------|
| [JEP 467](jep-467.md) | Markdown Documentation Comments | 23 | ✅ 正式 | Markdown 文档注释 |
| [JEP 466](jep-466.md) | Class-File API (2nd) | 23 | 🔍 预览 | ClassFile API |
| [JEP 484](jep-484.md) | Class-File API | 24 | ✅ 正式 | ClassFile API |
| [JEP 511](jep-511.md) | Module Import Declarations | 25 | ✅ 正式 | 模块导入声明 |

| [JEP 512](../language/jep-512.md) | Compact Source Files | 25 | ✅ 正式 | 紧凑源文件 |
| [JEP 526](jep-526.md) | Lazy Constants | 26 | 🔍 预览 | 凶迟常量 |

---

## 2. Markdown Documentation Comments (JEP 467)

### 核心特性

- **Markdown 格式**： 在 JavaDoc 中使用 Markdown
- **更好的可读性**： 支持代码块、列表
- **HTML 支持**: 生成 HTML 格式文档

```java
/**
 * 计算器示例
 * 
 * @param a 第一个操作数
 * @param b 第二个操作数
 * @return 计算结果
 */
public int calculate(int a, int b) {
    return a + b;
}
```

**详见**：[JEP 467](jep-467.md)

---

## 3. Class-File API (JEP 466, 484)

### 演进历程

| 版本 | JEP | 状态 |
|------|-----|------|
| JDK 22 | 457 | 🔧 孞化 |
| JDK 23 | 466 | 🔍 预览 |
| JDK 24 | 484 | ✅ 正式 |

### 核心用法

```java
// 解析 Class 文件
ClassModel model = ClassFile.of(ClassDesc.of("java/lang/String"));
for (FieldModel field : model.fields()) {
    System.out.println(field.fieldName() + ": " + field.fieldType());
}
```

**详见**：[JEP 466](jep-466.md) | [JEP 484](jep-484.md)

---

## 4. Module Import Declarations (JEP 511)

### 核心特性

- **模块级别导入**： 壽令式模块导入
- **更清晰的依赖**： 明确声明模块依赖
- **工具支持**： jdeps, jlink 等支持分析

```java
// 模块导入声明
module com.example.myapp {
    requires java.sql;  // 娡块依赖
    exports com.example.api;
}
```

**详见**：[JEP 511](jep-511.md)

---

## 5. Compact Source Files (JEP 512)

### 核心特性

- **单文件发布**： 将多个文件合并为单文件
- **更快启动**： 减少 I/O
- **更小体积**： 减少部署大小

**详见**：[JEP 512](../language/jep-512.md)

---

## 6. Lazy Constants (JEP 526)

### 核心特性

- **延迟初始化**： 常量在首次使用时初始化
- **性能优化**： 减少启动时间
- **灵活控制**： 支持运行时配置

```java
// 凶迟常量
private static final String CONFIG = Lazy.of(() -> loadConfig());

private static String loadConfig() {
    // 首次访问时加载
    return System.getenv("APP_CONFIG");
}
```

**详见**：[JEP 526](jep-526.md)

---

## 7. 相关链接

- [JEP 467: Markdown Documentation Comments](https://openjdk.org/jeps/467)
- [JEP 484: Class-File API](https://openjdk.org/jeps/484)
- [JEP 511: Module Import Declarations](https://openjdk.org/jeps/511)
