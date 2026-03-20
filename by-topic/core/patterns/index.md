# 模式匹配

> Pattern Matching、类型模式、Record 模式、守卫、解构

[← 返回核心平台](../)

---

## 快速概览

```
JDK 1.0 ── JDK 7 ── JDK 10 ── JDK 14 ── JDK 16 ── JDK 17 ── JDK 21
   │        │        │        │        │        │        │
instance  Switch  Var     instanceof  Switch  Record  模式匹配
of       String  类型    模式       表达式   模式    正式版
```

### 核心演进

| 版本 | 特性 | JEP | 说明 |
|------|------|-----|------|
| **JDK 14** | instanceof 模式 | JEP 305 | 预览 |
| **JDK 15** | instanceof 模式 | JEP 375 | 二次预览 |
| **JDK 16** | instanceof 模式 | JEP 394 | 正式版 |
| **JDK 17** | switch 模式 | JEP 406 | 预览 |
| **JDK 18** | switch 模式 | JEP 420 | 二次预览 |
| **JDK 19** | switch 模式 | JEP 427 | 三次预览 |
| **JDK 20** | switch 模式 | JEP 433 | 四次预览 |
| **JDK 21** | switch 模式 | JEP 441 | 正式版 |
| **JDK 19** | Record 模式 | JEP 405 | 预览 |
| **JDK 20** | Record 模式 | JEP 432 | 二次预览 |
| **JDK 21** | Record 模式 | JEP 440 | 正式版 |

---

## 目录

