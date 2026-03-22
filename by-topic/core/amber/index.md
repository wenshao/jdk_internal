# Project Amber

Java 语言特性演进项目：让 Java 更简洁、更安全、更易表达。

[← 返回核心平台](../)

---
## 目录

1. [TL;DR](#1-tldr)
2. [项目概述](#2-项目概述)
3. [主要特性详解](#3-主要特性详解)
4. [时间线](#4-时间线)
5. [核心贡献者](#5-核心贡献者)
6. [与其他项目的关系](#6-与其他项目的关系)
7. [语法对比](#7-语法对比)
8. [特性状态说明](#8-特性状态说明)
9. [参考资料](#9-参考资料)

---


## 1. TL;DR

**Project Amber** 是 OpenJDK 的语言特性项目，专注于：
- **更简洁的语法** - 减少样板代码
- **更安全的类型** - 模式匹配、密封类
- **更易表达** - Record、switch 表达式

**状态**: 持续交付中 (2017-至今)，多个特性已正式发布

---

## 2. 项目概述

### 目标

```
┌─────────────────────────────────────────────────────────┐
│                   Project Amber                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  • 减少"噪音"代码          • 提高类型安全                │
│  • 增强模式匹配            • 简化日常开发                │
│  • 更好的数据建模          • 保持向后兼容                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 核心特性

| 特性 | 版本 | JEP |
|------|------|-----|
| **Local Variable Type Inference** | JDK 10 | JEP 286 |
| **Switch Expressions** | JDK 14 | JEP 361 |
| **Text Blocks** | JDK 15 | JEP 378 |
| **Records** | JDK 16 | JEP 395 |
| **Pattern Matching for instanceof** | JDK 16 | JEP 394 |
| **Sealed Classes** | JDK 17 | JEP 409 |
| **Pattern Matching for switch** | JDK 21 | JEP 441 |
| **Record Patterns** | JDK 21 | JEP 440 |
| **Unnamed Patterns & Variables** | JDK 22 | JEP 456 |
| **Implicit Classes** | JDK 25 | JEP 512 |
| **Module Import Declarations** | JDK 25 | JEP 511 |
| **Flexible Constructor Bodies** | JDK 25 | JEP 513 |
| **String Templates** | (已撤回) | JEP 430 → 459 → 465 |
| **Primitive Patterns** | JDK 23 (4th Preview) | JEP 455 → 488 → 507 → 530 |

---

## 3. 主要特性详解

### 1. Records (JEP 395)

```java
// 传统写法
public final class Point {
    private final int x;
    private final int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() { return x; }
    public int getY() { return y; }

    @Override
    public boolean equals(Object o) { ... }
    @Override
    public int hashCode() { ... }
    @Override
    public String toString() { ... }
}

// Record 写法
public record Point(int x, int y) {}
```

### 2. Pattern Matching (JEP 394, 441)

```java
// instanceof 模式匹配
// 旧写法
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.length());
}

// 新写法 (JDK 16)
if (obj instanceof String s) {
    System.out.println(s.length());
}

// switch 模式匹配 (JDK 21)
String formatted = switch (obj) {
    case Integer i -> String.format("int %d", i);
    case Long l    -> String.format("long %d", l);
    case Double d  -> String.format("double %f", d);
    case String s  -> String.format("String %s", s);
    default        -> obj.toString();
};

// 守卫语法 (Guards)
String check = switch (obj) {
    case String s when s.length() > 5 -> "Long string: " + s;
    case String s                    -> "Short string: " + s;
    case Integer i when i > 0         -> "Positive int";
    case Integer i                   -> "Non-positive int";
    default                          -> "Unknown";
};

// null 处理 (JDK 21)
String result = switch (obj) {
    case null      -> "null value";
    case String s  -> "String: " + s;
    default        -> "Other type";
};
```

### 3. Record Patterns (JEP 440)

```java
// 嵌套解构
record Point(int x, int y) {}
record Rectangle(Point topLeft, Point bottomRight) {}

// 旧写法
void printOld(Rectangle r) {
    Point tl = r.topLeft();
    int x = tl.x();
    int y = tl.y();
    System.out.println("Top-left: (" + x + ", " + y + ")");
}

// 新写法 - Record Pattern
void printNew(Rectangle r) {
    if (r instanceof Rectangle(Point(int x, int y), Point bottomRight)) {
        System.out.println("Top-left: (" + x + ", " + y + ")");
    }
}

// switch + Record Pattern
String describe(Object obj) {
    return switch (obj) {
        case Rectangle(Point(int x1, int y1), Point(int x2, int y2)) ->
            "Rectangle from (%d,%d) to (%d,%d)".formatted(x1, y1, x2, y2);
        case Point(int x, int y) ->
            "Point at (%d,%d)".formatted(x, y);
        default -> "Unknown shape";
    };
}

// 结合 unnamed pattern
void extractX(Object obj) {
    if (obj instanceof Point(int x, _)) {
        // 只关心 x 坐标，忽略 y
        System.out.println("X coordinate: " + x);
    }
}
```

### 4. Sealed Classes (JEP 409)

```java
// 定义密封类
public sealed interface Shape
    permits Circle, Rectangle, Square {
    double area();
}

// 实现类必须是 sealed、non-sealed 或 final
public final record Circle(double radius) implements Shape {
    public double area() { return Math.PI * radius * radius; }
}

public final record Rectangle(double width, double height) implements Shape {
    public double area() { return width * height; }
}

public non-sealed class Square implements Shape {
    // non-sealed 允许继续扩展
    private final double side;
    public Square(double side) { this.side = side; }
    public double side() { return side; }
    public double area() { return side * side; }
}

// 编译器检查穷尽性
String describe(Shape s) {
    return switch (s) {
        case Circle c    -> "Circle with radius " + c.radius();
        case Rectangle r -> "Rectangle " + r.width() + "x" + r.height();
        case Square sq   -> "Square with side " + sq.side();
        // 如果缺少某个 case，编译器会报错
    };
}
```

### 5. Text Blocks (JEP 378)

```java
// 旧写法
String json = "{\n" +
    "  \"name\": \"John\",\n" +
    "  \"age\": 30\n" +
    "}";

// Text Block 写法
String json = """
    {
      "name": "John",
      "age": 30
    }
    """;

// 多行字符串
String query = """
    SELECT id, name, email
    FROM users
    WHERE status = 'active'
    ORDER BY created_at DESC
    """;

// 文本块缩进和格式化
// \s 保留尾部空格，\ 取消换行
String text = """
    Line 1\s\s
    Line 2 \
    Line 3
    """;
// 输出: "Line 1  \nLine 2 Line 3\n"

// 文本块用于 SQL、JSON、XML 等场景
String html = """
    <html>
        <body>
            <p>Hello, %s!</p>
        </body>
    </html>
    """.formatted(name);
```

### 6. Switch Expressions (JEP 361)

```java
// 旧写法 - 语句形式
int result;
switch (day) {
    case MONDAY:
    case FRIDAY:
    case SUNDAY:
        result = 6;
        break;
    case TUESDAY:
        result = 7;
        break;
    default:
        result = 0;
}

// 新写法 - 表达式形式
int result = switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> 6;
    case TUESDAY               -> 7;
    default                   -> 0;
};

// 使用 yield 返回复杂值
String message = switch (status) {
    case 0 -> {
        System.out.println("Processing...");
        yield "OK";  // yield 用于代码块
    }
    case 1 -> "Warning";
    case 2 -> "Error";
    default -> "Unknown";
};

// 多标签 case
int numLetters = switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> 6;
    case TUESDAY                -> 7;
    case THURSDAY, SATURDAY     -> 8;
    case WEDNESDAY              -> 9;
};
```

### 7. Unnamed Patterns & Variables (JEP 456)

```java
// 使用 _ 忽略不关心的值

// instanceof 中忽略变量
if (obj instanceof String _) {
    // 只关心类型，不关心具体值
    System.out.println("It's a string!");
}

// Lambda 中忽略参数
stream.map(_ -> "constant")  // 所有元素映射为 "constant"

// Record 模式中忽略组件
if (obj instanceof Point(int x, _)) {
    // 只关心 x 坐标，忽略 y
    System.out.println("X: " + x);
}

// 异常处理中忽略异常对象
try {
    riskyOperation();
} catch (Exception _) {
    logger.error("Failed");
}

// try-with-resources 中忽略资源变量
try (var _ = ScopedContext.open()) {
    doWork();
}
```

### 8. Compact Source Files & Instance Main Methods (JEP 512)

```java
// 单文件程序无需类声明 (JDK 25 正式)
// HelloWorld.java
void main() {
    System.out.println("Hello, World!");
}

// 也支持实例 main 方法
class HelloWorld {
    void main() {
        System.out.println("Hello without static!");
    }
}

// 隐式类转换
// 上面的 void main() 会被编译器转换为：
final class HelloWorld {
    private HelloWorld() {}  // 私有构造器
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

### 9. Flexible Constructor Bodies (JEP 513)

```java
// 在构造器中，允许在 super() 或 this() 之前执行语句 (JDK 25 正式)
class Point {
    private final int x, y;
    private final String description;

    // 旧写法：需要辅助方法或静态工厂
    public Point(int x, int y) {
        this.x = x;
        this.y = y;
        this.description = validate(x, y);
    }

    // 新写法 (JDK 25+)
    public Point(int x, int y) {
        // Prologue: 在 super() 之前执行的语句
        if (x < 0 || y < 0) {
            throw new IllegalArgumentException("Coordinates must be non-negative");
        }
        String desc = "Point(" + x + "," + y + ")";

        // Constructor invocation
        super();  // 或 this(...)

        // Epilogue: 在 super() 之后执行的语句
        this.x = x;
        this.y = y;
        this.description = desc;
    }
}
```

### 10. Primitive Patterns (JEP 455 → 488 → 507 → 530)

```java
// 原始类型模式匹配 (JDK 23+ 预览，持续到 JDK 26)
// 支持 instanceof 和 switch 使用所有原始类型

// instanceof 原始类型
if (obj instanceof int i) {
    System.out.println("It's an int: " + i);
}

// switch 原始类型模式
String formatted = switch (value) {
    case int i    -> "int %d".formatted(i);
    case long l   -> "long %d".formatted(l);
    case double d -> "double %f".formatted(d);
    case boolean b -> "boolean %b".formatted(b);
    default        -> "unknown type";
};

// 结合守卫语法
String checkRange(Object obj) {
    return switch (obj) {
        case int i when i > 0  -> "positive int";
        case int i when i < 0  -> "negative int";
        case int i             -> "zero";
        default              -> "not an int";
    };
}

// 拆箱原始类型
Number num = 42;
if (num instanceof Integer i) {
    // i 已拆箱，可以直接使用
    System.out.println(i + 1);  // 输出 43
}
```

---

## 4. 时间线

| 年份 | 版本 | 里程碑 |
|------|------|--------|
| **2017** | - | Project Amber 启动 |
| **2018** | JDK 10 | Local-Variable Type Inference (var) |
| **2020** | JDK 14 | Switch Expressions (正式, JEP 361) |
| **2020** | JDK 14 | instanceof Pattern Matching (预览) |
| **2020** | JDK 15 | Text Blocks (正式) |
| **2021** | JDK 16 | Records (正式) |
| **2021** | JDK 16 | instanceof Pattern Matching (正式) |
| **2021** | JDK 17 | Sealed Classes (正式) |
| **2023** | JDK 21 | Record Patterns (正式) |
| **2023** | JDK 21 | Pattern Matching for switch (正式) |
| **2023** | JDK 21 | Unnamed Patterns & Variables (预览, JEP 443) |
| **2023** | JDK 21 | String Templates (第一预览) |
| **2024** | JDK 22 | Unnamed Patterns & Variables (正式, JEP 456) |
| **2024** | JDK 22 | Implicit Classes (第二预览) |
| **2024** | JDK 22 | Flexible Constructor Bodies (第一预览) |
| **2024** | JDK 22 | String Templates (第二预览) |
| **2024** | JDK 23 | Implicit Classes (第三预览, JEP 477) |
| **2024** | JDK 23 | Primitive Patterns (第一预览) |
| **2024** | JDK 23 | String Templates **撤回** |
| **2024** | JDK 23 | Flexible Constructor Bodies (第二预览) |
| **2025** | JDK 24 | Flexible Constructor Bodies (第三预览) |
| **2025** | JDK 24 | Primitive Patterns (第二预览) |
| **2025** | JDK 25 | Flexible Constructor Bodies (正式, JEP 513) |
| **2025** | JDK 25 | Implicit Classes (正式, JEP 512) |
| **2025** | JDK 25 | Module Import Declarations (正式, JEP 511) |
| **2025** | JDK 25 | Primitive Patterns (第三预览, JEP 507) |
| **2026** | JDK 26 | Primitive Patterns (第四预览, JEP 530) |

→ [完整时间线](timeline.md)

---

## 5. 核心贡献者

| 贡献者 | 组织 | 角色 |
|--------|------|------|
| [Brian Goetz](/by-contributor/profiles/brian-goetz.md) | Oracle | 语言架构师，项目领导人 |
| [Gavin Bierman](/by-contributor/profiles/gavin-bierman.md) | Oracle | JLS 编辑，Records, Sealed Classes |
| [Jan Lahoda](/by-contributor/profiles/jan-lahoda.md) | Oracle | javac, 模式匹配实现 |
| Jim Laskey | Oracle | Text Blocks, String Templates |
| Alex Buckley | Oracle | JLS 规范维护 |

---

## 6. 与其他项目的关系

```
┌─────────────────────────────────────────────────────────┐
│                  OpenJDK 项目关系                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   Project Amber ──────► 语言层面改进                     │
│        │                                                │
│        ├─── 配合 ────► Project Valhalla (值类型)         │
│        │                  - Primitive Patterns          │
│        │                  - Record 与 Inline Class      │
│        │                                                │
│        ├─── 配合 ────► Project Loom (虚拟线程)           │
│        │                  - Structured Concurrency      │
│        │                  - 模式匹配用于并发任务         │
│        │                                                │
│        └─── 配合 ────► Project Panama (FFI)             │
│                           - 外部函数的类型安全            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 与 Valhalla 的协同

```
Record (Amber) + Inline Class (Valhalla)
                    ↓
        无需装箱的数据载体
                    ↓
     更高性能的领域建模
```

**Primitive Patterns** 正是 Amber 与 Valhalla 协作的典型例子：
- 当 Valhalla 的值类型最终实现时
- Primitive Patterns 确保模式匹配能无缝处理原始类型和值类型

---

## 7. 语法对比

### 数据类定义

| Java (旧) | Java (Amber) |
|-----------|--------------|
| 50+ 行类定义 | 1 行 `record Point(int x, int y) {}` |
| 手动 equals/hashCode/toString | 自动生成 |
| 手动 getter/accessor | 自动生成 `x()`, `y()` |
| 手动构造器 | 自动生成 |
| 可变对象（需额外工作） | 默认不可变 |

### 类型检查与转换

| Java (旧) | Java (Amber) |
|-----------|--------------|
| `if (x instanceof String) { String s = (String)x; }` | `if (x instanceof String s) { }` |
| 显式类型转换 `(T)obj` | 模式变量自动推断 |
| 多层 if-else 检查 | switch 表达式 + 模式匹配 |
| 运行时发现遗漏的 case | 编译时穷尽性检查 |
| null 需要单独检查 | `case null` 统一处理 |

### Switch 表达式

| Java (旧) | Java (Amber) |
|-----------|--------------|
| 语句形式（statement） | 表达式形式（expression） |
| 需要 `break` 防止 fall-through | `->` 语法无需 break |
| 多个 case 需要分开写 | `case MONDAY, FRIDAY ->` |
| 无法直接赋值给变量 | `int result = switch(...) { ... }` |
| 无法嵌套使用 | 可作为表达式嵌套 |

### 字符串处理

| Java (旧) | Java (Amber) |
|-----------|--------------|
| 字符串连接 `"\n" +` | Text Blocks `"""..."""` |
| 转义字符 `\"` 难以阅读 | 直接使用引号 |
| SQL/JSON 需要外部文件 | 内联多行字符串 |
| `\s` 保留空格 | `\` 取消换行 |

---

## 8. 特性状态说明

### 最近正式发布特性

| 特性 | JEP | 正式版本 | 说明 |
|------|-----|----------|------|
| **Compact Source Files & Instance Main** | JEP 512 | JDK 25 | 简化 Java 入门语法 |
| **Module Import Declarations** | JEP 511 | JDK 25 | 简洁导入模块导出包 |
| **Flexible Constructor Bodies** | JEP 513 | JDK 25 | 构造器中可在 super() 前执行语句 |

### 已撤回特性

| 特性 | JEP | 撤回时间 | 原因 |
|------|-----|----------|------|
| **String Templates** | 430 → 459 → 465 | 2024年6月 | 安全性顾虑，设计需重新评估 |

**String Templates 撤回详情**：
- JDK 21: 第一预览 (JEP 430)
- JDK 22: 第二预览 (JEP 459)
- JDK 23: **撤回** (JEP 465 Closed/Withdrawn)
- 原因：社区反馈对字符串插值的安全性和表达方式存在分歧，需要重新设计

### 预览中特性 (截至 2026年)

| 特性 | 当前 JEP | 目标版本 |
|------|----------|----------|
| **Primitive Patterns** | JEP 530 (第四预览) | JDK 26+ |

---

## 9. 参考资料

### 官方资源
- [Project Amber Official Page](https://openjdk.org/projects/amber/)
- [Amber JEPs Complete List](https://openjdk.org/jeps/?q=amber)

### 已正式发布的 JEP
- [JEP 286](/jeps/language/jep-286.md)
- [JEP 361](/jeps/language/jep-361.md)
- [JEP 378](/jeps/language/jep-378.md)
- [JEP 395](/jeps/language/jep-395.md)
- [JEP 394](/jeps/language/jep-394.md)
- [JEP 441](/jeps/language/jep-441.md)
- [JEP 440](/jeps/language/jep-440.md)
- [JEP 409: Sealed Classes](https://openjdk.org/jeps/409)
- [JEP 456: Unnamed Variables & Patterns](https://openjdk.org/jeps/456)

### 预览中 / 撤回的 JEP
- [JEP 447: Statements before super (Preview)](https://openjdk.org/jeps/447)
- [JEP 463](/jeps/language/jep-463.md)
- [JEP 455](/jeps/tools/jep-455.md)
- [JEP 430](/jeps/language/jep-430.md)
- [JEP 465: String Templates (Third Preview - Withdrawn)](https://openjdk.org/jeps/465)

→ [相关主题: Records](../records/) | [模式匹配](../patterns/) | [语法演进](../../language/syntax/)
