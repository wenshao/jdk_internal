---

# JEP 454: Foreign Function & Memory API 实现分析

> JEP 454 | Maurizio Cimadamore (Oracle) | JDK 22 (正式) | Panama 项目核心

---

## 目录

1. [概述](#1-概述)
2. [为什么替代 JNI](#2-为什么替代-jni)
3. [架构设计](#3-架构设计)
4. [MemorySegment 与 MemoryLayout](#4-memorysegment-与-memorylayout)
5. [Downcall 与 Upcall](#5-downcall-与-upcall)
6. [性能对比](#6-性能对比)
7. [安全性保障](#7-安全性保障)
8. [代码示例](#8-代码示例)

---

## 1. 概述

Foreign Function & Memory API (FFM API) 是 Panama 项目的核心成果，提供了一种类型安全、高性能的方式来调用原生代码（C/Fortran 等）和管理堆外内存，替代了复杂的 JNI 机制。

| 属性 | 值 |
|------|-----|
| **JEP** | [JEP 454](https://openjdk.org/jeps/454) |
| **作者** | Maurizio Cimadamore |
| **目标版本** | JDK 22 (正式) |
| **演进** | JEP 412 (孵化, JDK 17) → JEP 419 (孵化2, JDK 18) → JEP 424 (Preview, JDK 19) → JEP 442 (Preview2, JDK 20-21) → JEP 454 (Final, JDK 22) |

---

## 2. 为什么替代 JNI

### 2.1 JNI 的问题

```
JNI 的痛点:
┌─────────────────────────────────────────────────────┐
│ 1. 复杂: 需要编写 C 代码、生成头文件、编译 .so/.dll │
│ 2. 不安全: raw pointer, 无边界检查, 易内存泄漏     │
│ 3. 开销大: JNI 调用需要从 Java→C→Java 上下文切换   │
│ 4. 脆弱: JNI 函数签名硬编码在 C 代码中             │
│ 5. 不便携: 需要为每个平台编译原生库                │
└─────────────────────────────────────────────────────┘
```

### 2.2 JNI vs FFM 开销对比

```
JNI 调用流程 (每次调用):
  Java → JNI Bridge → C 函数 → JNI Bridge → Java
         │                              │
         └── 句柄创建/销毁              └── 类型转换
         └── 引用计数管理               └── 异常检查
         └── 线程状态切换               └── GC 安全点检查

FFM 调用流程 (每次调用):
  Java → downcall stub → C 函数 → 返回
         │
         └── 直接调用 (无需中间层)
         └── 类型由 MethodHandle 系统处理
```

---

## 3. 架构设计

### 3.1 模块结构

```
┌─────────────────────────────────────────────────────────┐
│                   FFM API 架构                           │
│                                                         │
│  ┌─────────────────────────────────────────────┐       │
│  │           java.lang.foreign                  │       │
│  │                                              │       │
│  │  ┌─────────────┐  ┌────────────────────┐   │       │
│  │  │ Linker      │  │ MemorySegment      │   │       │
│  │  │ (原生链接)  │  │ (内存段)           │   │       │
│  │  └─────────────┘  └────────────────────┘   │       │
│  │                                              │       │
│  │  ┌─────────────┐  ┌────────────────────┐   │       │
│  │  │ Arena       │  │ MemoryLayout       │   │       │
│  │  │ (生命周期)  │  │ (内存布局)         │   │       │
│  │  └─────────────┘  └────────────────────┘   │       │
│  │                                              │       │
│  │  ┌─────────────┐  ┌────────────────────┐   │       │
│  │  │ SymbolLookup│  │ FunctionDescriptor │   │       │
│  │  │ (符号查找)  │  │ (函数签名)         │   │       │
│  │  └─────────────┘  └────────────────────┘   │       │
│  └─────────────────────────────────────────────┘       │
│                                                         │
│  ┌─────────────────────────────────────────────┐       │
│  │           JVM 底层支持                       │       │
│  │  Foreign Linker Runtime (HotSpot C++ 代码)  │       │
│  └─────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────┘
```

### 3.2 核心接口关系

```
SymbolLookup → 查找原生函数地址
       │
       ▼
Linker → 创建 downcall/upcall MethodHandle
       │
       ├── FunctionDescriptor → 描述函数签名
       │
       └── Linker.Option → 调用选项

MemorySegment → 堆外内存段
       │
       ├── Arena → 管理内存生命周期
       │
       └── MemoryLayout → 描述内存结构
```

---

## 4. MemorySegment 与 MemoryLayout

### 4.1 MemorySegment

```java
// 创建 100 字节的堆外内存
try (Arena arena = Arena.ofConfined()) {
    MemorySegment segment = arena.allocate(100);

    // 写入数据
    segment.set(ValueLayout.JAVA_INT, 0, 42);
    segment.set(ValueLayout.JAVA_INT, 4, 100);

    // 读取数据
    int value = segment.get(ValueLayout.JAVA_INT, 0);  // 42

    // 创建数组
    MemorySegment array = arena.allocate(ValueLayout.JAVA_INT, 10);
    for (int i = 0; i < 10; i++) {
        array.set(ValueLayout.JAVA_INT, i * 4, i * 10);
    }
} // arena 关闭时自动释放内存
```

### 4.2 Arena 生命周期

| Arena 类型 | 线程安全 | 生命周期 | 用途 |
|-----------|---------|---------|------|
| `Arena.ofConfined()` | 单线程 | try-with-resources | 临时计算 |
| `Arena.ofShared()` | 多线程 | 手动 close() | 跨线程共享 |
| `Arena.ofAuto()` | 单线程 | GC 回收 | 无需手动管理 |
| `Arena.ofGlobal()` | 全局 | 永不释放 | 全局常量 |

### 4.3 MemoryLayout

```java
// 描述 C 结构体: struct Point { int x; int y; double z; }
StructLayout pointLayout = MemoryLayout.structLayout(
    ValueLayout.JAVA_INT.withName("x"),
    ValueLayout.JAVA_INT.withName("y"),
    MemoryLayout.paddingLayout(32), // 对齐填充
    ValueLayout.JAVA_DOUBLE.withName("z")
);

// 使用 VarHandle 访问字段
VarHandle xHandle = pointLayout.varHandle(MemoryLayout.PathElement.groupElement("x"));
VarHandle zHandle = pointLayout.varHandle(MemoryLayout.PathElement.groupElement("z"));

try (Arena arena = Arena.ofConfined()) {
    MemorySegment point = arena.allocate(pointLayout);
    xHandle.set(point, 0, 10);
    zHandle.set(point, 0, 3.14);
}
```

---

## 5. Downcall 与 Upcall

### 5.1 Downcall (Java → C)

```java
// 调用 C 标准库的 strlen
Linker linker = Linker.nativeLinker();
SymbolLookup stdlib = linker.defaultLookup();

MethodHandle strlen = linker.downcallHandle(
    stdlib.find("strlen").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
);

try (Arena arena = Arena.ofConfined()) {
    MemorySegment str = arena.allocateFrom("Hello, FFM!");
    long length = (long) strlen.invokeExact(str);  // 12
}
```

### 5.2 Upcall (C → Java)

```java
// 创建 Java 回调，传给 C 函数
// C 声明: void qsort(void *base, size_t nmemb, size_t size,
//                    int (*compar)(const void *, const void *));

// Java 比较函数
int compare(MemorySegment a, MemorySegment b) {
    return a.get(ValueLayout.JAVA_INT, 0) - b.get(ValueLayout.JAVA_INT, 0);
}

// 创建 upcall stub
MethodHandle compareHandle =
    MethodHandles.lookup().findStatic(MyClass.class, "compare",
        FunctionDescriptor.of(ValueLayout.JAVA_INT,
            ValueLayout.ADDRESS, ValueLayout.ADDRESS));

MemorySegment comparCallback = linker.upcallStub(compareHandle,
    FunctionDescriptor.of(ValueLayout.JAVA_INT,
        ValueLayout.ADDRESS, ValueLayout.ADDRESS),
    Arena.ofAuto());
```

---

## 6. 性能对比

### 6.1 微基准测试（示意）

| 操作 | JNI | FFM API | Unsafe | 纯 Java |
|------|-----|---------|--------|---------|
| 单次原生调用 (strlen) | 40ns | 8ns | N/A | N/A |
| 批量内存访问 (1MB) | 2,100ns | 800ns | 750ns | 900ns |
| 结构体字段访问 | 15ns | 3ns | 2ns | 1ns |
| 回调 (upcall) | 80ns | 25ns | N/A | N/A |

> FFM API 原生调用开销约为 JNI 的 1/5，接近 Unsafe 的性能。

### 6.2 为什么 FFM 更快

1. **无需 JNI 桥接代码**：直接通过 MethodHandle 调用原生函数
2. **无句柄管理**：不创建/销毁 JNI local/global references
3. **无 GC 安全点**：调用前不需要检查 GC 安全点
4. **优化过的类型转换**：JVM 内部优化了 FFM 的参数传递路径

---

## 7. 安全性保障

| 安全特性 | JNI | FFM API | Unsafe |
|---------|-----|---------|--------|
| 边界检查 | ❌ | ✅ | ❌ |
| 生命周期管理 | ❌ | ✅ (Arena) | ❌ |
| 空指针检查 | ❌ | ✅ | ❌ |
| 对齐检查 | ❌ | ✅ | ❌ |
| 类型安全 | ⚠️ (C 层) | ✅ (Java 层) | ❌ |
| 内存泄漏防护 | ❌ | ✅ (Arena GC) | ❌ |

---

## 8. 代码示例

### 完整的 C 库调用示例

```java
import java.lang.foreign.*;
import java.lang.invoke.MethodHandle;
import java.lang.invoke.MethodHandles;

public class FFMExample {
    public static void main(String[] args) throws Throwable {
        Linker linker = Linker.nativeLinker();
        SymbolLookup stdlib = linker.defaultLookup();

        // 调用 printf
        MethodHandle printf = linker.downcallHandle(
            stdlib.find("printf").orElseThrow(),
            FunctionDescriptor.of(ValueLayout.JAVA_INT, ValueLayout.ADDRESS)
        );

        try (Arena arena = Arena.ofConfined()) {
            MemorySegment format = arena.allocateFrom("Hello from FFM! %d\n");
            int result = (int) printf.invokeExact(format, 2026);
        }
    }
}
```

---

## 相关链接

- [JEP 454: Foreign Function & Memory API](/jeps/ffi/jep-454.md)
- [JNI vs Panama 对比](/guides/comparisons/jni-vs-panama.md)
- [Panama 主题](/by-topic/core/panama/)
- [java.lang.foreign 包](/modules/java.base.md)
