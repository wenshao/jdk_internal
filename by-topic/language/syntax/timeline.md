# 语法演进时间线

Java 语言语法从 JDK 1.0 到 JDK 26 的完整演进历程。

---
## 目录

1. [时间线概览](#1-时间线概览)
2. [时间线详情](#2-时间线详情)
3. [语法对比表](#3-语法对比表)
4. [最佳实践](#4-最佳实践)
5. [贡献者](#5-贡献者)
6. [相关 JEP](#6-相关-jep)

---


## 1. 时间线概览

```
JDK 1.0 ──── JDK 5 ──── JDK 7 ──── JDK 8 ──── JDK 14 ──── JDK 16 ──── JDK 17 ──── JDK 21 ──── JDK 23 ──── JDK 26
 │            │           │           │           │           │           │           │           │           │
 类/接口      泛型        Diamond    Lambda     Records    Pattern    Sealed     String     Implicit   Primitive
              枚举        Try-resource instanceof Matching  Classes    Templates  Classes    Patterns
              变参        二进制字面量            Switch      (正式)
              注解        字面串下划线
              for-each    多异常捕获
```

---

## 2. 时间线详情

### JDK 1.0 (1996) - 基础语法

```java
// 基础类定义
public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() { return name; }
    public int getAge() { return age; }
}

// 接口
interface Runnable {
    void run();
}

// 继承
class Employee extends Person {
    private double salary;
}
```

### JDK 1.1 - 内部类

```java
// 成员内部类
public class Outer {
    class Inner {
        void method() {
            // 可访问外部类成员
        }
    }
}

// 匿名内部类
Runnable runnable = new Runnable() {
    public void run() {
        System.out.println("Running");
    }
};
```

### JDK 1.4 - assert

```java
// 断言
private void process(int value) {
    assert value > 0 : "Value must be positive";
    // ...
}

// 启用断言
java -ea MyApp
```

### JDK 5 (2004) - 重大语法更新 (JSR 14)

#### 泛型 (Generics)

```java
// 泛型类
public class Box<T> {
    private T value;

    public void set(T value) { this.value = value; }
    public T get() { return value; }
}

// 泛型方法
public static <T> T swap(T[] array, int i, int j) {
    T temp = array[i];
    array[i] = array[j];
    array[j] = temp;
    return temp;
}

// 通配符
List<?> unknownList;
List<? extends Number> upperBounded;
List<? super Integer> lowerBounded;
```

#### 枚举 (Enum)

```java
// 基础枚举
public enum Status {
    PENDING, APPROVED, REJECTED;
}

// 带方法和字段的枚举
public enum Planet {
    MERCURY(3.30e23, 2.44e6),
    VENUS(4.87e24, 6.05e6),
    EARTH(5.98e24, 6.37e6);

    private final double mass;
    private final double radius;

    Planet(double mass, double radius) {
        this.mass = mass;
        this.radius = radius;
    }

    public double mass() { return mass; }
}
```

#### 变参 (Varargs)

```java
public void printAll(String... args) {
    for (String arg : args) {
        System.out.println(arg);
    }
}

printAll("A", "B", "C");
```

#### 注解 (Annotations)

```java
// 定义注解
public @interface Deprecated {
    String since() default "";
}

// 使用注解
@Deprecated(since = "1.2")
public void oldMethod() { }
```

#### 增强 for 循环

```java
// 集合遍历
List<String> list = Arrays.asList("A", "B", "C");
for (String item : list) {
    System.out.println(item);
}

// 数组遍历
int[] array = {1, 2, 3};
for (int value : array) {
    System.out.println(value);
}
```

#### 静态导入

```java
import static java.lang.Math.*;
import static java.util.Collections.*;

double result = sqrt(25.0);
List<String> list = emptyList();
```

#### 自动装箱/拆箱

```java
// 自动装箱
Integer integer = 42;

// 自动拆箱
int value = integer;

// 泛型与自动装箱
List<Integer> numbers = new ArrayList<Integer>();
numbers.add(10);  // 自动装箱
int sum = numbers.get(0);  // 自动拆箱
```

### JDK 7 (2011) - 语法增强

#### Diamond 操作符

```java
// 类型推断
Map<String, List<Integer>> map =
    new HashMap<>();  // JDK 7+
```

#### Try-with-resources

```java
// 自动资源管理
try (FileInputStream fis = new FileInputStream("input.txt");
     BufferedReader br = new BufferedReader(new InputStreamReader(fis))) {
    // 资源自动关闭
} catch (IOException e) {
    e.printStackTrace();
}
```

#### 多异常捕获

```java
try {
    // ...
} catch (IOException | SQLException e) {
    // 捕获多个异常
    e.printStackTrace();
}
```

#### 二进制字面量

```java
int binary = 0b101010;  // 42
int hex = 0x2A;         // 42
```

#### 字面串下划线

```java
int million = 1_000_000;
long creditCard = 1234_5678_9012_3456L;
double pi = 3.141_592_653;
```

#### switch 字符串

```java
String day = "MONDAY";
switch (day) {
    case "MONDAY":
    case "FRIDAY":
        System.out.println("Work");
        break;
    default:
        System.out.println("Rest");
}
```

### JDK 8 (2014) - Lambda 表达式

**JEP 126** - **Brian Goetz** (Specification Lead, JSR-335)

#### Lambda 表达式

```java
// Lambda 语法
// (parameters) -> expression
// (parameters) -> { statements; }

// 无参数
Runnable runnable = () -> System.out.println("Hello");

// 单参数
Predicate<Integer> isEven = n -> n % 2 == 0;

// 多参数
BiFunction<Integer, Integer, Integer> add = (a, b) -> a + b;

// 多语句
Function<Integer, Integer> factorial = n -> {
    if (n <= 1) return 1;
    return n * factorial.apply(n - 1);
};
```

#### 方法引用

```java
// 静态方法引用
Function<String, Integer> parseInt = Integer::parseInt;

// 实例方法引用
List<String> list = Arrays.asList("a", "b", "c");
list.forEach(System.out::println);

// 构造器引用
Supplier<List<String>> listFactory = ArrayList::new;

// 数组构造器引用
Function<Integer, int[]> arrayFactory = int[]::new;
```

#### 默认方法

```java
interface Interface {
    void abstractMethod();

    default void defaultMethod() {
        System.out.println("Default implementation");
    }

    static void staticMethod() {
        System.out.println("Static method");
    }
}
```

### JDK 9 - 私有接口方法

```java
interface Interface {
    default void method1() {
        commonMethod();
    }

    default void method2() {
        commonMethod();
    }

    private void commonMethod() {
        // 共享私有逻辑
    }

    private static void staticCommon() {
        // 静态私有方法
    }
}
```

### JDK 10 - 局部变量类型推断

```java
// var 关键字
var name = "John";           // String
var age = 25;                // int
var list = new List<String>(); // List<String>

// 在 for 循环中
for (var item : list) {
    System.out.println(item);
}

// 注意: var 不能用于字段、方法参数、返回类型
```

### JDK 14 - Records 预览

**JEP 395** - **Gavin Bierman**, Brian Goetz

```java
// Record - 不可变数据载体
public record Person(String name, int age) { }

// 使用
Person person = new Person("Alice", 25);
System.out.println(person.name());  // 自动生成 accessor
System.out.println(person.age());

// 带验证的 Record
public record Range(int min, int max) {
    public Range {
        if (min > max) {
            throw new IllegalArgumentException();
        }
    }
}
```

### JDK 14 - instanceof 模式匹配 (预览)

**JEP 305** - **Gavin Bierman**

```java
// JDK 14 之前
if (obj instanceof String) {
    String str = (String) obj;
    System.out.println(str.length());
}

// JDK 14+ 模式匹配
if (obj instanceof String str) {
    System.out.println(str.length());  // 无需强制转换
}
```

### JDK 15 - Records (第二次预览)

```java
// Record 可以实现接口
public record Person(String name, int age)
    implements Comparable<Person> {

    @Override
    public int compareTo(Person other) {
        return this.name.compareTo(other.name);
    }
}
```

### JDK 15 - 文本块 (正式)

```java
// 多行字符串
String json = """
    {
        "name": "John",
        "age": 30
    }
    """;
```

### JDK 16 - Records (正式)

```java
// Records 正式发布
public record Point(int x, int y) { }
```

### JDK 16 - instanceof 模式匹配 (正式)

```java
// 模式变量在条件块外可用
if (obj instanceof String s && s.length() > 5) {
    System.out.println(s);  // s 可用
}
```

### JDK 17 - Sealed Classes (正式)

**JEP 409** - **Gavin Bierman** (Owner)

```java
// 密封类 - 限制继承
public sealed class Shape
    permits Circle, Rectangle, Square {

    public double area() { return 0; }
}

public final class Circle extends Shape {
    private final double radius;
    // ...
}

public final class Rectangle extends Shape {
    private final double width, height;
    // ...
}

public final class Square extends Shape {
    private final double side;
    // ...
}
```

### JDK 17 - 模式匹配 switch (预览)

**JEP 406** - **Gavin Bierman**, Brian Goetz

```java
// switch 类型模式
String formatted = switch (obj) {
    case Integer i -> String.format("int %d", i);
    case Long l    -> String.format("long %d", l);
    case Double d  -> String.format("double %f", d);
    case String s  -> String.format("String %s", s);
    default        -> obj.toString();
};
```

### JDK 18 - final 判定

```java
// JEP 421: 不会隐式修改 final 变量的模式
// 增强模式匹配的安全性
```

### JDK 19 - Record Patterns (预览)

**JEP 405** - **Gavin Bierman**

```java
// Record 模式匹配
record Point(int x, int y) {}

// 模式匹配 Record
if (obj instanceof Point(int x, int y)) {
    System.out.println("x=" + x + ", y=" + y);
}

// 嵌套模式
record ColoredPoint(Point point, String color) {}
record Rectangle(ColoredPoint upperLeft, ColoredPoint lowerRight) {}

if (obj instanceof Rectangle(
    ColoredPoint(Point(int x1, int y1), String color1),
    ColoredPoint(Point(int x2, int y2), String color2)
)) {
    // 解构嵌套 Record
}
```

### JDK 19 - switch 模式匹配增强

```java
// when 子句
static String formatter(Object obj) {
    return switch (obj) {
        case Integer i when i > 0 -> "positive integer";
        case Integer i             -> "other integer";
        case String s when s.length() > 5 -> "long string";
        case String s              -> "short string";
        default                    -> "unknown";
    };
}
```

### JDK 20 - Record Patterns (第二次预览)

```java
// 增强的 Record 模式
record Point(int x, int y) {}

void printSum(Object obj) {
    if (obj instanceof Point(int x, int y)) {
        System.out.println(x + y);
    }
}
```

### JDK 21 - String Templates (预览)

**JEP 430** - **Jim Laskey**, Brian Goetz

```java
// STR 模板处理器
String name = "Alice";
int age = 25;
String message = STR."Hello \{name}, you are \{age} years old";

// FMT 格式化处理器
String pi = FMT."Pi = \{Math.PI}%.2f";

// RAW 原始处理器
String json = RAW."""
    {"name": "\{name}", "age": \{age}}
    """;
```

### JDK 21 - Record Patterns (正式)

```java
// Record 模式正式发布
record Point(int x, int y) {}
record Circle(Point center, int radius) {}

// 在 switch 中使用
String describe(Object obj) {
    return switch (obj) {
        case Point(int x, int y) -> "Point at (%d, %d)".formatted(x, y);
        case Circle(Point(int x, int y), int r) -> "Circle center (%d,%d) r=%d".formatted(x, y, r);
        default -> "Unknown shape";
    };
}
```

### JDK 21 - 模式匹配 switch (正式, JEP 441)

```java
// 完整的 switch 模式匹配
sealed interface Shape permits Circle, Rectangle {}
record Circle(int radius) implements Shape {}
record Rectangle(int width, int height) implements Shape {}

static double area(Shape shape) {
    return switch (shape) {
        case Circle(int r) -> Math.PI * r * r;
        case Rectangle(int w, int h) -> w * h;
    };
}
```

### JDK 21 - 未命名模式和变量

```java
// 使用 _ 表示未命名的模式组件
record Point(int x, int y) {}

if (obj instanceof Point(int x, _)) {
    // 只关心 x，忽略 y
    System.out.println("x = " + x);
}

// 在 lambda 中
BiFunction<Integer, Integer, Integer> add = (a, _) -> a;  // 忽略第二个参数
```

### JDK 21 - 隐式类

**JEP 463** - **Gavin Bierman**, Jim Laskey

```java
// 隐式类 - 用于脚本风格
void main() {
    System.out.println("Hello, World!");
}

// 等价于
void main() {
    class Main {
        private void main() {
            System.out.println("Hello, World!");
        }
    }
    new Main().main();
}
```

### JDK 22 - String Templates (第二次预览)

```java
// 模板表达式增强
StringTemplate.Processor<String, RuntimeException> JSON = st -> {
    // 自定义模板处理器
    return processJson(st);
};

String json = JSON."""
    {"name": "\{name}", "age": \{age}}
    """;
```

### JDK 22 - 隐式类 (第二次预览)

```java
// 增强的隐式类支持
// 允许静态成员
static int count = 0;

void main() {
    System.out.println("Count: " + count);
}
```

### JDK 22 - 未命名类和实例主方法 (预览)

```java
// 简化的主类
class HelloWorld {
    void main() {
        System.out.println("Hello, World!");
    }
}
```

### JDK 23 - 隐式类 (第三次预览)

```java
// 持续改进的隐式类
void main() {
    var greet = "Hello";
    System.out.println(greet);
}
```

### JDK 23 - 模式匹配简化

```java
// 更简洁的模式匹配语法
if (obj instanceof Point(int x, int y)) {
    System.out.println(x + y);
}
```

### JDK 23 - Primitive Types in Patterns

```java
// 原始类型模式匹配
void test(Object obj) {
    switch (obj) {
        case int i -> System.out.println("int: " + i);
        case long l -> System.out.println("long: " + l);
        case double d -> System.out.println("double: " + d);
        default -> System.out.println("other");
    }
}
```

### JDK 23 - String Templates 撤回

**JEP 430 已撤回**

```java
// ⚠️ String Templates 在 JDK 21-22 预览后
// 从 JDK 23 开始移除，不再继续预览

// 原计划语法:
String name = "World";
String message = STR."Hello \{name}!";
```

**撤回原因**:
- 设计需要进一步讨论
- 社区反馈需要更多考虑
- 没有确定何时会重新引入

### JDK 24-25 - String Templates 未发布

由于 JEP 430 已撤回，JDK 24-25 没有继续此特性的预览。

### JDK 25 - 隐式类 (正式)

```java
// 隐式类正式发布
void main() {
    System.out.println("Hello!");
}
```

### JDK 26 - 模式匹配全面增强

```java
// 原始类型模式正式
// 完整的 switch 模式匹配
// Record 模式增强

// 综合示例
sealed interface Vehicle permits Car, Bicycle {}
record Car(String model, int seats) implements Vehicle {}
record Bicycle(String brand, int gears) implements Vehicle {}

String describe(Vehicle v) {
    return switch (v) {
        case Car(String model, int seats) when seats > 2
            -> "Family car: " + model;
        case Car(String model, _)
            -> "Sports car: " + model;
        case Bicycle(_, int gears) when gears > 18
            -> "Pro bicycle with " + gears + " gears";
        default -> "Standard vehicle";
    };
}
```

---

## 3. 语法对比表

| 特性 | 引入版本 | 语法示例 |
|------|----------|----------|
| 内部类 | JDK 1.1 | `class Outer { class Inner {} }` |
| 断言 | JDK 1.4 | `assert condition : message;` |
| 泛型 | JDK 5 | `List<String>` |
| 枚举 | JDK 5 | `enum E { A, B }` |
| 变参 | JDK 5 | `void method(T... args)` |
| 注解 | JDK 5 | `@Override` |
| 增强 for | JDK 5 | `for (T item : collection)` |
| 静态导入 | JDK 5 | `import static Math.*;` |
| 自动装箱 | JDK 5 | `Integer i = 42;` |
| Diamond | JDK 7 | `new List<>()` |
| Try-with-resources | JDK 7 | `try (Resource r = ...)` |
| 多异常捕获 | JDK 7 | `catch (A \| B e)` |
| 二进制字面量 | JDK 7 | `0b1010` |
| Lambda | JDK 8 | `x -> x * 2` |
| 方法引用 | JDK 8 | `Object::method` |
| 默认方法 | JDK 8 | `default void method() {}` |
| var | JDK 10 | `var x = 10;` |
| Records | JDK 16 | `record P(int x, int y) {}` |
| instanceof 模式 | JDK 16 | `obj instanceof String s` |
| Sealed Classes | JDK 17 | `sealed class C permits S1, S2 {}` |
| switch 模式 | JDK 21 | `case Type t -> ...` |
| Record Patterns | JDK 21 | `case P(int x, int y)` |
| String Templates | ~~JDK 21+~~ | **已撤回** (JEP 430) |
| 隐式类 | JDK 25 | `void main() {}` |

---

## 4. 最佳实践

### 泛型

```java
// ✅ 推荐: 使用泛型确保类型安全
List<String> list = new ArrayList<>();

// ✅ 推荐: 使用有界通配符
public void process(List<? extends Number> numbers) { }

// ❌ 避免: 原始类型
List list = new ArrayList();  // 警告
```

### Lambda

```java
// ✅ 推荐: 简洁的 Lambda
list.forEach(item -> System.out.println(item));

// ✅ 推荐: 方法引用
list.forEach(System.out::println);

// ❌ 避免: 过度复杂的 Lambda
// 拆分为命名方法
```

### Records

```java
// ✅ 推荐: 数据载体使用 Record
public record Person(String name, int age) { }

// ❌ 避免: Record 中添加可变状态
// Record 设计为不可变
```

### Pattern Matching

```java
// ✅ 推荐: 使用模式匹配简化代码
if (obj instanceof String s && s.length() > 0) {
    return s.toUpperCase();
}

// ✅ 推荐: switch 表达式
String result = switch (value) {
    case 1 -> "one";
    case 2 -> "two";
    default -> "other";
};
```

---

## 5. 贡献者

### 核心 JEP 作者

| JEP | 特性 | 主要贡献者 | 公司 |
|-----|------|-----------|------|
| JEP 126 | Lambda Expressions | **Brian Goetz** | Oracle |
| JEP 395 | Records | **Gavin Bierman**, Brian Goetz | Oracle |
| JEP 409 | Sealed Classes | **Gavin Bierman** | Oracle |
| JEP 441 | Pattern Matching for switch | **Gavin Bierman**, Brian Goetz | Oracle |
| JEP 440 | Record Patterns | **Gavin Bierman** | Oracle |
| JEP 430 | String Templates | **Jim Laskey**, Brian Goetz | Oracle |
| JEP 443 | Unnamed Patterns | **Gavin Bierman** | Oracle |
| JEP 477 | Implicitly Declared Classes | **Gavin Bierman**, Jim Laskey | Oracle |

### Brian Goetz

- **职位**: Java Language Architect, Oracle
- **代表作**: 《Java Concurrency in Practice》作者
- **主要贡献**:
  - JSR-335 Specification Lead (Lambda Expressions)
  - 主导 Java 8 函数式编程特性
  - 参与 Records、Pattern Matching、String Templates 等多个 JEP

> "Lambda expressions enable you to treat functionality as a method argument, or code as data."
> — Brian Goetz, JSR-335 Specification Lead

### Gavin Bierman

- **职位**: Consulting Member of Technical Staff, Oracle Labs
- **背景**:
  - PhD, University of Cambridge
  - BSc, Imperial College
  - 前微软剑桥研究院高级研究员 (2004-2014)
  - 加入 Oracle (2014-)
- **主要贡献**:
  - Records (JEP 395)
  - Sealed Classes (JEP 409)
  - Pattern Matching for instanceof (JEP 305/394)
  - Pattern Matching for switch (JEP 441)
  - Record Patterns (JEP 440)
  - Unnamed Patterns and Variables (JEP 443)

### Jim Laskey

- **职位**: Consulting Member of Technical Staff, Oracle
- **主要贡献**:
  - String Templates (JEP 430)
  - Text Blocks (JEP 378)
  - Implicitly Declared Classes (JEP 477)

---

## 6. 相关 JEP

- [Language Changes in Java SE](https://docs.oracle.com/en/java/javase/21/whatsnew/index.html)
- [Java Language Specification](https://docs.oracle.com/javase/specs/jls/se21/html/index.html)
