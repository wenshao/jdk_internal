# 外部函数接口 (FFI) JEPs

> Foreign Function & Memory API 相关 JEP

---
## 目录

1. [概览](#1-概览)
2. [Foreign Function & Memory API (JEP 454)](#2-foreign-function--memory-api-jep-454)
3. [Prepare to Restrict JNI (JEP 472)](#3-prepare-to-restrict-jni-jep-472)
4. [FFM vs JNI 对比](#4-ffm-vs-jni-对比)
5. [迁移指南](#5-迁移指南)
6. [相关链接](#6-相关链接)

---


## 1. 概览

| JEP | 标题 | 版本 | 状态 |
|-----|------|------|------|
| [JEP 454](jep-454.md) | Foreign Function & Memory API | JDK 22 | ✅ 正式 |
| [JEP 472](jep-472.md) | Prepare to Restrict JNI | JDK 24 | ⚠️ 废弃警告 |

---

## 2. Foreign Function & Memory API (JEP 454)

### 演进历程

| 版本 | JEP | 状态 |
|------|-----|------|
| JDK 14 | 370 | 🔧 孵化 | Foreign-Memory Access API |
| JDK 15 | 383 | 🔧 孵化 | Foreign-Memory Access API (Second Incubator) |
| JDK 16 | 389 | 🔧 孵化 | Foreign Linker API (First Incubator) |
| JDK 17 | 412 | 🔍 预览 | Foreign Function & Memory API |
| JDK 18 | 424 | 🔍 预览 | Foreign Function & Memory API |
| JDK 19 | 442 | 🔍 预览 | Foreign Function & Memory API |
| JDK 20 | 442 | 🔍 预览 | Foreign Function & Memory API |
| JDK 21 | 442 | 🔍 预览 | Foreign Function & Memory API |
| JDK 22 | 454 | ✅ 正式 | Foreign Function & Memory API |

### 核心用法

```java
// 1. 分配外部内存
try (Arena arena = Arena.ofConfined()) {
    MemorySegment segment = arena.allocate(100);
    
    // 2. 调用本地函数
    Linker linker = Linker.nativeLinker();
    SymbolLookup stdlib = linker.defaultLookup();
    
    MethodHandle strlen = linker.downcallHandle(
        stdlib.find("strlen").get(),
        FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
    );
    
    // 3. 执行调用
    long result = (long) strlen.invokeExact(segment);
}
```

### 主要组件

| 组件 | 说明 |
|------|------|
| `Linker` | 链接本地库 |
| `SymbolLookup` | 查找符号 |
| `FunctionDescriptor` | 描述函数签名 |
| `MemorySegment` | 内存段 |
| `MemoryLayout` | 内存布局 |
| `Arena` | 内存管理 |

**详见**：[FFM API 详解](ffm-api.md) | [JEP 454](jep-454.md)

---

## 3. Prepare to Restrict JNI (JEP 472)

### 背景

JNI (Java Native Interface) 存在安全问题：

1. **不安全**： JNI 允许绕过 Java 安全检查
2. **维护成本**： JNI 代码难以维护
3. **替代方案**： FFM API 提供更安全的替代

### 影响

```java
// JDK 24+ 默认发出警告
System.loadLibrary("mylib");  // Warning: JNI is deprecated
```

**详见**：[JNI 限制分析](jni-restrictions.md) | [JEP 472](jep-472.md)

---

## 4. FFM vs JNI 对比

| 特性 | JNI | FFM API |
|------|-----|---------|
| 类型安全 | ❌ 不安全 | ✅ 安全 |
| 内存安全 | ❌ 不安全 | ✅ 安全 |
| 性能 | 中等 | 更好 |
| 易用性 | 复杂 | 更简单 |
| 平台支持 | 全平台 | 全平台 |

---

## 5. 迁移指南

### 从 JNI 迁移到 FFM

```java
// JNI 方式
public class NativeLib {
    static {
        System.loadLibrary("native");
    }
    
    public static native long strlen(String s);
}

// FFM 方式
public class NativeLib {
    private static final Linker LINKER = Linker.nativeLinker();
    private static final MethodHandle STRLEN;
    
    static {
        SymbolLookup lookup = LINKER.defaultLookup();
        STRLEN = LINKER.downcallHandle(
            lookup.find("strlen").get(),
            FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
        );
    }
    
    public static long strlen(MemorySegment s) throws Throwable {
        return (long) STRLEN.invokeExact(s);
    }
}
```

---

## 6. 相关链接

- [JEP 454: Foreign Function & Memory API](https://openjdk.org/jeps/454)
- [JEP 472: Prepare to Restrict JNI](https://openjdk.org/jeps/472)
- FFM API 指南 
