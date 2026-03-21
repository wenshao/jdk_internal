# Java 模块系统指南

> JPMS (Java Platform Module System) 完整指南

---

## 概述

Java 模块系统 (JPMS) 在 Java 9 引入，提供：

- **强封装**: 模块内部实现细节隐藏
- **可靠配置**: 显式依赖声明
- **可扩展平台**: 模块化 JDK

---

## 模块基础

### module-info.java

```java
module com.example.myapp {
    // 依赖其他模块
    requires java.sql;
    requires java.logging;

    // 导出包供其他模块使用
    exports com.example.myapp.api;

    // 服务提供
    provides MyService with MyServiceImpl;

    // 服务消费
    uses MyService;
}
```

### 模块描述符关键字

| 关键字 | 描述 |
|--------|------|
| `module` | 定义模块 |
| `requires` | 声明依赖 |
| `exports` | 导出包 |
| `opens` | 开放包 (反射访问) |
| `uses` | 声明服务消费 |
| `provides` | 声明服务实现 |

---

## 模块类型

### 1. 命名模块

显式定义 `module-info.java` 的模块。

### 2. 自动模块

放在模块路径上的 JAR 文件，自动成为模块。

### 3. 未命名模块

放在类路径上的 JAR 文件，属于未命名模块。

---

## 常用命令

### 编译模块

```bash
javac -d out --module-source-path src $(find src -name "*.java")
```

### 运行模块

```bash
java --module-path out --module com.example.myapp/com.example.myapp.Main
```

### 查看模块信息

```bash
# 列出所有模块
java --list-modules

# 描述模块
java -d java.sql

# 显示模块依赖
jdeps --module-path out -s myapp.jar
```

---

## 模块化 JDK

### 常用 JDK 模块

| 模块 | 描述 |
|------|------|
| `java.base` | 基础类 (自动依赖) |
| `java.sql` | JDBC API |
| `java.logging` | java.util.logging |
| `java.desktop` | AWT, Swing, JavaFX |
| `jdk.httpserver` | HTTP Server |

### 创建自定义运行时

```bash
# 使用 jlink 创建精简运行时
jlink --add-modules java.base,java.sql --output custom-jre
```

---

## 迁移到模块系统

### 迁移步骤

1. **分析依赖**: 使用 `jdeps` 分析 JAR 依赖
2. **创建模块描述符**: 添加 `module-info.java`
3. **处理自动模块**: 逐步将依赖模块化
4. **测试验证**: 确保功能正常

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| 包冲突 | 使用 `jar --upgrade` |
| 反射访问 | 使用 `--add-opens` |
| 缺失依赖 | 添加 `requires` |

---

## JDK 25+ 新特性

### JEP 511: Module Import Declarations

```java
// 导入整个模块的公共 API
import module java.sql;

// 直接使用模块中的类
Connection conn = DriverManager.getConnection(url);
```

---

## 相关资源

- [JEP 261: Module System](https://openjdk.org/jeps/261)
- [模块化 JDK 文档](https://docs.oracle.com/en/java/javase/21/docs/api/)
- [jdeps 工具指南](https://docs.oracle.com/en/java/javase/21/docs/specs/man/jdeps.html)