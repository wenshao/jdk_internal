# Project Panama

外部函数接口、外部内存 API — Java 与原生代码的无缝互操作。

[← 返回核心平台](../)

---
## 目录

1. [TL;DR](#1-tldr)
2. [Project Panama 概述](#2-project-panama-概述)
3. [Foreign Function & Memory API 演进](#3-foreign-function--memory-api-演进)
4. [核心 API 深入](#4-核心-api-深入)
5. [调用原生函数详解](#5-调用原生函数详解)
6. [内存管理深入](#6-内存管理深入)
7. [vs JNI 对比](#7-vs-jni-对比)
8. [jextract 工具](#8-jextract-工具)
9. [性能特性](#9-性能特性)
10. [实际应用案例](#10-实际应用案例)
11. [JEP 472: 限制 JNI](#11-jep-472-限制-jni)
12. [核心贡献者](#12-核心贡献者)
13. [参考资料](#13-参考资料)

---


## 1. TL;DR

**Project Panama** 是 OpenJDK 的外部互操作项目，目标是彻底替代 JNI，提供：
- **Foreign Function Interface (FFI)** — 无需编写 C 胶水代码即可调用原生函数
- **Foreign Memory Access API** — 安全高效地访问堆外内存，取代 `sun.misc.Unsafe`
- **Linker API** — 基于平台 ABI 的 Java ↔ C/C++ 无缝绑定
- **jextract** — 从 C 头文件自动生成 Java 绑定代码

**状态** (截至 JDK 26):
- **FFM API**: 正式发布 (JDK 22+, JEP 454)；JDK 24-26 持续性能优化
- **Vector API**: 孵化中 (JDK 16-26+, JEP 529 第十一孵化器)
- **jextract**: 独立工具，EA 构建跟踪最新 JDK
- **JEP 472**: 逐步限制 JNI 使用 (JDK 24)
- **项目周期**: 2014-至今 (10+ 年，6 次孵化 + 3 次预览 → 正式)

---

## 2. Project Panama 概述

### 为什么需要 Panama

Java 自 1.1 起就通过 **JNI (Java Native Interface)** 与原生代码交互，但 JNI 存在根本性问题：

| 痛点 | 说明 |
|------|------|
| **开发复杂** | 需要编写 .h/.c 胶水代码 + javah/javac 双重编译 |
| **性能开销** | JNI 调用需要 marshalling/unmarshalling 数据 |
| **安全隐患** | 原生代码可以绕过 JVM 安全检查 |
| **内存不安全** | 通过 Unsafe API 访问堆外内存无边界检查 |
| **平台耦合** | 每个平台需要单独编译原生库 |
| **调试困难** | Java + C 混合调试极其复杂 |

**Panama 的目标**：提供纯 Java 的外部互操作方案——不需要写一行 C 代码，不需要 `javah`，不需要交叉编译。

### 核心组件

| 组件 | 职责 | 核心类/方法 |
|------|------|------------|
| **FFI (外部函数接口)** | Java 调用原生函数 | Linker, FunctionDescriptor, SymbolLookup, downcallHandle(), upcallStub() |
| **Foreign Memory (外部内存)** | 安全的堆外内存访问 | MemorySegment, Arena, MemoryLayout, SegmentAllocator, VarHandle |
| **jextract (独立工具)** | 从 C 头文件自动生成 Java 绑定 | CLI 工具，非 JDK 组件 |
| **Vector API (SIMD)** | 可移植的向量化计算 | → [详见 vector-api/](../vector-api/) |

### 设计哲学

Panama 的 API 设计遵循三条核心原则：

| 原则 | 说明 | 体现 |
|------|------|------|
| **安全优先** | 默认内存安全，边界检查、生命周期管理 | Arena 自动释放，MemorySegment 越界抛异常 |
| **零抽象开销** | 性能与手写 JNI 持平或更优 | JIT 内联 downcall handle，零拷贝内存访问 |
| **纯 Java** | 不需要任何非 Java 代码 | 无需 .h/.c 文件，无需 javah 工具 |

---

## 3. Foreign Function & Memory API 演进

Panama 的 API 经历了 **6 次孵化 + 3 次预览** 才最终定型。这不是优柔寡断——每一轮迭代都解决了社区反馈的真实问题。

### 演进总览

```
JDK 14 ──→ JDK 15 ──→ JDK 16 ──→ JDK 17 ──→ JDK 18 ──→ JDK 19 ──→ JDK 20 ──→ JDK 21 ──→ JDK 22
JEP 370   JEP 383   JEP 393   JEP 412   JEP 419   JEP 424   JEP 434   JEP 442   JEP 454
孵化1     孵化2     孵化3     孵化4     孵化5     预览1     预览2     预览3     ★ 正式
(内存)    (内存)    (内存)    (合并FFI) (合并)    (API重构) (精简)    (微调)    (GA)
```

### JEP 370 (JDK 14) — 第一孵化器: Memory Access

引入 `jdk.incubator.foreign` 模块。核心概念: `MemorySegment`、`MemoryAddress`、`MemoryLayout`。API 需要手动 `close()`，缺少 FFI 集成。

### JEP 383 (JDK 15) — 第二孵化器

增加 `MemoryAccess` 静态方法简化读写，支持 mapped segments (文件映射)、`spliterator()` 并行处理。

### JEP 393 + 389 (JDK 16) — 第三孵化器 + Linker API

引入 `ResourceScope` 替代手动 close；同版本 JEP 389 引入 Foreign Linker API，但内存和 FFI 分属不同 JEP。

```java
// JDK 16: ResourceScope
try (ResourceScope scope = ResourceScope.newConfinedScope()) {
    MemorySegment segment = MemorySegment.allocateNative(100, scope);
}
```

### JEP 412 (JDK 17) — 合并! FFM API 第一孵化器

**里程碑**: Memory API + Linker API 合并为统一的 FFM API。引入 `CLinker` 类和 `VaList`。

```java
// JDK 17: CLinker (后更名为 Linker)
CLinker linker = CLinker.systemCLinker();
MethodHandle strlen = linker.downcallHandle(
    linker.lookup("strlen").get(),
    FunctionDescriptor.of(CLinker.C_LONG, CLinker.C_POINTER)
);
```

### JEP 419 (JDK 18) — 第二孵化器

`CLinker` → `Linker`；`CLinker.C_INT` → `ValueLayout.JAVA_INT` (Java 侧命名)。

### JEP 424 (JDK 19) — 第一预览

`ResourceScope` → `MemorySession`；`MemorySegment` 与 `MemoryAddress` 合并；`Linker.nativeLinker()` 替代 `systemLinker()`。

### JEP 434 (JDK 20) — 第二预览: Arena 诞生

`MemorySession` 拆分为 `Arena` + `SegmentScope` (单一职责)。

```java
// JDK 20+: Arena — 最终形态
try (Arena arena = Arena.ofConfined()) {
    MemorySegment segment = arena.allocate(100);
}
```

### JEP 442 (JDK 21) — 第三预览

`SegmentScope` 合并回 `Arena`；移除 `VaList` (改用 `Linker.Option.firstVariadicArg()`)；增加 `MemorySegment::reinterpret`。

### JEP 454 (JDK 22) — 正式发布 (GA)

API 进入 `java.lang.foreign` 包。`--enable-native-access` 安全模型确定。

### 为什么需要 9 轮迭代

| 挑战 | 迭代过程 | 最终方案 |
|------|----------|----------|
| **内存生命周期** | close → ResourceScope → MemorySession → Arena | Arena (简洁的 try-with-resources) |
| **地址 vs 段** | MemoryAddress + MemorySegment 分离 → 合并 | MemorySegment 统一表示 |
| **Linker 命名** | CLinker → Linker.systemLinker → Linker.nativeLinker | `Linker.nativeLinker()` |
| **类型命名** | C_INT → JAVA_INT | Java 侧命名 (ValueLayout.JAVA_INT) |
| **可变参数** | VaList 类 → 移除 | `Linker.Option.firstVariadicArg()` |
| **模块归属** | jdk.incubator.foreign → java.lang.foreign | 标准 `java.base` 模块 |

---

## 4. 核心 API 深入

### 4.1 Arena — 内存生命周期管理

Arena 是 FFM API 的内存管理核心，负责分配和释放堆外内存。

#### 四种 Arena 类型

| Arena | 生命周期 | 线程 | 典型场景 |
|-------|----------|------|----------|
| `Arena.ofConfined()` | try-with-resources 确定性释放 | 仅创建线程 | 函数内临时使用 (最常用) |
| `Arena.ofShared()` | try-with-resources 确定性释放 | 任意线程 | 多线程共享段 |
| `Arena.ofAuto()` | GC 自动管理 | 任意线程 | 生命周期不确定、upcall stub |
| `Arena.global()` | 永不释放 | 任意线程 | 全局常量、永久符号 |

```java
try (Arena arena = Arena.ofConfined()) {      // 最常用
    MemorySegment seg = arena.allocate(1024);  // try 块结束即释放
}
Arena.ofAuto().allocate(1024);                 // GC 管理，无需 close
Arena.global().allocate(64);                   // JVM 生命周期，不可 close
```

→ [Arena 详解](arena.md)

### 4.2 MemorySegment — 内存段

MemorySegment 表示一个连续的内存区域，是 FFM API 中数据访问的核心抽象。

#### 三种内存段类型

```java
// 1. Native segment — 堆外内存 (最常用)
try (Arena arena = Arena.ofConfined()) {
    MemorySegment native_ = arena.allocate(256);
    // 底层调用 malloc() 分配，arena 关闭时 free()
}

// 2. Heap segment — 堆上内存 (包装 Java 数组)
int[] array = {1, 2, 3, 4, 5};
MemorySegment heap = MemorySegment.ofArray(array);
// 零拷贝: 直接引用 Java 数组的内存
// 生命周期由 GC 管理
// 注意: 不能传递给原生函数 (地址不稳定，GC 可能移动)

// 3. Mapped segment — 文件映射内存
try (Arena arena = Arena.ofConfined();
     FileChannel fc = FileChannel.open(Path.of("data.bin"),
         StandardOpenOption.READ, StandardOpenOption.WRITE)) {
    MemorySegment mapped = fc.map(
        FileChannel.MapMode.READ_WRITE,
        0, fc.size(),
        arena
    );
    // 直接读写文件内容，OS 负责页面调度
    int header = mapped.get(ValueLayout.JAVA_INT, 0);
    mapped.set(ValueLayout.JAVA_INT, 0, header + 1);
    mapped.force(); // 强制刷盘 (类似 MappedByteBuffer.force)
}
```

#### 常用操作

```java
try (Arena arena = Arena.ofConfined()) {
    MemorySegment seg = arena.allocate(100);
    seg.set(ValueLayout.JAVA_INT, 0, 42);              // 写入
    int val = seg.get(ValueLayout.JAVA_INT, 0);         // 读取

    MemorySegment str = arena.allocateFrom("Hello!");    // Java String → C char*
    String back = str.getString(0);                      // C char* → Java String

    int[] data = {10, 20, 30};
    MemorySegment arr = arena.allocateFrom(ValueLayout.JAVA_INT, data);  // 数组
    int[] readBack = arr.toArray(ValueLayout.JAVA_INT);

    MemorySegment sub = seg.asSlice(8, 16);             // 切片
    seg.fill((byte) 0);                                  // 清零
    MemorySegment.copy(seg, 0, arena.allocate(100), 0, 100); // 拷贝
}
```

### 4.3 MemoryLayout — 内存布局

MemoryLayout 描述内存中数据的结构，类似 C 中的 `struct`/`union` 定义。

#### ValueLayout 基本类型

| ValueLayout 常量 | C 对应类型 | 大小 (字节) | Java 类型 |
|------------------|-----------|------------|-----------|
| `JAVA_BOOLEAN` | `_Bool` | 1 | boolean |
| `JAVA_BYTE` | `char` | 1 | byte |
| `JAVA_CHAR` | `wchar_t` (Windows) | 2 | char |
| `JAVA_SHORT` | `short` | 2 | short |
| `JAVA_INT` | `int` | 4 | int |
| `JAVA_LONG` | `long long` | 8 | long |
| `JAVA_FLOAT` | `float` | 4 | float |
| `JAVA_DOUBLE` | `double` | 8 | double |
| `ADDRESS` | `void*` | 4/8 (平台相关) | MemorySegment |

#### 结构体布局 (structLayout)

```java
// C 结构体:
// struct Point {
//     double x;
//     double y;
// };
MemoryLayout POINT = MemoryLayout.structLayout(
    ValueLayout.JAVA_DOUBLE.withName("x"),
    ValueLayout.JAVA_DOUBLE.withName("y")
);
// 大小: 16 字节, 自然对齐

// C 结构体 (需要手动填充):
// struct Record {
//     int id;        // 4 bytes
//                    // 4 bytes padding (为了对齐 double)
//     double value;  // 8 bytes
//     char name[32]; // 32 bytes
// };
MemoryLayout RECORD = MemoryLayout.structLayout(
    ValueLayout.JAVA_INT.withName("id"),
    MemoryLayout.paddingLayout(4),  // 手动插入 4 字节填充
    ValueLayout.JAVA_DOUBLE.withName("value"),
    MemoryLayout.sequenceLayout(32, ValueLayout.JAVA_BYTE).withName("name")
);
// 注意: structLayout 不会自动插入对齐填充！必须手动添加 paddingLayout
```

#### 序列布局 (sequenceLayout)

```java
MemoryLayout INT_ARRAY = MemoryLayout.sequenceLayout(100, ValueLayout.JAVA_INT);  // int[100] = 400B
MemoryLayout POINT_ARRAY = MemoryLayout.sequenceLayout(50, POINT);                // Point[50] = 800B
```

#### 联合布局 (unionLayout) 和嵌套访问

```java
// union Value { int i; float f; double d; };  → 大小 = 最大成员 (8 bytes)
MemoryLayout VALUE_UNION = MemoryLayout.unionLayout(
    ValueLayout.JAVA_INT.withName("i"), ValueLayout.JAVA_FLOAT.withName("f"),
    ValueLayout.JAVA_DOUBLE.withName("d"));

// 嵌套字段访问: line.end.y
MemoryLayout LINE = MemoryLayout.structLayout(POINT.withName("start"), POINT.withName("end"));
VarHandle endY = LINE.varHandle(
    MemoryLayout.PathElement.groupElement("end"), MemoryLayout.PathElement.groupElement("y"));

// 数组元素访问: points[i].x
VarHandle pointX = MemoryLayout.sequenceLayout(50, POINT).varHandle(
    MemoryLayout.PathElement.sequenceElement(), MemoryLayout.PathElement.groupElement("x"));
```

### 4.4 Linker — 外部函数调用

Linker 是 Java 与原生代码之间的桥梁，基于平台 ABI 实现函数调用。

```java
// 获取平台原生链接器 (Linux: System V ABI, Windows: MSVC ABI)
Linker linker = Linker.nativeLinker();
```

#### downcallHandle — Java 调用原生函数

```java
Linker linker = Linker.nativeLinker();
MethodHandle abs = linker.downcallHandle(
    linker.defaultLookup().find("abs").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_INT, ValueLayout.JAVA_INT));

int result = (int) abs.invokeExact(-42);  // result == 42
```

#### upcallStub — 原生代码回调 Java

```java
// Java 方法 → C 函数指针
MethodHandle comparator = MethodHandles.lookup().findStatic(
    MyClass.class, "compare",
    MethodType.methodType(int.class, MemorySegment.class, MemorySegment.class));

try (Arena arena = Arena.ofConfined()) {
    MemorySegment callbackPtr = linker.upcallStub(
        comparator,
        FunctionDescriptor.of(ValueLayout.JAVA_INT, ValueLayout.ADDRESS, ValueLayout.ADDRESS),
        arena);
    // callbackPtr 可传给 qsort 等需要函数指针的 C 函数
}
```

#### Linker.Option — 链接器选项

```java
// 捕获 errno
MethodHandle open = linker.downcallHandle(stdlib.find("open").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_INT, ValueLayout.ADDRESS, ValueLayout.JAVA_INT),
    Linker.Option.captureCallState("errno"));

// 可变参数: 每种参数组合需要不同的 MethodHandle
MethodHandle printf = linker.downcallHandle(stdlib.find("printf").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_INT,
        ValueLayout.ADDRESS, ValueLayout.JAVA_INT, ValueLayout.JAVA_DOUBLE),
    Linker.Option.firstVariadicArg(1)); // 第 1 个参数起是可变参数
```

### 4.5 SymbolLookup — 符号查找

```java
Linker linker = Linker.nativeLinker();

// 方式 1: 系统标准库 (libc, libm)
SymbolLookup defaultLookup = linker.defaultLookup();

// 方式 2: 从路径加载共享库
SymbolLookup customLib = SymbolLookup.libraryLookup(Path.of("/usr/lib/libcurl.so"), Arena.ofAuto());

// 方式 3: 通过名称加载 (系统搜索路径)
SymbolLookup namedLib = SymbolLookup.libraryLookup("curl", Arena.ofAuto());

// 方式 4: 已加载的 JNI 库 (用于 JNI → Panama 迁移)
System.loadLibrary("mylegacylib");
SymbolLookup loaderLookup = SymbolLookup.loaderLookup();

// 组合查找
SymbolLookup combined = name -> customLib.find(name).or(() -> defaultLookup.find(name));
```

### 4.6 FunctionDescriptor — 函数签名

```java
// of(returnLayout, argLayouts...) — 有返回值
FunctionDescriptor.of(ValueLayout.JAVA_INT, ValueLayout.JAVA_INT, ValueLayout.JAVA_INT);  // int(int,int)
FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS);  // size_t(char*)

// ofVoid(argLayouts...) — 无返回值
FunctionDescriptor.ofVoid(ValueLayout.JAVA_INT);                    // void(int)
FunctionDescriptor.ofVoid(ValueLayout.ADDRESS, ValueLayout.JAVA_INT); // void(Point*,int)

// 结构体按值: 返回类型可以是 GroupLayout
FunctionDescriptor.of(POINT);                                        // Point(void)
```

---

## 5. 调用原生函数详解

### 5.1 调用 C 标准库函数

#### strlen

```java
import java.lang.foreign.*;
import java.lang.invoke.*;

Linker linker = Linker.nativeLinker();

// C: size_t strlen(const char *s);
MethodHandle strlen = linker.downcallHandle(
    linker.defaultLookup().find("strlen").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS));

try (Arena arena = Arena.ofConfined()) {
    long len = (long) strlen.invokeExact(arena.allocateFrom("Hello, Panama!"));
    // len == 14
}
```

#### printf (可变参数)

```java
// 每种参数组合需要单独的 handle
MethodHandle printfInt = linker.downcallHandle(
    linker.defaultLookup().find("printf").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_INT, ValueLayout.ADDRESS, ValueLayout.JAVA_INT),
    Linker.Option.firstVariadicArg(1));

MethodHandle printfStrDbl = linker.downcallHandle(
    linker.defaultLookup().find("printf").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_INT,
        ValueLayout.ADDRESS, ValueLayout.ADDRESS, ValueLayout.JAVA_DOUBLE),
    Linker.Option.firstVariadicArg(1));

try (Arena arena = Arena.ofConfined()) {
    printfInt.invokeExact(arena.allocateFrom("Value: %d\n"), 42);
    printfStrDbl.invokeExact(arena.allocateFrom("Name: %s, Score: %.2f\n"),
        arena.allocateFrom("Alice"), 95.5);
}
```

### 5.2 调用自定义 .so/.dll

```c
// math_ext.c — 编译: gcc -shared -fPIC -o libmath_ext.so math_ext.c -lm
double fast_distance(double x1, double y1, double x2, double y2) {
    double dx = x2 - x1, dy = y2 - y1;
    return sqrt(dx * dx + dy * dy);
}
```

```java
SymbolLookup mathExt = SymbolLookup.libraryLookup(Path.of("./libmath_ext.so"), Arena.ofAuto());

MethodHandle fastDistance = Linker.nativeLinker().downcallHandle(
    mathExt.find("fast_distance").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_DOUBLE,
        ValueLayout.JAVA_DOUBLE, ValueLayout.JAVA_DOUBLE,
        ValueLayout.JAVA_DOUBLE, ValueLayout.JAVA_DOUBLE));

double dist = (double) fastDistance.invokeExact(0.0, 0.0, 3.0, 4.0);
// dist == 5.0
```

运行: `java --enable-native-access=ALL-UNNAMED CustomLibExample.java`

### 5.3 回调 (Upcall): Java 函数作为 C 回调

经典场景: 用 Panama 调用 C 标准库的 `qsort`。

```java
// Java 比较函数 — 将作为 C 函数指针传给 qsort
static int compareInts(MemorySegment a, MemorySegment b) {
    return Integer.compare(
        a.reinterpret(4).get(ValueLayout.JAVA_INT, 0),
        b.reinterpret(4).get(ValueLayout.JAVA_INT, 0));
}

// void qsort(void *base, size_t nmemb, size_t size, int(*compar)(const void*, const void*))
MethodHandle qsort = linker.downcallHandle(
    linker.defaultLookup().find("qsort").orElseThrow(),
    FunctionDescriptor.ofVoid(ValueLayout.ADDRESS, ValueLayout.JAVA_LONG,
        ValueLayout.JAVA_LONG, ValueLayout.ADDRESS));

MethodHandle comparator = MethodHandles.lookup().findStatic(QsortExample.class,
    "compareInts", MethodType.methodType(int.class, MemorySegment.class, MemorySegment.class));

try (Arena arena = Arena.ofConfined()) {
    MemorySegment comparatorPtr = linker.upcallStub(comparator,
        FunctionDescriptor.of(ValueLayout.JAVA_INT, ValueLayout.ADDRESS, ValueLayout.ADDRESS),
        arena);

    int[] data = {5, 3, 8, 1, 9, 2, 7};
    MemorySegment array = arena.allocateFrom(ValueLayout.JAVA_INT, data);
    qsort.invokeExact(array, (long) data.length, ValueLayout.JAVA_INT.byteSize(), comparatorPtr);

    int[] sorted = array.toArray(ValueLayout.JAVA_INT);
    // [1, 2, 3, 5, 7, 8, 9]
}
```

### 5.4 结构体传递

#### 结构体按值传递 (by value)

```java
// C: double point_distance(struct Point a, struct Point b);
MethodHandle pointDistance = linker.downcallHandle(
    lib.find("point_distance").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_DOUBLE, POINT, POINT)); // 参数类型=布局

try (Arena arena = Arena.ofConfined()) {
    MemorySegment a = arena.allocate(POINT);
    a.set(ValueLayout.JAVA_DOUBLE, 0, 0.0);  a.set(ValueLayout.JAVA_DOUBLE, 8, 0.0);
    MemorySegment b = arena.allocate(POINT);
    b.set(ValueLayout.JAVA_DOUBLE, 0, 3.0);  b.set(ValueLayout.JAVA_DOUBLE, 8, 4.0);
    double dist = (double) pointDistance.invokeExact(a, b); // 5.0
}
```

#### 结构体按指针传递 (by pointer)

```java
// C: void point_translate(struct Point* p, double dx, double dy);
MethodHandle pointTranslate = linker.downcallHandle(
    lib.find("point_translate").orElseThrow(),
    FunctionDescriptor.ofVoid(ValueLayout.ADDRESS, ValueLayout.JAVA_DOUBLE, ValueLayout.JAVA_DOUBLE));
    // 注意: 指针用 ADDRESS，按值用结构体 Layout

try (Arena arena = Arena.ofConfined()) {
    MemorySegment point = arena.allocate(POINT);
    point.set(ValueLayout.JAVA_DOUBLE, 0, 1.0);
    pointTranslate.invokeExact(point, 10.0, 20.0); // point.x → 11.0
}
```

#### 结构体按值返回

```java
// C: struct Point make_point(double x, double y);
MethodHandle makePoint = linker.downcallHandle(lib.find("make_point").orElseThrow(),
    FunctionDescriptor.of(POINT, ValueLayout.JAVA_DOUBLE, ValueLayout.JAVA_DOUBLE));

try (Arena arena = Arena.ofConfined()) {
    // 注意: 返回结构体时，MethodHandle 自动在前面插入 SegmentAllocator 参数
    MemorySegment point = (MemorySegment) makePoint.invokeExact(arena, 3.0, 4.0);
}
```

---

## 6. 内存管理深入

### 6.1 SegmentAllocator

`Arena` 实现了 `SegmentAllocator` 接口。对于高性能场景，可使用 slicing allocator:

```java
try (Arena arena = Arena.ofConfined()) {
    MemorySegment buffer = arena.allocate(1024 * 1024); // 预分配 1MB
    SegmentAllocator slicing = SegmentAllocator.slicingAllocator(buffer);

    // 从 buffer 中切片 — 只移动指针，无 malloc 调用
    MemorySegment a = slicing.allocate(100);  // buffer[0..100)
    MemorySegment b = slicing.allocate(200);  // buffer[100..300)
}
```

### 6.2 内存对齐

```java
// ValueLayout 自带对齐要求: JAVA_INT=4, JAVA_DOUBLE=8, ADDRESS=8 (64-bit)
// Arena.allocate(byteSize, byteAlignment) 可指定对齐
MemorySegment seg = arena.allocate(100, 16); // 16 字节对齐 (适合 SIMD)

// 结构体中手动处理: struct { char c; int i; double d; } → 需要 padding
MemoryLayout MIXED = MemoryLayout.structLayout(
    ValueLayout.JAVA_BYTE.withName("c"),
    MemoryLayout.paddingLayout(3),           // 手动填充 3 字节对齐 int
    ValueLayout.JAVA_INT.withName("i"),
    ValueLayout.JAVA_DOUBLE.withName("d"));  // byteSize() == 16
```

### 6.3 零拷贝映射: FileChannel → MemorySegment

```java
try (Arena arena = Arena.ofConfined();
     FileChannel fc = FileChannel.open(Path.of("huge_data.bin"),
         StandardOpenOption.READ, StandardOpenOption.WRITE)) {
    // 映射整个文件 — 无大小限制 (突破 ByteBuffer 的 2GB 限制)
    MemorySegment mapped = fc.map(FileChannel.MapMode.READ_WRITE, 0, fc.size(), arena);

    // 直接读写，OS 负责页面调度，适合 GB 级文件
    mapped.set(ValueLayout.JAVA_INT, 0, 42);
    mapped.force(); // 强制刷盘
}
```

### 6.4 与 ByteBuffer 的对比和互操作

| 特性 | ByteBuffer | MemorySegment |
|------|-----------|---------------|
| **最大大小** | 2GB (`int` 索引) | 理论无限 (`long` 索引) |
| **生命周期** | GC 管理 (可能延迟回收) | Arena 精确控制 |
| **结构化访问** | 无 | MemoryLayout + VarHandle |
| **文件映射** | `MappedByteBuffer` (2GB 限制) | `FileChannel.map()` (无限制) |

```java
// 互操作: 共享底层内存
MemorySegment seg = MemorySegment.ofBuffer(ByteBuffer.allocateDirect(1024));
ByteBuffer bb = arena.allocate(1024).asByteBuffer(); // 仅限 <= 2GB
```

---

## 7. vs JNI 对比

### 详细对比表

| 维度 | JNI | Panama FFM API |
|------|-----|----------------|
| **语言** | 需要编写 C/C++ 胶水代码 | 纯 Java |
| **编译** | javah + gcc/clang 交叉编译 | javac 即可 |
| **类型映射** | 手动 jint/jstring/jobject 转换 | ValueLayout 自动映射 |
| **内存安全** | 无边界检查，可能悬挂指针 | MemorySegment 越界抛异常 |
| **生命周期** | 手动 NewGlobalRef/DeleteGlobalRef | Arena try-with-resources |
| **线程模型** | 需要 AttachCurrentThread | Confined/Shared Arena |
| **性能** | ~50-100ns 调用开销 | ~10-20ns (JIT 可内联) |
| **调试** | Java + C 混合调试 | 纯 Java 调试 |
| **错误处理** | C 崩溃导致 JVM 崩溃 | 边界检查 + IllegalStateException |
| **学习曲线** | 高 (需懂 C + JNI 规范) | 中 (纯 Java API) |
| **工具链** | javah, gcc, make | javac (+ 可选 jextract) |

### 代码量对比: 调用 strlen

**JNI** — 需要 Java 声明 + C 实现 + javah + gcc 编译 (3 步骤，2 种语言):

```c
// strlen_jni.c — 必须手写 C 胶水代码
#include <jni.h>
#include <string.h>
JNIEXPORT jlong JNICALL Java_NativeStrlen_strlen
  (JNIEnv *env, jclass cls, jstring s) {
    const char *str = (*env)->GetStringUTFChars(env, s, NULL);
    jlong len = (jlong) strlen(str);
    (*env)->ReleaseStringUTFChars(env, s, str);
    return len;
}
```

**Panama** — 纯 Java，5 行:

```java
Linker linker = Linker.nativeLinker();
MethodHandle strlen = linker.downcallHandle(
    linker.defaultLookup().find("strlen").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
);
try (Arena arena = Arena.ofConfined()) {
    long len = (long) strlen.invokeExact(arena.allocateFrom("hello"));
}
```

### 安全性优势

```java
// 防止 use-after-free (JNI 中会导致 segfault 或 silent corruption)
MemorySegment seg;
try (Arena arena = Arena.ofConfined()) { seg = arena.allocate(100); }
// seg.get(ValueLayout.JAVA_INT, 0);  // → IllegalStateException!

// 防止越界访问
MemorySegment seg2 = Arena.ofConfined().allocate(100);
// seg2.get(ValueLayout.JAVA_INT, 100);  // → IndexOutOfBoundsException!
```

---

## 8. jextract 工具

**jextract** 是 Panama 生态的配套工具，可从 C 头文件自动生成 Java 绑定代码。它不属于 JDK 正式发行版，以独立 [EA 构建](https://jdk.java.net/jextract/) 形式发布。

### 基本使用

```bash
# 安装 (从 EA 构建下载或源码编译)
git clone https://github.com/openjdk/jextract.git
cd jextract && ./gradlew

# 从 C 头文件生成 Java 绑定
jextract --source \
    --target-package com.example.stdio \
    --output src \
    /usr/include/stdio.h

# 生成指定函数的绑定 (过滤)
jextract --source \
    --target-package com.example.math \
    --output src \
    --include-function sqrt \
    --include-function pow \
    --include-function sin \
    /usr/include/math.h
```

### 生成代码示例

jextract 自动生成类型安全的 Java 包装:

```java
// 自动生成 — 无需手写
public class stdio_h {
    private static final MethodHandle printf$MH = Linker.nativeLinker()
        .downcallHandle(/* 自动填充地址和签名 */);

    public static int printf(MemorySegment format) {
        try { return (int) printf$MH.invokeExact(format); }
        catch (Throwable t) { throw new AssertionError(t); }
    }
}
```

### 复杂库绑定

```bash
# 选择性绑定 libcurl
jextract --source --target-package com.example.curl --output src \
    -I /usr/include \
    --include-function curl_easy_init --include-function curl_easy_perform \
    /usr/include/curl/curl.h
```

### 当前限制

| 限制 | 说明 |
|------|------|
| **仅 C 语言** | 不支持 C++ 头文件 (C++ 支持在计划中) |
| **平台特定** | 生成的代码可能包含平台特定的布局 |
| **宏处理** | 只处理简单的 `#define` 常量，不支持复杂宏函数 |
| **EA 状态** | 非正式发布，API 可能变化 |

---

## 9. 性能特性

### 调用开销对比

| 操作 | JNI | Panama FFM | 说明 |
|------|-----|-----------|------|
| **空函数调用** | ~50-80ns | ~10-15ns | Panama ~5x 快 |
| **带 int 参数** | ~60-90ns | ~12-18ns | 无 marshalling 开销 |
| **字符串传递** | ~200-500ns | ~50-100ns | JNI 需要 GetStringUTFChars + Release |
| **结构体按值** | 不支持 (需要指针) | ~20-30ns | Panama 支持按值传递 |
| **回调 (upcall)** | ~150-300ns | ~30-50ns | 无 AttachCurrentThread 开销 |

### Panama 性能优势来源

| 原因 | 说明 |
|------|------|
| **JIT 内联** | downcallHandle 可被 JIT 内联优化；JNI native 方法对 JIT 不透明 |
| **零拷贝** | MemorySegment 直接操作原生内存；JNI 需要 GetIntArrayElements → 拷贝 → Release |
| **无状态切换** | Panama 不需要切换 JNI 环境；JNI 每次调用需要保存/恢复 JVM 状态 |
| **批量优化 (JDK 24-25)** | fill/copy/mismatch 按 long/int 单位操作；JDK 25 fill ~2.5x 加速 |

### JMH Benchmark 示例

```java
@BenchmarkMode(Mode.AverageTime) @OutputTimeUnit(TimeUnit.NANOSECONDS)
public class PanamaVsJniBenchmark {
    private static final MethodHandle STRLEN = Linker.nativeLinker().downcallHandle(
        Linker.nativeLinker().defaultLookup().find("strlen").orElseThrow(),
        FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS));

    @Benchmark public long panamaStrlen() throws Throwable {
        return (long) STRLEN.invokeExact(testString);
    }
    @Benchmark public long jniStrlen() { return jniStrlen("Hello!"); }
}
// 典型结果 (JDK 22, x86-64):
// panamaStrlen  avgt  14.2 ± 0.3  ns/op
// jniStrlen     avgt  72.5 ± 1.2  ns/op   (~5x 慢)
```

### 内存操作性能 (JDK 24-25 优化)

JDK 24 将 `MemorySegment::fill`、`copy`、`mismatch` 等批量操作重构到专用类 `SegmentBulkOperations`，按 long/int/short/byte 单位操作，小段性能显著提升。JDK 25 进一步通过 `Unsafe::setMemory` 内联优化，`fill` 获得约 2.5 倍加速。

---

## 10. 实际应用案例

### 10.1 调用 libcurl — HTTP 请求

```java
Linker linker = Linker.nativeLinker();
SymbolLookup curl = SymbolLookup.libraryLookup("curl", Arena.ofAuto());

MethodHandle curl_easy_init = linker.downcallHandle(
    curl.find("curl_easy_init").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.ADDRESS));

MethodHandle curl_easy_setopt_str = linker.downcallHandle(
    curl.find("curl_easy_setopt").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_INT,
        ValueLayout.ADDRESS, ValueLayout.JAVA_INT, ValueLayout.ADDRESS),
    Linker.Option.firstVariadicArg(2));

MethodHandle curl_easy_perform = linker.downcallHandle(
    curl.find("curl_easy_perform").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_INT, ValueLayout.ADDRESS));

MethodHandle curl_easy_cleanup = linker.downcallHandle(
    curl.find("curl_easy_cleanup").orElseThrow(),
    FunctionDescriptor.ofVoid(ValueLayout.ADDRESS));

try (Arena arena = Arena.ofConfined()) {
    MemorySegment handle = ((MemorySegment) curl_easy_init.invokeExact())
        .reinterpret(Long.MAX_VALUE);
    MemorySegment url = arena.allocateFrom("https://httpbin.org/get");
    curl_easy_setopt_str.invokeExact(handle, /*CURLOPT_URL*/ 10002, url);
    int result = (int) curl_easy_perform.invokeExact(handle);
    curl_easy_cleanup.invokeExact(handle);
}
```

### 10.2 调用 SQLite — 数据库操作

```java
SymbolLookup sqlite = SymbolLookup.libraryLookup("sqlite3", Arena.ofAuto());
Linker linker = Linker.nativeLinker();

MethodHandle sqlite3_open = linker.downcallHandle(
    sqlite.find("sqlite3_open").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_INT, ValueLayout.ADDRESS, ValueLayout.ADDRESS));

MethodHandle sqlite3_exec = linker.downcallHandle(
    sqlite.find("sqlite3_exec").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_INT,
        ValueLayout.ADDRESS, ValueLayout.ADDRESS, ValueLayout.ADDRESS,
        ValueLayout.ADDRESS, ValueLayout.ADDRESS));

MethodHandle sqlite3_close = linker.downcallHandle(
    sqlite.find("sqlite3_close").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_INT, ValueLayout.ADDRESS));

try (Arena arena = Arena.ofConfined()) {
    MemorySegment ppDb = arena.allocate(ValueLayout.ADDRESS);
    int rc = (int) sqlite3_open.invokeExact(arena.allocateFrom(":memory:"), ppDb);

    MemorySegment db = ppDb.get(ValueLayout.ADDRESS, 0).reinterpret(Long.MAX_VALUE);

    MemorySegment sql = arena.allocateFrom(
        "CREATE TABLE test(id INT, name TEXT); INSERT INTO test VALUES(1,'Alice');");
    sqlite3_exec.invokeExact(db, sql,
        MemorySegment.NULL, MemorySegment.NULL, MemorySegment.NULL);

    sqlite3_close.invokeExact(db);
}
```

### 10.3 调用 OpenSSL — 计算 SHA-256

```java
SymbolLookup ssl = SymbolLookup.libraryLookup("crypto", Arena.ofAuto());

// unsigned char *SHA256(const unsigned char *d, size_t n, unsigned char *md);
MethodHandle sha256 = Linker.nativeLinker().downcallHandle(
    ssl.find("SHA256").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.ADDRESS,
        ValueLayout.ADDRESS, ValueLayout.JAVA_LONG, ValueLayout.ADDRESS));

try (Arena arena = Arena.ofConfined()) {
    byte[] input = "Hello, Panama!".getBytes();
    MemorySegment inputSeg = arena.allocateFrom(ValueLayout.JAVA_BYTE, input);
    MemorySegment outputSeg = arena.allocate(32); // SHA-256 = 32 bytes

    sha256.invokeExact(inputSeg, (long) input.length, outputSeg);

    byte[] hash = outputSeg.toArray(ValueLayout.JAVA_BYTE);
    StringBuilder hex = new StringBuilder();
    for (byte b : hash) hex.append(String.format("%02x", b));
    System.out.println("SHA-256: " + hex);
}
```

### 10.4 调用系统函数 — gettimeofday

```java
Linker linker = Linker.nativeLinker();

MemoryLayout TIMEVAL = MemoryLayout.structLayout(
    ValueLayout.JAVA_LONG.withName("tv_sec"),
    ValueLayout.JAVA_LONG.withName("tv_usec"));

MethodHandle gettimeofday = linker.downcallHandle(
    linker.defaultLookup().find("gettimeofday").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_INT, ValueLayout.ADDRESS, ValueLayout.ADDRESS));

VarHandle tvSec = TIMEVAL.varHandle(MemoryLayout.PathElement.groupElement("tv_sec"));
VarHandle tvUsec = TIMEVAL.varHandle(MemoryLayout.PathElement.groupElement("tv_usec"));

try (Arena arena = Arena.ofConfined()) {
    MemorySegment tv = arena.allocate(TIMEVAL);
    gettimeofday.invokeExact(tv, MemorySegment.NULL);
    System.out.printf("Time: %d.%06d%n",
        (long) tvSec.get(tv, 0L), (long) tvUsec.get(tv, 0L));
}
```

---

## 11. JEP 472: 限制 JNI

[JEP 472: Prepare to Restrict the Use of JNI](/jeps/ffi/jep-472.md) (JDK 24) 标志着从 JNI 向 Panama FFM 迁移的官方路线图。

### 核心变化

| 变化 | 说明 |
|------|------|
| **统一限制** | FFM 和 JNI 共用 `--enable-native-access` 选项 |
| **默认警告** | 未授权的原生访问产生运行时警告 |
| **逐步收紧** | 路线图: JDK 24 warning → 未来 error → 最终禁止未授权 JNI |
| **模块声明** | `module-info.java` 中需要显式声明原生访问需求 |

### 如何迁移

```java
// JNI: 需要 native 声明 + C 实现
public class Legacy {
    static { System.loadLibrary("mylib"); }
    private static native int compute(int x);
}

// Panama: 纯 Java
private static final MethodHandle COMPUTE = Linker.nativeLinker().downcallHandle(
    SymbolLookup.libraryLookup("mylib", Arena.ofAuto()).find("compute").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_INT, ValueLayout.JAVA_INT));
// 调用: (int) COMPUTE.invokeExact(42);
```

### 过渡期兼容

```bash
java --enable-native-access=ALL-UNNAMED MyApp      # 非模块化
java --enable-native-access=com.myapp MyApp         # 模块化
```

---

## 12. 核心贡献者

| 贡献者 | 组织 | 主要贡献 |
|--------|------|----------|
| [Maurizio Cimadamore](/by-contributor/profiles/maurizio-cimadamore.md) | Oracle | Panama 项目领导人，FFM API 总设计师。从 JEP 370 到 JEP 454，主导了所有 9 轮迭代的 API 设计。同时也是 Java 泛型推断引擎的作者。 |
| [Jorn Vernee](/by-contributor/profiles/jorn-vernee.md) | Oracle | Linker 实现的核心开发者。负责 downcall/upcall 的底层 ABI 适配、调用约定处理、以及与 JIT 的集成优化。 |
| [Vladimir Ivanov](/by-contributor/profiles/vladimir-ivanov.md) | Oracle | JIT 编译器集成。确保 downcall handle 能被 JIT 内联优化，使 Panama 调用性能接近手写 JNI。 |

Panama 开发在 [panama-dev](https://mail.openjdk.org/pipermail/panama-dev/) 邮件列表进行，关键设计决策 (MemoryAddress/MemorySegment 合并、VaList 移除、Arena 命名) 均由社区反馈驱动。

---

## 13. 参考资料

### 官方资源
- [Project Panama Official Page](https://openjdk.org/projects/panama/)
- [jextract EA Builds](https://jdk.java.net/jextract/)
- [panama-dev 邮件列表](https://mail.openjdk.org/pipermail/panama-dev/)

### JEP 列表 (按时间正序)
- [JEP 370: Foreign-Memory Access API (Incubator)](/jeps/ffi/jep-370.md) — JDK 14
- [JEP 383: Foreign-Memory Access API (Second Incubator)](https://openjdk.org/jeps/383) — JDK 15
- [JEP 389: Foreign Linker API (Incubator)](/jeps/ffi/jep-389.md) — JDK 16
- [JEP 393: Foreign-Memory Access API (Third Incubator)](https://openjdk.org/jeps/393) — JDK 16
- [JEP 412: Foreign Function & Memory API (First Incubator)](https://openjdk.org/jeps/412) — JDK 17
- [JEP 419: Foreign Function & Memory API (Second Incubator)](https://openjdk.org/jeps/419) — JDK 18
- [JEP 424: Foreign Function & Memory API (First Preview)](https://openjdk.org/jeps/424) — JDK 19
- [JEP 434: Foreign Function & Memory API (Second Preview)](https://openjdk.org/jeps/434) — JDK 20
- [JEP 442: Foreign Function & Memory API (Third Preview)](https://openjdk.org/jeps/442) — JDK 21
- [JEP 454: Foreign Function & Memory API](/jeps/ffi/jep-454.md) — JDK 22 (GA)
- [JEP 472: Prepare to Restrict the Use of JNI](/jeps/ffi/jep-472.md) — JDK 24

### 子文档
- → [Arena 详解](arena.md) — 内存生命周期管理深入
- → [完整时间线](timeline.md) — Panama 项目演进历史

### 相关项目
- [Vector API (SIMD 向量化)](../vector-api/) — Panama 子项目，JDK 26 第十一孵化器 (JEP 529)
