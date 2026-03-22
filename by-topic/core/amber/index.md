# Project Amber

Java 语言特性演进项目：让 Java 更简洁、更安全、更易表达。

[← 返回核心平台](../)

---
## 目录

1. [TL;DR](#1-tldr)
2. [项目概述](#2-项目概述)
3. [主要特性详解](#3-主要特性详解)
   - [3.1 var 类型推断](#31-var-类型推断-local-variable-type-inference---jep-286323)
   - [3.2 Switch 表达式与模式匹配完整演进](#32-switch-表达式与模式匹配完整演进)
   - [3.3 Records 深入](#33-records-深入-jep-395)
   - [3.4 Sealed Classes 深入](#34-sealed-classes-深入-jep-409)
   - [3.5 Text Blocks](#35-text-blocks-深入-jep-378)
   - [3.6 Record Patterns](#36-record-patterns-jep-440)
   - [3.7 Unnamed Patterns & Variables](#37-unnamed-patterns--variables-jep-456)
   - [3.8 Compact Source Files & Instance Main](#38-compact-source-files--instance-main-methods-jep-512)
   - [3.9 Flexible Constructor Bodies](#39-flexible-constructor-bodies-深入-jep-513)
   - [3.10 Primitive Patterns](#310-primitive-patterns-jep-455--488--507--530)
   - [3.11 String Templates (已撤回)](#311-string-templates-已撤回---jep-430--459--465)
   - [3.12 Stream Gatherers](#312-stream-gatherers-jep-485)
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
| **Stream Gatherers** | JDK 24 | JEP 485 |
| **Implicit Classes** | JDK 25 | JEP 512 |
| **Module Import Declarations** | JDK 25 | JEP 511 |
| **Flexible Constructor Bodies** | JDK 25 | JEP 513 |
| **String Templates** | (已撤回) | JEP 430 → 459 → 465 |
| **Primitive Patterns** | JDK 26 (4th Preview) | JEP 455 → 488 → 507 → 530 |

---

## 3. 主要特性详解

### 3.1 var 类型推断 (Local Variable Type Inference - JEP 286/323)

JDK 10 引入 `var` 关键字 (局部变量类型推断, local variable type inference)，
JDK 11 的 JEP 323 将其扩展到 Lambda 参数。

#### 基本用法 (Basic Usage)

```java
// 传统写法
ArrayList<String> names = new ArrayList<String>();
Map<String, List<Integer>> scores = new HashMap<String, List<Integer>>();
BufferedReader reader = new BufferedReader(new FileReader("data.txt"));

// 使用 var - 编译器自动推断类型
var names = new ArrayList<String>();          // 推断为 ArrayList<String>
var scores = new HashMap<String, List<Integer>>(); // 推断为 HashMap<String, List<Integer>>
var reader = new BufferedReader(new FileReader("data.txt"));

// for 循环中使用 var
for (var entry : map.entrySet()) {
    var key = entry.getKey();
    var value = entry.getValue();
}

// try-with-resources 中使用 var
try (var stream = Files.lines(Path.of("data.txt"))) {
    stream.forEach(System.out::println);
}
```

#### 适用场景 (When to Use)

```java
// 1. 构造器调用 - 类型已在右侧明确
var list = new ArrayList<String>();          // 清晰：右侧已有类型
var map = new TreeMap<String, Integer>();

// 2. 工厂方法 - 返回类型显而易见
var path = Path.of("/tmp/data.txt");         // 显然是 Path
var now = Instant.now();                     // 显然是 Instant
var stream = list.stream();                  // Stream<String>

// 3. 复杂泛型 - 减少视觉噪音
var lookup = MethodHandles.lookup();
var entries = map.entrySet().iterator();

// 4. Lambda 参数 (JEP 323, JDK 11) - 允许在 Lambda 参数上添加注解
list.sort((var a, var b) -> a.compareToIgnoreCase(b));
// 主要目的：可以给 Lambda 参数加注解
list.forEach((@NonNull var item) -> process(item));
```

#### 限制 (Restrictions) - var 不能用于：

```java
// ✗ 字段 (fields) - 不支持
class MyClass {
    var name = "hello";      // 编译错误！
    private var count = 0;   // 编译错误！
}

// ✗ 方法参数 (method parameters) - 不支持
void process(var data) { }   // 编译错误！

// ✗ 方法返回类型 (return types) - 不支持
var getName() { return "hello"; }  // 编译错误！

// ✗ 没有初始化器 (no initializer)
var x;                       // 编译错误！必须有初始化表达式
x = 42;

// ✗ null 初始化 (null initializer)
var nothing = null;          // 编译错误！无法推断类型

// ✗ 数组初始化器 (array initializer)
var arr = { 1, 2, 3 };      // 编译错误！
var arr = new int[]{ 1, 2, 3 };  // ✓ 这样可以

// ✗ Lambda 表达式和方法引用 (lambda / method reference)
var fn = x -> x + 1;        // 编译错误！目标类型未知
var ref = System.out::println; // 编译错误！
```

#### 风格指南 (Style Guidelines)

```java
// ✓ 推荐：类型从上下文中显而易见
var names = new ArrayList<String>();          // 右侧有类型名
var count = inventory.getItemCount();         // 方法名暗示 int/long

// ✗ 不推荐：类型不明显，降低可读性
var result = service.process(data);           // result 是什么类型？
var x = computeSomething();                   // 完全不可读

// ✓ 推荐：使用有意义的变量名弥补类型信息的缺失
var customerById = new HashMap<Long, Customer>();  // 变量名描述用途
var activeOrders = orderService.findActive();       // 变量名说明内容

// ✗ 不推荐：短变量名 + var = 不可读
var m = new HashMap<Long, Customer>();        // m 是什么？
var r = orderService.findActive();            // r 是什么类型？

// Oracle 官方建议 (Style Guidelines for Local Variable Type Inference):
// G1: 选择能提供有用信息的变量名
// G2: 减少局部变量的作用域
// G3: 当初始化器能提供足够类型信息时才使用 var
// G4: 用 var 消除样板代码而不是降低清晰度
// G5: 不要过于担心"编程到接口" (var list = new ArrayList<>() 是可以的)
```

---

### 3.2 Switch 表达式与模式匹配完整演进

Switch 在 Amber 项目下经历了**最长的演进链**，从简单的语法改进到完整的模式匹配系统：

```
JEP 325 (Preview)    JDK 12   Switch Expressions (第一预览)
    ↓
JEP 354 (2nd Preview) JDK 13  Switch Expressions (第二预览, 引入 yield)
    ↓
JEP 361 (Final)       JDK 14  Switch Expressions (正式发布)
    ↓
JEP 394 (Final)       JDK 16  Pattern Matching for instanceof (正式)
    ↓
JEP 406 (Preview)     JDK 17  Pattern Matching for switch (第一预览)
    ↓
JEP 440 (Final)       JDK 21  Record Patterns (正式)
    ↓
JEP 441 (Final)       JDK 21  Pattern Matching for switch (正式)
    ↓
JEP 456 (Final)       JDK 22  Unnamed Patterns & Variables (正式)
    ↓
JEP 455→488→507→530   JDK 23-26  Primitive Patterns (预览中)
```

#### 阶段 1: Switch Expressions (JEP 325 → 354 → 361)

```java
// ===== JEP 325 (JDK 12 Preview): 引入 arrow syntax =====
// 旧写法 - 语句形式, 需要 break, 容易 fall-through 出错
int result;
switch (day) {
    case MONDAY:
    case FRIDAY:
    case SUNDAY:
        result = 6;
        break;        // 忘记 break 就 fall-through!
    case TUESDAY:
        result = 7;
        break;
    default:
        result = 0;
}

// JDK 12 新写法 - 表达式形式
int result = switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> 6;    // 多标签, 无 fall-through
    case TUESDAY                -> 7;
    default                     -> 0;
};  // 注意分号 - 因为整个 switch 是一个表达式

// ===== JEP 354 (JDK 13 Preview): break 改为 yield =====
// JDK 12 中使用 break value 返回值，JDK 13 改为 yield 更清晰
String message = switch (status) {
    case 0 -> {
        log("Processing...");
        yield "OK";       // yield 用于代码块中返回值 (替代了 JDK 12 的 break value)
    }
    case 1 -> "Warning";  // 单行表达式不需要 yield
    case 2 -> "Error";
    default -> "Unknown";
};

// ===== JEP 361 (JDK 14 Final): 正式发布 =====
// 语义与 JDK 13 相同, 两种形式都可用：
// 1) arrow 形式 (推荐, 无 fall-through)
int numLetters = switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> 6;
    case TUESDAY                -> 7;
    case THURSDAY, SATURDAY     -> 8;
    case WEDNESDAY              -> 9;
};

// 2) colon 形式 + yield (兼容旧语法, 仍有 fall-through 风险)
int numLetters = switch (day) {
    case MONDAY:
    case FRIDAY:
    case SUNDAY:
        yield 6;          // 用 yield 替代 break
    case TUESDAY:
        yield 7;
    default:
        yield 0;
};
```

#### 阶段 2: Pattern Matching for instanceof (JEP 394)

```java
// JDK 16 正式 - 消除冗余的类型转换
// 旧写法
if (obj instanceof String) {
    String s = (String) obj;     // 冗余的强制转换
    System.out.println(s.length());
}

// 新写法 - 模式变量 (pattern variable)
if (obj instanceof String s) {
    System.out.println(s.length());  // s 已自动绑定
}

// 模式变量的作用域 (flow scoping) - 编译器根据控制流推断
if (obj instanceof String s && s.length() > 5) {
    // ✓ s 在 && 后面可用 (因为 && 只在左边为 true 时计算右边)
}

if (!(obj instanceof String s)) {
    return;
}
// ✓ s 在这里可用 (因为如果 obj 不是 String, 已经 return 了)
System.out.println(s.toUpperCase());

// ✗ 编译错误 - 在 || 后面不安全
if (obj instanceof String s || s.length() > 5) {  // 编译错误！
    // s 可能没有被绑定
}
```

#### 阶段 3: Pattern Matching for switch (JEP 406 → 441)

```java
// JEP 406 (JDK 17 Preview) → JEP 420 (JDK 18) → JEP 427 (JDK 19)
// → JEP 433 (JDK 20) → JEP 441 (JDK 21 Final)
// 经过了 4 轮预览才最终定稿

// 类型模式 (type pattern) 在 switch 中
String formatted = switch (obj) {
    case Integer i -> String.format("int %d", i);
    case Long l    -> String.format("long %d", l);
    case Double d  -> String.format("double %f", d);
    case String s  -> String.format("String %s", s);
    default        -> obj.toString();
};

// 守卫模式 (guarded pattern) - when 子句
String check = switch (obj) {
    case String s when s.length() > 5 -> "Long string: " + s;
    case String s                     -> "Short string: " + s;
    case Integer i when i > 0         -> "Positive int";
    case Integer i                    -> "Non-positive int";
    default                           -> "Unknown";
};
// 注意: case 的顺序重要! 有守卫的 case 必须在无守卫的同类型 case 之前

// null 处理 (不再需要在 switch 外检查 null)
String result = switch (obj) {
    case null      -> "null value";        // 显式处理 null
    case String s  -> "String: " + s;
    default        -> "Other type";
};

// null + default 合并
String result = switch (obj) {
    case String s  -> "String: " + s;
    case null, default -> "null or other";  // null 和 default 可以合并
};

// 穷尽性检查 (exhaustiveness) - 密封类不需要 default
sealed interface Shape permits Circle, Rectangle {}
record Circle(double r) implements Shape {}
record Rectangle(double w, double h) implements Shape {}

double area = switch (shape) {
    case Circle c    -> Math.PI * c.r() * c.r();
    case Rectangle r -> r.w() * r.h();
    // 无需 default - 编译器知道所有子类型都已覆盖
};
```

#### 阶段 4: Record Patterns + Unnamed Patterns (JEP 440, 456)

```java
// Record Patterns (JEP 440, JDK 21) - 解构 Record 组件
record Point(int x, int y) {}
record Rectangle(Point topLeft, Point bottomRight) {}

// 嵌套解构 (nested deconstruction)
String describe(Object obj) {
    return switch (obj) {
        case Rectangle(Point(int x1, int y1), Point(int x2, int y2)) ->
            "Rectangle from (%d,%d) to (%d,%d)".formatted(x1, y1, x2, y2);
        case Point(int x, int y) ->
            "Point at (%d,%d)".formatted(x, y);
        default -> "Unknown shape";
    };
}

// Unnamed Patterns (JEP 456, JDK 22) - 使用 _ 忽略不关心的值
void extractX(Object obj) {
    if (obj instanceof Point(int x, _)) {   // 只关心 x, 忽略 y
        System.out.println("X: " + x);
    }
}

// Lambda 中忽略参数
stream.map(_ -> "constant");

// catch 中忽略异常对象
try { riskyOp(); }
catch (Exception _) { logger.error("Failed"); }
```

---

### 3.3 Records 深入 (JEP 395)

Records (记录类) 是**透明的数据载体** (transparent carriers for data)，
自动生成 constructor、accessor、equals、hashCode、toString。

#### 规范构造器 vs 紧凑构造器 (Canonical vs Compact Constructor)

```java
record Range(int lo, int hi) {

    // 规范构造器 (canonical constructor) - 显式列出所有参数
    // 当你需要完全控制赋值逻辑时使用
    Range(int lo, int hi) {
        if (lo > hi) throw new IllegalArgumentException(
            "lo (%d) > hi (%d)".formatted(lo, hi));
        this.lo = lo;   // 必须显式赋值
        this.hi = hi;   // 必须显式赋值
    }
}

record Range(int lo, int hi) {

    // 紧凑构造器 (compact constructor) - 无参数列表, 无显式赋值
    // 更常用: 只写验证/归一化逻辑, 赋值由编译器自动生成
    Range {
        if (lo > hi) throw new IllegalArgumentException(
            "lo (%d) > hi (%d)".formatted(lo, hi));
        // 可以修改参数值 (归一化)
        lo = Math.max(lo, 0);    // 修改的是参数, 不是字段
        hi = Math.min(hi, 100);
        // 编译器自动在最后生成 this.lo = lo; this.hi = hi;
    }
}

// 非规范构造器 (custom/alternative constructor) - 必须委托给规范构造器
record Point(double x, double y) {
    // 从极坐标构造 (工厂风格的额外构造器)
    Point(double r, double theta, boolean polar) {
        this(r * Math.cos(theta), r * Math.sin(theta)); // 委托给规范构造器
    }
}
```

#### 自定义方法与限制 (Custom Methods & Restrictions)

```java
record Employee(String name, String department, double salary) {

    // ✓ 可以添加实例方法
    String displayName() {
        return name.toUpperCase() + " (" + department + ")";
    }

    // ✓ 可以添加静态方法/字段
    static Employee of(String name) {
        return new Employee(name, "Unknown", 0);
    }
    static final Employee EMPTY = new Employee("", "", 0);

    // ✓ 可以覆盖自动生成的方法
    @Override
    public String toString() {
        return "%s [%s] $%.2f".formatted(name, department, salary);
    }

    // ✓ 可以实现接口
    // record Employee(...) implements Comparable<Employee> { ... }

    // ✗ 不能声明实例字段 (只有组件字段)
    // private int age;     // 编译错误！

    // ✗ 不能继承其他类 (隐式 extends java.lang.Record)
    // record Manager(...) extends Employee { } // 编译错误！

    // ✗ Record 是隐式 final 的, 不能被继承
    // class SeniorEmployee extends Employee { } // 编译错误！

    // ✗ 组件字段隐式 final, 不能修改
    // void setSalary(double s) { this.salary = s; } // 编译错误！
}
```

#### Records 与序列化 (Serialization)

```java
// Record 天然支持序列化, 且比传统类更安全
// 序列化使用组件值, 反序列化**总是调用规范构造器**
// (传统类的反序列化绕过构造器, 可能导致不变量被破坏)
record User(String name, int age) implements Serializable {
    User {
        if (age < 0) throw new IllegalArgumentException("age < 0");
        // 反序列化也会执行此验证！传统类做不到
    }
}

// 序列化/反序列化
var user = new User("Alice", 30);
byte[] bytes;
try (var out = new ObjectOutputStream(new ByteArrayOutputStream())) {
    out.writeObject(user);    // 序列化
    bytes = ((ByteArrayOutputStream) out).toByteArray();
}
try (var in = new ObjectInputStream(new ByteArrayInputStream(bytes))) {
    var restored = (User) in.readObject();  // 反序列化 - 调用规范构造器
    assert restored.equals(user);
}

// Record 不需要 serialVersionUID
// Record 不支持 writeObject/readObject 自定义序列化方法
// Record 不支持 Externalizable 接口
```

#### Records 与 Sealed Classes 的组合 (ADT 模式)

```java
// Record + Sealed = 代数数据类型 (Algebraic Data Type)
// 经典案例: 表达式树 (expression tree)
sealed interface Expr permits Num, Add, Mul, Neg {
    // 可选: 在接口上定义通用行为
}

record Num(double value)       implements Expr {}
record Add(Expr left, Expr right) implements Expr {}
record Mul(Expr left, Expr right) implements Expr {}
record Neg(Expr operand)       implements Expr {}

// 使用模式匹配进行求值 (pattern matching evaluation)
double eval(Expr expr) {
    return switch (expr) {
        case Num(var v)          -> v;
        case Add(var l, var r)   -> eval(l) + eval(r);
        case Mul(var l, var r)   -> eval(l) * eval(r);
        case Neg(var e)          -> -eval(e);
        // 无需 default! sealed 保证穷尽性
    };
}

// 使用示例
var expr = new Add(new Num(1), new Mul(new Num(2), new Num(3)));
System.out.println(eval(expr)); // 输出 7.0
```

---

### 3.4 Sealed Classes 深入 (JEP 409)

密封类 (sealed classes) 限制哪些类可以继承/实现它，
结合模式匹配实现**穷尽性检查** (exhaustiveness checking)。

#### 声明规则 (Declaration Rules)

```java
// 子类型修饰符有三种选择:
// 1. final    - 不可再继承
// 2. sealed   - 继续限制继承
// 3. non-sealed - 开放继承

sealed interface Animal permits Dog, Cat, Fish {}

final class Dog implements Animal {            // final: 到此为止
    String breed;
}

sealed class Cat implements Animal permits Siamese, Persian {} // sealed: 继续限制
final class Siamese extends Cat {}
final class Persian extends Cat {}

non-sealed class Fish implements Animal {}     // non-sealed: 开放给任何人继承
class Goldfish extends Fish {}                 // ✓ 允许
class Shark extends Fish {}                    // ✓ 允许

// 子类型必须在同一模块 (module) 或同一包 (package) 中声明
// permits 子句中的类型必须直接扩展/实现密封类

// 如果所有子类都在同一个编译单元, permits 可以省略:
sealed interface Coin { }  // permits 自动推断
record Penny()   implements Coin {}
record Nickel()  implements Coin {}
record Dime()    implements Coin {}
record Quarter() implements Coin {}
```

#### 穷尽性 Switch (Exhaustive Switch)

```java
sealed interface Result<T> permits Success, Failure {}
record Success<T>(T value) implements Result<T> {}
record Failure<T>(Exception error) implements Result<T> {}

// 编译器保证所有情况都被覆盖
<T> String handle(Result<T> result) {
    return switch (result) {
        case Success<T>(var value) -> "OK: " + value;
        case Failure<T>(var error) -> "Error: " + error.getMessage();
        // 无需 default - 编译器知道只有 Success 和 Failure
    };
}

// 如果未来添加了新的 permits 子类:
// sealed interface Result<T> permits Success, Failure, Pending {}
// 所有没有覆盖 Pending 的 switch 语句都会产生编译错误！
// 这就是 sealed classes 的核心价值: 让编译器帮你发现遗漏
```

#### 代数数据类型 (ADT) 模式与深度模式匹配

```java
// 经典 ADT: Option/Maybe
sealed interface Maybe<T> permits Just, Nothing {}
record Just<T>(T value) implements Maybe<T> {}
record Nothing<T>() implements Maybe<T> {}

<T> T orElse(Maybe<T> maybe, T fallback) {
    return switch (maybe) {
        case Just(var v) -> v;
        case Nothing()   -> fallback;
    };
}

// 经典 ADT: Either (二选一)
sealed interface Either<L, R> permits Left, Right {}
record Left<L, R>(L value) implements Either<L, R> {}
record Right<L, R>(R value) implements Either<L, R> {}

// 实际项目中: JSON AST
sealed interface JsonValue permits JsonNull, JsonBool, JsonNumber, JsonString,
                                   JsonArray, JsonObject {}
record JsonNull()                            implements JsonValue {}
record JsonBool(boolean value)               implements JsonValue {}
record JsonNumber(double value)              implements JsonValue {}
record JsonString(String value)              implements JsonValue {}
record JsonArray(List<JsonValue> elements)   implements JsonValue {}
record JsonObject(Map<String, JsonValue> fields) implements JsonValue {}

// 深度模式匹配解析 JSON
String prettyPrint(JsonValue json, int indent) {
    var pad = " ".repeat(indent);
    return switch (json) {
        case JsonNull()       -> "null";
        case JsonBool(var b)  -> String.valueOf(b);
        case JsonNumber(var n) -> String.valueOf(n);
        case JsonString(var s) -> "\"" + s + "\"";
        case JsonArray(var elems) -> {
            var items = elems.stream()
                .map(e -> pad + "  " + prettyPrint(e, indent + 2))
                .collect(Collectors.joining(",\n"));
            yield "[\n" + items + "\n" + pad + "]";
        }
        case JsonObject(var fields) -> {
            var entries = fields.entrySet().stream()
                .map(e -> pad + "  \"" + e.getKey() + "\": "
                          + prettyPrint(e.getValue(), indent + 2))
                .collect(Collectors.joining(",\n"));
            yield "{\n" + entries + "\n" + pad + "}";
        }
    };
}
```

---

### 3.5 Text Blocks 深入 (JEP 378)

Text Blocks (文本块) 是 JDK 15 正式引入的多行字符串字面量 (multi-line string literals)。

#### 缩进管理 (Indentation Management)

```java
// Text Block 的缩进由**结束分隔符 (closing delimiter) 的位置**决定
// 编译器会自动调用 String::stripIndent 移除"附带缩进" (incidental whitespace)

// 示例 1: 结束符与内容同级 → 无附带缩进
String s1 = """
    line 1
    line 2
    """;
// 等价于 "line 1\nline 2\n"  (4 个空格被视为附带缩进, 被移除)

// 示例 2: 结束符更靠左 → 保留部分缩进
String s2 = """
    line 1
    line 2
""";
// 等价于 "    line 1\n    line 2\n"  (结束符在第 0 列, 所以 4 个空格保留)

// 示例 3: 结束符更靠右 → 不影响缩进移除
String s3 = """
    line 1
    line 2
        """;
// 等价于 "line 1\nline 2\n"  (最小缩进仍是 4 个空格)

// String::stripIndent() 算法:
// 1. 找到所有非空行的最小公共前导空白 (common leading whitespace)
// 2. 移除每行的该前缀
// 3. 移除尾部空白 (trailing whitespace from each line)
```

#### 转义序列 (Escape Sequences)

```java
// \s - 保留尾部空格 (preserve trailing space)
// 普通 text block 会移除每行尾部空白, \s 阻止这种移除
String table = """
    Name   \s
    Alice  \s
    Bob    \s
    """;
// 每行保留了尾部的空格 (不含 \s 本身, \s 转义为一个空格)

// \ - 行连续符 (line continuation), 取消行尾换行
String longLine = """
    This is a very long line that \
    we want to keep on a single line \
    in the output.""";
// 等价于 "This is a very long line that we want to keep on a single line in the output."
// 注意: \ 后面不能有空格!

// 组合使用
String poem = """
    Roses are red,\s\s\s
    Violets are blue.\
     Sugar is sweet.""";
// "Roses are red,   \nViolets are blue. Sugar is sweet."
// 第1行: \s\s\s 保留 3 个尾部空格
// 第2行: \ 取消换行, 第3行的前导空格成为连接的一部分
```

#### String.formatted() 与 Text Blocks

```java
// String.formatted() 是 String.format() 的实例方法版本 (JDK 15+)
// 非常适合与 text blocks 搭配使用

String html = """
    <html>
        <body>
            <h1>%s</h1>
            <p>Welcome, %s! You have %d messages.</p>
        </body>
    </html>
    """.formatted(title, userName, messageCount);

String json = """
    {
        "name": "%s",
        "age": %d,
        "email": "%s"
    }
    """.formatted(name, age, email);

// SQL 查询
String sql = """
    SELECT u.name, u.email, COUNT(o.id) as order_count
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    WHERE u.status = '%s'
      AND u.created_at > '%s'
    GROUP BY u.name, u.email
    HAVING COUNT(o.id) > %d
    ORDER BY order_count DESC
    """.formatted(status, startDate, minOrders);

// 注意: 对于 SQL, 实际项目中应使用 PreparedStatement 防止注入
// formatted() 主要用于日志、模板、测试等场景
```

---

### 3.6 Record Patterns (JEP 440)

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

### 3.7 Unnamed Patterns & Variables (JEP 456)

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

### 3.8 Compact Source Files & Instance Main Methods (JEP 512)

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

### 3.9 Flexible Constructor Bodies 深入 (JEP 513)

JDK 25 正式发布。允许在构造器中 `super()` 或 `this()` **之前**执行语句 (prologue statements)。

#### 问题背景 (Motivation)

```java
// 旧规则: super() 或 this() 必须是构造器的第一条语句
// 这导致了很多丑陋的 workaround:

// Workaround 1: 静态辅助方法
class SubClass extends SuperClass {
    SubClass(String raw) {
        super(validate(raw));  // 必须把验证逻辑藏在静态方法里
    }
    private static String validate(String s) {
        if (s == null || s.isBlank()) throw new IllegalArgumentException();
        return s.strip();
    }
}

// Workaround 2: 三元表达式塞进 super() 调用
class SubClass extends SuperClass {
    SubClass(int value) {
        super(value >= 0 ? value : throwIAE());  // 不可读
    }
}
```

#### 新语法 (New Syntax)

```java
class SubClass extends SuperClass {

    private final String normalizedName;

    SubClass(String raw) {
        // ===== Prologue (super() 之前) =====
        // 可以执行: 验证、计算、日志、资源获取
        Objects.requireNonNull(raw, "name must not be null");
        if (raw.isBlank()) {
            throw new IllegalArgumentException("name must not be blank");
        }
        var normalized = raw.strip().toLowerCase();
        System.out.println("Creating SubClass: " + normalized);

        // ===== Constructor invocation =====
        super(normalized);     // 可以使用 prologue 中计算的值

        // ===== Epilogue (super() 之后) =====
        this.normalizedName = normalized;
    }
}

// Prologue 中的限制 (restrictions in prologue):
// ✗ 不能访问 this (实例尚未初始化)
// ✗ 不能访问实例字段
// ✗ 不能调用实例方法
// ✗ 不能使用 super.xxx
// ✓ 可以访问参数
// ✓ 可以声明局部变量
// ✓ 可以调用静态方法
// ✓ 可以抛出异常
// ✓ 可以使用控制流语句 (if, for, try-catch 等)
```

#### 实际场景: Record 的辅助构造器

```java
record Connection(String host, int port, boolean secure) {

    // 紧凑构造器验证
    Connection {
        Objects.requireNonNull(host);
        if (port < 0 || port > 65535) throw new IllegalArgumentException("bad port");
    }

    // 从 URL 字符串解析 - 使用 flexible constructor body
    Connection(String url) {
        // Prologue: 在 this() 之前解析 URL
        var uri = URI.create(url);
        var scheme = uri.getScheme();
        var resolvedPort = uri.getPort() == -1
            ? ("https".equals(scheme) ? 443 : 80)
            : uri.getPort();

        // 委托给规范构造器
        this(uri.getHost(), resolvedPort, "https".equals(scheme));
    }
}

// 使用
var c1 = new Connection("example.com", 443, true);
var c2 = new Connection("https://example.com/api");  // 自动解析
```

---

### 3.10 Primitive Patterns (JEP 455 → 488 → 507 → 530)

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

### 3.11 String Templates (已撤回 - JEP 430 → 459 → 465)

#### 原始设计 (Original Design)

```java
// JDK 21/22 预览期间的语法 (已不再可用)
// 使用模板处理器 (template processor) + 模板表达式 (template expression)

String name = "Alice";
int age = 30;

// STR 处理器: 简单字符串插值
String msg = STR."Hello \{name}, you are \{age} years old.";

// FMT 处理器: 带格式化的插值
String formatted = FMT."%-10s\{name} is %5d\{age} years old.";

// 自定义处理器: 可以实现 SQL 注入防护等
PreparedStatement stmt = DB."SELECT * FROM users WHERE name = \{name}";
// DB 处理器会自动将 \{name} 转为 ? 占位符
```

#### 为什么撤回 (Why Withdrawn)

String Templates 在经过两轮预览后于 JDK 23 被**撤回** (JEP 465, Closed/Withdrawn)。
Brian Goetz 在邮件列表中解释了主要原因:

1. **过度工程化 (over-engineering)**: 模板处理器 (template processor) 的概念
   过于复杂。大多数开发者只需要简单的字符串插值 (`STR."..."`)，
   但为了支持自定义处理器 (如 SQL 安全), 整个设计变得笨重。

2. **类型系统问题**: `StringTemplate` 作为一种新类型引入，
   与现有的 `String` 类型之间的关系不清晰。
   `STR."Hello \{name}"` 返回 `String`，但裸模板表达式
   `"Hello \{name}"` 返回 `StringTemplate`，这个区分让人困惑。

3. **安全性目标未达成**: 最初的设计目标之一是通过自定义处理器
   防止 SQL 注入等安全问题，但实际上开发者总是可以先用 `STR` 拼接
   再传给 SQL，安全性无法通过类型系统强制保证。

4. **社区反馈**: 大量反馈认为 `\{expr}` 语法不直观，
   而且 `STR.` 前缀是不必要的噪音。其他 JVM 语言 (Kotlin: `"$var"`,
   Scala: `s"$var"`) 的插值语法更简洁。

#### 教训 (Lessons Learned)

- **简单需求不要复杂方案**: 字符串插值是一个"简单"需求，
  不应该承担"防止 SQL 注入"这样的安全职责
- **预览机制的价值**: Preview feature 机制正是为了在正式发布前
  发现这类问题。撤回是正确的决策，比发布一个有缺陷的特性好得多
- **可能的未来方向**: Brian Goetz 暗示未来可能以更简单的形式重新引入
  字符串插值，但截至 2026 年初尚无新的 JEP 提案

---

### 3.12 Stream Gatherers (JEP 485)

JDK 24 正式发布。Gatherers 是 Stream API 的扩展，
允许定义**自定义中间操作** (custom intermediate operations)，
弥补了 Stream API 只能通过 `Collector` 自定义终端操作的不足。

#### 核心概念 (Core Concepts)

```java
// Stream 管道: source → intermediate ops → terminal op
// 内置中间操作: map, filter, flatMap, sorted, distinct, limit...
// 自定义终端操作: Collector (JDK 8)
// 自定义中间操作: Gatherer (JDK 24) ← 新增！

// 使用方式: stream.gather(myGatherer)
// Gatherer 接口: Gatherer<T, A, R>
//   T = 输入元素类型 (input type)
//   A = 中间状态类型 (state type)
//   R = 输出元素类型 (output type)
```

#### 内置 Gatherers (Built-in Gatherers)

```java
import java.util.stream.Gatherers;

// 1. windowFixed(int size) - 固定大小的窗口 (fixed-size window)
List<List<Integer>> windows = Stream.of(1, 2, 3, 4, 5, 6, 7)
    .gather(Gatherers.windowFixed(3))
    .toList();
// [[1, 2, 3], [4, 5, 6], [7]]

// 2. windowSliding(int size) - 滑动窗口 (sliding window)
List<List<Integer>> sliding = Stream.of(1, 2, 3, 4, 5)
    .gather(Gatherers.windowSliding(3))
    .toList();
// [[1, 2, 3], [2, 3, 4], [3, 4, 5]]

// 3. fold(init, folder) - 有状态的归约, 输出单个结果
// 类似 reduce, 但初始值可以是不同类型
Optional<String> csv = Stream.of("a", "b", "c")
    .gather(Gatherers.fold(() -> "", (acc, el) -> acc.isEmpty() ? el : acc + "," + el))
    .findFirst();
// "a,b,c"

// 4. scan(init, scanner) - 有状态的累积, 输出每步结果
// 类似 fold, 但每步都输出中间结果
List<Integer> runningSum = Stream.of(1, 2, 3, 4, 5)
    .gather(Gatherers.scan(() -> 0, Integer::sum))
    .toList();
// [1, 3, 6, 10, 15]

// 5. mapConcurrent(maxConcurrency, mapper) - 并发映射
// 自动使用虚拟线程, 限制最大并发数
List<String> results = urls.stream()
    .gather(Gatherers.mapConcurrent(10, url -> fetchContent(url)))
    .toList();
// 最多 10 个虚拟线程同时执行 fetchContent
```

#### 自定义 Gatherer (Custom Gatherer)

```java
// Gatherer 由 4 个函数组成:
// 1. initializer  - 创建初始状态 (可选)
// 2. integrator   - 处理每个输入元素 (必需)
// 3. combiner     - 合并并行状态 (可选, 并行流需要)
// 4. finisher     - 处理最终状态 (可选)

// 示例 1: distinctBy - 按某个属性去重
static <T, K> Gatherer<T, ?, T> distinctBy(Function<T, K> keyExtractor) {
    return Gatherer.ofSequential(
        HashSet<K>::new,                         // initializer: 创建 Set 记录已见的 key
        (seen, element, downstream) -> {         // integrator
            K key = keyExtractor.apply(element);
            if (seen.add(key)) {                 // 如果 key 是新的
                return downstream.push(element); // 推送到下游
            }
            return true;                         // 继续处理 (返回 false 则短路)
        }
    );
}

// 使用
record Employee(String name, String dept) {}
var unique = employees.stream()
    .gather(distinctBy(Employee::dept))  // 每个部门只保留第一个
    .toList();

// 示例 2: takeWhileInclusive - 类似 takeWhile 但包含第一个不满足条件的元素
static <T> Gatherer<T, ?, T> takeWhileInclusive(Predicate<T> predicate) {
    return Gatherer.ofSequential(
        () -> new Object() { boolean done = false; },
        (state, element, downstream) -> {
            if (state.done) return false;        // 已结束, 短路
            if (!predicate.test(element)) {
                state.done = true;
            }
            return downstream.push(element);     // 包含不满足条件的那个元素
        }
    );
}

// 使用
var result = Stream.of(1, 2, 3, 10, 4, 5)
    .gather(takeWhileInclusive(n -> n < 10))
    .toList();
// [1, 2, 3, 10]  ← 包含了 10

// 示例 3: 带 finisher 的 Gatherer - 批量收集后在结束时输出最后一批
static <T> Gatherer<T, ?, List<T>> batch(int size) {
    return Gatherer.ofSequential(
        ArrayList<T>::new,                       // initializer
        (buffer, element, downstream) -> {       // integrator
            buffer.add(element);
            if (buffer.size() >= size) {
                var batch = List.copyOf(buffer);
                buffer.clear();
                return downstream.push(batch);
            }
            return true;
        },
        (buffer, downstream) -> {                // finisher
            if (!buffer.isEmpty()) {
                downstream.push(List.copyOf(buffer));  // 输出最后不足 size 的一批
            }
        }
    );
}
```

#### Gatherer 组合 (Composition)

```java
// Gatherer 可以通过 andThen 组合
var pipeline = Gatherers.<String>windowSliding(3)
    .andThen(Gatherers.mapConcurrent(4, window ->
        window.stream().mapToInt(String::length).average().orElse(0)));

var movingAvgLengths = words.stream()
    .gather(pipeline)
    .toList();
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
| **2024** | JDK 23 | Stream Gatherers (第二预览, JEP 473) |
| **2024** | JDK 24 | Stream Gatherers (正式, JEP 485) |
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
| Viktor Klang | Oracle | Stream Gatherers |

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
│        │                  - Gatherers.mapConcurrent      │
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
| **Stream Gatherers** | JEP 485 | JDK 24 | 自定义 Stream 中间操作 |
| **Compact Source Files & Instance Main** | JEP 512 | JDK 25 | 简化 Java 入门语法 |
| **Module Import Declarations** | JEP 511 | JDK 25 | 简洁导入模块导出包 |
| **Flexible Constructor Bodies** | JEP 513 | JDK 25 | 构造器中可在 super() 前执行语句 |

### 已撤回特性

| 特性 | JEP | 撤回时间 | 原因 |
|------|-----|----------|------|
| **String Templates** | 430 → 459 → 465 | 2024年6月 | 过度工程化，设计需重新评估 |

**String Templates 撤回详情**：
- JDK 21: 第一预览 (JEP 430)
- JDK 22: 第二预览 (JEP 459)
- JDK 23: **撤回** (JEP 465 Closed/Withdrawn)
- 原因：模板处理器概念过于复杂，类型系统设计不清晰，安全性目标未达成，社区对语法设计有广泛分歧

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
- [JEP 485: Stream Gatherers](https://openjdk.org/jeps/485)

### 预览中 / 撤回的 JEP
- [JEP 447: Statements before super (Preview)](https://openjdk.org/jeps/447)
- [JEP 463](/jeps/language/jep-463.md)
- [JEP 455](/jeps/tools/jep-455.md)
- [JEP 430](/jeps/language/jep-430.md)
- [JEP 465: String Templates (Third Preview - Withdrawn)](https://openjdk.org/jeps/465)

→ [相关主题: Records](../records/) | [模式匹配](../patterns/) | [语法演进](../../language/syntax/)
