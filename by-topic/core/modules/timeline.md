# 模块系统演进时间线

Java 模块系统 (JPMS) 从 JDK 9 到 JDK 25 的完整演进历程。

---
## 目录

1. [时间线概览](#1-时间线概览)
2. [为什么需要模块系统](#2-为什么需要模块系统)
3. [JDK 9 - JPMS (JEP 261)](#3-jdk-9---jpms-jep-261)
4. [模块类型](#4-模块类型)
5. [模块命令](#5-模块命令)
6. [JDK 11+ - 模块增强](#6-jdk-11---模块增强)
7. [JDK 16+ - 封装增强](#7-jdk-16---封装增强)
8. [JDK 17+ - 遗留封装](#8-jdk-17---遗留封装)
9. [JDK 23+ - 模块导入声明](#9-jdk-23---模块导入声明)
10. [迁移到模块系统](#10-迁移到模块系统)
11. [最佳实践](#11-最佳实践)
12. [模块图分析](#12-模块图分析)
13. [时间线总结](#13-时间线总结)
14. [相关链接](#14-相关链接)

---


## 1. 时间线概览

```
JDK 8 ───── JDK 9 ───── JDK 11 ───── JDK 16 ───── JDK 17 ───── JDK 23 ───── JDK 25
 │             │             │             │             │             │             │
Classpath    JPMS         jlink        jpackage      强封装      模块导入     模块导入
             (JEP 261)    定制         正式版       (JEP 403)    预览         正式
                          运行                                   (JEP 476)   (JEP 511)
```

---

## 2. 为什么需要模块系统

### Classpath 的问题

```
┌─────────────────────────────────────────────────────────┐
│                  Classpath 问题                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. JAR Hell                                           │
│     ├── 版本冲突                                       │
│     ├── 依赖地狱                                       │
│     └── 类路径加载顺序不确定                            │
│                                                         │
│  2. 弱封装                                              │
│     ├── public 类可被任意访问                          │
│     ├── internal 类可被反射访问                         │
│     └── 无法隐藏实现细节                                │
│                                                         │
│  3. 性能问题                                            │
│     ├── 启动时扫描所有 JAR                             │
│     ├── 类加载器层次复杂                               │
│     └── 内存占用大                                     │
│                                                         │
│  4. 单体应用                                            │
│     ├── rt.jar 超过 50MB                              │
│     ├── 包含不需要的功能                               │
│     └── 无法裁剪运行时                                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 3. JDK 9 - JPMS (JEP 261)

### 模块声明

```java
// module-info.java
module com.example.myapp {
    // 导入模块
    requires java.base;
    requires java.sql;
    requires java.logging;

    // 可传递导入
    requires transitive java.net.http;

    // 导出包
    exports com.example.myapp.api;

    // 导出给特定模块
    exports com.example.myapp.impl
        to com.example.myapp.test;

    // 服务提供
    provides com.example.myapp.spi.Service
        with com.example.myapp.impl.ServiceImpl;

    // 服务消费
    uses com.example.myapp.spi.Service;
}
```

### 模块图

```
┌─────────────────────────────────────────────────────────┐
│                   JDK 模块图                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│                    java.base                           │
│                         │                               │
│         ┌───────────────┼───────────────┐               │
│         │               │               │               │
│    java.sql      java.logging    java.net.http          │
│         │               │               │               │
│    myapp.module      │           │                       │
│         │               │               │               │
│         └───────────────┴───────────────┘               │
│                         │                               │
│                    java.xml                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 模块描述符

```java
// 基础模块
module com.example.app {
    requires java.base;  // 隐式导入
}

// 多个 requires
module com.example.database {
    requires java.sql;
    requires java.logging;
    requires java.xml;
}

// 静态导入
module com.example.app {
    // 编译时需要，运行时不强依赖
    requires static com.example.annotations;
}

// 可选导入
module com.example.app {
    // 可能不存在的模块
    requires static com.example.optional;
}
```

---

## 4. 模块类型

### 模块分类

```
┌─────────────────────────────────────────────────────────┐
│                    模块类型                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │          命名模块 (Named Modules)           │        │
│  │  - 在 module-info.java 中声明              │        │
│  │  - 显式依赖关系                           │        │
│  │  - 强封装                                 │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │          自动模块 (Automatic Modules)       │        │
│  │  - JAR 文件放在 module path               │        │
│  │  - 自动命名为模块                          │        │
│  │  - module-info.java 从 manifest 读取       │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │          未命名模块 (Unnamed Modules)       │        │
│  │  - 放在 classpath 上                        │        │
│  │  - 整个 classpath 是一个模块               │        │
│  │  - 用于向后兼容                             │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 5. 模块命令

### jmod 命令

```bash
# 创建模块 JAR
jar --create --file com.example.myapp.jar \
     --module-version 1.0 \
     --main-class com.example.myapp.Main \
     -C classes .

# 创建 JMOD 文件
jmod create --class-path classes \
    --main-class com.example.myapp.Main \
    com.example.myapp.jmod

# 列出模块描述符
jmod describe --file com.example.myapp.jmod

# 列出模块内容
jmod list com.example.myapp.jmod
```

### jar 命令增强

```bash
# 创建模块化 JAR
jar --create \
    --file myapp.jar \
    --main-class com.example.myapp.Main \
    --module-version 1.0 \
    -C classes .

# 更新模块描述符
jar --update --file myapp.jar \
    --module-version 1.1 \
    -C classes-new .

# 从模块化 JAR 运行
java --module-path lib -m myapp/com.example.myapp.Main
```

### javac 命令

```bash
# 编译模块
javac -d classes \
    --module-source-path src \
    $(find src -name "*.java")

# 编译特定模块
javac -d classes \
    --module-source-path src \
    --module com.example.myapp

# 模块路径编译
javac --module-path mods \
    -d classes \
    --module-source-path src \
    --module com.example.myapp
```

### java 命令

```bash
# 运行模块化应用
java --module-path lib \
    --module com.example.myapp/com.example.myapp.Main

# 添加模块
java --module-path lib \
    --add-modules java.logging \
    -m myapp/com.example.myapp.Main

# 打印模块图
java --module-path lib \
    --print-module-deps \
    -m myapp/com.example.myapp.Main

# 启动时验证
java --validate-modules \
    --module-path lib \
    -m myapp/com.example.myapp.Main
```

---

## 6. JDK 11+ - 模块增强

### 打包工具 (jlink)

```bash
# jlink - 定制运行时镜像
jlink --module-path $JAVA_HOME/jmods \
    --add-modules java.base,java.sql,java.logging \
    --output custom-runtime

# 结果: 约 40MB (vs 完整 JDK ~200MB)

# 添加启动器
jlink --module-path $JAVA_HOME/jmods \
    --add-modules myapp \
    --output myapp-runtime \
    --launcher myapp=myapp/com.example.myapp.Main

# 压缩资源
jlink --compress=2 \
    --module-path $JAVA_HOME/jmods \
    --add-modules java.base \
    --output tiny-runtime
```

### jdeps 依赖分析

```bash
# 分析模块依赖
jdeps --module-path lib \
    myapp.jar

# 生成模块图
jdeps --module-path lib \
    --print-module-deps \
    myapp.jar

# 分析包依赖
jdeps --verbose:package \
    myapp.jar

# 找出 JDK 内部依赖
jdeps -J-Djdk.lang.Process.launchMechanism=fork \
    --jdk-internals \
    myapp.jar
```

---

## 7. JDK 16+ - 封装增强

### 强封装

```java
// JDK 16+ 强封装
// 默认情况下，反射访问内部 API 被禁止

// 允许访问
module com.example.myapp {
    // 开放反射给特定模块
    opens com.example.myapp.internal
        to com.example.myapp.reflection;

    // 开放所有反射
    opens com.example.myapp.internal;
}

// 运行时允许
java --add-opens \
    java.base/java.lang=ALL-UNNAMED \
    -m myapp/com.example.myapp.Main

// 允许整个模块
java --add-opens=java.base/java.lang=ALL-UNNAMED \
    --add-opens=java.base/java.lang.reflect=ALL-UNNAMED
```

---

## 8. JDK 17+ - 遗留封装

### 遗留访问

```java
// JDK 17+ 允许在模块内部访问非导出包
module com.example.myapp {
    // 允许本模块内深度反射
    // 仅影响本模块的代码，不影响其他模块
    // 默认启用
}
```

---

## 9. JDK 23+ - 模块导入声明

> **JEP 476** (JDK 23 预览) → **JEP 511** (JDK 25 正式)

### 基本用法

```java
// 以前需要多个 import
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.io.IOException;

// 现在只需一行
import module java.base;

public class Example {
    public static void main(String... args) {
        List<String> list = new ArrayList<>();
        Map<String, Integer> map = Map.of();
    }
}
```

### 动态模块加载

```java
import java.lang.module.*;

// 动态配置模块层 (JDK 9+)
public class DynamicModuleLoader {

    public static void loadModuleFromJar(Path jarPath) throws Exception {
        ModuleLayer bootLayer = ModuleLayer.boot();

        // 模块查找
        ModuleFinder finder = ModuleFinder.of(jarPath);

        // 模块配置
        Configuration config = bootLayer.configuration()
            .resolve(finder, ModuleFinder.of(), Set.of("com.example.plugin"));

        // 新模块层
        ModuleLayer layer = bootLayer.defineModulesWithOneLoader(
            config,
            ClassLoader.getSystemClassLoader()
        );

        // 加载类
        Module module = layer.findModule("com.example.plugin").get();
        Class<?> clazz = Class.forName(module, "com.example.Plugin");
    }
}
```

---

## 10. 迁移到模块系统

### 迁移步骤

```bash
# 第一步: 分析依赖
jdeps --module-path $JAVA_HOME/jmods \
    myapp.jar

# 第二步: 创建模块描述符
# 在 src/com.example.myapp/module-info.java

# 第三步: 编译模块
javac -d classes \
    --module-source-path src \
    --module com.example.myapp

# 第四步: 创建模块 JAR
jar --create \
    --file lib/com.example.myapp.jar \
    --main-class com.example.myapp.Main \
    -C classes/com.example.myapp .

# 第五步: 测试运行
java --module-path lib \
    -m com.example.myapp/com.example.myapp.Main
```

### 自动模块

```java
// 不修改现有 JAR，自动转换为模块
// 方法 1: 使用 Automatic-Module-Name
// MANIFEST.MF:
// Automatic-Module-Name: com.example.legacy

// 方法 2: 放在 module-path，自动命名
java --module-path libs/legacy.jar \
    --module myapp/com.example.myapp.Main
```

---

## 11. 最佳实践

### 模块设计

```java
// ✅ 推荐: 清晰的模块边界
module com.example.app {
    requires java.base;
    requires java.net.http;

    exports com.example.app.api;
    // 不导出实现包
}

// ✅ 推荐: 使用服务接口
module com.example.app {
    uses com.example.plugin.Plugin;

    // 不依赖具体实现
}

module com.example.plugin.impl {
    requires com.example.app;
    provides com.example.plugin.Plugin
        with com.example.plugin.impl.MyPlugin;
}

// ❌ 避免: 导出所有包
module com.example.bad {
    exports com.example.everything;  // 破坏封装
}
```

### 模块命名

```java
// 命名约定: 反向域名
module com.example.myapp { }  // 推荐

// JDK 模块: java.*
module java.base { }
module java.sql { }

// 不推荐
module myapp { }  // 太短
module com.example.v1 { }  // 避免版本号
```

---

## 12. 模块图分析

### 循环依赖检测

```bash
# 检测循环依赖
jdeps --reverse --module-path lib \
    --module com.example.myapp

# 如果存在循环依赖
// Error: cycles exist among modules:
// com.example.app -> com.example.lib -> com.example.app
```

---

## 13. 时间线总结

| 版本 | 特性 | JEP |
|------|------|-----|
| JDK 9 | **JPMS** | JEP 200, 261 |
| JDK 9 | jlink | JEP 282 |
| JDK 9 | 内部 API 封装 | JEP 260 |
| JDK 14 | jpackage (孵化) | JEP 343 |
| JDK 15 | jpackage (孵化) | JEP 384 |
| JDK 16 | jpackage 正式 | JEP 392 |
| JDK 16 | 强封装默认 | JEP 396 |
| JDK 17 | 完全强封装 | JEP 403 |
| JDK 23 | 模块导入声明 (预览) | JEP 476 |
| JDK 24 | 模块导入声明 (二次预览) | JEP 494 |
| JDK 25 | 模块导入声明 (正式) | JEP 511 |

---

## 14. 相关链接

- [JEP 200](/jeps/language/jep-200.md)
- [JEP 261](/jeps/language/jep-261.md)
- [JEP 260](/jeps/language/jep-260.md)
- [JEP 282](/jeps/tools/jep-282.md)
- [JEP 343](/jeps/tools/jep-343.md)
- [JEP 392](/jeps/tools/jep-392.md)
- [JEP 396](/jeps/language/jep-396.md)
- [JEP 403](/jeps/language/jep-403.md)
- [JEP 476](/jeps/language/jep-476.md)
- [JEP 511](/jeps/tools/jep-511.md)
- [jlink Tool](https://docs.oracle.com/en/java/javase/21/docs/specs/man/jlink.html)
