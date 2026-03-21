# Project Panama 时间线

外部函数接口和外部内存器 API 的完整演进历史。

[← 返回 Panama](./)

---
## 目录

1. [2014: 项目启动](#1-2014-项目启动)
2. [2015-2018: 早期原型](#2-2015-2018-早期原型)
3. [2020: JDK 14 - Foreign Memory 孵化](#3-2019-jdk-14---foreign-memory-孵化)
4. [2020-2021: JDK 15-16 - Linker API](#4-2020-jdk-15---linker-api)
5. [2021: JDK 16 - 内存 API 改进](#5-2021-jdk-16---内存-api-改进)
6. [2022: JDK 17-19 - FFI 整合](#6-2022-jdk-17-19---ffi-整合)
7. [2022-2023: JDK 19-21 - 预览版本](#7-2023-jdk-19-20---预览版本)
8. [2024: JDK 22 - 正式发布](#8-2024-jdk-22---正式发布)
9. [API 演进历史](#9-api-演进历史)
10. [时间线总览](#10-时间线总览)
11. [里程碑总结](#11-里程碑总结)
12. [相关项目](#12-相关项目)

---


## 1. 2014: 项目启动

### 项目宣布

- **日期**: 2014-08
- **事件**: Project Panama 正式启动
- **目标**: "替代 JNI，提供与原生代码的无缝互操作"
- **初始动机**:
  - JNI 复杂且易错
  - 跨平台困难
  - 性能开销

---

## 2. 2015-2018: 早期原型

### 原型开发

- **日期**: 2015-2018
- **内容**:
  - `jextract` 工具原型
  - `ffi` 库绑定
  - `ByteBuffer` 改进讨论

### JNI 问题总结

- **日期**: 2017-03
- **文档**: "The Case for Panama"
- **关键问题**:
  - JNI 调用开销 ~50-100ns
  - 需要生成胶水代码
  - 错误处理复杂

---

## 3. 2020: JDK 14 - Foreign Memory 孵化

### JEP 370: Foreign Memory Access API (Incubator)

- **日期**: 2020-03 (JDK 14 孵化器)
- **包**: `jdk.incubator.foreign`
- **特性**:
  - `MemorySegment` - 内存段
  - `MemoryAddress` - 内存地址
  - `MemoryLayout` - 内存布局

```java
// JDK 14 示例
// JDK 14 使用 MemorySegment.allocateNative()
MemorySegment segment = MemorySegment.allocateNative(100);
segment.set(ValueLayout.JAVA_INT, 0, 42);
// 需要手动管理生命周期
```

---

## 4. 2020-2021: JDK 15-16 - Linker API

### JEP 389: Foreign Linker API (Incubator)

- **日期**: 2021-03 (JDK 16 孵化器)
- **特性**:
  - `Linker` - 原生链接器
  - `SymbolLookup` - 符号查找
  - `FunctionDescriptor` - 函数描述符
  - `MemoryLayout` - 结构体布局

```java
// JDK 16 示例
Linker linker = Linker.nativeLinker();
SymbolLookup stdlib = linker.defaultLookup();
MethodHandle strlen = linker.downcallHandle(
    stdlib.lookup("strlen").get(),
    FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
);
```

### JEP 373: Reimplementing the Legacy Socket API

- **日期**: 2020-06 (JDK 15)
- **相关**: 为 Panama 奠定基础

---

## 5. 2021: JDK 16 - 内存 API 改进

### JEP 393: Foreign Memory Access API (Third Incubator)

- **日期**: 2021-03 (JDK 16 第三孵化器)
- **改进**:
  - `MemorySession` 替代手动管理
  - 更好的内存生命周期管理
  - `Arena` 概念引入

### JEP 416: Reimplementing the JDK Intrinsics

- **日期**: 2021-03 (JDK 16)
- **相关**: 为 Panama JIT 优化打基础

---

## 6. 2022: JDK 17-19 - FFI 整合

### JEP 412: Foreign Function & Memory API (Incubator)

- **日期**: 2021-09 (JDK 17 孵化器)
- **里程碑**: FFI 和 Memory API 合并

### JEP 419: Foreign Function & Memory API (Second Incubator)

- **日期**: 2022-03 (JDK 18 第二孵化器)
- **改进**:
  - 统一的 `Linker` 接口
  - 改进的 `MemoryLayout`
  - 更好的错误处理

---

## 7. 2022-2023: JDK 19-21 - 预览版本

### JEP 424: Foreign Function & Memory API (Preview)

- **日期**: 2022-09 (JDK 19 预览)
- **包**: `java.lang.foreign` (移除 incubator)
- **特性**:
  - 类型安全的外部函数调用
  - 结构化内存访问
  - Arena 内存管理

```java
// JDK 19 预览 API
import java.lang.foreign.*;

Linker linker = Linker.nativeLinker();
MethodHandle strlen = linker.downcallHandle(...);
```

### JEP 434: Foreign Function & Memory API (Second Preview)

- **日期**: 2023-03 (JDK 20 第二预览)
- **改进**:
  - API 细节调整
  - 性能优化
  - 文档完善

### JEP 442: Foreign Function & Memory API (Third Preview)

- **日期**: 2023-09 (JDK 21 第三预览)
- **改进**:
  - 最终 API 调整
  - 准备正式发布

---

## 8. 2024: JDK 22 - 正式发布

### JEP 454: Foreign Function & Memory API

- **日期**: 2024-03 (JDK 22 正式)
- **里程碑**: API 正式发布
- **包**: `java.lang.foreign.*`
- **特性**:
  - `Linker` - 原生函数链接器
  - `MemorySegment` - 内存段
  - `Arena` - 内存生命周期管理
  - `FunctionDescriptor` - 函数签名
  - `GroupLayout` - 结构体布局

---

## 9. API 演进历史

### MemorySegment

| 版本 | API | 变化 |
|------|-----|------|
| JDK 14 | `MemorySegment` | 首次引入 |
| JDK 15 | `MemoryAddress` | 分离地址概念 |
| JDK 19 | `MemorySession` | 会话管理 |
| JDK 19 | `MemorySegment` | 统一 API |
| JDK 22 | `MemorySegment` | 正式版 |

### Linker

| 版本 | API | 变化 |
|------|-----|------|
| JDK 16 | `NativeLinker` | 孵化器 |
| JDK 18 | `Linker` | 统一接口 |
| JDK 19 | `Linker` | 预览版 |
| JDK 22 | `Linker` | 正式版 |

---

## 10. 时间线总览

```
2014 ── 2019 ── 2020 ── 2021 ── 2023 ── 2024
  │        │        │        │        │        │
启动    Memory  Linker   第二孵化  预览    正式
        孵化器   孵化器   整合     JDK19   JDK22
        JDK14   JDK15    JDK18
```

---

## 11. 里程碑总结

| 里程碑 | 版本 | 影响 |
|--------|------|------|
| **Foreign Memory 孵化** | JDK 14 | 堆外内存 API |
| **Foreign Linker 孵化** | JDK 16 | FFI API |
| **API 合并** | JDK 18 | 统一接口 |
| **预览版本** | JDK 19 | 移出 incubator |
| **正式发布** | JDK 22 | 生产就绪 |

---

## 12. 相关项目

| 项目 | 关系 |
|------|------|
| **Project Valhalla** | 值类型与外部内存配合 |
| **Project Loom** | 虚拟线程与阻塞 I/O |
| **JNI** | Panama 替代的技术 |

→ [返回 Panama](./)
