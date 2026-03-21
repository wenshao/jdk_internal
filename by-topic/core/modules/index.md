# 模块系统

> JEP 200、JPMS、jlink 演进历程

[← 返回核心平台](../)

---

## 快速概览

```
JDK 1.0 ── JDK 8 ── JDK 9 ── JDK 11 ── JDK 16 ── JDK 17 ── JDK 23 ── JDK 25
   │         │        │        │        │        │        │        │
单一下载  RT.jar   JPMS    jlink   jpackage  强封装  模块     模块
          Monolith  JEP    JEP    JEP     JDK     导入     导入
          Jar      200/261 282   392     内部    声明     声明
                   module-info      JDK    API     预览     正式
                   .java            16     封装     (476)   (511)
```

### 核心演进

| 版本 | 特性 | 说明 | JEP |
|------|------|------|-----|
| **JDK 8** | ClassPath | 传统类路径 (rt.jar) | - |
| **JDK 9** | JPMS | Java 平台模块系统 | JEP 200, 261 |
| **JDK 9** | module-info | 模块描述符 | JEP 261 |
| **JDK 9** | jlink | 自定义运行时 | JEP 282 |
| **JDK 9** | 内部 API 封装 | 大部分内部 API 封装 | JEP 260 |
| **JDK 11** | 模块化增强 | 稳定化 | - |
| **JDK 14** | jpackage (孵化) | 原生打包工具 | JEP 343 |
| **JDK 15** | jpackage (孵化) | 改进孵化版 | JEP 384 |
| **JDK 16** | jpackage | 正式发布 | JEP 392 |
| **JDK 16** | 强封装默认 | 内部 API 默认强封装 | JEP 396 |
| **JDK 17** | 强封装增强 | 完全强封装 | JEP 403 |
| **JDK 23** | 模块导入声明 | 预览版 `import module` | JEP 476 |
| **JDK 24** | 模块导入声明 | 第二次预览 | JEP 476 |
| **JDK 25** | 模块导入声明 | 正式版 | JEP 511 |

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 模块系统团队 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Claes Redestad | 18 | Oracle | 模块系统 |
| 2 | Alan Bateman | 17 | Oracle | JPMS 设计 |
| 3 | Severin Gehwolf | 13 | Red Hat | 模块系统 |
| 4 | Athijegannathan Sundararajan | 13 | Oracle | jlink |
| 5 | Mandy Chung | 9 | Oracle | 模块层 |
| 6 | Naoto Sato | 7 | Oracle | i18n 模块 |
| 7 | Henry Jen | 6 | Oracle | jlink |
| 8 | Jonathan Gibbons | 5 | Oracle | javadoc 模块 |

---

## JPMS 架构

### 模块系统概览

```
┌─────────────────────────────────────────────────────────┐
│                    JPMS 架构                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  模块描述符 (module-info.java)                           │
│  ├── requires    # 依赖模块                             │
│  ├── exports     # 导出包                               │
│  ├── opens       # 开放包 (反射)                         │
│  ├── uses        # 服务接口                             │
│  └── provides    # 服务实现                             │
│                                                         │
│  模块路径 (--module-path)                               │
│  ├── 模块 JAR (.jar)                                    │
│  ├── 模块目录                                          │
│  └── 自动模块 (Classpath JAR)                           │
│                                                         │
│  模块层                                                │
│  ├── Boot Layer    (启动模块)                          │
│  ├── Platform Layer (平台模块)                         │
│  └── App Layer     (应用模块)                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### module-info.java

```java
// 模块描述符
module com.example.myapp {
    // 依赖模块
    requires java.base;      // 默认导入
    requires java.sql;       // JDBC

    // 传递依赖
    requires transitive java.logging;

    // 静态依赖 (编译时)
    requires static java.compiler;

    // 导出包
    exports com.example.api;

    // 导出到特定模块
    exports com.example.impl to com.example.test;

    // 开放包 (反射)
    opens com.example.entities;

    // 开放到特定模块
    opens com.example.internal to hibernate.core;

    // 服务使用
    uses com.example.spi.Provider;

    // 服务提供
    provides com.example.spi.Provider
        with com.example.impl.ProviderImpl;
}
```

---

## 模块声明

### requires

```java
// 基础依赖
requires java.sql;

// 传递依赖 (依赖此模块的用户也依赖 java.logging)
requires transitive java.logging;

// 静态依赖 (编译时依赖，运行时可选)
requires static java.compiler;

// 指定版本 (不推荐，依赖模块系统)
requires java.sql@11.0.1;
```

### exports

```java
// 导出包
exports com.example.api;

// 导出到特定模块 (限定导出)
exports com.example.internal to
    com.example.test,
    com.example.debug;
```

### opens

```java
// 开放包 (深度反射)
opens com.example.entities;

// 开放到特定模块
opens com.example.entities to
    hibernate.core,
    eclipse.persistence;

