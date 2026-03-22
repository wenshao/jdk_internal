# 模式匹配

> Pattern Matching、类型模式、Record 模式、守卫、解构

[← 返回核心平台](../)

---

## 1. 快速概览

```
JDK 14 ── JDK 16 ── JDK 17 ── JDK 19 ── JDK 21 ── JDK 22 ── JDK 23 ── JDK 24
   │        │        │        │        │        │        │        │
instance  instanceof  Switch  Record  模式匹配  未命名  原始类型  原始类型
of       模式正式    模式    模式    正式版   模式    模式预览  模式二次
                   预览    预览    (三大)   正式版            预览
```

**核心里程碑**:
- **JDK 14**: instanceof 模式预览
- **JDK 16**: instanceof 模式正式版
- **JDK 17**: Switch 模式预览
- **JDK 19**: Record 模式预览
- **JDK 21**: Pattern Matching 完整版（instanceof + switch + record）
- **JDK 22**: 未命名模式和变量正式版
- **JDK 23/24**: 原始类型模式扩展（预览中）

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
| **JDK 21** | 未命名模式/变量 | JEP 443 | 预览 |
| **JDK 22** | 未命名模式/变量 | JEP 456 | 正式版 |
| **JDK 23** | 原始类型模式 | JEP 455 | 预览 |
| **JDK 24** | 原始类型模式 | JEP 488 | 二次预览 |

---

## 目录

