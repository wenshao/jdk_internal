# 模块/组件源码分析 (Module & Component Source Analysis)

> 本目录包含 JDK 核心模块和组件的源码分析文档

---

## 1. 概述 (Overview)

JDK 源码 `src/` 目录下共有 **72 个顶层目录**（含 `hotspot`、`demo`、`utils`），其中约 **68 个为 Java 模块**（以 `java.*` 或 `jdk.*` 命名）。

本目录分析最重要的核心模块与 HotSpot 组件，共 **13 篇分析文档**。

---

## 2. 模块索引 (Document Index)

### 核心模块 (Core Modules, java.base)

| 文档 | 分析对象 | 源码位置 |
|---|---|---|
| [java.base.md](java.base.md) | java.base 核心模块 | `src/java.base/` |
| [concurrent.md](concurrent.md) | java.util.concurrent 并发包 (97 个文件) | `src/java.base/.../concurrent/` |
| [java.crypto.md](java.crypto.md) | java.security + javax.crypto 安全包 (~235 个文件) | `src/java.base/.../security/`, `.../crypto/` |

### 独立模块 (Standalone Modules)

| 文档 | 模块 | 文件数 | 源码位置 |
|---|---|---|---|
| [java.logging.md](java.logging.md) | java.logging — 日志 API (JUL) | 23 | `src/java.logging/` |
| [java.management.md](java.management.md) | java.management — JMX 管理 | 328 | `src/java.management/` |
| [java.sql.md](java.sql.md) | java.sql — JDBC 数据库连接 | - | `src/java.sql/` |
| [java.net.http.md](java.net.http.md) | java.net.http — HTTP Client | - | `src/java.net.http/` |
| [java.xml.md](java.xml.md) | java.xml — XML 处理 (JAXP) | - | `src/java.xml/` |
| [jdk.compiler.md](jdk.compiler.md) | jdk.compiler — javac 编译器 | - | `src/jdk.compiler/` |

### HotSpot JVM 组件

| 文档 | 分析对象 | 源码位置 |
|---|---|---|
| [hotspot.md](hotspot.md) | HotSpot VM 总体架构 | `src/hotspot/` |
| [hotspot-gc.md](hotspot-gc.md) | 垃圾回收器 (GC) | `src/hotspot/share/gc/` |
| [hotspot-c2.md](hotspot-c2.md) | C2 JIT 编译器 | `src/hotspot/share/opto/` |

---

## 3. JDK 模块全景 (All 72 Source Directories)

### java.* 标准模块 (24 个)

| 模块 | 说明 | 文档状态 |
|---|---|---|
| `java.base` | 核心 API (lang, util, io, net, nio, security, crypto) | [已分析](java.base.md) |
| `java.compiler` | javax.lang.model 编译器接口 | - |
| `java.datatransfer` | 数据传输 (剪贴板) | - |
| `java.desktop` | AWT/Swing/2D/Accessibility | - |
| `java.instrument` | Java Agent / Instrumentation | - |
| `java.logging` | JUL 日志 | [已分析](java.logging.md) |
| `java.management` | JMX 管理 | [已分析](java.management.md) |
| `java.management.rmi` | JMX RMI 连接器 | - |
| `java.naming` | JNDI 命名服务 | - |
| `java.net.http` | HTTP Client (HTTP/1.1, HTTP/2) | [已分析](java.net.http.md) |
| `java.prefs` | 首选项 API | - |
| `java.rmi` | RMI 远程方法调用 | - |
| `java.scripting` | 脚本引擎 API | - |
| `java.se` | 聚合模块 (Java SE 全部 API) | - |
| `java.security.jgss` | GSS-API / Kerberos | - |
| `java.security.sasl` | SASL 认证 | - |
| `java.smartcardio` | 智能卡 I/O | - |
| `java.sql` | JDBC 核心 | [已分析](java.sql.md) |
| `java.sql.rowset` | JDBC RowSet | - |
| `java.transaction.xa` | XA 分布式事务 | - |
| `java.xml` | JAXP XML 处理 | [已分析](java.xml.md) |
| `java.xml.crypto` | XML 数字签名 | - |

### jdk.* 工具/扩展模块 (46 个)

