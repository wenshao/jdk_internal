# JSR (Java Specification Request) 索引

> Java 规范请求 - Java 平台正式规范文档

---

## 什么是 JSR？

JSR (Java Specification Request) 是通过 **JCP (Java Community Process)** 提交和审批的 Java 平台规范请求。与 JEP 不同，JSR 是正式的规范文档，需要经过 JCP 执行委员会投票通过。

---

## JSR vs JEP 对比

| 维度 | JSR | JEP |
|------|-----|-----|
| **组织** | JCP (Java Community Process) | OpenJDK |
| **类型** | 规范 (Specification) | 实现 (Implementation) |
| **审批** | JCP 执行委员会投票 | OpenJDK 项目组决定 |
| **内容** | API 契约、语言语法 | 实现细节、性能、工具 |
| **生命周期** | 独立版本 (JSR 335) | 绑定 JDK 版本 |
| **示例** | Lambda (JSR 335) | Virtual Threads (JEP 444) |

### 关系图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Java 平台演进                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   JSR (规范)                    JEP (实现)                      │
│   ┌──────────────┐              ┌──────────────┐                │
│   │ JSR 335      │ ──────────► │ JEP 126      │                │
│   │ Lambda       │   定义       │ 实现         │                │
│   └──────────────┘              └──────────────┘                │
│                                                                 │
│   ┌──────────────┐              ┌──────────────┐                │
│   │ JSR 376      │ ──────────► │ JEP 261      │                │
│   │ 模块系统     │   定义       │ 模块实现     │                │
│   └──────────────┘              └──────────────┘                │
│                                                                 │
│   ┌──────────────┐              ┌──────────────┐                │
│   │ (无 JSR)     │ ◄────────── │ JEP 444      │                │
│   │              │   纯实现     │ 虚拟线程     │                │
│   └──────────────┘              └──────────────┘                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 何时需要 JSR？

| 场景 | 需要 JSR | 只需 JEP |
|------|----------|----------|
| 新语言语法 | ✅ | ❌ |
| 新 API | ✅ | ❌ |
| JVM 内部优化 | ❌ | ✅ |
| GC 改进 | ❌ | ✅ |
| 工具改进 | ❌ | ✅ |
| 性能优化 | ❌ | ✅ |

---

## 主题分类

### 语言规范