// 开放所有包 (不推荐)
opens com.example.*;
```

### uses 和 provides

```java
// 服务接口
uses com.example.spi.Provider;

// 服务实现
provides com.example.spi.Provider
    with com.example.impl.ProviderImpl;
```

---

## 模块导入声明 (JDK 23+)

> **JEP 476** (JDK 23 预览) → **JEP 511** (JDK 25 正式)

### 基本语法

```java
// 以前需要多个 import
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.Set;
import java.io.IOException;
import java.nio.file.Path;
// ... 可能需要几十个 import

// 现在只需一行
import module java.base;

public class Example {
    public static void main(String... args) {
        List<String> list = new ArrayList<>();  // 直接使用
        Map<String, Integer> map = Map.of();    // 直接使用
        Path path = Path.of("/tmp");            // 直接使用
    }
}
```

### 多模块导入

```java
import module java.base;
import module java.sql;
import module java.logging;

public class DatabaseApp {
    private static final Logger logger = Logger.getLogger("DB");
    // Logger 来自 java.logging
    // Connection 来自 java.sql
}
```

### 与普通 import 混用

```java
import module java.base;
import java.sql.Date;  // 明确指定解决歧义

public class DateExample {
    Date sqlDate;              // java.sql.Date (显式导入)
    java.util.Date utilDate;   // java.util.Date (来自模块导入)
}
```

### JShell 默认脚本

JDK 25+ 起默认启动脚本简化：

```java
// 旧版 DEFAULT.jsh (需要多个 import)
import java.io.*;
import java.math.*;
import java.net.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.function.*;
import java.util.prefs.*;
import java.util.regex.*;
import java.util.stream.*;

// 新版 DEFAULT.jsh (JDK 25+)
import module java.base;
```

### 使用场景

| 场景 | 推荐度 | 说明 |
|------|--------|------|
| 新项目 | ✅ 推荐 | 大幅简化代码 |
| 教学场景 | ✅ 推荐 | 降低入门门槛 |
| JShell 脚本 | ✅ 推荐 | 快速原型开发 |
| 库开发 | ⚠️ 谨慎 | 考虑用户 JDK 版本 |
| 已有项目 | 可选 | 无需强制迁移 |

---

## 模块编译与运行

### 编译模块

```bash
# 单模块编译
javac -d out/module/com.example \
    --module-source-path src \
    com.example/module-info.java \
    com.example/com/example/Main.java

# 多模块编译
javac -d out \
    --module-source-path src \
    $(find src -name "*.java")
```

### 打包模块

```bash
# 创建模块 JAR
jar --create \
    --file lib/com.example.jar \
    --main-class com.example.Main \
    -C out/com.example .

# 查看模块描述
jar --describe-module --file=com.example.jar
```

### 运行模块

```bash
# 运行模块
java --module-path lib \
    --module com.example/com.example.Main

# 指定主类
java --module-path lib \
    -m com.example/com.example.Main

# 添加模块
java --module-path lib \
    --add-modules java.logging \
    -m com.example/com.example.Main
```

---

## jlink (自定义运行时)

### 创建自定义运行时

```bash
# 创建最小运行时
jlink --module-path lib \
    --add-modules com.example \
    --output runtime

# 指定启动器
jlink --module-path lib \
    --add-modules com.example \
    --output runtime \
    --launcher myapp=com.example/com.example.Main

# 压缩
jlink --module-path lib \
    --add-modules com.example \
    --output runtime \
    --compress=2  # 0=无, 1=过滤, 2=Zip

# 排除文件
jlink --module-path lib \
    --add-modules com.example \
    --output runtime \
    --strip-debug \
    --no-man-pages \
    --no-header-files
```

### 查看可用模块

```bash
# 查看所有平台模块
jlink --list-modules

# 查看模块描述
jlink --module-path $JAVA_HOME/jmods \
    --add-modules java.base \
    --verbose
```

---

## jpackage (JDK 14+)

### 打包工具 (JEP 343 → JEP 384 → JEP 392)

```bash
# 创建应用包
jpackage \
    --input lib \
    --dest dist \
    --name MyApp \
    --main-class com.example.Main \
    --main-jar myapp.jar

# 创建安装程序
jpackage \
    --type rpm \
    --input lib \
    --dest dist \
    --name MyApp \
    --main-class com.example.Main \
    --main-jar myapp.jar

# Windows exe
jpackage \
    --type exe \
    --input lib \
    --dest dist \
    --name MyApp \
    --main-class com.example.Main \
    --main-jar myapp.jar \
    --win-console \
    --win-shortcut \
    --win-menu
```

---

## 强封装 (JDK 16+)

### JEP 396 (JDK 16) / JEP 403 (JDK 17): 强封装

```bash
# JDK 9-15: 允许非法访问 (默认警告)
java --illegal-access=permit \
    -cp myapp.jar Main