| 模块 | 说明 | 文档状态 |
|---|---|---|
| `jdk.accessibility` | 辅助功能 | - |
| `jdk.attach` | Attach API (连接 JVM) | - |
| `jdk.charsets` | 扩展字符集 | - |
| `jdk.compiler` | javac 编译器 | [已分析](jdk.compiler.md) |
| `jdk.crypto.cryptoki` | PKCS#11 加密提供者 | - |
| `jdk.crypto.ec` | 椭圆曲线加密 | - |
| `jdk.crypto.mscapi` | Windows CAPI 加密 | - |
| `jdk.dynalink` | 动态链接 | - |
| `jdk.editpad` | 编辑器 Pad | - |
| `jdk.graal.compiler` | Graal JIT 编译器 | - |
| `jdk.graal.compiler.management` | Graal 管理 MBean | - |
| `jdk.hotspot.agent` | SA (Serviceability Agent) | - |
| `jdk.httpserver` | 简易 HTTP 服务器 | - |
| `jdk.incubator.vector` | Vector API (孵化) | - |
| `jdk.internal.ed` | 内部编辑器 | - |
| `jdk.internal.jvmstat` | JVM 统计数据 | - |
| `jdk.internal.le` | 行编辑器 (JShell 用) | - |
| `jdk.internal.md` | Markdown 处理 | - |
| `jdk.internal.opt` | 命令行选项解析 | - |
| `jdk.internal.vm.ci` | JVMCI (JIT 编译器接口) | - |
| `jdk.jartool` | jar 工具 | - |
| `jdk.javadoc` | javadoc 工具 | - |
| `jdk.jcmd` | jcmd 诊断命令 | - |
| `jdk.jconsole` | JConsole 监控工具 | - |
| `jdk.jdeps` | jdeps 依赖分析 | - |
| `jdk.jdi` | JDI (调试接口) | - |
| `jdk.jdwp.agent` | JDWP 调试协议代理 | - |
| `jdk.jfr` | JDK Flight Recorder | - |
| `jdk.jlink` | jlink 自定义运行时 | - |
| `jdk.jpackage` | jpackage 打包工具 | - |
| `jdk.jshell` | JShell REPL | - |
| `jdk.jstatd` | jstatd 远程统计 | - |
| `jdk.localedata` | 本地化数据 | - |
| `jdk.management` | 扩展管理 MXBean | - |
| `jdk.management.agent` | JMX Agent | - |
| `jdk.management.jfr` | JFR 管理 MXBean | - |
| `jdk.naming.dns` | DNS 命名提供者 | - |
| `jdk.naming.rmi` | RMI 命名提供者 | - |
| `jdk.net` | 扩展网络 API | - |
| `jdk.nio.mapmode` | 扩展内存映射模式 | - |
| `jdk.sctp` | SCTP 协议 | - |
| `jdk.security.auth` | JAAS 认证扩展 | - |
| `jdk.security.jgss` | GSS-API 扩展 | - |
| `jdk.unsupported` | 不受支持的 API (sun.misc.Unsafe) | - |
| `jdk.unsupported.desktop` | 不受支持的桌面 API | - |
| `jdk.xml.dom` | W3C DOM API | - |
| `jdk.zipfs` | ZIP 文件系统提供者 | - |

### 非模块目录 (2 个)

| 目录 | 说明 |
|---|---|
| `hotspot` | HotSpot JVM C++ 源码 |
| `demo` | 示例代码 |
| `utils` | 构建工具 |

---

## 4. 源码结构 (Source Layout)

```
jdk/src/
├── java.base/                  # 核心模块 (最大)
│   ├── share/classes/          # 平台无关 Java 源码
│   │   ├── java/lang/          #   java.lang 包
│   │   ├── java/util/          #   java.util (含 concurrent)
│   │   ├── java/io/            #   java.io 包
│   │   ├── java/net/           #   java.net 包
│   │   ├── java/nio/           #   java.nio 包
│   │   ├── java/security/      #   JCA (81 个文件)
│   │   ├── javax/crypto/       #   JCE (42 个文件)
│   │   └── jdk/internal/       #   内部 API
│   ├── share/native/           # 本地 C/C++ 代码
│   ├── share/conf/             # 配置文件 (security/java.security)
│   ├── unix/                   # Unix/Linux/macOS 特定
│   └── windows/                # Windows 特定
│
├── java.logging/               # 日志模块 (23 个文件)
│   └── share/classes/
│       ├── java/util/logging/  #   JUL API
│       └── sun/util/logging/   #   内部实现
│
├── java.management/            # JMX 模块 (328 个文件)
│   └── share/classes/
│       ├── java/lang/management/ # 平台 MXBean
│       ├── javax/management/   #   JMX 核心
│       └── sun/management/     #   HotSpot MXBean 实现
│
├── hotspot/                    # HotSpot JVM (C++)
│   └── share/
│       ├── gc/                 #   GC 实现 (G1/ZGC/Shenandoah/...)
│       ├── opto/               #   C2 JIT 编译器
│       ├── runtime/            #   运行时
│       └── ...
│
└── jdk.compiler/               # javac 编译器
    └── share/classes/
        └── com/sun/tools/javac/
```

---

## 5. 模块依赖图 (Module Dependency Graph)

```
                         ┌─────────────┐
                         │   java.se   │  (聚合模块)
                         └──────┬──────┘
                                │
         ┌──────────────────────┼──────────────────────┐
         │                      │                      │
  ┌──────┴──────┐   ┌──────────┴──────────┐   ┌──────┴──────┐
  │java.desktop │   │ java.management     │   │ java.naming │
  └──────┬──────┘   └──────────┬──────────┘   └──────┬──────┘
         │                      │                      │
  ┌──────┴──────┐   ┌──────────┴──────────┐           │
  │java.xml     │   │ java.management.rmi │           │
  └──────┬──────┘   └──────────┬──────────┘           │
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                │
                         ┌──────┴──────┐
                         │  java.base  │  (根模块, 所有模块隐式依赖)
                         └─────────────┘
```

---

## 6. 文档模板 (Document Template)

每篇模块分析文档包含：

1. **模块概述 (Overview)**: 模块定义、包结构、文件统计
2. **完整类清单 (Class Listing)**: 基于实际源码的类列表
3. **核心类分析 (Key Class Analysis)**: 重要类的源码解读
4. **架构图 (Architecture)**: 组件关系和数据流
5. **使用示例 (Usage Examples)**: 基于实际 API 的代码示例
6. **相关链接 (References)**: 源码路径和官方文档

---

## 7. 相关链接 (References)

- [JDK 模块规范](https://openjdk.org/projects/jdk/21/spec/)
- [API 文档 (Javadoc)](https://docs.oracle.com/en/java/javase/21/docs/api/)
- [OpenJDK 源码](https://github.com/openjdk/jdk)
- 本地源码: `/root/git/jdk/src/`
