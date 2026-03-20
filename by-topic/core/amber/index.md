# Project Amber

Java 语言特性演进项目：让 Java 更简洁、更安全、更易表达。

[← 返回核心平台](../)

---

## TL;DR

**Project Amber** 是 OpenJDK 的语言特性项目，专注于：
- **更简洁的语法** - 减少样板代码
- **更安全的类型** - 模式匹配、密封类
- **更易表达** - Record、switch 表达式

**状态**: 持续交付中 (2017-至今)，多个特性已正式发布

---

## 项目概述

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
| **Lambda Parameter Names** | JDK 11 | JEP 323 |
| **Switch Expressions** | JDK 14 | JEP 361 |
| **Text Blocks** | JDK 15 | JEP 378 |
| **Records** | JDK 16 | JEP 395 |
| **Pattern Matching for instanceof** | JDK 16 | JEP 394 |
| **Sealed Classes** | JDK 17 | JEP 409 |
| **Pattern Matching for switch** | JDK 21 | JEP 441 |
| **Record Patterns** | JDK 21 | JEP 440 |
| **String Templates** | (撤回) | JEP 430 |
| **Unnamed Patterns & Variables** | JDK 21 | JEP 443 |
| **Implicit Classes** | JDK 21+ | JEP 463 |
| **Flexible Constructor Bodies** | JDK 22 | JEP 448 |
| **Statements before super** | JDK 22 | JEP 447 |
| **Primitive Patterns** | JDK 26 | JEP 455 |

---

## 主要特性详解

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
```

### 3. Sealed Classes (JEP 409)

```java
// 定义密封类
public sealed interface Shape
    permits Circle, Rectangle, Square {
    double area();
}

// 实现类必须是 sealed 或 final
public final record Circle(double radius) implements Shape {
    public double area() { return Math.PI * radius * radius; }
}

public final record Rectangle(double width, double height) implements Shape {
    public double area() { return width * height; }
}

// 编译器检查穷尽性
String describe(Shape s) {
    return switch (s) {
        case Circle c -> "Circle with radius " + c.radius();
        case Rectangle r -> "Rectangle " + r.width() + "x" + r.height();
        // 编译器会检查是否覆盖所有 permits
    };
}
```

### 4. Text Blocks (JEP 378)

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
```

### 5. Switch Expressions (JEP 361)

```java
// 旧写法
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

// 新写法
int result = switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> 6;
    case TUESDAY               -> 7;
    default                   -> 0;
};
```

### 6. Unnamed Patterns & Variables (JEP 443)

```java
// 使用 _ 忽略不关心的值
// 旧写法
if (obj instanceof String s && s.length() > 0) {
    System.out.println(s);
}

// 新写法 - 忽略长度检查
if (obj instanceof String _ && obj.hashCode() != 0) {
    System.out.println("Non-empty string");
}

// Lambda 中忽略参数
stream.map(_ -> "constant")  // 所有元素映射为 "constant"

// Record 模式中忽略字段
if (obj instanceof Point(int x, _)) {
    // 只关心 x 坐标
}
```

### 7. Implicit Classes (JEP 463)

```java
// 单文件程序无需类声明
// main.java
void main() {
    System.out.println("Hello, World!");
}

// 等价于
// 隐式类生成
final class main {
    private main() {}  // 私有构造器
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

### 8. Primitive Patterns (JEP 455)

```java
// 原始类型模式匹配 (JDK 26)
switch (value) {
    case int i    -> "Integer: " + i;
    case long l   -> "Long: " + l;
    case double d -> "Double: " + d;
    default       -> "Other";
}

// 结合泛型特化
<T> String describe(T value) {
    return switch (value) {
        case int i    -> "int " + i;
        case String s -> "String " + s;
        case null     -> "null";
        default       -> "unknown";
    };
}
```

---

## 时间线

| 年份 | 版本 | 里程碑 |
|------|------|--------|
| **2017** | - | Project Amber 启动 |
| **2018** | JDK 10 | Local-Variable Type Inference (var) |
| **2019** | JDK 14 | Switch Expressions (预览) |
| **2020** | JDK 14 | instanceof Pattern Matching (预览) |
| **2020** | JDK 15 | Text Blocks (正式) |
| **2021** | JDK 16 | Records (正式) |
| **2021** | JDK 16 | instanceof Pattern Matching (正式) |
| **2021** | JDK 17 | Sealed Classes (正式) |
| **2023** | JDK 21 | Record Patterns (正式) |
| **2023** | JDK 21 | Pattern Matching for switch (正式) |
| **2023** | JDK 21 | Unnamed Patterns & Variables |
| **2024** | JDK 22 | Flexible Constructor Bodies |
| **2025** | JDK 26 | Primitive Patterns |

→ [完整时间线](timeline.md)

---

## 核心贡献者

| 贡献者 | 组织 | 角色 |
|--------|------|------|
| [Brian Goetz](/by-contributor/profiles/brian-goetz.md) | Oracle | 语言架构师，项目领导人 |
| [Gavin Bierman](/by-contributor/profiles/gavin-bierman.md) | Oracle | Records, Sealed Classes |
| [Jan Lahoda](/by-contributor/profiles/jan-lahoda.md) | Oracle | javac, 模式匹配实现 |
| Jim Laskey | Oracle | Text Blocks, String Templates |
| Alex Buckley | Oracle | JLS 规范维护 |

---

## 与其他项目的关系

```
┌─────────────────────────────────────────────────────────┐
│                  OpenJDK 项目关系                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   Project Amber ──────► 语言层面改进                     │
│        │                                                │
│        ├─── 配合 ────► Project Valhalla (值类型)         │
│        │                  - 模式匹配支持值类型            │
│        │                  - Record 与 Inline Class      │
│        │                                                │
│        ├─── 配合 ────► Project Loom (虚拟线程)           │
│        │                  - 结构化并发                  │
│        │                                                │
│        └─── 配合 ────► Project Panama (FFI)             │
│                           - 外部函数的类型安全            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 语法对比

### 数据类

| Java (旧) | Java (Amber) |
|-----------|--------------|
| 50+ 行类 | 1 行 record |
| 手动 equals/hashCode | 自动生成 |
| 手动 getter/accessor | 自动生成 |

### 类型检查

| Java (旧) | Java (Amber) |
|-----------|--------------|
| `if (x instanceof T) { T t = (T)x; }` | `if (x instanceof T t) { }` |
| 多层 if-else 检查 | switch 表达式 + 模式匹配 |
| 运行时类型错误 | 编译时穷尽性检查 |

---

## 参考资料

- [Project Amber Official Page](https://openjdk.org/projects/amber/)
- [JEP 395: Records](https://openjdk.org/jeps/395)
- [JEP 394: Pattern Matching for instanceof](https://openjdk.org/jeps/394)
- [JEP 441: Pattern Matching for switch](https://openjdk.org/jeps/441)
- [JEP 409: Sealed Classes](https://openjdk.org/jeps/409)

→ [相关主题: Records](../records/) | [模式匹配](../patterns/) | [语法演进](../../language/syntax/)
