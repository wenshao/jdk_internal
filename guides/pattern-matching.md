# Java Pattern Matching 完整指南

> 模式匹配 (Pattern Matching) 是 Java 语言现代化的核心特性之一，从 JDK 16 到 JDK 26 逐步演进，根本性地改变了 Java 的类型检查、数据提取和条件分支的编码方式。

---
## 目录

1. [概述与演进历史](#1-概述与演进历史)
2. [instanceof 模式 (JDK 16)](#2-instanceof-模式-jdk-16)
3. [switch 模式 (JDK 21)](#3-switch-模式-jdk-21)
4. [Record 模式 (JDK 21)](#4-record-模式-jdk-21)
5. [Unnamed 模式 (JDK 22)](#5-unnamed-模式-jdk-22)
6. [Primitive 模式 (JDK 25-26 Preview)](#6-primitive-模式-jdk-25-26-preview)
7. [与 Sealed Classes 配合](#7-与-sealed-classes-配合)
8. [实际应用](#8-实际应用)
9. [最佳实践与常见陷阱](#9-最佳实践与常见陷阱)
10. [相关资源](#10-相关资源)

---

## 1. 概述与演进历史

模式匹配让 Java 从"先判断类型，再手动转换"的繁琐模式，演进到"声明式地匹配并提取数据"的现代风格。

### 演进时间线

| 版本 | 特性 | JEP | 状态 |
|------|------|-----|------|
| JDK 16 | instanceof 模式匹配 | JEP 394 | Final |
| JDK 21 | switch 模式匹配 | JEP 441 | Final |
| JDK 21 | Record Patterns (Record 解构模式) | JEP 440 | Final |
| JDK 22 | Unnamed Variables & Patterns (未命名模式) | JEP 456 | Final |
| JDK 23 | Primitive Types in Patterns (1st Preview) | JEP 455 | Preview |
| JDK 24 | Primitive Types in Patterns (2nd Preview) | JEP 488 | Preview |
| JDK 25 | Primitive Types in Patterns (3rd Preview) | JEP 510 | Preview |
| JDK 26 | Primitive Types in Patterns (4th Preview) | JEP 530 | Preview |

### 核心概念

**模式 (Pattern)** 是一个"测试 + 提取"的组合结构：
- **测试 (Test)**: 判断目标值是否匹配某种结构
- **提取 (Extraction)**: 如果匹配，将目标值的部分数据绑定到新变量

```java
// "obj instanceof String s" 就是一个模式
// 测试: obj 是不是 String?
// 提取: 如果是，绑定为变量 s
if (obj instanceof String s) {
    // s 可以直接使用，无需强转
}
```

---

## 2. instanceof 模式 (JDK 16)

> JEP 394: Pattern Matching for instanceof — JDK 16 正式发布

### 2.1 基本语法

传统写法需要先 instanceof 判断，再手动强转 (cast)：

```java
// 传统写法 (JDK 15 及之前)
if (obj instanceof String) {
    String s = (String) obj;    // 冗余的强转
    System.out.println(s.length());
}
```

模式匹配将类型测试和变量绑定合二为一：

```java
// 模式匹配写法 (JDK 16+)
if (obj instanceof String s) {
    System.out.println(s.length());  // s 已经是 String 类型
}
```

### 2.2 流作用域 (Flow Scoping)

模式变量 (pattern variable) 的作用域由编译器的"确定性赋值分析"(definite assignment) 决定，而不是简单的词法作用域。变量只在编译器能证明匹配成功的区域内可用。

```java
// 流作用域示例
if (obj instanceof String s) {
    // s 在这里可用——因为条件为 true 意味着匹配成功
    System.out.println(s.toUpperCase());
}
// s 在这里不可用——因为不确定是否匹配

// 取反时，变量作用域在 else 分支
if (!(obj instanceof String s)) {
    // s 在这里不可用
    return;
}
// s 在这里可用！因为 if 已经 return，走到这里意味着 obj 是 String
System.out.println(s.toLowerCase());
```

**与 && 和 || 的交互：**

```java
// && 右侧可以使用模式变量（短路求值保证匹配成功）
if (obj instanceof String s && s.length() > 5) {
    System.out.println("Long string: " + s);
}

// || 右侧不能使用模式变量（短路求值不保证匹配）
// 编译错误:
// if (obj instanceof String s || s.length() > 5) { ... }
```

### 2.3 与 equals() 的配合

模式匹配极大简化了 `equals()` 方法的实现：

```java
public class Point {
    private final int x, y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    // 传统写法
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (!(obj instanceof Point)) return false;
        Point other = (Point) obj;
        return this.x == other.x && this.y == other.y;
    }

    // 模式匹配写法
    @Override
    public boolean equals(Object obj) {
        return obj instanceof Point(int ox, int oy)  // JDK 21+ Record Pattern
               && this.x == ox && this.y == oy;
        // 如果 Point 不是 record，可以用:
        // return obj instanceof Point p
        //        && this.x == p.x && this.y == p.y;
    }
}
```

### 2.4 多条件组合

```java
public String describe(Object obj) {
    if (obj instanceof Integer i && i > 0) {
        return "正整数: " + i;
    } else if (obj instanceof Integer i && i < 0) {
        return "负整数: " + i;
    } else if (obj instanceof String s && !s.isBlank()) {
        return "非空字符串: " + s;
    } else if (obj instanceof List<?> list && !list.isEmpty()) {
        return "非空列表，大小: " + list.size();
    } else {
        return "其他: " + obj;
    }
}
```

---

## 3. switch 模式 (JDK 21)

> JEP 441: Pattern Matching for switch — JDK 21 正式发布

switch 模式匹配是 Java 模式匹配最强大的特性。它将 switch 从一个简单的值选择器提升为一个通用的模式匹配结构。

### 3.1 类型模式 (Type Pattern)

```java
// 用 switch 替代 if-else instanceof 链
public String format(Object obj) {
    return switch (obj) {
        case Integer i  -> String.format("整数: %,d", i);
        case Long l     -> String.format("长整数: %,d", l);
        case Double d   -> String.format("浮点数: %.2f", d);
        case String s   -> String.format("字符串: \"%s\" (长度=%d)", s, s.length());
        case int[] arr  -> "整数数组, 长度=" + arr.length;
        case null       -> "null";
        default         -> "未知类型: " + obj.getClass().getName();
    };
}
```

### 3.2 守卫模式 (Guarded Pattern, when)

`when` 关键字在模式之后添加额外的布尔条件 (guard)：

```java
public String classifyTemperature(Object reading) {
    return switch (reading) {
        case Double d when d < -40   -> "极寒 (Extreme Cold)";
        case Double d when d < 0     -> "零下 (Below Freezing)";
        case Double d when d < 15    -> "寒冷 (Cold)";
        case Double d when d < 25    -> "舒适 (Comfortable)";
        case Double d when d < 35    -> "炎热 (Hot)";
        case Double d               -> "极热 (Extreme Heat): " + d;
        case String s               -> "文本读数: " + s;
        case null                   -> "无读数";
        default                     -> "未知格式";
    };
}
```

**注意顺序**: 带 `when` 守卫的 case 必须出现在同类型无守卫的 case 之前，否则无守卫的 case 会先匹配：

```java
// 正确顺序
case String s when s.isEmpty() -> "空字符串";
case String s                  -> "字符串: " + s;

// 编译错误——第一个 case 已经匹配所有 String，第二个不可达
// case String s                  -> "字符串: " + s;
// case String s when s.isEmpty() -> "空字符串";  // 不可达
```

### 3.3 null 处理

传统 switch 遇到 null 会抛 NullPointerException。模式匹配 switch 允许显式处理 null：

```java
public String process(String input) {
    return switch (input) {
        case null                       -> "输入为 null";
        case String s when s.isBlank()  -> "输入为空白";
        case String s                   -> "输入: " + s;
    };
}

// null 也可以和 default 合并
return switch (input) {
    case String s when s.length() > 10 -> "长字符串";
    case String s when !s.isBlank()    -> "普通字符串";
    case null, default                 -> "null 或空白";
};
```

### 3.4 穷举性 (Exhaustiveness)

当 switch 作为表达式 (expression) 或对 sealed 类型做 switch 时，编译器要求穷举 (exhaustive) 所有可能：

```java
// 对 Object 做 switch 必须有 default
String result = switch (obj) {
    case String s  -> s;
    case Integer i -> i.toString();
    // 编译错误：缺少 default，没有穷举所有可能
};

// 对 sealed 类型做 switch 不需要 default (见第 7 节)
sealed interface Shape permits Circle, Rectangle, Triangle {}

String name = switch (shape) {
    case Circle c    -> "圆形";
    case Rectangle r -> "矩形";
    case Triangle t  -> "三角形";
    // 不需要 default——编译器知道这三个子类已穷举
};
```

### 3.5 switch 模式中的 Dominance (支配关系)

编译器检查 case 之间的支配关系 (dominance)，防止不可达的分支：

```java
// 编译错误：case Object o 支配了后续所有 case
switch (obj) {
    case Object o   -> "任意对象";   // 匹配一切
    case String s   -> "字符串";     // 不可达！
    case Integer i  -> "整数";       // 不可达！
}

// 正确：更具体的模式放前面
switch (obj) {
    case String s   -> "字符串";
    case Integer i  -> "整数";
    case Object o   -> "其他: " + o;
}
```

### 3.6 switch 表达式 vs 语句

```java
// switch 表达式 (expression) - 有返回值
int result = switch (obj) {
    case Integer i -> i * 2;
    case String s  -> Integer.parseInt(s);
    default        -> 0;
};

// switch 语句 (statement) - 无返回值，可以用 break、continue、return
switch (command) {
    case "quit", "exit" -> System.exit(0);
    case String s when s.startsWith("echo ") -> {
        String msg = s.substring(5);
        System.out.println(msg);
    }
    case null, default -> System.out.println("Unknown command");
}
```

---

## 4. Record 模式 (JDK 21)

> JEP 440: Record Patterns — JDK 21 正式发布

Record 模式 (Record Pattern) 允许直接解构 (deconstruct) record 的组件 (component)，而无需调用访问器方法。

### 4.1 基本解构

```java
record Point(int x, int y) {}

Object obj = new Point(3, 4);

// 传统写法: instanceof + 访问器
if (obj instanceof Point p) {
    int x = p.x();
    int y = p.y();
    System.out.println("坐标: (" + x + ", " + y + ")");
}

// Record 模式: 直接解构
if (obj instanceof Point(int x, int y)) {
    System.out.println("坐标: (" + x + ", " + y + ")");
}

// 在 switch 中使用
String desc = switch (obj) {
    case Point(int x, int y) when x == 0 && y == 0 -> "原点";
    case Point(int x, int y) when x == 0           -> "Y轴上, y=" + y;
    case Point(int x, int y) when y == 0           -> "X轴上, x=" + x;
    case Point(int x, int y)                       -> "点(" + x + ", " + y + ")";
    default                                         -> "不是点";
};
```

### 4.2 嵌套解构 (Nested Deconstruction)

Record 模式可以嵌套，一次性解构多层结构：

```java
record Point(int x, int y) {}
record Line(Point start, Point end) {}
record Rectangle(Point topLeft, Point bottomRight) {}

Object shape = new Rectangle(new Point(0, 10), new Point(20, 0));

// 嵌套解构——一步到位提取所有坐标
if (shape instanceof Rectangle(Point(int x1, int y1), Point(int x2, int y2))) {
    int width = Math.abs(x2 - x1);
    int height = Math.abs(y2 - y1);
    System.out.printf("矩形: 宽=%d, 高=%d, 面积=%d%n", width, height, width * height);
}

// 在 switch 中嵌套解构
String describe(Object shape) {
    return switch (shape) {
        case Line(Point(int x1, int y1), Point(int x2, int y2)) -> {
            double length = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
            yield String.format("线段长度: %.2f", length);
        }
        case Rectangle(Point(int x1, int y1), Point(int x2, int y2)) -> {
            int area = Math.abs(x2 - x1) * Math.abs(y2 - y1);
            yield "矩形面积: " + area;
        }
        default -> "未知图形";
    };
}
```

### 4.3 泛型 Record 解构

Record 模式支持泛型 record 的解构，编译器自动推断类型参数：

```java
record Pair<A, B>(A first, B second) {}
record Result<T>(T value, String error) {}

Object obj = new Pair<>("hello", 42);

// 泛型 record 解构
if (obj instanceof Pair<String, Integer>(String s, Integer i)) {
    System.out.println(s + " -> " + i);
}

// 泛型嵌套
record Box<T>(T content) {}
Object box = new Box<>(new Pair<>("key", 100));

if (box instanceof Box<Pair<String, Integer>>(Pair<String, Integer>(String k, Integer v))) {
    System.out.println(k + " = " + v);
}

// 在 switch 中使用
Object result = new Result<>("success data", null);
String message = switch (result) {
    case Result(var value, String err) when err != null -> "错误: " + err;
    case Result(var value, var err)                     -> "成功: " + value;
    default                                             -> "未知";
};
```

### 4.4 var 在 Record 模式中的使用

可以用 `var` 让编译器推断组件类型：

```java
record Point(int x, int y) {}

// 用 var 代替显式类型
if (obj instanceof Point(var x, var y)) {
    // x 和 y 被推断为 int
    System.out.println(x + y);
}
```

---

## 5. Unnamed 模式 (JDK 22)

> JEP 456: Unnamed Variables & Patterns — JDK 22 正式发布

当你不需要使用某个变量或组件时，可以用 `_` (下划线) 作为占位符，明确表示"这个值我不关心"。

### 5.1 未命名变量 (Unnamed Variable)

```java
// 不需要异常变量
try {
    int num = Integer.parseInt(input);
} catch (NumberFormatException _) {
    System.out.println("无效数字");
}

// 不需要 lambda 参数
Map<String, List<String>> groups = items.stream()
    .collect(Collectors.groupingBy(
        Item::category,
        Collectors.mapping(Item::name, Collectors.toList())
    ));
groups.forEach((_, values) -> System.out.println(values));

// 不需要 for-each 变量 (只关心计数)
int count = 0;
for (var _ : collection) {
    count++;
}

// 多个未使用的变量
try (var _ = ScopedValue.where(USER, currentUser).call(() -> {
    // ...
    return null;
})) {}
```

### 5.2 未命名模式 (Unnamed Pattern) 在 Record 解构中

```java
record Point(int x, int y) {}
record Line(Point start, Point end) {}

// 只关心 x 坐标，忽略 y
if (obj instanceof Point(int x, _)) {
    System.out.println("x = " + x);
}

// 只关心起点的 x，忽略其他所有
if (obj instanceof Line(Point(int startX, _), _)) {
    System.out.println("起点 x = " + startX);
}

// 在 switch 中使用
record Result<T>(T value, int code, String message) {}

String summary = switch (result) {
    case Result(var v, 200, _)    -> "成功: " + v;
    case Result(_, 404, _)        -> "未找到";
    case Result(_, 500, var msg)  -> "服务器错误: " + msg;
    case Result(_, var code, _)   -> "状态码: " + code;
};
```

### 5.3 未命名模式变量 (Unnamed Pattern Variable) 在 switch 中

```java
// 只需要匹配类型，不需要使用绑定的变量
switch (obj) {
    case Integer _ -> System.out.println("是整数");
    case String _  -> System.out.println("是字符串");
    case List<?> _ -> System.out.println("是列表");
    default        -> System.out.println("其他");
}
```

---

## 6. Primitive 模式 (JDK 25-26 Preview)

> JEP 455/488/510/530: Primitive Types in Patterns — Preview 特性

原始类型模式 (Primitive Pattern) 扩展了模式匹配对 `int`, `long`, `double`, `boolean` 等原始类型的支持。

### 6.1 instanceof 支持原始类型

```java
// 安全的窄化转换 (narrowing conversion)
long bigNumber = 42L;
if (bigNumber instanceof int i) {
    // 只有当 bigNumber 的值在 int 范围内时才匹配
    System.out.println("可以安全转为 int: " + i);
}

long overflow = 3_000_000_000L;
if (overflow instanceof int i) {
    // 不会执行——值超出 int 范围
} else {
    System.out.println("超出 int 范围");
}

// 对 Number 拆箱 + 窄化
Object obj = 42;  // 自动装箱为 Integer
if (obj instanceof int i) {
    System.out.println("int 值: " + i);
}

// double 到 int 的安全转换
double d = 42.0;
if (d instanceof int i) {
    // 只有当 d 没有小数部分且在 int 范围内时匹配
    System.out.println("可以转为 int: " + i);
}

double pi = 3.14;
if (pi instanceof int i) {
    // 不匹配——有小数部分
}
```

### 6.2 switch 支持原始类型

```java
// 对 int 值做精确匹配 (不需要装箱为 Integer)
int statusCode = 404;
String message = switch (statusCode) {
    case 200 -> "OK";
    case 301 -> "Moved Permanently";
    case 400 -> "Bad Request";
    case 404 -> "Not Found";
    case 500 -> "Internal Server Error";
    default  -> "Unknown: " + statusCode;
};

// 对 long 值做 switch (之前 switch 不支持 long)
long fileSize = 1_500_000L;
String category = switch (fileSize) {
    case long s when s < 1024        -> "tiny";
    case long s when s < 1024 * 1024 -> "small";
    case long s when s < 1024 * 1024 * 1024 -> "medium";
    case long s                      -> "large (" + s / (1024 * 1024) + " MB)";
};

// 对 boolean 做 switch
boolean enabled = true;
String label = switch (enabled) {
    case true  -> "已启用";
    case false -> "已禁用";
};

// 混合原始类型和引用类型模式
record Config(String key, Object value) {}

String describeValue(Object val) {
    return switch (val) {
        case int i    -> "int: " + i;
        case long l   -> "long: " + l;
        case double d -> "double: " + d;
        case boolean b -> b ? "true" : "false";
        case String s -> "string: \"" + s + "\"";
        case null     -> "null";
        default       -> "object: " + val;
    };
}
```

### 6.3 在 Record 模式中使用原始类型

```java
record Measurement(String unit, double value) {}

String classify(Object obj) {
    return switch (obj) {
        // 解构 record 并对原始类型组件做模式匹配
        case Measurement(var unit, double v) when v instanceof int i ->
            unit + ": 精确整数值 " + i;
        case Measurement(String unit, double v) when v < 0 ->
            unit + ": 负值 " + v;
        case Measurement(String unit, double v) ->
            unit + ": " + v;
        default -> "未知";
    };
}
```

**注意**: Primitive 模式在 JDK 25-26 仍然是 Preview 特性，需要 `--enable-preview` 编译和运行。

---

## 7. 与 Sealed Classes 配合

模式匹配与密封类 (Sealed Classes, JEP 409, JDK 17) 配合使用时，编译器可以进行穷举性检查 (exhaustiveness check)，形成代数数据类型 (ADT, Algebraic Data Type) 模式。

### 7.1 基本的 Sealed + Switch

```java
// 定义密封层次结构 (ADT)
sealed interface Shape permits Circle, Rectangle, Triangle {}
record Circle(double radius) implements Shape {}
record Rectangle(double width, double height) implements Shape {}
record Triangle(double a, double b, double c) implements Shape {}

// switch 穷举——不需要 default
double area(Shape shape) {
    return switch (shape) {
        case Circle(double r)                -> Math.PI * r * r;
        case Rectangle(double w, double h)   -> w * h;
        case Triangle(double a, double b, double c) -> {
            double s = (a + b + c) / 2;
            yield Math.sqrt(s * (s - a) * (s - b) * (s - c));  // 海伦公式
        }
    };
    // 如果以后新增 Shape 的子类，编译器会报错要求更新这个 switch
}

String describe(Shape shape) {
    return switch (shape) {
        case Circle(double r) when r > 100   -> "大圆 (半径=" + r + ")";
        case Circle(double r)                -> "圆 (半径=" + r + ")";
        case Rectangle(double w, double h) when w == h -> "正方形 (边长=" + w + ")";
        case Rectangle(double w, double h)   -> "矩形 (" + w + "x" + h + ")";
        case Triangle(double a, double b, double c)
            when a == b && b == c            -> "等边三角形 (边长=" + a + ")";
        case Triangle(_, _, _)               -> "三角形";
    };
}
```

### 7.2 多层密封结构

```java
sealed interface Expr permits Literal, BinOp, UnaryOp, Variable {}
record Literal(double value) implements Expr {}
record Variable(String name) implements Expr {}
record BinOp(Expr left, String op, Expr right) implements Expr {}
record UnaryOp(String op, Expr operand) implements Expr {}

// 嵌套解构 + 穷举 switch
double evaluate(Expr expr, Map<String, Double> env) {
    return switch (expr) {
        case Literal(double v) -> v;
        case Variable(String name) -> {
            Double val = env.get(name);
            if (val == null) throw new IllegalArgumentException("未定义变量: " + name);
            yield val;
        }
        case BinOp(var left, String op, var right) -> {
            double l = evaluate(left, env);
            double r = evaluate(right, env);
            yield switch (op) {
                case "+" -> l + r;
                case "-" -> l - r;
                case "*" -> l * r;
                case "/" -> {
                    if (r == 0) throw new ArithmeticException("除以零");
                    yield l / r;
                }
                default -> throw new IllegalArgumentException("未知运算符: " + op);
            };
        }
        case UnaryOp(String op, var operand) -> switch (op) {
            case "-" -> -evaluate(operand, env);
            case "+" ->  evaluate(operand, env);
            default  -> throw new IllegalArgumentException("未知运算符: " + op);
        };
    };
}
```

### 7.3 编译时安全性

密封类 + 穷举 switch 最大的价值是**编译时安全性**——当你新增一个子类时，编译器会强制你更新所有相关的 switch：

```java
// 如果新增一个 Shape 子类:
// record Pentagon(double side) implements Shape {}
//
// 编译器会在所有 switch(shape) 处报错:
// "the switch expression does not cover all possible input values"
// 这比运行时 default + 异常要安全得多
```

---

## 8. 实际应用

### 8.1 JSON AST 处理

```java
// 定义 JSON AST (抽象语法树)
sealed interface JsonValue permits JsonNull, JsonBool, JsonNumber, JsonString,
                                   JsonArray, JsonObject {}
record JsonNull() implements JsonValue {}
record JsonBool(boolean value) implements JsonValue {}
record JsonNumber(double value) implements JsonValue {}
record JsonString(String value) implements JsonValue {}
record JsonArray(List<JsonValue> elements) implements JsonValue {}
record JsonObject(Map<String, JsonValue> fields) implements JsonValue {}

// JSON 序列化 (pretty print)
String toJson(JsonValue value) {
    return switch (value) {
        case JsonNull()       -> "null";
        case JsonBool(true)   -> "true";
        case JsonBool(false)  -> "false";
        case JsonNumber(double d) -> {
            // 整数值不输出小数点
            yield d == Math.floor(d) ? String.valueOf((long) d) : String.valueOf(d);
        }
        case JsonString(String s) -> "\"" + escape(s) + "\"";
        case JsonArray(List<JsonValue> elems) -> {
            String items = elems.stream()
                .map(this::toJson)
                .collect(Collectors.joining(", "));
            yield "[" + items + "]";
        }
        case JsonObject(Map<String, JsonValue> fields) -> {
            String entries = fields.entrySet().stream()
                .map(e -> "\"" + escape(e.getKey()) + "\": " + toJson(e.getValue()))
                .collect(Collectors.joining(", "));
            yield "{" + entries + "}";
        }
    };
}

// 安全地提取嵌套值
Optional<String> getStringField(JsonValue json, String fieldName) {
    return switch (json) {
        case JsonObject(var fields)
            when fields.get(fieldName) instanceof JsonString(String s) ->
                Optional.of(s);
        default -> Optional.empty();
    };
}

// 深度提取 (支持路径如 "user.address.city")
Optional<JsonValue> getPath(JsonValue json, String... path) {
    JsonValue current = json;
    for (String key : path) {
        if (current instanceof JsonObject(var fields) && fields.containsKey(key)) {
            current = fields.get(key);
        } else {
            return Optional.empty();
        }
    }
    return Optional.of(current);
}
```

### 8.2 表达式求值器 (Expression Evaluator)

```java
sealed interface Expr permits Num, Add, Mul, Neg, Let, Var {}
record Num(double value) implements Expr {}
record Add(Expr left, Expr right) implements Expr {}
record Mul(Expr left, Expr right) implements Expr {}
record Neg(Expr operand) implements Expr {}
record Var(String name) implements Expr {}
record Let(String name, Expr value, Expr body) implements Expr {}

// 求值器
double eval(Expr expr, Map<String, Double> env) {
    return switch (expr) {
        case Num(double v)             -> v;
        case Add(var l, var r)         -> eval(l, env) + eval(r, env);
        case Mul(var l, var r)         -> eval(l, env) * eval(r, env);
        case Neg(var e)                -> -eval(e, env);
        case Var(String name)          -> env.getOrDefault(name, 0.0);
        case Let(String name, var val, var body) -> {
            var newEnv = new HashMap<>(env);
            newEnv.put(name, eval(val, env));
            yield eval(body, newEnv);
        }
    };
}

// 表达式优化 (常量折叠 constant folding)
Expr optimize(Expr expr) {
    return switch (expr) {
        // 0 + x = x
        case Add(Num(0.0), var right)  -> optimize(right);
        // x + 0 = x
        case Add(var left, Num(0.0))   -> optimize(left);
        // 0 * x = 0
        case Mul(Num(0.0), _)          -> new Num(0);
        // x * 0 = 0
        case Mul(_, Num(0.0))          -> new Num(0);
        // 1 * x = x
        case Mul(Num(1.0), var right)  -> optimize(right);
        // x * 1 = x
        case Mul(var left, Num(1.0))   -> optimize(left);
        // --x = x
        case Neg(Neg(var e))           -> optimize(e);
        // 两个常量直接计算
        case Add(Num(double l), Num(double r)) -> new Num(l + r);
        case Mul(Num(double l), Num(double r)) -> new Num(l * r);
        case Neg(Num(double v))        -> new Num(-v);
        // 递归优化子表达式
        case Add(var l, var r)         -> new Add(optimize(l), optimize(r));
        case Mul(var l, var r)         -> new Mul(optimize(l), optimize(r));
        case Neg(var e)                -> new Neg(optimize(e));
        // 叶子节点不变
        case Num _, Var _, Let _       -> expr;
    };
}

// Pretty print
String prettyPrint(Expr expr) {
    return switch (expr) {
        case Num(double v)      -> v == Math.floor(v) ? String.valueOf((long) v) : String.valueOf(v);
        case Var(String name)   -> name;
        case Add(var l, var r)  -> "(" + prettyPrint(l) + " + " + prettyPrint(r) + ")";
        case Mul(var l, var r)  -> "(" + prettyPrint(l) + " * " + prettyPrint(r) + ")";
        case Neg(var e)         -> "-" + prettyPrint(e);
        case Let(String n, var v, var b) ->
            "let " + n + " = " + prettyPrint(v) + " in " + prettyPrint(b);
    };
}
```

### 8.3 状态机 (State Machine)

```java
// HTTP 连接状态机
sealed interface ConnState permits Idle, Connecting, Connected, Failed, Closed {}
record Idle() implements ConnState {}
record Connecting(String host, int port) implements ConnState {}
record Connected(String host, int port, long connectedAt) implements ConnState {}
record Failed(String host, String reason, int retryCount) implements ConnState {}
record Closed(String reason) implements ConnState {}

sealed interface ConnEvent permits Connect, ConnectionEstablished,
                                    ConnectionFailed, Disconnect, Retry {}
record Connect(String host, int port) implements ConnEvent {}
record ConnectionEstablished(long timestamp) implements ConnEvent {}
record ConnectionFailed(String reason) implements ConnEvent {}
record Disconnect(String reason) implements ConnEvent {}
record Retry() implements ConnEvent {}

// 状态转换函数 (纯函数，没有副作用)
ConnState transition(ConnState state, ConnEvent event) {
    return switch (state) {
        case Idle() -> switch (event) {
            case Connect(String host, int port) -> new Connecting(host, port);
            default -> state;  // 忽略非法事件
        };
        case Connecting(String host, int port) -> switch (event) {
            case ConnectionEstablished(long ts) -> new Connected(host, port, ts);
            case ConnectionFailed(String reason) -> new Failed(host, reason, 0);
            default -> state;
        };
        case Connected(String host, _, _) -> switch (event) {
            case Disconnect(String reason) -> new Closed(reason);
            case ConnectionFailed(String reason) -> new Failed(host, reason, 0);
            default -> state;
        };
        case Failed(String host, _, int retries) -> switch (event) {
            case Retry() when retries < 3 -> new Connecting(host, 80);
            case Retry() -> new Closed("max retries exceeded");
            case Disconnect(String reason) -> new Closed(reason);
            default -> state;
        };
        case Closed(_) -> switch (event) {
            case Connect(String host, int port) -> new Connecting(host, port);
            default -> state;
        };
    };
}

// 日志
void logTransition(ConnState from, ConnEvent event, ConnState to) {
    String fromName = switch (from) {
        case Idle()          -> "IDLE";
        case Connecting(_, _) -> "CONNECTING";
        case Connected(_, _, _) -> "CONNECTED";
        case Failed(_, _, _)  -> "FAILED";
        case Closed(_)       -> "CLOSED";
    };
    System.out.printf("[%s] --%s--> [%s]%n",
        fromName, event.getClass().getSimpleName(),
        to.getClass().getSimpleName().toUpperCase());
}
```

### 8.4 访问者模式替代 (Visitor Pattern Replacement)

传统 Visitor 模式需要大量样板代码。模式匹配可以直接替代：

```java
// ---- 传统 Visitor 模式 (大量样板) ----
interface NodeVisitor<T> {
    T visitLiteral(LiteralNode node);
    T visitBinary(BinaryNode node);
    T visitUnary(UnaryNode node);
    T visitCall(CallNode node);
}

interface AstNode {
    <T> T accept(NodeVisitor<T> visitor);
}

// 每个节点类都要实现 accept 方法...
// 每种操作都要创建 Visitor 实现类...

// ---- 模式匹配替代 (简洁直观) ----
sealed interface AstNode permits LiteralNode, BinaryNode, UnaryNode, CallNode {}
record LiteralNode(Object value) implements AstNode {}
record BinaryNode(AstNode left, String op, AstNode right) implements AstNode {}
record UnaryNode(String op, AstNode operand) implements AstNode {}
record CallNode(String function, List<AstNode> args) implements AstNode {}

// 直接用 switch 代替 Visitor——新增操作只需写一个方法
String format(AstNode node) {
    return switch (node) {
        case LiteralNode(Object v) -> v.toString();
        case BinaryNode(var l, String op, var r) ->
            "(" + format(l) + " " + op + " " + format(r) + ")";
        case UnaryNode(String op, var operand) ->
            op + format(operand);
        case CallNode(String fn, List<AstNode> args) -> {
            String argStr = args.stream().map(this::format).collect(Collectors.joining(", "));
            yield fn + "(" + argStr + ")";
        }
    };
}

Set<String> collectVariables(AstNode node) {
    return switch (node) {
        case LiteralNode(String name) when isIdentifier(name) -> Set.of(name);
        case LiteralNode(_)           -> Set.of();
        case BinaryNode(var l, _, var r) -> {
            var vars = new HashSet<>(collectVariables(l));
            vars.addAll(collectVariables(r));
            yield vars;
        }
        case UnaryNode(_, var operand)  -> collectVariables(operand);
        case CallNode(_, List<AstNode> args) -> {
            var vars = new HashSet<String>();
            args.forEach(a -> vars.addAll(collectVariables(a)));
            yield vars;
        }
    };
}
```

**Visitor vs Pattern Matching 对比：**

| 维度 | Visitor 模式 | 模式匹配 |
|------|-------------|---------|
| 新增操作 (operation) | 需要新建 Visitor 类 | 写一个 switch 方法 |
| 新增节点类型 (data variant) | 只改 interface，不改 Visitor | 编译器强制更新所有 switch |
| 样板代码量 | 大量 (accept, visit 方法) | 极少 |
| 类型安全 | 依赖 Visitor 接口约束 | 编译器穷举检查 |
| 适用场景 | 类型层次稳定，操作频繁变化 | 类型和操作都在变化 |

---

## 9. 最佳实践与常见陷阱

### 9.1 最佳实践

**1. 优先使用模式匹配替代手动 instanceof + cast：**

```java
// 推荐
if (obj instanceof String s) { ... }

// 不推荐
if (obj instanceof String) {
    String s = (String) obj;
    ...
}
```

**2. switch 表达式优先于 if-else 链：**

```java
// 推荐：结构清晰，编译器检查穷举
return switch (event) {
    case Click(int x, int y)       -> handleClick(x, y);
    case KeyPress(char c)          -> handleKey(c);
    case Scroll(int delta)         -> handleScroll(delta);
};

// 不推荐：if-else 链，容易遗漏分支
if (event instanceof Click c) { return handleClick(c.x(), c.y()); }
else if (event instanceof KeyPress k) { return handleKey(k.c()); }
else if (event instanceof Scroll s) { return handleScroll(s.delta()); }
else { throw new IllegalArgumentException(); }  // 手动兜底
```

**3. sealed + record + switch 三件套构建 ADT：**

```java
// 定义: sealed interface + record permits
sealed interface Result<T> permits Success, Failure {}
record Success<T>(T value) implements Result<T> {}
record Failure<T>(String error, Exception cause) implements Result<T> {}

// 使用: switch 穷举
<T> T unwrap(Result<T> result) {
    return switch (result) {
        case Success(var value) -> value;
        case Failure(var error, var cause) -> throw new RuntimeException(error, cause);
    };
}
```

**4. 用 `_` 明确表示不关心的变量：**

```java
// 推荐：意图明确
case Point(int x, _) -> "x=" + x;

// 不推荐：引入了不使用的变量
case Point(int x, int y) -> "x=" + x;  // y 未使用
```

**5. guard (`when`) 比嵌套 if 更清晰：**

```java
// 推荐
case String s when s.length() > 100 -> truncate(s);
case String s                       -> s;

// 不推荐
case String s -> {
    if (s.length() > 100) yield truncate(s);
    else yield s;
}
```

### 9.2 常见陷阱

**陷阱 1: case 顺序错误导致不可达分支**

```java
// 编译错误：case Object 支配了后续所有 case
switch (obj) {
    case Object o  -> "object";
    case String s  -> "string";   // 不可达!
}

// 修正：具体类型放前面
switch (obj) {
    case String s  -> "string";
    case Object o  -> "object";
}
```

**陷阱 2: 忘记 null 处理**

```java
// 如果 obj 可能为 null，且没有 case null，switch 会抛 NPE
String result = switch (obj) {    // obj = null 时抛 NullPointerException
    case String s  -> s;
    case Integer i -> i.toString();
    default        -> "other";    // default 不匹配 null!
};

// 修正：显式处理 null
String result = switch (obj) {
    case null       -> "null";
    case String s   -> s;
    case Integer i  -> i.toString();
    default         -> "other";
};

// 或者用 null, default 合并
String result = switch (obj) {
    case String s   -> s;
    case Integer i  -> i.toString();
    case null, default -> "other";
};
```

**陷阱 3: 模式变量作用域误解**

```java
// 编译错误：|| 右侧不能使用左侧的模式变量
if (obj instanceof String s || s.isEmpty()) { }

// 修正：用 && 或 when
if (obj instanceof String s && s.isEmpty()) { }
```

**陷阱 4: switch 中遗忘 yield 关键字**

```java
// 编译错误：多行 case body 必须用 yield 返回值
String result = switch (obj) {
    case String s -> {
        String upper = s.toUpperCase();
        upper;          // 错误！不是合法的语句
    }
    default -> "other";
};

// 修正：使用 yield
String result = switch (obj) {
    case String s -> {
        String upper = s.toUpperCase();
        yield upper;    // 正确
    }
    default -> "other";
};
```

**陷阱 5: Record 模式中的类型不匹配**

```java
record Pair<A, B>(A first, B second) {}

// 编译错误：泛型擦除，运行时无法验证泛型参数
// Object obj = new Pair<>("hello", 42);
// if (obj instanceof Pair<String, String>(var a, var b)) { }  // 不安全

// 正确：使用 raw 类型或通配符
if (obj instanceof Pair<?,?>(var a, var b)) {
    // a 和 b 的类型是 Object
}
```

**陷阱 6: sealed class 新增子类后忘记更新 switch**

这实际上是模式匹配的**优势**而非陷阱——编译器会告诉你哪些 switch 需要更新。但如果你到处写 `default -> throw new AssertionError()`，就失去了这个编译时保障：

```java
// 不推荐：default 吞掉了穷举检查
return switch (shape) {
    case Circle c    -> area(c);
    case Rectangle r -> area(r);
    default -> throw new AssertionError("unexpected shape");
    // 新增 Triangle 时不会编译报错，而是运行时才崩溃
};

// 推荐：不写 default，让编译器检查穷举性
return switch (shape) {
    case Circle c    -> area(c);
    case Rectangle r -> area(r);
    // 新增 Triangle 时编译器立即报错
};
```

---

## 10. 相关资源

- [JEP 394: Pattern Matching for instanceof](https://openjdk.org/jeps/394) (JDK 16, Final)
- [JEP 441: Pattern Matching for switch](https://openjdk.org/jeps/441) (JDK 21, Final)
- [JEP 440: Record Patterns](https://openjdk.org/jeps/440) (JDK 21, Final)
- [JEP 456: Unnamed Variables & Patterns](https://openjdk.org/jeps/456) (JDK 22, Final)
- [JEP 455: Primitive Types in Patterns](https://openjdk.org/jeps/455) (JDK 23, Preview)
- [JEP 530: Primitive Types in Patterns](https://openjdk.org/jeps/530) (JDK 26, 4th Preview)
- [JEP 409: Sealed Classes](https://openjdk.org/jeps/409) (JDK 17, Final)