# JDK 16: 默认强封装，但可绕过
java --add-opens java.base/java.lang=ALL-UNNAMED \
    -cp myapp.jar Main

# JDK 17+: 完全强封装，--illegal-access 选项已移除
# 必须显式使用 --add-opens 和 --add-exports
java --add-opens=java.base/java.lang=ALL-UNNAMED \
    --add-exports=java.base/sun.security.x509=ALL-UNNAMED \
    -cp myapp.jar Main
```

### 常见内部 API 替代

| 内部 API | 替代方案 |
|---------|----------|
| `sun.misc.Unsafe` | `VarHandle` (JDK 9+) |
| `sun.reflect.ReflectionFactory` | `MethodHandles.Lookup` |
| `com.sun.nio.file.SolarisWatchService` | `WatchService` API |
| `jdk.internal.misc.Unsafe` | `Foreign Function & Memory` |

---

## 服务加载 (ServiceLoader)

### 定义服务

```java
// com.example.spi/provider-api.jar
module com.example.spi {
    exports com.example.spi;
}

// com.example.spi.Provider
package com.example.spi;
public interface Provider {
    String getName();
}
```

### 实现服务

```java
// com.example.impl/module-info.java
module com.example.impl {
    requires com.example.spi;
    provides com.example.spi.Provider
        with com.example.impl.ProviderImpl;
}

// com.example.impl.ProviderImpl
package com.example.impl;
public class ProviderImpl implements com.example.spi.Provider {
    @Override
    public String getName() {
        return "Impl";
    }
}
```

### 使用服务

```java
// com.example.app/module-info.java
module com.example.app {
    requires com.example.spi;
    uses com.example.spi.Provider;
}

// com.example.app.Main
import com.example.spi.Provider;
import java.util.ServiceLoader;

public class Main {
    public static void main(String[] args) {
        Iterable<Provider> providers =
            ServiceLoader.load(Provider.class);
        providers.forEach(p ->
            System.out.println(p.getName()));
    }
}
```

---

## 自动模块

### Classpath JAR 自动模块化

```bash
# 传统 JAR 自动成为模块
# 模块名 = JAR 文件名 (或 Automatic-Module-Name)
java --module-path lib/my-lib.jar \
    --module myapp/com.example.Main

# 模块名规则
# my-lib-1.0.jar -> my.lib
```

### 指定自动模块名

```bash
# 在 MANIFEST.MF 中指定
Manifest-Version: 1.0
Automatic-Module-Name: com.example.mylib
```

---

## 分层启动 (Layer)

### 自定义模块层

```java
import java.lang.module.Configuration;
import java.lang.module.ModuleFinder;
import java.lang.module.ModuleReference;
import java.lang.reflect.Method;
import java.nio.file.Paths;
import java.util.Set;

public class LayerExample {
    public static void main(String[] args) throws Exception {
        // Boot Layer
        ModuleLayer bootLayer = ModuleLayer.boot();

        // 配置新模块
        Configuration config = bootLayer.configuration()
            .resolve(
                ModuleFinder.of(),
                ModuleFinder.of(Paths.get("mods")),
                Set.of("com.example.dynamic"));

        // 创建新层
        ModuleLayer layer = bootLayer.defineModulesWithOneLoader(
            config, ClassLoader.getSystemClassLoader());

        // 加载类
        Class<?> clazz = layer.findLoader("com.example.dynamic")
            .loadClass("com.example.dynamic.Main");
        Method main = clazz.getMethod("main", String[].class);
        main.invoke(null, (Object) new String[0]);
    }
}
```

---

## 相关链接

### 本地文档

- [JVM 调优](../jvm/) - 模块化 JVM 参数
- [类加载](../classloading/) - 模块化类加载

### 外部参考

**JEP 文档:**
- [JEP 200: The Modular JDK](https://openjdk.org/jeps/200)
- [JEP 261: Module System](https://openjdk.org/jeps/261)
- [JEP 260: Encapsulate Most Internal APIs](https://openjdk.org/jeps/260)
- [JEP 282: jlink](https://openjdk.org/jeps/282)
- [JEP 343: Packaging Tool (Incubator)](https://openjdk.org/jeps/343)
- [JEP 392: Packaging Tool](https://openjdk.org/jeps/392)
- [JEP 396: Strongly Encapsulate JDK Internals by Default](https://openjdk.org/jeps/396)
- [JEP 403: Strongly Encapsulate JDK Internals](https://openjdk.org/jeps/403)
- [JEP 476: Module Import Declarations (Preview)](https://openjdk.org/jeps/476)
- [JEP 511: Module Import Declarations](https://openjdk.org/jeps/511)

**技术文档:**
- [JPMS Guide](https://openjdk.org/projects/jigsaw/)
- [State of the Module System](https://openjdk.org/jeps/8207164)
