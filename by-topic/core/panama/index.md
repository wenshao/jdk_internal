# Project Panama

外部函数接口、外部内存器 - Java 与原生代码的无缝互操作。

[← 返回核心平台](../)

---

## TL;DR

**Project Panama** 是 OpenJDK 的外部互操作项目，提供：
- **Foreign Function Interface (FFI)** - 无需 JNI 调用原生代码
- **Foreign Memory Access API** - 安全高效地访问堆外内存
- **Linker API** - 与 C/C++ 等语言的无缝绑定

**状态**:
- **FFM API**: 正式发布 (JDK 22+, JEP 454)
- **Vector API**: 孵化中 (JDK 16-26+)
- **项目周期**: 2014-至今 (10+ 年)

---

## 项目概述

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

## Foreign Function Interface

### 核心概念

| 概念 | 说明 |
|------|------|
| **Downcall** | Java 调用原生函数 (downcallHandle) |
| **Upcall** | 原生代码调用 Java (upcallStub) |
| **Linker** | 连接 Java 与原生代码的桥梁 |
| **SymbolLookup** | 查找原生库中的符号地址 |
| **FunctionDescriptor** | 描述函数签名和参数/返回值类型 |

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

### VaList (可变参数)

```java
// 处理 C 可变参数函数 (如 printf, scanf)
Linker linker = Linker.nativeLinker();

// 创建 VaList
VaList.Builder builder = VaList.make(
    linker,
    ValueLayout.JAVA_INT,
    ValueLayout.JAVA_DOUBLE
);
builder.add(VaList.ofInt(42));
builder.add(VaList.ofDouble(3.14));
VaList vaList = builder.build();

// 传递给原生函数
MethodHandle myFunc = linker.downcallHandle(
    lib.find("variadic_func").get(),
    FunctionDescriptor.of(
        ValueLayout.JAVA_INT,
        ValueLayout.JAVA_INT,
        ValueLayout.ADDRESS  // VaList as pointer
    )
);
```

### 限制和约束

| 限制 | 说明 |
|------|------|
| **无自动类型转换** | 必须显式指定类型映射 |
| **手动内存管理** | Arena 生命周期需正确管理 |
| **ABI 依赖** | 某些功能依赖特定平台 ABI |
| **结构体对齐** | 需手动处理结构体对齐问题 |
| **异常处理** | 原生代码异常不会自动转换为 Java 异常 |

---

## Foreign Memory Access API

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

```java
// 定义结构体布局
struct Layout {
    int id;
    double value;
    char name[32];
}

// Java 中定义
MemoryLayout personLayout = MemoryLayout.structLayout(
    ValueLayout.JAVA_INT.withName("id"),
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

## 与 JNI 对比

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

## 性能对比

### 调用开销

| 操作 | JNI | Panama | 提升 |
|------|-----|---------|------|
| **简单函数调用** | 50-100ns | 10-20ns | 5x |
| **内存访问** | 需要复制 | 零拷贝 | 10x |
| **回调** | 复杂 | 简单 | - |

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

## 时间线

| 年份 | 版本 | JEP | 里程碑 |
|------|------|-----|--------|
| **2014** | - | - | Project Panama 启动 |
| **2020** | JDK 14 | JEP 370 | Foreign-Memory Access API (第一孵化器) |
| **2020** | JDK 15 | JEP 383, JEP 389 | Memory Access 第二孵化器 + Linker API 孵化 |
| **2021** | JDK 16 | JEP 393 | Foreign-Memory Access API (第三孵化器) |
| **2021** | JDK 17 | JEP 412 | Foreign Function & Memory API (第一孵化器，合并) |
| **2022** | JDK 18 | JEP 419 | Foreign Function & Memory API (第二孵化器) |
| **2022** | JDK 19 | JEP 424 | Foreign Function & Memory API (第一预览) |
| **2023** | JDK 20 | JEP 434 | Foreign Function & Memory API (第二预览) |
| **2023** | JDK 21 | JEP 442 | Foreign Function & Memory API (第三预览) |
| **2024** | JDK 22 | JEP 454 | **Foreign Function & Memory API (正式)** |
| **2024** | JDK 23 | - | API 改进和性能优化 |
| **2025** | JDK 24 | - | 持续优化 |

→ [完整时间线](timeline.md)

---

## 核心贡献者

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| [Maurizio Cimadamore](/by-contributor/profiles/maurizio-cimadamore.md) | Oracle | 项目领导人，FFI 设计 |
| [Jorn Vernee](/by-contributor/profiles/jorn-vernee.md) | Oracle | Linker 实现 |
| [Vladimir Ivanov](/by-contributor/profiles/vladimir-ivanov.md) | Oracle | JIT 集成 |

---

## 实际应用

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
    FunctionDescriptor.of(
        ValueLayout.JAVA_VOID,
        ValueLayout.JAVA_FLOAT,  // red
        ValueLayout.JAVA_FLOAT,  // green
        ValueLayout.JAVA_FLOAT,  // blue
        ValueLayout.JAVA_FLOAT   // alpha
    )
);

// 调用 OpenGL 函数
glClearColor.invokeExact(1.0f, 0.0f, 0.0f, 1.0f);
```

