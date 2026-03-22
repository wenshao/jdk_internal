# 类加载

> ClassLoader、双亲委派、模块化类加载演进历程

[← 返回核心平台](../)

---
## 目录

1. [快速概览](#1-快速概览)
2. [核心贡献者](#2-核心贡献者)
3. [类加载过程详解](#3-类加载过程详解)
4. [双亲委派模型](#4-双亲委派模型)
5. [类加载器层次](#5-类加载器层次)
6. [线程上下文类加载器 (TCCL)](#6-线程上下文类加载器-tccl)
7. [元空间 (Metaspace)](#7-元空间-metaspace)
8. [模块化类加载 (JDK 9+)](#8-模块化类加载-jdk-9)
9. [自定义类加载器](#9-自定义类加载器)
10. [CDS / AppCDS / AOT 深入](#10-cds--appcds--aot-深入)
11. [类卸载 (Class Unloading)](#11-类卸载-class-unloading)
12. [常见问题排查](#12-常见问题排查)
13. [类加载器泄漏](#13-类加载器泄漏)
14. [重要 PR 分析](#14-重要-pr-分析)
15. [类加载最佳实践](#15-类加载最佳实践)
16. [相关链接](#16-相关链接)

---


## 1. 快速概览

```
JDK 1.0 ── JDK 1.2 ── JDK 6 ── JDK 8 ── JDK 9 ── JDK 17 ── JDK 21 ── JDK 26
   │         │        │        │        │        │        │        │
类加载   双亲    线程上下   元空间   模块化   层层    外部    CDS
机制    委派    类加载器   类加载   类加载   初始化   函数    改进
                (TCCL)   (Metaspace) (JPMS) (Layinit) (FFM)  (AOT)
```

### 核心演进

| 版本 | 特性 | 说明 | JEP |
|------|------|------|-----|
| **JDK 1.0** | ClassLoader | 基础类加载 | - |
| **JDK 1.2** | 双亲委派 | 安全性保证 | - |
| **JDK 1.2** | 线程上下文类加载器 | JavaEE 支持 | - |
| **JDK 5** | CDS (初版) | 核心类共享 metadata | - |
| **JDK 8** | 元空间 | 取代永久代 | - |
| **JDK 9** | 模块化类加载 | JPMS | JEP 220 |
| **JDK 10** | AppCDS | 扩展到应用类 | JEP 310 |
| **JDK 13** | Dynamic CDS | 运行时动态归档 | JEP 350 |
| **JDK 21** | 外部函数 | 不依赖 JNI | JEP 442 |
| **JDK 24** | AOT Class Loading | 预完成 loading/linking | JEP 483 |
| **JDK 26** | AOT Object Caching | Ahead-of-Time 对象缓存 (任意 GC) | JEP 516 |

---

## 2. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 类加载团队 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | [Coleen Phillimore](/by-contributor/profiles/coleen-phillimore.md) | 341 | Oracle | SystemDictionary |
| 2 | [Ioi Lam](/by-contributor/profiles/ioi-lam.md) | 254 | Oracle | CDS, AOT |
| 3 | Calvin Cheung | 103 | Oracle | 类加载器 |
| 4 | Harold Seigel | 89 | Oracle | JVM 运行时 |
| 5 | Stefan Karlsson | 87 | Oracle | 并发 GC |
| 6 | Jiangli Zhou | 74 | Oracle | CDS, 存档 |
| 7 | [David Holmes](/by-contributor/profiles/david-holmes.md) | 68 | Oracle | 并发类加载 |

---

## 3. 类加载过程详解

JVM 规范 (JVMS Chapter 5) 将类的生命周期分为三大阶段: **Loading → Linking → Initialization**。

### 3.1 加载 (Loading)

加载阶段由 `ClassLoader.loadClass()` 触发，核心方法链:

```
loadClass(name)
  ├── findLoadedClass(name)    // 检查已加载 (native 方法，查 SystemDictionary)
  ├── parent.loadClass(name)   // 双亲委派
  └── findClass(name)          // 自行加载
        └── defineClass()      // 将 byte[] 转为 Class 对象 (native)
```

**`findClass(String name)`** — 子类覆盖此方法实现自定义查找逻辑:

```java
// java.lang.ClassLoader (JDK 源码简化)
protected Class<?> findClass(String name) throws ClassNotFoundException {
    throw new ClassNotFoundException(name);
}

// 模块化版本 (JDK 9+)
protected Class<?> findClass(String moduleName, String name) {
    // 从指定模块中查找类
    return null;  // 默认返回 null，由子类覆盖
}
```

**`defineClass(name, byte[], off, len)`** — 将字节数组转化为 Class 对象:

```java
// java.lang.ClassLoader 核心 native 方法
protected final Class<?> defineClass(String name, byte[] b, int off, int len,
                                      ProtectionDomain protectionDomain)
    throws ClassFormatError
{
    // 1. 前置检查 (preDefineClass): 包名安全检查，禁止定义 java.* 包的类
    // 2. 调用 native defineClass0/defineClass1/defineClass2
    //    → HotSpot: SystemDictionary::resolve_from_stream()
    // 3. 后置处理 (postDefineClass): 注册 ProtectionDomain
    // 4. 返回 Class<?> 对象 (mirror of InstanceKlass)
}
```

HotSpot 内部，`defineClass` 会创建 `InstanceKlass` 对象并存入 `SystemDictionary`。一个类由 **(ClassLoader, fully-qualified-name)** 二元组唯一标识 — 不同 ClassLoader 加载的同名类是不同的 Class 对象。

### 3.2 链接 (Linking)

链接分为三个子阶段，对应 JVMS 5.4:

```
┌────────────────────────────────────────────────────────────────┐
│                       Linking 阶段                              │
├──────────────┬─────────────────────────────────────────────────┤
│              │                                                 │
│  验证         │  Verification — 确保 class 文件格式正确          │
│ (Verification)│  ├── 文件格式验证: magic number (0xCAFEBABE),   │
│              │  │   版本号, 常量池标签                           │
│              │  ├── 元数据验证: 父类合法性, final 继承检查       │
│              │  ├── 字节码验证: 操作数栈类型安全 (Type Checking)  │
│              │  └── 符号引用验证: 类/字段/方法的访问权限          │
│              │                                                 │
├──────────────┼─────────────────────────────────────────────────┤
│              │                                                 │
│  准备         │  Preparation — 分配静态变量内存并设零值           │
│ (Preparation)│  ├── static int x = 42;    → 准备阶段: x = 0    │
│              │  ├── static String s;      → 准备阶段: s = null  │
│              │  └── static final int C=42 → 准备阶段: C = 42   │
│              │      (ConstantValue 属性的 compile-time constant │
│              │       在准备阶段直接赋值，不等到初始化)            │
│              │                                                 │
├──────────────┼─────────────────────────────────────────────────┤
│              │                                                 │
│  解析         │  Resolution — 符号引用 → 直接引用               │
│ (Resolution) │  ├── 类/接口解析: CONSTANT_Class → InstanceKlass*│
│              │  ├── 字段解析: CONSTANT_Fieldref → 字段偏移量     │
│              │  ├── 方法解析: CONSTANT_Methodref → Method*      │
│              │  └── 可延迟到首次使用时 (lazy resolution)         │
│              │                                                 │
└──────────────┴─────────────────────────────────────────────────┘
```

> **注意**: `static final` 字段如果携带 `ConstantValue` 属性 (即编译期常量，如 `static final int X = 42`)，其值在 Preparation 阶段就会赋上，而非等到 Initialization。非编译期常量的 `static final` (如 `static final Object O = new Object()`) 仍在 `<clinit>` 中初始化。

### 3.3 初始化 (Initialization)

初始化阶段执行类的 `<clinit>` 方法 (class initialization method):

```java
// <clinit> 由编译器自动收集以下内容合成:
// 1. 所有 static 变量的赋值语句
// 2. 所有 static {} 块
// 按源码中出现顺序合并

public class Example {
    static int a = 1;                    // 收入 <clinit>
    static { System.out.println("init"); } // 收入 <clinit>
    static int b = a + 1;               // 收入 <clinit>
}
```

**初始化触发时机** (JVMS 5.5 "An implementation may provide the option of ..."):

| 触发条件 | 说明 |
|----------|------|
| `new` / `getstatic` / `putstatic` / `invokestatic` | 首次主动使用 |
| 反射调用 (`Class.forName(name, true, loader)`) | `initialize=true` |
| 子类初始化 | 父类尚未初始化时先初始化父类 |
| 主类 (main method 所在类) | JVM 启动 |
| `MethodHandle` 解析 `REF_getStatic` 等 | 首次解析 |

**`<clinit>` 线程安全**: JVM 保证 `<clinit>` 在多线程环境下只执行一次。HotSpot 使用 `InstanceKlass::_init_state` 状态机 + `InstanceKlass::_init_lock` 互斥锁实现。如果线程 A 正在执行 `<clinit>`，线程 B 尝试初始化同一个类将阻塞直到 A 完成。

```
状态机: allocated → loaded → linked → being_initialized → fully_initialized
                                              │
                                              └→ initialization_error (如果 <clinit> 抛异常)
```

---

## 4. 双亲委派模型

### 原理

```java
// java.lang.ClassLoader.loadClass() — 双亲委派的核心实现
protected Class<?> loadClass(String name, boolean resolve)
    throws ClassNotFoundException
{
    synchronized (getClassLoadingLock(name)) {
        // 1. 检查是否已加载 (查 VM 内部缓存)
        Class<?> c = findLoadedClass(name);
        if (c == null) {
            try {
                // 2. 委派父加载器
                if (parent != null) {
                    c = parent.loadClass(name, false);
                } else {
                    c = findBootstrapClassOrNull(name);
                }
            } catch (ClassNotFoundException e) {
                // 父加载器无法加载
            }
            if (c == null) {
                // 3. 父加载器未找到，自己加载
                c = findClass(name);
            }
        }
        if (resolve) {
            resolveClass(c);
        }
        return c;
    }
}
```

### 优势

1. **安全性 (Security)**: 防止替换核心类 (如 `java.lang.String`)
2. **避免重复加载 (Avoid Duplicates)**: 父加载器已加载的类不会重复加载
3. **层次清晰 (Clear Hierarchy)**: 职责明确

### 打破双亲委派的经典场景

| 场景 | 机制 | 典型案例 |
|------|------|----------|
| SPI (服务发现) | TCCL (线程上下文类加载器) | JDBC `DriverManager`, JNDI |
| OSGi / 模块化容器 | 网状委派 (Peer Delegation) | Eclipse Equinox, Apache Felix |
| 热部署 (Hot Deploy) | 丢弃旧 ClassLoader，创建新实例 | Tomcat WebappClassLoader |
| 代码加密 | 自定义 `findClass` 解密字节码 | 商业软件保护 |

子优先 (child-first) 模式: 覆盖 `loadClass()`，先调用 `findClass()` 自行加载，失败时再委派 `super.loadClass()`。

---

## 5. 类加载器层次

### JDK 8 及之前: 三层结构

```
┌──────────────────────────────────────────────────────────────┐
│  Bootstrap ClassLoader (启动类加载器)                          │
│  ├── 实现: C++ (HotSpot 内部, 不可见 Java 代码中)             │
│  ├── getClassLoader() 返回 null                              │
│  ├── 加载路径: $JAVA_HOME/lib/rt.jar, charsets.jar 等        │
│  └── 加载内容: java.*, javax.*, sun.* 核心类                 │
│       │                                                      │
│       ▼                                                      │
│  Extension ClassLoader (扩展类加载器)                         │
│  ├── 实现: sun.misc.Launcher$ExtClassLoader                  │
│  ├── 加载路径: $JAVA_HOME/lib/ext/*.jar                      │
│  └── 加载内容: JCE, JMX 等扩展库                             │
│       │                                                      │
│       ▼                                                      │
│  Application ClassLoader (应用类加载器)                       │
│  ├── 实现: sun.misc.Launcher$AppClassLoader                  │
│  ├── 加载路径: -cp / -classpath / CLASSPATH                  │
│  └── 加载内容: 用户应用类                                     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### JDK 9+: 模块化后的变化

```
┌──────────────────────────────────────────────────────────────┐
│  Bootstrap ClassLoader (启动类加载器)                          │
│  ├── 实现: C++ (不变)                                         │
│  ├── getClassLoader() 仍返回 null                             │
│  ├── 加载模块: java.base (核心)                               │
│  └── 不再加载 rt.jar (模块化 jimage 格式)                     │
│       │                                                      │
│       ▼                                                      │
│  Platform ClassLoader (平台类加载器) ← 取代 ExtClassLoader    │
│  ├── 实现: jdk.internal.loader.ClassLoaders$PlatformClassLoader│
│  ├── 父类: BuiltinClassLoader (新增)                          │
│  ├── 加载模块: java.sql, java.xml, java.logging 等           │
│  └── 不再依赖 ext 目录 (已移除)                               │
│       │                                                      │
│       ▼                                                      │
│  Application ClassLoader (应用类加载器)                       │
│  ├── 实现: jdk.internal.loader.ClassLoaders$AppClassLoader    │
│  ├── 父类: BuiltinClassLoader                                │
│  ├── 加载路径: -cp / --module-path                           │
│  └── 不再是 URLClassLoader 的子类 (JDK 9 破坏性变更)          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**关键变更 (JDK 9)**:

| 变化 | JDK 8 | JDK 9+ |
|------|-------|--------|
| Extension ClassLoader | `sun.misc.Launcher$ExtClassLoader` | 已移除，替换为 PlatformClassLoader |
| AppClassLoader 父类 | `URLClassLoader` | `BuiltinClassLoader` (不再是 URLClassLoader) |
| 类存储格式 | rt.jar, ext/*.jar | jimage 模块化格式 (`$JAVA_HOME/lib/modules`) |
| `sun.boot.class.path` 属性 | 可用 | 已移除 |
| `ClassLoader.getSystemClassLoader()` 返回类型 | `URLClassLoader` (可强转) | `AppClassLoader` (强转到 URLClassLoader 会 ClassCastException) |

```java
// JDK 9+ 获取类加载器
ClassLoader bootstrap = null;                           // 始终为 null
ClassLoader platform  = ClassLoader.getPlatformClassLoader();  // 新 API
ClassLoader app       = ClassLoader.getSystemClassLoader();

// 验证层次
System.out.println(app.getParent());           // PlatformClassLoader
System.out.println(platform.getParent());      // null (Bootstrap)
```

### BuiltinClassLoader 架构 (JDK 9+)

JDK 9 引入 `jdk.internal.loader.BuiltinClassLoader` 作为三个内置加载器的公共父类:

```
                    ClassLoader (java.lang)
                         │
                    SecureClassLoader
                         │
                   BuiltinClassLoader  ← JDK 9 新增
                    ├── loadClassOrNull(name) — 模块感知的加载逻辑
                    ├── 查询 module → loader 的映射表
                    └── 不再沿用简单的 parent delegation
                   ╱              ╲
    PlatformClassLoader     AppClassLoader
```

`BuiltinClassLoader.loadClassOrNull()` 的加载逻辑不再是简单的双亲委派，而是**模块感知**的:
1. 如果目标类在一个已知模块中 → 直接找到该模块对应的 loader 加载
2. 否则 → 回退到双亲委派

---

## 6. 线程上下文类加载器 (TCCL)

### 问题背景

**问题**: 双亲委派模型下，Bootstrap ClassLoader 加载的核心类 (如 `java.sql.DriverManager`) 无法加载应用类路径上的类 (如 MySQL JDBC 驱动)。

**解决**: Thread Context ClassLoader (TCCL) — 每个线程携带一个类加载器引用，默认继承父线程的 TCCL，通常为 AppClassLoader。

### SPI 使用场景

```java
// JDBC DriverManager 示例 — 经典的 SPI 场景
// DriverManager 在 java.base 模块中 (Bootstrap ClassLoader 加载)
// MySQL 驱动在应用 classpath 上 (AppClassLoader 加载)

// DriverManager 内部使用 TCCL:
public class DriverManager {
    private static Connection getConnection(...) {
        // 使用调用者的 ClassLoader 或 TCCL
        ClassLoader callerCL = caller != null ? caller.getClassLoader() : null;
        if (callerCL == null) {
            callerCL = Thread.currentThread().getContextClassLoader();
        }
        // 通过 TCCL 发现并加载 JDBC 驱动
    }
}

// ServiceLoader 也依赖 TCCL:
ServiceLoader<Driver> drivers = ServiceLoader.load(Driver.class);
// 等同于:
ServiceLoader.load(Driver.class, Thread.currentThread().getContextClassLoader());
```

### 最佳实践: 切换 TCCL 时保存和恢复

```java
ClassLoader original = Thread.currentThread().getContextClassLoader();
try {
    Thread.currentThread().setContextClassLoader(customLoader);
    ServiceLoader.load(MyService.class);  // 使用 customLoader 加载
} finally {
    Thread.currentThread().setContextClassLoader(original);
}
```

---

## 7. 元空间 (Metaspace)

### JDK 8 变化

**JDK 7**: 永久代 (PermGen)
**JDK 8+**: 元空间 (Metaspace)

### 对比

| 特性 | 永久代 (PermGen) | 元空间 (Metaspace) |
|------|-----------------|-------------------|
| 位置 | 堆内 (Heap) | 本地内存 (Native Memory) |
| 大小 | 固定 (`-XX:MaxPermSize`) | 动态增长 (受物理内存限制) |
| GC | Full GC 触发 | 当达到阈值时触发 |
| OOM | `OutOfMemoryError: PermGen space` | `OutOfMemoryError: Metaspace` |
| 存储内容 | 类元数据 + 字符串常量池 | 仅类元数据 (字符串常量池移至堆) |

### Metaspace 内部结构

```
┌──────────────────────────────────────────────────────┐
│                  Metaspace                            │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Compressed Class Space (压缩类空间)                   │
│  ├── Klass 结构体 (InstanceKlass, ArrayKlass 等)      │
│  ├── 使用压缩指针 (narrow Klass pointer)              │
│  └── 大小: -XX:CompressedClassSpaceSize (默认 1G)     │
│                                                      │
│  Non-Class Metaspace (非类元空间)                      │
│  ├── Method 对象                                     │
│  ├── ConstantPool (常量池)                            │
│  ├── Annotations (注解)                              │
│  └── Bytecodes (字节码)                              │
│                                                      │
│  每个 ClassLoader 拥有独立的 ClassLoaderMetaspace      │
│  └── 当 ClassLoader 被 GC 回收时，                    │
│      其 ClassLoaderMetaspace 整体释放                  │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### 配置参数

```bash
# 元空间大小
-XX:MetaspaceSize=256m              # 初始高水位 (首次触发 GC 的阈值)
-XX:MaxMetaspaceSize=512m           # 最大大小 (默认无限制)

# 压缩类指针
-XX:CompressedClassSpaceSize=1g     # 压缩类空间大小

# 类数据共享
-XX:SharedClassListFile=classes.lst # 类列表
-XX:SharedArchiveFile=app.jsa       # 共享归档
```

---

## 8. 模块化类加载 (JDK 9+)

### JEP 220: 模块化系统

**影响**:
- 扩展机制移除 (`ext` 目录废弃)
- 类加载器重构 (`BuiltinClassLoader` 引入)
- 封装性增强 (module `exports` / `opens`)

### 模块 → 类加载器映射

```
┌────────────────────────────────────────────────────────────┐
│              模块化类加载器结构 (JDK 9+)                      │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Bootstrap ClassLoader                                     │
│  └── java.base (String, Object, ClassLoader, Thread ...)   │
│                                                            │
│  Platform ClassLoader                                      │
│  ├── java.sql (JDBC API)                                   │
│  ├── java.xml (XML 处理)                                   │
│  ├── java.logging (日志)                                   │
│  ├── java.desktop (AWT/Swing)                              │
│  └── ... (大部分 java.* 和 jdk.* 模块)                     │
│                                                            │
│  App ClassLoader                                           │
│  ├── 未命名模块 (classpath 上的类)                          │
│  └── 应用命名模块 (--module-path 上的类)                    │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 模块化类加载特性

```java
// 模块化类加载检查
Module module = MyClass.class.getModule();

// 检查模块是否导出包
boolean isExported = module.isExported("com.example.internal");

// 检查模块是否打开包 (反射)
boolean isOpen = module.isOpen("com.example.internal");

// 运行时 --add-opens (打破模块封装)
// java --add-opens java.base/java.lang=ALL-UNNAMED MyApp
```

### ModuleLayer (模块层)

```java
// 自定义 ModuleLayer — 可实现插件化类加载
ModuleFinder finder = ModuleFinder.of(Path.of("plugins/"));
ModuleLayer parent = ModuleLayer.boot();

Configuration cf = parent.configuration()
    .resolve(finder, ModuleFinder.of(), Set.of("com.example.plugin"));

ClassLoader pluginLoader = new URLClassLoader(/* plugin jars */);
ModuleLayer layer = parent.defineModulesWithOneLoader(cf, pluginLoader);

// 从自定义层加载类
Class<?> pluginClass = layer.findLoader("com.example.plugin")
    .loadClass("com.example.plugin.Main");
```

---

## 9. 自定义类加载器

### 9.1 URLClassLoader

`URLClassLoader` 是最常用的预置自定义类加载器，支持从 URL (jar/目录) 加载类:

```java
// 从外部 JAR 加载类
URL[] urls = { new URL("file:///path/to/plugin.jar") };
try (URLClassLoader loader = new URLClassLoader(urls, getClass().getClassLoader())) {
    Class<?> clazz = loader.loadClass("com.plugin.MyPlugin");
    Object instance = clazz.getDeclaredConstructor().newInstance();
}
// 注意: JDK 9+ AppClassLoader 不再继承 URLClassLoader
// 不可: (URLClassLoader) ClassLoader.getSystemClassLoader()
```

### 9.2 ServiceLoader (SPI)

`ServiceLoader` 是 Java 标准的服务发现机制，依赖类加载器查找 `META-INF/services/` 或 `module-info.java` 中声明的实现:

```java
// 传统方式: META-INF/services/com.example.PaymentProcessor 文件中声明实现类名
ServiceLoader<PaymentProcessor> processors = ServiceLoader.load(PaymentProcessor.class);
for (PaymentProcessor p : processors) { p.process(amount); }

// 模块化方式 (JDK 9+): module-info.java 中声明
// provides com.example.PaymentProcessor with com.example.StripeProcessor;
// uses com.example.PaymentProcessor;
```

### 9.3 热部署模式 (Hot Deploy)

热部署的核心原理: **丢弃旧 ClassLoader，创建新 ClassLoader 重新加载类**。

```java
public class HotDeployManager {
    private volatile ClassLoader currentLoader;
    private final String classpath;

    public HotDeployManager(String classpath) {
        this.classpath = classpath;
        reload();
    }

    public void reload() {
        // 丢弃旧 ClassLoader (及其所有已加载的类)
        // 前提: 不存在外部强引用指向旧 loader 或其加载的对象
        currentLoader = new HotSwapClassLoader(classpath,
            getClass().getClassLoader());
    }

    public Object createInstance(String className) throws Exception {
        Class<?> clazz = currentLoader.loadClass(className);
        return clazz.getDeclaredConstructor().newInstance();
    }
}

public class HotSwapClassLoader extends ClassLoader {
    private final String classpath;

    public HotSwapClassLoader(String classpath, ClassLoader parent) {
        super(parent);
        this.classpath = classpath;
    }

    @Override
    protected Class<?> findClass(String name)
            throws ClassNotFoundException {
        byte[] classBytes = loadClassBytes(name);
        if (classBytes == null) {
            throw new ClassNotFoundException(name);
        }
        return defineClass(name, classBytes, 0, classBytes.length);
    }

    private byte[] loadClassBytes(String name) {
        String path = classpath + "/"
            + name.replace('.', '/') + ".class";
        try {
            return Files.readAllBytes(Paths.get(path));
        } catch (IOException e) {
            return null;
        }
    }
}
```

> **热部署陷阱**: 如果旧 ClassLoader 或其加载的类仍被引用 (如 ThreadLocal、static 集合、JMX MBean 注册)，则旧 ClassLoader 无法被 GC，导致 Metaspace 泄漏。参见 [第 13 节: 类加载器泄漏](#13-类加载器泄漏)。

### 9.4 字节码加密

```java
// 自定义 ClassLoader 解密字节码后调用 defineClass
public class DecryptClassLoader extends ClassLoader {
    @Override
    protected Class<?> findClass(String name) throws ClassNotFoundException {
        byte[] decrypted = decrypt(loadEncryptedClass(name), key);
        return defineClass(name, decrypted, 0, decrypted.length);
    }
}
```

---

## 10. CDS / AppCDS / AOT 深入

### 10.1 CDS 演进时间线

| JEP | JDK | 名称 | 关键能力 |
|-----|-----|------|----------|
| — | 5 | CDS (初版) | 共享核心类 metadata，多 JVM 进程共享只读内存 |
| JEP 310 | 10 | Application CDS (AppCDS) | 扩展到应用类和第三方库 |
| JEP 341 | 12 | Default CDS Archives | JDK 构建时自动生成默认 CDS archive |
| JEP 350 | 13 | Dynamic CDS Archives | 运行结束时自动生成 archive，无需预跑类列表 |
| JEP 483 | 24 | AOT Class Loading & Linking | 预完成 loading + linking (验证/准备/解析) |
| JEP 516 | 26 | AOT Cache | 统一 cache: metadata + compiled code + heap objects + profiling |

### 10.2 共享归档结构 (Shared Archive)

CDS archive (`.jsa` 文件) 的内部结构:

```
┌──────────────────────────────────────────────────────────────┐
│                  CDS Archive (.jsa)                           │
├──────────────────────────────────────────────────────────────┤
│  Header                                                      │
│  ├── magic number, 版本号                                    │
│  ├── JVM 配置指纹 (确保兼容性)                                │
│  └── 各 region 的 offset 和 size                             │
├──────────────────────────────────────────────────────────────┤
│  RW Region (read-write)                                      │
│  ├── InstanceKlass / ArrayKlass                              │
│  ├── ConstantPool (可变部分: resolved entries)               │
│  └── 需要运行时修改的 metadata                                │
├──────────────────────────────────────────────────────────────┤
│  RO Region (read-only)                                       │
│  ├── Method, ConstMethod                                     │
│  ├── 字节码 (bytecodes)                                      │
│  ├── Symbol (类名, 方法签名)                                 │
│  └── 多进程间通过 mmap 共享此区域 (节省物理内存)              │
├──────────────────────────────────────────────────────────────┤
│  Relocation Bitmaps (BM)                                     │
│  └── 地址重定位信息 (ASLR 支持)                              │
├──────────────────────────────────────────────────────────────┤
│  Heap Region (HP)  — JEP 516 增强                            │
│  ├── 预初始化的 Java 对象                                    │
│  ├── interned String 对象                                    │
│  └── 静态 final 字段引用的对象图                              │
├──────────────────────────────────────────────────────────────┤
│  AOT Code Region (AC) — JEP 516 新增                         │
│  ├── C1/C2 编译的 native code                                │
│  └── Method profiling data (来自 JEP 515)                    │
└──────────────────────────────────────────────────────────────┘
```

### 10.3 Dynamic CDS (JEP 350, JDK 13)

Dynamic CDS 简化了 archive 创建流程，无需预先生成类列表:

```bash
# 传统方式 (三步)
java -XX:DumpLoadedClassList=classes.lst -cp app.jar Main    # 1. 生成类列表
java -Xshare:dump -XX:SharedClassListFile=classes.lst \
    -XX:SharedArchiveFile=app.jsa -cp app.jar                # 2. 生成归档
java -Xshare:on -XX:SharedArchiveFile=app.jsa -cp app.jar Main  # 3. 使用

# Dynamic CDS (一步训练 + 使用)
java -XX:ArchiveClassesAtExit=app.jsa -cp app.jar Main       # 训练运行结束时自动 dump
java -XX:SharedArchiveFile=app.jsa -cp app.jar Main          # 后续使用
```

### 10.4 JEP 483: AOT Class Loading & Linking (JDK 24)

JEP 483 将 CDS 从仅缓存 metadata 升级为**预完成 loading 和 linking**:

- **传统 CDS**: 启动时仍需执行 verification、preparation、resolution
- **JEP 483**: 在 archive 中存储已验证、已链接的类 → 启动时直接跳过这些步骤

```bash
# JDK 24+ AOT class loading
java -XX:AOTMode=record -XX:AOTConfiguration=app.aotconf -cp app.jar Main
java -XX:AOTMode=create -XX:AOTConfiguration=app.aotconf \
     -XX:AOTCache=app.aot -cp app.jar
java -XX:AOTCache=app.aot -cp app.jar Main
```

### 10.5 JEP 516: AOT Cache (JDK 26)

JEP 516 是 Project Leyden 的里程碑式交付，将四类数据统一到一个 AOT Cache 文件中:

| 数据类型 | 说明 | 来源 |
|----------|------|------|
| **Class Metadata** | 已加载、验证、链接的 class 数据 | 继承自 CDS / JEP 483 |
| **Compiled Native Code** | C1/C2 编译的 machine code | JEP 516 新增 |
| **Method Profiling Data** | 调用频率、分支概率、类型反馈 | 来自 JEP 515 |
| **Heap Objects** | 预初始化的 Java 对象 (String 常量池等) | JEP 516 增强 |

```bash
# JDK 26 AOT Cache — 简化工作流
# 训练运行 (record + create 合一)
java -XX:AOTCacheOutput=app.aot -cp app.jar Main

# 生产运行
java -XX:AOTCache=app.aot -cp app.jar Main
```

**性能提升** (来自 JEP 516 文档):
- 启动时间: 减少 40-60% (取决于应用规模)
- 预热时间: 显著缩短 (pre-compiled native code + profiling data)
- 内存共享: 多进程共享 RO region (容器场景尤为有效)

### 10.6 HotSpot 内部: AOTMetaspace

AOT Cache 在 HotSpot 中由 `AOTMetaspace` 类管理 (`src/hotspot/share/cds/aotMetaspace.hpp`)，内部维护 5 个 region: `rw` (read-write, 可变类元数据)、`ro` (read-only, 多进程 mmap 共享)、`bm` (relocation bitmaps)、`hp` (heap objects)、`ac` (aot compiled code)。启动时通过 `_relocation_delta` 处理 ASLR 地址重定位。

---

## 11. 类卸载 (Class Unloading)

### 卸载条件

一个类可以被卸载，当且仅当满足以下**全部条件**:

1. **加载该类的 ClassLoader 实例不可达** (不再被任何活动线程或对象引用)
2. **该 ClassLoader 加载的所有 Class 对象不可达**
3. **这些 Class 的所有实例对象不可达**

```
ClassLoader → Class → Instance
    ↑            ↑        │
    │            │        │  (如果 Instance 持有 Class 引用，
    │            └────────┘   Class 持有 ClassLoader 引用)
    │
    └─ 只要 ClassLoader 可达，其所有类都不会被卸载
```

> **注意**: Bootstrap ClassLoader、Platform ClassLoader、App ClassLoader 是 JVM 内部持有的，永远不会被 GC → 它们加载的类**永远不会被卸载**。只有自定义 ClassLoader 加载的类才有可能被卸载。

### Metaspace 回收

当 ClassLoader 被 GC 回收时:
1. 该 ClassLoader 的 `ClassLoaderMetaspace` 被释放
2. 其中所有 `InstanceKlass` 从 `SystemDictionary` 移除
3. Metaspace 的 chunk 返还给全局 `ChunkManager`
4. 如果空闲 chunk 足够，物理内存可归还操作系统

```bash
# 监控类卸载
java -verbose:class -Xlog:class+unload=info MyApp

# 输出示例:
# [class,unload] unloading class com.example.OldPlugin 0x00007f1234567890
```

### 强制卸载? 不可能

JVM 不提供任何 API 强制卸载一个类。唯一的方式是确保 ClassLoader 及其加载的所有类和实例都不可达，然后**等待 GC**。

```java
// 正确的类卸载模式
WeakReference<ClassLoader> loaderRef;

{
    ClassLoader loader = new HotSwapClassLoader("path", parent);
    Class<?> clazz = loader.loadClass("com.example.Plugin");
    Object instance = clazz.getDeclaredConstructor().newInstance();
    loaderRef = new WeakReference<>(loader);

    // 使用 instance ...

    // 释放所有引用
    instance = null;
    clazz = null;
    loader = null;
}

System.gc();  // 建议 GC (不保证)
// loaderRef.get() == null 时，类已卸载
```

### 类卸载与 GC 算法

| GC 算法 | 类卸载支持 | 触发时机 |
|---------|-----------|----------|
| G1 GC | 支持 (默认开启) | Concurrent Cycle 或 Full GC |
| ZGC | 支持 (JDK 16+) | Concurrent Phase |
| Shenandoah | 支持 | Concurrent Phase |
| Serial GC | 支持 | Full GC |
| Parallel GC | 支持 | Full GC |

```bash
# 控制类卸载的 JVM 参数
-XX:+ClassUnloading           # 启用类卸载 (默认 true)
-XX:+ClassUnloadingWithConcurrentMark  # G1: concurrent mark 时卸载 (默认 true)
```

---

## 12. 常见问题排查

### 12.1 ClassNotFoundException vs NoClassDefFoundError

这两个异常经常混淆，但含义和触发场景完全不同:

| 特征 | `ClassNotFoundException` | `NoClassDefFoundError` |
|------|--------------------------|------------------------|
| 类型 | **受检异常** (checked, extends `ReflectiveOperationException`) | **错误** (unchecked, extends `LinkageError`) |
| 触发时机 | 显式加载时 (runtime) | 隐式加载时 (link time) |
| 触发方式 | `Class.forName()`, `ClassLoader.loadClass()` | JVM 在解析类依赖时自动触发 |
| 含义 | 类在 classpath 上**完全找不到** | 类在**编译时存在**但运行时缺失，或 `<clinit>` 失败 |
| 常见原因 | JAR 缺失、classpath 配置错误 | 依赖 JAR 缺失、static 初始化抛异常 |

```java
// ClassNotFoundException 示例
try {
    Class.forName("com.mysql.cj.jdbc.Driver"); // 如果 mysql JAR 不在 classpath
} catch (ClassNotFoundException e) {
    // "com.mysql.cj.jdbc.Driver" — 找不到
}

// NoClassDefFoundError 示例 — static 初始化失败
public class Broken {
    static {
        if (true) throw new RuntimeException("init failed!");
    }
}

try {
    new Broken();                    // 第一次: ExceptionInInitializerError
} catch (ExceptionInInitializerError e) { }

try {
    new Broken();                    // 第二次及之后: NoClassDefFoundError
} catch (NoClassDefFoundError e) {
    // Broken 的 <clinit> 已失败，类被标记为 initialization_error
    // 后续所有使用都抛 NoClassDefFoundError
}
```

### 12.2 类冲突 (同名不同版本)

当 classpath 上存在同一类的多个版本时:

```bash
# 诊断: 查看实际加载了哪个 JAR 中的类
java -verbose:class MyApp 2>&1 | grep "com.example.ConflictClass"
# 输出: [Loaded com.example.ConflictClass from file:/path/to/old.jar]

# 诊断: 查看 classpath 中重复的类
jar -tf lib/a.jar | sort > a.txt
jar -tf lib/b.jar | sort > b.txt
comm -12 a.txt b.txt  # 找出重复类
```

**JDK 9+ 模块化解决方案**: 使用 `--module-path` 替代 `-classpath`，模块系统在启动时即检查 split package (同一个包出现在两个模块中) 并报错，将运行时类冲突转化为启动时错误。

### 12.3 LinkageError

`LinkageError` 是类链接阶段失败时抛出的错误，常见子类:

| 错误 | 原因 | 典型场景 |
|------|------|----------|
| `NoClassDefFoundError` | 依赖类不可用 | 见上节 |
| `UnsatisfiedLinkError` | native 库找不到 | JNI 方法的 `.so`/`.dll` 缺失 |
| `IncompatibleClassChangeError` | 类结构不兼容 | 编译时是 class，运行时变成 interface |
| `NoSuchMethodError` | 方法签名不匹配 | 编译依赖的版本与运行时不一致 |
| `NoSuchFieldError` | 字段不存在 | 同上 |
| `AbstractMethodError` | 抽象方法未实现 | 新增了接口方法但实现类未更新 |
| `ClassCircularityError` | 类循环依赖 | A extends B, B extends A |
| `VerifyError` | 字节码验证失败 | 被篡改的 class 文件、不兼容的字节码操作库 |

```java
// LinkageError 经典场景: 不同 ClassLoader 加载同名类导致 ClassCastException
ClassLoader loader1 = new CustomLoader("path1");
ClassLoader loader2 = new CustomLoader("path2");

Object obj = loader1.loadClass("com.example.Foo").getDeclaredConstructor().newInstance();
Class<?> fooClass2 = loader2.loadClass("com.example.Foo");

fooClass2.cast(obj);  // ClassCastException!
// 原因: loader1 的 Foo != loader2 的 Foo (不同 ClassLoader → 不同 Class 对象)
```

### 12.4 排查工具

```bash
java -verbose:class MyApp                             # 查看类加载详情
java -Xlog:class+load=info,class+unload=info MyApp    # JDK 9+ 统一日志
jcmd <pid> VM.classloaders                             # 类加载器层次
jcmd <pid> GC.class_stats                              # 类统计
jmap -dump:format=b,file=heap.hprof <pid>              # 堆转储 (MAT 分析)
java --show-module-resolution MyApp                    # 模块解析过程
```

---

## 13. 类加载器泄漏

### 常见原因

1. **静态集合持有引用**: 核心类的 `static Map` 缓存了自定义 ClassLoader 加载的对象
2. **ThreadLocal 未清理**: 线程池中的线程持有旧 ClassLoader 加载的对象
3. **JDBC 驱动注册**: `DriverManager` 持有驱动类引用
4. **JMX MBean 注册**: MBeanServer 持有 MBean 对象引用
5. **Shutdown Hook**: `Runtime.addShutdownHook()` 注册的线程持有引用

### 检测

```bash
# 查看类加载器数量
jcmd <pid> GC.classloader_stats

# 堆转储分析
jmap -dump:format=b,file=heap.hprof <pid>
# 使用 Eclipse MAT: "Duplicate Classes" 查找被多个 ClassLoader 加载的同名类
# 如果数量持续增长 → 可能存在 ClassLoader 泄漏
```

### 预防

```java
// 1. 清理 ThreadLocal
try {
    threadLocal.set(value);
} finally {
    threadLocal.remove();  // 防止内存泄漏
}

// 2. 取消 JDBC 驱动注册 (在 webapp undeploy 时)
Enumeration<Driver> drivers = DriverManager.getDrivers();
while (drivers.hasMoreElements()) {
    Driver driver = drivers.nextElement();
    if (driver.getClass().getClassLoader() == this.getClassLoader()) {
        DriverManager.deregisterDriver(driver);
    }
}

// 3. 使用弱引用缓存
private static final Map<ClassLoader, Object> CACHE =
    new WeakHashMap<>();  // key 为 ClassLoader，GC 时自动清理

// 4. 清理 JMX MBean
ManagementFactory.getPlatformMBeanServer().unregisterMBean(objectName);
```

---

## 14. 重要 PR 分析

### 启动性能优化

#### JDK-8349400: 消除匿名内部类优化启动

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ 减少 10 个类加载，元空间占用减少 82%

将 `KnownOIDs` 枚举中的匿名内部类转换为构造函数参数：

**核心改进**:
- 消除 10 个匿名内部类
- 减少 Java Agent 场景的启动类加载
- 元空间占用减少 82%

```java
// 优化前：使用匿名内部类覆盖方法
enum KnownOIDs {
    KP_TimeStamping("1.3.6.1.5.5.7.3.8", "timeStamping") {
        @Override
        boolean registerNames() { return false; }
    }
}

// 优化后：使用构造函数参数
enum KnownOIDs {
    KP_TimeStamping("1.3.6.1.5.5.7.3.8", "timeStamping", false)
}
```

→ [详细分析](/by-pr/8349/8349400.md)

### Lambda 生成优化

#### JDK-8341755: Lambda 参数名称生成优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ +15-20% Lambda 生成性能

优化 `InnerClassLambdaMetafactory` 的参数名称构造：

**优化点**:
- 0 参数 Lambda 使用常量（消除数组分配）
- 缓存常见参数名称（1-8 参数）
- 使用 `@Stable` 注解启用 JIT 优化

```java
// 优化前：每次创建新数组
String[] argNames = new String[parameterCount];
for (int i = 0; i < parameterCount; i++) {
    argNames[i] = "arg$" + (i + 1);
}

// 优化后：使用缓存
private static final @Stable String[] ARG_NAME_CACHE;
static {
    var argNameCache = new String[8];
    for (int i = 0; i < 8; i++) {
        argNameCache[i] = "arg$" + (i + 1);
    }
    ARG_NAME_CACHE = argNameCache;
}
```

→ [详细分析](/by-pr/8341/8341755.md)

---

## 15. 类加载最佳实践

### 类加载器使用原则

1. **覆盖 `findClass` 而非 `loadClass`** — 遵循双亲委派，除非明确需要打破 (热部署/隔离)
2. **使用 `WeakHashMap`** — 缓存 key 为 ClassLoader 时使用弱引用，避免泄漏
3. **清理 `ThreadLocal`** — `finally` 中调用 `remove()`，防止线程池场景泄漏
4. **关闭 `URLClassLoader`** — `try-with-resources` 或显式 `close()`，释放 JAR 文件句柄

### CDS / AOT 启动优化

```bash
# JDK 13-23: 使用 Dynamic CDS
java -XX:ArchiveClassesAtExit=app.jsa -cp app.jar Main    # 训练
java -XX:SharedArchiveFile=app.jsa -cp app.jar Main        # 使用

# JDK 24-25: 使用 AOT Class Loading
java -XX:AOTMode=record -XX:AOTConfiguration=app.aotconf -cp app.jar Main
java -XX:AOTMode=create -XX:AOTConfiguration=app.aotconf \
     -XX:AOTCache=app.aot -cp app.jar
java -XX:AOTCache=app.aot -cp app.jar Main

# JDK 26+: 使用 AOT Cache (最简)
java -XX:AOTCacheOutput=app.aot -cp app.jar Main           # 训练
java -XX:AOTCache=app.aot -cp app.jar Main                 # 使用
```

### 模块化类加载

```java
// 推荐：使用模块化反射
Module module = MyClass.class.getModule();

// 检查导出
if (module.isExported("com.example.api")) {
    // 可以访问
}

// 运行时打开 (仅在必要时)
// java --add-opens java.base/java.lang=ALL-UNNAMED MyApp
```

---

## 16. 相关链接

### 本地文档

- [类加载器演进时间线](timeline.md) - 从 JDK 1.0 到 JDK 26 的完整时间线
- [JVM 调优](../jvm/) - 类加载调优
- [内存管理](../memory/) - Metaspace 管理
- [JEP 516: AOT Cache](/jeps/performance/jep-516.md) - AOT Cache 详细分析
- [JDK 26 AOT 改进](/by-version/jdk26/deep-dive/aot-improvements.md) - 源码级分析

### 外部参考

**JEP 文档:**
- [JEP 220: Modular Run-Time Images](https://openjdk.org/jeps/220)
- [JEP 310: Application Class-Data Sharing](https://openjdk.org/jeps/310)
- [JEP 350: Dynamic CDS Archives](https://openjdk.org/jeps/350)
- [JEP 483: Ahead-of-Time Class Loading & Linking](https://openjdk.org/jeps/483)
- [JEP 516: AOT Cache](https://openjdk.org/jeps/516)

**规范与 API:**
- [JVMS Chapter 5: Loading, Linking, and Initializing](https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-5.html)
- [ClassLoader API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/ClassLoader.html)
- [ServiceLoader API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ServiceLoader.html)