- [类型模式](#类型模式)
- [未命名模式和变量](#未命名模式和变量)
- [Switch 模式](#switch-模式)
- [Record 模式](#record-模式)
- [守卫条件](#守卫条件)
- [解构模式](#解构模式)
- [原始类型模式](#原始类型模式)
- [最佳实践](#最佳实践)
- [核心贡献者](#核心贡献者)
- [相关链接](#相关链接)

---

## 2. 类型模式

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

## 3. 未命名模式和变量

### JEP 456: 未命名变量和模式 (Java 22+)

> Java 21 预览 (JEP 443)，Java 22 正式版 (JEP 456)

使用下划线 `_` 表示不需要使用的变量或模式组件。

### 未命名模式变量

```java
// 传统方式：变量声明但未使用
switch (obj) {
    case String s -> "字符串";  // s 未使用，产生警告
    case Integer i -> "整数";   // i 未使用，产生警告
    default -> "其他";
}

// 使用未命名模式变量
switch (obj) {
    case String _  -> "字符串";  // ✅ 明确表示不使用该变量
    case Integer _ -> "整数";    // ✅ 无警告
    case null, default -> "其他";
}
```

### 未命名模式（省略整个组件）

```java
// Record 模式中使用未命名模式
record Point(int x, int y) { }
record ColoredPoint(Point p, Color color) { }

// 只需要 x 坐标，忽略 y 和 color
if (obj instanceof ColoredPoint(Point(int x, _), _)) {
    System.out.println("x = " + x);  // ✅ 清晰表达意图
}

// 传统方式：需要声明所有变量
if (obj instanceof ColoredPoint(Point(int x, int y), Color c)) {
    System.out.println("x = " + x);  // y 和 c 未使用
}
```

### 多个模式合并

```java
// Java 21+ 允许多个模式在同一 case
public String process(Box<? extends Ball> box) {
    return switch (box) {
        // 多个模式共享同一处理逻辑
        case Box(RedBall _), Box(BlueBall _) -> "处理红球或蓝球";
        case Box(GreenBall _) -> "处理绿球";
        case Box(_) -> "处理其他球";
    };
}
```

### 未命名变量在其他场景

```java
// 1. Lambda 参数
stream.collect(Collectors.toMap(
    String::toUpperCase,
    _ -> "NODATA"  // 值不重要，使用未命名参数
));

// 2. try-catch 异常参数
try {
    int i = Integer.parseInt(s);
} catch (NumberFormatException _) {  // 不需要异常对象
    System.out.println("解析失败");
}

// 3. 增强型 for 循环
int count = 0;
for (Order _ : orders) {  // 只需要副作用（计数）
    count++;
}

// 4. try-with-resources
try (var _ = ScopedContext.acquire()) {
    // 不需要使用资源变量
}
```

### 未命名模式的限制

```java
// ❌ 未命名模式不能作为顶层模式
if (obj instanceof _) { }  // 编译错误

// ✅ 未命名模式只能在嵌套位置使用
if (obj instanceof Point(_, _)) { }  // 正确

// ❌ 未命名变量不能被读取
var _ = someValue;
System.out.println(_);  // 编译错误：_ 不能被引用
```

### 未命名模式最佳实践

```java
// 1. 验证类型但不需要值
public boolean isPositiveNumber(Object obj) {
    return switch (obj) {
        case Integer i when i > 0 -> true;
        case Long l when l > 0 -> true;
        case Double d when d > 0.0 -> true;
        case Integer _, Long _, Double _ -> false;  // 负数或零
        default -> false;
    };
}

// 2. Option/Result 类型的解构
record Success<T>(T value, String message) { }
record Error(String code, String message) { }

public String process(Object result) {
    return switch (result) {
        case Success(var value, _) -> "成功: " + value;  // 忽略 message
        case Error(var code, var msg) -> "错误 " + code + ": " + msg;
        default -> "未知结果";
    };
}

// 3. 复杂嵌套解构
record User(String name, Address address) { }
record Address(String city, String street, int zip) { }

// 只需要城市信息
if (obj instanceof User(var name, Address(var city, _, _))) {
    System.out.println(name + " 住在 " + city);
}

// 4. 使用未命名模式简化 Record 比较
public boolean isEqual(Box<?> box1, Box<?> box2) {
    return switch (box1) {
        case Box(var contents1), Box(var contents2) ->
            contents1.equals(contents2);  // 多模式匹配
    };
}
```

---

## 4. Switch 模式

### Switch 表达式基础

```java
// JDK 14+ Switch 表达式
public String getDayType(Day day) {
    return switch (day) {
        case MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY -> "工作日";
        case SATURDAY, SUNDAY -> "周末";
    };
}

// JDK 21+ Switch 模式匹配 (JDK 17 预览, JDK 21 正式)
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

## 5. Record 模式

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

## 6. 守卫条件

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

## 7. 解构模式

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
// JDK 21+ 不直接支持数组/List 模式解构
// 但可以使用 Record 包装实现类似功能

public record Triple(int a, int b, int c) { }

Object obj = new Triple(1, 2, 3);

if (obj instanceof Triple(int a, int b, int c)) {
    System.out.println("Sum: " + (a + b + c));
}

// 自定义链表解构（避免与 java.util.List 冲突）
public record LinkedList<T>(T head, LinkedList<T> tail) {
    public static <T> LinkedList<T> from(java.util.List<T> list) {
        if (list.isEmpty()) {
            return null;
        }
        return new LinkedList<>(list.get(0),
            list.size() > 1 ? from(list.subList(1, list.size())) : null);
    }
}

// 使用
java.util.List<String> input = java.util.List.of("a", "b", "c");
LinkedList<String> list = LinkedList.from(input);

if (list instanceof LinkedList(var head, var tail)) {
    System.out.println("Head: " + head);
}
```

### 数组模式限制

```java
// ❌ 当前不支持数组模式
int[] arr = {1, 2, 3};
if (arr instanceof int[1, 2, 3]) { }  // 编译错误

// ✅ 使用 Record 模拟
public record IntArray(int a, int b, int c) {
    public static IntArray from(int[] arr) {
        if (arr.length != 3) throw new IllegalArgumentException();
        return new IntArray(arr[0], arr[1], arr[2]);
    }
}
```

---

## 8. 原始类型模式

### JEP 455/488: 原始类型模式 (Java 23+ 预览)

> Java 23 预览 (JEP 455)，Java 24 二次预览 (JEP 488)

允许在模式匹配中使用所有原始类型（int, long, double, float, short, byte, char, boolean）。

### instanceof 中的原始类型模式

```java
// JDK 23 之前：instanceof 只支持引用类型
Object obj = 42;
if (obj instanceof Integer i) {  // 需要包装类型
    System.out.println(i);
}

// JDK 23+：支持原始类型模式
if (obj instanceof int i) {  // 直接使用原始类型
    System.out.println("int: " + i);
}

// 支持所有原始类型
Object obj = 3.14;
if (obj instanceof double d) {
    System.out.println("double: " + d);
}

Object obj2 = true;
if (obj2 instanceof boolean b) {
    System.out.println("boolean: " + b);
}
```

### Switch 中的原始类型模式

```java
// JDK 23+：switch 支持所有原始类型
public String describeNumber(Object obj) {
    return switch (obj) {
        case int i -> "整数: " + i;
        case long l -> "长整数: " + l;
        case double d -> "浮点数: " + d;
        case float f -> "单精度浮点: " + f;
        case short s -> "短整数: " + s;
        case byte b -> "字节: " + b;
        case char c -> "字符: " + c;
        case boolean z -> "布尔: " + z;
        case null -> "null";
        default -> "其他类型";
    };
}
```

### 原始类型模式的特殊规则

```java
// 窄化原始类型转换
Object obj = 42L;  // long 值

// ❌ 编译错误：long 不能直接匹配 int 模式
if (obj instanceof int i) {
    // 42L 不匹配 int 模式（需要精确类型匹配）
}

// ✅ 需要使用精确类型或包装类型
if (obj instanceof long l) {
    System.out.println("long: " + l);
}

// 原始类型与包装类型的区别
Object obj1 = 42;        // 自动装箱为 Integer
Object obj2 = 42L;       // 自动装箱为 Long

if (obj1 instanceof int i) {     // ✅ 匹配
    System.out.println("int: " + i);
}

if (obj1 instanceof Integer i) { // ✅ 也匹配
    System.out.println("Integer: " + i);
}

// 注意：int 模式不匹配 Long 对象
if (obj2 instanceof int i) {     // ❌ 不匹配
}
if (obj2 instanceof long l) {    // ✅ 匹配
    System.out.println("long: " + l);
}
```

### 原始类型常量模式

```java
// JDK 23+：原始类型常量模式
public String classify(Object obj) {
    return switch (obj) {
        case int i when i > 0 -> "正整数";
        case int i when i < 0 -> "负整数";
        case int 0 -> "零";
        case double d when d > 0.0 -> "正浮点数";
        case boolean true -> "真";
        case boolean false -> "假";
        default -> "其他";
    };
}
```

---

## 9. 最佳实践

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

## 10. 重要 PR 分析

### 编译器优化

#### JDK-8341755: Lambda 生成优化

> **作者**: [Shaojin Wen](/by-contributor/profiles/shaojin-wen.md)
> **影响**: ⭐⭐⭐ +15-20% Lambda 生成性能

模式匹配经常与 Lambda 一起使用，此 PR 优化了 Lambda 生成：

**优化点**:
- 0 参数 Lambda 使用常量（消除数组分配）
- 缓存常见参数名称（1-8 参数）
- 使用 `@Stable` 注解启用 JIT 优化

```java
// 模式匹配 + Lambda 组合
List<Point> points = List.of(new Point(1, 2), new Point(3, 4));

points.stream()
    .filter(p -> p instanceof Point(int x, int y) && x > 0)  // Lambda 优化受益
    .mapToInt(p -> p.y())
    .sum();
```

→ [详细分析](/by-pr/8341/8341755.md)

---

## 11. 模式匹配性能最佳实践

### 模式匹配性能对比

```java
// 传统方式 vs 模式匹配

// ❌ 传统方式：多次类型检查
public String describeOld(Object obj) {
    if (obj instanceof Circle) {
        Circle c = (Circle) obj;
        return "Circle: " + c.radius();
    } else if (obj instanceof Rectangle) {
        Rectangle r = (Rectangle) obj;
        return "Rectangle: " + r.width() + "x" + r.height();
    }
    return "Unknown";
}

// ✅ 模式匹配：单次类型检查
public String describeNew(Object obj) {
    return switch (obj) {
        case Circle(double r) -> "Circle: " + r;
        case Rectangle(double w, double h) -> "Rectangle: " + w + "x" + h;
        default -> "Unknown";
    };
}
```

**性能对比**:
- 传统方式：2-3 次类型检查 + 强制转换
- 模式匹配：1 次类型检查 + 直接解构
- 代码简洁性：显著提升（减少样板代码）
- 性能：在热路径中 JIT 优化后相当，冷启动时可能略慢（约 5-10%）

> **注意**: 模式匹配的主要优势在于代码可读性和类型安全，而非纯性能提升。JIT 编译器会对两种模式进行类似的优化。

### Sealed Types 模式匹配

```java
// ✅ 推荐：使用 sealed 类型启用穷尽检查
public sealed interface Shape permits Circle, Rectangle {
    record Circle(double radius) implements Shape { }
    record Rectangle(double width, double height) implements Shape { }
}

// 编译器验证覆盖所有情况
public double area(Shape shape) {
    return switch (shape) {
        case Circle(double r) -> Math.PI * r * r;
        case Rectangle(double w, double h) -> w * h;
        // 无需 default - 编译器确保完整性
    };
}
```

**优势**:
- 编译时验证完整性
- 新增类型时自动提醒更新
- JIT 优化更激进（已知所有情况）

### 守卫模式性能

```java
// ✅ 推荐：使用守卫替代嵌套 if
public String describe(Object obj) {
    return switch (obj) {
        case String s when s.isEmpty() -> "Empty string";
        case String s when s.length() < 10 -> "Short string";
        case String s -> "Long string";
        default -> "Not a string";
    };
}

// ❌ 避免：深层嵌套
public String describeBad(Object obj) {
    if (obj instanceof String s) {
        if (s.isEmpty()) {
            return "Empty string";
        } else {
            if (s.length() < 10) {
                return "Short string";
            } else {
                return "Long string";
            }
        }
    }
    return "Not a string";
}
```

---

## 12. 核心贡献者

> **统计来源**: 本地 JDK 源码 master 分支 git 历史分析
> **统计时间**: 2026-03-20

### 模式匹配 (按 Git 提交数)

| 排名 | 贡献者 | 提交数 | 组织 | 主要贡献 |
|------|--------|--------|------|----------|
| 1 | Gavin Bierman | 30+ | Oracle | 模式匹配规范 |
| 2 | [Brian Goetz](/by-contributor/profiles/brian-goetz.md) | 20+ | Oracle | 语言设计 |
| 3 | [Jan Lahoda](/by-contributor/profiles/jan-lahoda.md) | 15+ | Oracle | 编译器实现 |
| 4 | Vicente Romero | 10+ | Oracle | 类型检查 |

### 历史贡献者

| 贡献者 | 公司/机构 | 主要贡献 |
|--------|----------|----------|
| **Gavin Bierman** | Oracle | JEP 305/394/406/420/440 规范 |
| **Brian Goetz** | Oracle | 模式匹配设计 |

---

## 13. 相关链接

### 内部文档

- [Record 类型](../records/) - Record 详解
- [语法演进](../language/syntax/) - 语法演进历程

### 外部资源

#### 核心 JEP
- [JEP 305](/jeps/language/jep-305.md)
- [JEP 375](/jeps/language/jep-375.md)
- [JEP 394](/jeps/language/jep-394.md)
- [JEP 406](https://openjdk.org/jeps/406)
- [JEP 420](https://openjdk.org/jeps/420)
- [JEP 427](https://openjdk.org/jeps/427)
- [JEP 433](https://openjdk.org/jeps/433)
- [JEP 441](/jeps/language/jep-441.md)
- [JEP 405](https://openjdk.org/jeps/405)
- [JEP 432](https://openjdk.org/jeps/432)
- [JEP 440](/jeps/language/jep-440.md)

#### 扩展 JEP
- [JEP 443](/jeps/language/jep-443.md)
- [JEP 456](/jeps/language/jep-456.md)
- [JEP 455](/jeps/tools/jep-455.md)
- [JEP 488](https://openjdk.org/jeps/488)

#### 规范文档
- [Pattern Matching (JLS 14)](https://docs.oracle.com/javase/specs/jls/se21/html/jls-14.html#jls-14.30)
- [Unnamed Variables and Variables (Oracle Docs)](https://docs.oracle.com/en/java/javase/22/language/unnamed-variables-and-patterns.html)

---

**最后更新**: 2026-03-21