---

## 深入阅读

### Arena 专题

→ [Arena 详解](arena.md) - 内存生命周期管理器

**内容**:
- 三种 Arena 类型的详细对比
- SegmentedAllocator 分配策略
- 生命周期管理与作用域
- 与 ByteBuffer/Unsafe/JNI 的对比
- 性能分析与最佳实践
- 常见陷阱与高级主题

### Arena vs MemorySession

| 概念 | 说明 | 版本 |
|------|------|------|
| **MemorySession** | 早期 API 中的内存会话概念 | JDK 14-19 |
| **Arena** | 简化后的内存管理 API | JDK 19+ |

**Arena 是 MemorySession 的简化版本**，提供了更直观的 API：

```java
// 旧 API (MemorySession) - JDK 14-19
try (MemorySession session = MemorySession.openConfined()) {
    MemorySegment segment = session.allocate(100);
}

// 新 API (Arena) - JDK 19+ (推荐)
try (Arena arena = Arena.ofConfined()) {
    MemorySegment segment = arena.allocate(100);
}
```

---

## Arena 详解

### Arena 类型

| Arena | 生命周期 | 使用场景 |
|-------|----------|----------|
| **Arena.ofConfined()** | 单线程 | 高性能，单线程访问 |
| **Arena.ofShared()** | 多线程 | 需要多线程访问 |
| **Arena.ofAuto()** | 自动释放 | 简单场景 |

### 生命周期管理

```java
// Confined Arena - 单线程
try (Arena arena = Arena.ofConfined()) {
    MemorySegment segment = arena.allocate(1000);
    // 使用 segment
    // 离开 try 块自动释放
}

// Shared Arena - 多线程
try (Arena arena = Arena.ofShared()) {
    MemorySegment segment = arena.allocate(1000);
    // 可以多线程访问 segment
}
```

---

## 安全性

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

## 相关项目

### Vector API (SIMD 向量化)
Vector API 是 Panama 项目的子项目，提供可移植的 SIMD 向量化计算能力。JDK 26 开始与 FFM API 深度集成。

→ [Vector API 详细文档](../vector-api/)

---

## 参考资料

### 官方资源
- [Project Panama Official Page](https://openjdk.org/projects/panama/)
- [JEP 454: Foreign Function & Memory API (Final)](https://openjdk.org/jeps/454) - JDK 22 正式版
- [JEP 442: Foreign Function & Memory API (Third Preview)](https://openjdk.org/jeps/442) - JDK 21 预览
- [JEP 434: Foreign Function & Memory API (Second Preview)](https://openjdk.org/jeps/434) - JDK 20 预览
- [JEP 424: Foreign Function & Memory API (First Preview)](https://openjdk.org/jeps/424) - JDK 19 预览
- [JEP 419: Foreign Function & Memory API (Second Incubator)](https://openjdk.org/jeps/419) - JDK 18 孵化器
- [JEP 412: Foreign Function & Memory API (First Incubator)](https://openjdk.org/jeps/412) - JDK 17 孵化器
- [JEP 393: Foreign-Memory Access API (Third Incubator)](https://openjdk.org/jeps/393) - JDK 16 孵化器
- [JEP 389: Foreign Linker API (Incubator)](https://openjdk.org/jeps/389) - JDK 15 孵化器
- [JEP 383: Foreign-Memory Access API (Second Incubator)](https://openjdk.org/jeps/383) - JDK 15 孵化器
- [JEP 370: Foreign-Memory Access API (First Incubator)](https://openjdk.org/jeps/370) - JDK 14 孵化器

→ [完整时间线](timeline.md)
