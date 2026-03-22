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
| **G1 可中断 Mixed GC** | ⭐⭐⭐ | [JEP 344](/jeps/gc/jep-344.md) |
| **微基准测试套件** | ⭐⭐⭐ | JEP 230 |
| **默认 CDS 存档** | ⭐⭐ | [JEP 341](/jeps/performance/jep-341.md) |

---

## 2. 关键 JEP

| JEP | 标题 | 说明 |
|-----|------|------|
| [JEP 325](/jeps/language/jep-325.md) | Switch Expressions (Preview) | Switch 表达式 |
| [JEP 189](/jeps/gc/jep-189.md) | Shenandoah: A Low-Pause-Time Garbage Collector | Shenandoah GC |
| [JEP 344](/jeps/gc/jep-344.md) | Abortable Mixed Collections for G1 | G1 可中断 Mixed GC |
| [JEP 230](https://openjdk.org/jeps/230) | Microbenchmark Suite | 微基准测试套件 |
| [JEP 341](/jeps/performance/jep-341.md) | Default CDS Archives | 默认 CDS 存档 |
| [JEP 334](/jeps/language/jep-334.md) | JVM Constants API | JVM 常量 API |
| [JEP 340](/jeps/platform/jep-340.md) | One AArch64 Port, Not Two | 统一 AArch64 端口 |
| [JEP 346](/jeps/gc/jep-346.md) | Promptly Return Unused Committed Memory | 及时归还内存 |

---

## 3. 代码示例

### Switch 表达式（第1次预览）

```java
// 之前
switch (day) {
    case MONDAY:
    case FRIDAY:
    case SUNDAY:
        System.out.println(6);
        break;
    // ...
}

// JDK 12 (第1次预览)
switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> System.out.println(6);
    case TUESDAY                -> System.out.println(7);
    case THURSDAY, SATURDAY     -> System.out.println(8);
    case WEDNESDAY              -> System.out.println(9);
}
```

---

## 4. 相关链接

- [发布说明](https://openjdk.org/projects/jdk/12/)
