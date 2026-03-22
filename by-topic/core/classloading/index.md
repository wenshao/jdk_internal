# 类加载

> ClassLoader、双亲委派、模块化类加载演进历程

[← 返回核心平台](../)

---
## 目录

1. [快速概览](#1-快速概览)
2. [核心贡献者](#2-核心贡献者)
3. [类加载过程](#3-类加载过程)
4. [双亲委派模型](#4-双亲委派模型)
5. [内置类加载器](#5-内置类加载器)
6. [线程上下文类加载器 (TCCL)](#6-线程上下文类加载器-tccl)
7. [元空间 (Metaspace)](#7-元空间-metaspace)
8. [模块化类加载 (JDK 9+)](#8-模块化类加载-jdk-9)
9. [自定义类加载器](#9-自定义类加载器)
10. [类加载器泄漏](#10-类加载器泄漏)
11. [CDS (Class Data Sharing)](#11-cds-class-data-sharing)
12. [重要 PR 分析](#12-重要-pr-分析)
13. [类加载最佳实践](#13-类加载最佳实践)
14. [相关链接](#14-相关链接)

---


## 1. 快速概览

```
JDK 1.0 ── JDK 2 ── JDK 6 ── JDK 8 ── JDK 9 ── JDK 17 ── JDK 21 ── JDK 26
   │         │        │        │        │        │        │        │
类加载   双亲    线程上下   元空间   模块化   层层    外部    CDS
机制    委派    类加载器   类加载   类加载   初始化   函数    改进
                (TCCL)   (Metaspace) (JPMS) (Layinit) (FFM)  (AOT)
```

### 核心演进

| 版本 | 特性 | 说明 | JEP |
|------|------|------|-----|
| **JDK 1.0** | ClassLoader | 基础类加载 | - |
| **JDK 2** | 双亲委派 | 安全性保证 | - |
| **JDK 1.2** | 线程上下文类加载器 | JavaEE 支持 | - |
| **JDK 8** | 元空间 | 取代永久代 | - |
| **JDK 9** | 模块化类加载 | JPMS | JEP 220 |
| **JDK 21** | 外部函数 | 不依赖 JNI | JEP 442 |
| **JDK 23** | CDS 改进 | 应用类数据共享 | JEP 467 |

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

## 3. 类加载过程

### 加载阶段

```
┌─────────────────────────────────────────────────────────┐
│                    类加载过程                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 加载 (Loading)                                      │
│     ├── 获取二进制流                                      │
│     ├── 转换为运行时结构                                  │
│     └── 生成 Class 对象                                  │
│                                                         │
│  2. 验证 (Verification)                                 │
│     ├── 文件格式验证                                      │
│     ├── 字节码验证                                        │
│     └── 符号引用验证                                      │
│                                                         │
│  3. 准备 (Preparation)                                  │
│     ├── 分配静态变量内存                                  │
│     └── 设置初始值 (0, null, false)                      │
│                                                         │
│  4. 解析 (Resolution)                                   │
│     ├── 符号引用转直接引用                                │
│     └── 类、接口、字段、方法解析                           │
│                                                         │
│  5. 初始化 (Initialization)                             │
│     ├── 执行 <clinit> 方法                               │
│     └── 静态变量赋值和静态块                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 类加载器层次

```
┌─────────────────────────────────────────────────────────┐
│                  类加载器层次结构                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│                    BootstrapClassLoader                 │
│                    (启动类加载器/C++)                     │
│                         │                               │
│                         ▼                               │
│                   PlatformClassLoader                  │
│                   (平台类加载器/Java)                     │
│                         │                               │
│                         ▼                               │
│                   AppClassLoader                       │
│                   (应用类加载器/Java)                     │
│                         │                               │
│                         ▼                               │
│                   CustomClassLoader                    │
│                   (自定义类加载器)                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 4. 双亲委派模型

### 原理

```java
// 双亲委派伪代码
public Class<?> loadClass(String name) {
    // 1. 检查是否已加载
    Class<?> c = findLoadedClass(name);
    if (c == null) {
        // 2. 委派父加载器
        try {
            if (parent != null) {
                c = parent.loadClass(name);
            } else {
                c = findBootstrapClassOrNull(name);
            }
        } catch (ClassNotFoundException e) {
            // 3. 父加载器无法加载，自己加载
            c = findClass(name);
        }
    }
    return c;
}
```

### 优势

1. **安全性**: 防止替换核心类 (如 java.lang.String)
2. **避免重复加载**: 父加载器已加载的类不会重复加载
3. **层次清晰**: 职责明确

### 打破双亲委派

```java
// 自定义类加载器
public class CustomClassLoader extends ClassLoader {
    @Override
    protected Class<?> loadClass(String name, boolean resolve)
            throws ClassNotFoundException {
        // 1. 检查是否已加载
        Class<?> c = findLoadedClass(name);
        if (c == null) {
            // 2. 自己先尝试加载 (打破双亲委派)
            try {
                c = findClass(name);
            } catch (ClassNotFoundException e) {
                // 3. 无法加载，委派父加载器
                c = super.loadClass(name, resolve);
            }
        }
        return c;
    }

    @Override
    protected Class<?> findClass(String name)
            throws ClassNotFoundException {
        // 自定义类查找逻辑
        byte[] classBytes = loadClassBytes(name);
        return defineClass(name, classBytes, 0, classBytes.length);
    }
}
```

---

## 5. 内置类加载器

### Bootstrap ClassLoader

**实现**: C++ (HotSpot)

**加载路径**:
```bash
# 查看 Bootstrap ClassLoader 路径
java -Xbootclasspath/a:/path -version

# 输出
# 注意: sun.boot.class.path 在 JDK 9+ 已移除
# JDK 8 及之前:
# sun.boot.class.path = /usr/lib/jvm/java-8/jre/lib/rt.jar:...
```

**加载内容**:
- `java.*` 核心类
- `javax.*` 部分核心类
- 启动相关类

### Platform ClassLoader (JDK 9+)

**替代**: Extension ClassLoader (JDK 8)

**加载内容**:
- Java SE 平台 API
- JDK 扩展类

```java
// 获取 Platform ClassLoader
ClassLoader platformLoader = ClassLoader.getPlatformClassLoader();
```

### Application ClassLoader

**别名**: System ClassLoader

**加载内容**:
- 应用类路径 (`-cp` / `-classpath`)
- 用户类

```java
// 获取 Application ClassLoader
ClassLoader appLoader = ClassLoader.getSystemClassLoader();
```

---

## 6. 线程上下文类加载器 (TCCL)

### 用途

**问题**: 双亲委派无法加载应用类

**解决**: 线程上下文类加载器

### 使用场景

```java
// JavaEE SPI (Service Provider Interface)
// 核心库 (Bootstrap ClassLoader) 需要加载应用类

// 1. 设置 TCCL
Thread.currentThread().setContextClassLoader(
    Thread.currentThread().getContextClassLoader());

// 2. 使用 TCCL 加载
Class<?> clazz = Thread.currentThread()
    .getContextClassLoader()
    .loadClass("com.example.Provider");

// 3. JDBC 示例
// DriverManager 在 rt.jar 中 (Bootstrap)
// 需要加载应用提供的 JDBC 驱动
Connection conn = DriverManager.getConnection(url);
```

### 实现原理

```java
// DriverManager 使用 TCCL
public static Driver getService(Iterator<Driver> drivers) {
    ClassLoader cl = Thread.currentThread().getContextClassLoader();
    ServiceLoader<Driver> loadedDrivers = ServiceLoader.load(Driver.class, cl);
    // ...
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
| 位置 | 堆内 | 本地内存 |
| 大小 | 固定 | 动态增长 |
| GC | Full GC 触发 | 自动触发 |
| OOM | java.lang.OutOfMemoryError: PermGen space | java.lang.OutOfMemoryError: Metaspace |

### 配置参数

```bash
# 元空间大小
-XX:MetaspaceSize=256m              # 初始大小
-XX:MaxMetaspaceSize=512m           # 最大大小

# 类数据共享
-XX:SharedClassListFile=classes.lst # 类列表
-XX:SharedArchiveFile=app.jsa       # 共享归档

# 压缩类指针
-XX:CompressedClassSpaceSize=1g     # 压缩类空间大小
```

---

## 8. 模块化类加载 (JDK 9+)

### JEP 220: 模块化系统

**影响**:
- 扩展机制移除
- 类加载器重构
- 封装性增强

### 模块化类加载器

```
┌─────────────────────────────────────────────────────────┐
│              模块化类加载器结构 (JDK 9+)                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Bootstrap ClassLoader                                  │
│  └── java.base                                         │
│                                                         │
│  Platform ClassLoader                                   │
│  ├── java.sql                                          │
│  ├── java.xml                                           │
│  └── ...                                               │
│                                                         │
│  App ClassLoader                                        │
│  └── 应用模块                                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 模块化类加载特性

```java
// 模块化类加载检查
Module module = MyClass.class.getModule();

// 检查模块是否导出包
boolean isExported = module.isExported("com.example.internal");

// 检查模块是否打开包 (反射)
boolean isOpen = module.isOpen("com.example.internal");

// 添加读取边 (运行时)
ModuleLayer.boot().addOpens(
    "java.base",
    "com.example",
    MyClass.class.getModule());
```

---

## 9. 自定义类加载器

### 热部署

```java
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

### 字节码加密

```java
public class DecryptClassLoader extends ClassLoader {
    private final String key;

    @Override
    protected Class<?> findClass(String name)
            throws ClassNotFoundException {
        byte[] encrypted = loadEncryptedClass(name);
        byte[] decrypted = decrypt(encrypted, key);
        return defineClass(name, decrypted, 0, decrypted.length);
    }

    private byte[] decrypt(byte[] data, String key) {
        // 解密逻辑
        return data;
    }
}
```

---

## 10. 类加载器泄漏

### 常见原因

1. **静态集合持有引用**
2. **ThreadLocal 未清理**
3. **未关闭的资源**
4. **JDBC 驱动注册**

### 检测

```bash
# 查看类加载器数量
jcmd <pid> GC.classloader_stats

# 查看类加载器层次
jcmd <pid> VM.classloader_stats

# 堆转储分析
jmap -dump:format=b,file=heap.hprof <pid>
```

### 预防

```java
// 1. 清理 ThreadLocal
try {
    threadLocal.set(value);
} finally {
    threadLocal.remove();  // 防止内存泄漏
}

// 2. 取消 JDBC 驱动注册
try {
    DriverManager.deregisterDriver(driver);
} catch (SQLException e) {
    // 忽略
}

// 3. 使用弱引用
private static final Map<String, Object> CACHE =
    new WeakHashMap<>();
```

---

## 11. CDS (Class Data Sharing)

### 原理

```
┌─────────────────────────────────────────────────────────┐
│                    CDS 工作流程                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 类列表生成                                           │
│     java -Xshare:dump -XX:SharedClassListFile=classes.lst│
│                                                         │
│  2. 归档生成                                             │
│     java -Xshare:dump -XX:SharedArchiveFile=app.jsa     │
│                                                         │
│  3. 使用归档                                             │
│     java -Xshare:on -XX:SharedArchiveFile=app.jsa       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### AppCDS (JDK 10+)

**应用类数据共享**

```bash
# 1. 生成类列表
java -XX:DumpLoadedClassList=classes.lst -cp app.jar Main

# 2. 生成归档
java -Xshare:dump -XX:SharedClassListFile=classes.lst \
    -XX:SharedArchiveFile=app.jsa -cp app.jar

# 3. 使用归档
java -Xshare:on -XX:SharedArchiveFile=app.jsa -cp app.jar Main
```

### AOT (JDK 26+)

**JEP 467: 准备简化 AppCDS**

**改进**:
- 自动类归档
- 无需手动生成类列表
- 更快的启动时间

```bash
# JDK 26+ 自动 AOT
java -XX:AOTMode=create -jar app.jar
java -XX:AOTMode=use -jar app.jar
```

---

## 12. 重要 PR 分析

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

## 13. 类加载最佳实践

### 避免类加载泄漏

```java
// ✅ 推荐：使用弱引用
private static final Map<String, Object> CACHE =
    new WeakHashMap<>();

// ✅ 推荐：清理 ThreadLocal
try {
    threadLocal.set(value);
} finally {
    threadLocal.remove();  // 防止内存泄漏
}

// ❌ 避免：静态集合持有强引用
private static final Map<String, Object> CACHE = new HashMap<>();
// 类加载器无法被回收
```

### 选择合适的类加载器

```java
// ✅ 推荐：使用双亲委派
protected Class<?> loadClass(String name, boolean resolve) {
    // 1. 检查已加载
    Class<?> c = findLoadedClass(name);
    if (c != null) return c;

    // 2. 委派父加载器
    if (parent != null) {
        c = parent.loadClass(name);
    } else {
        c = findBootstrapClassOrNull(name);
    }

    // 3. 自己加载
    if (c == null) {
        c = findClass(name);
    }
    return c;
}

// ❌ 避免：破坏双亲委派（除非必要）
protected Class<?> loadClass(String name, boolean resolve) {
    // 直接自己加载，可能重复加载类
    return findClass(name);
}
```

### 模块化类加载

```java
// ✅ 推荐：使用模块化反射
Module module = MyClass.class.getModule();

// 检查导出
if (module.isExported("com.example.api")) {
    // 可以访问
}

// 添加 opens 边（运行时）
ModuleLayer.boot().addOpens(
    "java.base",
    "com.example",
    MyClass.class.getModule());
```

---

## 14. 相关链接

### 本地文档

- [JVM 调优](../jvm/) - 类加载调优
- [内存管理](../memory/) - Metaspace 管理

### 外部参考

**JEP 文档:**
- [JEP 220](https://openjdk.org/jeps/220)
- [JEP 467](/jeps/tools/jep-467.md)

**技术文档:**
- [Class Loading](https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-5.html)
- [ClassLoader API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/ClassLoader.html)
