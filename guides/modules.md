# Java 模块系统 (JPMS) 实用指南

> 面向实际操作的模块系统指南：从 5 分钟上手到生产迁移。

---
## 目录

1. [5 分钟上手](#1-5-分钟上手)
2. [module-info.java 详解](#2-module-infojava-详解)
3. [模块类型 (Module Types)](#3-模块类型-module-types)
4. [迁移现有项目: classpath → modulepath](#4-迁移现有项目-classpath--modulepath)
5. [常见问题与解法](#5-常见问题与解法)
6. [jlink 自定义运行时](#6-jlink-自定义运行时)
7. [与 Maven/Gradle 集成](#7-与-mavengradle-集成)
8. [JDK 25+ 模块新特性](#8-jdk-25-模块新特性)
9. [模块化 JDK 常用模块速查](#9-模块化-jdk-常用模块速查)
10. [最佳实践与反模式](#10-最佳实践与反模式)

---


## 1. 5 分钟上手

### 最小示例: 一个模块化的 Hello World

项目结构：
```
myapp/
├── src/
│   └── com.example.app/
│       ├── module-info.java
│       └── com/example/app/
│           └── Main.java
```

`module-info.java` (放在源码根目录):
```java
module com.example.app {
    // 不需要 requires java.base; — 它是隐式依赖
}
```

`Main.java`:
```java
package com.example.app;

public class Main {
    public static void main(String[] args) {
        System.out.println("Hello from a module!");
    }
}
```

编译与运行：
```bash
# 编译
javac -d out/com.example.app \
  src/com.example.app/module-info.java \
  src/com.example.app/com/example/app/Main.java

# 运行
java --module-path out \
     --module com.example.app/com.example.app.Main

# 简写
java -p out -m com.example.app/com.example.app.Main
```

### 两个模块的示例

```
mylib/
├── src/
│   ├── com.example.lib/
│   │   ├── module-info.java
│   │   └── com/example/lib/
│   │       └── Greeter.java
│   └── com.example.app/
│       ├── module-info.java
│       └── com/example/app/
│           └── Main.java
```

库模块 `com.example.lib`:
```java
// module-info.java
module com.example.lib {
    exports com.example.lib;  // 导出公共 API 包
}

// Greeter.java
package com.example.lib;
public class Greeter {
    public static String hello(String name) {
        return "Hello, " + name + "!";
    }
}
```

应用模块 `com.example.app`:
```java
// module-info.java
module com.example.app {
    requires com.example.lib;  // 声明依赖
}

// Main.java
package com.example.app;
import com.example.lib.Greeter;

public class Main {
    public static void main(String[] args) {
        System.out.println(Greeter.hello("JPMS"));
    }
}
```

编译与运行：
```bash
# 编译所有模块
javac -d out --module-source-path src $(find src -name "*.java")

# 运行
java -p out -m com.example.app/com.example.app.Main
```

---

## 2. module-info.java 详解

### 所有指令 (Directives)

```java
module com.example.myapp {
    // ── 依赖 ──
    requires java.sql;                    // 编译时 + 运行时依赖
    requires transitive java.logging;     // 传递依赖 (下游模块也能用)
    requires static java.compiler;        // 仅编译时 (可选依赖)

    // ── 导出 ──
    exports com.example.myapp.api;                      // 导出包给所有模块
    exports com.example.myapp.spi to com.example.plugin; // 限定导出

    // ── 开放反射 ──
    opens com.example.myapp.model;                      // 允许运行时反射
    opens com.example.myapp.entity to org.hibernate.orm; // 限定开放

    // ── 服务 ──
    uses com.example.myapp.spi.Plugin;                  // 消费服务
    provides com.example.myapp.spi.Plugin               // 提供服务实现
        with com.example.myapp.internal.DefaultPlugin;
}
```

### exports vs opens

| 指令 | 编译时访问 | 运行时反射 | 典型用途 |
|------|-----------|-----------|---------|
| `exports` | public 类型可访问 | 仅 public 成员 | 公共 API |
| `opens` | 无编译时访问 | 所有成员可反射 | JPA entity, JSON 序列化 |
| `exports` + `opens` | 两者皆可 | 两者皆可 | 需要 API + 反射的包 |

### requires transitive 的传递效果

```java
module com.example.service {
    requires transitive java.sql;  // 下游模块自动获得 java.sql 依赖
}

module com.example.app {
    requires com.example.service;
    // 不需要显式 requires java.sql — 已通过 transitive 传递
}
```

### open module (完全开放模块)

```java
// 整个模块对反射完全开放 (不推荐生产使用，但迁移期有用)
open module com.example.legacy {
    requires java.sql;
    exports com.example.legacy.api;
}
```

---

## 3. 模块类型 (Module Types)

### 三种模块及其关系

```
                    模块路径 (--module-path)          类路径 (--class-path)
                    ┌──────────────────────┐          ┌──────────────────┐
有 module-info  →   │  命名模块             │          │  (被忽略)        │
                    │  Named Module         │          │                  │
                    │                      │          │                  │
无 module-info  →   │  自动模块             │          │  未命名模块      │
                    │  Automatic Module     │          │  Unnamed Module  │
                    └──────────────────────┘          └──────────────────┘
```

| 类型 | module-info | 放置位置 | 模块名来源 | 能 requires | 能被 requires |
|------|-------------|---------|-----------|-------------|---------------|
| **命名模块** | 有 | module-path | module-info.java | 命名 + 自动 | 是 |
| **自动模块** | 无 | module-path | JAR Manifest 或文件名 | 命名 + 自动 + 未命名 | 是 |
| **未命名模块** | 无 | class-path | (无名) | 所有模块 | 否 |

**关键规则**:
- 命名模块 **不能** requires 未命名模块 (这是迁移的主要痛点)
- 自动模块是**桥梁**：它既能被命名模块 requires，又能读取类路径上的 JAR

### 自动模块名的确定规则

```
优先级:
1. JAR 的 MANIFEST.MF 中有 Automatic-Module-Name → 使用该名称
2. 否则，根据 JAR 文件名推导:
   guava-33.0.jar → guava
   jackson-databind-2.18.0.jar → jackson.databind

   规则: 去掉版本号，连字符转为点号
```

检查 JAR 的自动模块名：
```bash
jar --describe-module --file=guava-33.0.jar
```

---

## 4. 迁移现有项目: classpath → modulepath

### 渐进式迁移策略 (推荐)

```
阶段 1: 全部留在 classpath (现状)
  └─ 所有 JAR 在未命名模块中，和 JDK 8 行为一致

阶段 2: 应用代码模块化，第三方库留在 classpath
  ├─ 添加 module-info.java 到你的项目
  ├─ 第三方库放在 module-path (成为自动模块)
  └─ 可以 requires 自动模块

阶段 3: 逐步将依赖升级为命名模块
  └─ 大多数主流库已提供 module-info
      (Guava 33+, Jackson 2.18+, SLF4J 2.x, Log4j2 3.x)

阶段 4: 完全模块化
  └─ 可以使用 jlink 创建自定义运行时
```

### 实操步骤

#### Step 1: 分析现有依赖

```bash
# 扫描 JAR 的内部 API 使用
jdeps --jdk-internals -cp 'libs/*.jar' myapp.jar

# 生成模块依赖图
jdeps --module-path libs -s myapp.jar

# 自动生成 module-info.java (参考)
jdeps --generate-module-info out myapp.jar
```

#### Step 2: 创建 module-info.java

```java
module com.mycompany.myapp {
    // 依赖 JDK 模块
    requires java.sql;
    requires java.logging;

    // 依赖第三方库 (自动模块)
    requires com.google.gson;
    requires org.slf4j;

    // 导出公共 API
    exports com.mycompany.myapp.api;

    // 开放给反射框架 (Spring, Hibernate, Jackson)
    opens com.mycompany.myapp.model to com.fasterxml.jackson.databind;
    opens com.mycompany.myapp.entity to org.hibernate.orm;
}
```

#### Step 3: 调整编译命令

```bash
# 从
javac -cp libs/* -d out src/**/*.java

# 改为
javac --module-path libs -d out src/**/*.java
```

#### Step 4: 调整运行命令

```bash
# 从
java -cp "out:libs/*" com.mycompany.myapp.Main

# 改为
java --module-path "out:libs" \
     --module com.mycompany.myapp/com.mycompany.myapp.Main
```

---

## 5. 常见问题与解法

### 问题 1: `--add-opens` 和 `--add-exports`

**场景**: 框架需要反射访问被封装的包。

```bash
# --add-exports: 编译时 + 运行时，导出包的 public 成员
java --add-exports java.base/sun.nio.ch=ALL-UNNAMED -jar app.jar

# --add-opens: 运行时，允许深度反射 (private 成员)
java --add-opens java.base/java.lang=ALL-UNNAMED -jar app.jar

# 多个 --add-opens 用空格分隔
java --add-opens java.base/java.lang=ALL-UNNAMED \
     --add-opens java.base/java.lang.reflect=ALL-UNNAMED \
     -jar app.jar
```

**长期方案**: 替换内部 API 调用。使用 `jdeps --jdk-internals` 找出所有使用点。

### 问题 2: Split Package (拆分包)

**现象**:
```
Error: Package com.example.util exists in both
  module.a and module.b
```

**原因**: 同一个包存在于两个不同模块中。模块系统禁止此行为。

**解法**:
```
方案 A: 重命名其中一个包
  com.example.util → com.example.util.extra

方案 B: 合并两个 JAR 为一个模块

方案 C: 将其中一个 JAR 放在 classpath (成为未命名模块的一部分)
```

### 问题 3: 反射框架失败 (Spring, Hibernate, Jackson)

**现象**:
```
java.lang.reflect.InaccessibleObjectException:
  Unable to make field private ... accessible
```

**解法**: 在 module-info.java 中 `opens` 需要反射的包:

```java
module com.myapp {
    // Spring
    opens com.myapp to spring.core, spring.beans, spring.context;

    // Hibernate / JPA
    opens com.myapp.entity to org.hibernate.orm, jakarta.persistence;

    // Jackson
    opens com.myapp.dto to com.fasterxml.jackson.databind;

    // 或者偷懒 (不推荐生产):
    opens com.myapp.entity;  // 对所有模块开放
}
```

### 问题 4: ServiceLoader 找不到实现

**现象**: `ServiceLoader.load(MyService.class)` 返回空。

**解法**: 在 module-info.java 中声明:

```java
// 服务消费者
module consumer {
    uses com.example.spi.MyService;
}

// 服务提供者
module provider {
    provides com.example.spi.MyService
        with com.example.impl.MyServiceImpl;
}
```

### 问题 5: 资源文件访问

**现象**: `getClass().getResource("/config.properties")` 返回 null。

**原因**: 模块系统限制了跨模块资源访问。

**解法**:
```java
// 方案 A: 资源在当前模块内 — 直接访问
InputStream is = getClass().getResourceAsStream("/config.properties");

// 方案 B: 资源在其他模块 — 使用 Module API
Module mod = ModuleLayer.boot().findModule("com.example.lib").orElseThrow();
InputStream is = mod.getResourceAsStream("com/example/lib/config.properties");

// 方案 C: opens 包含资源的包
// module-info.java:
// opens com.example.lib.resources;
```

---

## 6. jlink 自定义运行时

### 基本用法

```bash
# 创建仅包含所需模块的最小 JRE
jlink --add-modules java.base,java.sql,java.logging \
      --output my-runtime \
      --strip-debug \
      --compress zip-9 \
      --no-man-pages \
      --no-header-files

# 查看大小对比
du -sh $JAVA_HOME   # 完整 JDK: ~300MB
du -sh my-runtime   # 自定义:   ~30-50MB
```

### 包含应用模块

```bash
# 先打包应用为模块化 JAR
jar --create --file=myapp.jar \
    --main-class=com.myapp.Main \
    --module-version=1.0 \
    -C out/com.myapp .

# 创建包含应用的自定义运行时
jlink --module-path myapp.jar:libs \
      --add-modules com.myapp \
      --output my-runtime \
      --launcher myapp=com.myapp/com.myapp.Main \
      --strip-debug \
      --compress zip-9

# 直接运行
./my-runtime/bin/myapp
```

### jlink 与 Docker 结合

```dockerfile
# 多阶段构建
FROM eclipse-temurin:25-jdk-alpine AS build

WORKDIR /app
COPY . .

# 编译
RUN javac -d out --module-source-path src $(find src -name "*.java")

# 创建自定义运行时
RUN jlink --add-modules com.myapp \
          --module-path out \
          --output /opt/runtime \
          --launcher app=com.myapp/com.myapp.Main \
          --strip-debug --compress zip-9 \
          --no-man-pages --no-header-files

# 最终镜像
FROM alpine:3.20
COPY --from=build /opt/runtime /opt/runtime
ENTRYPOINT ["/opt/runtime/bin/app"]
# 镜像大小约 40-60MB
```

### jlink 限制

- **只能包含命名模块** (不支持自动模块或未命名模块)
- 如果依赖的第三方库没有 module-info，需要先用 `jmod` 或手动添加
- 不支持跨平台生成 (Linux 上 jlink 只能生成 Linux 运行时)

---

## 7. 与 Maven/Gradle 集成

### Maven

#### 基本模块化项目

```xml
<project>
    <groupId>com.example</groupId>
    <artifactId>myapp</artifactId>
    <version>1.0.0</version>

    <properties>
        <maven.compiler.release>25</maven.compiler.release>
    </properties>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.14.0</version>
            </plugin>
        </plugins>
    </build>
</project>
```

`src/main/java/module-info.java`:
```java
module com.example.myapp {
    requires java.sql;
    requires com.google.gson;   // Maven 依赖自动变成自动模块
    exports com.example.myapp.api;
}
```

#### 多模块 Maven 项目

```
parent/
├── pom.xml (parent)
├── core/
│   ├── pom.xml
│   └── src/main/java/
│       ├── module-info.java    → module com.example.core
│       └── com/example/core/
├── api/
│   ├── pom.xml
│   └── src/main/java/
│       ├── module-info.java    → module com.example.api
│       └── com/example/api/
└── app/
    ├── pom.xml
    └── src/main/java/
        ├── module-info.java    → module com.example.app
        └── com/example/app/
```

#### Maven + jlink 插件

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-jlink-plugin</artifactId>
    <version>3.2.0</version>
    <configuration>
        <addModules>
            <addModule>com.example.myapp</addModule>
        </addModules>
        <launcher>myapp=com.example.myapp/com.example.myapp.Main</launcher>
        <stripDebug>true</stripDebug>
        <compress>zip-9</compress>
        <noManPages>true</noManPages>
        <noHeaderFiles>true</noHeaderFiles>
    </configuration>
</plugin>
```

### Gradle

#### 基本模块化项目

```groovy
// build.gradle
plugins {
    id 'java'
    id 'application'
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(25)
    }
    modularity.inferModulePath = true  // 默认为 true
}

application {
    mainModule = 'com.example.myapp'
    mainClass = 'com.example.myapp.Main'
}
```

#### Gradle + jlink

```groovy
// 使用 org.beryx.jlink 插件
plugins {
    id 'org.beryx.jlink' version '3.1.1'
}

jlink {
    options = ['--strip-debug', '--compress', 'zip-9',
               '--no-header-files', '--no-man-pages']
    launcher {
        name = 'myapp'
    }
}
```

#### 测试模块 (Gradle)

```groovy
// 测试代码在非模块化 classpath 上运行 (默认行为)
// 如需在 module-path 上测试:
tasks.withType(Test).configureEach {
    jvmArgs += [
        '--add-opens', 'com.example.myapp/com.example.myapp.internal=ALL-UNNAMED'
    ]
}
```

---

## 8. JDK 25+ 模块新特性

### JEP 511: Module Import Declarations (JDK 26 Final)

```java
// 导入整个模块的公共 API — 不需要 module-info.java 中 requires
import module java.sql;

// 等价于导入 java.sql 模块导出的所有包:
// import java.sql.*;
// import javax.sql.*;

Connection conn = DriverManager.getConnection(url);
```

**注意**: `import module` 是编译时语法糖，与 JPMS module-info.java 中的 `requires` 无关。非模块化项目也可以使用。

### 模块封装持续收紧

| JDK 版本 | 封装行为 |
|----------|---------|
| JDK 9-15 | 默认允许非法访问 (`--illegal-access=permit`) |
| JDK 16 | 默认拒绝 (`--illegal-access=deny`)，可放宽 |
| JDK 17+ | 移除 `--illegal-access`，只能用 `--add-opens` |

---

## 9. 模块化 JDK 常用模块速查

| 模块 | 包含内容 | 典型用途 |
|------|---------|---------|
| `java.base` | Collections, I/O, NIO, 并发, 反射 | 自动依赖，无需 requires |
| `java.sql` | JDBC API | 数据库访问 |
| `java.logging` | java.util.logging | JUL 日志 |
| `java.net.http` | HttpClient (HTTP/1.1, 2, 3) | HTTP 请求 |
| `java.desktop` | AWT, Swing, 2D | GUI 应用 |
| `java.xml` | DOM, SAX, StAX, XSLT | XML 处理 |
| `java.naming` | JNDI | 目录服务 |
| `java.management` | JMX | 监控管理 |
| `java.instrument` | Java Agent | 字节码增强 |
| `java.compiler` | javax.annotation.processing | 注解处理 |
| `jdk.httpserver` | 内嵌 HTTP 服务器 | 测试/简单服务 |
| `jdk.jfr` | Java Flight Recorder | 性能诊断 |
| `jdk.management` | 扩展 JMX | 高级监控 |

查看完整模块列表：
```bash
java --list-modules
java --describe-module java.sql
```

---

## 10. 最佳实践与反模式

### 推荐做法

```
1. 模块名使用反向域名 (与包名一致)
   ✓ com.example.myapp
   ✗ myapp

2. 只导出 API 包，不导出 internal 包
   ✓ exports com.example.myapp.api;
   ✗ exports com.example.myapp.internal;

3. 使用 requires transitive 传递必要依赖
   如果你的 API 返回 java.sql.Connection，
   应该 requires transitive java.sql;

4. 使用 opens 而非 open module
   ✓ opens com.example.entity to org.hibernate.orm;
   ✗ open module com.example.myapp { ... }

5. 优先使用 ServiceLoader 替代反射发现
```

### 反模式

```
1. 滥用 --add-opens / --add-exports
   → 这是迁移临时方案，不是长期策略

2. 使用 open module 图省事
   → 丧失了模块系统的封装优势

3. 把所有类放在一个包里避免 split package
   → 应该重新设计包结构

4. 在 module-info.java 中 requires 不使用的模块
   → 增加不必要的依赖，影响 jlink 镜像大小

5. 导出 internal/impl 包
   → 违背封装原则，API 不稳定
```

---

**相关资源**:
- [JEP 261: Module System](https://openjdk.org/jeps/261) — 原始 JEP
- [学习路径](learning-path.md) — 按角色推荐的学习路线
- [FAQ](faq.md) — 常见问题
- [速查表](cheat-sheet.md) — JVM 参数快速参考