- [类型模式](#类型模式)
- [Switch 模式](#switch-模式)
- [Record 模式](#record-模式)
- [守卫条件](#守卫条件)
- [解构模式](#解构模式)
- [最佳实践](#最佳实践)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 类型模式

### instanceof 类型模式 (JDK 16+)

```java
// JDK 16 之前
Object obj = "Hello";

if (obj instanceof String) {
    String str = (String) obj;  // 需要强制转换
    System.out.println(str.length());
}

// JDK 16+ 类型模式
if (obj instanceof String str) {  // 自动转换
    System.out.println(str.length());  // 直接使用 str
}

// 模式变量的作用域
if (obj instanceof String str && str.length() > 0) {
    System.out.println(str);  // ✅ 可以使用
}

// if (obj instanceof String str || str.length() > 0) { }  // ❌ 编译错误!
```

### 复杂类型模式

```java
// 嵌套类型检查
Object obj = List.of("a", "b", "c");

if (obj instanceof List<?> list && !list.isEmpty()) {
    // list 可以使用
    System.out.println(list.size());
}

// 链式类型模式
if (obj instanceof List<?> list &&
    list.get(0) instanceof String first &&
    first.startsWith("a")) {
    System.out.println("First element starts with 'a'");
}
```

---

## Switch 模式

### Switch 表达式基础

```java
// JDK 14+ Switch 表达式
public String getDayType(Day day) {
    return switch (day) {
        case MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY -> "工作日";
        case SATURDAY, SUNDAY -> "周末";
    };
}

// JDK 17+ Switch 模式匹配
public String describe(Object obj) {
    return switch (obj) {
        case String s -> "字符串: " + s;
        case Integer i -> "整数: " + i;
        case Long l -> "长整数: " + l;
        case Double d -> "浮点数: " + d;
        case null -> "null";
        default -> "其他类型";
    };
}
```

### 模式覆盖检查

```java
// 编译器会检查模式是否完整
public String test(Object obj) {
    return switch (obj) {
        case String s -> "String";
        case Integer i -> "Integer";
        // 编译错误: 模式的覆盖域不是穷尽的
        // 需要添加 default 分支
    };
}

// 穷尽的模式匹配
public sealed interface Shape permits Circle, Rectangle {
    record Circle(double radius) implements Shape { }
    record Rectangle(double width, double height) implements Shape { }
}

public double area(Shape shape) {
    return switch (shape) {
        // 不需要 default - 编译器知道所有情况都已覆盖
        case Circle(double r) -> Math.PI * r * r;
        case Rectangle(double w, double h) -> w * h;
    };
}
```

### Switch 语句 vs 表达式

```java
// Switch 语句 (有副作用)
public void process(Object obj) {
    switch (obj) {
        case String s -> System.out.println("处理字符串: " + s);
        case Integer i -> System.out.println("处理整数: " + i);
        case null, default -> System.out.println("处理其他");
    }
}

// Switch 表达式 (返回值)
public String describe(Object obj) {
    return switch (obj) {
        case String s -> "字符串";
        case Integer i -> "整数";
        case null, default -> "其他";
    };
}

// 使用 yield 返回复杂值
public String detailedDescribe(Object obj) {
    return switch (obj) {
        case String s -> {
            System.out.println("处理字符串");
            yield "字符串: " + s;  // 使用 yield
        }
        case Integer i -> {
            int doubled = i * 2;
            yield "整数 x2: " + doubled;
        }
        default -> "其他";
    };
}
```

---

## Record 模式

### Record 解构

```java
// Record 定义
public record Point(int x, int y) { }
public record Circle(Point center, double radius) { }

// 基础 Record 模式
Object obj = new Point(3, 4);

if (obj instanceof Point(int x, int y)) {
    System.out.println("x=" + x + ", y=" + y);
}

// 嵌套 Record 模式
Object obj2 = new Circle(new Point(1, 2), 5.0);

if (obj2 instanceof Circle(Point(int x, int y), double r)) {
    System.out.println("Circle at (" + x + ", " + y + ") with radius " + r);
}
```

### Switch 中的 Record 模式

```java
// 在 switch 表达式中使用 Record 模式
public double calculate(Object obj) {
    return switch (obj) {
        case Point(int x, int y) -> Math.sqrt(x * x + y * y);
        case Circle(Point(int x, int y), double r) -> Math.PI * r * r;
        case null -> 0;
        default -> throw new IllegalArgumentException("Unknown shape");
    };
}
```

### Record 模式与 var

```java
// 使用 var 简化模式匹配
public record Pair(String name, int value) { }

Object obj = new Pair("Alice", 100);

if (obj instanceof Pair(var name, var value)) {
    // var 推断类型: name 是 String, value 是 int
    System.out.println(name + ": " + value);
}

// 混合使用 var 和具体类型
if (obj instanceof Pair(String name, var value)) {
    System.out.println(name + ": " + value);
}
```

---

## 守卫条件

### when 守卫

```java
// JDK 21+ when 守卫
public String describe(Object obj) {
    return switch (obj) {
        case String s when s.isEmpty() -> "空字符串";
        case String s when s.length() < 10 -> "短字符串";
        case String s -> "长字符串";
        case Integer i when i > 0 -> "正整数";
        case Integer i when i < 0 -> "负整数";
        case Integer i -> "零";
        default -> "其他";
    };
}

// 在 instanceof 中使用守卫
if (obj instanceof String s && s.length() > 0) {
    // 逻辑与守卫
}

// when 子句中的变量访问
public record Employee(String name, double salary, String department) { }

public String bonus(Employee emp) {
    return switch (emp) {
        case Employee(String n, double s, String d)
            when d.equals("Engineering") && s > 100000
            -> "高级工程师奖金";

        case Employee(String n, double s, String d)
            when d.equals("Engineering")
            -> "工程师奖金";

        case Employee(var n, var s, var d)
            -> "普通员工";
    };
}
```

### 守卫执行顺序

```java
// 守卫按顺序求值
public String test(int value) {
    return switch (value) {
        case 0 -> "零";
        case int i when i > 0 && i < 10 -> "个位数正数";
        case int i when i > 0 -> "多位数正数";
        case int i when i < 0 && i > -10 -> "个位数负数";
        case int i when i < 0 -> "多位数负数";
        default -> "不应到达";
    };
}
```

---

## 解构模式

### 嵌套解构

```java
// 复杂嵌套解构
public record Address(String city, String street, int number) { }
public record Person(String name, Address address) { }
public record Company(String name, Person ceo) { }

Object obj = new Company("Acme",
    new Person("Alice",
        new Address("New York", "5th Ave", 100)));

// 多层解构
if (obj instanceof Company(String cname,
                         Person(String pname,
                               Address(String city, String street, int num)))) {
    System.out.println(cname + " CEO " + pname +
                      " lives at " + num + " " + street + ", " + city);
}
```

### 数组/List 解构

```java
// JDK 21+ 不直接支持数组/List 模式
// 但可以使用 Record 包装

public record Triple(int a, int b, int c) { }

Object obj = new Triple(1, 2, 3);

if (obj instanceof Triple(int a, int b, int c)) {
    System.out.println("Sum: " + (a + b + c));
}

// 自定义解构方法
public record List<T>(T head, List<T> tail) {
    public static <T> List<T> of(java.util.List<T> list) {
        if (list.isEmpty()) {
            throw new IllegalArgumentException("Empty list");
        }
        return new List<>(list.get(0),
            list.isEmpty() ? null : of(list.subList(1, list.size())));
    }
}

// 使用
List<String> list = List.of("a", "b", "c");
if (list instanceof List(var head, var tail)) {
    System.out.println("Head: " + head);
}
```

---

## 最佳实践

### 模式匹配原则

```java
// ✅ 推荐

// 1. 使用模式匹配简化类型检查
// JDK 16 之前
if (obj instanceof String) {
    String s = (String) obj;
    process(s);
}

// JDK 16+
if (obj instanceof String s) {
    process(s);
}

// 2. 使用守卫替代嵌套 if
// ❌ 不好
if (obj instanceof String s) {
    if (!s.isEmpty()) {
        if (s.length() < 10) {
            processShort(s);
        } else {
            processLong(s);
        }
    }
}

// ✅ 好
switch (obj) {
    case String s when s.isEmpty() -> { }
    case String s when s.length() < 10 -> processShort(s);
    case String s -> processLong(s);
    default -> { }
}

// 3. 使用 Record 模式解构数据
// ❌ 不好
if (obj instanceof Point p) {
    int x = p.x();
    int y = p.y();
    System.out.println(x + ", " + y);
}

// ✅ 好
if (obj instanceof Point(int x, int y)) {
    System.out.println(x + ", " + y);
}
```

### 模式覆盖

```java
// ✅ 确保 switch 模式穷尽

// 使用 sealed 类型确保完整性
public sealed interface Shape permits Circle, Rectangle, Square {
    record Circle(double radius) implements Shape { }
    record Rectangle(double width, double height) implements Shape { }
    record Square(double side) implements Shape { }
}

public double area(Shape shape) {
    return switch (shape) {
        case Circle(double r) -> Math.PI * r * r;
        case Rectangle(double w, double h) -> w * h;
        case Square(double s) -> s * s;
        // 不需要 default - 编译器知道已覆盖所有情况
    };
}

// 对于非 sealed 类型, 使用 default
public String describe(Object obj) {
    return switch (obj) {
        case String s -> "String";
        case Integer i -> "Integer";
        case null -> "null";
        default -> "Other";  // 必需
    };
}
```

### 避免过度复杂

```java
// ❌ 避免: 过度嵌套的模式
if (obj instanceof Company(String cname,
                          Person(String pname,
                                Address(String city,
                                       String street,
                                       int num) a)
                         ) p) {
    // 太深, 难以阅读
}

// ✅ 好: 分步解构或使用中间变量
if (obj instanceof Company(var name, Person ceo)) {
    if (ceo instanceof Person(String pname, Address addr)) {
        if (addr instanceof Address(String city, var street, var num)) {
            System.out.println(name + " CEO in " + city);
        }
    }
}

// 或者提取方法
public void describe(Object obj) {
    if (obj instanceof Company c) {
        describeCompany(c);
    }
}

private void describeCompany(Company c) {
    if (c.ceo() instanceof Person(String name, Address a)) {
        System.out.println(name + " at " + a.city());
    }
}
```

---

## 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 模式匹配 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Gavin Bierman | 30+ | Oracle | 模式匹配规范 |
| 2 | Brian Goetz | 20+ | Oracle | 语言设计 |
| 3 | Jan Lahoda | 15+ | Oracle | 编译器实现 |
| 4 | Vicente Romero | 10+ | Oracle | 类型检查 |

### 历史贡献者

| 贡献者 | 公司/机构 | 主要贡献 |
|--------|----------|----------|
| **Gavin Bierman** | Oracle | JEP 305/394/406/420/440 规范 |
| **Brian Goetz** | Oracle | 模式匹配设计 |

---

## 相关链接

### 内部文档

- [Record 类型](../records/) - Record 详解
- [语法演进](../language/syntax/) - 语法演进历程

### 外部资源

- [JEP 305: Pattern Matching for instanceof](https://openjdk.org/jeps/305)
- [JEP 394: Pattern Matching for instanceof](https://openjdk.org/jeps/394)
- [JEP 406: Pattern Matching for switch](https://openjdk.org/jeps/406)
- [JEP 420: Pattern Matching for switch (Second Preview)](https://openjdk.org/jeps/420)
- [JEP 441: Pattern Matching for switch](https://openjdk.org/jeps/441)
- [JEP 405: Record Patterns (Preview)](https://openjdk.org/jeps/405)
- [JEP 432: Record Patterns (Second Preview)](https://openjdk.org/jeps/432)
- [JEP 440: Record Patterns](https://openjdk.org/jeps/440)
- [Pattern Matching (JLS)](https://docs.oracle.com/javase/specs/jls/se21/html/jls-14.html#jls-14.30)

---

**最后更新**: 2026-03-20
