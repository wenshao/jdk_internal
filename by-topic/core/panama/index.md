# Project Panama

外部函数接口、外部内存器 - Java 与原生代码的无缝互操作。

[← 返回核心平台](../)

---
## 目录

1. [TL;DR](#1-tldr)
2. [项目概述](#2-项目概述)
3. [Foreign Function Interface](#3-foreign-function-interface)
4. [Foreign Memory Access API](#4-foreign-memory-access-api)
5. [与 JNI 对比](#5-与-jni-对比)
6. [性能对比](#6-性能对比)
7. [时间线](#7-时间线)
8. [核心贡献者](#8-核心贡献者)
9. [实际应用](#9-实际应用)
10. [深入阅读](#10-深入阅读)
11. [安全性](#11-安全性)
12. [相关项目](#12-相关项目)
13. [参考资料](#13-参考资料)

---


## 1. TL;DR

**Project Panama** 是 OpenJDK 的外部互操作项目，提供：
- **Foreign Function Interface (FFI)** - 无需 JNI 调用原生代码
- **Foreign Memory Access API** - 安全高效地访问堆外内存
- **Linker API** - 与 C/C++ 等语言的无缝绑定

**状态**:
- **FFM API**: 正式发布 (JDK 22+, JEP 454)；JDK 24-25 持续性能优化
- **Vector API**: 孵化中 (JDK 16-26+)
- **jextract**: 独立工具，EA 构建跟踪最新 JDK
- **项目周期**: 2014-至今 (10+ 年)

---

## 2. 项目概述

### 解决的问题

| 问题 | 描述 | Panama 解决方案 |
|------|------|----------------|
| **JNI 复杂性** | JNI 需要生成胶水代码 | 自动生成绑定 |
| **JNI 性能开销** | JNI 调用有额外开销 | 接近原生调用 |
| **堆外内存不安全** | Unsafe API 不安全 | 类型安全的 API |
| **跨平台困难** | 每个平台需要编译 | 统一 API |

### 核心组件

```
┌─────────────────────────────────────────────────────────┐
│                   Project Panama                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  FFI API        │  │  Foreign Memory  │              │
│  │  (外部函数接口)  │  │  (外部内存器)    │              │
│  ├─────────────────┤  ├─────────────────┤              │
│  │ • Linker        │  │ • MemorySegment │              │
│  │ • FunctionDesc  │  │ • Arena         │              │
│  │ • SymbolLookup  │  │ • MemoryLayout  │              │
│  └─────────────────┘  └─────────────────┘              │
│                                                          │
│  ┌─────────────────┐                                    │
│  │  Vector API     │  ← SIMD 向量化计算                  │
│  │  (向量计算)      │  → [详细文档](../vector-api/)      │
│  └─────────────────┘                                    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Foreign Function Interface

### 核心概念

| 概念 | 说明 |
|------|------|
| **Downcall** | Java 调用原生函数 (downcallHandle) |
| **Upcall** | 原生代码调用 Java (upcallStub) |
| **Linker** | 连接 Java 与原生代码的桥梁 |
| **SymbolLookup** | 查找原生库中的符号地址 |
| **FunctionDescriptor** | 描述函数签名和参数/返回值类型 |
| **ValueLayout** | 描述原生类型的内存布局 |

### SymbolLookup 方式

| 方式 | 方法 | 说明 | 示例 |
|------|------|------|------|
| **默认查找** | `Linker.defaultLookup()` | 查找系统标准库 | libc, libm |
| **加载器查找** | `SymbolLookup.loaderLookup()` | 查找已加载的 JNI 库 | 通过 System.loadLibrary 加载的库 |
| **库查找** | `SymbolLookup.libraryLookup()` | 动态加载指定库 | 按名称加载共享库 |

```java
// 1. 系统标准库 (libc, libm 等)
SymbolLookup stdlib = Linker.nativeLinker().defaultLookup();

// 2. 已加载的 JNI 库
System.loadLibrary("mylib");
SymbolLookup loadedLib = SymbolLookup.loaderLookup();

// 3. 动态加载库
SymbolLookup customLib = SymbolLookup.libraryLookup("mylib", Arena.ofAuto());
```

### 基本用法 (Downcall)

```java
import java.lang.foreign.*;
import java.lang.invoke.MethodHandle;

// 1. 获取 linker
Linker linker = Linker.nativeLinker();

// 2. 查找 C 函数符号
SymbolLookup stdlib = linker.defaultLookup();

// 3. 创建 downcall handle
MethodHandle strlen = linker.downcallHandle(
    stdlib.find("strlen").get(),                    // 函数地址
    FunctionDescriptor.of(ValueLayout.JAVA_LONG,     // 返回值
                         ValueLayout.ADDRESS)        // 参数 (char*)
);

// 4. 调用 C 函数
try (Arena arena = Arena.ofConfined()) {
    MemorySegment str = arena.allocateFrom("Hello, Panama!");
    long len = (long) strlen.invokeExact(str);
    System.out.println("Length: " + len);
}
```

### 回调 C 代码 (Upcall)

```java
// 1. 定义回调函数接口
Linker linker = Linker.nativeLinker();

// 2. 创建函数描述符
FunctionDescriptor callbackDesc = FunctionDescriptor.of(
    ValueLayout.JAVA_INT,      // 返回值
    ValueLayout.JAVA_INT,      // 参数 1
    ValueLayout.JAVA_INT       // 参数 2
);

// 3. 创建 Java 方法句柄
MethodHandle comparator = MethodHandles.lookup().findStatic(
    MyCallback.class,
    "compare",
    MethodType.methodType(int.class, int.class, int.class)
);

// 4. 创建原生函数指针 (upcall stub)
MemorySegment callbackPtr = linker.upcallStub(
    comparator,           // Java 方法句柄
    callbackDesc,         // 函数签名
    Arena.ofAuto()        // 内存管理
);

// 5. 传递给 C 函数
qsort.sort(array, callbackPtr);
```

### Linker Options

```java
// 链接器选项控制函数调用的行为
Linker.Option[] options = {
    Linker.Option.captureCallState("errno"),  // 捕获 errno
    Linker.Option.firstVariadicArg(1)         // 可变参数起始位置
};

MethodHandle printf = linker.downcallHandle(
    libC.find("printf").get(),
    FunctionDescriptor.of(
        ValueLayout.JAVA_INT,
        ValueLayout.ADDRESS  // format string
    ),
    options  // 应用选项
);
```

### VaList (可变参数) - 已移除

> **注意**: `VaList` 在 JDK 22 正式版发布前已被移除。对于可变参数函数，推荐使用 `Linker.Option.firstVariadicArg(n)` 指定可变参数的起始位置。

以下为历史 API 示例（仅供参考）：

```java
// 处理 C 可变参数函数 (如 vsprintf, vprintf)
import java.lang.foreign.*;

Linker linker = Linker.nativeLinker();

try (Arena arena = Arena.ofConfined()) {
    // 创建 VaList - 正确语法
    VaList vaList = VaList.make(builder -> {
        builder.add(ValueLayout.JAVA_INT, 42);
        builder.add(ValueLayout.JAVA_DOUBLE, 3.14);
        builder.add(ValueLayout.JAVA_INT, 100);
    }, arena);

    // 使用 VaList 调用可变参数函数
    MethodHandle vprintf = linker.downcallHandle(
        libC.find("vprintf").get(),
        FunctionDescriptor.of(
            ValueLayout.JAVA_INT,      // 返回值
            ValueLayout.ADDRESS,       // format string
            ValueLayout.ADDRESS        // va_list
        )
    );

    MemorySegment format = arena.allocateFrom("Values: %d, %f, %d\n");
    vprintf.invokeExact(format, vaList);
}
```

### 限制和约束

| 限制 | 说明 |
|------|------|
| **无自动类型转换** | 必须显式指定类型映射 |
| **手动内存管理** | Arena 生命周期需正确管理 |
| **ABI 依赖** | 某些功能依赖特定平台 ABI |
| **结构体对齐** | 需手动处理结构体对齐问题 |
| **异常处理** | 原生代码异常不会自动转换为 Java 异常 |

### jextract 工具

**jextract** 是 Panama 项目的辅助工具，可自动从 C 头文件生成 Java 绑定代码。

```bash
# 安装 jextract (从源码构建)
git clone https://github.com/openjdk/jextract.git
cd jextract
./build jextract

# 使用 jextract 生成绑定
jextract -t com.example.bindings \
        -I /usr/include \
        /usr/include/stdio.h

# 生成的代码可以直接使用
import com.example.bindings.stdio.*;
```

**注意**: jextract 不属于正式 JDK 发行版，作为独立工具以 [EA 构建](https://jdk.java.net/jextract/) 形式发布。EA 构建跟踪最新 JDK（master 分支始终对应最新版本），支持 C 头文件解析；C++ 支持尚在计划中。

---

## 4. Foreign Memory Access API

### MemorySegment 核心

| 特性 | 说明 |
|------|------|
| **内存区域** | 表示连续的内存区域 (堆内或堆外) |
| **生命周期绑定** | 绑定到 Arena/Scope，自动管理 |
| **线程安全** | Confined Arena 分配的段仅创建线程可访问 |
| **零拷贝** | 与原生代码交互时无需复制 |

### 基本操作

```java
// 分配堆外内存
try (Arena arena = Arena.ofConfined()) {
    // 分配 100 字节
    MemorySegment segment = arena.allocate(100);

    // 写入数据
    segment.set(ValueLayout.JAVA_INT, 0, 42);
    segment.set(ValueLayout.JAVA_LONG, 8, 123456789L);

    // 读取数据
    int value = segment.get(ValueLayout.JAVA_INT, 0);
    System.out.println("Value: " + value);

    // 自动释放内存
}
```

### 内存布局

#### ValueLayout 常量

| Java 类型 | ValueLayout 常量 | 位宽 | 描述 |
|-----------|------------------|------|------|
| boolean | `ValueLayout.JAVA_BOOLEAN` | 8 | 布尔值 |
| byte | `ValueLayout.JAVA_BYTE` | 8 | 字节 |
| char | `ValueLayout.JAVA_CHAR` | 16 | Unicode 字符 |
| short | `ValueLayout.JAVA_SHORT` | 16 | 短整型 |
| int | `ValueLayout.JAVA_INT` | 32 | 整型 |
| long | `ValueLayout.JAVA_LONG` | 64 | 长整型 |
| float | `ValueLayout.JAVA_FLOAT` | 32 | 单精度浮点 |
| double | `ValueLayout.JAVA_DOUBLE` | 64 | 双精度浮点 |
| address | `ValueLayout.ADDRESS` | 平台相关 | 内存地址 (32/64 位) |

#### 结构体布局

```java
// 定义结构体布局
struct Layout {
    int id;
    double value;
    char name[32];
}

// Java 中定义 (注意: structLayout 不会自动插入对齐填充)
MemoryLayout personLayout = MemoryLayout.structLayout(
    ValueLayout.JAVA_INT.withName("id"),
    MemoryLayout.paddingLayout(4),                           // 4 字节填充 (对齐 double)
    ValueLayout.JAVA_DOUBLE.withName("value"),
    MemoryLayout.sequenceLayout(32, ValueLayout.JAVA_BYTE).withName("name")
);

// 使用
try (Arena arena = Arena.ofConfined()) {
    MemorySegment person = arena.allocate(personLayout);
    // 访问字段
    VarHandle idHandle = personLayout.varHandle(MemoryLayout.PathElement.groupElement("id"));
    idHandle.set(person, 0L, 42);
}
```

---

## 5. 与 JNI 对比

### JNI 方式

```java
// 需要 C 胶水代码
public class Native {
    static {
        System.loadLibrary("native");
    }

    // 声明 native 方法
    private native int calculate(int a, int b);

    public int useNative(int a, int b) {
        return calculate(a, b);
    }
}

// C 代码 (需要编译)
#include <jni.h>
JNIEXPORT jint JNICALL
Java_Native_calculate(JNIEnv *env, jobject obj, jint a, jint b) {
    return a + b;
}
```

### Panama 方式

```java
// 无需 C 代码
Linker linker = Linker.nativeLinker();
SymbolLookup lib = SymbolLookup.loaderLookup();

// 直接绑定现有 C 函数
MethodHandle add = linker.downcallHandle(
    lib.find("add").get(),
    FunctionDescriptor.of(ValueLayout.JAVA_INT, ValueLayout.JAVA_INT, ValueLayout.JAVA_INT)
);

// 直接调用
int result = (int) add.invokeExact(10, 20);
```

---

## 6. 性能对比

### 调用开销

| 操作 | JNI | Panama | 提升 |
|------|-----|---------|------|
| **简单函数调用** | 50-100ns | 10-20ns | 5x |
| **内存访问** | 需要复制 | 零拷贝 | 10x |
| **回调** | 复杂 | 简单 | - |

> **JDK 24-25 性能提升**: JDK 24 将 `MemorySegment::fill`、`copy`、`mismatch` 等批量操作重构到专用类，按 long/int/short/byte 单位操作，小段性能显著提升。JDK 25 进一步通过 `Unsafe::setMemory` 内联优化，`MemorySegment::fill` 获得约 2.5 倍加速。

### 基准测试示例

```java
// JNI 方式
for (int i = 0; i < 1_000_000; i++) {
    nativeMethod(i);  // ~50ms
}

// Panama 方式
MethodHandle handle = ...;
for (int i = 0; i < 1_000_000; i++) {
    handle.invokeExact(i);  // ~10ms
}
```

---

## 7. 时间线

| 年份 | 版本 | JEP | 里程碑 |
|------|------|-----|--------|
| **2014** | - | - | Project Panama 启动 |
| **2020.03** | JDK 14 | JEP 370 | Foreign-Memory Access API (第一孵化器) |
| **2020.09** | JDK 15 | JEP 383 | Memory Access 第二孵化器 |
| **2021.03** | JDK 16 | JEP 389 | Linker API 孵化 |
| **2021.03** | JDK 16 | JEP 393 | Foreign-Memory Access API (第三孵化器) |
| **2021.09** | JDK 17 | JEP 412 | Foreign Function & Memory API (第一孵化器，合并) |
| **2022.03** | JDK 18 | JEP 419 | Foreign Function & Memory API (第二孵化器) |
| **2022.09** | JDK 19 | JEP 424 | Foreign Function & Memory API (第一预览) |
| **2023.03** | JDK 20 | JEP 434 | Foreign Function & Memory API (第二预览) |
| **2023.09** | JDK 21 | JEP 442 | Foreign Function & Memory API (第三预览) |
| **2024.03** | JDK 22 | JEP 454 | **Foreign Function & Memory API (正式)** |
| **2024.09** | JDK 23 | - | API 改进和性能优化 |
| **2025.03** | JDK 24 | - | 性能优化: `MemorySegment::fill`/`copy`/`mismatch` 批量操作提速 |
| **2025.09** | JDK 25 | - | `MemorySegment::fill` ~2.5x 提速 (Unsafe::setMemory 内联优化) |
| **2026.03** | JDK 26 | - | 持续优化，Vector API 深度集成 |

→ [完整时间线](timeline.md)

---

## 8. 核心贡献者

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| [Maurizio Cimadamore](/by-contributor/profiles/maurizio-cimadamore.md) | Oracle | 项目领导人，FFI 设计 |
| [Jorn Vernee](/by-contributor/profiles/jorn-vernee.md) | Oracle | Linker 实现 |
| [Vladimir Ivanov](/by-contributor/profiles/vladimir-ivanov.md) | Oracle | JIT 集成 |

---

## 9. 实际应用

### 调用系统函数

```java
// 获取当前时间 (gettimeofday)
Linker linker = Linker.nativeLinker();
SymbolLookup libc = linker.defaultLookup();

MethodHandle gettimeofday = linker.downcallHandle(
    libc.find("gettimeofday").get(),
    FunctionDescriptor.of(ValueLayout.JAVA_INT,
        ValueLayout.ADDRESS,
        ValueLayout.ADDRESS)
);

try (Arena arena = Arena.ofConfined()) {
    MemorySegment timeval = arena.allocate(
        MemoryLayout.structLayout(
            ValueLayout.JAVA_LONG,
            ValueLayout.JAVA_LONG
        )
    );

    int rc = (int) gettimeofday.invokeExact(timeval, MemorySegment.NULL);
    // 读取 timeval
}
```

### 调用 OpenGL

```java
// 直接调用 OpenGL
MethodHandle glClearColor = linker.downcallHandle(
    libGL.find("glClearColor").get(),
    FunctionDescriptor.ofVoid(
        ValueLayout.JAVA_FLOAT,  // red
        ValueLayout.JAVA_FLOAT,  // green
        ValueLayout.JAVA_FLOAT,  // blue
        ValueLayout.JAVA_FLOAT   // alpha
    )
);

// 调用 OpenGL 函数
glClearColor.invokeExact(1.0f, 0.0f, 0.0f, 1.0f);
```

### 常见使用模式

#### 字符串传递

```java
// Java 字符串 → C char*
try (Arena arena = Arena.ofConfined()) {
    MemorySegment cStr = arena.allocateFrom("Hello");
    myFunc.invokeExact(cStr);
}

// C char* → Java 字符串
MemorySegment cResult = ...;
String javaStr = cResult.getString(0);
```

#### 数组传递

```java
// Java 数组 → C 数组
try (Arena arena = Arena.ofConfined()) {
    int[] javaArray = {1, 2, 3, 4, 5};
    MemorySegment cArray = arena.allocateFrom(
        ValueLayout.JAVA_INT,
        javaArray
    );
    processArray(cArray, javaArray.length);
}
```

#### 结构体操作

```java
// 定义并操作结构体
MemoryLayout pointLayout = MemoryLayout.structLayout(
    ValueLayout.JAVA_DOUBLE.withName("x"),
    ValueLayout.JAVA_DOUBLE.withName("y")
);

try (Arena arena = Arena.ofConfined()) {
    MemorySegment point = arena.allocate(pointLayout);

    // 使用 VarHandle 访问字段
    VarHandle xHandle = pointLayout.varHandle(
        MemoryLayout.PathElement.groupElement("x")
    );
    xHandle.set(point, 0L, 3.14);
}
```

---

## 10. 深入阅读

### Arena 专题

→ [Arena 详解](arena.md) - 内存生命周期管理器

**内容**:
- 四种 Arena 类型的详细对比
- SegmentedAllocator 分配策略
- 生命周期管理与作用域
- 与 ByteBuffer/Unsafe/JNI 的对比
- 性能分析与最佳实践
- 常见陷阱与高级主题

### Arena vs MemorySession

| 概念 | 说明 | 版本 |
|------|------|------|
| **MemorySession** | 早期 API 中的内存会话概念 | JDK 19 |
| **Arena** | 简化后的内存管理 API | JDK 20+ (推荐) |

**Arena 是 MemorySession 的简化版本**：

```java
// 旧 API (MemorySession) - JDK 19
try (MemorySession session = MemorySession.openConfined()) {
    MemorySegment segment = session.allocate(100);
}

// 新 API (Arena) - JDK 20+ (推荐)
try (Arena arena = Arena.ofConfined()) {
    MemorySegment segment = arena.allocate(100);
}
```

### Arena 类型与生命周期

| Arena | 生命周期 | 使用场景 |
|-------|----------|----------|
| **Arena.ofConfined()** | 手动关闭，单线程 | 高性能，单线程访问 |
| **Arena.ofShared()** | 手动关闭，多线程 | 需要多线程访问 |
| **Arena.ofAuto()** | GC 自动释放 | 简单场景 |
| **Arena.global()** | 无界 (不可关闭) | 全局常量、永久存活的段 |

```java
// Confined Arena - 单线程
try (Arena arena = Arena.ofConfined()) {
    MemorySegment segment = arena.allocate(1000);
    // 使用 segment，离开 try 块自动释放
}

// Shared Arena - 多线程
try (Arena arena = Arena.ofShared()) {
    MemorySegment segment = arena.allocate(1000);
    // 可以多线程访问 segment
}
```

---

## 11. 安全性

### 类型安全

```java
// 类型安全的内存访问
MemorySegment segment = ...;

// ❌ 编译错误 - 类型不匹配
// segment.set(ValueLayout.JAVA_INT, 0, "string");

// ✅ 正确
segment.set(ValueLayout.JAVA_INT, 0, 42);
```

### 边界检查

```java
MemorySegment segment = arena.allocate(100);

// ❌ 抛出 IndexOutOfBoundsException
// segment.get(ValueLayout.JAVA_INT, 100);

// ✅ 正确访问
segment.get(ValueLayout.JAVA_INT, 96);  // 最后一个 int
```

---

## 12. 相关项目

### Vector API (SIMD 向量化)
Vector API 是 Panama 项目的子项目，提供可移植的 SIMD 向量化计算能力。JDK 26 开始与 FFM API 深度集成。

→ [Vector API 详细文档](../vector-api/)

---

## 13. 参考资料

### 官方资源
- [Project Panama Official Page](https://openjdk.org/projects/panama/)
- [jextract EA Builds](https://jdk.java.net/jextract/)
- [JEP 454](/jeps/ffi/jep-454.md) - JDK 22 正式版
- [JEP 442: Foreign Function & Memory API (Third Preview)](https://openjdk.org/jeps/442) - JDK 21 预览
- [JEP 434: Foreign Function & Memory API (Second Preview)](https://openjdk.org/jeps/434) - JDK 20 预览
- [JEP 424: Foreign Function & Memory API (First Preview)](https://openjdk.org/jeps/424) - JDK 19 预览
- [JEP 419: Foreign Function & Memory API (Second Incubator)](https://openjdk.org/jeps/419) - JDK 18 孵化器
- [JEP 412: Foreign Function & Memory API (First Incubator)](https://openjdk.org/jeps/412) - JDK 17 孵化器
- [JEP 393: Foreign-Memory Access API (Third Incubator)](https://openjdk.org/jeps/393) - JDK 16 孵化器
- [JEP 389](/jeps/ffi/jep-389.md) - JDK 16 孵化器
- [JEP 383: Foreign-Memory Access API (Second Incubator)](https://openjdk.org/jeps/383) - JDK 15 孵化器
- [JEP 370](/jeps/ffi/jep-370.md) - JDK 14 孵化器

→ [完整时间线](timeline.md)
