# Project Panama

外部函数接口、外部内存器 - Java 与原生代码的无缝互操作。

[← 返回核心平台](../)

---

## TL;DR

**Project Panama** 是 OpenJDK 的外部互操作项目，提供：
- **Foreign Function Interface (FFI)** - 无需 JNI 调用原生代码
- **Foreign Memory Access API** - 安全高效地访问堆外内存
- **Linker API** - 与 C/C++ 等语言的无缝绑定

**状态**: 持续交付中 (2014-至今)，核心 API 已正式发布 (JDK 22)

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
│  │ • FunctionDescriptor    │ • Arena         │              │
│  │ • Symbol Lookup │  │ • MemoryLayout  │              │
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

### 基本用法

```java
import java.lang.foreign.*;
import java.lang.invoke.MethodHandle;

// 获取 linker
Linker linker = Linker.nativeLinker();

// 查找 C 函数
SymbolLookup stdlib = linker.defaultLookup();

// 获取 strlen 函数
MethodHandle strlen = linker.downcallHandle(
    stdlib.find("strlen").get(),
    FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
);

// 调用 C 函数
try (Arena arena = Arena.ofConfined()) {
    MemorySegment str = arena.allocateFrom("Hello, Panama!");
    long len = (long) strlen.invokeExact(str);
    System.out.println("Length: " + len);
}
```

### 回调 C 代码

```java
// 定义回调函数接口
Linker linker = Linker.nativeLinker();

// 创建函数描述符
FunctionDescriptor callbackDesc = FunctionDescriptor.of(
    ValueLayout.JAVA_INT,
    ValueLayout.JAVA_INT,
    ValueLayout.JAVA_INT
);

// 创建 Java 方法句柄
MethodHandle comparator = MethodHandles.lookup().findStatic(
    MyCallback.class,
    "compare",
    MethodType.methodType(int.class, int.class, int.class)
);

// 创建原生函数指针
MemorySegment callbackPtr = linker.upcallStub(
    comparator,
    callbackDesc,
    Arena.ofAuto()
);

// 传递给 C 函数
qsort.sort(array, callbackPtr);
```

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

| 年份 | 版本 | 里程碑 |
|------|------|--------|
| **2014** | - | Project Panama 启动 |
| **2019** | JDK 14 | Foreign Memory Access (孵化) |
| **2020** | JDK 15 | Foreign Linker API (孵化) |
| **2021** | JDK 16 | Foreign Memory Access (第二孵化器) |
| **2022** | JDK 17 | Foreign Function Interface (孵化) |
| **2023** | JDK 19 | Foreign Function & Memory API (预览) |
| **2023** | JDK 20 | Foreign Function & Memory API (第二次预览) |
| **2024** | JDK 22 | **Foreign Function & Memory API (正式)** |

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

- [Project Panama Official Page](https://openjdk.org/projects/panama/)
- [JEP 454: Foreign Function & Memory API](https://openjdk.org/jeps/454)
- [JEP 389: Foreign Linker API (Incubator)](https://openjdk.org/jeps/389)
- [JEP 393: Foreign Memory Access API](https://openjdk.org/jeps/393)

→ [时间线](timeline.md)