| JSR | 标题 | JDK | 状态 | 说明 |
|-----|------|-----|------|------|
| [JSR 335](language/jsr-335.md) ⭐ | Lambda Expressions | 8 | ✅ Final | Lambda 表达式、Stream API |
| [JSR 308](https://jcp.org/en/jsr/detail?id=308) | Type Annotations | 8 | ✅ Final | 类型注解 |
| [JSR 394](https://jcp.org/en/jsr/detail?id=394) | Pattern Matching for instanceof | 16 | ✅ Final | 类型模式匹配 |
| [JSR 395](https://jcp.org/en/jsr/detail?id=395) | Records | 16 | ✅ Final | 记录类 |
| [JSR 397](https://jcp.org/en/jsr/detail?id=397) | Sealed Classes | 17 | ✅ Final | 密封类 |
| ~~JSR 409~~ | Value Types | ❌ Withdrawn | 值类型 (已撤回，并入 Project Valhalla) |

### API 规范

| JSR | 标题 | JDK | 状态 | 说明 |
|-----|------|-----|------|------|
| [JSR 166](https://jcp.org/en/jsr/detail?id=166) | Concurrency Utilities | 5 | ✅ Final | 并发工具 |
| [JSR 203](https://jcp.org/en/jsr/detail?id=203) | NIO.2 | 7 | ✅ Final | 新 I/O API |
| [JSR 310](api/jsr-310.md) ⭐ | Date and Time API | 8 | ✅ Final | 日期时间 |
| [JSR 353](https://jcp.org/en/jsr/detail?id=353) | JSON Processing | 8 | ✅ Final | JSON 处理 |
| [JSR 366](https://jcp.org/en/jsr/detail?id=366) | HTTP Client | 11 | ✅ Final | HTTP 客户端 |

### 平台规范

| JSR | 标题 | 版本 | 状态 | 说明 |
|-----|------|------|------|------|
| [JSR 376](platform/jsr-376.md) ⭐ | Java SE 9 Platform | 9 | ✅ Final | Java SE 9 平台 + 模块系统 |
| [JSR 383](https://jcp.org/en/jsr/detail?id=383) | Java SE 11 Platform | 11 | ✅ Final | Java SE 11 平台 |
| [JSR 384](https://jcp.org/en/jsr/detail?id=384) | Java SE 17 Platform | 17 | ✅ Final | Java SE 17 平台 |
| [JSR 396](https://jcp.org/en/jsr/detail?id=396) | Java SE 21 Platform | 21 | ✅ Final | Java SE 21 平台 |

> ⭐ = 有本地详细文档

---

## JSR 生命周期

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Draft   │───►│  Early   │───►│  Public  │───►│ Proposed │───►│  Final   │
│ Review   │    │  Draft   │    │  Review  │    │  Final   │    │ Release  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │               │               │               │
   几周            1-3个月          30-90天         投票期          完成
```

### 状态说明

| 状态 | 说明 |
|------|------|
| 📝 Draft | 草稿阶段 |
| 🔍 Early Draft | 早期草案审查 |
| 👁️ Public Review | 公开审查 |
| 📊 Proposed Final | 提议最终草案 |
| ✅ Final Release | 最终发布 |
| ❌ Withdrawn | 撤回 |
| 💤 Dormant | 休眠 |

---

## 知名 JSR 贡献者

### Brian Goetz (JSR 335 - Lambda)

- **角色**: JSR 335 Specification Lead
- **组织**: Oracle
- **著作**: 《Java Concurrency in Practice》
- **贡献**: Lambda 表达式、Stream API、默认方法

### Mark Reinhold (JSR 376 - Module System)

- **角色**: JSR 376 Specification Lead
- **组织**: Oracle
- **职位**: Java Platform Group 首席架构师
- **贡献**: 模块系统 (12年开发周期)

### Stephen Colebourne (JSR 310 - Date/Time)

- **角色**: JSR 310 Specification Lead
- **组织**: Independent
- **项目**: Joda-Time 创建者、ThreeTen 项目
- **贡献**: java.time API

### Gavin Bierman (JSR 395/397 - Records/Sealed)

- **角色**: JEP Owner
- **组织**: Oracle Labs
- **背景**: 前微软研究院研究员
- **贡献**: Records、Sealed Classes、Pattern Matching

---

## 源码参考

### java.lang.Record

```java
// src/java.base/share/classes/java/lang/Record.java
/**
 * 所有 Java 语言 record 类的公共基类。
 * @since 16
 */
public abstract class Record {
    @Override
    public abstract boolean equals(Object obj);
    @Override
    public abstract int hashCode();
    @Override
    public abstract String toString();
}
```

### java.base 模块

```java
// src/java.base/share/classes/module-info.java
module java.base {
    exports java.io;
    exports java.lang;
    exports java.lang.invoke;
    exports java.time;      // JSR 310
    exports java.util.function;  // JSR 335
    exports java.util.stream;    // JSR 335
    // ...
}
```

---

## 重要 JSR 详解

### JSR 335: Lambda Expressions (JDK 8)

**最重要的语言特性 JSR 之一**

```java
// Lambda 表达式
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
names.stream()
     .filter(s -> s.startsWith("A"))
     .forEach(System.out::println);

// 方法引用
list.stream().map(String::toUpperCase)

// 默认方法
interface Collection {
    default Stream<E> stream() { ... }
}
```

**关联 JEP**: JEP 126

**详见**: [JSR 335 分析](language/jsr-335.md)

---

### JSR 310: Date and Time API (JDK 8)

**取代 Date 和 Calendar 的新日期时间 API**

```java
// 本地日期时间
LocalDate date = LocalDate.of(2024, 3, 20);
LocalTime time = LocalTime.of(10, 30);
LocalDateTime dateTime = LocalDateTime.of(date, time);

// 时区
ZonedDateTime zoned = ZonedDateTime.of(dateTime, ZoneId.of("Asia/Shanghai"));

// 时间段
Duration duration = Duration.between(start, end);
Period period = Period.between(date1, date2);

// 格式化
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm");
String formatted = dateTime.format(formatter);
```

**详见**: [JSR 310 分析](api/jsr-310.md)

---

### JSR 376: Java Platform Module System (JDK 9)

**模块系统的核心规范**

```java
// module-info.java
module com.example.myapp {
    requires java.sql;
    requires transitive java.logging;
    exports com.example.api;
    opens com.example.internal to com.example.tests;
}
```

**关联 JEP**: JEP 261

**详见**: [JSR 376 分析](platform/jsr-376.md)

---

### JSR 395: Records (JDK 16)

**记录类的规范**

```java
// 记录类
public record Point(int x, int y) {
    // 自动生成: constructor, equals, hashCode, toString
}

// 使用
Point p = new Point(10, 20);
System.out.println(p.x());  // 10
```

**关联 JEP**: JEP 395

**详见**: [JSR 395 分析](language/jsr-395.md)

---

### JSR 397: Sealed Classes (JDK 17)

**密封类的规范**

```java
// 密封类
public sealed class Shape 
    permits Circle, Rectangle, Triangle {
}

public final class Circle extends Shape {
    private final double radius;
}

public final class Rectangle extends Shape {
    private final double width, height;
}
```

**关联 JEP**: JEP 409

**详见**: [JSR 397 分析](language/jsr-397.md)

---

## JSR 与 JEP 的协同

### 同时有 JSR 和 JEP 的特性

| 特性 | JSR | JEP | 关系 |
|------|-----|-----|------|
| Lambda | 335 | 126 | JSR 定义语法，JEP 实现编译器 |
| 模块系统 | 376 | 261 | JSR 定义规范，JEP 实现 jlink |
| Records | 395 | 395 | JSR 和 JEP 编号相同 |
| Sealed Classes | 397 | 409 | 不同编号 |
| Pattern Matching | 394, 398 | 394, 411 | 多个 JSR 和 JEP |

### 只有 JEP 的特性

这些特性不需要 JSR，因为它们不改变语言语法或 API 契约：

| 特性 | JEP | 原因 |
|------|-----|------|
| Virtual Threads | 444 | API 不变，只是实现 |
| ZGC | 333 | JVM 内部 |
| String Templates | 430 | 语法糖 |
| FFM API | 454 | 新 API (有争议) |

---

## 相关链接

- [JCP 官网](https://jcp.org/)
- [JSR 列表](https://jcp.org/en/jsr/all)
- [OpenJDK JEPs](https://openjdk.org/jeps/)
- [JEP 索引](/jeps/)
- [语言特性时间线](/by-topic/language/)

---

## 参考

- [JSR 335: Lambda Expressions](https://jcp.org/en/jsr/detail?id=335)
- [JSR 310: Date and Time API](https://jcp.org/en/jsr/detail?id=310)
- [JSR 376: Module System](https://jcp.org/en/jsr/detail?id=376)
- [JSR 395: Records](https://jcp.org/en/jsr/detail?id=395)
- [JSR 397: Sealed Classes](https://jcp.org/en/jsr/detail?id=397)
