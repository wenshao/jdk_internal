# 类加载器演进时间线

Java 类加载器从 JDK 1.0 到 JDK 26 的完整演进历程。

---
## 目录

1. [时间线概览](#1-时间线概览)
2. [类加载器层次](#2-类加载器层次)
3. [JDK 1.2 - ClassLoader](#3-jdk-12---classloader)
4. [JDK 5 - 线程上下文类加载器](#4-jdk-5---线程上下文类加载器)
5. [JDK 6 - Instrumentation](#5-jdk-6---instrumentation)
6. [JDK 7 - ServiceLoader](#6-jdk-7---serviceloader)
7. [JDK 9+ - 模块类加载](#7-jdk-9---模块类加载)
8. [JDK 17+ - 封装类加载](#8-jdk-17---封装类加载)
9. [类加载问题排查](#9-类加载问题排查)
10. [时间线总结](#10-时间线总结)
11. [相关链接](#11-相关链接)

---


## 1. 时间线概览

```
JDK 1.0 ──── JDK 1.2 ──── JDK 5 ──── JDK 6 ──── JDK 7 ──── JDK 9 ──── JDK 17 ──── JDK 26
 │             │           │           │           │           │           │           │
Bootstrap/    线程上下文   注解        Service     模块化     密封类     动态类
Extension    类加载器     处理器     Loader      类加载      加载
             加载器
```

---

## 2. 类加载器层次

### 双亲委派模型

```
┌─────────────────────────────────────────────────────────┐
│              类加载器层次结构 (JDK 8 及之前)            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Bootstrap ClassLoader                                │
│  ├── $JAVA_HOME/lib/rt.jar (JDK 8)                   │
│  ├── 核心类库                                         │
│  └── C++ 实现                                         │
│       │                                                 │
│       ▼                                                 │
│  Extension ClassLoader                                │
│  ├── $JAVA_HOME/lib/ext/*.jar (JDK 8)                │
│  └── 扩展类库                                         │
│       │                                                 │
│       ▼                                                 │
│  Application ClassLoader                               │
│  ├── Classpath                                        │
│  └── 应用类库                                         │
│       │                                                 │
│       ▼                                                 │
│  Custom ClassLoader                                   │
│  └── 用户自定义                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 平台类加载器 (JDK 9+)

```
┌─────────────────────────────────────────────────────────┐
│             类加载器层次结构 (JDK 9+)                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Bootstrap ClassLoader                                │
│  ├── java.base                                        │
│  └── 核心模块                                         │
│       │                                                 │
│       ▼                                                 │
│  Platform ClassLoader                                 │
│  ├── java.se                                          │
│  ├── java.sql                                         │
│  └── 其他 Java 模块                                    │
│       │                                                 │
│       ▼                                                 │
│  Application ClassLoader                               │
│  ├── Classpath                                        │
│  └── 应用类库                                         │
│       │                                                 │
│       ▼                                                 │
│  Custom ClassLoader                                   │
│  └── 用户自定义                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 3. JDK 1.2 - ClassLoader

### 自定义类加载器

```java
import java.io.*;

// 自定义类加载器
public class MyClassLoader extends ClassLoader {
    private String classPath;

    public MyClassLoader(String classPath) {
        this.classPath = classPath;
    }

    @Override
    protected Class<?> findClass(String name) throws ClassNotFoundException {
        byte[] classData = loadClassData(name);
        return defineClass(name, classData, 0, classData.length);
    }

    private byte[] loadClassData(String name) {
        String fileName = classPath + "/" + name.replace('.', '/') + ".class";
        try (InputStream is = new FileInputStream(fileName);
             ByteArrayOutputStream baos = new ByteArrayOutputStream()) {

            byte[] buffer = new byte[1024];
            int bytesRead;
            while ((bytesRead = is.read(buffer)) != -1) {
                baos.write(buffer, 0, bytesRead);
            }
            return baos.toByteArray();
        } catch (IOException e) {
            throw new RuntimeException("无法加载类: " + name, e);
        }
    }
}
```

### 双亲委派

```java
// 双亲委派模型
// 优点:
// 1. 避免重复加载
// 2. 安全性 (核心类由 Bootstrap 加载)
// 3. 沙箱隔离

public class MyClassLoader extends ClassLoader {
    @Override
    public Class<?> loadClass(String name) throws ClassNotFoundException {
        // 1. 检查是否已加载
        Class<?> c = findLoadedClass(name);
        if (c != null) {
            return c;
        }

        // 2. 委派给父加载器
        try {
            if (getParent() != null) {
                c = getParent().loadClass(name);
            } else {
                c = findBootstrapClassOrNull(name);
            }
        } catch (ClassNotFoundException e) {
            // 父加载器找不到
        }

        // 3. 自己尝试加载
        if (c == null) {
            c = findClass(name);
        }

        return c;
    }
}
```

---

## 4. JDK 5 - 线程上下文类加载器

### ContextClassLoader

```java
// 线程上下文类加载器
// 用于 SPI (Service Provider Interface)

// 获取当前线程的 ContextClassLoader
ClassLoader contextLoader = Thread.currentThread().getContextClassLoader();

// 设置 ContextClassLoader
Thread.currentThread().setContextClassLoader(customClassLoader);

// SPI 示例
ServiceLoader<Driver> drivers = ServiceLoader.load(Driver.class);
for (Driver driver : drivers) {
    System.out.println(driver.getClass().getName());
}
```

---

## 5. JDK 6 - Instrumentation

### ClassFileTransformer

```java
import java.lang.instrument.*;

// 类文件转换
public class MyTransformer implements ClassFileTransformer {
    @Override
    public byte[] transform(ClassLoader loader,
                           String className,
                           Class<?> classBeingRedefined,
                           ProtectionDomain protectionDomain,
                           byte[] classfileBuffer) {
        // 修改字节码
        return transformBytes(classfileBuffer);
    }

    private byte[] transformBytes(byte[] original) {
        // 字节码操作
        return original;
    }
}

// MANIFEST.MF
// Premain-Class: com.example.MyAgent
// Agent-Class: com.example.MyAgent

// Java Agent
public class MyAgent {
    public static void premain(String args, Instrumentation inst) {
        inst.addTransformer(new MyTransformer());
    }
}
```

---

## 6. JDK 7 - ServiceLoader

### SPI 机制

```java
import java.util.*;

// 服务接口
public interface UserService {
    String getUserName(int userId);
}

// 服务实现
public class UserServiceImpl implements UserService {
    @Override
    public String getUserName(int userId) {
        return "User" + userId;
    }
}

// META-INF/services/com.example.UserService
// com.example.UserServiceImpl

// 加载服务
ServiceLoader<UserService> services =
    ServiceLoader.load(UserService.class);

for (UserService service : services) {
    System.out.println(service.getUserName(1));
}
```

---

## 7. JDK 9+ - 模块类加载

### 模块类加载

```java
// 模块类加载器
// 层次结构:
// 1. Bootstrap ClassLoader (java.base)
// 2. Platform ClassLoader (其他 Java 模块)
// 3. Application ClassLoader (应用模块)

// 获取类加载器
Class<?> clazz = String.class;
ClassLoader loader = clazz.getClassLoader();

// JDK 9+ 返回 null (Bootstrap ClassLoader)
// JDK 8 返回 null

// 获取模块
Module module = clazz.getModule();
System.out.println(module.getName());  // java.base
```

---

## 8. JDK 17+ - 封装类加载

### 强封装

```java
// JDK 17+ 强封装
// 默认禁止访问内部 API

// 命令行允许访问
java --add-opens java.base/java.lang=ALL-UNNAMED MyApp

// 运行时反射
Class<?> unsafeClass = Class.forName("sun.misc.Unsafe");
// JDK 17+ 需要显式允许
```

---

## 9. 类加载问题排查

### ClassNotFoundException

```java
// 常见原因:
// 1. 类文件不存在
// 2. 类路径不包含 JAR
// 3. 模块未导出包 (JDK 9+)

// 诊断
// -verbose:class
java -verbose:class MyApp

// 检查类路径
echo $CLASSPATH

// 查找类
jar -tf myapp.jar | grep MyClass
```

### NoClassDefFoundError

```java
// 常见原因:
// 1. 类加载失败
// 2. 依赖类缺失
// 3. 静态初始化失败

// 诊断
java -verbose:class -Xcheck:jni MyApp
```

### ClassCastException

```java
// 常见原因:
// 1. 不同的类加载器加载同名类
// 2. 类型转换不匹配

// 示例
ClassLoader loader1 = new MyClassLoader();
ClassLoader loader2 = new MyClassLoader();

Class<?> clazz1 = loader1.loadClass("com.example.MyClass");
Class<?> clazz2 = loader2.loadClass("com.example.MyClass");

// clazz1 != clazz2 (不同类加载器)
MyClass obj1 = (MyClass) clazz1.newInstance();
MyClass obj2 = (MyClass) clazz2.newInstance();  // ClassCastException!
```

---

## 10. 时间线总结

| 版本 | 特性 | 说明 |
|------|------|------|
| JDK 1.0 | Bootstrap/Extension/Application | 三层类加载 |
| JDK 1.2 | 自定义 ClassLoader | 用户类加载 |
| JDK 5 | ContextClassLoader | SPI 支持 |
| JDK 6 | Instrumentation | Java Agent |
| JDK 6 | ServiceLoader | SPI 标准化 |
| JDK 7 | Parallel ClassLoader | 并行类加载 |
| JDK 9 | Platform ClassLoader | 模块化 |
| JDK 17 | 强封装 | 内部 API 限制 |

---

## 11. 相关链接

- [ClassLoader](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/ClassLoader.html)
- [ServiceLoader](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ServiceLoader.html)
