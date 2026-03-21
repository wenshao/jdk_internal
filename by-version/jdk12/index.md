# JDK 12

> **发布日期**: 2019-03-19 | **类型**: Feature Release

---
## 目录

1. [核心特性](#1-核心特性)
2. [关键 JEP](#2-关键-jep)
3. [代码示例](#3-代码示例)
4. [相关链接](#4-相关链接)

---


## 1. 核心特性

JDK 12 引入了 Switch 表达式（第1次预览）和 Shenandoah GC。

| 特性 | 影响 | 详情 |
|------|------|------|
| **Switch 表达式（第1次预览）** | ⭐⭐⭐⭐⭐ | JEP 325，简化条件逻辑 |
| **Shenandoah GC（实验）** | ⭐⭐⭐⭐ | JEP 189，低延迟 GC |
| **G1 可中断 Mixed GC** | ⭐⭐⭐ | JEP 344 |
| **微基准测试套件** | ⭐⭐⭐ | JEP 230 |
| **默认 CDS 存档** | ⭐⭐ | JEP 341 |

---

## 2. 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 325](https://openjdk.org/jeps/325) | Switch Expressions (Preview) | Switch 表达式 |
| [JEP 189](https://openjdk.org/jeps/189) | Shenandoah: A Low-Pause-Time Garbage Collector | Shenandoah GC |
| [JEP 344](https://openjdk.org/jeps/344) | Abortable Mixed Collections for G1 | G1 可中断 Mixed GC |
| [JEP 230](https://openjdk.org/jeps/230) | Microbenchmark Suite | 微基准测试套件 |
| [JEP 341](https://openjdk.org/jeps/341) | Default CDS Archives | 默认 CDS 存档 |
| [JEP 334](https://openjdk.org/jeps/334) | JVM Constants API | JVM 常量 API |
| [JEP 340](https://openjdk.org/jeps/340) | One AArch64 Port, Not Two | 统一 AArch64 端口 |
| [JEP 346](https://openjdk.org/jeps/346) | Promptly Return Unused Committed Memory | 及时归还内存 |

---

## 3. 代码示例

### Switch 表达式（第1次预览）

```java
// 之前
switch (day) {
    case MONDAY:
    case FRIDAY:
    case SUNDAY:
        System.out.println("Weekend");
        break;
    // ...
}

// JDK 12 (第1次预览)
switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> System.out.println("Weekend");
    case TUESDAY, WEDNESDAY, THURSDAY -> System.out.println("Weekday");
    case SATURDAY -> System.out.println("Weekend");
}
```

---

## 4. 相关链接

- [发布说明](https://openjdk.org/projects/jdk/12/)
