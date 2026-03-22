# 模块系统

> JEP 200、JPMS、jlink 演进历程

[← 返回核心平台](../)

---
## 目录

1. [快速概览](#1-快速概览)
2. [核心贡献者](#2-核心贡献者)
3. [JPMS 架构](#3-jpms-架构) — 模块解析、Readability vs Accessibility、module-info.java 语法详解
4. [模块声明实例](#4-模块声明实例)
5. [模块导入声明 (JDK 23+)](#5-模块导入声明-jdk-23)
6. [模块编译与运行](#6-模块编译与运行)
7. [jlink (自定义运行时镜像)](#7-jlink-自定义运行时镜像) — --compress 选项、CDS 集成、Docker
8. [jpackage (JDK 14+)](#8-jpackage-jdk-14)
9. [强封装 (JDK 16+)](#9-强封装-strong-encapsulation-jdk-16) — --illegal-access 演进、JEP 396/403、反射影响
10. [服务加载 (ServiceLoader) 与模块](#10-服务加载-serviceloader-与模块) — provides...with、META-INF/services 兼容
11. [迁移实践](#11-迁移实践-自动模块与未命名模块) — Automatic Module、Unnamed Module、Split Package
12. [分层启动 (Layer)](#12-分层启动-layer)
13. [相关链接](#13-相关链接)

---


## 1. 快速概览

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
| **JDK 15** | jpackage (二次孵化) | 改进孵化版 | JEP 375 |
| **JDK 16** | jpackage | 正式发布 | JEP 392 |
| **JDK 16** | 强封装默认 | 内部 API 默认强封装 | JEP 396 |
| **JDK 17** | 强封装增强 | 完全强封装 | JEP 403 |
| **JDK 23** | 模块导入声明 | 预览版 `import module` | JEP 476 |
| **JDK 24** | 模块导入声明 | 第二次预览 | JEP 494 |
| **JDK 25** | 模块导入声明 | 正式版 | JEP 511 |

---

## 2. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 模块系统团队 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Claes Redestad | 18 | Oracle | 模块系统 |
| 2 | Alan Bateman | 17 | Oracle | JPMS 设计 |
| 3 | Severin Gehwolf | 13 | Red Hat (当时；现 IBM) | 模块系统 |
| 4 | Athijegannathan Sundararajan | 13 | Oracle | jlink |
| 5 | Mandy Chung | 9 | Oracle | 模块层 |
| 6 | Naoto Sato | 7 | Oracle | i18n 模块 |
| 7 | Henry Jen | 6 | Oracle | jlink |
| 8 | Jonathan Gibbons | 5 | Oracle | javadoc 模块 |

---

## 3. JPMS 架构

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

### 模块解析过程 (Module Resolution)

模块系统在编译或启动时构建**模块图 (Module Graph)**：

```
模块解析流程:

1. 从 root modules (根模块) 出发
2. 递归解析所有 requires 依赖
3. 构建有向图 (Directed Graph)
4. 检查可读性 (Readability) 与可访问性 (Accessibility)

┌──────────┐  requires   ┌──────────┐  requires   ┌──────────┐
│ com.app  │────────────→│ com.lib  │────────────→│java.base │
└──────────┘             └──────────┘             └──────────┘
     │                        │
     │ requires               │ requires transitive
     ▼                        ▼
┌──────────┐             ┌──────────┐
│ java.sql │             │java.logging│
└──────────┘             └──────────┘
```

**可读性 vs 可访问性 (Readability vs Accessibility):**

| 概念 | 英文 | 含义 | 控制方式 |
|------|------|------|----------|
| 可读性 | Readability | 模块 A 能否"看到"模块 B | `requires` 声明 |
| 可访问性 | Accessibility | 模块 A 能否访问模块 B 中的某个类型 | `exports` / `opens` 声明 |

```java
// 即使 com.app requires com.lib，
// 也只能访问 com.lib 中 exports 的包
module com.lib {
    exports com.lib.api;        // 可访问 ✅
    // com.lib.internal 未导出   // 不可访问 ❌
}
```

### module-info.java 语法详解

```java
// 模块描述符 (Module Descriptor)
module com.example.myapp {
    // ──── requires: 声明依赖 ────
    requires java.base;      // 隐式依赖，可省略
    requires java.sql;       // 显式依赖 JDBC 模块

    // ──── requires transitive: 传递依赖 (Implied Readability) ────
    // 任何 requires com.example.myapp 的模块，也自动获得对 java.logging 的可读性
    requires transitive java.logging;

    // ──── requires static: 编译时依赖 (Optional Dependency) ────
    // 编译时必须存在，运行时可选（不存在不会报错）
    // 典型场景: 注解处理器、编译时检查框架
    requires static java.compiler;

    // ──── exports: 导出包 (Qualified / Unqualified) ────
    exports com.example.api;                        // 无限定导出: 所有模块可访问
    exports com.example.impl to com.example.test;   // 限定导出: 仅指定模块可访问

    // ──── opens: 开放包 (Deep Reflection) ────
    // exports 只允许编译时访问 public 类型
    // opens 额外允许运行时反射访问所有成员（包括 private）
    opens com.example.entities;                     // 无限定开放
    opens com.example.internal to hibernate.core;   // 限定开放

    // ──── open module: 整个模块开放 ────
    // 替代方案: 将 module 声明为 open module，等价于 opens 所有包
    // open module com.example.myapp { ... }

    // ──── uses: 声明消费的服务接口 ────
    uses com.example.spi.Provider;

    // ──── provides...with: 声明服务实现 ────
    // 可提供多个实现类
    provides com.example.spi.Provider
        with com.example.impl.ProviderImpl,
             com.example.impl.ProviderImplV2;
}
```

### requires 修饰符总结

| 修饰符 | 语法 | 编译时 | 运行时 | 传递给依赖方 | 典型场景 |
|--------|------|--------|--------|-------------|----------|
| (无) | `requires M;` | 必须 | 必须 | 否 | 普通依赖 |
| `transitive` | `requires transitive M;` | 必须 | 必须 | 是 | API 中暴露的类型 |
| `static` | `requires static M;` | 必须 | 可选 | 否 | 注解处理、可选功能 |
| `static transitive` | `requires static transitive M;` | 必须 | 可选 | 是 | 罕见组合 |

### exports vs opens 区别

```
                  编译时访问          运行时反射
                  (Compile-time)     (Deep Reflection)

exports pkg;      ✅ public 类型      ❌ 无法反射 private
opens pkg;        ❌ 不能编译引用      ✅ 可反射所有成员
exports + opens;  ✅ public 类型      ✅ 可反射所有成员

// 实际等价声明:
exports com.example.api;     // API 包: 编译访问
opens com.example.entities;  // JPA 实体: 框架反射用
```

---

## 4. 模块声明实例

### 完整示例: 多模块项目

```
项目结构:
├── com.example.api/
│   ├── module-info.java
│   └── com/example/api/
│       └── Greeting.java
├── com.example.impl/
│   ├── module-info.java
│   └── com/example/impl/
│       └── GreetingImpl.java
└── com.example.app/
    ├── module-info.java
    └── com/example/app/
        └── Main.java
```

```java
// ── com.example.api/module-info.java ──
module com.example.api {
    exports com.example.api;
}

// ── com.example.impl/module-info.java ──
module com.example.impl {
    requires com.example.api;
    provides com.example.api.Greeting
        with com.example.impl.GreetingImpl;
}

// ── com.example.app/module-info.java ──
module com.example.app {
    requires com.example.api;
    uses com.example.api.Greeting;
}
```

### open module 声明

```java
// 整个模块对反射开放 — 常用于 Spring/Hibernate 等框架项目
open module com.example.webapp {
    requires java.sql;
    requires spring.core;
    // 所有包自动 opens，无需逐个声明
}
```

---

## 5. 模块导入声明 (JDK 23+)

> **JEP 476** (JDK 25 预览) → **JEP 511** (JDK 25 正式)

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

## 6. 模块编译与运行

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

## 7. jlink (自定义运行时镜像)

### 基本用法

```bash
# 创建最小运行时 (Custom Runtime Image)
jlink --module-path lib \
    --add-modules com.example \
    --output runtime

# 指定启动器脚本 (Launcher Script)
jlink --module-path lib \
    --add-modules com.example \
    --output runtime \
    --launcher myapp=com.example/com.example.Main

# 运行自定义镜像
./runtime/bin/myapp       # 使用启动器
./runtime/bin/java -m com.example  # 使用 java 命令
```

### --compress 选项演进

```bash
# JDK 9-20: 数字压缩级别
jlink --compress=0  # 无压缩 (No Compression)
jlink --compress=1  # 常量字符串共享 (Constant String Sharing)
jlink --compress=2  # ZIP 压缩 (ZIP Compression)

# JDK 21+ (JEP 参考): 改为命名压缩级别
jlink --compress=zip-0   # 无压缩
jlink --compress=zip-1   # 最快压缩
jlink --compress=zip-6   # 默认 ZIP 压缩 (等价于旧 --compress=2)
jlink --compress=zip-9   # 最高 ZIP 压缩
```

### 镜像瘦身实践

```bash
# 完整 JDK 21: ~300MB
# 最小 java.base 运行时: ~25-35MB

# 生产级瘦身配置
jlink --module-path $JAVA_HOME/jmods:lib \
    --add-modules com.example \
    --output runtime \
    --strip-debug \
    --strip-native-commands \
    --no-man-pages \
    --no-header-files \
    --compress=zip-6

# 查看镜像中的模块
./runtime/bin/java --list-modules
```

### jlink + CDS 集成 (Class Data Sharing)

```bash
# 1. 创建 jlink 镜像
jlink --module-path lib \
    --add-modules com.example \
    --output runtime

# 2. 生成默认 CDS 归档 (Default CDS Archive)
./runtime/bin/java -Xshare:dump

# 3. 生成应用 CDS 归档 (Application CDS)
# 步骤 a: 记录类列表
./runtime/bin/java -Xshare:off \
    -XX:DumpLoadedClassList=classes.lst \
    -m com.example/com.example.Main

# 步骤 b: 创建归档
./runtime/bin/java -Xshare:dump \
    -XX:SharedClassListFile=classes.lst \
    -XX:SharedArchiveFile=app-cds.jsa

# 步骤 c: 使用归档启动 (更快的启动时间)
./runtime/bin/java -Xshare:on \
    -XX:SharedArchiveFile=app-cds.jsa \
    -m com.example/com.example.Main
```

### jlink 与 Docker 容器

```dockerfile
# 多阶段构建: 使用 jlink 创建最小镜像
FROM eclipse-temurin:21-jdk AS builder
COPY . /app
WORKDIR /app
RUN javac -d out --module-source-path src $(find src -name "*.java") && \
    jlink --module-path out \
          --add-modules com.example \
          --output /javaruntime \
          --strip-debug --no-man-pages --no-header-files \
          --compress=zip-6

FROM debian:bookworm-slim
COPY --from=builder /javaruntime /opt/java
COPY --from=builder /app/out /app
ENTRYPOINT ["/opt/java/bin/java", "-m", "com.example/com.example.Main"]
# 最终镜像: ~50MB (vs ~400MB+ 使用完整 JDK)
```

### 查看可用模块

```bash
# 查看所有平台模块
java --list-modules

# 查看模块描述
jar --describe-module --file=com.example.jar

# 查看模块依赖树
jdeps --module-path lib -s -m com.example
```

---

## 8. jpackage (JDK 14+)

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

## 9. 强封装 (Strong Encapsulation, JDK 16+)

### --illegal-access 演进历程

```
JDK 9-15    JDK 16 (JEP 396)    JDK 17 (JEP 403)
   │              │                     │
   ▼              ▼                     ▼
 permit          deny                 removed
 (默认允许,     (默认拒绝,            (选项本身
  首次警告)      可切回 permit)        被移除)
```

| JDK 版本 | --illegal-access 默认值 | 行为 | JEP |
|----------|------------------------|------|-----|
| **9–15** | `permit` | 首次非法反射访问时打印警告，之后静默允许 | JEP 261 |
| **16** | `deny` | 默认拒绝，仍可通过 `--illegal-access=permit` 绕过 | JEP 396 |
| **17+** | (已移除) | 选项本身被删除，使用会报错；必须用 `--add-opens` | JEP 403 |

### JEP 396: 默认强封装 JDK 内部 API

```bash
# JDK 9-15: 默认 permit，首次访问警告
# WARNING: An illegal reflective access operation has occurred
# WARNING: Please consider reporting this to the maintainers of ...
java -cp myapp.jar Main

# JDK 16: 默认 deny，旧代码直接报错
# java.lang.reflect.InaccessibleObjectException
java -cp myapp.jar Main  # ❌ 如果访问了内部 API

# JDK 16: 可临时回退
java --illegal-access=permit -cp myapp.jar Main  # ⚠️ 仍可用但已废弃
```

### JEP 403: 完全强封装 — 不可逆

```bash
# JDK 17+: --illegal-access 选项已移除
java --illegal-access=permit -cp myapp.jar Main
# ❌ 错误: Unrecognized option: --illegal-access=permit

# 唯一绕过方式: 显式 --add-opens / --add-exports
java --add-opens=java.base/java.lang=ALL-UNNAMED \
    --add-exports=java.base/sun.security.x509=ALL-UNNAMED \
    -cp myapp.jar Main

# 在 MANIFEST.MF 中声明 (推荐用于库)
Add-Opens: java.base/java.lang
Add-Exports: java.base/sun.security.x509
```

### 对反射的影响 (Impact on Reflection)

```java
// JDK 8 可以随意反射:
Field field = String.class.getDeclaredField("value");
field.setAccessible(true);  // ✅ JDK 8 正常
                              // ❌ JDK 17+ InaccessibleObjectException

// JDK 17+ 正确做法:
// 1. 使用 opens 声明 (模块化项目)
// 2. 使用 --add-opens (命令行)
// 3. 使用标准 API 替代反射
```

### 常见内部 API 替代

| 内部 API | 替代方案 | 可用版本 |
|---------|----------|---------|
| `sun.misc.Unsafe` (内存操作) | `VarHandle` | JDK 9+ |
| `sun.misc.Unsafe` (堆外内存) | `MemorySegment` (Foreign Memory API) | JDK 22+ |
| `sun.reflect.ReflectionFactory` | `MethodHandles.Lookup` | JDK 9+ |
| `sun.misc.BASE64Encoder` | `java.util.Base64` | JDK 8+ |
| `com.sun.nio.file.*` | `java.nio.file.WatchService` | JDK 7+ |
| `jdk.internal.misc.Unsafe` | Foreign Function & Memory API | JDK 22+ |
| `sun.security.x509.*` | `java.security.cert` 标准 API | JDK 1.4+ |

### 模块化对 classpath 库的影响

```
classpath 上的库 → Unnamed Module (未命名模块)

特点:
├── 可以读取 (reads) 所有命名模块
├── 导出 (exports) 自己的所有包
├── 但不能被命名模块 requires
└── 无法访问其他模块未导出的包 (强封装仍生效)
```

```java
// 典型迁移问题: classpath 库使用了内部 API
// 例: 某 XML 库内部调用了 com.sun.xml.internal.*

// 运行时报错:
// java.lang.IllegalAccessError:
//   class com.thirdparty.XmlUtil (in unnamed module)
//   cannot access class com.sun.xml.internal.* (in module java.xml)

// 临时解决: 添加命令行标志
java --add-exports=java.xml/com.sun.xml.internal.stream=ALL-UNNAMED \
    -cp lib/* com.myapp.Main

// 长期解决: 升级库版本或替换为使用标准 API 的库
```

---

## 10. 服务加载 (ServiceLoader) 与模块

### provides...with 声明

```java
// ── 服务接口模块 ──
module com.example.spi {
    exports com.example.spi;
}

package com.example.spi;
public interface Provider {
    String getName();
    // JDK 9+: 支持 provider() 静态工厂方法
    // 如果实现类有 public static Provider provider() 方法,
    // ServiceLoader 会优先调用它而非无参构造器
}
```

```java
// ── 服务实现模块 ──
module com.example.impl {
    requires com.example.spi;

    // provides...with: 声明服务实现
    // 实现类不需要 exports — 模块系统自动授权 ServiceLoader 访问
    provides com.example.spi.Provider
        with com.example.impl.ProviderImpl;
}

package com.example.impl;
public class ProviderImpl implements com.example.spi.Provider {
    public ProviderImpl() {}  // 必须有 public 无参构造器

    @Override
    public String getName() { return "Impl"; }

    // 可选: 静态工厂方法 (优先于构造器)
    // public static Provider provider() { return new ProviderImpl(); }
}
```

```java
// ── 消费模块 ──
module com.example.app {
    requires com.example.spi;
    uses com.example.spi.Provider;  // 必须声明 uses
}

import com.example.spi.Provider;
import java.util.ServiceLoader;

public class Main {
    public static void main(String[] args) {
        // 惰性加载 (Lazy Loading): stream() API
        ServiceLoader.load(Provider.class)
            .stream()
            .map(ServiceLoader.Provider::get)
            .forEach(p -> System.out.println(p.getName()));

        // 或传统方式
        for (Provider p : ServiceLoader.load(Provider.class)) {
            System.out.println(p.getName());
        }

        // 获取第一个可用实现
        Provider first = ServiceLoader.load(Provider.class)
            .findFirst()
            .orElseThrow(() -> new RuntimeException("No provider found"));
    }
}
```

### META-INF/services 兼容性

```
模块化之前 (JDK 8-):
└── META-INF/services/com.example.spi.Provider
    内容: com.example.impl.ProviderImpl

模块化之后 (JDK 9+):
├── module-info.java 中用 provides...with 声明  ← 推荐
└── META-INF/services/ 仍然支持                  ← 向后兼容
```

| 场景 | META-INF/services | module-info provides | 说明 |
|------|-------------------|---------------------|------|
| 未模块化 JAR | ✅ 唯一方式 | 不适用 | classpath 上的传统 JAR |
| 自动模块 | ✅ 有效 | 不适用 | 无 module-info，依赖 META-INF |
| 命名模块 | ❌ 被忽略 | ✅ 必须使用 | module-info 中的声明优先 |

---

## 11. 迁移实践: 自动模块与未命名模块

### 三种模块类型对比

```
┌─────────────────┬──────────────────┬──────────────────┐
│  命名模块        │  自动模块          │  未命名模块        │
│ (Named Module)  │ (Automatic Module)│ (Unnamed Module) │
├─────────────────┼──────────────────┼──────────────────┤
│ 有 module-info  │ 无 module-info    │ 无 module-info    │
│ 在 module-path  │ 在 module-path    │ 在 classpath      │
│ 只读 requires 的│ 读所有模块         │ 读所有模块         │
│ 只导出 exports 的│ 导出所有包        │ 导出所有包         │
│ 可被 requires   │ 可被 requires     │ 不可被 requires   │
└─────────────────┴──────────────────┴──────────────────┘
```

### 自动模块 (Automatic Module)

```bash
# 传统 JAR 放到 --module-path 上 → 自动成为模块
java --module-path lib/guava-31.1.jar \
    --module myapp/com.example.Main

# 模块名推导规则 (Module Name Derivation):
# 1. 优先: MANIFEST.MF 中的 Automatic-Module-Name
# 2. 备选: 从 JAR 文件名推导
#    guava-31.1-jre.jar  →  guava
#    commons-lang3-3.12.jar  →  commons.lang3
#    规则: 去除版本号, 将 '-' 替换为 '.'
```

```bash
# 在 MANIFEST.MF 中显式指定 (库作者推荐做法)
Manifest-Version: 1.0
Automatic-Module-Name: com.google.common

# 使用 jar 工具查看推导的模块名
jar --describe-module --file=guava-31.1-jre.jar
```

### 未命名模块 (Unnamed Module)

```bash
# classpath 上的所有 JAR → 归入一个 Unnamed Module
java -cp lib/* com.example.Main
# 所有 classpath 上的类共享同一个 Unnamed Module
```

```java
// 命名模块不能 requires 未命名模块
module com.example.app {
    requires unnamed.module;  // ❌ 编译错误! 不存在这样的语法
}

// 解决: 将依赖移到 module-path (变为自动模块)
// 或使用 --add-reads 命令行标志
```

### Split Package 问题 (拆分包)

```
Split Package: 同一个包出现在多个模块中 → 模块系统禁止

示例:
├── module-a.jar
│   └── com/example/util/StringUtils.class
└── module-b.jar
    └── com/example/util/DateUtils.class
           ↑
    同一个包 com.example.util 分散在两个模块中 ❌
```

```bash
# 运行时报错:
# java.lang.module.ResolutionException:
#   Modules module.a and module.b export package com.example.util

# 解决方案:
# 1. 合并到同一个模块
# 2. 重命名包 (推荐)
# 3. 使用 --patch-module 临时修补 (不推荐用于生产)
java --patch-module module.a=module-b.jar \
    --module-path lib \
    -m com.example/com.example.Main
```

### 迁移策略: Bottom-Up (自底向上)

```
推荐迁移顺序:

1. 底层库先模块化 (无外部依赖)
   └── 添加 module-info.java
       └── 先用 Automatic-Module-Name 过渡

2. 中间层库逐步模块化
   └── requires 已模块化的底层库
   └── requires 尚未模块化的库 (作为自动模块)

3. 应用层最后模块化

工具:
  jdeps --generate-module-info out lib/my-lib.jar
  # 自动生成 module-info.java 草稿
```

---

## 12. 分层启动 (Layer)

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

## 13. 相关链接

### 本地文档

- [JVM 调优](../jvm/) - 模块化 JVM 参数
- [类加载](../classloading/) - 模块化类加载

### 外部参考

**JEP 文档:**
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

**技术文档:**
- [JPMS Guide](https://openjdk.org/projects/jigsaw/)
- [State of the Module System](https://openjdk.org/jeps/8207164)
